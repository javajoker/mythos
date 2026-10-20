# Mythos Whitepaper: Reading Ancient Texts in the World That Produced Them

> Version 3.0 · 2026-10-20 · [繁體中文](whitepaper.zh-Hant.md)

## Abstract

Much of humanity's earliest writing is filed under "myth", "legend" or "the strange". Some of it is pure imagination. Some of it may be **real observation in deformed form**, kept for centuries by retelling and copying. Mythos reads such a text as a **transmitted record**: a set of entities (places, waters, peoples, creatures, objects), what the text says about each, and how they relate. It rebuilds **the world of the period** in which the record accumulated (its coastlines, rivers, climate, animals, civilisations and their works) and looks for the most consistent correspondence between the two. Correspondence is judged **semantically**, attribute by attribute, by a large language model working on masked input, with every judgment recorded, and the judgments are solved jointly across the whole text.

The first object of study is the **Shanhaijing** 《山海經》, treated as a record accumulated between roughly 4000 and 2000 BCE and read from the Central Plains of China, its compilers' homeland. Its 869 paragraphs name about two thousand mountains, waters, peoples, creatures and objects, linked by itineraries, river courses and relative positions.

## 1. The problem

1. **Conclusion first.** Some readings confine the text to one region; others project it onto the whole world. Both usually start from an answer.
2. **The wrong map.** Comparing an ancient text with today's map ignores six thousand years of change: coastlines, rivers, deserts, animals and buildings were different.
3. **Names as evidence.** Identifications often rest on a modern name or a single striking feature.
4. **Irreproducibility.** The reasoning cannot be re-checked step by step.

## 2. Method: era-semantic correspondence

| Step | What happens |
|---|---|
| Original text | Only the earliest witness; commentary never enters; copying errors are tolerated and recorded |
| Entities and relations | Every entity, its description, its relations, and the meaning carried by its name (赤 = red), which never identifies it |
| Observer frame | Bearings and distances read from the compilers' origin, as soft constraints |
| World of the period | Coasts, rivers, climate, animals (including extinct ones), civilisations and their works, each dated |
| Semantic judgments | A language model proposes candidates and scores them attribute by attribute on masked input, with evidence, reasons and several samples; leakage probes and decoys guard against prior knowledge |
| Joint solving | The most consistent whole-text mapping, with confidence |
| Deliverable | Every paragraph and entity, and a map of the period |

The full method is in the [research framework](research-framework.md).

## 3. Why now

- The texts are digitised, often in several independent witnesses.
- Archaeology and palaeogeography describe the ancient world in enough detail to build a world of the period.
- Language models can judge semantic correspondence at scale, and every judgment can be recorded and audited.

## 4. Status

- The Shanhaijing text layer is complete: three witnesses, 869 paragraphs, the 1470 Chenghua order, and a finding that the common digital text silently relocates paragraphs ([F-0001](../projects/shanhaijing/findings/F-0001-base-text-modern-relocations.md)).
- The knowledge graph covers the whole book (1,943 entities, 2,741 relations) with a passing coverage audit.
- Framework v3, the world of 4000–2000 BCE, the specification, agents and skills are in place; a pilot on the Western books comes next, then the whole book (draft v4).
- A lesson from earlier versions (in git history): a candidate base that is richer for one region produces a clear but false result, so base balance and held-configuration tests against rivals are mandatory.

## 5. Scope and roadmap
Phase 1: the Shanhaijing era-semantic version. Phase 2: related Chinese texts. Phase 3: texts in other languages, sharing the same world of the period. Phase 4: astronomy and calendars. See the [roadmap](roadmap.md).

## 6. Non-goals
- No presupposed region, neither "China only" nor "the whole world".
- No identification by modern name or by fame.
- No result cited above its confidence tier.

## 7. Get involved
See the [PRD](prd.en.md), the [conventions](conventions.md) and the Shanhaijing [task list](../projects/shanhaijing/docs/tasks.md).
