---
name: observer-frame
description: Read the bearings and distances of an ancient itinerary text from the compilers' point of origin — directions as seen from the origin, routes rebuilt from legs with an unknown start and an unknown unit length (li to km), all as soft constraints that cannot veto a candidate. Use when building the observer frame, testing whether a candidate lies in the stated direction, or estimating the scale of an ancient distance unit.
---

# 觀察框架 / Observer frame（框架 v3 R9、P12）

1. **原點**：編者所在地（山海經：中原，北緯 34.7°、東經 113.6°）。書名、篇名的方位（南、西、北、東、中、海外、海內、大荒）從原點理解。/ The origin frames book directions.
2. **路線**：每篇依「又{方}{N}里」累計出相對路線；起點與比例尺（里 → 公里）都是未知數，比例尺的先驗範圍很寬（0.1–1 公里／里），由求解決定。/ Routes from legs, unknown start and scale.
3. **軟約束**：方向偏差、比例尺不合只扣分，不否決；與語義判斷相比權重較低。/ Soft, low-weight constraints.
4. **方位慣例**：前／後依 R5（前 = 東，前 = 南作對照）。/ 前／後 per R5.
5. **輸出**：`frame.jsonl`：每站相對原點的方位、累計里數、所屬篇。/ Output per station.

山海經實作：`tools/shj/era_frame.py`（規格 §4）。
