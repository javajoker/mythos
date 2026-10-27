---
name: conflict-adjudication
description: Runbook for LLM conflict adjudication (衝突裁決) in the Shanhaijing project — every adjudication must cascade to mappings, sentence docs, maps (scroll/book/overview), KG, draft, and coverage table. Use when adjudicating any recorded conflict (F-xxxx references, competing hypotheses, same-name disputes).
---

# 衝突裁決 runbook（ADJ 系列）

## 裁決方法

LLM 依基礎判斷邏輯（`docs/research-framework.md`：靜態形狀優先／禁止因果倒置／古代通用詞義／文化斷層／統一推論順序／名類判別）裁決；列出競爭假說、證據鏈、綜合支持理由、張力項與遺留未知。裁決結果維持 `proposed_pending_review` 直至發起人覆核。

## 對稱性檢查（裁決前置，紅隊 G-6）

裁決文檔必附「對稱性檢查」一節：同一判據對主候選與對立候選的適用並列展示；不對稱適用必須給出理由，否則判據作廢。晚出層對主/對立候選一律不作定位證據、僅作流變註記；物種分布帶寬者屬非定位性證據（只可否決、不可釘點）；俗名/今名層不作證據。

## 置信度繼承（framework 發現 11＋zhongci E1）

復用/依賴節點的置信度 ≤ 被復用/被依賴節點；凡依賴 pending 錨的節點置信度自動封頂。裁決降級某錨時，沿依賴圖逐級回寫所有下游節點。

## 裁決執行五步閉環（framework 發現 1）

**裁決 → 受影響記錄清單 → 逐條回寫 → 計數覆核 → 對外陳述覆核**。對外陳述（coverage 頭條、任務表、交付措辭）與數據層不一致視為裁決未完成。

## 配套更新清單（每項裁決必做，缺一不可）

1. **裁決記錄**：`findings/adjudication-rec-NNN.md`（全證據鏈）＋ `findings/conflict-resolutions.md` 日誌條目。
2. **mappings**：受影響的 `*-mappings.jsonl` 行——primary_candidate/disposition/confidence/conflicts/unknowns 逐項更新；被否決假說保留在 conflicts 留檔（不刪除）。
3. **逐句文檔**：受影響條目插入裁決注記（ADJ-NNN 引用＋摘要）；不重寫原文展開。
4. **地圖**：受影響的 spec（子經 `specs/<slug>-map.json`／卷 `specs/bookNN-map.json`）改點位/注記 → 重渲 → 審計 `overflow: none`；概要圖（`*-overview.json`）若引用受影響點位則重建（`build_shanjing_overview.py` 後重渲）。
5. **KG**：`kg_framework_build.py`（框架書）或 `kg_v1_assemble.py`（山經）重建 → `kg_readings_build.py` → `kg_edges_build.py` → `kg_validate.py` 必須通過。
6. **草稿**：`draft_wuzang_build.py` 重建＋實體零遺漏核對。
7. **文明證據**：涉及文明/族群的裁決更新 `docs/civilization-coverage.md`。
8. **任務表**：`docs/tasks.md` 狀態按需更新。

## 提交

每項裁決的配套更新作一次提交，提交信息含 ADJ 編號與受影響範圍。

## 既有裁決登記

| ADJ | 對象 | 結論 |
|---|---|---|
| ADJ-002 | 昆侖虛 | ＝理查特構造（撒哈拉之眼）；吉薩合併說否決 |
| ADJ-003 | 章尾山燭龍 | ＝極晝極夜＋極光讀法；章尾山取 60–70°N 北方山系（上揚斯克—切爾斯基主候選）；與西三鍾山分立 |
| ADJ-004 | 兩河空檔 | F-0007 採納——體例性缺席，框架書待錨群承擔 |
| ADJ-005 | 名類判別 | 山名同名唯一／水名性狀類名（多實例合法）／實體五判據類判流程 |
