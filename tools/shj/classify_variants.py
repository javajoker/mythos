"""First-pass classification of collation differences (task T-102).

Only mechanically safe cases are auto-classified; automatic rows are proposals, not semantic adjudication.
Overrides may come from LLM or human review and use the precedence human > llm > auto. Every row carries a
`decision_status`, so downstream consumers can distinguish proposals from confirmed decisions.

Statuses (data-model §4):
  orthographic        pure glyph variant (異體) or conventional interchange (古今字/通假, subtype noted)
  displacement        difference caused by a registered X3 relocation block
  interpolation       text the base inserted (I-001/I-002, confirmed absent from both witnesses)
  transcription-gap   text missing from a witness transcription (page gap)
  witness-noise       wiki notices / stray notes in the witness transcription, not text
  base-deviation      the base differs from BOTH early witnesses, which agree with each other (factual candidate;
                      changing the working reading still requires an LLM/human decision)
  scribal-error       (human only) one reading is a copying error
  substantive         (human only) genuinely different readings
  unclassified        needs review; see `hint`

Input : projects/shanhaijing/data/derived/collation.jsonl, displacements.jsonl
        projects/shanhaijing/ledgers/variant-overrides.jsonl   (human decisions; optional)
Output: projects/shanhaijing/data/derived/variant-classes.jsonl, variant-classes-summary.md
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DER = ROOT / "projects/shanhaijing/data/derived"
OVERRIDES = ROOT / "projects/shanhaijing/ledgers/variant-overrides.jsonl"

# Pure glyph variants: same word, different written form. Conservative — when in doubt, leave it out.
GLYPH = [
    "面靣", "柏栢", "美羙", "玄𤣥", "高髙", "仞仭", "鳳鳯", "鐵鐡", "鼓皷", "鼓鼔", "鼓𡔷", "歷歴", "苗苖", "枏柟",
    "鉤鈎", "歲歳", "嚻囂", "鳧鳬", "內内", "椶㯶", "陵𨹧", "豎竪", "荊荆", "瑤瑶", "皋皐", "皋臯", "臯皐", "訆䚯",
    "訆叫", "訆呌", "叫呌", "貍狸", "冢冡", "塚冡", "獆獋", "蔥葱", "蹏蹄", "潜潛", "潛濳", "瑉珉", "柳栁", "柳桞",
    "栁桞", "葬𦵏", "葬塟", "劍劔", "鴟䲭", "涅𣵀", "久乆", "象𧰼", "德徳", "玉玊", "鶏雞", "䪥薤", "懷懐", "彙彚",
    "器噐", "妒妬", "苟茍", "棃梨", "夔䕫", "腸膓", "鬱鬰", "虔䖍", "緣縁", "類𩔗", "棗𬃷", "出岀", "爪𤓰", "瓜𤓰",
    "笑𥬇", "菟莬", "泰㤗", "戲戱", "鵹𪁐", "恒恆", "恒𢘆", "步歩", "鄉郷", "蘇蘓", "卵𡖉", "卵夘", "謠謡", "蛇虵",
    "留畱", "臥卧", "橐槖", "冒冐", "藏蔵", "乘乗", "錄録", "收𭣣", "鵌䳜", "疏䟽", "棘𣗥", "晋晉", "晉𣈆", "鈎鉤",
    "邛卭", "吳吴", "吳呉", "吴呉", "銳鋭", "鬣鬛", "寇冦", "綠緑", "脃脆", "脫脱", "虛虚", "腳脚", "俎爼", "厀膝",
    "䣛膝", "繫繋", "解觧", "明眀", "會㑹", "溫温", "戶戸", "僕㒒", "達逹", "弘𢎞", "真眞", "瑶瑤", "濱濵", "往徃",
    "来來", "慎愼", "尋㝷", "賴頼", "稻稲", "宮宫", "青靑", "聯聮", "聯聨", "侯矦", "奧奥", "蓋葢", "棄弃", "勳勲",
    "縛縳", "怪恠", "伏㐲", "夾㚒", "敘敍", "猬蝟", "曾曽", "涌湧", "黎𥠖", "銜㗸", "船舡", "樹𣗳", "并並",
    "鳳凰"[:0] or "髮髪",  # placeholder-safe: 髮/髪
]
# Conventional interchanges (古今字 / 通假 / 異寫): same meaning in classical usage but distinct characters.
CONVENTIONAL = {
    "采彩": "通假", "原源": "古今字", "虛墟": "古今字", "涂塗": "古今字", "后後": "通假", "遊游": "異寫", "游遊": "異寫",
    "柜櫃": "古今字", "鍾鐘": "通假", "尸屍": "古今字", "屍尸": "古今字", "腳足": "同義", "云雲": "古今字",
    "要腰": "古今字", "累纍": "古今字", "誌志": "通假", "惟維": "通假", "披被": "通假", "沈沉": "異寫",
    "湧涌": "異寫", "嶽獄": "形近?", "岳嶽": "異寫", "脣唇": "異寫", "托託": "通假", "無毋": "通假", "毋母": "形近?",
    "采採": "古今字", "胏肺": "異寫", "蠭蜂": "異寫", "豪毫": "古今字", "如若": "同義", "菟兔": "通假", "腊臘": "異寫",
    "沙砂": "異寫", "狸貍": "異寫", "皇凰": "古今字", "席蓆": "古今字", "暴𭧂": "異寫", "糱櫱": "異寫", "糱蘖": "異寫",
    "籜蘀": "異寫", "璇琁": "異寫", "梨犂": "異寫", "梨犁": "異寫", "響嚮": "通假", "鄉嚮": "通假", "眯昧": "形近?",
}
# Meaning-changing pairs that look alike: likely copying errors one way or the other (X2 candidates) — review.
SIMILAR = {"白自", "自白", "已己", "己已", "氐互", "民氏", "役沒", "役没", "肆肄", "泠冷", "反大", "山出", "林木", "玉金",
           "北百", "北比", "比北", "犬大", "大犬", "木水", "木不", "曰目", "目曰", "首手", "天先", "刑形", "瞑暝", "雎睢",
           "粟栗", "章樟", "茈芘", "封邽", "淅浙", "州川", "百甘", "几凡", "烏鳥", "雪雷", "夙風", "立帝", "林陵", "狗拘",
           "垣短", "嫘雷", "臂耳", "脣臂", "清青", "桓柏", "桃栁", "桃柳", "鵌䳜", "毋母", "眯昧", "嶽獄"}
NUMERALS = set("一二三四五六七八九十百千萬")
PARTICLES = set("之而焉也其于於者曰以有乃是則亦")
NOISE = ("此頁面可能存在", "按夏後開即啟避漢景帝諱")


def pairset(pairs):
    out = set()
    for p in pairs:
        if len(p) == 2:
            out.add(p); out.add(p[::-1])
    return out


GLYPHS = pairset(GLYPH)
CONV = {}
for k, v in CONVENTIONAL.items():
    CONV[k] = v; CONV[k[::-1]] = v


def key(d):
    return f"{d['entry_id']}|{d['witness']}|{d['op']}|{d['base']}|{d['witness_text']}"


def classify(d, x3, gaps, agree):
    b, w = d["base"], d["witness_text"]
    if d["entry_id"] in x3:
        return "displacement", f"inside {x3[d['entry_id']]}"
    if d["entry_id"] in gaps.get(d["witness"], set()) and d["op"] == "delete":
        return "transcription-gap", "known page gap (source-assessment §3.2)"
    if any(n in w for n in NOISE):
        return "witness-noise", "wiki notice or stray note in the witness transcription"
    if d["entry_id"] == "SHJ-18-1-008" and "素女所出" in b:
        return "interpolation", "I-001"
    if d["op"] == "replace" and len(b) == len(w):
        pairs = [b[i] + w[i] for i in range(len(b)) if b[i] != w[i]]
        if pairs and all(p in GLYPHS for p in pairs):
            return "orthographic", "異體"
        if pairs and all(p in GLYPHS or p in CONV for p in pairs) and not any(p in SIMILAR for p in pairs):
            return "orthographic", "/".join(sorted({CONV[p] for p in pairs if p in CONV}))
    both = (d["entry_id"], d["op"], b, w) in agree      # the other witness has the same difference
    if both:
        # Factual, not a judgement of who is right: the base departs from BOTH early witnesses. It may be a base
        # typo or a modern editorial emendation (a prior conclusion, spec §3); the working text follows the witnesses.
        diff = set(b) | set(w)
        kind = ("numeral" if diff & NUMERALS else
                "look-alike" if d["op"] == "replace" and len(b) == len(w) and any(
                    b[i] + w[i] in SIMILAR for i in range(len(b))) else
                "particle" if set(b + w) <= PARTICLES else "other")
        return "base-deviation", f"both witnesses read 「{w}」 ({kind})"
    # needs review — give the reviewer a hint
    chars = set(b) | set(w)
    if chars & NUMERALS and (set(b) & NUMERALS or set(w) & NUMERALS):
        return "unclassified", "numeral (X1 candidate)"
    if d["op"] == "replace" and len(b) == len(w) and any(b[i] + w[i] in SIMILAR for i in range(len(b))):
        return "unclassified", "graphic-similar, meaning changes (X2 candidate)"
    if d["op"] in ("insert", "delete") and set(b + w) <= PARTICLES:
        return "unclassified", "particle only"
    if max(len(b), len(w)) >= 8:
        return "unclassified", "long passage — check displacement/gap/interpolation"
    return "unclassified", ""


def main():
    x3 = {}
    for l in (DER / "displacements.jsonl").open():
        r = json.loads(l)
        for i in r["entries"]:
            x3[i] = r["id"]
    gaps = {"sbck": {"SHJ-01-2-013", "SHJ-01-2-014", "SHJ-01-2-015"}}
    overrides = {}
    priority = {"auto": 0, "auto-v1": 0, "llm": 1, "human": 2}
    if OVERRIDES.exists():
        for l in OVERRIDES.open():
            if l.strip():
                r = json.loads(l)
                previous = overrides.get(r["key"])
                if previous is None or priority.get(r.get("by", "human"), 0) >= priority.get(previous.get("by", "human"), 0):
                    overrides[r["key"]] = r
    diffs = [json.loads(l) for l in (DER / "collation.jsonl").open()]
    seen = Counter((d["entry_id"], d["op"], d["base"], d["witness_text"]) for d in diffs)
    agree = {k for k, n in seen.items() if n >= 2}
    rows, c, hints = [], Counter(), Counter()
    for d in diffs:
        k = key(d)
        if k in overrides:
            o = overrides[k]
            st, why, by = o["status"], o.get("reason", ""), o.get("by", "human")
            decision_status = "decided" if by in ("human", "llm") else "proposed"
        else:
            st, why = classify(d, x3, gaps, agree)
            by = "auto-v1"
            decision_status = "proposed"
        rows.append({"key": k, **d, "status": st, "reason": why, "classifier": by, "decision_status": decision_status})
        c[st] += 1
        if st == "unclassified":
            hints[why or "(none)"] += 1
    with (DER / "variant-classes.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lines = ["# Variant classification / 異文分類", "",
             f"Generated by `tools/shj/classify_variants.py` from {len(rows)} collation differences. "
             "Auto rows are proposals only. Overrides live in "
             "`projects/shanhaijing/ledgers/variant-overrides.jsonl` and use human > llm > auto precedence.", "",
             "| status | count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in c.most_common()]
    lines += ["", "## Unclassified by hint / 待審異文（依提示）", "", "| hint | count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in hints.most_common()]
    lines += ["", "## Review queue: meaning-changing candidates / 優先審查（可能影響詞義）", ""]
    for r in rows:
        if (r["status"] == "base-deviation" and r["witness"] == "sbck" and "(other)" not in r["reason"]
                and "(particle)" not in r["reason"]) or (
                r["status"] == "unclassified" and r["reason"].startswith(("numeral", "graphic"))):
            lines.append(f"- `{r['entry_id']}` {r['witness']}: 「{r['base']}」→「{r['witness_text']}」 ({r['reason']}) "
                         f"…{r['context']}…")
    (DER / "variant-classes-summary.md").write_text("\n".join(lines) + "\n")
    print(dict(c))


if __name__ == "__main__":
    main()
