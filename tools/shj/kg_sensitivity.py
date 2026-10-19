"""Weight sensitivity of the cross-validation (task T-X04).

Re-solves the whole book with one relation weight changed at a time (kg_crossval.py --set …), runs the variants in
parallel, and compares each variant's mapping with the baseline kg/mapping.jsonl: the share of mapped entities that keep
their candidate, by tier, and the key entities listed below.

  python3 -I tools/shj/kg_sensitivity.py [--jobs N]

Runs go to kg/sensitivity/runs/ (not committed); the report is kg/sensitivity/sensitivity.md.
"""
import json
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kg_common import KG, ROOT, jl  # noqa: E402

OUT = KG / "sensitivity"
RUNS = OUT / "runs"
# one change at a time: roughly halve and raise each weight family
VARIANTS = {
    "uniq×0.5": ["uniq=1.0"], "uniq×1.5": ["uniq=3.0"],
    "flow_hit×0.75": ["flow_hit=1.5"], "flow_hit×1.5": ["flow_hit=3.0"],
    "flow_miss×0.5": ["flow_miss=-0.5"], "flow_miss×1.5": ["flow_miss=-1.5"],
    "rise×0.5": ["rise_hit=0.5", "rise_adj=0.15", "rise_miss=-0.25"],
    "rise×1.5": ["rise_hit=1.5", "rise_adj=0.45", "rise_miss=-0.75"],
    "next×0.5": ["next_same=0.15", "next_adj=0.05", "next_miss=-0.15"],
    "next×2": ["next_same=0.6", "next_adj=0.2", "next_miss=-0.6"],
    "minor×0.5": ["minor_hit=0.3", "minor_miss=-0.15"], "minor×2": ["minor_hit=1.2", "minor_miss=-0.6"],
    "bearing×0": ["bearing_scale=0"], "bearing×2": ["bearing_scale=2"],
    "creature×0": ["creature_scale=0"], "creature×2": ["creature_scale=2"],
}
KEY = ["WAT:河", "WAT:江", "WAT:渭", "WAT:涇", "WAT:汾", "WAT:洛→河", "WAT:漢", "WAT:赤", "WAT:黑", "WAT:弱", "WAT:渤海",
       "WAT:泑澤", "MTN:昆侖之丘", "CRE:羬羊", "CRE:文鰩魚", "POL:毛民", "POL:玄股", "POL:黑齒"]


def run(name, sets):
    d = RUNS / name
    if (d / "mapping.jsonl").exists():
        return name, 0
    args = [sys.executable, "-I", str(ROOT / "tools/shj/kg_crossval.py"), "--out", str(d)]
    for s in sets:
        args += ["--set", s]
    r = subprocess.run(args, capture_output=True, text=True)
    (RUNS / f"{name}.log").write_text(r.stderr)
    return name, r.returncode


def main():
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    RUNS.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(jobs) as ex:
        for name, rc in ex.map(lambda kv: run(*kv), VARIANTS.items()):
            print(f"{name}: {'ok' if rc == 0 else 'FAILED'}", file=sys.stderr)
    base = {m["node"]: m for m in jl(KG / "mapping.jsonl")}
    mapped = {k: m for k, m in base.items() if m["status"] == "mapped"}
    tier_n = Counter(m["tier"] for m in mapped.values())
    rows, key_rows = [], defaultdict(dict)
    for name in VARIANTS:
        var = {m["node"]: m for m in jl(RUNS / name / "mapping.jsonl")}
        same = Counter(m["tier"] for k, m in mapped.items() if var.get(k, {}).get("cand") == m["cand"])
        sys_same = sum(1 for k, m in mapped.items() if m["type"] == "WAT" and var.get(k, {}).get("system") == m.get("system"))
        n_wat = sum(1 for m in mapped.values() if m["type"] == "WAT")
        rows.append((name, VARIANTS[name], same, sys_same, n_wat))
        for k in KEY:
            key_rows[k][name] = var.get(k, {}).get("cand")
    order = ["high", "medium", "low", "tentative"]
    L = ["# 權重敏感度 / Weight sensitivity", "",
         "每次只改一組權重，重解全書，與基準對應比較：各級別中候選不變的比例；河流另計水系不變的比例。",
         "One weight family changed at a time; the whole book re-solved and compared with the baseline: share of mapped "
         "entities keeping their candidate, by tier, and share of waters keeping their river system.", "",
         "| 變體 / variant | 設定 / setting | " + " | ".join(f"{t} (n={tier_n[t]})" for t in order) + " | 水系 / water system |",
         "|---|---|" + "---|" * (len(order) + 1)]
    for name, sets, same, sys_same, n_wat in rows:
        cells = [f"{same[t] / tier_n[t]:.0%}" if tier_n[t] else "—" for t in order]
        L.append(f"| {name} | `{' '.join(sets)}` | " + " | ".join(cells) + f" | {sys_same / max(n_wat, 1):.0%} |")
    hi = [same["high"] + same["medium"] for _, _, same, _, _ in rows]
    L += ["", f"高與中級別的對應在各變體中保持不變的最低比例 / lowest share of high+medium mappings unchanged: "
          f"**{min(hi) / max(tier_n['high'] + tier_n['medium'], 1):.0%}**", "",
          "## 重點實體 / Key entities", "",
          "| 實體 | 基準 / baseline | " + " | ".join(VARIANTS) + " | 不變 / unchanged |",
          "|---|---|" + "---|" * (len(VARIANTS) + 1)]
    for k in KEY:
        if k not in base:
            continue
        b = base[k].get("cand")
        vals = [key_rows[k].get(n) for n in VARIANTS]
        short = lambda c: (c or "—").split(":")[-1]  # noqa: E731
        L.append(f"| {k} | {short(b)} ({base[k].get('confidence')}) | "
                 + " | ".join("=" if v == b else short(v) for v in vals)
                 + f" | {sum(v == b for v in vals)}/{len(vals)} |")
    (OUT / "sensitivity.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:len(rows) + 8]), file=sys.stderr)


if __name__ == "__main__":
    main()
