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
| T-E05 | 檢查同名河流的拆分與合併（洛、丹、涇等）/ audit homonym-river splits and merges | `entity-extractor` | ⬜ |
| T-E06 | 抽取空間句式：之南／之北、之濱、之後／之前、環之、其外有、「X流于Y」（無「注」）；修正「外有炎火之山」等名稱（紅隊 R1，例 `SHJ-16-1-037`）/ extract spatial clauses and fix names found by review R1 | `entity-extractor` | ⬜ |
| T-E07 | 每段每種關係只計一次（去除 25 條重複）；以動物部件描述的神改為神人（7 個）/ dedupe relations; deities with animal parts are persons | `kg_extract.py` | ✅ |

## 步驟 3 真實世界候選 / Candidates
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-C01 | 全球庫：31 地區、36 性質、135 水體、116 動物、47 文化 / world base | `data/world/` | ✅ |
| T-C02 | 每個實體的候選與自身分數 / candidates with own scores | `kg_candidates.py` | ✅ |
| T-C03 | **庫的平衡**：以統一規則補 125 條支流（R1、R2，見 data/world/README）；重跑後河流全部暫定 / tributaries balanced by one rule; all rivers tentative after re-run | `world-candidate-scout` | ✅ |
| T-C04 | 為 121 個「無合適真實對應」的生物檢查是否缺少候選動物 / check whether unmatched creatures lack candidate animals | `world-candidate-scout` | ⬜ |
| T-C05 | 為 76 個無詞義的植物、礦物專名決定處理方式 / decide on proper-named plants and minerals | `world-candidate-scout` | ⬜ |
| T-C06 | 地區性質加「火山、熔岩湖、天然氣或石油之火」與「沙丘地形」；新候選類型「紀念建築與造像」（例：人面獸身像）/ add fire-ground and dune properties; a monument/statue candidate type | `world-candidate-scout` | ⬜ |

## 步驟 4 交叉驗證 / Cross-validation
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-X01 | 聯合求解（退火 + ICM + 區塊調整）、樣本穩定度、可信度與級別 / joint solve, stability, confidence, tiers | `kg_crossval.py` | ✅ |
| T-X02 | 確定性與單調性檢查 / determinism and monotonicity checks | `cross-validator` | ✅ |
| T-X03 | 降低多峰：各鏈總分相差約 3%；試平行回火或更多鏈 / reduce multimodality (≈3% spread across chains) | `cross-validator` | ⬜ |
| T-X04 | 權重敏感度：16 個變體＋重跑；每個對應的穩健度 / weight sensitivity with per-entity robustness | `kg_sensitivity.py` | ✅ |
| T-X05 | **待決定**：新的解讀規則：河流的地圖讀法、前／後慣例雙測、古蹟（需引證、扣分）、外觀與行為分開、觀察者替代（獅 → 虎）；全部候選一體適用 / **pending decision**: new reading rules applied to every candidate | 項目發起人 / initiator | ⬜ |
| T-X06 | 對立組態檢驗：崑崙＝開羅一帶（西海＝地中海、流沙＝撒哈拉、赤水＝紅海、黑水＝尼羅河）對比青藏、衣索比亞高原、美索不達米亞、帕米爾，報告總分與違反的關係 / rival-configuration test for Kunlun | `cross-validator` | ⬜ |
| T-X07 | 「小溪」因子從未產生（有出入記錄的水都算主要水體）：刪除或重新定義 / the minor-stream factor never fires: remove or redefine | `cross-validator` | ⬜ |

## 步驟 5 交付 / Deliverable
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-D01 | 初稿 v1：逐條對照（主要結論經紅隊 R1 撤回，已刪除）/ draft v1 (headline results withdrawn by review R1; removed) | `kg_deliver.py` | ✅ |
| T-D03 | 初稿 v2：完整性 PASS、權重穩健度、海岸線地圖 / draft v2 with robustness and a coastline map | `kg_deliver.py` → `deliverables/draft-v2/` | ✅ |
| T-D02 | 逐篇的文字摘要（每篇的山落在哪些地區、主要水系）/ per-section narrative summaries | `shj-lead` | ⬜ |

## 紅隊 / Red team
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-R01 | 審查初稿 v1：庫的偏差、誘餌（每區已知性質上限 21）、抽取錯誤、敏感度、使用者的崑崙解讀（[red-team.md](red-team.md) R1）/ review draft v1 | `devils-advocate` | ✅ |
| T-R02 | 審查初稿 v2 與 T-X06 的結果 / review draft v2 and the T-X06 results | `devils-advocate` | ⬜ |
