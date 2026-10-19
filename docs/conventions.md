# 規範 / Conventions

> v2.0 ・ 2026-10-19

## 1. 語言 / Languages

| 代碼 / Code | 語言 / Language | 用途 / Use | 加入原因 / Added because |
|---|---|---|---|
| `zh-Hant` | 繁體中文 / Traditional Chinese | 主要文檔語言之一；古籍引文保留原字形 / primary doc language; quotations keep source glyphs | 首個語料《山海經》/ first corpus |
| `en` | English | 主要文檔語言之一 / primary doc language | 國際協作 / international collaboration |

**規則 / Rules**
- 敘述型文檔（白皮書、PRD）每種語言一個檔案：`<name>.<lang>.md`。/ Narrative docs get one file per language.
- 規格型文檔（規格、清單、資料模型、任務、交付）採用段落級雙語，繁中在前、英文在後，表格欄位也雙語。/ Spec-type docs are bilingual paragraph by paragraph, zh-Hant first.
- Agent 與 skill 的說明與指令用英文；skill 的步驟可雙語。/ Agent and skill instructions in English; skill steps may be bilingual.
- 新增其他語種的古籍時（例如阿卡德語、古埃及語、梵語、古希臘語），在上表加入該語言，並為白皮書和 PRD 建立該語言版本。/ When a corpus in a new language is added, add it here and create that locale of the whitepaper and PRD.
- 古籍引文一律保留原字形，不轉簡體，也不統一異體。/ Quotations keep the source glyphs.

## 2. 編號 / Identifiers

| 物件 / Object | 格式 / Format | 例 / Example |
|---|---|---|
| 條目 / Entry | `<CORPUS>-BB-S-EEE` | `SHJ-02-3-006` |
| 實體 / Entity (KG node) | `<TYPE>:<符號 / symbol>`；同名不同篇的山加 `#<篇>`，同名異水加 `→<去向>`，無名生物用條目編號 / homonyms get `#section` or `→destination`; unnamed creatures use the entry ID | `MTN:昆侖之丘`, `WAT:洛→渭`, `CRE:SHJ-02-1-017#1` |
| 實體類型 / Entity type | `MTN` 山、`WAT` 水、`LND` 地、`POL` 國族、`CRE` 生物、`PLA` 植物、`MIN` 礦物、`PER` 神人、`UNK` 未定、`DOC` 結構 | — |
| 候選 / Candidate | `region:<code>`、`water:<id>`、`animal:<id>`、`culture:<id>`、`none` | `region:CHN`, `water:yellow` |
| 可信度級別 / Tier | `high` ≥ 0.6、`medium` ≥ 0.3、`low` ≥ 0.1、`tentative` < 0.1 | — |
| 對應狀態 / Status | `mapped`、`mapped:lexical`、`via-relations`、`unmapped:<reason>` | `unmapped:non-geographic` |
| 發現 / Finding | `F-NNNN-<slug>` | `F-0001-base-text-modern-relocations` |
| 任務 / Task | 文本層 `T-0nn`–`T-2nn`；方法步驟 `T-E`、`T-C`、`T-X`、`T-D`；紅隊 `T-R` / text layer, method steps, red team | `T-C03` |
| 交付版本 / Deliverable | `deliverables/draft-vN/` | `draft-v1` |

## 3. 引用 / Citation
- 文本：`` `SHJ-02-3-006` ``，並附上逐字引文「……」；若條目涉及移段，再附上明成化本的位置。/ Entry ID plus verbatim quote; add the Chenghua position for relocated entries.
- 真實世界庫的條目只用一般性的地理、動物學事實，不引用任何對本書的既有詮釋。/ World-base entries rely on general geographic and zoological facts, never on an existing interpretation of the book.
- 前人學說不作為證據，也不用來產生候選。/ Prior scholarship is never evidence and never used to generate candidates.

## 4. 檔案 / Files
- 資料用 JSONL、UTF-8，鍵名英文；知識圖譜另匯出 GraphML。/ JSONL, UTF-8, English keys; the KG is also exported as GraphML.
- 衍生資料與交付一律由 `tools/` 產生；人工判定放在 `ledgers/`，必須寫理由。/ Derived data and deliverables are tool-generated; human decisions go in `ledgers/` with reasons.
- 腳本以 `python3 -I tools/<corpus>/<script>.py` 從倉庫根目錄執行；輸出前排序所有集合。/ Run from the repo root; sort every set before output.

## 5. 提交 / Commits
- 每完成一項任務就提交；一次提交只做一件事；訊息用英文的祈使句。/ Commit each finished task; one concern per commit; imperative English subject.
- 改動 `reference/` 或 `data/world/` 時，必須說明來源和原因。/ Changes to `reference/` or `data/world/` state source and reason.
- 提交前刪除 `tools/<corpus>/__pycache__`。/ Remove `__pycache__` before committing.
