#!/usr/bin/env python3
"""Render the Xici-3 adaptation map as SVG.

Geometry from data/derived/era/adaptation/xici3-station-grid.jsonl (0.385 band)
and candidate short-names decided in xici3-mappings.jsonl. Coastlines, period
water bodies and sand seas are simplified示意 geometry, marked as such on the
map. All mappings are proposed_pending_review.
"""
import json, math, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "projects", "shanhaijing", "data", "derived", "era", "adaptation")
GRID = os.path.join(ROOT, "xici3-station-grid.jsonl")
MAPJ = os.path.join(ROOT, "xici3-mappings.jsonl")
OUT = os.path.join(ROOT, "xici3-map.svg")

# ---- data ----
stations = []
for line in open(GRID):
    r = json.loads(line)
    if "meta" in r:
        continue
    g = r["grid"]["0.385"]
    stations.append({"name": r["station"], "order": r["order"], "lat": g["lat"], "lon": g["lon"]})

short = {
    "崇吾之山": "米甸—希斯馬高原",     "長沙之山": "希賈茲北部山地｜⛰希賈茲山脈·北部結晶岩山地",     "不周之山": "阿拉伯谷裂谷斷崖｜⛰阿拉伯谷東側斷層山",
    "峚山": "死海瀝青—鹽礦帶｜⛰所多瑪山",     "鍾山": "南黎凡特海岸丘陵",     "泰器之山": "北西奈海岸｜⛰北西奈海岸丘陵",
    "槐江之山": "三角洲東緣湖沼｜⛰尼羅河三角洲東緣湖沼台地",     "昆侖之丘": "吉薩金字塔群（錨）｜⛰吉薩高原",     "樂遊之山": "瓦迪奈特倫湖谷",
    "流沙": "蓋塔拉東緣沙沼",     "蠃母之山": "蓋塔拉西緣台地｜⛰蓋塔拉窪地西緣台地",     "玉山": "錫瓦綠洲（西王母）｜⛰錫瓦綠洲台地",
    "軒轅之丘": "大沙海北緣丘台",     "積石之山": "卡蘭西奧古河道·石門｜⛰卡蘭西奧—薩里爾古河道區台地",     "長留之山": "蜃景台地（反景）｜⛰利比亞沙漠中部台地",
    "章莪之山": "錫爾特東緣裸岩｜⛰錫爾特盆地東緣裸岩帶",     "陰山": "古湖盆北緣·文貝｜⛰利比亞古湖盆北緣",     "符愓之山": "綠洲致雨山｜⛰昔蘭尼加南緣綠洲山地",
    "三危之山": "哈魯傑火山原",     "騩山": "鳴沙帶·耆童｜⛰利比亞沙海鳴沙帶",     "天山": "綠洲·湯谷溫泉｜⛰錫爾特盆地南緣綠洲山地",
    "泑山": "蘇爾特灣日落山·蓐收｜⛰蘇爾特灣南岸山地",     "翼望之山": "蘇爾特灣西南岸（終點）｜⛰蘇爾特灣西南岸山地",
}

# ---- projection ----
LON0, LON1 = 11.0, 42.0
LAT0, LAT1 = 25.0, 33.2
MX, MY = 70, 90
MW, MH = 980, 560  # map pixel size
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

def wrap_text(x, y, max_w, size, color, text, lh=None):
    """CJK-aware character wrapping; returns next y after the block."""
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

S = []
S.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="880" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">')
S.append(f'<rect x="0" y="0" width="1600" height="880" fill="#f7f3e8"/>')

# ---- title ----
S.append('<text x="70" y="34" font-size="21" font-weight="bold" fill="#333">《西次三經》時代假想推理 × 現代映射參照圖</text>')
S.append('<text x="70" y="56" font-size="12" fill="#666">adapt-xici3-1 ｜ 錨點：昆侖之丘＝吉薩（ANC-01，未確認）｜ 里程鏈 0.385 km/里（帶 0.35–0.42，±150 km）｜ 全部映射 proposed_pending_review</text>')

# ---- sea: Mediterranean (polygon: coast polyline + map top/side edges) ----
med_coast = [
    (42.0, 31.15), (40.5, 31.1), (39.5, 31.15), (38.5, 31.05), (37.5, 31.0),  # N Saudi inland edge (not sea; placeholder replaced below)
]
# Real coast path: east edge down the Levant, then west along Sinai/Egypt/Libya
coast = [
    (35.6, 33.2), (35.4, 32.8), (35.0, 32.4), (34.75, 31.9), (34.45, 31.5), (34.3, 31.3),
    (34.25, 31.15), (34.0, 31.1), (33.5, 31.1), (33.0, 31.2), (32.5, 31.25), (32.3, 31.4),
    (31.9, 31.55), (31.4, 31.6), (30.9, 31.5), (30.3, 31.4), (29.9, 31.25), (28.9, 31.05),
    (28.0, 31.1), (27.2, 31.35), (26.0, 31.6), (24.8, 31.95), (23.2, 32.3), (22.0, 32.7),
    (20.9, 32.3), (20.05, 32.1), (19.7, 31.3), (19.2, 30.55), (18.5, 30.25), (17.5, 30.3),
    (16.6, 30.9), (16.1, 31.4), (15.4, 32.2), (14.9, 32.5), (13.8, 32.9), (13.2, 33.2),
]
med_poly = coast + [(11.0, 33.2), (35.6, 33.2)]
S.append(f'<polygon points="{pts(med_poly)}" fill="#bcd6e8" stroke="none"/>')
S.append(f'<polyline points="{pts(coast)}" fill="none" stroke="#7fa8c9" stroke-width="1.4"/>')
S.append(f'<text x="{X(24.5):.0f}" y="{Y(32.6):.0f}" font-size="14" fill="#4a7596" font-style="italic">地中海（西海）</text>')

# ---- Red Sea / Gulfs (simplified) ----
suez = [(32.3, 30.0), (32.45, 29.6), (32.55, 29.1), (32.75, 28.5), (33.0, 28.0), (33.4, 27.75),
        (34.3, 27.7), (34.5, 27.2), (34.9, 26.6), (35.3, 26.0), (35.6, 25.0), (37.4, 25.0),
        (38.0, 25.8), (37.6, 26.4), (36.9, 27.0), (36.2, 27.6), (35.0, 27.9), (34.0, 28.1),
        (33.6, 28.4), (33.2, 28.9), (32.95, 29.4), (32.75, 29.9)]
S.append(f'<polygon points="{pts(suez)}" fill="#bcd6e8" stroke="#7fa8c9" stroke-width="1.2"/>')
S.append(f'<text x="{X(36.6):.0f}" y="{Y(26.0):.0f}" font-size="13" fill="#4a7596" font-style="italic">紅海（赤水／東海）</text>')
S.append(f'<text x="{X(32.0):.0f}" y="{Y(28.6):.0f}" font-size="10" fill="#4a7596">蘇伊士灣</text>')
aqaba = [(34.55, 29.5), (34.95, 29.3), (34.95, 28.7), (34.7, 28.05), (34.5, 28.1), (34.45, 28.7), (34.35, 29.3)]
S.append(f'<polygon points="{pts(aqaba)}" fill="#bcd6e8" stroke="#7fa8c9" stroke-width="1"/>')
S.append(f'<text x="{X(34.75):.0f}" y="{Y(28.5):.0f}" font-size="9" fill="#4a7596">亞喀巴灣</text>')

# ---- Dead Sea ----
S.append(f'<ellipse cx="{X(35.5):.0f}" cy="{Y(31.3):.0f}" rx="6" ry="16" fill="#9dc2dd" stroke="#7fa8c9"/>')
S.append(f'<text x="{X(34.85):.0f}" y="{Y(30.72):.0f}" font-size="9" fill="#4a7596">死海（峚山·玉膏瀝青）</text>')

# ---- Nile (modern reference, solid) ----
nile = [(32.7, 25.0), (32.65, 25.7), (32.3, 26.1), (31.6, 26.9), (31.4, 27.2), (31.2, 27.7),
        (30.95, 28.2), (30.9, 28.7), (31.1, 29.2), (31.15, 29.7), (31.13, 30.0)]
S.append(f'<polyline points="{pts(nile)}" fill="none" stroke="#2f7fbf" stroke-width="2.2"/>')
# delta branches
S.append(f'<polyline points="{pts([(31.13,30.0),(31.0,30.5),(30.4,31.35)])}" fill="none" stroke="#2f7fbf" stroke-width="1.4"/>')
S.append(f'<polyline points="{pts([(31.13,30.0),(31.5,30.6),(31.5,31.5)])}" fill="none" stroke="#2f7fbf" stroke-width="1.4"/>')
S.append(f'<text x="{X(31.7):.0f}" y="{Y(27.6):.0f}" font-size="11" fill="#2f7fbf">尼羅河（河水→無逹·南方未至之地）</text>')

# ---- Faiyum ----
S.append(f'<ellipse cx="{X(30.62):.0f}" cy="{Y(29.42):.0f}" rx="12" ry="8" fill="#9dc2dd" stroke="#5b97c4" stroke-dasharray="4 2"/>')
S.append(f'<text x="{X(30.3):.0f}" y="{Y(29.1):.0f}" font-size="10" fill="#2f6d9e">法雍湖（醜塗之水）</text>')

# ---- Qattara (大杅) ----
qx, qy = X(27.7), Y(29.5)
S.append(f'<ellipse cx="{qx:.0f}" cy="{qy:.0f}" rx="34" ry="15" fill="#e3d7b5" stroke="#b09050" stroke-width="1.4" stroke-dasharray="6 3"/>')
S.append(f'<text x="{qx-52:.0f}" y="{qy+4:.0f}" font-size="11" fill="#8a6a2f">蓋塔拉窪地（大杅）</text>')

# ---- sand seas (hatched light) ----
S.append('<defs><pattern id="sand" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#efe3c0"/><circle cx="2" cy="2" r="0.8" fill="#d6b96a"/><circle cx="6" cy="6" r="0.8" fill="#d6b96a"/></pattern></defs>')
S.append(f'<polygon points="{pts([(25.2,29.6),(27.8,29.6),(27.8,25.0),(25.2,25.0)])}" fill="url(#sand)" opacity="0.75"/>')
S.append(f'<text x="{X(25.9):.0f}" y="{Y(28.4):.0f}" font-size="11" fill="#8a6a2f">大沙海</text>')
S.append(f'<polygon points="{pts([(20.5,30.3),(24.2,30.3),(24.2,28.6),(20.5,28.6)])}" fill="url(#sand)" opacity="0.55"/>')
S.append(f'<text x="{X(21.3):.0f}" y="{Y(29.5):.0f}" font-size="10" fill="#8a6a2f">卡蘭西奧沙海</text>')
S.append(f'<ellipse cx="{X(33.9):.0f}" cy="{Y(30.75):.0f}" rx="26" ry="10" fill="url(#sand)" opacity="0.6"/>')
S.append(f'<text x="{X(33.5):.0f}" y="{Y(30.45):.0f}" font-size="9" fill="#8a6a2f">北西奈沙丘（流沙）</text>')

# ---- Haruj volcanic field ----
S.append(f'<ellipse cx="{X(17.5):.0f}" cy="{Y(27.25):.0f}" rx="40" ry="18" fill="#6b5f52" opacity="0.5"/>')
S.append(f'<text x="{X(16.3):.0f}" y="{Y(27.25):.0f}" font-size="10" fill="#3d352c">哈魯傑火山原（三危之山候選）</text>')

# ---- Wadi Sirhan + 泑澤 paleolake ----
S.append(f'<polyline points="{pts([(36.8,31.8),(37.4,30.8),(38.0,30.0),(38.7,29.3)])}" fill="none" stroke="#c47f2a" stroke-width="2" stroke-dasharray="7 4"/>')
S.append(f'<ellipse cx="{X(37.55):.0f}" cy="{Y(29.35):.0f}" rx="14" ry="8" fill="#d8e6c8" stroke="#7a9a5a" stroke-dasharray="4 3"/>')
S.append(f'<text x="{X(37.0):.0f}" y="{Y(29.1):.0f}" font-size="10" fill="#5a7a3a">泑澤（西爾罕古湖·河水所潛）</text>')

# ---- period paleorivers (假想推理, dashed orange) ----
heishui = [(31.13, 29.98), (30.5, 29.85), (30.0, 29.75), (29.2, 29.65), (28.3, 29.55),
           (27.3, 29.5), (26.2, 29.4), (25.0, 29.35), (24.0, 29.4), (23.0, 29.5), (21.8, 29.5)]
S.append(f'<polyline points="{pts(heishui)}" fill="none" stroke="#c0392b" stroke-width="2.2" stroke-dasharray="8 5"/>')
S.append(f'<text x="{X(26.2):.0f}" y="{Y(29.15):.0f}" font-size="11" fill="#c0392b">黑水（西向古河道·濕期→消亡）</text>')
# 洵水 tributary
S.append(f'<polyline points="{pts([(23.95,29.98),(23.98,29.7),(24.0,29.42)])}" fill="none" stroke="#c0392b" stroke-width="1.6" stroke-dasharray="5 4"/>')
S.append(f'<text x="{X(24.35):.0f}" y="{Y(29.75):.0f}" font-size="9" fill="#c0392b">洵水南注黑水</text>')
# 河水冒以西流 from 積石
S.append(f'<polyline points="{pts([(22.75,29.98),(21.8,29.7),(20.8,29.5)])}" fill="none" stroke="#2f7fbf" stroke-width="1.8" stroke-dasharray="3 4"/>')
S.append(f'<text x="{X(20.7):.0f}" y="{Y(29.28):.0f}" font-size="9" fill="#2f7fbf">河水冒以西流（石門復湧）</text>')
# 水行湖鏈 (樂遊→流沙→蠃母)
S.append(f'<polyline points="{pts([(29.66,29.98),(28.9,29.9),(28.06,29.98),(27.7,29.92),(27.26,29.98)])}" fill="none" stroke="#2f9e8f" stroke-width="3" stroke-dasharray="2 5" stroke-linecap="round"/>')
S.append(f'<text x="{X(28.35):.0f}" y="{Y(30.25):.0f}" font-size="9" fill="#1f7a6e">濕期湖鏈（「水行四百里」）</text>')
# 蕃澤 / 湯谷
S.append(f'<ellipse cx="{X(19.55):.0f}" cy="{Y(29.35):.0f}" rx="13" ry="7" fill="#d8e6c8" stroke="#7a9a5a" stroke-dasharray="4 3"/>')
S.append(f'<text x="{X(19.1):.0f}" y="{Y(29.1):.0f}" font-size="9" fill="#5a7a3a">蕃澤（古湖·文貝）</text>')
S.append(f'<circle cx="{X(15.65):.0f}" cy="{Y(29.6):.0f}" r="5" fill="#e8a0a0" stroke="#c05050"/>')
S.append(f'<text x="{X(15.15):.0f}" y="{Y(29.3):.0f}" font-size="9" fill="#a04040">湯谷（溫泉）</text>')
# 大澤 (瑪麗尤特)
S.append(f'<ellipse cx="{X(30.0):.0f}" cy="{Y(31.0):.0f}" rx="14" ry="7" fill="#9dc2dd" stroke="#5b97c4" stroke-dasharray="4 2"/>')
S.append(f'<text x="{X(29.6):.0f}" y="{Y(30.8):.0f}" font-size="9" fill="#2f6d9e">大澤（后稷所潛）</text>')

# ---- Giza anchor: four waters + 弱水 ring ----
gx, gy = X(31.134), Y(29.979)
S.append(f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="17" fill="none" stroke="#8e44ad" stroke-width="1.6" stroke-dasharray="4 3"/>')
S.append(f'<text x="{gx-166:.0f}" y="{gy-24:.0f}" font-size="9" fill="#8e44ad">弱水環之（運河→沼澤化）</text>')
def arrow(x1, y1, x2, y2, color, w=2.0, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    S.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"{d} marker-end="url(#arr)"/>')
S.append('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#555"/></marker></defs>')
arrow(gx + 14, gy + 8, X(32.0), Y(29.3), "#2f7fbf")     # 赤水 toward Red Sea
S.append(f'<text x="{X(32.5):.0f}" y="{Y(28.8):.0f}" font-size="10" fill="#2f7fbf">赤水→紅海→氾天之水</text>')
arrow(gx - 8, gy + 10, X(30.65), Y(29.5), "#2f9e8f")    # 洋水 to Faiyum
S.append(f'<text x="{X(29.85):.0f}" y="{Y(29.5):.0f}" font-size="9" fill="#1f7a6e">洋水→醜塗之水</text>')
arrow(gx - 14, gy + 2, X(29.3), Y(29.6), "#c0392b", dash="6 4")  # 黑水 west
arrow(gx + 2, gy + 14, X(31.2), Y(29.2), "#2f7fbf")     # 河水 south
S.append(f'<text x="{X(31.55):.0f}" y="{Y(29.1):.0f}" font-size="9" fill="#2f7fbf">河水南流→無逹</text>')

# ---- route chain ----
route = [(s["lon"], s["lat"]) for s in stations]
S.append(f'<polyline points="{pts(route)}" fill="none" stroke="#b03a2e" stroke-width="2.6" opacity="0.85"/>')
for i, s in enumerate(stations):
    x, y = X(s["lon"]), Y(s["lat"])
    anchor = (s["name"] == "昆侖之丘")
    r = 8 if anchor else 5
    fill = "#e74c3c" if anchor else "#c0392b"
    S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="#fff" stroke-width="1.5"/>')
    S.append(f'<text x="{x-4:.0f}" y="{y+4:.0f}" font-size="9" fill="#fff" font-weight="bold">{s["order"]}</text>')
    # station name labels, staggered
    dy = -12 if i % 2 == 0 else 16
    if anchor:
        dy = -30
    S.append(f'<text x="{x-16:.0f}" y="{y+dy:.0f}" font-size="11" fill="#7b241c" font-weight="bold">{s["name"]}</text>')

# ---- modern reference points ----
modern = [("開羅/吉薩", 31.13, 30.04), ("錫瓦", 25.52, 29.2), ("耶路撒冷", 35.22, 31.77),
          ("亞喀巴", 35.0, 29.52), ("蘇爾特", 16.6, 31.2), ("阿茲拉克", 36.83, 31.83),
          ("米蘇拉塔", 15.1, 32.35)]
for name, lo, la in modern:
    x, y = X(lo), Y(la)
    S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
    S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

# ---- scale bar ----
bx, by = X(11.5), Y(25.5)
S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*31.6:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
for k in range(5):
    S.append(f'<line x1="{bx + k*31.6:.0f}" y1="{by-4:.0f}" x2="{bx + k*31.6:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
    S.append(f'<text x="{bx + k*31.6 - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*100}</text>')
S.append(f'<text x="{bx+130:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">km（1°lon≈96.5km @30°N；100里≈38.5km @0.385）</text>')

# ---- grid frame ----
for lon in range(12, 43, 4):
    S.append(f'<line x1="{X(lon):.0f}" y1="{Y(LAT0):.0f}" x2="{X(lon):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(lon)-8:.0f}" y="{Y(LAT0)+14:.0f}" font-size="9" fill="#999">{lon}°E</text>')
for lat in range(26, 34):
    S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(lat):.0f}" x2="{X(LON1):.0f}" y2="{Y(lat):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(lat)+3:.0f}" font-size="9" fill="#999">{lat}°N</text>')

# ---- frame border + right panel: legend + station table ----
S.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="none" stroke="#b8ad92" stroke-width="1.4"/>')
px = PANEL_X
S.append(f'<rect x="{px-12}" y="70" width="520" height="800" fill="#fffdf5" stroke="#cbb"/>')
S.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
legend = [
    ("#c0392b", "solid", "里程鏈（23站，紅圈數字＝站序）"),
    ("#e74c3c", "star", "大圈＝錨點：昆侖之丘＝吉薩"),
    ("#2f7fbf", "solid", "現代水體參照（尼羅河/死海/海灣）"),
    ("#c0392b", "dash", "時代假想：黑水西向古河道（消亡）"),
    ("#2f9e8f", "dot", "時代假想：濕期湖鏈（「水行」）"),
    ("#8e44ad", "dash", "時代假想：弱水環狀港池運河（沼澤化）"),
    ("#7a9a5a", "dash", "時代假想：古湖沼（泑澤/蕃澤，已涸）"),
    ("#b09050", "dash", "蓋塔拉窪地（大杅）/沙丘帶（流沙）"),
    ("#34495e", "sq", "現代地點參照點"),
]
ly = 118
for color, style, label in legend:
    if style == "solid":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
    elif style == "dash":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2" stroke-dasharray="6 4"/>')
    elif style == "dot":
        S.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="3" stroke-dasharray="2 5" stroke-linecap="round"/>')
    elif style == "sq":
        S.append(f'<rect x="{px+8}" y="{ly-5}" width="8" height="8" fill="{color}"/>')
    elif style == "star":
        S.append(f'<circle cx="{px+13}" cy="{ly}" r="8" fill="{color}"/>')
    S.append(f'<text x="{px+34}" y="{ly+4}" font-size="11" fill="#444">{label}</text>')
    ly += 22

S.append(f'<text x="{px}" y="{ly+14}" font-size="14" font-weight="bold" fill="#333">23 站 → 現實候選（審核中）</text>')
ty = ly + 40
for s in stations:
    name, cand = s["name"], short.get(s["name"], "")
    S.append(f'<text x="{px}" y="{ty}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {name}</tspan>　→ {cand}</text>')
    ty += 21.2

# ---- footer notes ----
fy = wrap_text(70, Y(25.0) + 40, MW - 60, 11, "#666",
    "推理說明：自崇吾（米甸）向西北至死海（峚山·玉膏瀝青），轉西跨西奈（泰器·文鰩魚雙海）、三角洲東緣（槐江·南望昆侖其光熊熊），西南至吉薩（昆侖之丘）；自吉薩正西：奈特倫（樂遊）→蓋塔拉（流沙·水行）→錫瓦（玉山·西王母）→沙海古河道（軒轅之丘·積石·黑水）→利比亞綠洲帶（陰山文貝·符愓致雨·三危火山原）→蘇爾特灣（泑山日落·翼望終點）。")
fy = wrap_text(70, fy + 6, MW - 60, 11, "#666",
    "全鏈 6,640 里≈2,556 km（0.385）；吉薩→錫瓦 1,320 里，0.42 端＝554 km vs 實測 541 km。所有對應為競爭假說，時代窗口 4000–1000 BCE；虛線水體可能已改道、消亡、沼澤化，現代無水不作否決。")

S.append('</svg>')

with open(OUT, "w") as f:
    f.write("\n".join(S))

import re as _re
svg = "\n".join(S)
bad = []
for m in _re.finditer(r'<text x="([\d.-]+)" y="([\d.-]+)" font-size="([\d.]+)"[^>]*>([^<]+)</text>', svg):
    x, y, size, t = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
    end = x + _twidth(t, size)
    if x < 0:
        bad.append(("left-off", t[:20], int(x)))
    elif y >= 85 and x < PANEL_X - 12 and end > MX + MW - 8:
        bad.append(("past-frame", t[:20], int(end)))
    elif x >= PANEL_X - 12 and end > 1580:
        bad.append(("past-panel", t[:20], int(end)))
    if y > 888:
        bad.append(("bottom-off", t[:20], int(y)))
print("wrote", OUT, os.path.getsize(OUT), "bytes | overflow:", bad if bad else "none")
