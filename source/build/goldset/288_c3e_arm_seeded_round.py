#!/usr/bin/env python3
"""288 — C.3.e: Arm S and Arm B seeded snowball, staged. TICK-077.

Round 1 DID snowball both arms — but from seeds chosen the same way that failed for the
composite cell: by standing in the literature rather than by estimand. 283 showed what that
cost (112 term-only hits against 2 provenance-only), and round 2 fixed it for composite only.
This does the same repair for Arm S and Arm B.

Three stages, in order, because seeding before you know your seeds is the original error:

  STAGE 1 — find estimand-matched studies by TERM, per arm: arm exposure x fertility outcome,
    pulled in full, scored for identification vocabulary. This is the channel that could see
    past round 1's anchors.
  STAGE 2 — subtract the round 1 and round 2 pools. What is left is what provenance missed,
    and its SIZE is the measurement of the arms' blind spot, comparable to composite's.
  STAGE 3 — snowball from the new estimand-matched seeds, and report redundancy against the
    earlier pools. A round that only re-finds what rounds 1-2 had is REDUNDANT, not productive.

Seeds are capped per arm and chosen by citation among the identified-and-new, so the seed set
is reproducible from this file rather than from a judgement call made once.

Usage: python3 288_c3e_arm_seeded_round.py
"""
import importlib.util, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"
OUT = LOGS / "credit-constraints-arm-seeded-round.json"
SEEDS_PER_ARM = 8
FORWARD_CAP = 200


def load(n, p):
    spec = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[n] = m
    spec.loader.exec_module(m)
    return m


m283 = load("m283", GOLD / "283_c3e_boundary_hunt.py")
m277 = load("m277", GOLD / "277_c3e_snowball.py")
get, shape, fold, SELECT = m283.get, m283.shape, m277.fold, m283.SELECT
NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter", "other"}


def pull(filter_str, label):
    recs, cursor = {}, "*"
    while cursor:
        d, err = get([("filter", filter_str), ("per-page", "200"), ("cursor", cursor),
                      ("select", SELECT)])
        if err:
            print(f"  {label} FAILED: {err}", file=sys.stderr)
            break
        for w in d["results"]:
            recs[w["id"].rsplit("/", 1)[-1]] = shape(w)
        cursor = d["meta"].get("next_cursor")
        if not d["results"]:
            break
    print(f"  {label}: {len(recs)} records")
    return recs


def main():
    rep = json.loads((LOGS / "credit-constraints-query-repair.json").read_text())
    OUTCOME, EXPO = rep["final"]["outcome_axis"], rep["final"]["exposure_axes"]
    blk, phr = m283.blk, m283.phr

    prior = {r["openalex"] for r in
             json.loads((LOGS / "credit-constraints-snowball-pool.json").read_text())}
    prior |= {r["openalex"] for r in
              json.loads((LOGS / "credit-constraints-snowball-round2.json").read_text())["records"]}
    print(f"prior pools (rounds 1+2): {len(prior)} records\n")

    # ---- stage 1 + 2 -------------------------------------------------------
    print("STAGE 1 — term channel, per arm")
    stage = {}
    seeds = []
    for arm in ("S", "B"):
        recs = pull(f"title_and_abstract.search:{blk(EXPO[arm])} AND {blk(OUTCOME)}",
                    f"arm {arm}")
        for r in recs.values():
            r.update(m283.score(r))
        ident = [r for r in recs.values() if r["has_ident"]
                 and (r["has_S"] if arm == "S" else r["has_B"])]
        new = [r for r in ident if r["openalex"] not in prior]
        new.sort(key=lambda r: -(r["cited_by"] or 0))
        stage[arm] = {
            "frame": len(recs),
            "identified": len(ident),
            "identified_and_new_to_rounds_1_2": len(new),
            "blind_spot_share": round(len(new) / len(ident), 3) if ident else None,
            "no_abstract": sum(1 for r in recs.values() if not r["abstract"]),
        }
        print(f"    arm {arm}: {len(recs)} frame -> {len(ident)} identified -> "
              f"{len(new)} NEW to rounds 1-2 ({stage[arm]['blind_spot_share']})")
        for r in new[:SEEDS_PER_ARM]:
            if (r.get("type") or "").lower() in NON_STUDY:
                continue
            seeds.append({"openalex": r["openalex"], "arm": arm, "title": r["title"],
                          "cited_by": r["cited_by"], "venue": r["venue"], "year": r["year"]})
        stage[arm]["top_new"] = [{k: r[k] for k in
                                  ("openalex", "doi", "title", "year", "venue", "cited_by")}
                                 for r in new[:20]]

    print(f"\nSTAGE 3 — snowball from {len(seeds)} new estimand-matched seeds")
    for s in seeds:
        print(f"  seed [{s['arm']}] {s['year']} cites{(s['cited_by'] or 0):5d} "
              f"{(s['title'] or '')[:66]}")

    # hydrate refs + twins (with ? and ! stripped: inside a quoted filter value they
    # return a SILENT zero, which cost round 1 every `?` seed's twins)
    pool, back = {}, defaultdict(set)
    for s in seeds:
        d, err = get([("filter", f"openalex_id:{s['openalex']}"), ("per-page", "1"),
                      ("select", SELECT)])
        s["refs"] = [] if err else (d["results"][0].get("referenced_works") or [])
        qt = re.sub(r"\s+", " ", re.sub(r"[?!]", " ", (s["title"] or "").replace('"', " "))).strip()
        dt, et = get([("filter", f'title.search:"{qt}"'), ("per-page", "10"), ("select", SELECT)])
        s["twins"] = []
        if not et:
            for tw in dt.get("results", []):
                oid = tw["id"].rsplit("/", 1)[-1]
                if oid != s["openalex"] and (tw.get("type") or "").lower() not in NON_STUDY \
                        and fold(tw.get("title")) == fold(s["title"]):
                    s["twins"].append({"openalex": oid,
                                       "refs": tw.get("referenced_works") or []})

    refs = sorted({r.rsplit("/", 1)[-1] for s in seeds
                   for r in s["refs"] + [x for t in s["twins"] for x in t["refs"]]})
    for s in seeds:
        for r in s["refs"] + [x for t in s["twins"] for x in t["refs"]]:
            back[r.rsplit("/", 1)[-1]].add(s["openalex"])
    print(f"\nbackward: {len(refs)} distinct works")
    for i in range(0, len(refs), 50):
        d, err = get([("filter", "openalex_id:" + "|".join(refs[i:i + 50])),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            continue
        for w in d["results"]:
            rec = shape(w)
            rec.update({"seeds_backward": sorted(back.get(rec["openalex"], [])),
                        "seeds_forward": []})
            pool[rec["openalex"]] = rec

    print("forward:")
    for s in seeds:
        for cid in [s["openalex"]] + [t["openalex"] for t in s["twins"]]:
            d, err = get([("filter", f"cites:{cid}"), ("per-page", str(FORWARD_CAP)),
                          ("sort", "cited_by_count:desc"), ("select", SELECT)])
            if err:
                continue
            for w in d["results"]:
                oid = w["id"].rsplit("/", 1)[-1]
                rec = pool.get(oid)
                if rec is None:
                    rec = shape(w)
                    rec.update({"seeds_backward": [], "seeds_forward": []})
                    pool[oid] = rec
                if s["openalex"] not in rec["seeds_forward"]:
                    rec["seeds_forward"].append(s["openalex"])

    arm_of = {s["openalex"]: s["arm"] for s in seeds}
    recs = list(pool.values())
    for r in recs:
        srcs = r["seeds_backward"] + r["seeds_forward"]
        r["seed_arms"] = sorted({arm_of[x] for x in srcs if x in arm_of})
        r.update(m283.score(r))
    new = [r for r in recs if r["openalex"] not in prior]
    keep = [r for r in new if r["has_outcome"] and (r["has_S"] or r["has_B"] or r["has_composite"])]
    keep.sort(key=lambda r: -(r["cited_by"] or 0))

    summary = {"prior_pool": len(prior), "stage1_2": stage,
               "seeds": len(seeds), "seeds_by_arm":
                   {a: sum(1 for s in seeds if s["arm"] == a) for a in ("S", "B")},
               "round3_pool": len(recs),
               "already_in_rounds_1_2": len(recs) - len(new),
               "NEW": len(new),
               "redundancy_rate": round((len(recs) - len(new)) / len(recs), 3) if recs else None,
               "NEW_carrying_exposure_and_outcome": len(keep),
               "of_those_identified": sum(1 for r in keep if r["has_ident"])}
    OUT.write_text(json.dumps({"summary": summary, "seeds": [
        {k: s[k] for k in ("openalex", "arm", "title", "year", "venue", "cited_by")}
        for s in seeds], "candidates": keep[:80]}, indent=2))
    print("\n" + json.dumps(summary, indent=1))
    print("\nNEW CANDIDATES (exposure x fertility outcome), round 3\n")
    for r in keep[:30]:
        arms = "".join(a for a, f in (("C", r["has_composite"]), ("S", r["has_S"]),
                                      ("B", r["has_B"])) if f)
        print(f"  {r['year']} {arms:3s} ident={'Y' if r['has_ident'] else 'n'} "
              f"cites{(r['cited_by'] or 0):5d} | {(r['title'] or '')[:76]}")
        print(f"        {r['venue']}")


if __name__ == "__main__":
    main()
