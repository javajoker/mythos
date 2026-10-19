# 架構 / Architecture

## 1. 分層 / Layers

```
            ┌──────────────────────────── docs/ ────────────────────────────┐
            │ whitepaper · prd · research-framework · conventions · glossary │
            └────────────────────────────────────────────────────────────────┘
 reference/<corpus>/            tools/<corpus>/                projects/<corpus>/
 ┌──────────────────┐   ingest  ┌───────────────┐  derive  ┌─────────────────────────┐
 │ sources/<witness>│ ────────▶ │ fetch, ingest │ ───────▶ │ data/derived/           │
 │ data/entries     │           │ collate,      │          │ hypotheses/H-*/dossier  │
 │ text/*.md        │ ◀──────── │ extract, fit  │ ◀─────── │ findings/F-*            │
 └──────────────────┘   cite    └───────────────┘   test   │ docs/ (spec, tasks …)   │
                                                            └─────────────────────────┘
                     .claude/agents + .claude/skills（公共層 + 子項目層 / common + sub-project）
```

- `reference/` 只放原文和忠實的結構化轉寫，**不放詮釋**。/ holds source texts and faithful structured transcriptions only, **no interpretation**.
- `projects/` 放詮釋：衍生資料、假說、發現。所有詮釋都可以追溯到 `reference/` 的條目。/ holds interpretation (derived data, hypotheses, findings), all traceable to `reference/` entries.
- `tools/` 是確定性的腳本，只用標準庫，固定隨機種子。/ deterministic scripts, standard library only, fixed seeds.

## 2. 研究流程與代理分工 / Pipeline and agent roles

| 階段 / Stage | 主責 / Lead | 支援 / Support | Skill |
|---|---|---|---|
| S0 語料 / Corpus | `textual-critic` | — | `source-ingest` |
| S1 校勘 / Criticism | `textual-critic` | — | `witness-collation` |
| S2–S4 抽取、一致性、重建 / Extraction, consistency, reconstruction | `shj-route-reconstructor` | `textual-critic` | `shj-itinerary-reconstruction` |
| S5 指紋 / Fingerprints | `geo-triangulator` | `naturalist` | `toponym-triangulation`, `biogeo-identification` |
| S6 盲候選 / Blind candidates | `geo-triangulator` | `naturalist` | `toponym-triangulation` |
| S7 交叉定位 / Triangulation | `geo-triangulator` | `naturalist`, `shj-route-reconstructor` | 同上 / same |
| S8 裁決 / Adjudication | `adjudicator` | `devils-advocate` | `hypothesis-adjudication` |
| S9 發佈 / Publication | `shj-lead` | — | `shj-hypothesis-case` |
| 全程協調 / Orchestration | `shj-lead` | 全部 / all | `shj-hypothesis-case` |

## 3. Agent 與 Skill 清單 / Catalogue

| 層 / Layer | 類型 / Kind | 名稱 / Name | 用途 / Purpose |
|---|---|---|---|
| 公共 Common | agent | [textual-critic](../.claude/agents/textual-critic.md) | 校勘、引文核對、工作文本 / collation, quote checking, working text |
| 公共 Common | agent | [geo-triangulator](../.claude/agents/geo-triangulator.md) | 地理指紋、盲候選、關係網路、水系同構 / fingerprints, blind candidates, relation networks, hydrology |
| 公共 Common | agent | [naturalist](../.claude/agents/naturalist.md) | 生物和礦產鑑定、分佈與遷徙 / biota and minerals, ranges and migration |
| 公共 Common | agent | [adjudicator](../.claude/agents/adjudicator.md) | 依檢查清單審查、定級 / checklist audit and grading |
| 公共 Common | agent | [devils-advocate](../.claude/agents/devils-advocate.md) | 紅隊五項 / the five red-team checks |
| 公共 Common | skill | [source-ingest](../.claude/skills/source-ingest/SKILL.md) | 新語料入庫 / onboard a corpus |
| 公共 Common | skill | [witness-collation](../.claude/skills/witness-collation/SKILL.md) | 見證本對勘與異文分類 / collation and variant classes |
| 公共 Common | skill | [toponym-triangulation](../.claude/skills/toponym-triangulation/SKILL.md) | 地名交叉定位 / place triangulation |
| 公共 Common | skill | [biogeo-identification](../.claude/skills/biogeo-identification/SKILL.md) | 生物鑑定與分佈 / taxa and ranges |
| 公共 Common | skill | [hypothesis-adjudication](../.claude/skills/hypothesis-adjudication/SKILL.md) | 證據分級、合計、定級 / grading, tally, verdict |
| 山海經 SHJ | agent | [shj-lead](../.claude/agents/shj-lead.md) | 子項目主持 / sub-project lead |
| 山海經 SHJ | agent | [shj-route-reconstructor](../.claude/agents/shj-route-reconstructor.md) | 山經路線與水系 / itineraries and rivers |
| 山海經 SHJ | skill | [shj-itinerary-reconstruction](../.claude/skills/shj-itinerary-reconstruction/SKILL.md) | S2–S4 |
| 山海經 SHJ | skill | [shj-hypothesis-case](../.claude/skills/shj-hypothesis-case/SKILL.md) | S0–S9 卷宗 / dossiers |

## 4. 抽取紀錄：從子項目到公共層 / Extraction record: sub-project → common layer

先完成山海經子項目的工作（H-0001 全流程），再把其中與語料無關的部分抽取為公共層。
The Shanhaijing work (the full H-0001 run) was done first; the corpus-independent parts were then extracted into the common layer.

| 山海經中的做法 / Shanhaijing practice | 抽取為 / Extracted to | 留在子項目的部分 / Kept sub-project-specific |
|---|---|---|
| 三見證本對勘、移段偵測（F-0001）/ three-witness collation, displacement detection | `witness-collation`, `textual-critic` | 異體摺疊表、X1–X6 錯誤類型 / graphic-variant fold table, error types X1–X6 |
| 證據分級、校改預算、定級（H-0001 §5）/ grading, budget, verdict | `hypothesis-adjudication`, `adjudicator`, `docs/research-framework.md` | 預設預算值、山海經檢查清單 / default budget, SHJ checklist |
| 紅隊五項（H-0001 §6）/ the five red-team checks | `devils-advocate` | — |
| 鏈條擬合、盲候選、古環境檢查（H-0001 §4.8）/ chain fit, blind candidates, palaeo-environment check | `toponym-triangulation`, `geo-triangulator` | 「里」、八方位、出／注／潛、水／海／澤詞彙 / 里, eight-point bearings, 出/注/潛, the 水/海/澤 lexicon |
| 分類群對照表、棲地矛盾、母題基準率（H-0001 §4.6、§4.9）/ taxon fit table, habitat conflict, motif base rates | `biogeo-identification`, `naturalist` | 「狀如X」「其音如X」等句式解析 / parsing of formulas like 狀如X, 其音如X |
| 語料入庫與編號（`ingest.py`）/ corpus ingest and IDs | `source-ingest` | 維基文庫模板解析 / Wikisource template parsing |

## 5. 新語料接入 / Adding a corpus

1. 依 `source-ingest` 建立 `reference/<corpus>/` 和 `tools/<corpus>/`。/ create both directories per `source-ingest`.
2. 寫 `projects/<corpus>/docs/methodology-spec.md`，只寫專用部分：結構事實、領域慣例、專用錯誤類型、抽取規則。/ write a spec covering only the specific parts.
3. 需要時再寫專用 agent 或 skill，例如 `<corpus>-lead`。其他一律重用公共層。/ add specialised agents or skills only as needed; reuse the common layer for everything else.
