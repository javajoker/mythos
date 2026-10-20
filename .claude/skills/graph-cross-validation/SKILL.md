---
name: graph-cross-validation
description: Solve an ancient text's mapping jointly — turn semantic judgment records and computable relations into own and relation scores, choose all entity mappings at once for the most consistent whole-text configuration (rarity weighting, capped contradictions, soft uniqueness, simulated annealing with ICM and block moves), measure confidence from re-solves, judgment spread and leakage, and test readings as held configurations against rivals. Use for the solving step of the era-semantic method, when a mapping looks inconsistent, or when asked "how confident is this mapping?" or "does this reading hold?".
---

# 聯合求解與可信度 / Joint solving and confidence（框架 v3 §5、規格 §7–§9）

## 分數 / Scores
- **自身分數**：由判斷紀錄計算：Σ 維度權重 × 吻合 × 罕見度 − Σ min(矛盾, 0.5) + 名稱特徵 × 較低權重；判斷標準差大的維度降權。/ From judgment records, rarity-weighted, capped contradictions, down-weighted name features.
- **關係分數**：可計算的（注入、發源、相鄰、方位、同區）在**當時**的地理上計算，套用解讀規則 R1–R6；需語義的（環之、其外有、濱、望見、居）取自關係判斷；相鄰實體年代相差過大時扣分（R8）。/ Computed on period geography or taken from relation judgments; date gaps cost.
- **唯一性**：兩個書中實體對到同一真實實體，每對扣分。/ Uniqueness penalty.

## 求解 / Solving
1. 模擬退火（多條鏈、固定種子；一半提議由關係引導）。/ Annealing, relation-guided proposals.
2. ICM 收尾（平手保留現值）。/ ICM polish.
3. **區塊調整**：一個實體連同相鄰實體（例：一條水與它的源山、鄰站）一起換候選，總分上升才接受。/ Block moves.
4. 對應 = 總分最高的組態；不用逐實體多數決。/ Best-energy configuration.

## 可信度 / Confidence
可信度 = 穩定度（完整求解與略去 20% 關係的重解中一致的比例）× (1 − e^(−邊際)) × (1 − 判斷標準差) × 洩漏折扣。級別：高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、暫定 < 0.1（不宜引用）。/ Confidence and tiers.

## 假說檢驗 / Hypothesis tests
把一個解讀寫成**固定組態**：固定的實體只保留假說的候選，其餘全書重新求解；與自由解、至少兩個對立組態、一個誘餌比較總分，並列出被違反的關係。篇段 × 遺址或地區的掃描就是當時的篇段地圖。/ Held configurations against the free solution, rivals and a decoy; section scans.

## 必做檢查 / Mandatory checks
- **確定性**：同一輸入兩次執行，輸出逐位元組相同。/ Determinism.
- **單調性**：「變好才接受」的步驟不得讓總分下降。/ Monotonicity.
- **一致性抽查**：原文說「A 注于 B」「X 在 Y 西」，對應中是否成立；不成立時找出把它拉走的群聚。/ Spot-check the text's own statements.
- **庫的偏差與對稱**：結果是否偏向候選卡較詳細的地區或文明；寬容是否也給了對立候選。/ Base bias and symmetry.

## 山海經實作 / Shanhaijing implementation
`tools/shj/era_solve.py`、`era_sensitivity.py`、`era_sections.py`（試點中建立；求解器改寫自 git 歷史中的 `kg_crossval.py`）。規格 §7–§9。
