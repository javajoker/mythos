"""Two-anchor calibration of 山經 itineraries against a candidate real-world frame (spec §6.4, §7.1).

For every pair of anchored stations in the same section, compare the text's displacement (from its own bearings
and 里 distances) with the real displacement between the anchors:
  implied 里 length  = real distance / text distance          (must be physically plausible, ~250–600 m)
  bearing residual   = angle between text and real direction  (0° = perfect; 90° = no information)
A null test asks how likely the observed mean bearing residual is if the text's bearings carried no information
(residuals uniform on 0–180°).

Usage: python3 -I tools/shj/calibrate.py --anchors projects/shanhaijing/data/geo/anchors-yellow-yangtze.jsonl \
           [--basis "hydrological role"] [--md out.md]
"""
import argparse
import itertools
import json
import math
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chain_fit import offsets_km  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STATIONS = ROOT / "projects/shanhaijing/data/derived/stations.jsonl"


def haversine(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = 2 * 6371 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 +
                                       math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return d, (math.degrees(math.atan2(y, x)) + 360) % 360


def angdiff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchors", required=True)
    ap.add_argument("--basis", default=None, help="only use anchors with this anchor_basis")
    ap.add_argument("--runs", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--adjacent", action="store_true", help="only consecutive anchors in each section "
                    "(non-overlapping pairs, for an honest significance test)")
    ap.add_argument("--md")
    a = ap.parse_args()

    anchors = [json.loads(l) for l in open(a.anchors) if l.strip()]
    if a.basis:
        anchors = [x for x in anchors if x["anchor_basis"] == a.basis]
    stations = [json.loads(l) for l in STATIONS.open()]
    rng = random.Random(a.seed)
    rows = []
    for sec in sorted({x["section"] for x in anchors}):
        chain = [s for s in stations if s["section"] == sec]
        names = [s["name"] for s in chain]
        here = [x for x in anchors if x["section"] == sec and x["station"] in names]
        here.sort(key=lambda x: names.index(x["station"]))
        pairs = list(zip(here, here[1:])) if a.adjacent else itertools.combinations(here, 2)
        for p, q in pairs:
            i, j = sorted((names.index(p["station"]), names.index(q["station"])))
            if names[i] != p["station"]:
                p, q = q, p
            off = offsets_km(chain, 1000.0)          # 1 里 = 1 km -> offsets are in 里
            dx, dy = off[j][0] - off[i][0], off[j][1] - off[i][1]
            text_li = math.hypot(dx, dy)
            text_brg = (math.degrees(math.atan2(dx, dy)) + 360) % 360
            path_li = sum(s["leg_li"] or 0 for s in chain[i + 1:j + 1])
            real_km, real_brg = haversine((p["lat"], p["lon"]), (q["lat"], q["lon"]))
            sims = []
            for _ in range(a.runs):
                o = offsets_km(chain, 1000.0, rng)
                sdx, sdy = o[j][0] - o[i][0], o[j][1] - o[i][1]
                sims.append(real_km * 1000 / max(1e-6, math.hypot(sdx, sdy)))
            sims.sort()
            rows.append({"_p": p, "_q": q, "section": sec, "from": p["station"], "to": q["station"], "legs": j - i,
                         "path_li": path_li, "text_li": round(text_li), "text_brg": round(text_brg),
                         "real_km": round(real_km), "real_brg": round(real_brg),
                         "li_m": round(real_km * 1000 / text_li) if text_li else None,
                         "li_m_90": [round(sims[int(.05 * len(sims))]), round(sims[int(.95 * len(sims))])],
                         "li_m_path": round(real_km * 1000 / path_li) if path_li else None,
                         "brg_resid": round(angdiff(text_brg, real_brg)),
                         "basis": f"{p['anchor_basis']} / {q['anchor_basis']}"})

    res = [r["brg_resid"] for r in rows]
    mean_res = statistics.fmean(res) if res else float("nan")
    null = [statistics.fmean(rng.uniform(0, 180) for _ in res) for _ in range(20000)] if res else []
    p_null = sum(m <= mean_res for m in null) / len(null) if null else float("nan")
    li = [r["li_m"] for r in rows if r["li_m"]]
    # permutation test: does matching THESE real places to THESE stations matter? Shuffle the real coordinates among
    # the anchors of each section and recompute the mean bearing residual.
    perm_better, n_perm = 0, 5000
    for _ in range(n_perm):
        tot = []
        for sec in sorted({r["section"] for r in rows}):
            rs = [r for r in rows if r["section"] == sec]
            pts = {id(x): x for r in rs for x in (r["_p"], r["_q"])}
            keys = list(pts); vals = [(pts[k]["lat"], pts[k]["lon"]) for k in keys]
            rng.shuffle(vals)
            m = dict(zip(keys, vals))
            for r in rs:
                _, b = haversine(m[id(r["_p"])], m[id(r["_q"])])
                tot.append(angdiff(r["text_brg"], b))
        perm_better += statistics.fmean(tot) <= mean_res
    p_perm = perm_better / n_perm
    lines = [f"Two-anchor calibration — anchors `{Path(a.anchors).name}`"
             + (f" (basis: {a.basis})" if a.basis else "") + f"; {a.runs} Monte Carlo runs, seed {a.seed}.", "",
             "| section | from → to | legs | path 里 | displacement 里 | text bearing | real km | real bearing | "
             "bearing residual | implied 里 (m) | 90% range (m) | 里 if path = distance (m) |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['section']} | {r['from']} → {r['to']} | {r['legs']} | {r['path_li']} | {r['text_li']} | "
                     f"{r['text_brg']}° | {r['real_km']} | {r['real_brg']}° | {r['brg_resid']}° | {r['li_m']} | "
                     f"{r['li_m_90'][0]}–{r['li_m_90'][1]} | {r['li_m_path']} |")
    if rows:
        lines += ["", f"- pairs: {len(rows)}; mean bearing residual **{mean_res:.0f}°** "
                      f"(no-information expectation 90°); P(mean ≤ observed | no information) = **{p_null:.4f}**; "
                      f"permutation test (shuffle which real place goes with which station) p = **{p_perm:.4f}**",
                  f"- implied 里 length: median **{statistics.median(li):.0f} m**, range {min(li)}–{max(li)} m "
                  f"(plausible band 250–600 m)"]
    text = "\n".join(lines) + "\n"
    if a.md:
        Path(a.md).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
