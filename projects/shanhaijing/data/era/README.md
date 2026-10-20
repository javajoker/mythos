# 時代世界庫 / Era World Base（前 4000–前 2000 年）

> 依 [era-world.md](../../docs/era-world.md) 與 skill `era-world-modelling` 建立；**在計分之前提交**，之後的修改要在提交訊息中說明原因。資料只用一般性的考古、古地理、動物學來源，不用任何對山海經的既有詮釋。
> Built per era-world.md and skill `era-world-modelling`; committed before scoring; general sources only.

## 現況 / Current state

下列檔案是**種子**：內容沿自先前整理的今日世界資料（含部分古河道、乾河谷、古運河與已滅絕動物），**尚未全部改成時代窗口內的狀態**。任務 T-V05 會逐筆加上年代（`from`、`to`）、當時樣貌（`state`）與顏色等屬性，刪去窗口外的項目，並補上遺址與造物（`sites.jsonl`）及約前 2500 年的海岸線（`palaeo-coast.json`）。
These files are **seeds** carried over from earlier present-day data (including some palaeo-rivers, dry valleys, ancient canals and extinct animals). They are **not yet converted** to the window; task T-V05 dates every record, adds state and colour, removes what lies outside the window, and adds `sites.jsonl` and `palaeo-coast.json`.

| 檔案 / File | 筆數 / Records | 用途 / Use | 待辦 / To do (T-V05) |
|---|---|---|---|
| `regions.jsonl` | 33 | 彙總用的大區（中心、相鄰；EGY、IDS 依「河谷文明自成一區」分出）/ roll-up regions | 保留 / keep |
| `region-properties.jsonl` | 38 | 大區的礦產、植物、地形、習俗 / region attributes | 改為窗口內的狀態（例：撒哈拉由濕轉乾）|
| `waters-era.jsonl` | 287 | 河、湖、海、沙漠終點、古河道、乾河谷、古運河 / waters | 加年代、顏色、當時連接；刪去窗口後才出現者（例：法老運河約前 600 年）|
| `fauna-era.jsonl` | 145 | 動物（形態標籤、分佈）/ animals | 改為窗口內的分佈；補已滅絕或已退出原分佈者 |
| `cultures-era.jsonl` | 48 | 人群與文化 / cultures | 加年代；刪去窗口外者（例：匈奴、阿克蘇姆、玻里尼西亞）；補同時期文化 |
| `coastlines-present.json` | 33 + 6 | 今日的簡化陸地輪廓，作為繪製當時地圖的底圖，只用於繪圖 / present outlines, base for drawing | 衍生 `palaeo-coast.json` |
| `sites.jsonl` | — | 遺址、地景與造物 / sites and works | 新建 / new |
| `palaeo-coast.json` | — | 約前 2500 年的海岸線、河道、乾濕界線 / coasts c. 2500 BCE | 新建 / new |

格式見 [data-model](../../docs/data-model.md) §3；地區代碼見 [conventions](../../../../docs/conventions.md)。
