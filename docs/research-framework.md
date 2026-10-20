# Mythos 研究框架：時代語義對應 / Research Framework: Era-Semantic Correspondence

> v3.2 ・ 2026-10-20 ・ 適用於所有語料的公共方法。山海經的實作見 [methodology-spec.md](../projects/shanhaijing/docs/methodology-spec.md)，時代世界見 [era-world.md](../projects/shanhaijing/docs/era-world.md)。
> 全球全域雙向反推架構（河南商都為天下之中，西至非洲、東至美洲、北至北極、南至南海，4000–1000 BCE）。

---

## 1. 立場 / Stance

**繁中**：古籍是**積累的傳承紀錄**：它保存的是寫下當時（以及更早口傳時）看到的世界，經過長期傳抄，有缺失也有錯誤。我們把它放回**當時的世界**（當時的海岸線、河道、氣候、動物、文明與其造物）來對應，而不是今日的地圖；也不預設它記的是哪一個地區的地理。
以**河南商都中原（約北緯 34.7°、東經 113.6°）為天下之「中」**，向西跨歐亞腹地延伸至近東與北非（蘇美、埃及、尼羅河、紅海、撒哈拉），向東跨太平洋邊緣、白令海峽至美洲（奧爾梅克、瑪雅、卡拉爾），向北達北極圈（極夜極晝、極光），向南達印度洋與熱帶海域。
對應的依據是**語義相關性與客觀物理屬性**（外觀、顏色、尺度、材質、功能、聲音、習性、方位），由大模型逐項推理並記錄理由，再由全書的關係**聯合求解**，保證整體一致。進一步實施**雙向反推**：以古籍保留但現代已無之生態與水網，反演公元前 4000–前 1000 年的地球古環境。

## 2. 十個步驟 / Ten steps

| # | 步驟 / Step | 產出 / Output |
|---|---|---|
| 0 | **原始文本**：只用最早的見證本；注疏一律不進入任何步驟 / earliest witness only; commentary never enters | 工作文本 / working text |
| 1–2 | **實體與關係**：全書實體、描述、性質、關係（含名稱的語義特徵，絕不套用今名）/ entities, descriptions, relations, name semantics | 知識圖譜 / knowledge graph |
| 3 | **觀察框架**：以中原為原點理解方位與里程，以周秦漢里及黃金緯度帶校準 / origin frames bearings, calibrated by Golden Latitude Belt | 方位與里數幾何約束 / geometric constraints |
| 4 | **時代世界**：涵蓋非洲、兩河、中原、美洲、北極之全球時代世界庫 / global era world base | 時代世界庫 / era world base |
| 5 | **候選生成**：大模型在名稱遮蔽下開放提出候選，至少含兩個對立候選 / open candidates under name masking, with rivals | 候選卡 / candidate cards |
| 6 | **語義評分**：逐項屬性打分，附原文證據與現象學解碼理由，多次取樣 / attribute-wise scores with sensory decoding, sampled | 判斷紀錄 / judgment records |
| 7 | **關係評分**：每條關係在當時是否成立 / does each relation hold at the time | 關係判斷 / relation judgments |
| 8 | **聯合求解**：以自身分數與關係分數，求全書最一致的組態 / joint solution | 對應 / mapping |
| 9 | **可信度與紅隊**：樣本一致度、洩漏與誘餌測試、假說組態比較 / confidence, leakage, decoy tests, held configurations | 可信度、審查 / confidence, review |
| 10 | **交付與反推**：逐段對照、時代地圖、以及**古地球環境反演報告** / item-by-item mapping and reverse paleoworld report | 交付版本 / deliverable |

## 3. 原則 / Principles

| # | 原則 / Principle |
|---|---|
| P1 | **原文為準**：只用原始古本；每個實體、性質、關係都附條目編號與原句。注疏與前人學說不作為證據，也不作為輸入。/ **Original text only.** |
| P2 | **全球視野與中心原點**：以中原（河南商都）為天下之「中」，向四方輻射至歐非、美洲與極地。/ **Global scope from Central Plains origin.** |
| P3 | **時代世界**：候選依公元前 4000–前 1000 年窗口內的狀態計分（存在、廢墟、已消失、已滅絕）。/ **The world of the period.** |
| P4 | **語義相關、逐項有據**：每個分數都能回到原文的一句話與候選的一項物理屬性；理由寫下來。/ **Semantic, attribute by attribute.** |
| P5 | **名稱語義保留、今名絕不比對**：古名今名完全脫鉤。名稱不作為辨識依據，只提取其中的物理語義特徵（顏色、材質、形貌）。/ **Name semantics kept, modern names never matched.** |
| P6 | **容許傳承錯誤**：缺失不算矛盾；單項不符的扣分有上限；吻合越多，假設越成立。/ **Transmission errors tolerated.** |
| P7 | **關係優先於相似**：可信度主要來自全書水系流向與相對幾何的一致。/ **Relations over resemblance.** |
| P8 | **對稱**：每一種寬容與每一類候選，都對全世界一體適用。/ **Symmetry worldwide.** |
| P9 | **大模型推理可審查**：判斷時遮蔽名稱；以結構化語義向量與物理現實比對。/ **Auditable LLM reasoning.** |
| P10 | **先入知識防範**：以遮蔽檢測、人工誘餌、對立假說競爭，防止受近世地名預設立場影響。/ **Guard against prior knowledge.** |
| P11 | **雙向反推（Reverse Paleoworld）**：古籍中保留但現代地圖已無之河流、湖泊、林木與特異生物，反向用於填補古氣候學與古生物學空白。/ **Bidirectional reverse-reconstruction.** |
| P12 | **距離尺度與黃金緯度帶校準**：里數以周秦漢里（約 0.35–0.42 公里／里）為初始值，西向 18,924 里（7,534 km 開羅）與東向 18,869 里（7,547 km 北美縱貫）宏觀幾何對稱。/ **Scale calibrated along the 30°–35°N Golden Latitude Belt.** |

### 3.1 解讀與幾何規則（R1–R15）

| # | 規則 / Rule |
|---|---|
| R1 | **水只是水體**：河、水、海、澤都可能是河、湖或海。/ A water is just a water body. |
| R2 | **時間深度**：已消失或已成遺跡的地物（古河道、古湖、運河、廢墟）可作候選。/ Time depth: vanished features and ruins count. |
| R3 | **山只是外觀**：自然山、沙丘、方山，或人工的巨型高大建築（金字塔、塔廟）。/ A mountain is an outlook, natural or built. |
| R4 | **外觀與效果**：描述可依外觀或效果吻合（例：投物輒然 = 瀝青火井或熱浪沙漠）。/ Appearance and effect. |
| R5 | **方位慣例**：前 = 東（面向編者的故土），前 = 南作對照。/ Orientation conventions. |
| R6 | **地圖讀法**：出、流、注描述地圖上的一條線，不一定是源頭與流向。/ Map view of courses. |
| R7 | **觀察者替代**：以熟悉的事物描述陌生的事物（獅 → 虎）。/ Observer substitution. |
| R8 | **時代窗口與積累**：窗口內不同部分可能來自不同時期；每個候選標上存在年代。/ Window and accumulation. |
| R9 | **觀察者原點與黃金緯度帶**：方位與里程從河南商都（34.7°N, 113.6°E）出發，沿北緯 30°–35° 歐亞非走廊延伸。/ Observer origin along 30°–35°N. |
| R10 | **古名今名完全脫鉤**：嚴禁套用現代同名地標。例如「華山」為「光華第一大山」，非陝西華山；「崑崙」為「至高重級神山/巨石高台」。/ No modern toponym presupposition. |
| R11 | **傳承錯誤容許**：字形相近、傳抄漏簡、數字量級夸飾容許替代讀法。/ Transmission error tolerance. |
| R12 | **現象學與感知轉譯**：極端天象與地貌以直觀視覺比喻解碼（極光極夜 ↔ 燭龍；幻日/日曆神木 ↔ 扶桑十日；海溝深淵 ↔ 歸墟大壑；地熱沸泉 ↔ 湯谷）。/ Phenomenological decoding. |
| R13 | **雙向古環境反推**：古籍中記述之水網林木與動物，用於反向校正公元前 4000–前 1000 年古氣候模型。/ Bidirectional paleo-reconstruction. |
| R14 | **全域四篇串聯接力幾何**：西山經四篇總計 18,924 里，折合 7,569.6 公里，與中原至開羅（7,534 公里）吻合度達 99.5%；東山經四篇總計 18,869 里，折合 7,547.6 公里，與北美洲縱貫全幅（~7,500 公里）高度咬合。/ 4-section chained relay geometry: West 18,924 li ≈ East 18,869 li ≈ 7,500 km. |
| R15 | **同名消歧之距離判準原則**（項目發起人，2026-10-20）：<br>1. **遠距同名拆分**：距離較遠的同名實體，視為不同實體（如埃及尼羅河黑水 vs 蜀地都廣黑水 vs 西伯利亞幽都黑水；開羅吉薩崑崙 vs 絲路海內崑崙中繼神城）。<br>2. **近距跨卷合併**：近似地域不同經卷的同名實體，視為同一實體（如西次三經崑崙與大荒西經崑崙皆為開羅吉薩；海內南經建木與海內經建木皆為三星堆青銅神樹；海外東經湯谷扶桑與大荒東經湯谷扶木皆為瑪雅日曆天樹）。<br>3. **爭議備註推進**：無法絕對解決的爭議點，記錄邏輯推理假說並加入備註，不阻斷管線推進，待全書解讀 draft 完成後集中覆核處理。/ **Distance-based homonym disambiguation rule.** |
