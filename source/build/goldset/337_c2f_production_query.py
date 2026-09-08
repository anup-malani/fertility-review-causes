#!/usr/bin/env python3
"""337 — C.2.f production query SET, calibrated against the resolved anchors (TICK-081).

Ported from C.2.b's 320 (itself C.6.a's 308). The machinery -- per-term leave-one-out, a cost
ceiling per additional anchor recalled, recall measured by asking OpenAlex which anchors a query
returns rather than re-implementing its tokenizer -- is carried over unchanged.

Why a SET, and the reason is specific to this chapter
----------------------------------------------------
Scope §4 measured the mechanism as a conjunction whose join is empty: inequality -> required
investment per child -> fertility returns ~2 records, while each outer link has a substantial
literature. Script 336 then confirmed it on the canon -- **9 of the 14 Tier-A hand anchors carry
`outcome_is_fertility: false`**: Ramey & Ramey, Kornrich & Furstenberg, Schneider et al., Frank's
*Expenditure Cascades*, and all four positional monographs.

**That fact dictates the arm design.** An arm targeting those nine CANNOT carry the fertility outcome
axis: its recall would be zero by construction, and a structural zero read as an absence is the
`named-retry-author-queries-fake-zeros` failure. So `link1-investment` and `positional-canon` get an
INVESTMENT outcome axis instead, and the `dispersion`/`fertility` arms keep the fertility one. The
arms are then reported separately, because a union recall number that mixes them would be measuring
two different questions.

Scope §3's two measured corrections are built in from the start: the distribution statistics the
2026-09-03 axis omitted entirely (`"Gini"` alone is 288 inside the frame) and `"credential
inflation"` (~205 against `"educational arms race"`'s 16).

Acceptance rule
---------------
Gain > 0 AND cost-per-anchor under COST_CEILING, every rejection logged with its price. A frozen
baseline would credit later terms with earlier ones' gold, so the baseline advances as terms are
accepted (`advance-the-baseline-when-accepting-terms`).

Usage: python3 source/build/goldset/337_c2f_production_query.py
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

OUTCOME = ['"fertility"', '"childbearing"', '"birth rate"', '"total fertility rate"',
           '"family size"', '"number of children"']

# The second outcome axis. Scope §4 and script 336: nine of fourteen canon anchors do not measure
# fertility at all, so an arm aimed at them must be scored against the INVESTMENT outcome or its
# recall is a structural zero rather than a measurement.
OUTCOME_INVEST = ['"parental investment"', '"child investment"', '"investment in children"',
                  '"educational spending"', '"parental spending"', '"educational investment"']

# Only the arms whose outcome IS fertility can populate a primary cell. The link-1 and positional
# arms are retrieved to size the mechanism literature and to feed the snowball, never to be counted
# as evidence on the demographic question.
PRIMARY_ARMS = {"dispersion", "fertility", "mechanism"}

ARMS = [
    # The general exposure axis. Scope §3 measured "income inequality" carrying 635 of a 716-record
    # frame, so this arm is expected to be large and mostly off-target; it is here because the
    # identified designs, if any exist, are written in it.
    {"name": "dispersion", "targets": ["inequality-general", "fertility"],
     "base": ['"income inequality"', '"Gini"'], "outcome": OUTCOME,
     "candidates": ['"top income share"', '"income concentration"', '"wage dispersion"',
                    '"earnings inequality"', '"income dispersion"', '"income distribution"',
                    '"90/10 ratio"', '"top 1 percent"'],
     "outcome_candidates": ['"completed fertility"', '"desired family size"',
                            '"fertility intentions"', '"first birth"']},
    # The mechanism vocabulary. Scope §3: these six terms return 83 records BETWEEN them inside the
    # frame, against 635 for the general term. Small is the expected result, not a failure.
    {"name": "mechanism", "targets": ["mechanism"],
     "base": ['"status competition"', '"relative status"'], "outcome": OUTCOME,
     "candidates": ['"positional good"', '"positional externality"', '"social comparison"',
                    '"conspicuous consumption"', '"relative deprivation"', '"status anxiety"',
                    '"positional competition"', '"reproductive competition"'],
     "outcome_candidates": ['"desired family size"', '"fertility intentions"']},
    # Scope §7's SECOND CHANNEL, and it is a different literature's local vocabulary
    # (`policy-literatures-indexed-in-local-vocabulary`, worth +40% of A.23's frame). Scored on the
    # INVESTMENT outcome: these anchors do not measure fertility.
    {"name": "link1-investment", "targets": ["link1-investment"], "outcome": OUTCOME_INVEST,
     "base": ['"shadow education"', '"private tutoring"'],
     "candidates": ['"cram school"', '"credential inflation"', '"educational arms race"',
                    '"enrichment activities"', '"extracurricular"', '"supplementary education"',
                    '"double reduction"'],
     "outcome_candidates": ['"educational expenditure"', '"human capital investment"']},
    # The positional monograph canon -- Hirsch, Frank, Schor, Veblen. Also INVESTMENT-scored.
    {"name": "positional-canon", "targets": ["positional-canon"], "outcome": OUTCOME_INVEST,
     "base": ['"positional good"', '"conspicuous consumption"'],
     "candidates": ['"social limits"', '"expenditure cascade"', '"keeping up with the Joneses"',
                    '"rat race"', '"arms race"', '"status signaling"'],
     "outcome_candidates": ['"consumption"', '"household spending"']},
    # Wall 1's separation arm. Scope §8 measured C.3.d contamination at 8 records inside the frame,
    # and scope §4 records link 2 as C.3.d's chapter rather than this one's. Retrieved so the wall is
    # TAGGABLE, and kept out of the union: 683 records is too dear for a wall that does not leak.
    {"name": "c3d-boundary", "targets": ["c3d-boundary"], "in_union": False,
     "base": ['"quantity-quality"', '"child quality"'], "outcome": OUTCOME,
     "candidates": ['"quantity quality tradeoff"', '"sibsize"', '"human capital of children"'],
     "outcome_candidates": ['"family size"']},
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


CACHE_PATH = LOGS / ".cache" / "c2f-query-measurements.json"


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
    anchors = json.loads((LOGS / "rising-inequality-and-status-competition-cold-start-anchors.json").read_text())
    gold = [a for a in anchors
            if a["verdict"] in MATCHED and (a.get("top_candidate") or {}).get("oa_id")]
    for a in gold:
        a["oa"] = a["top_candidate"]["oa_id"].rsplit("/", 1)[-1]
    all_ids = [a["oa"] for a in gold]
    primary_all = [a for a in gold if a["arm"] in PRIMARY_ARMS]
    # An anchor whose own outcome is not fertility cannot be recalled by a query with a fertility
    # outcome axis, and counting it as a miss would blame the query for the anchor list's error.
    primary = [a for a in primary_all if a.get("outcome_is_fertility", True)]
    excluded = [a for a in primary_all if not a.get("outcome_is_fertility", True)]
    print(f"gold {len(gold)} anchors; {len(primary_all)} in a PRIMARY arm, of which {len(primary)} "
          f"measure fertility and {len(excluded)} do not:")
    for a in excluded:
        print(f"    STRUCTURALLY EXCLUDED  {a['title'][:60]} — {a.get('outcome_note','')}")
    print()

    log = {"cost_ceiling": COST_CEILING, "arms": [], "gold_n": len(gold)}
    union_hits = set()
    refusals = []

    for arm in ARMS:
        tgt = [a for a in gold if a["arm"] in arm["targets"]]
        tgt_ids = [a["oa"] for a in tgt]
        print(f"ARM {arm['name']}  ({len(tgt)} target anchors: "
              f"{', '.join(arm['targets'])})")
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
        log["arms"].append({"name": arm["name"], "targets": arm["targets"],
                            "exposure_axis": exposure, "outcome_axis": arm["outcome"],
                            "query": q(exposure, arm["outcome"]), "frame": base_n,
                            "arm_recall": base_hit, "arm_n": len(tgt),
                            "steps": steps, "leave_one_out": loo})
        print(f"  => {arm['name']}: frame {base_n}, arm recall {base_hit}/{len(tgt)}\n")

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

    covered = sum(1 for a in primary if a["oa"] in union_hits)
    unreachable = [a for a in gold if a["oa"] not in union_hits]
    log["union"] = {"primary_recall": covered, "primary_n": len(primary),
                    "total_frame_upper_bound": sum(a["frame"] for a in log["arms"]
                                                   if a["name"] in screened),
                    "unreachable": [{"arm": a["arm"], "source": a["source"],
                                     "title": a["top_candidate"]["title"]} for a in unreachable]}
    print(f"UNION primary recall {covered}/{len(primary)}  "
          f"({100*covered/len(primary):.0f}%)")
    print(f"frame upper bound (arms not deduplicated): {log['union']['total_frame_upper_bound']}")
    not_screened = {a["name"] for a in ARMS if not a.get("in_union", True)} | {"theory"}
    for a in unreachable:
        a["_why"] = ("arm not screened" if a["arm"] in not_screened
                     else "outcome is not fertility" if not a.get("outcome_is_fertility", True)
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

    (LOGS / "rising-inequality-and-status-competition-production-query.json").write_text(
        json.dumps(log, indent=2) + "\n")

    # Generated, never retyped.
    import datetime
    L = [f"# C.2.f production query set — calibrated {datetime.date.today().isoformat()}", "",
         "Generated by `source/build/goldset/337_c2f_production_query.py`. Do not edit by hand.", "",
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
    (LOGS / "rising-inequality-and-status-competition-production-query.md").write_text("\n".join(L))


main()
