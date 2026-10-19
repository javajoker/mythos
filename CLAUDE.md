# Mythos — project instructions

Mythos tests ancient texts, myths and legends as possible records of real observations, using reproducible methods. The first sub-project is the Shanhaijing 《山海經》.

## Method: entity-graph cross-validation (the only current method)
1. Extract every entity of the whole book, merged and integrated (the whole book is always the baseline, never a single place).
2. For each entity: description, properties, and relations to other entities → knowledge graph.
3. Real-world candidates worldwide, several per entity if needed. Names in the text are symbols: never match modern names.
4. Cross-validate candidates through the relations; the mapping is the best-energy joint configuration; confidence = stability × (1 − e^(−margin)); tiers high / medium / low / tentative.
5. Deliver an item-by-item mapping of the original: every paragraph and every entity mention, with the reason when unmapped. The completeness check must PASS.

Specs: `docs/research-framework.md`, `projects/shanhaijing/docs/methodology-spec.md`, `projects/shanhaijing/docs/data-model.md`. Tasks: `projects/shanhaijing/docs/tasks.md`; pre-delivery checklist: `checklist.md`.

## Research rules
- **Text first**: every entity and relation carries entry IDs (e.g. `SHJ-02-3-006`) from `reference/<corpus>/data/entries.jsonl`; quotations are verbatim.
- **No inherited conclusions**: commentary (郭注) and prior scholarship are never evidence and never used to build candidates.
- **The world base is committed before scoring**; later changes need a stated reason and a full re-run. Never tune a weight toward a desired answer; a change needs a general reason and applies to the whole book.
- Distances and bearings are only a small-weight reference. Read by outlook and time (framework §3.1, rules R1–R7: waters are water bodies, mountains are outlooks, palaeo-features and relics count at a cost, map view of courses, 前 = east, observer substitution), for every candidate alike. Test a reading as a held configuration against rivals (`kg_sections.py`).
- Be direct about results, including when the evidence is insufficient or contradicts the user's own hypothesis. Never cite a tentative mapping as a finding.
- The Shanhaijing base text contains modern paragraph relocations; follow the 1470 Chenghua (`sbck`) order (`projects/shanhaijing/docs/source-assessment.md`).

## Layout
- `docs/`: overall docs (whitepaper and PRD as `zh-Hant`/`en` files; the other docs bilingual inline)
- `reference/<corpus>/`: sources, `data/entries.jsonl`, `text/*.md` (no interpretation)
- `projects/<corpus>/`: spec, data model, tasks, checklist, `data/world/` (real-world base), `data/derived/` (text layer and `kg/`), `deliverables/draft-vN/`, `findings/F-*`
- `tools/<corpus>/`: standard-library Python; run from the repo root with `python3 -I`
- `.claude/agents`: textual-critic, entity-extractor, world-candidate-scout, cross-validator, devils-advocate (common); shj-lead
- `.claude/skills`: source-ingest, witness-collation, entity-graph-extraction, world-candidate-generation, graph-cross-validation (common); shj-entity-mapping

## Commands
```bash
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/align_witness.py && python3 -I tools/shj/classify_variants.py && python3 -I tools/shj/extract_routes.py   # text layer
python3 -I tools/shj/kg_extract.py      # steps 1–2 + coverage audit
python3 -I tools/shj/kg_candidates.py   # step 3
python3 -I tools/shj/kg_crossval.py     # step 4 (~15 min)
python3 -I tools/shj/kg_sections.py     # section scan and joint hypotheses (~1 h)
python3 -I tools/shj/kg_sensitivity.py  # weight sensitivity (~40 min)
python3 -I tools/shj/kg_deliver.py      # step 5; fails unless complete
python3 -I tools/shj/cn_numerals.py     # self-test
```
Remove `tools/shj/__pycache__` before committing. Commit each finished task.

## Languages
Docs are in Traditional Chinese and English. When a corpus in a new language is added, add that language per `docs/conventions.md` §1. Never convert quotations to simplified characters or normalise variant glyphs.
