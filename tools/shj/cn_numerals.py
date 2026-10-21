"""Chinese numeral parsing for classical texts (e.g. 三百八十里, 百八十里, 一萬七千五百一十七里)."""
from __future__ import annotations

DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "兩": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9}
UNITS = {"十": 10, "百": 100, "千": 1000}
BIG = {"萬": 10_000}
NUMERAL_CHARS = set(DIGITS) | set(UNITS) | set(BIG)


def parse(s: str) -> int | None:
    """Parse a Chinese numeral string. Returns None if it contains non-numeral characters."""
    if not s or any(c not in NUMERAL_CHARS for c in s):
        return None
    total, section, digit = 0, 0, None
    for c in s:
        if c in DIGITS:
            digit = DIGITS[c]
        elif c in UNITS:
            section += (1 if digit is None else digit) * UNITS[c]
            digit = None
        else:  # 萬
            section += digit or 0
            total += (section or 1) * BIG[c]
            section, digit = 0, None
    return total + section + (digit or 0)


if __name__ == "__main__":
    for s, want in [("三百八十里"[:-1], 380), ("百八十", 180), ("一萬七千五百一十七", 17517),
                    ("二千九百五十", 2950), ("十", 10), ("十九", 19), ("四十", 40), ("三", 3)]:
        assert parse(s) == want, (s, parse(s), want)
    print("ok")
