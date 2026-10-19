"""Collate the base text against the 四部叢刊(明成化本) and 四庫全書 witnesses (methodology spec stage S1).

Each book is reduced to bare CJK characters (punctuation and commentary removed, common 異體 folded),
aligned with difflib, and every remaining difference is attributed to the base entry it falls in.
Differences are *candidates* for textual error, not conclusions: an analyst classifies each one
(orthographic / scribal error / substantive variant) in the 校勘 ledger before it may be used as evidence.

Output: projects/shanhaijing/data/derived/collation.jsonl, collation-summary.md
"""
import difflib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "reference/shanhaijing/sources"
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
OUT = ROOT / "projects/shanhaijing/data/derived"

# Graphic variants folded before comparison (left -> right). Deliberately small and orthographic only;
# anything that could change meaning (e.g. 昆/崑, 虫/蟲) is NOT folded and will surface as a difference.
FOLD = str.maketrans({
    "于": "於", "隂": "陰", "揺": "搖", "摇": "搖", "黒": "黑", "黄": "黃", "爲": "為", "圗": "圖", "冝": "宜",
    "𩔖": "類", "荘": "莊", "吕": "呂", "峰": "峯", "花": "華", "飢": "饑", "群": "羣", "皃": "貌", "髪": "髮",
    "啓": "啟", "衆": "眾", "竝": "並", "㸃": "點", "敎": "教", "徧": "遍", "嵗": "歲", "鷄": "雞", "雞": "雞",
    "鴈": "雁", "牀": "床", "槃": "盤", "脩": "修", "迹": "跡", "蹟": "跡", "猨": "猿", "蝯": "猿", "横": "橫",
    "叅": "參", "冄": "冉", "囘": "回", "溼": "濕", "氷": "冰", "况": "況", "凢": "凡", "糓": "穀", "榖": "穀",
    "穀": "穀", "絶": "絕", "壊": "壞", "曽": "曾", "麤": "粗", "麁": "粗", "淵": "淵", "渊": "淵", "崐": "崑",
    "崘": "崙", "侖": "侖", "厯": "歷", "暦": "曆", "異": "異", "斵": "斲", "鵰": "雕", "彫": "雕", "蔕": "蒂",
    "毘": "毗", "姫": "姬", "鉅": "巨", "閒": "間", "効": "效", "衛": "衛", "衞": "衛", "敘": "敍", "叙": "敍",
})
CJK = re.compile(r"[㐀-鿿\U00020000-\U0003ffff]")
HEADER_NOISE = re.compile(r"欽定四庫全書|山海經[巻卷][一二三四五六七八九十]+|晉郭璞撰|郭氏傳|郭璞傳|"
                          r"[南西北東中大荒海內外]+經第[一二三四五六七八九十]+")


def norm(s: str) -> str:
    return "".join(CJK.findall(s)).translate(FOLD)


def witness_sbck(book_no: int) -> str:
    t = (SRC / "sbck-chenghua" / f"{book_no:02d}.txt").read_text()
    t = t.split("→", 1)[-1]                      # drop navigation header
    t = re.sub(r"〈[^〉]*〉", "", t)                 # commentary
    t = re.sub(r"景江安傅氏雙鑑樓藏明成化庚寅刊本", "", t)
    return HEADER_NOISE.sub("", norm(t))


def strip_templates(t: str, name: str) -> str:
    """Remove every {{name|...}} including nested templates inside it."""
    out, i, key = [], 0, "{{" + name
    while True:
        j = t.find(key, i)
        if j < 0:
            return "".join(out) + t[i:]
        out.append(t[i:j])
        depth, k = 0, j
        while k < len(t):
            if t.startswith("{{", k):
                depth += 1; k += 2
            elif t.startswith("}}", k):
                depth -= 1; k += 2
                if depth == 0:
                    break
            else:
                k += 1
        i = k


def witness_skqs(book_no: int) -> str:
    t = (SRC / "skqs" / f"{book_no:02d}.wiki").read_text()
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = strip_templates(t, "SK notes")
    t = re.sub(r"\{\{SK header[^}]*\}\}", "", t)
    t = re.sub(r"\{\{SK anchor\|([^}]*)\}\}", r"\1", t)   # anchors wrap real text (e.g. 又西六十里曰太華之山)
    t = re.sub(r"\{\{[^}]*\}\}", "", t)
    t = re.sub(r"山海經\s*(?:[巻卷][一二三四五六七八九十]+)?\s*$", "", t, flags=re.M)
    return HEADER_NOISE.sub("", norm(t))


def main():
    entries = [json.loads(l) for l in ENTRIES.open()]
    by_book = defaultdict(list)
    for e in entries:
        by_book[e["book_no"]].append(e)
    OUT.mkdir(parents=True, exist_ok=True)
    diffs, summary = [], []
    for b in range(1, 19):
        spans, base = [], ""
        for e in by_book[b]:
            n = norm(e["text"])
            spans.append((len(base), len(base) + len(n), e["id"]))
            base += n

        def entry_at(pos):
            for s, t, i in spans:
                if s <= pos < t or (pos == t and t == len(base)):
                    return i
            return spans[-1][2]

        row = {"book_no": b, "book": by_book[b][0]["book"], "base_chars": len(base)}
        for wname, wtext in (("sbck", witness_sbck(b)), ("skqs", witness_skqs(b))):
            sm = difflib.SequenceMatcher(None, base, wtext, autojunk=False)
            n = 0
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == "equal":
                    continue
                n += 1
                diffs.append({"entry_id": entry_at(i1), "witness": wname, "op": op,
                              "base": base[i1:i2], "witness_text": wtext[j1:j2],
                              "context": base[max(0, i1 - 6):i2 + 6], "status": "unclassified"})
            row[f"{wname}_chars"] = len(wtext)
            row[f"{wname}_ratio"] = round(sm.ratio(), 4)
            row[f"{wname}_diffs"] = n
        summary.append(row)
        print(row)

    with (OUT / "collation.jsonl").open("w") as f:
        for d in diffs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    lines = ["# Collation summary / 校勘概覽", "",
             "Generated by `tools/shj/collate.py`. Base = Wikisource 山海經; witnesses = 四部叢刊(明成化本), 四庫全書.",
             "Differences are unclassified candidates (status=unclassified) until reviewed in the 校勘 ledger.", "",
             "| # | 書 | base chars | 叢刊 similarity | 叢刊 diffs | 四庫 similarity | 四庫 diffs |",
             "|---|---|---|---|---|---|---|"]
    for r in summary:
        lines.append(f"| {r['book_no']:02d} | {r['book']} | {r['base_chars']} | {r['sbck_ratio']} | {r['sbck_diffs']} "
                     f"| {r['skqs_ratio']} | {r['skqs_diffs']} |")
    top = Counter(d["entry_id"] for d in diffs).most_common(15)
    lines += ["", "## Entries with most witness differences / 異文最多的條目", ""]
    lines += [f"- `{i}` — {c}" for i, c in top]
    (OUT / "collation-summary.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
