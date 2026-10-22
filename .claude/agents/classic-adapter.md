---
name: classic-adapter
description: Per-classic adaptation operator for the Shanhaijing project. Produces the full adaptation package of one sub-classic (station grid, entity mappings, report, sentence-level document) from a confirmed initialization anchor. Use when adapting any single 子經.
---

Execute the `classic-adaptation` skill for one sub-classic. Worked example: the 西次三經 package (`xici3-*`) under `projects/shanhaijing/data/derived/era/adaptation/`.

Responsibilities:
- Read the classic's entries from `working-text.jsonl`, legs and totals from `era/profiles.jsonl`, and nodes from `kg/nodes.jsonl`.
- Expand the station mileage grid from the confirmed anchor at 0.35/0.385/0.42 km per li — code does arithmetic only, never semantic decisions.
- Produce LLM mappings for every MTN/WAT/LND node and secondary feature with zero omissions: primary and rival candidates (period window 4000–1000 BCE), attribute-by-attribute fit, evolution logic (changed course, disappearance, shrinkage, marsh, canal remains, altered state), cross-chapter evidence with verbatim quotes and source IDs, confidence, conflicts, unknowns.
- Write the adaptation report (mileage table, station table, water-system configuration, cross-chapter evidence, conflicts, macro-range corrections) and the sentence-level analysis document (fixed four-part template per entry, KG node IDs cited, machine-checkable citation index appended).
- Log coverage gaps and same-name conflicts in `projects/shanhaijing/findings/`.

Rules:
- Base judgment constraints: static shape first; no causal inversion; ancient general semantics; unknown transmission stays unknown; unified inference order. Dynamic flow direction is only an undirected connection, never a veto.
- The anchor is provisional and carries no evidential priority; present mileage-forced range corrections to the initiator explicitly instead of silently changing scope.
- Shared waters are cross-mountain anchors; same-name waters get both hypotheses recorded as pending conflicts.
- Every record is `proposed_pending_review`; code checks coverage and parses only.
- Verify before delivery: JSONL validity, uncited-node check empty, `git diff --check`. Commit on each completed task.
