---
name: framework-books
description: Runbook for adapting Shanhaijing Books 6–18 (海外/海內/大荒 framework books) — regional surveys that reuse the Five Mountain Classics geography, mark new entities, and produce per-book patch maps. Use when adapting any framework book (SHJ-06 … SHJ-18).
---

# 框架書（卷六至十八）適配 runbook

## 與山經的結構差異

卷六至十八不是里程鏈，是區域調查：以「海外自X陬至Y陬」等方位框架組織的國/族群/地標/神話記錄。**不展開站點網格**——以復用錨定＋區域指向取代里程算術。

## 基礎判斷約束（與山經一致）

靜態形狀優先／禁止因果倒置（後世命名不反證——堯舜禹葬地、朝鮮、會稽等一律借名標記）／古代通用詞義／文化斷層保持未知／統一推論順序。語義判斷全部由 LLM 產生；代碼只做結構化與覆蓋核對。**歷史演變優先：不以今果為因**；歷史缺失環節可用嚴謹假設補充推理鏈（須標明假設級別）。

## 復用規則（硬性）

1. 地理提及**優先復用五臧山經節點**：查 `era/adaptation/geo-reuse-index.jsonl`（981 行：node/名稱/候選/現代名/網格坐標/置信度）。復用必須給出對齊理由（同名＋方位＋屬性相容）。
2. 無法對齊的地理提及 → `pending_anchor`（待定錨），給方向性候選與理由；不得編造坐標。
3. 同名異實（如山經昆侖之丘 vs 海內西經昆侖虛）→ 記 `conflict`，兩假說並存，不在本層裁決。
4. 山經沒有的實體（國/族群/神話/風物）→ 標注 `new_entity`，給時代窗口記錄與讀法。

## 產出（每卷三件套＋補丁地圖）

置於 `projects/shanhaijing/data/derived/era/adaptation/`，slug＝`book06`…`book18`：

1. `<slug>-mappings.jsonl`：每條目地理提及的復用/待錨記錄——`{name, kind, node(复用時填山經節點id), entry, mapping_status, disposition: reuse|pending_anchor|new_entity, primary_candidate{name,region,fit}, confidence, conflicts, unknowns, review}`。人文風物新實體同格式（kind 用 POL/PER/CRE 等）。
2. `<slug>-sentence-analysis.md`：每條目四段式（原文／逐句全要素展開／時代映射表／4D 交叉驗證），與山經文檔同構；**額外實體在 §2 與 §3 標注「新增」**。
3. `specs/<slug>-map.json` → `<slug>-map.svg`：補丁地圖，用 `render_overview_map.py` 的 points 模式——`points[{name,lon,lat,color,note,status(mapped|region|pending_anchor),label_pos}]`；`chains` 可帶 `context:true` 疊加相關山經鏈（淺灰參照）。窗口按本卷實際範圍選；審計必須 `overflow: none`。

## 校驗

- mappings 逐行 json.loads；本卷全部地理提及（國/山/水/地標）在 mappings 有記錄（零遺漏）。
- 地圖渲染審計無越界＋瀏覽器目檢。
- 文明證據按需更新 `projects/shanhaijing/docs/civilization-coverage.md`。

## 圖譜入庫（適配完成後）

1. `tools/shj/kg_framework_build.py`：框架書實體入 KG——reuse 行＝提及掛山經節點＋framework_reference 屬性；pending_anchor/new_entity 行＝新節點（status=pending_anchor；非本體類型歸一並保留 original_kind）；mappings 全行入庫零遺漏。
2. 關係抽取（LLM）：每卷 `<slug>-edges.jsonl`（rises_at/flows_into/adjacent_to+bearing/located_in/produces/inhabits/worships/invented_by/same_entity_as/motif_of/related_to；動態流向保留原文於 quote；異文方位全建邊）；`tools/shj/kg_edges_build.py` 入庫（REL:FW 前綴，冪等）。
3. 新關係類型/層/域按開放式註冊先入 `data/kg-ontology.json`；`kg_validate.py` 必須通過。
4. 草稿重建：`tools/shj/draft_wuzang_build.py`——框架書 mapping 實體名在草稿中零遺漏（腳本核對）。
