---
name: entity-graph-extraction
description: Turn LLM-reasoned draft volumes of the Shan Hai Jing into a structured Knowledge Graph — extract standardized entities and topological relations directly from finalized draft volumes (Phase 2), enforce the Zero-New-Geography Axiom for Books 6-18 (mountains/waters 100% reused from Wuzang Shanjing), anchor humanities and products onto Wuzang Shanjing nodes, and derive associative/deductive properties.
---

# 知識圖譜抽提與多維屬性生成 / Entity Graph Extraction & Knowledge Graph Synthesis（階段二）

## 一、核心公理與本體架構 (Core Axioms & Ontology)

### 1. 【無新地理實體公理】(Zero-New-Geography for Books 6–18)
- **《五臧山經》（卷一至五）是全書唯一的地理空間底座**：
  - 確立全部山川走向、方位里數與發源注入水系網絡骨架。
- **卷六至卷十八純屬人文與特產，絕無新地理內容**：
  - 卷六至卷十八描述的是邦國、神祇、先賢帝陵、特產風物、異獸靈木與科技發明。
  - **所有卷六至卷十八出現的山、水、澤、海實體，必須在《五臧山經》中找到對應，並且強制 100% 複用五臧山經的實體節點與空間坐標**！
  - 嚴禁為後續卷創建獨立漂移的重複地理節點。
- **實體複用與對位鐵律**：
  - **崑崙之丘**：《大荒西經》之崑崙之丘與《海內西經》之崑崙之虛，**100% 複用《西山經》崑崙之丘節點**，嚴格對應於埃及開羅吉薩高地金字塔群（30.0°N, 31.2°E）。
  - **赤水 ≡ 紅海 (Red Sea)**：崑崙東北出西南流注南海之赤水，100% 複用為紅海。
  - **黑水 ≡ 尼羅河 (Nile River)**：自崑崙流出西南入海之黑水，100% 複用為古埃及尼羅河（古名 Aur/Ar 意為黑水）。
  - **神陸吾 / 開明獸 ≡ 吉薩獅身人面像 (Sphinx)**：人面虎身九尾虎爪守衛帝之下都九門，100% 複用為獅身人面像。
  - **地中海與非洲板塊**：西次三經一路向西，橫貫兩河進入地中海、埃及與北非板塊。
  - **不周之山**：帕米爾天門／地中海亞洲地質斷裂帶。
  - **崦嵫之山**：摩洛哥大西洋日落之門。
  - **湯谷扶桑**：北美中美洲日出觀測大洋軸。
  - **章尾山燭龍**：北極圈極晝極夜極光圈。

### 2. 【拋棄後世注釋·文字出發】(Discard Post-Han Commentary, Text-First)
- 徹底拋棄漢魏郭璞注、清代經學與現代一切微縮割裂經文的注釋。
- 嚴格從《山海經》文字出發，提取客觀事實與時代語義。

---

## 二、新屬性挖掘規範 (New Properties Induction)

1. **聯想性屬性（Associative Properties）**：
   - **圖騰信仰聯想**：
     - 陸吾/開明獸（人面虎身九尾虎爪）與古埃及獅身人面像（Sphinx）法老守衛神格的跨文明聯想；
     - 「鳥身人面」與東夷少皞鳳鳥信仰及石家河文化「玉羽人」的聯想；
     - 「彘身人首」與凌家灘-良渚文化「玉豬龍」的聯想。
   - **神話流變聯想**：
     - 女尸化䔄草與戰國《楚辭》「巫山神女瑤姬」之演進淵源；
     - 刑天斷首操干戚與古蘇美爾/西亞無頭神兵神話的互證。
2. **演繹性推理屬性（Deductive Properties）**：
   - **生態位適應演繹**：
     - 幽都玄鳥玄蛇玄豹玄虎玄狐與高緯度泰加林極地動物黑化適應；
     - 巴蛇食象與長江中游全新世大暖期古菱齒象、巨蟒共存生態。
   - **工藝材料功能演繹**：
     - 番禺造舟、奚仲吉光以木為車與跨湖橋木舟、二里頭雙輪車轍工藝力學演進；
     - 殳為侯（皮侯/布侯射靶）與周代大射禮天子諸侯選士禮制；
     - 鼓延始為鍾（編鐘）與曾侯乙編鐘十二律呂體系。
   - **天文曆法功能演繹**：
     - 噎鳴生歲十有二與陶寺觀象台十三柱十二縫隙歲星/十二月天文授時。

---

## 三、圖譜數據結構規範

- **實體節點表 (`nodes.jsonl`)**：
  - `id`: 實體唯一標識（山水節點統一格式如 `MTN:SHJ-02-3-006-崑崙之丘`；人文特產節點如 `POL:SHJ-06-1-001-結匈國`, `PER:SHJ-18-1-032-奚仲`）
  - `canonical_name`: 規範正體名稱
  - `category`: 實體分類（MTN/WAT/LND/POL/PER/CRE/PLA/MIN/OBJ/AST/CLIM）
  - `is_geography_base`: 布爾值（是否屬於五臧山經地理底座，`true` 僅限卷一至五山水）
  - `anchored_shanjing_id`: 若為卷六至十八的人文/物產實體，必須指向其在五臧山經錨定的具體山水節點 ID
  - `coordinates_era`: 4000–1000 BCE 坐標
  - `era_entity`: 考古遺址、古水文或古生物化石映射
  - `temporal_state`: 時代存續狀態（存續/荒廢/絕滅/改道）
  - `associative_properties`: 聯想圖騰與文化屬性列表
  - `deductive_properties`: 演繹功能與生態工藝屬性列表
  - `cross_refs`: 出現的所有段落 ID（如 `["SHJ-02-3-006", "SHJ-11-1-010", "SHJ-16-1-020"]`）
- **關聯邊表 (`edges.jsonl`)**：
  - `source`, `target`, `relation_type` (`anchored_to`, `rises_at`, `flows_into`, `adjacent_to`, `same_entity_as`, `produces`, `inhabits`, `worships`, `invented_by`)
  - `evidence_para_ids`: 證據段落編號
