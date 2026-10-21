# 山海經子項目 / Shanhaijing Sub-project

> 第一版時代窗口：**4000–1000 BCE**。以工作文本為證據，透過競爭候選與迭代圖譜檢驗《山海經》可能保存的時代觀測。
> First-version window: 4000–1000 BCE. All real-world correspondences are competing hypotheses.

## 權威規格 / Authoritative specifications

| 文件 / Document | 內容 / Content |
|---|---|
| [docs/methodology-spec.md](docs/methodology-spec.md) | 發起人確認的迭代流程、第一版地理復用、比例尺與地標共識 |
| [docs/data-model.md](docs/data-model.md) | 工作文本、圖譜、屬性、判斷與 LLM 裁決格式 |
| [data/kg-ontology.json](data/kg-ontology.json) | 按實體類型定義的可擴展 predicate 與關係 |
| [docs/era-world.md](docs/era-world.md) | 時代世界庫的範圍、卡片要求與目前缺口 |
| [docs/tasks.md](docs/tasks.md) | 可驗證任務狀態 |
| [docs/checklist.md](docs/checklist.md) | 草稿與交付前檢查 |
| [docs/red-team.md](docs/red-team.md) | 紅隊審查記錄 |
| [docs/source-assessment.md](docs/source-assessment.md) | 見證本、移段、缺頁與讀法政策 |
| [findings/](findings/) | 文本層發現與後續 LLM 衝突日誌 |

公共方法見 [研究框架 v4](../../docs/research-framework.md)，已裁決的項目整理見 [決策記錄](../../docs/project-review.md)。

## 目前狀態 / Current state

- 已完成：舊解釋草稿、地圖、渲染器與舊圖譜清理；框架、規格和本體 v4。
- 已生成：三個見證本快照 manifest、869 條 base entries、working text、對勘、移段、異文分類、447 個山經站點與 26 個篇末總數。
- 注意：working text 的 base 讀法目前仍為 `unreviewed`，不能宣稱所有正式讀法已確認。
- 第一輪已完成：五臧山經 481 段實體抽取，3,781 條提及、3,593 個節點、1,019 條關係邊；另有 488 個山體與 452 個水體節點。
- 待你審核：5 組初始化錨點與 27 條候選屬性，見 [anchor-review.md](data/derived/review/anchor-review.md)。全部為未確認候選，需經聯合校準。
- 待完成：全量時代世界卡與其餘語義判斷、KG v1 定稿、新草稿、紅隊和地圖。
- 時代世界庫仍是種子資料；`sites.jsonl` 與 `palaeo-coast.json` 尚未建立。

## 重現文本層 / Reproduce the text layer

```bash
python3 -I tools/shj/fetch_sources.py --manifest-only
python3 -I tools/shj/ingest.py
python3 -I tools/shj/collate.py
python3 -I tools/shj/align_witness.py
python3 -I tools/shj/classify_variants.py
python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/era_frame.py
python3 -I tools/shj/kg_build.py
python3 -I tools/shj/kg_export_geography.py
python3 -I tools/shj/kg_validate.py --require-graph
```

只在明確需要更新上游見證本時，不帶 `--manifest-only` 執行 `fetch_sources.py`。更新後必須重新審查所有受影響的對勘、判斷與衍生資料。

## Agent 與 skill

主持者 `shj-lead`，runbook 為 `shj-era-mapping`。文本、實體、時代世界、語義、交叉驗證與紅隊角色見 [架構 v4](../../docs/architecture.md)。公共 agent/skill 不含《山海經》的固定地理答案。
