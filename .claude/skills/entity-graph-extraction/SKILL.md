---
name: entity-graph-extraction
description: Turn LLM-reasoned draft volumes of the Shan Hai Jing into a structured Knowledge Graph — extract standardized entities and topological relations directly from finalized draft volumes (Phase 2), figure out new associative and deductive properties, identify and integrate identical entities across books via R15 distance rules, and maintain 100% paragraph coverage.
---

# 知識圖譜抽提與多維屬性生成 / Entity Graph Extraction & Knowledge Graph Synthesis（階段二）

## 一、核心定位與原則
- **階段二作業**：實體圖譜抽提嚴格基於由 LLM 深度解讀完成的 Draft Volumes（`vol-01` 至 `vol-18`），將高質量的非結構化草稿轉化為高保真結構化知識圖譜。
- **全要素覆蓋**：全書 869 段原文涉及的所有實體（山、水、地、國族、人物神祇、動物生物、植物、礦物、器物禮器、天象、氣候）無一遺漏。
- **名實分離與符號性**：名稱為符號，不預設今名；同名異地依據 R15 距離法則分立；近距離跨卷描述則進行超集節點合併。

## 二、新屬性挖掘規範 (New Properties Induction)
1. **聯想性屬性（Associative Properties）**：
   - **圖騰信仰聯想**：如「鳥身人面」與江漢天門石家河文化「玉羽人」及楚鳳崇拜的關聯；「彘身人首」與長江下游凌家灘-良渚文化「玉豬龍」的關聯。
   - **神話流變聯想**：如姑媱之山「女尸化䔄草」與戰國《楚辭》「巫山神女瑤姬」之演進淵源。
2. **演繹性推理屬性（Deductive Properties）**：
   - **生態位適應演繹**：如「䱱魚白足對長距」演繹為深澗冷水古大鯢特異種；「白身赤首蛫」演繹為近水特種平胸龜之辟火神化。
   - **工藝材料功能演繹**：如「羊桃方莖為皮張」演繹為新石器皮革鞣製張緊用韌皮；「椆杻橿木」演繹為車軸與地下採礦木支護耐磨木料。
   - **藥用理化機制演繹**：如「穿山甲（獜）食者不風」演繹為搜風通絡傳統藥理；「嘉榮草不霆」演繹為抗驚厥鎮定草藥。

## 三、跨卷實體辨識與整合 (Cross-Book Entity Integration)
- 遵循 **R15 距離仲裁法則**：
  1. **遠距離同名分立（Far-Distance Homonym Split）**：
     - 若同名實體物理距離跨越數千公里不同板塊（如《西次三經》開羅崑崙 vs 《西次一經》西域崑崙），圖譜中必須建立不同實體節點（如 `MTN:崑崙_埃及吉薩` 與 `MTN:崑崙_于闐`）。
  2. **近距離跨卷合併（Proximate Trans-Book Merge）**：
     - 若同名實體處於相容之宏觀地理板塊（如《西山經》崑崙之丘與《大荒西經》崑崙之丘），圖譜判定為同一物理實體，進行節點合流，屬性整合為超集，並標註不同卷冊視角。

## 四、圖譜數據結構規範
- **實體節點表 (`nodes.jsonl`)**：
  - `id`: 實體唯一標識（如 `MTN:05-07-010-泰室山`）
  - `canonical_name`: 規範正體名稱
  - `category`: 實體分類（MTN/WAT/LND/POL/PER/CRE/PLA/MIN/OBJ/AST/CLIM）
  - `coordinates_era`: 4000–1000 BCE 坐標
  - `era_entity`: 考古遺址或古生物化石映射
  - `temporal_state`: 時代存續狀態（存續/荒廢/絕滅/改道）
  - `associative_properties`: 聯想圖騰與文化屬性列表
  - `deductive_properties`: 演繹功能與生態工藝屬性列表
  - `cross_refs`: 出現的所有段落 ID（如 `["SHJ-05-7-010", "SHJ-05-7-020"]`）
- **關聯邊表 (`edges.jsonl`)**：
  - `source`, `target`, `relation_type` (`rises_at`, `flows_into`, `adjacent_to`, `same_entity_as`, `produces`, `inhabits`, `worships`)
  - `evidence_para_ids`: 證據段落編號
