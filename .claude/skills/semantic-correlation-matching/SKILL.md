---
name: semantic-correlation-matching
description: Judge how well a real-world candidate (a site, monument, water, animal, people of the period) matches an entity described in an ancient text, attribute by attribute (appearance, colour, scale, material, function, sound, ecology, bearing, date, name features), with the names masked, evidence quoted, reasons written and several samples recorded — plus leakage probes and decoys against the model's prior knowledge. Use for candidate generation and scoring in the era-semantic method, or when asked "does X match Y?" for an ancient-text entity.
---

# 語義相關評分 / Semantic correlation matching（框架 v3 §5、規格 §6）

## 輸入必須遮蔽 / Masked input only
- 把實體名稱換成代號（例：「W-17」）；保留原文描述、**名稱特徵**（例：「名稱含『紅色』」）、關係摘要（「一端在 M-3，東南延伸，與一大水相接」）、從觀察原點的方位。/ Replace names with codes; keep description, name features, relation summary, bearing.
- 不提供任何注疏、前人比定，也不提供今名。/ No commentary, prior identifications or modern names.

## 候選生成 / Generating candidates
- 每個實體至少 3 個候選、至少來自 2 個不同大區；重點文明（若專案指定）之外，必須包含其他同時期文明或地景作為對立候選。/ ≥ 3 candidates from ≥ 2 macro-regions, rivals included.
- 候選必須在時代窗口內存在或可見；寫明年代與當時樣貌。/ Dated within the window.

## 評分 / Scoring
對每個維度輸出：`score`（0–1）、`contradiction`（真／假）、`evidence`（條目編號與原句，或 `name:字`）、`attribute`（候選的對應屬性）、`reason`（一句話）。無資料時 `null`：**缺失不算矛盾**。/ Per dimension: score, contradiction, evidence, attribute, reason; null when absent.

| 維度 / dimension | 要點 / notes |
|---|---|
| 外觀與形狀 / appearance | 以外觀為準（R3）：山可以是建築；「人面虎身」可以是造像 |
| 顏色 / colour | 原文與名稱特徵的顏色，對候選的**實際**顏色（泥沙、藻類、岩石、材質）|
| 尺度 / scale | 只作大小級別的比較，古代數字容許誇大與訛誤 |
| 材質與物產 / material | 金、玉、銅…對當時的產地與貿易品 |
| 功能與行為 / function | 依外觀或效果（R4）|
| 聲音 / sound | 動物叫聲的類比 |
| 生態與分佈 / ecology | **當時**的分佈（含已滅絕或已退出原分佈的物種）|
| 方位 / bearing | 從觀察原點；只作軟約束 |
| 年代 / date | 窗口外 = 不得為候選 |
| 名稱特徵 / name features | 權重較低，標明「來自名稱」|

## 禁止 / Never
- 以今名的相似作為理由（「紅海」因叫紅海而吻合）。比的是外觀為紅的水，所有紅色水體一起競爭。/ Modern-name similarity as a reason.
- 因為某個答案「有名」或「常被提起」而加分。/ Fame as evidence.

## 取樣與紀錄 / Sampling and records
- 每個判斷 3 個樣本，每次打亂候選順序；記錄 `model`、`prompt_version`、`input_hash`、`sample`。輸入不變不重判。/ Three shuffled samples, full records, re-judge only on change.
- **洩漏探測**：抽 10% 以不遮蔽的輸入重判；最佳候選改變或分數差 > 0.3 即標 `leakage`。/ 10% unmasked probes.
- **誘餌**：每批混入 5% 人工編造的描述；誘餌被高分套到熱門候選時，向紅隊報告。/ 5% decoys.

## 山海經實作 / Shanhaijing implementation
`tools/shj/era_tasks.py`（產生遮蔽任務）→ agent `semantic-matcher` → `data/derived/era/judgments.jsonl`；規格 `projects/shanhaijing/docs/methodology-spec.md` §5–§6、§9。
