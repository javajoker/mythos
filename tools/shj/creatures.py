"""Extract every creature description in the book and tag it by description only (Method G, stage G1).

A creature segment starts at 「有獸焉」「有鳥焉」「有魚焉」「有蛇焉」, at 「其中多X，其狀如…」/「是多X，狀如…」,
or (in the Sea and Wilderness books) at 「X，其狀如…」, and runs until the next creature, plant or river clause.
Names are kept for display only; tags are computed with the name clause masked (tools/shj/cues.py).

Output: projects/shanhaijing/data/derived/creatures.jsonl
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cues import creature_tags  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ROOT / "reference/shanhaijing/data/entries.jsonl"
OUT = ROOT / "projects/shanhaijing/data/derived/creatures.jsonl"

KIND = {"獸": "beast", "鳥": "bird", "魚": "fish", "蛇": "snake", "蟲": "beast"}
RE_START = re.compile(
    r"有(?P<k1>獸|鳥|魚|蛇|蟲)焉"
    r"|(?:其中|是)多(?P<n2>[^，。；]{1,4})，(?:其)?狀如"
    r"|有(?:[青赤黃白黑蒼]|五采之)?(?P<k3>獸|鳥|蛇|魚)[，。]"
    r"|(?:^|。)(?P<n4>(?!有)[^，。；]{1,4})，?其狀如")
RE_END = re.compile(r"有(?:獸|鳥|魚|蛇|蟲|木|草)焉|[^，。]{1,6}之?水出焉|其祠|(?:其中|是)多[^，。；]{1,4}，(?:其)?狀如")
RE_NAME = re.compile(r"(?:其名曰|名曰)([^，。；]{1,6})")


def main():
    out = []
    for line in ENTRIES.open():
        e = json.loads(line)
        t = e["text"]
        starts = list(RE_START.finditer(t))
        for i, m in enumerate(starts):
            s = m.end()
            nxt = starts[i + 1].start() if i + 1 < len(starts) else len(t)
            stop = RE_END.search(t, s)
            end = min(nxt, stop.start() if stop else len(t))
            seg = t[m.start():end]
            kind = KIND.get(m.group("k1") or m.group("k3") or "", "fish" if "其中多" in m.group(0) else "unknown")
            nm = RE_NAME.search(seg)
            name = (nm.group(1) if nm else (m.group("n2") or m.group("n4") or "")).strip()
            tags = sorted(creature_tags(seg))
            if kind == "unknown" and ("body_fish" in tags or name.endswith("魚")):
                kind = "fish"
            if len([x for x in tags if x not in ("vocal", "aquatic", "marine")]) < 2:
                continue
            out.append({"cid": f"{e['id']}#{i + 1}", "entry_id": e["id"], "book": e["book"], "section": e["section"],
                        "layer": e["layer"], "kind": kind, "name_display_only": name, "text": seg, "tags": tags})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(out)} creature descriptions", file=sys.stderr)


if __name__ == "__main__":
    main()
