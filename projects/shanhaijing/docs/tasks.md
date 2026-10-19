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
| T-E06 | 抽取海經、大荒經更多的方位關係（目前多數國族只有 1–2 條 `located`）/ extract more bearings in the Sea and Wilderness books | `entity-extractor` | ⬜ |

## 步驟 3 真實世界候選 / Candidates
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-C01 | 全球庫：31 地區、36 性質、135 水體、116 動物、47 文化 / world base | `data/world/` | ✅ |
| T-C02 | 每個實體的候選與自身分數 / candidates with own scores | `kg_candidates.py` | ✅ |
| T-C03 | **庫的平衡**：每條大河列出的支流數相近（目前長江 6 條、渭河 2 條），重跑並比較 / balance listed tributaries per major river; re-run and compare | `world-candidate-scout` | ⬜ |
| T-C04 | 為 121 個「無合適真實對應」的生物檢查是否缺少候選動物 / check whether unmatched creatures lack candidate animals | `world-candidate-scout` | ⬜ |
| T-C05 | 為 76 個無詞義的植物、礦物專名決定處理方式 / decide on proper-named plants and minerals | `world-candidate-scout` | ⬜ |

## 步驟 4 交叉驗證 / Cross-validation
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-X01 | 聯合求解（退火 + ICM + 區塊調整）、樣本穩定度、可信度與級別 / joint solve, stability, confidence, tiers | `kg_crossval.py` | ✅ |
| T-X02 | 確定性與單調性檢查 / determinism and monotonicity checks | `cross-validator` | ✅ |
| T-X03 | 降低多峰：各鏈總分相差約 1%；試平行回火或更多鏈 / reduce multimodality (≈1% spread across chains) | `cross-validator` | ⬜ |
| T-X04 | 權重敏感度：UNIQ、`flows_into`、`next` 各在合理範圍內變動，報告對應的變化 / weight sensitivity | `cross-validator` | ⬜ |

## 步驟 5 交付 / Deliverable
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-D01 | 初稿 v1：869 段、4,004 次提及逐條對照，完整性 PASS / draft v1, item by item, completeness PASS | `kg_deliver.py` → `deliverables/draft-v1/` | ✅ |
| T-D02 | 逐篇的文字摘要（每篇的山落在哪些地區、主要水系）/ per-section narrative summaries | `shj-lead` | ⬜ |

## 紅隊 / Red team
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-R01 | 審查初稿 v1：反例、誘餌（河、昆侖之丘、羬羊、毛民）、庫的偏差、可信度是否被誇大 / review draft v1 | `devils-advocate` | ⬜ |
