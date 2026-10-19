# 山海經子項目任務 / Shanhaijing Sub-project Tasks

> v2.0 ・ 2026-10-19 ・ 狀態 / Status: ✅ done ・ ⏳ in progress ・ ⬜ todo
> 方法：實體圖譜交叉驗證（[methodology-spec](methodology-spec.md)）。舊方法（方法 A 的 S0–S9 卷宗、方法 G 的地點比對）的任務已隨方法退役，記錄在 git 歷史中。/ Tasks of the retired methods are in git history.
> 編號 / IDs: `T-0nn`–`T-2nn` 文本層 / text layer（沿用舊編號 / kept）；`T-E` 實體與關係（步驟 1–2）；`T-C` 候選（步驟 3）；`T-X` 交叉驗證（步驟 4）；`T-D` 交付（步驟 5）；`T-R` 紅隊 / red team。

## 文本層 / Text layer
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-001 | 擷取三個見證本（通行本、四部叢刊明成化本、四庫本）/ fetch the three witnesses | `fetch_sources.py` | ✅ |
| T-002 | 逐段編號（869 段），分離注疏與編者註 / per-paragraph IDs, commentary split off | `ingest.py` | ✅ |
| T-003 | 在明成化本與四庫本中定位每個底本條目 / locate every base entry in both witnesses | `align_witness.py` | ✅ |
| T-004 | 以明成化本為序的工作文本 / working text in Chenghua order | `align_witness.py` | ✅ |
| T-005 | 對照掃描頁補齊四部叢刊本缺頁（卷 1 三山；卷 15 一頁）/ fill the Sibu Congkan gaps from the scans | `textual-critic` | ⬜ |
| T-101 | 機器對勘，異文歸屬到條目 / machine collation | `collate.py` | ✅ |
| T-102 | 異文分類：自動 1,604 / 2,021；人工審查已取消，採草稿讀法政策（source-assessment §4）/ auto-classified; human review cancelled; draft-reading policy | `classify_variants.py` | ✅（草稿 / draft） |
| T-103 | 擴充異體字摺疊表 / extend the graphic-variant fold table | `textual-critic` | ⬜ |
| T-104 | 登記底本的現代移段 X3-001–008 與補入文字 / register modern relocations and insertions | `align_witness.py` | ✅ |
| T-105 | 以見證本的數字讀法重抽里程，檢查與篇末總數的差異（F-0002）/ re-extract distances with witness numerals; check against section totals | `textual-critic` | ⬜ |
| T-201 | 山經站點、方位、里程、水系抽取（447 站）/ Mountain-Classic stations | `extract_routes.py` | ✅ |
| T-202 | 補抓段內遺漏的站點（例：`SHJ-02-3-010` 的「蠃母之山」）/ catch stations missed inside paragraphs | `entity-extractor` | ⬜ |

## 步驟 1–2 實體、性質、關係 / Entities, properties, relations
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-E01 | 全書實體抽取與合併：1,941 個實體、10 種類型 / whole-book extraction and merge | `kg_extract.py` | ✅ |
| T-E02 | 關係抽取：2,750 條邊（相鄰、發源、注入、潛入、位於、望見、產…）/ relation extraction | `kg_extract.py` | ✅ |
| T-E03 | 覆蓋檢查：無實體段落 0、未解釋的名稱句式 0 / coverage audit at 0 / 0 | `kg_extract.py` → `kg/coverage.md` | ✅ |
| T-E04 | 為 50 個「未定」（UNK）實體確定類型 / type the 50 undetermined entities | `entity-extractor` | ⬜ |
| T-E05 | 檢查同名河流的拆分與合併（洛、丹、涇；崑崙之丘與勞山的兩個弱水，紅隊 R2）/ audit homonym-river splits and merges | `entity-extractor` | ⬜ |
| T-E06 | 抽取空間句式：之南／之北、之濱、之後／之前、環之、其外有、「X流于Y」（無「注」）；修正「外有炎火之山」等名稱（紅隊 R1，例 `SHJ-16-1-037`）/ extract spatial clauses and fix names found by review R1 | `kg_extract.py` | ✅ |
| T-E07 | 每段每種關係只計一次（去除 25 條重複）；以動物部件描述的神改為神人（7 個）/ dedupe relations; deities with animal parts are persons | `kg_extract.py` | ✅ |

## 步驟 3 真實世界候選 / Candidates
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-C01 | 全球庫：31 地區、36 性質、135 水體、116 動物、47 文化 / world base | `data/world/` | ✅ |
| T-C02 | 每個實體的候選與自身分數 / candidates with own scores | `kg_candidates.py` | ✅ |
| T-C03 | **庫的平衡**：以統一規則補 125 條支流（R1、R2，見 data/world/README）；重跑後河流全部暫定 / tributaries balanced by one rule; all rivers tentative after re-run | `world-candidate-scout` | ✅ |
| T-C04 | 補動物候選：會說話的鳥、有爪的獸，以及動物少於 18 種的地區（共 29 種）/ 29 animals added by rule | `data/world/animals.jsonl` | ✅ |
| T-C05 | 為 76 個無詞義的植物、礦物專名決定處理方式 / decide on proper-named plants and minerals | `world-candidate-scout` | ⬜ |
| T-C06 | 性質「火或酷熱」「方形外觀」；古水體 9 個；長條形海的軸向與出口；哈拉帕 / fire-or-heat and square-form properties, palaeo waters, sea axes, Harappan | `data/world/` | ✅ |
| T-C07 | 河谷文明自成一區：EGY（埃及與尼羅河下游）、IDS（印度河流域）/ split river-valley regions | `data/world/regions.jsonl` | ✅ |
| T-C09 | 全世界的乾河谷與古運河（R2）/ dry valleys and ancient canals worldwide | `data/world/waters.jsonl` | ✅ |
| T-C10 | 比地區更細的地點（河岸、沙漠邊緣），用於「黑水之前」「流沙之濱」/ places finer than regions | `world-candidate-scout` | ⬜ |
| T-C08 | 「紀念建築與造像」作為生物或神人的候選（例：人面獸身像）/ monuments and statues as candidates for described beings | `world-candidate-scout` | ⬜ |

## 步驟 4 交叉驗證 / Cross-validation
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-X01 | 聯合求解（退火 + ICM + 區塊調整）、樣本穩定度、可信度與級別 / joint solve, stability, confidence, tiers | `kg_crossval.py` | ✅ |
| T-X02 | 確定性與單調性檢查 / determinism and monotonicity checks | `cross-validator` | ✅ |
| T-X03 | 降低多峰：各鏈總分相差約 3%；試平行回火或更多鏈 / reduce multimodality (≈3% spread across chains) | `cross-validator` | ⬜ |
| T-X04 | 權重敏感度：16 個變體＋重跑；每個對應的穩健度 / weight sensitivity with per-entity robustness | `kg_sensitivity.py` | ✅ |
| T-X05 | 解讀規則 R1–R7（framework §3.1）：水只是水體、時間深度、山只是外觀、外觀與效果、前 = 東、地圖讀法、觀察者替代；全部候選一體適用 / reading rules adopted (initiator, 2026-10-19) | `kg_candidates.py`, `kg_crossval.py` | ✅ |
| T-X06 | 聯合假說：西次一經 = 印度河、西次二經 = 美索不達米亞、西次三經 = 埃及（赤水 = 紅海、黑水 = 尼羅河、西海 = 地中海）對比衣索比亞、中國、塔里木、伊朗—中亞、北美誘餌 / joint hypothesis vs rivals | `kg_sections.py` | ✅（−40.8，不被支持 / not supported）|
| T-X08 | 篇段掃描：26 篇 × 33 地區，附完整重解 / section × region scan with full re-solves | `kg_sections.py` | ✅ |
| T-X09 | 約束 R1：有「出焉」（一端在山）的水不對到大洋（「河 = 大西洋」副作用）/ constrain R1: waters with a stated source are not oceans | `cross-validator` | ⬜ |
| T-X07 | 「小溪」因子從未產生（有出入記錄的水都算主要水體）：刪除或重新定義 / the minor-stream factor never fires: remove or redefine | `cross-validator` | ⬜ |

## 步驟 5 交付 / Deliverable
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-D01 | 初稿 v1：逐條對照（主要結論經紅隊 R1 撤回，已刪除）/ draft v1 (headline results withdrawn by review R1; removed) | `kg_deliver.py` | ✅ |
| T-D03 | 初稿 v2：完整性 PASS、權重穩健度、海岸線地圖 / draft v2 with robustness and a coastline map | `kg_deliver.py` | ✅（由 v3 取代 / superseded）|
| T-D04 | 初稿 v3：解讀規則、篇段地圖、假說檢驗 / draft v3 with reading rules, section map and hypothesis tests | `kg_deliver.py` → `deliverables/draft-v3/` | ✅ |
| T-D02 | 逐篇的文字摘要（每篇的山落在哪些地區、主要水系）/ per-section narrative summaries | `shj-lead` | ⬜ |

## 紅隊 / Red team
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-R01 | 審查初稿 v1：庫的偏差、誘餌（每區已知性質上限 21）、抽取錯誤、敏感度、使用者的崑崙解讀（[red-team.md](red-team.md) R1）/ review draft v1 | `devils-advocate` | ✅ |
| T-R02 | 審查初稿 v3、解讀規則的對稱性與 T-X06 的結果（[red-team.md](red-team.md) R2）/ review draft v3 | `devils-advocate` | ✅ |
