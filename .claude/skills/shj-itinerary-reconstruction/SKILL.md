---
name: shj-itinerary-reconstruction
description: Reconstruct the relative geometry and river network of a Shanhaijing 五藏山經 section (stages S2–S4 of the Shanhaijing methodology spec) — extract stations/bearings/里 distances/rivers, check them against the section's own 凡N山N里 totals, explain discrepancies with the X1–X6 error model, and run unanchored or anchored Monte Carlo chain fits. Use when asked to "reconstruct 西次三經", "map a 山經 route", "check the 里 totals", "fit this chain to <place>", or when a Shanhaijing hypothesis needs its GEO/HYD channel evidence.
---

# 山經路線重建 / Mountain-Classic itinerary reconstruction

適用規格 / Spec: `projects/shanhaijing/docs/methodology-spec.md` §2 (S2–S4), §4, §6.3–6.4, §7.1–7.2.

## 不可違反 / Non-negotiable
- 只用文本自身的方位與里程；**不預設**任何站點的現代位置，也不預設里長。/ Use only the text's bearings and distances; **never assume** a station's modern location or the 里 length.
- 前人比定（郭注、現代學者）不得作為輸入。/ Prior identifications are not inputs.
- 抽取錯誤 ≠ 文本錯誤：先排除抽取器的問題，再提出 X1–X6。/ An extraction error is not a text error: rule out extractor problems before invoking X1–X6.

## 步驟 / Steps

1. **重新產生資料 / Regenerate**
   ```bash
   python3 -I tools/shj/ingest.py && python3 -I tools/shj/extract_routes.py
   ```
2. **讀取該篇 / Load the section**：從 `projects/shanhaijing/data/derived/stations.jsonl` 篩出 `section == <篇名>`，並對照 `reference/shanhaijing/text/NN-*.md` 的原文。/ filter by section and compare against the source text.
3. **站數核對 / Station count**：抽取的站數與 `sections.jsonl` 的 `stated_mountains` 比較。不符時，逐段讀原文，找出被漏抓的站點，例如一段之內「二百里至于蠃母之山」這樣的第二站。/ compare with `stated_mountains`; if different, read each paragraph for missed stations such as a second station inside one paragraph.
4. **里程核對 / Distance check**：Σ`leg_li` 對 `stated_li`。每個差異寫一行解釋：抽取錯誤 / X1 數字訛誤 / X4 站點脫漏 / 未解，附上條目編號。/ one line per discrepancy with entry ID.
5. **水系圖 / River graph**：把 `rivers[]` 轉成有向邊 `river: station → to`。同名河流在全書歸併；列出懸空節點，即只被注入、卻沒有出處的水，以及流向與鏈條幾何矛盾的情況，例如「西流注于X」而X在東邊。/ build directed edges; merge same-name rivers book-wide; list dangling nodes and direction conflicts.
6. **望見約束 / Sight-lines**：抽取「{方}望X」，檢查它與鏈條推得的方向是否一致（±45°）。/ extract sight-lines and check them against chain-derived bearings (±45°).
7. **相對重建 / Relative fit**：不錨定時，用任意錨點和座標 (0,0)，只看形狀與不確定度。錨定時：
   ```bash
   python3 -I tools/shj/chain_fit.py --section <篇> --anchor <站> --lat <緯度> --lon <經度> --md <卷宗目錄>/chain-fit-<名>.md
   ```
   錨點應選在要檢驗的站點附近，因為誤差隨鏈長累積。/ anchor near the stations under test, since error accumulates along the chain.
8. **兩錨點校準 / Two-anchor calibration**：如果假說指定了兩個站點，反推里長，檢查是否落在 250–600 m（規格 §6.4）。/ back-calculate the 里 length and check that it falls in 250–600 m.

## 產出 / Output
- 篇段報告：站數和里程核對表、差異解釋、水系邊表、望見一致性、擬合表（若有錨點）。/ Section report with the above tables.
- 每個發現都附條目編號；不寫任何「此山即今某山」。/ Every finding cites entry IDs; never write "this mountain is modern X".
