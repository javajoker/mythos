"""Description cue lexicon for Method G (projects/shanhaijing/docs/method-g-global.md).

Maps the book's descriptive phrases to the tag vocabulary shared with
projects/shanhaijing/data/world/animals.jsonl and loci.jsonl. Names are never used: callers strip the
「(其)名曰X」 clause before tagging.
"""
import re

# body analogy: the character after 如 / before 身
BODY_CHARS = {
    "牛": "body_cattle", "馬": "body_horse", "羊": "body_sheep", "豕": "body_pig", "彘": "body_pig", "豚": "body_pig",
    "犬": "body_dog", "狗": "body_dog", "狐": "body_fox", "狸": "body_wildcat", "貍": "body_wildcat",
    "禺": "body_ape", "猿": "body_ape", "猨": "body_ape", "蜼": "body_ape", "鹿": "body_deer", "麋": "body_deer",
    "麐": "body_deer", "麈": "body_deer", "鼠": "body_rat", "虎": "body_bigcat", "豹": "body_bigcat",
    "熊": "body_bear", "羆": "body_bear", "蛇": "body_snake", "魚": "body_fish", "鯉": "body_fish", "鮒": "body_fish",
    "鯈": "body_fish", "鱣": "body_fish", "鮎": "body_fish", "鯑": "body_fish", "鮪": "body_fish",
    "雞": "body_fowl", "鷄": "body_fowl", "雉": "body_fowl", "翟": "body_fowl", "鳧": "body_duck", "鴛": "body_duck",
    "梟": "body_owl", "鴞": "body_owl", "鵂": "body_owl", "烏": "body_crow", "鵲": "body_crow", "鶴": "body_crane",
    "龜": "body_turtle", "鼈": "body_turtle", "人": "body_human", "蠭": "body_bee", "蜂": "body_bee",
    "鳥": "body_bird", "兔": "body_hare", "蝟": "body_rat",
    "鶉": "body_fowl", "鶡": "body_fowl", "鴟": "body_owl", "鵰": "body_bird", "雕": "body_bird", "鳩": "body_bird",
    "鶻": "body_bird", "鸛": "body_crane", "貆": "body_fox", "駮": "body_horse", "驢": "body_horse", "羭": "body_sheep",
    "麢": "body_deer", "麝": "body_deer", "獼": "body_ape", "黿": "body_turtle", "鮫": "body_fish", "鯽": "body_fish",
}
RE_SHAPE = re.compile(r"狀如([^，。；而]{1,5})")          # body analogy: only the 「狀如…」 clause (not 文如/音如/大如)
RE_BODY_SHEN = re.compile(r"([" + "".join(BODY_CHARS) + r"])身")

CREATURE_CUES = [
    (r"[翼羽]", "wings"), (r"一角", "horn_one"), (r"四角", "horns_four"), (r"兩角|二角", "horns_two"),
    (r"[兩二三六九]首", "heads_many"), (r"[三四五六九]尾", "tails_many"), (r"一目", "eye_one"),
    (r"四足", "legs_four"), (r"六足", "legs_six"), (r"一足", "leg_one"), (r"人面|人首", "human_face"),
    (r"長尾|尾長", "long_tail"), (r"長臂|文臂", "long_arms"), (r"[髦鬣]", "mane"), (r"牙|虎齒", "tusks"),
    (r"鱗", "scales"), (r"披蓑|毛如|豪如", "long_shaggy_hair"), (r"如笄|白毛.*黑端|豪彘", "quills"),
    (r"(?:蛇|魚)[^，。]{0,4}四足|四足[^，。]{0,4}(?:蛇|魚)", "elongated_four_legged"),
    (r"虎文|其文如虎|文如虎|有文", "striped"), (r"豹文|文如豹", "spotted"), (r"五采|五色", "five_colours"),
    (r"白身|身白|皆白", "body_white"), (r"黑身|身黑|蒼黑", "body_black"), (r"赤身|身赤|赤如丹", "body_red"),
    (r"蒼文|青文|蒼身|青身", "blue_green"), (r"白首", "head_white"), (r"赤喙", "beak_red"), (r"赤尾", "tail_red"),
    (r"嬰兒", "sound_baby"), (r"吠犬|如吠|狗吠|犬吠", "sound_dog"), (r"音如牛|如牛鳴", "sound_cattle"),
    (r"自叫|自呼|自號|自詨|自訆|自名", "self_named_call"), (r"音如人|如呼|如叱|如詈|如謠|笑", "sound_human"),
    (r"如鼓|如雷|擊石", "sound_drum"), (r"鳴|嘯|音", "vocal"),
    (r"夜飛|以夜", "flies_night"), (r"夜", "nocturnal"), (r"冬死|冬蟄|夏生|蟄", "dormancy"), (r"陵居", "on_land"),
    (r"善投", "throws"), (r"人立|人走|伏行", "bipedal_gait"), (r"食人", "man_eater"), (r"穴", "burrow"),
    (r"[遊游行][^，。]{0,3}海", "sea_migration"), (r"善登|善緣", "climber"), (r"善走|走[^，。]{0,2}如飛", "fast_runner"),
    (r"海", "marine"), (r"水|澤|淵", "aquatic"),
]
CREATURE_CUES = [(re.compile(p), t) for p, t in CREATURE_CUES]

# Place cues: (regex, tag) — searched in all entries naming the target place.
PLACE_CUES = [
    (r"萬仞|高萬|大山|方八百里", "great_peak"),
    (r"其光熊熊|光熊熊", "glow"),
    (r"流沙", "desert_edge"),
    (r"炎火|投物輒然", "fire_ground"),
    (r"淵環之|環之|弱水之淵", "encircling_water"),
    (r"人面[^。]{0,3}虎身|虎身[^。]{0,6}人面|類虎[^。]{0,6}人面", "human_feline_colossus"),
    (r"東嚮立|東向立", "east_facing_colossus"),
    (r"九井|九門|以玉為檻|開明獸守之", "built_complex"),
    (r"穴處", "cave_dwelling"),
    (r"帝之下都|百神|萬物盡有", "sacred_mountain"),
    (r"玉|琅玕|珠樹", "gems_jade"),
]
PLACE_CUES = [(re.compile(p), t) for p, t in PLACE_CUES]
RE_SEA_SIDE = re.compile(r"(?:[東西南北]+)?海之(南|北|東|西)")   # 「X海之南」: the place lies S of a sea -> sea_north
OPPOSITE = {"南": "sea_north", "北": "sea_south", "東": "sea_west", "西": "sea_east"}
RE_RIVER_OUT = re.compile(r"([^，。；]{1,6}?水)出(?:焉|(東南|西南|東北|西北)隅)[^。]*?(東南|西南|東北|西北|東|西|南|北)?")
RE_NAME = re.compile(r"(?:其名曰|名曰|號曰|是為)[^，。；]{1,6}")


def mask_names(text: str) -> str:
    return RE_NAME.sub("", text)


def body_tags(text: str) -> set[str]:
    out = set()
    for m in RE_SHAPE.finditer(text):
        out |= {BODY_CHARS[ch] for ch in m.group(1) if ch in BODY_CHARS}
    for m in RE_BODY_SHEN.finditer(text):
        out.add(BODY_CHARS[m.group(1)])
    return out


def creature_tags(text: str) -> set[str]:
    t = mask_names(text)
    tags = body_tags(t)
    for rx, tag in CREATURE_CUES:
        if rx.search(t):
            tags.add(tag)
    if "body_bird" in tags or "body_fowl" in tags or "body_duck" in tags or "body_owl" in tags:
        tags.discard("body_bird") if tags & {"body_fowl", "body_duck", "body_owl", "body_crow", "body_crane"} else None
    return tags


def place_tags(text: str) -> set[str]:
    t = mask_names(text)
    out = {tag for rx, tag in PLACE_CUES if rx.search(t)}
    for m in RE_SEA_SIDE.finditer(t):
        out.add(OPPOSITE[m.group(1)])
    return out


# Region-property cues for whole sections (Method G whole-book mapping; data/world/region-properties.jsonl).
# Each maps a textual cue to a region property. Notes: 「玉」 -> jade is an interpretive step (玉 covers precious
# stones generally); 「丹粟」 are cinnabar grains, so 粟 counts as millet only when not preceded by 丹.
REGION_CUES = [
    (r"黃金", "gold"), (r"白金|銀", "silver"), (r"赤金|銅", "copper"), (r"鐵", "iron"), (r"錫", "tin"),
    (r"玉", "jade"), (r"丹粟|丹沙|丹砂|丹雘", "cinnabar"), (r"雄黃", "realgar"),
    (r"青雘|青碧|空青|曾青|碧", "azurite_malachite"), (r"鹽", "salt"),
    (r"竹|箭|篃|䈰|簜|桃枝", "bamboo"), (r"橘|櫾|柚", "citrus"), (r"桑", "mulberry"), (r"漆", "lacquer"),
    (r"松", "pine"), (r"柏", "cypress"), (r"椶", "palm"), (r"棗", "jujube"), (r"(?<!桃枝)桃|李", "peach_plum"),
    (r"稷|黍|(?<!丹)粟", "millet"), (r"稻|秔|稌", "rice"),
    (r"冬夏有雪|有雪", "snow_peaks"), (r"流沙|多沙", "sand_desert"), (r"炎火|投物輒然|火山", "volcanic_fire"),
    (r"湯水|溫水|湯谷|多湯", "hot_springs"), (r"鹽澤|鹽池|鹽水", "salt_lakes"), (r"海", "sea_coast"),
    (r"雕題|文身|黥", "tattoo"), (r"黑齒", "black_teeth"), (r"離耳|儋耳|聶耳|聶其耳|大耳", "ear_ornaments"),
    (r"羽民|生羽|身生羽", "feather_dress"), (r"毛民|身生毛|生毛", "hairy_people"),
    (r"小人|焦僥|周饒|長三尺|靖人|菌人", "pygmy_people"), (r"其為人黑|黑人|為人黑", "dark_skin"),
    (r"穴處|穴居", "cave_dwelling"),
]
REGION_CUES = [(re.compile(p), t) for p, t in REGION_CUES]
RE_BARREN = re.compile(r"無草木")


def region_cue_hits(text: str) -> dict[str, int]:
    """Count region-property cues in a text (names masked)."""
    t = mask_names(text)
    out = {}
    for rx, tag in REGION_CUES:
        n = len(rx.findall(t))
        if n:
            out[tag] = out.get(tag, 0) + n
    return out
