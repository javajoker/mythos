#!/usr/bin/env python3
"""Apply reviewer decisions to KG attributes.

Reads a review-actions file (JSONL): {"attribute_id", "decision":
"accepted|contested|rejected", "note"?, "reviewer"?, "date"?}. Sets the
attribute's status and records review provenance. Decisions are human
(initiator) decisions; this tool only writes them back structurally.

Usage: python3 tools/shj/apply_review.py <review-actions.jsonl>
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATTRS = ROOT / "projects/shanhaijing/data/derived/kg/attributes.jsonl"
VALID = {"accepted", "contested", "rejected"}


def main(path):
    actions = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    rows = [json.loads(l) for l in open(ATTRS, encoding="utf-8")]
    by_id = {a["id"]: a for a in rows}
    applied, missing, skipped = 0, [], 0
    for act in actions:
        aid = act.get("attribute_id")
        dec = act.get("decision")
        if dec not in VALID:
            skipped += 1
            continue
        a = by_id.get(aid)
        if not a:
            missing.append(aid)
            continue
        a["status"] = dec
        a.setdefault("provenance", {})["reviewed_by"] = act.get("reviewer", "initiator")
        a["provenance"]["review_date"] = act.get("date", str(date.today()))
        if act.get("note"):
            a["provenance"]["review_note"] = act["note"]
        applied += 1
    with open(ATTRS, "w", encoding="utf-8") as f:
        for a in rows:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    print(f"applied {applied}; skipped {skipped}; missing {len(missing)}")
    for m in missing[:10]:
        print("  missing:", m)
    return 1 if missing else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: apply_review.py <review-actions.jsonl>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
