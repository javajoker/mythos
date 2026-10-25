#!/usr/bin/env python3
"""Lift LLM-authored entity readings (人文風物資源 identifications) from the
sentence-analysis documents into KG attributes.

Source of truth: each <slug>-sentence-analysis.md — §2 bullet expansions (full
reading text) and §3 era-mapping table rows (compact classification + era state).
This tool only restructures LLM-authored text into attribute records; it makes
no semantic decisions. Geo types (MTN/WAT/LND) are skipped — they are covered by
kg_v1_assemble.py (ATTMAP records). Idempotent: ATTRD records are rebuilt.

Usage: python3 tools/shj/kg_readings_build.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
GEO_TYPES = {"MTN", "WAT", "LND"}
SKIP_TYPES = GEO_TYPES | {"DOC"}
PLACEHOLDERS = {"見 §2 展開", "—", "-", ""}

ROW = re.compile(r"^\| ([A-Z]+):…(\d{3})#(\d+) *\| *([^|]*?) *\| *([^|]*?) *\| *([^|]*?) *\| *([^|]*?) *\| *([^|]*?) *\|$")
ENTRY_HEAD = re.compile(r"^### 【(SHJ-\d{2}-\d+-\d{3})】")
REF = re.compile(r"`([A-Z]+):(?:SHJ-(\d{2})-(\d+)-(\d{3})|…(\d{3})?)#(\d+)`")


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def clean_md(s):
    return re.sub(r"\s+", " ", re.sub(r"[`*]", "", s)).strip()


def parse_doc(path):
    """Return {node_id: {name, attr, coord, classification, status, entry, s2}}"""
    text = path.open(encoding="utf-8").read()
    nodes = {}
    by_name = {}  # (entry, leading name) -> segment; fallback for §2/§3 numbering drift
    current_entry = None
    for line in text.split("\n"):
        h = ENTRY_HEAD.match(line)
        if h:
            current_entry = h.group(1)
            continue
        r = ROW.match(line)
        if r and current_entry:
            typ, suf, num, name, attr, coord, cls, status = r.groups()
            nid = f"{typ}:{current_entry}#{num}"
            prev = nodes.get(nid)
            nodes[nid] = {"name": name.strip(), "attr": attr.strip(), "coord": coord.strip(),
                          "classification": cls.strip(), "status": status.strip(),
                          "entry": current_entry, "s2": prev["s2"] if prev else None}
            continue
        # §2 bullets: backticked node refs; segment runs to the next ref
        if line.strip().startswith(("-", "*")) and "`" in line:
            refs = list(REF.finditer(line))
            for i, m in enumerate(refs):
                if m.group(2):
                    nid = f"{m.group(1)}:SHJ-{m.group(2)}-{m.group(3)}-{m.group(4)}#{m.group(6)}"
                elif m.group(5) and current_entry:
                    nid = f"{m.group(1)}:{current_entry.rsplit('-',1)[0]}-{m.group(5)}#{m.group(6)}"
                elif current_entry:
                    nid = f"{m.group(1)}:{current_entry}#{m.group(6)}"
                else:
                    continue
                seg = line[m.end(): refs[i + 1].start() if i + 1 < len(refs) else len(line)]
                seg = clean_md(seg)
                seg = re.sub(r"^[：:，,、\s]+", "", seg)
                if current_entry and "：" in seg:
                    lead = seg.split("：", 1)[0].strip()
                    by_name.setdefault((current_entry, lead), seg.split("：", 1)[1])
                if nid in nodes and nodes[nid]["s2"] is None and seg:
                    nodes[nid]["s2"] = seg
                elif nid not in nodes:
                    nodes.setdefault(nid, {"name": "", "attr": "", "coord": "", "classification": "",
                                           "status": "", "entry": nid.split(":")[1].rsplit("#", 1)[0],
                                           "s2": seg})
    # fallback: fill s2 by (entry, name) where ref numbering drifted
    for nid, info in nodes.items():
        if info["s2"] is None and info["name"]:
            seg = by_name.get((info["entry"], info["name"]))
            if seg:
                info["s2"] = seg
    return nodes


def main():
    kg_nodes = {n["id"] for n in read_jsonl(KG / "nodes.jsonl")}
    # LLM-authored supplement for readings not recoverable by structure
    # (无引用符號的 §2 段、編號漂移、基準/祀制類)
    supplement = {}
    sup_path = ADJ / "readings-supplement.jsonl"
    if sup_path.exists():
        for row in read_jsonl(sup_path):
            supplement[row["node"]] = row
    records = []
    stats = {"identified": 0, "state_only": 0, "no_reading": 0, "skipped_geo": 0, "not_in_kg": 0}
    no_reading_samples = []
    for path in sorted(ADJ.glob("*-sentence-analysis.md")):
        slug = path.name.replace("-sentence-analysis.md", "")
        for nid, info in parse_doc(path).items():
            typ = nid.split(":")[0]
            if typ in SKIP_TYPES:
                stats["skipped_geo"] += 1
                continue
            if nid not in kg_nodes:
                stats["not_in_kg"] += 1
                continue
            cls, s2 = info["classification"], info["s2"]
            has_cls = cls and cls not in PLACEHOLDERS
            truncated = has_cls and cls.endswith("…")
            name_reading, fit = None, None
            if has_cls and not truncated:
                name_reading, fit = cls, s2 or cls
            elif s2:
                first = re.split(r"[；。]", s2)[0].strip()
                name_reading = first[:40]
                fit = s2 if not has_cls else f"{cls}｜{s2}"
            base = {
                "subject": nid,
                "kind": "semantic_fit",
                "status": "proposed",
                "confidence": None,
                "evidence": [{"entry": info["entry"]}],
                "provenance": {"package": f"era/adaptation/{slug}", "assembled": "kg-v1-readings",
                               "review_status": "proposed_pending_review",
                               "source": "sentence-analysis §2/§3"},
            }
            if name_reading:
                records.append({"id": f"ATTRD:{slug}:{nid}", "predicate": "era.candidate",
                                "value": {"role": "identification", "entity_attr": info["attr"],
                                          "name": name_reading, "fit": fit,
                                          "station_ref": info["coord"]},
                                **base})
                stats["identified"] += 1
            else:
                sup = supplement.get(nid)
                if sup:
                    records.append({"id": f"ATTRD:{slug}:{nid}", "predicate": "era.candidate",
                                    "value": {"role": "identification", "entity_attr": info["attr"],
                                              "name": sup["name"], "fit": sup["fit"],
                                              "station_ref": info["coord"]},
                                    **base})
                    stats["identified"] += 1
                else:
                    stats["no_reading"] += 1
                    if len(no_reading_samples) < 15:
                        no_reading_samples.append((slug, nid, info["name"]))
            if info["status"]:
                records.append({"id": f"ATTRD:{slug}:{nid}:state", "predicate": "era.state",
                                "value": info["status"], **base})
                if not name_reading:
                    stats["state_only"] += 1

    # supplement-only nodes (entries with no sentence-analysis section, e.g. SHJ-05-13 總結段)
    seen = {r["subject"] for r in records}
    for nid, sup in supplement.items():
        if nid in seen or nid not in kg_nodes:
            continue
        records.append({"id": f"ATTRD:{sup['package']}:{nid}", "predicate": "era.candidate",
                        "subject": nid, "kind": "semantic_fit", "status": "proposed",
                        "confidence": None,
                        "value": {"role": "identification", "name": sup["name"], "fit": sup["fit"]},
                        "evidence": [{"entry": nid.split(":")[1].rsplit("#", 1)[0]}],
                        "provenance": {"package": f"era/adaptation/{sup['package']}",
                                       "assembled": "kg-v1-readings",
                                       "review_status": sup.get("review_status", "proposed_pending_review"),
                                       "source": "readings-supplement"}})
        stats["identified"] += 1

    attributes = [a for a in read_jsonl(KG / "attributes.jsonl") if not a.get("id", "").startswith("ATTRD:")]
    attributes.extend(records)
    write_jsonl(KG / "attributes.jsonl", attributes)

    manifest_path = KG / "build-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["kg_v1_readings"] = {
        "assembled_by": "kg_readings_build.py",
        "source": "era/adaptation/*-sentence-analysis.md (LLM-authored §2/§3)",
        "records": len(records),
        **stats,
        "attributes_total": len(attributes),
        "review_status": "proposed_pending_review",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"attributes.jsonl now {len(attributes)} records ({len(records)} reading records)")
    print("stats:", json.dumps(stats, ensure_ascii=False))
    if no_reading_samples:
        print("no-reading samples (基準/泛稱類，允許):")
        for s in no_reading_samples:
            print(" ", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
