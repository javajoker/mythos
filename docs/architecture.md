# 架構 / Architecture

> v2.0 ・ 2026-10-19

## 1. 分層 / Layers

```
            ┌──────────────────────────── docs/ ────────────────────────────┐
            │ whitepaper · prd · research-framework · conventions · glossary │
            └────────────────────────────────────────────────────────────────┘
 reference/<corpus>/          tools/<corpus>/                  projects/<corpus>/
 ┌──────────────────┐  ingest ┌──────────────────┐   derive   ┌──────────────────────────┐
 │ sources/<witness>│ ──────▶ │ text layer       │ ─────────▶ │ data/derived/ (text)     │
 │ data/entries     │         │ kg_extract       │ ─────────▶ │ data/derived/kg/ (graph) │
 │ text/*.md        │         │ kg_candidates  ◀─┼─ world ─── │ data/world/ (real world) │
 └──────────────────┘         │ kg_crossval      │ ─────────▶ │ kg/mapping.jsonl         │
                              │ kg_deliver       │ ─────────▶ │ deliverables/draft-vN/   │
                              └──────────────────┘            └──────────────────────────┘
                     .claude/agents + .claude/skills（公共層 + 子項目層 / common + sub-project）
```

- `reference/` 只放原文和忠實的結構化轉寫，**不放詮釋**。/ Source texts and faithful transcriptions only, **no interpretation**.
- `projects/<corpus>/data/world/` 是真實世界庫，在計分之前提交。/ The real-world base, committed before scoring.
- `projects/<corpus>/data/derived/` 全部可由 `tools/` 重新產生；`deliverables/` 是交付版本（也由工具產生）。/ Everything derived is regenerable; deliverables are tool-generated too.
- `tools/` 是確定性的腳本，只用標準庫，固定隨機種子，輸出逐位元組可重現。/ Deterministic, standard-library scripts with fixed seeds.

## 2. 流程與代理分工 / Pipeline and roles

| 步驟 / Step | 主責 / Lead | 支援 / Support | Skill | 山海經工具 / SHJ tool |
|---|---|---|---|---|
| 0 語料與校勘 / Corpus and collation | `textual-critic` | — | `source-ingest`, `witness-collation` | `fetch_sources`, `ingest`, `collate`, `align_witness`, `classify_variants`, `extract_routes` |
| 1–2 實體、性質、關係 / Entities, properties, relations | `entity-extractor` | `textual-critic` | `entity-graph-extraction` | `kg_extract`（`cues`）|
| 3 真實世界候選 / Candidates | `world-candidate-scout` | — | `world-candidate-generation` | `kg_candidates`（`kg_common`）|
| 4 交叉驗證 / Cross-validation | `cross-validator` | `devils-advocate` | `graph-cross-validation` | `kg_crossval`, `kg_sensitivity` |
| 5 交付 / Deliverable | `shj-lead` | `devils-advocate` | `shj-entity-mapping` | `kg_deliver` |
| 全程協調 / Orchestration | `shj-lead` | 全部 / all | `shj-entity-mapping` | — |

## 3. Agent 與 Skill 清單 / Catalogue

| 層 / Layer | 類型 / Kind | 名稱 / Name | 用途 / Purpose |
|---|---|---|---|
| 公共 Common | agent | [textual-critic](../.claude/agents/textual-critic.md) | 校勘、引文核對、工作文本 / collation, quotation checks, working text |
| 公共 Common | agent | [entity-extractor](../.claude/agents/entity-extractor.md) | 實體、性質、關係與覆蓋檢查 / entities, properties, relations, coverage audit |
| 公共 Common | agent | [world-candidate-scout](../.claude/agents/world-candidate-scout.md) | 真實世界庫與候選、庫的平衡 / world base, candidates, balance |
| 公共 Common | agent | [cross-validator](../.claude/agents/cross-validator.md) | 聯合求解、可信度、確定性與一致性檢查 / joint solve, confidence, checks |
| 公共 Common | agent | [devils-advocate](../.claude/agents/devils-advocate.md) | 紅隊 / red team |
| 公共 Common | skill | [source-ingest](../.claude/skills/source-ingest/SKILL.md) | 新語料入庫 / onboard a corpus |
| 公共 Common | skill | [witness-collation](../.claude/skills/witness-collation/SKILL.md) | 見證本對勘與異文分類 / collation and variant classes |
| 公共 Common | skill | [entity-graph-extraction](../.claude/skills/entity-graph-extraction/SKILL.md) | 步驟 1–2 / steps 1–2 |
| 公共 Common | skill | [world-candidate-generation](../.claude/skills/world-candidate-generation/SKILL.md) | 步驟 3 / step 3 |
| 公共 Common | skill | [graph-cross-validation](../.claude/skills/graph-cross-validation/SKILL.md) | 步驟 4 / step 4 |
| 山海經 SHJ | agent | [shj-lead](../.claude/agents/shj-lead.md) | 子項目主持 / sub-project lead |
| 山海經 SHJ | skill | [shj-entity-mapping](../.claude/skills/shj-entity-mapping/SKILL.md) | 流程 runbook、回答「X 在哪裡」/ runbook, "where is X" |

## 4. 公共層與子項目層 / Common vs sub-project

| 公共（與語料無關）/ Common | 山海經專用 / Shanhaijing-specific |
|---|---|
| 五個步驟、計分公式、可信度與級別、完整性規則（`docs/research-framework.md`）/ steps, scoring, confidence, completeness | 實體句式（曰X之山、X水出焉、注于X…）、異體摺疊、`cues.py` 詞彙 / sentence patterns, glyph folding, cue vocabulary |
| 求解器設計（退火、ICM、區塊調整、丟棄重解）/ solver design | 關係權重（規格 §5）、唯一性 2.0、主要水體的定義 / relation weights, uniqueness, major-water rule |
| 真實世界庫的格式（地區、性質、水體、動物、文化）/ world-base schemas | 庫的內容（31 地區、135 水體、116 動物、47 文化）/ base contents |
| 紅隊檢查 / red-team checks | 交付格式（`book/NN-書名.md`）/ deliverable layout |

## 5. 退役紀錄 / Retirement record (2026-10-19)

實體圖譜交叉驗證取代了先前的兩個方法；它們的檔案已刪除，保留在 git 歷史中（`git log --diff-filter=D --stat` 可查）。
Entity-graph cross-validation replaced the two earlier methods; their files are deleted and remain in git history (`git log --diff-filter=D --stat`).

| 退役項目 / Retired | 種類 / Kind | 原因 / Reason |
|---|---|---|
| 方法 A（S0–S9 假說卷宗、證據分級、校改預算、裁決）/ Method A | 方法 / method | 以單一假說為中心，不以全書為基準 / hypothesis-centred, not whole-book |
| 方法 G（描述優先的地點比對、地區性質比對）/ Method G | 方法 / method | 逐地比對，沒有實體之間的交叉驗證 / per-place matching without cross-validation |
| `chain_fit.py`, `calibrate.py`, `river_graph.py`, `geo_match.py`, `region_match.py`, `animal_map.py`, `creatures.py` | 工具 / tools | 由 `kg_*.py` 取代 / superseded by `kg_*.py` |
| `loci.jsonl`, `data/geo/anchors-*.jsonl`, `animal-map.*`, `creatures.jsonl`, `global-map.*`, `peoples-map.md`, `river-graph.*` | 資料 / data | 同上 / same |
| `hypotheses/H-0001…H-0006`、`reports/draft-v0.1.md`、`reports/draft-v1.0-global.md`、`findings/F-0003`、`F-0004`、`docs/method-g-global.md` | 文檔與交付 / docs and deliverables | 由 `deliverables/draft-v2/` 取代 / superseded |
| `deliverables/draft-v1/` | 交付 / deliverable | 紅隊審查 R1 撤回其主要結論，由 draft-v2 取代 / withdrawn by review R1, superseded by draft-v2 |
| agents `adjudicator`, `geo-triangulator`, `naturalist`, `shj-route-reconstructor`；skills `hypothesis-adjudication`, `toponym-triangulation`, `biogeo-identification`, `description-first-matching`, `shj-hypothesis-case`, `shj-itinerary-reconstruction`, `shj-global-locate` | 代理與技能 / agents and skills | 由新的公共層取代 / replaced by the new common layer |

## 6. 新語料接入 / Adding a corpus

1. 依 `source-ingest` 建立 `reference/<corpus>/` 和 `tools/<corpus>/`。/ Create both per `source-ingest`.
2. 寫 `projects/<corpus>/docs/methodology-spec.md`，只寫專用部分：實體句式、關係權重、交付格式。/ A spec with only the specific parts.
3. 建立或擴充真實世界庫；其他一律重用公共層。/ Build or extend the world base; reuse the common layer for everything else.
