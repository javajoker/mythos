"""Ingest the Wikisource base text of 山海經 into structured, citable entries.

Input : reference/shanhaijing/sources/wikisource-base/NN-書名.wiki
Output: reference/shanhaijing/data/entries.jsonl   (one JSON object per paragraph/entry)
        reference/shanhaijing/text/NN-書名.md        (clean reading text, entry IDs as anchors)

Entry ID: SHJ-BB-S-EEE  (BB = book 01-18, S = section within book, EEE = paragraph number in section)

Markup handled:
  {{*|...}}          interlinear commentary (mostly 郭璞注, some later)   -> notes[]
  {{另|主|異}}        variant reading                                    -> main text + variants[]
  {{另2|主|說明}}      variant with explanatory note                       -> main text + variants[]
  {{!|字|IDS}}        rare character                                     -> 字
  <ref>...</ref>     modern editorial footnote (e.g. 袁珂)                -> editorial_refs[]
Modern editorial notes are kept as *claims about* the text, never as conclusions (see methodology spec §3).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "reference/shanhaijing/sources/wikisource-base"
OUT_DATA = ROOT / "reference/shanhaijing/data"
OUT_TEXT = ROOT / "reference/shanhaijing/text"

BOOKS = ["南山經", "西山經", "北山經", "東山經", "中山經",
         "海外南經", "海外西經", "海外北經", "海外東經",
         "海內南經", "海內西經", "海內北經", "海內東經",
         "大荒東經", "大荒南經", "大荒西經", "大荒北經", "海內經"]
BOOKS_EN = ["Classic of the Southern Mountains", "Classic of the Western Mountains",
            "Classic of the Northern Mountains", "Classic of the Eastern Mountains",
            "Classic of the Central Mountains",
            "Classic of Regions Beyond the Seas: South", "Classic of Regions Beyond the Seas: West",
            "Classic of Regions Beyond the Seas: North", "Classic of Regions Beyond the Seas: East",
            "Classic of Regions Within the Seas: South", "Classic of Regions Within the Seas: West",
            "Classic of Regions Within the Seas: North", "Classic of Regions Within the Seas: East",
            "Classic of the Great Wilderness: East", "Classic of the Great Wilderness: South",
            "Classic of the Great Wilderness: West", "Classic of the Great Wilderness: North",
            "Classic of Regions Within the Seas"]


def layer(book_no: int) -> str:
    if book_no <= 5:
        return "山經"
    if book_no <= 13:
        return "海外經" if book_no <= 9 else "海內經(四篇)"
    return "大荒經" if book_no <= 17 else "海內經"


def split_args(body: str) -> list[str]:
    """Split template arguments on top-level '|'."""
    args, depth, cur = [], 0, []
    i = 0
    while i < len(body):
        if body.startswith("{{", i):
            depth += 1; cur.append("{{"); i += 2; continue
        if body.startswith("}}", i):
            depth -= 1; cur.append("}}"); i += 2; continue
        if body[i] == "|" and depth == 0:
            args.append("".join(cur)); cur = []; i += 1; continue
        cur.append(body[i]); i += 1
    args.append("".join(cur))
    return args


def parse_paragraph(raw: str):
    """Return (clean_text, notes, variants, refs). Offsets are into clean_text."""
    out, notes, variants, refs = [], [], [], []
    i = 0
    while i < len(raw):
        if raw.startswith("<ref", i):
            end = raw.find("</ref>", i)
            start_body = raw.find(">", i) + 1
            refs.append({"at": len("".join(out)), "text": raw[start_body:end].strip()})
            i = end + len("</ref>")
            continue
        if raw.startswith("{{", i):
            depth, j = 0, i
            while j < len(raw):
                if raw.startswith("{{", j):
                    depth += 1; j += 2
                elif raw.startswith("}}", j):
                    depth -= 1; j += 2
                    if depth == 0:
                        break
                else:
                    j += 1
            body = raw[i + 2:j - 2]
            name, *args = split_args(body)
            at = len("".join(out))
            if name == "*":
                inner, *_ = parse_paragraph("|".join(args))
                notes.append({"at": at, "text": inner})
            elif name in ("另", "另2"):
                main = parse_paragraph(args[0])[0] if args else ""
                alt = parse_paragraph(args[1])[0] if len(args) > 1 else ""
                out.append(main)
                variants.append({"at": at, "main": main, "alt": alt, "kind": "note" if name == "另2" else "reading"})
            elif name == "!":
                out.append(args[0] if args else "")
            else:
                out.append("")  # unknown template: drop, but keep position
            i = j
            continue
        out.append(raw[i]); i += 1
    text = "".join(out)
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", text)
    text = text.replace("'''", "").replace("''", "").replace("【】", "")
    return text.strip().lstrip("　").strip(), notes, variants, refs


def ingest_book(book_no: int):
    name = BOOKS[book_no - 1]
    path = SRC / f"{book_no:02d}-{name}.wiki"
    wiki = path.read_text(encoding="utf-8")
    # drop header template and trailing non-text blocks
    wiki = re.sub(r"\{\{Textquality[^}]*\}\}", "", wiki)
    wiki = re.sub(r"\{\{header2.*?\n\}\}", "", wiki, flags=re.S)
    wiki = re.sub(r"<gallery>.*?</gallery>", "", wiki, flags=re.S)
    wiki = re.sub(r"<references\s*/?>", "", wiki)
    wiki = re.sub(r"\[\[Category:[^\]]*\]\]", "", wiki)

    section_no, section, para_no, entries = 0, name, 0, []
    in_notes_section = False
    for line in wiki.splitlines():
        s = line.strip()
        if not s:
            continue
        m = re.fullmatch(r"==\s*([^=]+?)\s*==", s)
        if m:
            if m.group(1) == "註釋":
                in_notes_section = True
                continue
            in_notes_section = False
            section_no += 1; section = m.group(1); para_no = 0
            continue
        if in_notes_section or s.startswith(("{{", "__", "<", "http")) and not s.startswith("{{另"):
            continue
        if section_no == 0:
            section_no, section = 1, name
        para_no += 1
        text, notes, variants, refs = parse_paragraph(s)
        if not text:
            para_no -= 1
            continue
        entries.append({
            "id": f"SHJ-{book_no:02d}-{section_no}-{para_no:03d}",
            "book_no": book_no, "book": name, "book_en": BOOKS_EN[book_no - 1],
            "layer": layer(book_no), "section_no": section_no, "section": section,
            "para_no": para_no, "text": text,
            "notes": notes, "variants": variants, "editorial_refs": refs,
            "source": f"wikisource:山海經/{name}",
        })
    return entries


def write_markdown(book_no: int, entries: list[dict]):
    name = BOOKS[book_no - 1]
    lines = [f"# 山海經 卷{book_no:02d}・{name}", "",
             f"*{BOOKS_EN[book_no - 1]}* — clean reading text (commentary removed; see `data/entries.jsonl`).", "",
             "Source: Wikisource 《山海經》 base text (public domain). Each paragraph carries its citable entry ID.", ""]
    cur = None
    for e in entries:
        if e["section"] != cur:
            cur = e["section"]
            lines += [f"## {cur}", ""]
        flag = ""
        if e["variants"]:
            flag += " ⟨異文 " + "；".join(f"{v['main']}／{v['alt']}" for v in e["variants"]) + "⟩"
        lines += [f"<a id=\"{e['id']}\"></a>**`{e['id']}`** {e['text']}{flag}", ""]
    (OUT_TEXT / f"{book_no:02d}-{name}.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT_DATA.mkdir(parents=True, exist_ok=True)
    OUT_TEXT.mkdir(parents=True, exist_ok=True)
    all_entries = []
    for b in range(1, 19):
        es = ingest_book(b)
        write_markdown(b, es)
        all_entries += es
    with open(OUT_DATA / "entries.jsonl", "w", encoding="utf-8") as f:
        for e in all_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    chars = sum(len(e["text"]) for e in all_entries)
    print(f"{len(all_entries)} entries, {chars} characters of main text", file=sys.stderr)


if __name__ == "__main__":
    main()
