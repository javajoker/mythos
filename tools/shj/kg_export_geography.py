"""Export mountain/water nodes and water-related edges for human review.

This is a deterministic filter only. It does not select anchors or interpret locations.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
OUT = ROOT / "projects/shanhaijing/data/derived/review"


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    nodes = read_jsonl(KG / "nodes.jsonl")
    edges = read_jsonl(KG / "edges.jsonl")
    geography = [node for node in nodes if node["type"] in {"MTN", "WAT"}]
    node_by_id = {node["id"]: node for node in nodes}
    water_edges = [edge for edge in edges
                   if node_by_id[edge["src"]]["type"] == "WAT" or node_by_id[edge["dst"]]["type"] == "WAT"]
    OUT.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT / "geography-nodes.jsonl", geography)
    write_jsonl(OUT / "water-relations.jsonl", water_edges)

    node_types = Counter(node["type"] for node in geography)
    relation_types = Counter(edge["type"] for edge in water_edges)
    books = Counter(node["first_entry"].split("-")[1] for node in geography)
    summary = {"mountain_nodes": node_types["MTN"], "water_nodes": node_types["WAT"],
               "water_relations": len(water_edges), "relation_types": dict(sorted(relation_types.items())),
               "geography_nodes_by_book": dict(sorted(books.items()))}
    (OUT / "geography-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    node_by_id = {node["id"]: node for node in nodes}
    lines = ["# 五臧山經山水與水體關係審核 / Mountain and water review", "",
             f"- 山體節點 / MTN: {node_types['MTN']}",
             f"- 水體節點 / WAT: {node_types['WAT']}",
             f"- 水體相關關係 / water relations: {len(water_edges)}", "",
             "| 條目 / Entry | 關係 / Relation | 起點 / Source | 終點 / Target | 層 / Layer |",
             "|---|---|---|---|---|"]
    for edge in water_edges:
        lines.append(f"| {edge['entry']} | {edge['type']} | {node_by_id[edge['src']]['canonical_name']} | "
                     f"{node_by_id[edge['dst']]['canonical_name']} | {edge['layer']} |")
    (OUT / "water-network.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
