"""Description-first place matching against all candidate loci (Method G, stage G3).

For a target place, collect every passage describing it (names masked), derive features, and score every locus in
projects/shanhaijing/data/world/loci.jsonl under one rule set (method-g-global.md §3):

  property feature  T: +w   F: −w   unknown: 0          w = log10(N_known / N_true) + 0.05
  fauna feature     animal range covers the locus: +w·cov ; does not: −0.5·w·cov
                    (w from how many loci the matched animals reach; cov from tools/shj/animal_map.py)
  alternatives      one passage with two readings (e.g. monument vs animal) scores its better reading, once
  distance          not used here (reference only)

Scope: only passages where the place is the SUBJECT are scored (--entries, plus single clauses via --clause
"ENTRY:text"). Passages that merely mention the name (--target) are listed for audit but never scored, so a
neighbouring mountain's own minerals or rivers cannot leak into the target.

Usage:
  python3 -I tools/shj/geo_match.py --target "崑崙|昆侖|崐崘" \
      --entries SHJ-02-3-008,SHJ-06-1-017,SHJ-11-1-012,...,SHJ-16-1-037 \
      --clause "SHJ-02-3-007:南望昆侖，其光熊熊，其氣魂魂" --md projects/shanhaijing/hypotheses/H-0006/geo-match.md
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from animal_map import load_animals, match  # noqa: E402
from cues import RE_RIVER_OUT, creature_tags, mask_names, place_tags  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
CREATURES = ROOT / "projects/shanhaijing/data/derived/creatures.jsonl"
LOCI = ROOT / "projects/shanhaijing/data/world/loci.jsonl"

# Passages whose description can be read two ways: (regex, property reading, fauna tags for the animal reading)
ALTERNATIVES = [
    (r"人面[^。]{0,3}虎身[^。]{0,8}有文有尾[^。]{0,3}皆白", "human_feline_colossus",
     ["body_bigcat", "striped", "long_tail", "body_white"]),
    (r"身大類虎[^。]{0,6}人面", "human_feline_colossus", ["body_bigcat"]),
    (r"虎身而九尾，人面而虎爪", "human_feline_colossus", ["body_bigcat", "tails_many"]),
]
# Creatures named without a description in the target passage, described elsewhere in the book (cited)
DESCRIBED_ELSEWHERE = [
    (r"鳳皇|鸞鳥", ["body_fowl", "five_colours"], "SHJ-01-3-003 鳳皇「其狀如雞，五采而文」"),
]
GLOW = ("snow_cap", "fire_ground")
BUILT = ("guardian:", "east_facing_colossus", "built_complex", "cave_dwelling", "sacred_mountain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="regex for the place name (lists mentions; never scored)")
    ap.add_argument("--entries", required=True, help="comma-separated entry IDs where the place is the subject")
    ap.add_argument("--clause", action="append", default=[], help='"ENTRY_ID:exact clause" describing the place')
    ap.add_argument("--group", choices=["all", "natural", "built"], default="all",
                    help="score all features, only natural ones (landform, water, fire, fauna), or only built/cultic ones")
    ap.add_argument("--pairs", action="store_true",
                    help="also score composites: two loci on the same river system, each feature taking the better")
    ap.add_argument("--md")
    a = ap.parse_args()

    entries = [json.loads(l) for l in ENTRIES.open()]
    rx = re.compile(a.target)
    subj = list(filter(None, a.entries.split(",")))
    by_id = {e["id"]: e for e in entries}
    target = [by_id[i] for i in subj]
    for c in a.clause:
        eid, txt = c.split(":", 1)
        if txt not in by_id[eid]["text"]:
            raise SystemExit(f"clause not found verbatim in {eid}: {txt}")
        target.append({**by_id[eid], "text": txt, "id": eid + "(clause)"})
    mentions = [e["id"] for e in entries if rx.search(e["text"]) and e["id"] not in subj]
    loci = [json.loads(l) for l in LOCI.open() if l.strip()]
    animals, w_tags = load_animals()
    by_animal = {x["id"]: x for x in animals}

    # ---- features from the text ------------------------------------------------------------------
    props, evidence = {}, {}
    for e in target:
        t = mask_names(e["text"])
        for tag in sorted(place_tags(t)):
            props.setdefault(tag, e["id"])
    rivers = set()
    for e in target:
        for m in RE_RIVER_OUT.finditer(e["text"]):
            rivers.add((m.group(1), m.group(2) or m.group(3) or "?"))
    dirs = {d for _, d in rivers if d != "?"}
    if rivers:
        props["river_source_major"] = "+".join(sorted({e['id'] for e in target if RE_RIVER_OUT.search(e['text'])}))
    if len(dirs) >= 3:
        props["rivers_multi_dir"] = f"{len(rivers)} rivers, directions {''.join(sorted(dirs))}"

    features = []   # each: {"id", "alts": [("prop", tag) | ("fauna", tags)], "evidence"}
    used_alt, guardian = set(), None
    for e in target:
        for pat, prop, ftags in ALTERNATIVES:
            m = re.search(pat, e["text"])
            if not m:
                continue
            used_alt.add(prop)
            if guardian is None:
                guardian = {"id": f"guardian:{prop}", "alts": [("prop", prop)], "evidence": ""}
                features.append(guardian)
            guardian["alts"].append(("fauna", ftags))
            guardian["evidence"] += f"`{e['id']}` 「{m.group(0)}」 "
    for tag, src in props.items():
        if tag in used_alt:
            continue
        alts = [("prop", g) for g in GLOW] if tag == "glow" else [("prop", tag)]
        features.append({"id": tag, "alts": alts, "evidence": f"`{src}`" if src.startswith("SHJ") else src})
    creatures = [json.loads(l) for l in CREATURES.open()]
    ids = {e["id"] for e in target}
    for c in creatures:
        if c["entry_id"] in ids:
            features.append({"id": f"fauna:{c['name_display_only'] or c['cid']}", "alts": [("fauna", c["tags"])],
                             "evidence": f"`{c['entry_id']}` 「{c['text'][:28]}…」", "kind": c["kind"]})
    for e in target:
        for pat, ftags, cite in DESCRIBED_ELSEWHERE:
            if re.search(pat, e["text"]) and not any(f["id"] == f"fauna:{pat}" for f in features):
                features.append({"id": f"fauna:{pat}", "alts": [("fauna", ftags)],
                                 "evidence": f"`{e['id']}`; description from {cite}"})

    if a.group != "all":
        is_built = lambda f: f["id"].startswith(BUILT)  # noqa: E731
        features = [f for f in features if is_built(f) == (a.group == "built")]

    # ---- weights ---------------------------------------------------------------------------------
    def prop_w(tag):
        known = [L["props"].get(tag) for L in loci if L["props"].get(tag) is not None]
        n_true = sum(1 for v in known if v)
        if not known or not n_true:
            return 0.05
        return math.log10(len(known) / n_true) + 0.05

    def fauna_info(tags, kind="unknown"):
        best = match(tags, kind, animals, w_tags, top=3)
        top = [b for b in best if b[0] >= 0.5 and b[0] >= best[0][0] - 0.05]
        if not top:
            return None
        regions = set().union(*(set(b[2]["regions"]) for b in top))
        reach = sum(1 for L in loci if regions & set(L["regions"]))
        w = math.log10(len(loci) / max(1, reach)) + 0.05
        return {"cov": top[0][0], "animals": [b[2]["id"] for b in top], "regions": regions, "w": w}

    for f in features:
        f["resolved"] = []
        for alt in f["alts"]:
            if alt[0] == "prop":
                f["resolved"].append({"type": "prop", "tag": alt[1], "w": prop_w(alt[1])})
            else:
                info = fauna_info(alt[1], f.get("kind", "unknown"))
                if info:
                    f["resolved"].append({"type": "fauna", **info})

    # ---- scoring ---------------------------------------------------------------------------------
    def feature_score(f, L):
        best = None
        for r in f["resolved"]:
            if r["type"] == "prop":
                v = L["props"].get(r["tag"])
                s_ = 0.0 if v is None else (r["w"] if v else -r["w"])
                lab = f"{r['tag']}={'?' if v is None else ('T' if v else 'F')}"
            else:
                hit = bool(r["regions"] & set(L["regions"]))
                s_ = r["w"] * r["cov"] * (1 if hit else -0.5)
                lab = f"{'/'.join(r['animals'])} {'present' if hit else 'absent'}"
            if best is None or s_ > best[0]:
                best = (s_, lab)
        return best

    def score(L, feats):
        detail = []
        for f in feats:
            b = feature_score(f, L)
            if b:
                detail.append((f["id"], round(b[0], 2), b[1]))
        return round(sum(d[1] for d in detail), 2), detail

    results = []
    for L in loci:
        total, detail = score(L, features)
        results.append({"id": L["id"], "name": L["name"], "score": total, "detail": detail,
                        "plus": sum(1 for d in detail if d[1] > 0), "minus": sum(1 for d in detail if d[1] < 0)})
    results.sort(key=lambda r: -r["score"])

    lines = [f"# Method G place match — target `{a.target}` — feature group: {a.group}", "",
             f"Scored passages (place is the subject): {len(target)} ({', '.join(e['id'] for e in target)}). "
             f"Loci: {len(loci)}. Names masked; distances not used.", "",
             f"Mentions listed for audit only, not scored ({len(mentions)}): {', '.join(mentions)}", "",
             "## 1. 書中特徵 / Features found in the text", "",
             "| feature | readings (alternatives score once) | weight(s) | evidence |", "|---|---|---|---|"]
    for f in features:
        rd = " or ".join(r["tag"] if r["type"] == "prop" else "animal: " + "/".join(r["animals"]) for r in f["resolved"])
        ws = ", ".join(f"{r['w']:.2f}" + (f"×{r['cov']}" if r["type"] == "fauna" else "") for r in f["resolved"])
        lines.append(f"| {f['id']} | {rd or '(no real-animal match ≥ 0.5)'} | {ws} | {f['evidence']} |")
    lines += ["", "## 2. 全部候選排名 / Ranking of all candidates", "",
              "| rank | locus | score | matches | contradictions |", "|---|---|---|---|---|"]
    for i, r in enumerate(results, 1):
        lines.append(f"| {i} | {r['id']} {r['name']} | **{r['score']}** | {r['plus']} | {r['minus']} |")
    lead = results[0]["score"] - results[1]["score"]
    grade = ("G-strong" if lead >= 1.0 and results[0]["plus"] >= 5 else "G-moderate" if lead >= 0.3 else "G-weak")
    lines += ["", f"Leader margin: **{lead:.2f}** → **{grade}** (method-g-global.md §3.4)", "",
              "### 留一檢驗 / Jackknife (drop one feature at a time)", "",
              "| dropped feature | leader | margin |", "|---|---|---|"]
    from collections import Counter as _C
    leaders = _C()
    for f in features:
        rest = [g for g in features if g is not f]
        rk = sorted(((score(L, rest)[0], L["id"]) for L in loci), reverse=True)
        leaders[rk[0][1]] += 1
        lines.append(f"| {f['id']} | {rk[0][1]} | {rk[0][0] - rk[1][0]:.2f} |")
    lines += ["", "Leader frequency over the jackknife: " + ", ".join(f"{k} ×{v}" for k, v in leaders.most_common()), ""]
    if a.pairs:
        comp = []
        for i, A in enumerate(loci):
            for B in loci[i + 1:]:
                shared = set(A.get("basins", [])) & set(B.get("basins", []))
                if not shared:
                    continue
                tot = 0.0
                for f in features:
                    sa, sb = feature_score(f, A), feature_score(f, B)
                    tot += max(x[0] for x in (sa, sb) if x)
                comp.append((round(tot, 2), A["id"], B["id"], "/".join(sorted(shared))))
        comp.sort(reverse=True)
        lines += ["### 同一水系的複合候選 / Composites on the same river system (post-hoc)", "",
                  "Each feature takes the better of the two loci. Only pairs sharing a river system are scored.", "",
                  "| composite score | loci | shared river system |", "|---|---|---|"]
        lines += [f"| **{t}** | {x} + {y} | {sh} |" for t, x, y, sh in comp[:10]]
        lines.append("")
    lines += ["",
              "## 3. 逐項明細 / Itemised scores (top 5 and any locus requested with --show)", ""]
    show = results[:5] + [r for r in results[5:] if r["id"] in ("L01",)]
    for r in show:
        lines += [f"### {r['id']} {r['name']} — {r['score']}", "", "| feature | score | reading |", "|---|---|---|"]
        lines += [f"| {fid} | {s:+.2f} | {lab} |" for fid, s, lab in r["detail"]]
        lines.append("")
    text = "\n".join(lines) + "\n"
    if a.md:
        Path(a.md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.md).write_text(text)
    print("\n".join(lines[lines.index("## 2. 全部候選排名 / Ranking of all candidates"):][:35]))


if __name__ == "__main__":
    main()
