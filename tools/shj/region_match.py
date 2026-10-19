"""Whole-book global mapping (Method G, stage G4): score every section of all 18 books — and a set of key named
places — against 31 world regions, by description only.

Features of a unit (names masked):
  property   a region property cued in the unit's text (tools/shj/cues.py REGION_CUES); "barren" when ≥ 30% of the
             unit's entries say 無草木. Present-only: silence is never evidence.
  fauna      each creature in the unit accepted by the animal map (cov ≥ 0.5); its real ranges.
Scoring per region (method-g-global.md §3): property T +w, F −w, unknown 0, w = log10(N_known/N_true) + 0.05;
fauna in range +w·cov, out of range −0.5·w·cov, w = log10(31/regions reached) + 0.05. Marine-only animals count for
coastal regions. Distances are not used; the book's own direction words are reported as a reference check only.

Unknown values: regions are not equally well documented (northern China has few unknowns, Siberia many), and a
plain "unknown = 0" lets well-documented regions collect more matches. An unknown is therefore scored at its base-rate
expectation, w·(2p − 1), where p = N_true / N_known for that property. (A uniform random-feature null was tried first
and rejected: it rewarded regions marked absent for many properties whenever a section's features were merely
unknown for them.)
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cues import RE_BARREN, mask_names, region_cue_hits  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
AMAP = ROOT / "projects/shanhaijing/data/derived/animal-map.jsonl"
WORLD = ROOT / "projects/shanhaijing/data/world"
OUT = ROOT / "projects/shanhaijing/data/derived"
SKIP_SECTIONS = {"五臧山經"}
CUSTOMS = {"tattoo", "black_teeth", "ear_ornaments", "feather_dress", "hairy_people", "pygmy_people", "dark_skin",
           "cave_dwelling"}
# Key named places, mention-based (every entry naming them); 崑崙 uses its subject passages (H-0006).
NAMED = {
    "崑崙（主語段落）/ Kunlun (subject passages)": {"ids": ["SHJ-02-3-008", "SHJ-06-1-017", "SHJ-11-1-012", "SHJ-11-1-013",
                                                   "SHJ-11-1-014", "SHJ-11-1-015", "SHJ-11-1-016", "SHJ-11-1-017",
                                                   "SHJ-11-1-018", "SHJ-11-1-019", "SHJ-11-1-020", "SHJ-11-1-021",
                                                   "SHJ-11-1-022", "SHJ-16-1-037"]},
    "流沙 / Flowing Sands": {"re": "流沙"}, "赤水 / Red Water": {"re": "赤水"}, "黑水 / Black Water": {"re": "黑水|黒水"},
    "弱水 / Weak Water": {"re": "弱水"}, "西王母 / Queen Mother of the West": {"re": "西王母"},
    "湯谷・扶桑 / Sunrise Valley and Fusang": {"re": "湯谷|扶桑|暘谷"}, "蓬萊 / Penglai": {"re": "蓬萊"},
    "不周 / Buzhou": {"re": "不周"},
}


# Schematic continent outlines (lon, lat), for orientation only.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-95, 72), (-80, 63), (-60, 55), (-66, 44), (-75, 35), (-81, 25), (-97, 26), (-97, 18),
     (-87, 15), (-79, 9), (-90, 14), (-105, 20), (-117, 32), (-124, 40), (-125, 49), (-135, 58), (-150, 60), (-165, 60)],
    [(-80, 9), (-72, 12), (-60, 8), (-50, 0), (-35, -6), (-39, -15), (-48, -26), (-58, -35), (-65, -42), (-68, -55),
     (-74, -50), (-72, -35), (-71, -18), (-81, -5), (-78, 1)],
    [(-17, 21), (-6, 36), (10, 37), (20, 32), (32, 31), (35, 24), (43, 12), (51, 12), (40, -2), (40, -15), (35, -24),
     (20, -35), (15, -25), (12, -6), (9, 4), (-8, 5), (-17, 14)],
    [(-10, 36), (-9, 43), (-2, 48), (5, 52), (8, 57), (5, 62), (15, 69), (30, 71), (45, 68), (70, 73), (100, 77),
     (140, 72), (170, 69), (180, 66), (160, 60), (155, 52), (140, 46), (135, 35), (128, 35), (122, 40), (122, 30),
     (110, 20), (106, 10), (100, 13), (101, 3), (98, 9), (94, 16), (88, 22), (80, 15), (77, 8), (72, 20), (67, 25),
     (57, 25), (52, 17), (44, 13), (35, 30), (28, 37), (26, 40), (23, 36), (15, 40), (18, 45), (12, 44), (8, 44),
     (3, 43), (-5, 36)],
    [(114, -22), (122, -17), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37), (141, -38),
     (130, -32), (115, -34)],
    [(130, 31), (135, 34), (140, 36), (142, 40), (141, 45), (139, 40), (133, 35)],
    [(44, -25), (47, -25), (50, -15), (49, -12), (44, -16)],
    [(-50, 60), (-20, 70), (-25, 82), (-60, 82), (-70, 77)],
    [(-5, 50), (1, 51), (-2, 57), (-6, 58), (-5, 54)],
    [(95, 5), (105, -6), (115, -8), (120, -9), (117, 1), (110, 2), (104, 1)],
    [(131, -1), (141, -3), (150, -10), (142, -9), (135, -4)],
]


def load():
    entries = [json.loads(l) for l in ENTRIES.open()]
    regions = [json.loads(l) for l in (WORLD / "regions.jsonl").open() if l.strip()]
    props = {p["prop"]: p for p in (json.loads(l) for l in (WORLD / "region-properties.jsonl").open() if l.strip())}
    amap = [json.loads(l) for l in AMAP.open()]
    return entries, regions, props, amap


def units(entries):
    by = defaultdict(list)
    for e in entries:
        if e["section"] in SKIP_SECTIONS:
            continue
        by[(e["book_no"], e["section_no"], e["book"], e["section"], e["layer"])].append(e)
    out = [{"uid": f"{k[0]:02d}.{k[1]:02d}", "label": f"{k[2]}・{k[3]}" if k[2] != k[3] else k[2], "layer": k[4],
            "book": k[2], "entries": v} for k, v in sorted(by.items())]
    by_id = {e["id"]: e for e in entries}
    for name, spec in NAMED.items():
        es = [by_id[i] for i in spec["ids"]] if "ids" in spec else [e for e in entries if re.search(spec["re"], e["text"])]
        out.append({"uid": "N." + name.split(" /")[0], "label": name, "layer": "named place", "book": "", "entries": es})
    return out


def unit_features(u, props, amap_by_entry, land):
    ids = {e["id"] for e in u["entries"]}
    feats = []
    hits, where = Counter(), {}
    for e in u["entries"]:
        for tag, n in region_cue_hits(e["text"]).items():
            hits[tag] += n
            where.setdefault(tag, e["id"])
    barren = sum(1 for e in u["entries"] if RE_BARREN.search(e["text"]))
    if u["entries"] and barren / len(u["entries"]) >= 0.3:
        hits["barren"] = barren
        where["barren"] = f"{barren}/{len(u['entries'])} entries 無草木"
    for tag, n in sorted(hits.items()):
        p = props[tag]
        known = len(p["true"]) + len(p["false"])
        w = math.log10(known / len(p["true"])) + 0.05 if p["true"] else 0.05
        feats.append({"fid": tag, "type": "prop", "group": p["group"], "true": set(p["true"]), "false": set(p["false"]),
                      "w": w, "count": n, "evidence": where[tag]})
    for r in (r for eid in sorted(ids) for r in amap_by_entry.get(eid, [])):
        if not r["accepted"]:
            continue
        m = r["matches"][0]
        regs = {x for x in m["regions"] if x in land}
        if not regs:   # marine-only animal: supports coastal regions
            regs = set(props["sea_coast"]["true"])
        w = math.log10(len(land) / len(regs)) + 0.05
        feats.append({"fid": f"fauna:{r['name_display_only'] or r['cid']}→{m['animal']}", "type": "fauna",
                      "group": "fauna", "regions": regs, "w": w, "cov": m["coverage"], "evidence": r["entry_id"]})
    return feats


def score_region(code, feats):
    detail = []
    for f in feats:
        if f["type"] == "prop":
            known = len(f["true"]) + len(f["false"])
            p = len(f["true"]) / known if known else 0.5
            s = f["w"] if code in f["true"] else (-f["w"] if code in f["false"] else f["w"] * (2 * p - 1))
        else:
            s = f["w"] * f["cov"] * (1 if code in f["regions"] else -0.5)
        detail.append((f["fid"], round(s, 3)))
    return round(sum(s for _, s in detail), 2), detail


def rank(feats, codes):
    return sorted(((score_region(c, feats)[0], c) for c in codes), key=lambda x: (-x[0], x[1]))


def main():
    entries, regions, props, amap = load()
    codes = [r["code"] for r in regions]
    land = set(codes)
    cen = {r["code"]: (r["lat"], r["lon"]) for r in regions}
    rname = {r["code"]: r["name"] for r in regions}
    amap_by_entry = defaultdict(list)
    for r in amap:
        amap_by_entry[r["entry_id"]].append(r)

    results = []
    for u in units(entries):
        feats = unit_features(u, props, amap_by_entry, land)
        rk = rank(feats, codes)
        margin = rk[0][0] - rk[1][0] if len(rk) > 1 else 0
        n_pos = sum(1 for _, s in score_region(rk[0][1], feats)[1] if s > 0)
        grade = ("G-strong" if margin >= 1.0 and n_pos >= 5 else "G-moderate" if margin >= 0.3 and n_pos >= 3
                 else "G-weak" if feats else "no data")
        jk = Counter()
        for f in feats:
            rest = [g for g in feats if g is not f]
            if rest:
                jk[rank(rest, codes)[0][1]] += 1
        top_detail = sorted(score_region(rk[0][1], feats)[1], key=lambda d: -d[1])
        ev = {f["fid"]: f["evidence"] for f in feats}
        results.append({"uid": u["uid"], "label": u["label"], "layer": u["layer"], "n_entries": len(u["entries"]),
                        "n_features": len(feats),
                        "top": [{"region": c, "score": s} for s, c in rk[:5]],
                        "margin": round(margin, 2), "grade": grade,
                        "jackknife_leader_share": round(jk[rk[0][1]] / sum(jk.values()), 2) if jk else None,
                        "for_leader": [{"feature": fid, "score": s, "evidence": ev[fid]} for fid, s in top_detail if s > 0][:6],
                        "against_leader": [{"feature": fid, "score": s, "evidence": ev[fid]} for fid, s in top_detail if s < 0][:4]})

    with (OUT / "global-map.jsonl").open("w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- markdown ----------------------------------------------------------------------------------
    L = ["# 全書全球對照圖（方法 G）/ Whole-book global map (Method G)", "",
         "Generated by `tools/shj/region_match.py`. Every section of the 18 books and 9 key named places, scored "
         f"against {len(codes)} world regions by description only (names masked, distances unused). "
         "Unknown region values are scored at their base-rate expectation, so better-documented regions gain no "
         "advantage. "
         "Grades: G-strong (margin ≥ 1.0, ≥ 5 supporting features), G-moderate (margin ≥ 0.3, ≥ 3), G-weak otherwise. "
         "Jackknife = share of drop-one-feature runs that keep the same leader.", "",
         "| unit | layer | entries | features | 1st | 2nd | 3rd | margin | grade | jackknife |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        t = r["top"]
        L.append(f"| {r['label']} | {r['layer']} | {r['n_entries']} | {r['n_features']} | "
                 + " | ".join(f"{x['region']} {x['score']}" for x in t[:3])
                 + f" | {r['margin']} | {r['grade']} | {r['jackknife_leader_share']} |")
    lead = Counter(r["top"][0]["region"] for r in results if r["grade"] != "no data" and r["layer"] != "named place")
    L += ["", "## 各地區被選為第一的次數（不含具名地點）/ How often each region leads (sections only)", "",
          ", ".join(f"{rname[k]} ({k}) ×{v}" for k, v in lead.most_common()), ""]

    # direction coherence (reference only)
    L += ["## 方位自洽（只作參考）/ Direction coherence (reference only)", "",
          "Leading region of each section, grouped by Mountain classic, with the region's centroid. Under the book's "
          "own naming one would expect 南 to lie south of 北, and 西 west of 東. Distances and bearings carry no score.", "",
          "| classic | leading regions (lat, lon) |", "|---|---|"]
    for bk in ["南山經", "西山經", "北山經", "東山經", "中山經"]:
        rs = [r for r in results if r["label"].startswith(bk) and r["grade"] != "no data"]
        cnt = Counter(r["top"][0]["region"] for r in rs)
        L.append(f"| {bk} | " + ", ".join(f"{k} ×{v} ({cen[k][0]:.0f}, {cen[k][1]:.0f})" for k, v in cnt.most_common()) + " |")
    L += ["", "## 每個單位的假設候選與書內證據 / Assumption candidates and in-text evidence per unit", ""]
    for r in results:
        if r["grade"] == "no data":
            continue
        t = r["top"]
        L += [f"### {r['label']}", "",
              f"- **候選 / candidates**: " + "；".join(f"{rname[x['region']]} ({x['region']}) {x['score']}" for x in t[:3])
              + f" — {r['grade']}, margin {r['margin']}, jackknife {r['jackknife_leader_share']}",
              "- **支持第一候選 / for the leader**: " + "; ".join(f"{d['feature']} (+{d['score']:.2f}, `{d['evidence']}`)"
                                                       for d in r["for_leader"]),
              "- **不利第一候選 / against the leader**: " + ("; ".join(f"{d['feature']} ({d['score']:.2f}, `{d['evidence']}`)"
                                                         for d in r["against_leader"]) or "—"), ""]
    (OUT / "global-map.md").write_text("\n".join(L) + "\n")

    # ---- peoples map ---------------------------------------------------------------------------------
    P = ["# 海經・大荒經人群習俗對照 / Peoples and customs (Sea & Wilderness books)", "",
         "Entries in books 6–18 whose descriptions carry custom cues; regions are those where every cued custom is "
         "attested (region-properties.jsonl). Names masked; descriptions only.", "",
         "| entry | text | customs | regions where all are attested |", "|---|---|---|---|"]
    for e in entries:
        if e["book_no"] < 6:
            continue
        cs = sorted(t for t in region_cue_hits(e["text"]) if t in CUSTOMS)
        if not cs:
            continue
        regs = set(codes)
        for c in cs:
            regs &= set(props[c]["true"])
        P.append(f"| `{e['id']}` | {mask_names(e['text'])[:36]}… | {', '.join(cs)} | {' '.join(sorted(regs)) or '(none)'} |")
    (OUT / "peoples-map.md").write_text("\n".join(P) + "\n")

    # ---- SVG map: schematic continents, region circles sized by sections led, side panel of units ---------
    W, H, MW = 1500, 720, 1000
    xy = lambda la, lo: ((lo + 180) / 360 * MW, 60 + (90 - la) / 180 * (MW / 2))  # noqa: E731
    colour = {"山經": "#b5542d", "海外經": "#2d6cb5", "海內經(四篇)": "#1f8f9c", "大荒經": "#7a4cb5", "海內經": "#3f8f5a",
              "named place": "#333333"}
    S = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="11">',
         f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
         '<text x="12" y="28" font-size="17" font-weight="bold" fill="#222">山海經全書全球對照（方法 G，初稿）'
         '/ Shanhaijing whole-book global map (Method G, draft)</text>',
         '<text x="12" y="48" fill="#555">Each section is assigned to its best-matching world region by description only '
         '(names masked, distances unused). Circle size = sections led. Continents are schematic.</text>']
    for poly in CONTINENTS:
        pts = " ".join(f"{xy(la, lo)[0]:.0f},{xy(la, lo)[1]:.0f}" for lo, la in poly)
        S.append(f'<polygon points="{pts}" fill="#e8e3d6" stroke="#cfc8b6"/>')
    for lo in range(-180, 181, 30):
        x, _ = xy(0, lo)
        S.append(f'<line x1="{x:.0f}" y1="60" x2="{x:.0f}" y2="{60 + MW / 2:.0f}" stroke="#000" opacity="0.06"/>')
    for la in range(-60, 91, 30):
        _, y = xy(la, 0)
        S.append(f'<line x1="0" y1="{y:.0f}" x2="{MW}" y2="{y:.0f}" stroke="#000" opacity="0.06"/>')
    led = defaultdict(list)
    for r in results:
        if r["grade"] != "no data":
            led[r["top"][0]["region"]].append(r)
    for code, (la, lo) in cen.items():
        x, y = xy(la, lo)
        n = len(led.get(code, []))
        S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{3 + 2.2 * n:.1f}" fill="#b5542d" opacity="{0.25 if n else 0.08}" '
                 f'stroke="#7a3a1f" stroke-opacity="{0.6 if n else 0.2}"/>'
                 f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" font-weight="bold" '
                 f'fill="{"#222" if n else "#999"}">{code}</text>')
    y0, x0 = 80, MW + 20
    S.append(f'<text x="{x0}" y="{y0 - 12}" font-weight="bold" fill="#222">Sections by leading region</text>')
    yy = y0
    for code, rs in sorted(led.items(), key=lambda kv: -len(kv[1])):
        S.append(f'<text x="{x0}" y="{yy}" font-weight="bold" fill="#222">{code} — {rname[code]} ({len(rs)})</text>')
        yy += 13
        for r in rs:
            op = {"G-strong": 1.0, "G-moderate": 0.85, "G-weak": 0.5}[r["grade"]]
            S.append(f'<text x="{x0 + 12}" y="{yy}" fill="{colour.get(r["layer"], "#000")}" opacity="{op}">'
                     f'{r["label"].split(" /")[0]}  ·  {r["grade"]}</text>')
            yy += 12
        yy += 4
    ly = 60 + MW / 2 + 30
    for i, (lab, c) in enumerate([("山經 Mountains", "#b5542d"), ("海外經", "#2d6cb5"), ("海內經(四篇)", "#1f8f9c"),
                                  ("大荒經", "#7a4cb5"), ("海內經", "#3f8f5a"), ("named place", "#333333")]):
        S.append(f'<rect x="{12 + i * 150}" y="{ly - 10}" width="10" height="10" fill="{c}"/>'
                 f'<text x="{27 + i * 150}" y="{ly}" fill="#333">{lab}</text>')
    S.append(f'<text x="12" y="{ly + 22}" fill="#555">Text opacity: G-strong solid, G-moderate medium, G-weak faint. '
             'Source: projects/shanhaijing/data/derived/global-map.md</text></svg>')
    H2 = max(H, int(yy) + 20)
    S[0] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H2}" font-family="sans-serif" font-size="11">'
    S[1] = f'<rect width="{W}" height="{H2}" fill="#fbfaf6"/>'
    (OUT / "global-map.svg").write_text("\n".join(S))
    print(f"{len(results)} units; leaders: {lead.most_common(8)}", file=sys.stderr)


if __name__ == "__main__":
    main()
