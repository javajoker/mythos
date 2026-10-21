# Mythos — project instructions

Mythos tests ancient texts as possible records of real observations using reproducible, auditable methods. The primary sub-project is the Shanhaijing 《山海經》.

## Framework v4 and initiator decisions (2026-10-21)

- **Period**: 4000–1000 BCE.
- **Competing hypotheses**: no real-world correspondence is a preset answer. Use masked candidates, rivals and evidence.
- **Scale**: evaluate 0.35–0.42 km/li as a range with sensitivity analysis, never a fixed 0.400 conversion.
- **Sections**: model each section independently. Cross-section links need textual or accepted relational evidence; summed li is not automatically geographic span.
- **Observer origin and anchors**: provisional candidates may seed the search as `initialization` anchors, with no evidential priority. Calibrate or replace them iteratively; only mutually confirmed landmarks become the consensus observer origin. Do not hardcode a conflated city datum.
- **v1 geography constraint**: Books 1–5 are the only source of new `MTN/WAT/LND` nodes. Books 6–18 must reuse those nodes. Unresolved mentions become `pending_anchor` and go to LLM adjudication; code must not create a replacement node or select a mapping.

## Foundational judgment logic for every corpus and agent

- **Static shape first**: compare outlines, relative positions, connections, enclosure, containment, branching and distribution before dynamic narratives. Preserve `出/入/注` in the text graph, but candidate comparison may use undirected `connected_to`; modern flow direction is not a standalone veto.
- **No causal inversion**: later names, commentary, boundaries and modern classifications cannot explain the earlier text's formation. Modern remains are comparison objects, not rules for how ancient observers had to write.
- **Ancient general semantics**: allow observer substitution and category generalisation symmetrically. Do not reject candidates through narrow modern taxonomy; sand dunes and built platforms may share the outlook of a mountain.
- **Cultural and historical discontinuity**: missing transmission chains are unknown, not evidence for or against a correspondence. Do not invent contacts, routes or motives.
- **Required order**: source evidence → static shape and physical features → ancient general semantics → period candidates → symmetric fit/contradictions → confidence and unknowns. Dynamic flow, later names and transmission mechanisms must not bypass this order.

## Required iterative pipeline

1. Establish the working text with stable entry IDs and reading status.
2. Extract entities, mentions, name semantics and textual relations.
3. Produce geographic semantic-fit attributes from masked competing candidates.
4. Assemble and validate the initial knowledge graph.
5. Complete the Five Mountain Classics draft without forcing a mapping where evidence is insufficient.
6. Supplement associative and deductive attributes in the graph.
7. Complete Books 6–18, then update the graph with later entities, reuse and anchoring relations.
8. Resolve semantic conflicts and merge/split through LLM decisions; update only the affected graph records and draft entries.
9. Iterate steps 1–8 as needed, then run completeness, sensitivity and independent red-team review before delivery and maps.

The authoritative details are `docs/research-framework.md` and `projects/shanhaijing/docs/methodology-spec.md`. Do not create a competing pipeline in another document.

## Research rules

- **Text first**: quotations are verbatim and carry entry IDs. Commentary and modern editorial claims never enter source-text evidence.
- **Layered assertions**: separate `textual`, `semantic_fit`, `associative` and `deductive` attributes; use `stated/proposed/accepted/contested/rejected` honestly.
- **Extensible ontology**: use `TYPE:SHJ-BB-S-EEE#n` node IDs and register predicates by entity type in `projects/shanhaijing/data/kg-ontology.json`.
- **Code versus LLM**: code performs snapshots, validation, calculations, coverage and conflict detection. LLM performs semantic extraction, candidate scoring, variant adjudication, merge/split and draft revision. Code never resolves semantic conflicts by heuristics.
- **No generated prose by scripts**: interpretation and reasoning are produced by LLM, not Python templates. Python may generate deterministic data products and verify counts.
- **Coverage is not correctness**: every entry and mention must be accounted for, but unresolved items remain explicit.
- **Reproducibility**: standard-library Python 3.9+, run from the repository root with `python3 -I`; preserve source manifests and judgment hashes.
- Commit each finished task. Keep one concern per commit and run the relevant validation before committing.

## Current state

Old interpretive drafts, maps, renderers and legacy graph outputs have been removed. The text pipeline has been rerun and its missing derived outputs restored. The new KG, drafts, semantic judgments and maps have not been generated. The era base remains seed data and no v4 red-team review has occurred.

## Layout

- `MEMORY.md`: current verified status and next actions, not a repository of conclusions.
- `docs/`: common framework, conventions, architecture and decision record.
- `reference/<corpus>/`: source snapshots, manifest, entries and clean reading text.
- `projects/<corpus>/docs/`: corpus specification, data model, tasks and review logs.
- `projects/<corpus>/data/`: era base, ontology and derived text/era/KG records.
- `projects/<corpus>/deliverables/`: future draft versions.
- `projects/<corpus>/findings/`: findings and LLM conflict-resolution log.
- `tools/<corpus>/`: standard-library text and validation tools.
