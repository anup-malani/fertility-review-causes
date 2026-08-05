#!/usr/bin/env python3
"""
96_d1a_snowball_r2.py — D.1.a, GACS channel 3, round 2. Repair round 1, then extend to generation 2.

Round 1 (`93_`) ended above the saturation floor at 1.73 new relevant per 50 pulled against a floor of
1.0, and its log left round 2 three specific jobs. This does those three and separates the two things
they measure, because mixing them would confound a repair with an extension.

  PART A -- REPAIR. Round 1's pull was incomplete in four known places and its yield was recorded as a
  lower bound rather than a saturation reading. Fixing all four changes what round 1's number MEANS,
  so it is measured against round 1's denominator and reported as a corrected round-1 statistic, not
  as round-2 output.
    A1. van de Kaa 1987 contributed 2 forward citations instead of its true neighbourhood, because
        the round-1 seed table carried a hand-typed DOI for a work that has none. Three providers now
        agree it has none. It is seeded here by Semantic Scholar paperId, READ FROM 95's OUTPUT --
        which is the process change round 1 committed to: seed tables are generated from resolver
        output, never typed. No identifier in this file is a literal.
    A2..A4. Three seed cells came back UNCONFIRMED on unauthenticated S2 throttling, which is a
        statement about the network and not about the literature. Retried.
    A5. Lesthaeghe and Surkyn 1988 hit the 600-record forward cap with more available. The cap is
        lifted for this seed only.

  PART B -- EXTEND. Generation 2, which is what a round 2 actually is.
    B1. New channel-2 canon seeds in the families round 1 under-reached. Round 1's frame was six of
        nine seeds in demography-SDT, the economics-of-culture family had one seed whose forward pull
        failed, and the values-psychology family had NO seed at all.
    B2. The round-1 relevant records, as second-generation seeds. This is not circular: the round-1
        constraint that Tier B must not be seeded from the query's own output is about TIER-A keyword
        results, and these records came out of the snowball itself.

SEED SELECTION APPLIES ROUND 1'S CRITERION, WHICH IS SPECIFICITY OF THE CITATION NEIGHBOURHOOD AND NOT
FAME. Round 1 refused to seed Hofstede 1980 (15,158 citations) and Schwartz 1992 because their
neighbourhoods are the management and cross-cultural-psychology literatures -- canon for a CONSTRUCT,
not for this treatment x outcome pair -- and seeding them would bury the frame and make the yield
statistic meaningless. That holds here. Note in passing that all four construct-canon works excluded
on that criterion are also the four that failed to resolve cleanly in 95; the judgement and the
evidence happen to agree, but the judgement was made first and would stand without it.

THE JUDGEMENT CALLS ARE MARKED AND MEASURED RATHER THAN ARGUED. Three seeds sit near the line: Voas
2009 and Inglehart 1977 / Inglehart and Baker 2000 are closer to construct canon than to pair canon,
but the postmaterialism and individualism strata have no channel-1 review and no seed at all, so
refusing them means those strata are unreachable through channel 3 entirely. They are seeded and
flagged `judgement`, and per-seed yield is reported, so a reader can see whether they earned their
place or swamped the frame. If they swamped it, that is itself the finding the chapter needs about
whether S1 and S2 have a reachable empirical literature.

THE STOP STATISTIC CHANGES MEANING IN ROUND 2 AND THAT IS EASY TO GET WRONG. GACS 7.2's floor is new
relevant papers per 50 records pulled. In round 1 every relevant record was new. Here the numerator
must exclude anything already in the round-1 pool, or the frame re-counts its own round-1 catch and
reports saturation it has not reached. Novelty is keyed on normalized title, matching round 1's dedup.

Output: temp/d1a/snowball-r2-pool.json
        literature/search-logs/{slug}-snowball-log.md   (rewritten to cover both rounds)
"""
import json, os, re, subprocess, sys, time, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1a_fetch import Fetcher, is_not_found  # noqa: E402
from d1a_relevance import VERSION as RELEVANCE_VERSION, relevant  # noqa: E402

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
R1_POOL = os.path.join(TMP, "snowball-r1-pool-relabelled.json")
CANON = os.path.join(TMP, "canon-seeds-reresolved.json")
OUT = os.path.join(TMP, "snowball-r2-pool.json")
CACHE_PATH = os.path.join(HERE, "d1a_snowball_cache.json")   # shared with 93; round-1 calls are free
FETCH = Fetcher(CACHE_PATH, UA)
_purged = FETCH.purge_throttled()
if _purged:
    print(f"purged {_purged} cached throttle responses -- see d1a_fetch.py", file=sys.stderr)

FWD_CAP_CANON = 600     # a canon seed's neighbourhood, same as round 1
FWD_CAP_UNCAPPED = 2000  # A5 only: Lesthaeghe and Surkyn hit the round-1 cap with more available
FWD_CAP_GEN2 = 200      # generation-2 seeds are for BREADTH, not depth -- see the cap note in main()
S2_PAGE = 100
S2_SLEEP = 1.8

# Round-1 seeds needing a retry. Labels and DOIs carried from 93's SEEDS so the two runs line up.
REPAIR = {
    "Fernandez (Does Culture Matter?)": ("10.1016/b978-0-444-53187-2.00011-5", "forward", "econ-of-culture"),
    "SSA religions review 2023": ("10.29063/ajrh2023/v27i1.11", "backward", "sociology-of-religion"),
    "SSA religion/religiosity review 2021": ("10.31237/osf.io/sezdq", "forward", "sociology-of-religion"),
}
UNCAP = {"Lesthaeghe & Surkyn 1988": ("10.2307/1972499", "demography-SDT")}

# Canon labels to add as generation-2 seeds, with the family they are being added to REACH and whether
# the call is a judgement one. Identifiers come from 95's output, keyed on these labels -- not typed.
NEW_CANON = {
    "Frejka and Westoff 2008":   ("sociology-of-religion", False),  # v5 seminal, on-pair, 92 left UNCONFIRMED
    "McQuillan 2004":            ("sociology-of-religion", False),  # "When does religion influence fertility?"
    "Hagestad and Call 2007":    ("sociology-of-religion", False),  # v5 seminal, rescued by 95's subtitle gate
    "Lesthaeghe 1983":           ("demography-SDT", False),         # v5 seminal, resolved in 92 and never seeded
    "Enke 2019":                 ("econ-of-culture", False),        # the family round 1 reached with one dead seed
    "Voas 2009":                 ("sociology-of-religion", True),   # judgement: secularization construct canon
    "Inglehart 1977":            ("values-psychology", True),       # judgement: the family with no seed at all
    "Inglehart and Baker 2000":  ("values-psychology", True),       # judgement; also TWIN_DOI, both are pulled
}


def get(url, sleep=None):
    return FETCH.get(url, sleep=sleep)


def crossref_refs(doi):
    d = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}")
    if d is not None and is_not_found(d):
        return "NOT_INDEXED"
    if not d or "message" not in d:
        return None
    # Crossref reference deposition is optional and widely skipped, so an empty reference list is a
    # fact about the PUBLISHER'S metadata, not about the paper. Lesthaeghe 1983 in PDR returns zero
    # references and obviously has them. Reported as its own state so a backward count of 0 is never
    # read as "this work cites nothing".
    if not (d["message"].get("reference") or []):
        return "NO_REFS_DEPOSITED"
    out = []
    for r in (d["message"].get("reference") or []):
        t = r.get("article-title") or r.get("volume-title") or r.get("unstructured") or ""
        out.append({"doi": (r.get("DOI") or "").lower() or None, "title": t.strip()[:300],
                    "year": r.get("year"), "venue": r.get("journal-title") or "",
                    "direction": "backward"})
    return out


def s2_page(ident, kind, cap):
    """kind is 'citations' (forward) or 'references' (backward). ident is DOI:x or a raw paperId."""
    out, offset = [], 0
    field = "citingPaper" if kind == "citations" else "citedPaper"
    while offset < cap:
        url = (f"https://api.semanticscholar.org/graph/v1/paper/{urllib.parse.quote(ident, safe=':')}"
               f"/{kind}?fields=title,year,venue,externalIds&limit={S2_PAGE}&offset={offset}")
        d = get(url, sleep=S2_SLEEP)
        if d is None:
            return out if out else None
        if is_not_found(d):
            return out if out else "NOT_INDEXED"
        data = d.get("data") or []
        for row in data:
            p = row.get(field) or {}
            ext = p.get("externalIds") or {}
            out.append({"doi": (ext.get("DOI") or "").lower() or None, "title": p.get("title") or "",
                        "year": p.get("year"), "venue": p.get("venue") or "",
                        "s2id": p.get("paperId"),
                        "direction": "forward" if kind == "citations" else "backward"})
        if len(data) < S2_PAGE or "next" not in d:
            break
        offset = d["next"]
        time.sleep(S2_SLEEP)
    return out


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def pull(ident, want, cap):
    """Returns (records, status). `ident` is a DOI or an s2:<paperId>.

    FOUR STATES, kept apart because they support four different sentences about the literature:
      OK                 the provider answered with records
      UNCONFIRMED        the provider did not answer -- a fact about the network
      NOT_INDEXED        the provider answered and does not hold this work -- a fact about the index
      NO_REFS_DEPOSITED  Crossref holds the work but the publisher deposited no reference list
    Only the first supports a count. Collapsing any of the other three to zero manufactures an
    absence, which is the error this chapter has now made in three separate dialects.
    """
    if ident.startswith("s2:"):
        recs = s2_page(ident[3:], "citations" if want == "forward" else "references", cap)
    elif want == "backward":
        recs = crossref_refs(ident)
    else:
        recs = s2_page(f"DOI:{ident}", "citations", cap)
    if recs is None:
        return None, "UNCONFIRMED"
    if isinstance(recs, str):
        return None, recs
    return recs, "OK"


def main():
    r1 = json.load(open(R1_POOL))
    r1_keys = {norm_title(r.get("title"))[:120] for r in r1["pool"]}
    r1_keys.discard("")
    canon = {r["label"]: r for r in json.load(open(CANON))["rows"]}

    seeds, pool = {}, {}

    def add(label, ident, want, cap, family, part, judgement=False):
        recs, status = pull(ident, want, cap)
        seeds.setdefault(label, {"family": family, "part": part, "judgement": judgement,
                                 "idents": [], "backward": None, "forward": None,
                                 "backward_status": None, "forward_status": None, "caps": {}})
        s = seeds[label]
        s["caps"][want] = cap   # the cap ACTUALLY applied, so truncation is judged against it
        if ident not in s["idents"]:
            s["idents"].append(ident)
        if status == "OK":
            s[want] = (s[want] or 0) + len(recs)
        # A seed pulled under two identifiers (the TWIN_DOI case) can succeed on one and fail on the
        # other. OK wins, because the records were genuinely retrieved; otherwise keep the first
        # non-OK reason rather than overwriting it with a later one.
        if status == "OK" or s[f"{want}_status"] is None:
            s[f"{want}_status"] = status
        for rec in (recs or []):
            nt = norm_title(rec.get("title"))[:120]
            if not nt:
                continue
            if nt in pool:
                pool[nt]["seen_from"].append(label)
                if not pool[nt].get("doi") and rec.get("doi"):
                    pool[nt]["doi"] = rec["doi"]
            else:
                pool[nt] = {**rec, "seen_from": [label], "new_in_r2": nt not in r1_keys}
        print(f"  {label[:46]:48s} {want:8s} {status:12s} n={len(recs or [])}", file=sys.stderr)
        FETCH.save()

    # ---- PART A: repair round 1 -------------------------------------------------------------
    print("PART A -- repairing round 1", file=sys.stderr)
    vdk = canon["van de Kaa 1987"]
    if not vdk["seed_s2id"]:
        sys.exit("van de Kaa 1987 has no seedable S2 id in 95's output -- refusing to guess one")
    # Uncapped deliberately. The 600-record cap exists so one canon work cannot swamp the frame, but
    # van de Kaa 1987 carries ~1,316 citations and is the seed this entire round was convened to
    # repair. Fixing a seed that contributed 2 records and then truncating it at 46% of its
    # neighbourhood would leave the same gap the round-1 log called a lower bound, just smaller.
    add("van de Kaa 1987 (REPAIRED)", f"s2:{vdk['seed_s2id']}", "forward", FWD_CAP_UNCAPPED,
        "demography-SDT", "A")
    add("van de Kaa 1987 (REPAIRED)", f"s2:{vdk['seed_s2id']}", "backward", FWD_CAP_CANON,
        "demography-SDT", "A")
    for label, (doi, want, fam) in REPAIR.items():
        add(f"{label} (RETRY)", doi, want, FWD_CAP_CANON, fam, "A")
    for label, (doi, fam) in UNCAP.items():
        add(f"{label} (UNCAPPED)", doi, "forward", FWD_CAP_UNCAPPED, fam, "A")

    # ---- PART B1: new canon seeds in the under-reached families -----------------------------
    print("PART B1 -- new canon seeds", file=sys.stderr)
    for label, (fam, judge) in NEW_CANON.items():
        row = canon.get(label)
        if not row or not row["seedable"]:
            print(f"  {label[:46]:48s} SKIPPED -- no seedable identifier in 95", file=sys.stderr)
            continue
        ids = [i for i in (row["seed_doi"], row["seed_doi_alt"]) if i]
        if row["seed_s2id"] and not ids:
            ids = [f"s2:{row['seed_s2id']}"]
        for ident in ids:
            add(label, ident, "backward", FWD_CAP_CANON, fam, "B1", judge)
            add(label, ident, "forward", FWD_CAP_CANON, fam, "B1", judge)

    # ---- PART B2: generation 2, seeded from the round-1 relevant records ---------------------
    # THE FORWARD CAP HERE IS A COVERAGE DECISION AND IS STATED RATHER THAN BURIED. Generation-2
    # seeds are ordinary papers, not canon, and the job of this leg is breadth across 84 of them
    # rather than depth into any one, so forward pulls stop at 200. Any seed that hits the cap is
    # reported by name in the log, so a reader sees exactly where the frame was truncated instead of
    # being handed a total that reads as complete coverage.
    # A round-1 relevant record with no DOI but an S2 paperId is still seedable -- forward from the
    # paperId, no backward. Dropping those would repeat the round-1 seed error's whole lesson in
    # miniature: van de Kaa 1987 has no DOI and is the single most important work in this literature,
    # so "no DOI" cannot be allowed to mean "not seedable".
    r1_rel = [r for r in r1["pool"] if r["relevant"]]
    gen2 = [r for r in r1_rel if r.get("doi") or r.get("s2id")]
    n_unseedable = len(r1_rel) - len(gen2)
    print(f"PART B2 -- generation 2 from {len(gen2)} of {len(r1_rel)} round-1 relevant records "
          f"({n_unseedable} carry neither a DOI nor an S2 id and cannot be seeded)", file=sys.stderr)
    for i, r in enumerate(gen2, 1):
        lab = f"gen2:{(r.get('title') or '')[:60]}"
        print(f"  [{i}/{len(gen2)}]", file=sys.stderr)
        if r.get("doi"):
            add(lab, r["doi"], "backward", FWD_CAP_GEN2, "gen2", "B2")
            add(lab, r["doi"], "forward", FWD_CAP_GEN2, "gen2", "B2")
        else:
            add(lab, f"s2:{r['s2id']}", "forward", FWD_CAP_GEN2, "gen2", "B2")

    # ---- scoring ---------------------------------------------------------------------------
    for v in pool.values():
        ok, why = relevant(v)
        v["relevant"], v["relevance_reason"] = ok, why

    recs = list(pool.values())
    new = [r for r in recs if r["new_in_r2"]]
    new_rel = [r for r in new if r["relevant"]]
    part = lambda p: [s for s in seeds.values() if s["part"] == p]  # noqa: E731
    pulled_of = lambda ss: sum((s["backward"] or 0) + (s["forward"] or 0) for s in ss)  # noqa: E731

    pulled_A, pulled_B = pulled_of(part("A")), pulled_of(part("B1") + part("B2"))
    pulled_all = pulled_A + pulled_B
    # Attribute a new relevant record to part A only if EVERY seed that reached it is a part-A seed.
    seed_part = {lab: s["part"] for lab, s in seeds.items()}
    relA = [r for r in new_rel if all(seed_part.get(l) == "A" for l in set(r["seen_from"]))]
    relB = [r for r in new_rel if r not in relA]

    counts = {
        "relevance_filter_version": RELEVANCE_VERSION,
        "round1_corrected": {"relevant": sum(1 for r in r1["pool"] if r["relevant"]),
                             "records_pulled": r1["counts"]["records_pulled"],
                             "yield_per_50": r1["counts"]["yield_per_50_pulled"]},
        "partA_repair": {"records_pulled": pulled_A, "new_relevant": len(relA),
                         "yield_per_50": round(len(relA) / pulled_A * 50, 2) if pulled_A else 0},
        "partB_generation2": {"records_pulled": pulled_B, "new_relevant": len(relB),
                              "yield_per_50": round(len(relB) / pulled_B * 50, 2) if pulled_B else 0},
        "round2_total": {"records_pulled": pulled_all, "distinct": len(recs),
                         "new_vs_round1": len(new), "new_relevant": len(new_rel),
                         "yield_per_50": round(len(new_rel) / pulled_all * 50, 2) if pulled_all else 0,
                         "stop_floor_per_50": 1.0},
        # Truncated against the cap that was actually applied to THAT seed, not a global constant.
        # van de Kaa was pulled uncapped and returned its full 1,316; comparing it to the 600 default
        # reported the repaired seed as truncated, which is the opposite of what happened.
        "capped_seeds": sorted(lab for lab, s in seeds.items()
                               if (s["forward"] or 0) >= s["caps"].get("forward", 10 ** 9)),
        "gen2_seeds_used": len(gen2), "gen2_unseedable": n_unseedable,
        # Every cell that did not return records, by reason. This is the denominator's honesty check:
        # a pull total means nothing without knowing what failed to be pulled and why.
        "non_ok_cells": {
            st: sorted(f"{lab} [{d}]" for lab, s in seeds.items() for d in ("backward", "forward")
                       if s[f"{d}_status"] == st)
            for st in ("UNCONFIRMED", "NOT_INDEXED", "NO_REFS_DEPOSITED")
        },
        "throttle_retries": FETCH.throttled,
    }
    json.dump({"slug": SLUG, "round": 2, "counts": counts, "seeds": seeds, "pool": recs},
              open(OUT, "w"), indent=1)
    print(json.dumps(counts, indent=1)[:2200], file=sys.stderr)
    print(f"wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
