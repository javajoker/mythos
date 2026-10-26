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

> 2026-10-26 更新。全部映射與裁決為競爭假說（`proposed_pending_review`），待發起人覆核。

- 文本層：三見證本快照 manifest、869 條 working text（base 讀法仍 `unreviewed`）、對勘/移段/異文分類、447 個山經站點與 26 個篇末總數。
- 適配層：五臧山經 26 子經五件套（站點網格/逐實體映射/適配報告/逐句文檔/SVG 地圖，見 `data/derived/era/adaptation/`）＋卷六至十八 13 卷框架書三件套＋補丁圖；概要圖 7 張（分經 5＋五臧總體＋全書太平洋中心視圖）。
- 圖譜：KG v1 = 4,334 節點／4,618 提及／1,805 邊／9,234 屬性（地理映射全覆蓋＋人文風物讀法＋associative/deductive＋框架書待定錨與關係）。
- 草稿：`deliverables/draft-v1/`（結構版）與 `deliverables/draft-v2/`（白話通順版，869 條目、111 張本地配圖、各卷嵌地圖）。
- 裁決：ADJ-002 昆侖虛＝撒哈拉之眼；ADJ-003 燭龍＝極晝極夜＋極光；ADJ-004 兩河採納 F-0007；ADJ-005 名類判別（見 `findings/`）。
- Web App：`webapp/`（文檔在 `webapp/docs/`；本地 `python3 -m http.server` 於 webapp/ 後開 index.html——世界地圖/卷目錄/實體庫/裁決記錄）。
- 待完成：發起人覆核全部適配與裁決；紅隊審查。

## 重現文本層 / Reproduce the text layer

```bash
# 文本層
python3 -I tools/shj/fetch_sources.py --manifest-only
python3 -I tools/shj/ingest.py
python3 -I tools/shj/collate.py
python3 -I tools/shj/align_witness.py
python3 -I tools/shj/classify_variants.py
python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/era_frame.py
python3 -I tools/shj/kg_build.py
# 適配與圖譜（語義內容由 LLM 產生於 era/adaptation/，工具只做組裝與核對）
python3 tools/shj/kg_v1_assemble.py        # 山經地理映射屬性
python3 tools/shj/kg_readings_build.py     # 人文風物讀法
python3 tools/shj/kg_assoc_ded_build.py    # 賦義/功用層
python3 tools/shj/kg_framework_build.py    # 卷六至十八實體
python3 tools/shj/kg_edges_build.py        # 框架書關係邊
python3 -I tools/shj/kg_validate.py --require-graph
# 地圖與草稿
python3 tools/shj/render_nanci_map.py <specs/…-map.json>     # 子經圖
python3 tools/shj/render_overview_map.py <specs/…json>       # 概要/補丁圖
python3 tools/shj/build_shanjing_overview.py                 # 全書概要 spec
python3 tools/shj/draft_wuzang_build.py                      # draft-v1
```


只在明確需要更新上游見證本時，不帶 `--manifest-only` 執行 `fetch_sources.py`。更新後必須重新審查所有受影響的對勘、判斷與衍生資料。

## Agent 與 skill

主持者 `shj-lead`，runbook 為 `shj-era-mapping`。文本、實體、時代世界、語義、交叉驗證與紅隊角色見 [架構 v4](../../docs/architecture.md)。公共 agent/skill 不含《山海經》的固定地理答案。
