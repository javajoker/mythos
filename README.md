# Mythos — 尋找古籍、神話、傳說中的宇宙真相

> **繁體中文** ｜ [English](#english)

Mythos 是一個開放研究項目：把古籍、神話與傳說視為可能保存真實觀測的傳承紀錄，放回其形成的時代世界，以可審查、可重現的方法比較競爭解讀。

第一個子項目是 **《山海經》**（[projects/shanhaijing](projects/shanhaijing/README.md)），第一版時代窗口為 **4000–1000 BCE**。所有現實地理對應都是候選假說，不是前置答案。

## 方法：迭代時代語義對應（框架 v4）

1. 校勘見證本，建立有穩定 ID 和讀法狀態的工作文本；
2. 抽取實體、提及、名稱語義與文本關係；
3. 在名稱遮蔽下生成競爭候選，逐屬性形成地理語義擬合；
4. 建立初版圖譜，再完成底層卷冊草稿並補充聯想、演繹屬性；
5. 完成後續卷冊並更新圖譜；
6. 由 LLM 依證據解決語義衝突、合併或拆分，迭代受影響產物；
7. 通過完整性、對立候選、敏感度和紅隊審查後，交付逐條對照與時代示意地圖。

《山海經》第一版另強制卷六至十八的地理提及復用《五臧山經》節點；這是圖譜結構約束，不指定任何現實地理答案。詳見 [研究框架](docs/research-framework.md) 與 [山海經規格](projects/shanhaijing/docs/methodology-spec.md)。

## 原則

- **原文為準**：主文、注疏、異文分離；每個判斷可回到條目 ID 和逐字引文。
- **競爭假說**：不以今名、名氣或預設地區代替候選比較。
- **靜態形狀優先**：先比較輪廓、相對位置、連接、環繞、包含、分支與分佈；動態水流和現代流向不作硬性否決。
- **禁止因果倒置**：後世地名、注釋與現代分類不能反向解釋文本形成；按古代通用詞義理解描述。
- **承認歷史斷層**：傳播鏈缺失不是正反證，未知機制保持未知，不編造路線或動機。
- **文本與解釋分層**：文本事實、語義擬合、聯想和演繹屬性各有來源與狀態。
- **程序與 LLM 分工**：程序檢查、計算和發現衝突；LLM 負責語義裁決，人工覆核最高。
- **可重現**：原始快照有 SHA-256，工具輸出可重建，判斷有輸入雜湊與版本。

## 倉庫結構

| 路徑 | 內容 |
|---|---|
| [docs/](docs/README.md) | 方法、規格、架構、決策記錄與路線圖 |
| [reference/](reference/README.md) | 原始見證本、快照 manifest、結構化條目與乾淨文本 |
| [projects/shanhaijing/](projects/shanhaijing/README.md) | 山海經規格、本體、時代世界、派生資料與任務 |
| [tools/shj/](tools/shj) | 文本處理、路線分析與圖譜結構校驗工具 |
| [.claude/](.claude/) | 研究 agent 與 skill |

## 目前狀態

舊解釋草稿、舊地圖和舊圖譜已清除。文本層已重新生成；新知識圖譜、草稿、語義判斷和地圖待依框架 v4 建立。時代世界庫仍是種子資料，新版本尚未進行紅隊審查。

---

<a id="english"></a>
# Mythos — Seeking the Truths of the Universe in Ancient Texts, Myths and Legends

Mythos is an open research project that reads ancient texts, myths and legends as transmitted records which may preserve real observations. It compares rival interpretations against the world of the period with auditable, reproducible methods.

The first sub-project is the **Shanhaijing 《山海經》**, with a first-version period window of **4000–1000 BCE**. Every real-world correspondence is a competing hypothesis, never a predetermined answer.

The iterative v4 pipeline is: working text → entity extraction → geographic semantic-fit attributes → initial knowledge graph → base-section draft → enriched attributes → later sections and graph update → LLM conflict adjudication and merging → repeat until reviewed delivery. For the first SHJ version, geographic mentions in Books 6–18 must reuse nodes from the Five Mountain Classics; this constrains graph structure, not the real-world answer.

Every corpus follows the same judgment order: source evidence → static shape and physical features → ancient general semantics → period candidates → symmetric evaluation → confidence and unknowns. Later names and modern classifications cannot reverse causality; modern flow and missing transmission chains are not standalone vetoes, and unknown mechanisms remain unknown.

See the [research framework](docs/research-framework.md), [SHJ specification](projects/shanhaijing/docs/methodology-spec.md), and [current SHJ status](projects/shanhaijing/README.md).

## License

Code and documentation: Apache-2.0 ([LICENSE](LICENSE)). The ancient source texts are public domain. Wikisource transcriptions are CC BY-SA 4.0; see [reference/shanhaijing/README.md](reference/shanhaijing/README.md).
