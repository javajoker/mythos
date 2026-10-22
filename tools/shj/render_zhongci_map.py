#!/usr/bin/env python3
"""Generic Zhongshan-classic SVG map renderer.

Usage: render_zhongci_map.py <config.json>
Config: {slug, title, subtitle, grid, stations_short{station: short}, anchor_note,
         window {lon0,lon1,lat0,lat1}, annotations [[text, lon, lat, color]...],
         features_extra [...], out}
Basemap (Central China rivers and ranges) is simplified示意 geometry.
Overflow audit built in. All mappings proposed_pending_review.
"""
import json, math, os, re, sys

HERE = os.path.join(os.path.dirname(__file__), "..", "..", "projects", "shanhaijing", "data", "derived", "era", "adaptation")

def render(cfg):
    stations = []
    for line in open(os.path.join(HERE, cfg["grid"])):
        r = json.loads(line)
        if "meta" in r:
            continue
        g = r["grid"]["0.385"]
        stations.append({"name": r["station"], "order": r["order"], "lat": g["lat"], "lon": g["lon"]})
    short = cfg["stations_short"]
    W = cfg["window"]
    LON0, LON1, LAT0, LAT1 = W["lon0"], W["lon1"], W["lat0"], W["lat1"]
    MX, MY, MW, MH = 60, 80, 1000, 470
    PANEL_X = MX + MW + 30

    def X(lon): return MX + (lon - LON0) / (LON1 - LON0) * MW
    def Y(lat): return MY + (LAT1 - lat) / (LAT1 - LAT0) * MH
    def pts(seq): return " ".join(f"{X(lo):.1f},{Y(la):.1f}" for lo, la in seq)
    def _tw(t, size): return sum(size if ord(c) > 0x2E7F else size * 0.55 for c in t)

    S = []
    def wrap_text(x, y, max_w, size, color, text, lh=None):
        lh = lh or size * 1.45
        line, lines = "", []
        for ch in text:
            if _tw(line + ch, size) > max_w:
                lines.append(line); line = ch
            else:
                line += ch
        if line:
            lines.append(line)
        for i, ln in enumerate(lines):
            S.append(f'<text x="{x}" y="{y + i * lh:.0f}" font-size="{size}" fill="{color}">{ln}</text>')
        return y + len(lines) * lh

    S.append('<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="900" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">')
    S.append('<rect width="1700" height="900" fill="#f7f3e8"/>')
    S.append('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#555"/></marker>'
             '<pattern id="sand" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#efe3c0"/><circle cx="2" cy="2" r="0.8" fill="#d6b96a"/><circle cx="6" cy="6" r="0.8" fill="#d6b96a"/></pattern></defs>')
    S.append(f'<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">{cfg["title"]}</text>')
    S.append(f'<text x="60" y="56" font-size="12" fill="#666">{cfg["subtitle"]}</text>')

    # ---- Central China basemap (simplified) ----
    yellow = [(96.5,34.6),(98.0,34.4),(99.5,35.0),(100.5,35.6),(101.8,35.9),(103.0,36.05),(103.8,36.1),
              (104.4,36.5),(105.0,37.3),(105.6,37.9),(106.2,38.5),(106.9,39.1),(107.4,39.7),(108.4,40.3),
              (109.5,40.5),(110.4,40.5),(111.1,40.3),(111.6,40.0),(111.6,39.3),(111.3,38.5),(110.9,37.6),
              (110.7,36.7),(110.55,35.8),(110.5,35.0),(110.55,34.6),(111.0,34.7),(111.8,34.8),(112.8,34.85),
              (113.7,34.9),(114.6,35.0),(115.5,35.3),(116.3,35.6),(117.0,36.3),(117.6,37.0),(118.2,37.4),(118.8,37.6)]
    if LON1 > 96 and LON0 < 119 and LAT1 > 34 and LAT0 < 41:
        S.append(f'<polyline points="{pts(yellow)}" fill="none" stroke="#c89a2e" stroke-width="2.4"/>')
        S.append(f'<text x="{X(112.5):.0f}" y="{Y(35.25):.0f}" font-size="10" fill="#a07d1e">黃河（現代參照）</text>')
    wei = [(104.2,34.75),(105.5,34.7),(106.8,34.55),(108.0,34.5),(109.2,34.45),(110.2,34.5),(110.55,34.62)]
    if LON1 > 104 and LON0 < 111:
        S.append(f'<polyline points="{pts(wei)}" fill="none" stroke="#2f7fbf" stroke-width="2"/>')
        S.append(f'<text x="{X(106.6):.0f}" y="{Y(34.72):.0f}" font-size="9" fill="#2f7fbf">渭河</text>')
    luo = [(110.1,34.1),(110.9,34.25),(111.6,34.4),(112.3,34.55),(112.9,34.62),(113.4,34.68)]
    if LON1 > 110 and LON0 < 114:
        S.append(f'<polyline points="{pts(luo)}" fill="none" stroke="#2f7fbf" stroke-width="1.8"/>')
        S.append(f'<text x="{X(111.3):.0f}" y="{Y(34.15):.0f}" font-size="9" fill="#2f7fbf">洛河（洛——借名標記）</text>')
    yi = [(111.3,33.8),(111.8,34.1),(112.35,34.45),(112.8,34.6)]
    if LON1 > 111 and LON0 < 113:
        S.append(f'<polyline points="{pts(yi)}" fill="none" stroke="#2f7fbf" stroke-width="1.5"/>')
        S.append(f'<text x="{X(111.5):.0f}" y="{Y(33.9):.0f}" font-size="9" fill="#2f7fbf">伊河（伊水——借名標記）</text>')
    fen = [(112.4,38.3),(111.9,37.5),(111.5,36.7),(111.2,36.1),(110.9,35.6),(110.7,35.15)]
    if LON1 > 110 and LON0 < 113 and LAT1 > 35:
        S.append(f'<polyline points="{pts(fen)}" fill="none" stroke="#2f7fbf" stroke-width="1.6"/>')
        S.append(f'<text x="{X(111.6):.0f}" y="{Y(37.2):.0f}" font-size="9" fill="#2f7fbf">汾河（汾水——借名標記）</text>')
    han = [(106.8,33.0),(108.0,32.8),(109.2,32.6),(110.4,32.45),(111.4,32.35),(112.3,32.3),(113.2,32.2),(114.0,32.1),(114.5,31.9)]
    if LON1 > 106 and LAT0 < 33:
        S.append(f'<polyline points="{pts(han)}" fill="none" stroke="#2f7fbf" stroke-width="1.8"/>')
        S.append(f'<text x="{X(108.0):.0f}" y="{Y(32.6):.0f}" font-size="9" fill="#2f7fbf">漢江（漢水——借名標記）</text>')
    yangtze = [(99.0,32.6),(100.5,31.8),(102.0,31.2),(103.6,30.9),(104.8,30.7),(106.0,30.4),(107.3,30.1),
               (108.5,29.8),(109.5,29.9),(110.2,30.3),(111.0,30.5),(111.8,30.7),(112.6,30.6),(113.4,30.4),(114.2,30.4),(114.9,30.5)]
    if LON1 > 99 and LAT0 < 31.5:
        S.append(f'<polyline points="{pts(yangtze)}" fill="none" stroke="#2f7fbf" stroke-width="2.2"/>')
        S.append(f'<text x="{X(110.3):.0f}" y="{Y(30.15):.0f}" font-size="10" fill="#2f7fbf">長江（江/大江——借名標記）</text>')
    # ranges shading
    for name, cx, cy, rx, ry in cfg.get("ranges", []):
        S.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{rx/ (LON1-LON0) * MW:.0f}" ry="{ry / (LAT1-LAT0) * MH:.0f}" fill="#c9b18a" opacity="0.4"/>')
        S.append(f'<text x="{X(cx)-24:.0f}" y="{Y(cy)+3:.0f}" font-size="10" fill="#7a6540">{name}</text>')

    # ---- extra features (period hypothesis etc.) ----
    for feat in cfg.get("features_extra", []):
        kind = feat[0]
        if kind == "line":
            _, line, color, dash, width = feat
            d = f' stroke-dasharray="{dash}"' if dash else ""
            S.append(f'<polyline points="{pts(line)}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>')
        elif kind == "blob":
            _, cx, cy, rx, ry, color, label = feat
            S.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{rx/(LON1-LON0)*MW:.0f}" ry="{ry/(LAT1-LAT0)*MH:.0f}" fill="{color}" opacity="0.35" stroke="{color}" stroke-dasharray="4 3"/>')
            if label:
                S.append(f'<text x="{X(cx)-30:.0f}" y="{Y(cy):.0f}" font-size="9" fill="{color}">{label}</text>')

    # ---- route chain ----
    route = [(s["lon"], s["lat"]) for s in stations]
    S.append(f'<polyline points="{pts(route)}" fill="none" stroke="#b03a2e" stroke-width="2.6" opacity="0.85"/>')
    anchor_idx = cfg.get("anchor_index", -1)
    for i, s in enumerate(stations):
        x, y = X(s["lon"]), Y(s["lat"])
        anchor = (i == anchor_idx)
        r = 8 if anchor else 5
        S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{"#e74c3c" if anchor else "#c0392b"}" stroke="#fff" stroke-width="1.5"/>')
        S.append(f'<text x="{x-4:.0f}" y="{y+4:.0f}" font-size="9" fill="#fff" font-weight="bold">{s["order"]}</text>')
        dy = -11 if i % 2 == 0 else 16
        if anchor:
            dy = -20
        S.append(f'<text x="{x-18:.0f}" y="{y+dy:.0f}" font-size="10" fill="#7b241c" font-weight="bold">{s["name"]}</text>')

    # ---- annotations ----
    for text_, lo, la, color in cfg.get("annotations", []):
        S.append(f'<text x="{X(lo):.0f}" y="{Y(la):.0f}" font-size="9" fill="{color}">{text_}</text>')

    # ---- modern reference points ----
    for name, lo, la in cfg.get("modern", []):
        x, y = X(lo), Y(la)
        S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
        S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

    # ---- scale bar ----
    latm = (LAT0 + LAT1) / 2
    km_per_deg = 111.3 * math.cos(math.radians(latm))
    bx, by = X(LON0 + 0.4), Y(LAT0 + 0.5)
    px100 = 100 / km_per_deg * (MW / (LON1 - LON0))
    S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*px100:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
    for k in range(5):
        S.append(f'<line x1="{bx + k*px100:.0f}" y1="{by-4:.0f}" x2="{bx + k*px100:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
        S.append(f'<text x="{bx + k*px100 - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*100}</text>')
    S.append(f'<text x="{bx + 4*px100 + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

    # ---- grid ----
    for lon in range(int(LON0) + 1, int(LON1), 2):
        S.append(f'<line x1="{X(lon):.0f}" y1="{Y(LAT0):.0f}" x2="{X(lon):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
        S.append(f'<text x="{X(lon)-8:.0f}" y="{Y(LAT0)+14:.0f}" font-size="9" fill="#999">{lon}°E</text>')
    for lat in range(int(LAT0) + 1, int(LAT1)):
        S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(lat):.0f}" x2="{X(LON1):.0f}" y2="{Y(lat):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
        S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(lat)+3:.0f}" font-size="9" fill="#999">{lat}°N</text>')

    # ---- panel ----
    px = PANEL_X
    S.append(f'<rect x="{px-12}" y="70" width="560" height="800" fill="#fffdf5" stroke="#cbb"/>')
    S.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
    ly = 118
    for color, style, label in cfg["legend"]:
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
    for note in cfg.get("panel_notes", []):
        ly = wrap_text(px, ly, 500, 10, "#666", note) + 4
    S.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">{len(stations)} 站 → 現實候選（審核中）</text>')
    ty = ly + 38
    for s in stations:
        S.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {s["name"]}</tspan>　→ {short.get(s["name"], "")}</text>')
        ty += 21.2

    fy = wrap_text(60, Y(LAT0) + 40, MW, 11, "#666", cfg["footer1"])
    fy = wrap_text(60, fy + 6, MW, 11, "#666", cfg["footer2"])

    S.append('</svg>')
    svg = "\n".join(S)
    out = os.path.join(HERE, cfg["out"])
    with open(out, "w") as f:
        f.write(svg)
    bad = []
    for m in re.finditer(r'<text x="([\d.-]+)" y="[\d.-]+" font-size="([\d.]+)"[^>]*>([^<]+)</text>', svg):
        x, size, t = float(m.group(1)), float(m.group(2)), m.group(3)
        end = x + _tw(t, size)
        limit = 1700 if x >= PANEL_X - 12 else PANEL_X - 16
        if end > limit:
            bad.append((t[:24], int(x), int(end)))
    print("wrote", out, os.path.getsize(out), "bytes | overflow:", bad if bad else "none")

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])))
