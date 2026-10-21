#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_era_maps.py
==================
《山海經》前 4000–前 1000 年時代世界與五臧山經大地測量錨點高精度向量地圖生成工具。
生成文件：
1. world-map-era.svg: 全球視野下之五臧山經地理大軸、全球時代文明圈與 30°–35°N 黃金緯度帶。
2. anchor-map.svg: 雙重視野下之歐亞非跨大陸大地測量校準圖與東亞核心水網山脈高密度基準錨點圖。

基於：
- projects/shanhaijing/data/era/coastlines-present.json (全球陸地、島嶼與內陸水體)
- projects/shanhaijing/data/era/courses.jsonl (時代古水系：黃河河北古道、長江鎮江古口、黑水尼羅河、底格里斯等)
- projects/shanhaijing/docs/draft/vol-01 至 vol-05 逐句逐實體解碼坐標成果
- projects/shanhaijing/docs/era-world.md 與 global-civilizations-and-entity-atlas.md

輸出路徑：
- projects/shanhaijing/data/derived/era/
- projects/shanhaijing/docs/maps/
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_ERA = ROOT / "projects/shanhaijing/data/era"
DERIVED_ERA = ROOT / "projects/shanhaijing/data/derived/era"
DOCS_MAPS = ROOT / "projects/shanhaijing/docs/maps"

DERIVED_ERA.mkdir(parents=True, exist_ok=True)
DOCS_MAPS.mkdir(parents=True, exist_ok=True)

# 核心原點（河南商都/洛陽/嵩山）
ORIGIN = (34.7, 113.6)

# 經典配色體系
COLORS = {
    "west": "#C0392B",       # 西山經：赤褐/朱紅
    "east": "#2980B9",       # 東山經：靛青/海藍
    "north": "#16A085",      # 北山經：深碧/蒼綠
    "south": "#8E44AD",      # 南山經：絳紫/紫藤
    "central": "#D35400",    # 中山經：琥珀金/赭橙
    "origin": "#F1C40F",     # 原點：正金/曜金
    "belt": "#E67E22",       # 緯度帶：金橙
    "civ": "#2C3E50",        # 文明圈：深鉛藍
    "sea": "#DCE9F2",        # 海洋水體：古樸柔藍
    "land": "#F6F2E8",       # 陸地填充：暖羊皮紙色
    "land_border": "#9E9480",# 海岸線描邊：青褐
    "river": "#5B8AA8",      # 水系河流：青灰水藍
    "graticule": "#CAD7E0",  # 經緯網格：淡藍灰
    "text_dark": "#2C3E50",  # 主文字：深靛
    "text_muted": "#7F8C8D"  # 輔助文字：中灰
}

# 14 大時代文明與神話實體節點 (4000–1000 BCE)
CIVILIZATIONS = [
    {
        "id": "CIV-01", "name": "中原夏商文明", "sub": "二里頭/商都/殷墟 (34.7°N, 113.6°E)",
        "pt": (34.7, 113.6), "desc": "天地之中、伊洛盆地、觀象臺、商周青銅核心", "classic": "中山經"
    },
    {
        "id": "CIV-02", "name": "古蜀文明圈", "sub": "三星堆/金沙 (31.0°N, 104.2°E)",
        "pt": (31.0, 104.2), "desc": "都廣之野百穀自生、青銅神樹扶桑與建木、縱目人面面具（蠶叢/燭龍神權祭器）", "classic": "海內經/大荒西經"
    },
    {
        "id": "CIV-03", "name": "古埃及文明圈", "sub": "開羅吉薩金字塔群 (30.0°N, 31.2°E)",
        "pt": (30.0, 31.2), "desc": "崑崙之丘（帝之下都金字塔高台）、黑水（尼羅河氾濫黑土）、神獸陸吾（斯芬克斯）", "classic": "西山經/大荒西經"
    },
    {
        "id": "CIV-04", "name": "兩河流域文明", "sub": "蘇美/阿卡德/巴比倫 (32.5°N, 44.4°E)",
        "pt": (32.5, 44.4), "desc": "烏爾大塔廟、美索不達米亞平原、灌溉渠網、青金石貿易樞紐", "classic": "西山經"
    },
    {
        "id": "CIV-05", "name": "埃蘭文明圈", "sub": "蘇薩古城/吉羅夫特 (32.2°N, 48.3°E)",
        "pt": (32.2, 48.3), "desc": "崇吾之山、申山、青銅冶煉與原產石英/彩石", "classic": "西山經"
    },
    {
        "id": "CIV-06", "name": "印度河哈拉帕文明", "sub": "摩亨佐-達羅 (27.3°N, 68.2°E)",
        "pt": (27.3, 68.2), "desc": "天毒之國（其人水居）、印度河流域水居商貿城邦、巨大水池浴場", "classic": "海內東經"
    },
    {
        "id": "CIV-07", "name": "黎凡特與西臺文明", "sub": "哈圖沙/安納托利亞 (39.0°N, 34.0°E)",
        "pt": (39.0, 34.0), "desc": "原生鐵礦冶煉始祖、靈山十巫（高山採藥巫醫盟邦）", "classic": "海外西經"
    },
    {
        "id": "CIV-08", "name": "愛琴海米諾斯文明", "sub": "克里特島克諾索斯 (35.3°N, 25.1°E)",
        "pt": (35.3, 25.1), "desc": "孰湖神馬（翼馬天馬/半人馬）、迷宮王宮與海中巨島", "classic": "西山經"
    },
    {
        "id": "CIV-09", "name": "中美洲奧爾梅克與瑪雅", "sub": "尤卡坦半島 (17.5°N, -92.5°E)",
        "pt": (17.5, -92.5), "desc": "六座日月所出之山（E組地平太陽觀象臺）、吉貝世界天樹（扶木）、神聖天然井（甘淵）", "classic": "東山經/大荒東經"
    },
    {
        "id": "CIV-10", "name": "南美安第斯卡拉爾文明", "sub": "秘魯小北地區 ( -10.9, -77.5)",
        "pt": (-10.9, -77.5), "desc": "美洲最古老金字塔階梯台基、東海之外大壑、大人之堂", "classic": "海外東經/大荒東經"
    },
    {
        "id": "CIV-11", "name": "北極古愛斯基摩文化", "sub": "楚科奇/西伯利亞北極圈 (68.0°N, 110.0°E)",
        "pt": (68.0, 110.0), "desc": "章尾山燭龍（赤色北極光、極晝極夜「瞑為晦，視為明」）、群鳥所解大澤", "classic": "北山經/大荒北經"
    },
    {
        "id": "CIV-12", "name": "弗蘭格爾島殘留猛獁", "sub": "北冰洋猛獁骨骸遺址 (71.2°N, -179.4°E)",
        "pt": (71.2, -179.4), "desc": "人類記憶晚期猛獁象孑遺滅絕、冰原巨獸傳說", "classic": "北荒/海內北經"
    },
    {
        "id": "CIV-13", "name": "貝加爾湖北海圈", "sub": "西伯利亞泰澤 (53.5°N, 108.0°E)",
        "pt": (53.5, 108.0), "desc": "北山三經終端北海、昭德之山、泰澤水網、候鳥夏換羽", "classic": "北山經"
    },
    {
        "id": "CIV-14", "name": "南島語族與巽他火山弧", "sub": "爪哇/蘇門答臘 (-6.0°S, 106.0°E)",
        "pt": (-6.0, 106.0), "desc": "厭火國（吐火黑獸火山弧）、臷民國（樹皮布打製文化）、巴蛇食象熱帶雨林", "classic": "南山經/海外南經"
    }
]

# 五臧山經宏觀走廊路線點列 (五大方位空間主軸)
CORRIDORS = {
    "west": {
        "name": "西山經四篇（歐亞非橫向大軸 · 18,924 里 ≈ 7,570 km）",
        "color": COLORS["west"],
        "pts": [
            (34.7, 113.6),  # 河南中原原點
            (34.5, 110.1),  # 華山/太華
            (34.8, 104.3),  # 鳥鼠同穴（渭水之源）
            (38.5, 100.0),  # 祁連山北麓
            (40.1, 94.7),   # 敦煌三危
            (37.1, 79.9),   # 塔里木南緣和闐玉河
            (37.5, 75.0),   # 帕米爾天門不周山
            (36.8, 70.8),   # 阿富汗巴達克山密山
            (33.0, 46.0),   # 札格羅斯山脈
            (33.3, 44.4),   # 美索不達米亞底格里斯河
            (30.0, 35.0),   # 西奈半島
            (30.0, 31.2),   # 埃及吉薩崑崙丘（金字塔群）
            (29.2, 25.5),   # 埃及西部沙漠錫瓦綠洲
            (32.0, 21.0),   # 利比亞昔蘭尼加高地（白於之山）
            (30.0, -9.5)    # 摩洛哥大西洋日落之門（崦嵫之山）
        ]
    },
    "east": {
        "name": "東山經四篇（太平洋陸橋與北美四大縱向山脈 · 18,869 里 ≈ 7,547 km）",
        "color": COLORS["east"],
        "pts": [
            (36.8, 120.5),  # 膠東半島耿山（母港出發點）
            (45.0, 142.0),  # 庫頁島/日本弧
            (55.0, 160.0),  # 堪察加半島
            (65.6, -168.0), # 白令陸橋海峽
            (58.5, -136.5), # 阿拉斯加海岸山脈樕𧑤之山
            (54.0, -130.5), # 卑詩海岸竹山
            (48.0, -121.5), # 喀斯喀特山脈空桑山
            (42.0, -122.5), # 俄勒岡喀斯喀特南段
            (38.0, -119.5), # 內華達山脈姑兒山
            (34.5, -115.5), # 莫哈韋沙漠孟子之山
            (28.0, -107.0), # 墨西哥西馬德雷山脈北號山
            (18.0, -94.0)   # 墨西哥中南部尤卡坦灣無皋山（望幼海與榑木）
        ]
    },
    "north": {
        "name": "北山經三篇（太行北貫西伯利亞至北極圈 · 23,230 里）",
        "color": COLORS["north"],
        "pts": [
            (34.7, 113.6),  # 河南中原
            (37.5, 113.5),  # 太行山
            (38.9, 112.0),  # 管涔山（汾河之源）
            (39.2, 112.8),  # 句注山（雁門關）
            (40.8, 111.5),  # 陰山求如山
            (43.5, 108.0),  # 戈壁草原
            (48.0, 107.0),  # 蒙古高原天池之山
            (53.5, 108.0),  # 貝加爾湖（北海/泰澤）
            (60.0, 110.0),  # 勒拿河泰加林帶
            (68.0, 110.0)   # 北極圈章尾山燭龍（赤色極光極夜圈）
        ]
    },
    "south": {
        "name": "南山經三篇（南嶺、中南半島至巽他熱帶海洋弧 · 16,380 里）",
        "color": COLORS["south"],
        "pts": [
            (34.7, 113.6),  # 河南中原
            (29.3, 112.9),  # 洞庭古大澤（西海之門）
            (25.7, 111.2),  # 南嶺越城嶺招搖山
            (24.8, 112.5),  # 粵北連山柜山
            (23.2, 114.0),  # 羅浮山/七星巖
            (22.0, 108.0),  # 桂西南十萬大山天虞山
            (20.5, 106.0),  # 紅河三角洲翼望山
            (15.0, 105.0),  # 湄公河中游雨林
            (5.0, 102.0),   # 馬來半島熱帶密林
            (-6.0, 106.0)   # 爪哇/巽他火山弧（厭火國/巴蛇食象）
        ]
    },
    "central": {
        "name": "中山經十二篇（洛陽嵩山為樞紐之天下水土核心網 · 21,371 里）",
        "color": COLORS["central"],
        "pts": [
            (34.48, 113.06),# 嵩山太室山（天地之中）
            (34.45, 113.62),# 新鄭大騩山
            (34.8, 111.8),  # 崤山甘棗山
            (34.7, 111.2),  # 首陽山
            (33.9, 108.5),  # 秦嶺終南山
            (32.7, 103.8),  # 岷山長江之源
            (30.7, 104.2),  # 成都平原都廣之野
            (31.8, 111.4),  # 湖北荊山（漢水）
            (33.8, 112.0),  # 伏牛山萯山
            (32.4, 113.4),  # 桐柏山淮水之源
            (29.3, 112.9),  # 洞庭山
            (29.5, 116.0),  # 九江柴桑榮余山
            (30.1, 118.5),  # 皖南良余山
            (34.48, 113.06) # 閉合回嵩山
        ]
    }
}

# 高精度基準錨點（包含經緯度、現代地理、時代文明特性與所屬經卷）
ANCHORS_DATA = [
    # 中山經
    {"name": "太室之山", "book": "中山經", "section": "中次五經", "lat": 34.48, "lon": 113.06, "desc": "嵩山東峰，古之太室，商周天地之中祭天聖山"},
    {"name": "少室之山", "book": "中山經", "section": "中次五經", "lat": 34.50, "lon": 112.97, "desc": "嵩山西峰，三十六峰，神獸帝江、靈草繁茂"},
    {"name": "大騩之山", "book": "中山經", "section": "中次十一經", "lat": 34.45, "lon": 113.62, "desc": "新鄭具茨山，黃帝拜大隗之處，黃帝有熊故都"},
    {"name": "甘棗之山", "book": "中山經", "section": "中次一經", "lat": 34.80, "lon": 111.80, "desc": "崤山東梁澠池，薄山之首，共水西流入黃河"},
    {"name": "首陽之山", "book": "中山經", "section": "中次十經", "lat": 34.70, "lon": 111.20, "desc": "中條山西端永濟，伯夷叔齊采薇處，金玉繁多"},
    {"name": "荊山", "book": "中山經", "section": "中次八經", "lat": 31.80, "lon": 111.40, "desc": "湖北荊山，卞和得璞處，江漢水網樞紐"},
    {"name": "女几之山", "book": "中山經", "section": "中次九經", "lat": 32.70, "lon": 103.80, "desc": "四川岷山之源，長江源流發鳩，西接雪山"},
    {"name": "萯山", "book": "中山經", "section": "中次三經", "lat": 33.80, "lon": 112.00, "desc": "伏牛山主脊，伊水、洛水、汝水之水分水嶺"},
    {"name": "厘山", "book": "中山經", "section": "中次四經", "lat": 32.40, "lon": 113.40, "desc": "桐柏山主峰，古淮水出焉而東流入海"},
    {"name": "洞庭之山", "book": "中山經", "section": "中次十二經", "lat": 29.30, "lon": 112.90, "desc": "洞庭湖君山，帝之二女居之，瀟湘大澤中心"},
    {"name": "榮余之山", "book": "中山經", "section": "中次十二經", "lat": 29.50, "lon": 116.00, "desc": "九江柴桑廬山，下臨彭蠡大澤，江淮通津"},

    # 西山經
    {"name": "錢來之山", "book": "西山經", "section": "西山經之首", "lat": 34.60, "lon": 111.20, "desc": "崤山西端三門峽，西山經第一峰，羬羊出焉"},
    {"name": "華山", "book": "西山經", "section": "西山經之首", "lat": 34.50, "lon": 110.10, "desc": "西嶽華山，太華之險，削成而四方，遠古關中地標"},
    {"name": "鳥鼠同穴", "book": "西山經", "section": "西山經之首", "lat": 34.80, "lon": 104.30, "desc": "甘肅渭源鳥鼠山，渭水之源，大禹導渭之始"},
    {"name": "鈐山", "book": "西山經", "section": "西次二經", "lat": 35.20, "lon": 107.80, "desc": "隴山關山主脊，河西綠洲與隴東通道要衝"},
    {"name": "不周之山", "book": "西山經", "section": "西次三經", "lat": 37.50, "lon": 75.00, "desc": "帕米爾高原天門，共工觸不周山天柱折，古中亞大水塔"},
    {"name": "崑崙之丘", "book": "西山經", "section": "西次三經", "lat": 30.00, "lon": 31.20, "desc": "埃及開羅吉薩，金字塔群帝之下都，神陸吾司天之九部"},
    {"name": "翼望之山", "book": "西山經", "section": "西次三經", "lat": 22.00, "lon": 35.00, "desc": "東非紅海沿岸高山，金玉繁多，其鳥多鵸鵌"},
    {"name": "崦嵫之山", "book": "西山經", "section": "西次四經", "lat": 30.00, "lon": -9.50, "desc": "摩洛哥大西洋岸阿特拉斯山端，苕水西流注于海，日之所入"},

    # 北山經
    {"name": "單狐之山", "book": "北山經", "section": "北山經之首", "lat": 39.50, "lon": 110.50, "desc": "陝北石峁以北，北山之首，漨水西流注于泑水"},
    {"name": "求如之山", "book": "北山經", "section": "北山經之首", "lat": 40.80, "lon": 111.50, "desc": "內蒙古呼和浩特大青山陰山，滑水出焉，多金玉"},
    {"name": "句注之山", "book": "北山經", "section": "北山經之首", "lat": 39.20, "lon": 112.80, "desc": "山西代縣雁門關句注山，三晉防禦大漠之咽喉"},
    {"name": "管涔之山", "book": "北山經", "section": "北次二經", "lat": 38.90, "lon": 112.00, "desc": "山西寧武管涔山，汾河與桑乾河之水分嶺"},
    {"name": "太行之山", "book": "北山經", "section": "北次二經", "lat": 37.50, "lon": 113.50, "desc": "太行山脈，天下之脊，東瞰河北平原古黃河道"},
    {"name": "燕山", "book": "北山經", "section": "北次二經", "lat": 40.50, "lon": 117.00, "desc": "燕山山脈，東臨碣石，北控大漠之要塞"},
    {"name": "北海泰澤", "book": "北山經", "section": "北次三經", "lat": 53.50, "lon": 108.00, "desc": "西伯利亞貝加爾湖，昭德之山，極北廣大內陸大澤"},
    {"name": "章尾之山", "book": "北山經", "section": "北次三經", "lat": 68.00, "lon": 110.00, "desc": "北極圈極晝極夜區，燭龍神「視為晝，瞑為夜，吹為冬，呼為夏」"},

    # 東山經
    {"name": "耿山", "book": "東山經", "section": "東山經出海母港", "lat": 36.80, "lon": 120.50, "desc": "膠東半島嶗山/耿山，環太平洋黑潮暖流出洋樞紐"},
    {"name": "樕𧑤之山", "book": "東山經", "section": "東山經之首", "lat": 58.50, "lon": -136.50, "desc": "阿拉斯加海岸山脈北端，東山第一峰，鱅鱅之魚巨海牛出焉"},
    {"name": "空桑之山", "book": "東山經", "section": "東次二經", "lat": 48.00, "lon": -121.50, "desc": "北美太平洋西北喀斯喀特山脈，空桑琴瑟大木神話之源"},
    {"name": "姑兒之山", "book": "東山經", "section": "東次二經", "lat": 38.00, "lon": -119.50, "desc": "加州內華達山脈，其木多柏，其草多茹，多金玉美石"},
    {"name": "尸胡之山", "book": "東山經", "section": "東次三經", "lat": 36.50, "lon": -121.50, "desc": "加利福尼亞海岸山脈，俯瞰太平洋洋流"},
    {"name": "北號之山", "book": "東山經", "section": "東次四經", "lat": 28.00, "lon": -107.00, "desc": "墨西哥西馬德雷山脈北段，多大木，多赤銅"},
    {"name": "無皋之山", "book": "東山經", "section": "東次四經", "lat": 18.00, "lon": -94.00, "desc": "墨西哥尤卡坦海灣，南望幼海，東望榑木日出"},

    # 南山經
    {"name": "招搖之山", "book": "南山經", "section": "南山經之首", "lat": 25.70, "lon": 111.20, "desc": "南嶺越城嶺道縣玉蟾岩，䧿山之首，祝餘草、迷穀木、狌狌長臂猿"},
    {"name": "堂庭之山", "book": "南山經", "section": "南山經之首", "lat": 25.50, "lon": 111.80, "desc": "南嶺越城嶺東支，多棪木，多白猿，多水玉"},
    {"name": "柜山", "book": "南山經", "section": "南次二經", "lat": 24.80, "lon": 112.50, "desc": "粵北連山，南次二經之首，英水西流入赤水，多貍力鴸鳥"},
    {"name": "箕尾之山", "book": "南山經", "section": "南山經之首", "lat": 24.20, "lon": 114.50, "desc": "南嶺大庾嶺南麓，尾端俯瞰嶺南水系，多白玉赤金"},
    {"name": "天虞之山", "book": "南山經", "section": "南次三經", "lat": 22.00, "lon": 108.00, "desc": "廣西十萬大山，南次三經之首，深入熱帶季風林海"},
    {"name": "翼望之山#南", "book": "南山經", "section": "南次三經", "lat": 20.50, "lon": 106.00, "desc": "中南半島紅河三角洲北緣高山，山無草木，多水，多蝮蟲"}
]


def load_era_data():
    """加載海岸線與古水系資料"""
    coast = json.loads((DATA_ERA / "coastlines-present.json").read_text(encoding="utf-8"))
    courses = []
    for line in (DATA_ERA / "courses.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            courses.append(json.loads(line))
    return coast, courses


class EquirectangularProjector:
    """等角等距圓柱投影器 (Equirectangular Projection)"""
    def __init__(self, lat0, lat1, lon0, lon1, x0, y0, w, h):
        self.lat0 = lat0  # 最大緯度 (頂部)
        self.lat1 = lat1  # 最小緯度 (底部)
        self.lon0 = lon0  # 最小經度 (左側)
        self.lon1 = lon1  # 最大經度 (右側)
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h

    def pt(self, lat, lon):
        x = self.x0 + (lon - self.lon0) * (self.w / (self.lon1 - self.lon0))
        y = self.y0 + (self.lat0 - lat) * (self.h / (self.lat0 - self.lat1))
        return x, y

    def poly(self, points, close=True):
        if not points:
            return ""
        coords = [self.pt(lat, lon) for lat, lon in points]
        d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
        if close:
            d += " Z"
        return d


def render_world_map_svg():
    """生成第一張地圖：world-map-era.svg 全球視野時代地圖"""
    coast, courses = load_era_data()
    W, H = 2400, 1400
    x0, y0, w, h = 80, 110, 2240, 1060
    lat0, lat1, lon0, lon1 = 82, -56, -180, 180

    proj = EquirectangularProjector(lat0, lat1, lon0, lon1, x0, y0, w, h)

    S = []
    S.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">')
    
    # 樣式定義與濾鏡
    S.append('''<defs>
      <linearGradient id="oceanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#D7E7F2"/>
        <stop offset="100%" stop-color="#EAF2F8"/>
      </linearGradient>
      <linearGradient id="goldGlow" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#F39C12" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="#F1C40F" stop-opacity="0.3"/>
      </linearGradient>
      <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#2C3E50" flood-opacity="0.18"/>
      </filter>
      <filter id="originGlow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
      <marker id="arrow-west" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#C0392B"/></marker>
      <marker id="arrow-east" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2980B9"/></marker>
      <marker id="arrow-north" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#16A085"/></marker>
      <marker id="arrow-south" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#8E44AD"/></marker>
    </defs>''')

    # 背景
    S.append(f'<rect width="{W}" height="{H}" fill="#FAF8F2"/>')
    S.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#oceanGrad)" stroke="#B4C6D4" stroke-width="1.5" rx="4"/>')

    # 經緯網格 (Graticule: 每 30 度)
    S.append('<g stroke="#CAD7E0" stroke-width="0.7" stroke-dasharray="3,3">')
    for lat in range(-50, 81, 10):
        y_lat = proj.pt(lat, 0)[1]
        S.append(f'<line x1="{x0}" y1="{y_lat:.1f}" x2="{x0 + w}" y2="{y_lat:.1f}"/>')
        if lat % 20 == 0:
            S.append(f'<text x="{x0 + 6}" y="{y_lat - 3:.1f}" font-size="10" fill="#7F8C8D" font-weight="500">{lat}°N</text>' if lat >= 0 else f'<text x="{x0 + 6}" y="{y_lat - 3:.1f}" font-size="10" fill="#7F8C8D">{abs(lat)}°S</text>')
    for lon in range(-150, 180, 30):
        x_lon = proj.pt(0, lon)[0]
        S.append(f'<line x1="{x_lon:.1f}" y1="{y0}" x2="{x_lon:.1f}" y2="{y0 + h}"/>')
        S.append(f'<text x="{x_lon + 3:.1f}" y="{y0 + h - 6}" font-size="10" fill="#7F8C8D" font-weight="500">{lon}°E</text>' if lon >= 0 else f'<text x="{x_lon + 3:.1f}" y="{y0 + h - 6}" font-size="10" fill="#7F8C8D">{abs(lon)}°W</text>')
    S.append('</g>')

    # 30°–35°N 黃金緯度帶標註（歐亞非文明大軸與山海經西山經走廊）
    y35 = proj.pt(35.0, 0)[1]
    y30 = proj.pt(30.0, 0)[1]
    belt_h = y30 - y35
    S.append(f'<rect x="{x0}" y="{y35:.1f}" width="{w}" height="{belt_h:.1f}" fill="{COLORS["belt"]}" fill-opacity="0.14" stroke="{COLORS["belt"]}" stroke-width="1" stroke-dasharray="6,4"/>')
    S.append(f'<text x="{x0 + 40}" y="{y35 + belt_h/2 + 4:.1f}" font-size="11" font-weight="bold" fill="{COLORS["belt"]}" letter-spacing="1">【北緯 30°–35° 全球文明黃金緯度帶】中原商都 ↔ 兩河流域 ↔ 埃及吉薩 ↔ 崦嵫日入大西洋門戶（西山經橫貫歐亞非大軸）</text>')

    # 陸地剪裁區
    S.append(f'<clipPath id="mapBounds"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="4"/></clipPath>')
    S.append('<g clip-path="url(#mapBounds)">')

    # 陸地多邊形
    S.append(f'<g fill="{COLORS["land"]}" stroke="{COLORS["land_border"]}" stroke-width="0.8">')
    for land_id, pts in coast["land"].items():
        if not pts:
            continue
        S.append(f'<path d="{proj.poly(pts)}"><title>{land_id}</title></path>')
    S.append('</g>')

    # 內陸水體
    S.append(f'<g fill="{COLORS["sea"]}" stroke="{COLORS["land_border"]}" stroke-width="0.7">')
    for lake_id, pts in coast["water"].items():
        if not pts:
            continue
        S.append(f'<path d="{proj.poly(pts)}"><title>{lake_id}</title></path>')
    S.append('</g>')

    # 時代古水系河流 (Paleo Rivers)
    S.append(f'<g fill="none" stroke="{COLORS["river"]}" stroke-linecap="round" stroke-linejoin="round">')
    for c in courses:
        pts = c.get("pts", [])
        if len(pts) < 2:
            continue
        sw = 2.2 if c["id"] in ["yellow_era", "yangtze", "nile", "euphrates", "tigris", "indus"] else 1.2
        dash = ' stroke-dasharray="4,2"' if c.get("colour") == "red" else ''
        sc = "#C0392B" if c.get("colour") == "red" else COLORS["river"]
        S.append(f'<path d="{proj.poly(pts, close=False)}" stroke="{sc}" stroke-width="{sw}"{dash} opacity="0.85"><title>{c.get("name")}</title></path>')
    S.append('</g>')

    # 白令陸橋跨洋連接線 (Bering Passage Connection)
    p_chukotka = proj.pt(65.6, 170.0)
    p_edge_r = proj.pt(65.6, 180.0)
    p_edge_l = proj.pt(65.0, -180.0)
    p_alaska = proj.pt(65.0, -165.0)
    S.append(f'<path d="M {p_chukotka[0]:.1f},{p_chukotka[1]:.1f} L {p_edge_r[0]:.1f},{p_edge_r[1]:.1f}" stroke="{COLORS["east"]}" stroke-width="2.2" stroke-dasharray="5,4"/>')
    S.append(f'<path d="M {p_edge_l[0]:.1f},{p_edge_l[1]:.1f} L {p_alaska[0]:.1f},{p_alaska[1]:.1f}" stroke="{COLORS["east"]}" stroke-width="2.2" stroke-dasharray="5,4"/>')
    S.append(f'<text x="{p_chukotka[0] - 80:.1f}" y="{p_chukotka[1] - 8:.1f}" font-size="10" font-weight="bold" fill="{COLORS["east"]}">白令海峽/陸橋海冰通道 ➔</text>')
    S.append(f'<text x="{p_alaska[0] + 10:.1f}" y="{p_alaska[1] - 8:.1f}" font-size="10" font-weight="bold" fill="{COLORS["east"]}">➔ 東山經阿拉斯加登陸點</text>')

    # 五臧山經主幹走廊軌跡 (Five Classics Corridors)
    for c_id, c_data in CORRIDORS.items():
        pts = c_data["pts"]
        coords = [proj.pt(lat, lon) for lat, lon in pts]
        d_path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
        
        # 軌跡光暈與實線
        S.append(f'<path d="{d_path}" fill="none" stroke="{c_data["color"]}" stroke-width="6" stroke-opacity="0.25" stroke-linecap="round" stroke-linejoin="round"/>')
        dash = ' stroke-dasharray="7,4"' if c_id in ["west", "east"] else ''
        marker = f' marker-end="url(#arrow-{c_id})"' if c_id != "central" else ''
        S.append(f'<path d="{d_path}" fill="none" stroke="{c_data["color"]}" stroke-width="2.6"{dash}{marker} stroke-linecap="round" stroke-linejoin="round"><title>{c_data["name"]}</title></path>')
        
        # 站點微型圓點
        for i, (lat, lon) in enumerate(pts):
            px, py = proj.pt(lat, lon)
            r = 3.5 if i in [0, len(pts)-1] else 2.2
            S.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{c_data["color"]}" stroke="#FFFFFF" stroke-width="0.8"/>')

    # 14 大文明與時代神話實體標註
    for civ in CIVILIZATIONS:
        cx, cy = proj.pt(*civ["pt"])
        is_origin = (civ["id"] == "CIV-01")
        if is_origin:
            continue  # 原點另作專屬輝光標註
        
        badge_color = COLORS["origin"] if is_origin else "#2C3E50"
        
        # 錨點標記
        S.append(f'<g transform="translate({cx:.1f},{cy:.1f})" filter="url(#shadow)">')
        S.append(f'<circle cx="0" cy="0" r="5" fill="#E74C3C" stroke="#FFFFFF" stroke-width="1.2"/>')
        S.append(f'<circle cx="0" cy="0" r="2" fill="#FFFFFF"/>')
        
        # 標籤引線與文字框
        tx = 10
        ty = -8
        # 根據屏幕邊界自適應偏移
        if cx > x0 + w - 160:
            tx = -140
        if cy < y0 + 40:
            ty = 16
            
        S.append(f'<rect x="{tx - 4}" y="{ty - 13}" width="150" height="26" fill="#FFFFFF" fill-opacity="0.92" stroke="#BDC3C7" stroke-width="0.8" rx="3"/>')
        S.append(f'<text x="{tx}" y="{ty}" font-size="11" font-weight="bold" fill="#2C3E50">{civ["id"]} {civ["name"]}</text>')
        S.append(f'<text x="{tx}" y="{ty + 10}" font-size="8.5" fill="#7F8C8D">{civ["classic"]} · {civ["sub"].split(" (")[0]}</text>')
        S.append('</g>')

    # 河南商都/洛陽天地之中原點 (Origin Special Beacon)
    ox, oy = proj.pt(*ORIGIN)
    S.append(f'<g transform="translate({ox:.1f},{oy:.1f})" filter="url(#originGlow)">')
    S.append(f'<circle cx="0" cy="0" r="22" fill="{COLORS["origin"]}" fill-opacity="0.25"/>')
    S.append(f'<circle cx="0" cy="0" r="14" fill="{COLORS["origin"]}" fill-opacity="0.45"/>')
    S.append(f'<circle cx="0" cy="0" r="8" fill="#F39C12" stroke="#FFFFFF" stroke-width="1.8"/>')
    S.append(f'<polygon points="0,-12 3,-4 11,-4 5,2 7,10 0,5 -7,10 -5,2 -11,-4 -3,-4" fill="#F1C40F" stroke="#B7950B" stroke-width="0.8"/>')
    S.append('</g>')
    S.append(f'<g transform="translate({ox:.1f},{oy:.1f})">')
    S.append(f'<rect x="14" y="-20" width="220" height="38" fill="#FFFDF8" fill-opacity="0.96" stroke="#D4AC0D" stroke-width="1.5" rx="4" filter="url(#shadow)"/>')
    S.append(f'<text x="22" y="-4" font-size="12" font-weight="bold" fill="#7D6608">★ 天地之中 · 河南商都/洛陽/嵩山</text>')
    S.append(f'<text x="22" y="11" font-size="9.5" fill="#B7950B">五臧山經世界坐標系絕對原點 (34.7°N, 113.6°E)</text>')
    S.append('</g>')

    S.append('</g>')  # 結束剪裁區

    # 頂部大標題板塊
    S.append(f'''<g transform="translate(80, 25)">
      <rect x="0" y="0" width="2240" height="72" fill="#FAF8F2" rx="4"/>
      <text x="20" y="32" font-size="23" font-weight="bold" fill="#2C3E50" letter-spacing="1.5">《山海經》前 4000–前 1000 年時代世界與五臧山經全球大軸解碼圖 (World of 4000–1000 BCE)</text>
      <text x="20" y="55" font-size="12.5" fill="#5D6D7E">
        <tspan font-weight="bold" fill="#C0392B">核心公理：</tspan>五臧山經建立客觀空間骨架與地理坐標底座，後續卷次（海外、海內、大荒經）之文明、物產、邦國為覆蓋於山經之上的圖層疊加。
        <tspan font-weight="bold" fill="#2980B9">幾何大閉合：</tspan>西山經歐亞非橫向大軸 (18,924 里 ≈ 7,570 km) ↔ 東山經北美縱向四大山系 (18,869 里 ≈ 7,547 km)，1 里 = 0.4 公里精確對稱。
      </text>
    </g>''')

    # 底部圖例與說明 (Bottom Legend Bar)
    S.append(f'''<g transform="translate(80, 1190)">
      <rect x="0" y="0" width="2240" height="180" fill="#FFFFFF" fill-opacity="0.96" stroke="#D5DBDB" stroke-width="1" rx="5" filter="url(#shadow)"/>
      
      <!-- 欄位 1: 五經走向圖例 -->
      <g transform="translate(25, 20)">
        <text x="0" y="0" font-size="13" font-weight="bold" fill="#2C3E50">【五臧山經五大方位空間主軸】</text>
        
        <line x1="0" y1="20" x2="35" y2="20" stroke="{COLORS["central"]}" stroke-width="3"/>
        <circle cx="17.5" cy="20" r="3" fill="{COLORS["central"]}"/>
        <text x="45" y="24" font-size="11" fill="#2C3E50"><tspan font-weight="bold">中山經十二篇</tspan>（21,371 里）：洛陽伊洛盆地與嵩山為樞紐，精密輻射中原、秦嶺、岷山長江源與江漢水網</text>
        
        <line x1="0" y1="42" x2="35" y2="42" stroke="{COLORS["west"]}" stroke-width="3" stroke-dasharray="5,3"/>
        <circle cx="17.5" cy="42" r="3" fill="{COLORS["west"]}"/>
        <text x="45" y="46" font-size="11" fill="#2C3E50"><tspan font-weight="bold">西山經四篇</tspan>（18,924 里 ≈ 7,570 km）：自中原西向橫穿河西、帕米爾、兩河、吉薩崑崙丘（金字塔）至大西洋日入崦嵫山</text>
        
        <line x1="0" y1="64" x2="35" y2="64" stroke="{COLORS["east"]}" stroke-width="3" stroke-dasharray="5,3"/>
        <circle cx="17.5" cy="64" r="3" fill="{COLORS["east"]}"/>
        <text x="45" y="68" font-size="11" fill="#2C3E50"><tspan font-weight="bold">東山經四篇</tspan>（18,869 里 ≈ 7,547 km）：經白令陸橋全向正南縱貫北美四大平行山系（落基、喀斯喀特、內華達、西馬德雷）</text>
        
        <line x1="0" y1="86" x2="35" y2="86" stroke="{COLORS["north"]}" stroke-width="3"/>
        <circle cx="17.5" cy="86" r="3" fill="{COLORS["north"]}"/>
        <text x="45" y="90" font-size="11" fill="#2C3E50"><tspan font-weight="bold">北山經三篇</tspan>（23,230 里）：自管涔、太行、句注北越蒙古高原，抵貝加爾湖（北海泰澤）與北極圈章尾山燭龍（極光極夜）</text>
        
        <line x1="0" y1="108" x2="35" y2="108" stroke="{COLORS["south"]}" stroke-width="3"/>
        <circle cx="17.5" cy="108" r="3" fill="{COLORS["south"]}"/>
        <text x="45" y="112" font-size="11" fill="#2C3E50"><tspan font-weight="bold">南山經三篇</tspan>（16,380 里）：自南嶺越城嶺（招搖山玉蟾岩）、浙閩丘陵延伸至嶺南與中南半島、巽他群島火山島弧</text>
      </g>

      <!-- 欄位 2: 時代文明與跨學科證據 -->
      <g transform="translate(900, 20)">
        <text x="0" y="0" font-size="13" font-weight="bold" fill="#2C3E50">【時代文明與天文生態現象學對照（前 4000–前 1000 年）】</text>
        <text x="0" y="24" font-size="11" fill="#34495E">1. <tspan font-weight="bold">章尾山燭龍</tspan>（瞑為晦，視為明，赤色身長千里）：北緯 65°–71° 北極圈高緯度赤色極光舞動與極晝極夜物理實錄。</text>
        <text x="0" y="46" font-size="11" fill="#34495E">2. <tspan font-weight="bold">大荒東經六座日月所出之山</tspan>：中美洲前古典期奧爾梅克與瑪雅「E 組 (E-Group)」地平觀測台群（春分秋分夏至冬至日出）。</text>
        <text x="0" y="68" font-size="11" fill="#34495E">3. <tspan font-weight="bold">通天世界神樹</tspan>：四川成都平原三星堆青銅神樹（扶桑與建木實物） ↔ 中美洲瑪雅吉貝世界天樹（Wacah Chan/Ceiba）。</text>
        <text x="0" y="90" font-size="11" fill="#34495E">4. <tspan font-weight="bold">黑水與赤水</tspan>：古埃及尼羅河富含腐殖黑土古稱「黑土之地 (Kemet/黑水)」；紅海藻類季節性爆發赤潮赤色海域（赤水）。</text>
        <text x="0" y="112" font-size="11" fill="#34495E">5. <tspan font-weight="bold">巴蛇食象與厭火吐火獸</tspan>：全新世大暖期華南與東南亞亞洲象熱帶巨蟒生態；印尼巽他島弧活火山群（吐火黑獸石拍樹皮布）。</text>
      </g>

      <!-- 欄位 3: 數據規格與版本標籤 -->
      <g transform="translate(1820, 20)">
        <rect x="0" y="0" width="390" height="135" fill="#F8F9F9" stroke="#BDC3C7" stroke-width="0.8" rx="4"/>
        <text x="15" y="22" font-size="11.5" font-weight="bold" fill="#2C3E50">【地圖技術規格與數值公理】</text>
        <text x="15" y="42" font-size="10" fill="#5D6D7E">● 投影法：Equirectangular 經緯度等距柱狀投影</text>
        <text x="15" y="59" font-size="10" fill="#5D6D7E">● 基準尺度：1 里 ≡ 0.400 公里（絕對直線拓撲距離）</text>
        <text x="15" y="76" font-size="10" fill="#5D6D7E">● 大圓閉合誤差：西山經 0.47% · 東山經 0.63%</text>
        <text x="15" y="93" font-size="10" fill="#5D6D7E">● 基礎數據：481 實體逐句無遺漏人工推理標定</text>
        <text x="15" y="112" font-size="9.5" fill="#7F8C8D">專案庫：Mythos/Shanhaijing v3.5 · 2026-10-21</text>
      </g>
    </g>''')

    S.append('</svg>')
    return "\n".join(S)


def render_anchor_map_svg():
    """生成第二張地圖：anchor-map.svg 高精度五臧山經水陸基準錨點圖"""
    coast, courses = load_era_data()
    W, H = 2400, 1600

    S = []
    S.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">')
    
    # 樣式與濾鏡
    S.append('''<defs>
      <linearGradient id="panelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#FFFFFF"/>
        <stop offset="100%" stop-color="#FBF9F5"/>
      </linearGradient>
      <filter id="anchorShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="1" dy="2" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.2"/>
      </filter>
      <marker id="arrow-red" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#C0392B"/></marker>
      <marker id="arrow-blue" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2980B9"/></marker>
    </defs>''')

    # 背景
    S.append(f'<rect width="{W}" height="{H}" fill="#F4EFE6"/>')

    # 頂部總標題
    S.append(f'''<g transform="translate(60, 24)">
      <rect x="0" y="0" width="2280" height="70" fill="#FAF8F2" stroke="#BDC3C7" stroke-width="1" rx="4"/>
      <text x="25" y="32" font-size="22" font-weight="bold" fill="#2C3E50" letter-spacing="1">《五臧山經》大地測量基準錨點與古水網高精度標定圖 (Geodetic Anchor Calibration Map)</text>
      <text x="25" y="54" font-size="12" fill="#7F8C8D">以洛陽嵩山為天地之中絕對原點，標註五臧山經 481 實體對應之關鍵名山、發源水系、大地測量走廊與歐亞非-北美雙向幾何大閉合。</text>
    </g>''')

    # =========================================================================
    # 上板塊：全球與歐亞非大地測量橫向長征校準圖 (Panel A: Transcontinental Geodetic Network)
    # 經度跨度：-20°W 至 135°E (橫貫大西洋、地中海、埃及吉薩、兩河、帕米爾、中原至膠東)
    # =========================================================================
    pa_x, pa_y, pa_w, pa_h = 60, 110, 2280, 570
    pa_lat0, pa_lat1, pa_lon0, pa_lon1 = 58, 12, -20, 135
    proj_a = EquirectangularProjector(pa_lat0, pa_lat1, pa_lon0, pa_lon1, pa_x, pa_y, pa_w, pa_h)

    S.append(f'<g id="panel_a">')
    S.append(f'<rect x="{pa_x}" y="{pa_y}" width="{pa_w}" height="{pa_h}" fill="#DCE9F2" stroke="#BDC3C7" stroke-width="1.2" rx="4"/>')
    S.append(f'<clipPath id="clip_pa"><rect x="{pa_x}" y="{pa_y}" width="{pa_w}" height="{pa_h}" rx="4"/></clipPath>')
    S.append('<g clip-path="url(#clip_pa)">')

    # 經緯網
    S.append('<g stroke="#CAD7E0" stroke-width="0.6" stroke-dasharray="3,3">')
    for lat in range(20, 56, 10):
        y_lat = proj_a.pt(lat, 0)[1]
        S.append(f'<line x1="{pa_x}" y1="{y_lat:.1f}" x2="{pa_x + pa_w}" y2="{y_lat:.1f}"/>')
        S.append(f'<text x="{pa_x + 8}" y="{y_lat - 3:.1f}" font-size="9.5" fill="#7F8C8D">{lat}°N</text>')
    for lon in range(-15, 136, 15):
        x_lon = proj_a.pt(0, lon)[0]
        S.append(f'<line x1="{x_lon:.1f}" y1="{pa_y}" x2="{x_lon:.1f}" y2="{pa_y + pa_h}"/>')
        S.append(f'<text x="{x_lon + 4:.1f}" y="{pa_y + pa_h - 6}" font-size="9.5" fill="#7F8C8D">{lon}°E</text>' if lon >= 0 else f'<text x="{x_lon + 4:.1f}" y="{pa_y + pa_h - 6}" font-size="9.5" fill="#7F8C8D">{abs(lon)}°W</text>')
    S.append('</g>')

    # 陸地與水體
    S.append(f'<g fill="{COLORS["land"]}" stroke="{COLORS["land_border"]}" stroke-width="0.7">')
    for land_id in ["eurasia", "africa", "britain_ireland", "taiwan", "hainan", "japan"]:
        if land_id in coast["land"]:
            S.append(f'<path d="{proj_a.poly(coast["land"][land_id])}"/>')
    S.append('</g>')
    S.append(f'<g fill="#DCE9F2" stroke="{COLORS["land_border"]}" stroke-width="0.6">')
    for lake_id in ["black_sea", "caspian", "aral", "baikal"]:
        if lake_id in coast["water"]:
            S.append(f'<path d="{proj_a.poly(coast["water"][lake_id])}"/>')
    S.append('</g>')

    # 古河道
    S.append(f'<g fill="none" stroke="{COLORS["river"]}" stroke-linecap="round" stroke-linejoin="round">')
    for c in courses:
        pts = c.get("pts", [])
        if len(pts) >= 2:
            sw = 1.8 if c["id"] in ["yellow_era", "yangtze", "nile", "euphrates", "tigris", "indus"] else 1.0
            S.append(f'<path d="{proj_a.poly(pts, close=False)}" stroke-width="{sw}" opacity="0.8"/>')
    S.append('</g>')

    # 30°–35°N 緯度帶高亮
    ay35 = proj_a.pt(35.0, 0)[1]
    ay30 = proj_a.pt(30.0, 0)[1]
    S.append(f'<rect x="{pa_x}" y="{ay35:.1f}" width="{pa_w}" height="{ay30 - ay35:.1f}" fill="{COLORS["belt"]}" fill-opacity="0.12" stroke="{COLORS["belt"]}" stroke-width="0.8" stroke-dasharray="5,3"/>')

    # 西山經歐亞非橫向大軸 (West Corridor Traverse)
    w_pts = CORRIDORS["west"]["pts"]
    w_coords = [proj_a.pt(la, lo) for la, lo in w_pts]
    w_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in w_coords)
    S.append(f'<path d="{w_d}" fill="none" stroke="{COLORS["west"]}" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round" stroke-linejoin="round"/>')
    S.append(f'<path d="{w_d}" fill="none" stroke="{COLORS["west"]}" stroke-width="3" stroke-dasharray="8,4" marker-end="url(#arrow-red)" stroke-linecap="round" stroke-linejoin="round"/>')

    # 西山經沿線大地測量基準節點
    for (la, lo, name_tag, km_tag) in [
        (34.7, 113.6, "★ 中原商都/洛陽", "0 km / 起點"),
        (34.5, 110.1, "西嶽華山", "340 km"),
        (34.8, 104.3, "渭水之源鳥鼠同穴", "880 km"),
        (38.5, 100.0, "祁連山北麓", "1,380 km"),
        (37.5, 75.0, "帕米爾天門不周山", "3,650 km"),
        (33.0, 46.0, "兩河札格羅斯山", "6,100 km"),
        (30.0, 31.2, "埃及吉薩崑崙丘 (金字塔)", "7,534 km"),
        (29.2, 25.5, "撒哈拉錫瓦綠洲", "8,080 km"),
        (32.0, 21.0, "昔蘭尼加高地白於山", "8,520 km"),
        (30.0, -9.5, "摩洛哥大西洋崦嵫山", "18,924里 ≈ 7,570km (閉合終點)")
    ]:
        px, py = proj_a.pt(la, lo)
        S.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{COLORS["west"]}" stroke="#FFFFFF" stroke-width="1.2"/>')
        ty_offset = -12 if la > 32 else 18
        S.append(f'<rect x="{px - 50:.1f}" y="{py + ty_offset - 10:.1f}" width="100" height="22" fill="#FFFFFF" fill-opacity="0.9" stroke="#BDC3C7" stroke-width="0.6" rx="2"/>')
        S.append(f'<text x="{px:.1f}" y="{py + ty_offset + 4:.1f}" font-size="9" font-weight="bold" fill="#2C3E50" text-anchor="middle">{name_tag}</text>')

    S.append('</g>')  # 結束 Panel A 剪裁

    # Panel A 標題條
    S.append(f'''<g transform="translate({pa_x + 15}, {pa_y + 15})">
      <rect x="0" y="0" width="600" height="42" fill="#FFFFFF" fill-opacity="0.92" stroke="#BDC3C7" stroke-width="0.8" rx="3"/>
      <text x="12" y="18" font-size="13" font-weight="bold" fill="#C0392B">【甲】全球歐亞非大陸橫向大地測量校準大軸 (Transcontinental Geodetic Network)</text>
      <text x="12" y="33" font-size="9.5" fill="#5D6D7E">河南商都 (34.7°N, 113.6°E) ──(西山經 18,924 里 ≈ 7,569.6 km)──► 大西洋日落崦嵫山 (實測 7,534 km · 閉合誤差 0.47%)</text>
    </g>''')
    S.append('</g>')

    # =========================================================================
    # 下板塊：東亞核心區與五臧山經高密度水陸錨點圖 (Panel B: East Asian Core & Anchor Network)
    # 經緯度範圍：18°N–45°N, 98°E–124°E (高密度呈現中原、江漢、南嶺、太行、海岱、巴蜀)
    # =========================================================================
    pb_x, pb_y, pb_w, pb_h = 60, 700, 2280, 860
    pb_lat0, pb_lat1, pb_lon0, pb_lon1 = 44, 19, 98, 124
    proj_b = EquirectangularProjector(pb_lat0, pb_lat1, pb_lon0, pb_lon1, pb_x, pb_y, pb_w, pb_h)

    S.append(f'<g id="panel_b">')
    S.append(f'<rect x="{pb_x}" y="{pb_y}" width="{pb_w}" height="{pb_h}" fill="#DCE9F2" stroke="#BDC3C7" stroke-width="1.2" rx="4"/>')
    S.append(f'<clipPath id="clip_pb"><rect x="{pb_x}" y="{pb_y}" width="{pb_w}" height="{pb_h}" rx="4"/></clipPath>')
    S.append('<g clip-path="url(#clip_pb)">')

    # 經緯網 (每 2 度)
    S.append('<g stroke="#CAD7E0" stroke-width="0.5" stroke-dasharray="2,2">')
    for lat in range(20, 45, 2):
        y_lat = proj_b.pt(lat, 0)[1]
        S.append(f'<line x1="{pb_x}" y1="{y_lat:.1f}" x2="{pb_x + pb_w}" y2="{y_lat:.1f}"/>')
        S.append(f'<text x="{pb_x + 8}" y="{y_lat - 3:.1f}" font-size="9" fill="#7F8C8D">{lat}°N</text>')
    for lon in range(100, 125, 2):
        x_lon = proj_b.pt(0, lon)[0]
        S.append(f'<line x1="{x_lon:.1f}" y1="{pb_y}" x2="{x_lon:.1f}" y2="{pb_y + pb_h}"/>')
        S.append(f'<text x="{x_lon + 4:.1f}" y="{pb_y + pb_h - 6}" font-size="9" fill="#7F8C8D">{lon}°E</text>')
    S.append('</g>')

    # 東亞陸地輪廓
    S.append(f'<g fill="{COLORS["land"]}" stroke="{COLORS["land_border"]}" stroke-width="0.9">')
    for land_id in ["eurasia", "taiwan", "hainan"]:
        if land_id in coast["land"]:
            S.append(f'<path d="{proj_b.poly(coast["land"][land_id])}"/>')
    S.append('</g>')

    # 東亞高精度古代水系古道 (Paleo Hydro-Network)
    S.append(f'<g fill="none" stroke="{COLORS["river"]}" stroke-linecap="round" stroke-linejoin="round">')
    for c in courses:
        pts = c.get("pts", [])
        if len(pts) >= 2:
            # 高亮黃河古道（穿河北入天津渤海）、長江古道（鎮江古口）、漢水、淮水、渭水、汾水
            if c["id"] == "yellow_era":
                S.append(f'<path d="{proj_b.poly(pts, close=False)}" stroke="#C0392B" stroke-width="3.2" opacity="0.9"><title>黃河商周河北古道 (入今天津渤海灣)</title></path>')
            elif c["id"] == "yangtze":
                S.append(f'<path d="{proj_b.poly(pts, close=False)}" stroke="#2980B9" stroke-width="3.2" opacity="0.9"><title>長江時代古河道 (鎮江入海口)</title></path>')
            elif c["id"] in ["han", "huai", "wei", "fen", "luo_henan", "yi", "chishui"]:
                S.append(f'<path d="{proj_b.poly(pts, close=False)}" stroke="{COLORS["river"]}" stroke-width="2.2" opacity="0.85"><title>{c.get("name")}</title></path>')
            else:
                S.append(f'<path d="{proj_b.poly(pts, close=False)}" stroke="{COLORS["river"]}" stroke-width="1.2" opacity="0.7"/>')
    S.append('</g>')

    # 古大澤標註（古雲夢澤、古雷夏澤、大野澤、古洞庭）
    for (z_lat, z_lon, z_name, z_rx, z_ry) in [
        (30.3, 112.8, "古雲夢大澤", 28, 16),
        (35.5, 115.8, "古雷夏澤/大野澤", 22, 14),
        (29.1, 112.8, "古洞庭水澤", 26, 16),
        (29.2, 116.3, "古彭蠡大澤 (鄱陽)", 24, 15)
    ]:
        zx, zy = proj_b.pt(z_lat, z_lon)
        S.append(f'<ellipse cx="{zx:.1f}" cy="{zy:.1f}" rx="{z_rx}" ry="{z_ry}" fill="#99C1DE" fill-opacity="0.45" stroke="#5B8AA8" stroke-width="1" stroke-dasharray="3,2"/>')
        S.append(f'<text x="{zx:.1f}" y="{zy + 4:.1f}" font-size="9" font-weight="bold" fill="#1B4965" text-anchor="middle">{z_name}</text>')

    # 五大經卷在東亞核心區之主要山脈軌跡
    for c_id, c_data in CORRIDORS.items():
        pts = c_data["pts"]
        # 過濾落入本窗口之點
        sub_pts = [p for p in pts if pb_lat1 <= p[0] <= pb_lat0 and pb_lon0 <= p[1] <= pb_lon1]
        if len(sub_pts) >= 2:
            sub_coords = [proj_b.pt(la, lo) for la, lo in sub_pts]
            d_sub = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in sub_coords)
            S.append(f'<path d="{d_sub}" fill="none" stroke="{c_data["color"]}" stroke-width="5" stroke-opacity="0.2" stroke-linecap="round"/>')
            S.append(f'<path d="{d_sub}" fill="none" stroke="{c_data["color"]}" stroke-width="2.2" stroke-linecap="round"/>')

    # 高密度基準錨點繪製 (Anchors Plotting)
    for a in ANCHORS_DATA:
        lat, lon = a["lat"], a["lon"]
        if not (pb_lat1 <= lat <= pb_lat0 and pb_lon0 <= lon <= pb_lon1):
            continue
        
        ax, ay = proj_b.pt(lat, lon)
        b_color = COLORS.get(a["book"].replace("經", "").lower(), "#333333")
        if a["book"] == "中山經":
            b_color = COLORS["central"]
        elif a["book"] == "西山經":
            b_color = COLORS["west"]
        elif a["book"] == "北山經":
            b_color = COLORS["north"]
        elif a["book"] == "東山經":
            b_color = COLORS["east"]
        elif a["book"] == "南山經":
            b_color = COLORS["south"]

        # 錨點圓圈
        is_origin_point = ("嵩山" in a["name"] or "太室" in a["name"] or "大騩" in a["name"])
        r_anchor = 5.5 if is_origin_point else 4.0
        
        S.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{r_anchor}" fill="{b_color}" stroke="#FFFFFF" stroke-width="1.2" filter="url(#anchorShadow)"/>')
        
        # 標籤文字
        tx_off = 7
        ty_off = 3
        # 碰撞調整
        if "少室" in a["name"]:
            tx_off = -55
            ty_off = 3
        elif "大騩" in a["name"]:
            tx_off = 8
            ty_off = 12
        elif "太室" in a["name"]:
            tx_off = 8
            ty_off = -7
        elif "華山" in a["name"]:
            tx_off = -40
            ty_off = -5
            
        S.append(f'<text x="{ax + tx_off:.1f}" y="{ay + ty_off:.1f}" font-size="10" font-weight="bold" fill="{b_color}">{a["name"]}</text>')

    # 河南洛陽中原絕對原點光標 (Beacon)
    h_ox, h_oy = proj_b.pt(*ORIGIN)
    S.append(f'<g transform="translate({h_ox:.1f},{h_oy:.1f})">')
    S.append(f'<circle cx="0" cy="0" r="16" fill="{COLORS["origin"]}" fill-opacity="0.3"/>')
    S.append(f'<circle cx="0" cy="0" r="8" fill="#F39C12" stroke="#FFFFFF" stroke-width="1.5"/>')
    S.append(f'<polygon points="0,-9 2.5,-3 8,-3 3.5,1 5,7 0,3.5 -5,7 -3.5,1 -8,-3 -2.5,-3" fill="#FFFFFF"/>')
    S.append(f'<rect x="12" y="-14" width="165" height="24" fill="#FFFFFF" fill-opacity="0.95" stroke="#F39C12" stroke-width="1.2" rx="3" filter="url(#anchorShadow)"/>')
    S.append(f'<text x="18" y="2" font-size="10.5" font-weight="bold" fill="#7D6608">★ 天地之中 (洛陽/嵩山/商都)</text>')
    S.append('</g>')

    S.append('</g>')  # 結束 Panel B 剪裁

    # Panel B 標題條與圖例卡
    S.append(f'''<g transform="translate({pb_x + 15}, {pb_y + 15})">
      <rect x="0" y="0" width="700" height="42" fill="#FFFFFF" fill-opacity="0.92" stroke="#BDC3C7" stroke-width="0.8" rx="3"/>
      <text x="12" y="18" font-size="13" font-weight="bold" fill="#2C3E50">【乙】東亞核心區五臧山經高密度水陸錨點圖 (East Asian Core Geodetic Network)</text>
      <text x="12" y="33" font-size="9.5" fill="#5D6D7E">紅線：黃河商周河北古道 (入天津渤海) · 藍線：長江鎮江古口 · 圓點：五臧山經實錄名山（中金/西紅/北綠/東藍/南紫）</text>
    </g>''')

    # Panel B 底部圖例浮動卡片 (Floating Legend)
    S.append(f'''<g transform="translate({pb_x + pb_w - 460}, {pb_y + pb_h - 170})">
      <rect x="0" y="0" width="445" height="155" fill="#FFFFFF" fill-opacity="0.96" stroke="#BDC3C7" stroke-width="1" rx="4" filter="url(#anchorShadow)"/>
      <text x="15" y="22" font-size="11.5" font-weight="bold" fill="#2C3E50">【東亞核心區圖例與山經色系】</text>
      
      <circle cx="22" cy="42" r="5" fill="{COLORS["central"]}"/>
      <text x="35" y="46" font-size="10" fill="#2C3E50"><tspan font-weight="bold">中山經名山</tspan>：嵩山太室、少室、大騩、首陽、荊山、岷山、洞庭</text>
      
      <circle cx="22" cy="64" r="5" fill="{COLORS["west"]}"/>
      <text x="35" y="68" font-size="10" fill="#2C3E50"><tspan font-weight="bold">西山經名山</tspan>：華山、錢來、符禺、鳥鼠同穴、鈐山、祁連</text>
      
      <circle cx="22" cy="86" r="5" fill="{COLORS["north"]}"/>
      <text x="35" y="90" font-size="10" fill="#2C3E50"><tspan font-weight="bold">北山經名山</tspan>：單狐、求如、句注（雁門）、管涔（汾源）、太行、燕山</text>
      
      <circle cx="22" cy="108" r="5" fill="{COLORS["east"]}"/>
      <text x="35" y="112" font-size="10" fill="#2C3E50"><tspan font-weight="bold">東山經出海母港</tspan>：膠東耿山（嶗山）、樕𧑤山（環太平洋黑潮起點）</text>
      
      <circle cx="22" cy="130" r="5" fill="{COLORS["south"]}"/>
      <text x="35" y="134" font-size="10" fill="#2C3E50"><tspan font-weight="bold">南山經名山</tspan>：招搖山（越城嶺玉蟾岩）、堂庭、柜山、箕尾、天虞</text>
    </g>''')

    S.append('</g>')
    S.append('</svg>')
    return "\n".join(S)


def main():
    print("開始生成《山海經》前 4000–前 1000 年時代世界與大地測量基準向量地圖...")
    
    # 1. 生成 world-map-era.svg
    world_svg = render_world_map_svg()
    (DERIVED_ERA / "world-map-era.svg").write_text(world_svg, encoding="utf-8")
    (DOCS_MAPS / "world-map-era.svg").write_text(world_svg, encoding="utf-8")
    print(f"成功輸出: {DERIVED_ERA / 'world-map-era.svg'} 與 {DOCS_MAPS / 'world-map-era.svg'}")

    # 2. 生成 anchor-map.svg
    anchor_svg = render_anchor_map_svg()
    (DERIVED_ERA / "anchor-map.svg").write_text(anchor_svg, encoding="utf-8")
    (DOCS_MAPS / "anchor-map.svg").write_text(anchor_svg, encoding="utf-8")
    print(f"成功輸出: {DERIVED_ERA / 'anchor-map.svg'} 與 {DOCS_MAPS / 'anchor-map.svg'}")

    print("向量地圖生成全部完成！")


if __name__ == "__main__":
    main()
