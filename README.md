# Mythos — 尋找古籍、神話、傳說中的宇宙真相

> **繁體中文** ｜ [English](#english)

Mythos 是一個開放研究項目：把古籍、神話與傳說當作**可能保存了真實觀測的資料**來閱讀，用可重現的方法，把它們放回現有的世界觀與宇宙觀中檢驗，看看它們可能記錄了什麼。

第一個子項目是 **《山海經》**（[projects/shanhaijing](projects/shanhaijing/README.md)）。交付：[初稿 v2：全書逐段、逐實體的真實世界對照](projects/shanhaijing/deliverables/draft-v2/README.md)。

## 方法：實體圖譜交叉驗證

1. 找出書中**所有實體**並合併整合；
2. 取得每個實體的**描述、性質**，以及**實體之間的關係**，組成知識圖譜；
3. 在**全球**真實世界中為每個實體找出候選，可以有多個；書中名稱只是符號，不比對今名；
4. 用關係**交叉驗證**候選，求出整體最一致的對應，並計算**可信度**；
5. 交付：與原書**逐條對應**，不遺漏任何一段、任何一個實體。

詳見 [研究框架](docs/research-framework.md) 與 [山海經方法規格](projects/shanhaijing/docs/methodology-spec.md)。

## 原則

- **原文為準**：每個實體、關係都附條目編號（例如 `SHJ-02-3-006`），可回到原文。
- **不繼承結論**：注疏與前人學說不作為證據；候選只依描述與關係計分。
- **全球範圍、距離只是參考。**
- **不遺漏**：完整性檢查不通過，不得交付。
- **可重現**：標準庫腳本、固定種子，輸出逐位元組相同。

## 倉庫結構

| 路徑 | 內容 |
|---|---|
| [docs/](docs/README.md) | 總體文檔：白皮書、PRD、研究框架、架構、規範、詞彙表、路線圖 |
| [reference/](reference/README.md) | 古籍原文（公有領域），含多個見證本與結構化條目 |
| [projects/shanhaijing/](projects/shanhaijing/README.md) | 山海經子項目：方法規格、資料模型、任務、知識圖譜、交付 |
| [tools/shj/](tools/shj) | 可重現的處理腳本（文本層、知識圖譜、候選、交叉驗證、交付） |
| [.claude/](.claude/) | 研究 agent 與 skill（公共 + 山海經專用） |

---

<a id="english"></a>
# Mythos — Seeking the Truths of the Universe in Ancient Texts, Myths and Legends

Mythos is an open research project. It reads ancient texts, myths and legends as **records that may preserve real observations** and tests them, with reproducible methods, against our present understanding of the world and the cosmos.

The first sub-project is the **Shanhaijing 《山海經》** ([projects/shanhaijing](projects/shanhaijing/README.md)). Deliverable: [draft v2, a paragraph-by-paragraph, entity-by-entity real-world mapping of the whole book](projects/shanhaijing/deliverables/draft-v2/README.md).

## Method: entity-graph cross-validation

1. Find **every entity** in the text, merged and integrated.
2. Collect each entity's **description and properties** and the **relations between entities** into a knowledge graph.
3. Generate real-world candidates **worldwide**, several per entity if needed. Names in the text are symbols and are never matched to modern names.
4. **Cross-validate** the candidates through the relations, solve for the most consistent joint mapping, and compute **confidence**.
5. Deliver a mapping that follows the original **item by item**, missing no paragraph and no entity.

See the [research framework](docs/research-framework.md) and the [Shanhaijing method spec](projects/shanhaijing/docs/methodology-spec.md).

## Principles

Text-anchored (every entity and relation carries entry IDs) · no inherited conclusions (commentary and prior theories are not evidence) · global search space, with distances only as a reference · nothing missed (no delivery without a passing completeness check) · reproducible (standard-library scripts, fixed seeds, byte-identical outputs).

## License

Code and documentation: Apache-2.0 ([LICENSE](LICENSE)). The ancient source texts are public domain. Wikisource transcriptions are CC BY-SA 4.0; see [reference/shanhaijing/README.md](reference/shanhaijing/README.md).
