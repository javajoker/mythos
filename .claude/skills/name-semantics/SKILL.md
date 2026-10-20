---
name: name-semantics
description: Extract the semantic features carried by names in an ancient text (colours such as 赤 red or 黑 black, materials such as 玉 jade, shapes, states such as 流 flowing or 弱 weak, directions, people traits) and use them as down-weighted description features — never as identifiers and never matched against modern names. Use when building name_features, reviewing a judgment that relies on a name, or when a user says a name "means" something.
---

# 名稱語義 / Name semantics（框架 v3 P5、R10）

1. **名稱不作辨識**：同名不代表同一實體，異名不代表不同實體；辨識靠描述與關係。/ Names do not identify.
2. **名稱特徵保留**：名稱中的語義詞（顏色、材質、形狀與尺度、狀態、方位、人群特徵）抽成 `name_features`，例如「赤水」→ `colour: red`、`kind: water`。/ Semantic words become features.
3. **比實際特徵，不比今名**：「赤水」對的是**外觀為紅色**的水（泥沙、藻類、紅岩），所有這樣的水一起競爭；候選今名中的「紅」「黑」等字不加分。/ Match real features, never modern names.
4. **權重較低並標明**：名稱特徵的權重低於原文描述（規格 §6：0.4），每次使用都標「來自名稱」。/ Down-weighted and flagged.
5. **人群特徵**：「毛民」「黑齒」「羽民」等只在該族作為主語時計入。/ Ethnonym traits only for the subject.

山海經的語義詞表見 `projects/shanhaijing/docs/methodology-spec.md` §3。
