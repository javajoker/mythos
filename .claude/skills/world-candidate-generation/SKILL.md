---
name: world-candidate-generation
description: Build and use a worldwide real-world base (regions with properties, waters with source/mouth/basin, animals with traits and ranges, ancient cultures with customs) and generate multiple scored real-world candidates for every entity of an ancient text from its description alone, never from its name. Use for step 3 of the entity-graph method, when adding a new region/river/animal/culture to the base, or when asked "what real things could this be?".
---

# 真實世界候選 / Real-world candidates（步驟 3）

## 原則 / Principles
- **全球範圍**：每個實體都要考慮全世界的候選，不預設地區。/ **Global**: consider worldwide candidates for every entity; no region is assumed.
- **先建庫，後計分**：真實世界庫在看結果之前定好；之後的修改要寫明理由並重跑全部。/ **Base before scoring**: fix the base before seeing results; later changes need a stated reason and a full re-run.
- **庫要平衡**：每個區域、每條大河的資料密度要相近；某河列出的支流特別多，就會吸引更多對應，要在檢查時說明。/ **Balance the base**: comparable detail per region and river; a river with many listed tributaries attracts more mappings.
- **名稱不計分**：只比描述與性質。/ **Names never score.**
- **外觀與時間**：書中所見是外觀、是當時的樣子：山可能是沙丘、方山或高大建築；水可能是任何水體；古河道、古湖與遺跡可以作候選（需資料來源，小扣分）。新增這類候選時，**全世界同類的都要加**，不只假說所在的地區。/ **Outlook and time**: candidates include dunes, mesas, built forms, any water type, palaeo-waters and relics — added worldwide, not only where a hypothesis needs them.
- **地區解析度**：若一個地區同時包含河谷文明與大片其他區域，依「河谷自成一區」規則分出（例：EGY、IDS）。/ Split regions where a river-valley civilisation sits inside a larger zone.

## 候選的種類 / Kinds of candidate
| 實體 | 候選 | 自身分數 / own score |
|---|---|---|
| 山、地 | 全球地區 | 性質（礦物、植物、地形）的稀有度加權：有 +w、確定沒有 −w、未知取基準期望 w·(2p − 1)；w = log10(N_known / N_true) + 0.05 |
| 大的水 | 河、湖、海、沙漠終點 | 流向、終點類型、規模（小權重）；外加「庫中沒有」（成本隨支流數增加） |
| 小溪 | 無 | 只經由關係（發源的山、注入的大水）起作用 |
| 生物 | 真實動物，外加「無」（複合神怪） | 描述特徵的稀有度加權覆蓋率；類別（鳥、魚）與身體形態的檢查 |
| 國族 | 古代文化，外加「證據不足」 | 習俗與生業（紋身、黑齒、食魚、騎馬…）的稀有度加權 |
| 植物、礦物 | 詞義（翻譯） | 普通名詞給詞義；專名不對應 |
| 神、人 | 不對應（非地理） | — |

## 新增庫條目 / Adding to the base
寫明來源性質（常識性地理事實，不引用任何對本書的既有詮釋）、座標、相鄰關係、流域；新增後重跑候選與交叉驗證，並在提交訊息中說明。/ State the kind of source (general geographic facts, never an existing interpretation of the book), coordinates, adjacency, basin; re-run candidates and cross-validation; explain in the commit message.

## 山海經實作 / Shanhaijing implementation
`projects/shanhaijing/data/world/`（regions、region-properties、waters、animals、cultures）；`tools/shj/kg_candidates.py`、`tools/shj/kg_common.py`。規格 §4。
