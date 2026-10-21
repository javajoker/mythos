---
name: shj-era-mapping
description: Runbook for the Shanhaijing v4 iterative pipeline from working text and entity extraction through semantic-fit graph, base and later drafts, LLM conflict adjudication and reviewed delivery.
---

# 《山海經》時代語義對應 runbook v4

本 skill 只負責編排，不複製方法細節。權威規格為：

- `docs/research-framework.md`
- `projects/shanhaijing/docs/methodology-spec.md`
- `projects/shanhaijing/docs/data-model.md`
- `projects/shanhaijing/data/kg-ontology.json`

## 執行順序

1. `textual-critic`：確認 working text 的次序與正式證據讀法。
2. `entity-extractor`：建立全書實體、提及、名稱語義和文本關係。
3. `civilization-scout`／`palaeo-geographer`：完成有年代、來源和對立候選的時代世界卡。
4. `semantic-matcher`：遮蔽生成競爭候選，形成地理語義擬合屬性與地標共識。
5. `entity-extractor`：組成 KG v1，運行 `kg_validate.py`。
6. `shj-lead`：重新生成五臧山經草稿，保留未決項。
7. `entity-extractor`／`semantic-matcher`：補充 associative 和 deductive 屬性。
8. `shj-lead`：重新生成卷六至十八草稿並更新圖譜。
9. `cross-validator`：由 LLM 解決語義衝突、合併或拆分，回寫指定記錄並迭代。
10. `devils-advocate`：獨立紅隊通過後，才交付 `deliverables/draft-v1/` 並評估地圖重建。

## 基礎判斷約束

每個階段均按「原文 → 靜態形狀／物理特徵 → 古代通用詞義 → 同時代候選 → 對稱評估 → 可信度與未知項」執行。後世地名、現代水流、傳播鏈缺失和獅虎等現代狹窄分類不得單獨否決；文化歷史機制未知時保持未知。

開羅／吉薩可作為崑崙之丘的競爭候選，但不是既定答案。其人工高台、陵寢格局、人面獸身造像與其他同時代物理特徵，必須與其他候選按同一規則比較。

## 第一版硬約束

只有卷一至五可新增 `MTN/WAT/LND` 節點。卷六至十八必須復用這些節點；無法對齊的提及保持 `pending_anchor`，由 LLM 裁決，不得由程序新增或指定節點。

此約束不指定任何現實地理答案。所有對應均為競爭假說，時代窗口為 4000–1000 BCE，比例尺在 0.35–0.42 km/里區間做敏感度分析。
