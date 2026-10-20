# 山海經子項目任務 / Shanhaijing Sub-project Tasks

> v3.1 ・ 2026-10-20 ・ 方法：全球時代語義對應與雙向古世界反推（[框架 v3.1](../../../docs/research-framework.md)、[規格 v3.1](methodology-spec.md)）。
> 狀態 / Status: ✅ done ・ ⏳ in progress ・ ⬜ todo。
> 編號 / IDs: `T-0nn`–`T-2nn` 文本層；`T-G` 全球時代語義與反推版（Global Era & Reverse Paleoworld）；`T-R` 紅隊。

---

## 文本層 / Text layer
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-001 | 擷取三個見證本（通行本、四部叢刊明成化本、四庫本）/ fetch the three witnesses | `fetch_sources.py` | ✅ |
| T-002 | 逐段編號（869 段）；注疏分欄保存，不進入分析 / IDs; commentary kept apart, never analysed | `ingest.py` | ✅ |
| T-003 | 在明成化本與四庫本中定位每個底本條目 / locate every base entry in both witnesses | `align_witness.py` | ✅ |
| T-004 | 以明成化本為序的工作文本 / working text in Chenghua order | `align_witness.py` | ✅ |
| T-005 | 對照掃描頁補齊四部叢刊本缺頁 / fill the Sibu Congkan gaps from the scans | `textual-critic` | ⬜ |
| T-101 | 機器對勘 / machine collation | `collate.py` | ✅ |
| T-102 | 異文分類（自動首輪；草稿讀法政策，見 source-assessment §4）/ variant classes | `classify_variants.py` | ✅ |
| T-103 | 擴充異體字摺疊表 / extend the graphic-variant fold table | `textual-critic` | ⬜ |
| T-104 | 登記底本的現代移段與補入文字 / register modern relocations and insertions | `align_witness.py` | ✅ |
| T-105 | 以見證本的數字讀法重抽里程，並記為替代讀法（R11）/ witness numerals as variant readings | `textual-critic` | ⬜ |

---

## 全球時代語義與雙向反推版 / Global Era & Reverse Paleoworld
設定（項目發起人，2026-10-20）：
- 時代：前 4000–前 1000 年（新石器晚期至商周青銅時代）逐步積累的全球人類自然與人文觀察記錄。
- 原點：古中國商朝（河南，34.7°N, 113.6°E）為天下之「中」。
- 範圍：西至非洲（埃及、尼羅河、紅海、撒哈拉）、東至美洲（奧爾梅克前身、卡拉爾）、北至北極圈（極夜極光燭龍）、南至南海熱帶海域。
- 原則：只用原文、容許傳承錯誤、古名今名完全脫鉤、現象學與感知解碼、雙向反推古氣候與滅絕生態。
- 尺度：黃金緯度帶（30°–35°N）與周秦漢里（~0.4 km/里）校準，西山經 18,924 里 ≈ 7,570 km 精確對應中原至開羅（7,534 km）。

| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-G01 | 升級專案核心架構文檔：確立全球全域視野、7500km/18924里幾何校準、現象學解碼與雙向反推機制 | `shj-lead` | ✅ |
| T-G02 | 清空歷史生成檔案：清空 derived/ 下舊運算數據，保證純淨重置 | `shj-lead` | ✅ |
| T-G03 | 全球四大極致現象與地標深度對照（北極燭龍極夜、東洋十日湯谷、西洋開羅崑崙、大洋歸墟） | `palaeo-geographer`, `semantic-matcher` | ⏳ |
| T-G04 | 《西山經》18,924 里跨大陸接力賽段逐山逐水幾何排布與交叉驗證（四篇串聯假說 vs 樞紐假說） | `cross-validator` | ⬜ |
| T-G05 | 《大荒東經》《東山經》跨太平洋與美洲航路及古遺址（Caral/北美巨木）對應 | `civilization-scout` | ⬜ |
| T-G06 | 雙向反推成果庫：建立《山海經》反映之公元前 4000–前 1000 年古氣候、古水網與滅絕物種反演報告 | `devils-advocate` | ⬜ |
| T-G07 | 交付逐段逐句全球對照矩陣與當時世界地圖（draft-v5） | `shj-lead` | ⬜ |

---

## 紅隊審查 / Red team
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-R01 | 今名依賴與先入知識審查：全面排查「華山」「崑崙」「紅海」等今名對大模型判斷之污染 | `devils-advocate` | ⬜ |
| T-R02 | 距離尺度與幾何拓撲一致性審查：檢驗 18,924 里與開羅之間沿途水系流向與山脈排布之物理真實性 | `devils-advocate` | ⬜ |
| T-R03 | 全球時代地圖與反推成果審查 | `devils-advocate` | ⬜ |
