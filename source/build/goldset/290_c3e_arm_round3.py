#!/usr/bin/env python3
"""290 — C.3.e: Arm S / Arm B snowball round 3, HAND-SEEDED. TICK-077.

288 selected its seeds automatically -- top-cited among records the abstract classifier scored
as arm-matched and identified -- and returned "The legacy of Lionel McKenzie" and a Spanish-
language paper on the Mexican electricity sector. The classifier is a TRIAGE. Automating a seed
choice that was hand-read for the composite cell in 283 just reproduces the triage's noise, and
a snowball amplifies whatever it is given.

So the seeds here are hand-read from 288's stage-1 lists, and named in the file so the round is
reproducible and the judgement is auditable:

  Arm S  · AGEP Zambia cluster-RCT (savings-account component, fertility outcomes)
         · Delavallade et al., insurance-versus-savings experiment
         · Billari and Galasso, Italian pension reforms -- BOUNDARY: pension exposure is C.3.c's
           under Wall 1, seeded as a decoy because decoy clouds have run 29-88% on-topic
  Arm B  · Dettling and Kearney, "Did the Modern Mortgage Set the Stage for the U.S. Baby Boom?"
           -- mortgage CREDIT, not house prices, so C.3.e's under Wall 2
         · Li, Fertility and Housing Market: Australian Evidence
         · Davis-Friedmann, Old Age Security and the One-child Campaign -- boundary, C.3.c

The measurement that matters is redundancy against rounds 1-2. Round 1's ARM seeds, unlike its
composite ones, were estimand-matched (Cain, Pörtner, Pitt; Cumming, Babies of Mortgage
Deregulation, PNAS). If those arms were already covered, this round should come back largely
REDUNDANT -- and that is a result about coverage, not a failure.

Usage: python3 290_c3e_arm_round3.py
"""
import importlib.util, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"
OUT = LOGS / "credit-constraints-arm-round3.json"
FORWARD_CAP = 200

HAND_SEEDS = [
    ("W3011170043", "S", "anchor", "AGEP Zambia cluster RCT"),
    ("W3122525178", "S", "anchor", "Delavallade: insurance vs savings experiment"),
    ("W1512976090", "S", "decoy", "Billari and Galasso: Italian pension reforms (C.3.c boundary)"),
    ("W4407312762", "B", "anchor", "Dettling and Kearney: the modern mortgage and the baby boom"),
    ("W2998507442", "B", "anchor", "Li: fertility and housing market, Australia"),
    ("W2476864819", "S", "decoy", "Davis-Friedmann: old age security and the one-child campaign"),
]


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


def main():
    prior = {r["openalex"] for r in
             json.loads((LOGS / "credit-constraints-snowball-pool.json").read_text())}
    prior |= {r["openalex"] for r in
              json.loads((LOGS / "credit-constraints-snowball-round2.json").read_text())["records"]}

    seeds = []
    for oid, arm, role, label in HAND_SEEDS:
        d, err = get([("filter", f"openalex_id:{oid}"), ("per-page", "1"), ("select", SELECT)])
        if err or not d["results"]:
            print(f"  seed {oid} FAILED: {err}")
            continue
        w = d["results"][0]
        s = {"openalex": oid, "arm": arm, "role": role, "label": label,
             "title": w.get("title"), "refs": w.get("referenced_works") or [], "twins": []}
        qt = re.sub(r"\s+", " ",
                    re.sub(r"[?!]", " ", (s["title"] or "").replace('"', " "))).strip()
        dt, et = get([("filter", f'title.search:"{qt}"'), ("per-page", "10"), ("select", SELECT)])
        if not et:
            for tw in dt.get("results", []):
                t = tw["id"].rsplit("/", 1)[-1]
                if t != oid and (tw.get("type") or "").lower() not in NON_STUDY \
                        and fold(tw.get("title")) == fold(s["title"]):
                    s["twins"].append({"openalex": t, "refs": tw.get("referenced_works") or []})
        seeds.append(s)
        print(f"  [{arm}/{role}] {label}: {len(s['refs'])} refs, {len(s['twins'])} twins")

    pool, back = {}, defaultdict(set)
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
            print(f"  {d['meta']['count']:5d} citing {cid} ({s['label'][:44]})")
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
    cand = [r for r in new if r["has_outcome"] and (r["has_S"] or r["has_B"] or r["has_composite"])]
    cand.sort(key=lambda r: -(r["cited_by"] or 0))

    summary = {"seeds": len(seeds), "prior_pool": len(prior), "round3_pool": len(recs),
               "already_in_rounds_1_2": len(recs) - len(new), "NEW": len(new),
               "redundancy_rate": round((len(recs) - len(new)) / len(recs), 3) if recs else None,
               "NEW_carrying_exposure_and_outcome": len(cand),
               "of_those_identified": sum(1 for r in cand if r["has_ident"]),
               "no_abstract_in_new": sum(1 for r in new if not r["abstract"])}
    OUT.write_text(json.dumps({"summary": summary,
                               "seeds": [{k: s[k] for k in ("openalex", "arm", "role", "label")}
                                         for s in seeds],
                               "candidates": cand[:80]}, indent=2))
    print("\n" + json.dumps(summary, indent=1))
    print("\nNEW CANDIDATES (exposure x fertility outcome)\n")
    for r in cand[:28]:
        arms = "".join(a for a, f in (("C", r["has_composite"]), ("S", r["has_S"]),
                                      ("B", r["has_B"])) if f)
        print(f"  {r['year']} {arms:3s} ident={'Y' if r['has_ident'] else 'n'} "
              f"cites{(r['cited_by'] or 0):5d} | {(r['title'] or '')[:74]}")


if __name__ == "__main__":
    main()
