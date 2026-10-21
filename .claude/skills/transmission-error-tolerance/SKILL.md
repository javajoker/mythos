---
name: transmission-error-tolerance
description: Handle missing details and possible copying errors without allowing unlimited fitting. Variant readings require evidence and LLM or human adjudication; code only reports candidates.
---

# 傳承錯誤的容許 / Transmission-error tolerance

| 情況 / Case | 處理 / Treatment |
|---|---|
| 原文未提 | 不計分、不扣分，也不自動視為矛盾 |
| 單項不符 | 記錄矛盾與影響，納入整體候選比較，不能隱藏 |
| 多項吻合 | 只在獨立特徵與關係上累積支持，避免重複計算同一證據 |
| 形近字 | 形成替代讀法候選，須有見證本或明確錯誤類型 |
| 數字差異 | 保留各見證本讀數與分段合計，做級別與敏感度比較 |
| 錯簡 | 以最早見證本次序為工作次序，其他排法只作移段假說 |
| 誇張 | 可降為大小級別，但必須標明轉換規則並對所有候選一致 |

程序可以發現差異、計算合計和報告異常，不能決定哪個讀法正確。LLM 或人工裁決必須記錄證據、理由、錯誤類型、審核狀態與受影響產物；人工覆核高於 LLM。

不得為遷就候選自創讀法，也不得把容錯變成任何候選都能通過的免責規則。古代通用詞義、觀察替代和類別泛化必須對所有候選一致適用。

文化與歷史可能斷層：傳播鏈缺失既不是反證也不是正證。未知機制標為未知，不編造接觸者、路線或動機。
