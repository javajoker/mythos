#!/usr/bin/env python3
"""Build the draft-v2 PDF book via pandoc + tectonic.

Assembles cover + TOC + 18 books from deliverables/draft-v2/, converts embedded
SVG map references to PNG (qlmanage), rewrites paths for the build dir, and runs
pandoc with a CJK-capable engine.

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
OUT = ROOT / "projects/shanhaijing/deliverables/shanhaijing-draft-v2.pdf"


def svg_to_png(svg_rel):
    """Convert adaptation SVG to PNG inside build dir; return relative name."""
    src = (DRAFT / svg_rel).resolve()
    if not src.exists():
        print("missing svg:", src)
        return None
    name = src.stem + ".png"
    dest = BUILD / "images" / name
    if not dest.exists():
        r = subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", str(dest.parent), str(src)],
                           capture_output=True, text=True)
        produced = dest.parent / (src.stem + ".svg.png")
        if produced.exists():
            produced.rename(dest)
    return "images/" + name if dest.exists() else None


def main():
    (BUILD / "images").mkdir(parents=True, exist_ok=True)
    books = sorted(DRAFT.glob("book-*.md"))
    cover = f"""---
title: "山海經時代假想推理草稿"
subtitle: "五臧山經 × 海外海內大荒：現實世界映射（競爭假說集，4000–1000 BCE）"
author: "Mythos 項目（LLM 識別與映射＋程序結構化；全部 proposed_pending_review）"
date: "2026-10-26"
CJKmainfont: "PingFang SC"
mainfont: "PingFang SC"
geometry: margin=2.2cm
toc: false
---

# 山海經時代假想推理草稿（draft-v2 白話配圖版）

本書為《山海經》18 卷的白話解讀草稿：每條目含原文、白話解讀、配圖（實拍照片）與未決項。
全部現實對應為競爭假說，等待逐項覆核。地圖為推理示意（簡化海岸線）。

\\newpage
"""
    parts = [cover]
    for md in books:
        s = md.read_text(encoding="utf-8")
        # rewrite image paths: images/x -> _pdf_build relative is fine if we build inside DRAFT... we build in BUILD
        s = re.sub(r"!\[([^\]]*)\]\(images/([^)]+)\)", r"![\1](images/\2)", s)
        # convert SVG map refs to PNG
        def maprep(m):
            rel = m.group(2)
            src = (DRAFT / rel).resolve()
            png = svg_to_png(str(Path(rel)))
            return f'![{m.group(1)}]({png})' if png else m.group(0)
        s = re.sub(r"!\[([^\]]*)\]\(([^)]*-map\.svg)\)", maprep, s)
        parts.append(s)
        parts.append("\n\\newpage\n")
    full = "\n".join(parts)
    (BUILD / "book.md").write_text(full, encoding="utf-8")
    # link local images into build dir
    for img in DRAFT.glob("images/*"):
        dest = BUILD / "images" / img.name
        if not dest.exists():
            dest.symlink_to(img)
    print("assembled", len(books), "books")
    r = subprocess.run(["pandoc", "book.md", "-o", str(OUT), "--pdf-engine=tectonic",
                        "-V", "CJKmainfont=PingFang SC", "--toc", "--toc-depth=1",
                        "-V", "geometry:margin=2.2cm"],
                       cwd=BUILD, capture_output=True, text=True)
    print(r.returncode, r.stderr[-3000:] if r.returncode else "PDF written: " + str(OUT))
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
