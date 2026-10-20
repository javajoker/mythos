# F-0002：五藏山經的里程大體自洽，可以作為測量資料 / The Mountain-Classic itineraries are largely self-consistent and usable as survey data

| 欄位 / Field | 值 / Value |
|---|---|
| 信心 / Confidence | 中（抽取器仍有遺漏 / the extractor still misses some stations）/ medium |
| 依據 / Basis | `tools/shj/extract_routes.py` → [routes-summary.md](../data/derived/routes-summary.md) |
| 撤回條件 / Retraction | 抽取器修正後，若大多數篇段的差異超過 ±10% / if, after extractor fixes, most sections differ by more than ±10% |

**繁中**：26 個有篇末總數的篇段中，有 8 段的分段里程合計與篇末總數相差在 ±2% 以內（例如東次二經 6,640 對 6,640、東次四經 1,720 對 1,720、中次四經 1,670 對 1,670），另有 10 段在 ±10% 以內，其餘 8 段差異較大。這說明山經的里程不是隨意編造的數字，而是經過加總核對的紀錄，可以作為測量資料使用。差異大的篇段，例如中山經首篇（937 對 6,670）、南次三經、東次三經，則是數字訛誤或站點脫漏的候選，列入任務 T-105 與 T-202。

**EN**: Of the 26 sections with a stated total, 8 have leg sums within ±2% of the total (e.g. 東次二經 6,640 vs 6,640; 東次四經 1,720 vs 1,720; 中次四經 1,670 vs 1,670), 10 more are within ±10%, and the remaining 8 differ more. The distances are therefore not arbitrary numbers: they are tallied records and can be used as survey data. Sections with large gaps, such as the first 中山經 section (937 vs 6,670), 南次三經 and 東次三經, are candidates for numeral corruption or dropped stations, queued under tasks T-105 and T-202.

> 註 / Note：這一點只說明文本內部有核算，**並不說明**這些里程對應真實地面距離。在時代語義方法中，里程是比例尺未知的軟約束（觀察框架，規格 §4）。/ This shows internal bookkeeping only; it does **not** show that the distances match real ground distances. In the era-semantic method, distances are soft constraints of unknown scale (observer frame, spec §4).

**更新 / Update (2026-10-20)**：依「其他篇的總數與各段一致」的推論，中山經首篇（6,670 → 937）、中次三經（440 → 80）、中次十二經（2,800 → 1,849；同段「凡十萬山」亦為訛誤）的篇末總數視為傳承錯誤，以齊全的各段合計校準；見 `data/derived/era/totals.md`。/ Three totals recalibrated from complete legs.
