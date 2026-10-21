# 架構 v4 / Architecture v4

> 2026-10-21 · 對應研究框架 v4 與山海經規格 v4。

## 1. 分層 / Layers

```text
reference/<corpus>/                 projects/<corpus>/
  sources/<witness>/  原始快照        data/era/               時代世界種子與卡片
  sources/manifest    快照雜湊        data/kg-ontology.json   語料專用本體（SHJ）
  data/entries        穩定條目         data/derived/
  text/               乾淨閱讀文本       working-text / collation / variants
                                      stations / sections / era judgments
                                      kg/ nodes·mentions·edges·attributes
                                    deliverables/draft-vN/  草稿與交付
                                    findings/               發現與 LLM 衝突日誌

tools/<corpus>/       可重現文本處理、結構校驗和計算
.claude/agents/       通用研究角色與子項目主持
.claude/skills/       可組合的操作規程
docs/                 公共方法與規範，不含語料專用固定答案
```

原文層不放解釋。文本事實圖與解釋圖使用同一實體 ID，但屬性以 `kind` 和 `status` 分層。衍生資料必須能回到工作文本、判斷或 LLM 裁決記錄。

所有層共用同一推論順序：原文 → 靜態形狀／物理特徵 → 古代通用詞義 → 同時代候選 → 對稱評估 → 可信度與未知項。`static.shape`、`static.topology` 記錄形狀與格局；動態 `flows_into` 保留原文方向，候選比較另用有來源的無方向 `connected_to`。後世地名、現代分類與傳播鏈缺失不得提前否決或鎖定答案。

## 2. 公共層與語料層 / Common versus corpus-specific

| 公共層 / Common | 語料專用層 / Corpus-specific |
|---|---|
| 見證本入庫、校勘、名稱語義、候選評分、關係驗證、紅隊 | 時代窗口、底層卷冊、實體句式、比例尺區間、第一版地理復用規則 |
| 判斷與裁決紀錄格式、可重現要求、實體與屬性分層原則 | `kg-ontology.json` 的類型適用規則、候選地區與時代世界庫 |
| 通用 agent 與 skill，不包含任何語料的現實對應答案 | `projects/shanhaijing/docs/methodology-spec.md` 與 `shj-era-mapping` runbook |

新增語料時，公共 agent/skill 不得需要修改；只新增語料規格、文本適配器、本體與時代世界設定。

## 3. 流程與職責 / Pipeline and ownership

| 階段 / Stage | 主責 / Lead | 支援 / Support | 產物 / Output |
|---|---|---|---|
| 工作文本 | `textual-critic` | `devils-advocate` | entries、working text、異文與移段記錄 |
| 實體抽取 | `entity-extractor` | `textual-critic` | nodes、mentions、textual edges |
| 時代世界 | `civilization-scout`、`palaeo-geographer` | `devils-advocate` | 有年代與來源的候選卡 |
| 地理語義擬合 | `semantic-matcher` | `cross-validator` | candidates、judgments、semantic-fit attributes |
| 初版圖譜 | `entity-extractor` | `cross-validator` | KG v1 與結構校驗結果 |
| 草稿與屬性補充 | `shj-lead` | `entity-extractor`、`semantic-matcher` | 底層卷草稿、associative/deductive attributes |
| 後續卷與圖譜更新 | `shj-lead`、`entity-extractor` | `semantic-matcher` | 後續卷草稿、復用與錨定關係 |
| 衝突解決與迭代 | `cross-validator` | `textual-critic`、`devils-advocate` | LLM 裁決、合併記錄、指定草稿修訂 |
| 交付與地圖 | `shj-lead` | `devils-advocate`、`palaeo-geographer` | 審查後的草稿、對照表與示意地圖 |

## 4. 現有工具 / Current tools

| 工具 / Tool | 職責 / Role |
|---|---|
| `fetch_sources.py` | 下載見證本；另可離線生成快照 manifest |
| `ingest.py` | 從 base 建立穩定條目、主文與注疏分欄 |
| `collate.py` | 見證本差異定位 |
| `align_witness.py` | 條目定位、明成化本次序與讀法狀態 |
| `classify_variants.py` | 異文分類提議與人工／LLM overrides |
| `extract_routes.py` | 從 working text 抽取山經站點、方向、里數與水系 |
| `era_frame.py` | 各篇獨立相對幾何、概況與里程差異報告 |
| `cn_numerals.py` | 中文數字解析 |
| `kg_validate.py` | 本體、schema、引用、類型及第一版地理約束校驗；只報告語義衝突 |

語義候選生成、判斷、合併與草稿推理由 agent 產生結構化記錄；不得以硬編碼腳本代替。後續需要的任務生成、求解、交付與地圖工具，須在相應資料契約可用後新增，不引用已刪除的舊工具名。

## 5. Agent 與 skill / Catalogue

- 主持：`shj-lead`；runbook：`shj-era-mapping`。
- 文本：`textual-critic`；`source-ingest`、`witness-collation`、`transmission-error-tolerance`。
- 實體與名稱：`entity-extractor`；`entity-graph-extraction`、`name-semantics`。
- 時代世界：`civilization-scout`、`palaeo-geographer`；`era-world-modelling`。
- 語義與框架：`semantic-matcher`；`semantic-correlation-matching`、`observer-frame`。
- 一致性與紅隊：`cross-validator`、`devils-advocate`；`graph-cross-validation`。

## 6. 可重現與語義裁決 / Reproducibility and adjudication

工具使用 Python 標準庫，從倉庫根目錄以 `python3 -I` 執行；支援 Python 3.9 以上。輸出排序並以快照和輸入雜湊確定。程序可做格式檢查、引用檢查、數值計算和衝突發現，但不得選擇語義答案。LLM 的裁決附證據、理由與版本；人工覆核高於 LLM，LLM 高於自動提議。
