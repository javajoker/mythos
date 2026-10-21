# LLM 衝突裁決日誌 / LLM Conflict-resolution Log

## CFT-SHJ-01-2-015-order

- **狀態**：LLM proposed，待人工覆核。
- **衝突**：`working-text.jsonl` 將 `SHJ-01-2-015`（區吳之山）以 `partial` 對齊放入卷四，與 base 卷一南次二經順序衝突。
- **原文順序**：`SHJ-01-2-013` 洵山 → `014` 虖勺之山 → `015` 區吳之山 → `016` 鹿吳之山。
- **證據**：來源評估已確認明成化本卷一缺頁正好涵蓋 `SHJ-01-2-013` 至 `015`；卷四匹配由「又東五百里」等公式化文字造成，不能推翻卷一序列。
- **裁決**：採 `restore_base_sequence`，將 `SHJ-01-2-015` 置於 `SHJ-01-2-014` 之後。讀法仍保持 `unreviewed`，不改變任何文字。
- **執行**：記錄於 `ledgers/working-order-overrides.jsonl`，由 `align_witness.py` 可重現地應用。
- **影響**：五臧山經首、二、三、四按各自序列擴展，不因本次對齊偽影互相插入。
