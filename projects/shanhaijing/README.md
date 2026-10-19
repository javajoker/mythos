# 山海經子項目 / Shanhaijing Sub-project

> 從《山海經》原文出發，不採用任何既有結論：把書中每一個實體當作符號，依描述、性質與實體之間的關係，在全球範圍內找出最一致的真實世界對應，並給出可信度。
> Starting from the text alone and adopting no prior conclusion: treat every entity as a symbol and, from its description, properties and relations, find the most consistent real-world counterparts worldwide, with confidence scores.

## 交付 / Deliverable

**[初稿 v2 / draft v2](deliverables/draft-v2/README.md)**：全書 869 段、4,004 次實體提及逐條對照（[逐段](deliverables/draft-v2/book/)、[全部實體](deliverables/draft-v2/entities.md)、[完整性檢查 PASS](deliverables/draft-v2/coverage.md)）。
Item-by-item mapping of all 869 paragraphs and 4,004 entity mentions.

## 文檔 / Documents

| 文件 / Doc | 內容 / Content |
|---|---|
| [docs/methodology-spec.md](docs/methodology-spec.md) | **方法規格**：五個步驟、實體類型與合併規則、關係、候選庫、交叉驗證的權重與求解、交付格式 / **method spec** |
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
- ✅ 知識圖譜：1,941 個實體、2,725 條關係；覆蓋檢查 0 / 0 / knowledge graph with a passing coverage audit
- ✅ 全球候選（支流已平衡）與交叉驗證：已對應 973 個（高 1、中 34、低 171、暫定 767）/ mapped 973 on the balanced base
- ✅ 紅隊審查 R1（[red-team.md](docs/red-team.md)）：庫的偏差、抽取錯誤、權重敏感度、誘餌 / red-team review R1
- ✅ 初稿 v2（取代 v1）/ draft v2 (supersedes v1)
- ⏳ 下一步：補抽空間關係（T-E06）；新的解讀規則等待決定（T-X05）/ next: spatial relations (T-E06); new reading rules pending a decision (T-X05)

**主要結果 / Main results**：v1 的「河 = 黃河」「山經在黃河、渭河流域」已撤回（真實世界庫只為中國河流列出支流）。平衡後，河流的對應全部暫定；可引用的（可信度 ≥ 0.3 且 16 個權重變體中 ≥ 14 個不變）只有 19 個，多為描述特別的動物，加上毛民 → 阿伊努與中國境內少數山。詳見 [draft v2](deliverables/draft-v2/README.md)。
v1's 河 = Yellow River and Yellow/Wei-basin results are withdrawn (base bias). After balancing, all rivers are tentative; 19 mappings are cite-able (≥ 0.3 and robust in ≥ 14/16 weight variants), mostly distinctive creatures, plus 毛民 → Ainu and a few mountains in China.

## 重現 / Reproduce

```bash
python3 -I tools/shj/fetch_sources.py   # 只在需要重新下載見證本時 / only to re-fetch witnesses
python3 -I tools/shj/ingest.py && python3 -I tools/shj/collate.py && python3 -I tools/shj/align_witness.py
python3 -I tools/shj/classify_variants.py && python3 -I tools/shj/extract_routes.py
python3 -I tools/shj/kg_extract.py && python3 -I tools/shj/kg_candidates.py
python3 -I tools/shj/kg_crossval.py     # 約 11 分鐘 / about 11 minutes
python3 -I tools/shj/kg_sensitivity.py  # 權重敏感度，約 30 分鐘 / weight sensitivity, about 30 minutes
python3 -I tools/shj/kg_deliver.py
```

## 代理與技能 / Agents and skills

主持者 `shj-lead`（runbook：skill `shj-entity-mapping`）；公共代理 `textual-critic`、`entity-extractor`、`world-candidate-scout`、`cross-validator`、`devils-advocate`。見 [architecture](../../docs/architecture.md)。
Led by `shj-lead` (runbook: skill `shj-entity-mapping`), with the common agents listed above.
