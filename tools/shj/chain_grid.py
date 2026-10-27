#!/usr/bin/env python3
"""Generic per-classic station grid builder (Zhongshan set).

Reads a spec JSON: {"stations": [...], "legs": [[bearing_deg, li] or null...],
"anchor": {"index": i, "lat": ..., "lon": ...}, "meta": {...}, "out": path}.
Expands positions at 0.35/0.385/0.42 km/li. Arithmetic only — no semantics.
"""
import json, math, sys

def main(spec_path):
    spec = json.load(open(spec_path))
    stations, legs = spec["stations"], spec["legs"]
    ai, anchor = spec["anchor"]["index"], (spec["anchor"]["lat"], spec["anchor"]["lon"])
    scales = (0.35, 0.385, 0.42)
    records = {}
    cum = 0
    cum_list = [0]
    for leg in legs[1:]:
        cum += leg[1]
        cum_list.append(cum)
    for scale in scales:
        cumkm = [(0.0, 0.0)]
        for leg in legs[1:]:
            d = leg[1] * scale
            rad = math.radians(leg[0])
            cumkm.append((cumkm[-1][0] + d * math.cos(rad), cumkm[-1][1] + d * math.sin(rad)))
        an, ae = cumkm[ai]
        for i, st in enumerate(stations):
            dn, de = cumkm[i][0] - an, cumkm[i][1] - ae
            lat = anchor[0] + dn / 110.9
            lon = anchor[1] + de / (111.3 * math.cos(math.radians(anchor[0])))
            rec = records.setdefault(st, {"station": st, "order": i + 1, "grid": {}})
            rec["grid"][str(scale)] = {"lat": round(lat, 2), "lon": round(lon, 2)}
    bearname = spec.get("bearnames", {})
    for i, st in enumerate(stations):
        rec = records[st]
        if legs[i]:
            rec["leg"] = {"bearing": bearname.get(str(legs[i][0]), str(legs[i][0])), "li": legs[i][1]}
        rec["cum_li_from_start"] = cum_list[i]
        # G-3：網格＝否定工具——輸出經緯帶（三檔極值包絡）而非單點
        lats = [records[st]["grid"][str(s)]["lat"] for s in scales]
        lons = [records[st]["grid"][str(s)]["lon"] for s in scales]
        rec["band"] = {"lat_min": round(min(lats), 2), "lat_max": round(max(lats), 2),
                       "lon_min": round(min(lons), 2), "lon_max": round(max(lons), 2),
                       "note": "網格僅作否定檢核帶（G-3）；帶內不構成定位證據"}
    with open(spec["out"], "w") as f:
        f.write(json.dumps(spec["meta"], ensure_ascii=False) + "\n")
        for st in stations:
            f.write(json.dumps(records[st], ensure_ascii=False) + "\n")
    for st in stations:
        g = records[st]["grid"]["0.385"]
        print(f"{records[st]['order']:2d} {st:8s} {g['lat']:6.2f} {g['lon']:7.2f}")

if __name__ == "__main__":
    main(sys.argv[1])
