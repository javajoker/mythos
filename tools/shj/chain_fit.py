"""Project a 山經 itinerary chain onto the Earth from one anchored station (methodology spec stage S7).

The chain is rebuilt from the text's own bearings (8-point) and leg distances, then Monte Carlo
perturbed with the error model of spec §6.3:
  bearing   : uniform ±22.5° (8-point compass resolution)
  distance  : log-normal, sigma = 0.30 (ancient pacing/estimation error)
  里 length : uniform [LI_MIN, LI_MAX] metres per run (scale is NOT assumed; see spec §6.4)
The result is where each station *would have to be* if the anchor hypothesis were true —
a prediction to check against real geography, never an identification by itself.

Usage:
  python3 -I tools/shj/chain_fit.py --section 西次三經 --anchor 昆侖之丘 --lat 29.975 --lon 31.138 \
      [--li-min 300 --li-max 500 --runs 4000 --seed 1] [--md out.md]
"""
import argparse
import json
import math
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATIONS = ROOT / "projects/shanhaijing/data/derived/stations.jsonl"
R_EARTH_KM = 6371.0


def load_chain(section: str):
    chain = [json.loads(l) for l in STATIONS.open() if json.loads(l)["section"] == section]
    if not chain:
        raise SystemExit(f"no stations for section {section}")
    return chain


def offsets_km(chain, li_m, rng=None, sb=22.5, sd=0.30):
    """Cumulative (east_km, north_km) of every station relative to station 0."""
    x = y = 0.0
    out = [(0.0, 0.0)]
    for st in chain[1:]:
        if st.get("bearing_deg") is None or not st.get("leg_li"):
            out.append((x, y)); continue
        b, d = st["bearing_deg"], st["leg_li"] * li_m / 1000
        if rng:
            b += rng.uniform(-sb, sb)
            d *= math.exp(rng.gauss(0, sd))
        x += d * math.sin(math.radians(b))
        y += d * math.cos(math.radians(b))
        out.append((x, y))
    return out


def to_latlon(lat0, lon0, east_km, north_km):
    lat = lat0 + math.degrees(north_km / R_EARTH_KM)
    lon = lon0 + math.degrees(east_km / (R_EARTH_KM * math.cos(math.radians((lat0 + lat) / 2))))
    return lat, lon


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True)
    ap.add_argument("--anchor", required=True, help="station name to pin")
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--li-min", type=float, default=300)
    ap.add_argument("--li-max", type=float, default=500)
    ap.add_argument("--runs", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--md")
    a = ap.parse_args()

    chain = load_chain(a.section)
    idx = next((i for i, s in enumerate(chain) if s["name"] == a.anchor), None)
    if idx is None:
        raise SystemExit(f"anchor {a.anchor} not in {a.section}: {[s['name'] for s in chain]}")
    rng = random.Random(a.seed)
    samples = [[] for _ in chain]
    for _ in range(a.runs):
        li = rng.uniform(a.li_min, a.li_max)
        off = offsets_km(chain, li, rng)
        ax, ay = off[idx]
        for i, (x, y) in enumerate(off):
            samples[i].append(to_latlon(a.lat, a.lon, x - ax, y - ay))

    nominal = offsets_km(chain, (a.li_min + a.li_max) / 2)
    nx, ny = nominal[idx]
    rows = []
    for i, st in enumerate(chain):
        lats = [p[0] for p in samples[i]]; lons = [p[1] for p in samples[i]]
        mlat, mlon = statistics.fmean(lats), statistics.fmean(lons)
        dists = sorted(math.hypot((la - mlat) * 111.2, (lo - mlon) * 111.2 * math.cos(math.radians(mlat)))
                       for la, lo in zip(lats, lons))
        r90 = dists[int(0.9 * len(dists)) - 1]
        nlat, nlon = to_latlon(a.lat, a.lon, nominal[i][0] - nx, nominal[i][1] - ny)
        rows.append({"seq": st["seq"], "entry_id": st["entry_id"], "name": st["name"],
                     "bearing": st.get("bearing") or "—", "leg_li": st.get("leg_li") or 0,
                     "lat": round(nlat, 2), "lon": round(nlon, 2), "r90_km": round(r90)})

    head = (f"Chain fit — section **{a.section}**, anchor **{a.anchor}** = ({a.lat}, {a.lon}); "
            f"里 ∈ [{a.li_min:.0f}, {a.li_max:.0f}] m; {a.runs} Monte Carlo runs; seed {a.seed}.")
    lines = [head, "", "| # | entry | station | bearing | leg 里 | nominal lat | nominal lon | 90% radius km |",
             "|---|---|---|---|---|---|---|---|"]
    lines += [f"| {r['seq']} | `{r['entry_id']}` | {r['name']} | {r['bearing']} | {r['leg_li']} | {r['lat']} | "
              f"{r['lon']} | {r['r90_km']} |" for r in rows]
    text = "\n".join(lines) + "\n"
    if a.md:
        Path(a.md).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
