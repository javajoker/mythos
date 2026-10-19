---
name: shj-hypothesis-case
description: Run one Shanhaijing identification hypothesis (e.g. "崑崙 is X", "赤水 is Y", "文鰩魚 is a flying fish") end-to-end through stages S0–S9 and produce a dossier under projects/shanhaijing/hypotheses/H-NNNN/ that passes the checklist. Use whenever a user proposes, or asks to test, evaluate, verify, or debunk an interpretation of any Shanhaijing passage — even if phrased as a statement of fact ("赤水就是紅海") rather than a question.
---

# 山海經假說卷宗 / Shanhaijing hypothesis case

這是山海經對公共 skill `hypothesis-adjudication` 的專用包裝：補上山海經的條目編號、見證本、慣例和工具。
Shanhaijing wrapper around the common `hypothesis-adjudication` skill, adding entry IDs, witnesses, conventions and tools.

## 0. 先讀 / Read first
- `projects/shanhaijing/docs/methodology-spec.md`
- `projects/shanhaijing/docs/checklist.md`
- `projects/shanhaijing/hypotheses/TEMPLATE.md`，並參考範例 `H-0001/dossier.md` / and the worked example

## 1. 登記 / Register
1. 在 `hypotheses/README.md` 取下一個編號，建立 `H-NNNN/dossier.md`。/ take the next ID and create the dossier.
2. **核對引文**：在 `reference/shanhaijing/data/entries.jsonl` 找到每條引文，改為逐字原文；查 `projects/shanhaijing/data/derived/collation.jsonl` 中該條目的異文，以及 `docs/source-assessment.md` §3.1 的移段清單。/ **Check quotes** verbatim, then look up the entry's witness variants and the relocation list.
3. **範圍宣告**：對假說中每個地名或物名，用全文搜尋列出所有同名條目，包括異體寫法（昆侖、崑崙、崐崘；黑、黒）。/ **Scope**: list every same-name entry, including variant spellings.
4. 寫下預測和證偽條件、校改預算、慣例選擇，然後把狀態改為 `registered`。/ write predictions, falsifiers, budget and conventions, then set status to `registered`.

## 2. 檢驗 / Test
對每個預測，交給對應的專家（可以平行處理）：/ route each prediction to its specialist (in parallel where possible):

| 通道 / Channel | 交給 / Delegate to | 工具 / Tool |
|---|---|---|
| GEO, HYD（山經 / Mountain Classics） | `shj-route-reconstructor` | skill `shj-itinerary-reconstruction`, `tools/shj/chain_fit.py` |
| GEO, ETH（海經、大荒經的相對方位 / relative positions in the Sea & Wilderness classics） | `geo-triangulator` | skill `toponym-triangulation` |
| BIO | `naturalist` | skill `biogeo-identification` |
| 文本 / Text | `textual-critic` | skill `witness-collation` |

**全書基準率 / Corpus base rates**：對假說用到的每個文本特徵，用 `entries.jsonl` 統計它在全書出現的頻率，例如：
```bash
python3 -I -c "import json,re,sys; es=[json.loads(l) for l in open('reference/shanhaijing/data/entries.jsonl')]; p=re.compile(sys.argv[1]); print([e['id'] for e in es if p.search(e['text'])])" '人面[^，。]{0,3}虎身'
```

## 3. 裁決 / Adjudicate
- 合計 log₁₀ LR 並扣除校改成本，交給 `adjudicator` 依框架 §6 定級。/ sum log-LR minus emendation costs; `adjudicator` grades per framework §6.
- 交給 `devils-advocate` 做紅隊五項，結果寫入卷宗 §6。/ `devils-advocate` runs the five red-team checks.
- 寫出保留的觀察（任何框架都必須解釋的事實）、可登記的改寫和重測觸發條件。/ write retained observations, reformulations and re-test triggers.
- 更新 `hypotheses/README.md`；若有可發佈的結論，寫入 `findings/F-NNNN-*.md`；新任務加入 `docs/tasks.md`。/ update the registry, findings and tasks.

## 4. 語氣 / Tone
結論要直接，使用者自己的假說也不例外。否定的結論同樣是成果：寫清楚哪個通道、哪幾條原文造成否定，以及怎樣改寫才可能重新檢驗。
Be direct, including about the user's own hypothesis. A refutation is a result too: state which channel and which entries caused it, and how a reformulation could be re-tested.
