---
name: era-world-modelling
description: Build the world of a text's period as a candidate base — coastlines, rivers, lakes and climate as they were, civilisations and their works (cities, temples, ziggurats, pyramids, canals, statues) with dates and state (living, ruin, gone), animals with their ranges at the time including extinct or extirpated species, and peoples of the period — each card dated and sourced, added symmetrically worldwide. Use when building or auditing data/era/, answering "what existed then?", or drawing a map of the period.
---

# 時代世界建模 / Era-world modelling（框架 v3 P3、R2、R8）

## 原則 / Principles
- **時代窗口**：只收窗口內存在或可見的事物；每張卡都有 `from`、`to`（公元前為負數）與 `state`（`living`／`ruin`／`gone`）。/ Only what existed or was visible in the window, dated.
- **積累**：窗口很長時，同一地點可能有多個狀態（例：埃利都神廟各期、撒哈拉由濕轉乾），分別成卡。/ Separate cards for successive states.
- **對稱**：某類事物（運河、造像、乾河谷、已滅絕動物）一旦加入，就在全世界同類中一起加入；重點文明之外要有同時期的對照文明。/ Symmetry worldwide; rivals for focus civilisations.
- **來源**：一般性的考古與古地理概述；不引用任何對研究文本的既有詮釋。/ General sources only.
- **板塊漂移**在人類歷史尺度可忽略；寫入的是海平面、海岸線、河道、湖泊、氣候與人造地景的變化。/ Plate drift is negligible; record sea level, coasts, rivers, lakes, climate, built landscape.

## 卡片 / Cards
遺址與造物（外觀、尺度、材質、顏色、功能、朝向）、水體（顏色、走向、連接）、動物（形態、顏色、聲音、當時分佈）、人群（習俗、生業、外觀）。格式見 `projects/shanhaijing/docs/data-model.md` §5.1。/ Formats in data-model §5.1.

## 當時地圖 / Map of the period
以一個代表年代（山海經：約前 2500 年）畫海岸線、河道、乾濕界線、遺址與造物；所有輪廓注明為簡化示意，只用於繪圖。/ Schematic, for drawing only.

## 山海經實作 / Shanhaijing implementation
`projects/shanhaijing/docs/era-world.md`；`data/era/`；agents `civilization-scout`、`palaeo-geographer`。
