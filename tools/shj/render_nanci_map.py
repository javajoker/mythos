#!/usr/bin/env python3
"""Generic spec-driven per-scroll SVG map renderer.

Usage: render_nanci_map.py <config.json>  (specs in era/adaptation/specs/)
Spec is the single source of truth: window, basemap/ranges/features_extra,
stations_short, legend, annotations, modern points, panel notes, footers.
Supports fit_coords (plotting-only overrides for divergent arithmetic grids),
key_labels/compact markers for dense clusters, name#order keys for duplicate
station names, auto two-column station list, and a full overflow audit
(plain-text and tspan rows, position and width). All mappings
proposed_pending_review.
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
    MX, MY, MW, MH = 60, 80, 1000, 560
    PANEL_X = MX + MW + 30

    def X(lon): return MX + (lon - LON0) / (LON1 - LON0) * MW
    def Y(lat): return MY + (LAT1 - lat) / (LAT1 - LAT0) * MH
    def pts(seq): return " ".join(f"{X(lo):.1f},{Y(la):.1f}" for lo, la in seq)
    def _tw(t, size):
        # CJK 与全角符号按全宽；箭头/≈/×/破折号在 CJK 字体中亦为全宽
        w = 0.0
        for c in t:
            o = ord(c)
            if o > 0x2E7F or 0x2190 <= o <= 0x27BF or o in (0x00D7, 0x2248, 0x2013, 0x2014):
                w += size
            else:
                w += size * 0.55
        return w
    def in_win(lo, la): return LON0 < lo < LON1 and LAT0 < la < LAT1

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
             '<pattern id="sand" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#efe3c0"/><circle cx="2" cy="2" r="0.8" fill="#d6b96a"/><circle cx="6" cy="6" r="0.8" fill="#d6b96a"/></pattern>'
             f'<clipPath id="mapclip"><rect x="{MX}" y="{MY}" width="{MW}" height="{MH}"/></clipPath></defs>')
    S.append(f'<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">{cfg["title"]}</text>')
    S.append(f'<text x="60" y="56" font-size="12" fill="#666">{cfg["subtitle"]}</text>')

    # ---- map content group: clipped to the main frame, nothing may spill ----
    S.append('<g clip-path="url(#mapclip)">')

    # ---- spec-driven basemap (simplified示意 geometry) ----
    for feat in cfg.get("basemap", []):
        kind = feat[0]
        if kind == "line":
            _, seq, color, width, label, lpos = feat
            S.append(f'<polyline points="{pts(seq)}" fill="none" stroke="{color}" stroke-width="{width}"/>')
            if label and lpos and in_win(lpos[0], lpos[1]):
                S.append(f'<text x="{X(lpos[0]):.0f}" y="{Y(lpos[1]):.0f}" font-size="10" fill="{color}">{label}</text>')
        elif kind == "blob":
            _, cx, cy, rx, ry, color, label = feat
            S.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{rx/(LON1-LON0)*MW:.0f}" ry="{ry/(LAT1-LAT0)*MH:.0f}" fill="{color}" opacity="0.35"/>')
            if label and in_win(cx, cy):
                S.append(f'<text x="{X(cx)-24:.0f}" y="{Y(cy)+3:.0f}" font-size="10" fill="#7a6540">{label}</text>')
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
    # fit_coords (optional): {"order": [lon, lat]} plotting-only overrides for scrolls whose
    # raw arithmetic grid diverges grossly from the semantic corridor (documented variant).
    fit = {int(k): tuple(v) for k, v in cfg.get("fit_coords", {}).items()}
    for s in stations:
        if s["order"] in fit:
            s["lon"], s["lat"] = fit[s["order"]]
    route = [(s["lon"], s["lat"]) for s in stations]
    S.append(f'<polyline points="{pts(route)}" fill="none" stroke="#b03a2e" stroke-width="2.6" opacity="0.85"/>')
    _dx_tot = abs(X(route[-1][0]) - X(route[0][0]))
    _dy_tot = abs(Y(route[-1][1]) - Y(route[0][1]))
    vertical_chain = _dy_tot > _dx_tot * 1.5
    anchor_idx = cfg.get("anchor_index", -1)
    # key_labels (optional): only these station orders get name labels; compact markers elsewhere
    key_labels = set(cfg.get("key_labels", []))
    compact = bool(key_labels)
    ki = 0
    for i, s in enumerate(stations):
        x, y = X(s["lon"]), Y(s["lat"])
        anchor = (i == anchor_idx)
        is_key = (not compact) or (s["order"] in key_labels)
        r = 8 if anchor else (5 if is_key else 3)
        S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{"#e74c3c" if anchor else "#c0392b"}" stroke="#fff" stroke-width="1.5"/>')
        if is_key:
            S.append(f'<text x="{x-4:.0f}" y="{y+4:.0f}" font-size="9" fill="#fff" font-weight="bold">{s["order"]}</text>')
        # 南北走向鏈（縱向相鄰站）改用左右交替標註，避免上下標籤重合
        if not is_key:
            continue
        if vertical_chain:
            dxl = 9 if ki % 2 == 0 else -int(_tw(s["name"], 10)) - 8
            S.append(f'<text x="{x+dxl:.0f}" y="{y+4:.0f}" font-size="10" fill="#7b241c" font-weight="bold">{s["name"]}</text>')
        else:
            dy = -11 if ki % 2 == 0 else 16
            if anchor:
                dy = -20
            S.append(f'<text x="{x-18:.0f}" y="{y+dy:.0f}" font-size="10" fill="#7b241c" font-weight="bold">{s["name"]}</text>')
        ki += 1

    # ---- annotations ----
    for text_, lo, la, color in cfg.get("annotations", []):
        S.append(f'<text x="{X(lo):.0f}" y="{Y(la):.0f}" font-size="9" fill="{color}">{text_}</text>')

    # ---- modern reference points ----
    for name, lo, la in cfg.get("modern", []):
        x, y = X(lo), Y(la)
        S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
        S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

    S.append('</g>')  # end mapclip group

    # ---- grid ----
    lon_span, lat_span = LON1 - LON0, LAT1 - LAT0
    lon_step = 2 if lon_span >= 6 else (1 if lon_span >= 2.5 else 0.5)
    lat_step = 1 if lat_span >= 2.5 else 0.5
    v = math.ceil(LON0 / lon_step) * lon_step
    if v <= LON0: v += lon_step
    while v < LON1:
        S.append(f'<line x1="{X(v):.0f}" y1="{Y(LAT0):.0f}" x2="{X(v):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
        S.append(f'<text x="{X(v)-8:.0f}" y="{Y(LAT0)+16:.0f}" font-size="9" fill="#999">{v:g}°E</text>')
        v += lon_step
    v = math.ceil(LAT0 / lat_step) * lat_step
    if v <= LAT0: v += lat_step
    while v < LAT1:
        S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(v):.0f}" x2="{X(LON1):.0f}" y2="{Y(v):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
        S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(v)+3:.0f}" font-size="9" fill="#999">{v:g}°N</text>')
        v += lat_step

    # ---- main frame border (above grid, below scale bar) ----
    S.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="none" stroke="#b8ad92" stroke-width="1.4"/>')

    # ---- scale bar (adaptive segment length, never wider than 400 px) ----
    latm = (LAT0 + LAT1) / 2
    km_per_deg = 111.3 * math.cos(math.radians(latm))
    px_per_km = (MW / lon_span) / km_per_deg
    seg = next((s for s in (200, 100, 50, 25, 10) if 4 * s * px_per_km <= 400), 10)
    pxs = seg * px_per_km
    bx, by = X(LON0 + cfg.get("scale_bar_frac", 0.06) * lon_span), Y(LAT0 + 0.14 * lat_span)
    S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*pxs:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
    for k in range(5):
        S.append(f'<line x1="{bx + k*pxs:.0f}" y1="{by-4:.0f}" x2="{bx + k*pxs:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
        S.append(f'<text x="{bx + k*pxs - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*seg}</text>')
    S.append(f'<text x="{bx + 4*pxs + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

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
    if len(stations) > 26 or ty + len(stations) * 21.2 > 850:
        # two-column compact list; entries trimmed to the column width
        half = (len(stations) + 1) // 2
        for idx, s in enumerate(stations):
            col, row = (0, idx) if idx < half else (1, idx - half)
            skey = f"{s['name']}#{s['order']}"
            label = f'{s["order"]:2d} {s["name"]} → {short.get(skey, short.get(s["name"], ""))}'
            while label and _tw(label, 9.5) > 262:
                label = label[:-2] + '…'
            S.append(f'<text x="{px + col * 272}" y="{ty + row * 17.5:.0f}" font-size="9.5" fill="#7b241c">{label}</text>')
    else:
        for s in stations:
            skey = f"{s['name']}#{s['order']}"
            S.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="#7b241c"><tspan font-weight="bold">{s["order"]:2d} {s["name"]}</tspan>　→ {short.get(skey, short.get(s["name"], ""))}</text>')
            ty += 21.2

    fy = wrap_text(60, Y(LAT0) + 46, MW - 60, 11, "#666", cfg["footer1"])
    fy = wrap_text(60, fy + 6, MW - 60, 11, "#666", cfg["footer2"])

    S.append('</svg>')
    svg = "\n".join(S)
    out = os.path.join(HERE, cfg["out"])
    with open(out, "w") as f:
        f.write(svg)
    bad = []
    for m in re.finditer(r'<text x="([\d.-]+)" y="([\d.-]+)" font-size="([\d.]+)"[^>]*>([^<]+)</text>', svg):
        x, y, size, t = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        end = x + _tw(t, size)
        if x < 0:
            bad.append(("left-off", t[:20], int(x)))
        elif y >= 65 and x < PANEL_X - 12 and end > MX + MW - 8:
            bad.append(("past-frame", t[:20], int(end)))
        elif x >= PANEL_X - 12 and end > 1630:
            bad.append(("past-panel", t[:20], int(end)))
        if y > 888:
            bad.append(("bottom-off", t[:20], int(y)))
    # tspan rows: strip child markup, audit position AND width
    for m in re.finditer(r'<text x="([\d.-]+)" y="([\d.-]+)" font-size="([\d.]+)"[^>]*>(.*?)</text>', svg):
        x, y, size, inner = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        if '<' not in inner:
            continue
        t = re.sub(r'<[^>]+>', '', inner)
        end = x + _tw(t, size)
        if x < 0:
            bad.append(("left-off", t[:20], int(x)))
        elif y >= 65 and x < PANEL_X - 12 and end > MX + MW - 8:
            bad.append(("past-frame", t[:20], int(end)))
        elif x >= PANEL_X - 12 and end > 1630:
            bad.append(("past-panel", t[:20], int(end)))
        if y > 888:
            bad.append(("bottom-off", t[:20], int(y)))
    for m in re.finditer(r'<circle cx="([\d.-]+)" cy="([\d.-]+)" r="[\d.]+" fill="#(?:e74c3c|c0392b)" stroke="#fff"', svg):
        cx, cy = float(m.group(1)), float(m.group(2))
        if not (MX <= cx <= MX + MW and MY <= cy <= MY + MH):
            bad.append(("station-off-frame", f"({cx:.0f},{cy:.0f})", 0))
    print("wrote", out, os.path.getsize(out), "bytes | overflow:", bad if bad else "none")

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])))
