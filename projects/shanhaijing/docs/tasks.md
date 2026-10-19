# 山海經子項目任務 / Shanhaijing Sub-project Tasks

> 狀態 / Status: ✅ done ・ ⏳ in progress ・ ⬜ todo。編號按方法階段分組（T-0xx 對應 S0，依此類推）。
> IDs grouped by method stage (T-0xx ↔ S0, …). Agent / skill names refer to [.claude/](../../../.claude/).

## S0 語料 / Corpus
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-001 | 擷取三個見證本（通行本、四部叢刊明成化本、四庫本）/ fetch the three witnesses | `tools/shj/fetch_sources.py` | ✅ |
| T-002 | 逐段編號，分離注疏、異文和現代編者註 / per-paragraph IDs; split commentary, variants and editorial notes | `tools/shj/ingest.py` | ✅ |
| T-003 | 在明成化本與四庫本中定位每個底本條目（n-gram 投票，與順序無關），建立對應表 / locate every base entry in the Chenghua and Siku witnesses (order-independent n-gram voting) | `tools/shj/align_witness.py` → `witness-alignment.jsonl` | ✅ |
| T-004 | 產生以明成化本為序的正式工作文本 `working-text.jsonl`（讀法暫取底本，待 T-102 逐條選定）/ build the canonical working text in Chenghua order (base readings until T-102 chooses per variant) | `tools/shj/align_witness.py` | ✅ |
| T-005 | 對照掃描頁補齊四部叢刊本缺頁（卷 1 洵山、虖勺、區吳三山；卷 15 一頁）/ fill the Sibu Congkan gaps from the scans (book 1: 洵山, 虖勺, 區吳; one page of book 15) | `textual-critic` | ⬜ |

## S1 校勘 / Textual criticism
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-101 | 機器對勘並把異文歸屬到條目 / machine collation, variants attributed to entries | `tools/shj/collate.py` | ✅ |
| T-102 | 異文分類：自動首輪已分類 1,604 / 2,021 筆。**人工審查已取消（2026-10-19，項目發起人決定）**；初稿採用「草稿讀法政策」（source-assessment §4.4），其餘 417 筆在卷宗引用時逐條處理 / variant classification: 1,604 of 2,021 auto-classified. **Human review cancelled (2026-10-19, initiator's decision)**; the draft uses the draft-reading policy (source-assessment §4.4) and handles the other 417 case by case when a dossier cites them | `tools/shj/classify_variants.py` | ✅（草稿 / draft） |
| T-105 | 以見證本讀法（底本偏離中的 19 處數字）重新抽取山經里程，比較與篇末總數的自洽度變化 / re-extract Mountain-Classic distances with the witness readings (19 numeral base-deviations) and compare consistency with the stated totals | `shj-route-reconstructor` | ⬜ |
| T-103 | 擴充異體字摺疊表，降低雜訊 / extend the graphic-variant fold table to reduce noise | `textual-critic` | ⬜ |
| T-104 | 登記底本中的現代移段為錯簡假說：X3-001–008（22 條），補入文字 I-001–002 / register modern relocations as X3-001–008 (22 entries) and insertions I-001–002 | `align_witness.py` → `displacements.jsonl`；source-assessment §3.1 | ✅ |

## S2 結構抽取 / Extraction
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-201 | 山經站點、方位、里程、水系、生物抽取 v1 / Mountain-Classic extraction v1 | `tools/shj/extract_routes.py` | ✅ |
| T-202 | 補抓遺漏的站點（例如 `SHJ-02-3-010` 段內的「蠃母之山」）/ catch missed stations (e.g. 蠃母之山 inside `SHJ-02-3-010`) | skill `shj-itinerary-reconstruction` | ⬜ |
| T-203 | 抽取「望」見關係（方向約束）/ extract sight-lines | 同上 / same | ⬜ |
| T-204 | 抽取礦產詞表和分佈 / mineral lexicon and distribution | 同上 / same | ⬜ |
| T-205 | 生物描述的特徵向量（形、色、聲、習性）/ creature feature vectors | skill `biogeo-identification` | ⬜ |
| T-206 | 海經、大荒經的相對方位關係抽取（A 在 B 某方）/ relative-position relations in the Sea and Wilderness classics | skill `toponym-triangulation` | ⬜ |

## S3 內部一致性 / Internal consistency
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-301 | 26 段里程與篇末總數對比 / leg sums vs stated totals for 26 sections | `extract_routes.py` | ✅ |
| T-302 | 逐段解釋每個差異（抽取錯誤 / 文本錯誤 / 未解），例如中山經首篇 937 對 6670、中次十二經「凡十萬山」/ explain each discrepancy | `shj-route-reconstructor` | ⬜ |
| T-303 | 全書水系圖：出、注、潛關係，同名河流歸併，懸空節點檢查 / whole-book river graph: merge same-name rivers, check dangling nodes | `tools/shj/river_graph.py` | ✅ |
| T-310 | 大荒西經的相對方位網路，作為 H-0001b 的前置任務 / 大荒西經 relative network (prerequisite for H-0001b) | `geo-triangulator` | ⬜ |

## S4 相對重建 / Relative reconstruction
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-401 | 鏈條擬合工具（蒙地卡羅）/ Monte Carlo chain-fit tool | `tools/shj/chain_fit.py` | ✅ |
| T-402 | 26 段的不錨定相對圖與不確定度橢圓 / unanchored relative maps with uncertainty ellipses for all 26 sections | `shj-route-reconstructor` | ⬜ |
| T-403 | 各段之間的銜接：哪幾段共享地名或水系 / inter-section links via shared names or rivers | 同上 / same | ⬜ |

## S5–S6 指紋與盲候選 / Fingerprints & blind candidates
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-501 | 每段的指紋卡（地形、水系型態、生物、礦產、氣候）/ fingerprint card per section | `naturalist` + `geo-triangulator` | ⬜ |
| T-610 | 用 H-0001 的觀察 O-2、O-3、O-4 做全球盲候選生成；O-4 已由 H-0003 部分處理 / blind global candidates from O-2–O-4; O-4 partly handled in H-0003 | `geo-triangulator` | ⏳ |
| T-611 | 為西次三經生成 ≥ 3 個候選框架（必含本地框架和虛無假說）/ ≥ 3 candidate frames for 西次三經 (incl. local + null) | H-0003 | ✅ |
| T-620 | 海外四經奇異民族與真實習俗的比對（黑齒、雕題、穿胸等）/ match 海外 strange peoples with real customs | `naturalist` | ⬜ |
| T-630 | 核實甲骨「四方風」刻辭（合集 14294）釋文並與大荒經比對 / verify the oracle-bone four-winds inscription and compare | `textual-critic` | ⬜ |
| T-640 | 尋找東西地平線各有 6–7 個標記山頭的觀測點 / find an observation site with 6–7 horizon markers east and west | `geo-triangulator` | ⬜ |
| T-650 | 南山經、東山經的指紋與候選（河網連結少，需改用地形與生物通道）/ fingerprints for 南山經 and 東山經 via terrain and biota | `shj-lead` | ⬜ |
| T-651 | 北山經之首與泑澤的定位 / place 北山經之首 and 泑澤 | `shj-route-reconstructor` | ⬜ |
| T-652 | 西次三經西半段的定位（需篇內錨點）/ place the western half of 西次三經 (needs in-section anchors) | `shj-route-reconstructor` | ⬜ |

## S7–S8 交叉定位與裁決 / Triangulation & adjudication
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-701 | H-0001 全流程卷宗 / full H-0001 dossier | `shj-lead` | ✅ |
| T-702 | 對 T-611 的每個候選做多通道擬合 / multi-channel fits for each T-611 candidate | H-0003 | ✅ |
| T-704 | H-0002 山經核心河網卷宗；H-0004 海內知識範圍；H-0005 大荒經曆法框架 / dossiers H-0002, H-0004, H-0005 | `shj-lead` | ✅ |
| T-705 | 初稿 v0.1 綜合報告 / draft v0.1 synthesis report (`reports/draft-v0.1.md`) | `shj-lead` | ✅ |

## 方法 G / Method G
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-G01 | 方法 G 規格、框架 §10 / Method G spec and framework §10 | `shj-lead` | ✅ |
| T-G02 | 世界知識庫：94 種動物、27 處候選（跑分前提交）/ world base: 94 animals, 27 loci (committed before scoring) | `naturalist`, `geo-triangulator` | ✅ |
| T-G03 | 描述線索詞彙、生物抽取、動物地圖 / cue lexicon, creature extraction, animal map | `tools/shj/cues.py`, `creatures.py`, `animal_map.py` | ✅ |
| T-G04 | 描述優先地點比對（含 jackknife、同水系複合）/ place matcher with jackknife and composites | `tools/shj/geo_match.py` | ✅ |
| T-G05 | H-0006 崑崙全球比對 / H-0006 Kunlun global match | `shj-lead` | ✅ |
| T-660 | N5：補齊各大水系候選（每系 ≥ 4 處，含古代紀念建築），重跑 H-0006 / balance the base and rerun | `geo-triangulator` | ⬜ |
| T-661 | N6：流沙、赤水、黑水、弱水、西王母之山分別做方法 G 比對 / match the neighbouring names separately | `shj-lead` | ⬜ |
| T-662 | N7：開明諸段與西王母描述的動物投票 / animal vote for the 開明 block and 西王母 | `naturalist` | ⬜ |
| T-663 | 擴充動物庫（目前偏重南亞特有種），並補海經、大荒經的生物描述句式 / extend the animal base and the Sea/Wilderness creature formats | `naturalist` | ⬜ |
| T-703 | 引入地形、水系、GBIF、古氣候資料適配器 / DEM, river, GBIF, palaeoclimate adapters | `tools/` | ⬜ |
| T-801 | H-0001b 登記與檢驗 / register and test H-0001b | `shj-lead` | ⬜ |

## S9 發佈 / Publication
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-901 | 發現 F-0001（底本含現代移段）、F-0002（山經里程自洽性）/ findings F-0001 and F-0002 | `shj-lead` | ✅ |
| T-902 | 地名帳、物種帳的格式與首批條目 / toponym and taxon ledgers: format and first entries | `shj-lead` | ⬜ |

## 工具與代理 / Tooling & agents
| ID | 任務 / Task | 狀態 |
|---|---|---|
| T-951 | 山海經專用 agent 與 skill / Shanhaijing agents & skills | ✅ |
| T-952 | 抽取公共 agent 與 skill / extract common agents & skills | ✅ |
| T-953 | 為腳本加上回歸測試（固定輸出摘要）/ regression tests for the scripts (fixed output digests) | ⬜ |
