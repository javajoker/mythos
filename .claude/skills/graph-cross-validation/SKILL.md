---
name: graph-cross-validation
description: 4D semantic cross-validation and LLM conflict resolution for Shan Hai Jing era mappings. Evaluates distances, topological networks, archaeological layers, and paleo-environments; resolves knowledge conflicts during cross-volume migration and integration strictly via LLM deductive reasoning (never programmatic heuristics); judges errors vs variants, and triggers feedback updates to draft volumes.
---

# 4D 語義交叉驗證與衝突裁決手冊 / 4D Cross-Validation & LLM Conflict Resolution

## 一、4D 多維交叉驗證體系 (4D Cross-Validation Dimensions)
1. **空間拓撲與水系閉環（Topology & Hydrology）**：
   - 驗證水流方向、分水嶺對稱性、注入大河或湖澤之拓撲自洽。
   - 杜絕水系自注或逆流等未加說明的矛盾。
2. **比例尺與物理距離（Distance & Scale）**：
   - 基於周秦漢「里」（0.35–0.42 km/li），檢驗各經山系總里數與實地宏觀地貌的幾何吻合度。
3. **4000–1000 BCE 考古地層（Archaeological Synchronization）**：
   - 將經文所載金屬（銅鐵錫金銀）、美玉、陶器、彩繪、祭祀禮器與對應時代的考古發現嚴格對位（如殷墟高錫合金、良渚玉豬龍、曾侯乙梓楠木槨、三星堆象牙群）。
4. **古環境、古生物與地質變遷（Paleo-Environment & Extinctions）**：
   - 結合全新世大暖期氣候、植被北界、長江中上游古犀象群、溶洞喀斯特伏流及局部荒漠化歷史進行實證。

## 二、知識衝突的 LLM 實質裁決機制 (Conflict Handling by LLM)
在知識遷移、跨卷整合或圖譜構建中，若出現空間、屬性或歷史認知衝突：
- **核心禁令**：**衝突裁決必須完全由 LLM 承擔，絕不用簡單的程序代碼或啟發式算法草率抹平！**
- **LLM 裁決四步法**：
  1. **衝突暴露（Detection）**：明確指出衝突涉及的實體、不同卷冊原文、矛盾點（如方位不合、物產相左、距離超限）。
  2. **多維推演（LLM Deduction）**：LLM 綜合版本字形（通假/脫文）、古水文改道、視角轉換（微觀巡察 vs 宏觀四極）進行深度論證。
  3. **定性裁決（Decision）**：
     - 若屬版本誤寫（如「十萬山」訛為「十五山」），確認為古訛字並說明理由；
     - 若屬不同地理板塊同名，判定為 R15 遠距離同名分立；
     - 若屬認知互補，判定為同一實體的不同視角描述；
     - 若發現前期 Draft 存在分析疏漏，裁定進行草稿修訂。
  4. **反饋回寫與日誌記敘（Feedback Update & Logging）**：
     - 若裁決引發草稿修訂，由 LLM 精確更新指定草稿卷冊文件（`vol-XX.md`）；
     - 所有衝突案例、裁決依據與修訂記錄，必須嚴格記入 `findings/conflict-resolutions.md`。
