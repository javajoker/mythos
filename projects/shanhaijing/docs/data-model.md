# 資料模型 / Data Model

所有資料都用 JSONL（每行一筆），UTF-8，鍵名用英文，值保留原文。
All data is JSONL (one record per line), UTF-8, English keys, source-language values.

## 1. 條目 Entry — `reference/shanhaijing/data/entries.jsonl`

| 鍵 / Key | 型別 / Type | 說明 / Description |
|---|---|---|
| `id` | str | `SHJ-BB-S-EEE`：BB 為卷 01–18，S 為卷內篇次，EEE 為篇內段次 / book, section, paragraph |
| `book_no`, `book`, `book_en` | int, str, str | 卷號、卷名、英譯 / book number, name, English |
| `layer` | str | 山經 / 海外經 / 海內經(四篇) / 大荒經 / 海內經 |
| `section_no`, `section` | int, str | 篇次與篇名（例如「西次三經」）/ section number and name |
| `para_no` | int | 篇內段次 / paragraph in section |
| `text` | str | 主文（去注，保留標點；異文取主讀）/ main text (no notes, punctuation kept, main reading) |
| `notes[]` | `{at, text}` | 夾注，`at` 為在 `text` 中的位置 / interlinear notes with offset |
| `variants[]` | `{at, main, alt, kind}` | 異文；`kind` = reading / note |
| `editorial_refs[]` | `{at, text}` | 現代編者註（只作為「主張」）/ modern editorial notes (claims only) |
| `source` | str | 來源頁 / source page |

## 2. 站點 Station — `projects/shanhaijing/data/derived/stations.jsonl`

| 鍵 / Key | 說明 / Description |
|---|---|
| `entry_id`, `book`, `section`, `seq` | 出處與篇內序號 / provenance and order in section |
| `bearing`, `bearing_deg` | 由上一站出發的方位（八方位）/ bearing from the previous station |
| `leg_raw`, `leg_parts[]`, `leg_li` | 里程原文、分段（`mode`: 陸行(默認) / 水行 / 流沙 / 山行）、合計 / raw distance, parts, total |
| `name`, `start` | 山名；是否為篇首 / name; section start |
| `complex_leg` | 是否為多段或非陸行 / multi-part or non-land leg |
| `rivers[]` | `{river, where, flow, to}`：發源處、流向、匯入處 / source, direction, destination |
| `creatures[]` | `{kind, desc, name}`：獸、鳥、魚、蛇、木、草、神、人 / beast, bird, fish, snake, tree, plant, god, person |

## 3. 篇段 Section — `sections.jsonl`
`{entry_id, book, section, stated_mountains, stated_li, text}`：篇末的「凡N山，N里」/ the section's own stated totals.

## 4. 異文 Collation — `collation.jsonl` → `variant-classes.jsonl`
`collation.jsonl`：`{entry_id, witness: sbck|skqs, op: replace|insert|delete, base, witness_text, context}`（機器對勘，可隨時重新產生 / regenerable）。

`variant-classes.jsonl`（`tools/shj/classify_variants.py`）在每筆上加 `key`、`status`、`reason`、`classifier`。/ adds `key`, `status`, `reason`, `classifier` to each difference.

| status | 意義 / Meaning | 誰判定 / Who |
|---|---|---|
| `orthographic` | 純字形異體，或古今字、通假（`reason` 註明）/ glyph variant, or 古今字/通假 (noted in `reason`) | auto |
| `base-deviation` | 底本與**兩個**早期見證本都不同，而兩見證本一致；可能是底本誤字或現代校改。工作文本從見證本 / base differs from **both** early witnesses, which agree; base typo or modern emendation; working text follows the witnesses | auto（事實判定 / factual） |
| `displacement` | 屬於已登記的 X3 移段塊 / inside a registered X3 block | auto |
| `interpolation` | 底本補入的文字（I-*）/ text the base inserted | auto |
| `transcription-gap` | 見證本轉錄缺頁 / page gap in a witness transcription | auto |
| `witness-noise` | 維基頁面提示、雜入的注語 / wiki notices, stray notes | auto |
| `scribal-error` | 某一讀法為傳抄錯誤 / one reading is a copying error | 人工 / human |
| `substantive` | 實質不同的讀法 / genuinely different readings | 人工 / human |
| `unclassified` | 待審，`reason` 給出提示 / to review; `reason` gives a hint | — |

**人工判定 / Human decisions**：寫入 `projects/shanhaijing/ledgers/variant-overrides.jsonl`，每行 `{key, status, reason, by}`，`key` 取自 `variant-classes.jsonl`。人工判定永遠優先於自動規則，重新產生資料時也不會遺失。/ one line per decision, keyed by `key`; always wins over the auto rules and survives regeneration.

## 5. 假說證據項 Evidence item（卷宗內表格，未來會轉成 `evidence.jsonl` / dossier tables, later `evidence.jsonl`）

```json
{"hypothesis": "H-0001", "pred": "P4", "channel": "HYD", "entries": ["SHJ-02-3-008"],
 "quote": "黑水出焉，而西流于大杅", "external_fact": "Nile flows S→N", "citation": null,
 "comparison_set": "any locus that is not a river source", "grade": "E-2", "log10_lr": -1.0,
 "correlated_with": [], "emendations": []}
```

## 6. 地名帳 Toponym ledger（規劃中 / planned: `ledgers/toponyms.jsonl`）
`{name, variants[], entries[], type: 山|水|海|澤|國|丘|虛, relations[], candidates[{hypothesis, locus, verdict}]}`
同一地名的不同假說並列，**不寫「定論」欄位**。/ Different hypotheses for the same name sit side by side; **there is no "settled answer" field**.

## 7. 物種帳 Taxon ledger（規劃中 / planned: `ledgers/taxa.jsonl`）
`{name, entries[], features{body, parts, colour, sound, behaviour, habitat}, candidates[{taxon, fit_table, habitat_ok}]}`
