# Mythos — 尋找古籍、神話、傳說中的宇宙真相

> **繁體中文** ｜ [English](#english)

Mythos 是一個開放研究項目：把古籍、神話與傳說當作**可能保存了真實觀測的傳承紀錄**來閱讀，放回**它們形成的那個時代的世界**中，用可審查、可重現的方法檢驗它們可能記錄了什麼。

第一個子項目是 **《山海經》**（[projects/shanhaijing](projects/shanhaijing/README.md)）：視為前 4000–前 2000 年逐步積累的紀錄，從中原出發，只用原文。

## 方法：時代語義對應（框架 v3）

1. 找出書中**所有實體**、它們的描述、關係，以及名稱中的語義（例：「赤」= 紅色）；
2. 建立**當時的世界**：當時的海岸線、河道、氣候、動物（含已滅絕者）、文明與其造物；
3. 在名稱遮蔽下，由大模型依**語義相關性**逐項評分（外觀、顏色、尺度、材質、功能、聲音、生態、方位、年代），附原文證據與理由；
4. 以全書的關係**聯合求解**，求最一致的對應，並計算可信度；
5. 交付：與原書**逐條對應**，不遺漏任何一段、任何一個實體，並畫出**當時的地圖**。

詳見 [研究框架](docs/research-framework.md)。

## 原則

- **原文為準**：只用原始古本；注疏與前人學說不作為證據，也不作為輸入。
- **不預設地區**：所有地區、所有同時期文明公平競爭。
- **名稱語義保留、今名不比對。**
- **容許傳抄錯誤**：缺失不算矛盾，吻合越多越可信。
- **可審查、可重現**：每個判斷都有紀錄；完整性檢查不通過不得交付。

## 倉庫結構

| 路徑 | 內容 |
|---|---|
| [docs/](docs/README.md) | 總體文檔：白皮書、PRD、研究框架、架構、規範、詞彙表、路線圖 |
| [reference/](reference/README.md) | 古籍原文（公有領域），含多個見證本與結構化條目 |
| [projects/shanhaijing/](projects/shanhaijing/README.md) | 山海經子項目：規格、時代世界、資料模型、任務、知識圖譜 |
| [tools/shj/](tools/shj) | 可重現的處理腳本 |
| [.claude/](.claude/) | 研究 agent 與 skill |

---

<a id="english"></a>
# Mythos — Seeking the Truths of the Universe in Ancient Texts, Myths and Legends

Mythos is an open research project. It reads ancient texts, myths and legends as **transmitted records that may preserve real observations**, places them back in **the world of the period that produced them**, and tests what they may record with auditable, reproducible methods.

The first sub-project is the **Shanhaijing 《山海經》** ([projects/shanhaijing](projects/shanhaijing/README.md)), read as a record accumulated between 4000 and 2000 BCE, from the Central Plains, in its original text only.

## Method: era-semantic correspondence (framework v3)

(1) every entity with its description, relations and name semantics; (2) the world of the period: coasts, rivers, climate, animals including extinct ones, civilisations and their works; (3) masked LLM judgments of semantic correspondence, attribute by attribute, with evidence and reasons; (4) joint solving across the book's relations, with confidence; (5) an item-by-item deliverable with a map of the period. See the [research framework](docs/research-framework.md).

## License

Code and documentation: Apache-2.0 ([LICENSE](LICENSE)). The ancient source texts are public domain. Wikisource transcriptions are CC BY-SA 4.0; see [reference/shanhaijing/README.md](reference/shanhaijing/README.md).
