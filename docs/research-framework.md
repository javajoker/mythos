# Mythos 研究框架：實體圖譜交叉驗證 / Research Framework: Entity-Graph Cross-Validation

> v2.1 ・ 2026-10-19 ・ 適用於所有語料的公共方法。山海經的實作見 [methodology-spec.md](../projects/shanhaijing/docs/methodology-spec.md)。
> The common, corpus-agnostic method. The Shanhaijing implementation is in [methodology-spec.md](../projects/shanhaijing/docs/methodology-spec.md).

---

## 1. 立場 / Stance

**繁中**：古籍中的每一個名稱只是**符號**。我們不比對今天的名稱，只比對書中對它的**描述、性質，以及它與其他實體的關係**。候選來自**全球**的真實世界實體；一個書中實體可以有多個候選。最後由實體之間的關係**交叉驗證**，選出整體最一致、可信度最高的對應。

**EN**: Every name in an ancient text is only a **symbol**. We never match modern names; we match what the text **says about** an entity — its description, its properties and its **relationships** to other entities. Candidates come from real-world entities **worldwide**, several per text entity if needed. The relationships then **cross-validate** the candidates, and the most consistent, highest-confidence mapping is selected.

## 2. 五個步驟 / Five steps

| # | 步驟 / Step | 產出 / Output |
|---|---|---|
| 1 | **實體**：找出書中所有實體，合併同名與異寫，整合成一張清單 / **Entities**: find every entity, merge names and variant spellings | 知識圖譜的節點 / KG nodes |
| 2 | **描述、性質、關係**：每個實體的原文描述、從描述得到的性質，以及實體之間的關係 / **Descriptions, properties, relations** for every entity | 節點屬性與邊 / node attributes and edges |
| 3 | **真實世界候選**：在全球真實實體中，按描述與性質為每個實體找出一個或多個候選 / **Real-world candidates** worldwide, one or more per entity | 候選表與各自的自身分數 / candidate lists with own scores |
| 4 | **交叉驗證**：用書中的關係檢查候選之間的一致性，求整體最一致的對應，並計算可信度 / **Cross-validation**: test candidates against the text's relationships, solve for the most consistent joint mapping, compute confidence | 對應結果與可信度 / mapping with confidence |
| 5 | **交付**：逐條對應原書，不遺漏任何一段、任何一個實體 / **Deliverable**: an item-by-item mapping of the original text, missing nothing | 逐條對照表與報告 / per-entry tables and report |

## 3. 原則 / Principles

| # | 原則 / Principle |
|---|---|
| P1 | **原文為準**：每個實體、性質、關係都附條目編號，可回到原文。/ **Text-anchored**: every node, property and edge carries its entry IDs. |
| P2 | **名稱只是符號**：計分時一律不使用名稱與今名的相似度。描述性的族名（如「黑齒」）只有在該族作為主語時才算描述。/ **Names are symbols**: name similarity never scores; descriptive ethnonyms count only when the people is the subject. |
| P3 | **全球候選**：候選庫覆蓋全部有人居住的大陸；候選庫在跑分前提交，之後的修改要在提交訊息中說明。/ **Global candidates**: the base covers every inhabited continent, is committed before scoring, and later changes are explained in commits. |
| P4 | **關係優先於相似**：單一實體的相似只算「自身分數」；可信度主要來自它與鄰近實體的候選是否互相一致。/ **Relations over resemblance**: resemblance gives only an own score; confidence comes mainly from consistency with neighbours' candidates. |
| P5 | **距離只是參考**：里數與方位權重很小，不能單獨否定一個候選。/ **Distances are a reference**: small weight, never decisive alone. |
| P6 | **罕見度加權、矛盾扣分、未知取基準率**：罕見的吻合權重大；明確的矛盾扣分；資料未知時取基準率期望，不讓資料較詳的地區佔便宜。/ **Rarity-weighted, contradictions subtract, unknowns at base rate.** |
| P7 | **不遺漏**：交付必須涵蓋原書每一段、每一個抽出的實體；無法對應的也要列出原因。覆蓋檢查不通過，不得交付。/ **Nothing missed**: the deliverable covers every paragraph and every extracted entity; unmapped items are listed with reasons. No delivery without a passing coverage audit. |
| P8 | **可重現**：所有步驟是標準庫腳本，固定種子，輸出逐位元組可重現。/ **Reproducible**: standard-library scripts, fixed seeds, byte-identical outputs. |

### 3.1 解讀規則 / Reading rules（2026-10-19，項目發起人採用 / adopted by the initiator）

古籍的作者看到的是**外觀**，寫下的是**當時**的樣子。以下規則對**所有候選一體適用**，每一種寬容都要付一點代價，否則任何地點都能被說成吻合。
The authors recorded what things **looked like**, **at the time**. These rules apply to **every candidate alike**, and each leniency costs a little; otherwise any place can be made to fit.

| # | 規則 / Rule | 計分 / Scoring |
|---|---|---|
| R1 | **水只是水體**：「河」「水」「海」「澤」都可能是河、湖或海；詞與實際類型不同時小扣分。/ **A water is just a water body**: 河, 水, 海, 澤 may be a river, lake or sea; a small cost when the type differs. | 類型不同 −0.3 |
| R2 | **時間深度**：書中所見可能是今日已消失或已成遺跡的地物（古河道、古湖、運河遺跡）；必須有一般性資料來源，並小扣分。/ **Time depth**: features may be gone or relics today (palaeo-rivers, former lakes, canal relics); a general source is required, at a small cost. | 古水體 −0.2 |
| R3 | **山只是外觀**：「山」可能是自然山、沙丘、方山，或人工的高大建築（金字塔、塔廟、平臺丘）。/ **A mountain is an outlook**: natural peaks, dunes, mesas, or tall built forms (pyramids, ziggurats, platform mounds). | 依性質計分，例「削成而四方」= 方形外觀 |
| R4 | **外觀與效果**：描述可依外觀或效果吻合；「投物輒然」可讀為火（火山、天然氣）或足以燒熟物品的高溫地表。/ **Appearance and effect**: 投物輒然 may be fire (volcanic or gas) or a surface hot enough to cook. | 兩種解讀的聯集作為一項性質 |
| R5 | **方位慣例**：觀察者面向東方（面向編者的故土），所以「前」= 東、「後」= 西；另一慣例（前 = 南）保留並作為對照計分。/ **Orientation**: the observer faces east (toward the compilers' homeland), so 前 = east and 後 = west; the other convention (前 = south) is kept and scored as a check. | 兩種慣例都報告 |
| R6 | **地圖讀法**：「X 出焉，東南流注于 Y」描述的是地圖上的一條線：一端在此、往東南延伸、與 Y 相接；不一定是源頭和流向。/ **Map view**: 「X出焉，東南流注于Y」 is a line on a map: one end here, extending southeast, joining Y; not necessarily source and flow. | 另一端吻合 ×0.8；方向相反 −0.1；反向相接 +1.5（正向 +2.0）|
| R7 | **觀察者替代**：沒見過的動物以熟悉的動物描述（獅 → 虎）。/ **Observer substitution**: an unfamiliar animal described as a familiar one (lion → tiger). | 由描述特徵的權重處理，不另加分 |

**對稱檢查 / Symmetry check**：每次使用這些規則，紅隊都要確認同樣的寬容也給了對立的候選，並比較採用前後各候選的總分。/ The red team checks that every leniency was also given to the rival candidates.

**假說檢驗 / Hypothesis tests**：一個解讀（例如「西次三經 = 古埃及」）被寫成一個**固定組態**：把相關實體固定在假說的候選上，其餘全書重新擬合；與不固定的基準及對立組態比較總分，並列出被違反的關係。/ A reading becomes a **held configuration**; the rest of the book is re-fitted, and its energy is compared with the free baseline and with rival configurations, listing the relations it breaks.

## 4. 知識圖譜 / Knowledge graph

- **節點 / Nodes**：實體，類型為山、水（河、海、澤）、地（沙、野、丘）、國族、生物、植物、礦物、神人。/ Entities of type mountain, water, land feature, polity/people, creature, plant, mineral, person/deity.
- **邊 / Edges**：有類型的關係，例如路線相鄰、水出於山、水注入水、山有某物產、某生物見於某山、某國在某國某方、某人生某人。每條邊都附條目編號與原文。/ Typed relations, each with entry IDs and the source clause.
- **格式 / Formats**：JSONL（`nodes.jsonl`、`edges.jsonl`）與 GraphML 匯出。/ JSONL plus a GraphML export.

## 5. 計分 / Scoring

**自身分數 / Own score**（候選 c 對實體 e）：e 的每個性質，若 c 具有則 +w，明確沒有則 −w，未知則 w·(2p − 1)；w = log₁₀(N_known / N_true) + 0.05。生物以描述特徵的覆蓋率計分。
For each property of e: +w if c has it, −w if c clearly lacks it, w·(2p − 1) if unknown.

**關係分數 / Relation score**：每條邊依兩端當前候選是否在真實世界中具有相同的關係計分（例如書中「A 水注入 B 水」，候選 A′ 的河口是否正是 B′）。關係的權重依其可檢驗程度設定，距離與方位類關係權重最小。
Each edge scores by whether the two ends' current candidates stand in the same relation in the real world; distance and bearing relations weigh least.

**唯一性 / Uniqueness**：兩個書中實體對到同一個真實的同類實體（例如兩條書中河流對到同一條真實河流）時，每對扣分。/ A penalty per pair of text entities mapped to the same real entity of a kind that should be unique (e.g. rivers).

**聯合求解 / Joint solution**：對所有實體**同時**求解，使總分 E = Σ 自身分數 + Σ 關係分數 − 唯一性懲罰 最高：模擬退火（固定種子，部分提議由關係引導），再用迭代條件眾數法收尾，最後做**區塊調整**（一個實體連同其相鄰實體一起換候選，總分上升才接受）。對應 = 總分最高的組態；不用逐實體多數決，因為各自的贏家拼不起來。
Solve all entities **jointly** for the highest E = Σ own + Σ relation − uniqueness: simulated annealing (fixed seeds, partly relation-guided proposals), iterated conditional modes, then **block moves** (an entity changes together with its neighbours; kept only if E rises). The mapping is the best-energy configuration, never per-entity majority votes, whose winners do not fit together.

**可信度 / Confidence** = 穩定度 × (1 − e^(−邊際))。穩定度是全部樣本（完整求解，以及多次隨機略去 20% 關係的重解）中選到同一候選的比例；邊際是該實體最佳與次佳候選的局部分差。分級：高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、**暫定 < 0.1**（總分最高，但樣本意見不一，不宜引用）。
stability × (1 − e^(−margin)); stability = share of samples (full solves and re-solves with 20% of relations dropped) choosing the same candidate; margin = local best minus second best. High ≥ 0.6, medium ≥ 0.3, low ≥ 0.1, **tentative < 0.1** (best-energy pick, but samples disagree: do not cite).

**必做檢查 / Mandatory checks**：同一輸入兩次執行，輸出逐位元組相同；任何「變好才接受」的步驟不得讓總分下降；抽查原文自己的陳述（「A 注于 B」）是否在對應中成立。/ Two runs give identical bytes; accept-if-better steps never lower E; spot-check the text's own statements.

## 6. 交付的完整性 / Completeness of the deliverable

1. 每一段原文都出現在逐條對照表中。/ Every paragraph appears in the per-entry table.
2. 每一段中抽出的每個實體都有一行對應（或「未對應」及原因：無候選、非地理實體、證據不足）。/ Every entity in every paragraph has a row (or "unmapped" with a reason).
3. 覆蓋檢查列出：沒有抽到任何實體的段落、名稱模式（「曰X之山」「X水」「X國」「名曰X」）出現但未抽出的地方。這兩項必須為零，或逐項說明。/ The coverage audit lists paragraphs with no entity and name patterns not extracted; both must be zero or individually explained.

## 7. 紅隊 / Red team
- 候選庫的組成與分析者的熟悉程度，是否讓某些地區更容易勝出？/ Does base composition or analyst familiarity favour some regions?
- 高可信度的對應，是否只依賴一兩條關係？移除後是否仍成立？/ Do high-confidence mappings rest on one or two relations?
- 是否有關係被違反卻仍選了該候選？違反的關係要列出。/ Which relations does the chosen mapping violate? List them.
- 低可信度或暫定的對應，是否被當作結論引用？/ Is a low or tentative mapping being cited as a finding?
- 支持的關係是否其實是抽取錯誤（比喻、篇名、誤併的同名）？/ Is a supporting relation an extraction artifact?
