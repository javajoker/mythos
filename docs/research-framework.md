# Mythos 研究框架：實體圖譜交叉驗證 / Research Framework: Entity-Graph Cross-Validation

> v2.0 ・ 2026-10-19 ・ 適用於所有語料的公共方法。山海經的實作見 [methodology-spec.md](../projects/shanhaijing/docs/methodology-spec.md)。
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

## 4. 知識圖譜 / Knowledge graph

- **節點 / Nodes**：實體，類型為山、水（河、海、澤）、地（沙、野、丘）、國族、生物、植物、礦物、神人。/ Entities of type mountain, water, land feature, polity/people, creature, plant, mineral, person/deity.
- **邊 / Edges**：有類型的關係，例如路線相鄰、水出於山、水注入水、山有某物產、某生物見於某山、某國在某國某方、某人生某人。每條邊都附條目編號與原文。/ Typed relations, each with entry IDs and the source clause.
- **格式 / Formats**：JSONL（`nodes.jsonl`、`edges.jsonl`）與 GraphML 匯出。/ JSONL plus a GraphML export.

## 5. 計分 / Scoring

**自身分數 / Own score**（候選 c 對實體 e）：e 的每個性質，若 c 具有則 +w，明確沒有則 −w，未知則 w·(2p − 1)；w = log₁₀(N_known / N_true) + 0.05。生物以描述特徵的覆蓋率計分。
For each property of e: +w if c has it, −w if c clearly lacks it, w·(2p − 1) if unknown.

**關係分數 / Relation score**：每條邊依兩端當前候選是否在真實世界中具有相同的關係計分（例如書中「A 水注入 B 水」，候選 A′ 的河口是否正是 B′）。關係的權重依其可檢驗程度設定，距離與方位類關係權重最小。
Each edge scores by whether the two ends' current candidates stand in the same relation in the real world; distance and bearing relations weigh least.

**聯合求解 / Joint solution**：從各實體的最佳自身候選開始，反覆為每個實體選擇「自身分數＋與鄰居一致的關係分數」最高的候選，直到不再變化。多次重啟，每次隨機略去一部分關係，以檢驗穩定性。
Start from each entity's best own candidate; repeatedly re-choose the candidate maximising own score plus relation score given the neighbours, until stable. Restart several times, each time dropping a random share of relations, to test stability.

**可信度 / Confidence** = 穩定度 × (1 − e^(−邊際))。穩定度是各次重啟中選到同一候選的比例；邊際是最佳與次佳候選的總分差。分級：高 ≥ 0.6，中 0.3–0.6，低 < 0.3。
stability × (1 − e^(−margin)); stability = share of restarts choosing the same candidate; margin = best minus second-best total. High ≥ 0.6, medium 0.3–0.6, low < 0.3.

## 6. 交付的完整性 / Completeness of the deliverable

1. 每一段原文都出現在逐條對照表中。/ Every paragraph appears in the per-entry table.
2. 每一段中抽出的每個實體都有一行對應（或「未對應」及原因：無候選、非地理實體、證據不足）。/ Every entity in every paragraph has a row (or "unmapped" with a reason).
3. 覆蓋檢查列出：沒有抽到任何實體的段落、名稱模式（「曰X之山」「X水」「X國」「名曰X」）出現但未抽出的地方。這兩項必須為零，或逐項說明。/ The coverage audit lists paragraphs with no entity and name patterns not extracted; both must be zero or individually explained.

## 7. 紅隊 / Red team
- 候選庫的組成與分析者的熟悉程度，是否讓某些地區更容易勝出？/ Does base composition or analyst familiarity favour some regions?
- 高可信度的對應，是否只依賴一兩條關係？移除後是否仍成立？/ Do high-confidence mappings rest on one or two relations?
- 是否有關係被違反卻仍選了該候選？違反的關係要列出。/ Which relations does the chosen mapping violate? List them.
