---
name: toponym-triangulation
description: Locate places named in ancient texts by multi-channel triangulation — fingerprinting each place from the text (terrain, hydrology topology, sight-lines, relative positions, climate cues), generating candidate regions blindly worldwide, fitting relative geometry/constraint networks to each candidate, and scoring residuals. Use when asked where a mythical/ancient place "really" is, to generate rival candidates for a hypothesis, to solve "A is east of B" relation networks, or to test a proposed identification on the GEO/HYD/TER channels.
---

# 地名交叉定位 / Toponym triangulation

## 1. 指紋 / Fingerprint (text only)
對每個地點，只從文本中收集以下資訊，每項都附條目編號。/ For each place collect, from the text only and with entry IDs:
- 地形：山、丘、沙、澤、火、石門、深淵 / terrain: mountain, mound, sand, marsh, fire, stone gate, abyss
- 水系拓撲：發源、流向、匯入、伏流、內流 / hydrology topology: source, direction, mouth, sinking, endorheic
- 相對位置：鏈條方位與距離、「A 在 B 某方」、望見關係 / relative position: chain bearings and distances, "A is <dir> of B", sight-lines
- 氣候和天象：寒暑、風雨、日月出入 / climate and sky: seasons, winds and rain, sunrise and sunset points
- 生物和礦產（交給 `biogeo-identification` 和礦產表）/ biota and minerals (via `biogeo-identification` and the mineral table)

## 2. 盲候選生成 / Blind candidate generation
- **先生成，再看假說**：用指紋中最具區分力的 2–3 項，在全球範圍內篩選候選區，過程要記錄（查詢條件和篩選理由）。/ **Generate before looking at hypotheses**: filter worldwide on the 2–3 most discriminating features, and log the queries and reasons.
- 候選必須包含：本地框架、至少一個遠距框架，以及虛無假說（想像、拼合或圖像衍生）。/ Must include a local frame, ≥ 1 distant frame and the null.
- 不查閱前人比定，避免錨定效應。/ Do not consult prior identifications (anchoring).

## 3. 擬合 / Fit
- **鏈條**：錨定一點，以蒙地卡羅投影其餘各點（方位 ±22.5°，距離 σ = 0.30，單位長度不預設）；兩個錨點時反推單位長度。/ **Chains**: anchor one point and project the rest by Monte Carlo; with two anchors back-calculate the unit.
- **關係網路**：把「A 在 B 東」轉成不等式約束，求可行佈局；在候選世界圖上計算違反約束的數目。/ **Relation networks**: turn "A is east of B" into inequality constraints, solve for feasible layouts, count violations on the candidate map.
- **水系同構**：比較文本的有向河流圖與候選區的實際排水網路，看源頭、流向、匯入點、內流盆地是否對應。/ **Hydrological isomorphism**: compare the text's directed river graph with the candidate's real drainage.

## 4. 評分 / Score
每個通道分開評分，給出 E 等級、對照集和 log₁₀ LR（`hypothesis-adjudication`）。預測位置的地面條件，例如「此處需要一條向西的河」，必須逐站寫出並判定。/ Score each channel separately. Spell out and judge the ground requirement at every predicted station.

## 5. 年代 / Date
假說要寫明所假設的觀測年代；若需要的環境只在別的年代存在（例如古河道、海平面、綠色撒哈拉），必須另外論證文本有那麼古老。/ State the assumed observation date; if the required environment existed only at another date, the age must be argued separately.

## 山海經實作 / Shanhaijing implementation
`tools/shj/chain_fit.py`；skill `shj-itinerary-reconstruction`；範例 / example: `projects/shanhaijing/hypotheses/H-0001/`.
