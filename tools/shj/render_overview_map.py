#!/usr/bin/env python3
"""Overview-map renderer: multiple route chains (sub-scrolls) on one canvas.

Usage: render_overview_map.py <config.json>
Config: {out, title, subtitle, window{lon0,lon1,lat0,lat1},
         basemap[...], chains[{grid,label,short,color,anchor_index?,label_pos?,fit?}...],
         legend[...], annotations[...], modern[...], panel_notes[...], footer1, footer2}
fit=true auto-applies fit_coords from specs/<slug>-map.json (plotting-only overrides).
Overflow audit built in. All mappings proposed_pending_review.
"""
import json, math, os, re, sys

HERE = os.path.join(os.path.dirname(__file__), "..", "..", "projects", "shanhaijing", "data", "derived", "era", "adaptation")

def render(cfg):
    W = cfg["window"]
    LON0, LON1, LAT0, LAT1 = W["lon0"], W["lon1"], W["lat0"], W["lat1"]
    MX, MY, MW, MH = 60, 80, 1000, 560
    PANEL_X = MX + MW + 30

    def X(lon): return MX + (lon - LON0) / (LON1 - LON0) * MW
    def Y(lat): return MY + (LAT1 - lat) / (LAT1 - LAT0) * MH
    def pts(seq): return " ".join(f"{X(lo):.1f},{Y(la):.1f}" for lo, la in seq)
    def _tw(t, size):
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
    def wrap_text(x, y, max_w, size, color, text, lh=None, tgt=None):
        tgt = S if tgt is None else tgt
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
            tgt.append(f'<text x="{x}" y="{y + i * lh:.0f}" font-size="{size}" fill="{color}">{ln}</text>')
        return y + len(lines) * lh

    S.append('<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="900" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">')
    S.append('<rect width="1700" height="900" fill="#f7f3e8"/>')
    S.append(f'<clipPath id="mapclip"><rect x="{MX}" y="{MY}" width="{MW}" height="{MH}"/></clipPath>')
    S.append(f'<defs><clipPath id="mapclip"><rect x="{MX}" y="{MY}" width="{MW}" height="{MH}"/></clipPath>'
             '<pattern id="sand" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#efe3c0"/><circle cx="2" cy="2" r="0.8" fill="#d6b96a"/><circle cx="6" cy="6" r="0.8" fill="#d6b96a"/></pattern></defs>')
    S.append(f'<text x="60" y="34" font-size="21" font-weight="bold" fill="#333">{cfg["title"]}</text>')
    S.append(f'<text x="60" y="56" font-size="12" fill="#666">{cfg["subtitle"]}</text>')

    S.append('<g clip-path="url(#mapclip)">')

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
    for name, cx, cy, rx, ry in cfg.get("ranges", []):
        S.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{rx/ (LON1-LON0) * MW:.0f}" ry="{ry / (LAT1-LAT0) * MH:.0f}" fill="#c9b18a" opacity="0.4"/>')
        S.append(f'<text x="{X(cx)-24:.0f}" y="{Y(cy)+3:.0f}" font-size="10" fill="#7a6540">{name}</text>')

    # ---- chains ----
    for ch in cfg.get("chains", []):
        slug = re.sub(r"-station-grid\.jsonl$", "", ch["grid"])
        stations = []
        for line in open(os.path.join(HERE, ch["grid"])):
            r = json.loads(line)
            if "meta" in r:
                continue
            g = r["grid"]["0.385"]
            stations.append({"name": r["station"], "order": r["order"], "lat": g["lat"], "lon": g["lon"]})
        if ch.get("fit"):
            sp = os.path.join(HERE, "specs", f"{slug}-map.json")
            if os.path.exists(sp):
                fit = {int(k): tuple(v) for k, v in json.load(open(sp)).get("fit_coords", {}).items()}
                for s in stations:
                    if s["order"] in fit:
                        s["lon"], s["lat"] = fit[s["order"]]
        context = bool(ch.get("context"))
        color = "#b7a98c" if context else ch.get("color", "#c0392b")
        width = 1.4 if context else 2.6
        route = [(s["lon"], s["lat"]) for s in stations]
        S.append(f'<polyline points="{pts(route)}" fill="none" stroke="{color}" stroke-width="{width}" opacity="0.85"/>')
        if context:
            continue
        for i, s in enumerate(stations):
            x, y = X(s["lon"]), Y(s["lat"])
            r = 5 if i in (0, len(stations) - 1) else 3
            S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{color}" stroke="#fff" stroke-width="1.2"/>')
        ai = ch.get("anchor_index")
        if ai is not None:
            s = stations[ai]
            S.append(f'<circle cx="{X(s["lon"]):.0f}" cy="{Y(s["lat"]):.0f}" r="9" fill="none" stroke="{color}" stroke-width="2.5"/>')
        lp = ch.get("label_pos")
        if lp:
            lx, ly = X(lp[0]), Y(lp[1])
        else:
            lx, ly = X(route[0][0]) + 8, Y(route[0][1]) - 8
        S.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="11" font-weight="bold" fill="{color}">{ch["label"]}</text>')

    for text_, lo, la, color in cfg.get("annotations", []):
        S.append(f'<text x="{X(lo):.0f}" y="{Y(la):.0f}" font-size="9" fill="{color}">{text_}</text>')

    # ---- point markers (framework-book patch maps: regions/cultures/pending anchors) ----
    for p in cfg.get("points", []):
        x, y = X(p["lon"]), Y(p["lat"])
        color = p.get("color", "#8e44ad")
        status = p.get("status", "mapped")
        if status == "pending_anchor":
            S.append(f'<rect x="{x-5:.0f}" y="{y-5:.0f}" width="10" height="10" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="3 2"/>')
        elif status == "region":
            S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{color}" opacity="0.45" stroke="{color}" stroke-width="1.5"/>')
        else:
            S.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{p.get("size", 5.5)}" fill="{color}" stroke="#fff" stroke-width="1.2"/>')
        if p.get("label", True):
            if p.get("label_pos"):
                lx, ly = X(p["label_pos"][0]), Y(p["label_pos"][1])
            else:
                lx, ly = x + 8, y + 4
            S.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="10" font-weight="bold" fill="{color}">{p["name"]}</text>')

    for name, lo, la in cfg.get("modern", []):
        x, y = X(lo), Y(la)
        S.append(f'<rect x="{x-3:.0f}" y="{y-3:.0f}" width="6" height="6" fill="#34495e"/>')
        S.append(f'<text x="{x+5:.0f}" y="{y-4:.0f}" font-size="9" fill="#34495e">{name}</text>')

    S.append('</g>')  # end mapclip group

    # ---- grid ----
    lon_span, lat_span = LON1 - LON0, LAT1 - LAT0
    lon_step = 10 if lon_span >= 60 else (5 if lon_span >= 20 else 2)
    lat_step = 5 if lat_span >= 20 else 2
    v = math.ceil(LON0 / lon_step) * lon_step
    if v <= LON0: v += lon_step
    while v < LON1:
        S.append(f'<line x1="{X(v):.0f}" y1="{Y(LAT0):.0f}" x2="{X(v):.0f}" y2="{Y(LAT1):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
        S.append(f'<text x="{X(v)-8:.0f}" y="{Y(LAT0)+16:.0f}" font-size="9" fill="#999">{v:g}°{"W" if v<0 else "E"}</text>')
        v += lon_step
    v = math.ceil(LAT0 / lat_step) * lat_step
    if v <= LAT0: v += lat_step
    while v < LAT1:
        S.append(f'<line x1="{X(LON0):.0f}" y1="{Y(v):.0f}" x2="{X(LON1):.0f}" y2="{Y(v):.0f}" stroke="#d9d2c0" stroke-width="0.6"/>')
        S.append(f'<text x="{X(LON0)-26:.0f}" y="{Y(v)+3:.0f}" font-size="9" fill="#999">{v:g}°N</text>')
        v += lat_step

    S.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="none" stroke="#b8ad92" stroke-width="1.4"/>')

    # ---- scale bar ----
    latm = (LAT0 + LAT1) / 2
    km_per_deg = 111.3 * math.cos(math.radians(latm))
    px_per_km = (MW / lon_span) / km_per_deg
    seg = next((s for s in (1000, 500, 200, 100, 50) if 4 * s * px_per_km <= 400), 50)
    pxs = seg * px_per_km
    bx, by = X(LON0 + cfg.get("scale_bar_frac", 0.06) * lon_span), Y(LAT0 + 0.14 * lat_span)
    S.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx + 4*pxs:.0f}" y2="{by:.0f}" stroke="#333" stroke-width="2"/>')
    for k in range(5):
        S.append(f'<line x1="{bx + k*pxs:.0f}" y1="{by-4:.0f}" x2="{bx + k*pxs:.0f}" y2="{by+4:.0f}" stroke="#333" stroke-width="1.5"/>')
        S.append(f'<text x="{bx + k*pxs - 8:.0f}" y="{by+16:.0f}" font-size="9" fill="#333">{k*seg}</text>')
    S.append(f'<text x="{bx + 4*pxs + 8:.0f}" y="{by+4:.0f}" font-size="9" fill="#333">km（100里≈38.5km @0.385）</text>')

    # ---- panel ----
    P = []
    px = PANEL_X
    P.append(f'<text x="{px}" y="96" font-size="14" font-weight="bold" fill="#333">圖例</text>')
    ly = 118
    for color, style, label in cfg["legend"]:
        if style == "solid":
            P.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
        elif style == "dash":
            P.append(f'<line x1="{px}" y1="{ly}" x2="{px+26}" y2="{ly}" stroke="{color}" stroke-width="2" stroke-dasharray="6 4"/>')
        elif style == "sq":
            P.append(f'<rect x="{px+8}" y="{ly-5}" width="8" height="8" fill="{color}"/>')
        elif style == "star":
            P.append(f'<circle cx="{px+13}" cy="{ly}" r="8" fill="{color}"/>')
        P.append(f'<text x="{px+34}" y="{ly+4}" font-size="11" fill="#444">{label}</text>')
        ly += 22
    ly += 8
    for note in cfg.get("panel_notes", []):
        ly = wrap_text(px, ly, 500, 10, "#666", note, tgt=P) + 4
    chains = [c for c in cfg.get("chains", []) if not c.get("context")]
    points = cfg.get("points", [])
    if points and cfg.get("points_panel", True):
        P.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">本卷地點/區域 → 現實候選（審核中）</text>')
        ty = ly + 38
        rows_p = points
        if ty + len(rows_p) * 21.2 > 850:
            half = (len(rows_p) + 1) // 2
            for idx, p in enumerate(rows_p):
                col, row = (0, idx) if idx < half else (1, idx - half)
                label = f'{p["name"]} → {p.get("note","")}'
                while label and _tw(label, 9.5) > 262:
                    label = label[:-2] + '…'
                P.append(f'<text x="{px + col * 272}" y="{ty + row * 17.5:.0f}" font-size="9.5" fill="{p.get("color","#8e44ad")}">{label}</text>')
            ty = ty + half * 17.5
        else:
            for p in rows_p:
                label = f'{p["name"]} → {p.get("note","")}'
                while label and _tw(label, 11) > 530:
                    label = label[:-2] + '…'
                P.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="{p.get("color","#8e44ad")}">{label}</text>')
                ty += 21.2
    if chains:
        P.append(f'<text x="{px}" y="{ly+16}" font-size="14" font-weight="bold" fill="#333">子經鏈 → 現實區域（審核中）</text>')
        ty = ly + 38
        nch = len(chains)
        if ty + nch * 21.2 > 850:
            half = (nch + 1) // 2
            for idx, ch in enumerate(chains):
                col, row = (0, idx) if idx < half else (1, idx - half)
                n = sum(1 for l in open(os.path.join(HERE, ch["grid"])) if '"station"' in l)
                label = f'{ch["label"]}（{n}）→ {ch.get("short","")}'
                while label and _tw(label, 9.5) > 262:
                    label = label[:-2] + '…'
                P.append(f'<text x="{px + col * 272}" y="{ty + row * 17.5:.0f}" font-size="9.5" fill="{ch.get("color","#c0392b")}">{label}</text>')
            ty = ty + half * 17.5
        else:
            for ch in chains:
                n = sum(1 for l in open(os.path.join(HERE, ch["grid"])) if '"station"' in l)
                label = f'{ch["label"]}（{n} 站）→ {ch.get("short","")}'
                trimmed = False
                while label and _tw(label, 11) > 530:
                    label = label[:-2] + '…'
                    trimmed = True
                if trimmed:
                    P.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="{ch.get("color","#c0392b")}">{label}</text>')
                else:
                    P.append(f'<text x="{px}" y="{ty:.0f}" font-size="11" fill="{ch.get("color","#c0392b")}"><tspan font-weight="bold">{ch["label"]}</tspan>（{n} 站）→ {ch.get("short","")}</text>')
                ty += 21.2


    panel_bottom = ty if (points or chains) else ly
    ph = min(820, max(800, int(panel_bottom - 70 + 18)))
    S.append(f'<rect x="{px-12}" y="70" width="560" height="{ph}" fill="#fffdf5" stroke="#cbb"/>')
    S.extend(P)
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
    for m in re.finditer(r'<circle cx="([\d.-]+)" cy="([\d.-]+)" r="[\d.]+" fill="#[0-9a-fA-F]+" stroke="#fff"', svg):
        cx, cy = float(m.group(1)), float(m.group(2))
        if not (MX <= cx <= MX + MW and MY <= cy <= MY + MH):
            bad.append(("station-off-frame", f"({cx:.0f},{cy:.0f})", 0))
    print("wrote", out, os.path.getsize(out), "bytes | overflow:", bad if bad else "none")

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])))
