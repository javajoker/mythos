# Mythos Product Requirements Document (PRD)

> Version 0.1 · 2026-10-19 · [繁體中文](prd.zh-Hant.md)

## 1. Background and goals

The Mythos "product" has three parts: a research method, a reproducible research database, and a set of AI research agents. The goal is that any researcher, human or agent, can propose a hypothesis about an ancient text, test it under one shared protocol, and get a graded, traceable, re-testable conclusion.

| Goal | Metric |
|---|---|
| G1 Every conclusion is traceable | 100% of findings cite entry IDs and source text; the reasoning chain can be reproduced by scripts or checklists |
| G2 No inherited conclusions | Every external theory is registered as `H-ext-*`; in evidence tables, "a prior author said so" cannot count as evidence |
| G3 The method is executable | Every stage of the methodology spec has a matching skill or script and a checkable gate |
| G4 Extensible to other texts | A new corpus only needs two adapters (ingest + structural extraction) to reuse the common layer |
| G5 Multilingual | Core docs exist in Traditional Chinese and English; a corpus in another language adds that locale |

## 2. Users

| Role | Needs |
|---|---|
| Researcher (human) | Propose hypotheses, review evidence and counter-evidence, adjudicate |
| AI research agent | Run collation, extraction, fitting and matching to spec; emit structured evidence records |
| Reviewer / red team | Hunt counter-examples, audit the correction budget, run sensitivity analysis |
| Reader | Read graded conclusions with their reasons and uncertainty |

## 3. Scope (Phase 1: Shanhaijing)

### 3.1 Must have (P0)

- **R1 Reference corpus**: at least three public-domain witnesses in `reference/shanhaijing/`, with provenance, licence and a re-fetch script. ✅
- **R2 Structured entries**: a citable ID (`SHJ-BB-S-EEE`) for every paragraph of all 18 books, keeping commentary, variants and modern editorial notes. ✅
- **R3 Collation**: a witness-variant table where each variant can be classified as orthographic, scribal error, substantive variant or displaced slip. ⏳ (machine alignment done; human classification pending)
- **R4 Itinerary extraction**: stations, bearings, distances, rivers and creatures of the Mountain Classics, plus a consistency check against the stated section totals. ✅ (v1)
- **R5 Methodology spec**: stages S0–S9, evidence grading, error model, correction budget, adjudication rules. ✅
- **R6 Hypothesis dossiers**: a template and checklist, and the first dossier, H-0001. ✅
- **R7 Agents & skills**: Shanhaijing-specific agents and skills, with a common layer extracted from them. ✅ (v1)

### 3.2 Should have (P1)

- **R8** Chain-fit tool: Monte Carlo projection from an anchor under the error model. ✅
- **R9** Hydrological topology graph: the whole-book "issues from / flows into" network, with consistency checks.
- **R10** Relative-position network for the Sea and Wilderness classics: extract relations like "A is east of B".
- **R11** Creature fingerprints: normalised morphology and behaviour descriptions, matched against taxon trait profiles.
- **R12** Geo and bio data adapters: DEM, river networks, GBIF, palaeoclimate.

### 3.3 Could have (P2)

- **R13** Interactive map (multiple hypotheses overlaid, residuals visualised)
- **R14** Cross-corpus: 穆天子傳, 淮南子・地形訓, 禹貢, 水經
- **R15** Adapters for texts in other languages

## 4. Functional requirements

| ID | Requirement | Acceptance |
|---|---|---|
| F1 | Ingest | `tools/shj/ingest.py` produces `entries.jsonl`, one record per paragraph, no markup left over |
| F2 | Collate | `collate.py` emits a variant table and summary; every variant is attributed to an entry |
| F3 | Extract | `extract_routes.py` emits stations, sections and a consistency report |
| F4 | Fit | Given an anchor, `chain_fit.py` emits predicted coordinates and a 90% radius for every station |
| F5 | Dossier | Every hypothesis directory has a `dossier.md` that passes every gate of the [checklist](../projects/shanhaijing/docs/checklist.md) |
| F6 | Findings | Each `findings/F-*.md` states its confidence level, the hypotheses it rests on, and its retraction conditions |

## 5. Non-functional requirements

- **Reproducible**: scripts use only the Python standard library and run with `python3 -I`; every random process uses a fixed seed.
- **Traceable**: all derived data can be regenerated from `reference/` plus the scripts.
- **Neutral**: the spec and agent prompts forbid picking the conclusion first; the red team is a mandatory step.
- **Licensing**: code and docs are Apache-2.0; the classical texts are public domain; Wikisource transcriptions are attributed under CC BY-SA 4.0.

## 6. Milestones

| Milestone | Content | Status |
|---|---|---|
| M0 | Repo skeleton, reference corpus, overall docs | ✅ |
| M1 | Shanhaijing methodology spec, pipeline v1, H-0001 | ✅ |
| M2 | Human classification of variants; canonical working text in the original order of the 1470 Chenghua edition | todo |
| M3 | Relative geometry and hydrology reconstructed for all 26 Mountain-Classic sections | todo |
| M4 | Candidate-region generation and multi-axis fitting (≥3 competing frames) | todo |
| M5 | Relative-position network for the Sea and Wilderness classics | todo |
| M6 | Common layer v1; a second corpus ingested | todo |

## 7. Risks

| Risk | Mitigation |
|---|---|
| Confirmation bias (looking only for support) | Pre-registration, mandatory competing hypotheses, red-team agent, base-rate correction |
| Over-emendation | Correction budget; every emendation is logged in the dossier |
| Base text carries modern editorial changes | Multi-witness collation; the working text follows the earliest witness's order |
| Wrong external facts | External facts must cite a source, otherwise they are tagged `needs-citation` and score nothing |
| Unknown length of the 里 | No fixed 里 length; anchor it inside the text, or treat it as a Monte Carlo parameter |
