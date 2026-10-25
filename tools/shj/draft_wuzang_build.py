#!/usr/bin/env python3
"""Assemble the Five Mountain Classics draft (deliverables/draft-v1/) from the
26 adaptation packages.

All semantic content is LLM-authored upstream (working text, sentence-analysis
§2 expansions, mappings.jsonl, readings-supplement). This tool only recombines
those artifacts into per-book readable drafts and never invents readings.
Unresolved items (conflicts, unknowns, variants, pending review) are preserved.

Usage: python3 tools/shj/draft_wuzang_build.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
OUT = ROOT / "projects/shanhaijing/deliverables/draft-v1"
WORKING = ROOT / "projects/shanhaijing/data/derived/working-text.jsonl"

BOOKS = {
    "01": ("南", "南山經", "nanci", "book-01-nanshan.md"),
    "02": ("西", "西山經", "xici", "book-02-xishan.md"),
    "03": ("北", "北山經", "beici", "book-03-beishan.md"),
    "04": ("東", "東山經", "dongci", "book-04-dongshan.md"),
    "05": ("中", "中山經", "zhongci", "book-05-zhongshan.md"),
}
BOOK_SCOPE = {
    "01": "中南半島（若開→長山）／滇東—南嶺—武夷—東海島鏈／嶺南—閩粵沿海——南島文明方向",
    "02": "藏東橫斷山／喜馬拉雅南麓—印度河／希斯馬—吉薩—利比亞／阿特拉斯—大西洋——起自古印度、三星堆方向，含古埃及、北非",
    "03": "青海南部→杭愛—圖瓦／晉北→陰山→貝加爾／山西—太行→奧爾洪島→楚科奇方向——極北生業（古愛斯基摩方向）",
    "04": "阿巴拉契亞／落基山東麓—大平原—灣岸／加勒比—中美島鏈／灣北岸——美洲（印第安/瑪雅方向）",
    "05": "現實昆侖山源頭帶→關中→河洛嵩山樞紐→桐柏大別→岷山巫山→江南——河南中原文明及中國大山系",
}
ENTRY_HEAD = re.compile(r"^### 【\*\*(SHJ-\d{2}-\d+-\d{3})\*\*】(.*)$|^### 【(SHJ-\d{2}-\d+-\d{3})】(.*)$", re.M)


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def parse_sentence_doc(path):
    """entry_id -> {head, s2_block}"""
    text = path.open(encoding="utf-8").read()
    out = {}
    for m in ENTRY_HEAD.finditer(text):
        eid = m.group(1) or m.group(3)
        head = (m.group(2) if m.group(1) else m.group(4)) or ""
        out.setdefault(eid, {})["head"] = head.replace("**", "").strip()
    # §2 blocks
    parts = re.split(r"\n### 【", text)
    for part in parts[1:]:
        eid = re.search(r"(SHJ-\d{2}-\d+-\d{3})", part.split("】", 1)[0]).group(1)
        m2 = re.search(r"#### 2\..*?\n(.*?)\n#### 3\.", part, re.S)
        if m2:
            out.setdefault(eid, {})["s2"] = m2.group(1).strip()
    return out


def main():
    working = {e["entry_id"]: e for e in read_jsonl(WORKING) if e.get("entry_id")}

    # mappings per entry per slug
    maps_by_entry = defaultdict(list)
    for path in sorted(ADJ.glob("*-mappings.jsonl")):
        for row in read_jsonl(path):
            if row.get("node"):
                maps_by_entry[row["entry"]].append(row)
    supp_by_node = {}
    supp_path = ADJ / "readings-supplement.jsonl"
    if supp_path.exists():
        for row in read_jsonl(supp_path):
            supp_by_node[row["node"]] = row

    OUT.mkdir(parents=True, exist_ok=True)
    index_lines = ["# 五臧山經草稿 v1（draft-v1）", "",
                   "> 全部映射與讀法為競爭假說（proposed_pending_review）；時代窗口 4000–1000 BCE。",
                   "> 本草稿由適配包重組而成：原文（working text）＋ 逐句實體展開（§2）＋ 地理候選（mappings）＋ 未決項。",
                   "> 基礎判斷邏輯：靜態形狀優先／禁止因果倒置／古代通用詞義／承認文化斷層／統一推論順序。", ""]
    total_entries = 0
    for book_no, (mark, book_name, prefix, fname) in BOOKS.items():
        nsec = {"01": 3, "02": 4, "03": 3, "04": 4, "05": 13}[book_no]
        L = [f"# 《{book_name}》草稿（五臧山經卷{mark}）", "",
             f"> 範圍概要：{BOOK_SCOPE[book_no]}", "",
             "> 每條目：原文 → 全要素逐句實體展開 → 地理候選解釋 → 未決項。山水人文風物全部實體的 LLM 識別讀法已結構化入 KG v1（attributes.jsonl）。", ""]
        book_entries = 0
        book_unresolved = 0
        for sec in range(1, nsec + 1):
            slug = f"{prefix}{sec}"
            doc_path = ADJ / f"{slug}-sentence-analysis.md"
            doc = parse_sentence_doc(doc_path) if doc_path.exists() else {}
            sec_entries = sorted([e for e in working
                                  if e.startswith(f"SHJ-{book_no}-{sec}-")],
                                 key=lambda e: working[e]["seq"])
            sec_names = ["首", "次二", "次三", "次四", "次五", "次六", "次七", "次八", "次九", "次十", "次十一", "次十二", "總結"]
            L.append(f"\n## {book_name}·{sec_names[sec-1]}（{slug}）\n")
            for eid in sec_entries:
                book_entries += 1
                info = doc.get(eid, {})
                head = info.get("head", "")
                L.append(f"\n### 【{eid}】{head}\n")
                L.append("> **【經文原文】**")
                L.append(f"> {working[eid]['text']}\n")
                if info.get("s2"):
                    L.append("#### 全要素逐句實體展開")
                    L.append(info["s2"] + "\n")
                # geo candidates
                geo = maps_by_entry.get(eid, [])
                if geo:
                    L.append("#### 地理候選解釋（proposed_pending_review）")
                    for g in geo:
                        pc = g["primary_candidate"]
                        modern = g.get("modern_mountain") or g.get("modern_water") or ""
                        if modern and modern in pc["name"]:
                            modern = ""
                        tail = f"；⛰{modern}" if modern and g["kind"] == "MTN" else (f"；💧{modern}" if modern else "")
                        L.append(f"- `{g['node']}` {g['name']} → {pc['name']}{tail}"
                                 f"（{g.get('confidence','?')}；{pc.get('period_state')}→{pc.get('present_state')}）")
                    L.append("")
                # unresolved
                un = []
                for g in geo:
                    for c in g.get("conflicts", []):
                        un.append(f"衝突：{g['name']}——{c}")
                    for u in g.get("unknowns", []):
                        un.append(f"未知：{g['name']}——{u}")
                if eid == "SHJ-05-13-001":
                    un.append("五臧山經總結段：封禪/禹曰/出銅出鐵統計為文獻層記錄（見 readings-supplement）")
                if un:
                    book_unresolved += len(un)
                    L.append("#### 未決項")
                    for u in un:
                        L.append(f"- {u}")
                    L.append("")
        L.append(f"\n---\n\n本卷條目 {book_entries}；未決項 {book_unresolved} 條（另見各子經適配報告 variant 記錄）。\n")
        (OUT / fname).write_text("\n".join(L), encoding="utf-8")
        total_entries += book_entries
        index_lines.append(f"- [{book_name}（卷{mark}）]({fname})——{book_entries} 條目；{BOOK_SCOPE[book_no]}")
    index_lines += ["", f"共 {total_entries} 條目。未決項逐條目保留；衝突裁決見後續 LLM 衝突解決階段。"]
    (OUT / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"draft-v1 written: {total_entries} entries, 5 books + README -> {OUT}")


if __name__ == "__main__":
    main()
