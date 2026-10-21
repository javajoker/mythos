---
name: graph-cross-validation
description: 4D semantic cross-validation and LLM conflict resolution for Shan Hai Jing era mappings. Evaluates distances, topological networks, archaeological layers, and paleo-environments; resolves knowledge conflicts during cross-volume migration and integration strictly via LLM deductive reasoning (never programmatic heuristics); enforces the Zero-New-Geography Axiom for Books 6-18 (mountains/waters 100% reused from Wuzang Shanjing), judges errors vs variants, and triggers feedback updates to draft volumes.
---

# 4D 語義交叉驗證與衝突裁決手冊 / 4D Cross-Validation & LLM Conflict Resolution

## 一、核心公理與校準基石 (Core Axioms & Geodetic Anchors)

### 1. 【無新地理實體公理】(Zero-New-Geography Axiom)
- **《五臧山經》是唯一的地理空間基石**：前五卷確立了封閉、客觀的空間幾何、走向方位、里數（1里 ≡ 0.400公里）與水系閉環網絡。
- **卷六至卷十八無新地理內容**：後續十三卷純粹描述人文、邦國、神祇、陵墓與特產物候。
- **山水實體 100% 複用五臧山經**：
  - 卷六至卷十八提到的任何山水（如崑崙、不周、凶桑、衡山、巫山、幽都、赤水、黑水、弱水、江水、河水等），**必須強制在《五臧山經》中找到對應，並且 100% 複用其空間坐標與節點**！
  - 嚴禁在後續卷中建立獨立漂移的重複地理節點。
- **交叉驗證標竿鐵例**：
  - **崑崙之丘**：《大荒西經》之崑崙之丘與《西山經》之崑崙之丘同為埃及開羅吉薩高地金字塔群（30.0°N, 31.2°E）。
  - **赤水 ≡ 紅海 (Red Sea)**：環繞崑崙、西南流入南海之赤水，100% 複用為紅海。
  - **黑水 ≡ 尼羅河 (Nile River)**：自崑崙流出西南入海之黑水，100% 複用為古埃及尼羅河（古名 Aur/Ar 意為黑水）。
  - **神陸吾 / 開明獸 ≡ 獅身人面像 (Sphinx)**：人面虎身九尾虎爪守衛帝之下都九門，100% 複用為吉薩獅身人面像。
  - **地中海與非洲板塊**：西次三經一路向西，橫貫兩河進入地中海、埃及與北非板塊。

### 2. 【拋棄後世注釋·文字出發】(Discard Post-Han Commentary, Text-First)
- 堅決剔除漢魏郭璞注、清代考據與近現代人將山海經微縮於四川一盆地、山西一隅的狹隘附會。
- 一切論證嚴格從《山海經》原始經文字面出發，以客觀大地測量學與地質古水文作為檢驗尺度。

---

## 二、4D 多維交叉驗證體系 (4D Cross-Validation Dimensions)

1. **空間拓撲與水系閉環（Topology & Hydrology）**：
   - 驗證水流方向、分水嶺對稱性、注入大河或湖澤之拓撲自洽。
   - 杜絕水系自注或逆流等未加說明的矛盾。
2. **比例尺與物理距離（Distance & Scale）**：
   - 基於 1 里 ≡ 0.400 公里，檢驗各經山系總里數與實地宏觀地貌的幾何吻合度（歐亞非大軸 18,924 里 ↔ 7,569.6 km ↔ 7,534 km 誤差 0.47%；北美四大平行山系 18,869 里 ↔ 7,547.6 km ↔ 7,500 km 誤差 0.63%）。
3. **4000–1000 BCE 考古地層（Archaeological Synchronization）**：
   - 將經文所載金屬（銅鐵錫金銀）、美玉、陶器、彩繪、祭祀禮器與對應時代的考古發現嚴格對位（如殷墟高錫合金、良渚玉豬龍、曾侯乙編鐘、三星堆青銅神樹與象牙、吉薩金字塔群與獅身人面像）。
4. **古環境、古生物與地質變遷（Paleo-Environment & Extinctions）**：
   - 結合全新世大暖期氣候、植被北界、長江中上游古犀象群、溶洞喀斯特伏流及撒哈拉綠洲乾涸歷史進行實證。

---

## 三、知識衝突的 LLM 實質裁決機制 (Conflict Handling by LLM)

在知識遷移、跨卷整合或圖譜構建中，若出現空間、屬性或歷史認知衝突：
- **核心禁令**：**衝突裁決必須完全由 LLM 承擔，絕不用簡單的程序代碼或啟發式算法草率抹平！**
- **LLM 裁決流程**：
  1. **衝突暴露（Detection）**：明確指出衝突涉及的實體、不同卷冊原文、矛盾點（如方位不合、物產相左、地理節點未複用山經）。
  2. **多維推演（LLM Deduction）**：LLM 依據原始字面、古水文與五臧山經地理底座進行深度推論。
  3. **定性裁決（Decision）**：
     - 若後續卷出現偏離五臧山經的漂移坐標，強制歸併並複用五臧山經節點；
     - 若屬版本誤寫（如「十萬山」訛為「十五山」），確認為古訛字並說明理由；
     - 若屬認知互補，判定為同一實體的不同視角描述；
     - 若發現前期 Draft 存在分析疏漏，裁定進行草稿修訂。
  4. **反饋回寫與日誌記敘（Feedback Update & Logging）**：
     - 若裁決引發草稿修訂，由 LLM 精確更新指定草稿卷冊文件（`vol-XX.md`）；
     - 所有衝突案例、裁決依據與修訂記錄，必須嚴格記入 `findings/conflict-resolutions.md`。
