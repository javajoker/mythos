#!/usr/bin/env python3
"""Export web-app static data from the Mythos KG + adaptation packages + draft-v2.

Read-only over sources; writes webapp/data/*.json, copies images/maps, and emits
manifest.json with reconciliation counts. No semantic decisions.

Usage: python3 tools/shj/webapp_export.py
"""
import hashlib
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHJ = ROOT / "projects/shanhaijing"
KG = SHJ / "data/derived/kg"
ADJ = SHJ / "data/derived/era/adaptation"
DRAFT = SHJ / "deliverables/draft-v2"
WEB = SHJ / "webapp"
DATA = WEB / "data"

BOOKS = {"01": ("nanci", 3, "南山經"), "02": ("xici", 4, "西山經"), "03": ("beici", 3, "北山經"),
         "04": ("dongci", 4, "東山經"), "05": ("zhongci", 13, "中山經")}
FRAMEWORK = {f"{i:02d}": name for i, name in enumerate(
    ["", "", "", "", "", "", "海外南經", "海外西經", "海外北經", "海外東經", "海內南經",
     "海內西經", "海內北經", "海內東經", "大荒東經", "大荒南經", "大荒西經", "大荒北經", "海內經"]) if name}


def read_jsonl(p):
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    manifest = {}

    # ---- graph.json ----
    nodes = read_jsonl(KG / "nodes.jsonl")
    edges = read_jsonl(KG / "edges.jsonl")
    attrs = read_jsonl(KG / "attributes.jsonl")
    by_subj = defaultdict(list)
    for a in attrs:
        by_subj[a["subject"]].append({"id": a["id"], "predicate": a["predicate"],
                                      "value": a["value"], "kind": a["kind"],
                                      "status": a["status"], "confidence": a.get("confidence")})
    graph = {
        "nodes": [{"id": n["id"], "type": n["type"], "name": n["canonical_name"],
                   "entry": n["first_entry"], "status": n.get("status", "active"),
                   "attrs": by_subj.get(n["id"], [])} for n in nodes],
        "edges": [{"id": e["id"], "src": e["src"], "dst": e["dst"], "type": e["type"],
                   "layer": e["layer"], "entry": e.get("entry"),
                   **({"bearing": e["bearing"]} if e.get("bearing") else {}),
                   "status": e.get("status")} for e in edges],
    }
    (DATA / "graph.json").write_text(json.dumps(graph, ensure_ascii=False), encoding="utf-8")
    manifest["graph"] = {"nodes": len(nodes), "edges": len(edges), "attributes": len(attrs),
                         "sha": sha(KG / "nodes.jsonl")}

    # ---- entries.json ----
    working = {e["entry_id"]: e for e in read_jsonl(SHJ / "data/derived/working-text.jsonl")
               if e.get("entry_id")}
    # name -> entry for framework points linkage
    fw_name2entry = {}
    for f in sorted(ADJ.glob("book*-mappings.jsonl")):
        for r in read_jsonl(f):
            if "disposition" in r:
                fw_name2entry.setdefault(r["name"], re.findall(r"SHJ-\d{2}-\d+-\d{3}", r.get("entry", ""))[0]
                                         if re.findall(r"SHJ-\d{2}-\d+-\d{3}", r.get("entry", "")) else None)
    entries = []
    matched = set()
    for md in sorted(DRAFT.glob("book-*.md")):
        bk = re.search(r"book-(\d+)-", md.name).group(1)
        text = md.read_text(encoding="utf-8")
        # split into sections at ### headings
        chunks = re.split(r"\n(?=### )", text)
        for ch in chunks:
            if not ch.startswith("### "):
                continue
            title = ch.split("\n", 1)[0].lstrip("# ").strip()
            quoted = []
            for l in ch.split("\n"):
                if not l.startswith(">"):
                    continue
                q = re.sub(r"^\*\*[^*]+\*\*[:：]?", "", l[1:].strip()).strip()
                if q:
                    quoted.append(q)
            original = " ".join(quoted)
            eid = None
            norm_orig = re.sub(r"\s+", "", original)
            for e, rec in working.items():
                if e in matched or not e.startswith(f"SHJ-{bk}-"):
                    continue
                t = re.sub(r"\s+", "", rec["text"])
                if norm_orig and (t[:40] in norm_orig or norm_orig[:40] in t):
                    eid = e
                    break
            body = re.sub(r"\*\*未[决決]项\*\*", "\n%%UNRESOLVED%%\n", ch)
            un = []
            if "%%UNRESOLVED%%" in body:
                after = body.split("%%UNRESOLVED%%", 1)[1]
                un = [l.lstrip("- ").strip() for l in after.split("\n") if l.strip().startswith("- ")]
            images = re.findall(r"!\[([^\]]*)\]\((images/[^)]+)\)", ch)
            entries.append({"id": eid, "book": bk, "title": title, "original": original,
                            "reading_md": ch, "images": [{"alt": a, "src": s} for a, s in images],
                            "unresolved": un})
            if eid:
                matched.add(eid)
    # fallback: order-pairing for books whose remaining counts agree (e.g. script variants)
    from collections import defaultdict as _dd
    by_book = _dd(list)
    for e in entries:
        if not e["id"]:
            by_book[e["book"]].append(e)
    for bk, secs in by_book.items():
        remaining = sorted([e for e in working if e.startswith(f"SHJ-{bk}-") and e not in matched],
                           key=lambda e: working[e]["seq"])
        if len(remaining) == len(secs):
            for e, rec in zip(secs, remaining):
                e["id"] = rec
                matched.add(rec)
    (DATA / "entries.json").write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    manifest["entries"] = {"sections": len(entries), "matched": len(matched),
                           "working_total": len(working)}

    # ---- map data ----
    wz = json.loads((ADJ / "specs/wuzang-overview.json").read_text(encoding="utf-8"))
    chains = []
    for ch in wz["chains"]:
        slug = ch["grid"].replace("-station-grid.jsonl", "")
        sts = [r for r in read_jsonl(ADJ / ch["grid"]) if "station" in r]
        spec_path = ADJ / "specs" / f"{slug}-map.json"
        fit = {}
        if ch.get("fit") and spec_path.exists():
            fit = {int(k): tuple(v) for k, v in json.loads(spec_path.read_text(encoding="utf-8")).get("fit_coords", {}).items()}
        pts = []
        for s in sts:
            g = s["grid"]["0.385"]
            if s["order"] in fit:
                g = {"lon": fit[s["order"]][0], "lat": fit[s["order"]][1]}
            pts.append({"n": s["station"], "o": s["order"], "lon": g["lon"], "lat": g["lat"]})
        chains.append({"label": ch["label"], "short": ch.get("short", ""), "color": ch["color"],
                       "anchor_index": ch.get("anchor_index"), "label_pos": ch.get("label_pos"),
                       "points": pts})
    (DATA / "map-chains.json").write_text(json.dumps({"window": wz["window"],
        "lon_wrap_below": wz.get("lon_wrap_below"), "chains": chains}, ensure_ascii=False), encoding="utf-8")
    sj = json.loads((ADJ / "specs/shanjing-overview.json").read_text(encoding="utf-8"))
    points = [{**p, "entry": fw_name2entry.get(p["name"])} for p in sj["points"]]
    (DATA / "map-points.json").write_text(json.dumps(points, ensure_ascii=False), encoding="utf-8")
    (DATA / "basemap.json").write_text(json.dumps(
        {"window": wz["window"], "lon_wrap_below": wz.get("lon_wrap_below"),
         "basemap": wz["basemap"], "annotations": wz.get("annotations", []),
         "modern": wz.get("modern", [])}, ensure_ascii=False), encoding="utf-8")
    manifest["maps"] = {"chains": len(chains), "points": len(points)}

    # ---- adjudications.json ----
    adjs = []
    for f in sorted((SHJ / "findings").glob("*.md")):
        head = f.read_text(encoding="utf-8").split("\n")[0].lstrip("# ").strip()
        adjs.append({"file": f"findings/{f.name}", "title": head})
    (DATA / "adjudications.json").write_text(json.dumps(adjs, ensure_ascii=False), encoding="utf-8")
    manifest["adjudications"] = len(adjs)

    # ---- images & maps ----
    (WEB / "images").mkdir(exist_ok=True)
    n_img = 0
    for img in DRAFT.glob("images/*"):
        dest = WEB / "images" / img.name
        if not dest.exists():
            shutil.copy2(img, dest)
        n_img += 1
    (WEB / "maps").mkdir(exist_ok=True)
    n_map = 0
    for svg in list(ADJ.glob("*-map.svg")) + list(ADJ.glob("*-overview.svg")):
        dest = WEB / "maps" / svg.name
        if not dest.exists():
            shutil.copy2(svg, dest)
        n_map += 1
    manifest["images"] = n_img
    manifest["maps"] = n_map
    (DATA / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
