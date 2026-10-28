#!/usr/bin/env python3
"""Assemble LLM-authored framework-book relations into kg/edges.jsonl.

Reads era/adaptation/bookNN-edges.jsonl (LLM-authored relational decisions with
verbatim quotes). Code validates node existence, relation registration, assigns
REL ids, and rebuilds REL:FW records idempotently. No semantic decisions.

Row schema: {book, entry, src, dst, type, layer, quote, status?, note?}
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
ONTOLOGY = ROOT / "projects/shanhaijing/data/kg-ontology.json"


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    onto = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    relations = onto["relation_types"]
    node_by_id = {n["id"]: n for n in read_jsonl(KG / "nodes.jsonl")}
    edges = [e for e in read_jsonl(KG / "edges.jsonl") if not e.get("id", "").startswith(("REL:FW:", "REL:XLINK"))]
    errors = []
    added = 0
    seq = 0
    for n in range(6, 19):
        slug = f"book{n:02d}"
        path = ADJ / f"{slug}-edges.jsonl"
        if not path.exists():
            errors.append(f"missing {path}")
            continue
        for row in read_jsonl(path):
            rel = row["type"]
            if rel not in relations:
                errors.append(f"{slug}:{row.get('entry')}: unregistered relation {rel}")
                continue
            for end in ("src", "dst"):
                if row[end] not in node_by_id:
                    errors.append(f"{slug}:{row.get('entry')}: {end} {row[end]} not in KG")
            else:
                seq += 1
                edges.append({
                    "id": f"REL:FW:{slug}#{seq}",
                        "src": row["src"], "dst": row["dst"], "type": rel,
                        "layer": row.get("layer", "textual"), "entry": row["entry"],
                        "quote": row.get("quote", ""),
                        "status": row.get("status", "stated"),
                        "provenance": {"package": f"era/adaptation/{slug}",
                                       "assembled": "kg-framework-edges-v1",
                                       "note": row.get("note", "")},
                        **({"bearing": row["bearing"]} if row.get("bearing") else {}),
                })
                added += 1
    # 跨條目同實體連接（LLM 裁決後登記於 ledgers/cross-entry-links.jsonl；本工具只驗證不裁決）
    links_path = ROOT / "projects/shanhaijing/ledgers/cross-entry-links.jsonl"
    if links_path.exists():
        for row in read_jsonl(links_path):
            rel = row["type"]
            if rel not in relations:
                errors.append(f"xlink:{row.get('entry')}: unregistered relation {rel}")
                continue
            ok = True
            for end in ("src", "dst"):
                if row[end] not in node_by_id:
                    errors.append(f"xlink:{row.get('entry')}: {end} {row[end]} not in KG")
                    ok = False
            if ok:
                seq += 1
                edges.append({
                    "id": f"REL:XLINK#{seq}",
                    "src": row["src"], "dst": row["dst"], "type": rel,
                    "layer": row.get("layer", "interpretive"), "entry": row["entry"],
                    "quote": row.get("quote", ""),
                    "status": row.get("status", "adjudicated"),
                    "provenance": {"package": "ledgers/cross-entry-links.jsonl",
                                   "assembled": "kg-framework-edges-v1",
                                   "note": row.get("note", "")},
                })
                added += 1
    write_jsonl(KG / "edges.jsonl", edges)
    print(f"framework edges +{added}; edges total {len(edges)}")
    if errors:
        for e in errors[:40]:
            print("ERROR:", e)
        print(f"total errors: {len(errors)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
