# 規範 v4 / Conventions v4

## 1. 語言 / Languages

| 代碼 / Code | 語言 / Language | 用途 / Use |
|---|---|---|
| `zh-Hant` | 繁體中文 | 主要文檔語言；古籍引文保留原字形 |
| `en` | English | 國際協作 |

- 敘述型文檔（白皮書、PRD）每種語言一個檔案：`<name>.<lang>.md`。
- 規格型文檔採用段落級雙語，繁中在前；表格欄位雙語。工作記錄與衝突日誌可使用單語，但欄位名維持英文。
- Agent 與 skill 的名稱和 frontmatter 使用英文；操作規程可雙語。
- 新增語種時加入本表，並為白皮書和 PRD 建立對應語言版本。
- 古籍引文不轉簡體，也不統一異體。

## 2. 編號 / Identifiers

| 物件 / Object | 格式 / Format | 例 / Example |
|---|---|---|
| 條目 / Entry | `<CORPUS>-BB-S-EEE` | `SHJ-02-3-008` |
| 節點 / Node | `<TYPE>:<ENTRY>#<n>` | `MTN:SHJ-02-3-008#1` |
| 提及 / Mention | `MEN:<ENTRY>#<n>` | `MEN:SHJ-11-1-016#1` |
| 關係 / Edge | `REL:<ENTRY>#<n>` | `REL:SHJ-02-3-008#1` |
| 屬性 / Attribute | `ATT:<ENTRY>#<n>` | `ATT:SHJ-02-3-008#1` |
| 遮蔽代號 / Masked code | 類型首字母＋序號，只用於判斷任務 | `M-3`、`W-17` |
| 候選 / Candidate | `cand:<registry-id>`；無可行候選用 `cand:none` | `cand:region_001` |
| 判斷 / Judgment | `JDG:<stable-task-id>` | `JDG:W-17-sample-1` |
| 衝突 / Conflict | `CFT:<stable-subject-or-entry>` | `CFT:SHJ-11-1-016-1` |
| 發現 / Finding | `F-NNNN-<slug>` | `F-0001-base-text-modern-relocations` |
| 交付 / Deliverable | `deliverables/draft-vN/` | `deliverables/draft-v1/` |

- 節點名稱、異體、現代對應和坐標不得進入節點 ID。
- 同一 entry 中同類型實體按原文出現順序編 `#n`。
- 合併保留首發節點 ID；被合併節點標為 `merged`，所有提及保留。
- ID 的分配由程序做結構校驗；是否代表同一實體由 LLM 裁決。

## 3. 類型與狀態 / Types and statuses

實體類型：`MTN` 山、`WAT` 水、`LND` 地、`POL` 國族、`PER` 神人、`CRE` 生物、`PLA` 植物、`MIN` 礦物、`OBJ` 器物、`AST` 天象、`CLIM` 氣候、`UNK` 未定、`DOC` 文本結構。

- 地理類型：`MTN/WAT/LND`。
- 屬性種類：`textual`、`semantic_fit`、`associative`、`deductive`。
- 斷言狀態：`stated`、`proposed`、`accepted`、`contested`、`rejected`。
- 提及狀態：`linked`、`pending_anchor`、`unresolved`、`ignored`。
- 對應可信度：`high` ≥ 0.6、`medium` ≥ 0.3、`low` ≥ 0.1、`tentative` < 0.1；沒有足夠判斷時為空，不填 0 代替未知。

各類型可用的 predicate 和關係以 `projects/shanhaijing/data/kg-ontology.json` 為準。

## 4. 引用與證據 / Citation and evidence

- 文本證據使用條目 ID 加逐字引文；涉及移段時附明成化本位置。
- 注疏與現代編者內容只作轉錄或主張，不能冒充原文證據。
- 時代世界卡只用一般性考古、古地理和動物學資料，不引用對本書的既有詮釋。
- 推論順序固定為原文 → 靜態形狀與物理特徵 → 古代通用詞義 → 同時代候選 → 對稱評估 → 可信度與未知項。
- 動態關係保留原文方向；候選比較可用無方向 `connected_to`，現代水流不得單獨否決。
- 後世地名、注釋和現代分類不得反向解釋文本形成；詞義寬容對所有候選一致。
- 傳播鏈缺失不是正反證；未知機制標為未知，不編造接觸者、路線或動機。
- 每個語義判斷記錄模型、提示版本、樣本、輸入雜湊、證據與理由；輸入不變不重判。
- 人工覆核優先於 LLM，LLM 裁決優先於自動提議；所有優先級變更必須留痕。

## 5. 檔案與工具 / Files and tools

- 逐記錄資料用 JSONL、UTF-8、英文鍵；本體用 JSON；需要時另匯出 GraphML。
- 衍生資料由工具、結構化判斷或 LLM 裁決產生；不得手工改寫生成物而不更新來源。
- 工具使用 Python 標準庫，支援 Python 3.9 以上，從倉庫根目錄以 `python3 -I tools/<corpus>/<script>.py` 執行。
- 輸出前排序集合；相同輸入應產生逐位元組相同的檔案。
- 原始快照記錄路徑、大小與 SHA-256；下載和分析分離。

## 6. 提交 / Commits

- 每完成一項任務提交一次；一次提交只做一件事，訊息使用英文祈使句。
- 改動 `reference/` 或 `data/era/` 時說明來源與原因。
- 提交前刪除 `__pycache__`，不得提交本機雜項。
