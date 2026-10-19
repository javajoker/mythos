---
name: hypothesis-adjudication
description: Corpus-agnostic procedure for registering, scoring and grading an interpretation of an ancient text, myth or legend under the Mythos research framework — pre-registration, evidence channels, E-grades with comparison sets, log-likelihood-ratio tally, correction budget, red team, and verdict levels R/L0–L4. Use whenever any Mythos sub-project needs to evaluate a claim like "place X in the text is real place Y", "creature X is species Y", or "event X records phenomenon Y", or when auditing an existing dossier.
---

# 假說裁決 / Hypothesis adjudication

規範來源 / Normative source: `docs/research-framework.md`。子項目會提供自己的包裝 skill（例如 `shj-hypothesis-case`），補上條目編號、見證本、慣例和工具。/ Sub-projects wrap this skill (e.g. `shj-hypothesis-case`) with their IDs, witnesses, conventions and tools.

## 1. 登記 / Register (before any testing)
- 假說原文、逐字引文（含條目編號和見證本）/ hypothesis as stated; verbatim quotes with entry IDs and witnesses
- 範圍：所有同名或同物條目 / scope: every same-name entry
- 預測與證偽條件的表格 / predictions and falsifiers table
- 校改預算（預設 log₁₀ −1.5）和慣例選擇 / correction budget and conventions

## 2. 證據項 / Evidence items
每一項都必須包含以下欄位。/ Each item must have:

| 欄位 / Field | 規則 / Rule |
|---|---|
| channel | GEO HYD TER BIO MIN CLI ETH XCP ARC 之一；同一個觀察只能計一次 / exactly one; an observation counts once |
| entries + quote | 逐字原文 / verbatim |
| external fact | 附來源，否則標 `needs-citation`，並記 LR = 1 / cited, else LR = 1 |
| comparison set | 「若 H 不成立，還有什麼也會產生這個觀察」/ what else would produce this if H were false |
| grade | E−3 … E4（框架 §4）/ framework §4 |
| log₁₀ LR | 取該等級區間內的值；同通道內相關的項目，第二項起折半 / within the grade's bin; correlated items in one channel discounted 50% after the first |

**基準率**：文本特徵要先在全語料中統計頻率；頻率越高，獨特性越低。/ **Base rate**: count textual features across the whole corpus first; the more common, the less distinctive.

## 3. 合計與定級 / Tally & grade
合計值 = Σ 各通道 log₁₀ LR + Σ 校改成本。/ total = Σ channel log₁₀ LR + Σ emendation costs.
- 任一 E−3，或者合計 < −2 → R / any E−3 or total < −2 → R
- 合計在 −2 到 0 之間，或只有單一通道 → L0 / total in [−2, 0] or single channel → L0
- 合計 > 0，且至少兩個通道為正 → L1 / total > 0 with ≥ 2 positive channels → L1
- 合計 > 1，至少三個獨立通道為正，無 ≤ E−2 的項目，且未超預算 → L2 / total > 1, ≥ 3 independent positive channels, nothing ≤ E−2, within budget → L2
- 合計 > 2，並通過紅隊和敏感度分析 → L3 / total > 2 and passes red team and sensitivity → L3
- L3 加上事先登記、隨後證實的新預測 → L4 / L3 plus a confirmed pre-registered novel prediction → L4
- 超出校改預算 → 上限 L1 / over budget → capped at L1

## 4. 紅隊 / Red team (delegate to `devils-advocate`)
反例搜尋 → 替身測試 → 基準率審查 → 校改審查 → 敏感度分析。/ Counter-examples → decoy → base-rate audit → emendation audit → sensitivity.

## 5. 收尾 / Close-out
保留的觀察、可登記的改寫、重測觸發條件；更新登記冊。/ Retained observations, reformulations, re-test triggers; update the registry.
