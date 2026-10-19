# Mythos — project instructions

Mythos tests ancient texts, myths and legends as possible records of real observations, using falsifiable, reproducible methods. The first sub-project is the Shanhaijing 《山海經》.

## Non-negotiable research rules
- **Text first**: every claim cites an entry ID (e.g. `SHJ-02-3-006`) and a verbatim quote from `reference/<corpus>/data/entries.jsonl`.
- **No inherited conclusions**: commentary (郭注) and all prior scholarship are registered as hypotheses (`H-ext-*`), never used as evidence, and are not consulted during candidate generation.
- **Pre-register** predictions, falsifiers, correction budget and conventions before testing. Generate ≥ 2 rivals + the null. Always run the red team.
- Score evidence per `docs/research-framework.md` (channels, E grades with comparison sets, log₁₀ LR, correction budget, verdicts R/L0–L4). Uncited external facts score LR = 1 (`needs-citation`).
- Be direct about results, including refutations of the user's own hypotheses; always state the retained observations and the possible reformulations.
- The Shanhaijing base text contains modern paragraph relocations; use the 1470 Chenghua (`sbck`) order for relative-position reasoning (`projects/shanhaijing/docs/source-assessment.md`).

## Method G (description-first, global premise) — set by the initiator 2026-10-19
- Working premise: the book covers the whole Earth. Judge by descriptions only (mask names); distances/bearings are a small-weight reference.
- Pipeline: real-animal base → animal map (`tools/shj/creatures.py`, `animal_map.py`) → geo assumptions → in-book proof (`tools/shj/geo_match.py`) against ALL candidate loci in `projects/shanhaijing/data/world/loci.jsonl`.
- Score = rarity-weighted matches minus contradictions; report rankings, never a single place's match count. Write locus values before scoring.
- Spec: `projects/shanhaijing/docs/method-g-global.md`. Keep Method A results alongside; explain disagreements.

## Layout
- `docs/`: overall docs (whitepaper and PRD in `zh-Hant`/`en` files; the other docs bilingual inline)
- `reference/<corpus>/`: sources, `data/entries.jsonl`, `text/*.md` (no interpretation)
- `projects/<corpus>/`: spec, checklist, tasks, data model, `data/derived/`, `hypotheses/H-*/dossier.md`, `findings/F-*`
- `tools/<corpus>/`: standard-library Python scripts; run from the repo root with `python3 -I`
- `.claude/agents`, `.claude/skills`: common layer (textual-critic, geo-triangulator, naturalist, adjudicator, devils-advocate; source-ingest, witness-collation, toponym-triangulation, biogeo-identification, hypothesis-adjudication, description-first-matching) plus Shanhaijing layer (shj-lead, shj-route-reconstructor; shj-itinerary-reconstruction, shj-hypothesis-case, shj-global-locate)

## Commands
```bash
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/chain_fit.py --section 西次三經 --anchor 昆侖之丘 --lat <lat> --lon <lon>
python3 -I tools/shj/cn_numerals.py   # self-test
python3 -I tools/shj/creatures.py && python3 -I tools/shj/animal_map.py   # Method G animal map
python3 -I tools/shj/geo_match.py --target <regex> --entries <IDs> --pairs   # Method G place ranking
```

## Languages
Docs are in Traditional Chinese and English. When a corpus in a new language is added, add that language per `docs/conventions.md` §1. Never convert quotations to simplified characters or normalise variant glyphs.
