---
name: observer-frame
description: Read the bearings and distances of an ancient itinerary text from the compilers' point of origin — directions as seen from the origin, routes rebuilt from legs with an unknown start and an unknown unit length (li to km), all as soft constraints that cannot veto a candidate. Use when building the observer frame, testing whether a candidate lies in the stated direction, or estimating the scale of an ancient distance unit.
---

# 觀察框架 / Observer frame（框架 v3 R9、P12）

1. **原點與圖層坐標基準**：編者所在地（山海經：中原，北緯 34.7°、東經 113.6°）。《五臧山經》（卷一至五）確立客觀地理走向、里數與水網閉環，是全書唯一的地理坐標骨架網。後續各卷（海外經、海內經、大荒經）描述的人文邦國、特產風物等，均以此山經坐標系為基準進行校準和標註補充。
2. **路線與絕對距離**：每篇依「又{方}{N}里」累計出路線；里數是**絕對的直線距離**（不假設沿路里程），里的長度未知、全書共用一個，先驗範圍很寬（0.1–1 公里／里），由求解決定。/ Legs are absolute displacements in one unknown unit.
2b. **各篇獨立**：書中沒有篇與篇之間的距離，只有相對位置；每篇的起點各自錨定。篇末總數與齊全的各段合計相差超過 20% 時，以各段合計校準（R11）。/ Sections are independent; inconsistent totals are recalibrated from the legs.
3. **軟約束**：方向偏差、比例尺不合只扣分，不否決；與語義判斷相比權重較低。/ Soft, low-weight constraints.
4. **方位慣例**：前／後依 R5（前 = 東，前 = 南作對照）。/ 前／後 per R5.
5. **輸出**：`frame.jsonl`：每站相對原點的方位、累計里數、所屬篇。/ Output per station.

山海經實作：`tools/shj/era_frame.py`（規格 §4）。
