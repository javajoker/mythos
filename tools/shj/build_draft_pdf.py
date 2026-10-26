#!/usr/bin/env python3
"""Build the draft-v2 PDF book: pandoc (md→docx) + LibreOffice headless (docx→pdf).

No TeX/typst dependency. Assembles cover + 18 books from deliverables/draft-v2/,
converts embedded SVG map references to PNG (qlmanage), symlinks local images,
then runs pandoc and soffice.

Usage: python3 tools/shj/build_draft_pdf.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / "projects/shanhaijing/deliverables/draft-v2"
BUILD = DRAFT / "_pdf_build"
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
OUT = DRAFT / "shanhaijing-draft-v2.pdf"
SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"

COVER = """---
title: "山海經時代假想推理草稿"
subtitle: "五臧山經 × 海外海內大荒：現實世界映射（競爭假說集，4000–1000 BCE）"
author: "Mythos 項目（LLM 識別與映射＋程序結構化；全部 proposed_pending_review）"
date: "2026-10-26"
---

# 山海經時代假想推理草稿（draft-v2 白話配圖版）

本書為《山海經》18 卷的白話解讀草稿：每條目含原文、白話解讀、配圖（實拍照片）與未決項。
全部現實對應為競爭假說，等待逐項覆核。地圖為推理示意（簡化海岸線）。

"""


def svg_to_png(svg_rel):
    src = (DRAFT / svg_rel).resolve()
    if not src.exists():
        print("missing svg:", src)
        return None
    name = src.stem + ".png"
    dest = BUILD / "images" / name
    if not dest.exists():
        subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", str(dest.parent), str(src)],
                       capture_output=True)
        produced = dest.parent / (src.stem + ".svg.png")
        if produced.exists():
            produced.rename(dest)
    return "images/" + name if dest.exists() else None


def main():
    (BUILD / "images").mkdir(parents=True, exist_ok=True)
    parts = [COVER]
    for md in sorted(DRAFT.glob("book-*.md")):
        s = md.read_text(encoding="utf-8")

        def maprep(m):
            png = svg_to_png(m.group(2))
            return f'![{m.group(1)}]({png})' if png else m.group(0)
        s = re.sub(r"!\[([^\]]*)\]\(([^)]*-map\.svg)\)", maprep, s)
        parts.append(s)
    (BUILD / "book.md").write_text(COVER[COVER.find("---"):] and "\n\n".join(parts), encoding="utf-8")
    for img in DRAFT.glob("images/*"):
        dest = BUILD / "images" / img.name
        if not dest.exists():
            dest.symlink_to(img)
    print("assembled", len(parts) - 1, "books")
    r = subprocess.run(["pandoc", "book.md", "-o", "book.docx", "--resource-path=."],
                       cwd=BUILD, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:])
        return r.returncode
    r = subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "book.docx"],
                       cwd=BUILD, capture_output=True, text=True)
    if r.returncode or not (BUILD / "book.pdf").exists():
        print(r.stderr[-2000:])
        return 1
    (BUILD / "book.pdf").replace(OUT)
    print("PDF written:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
