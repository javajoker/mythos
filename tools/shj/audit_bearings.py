# -*- coding: utf-8 -*-
"""五臧山經 26 鏈「嚴格走向」審計 v3（adapt-audit-2026-10-29）。

兩層檢驗：
A. 站位 vs 聲明腿（specs/<slug>.json legs 或 station-grid 內腿記錄）：
   每腿實際方位（fit_coords 優先、缺則退回網格）是否落在聲明方位 ±22.5° 容差錐。
B. 聲明腿 vs 原文腿（working-text.jsonl 逐條解析）：腿數、逐腿方位/里數是否一致
   （不一致＝spec 腿被改動過，屬校勘留痕點）。
"""
import json
import math
import re
from pathlib import Path

SHJ = Path(__file__).resolve().parents[2] / "projects/shanhaijing"
ADJ = SHJ / "data/derived/era/adaptation"
WORK = SHJ / "data/derived/working-text.jsonl"

BOOK_SLUGS = {"01": (3, "nanci"), "02": (4, "xici"), "03": (3, "beici"),
              "04": (4, "dongci"), "05": (12, "zhongci")}
DIRS = {"北": 0, "東北": 45, "東": 90, "東南": 135, "南": 180, "西南": 225, "西": 270, "西北": 315}
CN_NUM = {"一": 1, "二": 2, "兩": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
LEG_RE = re.compile(
    r"(?:又)?(東北|東南|西北|西南|[東南西北])(?:山行|水行)?([一二兩三四五六七八九十百千]+)里"
    r"(?:[，,](?:山行|水行|流沙)([一二兩三四五六七八九十百千]+)里)?"
    r"(?:[，,]?流沙(?:行)?([一二兩三四五六七八九十百千]+)里)?")


def cn2int(s):
    if not s:
        return 0
    total = cur = 0
    for ch in s:
        if ch in ("十", "百", "千"):
            unit = {"十": 10, "百": 100, "千": 1000}[ch]
            cur = max(cur, 1) * unit
            total += cur
            cur = 0
        elif ch in CN_NUM:
            cur = CN_NUM[ch]
    return total + cur


def text_legs(book, sub):
    out = []
    pref = f"SHJ-{book}-{sub}-"
    for line in open(WORK, encoding="utf-8"):
        r = json.loads(line)
        eid = r.get("entry_id") or ""
        if not eid.startswith(pref) or r.get("kind") not in ("aligned", "fuzzy"):
            continue
        m = LEG_RE.search(r.get("text") or "")
        if m:
            out.append((eid, DIRS[m.group(1)], cn2int(m.group(2)) + cn2int(m.group(3))))
    return out


def bearing(p, q):
    dn = (q[1] - p[1]) * 110.9
    de = (q[0] - p[0]) * 111.3 * math.cos(math.radians((p[1] + q[1]) / 2))
    return math.degrees(math.atan2(de, dn)) % 360


grand_bad = grand_mismatch = 0
for book, (nsub, slugp) in BOOK_SLUGS.items():
    for sub in range(1, nsub + 1):
        slug = f"{slugp}{sub}"
        # 聲明腿：grid spec 優先，否則 station-grid 內腿記錄
        legs_decl = None
        gspec = ADJ / "specs" / f"{slug}.json"
        gridrecs = {}
        gfile = ADJ / f"{slug}-station-grid.jsonl"
        if gfile.exists():
            for line in open(gfile, encoding="utf-8"):
                r = json.loads(line)
                if "station" in r:
                    gridrecs[r["order"]] = r
        if gspec.exists():
            g = json.load(open(gspec, encoding="utf-8"))
            legs_decl = [tuple(l) if l else None for l in g["legs"]]
            n_st = len(g["stations"])
        elif gridrecs:
            n_st = max(gridrecs)
            legs_decl = []
            for i in range(1, n_st + 1):
                lg = gridrecs.get(i, {}).get("leg")
                legs_decl.append((DIRS.get(lg["bearing"], -1), lg["li"]) if lg else None)
        else:
            print(f"{slug}: 無 spec 亦無 grid"); continue

        # 站位
        pos = {}
        mspec = ADJ / "specs" / f"{slug}-map.json"
        if mspec.exists():
            for k, v in json.load(open(mspec, encoding="utf-8")).get("fit_coords", {}).items():
                pos[int(k)] = tuple(v)
        for o, r in gridrecs.items():
            if o not in pos:
                pos[o] = (r["grid"]["0.385"]["lon"], r["grid"]["0.385"]["lat"])

        # A 層
        breaks = set()
        if gspec.exists():
            breaks = set(json.load(open(gspec, encoding="utf-8")).get("breaks", []))
        bad = []
        for i in range(2, n_st + 1):
            if i in breaks:  # 文本層累拼接點（多源接合）——不作走向約束（發起人 2026-10-29 裁定口徑：分段承認）
                continue
            dl = legs_decl[i - 1] if i - 1 < len(legs_decl) else None
            if not dl or dl[0] < 0:
                continue
            p, q = pos.get(i - 1), pos.get(i)
            if not p or not q:
                bad.append((i, "站位缺失"))
                continue
            real = bearing(p, q)
            diff = (real - dl[0] + 180) % 360 - 180
            if abs(diff) > 22.5:
                bad.append((i, f"經文{dl[0]}° 實際{real:.1f}° 偏差{diff:+.1f}°（{dl[1]}里）"))
        # B 層
        tl = text_legs(book, sub)
        mism = []
        decl_legs = [l for l in legs_decl[1:] if l]
        if len(decl_legs) != len(tl):
            mism.append(f"腿數不合：聲明{len(decl_legs)} vs 文本{len(tl)}")
        for k, (d, t) in enumerate(zip(decl_legs, tl)):
            if d[0] != t[1] or d[1] != t[2]:
                mism.append(f"腿{k+2}（{t[0]}）：聲明{d[0]}°/{d[1]}里 vs 文本{t[1]}°/{t[2]}里")
        grand_bad += len(bad)
        grand_mismatch += len(mism)
        print(f"{slug}: 站 {n_st} A層違背 {len(bad)}；B層聲明腿vs文本不符 {len(mism)}")
        for i, msg in bad:
            print(f"    leg→站{i}: {msg}")
        for msg in mism[:6]:
            print(f"    B: {msg}")
print(f"\n=== A層總違背 {grand_bad}；B層總不符 {grand_mismatch} ===")
