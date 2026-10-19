# 紅隊審查紀錄 / Red-team review log

> 每一版交付之前的審查（task T-R）。依 [framework §7](../../../docs/research-framework.md) 與 agent `devils-advocate` 的檢查項。
> Reviews before each deliverable (tasks T-R), per framework §7 and the `devils-advocate` checks.

---

## R1：初稿 v1 / Review of draft v1（2026-10-19）

**結論 / Verdict**：初稿 v1 的兩個主要結論（「河 = 黃河」「五藏山經的骨架在黃河、渭河流域」）**撤回**。它們依賴真實世界庫的偏差：只有中國的河流列出了支流。修正後，所有河流的對應都降為「暫定」。v1 由 v2 取代。
The two headline results of draft v1 (河 = Yellow River; the Mountain Classics' skeleton in the Yellow and Wei basins) are **withdrawn**: they depended on a base bias, since only Chinese rivers had tributaries listed. After the fix every river mapping is tentative. Draft v2 supersedes v1.

### 1. 庫的偏差 / Base bias

| 檢查 / Check | 發現 / Finding | 處理 / Action |
|---|---|---|
| 各河列出的支流數 / tributaries listed per river | 長江 6、黃河 5、渭河 2、洛河 1；亞馬遜、剛果、尼日、多瑙、伏爾加、勒拿等 25 條 2,000 km 以上的大河為 0。書中支流多的河只能在中國得到「河口吻合」/ only China's rivers had tributaries | 統一規則補 125 條支流（T-C03，提交於重算之前）/ one rule worldwide, 125 added, committed before re-scoring |
| 重算的結果 / after re-scoring | 河的對應在黃河、恆河、科羅拉多等之間變動，可信度 ≤ 0.03；把 v1 的中國一致組態放進新庫打磨，總分 827.5，低於最佳鏈 846 / 河 flips between rivers at ≤ 0.03; the v1 China-coherent configuration scores 827.5 vs 846 | 河流全部降為「暫定」/ all rivers tentative |
| 地區性質的知名度 / known region properties | 中國 31 項已知、5 項未知，資料最詳；喜馬拉雅只有 9 項已知 / China is the best described region | 誘餌：每區最多保留 21 項已知 / decoy: cap at 21 known per region |
| 誘餌結果 / decoy result | 可信度 ≥ 0.1 的山：中國 57 → 38、北美 23 → 7、塔里木 11 → 17；中與高級別的對應 25/35 不變 / CHN 57 → 38 | 中國仍居首，但部分領先來自資料密度 / China still leads, partly by description density |
| 動物分佈 / animal ranges | 中國 43 種，其他地區中位數約 20 / 43 animals in China vs a median of about 20 | 列入 T-C04：補其他地區的候選動物 / balance animals (T-C04) |
| 國族 / peoples | 毛民 → 阿伊努的高可信度主要來自單一稀有特徵「身生毛」，庫中只有阿伊努帶此標籤 / 毛民 → Ainu rests on one rare tag that only the Ainu carry | 標註為單一特徵的對應 / flagged as single-feature |

### 2. 抽取錯誤 / Extraction errors

| 發現 / Finding | 例 / Example | 處理 / Action |
|---|---|---|
| 同段重複的關係（25 條）/ 25 duplicate relations from one paragraph | 毛民 的兩條「位於 → 玄股」都來自 `SHJ-09-1-014` | 已修：每段每種關係只計一次 / fixed |
| 神被當作生物（7 個）/ 7 deities typed as creatures | 「有神，人面…曰不廷胡余」被對到儒艮；禺彊、九鳳、彊良、弇茲、延維、奢比尸 | 已修：改為神人 / fixed (now PER) |
| 空間句式沒有抽出 / spatial clauses not extracted | `SHJ-16-1-037`（崑崙之丘）的「西海之南」「流沙之濱」「赤水之後，黒水之前」「弱水之淵環之」「其外有炎火之山」全無關係 | 待辦 T-E06 / pending |
| 名稱與水道遺漏 / names and courses missed | 「外有炎火之山」被當作山名；「黑水出焉，而西流于大杅」（無「注」字）沒有抽出 | 待辦 T-E06 / pending |
| 不起作用的因子 / a factor that never fires | 「小溪」因子：凡有出入記錄的水都已算主要水體，所以從未產生 / the minor-stream factor never fires | 記錄；權重敏感度中「minor」兩個變體與基準完全相同 / recorded |

### 3. 敏感度 / Sensitivity（[kg/sensitivity/sensitivity.md](../data/derived/kg/sensitivity/sensitivity.md)）

- 不改權重的重跑與基準 100% 相同（確定性）。/ The repeat run is 100% identical (deterministic).
- 高與中級別在各權重變體下不變的最低比例：63%。/ High+medium mappings unchanged: at least 63% in every variant.
- 河流水系不變的比例只有 3–15%；河、渭、涇、汾、漢、赤水、黑水、弱水、崑崙之丘在 16 個權重變體中只有 2–4 個不變。/ River systems unchanged in only 3–15%; the key rivers and 崑崙之丘 keep their mapping in 2–4 of 16 weight variants.
- 穩健：毛民 → 阿伊努 16/16、玄股 → 北極民族 15/16、黑齒 → 南島語族 14/16。文鰩魚 在 12 個變體中改為飛魚。/ Robust: 毛民, 玄股, 黑齒; 文鰩魚 flips to flying fish in 12 variants.
- 江 → 奧里諾科（0.50，中）只在 8/16 個變體不變：單看可信度會高估。交付中每個對應都附「權重變體 k/n」。/ 江 → Orinoco (0.50) holds in only 8/16: confidence alone overstates; the deliverable now shows robustness per mapping.

### 4. 多峰 / Multimodality
各鏈總分 819.5–846.1（約 3%）。區塊調整之後仍然多峰：只靠「注入」拓撲，許多真實水系都能同樣吻合。/ Chain energies 819.5–846.1; with topology alone many real river systems fit about equally well.

### 5. 使用者提出的崑崙解讀 / The user's Kunlun reading（`SHJ-16-1-037`）
西海＝地中海、流沙＝撒哈拉、赤水＝紅海、黑水＝尼羅河、人面虎身之神＝獅身人面像、崑崙＝開羅一帶。審查意見：
- 地圖（狀態）讀法下，「赤水出焉，東南流注于氾天之水」（`SHJ-02-3-008`）與紅海的走向相合。/ Under a map reading, 赤水 fits the Red Sea's orientation.
- 同段「黑水出焉，而西流于大杅」：從開羅看，尼羅河不向西延伸；在這個讀法下，「河水出焉，南流東注」反而較像尼羅河。/ 黑水 extending west does not fit the Nile; 河 fits it better.
- 「赤水之後，黒水之前」取決於「前」的方位慣例，兩種慣例都要對每個候選地計分。/ Both 前/後 conventions must be scored for every candidate.
- 「投物輒然」在全書只出現一次，是最有區別力的線索：火山、熔岩湖、天然氣或石油之火在外觀與行為上都相合；沙丘只在外觀上相合。/ 投物輒然 is the most discriminating clue.
- 人面虎身 在全書 2 段、人面 70 段：作為單獨證據權重有限；獅被描述為虎是可接受的觀察者替代。/ moderate weight; lion-for-tiger accepted as an observer substitution.
- 這些都需要 T-E06 的空間關係與新的計分規則（地圖讀法、方位慣例雙測、古蹟需引證並扣分、外觀與行為分開、觀察者替代）才能在全書層級檢驗；**是否採用這些規則，等待項目發起人決定**。/ Testing at the whole-book level needs T-E06 and new rules, **pending the initiator's decision**.

### 6. 交付的改變 / Changes to the deliverable
v2：撤回 v1 的兩個主要結論；每個對應附權重穩健度；地圖加上海岸線，暫定項目以虛線顯示。/ v2 withdraws v1's headline results, shows weight robustness per mapping, and draws coastlines with tentative items dashed.

---

## R2：解讀規則與初稿 v3 / Review of the reading rules and draft v3（2026-10-20）

**結論 / Verdict**：使用者的「西次一、二、三經 = 哈拉帕、蘇美、埃及」在目前的證據下**不被支持**（完整重解 −40.8，低於衣索比亞對立組態與北美誘餌）；崑崙之丘一段本身與埃及相容。v3 可以交付，附下列待辦。
The user's Harappa–Sumer–Egypt reading is **not supported** (−40.8 in a full re-solve, below the Ethiopia rival and a North America decoy); the Kunlun paragraph itself is compatible with Egypt. v3 may ship with the items below.

| # | 檢查 / Check | 發現 / Finding | 處理 / Action |
|---|---|---|---|
| 1 | 對稱 / symmetry | 新規則與新候選都在全世界加入：古河道與乾河谷分佈於非洲、阿拉伯、黎凡特、美索不達米亞、印度、塔里木、澳洲；古運河含中國的鴻溝；地區分割依「河谷文明」規則 / rules and candidates added worldwide | 通過 / pass |
| 2 | 起點偏差 / start bias | 局部擬合與從頭重解的排序一致（中國 > 北美誘餌 > 衣索比亞 > 使用者）/ local re-fits and full re-solves agree | 通過 / pass |
| 3 | 方位慣例 / orientation | 前 = 南時，使用者組態 −51.2，與前 = 東（−51.5）幾乎相同：結論不取決於慣例 / the verdict does not depend on the convention | 通過 / pass |
| 4 | 同名誤併 / merged homonyms | 崑崙之丘的「弱水」與西次四經勞山的「弱水」被併為一個實體；同樣情況可能還有 / two different 弱水 merged | T-E05 |
| 5 | 規則副作用 / side effect of R1 | 「河」被對到大西洋（0.30，10/16）：許多水注入「河」，最容易被承接眾河的大洋吻合。R1 需要約束：書中有「出焉」（有一端在山）的水，不宜對到大洋 / an ocean absorbs a hub | T-X09 |
| 6 | 解析度 / resolution | 「黑水之前」（尼羅河東岸）與「流沙之濱」需要比地區更細的地點 / finer places needed | T-C10 |
| 7 | 收斂 / convergence | 固定中國的完整重解（912.6）高於自由解（897.4）：求解器未找到全域最佳 / the free solve misses a better configuration | T-X03 |
| 8 | 庫的殘餘偏差 / residual base bias | 500 km 以下的河，中國 7 條，其他地區最多 3 條；河源總數北美 26、歐洲 22、中國 21、埃及 5（含乾河谷與運河）/ short rivers still China-heavy | 記錄；T-C03b |
| 9 | 權重敏感度 / weights | 高與中級別的對應在各權重變體中至少 73% 不變 / ≥ 73% of high+medium mappings unchanged | 通過 / pass |
