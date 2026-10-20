# 資料模型 / Data Model

所有資料為 JSONL（每行一筆）、UTF-8，鍵名英文，值保留原文。/ JSONL, UTF-8, English keys, source-language values.

## 1. 文本層 / Text layer

| 檔案 / File | 內容 / Content |
|---|---|
| `reference/shanhaijing/data/entries.jsonl` | 869 段，`id` = `SHJ-BB-S-EEE`；`text`、`notes[]`、`variants[]`、`editorial_refs[]` |
| `data/derived/working-text.jsonl` | 依明成化本次序的段落序列 / paragraphs in Chenghua order |
| `data/derived/variant-classes.jsonl` | 異文與分類；人工判定在 `ledgers/variant-overrides.jsonl` / variants and classes |
| `data/derived/stations.jsonl`, `sections.jsonl` | 山經站點、方位、里數、水系；篇末總數 / Mountain stations and section totals |

## 2. 知識圖譜 / Knowledge graph（`data/derived/kg/`）

### 2.1 節點 `nodes.jsonl`
```json
{"id": "WAT:渭", "type": "WAT", "symbol": "渭", "variants": ["渭水"], "subtype": "river",
 "mentions": ["SHJ-02-4-018", "SHJ-13-1-022"], "descriptions": [{"entry": "SHJ-02-4-018", "text": "渭水出焉，而東流注于河"}],
 "props": {"flow_dir": "東", "n_inflows": 12, "dest_type": "river"}, "tags": [], "section": null}
```
| 鍵 / Key | 說明 / Meaning |
|---|---|
| `id` | `類型:符號`，同名異實體加 `#n`（例如 `MTN:陰山#2`、`WAT:洛#2`）/ `TYPE:symbol`, `#n` for homonyms |
| `type` | MTN 山、WAT 水、LND 地、POL 國族、CRE 生物、PLA 植物、MIN 礦物、PER 神人 |
| `symbol` | 書中的名稱（只是符號，不參與計分）/ the text's name (a symbol only, never scored) |
| `mentions` | 出現的全部條目編號 / every entry where it appears |
| `descriptions` | 描述它的原文片段 / source clauses describing it |
| `props`, `tags` | 從描述得到的性質與標籤 / properties and tags from descriptions |
| `section` | 山經站點所屬的篇 / section of a Mountain station |

### 2.2 邊 `edges.jsonl`
```json
{"src": "WAT:渭", "dst": "MTN:鳥鼠同穴之山", "type": "rises_at", "attrs": {}, "entry": "SHJ-02-4-018", "clause": "渭水出焉"}
```
邊的類型見 [methodology-spec](methodology-spec.md) §3。框架句的 `located` 另有 `alt_direction`（另一方位慣例）與 `convention`。/ Edge types in methodology-spec §3; frame-clause `located` edges also carry `alt_direction` and `convention`.

### 2.6 篇段與假說檢驗 / Section and hypothesis tests（`kg/sections/`）
- `scan.jsonl`：每個固定組態一行：`name`、`energy`、`n_fixed`、`violated`、`violated_score`、`violated_top`、`key`。/ one line per held configuration.
- `section-best.json`：每一篇的地區排名與 ΔE。/ region ranking per section.
- `sections.md`：報告。/ report.

### 2.3 提及 `mentions.jsonl`
每段一行，列出該段抽出的全部實體 ID；這是逐段對照的骨架。/ One line per paragraph listing every entity extracted from it — the backbone of the per-paragraph deliverable.
```json
{"entry": "SHJ-02-3-006", "nodes": ["MTN:泰器之山", "WAT:觀水", "LND:流沙", "CRE:文鰩魚", "WAT:西海", "WAT:東海"]}
```

### 2.4 候選 `candidates.jsonl`
```json
{"node": "CRE:文鰩魚", "candidates": [{"cand": "animal:flying_fish", "own": 0.60, "why": ["body_fish", "wings", "flies_night"]}]}
```
候選 ID 前綴 / candidate prefixes：`region:`（33 區）、`water:`、`culture:`、`animal:`、`plant:`、`mineral:`。

### 2.5 對應 `mapping.jsonl`
```json
{"node": "WAT:渭", "cand": "water:wei", "confidence": 0.82, "tier": "high", "margin": 2.4, "stability": 1.0,
 "alternatives": [{"cand": "water:blue_nile", "total": 1.1}],
 "supported_by": [{"edge": "flows_into", "to": "WAT:河", "entry": "SHJ-02-4-018"}],
 "violated": [], "status": "mapped"}
```
`status`：`mapped`、`unmapped:no-candidate`、`unmapped:non-geographic`（神人）、`unmapped:insufficient`（證據不足）、`via-relations`（小溪：不單獨對應，只透過關係）。

## 3. 真實世界庫 / Real-world base（`data/world/`）

| 檔案 / File | 內容 / Content |
|---|---|
| `animals.jsonl` | 真實動物：特徵標籤、古代分佈區、來源 / animals with tags, ancient ranges, sources |
| `regions.jsonl` | 31 個地區、中心座標、相鄰地區 / 31 regions, centroids, adjacency |
| `region-properties.jsonl` | 36 項地區性質（礦產、植物、地形、習俗）的 T／F 地區 / region properties |
| `waters.jsonl` | 全球河湖海：類型、河源地區、河口、流域地區、流向（海為軸向）、長度、是否內流、`era`（`palaeo` 為古水體）/ rivers, lakes, seas worldwide, with `era` for former waters |
| `cultures.jsonl` | 全球古代人群：地區、中心點、習俗與食物標籤 / ancient peoples worldwide |

## 4. 帳簿 / Ledgers
- `ledgers/variant-overrides.jsonl`：人工異文判定，永遠優先 / human variant decisions.
- `ledgers/mapping-overrides.jsonl`（**尚未實作**，人工審查已取消）：人工對應判定，必須寫理由 / (**not implemented**; human review is cancelled) human mapping decisions with reasons.

## 5. 時代語義版 / Era-semantic version（規格 v3，`draft-v4`）

### 5.1 時代世界庫 / Era world base（`data/era/`，提交於計分之前 / committed before scoring）
| 檔案 / File | 內容 / Content |
|---|---|
| `sites.jsonl` | 遺址、地景與造物卡：`id`, `kind`（`natural` 山、沙丘、方山…／`built` 神廟、塔廟、金字塔、城、墓塚、運河、造像）、`region`, `pt`, `from`, `to`（存在年代，負數為公元前）, `state`（`living`／`ruin`／`gone`）, `attributes`（外觀、尺度、材質、顏色、功能、朝向）, `source` |
| `waters-era.jsonl` | 當時的水體：沿用 `waters.jsonl` 欄位，加 `from`, `to`, `colour`（泥沙、藻類）, `state_note`（例：波斯灣頂端在烏爾附近）|
| `fauna-era.jsonl` | 當時的動物分佈（含已滅絕或已退出原分佈者）：沿用 `animals.jsonl`，加 `range_era`（窗口內的分佈）, `extinct_after` |
| `cultures-era.jsonl` | 當時的人群與文化：`from`, `to`, 習俗、生業、外觀 |
| `palaeo-coast.json` | 約前 2500 年的海岸線、河道與撒哈拉乾濕界線，只用於繪圖 / drawing only |

### 5.2 判斷紀錄 / Judgment records（`data/derived/era/judgments.jsonl`）
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
- `candidates.jsonl`：大模型提出的候選與理由；`frame.jsonl`：每站從原點的方位與累計里數。/ Proposed candidates; the observer frame.

### 5.3 對應 / Mapping（`data/derived/era/mapping.jsonl`）
沿用 §2.5，另加 / as §2.5 plus：`period`（候選的年代）、`dims_top`（主要吻合維度與證據）、`name_feature_used`、`judgment_sd`、`leakage`。
