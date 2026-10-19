"""Step 5 of the entity-graph method: the deliverable — an item-by-item mapping of the whole book.

Writes projects/shanhaijing/deliverables/<version>/ (default DRAFT below; `--version draft-vN` to override):
  book/NN-書名.md         every paragraph (all 869), its text, and every entity in it with its real-world mapping,
                          confidence and basis — or the reason it is not mapped
  entities.md             catalogue of all entities by type
  mapping-*.md            tables by type (waters, mountains by section, creatures, peoples, plants and minerals)
  world-map.svg           mapped mountains (by region), waters (source → mouth) and peoples on a schematic world
  coverage.md             completeness check: every paragraph and every mention present (must pass)
  summary.json            counts used by README.md
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kg_common import KG, ROOT, jl, load_world  # noqa: E402

DRAFT = "draft-v3"
OUT = ROOT / "projects/shanhaijing/deliverables" / (sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else DRAFT)
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
TYPE_ZH = {"MTN": "山", "WAT": "水", "LND": "地", "POL": "國族", "CRE": "生物", "PLA": "植物", "MIN": "礦物",
           "PER": "神人", "UNK": "未定", "DOC": "結構"}
STATUS_ZH = {
    "unmapped:none": "無合適真實對應 / no fitting real-world counterpart",
    "unmapped:insufficient": "證據不足 / insufficient evidence",
    "unmapped:non-geographic": "非地理實體（神、人）/ non-geographic (deity, person)",
    "unmapped:undetermined": "類型未定 / type undetermined",
    "unmapped:structural": "結構性文字（總述、題記）/ structural text",
    "unmapped:no-candidate": "庫中無候選 / no candidate in the base",
    "unmapped:generic": "泛稱（海）/ generic term (sea)",
    "via-relations": "小溪：經由關係對應 / minor stream: mapped through its relations",
}


def main():
    regions, props, animals, waters, cultures = load_world()
    rname = {r["code"]: r["name"] for r in regions}
    wname = {w["id"]: w["name"] for w in waters}
    aname = {a["id"]: f"{a['en']}（{a['zh_display']}）" for a in animals}
    cname = {c["id"]: c["name"] for c in cultures}
    nodes = {n["id"]: n for n in jl(KG / "nodes.jsonl")}
    edges = jl(KG / "edges.jsonl")
    mapping = {m["node"]: m for m in jl(KG / "mapping.jsonl")}
    mentions = jl(KG / "mentions.jsonl")
    rob_path = KG / "sensitivity/robustness.jsonl"
    robust = {r["node"]: r for r in jl(rob_path)} if rob_path.exists() else {}
    entries = jl(ENTRIES)
    by_entry = {m["entry"]: m["nodes"] for m in mentions}

    def label(cand):
        if not cand:
            return ""
        kind, _, key = cand.partition(":")
        return {"region": rname, "water": wname, "animal": aname, "culture": cname}.get(kind, {}).get(key, cand)

    out_e = defaultdict(list)
    for x in edges:
        out_e[x["src"]].append(x)

    edge_dir = {}
    for x in edges:
        edge_dir.setdefault((x["src"], x["dst"]), x["type"])
    REL_ZH = {"flows_into": "注入", "rises_at": "發源", "next": "相鄰", "has_creature": "產", "located": "位於",
              "sees": "望見", "sinks_at": "潛入", "has_resource": "產", "dwells": "居", "begets": "生"}

    def disp(nid):
        """Readable symbol: waters get 水 back unless the name already says what it is."""
        if not nid or nid not in nodes:
            return "海" if nid is None else str(nid)
        n = nodes[nid]
        sym = n["symbol"]
        if sym.startswith("SHJ-"):                         # an unnamed creature or plant: 「有獸焉」 without a name
            return f"無名{TYPE_ZH[n['type']]}（{sym.split('#')[0]}）"
        if n["type"] == "WAT" and not re.search(r"(海|澤|淵|泉|池|湖|浦|谷)$", sym) and sym not in ("河", "江"):
            sym += "水"
        return sym

    def rel(nid, s):
        """Relation as read from the entity: 「→X」 when the entity is the subject, 「←X」 when it is the object."""
        w, r = s.get("with"), s["relation"].split("(")[0]
        arrow = "←" if (w, nid) in edge_dir and (nid, w) not in edge_dir else "→"
        return f"{REL_ZH.get(r, r)}{arrow}{disp(w)}"

    def describe(nid):
        """(mapping text, confidence text, basis text) for one entity."""
        n, m = nodes[nid], mapping.get(nid, {})
        st = m.get("status", "")
        if st == "mapped":
            conf = f"{m['confidence']:.2f}（{m['tier']}）"
            r = robust.get(nid)
            if r and r["cand"] == m["cand"]:
                conf += f"；權重變體 {r['kept']}/{r['of']}"
            alts = "；".join(f"{label(a['cand'])} {a['share']:.0%}" for a in m.get("sample_alternatives", [])[:2])
            sup = "；".join(dict.fromkeys(rel(nid, s) for s in m.get("supported_by", [])[:4]))
            basis = "；".join(x for x in (f"支持 {sup}" if sup else "", f"其他 {alts}" if alts else "") if x)
            return label(m["cand"]), conf, basis or "自身描述 / own description"
        if st == "mapped:lexical":
            return f"{m.get('gloss')}（詞義 / lexical）", "—", "普通名詞的詞義 / meaning of a common noun"
        if st == "via-relations":
            parts = []
            for x in out_e.get(nid, []):
                if x["type"] == "rises_at":
                    tm = mapping.get(x["dst"], {})
                    parts.append(f"源於 {disp(x['dst'])}"
                                 + (f"（{label(tm['cand'])}）" if tm.get("status") == "mapped" else ""))
                elif x["type"] == "flows_into":
                    tm = mapping.get(x["dst"], {})
                    parts.append(f"注入 {disp(x['dst'])}"
                                 + (f"（{label(tm['cand'])}）" if tm.get("status") == "mapped" else ""))
            return "—", "—", "；".join(parts) or STATUS_ZH[st]
        return "—", "—", STATUS_ZH.get(st, st)

    # ---- per-book paragraph files --------------------------------------------------------------------------------
    (OUT / "book").mkdir(parents=True, exist_ok=True)
    rows_written, paras_written = 0, 0
    by_book = defaultdict(list)
    for e in entries:
        by_book[(e["book_no"], e["book"])].append(e)
    for (bno, bname), es in sorted(by_book.items()):
        L = [f"# 卷{bno:02d}・{bname} — 逐段對照 / Paragraph-by-paragraph mapping", "",
             "每一段：原文、其中每個實體、真實世界對應、可信度（0–1；高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、暫定 < 0.1）、依據。名稱只是符號；對應只依描述與關係。",
             "Every paragraph: text, every entity in it, its real-world mapping, confidence and basis. Names are symbols.",
             "「權重變體 k/n」：在 n 個權重變體中，有 k 個保持同一對應（見 kg/sensitivity）。/ kept in k of n weight variants.",
             ""]
        cur = None
        for e in es:
            if e["section"] != cur:
                cur = e["section"]
                L += [f"## {cur}", ""]
            L += [f"### `{e['id']}`", "", f"> {e['text']}", "",
                  "| 實體 / entity | 類型 | 真實世界對應 / real-world mapping | 可信度 / confidence | 依據 / basis |",
                  "|---|---|---|---|---|"]
            for nid in by_entry.get(e["id"], []):
                if nid not in nodes:
                    continue
                n = nodes[nid]
                mp, cf, bs = describe(nid)
                L.append(f"| {disp(nid)} | {TYPE_ZH[n['type']]} | {mp} | {cf} | {bs} |")
                rows_written += 1
            L.append("")
            paras_written += 1
        (OUT / "book" / f"{bno:02d}-{bname}.md").write_text("\n".join(L) + "\n")

    # ---- entity catalogue and type tables ---------------------------------------------------------------------------
    def table(nids, title, cols_extra=None):
        L = [f"# {title}", "", "| 實體 / entity | 類型 | 出現段數 | 真實世界對應 | 可信度 | 依據 |", "|---|---|---|---|---|---|"]
        for nid in nids:
            n = nodes[nid]
            mp, cf, bs = describe(nid)
            L.append(f"| {disp(nid)} | {TYPE_ZH[n['type']]} | {len(n['mentions'])} | {mp} | {cf} | {bs} |")
        return L

    order = sorted(nodes, key=lambda i: (list(TYPE_ZH).index(nodes[i]["type"]), -len(nodes[i]["mentions"]), i))
    (OUT / "entities.md").write_text("\n".join(table(order, "全部實體 / All entities")) + "\n")

    def conf_key(i):
        return -(mapping.get(i, {}).get("confidence") or 0)

    wat = sorted([i for i in nodes if nodes[i]["type"] == "WAT"], key=lambda i: (conf_key(i), i))
    (OUT / "mapping-waters.md").write_text("\n".join(table(wat, "水的對應 / Waters")) + "\n")
    cre = sorted([i for i in nodes if nodes[i]["type"] == "CRE"], key=lambda i: (conf_key(i), i))
    (OUT / "mapping-creatures.md").write_text("\n".join(table(cre, "生物的對應 / Creatures")) + "\n")
    pol = sorted([i for i in nodes if nodes[i]["type"] == "POL"], key=lambda i: (conf_key(i), i))
    (OUT / "mapping-peoples.md").write_text("\n".join(table(pol, "國族的對應 / Peoples")) + "\n")
    pm = sorted([i for i in nodes if nodes[i]["type"] in ("PLA", "MIN")], key=lambda i: (nodes[i]["type"], i))
    (OUT / "mapping-plants-minerals.md").write_text("\n".join(table(pm, "植物與礦物 / Plants and minerals")) + "\n")
    # mountains by section with a section-level summary
    L = ["# 山的對應（依篇）/ Mountains by section", "",
         "每篇先列各地區的山數（只計已對應者），再列每一座山。/ Region counts per section, then every mountain.", ""]
    sec = defaultdict(list)
    for i, n in nodes.items():
        if n["type"] == "MTN":
            sec[n["props"].get("section", "（海經、大荒經或其他）")].append(i)
    for s_name in sorted(sec, key=lambda k: min(nodes[i]["mentions"][0] for i in sec[k])):
        ids = sorted(sec[s_name], key=lambda i: (nodes[i]["props"].get("seq", 999), i))
        cnt = Counter(label(mapping[i]["cand"]) for i in ids if mapping.get(i, {}).get("status") == "mapped")
        L += [f"## {s_name}", "", "地區分佈 / regions: " + ("；".join(f"{k} ×{v}" for k, v in cnt.most_common()) or "—"), ""]
        L += table(ids, s_name)[2:] + [""]
    (OUT / "mapping-mountains.md").write_text("\n".join(L) + "\n")

    # ---- world map ------------------------------------------------------------------------------------------------
    # equirectangular, 85°N–60°S; coastlines are display-only outlines (data/world/coastlines.json), never scored
    coast = json.loads((ROOT / "projects/shanhaijing/data/world/coastlines.json").read_text())
    W, LAT0, LAT1, TOP = 1400, 85, -60, 64
    K = W / 360
    H = TOP + (LAT0 - LAT1) * K + 96
    xy = lambda la, lo: ((lo + 180) * K, TOP + (LAT0 - max(min(la, LAT0), LAT1)) * K)  # noqa: E731

    def poly(pts):
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (xy(la, lo) for la, lo in pts)) + " Z"

    cite = lambda m: m.get("status") == "mapped" and m.get("tier") != "tentative"  # noqa: E731
    ver = OUT.name
    S = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" font-family="sans-serif" font-size="11">',
         f'<rect width="{W}" height="{H:.0f}" fill="#fbfaf6"/>',
         f'<rect x="0" y="{TOP}" width="{W}" height="{(LAT0 - LAT1) * K:.1f}" fill="#dce8f1"/>',
         f'<text x="12" y="24" font-size="17" font-weight="bold" fill="#222">山海經實體圖譜的全球對應（{ver}）'
         f'/ Shanhaijing entity graph mapped to the world ({ver})</text>',
         '<text x="12" y="44" fill="#555">實心 = 可信度 ≥ 0.1；虛線或淡色 = 暫定（不宜引用）。河線為示意：源頭到河口的直線。'
         '/ Solid = confidence ≥ 0.1; dashed or faint = tentative (do not cite). River lines are schematic, source to mouth.</text>']
    S.append('<g fill="#f3efe4" stroke="#a89f88" stroke-width="0.7">'
             + "".join(f'<path d="{poly(v)}"/>' for v in coast["land"].values()) + "</g>")
    S.append('<g fill="#dce8f1" stroke="#a89f88" stroke-width="0.5">'
             + "".join(f'<path d="{poly(v)}"/>' for v in coast["water"].values()) + "</g>")
    for lo in range(-180, 181, 30):
        x, _ = xy(0, lo)
        S.append(f'<line x1="{x:.0f}" y1="{TOP}" x2="{x:.0f}" y2="{TOP + (LAT0 - LAT1) * K:.0f}" stroke="#000" opacity="0.07"/>')
    for la in range(-60, 85, 30):
        _, y = xy(la, 0)
        S.append(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="#000" opacity="0.07"/>'
                 f'<text x="3" y="{y - 2:.0f}" font-size="9" fill="#888">{abs(la)}°{"N" if la > 0 else "S" if la < 0 else ""}</text>')
    wat_by = {w["id"]: w for w in waters}
    for i in wat:
        m = mapping.get(i, {})
        if m.get("status") != "mapped" or not m["cand"].startswith("water:"):
            continue
        w = wat_by[m["cand"][6:]]
        if w["type"] == "river":
            (x1, y1), (x2, y2) = xy(*w["src"]), xy(*w["mouth_pt"])
            style = 'stroke-width="2.2" opacity="0.9"' if cite(m) else 'stroke-width="1" opacity="0.35" stroke-dasharray="3,3"'
            S.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#2d6cb5" {style}>'
                     f'<title>{disp(i)} → {label(m["cand"])} ({m["confidence"]:.2f}, {m["tier"]})</title></line>')
            if cite(m):
                S.append(f'<text x="{x2 + 3:.0f}" y="{y2 - 3:.0f}" font-size="10" fill="#1d4f8a">{disp(i)}</text>')
    places = [i for i in nodes if nodes[i]["type"] in ("MTN", "LND") and mapping.get(i, {}).get("status") == "mapped"]
    reg_cite = Counter(mapping[i]["cand"][7:] for i in places if cite(mapping[i]))
    reg_all = Counter(mapping[i]["cand"][7:] for i in places)
    for r in regions:
        x, y = xy(r["lat"], r["lon"])
        n, t = reg_cite.get(r["code"], 0), reg_all.get(r["code"], 0)
        S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{3 + 1.6 * t ** 0.5:.1f}" fill="none" stroke="#b5542d" '
                 f'stroke-dasharray="2,2" opacity="0.6"/>')
        if n:
            S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{3 + 1.6 * n ** 0.5:.1f}" fill="#b5542d" opacity="0.55"/>')
        S.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" font-size="10" fill="#222">'
                 f'<title>{r["name"]}: {n} mapped at ≥ 0.1, {t} including tentative</title>{r["code"]} {n}/{t}</text>')
    cul = {c["id"]: c for c in cultures}
    pc_cite = Counter(mapping[i]["cand"][8:] for i in pol if cite(mapping.get(i, {})))
    pc_all = Counter(mapping[i]["cand"][8:] for i in pol if mapping.get(i, {}).get("status") == "mapped")
    for k, v in sorted(pc_all.items()):
        x, y = xy(*cul[k]["pt"])
        c = pc_cite.get(k, 0)
        S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{2 + 1.5 * v}" fill="#7a4cb5" opacity="{0.8 if c else 0.25}">'
                 f'<title>{cul[k]["name"]}: {c} at ≥ 0.1, {v} including tentative</title></circle>')
        if c:
            names = "、".join(disp(i) for i in pol if mapping.get(i, {}).get("cand") == "culture:" + k and cite(mapping[i]))
            S.append(f'<text x="{x + 6:.0f}" y="{y + 4:.0f}" font-size="10" fill="#5a2f8f">{names}</text>')
    ly = TOP + (LAT0 - LAT1) * K + 22
    S += [f'<circle cx="20" cy="{ly}" r="7" fill="#b5542d" opacity="0.55"/>',
          f'<text x="34" y="{ly + 4}">地區：山與地的數目「≥ 0.1 / 全部」/ region: mountains and places mapped, "≥ 0.1 / all"</text>',
          f'<line x1="12" y1="{ly + 24}" x2="30" y2="{ly + 24}" stroke="#2d6cb5" stroke-width="2.2"/>',
          f'<text x="34" y="{ly + 28}">水：書中之水對到的真實河流（源 → 口）/ water: book water mapped to a real river (source → mouth)</text>',
          f'<circle cx="20" cy="{ly + 48}" r="5" fill="#7a4cb5" opacity="0.8"/>',
          f'<text x="34" y="{ly + 52}">國族：對到的古代人群 / peoples: matched ancient cultures. 海岸線僅供定位，不參與計分 / coastlines for orientation only, not scored.</text>']
    S.append("</svg>")
    (OUT / "world-map.svg").write_text("\n".join(S))

    # ---- section and hypothesis tests (kg_sections.py), copied when present ------------------------------------------
    sec_md = KG / "sections/sections.md"
    if sec_md.exists():
        (OUT / "hypotheses.md").write_text(sec_md.read_text())

    # ---- coverage of the deliverable --------------------------------------------------------------------------------
    total_mentions = sum(len([n for n in v if n in nodes]) for v in by_entry.values())
    missing_paras = [e["id"] for e in entries if e["id"] not in by_entry or not by_entry[e["id"]]]
    status = Counter(mapping.get(i, {}).get("status", "?") for i in nodes)
    tiers = Counter(mapping[i].get("tier") for i in nodes if mapping.get(i, {}).get("status") == "mapped")
    ok = paras_written == len(entries) and rows_written == total_mentions and not missing_paras
    C = ["# 交付完整性檢查 / Deliverable completeness check", "",
         f"- 原文段落 / paragraphs in the text: **{len(entries)}**；寫入逐段對照 / written: **{paras_written}**",
         f"- 段內實體提及 / entity mentions: **{total_mentions}**；寫入的列 / rows written: **{rows_written}**",
         f"- 沒有實體的段落 / paragraphs without entities: **{len(missing_paras)}**",
         f"- 結果 / result: **{'PASS' if ok else 'FAIL'}**", "",
         "知識圖譜層的覆蓋檢查見 `data/derived/kg/coverage.md`。/ KG-level audit in data/derived/kg/coverage.md.", "",
         "| 狀態 / status | 實體數 / entities |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(status.items())] + \
        ["", "| 可信度級別 / tier (mapped) | 實體數 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(tiers.items())]
    (OUT / "coverage.md").write_text("\n".join(C) + "\n")
    summary = {"paragraphs": len(entries), "entities": len(nodes), "edges": len(edges), "mentions": total_mentions,
               "types": Counter(n["type"] for n in nodes.values()), "status": status, "tiers": tiers,
               "regions_of_mountains": reg_cite.most_common(12), "regions_of_mountains_all": reg_all.most_common(12),
               "peoples": pc_cite.most_common(), "peoples_all": pc_all.most_common(), "complete": ok}
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"paragraphs {paras_written}/{len(entries)}; rows {rows_written}/{total_mentions}; complete={ok}",
          file=sys.stderr)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
