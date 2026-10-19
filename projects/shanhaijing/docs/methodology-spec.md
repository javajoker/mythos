# 山海經實體圖譜交叉驗證規格 / Shanhaijing Entity-Graph Cross-Validation Spec

> v2.0 ・ 2026-10-19 ・ 實作 [Mythos 研究框架](../../../docs/research-framework.md)。這是本項目目前唯一的方法；舊方法（「方法 A」「方法 G」）已退役，保留在 git 歷史中。
> Implements the [Mythos research framework](../../../docs/research-framework.md). This is the project's only current method; earlier methods are retired and kept in git history.

---

## 0. 前提 / Premises
- 全書以整個地球為範圍；書中名稱只是符號。/ The whole Earth; names are symbols.
- 文本：以 `reference/shanhaijing/data/entries.jsonl`（869 段）為底，次序依工作文本（明成化本），讀法依 [source-assessment](source-assessment.md) §4 的草稿政策。/ 869 paragraphs; working-text order; draft-reading policy.

## 1. 流程 / Pipeline

| 步驟 / Step | 工具 / Tool | 輸出（`data/derived/`）/ Outputs |
|---|---|---|
| 0 文本層 / text layer | `ingest.py`, `collate.py`, `align_witness.py`, `classify_variants.py`, `extract_routes.py` | `entries.jsonl`, `working-text.jsonl`, `stations.jsonl` … |
| 1–2 實體、性質、關係 / entities, properties, relations | `tools/shj/kg_extract.py` | `kg/nodes.jsonl`, `kg/edges.jsonl`, `kg/mentions.jsonl`, `kg/shanhaijing.graphml`, `kg/coverage.md` |
| 3 真實世界候選 / candidates | `tools/shj/kg_candidates.py` | `kg/candidates.jsonl` |
| 4 交叉驗證 / cross-validation | `tools/shj/kg_crossval.py`（約 6 分鐘 / ~6 min） | `kg/mapping.jsonl`, `kg/crossval-log.json` |
| 4b 敏感度 / sensitivity | `tools/shj/kg_sensitivity.py` | `kg/sensitivity/sensitivity.md`, `robustness.jsonl` |
| 5 交付 / deliverable | `tools/shj/kg_deliver.py` | `projects/shanhaijing/deliverables/draft-v2/` |

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

## 3. 性質與關係 / Properties and relations（步驟 2）

**性質 / Properties**：由描述抽出的標籤，詞彙見 `tools/shj/cues.py`：生物的體型參照、部件、顏色、聲音、習性；地點的礦產、植物、地形、氣候；國族的習俗、食物。/ Tags from descriptions (vocabulary in `cues.py`).

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

## 4. 真實世界候選 / Real-world candidates（步驟 3）

| 書中類型 / Text type | 候選庫 / Candidate base | 自身分數依據 / Own-score basis |
|---|---|---|
| 生物 CRE | `world/animals.jsonl`（116 種，含特徵與古代分佈），外加「無」（自身分數 0.35）| 描述特徵的稀有度加權覆蓋率；鳥、魚與身體形態檢查 / rarity-weighted coverage of description tags, with bird/fish and body checks; 'none' own score 0.35 |
| 山 MTN、地 LND | `world/regions.jsonl`（31 個地區）＋ `region-properties.jsonl` | 該山的物產、生物、地形與地區性質的吻合 / resources, creatures and terrain vs region properties |
| 水 WAT（主要水體）| `world/waters.jsonl`（135 個全球河、湖、海、沙漠終點，含河源地區、河口、流域、流向），外加「庫中沒有」| 類型、流向、終點類型、規模（小權重）；「庫中沒有」的成本 = min(0.1 × 支流數, 1.5) / type, flow direction, destination type, size (small); 'none' costs min(0.1 × inflows, 1.5) |
| 國族 POL | `world/cultures.jsonl`（47 個全球古代人群，含習俗、地區），外加「證據不足」| 習俗、生業的稀有度加權（只計該族作主語的句子）/ rarity-weighted customs and livelihood, subject clauses only |
| 植物 PLA、礦物 MIN | 普通名詞的詞義（`kg_common.LEXICAL`）；專名不對應 / lexical meaning of common nouns; proper names unmapped | 亦作為山的性質使用 / also used as mountain properties |
| 神人 PER | 無（非地理實體）/ none (non-geographic) | 不對應，但保留在圖中 / not mapped, kept in the graph |

**主要水體 / Major waters**：收納 ≥ 2 條書中之水、提及 ≥ 3 次、為海或湖澤，或有完整的出入記錄（例如海內東經水道表）者，逐一對應真實水體。其餘小溪不單獨對應，只作為關係（它的源山與它所注入的水）參與交叉驗證。/ Major waters (≥ 2 inflows, seas, marshes, or in the 海內東經 waterway list) are mapped individually; minor streams take part only through their relations.

## 5. 交叉驗證 / Cross-validation（步驟 4）

| 邊 / Edge | 一致 / Consistent | 權重 / Weight |
|---|---|---|
| `flows_into`（兩端皆主要水體）| 候選 A′ 的河口正是 B′ / A′'s mouth is B′ | +2.0；同地區 +0.3；否則 −1.0；A′＝B′（自注）−2.0；B′ 為「庫中沒有」而 A′ 的真實河口在庫中 −1.0 |
| `flows_into`（→ 泛稱的海；→ 流沙等地）| A′ 入海 / A′ 為內流或沒入沙漠 | ±0.5；+0.5 / −0.3 |
| `sinks_at` | A′ 為內流或沒入沙漠 / endorheic or ends in desert | +0.3 / −0.2 |
| `rises_at`（主要水體 → 山）| A′ 的河源地區＝山的候選地區 / source region = the mountain's region | +1.0；相鄰 +0.3；否則 −0.5 |
| 小溪的 `rises_at` ＋ `flows_into` | 源山的候選地區屬於所注入水體 B′ 的流域地區 / the source mountain's region lies in B′'s basin | +0.6；否則 −0.3 |
| `next` | 兩山同一地區 +0.3、相鄰 +0.1、否則 −0.3（距離只是參考）/ same region, adjacent, otherwise | ≤ 0.3 |
| `has_creature` | 動物的分佈涵蓋山的候選地區 / the animal's range covers the region | +0.5 × 覆蓋率；否則 −0.25 × 覆蓋率（海洋動物免檢）|
| `located`、`sees` | 兩端候選中心點的方位與書中方位相差 ≤ 67.5° / bearing agrees within 67.5° | +0.2 / −0.1（`sees` ±0.1 / −0.05）|

**唯一性 / Uniqueness**：兩條書中河流對到同一條真實水體，每對扣 2.0。/ 2.0 per pair of book waters on one real water.

**求解 / Solve**：模擬退火 6 條鏈 × 120 萬步（溫度 2.0 → 0.02，固定種子；一半提議由關係引導），ICM 收尾（平手保留現值），再做區塊調整：一條河設為某候選，同時重配相鄰的河、它們的源山及源山的鄰站，總分上升才接受。對應＝總分最高的鏈。樣本：6 條完整鏈＋12 次「略去 20% 關係」的重解（各 2 條鏈），共 30 個。/ Simulated annealing (6 chains × 1.2M steps, T 2.0 → 0.02, fixed seeds, half the proposals relation-guided), ICM polish, then block moves (a river with its neighbouring rivers, source mountains and their stations; kept only if E rises). Mapping = the best chain. 30 samples: 6 full chains plus 12 re-solves with 20% of relations dropped (2 chains each).

**可信度 / Confidence** = 穩定度 × (1 − e^(−邊際))；高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、暫定 < 0.1。每個對應都列出支持與違反的關係、樣本中的其他候選及比例；河流另報水系層級的穩定度。/ High, medium, low, tentative; every mapping lists supporting and violated relations and sample alternatives; rivers also report system-level stability.

## 6. 交付 / Deliverable（步驟 5）

`deliverables/draft-vN/`（目前 / current: `draft-v2`；每個對應附「權重變體 k/16」/ each mapping shows its weight robustness）：
- `README.md`：方法摘要、結果摘要、可信度分佈、限制。/ summary, results, confidence, limits.
- `book/NN-書名.md`：**逐段對照**：每一段的原文、其中每個實體、對應的真實世界實體、可信度與理由。869 段一段不漏。/ **per-paragraph mapping** for all 869 paragraphs.
- `entities.md`：全部實體的總表（依類型），含描述、性質、關係數、對應與可信度。/ the full entity catalogue.
- `mapping-waters.md`、`mapping-mountains.md`（依篇）、`mapping-creatures.md`、`mapping-peoples.md`、`mapping-plants-minerals.md`：各類對應表。/ tables by type.
- `world-map.svg`：全球圖。/ world map.
- `coverage.md`：交付完整性檢查：段落數、提及數與寫入的列數必須相等（PASS），否則 `kg_deliver.py` 失敗。/ completeness check: paragraphs and mentions written must equal those in the text, or the tool fails.
- `summary.json`：統計。/ counts.

## 7. 覆蓋檢查 / Coverage audit
`kg_extract.py` 產出 `coverage.md`：(1) 每段抽到的實體數；(2) 沒有任何實體的段落；(3) 名稱句式出現但未抽出的地方，每一處要嘛已成實體，要嘛歸入明列的理由（數量、題記、泛稱、比喻、異說、敘事語）。交付前，(2) 與 (3) 的「未解釋」必須為零。/ Paragraphs with no entity and unextracted name patterns must be zero or individually explained before delivery.
