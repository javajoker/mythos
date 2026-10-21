# Mythos 清理與方法決策記錄 / Cleanup and Method Decision Record

> 狀態：D01–D25 已由項目發起人於 2026-10-21 裁決並落實為框架 v4。本文保留決策依據，不再是待審清單。

## 1. 清理結果 / Cleanup outcome

已刪除舊綜合解釋、舊十八卷草稿、舊地圖、兩個地圖渲染器、舊知識圖譜、重複 SVG、重複子項目 MEMORY 和本機快取。原始見證本與文本層資料保留；新草稿和地圖只能由新流程重建。

## 2. 已裁決事項 / Decisions

| ID | 發起人決策 / Decision | 實施位置 / Implementation |
|---|---|---|
| D01 | 時代窗口統一為 **4000–1000 BCE** | 全部框架、規格、PRD、時代世界與 agent/skill |
| D02 | 所有現實對應均為**競爭假說** | 框架 P2、語義匹配與紅隊規程 |
| D03 | **第一版強制**後續卷地理提及復用五臧山經節點 | SHJ 規格 §1/§4、ontology 與 `kg_validate.py` |
| D04 | 實體抽取→地理語義擬合屬性→初版圖譜→五臧山經草稿→屬性補充→後續卷→圖譜更新→LLM 衝突解決與合併→迭代 | SHJ 規格 §2、架構與 runbook |
| D05 | 比例尺採 **0.35–0.42 km/里** 區間 | 框架 R14、觀察框架與敏感度檢查 |
| D06 | 各篇先獨立；跨篇連接需要證據，總里程不直接作跨度 | 框架 R14、`era_frame.py` |
| D07 | 重新生成唯一里程帳本，保留篇末數與分段合計 | `routes-summary.md`、`era/totals.md` |
| D08 | 同名合併或拆分不預設答案，交 LLM 依證據裁決 | 框架 R15、衝突裁決記錄 |
| D09 | 舊草稿刪除，未來重新生成 | `deliverables/draft-v1/` 待建 |
| D10 | 進度只由可驗證產物決定 | `MEMORY.md`、子項目 README 與 tasks |
| D11 | 重新設計可擴展圖譜；衝突由 LLM AI 而非代碼裁決 | data model、ontology、框架 §6 |
| D12 | ID 與欄位全項目統一 | conventions、`TYPE:SHJ-BB-S-EEE#n` |
| D13 | 按對象實體類型設計屬性與關係 | `data/kg-ontology.json` |
| D14 | 公共層與 SHJ 專用層分離 | architecture、全部 agent/skill |
| D15 | 明確 base ID、working text 次序與讀法契約 | `align_witness.py`、source assessment |
| D16 | 重新生成缺失文本派生資料，不虛報完成 | working text、collation、variants、routes 已重建 |
| D17 | 時代庫如實標為種子，完成後才可評分 | `data/era/README.md`、era-world 規格 |
| D18 | 未經紅隊的結果只稱假說，不使用定論措辭 | 全部敘述文檔與 checklist |
| D19 | 裁決優先級 **human > llm > auto** | `classify_variants.py`、conventions |
| D20 | 程序檢測與計算，LLM 做語義裁決 | 框架 §6、`era_frame.py`、kg validator |
| D21 | 由共同可確定地標反推原點，共識後配合穩定 ID 登記 | SHJ 規格、`anchors.jsonl` 契約 |
| D22 | 修正失效章節與工具引用 | 全部規格、agent/skill 已改為 v4 引用 |
| D23 | 不恢復舊工具名；按新流程需要新增能力 | architecture 只列現有工具與未來能力 |
| D24 | 舊地圖與渲染器刪除，未來由有效圖譜重建 | 已刪除；T-M01 待辦 |
| D25 | 全域採用靜態形狀優先、禁止因果倒置、古代通用詞義、文化歷史斷層與統一推論順序；吉薩只作崑崙競爭候選 | 公共框架、SHJ 規格 §7、ontology、工具與全部 agent/skill |

## 3. 目前工具與組織 / Current tools and roles

現有工具：`fetch_sources`、`ingest`、`collate`、`align_witness`、`classify_variants`、`extract_routes`、`cn_numerals`、`era_frame`、`kg_validate`。舊地圖工具已刪除，語義任務、交付與地圖工具只在相應資料契約可用後新增。

保留 8 個 agent 與 10 個 skill 的名稱，按 v4 重寫職責。公共角色不包含 SHJ 固定答案；`shj-lead` 與 `shj-era-mapping` 只負責子項目編排並引用唯一規格。

## 4. 後續變更 / Later changes

本記錄不代表所有研究問題已解決，只表示項目結構與方法取捨已統一。若要放寬第一版地理復用、改變時代窗口或調整 LLM／人工裁決權限，須建立新決策並同步所有權威規格與工具。
