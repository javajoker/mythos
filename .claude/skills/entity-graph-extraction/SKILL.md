---
name: entity-graph-extraction
description: Extract entities, mentions, name semantics and textual relations from working text into a typed, extensible graph while preserving unresolved states and separating textual from interpretive assertions.
---

# 實體與文本圖譜抽取 / Entity and text-graph extraction

## 輸入與順序

只從目前 working text 和語料 ontology 工作。先建立文本事實圖，再加入其他屬性層；不得從未校驗的解釋草稿反向製造原文實體。

## 步驟

1. 逐段識別每次實體提及，保存 entry、surface、逐字引文和出現順序。
2. 以 `TYPE:ENTRY#n` 建立首發節點，以 `MEN:ENTRY#n` 建立提及；名稱、異體與坐標不進入 ID。
3. 抽取名稱語義作為低權重特徵，按古代通用詞義理解，不以今名或現代狹窄分類決定實體。
4. 先抽取 `static.shape` 與 `static.topology`：輪廓、相對位置、連接、環繞、包含、分支和分佈。
5. 只把原文明示的發源、注入、相鄰、出產、棲居、祭祀、發明等關係寫入 `textual` layer；動態方向保留原文，候選比較另用有來源的無方向 `connected_to`。
6. 類型不明使用 `UNK`；未決提及使用 `unresolved` 或語料指定的 `pending_anchor`；忽略必須有理由。
7. 屬性分為 `textual`、`semantic_fit`、`associative`、`deductive`，每個 predicate 必須先在 ontology 註冊。
8. 合併與拆分不是字符串操作：程序發現候選衝突，LLM 依證據裁決並保留首發 ID 和全部提及。**合併節點必須引用裁決記錄（ADJ/F 項編號），無裁決記錄的合併一律回退。**
9. **否定句不生成實體節點**：「無水」「無草木」等否定記錄只作所在站的屬性，不得抽成獨立 WAT/PLA 節點（xici C13 教訓：「無水」被抽成 WAT 節點）。
10. **範疇檢查**：系譜人名不作地理水體——「赤水之子聽訞」一類「X 之子/之女」為 PER（妻族源地人格化），非 WAT；抽取時逐例檢查 PER/WAT 範疇，誤置者改類並撤水體復用。
11. 執行結構、引用、類型和覆蓋檢查，不能用自動補齊隱藏漏抽。
12. 全部水體必須有映射記錄。共享同一水體的山體及其關係 ID 保留為跨山語義錨點；不得由程序拆分、合併或指定現實位置。
13. **開放式屬性與關係**：所有識別、映射與讀法由 LLM 產生，KG 只負責結構化保存。新的屬性謂詞或關係類型按需擴展——先在本體（`data/kg-ontology.json` 或語料指定位置）註冊，再入庫；不得硬編碼封閉詞表，也不得為了遷就現有詞表而丟棄 LLM 讀法。人文風物資源（CRE/PLA/MIN/PER/OBJ/POL/CLIM/AST）的 LLM 識別讀法由 `kg_readings_build.py` 從逐句文檔 §2/§3 結構化入庫（`era.candidate` role=identification＋`era.state`），無結構可恢復者由 LLM 撰寫 `readings-supplement.jsonl` 補充——目標是全類型節點零遺漏。

輸出為 `nodes.jsonl`、`mentions.jsonl`、`edges.jsonl`、`attributes.jsonl`。語料專用的地理復用規則只從其規格與 ontology 讀取，不複製到公共 skill。
