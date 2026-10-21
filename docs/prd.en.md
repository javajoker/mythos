# Mythos Product Requirements Document v4

> Version 4.0 · 2026-10-21 · [繁體中文](prd.zh-Hant.md)

## 1. Product and goals

Mythos provides an iterative era-semantic method, a reproducible research database, and specialised AI research agents. Anyone should be able to regenerate, inspect and challenge an item-by-item correspondence between an ancient text and its period world.

| Goal | Acceptance metric |
|---|---|
| G1 Coverage | Every paragraph and entity mention is accounted for, including unresolved items |
| G2 Traceability | Every entity, attribute, relation, judgment and decision links to source evidence |
| G3 No inherited answers | Commentary is excluded; correspondences arise from masked competing candidates |
| G4 Period truth | Candidates exist or are visible within 4000–1000 BCE and carry dates and state |
| G5 Honest confidence | Mappings retain rivals, evidence, confidence and counter-evidence; unknown is not zero |
| G6 Reproducibility | Source hashes, rerunnable tools and hashed judgment inputs |
| G7 Extensibility | Predicates are registered by entity type; common agents contain no corpus answers |

## 2. First-version requirements

| ID | Requirement | Acceptance |
|---|---|---|
| R1 Source | Three witnesses, 869 stable entries, snapshot manifest, Chenghua order and reading status | Local hashes verify; only confirmed readings are formal evidence |
| R2 Text graph | Entities, mentions, name semantics and textual relations from working text | Per-entry coverage with explicit misses |
| R3 Era base | Dated and sourced geography, fauna, cultures and works | Out-of-window candidates rejected; symmetric coverage |
| R4 Semantic fit | Source → static shape → ancient general semantics → period candidates → symmetric evaluation, with at least three candidates from two macro-regions and recorded samples | No acceptance without rivals; modern flow, later names, missing transmission and narrow modern taxonomy are not standalone vetoes; leakage and decoy checks |
| R5 Initial graph | `nodes/mentions/edges/attributes` with typed ontology | Schema, references, types and v1 geography constraint pass |
| R6 Iterative drafts | Base draft → enriched attributes → later books → graph update | Text, hypotheses and unresolved items remain distinct |
| R7 LLM adjudication | Evidence-backed merge, split, variant and revision decisions | Code detects/executes only; human > LLM > automatic proposal |
| R8 Delivery | `deliverables/draft-v1/`, comparison, conflict log and rebuilt maps | Completeness, sensitivity and red-team review pass |

### SHJ v1 constraints

- Only Books 1–5 may introduce geographic nodes. Books 6–18 reuse them or remain `pending_anchor`.
- Scale is fitted over **0.35–0.42 km/li** with sensitivity analysis.
- Sections start independently. Cross-section links need evidence; summed distance is not automatically span.
- Observer origin is inferred from mutually confirmed landmarks and registered by stable ID.

## 3. Non-functional requirements

- Keep `textual`, `semantic_fit`, `associative` and `deductive` assertions separate.
- Register predicates by entity type, with evidence, status and provenance.
- Use standard-library Python 3.9+, `python3 -I`, sorted outputs and input-hash caching.
- Modern names and fame are not evidence; equivalent candidates use equivalent rules.
- Code and documentation are Apache-2.0; ancient texts are public domain; Wikisource transcriptions are CC BY-SA 4.0.

## 4. Milestones

| Milestone | Content | Status |
|---|---|---|
| M0 Cleanup and specifications | Legacy outputs removed; framework, SHJ specification, data model and ontology v4 | Done |
| M1 Text foundation | Manifest, 869 entries, collation, working text, variants and routes | Generated; formal readings still require confirmation |
| M2 Text graph | Full-book entities, mentions and textual relations | Todo |
| M3 Semantic fit and KG v1 | Era cards, candidates, judgments, anchor consensus and initial graph | Todo |
| M4 Iterative drafts | Base draft, enriched attributes, later books and graph update | Todo |
| M5 Conflicts and delivery | LLM merge/split, red team, draft-v1 and rebuilt maps | Todo |
| M6 Second corpus | Onboard without changing common agents or skills | Todo |

## 5. Risks

Predetermined answers, unconstrained semantic fitting, era-base bias, mixed fact and inference, programmatic semantic adjudication, and overstatement are handled respectively by masking and rivals, relation and falsifiability checks, symmetric cards, typed assertion layers, LLM decisions with human review, and explicit confidence tiers.
