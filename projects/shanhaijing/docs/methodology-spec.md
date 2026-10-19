# 山海經研究方法規格 / Shanhaijing Research Methodology Spec

> v0.1 · 2026-10-19 · 繼承 [Mythos 研究框架](../../../docs/research-framework.md) 的原則、證據分級、校改預算和結論等級，本文件只寫山海經專用的部分。
> Inherits the principles, evidence grading, correction budget and verdict levels of the [Mythos research framework](../../../docs/research-framework.md); this document covers only what is specific to the Shanhaijing.

---

## 0. 目的 / Purpose

**繁中**：從《山海經》原文出發，不採用任何既有結論，按照可重現的流程，判斷每一條記錄最可能對應現實世界中的什麼（地點、水系、物種、天象、族群），或者判定它無法對應，並給出分級結論。

**EN**: Starting from the Shanhaijing text itself and adopting no prior conclusion, follow a reproducible procedure to decide what each record most likely corresponds to in the real world (place, river system, species, sky phenomenon, people), or to conclude that it corresponds to nothing, and give a graded verdict.

## 1. 語料的結構事實 / Structural facts of the corpus

以下事實都可以直接從資料驗證（`reference/shanhaijing/data/entries.jsonl`，共 869 段）。
All of these can be verified directly from the data (`reference/shanhaijing/data/entries.jsonl`, 869 paragraphs).

| 層 / Layer | 卷 / Books | 記錄格式 / Record format | 主要可用通道 / Main channels |
|---|---|---|---|
| 五藏山經 Mountain Classics | 01–05 | `又{方位}{N}里，曰{山名}` 加上物產、`{水}出焉，而{方位}流注于{水}`、生物描述、望見關係；每段篇末有「凡N山，N里」/ `又{bearing}{N}里，曰{name}` + resources, rivers, creatures, sight-lines; each section ends with its own totals | GEO HYD TER BIO MIN |
| 海外四經 Beyond the Seas | 06–09 | `{國}在{參照}{方位}`，按方位順序環列 / `{polity} is {direction} of {reference}`, listed in directional order | ETH GEO(相對 / relative) BIO |
| 海內四經 Within the Seas | 10–13 | 同上，另有河流的「出／入」路線（第 13 卷末為水道記錄）/ same, plus river courses (end of book 13 is a list of waterways) | HYD ETH GEO(相對) |
| 大荒四經 + 海內經 Great Wilderness | 14–18 | `{方位}海之外，大荒之中，有山…`；日月出入之山；神譜 / sunrise and sunset mountains; genealogies | CLI(日月出入 / sunrise-sunset points) ETH GEO(相對) |

## 2. 流程 / Pipeline (S0–S9)

| 階段 / Stage | 輸入 / Input | 動作 / Action | 輸出 / Output | 工具 / Tool | 關卡 / Gate |
|---|---|---|---|---|---|
| **S0 語料 / Corpus** | 見證本 / witnesses | 擷取，給出編號，保留注疏和異文 / fetch, assign IDs, keep commentary & variants | `entries.jsonl`, `text/*.md` | `fetch_sources.py`, `ingest.py` | 零殘留標記，每段都有編號 / no markup left, every paragraph has an ID |
| **S1 校勘 / Textual criticism** | 三個見證本 / 3 witnesses | 對勘，並把異文分類為：異體 / 訛誤 / 實質 / 錯簡 / collate, classify each variant as orthographic / error / substantive / displacement | `collation.jsonl`, 校勘帳 / collation ledger | `collate.py`, skill `witness-collation` | 被引用的條目，其異文都已分類 / every variant in a cited entry is classified |
| **S2 結構抽取 / Extraction** | 工作文本 / working text | 抽取站點、方位、里程、水系、生物、礦產、望見關係、相對方位 / stations, bearings, distances, rivers, creatures, minerals, sight-lines, relative positions | `stations.jsonl`, `sections.jsonl` | `extract_routes.py`, skill `shj-itinerary-reconstruction` | 抽取的站數與篇末「凡N山」相符；不符的列為待查 / station count matches the stated total, or is logged as a discrepancy |
| **S3 內部一致性 / Internal consistency** | S2 | 檢查分段里程與總數、水系拓撲、同名站點、方位閉合 / leg sums vs totals, river topology, duplicate names, bearing closure | `routes-summary.md`, 錯誤候選 / error candidates | 同上 / same | 每個差異都有初步解釋（抽取錯誤 / 文本錯誤 / 未解）/ every discrepancy has a provisional explanation (extraction error / text error / unresolved) |
| **S4 相對重建 / Relative reconstruction** | S2+S3 | 不錨定地球，只用文本自身的單位「里」重建相對幾何和水系圖 / rebuild relative geometry and river graph in the text's own unit, without anchoring to Earth | 相對圖、水系圖 / relative map, river graph | `chain_fit.py`（不錨定 / unanchored） | 不確定度要有量化 / uncertainty is quantified |
| **S5 特徵指紋 / Fingerprints** | S2 | 為每站和每段建立指紋：地形、水系型態、生物、礦產、氣候、望見關係 / build a fingerprint per station and section | 指紋表 / fingerprint table | skill `biogeo-identification`, `toponym-triangulation` | 每項特徵都標明來源條目 / every feature cites its entry |
| **S6 候選生成 / Candidate generation** | S5 | **盲生成**：只用指紋在全球範圍內檢索候選區，不看前人結論 / **blind**: search worldwide using fingerprints only, without looking at prior conclusions | 候選清單（≥ 3 個，必須含本地框架和虛無假說）/ candidate list (≥ 3, must include a local frame and the null) | skill `toponym-triangulation` | 生成過程有紀錄，可以重現 / generation is logged and reproducible |
| **S7 交叉定位 / Triangulation** | S4+S6 | 對每個候選區，在每個通道內獨立評分：幾何擬合殘差、水系拓撲同構、生物分佈與遷徙、礦產、氣候 / score each candidate independently per channel | 證據表 / evidence table | `chain_fit.py`, 各 skill / skills | 每條證據都有 E 等級和對照集 / every item has an E grade and a comparison set |
| **S8 裁決 / Adjudication** | S7 | 合計對數似然比，扣除校改成本，經過紅隊和敏感度分析後定級 / sum log-LR, subtract emendation costs, red team, sensitivity, grade | `dossier.md` 裁決段 / verdict section | agent `adjudicator`, `devils-advocate` | 通過 [檢查清單](checklist.md) / passes the [checklist](checklist.md) |
| **S9 發佈 / Publication** | S8 | 寫成 finding，更新地名帳和物種帳，設定重測觸發條件 / write a finding, update the toponym and taxon ledgers, set re-test triggers | `findings/F-*.md` | — | 寫明撤回條件 / retraction conditions stated |

## 3. 注疏與前人學說 / Commentary and prior scholarship

| 來源 / Source | 處理方式 / Treatment |
|---|---|
| 郭璞注（晉）、其他夾注 / Guo Pu and other interlinear notes | 保存在 `notes[]`。只把它看作「四世紀讀者的理解」，可以用來提出 `H-ext` 假說，或者幫助釋讀字義，但不計分 / Kept in `notes[]`. Treated as "how a 4th-century reader understood it": may seed an `H-ext` hypothesis or help with word meaning, but never scores |
| 現代校注（如袁珂）的移段、補字 / Modern editorial relocations and insertions (e.g. Yuan Ke) | 保存在 `editorial_refs[]`。工作文本**按最早見證本的原始順序**，移段只作為 S1 的錯簡假說 / Kept in `editorial_refs[]`. The working text follows **the earliest witness's order**; relocations are treated only as displacement hypotheses in S1 |
| 前人的地理比定（任何方向）/ Prior geographic identifications (any direction) | 登記為 `H-ext-*`，和其他假說走同一流程。在 S6 候選生成時**不得查看**，以免錨定效應 / Registered as `H-ext-*` and tested like any other. **Not consulted** during S6, to avoid anchoring |

## 4. 領域慣例 / Domain conventions

以下慣例都是**待校準的參數**，不是定論。每份卷宗都要寫明自己採用哪一種，並在敏感度分析中測試其他選項。
These conventions are **parameters to calibrate**, not settled facts. Each dossier states which option it uses and tests the alternatives in its sensitivity analysis.

| 項目 / Item | 文本現象 / Textual phenomenon | 選項 / Options |
|---|---|---|
| 方位 Bearing | 「東、西南…」八方位 / eight directions | 真北或磁北；誤差 ±22.5°（八方位的解析度）/ true or magnetic; ±22.5° (eight-point resolution) |
| 前／後 Front / back | 「赤水之後，黑水之前」 | (a) 面南：前 = 南，後 = 北；(b) 行進方向：前 = 去程方向；(c) 上下游 / (a) facing south: front = S, back = N; (b) direction of travel; (c) downstream vs upstream |
| 陰／陽 | 「其陽多玉，其陰多…」 | 山南坡、山北坡（以及水北、水南）/ south and north slopes (and north and south banks) |
| 出／注／潛／入 | 「X水出焉，而西流注于Y」「河水所潛」 | 出 = 發源；注 = 匯入；潛 = 伏流或沒入內流區 / rises; flows into; sinks underground or into an endorheic basin |
| 水 vs 海 vs 澤 | 「赤水」「西海」「稷澤」 | 語料內部詞彙：水 = 河流，海 = 大型鹹水體，澤 = 湖沼。比定時不得跨類，跨類算 T5 校改 / internal lexicon: 水 = river, 海 = large saline body, 澤 = lake or marsh; crossing categories counts as a T5 emendation |
| 里 Li | 里程 / distances | 不預設長度；作為參數（預設在 300–500 m 間均勻分佈），或用兩個以上的錨點從文本內部校準 / not fixed; a parameter (default uniform 300–500 m) or calibrated internally from ≥ 2 anchors |
| 水行／流沙 | 「水行五百里，流沙三百里」 | 不同的行進方式，誤差模型要分開；流沙是通名，在全書出現 21 段 / different travel modes with separate error models; 流沙 is a generic term occurring in 21 paragraphs |
| 望 Sight-line | 「南望昆侖」「東望泑澤」 | 方向約束；距離上限取決於地形能見度 / directional constraint; maximum distance set by terrain visibility |
| 日月所出／入 | 大荒經的山 / Wilderness-classic mountains | 可能是地平線曆法（日出方位隨季節變化），可以用來推算緯度 / possibly horizon calendars (sunrise azimuth varies with season); can constrain latitude |

## 5. 生物條目的處理 / Treatment of creature entries

1. **分解**：把描述拆成特徵向量，包括體型參照（「狀如X」）、部件（「魚身而鳥翼」）、顏色、聲音（「其音如…」）、習性（「以夜飛」「常從西海遊于東海」）、功用和預兆。功用和預兆不作為生物證據。/ **Decompose** each description into a feature vector: body analogy ("狀如X"), parts, colours, sound, behaviour, uses and omens. Uses and omens never count as biological evidence.
2. **候選分類群**：列出至少三個候選分類群，逐項標記吻合（✓）、不吻合（✗）、未知（?）。/ **Candidate taxa**: list at least three and mark each feature as fit, misfit or unknown.
3. **棲地一致性**：描述的棲地（站點的河流、山、海）必須和候選分類群的生態相容，例如海洋魚類不可能生活在注入沙漠的溪流裡。不相容時，要考慮「傳聞插入」的錯誤模型。/ **Habitat consistency**: the habitat in the text (river, mountain, sea at the station) must be ecologically compatible with the candidate taxon; a marine fish cannot live in a stream that runs into desert sand. If incompatible, consider a hearsay-insertion error model.
4. **分佈與遷徙**：用分類群的地理分佈（包括全新世的古分佈）和遷徙路線，對候選區域打分。/ **Range & migration**: score candidate regions against the taxon's range (including Holocene palaeo-ranges) and migration routes.
5. **基準率**：在全書中統計同類描述的頻率，例如「人面X身」在全書至少出現 22 次。頻率越高，獨特性越低。/ **Base rate**: count how often the same kind of description occurs in the corpus; the more frequent, the less distinctive.

## 6. 錯誤模型 / Error model

### 6.1 文本錯誤（山海經專用補充）/ Textual errors (Shanhaijing additions)

| 代號 / Code | 類型 / Type | 偵測方式 / Detection | 對應框架成本 / Framework cost |
|---|---|---|---|
| X1 | 數字訛誤 / numeral corruption | S3 里程與總數差異，例如 937 對 6670 / leg-sum vs total, e.g. 937 vs 6670 | T2 |
| X2 | 形近字 / graphic confusion | 見證本異文，例如「白甘棗之山」應作「自」/ witness variants, e.g. 白 for 自 | T0/T1 |
| X3 | 段落錯簡 / displaced paragraph | 見證本順序差異（海內三經），相對方位矛盾 / differing witness order; contradictory relative positions | T3 |
| X4 | 站點脫漏或誤併 / station dropped or merged | 站數與「凡N山」不符 / station count ≠ stated count | T2 |
| X5 | 圖轉文 / picture-to-text | 描述像是在讀一幅圖，例如「東向立」「兩手各操一魚」；方位描述和圖像方向一致 / reads like a picture description; orientations match a drawing | 作為獨立的「圖本假說」登記，不作為校改 / registered as a separate "map-source hypothesis", not an emendation |
| X6 | 傳聞插入 / hearsay insertion | 習性描述與站點棲地矛盾 / behaviour contradicts the station's habitat | T5（除非有結構證據 / unless there is structural evidence） |

### 6.2 觀測與記錄錯誤 / Observation & recording error

觀測與記錄錯誤不靠校改處理，而是放進統計模型。/ Not emended; modelled statistically.

### 6.3 鏈條擬合的數值誤差模型 / Numeric error model for chain fitting

| 參數 / Parameter | 預設 / Default | 理由 / Rationale |
|---|---|---|
| 方位 / bearing | 均勻 ±22.5° / uniform ±22.5° | 八方位的解析度 / 8-point compass resolution |
| 距離 / distance | 對數常態，σ = 0.30 / log-normal σ = 0.30 | 步測或估算的誤差，乘法性質 / multiplicative pacing or estimation error |
| 里長 / li length | 每次模擬從均勻 [300, 500] m 中抽一個 / uniform [300, 500] m per run | 不預設單位 / unit not assumed |
| 誤差累積 / error accumulation | 隨機漫步 / random walk | 鏈越長，不確定越大。所以錨點要選在要檢驗的站點附近 / longer chains, more uncertainty; anchor near the stations under test |

### 6.4 尺度校準 / Scale calibration

如果某假說錨定了同一段中的兩個以上站點，可以反推出里長。反推的里長必須落在物理合理的範圍（約 250–600 m），否則記為 E−2。
If a hypothesis anchors two or more stations in the same section, the implied 里 length can be back-calculated. It must fall in a physically plausible range (about 250–600 m), otherwise score E−2.

## 7. 交叉定位方法 / Triangulation methods

| 方法 / Method | 做法 / Procedure | 通道 / Channel |
|---|---|---|
| 7.1 鏈條擬合 Chain fit | 用一個錨點投影整段，檢查其餘站點的預測位置與現實地形是否相符；用兩個錨點時，同時檢查反推的里長 / project the whole section from one anchor and check the other stations against real terrain; with two anchors, also check the implied 里 | GEO |
| 7.2 水系同構 Hydrological isomorphism | 把文本的「出／注」關係圖與候選區的實際水系做圖同構比較：流向、匯入點、內流、伏流 / compare the text's river graph with the candidate's real drainage | HYD |
| 7.3 生物分佈與遷徙 Biogeography & migration | 候選分類群的分佈與遷徙路線要覆蓋所述站點和路線，例如「常從西海遊于東海」要求東西兩海之間有可通行的路線 / the taxon's range and migration must cover the stations and routes described; "swims from the West Sea to the East Sea" requires a passable route between the two | BIO |
| 7.4 礦產 Minerals | 站點礦產組合與候選區礦床的對比 / match mineral assemblages | MIN |
| 7.5 天象氣候 Sky & climate | 日出入方位推算緯度；「多怪雨」「寒暑之水」等氣候描述 / sunrise azimuths constrain latitude; climate cues | CLI |
| 7.6 相對方位網路 Relational network | 把海經、大荒經的「A 在 B 東」轉為約束滿足問題，求可行的佈局，再與候選世界圖比對 / turn "A is east of B" statements into a constraint-satisfaction problem, solve for feasible layouts, compare with candidate world maps | GEO ETH |
| 7.7 跨語料 Cross-corpus | 其他獨立文本的同名或同構記錄（獨立性要先論證）/ same-name or same-structure records in independent texts (independence must be argued first) | XCP |
| 7.8 古環境 Palaeo-environment | 假說涉及的年代必須明確。若要求的環境（例如撒哈拉有河）只在更早的年代存在，假說就必須另外論證文本有那麼古老 / the hypothesis must state its date; if the environment it needs (e.g. rivers in the Sahara) existed only earlier, it must separately argue that the text is that old | TER CLI |

## 8. 候選生成規則 / Candidate-generation rules

1. 先用 S5 的指紋生成候選，再登記假說；不能先選定地點，再找指紋。/ Generate candidates from S5 fingerprints *before* registering a hypothesis, never the other way round.
2. 候選清單必須包含：(a) 本地框架，即該段落鄰近卷篇所暗示的區域；(b) 至少一個遠距框架；(c) 虛無假說，即「此處是想像、拼合，或圖像衍生的地點」。/ The list must include (a) a local frame (the area implied by neighbouring sections), (b) at least one distant frame, (c) the null (an imagined, composite or picture-derived place).
3. 使用者提出的假說（例如 H-0001）照常登記和檢驗，但對立候選仍然要按第 1 條盲生成。/ User-proposed hypotheses (e.g. H-0001) are registered and tested normally, but their rivals are still generated blind under rule 1.

## 9. 裁決規則補充 / Adjudication addenda

- 預設校改預算為 log₁₀ −1.5（見框架 §5）。/ Default correction budget: log₁₀ −1.5 (framework §5).
- **同名多地**：如果假說主張書中同名的地點（例如三種「昆侖」寫法）指不同的地方，必須先在語料內部提出證據，例如描述互相矛盾。否則預設同名同地，並對所有同名條目負責（P4）。/ **Same name, different places**: a hypothesis claiming that same-named places (e.g. the three spellings of 昆侖) are distinct must first show internal evidence such as contradictory descriptions; otherwise same name means same place, and it answers for every same-named entry (P4).
- **範圍宣告**：卷宗必須宣告適用的條目範圍。範圍越窄，結論等級上限越低：只涵蓋單段的，上限為 L1。/ **Scope declaration**: the dossier states which entries it covers; a narrower scope caps the verdict lower (single paragraph caps at L1).

## 10. 示範 / Worked example

見 [H-0001 卷宗](../hypotheses/H-0001/dossier.md)：「崑崙在埃及、赤水為紅海、黑水為尼羅河、流沙為撒哈拉、文鰩魚為跨洋飛魚」，按 S0–S9 全流程檢驗。
See the [H-0001 dossier](../hypotheses/H-0001/dossier.md) ("Kunlun in Egypt, Red Water = Red Sea, Black Water = Nile, Flowing Sands = Sahara, 文鰩魚 = trans-oceanic flying fish"), tested end to end under S0–S9.
