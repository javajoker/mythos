"""Expand LLM-authored mapping groups onto every SHJ mountain and water node.

The mapping groups contain the semantic choices and reasons. This tool only
matches the explicit scope supplied by those groups, preserves LLM review memory,
and checks that no MTN/WAT node is omitted.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
ERA = ROOT / "projects/shanhaijing/data/derived/era"
GROUPS = ERA / "mapping-groups.jsonl"
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
WATER_REGISTRY = ERA / "water-mappings.jsonl"
MOUNTAIN_OUT = ERA / "mountain-mappings.jsonl"
SUMMARY_OUT = ERA / "mapping-summary.json"


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    if not GROUPS.exists():
        raise SystemExit(f"missing LLM-authored mapping groups: {GROUPS}")
    nodes = read_jsonl(KG / "nodes.jsonl")
    entries = {entry["id"]: entry for entry in read_jsonl(ENTRIES)}
    groups = read_jsonl(GROUPS)
    for group in groups:
        if group.get("status") not in {"proposed_pending_review", "unresolved_aggregate"} or len(group.get("candidates", [])) < 3:
            raise ValueError(f"{group.get('id')}: mappings need a valid LLM status and at least three candidates")

    def group_for(node):
        explicit = [group for group in groups if node["id"] in group.get("scope", {}).get("entity_ids", [])]
        if explicit:
            return explicit[0]
        entry = entries[node["first_entry"]]
        matches = [group for group in groups
                   if group.get("scope", {}).get("type") == node["type"]
                   and group.get("scope", {}).get("book") == entry["book_no"]
                   and group.get("scope", {}).get("section") == entry["section"]]
        if len(matches) != 1:
            raise ValueError(f"{node['id']}: expected one group, got {len(matches)}")
        return matches[0]

    existing_water = {row["entity"]: row for row in read_jsonl(WATER_REGISTRY)} if WATER_REGISTRY.exists() else {}
    water_records, mountain_records = [], []
    for node in nodes:
        if node["type"] not in {"MTN", "WAT"}:
            continue
        group = group_for(node)
        entry = entries[node["first_entry"]]
        record = {
            "entity": node["id"],
            "canonical_name": node["canonical_name"],
            "type": node["type"],
            "first_entry": node["first_entry"],
            "book": entry["book_no"],
            "section": entry["section"],
            "mentions": node["names"],
            "mapping_group": group["id"],
            "mapping_status": group["status"],
            "candidates": group["candidates"],
            "historical_states": group["historical_states"],
            "reason": group["reason"],
            "evidence_entries": sorted({name["entry"] for name in node["names"]}),
            "review": {"status": "pending", "reviewer": None, "decision": None},
        }
        if node["type"] == "WAT":
            previous = existing_water.get(node["id"], {})
            for key in ("initiator_hypotheses", "shared_mountains", "relation_ids"):
                if key in previous:
                    record[key] = previous[key]
            water_records.append(record)
        else:
            mountain_records.append(record)

    write_jsonl(WATER_REGISTRY, water_records)
    write_jsonl(MOUNTAIN_OUT, mountain_records)
    counts = Counter(record["mapping_group"] for record in water_records + mountain_records)
    summary = {
        "schema_version": "shj-kg-1.3",
        "mapping_groups_sha256": hashlib.sha256(GROUPS.read_bytes()).hexdigest(),
        "water_nodes": len(water_records),
        "mountain_nodes": len(mountain_records),
        "proposed_pending_review": sum(record["mapping_status"] == "proposed_pending_review"
                                      for record in water_records + mountain_records),
        "unresolved_aggregate": sum(record["mapping_status"] == "unresolved_aggregate"
                                    for record in water_records + mountain_records),
        "groups": dict(sorted(counts.items())),
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("water_nodes", "mountain_nodes", "proposed_pending_review",
                                                   "unresolved_aggregate")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
