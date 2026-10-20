---
name: shj-era-mapping
description: Runbook for the Shanhaijing (山海經) era-semantic mapping — the book as a record accumulated 4000–2000 BCE, read from the Central Plains origin, original text only, mapped by masked LLM semantic judgments onto the world of that period (its coasts, rivers, animals, civilisations and works such as Sumer, Harappa and Egypt, always with rivals), solved jointly for consistency, delivered item by item with a map of the period. Use for any Shanhaijing mapping request ("where is X", "regenerate the draft", "test this reading", "add a site or animal").
---

# 山海經時代語義對應 / Shanhaijing era-semantic mapping（規格 v3）

## 設定 / Settings（項目發起人，2026-10-20）
前 4000–前 2000 年逐步積累；原點中原；只用原文（明成化本），不用注疏；容許傳承錯誤；名稱語義保留、今名不比對；以大模型語義判斷為主、求解器保證一致；重點為兩河流域、哈拉帕、古埃及，並含其他同時期文明作為對立候選；試點為西山經四篇與大荒西經。

## 流程 / Pipeline（規格 §1）
```bash
python3 -I tools/shj/kg_extract.py        # 實體、關係、名稱語義（name_features：T-V03）
python3 -I tools/shj/era_frame.py         # 觀察框架：各篇路線與概況（T-V04）
python3 -I tools/shj/era_anchors.py       # 篇段錨點的報告與地圖（判斷紀錄 era/anchors.jsonl，T-V04b）
python3 -I tools/shj/era_tasks.py         # 遮蔽後的判斷任務（T-V06，待建）
#   → agent semantic-matcher：候選生成與語義評分 → data/derived/era/judgments.jsonl（T-V07）
python3 -I tools/shj/era_leakage.py       # 洩漏與誘餌（T-V08，待建）
python3 -I tools/shj/era_relations.py && python3 -I tools/shj/era_solve.py   # 關係與聯合求解（T-V09，待建）
python3 -I tools/shj/era_sensitivity.py && python3 -I tools/shj/era_sections.py   # 敏感度、假說組態（T-V10，待建）
python3 -I tools/shj/era_deliver.py       # 交付 draft-v4 與當時地圖（T-V11，待建）
```
時代世界庫 `data/era/` 由 agent `civilization-scout` 與 `palaeo-geographer` 建立（T-V05）。

## 回答「X 在哪裡」或「這個解讀成立嗎」/ Answering
1. 從全書的對應讀，不做單點搜尋；報告候選、年代、主要吻合維度與證據、可信度、對立候選。/ Read from the whole-book mapping.
2. 使用者提出的解讀寫成固定組態，與對立組態一起求解（`era_sections.py`）；不為了解讀改權重。/ Test readings as held configurations.
3. 新的解讀原則寫成一般規則（框架 §3.1），對所有候選一體適用。/ New principles become general rules.

## 檢查 / Checks
`projects/shanhaijing/docs/checklist.md` §6；紅隊紀錄 `projects/shanhaijing/docs/red-team.md`。
