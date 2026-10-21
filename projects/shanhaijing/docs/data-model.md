# 資料模型 / Data Model

所有資料為 JSONL（每行一筆）、UTF-8，鍵名英文，值保留原文。/ JSONL, UTF-8, English keys, source-language values.

## 1. 文本層 / Text layer

| 檔案 / File | 內容 / Content |
|---|---|
| `reference/shanhaijing/data/entries.jsonl` | 869 段，`id` = `SHJ-BB-S-EEE`；`text`、`notes[]`、`variants[]`、`editorial_refs[]` |
| `data/derived/working-text.jsonl` | 依明成化本次序的段落序列 / paragraphs in Chenghua order |
| `data/derived/variant-classes.jsonl` | 異文與分類；人工判定在 `ledgers/variant-overrides.jsonl` / variants and classes |
| `data/derived/stations.jsonl`, `sections.jsonl` | 山經站點、方位、里數、水系；篇末總數 / Mountain stations and section totals |

注疏（`notes[]`）保存在 `entries.jsonl` 中只為完整轉錄，**不進入任何分析步驟**。/ Commentary is kept only as transcription and never enters analysis.

## 2. 知識圖譜 / Knowledge graph（`data/derived/kg/`）

### 2.0 核心本體公理 (Core Ontology Axioms)
1. **【無新地理實體公理】**：
   - 《五臧山經》（卷一至五）是全書唯一的客觀地理空間底座，所有地理實體節點（`MTN`, `WAT`, `LND`）首發於此，標記 `is_geography_base: true`。
   - 卷六至卷十八純屬人文與特產，絕無新地理內容。卷六至卷十八出現的所有山、水實體，**100% 複用五臧山經的實體節點與地理坐標**，標記 `reused_from_shanjing: true`。
   - 卷六至卷十八的人文與特產實體（`POL`, `PER`, `CRE`, `PLA`, `OBJ`, `AST`），通過 `anchored_shanjing_id` 邊或屬性直接錨定於五臧山經對應的地理底座節點之上。
2. **【拋棄後世注釋·文字出發】**：
   - 徹底拋棄郭璞注等後世狹隘微縮注疏，嚴格依據經文字面全球尺度實證：
     - 開羅吉薩金字塔群 ≡ 崑崙之丘；
     - 吉薩獅身人面像 ≡ 神陸吾 / 開明獸；
     - 紅海 ≡ 赤水；
     - 尼羅河 ≡ 黑水；
     - 地中海與北非板塊 ≡ 西次三經。

### 2.1 節點 `nodes.jsonl`
```json
{"id": "MTN:SHJ-02-3-006-崑崙之丘", "type": "MTN", "canonical_name": "崑崙之丘", "is_geography_base": true,
 "coordinates_era": [30.0, 31.2], "era_entity": "埃及開羅吉薩高地金字塔群", "temporal_state": "living",
 "mentions": ["SHJ-02-3-006", "SHJ-11-1-010", "SHJ-16-1-020"],
 "associative_properties": ["帝之下都", "法老王陵", "天門樞紐"],
 "deductive_properties": ["花崗岩與石灰岩巨石台", "高萬仞", "面有九門"]}
```
| 鍵 / Key | 說明 / Meaning |
|---|---|
| `id` | `類型:條目編號-符號`（如 `MTN:SHJ-02-3-006-崑崙之丘`）/ Unique node identifier |
| `type` | MTN 山、WAT 水、LND 地、POL 國族、CRE 生物、PLA 植物、MIN 礦物、PER 神人、OBJ 器物、AST 天象、CLIM 氣候 |
| `canonical_name` | 規範正體名稱（原始經文）/ Canonical source name |
| `is_geography_base` | 布爾值（是否屬於五臧山經地理底座，`true` 僅限卷一至五山水）/ Is Wuzang Shanjing base |
| `reused_from_shanjing` | 布爾值（卷六至十八山水實體強制為 `true`，複用山經節點）/ Reused from Shanjing |
| `anchored_shanjing_id` | 若為卷六至十八的人文/特產實體，必須指向五臧山經錨定節點 ID / Anchor Mountain/Water ID |
| `coordinates_era` | 4000–1000 BCE 時代地理坐標 `[lat, lon]` / Era coordinates |
| `era_entity` | 考古遺址、古生物化石或時代古水文對位實體 / Archaeological or paleo-entity |
| `associative_properties` | 聯想性圖騰信仰與文化屬性列表 / Associative cultural properties |
| `deductive_properties` | 演繹性生態適應、工藝材料與理化功能列表 / Deductive functional properties |
| `mentions` | 出現的全部條目編號（含跨卷複用引用）/ All entry mentions across 18 books |

### 2.2 邊 `edges.jsonl`
```json
{"src": "PER:SHJ-16-1-020-西王母", "dst": "MTN:SHJ-02-3-006-崑崙之丘", "type": "anchored_to", "attrs": {"role": "穴居主天之厲"}, "entry": "SHJ-16-1-020"}
```
邊的類型包括：`anchored_to`（人文特產錨定於山經地理底座）、`rises_at`（發源）、`flows_into`（注入）、`adjacent_to`（相鄰）、`same_entity_as`（同一實體跨卷同一）、`produces`（出產物候）、`inhabits`（棲居生息）、`worships`（祭祀奉祠）、`invented_by`（科技發明）。

### 2.3 提及 `mentions.jsonl`
每段一行，列出該段抽出的全部實體 ID；這是逐段對照的骨架。/ One line per paragraph listing every entity extracted from it — the backbone of the per-paragraph deliverable.
```json
{"entry": "SHJ-02-3-006", "nodes": ["MTN:泰器之山", "WAT:觀水", "LND:流沙", "CRE:文鰩魚", "WAT:西海", "WAT:東海"]}
```

## 3. 時代世界庫 / Era world base（`data/era/`，提交於計分之前 / committed before scoring）
| 檔案 / File | 內容 / Content |
|---|---|
| `sites.jsonl` | 遺址、地景與造物卡：`id`, `kind`（`natural` 山、沙丘、方山…／`built` 神廟、塔廟、金字塔、城、墓塚、運河、造像）、`region`, `pt`, `from`, `to`（存在年代，負數為公元前）, `state`（`living`／`ruin`／`gone`）, `attributes`（外觀、尺度、材質、顏色、功能、朝向）, `source` |
| `waters-era.jsonl` | 當時的水體：沿用 `waters.jsonl` 欄位，加 `from`, `to`, `colour`（泥沙、藻類）, `state_note`（例：波斯灣頂端在烏爾附近）|
| `fauna-era.jsonl` | 當時的動物分佈（含已滅絕或已退出原分佈者）：沿用 `animals.jsonl`，加 `range_era`（窗口內的分佈）, `extinct_after` |
| `cultures-era.jsonl` | 當時的人群與文化：`from`, `to`, 習俗、生業、外觀 |
| `palaeo-coast.json` | 約前 2500 年的海岸線、河道與撒哈拉乾濕界線，只用於繪圖 / drawing only |
| `regions.jsonl` | 33 個彙總用大區：`code`, `name`, `lat`, `lon`, `adjacent`（對稱）/ roll-up regions |
| `region-properties.jsonl` | 大區屬性：`prop`, `group`, `true`, `false`, `source` / region attributes |
| `coastlines-present.json` | 今日的簡化陸地輪廓，繪圖底圖 / present outlines for drawing |

現況與待辦見 [`data/era/README.md`](../data/era/README.md)。/ Current state in data/era/README.md.

## 4. 判斷紀錄 / Judgment records（`data/derived/era/judgments.jsonl`）
```json
{"node": "WAT:赤", "cand": "water:red_sea", "sample": 1, "masked": true,
 "input_hash": "…", "model": "claude-opus-5-5", "prompt_version": "sem-1.0",
 "dims": {"colour": {"score": 0.7, "contradiction": false, "evidence": ["name:赤"], "attribute": "seasonal Trichodesmium blooms, red coastal rocks", "reason": "…"},
          "shape":  {"score": 0.8, "contradiction": false, "evidence": ["SHJ-02-3-008:赤水出焉，東南流注于氾天之水"], "attribute": "NW–SE axis, opens to the Arabian Sea", "reason": "…"},
          "date":   {"score": 1.0, "contradiction": false, "evidence": [], "attribute": "present throughout", "reason": "…"}},
 "variant_reading": null, "leakage_probe": false}
```
- 每個實體與候選至少 3 個樣本；`input_hash` 不變則不重判。/ At least three samples; re-judged only when the input changes.
- `relation-judgments.jsonl`：`{"edge": …, "a_cand": …, "b_cand": …, "score": 0–1, "reason": …, "sample": n}`。
- `candidates.jsonl`：大模型提出的候選與理由；`frame.jsonl`：每站的累計位置（東 x、北 y，單位里）；`profiles.jsonl`：各篇的路線、地形、物產、水與生物；`anchors.jsonl`：篇段錨點的判斷（每篇的候選、起點、比例尺、逐維度分數、證據、理由、洩漏風險）；`benchmarks.jsonl`：基準點的判斷（實體、書中段落、各來源的候選與座標、描述／關係／比例尺／聯想的分數與理由、可否定的檢驗）。/ Proposed candidates; the observer frame.

## 5. 對應 / Mapping（`data/derived/era/mapping.jsonl`）
```json
{"node": "WAT:赤", "cand": "water:red_sea", "period": [-4000, -2000], "state": "living", "confidence": 0.41, "tier": "medium",
 "margin": 1.3, "stability": 0.7, "judgment_sd": 0.08, "leakage": false, "name_feature_used": true,
 "dims_top": [{"dim": "shape", "score": 0.8, "evidence": "SHJ-02-3-008"}],
 "alternatives": [{"cand": "water:kizilirmak", "share": 0.2}], "supported_by": [], "violated": [], "status": "mapped"}
```
`status`：`mapped`、`unmapped:no-candidate`、`unmapped:non-geographic`、`unmapped:insufficient`、`unmapped:structural`、`unmapped:undetermined`。可信度級別：高 ≥ 0.6、中 ≥ 0.3、低 ≥ 0.1、暫定 < 0.1。/ statuses and tiers.

## 6. 帳簿 / Ledgers
- `ledgers/variant-overrides.jsonl`：人工異文判定，永遠優先 / human variant decisions, always win.
