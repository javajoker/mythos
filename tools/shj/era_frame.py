"""Build independent section frames from working text; report, never adjudicate.

Every Mountain-Classic section is rebuilt from its own legs. Start and scale are
unknown. Cross-section distance is never inferred by this tool. Discrepancies are
review candidates for LLM adjudication, not automatic textual corrections.
Dynamic flow is preserved as a source assertion and also exposed as an undirected
comparison connection. Modern flow direction is not a candidate veto.
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
WORKING = DER / "working-text.jsonl"
COLOURS = {"赤": "red", "丹": "red", "朱": "red", "黑": "black", "玄": "black", "白": "white", "素": "white",
           "青": "blue-green", "蒼": "blue-green", "碧": "blue-green", "黃": "yellow"}
STATES = {"弱": "weak (cannot carry)", "流": "flowing", "炎": "blazing", "湯": "hot", "溫": "warm", "鹽": "salt"}
TERRAIN = [(r"無草木", "barren"), (r"流沙|多沙|沙", "sand"), (r"澤|淵|沮洳", "marsh/pool"), (r"冬夏有雪|有雪", "snow"),
           (r"多水|水出", "watery"), (r"石", "stony"), (r"湯|溫", "hot water"), (r"炎火|投物輒然", "fire or heat"),
           (r"削成而四方", "square-cut form"), (r"其高|萬仞|千仞", "high"), (r"穴", "caves")]


def jl(path):
    return [json.loads(line) for line in Path(path).open(encoding="utf-8") if line.strip()]


def name_features(name):
    features = {}
    for char, value in COLOURS.items():
        if char in name:
            features["colour"] = value
    for char, value in STATES.items():
        if char in name:
            features["state"] = value
    return features


def compass(dx, dy):
    if dx == 0 and dy == 0:
        return "—", None
    degrees = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    names = ["北", "東北", "東", "東南", "南", "西南", "西", "西北"]
    return names[int((degrees + 22.5) // 45) % 8], round(degrees)


def main():
    if not WORKING.exists():
        raise SystemExit("working-text.jsonl is required; run align_witness.py first")
    working = {row["entry_id"]: row for row in jl(WORKING) if row.get("entry_id")}
    stations = jl(DER / "stations.jsonl")
    sections = {s["section"]: s for s in jl(DER / "sections.jsonl")}
    by_sec = defaultdict(list)
    for station in stations:
        by_sec[station["section"]].append(station)
    OUT.mkdir(parents=True, exist_ok=True)
    frame, profiles = [], []
    for section_name, section_stations in by_sec.items():
        section_stations.sort(key=lambda s: s["seq"])
        x = y = 0.0
        bearings, terrain, resources = Counter(), Counter(), Counter()
        waters, creatures = [], []
        unresolved = 0
        for station in section_stations:
            if station.get("bearing_deg") is not None and station.get("leg_li"):
                radians = math.radians(station["bearing_deg"])
                x += station["leg_li"] * math.sin(radians)
                y += station["leg_li"] * math.cos(radians)
                bearings[station["bearing"]] += station["leg_li"]
            elif not station.get("start"):
                unresolved += 1
            row = working[station["entry_id"]]
            text = row["text"]
            for pattern, tag in TERRAIN:
                if re.search(pattern, text):
                    terrain[tag] += 1
            for match in re.finditer(r"(?:其上|其下|其陽|其陰|其中)?多([金玉銀銅鐵錫丹青碧雄黃赭堊砥礪文石沙竹箭松柏漆桑棕櫟]{1,3})", text):
                resources[match.group(1)] += 1
            for river in station.get("rivers", []):
                waters.append({"station": station["name"], "water": river["river"], "flow": river.get("flow"), "to": river.get("to"),
                               "undirected_connection": ({"a": river["river"], "b": river["to"]} if river.get("to") else None),
                               "name_features": name_features(river["river"]),
                               "to_features": name_features(river.get("to") or "")})
            for creature in station.get("creatures", []):
                creatures.append({"station": station["name"], "kind": creature["kind"], "desc": creature["desc"]})
            frame.append({"section": section_name, "seq": station["seq"], "station": station["name"],
                          "entry": station["entry_id"], "x_li": round(x), "y_li": round(y),
                          "bearing": station.get("bearing"), "leg_li": station.get("leg_li"),
                          "reading_source": row.get("reading_source"), "reading_status": row.get("reading_status")})
        net_dir, net_deg = compass(x, y)
        stated = sections.get(section_name, {}).get("stated_li")
        stated_mountains = sections.get(section_name, {}).get("stated_mountains")
        leg_sum = sum(s.get("leg_li") or 0 for s in section_stations)
        diff = (leg_sum - stated) / stated if stated else None
        if diff is None:
            status = "no total"
        elif abs(diff) <= 0.10:
            status = "consistent"
        elif abs(diff) <= 0.20:
            status = "review: minor gap or unparsed leg"
        else:
            status = "review: LLM required"
        destinations = Counter(w["to"] for w in waters if w["to"])
        profiles.append({"section": section_name, "book": section_stations[0]["book"], "stations": len(section_stations),
                         "stated_li": stated, "leg_li_sum": leg_sum, "net_x_li": round(x), "net_y_li": round(y),
                         "net_direction": net_dir, "net_deg": net_deg, "net_li": round(math.hypot(x, y)),
                         "stated_mountains": stated_mountains, "total_diff": round(diff, 3) if diff is not None else None,
                         "total_status": status, "legs_by_bearing": dict(bearings.most_common()),
                         "unresolved_legs": unresolved, "terrain": dict(terrain.most_common()),
                         "resources": dict(resources.most_common(12)), "waters": waters,
                         "water_destinations": dict(destinations.most_common()), "creatures": creatures})
    order = ["南山經", "西山經", "北山經", "東山經", "中山經"]
    profiles.sort(key=lambda p: (order.index(p["book"]), min(f["entry"] for f in frame if f["section"] == p["section"])))
    with (OUT / "frame.jsonl").open("w", encoding="utf-8") as handle:
        for row in frame:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "profiles.jsonl").open("w", encoding="utf-8") as handle:
        for profile in profiles:
            handle.write(json.dumps(profile, ensure_ascii=False) + "\n")

    lines = ["# 山經各篇的觀察框架與概況 / Section frames and profiles", "",
             "各篇依自身站段累計；起點與比例尺未知，篇間距離不自動推定。/ Independent sections; unknown start and scale.", ""]
    for profile in profiles:
        lines += [f"## {profile['book']}・{profile['section']}", "",
                  f"- 站數 {profile['stations']}；篇末總數 {profile['stated_li']} 里；各段合計 {profile['leg_li_sum']} 里；"
                  f"淨位移 {profile['net_li']} 里，方向 {profile['net_direction']}（{profile['net_deg']}°）；無方位段 {profile['unresolved_legs']}",
                  f"- 里程審查 / total review：{profile['total_status']}",
                  f"- 各方位里數 / li by bearing：{profile['legs_by_bearing']}",
                  f"- 地形線索 / terrain：{profile['terrain']}",
                  f"- 物產 / resources：{profile['resources']}",
                  f"- 水的去處 / water destinations：{profile['water_destinations']}",
                  "- 水 / waters：" + "；".join(
                      f"{w['water']}（{w['flow'] or '?'}→{w['to'] or '?'}）"
                      + (f"，名稱特徵 {w['name_features']}" if w["name_features"] else "")
                      for w in profile["waters"]), ""]
    (OUT / "profiles.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    totals = ["# 篇末總數與分段合計 / Stated totals and leg sums", "",
              "差異只作為 LLM 審查候選；本工具不改寫篇末總數，也不把跨篇合計視為地理跨度。", "",
              "| 經 | 篇 | 山（篇末／抽出）| 篇末總數 | 各段合計 | 差 | 審查狀態 |",
              "|---|---|---|---|---|---|---|"]
    books = defaultdict(lambda: [0, 0])
    for profile in profiles:
        totals.append(f"| {profile['book']} | {profile['section']} | {profile['stated_mountains']}／{profile['stations']} | "
                      f"{profile['stated_li']} | {profile['leg_li_sum']} | {(profile['total_diff'] * 100):+.1f}% | {profile['total_status']} |")
        books[profile["book"]][0] += profile["stated_li"] or 0
        books[profile["book"]][1] += profile["leg_li_sum"]
    totals += ["", "| 經 | 篇末總數合計 | 各段合計（不是地理跨度）|", "|---|---|---|"]
    for book in order:
        totals.append(f"| {book} | {books[book][0]} | {books[book][1]} |")
    totals += ["", "跨篇連接須另有文本或已接受關係證據；里程差異由 LLM 裁決。"]
    (OUT / "totals.md").write_text("\n".join(totals) + "\n", encoding="utf-8")
    print(f"{len(frame)} stations, {len(profiles)} sections", file=sys.stderr)


if __name__ == "__main__":
    main()
