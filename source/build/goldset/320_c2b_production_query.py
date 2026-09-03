#!/usr/bin/env python3
"""320 — C.2.b production query SET, calibrated against the 32 resolved anchors (TICK-079).

Why a set and not a query
-------------------------
Ported from C.6.a's 308, which learned this the expensive way: one exposure axis calibrated against
all primary anchors plateaued at 15/21 with the misses clustered by arm, because they were not
written in the vocabulary that axis was made of.

C.2.b needs the set for a reason of its own, recorded in scope §16.1. The fee-abolition literature
(scope §7 row 1) is indexed in a policy-evaluation vocabulary — "user fees", "fee abolition",
"tuition-free" — which shares almost nothing with the economics-of-fertility vocabulary that reaches
the cost-of-children literature. That is `policy-literatures-indexed-in-local-vocabulary`, worth +40%
of A.23's frame. A single axis cannot hold both.

**Two arms exist to SEPARATE, not to include.** Scope §16.1: the free-seed harvest found that 17 of
130 records are C.2.e's time-cost / child-penalty literature — 11 of the 33 returned by "cost of
children" and 5 of the 6 returned by "cost of childbearing". The hypothesis's own name is the
neighbour's name, so the separation has to happen on the exposure axis and cannot be deferred to the
screen. `boundary-timecost` and `boundary-qq` are calibrated so that cloud is identifiable and
taggable rather than silently mixed into the primary cells. Their frames are reported separately, and
the union is reported both with and without them so the cost of carrying them is visible.

Acceptance rule
---------------
The first version accepted any term with recall gain > 0. That let `"aspirations"` in for **one**
anchor at a cost of **2,082 records** — a 2,082:1 price, and the leave-one-out then showed the term
carried nothing else. Acceptance is now gain > 0 AND cost-per-anchor under a stated ceiling, and
every rejection is logged with its price so the ceiling is auditable rather than invisible.

Recall is measured by asking OpenAlex which anchors a query returns (`ids.openalex:` alongside the
search filter), never by re-implementing its tokenizer locally.

Usage: python3 source/build/goldset/320_c2b_production_query.py
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

# Arms are keyed on the `arm` field of the anchor list, so every anchor is somebody's target or is
# explicitly expected to be unreachable. `theory` anchors have no arm on purpose: a query that
# retrieved the theoretical literature well would be retrieving the wrong literature, and C.6.a's
# LINK1_LABOUR anchors played the same role.
PRIMARY_ARMS = {"direct-cost", "school-fee", "health-price", "anticipated-cost"}

ARMS = [
    {"name": "direct-cost", "targets": ["direct-cost"],
     "base": ['"cost of children"', '"price of children"'], "outcome": OUTCOME,
     "candidates": ['"cost of raising children"', '"child costs"', '"cost of a child"',
                    '"child rearing costs"', '"direct costs of children"',
                    '"economic cost of children"', '"cost of childrearing"',
                    '"price of a child"', '"net price"'],
     "outcome_candidates": ['"desired family size"', '"ideal family size"',
                            '"completed fertility"', '"first birth"']},
    # The policy-evaluation vocabulary. This is scope §7's second channel and the reason the query
    # is a set: none of these terms appears in the economics-of-fertility arm above.
    {"name": "school-fee", "targets": ["school-fee"],
     "base": ['"school fees"', '"free primary education"'], "outcome": OUTCOME,
     "candidates": ['"user fees"', '"fee abolition"', '"tuition-free"', '"cost of schooling"',
                    '"universal primary education"', '"school costs"', '"education costs"'],
     "outcome_candidates": ['"family planning"', '"age at first birth"', '"birth spacing"']},
    # UNCALIBRATED, and labelled as such. Its only anchor was Currie and Gruber, whose outcome is
    # infant mortality and birth weight rather than fertility, so this arm has no valid anchor and
    # its recall CANNOT be measured. It is kept narrow and kept in the union anyway, because scope
    # §7 row 3 registers child health-insurance expansion as admissible variation and an arm that
    # does not exist would turn a vocabulary gap into a finding of no evidence
    # (`empty-cell-needs-second-channel`). The first version of this arm was '"Medicaid"' OR
    # '"health insurance"': 2,865 records for zero anchors, with leave-one-out reporting both base
    # terms as carrying nothing.
    {"name": "health-price", "targets": ["health-price"], "uncalibrated": True,
     "base": ['"child health insurance"', '"health insurance expansion"', '"maternity care fees"',
              '"delivery fees"'], "outcome": OUTCOME,
     "candidates": ['"out-of-pocket health"'],
     "outcome_candidates": []},
    # Scope §7 row 8: the anticipated FUTURE cost of a child. The free-seed harvest measured
    # `tuition` at roughly 13% on topic unrestricted; the outcome axis is what has to clean it up,
    # and if it does not, the arm is not worth its frame.
    {"name": "anticipated-cost", "targets": ["anticipated-cost"],
     "base": ['"tuition"'], "outcome": OUTCOME,
     "candidates": ['"college costs"', '"cost of higher education"', '"expected costs"',
                    '"anticipated costs"'],
     "outcome_candidates": ['"fertility intentions"', '"first birth"']},
    # Exposure MEASUREMENT, not effect (scope §9). Retrieved because §5's index needs it and because
    # a chapter that cannot see its own measurement literature cannot say what its exposure is.
    {"name": "measurement", "targets": ["measurement"],
     "base": ['"equivalence scale"', '"expenditures on children"'], "outcome": OUTCOME,
     "candidates": ['"parental spending"', '"child expenditure"', '"consumer expenditure"',
                    '"cost of children"', '"household expenditure"'],
     "outcome_candidates": ['"family size"']},
    # ---- the two separation arms. These exist so Wall 4 and Wall 1 are taggable, not includable.
    {"name": "boundary-timecost", "targets": ["boundary-timecost"],
     "base": ['"career costs of children"', '"child penalty"'], "outcome": OUTCOME,
     "candidates": ['"opportunity cost of time"', '"time costs"', '"motherhood penalty"',
                    '"forgone earnings"', '"cost of childbearing"'],
     "outcome_candidates": ['"labor supply"']},
    # Reported but NOT screened. §16.1's separation requirement is specific to Wall 4: the
    # time-cost literature shares this chapter's own name, so it must be separated on the exposure
    # axis. Quantity-quality vocabulary shares nothing with "cost of children", so a QQ paper will
    # not arrive in the primary arms and does not need to be retrieved to be kept out. 683 records
    # is too dear for a wall that does not leak.
    {"name": "boundary-qq", "targets": ["boundary-qq"], "in_union": False,
     "base": ['"quantity-quality"', '"child quality"'], "outcome": OUTCOME,
     "candidates": ['"quantity quality tradeoff"', '"child investment"', '"sibsize"',
                    '"human capital of children"'],
     "outcome_candidates": ['"family size"']},
]


def q(exposure, outcome):
    return f"({' OR '.join(exposure)}) AND ({' OR '.join(outcome)})"


def call(params):
    args = ["curl", "-sS", "--max-time", "120", "-G", "https://api.openalex.org/works"]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, f"non-JSON: {r.stdout[:160]}"
    if "meta" not in d or d["meta"].get("count") is None:
        return None, f"query refused (NOT an empty literature): {json.dumps(d)[:200]}"
    return d, None


def measure(query, ids):
    d, err = call({"filter": f"title_and_abstract.search:{query}", "per-page": "1"})
    if err:
        return None, None, err
    n = d["meta"]["count"]
    d2, err = call({"filter": f"ids.openalex:{'|'.join(ids)},title_and_abstract.search:{query}",
                    "per-page": "200", "select": "id"})
    if err:
        return n, None, err
    return n, {w["id"].rsplit("/", 1)[-1] for w in d2.get("results", [])}, None


def main():
    anchors = json.loads((LOGS / "child-cost-direct-cold-start-anchors.json").read_text())
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

    (LOGS / "child-cost-direct-production-query.json").write_text(
        json.dumps(log, indent=2) + "\n")

    # Generated, never retyped.
    L = ["# C.2.b production query set — calibrated 2026-09-03", "",
         "Generated by `source/build/goldset/308_c6a_production_query.py`. Do not edit by hand.", "",
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
         "## Why a set of queries and not one query", "",
         "The fee-abolition literature is indexed in a policy-evaluation vocabulary — \"user "
         "fees\", \"fee abolition\", \"tuition-free\" — that shares almost nothing with the "
         "economics-of-fertility vocabulary reaching the cost-of-children literature. One axis "
         "cannot hold both (`policy-literatures-indexed-in-local-vocabulary`).", "",
         "**Two arms exist to separate, not to include.** Scope §16.1: the free-seed harvest found "
         "17 of 130 records are C.2.e's time-cost / child-penalty literature, including 11 of the 33 "
         "returned by \"cost of children\" and 5 of the 6 returned by \"cost of childbearing\". "
         "The hypothesis's own name is the neighbour's name, so the separation has to happen on the "
         "exposure axis. `boundary-timecost` and `boundary-qq` make that cloud taggable; their "
         "frames are reported separately below.", "",
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
    (LOGS / "child-cost-direct-production-query.md").write_text("\n".join(L))


main()
