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

### 2.1 節點 `nodes.jsonl`
```json
{"id": "WAT:渭", "type": "WAT", "symbol": "渭", "variants": ["渭水"], "subtype": "river",
 "mentions": ["SHJ-02-4-018", "SHJ-13-1-022"], "descriptions": [{"entry": "SHJ-02-4-018", "text": "渭水出焉，而東流注于河"}],
 "props": {"flow_dir": "東", "n_inflows": 12, "dest_type": "river"}, "tags": [], "section": null,
 "name_features": {"kind": "water"}}
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
| `name_features` | 名稱中的語義特徵（顏色、材質、形狀、狀態、方位），不作辨識（T-V03 加入）/ name semantics, never identifiers |

### 2.2 邊 `edges.jsonl`
```json
{"src": "WAT:渭", "dst": "MTN:鳥鼠同穴之山", "type": "rises_at", "attrs": {}, "entry": "SHJ-02-4-018", "clause": "渭水出焉"}
```
邊的類型見 [methodology-spec](methodology-spec.md) §3。框架句的 `located` 另有 `alt_direction`（另一方位慣例）與 `convention`。/ Edge types in methodology-spec §3; frame-clause `located` edges also carry `alt_direction` and `convention`.

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
