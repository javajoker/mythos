#!/usr/bin/env python3
"""Render the Xici-1 adaptation map as SVG (v2).

Data-driven from xici1-station-grid.jsonl (0.385 band, v2). Basemap
(Yellow River first bend, Yangtze upper system, Yarlung, plateau lakes)
is simplified示意 geometry. All mappings proposed_pending_review.
Built-in overflow audit.
"""
import json, math, os, re

HERE = os.path.join(os.path.dirname(__file__), "..", "..", "projects", "shanhaijing", "data", "derived", "era", "adaptation")
GRID = os.path.join(HERE, "xici1-station-grid.jsonl")
OUT = os.path.join(HERE, "xici1-map.svg")

stations = []
for line in open(GRID):
    r = json.loads(line)
    if "meta" in r:
        continue
    g = r["grid"]["0.385"]
    stations.append({"name": r["station"], "order": r["order"], "lat": g["lat"], "lon": g["lon"]})

short = {
    "錢來之山": "成都平原西緣（東端）｜⛰龍門山·東緣",     "松果之山": "龍門山·濩水注渭",     "太華之山": "邛崍山系花崗岩峰群",
    "小華之山": "邛崍西段·紅腹錦雞｜⛰邛崍山·西段",     "符禺之山": "夾金山方向",     "石脆之山": "大雪山東緣·流赭｜⛰大雪山脈·東緣",
    "英山": "大雪山系·箭竹｜⛰大雪山脈·中段",     "竹山": "雙源·人魚＝大鯢·豪豬｜⛰大雪山脈—川西竹林山",     "浮山": "薰草（香草民俗）｜⛰川西·雅礱江流域山嶺",
    "羭次之山": "神山·川金絲猴｜⛰邛崍山·西段",     "時山": "裸山·水玉｜⛰川西裸岩山嶺",     "南山": "橫斷山北段·猛豹＝熊貓候選",
    "大時之山": "黃河—長江分水嶺｜⛰巴顏喀拉山·東段南麓",     "嶓塚之山": "昌都方向·卡若文化帶｜⛰橫斷山·北段",     "天帝之山": "藏東·杜衡｜⛰念青唐古拉山·東段",
    "塗途之山": "藏東南·西南折點｜⛰念青唐古拉山·東段南麓",     "黃山": "林芝方向·鸚鵡｜⛰念青唐古拉山·東段",     "翠山": "藏東牧區·犛牛麝鹿｜⛰念青唐古拉山·東段",
    "騩山": "念青唐古拉—納木錯東緣（終點）｜⛰念青唐古拉山·東段北麓—納木錯東緣",
}

# ---- projection: lon 88.5..105, lat 28..34.5 ----
LON0, LON1 = 88.5, 105.0
LAT0, LAT1 = 28.0, 34.5
MX, MY = 60, 80
MW, MH = 1000, 560
PANEL_X = MX + MW + 30

def X(lon): return MX + (lon - LON0) / (LON1 - LON0) * MW
def Y(lat): return MY + (LAT1 - lat) / (LAT1 - LAT0) * MH
def pts(seq): return " ".join(f"{X(lo):.1f},{Y(la):.1f}" for lo, la in seq)
def _twidth(t, size):
    w = 0.0
    for c in t:
        o = ord(c)
        if o > 0x2E7F or 0x2190 <= o <= 0x27BF or o in (0x00D7, 0x2248, 0x2013, 0x2014):
            w += size
        else:
            w += size * 0.55
    return w

S = []
def wrap_text(x, y, max_w, size, color, text, lh=None):
    lh = lh or size * 1.45
    line, lines = "", []
    for ch in text:
        if _twidth(line + ch, size) > max_w:
            lines.append(line); line = ch
        else:
            line += ch
    if line:
        lines.append(line)
    for i, ln in enumerate(lines):
        S.append(f'<text x="{x}" y="{y + i * lh:.0f}" font-size="{size}" fill="{color}">{ln}</text>')
    return y + len(lines) * lh

S.append('<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="900" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">')
S.append('<rect x="0" y="0" width="1700" height="900" fill="#f7f3e8"/>')
S.append('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#555"/></marker></defs>')

S.append('<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">《西山經之首》時代假想推理 × 現代映射參照圖 v2</text>')
S.append('<text x="60" y="56" font-size="12" fill="#666">adapt-xici1-2 ｜ 錨點傳播鏈：開羅→西三→西二→本經（無獨立錨點）｜ 0.385 km/里（±150 km）｜ 全部映射 proposed_pending_review</text>')

# ---- terrain shading ----
for name, cx, cy, rx, ry in [("巴顏喀拉（黃河—長江分水嶺）", 98.2, 33.9, 2.6, 0.45),
                             ("橫斷山脈", 98.8, 31.0, 1.8, 1.1),
                             ("邛崍山系", 102.5, 31.2, 0.8, 0.5),
                             ("龍門山", 103.9, 31.6, 0.6, 0.5),
                             ("念青唐古拉", 91.8, 30.5, 1.6, 0.4)]:
    S.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{rx/16.5*MW:.0f}" ry="{ry/6.5*MH:.0f}" fill="#c9b18a" opacity="0.45"/>')
    S.append(f'<text x="{X(cx)-26:.0f}" y="{Y(cy)+3:.0f}" font-size="10" fill="#7a6540">{name}</text>')
S.append(f'<rect x="{X(103.9):.0f}" y="{Y(31.2):.0f}" width="{X(104.9)-X(103.9):.0f}" height="{Y(30.5)-Y(31.2):.0f}" fill="#dce8cf" opacity="0.8"/>')
S.append(f'<text x="{X(104.0):.0f}" y="{Y(30.75):.0f}" font-size="10" fill="#5a7a3a">成都平原</text>')
S.append(f'<rect x="{X(88.5):.0f}" y="{Y(31.5):.0f}" width="{X(97.5)-X(88.5):.0f}" height="{Y(28.0)-Y(31.5):.0f}" fill="#e2d9c8" opacity="0.45"/>')
S.append(f'<text x="{X(89.0):.0f}" y="{Y(28.5):.0f}" font-size="11" fill="#8a7d5f">藏東—藏東南高原</text>')

# ---- plateau lakes ----
S.append(f'<ellipse cx="{X(90.6):.0f}" cy="{Y(30.7):.0f}" rx="16" ry="11" fill="#9dc2dd" stroke="#5b97c4"/>')
S.append(f'<text x="{X(89.85):.0f}" y="{Y(30.35):.0f}" font-size="10" fill="#2f6d9e">納木錯（西海候選A）</text>')
S.append(f'<ellipse cx="{X(88.9):.0f}" cy="{Y(31.8):.0f}" rx="15" ry="8" fill="#9dc2dd" stroke="#7fa8c9" stroke-dasharray="4 3"/>')
S.append(f'<text x="{X(88.55):.0f}" y="{Y(32.1):.0f}" font-size="9" fill="#2f6d9e">色林錯（候選B）</text>')

# ---- rivers (modern reference) ----
yellow = [(95.9,35.0),(97.3,34.9),(99.0,34.65),(100.8,34.45),(102.5,34.0),(103.0,33.65),(101.9,33.8),(101.3,34.4),(101.4,36.0),(102.5,36.2),(103.8,36.06)]
S.append(f'<polyline points="{pts(yellow)}" fill="none" stroke="#c89a2e" stroke-width="2.4"/>')
S.append(f'<text x="{X(98.6):.0f}" y="{Y(34.42):.0f}" font-size="10" fill="#a07d1e">黃河上游河曲（渭候選）</text>')
for nm, ln in [("白河", [(101.3,32.3),(101.5,32.9),(101.95,32.97)]), ("黑河", [(102.2,32.5),(102.5,33.2)])]:
    S.append(f'<polyline points="{pts(ln)}" fill="none" stroke="#c89a2e" stroke-width="1.2"/>')
S.append(f'<text x="{X(101.35):.0f}" y="{Y(32.55):.0f}" font-size="8" fill="#a07d1e">白河/黑河（北注渭格局）</text>')
rivers = [
    ("岷江（沔候選方向）", [(103.6,32.6),(103.62,31.9),(103.62,31.0),(104.1,30.3),(104.6,28.8)]),
    ("大渡河（漢水候選方向）", [(97.4,32.2),(98.9,31.6),(100.2,30.9),(101.4,30.1),(102.3,29.55)]),
    ("雅礱江", [(98.2,32.0),(98.9,30.9),(99.6,29.8),(100.2,28.9)]),
    ("金沙江", [(97.3,31.2),(97.25,30.0),(97.6,29.0),(98.6,28.55)]),
    ("雅魯藏布江（赤水候選）", [(90.2,29.75),(91.5,29.55),(92.8,29.45),(94.0,29.35),(95.2,29.35),(95.9,29.55)]),
    ("尼洋河（盼水方向）", [(94.35,29.95),(93.8,29.75),(93.3,29.55),(93.0,29.5)]),
]
for name, line in rivers:
    S.append(f'<polyline points="{pts(line)}" fill="none" stroke="#2f7fbf" stroke-width="1.6"/>')
S.append(f'<text x="{X(103.35):.0f}" y="{Y(31.6):.0f}" font-size="9" fill="#2f7fbf">岷江（沔候選）</text>')
S.append(f'<text x="{X(99.2):.0f}" y="{Y(30.55):.0f}" font-size="9" fill="#2f7fbf">大渡河（漢水候選）</text>')
S.append(f'<text x="{X(90.4):.0f}" y="{Y(29.45):.0f}" font-size="9" fill="#2f7fbf">雅魯藏布江（赤水候選）</text>')

# ---- xici2 adjacency marker ----
qx, qy = X(90.0), Y(29.5)
S.append(f'<circle cx="{qx:.0f}" cy="{qy:.0f}" r="7" fill="none" stroke="#8e44ad" stroke-width="1.8" stroke-dasharray="3 3"/>')
S.append(f'<text x="{qx-60:.0f}" y="{qy+22:.0f}" font-size="9" fill="#8e44ad">鈐山（西次二經 v2 起點·相鄰）</text>')

# ---- route chain ----
route = [(s["lon"], s["lat"]) for s in stations]
S.append(f'<polyline points="{pts(route)}" fill="none" stroke="#b03a2e" stroke-width="2.6" opacity="0.85"/>')
for i, s in enumerate(stations):
    x, y = X(s["lon"]), Y(s["lat"])
    anchor = (s["name"] == "太華之山")
    r = 8 if anchor else 5
    S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{"#e74c3c" if anchor else "#c0392b"}" stroke="#fff" stroke-width="1.5"/>')
    S.append(f'<text x="{x-4:.0f}" y="{y+4:.0f}" font-size="9" fill="#fff" font-weight="bold">{s["order"]}</text>')
    dy = -11 if i % 2 == 0 else 16
    dx = -26 if anchor else -18
    if anchor:
        dy = -20
    S.append(f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" font-size="10" fill="#7b241c" font-weight="bold">{s["name"]}</text>')

# ---- modern reference points ----
modern = [("成都", 104.07, 30.65), ("拉薩", 91.11, 29.65), ("昌都（卡若）", 97.17, 31.14),
          ("汶川", 103.59, 31.48), ("四姑娘山", 102.83, 31.11), ("貢嘎山", 101.88, 29.6)]
for name, lo, la in modern:
    x, y = X(lo), Y(la)
    S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
    S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

# ---- scale bar (1°lon≈97km @31.5°N; px/deg = MW/16.5) ----
bx, by = X(88.9), Y(28.5)
px100 = 100 / 97.0 * (MW / 16.5)
S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*px100:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
for k in range(5):
    S.append(f'<line x1="{bx + k*px100:.0f}" y1="{by-4:.0f}" x2="{bx + k*px100:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
    S.append(f'<text x="{bx + k*px100 - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*100}</text>')
S.append(f'<text x="{bx + 4*px100 + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

# ---- grid ----
for lon in range(90, 106, 2):
    S.append(f'<line x1="{X(lon):.0f}" y1="{Y(LAT0):.0f}" x2="{X(lon):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(lon)-8:.0f}" y="{Y(LAT0)+14:.0f}" font-size="9" fill="#999">{lon}°E</text>')
for lat in range(29, 35):
    S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(lat):.0f}" x2="{X(LON1):.0f}" y2="{Y(lat):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(lat)+3:.0f}" font-size="9" fill="#999">{lat}°N</text>')

# ---- frame border + panel ----
S.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="none" stroke="#b8ad92" stroke-width="1.4"/>')
px = PANEL_X
S.append(f'<rect x="{px-12}" y="70" width="560" height="800" fill="#fffdf5" stroke="#cbb"/>')
S.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
legend = [
    ("#c0392b", "solid", "里程鏈（19站；成都平原西緣→納木錯）"),
    ("#e74c3c", "star", "大圈＝太華之山（屬性 corroborate，非獨立錨）"),
    ("#2f7fbf", "solid", "現代水體參照（長江上游系/雅魯藏布/湖泊）"),
    ("#c89a2e", "solid", "黃河上游河曲（渭候選）"),
    ("#5b97c4", "solid", "納木錯＝西海候選A"),
    ("#8e44ad", "dash", "鈐山（西次二經 v2 起點——兩經相鄰）"),
    ("#c9b18a", "sq", "山系（簡化示意）"),
    ("#34495e", "sq", "現代地點參照點"),
]
ly = 118
for color, style, label in legend:
    if style == "solid":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
    elif style == "dash":
        S.append(f'<circle cx="{px+13}" cy="{ly}" r="9" fill="none" stroke="{color}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    elif style == "sq":
        S.append(f'<rect x="{px+8}" y="{ly-5}" width="8" height="8" fill="{color}"/>')
    elif style == "star":
        S.append(f'<circle cx="{px+13}" cy="{ly}" r="8" fill="{color}"/>')
    S.append(f'<text x="{px+34}" y="{ly+4}" font-size="11" fill="#444">{label}</text>')
    ly += 22

ly += 8
ly = wrap_text(px, ly, 500, 10, "#666", "錨點傳播鏈（發起人裁定）：開羅（吉薩）→西次三經→西次二經→本經；本經無獨立錨點。鏈位＝傳播鄰接（騩山≈91°E 與鈐山 90°E 相鄰）＋屬性 corroborate（太華削成四方＝邛崍山系；騩山錞于西海＝納木錯）。")
ly = wrap_text(px, ly + 4, 500, 10, "#666", "借名純化：華山/渭/洛/漢/沔/嶓塚/南山/黃山/西海全部同名脫鉤——文本地理實為川西—藏東，後世以文本名命名陝西地理（因果倒置最純粹案例，不依名反證）。")
ly = wrap_text(px, ly + 4, 500, 10, "#666", "時代文明：卡若文化（昌都，5000–4000BP，窗口內）與嶓塚之山鏈位同域；三星堆不納入本經（交中山經校準）。")

S.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">19 站 → 現實候選（審核中）</text>')
ty = ly + 38
for s in stations:
    S.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {s["name"]}</tspan>　→ {short.get(s["name"], "")}</text>')
    ty += 21.2

# ---- footer ----
fy = wrap_text(60, Y(LAT0) + 40, MW - 60, 11, "#666",
    "推理說明：自錢來之山（成都平原西緣）沿川西高原—橫斷山北段西行——七溪北注渭（黃河河曲方向）；大時之山黃河—長江分水（巴顏喀拉）；嶓塚漢水源（昌都·卡若文化帶）；塗途西南折入藏東南；經黃山（鸚鵡北緣）、翠山（犛牛麝鹿）至騩山——錞于西海（納木錯候選A／色林錯候選B）。")
fy = wrap_text(60, fy + 6, MW - 60, 11, "#666",
    "腿程 3,045 里≈1,172 km（0.385；原文自記 2,957 里）。太華—騩山淨位移擬合約 94%；騩山鏈位與納木錯幾乎重合；騩山與鈐山（西次二經 v2 起點）相距約 140 km——兩經端點相鄰。所有對應為競爭假說，時代窗口 4000–1000 BCE。")

S.append('</svg>')
svg = "\n".join(S)
with open(OUT, "w") as f:
    f.write(svg)

bad = []
for m in re.finditer(r'<text x="([\d.-]+)" y="([\d.-]+)" font-size="([\d.]+)"[^>]*>([^<]+)</text>', svg):
    x, y, size, t = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
    end = x + _twidth(t, size)
    if x < 0:
        bad.append(("left-off", t[:20], int(x)))
    elif y >= 65 and x < PANEL_X - 12 and end > MX + MW - 8:
        bad.append(("past-frame", t[:20], int(end)))
    elif x >= PANEL_X - 12 and end > 1630:
        bad.append(("past-panel", t[:20], int(end)))
    if y > 888:
        bad.append(("bottom-off", t[:20], int(y)))
print("wrote", OUT, os.path.getsize(OUT), "bytes | overflow:", bad if bad else "none")
