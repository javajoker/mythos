---
name: name-semantics
description: Extract colour, material, form, state, direction and people traits carried by ancient names as down-weighted semantic features, never as modern-name identifiers.
---

# 名稱語義 / Name semantics

1. **名稱不作辨識**：同名不代表同一實體，異名不代表不同實體；辨識依描述與關係。
2. **保留語義特徵**：將名稱中的顏色、材質、形狀、尺度、狀態、方位和人群特徵寫入已註冊的 `name.semantic` 屬性。
3. **比實際特徵**：例如名稱含「赤」只提供紅色語義，候選必須以實際顏色、泥沙、藻類或材料比較；今名含相同字不加分。
4. **低權重並標記**：名稱特徵低於原文直接描述，每個判斷標明哪些分數來自名稱。
5. **人群特徵有主語限制**：族名中的毛、黑齒、羽等只在該族作為描述主語時使用。
6. **異體不進 ID**：名稱、異體與規範名放在 `names`，不改寫穩定節點 ID。
7. **古代通用詞義**：允許觀察替代和類別泛化；「山、水、丘」先按外觀與通用語義理解，不以現代狹窄分類否決。所有候選使用相同寬容。
8. **禁止因果倒置**：後世可能借用古名命名現實地理，今名不能反向證明原文位置或成書原因。

具體詞表屬於語料設定，公共 skill 不保存任何語料的現實對應答案。
