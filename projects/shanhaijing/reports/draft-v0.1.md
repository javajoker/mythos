# 《山海經》真實世界解讀・初稿 v0.2 / Shanhaijing Real-World Interpretation — Draft v0.2

> 2026-10-19 ・ 草稿：異文人工審查已依項目發起人決定取消，採用草稿讀法政策（source-assessment §4.4）。所有結論都可由倉庫中的腳本與卷宗重現。
> Draft: human variant review was cancelled by the initiator's decision; the draft-reading policy applies. Every conclusion is reproducible from the scripts and dossiers in this repository.

---

## 0. 一句話結論 / Bottom line

**繁中**：《山海經》不是一部「全球地圖」，也不全是想像。依本項目的方法，它是**四層性質不同的記錄疊合在一起**：

1. 一份鐵器時代、對黃河中游、太行東麓（當時黃河北流）、秦嶺、漢水、岷江一帶的**路線測量式記錄**（五藏山經）；
2. 一條從黃河上游延伸到**青藏高原東北緣**的西行路線，「崑崙」最可能指青海湖周圍的高地，同時帶有「天下中心」的宇宙山圖式；
3. 一份**秦至西漢**的地理知識清單，範圍從大夏、月氏到朝鮮、倭與海南（海內諸經）；
4. 一套以地平線上日月出沒點為骨架的**曆法與宇宙論框架**（大荒經）。

在 869 段原文中，**沒有任何一段可以核實到美洲、歐洲或撒哈拉以南非洲**；「崑崙在埃及」的假說經全流程檢驗後被否定。

**EN**: The Shanhaijing is neither a "world map" nor pure fantasy. By this project's method it is **four different kinds of record stacked together**: (1) an Iron Age **route-survey record** of the middle Yellow River, the Taihang front (when the Yellow River still flowed north), the Qinling, the Han and the Min (the Mountain Classics); (2) a westward route from the upper Yellow River to the **NE margin of the Tibetan Plateau**, where "Kunlun" most likely denotes the high country around Qinghai Lake while also serving as a cosmic-mountain schema; (3) a **Qin–Western Han** list of geographic knowledge reaching from Bactria and the Yuezhi to Korea, Wa (Japan) and Hainan (the 海內 books); (4) a **calendrical and cosmological framework** built on horizon sunrise and sunset points (the 大荒經). **No paragraph of the 869 can be verified as reaching the Americas, Europe or sub-Saharan Africa**, and "Kunlun in Egypt" is refuted after a full test.

## 1. 完整推理路徑 / The complete reasoning path

```
S0 語料      三個公有領域見證本（通行本、1470 明成化本、1781 四庫本）→ 869 段，逐段編號
   │         tools/shj/fetch_sources.py, ingest.py
S1 校勘      2,021 處異文；8 個現代移段塊（X3）；681 處底本偏離；工作文本依明成化本次序
   │         collate.py, align_witness.py, classify_variants.py → F-0001
S2 抽取      447 個站點、26 個篇段總數、232 條「出／注」水系邊
   │         extract_routes.py, river_graph.py
S3 自洽      8 段里程與篇末總數誤差 ≤ 2%，另 10 段 ≤ 10% → 里數是核算過的記錄（F-0002）
   │
S5 指紋      名稱遮蔽的水系指紋 F1–F7；各篇流域側位；生物溫度帶；日月山計數
   │
S6 候選      7 個世界大流域盲比對：黃河＋漢水／長江 7/7，其次 2.5/7
   │
S7 交叉定位  以水文角色選錨點 → 方位殘差、置換檢驗、反推里長（calibrate.py）
   │         以校準比例投影西次三經（chain_fit.py）；海內地名與匯流點逐條核對；日月方位天文計算
S8 裁決      H-0001 R ・ H-0002 L2 ・ H-0003 L1 ・ H-0004 L2 ・ H-0005 L1
S9 發佈      本報告；F-0001–F-0003
```

每一步的輸入、輸出和腳本都在倉庫中；以下各節依層次說明，每一個結論都附條目編號和卷宗連結。
Each step's inputs, outputs and scripts are in the repository; each section below gives the conclusion with entry IDs and dossier links.

## 2. 第一層：五藏山經的核心河網 / Layer 1: the Mountain-Classic core — [H-0002](../hypotheses/H-0002/dossier.md)，**L2**

| 推理步驟 / Step | 結果 / Result |
|---|---|
| 從文本建立河網，把名稱換成代號 / build the river network, mask the names | 幹流 T 收 47 條水；B 自西東流入 T，K 自東西流入 T；A 自南北流入 T；另有大河 C |
| 與世界大流域比較 / compare with world basins | 只有黃河＋漢水／長江上游符合全部 7 項（晉陝峽谷南流、潼關轉東；渭、汾、洛、沁、涇、北洛、伊、穀、漢、岷江）|
| 以水文角色選錨點（「某支流的源頭」）/ role-defined anchors | 方位殘差平均 56°（隨機 90°），**置換檢驗 p ≈ 0.01**：文本的方位是真實的資訊 |
| 反推里長 / implied 里 | 篇內一致，篇間不同（約 100 m 與 250 m），比直線距離長 1.6–4 倍 → 可能是行走路程（F-0003）|
| 生物溫度帶 / thermal zoning | 柑橘「橘櫾」只出現在流入長江、漢水的篇段，從未出現在黃河篇段，與秦嶺–淮河的柑橘北界一致 |
| 古河道 / ancient course | 北次三經十條溪流「東流注于河」直到燕山、碣石 → 當時黃河沿太行東麓北流入渤海，與西漢以前的河道一致 |

**真實地理 / Real geography**：晉陝峽谷、渭河盆地、汾河谷地、伊洛河流域、崤山、太行山東麓、秦嶺北坡與分水嶺、漢江源（寧強）、岷江源。

## 3. 第二層：西次三經與崑崙 / Layer 2: 西次三經 and Kunlun — [H-0003](../hypotheses/H-0003/dossier.md)，**L1**；[H-0001](../hypotheses/H-0001/dossier.md)，**R**

| 推理步驟 / Step | 結果 / Result |
|---|---|
| 「崑崙在埃及」全流程檢驗 / full test of "Kunlun in Egypt" | 否定：赤水、黑水、河水都是**從崑崙發源**的河流；紅海不是河；以吉薩為錨，西半段需要利比亞沙漠中有 7 條河 |
| 用第一層獨立校準的比例投影西次三經 / project with the Layer-1 scale | 崇吾之山（在河之南）→ 西北進入祁連山南麓；**崑崙之丘落在青海湖中心約 30 km 處**（90% 半徑 175 km）|
| 地面條件 / ground checks | 槐江「西望大澤」＝青海湖 ✓；河水「南流東注」✓；流沙＝共和、柴達木東部沙地 ✓；三危「披蓑」之牛＝牦牛類 ✓；積石、泑澤 ✗ |
| 跨語料 / cross-corpus | 《漢書・地理志》臨羌：「西北至塞外，有西王母石室、仙海、鹽池」；《論衡》：元始四年「遂得西王母石室，因為西海郡」（已核實；可能非獨立）|
| 基準率 / base rate | 「中心山向四方出四水」是跨文化宇宙山母題 → 崑崙同時是圖式化的世界中心 |

**真實地理 / Real geography**：青海湖、日月山與青海南山、祁連山南麓、柴達木盆地東緣。

**關於你的原始範例 / On the original example**：文鰩魚條的早期見證本作「常行西海，遊於東海」，與你的引文一致；本項目 r1 曾誤改，已更正。在青海湖框架下，漢代確實稱青海湖為「西海」，但湖中沒有飛魚；文鰩魚的描述（鳥翼、夜飛、往來兩海）指向某種海洋飛魚的傳聞，其來源海域仍未確定（O-2）。
The early witnesses read 「常行西海，遊於東海」, matching your quotation (r1 wrongly altered it; corrected). In the Qinghai frame the Han did call Qinghai Lake the 西海, but it has no flying fish; the 文鰩魚 description points to hearsay about a marine flying fish whose source sea is still undetermined (O-2).

## 4. 第三層：海內諸經的知識範圍 / Layer 3: the 海內 horizon — [H-0004](../hypotheses/H-0004/dossier.md)，**L2**

| 推理步驟 / Step | 結果 / Result |
|---|---|
| 14 條可核實的相對方位句 / 14 checkable relations | ✓ 9、~ 3、✗ 2（蓋國在燕南倭北、朝鮮、離耳在鬱水南、大夏月氏在流沙外……）|
| 12 條水道入口點 / 12 waterway endpoints | ✓ 11（渭入華陰北、洛入成皋西、汾入皮氏南、沁入懷東南、漳入章武南、濟入琅槐東北……）|
| 年代 / dating | 象郡（秦）、零陵（111 BCE）、大夏月氏（張騫以後）、章武（西漢縣）、建平元年題記（6 BCE）→ 約公元前 111 至前 6 年定稿 |

**真實地理 / Real geography**：西至今阿富汗北部、烏茲別克南部，北至蒙古高原，東北至朝鮮半島與日本，南至海南島與兩廣沿海，西南至四川盆地。

## 5. 第四層：大荒經的曆法框架 / Layer 4: the 大荒經 calendar framework — [H-0005](../hypotheses/H-0005/dossier.md)，**L1**

| 推理步驟 / Step | 結果 / Result |
|---|---|
| 計數 / counts | 東方日月所出之山 6 座，西方日月所入之山 6 座（另 1 座出入）|
| 天文檢驗 / astronomy | 司日長的神人在東北隅與西北隅＝北半球中緯度夏至日出（方位角約 58–62°）與日落方向 ✓ |
| 跨語料 / cross-corpus | 十日（十天一旬）、十二月；《尚書・堯典》「乃命羲、和……曆象日月星辰，敬授民時」，並分派四方 |
| 反面 / against | 大荒經沒有里程與可核實地名鏈，「遠方實際地理」說為 L0 |

## 6. 年代綜合 / Dating synthesis

| 線索 / Clue | 指向 / Points to | 來源 / Source |
|---|---|---|
| 山經「鐵」40 次 / iron 40× | 鐵器時代（約前 6 世紀以後）`needs-citation` | H-0002 §4.7 |
| 黃河北流入渤海的古河道 / northward Yellow River | 西漢以前 | H-0002 §4.5 |
| 象郡、零陵、章武、大夏月氏 / Qin–Han names | 秦至西漢，約前 111 年以後 | H-0004 §4 |
| 建平元年劉秀校上 / Liu Xin's submission | 前 6 年 | `SHJ-09-1-017` |

山經的觀測記錄最可能形成於戰國至西漢以前；海內諸經的定稿在西漢中後期；全書在公元前 6 年由劉歆校定。
The Mountain-Classic records most likely formed between the Warring States and the early Western Han; the 海內 books were finalised in the mid–late Western Han; the whole was edited by Liu Xin in 6 BCE.

## 7. 尚未解決 / Unresolved (L0 or untested)

| 部分 / Part | 狀況 / Status | 任務 / Task |
|---|---|---|
| 南山經、東山經 | 河網連結太少，指紋不足 / too few river links | T-650 |
| 北山經之首、泑澤 | 泑澤的位置在任何框架下都不合 / 泑澤 fits no frame | T-651 |
| 西次三經西半段（三危以西）| 不確定度 > 390 km / uncertainty > 390 km | T-652 |
| 海外四經的奇異民族 / strange peoples of the 海外 books | 多數無法核實；黑齒、雕題等可能是真實習俗 | T-620 |
| 文鰩魚的來源海域 / the flying fish's source sea | 仍未確定 / undetermined | T-610 |
| 甲骨「四方風」刻辭比對 / oracle-bone four winds | 尚未核實釋文 / reading not verified | T-630 |

## 8. 本草稿的限制 / Limitations of this draft

1. **非認知盲**：分析者知道傳統的中國中心說法；結構證據都已名稱遮蔽，名稱延續則大幅折減，但不能完全排除影響。/ **Not cognitively blind**: names were masked and name continuity heavily discounted, but influence cannot be fully excluded.
2. **人工異文審查已取消**：417 處異文未分類；里數仍取底本（T-105 未做）。/ **Human variant review cancelled**: 417 variants unclassified; distances still from the base text (T-105 pending).
3. **錨點座標為近似值**（±20–30 km），依各河流的標準條目；尚未用 DEM 與河網資料精確化（T-703）。/ **Anchor coordinates are approximate** (±20–30 km); not yet refined with DEM and river-network data.
4. **尺度問題**：山經里數比直線長 1.6–4 倍，原因（行走路程或單位）尚未確定（F-0003）。/ **Scale**: the cause of the 1.6–4× ratio is unresolved.
5. **標為 `needs-citation` 的外部事實不計分**，因此部分結論可能偏保守。/ **Uncited external facts score nothing**, so some conclusions may be conservative.

## 9. 等級總表 / Verdict summary

| ID | 層 / Layer | 結論 / Conclusion | 等級 / Grade |
|---|---|---|---|
| H-0001 | 崑崙 | 崑崙在埃及、赤水紅海、黑水尼羅河 / Kunlun in Egypt | **R** |
| H-0002 | 山經核心 / Mountain core | 黃河中下游（含古河道）＋漢水、岷江 / middle–lower Yellow River + Han, Min | **L2**（上限 L3）|
| H-0003 | 西次三經・崑崙 | 青藏高原東北緣、青海湖一帶 / NE Tibetan Plateau, Qinghai Lake | **L1** |
| H-0004 | 海內諸經 / 海內 books | 秦至西漢知識範圍：大夏月氏至朝鮮、倭、海南 / Qin–Han horizon | **L2** |
| H-0005 | 大荒經 | 地平線曆法框架，北半球中緯度 / horizon calendar, northern mid-latitudes | **L1** |

## 10. 方法 G（全球、描述優先）的初步結果 / First results of Method G (global, description-first)

> v0.2 新增（2026-10-19）。項目發起人設定：全書以整個地球為範圍；只看描述、不看名稱；距離只是參考；先從真實動物與地理出發，再到書中找證據。規格見 [method-g-global.md](../docs/method-g-global.md)。
> Added in v0.2. The initiator's premises: the whole Earth; descriptions only; distances only a reference; real animals and geography first, then evidence in the book.

### 10.1 動物地圖 / Animal map — [animal-map.md](../data/derived/animal-map.md)
119 個生物描述中，39 個以描述（名稱遮蔽）比對到真實動物（覆蓋率 ≥ 0.5）。最明確的幾例 / clearest cases：

| 書中描述 / Description | 真實動物 / Real animal | 分佈 / Range |
|---|---|---|
| 「狀如豚而白毛，毛大如笄而黑端」（`SHJ-02-1-008`）| 豪豬 / porcupine | 舊大陸 / Old World |
| 「狀如羊而四角」「如鹿而四角」（`SHJ-02-3-008` 等 4 處）| 四角羚 / four-horned antelope | 印度、喜馬拉雅 / India, Himalaya |
| 「其狀如䱱魚，四足，其音如嬰兒」（`SHJ-03-3-002`）| 大鯢 / giant salamander | 東亞 / East Asia |
| 「狀如雞，五采而文」（`SHJ-01-3-003`）| 孔雀、雉類 / peafowl, pheasants | 南亞、東亞、中非 / South & East Asia, Central Africa |
| 「魚身而鳥翼」（`SHJ-02-3-006` 等）| 飛魚 / flying fish | 各溫暖海域 / warm seas |
| 「狀如禺而文臂……善投」（`SHJ-02-3-001`）| 狒狒 / baboon | 非洲、阿拉伯 / Africa, Arabia |

全書投票：印度 > 喜馬拉雅 > 中國 > 東南亞 > 西非、中非、東非。注意：動物庫的物種組成會影響投票（例如印度特有種較多）。
Whole-book vote: India > Himalaya > China > SE Asia > West, Central and East Africa. Caveat: the species chosen for the base influence the vote.

### 10.2 崑崙在哪裡？/ Where is Kunlun? — [H-0006](../hypotheses/H-0006/dossier.md)

| 讀法 / Reading | 結果 / Result |
|---|---|
| 單一地點（27 處全球候選）/ single place | 安那托利亞中部 0.59、**吉薩 0.13**、墨西哥中部 0.10；領先不穩（G-弱至中）|
| 只看自然描述 / natural description only | 魯文佐里（月亮山，尼羅河源）0.96 > 興都庫什 0.44 |
| 只看人工描述 / built description only | 安那托利亞 2.60 > **吉薩 1.61**；吉薩是唯一「面向東方的人面獸身巨像」|
| 同一水系複合（事後）/ same-river composite (post-hoc) | **尼羅河：吉薩 ＋ 月亮山 6.51**；非尼羅河最佳為印度河 0.73 |

**回答「崑崙可能在埃及嗎？」/ Answer**：在方法 G 下，**可能，但尚未證實**。埃及獨有「東向的人面獸身守衛」這一描述；若崑崙是「同一條大河上的聖所與源頭雪山」，尼羅河組合大幅領先。但這一組合是事後提出的，而且庫中尼羅河候選較多。必須通過庫平衡檢驗（N5）與相鄰地名檢驗（N6）之後，才能升級。方法 A 的結論（H-0001：R；H-0003：青海湖 L1）保留並列，因為兩種方法回答的是不同的問題。
Under Method G, **possibly, not yet proven**. Egypt alone matches the east-facing human-faced feline guardian, and a Nile composite leads by a wide margin, but that composite is post-hoc and the base has more Nile loci. It must pass the balanced-base test (N5) and the neighbouring-names test (N6) before being upgraded. Method A's conclusions stay alongside, since the two methods answer different questions.
