---
name: entity-graph-extraction
description: Turn an ancient text into a knowledge graph — find every entity (places, waters, peoples, creatures, plants, minerals, persons), merge variants and homonyms, record each entity's description and properties, and extract the relations between entities (adjacent, rises at, flows into, located, sees, produces, begets…), with a coverage audit proving no paragraph or name pattern was missed. Use for steps 1–2 of the entity-graph method on any corpus, or when asked to "extract all entities", "build the knowledge graph", or "check that nothing is missed".
---

# 實體圖譜抽取 / Entity-graph extraction（步驟 1–2）

## 原則 / Principles
- **名稱只是符號。** 抽取時保留原文寫法，不把它改成今名，也不因為名字相同就認定是同一地點。/ **Names are symbols.** Keep the text's spelling; never convert to a modern name or assume identity from a shared name.
- **全書為基準。** 每一段都要有實體；每一個實體都要回指段落編號。/ **The whole book is the baseline**: every paragraph has entities, every entity points back to paragraph IDs.
- **描述優先。** 每個實體保存其描述原句與抽出的性質（礦物、植物、形態、習俗…），候選與計分只用這些。/ **Descriptions first**: keep each entity's source clauses and extracted properties; candidates and scoring use only these.

## 步驟 / Steps
1. **實體類型**：先為語料定義類型（例：山、水、地、國族、生物、植物、礦物、神人、未定、結構）與每類的句式。/ Define entity types and the sentence patterns that introduce each.
2. **抽取**：逐段跑句式；清理標點、前綴（又、其、曰…）與動詞尾巴；常見名詞（金、玉、松）走詞庫。/ Run the patterns paragraph by paragraph; strip punctuation, prefixes and trailing verbs; common nouns go through a lexicon.
3. **合併**：異體字摺疊；同名但在不同篇、不同路線的山分開；同名河流只在去向明確不同時拆分（不可自注）。總述（「凡…」）也要處理，並連回其總結的實體。/ Merge orthographic variants; keep same-name mountains in different sections apart; split homonym rivers only on clearly different destinations (never self-flow). Summaries are processed and linked to what they summarise.
4. **關係**：每條邊保存類型、方向、來源段落與原句；同一段同一關係只計一次。框架句（「X之南，Y之濱，Z之後，W之前，有…名曰S」）、包圍（「環之」）、外圍（「其外有」）都要抽出；方位慣例不確定時，保存另一種讀法（`alt_direction`）。常見類型：`next`、`rises_at`、`flows_into`、`sinks_at`、`located`（含「一曰」異說）、`sees`、`has_resource`、`has_creature`、`dwells`、`begets`、`same_name`、`summarizes`、`described_in`。/ Every edge keeps type, direction, source paragraph and clause.
5. **覆蓋檢查**：(a) 沒有實體的段落 = 0；(b) 每個名稱句式（曰X、X山、X水、X國、X民）要嘛已成實體，要嘛有明列的理由（數量、題記、泛稱、比喻、異說）；未解釋 = 0 才算通過。/ **Coverage audit**: paragraphs without entities = 0, and every name pattern is either an entity or explained by a listed reason; pass only at 0 unexplained.
6. **輸出**：`nodes.jsonl`、`edges.jsonl`、`mentions.jsonl`、GraphML、`coverage.md`；集合一律排序後輸出，結果可重現。/ Sort every set before output; results must be reproducible.

## 常見陷阱 / Pitfalls
比喻（「其狀如山雞」不是山）、篇名（「西山經華山之首」的山名是「華山」）、洪水用語（「天下大水」不是水體）、自注迴圈、把生物名誤當地名、以動物部件描述的神（「有神，人面鳥身…名曰禺彊」是神，不是生物）、地名前的方位字（「西海」不是「海」）、沒有「注」字的水道（「西流于大杅」）。修正後重跑覆蓋檢查。/ Similes, range headings, flood idioms, self-loops, creature names taken as places; re-run the audit after each fix.

## 山海經實作 / Shanhaijing implementation
`tools/shj/kg_extract.py`（`tools/shj/cues.py` 為描述線索）→ `projects/shanhaijing/data/derived/kg/`。規格：`projects/shanhaijing/docs/methodology-spec.md` §2–3、§7。
