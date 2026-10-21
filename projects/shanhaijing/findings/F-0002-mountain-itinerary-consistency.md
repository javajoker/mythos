# F-0002：五藏山經的里程具有內部核算線索 / Mountain-Classic itineraries show internal bookkeeping

| 欄位 / Field | 值 / Value |
|---|---|
| 信心 / Confidence | 中；抽取器仍有漏站與漏里程 / medium; extraction remains incomplete |
| 依據 / Basis | `tools/shj/extract_routes.py`、`tools/shj/era_frame.py`、`data/derived/era/totals.md` |
| 撤回條件 / Retraction | 工作讀法確認或抽取修正後，大多數篇段不再呈現穩定核算關係 |

26 個有篇末總數的篇段中，部分分段合計與篇末總數接近，另一些差異較大。這只說明文本內部可能存在加總與傳抄線索，**不證明里數對應任何現實地面距離，也不證明各篇可以串成連續路線**。

目前工具分別保留「篇末總數」與「各段合計」，差異只作為審查候選。框架 v4 不再沿用舊版以 20% 閾值自動改寫篇末總數的做法；是否屬於漏站、抽取失敗、數字訛誤或其他情況，由 LLM 結合見證本和上下文裁決。

後續比例尺只在 **0.35–0.42 km/里** 區間擬合並做敏感度分析。各篇先獨立，跨篇合計不得直接用作地理跨度。
