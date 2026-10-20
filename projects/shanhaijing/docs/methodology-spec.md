# 山海經時代語義對應規格 / Shanhaijing Era-Semantic Correspondence Spec

> v3.0 ・ 2026-10-20 ・ 實作 [研究框架 v3](../../../docs/research-framework.md)；時代世界見 [era-world.md](era-world.md)。交付：`deliverables/draft-v4/`。先前的方法與交付只保留在 git 歷史中。
> Implements framework v3; deliverable draft-v4. Earlier methods and drafts are in git history only.

---

## 0. 前提 / Premises
- **文本**：只用原文；次序與讀法依明成化本（最早的完整見證本，[source-assessment](source-assessment.md)）；注疏（郭璞注等）不進入任何步驟。869 段。/ Original text only, Chenghua order and readings; no commentary.
- **時代**：前 4000–前 2000 年逐步積累的傳承紀錄（[era-world](era-world.md) §1）。/ Accumulated 4000–2000 BCE.
- **原點**：中原（北緯 34.7°、東經 113.6°）。/ Observer origin.
- **範圍**：整個地球；不預設任何地區。/ The whole Earth; no presupposed region.

## 1. 流程 / Pipeline

| 步驟 / Step | 工具或代理 / Tool or agent | 輸出 / Outputs | 狀態 / Status |
|---|---|---|---|
| 0 文本層 / text layer | `ingest.py` … `extract_routes.py` | `entries.jsonl`, `working-text.jsonl`, `stations.jsonl` | 已有 / done |
| 1–2 實體、關係、名稱語義 / entities, relations, name semantics | `kg_extract.py`（`name_features` 待加）| `kg/nodes.jsonl`, `kg/edges.jsonl` … | 已有，待擴充 / done, to extend |
| 3 觀察框架 / observer frame | `era_frame.py` | `era/frame.jsonl`、`profiles.jsonl`、`profiles.md`（各篇路線與概況）| 已有 / done |
| 3b 篇段錨點 / section anchors | 大模型判斷（`anchor-1.0`）→ `era_anchors.py` | `era/anchors.jsonl`、`anchors.md`、`anchor-map.svg` | 暫定 / provisional |
| 4 時代世界庫 / era world base | `civilization-scout`、`palaeo-geographer`（代理）→ `data/era/` | 遺址、造物、時代地理、時代動物的屬性卡 | 種子已有，待轉換 / seeds, to convert |
| 5 候選生成 / candidates | `semantic-matcher`（代理）＋ `era_tasks.py`（產生遮蔽後的判斷任務）| `era/candidates.jsonl` | 待建 / to build |
| 6 語義評分 / semantic judgments | `semantic-matcher`（代理）| `era/judgments.jsonl`（逐項分數、證據、理由、樣本）| 待做 / to do |
| 7 關係評分 / relation judgments | 可計算者用 `era_relations.py`；需語義者用 `semantic-matcher` | `era/relation-judgments.jsonl` | 待建 / to build |
| 8 聯合求解 / joint solution | `era_solve.py`（以判斷分數計分；求解器改寫自 git 歷史中的 `kg_crossval.py`）| `era/mapping.jsonl` | 待建 / to build |
| 9 可信度、紅隊、假說 / confidence, review, hypotheses | `era_sensitivity.py`、`era_sections.py`、`era_leakage.py`；`devils-advocate` | `era/sensitivity/`, `era/sections/`, `era/leakage.md` | 待建 / to build |
| 10 交付與當時地圖 / deliverable and era map | `era_deliver.py` | `deliverables/draft-v4/`（含 `era-map.svg`）| 待建 / to build |

**試點**：先做西山經四篇與大荒西經，確認流程、成本與判斷品質，再擴及全書。/ Pilot: the four West sections and 大荒西經 first.

## 2. 實體 / Entities（步驟 1）

| 類型 / Type | 代碼 | 抽取線索 / Cues | 合併規則 / Merge rule |
|---|---|---|---|
| 山 / mountain | `MTN` | 山經站點；「有山名曰X」「X之山」「X山」 | 山經內同名不同篇者為不同實體（以 `same_name` 邊相連）；海經、大荒經提到的同名山併入唯一的山經同名山 / same name in different Mountain sections = different entities linked by `same_name`; Sea/Wilderness mentions merge into a unique Mountain namesake |
| 水 / water | `WAT` | 「X水出焉」「注于X」「X海」「X澤」「X淵」 | 同名合併；若同名之水注入不同的對象，拆成同名異水（例如兩條「洛」）/ merge by name; split when the same name flows into different targets |
| 地 / land feature | `LND` | 流沙、X野、X丘、X虛、大荒 | 同名合併 / merge by name |
| 國族 / polity–people | `POL` | 「X國」「X之國」「X民」「有人曰X」 | 同名合併（海外經與大荒經重複者）/ merge by name |
| 生物 / creature | `CRE` | 「有獸／鳥／魚／蛇焉…名曰X」「其中多X，其狀如…」「其獸多X」 | 同名合併；描述合併 / merge by name, pool descriptions |
| 植物 / plant | `PLA` | 「有木／草焉…名曰X」「其木多X」「其草多X」 | 同名合併 / merge by name |
| 礦物 / mineral | `MIN` | 「多X」「其陽多X，其陰多X」中的金、玉、銅、鐵… | 依礦物種類合併 / merge by mineral type |
| 神人 / person–deity | `PER` | 「神X」「帝X」「X生Y」「X居之」「X司之」 | 同名合併 / merge by name |

**異寫歸併 / Variant folding**：昆侖＝崑崙＝崐崘；黑＝黒；雒＝洛；榖＝穀等，只作為同一符號的寫法，不作為證據。/ spelling variants are the same symbol, never evidence.

## 3. 性質、名稱語義與關係 / Properties, name semantics and relations（步驟 2）

**性質 / Properties**：由描述抽出的標籤，詞彙見 `tools/shj/cues.py`：生物的體型參照、部件、顏色、聲音、習性；地點的礦產、植物、地形、氣候；國族的習俗、食物。/ Tags from descriptions (vocabulary in `cues.py`).

**名稱語義 / Name semantics**（R10）：名稱中的語義詞抽為節點的 `name_features`，不作為辨識依據：
- 顏色 / colour：赤、丹、朱（紅）；黑、玄（黑）；白、素（白）；青、蒼、碧（青綠）；黃（黃）
- 材質 / material：玉、金、銅、鐵、石、沙、鹽
- 形狀與尺度 / shape and scale：大、小、長、方、圓、高、積、不周
- 狀態 / state：流、弱、炎、湯、溫、冰
- 方位 / direction：東、西、南、北（從原點理解）
- 人群特徵 / people：毛、黑齒、羽、一目、長股等（只在該族為主語時）
比對的是候選的**實際特徵**（外觀為紅色的水、挾黃土的河），**不是**候選今名中的字（「紅海」「黑海」的名稱不加分）。/ Matched against the candidate's actual features, never its modern name.

**關係（邊）/ Relations (edges)**：

| 邊 / Edge | 由 → 到 | 來源句式 / Source pattern | 屬性 / Attributes |
|---|---|---|---|
| `next` | MTN → MTN | 山經「又{方}{N}里，曰…」 | 方位、里數 / bearing, li |
| `rises_at` | WAT → MTN | 「X水出焉」 | 山之陽／陰 / slope |
| `flows_into` | WAT → WAT／LND | 「…流注于Y」「…入Y」 | 流向 / direction |
| `sinks_at` | WAT → WAT／LND | 「…所潛」「潛於」 | — |
| `has_resource` | MTN → MIN／PLA | 「其上多X」「其陽多X」 | 部位 / position |
| `has_creature` | MTN／WAT → CRE | 「有獸焉」「其中多X」「其獸多X」 | — |
| `sees` | MTN → 任意 / any | 「{方}望X」 | 方位 / direction |
| `located` | 任意 → 任意 / any → any | 「X在Y{方}」「X之{方}」 | 方位 / direction |
| `dwells` / `rules` | PER → MTN／WAT | 「X居之」「X司之」「X處之」 | — |
| `begets` | PER → PER／POL | 「X生Y」 | — |
| `same_name` | MTN ↔ MTN | 不同篇的同名山 / homonyms across sections | — |
| `located`（框架句）| 任意 → 任意 | 「X之南，Y之濱，Z之後，W之前，有…名曰S」：S 在 X 之南；前／後依解讀規則 R5（前 = 東）/ frame clauses; 前／後 per rule R5 | 方位、另一慣例 / direction, alt_direction |
| `beside` | 任意 → 任意 | 「X之濱」 | — |
| `encircles` | WAT → 任意 | 「其下有X之淵環之」「X環之」 | — |
| `outside` | 任意 → 任意 | 「其外有X」 | — |

## 4. 觀察框架 / Observer frame（R9）
- 每篇山經以其首站為起點，依「又{方}{N}里」累計出相對路線；路線的**起點位置**與**比例尺**（里 → 公里）都是未知數，由求解決定，比例尺的先驗範圍很寬。/ Each section's route is built from its legs; its start and its li-to-km scale are unknowns.
- 篇名的方位（南山經、西山經…）與海經、大荒經的方位從原點理解，作為**軟約束**：方向相差越多扣分越多，但不能單獨否決。/ Book directions read from the origin as soft constraints.

### 4.1 篇段錨點 / Section anchors
在逐實體評分之前，先為每一篇判斷大致的位置（錨點）：候選地帶（含遠方對立候選）、起點與比例尺，依方位（斜向容許 ±67.5° 偏移）、路線與比例尺、地形外觀（山可為沙丘、貝殼堤、方山；水可為湖、沼澤、海灣）、水系結構、物產、動物逐項評分。錨點作為後續逐實體判斷的先驗與檢查，不是結論。/ Section-level anchors judged before entity-level scoring; a prior and a check, not a conclusion.

## 5. 時代世界庫與候選 / Era world base and candidates（步驟 4–5）

| 書中類型 / Text type | 候選 / Candidates | 卡片屬性 / Card attributes |
|---|---|---|
| 山 MTN、地 LND | **遺址與地景**：自然山脈與山峰、沙丘區、方山，與人工高大建築（神廟平臺、塔廟、金字塔、城牆、墓塚）；再彙總到地區 / sites and landforms, natural or built, rolled up to regions | 外觀、尺度、材質、顏色、物產、動植物、存在年代、當時樣貌、座標 |
| 水 WAT | 當時的河、湖、海、沼澤、運河（含已消失者）/ waters of the period | 顏色（泥沙、藻類）、流向與走向、與其他水的連接、存在年代 |
| 生物 CRE | 當時的動物（含已滅絕或已退出原分佈者），以及人工造像（如人面獸身像）/ animals of the period and statues | 形態、顏色、聲音、習性、當時分佈 |
| 國族 POL | 當時的人群與文化 / peoples of the period | 習俗、生業、外觀、地區、年代 |
| 神人 PER | 當時的神祇形象與造像（只在描述可比時）；否則不對應 / deity images where comparable | 形象、屬物、所在 |
| 植物、礦物 PLA、MIN | 詞義，加上當時的產地與貿易品（青金石、紅玉髓、錫、銅、和田玉、黃金）/ meaning plus period sources and trade goods | 產地、年代 |

- **候選生成**：`semantic-matcher` 只看遮蔽後的輸入（描述、名稱特徵、關係、原點方位），開放提出候選；每個實體至少 3 個候選、至少 2 個不同大區；兩河流域、哈拉帕、古埃及為重點，但必須同時提出其他同時期文明作為對立候選。新候選寫成卡片，附一般性來源，由 `civilization-scout` 或 `palaeo-geographer` 審核後入庫。/ Open, masked candidate generation with rivals; cards reviewed before entering the base.
- **對稱**：某類候選（例如運河、乾河谷、造像）只要加入，就要在全世界同類中一起加入。/ Symmetry.

## 6. 語義評分 / Semantic judgments（步驟 6）

**輸入（遮蔽）/ Masked input**：實體的原文描述（名稱以代號取代）、名稱特徵、關係摘要（「一端在甲山、東南延伸、與一大水相接」）、從原點的方位；候選卡。/ Description with names replaced, name features, relation summary, bearing from origin; the candidate card.

**維度與權重 / Dimensions and weights**（預設，可在敏感度中變動）：

| 維度 / dimension | 權重 / weight | 例 / example |
|---|---|---|
| 外觀與形狀 / appearance, shape | 1.0 | 「削成而四方」、「人面虎身」|
| 顏色 / colour | 0.8 | 「皆白」、名稱的「赤」|
| 尺度 / scale | 0.6 | 「其高五千仞」、「方八百里」|
| 材質與物產 / material, products | 0.8 | 「多玉」、「其陽多金」|
| 功能與行為 / function, behaviour | 0.8 | 「投物輒然」、「人舌能言」|
| 聲音 / sound | 0.5 | 「其音如吠犬」|
| 生態與分佈 / ecology, range | 0.8 | 物種在當時的分佈 |
| 方位 / bearing from origin | 0.4 | 書的方位與候選相對原點的方向 |
| 年代 / date | 硬條件 / hard | 窗口內不存在則不得為候選 |
| 名稱特徵 / name features | 0.4 | 名稱中的「赤」「黑」「白」「玉」 |

**每一維的輸出 / Per dimension**：吻合 0–1、`contradiction`（真／假）、原文證據（條目編號與原句）、候選屬性、一句理由。無資料時為 `null`（不計分，不扣分：缺失不算矛盾）。/ score, contradiction flag, evidence, attribute, reason; null when absent.

**自身分數 / Own score** = Σ 權重 × 吻合 × 罕見度 − Σ min(矛盾扣分, 0.5)；罕見度 = log₁₀(候選池大小 / 具有該屬性的候選數) + 0.1，由全部判斷統計。/ rarity-weighted agreement minus capped contradictions.

**取樣 / Sampling**：每個判斷 3 個樣本（不同的候選順序）；取平均與標準差；標準差 > 0.25 的維度降權。/ three samples; noisy dimensions down-weighted.

**傳承錯誤 / Transmission errors**（R11）：判斷時允許替代讀法（形近字、數字、錯簡），記為 `variant_reading` 並扣 0.1；所用讀法須來自見證本或明列的錯誤類型。/ variant readings at −0.1, sourced from witnesses or a stated error type.

## 7. 關係評分 / Relation judgments（步驟 7）
- **可計算的**（相鄰、方位、注入、發源、同區）：依時代地理的座標與連接直接計算：注入（候選的去處正是對方 +2.0、地圖讀法下反向相接 +1.5、同區 +0.3、否則 −1.0）、發源（一端在山的地區 +1.0、另一端 ×0.8、相鄰 +0.3、否則 −0.5）、相鄰站（同區 +0.3、相鄰區 +0.1、否則 −0.3）、方位（與書中方位相差 ≤ 67.5° 時 +0.2，否則 −0.1）；套用 R1–R6。/ Computable relations on period geography, with these weights.
- **需語義的**（環之、其外有、濱、望見、居、生）：由 `semantic-matcher` 判斷兩個候選在當時是否處於該關係，給 0–1 與理由。/ Semantic relations judged.
- 相鄰實體的候選年代不重疊時扣分（R8）：相差 ≤ 500 年不扣，> 1000 年扣 0.2。/ Date gaps between neighbours.

## 8. 聯合求解與可信度 / Joint solution and confidence
總分 E = Σ 自身分數 + Σ 關係分數 − 唯一性懲罰（兩個書中實體對到同一真實實體，每對 2.0）；以模擬退火（多條鏈、固定種子、一半提議由關係引導）、ICM 與區塊調整求最高；對應 = 總分最高的組態。可信度 = 穩定度（完整求解與略去 20% 關係的重解中一致的比例）× (1 − e^(−邊際)) × (1 − 判斷標準差) × 洩漏折扣（§9）。級別同框架。輸出逐位元組可重現。/ Energy, annealing with ICM and block moves, confidence with judgment spread and leakage; byte-reproducible.

## 9. 先入知識、誘餌與假說 / Leakage, decoys, hypotheses
- **洩漏檢測**：抽樣 10% 的實體，以不遮蔽的輸入再判一次；若最佳候選改變或分數差 > 0.3，標記 `leakage` 並把可信度乘以 0.5。/ 10% re-judged unmasked; differences flag leakage.
- **誘餌**：每批混入 5% 人工編造的描述（隨機組合書中常見特徵）；若誘餌被高分套到某個熱門候選，該候選的所有判斷降權並在紅隊中報告。/ 5% synthetic decoys per batch.
- **假說檢驗**：`era_sections.py`：一個解讀寫成固定組態（例：西次三經 = 古埃及），其餘全書重新求解，與自由解、對立組態、誘餌比較總分並列出被違反的關係；篇段 × 遺址或地區的掃描即當時的篇段地圖。/ Held configurations and section scans.

## 10. 交付 / Deliverable（`deliverables/draft-v4/`）
- `book/NN-書名.md`：逐段的原文、段內每個實體、對應、年代與當時樣貌、可信度與穩健度、主要吻合維度與證據、名稱特徵是否參與、洩漏標記；未對應的寫明原因。/ per paragraph.
- `entities.md` 與各類對應表；`coverage.md` 完整性檢查（段落數與提及數必須相等）。/ catalogue, tables, completeness check.
- **當時地圖** `era-map.svg`：約前 2500 年的海岸線與河道、撒哈拉乾濕界線、文明遺址與造物、中原原點與各篇的方位線，疊加對應與可信度。/ The era map.
- `hypotheses.md`：篇段掃描與聯合假說（含兩河流域、哈拉帕、古埃及的組態與對立組態）。

## 11. 覆蓋檢查 / Coverage audit
沿用：沒有實體的段落 0、未解釋的名稱句式 0；交付的完整性檢查 PASS。/ Unchanged.
