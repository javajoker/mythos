#!/usr/bin/env python3
"""Build masked (blind) re-judgment packs for T-RT05.

For each sampled chain segment, emits a markdown pack containing ONLY:
  - the verbatim original text of each entry (from working-text.jsonl),
  - a neutral entity checklist (names/types as extracted),
stripped of: classic/chain names, station order, anchors, mileage grids,
current mapping candidates, and any modern-place hints.

The LLM judge reads the pack and locates the segment independently; the
comparison with current mappings is a separate step (manual or reviewer).

Usage:
  python3 tools/shj/blind_pack.py --pack xici1:SHJ-02-1-001,SHJ-02-1-013,SHJ-02-1-014 \
      [--pack nanci2:SHJ-01-2-007] [--out projects/shanhaijing/data/derived/review/blind]
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHJ = ROOT / "projects/shanhaijing"
WORKING = SHJ / "data/derived/working-text.jsonl"
EXTRACTION = SHJ / "data/derived/extraction"

BANNER = (
    "以下為一段來源不明的古代地理記錄（已遮蔽所屬經卷、站序、錨點與一切現代地名提示）。"
    "請僅依據原文的方位、水系（出/流/注/臨/望）、物產、動植物與人文描述，"
    "獨立判斷每一條記錄最可能位於現實世界哪個山系/區域（給出經緯度範圍與現實山名），"
    "並逐條列出推理。不要假設它屬於任何已知古籍篇章。\n"
    "**重要紀律**：不得使用名稱匹配——即不得因文本中的山川名與某個現代/歷史地名同名、音近、"
    "或有文獻比定傳統而定位（例如不可說「涇水出焉所以是六盤山」）；後世可能借用本文命名現實地理。"
    "只能用性狀（地貌/氣候/物候）、水系拓撲（流向與匯流關係，不涉及水名所指）、方位、里程、"
    "人文風物資源作證。水系名僅作為結構節點（A 注于 B），不關心它在後世叫什麼。\n"
)

# 經卷名與鏈首標記：盲測包必須剔除，否則洩漏所屬經卷
LEAK_PATTERNS = [
    (r"《[^》]+》", ""),
    (r"^[东西南北中]山經[^，。]*?之首[，]?", ""),
    (r"^[东西南北中]次[一二三四五六七八九十]+經之首[，]?", ""),
    (r"^又[东西南北中]次[一二三四五六七八九十]+經之首[，]?", ""),
    (r"^凡[^，。]*?之首，自[^，。]*?以至[^，。]*?，凡[0-9一二三四五六七八九十百]+山，[0-9一二三四五六七八九十百千萬]+里。", "[卷末里程總結已遮蔽]"),
    (r"^[^，。曰]{0,10}之首[，]", ""),  # 通用鏈首標記（如「荊山之首，」「之首，」）
]


def mask_text(text):
    import re
    for pat, rep in LEAK_PATTERNS:
        text = re.sub(pat, rep, text)
    return text.strip("，。、 ") or text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", action="append", required=True,
                    help="label:ENTRY1,ENTRY2,...（可多個 --pack）")
    ap.add_argument("--out", default=str(SHJ / "data/derived/review/blind"))
    args = ap.parse_args()

    working = {}
    for line in WORKING.open(encoding="utf-8"):
        row = json.loads(line)
        if row.get("entry_id"):
            working[row["entry_id"]] = row.get("text") or ""

    entities = {}
    for path in EXTRACTION.glob("book-*.jsonl"):
        for line in path.open(encoding="utf-8"):
            row = json.loads(line)
            entities[row["entry"]] = row.get("entities", [])

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for pack in args.pack:
        label, ids = pack.split(":", 1)
        ids = [i.strip() for i in ids.split(",") if i.strip()]
        parts = [f"# 遮蔽重判測試包：{label}（{len(ids)} 條）\n", BANNER]
        for i, eid in enumerate(ids, 1):
            text = working.get(eid)
            if text is None:
                parts.append(f"## 記錄 {i}\n\n（找不到條目 {eid}）\n")
                continue
            text = mask_text(text)
            ents = "、".join(e[0] for e in entities.get(eid, []))
            parts.append(f"## 記錄 {i}\n\n> {text}\n\n實體清單：{ents}\n")
        out = out_dir / f"{label}-blind-pack.md"
        out.write_text("\n".join(parts), encoding="utf-8")
        print("wrote", out)


if __name__ == "__main__":
    main()
