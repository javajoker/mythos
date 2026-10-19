# 真實世界候選庫 / Real-World Candidate Base

> 草稿 v2.0。每筆資料都附來源（多為 Wikipedia 條目），**在跑分程式之前提交**；之後的修改必須在提交訊息中說明原因。覆蓋全部有人居住的大陸。
> Draft v2.0. Every record cites its sources, and the base was **committed before the scoring code**; later changes must be explained in the commit message. Covers every inhabited continent.

| 檔案 / File | 筆數 / Records | 用途 / Used for |
|---|---|---|
| `regions.jsonl` | 31 | 山與地的候選；中心座標；相鄰地區（對稱）/ candidates for mountains and land features; centroids; symmetric adjacency |
| `region-properties.jsonl` | 36 | 地區的礦產、植物、地形、習俗：為 T 的地區、為 F 的地區，其餘未知 / region properties: true regions, false regions, rest unknown |
| `animals.jsonl` | 116 | 生物的候選：描述標籤、古代分佈 / creature candidates: tags and ancient ranges |
| `waters.jsonl` | 135 | 水的候選：84 條河（河源地區、河口、流域、總流向、長度、內流、終於沙漠）、24 湖、23 海、4 個沙漠終點 / water candidates |
| `cultures.jsonl` | 47 | 國族的候選：地區、中心點、習俗與食物標籤 / polity/people candidates |

## 1. 地區代碼 / Region codes

| 代碼 | 地區 | 代碼 | 地區 |
|---|---|---|---|
| NAF | 北非（埃及、馬格里布、撒哈拉）| IND | 印度次大陸 |
| EAF | 東非、非洲之角 | HIM | 喜馬拉雅南坡 |
| CAF | 中非、大湖區 | TIB | 青藏高原 |
| WAF | 西非 | TAR | 塔里木、西崑崙、帕米爾 |
| SAF | 南部非洲 | CAS | 中亞（阿姆河、錫爾河）|
| MDG | 馬達加斯加 | MON | 蒙古、阿爾泰 |
| LEV | 黎凡特、西奈 | SIB | 西伯利亞 |
| ARB | 阿拉伯半島 | CHN | 中國北部與中部 |
| MES | 美索不達米亞、扎格羅斯 | SCN | 華南 |
| IRN | 伊朗高原、裏海南岸 | KOR | 朝鮮、滿洲 |
| CAU | 高加索、亞美尼亞高原 | JPN | 日本 |
| ANA | 安那托利亞 | SEA | 東南亞 |
| MED | 地中海歐洲 | AUS | 澳洲、新幾內亞、大洋洲 |
| EUR | 溫帶歐洲 | NAM | 北美 |
| ARC | 北極、冰島 | MAM | 中美洲 |
| | | SAM | 南美 |

動物分佈另有海域代碼：`S_MED` `S_RED` `S_IND` `S_PAC` `S_ATL` `S_ARC`。/ Animal ranges also use sea codes.

## 2. 標籤詞彙 / Tag vocabulary
- 動物：體型參照（`body_*`）、部件、顏色、聲音、習性、棲地；與書中線索（`tools/shj/cues.py`）共用。/ Animals share the text-cue vocabulary.
- 地區性質：礦產 gold, silver, copper, iron, tin, jade, cinnabar, realgar, azurite_malachite, salt；植物 bamboo, citrus, mulberry, lacquer, pine, cypress, palm, jujube, peach_plum, millet, rice；地形 snow_peaks, sand_desert, barren, volcanic_fire, hot_springs, salt_lakes, sea_coast；習俗 tattoo, black_teeth, ear_ornaments, feather_dress, hairy_people, pygmy_people, dark_skin, cave_dwelling。
- 人群：上列習俗，加上 rice, millet, agriculture, fishing, seafaring, hunting, nomadic_herding, horse, fishskin_clothing, meat_diet。/ Cultures: customs plus diet and livelihood.
- 水：`type`（river／lake／sea／desert）、`flow_dir`（八方位，河源到河口的總方向）、`mouth`（河口所入的水體 ID）、`basin`（流域地區）、`endorheic`、`ends_in_desert`。

## 3. 判定原則 / Principles
- 只記古代已存在或可見的情況（例如古代動物分佈、公元前的栽培、古代記載的習俗）。/ Only conditions existing or visible in antiquity.
- 不確定的一律不填（地區性質）或不列（人群標籤），計分時以基準率期望處理。/ Uncertain values are left out and scored at base-rate expectation.
