# 山海經子項目任務 / Shanhaijing Sub-project Tasks

> v3.5 ・ 2026-10-21 ・ 方法：全球時代語義對應與雙向古世界反推（[框架 v3.2](../../../docs/research-framework.md)、[規格 v3.3](methodology-spec.md)）。
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
設定（項目發起人，2026-10-21）：
- **無新地理實體公理**：卷六到卷十八只是描述人文和物產，沒有新的地理內容。所有卷六到卷十八提到的山、水實體，一定在五臧山經中找到對應的，並且 100% 強制複用對應的實體與地理坐標！
- **地圖表現法則**：反應到地圖上，也是把對應的人文物產添加到已有的五臧山經地圖之上：根據描述的五臧山經地理位置，補充人文和物產。
- **徹底拋棄後世注釋·文字出發**：五臧山經應該嚴格按照地理位置執行。徹底拋棄所有現在對於山海經的注釋和解讀！嚴格從山海經文字出發。
- **經典實證鐵律**：
  - 《大荒西經》的崑崙之丘就應該和《西山經》一樣，對應在開羅位置（30.0°N, 31.2°E，吉薩金字塔群）。
  - 一路向西，《西次三經》就應該是地中海非洲板塊。
  - 赤水 ≡ 紅海 (Red Sea)。
  - 黑水 ≡ 古埃及尼羅河 (Nile River，古埃及名 Aur 黑水)。
  - 陸吾 ≡ 吉薩獅身人面像 (Sphinx，人面虎身九尾虎爪守衛帝之下都)。
- 尺度：黃金緯度帶（30°–35°N）與周秦漢里（1 里 ≡ 0.400 公里）校準，西山經 18,924 里 ≈ 7,569.6 km 精確對應中原至開羅（7,534 km）。

| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-G01 | 升級專案核心架構文檔：確立全球全域視野、7500km/18924里幾何校準、現象學解碼與雙向反推機制 | `shj-lead` | ✅ |
| T-G02 | 清空歷史生成檔案：清空 derived/ 下舊運算數據，保證純淨重置 | `shj-lead` | ✅ |
| T-G03 | 全球四大極致現象與地標深度對照（北極燭龍極夜、東洋十日湯谷、西洋開羅崑崙、大洋歸墟） | `palaeo-geographer`, `semantic-matcher` | ✅ |
| T-G04 | 《西山經》18,924 里跨大陸接力賽段逐山逐水幾何排布與交叉驗證（四篇串聯假說 vs 樞紐假說） | `cross-validator` | ✅ |
| T-G05 | 《大荒東經》《東山經》跨太平洋與美洲航路及古遺址（Caral/北美巨木/奧爾梅克/瑪雅）對應 | `civilization-scout` | ✅ |
| T-G06 | 雙向反推成果庫：建立《山海經》反映之公元前 4000–前 1000 年古氣候、古水網與滅絕物種反演報告 | `devils-advocate` | ✅ |
| T-G07 | 交付逐段逐句全球對照矩陣與當時世界地圖（draft-v5） | `shj-lead` | ✅ |
| T-G08 | 【第一階段 Phase 1】全書十八卷（869 條經文，21,456 行草稿）100% 逐句純 LLM 解碼入庫 | `shj-lead` | ✅ |
| T-G09 | 確立「無新地理實體公理」、「山水 100% 複用五臧山經」與「拋棄注釋文字出發」：更新 docs, agents 與 skills | `shj-lead` | ✅ |
| T-G10 | 【第二階段 Phase 2】全要素知識圖譜抽取：卷六至十八山水節點 100% 複用山經，人文特產錨定於山經底座 | `entity-extractor`, `cross-validator` | ⏳ |

---

## 紅隊審查 / Red team
| ID | 任務 / Task | 負責 / Owner | 狀態 |
|---|---|---|---|
| T-R01 | 今名依賴與先入知識審查：全面排查「華山」「崑崙」「紅海」等今名對大模型判斷之污染 | `devils-advocate` | ⬜ |
| T-R02 | 距離尺度與幾何拓撲一致性審查：檢驗 18,924 里與開羅之間沿途水系流向與山脈排布之物理真實性 | `devils-advocate` | ⬜ |
| T-R03 | 全球時代地圖與反推成果審查 | `devils-advocate` | ⬜ |
