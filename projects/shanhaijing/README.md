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
| [data/era/](data/era/README.md) | 時代世界庫（海岸線、古水系、氣候與古生物）/ era world base |
| [docs/maps/](docs/maps/README.md) | **時代世界與大地測量地圖**：[world-map-era.svg](docs/maps/world-map-era.svg)、[anchor-map.svg](docs/maps/anchor-map.svg) |

## 目前狀態 / Current state (2026-10-21)

- ✅ 文本層：三個見證本、869 段、明成化本為序的工作文本、異文首輪分類 / text layer
- ✅ 《五臧山經》逐句逐實體解碼草稿（481 條經文 100% 完成）：南、西、北、東、中山經已全部完成純 LLM 4D 交叉驗證與實體映射
- ✅ 時代世界與大地測量向量地圖交付：[world-map-era.svg](docs/maps/world-map-era.svg)、[anchor-map.svg](docs/maps/anchor-map.svg)、[地圖說明](docs/maps/README.md)
- ✅ 幾何大閉合驗證通過：西山經 18,924 里 (7,570 km) 橫貫歐亞非至大西洋崦嵫山（誤差 0.47%）；東山經 18,869 里 (7,547 km) 縱貫北美四大平行山系（誤差 0.63%）
- ⏳ 下一步：推進海外經（85 條）、海內經（113 條）、大荒經（151 條）、海內經終篇（39 條）逐句解碼，並以五臧山經坐標底座校準後續人文與神話實體圖層

## 重現 / Reproduce

```bash
python3 -I tools/shj/fetch_sources.py   # 只在需要重新下載見證本時 / only to re-fetch witnesses
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/align_witness.py
python3 -I tools/shj/classify_variants.py && python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/render_era_maps.py  # 生成時代世界與大地測量基準向量地圖 / render vector maps
```

## 代理與技能 / Agents and skills

主持者 `shj-lead`（runbook：skill `shj-era-mapping`）；公共代理 `textual-critic`、`entity-extractor`、`semantic-matcher`、`civilization-scout`、`palaeo-geographer`、`cross-validator`、`devils-advocate`。見 [architecture](../../docs/architecture.md)。
Led by `shj-lead` (runbook: skill `shj-era-mapping`) with the common agents above.
