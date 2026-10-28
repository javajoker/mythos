#!/usr/bin/env python3
"""One-shot regression: rebuild KG layers, validate, re-render all maps with
overflow audit, rebuild draft, zero-omission checks.

All builders are deterministic and idempotent; this script rewrites derived
files in place. Exit non-zero on any failure.

Usage: python3 tools/shj/check_all.py
"""
import json
import re
import subprocess
import sys
import glob as g
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHJ = ROOT / "projects/shanhaijing"
ADJ = SHJ / "data/derived/era/adaptation"
FAIL = []


def step(name, cmd, grep_bad=None):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    bad = r.returncode != 0
    if grep_bad and re.search(grep_bad, out):
        bad = True
    print(("FAIL" if bad else " ok "), name)
    if bad:
        FAIL.append((name, out[-1500:]))


def main():
    # 1. KG 層（順序依賴）
    step("kg_v1_assemble", ["python3", "tools/shj/kg_v1_assemble.py"])
    step("kg_readings_build", ["python3", "tools/shj/kg_readings_build.py"])
    step("kg_assoc_ded_build", ["python3", "tools/shj/kg_assoc_ded_build.py"])
    step("kg_framework_build", ["python3", "tools/shj/kg_framework_build.py"])
    step("kg_edges_build", ["python3", "tools/shj/kg_edges_build.py"])
    step("kg_validate", ["python3", "-I", "tools/shj/kg_validate.py", "--require-graph"], grep_bad=r"ERROR")

    # 2. 地圖審計
    for f in sorted(f for f in g.glob(str(ADJ / "specs/*-map.json")) if not Path(f).name.startswith("book")):
        step("render " + Path(f).name, ["python3", "tools/shj/render_nanci_map.py", f], grep_bad=r"overflow: \[")
    for f in sorted(g.glob(str(ADJ / "specs/*-overview.json")) + g.glob(str(ADJ / "specs/book*-map.json"))):
        step("render " + Path(f).name, ["python3", "tools/shj/render_overview_map.py", f], grep_bad=r"overflow: \[")
    step("build_shanjing_overview", ["python3", "tools/shj/build_shanjing_overview.py"])
    step("render shanjing-overview", ["python3", "tools/shj/render_overview_map.py", str(ADJ / "specs/shanjing-overview.json")], grep_bad=r"overflow: \[")

    # 3. 草稿重建
    step("draft_wuzang_build", ["python3", "tools/shj/draft_wuzang_build.py"])

    # 4. 零遺漏核對
    # 4a. JSONL 逐行可解析
    bad_jsonl = []
    for f in list(SHJ.glob("data/derived/**/*.jsonl")) + list(SHJ.glob("deliverables/**/*.jsonl")):
        try:
            for i, l in enumerate(f.open(encoding="utf-8"), 1):
                if l.strip():
                    json.loads(l)
        except Exception as e:
            bad_jsonl.append(f"{f.name}:{i} {e}")
    print(("FAIL" if bad_jsonl else " ok "), "jsonl validity")
    if bad_jsonl:
        FAIL.append(("jsonl", "\n".join(bad_jsonl[:10])))

    # 4a2. SVG 良構性（文字轉義缺漏會讓整圖無法顯示）
    import xml.dom.minidom
    bad_svg = []
    for f in list(ADJ.glob("*.svg")):
        try:
            xml.dom.minidom.parse(str(f))
        except Exception as e:
            bad_svg.append(f"{f.name}: {e}")
    print(("FAIL" if bad_svg else " ok "), "svg well-formedness")
    if bad_svg:
        FAIL.append(("svg", "\n".join(bad_svg[:10])))

    # 4b. 框架書 mapping 實體名 → 草稿覆蓋
    books = {}
    for f in g.glob(str(SHJ / "deliverables/draft-v1/book-*.md")):
        books[re.search(r"book-(\d+)-", f).group(1)] = Path(f).read_text(encoding="utf-8")
    miss = []
    for f in g.glob(str(ADJ / "book*-mappings.jsonl")):
        bk = re.search(r"book(\d+)", f).group(1)
        for l in open(f, encoding="utf-8"):
            d = json.loads(l)
            if "disposition" not in d:
                continue
            base = re.split(r"[（(]", d["name"])[0]
            if base and base not in books.get(bk, ""):
                miss.append((bk, d["name"]))
    print(("FAIL" if miss else " ok "), f"draft coverage (framework names) miss={len(miss)}")
    if miss:
        FAIL.append(("draft-coverage", str(miss[:10])))

    # 4c. KG 非 DOC 節點屬性覆蓋
    attrs = [json.loads(l) for l in open(SHJ / "data/derived/kg/attributes.jsonl", encoding="utf-8")]
    covered = {a["subject"] for a in attrs if a["id"].startswith(("ATTMAP:", "ATTRD:", "ATTFW:", "ATTAD:"))}
    nodes = [json.loads(l) for l in open(SHJ / "data/derived/kg/nodes.jsonl", encoding="utf-8")]
    miss_kg = [n["id"] for n in nodes if n["type"] != "DOC" and n["id"] not in covered]
    print(("FAIL" if miss_kg else " ok "), f"KG attribute coverage miss={len(miss_kg)}")
    if miss_kg:
        FAIL.append(("kg-coverage", str(miss_kg[:10])))

    print()
    if FAIL:
        print(f"=== {len(FAIL)} FAILED ===")
        for n, o in FAIL:
            print(f"--- {n} ---\n{o[:600]}")
        return 1
    print("=== ALL CHECKS PASSED ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
