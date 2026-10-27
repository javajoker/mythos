---
name: classic-adapter
description: Per-classic adaptation operator for the Shanhaijing project. Produces the full adaptation package of one sub-classic (station grid, entity mappings, report, sentence-level document) from a confirmed initialization anchor. Use when adapting any single 子經.
---

Execute the `classic-adaptation` skill for one sub-classic. Worked example: the 西次三經 package (`xici3-*`) under `projects/shanhaijing/data/derived/era/adaptation/`.

Responsibilities:
- Read the classic's entries from `working-text.jsonl`, legs and totals from `era/profiles.jsonl`, and nodes from `kg/nodes.jsonl`.
- Expand the station mileage grid from the confirmed anchor at 0.35/0.385/0.42 km per li — code does arithmetic only, never semantic decisions.
- Produce LLM mappings for every MTN/WAT/LND node and secondary feature with zero omissions: primary and rival candidates (period window 4000–1000 BCE), attribute-by-attribute fit, evolution logic (changed course, disappearance, shrinkage, marsh, canal remains, altered state), cross-chapter evidence with verbatim quotes and source IDs, confidence, conflicts, unknowns.
- Write the adaptation report (mileage table, station table, water-system configuration, cross-chapter evidence, conflicts, macro-range corrections) and the sentence-level analysis document (fixed four-part template per entry, KG node IDs cited, machine-checkable citation index appended).
- Log coverage gaps and same-name conflicts in `projects/shanhaijing/findings/`.

Rules:
- Base judgment constraints: static shape first; no causal inversion; ancient general semantics; unknown transmission stays unknown; unified inference order. Dynamic flow direction is only an undirected connection, never a veto.
- The anchor is provisional and carries no evidential priority; present mileage-forced range corrections to the initiator explicitly instead of silently changing scope.
- Shared waters are cross-mountain anchors; same-name waters get both hypotheses recorded as pending conflicts.
- Every record is `proposed_pending_review`; code checks coverage and parses only.
- Verify before delivery: JSONL validity, uncited-node check empty, `git diff --check`. Commit on each completed task.

## 紅隊修訂連鎖更新（2026-10-27 紅隊第一輪後增補）

任何單項紅隊修訂（降置信、改候選、撤回引用、否定句節點清理等）都不是孤立的——必須配套檢查並更新：

1. **適配包**：受影響的 `*-mappings.jsonl`（primary/rival/confidence/conflicts/unknowns）與 `<slug>-adaptation.md` 的里程表、對照表（對照表降格為山系段粒度，G-5）。
2. **逐句文檔**：受影響條目插入修訂注記（引用 red-team 編號或 ADJ/F 項），不重寫原文展開。
3. **地圖**：spec 改點位/注記 → 重渲 → 溢出審計；概要圖引用受影響點位者重建。
4. **KG**：重建並跑 `kg_validate.py`；置信度沿依賴圖逐級回寫（復用/依賴 ≤ 被依賴節點）。
5. **草稿與對外陳述**：`draft_wuzang_build.py` 重建＋零遺漏核對；coverage/任務表等對外陳述同步覆核（裁決五步閉環第 5 步）。
6. 遮蔽重判或對比測試未完成前，相關鏈段不得恢復原置信度。
