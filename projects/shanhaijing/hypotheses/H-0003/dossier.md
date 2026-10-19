# H-0003 卷宗：西次三經與崑崙之丘位於青藏高原東北緣（青海湖一帶）
# Dossier H-0003: 西次三經 and 崑崙之丘 lie on the NE margin of the Tibetan Plateau (Qinghai Lake region)

| 欄位 / Field | 值 / Value |
|---|---|
| 狀態 / Status | **adjudicated (draft v0.1) — L1（可能）/ Plausible** |
| 對立框架 / Rival frames | F-a 青海湖／祁連–柴達木（本假說）；F-b 阿爾金–塔里木（傳統里長）；F-c 吉薩（H-0001，已否定）/ F-a Qinghai Lake / Qilian–Qaidam (this hypothesis); F-b Altun–Tarim (traditional 里); F-c Giza (H-0001, refuted) |
| 登記日期 / Registered | 2026-10-19 |
| 慣例 / Conventions | 里長 90–250 m，依 F-0003（由 H-0002 獨立校準）；F-b 用 350–500 m / 里 90–250 m per F-0003 (calibrated independently in H-0002); F-b uses 350–500 m |
| 錨點 / Anchor | 崇吾之山「在河之南」：放在黃河蘭州段南岸（35.95°N, 103.80°E）；另以貴德段（36.03°N, 101.45°E）做敏感度分析 / placed on the south bank of the Yellow River's Lanzhou reach; the Guide reach is the sensitivity case |
| 重現 / Reproduce | `python3 -I tools/shj/chain_fit.py --section 西次三經 --anchor 崇吾之山 --lat 35.95 --lon 103.80 --li-min 90 --li-max 250` |

---

## 1. 推理路徑 / Reasoning path

```
H-0002（河 = 黃河，L2）＋ F-0003（里長 90–250 m）
   └─▶ 西次三經首站「崇吾之山，在河之南」：錨定在黃河上游南岸
         └─▶ 依文本方位與里數投影全段 22 站（蒙地卡羅）
               └─▶ 檢查每個預測位置的地面條件（湖、河、沙、牛、玉）
                     └─▶ 與 F-b、F-c 用同一標準比較 ─▶ L1
```

本卷宗**依賴 H-0002**。若 H-0002 被否定，本卷宗自動降為 L0。/ This dossier **depends on H-0002**; if H-0002 falls, this drops to L0.

## 2. 預測位置（F-a，蘭州段錨點）/ Predicted positions (F-a, Lanzhou anchor)

完整表格見 [chain-fit-Fa-lanzhou.md](chain-fit-Fa-lanzhou.md)。/ Full table in the linked file.

| 站 / Station | 預測 / Predicted | 90% 半徑 / radius | 文本要求 / Text requires | 實際 / Real world |
|---|---|---|---|---|
| 不周之山 #3 | 36.7°N 102.9°E | 68 km | 「東望泑澤，河水所潛也」/ a lake to the east where the 河 sinks | 東面是黃河谷地，沒有內流湖 ✗ / the Yellow River valley, no endorheic lake ✗ |
| 槐江之山 #7 | 37.6°N 100.8°E | 162 km | 「西望大澤」「南望昆侖」/ a great lake to the west; Kunlun to the south | 青海湖在其西南約 90 km ✓；崑崙預測位置在其西南 ✓ / Qinghai Lake ~90 km SW ✓ |
| **崑崙之丘 #8** | **37.15°N 100.3°E** | **175 km** | 河水出焉，南流東注；赤水東南流；洋水西南流；黑水西流 / four rivers in four directions | **距青海湖中心約 30 km**。湖南面的山地向南排水入黃河，黃河在那裡向東流 ✓；湖西是柴達木內流區 ~ / **~30 km from the centre of Qinghai Lake**; the mountains south of the lake drain south to the Yellow River, which flows east there ✓; west of the lake is the Qaidam endorheic basin ~ |
| 流沙 #10 | 37.15°N 98.7°E | 218 km | 沙地 / sand | 共和盆地、柴達木東部沙地 ✓ / Gonghe basin and east Qaidam dunes ✓ |
| 玉山 #11（西王母所居）| 37.15°N 98.15°E | 251 km | 西王母 / the Queen Mother of the West | 漢代的「西王母石室」在臨羌塞外，相距約 300 km，在半徑外 ~ / the Han-era 西王母石室 lay beyond 臨羌, ~300 km away, outside the radius ~ |
| 積石之山 #13 | 37.15°N 96.7°E | 308 km | 「石門，河水冒以西流」/ the 河 flows west through a stone gate | 黃河的西北流峽谷段（瑪曲–龍羊峽，約 35.4°N 100.5°E）相距約 410 km，在半徑外 ✗ / the Yellow River's NW-flowing gorge reach is ~410 km away, outside the radius ✗ |
| 三危之山 #18 | 37.15°N 94.4°E | 395 km | 「牛，白身四角，其豪如披蓑」/ a white ox whose hair hangs like a straw cape | 牦牛分佈區 ✓（四角 ✗）/ within yak range ✓ (four horns ✗) |

## 3. 證據 / Evidence

| # | 通道 / Channel | 內容 / Item | F-a | F-b（阿爾金–塔里木）| F-c（吉薩）|
|---|---|---|---|---|---|
| E1 | GEO | 尺度：F-a 用 H-0002 獨立校準的比例；F-b 用與 F-0003 矛盾的傳統里長 / scale | +0.3 | −0.3 | −0.3 |
| E2 | TER | 槐江「西望大澤」：青海湖為中國最大湖泊，位置吻合 / the great lake | +0.5 | 0（羅布泊在崑崙預測位置西北約 430 km）| ~0 |
| E3 | HYD | 崑崙的河水「南流東注」/ 河水 flows S then E from Kunlun | +0.2 | −0.3（阿爾金北坡河流北流）| −1.0（H-0001）|
| E4 | HYD | 不周「東望泑澤，河水所潛」/ the sinking lake east of 不周 | −0.3 | −0.3 | −0.3 |
| E5 | HYD/GEO | 積石西流河段 / west-flowing 河 at 積石 | −0.3 | −0.3 | −1.0 |
| E6 | TER | 流沙 / sands | +0.15 | +0.15 | +0.15 |
| E7 | BIO | 三危的「披蓑」之牛（牦牛類）/ yak-like ox | +0.15 | +0.15 | −0.3 |
| E8 | XCP | 漢代「西王母石室」與「西海」在青海湖一帶（《漢書・地理志》臨羌條，《論衡》元始四年西海郡條；見 §4）/ Han records place 西王母石室 and 西海 at Qinghai Lake | +0.2（玉山超出半徑，且漢人說法可能來自同一傳說，非獨立）| 0 | 0 |
| | | **合計 / Total** | **+0.90** | **−0.90** | **≤ −2.75** |

## 4. 跨語料原文 / Cross-corpus texts (verified)

- 《漢書・地理志》金城郡臨羌（引自《清史稿》卷 79；《太平御覽》卷 65 引文略同）：「西北至塞外，有西王母石室、仙海、鹽池。北則湟水所出，東至允吾入河。」/ Quoted in 清史稿 79 and 太平御覽 65.
- 王充《論衡》（Wikisource 論衡/58）：「後至四年，金城塞外羌……獻其魚鹽之地，願內屬漢，遂得西王母石室，因為西海郡。」
- 《水經注》（引自《清史稿》卷 79）：湟水「東逕西王母石室……又東南，逕卑禾羌海北，有鹽池，世謂之青海」。

**獨立性 / Independence**：這些漢代說法可能本身就受崑崙／西王母傳說影響，所以不算完全獨立的證據，只記 E1。/ These Han statements may themselves derive from the Kunlun / Queen Mother tradition, so they are not fully independent; E1 only.

## 5. 紅隊 / Red team

1. **反例 / Counter-examples**：E4、E5 都是負向證據，已計入。H-0001 的範圍條目（海內西經的崑崙虛「方八百里，高萬仞」，四角各出一水）具有明顯的宇宙論圖式色彩，F-a 無法完整解釋。/ E4 and E5 are negative and counted. The 海內西經 Kunlun (800 里 square, 10,000 仞 high, a river from each corner) is strongly schematic and F-a cannot explain it in full.
2. **替身 / Decoy**：換成貴德段錨點後，崑崙落在 37.2°N 97.9°E（柴達木東緣），與青海湖相距約 200 km，E2 降為 +0.15，合計約 +0.55，仍為 L1。/ With the Guide-reach anchor, Kunlun lands at the east edge of the Qaidam, ~200 km from the lake; E2 falls to +0.15 and the total to about +0.55, still L1.
3. **基準率 / Base rate**：「從一座中心山向四方流出四條河」是跨文化常見的宇宙山母題（例如須彌山、伊甸園的四條河，Wikipedia: Mount Meru; Garden of Eden）。這支持崑崙至少部分是**圖式化的宇宙中心**，而不全是地理實體（虛無假說的成分）。/ "Four rivers flowing in four directions from a central mountain" is a common cross-cultural cosmic-mountain motif (Meru, Eden), which supports Kunlun being at least partly a **schematic cosmic centre** rather than wholly a physical place (a null-hypothesis component).
4. **校改 / Emendations**：無。/ None.
5. **敏感度 / Sensitivity**：移除最強的 E2 → +0.40，仍為 L1。若 H-0002 降為 L1，E1 減半 → +0.75，L1。/ Drop E2 → +0.40, still L1. If H-0002 drops to L1, halve E1 → +0.75, L1.

## 6. 裁決 / Verdict

**F-a：L1（可能）。F-b：L0。F-c（吉薩）：R。**
**F-a: L1 (plausible). F-b: L0. F-c (Giza): R.**

**真實世界意義 / Real-world meaning**：以山經自己的方位與里數，並以獨立校準的比例投影，西次三經從黃河上游向西北進入祁連山南麓、青海湖與柴達木東部。「崑崙之丘」最可能指青海湖周圍的高山地帶，也就是農耕世界看到的青藏高原東北邊緣。漢代把西王母石室和「西海」定在同一地區，與此一致，但可能不是獨立的證據。崑崙同時帶有強烈的宇宙山圖式成分：它既是一個可以指出的地理區域，也是一張「天下中心」的示意圖。

Projected with the text's own bearings and distances and an independently calibrated scale, 西次三經 runs from the upper Yellow River north-west to the southern flank of the Qilian range, Qinghai Lake and the eastern Qaidam. 崑崙之丘 most likely denotes the high country around Qinghai Lake: the NE edge of the Tibetan Plateau as seen from the farming world. Han sources put 西王母石室 and the 西海 in the same area, which agrees, though possibly not independently. Kunlun also carries a strong cosmic-mountain schema: it is both an identifiable region and a diagram of the world's centre.

## 7. 保留的觀察 / Retained observations
- O-7：泑澤（河水所潛之處）在任何框架下都沒有找到合適的位置。/ No frame yet places 泑澤 (where the 河 sinks) satisfactorily.
- O-8：西次三經後半段（三危以西）的不確定度超過 390 km，目前無法定位。/ The western half (beyond 三危) has an uncertainty above 390 km and cannot yet be placed.

## 8. 重測觸發條件 / Re-test triggers
- 為西次三經找到兩個以水文角色定義的錨點，就可以直接校準本篇的里長，而不必借用其他篇的比例。/ Two role-defined anchors inside 西次三經 would allow calibrating its own scale instead of borrowing another section's.
- H-0002 的等級改變。/ A change in H-0002's grade.
