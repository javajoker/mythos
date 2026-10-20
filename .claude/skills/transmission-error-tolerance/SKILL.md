---
name: transmission-error-tolerance
description: Score an ancient text that has been copied for millennia without letting losses and copying errors veto a match — absence is not contradiction, per-item penalties are capped, more agreement makes a reading stronger, and variant readings (graphic confusion, numeral corruption, displaced slips) are allowed only from witnesses or stated error types, at a small recorded cost. Use when a candidate fails on one detail, when numbers look wrong, or when deciding whether a mismatch is a copying error.
---

# 傳承錯誤的容許 / Tolerating transmission errors（框架 v3 P6、R11）

| 情況 / Case | 處理 / Treatment |
|---|---|
| 書中沒提到 / not mentioned | 不計分、不扣分 / no score, no penalty |
| 單項不符 / one item contradicts | 扣分，上限 0.5 / capped at 0.5 |
| 多項吻合 / many agree | 分數累加：吻合越多，越可信 / agreement accumulates |
| 形近字 / graphic confusion（已／己、千／十、日／曰）| 替代讀法，−0.1，須有見證本或明列的類型 |
| 數字訛誤 / numeral corruption | 只比較大小級別；替代數字須有見證本支持 |
| 錯簡 / displaced slips | 依工作文本（明成化本）的次序；已登記的錯簡可作替代 |
| 誇張 / exaggeration（「其高五千仞」）| 只取「很高」的級別 |

**不得**為了讓某個候選吻合而自創讀法；每一個替代讀法都寫入判斷紀錄的 `variant_reading`，紅隊可以逐條檢查。/ Never invent readings to fit; every variant is recorded.
