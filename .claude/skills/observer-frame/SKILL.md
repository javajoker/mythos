---
name: observer-frame
description: Rebuild ancient itinerary frames from independent sections, infer observer origins from mutually confirmable landmarks and evaluate distance scales with sensitivity rather than fixed conversion.
---

# 觀察框架 / Observer frame

1. **靜態形狀優先**：先記錄輪廓、相對位置、連接、環繞、包含、分支與分佈，再處理動態敘述。
2. **篇段獨立**：依每篇自身的「又{方}{N}里」累計相對位置。沒有文本或已接受關係時，不推定篇間距離。
3. **原點反推**：收集多個可共同確認的地標及其相對關係，比較可行原點；形成共識後以穩定 ID 寫入 `anchors.jsonl`。
4. **比例尺區間**：使用語料指定範圍擬合，不把單一換算率稱為公理。山海經 v4 的範圍是 0.35–0.42 km/里。
5. **距離不是路線證明**：里數可表示直線或行程的候選模型，必須分別記錄；總里程不直接等於地理跨度。
6. **動態關係降階**：「出、入、注」在原文中保留方向，候選比較可簡化為無方向連接；現代水流方向不得單獨否決。
7. **敏感度**：在比例尺和方位慣例變化時重新計算，報告候選是否穩定。
8. **輸出**：每站保留 entry、篇、序號、相對 x/y、原始里數與讀法狀態；地標共識和跨篇連接另存判斷記錄。

程序負責幾何計算，LLM 負責地標、連接和解釋衝突裁決。
