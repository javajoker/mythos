"""Observer frame and section profiles (framework v3 R9; methodology-spec §4; task T-V04).

For every Mountain-Classic section: the route rebuilt from its legs (「又{方}{N}里」) in li, east (x) and north (y) of
the section's first station, with the start and the li-to-km scale left unknown; plus a profile of what the section
describes — terrain (barren, sand, snow, marsh, water), resources, plants, creatures, and its waters with their
directions, destinations and name features. Profiles are the input for the section-level anchoring and, masked, for
the semantic judgments.

Outputs (projects/shanhaijing/data/derived/era/): frame.jsonl (one line per station), profiles.jsonl (one line per
section), profiles.md (readable).
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DER = ROOT / "projects/shanhaijing/data/derived"
OUT = DER / "era"
ORIGIN = (34.7, 113.6)          # Central Plains (era-world.md §6)
COLOURS = {"赤": "red", "丹": "red", "朱": "red", "黑": "black", "玄": "black", "白": "white", "素": "white",
           "青": "blue-green", "蒼": "blue-green", "碧": "blue-green", "黃": "yellow"}
STATES = {"弱": "weak (cannot carry)", "流": "flowing", "炎": "blazing", "湯": "hot", "溫": "warm", "鹽": "salt"}
TERRAIN = [(r"無草木", "barren"), (r"流沙|多沙|沙", "sand"), (r"澤|淵|沮洳", "marsh/pool"), (r"冬夏有雪|有雪", "snow"),
           (r"多水|水出", "watery"), (r"石", "stony"), (r"湯|溫", "hot water"), (r"炎火|投物輒然", "fire or heat"),
           (r"削成而四方", "square-cut form"), (r"其高|萬仞|千仞", "high"), (r"穴", "caves")]


def jl(p):
    return [json.loads(l) for l in Path(p).open() if l.strip()]


def name_features(name):
    f = {}
    for ch, v in COLOURS.items():
        if ch in name:
            f["colour"] = v
    for ch, v in STATES.items():
        if ch in name:
            f["state"] = v
    return f


def compass(dx, dy):
    if dx == 0 and dy == 0:
        return "—", None
    deg = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    names = ["北", "東北", "東", "東南", "南", "西南", "西", "西北"]
    return names[int((deg + 22.5) // 45) % 8], round(deg)


def main():
    stations = jl(DER / "stations.jsonl")
    entries = {e["id"]: e for e in jl(ROOT / "reference/shanhaijing/data/entries.jsonl")}
    sections = {s["section"]: s for s in jl(DER / "sections.jsonl")}
    by_sec = defaultdict(list)
    for s in stations:
        by_sec[s["section"]].append(s)
    OUT.mkdir(parents=True, exist_ok=True)
    frame, profiles = [], []
    for sec, ss in by_sec.items():
        ss.sort(key=lambda s: s["seq"])
        x = y = 0.0
        bearings = Counter()
        terrain = Counter()
        waters = []
        res = Counter()
        crit = []
        unresolved = 0
        for s in ss:
            if s.get("bearing_deg") is not None and s.get("leg_li"):
                r = math.radians(s["bearing_deg"])
                x += s["leg_li"] * math.sin(r)
                y += s["leg_li"] * math.cos(r)
                bearings[s["bearing"]] += s["leg_li"]
            elif not s.get("start"):
                unresolved += 1
            t = entries[s["entry_id"]]["text"]
            for rx, tag in TERRAIN:
                if re.search(rx, t):
                    terrain[tag] += 1
            for m in re.finditer(r"(?:其上|其下|其陽|其陰|其中)?多([金玉銀銅鐵錫丹青碧雄黃赭堊砥礪文石沙竹箭松柏漆桑棕櫟]{1,3})", t):
                res[m.group(1)] += 1
            for r_ in s.get("rivers", []):
                waters.append({"station": s["name"], "water": r_["river"], "flow": r_.get("flow"), "to": r_.get("to"),
                               "name_features": name_features(r_["river"]), "to_features": name_features(r_.get("to") or "")})
            for c in s.get("creatures", []):
                crit.append({"station": s["name"], "kind": c["kind"], "desc": c["desc"]})
            frame.append({"section": sec, "seq": s["seq"], "station": s["name"], "entry": s["entry_id"],
                          "x_li": round(x), "y_li": round(y), "bearing": s.get("bearing"), "leg_li": s.get("leg_li")})
        net_dir, net_deg = compass(x, y)
        dest = Counter(w["to"] for w in waters if w["to"])
        prof = {"section": sec, "book": ss[0]["book"], "stations": len(ss), "stated_li": sections.get(sec, {}).get("stated_li"),
                "leg_li_sum": sum(s.get("leg_li") or 0 for s in ss), "net_x_li": round(x), "net_y_li": round(y),
                "net_direction": net_dir, "net_deg": net_deg, "net_li": round(math.hypot(x, y)),
                "legs_by_bearing": dict(bearings.most_common()), "unresolved_legs": unresolved,
                "terrain": dict(terrain.most_common()), "resources": dict(res.most_common(12)),
                "waters": waters, "water_destinations": dict(dest.most_common()), "creatures": crit}
        profiles.append(prof)
    order = ["南山經", "西山經", "北山經", "東山經", "中山經"]
    profiles.sort(key=lambda p: (order.index(p["book"]), min(f["entry"] for f in frame if f["section"] == p["section"])))
    with (OUT / "frame.jsonl").open("w") as f:
        for r in frame:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with (OUT / "profiles.jsonl").open("w") as f:
        for p in profiles:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    L = ["# 山經各篇的觀察框架與概況 / Section frames and profiles", "",
         "路線由各站的「又{方}{N}里」累計（東 = x、北 = y，單位為里）；起點與里的長度未知。地形、物產、水與生物取自原文。",
         "Routes accumulated from the legs (x east, y north, in li); start and li length unknown.", ""]
    for p in profiles:
        L += [f"## {p['book']}・{p['section']}", "",
              f"- 站數 {p['stations']}；篇末總數 {p['stated_li']} 里；各段合計 {p['leg_li_sum']} 里；"
              f"淨位移 {p['net_li']} 里，方向 {p['net_direction']}（{p['net_deg']}°）；無方位的段 {p['unresolved_legs']}",
              f"- 各方位里數 / li by bearing：{p['legs_by_bearing']}",
              f"- 地形線索 / terrain：{p['terrain']}",
              f"- 物產 / resources：{p['resources']}",
              f"- 水的去處 / water destinations：{p['water_destinations']}",
              "- 水 / waters：" + "；".join(f"{w['water']}（{w['flow'] or '?'}→{w['to'] or '?'}"
                                          + (f"，名稱特徵 {w['name_features']}" if w['name_features'] else "") + "）"
                                          for w in p["waters"]), ""]
    (OUT / "profiles.md").write_text("\n".join(L) + "\n")
    print(f"{len(frame)} stations, {len(profiles)} sections", file=sys.stderr)


if __name__ == "__main__":
    main()
