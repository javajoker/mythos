# Mythos 研究框架：時代語義對應 / Research Framework: Era-Semantic Correspondence

> v3.0 ・ 2026-10-20 ・ 適用於所有語料的公共方法。山海經的實作見 [methodology-spec.md](../projects/shanhaijing/docs/methodology-spec.md)，時代世界見 [era-world.md](../projects/shanhaijing/docs/era-world.md)。
> The common, corpus-agnostic method. Shanhaijing implementation: methodology-spec.md; the world of the period: era-world.md.
> 這是唯一的現行方法；先前的版本只保留在 git 歷史中。/ The only current method; earlier versions are in git history only.

---

## 1. 立場 / Stance

**繁中**：古籍是**積累的傳承紀錄**：它保存的是寫下當時（以及更早口傳時）看到的世界，經過長期傳抄，有缺失也有錯誤。我們把它放回**當時的世界**（當時的海岸線、河道、氣候、動物、文明與其造物）來對應，而不是今日的地圖；也不預設它記的是哪一個地區的地理。對應的依據是**語義相關性**：書中描述的屬性（外觀、顏色、尺度、材質、功能、聲音、習性、方位），與候選在當時所具有的屬性是否相符；由大模型逐項推理並記錄理由，再由全書的關係**聯合求解**，保證整體一致。

**EN**: An ancient text is an **accumulated, transmitted record** of the world as seen when it was written (and earlier, orally), copied for a long time, with losses and errors. We map it onto the **world of that time** (its coastlines, rivers, climate, animals, civilisations and their works), not today's map, and presuppose no region. Matching rests on **semantic correspondence** between the attributes the text describes and those a candidate had at the time, judged attribute by attribute by a large language model with recorded reasons, then **solved jointly** across the book's relations for overall consistency.

## 2. 十個步驟 / Ten steps

| # | 步驟 / Step | 產出 / Output |
|---|---|---|
| 0 | **原始文本**：只用最早的見證本；注疏一律不進入任何步驟 / earliest witness only; commentary never enters | 工作文本 / working text |
| 1–2 | **實體與關係**：全書實體、描述、性質、關係（含名稱的語義特徵）/ entities, descriptions, relations, name semantics | 知識圖譜 / knowledge graph |
| 3 | **觀察框架**：以編者所在的原點理解方位與里程 / the compilers' origin frames bearings and distances | 方位與里數的軟約束 / soft geometric constraints |
| 4 | **時代世界**：時代窗口內的地理、動物、文明與造物，每項附存在年代與當時樣貌 / the world of the period, each item with its dates and state | 時代世界庫 / era world base |
| 5 | **候選生成**：大模型在名稱遮蔽下開放提出候選，至少含兩個對立候選 / open candidates under name masking, with rivals | 候選卡 / candidate cards |
| 6 | **語義評分**：逐項屬性打分，附原文證據與理由，多次取樣 / attribute-wise scores with evidence and reasons, sampled | 判斷紀錄 / judgment records |
| 7 | **關係評分**：每條關係在當時是否成立 / does each relation hold at the time | 關係判斷 / relation judgments |
| 8 | **聯合求解**：以判斷分數為自身分數與關係分數，求全書最一致的組態 / joint solution | 對應 / mapping |
| 9 | **可信度與紅隊**：樣本一致度、判斷差異、洩漏與誘餌測試、假說組態比較 / confidence, leakage and decoy tests, held configurations | 可信度、審查 / confidence, review |
| 10 | **交付**：逐段、逐實體對照，加上**當時的地圖** / item-by-item mapping and a map of the period | 交付版本 / deliverable |

## 3. 原則 / Principles

| # | 原則 / Principle |
|---|---|
| P1 | **原文為準**：只用原始古本；每個實體、性質、關係都附條目編號與原句。注疏與前人學說不作為證據，也不作為輸入。/ **Original text only**, every item anchored to entries; commentary and prior scholarship are neither evidence nor input. |
| P2 | **不預設地區**：不預設山海經是任何一地的地理志；編者所在地只是觀察的原點，不是答案。所有地區在同一候選池中公平競爭。/ **No presupposed region**; the compilers' location is the observer's origin, not the answer. |
| P3 | **時代世界**：候選依時代窗口內的狀態計分（存在、廢墟、已消失、已滅絕）；不在窗口內存在的，不能作為候選。/ **The world of the period**: candidates score by their state within the window. |
| P4 | **語義相關、逐項有據**：每個分數都能回到原文的一句話與候選的一項屬性；理由寫下來。/ **Semantic, attribute by attribute, with evidence and reasons.** |
| P5 | **名稱的語義保留、今名不比對**：名稱不作為辨識依據，但其中的語義特徵（顏色、材質、形狀、狀態）是描述的一部分；不得因今名相同或相似而加分（「赤水」不因今名「紅海」而吻合，要比的是外觀為紅色的水）。/ **Name semantics kept, modern names never matched.** |
| P6 | **容許傳承錯誤**：缺失不算矛盾；單項不符的扣分有上限；吻合越多，假設越成立；錯字、數字訛誤、錯簡可作為替代讀法並小幅扣分。/ **Transmission errors tolerated**: absence is not contradiction; capped per-item penalties; variant readings at a small cost. |
| P7 | **關係優先於相似**：可信度主要來自全書關係的一致，而非單一實體的相似。/ **Relations over resemblance.** |
| P8 | **對稱**：每一種寬容與每一類候選，都對所有地區一體適用；新增候選要在全世界同類中一起加入。/ **Symmetry**: every leniency and every kind of candidate applies worldwide. |
| P9 | **大模型判斷可審查、可重現**：判斷時遮蔽名稱；每個判斷存成紀錄（輸入、分數、證據、理由、模型、提示詞版本、樣本序號）；只有輸入改變才重判；同一判斷取多個樣本，差異計入可信度。/ **LLM judgments are masked, recorded, re-run only on change, and sampled.** |
| P10 | **先入知識的防範**：大模型讀過注疏與各種比定；以遮蔽與不遮蔽的差異、人工誘餌、對立候選檢測，受先入知識影響的判斷降低可信度。/ **Guard against prior knowledge** with masking contrasts, decoys and rivals. |
| P11 | **不遺漏**：交付涵蓋每一段、每一個實體，未對應的寫明原因；完整性檢查不通過不得交付。/ **Nothing missed.** |
| P12 | **距離是絕對距離、單位未知**：里數視為直線距離（不假設是沿路里程），單位長度未知、全書共用一個，由求解決定；各篇只描述篇內距離，篇與篇之間沒有距離、只有相對位置，所以每一篇獨立錨定；距離是軟約束，不能單獨否定候選。/ **Distances are absolute, in one unknown unit**; sections are anchored independently and relate only by relative position; soft constraints. |

### 3.1 解讀規則 / Reading rules

R1–R7 由項目發起人於 2026-10-19 採用，R8–R12 於 2026-10-20 加入；全部對所有候選一體適用，每一種寬容都付一點代價。
R1–R7 adopted 2026-10-19, R8–R12 added 2026-10-20; all apply to every candidate, each at a small cost.

| # | 規則 / Rule |
|---|---|
| R1 | **水只是水體**：河、水、海、澤都可能是河、湖或海。/ A water is just a water body. |
| R2 | **時間深度**：已消失或已成遺跡的地物（古河道、古湖、運河、廢墟）可作候選。/ Time depth: vanished features and ruins count. |
| R3 | **山只是外觀**：自然山、沙丘、方山，或人工的高大建築。/ A mountain is an outlook, natural or built. |
| R4 | **外觀與效果**：描述可依外觀或效果吻合（例：投物輒然 = 火或酷熱）。/ Appearance and effect. |
| R5 | **方位慣例**：前 = 東（面向編者的故土），前 = 南作對照。/ Orientation, with the alternative as a check. |
| R6 | **地圖讀法**：出、流、注描述地圖上的一條線，不一定是源頭與流向。/ Map view of courses. |
| R7 | **觀察者替代**：以熟悉的事物描述陌生的事物（獅 → 虎）。/ Observer substitution. |
| R8 | **時代窗口與積累**：窗口內不同部分可能來自不同時期；每個候選標上存在年代，相鄰實體的年代相差太遠時小扣分。/ Window and accumulation. |
| R9 | **觀察者原點**：方位與里程從編者所在的原點理解（山海經：中原）。/ Observer origin. |
| R10 | **名稱語義**：名稱中的顏色、材質、形狀、狀態詞作為描述特徵，權重低於原文描述，並標明「來自名稱」。/ Name semantics, weighted below the description and flagged. |
| R11 | **傳承錯誤**：缺失、錯字、數字訛誤、錯簡（見 P6）。/ Transmission errors. |
| R12 | **聯想**：描述可以經由自然現象的聯想吻合（例：「十日」↔ 寒冷空氣中的幻日、高緯度夏季不落的太陽；「視為晝，瞑為夜，吹為冬，呼為夏」↔ 極晝與極夜；「赤色」↔ 紅色極光）。聯想單獨計分、權重最低（0.3）、每次標明「聯想」，且對所有候選一體適用。/ Association through natural phenomena, separately scored at the lowest weight, flagged, symmetric. |

## 4. 知識圖譜 / Knowledge graph
節點為實體（山、水、地、國族、生物、植物、礦物、神人），邊為有類型的關係；每條附條目編號與原句；名稱的語義特徵作為節點的「名稱特徵」欄位。JSONL 與 GraphML。/ Nodes, typed edges, entry IDs, name features as a separate field.

## 5. 計分與求解 / Scoring and solving

**語義判斷 / Semantic judgments**：對每個實體與候選，按屬性維度（外觀、顏色、尺度、材質、功能、聲音、習性、生態、方位、年代可見性）給 0–1 的吻合分數與「矛盾」標記，各附原文證據與候選屬性；名稱特徵單獨計分。多次取樣（預設 3 次），取平均與標準差。
Per entity and candidate: 0–1 per attribute dimension with a contradiction flag, each with text evidence and the candidate's attribute; name features scored separately; three samples by default.

**自身分數 / Own score** = Σ 維度權重 × 吻合 − Σ 有上限的矛盾扣分 + 名稱特徵 × 較低權重；罕見的屬性權重大（以候選池中具有該屬性的比例估計）。
Weighted agreement minus capped contradictions plus down-weighted name features; rare attributes weigh more.

**關係分數 / Relation score**：每條關係在**當時**是否成立的判斷（0–1，或依可計算的幾何與水系直接計算），權重依關係的可檢驗程度設定。/ Judged or computed at the time, weighted by testability.

**聯合求解、唯一性、可信度 / Joint solution, uniqueness, confidence**：對所有實體同時求解，使總分 E = Σ 自身分數 + Σ 關係分數 − 唯一性懲罰（兩個書中實體對到同一真實實體時扣分）最高：模擬退火（固定種子、部分提議由關係引導）、迭代條件眾數法、區塊調整（一個實體連同相鄰實體一起換候選，總分上升才接受）；不用逐實體多數決。可信度 = 穩定度（完整求解與略去 20% 關係的重解中一致的比例）× (1 − e^(−邊際)) × (1 − 判斷差異) × 洩漏折扣。級別：高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、暫定 < 0.1。
Joint energy maximisation with simulated annealing, ICM and block moves; confidence = stability × (1 − e^(−margin)) × (1 − judgment spread) × leakage discount.

**假說檢驗 / Hypothesis tests**：一個解讀寫成固定組態，其餘全書重新求解，與自由解及對立組態比較，列出被違反的關係。/ Held configurations against the free solution and rivals.

## 6. 交付的完整性 / Completeness
每一段、每一個實體都有一行（對應或原因）；覆蓋檢查與完整性檢查必須通過；地圖畫的是**時代窗口內**的世界。/ Every paragraph and entity; coverage and completeness pass; the map shows the world of the window.

## 7. 紅隊 / Red team
- 先入知識：遮蔽與不遮蔽的判斷差異；誘餌描述是否被套到熱門答案。/ Leakage and decoys.
- 今名比對：理由中是否出現今名的相似（「紅海」「黑海」等）作為依據。/ Modern-name matching in reasons.
- 對稱：寬容、名稱特徵、時代狀態是否對所有地區一體適用；新候選是否在全世界同類中一起加入。/ Symmetry.
- 庫的偏差：哪些地區、文明的候選卡較詳細。/ Base bias.
- 單點依賴：高可信度是否只靠一兩條關係或一個罕見特徵。/ Single-point dependence.
- 年代：候選在窗口內是否存在；相鄰實體的年代是否相合。/ Dates.
- 引用：暫定與低可信度的對應不得當作結論。/ No citing tentative results.
