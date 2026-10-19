# Mythos Product Requirements Document (PRD)

> Version 2.0 · 2026-10-19 · [繁體中文](prd.zh-Hant.md)

## 1. Background and goals

The Mythos "product" has three parts: a method (entity-graph cross-validation), a reproducible research database (text, knowledge graph, real-world base), and a set of AI research agents. The goal is that anyone can regenerate, inspect and challenge a complete, item-by-item real-world mapping of an ancient text.

| Goal | Metric |
|---|---|
| G1 Nothing missed | The deliverable covers 100% of paragraphs and entity mentions; unmapped items state a reason |
| G2 Traceable | Every entity, relation and mapping links to entry IDs and the source clause |
| G3 No inherited conclusions | Commentary and prior theories are never evidence; names never score |
| G4 Honest confidence | Every mapping carries confidence, tier, supporting and violated relations, and alternatives |
| G5 Reproducible | Two runs give byte-identical outputs |
| G6 Extensible and multilingual | A new corpus needs two adapters (ingest, entity patterns); each new language adds a doc locale |

## 2. Users

| Role | Needs |
|---|---|
| Researcher (human) | Read the mapping, ask "where is X", challenge an item, extend the world base |
| AI research agent | Run extraction, candidate generation, cross-validation and delivery to spec |
| Reviewer / red team | Find counter-examples, decoys, base bias and overstated confidence |
| Reader | Read the mapping with its confidence and limits |

## 3. Scope (Phase 1: Shanhaijing)

### 3.1 Must have (P0)

- **R1 Reference corpus**: three public-domain witnesses with provenance and a re-fetch script. ✅
- **R2 Structured entries**: a citable ID for each of the 869 paragraphs. ✅
- **R3 Collation**: variants attributed to entries and classified (draft policy); modern relocations registered. ✅
- **R4 Knowledge graph**: every entity and relation of the whole book, with a coverage audit at zero unexplained misses. ✅
- **R5 World base and candidates**: worldwide regions, waters, animals and cultures; multiple candidates per entity. ✅
- **R6 Cross-validation**: joint solution with confidence, tiers and alternatives; deterministic. ✅
- **R7 Deliverable**: per-book, per-paragraph mapping with a completeness check. ✅ (draft v1)
- **R8 Agents and skills**: common layer plus the Shanhaijing lead and runbook. ✅

### 3.2 Should have (P1)

- **R9** Base balance (comparable detail per river and region) and a re-run. 
- **R10** Weight sensitivity report.
- **R11** Red-team review of each draft.
- **R12** More relations for the Sea and Great Wilds books (bearings, adjacency).

### 3.3 Could have (P2)

- **R13** Interactive map of the mapping with confidence and alternatives.
- **R14** Cross-corpus graphs (穆天子傳, 淮南子・地形訓, 禹貢, 水經).
- **R15** Adapters for texts in other languages.

## 4. Functional requirements

| ID | Requirement | Acceptance |
|---|---|---|
| F1 | Ingest | `ingest.py` produces `entries.jsonl`, one record per paragraph |
| F2 | Collate | `collate.py`, `align_witness.py`, `classify_variants.py` produce the variant table, working text and displacements |
| F3 | Extract | `kg_extract.py` writes nodes, edges, mentions, GraphML and a coverage audit with 0 paragraphs without entities and 0 unexplained name patterns |
| F4 | Candidates | `kg_candidates.py` gives every mappable entity its candidates with own scores |
| F5 | Cross-validate | `kg_crossval.py` writes a mapping with confidence, tier, supporting and violated relations and sample alternatives |
| F6 | Deliver | `kg_deliver.py` writes the per-paragraph files and fails unless paragraphs and mentions written equal those in the text |

## 5. Non-functional requirements

- **Reproducible**: Python standard library only, `python3 -I`, fixed seeds, sorted outputs.
- **Neutral**: the world base is committed before scoring; weight changes need a general reason and apply to the whole book.
- **Licensing**: code and docs Apache-2.0; classical texts public domain; Wikisource transcriptions attributed under CC BY-SA 4.0.

## 6. Milestones

| Milestone | Content | Status |
|---|---|---|
| M0 | Repo skeleton, reference corpus, overall docs | ✅ |
| M1 | Text layer: collation, working text, relocations | ✅ |
| M2 | Knowledge graph of the whole book with a passing coverage audit | ✅ |
| M3 | World base, candidates, cross-validation | ✅ |
| M4 | Deliverable draft v1 | ✅ |
| M5 | Base balance, sensitivity, red team → draft v2 | todo |
| M6 | A second corpus on the common layer | todo |

## 7. Risks

| Risk | Mitigation |
|---|---|
| Base bias (detailed regions or rivers attract mappings) | Balance checks, uniqueness penalty, unknowns at base rate |
| Extraction errors create false relations | Coverage audit, explained categories with examples, spot checks against the text |
| Multimodal solutions | Several chains, block moves, stability from re-solves; tentative tier |
| Over-reading weak results | Tiers in every table; README wording checked against tiers |
| Base text carries modern editorial changes | Multi-witness collation; working text in earliest-witness order |
