"""Extract the itinerary skeleton of the 五藏山經 from working-text.jsonl.

This is a textual extractor only. It assigns no modern places and never silently
falls back to base readings when the working text is absent. Flow directions are
source assertions, not modern hydrological vetoes.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cn_numerals import parse as cn  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
OUT = ROOT / "projects/shanhaijing/data/derived"
WORKING = OUT / "working-text.jsonl"

DIRS = "東南|東北|西南|西北|東|西|南|北"
NUM = "[〇零一二兩三四五六七八九十百千萬]+"
BEARING_DEG = {"北": 0, "東北": 45, "東": 90, "東南": 135, "南": 180, "西南": 225, "西": 270, "西北": 315}
RE_STATION = re.compile(rf"^(?P<again>又)?(?P<dir>{DIRS})(?P<leg>(?:[^，。曰至有]*?{NUM}里，?)+)"
                        rf"(?:曰|至於|至|有)?(?P<name>[^，。；]+?)(?:[，。；]|$)")
RE_FIRST = re.compile(r"之首.{0,12}?[，。]?其(?:首|名)曰(?P<name>[^，。；]+)|之首，?曰(?P<name2>[^，。；]+)")
RE_LEG_PART = re.compile(rf"(?P<mode>水行|流沙|山行|陸行)?(?P<n>{NUM})里")
RE_RIVER = re.compile(rf"(?P<river>[^，。；]{{1,8}}?之?水)出(?P<where>焉|於其[陽陰]|其[陽陰]|於其上|其上|於其下)?"
                      rf"[，]?而?(?P<dir>{DIRS})?流注?於(?P<to>[^，。；]+)")
RE_CREATURE = re.compile(r"有(?P<kind>獸|鳥|魚|蛇|木|草|神|人)焉，(?P<desc>(?:(?!有[獸鳥魚蛇木草神人]焉).)*?)(?:其名曰|名曰)(?P<name>[^，。；]+)")
RE_SUMMARY = re.compile(rf"凡(?P<what>.+?)，?(?:自|起)?(?P<span>.*?)凡(?P<n_mtn>{NUM}(?:有{NUM})?)山，(?P<li>{NUM})里")


def norm(t: str) -> str:
    return t.translate(str.maketrans({"于": "於", "隂": "陰"}))


def parse_leg(leg: str):
    parts = [{"mode": m.group("mode") or "陸行(默認)", "li": cn(m.group("n"))} for m in RE_LEG_PART.finditer(leg)]
    total = sum(p["li"] for p in parts if p["li"]) if parts else None
    return parts, total


def load_working_entries():
    if not WORKING.exists():
        raise SystemExit("working-text.jsonl is required; run align_witness.py first")
    metadata = {e["id"]: e for e in (json.loads(line) for line in ENTRIES.open(encoding="utf-8"))}
    records = []
    for line in WORKING.open(encoding="utf-8"):
        row = json.loads(line)
        entry_id = row.get("entry_id")
        if not entry_id:
            continue
        record = dict(metadata[entry_id])
        record["text"] = row["text"]
        record["reading_source"] = row.get("reading_source", "unknown")
        record["reading_status"] = row.get("reading_status", "unreviewed")
        records.append(record)
    return records


def main():
    entries = load_working_entries()
    stations, sections = [], []
    seq = defaultdict(int)
    for e in entries:
        if e["book_no"] > 5:
            continue
        t = norm(e["text"])
        key = (e["book_no"], e["section_no"])
        sm = RE_SUMMARY.search(t)
        if t.startswith("凡") and sm:
            sections.append({"entry_id": e["id"], "book": e["book"], "section": e["section"],
                             "stated_mountains": cn(sm.group("n_mtn").replace("有", "")), "stated_li": cn(sm.group("li")),
                             "reading_source": e["reading_source"], "reading_status": e["reading_status"], "text": e["text"]})
            continue
        m = RE_STATION.match(t)
        first = RE_FIRST.search(t) if seq[key] == 0 else None
        if not m and not first:
            continue
        seq[key] += 1
        rec = {"entry_id": e["id"], "book": e["book"], "section": e["section"], "seq": seq[key],
               "reading_source": e["reading_source"], "reading_status": e["reading_status"]}
        if m and not (first and seq[key] == 1 and "之首" in t[:12]):
            parts, total = parse_leg(m.group("leg"))
            rec.update({"bearing": m.group("dir"), "bearing_deg": BEARING_DEG[m.group("dir")],
                        "leg_raw": m.group("leg"), "leg_parts": parts, "leg_li": total,
                        "name": m.group("name"), "explicit_again": bool(m.group("again"))})
        else:
            rec.update({"bearing": None, "bearing_deg": None, "leg_raw": "", "leg_parts": [], "leg_li": 0,
                        "name": (first.group("name") or first.group("name2")), "start": True})
        rec["complex_leg"] = any(p["mode"] != "陸行(默認)" for p in rec["leg_parts"]) or len(rec["leg_parts"]) > 1
        rec["rivers"] = [{"river": r.group("river").lstrip("而"), "where": r.group("where") or "焉",
                          "flow": r.group("dir"), "to": r.group("to")} for r in RE_RIVER.finditer(t)]
        rec["creatures"] = [{"kind": c.group("kind"), "desc": c.group("desc").rstrip("，"), "name": c.group("name")}
                            for c in RE_CREATURE.finditer(t)]
        stations.append(rec)

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "stations.jsonl").open("w", encoding="utf-8") as handle:
        for station in stations:
            handle.write(json.dumps(station, ensure_ascii=False) + "\n")
    with (OUT / "sections.jsonl").open("w", encoding="utf-8") as handle:
        for section in sections:
            handle.write(json.dumps(section, ensure_ascii=False) + "\n")

    by_sec = defaultdict(list)
    for station in stations:
        by_sec[(station["book"], station["section"])].append(station)
    lines = ["# 五藏山經 itinerary consistency / 山經里程自洽性檢查", "",
             "Generated from `working-text.jsonl`. Differences are review candidates, not automatic corrections.", "",
             "| 書 | 篇 | stations found | stated 山 | Σ leg 里 | stated 里 | Δ山 | Δ里 |", "|---|---|---|---|---|---|---|---|"]
    for section in sections:
        found = by_sec.get((section["book"], section["section"]), [])
        leg_sum = sum(s["leg_li"] or 0 for s in found)
        mountain_delta = len(found) - (section["stated_mountains"] or 0)
        li_delta = leg_sum - (section["stated_li"] or 0)
        lines.append(f"| {section['book']} | {section['section']} | {len(found)} | {section['stated_mountains']} | {leg_sum} | "
                     f"{section['stated_li']} | {mountain_delta:+d} | {li_delta:+d} |")
    (OUT / "routes-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(stations)} stations, {len(sections)} section summaries", file=sys.stderr)


if __name__ == "__main__":
    main()
