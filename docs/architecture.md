# 架構 / Architecture

> v3.0 ・ 2026-10-20 ・ 對應研究框架 v3（時代語義對應）。先前的方法、工具與交付只保留在 git 歷史中。
> For framework v3. Earlier methods, tools and drafts are in git history only.

## 1. 分層 / Layers

```
            ┌──────────────────────────── docs/ ────────────────────────────┐
            │ whitepaper · prd · research-framework · conventions · glossary │
            └────────────────────────────────────────────────────────────────┘
 reference/<corpus>/          tools/<corpus>/                    projects/<corpus>/
 ┌──────────────────┐ ingest ┌───────────────────┐   derive   ┌──────────────────────────────┐
 │ sources/<witness>│ ─────▶ │ text layer        │ ─────────▶ │ data/derived/ (text layer)   │
 │ data/entries     │        │ kg_extract        │ ─────────▶ │ data/derived/kg/ (graph)     │
 │ text/*.md        │        │ era_* (pilot)     │ ◀── era ── │ data/era/ (world of period)  │
 └──────────────────┘        └───────────────────┘ ─────────▶ │ data/derived/era/ (judgments,│
                                       ▲                       │   mapping) · deliverables/   │
                    .claude/agents: semantic-matcher …         └──────────────────────────────┘
```

- `reference/` 只放原文和忠實的結構化轉寫，**不放詮釋**；注疏只作為轉錄保存，不進入分析。/ Sources and faithful transcriptions only; commentary is never analysed.
- `data/era/` 是時代世界庫，在計分之前提交。/ The era world base, committed before scoring.
- `data/derived/` 與 `deliverables/` 全部由工具與判斷紀錄產生。/ Everything derived comes from tools and judgment records.
- 工具只用標準庫，固定種子，輸出可重現；大模型的判斷存成紀錄，輸入不變不重判。/ Standard-library tools; LLM judgments are recorded and re-run only on change.

## 2. 流程與代理分工 / Pipeline and roles

| 步驟 / Step | 主責 / Lead | 支援 / Support | Skill | 山海經工具 / SHJ tool |
|---|---|---|---|---|
| 0 原始文本 / original text | `textual-critic` | — | `source-ingest`, `witness-collation`, `transmission-error-tolerance` | `fetch_sources`, `ingest`, `collate`, `align_witness`, `classify_variants`, `extract_routes` |
| 1–2 實體、關係、名稱語義 / entities, relations, name semantics | `entity-extractor` | `textual-critic` | `entity-graph-extraction`, `name-semantics` | `kg_extract`（`cues`）|
| 3 觀察框架 / observer frame | `cross-validator` | — | `observer-frame` | `era_frame`（待建）|
| 4 時代世界 / era world | `civilization-scout`, `palaeo-geographer` | — | `era-world-modelling` | `data/era/` |
| 5–7 候選與語義評分 / candidates and judgments | `semantic-matcher` | `civilization-scout` | `semantic-correlation-matching` | `era_tasks`, `era_relations`（待建）|
| 8–9 求解、可信度、假說 / solving, confidence, hypotheses | `cross-validator` | `devils-advocate` | `graph-cross-validation` | `era_solve`, `era_sensitivity`, `era_sections`, `era_leakage`（待建）|
| 10 交付與當時地圖 / deliverable and era map | `shj-lead` | `devils-advocate`, `palaeo-geographer` | `shj-era-mapping` | `era_deliver`（待建）|
| 全程協調 / orchestration | `shj-lead` | 全部 / all | `shj-era-mapping` | — |

## 3. Agent 與 Skill 清單 / Catalogue

| 層 / Layer | 類型 / Kind | 名稱 / Name | 用途 / Purpose |
|---|---|---|---|
| 公共 Common | agent | [textual-critic](../.claude/agents/textual-critic.md) | 原文、校勘、替代讀法 / original text, collation, variant readings |
| 公共 Common | agent | [entity-extractor](../.claude/agents/entity-extractor.md) | 實體、關係、名稱語義、覆蓋檢查 / entities, relations, name features, coverage |
| 公共 Common | agent | [semantic-matcher](../.claude/agents/semantic-matcher.md) | 遮蔽下的候選生成與語義評分 / masked candidates and judgments |
| 公共 Common | agent | [civilization-scout](../.claude/agents/civilization-scout.md) | 時代內的文明、造物與人群 / civilisations, works, peoples of the period |
| 公共 Common | agent | [palaeo-geographer](../.claude/agents/palaeo-geographer.md) | 時代內的地理、動物與地圖 / geography, fauna and map of the period |
| 公共 Common | agent | [cross-validator](../.claude/agents/cross-validator.md) | 觀察框架、求解、可信度、假說組態 / frame, solver, confidence, held configurations |
| 公共 Common | agent | [devils-advocate](../.claude/agents/devils-advocate.md) | 紅隊：洩漏、誘餌、對稱、年代 / red team |
| 公共 Common | skill | [source-ingest](../.claude/skills/source-ingest/SKILL.md) | 新語料入庫 / onboard a corpus |
| 公共 Common | skill | [witness-collation](../.claude/skills/witness-collation/SKILL.md) | 見證本對勘 / collation |
| 公共 Common | skill | [transmission-error-tolerance](../.claude/skills/transmission-error-tolerance/SKILL.md) | 傳承錯誤 / transmission errors |
| 公共 Common | skill | [entity-graph-extraction](../.claude/skills/entity-graph-extraction/SKILL.md) | 實體與關係 / entities and relations |
| 公共 Common | skill | [name-semantics](../.claude/skills/name-semantics/SKILL.md) | 名稱語義 / name semantics |
| 公共 Common | skill | [observer-frame](../.claude/skills/observer-frame/SKILL.md) | 觀察框架 / observer frame |
| 公共 Common | skill | [era-world-modelling](../.claude/skills/era-world-modelling/SKILL.md) | 時代世界 / world of the period |
| 公共 Common | skill | [semantic-correlation-matching](../.claude/skills/semantic-correlation-matching/SKILL.md) | 語義評分規程 / judgment protocol |
| 公共 Common | skill | [graph-cross-validation](../.claude/skills/graph-cross-validation/SKILL.md) | 聯合求解與可信度 / joint solving and confidence |
| 山海經 SHJ | agent | [shj-lead](../.claude/agents/shj-lead.md) | 子項目主持 / sub-project lead |
| 山海經 SHJ | skill | [shj-era-mapping](../.claude/skills/shj-era-mapping/SKILL.md) | runbook |

## 4. 公共層與子項目層 / Common vs sub-project

| 公共 / Common | 山海經專用 / Shanhaijing-specific |
|---|---|
| 框架 v3 的步驟、原則、解讀規則、計分與求解、紅隊（`docs/research-framework.md`）| 時代窗口（前 4000–前 2000）、原點（中原）、實體句式、名稱語義詞表、試點範圍 |
| 判斷紀錄格式、遮蔽與洩漏檢測 | 重點文明（兩河流域、哈拉帕、古埃及）與對立文明清單 |
| 時代世界庫的卡片格式 | `data/era/` 的內容、`era-world.md` |

## 5. 新語料接入 / Adding a corpus
1. 依 `source-ingest` 建立 `reference/<corpus>/` 和 `tools/<corpus>/`。/ Create both per `source-ingest`.
2. 決定時代窗口與觀察原點，寫 `projects/<corpus>/docs/era-world.md` 與規格（只寫專用部分）。/ Set the window and origin; write era-world and a spec.
3. 建立該時代的世界庫；其他一律重用公共層。/ Build the era base; reuse the common layer.
