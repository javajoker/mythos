"""Render the section-level anchors (judgment records, prompt anchor-1.0) as a report and a map of the period.

Input: projects/shanhaijing/data/derived/era/anchors.jsonl (one record per section: candidates with dimension
scores, evidence and reasons), frame.jsonl (routes in li), data/era/regions.jsonl and coastlines-present.json.
Output: data/derived/era/anchors.md and anchor-map.svg. Each lead candidate's route is drawn from its start point at
its li scale; rivals are listed, and far rivals of 西次三經 are marked with the scale they would need.
"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERA = ROOT / "projects/shanhaijing/data/derived/era"
BASE = ROOT / "projects/shanhaijing/data/era"
ORIGIN = (34.7, 113.6)
DIMS = ["direction", "route_scale", "terrain", "waters", "resources", "fauna"]
DIM_ZH = {"direction": "方位", "route_scale": "路線與比例尺", "terrain": "地形外觀", "waters": "水系", "resources": "物產",
          "fauna": "動物"}
FAR = {"anchor:pamir_badakhshan": (37.5, 72.0), "anchor:armenian_highlands": (39.5, 43.0),
       "anchor:ethiopian_highlands": (9.0, 39.0), "anchor:egypt_giza": (30.0, 31.2), "anchor:alborz": (36.0, 52.0),
       "anchor:upper_indus_harappa": (31.0, 72.0)}


def jl(p):
    return [json.loads(l) for l in Path(p).open() if l.strip()]


def route(start, scale, pts):
    out = []
    for x, y in pts:
        lat = start[0] + y * scale / 111.0
        lon = start[1] + x * scale / (111.0 * math.cos(math.radians(lat)))
        out.append((lat, lon))
    return out


def main():
    anchors = jl(ERA / "anchors.jsonl")
    frame = defaultdict(list)
    for f in jl(ERA / "frame.jsonl"):
        frame[f["section"]].append((f["x_li"], f["y_li"]))
    coast = json.loads((BASE / "coastlines-present.json").read_text())
    # ---- report ---------------------------------------------------------------------------------------------------
    L = ["# 西、東、中山經的篇段錨點 / Section anchors for the Western, Eastern and Central Mountain Classics", "",
         "> 判斷：大模型推理（`anchor-1.0`），**未遮蔽**：許多書中名稱延續為今名（渭、洛、江、漢、華山…），所以洩漏風險高；"
         "名稱的延續**不作為證據**，下列理由只用描述、水系結構、方位與物產。所有錨點為**暫定**，待 T-V07 以遮蔽輸入重判。",
         "> Unmasked LLM judgments (anchor-1.0); provisional until re-judged on masked input (T-V07). Name continuity is never evidence.", "",
         "- 方位：書中的西南、西北、東南、東北不是正 45°，容許偏移（±67.5°）。/ Diagonal bearings allow offset.",
         "- 山與水依外觀：山可以是沙丘、貝殼堤、方山，水可以是湖、沼澤、海灣（R1、R3）。/ Outlook readings.",
         "- 比例尺：中次六經（790 里 ≈ 150 公里）、西山經之首（2,957 里 ≈ 650 公里）、東山經之首（3,500 里 ≈ 950 公里）"
         "得出每里約 0.2–0.3 公里（路程里，不是直線）。/ Scale about 0.2–0.3 km per li of route.",
         "- 權重：方位 0.4、路線與比例尺 0.4、地形 1.0、水系 1.0、物產 0.8、動物 0.8；矛盾扣分上限 0.5。/ Weights.", "",
         "## 總表 / Summary", "",
         "| 經 | 篇 | 領先錨點 / lead | 分數 | 次位 / runner-up | 差距 | 洩漏風險 |", "|---|---|---|---|---|---|---|"]
    for a in anchors:
        lead = next(c for c in a["candidates"] if c["cand"] == a["lead"])
        ru = [c for c in sorted(a["candidates"], key=lambda c: -c["total"]) if c["cand"] != a["lead"]]
        L.append(f"| {a['book']} | {a['section']} | {lead['label']} | {lead['total']} | "
                 f"{(ru[0]['label'] + '（' + str(ru[0]['total']) + '）') if ru else '—'} | {a['margin'] if a['margin'] is not None else '—'} | {a['leakage_risk']} |")
    for a in anchors:
        L += ["", f"## {a['book']}・{a['section']}", ""]
        for c in sorted(a["candidates"], key=lambda c: -c["total"]):
            mark = "**領先 / lead**" if c["cand"] == a["lead"] else "對立 / rival"
            L += [f"### {c['label']}（{c['region']}，{mark}，總分 {c['total']}）", "",
                  f"- 起點 {c['start']}、比例尺 {c['scale_km_per_li']} 公里／里；年代：{c['era']}" + (f"；{c['note']}" if c.get("note") else ""),
                  "", "| 維度 | 分數 | 矛盾 | 證據 | 理由 |", "|---|---|---|---|---|"]
            for k in DIMS:
                v = c["dims"][k]
                L.append(f"| {DIM_ZH[k]} | {v['score']} | {'是' if v['contradiction'] else ''} | "
                         f"{' '.join('`' + e + '`' for e in v['evidence'])} | {v['reason']} |")
            L.append("")
    (ERA / "anchors.md").write_text("\n".join(L) + "\n")
    # ---- map ------------------------------------------------------------------------------------------------------
    W, H = 1400, 1420

    def panel(lat0, lat1, lon0, lon1, x0, y0, w):
        k = w / (lon1 - lon0)
        h = (lat0 - lat1) * k
        return (lambda la, lo: (x0 + (lo - lon0) * k, y0 + (lat0 - la) * k)), h

    def poly(f, pts):
        return "M" + " L".join(f"{f(a, b)[0]:.1f},{f(a, b)[1]:.1f}" for a, b in pts) + " Z"

    S = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="11">',
         f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
         '<text x="12" y="24" font-size="17" font-weight="bold">西、東、中山經的篇段錨點（暫定，前 4000–前 2000 年）/ Section anchors (provisional)</text>',
         '<text x="12" y="44" fill="#555">實線：各篇領先錨點的路線（由各段方位與里數畫出，比例尺見報告）；★ 中原原點；紫點：西次三經的遠方對立候選與所需比例尺。'
         '海岸線為今日簡化輪廓；窗口內渤海西岸、蘇北海岸、波斯灣頂端更深入內陸（見 era-world.md）。</text>']
    for (lat0, lat1, lon0, lon1, x0, y0, w, title) in [(52, -2, 20, 128, 12, 60, 1376, "歐亞與非洲 / wide view"),
                                                          (43, 20, 96, 126, 12, 770, 980, "東亞 / East Asia")]:
        f, h = panel(lat0, lat1, lon0, lon1, x0, y0, w)
        S.append(f'<svg x="{x0}" y="{y0}" width="{w}" height="{h:.0f}" viewBox="{x0} {y0} {w} {h:.0f}">'
                 f'<rect x="{x0}" y="{y0}" width="{w}" height="{h:.0f}" fill="#dce8f1"/>')
        S.append('<g fill="#f3efe4" stroke="#a89f88" stroke-width="0.6">' + "".join(f'<path d="{poly(f, v)}"/>' for v in coast["land"].values()) + "</g>")
        S.append('<g fill="#dce8f1" stroke="#a89f88" stroke-width="0.4">' + "".join(f'<path d="{poly(f, v)}"/>' for v in coast["water"].values()) + "</g>")
        colours = {"西山經": "#b5542d", "東山經": "#2d6cb5", "中山經": "#2d8a4a"}
        for a in anchors:
            c = next(c for c in a["candidates"] if c["cand"] == a["lead"])
            pts = route(c["start"], c["scale_km_per_li"], frame[a["section"]])
            path = " L".join(f"{f(la, lo)[0]:.1f},{f(la, lo)[1]:.1f}" for la, lo in pts)
            S.append(f'<path d="M{path}" fill="none" stroke="{colours[a["book"]]}" stroke-width="2.2" opacity="0.85">'
                     f'<title>{a["section"]}: {c["label"]} ({c["total"]})</title></path>')
            ex, ey = f(*pts[-1])
            sx, sy = f(*pts[0])
            S.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.5" fill="{colours[a["book"]]}"/>')
            if title.startswith("東亞"):
                S.append(f'<text x="{ex + 3:.1f}" y="{ey - 3:.1f}" font-size="10" fill="{colours[a["book"]]}">{a["section"]}</text>')
        for a in anchors:
            for c in a["candidates"]:
                if c["cand"] in FAR and title.startswith("歐亞"):
                    x, y = f(*FAR[c["cand"]])
                    S.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#7a4cb5" opacity="0.8"/>'
                             f'<text x="{x + 7:.1f}" y="{y + 4:.1f}" font-size="10" fill="#5a2f8f">{c["label"].split("（")[0]}（{a["section"]}，{c["total"]}，需 {c["scale_km_per_li"]} 公里／里）</text>')
        ox, oy = f(*ORIGIN)
        S.append(f'<text x="{ox - 6:.1f}" y="{oy + 5:.1f}" font-size="15" fill="#d4a017">★</text>')
        S.append(f'<text x="{x0 + 6}" y="{y0 + 16}" font-size="12" font-weight="bold">{title}</text></svg>')
    S.append('<g font-size="11"><rect x="1010" y="790" width="12" height="4" fill="#b5542d"/><text x="1028" y="796">西山經 West</text>'
             '<rect x="1010" y="810" width="12" height="4" fill="#2d6cb5"/><text x="1028" y="816">東山經 East</text>'
             '<rect x="1010" y="830" width="12" height="4" fill="#2d8a4a"/><text x="1028" y="836">中山經 Central</text>'
             '<circle cx="1016" cy="852" r="5" fill="#7a4cb5"/><text x="1028" y="856">遠方對立候選 far rivals</text>'
             '<text x="1010" y="880" fill="#555">路線只示走向與長度（地圖讀法）。</text>'
             '<text x="1010" y="898" fill="#555">圓點 = 各篇起點。</text></g>')
    S.append("</svg>")
    (ERA / "anchor-map.svg").write_text("\n".join(S))
    print(f"{len(anchors)} sections", file=sys.stderr)


if __name__ == "__main__":
    main()
