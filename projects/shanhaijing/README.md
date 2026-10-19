# 山海經子項目 / Shanhaijing Sub-project

> 從《山海經》原文出發，不採用任何既有結論，按照可證偽的方法，判斷它在現有世界觀與宇宙觀中記錄了什麼。
> Starting from the text alone and adopting no prior conclusion, use falsifiable methods to determine what the Shanhaijing records about the world and cosmos as we know them.

## 文檔 / Documents

| 文件 / Doc | 內容 / Content |
|---|---|
| [docs/methodology-spec.md](docs/methodology-spec.md) | **研究方法規格**：S0–S9 流程、領域慣例、錯誤模型、交叉定位方法 / **Methodology spec**: S0–S9 pipeline, conventions, error model, triangulation |
| [docs/method-g-global.md](docs/method-g-global.md) | **方法 G：描述優先的全球比對**（全球前提、名稱遮蔽、距離僅供參考）/ **Method G: description-first global matching** |
| [docs/checklist.md](docs/checklist.md) | 卷宗關卡檢查清單 / dossier gate checklist |
| [docs/tasks.md](docs/tasks.md) | 任務清單與狀態 / tasks and status |
| [docs/data-model.md](docs/data-model.md) | 資料結構 / data schemas |
| [docs/source-assessment.md](docs/source-assessment.md) | 三個見證本的評估與已知問題 / the three witnesses and known issues |
| [hypotheses/](hypotheses/README.md) | 假說登記冊與卷宗 / hypothesis registry and dossiers |
| [reports/draft-v1.0-global.md](reports/draft-v1.0-global.md) | **完整初稿 v1.0：全書全球對照（方法 G）/ full draft v1.0: whole-book global mapping** |
| [reports/draft-v0.1.md](reports/draft-v0.1.md) | 初稿 v0.2（方法 A 為主，含方法 G 的崑崙）/ draft v0.2 (Method A, plus Method G Kunlun) |
| [findings/](findings/) | 已發佈的發現 / published findings |
| [data/derived/](data/derived/) | 衍生資料（可由腳本重新產生）/ derived data (regenerable) |

## 目前狀態 / Current state (2026-10-19)

- ✅ 三個見證本已入庫；869 段已編號 / 3 witnesses ingested; 869 paragraphs with IDs
- ✅ 機器對勘：2,026 處異文已歸屬到條目 / machine collation: 2,026 variants attributed to entries
- ✅ 山經抽取：447 個站點、26 個篇段總數；8 段在 ±2% 內自洽（[F-0002](findings/F-0002-mountain-itinerary-consistency.md)）/ Mountain-Classic extraction: 447 stations, 26 section totals; 8 sections consistent within ±2%
- ✅ 發現通行本含現代移段（[F-0001](findings/F-0001-base-text-modern-relocations.md)）/ found modern relocations in the base text
- ✅ [H-0001](hypotheses/H-0001/dossier.md)「崑崙在埃及」：**R（就目前表述而言否定）**，保留 4 項任何框架都必須解釋的觀察 / "Kunlun in Egypt": **R (refuted as formulated)**, with 4 retained observations every frame must explain
- ✅ 明成化本為序的工作文本（T-004）；8 個移段塊登記為 X3-001–008（T-104）/ Chenghua-order working text; 8 relocation blocks registered as X3-001–008
- ⏳ 異文分類首輪：1,604 / 2,021 筆自動分類，417 筆待審（T-102）/ variant classification first pass: 1,604 of 2,021 auto-classified, 417 to review
- ✅ **初稿 v0.1 真實世界解讀 / Draft v0.1 real-world interpretation → [reports/draft-v0.1.md](reports/draft-v0.1.md)**：山經核心＝黃河中下游與漢水、岷江（H-0002，L2）；崑崙＝青海湖一帶（H-0003，L1）；海內諸經＝秦至西漢知識範圍（H-0004，L2）；大荒經＝地平線曆法框架（H-0005，L1）
- ✅ **方法 G（全球、描述優先）/ Method G**：動物地圖（39 個描述比對到真實動物）；[H-0006](hypotheses/H-0006/dossier.md) 崑崙：單一地點 G-弱至中（安那托利亞／吉薩／墨西哥），尼羅河複合（吉薩＋月亮山）為候選 / animal map; Kunlun: single place weak–moderate, Nile composite a candidate
- ✅ **完整初稿 v1.0（全球對照）/ full draft v1.0**：39 篇＋9 個具名地點 對 31 個全球地區；18 篇達 G-強／中，全部在亞洲（華北華中 11、印度 5、東南亞 1、日本 1）；見 [F-0004](findings/F-0004-global-map-asia-centred.md) / all 18 strong/moderate sections in Asia
- ⬜ 下一步 / next：T-660–T-665、T-105、T-620、T-630、T-640、T-650–652、T-703（見 [tasks](docs/tasks.md)）

## 重現 / Reproduce

```bash
python3 -I tools/shj/ingest.py
```

```bash
python3 -I tools/shj/collate.py
```

```bash
python3 -I tools/shj/extract_routes.py
```

```bash
python3 -I tools/shj/align_witness.py && python3 -I tools/shj/classify_variants.py
```

```bash
python3 -I tools/shj/creatures.py && python3 -I tools/shj/animal_map.py && python3 -I tools/shj/region_match.py
```

```bash
python3 -I tools/shj/river_graph.py && python3 -I tools/shj/calibrate.py --anchors projects/shanhaijing/data/geo/anchors-yellow-yangtze.jsonl --adjacent
```

```bash
python3 -I tools/shj/chain_fit.py --section 西次三經 --anchor 昆侖之丘 --lat 29.975 --lon 31.138
```

## 研究代理 / Agents

主持者為 `shj-lead`；專用代理為 `shj-route-reconstructor`；公共代理包括 `textual-critic`、`geo-triangulator`、`naturalist`、`adjudicator`、`devils-advocate`。詳見 [docs/architecture.md](../../docs/architecture.md)。
Led by `shj-lead`; specialist `shj-route-reconstructor`; common agents `textual-critic`, `geo-triangulator`, `naturalist`, `adjudicator`, `devils-advocate`. See [docs/architecture.md](../../docs/architecture.md).
