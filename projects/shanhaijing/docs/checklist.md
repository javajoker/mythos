# 山海經研究檢查清單 / Shanhaijing Research Checklist

> 每份卷宗在進入 `adjudicated` 之前，必須逐項勾選。agent `adjudicator` 會依本清單審查。
> Every dossier must tick each item before it can become `adjudicated`. The `adjudicator` agent audits against this list.

## G1 原文 / Text (S0–S1)
- [ ] 每條引文都附條目編號，並且與 `entries.jsonl` 逐字相符 / every quote has an entry ID and matches `entries.jsonl` verbatim
- [ ] 已查核三個見證本的異文；被引用條目中的異文都已分類 / the three witnesses were checked; every variant in a cited entry is classified
- [ ] 若條目受到底本移段影響（見 [source-assessment](source-assessment.md)），已改用明成化本的順序 / if the entry is affected by base-text relocation, the Chenghua order is used

## G2 不繼承結論 / No inherited conclusions
- [ ] 沒有把注疏或前人比定當作證據 / no commentary or prior identification used as evidence
- [ ] 候選生成在查閱任何 `H-ext` 之前完成，並且留有紀錄 / candidate generation was done before consulting any `H-ext`, and logged

## G3 預先登記 / Pre-registration
- [ ] 預測、證偽條件、校改預算和慣例選擇，都在檢驗前寫入 / predictions, falsifiers, budget and conventions written before testing
- [ ] 範圍宣告完整，同名條目全部列出 / scope declared; all same-name entries listed

## G4 證據 / Evidence
- [ ] 每項證據都標明一個通道，沒有重複計分 / each item has exactly one channel, nothing double-counted
- [ ] 每項 E2 以上的證據都寫出了對照集 / every item graded E2 or above names its comparison set
- [ ] 文本中的特徵已做全書基準率統計（例如生物描述、通名）/ corpus base rates computed for textual features (creature descriptions, generic terms)
- [ ] 外部事實都附來源，否則標為 `needs-citation` 並記 LR = 1 / external facts cited, or tagged `needs-citation` with LR = 1
- [ ] 同一通道內相關的證據已折減 / correlated items in one channel discounted

## G5 交叉定位 / Triangulation
- [ ] 至少檢驗了 3 個通道 / at least 3 channels tested
- [ ] 鏈條擬合使用規格 §6.3 的誤差模型，種子固定，產出檔案已存入卷宗目錄 / chain fits use the §6.3 error model with a fixed seed, outputs saved in the dossier folder
- [ ] 水系假說已做拓撲檢查（出、注、潛、流向）/ hydrology topology checked (source, mouth, sinking, direction)
- [ ] 生物假說列出了至少 3 個候選分類群，並檢查了棲地一致性 / ≥ 3 candidate taxa listed, habitat consistency checked
- [ ] 年代與古環境已明確說明（規格 §7.8）/ date and palaeo-environment stated (spec §7.8)

## G6 錯誤與校改 / Errors & emendations
- [ ] 每次校改都標明類型（T0–T5 / X1–X6）和成本 / every emendation typed (T0–T5 / X1–X6) and costed
- [ ] 總成本未超出預算，否則等級上限為 L1 / within budget, or verdict capped at L1

## G7 對立假說 / Competing hypotheses
- [ ] 至少 2 個實質對立假說和 1 個虛無假說，並且用相同標準檢驗（或已排入任務）/ ≥ 2 rivals + null tested by the same standard (or scheduled as tasks)

## G8 紅隊 / Red team
- [ ] 五項都已完成：反例、替身、基準率、校改、敏感度 / all five done: counter-examples, decoy, base rate, emendations, sensitivity

## G9 裁決與發佈 / Verdict & publication
- [ ] 等級依框架 §6 的門檻判定 / grade follows framework §6 thresholds
- [ ] 列出了保留的觀察和重測觸發條件 / retained observations and re-test triggers listed
- [ ] 已更新登記冊（`hypotheses/README.md`）；若形成發現，已寫入 `findings/` / registry updated; findings written if any
