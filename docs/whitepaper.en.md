# Mythos Whitepaper: Reading Ancient Texts in the World That Produced Them

> Version 4.0 · 2026-10-21 · [繁體中文](whitepaper.zh-Hant.md)

## Abstract

Ancient texts may contain imagination, but they may also preserve transformed observations. Mythos treats them as transmitted records: it extracts entities, descriptions and relations, reconstructs the world of their period, and compares rival correspondences with reproducible evidence.

The first object of study is the **Shanhaijing 《山海經》**, with a first-version period window of **4000–1000 BCE**. We presuppose neither a China-only nor a global interpretation. Every real-world correspondence must compete against alternatives.

## 1. Problems addressed

1. **Conclusion first**: bending the text to a predetermined answer.
2. **The wrong period map**: ignoring historical coasts, rivers, climate, fauna and built landscapes.
3. **Names as evidence**: replacing a complete comparison with modern-name similarity or one striking feature.
4. **Mixed assertion layers**: confusing textual statements with semantic fits, associations and deductions.
5. **Irreproducibility**: losing the provenance of sources, judgments, conflicts and generated outputs.

## 2. Iterative era-semantic correspondence

The pipeline is: working text → entity extraction → geographic semantic-fit attributes → initial graph → base-section draft → associative and deductive attributes → later sections and graph update → LLM conflict adjudication and merging → iteration → red-team-reviewed delivery and maps.

For the first SHJ version, geographic mentions in Books 6–18 must reuse nodes from the Five Mountain Classics. This is a graph constraint, not a predetermined geographic answer. Distances are evaluated over **0.35–0.42 km/li**. Sections start independently; cross-section links require evidence.

## 3. Auditable division of labour

Code handles source manifests, structural validation, alignment, calculations, coverage and conflict detection. LLMs handle semantic extraction, candidate scoring, reading and interpretation decisions, merge/split decisions and targeted draft revisions. Human review overrides LLM decisions; LLM decisions override automatic proposals.

Every judgment records model, prompt version, sample, input hash, evidence and reasons. Unchanged inputs are not re-judged, and identical data should regenerate identical outputs.

## 4. Current state

- Three witnesses, 869 stable entries and source SHA-256 manifests are preserved.
- Collation, working text, variant classifications and mountain itineraries have been regenerated.
- Base readings remain explicitly unreviewed; alignment is not reading confirmation.
- Legacy interpretive drafts, maps and graph outputs have been removed; v4 replacements have not been generated.
- The era base remains seed data, and no v4 red-team review has occurred.

## 5. Scope and non-goals

The first milestone is a complete, reviewed SHJ draft and graph. Only then should the common layer be reused for other Chinese and multilingual corpora.

Mythos does not presuppose a region or a specific correspondence, use modern names or fame as evidence, treat summed itinerary distances as automatic geographic spans, replace LLM semantic adjudication with heuristics, or present coverage and similarity as proof.

See the [research framework](research-framework.md), [PRD](prd.en.md), and [roadmap](roadmap.md).
