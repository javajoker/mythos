# 權重敏感度 / Weight sensitivity

每次只改一組權重，重解全書，與基準對應比較：各級別中候選不變的比例；河流另計水系不變的比例。
One weight family changed at a time; the whole book re-solved and compared with the baseline: share of mapped entities keeping their candidate, by tier, and share of waters keeping their river system.

| 變體 / variant | 設定 / setting | high (n=1) | medium (n=34) | low (n=171) | tentative (n=767) | 水系 / water system |
|---|---|---|---|---|---|---|
| repeat | `` | 100% | 100% | 100% | 100% | 100% |
| uniq×0.5 | `uniq=1.0` | 100% | 74% | 61% | 21% | 10% |
| uniq×1.5 | `uniq=3.0` | 100% | 76% | 52% | 17% | 6% |
| flow_hit×0.75 | `flow_hit=1.5` | 100% | 79% | 49% | 16% | 8% |
| flow_hit×1.5 | `flow_hit=3.0` | 100% | 79% | 46% | 15% | 8% |
| flow_miss×0.5 | `flow_miss=-0.5` | 100% | 74% | 40% | 12% | 5% |
| flow_miss×1.5 | `flow_miss=-1.5` | 100% | 82% | 43% | 14% | 12% |
| rise×0.5 | `rise_hit=0.5 rise_adj=0.15 rise_miss=-0.25` | 100% | 76% | 44% | 17% | 9% |
| rise×1.5 | `rise_hit=1.5 rise_adj=0.45 rise_miss=-0.75` | 100% | 71% | 50% | 17% | 11% |
| next×0.5 | `next_same=0.15 next_adj=0.05 next_miss=-0.15` | 100% | 82% | 50% | 15% | 10% |
| next×2 | `next_same=0.6 next_adj=0.2 next_miss=-0.6` | 100% | 62% | 44% | 13% | 8% |
| minor×0.5 | `minor_hit=0.3 minor_miss=-0.15` | 100% | 100% | 100% | 100% | 100% |
| minor×2 | `minor_hit=1.2 minor_miss=-0.6` | 100% | 100% | 100% | 100% | 100% |
| bearing×0 | `bearing_scale=0` | 100% | 65% | 45% | 13% | 3% |
| bearing×2 | `bearing_scale=2` | 100% | 71% | 48% | 23% | 15% |
| creature×0 | `creature_scale=0` | 100% | 71% | 50% | 14% | 7% |
| creature×2 | `creature_scale=2` | 100% | 79% | 39% | 13% | 8% |

高與中級別的對應在各變體中保持不變的最低比例 / lowest share of high+medium mappings unchanged: **63%**

## 重點實體 / Key entities

| 實體 | 基準 / baseline | repeat | uniq×0.5 | uniq×1.5 | flow_hit×0.75 | flow_hit×1.5 | flow_miss×0.5 | flow_miss×1.5 | rise×0.5 | rise×1.5 | next×0.5 | next×2 | minor×0.5 | minor×2 | bearing×0 | bearing×2 | creature×0 | creature×2 | 不變 / unchanged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WAT:河 | colorado (0.033) | = | missouri | yukon | amur | yellow | yellow | yangtze | yellow | amur | yellow | yellow | = | = | amur | = | mississippi | yellow | 4/17 |
| WAT:江 | orinoco (0.5) | = | = | ob | volga | = | rio_grande | = | danube | = | = | yenisei | = | = | ganges | yenisei | danube | = | 9/17 |
| WAT:渭 | amazon (0.033) | = | lena | volga | red | danube | yenisei | yellow | wei | yangtze | indus | dnieper | = | = | yenisei | parana | lena | colorado | 3/17 |
| WAT:涇 | jurua (0.0) | = | vilyuy | vetluga | da | prut | lower_tunguska | luo_henan | jing | han | shyok | pripyat | = | = | abakan | paraguay | vilyuy | green | 3/17 |
| WAT:汾 | yukon (0.1) | = | mississippi | orinoco | huai | wei | luo_henan | volga | luo_henan | yellow | wei | wei | = | = | liao | san_juan | missouri | luo_henan | 3/17 |
| WAT:洛→河 | yellow (0.167) | = | yukon | columbia | yenisei | yangtze | rhone | = | yukon | ob | amur | amur | = | = | mississippi | = | ob | irtysh | 5/17 |
| WAT:漢 | jialing (0.1) | = | om | wei | rhone | red | ohio | mississippi | platte | huai | danube | red | = | = | han | sokoto | yamuna | missouri | 3/17 |
| WAT:赤 | red (0.067) | = | yellow | jialing | han | yukon | volga | ganges | amazon | volga | yukon | yukon | = | = | jialing | yangtze | yukon | indus | 3/17 |
| WAT:黑 | rhone (0.158) | = | yangtze | mekong | indus | dnieper | mississippi | = | murray | tigris | karun | volga | = | = | yangtze | kura | tigris | irrawaddy | 4/17 |
| WAT:弱 | fen (0.084) | = | porcupine | conchos | ket | aruwimi | parana | angara | james | ket | ussuri | ussuri | = | = | snake | hun_liaoning | om | ishim | 3/17 |
| WAT:渤海 | gulf_of_mexico (0.033) | = | atlantic | atlantic | arctic | atlantic | bohai | pacific | = | atlantic | bohai | bohai | = | = | atlantic | = | atlantic | bohai | 5/17 |
| WAT:泑澤 | desert_kyzylkum (0.133) | = | aral | desert_kumtag | = | = | juyan | aral | aral | aral | aral | hamun | = | = | baikal | aral | hamun | aral | 5/17 |
| MTN:昆侖之丘 | SCN (0.004) | = | TIB | NAM | CHN | NAM | NAM | TAR | CHN | SIB | NAM | NAM | = | = | MON | NAM | NAM | TIB | 3/17 |
| CRE:羬羊 | takin (0.185) | = | argali_ibex | = | = | argali_ibex | saiga | = | = | = | saiga | saiga | = | = | saiga | = | argali_ibex | argali_ibex | 9/17 |
| CRE:文鰩魚 | pufferfish (0.009) | = | flying_fish | flying_fish | flying_fish | flying_fish | flying_fish | flying_fish | = | flying_fish | flying_fish | flying_fish | = | = | flying_fish | = | flying_fish | flying_fish | 5/17 |
| POL:毛民 | ainu (0.874) | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | = | 17/17 |
| POL:玄股 | inuit (0.169) | = | = | = | = | = | = | = | = | = | = | = | = | = | sushen_nanai | = | = | = | 16/17 |
| POL:黑齒 | austronesian (0.216) | = | = | mon_khmer_viet | = | = | = | = | = | = | = | = | = | = | = | = | = | mon_khmer_viet | 15/17 |
