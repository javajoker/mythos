# Mythos Whitepaper: Mapping Ancient Texts to the Real World, Entity by Entity

> Version 2.1 · 2026-10-19 · [繁體中文](whitepaper.zh-Hant.md)

## Abstract

Much of humanity's earliest writing is now filed under "myth", "legend" or "the strange". Some of it is pure imagination. Some of it may be **real observation in deformed form**: records of places, rivers, species and peoples whose original frame of reference was lost through retelling, redrawing, recopying and translation. Mythos treats such a text as a **knowledge graph**: every entity it mentions, what it says about each one, and how the entities relate. It then searches the whole Earth for real-world candidates and lets the relations **cross-validate** them, producing a mapping of the entire text, item by item, with a confidence score for every item.

The first object of study is the **Shanhaijing** 《山海經》 (*Classic of Mountains and Seas*). Its 869 paragraphs name about two thousand mountains, waters, peoples, creatures, plants and minerals, and link them by adjacency, river courses ("rises at", "flows into") and relative bearings. That density of relations makes it an unusually good test case.

## 1. The problem

1. **Conclusion first.** Traditional commentaries confine the text to the Chinese heartland; modern "Shanhaijing is world geography" theses do the opposite. Both usually start from an answer and pick the entries that fit.
2. **Names as evidence.** Identifications often rest on a modern place that shares a name or a single striking feature, while the entity's other relations are ignored.
3. **One place at a time.** Testing one identification in isolation cannot tell whether the rest of the book still fits.
4. **Irreproducibility.** The reasoning is scattered and cannot be re-checked step by step.

## 2. Method: entity-graph cross-validation

| Step | What happens |
|---|---|
| 1. Entities | Extract every entity of the whole book and merge spelling variants and homonyms |
| 2. Descriptions and relations | Record each entity's description and properties, and every relation between entities, as a knowledge graph with entry IDs |
| 3. Candidates | For each entity, find real-world candidates **worldwide** (regions, rivers, lakes, seas, animals, ancient cultures) by description alone. **Names are symbols** and never score |
| 4. Cross-validation | Choose all mappings jointly so that descriptions and relations fit best; measure stability by re-solving with part of the relations dropped; confidence = stability × (1 − e^(−margin)) |
| 5. Deliverable | Map the original item by item: every paragraph, every entity, its mapping and confidence, or the reason it is unmapped. A completeness check must pass |

Distances and bearings are kept only as a small-weight reference; the relations that matter most are the structural ones, such as which river flows into which.

## 3. Why now

- **The texts are digitised**, often in several independent witnesses (for the Shanhaijing: the common Wikisource text, the 1470 Chenghua edition and the Siku Quanshu edition).
- **World data are open**: river networks, species ranges and archaeological cultures can be encoded as a real-world base.
- **AI agents** can carry out exhaustive extraction and checking under a strict protocol, and every step can be written as a deterministic script.

## 4. First results (Shanhaijing draft v3)

- **Nothing missed**: all 869 paragraphs and 4,004 entity mentions are mapped or explained ([deliverable](../projects/shanhaijing/deliverables/draft-v3/README.md)).
- **A clear result can come from a biased base.** Draft v1's "Yellow River" result depended on only Chinese rivers having tributaries listed, and was withdrawn after review ([red team](../projects/shanhaijing/docs/red-team.md)).
- **Readings are tested, not adopted.** The initiator's reading rules (waters are water bodies, mountains are outlooks, time depth, map view, orientation) apply to every candidate. A proposed reading (the West sections as Harappa, Sumer and Egypt) is held as a configuration and compared with rivals: it scores below China, a North America decoy and an Ethiopia rival, while its Kunlun paragraph alone is compatible with Egypt.
- **What survives**: 20 mappings are confident and robust, mostly distinctive creatures, plus 毛民 → Ainu and a few mountains in China.
- **The common digital text is not the original** ([F-0001](../projects/shanhaijing/findings/F-0001-base-text-modern-relocations.md)).

## 5. Scope and roadmap

- **Phase 1**: Shanhaijing: extract the remaining spatial relations, decide on new reading rules (map view of rivers, time depth, appearance vs behaviour), and test rival configurations such as Kunlun in Egypt.
- **Phase 2**: related Chinese texts (穆天子傳, 淮南子・地形訓, 禹貢, 水經) as more graphs whose shared entities add cross-book relations.
- **Phase 3**: texts in other languages (Mesopotamian, Egyptian, Vedic, Greek, Maya), each adding a documentation locale.

## 6. Non-goals

- No predetermined answer, neither "the Shanhaijing is global geography" nor "the Shanhaijing is only about China".
- No identification by name.
- No result cited above its confidence tier.

## 7. Get involved

See the [PRD](prd.en.md), the [research framework](research-framework.md), the [conventions](conventions.md) and the Shanhaijing [task list](../projects/shanhaijing/docs/tasks.md).
