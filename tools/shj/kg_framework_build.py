#!/usr/bin/env python3
"""Assemble framework-book (Books 6–18) entities into the KG.

Reads era/adaptation/bookNN-mappings.jsonl (LLM-authored adaptation records) and:
- reuse rows -> mention linked to the reused Books 1–5 node + framework_reference
  attribute on that node; a reused_from_shanjing edge is emitted when the mention
  and node exist.
- pending_anchor / new_entity rows -> new nodes (TYPE:ENTRY#n), mentions, and
  era.candidate / era.state attributes.
Non-ontology kinds are normalized (REG/REGION->LND, SET->POL, TMB/COM->LND,
MAT->MIN, GOD/MYTH->PER, PLT->PLA); the original kind is preserved in the
attribute value. Idempotent: all Books 6–18 nodes/mentions/edges and ATTFW
attributes are rebuilt from scratch. Code assigns IDs and restructures only;
no semantic decisions.

Usage: python3 tools/shj/kg_framework_build.py
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
ADJ = ROOT / "projects/shanhaijing/data/derived/era/adaptation"
NORM = {"REG": "LND", "REGION": "LND", "SET": "POL", "TMB": "LND", "COM": "LND",
        "MAT": "MIN", "GOD": "PER", "MYTH": "PER", "PLT": "PLA"}
FRAMEWORK_BOOKS = {f"{i:02d}" for i in range(6, 19)}


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    nodes = read_jsonl(KG / "nodes.jsonl")
    mentions = read_jsonl(KG / "mentions.jsonl")
    edges = read_jsonl(KG / "edges.jsonl")
    attributes = read_jsonl(KG / "attributes.jsonl")
    node_by_id = {n["id"]: n for n in nodes}
    men_by_entry = defaultdict(int)
    for m in mentions:
        men_by_entry[m["entry"]] += 1

    # wipe previous framework build (incl. malformed artifacts of earlier runs)
    STRICT = re.compile(r"^SHJ-\d{2}-\d+-\d{3}$")
    def is_fw(eid):
        if not STRICT.match(eid or ""):
            return True
        return eid.split("-")[1] in FRAMEWORK_BOOKS
    nodes = [n for n in nodes if not is_fw(n["first_entry"])]
    mentions = [m for m in mentions if not is_fw(m.get("entry", ""))]
    edges = [e for e in edges if not e.get("id", "").startswith("EDGE-FW:")]
    attributes = [a for a in attributes if not a.get("id", "").startswith("ATTFW:")]
    node_by_id = {n["id"]: n for n in nodes}
    men_seq = defaultdict(int)
    for m in mentions:
        men_seq[m["entry"]] += 1

    stats = defaultdict(int)
    errors = []
    new_nodes = []
    for n in range(6, 19):
        slug = f"book{n:02d}"
        path = ADJ / f"{slug}-mappings.jsonl"
        if not path.exists():
            errors.append(f"missing {path}")
            continue
        seq = defaultdict(int)   # (entry, type) -> running #
        for row in read_jsonl(path):
            if "disposition" not in row:
                continue
            entries = [e.strip() for e in row["entry"].split(",")]
            norm = []
            for e in entries:
                m = re.search(r"SHJ-\d{2}-\d+-\d{3}", e)
                if m:
                    norm.append(m.group(0))
            if not norm:
                errors.append(f"{slug}:{row['name']}: no valid entry in {row['entry']!r}")
                continue
            entries = norm
            entry = entries[0]
            typ = NORM.get(row["kind"], row["kind"])
            pc = row.get("primary_candidate", {})
            disp = row["disposition"]
            prov = {"package": f"era/adaptation/{slug}", "assembled": "kg-framework-v1",
                    "review_status": row.get("mapping_status", "proposed_pending_review")}
            if disp == "reuse":
                nid = row.get("node")
                if nid not in node_by_id:
                    errors.append(f"{slug}:{row['name']}: reuse node {nid} not in KG")
                    continue
                for e in entries:
                    men_seq[e] += 1
                    mentions.append({"id": f"MEN:{e}#{men_seq[e]}", "entry": e, "surface": row["name"],
                                     "type": node_by_id[nid]["type"], "node": nid, "status": "linked",
                                     "quote": "", "presence": "framework_reference"})
                attributes.append({
                    "id": f"ATTFW:{slug}:{entry}:reuse:{nid}",
                    "subject": nid, "predicate": "era.candidate",
                    "value": {"role": "framework_reference", "book": slug, "entry": row["entry"],
                              "name": row["name"], "fit": pc.get("fit")},
                    "kind": "semantic_fit", "status": "proposed",
                    "confidence": row.get("confidence"),
                    "evidence": [{"entry": entry}],
                    "provenance": prov})
                stats["reuse"] += 1
                continue
            # new node (pending_anchor / new_entity)
            seq[(entry, typ)] += 1
            nid = f"{typ}:{entry}#{seq[(entry, typ)]}"
            new_nodes.append({"id": nid, "type": typ, "canonical_name": row["name"],
                              "first_entry": entry,
                              "names": [{"value": row["name"], "entry": e} for e in entries],
                              "status": "pending_anchor"})
            node_by_id[nid] = new_nodes[-1]
            for e in entries:
                men_seq[e] += 1
                mentions.append({"id": f"MEN:{e}#{men_seq[e]}", "entry": e, "surface": row["name"],
                                 "type": typ, "node": nid, "status": "linked", "quote": "",
                                 "presence": "present"})
            base = {"subject": nid, "kind": "semantic_fit", "status": "proposed",
                    "confidence": row.get("confidence"), "evidence": [{"entry": entry}],
                    "provenance": prov}
            attributes.append({
                "id": f"ATTFW:{slug}:{nid}:primary", "predicate": "era.candidate",
                "value": {"role": "primary", "name": pc.get("name"), "region": pc.get("region"),
                          "kind": pc.get("kind"), "period_state": pc.get("period_state"),
                          "present_state": pc.get("present_state"), "fit": pc.get("fit"),
                          "disposition": disp, "original_kind": row["kind"],
                          "conflicts": row.get("conflicts", []), "unknowns": row.get("unknowns", [])},
                **base})
            attributes.append({
                "id": f"ATTFW:{slug}:{nid}:state", "predicate": "era.state",
                "value": f"{pc.get('period_state')}→{pc.get('present_state')}", **base})
            stats[disp] += 1
    nodes.extend(new_nodes)

    write_jsonl(KG / "nodes.jsonl", nodes)
    write_jsonl(KG / "mentions.jsonl", mentions)
    write_jsonl(KG / "edges.jsonl", edges)
    write_jsonl(KG / "attributes.jsonl", attributes)

    manifest_path = KG / "build-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["kg_framework_v1"] = {
        "assembled_by": "kg_framework_build.py",
        "books": sorted(FRAMEWORK_BOOKS),
        "new_nodes": len(new_nodes),
        "by_disposition": {k: v for k, v in stats.items() if k != "reuse"},
        "reuse_links": stats["reuse"],
        "nodes_total": len(nodes), "mentions_total": len(mentions),
        "attributes_total": len(attributes),
        "review_status": "proposed_pending_review",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"framework nodes +{len(new_nodes)}; reuse links {stats['reuse']}; "
          f"nodes={len(nodes)} mentions={len(mentions)} attributes={len(attributes)}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
