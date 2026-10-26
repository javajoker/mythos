#!/usr/bin/env python3
"""Assemble KG v1: attach the 26 sub-classic adaptation mappings to the base graph.

Reads kg/nodes.jsonl + era/adaptation/*-mappings.jsonl (LLM-authored semantic-fit
decisions) and writes era.candidate / era.state semantic_fit attributes into
kg/attributes.jsonl. This tool only restructures LLM-authored records; it makes
no semantic decisions. Idempotent: previously assembled ATTMAP records are replaced.

Usage: python3 tools/shj/kg_v1_assemble.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
GEO_TYPES = {"MTN", "WAT", "LND"}


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    nodes = read_jsonl(KG / "nodes.jsonl")
    node_by_id = {n["id"]: n for n in nodes}
    geo_nodes = {n["id"] for n in nodes if n["type"] in GEO_TYPES and n["first_entry"].split("-")[1] in {"01","02","03","04","05"}}  # 框架書 geo 節點由 kg_framework_build 覆蓋

    mappings = []
    for path in sorted(ADJ.glob("*-mappings.jsonl")):
        slug = path.name.replace("-mappings.jsonl", "")
        for row in read_jsonl(path):
            row["_slug"] = slug
            mappings.append(row)

    # shared nodes may carry several segment readings (e.g. shared waters across
    # stations); keep all, with suffixed attribute ids
    seg_count = {}
    records = []
    covered = set()
    errors = []
    for m in mappings:
        nid = m.get("node")
        if not nid:
            continue
        if nid not in node_by_id:
            errors.append(f"{m['_slug']}:{m.get('name')}: node {nid} not in KG")
            continue
        covered.add(nid)
        slug = m["_slug"]
        seg_count[nid] = seg_count.get(nid, 0) + 1
        seg = "" if seg_count[nid] == 1 else f":seg{seg_count[nid]}"
        pc = m.get("primary_candidate", {})
        modern = m.get("modern_mountain") or m.get("modern_water")
        value = {
            "role": "primary",
            "name": pc.get("name"),
            "region": pc.get("region"),
            "kind": pc.get("kind"),
            "period_state": pc.get("period_state"),
            "present_state": pc.get("present_state"),
            "fit": m.get("attribute_fit") or pc.get("fit"),
            "modern_name": modern,
            "grid_0385": (m.get("grid") or {}).get("0.385"),
            "evolution_logic": m.get("evolution_logic"),
            "conflicts": m.get("conflicts", []),
            "unknowns": m.get("unknowns", []),
        }
        base = {
            "subject": nid,
            "kind": "semantic_fit",
            "status": "proposed",
            "confidence": m.get("confidence"),
            "evidence": [{"entry": m.get("entry")}],
            "provenance": {"package": f"era/adaptation/{slug}", "assembled": "kg-v1",
                           "review_status": m.get("mapping_status", "proposed_pending_review")},
        }
        records.append({"id": f"ATTMAP:{slug}:{nid}{seg}:primary", "predicate": "era.candidate",
                        "value": value, **base})
        for i, rv in enumerate(m.get("rival_candidates", []), 1):
            records.append({"id": f"ATTMAP:{slug}:{nid}{seg}:rival{i}", "predicate": "era.candidate",
                            "value": {"role": "rival", "name": rv.get("name"), "fit": rv.get("fit"),
                                      "status": rv.get("status", "rival")},
                            **base})
        records.append({"id": f"ATTMAP:{slug}:{nid}{seg}:state", "predicate": "era.state",
                        "value": f"{pc.get('period_state')}→{pc.get('present_state')}",
                        **base})

    missing = sorted(geo_nodes - covered)
    print(f"mappings: {len(mappings)} rows from {len(set(m['_slug'] for m in mappings))} packages")
    print(f"geo nodes covered: {len(covered)}/{len(geo_nodes)}; attributes assembled: {len(records)}")
    if missing:
        print(f"UNCOVERED geo nodes: {len(missing)}")
        for nid in missing[:20]:
            print(" ", nid, node_by_id[nid]["canonical_name"])
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    if missing:
        return 1

    attributes = [a for a in read_jsonl(KG / "attributes.jsonl") if not a.get("id", "").startswith("ATTMAP:")]
    attributes.extend(records)
    write_jsonl(KG / "attributes.jsonl", attributes)

    manifest_path = KG / "build-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["kg_v1"] = {
        "assembled_by": "kg_v1_assemble.py",
        "packages": sorted(set(m["_slug"] for m in mappings)),
        "mapping_attributes": len(records),
        "geo_nodes_covered": len(covered),
        "geo_nodes_total": len(geo_nodes),
        "attributes_total": len(attributes),
        "review_status": "proposed_pending_review",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"kg/attributes.jsonl now {len(attributes)} records; manifest updated (kg_v1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
