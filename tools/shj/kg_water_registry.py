"""Create a complete pending water-mapping registry for LLM review.

This tool only inventories existing WAT nodes and their structural relations.
It never proposes real-world candidates, merges waters or assigns coordinates.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
OUT = ROOT / "projects/shanhaijing/data/derived/era"
HYPOTHESES = OUT / "water-hypotheses.jsonl"


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def main():
    nodes = read_jsonl(KG / "nodes.jsonl")
    edges = read_jsonl(KG / "edges.jsonl")
    waters = {node["id"]: node for node in nodes if node["type"] == "WAT"}
    shared_mountains = defaultdict(set)
    relation_ids = defaultdict(list)
    for edge in edges:
        for endpoint in (edge["src"], edge["dst"]):
            if endpoint in waters:
                relation_ids[endpoint].append(edge["id"])
                other = edge["dst"] if endpoint == edge["src"] else edge["src"]
                if other.startswith("MTN:"):
                    shared_mountains[endpoint].add(other)

    hypotheses = {}
    if HYPOTHESES.exists():
        for hypothesis in read_jsonl(HYPOTHESES):
            hypotheses[hypothesis["entity"]] = hypothesis["hypotheses"]

    existing = {}
    existing_path = OUT / "water-mappings.jsonl"
    if existing_path.exists():
        existing = {row["entity"]: row for row in read_jsonl(existing_path)}

    records = []
    for water_id, node in sorted(waters.items()):
        previous = existing.get(water_id, {})
        records.append({
            "entity": water_id,
            "canonical_name": node["canonical_name"],
            "mentions": node["names"],
            "mapping_status": previous.get("mapping_status", "pending"),
            "candidates": previous.get("candidates", []),
            "historical_states": previous.get("historical_states", []),
            "initiator_hypotheses": hypotheses.get(water_id, previous.get("initiator_hypotheses", [])),
            "shared_mountains": sorted(shared_mountains[water_id]),
            "relation_ids": sorted(relation_ids[water_id]),
            "mapping_group": previous.get("mapping_group"),
            "reason": previous.get("reason"),
            "evidence_entries": previous.get("evidence_entries", []),
            "review": previous.get("review", {"status": "pending", "reviewer": None, "decision": None}),
        })
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "water-mappings.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    shared = sum(bool(record["shared_mountains"]) for record in records)
    summary = {"water_nodes": len(records),
               "pending_mappings": sum(record["mapping_status"] == "pending" for record in records),
               "proposed_pending_review": sum(record["mapping_status"] == "proposed_pending_review" for record in records),
               "waters_with_initiator_hypotheses": sum(bool(record["initiator_hypotheses"]) for record in records),
               "waters_with_mountain_relations": shared,
               "waters_shared_by_multiple_mountains": sum(len(record["shared_mountains"]) > 1 for record in records)}
    (OUT / "water-mapping-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
