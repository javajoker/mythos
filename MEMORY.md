# Mythos 核心記憶庫 / Project Memory

> 更新：2026-10-26
> 本文件只記錄已核驗狀態與下一步，不保存未經審查的地理結論。

## 1. 已確認的方法

- 框架 v4，時代窗口 **4000–1000 BCE**。
- 所有現實對應均為競爭假說；名稱遮蔽、對立候選、逐屬性證據與紅隊審查是必要條件。
- 基礎判斷邏輯（`docs/research-framework.md`）：靜態形狀優先／禁止因果倒置／古代通用詞義／文化斷層保持未知／統一推論順序／**名類判別**（ADJ-005：山名同名唯一，水名為性狀類名可多實例）。
- 里數以 **0.35–0.42 km/里** 為擬合區間（中值 0.385）。
- 黃河改道規則：河＝黃河中游穩定段錨定，下游改道不否決不鎖定。
- 卷六至十八地理提及復用山經節點或保持 `pending_anchor`；新實體標注 `new_entity`。
- 流程：工作文本 → 實體抽取 → 地理語義擬合 → KG v1 → 五臧草稿 → 屬性補充 → 後續經卷 → 圖譜更新 → LLM 衝突裁決 → 迭代交付。
- 程序做檢查與計算，LLM 做語義裁決；人工覆核高於 LLM，LLM 高於自動提議。衝突裁決配套級聯見 `.claude/skills/conflict-adjudication/SKILL.md`。

唯一權威規格：`docs/research-framework.md`、`projects/shanhaijing/docs/methodology-spec.md`、`projects/shanhaijing/docs/data-model.md`。

## 2. 已完成（截至 2026-10-26）

- 文本層：三見證本對勘、869 條目 working text、異文分類、路線抽取（447 站點）。
- 五臧山經 26 子經全量適配包（網格/映射/報告/逐句文檔/地圖五件套）＋分經概要圖 5＋五臧總體圖 1。
- KG v1：4,334 節點／4,618 提及／1,805 邊／9,234 屬性——山經地理映射（980/980 全覆蓋）＋人文風物讀法（2,606 節點）＋associative/deductive 566 條＋框架書 739 待定錨節點＋786 條框架書關係邊。`kg_validate.py` 通過。
- 卷六至十八 13 卷框架書適配三件套＋補丁地圖（復用 75／待錨 325／新增 408）。
- 全書概要圖（太平洋中心視圖：美洲在中原以東）。
- 草稿：`deliverables/draft-v1/`（結構版）＋ `deliverables/draft-v2/`（白話通順版，111 張本地實拍配圖，各卷嵌地圖）。
- 裁決在案：ADJ-002 昆侖虛＝撒哈拉之眼（吉薩合併否決）；ADJ-003 燭龍＝極晝極夜＋極光（章尾山 60–70°N）；ADJ-004 兩河空檔採納 F-0007；ADJ-005 名類判別原則。全部 `proposed_pending_review`。

## 3. 注意事項

- working text 的 base 讀法仍為 `unreviewed`；不得宣稱讀法已全部確認。
- 全部映射與裁決維持 `proposed_pending_review`，待項目發起人覆核。
- 2026-10-26 清理：舊「映射組」方案工具與產物（kg_mapping_build/kg_mapping_review/kg_water_registry/kg_export_geography 及其 era/、review/ 產物）已刪除；render_dongci/zhongci 一次性渲染器已刪除；xici 四圖已補 spec 遷移至通用渲染器。
- `review/` 僅存 `undirected-review.json`（kg_build 現役依賴）與 `semantic-referents.jsonl`（data-model 正式組件）。

## 4. 下一步

- 發起人覆核全部適配與裁決（ADJ-002–005）。
- 紅隊審查（devils-advocate）與交付評估。
- 山海經 web app（PRD/UI/UX/tech spec 文檔先行）。
- `sites.jsonl`／`palaeo-coast.json`（時代世界庫擴建，需要時）。
