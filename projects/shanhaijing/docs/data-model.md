# 山海經資料模型 v4 / SHJ Data Model v4

所有資料使用 UTF-8；逐記錄資料使用 JSONL，機器可讀本體使用 JSON。欄位名使用英文，原文保留原字形。機器可讀約束見 `data/kg-ontology.json`，結構校驗使用 `tools/shj/kg_validate.py`。

## 1. 原文與工作文本 / Source and working text

| 檔案 / File | 內容 / Content |
|---|---|
| `reference/shanhaijing/sources/manifest.json` | 原始快照的路徑、位元組數與 SHA-256 |
| `reference/shanhaijing/data/entries.jsonl` | 以現代 base 建立的穩定條目 ID、主文、注疏、異文與編輯參照；不是最終工作讀法 |
| `data/derived/working-text.jsonl` | 明成化本次序的條目序列，含 `reading_source`、`reading_status` 和見證本定位；只有已確認讀法可作正式證據 |
| `data/derived/collation.jsonl` | 見證本差異候選 |
| `data/derived/witness-alignment.jsonl` | 每個 base 條目在兩個見證本中的定位 |
| `data/derived/displacements.jsonl` | 移段候選與見證支持 |
| `data/derived/variant-classes.jsonl` | 自動提議或人工／LLM 裁決的異文分類與審核狀態 |
| `data/derived/stations.jsonl`、`sections.jsonl` | 從 working text 抽取的山經站點、方位、里數與篇末總數 |

注疏只為完整轉錄而保存，不進入原文事實圖或語義評分輸入。

## 2. 知識圖譜檔案 / Knowledge-graph files

圖譜位於 `projects/shanhaijing/data/derived/kg/`：

| 檔案 / File | 內容 / Content |
|---|---|
| `nodes.jsonl` | 首發實體節點；名稱與坐標不進入 ID |
| `mentions.jsonl` | 每一次原文提及；可指向節點或處於 `pending_anchor` |
| `edges.jsonl` | 文本事實關係或解釋關係 |
| `attributes.jsonl` | 可擴展的屬性斷言，區分文本、語義擬合、聯想與演繹 |

### 2.1 節點 `nodes.jsonl`

```json
{"id":"MTN:SHJ-02-3-008#1","type":"MTN","canonical_name":"昆侖之丘","first_entry":"SHJ-02-3-008","names":[{"value":"崑崙之丘","entry":"SHJ-16-1-037"}],"status":"active"}
```

必要欄位：`id`、`type`、`canonical_name`、`first_entry`、`names`、`status`。地理節點在第一版只能以卷一至五的條目作 `first_entry`；後續卷復用透過提及與關係表達，不複製節點。

### 2.2 提及 `mentions.jsonl`

```json
{"id":"MEN:SHJ-11-1-016#1","entry":"SHJ-11-1-016","surface":"昆侖之虛","type":"MTN","node":null,"status":"pending_anchor","quote":"海內西經……"}
```

- `node` 為有效節點 ID，或在第一版後續卷地理提及中為 `null`。
- `status`：`linked`、`pending_anchor`、`unresolved`、`ignored`；`ignored` 必須有理由。
- 一個段落可有多個提及；完整性以原文實體提及數與提及記錄數比較，不以段落是否有節點代替。

### 2.3 關係 `edges.jsonl`

```json
{"id":"REL:SHJ-02-3-008#1","src":"WAT:SHJ-02-3-008#2","dst":"WAT:SHJ-02-3-008#3","type":"flows_into","layer":"textual","entry":"SHJ-02-3-008","quote":"赤水出焉……","status":"stated"}
```

- `layer`：`textual` 或 `interpretive`。
- `type`、`src/dst` 類型與 `layer` 必須符合 ontology。
- 解釋關係另附 `decision` 或 `judgment` 來源，不得只寫模型結論。

### 2.4 屬性 `attributes.jsonl`

```json
{"id":"ATT:SHJ-02-3-008#1","subject":"MTN:SHJ-02-3-008#1","predicate":"era.candidate","value":{"candidate":"cand:example"},"kind":"semantic_fit","status":"proposed","confidence":null,"evidence":[{"entry":"SHJ-02-3-008","quote":"……"}],"provenance":{"judgment":"JDG:example"}}
```

必要欄位：`id`、`subject`、`predicate`、`value`、`kind`、`status`、`evidence`、`provenance`。

- `kind`：`textual`、`semantic_fit`、`associative`、`deductive`。
- `status`：`stated`、`proposed`、`accepted`、`contested`、`rejected`。
- predicate 的適用實體類型和值類型由 ontology 定義；新增語義先註冊新 predicate，不建立無定義的自由欄位。
- 值格式：`geo_point` 為 `{"lat": 25.5, "lon": 111.5}`；`year_range` 為 `[from, to]` 兩個整數年，BCE 為負且 `from <= to`；`geometry` 為含 `type` 與 `coordinates` 的 GeoJSON 類物件；`object` 為 JSON 物件；`string` 為字串；`any` 可為任何 JSON 值。
- `confidence` 可為空；沒有判斷記錄時不得填入確定數值或把 `proposed` 改為 `accepted`。

## 3. 時代語義判斷 / Era and semantic judgments

位於 `projects/shanhaijing/data/derived/era/`：

| 檔案 / File | 必要內容 / Required content |
|---|---|
| `candidates.jsonl` | 實體、候選、年代、當時狀態、物理屬性、一般性來源與對立候選組 |
| `judgments.jsonl` | 遮蔽輸入雜湊、模型、提示版本、樣本、逐維分數、證據與理由 |
| `relation-judgments.jsonl` | 兩個候選之間的關係是否成立、證據、樣本與理由 |
| `anchors.jsonl` | 地標候選、支持條目、共同關係、共識狀態與反推的觀察原點 |
| `mapping.jsonl` | 目前有效的對應、狀態、可信度、對立候選、支持與違反關係 |

每個實體至少三個候選、至少兩個大區；沒有對立候選的結果只能保留為未決，不得標為接受。

## 4. LLM 衝突與合併 / LLM conflict decisions

`data/derived/kg/conflict-decisions.jsonl`：

```json
{"conflict":"CFT:example","subjects":["MTN:SHJ-02-3-008#1"],"predicate":"era.candidate","decision":"unresolved","rationale":"……","evidence":[{"entry":"SHJ-02-3-008","quote":"……"}],"decided_by":"llm","model":"……","prompt_version":"……","input_hash":"……","review_status":"pending","updates":[]}
```

- `decision`：`merge`、`split`、`accept_variant`、`keep_both`、`revise`、`unresolved`。
- 合併保留首發節點 ID，其他節點標為 `merged`；不得刪除歷史提及。
- 人工覆核高於 LLM，LLM 高於自動提議。程序只驗證並執行 `updates`，不生成語義理由。
- 人可讀日誌為 `projects/shanhaijing/findings/conflict-resolutions.md`。

## 5. 類型與擴展 / Types and extensibility

實體類型：`MTN`、`WAT`、`LND`、`POL`、`PER`、`CRE`、`PLA`、`MIN`、`OBJ`、`AST`、`CLIM`、`UNK`、`DOC`。

- 地理類型：`MTN/WAT/LND`。
- 人文與物產：`POL/PER/CRE/PLA/MIN/OBJ`。
- 天象與氣候：`AST/CLIM`。
- `UNK` 用於尚未完成語義分類的實體，不是刪除或忽略的理由；`DOC` 只用於文本結構。

每種類型允許的 predicate、關係 domain/range 和 layer 由 `kg-ontology.json` 決定。該檔案是擴展語義的唯一入口，agent、skill 和工具不得各自維護不同詞表。
