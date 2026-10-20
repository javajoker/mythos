# Mythos Product Requirements Document (PRD)

> Version 3.0 · 2026-10-20 · [繁體中文](prd.zh-Hant.md)

## 1. Background and goals

The Mythos "product" has three parts: a method (era-semantic correspondence, framework v3), a reproducible research database (original text, knowledge graph, world of the period, judgment records), and a set of AI research agents. The goal is that anyone can regenerate, inspect and challenge a complete, item-by-item mapping of an ancient text onto the world of its period.

| Goal | Metric |
|---|---|
| G1 Nothing missed | The deliverable covers 100% of paragraphs and entity mentions; unmapped items state a reason |
| G2 Traceable | Every entity, relation, judgment and mapping links to entry IDs and the source clause |
| G3 No inherited conclusions | Commentary and prior scholarship are never input; judgments run on masked input; leakage is measured |
| G4 Period-true | Every candidate exists or is visible in the period window, with its dates and state |
| G5 Honest confidence | Every mapping carries confidence, tier, evidence and rivals |
| G6 Reproducible | Tools give byte-identical outputs; judgments are recorded and re-run only on change |
| G7 Extensible and multilingual | A new corpus needs an ingest adapter, entity patterns and a period window; each new language adds a doc locale |

## 2. Users

| Role | Needs |
|---|---|
| Researcher (human) | Read the mapping, ask "where is X", propose a reading and see it tested against rivals |
| AI research agent | Build the era world, judge candidates on masked input, solve, deliver |
| Reviewer / red team | Find leakage, decoy failures, modern-name matching, asymmetry, date errors |
| Reader | Read the mapping and the map of the period with confidence and limits |

## 3. Scope (Phase 1: Shanhaijing, era-semantic version)

### 3.1 Must have (P0)
- **R1** Original text: three witnesses, 869 paragraphs, Chenghua order; commentary excluded from analysis. ✅
- **R2** Knowledge graph of the whole book with a coverage audit at zero unexplained misses. ✅
- **R3** Name features (colour, material, shape, state, direction) for every entity.
- **R4** Observer frame from the Central Plains with soft bearing and distance constraints.
- **R5** Era world base 4000–2000 BCE: sites and works (Mesopotamia, Harappa, Egypt in focus, contemporaries as rivals), waters, fauna including extinct species, cultures, coastlines of the period.
- **R6** Masked semantic judgments with evidence, reasons and three samples; leakage probes and decoys.
- **R7** Joint solver on the judgments with confidence; held-configuration tests of readings.
- **R8** Deliverable draft-v4: every paragraph and entity, plus the map of the period, with a completeness check.

### 3.2 Should have (P1)
- **R9** Pilot on the four Western sections and 大荒西經 before the whole book.
- **R10** Weight sensitivity and red-team review of each draft.

### 3.3 Could have (P2)
- **R11** Interactive map of the period with the mapping and alternatives.
- **R12** Cross-corpus graphs (穆天子傳, 淮南子・地形訓, 禹貢, 水經).

## 4. Functional requirements

| ID | Requirement | Acceptance |
|---|---|---|
| F1 | Text layer | `ingest.py` … `extract_routes.py` produce entries, working text, variants, stations |
| F2 | Knowledge graph | `kg_extract.py`: 0 paragraphs without entities, 0 unexplained name patterns, name features present |
| F3 | Era base | `data/era/` cards each have dates, state and a general source; committed before scoring |
| F4 | Judgments | every record has masked input hash, model, prompt version, sample number, per-dimension evidence and reason |
| F5 | Solving | `era_solve.py` writes the mapping with confidence, tier, evidence and rivals; two runs identical |
| F6 | Deliverable | `era_deliver.py` fails unless paragraphs and mentions written equal those in the text; draws the era map |

## 5. Non-functional requirements
- Reproducible: Python standard library, `python3 -I`, fixed seeds, sorted outputs; judgments cached by input hash.
- Neutral: no presupposed region; symmetry for every leniency and kind of candidate; rivals in every comparison.
- Licensing: code and docs Apache-2.0; classical texts public domain; Wikisource transcriptions under CC BY-SA 4.0.

## 6. Milestones

| Milestone | Content | Status |
|---|---|---|
| M0 | Repository, reference corpus, overall docs | ✅ |
| M1 | Text layer | ✅ |
| M2 | Knowledge graph of the whole book | ✅ |
| M3 | Framework v3, era-world document, spec, agents, skills | ✅ |
| M4 | Pilot: name features, observer frame, era base, judgments, solver, review | todo |
| M5 | Whole book, draft-v4 with the map of the period, review | todo |
| M6 | A second corpus on the common layer | todo |

## 7. Risks

| Risk | Mitigation |
|---|---|
| The model's prior knowledge steers judgments | Masking, unmasked probes, decoys, rivals; leakage discounts confidence |
| Semantic matching fits anything | Rarity weighting, capped contradictions, joint solving across relations, held-configuration tests |
| Base bias toward well-described regions or focus civilisations | Symmetry rule, rivals, balance checks in every review |
| Wrong dates or period states | Every card dated; candidates outside the window excluded |
| Over-reading weak results | Tiers everywhere; tentative results never cited |
