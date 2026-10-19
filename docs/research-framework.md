# Mythos 研究框架 / Research Framework

> v0.1 · 2026-10-19 · 適用於所有語料的公共方法層。各子項目在此之上撰寫專用規格（例如 [山海經方法規格](../projects/shanhaijing/docs/methodology-spec.md)）。
> The common, corpus-agnostic method layer. Each sub-project writes a specialised spec on top of it (e.g. the [Shanhaijing methodology spec](../projects/shanhaijing/docs/methodology-spec.md)).

---

## 1. 基本立場 / Stance

**繁中**：我們不預設古籍「是真的」，也不預設它「是假的」。對任何一條記錄，我們只問：在所有可想到的解釋中，這條文本作為證據，最支持哪一種？支持到什麼程度？候選解釋包括真實觀測、轉述變形、象徵、想像，以及後人竄入。

**EN**: We assume neither that an ancient text "is true" nor that it "is false". For any record we ask only: of all the explanations we can think of, which one does this text best support as evidence, and how strongly? The candidates include real observation, deformed retelling, symbolism, imagination and later interpolation.

## 2. 十條原則 / Ten principles

| # | 原則 | Principle |
|---|---|---|
| P1 | **原文優先**：證據的最小單位是「條目編號＋原文引文＋見證本」 | **Text first**: the atomic unit of evidence is *entry ID + verbatim quote + witness* |
| P2 | **不繼承結論**：注疏和前人學說只登記為假說（`H-ext-*`），永遠不作為證據 | **No inherited conclusions**: commentary and prior scholarship are registered as hypotheses (`H-ext-*`), never used as evidence |
| P3 | **預先登記**：檢驗之前先寫下假說、預測、證偽條件和校改預算 | **Pre-registration**: write down the hypothesis, predictions, falsifiers and correction budget before testing |
| P4 | **全語料問責**：假說必須交代所有相關條目，不能只挑支持的 | **Whole-corpus accountability**: a hypothesis must account for every relevant entry, not just the convenient ones |
| P5 | **通道獨立**：同一個觀察只能在一個通道計分 | **Channel independence**: one observation scores in one channel only |
| P6 | **基準率與獨特性**：相似度要乘上「這種相似有多常見」的校正 | **Base rate & distinctiveness**: a resemblance is discounted by how common such resemblances are |
| P7 | **錯誤要建模，校改要付代價** | **Errors are modelled; emendations cost** |
| P8 | **對立假說**：至少要有兩個實質對立假說，再加一個虛無假說，用相同的標準檢驗 | **Competing hypotheses**: at least two substantive rivals plus a null, tested by the same standard |
| P9 | **尺度不預設**：單位、方向慣例、年代都作為參數，由資料校準 | **No assumed scale**: units, direction conventions and dates are parameters calibrated from data |
| P10 | **可重現、可撤回**：所有結論都附帶重現路徑和撤回條件 | **Reproducible & retractable**: every conclusion ships with its reproduction path and retraction conditions |

## 3. 證據通道 / Evidence channels

證據按「獨立的觀測來源」分成以下通道。子項目可以增加通道，但不能合併通道。
Evidence is partitioned by independent observational source. Sub-projects may add channels but must not merge them.

| 代號 | 通道 | Channel | 典型內容 / Typical content |
|---|---|---|---|
| GEO | 幾何 | Geometry | 方位、距離、鏈條形狀、相對位置 / bearings, distances, chain shape, relative positions |
| HYD | 水系 | Hydrology | 河流的源頭、流向、匯入點、伏流、內流湖 / sources, flow directions, confluences, sinking rivers, endorheic lakes |
| TER | 地形 | Terrain | 山的高度、形態、沙漠、沼澤、火山或氣火 / relief, landforms, deserts, marshes, volcanic or gas fires |
| BIO | 生物 | Biota | 動植物的形態、習性、分佈、遷徙 / morphology, behaviour, range, migration |
| MIN | 礦產 | Minerals | 金、銀、銅、玉、丹砂、雄黃、磁石 / gold, silver, copper, jade, cinnabar, realgar, magnetite |
| CLI | 氣候天象 | Climate & sky | 寒暑、風雨、日月出入、星象 / seasons, winds, sunrise and sunset points, stars |
| ETH | 族群文化 | Peoples & culture | 國名、習俗、食物、器物 / polities, customs, diet, artefacts |
| XCP | 跨語料 | Cross-corpus | 其他獨立文本中的同名或同構記錄 / same-name or same-structure records in other independent texts |
| ARC | 考古與物質 | Archaeology & material | 遺址、遺物、碑刻、紀念建築 / sites, finds, inscriptions, monuments |

## 4. 證據分級與似然比 / Evidence grading & likelihood ratios

每條證據都給出 **E 等級**和一個粗略的**似然比區間**（LR = P(觀察 | H) / P(觀察 | 非 H)）。
Each evidence item gets an **E grade** and a coarse **likelihood-ratio bin** (LR = P(obs | H) / P(obs | not-H)).

| 等級 | 名稱 | Name | LR 區間 | 判準 / Criterion |
|---|---|---|---|---|
| E−3 | 決定性矛盾 | Decisive contradiction | ≤ 0.05 | 與假說直接衝突，且無合理錯誤模型 / direct conflict with no plausible error model |
| E−2 | 強矛盾 | Strong contradiction | 0.05–0.2 | 衝突；只有付出高昂校改才能化解 / conflict that only costly emendation resolves |
| E−1 | 弱矛盾 | Weak contradiction | 0.2–0.8 | 不太吻合 / poor fit |
| E0 | 中性 | Neutral | 0.8–1.25 | 不能區分假說 / non-discriminating |
| E1 | 泛化吻合 | Generic match | 1.25–2 | 吻合，但這種特徵在世界上很常見 / fits, but the feature is common worldwide |
| E2 | 具體吻合 | Specific match | 2–5 | 吻合一個少見的特徵 / fits an uncommon feature |
| E3 | 獨特吻合 | Distinctive match | 5–20 | 吻合一個罕見特徵，或多個特徵的組合 / fits a rare feature or a feature combination |
| E4 | 唯一吻合 | Unique match | > 20 | 只有該地點才能同時滿足 / only this locus satisfies all of it |

**規則 / Rules**

1. 指定 E 等級時，必須寫出**對照集**，也就是「若非 H，還有哪些地方或解釋也會產生這個觀察」。/ Assigning an E grade requires naming the **comparison set**: what else would also produce this observation if H were false.
2. 同一通道內，多條證據如果彼此相關，只取最強的一條，其餘按 50% 折減。/ Within one channel, correlated items count once at full strength; the rest are discounted by 50%.
3. 外部事實（例如「某物種分佈於某地」）必須附來源；沒有來源的，標為 `needs-citation`，LR 一律記為 1。/ External facts (e.g. "species X occurs at Y") must cite a source; uncited ones are tagged `needs-citation` and get LR = 1.
4. 「前人也這麼說」的 LR 永遠是 1。/ "A prior author said so" always has LR = 1.

## 5. 錯誤模型與校改預算 / Error model & correction budget

| 類型 | Type | 例 / Example | 校改成本 / Cost (log₁₀ LR) |
|---|---|---|---|
| T0 | 見證本已有異文支持 / Supported by an extant witness variant | 甲本作「三」，乙本作「五」 | −0.1 |
| T1 | 形近字（有字形學依據）/ Graphic confusion with palaeographic support | 自↔白、己↔已 | −0.3 |
| T2 | 數字訛誤（位數、倒文）/ Numeral corruption (digit slip, inversion) | 三百↔三千 | −0.4 |
| T3 | 錯簡或段落移位（有結構證據）/ Displaced slip with structural evidence | 段落整體移位 | −0.5 |
| T4 | 方位慣例重解 / Reinterpreting a direction convention | 前／後的指向 | −0.5（全卷宗只能選一次 / chosen once per dossier） |
| T5 | 無文本證據的推測校改 / Conjectural emendation without textual evidence | 「此處當作某」 | −1.0 |

- 每份卷宗都要預先宣告**校改預算**（預設為 −1.5，即最多約一次 T5 或三次 T1）。/ Each dossier pre-declares a **correction budget** (default −1.5, i.e. about one T5 or three T1).
- 超出預算的假說，結論等級上限為 L1。/ A hypothesis that exceeds its budget is capped at L1.
- 校改成本直接加進總對數似然比。/ Emendation costs are added straight into the total log-LR.

## 6. 結論等級 / Verdict levels

| 等級 | 名稱 | Name | 判準 / Criterion |
|---|---|---|---|
| R | 否定 | Refuted | 有一個或多個 E−3，或者總 log₁₀LR < −2 |
| L0 | 推測 | Speculative | 總 log₁₀LR 在 −2 到 0 之間，或者證據只落在一個通道 / total in [−2, 0], or single-channel |
| L1 | 可能 | Plausible | 總值 > 0，至少兩個通道為正 / total > 0 with ≥ 2 positive channels |
| L2 | 有據 | Supported | 總值 > 1，至少三個獨立通道為正，無 E−2 以下的證據，且未超出校改預算 / total > 1, ≥ 3 independent positive channels, nothing ≤ E−2, within budget |
| L3 | 強支持 | Strongly supported | 總值 > 2，同時通過紅隊審查與敏感度分析 / total > 2, passes red team and sensitivity analysis |
| L4 | 確立 | Established | L3 加上一項事先登記、隨後獲得證實的新預測 / L3 plus a pre-registered novel prediction later confirmed |

> 註：數字門檻是半定量的約定，目的是讓推理**透明可爭論**，不是假裝精確。
> Note: the thresholds are semi-quantitative conventions, meant to make reasoning **transparent and arguable**, not to fake precision.

## 7. 假說生命週期 / Hypothesis lifecycle

```
proposed ─▶ registered ─▶ testing ─▶ red-team ─▶ adjudicated (R/L0–L4) ─▶ published
   │            │            │                            │
   │            └─ 預測、證偽條件、預算 / predictions, falsifiers, budget
   └─ H-ext-* 外部學說也從這裡進入 / external theories enter here too
                                                          └─▶ re-test triggers（新見證本、新資料 / new witness, new data）
```

## 8. 紅隊協議 / Red-team protocol

紅隊必須完成以下五項，並記錄在卷宗中。/ The red team must complete all five and record them in the dossier.

1. **反例搜尋 / Counter-example search**：在全語料中找出與假說衝突的條目。/ find every corpus entry that conflicts with the hypothesis.
2. **替身測試 / Decoy test**：把錨點換到對立候選地，看看證據是否同樣「吻合」。/ move the anchor to a rival locus and check whether the evidence "fits" just as well.
3. **基準率審查 / Base-rate audit**：每條 E2 以上的證據，都要重新檢查對照集。/ re-examine the comparison set of every item graded E2 or above.
4. **校改審查 / Emendation audit**：逐條覆核每次校改的類型和成本。/ re-check the type and cost of every emendation.
5. **敏感度分析 / Sensitivity**：把最強的一條證據移除，結論等級會怎樣變化？/ remove the single strongest item and see how the verdict changes.

## 9. 公共層與子項目的分工 / Common vs. sub-project responsibilities

| 公共層 / Common layer | 子項目 / Sub-project |
|---|---|
| 原則、通道、分級、預算、等級、生命週期、紅隊 / principles, channels, grading, budget, verdicts, lifecycle, red team | 語料匯入、條目編號、文本結構抽取、專用錯誤類型、領域慣例（例如「里」、方位詞）/ corpus ingest, entry IDs, structural extraction, corpus-specific error types, domain conventions (e.g. 里, direction words) |
| 公共 agent 與 skill（見 [architecture.md](architecture.md)）/ common agents & skills | 專用 agent 與 skill / specialised agents & skills |

## 10. 前提框架與描述優先比對 / Premise frames and description-first matching

**繁中**：子項目可以採用由項目發起人設定的**前提框架**（例如「全書以整個地球為範圍」），在該前提下進行比對。前提框架必須寫在卷宗開頭，結論要註明「在前提 X 下」。描述優先比對（山海經的「方法 G」，見 [method-g-global.md](../projects/shanhaijing/docs/method-g-global.md)）的通用規則：

1. 先從真實世界的動物與地理性質建立特徵庫，再到文本中找吻合與矛盾。
2. 名稱一律遮蔽，只比描述。
3. 特徵依罕見度加權：w = log₁₀(N_known / N_true) ＋ 0.05。
4. 吻合加分、矛盾扣分、未知不計；所有候選用同一規則排名。
5. 距離、方位只作參考（小權重），不能單獨否定候選。
6. 候選特徵值在跑分前寫入並附來源。

**EN**: A sub-project may adopt a **premise frame** set by the project initiator (e.g. "the book covers the whole Earth") and match under it. The premise is stated at the top of the dossier and conclusions are labelled "under premise X". General rules for description-first matching (the Shanhaijing "Method G"): build the feature base from real animals and geography first, then search the text for matches and contradictions; mask all names; weight features by rarity; add for matches, subtract for contradictions, ignore unknowns, and rank all candidates under the same rules; treat distances and bearings as a small-weight reference only; write candidate values, with sources, before scoring.
