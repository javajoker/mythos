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
| T-102 | 逐條分類 2,026 筆異文（異體 / 訛誤 / 實質 / 錯簡）/ classify the 2,026 variants | `textual-critic` + skill `witness-collation` | ⬜ |
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
| T-303 | 全書水系圖：出、注、潛關係，同名河流歸併，懸空節點檢查 / whole-book river graph: merge same-name rivers, check dangling nodes | `shj-route-reconstructor` | ⬜ |
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
| T-610 | 用 H-0001 的觀察 O-2、O-3、O-4 做全球盲候選生成 / blind global candidates from H-0001 observations O-2–O-4 | `geo-triangulator` | ⬜ |
| T-611 | 為西次三經生成 ≥ 3 個候選框架（必含本地框架和虛無假說）/ ≥ 3 candidate frames for 西次三經 (incl. local + null) | `geo-triangulator` | ⬜ |

## S7–S8 交叉定位與裁決 / Triangulation & adjudication
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-701 | H-0001 全流程卷宗 / full H-0001 dossier | `shj-lead` | ✅ |
| T-702 | 對 T-611 的每個候選做多通道擬合 / multi-channel fits for each T-611 candidate | `shj-lead` | ⬜ |
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
