#!/usr/bin/env python3
"""Embed scroll/book maps into draft-v2 markdown (robust heading walk-up).

Books 1–5: one map per sub-classic, inserted above the heading that carries the
section's first entry (SHJ-<bk>-<sec>-001). Books 6–18: patch map above the
heading carrying SHJ-<bk>-1-001. Idempotent.

Usage: python3 tools/shj/embed_draft_maps.py
"""
import re
from pathlib import Path

DRAFT = Path(__file__).resolve().parents[2] / "projects/shanhaijing/deliverables/draft-v2"
ADJ_REL = "../../data/derived/era/adaptation"
PREFIX = {"01": ("nanci", 3), "02": ("xici", 4), "03": ("beici", 3), "04": ("dongci", 4), "05": ("zhongci", 13)}


def insert_before_heading(lines, needle, payload):
    for i, line in enumerate(lines):
        if needle in line:
            j = i
            while j > 0 and not lines[j].startswith("### "):
                j -= 1
            lines[j:j] = [payload, ""]
            return True
    return False


def main():
    for md in sorted(DRAFT.glob("book-*.md")):
        bk = re.search(r"book-(\d+)-", md.name).group(1)
        s = md.read_text(encoding="utf-8")
        if "-map.svg" in s:
            print(md.name, "already has maps, skip")
            continue
        lines = s.split("\n")
        count = 0
        jobs = []
        if bk in PREFIX:
            prefix, nsec = PREFIX[bk]
            for sec in range(1, nsec + 1):
                if sec == 13:
                    continue
                slug = f"{prefix}{sec}"
                jobs.append((f"SHJ-{bk}-{sec}-001", f"![{slug} 地圖]({ADJ_REL}/{slug}-map.svg)"))
        else:
            jobs.append((f"SHJ-{bk}-1-001", f"![本卷補丁地圖]({ADJ_REL}/book{bk}-map.svg)"))
        # 從後往前插入，避免行號位移
        for needle, payload in reversed(jobs):
            if insert_before_heading(lines, needle, payload):
                count += 1
            else:
                print(md.name, "anchor missing:", needle)
        md.write_text("\n".join(lines), encoding="utf-8")
        print(md.name, f"embedded {count} map(s)")


if __name__ == "__main__":
    main()
