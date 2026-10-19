# Mythos — 尋找古籍、神話、傳說中的宇宙真相

> **繁體中文** ｜ [English](#english)

Mythos 是一個開放研究項目：把古籍、神話與傳說當作**可能保存了真實觀測的資料**來閱讀，用可重現、可證偽的方法，把它們放回現有的世界觀與宇宙觀中檢驗，看看它們可能記錄了什麼。

第一個子項目是 **《山海經》**（[projects/shanhaijing](projects/shanhaijing/README.md)）。完整初稿（全書全球對照）見 [draft v1.0](projects/shanhaijing/reports/draft-v1.0-global.md)；方法 A 的初稿見 [draft v0.2](projects/shanhaijing/reports/draft-v0.1.md)。

## 核心原則

1. **原文優先**：每個結論都要引到可追溯的條目編號（例如 `SHJ-02-3-006`），並引用原文。
2. **不繼承結論**：歷代注疏和現代學說（包括郭璞注、袁珂校注，以及各種「山海經即世界地理」之說）一律只登記為**待檢驗的假說**，不當作證據。
3. **先登記，再檢驗**：假說要先寫明預測和證偽條件，才能進行檢驗。
4. **多軸交叉定位**：地理幾何、水系、生物分佈與遷徙、礦產、天文氣候、族群、跨文本等證據通道要互相獨立，交叉印證。
5. **錯誤要有模型，也要付代價**：每一次文本校改都要有根據，而且會計入假說的「校改預算」，防止為了遷就假說而過度擬合。
6. **可重現**：原始資料、腳本和推理鏈全部存放在倉庫中。

## 倉庫結構

| 路徑 | 內容 |
|---|---|
| [docs/](docs/README.md) | 總體文檔：白皮書、PRD、研究框架、架構、規範、詞彙表、路線圖 |
| [reference/](reference/README.md) | 古籍原文（公有領域），含多個版本見證本與結構化條目 |
| [projects/shanhaijing/](projects/shanhaijing/README.md) | 山海經子項目：研究方法規格、資料模型、任務、假說卷宗、研究發現 |
| [tools/](tools/shj) | 可重現的處理腳本（匯入、校勘、路線抽取、鏈條擬合） |
| [.claude/](.claude/) | 配套的研究 agent 與 skill（公共 + 山海經專用） |

## 快速開始

```bash
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/extract_routes.py
```

---

<a id="english"></a>
# Mythos — Seeking the Truths of the Universe in Ancient Texts, Myths and Legends

Mythos is an open research project. It reads ancient texts, myths and legends as **records that may preserve real observations**, then tests them against our present understanding of the world and the cosmos with reproducible, falsifiable methods to find out what they may actually record.

The first sub-project is the **Shanhaijing 《山海經》** ([projects/shanhaijing](projects/shanhaijing/README.md)).

## Core principles

1. **Text first**: every claim cites a traceable entry ID (e.g. `SHJ-02-3-006`) and quotes the source text.
2. **No inherited conclusions**: classical commentary and modern theories (Guo Pu, Yuan Ke, the various "Shanhaijing is world geography" theses) are registered only as **hypotheses to be tested**, never used as evidence.
3. **Pre-register, then test**: a hypothesis states its predictions and falsifiers before any test is run.
4. **Multi-axis triangulation**: independent evidence channels (itinerary geometry, hydrology, biogeography and migration, minerals, astronomy and climate, peoples, cross-corpus) must corroborate each other.
5. **Errors need a model and carry a cost**: every textual emendation must be justified, and it is charged to the hypothesis's *correction budget* to prevent overfitting.
6. **Reproducible**: raw sources, scripts and reasoning chains are all kept in the repository.

See the [whitepaper](docs/whitepaper.en.md), the [PRD](docs/prd.en.md) and the [Shanhaijing methodology spec](projects/shanhaijing/docs/methodology-spec.md).

## License

Code and documentation: Apache-2.0 ([LICENSE](LICENSE)). The ancient source texts are public domain. Wikisource transcriptions are CC BY-SA 4.0; see [reference/shanhaijing/README.md](reference/shanhaijing/README.md).
