"""Shared loaders and scoring for the entity-graph method (candidates and cross-validation)."""
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KG = ROOT / "projects/shanhaijing/data/derived/kg"
WORLD = ROOT / "projects/shanhaijing/data/world"
DIR_DEG = {"北": 0, "東北": 45, "東": 90, "東南": 135, "南": 180, "西南": 225, "西": 270, "西北": 315}

# common nouns for plants and minerals: lexical meaning (translation), not name matching
LEXICAL = {
    "金": "metal (generic)", "黃金": "gold", "白金": "silver", "銀": "silver", "赤金": "copper", "銅": "copper",
    "鐵": "iron", "錫": "tin", "玉": "jade / precious stone", "白玉": "white jade", "美玉": "fine jade",
    "蒼玉": "grey-green jade", "水玉": "rock crystal", "碧": "green stone", "青碧": "green stone (azurite/malachite)",
    "青雘": "blue-green pigment (azurite/malachite)", "丹粟": "cinnabar grains", "丹雘": "red pigment (cinnabar)",
    "雄黃": "realgar", "青雄黃": "realgar (greenish)", "鹽": "salt", "磁石": "magnetite", "砥礪": "whetstone",
    "砥": "whetstone", "礪": "whetstone", "磬石": "chime stone", "文石": "patterned stone", "白堊": "white clay (chalk)",
    "黃堊": "yellow clay (ochre)", "堊": "clay", "赭": "red ochre", "美赭": "red ochre", "沙石": "sandstone, gravel",
    "石": "stone", "琅玕": "precious stone (coral-like)", "瑤": "fine jade", "瑤碧": "fine green jade", "瑾瑜": "fine jade",
    "竹": "bamboo", "箭": "arrow bamboo", "竹箭": "arrow bamboo", "篃": "bamboo (broad-leaf)", "桃枝": "bamboo (Taozhi)",
    "橘": "citrus (mandarin)", "櫾": "citrus (pomelo)", "柚": "pomelo", "桑": "mulberry", "漆": "lacquer tree",
    "松": "pine", "柏": "cypress / arborvitae", "椶": "windmill palm", "棗": "jujube", "桃": "peach", "李": "plum",
    "稷": "millet", "黍": "broomcorn millet", "稻": "rice", "桂": "cassia / osmanthus", "梓": "catalpa",
    "枏": "nanmu (Phoebe)", "楠": "nanmu (Phoebe)", "櫟": "oak", "柞": "oak", "榖": "paper mulberry", "楮": "paper mulberry",
    "梨": "pear", "栗": "chestnut", "荊": "chaste tree (Vitex)", "杞": "wolfberry / willow", "菊": "chrysanthemum",
    "韭": "chive", "葵": "mallow", "蔥": "scallion", "薤": "Chinese onion", "椒": "Sichuan pepper", "柘": "Maclura",
    "樗": "tree of heaven (Ailanthus)", "杏": "apricot", "楊": "poplar", "柳": "willow", "槐": "pagoda tree",
    "芍藥": "peony", "芎藭": "Ligusticum", "藷藇": "yam", "蒿": "Artemisia", "茅": "cogon grass", "棠": "crabapple",
}


def jl(path):
    return [json.loads(l) for l in Path(path).open() if l.strip()]


def load_world():
    regions = jl(WORLD / "regions.jsonl")
    props = {p["prop"]: p for p in jl(WORLD / "region-properties.jsonl")}
    animals = jl(WORLD / "animals.jsonl")
    waters = jl(WORLD / "waters.jsonl")
    cultures = jl(WORLD / "cultures.jsonl")
    return regions, props, animals, waters, cultures


def prop_weight(p):
    known = len(p["true"]) + len(p["false"])
    if not p["true"]:
        return 0.05, 0.0
    return math.log10(known / len(p["true"])) + 0.05, len(p["true"]) / known


def region_prop_score(code, p):
    """+w if the region has the property, −w if it clearly lacks it, base-rate expectation if unknown."""
    w, frac = prop_weight(p)
    if code in p["true"]:
        return w
    if code in p["false"]:
        return -w
    return w * (2 * frac - 1)


def animal_weights(animals):
    df = Counter(t for a in animals for t in set(a["tags"]))
    n = len(animals)
    w = {t: math.log10(n / c) + 0.05 for t, c in df.items()}
    for g in ("vocal", "aquatic"):
        if g in w:
            w[g] = min(w[g], 0.05)
    return w


def animal_match(tags, kind, animals, w):
    """Rarity-weighted coverage of a description by each animal (with kind and body checks)."""
    C = set(tags)
    denom = sum(w.get(t, math.log10(len(animals)) + 0.05) for t in C) or 1
    bodies = {t for t in C if t.startswith("body_")}
    out = []
    for a in animals:
        A = set(a["tags"])
        ov = C & A
        cov = sum(w.get(t, 0) for t in ov) / denom
        if kind in ("鳥", "bird") and not (A & {"wings", "body_bird", "body_fowl", "body_duck", "body_owl", "body_crow",
                                                 "body_crane"}):
            cov *= 0.5
        if kind in ("魚", "fish") and not (A & {"aquatic", "marine", "body_fish"}):
            cov *= 0.5
        if bodies and not (bodies & A):
            cov *= 0.6
        if len(ov) < 2:
            cov *= 0.5
        out.append((round(cov, 3), sorted(ov), a))
    out.sort(key=lambda r: (-r[0], r[2]["id"]))
    return out


def bearing(a, b):
    """Initial compass bearing from point a to point b (degrees)."""
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def angdiff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)
