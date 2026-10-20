# 山海經子項目 / Shanhaijing Sub-project

> 從《山海經》原文出發，不採用任何既有結論：把書中每一個實體當作符號，依描述、性質與實體之間的關係，在全球範圍內找出最一致的真實世界對應，並給出可信度。
> Starting from the text alone and adopting no prior conclusion: treat every entity as a symbol and, from its description, properties and relations, find the most consistent real-world counterparts worldwide, with confidence scores.

## 交付 / Deliverable

**[初稿 v3 / draft v3](deliverables/draft-v3/README.md)**：全書 869 段、4,004 次實體提及逐條對照（[逐段](deliverables/draft-v3/book/)、[全部實體](deliverables/draft-v3/entities.md)、[完整性檢查 PASS](deliverables/draft-v3/coverage.md)）。
Item-by-item mapping of all 869 paragraphs and 4,004 entity mentions.

## 文檔 / Documents

| 文件 / Doc | 內容 / Content |
|---|---|
| [docs/era-world.md](docs/era-world.md) | **時代世界**：前 4000–前 2000 年的海岸線、河道、氣候、文明與動物 / the world of 4000–2000 BCE |
| [docs/methodology-spec.md](docs/methodology-spec.md) | **方法規格 v3**：時代語義對應：原點、時代世界、遮蔽的語義評分、聯合求解、當時地圖 / **method spec v3** |
| [docs/data-model.md](docs/data-model.md) | 知識圖譜與真實世界庫的資料結構 / schemas of the knowledge graph and the world base |
| [docs/tasks.md](docs/tasks.md) | 任務與狀態 / tasks and status |
| [docs/checklist.md](docs/checklist.md) | 交付前檢查清單 / pre-delivery checklist |
| [docs/red-team.md](docs/red-team.md) | 紅隊審查紀錄 / red-team review log |
| [docs/source-assessment.md](docs/source-assessment.md) | 三個見證本的評估、現代移段、草稿讀法政策 / witnesses, modern relocations, draft-reading policy |
| [findings/](findings/) | 文本層的發現（F-0001 現代移段、F-0002 里程自洽）/ text-layer findings |
| [data/world/](data/world/README.md) | 真實世界庫：地區、性質、水體、動物、文化 / real-world base |
| [data/derived/kg/](data/derived/kg/) | 知識圖譜（節點、邊、提及、GraphML）、候選、對應 / knowledge graph, candidates, mapping |

## 目前狀態 / Current state (2026-10-19)

- ✅ 文本層：三個見證本、869 段、明成化本為序的工作文本、2,021 處異文的首輪分類 / text layer
- ✅ 知識圖譜：1,943 個實體、2,741 條關係；覆蓋檢查 0 / 0 / knowledge graph with a passing coverage audit
- ✅ 全球候選與交叉驗證：已對應 999 個（高 2、中 24、低 131、暫定 842）/ mapped 999
- ✅ 紅隊審查 R1（[red-team.md](docs/red-team.md)）：庫的偏差、抽取錯誤、權重敏感度、誘餌 / red-team review R1
- ✅ 解讀規則 R1–R7、空間句式、新候選、篇段掃描與假說檢驗；紅隊審查 R2 / reading rules, spatial clauses, new candidates, section scan and hypothesis tests; review R2
- ✅ 初稿 v3（取代 v2）/ draft v3 (supersedes v2)
- ✅ 時代語義版的框架、規格、agent 與 skill（框架 v3，T-V01–T-V02）/ era-semantic framework, spec, agents, skills
- ⏳ 下一步：時代語義版試點：西山經四篇與大荒西經（T-V03–T-V10），之後擴及全書並交付 draft-v4 / next: the era-semantic pilot, then draft-v4

**主要結果 / Main results**：使用者的「西次一、二、三經 = 哈拉帕、蘇美、埃及」在目前的證據下不被支持（完整重解 −40.8，低於中國、北美誘餌與衣索比亞組態）；崑崙之丘一段本身與埃及相容。可引用的對應 20 個，多為描述特別的動物，加上毛民 → 阿伊努與中國境內少數山；河流多為暫定。詳見 [draft v3](deliverables/draft-v3/README.md) 與 [hypotheses](deliverables/draft-v3/hypotheses.md)。
The Harappa–Sumer–Egypt reading of the West sections is not supported (−40.8 in a full re-solve); the Kunlun paragraph alone is compatible with Egypt. 20 mappings are cite-able; rivers are mostly tentative.

## 重現 / Reproduce

```bash
python3 -I tools/shj/fetch_sources.py   # 只在需要重新下載見證本時 / only to re-fetch witnesses
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/align_witness.py
python3 -I tools/shj/classify_variants.py && python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/kg_extract.py && python3 -I tools/shj/kg_candidates.py
python3 -I tools/shj/kg_crossval.py     # 約 17 分鐘 / about 17 minutes
python3 -I tools/shj/kg_sections.py     # 篇段掃描與假說，約 1.5 小時 / section scan and hypotheses, about 1.5 hours
python3 -I tools/shj/kg_sensitivity.py  # 權重敏感度，約 50 分鐘 / weight sensitivity, about 50 minutes
python3 -I tools/shj/kg_deliver.py
```

## 代理與技能 / Agents and skills

主持者 `shj-lead`（runbook：skill `shj-era-mapping`）；公共代理 `textual-critic`、`entity-extractor`、`semantic-matcher`、`civilization-scout`、`palaeo-geographer`、`world-candidate-scout`、`cross-validator`、`devils-advocate`。見 [architecture](../../docs/architecture.md)。
Led by `shj-lead` (runbook: skill `shj-era-mapping`), with the common agents listed above.
