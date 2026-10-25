"""Validate SHJ graph structure without making semantic decisions.

Usage:
  python3 -I tools/shj/kg_validate.py
  python3 -I tools/shj/kg_validate.py --require-graph

Missing graph files are skipped by default while the graph is being built.
Conflicting attribute values are reported, never resolved by this tool.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY = ROOT / "projects/shanhaijing/data/kg-ontology.json"
GRAPH = ROOT / "projects/shanhaijing/data/derived/kg"
ENTRY_ID = re.compile(r"^SHJ-\d{2}-\d+-\d{3}$")
NODE_ID = re.compile(r"^([A-Z]+):(SHJ-\d{2}-\d+-\d{3})#([1-9]\d*)$")


def read_jsonl(path):
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if line.strip():
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f"{path}:{line_no}: expected object")
                rows.append(row)
    return rows


def validate_ontology(ontology, errors):
    types = set(ontology["entity_types"])
    if set(ontology["geography_types"]) - types:
        errors.append("ontology: unknown geography type")
    for name, definition in ontology["predicate_definitions"].items():
        unknown = set(definition["domains"]) - types
        if unknown:
            errors.append(f"ontology predicate {name}: unknown domains {sorted(unknown)}")
        if not definition.get("value_type"):
            errors.append(f"ontology predicate {name}: missing value_type")
    for name, definition in ontology["relation_types"].items():
        unknown = (set(definition["domain"]) | set(definition["range"])) - types
        if unknown:
            errors.append(f"ontology relation {name}: unknown types {sorted(unknown)}")
        if set(definition["layers"]) - {"textual", "interpretive"}:
            errors.append(f"ontology relation {name}: invalid layer")


def unique_ids(rows, label, errors):
    seen = set()
    for row in rows:
        value = row.get("id")
        if not value:
            errors.append(f"{label}: missing id")
        elif value in seen:
            errors.append(f"{label}: duplicate id {value}")
        seen.add(value)


REQUIRED_FIELDS = {
    "nodes": ["id", "type", "canonical_name", "first_entry", "names", "status"],
    "mentions": ["id", "entry", "surface", "type", "node", "status", "quote"],
    "edges": ["id", "src", "dst", "type", "layer", "entry", "quote", "status"],
    "attributes": ["id", "subject", "predicate", "value", "kind", "status", "evidence", "provenance"],
}


def valid_value(value, value_type):
    if value_type == "any":
        return True
    if value_type == "string":
        return isinstance(value, str)
    if value_type == "object":
        return isinstance(value, dict)
    if value_type == "geo_point":
        if not isinstance(value, dict) or set(value) != {"lat", "lon"}:
            return False
        lat, lon = value["lat"], value["lon"]
        numeric = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
        return numeric(lat) and numeric(lon) and -90 <= lat <= 90 and -180 <= lon <= 180
    if value_type == "year_range":
        return (isinstance(value, list) and len(value) == 2
                and all(isinstance(x, int) and not isinstance(x, bool) for x in value)
                and value[0] <= value[1])
    if value_type == "geometry":
        return isinstance(value, dict) and bool(value.get("type")) and "coordinates" in value
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-graph", action="store_true")
    args = parser.parse_args()
    ontology = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    errors = []
    validate_ontology(ontology, errors)

    required = ["nodes", "mentions", "edges", "attributes"]
    missing = [name for name in required if not (GRAPH / f"{name}.jsonl").exists()]
    if args.require_graph and missing:
        errors.append(f"missing graph files: {', '.join(missing)}")

    nodes = read_jsonl(GRAPH / "nodes.jsonl")
    mentions = read_jsonl(GRAPH / "mentions.jsonl")
    edges = read_jsonl(GRAPH / "edges.jsonl")
    attributes = read_jsonl(GRAPH / "attributes.jsonl")
    for label, rows in [("nodes", nodes), ("mentions", mentions), ("edges", edges), ("attributes", attributes)]:
        unique_ids(rows, label, errors)
        for row in rows:
            missing_fields = [key for key in REQUIRED_FIELDS[label] if key not in row]
            if missing_fields:
                errors.append(f"{label} {row.get('id')}: missing fields {', '.join(missing_fields)}")

    node_by_id = {}
    for node in nodes:
        match = NODE_ID.match(node.get("id", ""))
        if not match:
            errors.append(f"node {node.get('id')}: invalid id")
            continue
        node_by_id[node["id"]] = node
        node_type, entry, _ = match.groups()
        if node.get("type") != node_type:
            errors.append(f"node {node['id']}: type/id mismatch")
        if node.get("first_entry") != entry:
            errors.append(f"node {node['id']}: first_entry/id mismatch")
        if node.get("status") not in ontology["node_statuses"]:
            errors.append(f"node {node['id']}: invalid status")
        if node_type in ontology["geography_types"]:
            book = int(entry.split("-")[1])
            if book not in ontology["base_books"] and node.get("status") != "pending_anchor":
                errors.append(f"node {node['id']}: v1 geography node outside books 1-5")

    for mention in mentions:
        entry = mention.get("entry", "")
        if not ENTRY_ID.match(entry):
            errors.append(f"mention {mention.get('id')}: invalid entry")
        if mention.get("status") not in ontology["mention_statuses"]:
            errors.append(f"mention {mention.get('id')}: invalid status")
        if mention.get("status") == "ignored" and not mention.get("reason"):
            errors.append(f"mention {mention.get('id')}: ignored requires a reason")
        target = mention.get("node")
        if target is not None and target not in node_by_id:
            errors.append(f"mention {mention.get('id')}: unknown node {target}")
        if target is None and mention.get("status") != "pending_anchor":
            errors.append(f"mention {mention.get('id')}: null node requires pending_anchor")
        if target is None and mention.get("type") not in ontology["geography_types"]:
            errors.append(f"mention {mention.get('id')}: only geography may be pending_anchor")

    relations = ontology["relation_types"]
    for edge in edges:
        relation = relations.get(edge.get("type"))
        if not relation:
            errors.append(f"edge {edge.get('id')}: unknown relation {edge.get('type')}")
            continue
        src, dst = node_by_id.get(edge.get("src")), node_by_id.get(edge.get("dst"))
        if not src or not dst:
            errors.append(f"edge {edge.get('id')}: unresolved endpoint")
            continue
        if src["type"] not in relation["domain"] or dst["type"] not in relation["range"]:
            errors.append(f"edge {edge.get('id')}: type mismatch")
        if edge.get("layer") not in relation["layers"]:
            errors.append(f"edge {edge.get('id')}: invalid layer")

    predicates = ontology["predicate_definitions"]
    values = defaultdict(set)
    for attribute in attributes:
        subject = node_by_id.get(attribute.get("subject"))
        if not subject:
            errors.append(f"attribute {attribute.get('id')}: unresolved subject")
            continue
        predicate = predicates.get(attribute.get("predicate"))
        if not predicate:
            errors.append(f"attribute {attribute.get('id')}: unregistered predicate")
            continue
        if subject["type"] not in predicate["domains"]:
            errors.append(f"attribute {attribute.get('id')}: predicate/type mismatch")
        if not valid_value(attribute.get("value"), predicate["value_type"]):
            errors.append(f"attribute {attribute.get('id')}: value does not match {predicate['value_type']}")
        if attribute.get("kind") not in ontology["attribute_kinds"]:
            errors.append(f"attribute {attribute.get('id')}: invalid kind")
        if attribute.get("status") not in ontology["assertion_statuses"]:
            errors.append(f"attribute {attribute.get('id')}: invalid status")
        if attribute.get("status") != "rejected":
            key = (attribute["subject"], attribute["predicate"])
            values[key].add(json.dumps(attribute.get("value"), ensure_ascii=False, sort_keys=True))

    conflicts = sum(len(options) > 1 for options in values.values())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"ontology valid; nodes={len(nodes)} mentions={len(mentions)} edges={len(edges)} attributes={len(attributes)}")
    if missing and not args.require_graph:
        print(f"graph files not yet present: {', '.join(missing)}")
    print(f"attribute conflicts reported={conflicts}; semantic resolution requires LLM review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
