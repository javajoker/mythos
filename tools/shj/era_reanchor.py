"""Re-anchor the Western, Eastern and Central Mountain Classics with one absolute li length (task T-V04g).

Rules (initiator, 2026-10-20; framework P12): distances are absolute straight-line distances in one unknown unit shared
by the whole book; every section is placed independently (its start is free); sections are linked only by relative
position (the book's direction from the Central Plains) and by the waters they share.

Model, for one li length s (km per li):
- A section's stations sit at start + s * (x, y) (route from the legs, era_frame.py), east-west converted to longitude at
  each station's own latitude (latitude calibration, era-world.md §5c).
- Constraints from the text only (entry IDs in stations.jsonl and TEXT_REL below):
  * a station's water flows <dir> into a shared water W  -> the course chosen for W lies in that direction (±67.5°);
  * a shared water W rises at a station                  -> the station is near the source of W's course, and the
    course leaves the source in the stated direction;
  * W flows into another shared water X, or into 海     -> W's course ends on X's course, or at a sea;
  * a station's water flows <dir> into 海               -> a sea coast or large lake lies in that direction;
  * TEXT_REL: other places where the text puts a station on or beside a shared water.
- Shared waters (named in two or more of these sections): 河 渭 洛 伊 漢 沔 江 涇 赤水. Each takes one course from the
  pool (data/era/courses.jsonl, every region alike) for the whole book; a section may read it as a different water
  (homonym) at cost H. Two names on one course cost U. A colour-named water (赤水) on a course without that colour
  costs C (name semantics as a feature).
- Relative position: a Western section's centroid lies west of the origin (±67.5°), an Eastern one east; a Central
  section within R_C of the origin.
- Search: for each s on a grid, every section's start is searched on a world grid and refined; the global course
  assignment is improved by coordinate descent; J(s) is the total cost. The solved s is the minimum of J.

Outputs (projects/shanhaijing/data/derived/era/): reanchor.json (curve, assignment, anchors with rivals),
reanchor.md (report), reanchor-map.svg. Run: python3 -I tools/shj/era_reanchor.py [--hold 河=nile] [--h 3] [--out tag]
"""
import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DER = ROOT / "projects/shanhaijing/data/derived"
ERA = DER / "era"
BASE = ROOT / "projects/shanhaijing/data/era"
ORIGIN = (34.7, 113.6)
BOOKS = ("西山經", "東山經", "中山經")
SHARED = ("河", "渭", "洛", "伊", "漢", "沔", "江", "涇", "赤水")
NORM = {"河水": "河", "渭水": "渭", "洛水": "洛", "伊水": "伊", "漢水": "漢", "江水": "江", "大江": "江", "涇水": "涇"}
COLOUR = {"赤水": "red"}
DIRS = {"北": 0, "東北": 1, "東": 2, "東南": 3, "南": 4, "西南": 5, "西": 6, "西北": 7}
# other places where the text puts a station on or beside a shared water: (section, seq, water, kind, dir, quote);
# the quote is checked against the station's entry
TEXT_REL = [("西次三經", 1, "河", "beside", "北", "在河之南"),
            ("西次三經", 13, "河", "on", None, "其下有石門，河水冒以西流"),
            ("東山經之首", 12, "江", "on", None, "錞于江"),
            ("中次四經", 9, "洛", "on", None, "此二山者，洛閒也"),
            ("中次六經", 1, "洛", "view", "南", "南望伊洛"),
            ("中次六經", 1, "伊", "view", "南", "南望伊洛")]
# tolerance (free km, scale km) by constraint kind; cost = min(CAP, ((d - free) / scale)^2)
TOL = {"trib": (60, 60), "rise": (100, 100), "on": (40, 60), "beside": (60, 60), "view": (80, 80), "sea": (80, 80)}
CAP = 4.0
CELL = 4                       # cells per degree (0.25°)
RADIUS = 260                   # km kept in the distance fields
INF = float("inf")


def jl(p):
    return [json.loads(l) for l in Path(p).open() if l.strip()]


def nlon(lon):
    return (lon + 180.0) % 360.0 - 180.0


def dlon(a, b):
    return (a - b + 180.0) % 360.0 - 180.0


def flat(p, q):
    """km offsets (east, north) from p to q, equirectangular at the mean latitude (map view)."""
    dy = (q[0] - p[0]) * 110.57
    dx = dlon(q[1], p[1]) * 111.32 * math.cos(math.radians((p[0] + q[0]) / 2))
    return dx, dy


def angdiff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


def densify(pts, step):
    out = [tuple(pts[0])]
    for a, b in zip(pts, pts[1:]):
        dx, dy = flat(a, b)
        n = max(1, int(math.hypot(dx, dy) // step))
        for i in range(1, n + 1):
            t = i / n
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + dlon(b[1], a[1]) * t))
    return out


def cell_of(lat, lon):
    return (math.floor(lat * CELL), math.floor(nlon(lon) * CELL))


def fill(field, pts, radius, key=None, directional=True):
    """For every cell within radius of the points: nearest distance overall and in each of 8 directions (±67.5°)."""
    rl = radius / 110.57
    for p in pts:
        i0, i1 = math.floor((p[0] - rl) * CELL), math.floor((p[0] + rl) * CELL)
        for i in range(i0, i1 + 1):
            clat = (i + 0.5) / CELL
            cosl = max(0.05, math.cos(math.radians(clat)))
            ro = radius / (111.32 * cosl)
            for j in range(math.floor((p[1] - ro) * CELL), math.floor((p[1] + ro) * CELL) + 1):
                clon = (j + 0.5) / CELL
                dx, dy = flat((clat, clon), p)
                d = math.hypot(dx, dy)
                if d > radius:
                    continue
                c = (i, ((j + 180 * CELL) % (360 * CELL)) - 180 * CELL)
                if key is None:
                    arr = field.get(c)
                    if arr is None:
                        arr = field[c] = [INF] * 9
                else:
                    sub = field.get(c)
                    if sub is None:
                        sub = field[c] = {}
                    arr = sub.get(key)
                    if arr is None:
                        arr = sub[key] = [INF] * 9 if directional else [INF]
                if not directional:
                    if d < arr[0]:
                        arr[0] = d
                    continue
                if d < arr[8]:
                    arr[8] = d
                b = math.degrees(math.atan2(dx, dy)) % 360.0 if d > 1e-6 else None
                for k in range(8):
                    if (b is None or angdiff(b, k * 45.0) <= 67.5) and d < arr[k]:
                        arr[k] = d


def cost(d, kind):
    free, scale = TOL[kind]
    if d <= free:
        return 0.0
    return min(CAP, ((d - free) / scale) ** 2)


class World:
    def __init__(self):
        self.courses = {c["id"]: c for c in jl(BASE / "courses.jsonl")}
        self.pool = [c["id"] for c in self.courses.values() if c["kind"] in ("river", "sea")]
        self.FR, self.FS, self.FSEA = {}, {}, {}
        for cid in self.pool:
            c = self.courses[cid]
            fill(self.FR, densify(c["pts"], 15), RADIUS, key=cid)
            fill(self.FS, [tuple(c["pts"][0])], 400, key=cid, directional=False)
        coast = json.loads((BASE / "coastlines-present.json").read_text())
        sea_pts = []
        for poly in list(coast["land"].values()) + list(coast["water"].values()):
            if max(p[0] for p in poly) < -5:
                continue
            sea_pts += densify(poly, 25)
        for c in self.courses.values():
            if c["kind"] in ("lake", "coast"):
                sea_pts += densify(c["pts"], 20)
        fill(self.FSEA, sea_pts, RADIUS)
        # initial bearing of each course (first 150 km), whether it reaches a sea, and which courses it ends on
        self.init_b, self.to_sea, self.ends_on = {}, {}, defaultdict(set)
        for cid in self.pool:
            c = self.courses[cid]
            d = densify(c["pts"], 15)
            k = min(len(d) - 1, 10)
            dx, dy = flat(d[0], d[k])
            self.init_b[cid] = math.degrees(math.atan2(dx, dy)) % 360.0
            self.to_sea[cid] = c["to"] == "sea"
            mouth = tuple(c["pts"][-1])
            for oid in self.pool:
                if oid == cid:
                    continue
                if c["to"] == oid or min(math.hypot(*flat(mouth, q)) for q in densify(self.courses[oid]["pts"], 15)) <= 60:
                    self.ends_on[cid].add(oid)


def load_sections():
    frame = defaultdict(list)
    for f in jl(ERA / "frame.jsonl"):
        frame[f["section"]].append(f)
    st = {(s["section"], s["seq"]): s for s in jl(DER / "stations.jsonl")}
    text = {e["id"]: e["text"] for e in jl(ROOT / "reference/shanhaijing/data/entries.jsonl")}
    secs = []
    for sec, fs in frame.items():
        book = st[(sec, fs[0]["seq"])]["book"]
        if book not in BOOKS:
            continue
        fs.sort(key=lambda f: f["seq"])
        idx = {f["seq"]: i for i, f in enumerate(fs)}
        cons, rels, waters = [], [], set()
        for f in fs:
            s = st[(sec, f["seq"])]
            for r in s.get("rivers", []):
                w, to = NORM.get(r["river"], r["river"]), NORM.get(r.get("to") or "", r.get("to") or "")
                d = DIRS.get(r.get("flow"))
                if w in SHARED and w != to:
                    cons.append((idx[f["seq"]], "rise", w, d, s["entry_id"]))
                    waters.add(w)
                    if to in SHARED:
                        rels.append((w, to, s["entry_id"]))
                        waters.add(to)
                    elif to == "海":
                        rels.append((w, "海", s["entry_id"]))
                elif to in SHARED and d is not None:
                    cons.append((idx[f["seq"]], "trib", to, d, s["entry_id"]))
                    waters.add(to)
                elif to == "海" and d is not None:
                    cons.append((idx[f["seq"]], "sea", None, d, s["entry_id"]))
        for (sc, seq, w, kind, dr, q) in TEXT_REL:
            if sc == sec:
                eid = st[(sec, seq)]["entry_id"]
                assert q in text[eid], (sec, seq, q)
                cons.append((idx[seq], kind, w, DIRS[dr] if dr else 8, eid))
                waters.add(w)
        secs.append({"section": sec, "book": book, "pts": [(f["x_li"], f["y_li"]) for f in fs],
                     "names": [f["station"] for f in fs], "cons": cons, "rels": rels, "waters": sorted(waters)})
    return secs


class Solver:
    def __init__(self, world, secs, H=3.0, U=3.0, C=1.0, RC=800.0, hold=None):
        self.w, self.secs, self.H, self.U, self.C, self.RC = world, secs, H, U, C, RC
        self.hold = hold or {}
        self.memo = {}

    def prior(self, sec, cen):
        dx, dy = flat(ORIGIN, cen)
        if sec["book"] == "中山經":
            d = math.hypot(dx, dy)
            return min(6.0, (max(0.0, d - self.RC) / (self.RC / 2)) ** 2)
        want = 270.0 if sec["book"] == "西山經" else 90.0
        ex = max(0.0, angdiff(math.degrees(math.atan2(dx, dy)) % 360.0, want) - 67.5)
        return min(6.0, (ex / 22.5) ** 2)

    def place(self, sec, s, start):
        out = []
        for x, y in sec["pts"]:
            lat = start[0] + y * s / 110.57
            out.append((lat, start[1] + x * s / (111.32 * max(0.05, math.cos(math.radians(lat))))))
        return out

    def evaluate(self, sec, s, start, g, detail=False):
        if not detail:
            key = (sec["section"], s, start, self.H, tuple(g.get(wn) for wn in sec["waters"]))
            hit = self.memo.get(key)
            if hit is None:
                hit = self.memo[key] = self._evaluate(sec, s, start, g)
            return hit
        return self._evaluate(sec, s, start, g, detail=True)

    def _evaluate(self, sec, s, start, g, detail=False):
        w = self.w
        pos = self.place(sec, s, start)
        cells = [cell_of(*p) for p in pos]
        total = 0.0
        sea_items = []
        per_w = defaultdict(lambda: [0.0, defaultdict(float), []])      # base, delta by course, constraint list
        for (i, kind, wn, d, eid) in sec["cons"]:
            if kind == "sea":
                arr = w.FSEA.get(cells[i])
                dist = arr[d] if arr else INF
                c = cost(dist, "sea")
                total += c
                sea_items.append((i, eid, round(dist) if dist < INF else None, round(c, 2)))
                continue
            e = per_w[wn]
            e[0] += CAP
            e[2].append((i, kind, d, eid))
            if kind == "rise":
                sub = w.FS.get(cells[i])
                if sub:
                    for cid, arr in sub.items():
                        e[1][cid] += cost(arr[0], "rise") - CAP
                        if d is not None and angdiff(w.init_b[cid], d * 45.0) > 67.5:
                            e[1][cid] += 1.0
            else:
                sub = w.FR.get(cells[i])
                if sub:
                    di = d if d is not None else 8
                    for cid, arr in sub.items():
                        e[1][cid] += cost(arr[di], kind) - CAP
        for wn in sec["waters"]:
            per_w[wn]
        # candidate courses per water
        cand = {}
        for wn, (base, delta, _) in per_w.items():
            gw = g.get(wn)
            opts = {}
            for cid in sorted(set(delta) | ({gw} if gw else set())):
                v = base + delta.get(cid, 0.0)
                if COLOUR.get(wn) and w.courses[cid].get("colour") != COLOUR[wn]:
                    v += self.C
                if cid != gw:
                    v += self.H
                opts[cid] = v
            opts[None] = base + self.H        # a water that is none of the listed courses
            cand[wn] = sorted(opts.items(), key=lambda t: (t[1], t[0] or "~"))
        # relations may need courses chosen for their partner
        for (a, b, _e) in sec["rels"]:
            if b == "海":
                cand[a] = sorted(((cid, v + (0 if cid and w.to_sea[cid] else 2.0)) for cid, v in cand[a]),
                                 key=lambda t: (t[1], t[0] or "~"))
        k = 3 if len(cand) <= 3 else 2
        tops = {wn: list(v[:k]) for wn, v in cand.items()}
        for (a, b, _e) in sec["rels"]:
            if b == "海":
                continue
            have_b = {cid for cid, _ in tops[b]}
            for cid, _ in tops[a][:2]:
                for oid in (sorted(w.ends_on[cid]) if cid else ()):
                    if oid not in have_b:
                        v = per_w[b][0] + per_w[b][1].get(oid, 0.0) + (self.H if oid != g.get(b) else 0.0)
                        tops[b].append((oid, v))
                        have_b.add(oid)
        names = list(tops)
        best, best_choice = INF, {}

        def rec(i, acc, choice, used):
            nonlocal best, best_choice
            if acc >= best:
                return
            if i == len(names):
                pen = 0.0
                for (a, b, _e) in sec["rels"]:
                    if b != "海" and (choice[a] is None or choice[b] not in w.ends_on[choice[a]]):
                        pen += 2.0
                if acc + pen < best:
                    best, best_choice = acc + pen, dict(choice)
                return
            wn = names[i]
            for cid, v in tops[wn]:
                u = self.U if cid is not None and cid in used else 0.0
                choice[wn] = cid
                rec(i + 1, acc + v + u, choice, used | {cid} if cid else used)
            choice.pop(wn, None)

        rec(0, 0.0, {}, frozenset())
        if not names:
            best = 0.0
        cen = (sum(p[0] for p in pos) / len(pos), sum(p[1] for p in pos) / len(pos))
        pr = self.prior(sec, cen)
        total += best + pr
        if not detail:
            return total, best_choice
        items = []
        for wn, (_b, _d, lst) in per_w.items():
            cid = best_choice.get(wn)
            for (i, kind, d, eid) in lst:
                if kind == "rise":
                    sub = w.FS.get(cells[i]) or {}
                    dist = sub.get(cid, [INF])[0]
                else:
                    sub = w.FR.get(cells[i]) or {}
                    dist = sub.get(cid, [INF] * 9)[d if d is not None else 8]
                items.append({"station": sec["names"][i], "entry": eid, "water": wn, "kind": kind,
                              "course": cid, "km": round(dist) if dist < INF else None, "cost": round(cost(dist, kind), 2)})
        for (i, eid, dist, c) in sea_items:
            items.append({"station": sec["names"][i], "entry": eid, "water": "海", "kind": "sea", "course": "coast",
                          "km": dist, "cost": c})
        return total, best_choice, {"centroid": [round(cen[0], 2), round(nlon(cen[1]), 2)], "prior": round(pr, 2),
                                    "items": items, "route": [[round(a, 3), round(nlon(b), 3)] for a, b in pos]}

    def seeds(self, sec):
        step = 1.0 if sec["book"] == "中山經" else 1.5
        if sec["book"] == "西山經":
            box = (-2, 60, -25, 118)
        elif sec["book"] == "東山經":
            box = (8, 66, 105, 300)
        else:
            box = (12, 58, 55, 150)
        la = box[0]
        while la <= box[1]:
            lo = box[2]
            while lo <= box[3]:
                yield (la, lo)
                lo += step
            la += step

    def refine(self, sec, s, start, g):
        cur = start
        val, ch = self.evaluate(sec, s, cur, g)
        step = 0.75
        while step >= 0.05:
            moved = True
            while moved:
                moved = False
                for dla, dlo in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                    nxt = (cur[0] + dla * step, cur[1] + dlo * step)
                    v, c = self.evaluate(sec, s, nxt, g)
                    if v < val - 1e-9:
                        cur, val, ch, moved = nxt, v, c, True
            step /= 2
        return val, cur, ch

    def solve_section(self, sec, s, g, keep=6):
        scored = []
        for st in self.seeds(sec):
            v, _ = self.evaluate(sec, s, st, g)
            scored.append((v, st))
        scored.sort()
        minima = []
        for v, st in scored[:40]:
            val, cur, ch = self.refine(sec, s, st, g)
            cen = self.place(sec, s, cur)
            cen = (sum(p[0] for p in cen) / len(cen), sum(p[1] for p in cen) / len(cen))
            if any(math.hypot(*flat(cen, m["cen"])) < 400 for m in minima):
                for m in minima:
                    if math.hypot(*flat(cen, m["cen"])) < 400 and val < m["cost"]:
                        m.update(cost=val, start=cur, choice=ch, cen=cen)
                continue
            minima.append({"cost": val, "start": cur, "choice": ch, "cen": cen})
            if len(minima) >= keep * 2:
                break
        minima.sort(key=lambda m: m["cost"])
        return minima[:keep]

    def global_cost(self, g):
        vals = [c for c in g.values() if c]
        return self.U * (len(vals) - len(set(vals)))

    def descend(self, s, g, starts):
        """Local search on the assignment with placements held: single moves over the whole pool, then pair moves for
        two waters that meet in one section (their best few courses each)."""
        g = dict(g)
        movable = [wn for wn in SHARED if wn not in self.hold and any(wn in sec["waters"] for sec in self.secs)]

        def total(gg, wns):
            secs_w = [sec for sec in self.secs if any(w in sec["waters"] for w in wns)]
            return self.global_cost(gg) + sum(min(self.evaluate(sec, s, st, gg)[0] for st in starts[sec["section"]])
                                              for sec in secs_w)
        improved = True
        while improved:
            improved = False
            ranked = {}
            for wn in movable:
                vals = sorted((total(dict(g, **{wn: cid}), [wn]), cid) for cid in self.w.pool)
                ranked[wn] = [cid for _, cid in vals[:6]]
                if vals[0][1] != g.get(wn) and vals[0][0] < total(g, [wn]) - 1e-9:
                    g[wn], improved = vals[0][1], True
            if improved:
                continue
            for i, a in enumerate(movable):
                for b in movable[i + 1:]:
                    if not any(a in sec["waters"] and b in sec["waters"] for sec in self.secs):
                        continue
                    cur = total(g, [a, b])
                    best = (cur, g.get(a), g.get(b))
                    for ca in ranked[a]:
                        for cb in ranked[b]:
                            v = total(dict(g, **{a: ca, b: cb}), [a, b])
                            if v < best[0] - 1e-9:
                                best = (v, ca, cb)
                    if (best[1], best[2]) != (g.get(a), g.get(b)):
                        g[a], g[b], improved = best[1], best[2], True
        return g

    def candidate_starts(self, s):
        """Placements to hold while the assignment is searched: each section with no coupling, and each section with
        one of its waters pinned to each of that water's best courses (so that every plausible course has a placement
        that suits it)."""
        H, self.H = self.H, 0.0
        starts = {sec["section"]: [m["start"] for m in self.solve_section(sec, s, {}, keep=6)] for sec in self.secs}
        self.H = H
        ranked = {}
        for wn in SHARED:
            secs_w = [sec for sec in self.secs if wn in sec["waters"]]
            if not secs_w:
                continue
            vals = []
            for cid in self.w.pool:
                gg = {wn: cid}
                vals.append((sum(min(self.evaluate(sec, s, st, gg)[0] for st in starts[sec["section"]]) for sec in secs_w), cid))
            ranked[wn] = [cid for _, cid in sorted(vals)[:8]]
        H, self.H = self.H, 10.0
        for sec in self.secs:
            for wn in sec["waters"]:
                for cid in ranked[wn] + ([self.hold[wn]] if wn in self.hold else []):
                    starts[sec["section"]] += [m["start"] for m in self.solve_section(sec, s, {wn: cid}, keep=2)]
        self.H = H
        return starts

    def solve_s(self, s, g0, rounds=3, starts=None):
        """Alternate: search the assignment with candidate placements held, then place every section under it."""
        g = dict(g0)
        g.update(self.hold)
        starts = {k: list(v) for k, v in (starts or self.candidate_starts(s)).items()}
        res = {}
        for _ in range(rounds):
            g = self.descend(s, g, starts)
            res = {sec["section"]: self.solve_section(sec, s, g) for sec in self.secs}
            for k, ms in res.items():
                starts[k] += [m["start"] for m in ms]
            if self.descend(s, g, starts) == g:
                break
        J = sum(ms[0]["cost"] for ms in res.values()) + self.global_cost(g)
        return J, g, res


def free_assignment(solver, s):
    """Start of the descent: each water's course chosen with no book-wide coupling (H = 0)."""
    H = solver.H
    solver.H = 0.0
    votes = defaultdict(lambda: defaultdict(float))
    for sec in solver.secs:
        ms = solver.solve_section(sec, s, {}, keep=1)
        for wn, cid in ms[0]["choice"].items():
            votes[wn][cid] += 1
    solver.H = H
    return {wn: max(v.items(), key=lambda t: t[1])[0] for wn, v in votes.items()}


BOOK_COL = {"西山經": "#b5542d", "東山經": "#2d6cb5", "中山經": "#2d8a4a"}


def interval(curve, J, d):
    ok = [c["s"] for c in curve if c["J"] <= J + d]
    return (min(ok), max(ok)) if ok else (None, None)


def report():
    main_ = json.loads((ERA / "reanchor.json").read_text())
    holds = [json.loads(p.read_text()) for p in sorted(ERA.glob("reanchor-hold_*.json"))]
    sens = [json.loads(p.read_text()) for p in sorted(ERA.glob("reanchor-sens_*.json"))]
    courses = {c["id"]: c for c in jl(BASE / "courses.jsonl")}
    old = {a["section"]: next(c for c in a["candidates"] if c["cand"] == a["lead"]) for a in jl(ERA / "anchors.jsonl")}
    s, J, g = main_["s_km_per_li"], main_["J"], main_["assignment"]
    i2, i5 = interval(main_["curve"], J, 2), interval(main_["curve"], J, 5)
    L = ["# 重新錨定：全書一個絕對里長 / Re-anchoring with one absolute li length (T-V04g)", "",
         "> `tools/shj/era_reanchor.py`。里數是絕對直線距離，全書共用一個未知的里長；每一篇的起點獨立；篇與篇之間只靠"
         "**相對位置**（各經相對中原的方向）與**共有的水**聯繫（項目發起人，2026-10-20）。",
         "> Li are absolute straight-line distances in one unknown unit; each section's start is free; sections are linked "
         "only by relative position and shared waters.", "",
         "## 方法 / Method", "",
         "- 每篇的路線由各段方位與里數得出（`frame.jsonl`），以里長 s 放大；東西向依各站自己的緯度換成經度（緯度校準）。",
         "- 約束只取原文：某山之水「X 流注于 W」→ W 在該方向（±67.5°）；W「出焉」→ 該山近 W 的源頭，且 W 離源的方向相符；"
         "W 注于另一共有水或海 → 兩條水道相接或入海；某山之水注于海 → 該方向有海岸或大湖；另有原文明言的「在河之南」「河水冒以西流」"
         "「錞于江」「洛閒」「南望伊洛」。",
         "- 共有的水（在兩篇以上出現）：河、渭、洛、伊、漢、沔、江、涇、赤水。每個名稱全書取同一條水道（`data/era/courses.jsonl`，"
         "42 條河與 2 個長水體，各地區一視同仁）；某篇讀作另一條同名水（同名異水）代價 H = 3；兩個名稱用同一條水道代價 3；"
         "赤水用不紅的水道代價 1（名稱語義作特徵）。",
         "- 相對位置：西山經各篇的重心在原點以西（±67.5°），東山經在以東，中山經在原點 800 公里以內（超出部分漸增代價）。",
         "- 搜索：每個里長在全球格點上搜各篇起點並細化，水道指派以座標下降求解（兩個起點取優）；總代價 J 最小的里長即解。",
         "- 沒有用任何大模型的地點判斷：唯一的人工輸入是水道的近似走向（地圖資料）與上列原文關係。仍屬**暫定**：水道庫由我選定，"
         "其中有與書中名稱同名的今日河流，求解只看幾何，但選庫本身可能帶入先入之見（見下「限制」）。", "",
         "## 解出的里長 / The solved li length", "",
         f"**s = {s} 公里／里**（J = {J}）。J 在最小值 +2 以內的範圍：{i2[0]}–{i2[1]}；+5 以內：{i5[0]}–{i5[1]}。",
         f"Solved **{s} km per li**; within +2 of the minimum: {i2[0]}–{i2[1]} km; within +5: {i5[0]}–{i5[1]} km.", "",
         "| 里長（公里）| J | 西山經 | 東山經 | 中山經 |", "|---|---|---|---|---|"]
    for c in main_["curve"]:
        bb = c.get("by_book", {})
        mark = " **←**" if c["s"] == s else ""
        L.append(f"| {c['s']}{mark} | {c['J']} | {bb.get('西山經', '')} | {bb.get('東山經', '')} | {bb.get('中山經', '')} |")
    L += ["", "各篇自己偏好的里長（在全書的水道指派下，只看這一篇的代價；多個值表示平手）/ Each section's own best li length:", "",
          "| 篇 | 約束數 | 狀態 | 自身最佳里長 | 代價曲線（里長: 代價）|", "|---|---|---|---|---|"]
    for o in main_["sections"]:
        own = o["own_best_s"]
        own_txt = "任何（無約束）" if o["status"] == "unanchored" else (f"{own[0]}–{own[-1]}" if len(own) > 1 else str(own[0]))
        L.append(f"| {o['section']} | {o['n_constraints']} | {o['status']} | {own_txt} | "
                 + "、".join(f"{x}:{c}" for x, c in o["own_curve"]) + " |")
    L += ["", "## 全書的水道指派 / Book-wide course of each shared water", "",
          "| 水 | 水道 | 用到的篇（同名異水者另列）|", "|---|---|---|"]
    for wn in SHARED:
        cid = g.get(wn)
        uses, homs = [], []
        for o in main_["sections"]:
            if wn in o["waters"] and o["placements"]:
                ch = o["placements"][0]["choice"].get(wn)
                (uses if ch == cid else homs).append(o["section"] + ("" if ch == cid else f"→{courses[ch]['name'] if ch else '表外的水'}"))
        L.append(f"| {wn} | {courses[cid]['name'] if cid else '—'} | {'、'.join(uses)}" + (f"；同名異水：{'、'.join(homs)}" if homs else "") + " |")
    L += ["", "## 各篇新錨點與對立位置 / New anchors with rivals", "",
          f"以 s = {s} 公里／里。起點 = 第一站；重心 = 各站平均；代價越低越好；「未命中」列出代價 > 0.5 的約束。",
          "", "| 經 | 篇 | 狀態 | 新錨點：起點 → 終點（重心）| 代價 | 對立 1（代價差）| 對立 2（代價差）| 舊錨點（T-V04，作廢）|",
          "|---|---|---|---|---|---|---|---|"]

    def fmt(p):
        return f"{p[0]:.1f}°N {p[1]:.1f}°E"

    for o in main_["sections"]:
        P = o["placements"]
        oldc = old.get(o["section"])
        oldt = f"{oldc['label']}（{fmt(oldc['start'])}）" if oldc else "—"
        if o["status"] == "unanchored" or not P:
            L.append(f"| {o['book']} | {o['section']} | 無水的約束 | 只能定方向（{'以西' if o['book'] == '西山經' else '以東' if o['book'] == '東山經' else '中原附近'}），無法錨定 | — | — | — | {oldt} |")
            continue
        b = P[0]
        rv = [f"{fmt(p['centroid'])}（+{round(p['cost'] - b['cost'], 2)}）" for p in P[1:3]]
        rv += ["—"] * (2 - len(rv))
        L.append(f"| {o['book']} | {o['section']} | {o['status']} | {fmt(b['route'][0])} → {fmt(b['route'][-1])}（{fmt(b['centroid'])}）| "
                 f"{b['cost']} | {rv[0]} | {rv[1]} | {oldt} |")
    for o in main_["sections"]:
        P = o["placements"]
        if o["status"] == "unanchored" or not P:
            continue
        L += ["", f"### {o['book']}・{o['section']}", ""]
        for k, p in enumerate(P[:3]):
            tag = "新錨點 / anchor" if k == 0 else f"對立 {k} / rival {k}"
            used = "、".join(f"{wn}={courses[c]['name'] if c else '表外'}" + ("（同名異水）" if wn in p["homonyms"] else "")
                            for wn, c in sorted(p["choice"].items()))
            L.append(f"- **{tag}**：起點 {fmt(p['start'])}，重心 {fmt(p['centroid'])}，代價 {p['cost']}（方向 {p['prior']}）；水道：{used or '—'}")
            if k == 0:
                miss = [it for it in p["items"] if it["cost"] > 0.5]
                for it in miss:
                    L.append(f"  - 未命中 / miss：{it['station']}（`{it['entry']}`）{it['water']} {it['kind']}，"
                             f"{'距離 ' + str(it['km']) + ' 公里' if it['km'] is not None else '附近沒有'}，代價 {it['cost']}")
    if holds:
        L += ["", "## 對立讀法：把某水固定在另一條水道上重解 / Held rival readings", "",
              "每一行固定指定的水道，其餘（里長、起點、其他水道、同名異水）重新求解；ΔJ 為比最佳解多出的代價。",
              "", "| 固定 / held | 解出里長 | J | ΔJ | 西山經 | 東山經 | 中山經 | 西山經各篇重心 |", "|---|---|---|---|---|---|---|---|"]
        for h in sorted(holds, key=lambda h: h["J"]):
            bb = next(c for c in h["curve"] if c["s"] == h["s_km_per_li"]).get("by_book", {})
            wc = "；".join(f"{o['section']} {fmt(o['placements'][0]['centroid'])}" for o in h["sections"]
                          if o["book"] == "西山經" and o["placements"])
            hold_txt = "、".join(f"{k}={courses[v]['name']}" for k, v in h["hold"].items())
            L.append(f"| {hold_txt} | {h['s_km_per_li']} | {h['J']} | +{round(h['J'] - J, 2)} | {bb.get('西山經', '')} | "
                     f"{bb.get('東山經', '')} | {bb.get('中山經', '')} | {wc} |")
    if sens:
        L += ["", "## 敏感度 / Sensitivity", "", "| 參數 | 解出里長 | J | +2 範圍 | 水道指派的變化 |", "|---|---|---|---|---|"]
        for h in sens:
            lo, hi = interval(h["curve"], h["J"], 2)
            diff = {k: v for k, v in h["assignment"].items() if v != g.get(k)}
            L.append(f"| H={h['H']}、R_C={h['RC']} | {h['s_km_per_li']} | {h['J']} | {lo}–{hi} | "
                     + ("、".join(f"{k}→{courses[v]['name'] if v else '—'}" for k, v in diff.items()) or "無") + " |")
    L += ["", "## 限制 / Limitations", "",
          "- 東次二經、東次三經、中次十經、中次十二經沒有任何水的約束（沒有注入共有水或海的水），只能定方向，**不能錨定**；"
          "東次四經只有兩條「注于海」，任何朝東北的海岸都合，屬弱錨定。",
          "- 里長的上限比下限清楚：大於約 0.25 公里／里時，中山經與西山經的支流無法同時落在共有的水旁；小於此值時各篇縮小，"
          "約束仍大多可以滿足，所以下限較鬆。",
          "- 水道庫的平衡：中國 15 條、中亞 5、南亞 5、西亞 13、非洲 3、長水體 2；中原附近列了較多小支流（伊、涇、北洛等），"
          "西方也列了相當的支流（喀布爾、大扎卜、迪亞拉、哈布爾、阿特巴拉、白尼羅等），但仍需紅隊檢查。",
          "- 水道庫裡有與書中名稱同名的今日河流；求解只用幾何，不用名稱，但選庫時可能帶入先入之見。待 T-V04c 以遮蔽輸入、"
          "由不知名稱的模型重新提出水道候選後重跑。",
          "- 共有的水只靠名稱相同來聯繫；「同名異水」的代價 H 是一般規則，對全書一視同仁，結果對 H 的敏感度見上表。", ""]
    (ERA / "reanchor.md").write_text("\n".join(L) + "\n")
    # ---- map ------------------------------------------------------------------------------------------------------
    coast = json.loads((BASE / "coastlines-present.json").read_text())
    W, Hh = 1400, 1360

    def panel(lat0, lat1, lon0, lon1, x0, y0, w):
        k = w / (lon1 - lon0)
        return (lambda la, lo: (x0 + (lo - lon0) * k, y0 + (lat0 - la) * k)), (lat0 - lat1) * k

    def path(f, pts, close=False):
        return "M" + " L".join(f"{f(a, b)[0]:.1f},{f(a, b)[1]:.1f}" for a, b in pts) + (" Z" if close else "")

    S = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" font-family="sans-serif" font-size="11">',
         f'<rect width="{W}" height="{Hh}" fill="#fbfaf6"/>',
         f'<text x="12" y="24" font-size="17" font-weight="bold">重新錨定（T-V04g）：全書一個里長 s = {s} 公里／里 / Re-anchored sections</text>',
         '<text x="12" y="44" fill="#555">實線：各篇新錨點的路線；虛線：對立 1；藍線：全書指派的共有水道；★ 中原原點。沒有水的約束的篇不畫。'
         '暫定結果；海岸為今日簡化輪廓。</text>']
    hold_west = [h for h in holds if "河" in h["hold"]]
    for (lat0, lat1, lon0, lon1, x0, y0, w, title) in [(52, 0, 20, 140, 12, 60, 1376, "歐亞與非洲 / wide view"),
                                                          (42, 26, 98, 124, 12, 690, 900, "東亞 / East Asia")]:
        f, h = panel(lat0, lat1, lon0, lon1, x0, y0, w)
        S.append(f'<svg x="{x0}" y="{y0}" width="{w}" height="{h:.0f}" viewBox="{x0} {y0} {w} {h:.0f}">'
                 f'<rect x="{x0}" y="{y0}" width="{w}" height="{h:.0f}" fill="#dce8f1"/>')
        S.append('<g fill="#f3efe4" stroke="#a89f88" stroke-width="0.6">' + "".join(f'<path d="{path(f, v, True)}"/>' for v in coast["land"].values()) + "</g>")
        S.append('<g fill="#dce8f1" stroke="#a89f88" stroke-width="0.4">' + "".join(f'<path d="{path(f, v, True)}"/>' for v in coast["water"].values()) + "</g>")
        S.append('<g fill="none" stroke="#9db7cc" stroke-width="0.8">' + "".join(
            f'<path d="{path(f, c["pts"])}"><title>{c["name"]}</title></path>' for c in courses.values() if c["kind"] == "river") + "</g>")
        for wn, cid in g.items():
            if cid:
                S.append(f'<path d="{path(f, courses[cid]["pts"])}" fill="none" stroke="#1f5fa8" stroke-width="2"><title>{wn} = {courses[cid]["name"]}</title></path>')
                if title.startswith("東亞"):
                    x, y = f(*courses[cid]["pts"][len(courses[cid]["pts"]) // 2])
                    S.append(f'<text x="{x + 3:.1f}" y="{y - 3:.1f}" font-size="12" fill="#1f5fa8" font-weight="bold">{wn}</text>')
        if title.startswith("歐亞"):
            for hh in hold_west:
                for o in hh["sections"]:
                    if o["book"] == "西山經" and o["placements"]:
                        S.append(f'<path d="{path(f, o["placements"][0]["route"])}" fill="none" stroke="#7a4cb5" stroke-width="1.2" '
                                 f'stroke-dasharray="2 2" opacity="0.8"><title>{o["section"]}（固定 河={hh["hold"]["河"]}）</title></path>')
        for o in main_["sections"]:
            if o["status"] == "unanchored" or not o["placements"]:
                continue
            col = BOOK_COL[o["book"]]
            P = o["placements"]
            if len(P) > 1:
                S.append(f'<path d="{path(f, P[1]["route"])}" fill="none" stroke="{col}" stroke-width="1" stroke-dasharray="5 3" opacity="0.6">'
                         f'<title>{o["section"]} 對立 1（+{round(P[1]["cost"] - P[0]["cost"], 2)}）</title></path>')
            S.append(f'<path d="{path(f, P[0]["route"])}" fill="none" stroke="{col}" stroke-width="2.4"><title>{o["section"]}（{P[0]["cost"]}）</title></path>')
            sx, sy = f(*P[0]["route"][0])
            ex, ey = f(*P[0]["route"][-1])
            S.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.8" fill="{col}"/>')
            if title.startswith("東亞"):
                S.append(f'<text x="{ex + 3:.1f}" y="{ey + 11:.1f}" font-size="10.5" fill="{col}">{o["section"]}</text>')
        ox, oy = f(*ORIGIN)
        S.append(f'<text x="{ox - 6:.1f}" y="{oy + 5:.1f}" font-size="15" fill="#d4a017">★</text>')
        S.append(f'<text x="{x0 + 6}" y="{y0 + 16}" font-size="12" font-weight="bold">{title}</text></svg>')
    lx, ly = 940, 710
    S.append(f'<g font-size="11"><rect x="{lx}" y="{ly}" width="14" height="4" fill="#b5542d"/><text x="{lx + 20}" y="{ly + 6}">西山經 West</text>'
             f'<rect x="{lx}" y="{ly + 20}" width="14" height="4" fill="#2d6cb5"/><text x="{lx + 20}" y="{ly + 26}">東山經 East</text>'
             f'<rect x="{lx}" y="{ly + 40}" width="14" height="4" fill="#2d8a4a"/><text x="{lx + 20}" y="{ly + 46}">中山經 Central</text>'
             f'<rect x="{lx}" y="{ly + 60}" width="14" height="3" fill="#1f5fa8"/><text x="{lx + 20}" y="{ly + 66}">共有水的指派 shared waters</text>'
             f'<line x1="{lx}" y1="{ly + 82}" x2="{lx + 14}" y2="{ly + 82}" stroke="#555" stroke-dasharray="5 3"/><text x="{lx + 20}" y="{ly + 86}">對立 1 rival 1</text>'
             f'<line x1="{lx}" y1="{ly + 102}" x2="{lx + 14}" y2="{ly + 102}" stroke="#7a4cb5" stroke-dasharray="2 2"/><text x="{lx + 20}" y="{ly + 106}">固定「河」為遠方大河時的西山經（寬圖）</text>'
             f'<text x="{lx}" y="{ly + 130}" fill="#555">s = {s} 公里／里；+2 範圍 {i2[0]}–{i2[1]}</text>'
             f'<text x="{lx}" y="{ly + 148}" fill="#555">無水約束而不畫：東次二、東次三、中次十、中次十二</text></g>')
    S.append("</svg>")
    (ERA / "reanchor-map.svg").write_text("\n".join(S))
    print("wrote reanchor.md, reanchor-map.svg", file=sys.stderr)


def by_book(secs, res):
    out = defaultdict(float)
    for sec in secs:
        out[sec["book"]] += res[sec["section"]][0]["cost"]
    return {k: round(v, 2) for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hold", action="append", default=[], help="hold a water on a course, e.g. 河=nile")
    ap.add_argument("--h", type=float, default=3.0, help="homonym cost")
    ap.add_argument("--rc", type=float, default=800.0, help="Central radius (km)")
    ap.add_argument("--grid", default="0.08:0.60:0.04")
    ap.add_argument("--out", default="", help="tag: write reanchor-<tag>.json only (no report)")
    ap.add_argument("--report", action="store_true", help="only write reanchor.md and the map from the saved runs")
    a = ap.parse_args()
    if a.report:
        report()
        return
    hold = dict(h.split("=") for h in a.hold)
    world = World()
    secs = load_sections()
    solver = Solver(world, secs, H=a.h, RC=a.rc, hold=hold)
    lo, hi, st = (float(x) for x in a.grid.split(":"))
    grid = [round(lo + i * st, 4) for i in range(int(round((hi - lo) / st)) + 1)]
    curve, best = [], None
    g = free_assignment(solver, grid[len(grid) // 2])
    for s in grid:
        inits = [g, free_assignment(solver, s)] + ([best[2]] if best else [])
        starts = solver.candidate_starts(s)
        runs, seen = [], []
        for gi in inits:
            if gi not in seen:
                seen.append(gi)
                runs.append(solver.solve_s(s, gi, starts=starts))
        J, g_s, res = min(runs, key=lambda r: r[0])
        g = g_s
        curve.append({"s": s, "J": round(J, 2), "g": g_s, "by_book": by_book(secs, res)})
        print(f"s={s:.3f} J={J:.2f} {g_s}", file=sys.stderr, flush=True)
        if best is None or J < best[0]:
            best = (J, s, g_s, res)
    # refine around the best grid point
    for s in [round(best[1] + d, 4) for d in (-st * 2 / 3, -st / 3, st / 3, st * 2 / 3)]:
        if s <= 0.02:
            continue
        J, g_s, res = solver.solve_s(s, best[2])
        curve.append({"s": s, "J": round(J, 2), "g": g_s, "by_book": by_book(secs, res)})
        print(f"s={s:.3f} J={J:.2f} (refine)", file=sys.stderr, flush=True)
        if J < best[0]:
            best = (J, s, g_s, res)
    curve.sort(key=lambda c: c["s"])
    J, s, g, res = best
    out = {"s_km_per_li": s, "J": round(J, 2), "assignment": g, "hold": hold, "H": a.h, "RC": a.rc, "curve": curve,
           "sections": []}
    for sec in secs:
        ms = res[sec["section"]]
        rows = []
        for m in ms[:4]:
            v, ch, det = solver.evaluate(sec, s, m["start"], g, detail=True)
            rows.append({"cost": round(v, 2), "start": [round(m["start"][0], 2), round(nlon(m["start"][1]), 2)],
                         "choice": ch, "homonyms": sorted(wn for wn, cid in ch.items() if cid != g.get(wn)), **det})
        kinds = {c[1] for c in sec["cons"]}
        status = "unanchored" if not kinds else ("weak (coast only)" if kinds == {"sea"} else "anchored")
        out["sections"].append({"section": sec["section"], "book": sec["book"], "waters": sec["waters"],
                                "n_constraints": len(sec["cons"]), "status": status, "placements": rows})
    # each section's own preferred li length under the solved assignment
    for o, sec in zip(out["sections"], secs):
        prof = []
        for x in sorted(set(grid) | {s}):
            ms = solver.solve_section(sec, x, g, keep=1)
            prof.append((x, round(ms[0]["cost"], 2)))
        o["own_curve"] = prof
        lo_c = min(c for _, c in prof)
        o["own_best_s"] = [x for x, c in prof if c <= lo_c + 1e-9]
    name = f"reanchor-{a.out}.json" if a.out else "reanchor.json"
    (ERA / name).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(f"solved s = {s} km/li, J = {J:.2f}; wrote {name}", file=sys.stderr)
    if not a.out:
        report()


if __name__ == "__main__":
    main()
