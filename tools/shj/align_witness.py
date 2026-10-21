"""Locate every base entry inside the 明成化本 (sbck) and 四庫本 (skqs) witnesses — tasks T-003/T-004/T-104.

The witnesses are unpunctuated and their line breaks follow the print layout, so paragraphs are not segmented
directly. Instead each base entry is *located* in the witness stream by character n-gram voting, which is
independent of paragraph order — relocated paragraphs are found wherever they actually sit.

Then:
  * entries are re-ordered by their sbck position          -> working-text.jsonl (Chenghua order)
  * entries whose base order breaks the sbck order         -> displacement candidates (X3), corroborated by skqs
  * witness text covered by no base entry                  -> witness-only spans (gaps in the base text)

Readings stay those of the base text in this pass and are explicitly marked `unreviewed`.
Choosing readings is a separate LLM/human adjudication task, not an alignment heuristic.

Output: projects/shanhaijing/data/derived/witness-alignment.jsonl, working-text.jsonl, alignment-summary.md
"""
import bisect
import difflib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collate import ENTRIES, OUT, norm, witness_sbck, witness_skqs  # noqa: E402

ORDER_OVERRIDES = OUT.parents[3] / "projects/shanhaijing/ledgers/working-order-overrides.jsonl"

K = 5                # n-gram length for voting
MAX_HITS = 6         # ignore n-grams that occur more often than this (formulaic phrases)
BUCKET = 24          # vote bucket width in characters
MAPPED, PARTIAL = 0.5, 0.2
MIN_GAP = 12         # minimum witness-only span worth reporting


def build_index(streams):
    idx = defaultdict(list)
    for b, s in streams.items():
        for p in range(len(s) - K + 1):
            idx[s[p:p + K]].append((b, p))
    return idx


def locate(text, idx, streams, hint=None):
    """Return {book, start, end, coverage} for the best placement of `text`, or None."""
    if len(text) < K:
        return locate_short(text, streams, hint)
    votes = Counter()
    offsets = defaultdict(list)
    grams = len(text) - K + 1
    for i in range(grams):
        hits = idx.get(text[i:i + K], ())
        if not hits or len(hits) > MAX_HITS:
            continue
        for b, p in hits:
            key = (b, (p - i) // BUCKET)
            votes[key] += 1
            offsets[key].append(p - i)
    if not votes:
        return locate_short(text, streams, hint)
    # merge neighbouring buckets
    def score(k):
        return votes[k] + votes.get((k[0], k[1] - 1), 0) + votes.get((k[0], k[1] + 1), 0)
    best = max(votes, key=score)
    offs = offsets[best] + offsets.get((best[0], best[1] - 1), []) + offsets.get((best[0], best[1] + 1), [])
    start = int(statistics.median(offs))
    return {"book": best[0], "start": max(0, start), "end": start + len(text),
            "coverage": round(min(1.0, score(best) / grams), 3)}


def locate_short(text, streams, hint):
    """Very short entries (e.g. 「有雙山」) are only searched near the previous located entry."""
    if not hint or not text:
        return None
    b, p = hint
    s = streams.get(b, "")
    q = s.find(text, max(0, p - 10), p + 400)
    if q < 0:
        return None
    return {"book": b, "start": q, "end": q + len(text), "coverage": 1.0}


def status(loc):
    if not loc:
        return "absent"
    return "aligned" if loc["coverage"] >= MAPPED else "partial" if loc["coverage"] >= PARTIAL else "absent"


def lis_members(keys):
    """Indices of one longest strictly increasing subsequence of `keys`."""
    tails, tails_i, prev = [], [], [-1] * len(keys)
    for i, k in enumerate(keys):
        j = bisect.bisect_left(tails, k)
        if j == len(tails):
            tails.append(k); tails_i.append(i)
        else:
            tails[j] = k; tails_i[j] = i
        prev[i] = tails_i[j - 1] if j else -1
    out, i = set(), tails_i[-1] if tails_i else -1
    while i >= 0:
        out.add(i); i = prev[i]
    return out


def align(entries, streams):
    idx = build_index(streams)
    res, hint = {}, None
    for e in entries:
        loc = locate(norm(e["text"]), idx, streams, hint)
        st = status(loc)
        if st == "absent":
            loc = None
        else:
            hint = (loc["book"], loc["end"])
        res[e["id"]] = {"status": st, **(loc or {})}
    return res


def pair_variants(entries, al, streams, names):
    """Second pass: an entry the n-grams missed is often a heavy variant of a witness-only span
    (e.g. 反舌國 / 岐舌國). Match it fuzzily against the uncovered spans of the whole witness."""
    strong = lambda a: a["status"] == "aligned"  # noqa: E731
    ids = [e["id"] for e in entries]
    floor = {}                                    # (book) -> lowest start still free after a re-pairing
    for n, e in enumerate(entries):
        a = al[e["id"]]
        if strong(a):
            continue
        prev = next((al[ids[k]] for k in range(n - 1, -1, -1) if strong(al[ids[k]])), None)
        nxt = next((al[ids[k]] for k in range(n + 1, len(ids)) if strong(al[ids[k]])), None)
        if not prev:
            continue
        t = norm(e["text"])
        book, lo = prev["book"], max(prev["end"], floor.get(prev["book"], 0)) - 4
        hi = nxt["start"] + 4 if nxt and nxt["book"] == book else prev["end"] + 3 * len(t) + 60
        s = streams[book]
        if min(hi, len(s)) - max(0, lo) < 0.5 * len(t):   # no room between aligned neighbours: text is missing
            continue
        best = None
        for st in range(max(0, lo), max(max(0, lo) + 1, min(hi, len(s)) - len(t) + 1)):
            w = s[st:st + len(t)]
            r = difflib.SequenceMatcher(None, t, w, autojunk=False).ratio()
            if not best or r > best[0]:
                best = (r, st, st + len(w))
        if best and best[0] >= 0.5 and best[0] > a.get("coverage", 0):
            al[e["id"]] = {"status": "fuzzy" if best[0] >= 0.8 else "variant", "book": book, "start": best[1], "end": best[2],
                           "coverage": round(best[0], 3)}
            floor[book] = best[2]


def blocks(entries, dis_sb, dis_sk, al):
    """Group displaced entries into relocation blocks (consecutive base entries moved to the same witness book).
    A block needs at least one member confirmed by both witnesses; sbck-only members adjacent to it join it."""
    out, cur = [], None
    for e in entries:
        i = e["id"]
        if i in dis_sb:
            tgt = al[i]["book"]
            if cur and cur["base_book"] == e["book_no"] and cur["sbck_book"] == tgt and cur["last"] == e["para_no"] - 1:
                cur["entries"].append(i); cur["last"] = e["para_no"]; cur["confirmed"] |= i in dis_sk
                continue
            cur = {"base_book": e["book_no"], "sbck_book": tgt, "entries": [i], "last": e["para_no"],
                   "confirmed": i in dis_sk, "editorial_ref": False}
            out.append(cur)
        else:
            cur = None
    by_id = {e["id"]: e for e in entries}
    for b in out:
        b["editorial_ref"] = any(by_id[i]["editorial_refs"] for i in b["entries"])
        del b["last"]
    return [b for b in out if b["confirmed"]], [b for b in out if not b["confirmed"]]


def displaced(entries, al):
    """Entry IDs whose position breaks the witness order (not on the LIS), per base book."""
    by_book = defaultdict(list)
    for e in entries:
        a = al[e["id"]]
        if a["status"] != "absent":
            by_book[e["book_no"]].append((e["id"], (a["book"], a["start"]), e["book_no"]))
    out = {}
    for b, rows in by_book.items():
        # cross-book moves are flagged directly; the order check runs only on entries that stayed in their book,
        # so a moved block cannot win an LIS tie against the book's own entries (e.g. section headers)
        home = [r for r in rows if r[1][0] == b]
        keep = {home[i][0] for i in lis_members([k[1] for _, k, _ in home])}
        for eid, key, bno in rows:
            if key[0] != bno or eid not in keep:
                out[eid] = {"cross_book": key[0] != bno}
    return out


def witness_only(streams, al, names):
    covered = defaultdict(list)
    for a in al.values():
        if a["status"] != "absent":
            covered[a["book"]].append((a["start"], a["end"]))
    spans = []
    for b, s in streams.items():
        iv = sorted(covered[b]); pos = 0
        for st, en in iv + [(len(s), len(s))]:
            if st - pos >= MIN_GAP:
                spans.append({"book": b, "book_name": names[b], "start": pos, "end": st, "text": s[pos:st]})
            pos = max(pos, en)
    return spans


def main():
    entries = [json.loads(l) for l in ENTRIES.open()]
    names = {e["book_no"]: e["book"] for e in entries}
    sbck = {b: witness_sbck(b) for b in range(1, 19)}
    skqs = {b: witness_skqs(b) for b in range(1, 19)}
    al_sb, al_sk = align(entries, sbck), align(entries, skqs)
    pair_variants(entries, al_sb, sbck, names)
    pair_variants(entries, al_sk, skqs, names)
    dis_sb, dis_sk = displaced(entries, al_sb), displaced(entries, al_sk)
    confirmed, unconfirmed = blocks(entries, dis_sb, dis_sk, al_sb)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "displacements.jsonl").open("w") as f:
        for n, b in enumerate(confirmed, 1):
            f.write(json.dumps({"id": f"X3-{n:03d}", "base_book": names[b["base_book"]],
                                "sbck_book": names[b["sbck_book"]], "entries": b["entries"],
                                "base_cites_modern_editor": b["editorial_ref"], "status": "registered"},
                               ensure_ascii=False) + "\n")

    with (OUT / "witness-alignment.jsonl").open("w") as f:
        for e in entries:
            i = e["id"]
            f.write(json.dumps({"entry_id": i, "base_book": e["book_no"], "sbck": al_sb[i], "skqs": al_sk[i],
                                "displaced_sbck": dis_sb.get(i), "displaced_skqs": dis_sk.get(i)},
                               ensure_ascii=False) + "\n")

    # working text: Chenghua order; base-only entries keep their slot after the base predecessor
    order_overrides = {}
    if ORDER_OVERRIDES.exists():
        for line in ORDER_OVERRIDES.open(encoding="utf-8"):
            if line.strip():
                override = json.loads(line)
                order_overrides[override["entry_id"]] = override
    order, last_key = [], (0, -1)
    for n, e in enumerate(entries):
        a = al_sb[e["id"]]
        override = order_overrides.get(e["id"])
        if override:
            if n == 0 or entries[n - 1]["id"] != override["after_entry"]:
                raise ValueError(f"working-order override for {e['id']} must follow {override['after_entry']}")
            order.append(((last_key[0], last_key[1], 1, n), e, a))
        elif a["status"] != "absent":
            last_key = (a["book"], a["start"])
            order.append(((a["book"], a["start"], 0, n), e, a))
        else:
            order.append(((last_key[0], last_key[1], 1, n), e, a))
    gaps = witness_only(sbck, al_sb, names)
    for g in gaps:
        order.append(((g["book"], g["start"], 0, -1), None, g))
    order.sort(key=lambda r: r[0])
    with (OUT / "working-text.jsonl").open("w") as f:
        for seq, (key, e, a) in enumerate(order, 1):
            if e is None:
                rec = {"seq": seq, "entry_id": None, "kind": "witness-only", "chenghua_book": a["book"],
                       "sbck_span": [a["start"], a["end"]], "text": a["text"],
                       "reading_source": "sbck", "reading_status": "unreviewed",
                       "note": "sbck text with no base entry (unpunctuated, normalised); LLM/human review required"}
            else:
                rec = {"seq": seq, "entry_id": e["id"],
                       "kind": a["status"] if a["status"] != "absent" else "base-only",
                       "chenghua_book": key[0], "base_book": e["book_no"],
                       "sbck_span": [a["start"], a["end"]] if a["status"] != "absent" else None,
                       "order_changed": e["id"] in dis_sb, "text": e["text"],
                       "order_override": order_overrides.get(e["id"], {}).get("after_entry"),
                       "reading_source": "wikisource-base", "reading_status": "unreviewed"}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # summary
    st_sb, st_sk = Counter(a["status"] for a in al_sb.values()), Counter(a["status"] for a in al_sk.values())
    by_id = {e["id"]: e for e in entries}
    lines = ["# Witness alignment / 見證本定位", "",
             "Generated by `tools/shj/align_witness.py`. Each base entry is located in the witness by 5-gram voting "
             "(order-independent), so relocated paragraphs are found where the witness actually has them. "
             "`fuzzy` = placed by similarity ≥ 0.8 between its aligned neighbours; `variant` = similarity 0.5–0.8 "
             "(heavy textual variant, review in T-102).", "",
             "| | aligned | fuzzy | variant | partial | absent |", "|---|---|---|---|---|---|",
             f"| 明成化本 sbck | {st_sb['aligned']} | {st_sb['fuzzy']} | {st_sb['variant']} | {st_sb['partial']} | {st_sb['absent']} |",
             f"| 四庫本 skqs | {st_sk['aligned']} | {st_sk['fuzzy']} | {st_sk['variant']} | {st_sk['partial']} | {st_sk['absent']} |", "",
             f"## Relocation blocks confirmed by both witnesses ({len(confirmed)}) / 兩個見證本都證實的移段", "",
             "Base text order differs from both 明成化本 and 四庫本. Registered as X3 displacement hypotheses in "
             "`displacements.jsonl`; the working text follows the witnesses.", "",
             "| X3 | base book | witnesses place it in | entries | base cites modern editor | first entry |",
             "|---|---|---|---|---|---|"]
    for n, b in enumerate(confirmed, 1):
        lines.append(f"| X3-{n:03d} | {names[b['base_book']]} | {names[b['sbck_book']]} | "
                     f"{', '.join('`'+i+'`' for i in b['entries'])} | {'yes' if b['editorial_ref'] else ''} | "
                     f"{by_id[b['entries'][0]]['text'][:24]}… |")
    lines += ["", f"## Unconfirmed order breaks ({sum(len(b['entries']) for b in unconfirmed)}) / 未證實的順序差異", "",
              "Seen in one witness only; usually alignment noise next to a page gap or a heavy variant.", ""]
    lines += [f"- `{i}` {by_id[i]['text'][:30]}…" for b in unconfirmed for i in b["entries"]]
    absent = [i for i, a in al_sb.items() if a["status"] == "absent"]
    var = [i for i, a in al_sb.items() if a["status"] == "variant"]
    lines += ["", f"## Heavy variants vs sbck ({len(var)}) / 與明成化本差異較大的條目", ""]
    lines += [f"- `{i}` (similarity {al_sb[i]['coverage']}) base: {by_id[i]['text'][:30]}… | sbck: "
              f"{sbck[al_sb[i]['book']][al_sb[i]['start']:al_sb[i]['end']][:30]}" for i in var]
    lines += ["", f"## Base entries not found in sbck ({len(absent)}) / 明成化本中找不到的底本條目", ""]
    lines += [f"- `{i}` {by_id[i]['text'][:40]}" for i in absent]
    lines += ["", f"## Witness-only spans in sbck ({len(gaps)}) / 明成化本有、底本沒有的文字", ""]
    lines += [f"- 卷{g['book']:02d} {g['book_name']} @{g['start']}: {g['text'][:50]}" for g in gaps]
    (OUT / "alignment-summary.md").write_text("\n".join(lines) + "\n")
    print(f"sbck {dict(st_sb)} skqs {dict(st_sk)} | X3 blocks={len(confirmed)} unconfirmed={len(unconfirmed)} "
          f"| witness-only spans={len(gaps)}", file=sys.stderr)


if __name__ == "__main__":
    main()
