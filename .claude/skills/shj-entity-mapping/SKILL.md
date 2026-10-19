---
name: shj-entity-mapping
description: Run, extend or audit the Shanhaijing (山海經) entity-graph pipeline end to end — extraction, world candidates, cross-validation and the item-by-item deliverable that maps every paragraph and every entity of the book to the real world. Use for any Shanhaijing mapping request ("where is X", "map the whole book", "regenerate the draft", "why is X mapped to Y", "add a river/animal to the base").
---

# 山海經實體對應 / Shanhaijing entity mapping

## 流程 / Pipeline
```bash
python3 -I tools/shj/kg_extract.py      # 步驟 1–2：實體、性質、關係、覆蓋檢查 → data/derived/kg/
python3 -I tools/shj/kg_candidates.py   # 步驟 3：全球候選 → kg/candidates.jsonl
python3 -I tools/shj/kg_crossval.py     # 步驟 4：交叉驗證、可信度 → kg/mapping.jsonl（約 11 分鐘）
python3 -I tools/shj/kg_sections.py     # 篇段掃描與聯合假說 → kg/sections/（約 1 小時）
python3 -I tools/shj/kg_sensitivity.py  # 權重敏感度 → kg/sensitivity/（約 30 分鐘）
python3 -I tools/shj/kg_deliver.py      # 步驟 5：逐段對照 → deliverables/draft-v3/（完整性不過就失敗）
```
文本層（只在見證本變動時重跑）：`fetch_sources.py` → `ingest.py` → `collate.py` → `align_witness.py` → `classify_variants.py` → `extract_routes.py`。

## 回答「X 在哪裡」/ Answering "where is X"
1. 在 `deliverables/draft-v3/entities.md` 找到 X 的所有節點（同名可能有數個）。
2. 報告對應、可信度、級別、權重穩健度、支持與違反的關係、其他候選及比例；暫定（< 0.1）要明說不可靠。可引用的標準：≥ 0.3 且權重變體 ≥ 14/16。
3. 若使用者提出特定假說（例：崑崙在埃及、西次三經 = 古埃及），把它寫成固定組態，加進 `kg_sections.py` 的組態清單，與對立組態一起計分；報告 ΔE、被違反的關係，以及篇段掃描中該地區的名次。不要為了假說改權重；若使用者提出新的解讀規則，寫成一般規則（framework §3.1）並對所有候選一體適用。

## 擴充 / Extending
- 新的真實世界條目：依 skill `world-candidate-generation`；新的抽取規則：依 `entity-graph-extraction`（重跑覆蓋檢查）；權重或求解器：依 `graph-cross-validation`（檢查確定性與單調性）。
- 每次修改後跑完整流程，交付的完整性檢查必須 PASS，再提交。
- 規格：`projects/shanhaijing/docs/methodology-spec.md`；資料模型：`data-model.md`；任務：`tasks.md`。
