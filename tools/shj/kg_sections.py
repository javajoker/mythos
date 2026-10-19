"""Section-level hypothesis tests (tasks T-X06, T-X08).

1. Scan: for every Mountain-Classic section and every world region, hold all of the section's mountains in that region,
   re-fit the rest of the book (ICM and block moves from the baseline mapping), and record the energy. The ranking of
   regions per section is a whole-book, section-level map; ΔE is the loss against the section's best region.
2. Configurations: named joint hypotheses (for example 西次一經 = Indus, 西次二經 = Mesopotamia, 西次三經 = Egypt with
   赤水 = Red Sea, 黑水 = Nile, 西海 = Mediterranean) and their rivals, scored the same way, with the relations each one
   breaks.

  python3 -I tools/shj/kg_sections.py [--jobs N]

Runs in kg/sections/runs/ (not committed); report kg/sections/sections.md and kg/sections/scan.jsonl.
"""
import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kg_common import KG, ROOT, WORLD, jl  # noqa: E402

OUT = KG / "sections"
RUNS = OUT / "runs"
WEST = ["西山經之首", "西次二經", "西次三經", "西次四經"]


def configurations(sec_nodes):
    """Named joint hypotheses. The user's reading and its rivals are built the same way: whole sections held in one
    region each, plus any named waters."""
    def sec(assign):
        fix = {}
        for s, r in assign.items():
            fix.update({n: f"region:{r}" for n in sec_nodes[s]})
        return fix
    user_waters = {"WAT:赤": "water:red_sea", "WAT:黑": "water:nile", "WAT:西海": "water:mediterranean",
                   "MTN:昆侖之丘": "region:EGY"}
    cfgs = [
        ("free (baseline, nothing held)", {}, []),
        ("user: 西首 IDS, 西二 MES, 西三 EGY + 赤水 Red Sea, 黑水 Nile, 西海 Mediterranean",
         {**sec({"西山經之首": "IDS", "西次二經": "MES", "西次三經": "EGY"}), **user_waters}, []),
        ("user, sections only: 西首 IDS, 西二 MES, 西三 EGY", sec({"西山經之首": "IDS", "西次二經": "MES", "西次三經": "EGY"}), []),
        ("user, 前 = south convention", {**sec({"西山經之首": "IDS", "西次二經": "MES", "西次三經": "EGY"}), **user_waters},
         ["front_east=0"]),
        ("user waters only: 赤水 Red Sea, 黑水 Nile, 西海 Mediterranean, 崑崙 EGY", dict(user_waters), []),
        ("rival: 西首 IDS, 西二 MES, 西三 EAF (Ethiopian Highlands)", sec({"西山經之首": "IDS", "西次二經": "MES", "西次三經": "EAF"}), []),
        ("rival: 西首 CHN, 西二 CHN, 西三 CHN", sec({"西山經之首": "CHN", "西次二經": "CHN", "西次三經": "CHN"}), []),
        ("rival: 西首 CHN, 西二 CHN, 西三 TAR", sec({"西山經之首": "CHN", "西次二經": "CHN", "西次三經": "TAR"}), []),
        ("rival: 西首 CHN, 西二 TIB, 西三 TAR", sec({"西山經之首": "CHN", "西次二經": "TIB", "西次三經": "TAR"}), []),
        ("rival: 西首 IRN, 西二 CAS, 西三 TAR", sec({"西山經之首": "IRN", "西次二經": "CAS", "西次三經": "TAR"}), []),
        ("decoy: 西首 NAM, 西二 NAM, 西三 NAM", sec({"西山經之首": "NAM", "西次二經": "NAM", "西次三經": "NAM"}), []),
    ]
    return cfgs


FULL = {"user": "user: ", "china": "rival: 西首 CHN, 西二 CHN, 西三 CHN", "ethiopia": "rival: 西首 IDS, 西二 MES, 西三 EAF",
        "decoy-nam": "decoy: "}   # configurations also re-solved from scratch (annealing, all chains) to rule out start bias


def run_full(key, fix):
    d = RUNS / f"full-{key}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "fix.json").write_text(json.dumps(fix, ensure_ascii=False))
    if not (d / "crossval-log.json").exists():
        r = subprocess.run([sys.executable, "-I", str(ROOT / "tools/shj/kg_crossval.py"), "--fix", str(d / "fix.json"),
                            "--out", str(d)], capture_output=True, text=True)
        (d / "log.txt").write_text(r.stderr)
    return key, json.loads((d / "crossval-log.json").read_text())


def run(name, cfg_list, sets):
    d = RUNS / name
    d.mkdir(parents=True, exist_ok=True)
    if (d / "scan.jsonl").exists() and sum(1 for _ in (d / "scan.jsonl").open()) == len(cfg_list):
        return name, 0
    (d / "configs.json").write_text(json.dumps(cfg_list, ensure_ascii=False))
    args = [sys.executable, "-I", str(ROOT / "tools/shj/kg_crossval.py"), "--init", str(KG / "mapping.jsonl"),
            "--scan", str(d / "configs.json"), "--out", str(d)]
    for s in sets:
        args += ["--set", s]
    r = subprocess.run(args, capture_output=True, text=True)
    (d / "log.txt").write_text(r.stderr)
    return name, r.returncode


def main():
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    nodes = jl(KG / "nodes.jsonl")
    regions = jl(WORLD / "regions.jsonl")
    rname = {r["code"]: r["name"] for r in regions}
    sec_nodes = defaultdict(list)
    first = {}
    for n in nodes:
        if n["type"] == "MTN" and n["props"].get("section"):
            s = n["props"]["section"]
            sec_nodes[s].append(n["id"])
            first[s] = min(first.get(s, "~"), min(n["mentions"]))
    sections = sorted(sec_nodes, key=lambda s: first[s])
    # scan jobs: one process per section (33 configurations each); configuration jobs grouped by their --set
    tasks = [(f"scan-{i:02d}", [{"name": f"{s}|{r['code']}", "fix": {n: f"region:{r['code']}" for n in sec_nodes[s]}}
                                for r in regions], []) for i, s in enumerate(sections)]
    by_sets = defaultdict(list)
    for name, fix, sets in configurations(sec_nodes):
        by_sets[tuple(sets)].append({"name": name, "fix": fix})
    for k, (sets, cl) in enumerate(sorted(by_sets.items())):
        tasks.append((f"configs-{k}", cl, list(sets)))
    with ThreadPoolExecutor(jobs) as ex:
        for name, rc in ex.map(lambda t: run(*t), tasks):
            print(f"{name}: {'ok' if rc == 0 else 'FAILED'}", file=sys.stderr)
    rows = [r for t in tasks for r in jl(RUNS / t[0] / "scan.jsonl")]
    cfg_fix = {c["name"]: c["fix"] for cl in by_sets.values() for c in cl}
    full_jobs = [(k, cfg_fix[next(n for n in cfg_fix if n.startswith(p))]) for k, p in FULL.items()]
    with ThreadPoolExecutor(min(jobs, len(full_jobs))) as ex:
        full = dict(ex.map(lambda t: run_full(*t), full_jobs))
    free_full = json.loads((KG / "crossval-log.json").read_text())
    with (OUT / "scan.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    scan = defaultdict(dict)
    for r in rows:
        if "|" in r["name"]:
            s, code = r["name"].split("|")
            scan[s][code] = r["energy"]
    cfg = {r["name"]: r for r in rows if "|" not in r["name"]}
    free = cfg["free (baseline, nothing held)"]["energy"]
    best_map = {}
    L = ["# 篇段層級的地區檢驗 / Section-level region tests", "",
         "每一篇的山全部放在某一地區，其餘全書重新擬合（ICM 與區塊調整，從基準對應出發），記錄總分。ΔE = 與該篇最佳地區的差。"
         "這是局部擬合，不是完整重解：用來比較，不是絕對值。",
         "Each section's mountains are held in one region and the rest of the book is re-fitted (ICM and block moves from "
         "the baseline). ΔE is the loss against the section's best region. A local re-fit, for comparison.", "",
         "## 1. 各篇最佳地區 / Best regions per section", "",
         "| 篇 / section | 山數 | 第一 / 1st | 第二 / 2nd (ΔE) | 第三 / 3rd (ΔE) | EGY ΔE | MES ΔE | IDS ΔE | CHN ΔE |",
         "|---|---|---|---|---|---|---|---|---|"]
    for s in sections:
        e = scan[s]
        rk = sorted(e, key=lambda c: -e[c])
        top = e[rk[0]]
        best_map[s] = {"best": rk[0], "second": rk[1], "margin": round(top - e[rk[1]], 2),
                       "ranking": [(c, round(top - e[c], 2)) for c in rk]}
        L.append(f"| {s} | {len(sec_nodes[s])} | {rk[0]} | {rk[1]} ({top - e[rk[1]]:.1f}) | {rk[2]} ({top - e[rk[2]]:.1f}) | "
                 + " | ".join(f"{top - e[c]:.1f} (#{rk.index(c) + 1})" for c in ("EGY", "MES", "IDS", "CHN")) + " |")
    (OUT / "section-best.json").write_text(json.dumps(best_map, ensure_ascii=False, indent=1))
    L += ["", "## 2. 聯合假說 / Joint configurations", "",
          f"ΔE 相對於不固定任何實體的基準（{free:.1f}）。違反 = 被固定的實體所違反的關係數與分數。",
          f"ΔE against the free baseline ({free:.1f}). Violated = relations broken by the held entities.", "",
          "| 組態 / configuration | 固定數 | ΔE | 違反 / violated (score) | 河 | 赤水 | 黑水 | 崑崙之丘 |", "|---|---|---|---|---|---|---|---|"]
    for name, r in sorted(cfg.items(), key=lambda kv: -kv[1]["energy"]):
        k = r["key"]
        L.append(f"| {name} | {r['n_fixed']} | {r['energy'] - free:+.1f} | {r['violated']} ({r['violated_score']}) | "
                 f"{(k.get('WAT:河') or '—').split(':')[-1]} | {(k.get('WAT:赤') or '—').split(':')[-1]} | "
                 f"{(k.get('WAT:黑') or '—').split(':')[-1]} | {(k.get('MTN:昆侖之丘') or '—').split(':')[-1]} |")
    L += ["", "### 完整重解 / Full re-solves", "",
          "從頭模擬退火（6 條鏈，固定實體不動），排除「從基準出發」造成的偏差。/ Annealing from scratch with the held "
          "entities fixed, to rule out a bias from starting at the baseline.", "",
          "| 組態 / configuration | 最佳總分 / best energy | 相對自由解 / vs free | 各鏈 / chains |", "|---|---|---|---|",
          f"| free (nothing held) | {free_full['best_energy']} | 0 | {free_full['chain_energies']} |"]
    for k, lg in sorted(full.items(), key=lambda kv: -kv[1]["best_energy"]):
        L.append(f"| {FULL[k].rstrip(': ')} ({k}) | {lg['best_energy']} | {lg['best_energy'] - free_full['best_energy']:+.1f} | "
                 f"{lg['chain_energies']} |")
    (OUT / "full-resolves.json").write_text(json.dumps({"free": free_full, **full}, ensure_ascii=False, indent=1))
    u = cfg[[n for n in cfg if n.startswith("user: ")][0]]
    L += ["", "## 3. 使用者假說最嚴重的違反 / Worst relations broken by the user's configuration", "",
          "| 關係 | 甲 → 乙 | 對應 | 條目 | 分數 |", "|---|---|---|---|---|"]
    for x in u["violated_top"]:
        L.append(f"| {x['relation']} | {x['a']} → {x['b'] or '—'} | {x['a_cand']} / {x['b_cand'] or '—'} | `{x['entry']}` | {x['score']} |")
    L += ["", "地區代碼 / region codes: " + "；".join(f"{c} {rname[c]}" for c in sorted(rname))]
    (OUT / "sections.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]), file=sys.stderr)


if __name__ == "__main__":
    main()
