#!/usr/bin/env python3
"""Render the Xici-1 adaptation map as SVG.

Data-driven from xici1-station-grid.jsonl (0.385 band). Basemap (Yellow
River bend, Wei/Han rivers, Qinling, plateau lakes) is simplified示意
geometry. All mappings proposed_pending_review. Built-in overflow audit.
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
    "錢來之山": "豫西—潼關丘陵", "松果之山": "潼關西·濩水注渭", "太華之山": "華山（削成四方·錨）",
    "小華之山": "少華山方向·紅腹錦雞", "符禺之山": "秦嶺北麓·陽銅陰鐵", "石脆之山": "流赭（赭石獸醫）",
    "英山": "箭竹帶·䰷魚", "竹山": "雙源·人魚＝大鯢·毫彘＝豪豬", "浮山": "薰草（香草民俗）",
    "羭次之山": "神山·金絲猴候選", "時山": "裸山·水玉", "南山": "猛豹＝熊貓候選·丹砂",
    "大時之山": "主脊分水（北渭南漢）", "嶓塚之山": "漢水源·犀兕熊羆·白翰赤鷩", "天帝之山": "杜衡藥草",
    "塗途之山": "西南折點·桂木·礜石毒鼠", "黃山": "鸚鵡（人舌能言）·西注赤水", "翠山": "犛牛＋麝鹿",
    "騩山": "巴顏喀拉·錞于西海（終點）",
}

# ---- projection: lon 94..112, lat 30.5..37 ----
LON0, LON1 = 94.0, 112.0
LAT0, LAT1 = 30.5, 37.0
MX, MY = 60, 80
MW, MH = 1000, 470
PANEL_X = MX + MW + 30

def X(lon): return MX + (lon - LON0) / (LON1 - LON0) * MW
def Y(lat): return MY + (LAT1 - lat) / (LAT1 - LAT0) * MH
def pts(seq): return " ".join(f"{X(lo):.1f},{Y(la):.1f}" for lo, la in seq)
def _twidth(t, size): return sum(size if ord(c) > 0x2E7F else size * 0.55 for c in t)

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
S.append('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#555"/></marker>'
         '<pattern id="sand" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#efe3c0"/><circle cx="2" cy="2" r="0.8" fill="#d6b96a"/><circle cx="6" cy="6" r="0.8" fill="#d6b96a"/></pattern></defs>')

S.append('<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">《西山經之首》時代假想推理 × 現代映射參照圖</text>')
S.append('<text x="60" y="56" font-size="12" fill="#666">adapt-xici1-1 ｜ 屬性錨：太華之山＝華山（削成四方；不依同名）｜ 里程鏈 0.385 km/里（±150 km）｜ 全部映射 proposed_pending_review</text>')

# ---- terrain shading ----
S.append(f'<ellipse cx="{X(107.0):.0f}" cy="{Y(34.1):.0f}" rx="160" ry="26" fill="#c9b18a" opacity="0.45"/>')
S.append(f'<text x="{X(106.3):.0f}" y="{Y(33.9):.0f}" font-size="11" fill="#7a6540">秦嶺主脊（簡化示意）</text>')
S.append(f'<ellipse cx="{X(99.0):.0f}" cy="{Y(33.8):.0f}" rx="90" ry="22" fill="#c9b18a" opacity="0.4"/>')
S.append(f'<text x="{X(98.35):.0f}" y="{Y(33.55):.0f}" font-size="10" fill="#7a6540">巴顏喀拉山</text>')
S.append(f'<ellipse cx="{X(103.3):.0f}" cy="{Y(32.3):.0f}" rx="55" ry="30" fill="#c9b18a" opacity="0.35"/>')
S.append(f'<text x="{X(102.8):.0f}" y="{Y(32.3):.0f}" font-size="10" fill="#7a6540">岷山</text>')
S.append(f'<rect x="{X(94):.0f}" y="{Y(34.6):.0f}" width="{X(101.5)-X(94):.0f}" height="{Y(31.0)-Y(34.6):.0f}" fill="#e2d9c8" opacity="0.5"/>')
S.append(f'<text x="{X(94.4):.0f}" y="{Y(31.5):.0f}" font-size="11" fill="#8a7d5f">川西高原—青藏高原東緣</text>')
S.append(f'<rect x="{X(105.5):.0f}" y="{Y(35.3):.0f}" width="{X(110.6)-X(105.5):.0f}" height="{Y(34.5)-Y(35.3):.0f}" fill="#dce8cf" opacity="0.8"/>')
S.append(f'<text x="{X(106.0):.0f}" y="{Y(35.05):.0f}" font-size="11" fill="#5a7a3a">關中平原（渭河谷）</text>')

# ---- Qinghai Lake + source lakes ----
S.append(f'<ellipse cx="{X(100.4):.0f}" cy="{Y(36.9):.0f}" rx="34" ry="14" fill="#9dc2dd" stroke="#7fa8c9"/>')
S.append(f'<text x="{X(100.0):.0f}" y="{Y(36.62):.0f}" font-size="9" fill="#2f6d9e">青海湖（西海候選B·借名警示）</text>')
S.append(f'<ellipse cx="{X(97.5):.0f}" cy="{Y(34.95):.0f}" rx="18" ry="8" fill="#9dc2dd" stroke="#5b97c4" stroke-dasharray="4 3"/>')
S.append(f'<ellipse cx="{X(98.3):.0f}" cy="{Y(34.8):.0f}" rx="14" ry="7" fill="#9dc2dd" stroke="#5b97c4" stroke-dasharray="4 3"/>')
S.append(f'<text x="{X(96.4):.0f}" y="{Y(34.5):.0f}" font-size="9" fill="#2f6d9e">扎陵湖—鄂陵湖（西海候選A·黃河源湖區）</text>')

# ---- rivers (modern reference) ----
yellow = [(97.6,34.95),(99.0,35.2),(100.5,35.6),(101.8,35.9),(103.0,36.0),(103.8,36.1),(104.6,36.4)]
S.append(f'<polyline points="{pts(yellow)}" fill="none" stroke="#c89a2e" stroke-width="2.4"/>')
jinshan = [(110.9,37.0),(110.8,36.3),(110.6,35.6),(110.5,35.0),(110.55,34.65),(111.0,34.75),(111.6,34.85)]
S.append(f'<polyline points="{pts(jinshan)}" fill="none" stroke="#c89a2e" stroke-width="2.4"/>')
S.append(f'<text x="{X(101.0):.0f}" y="{Y(36.25):.0f}" font-size="10" fill="#a07d1e">黃河（河曲段）</text>')
S.append(f'<text x="{X(110.75):.0f}" y="{Y(35.8):.0f}" font-size="9" fill="#a07d1e">黃河（晉陝峽谷段）</text>')
wei = [(104.2,34.75),(105.5,34.7),(106.8,34.55),(108.0,34.5),(109.2,34.45),(110.2,34.5),(110.55,34.62)]
S.append(f'<polyline points="{pts(wei)}" fill="none" stroke="#2f7fbf" stroke-width="2.2"/>')
S.append(f'<text x="{X(106.6):.0f}" y="{Y(34.75):.0f}" font-size="10" fill="#2f7fbf">渭河（渭——北麓七溪北注）</text>')
han = [(104.4,33.7),(105.6,33.3),(106.8,33.0),(107.9,32.8),(109.0,32.6),(110.3,32.4)]
S.append(f'<polyline points="{pts(han)}" fill="none" stroke="#2f7fbf" stroke-width="2.2"/>')
S.append(f'<text x="{X(106.5):.0f}" y="{Y(32.75):.0f}" font-size="10" fill="#2f7fbf">漢江（漢水—沔）</text>')
luo = [(109.9,35.6),(110.1,35.1),(110.3,34.8),(110.55,34.66)]
S.append(f'<polyline points="{pts(luo)}" fill="none" stroke="#2f7fbf" stroke-width="1.6"/>')
S.append(f'<text x="{X(110.05):.0f}" y="{Y(35.3):.0f}" font-size="9" fill="#2f7fbf">洛河</text>')
jialing = [(105.8,33.9),(105.6,33.2),(105.5,32.5),(105.9,31.6),(106.3,31.0)]
S.append(f'<polyline points="{pts(jialing)}" fill="none" stroke="#2f7fbf" stroke-width="1.4"/>')
S.append(f'<text x="{X(105.1):.0f}" y="{Y(32.6):.0f}" font-size="9" fill="#2f7fbf">嘉陵江</text>')
min = [(103.8,33.3),(103.6,32.5),(103.6,31.7),(103.9,31.0)]
S.append(f'<polyline points="{pts(min)}" fill="none" stroke="#2f7fbf" stroke-width="1.4"/>')
S.append(f'<text x="{X(103.15):.0f}" y="{Y(31.9):.0f}" font-size="9" fill="#2f7fbf">岷江</text>')
# period hypothesis: 赤水 (dashed red, W Sichuan)
S.append(f'<polyline points="{pts([(100.3,33.4),(99.9,33.2),(99.5,33.0),(99.2,32.8)])}" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="7 4"/>')
S.append(f'<text x="{X(99.0):.0f}" y="{Y(32.55):.0f}" font-size="9" fill="#c0392b">赤水（川西·同名異水待裁）</text>')

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
    dx = -22 if anchor else -18
    if anchor:
        dy = -20
    S.append(f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" font-size="10" fill="#7b241c" font-weight="bold">{s["name"]}</text>')

# ---- modern reference points ----
modern = [("西安", 108.94, 34.27), ("華山", 110.09, 34.5), ("寶雞", 107.24, 34.36), ("漢中", 107.02, 33.07),
          ("蘭州", 103.83, 36.06), ("西寧", 101.77, 36.62), ("成都", 104.07, 30.65)]
for name, lo, la in modern:
    x, y = X(lo), Y(la)
    S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
    S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

# ---- scale bar (1°lon≈92km @34.5°N; px/deg = MW/18) ----
bx, by = X(94.4), Y(31.0)
px100 = 100 / 92.0 * (MW / 18)
S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*px100:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
for k in range(5):
    S.append(f'<line x1="{bx + k*px100:.0f}" y1="{by-4:.0f}" x2="{bx + k*px100:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
    S.append(f'<text x="{bx + k*px100 - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*100}</text>')
S.append(f'<text x="{bx + 4*px100 + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

# ---- grid ----
for lon in range(96, 112, 4):
    S.append(f'<line x1="{X(lon):.0f}" y1="{Y(LAT0):.0f}" x2="{X(lon):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(lon)-8:.0f}" y="{Y(LAT0)+14:.0f}" font-size="9" fill="#999">{lon}°E</text>')
for lat in range(31, 37):
    S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(lat):.0f}" x2="{X(LON1):.0f}" y2="{Y(lat):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(lat)+3:.0f}" font-size="9" fill="#999">{lat}°N</text>')

# ---- panel ----
px = PANEL_X
S.append(f'<rect x="{px-12}" y="70" width="560" height="800" fill="#fffdf5" stroke="#cbb"/>')
S.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
legend = [
    ("#c0392b", "solid", "里程鏈（19站，紅圈數字＝站序；幾乎純西向）"),
    ("#e74c3c", "star", "大圈＝屬性錨：太華之山＝華山"),
    ("#2f7fbf", "solid", "現代水體參照（渭/漢/洛/嘉陵/岷江）"),
    ("#c89a2e", "solid", "黃河（現代參照）"),
    ("#5b97c4", "dash", "西海候選A：黃河源湖區（扎陵—鄂陵）"),
    ("#c0392b", "dash", "時代假想：赤水（川西·同名待裁）"),
    ("#c9b18a", "sq", "秦嶺/巴顏喀拉/岷山（簡化示意）"),
    ("#34495e", "sq", "現代地點參照點"),
]
ly = 118
for color, style, label in legend:
    if style == "solid":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
    elif style == "dash":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2" stroke-dasharray="6 4"/>')
    elif style == "sq":
        S.append(f'<rect x="{px+8}" y="{ly-5}" width="8" height="8" fill="{color}"/>')
    elif style == "star":
        S.append(f'<circle cx="{px+13}" cy="{ly}" r="8" fill="{color}"/>')
    S.append(f'<text x="{px+34}" y="{ly+4}" font-size="11" fill="#444">{label}</text>')
    ly += 22

ly += 8
ly = wrap_text(px, ly, 500, 10, "#666", "借名警示：本經為後世中國地理命名的最大借名輸出端（太華/渭/洛/漢/沔/嶓塚/南山/黃山/西海）——後世借名方向，不得以同名反證；映射僅依屬性＋里程。")
ly = wrap_text(px, ly + 4, 500, 10, "#666", "生態鏈證據：箭竹（7/8/17/18站）→猛豹/熊羆＝熊貓候選（12/14站）→旄牛麝鹿（18站高原動物群）→騩山臨西海——自關中向高原的生態梯度。")
ly = wrap_text(px, ly + 4, 500, 10, "#666", "三星堆（成都平原31°N）不在本經鏈條上（全程≥33.5°N）——建議留待中山經適配校準（F-0006）。")

S.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">19 站 → 現實候選（審核中）</text>')
ty = ly + 38
for s in stations:
    S.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {s["name"]}</tspan>　→ {short.get(s["name"], "")}</text>')
    ty += 21.2

# ---- footer ----
fy = wrap_text(60, Y(LAT0) + 40, MW, 11, "#666",
    "推理說明：自錢來之山（潼關方向）沿秦嶺北麓西行——北麓七溪北注渭；竹山雙源（北渭/東南洛）；大時之山主脊分水（北渭南漢）；嶓塚漢水源；塗途之山西南折入川西高原（水系轉西南）；經黃山（鸚鵡）、翠山（犛牛麝鹿）至騩山——錞于西海（黃河源湖區候選A／青海湖候選B）。")
fy = wrap_text(60, fy + 6, MW, 11, "#666",
    "腿程 3,045 里≈1,172 km（0.385；原文自記 2,957 里，+3.0%）。太華—騩山淨位移擬合約 95%。所有對應為競爭假說，時代窗口 4000–1000 BCE；犀牛溫暖期北界、竹林北界、大鯢均為後期退出記錄。")

S.append('</svg>')
svg = "\n".join(S)
with open(OUT, "w") as f:
    f.write(svg)

bad = []
for m in re.finditer(r'<text x="([\d.-]+)" y="[\d.-]+" font-size="([\d.]+)"[^>]*>([^<]+)</text>', svg):
    x, size, t = float(m.group(1)), float(m.group(2)), m.group(3)
    end = x + _twidth(t, size)
    limit = 1700 if x >= PANEL_X - 12 else PANEL_X - 16
    if end > limit:
        bad.append((t[:24], int(x), int(end)))
print("wrote", OUT, os.path.getsize(OUT), "bytes | overflow:", bad if bad else "none")
