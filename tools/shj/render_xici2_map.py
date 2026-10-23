#!/usr/bin/env python3
"""Render the Xici-2 adaptation map as SVG.

Data-driven from xici2-station-grid.jsonl (0.385 band). Basemap (Himalaya
crest, rivers, plains) is simplified示意 geometry, marked on the map.
All mappings proposed_pending_review. Includes a text-overflow audit.
"""
import json, math, os, re

HERE = os.path.join(os.path.dirname(__file__), "..", "..", "projects", "shanhaijing", "data", "derived", "era", "adaptation")
GRID = os.path.join(HERE, "xici2-station-grid.jsonl")
OUT = os.path.join(HERE, "xici2-map.svg")

stations = []
for line in open(GRID):
    r = json.loads(line)
    if "meta" in r:
        continue
    g = r["grid"]["0.385"]
    stations.append({"name": r["station"], "order": r["order"], "lat": g["lat"], "lon": g["lon"]})

short = {
    "鈐山": "錫金—不丹東緣（東端）｜⛰喜馬拉雅·東段",     "㤗冒之山": "不丹東·白蛇｜⛰喜馬拉雅·不丹東部山麓",     "數歷之山": "不丹東—錫金·鸚鵡·白珠｜⛰喜馬拉雅·不丹—錫金山麓",
    "高山": "錫金·棕竹·磬石｜⛰喜馬拉雅·錫金段",     "女牀之山": "尼泊爾東·孔雀候選＋犀牛｜⛰喜馬拉雅·尼泊爾東段山麓",     "龍首之山": "尼泊爾東·苕水｜⛰喜馬拉雅·尼泊爾東部山麓",
    "鹿臺之山": "尼泊爾中東·原雞人面化｜⛰喜馬拉雅·尼泊爾中東部山麓",     "鳥危之山": "尼泊爾中·西注赤水（轉向一）｜⛰喜馬拉雅·加德滿都谷地緣",     "小次之山": "尼中西·葉猴｜⛰喜馬拉雅·尼泊爾中西部山麓",
    "大次之山": "尼泊爾西·羚羊｜⛰喜馬拉雅·尼泊爾西部山麓",     "薰吳之山": "尼西緣·金玉｜⛰喜馬拉雅·尼泊爾西緣山麓",     "厎陽之山": "庫馬盎·楠樟＋犀牛｜⛰喜馬拉雅·庫馬盎山麓",
    "眾獸之山": "庫馬盎西·犀牛三見｜⛰喜馬拉雅·庫馬盎西—喜馬偕爾東緣",     "皇人之山": "喜馬偕爾·皇水西注赤水（轉向二）｜⛰喜馬拉雅·喜馬偕爾山麓",     "中皇之山": "喜馬偕爾西·蕙棠｜⛰西瓦利克山·喜馬偕爾西—旁遮普東緣",
    "西皇之山": "旁遮普東緣·沼鹿｜⛰西瓦利克山·旁遮普東緣段",     "萊山": "印度河中游—哈拉帕心臟帶（終點）｜⛰鹽嶺",
}

# ---- projection: lon 72..98, lat 25..33 ----
LON0, LON1 = 72.0, 98.0
LAT0, LAT1 = 25.0, 33.0
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

S.append('<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">《西次二經》時代假想推理 × 現代映射參照圖</text>')
S.append('<text x="60" y="56" font-size="12" fill="#666">adapt-xici2-2 ｜ 錨點傳播鏈：開羅→西三→本經（無獨立錨點）｜ 0.385 km/里（±150 km）｜ 物種鎖最西＝印度河｜ proposed_pending_review</text>')

# ---- Tibet plateau (north) + Ganga plain (south) + Terai belt ----
S.append(f'<rect x="{X(LON0):.0f}" y="{Y(33.0):.0f}" width="{MW}" height="{Y(29.9)-Y(33.0):.0f}" fill="#e8e0d0"/>')
S.append(f'<text x="{X(74.5):.0f}" y="{Y(31.6):.0f}" font-size="13" fill="#8a7d5f" font-style="italic">青藏高原（藏南谷地）</text>')
S.append(f'<rect x="{X(LON0):.0f}" y="{Y(26.9):.0f}" width="{MW}" height="{Y(25.0)-Y(26.9):.0f}" fill="#dce8cf"/>')
S.append(f'<text x="{X(81.5):.0f}" y="{Y(25.7):.0f}" font-size="13" fill="#5a7a3a" font-style="italic">恆河平原</text>')
S.append(f'<rect x="{X(LON0):.0f}" y="{Y(28.6):.0f}" width="{MW}" height="{Y(26.9)-Y(28.6):.0f}" fill="#cfe0b8" opacity="0.7"/>')
S.append(f'<text x="{X(80.2):.0f}" y="{Y(27.15):.0f}" font-size="10" fill="#5a7a3a">特萊帶（山麓沖積林帶——犀牛/楠樟/沼鹿生態帶）</text>')
# Himalaya crest band
crest = [(74.5,32.3),(76.5,31.9),(78.5,30.9),(80.5,30.2),(82.5,29.8),(84.5,28.5),(86.0,28.1),(87.5,28.0),(89.5,27.9),(91.0,28.2),(93.0,29.0),(94.8,29.3),(95.9,29.5)]
S.append(f'<polyline points="{pts(crest)}" fill="none" stroke="#a08a5a" stroke-width="10" opacity="0.4" stroke-linecap="round"/>')
S.append(f'<text x="{X(74.8):.0f}" y="{Y(31.55):.0f}" font-size="11" fill="#7a6540">喜馬拉雅主脊（簡化示意）</text>')

# ---- rivers (modern reference, solid) ----
rivers = [
    ("雅魯藏布江（河候選B）", [(82.0,29.9),(84.5,29.7),(87.0,29.5),(89.5,29.4),(92.0,29.4),(94.5,29.4),(95.4,29.3)], False),
    ("布拉馬普特拉（河候選A東段）", [(95.4,29.3),(95.6,28.3),(94.9,27.5),(94.0,27.6),(92.5,27.2),(91.75,26.15),(90.2,26.2),(89.9,25.3)], False),
    ("恆河（河候選A）", [(78.3,29.9),(79.0,28.9),(80.3,26.5),(82.0,25.6),(83.0,25.3),(85.5,25.4),(88.2,25.15),(89.9,25.3)], False),
    ("亞穆納河", [(77.3,30.1),(77.2,28.6),(78.0,27.2),(79.0,26.8),(80.2,26.5),(81.85,25.5)], False),
    ("薩特萊傑河（皇水方向）", [(78.7,31.8),(77.4,31.3),(76.5,30.97),(75.85,30.9),(74.6,30.9),(73.4,30.3),(72.3,29.5)], False),
    ("印度河（赤水候選）", [(73.2,33.0),(72.4,33.0),(72.0,32.3),(72.0,31.7)], False),
    ("戈西河", [(86.9,28.5),(86.7,27.5),(86.5,26.6),(86.4,25.8)], False),
    ("甘達克河", [(84.8,28.5),(84.6,27.6),(84.4,26.7),(84.2,25.9)], False),
    ("卡納利河", [(82.4,29.0),(82.1,28.4),(81.9,27.5),(81.7,26.6)], False),
]
for name, line, dash in rivers:
    dash_attr = ' stroke-dasharray="5 4"' if dash else ''
    S.append(f'<polyline points="{pts(line)}" fill="none" stroke="#2f7fbf" stroke-width="1.6"{dash_attr}/>')
S.append(f'<text x="{X(84.3):.0f}" y="{Y(29.75):.0f}" font-size="9" fill="#2f7fbf">雅魯藏布江（河候選B）</text>')
S.append(f'<text x="{X(90.6):.0f}" y="{Y(26.5):.0f}" font-size="9" fill="#2f7fbf">布拉馬普特拉（河候選A東段）</text>')
S.append(f'<text x="{X(83.2):.0f}" y="{Y(25.6):.0f}" font-size="9" fill="#2f7fbf">恆河（河候選A）</text>')
S.append(f'<text x="{X(75.2):.0f}" y="{Y(31.7):.0f}" font-size="9" fill="#2f7fbf">薩特萊傑河（皇水方向）</text>')
S.append(f'<text x="{X(72.15):.0f}" y="{Y(32.4):.0f}" font-size="9" fill="#2f7fbf">印度河（赤水候選）</text>')

# ---- water-direction annotations ----
S.append(f'<text x="{X(92.3):.0f}" y="{Y(28.05):.0f}" font-size="10" fill="#5a7a3a">東段：東/南注河·渭（恆河系統）→</text>')
S.append(f'<text x="{X(74.0):.0f}" y="{Y(28.05):.0f}" font-size="10" fill="#8a4a2a">← 西段：西注赤水（印度河系統）</text>')

# ---- route chain ----
route = [(s["lon"], s["lat"]) for s in stations]
S.append(f'<polyline points="{pts(route)}" fill="none" stroke="#b03a2e" stroke-width="2.6" opacity="0.85"/>')
for i, s in enumerate(stations):
    x, y = X(s["lon"]), Y(s["lat"])
    anchor = (s["name"] == "鈐山")
    r = 8 if anchor else 5
    S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{"#e74c3c" if anchor else "#c0392b"}" stroke="#fff" stroke-width="1.5"/>')
    S.append(f'<text x="{x-4:.0f}" y="{y+4:.0f}" font-size="9" fill="#fff" font-weight="bold">{s["order"]}</text>')
    dy = -12 if i % 2 == 0 else 16
    if anchor:
        dy = -20
    S.append(f'<text x="{x-18:.0f}" y="{y+dy:.0f}" font-size="11" fill="#7b241c" font-weight="bold">{s["name"]}</text>')

# ---- turn points ----
for name, idx in [("水系轉向點一（西注赤水）", 8), ("轉向點二", 14)]:
    st = stations[idx - 1]
    x, y = X(st["lon"]), Y(st["lat"])
    S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="none" stroke="#8e44ad" stroke-width="1.4" stroke-dasharray="3 3"/>')
S.append(f'<text x="{X(89.2):.0f}" y="{Y(27.15):.0f}" font-size="9" fill="#8e44ad">紫圈＝水系轉向點（東西分水）</text>')

# ---- modern reference points ----
modern = [("德里", 77.2, 28.6), ("加德滿都", 85.3, 27.72), ("廷布", 89.6, 27.47),
          ("大吉嶺", 88.26, 27.04), ("岡仁波齊", 81.31, 31.07), ("西姆拉", 77.17, 31.1)]
for name, lo, la in modern:
    x, y = X(lo), Y(la)
    S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
    S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

# ---- scale bar (1°lon≈98km @28°N; px/deg = MW/26) ----
bx, by = X(72.4), Y(25.5)
px100 = 100 / 98.0 * (MW / 26)
S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*px100:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
for k in range(5):
    S.append(f'<line x1="{bx + k*px100:.0f}" y1="{by-4:.0f}" x2="{bx + k*px100:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
    S.append(f'<text x="{bx + k*px100 - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*100}</text>')
S.append(f'<text x="{bx + 4*px100 + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

# ---- grid ----
for lon in range(74, 98, 4):
    S.append(f'<line x1="{X(lon):.0f}" y1="{Y(LAT0):.0f}" x2="{X(lon):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(lon)-8:.0f}" y="{Y(LAT0)+14:.0f}" font-size="9" fill="#999">{lon}°E</text>')
for lat in range(26, 33):
    S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(lat):.0f}" x2="{X(LON1):.0f}" y2="{Y(lat):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
    S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(lat)+3:.0f}" font-size="9" fill="#999">{lat}°N</text>')

# ---- frame border + panel ----
S.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="none" stroke="#b8ad92" stroke-width="1.4"/>')
px = PANEL_X
S.append(f'<rect x="{px-12}" y="70" width="560" height="800" fill="#fffdf5" stroke="#cbb"/>')
S.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
legend = [
    ("#c0392b", "solid", "里程鏈（17站，紅圈數字＝站序；幾乎純西向）"),
    ("#e74c3c", "star", "大圈＝東端：鈐山（錨點傳播自開羅）"),
    ("#2f7fbf", "solid", "現代水體參照（河流）"),
    ("#8e44ad", "dash", "水系轉向點（東注河渭→西注赤水）"),
    ("#cfe0b8", "sq", "特萊帶（山麓沖積林帶）"),
    ("#a08a5a", "sq", "喜馬拉雅主脊（簡化示意）"),
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
ly = wrap_text(px, ly, 500, 10, "#666", "決定性證據＝南亞亞熱帶生物群：鸚鵡（3站）、孔雀候選（5站）、犀牛三見（5/12/13站）、原雞（7站）、葉猴（9站）、沼鹿（16站）、竹棕檀楠樟。犀牛西界止於印度河——物種鎖定最西位置。")
ly = wrap_text(px, ly + 4, 500, 10, "#666", "借名警示：河/渭/涇/苕/楚與中國水名同名，後世借名方向。赤水＝印度河候選（同名異水待裁）。伊朗—兩河空檔（72.5°E→38.4°E）由卷六至十八框架地理承擔（F-0007）。")

S.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">17 站 → 現實候選（審核中）</text>')
ty = ly + 38
for s in stations:
    S.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {s["name"]}</tspan>　→ {short.get(s["name"], "")}</text>')
    ty += 21.2

# ---- footer ----
fy = wrap_text(60, Y(LAT0) + 40, MW - 60, 11, "#666",
    "推理說明：自鈐山（錫金—不丹東緣）沿喜馬拉雅南麓/特萊帶西行——尼泊爾（孔雀候選·犀牛·葉猴·楠樟）、庫馬盎—喜馬偕爾（皇水西注赤水＝印度河），至萊山（印度河中游—哈拉帕心臟帶；犀牛西界止於印度河，物種鎖定最西位置）。")
fy = wrap_text(60, fy + 6, MW - 60, 11, "#666",
    "腿程合計 4,570 里≈1,759 km（0.385；原文自記 4,140 里，+10.4% 差異待校）。所有對應為競爭假說，時代窗口 4000–1000 BCE；犀牛/沼鹿/葉猴分布後期收縮，退出不作否決。")

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
