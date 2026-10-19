"""Step 1–2 of the entity-graph method: extract, merge and relate every entity in the Shanhaijing.

Builds the knowledge graph from all 869 paragraphs:
  nodes   MTN mountain · WAT water · LND land feature/place · POL polity/people · CRE creature · PLA plant ·
          MIN mineral · PER person/deity · UNK named item of undetermined type · DOC structural text (summaries,
          colophons) — so that every paragraph is represented and nothing is dropped
  edges   next · rises_at · flows_into · sinks_at · has_resource · has_creature · sees · located · dwells · begets ·
          same_name · in_entry-level co-mention is kept in mentions.jsonl
Names are symbols: spelling variants are folded (昆侖/崑崙/崐崘, 黑/黒, 雒→洛 for waters) but never scored.

Outputs (projects/shanhaijing/data/derived/kg/): nodes.jsonl, edges.jsonl, mentions.jsonl, shanhaijing.graphml,
coverage.md (paragraphs without entities, name patterns not captured — both must be zero or explained).
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).parent))
from cues import creature_tags, culture_cue_hits, mask_names, region_cue_hits  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
STATIONS = ROOT / "projects/shanhaijing/data/derived/stations.jsonl"
OUT = ROOT / "projects/shanhaijing/data/derived/kg"

DIRS = "東南|東北|西南|西北|東|西|南|北"
FOLD = str.maketrans({"崑": "昆", "崐": "昆", "崙": "侖", "崘": "侖", "黒": "黑"})

MINERALS = {  # symbol -> region-property key (None = generic stone/metal, kept but no regional signal)
    "黃金": "gold", "赤金": "copper", "白金": "silver", "銀": "silver", "銅": "copper", "鐵": "iron", "錫": "tin",
    "金": None, "白玉": "jade", "美玉": "jade", "蒼玉": "jade", "水玉": "jade", "嬰垣之玉": "jade", "瑾瑜之玉": "jade",
    "瑾瑜": "jade", "瑤碧": "jade", "瑤": "jade", "玉": "jade", "琅玕": "jade", "碧": "azurite_malachite",
    "青碧": "azurite_malachite", "青雘": "azurite_malachite", "空青": "azurite_malachite", "丹粟": "cinnabar",
    "丹雘": "cinnabar", "丹沙": "cinnabar", "青雄黃": "realgar", "雄黃": "realgar", "鹽": "salt", "磁石": "magnetite",
    "磬石": None, "砥礪": None, "砥": None, "礪": None, "文石": None, "采石": None, "茈石": None, "白堊": None,
    "黃堊": None, "堊": None, "赭": None, "美赭": None, "沙石": None, "石涅": None, "涅石": None, "封石": None,
    "洗石": None, "石": None, "瑊石": None, "文貝": None, "珠": None, "鐵石": None, "磐石": None,
}
PLANTS = {
    "竹箭": "bamboo", "桃枝": "bamboo", "鉤端": "bamboo", "竹": "bamboo", "箭": "bamboo", "篃": "bamboo", "䈰": "bamboo",
    "橘": "citrus", "櫾": "citrus", "柚": "citrus", "桑": "mulberry", "漆": "lacquer", "松": "pine", "柏": "cypress",
    "椶": "palm", "棗": "jujube", "桃": "peach_plum", "李": "peach_plum", "梅": "peach_plum", "稷": "millet",
    "黍": "millet", "稻": "rice", "桂": None, "梓": None, "枏": None, "楠": None, "杻": None, "橿": None, "櫟": None,
    "柞": None, "榖": None, "楮": None, "柤": None, "梨": None, "栗": None, "荊": None, "杞": None, "蕙": None,
    "茝": None, "菅": None, "芍藥": None, "芎藭": None, "蘪蕪": None, "藷藇": None, "薯藇": None, "菊": None,
    "韭": None, "葵": None, "蔥": None, "薤": None, "檀": None, "楢": None, "椒": None, "柘": None, "樗": None,
    "杏": None, "櫨": None, "楊": None, "柳": None, "槐": None, "椐": None, "楛": None, "樸": None, "芑": None,
    "枳": None, "棕": None, "棪": None, "蘭": None, "蒿": None, "茈草": None, "草": None, "木": None, "櫄": None,
    "扶桑": None, "若木": None, "建木": None, "枸": None, "棠": None, "柟": None, "梧": None, "楓": None, "茅": None,
}
ANIMALS = [
    "犛牛", "羬羊", "白猿", "豪彘", "橐駞", "橐駝", "蝮虫", "蝮蟲", "鸞鳥", "鳳皇", "白鹿", "閭麋", "麢麝", "犀兕",
    "犀", "兕", "象", "虎", "豹", "熊", "羆", "麋", "鹿", "麝", "麢", "麈", "猿", "猨", "蜼", "禺", "牛", "馬", "羊",
    "豕", "彘", "狼", "犬", "狐", "兔", "鳥", "鴞", "翟", "雉", "鵲", "龜", "鼈", "蛇", "魚", "鼉", "蛟", "蟲", "虫",
    "鶹", "䍺", "閭", "麖", "夔", "蛙", "蚌", "蠃", "貝", "鷩", "鶡", "鴆", "鶉", "鴟", "鵰", "鷹", "鸇", "猴",
]
LEX = sorted(list(MINERALS) + list(PLANTS) + ANIMALS, key=len, reverse=True)
PERSONS_KNOWN = [
    "西王母", "帝俊", "帝堯", "帝嚳", "帝舜", "帝丹朱", "帝顓頊", "帝江", "帝臺", "黃帝", "炎帝", "顓頊", "后稷", "后土",
    "夸父", "共工", "祝融", "蚩尤", "羲和", "常羲", "燭陰", "燭龍", "刑天", "女媧", "蓐收", "句芒", "應龍", "女魃",
    "相柳", "相繇", "貳負", "窫窳", "開明獸", "陸吾", "英招", "長乘", "江疑", "耆童", "少昊", "白帝少昊", "老童", "叔均",
    "台璽", "噎", "禹", "鯀", "羿", "舜", "堯", "啟", "夏后啟", "夏后開", "王亥", "河伯", "冰夷", "帝", "天帝",
]
PERSONS_KNOWN.sort(key=len, reverse=True)

STRIP_PREFIX = re.compile(r"^(?:[又凡其是此有曰名乃至於于在之及與出入注過望臨東西南北多上下陽陰中至則見而以為自]|名曰|至于|至於)+")
STOP_MTN = {"山", "其山", "是山", "此山", "名山", "大山", "諸山", "群山", "羣山", "一山", "二山", "三山", "高山之",
            "中山", "南山經", "北山經", "西山經", "東山經", "五臧山", "下山", "上山", "之山"}
STOP_WAT = {"水", "其水", "是水", "此水", "多水", "無水", "大水", "洪水", "之水", "水玉", "海", "海水", "其海", "流水"}
STOP_POL = {"國", "其國", "是國", "此國", "天下", "郡國", "之國", "大國", "見則其國", "民", "人民", "其民", "萬民",
            "之民", "國民"}
WATER_SUFFIX = re.compile(r"(之水|水|海|澤|淵|泉|池|湖|浦)$")
BAD_NAME = re.compile(r"[可以禦食已使為多無其是此見則善不令所皆而與及或若乃曰]")   # verbs/pronouns: not part of a name


def fold(s: str) -> str:
    return s.translate(FOLD)


PUNCT = re.compile(r"[《》「」『』：:（）()─—]")


def clean(name: str) -> str:
    name = PUNCT.sub("", name.strip())
    name = re.split(r"[出在注入望]", name)[-1] if re.search(r".[出在注入望].", name) else name
    name = STRIP_PREFIX.sub("", name)
    return fold(name)


def water_core(name: str) -> str:
    n = fold(name).replace("雒", "洛").replace("榖", "穀").strip()
    if n.endswith(("海", "澤", "淵", "泉", "池", "湖", "浦")) or n in ("河", "江"):
        return n
    n = re.sub(r"之水$", "", n)
    n = re.sub(r"水$", "", n)
    return {"大江": "江", "河水": "河", "江水": "江"}.get(n, n)


def segment(token: str):
    """Greedy longest-match split of a 「多X」 list token into lexicon items; leftovers become UNK."""
    out, i = [], 0
    while i < len(token):
        for w in LEX:
            if token.startswith(w, i):
                out.append(w); i += len(w); break
        else:
            j = i + 1
            while j < len(token) and not any(token.startswith(w, j) for w in LEX):
                j += 1
            out.append(token[i:j]); i = j
    return out


SPLIT_NAME = re.compile(r"(?:一曰|一日|或曰|一云|故曰|曰|生|為|謂|攻|處|戰于|戰於|之於|居)")
NUM = re.compile(r"^[一二三四五六七八九十百千萬兩]+$")
PER_BAD = re.compile(r"[焉皆可不歳歲]|^有|有$")


def name_for(raw: str, kind: str) -> str:
    """Clean a raw capture into a symbol. POL / LND are split at speech, birth and motion verbs; UNK / PER keep the
    whole cleaned name (names such as 鞠陵于天 contain 于)."""
    n = clean(raw)
    if kind in ("POL", "LND"):
        parts = [x for x in SPLIT_NAME.split(n) if x]
        n = STRIP_PREFIX.sub("", parts[-1] if parts else n)
        n = re.sub(r"^[或故所]", "", n)
        n = re.sub(r"(之|也)$", "", n)
    if kind in ("PER", "UNK"):
        n = re.split(r"(?:處|居|司|在|以|東方|南方|西方|北方|曰)", n)[0] or n
    if kind == "POL":
        n = re.sub(r"之?國$", "", n)
    return n


class KG:
    def __init__(self):
        self.nodes, self.edges = {}, []
        self.mentions = defaultdict(list)
        self.by_symbol = defaultdict(list)

    def lookup(self, sym, types=None):
        """Existing node for a symbol or its suffixed forms (X之山, X山, X國, X之國, X水)."""
        forms = [sym, sym + "之山", sym + "山", sym + "國", sym + "之國", sym + "之丘", sym + "水"]
        if re.search(r"[鳥獸]$", sym) and len(sym) > 2:
            forms.append(sym[:-1])
        for form in forms:
            for nid in self.by_symbol.get(form, []):
                if types is None or self.nodes[nid]["type"] in types:
                    return nid
        for nid in self.by_symbol.get(re.sub(r"(之山|山|之國|國|之丘)$", "", sym), []):
            if types is None or self.nodes[nid]["type"] in types:
                return nid
        return None

    def ref(self, raw, entry, kind="LND", types=("POL", "MTN", "WAT", "LND", "PER", "CRE", "UNK")):
        """Resolve a reference to an existing entity (any type), else create one of `kind`."""
        sym = name_for(raw, kind)
        if not sym or NUM.match(sym) or (kind == "LND" and len(sym) < 2):
            return None
        nid = self.lookup(sym, types)
        if nid:
            return self.node(self.nodes[nid]["type"], self.nodes[nid]["symbol"], entry, nid=nid)
        return self.node(kind, sym, entry)

    def node(self, ntype, symbol, entry, desc=None, nid=None, **props):
        if not symbol or not str(symbol).strip():
            return None
        nid = nid or f"{ntype}:{symbol}"
        n = self.nodes.setdefault(nid, {"id": nid, "type": ntype, "symbol": symbol, "variants": [], "mentions": [],
                                       "descriptions": [], "props": {}, "tags": []})
        if nid not in self.by_symbol[symbol]:
            self.by_symbol[symbol].append(nid)
        if entry not in n["mentions"]:
            n["mentions"].append(entry)
        if desc and {"entry": entry, "text": desc} not in n["descriptions"]:
            n["descriptions"].append({"entry": entry, "text": desc})
        for k, v in props.items():
            if v is not None:
                n["props"][k] = v
        if nid not in self.mentions[entry]:
            self.mentions[entry].append(nid)
        return nid

    def edge(self, src, dst, etype, entry, clause="", **attrs):
        if not src or not dst or src == dst:
            return
        self.edges.append({"src": src, "dst": dst, "type": etype, "attrs": attrs, "entry": entry, "clause": clause})


def main():
    entries = [json.loads(l) for l in ENTRIES.open()]
    by_id = {e["id"]: e for e in entries}
    stations = [json.loads(l) for l in STATIONS.open()]
    kg = KG()

    # ---- mountain identities: same name in different Mountain sections = different entities ---------------------
    sec_of_name = defaultdict(set)
    for s in stations:
        sec_of_name[fold(s["name"])].add(s["section"])
    mtn_id = {}
    for s in stations:
        nm = fold(s["name"])
        mtn_id[(s["section"], nm)] = f"MTN:{nm}" + (f"#{s['section']}" if len(sec_of_name[nm]) > 1 else "")

    def resolve_mtn(name, entry, section=None):
        if re.search(r"(?:狀|實)如", name):                 # 「其狀如山雞」「其實如菟丘」: a simile, not a mountain
            return None
        nm = re.sub(r"^.*經(?:之首曰)?", "", clean(name))     # 「西山經華山之首」「南山經之首曰䧿山」: the range name
        if not nm or nm in STOP_MTN or len(nm) < 2:
            return None
        if section and (section, nm) in mtn_id:
            return kg.node("MTN", nm, entry, nid=mtn_id[(section, nm)])
        if section and (section, nm[1:]) in mtn_id:          # one-character slip such as 白甘棗 for 自甘棗
            return kg.node("MTN", nm[1:], entry, nid=mtn_id[(section, nm[1:])])
        secs = sec_of_name.get(nm)
        if secs and len(secs) == 1:
            return kg.node("MTN", nm, entry, nid=mtn_id[(next(iter(secs)), nm)])
        nid = kg.node("MTN", nm, entry, nid=f"MTN:{nm}" + ("@mention" if secs else ""))
        return nid

    # ---- 1. Mountain stations, itinerary, rivers ------------------------------------------------------------------
    prev = {}
    water_flow = []          # (symbol_core, dest_core, dir, entry, clause, source_node)
    sinks = []               # (water core, lake core, entry, clause)
    for s in stations:
        e = by_id[s["entry_id"]]
        nid = kg.node("MTN", fold(s["name"]), e["id"], nid=mtn_id[(s["section"], fold(s["name"]))],
                      section=s["section"], seq=s["seq"])
        kg.nodes[nid]["props"]["section"] = s["section"]
        key = s["section"]
        if key in prev and s.get("bearing"):
            kg.edge(prev[key], nid, "next", e["id"], s.get("leg_raw", ""), bearing=s["bearing"], li=s.get("leg_li"))
        prev[key] = nid
        for r in s["rivers"]:
            water_flow.append((water_core(r["river"]), water_core(r["to"]), r["flow"], e["id"],
                               f"{r['river']}出{r['where']}，{r['flow'] or ''}流注于{r['to']}", nid))

    # ---- 2. Every paragraph: generic extraction --------------------------------------------------------------------
    known_waters = {w for w, _, _, _, _, _ in water_flow} | {d for _, d, _, _, _, _ in water_flow}
    for e in entries:
        for m in re.finditer(r"([^\s，。；、]{1,5}?水)出|注(?:于|於)([^，。；]{1,6})", PUNCT.sub("", e["text"])):
            known_waters.add(water_core(clean(m.group(1) or m.group(2))))
    station_of_entry = {s["entry_id"]: mtn_id[(s["section"], fold(s["name"]))] for s in stations}
    last_subject = {}
    RE_MTN = re.compile(r"([^\s，。；、：「」（）]{1,6}?(?:之山|之丘(?!山)|山(?!雞)|丘(?!山)))")
    RE_WAT = re.compile(r"([^\s，。；、：「」（）]{1,5}?(?:之水|水|澤|淵|泉|池))")   # seas come from the sea pattern
    RE_POL = re.compile(r"([^\s，。；、：「」（）]{1,6}?(?:之國|國))")
    RE_MIN_PEOPLE = re.compile(r"([^\s，。；、：「」（）]{1,4}?民)(?:之國|國)?")
    RE_LND = re.compile(r"(流沙|大荒|[^\s，。；、]{1,4}?之野|[^\s，。；、]{1,4}?虛|湯谷|暘谷|虞淵)")
    RE_DUO = re.compile(r"(?:其上|其下|其陽|其陰|其中|其木|其草|其獸|其鳥|其魚|其蟲|其)?(?:多|有)([^，。；]{1,12})")
    RE_CRE_START = re.compile(r"有(獸|鳥|魚|蛇|蟲|木|草)焉")
    RE_NAMED = re.compile(r"(?:其名曰|名曰|名|號曰)([^，。；、]{1,6})")
    RE_SEES = re.compile(rf"({DIRS})望([^，。；]{{1,10}})")
    RE_LOC = re.compile(rf"^([^，。；]{{1,8}}?)在([^，。；]{{1,10}}?)({DIRS})")
    RE_BEGET = re.compile(r"([^\s，。；、]{1,4})生([^\s，。；、]{1,4})")
    RE_DWELL = re.compile(r"(?:神|帝)?([^\s，。；、]{1,4})(居之|司之|處之|處于此|居此)")
    RE_RIVER_OUT = re.compile(rf"([^\s，。；、]{{1,5}}?水)出(?:於|于)?([^，。；]{{0,10}}?)[，。]?(?:而)?(?:({DIRS})流?)?(?:注|入)(?:于|於)?([^，。；]{{1,8}})")

    for e in entries:
        t = PUNCT.sub("", e["text"])
        eid = e["id"]
        mt = mask_names(t)
        host = station_of_entry.get(eid)
        subject = host
        # summaries / colophons / rituals in the Mountain books
        if e["book_no"] <= 5 and (t.startswith(("凡", "右", "禹曰", "大凡")) or e["section"] == "五臧山經"):
            d = kg.node("DOC", f"{e['section']}・總述", eid, desc=t[:80])
            gods = re.search(r"其神(?:狀)?皆([^。]+)", t)
            if gods:
                p = kg.node("PER", f"{e['section']}之神", eid, desc=gods.group(0))
                kg.edge(p, d, "described_in", eid, gods.group(0))
            tt = PUNCT.sub("", t)
            for m in re.finditer(r"([^\s，。；、]{1,6}?(?:之山|山))", tt):
                raw = m.group(1)
                if re.search(r"[一二三四五六七八九十百千]山$|經之山|名山|出[銅鐵]之山|此[一二三]山", raw):
                    continue
                mid = resolve_mtn(raw, eid, e["section"])
                if mid:
                    kg.edge(d, mid, "summarizes", eid, raw)
            continue
        # waters described with 出/注 in the Sea books (e.g. the 海內東經 waterway list)
        if e["book_no"] >= 6:
            for sent in re.split(r"。", t):
                mc = re.search(r"([^\s，。；、]{1,5}?(?:水|江))出(?:於|于)?([^，。；]{0,12})", sent)
                if not mc:
                    continue
                src_place = mc.group(2).strip()
                if re.search(r"隅$", src_place):
                    mid = subject if subject else None          # 「出東北隅」: a corner of the paragraph's subject
                else:
                    src_place = re.split(r"而|，", src_place)[0]
                    if re.search(r"(山|丘)$", src_place):
                        mid = resolve_mtn(src_place, eid)
                    else:
                        mid = kg.ref(re.sub(r"(東|西|南|北)+$", "", src_place), eid, "LND") if src_place else None
                rest = sent[mc.end():]
                tgt = None
                for mt2 in re.finditer(rf"(?:({DIRS}))?(?:又)?(?:注|入)(?:于|於)?([^，。；]{{1,6}})", rest):
                    cand = clean(mt2.group(2))
                    core = water_core(cand)
                    if re.search(r"(海|水|澤|淵|河|江|湖)$", cand) or core in ("河", "江"):
                        tgt = (core, mt2.group(1))
                        break
                water_flow.append((water_core(mc.group(1)), tgt[0] if tgt else "", tgt[1] if tgt else None, eid,
                                   sent[:40], mid))
        # 「東望泑澤，河水所潛也」: the river sinks at the lake
        for ms in re.finditer(r"([^\s，。；、]{1,5}?(?:澤|淵))，?(河水|[^\s，。；、]{1,3}水)所潛", t):
            sinks.append((water_core(clean(ms.group(2))), water_core(clean(ms.group(1))), eid, ms.group(0)))
        # mountains mentioned
        for m in RE_MTN.finditer(t):
            nid = resolve_mtn(m.group(1), eid, e["section"] if e["book_no"] <= 5 else None)
            if nid and nid != host:
                if e["book_no"] >= 6 and subject is None:
                    subject = nid
        # waters mentioned
        for m in RE_WAT.finditer(t):
            full = m.group(1)
            core = re.split(r"[于於處]", water_core(clean(full)))[-1]
            if t[m.end():m.end() + 0] == "" and re.search(r"大水$", full):
                continue                                   # 「天下大水」「其邑大水」: flood idiom, not a water body
            raw_core = water_core(clean(full))
            if raw_core in known_waters:
                kg.node("WAT", raw_core, eid)
                continue
            if (core and core not in STOP_WAT and not BAD_NAME.search(core) and not NUM.match(core)
                    and (core in known_waters or re.search(r"(之水|澤|淵|泉|池)$", full))
                    and not re.match(r"[居捕攻將飲生後應禹走冬夏絕行閒有三九人天邑郡國]", core)):
                kg.node("WAT", core, eid)
        if "海" in t:
            for m in re.finditer(r"(東|西|南|北|渤|大)?海", t):
                sym = (m.group(1) or "") + "海"
                if sym not in ("大海",):
                    kg.node("WAT", sym, eid)
        # land features
        for m in RE_LND.finditer(t):
            sym = name_for(m.group(1), "LND")
            if sym and len(sym) >= 2 and not BAD_NAME.search(sym):
                kg.ref(sym, eid, "LND")
        for m in re.finditer(r"([^\s，。；]{1,4})、([^\s，。；]{1,4})", t):   # 「女祭、女戚」 style pairs
            pass
        # polities / peoples (Sea & Wilderness books, and 「X之國」 anywhere)
        if e["book_no"] >= 6:
            for m in RE_POL.finditer(t):
                sym = name_for(m.group(1), "POL")
                if sym and sym + "國" not in STOP_POL and sym not in STOP_POL and not re.search(r"[其則是見]", sym) \
                        and not NUM.match(sym) and sym not in ("始", "潛", "所經", "下民", "經", "州") \
                        and not sym.endswith("姓"):
                    pid = kg.node("POL", sym, eid)
                    subject = subject or pid
            for m in RE_MIN_PEOPLE.finditer(t):
                sym = name_for(m.group(1), "POL")
                if sym and sym not in STOP_POL and not re.search(r"[其則是見]", sym) and len(sym) >= 2 \
                        and sym not in ("下民", "作下民"):
                    pid = kg.lookup(sym, ("POL",)) or kg.node("POL", sym, eid)
                    kg.node("POL", kg.nodes[pid]["symbol"], eid, nid=pid)
                    subject = subject or pid
        # persons / deities
        for p in PERSONS_KNOWN:
            if p in t and not (p == "帝" and re.search(r"帝(之|乃|令|命|所)", t) and not re.search(r"帝[俊堯嚳舜江臺顓]", t)):
                if p == "帝" and re.search(r"帝[俊堯嚳舜江臺顓丹]", t):
                    continue
                kg.node("PER", p, eid)
        for m in re.finditer(r"(?:有神|神|有人|有女子|有獸)，?(?:名)?曰([^，。；、]{1,5})", t):
            sym = name_for(m.group(1), "PER")
            if sym and not PER_BAD.search(sym):
                kg.node("PER", sym, eid)
        for m in re.finditer(r"([^\s，。；、]{1,4}之尸)", t):
            kg.node("PER", clean(m.group(1)), eid)
        for m in RE_DWELL.finditer(t):
            who = clean(m.group(1))
            if who and len(who) >= 2 and not re.search(r"[其是此]", who) and host:
                pid = kg.node("PER", who, eid)
                kg.edge(pid, host, "dwells", eid, m.group(0))
        if e["book_no"] >= 14 or e["book_no"] == 18:
            for m in RE_BEGET.finditer(t):
                a, b = name_for(m.group(1), "PER"), name_for(m.group(2), "PER")
                if (a and b and len(a) >= 2 and not re.search(r"[而所之是其則死]", a + b)
                        and not PER_BAD.search(a + b) and not b.startswith(("焉", "之", "於", "于"))):
                    pa, pb = kg.node("PER", a, eid), kg.node("PER", b, eid)
                    kg.edge(pa, pb, "begets", eid, m.group(0))
        # creatures and named plants with descriptions
        starts = list(RE_CRE_START.finditer(t))
        for i, m in enumerate(starts):
            seg_end = starts[i + 1].start() if i + 1 < len(starts) else len(t)
            seg = t[m.start():seg_end]
            stop = re.search(r"[^，。]{1,6}之?水出焉", seg)
            seg = seg[:stop.start()] if stop else seg
            nm = RE_NAMED.search(seg)
            sym = clean(nm.group(1)) if nm else f"{eid}#{i + 1}"
            kind = m.group(1)
            ntype = "PLA" if kind in ("木", "草") else "CRE"
            nid = kg.node(ntype, sym, eid, desc=seg, kind=kind)
            if ntype == "CRE":
                kg.nodes[nid]["tags"] = sorted(set(kg.nodes[nid]["tags"]) | creature_tags(seg))
            if host:
                kg.edge(host, nid, "has_creature" if ntype == "CRE" else "has_resource", eid, seg[:20])
        for m in re.finditer(r"(?:其中|是)多([^，。；]{1,6})，(?:其)?狀如([^。]*)", t):
            sym = clean(m.group(1))
            nid = kg.node("CRE", sym, eid, desc=m.group(0))
            kg.nodes[nid]["tags"] = sorted(set(kg.nodes[nid]["tags"]) | creature_tags(m.group(0)))
            if host:
                kg.edge(host, nid, "has_creature", eid, m.group(0)[:20])
        if e["book_no"] >= 6 and "狀如" in t and not starts:
            first = re.split(r"[，在]", t)[0]
            sym = clean(first) or f"{eid}#1"
            if len(sym) <= 6:
                nid = kg.node("CRE", sym, eid, desc=t)
                kg.nodes[nid]["tags"] = sorted(set(kg.nodes[nid]["tags"]) | creature_tags(t))
        # resource lists 「多X、Y」 / 「其獸多X」
        for m in RE_DUO.finditer(t):
            body = m.group(1)
            if re.match(r"(怪|奇)", body) or "焉" in body[:2]:
                continue
            for tok in re.split(r"[、]", body):
                tok = re.sub(r"[而之其]$", "", tok.strip())
                for item in segment(tok)[:4]:
                    if item in MINERALS:
                        nid = kg.node("MIN", item, eid, prop=MINERALS[item])
                        if host:
                            kg.edge(host, nid, "has_resource", eid, m.group(0)[:16])
                    elif item in PLANTS:
                        nid = kg.node("PLA", item, eid, prop=PLANTS[item])
                        if host:
                            kg.edge(host, nid, "has_resource", eid, m.group(0)[:16])
                    elif item in ANIMALS:
                        nid = kg.node("CRE", item, eid)
                        if host:
                            kg.edge(host, nid, "has_creature", eid, m.group(0)[:16])
        # sight-lines
        if host:
            for m in RE_SEES.finditer(t):
                tgt = clean(m.group(2))
                if not tgt:
                    continue
                if WATER_SUFFIX.search(tgt):
                    tid = kg.node("WAT", water_core(tgt), eid)
                elif re.search(r"(山|丘)$", tgt):
                    tid = resolve_mtn(tgt, eid, e["section"])
                else:
                    tid = kg.node("LND", tgt, eid)
                if tid:
                    kg.edge(host, tid, "sees", eid, m.group(0), direction=m.group(1))
        # relative position 「X在Y方」 (Sea & Wilderness books)
        if e["book_no"] >= 6:
            m = RE_LOC.search(t)
            if m:
                a = clean(m.group(1))
                b = clean(m.group(2))
                src = (subject if subject and kg.nodes[subject]["symbol"] and kg.nodes[subject]["symbol"] in a
                       and kg.nodes[subject]["type"] in ("POL", "MTN", "LND", "PER", "CRE") else None) or \
                    kg.ref(a, eid, "POL" if re.search(r"(國|民)$", a) else "LND") or subject
                if b in ("其", ""):
                    dst = last_subject.get(e["book_no"])
                else:
                    dst = next((n for n in kg.mentions[eid] if kg.nodes[n]["symbol"] and kg.nodes[n]["symbol"] in b
                                and n != src), None) or kg.ref(b, eid, "LND")
                if dst and dst != src:
                    kg.edge(src, dst, "located", eid, m.group(0), direction=m.group(3))
                subject = src
            if subject:
                last_subject[e["book_no"]] = subject
        # properties of the paragraph's subject
        if subject and subject in kg.nodes and kg.nodes[subject]["symbol"]:
            n = kg.nodes[subject]
            if n["type"] == "MTN":
                for tag in region_cue_hits(t):
                    n["tags"] = sorted(set(n["tags"]) | {tag})
                if "無草木" in t:
                    n["props"]["barren"] = True
            elif n["type"] == "POL":
                hits = culture_cue_hits(t)
                n["tags"] = sorted(set(n["tags"]) | set(hits))
                n["descriptions"].append({"entry": eid, "text": mt[:60]})
        # 「一曰…」 alternate accounts: alternative location edge or alternative description on the subject
        for m in re.finditer(r"一曰([^。]*)", t):
            alt = m.group(1)
            if subject and subject in kg.nodes:
                kg.nodes[subject]["descriptions"].append({"entry": eid, "text": "一曰" + alt, "alternate": True})
                lm = re.match(rf"在([^，。；]{{1,10}}?)({DIRS})", alt)
                if lm:
                    tgt = next((n for n in kg.mentions[eid] if kg.nodes[n]["symbol"] and kg.nodes[n]["symbol"] in lm.group(1)
                                and n != subject), None) or kg.ref(lm.group(1), eid, "LND")
                    kg.edge(subject, tgt, "located", eid, "一曰" + lm.group(0), direction=lm.group(2), alternate=True)
        # plain 「曰X」 (no 名): classify by context
        for m in re.finditer(r"(?<![一文])曰([^，。；、]{1,5})", t):
            sym = clean(m.group(1))
            before = t[max(0, m.start() - 4):m.start()]
            if not sym or any(kg.nodes[n]["symbol"] == sym or sym in kg.nodes[n]["symbol"] for n in kg.mentions[eid]):
                continue
            if re.search(r"(谷|州|丘|野|淵|門|崖|陵|谿)$", sym) or re.search(r"(谷|東|西|南|北)，?$", before):
                kg.node("LND", sym, eid, desc=t[max(0, m.start() - 10):m.end() + 6])
            elif re.search(r"(子|人|神|臣|女|風|方|妻)$", before.rstrip("，")):
                kg.node("PER", sym, eid, desc=t[max(0, m.start() - 10):m.end() + 6])
            elif re.search(r"(獸|鳥|魚|蛇)", t[max(0, m.start() - 30):m.start()]):
                nid = kg.node("CRE", sym, eid, desc=t[max(0, m.start() - 30):m.end() + 10])
                kg.nodes[nid]["tags"] = sorted(set(kg.nodes[nid]["tags"]) | creature_tags(t[max(0, m.start() - 30):m.end()]))
            elif not re.search(r"[！？]", m.group(1)):
                kg.ref(sym, eid, "UNK")
        # rivers named 「X江」: 「首江出汶山」
        for m in re.finditer(r"([^\s，。；、]{1,3}江)出([^，。；]{1,6})", t):
            mid = resolve_mtn(m.group(2), eid) or kg.node("LND", clean(m.group(2)), eid)
            water_flow.append((water_core(m.group(1)), "", None, eid, m.group(0), mid))
        # every remaining 「名曰X」 not yet captured becomes an UNK node (nothing is dropped)
        for m in RE_NAMED.finditer(t):
            sym = clean(m.group(1))
            if sym and not any(kg.nodes[n]["symbol"] == sym or sym in kg.nodes[n]["symbol"] for n in kg.mentions[eid]):
                kg.ref(sym, eid, "UNK")
        if not kg.mentions.get(eid):
            kg.node("DOC", f"{eid}", eid, desc=t[:80])

    # ---- 3. waters: merge by name, split homonyms that flow into different targets --------------------------------
    # homonyms split only on distinct MAJOR destinations (≥ 3 inflows, never itself): 「江水注于大江」 is a tributary,
    # and a local stream such as 玄扈之水 does not make a second 洛
    indeg = Counter(d for _, d, _, _, _, _ in water_flow if d)
    dests = defaultdict(set)
    for core, dest, _, _, _, _ in water_flow:
        if core and dest and dest != core and indeg[dest] >= 3:
            dests[core].add(dest)
    sec_of_entry = {e["id"]: (e["book_no"], e["section"]) for e in entries}
    variant_home = defaultdict(lambda: defaultdict(Counter))   # core -> variant id -> Counter of (book, section)
    for core, dest, d, eid, clause, src_node in water_flow:
        if core and len(dests[core]) > 1 and dest in dests[core]:
            variant_home[core][f"WAT:{core}→{dest}"][sec_of_entry[eid]] += 1

    def water_ref(core, eid):
        """Node id for a water symbol used as a TARGET: for homonyms, the variant from the same section, else the
        same book, else the most-attested variant."""
        if core not in variant_home:
            return f"WAT:{core}"
        b, sec = sec_of_entry[eid]
        vs = variant_home[core]
        for test in (lambda h: h[(b, sec)] > 0, lambda h: any(k[0] == b for k in h)):
            hit = sorted(v for v, h in vs.items() if test(h))
            if hit:
                return hit[0]
        return max(sorted(vs), key=lambda v: sum(vs[v].values()))

    for core, dest, d, eid, clause, src_node in water_flow:
        if not core or core in STOP_WAT:
            continue
        if dest == core:
            dest = ""                                  # tributary of the same-named main river: no self-loop
        split = len(dests[core]) > 1
        vid = (f"WAT:{core}→{dest}" if dest in dests[core] else water_ref(core, eid)) if split else f"WAT:{core}"
        wid = kg.node("WAT", core, eid, nid=vid, desc=clause)
        did = kg.node("WAT", dest, eid, nid=water_ref(dest, eid)) if dest and dest not in ("",) else None
        if src_node and src_node in kg.nodes and kg.nodes[src_node]["type"] in ("MTN", "LND"):
            kg.edge(wid, src_node, "rises_at", eid, clause)
        if did:
            etype = "sinks_at" if "潛" in clause else "flows_into"
            kg.edge(wid, did, etype, eid, clause, direction=d)
    for core, lake, eid, clause in sinks:
        wid = water_ref(core, eid) if core in variant_home else f"WAT:{core}"
        if wid in kg.nodes:
            lid = kg.node("WAT", lake, eid, nid=f"WAT:{lake}")
            kg.edge(wid, lid, "sinks_at", eid, clause)
    # generic nodes of split homonyms: re-point edges and mentions to the right variant, then drop the generic node
    for core in list(variant_home):
        gid = f"WAT:{core}"
        if gid not in kg.nodes:
            continue
        g = kg.nodes.pop(gid)
        for x in kg.edges:
            if x["src"] == gid:
                x["src"] = water_ref(core, x["entry"])
            if x["dst"] == gid:
                x["dst"] = water_ref(core, x["entry"])
        for eid in g["mentions"]:
            vid = water_ref(core, eid)
            kg.node("WAT", core, eid, nid=vid)
            kg.mentions[eid] = [i for i in kg.mentions[eid] if i != gid]
    kg.edges = [x for x in kg.edges if x["src"] != x["dst"]]
    # water properties
    inflow = Counter(x["dst"] for x in kg.edges if x["type"] == "flows_into")
    for nid, n in kg.nodes.items():
        if n["type"] != "WAT":
            continue
        outs = [x for x in kg.edges if x["src"] == nid and x["type"] == "flows_into"]
        dirs = Counter(x["attrs"].get("direction") for x in outs if x["attrs"].get("direction"))
        dest_types = Counter("sea" if kg.nodes[x["dst"]]["symbol"].endswith("海") else
                             "lake" if re.search(r"(澤|淵|池)$", kg.nodes[x["dst"]]["symbol"]) else
                             "desert" if "沙" in kg.nodes[x["dst"]]["symbol"] else "river" for x in outs)
        n["props"].update({"n_inflows": inflow.get(nid, 0),
                           "flow_dir": dirs.most_common(1)[0][0] if dirs else None,
                           "dest_type": dest_types.most_common(1)[0][0] if dest_types else None,
                           "subtype": "sea" if n["symbol"].endswith("海") else
                           "lake" if re.search(r"(澤|淵|池|泉)$", n["symbol"]) else "river"})
    # same_name links between homonymous mountains
    groups = defaultdict(list)
    for nid, n in kg.nodes.items():
        if n["type"] == "MTN":
            groups[n["symbol"]].append(nid)
    for sym, ids in groups.items():
        for a, b in zip(ids, ids[1:]):
            kg.edge(a, b, "same_name", kg.nodes[a]["mentions"][0], sym)

    merge_duplicates(kg)
    write(kg, entries)


def merge_duplicates(kg):
    """Fold LND / UNK nodes into a typed node with the same (or suffixed) symbol created elsewhere — references
    can be met before the entity they point to."""
    redirect = {}
    for nid, n in list(kg.nodes.items()):
        if n["type"] not in ("LND", "UNK"):
            continue
        target = None
        for t in ("POL", "MTN", "WAT", "CRE", "PER", "PLA"):
            target = kg.lookup(n["symbol"], (t,))
            if target and target != nid:
                break
            target = None
        if target:
            redirect[nid] = target
    for old, new in redirect.items():
        o, n = kg.nodes.pop(old), kg.nodes[new]
        for e in o["mentions"]:
            if e not in n["mentions"]:
                n["mentions"].append(e)
        n["descriptions"] += o["descriptions"]
        n["variants"] = sorted(set(n["variants"]) | {o["symbol"]})
    for x in kg.edges:
        x["src"], x["dst"] = redirect.get(x["src"], x["src"]), redirect.get(x["dst"], x["dst"])
    for e, ids in kg.mentions.items():
        seen = []
        for i in ids:
            j = redirect.get(i, i)
            if j not in seen:
                seen.append(j)
        kg.mentions[e] = seen
    kg.edges = [x for x in kg.edges if x["src"] != x["dst"]]


def write(kg, entries):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "nodes.jsonl").open("w") as f:
        for nid in sorted(kg.nodes):
            f.write(json.dumps(kg.nodes[nid], ensure_ascii=False) + "\n")
    with (OUT / "edges.jsonl").open("w") as f:
        for x in kg.edges:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    with (OUT / "mentions.jsonl").open("w") as f:
        for e in entries:
            f.write(json.dumps({"entry": e["id"], "nodes": kg.mentions.get(e["id"], [])}, ensure_ascii=False) + "\n")
    # GraphML
    g = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
         '<key id="type" for="node" attr.name="type" attr.type="string"/>',
         '<key id="symbol" for="node" attr.name="symbol" attr.type="string"/>',
         '<key id="mentions" for="node" attr.name="mentions" attr.type="string"/>',
         '<key id="etype" for="edge" attr.name="type" attr.type="string"/>',
         '<key id="entry" for="edge" attr.name="entry" attr.type="string"/>',
         '<graph id="shanhaijing" edgedefault="directed">']
    for nid in sorted(kg.nodes):
        n = kg.nodes[nid]
        g.append(f'<node id="{escape(nid)}"><data key="type">{n["type"]}</data><data key="symbol">{escape(n["symbol"])}'
                 f'</data><data key="mentions">{" ".join(n["mentions"])}</data></node>')
    for i, x in enumerate(kg.edges):
        g.append(f'<edge id="e{i}" source="{escape(x["src"])}" target="{escape(x["dst"])}"><data key="etype">{x["type"]}'
                 f'</data><data key="entry">{x["entry"]}</data></edge>')
    g += ["</graph>", "</graphml>"]
    (OUT / "shanhaijing.graphml").write_text("\n".join(g))
    coverage(kg, entries)


def coverage(kg, entries):
    types = Counter(n["type"] for n in kg.nodes.values())
    etypes = Counter(x["type"] for x in kg.edges)
    no_ent = [e["id"] for e in entries if not kg.mentions.get(e["id"])]
    doc_only = [e["id"] for e in entries if all(kg.nodes[n]["type"] == "DOC" for n in kg.mentions.get(e["id"], []))]
    # name patterns that appear but are in no node of that paragraph
    pats = [("曰X", r"(?:名曰|其名曰|曰)([^，。；、]{1,5})"), ("X之山／X山", r"([^\s，。；、]{1,5}?(?:之山|山))"),
            ("X水", r"([^\s，。；、]{1,4}?水)(?:出|注)"), ("X國", r"([^\s，。；、]{1,5}?國)"), ("X民", r"([^\s，。；、]{1,3}民)")]
    misses = []
    EXPLAIN = [
        (r"[一二三四五六七八九十百千萬]+山$|其餘[^山]*山", "count of mountains"),
        (r"經之山|五臧山|^右", "colophon / book title"),
        (r"天下名山|出[銅鐵]之山|有大山|大山$|此[一二三]山", "generic phrase, not a name"),
        (r"[億萬]|^[一二三四五六七八九十百千]", "number"),
        (r"是謂|[！？]", "speech or definition, not a name"),
        (r"始為國|為之國|始作下民|潛為|所經", "narrative phrase, not a name"),
        (r"(?:狀|實)如", "simile (「其狀如山雞」), not a name"),
    ]
    for e in entries:
        syms = [kg.nodes[n]["symbol"] for n in kg.mentions.get(e["id"], [])]
        txt = PUNCT.sub("", e["text"])
        alt_spans = [(m.start(), m.end()) for m in re.finditer(r"一曰[^。]*|文曰[^，。]*|曰[^，。]*姓", txt)]
        for label, p in pats:
            for m in re.finditer(p, txt):
                if any(a <= m.start() < b for a, b in alt_spans):
                    misses.append((e["id"], label, m.group(1), "explained: alternate account / inscription / surname"))
                    continue
                why = next((w for rx, w in EXPLAIN if re.search(rx, m.group(1))), None)
                if why:
                    misses.append((e["id"], label, m.group(1), f"explained: {why}"))
                    continue
                raw = re.sub(r"^.*經(?:之首曰)?", "", clean(m.group(1))) if label == "X之山／X山" else clean(m.group(1))
                core = water_core(raw) if label == "X水" else re.sub(r"之?(國|山)$", "", raw)
                if not core or len(core) < 1:
                    continue
                if any(c and (c in s or s in c) for s in syms if s for c in (core, core[1:])):
                    continue
                if (raw in STOP_MTN | STOP_WAT | STOP_POL or core in STOP_MTN | STOP_WAT | STOP_POL
                        or re.search(r"[其則是見此]", raw) or raw in ("山", "國", "民")):
                    misses.append((e["id"], label, m.group(1), "explained: generic/pronoun, not a name"))
                else:
                    misses.append((e["id"], label, m.group(1), "UNEXPLAINED"))
    unexplained = [x for x in misses if x[3] == "UNEXPLAINED"]
    L = ["# 知識圖譜覆蓋檢查 / Knowledge-graph coverage audit", "",
         f"Paragraphs: {len(entries)} · nodes: {len(kg.nodes)} · edges: {len(kg.edges)}", "",
         "| node type | count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(types.items())] + \
        ["", "| edge type | count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(etypes.items())] + \
        ["", f"## 1. 沒有任何實體的段落 / Paragraphs with no entity: **{len(no_ent)}**", ""] + [f"- `{x}`" for x in no_ent] + \
        ["", f"## 2. 只有結構性文字（DOC）的段落 / Paragraphs with structural text only: {len(doc_only)}", "",
         "Section summaries, colophons and ritual notes; represented by DOC nodes so they still appear in the deliverable.",
         ""] + [f"- `{x}`" for x in doc_only] + \
        ["", f"## 3. 名稱句式未被抽出 / Name patterns not captured: **{len(unexplained)} unexplained**, "
             f"{len(misses) - len(unexplained)} explained", "", "| entry | pattern | text | status |", "|---|---|---|---|"] + \
        [f"| `{a}` | {b} | {c} | {d} |" for a, b, c, d in misses]
    (OUT / "coverage.md").write_text("\n".join(L) + "\n")
    print(f"nodes {len(kg.nodes)} {dict(types)}; edges {len(kg.edges)}; no-entity paragraphs {len(no_ent)}; "
          f"unexplained misses {len(unexplained)}", file=sys.stderr)


if __name__ == "__main__":
    main()
