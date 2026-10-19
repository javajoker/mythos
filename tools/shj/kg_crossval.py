"""Step 4 of the entity-graph method: cross-validate candidates through the relations and choose the most consistent
joint mapping, with confidence scores.

Variables: MTN/LND (31 regions), major WAT (waters), CRE (animals or none), POL (cultures).
Factors (methodology-spec §5):
  flows_into  major→major: candidate mouth is the target +2.0 · same region +0.3 · otherwise −1.0;
              target 'none' while the source's real mouth is in the base −1.0
              major→generic sea: candidate mouth is a sea +0.5 / −0.5 · major→LND (流沙): endorheic/desert +0.5 / −0.3
              minor stream (rises at M, flows into major B): M's region in B's basin +0.6 / −0.3
  rises_at    major→MTN/LND: candidate's source region is the mountain's region +1.0 · adjacent +0.3 · else −0.5
  next        MTN→MTN: same region +0.3 · adjacent +0.1 · else −0.3        (distances are only a reference)
  has_creature MTN→CRE: animal's range covers the region +0.5·cov · else −0.25·cov
  located, sees: bearing between candidate points within 67.5° of the stated direction +0.2 / −0.1 (sees ±0.1/−0.05)
Solver: simulated annealing over whole configurations (CHAINS chains, STEPS steps, temperature T0 → T1, fixed
seeds), maximising the global energy E = Σ own + Σ factors − uniqueness penalty (UNIQ per pair of book rivers on one
real river), then iterated conditional modes, then block moves (one river set to a candidate while its neighbouring
rivers, their source mountains and those mountains' stations are re-fitted; kept only if E rises); the best chain
wins. Single-entity updates alone get stuck when a river system and its mountains must move together. Mapping = the best-energy configuration. Every solution (CHAINS full chains + RESTARTS re-solves each dropping 20% of
the factors, SUB_CHAINS chains each) is a sample; stability = share of samples agreeing with the mapping, and the
most frequent alternatives across samples are reported. Confidence = stability × (1 − e^(−margin)); tiers high ≥ 0.6,
medium ≥ 0.3, low ≥ 0.1, tentative below (best-energy pick, but the samples disagree).

Output: projects/shanhaijing/data/derived/kg/mapping.jsonl (or --out DIR); --set name=value overrides a weight in WT;
--cands PATH reads another candidates file (red-team decoys).
"""
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kg_common import DIR_DEG, KG, angdiff, bearing, jl, load_world  # noqa: E402

RESTARTS, DROP, ITERS = 12, 0.2, 25
NONE_OWN = 0.05
CHAINS, STEPS, SUB_CHAINS, SUB_STEPS, T0, T1 = 6, 1_200_000, 2, 600_000, 2.0, 0.02
# relation weights (methodology-spec §5); `--set name=value` overrides one for a sensitivity run, `--out DIR` writes there
WT = {"flow_hit": 2.0, "flow_near": 0.3, "flow_miss": -1.0, "rise_hit": 1.0, "rise_adj": 0.3, "rise_miss": -0.5,
      "minor_hit": 0.6, "minor_miss": -0.3, "next_same": 0.3, "next_adj": 0.1, "next_miss": -0.3,
      "bearing_scale": 1.0, "creature_scale": 1.0, "uniq": 2.0,
      # reading rules (methodology-spec §5.1): map view of waters (an end, not necessarily the source, lies at the place;
      # a stated course may run either way), orientation 前 = east (front_east=1) or 前 = south (front_east=0),
      # and the spatial clauses of review R1 (濱 beside, 環之 encircles, 其外有 outside)
      "map_view": 1.0, "flow_rev": 1.5, "front_east": 1.0,
      "near_hit": 0.3, "near_adj": 0.1, "near_miss": -0.2}


CANDS = KG / "candidates.jsonl"
INIT = None          # --init MAPPING: diagnostic only — polish that configuration and report its energy, then exit
FIX = None           # --fix JSON {node: candidate}: hold these entities at the given candidates (hypothesis tests)
SCAN = None          # --scan JSON [{"name", "fix"}...]: with --init, polish each fixed configuration in turn (one load)


def parse_args(argv):
    global CANDS, INIT, FIX, SCAN
    out = KG
    i = 0
    while i < len(argv):
        if argv[i] == "--set":
            k, _, v = argv[i + 1].partition("=")
            if k not in WT:
                sys.exit(f"unknown weight {k}; known: {sorted(WT)}")
            WT[k] = float(v)
            i += 2
        elif argv[i] == "--scan":
            SCAN = json.loads(Path(argv[i + 1]).read_text())
            i += 2
        elif argv[i] == "--fix":
            FIX = json.loads(Path(argv[i + 1]).read_text())
            i += 2
        elif argv[i] == "--init":
            INIT = Path(argv[i + 1])
            i += 2
        elif argv[i] == "--cands":
            CANDS = Path(argv[i + 1])
            i += 2
        elif argv[i] == "--out":
            out = Path(argv[i + 1])
            out.mkdir(parents=True, exist_ok=True)
            i += 2
        else:
            sys.exit(f"unknown argument {argv[i]}")
    return out


def main():
    out_dir = parse_args(sys.argv[1:])
    regions, props, animals, waters, cultures = load_world()
    reg = {r["code"]: r for r in regions}
    adj = {r["code"]: sorted(r["adjacent"]) for r in regions}   # sorted: proposals index into it
    wat = {w["id"]: w for w in waters}
    ani = {a["id"]: a for a in animals}
    cul = {c["id"]: c for c in cultures}
    nodes = {n["id"]: n for n in jl(KG / "nodes.jsonl")}
    edges = jl(KG / "edges.jsonl")
    cands = {c["node"]: c for c in jl(CANDS)}

    # ---- variables and own scores ------------------------------------------------------------------------------------
    own = {}
    for nid, c in cands.items():
        if c.get("kind") == "region":
            own[nid] = {f"region:{k}": v for k, v in c["scores"].items()}
            own[nid]["none"] = NONE_OWN          # insufficient evidence: no features and no relational pull
        elif c.get("kind") == "culture":
            own[nid] = {f"culture:{k}": v for k, v in c["scores"].items()}
            own[nid]["none"] = NONE_OWN
        elif c.get("kind") in ("water", "animal"):
            own[nid] = {x["cand"]: x["own"] for x in c["candidates"]}
    if FIX and not INIT:
        for v, c in FIX.items():
            if v in own and c in own[v]:
                own[v] = {c: own[v][c]}      # a fixed entity keeps only its hypothesised candidate
            elif v in own:
                own[v] = {c: 0.0}
    var = set(own)

    def point(cand):
        kind, _, key = cand.partition(":")
        if kind == "region":
            return (reg[key]["lat"], reg[key]["lon"])
        if kind == "culture":
            return tuple(cul[key]["pt"])
        if kind == "water":
            w = wat[key]
            return tuple(w.get("pt") or w.get("mouth_pt"))
        return None

    def nearest_region(pt):
        return min(regions, key=lambda r: (r["lat"] - pt[0]) ** 2 + ((r["lon"] - pt[1]) * math.cos(math.radians(pt[0]))) ** 2)["code"]

    mouth_region = {w["id"]: nearest_region(w["mouth_pt"]) for w in waters if w.get("mouth_pt")}

    def region_of(cand):
        kind, _, key = cand.partition(":")
        if kind == "region":
            return {key}
        if kind == "culture":
            return {cul[key]["region"]}
        if kind == "water":
            w = wat[key]
            return set(w.get("basin") or w.get("regions") or []) | ({mouth_region[key]} if key in mouth_region else set())
        return set()

    def points(cand):
        """Points of a candidate for bearings: a river is a line (source, middle, mouth), a sea or lake a point."""
        kind, _, key = cand.partition(":")
        if kind == "water" and wat[key].get("src") and wat[key].get("mouth_pt"):
            (a, b), (c, d) = wat[key]["src"], wat[key]["mouth_pt"]
            return [(a, b), ((a + c) / 2, (b + d) / 2), (c, d)]
        p = point(cand)
        return [p] if p else []

    def f_near(hit, adj_w, miss):
        """beside / encircles / outside: the two candidates share a region (or are adjacent)."""
        def f(ca, cb):
            if "none" in (ca, cb):
                return 0.0
            A, B = region_of(ca), region_of(cb)
            if A & B:
                return hit
            return adj_w if any(b in adj.get(a, ()) for a in A for b in B) else miss
        return f

    # ---- factors ---------------------------------------------------------------------------------------------------
    factors = []   # (a, b, fn(ca, cb) -> score, label, entry)
    rises = defaultdict(list)
    for x in edges:
        if x["type"] == "rises_at":
            rises[x["src"]].append(x["dst"])

    def f_flow(ca, cb):
        if ca == "none":
            return 0.0                       # a small stream missing from the base may join any river
        if cb == "none":
            # the child is a real river whose mouth is itself in the base: "not in the base" contradicts it
            return WT["flow_miss"] if wat[ca[6:]].get("mouth") in wat else 0.0
        if ca == cb:
            return -2.0                      # a river cannot flow into itself
        wa, wb = wat[ca[6:]], wat[cb[6:]]
        if wa.get("mouth") == wb["id"]:
            return WT["flow_hit"]
        if wb.get("mouth") == wa["id"] and WT["map_view"]:
            return WT["flow_rev"]               # map view: the two connect, the book's direction is not the flow
        mouth = wat.get(wa.get("mouth") or "", {})
        if set(mouth.get("basin") or mouth.get("regions") or []) & set(wb.get("basin") or wb.get("regions") or []):
            return WT["flow_near"]
        return WT["flow_miss"]

    def f_rise(cw, cm):
        if cw == "none" or cm == "none":
            return 0.0
        w = wat[cw[6:]]
        m = cm.partition(":")[2]
        src = w.get("src_region")
        ends = {src, mouth_region.get(w["id"])} if w["type"] == "river" else set(w.get("regions") or [])
        if src == m:
            return WT["rise_hit"]
        if WT["map_view"] and m in ends:
            return WT["rise_hit"] * 0.8          # map view: the other end of the water lies at the place
        near = ends if WT["map_view"] else {src}
        return WT["rise_adj"] if any(e in adj.get(m, ()) for e in near if e) else WT["rise_miss"]

    def f_minor(cm, cb):
        if cb == "none" or cm == "none":
            return 0.0
        basin = set(wat[cb[6:]].get("basin") or wat[cb[6:]].get("regions") or [])
        return WT["minor_hit"] if cm.partition(":")[2] in basin else WT["minor_miss"]

    def f_next(ca, cb):
        if ca == "none" or cb == "none":
            return 0.0
        a, b = ca.partition(":")[2], cb.partition(":")[2]
        return WT["next_same"] if a == b else WT["next_adj"] if b in adj.get(a, ()) else WT["next_miss"]

    def f_creature(cm, ca):
        if ca == "none" or cm == "none":
            return 0.0
        a = ani[ca[7:]]
        if not any(not r.startswith("S_") for r in a["regions"]):
            return 0.0                      # sea-only animal: a mountain's land region says nothing about it
        cov = max(own_animal.get(ca, 0.0), 0.0)
        return WT["creature_scale"] * (0.5 if cm.partition(":")[2] in a["regions"] else -0.25) * max(cov, 0.3)

    def make_bearing(direction, w_ok, w_bad):
        def f(ca, cb):   # "A is <direction> of B": bearing from B to A
            if "none" in (ca, cb):
                return 0.0
            pa, pbs = point(ca), points(cb)
            if not pa or not pbs:
                return 0.0
            pb = min(pbs, key=lambda q: (q[0] - pa[0]) ** 2 + (q[1] - pa[1]) ** 2)   # nearest part of a river line
            if pa == pb:
                return 0.0
            return w_ok if angdiff(bearing(pb, pa), DIR_DEG[direction]) <= 67.5 else w_bad
        return f

    own_animal = {}
    for x in edges:
        a, b, t = x["src"], x["dst"], x["type"]
        if t == "flows_into" and a in var and b in var:
            factors.append((a, b, f_flow, "flows_into", x["entry"]))
        elif t == "flows_into" and a in var and nodes.get(b, {}).get("symbol") == "海":
            factors.append((a, None, lambda ca, _: 0.0 if ca == "none" else
                            (0.5 if wat.get(wat[ca[6:]].get("mouth") or "", {}).get("type") == "sea" else -0.5),
                            "flows_into(sea)", x["entry"]))
        elif t == "flows_into" and a in var and nodes.get(b, {}).get("type") == "LND":
            factors.append((a, None, lambda ca, _: 0.0 if ca == "none" else
                            (0.5 if wat[ca[6:]].get("endorheic") or wat[ca[6:]].get("ends_in_desert") else -0.3),
                            "flows_into(land)", x["entry"]))
        elif t == "flows_into" and a not in var and b in var and nodes.get(b, {}).get("type") == "WAT":
            for m in rises.get(a, []):
                if m in var:
                    factors.append((m, b, f_minor, "minor stream", x["entry"]))
        elif t == "sinks_at" and a in var:
            factors.append((a, None, lambda ca, _: 0.0 if ca == "none" else
                            (0.3 if wat[ca[6:]].get("endorheic") or wat[ca[6:]].get("ends_in_desert") else -0.2),
                            "sinks_at", x["entry"]))
        elif t == "rises_at" and a in var and b in var:
            factors.append((a, b, f_rise, "rises_at", x["entry"]))
        elif t == "next" and a in var and b in var:
            factors.append((a, b, f_next, "next", x["entry"]))
        elif t == "has_creature" and a in var and b in var:
            factors.append((a, b, f_creature, "has_creature", x["entry"]))
        elif t in ("located", "sees") and a in var and b in var and x["attrs"].get("direction") in DIR_DEG:
            w_ok, w_bad = (0.2, -0.1) if t == "located" else (0.1, -0.05)
            w_ok, w_bad = w_ok * WT["bearing_scale"], w_bad * WT["bearing_scale"]
            d = x["attrs"]["direction"]
            if x["attrs"].get("alt_direction") and not WT["front_east"]:
                d = x["attrs"]["alt_direction"]          # 前／後 under the other convention (前 = south)
            factors.append((a, b, make_bearing(d, w_ok, w_bad), t, x["entry"]))
        elif t in ("beside", "encircles", "outside") and a in var and b in var:
            k = 0.67 if t == "outside" else 1.0
            factors.append((a, b, f_near(WT["near_hit"] * k, WT["near_adj"], WT["near_miss"] * k), t, x["entry"]))
    for nid, sc in own.items():
        if cands[nid].get("kind") == "animal":
            own_animal.update({k: v for k, v in sc.items() if k.startswith("animal:")})
    by_var = defaultdict(list)
    for i, (a, b, fn, lab, ent) in enumerate(factors):
        by_var[a].append(i)
        if b:
            by_var[b].append(i)

    river_vars = {v for v in var if cands[v].get("kind") == "water"}
    UNIQ = WT["uniq"]

    def local(v, c, assign, active, counts=None):
        s = own[v][c]
        if counts is not None and v in river_vars and c != "none":
            s -= UNIQ * (counts[c] - (1 if assign[v] == c else 0))   # soft uniqueness: one real river per book river
        for i in by_var[v]:
            if i not in active:
                continue
            a, b, fn, _, _ = factors[i]
            if b is None:
                s += fn(c, None)
            elif a == v:
                s += fn(c, assign[b])
            else:
                s += fn(assign[a], c)
        return s

    def energy(assign, active):
        e = sum(own[v][assign[v]] for v in var)
        cnt = Counter(assign[v] for v in river_vars if assign[v] != "none")
        e -= UNIQ * sum(k * (k - 1) / 2 for k in cnt.values())
        for i in active:
            a, b, fn, _, _ = factors[i]
            e += fn(assign[a], None) if b is None else fn(assign[a], assign[b])
        return e

    def icm(assign, active, order_seed):
        order = sorted(var)
        random.Random(order_seed).shuffle(order)
        counts = Counter(assign[v] for v in river_vars)
        for _ in range(ITERS):
            changed = 0
            for v in order:
                cur_s = local(v, assign[v], assign, active, counts)
                best = max(sorted(own[v]), key=lambda c: round(local(v, c, assign, active, counts), 6))
                if best != assign[v] and local(v, best, assign, active, counts) > cur_s + 1e-9:
                    if v in river_vars:
                        counts[assign[v]] -= 1
                        counts[best] += 1
                    assign[v] = best
                    changed += 1
            if not changed:
                break
        return assign

    var_list = sorted(var)
    cand_list = {v: sorted(own[v]) for v in var_list}
    # relation-guided proposals: real-world candidates that would satisfy a relation given the neighbour's state
    tribs_of = defaultdict(list)
    for w in waters:
        if w.get("mouth"):
            tribs_of[w["mouth"]].append("water:" + w["id"])
    rising_in = defaultdict(list)
    for w in waters:
        if w.get("src_region"):
            rising_in[w["src_region"]].append("water:" + w["id"])
    nbr = defaultdict(list)          # v -> [(neighbour, relation, v_is_src)]
    for a, b, fn, lab, _ in factors:
        if b:
            nbr[a].append((b, lab, True))
            nbr[b].append((a, lab, False))

    def guided(v, assign, rng):
        opts = []
        for o, lab, v_src in nbr[v]:
            co = assign.get(o, "none")
            if lab == "flows_into" and co.startswith("water:"):
                if v_src:
                    opts += tribs_of.get(co[6:], [])                # v flows into o: v is a tributary of o's river
                else:
                    m = wat[co[6:]].get("mouth")                    # o flows into v: v is o's mouth
                    if m:
                        opts.append("water:" + m)
            elif lab == "rises_at" and co.startswith("region:") and v_src:
                opts += rising_in.get(co[7:], [])
            elif lab in ("rises_at", "next", "minor stream", "has_creature") and not v_src or lab == "next":
                if co.startswith("water:"):
                    opts += ["region:" + r for r in (wat[co[6:]].get("basin") or [])]
                elif co.startswith("region:"):
                    opts += [co] + ["region:" + r for r in adj.get(co[7:], ())]
        opts = [c for c in opts if c in own[v]]
        return opts[rng.randrange(len(opts))] if opts else None

    def anneal(active, seed, steps):
        rng = random.Random(seed)
        assign = {v: max(sorted(own[v]), key=lambda c: (own[v][c], c == "none")) for v in var_list}
        counts = Counter(assign[v] for v in river_vars)
        e = energy(assign, active)
        best, best_e = dict(assign), e
        for k in range(steps):
            T = T0 * (T1 / T0) ** (k / steps)
            v = var_list[rng.randrange(len(var_list))]
            cl = cand_list[v]
            if len(cl) < 2:
                continue
            c = (guided(v, assign, rng) if rng.random() < 0.5 else None) or cl[rng.randrange(len(cl))]
            cur = assign[v]
            if c == cur:
                continue
            d = local(v, c, assign, active, counts) - local(v, cur, assign, active, counts)
            if d >= 0 or rng.random() < math.exp(d / T):
                if v in river_vars:
                    counts[cur] -= 1
                    counts[c] += 1
                assign[v] = c
                e += d
                if e > best_e + 1e-9:
                    best, best_e = dict(assign), e
        best = icm(best, active, seed)
        best = block_moves(best, active, rng)
        return best, energy(best, active)

    river_nbrs = {v: sorted({o for o, lab, _ in nbr[v] if o in river_vars}) for v in river_vars}
    # the mountains the block's rivers rise at, and their neighbouring stations, move with the block
    rise_nbrs = {v: sorted({o for o, lab, _ in nbr[v] if lab == "rises_at" and o not in river_vars}) for v in river_vars}
    station_nbrs = {m: sorted({o for o, lab, _ in nbr[m] if lab == "next"}) for v in river_vars for m in rise_nbrs[v]}

    def block_of(v):
        rivers = [v] + river_nbrs[v]
        mtns = sorted({m for r in rivers for m in rise_nbrs[r]})
        mtns += sorted({s for m in mtns for s in station_nbrs.get(m, [])} - set(mtns))
        return rivers, mtns

    def shortlist(v, assign):
        """Candidates worth trying for v: what its neighbours' current states suggest, its best own scores, none."""
        opts = set()
        for o, lab, v_src in nbr[v]:
            co = assign.get(o, "none")
            if lab == "flows_into" and co.startswith("water:"):
                if v_src:
                    opts.update(tribs_of.get(co[6:], []))
                elif wat[co[6:]].get("mouth"):
                    opts.add("water:" + wat[co[6:]]["mouth"])
            elif lab == "rises_at" and co.startswith("region:"):
                opts.update(rising_in.get(co[7:], []))
        opts.update(sorted(own[v], key=lambda c: -own[v][c])[:5])
        opts.add("none")
        return sorted(c for c in opts if c in own[v])

    def block_terms(vs, assign, active):
        """Own scores and factors touching the variables vs (each factor once); uniqueness is handled separately."""
        e = sum(own[v][assign[v]] for v in vs)
        for i in {i for v in vs for i in by_var[v] if i in active}:
            a, b, fn, _, _ = factors[i]
            e += fn(assign[a], None) if b is None else fn(assign[a], assign[b])
        return e

    def uniq_delta(undo, assign, counts):
        """Change of −UNIQ·Σ k(k−1)/2 caused by moving the block from its undo state to the current state."""
        rv = [u for u in undo if u in river_vars]            # uniqueness applies to rivers only
        labels = {undo[u] for u in rv} | {assign[u] for u in rv}
        labels.discard("none")
        d = 0.0
        for c in labels:
            after = counts[c]
            before = after - sum(1 for u in rv if assign[u] == c) + sum(1 for u in rv if undo[u] == c)
            d -= UNIQ * (after * (after - 1) - before * (before - 1)) / 2
        return d

    def block_moves(assign, active, rng, passes=2):
        """Large-neighbourhood search: set one river to a candidate, re-fit its neighbouring rivers greedily, keep the
        block change only if the exact energy rises. Single-variable moves cannot make these coordinated changes."""
        counts = Counter(assign[v] for v in river_vars)
        order = sorted(river_vars)
        for _ in range(passes):
            rng.shuffle(order)
            gained = 0
            for v in order:
                rivers, mtns = block_of(v)
                block = rivers + mtns
                for c in shortlist(v, assign):
                    if c == assign[v]:
                        continue
                    undo = {u: assign[u] for u in block}
                    before = block_terms(block, assign, active)
                    set_label(v, c, assign, counts)
                    for _sweep in range(2):
                        for u in block[1:]:
                            opts = shortlist(u, assign) if u in river_vars else cand_list[u]
                            cur = local(u, assign[u], assign, active, counts)
                            bu = max(opts, key=lambda k: (round(local(u, k, assign, active, counts), 6), k))
                            if bu != assign[u] and local(u, bu, assign, active, counts) > cur + 1e-9:
                                set_label(u, bu, assign, counts)
                    gain = block_terms(block, assign, active) - before + uniq_delta(undo, assign, counts)
                    if gain > 1e-9:
                        gained += 1
                    else:
                        for u, k in undo.items():
                            set_label(u, k, assign, counts)
            if not gained:
                break
        return assign

    def set_label(u, k, assign, counts):
        if assign[u] != k:
            if u in river_vars:
                counts[assign[u]] -= 1
                counts[k] += 1
            assign[u] = k

    chain_log = []

    samples = []

    def solve(active, seed, chains, steps, log=False):
        results = [anneal(active, seed * 10 + k, steps) for k in range(chains)]
        samples.extend(r[0] for r in results)
        if log:
            chain_log.extend(round(r[1], 1) for r in results)
        return max(results, key=lambda r: r[1])

    all_f = set(range(len(factors)))
    if INIT:
        # Diagnostic and hypothesis tests: start from a given mapping, hold the --fix (or each --scan) configuration,
        # re-fit everything else with ICM and block moves, and report the energy and the relations the fixed
        # entities break. The chains are not run and kg/mapping.jsonl is not written.
        prev = {m["node"]: m.get("cand") for m in jl(INIT)}
        start = {v: (prev.get(v) if prev.get(v) in own[v] else max(sorted(own[v]), key=lambda c: own[v][c]))
                 for v in var_list}

        def polish(fix):
            saved = {}
            for v, c in fix.items():
                if v in own:
                    saved[v] = own[v]
                    own[v] = {c: saved[v].get(c, 0.0)}
            assign = dict(start)
            assign.update({v: c for v, c in fix.items() if v in own})
            e0 = energy(assign, all_f)
            assign = block_moves(icm(assign, all_f, 7), all_f, random.Random(7))
            e1 = energy(assign, all_f)
            broken = []
            for (a, b, fn, lab, ent) in factors:
                if a in fix or b in fix:
                    val = fn(assign[a], None) if b is None else fn(assign[a], assign[b])
                    if val < 0:
                        broken.append({"relation": lab, "a": a, "b": b, "a_cand": assign[a], "b_cand": assign.get(b),
                                       "entry": ent, "score": round(val, 3)})
            for v, o in saved.items():
                own[v] = o
            return e0, e1, assign, broken

        key_nodes = ("WAT:河", "WAT:赤", "WAT:黑", "WAT:弱", "WAT:西海", "MTN:昆侖之丘")
        if SCAN:
            with (out_dir / "scan.jsonl").open("w") as f:
                for cfg in SCAN:
                    e0, e1, assign, broken = polish(cfg["fix"])
                    f.write(json.dumps({"name": cfg["name"], "energy": round(e1, 2), "n_fixed": len(cfg["fix"]),
                                        "violated": len(broken), "violated_score": round(sum(x["score"] for x in broken), 2),
                                        "violated_top": sorted(broken, key=lambda x: x["score"])[:12],
                                        "key": {k: assign.get(k) for k in key_nodes}}, ensure_ascii=False) + "\n")
                    f.flush()
            return
        e0, e1, assign, broken = polish(FIX or {})
        print(f"init energy {e0:.1f}; after polish {e1:.1f}", file=sys.stderr)
        if out_dir != KG:
            (out_dir / "result.json").write_text(json.dumps(
                {"energy_init": round(e0, 2), "energy": round(e1, 2), "fixed": FIX or {}, "violated": broken,
                 "key": {k: assign.get(k) for k in key_nodes}, "weights": WT}, ensure_ascii=False, indent=1))
        return
    best_single, final_e = solve(all_f, 7, CHAINS, STEPS, log=True)
    for r in range(RESTARTS):
        rng = random.Random(1000 + r)
        active = {i for i in all_f if rng.random() >= DROP}
        solve(active, 1000 + r, SUB_CHAINS, SUB_STEPS)
    # the mapping is the best-energy configuration (internally consistent); per-entity majority votes were tried and
    # rejected because the winners do not fit together (much lower joint energy). Samples measure agreement.
    final = best_single
    runs = samples

    def system(cand):
        """Top-level river system of a water candidate (follow mouths to the river that reaches a sea or lake)."""
        if not cand or not cand.startswith("water:"):
            return cand
        w = wat[cand[6:]]
        seen = set()
        while w["type"] == "river" and w.get("mouth") in wat and wat[w["mouth"]]["type"] == "river" and w["id"] not in seen:
            seen.add(w["id"])
            w = wat[w["mouth"]]
        return "system:" + w["id"]

    out = []
    for nid in sorted(nodes):
        n, c = nodes[nid], cands.get(nid, {})
        rec = {"node": nid, "type": n["type"], "symbol": n["symbol"]}
        if nid in var:
            ch = final[nid]
            fcounts = Counter(final[v] for v in river_vars)
            tot = {k: local(nid, k, final, all_f, fcounts) for k in own[nid]}
            ranked = sorted(tot.items(), key=lambda kv: (-kv[1], kv[0]))
            margin = ranked[0][1] - ranked[1][1] if len(ranked) > 1 else ranked[0][1]
            stab = sum(1 for r in runs if r[nid] == ch) / len(runs)
            conf = round(stab * (1 - math.exp(-max(margin, 0))), 3)
            sup, vio = [], []
            for i in by_var[nid]:
                a, b, fn, lab, ent = factors[i]
                sc = fn(final[a], final[b] if b else None) if b is None or a in final else 0
                other = b if a == nid else a
                (sup if sc > 0 else vio if sc < 0 else []).append(
                    {"relation": lab, "with": other, "entry": ent, "score": round(sc, 2)})
            sys_ch = system(ch)
            sys_stab = sum(1 for r in runs if system(r[nid]) == sys_ch) / len(runs)
            freq = Counter(r[nid] for r in runs)
            rec.update({"cand": ch, "confidence": conf, "system": sys_ch, "system_stability": round(sys_stab, 2),
                        "sample_alternatives": [{"cand": k, "share": round(v / len(runs), 2)}
                                                for k, v in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
                                                if k != ch][:3],
                        "tier": ("high" if conf >= 0.6 else "medium" if conf >= 0.3 else "low" if conf >= 0.1
                                 else "tentative"),
                        "margin": round(margin, 3), "stability": round(stab, 2), "own": own[nid][ch],
                        "alternatives": [{"cand": k, "total": round(v, 3)} for k, v in ranked[1:4]],
                        "supported_by": sorted(sup, key=lambda d: -d["score"])[:6],
                        "violated": sorted(vio, key=lambda d: d["score"])[:6],
                        "status": ("unmapped:insufficient" if cands[nid].get("kind") in ("region", "culture")
                                   else "unmapped:none") if ch == "none" else "mapped"})
        else:
            rec.update({"cand": None, "status": c.get("status", "unmapped:no-candidate"), "gloss": c.get("gloss")})
        out.append(rec)
    with (out_dir / "mapping.jsonl").open("w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    st = Counter(r["status"] for r in out)
    tiers = Counter(r.get("tier") for r in out if r["status"] == "mapped")
    (out_dir / "crossval-log.json").write_text(json.dumps({"factors": len(factors), "variables": len(var),
                                                      "best_energy": round(final_e, 1), "chain_energies": chain_log,
                                                      "consensus_energy": round(energy(final, all_f), 1),
                                                      "samples": len(samples),
                                                      "restarts": RESTARTS, "drop": DROP, "weights": WT}, indent=1))
    print(f"factors {len(factors)}; energy {final_e:.1f}; chains {chain_log}; status {dict(st)}; tiers {dict(tiers)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
