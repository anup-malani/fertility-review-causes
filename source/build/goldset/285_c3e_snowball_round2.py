#!/usr/bin/env python3
"""285 — C.3.e snowball round 2, seeded from the boundary-spanning candidates. TICK-077.

Round 1 was seeded from anchors chosen by design celebrity, and 283 showed what that cost:
of 119 boundary-hunt hits, 112 came from the term channel and only 2 from the 3,976-record
provenance pool. The snowball could not see the microfinance-and-fertility literature because
its seeds were not in it.

Round 2 fixes the seeds, not the method. It snowballs from the four studies that actually pair
a financial-access exposure with a fertility outcome. Their citation neighbourhood is unexplored
and — unlike round 1's — should not be dominated by business-outcome microcredit work.

The measurement that matters is NOT pool size. It is how much of round 2's yield round 1 already
had: a rung that only finds what another rung already found is REDUNDANT, which is a different
finding from productive, and reporting a raw count hides it.

Usage: python3 285_c3e_snowball_round2.py
"""
import importlib.util, json, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"

spec = importlib.util.spec_from_file_location("m277", GOLD / "277_c3e_snowball.py")
m277 = importlib.util.module_from_spec(spec)
sys.modules["m277"] = m277
spec.loader.exec_module(m277)
get, shape, fold, SELECT, CAP = m277.get, m277.shape, m277.fold, m277.SELECT, m277.FORWARD_CAP

SEEDS = {"10.1007/s13524-011-0029-0": "desai-tarozzi-2011",
         "10.31899/pgy6.1016": "steele-amin-naved-1998",
         "10.1353/jda.2012.0037": "kuchler-2012",
         "10.1080/00036846.2023.2244249": "lan-pan-yu-2023"}
NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter", "other"}


def main():
    hunt = json.loads((LOGS / "credit-constraints-boundary-hunt.json").read_text())
    r1 = {r["openalex"] for r in
          json.loads((LOGS / "credit-constraints-snowball-pool.json").read_text())}
    seeds, errors = [], {}

    for h in hunt["hits"]:
        if h["doi"] not in SEEDS:
            continue
        d, err = get([("filter", f"openalex_id:{h['openalex']}"), ("per-page", "1"),
                      ("select", SELECT)])
        if err or not d["results"]:
            errors[h["openalex"]] = err or "not found"
            continue
        w = d["results"][0]
        s = {"openalex": h["openalex"], "key": SEEDS[h["doi"]], "title": w.get("title"),
             "refs": w.get("referenced_works") or [], "twins": []}
        # twins, with `?` and `!` stripped -- inside a quoted filter value they return a
        # SILENT zero, which is how round 1 lost twins for all seven `?` seeds.
        import re
        qt = re.sub(r"\s+", " ", re.sub(r"[?!]", " ", (s["title"] or "").replace('"', " "))).strip()
        dt, et = get([("filter", f'title.search:"{qt}"'), ("per-page", "10"), ("select", SELECT)])
        if not et:
            for tw in dt.get("results", []):
                oid = tw["id"].rsplit("/", 1)[-1]
                if oid != s["openalex"] and (tw.get("type") or "").lower() not in NON_STUDY \
                        and fold(tw.get("title")) == fold(s["title"]):
                    s["twins"].append({"openalex": oid, "refs": tw.get("referenced_works") or []})
        seeds.append(s)
        print(f"  seed {s['key']}: {len(s['refs'])} refs, {len(s['twins'])} twins")

    pool, back = {}, defaultdict(set)
    refs = sorted({r.rsplit("/", 1)[-1] for s in seeds
                   for r in s["refs"] + [x for t in s["twins"] for x in t["refs"]]})
    for s in seeds:
        for r in s["refs"] + [x for t in s["twins"] for x in t["refs"]]:
            back[r.rsplit("/", 1)[-1]].add(s["key"])
    print(f"\nbackward: {len(refs)} distinct works")
    for i in range(0, len(refs), 50):
        d, err = get([("filter", "openalex_id:" + "|".join(refs[i:i + 50])),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            errors[f"back:{i}"] = err
            continue
        for w in d["results"]:
            rec = shape(w)
            rec.update({"seeds_backward": sorted(back.get(rec["openalex"], [])),
                        "seeds_forward": [], "first_found_round": 2})
            pool[rec["openalex"]] = rec

    print(f"forward: citations of {len(seeds)} seeds (+twins), cap {CAP}")
    for s in seeds:
        for cid in [s["openalex"]] + [t["openalex"] for t in s["twins"]]:
            d, err = get([("filter", f"cites:{cid}"), ("per-page", str(CAP)),
                          ("sort", "cited_by_count:desc"), ("select", SELECT)])
            if err:
                errors[f"fwd:{cid}"] = err
                continue
            print(f"  {d['meta']['count']:5d} citing {cid} ({s['key']})")
            for w in d["results"]:
                oid = w["id"].rsplit("/", 1)[-1]
                rec = pool.get(oid)
                if rec is None:
                    rec = shape(w)
                    rec.update({"seeds_backward": [], "seeds_forward": [],
                                "first_found_round": 2})
                    pool[oid] = rec
                if s["key"] not in rec["seeds_forward"]:
                    rec["seeds_forward"].append(s["key"])

    recs = list(pool.values())
    new = [r for r in recs if r["openalex"] not in r1]
    log = {"meta": {"ticket": "TICK-077", "round": 2, "seeds": len(seeds),
                    "round2_pool": len(recs),
                    "already_in_round1": len(recs) - len(new),
                    "NEW_not_in_round1": len(new),
                    "redundancy_rate": round((len(recs) - len(new)) / len(recs), 3) if recs else None,
                    "errors": len(errors)},
           "errors": errors}
    (LOGS / "credit-constraints-snowball-round2.json").write_text(
        json.dumps({"log": log, "records": sorted(new, key=lambda r: -(r["cited_by"] or 0))},
                   indent=1))
    print("\n" + json.dumps(log["meta"], indent=1))
    print("\nTOP NEW RECORDS (not in round 1)")
    for r in sorted(new, key=lambda r: -(r["cited_by"] or 0))[:20]:
        print(f"  {r['year']} cites{(r['cited_by'] or 0):6d} | {(r['title'] or '')[:86]}")


if __name__ == "__main__":
    main()
