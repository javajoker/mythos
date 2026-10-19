# 權重敏感度 / Weight sensitivity

每次只改一組權重，重解全書，與基準對應比較：各級別中候選不變的比例；河流另計水系不變的比例。
One weight family changed at a time; the whole book re-solved and compared with the baseline: share of mapped entities keeping their candidate, by tier, and share of waters keeping their river system.

| 變體 / variant | 設定 / setting | high (n=2) | medium (n=24) | low (n=131) | tentative (n=842) | 水系 / water system |
|---|---|---|---|---|---|---|
| repeat | `` | 100% | 100% | 100% | 100% | 100% |
| uniq×0.5 | `uniq=1.0` | 100% | 83% | 50% | 12% | 1% |
| uniq×1.5 | `uniq=3.0` | 100% | 88% | 57% | 13% | 5% |
| flow_hit×0.75 | `flow_hit=1.5` | 100% | 96% | 58% | 13% | 2% |
| flow_hit×1.5 | `flow_hit=3.0` | 100% | 88% | 50% | 11% | 0% |
| flow_miss×0.5 | `flow_miss=-0.5` | 100% | 88% | 55% | 14% | 6% |
| flow_miss×1.5 | `flow_miss=-1.5` | 100% | 79% | 37% | 10% | 2% |
| rise×0.5 | `rise_hit=0.5 rise_adj=0.15 rise_miss=-0.25` | 100% | 100% | 51% | 12% | 4% |
| rise×1.5 | `rise_hit=1.5 rise_adj=0.45 rise_miss=-0.75` | 100% | 96% | 51% | 13% | 7% |
| next×0.5 | `next_same=0.15 next_adj=0.05 next_miss=-0.15` | 100% | 96% | 58% | 12% | 2% |
| next×2 | `next_same=0.6 next_adj=0.2 next_miss=-0.6` | 100% | 92% | 53% | 13% | 4% |
| minor×0.5 | `minor_hit=0.3 minor_miss=-0.15` | 100% | 100% | 100% | 100% | 100% |
| minor×2 | `minor_hit=1.2 minor_miss=-0.6` | 100% | 100% | 100% | 100% | 100% |
| bearing×0 | `bearing_scale=0` | 100% | 96% | 52% | 12% | 5% |
| bearing×2 | `bearing_scale=2` | 100% | 88% | 52% | 12% | 4% |
| creature×0 | `creature_scale=0` | 100% | 71% | 52% | 13% | 8% |
| creature×2 | `creature_scale=2` | 100% | 96% | 46% | 12% | 8% |

高與中級別的對應在各變體中保持不變的最低比例 / lowest share of high+medium mappings unchanged: **73%**

## 重點實體 / Key entities

| 實體 | 基準 / baseline | repeat | uniq×0.5 | uniq×1.5 | flow_hit×0.75 | flow_hit×1.5 | flow_miss×0.5 | flow_miss×1.5 | rise×0.5 | rise×1.5 | next×0.5 | next×2 | minor×0.5 | minor×2 | bearing×0 | bearing×2 | creature×0 | creature×2 | 不變 / unchanged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WAT:河 | atlantic (0.3) | = | yellow | = | = | yangtze | = | yellow | = | = | pacific | pacific | = | = | = | yangtze | = | = | 11/17 |
| WAT:江 | arabian_sea (0.033) | = | zambezi | mekong | danube | mediterranean | yellow | indus | mississippi | volga | lena | danube | = | = | parana | nile | huai | amur | 3/17 |
| WAT:渭 | parana (0.067) | = | lena | dnieper | pacific | lena | dnieper | yenisei | lena | lena | missouri | nile | = | = | lena | lena | amazon | yangtze | 3/17 |
| WAT:涇 | salado (0.028) | = | vilyuy | pripyat | south_china_sea | vilyuy | berezina | abakan | vilyuy | vilyuy | platte | wadi_howar | = | = | vilyuy | vilyuy | purus | han | 3/17 |
| WAT:汾 | congo (0.133) | = | luo_henan | orinoco | gulf_of_mexico | han | han | huai | = | north_sea | yukon | sea_of_japan | = | = | = | bohai | gulf_of_mexico | rhine | 5/17 |
| WAT:洛→河 | bohai (0.033) | = | yangtze | yenisei | ob | missouri | nile | atlantic | missouri | indus | atlantic | yellow | = | = | amur | yellow | mediterranean | yukon | 3/17 |
| WAT:漢 | apure (0.029) | = | dnieper | indian_ocean | wei | pacific | volga | tigris | murray | yukon | khopyor | dongting | = | = | ganges | tennessee | zeya | dnieper | 3/17 |
| WAT:赤 | jialing (0.1) | = | colorado | ob | huai | yellow | tarim | irtysh | yellow | yangtze | = | huai | = | = | yellow | ganges | bohai | huai | 4/17 |
| WAT:黑 | vakhsh (0.027) | = | volga | kura | arghandab | amur | huai | ili | huai | columbia | ili | desert_kumtag | = | = | tennessee | ghaggar_hakra | = | da | 4/17 |
| WAT:弱 | zhang (0.006) | = | da | om | hulun | san_juan | wadi_hammamat | durance | cumberland | shyok | iguazu | fen | = | = | ket | huangshui | durance | gila | 3/17 |
| WAT:渤海 | persian_gulf (0.1) | = | pacific | arabian_sea | yenisei | arabian_sea | atlantic | bohai | pacific | orinoco | indian_ocean | atlantic | = | = | niger | pacific | arabian_sea | bohai | 3/17 |
| WAT:泑澤 | desert_sahara_ergs (0.033) | = | bohai | bohai | caspian | lop_nur | colorado | desert_kyzylkum | nile | desert_kyzylkum | desert_karakum | hamun | = | = | desert_kyzylkum | zambezi | zambezi | tigris | 3/17 |
| MTN:昆侖之丘 | TAR (0.023) | = | CHN | EUR | CAS | TIB | CHN | = | CHN | NAM | CHN | CHN | = | = | NAM | HIM | = | CHN | 5/17 |
| CRE:羬羊 | serow (0.513) | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | llama | = | 16/17 |
| CRE:文鰩魚 | flying_fish (0.234) | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | 17/17 |
| POL:毛民 | ainu (0.875) | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | 17/17 |
| POL:玄股 | inuit (0.163) | = | = | = | = | = | = | = | = | = | = | = | = | = | sushen_nanai | = | = | = | 16/17 |
| POL:黑齒 | mon_khmer_viet (0.0) | = | austronesian | austronesian | austronesian | austronesian | austronesian | austronesian | austronesian | austronesian | austronesian | austronesian | = | = | = | austronesian | austronesian | austronesian | 4/17 |
