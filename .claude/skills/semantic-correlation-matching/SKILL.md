---
name: semantic-correlation-matching
description: Generate masked rival candidates and judge period correspondences attribute by attribute with recorded evidence, samples, leakage probes, decoys and uncertainty.
---

# 語義相關評分 / Semantic correlation matching

## 統一推論順序

**原文證據 → 靜態形狀與物理特徵 → 古代通用詞義 → 同時代候選 → 相同寬容下的吻合與矛盾 → 可信度與未知項**。

靜態比較包括輪廓、相對位置、連接、環繞、包含、分支與分佈。動態出入只保留為原文線索，候選比較可降為無方向連接；現代水流、後世地名、傳播鏈缺失和現代狹窄分類不得越過此順序提前否決。未知傳播機制標為未知。

## 遮蔽輸入

將實體名稱換成代號，只保留原文描述、名稱特徵、關係摘要和必要的觀察框架。不提供注疏、既有比定或今名。

## 候選與評分

- 每個實體至少三個候選、至少兩個大區；包含真正的對立候選。
- 每個候選在時代窗口內存在或可見，附年代、狀態和一般性來源。
- 對外觀、顏色、尺度、材質、功能、聲音、生態、方位和年代逐項輸出 `score`、`contradiction`、`evidence`、`attribute`、`reason`。
- 無資料時記 `null`，不以缺失代替矛盾；今名相似與名氣不得分。
- 比例尺只在語料區間內擬合，並與其他模型比較敏感度。

## 全量水體映射

先由 LLM 為每個 WAT 節點建立真實世界候選並交項目發起人確認，再進行其他錨點校準。保留共享山體與跨山系錨定關係。每個水體均須比較改道、消亡、萎縮、沼澤化、人工渠道遺址和性狀改變；未知狀態標為未知，不得以現代水文直接否決。

## 取樣與紀錄

- 每個判斷至少三個樣本，每次打亂候選順序。
- 記錄 `model`、`prompt_version`、`input_hash`、`sample` 和候選卡版本；輸入不變不重判。
- 抽 10% 做不遮蔽洩漏探測；最佳候選改變或分數差異顯著時標記審查。
- 每批混入 5% 誘餌；高分配上熱門候選時交紅隊。
- 初始屬性寫 `semantic_fit/proposed`，經衝突與紅隊審查後才可接受。

輸出使用資料模型中的 `candidates.jsonl`、`judgments.jsonl`、`relation-judgments.jsonl` 和 `attributes.jsonl`，不由腳本生成理由或結論。
