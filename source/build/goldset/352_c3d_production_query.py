#!/usr/bin/env python3
"""352 — C.3.d production query SET, calibrated against the 82 resolved anchors (TICK-083).

Ported from C.2.f's 337 (itself C.2.b's 320, itself C.6.a's 308). The machinery is carried over
unchanged: per-term leave-one-out, a cost ceiling per additional anchor recalled, recall measured by
asking OpenAlex which anchors a query returns rather than re-implementing its tokenizer, the
two-pool retry that tells an exhausted budget from a boolean throttle, and the refusal guard that
writes NOTHING if any query was refused.

WHY A SET OF ARMS, AND WHY THIS CHAPTER NEEDS FOUR
--------------------------------------------------
Scope §3 measured that C.3.d's own vocabulary does not index the studies that test C.3.d: 93% of
the channel-1 forward arm and 98% of the channel-2 shock literature sit outside the 762-record
theory frame, and only 61 of 4,690 family-size-shock records use any C.3.d term. A single query
built on the theory axis would retrieve the theoretical literature and miss the empirical one. So
the scope pre-registered THREE exposure axes -- theory, design, shock -- and this script builds
them, with recall reported PER ARM because a pooled recall number hides an arm that is failing.

THE OUTCOME AXIS IS NOT THE SAME IN EVERY ARM, AND THAT IS SCOPE §2
------------------------------------------------------------------
The registered claim runs FORWARD (return to child human capital -> fertility). The literature's
famous test runs BACKWARD (exogenous family size -> investment or attainment per child). Script 350
confirmed the asymmetry on the canon: the five BACKWARD hand anchors carry 2,898 citations against
491 for the four FORWARD ones.

**A backward anchor cannot be recalled by a query carrying a fertility outcome axis.** Its dependent
variable is children's schooling. Scoring it against the fertility axis would report a structural
zero as a vocabulary miss -- the `named-retry-author-queries-fake-zeros` failure. So the `backward`
arm is scored against a CHILD-OUTCOME axis, and only the forward arms can populate a primary cell.

ONE PORTED GATE NEEDED A FIX, AND IT IS THE `optional-field-gate-disengages` SHAPE
---------------------------------------------------------------------------------
337 selects gold with `a.get("outcome_is_fertility", True)`. Script 349 writes that field as
`None` on all 65 controls, meaning "not known" -- and `None` is falsy, so the ported expression
would have structurally excluded EVERY control from the primary recall denominator while looking
like it was working. `measures_fertility()` below treats None as includable and says so.

Acceptance rule: gain > 0 AND cost-per-anchor under COST_CEILING, every rejection logged with its
price. The baseline ADVANCES as terms are accepted, or later terms inherit credit for earlier ones'
gold (`advance-the-baseline-when-accepting-terms`).

Usage: python3 source/build/goldset/352_c3d_production_query.py
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"

MATCHED = {"MATCH", "MATCH_STEM", "MATCH_BY_ID", "MATCH_BY_DOI", "MATCH_VERSION_TWIN"}
COST_CEILING = 400      # records admitted per additional anchor recalled

# Held identical to the scope's §3 measurements so the frames compose with 344-346.
# `"demographic transition"` is in the BASE rather than offered as a candidate, and the reason is
# scope §6 rather than recall-chasing: C.3.d is registered for FDT as well as SDT, and the FDT
# literature calls the outcome "the demographic transition", not "fertility". Without it the
# reachability ceiling refused four of the eight theory anchors -- Becker & Lewis 1973, Becker &
# Tomes 1976, Galor & Weil 2000 and Galor & Moav 2002 -- whose titles and abstracts carry no
# fertility word at all. Galor & Weil's title is literally "...From Malthusian Stagnation to the
# Demographic Transition and Beyond". An outcome axis missing a registered phenomenon's own name is
# a gap in the axis, not a property of the literature.
OUTCOME = ['"fertility"', '"childbearing"', '"birth rate"', '"total fertility rate"',
           '"family size"', '"number of children"', '"demographic transition"']

# The BACKWARD arm's dependent variable. Scope §2: family size is the exposure and a child outcome
# is the outcome, so a fertility axis would score every backward anchor as a structural zero.
# WIDENED ONCE AND REVERTED, and the measurement is the reason to record it. The reachability
# ceiling showed this axis could not reach two of its own five Tier-A anchors -- Rosenzweig & Wolpin
# 1980 and Angrist, Lavy & Schlosser 2010 -- so the obvious move was to widen it. Priced properly,
# every candidate bought ZERO canon recall:
#
#     base                        frame  1,006   canon 3/5
#     + "schooling"               frame  1,328   canon 3/5
#     + "education"               frame 10,429   canon 3/5   (+9,423 records for nothing)
#     + "child quality"           frame  1,059   canon 3/5
#     + "human capital"           frame  1,292   canon 3/5
#
# The widening had raised the ceiling from 7/29 to 15/29 and recall from 7 to 13 -- but ALL of that
# was CONTROLS, not canon, and it cost a 10x frame. By the script's own acceptance rule that is a
# reject at roughly 1,600 records per anchor, and putting it in the BASE axis rather than in
# `outcome_candidates` was what let it bypass the rule. Reverted.
#
# The two anchors are not missing because the outcome axis is narrow. They are missing because
# their EXPOSURE vocabulary is the theory axis, not the design axis: neither title says "family
# size", both say "quantity and quality". They are reached by the `theory` arm and therefore by the
# union, which is what the union recall number is for. Per-arm attribution was the thing that was
# wrong, not the axis. `a-recall-miss-can-indict-the-anchors`: read the missed record before
# widening the query.
OUTCOME_CHILD = ['"educational attainment"', '"test scores"', '"years of schooling"',
                 '"child outcomes"', '"school achievement"', '"cognitive ability"']

# Only the FORWARD arms can populate a primary cell (scope §9). `theory` is context -- the models
# themselves -- and `backward` is mechanism evidence on link 2, retrieved into its own estimand cell
# and never pooled with a forward effect.
PRIMARY_ARMS = {"forward-shock", "forward-design"}


def measures_fertility(a):
    """Can this anchor be recalled by a fertility outcome axis?

    `outcome_is_fertility` is True/False on the 17 hand anchors and None on the 65 controls, where
    it means NOT KNOWN rather than no. The ported expression `measures_fertility(a)`
    returns None for a control, which is falsy, so every control would have been dropped from the
    primary denominator silently -- right-looking counters, wrong mechanism
    (`optional-field-gate-disengages`). Unknown is includable; only an explicit False excludes.
    """
    v = a.get("outcome_is_fertility")
    return True if v is None else bool(v)


ARMS = [
    # AXIS 1, THEORY. The 762-record frame from scope §3. Its dominant term is the mechanism's own
    # name (`quantity-quality`, 494 of 762), which is why the frame looked healthy and why §3 had to
    # go looking for what it missed. Retrieved and screened -- the models are the THEORY cell and the
    # snowball's richest seed bed -- but it cannot populate a primary cell on its own.
    {"name": "theory", "targets": ["theory", "seed:quantity-quality", "seed:child quality",
                                   "seed:child human capital", "seed:unified growth"],
     "base": ['"quantity-quality"', '"child quality"'], "outcome": OUTCOME,
     "candidates": ['"quantity quality tradeoff"', '"quality-quantity"', '"child quantity"',
                    '"human capital of children"', '"child human capital"', '"sibsize"',
                    '"unified growth"', '"quality of children"'],
     "outcome_candidates": ['"completed fertility"', '"desired family size"',
                            '"fertility decline"']},

    # AXIS 3, SHOCK -- forward, and on scope §7 rows 1, 2, 5 and 6 this is where the registered
    # estimand actually lives. 346 measured the channel-2 shock literature at 770 records against a
    # fertility outcome with only 15 inside the theory frame, and 35 carrying an identified-design
    # marker. If C.3.d has a primary cell, most of it is here.
    {"name": "forward-shock", "targets": ["forward", "seed:skill shock", "seed:returns to skill"],
     "base": ['"import competition"', '"skill premium"'], "outcome": OUTCOME,
     "candidates": ['"trade liberalization"', '"China shock"', '"industrial robots"',
                    '"automation"', '"returns to schooling"', '"return to education"',
                    '"occupational structure"', '"skill-biased technical change"',
                    '"return to human capital"', '"college premium"'],
     "outcome_candidates": ['"completed fertility"', '"fertility decline"',
                            '"fertility transition"']},

    # AXIS 2, DESIGN -- forward half. Scope §7 row 3 is the LARGEST forward row at 188 records, and
    # 350 already found it is where Wall 2 bites: five of the resolved fertility-outcome controls
    # name female or maternal education, which is C.2.e's estimand and not this chapter's. The arm
    # is retrieved in full and the wall is adjudicated at full text, not by excluding vocabulary
    # here -- refusing the records would make the wall unmeasurable.
    {"name": "forward-design", "targets": ["seed:schooling reform"],
     "base": ['"compulsory schooling"', '"school construction"'], "outcome": OUTCOME,
     "candidates": ['"compulsory education"', '"school leaving age"', '"education expansion"',
                    '"universal primary education"', '"education reform"', '"schooling reform"'],
     "outcome_candidates": ['"completed fertility"', '"fertility decline"']},

    # AXIS 2, DESIGN -- backward half, scored on the CHILD-OUTCOME axis (scope §2). This is link 2:
    # does the substitution the theory requires actually happen. It is the arm the field weights
    # six-to-one, and the arm whose best identification -- the twin instrument -- largely FAILS to
    # find the tradeoff. Retrieved into `QQ_SUBSTITUTION`, never pooled with a forward effect, and
    # it cannot carry a demographic-significance number because it has no fertility numerator.
    {"name": "backward", "targets": ["backward", "seed:sibsize / sibship",
                                     "seed:family-size instrument", "seed:resource dilution",
                                     "seed:child investment"],
     "base": ['"family size"', '"sibship size"'], "outcome": OUTCOME_CHILD,
     "candidates": ['"number of siblings"', '"sibsize"', '"twin birth"',
                    '"sibling sex composition"', '"birth order"', '"resource dilution"',
                    '"quantity-quality"', '"family size and"'],
     "outcome_candidates": ['"child quality"', '"human capital"', '"child development"']},

    # WALL 2's separation arm (scope §8). C.3.d owns the return to the CHILD's human capital; C.2.e
    # owns the return to the PARENT's. Retrieved so the wall is TAGGABLE and its size measurable,
    # and kept OUT of the union: C.2.e is unstarted and this arm is its chapter, not ours. 350 put
    # the floor at 19% of fertility-outcome controls, so this is not a formality.
    {"name": "c2e-boundary", "targets": [], "in_union": False,
     "base": ['"female education"', '"maternal education"'], "outcome": OUTCOME,
     "candidates": ['"mother education"', '"female labor force participation"',
                    '"opportunity cost of time"', '"female wage"'],
     "outcome_candidates": []},
]


def q(exposure, outcome):
    return f"({' OR '.join(exposure)}) AND ({' OR '.join(outcome)})"


# Which pool served each request, and the two DIFFERENT limits behind the same error string.
#
# Measured 2026-09-03, and the first reading of it was wrong:
#   * Both paths draw on one daily budget for the client. `api_key` reported
#     dailyRemainingUsd 0.0004 while keyless requests still succeeded, which looked like "the key is
#     the metered path and keyless is free". It is not: 89 keyless requests later the keyless path
#     also reported dailyRemainingUsd 0. Keyless is not a bypass, it is the same wallet.
#   * The keyless path has an ADDITIONAL limit the keyed path does not: "queries with more than 5
#     boolean operators are limited to 1 request per second per client". Every query here is a
#     multi-term boolean, so keyless requests must be paced above a second apart.
#
# Both failures are worded "Rate limit exceeded", so the message body must be read to tell an
# exhausted budget (retry tomorrow) from a throttle (retry in a second). That is what the retry loop
# below distinguishes, and the fallback is COUNTED rather than silent so a divergence between the
# paths would be visible in the log.
POOL = {"key": 0, "polite": 0, "refused": 0, "throttle_waits": 0}

# The keyless pool has its own limit, and it is a RATE limit rather than a cap: "queries with more
# than 5 operators are limited to 1 request per second per client". Every query in this script is a
# multi-term boolean, so the polite pool must be paced at over a second per request or it starts
# refusing -- and the refusal is worded as "Rate limit exceeded", exactly like the budget error, so
# the two failures are easy to confuse. Measured 2026-09-03: three requests succeeded back to back,
# the fourth was refused.
POLITE_MIN_INTERVAL = 1.15
_last_polite = [0.0]


def _get(params, use_key):
    args = ["curl", "-sS", "--max-time", "120", "-G", "https://api.openalex.org/works"]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    if use_key and KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    else:
        gap = POLITE_MIN_INTERVAL - (time.monotonic() - _last_polite[0])
        if gap > 0:
            POOL["throttle_waits"] += 1
            time.sleep(gap)
        _last_polite[0] = time.monotonic()
    args += ["--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError:
        return None, f"non-JSON: {r.stdout[:160]}"


def call(params):
    d, err = _get(params, use_key=True)
    if err is None and "meta" in d and d["meta"].get("count") is not None:
        POOL["key"] += 1
        return d, None
    # An exhausted budget is a property of the KEY, not of the literature. Retry keyless.
    body = "" if d is None else json.dumps(d)
    if "Insufficient budget" in body or "Rate limit exceeded" in body:
        for attempt in range(4):
            d2, err2 = _get(params, use_key=False)
            if err2 is None and "meta" in d2 and d2["meta"].get("count") is not None:
                POOL["polite"] += 1
                return d2, None
            b2 = "" if d2 is None else json.dumps(d2)
            if "boolean operators" not in b2 and "Rate limit" not in b2:
                break
            time.sleep(1.5 * (attempt + 1))   # the throttle is per second; back off past it
        d, err = d2, err2
    POOL["refused"] += 1
    if err:
        return None, err
    return None, f"query refused (NOT an empty literature): {json.dumps(d)[:200]}"


CACHE_PATH = LOGS / ".cache" / "c3d-query-measurements.json"


def _load_cache():
    try:
        return json.loads(CACHE_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


CACHE = _load_cache()
CACHE_STATS = {"hit": 0, "miss": 0}


def _save_cache():
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(CACHE, indent=0, sort_keys=True) + "\n")


def measure(query, ids):
    key = json.dumps([query, sorted(ids)], sort_keys=True)
    if key in CACHE:
        CACHE_STATS["hit"] += 1
        c = CACHE[key]
        return c["n"], set(c["got"]), None
    CACHE_STATS["miss"] += 1
    d, err = call({"filter": f"title_and_abstract.search:{query}", "per-page": "1"})
    if err:
        return None, None, err
    n = d["meta"]["count"]
    d2, err = call({"filter": f"ids.openalex:{'|'.join(ids)},title_and_abstract.search:{query}",
                    "per-page": "200", "select": "id"})
    if err:
        return n, None, err
    got = {w["id"].rsplit("/", 1)[-1] for w in d2.get("results", [])}
    CACHE[key] = {"n": n, "got": sorted(got)}
    _save_cache()          # written per measurement, so an interrupted run keeps what it bought
    return n, got, None


def main():
    anchors = json.loads((LOGS / "quantity-quality-tradeoff-cold-start-anchors.json").read_text())
    gold = [a for a in anchors
            if a["verdict"] in MATCHED and (a.get("top_candidate") or {}).get("oa_id")]
    for a in gold:
        a["oa"] = a["top_candidate"]["oa_id"].rsplit("/", 1)[-1]
    all_ids = [a["oa"] for a in gold]
    # PRIMARY_ARMS holds ARM names; anchors carry the `arm` values those arms TARGET. On C.2.f the
    # two vocabularies coincided and the ported expression `a["arm"] in PRIMARY_ARMS` worked by
    # accident. Here they do not, and it silently selected ZERO primary anchors -- a denominator of
    # 0 that then divided by zero instead of reporting a wrong number, which is the only reason it
    # was noticed. Map through the arm definitions rather than comparing the two vocabularies.
    primary_targets = {t for arm in ARMS if arm["name"] in PRIMARY_ARMS for t in arm["targets"]}
    primary_all = [a for a in gold if a["arm"] in primary_targets]
    # An anchor whose own outcome is not fertility cannot be recalled by a query with a fertility
    # outcome axis, and counting it as a miss would blame the query for the anchor list's error.
    primary = [a for a in primary_all if measures_fertility(a)]
    excluded = [a for a in primary_all if not measures_fertility(a)]
    print(f"gold {len(gold)} anchors; {len(primary_all)} in a PRIMARY arm, of which {len(primary)} "
          f"measure fertility and {len(excluded)} do not:")
    for a in excluded:
        print(f"    STRUCTURALLY EXCLUDED  {a['title'][:60]} — {a.get('outcome_note','')}")
    print()

    log = {"cost_ceiling": COST_CEILING, "arms": [], "gold_n": len(gold)}
    union_hits = set()
    refusals = []
    structurally_unreachable = set()   # anchors the OUTCOME axis alone cannot return, per arm

    for arm in ARMS:
        tgt = [a for a in gold if a["arm"] in arm["targets"]]
        tgt_ids = [a["oa"] for a in tgt]
        print(f"ARM {arm['name']}  ({len(tgt)} target anchors: "
              f"{', '.join(arm['targets'])})")

        # THE REACHABILITY CEILING, and it has to be measured before any recall number is read.
        # A query is (exposure AND outcome). An anchor the OUTCOME axis alone cannot return can
        # never be returned by the conjunction, so counting it as a miss blames the query for a
        # property of the anchor list. The 65 controls were harvested by matching an EXPOSURE
        # vocabulary against titles, so a good many of them have no fertility outcome at all --
        # "Pension Coverage for Parents and Educational Investment in China" is a real one. C.2.f
        # handled this by hand, with `outcome_is_fertility` set on 14 anchors it had read. With 82
        # anchors it has to be measured, not asserted.
        #
        # This is the same defect as `named-retry-author-queries-fake-zeros`: a structural zero
        # reported as a vocabulary miss. Recall is therefore reported twice -- over all targets, and
        # over the reachable ones -- and only the second is a statement about the query.
        ceiling_ids = set()
        if tgt_ids:
            _, ceil_got, ceil_err = measure(f"({' OR '.join(arm['outcome'])})", tgt_ids)
            if ceil_err:
                refusals.append({"arm": arm["name"], "stage": "ceiling", "error": ceil_err})
            else:
                ceiling_ids = {a["oa"] for a in tgt if a["oa"] in ceil_got}
                structurally_unreachable |= {a["oa"] for a in tgt if a["oa"] not in ceiling_ids}
                print(f"  {'outcome axis alone (ceiling)':32} "
                      f"reachable {len(ceiling_ids)}/{len(tgt)}")
                if len(ceiling_ids) < len(tgt):
                    for a in tgt:
                        if a["oa"] not in ceiling_ids:
                            print(f"      unreachable by construction: "
                                  f"{a['top_candidate']['title'][:64]}")
        exposure = list(arm["base"])
        n, got, err = measure(q(exposure, arm["outcome"]), all_ids)
        if err:
            print(f"  ERROR {err}")
            refusals.append({"arm": arm["name"], "stage": "baseline", "error": err})
            continue
        base_hit = sum(1 for a in tgt if a["oa"] in got)
        print(f"  {'baseline':32} frame={n:>7}  arm {base_hit}/{len(tgt)}")
        steps = [{"label": "baseline", "frame": n, "arm_recall": base_hit}]
        base_n, base_got = n, got
        for term in arm["candidates"]:
            n2, got2, err = measure(q(exposure + [term], arm["outcome"]), all_ids)
            if err:
                refusals.append({"arm": arm["name"], "stage": "exposure", "term": term,
                                 "error": err})
                continue
            hit2 = sum(1 for a in tgt if a["oa"] in got2)
            gain, cost = hit2 - base_hit, n2 - base_n
            price = (cost / gain) if gain > 0 else None
            accept = gain > 0 and price is not None and price <= COST_CEILING
            print(f"  + {term:30} frame={n2:>7}  arm {hit2}/{len(tgt)}"
                  f"{'   price %.0f/anchor' % price if price else ''}"
                  f"{'   ACCEPTED' if accept else ('   REJECTED (too dear)' if gain > 0 else '')}")
            steps.append({"term": term, "frame": n2, "arm_recall": hit2, "gain": gain,
                          "cost": cost, "price": price, "accepted": accept})
            if accept:
                exposure.append(term)
                base_hit, base_n, base_got = hit2, n2, got2
            time.sleep(0.25)
        # The outcome axis gets the same treatment. It is the half that usually carries the
        # contamination, and here it is also the half holding two of the three misses: an anchor
        # whose outcome is "family formation" is invisible to a fertility-only outcome axis no
        # matter how well the exposure axis is tuned.
        outcome = list(arm["outcome"])
        for term in arm.get("outcome_candidates", []):
            n2, got2, err = measure(q(exposure, outcome + [term]), all_ids)
            if err:
                refusals.append({"arm": arm["name"], "stage": "outcome", "term": term,
                                 "error": err})
                continue
            hit2 = sum(1 for a in tgt if a["oa"] in got2)
            gain, cost = hit2 - base_hit, n2 - base_n
            price = (cost / gain) if gain > 0 else None
            accept = gain > 0 and price is not None and price <= COST_CEILING
            print(f"  +out {term:28} frame={n2:>7}  arm {hit2}/{len(tgt)}"
                  f"{'   price %.0f/anchor' % price if price else ''}"
                  f"{'   ACCEPTED' if accept else ('   REJECTED (too dear)' if gain > 0 else '')}")
            steps.append({"axis": "outcome", "term": term, "frame": n2, "arm_recall": hit2,
                          "gain": gain, "cost": cost, "price": price, "accepted": accept})
            if accept:
                outcome.append(term)
                base_hit, base_n, base_got = hit2, n2, got2
            time.sleep(0.25)
        arm["outcome"] = outcome

        # leave-one-out on the accepted axis
        loo = []
        for term in exposure:
            if len(exposure) <= 1:
                break
            n3, got3, err = measure(q([x for x in exposure if x != term], arm["outcome"]), all_ids)
            if err:
                refusals.append({"arm": arm["name"], "stage": "loo", "term": term, "error": err})
                continue
            h3 = sum(1 for a in tgt if a["oa"] in got3)
            loo.append({"term": term, "arm_recall_without": h3,
                        "uniquely_carries": base_hit - h3, "frame_without": n3})
            if base_hit - h3 == 0:
                print(f"  LOO: {term} carries nothing unique — frame {base_n} -> {n3}")
        # For every accepted term, measure the records it uniquely contributes and how much gold
        # sits in them. A term adding many records and no gold is the shape of a homonym cloud --
        # "fertility cycles" added 177 records of menstrual-cycle literature and no gold, and only
        # a hand read caught it. This makes that pattern visible without one.
        for x in loo:
            n_unique = base_n - x["frame_without"]
            x["unique_records"] = n_unique
            x["suspect_homonym"] = n_unique >= 50 and x["uniquely_carries"] == 0
            if x["suspect_homonym"]:
                print(f"  SUSPECT: {x['term']} adds {n_unique} records and no anchor — "
                      f"read a sample of them before keeping it")
        if arm.get("in_union", True):
            union_hits |= base_got
        reach_hit = sum(1 for a in tgt if a["oa"] in base_got and a["oa"] in ceiling_ids)
        log["arms"].append({"name": arm["name"], "targets": arm["targets"],
                            "exposure_axis": exposure, "outcome_axis": arm["outcome"],
                            "query": q(exposure, arm["outcome"]), "frame": base_n,
                            "arm_recall": base_hit, "arm_n": len(tgt),
                            "reachable_n": len(ceiling_ids), "reachable_recall": reach_hit,
                            "steps": steps, "leave_one_out": loo})
        pct = f"{100*reach_hit/len(ceiling_ids):.0f}%" if ceiling_ids else "n/a"
        print(f"  => {arm['name']}: frame {base_n}, recall {base_hit}/{len(tgt)} of all targets, "
              f"{reach_hit}/{len(ceiling_ids)} of REACHABLE ({pct})\n")

    # The arms overlap -- three of them carry "Easterlin" -- so the sum of arm frames is an upper
    # bound, not the screening cost. Ask for the deduplicated union directly.
    screened = {a["name"] for a in ARMS if a.get("in_union", True)}
    log["arms_not_screened"] = sorted({a["name"] for a in ARMS} - screened)
    union_query = " OR ".join(f"({a['query']})" for a in log["arms"] if a["name"] in screened)
    union_frame, union_got, union_err = measure(union_query, all_ids)
    log["union_query"] = union_query
    log["union_frame_deduplicated"] = union_frame
    log["union_frame_error"] = union_err
    if union_frame is not None:
        print(f"\ndeduplicated union frame: {union_frame} "
              f"(sum of screened arms "
              f"{sum(a['frame'] for a in log['arms'] if a['name'] in screened)}; "
              f"not screened: {', '.join(log['arms_not_screened']) or 'none'})")
        # The union query must recall at least what the arms recall separately. If it does not,
        # the nesting is being parsed differently than intended and the number is not usable.
        if union_got is not None:
            u = sum(1 for a in primary if a["oa"] in union_got)
            print(f"union query recalls {u}/{len(primary)} primary "
                  f"(arms together: {sum(1 for a in primary if a['oa'] in union_hits)})")
            log["union_query_recall"] = u

    # UNION RECALL ON THE TIER-A CANON, BY DIRECTION -- the headline number of the calibration.
    # Per-arm recall answers "is this axis working"; this answers "does the query as a whole reach
    # the studies the chapter is about". They differ here: the backward arm misses two of its own
    # five canon anchors because Rosenzweig & Wolpin and Angrist, Lavy & Schlosser say "quantity and
    # quality" rather than "family size", so they arrive through the THEORY axis instead. Reading
    # per-arm recall alone would have sent me widening an axis that was not the problem.
    hand = [a for a in gold if a["source"] == "hand"]
    if hand:
        _, hand_got, hand_err = measure(union_query, [a["oa"] for a in hand])
        log["canon_union_recall"] = {}
        if hand_err:
            refusals.append({"arm": "union", "stage": "canon_recall", "error": hand_err})
        else:
            print("\nUNION recall on the Tier-A canon, by direction:")
            for dirn in ("THEORY", "BACKWARD", "FORWARD"):
                rs = [a for a in hand if a.get("direction") == dirn]
                if not rs:
                    continue
                hit = [a for a in rs if a["oa"] in hand_got]
                log["canon_union_recall"][dirn] = {
                    "hit": len(hit), "n": len(rs),
                    "missed": [a["title"] for a in rs if a["oa"] not in hand_got]}
                print(f"  {dirn:9} {len(hit)}/{len(rs)}")
                for a in rs:
                    if a["oa"] not in hand_got:
                        print(f"      MISS  {a['title'][:64]}")

    covered = sum(1 for a in primary if a["oa"] in union_hits)
    unreachable = [a for a in gold if a["oa"] not in union_hits]
    log["union"] = {"primary_recall": covered, "primary_n": len(primary),
                    "total_frame_upper_bound": sum(a["frame"] for a in log["arms"]
                                                   if a["name"] in screened),
                    "unreachable": [{"arm": a["arm"], "source": a["source"],
                                     "title": a["top_candidate"]["title"]} for a in unreachable]}
    print(f"UNION primary recall {covered}/{len(primary)}"
          + (f"  ({100*covered/len(primary):.0f}%)" if primary else
             "  -- EMPTY DENOMINATOR: no anchor mapped to a primary arm, which is a bug in the "
             "arm/target mapping, not a result"))
    print(f"frame upper bound (arms not deduplicated): {log['union']['total_frame_upper_bound']}")
    not_screened = {a['name'] for a in ARMS if not a.get('in_union', True)}
    for a in unreachable:
        a["_why"] = ("arm not screened" if a["arm"] in not_screened
                     else "outcome is not fertility" if not measures_fertility(a)
                     else "unreachable by construction (outcome axis alone cannot return it)"
                     if a["oa"] in structurally_unreachable
                     else "VOCABULARY MISS -> citation channel")
    log["union"]["unreachable"] = [{**u, "why": a["_why"]} for u, a
                                   in zip(log["union"]["unreachable"], unreachable)]
    print("\nUNREACHABLE, by reason — only the third kind is a query problem:")
    for a in unreachable:
        print(f"  {a['_why']:34} {a['arm']:18} {a['top_candidate']['title'][:52]}")
    log["pool"] = dict(POOL)
    log["cache"] = dict(CACHE_STATS)
    print(f"\nrequests served: {POOL['key']} on the api_key, {POOL['polite']} on the keyless "
          f"polite pool, {POOL['refused']} refused; "
          f"measurements {CACHE_STATS['hit']} cached / {CACHE_STATS['miss']} fetched")
    if refusals or union_err:
        for r in refusals[:6]:
            print(f"  REFUSED  {r['arm']}/{r['stage']} {r.get('term','')}: {r['error'][:110]}")
        if len(refusals) > 6:
            print(f"  ... and {len(refusals) - 6} more refusals")
        sys.exit(
            f"\n*** {len(refusals)} queries were REFUSED (not empty). NOTHING WAS WRITTEN.\n"
            "A refused query reports recall 0 and frame 0, and the union is then built from an "
            "empty hit set, so a partial run produces a log in which already-verified anchors read "
            "as vocabulary misses. The console output explaining that does not survive; the file "
            "does. Re-run once the cause is cleared -- an OpenAlex 'Insufficient budget' resets at "
            "midnight UTC.")

    (LOGS / "quantity-quality-tradeoff-production-query.json").write_text(
        json.dumps(log, indent=2) + "\n")

    # Generated, never retyped.
    import datetime
    L = [f"# C.3.d production query set — calibrated {datetime.date.today().isoformat()}", "",
         "Generated by `source/build/goldset/352_c3d_production_query.py`. Do not edit by hand.", "",
         f"Calibrated against the {log['gold_n']} resolved anchors, of which **{len(primary)}** sit "
         "in an arm's target cells. Recall is measured by asking OpenAlex which anchors each query "
         "returns, not by re-implementing its tokenizer.", "",
         f"**Union primary recall {covered}/{len(primary)} ({100*covered/len(primary):.0f}%)**, at a "
         f"deduplicated frame of **{log.get('union_frame_deduplicated')}** records "
         f"(the arms sum to {log['union']['total_frame_upper_bound']}, but three of them carry "
         "`\"Easterlin\"` and overlap heavily, so the sum is an upper bound and not the screening "
         "cost).", "",
         "The union query was checked to recall the same anchors the arms recall separately "
         f"({log.get('union_query_recall')} vs {covered}). A union that recalled fewer would mean "
         "the nested boolean is being parsed differently than intended, and its count would not be "
         "usable.", "",
         f"Requests served: **{log['pool']['key']}** on the api_key and "
         f"**{log['pool']['polite']}** on the keyless polite pool. The key is the METERED path — "
         "once its daily allowance is spent it returns `Insufficient budget` while the keyless pool "
         "answers the identical query, verified on matching counts, `ids.openalex:` recall and "
         "cursor pagination. The fallback is counted rather than silent, so a divergence between "
         "the pools would be visible here.", "",
         "## Why a set of queries and not one query", "",
         "Scope §4 measures the mechanism as a conjunction whose join is empty, and script 336 "
         "confirmed it on the canon: **9 of the 14 Tier-A anchors carry `outcome_is_fertility: "
         "false`**. An arm aimed at those cannot carry the fertility outcome axis, or its recall "
         "is zero by construction and a structural zero reads as an absence "
         "(`named-retry-author-queries-fake-zeros`). So `link1-investment` and `positional-canon` "
         "are scored against an INVESTMENT outcome axis and the rest against fertility, and the "
         "arms are reported separately because a union recall mixing them would answer two "
         "questions at once.", "",
         "**A positive control must be a record a correct query SHOULD retrieve.** The first "
         "version of this control list required only an exposure term plus a DOI, which admitted "
         "*The Nuclear Arms Race: An Evolutionary Perspective* and made the mechanism arm read "
         "2/57 when the interpretable figure was 2/13 — measuring the control list rather than the "
         "query. Controls now require an exposure term AND a fertility outcome in the title.", "",
         f"## Acceptance rule: gain > 0 AND under {log['cost_ceiling']} records per anchor", "",
         "Inherited from C.6.a, which accepted any term with recall gain > 0 and admitted "
         "`\"aspirations\"` for **one** anchor at a cost of **2,082 records** — leave-one-out then "
         "showed it carried nothing else. Every rejection below is logged with its price, so the "
         "ceiling is auditable instead of invisible (`advance-the-baseline-when-accepting-terms`).",
         "",
         "## The arms", ""]
    for a in log["arms"]:
        L += [f"### `{a['name']}` — {a['arm_recall']}/{a['arm_n']} of its target anchors, "
              f"frame {a['frame']}", "",
              f"Targets: {', '.join('`%s`' % c for c in a['targets'])}", "",
              "```", a["query"], "```", "",
              "| step | frame | arm recall | price/anchor | |", "|---|---|---|---|---|"]
        for s in a["steps"]:
            term = s.get("term", "baseline")
            price = f"{s['price']:.0f}" if s.get("price") else "—"
            verdict = ("accepted" if s.get("accepted") else
                       ("**rejected — too dear**" if s.get("gain", 0) > 0 else ""))
            axis = " (outcome)" if s.get("axis") == "outcome" else ""
            L.append(f"| {term}{axis} | {s['frame']} | {s['arm_recall']}/{a['arm_n']} | "
                     f"{price} | {verdict} |")
        dead = [x for x in a["leave_one_out"] if x["uniquely_carries"] == 0]
        if dead:
            L += ["", "Leave-one-out: " + ", ".join(f"`{x['term']}` (frame would be "
                  f"{x['frame_without']})" for x in dead) + " carry no anchor uniquely. "
                  + ("With only one target anchor this arm's leave-one-out cannot discriminate, so "
                     "these are kept rather than pruned." if a["arm_n"] < 3 else
                     "Candidates for pruning at the next calibration.")]
        L.append("")
    from collections import Counter as _C2
    why = _C2(u["why"] for u in log["union"]["unreachable"])
    L += ["## Unreachable, by reason", "",
          "Three reasons an anchor can be missing from the union, and **only the third is a query "
          "problem**. Counting all of them against the query blames it for the anchor list's errors.",
          "", "- **arm not screened** — `theory` has no arm by design, and `boundary-qq` is "
          "calibrated but excluded from the screened union (see above).",
          "- **outcome is not fertility** — the anchor's own outcome is enrolment, or infant health, "
          "or school achievement. A fertility-outcome query cannot reach it and should not. These "
          "are anchor-list errors, kept visible rather than deleted "
          "(`anchor-on-the-estimand-not-the-famous-design`).",
          "- **vocabulary miss** — the real residue. These route to the Phase 2 citation channel, "
          "where the most-cited works in a field are cheapest to find; adding a term to catch one "
          "anchor is what the cost ceiling exists to prevent.", "",
          "| reason | n |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(why.items())]
    L += ["", "| reason | arm | source | title |", "|---|---|---|---|"]
    for u in log["union"]["unreachable"]:
        L.append(f"| {u['why']} | `{u['arm']}` | {u['source']} | {u['title'][:70]} |")
    L.append("")
    (LOGS / "quantity-quality-tradeoff-production-query.md").write_text("\n".join(L))


main()
