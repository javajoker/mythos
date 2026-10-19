"""Step 3 of the entity-graph method: real-world candidates for every entity, with own scores.

  MTN, LND  -> 31 world regions, scored from the entity's resources, plants, terrain (region-properties.jsonl)
  WAT major -> type-compatible rivers / lakes / seas worldwide (waters.jsonl), scored on flow direction, size,
               destination type; minor streams get no candidates of their own (they act through relations)
  CRE       -> real animals by rarity-weighted description coverage, plus 'none' (mythical / composite)
  POL       -> 47 ancient cultures by customs and livelihood
  PLA, MIN  -> lexical meaning of the common noun (translation, not name matching); proper names: none
  PER, UNK, DOC -> not mapped (non-geographic or undetermined), kept for completeness

Names never score. Output: projects/shanhaijing/data/derived/kg/candidates.jsonl (or --out PATH).
Red-team option: --mask-known K caps every region at K known property values.
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kg_common import (DIR_DEG, KG, LEXICAL, angdiff, animal_match, animal_weights, jl, load_world,  # noqa: E402
                       region_prop_score)

NONE_ANIMAL_OWN = 0.35   # a description explained by no real animal better than this is treated as unmatched


def is_major(n, course):
    """Mapped individually: seas, lakes, waters receiving ≥ 2 inflows, waters mentioned ≥ 3 times, and any water with
    a stated course (both a source and a destination), e.g. the 海內東經 waterway list."""
    p = n["props"]
    return (p.get("subtype") in ("sea", "lake") or p.get("n_inflows", 0) >= 2 or len(n["mentions"]) >= 3
            or n["id"] in course)


def water_candidates(n, waters):
    p = n["props"]
    sub = p.get("subtype", "river")
    want = {"river": ("river",), "lake": ("lake", "desert"), "sea": ("sea",)}[sub]
    out = []
    for w in waters:
        if w["type"] not in want:
            continue
        s, why = 0.0, []
        if sub == "river":
            if p.get("flow_dir") and w.get("flow_dir"):
                d = angdiff(DIR_DEG[p["flow_dir"]], DIR_DEG[w["flow_dir"]])
                s += 0.4 if d == 0 else 0.2 if d <= 45 else 0 if d <= 90 else -0.3
                why.append(f"flow {p['flow_dir']}/{w['flow_dir']}")
            # size: the number of inflows the book lists reflects how densely it surveyed a basin, not river length,
            # so this term is kept small
            k, L = p.get("n_inflows", 0), w.get("length_km", 0)
            s += (0.15 if L >= 800 else -0.1) if k >= 10 else 0.0
            dt = p.get("dest_type")
            real_mouth_type = None
            if w.get("mouth"):
                real_mouth_type = next((x["type"] for x in waters if x["id"] == w["mouth"]), None)
            if dt and real_mouth_type:
                if dt in ("lake", "desert"):
                    s += 0.4 if (w.get("endorheic") or w.get("ends_in_desert")) else -0.2
                elif dt == "sea":
                    s += 0.3 if real_mouth_type == "sea" else -0.2
                elif dt == "river":
                    s += 0.3 if real_mouth_type == "river" else -0.1
                why.append(f"dest {dt}/{real_mouth_type}")
        out.append({"cand": f"water:{w['id']}", "own": round(s, 3), "why": why})
    out.sort(key=lambda c: (-c["own"], c["cand"]))
    # 'none' (not in the base) costs more for bigger book waters: the base holds the world's major rivers, lakes, seas
    none_own = -min(0.1 * p.get("n_inflows", 0), 1.5) if sub == "river" else -0.2
    return out + [{"cand": "none", "own": round(none_own, 3), "why": ["not in the base"]}]


def mask_known(props, cap, seed=11):
    """Red-team decoy (T-R01): cap every region at `cap` known property values (T or F); the excess, chosen with a
    fixed seed, becomes unknown. Tests whether a region wins only because it is described in more detail."""
    import random
    rng = random.Random(seed)
    known = {}
    for k in sorted(props):
        for c in props[k]["true"] + props[k]["false"]:
            known.setdefault(c, []).append(k)
    drop = set()
    for c, ks in sorted(known.items()):
        if len(ks) > cap:
            drop |= {(c, k) for k in rng.sample(ks, len(ks) - cap)}
    return {k: dict(p, true=[c for c in p["true"] if (c, k) not in drop], false=[c for c in p["false"] if (c, k) not in drop])
            for k, p in props.items()}


def main():
    regions, props, animals, waters, cultures = load_world()
    out_path = KG / "candidates.jsonl"
    if "--mask-known" in sys.argv:
        props = mask_known(props, int(sys.argv[sys.argv.index("--mask-known") + 1]))
    if "--out" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--out") + 1])
    codes = [r["code"] for r in regions]
    nodes = jl(KG / "nodes.jsonl")
    edges = jl(KG / "edges.jsonl")
    by_id = {n["id"]: n for n in nodes}
    w_anim = animal_weights(animals)
    resources = {}
    for x in edges:
        if x["type"] == "has_resource" and x["dst"] in by_id:
            key = by_id[x["dst"]]["props"].get("prop")
            if key in props:
                resources.setdefault(x["src"], set()).add(key)
    df = Counter(t for c in cultures for t in set(c["tags"]))
    nc = len(cultures)

    has_src = {x["src"] for x in edges if x["type"] == "rises_at"}
    has_dst = {x["src"] for x in edges if x["type"] == "flows_into"}
    course = has_src & has_dst
    out = []
    for n in nodes:
        t, rec = n["type"], {"node": n["id"], "type": n["type"]}
        if t in ("MTN", "LND"):
            tags = {g for g in n["tags"] if g in props} | resources.get(n["id"], set())
            if n["props"].get("barren"):
                tags.add("barren")
            scores = {c: round(sum(region_prop_score(c, props[g]) for g in tags), 3) for c in codes}
            rec.update({"kind": "region", "features": sorted(tags), "scores": scores})
        elif t == "WAT":
            if n["symbol"] == "海":
                rec.update({"kind": "generic-sea", "status": "unmapped:generic"})
            elif is_major(n, course):
                rec.update({"kind": "water", "candidates": water_candidates(n, waters)})
            else:
                rec.update({"kind": "water-minor", "status": "via-relations"})
        elif t == "CRE":
            if n["tags"]:
                ms = animal_match(n["tags"], n["props"].get("kind", ""), animals, w_anim)[:6]
                cands = [{"cand": f"animal:{a['id']}", "own": c, "why": ov} for c, ov, a in ms if c > 0]
            else:
                cands = []
            cands.append({"cand": "none", "own": NONE_ANIMAL_OWN, "why": ["no real animal explains the description"]})
            rec.update({"kind": "animal", "features": n["tags"], "candidates": sorted(cands, key=lambda c: -c["own"])})
        elif t == "POL":
            tags = [g for g in n["tags"]]
            scores = {}
            for c in cultures:
                s = 0.0
                for g in tags:
                    if g not in df:
                        continue
                    w = math.log10(nc / df[g]) + 0.05
                    s += w if g in c["tags"] else w * (2 * df[g] / nc - 1)
                scores[c["id"]] = round(s, 3)
            rec.update({"kind": "culture", "features": tags, "scores": scores})
        elif t in ("PLA", "MIN"):
            gloss = LEXICAL.get(n["symbol"])
            rec.update({"kind": "lexical", "status": "mapped:lexical" if gloss else "unmapped:no-candidate",
                        "gloss": gloss, "prop": n["props"].get("prop")})
        elif t == "PER":
            rec.update({"kind": "none", "status": "unmapped:non-geographic"})
        else:
            rec.update({"kind": "none", "status": "unmapped:undetermined" if t == "UNK" else "unmapped:structural"})
        out.append(rec)
    with out_path.open("w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(Counter(r.get("kind") for r in out), file=sys.stderr)


if __name__ == "__main__":
    main()
