# Mythos 核心記憶庫 / Project Memory

> 更新：2026-10-21
> 本文件只記錄已核驗狀態與下一步，不保存未經審查的地理結論。

## 1. 已確認的方法

- 框架 v4，時代窗口 **4000–1000 BCE**。
- 所有現實對應均為競爭假說；名稱遮蔽、對立候選、逐屬性證據與紅隊審查是必要條件。
- 全域推論順序：原文 → 靜態形狀與物理特徵 → 古代通用詞義 → 同時代候選 → 對稱評估 → 可信度與未知項。
- 動態流向、後世地名、現代分類與傳播鏈缺失不得提前否決；文化歷史機制未知時不得編造。
- 里數以 **0.35–0.42 km/里** 為擬合區間；各篇先獨立，跨篇連接須有文本或已接受關係。
- 觀察原點由共同可確認地標反推並形成共識，不預設含混城市坐標。
- 第一版卷六至十八的 `MTN/WAT/LND` 強制復用《五臧山經》節點；未決提及進入 `pending_anchor`，由 LLM 裁決。
- 流程：工作文本 → 實體抽取 → 地理語義擬合屬性 → 初版圖譜 → 五臧山經草稿 → 屬性補充 → 後續經卷 → 圖譜更新 → LLM 衝突解決與合併 → 迭代。
- 程序做檢查與計算，LLM 做語義裁決；人工覆核高於 LLM，LLM 高於自動提議。

唯一權威規格：`docs/research-framework.md`、`projects/shanhaijing/docs/methodology-spec.md`、`projects/shanhaijing/docs/data-model.md`。

## 2. 已完成的清理與重建

- 舊綜合解釋、舊十八卷草稿、舊地圖、地圖渲染器和舊知識圖譜均已刪除。
- 重複的子項目 MEMORY 與重複 SVG 已刪除；根 MEMORY 是唯一進度記憶入口。
- 已建立框架 v4、SHJ 規格 v4、可擴展資料模型和 `data/kg-ontology.json`。
- 已新增 `tools/shj/kg_validate.py`，只校驗結構與報告衝突，不裁決語義。
- 已補上來源快照 `reference/shanhaijing/sources/manifest.json`，含 57 個原始文件的 SHA-256。

## 3. 文本層實際狀態

- 三個見證本與 869 個穩定條目保留。
- `working-text.jsonl` 已重建：869 個 base 條目加 3 個 witness-only 片段，共 872 行。
- 當前 base 讀法明確標為 `reading_status: unreviewed`；不得把「已對齊」誤寫成「讀法已全部確認」。
- 已重建 collation、alignment、displacements、variant-classes 及其摘要。
- 路線抽取以 working text 為輸入：447 個站點、26 個篇末總數。
- 篇末里程差異只報告給 LLM，不再由程序自動校準。
- `cn_numerals.py` 可在系統 Python 3.9 下運行。

## 4. 尚未完成

- 新實體圖譜 `nodes/mentions/edges/attributes` 尚未生成。
- 地理候選、語義判斷、地標共識與最終 mapping 尚未生成。
- 新五臧山經與後續經卷草稿尚未生成。
- 時代世界庫仍是種子；`sites.jsonl` 與 `palaeo-coast.json` 尚未建立。
- 新 LLM 衝突日誌與紅隊審查尚未執行。
- 地圖待有效圖譜和時代資料完成後重建。

## 5. 下一步

1. 由 `textual-critic` 確認正式證據所需的讀法，保留 human > llm > auto 的裁決順序。
2. 由 `entity-extractor` 從 working text 建立文本事實圖，未決項不得強行補齊。
3. 完成時代世界卡與競爭候選，再由 `semantic-matcher` 形成地理語義擬合屬性。
4. 以 `kg_validate.py` 做結構檢查後，才開始新草稿。
