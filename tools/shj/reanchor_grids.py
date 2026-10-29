# -*- coding: utf-8 -*-
"""全鏈算術網格重錨（方案②，2026-10-29 發起人批准）。

每條子經：anchor 改為首站（index 0）的**語義站位**（map spec fit_coords[1]；
無 fit 者用現網格首站 0.385 位置——此時網格不變），自 chain_grid 前向展開。
字面保真段自此兩層重合；分歧起點＝文本里程層累起點。網格仍為 G-3 否定檢核帶。
xici2/3/4 無 grid spec——由 grid jsonl 反建 spec 落盤（補齊事實源）。
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
BEAR = {"北": 0, "東北": 45, "東": 90, "東南": 135, "南": 180, "西南": 225, "西": 270, "西北": 315}
BEAR_NAME = {v: k for k, v in BEAR.items()}
SLUGS = [f"{p}ci{c}" for p, n in [("nan", 3), ("xi", 4), ("bei", 3), ("dong", 4), ("zhong", 12)]
         for c in range(1, n + 1)]


def main():
    for slug in SLUGS:
        gspec = ADJ / "specs" / f"{slug}.json"
        grid_file = ADJ / f"{slug}-station-grid.jsonl"
        recs = {}
        if grid_file.exists():
            for line in open(grid_file, encoding="utf-8"):
                r = json.loads(line)
                if "station" in r:
                    recs[r["order"]] = r
        if not gspec.exists():
            # 由 grid 反建 spec
            if not recs:
                print(f"{slug}: 無 spec 無 grid，跳過"); continue
            stations = [r["station"] for _, r in sorted(recs.items())]
            legs = [None]
            for _, r in sorted(recs.items()):
                lg = r.get("leg")
                if lg:
                    legs.append([BEAR.get(lg["bearing"], -1), lg["li"]])
            g1 = recs[1]["grid"]["0.385"]
            spec = {"stations": stations, "legs": legs,
                    "anchor": {"index": 0, "lat": g1["lat"], "lon": g1["lon"]},
                    "bearnames": {str(v): k for k, v in BEAR.items()},
                    "meta": {"meta": f"{slug} 站點網格 spec（2026-10-29 由 grid 反建落盤＋方案②首站重錨）",
                             "version": "rebuild-1", "scales": [0.35, 0.385, 0.42]},
                    "out": f"{slug}-station-grid.jsonl"}
            json.dump(spec, open(gspec, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"{slug}: spec 反建")
            continue
        spec = json.load(open(gspec, encoding="utf-8"))
        # 首站語義站位
        mspec = ADJ / "specs" / f"{slug}-map.json"
        sem1 = None
        if mspec.exists():
            fit = json.load(open(mspec, encoding="utf-8")).get("fit_coords", {})
            if "1" in fit:
                sem1 = fit["1"]  # [lon, lat]
        if sem1 is None and 1 in recs:
            g1 = recs[1]["grid"]["0.385"]
            sem1 = [g1["lon"], g1["lat"]]
        if sem1 is None:
            print(f"{slug}: 首站無語義站位亦無網格，跳過"); continue
        spec["anchor"] = {"index": 0, "lat": sem1[1], "lon": sem1[0]}
        spec["meta"]["meta"] += " 【方案②（2026-10-29）：錨改首站語義站位前向展開——網格為 G-3 否定檢核帶，語義為準】"
        spec["meta"]["version"] = spec["meta"].get("version", "v?") + "+reanchor2"
        json.dump(spec, open(gspec, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run([sys.executable, str(ROOT / "tools/shj/chain_grid.py"), str(gspec)],
                           capture_output=True, text=True)
        print(f"{slug}: reanchor → ({sem1[1]:.2f},{sem1[0]:.2f}) {'ok' if r.returncode == 0 else 'FAIL ' + r.stderr[-200:]}")


if __name__ == "__main__":
    main()
