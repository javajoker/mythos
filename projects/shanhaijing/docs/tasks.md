# 山海經子項目任務 / Shanhaijing Sub-project Tasks

> v3.0 ・ 2026-10-20 ・ 方法：時代語義對應（[框架 v3](../../../docs/research-framework.md)、[規格 v3](methodology-spec.md)）。先前方法的任務只保留在 git 歷史中。
> 狀態 / Status: ✅ done ・ ⏳ in progress ・ ⬜ todo ・ 編號 / IDs: `T-0nn`–`T-2nn` 文本層 / text layer；`T-K` 知識圖譜 / knowledge graph；`T-V` 時代語義版 / era version；`T-R` 紅隊 / red team。

## 文本層 / Text layer
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-001 | 擷取三個見證本（通行本、四部叢刊明成化本、四庫本）/ fetch the three witnesses | `fetch_sources.py` | ✅ |
| T-002 | 逐段編號（869 段）；注疏分欄保存，不進入分析 / IDs; commentary kept apart, never analysed | `ingest.py` | ✅ |
| T-003 | 在明成化本與四庫本中定位每個底本條目 / locate every base entry in both witnesses | `align_witness.py` | ✅ |
| T-004 | 以明成化本為序的工作文本 / working text in Chenghua order | `align_witness.py` | ✅ |
| T-005 | 對照掃描頁補齊四部叢刊本缺頁 / fill the Sibu Congkan gaps from the scans | `textual-critic` | ⬜ |
| T-101 | 機器對勘 / machine collation | `collate.py` | ✅ |
| T-102 | 異文分類（自動首輪；草稿讀法政策，見 source-assessment §4）/ variant classes | `classify_variants.py` | ✅ |
| T-103 | 擴充異體字摺疊表 / extend the graphic-variant fold table | `textual-critic` | ⬜ |
| T-104 | 登記底本的現代移段與補入文字 / register modern relocations and insertions | `align_witness.py` | ✅ |
| T-105 | 以見證本的數字讀法重抽里程，並記為替代讀法（R11）/ witness numerals as variant readings | `textual-critic` | ⬜ |
| T-201 | 山經站點、方位、里程、水系（447 站）/ Mountain-Classic stations | `extract_routes.py` | ✅ |
| T-202 | 補抓段內遺漏的站點（例：`SHJ-02-3-010` 的「蠃母之山」）/ missed stations | `entity-extractor` | ⬜ |

## 知識圖譜 / Knowledge graph
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-K01 | 全書實體、關係（含框架句、環之、其外有、流于）；覆蓋檢查 0 / 0 / entities and relations; coverage 0 / 0 | `kg_extract.py` | ✅ |
| T-K02 | 為 47 個「未定」實體確定類型 / type the undetermined entities | `entity-extractor` | ⬜ |
| T-K03 | 同名誤併：崑崙之丘與勞山的兩個弱水、洛、丹、涇等 / merged homonyms | `entity-extractor` | ⬜ |
| T-K04 | 海經、大荒經更多的方位與相鄰關係 / more bearings in the Sea and Wilderness books | `entity-extractor` | ⬜ |

## 時代語義版 / Era-semantic version（規格 v3 → draft-v4）
設定（項目發起人，2026-10-20）：前 4000–前 2000 年的積累紀錄、中原為原點、只用原文、容許傳承錯誤、名稱語義保留但不比對今名、大模型語義判斷為主、重點為兩河流域、哈拉帕、古埃及並含同時期對立文明；試點為西山經四篇與大荒西經。

| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-V01 | 研究框架 v3、時代世界文件、規格 v3、資料模型 / framework, era-world, spec, data model | `shj-lead` | ✅ |
| T-V02 | agent 與 skill / agents and skills | `shj-lead` | ✅ |
| T-V03 | 名稱語義 `name_features`（顏色、材質、形狀、狀態、方位）/ name features | `entity-extractor` | ⬜ |
| T-V04 | 觀察框架 `era_frame.py`：各篇路線（里）與概況（地形、物產、水、生物）/ observer frame and section profiles | `era_frame.py` → `era/frame.jsonl`, `profiles.jsonl`, `profiles.md` | ✅ |
| T-V04b | 西、東、中山經的篇段錨點（暫定，未遮蔽，`anchor-1.0`）：比例尺約 0.2–0.3 公里／里；西次三經的領先錨點為青海—崑崙—塔里木，帕米爾為接近的對立候選；報告與地圖 / provisional section anchors, report and map | `era_anchors.py` → `era/anchors.jsonl`, `anchors.md`, `anchor-map.svg` | ✅（暫定）|
| T-V04d | 基準點（暫定，`benchmark-1.0`）：西海、赤水、黑水、流沙、崑崙之丘、炎火之山、泑澤、湯谷與十日、燭龍、大壑、白令；三種來源的候選與對立候選；世界地圖（含美洲、白令、緯度帶）/ benchmark points and world map | `era_anchors.py` → `era/benchmarks.jsonl`, `benchmarks.md`, `world-map-era.svg` | ✅（暫定）|
| T-V04e | 檢驗緯度帶模型：同名拆分（西海、赤水、河是否為相對或同名異實）、各篇是否串接、各書的比例尺是否可以不同；以固定組態與篇段錨點一起求解 / test the latitude-belt model | `cross-validator`, `entity-extractor` | ⬜ |
| T-V04c | 以遮蔽輸入重判篇段錨點與基準點，與未遮蔽的結果比較（洩漏）/ re-judge anchors and benchmarks masked and compare | `semantic-matcher`, `devils-advocate` | ⬜ |
| T-V05 | 時代世界庫：把 `data/era/` 的種子改為窗口內的狀態；新建 `sites.jsonl`（遺址與造物，含對立文明）與 `palaeo-coast.json` / convert the seeds; sites; palaeo coasts | `civilization-scout`, `palaeo-geographer` | ⬜ |
| T-V06 | 判斷任務 `era_tasks.py`（遮蔽、名稱特徵、關係摘要、樣本、雜湊、誘餌）/ judgment tasks | `cross-validator` | ⬜ |
| T-V07 | 試點的候選生成與語義評分 / pilot judgments | `semantic-matcher` | ⬜ |
| T-V08 | 洩漏與誘餌 `era_leakage.py` / leakage and decoys | `devils-advocate` | ⬜ |
| T-V09 | 關係評分 `era_relations.py` 與求解 `era_solve.py`（改寫自 git 歷史中的求解器）/ relations and solver | `cross-validator` | ⬜ |
| T-V10 | 敏感度 `era_sensitivity.py` 與假說組態 `era_sections.py`（兩河、哈拉帕、埃及與對立組態）/ sensitivity and hypotheses | `cross-validator` | ⬜ |
| T-V11 | 交付 `era_deliver.py`：逐段對照、當時地圖 `era-map.svg`、`hypotheses.md` / deliverable and era map | `shj-lead` | ⬜ |
| T-V12 | 擴及全書，交付 draft-v4 / full book, draft-v4 | `shj-lead` | ⬜ |

## 紅隊 / Red team
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-R01 | 試點審查：洩漏、誘餌、今名比對、對稱、年代、單點依賴 / pilot review | `devils-advocate` | ⬜ |
| T-R02 | draft-v4 審查 / draft-v4 review | `devils-advocate` | ⬜ |
