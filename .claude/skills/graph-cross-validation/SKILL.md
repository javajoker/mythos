---
name: graph-cross-validation
description: Test graph and candidate consistency across text, topology, scale, archaeology and period ecology, then obtain evidence-backed LLM decisions for semantic conflicts.
---

# 圖譜交叉驗證與衝突裁決 / Graph cross-validation

## 檢查維度

1. **文本與抽取**：逐字引文、讀法狀態、提及覆蓋、比喻與關係偽影。
2. **空間與水文**：發源、注入、相鄰、相對幾何、跨篇連接證據與未錨定項。
3. **距離與比例尺**：在語料允許區間做敏感度，不把單一數值吻合當證明。
4. **考古與年代**：候選及相鄰候選的存在年代、當時形態與遺跡狀態。
5. **古環境與生態**：氣候、水文、動植物分佈是否支持或反對組態。
6. **對立組態**：固定一組假說後重解其餘部分，與競爭組態比較，而非只挑單段吻合。

## 衝突處理

程序只負責 schema、引用、數值、覆蓋和衝突發現。LLM 裁決必須：

1. 列出衝突實體、屬性、原文、候選值和對立解釋。
2. 檢查至少一項反向證據或競爭候選。
3. 選擇 `merge`、`split`、`accept_variant`、`keep_both`、`revise` 或 `unresolved`，並附理由。
4. 記錄模型、提示版本、輸入雜湊、審核狀態和精確更新範圍。
5. 回寫受影響圖譜與指定草稿，重跑相關校驗；不得用程序啟發式自動選答案。

人工覆核高於 LLM。所有裁決寫入機器可讀記錄與 `findings/conflict-resolutions.md`。
