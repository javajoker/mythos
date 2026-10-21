---
name: witness-collation
description: Collate independent witnesses, attribute differences to stable entries, detect relocations and establish working-text order and reading status without automatic semantic emendation.
---

# 見證本對勘 / Witness collation

## 原則

- base 提供穩定 ID，最早見證本決定工作文本次序；現代移段與補字只登記為候選。
- 未分類異文不得作為正式證據；自動分類只是提議。
- 對齊完成不等於讀法全部確認。
- 後世地名、注釋和地理歸類不得反向證明早期文本的所指或形成原因。

## 步驟

1. 取得至少兩個、最好三個獨立見證本，保存快照 manifest。
2. 去除標點與注文，只摺疊純字形異體；可能改變意義的字不得摺疊。
3. 以卷為單位對齊，將每個差異歸屬到穩定條目；保留缺頁和轉錄噪聲。
4. 用順序無關的定位找出移段，並以另一見證本交叉確認。
5. 將差異標為 `orthographic`、`displacement`、`transcription-gap`、`base-deviation`、`scribal-error`、`substantive` 或其他待審類型。
6. 自動結果寫 `decision_status: proposed`；LLM／人工裁決後寫 `decided`，優先級 human > llm > auto。
7. working text 記錄次序、`reading_source`、`reading_status` 和見證本定位。正式證據只使用已確認讀法。
8. 後續工具必須讀 working text，缺失時失敗，不得靜默退回 base。

山海經工具：`collate.py`、`align_witness.py`、`classify_variants.py`。移段發現見 `findings/F-0001-*`。
