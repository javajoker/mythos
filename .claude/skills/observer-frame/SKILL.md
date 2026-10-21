---
name: observer-frame
description: Read the bearings and distances of an ancient itinerary text from the compilers' point of origin — directions as seen from the origin, routes rebuilt from legs with an unknown start and an unknown unit length (li to km). Enforces the Zero-New-Geography Axiom for Books 6-18 (mountains/waters 100% reused from Wuzang Shanjing) and Discard-Commentary text-first principle.
---

# 觀察框架 / Observer frame（框架 v3 R9、P12）

1. **原點與圖層坐標基準**：
   - 編者所在地：中原河南商都殷墟/洛陽一帶（北緯 34.7°、東經 113.6°）。
   - **《五臧山經》（卷一至五）確立客觀地理走向、里數與水網閉環，是全書唯一的地理坐標骨架底座**。
   - **卷六至十八無新地理內容**：後續各卷（海外經、海內經、大荒經、海內經終篇）純粹描述人文邦國、神人帝陵、特產風物等，**所有山水實體 100% 複用五臧山經節點與坐標**，以五臧山經坐標系為基準進行校準和標註補充。
2. **拋棄後世注釋·文字出發**：
   - 徹底拋棄漢唐郭璞注等微縮注疏，嚴格依據經文走向與里數客觀推演：
     - 開羅吉薩金字塔群 ≡ 崑崙之丘；
     - 吉薩獅身人面像 ≡ 神陸吾 / 開明獸；
     - 紅海 ≡ 赤水；
     - 尼羅河 ≡ 黑水；
     - 西次三經直入地中海非洲板塊。
3. **路線與絕對距離**：
   - 每篇依「又{方}{N}里」累計出路線；里數是**絕對的直線距離**（不假設沿路里程），周秦漢里換算公理：**1 里 ≡ 0.400 公里**。
   - 西向橫向長征 18,924 里 ≡ 7,569.6 km ↔ 7,534 km 開羅（閉合誤差 0.47%）。
   - 東向縱向長征 18,869 里 ≡ 7,547.6 km ↔ 7,500 km 北美縱深（閉合誤差 0.63%）。
4. **輸出**：`frame.jsonl`：每站相對原點的方位、累計里數、所屬篇。
