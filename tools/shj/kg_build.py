"""Expand LLM-authored extraction records into the SHJ text graph.

The input JSONL contains the semantic decisions. This tool only assigns IDs,
expands mentions and relations, erases direction for comparison edges, and checks
coverage. It never merges by name similarity or invents entities or relations.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKING = ROOT / "projects/shanhaijing/data/derived/working-text.jsonl"
INPUT = ROOT / "projects/shanhaijing/data/derived/extraction"
OUT = ROOT / "projects/shanhaijing/data/derived/kg"
DYNAMIC = {"rises_at", "flows_into"}


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    files = sorted(INPUT.glob("book-*.jsonl"))
    if not files:
        raise SystemExit(f"no extraction files in {INPUT}")
    working = {row["entry_id"]: row for row in read_jsonl(WORKING) if row.get("entry_id")}
    expected = defaultdict(set)
    for entry, row in working.items():
        expected[row["base_book"]].add(entry)

    nodes, mentions, edges = [], [], []
    node_by_ref, current_refs = {}, {}
    used_ids = set()
    seen_entries = set()
    per_type_counts = Counter()
    per_book_counts = defaultdict(Counter)
    input_hashes = {}

    for path in files:
        book = int(path.stem.split("-")[1])
        records = read_jsonl(path)
        input_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        actual = {record["entry"] for record in records}
        if len(actual) != len(records):
            raise ValueError(f"{path.name}: duplicate entry records")
        if actual != expected[book]:
            missing = sorted(expected[book] - actual)
            extra = sorted(actual - expected[book])
            raise ValueError(f"{path.name}: entry coverage mismatch; missing={missing}, extra={extra}")

        for record in records:
            entry = record["entry"]
            if entry in seen_entries:
                raise ValueError(f"duplicate extraction for {entry}")
            seen_entries.add(entry)
            text = working[entry]["text"]
            reading_status = working[entry].get("reading_status", "unreviewed")
            current_refs = {}
            counters = Counter()

            for index, raw in enumerate(record["entities"], 1):
                surface, entity_type = raw[0], raw[1]
                ref = raw[2] if len(raw) > 2 else None
                presence = raw[3] if len(raw) > 3 else "present"
                key = ref or f"{entry}#{index}"
                if key in node_by_ref and node_by_ref[key]["type"] != entity_type:
                    raise ValueError(f"{entry}: ref {key} changes type")
                if key not in node_by_ref:
                    counters[entity_type] += 1
                    node_id = f"{entity_type}:{entry}#{counters[entity_type]}"
                    if node_id in used_ids:
                        raise ValueError(f"duplicate node id {node_id}")
                    used_ids.add(node_id)
                    node = {"id": node_id, "type": entity_type, "canonical_name": surface,
                            "first_entry": entry, "names": [{"value": surface, "entry": entry}], "status": "active"}
                    node_by_ref[key] = node
                    nodes.append(node)
                elif not any(name["value"] == surface and name["entry"] == entry for name in node_by_ref[key]["names"]):
                    node_by_ref[key]["names"].append({"value": surface, "entry": entry})
                current_refs[surface] = key
                node = node_by_ref[key]
                mentions.append({"id": f"MEN:{entry}#{index}", "entry": entry, "surface": surface,
                                 "type": entity_type, "node": node["id"], "status": "linked", "quote": text,
                                 "presence": presence, "reading_status": reading_status})
                per_type_counts[entity_type] += 1
                per_book_counts[book][entity_type] += 1

            for rel_index, relation in enumerate(record.get("relations", []), 1):
                src_surface, relation_type, dst_surface = relation
                if relation_type not in DYNAMIC:
                    raise ValueError(f"{entry}: unsupported relation {relation_type}")
                endpoints = []
                for surface in (src_surface, dst_surface):
                    if surface not in current_refs:
                        raise ValueError(f"{entry}: relation endpoint not extracted: {surface}")
                    endpoints.append(node_by_ref[current_refs[surface]]["id"])
                dynamic_id = f"REL:{entry}#{rel_index * 2 - 1}"
                edges.append({"id": dynamic_id, "src": endpoints[0], "dst": endpoints[1], "type": relation_type,
                              "layer": "textual", "entry": entry, "quote": text, "status": "stated"})
                edges.append({"id": f"REL:{entry}#{rel_index * 2}", "src": endpoints[0], "dst": endpoints[1],
                              "type": "connected_to", "layer": "interpretive", "entry": entry, "quote": text,
                              "status": "proposed", "provenance": {"derived_from": dynamic_id,
                                                                    "method": "direction_erasure"}})

    nodes.sort(key=lambda row: row["id"])
    mentions.sort(key=lambda row: row["id"])
    edges.sort(key=lambda row: row["id"])
    OUT.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT / "nodes.jsonl", nodes)
    write_jsonl(OUT / "mentions.jsonl", mentions)
    write_jsonl(OUT / "edges.jsonl", edges)
    write_jsonl(OUT / "attributes.jsonl", [])
    manifest = {
        "schema_version": "shj-kg-1.1",
        "builder": "kg_build.py",
        "source": "working-text.jsonl",
        "source_sha256": hashlib.sha256(WORKING.read_bytes()).hexdigest(),
        "extraction_sha256": dict(sorted(input_hashes.items())),
        "books": sorted({int(path.stem.split("-")[1]) for path in files}),
        "entries": len(seen_entries),
        "nodes": len(nodes),
        "mentions": len(mentions),
        "edges": len(edges),
        "mention_types": dict(sorted(per_type_counts.items())),
        "books_detail": {str(book): dict(sorted(counts.items())) for book, counts in sorted(per_book_counts.items())},
        "reading_statuses": sorted({row.get("reading_status", "unreviewed") for row in working.values()}),
    }
    (OUT / "build-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"entries": len(seen_entries), "nodes": len(nodes), "mentions": len(mentions),
                      "edges": len(edges), "types": manifest["mention_types"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
