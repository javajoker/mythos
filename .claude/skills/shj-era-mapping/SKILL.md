---
name: shj-era-mapping
description: Runbook for the Shanhaijing v4 iterative pipeline from working text and entity extraction through semantic-fit graph, base and later drafts, LLM conflict adjudication and reviewed delivery.
---

# 《山海經》時代語義對應 runbook v4

本 skill 只負責編排，不複製方法細節。權威規格為：

- `docs/research-framework.md`
- `projects/shanhaijing/docs/methodology-spec.md`
- `projects/shanhaijing/docs/data-model.md`
- `projects/shanhaijing/data/kg-ontology.json`

## 執行順序

1. `textual-critic`：確認 working text 的次序與正式證據讀法。
2. `entity-extractor`：建立全書實體、提及、名稱語義和文本關係；代碼只保存結構與核對覆蓋。
3. `semantic-matcher`／`palaeo-geographer`：由 LLM 完成全部水體的真實世界映射，保留共享水體與歷史狀態，先交項目發起人確認。
4. `civilization-scout`／`palaeo-geographer`：完成有年代、來源和對立候選的時代世界卡。
5. `semantic-matcher`：在水體映射確認後，遮蔽生成競爭候選與語義擬合屬性；以未確認錨點初始化搜索，迭代校準後再形成地標共識。
5a. `classic-adapter`／`atlas-renderer`：按 `classic-adaptation` runbook 為單個子經產出適配包——里程網格、逐實體映射、適配報告、逐句文檔與 SVG 地圖（工作範例：`xici3-*`）。
6. `entity-extractor`：組成 KG v1——基礎圖（nodes/mentions/edges/attributes）＋26 子經適配包的時代映射屬性（地理實體，由 `tools/shj/kg_v1_assemble.py` 組裝：era.candidate 主/對立候選＋era.state；MTN/WAT/LND 覆蓋必須 100%）＋人文風物識別讀法（由 `tools/shj/kg_readings_build.py` 從逐句文檔 §2/§3 結構化，配 `readings-supplement.jsonl` 補充；非 DOC 節點零遺漏）；運行 `kg_validate.py`（屬性衝突僅報告，留待 LLM 裁決階段）。屬性與關係為開放式註冊制：新謂詞/關係類型先在本體註冊再入庫。
7. `shj-lead`：重新生成五臧山經草稿，保留未決項。
8. `entity-extractor`／`semantic-matcher`：補充 associative 和 deductive 屬性。
9. `shj-lead`：重新生成卷六至十八草稿並更新圖譜。
10. `cross-validator`：由 LLM 解決語義衝突、合併或拆分，回寫指定記錄並迭代。
11. `devils-advocate`：獨立紅隊通過後，才交付 `deliverables/draft-v1/` 並評估地圖重建。

## 基礎判斷約束

每個階段均按「原文 → 靜態形狀／物理特徵 → 古代通用詞義 → 同時代候選 → 對稱評估 → 可信度與未知項」執行。後世地名、現代水流、傳播鏈缺失和獅虎等現代狹窄分類不得單獨否決；文化歷史機制未知時保持未知。

開羅／吉薩可作為崑崙之丘的競爭候選與未確認 `initialization` 錨點，從《西次三經》反向擬合五臧山經位置；它不是既定答案，也沒有證據優先權。支持時可加入其他初始化錨點聯合校準。其人工高台、陵寢格局、人面獸身造像與其他同時代物理特徵，必須與其他候選按同一規則比較。

「昆侖之丘」「昆侖／昆侖山」「昆侖之虛／虛」與「西胡白玉山」是不同語義指稱；阿特拉斯、撒哈拉之眼與乞力馬扎羅等古今綜合聯想，只能在相應後續卷完成抽取並通過水體映射審核後，由 LLM 作競爭假說處理。

## 第一版硬約束

只有卷一至五可新增 `MTN/WAT/LND` 節點。卷六至十八必須復用這些節點；無法對齊的提及保持 `pending_anchor`，由 LLM 裁決，不得由程序新增或指定節點。

此約束不指定任何現實地理答案。所有對應均為競爭假說，時代窗口為 4000–1000 BCE，比例尺在 0.35–0.42 km/里區間做敏感度分析。
