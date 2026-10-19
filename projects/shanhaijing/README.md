# 山海經子項目 / Shanhaijing Sub-project

> 從《山海經》原文出發，不採用任何既有結論，按照可證偽的方法，判斷它在現有世界觀與宇宙觀中記錄了什麼。
> Starting from the text alone and adopting no prior conclusion, use falsifiable methods to determine what the Shanhaijing records about the world and cosmos as we know them.

## 文檔 / Documents

| 文件 / Doc | 內容 / Content |
|---|---|
| [docs/methodology-spec.md](docs/methodology-spec.md) | **研究方法規格**：S0–S9 流程、領域慣例、錯誤模型、交叉定位方法 / **Methodology spec**: S0–S9 pipeline, conventions, error model, triangulation |
| [docs/checklist.md](docs/checklist.md) | 卷宗關卡檢查清單 / dossier gate checklist |
| [docs/tasks.md](docs/tasks.md) | 任務清單與狀態 / tasks and status |
| [docs/data-model.md](docs/data-model.md) | 資料結構 / data schemas |
| [docs/source-assessment.md](docs/source-assessment.md) | 三個見證本的評估與已知問題 / the three witnesses and known issues |
| [hypotheses/](hypotheses/README.md) | 假說登記冊與卷宗 / hypothesis registry and dossiers |
| [findings/](findings/) | 已發佈的發現 / published findings |
| [data/derived/](data/derived/) | 衍生資料（可由腳本重新產生）/ derived data (regenerable) |

## 目前狀態 / Current state (2026-10-19)

- ✅ 三個見證本已入庫；869 段已編號 / 3 witnesses ingested; 869 paragraphs with IDs
- ✅ 機器對勘：2,201 處異文已歸屬到條目 / machine collation: 2,201 variants attributed to entries
- ✅ 山經抽取：447 個站點、26 個篇段總數；8 段在 ±2% 內自洽（[F-0002](findings/F-0002-mountain-itinerary-consistency.md)）/ Mountain-Classic extraction: 447 stations, 26 section totals; 8 sections consistent within ±2%
- ✅ 發現通行本含現代移段（[F-0001](findings/F-0001-base-text-modern-relocations.md)）/ found modern relocations in the base text
- ✅ [H-0001](hypotheses/H-0001/dossier.md)「崑崙在埃及」：**R（就目前表述而言否定）**，保留 4 項任何框架都必須解釋的觀察 / "Kunlun in Egypt": **R (refuted as formulated)**, with 4 retained observations every frame must explain
- ⬜ 下一步：異文分類（T-102）、明成化本工作文本（T-004）、26 段相對重建（T-402）、盲候選生成（T-610、T-611）/ next steps

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
python3 -I tools/shj/chain_fit.py --section 西次三經 --anchor 昆侖之丘 --lat 29.975 --lon 31.138
```

## 研究代理 / Agents

主持者為 `shj-lead`；專用代理為 `shj-route-reconstructor`；公共代理包括 `textual-critic`、`geo-triangulator`、`naturalist`、`adjudicator`、`devils-advocate`。詳見 [docs/architecture.md](../../docs/architecture.md)。
Led by `shj-lead`; specialist `shj-route-reconstructor`; common agents `textual-critic`, `geo-triangulator`, `naturalist`, `adjudicator`, `devils-advocate`. See [docs/architecture.md](../../docs/architecture.md).
