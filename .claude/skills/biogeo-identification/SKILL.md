---
name: biogeo-identification
description: Identify creatures and plants described in ancient texts and myths, and use their geographic ranges and migration routes as location evidence — decompose descriptions into feature vectors, list ≥3 candidate taxa with fit tables, check habitat consistency, apply corpus base rates for stock motifs (e.g. human-faced composites), and score candidate regions by range, palaeo-range and migration feasibility. Use whenever a text describes an animal, plant, or composite being and someone proposes what it is or where it lives.
---

# 生物鑑定與分佈 / Biological identification & biogeography

## 1. 分解 / Decompose
把描述拆成特徵向量。/ Split the description into a feature vector:
`body_analogy`（狀如X）· `parts`（部件 / parts）· `colour` · `sound` · `behaviour`（含遷徙 / incl. migration）· `habitat`（文本所在的站點和水體 / station and water body in the text）· `uses_omens`（功用和預兆，**不作為生物證據** / **never biological evidence**）

## 2. 候選分類群 / Candidate taxa (≥ 3)
用一張特徵對照表逐項標記 ✓ / ✗ / ~ / ?。候選至少要有一個「形態最像」的，和一個「棲地最合」的。/ Mark each feature in a fit table. Include at least one best-morphology and one best-habitat candidate.

## 3. 棲地一致性 / Habitat consistency
文本給出的棲地必須和分類群的生態相容，例如淡水或海水、山地或平原、夜行或日行。不相容時，有兩個選擇：(a) 換一個候選；(b) 提出「傳聞插入」錯誤模型（成本 T5），兩者都要記錄。/ The text's habitat must be ecologically compatible with the taxon. If not, (a) change candidate or (b) invoke a hearsay-insertion error model (T5 cost), and record which.

## 4. 基準率 / Base rate
在全語料中統計同類母題的頻率，例如「人面X身」、九尾、三首。母題越常見，作為指紋的獨特性越低。/ Count stock motifs across the corpus; the more common, the less distinctive.

## 5. 分佈與遷徙 / Range & migration
- 用分類群的分佈（GBIF 等資料庫，附查詢日期）為候選區打分。分佈遍及全球的分類群（例如飛魚）只能給 E0。/ Score regions by range (GBIF etc., with query date); cosmopolitan taxa score E0.
- **古分佈**：如果假設的年代分佈可能不同（例如全新世的氣候變化、人類造成的滅絕），要寫明並附來源。/ **Palaeo-range**: state and cite if the assumed date may differ.
- **遷徙可行性**：文本描述的移動路線（例如「從西海遊于東海」）必須在候選框架下有實際可行的通道，並符合該分類群已知的遷徙行為。/ **Migration feasibility**: a described route must be physically passable in the candidate frame and match known behaviour.

## 6. 評分 / Score
鑑定本身（是什麼）和地點證據（在哪裡）要分開評分；兩者都用 `hypothesis-adjudication` 的 E 等級。/ Score identity and location separately, both with `hypothesis-adjudication` E grades.

## 範例 / Example
`projects/shanhaijing/hypotheses/H-0001/dossier.md` §4.6（人面虎身的基準率 / base rate）和 §4.9（文鰩魚的分類群表、棲地矛盾、路線可行性 / taxon table, habitat conflict, route feasibility）。
