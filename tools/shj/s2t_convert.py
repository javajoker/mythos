#!/usr/bin/env python3
"""Simplified-to-Traditional conversion for draft/website prose (s2t).

Word-level longest match from vendored STPhrases.txt (OpenCC, Apache-2.0),
then character-level fallback from data/s2t-chars.tsv (project-maintained;
only chars actually appearing in the corpus need entries).

Characters inside fenced code blocks and existing traditional text are left
untouched automatically (already-traditional chars are not in the map).

Usage: python3 tools/shj/s2t_convert.py <file> [<file>...]
       python3 tools/shj/s2t_convert.py --check <file>   # report unmapped simplified chars
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHRASES = HERE / "data" / "STPhrases.txt"
CHARS = HERE / "data" / "s2t-chars.tsv"


def load_phrases():
    pairs = []
    for path in (PHRASES, HERE / "data" / "s2t-domain.tsv"):
        if not path.exists():
            continue
        for line in path.open(encoding="utf-8"):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            src, dst = parts[0], parts[1].split(" ")[0]
            if src != dst:
                pairs.append((src, dst))
    pairs.sort(key=lambda p: -len(p[0]))
    # 首字索引：每個位置只試同首字的短語
    by_first = {}
    for src, dst in pairs:
        by_first.setdefault(src[0], []).append((src, dst))
    return by_first


def load_chars():
    m = {}
    if CHARS.exists():
        for line in CHARS.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            a, b = line.split("\t")
            m[a] = b
    return m


# 轉換後修正規則：專名保護與字形統一
POST_RULES = [
    ("後稷", "后稷"), ("後羿", "后羿"), ("後土", "后土"), ("夏後", "夏后"),
    ("後啟", "后啟"), ("王後", "王后"), ("皇後", "皇後"), ("後妃", "后妃"),
    ("後夔", "后夔"),
    ("公裏", "公里"),  # 「里外→裏外」短語誤傷「公里外」；全書統一作公里
    ("裡", "裏"),  # 統一為古典字形（裏為正體，裡為臺灣標準變體）
    ("爲", "為"), ("羣", "群"), ("峯", "峰"),  # 統一常用體（僅作用於敘述行，原文引用行被跳過）
]


def convert(text, phrases, chars, missing):
    out = []
    i = 0
    n = len(text)
    while i < n:
        hit = None
        for src, dst in phrases.get(text[i], ()):
            if text.startswith(src, i):
                hit = dst
                i += len(src)
                break
        if hit is None:
            c = text[i]
            if c in chars:
                hit = chars[c]
            else:
                hit = c
                if missing is not None and "一" <= c <= "鿿":
                    missing.add(c)
            i += 1
        out.append(hit)
    result = "".join(out)
    for a, b in POST_RULES:
        result = result.replace(a, b)
    return result


def main():
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"]
    phrases = load_phrases()
    chars = load_chars()
    for f in files:
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        missing = set() if check else None
        # 逐行轉換：原文引用塊（> 開頭）與代碼行不動
        lines = text.split("\n")
        converted = []
        in_code = False
        in_quote = False
        for ln in lines:
            if ln.strip().startswith("```"):
                in_code = not in_code
                converted.append(ln)
                continue
            if "【原文】" in ln or "【經文原文】" in ln:
                in_quote = True
            elif not ln.strip():
                in_quote = False
            if in_code or in_quote or (ln.lstrip().startswith(">") and in_quote):
                converted.append(ln)
            else:
                converted.append(convert(ln, phrases, chars, missing))
        out = "\n".join(converted)
        if check:
            # 只報「簡化字特有字形」（出現在 phrases 來源側或已知會被轉換的）
            need = sorted(c for c in missing if any(c in s for lst in phrases.values() for s, _ in lst))
            print(p.name, "uncovered chars:", "".join(need) if need else "（無）")
        else:
            p.write_text(out, encoding="utf-8")
            print("converted", p)


if __name__ == "__main__":
    main()
