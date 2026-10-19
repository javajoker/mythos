---
name: graph-cross-validation
description: Cross-validate real-world candidates through the relations of a knowledge graph — choose all entity mappings jointly so that descriptions and relations fit best (rarity-weighted own scores plus relation factors, soft uniqueness, simulated annealing with block moves), then measure stability by re-solving with relations dropped and report confidence, tier, supporting and violated relations, and alternatives for every entity. Use for step 4 of the entity-graph method, when a mapping looks inconsistent, or when asked "how confident is this mapping?".
---

# 圖譜交叉驗證 / Graph cross-validation（步驟 4）

## 模型 / Model
- 每個可對應的實體是一個變數，值為它的候選之一。/ Each mappable entity is a variable over its candidates.
- **總分** E = Σ 自身分數 + Σ 關係因子 − 唯一性懲罰。/ **Energy** E = Σ own + Σ relation factors − uniqueness penalty.
- 關係因子（山海經的權重見規格 §5）：`flows_into`（候選的河口正是目標 +2.0；同區 +0.3；否則 −1.0；目標為「庫中沒有」而來源的真實河口在庫中 −1.0；自注 −2.0）、`rises_at`、`next`（同區、相鄰、不相鄰）、`has_creature`（物種分佈）、`located`/`sees`（方位，小權重）、`sinks_at`（內流）。距離只作小權重參考。/ Distances are only a small-weight reference.
- **唯一性**：兩條書中河流對到同一條真實河流，每對扣 UNIQ（山海經 2.0）。/ **Uniqueness**: UNIQ per pair of book rivers on one real river.

## 解讀規則 / Reading rules（framework §3.1）
同一套寬容給所有候選，每一種寬容都要付一點代價：R1 水只是水體（類型不同小扣分）；R2 時間深度（古水體、遺跡，需資料來源，小扣分）；R3 山只是外觀（自然山、沙丘、方山、高大建築）；R4 外觀與效果（例：投物輒然 = 火或酷熱）；R5 方位慣例（前 = 東為主，前 = 南為對照）；R6 地圖讀法（出／流是地圖上的線，不一定是源頭與流向）；R7 觀察者替代（獅 → 虎）。/ The same leniency for every candidate, each at a small cost.

## 求解 / Solving
1. 模擬退火（多條鏈、固定種子；一半提議由關係引導：例如「注入 X」就提議 X 的真實支流）。/ Simulated annealing, fixed seeds; half the proposals relation-guided.
2. ICM 收尾（平手時保留現值）。/ ICM polish (ties keep the current value).
3. **區塊調整**：把一條河設成某候選，同時重配它相鄰的河、發源的山與山的鄰站，總分上升才接受。單點更新無法完成這種整體移動。/ **Block moves**: set one river, re-fit its neighbouring rivers, source mountains and their stations; keep only if E rises.
4. 對應 = 總分最高的組態（不要用逐實體多數決：各自的贏家拼不起來）。/ Mapping = best-energy configuration, never per-entity majority votes.

## 假說檢驗 / Hypothesis tests
把一個解讀寫成**固定組態**（`--init 基準 --fix {實體: 候選}` 或 `--scan [組態…]`）：固定的實體只保留假說的候選，其餘全書以 ICM 與區塊調整重新擬合；與不固定的基準及**對立組態**比較 ΔE，並列出被違反的關係。篇段掃描（每一篇 × 每一地區）就是全書的篇段層級地圖。/ A reading becomes a held configuration; compare ΔE with the free baseline and with rivals, and list broken relations. A section × region scan is the section-level map.

## 可信度 / Confidence
- 樣本 = 全部完整鏈 + 多次「丟棄 20% 關係」的重解。穩定度 = 樣本中與對應一致的比例。/ Samples: all full chains plus re-solves with 20% of relations dropped; stability = agreement share.
- 領先幅度 = 該實體最佳與次佳候選的局部分差。可信度 = 穩定度 × (1 − e^(−幅度))。/ Confidence = stability × (1 − e^(−margin)).
- 級別：高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、暫定 < 0.1（不宜引用）。河流另報水系層級的穩定度。/ Tiers: high, medium, low, tentative; rivers also get system-level stability.

## 必做檢查 / Mandatory checks
- **確定性**：同一輸入連跑兩次，輸出逐位元相同（集合要排序；隨機只能來自固定種子）。/ **Determinism**: two runs, identical bytes.
- **單調性**：任何「只在變好時接受」的步驟都不能讓總分下降；若下降就是記帳錯誤。/ **Monotonicity**: an accept-if-better step must never lower E.
- **一致性抽查**：原文說「A 注于 B」，A 與 B 的對應是否同一水系？不一致時查是哪個群聚（河 + 山 + 鄰站）把它拉走。/ **Consistency spot-checks** against the text's own statements.
- **庫的偏差**：結果是否偏向資料較密的河或地區？/ **Base bias** toward densely described rivers or regions.
- **對稱**：解讀規則的寬容是否也給了對立的候選？/ **Symmetry**: was every leniency also given to the rivals?

## 山海經實作 / Shanhaijing implementation
`tools/shj/kg_crossval.py` → `kg/mapping.jsonl`、`kg/crossval-log.json`；`kg_sensitivity.py`（權重變體）；`kg_sections.py`（篇段掃描與聯合假說）。規格 §5、§5.1、§5.2。
