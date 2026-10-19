# 規範 / Conventions

## 1. 語言 / Languages

| 代碼 / Code | 語言 / Language | 用途 / Use | 加入原因 / Added because |
|---|---|---|---|
| `zh-Hant` | 繁體中文 / Traditional Chinese | 主要文檔語言之一；古籍引文保留原字形 / primary doc language; quotations keep source glyphs | 首個語料《山海經》/ first corpus |
| `en` | English | 主要文檔語言之一 / primary doc language | 國際協作 / international collaboration |

**規則 / Rules**
- 敘述型文檔（白皮書、PRD）每種語言一個檔案：`<name>.<lang>.md`。/ Narrative docs (whitepaper, PRD) get one file per language: `<name>.<lang>.md`.
- 規格型文檔（規格、清單、資料模型、卷宗）採用段落級雙語，繁中在前、英文在後，表格欄位也雙語。/ Spec-type docs (specs, checklists, data models, dossiers) are bilingual paragraph by paragraph (zh-Hant first, then en), with bilingual table columns.
- Agent 與 skill 的提示詞用英文（模型指令），使用者可見的範本用雙語。/ Agent and skill prompts are in English (model instructions); user-facing templates are bilingual.
- 新增其他語種的古籍時（例如阿卡德語、古埃及語、梵語、古希臘語），在上表加入該語言，並為白皮書和 PRD 建立該語言版本。/ When a corpus in a new language is added (e.g. Akkadian, Egyptian, Sanskrit, Greek), add it to the table and create that locale of the whitepaper and PRD.
- 古籍引文一律保留原字形，不轉簡體，也不統一異體。/ Quotations always keep the source glyphs: never convert to simplified, never normalise variants.

## 2. 編號 / Identifiers

| 物件 / Object | 格式 / Format | 例 / Example |
|---|---|---|
| 條目 / Entry | `<CORPUS>-BB-S-EEE` | `SHJ-02-3-006` |
| 假說 / Hypothesis | `H-NNNN`，外部學說用 `H-ext-NNNN` / external theories `H-ext-NNNN` | `H-0001` |
| 預測 / Prediction | `P<n>`（卷宗內 / within a dossier） | `P4` |
| 保留觀察 / Retained observation | `O-<n>` | `O-2` |
| 發現 / Finding | `F-NNNN-<slug>` | `F-0001-base-text-modern-relocations` |
| 任務 / Task | `T-<stage><nn>` | `T-610` |
| 錯誤類型 / Error type | 公共 `T0–T5`，山海經 `X1–X6` / common `T0–T5`, SHJ `X1–X6` | `X1` |

## 3. 引用 / Citation
- 文本：`` `SHJ-02-3-006` ``，並附上逐字引文「……」；若條目涉及移段，再附上明成化本的位置。/ Text: entry ID plus verbatim quote; add the Chenghua position for relocated entries.
- 外部事實：附來源（書目、資料庫及查詢日期、URL）；沒有來源的標為 `needs-citation`。/ External facts: cite the source (bibliography, database with query date, URL); otherwise tag `needs-citation`.
- 前人學說：只能出現在 `H-ext` 登記或「學術史」小節，不能出現在證據表中。/ Prior scholarship: only in `H-ext` registrations or a history-of-scholarship section, never in evidence tables.

## 4. 檔案 / Files
- 資料用 JSONL、UTF-8，鍵名英文。/ Data: JSONL, UTF-8, English keys.
- 衍生資料一律可以由 `tools/` 重新產生；手工產出放在卷宗或帳簿中，不放在 `data/derived/`。/ Derived data must be regenerable from `tools/`; hand-made outputs go in dossiers or ledgers, not `data/derived/`.
- 腳本以 `python3 -I tools/<corpus>/<script>.py` 從倉庫根目錄執行。/ Run scripts from the repo root as `python3 -I tools/<corpus>/<script>.py`.

## 5. 提交 / Commits
- 一次提交只做一件事；訊息用英文的祈使句，必要時附中文說明。/ One concern per commit; imperative English subject, Chinese body if helpful.
- 改動 `reference/` 時，必須說明來源和原因。/ Changes to `reference/` must state source and reason.
