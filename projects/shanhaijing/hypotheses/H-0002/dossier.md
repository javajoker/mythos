# H-0002 卷宗：五藏山經的核心河網是黃河中下游與漢水、長江上游
# Dossier H-0002: The Mountain-Classic core river network is the middle–lower Yellow River with the upper Han and Yangtze

| 欄位 / Field | 值 / Value |
|---|---|
| 狀態 / Status | **adjudicated (draft v0.1) — L2（有據）；上限 L3 / Supported; upper bound L3** |
| 提出方式 / Origin | 由名稱遮蔽的水系指紋生成（規格 §8），不是由前人比定生成 / generated from the name-masked river fingerprint (spec §8), not from prior identifications |
| 登記日期 / Registered | 2026-10-19 |
| 方法版本 / Method | methodology-spec v0.1；草稿讀法政策 / draft-reading policy (source-assessment §4.4) |
| 校改預算 / Correction budget | log₁₀ −1.5；實際使用 0 / used 0 |
| 慣例 / Conventions | 方位為真北；里長不預設，由兩錨點反推 / true north; 里 length back-calculated from anchor pairs |
| 重現 / Reproduce | `python3 -I tools/shj/river_graph.py`；`python3 -I tools/shj/calibrate.py --anchors projects/shanhaijing/data/geo/anchors-yellow-yangtze.jsonl --adjacent` |

---

## 1. 假說 / Hypothesis

**繁中**：五藏山經中，以「河」為幹流（入流 47 條）的水系，以及以「江」「漢」為主的南方水系，記錄的是今天的黃河中下游（含其古代下游河道）、渭河、汾河、洛河，以及漢水、岷江（長江上游）一帶。範圍包括西山經之首、西次二經、西次四經、北次二經、北次三經和中山經各篇。

**EN**: In the Mountain Classics, the river system whose trunk is 「河」 (47 inflows), together with the southern system of 「江」 and 「漢」, records today's middle–lower Yellow River (including its ancient lower course), the Wei, Fen and Luo rivers, and the Han and Min (upper Yangtze). Scope: 西山經之首, 西次二經, 西次四經, 北次二經, 北次三經 and the 中山經 sections.

**不在範圍內 / Out of scope**：南山經、東山經（河網連結太少）、西次三經（見 H-0003）、北山經之首。/ 南山經 and 東山經 (too few river links), 西次三經 (see H-0003), 北山經之首.

**透明聲明 / Transparency note**：本假說與傳統說法大致重合。分析者知道傳統說法，所以「盲生成」只是程序上的盲，不是認知上的盲。因此本卷宗以名稱遮蔽的結構證據為主，並把名稱延續性單獨計分、大幅折減。已知的同方向前人學說登記為 `H-ext-0001`（見 §9）。/ This hypothesis broadly coincides with the traditional view. The analyst knows that view, so the "blind" generation is procedurally, not cognitively, blind. The dossier therefore rests mainly on name-masked structural evidence and scores name continuity separately with a heavy discount. Known prior work in the same direction is registered as `H-ext-0001` (§9).

## 2. 推理路徑 / Reasoning path

```
原文 869 段 ─▶ 447 站、232 條「出／注」水系邊（S2）
            ─▶ 名稱遮蔽的網路指紋 F1–F7（S5）
            ─▶ 全球候選流域比對（S6）：黃河–長江 7/7，其次 3/7
            ─▶ 以水文角色（某支流的源頭）選錨點，兩錨點反推里長與方位殘差（S7）
            ─▶ 生物、地形、名稱等其他通道（S7）
            ─▶ 合計、紅隊、敏感度 ─▶ L2（S8）
```

## 3. 預先登記的預測 / Pre-registered predictions

| # | 預測 / Prediction | 證偽條件 / Falsifier |
|---|---|---|
| P1 | 候選流域的實際拓撲滿足指紋 F1–F7 / the real basin satisfies F1–F7 | 主要特徵不符 / key features missing |
| P2 | 以水文角色選定的錨點對，其文本方位比隨機好 / anchor pairs chosen by hydrological role have better-than-random text bearings | 方位殘差與隨機無異 / residuals indistinguishable from random |
| P3 | 反推的里長穩定，且落在 250–600 m / implied 里 is stable and within 250–600 m | 不穩定或落在範圍外 / unstable or outside the band |
| P4 | 喜暖生物（柑橘、鼉）只出現在南方水系的篇段 / warmth-loving taxa appear only in sections of the southern system | 出現在幹流水系的北方篇段 / they appear in northern trunk sections |
| P5 | 北次三經大量向東流入「河」的溪流，要求幹流下游曾向北流經華北平原 / the many streams flowing east into 河 in 北次三經 require a trunk once flowing north across the North China Plain | 候選幹流從未有此河道 / the candidate trunk never had such a course |

## 4. 證據 / Evidence

### 4.1 HYD・名稱遮蔽的水系指紋 — **E3 (+1.0)**

由 `river-graph.md` 得出，代號取代河名（T、A、B…），比對時不看名字。/ From `river-graph.md`; codes replace names during matching.

| 指紋 / Feature | 文本依據 / Text basis |
|---|---|
| F1 幹流 T 先南流、後東流：西來的 B「東流注」於 T，東來的 K「西流注」於 T；轉東以後，南岸的 A「北流注」T，北岸溪流「南流注」T / trunk T runs south, then east: B joins from the west flowing E, K from the east flowing W; after the turn A joins from the south flowing N and northern streams flow S | `SHJ-02-4-018` 渭水東流注于河；`SHJ-03-2-001` 汾水西流注于河；`SHJ-02-4-014` 洛水北流注于河；`SHJ-03-3-019` 沁水南流注于河 |
| F2 B 自西向東，南岸有東西走向的山脈，山北溪流向北注 B；北岸收納一條自西北向東南流的支流和一條北來的支流 / B runs W→E with a range on its south bank whose streams flow N into it; it takes a SE-flowing tributary from the NW and one from the N | 西山經之首 7 條溪流「北流注于渭」；`SHJ-02-4-012` 涇水東南流注于渭；`SHJ-02-4-010` 洛水東流注于渭 |
| F3 該山脈是分水嶺，南側另有一條東南流的河 I / that range is a divide; south of it a river I flows SE | `SHJ-02-1-013` 大時之山：涔水北注渭，清水南注漢水；`SHJ-02-1-014` 嶓冢之山：漢水東南流 |
| F4 A 收納東流的 D 與 F；A 與 F 之間有一道東西向山嶺，嶺上溪流南注 A、北注 F / A takes the E-flowing D and F; a W–E ridge between A and F sheds streams S to A and N to F | `SHJ-05-2-009` 伊水東流注于洛；`SHJ-05-6-010` 穀水東流注于洛；中次六經：4 條南注洛、2 條北注穀水 |
| F5 有兩條同名的 A：一條入 B，一條入 T / two rivers share the name A, one into B, one into T | `SHJ-02-4-010` vs `SHJ-02-4-014` |
| F6 另有一大河 C，其支流全部東流；C 發源於西方的山 / a separate large river C whose inflows all flow E, rising in a western mountain | 中次九經 C 東×5；`SHJ-05-9-002` 岷山江水出焉 |
| F7 K 從西岸收納東流的溪流 / K receives E-flowing streams from its west bank | `SHJ-03-2-002`–`004` |

**候選流域比對（S6）/ Candidate basins**。外部事實依各河流的標準條目（Wikipedia 各河條目）；✓ 吻合、~ 部分、✗ 不合。/ External facts per the standard entries for each river.

| 流域 / Basin | F1 | F2 | F3 | F4 | F5 | F6 | F7 | 合計 / Score |
|---|---|---|---|---|---|---|---|---|
| **黃河＋漢水／長江上游 Yellow + Han/upper Yangtze** | ✓ 晉陝峽谷南流，潼關轉東；渭河西來、汾河東來、洛河南來、沁河北來 | ✓ 秦嶺北坡溪流北注渭；涇河自西北、北洛河自北 | ✓ 秦嶺分隔渭、漢；漢江東南流 | ✓ 伊河、澗河入洛；崤山分隔洛、澗 | ✓ 北洛河入渭，洛河入黃河 | ✓ 岷江／長江 | ✓ 汾河西岸支流 | **7/7** |
| 密西西比 Mississippi | ~ 南流，密蘇里西來、俄亥俄東來，但不轉東 | ~ | ~ 阿肯色河 | ✗ | ✗ | ✗ | ~ | 2.5/7 |
| 印度河 Indus | ~ 南流，喀布爾河西來，但不轉東 | ~ | ✗ | ✗ | ✗ | ~ 恆河 | ✗ | 1.5/7 |
| 尼羅河 Nile | ~ 加扎勒河西來、索巴特河東來，但北流 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 0.5/7 |
| 恆河 Ganges | ✗ | ~ 亞穆納河 | ✗ | ~ 宋河 | ✗ | ~ 布拉馬普特拉河 | ✗ | 1.5/7 |
| 兩河 Tigris–Euphrates | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ~ 扎布河 | 1/7 |
| 多瑙河 Danube | ✗ | ~ | ✗ | ✗ | ✗ | ✗ | ✗ | 0.5/7 |

**對照集**：上表 7 個大流域。最佳對手只得 2.5/7。7 項特徵的組合在世界大河中只有一個流域全部滿足，記 E3。/ **Comparison set**: the seven basins above; the best rival scores 2.5/7. Only one basin satisfies the full combination, hence E3.

### 4.2 GEO・方位 — **E2 (+0.5)**
以水文角色選錨點（某支流的源頭，而不是同名的山），比較同篇兩錨點之間的文本方向與實際方向（[calibration-adjacent.md](calibration-adjacent.md)）。/ Anchors chosen by hydrological role (the source of a given tributary, not a same-named mountain).

- 不重疊的相鄰錨點對（8 對）：平均方位殘差 **56°**（無資訊時期望 90°），p = 0.03；**置換檢驗 p = 0.012**，也就是「把這些實際地點配給這些站點」比隨機配對好。/ 8 non-overlapping adjacent pairs: mean residual **56°** (90° expected without information), p = 0.03; **permutation p = 0.012**.
- 只用水文角色錨點（5 對）：49°，p = 0.04；置換 p = 0.03。/ Hydrological-role anchors only (5 pairs): 49°, p = 0.04; permutation p = 0.03.
- 最佳例子 / Best cases：少山（清漳源）→ 泰戲之山（滹沱源）殘差 3°；涇谷之山（涇源）→ 鳥鼠同穴之山（渭源）13°；太華 → 嶓冢 24°。
- 最差例子 / Worst cases：謁戾之山（沁源）→ 發鳩之山（濁漳源）121°；白於之山 → 涇谷之山 90°。

### 4.3 GEO・尺度 — **E−1 (−0.3)**
反推的里長（長距離錨點對）/ Implied 里 from long anchor pairs:

| 篇 / Section | 反推里長 / Implied 里 |
|---|---|
| 西山經之首（太華 → 嶓冢）| 254 m（90%：207–301）|
| 西次四經（白於 → 鳥鼠）| 243 m（195–290）|
| 北次三經（長距離各對）| 93–136 m |

規格 §6.4 預先登記的合理範圍是 250–600 m。西山經的兩段剛好在下限，北次三經明顯低於下限。依規則，北次三經的尺度不合；但同一篇內各長距離對的里長**相當一致**（變異小），說明數字不是隨意的，而是系統性地比直線位移大 2–4 倍，可能是實際行走路程，或者單位不同。這一點不能事後改規則來救，所以記 E−1，另立方法發現 F-0003。
The pre-registered plausible band (spec §6.4) is 250–600 m. The two 西山經 sections sit at its lower edge; 北次三經 is clearly below. By the rule, 北次三經 fails on scale. Yet within that section the long pairs agree closely, so the numbers are not arbitrary: they run systematically 2–4× the straight-line displacement (walking distance, or a different unit). The rule is not changed after the fact to rescue the hypothesis, hence E−1, with the method issue recorded as finding F-0003.

### 4.4 BIO・溫度帶 — **E2 (+0.5)**
- 「橘」「櫾」（柑橘）只出現在中次八經（`SHJ-05-8-006`、`-010`）、中次九經（`SHJ-05-9-015`、`-016`）和中次十二經（`SHJ-05-12-007`），這三篇的溪流都流入南方水系 C 或 I；在流入幹流 T 的篇段中，一次都沒有出現。/ 橘/櫾 appear only in sections draining to the southern system (C or I) and never in a trunk-T section.
- 「鼉」只出現在 C 的源頭篇（`SHJ-05-9-002` 岷山「其中多良龜，多鼉」）。/ 鼉 appears only at the source of C.
- 外部事實：中國柑橘的傳統北界約在秦嶺–淮河一線（Wikipedia: Qinling–Huaihe Line）。也就是說，文本內部的柑橘分佈界線，與實際的氣候分界相符。/ External: the traditional northern limit of citrus in China is about the Qinling–Huai line. The text's internal citrus boundary matches the real climatic divide.
- **對照集**：任何有明顯南北溫度分界的大陸流域都可能有類似分佈，所以記 E2，不記 E3。/ **Comparison set**: any continental basin with a clear N–S thermal divide could show a similar pattern, hence E2, not E3.
- 犀、兕、象出現在中山經、西山經各篇。外部事實：全新世中國北方和中部曾有象與犀牛（Mark Elvin, *The Retreat of the Elephants*, 2004）。但它們在非洲、南亞也有，所以只記 E1，併入本通道，不另計。/ Rhinos and elephants (Holocene presence in north and central China; Elvin 2004) also fit Africa and South Asia: E1, folded into this channel.

### 4.5 TER・古河道 — **E2 (+0.5)**
北次三經有 10 條溪流「東流注于河」，而且一路北上到燕山、碣石一帶（`SHJ-03-3-037`–`044`）。若幹流 T 是黃河，那麼它當時必須沿太行山東麓向北流過華北平原再入海，而不是像今天那樣向東流入山東。外部事實：黃河在歷史上多次改道，西漢以前的下游河道經河北平原北流，在今天津一帶入渤海（Wikipedia: Course changes of the Yellow River）。這是一項從文本推出、再由地質與歷史事實驗證的預測。/ In 北次三經, ten streams flow E into 河 as far north as 燕山 and 碣石. If T is the Yellow River, it must then have run north along the Taihang front across the North China Plain, not east into Shandong as today. External: the Yellow River's pre-Western-Han lower course did run north across the Hebei plain to the sea near Tianjin. A prediction derived from the text and checked against geology and history.

海內東經的水道表也獨立支持這一點：「漳水出山陽東，東注渤海，入章武南」（`SHJ-13-1-036`），「濟水……注渤海，入齊琅槐東北」（`SHJ-13-1-033`）。濟水今已不存，其故道後來被黃河奪佔（1855 年）。/ The 海內東經 waterway list independently agrees: the Zhang and the now-vanished Ji both reached the Bohai on their own.

### 4.6 XCP・名稱延續 — **E1 (+0.2)**
渭、涇、洛、汾、沁、漳、漢、江、華山、王屋、碣石、管涔、鳥鼠、嶓冢、岷山等名稱至今仍在使用，而且位置與水文角色一致。但許多現代名稱可能是後人依據《山海經》《禹貢》命名的，存在循環論證的風險。而且以名稱選錨點時，王屋之山的方位殘差反而偏大（58°–99°）。所以只記 E1。/ These names survive at places that match their hydrological roles, but many may have been assigned later from the classics themselves (circularity risk), and the name-only anchor 王屋 actually has large residuals. Hence only E1.

### 4.7 MIN・鐵 — 不計地點分，記為年代線索 / no location score, dating clue
「鐵」在山經出現 40 次，其中中山經 24 次。外部事實：中國鐵器在春秋晚期至戰國才普及。這支持山經的成書（或至少大量記錄）不早於鐵器時代，與 §4.5 的古河道（西漢以前）一起，把觀測年代框定在約公元前 6 至前 2 世紀。`needs-citation`（鐵器普及年代），故不計分。/ 鐵 occurs 40 times. Iron became common in China only from the late Spring and Autumn to Warring States periods, which places the records in the Iron Age; together with §4.5 this brackets the observations to roughly the 6th–2nd centuries BCE. `needs-citation`, not scored.

## 5. 合計 / Tally

| 通道 / Channel | 項目 / Item | log₁₀ LR |
|---|---|---|
| HYD | 名稱遮蔽指紋 7/7 / masked fingerprint 7/7 | +1.0 |
| GEO | 方位（置換 p ≈ 0.01）/ bearings | +0.5 |
| GEO | 尺度不合預設範圍 / scale outside the pre-set band | −0.3 |
| BIO | 柑橘、鼉的溫度帶分佈 / thermal zoning of citrus and alligator | +0.5 |
| TER | 古河道預測得到證實 / ancient-course prediction confirmed | +0.5 |
| XCP | 名稱延續（大幅折減）/ name continuity (heavily discounted) | +0.2 |
| 校改 / Emendations | 無 / none | 0 |
| **合計 / Total** | | **+2.4** |

## 6. 紅隊 / Red team

1. **反例 / Counter-examples**：(a) 北次二經的方位與實際相反：管涔之山（汾源）之後的站點都「北」行，而以水文角色看應在其南（例如晉水的源頭在今太原西南）。(b) 謁戾 → 發鳩殘差 121°。(c) 西山經之首的丹水「東南流注于洛水」（`SHJ-02-1-008`），而實際的丹江流入漢江。這些已計入 §4.2 的平均殘差，未另外隱藏。/ (a) 北次二經 runs "north" from the Fen source, but the hydrological roles place its stations south; (b) a 121° residual; (c) 丹水 is said to flow into 洛水, whereas the real Dan joins the Han. All are included in the §4.2 averages.
2. **替身測試 / Decoy**：§4.2 的置換檢驗就是替身測試：把實際地點隨機重配，方位一致性就消失（p ≈ 0.01）。其他流域在 §4.1 中最多只得 2.5/7，連錨點都無法依水文角色指定。/ The permutation test in §4.2 is the decoy: shuffling the real places destroys the bearing agreement. Rival basins cannot even host role-defined anchors.
3. **基準率 / Base rate**：§4.1 的對照集是世界主要大河；§4.4 已降為 E2。/ §4.1 compares against the world's major rivers; §4.4 is already downgraded to E2.
4. **校改 / Emendations**：無。/ None.
5. **敏感度 / Sensitivity**：
   - 移除最強的 HYD（+1.0）→ +1.4，仍為 L2（四個正向通道，無 ≤ E−2）。/ Drop HYD → +1.4, still L2.
   - 把 BIO 與 TER 都降一級 → +1.9，L2。/ Downgrade BIO and TER one step → +1.9, L2.
   - 若尺度改記 E−2（−1.0）→ +1.7，但出現 E−2，依規則上限為 L1。/ Score scale as E−2 → +1.7, but an E−2 caps the verdict at L1.
   - **非盲性折減**：分析者知道傳統說法，HYD 可能被高估。HYD 減半 → +1.9，L2。/ **Non-blindness**: halve HYD → +1.9, L2.

## 7. 裁決 / Verdict

**L2（有據），上限 L3。** 合計 +2.4 超過 L3 的門檻（> 2），但敏感度分析顯示結論會在 L1–L3 之間移動，尺度問題尚未解決，而且分析不是認知上盲的。因此草稿定為 L2。
**L2 (supported), upper bound L3.** The total of +2.4 clears the L3 threshold (> 2), but the sensitivity analysis moves the verdict between L1 and L3, the scale problem is unresolved, and the analysis is not cognitively blind, so the draft grade is L2.

**真實世界意義 / Real-world meaning**：山經的核心是一份對黃河中游（晉陝峽谷到潼關、伊洛河流域、渭河流域、汾河流域）、太行山東麓（當時黃河北流）、秦嶺與漢水、岷江上游的路線記錄。它的方位資訊在統計上真實可用，里數則系統性地大於直線距離。年代約在鐵器時代、西漢以前的河道時期。
The Mountain-Classic core is a route record of the middle Yellow River (the Jin–Shaan gorge to Tongguan, the Yi–Luo, Wei and Fen basins), the Taihang front (when the Yellow River still flowed north), the Qinling and the Han, and the upper Min. Its bearings carry statistically real information; its distances run systematically longer than straight lines. The period is the Iron Age, before the Western Han change of course.

## 8. 保留的觀察 / Retained observations
- O-5：同一篇內的里數比例相當一致，但各篇之間不同（約 100 m 對 250 m）。這是各篇可能出自不同記錄者或不同單位的線索。/ The 里 scale is consistent within a section but differs between sections: possibly different recorders or units.
- O-6：北次二經自汾源「北」行，與水文角色相反。這是 X 類錯誤（方位）候選，或者錨點選錯。/ 北次二經 runs "north" from the Fen source, against the hydrological roles: a bearing-error candidate, or a wrong anchor.

## 9. 外部學說登記 / External theories registered
- `H-ext-0001`：山經「河水」下游為西漢以前經河北北流的古河道（譚其驤〈《山經》河水下游及其支流考〉，1978）。本卷宗 §4.5 的結論與之相同，但係由文本與地質事實獨立得出；前人學說本身不計分。/ The 山經 河 lower course is the pre-Han northward course through Hebei (Tan Qixiang, 1978). §4.5 reaches the same conclusion independently; the prior work itself is not scored.

## 10. 重測觸發條件 / Re-test triggers
- 以見證本讀法重新抽取里數（T-105）後，若方位或尺度結果明顯改變。/ If re-extraction with witness readings (T-105) materially changes bearings or scale.
- 加入更多水文角色錨點（中山經各篇）後，若置換檢驗失去顯著性。/ If adding more role-defined anchors makes the permutation test lose significance.
