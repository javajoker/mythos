# 山海經子項目 / Shanhaijing Sub-project

> 把《山海經》看作前 4000–前 2000 年逐步積累的傳承紀錄：從中原出發、只用原文、容許傳抄錯誤，依語義相關性對應到**當時的世界**（當時的海岸、河道、動物、文明與其造物），不預設它記的是哪一個地區。
> The Shanhaijing as a record accumulated 4000–2000 BCE: read from the Central Plains, original text only, copying errors tolerated, mapped by semantic correspondence onto the world of that period, with no region presupposed.

## 文檔 / Documents

| 文件 / Doc | 內容 / Content |
|---|---|
| [docs/methodology-spec.md](docs/methodology-spec.md) | **方法規格 v3**：原點、時代世界、遮蔽的語義評分、聯合求解、當時地圖 / method spec v3 |
| [docs/era-world.md](docs/era-world.md) | **時代世界**：前 4000–前 2000 年的海岸線、河道、氣候、文明與動物 / the world of 4000–2000 BCE |
| [docs/data-model.md](docs/data-model.md) | 文本層、知識圖譜、時代世界庫、判斷紀錄、對應 / schemas |
| [docs/tasks.md](docs/tasks.md) | 任務與狀態 / tasks |
| [docs/checklist.md](docs/checklist.md) | 交付前檢查清單 / pre-delivery checklist |
| [docs/red-team.md](docs/red-team.md) | 紅隊審查紀錄 / red-team log |
| [docs/source-assessment.md](docs/source-assessment.md) | 三個見證本、現代移段、讀法政策 / witnesses, relocations, reading policy |
| [findings/](findings/) | 文本層的發現（F-0001 現代移段、F-0002 里程自洽）/ text-layer findings |
| [data/era/](data/era/README.md) | 時代世界庫（目前為種子，待轉換）/ era world base (seeds, to convert) |
| [data/derived/kg/](data/derived/kg/) | 知識圖譜：1,943 個實體、2,741 條關係；覆蓋檢查 0 / 0 / knowledge graph |

## 目前狀態 / Current state (2026-10-20)

- ✅ 文本層：三個見證本、869 段、明成化本為序的工作文本、異文首輪分類 / text layer
- ✅ 知識圖譜：全書實體與關係，覆蓋檢查通過 / knowledge graph
- ✅ 框架 v3、時代世界文件、規格、agent 與 skill / framework v3, era world doc, spec, agents, skills
- ✅ 觀察框架與西、東、中山經的篇段錨點（暫定，未遮蔽）：[anchors.md](data/derived/era/anchors.md)、[anchor-map.svg](data/derived/era/anchor-map.svg) / observer frame and provisional section anchors
- ⏳ 下一步：以遮蔽輸入重判錨點、時代世界庫、逐實體語義評分、求解，之後擴及全書並交付 draft-v4 / next: masked re-judging, era base, entity judgments, solver, draft-v4

先前方法的結果與交付只保留在 git 歷史中。/ Earlier methods and drafts are in git history only.

## 重現 / Reproduce

```bash
python3 -I tools/shj/fetch_sources.py   # 只在需要重新下載見證本時 / only to re-fetch witnesses
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/align_witness.py
python3 -I tools/shj/classify_variants.py && python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/kg_extract.py       # 知識圖譜與覆蓋檢查 / knowledge graph and coverage audit
```
時代語義版的工具（`era_frame`、`era_tasks`、`era_leakage`、`era_relations`、`era_solve`、`era_sensitivity`、`era_sections`、`era_deliver`）在試點中建立，見 [tasks](docs/tasks.md)。/ Era tools are built in the pilot.

## 代理與技能 / Agents and skills

主持者 `shj-lead`（runbook：skill `shj-era-mapping`）；公共代理 `textual-critic`、`entity-extractor`、`semantic-matcher`、`civilization-scout`、`palaeo-geographer`、`cross-validator`、`devils-advocate`。見 [architecture](../../docs/architecture.md)。
Led by `shj-lead` (runbook: skill `shj-era-mapping`) with the common agents above.
