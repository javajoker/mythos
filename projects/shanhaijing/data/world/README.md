# 方法 G 世界知識庫 / Method G World Knowledge Base

> 草稿 v0.1。所有值依各條目 `source` 所列的標準參考（多為 Wikipedia 條目）填寫，**在跑分之前寫入**。修改必須在提交訊息中說明原因。
> Draft v0.1. Values follow the standard references in each record's `source` (mostly Wikipedia articles) and were **written before any scoring**. Any change must be explained in its commit message.

## 1. 地區代碼 / Region codes（古代分佈 / ancient ranges）

| 代碼 | 地區 / Region | 代碼 | 地區 / Region |
|---|---|---|---|
| NAF | 北非（含埃及、馬格里布、撒哈拉）/ North Africa | IND | 印度次大陸 / Indian subcontinent |
| EAF | 東非、非洲之角（含衣索比亞）/ East Africa, Horn | HIM | 喜馬拉雅南坡 / southern Himalaya |
| CAF | 中非、大湖區 / Central Africa, Great Lakes | TIB | 青藏高原 / Tibetan Plateau |
| WAF | 西非 / West Africa | TAR | 塔里木、崑崙山西段、帕米爾 / Tarim, West Kunlun, Pamir |
| SAF | 南部非洲 / Southern Africa | CAS | 中亞（阿姆河、錫爾河、興都庫什北）/ Central Asia |
| MDG | 馬達加斯加 / Madagascar | MON | 蒙古、阿爾泰 / Mongolia, Altai |
| LEV | 黎凡特、西奈 / Levant, Sinai | SIB | 西伯利亞 / Siberia |
| ARB | 阿拉伯半島 / Arabia | CHN | 中國北部與中部 / northern & central China |
| MES | 美索不達米亞、扎格羅斯 / Mesopotamia, Zagros | SCN | 華南 / southern China |
| IRN | 伊朗高原、裏海南岸 / Iranian plateau, south Caspian | KOR | 朝鮮、滿洲 / Korea, Manchuria |
| CAU | 高加索、亞美尼亞高原 / Caucasus, Armenian Highlands | JPN | 日本 / Japan |
| ANA | 安那托利亞 / Anatolia | SEA | 東南亞 / Southeast Asia |
| MED | 地中海歐洲 / Mediterranean Europe | AUS | 澳洲、新幾內亞 / Australia, New Guinea |
| EUR | 溫帶歐洲 / temperate Europe | NAM | 北美 / North America |
| ARC | 北極、冰島 / Arctic, Iceland | MAM | 中美洲 / Mesoamerica |
| | | SAM | 南美 / South America |

海域 / Seas：`S_MED` 地中海、`S_RED` 紅海、`S_IND` 印度洋、`S_PAC` 太平洋、`S_ATL` 大西洋、`S_ARC` 北冰洋。

## 2. 動物特徵標籤 / Animal feature tags

與 `tools/shj/cues.py` 的書中線索共用同一套詞彙。/ Shared vocabulary with the text cues in `tools/shj/cues.py`.

- 體型參照 / body analogy：`body_cattle` `body_horse` `body_sheep` `body_pig` `body_dog` `body_fox` `body_wildcat` `body_ape` `body_deer` `body_rat` `body_bigcat` `body_bear` `body_snake` `body_fish` `body_fowl` `body_duck` `body_owl` `body_crow` `body_crane` `body_turtle` `body_human` `body_bee` `body_bird` `body_hare`
- 部件 / parts：`wings` `horn_one` `horns_two` `horns_four` `heads_many` `tails_many` `eye_one` `legs_four` `legs_six` `leg_one` `human_face` `long_tail` `long_arms` `mane` `tusks` `scales` `long_shaggy_hair` `quills` `elongated_four_legged` `humps` `long_neck` `trunk` `shell`
- 顏色 / colour：`striped` `spotted` `five_colours` `body_white` `body_black` `body_red` `blue_green` `head_white` `beak_red` `tail_red`
- 聲音 / sound：`sound_baby` `sound_dog` `sound_cattle` `sound_human` `sound_drum` `self_named_call` `vocal`
- 習性 / behaviour：`flies_night` `glides` `nocturnal` `dormancy` `on_land` `throws` `bipedal_gait` `man_eater` `burrow` `sea_migration` `climber` `fast_runner`
- 棲地 / habitat：`aquatic` `marine`

## 3. 地點性質標籤與門檻 / Locus property tags and thresholds

| 標籤 / Tag | 為 T 的條件 / True when |
|---|---|
| `great_peak` | 主峰 ≥ 4000 m，或為方圓 1000 km 內最高峰 / summit ≥ 4000 m or the highest within 1000 km |
| `snow_cap` | 有終年積雪或冰川 / permanent snow or glaciers |
| `river_source_major` | 150 km 內有長度 > 1000 km 的河流發源 / a river > 1000 km rises within 150 km |
| `rivers_multi_dir` | 300 km 內有 ≥ 3 條（各 > 300 km）向不同方向流出的河 / ≥ 3 rivers (> 300 km) rise within 300 km and flow in different directions |
| `desert_edge` | 300 km 內有沙海或沙丘區 / a sand sea or dune field within 300 km |
| `sea_north` | 600 km 內、北方（方位 315°–45°）有海 / a sea within 600 km to the north |
| `fire_ground` | 600 km 內有活火山、熔岩湖或長年燃燒的天然氣火 / an active volcano, lava lake or perpetual gas fire within 600 km |
| `encircling_water` | 湖、河、沼澤環繞或緊鄰山腳（< 50 km）/ a lake, river or marsh rings it or lies at its foot |
| `human_feline_colossus` | 200 km 內有公元前 500 年以前的人面貓科（或人面獸身）巨型雕像 / a pre-500 BCE monumental human-faced feline (or human-faced beast) sculpture within 200 km |
| `east_facing_colossus` | 上述雕像面向東方 / that sculpture faces east |
| `built_complex` | 100 km 內有公元前 500 年以前、有城牆或門的大型建築群 / a pre-500 BCE monumental complex with walls or gates within 100 km |
| `cave_dwelling` | 300 km 內有古代穴居傳統 / an ancient cave-dwelling tradition within 300 km |
| `sacred_mountain` | 當地古代文獻或傳統視之為神的居所 / documented ancient local tradition of a gods' abode |
| `gems_jade` | 300 km 內有古代著名的玉或寶石產地 / a famous ancient jade or gemstone source within 300 km |

值：`true` / `false` / `null`（未知或無法判定）。/ Values: true / false / null (unknown or undecidable).
