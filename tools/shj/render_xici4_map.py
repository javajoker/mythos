#!/usr/bin/env python3
"""Render the Xici-4 adaptation map as SVG.

Data-driven from xici4-station-grid.jsonl (0.385 band). Basemap (coasts,
Atlas ranges, rivers) is simplified示意 geometry, marked on the map.
All mappings proposed_pending_review. Includes a text-overflow audit.
"""
import json, math, os, re

HERE = os.path.join(os.path.dirname(__file__), "..", "..", "projects", "shanhaijing", "data", "derived", "era", "adaptation")
GRID = os.path.join(HERE, "xici4-station-grid.jsonl")
OUT = os.path.join(HERE, "xici4-map.svg")

stations = []
for line in open(GRID):
    r = json.loads(line)
    if "meta" in r:
        continue
    g = r["grid"]["0.385"]
    stations.append({"name": r["station"], "order": r["order"], "lat": g["lat"], "lon": g["lon"]})

short = {
    "陰山": "紹拉河谷下游台地", "勞山": "紹拉河東丘陵·弱水", "罷父之山": "河間台地",
    "申山": "山前帶·區水東注河", "鳥山": "桑楮山·陰鐵陽玉", "上申之山": "礫石山·白鹿·胡兀鷲",
    "諸次之山": "密林蛇山", "號山": "藥草漆樹山", "盂山": "鐵銅礦山·白色動物群",
    "白於之山": "雪松林山·雙源分水", "申首之山": "雪峯·伏流（冬夏有雪）", "涇谷之山": "高原谷山",
    "剛山": "山精人面獸身", "剛山之尾": "山脈尾端·洛水北注", "英鞮之山": "漆木林·鳥獸盡白",
    "中曲之山": "駮＝白大羚羊（一角）", "邽山": "窮奇·濛水南注洋水",
    "鳥鼠同穴之山": "主脊集水嶺（雙向分水）", "崦嵫之山": "大西洋岸日落山（終點錨）",
}

# ---- projection: lon -11.5..2.5, lat 26.5..36 ----
LON0, LON1 = -11.5, 2.5
LAT0, LAT1 = 26.5, 36.0
MX, MY = 60, 80
MW, MH = 1000, 500
PANEL_X = MX + MW + 30

def X(lon): return MX + (lon - LON0) / (LON1 - LON0) * MW
def Y(lat): return MY + (LAT1 - lat) / (LAT1 - LAT0) * MH
def pts(seq): return " ".join(f"{X(lo):.1f},{Y(la):.1f}" for lo, la in seq)

def _twidth(t, size):
    return sum(size if ord(c) > 0x2E7F else size * 0.55 for c in t)

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

# ---- title ----
S.append('<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">《西次四經》時代假想推理 × 現代映射參照圖</text>')
S.append('<text x="60" y="56" font-size="12" fill="#666">adapt-xici4-1 ｜ 終點錨：崦嵫之山＝摩洛哥大西洋岸（未確認）｜ 里程鏈 0.385 km/里（帶 0.35–0.42，±150 km）｜ 全部映射 proposed_pending_review</text>')

# ---- Atlantic (west of Moroccan coast) ----
atl_coast = [(-6.9, 34.2), (-6.85, 34.0), (-7.6, 33.6), (-8.5, 33.2), (-9.25, 32.3),
             (-9.77, 31.5), (-9.6, 30.42), (-9.75, 30.0), (-9.9, 29.4), (-10.05, 29.0),
             (-10.5, 28.5), (-11.0, 28.0), (-11.3, 27.5)]
atl_poly = atl_coast + [(-11.5, 27.5), (-11.5, 34.2), (-6.9, 34.2)]
S.append(f'<polygon points="{pts(atl_poly)}" fill="#bcd6e8"/>')
S.append(f'<polyline points="{pts(atl_coast)}" fill="none" stroke="#7fa8c9" stroke-width="1.4"/>')
S.append(f'<text x="{X(-10.9):.0f}" y="{Y(31.5):.0f}" font-size="14" fill="#4a7596" font-style="italic">大西洋（海）</text>')

# ---- Mediterranean (north, in-range strip lon -5..2.5) ----
med_coast = [(-5.6, 35.3), (-4.5, 35.25), (-3.5, 35.15), (-2.6, 35.1), (-1.5, 34.95),
             (-0.6, 35.6), (0.3, 36.3), (1.2, 36.6), (2.5, 36.75)]
med_poly = med_coast + [(2.5, 36.0), (-5.6, 36.0)]
med_poly = [(lo, la) for lo, la in med_poly]
S.append(f'<polygon points="{pts(med_poly)}" fill="#bcd6e8"/>')
S.append(f'<polyline points="{pts(med_coast)}" fill="none" stroke="#7fa8c9" stroke-width="1.4"/>')
S.append(f'<text x="{X(0.4):.0f}" y="{Y(35.75):.0f}" font-size="12" fill="#4a7596" font-style="italic">地中海</text>')

# ---- Atlas ranges (schematic shading) ----
for name, cx, cy, rx, ry in [("高阿特拉斯", -7.0, 31.2, 2.2, 0.5), ("中阿特拉斯", -5.3, 32.6, 1.6, 0.45),
                             ("撒哈拉阿特拉斯", -0.7, 33.3, 2.2, 0.5), ("反阿特拉斯", -9.3, 29.7, 1.3, 0.4)]:
    S.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{rx/14*MW*1.0:.0f}" ry="{ry/9.5*MH:.0f}" fill="#c9b18a" opacity="0.45"/>')
    S.append(f'<text x="{X(cx)-24:.0f}" y="{Y(cy)+3:.0f}" font-size="10" fill="#7a6540">{name}</text>')

# ---- Grand Erg Occidental (sand) ----
S.append(f'<ellipse cx="{X(0.8):.0f}" cy="{Y(30.6):.0f}" rx="60" ry="70" fill="url(#sand)" opacity="0.6"/>')
S.append(f'<text x="{X(0.2):.0f}" y="{Y(30.6):.0f}" font-size="9" fill="#8a6a2f">大東爾格（西緣）</text>')

# ---- rivers (modern reference, solid) ----
rivers = [
    ("德拉河（內流）", [(-6.8, 31.3), (-6.2, 30.9), (-5.7, 30.4), (-5.3, 29.8), (-5.9, 29.2), (-7.0, 28.9), (-8.5, 28.7), (-9.9, 28.5)], True),
    ("蘇斯河（漢水→苕水→海）", [(-8.6, 31.3), (-9.0, 30.9), (-9.45, 30.6), (-9.6, 30.42)], False),
    ("坦西夫特河（洋水方向）", [(-8.5, 31.5), (-8.2, 31.6), (-8.8, 31.7), (-9.35, 31.6)], False),
    ("烏姆賴卜阿河", [(-7.2, 32.4), (-7.7, 32.8), (-8.3, 33.0), (-8.6, 33.15)], False),
    ("穆盧耶河", [(-4.6, 32.7), (-3.8, 33.4), (-3.2, 34.3), (-2.95, 35.05)], False),
    ("紹拉河（洛·內流消失於沙）", [(-1.2, 30.4), (-0.75, 29.6), (-0.5, 29.0), (-0.32, 28.3), (-0.3, 27.87)], False),
]
for name, line, dash in rivers:
    dash_attr = ' stroke-dasharray="5 4"' if dash else ''
    S.append(f'<polyline points="{pts(line)}" fill="none" stroke="#2f7fbf" stroke-width="1.6"{dash_attr}/>')
# river labels (placed to avoid chain labels)
S.append(f'<text x="{X(-7.9):.0f}" y="{Y(28.75):.0f}" font-size="9" fill="#2f7fbf">德拉河（渭→河·內流方向）</text>')
S.append(f'<text x="{X(-10.4):.0f}" y="{Y(30.1):.0f}" font-size="9" fill="#2f7fbf">蘇斯河（漢水→苕水→海）</text>')
S.append(f'<text x="{X(-9.4):.0f}" y="{Y(31.85):.0f}" font-size="9" fill="#2f7fbf">坦西夫特河（洋水）</text>')
S.append(f'<text x="{X(-1.75):.0f}" y="{Y(29.4):.0f}" font-size="9" fill="#2f7fbf">紹拉河＝洛（內流·消失於沙）</text>')

# ---- period hypothesis (dashed): 河 endorheic system, 陵羊之澤, 申水伏流 ----
S.append(f'<ellipse cx="{X(0.4):.0f}" cy="{Y(32.6):.0f}" rx="34" ry="16" fill="#d8e6c8" stroke="#7a9a5a" stroke-dasharray="4 3"/>')
S.append(f'<text x="{X(-0.35):.0f}" y="{Y(32.2):.0f}" font-size="9" fill="#5a7a3a">河＝高原鹽沼系統（濕期大湖）</text>')
S.append(f'<ellipse cx="{X(-5.45):.0f}" cy="{Y(31.75):.0f}" rx="20" ry="10" fill="#d8e6c8" stroke="#7a9a5a" stroke-dasharray="4 3"/>')
S.append(f'<text x="{X(-6.1):.0f}" y="{Y(32.05):.0f}" font-size="9" fill="#5a7a3a">陵羊之澤（山前湖沼）</text>')
# snow peak marker at 申首之山 + karst note
sx, sy = X(-2.54), Y(31.3)
S.append(f'<path d="M{sx-8},{sy-14} L{sx},{sy-26} L{sx+8},{sy-14} Z" fill="#fff" stroke="#7fa8c9"/>')

# ---- route chain ----
route = [(s["lon"], s["lat"]) for s in stations]
S.append(f'<polyline points="{pts(route)}" fill="none" stroke="#b03a2e" stroke-width="2.6" opacity="0.85"/>')
for i, s in enumerate(stations):
    x, y = X(s["lon"]), Y(s["lat"])
    anchor = (s["name"] == "崦嵫之山")
    r = 8 if anchor else 5
    S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{"#e74c3c" if anchor else "#c0392b"}" stroke="#fff" stroke-width="1.5"/>')
    S.append(f'<text x="{x-4:.0f}" y="{y+4:.0f}" font-size="9" fill="#fff" font-weight="bold">{s["order"]}</text>')
    if i <= 8:   # N-S segment: labels right of chain
        S.append(f'<text x="{x+9:.0f}" y="{y+4:.0f}" font-size="11" fill="#7b241c" font-weight="bold">{s["name"]}</text>')
    elif anchor:
        S.append(f'<text x="{x-30:.0f}" y="{y-16:.0f}" font-size="11" fill="#7b241c" font-weight="bold">{s["name"]}</text>')
    else:        # W segment: alternate above/below
        dy = -10 if i % 2 else 16
        S.append(f'<text x="{x-18:.0f}" y="{y+dy:.0f}" font-size="11" fill="#7b241c" font-weight="bold">{s["name"]}</text>')

# ---- watershed annotation at 鳥鼠同穴 ----
wx, wy = X(-8.58), Y(31.3)
S.append(f'<line x1="{wx+4:.0f}" y1="{wy-6:.0f}" x2="{wx+30:.0f}" y2="{wy-24:.0f}" stroke="#2f7fbf" stroke-width="1.6" marker-end="url(#arr)"/>')
S.append(f'<line x1="{wx-4:.0f}" y1="{wy+6:.0f}" x2="{wx-30:.0f}" y2="{wy+22:.0f}" stroke="#2f7fbf" stroke-width="1.6" marker-end="url(#arr)"/>')
S.append(f'<text x="{wx-66:.0f}" y="{wy+38:.0f}" font-size="9" fill="#2f7fbf">一山雙向分水：渭水東流／濫水西流</text>')

# ---- 西洛東河 annotation (kept clear of the chain) ----
S.append(f'<text x="{X(-4.9):.0f}" y="{Y(27.35):.0f}" font-size="10" fill="#5a7a3a">分水脊線（站1–9）：西注洛（紹拉河·內流）｜東注河（鹽沼系統）</text>')

# ---- modern reference points ----
modern = [("阿加迪爾", -9.6, 30.45), ("馬拉喀什", -7.98, 31.63), ("卡薩布蘭卡", -7.6, 33.55),
          ("阿德拉爾", -0.29, 27.87), ("貝沙爾", -2.19, 31.62), ("圖卜卡勒", -7.92, 31.06),
          ("阿亞希山", -4.9, 32.48), ("非斯", -5.0, 34.03)]
for name, lo, la in modern:
    x, y = X(lo), Y(la)
    S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
    S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

# ---- scale bar (1°lon≈95.7km @31°N; px/deg = MW/14) ----
bx, by = X(-11.2), Y(27.0)
px_per_100km = 100 / 95.7 * (MW / 14)
S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*px_per_100km:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
for k in range(5):
    S.append(f'<line x1="{bx + k*px_per_100km:.0f}" y1="{by-4:.0f}" x2="{bx + k*px_per_100km:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
    S.append(f'<text x="{bx + k*px_per_100km - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*100}</text>')
S.append(f'<text x="{bx + 4*px_per_100km + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

# ---- grid ----
for lon in range(-11, 3):
    S.append(f'<line x1="{X(lon):.0f}" y1="{Y(LAT0):.0f}" x2="{X(lon):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(lon)-10:.0f}" y="{Y(LAT0)+14:.0f}" font-size="9" fill="#999">{lon}°E</text>')
for lat in range(27, 37):
    S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(lat):.0f}" x2="{X(LON1):.0f}" y2="{Y(lat):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(lat)+3:.0f}" font-size="9" fill="#999">{lat}°N</text>')

# ---- panel ----
px = PANEL_X
S.append(f'<rect x="{px-12}" y="70" width="560" height="800" fill="#fffdf5" stroke="#cbb"/>')
S.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
legend = [
    ("#c0392b", "solid", "里程鏈（19站，紅圈數字＝站序；先北後西 L 形）"),
    ("#e74c3c", "star", "大圈＝終點錨：崦嵫之山＝大西洋岸"),
    ("#2f7fbf", "solid", "現代水體參照（河流/海）"),
    ("#2f7fbf", "dash", "德拉河＝渭→河內流方向（虛線＝間歇）"),
    ("#7a9a5a", "dash", "時代假想：河＝高原鹽沼（濕期大湖，已退）"),
    ("#7a9a5a", "dash2", "時代假想：陵羊之澤（山前湖沼）"),
    ("#c9b18a", "sq", "阿特拉斯山系（簡化示意）"),
    ("#34495e", "sq", "現代地點參照點"),
]
ly = 118
for color, style, label in legend:
    if style == "solid":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
    elif style in ("dash", "dash2"):
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2" stroke-dasharray="6 4"/>')
    elif style == "sq":
        S.append(f'<rect x="{px+8}" y="{ly-5}" width="8" height="8" fill="{color}"/>')
    elif style == "star":
        S.append(f'<circle cx="{px+13}" cy="{ly}" r="8" fill="{color}"/>')
    S.append(f'<text x="{px+34}" y="{ly+4}" font-size="11" fill="#444">{label}</text>')
    ly += 22

ly += 8
ly = wrap_text(px, ly, 500, 10, "#666", "因果倒置警示：本經水名（河/渭/涇/洛/漢/洋/湯）與中國水名同名，一律為後世借名方向，不得以中國同名水系（如甘肅渭源鳥鼠山）反證本經位置。")
ly = wrap_text(px, ly + 4, 500, 10, "#666", "弱水四見（勞山/海內西經/大荒西經/海內南經）→ 類名說：弱水＝消失/不任舟楫之水的性狀類名，待裁。")

S.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">19 站 → 現實候選（審核中）</text>')
ty = ly + 38
for s in stations:
    S.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {s["name"]}</tspan>　→ {short.get(s["name"], "")}</text>')
    ty += 21.2

# ---- footer notes (wrapped to map width) ----
fy = wrap_text(60, Y(LAT0) + 40, MW, 11, "#666",
    "推理說明：自陰山（紹拉河谷下游）正北七站跨撒哈拉阿特拉斯山前帶（西洛東河分水脊線），於白於之山轉西，經申首雪峯（冬夏有雪）、中阿特拉斯，抵高阿特拉斯主脊集水嶺（鳥鼠同穴：渭水東流、濫水西流），西南至崦嵫之山（日落山）——苕水西流注于海＝蘇斯河入大西洋。")
fy = wrap_text(60, fy + 6, MW, 11, "#666",
    "腿程合計 3,205 里≈1,234 km（0.385；原文自記 3,680 里，差異記錄待校）。淨位移擬合約 97%。所有對應為競爭假說，時代窗口 4000–1000 BCE；內流水系已衰退、白色相動物群已退出，現代無水不作否決。")

S.append('</svg>')

svg = "\n".join(S)
with open(OUT, "w") as f:
    f.write(svg)

# overflow audit
bad = []
for m in re.finditer(r'<text x="([\d.-]+)" y="[\d.-]+" font-size="([\d.]+)"[^>]*>([^<]+)</text>', svg):
    x, size, t = float(m.group(1)), float(m.group(2)), m.group(3)
    end = x + _twidth(t, size)
    limit = 1700 if x >= PANEL_X - 12 else PANEL_X - 16
    if end > limit:
        bad.append((t[:24], int(x), int(end)))
print("wrote", OUT, os.path.getsize(OUT), "bytes | overflow:", bad if bad else "none")
