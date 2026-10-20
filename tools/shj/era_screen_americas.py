"""Screen the whole book for descriptions that point to the Americas (task T-V04f).

1. Creatures: for every creature with at least two description tags, rarity-weighted coverage by every animal of the
   era fauna seed; report the creatures for which an animal found only in the Americas fits at least as well as the
   best Old World animal (within 0.05).
2. Passages: every paragraph that places something beyond the eastern or north-eastern sea, at the sunrise, or at the
   north-east corner (the far side of the book's world from the Central Plains).

Output: projects/shanhaijing/data/derived/era/americas-screen.md
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AMERICAS = {"NAM", "MAM", "SAM", "ARC"}
PASSAGE = re.compile(r"東海之外|東北海外|東北海之外|東極|日月所出|日月所生|湯谷|扶桑|扶木|大壑|入海七千里|東北隅|東荒")


def jl(p):
    return [json.loads(l) for l in Path(p).open() if l.strip()]


def american_only(a):
    land = {r for r in a["regions"] if not r.startswith("S_")}
    return bool(land) and land <= AMERICAS


def main():
    fauna = jl(ROOT / "projects/shanhaijing/data/era/fauna-era.jsonl")
    nodes = jl(ROOT / "projects/shanhaijing/data/derived/kg/nodes.jsonl")
    entries = jl(ROOT / "reference/shanhaijing/data/entries.jsonl")
    df = Counter(t for a in fauna for t in set(a["tags"]))
    n = len(fauna)
    w = {t: math.log10(n / c) + 0.05 for t, c in df.items()}
    for g in ("vocal", "aquatic"):
        w[g] = min(w.get(g, 0.05), 0.05)
    rows, n_cre, n_am_better = [], 0, 0
    for nd in sorted(nodes, key=lambda x: x["id"]):
        if nd["type"] != "CRE" or len(nd["tags"]) < 2:
            continue
        n_cre += 1
        C = set(nd["tags"])
        den = sum(w.get(t, math.log10(n) + 0.05) for t in C)
        sc = []
        for a in fauna:
            ov = C & set(a["tags"])
            cov = sum(w.get(t, 0) for t in ov) / den * (0.5 if len(ov) < 2 else 1)
            sc.append((round(cov, 3), a["id"], american_only(a), sorted(ov)))
        sc.sort(key=lambda s: (-s[0], s[1]))
        am = next((s for s in sc if s[2]), None)
        ow = next((s for s in sc if not s[2]), None)
        if am and am[0] >= 0.3 and am[0] >= ow[0] - 0.05:
            rows.append((nd["symbol"], nd["mentions"][0], am, ow))
            if am[0] > ow[0]:
                n_am_better += 1
    L = ["# 美洲描述的篩查 / Screening the book for the Americas", "",
         f"生物：{n_cre} 個有兩個以上描述標籤的生物中，美洲特有動物吻合度不低於最佳舊大陸動物（差距 ≤ 0.05）的有 {len(rows)} 個；"
         f"**美洲特有動物明確勝出的有 {n_am_better} 個**。/ Creatures where an American-only animal fits as well as the best "
         f"Old World one: {len(rows)}; where it fits better: {n_am_better}.", "",
         "| 生物 | 條目 | 最佳美洲特有動物 | 最佳舊大陸動物 |", "|---|---|---|---|"]
    for sym, e, am, ow in rows:
        L.append(f"| {sym} | `{e}` | {am[1]}（{am[0]}；{'、'.join(am[3])}）| {ow[1]}（{ow[0]}；{'、'.join(ow[3])}）|")
    L += ["", "## 指向東方與東北遠方的段落 / Passages pointing far east or north-east", "",
          "| 條目 | 卷 | 原文 |", "|---|---|---|"]
    for e in entries:
        if PASSAGE.search(e["text"]):
            L.append(f"| `{e['id']}` | {e['book']} | {e['text'][:90]} |")
    (ROOT / "projects/shanhaijing/data/derived/era/americas-screen.md").write_text("\n".join(L) + "\n")
    print(f"{n_cre} creatures screened; {len(rows)} ties; {n_am_better} American-better")


if __name__ == "__main__":
    main()
