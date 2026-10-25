#!/usr/bin/env python3
"""Assemble the associative/deductive attribute layer into the KG.

Reads era/adaptation/*-assoc-ded.jsonl (LLM-authored symbolism/utility records)
and writes attributes with kind=associative / kind=deductive. This tool only
restructures LLM-authored records; no semantic decisions. Idempotent: ATTAD
records are rebuilt.

Usage: python3 tools/shj/kg_assoc_ded_build.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
KIND = {"associative.symbolism": "associative", "deductive.utility": "deductive"}


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    kg_nodes = {n["id"] for n in read_jsonl(KG / "nodes.jsonl")}
    records = []
    errors = []
    counts = Counter()
    seq = Counter()
    for path in sorted(ADJ.glob("*-assoc-ded.jsonl")):
        slug = path.name.replace("-assoc-ded.jsonl", "")
        for row in read_jsonl(path):
            nid = row["node"]
            if nid not in kg_nodes:
                errors.append(f"{slug}: node {nid} not in KG")
                continue
            pred = row["predicate"]
            if pred not in KIND:
                errors.append(f"{slug}: {nid}: bad predicate {pred}")
                continue
            seq[(nid, pred)] += 1
            records.append({
                "id": f"ATTAD:{slug}:{nid}:{pred}#{seq[(nid, pred)]}",
                "subject": nid,
                "predicate": pred,
                "value": row["value"],
                "kind": KIND[pred],
                "status": "proposed",
                "confidence": row.get("confidence"),
                "evidence": [{"entry": row.get("entry"), "quote": row.get("evidence_quote")}],
                "provenance": {"package": f"era/adaptation/{slug}", "assembled": "kg-v1-assoc-ded",
                               "review_status": row.get("review_status", "proposed_pending_review")},
            })
            counts[pred] += 1
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    attributes = [a for a in read_jsonl(KG / "attributes.jsonl") if not a.get("id", "").startswith("ATTAD:")]
    attributes.extend(records)
    write_jsonl(KG / "attributes.jsonl", attributes)

    manifest_path = KG / "build-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["kg_v1_assoc_ded"] = {
        "assembled_by": "kg_assoc_ded_build.py",
        "packages": 26,
        "records": len(records),
        "by_predicate": dict(counts),
        "attributes_total": len(attributes),
        "review_status": "proposed_pending_review",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"assoc/ded records: {len(records)} ({dict(counts)}); attributes.jsonl now {len(attributes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
