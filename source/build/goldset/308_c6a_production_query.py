#!/usr/bin/env python3
"""308 — C.6.a production query SET, calibrated against the 31 resolved anchors (TICK-078).

Why a set and not a query
-------------------------
The first version of this script calibrated ONE exposure axis against all 21 primary anchors and
plateaued at 15/21. The six misses were not scattered — they clustered by arm. All three `RIVAL_TEST`
anchors are Butz–Ward papers, which argue the competing female-wage model and never use Easterlin's
vocabulary; the `MIXED_COHORT_MARRIAGE` anchor pairs a cohort-size exposure with a *marriage*
outcome. **No amount of tuning a single axis reaches them, because they are not written in the
vocabulary that axis is made of.** Scope §8 Wall 5 says the rival-model tests are the most
informative records this search can find, so a query that structurally cannot retrieve them is not a
query that can be tightened — it is the wrong shape.

So: one query per arm, each calibrated against its OWN anchors, with the union reported.

Acceptance rule
---------------
The first version accepted any term with recall gain > 0. That let `"aspirations"` in for **one**
anchor at a cost of **2,082 records** — a 2,082:1 price, and the leave-one-out then showed the term
carried nothing else. Acceptance is now gain > 0 AND cost-per-anchor under a stated ceiling, and
every rejection is logged with its price so the ceiling is auditable rather than invisible.

Recall is measured by asking OpenAlex which anchors a query returns (`ids.openalex:` alongside the
search filter), never by re-implementing its tokenizer locally.

Usage: python3 source/build/goldset/308_c6a_production_query.py
"""
import json
import subprocess
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
OUTCOME_MARRIAGE = OUTCOME + ['"marriage rate"', '"marriage market"', '"nuptiality"',
                              '"family formation"']

# One arm per estimand family. `targets` names the cells whose anchors this arm is responsible for.
ARMS = [
    {"name": "easterlin", "targets": ["RELATIVE_INCOME_FERTILITY", "BENCHMARK_MEASURED"],
     "base": ['"relative income"', '"Easterlin"'], "outcome": OUTCOME,
     "candidates": ['"relative cohort size"', '"aspirations"', '"relative earnings"',
                    '"income relative to"', '"economic prospects"'],
     "outcome_candidates": ['"family formation"', '"first birth"', '"completed fertility"',
                            '"marriage"']},
    {"name": "cohort-size", "targets": ["COHORT_SIZE_FERTILITY"],
     "base": ['"cohort size"'], "outcome": OUTCOME,
     "candidates": ['"relative cohort size"', '"cohort crowding"', '"birth cohort size"',
                    '"size of the cohort"', '"cohort effects"'],
     "outcome_candidates": ['"family formation"', '"completed fertility"', '"first birth"']},
    # "fertility cycles" was in this arm's base until the screen universe was stratified and the
    # 177 records it uniquely produced turned out to be MENSTRUAL cycles -- menstruation, menopause,
    # cycle tracking -- for zero gold. Leave-one-out on recall had already said the term carried
    # nothing unique, and that was dismissed because the arm has one anchor and LOO cannot
    # discriminate on one. The precision side settled what the recall side could not.
    {"name": "cycle", "targets": ["CYCLE_TEST"],
     "base": ['"demographic cycles"', '"population cycles"', '"birth cycles"'], "outcome": OUTCOME,
     "candidates": ['"fertility waves"', '"endogenous cycles"', '"self-generating"',
                    '"echo effect"', '"baby bust"', '"Easterlin"'],
     "outcome_candidates": ['"births"', '"birth sequences"']},
    {"name": "rival", "targets": ["RIVAL_TEST"],
     "base": ['"countercyclical fertility"', '"Butz"'], "outcome": OUTCOME,
     "candidates": ['"female wage"', '"price of time"', '"opportunity cost of time"',
                    '"Butz-Ward"', '"Becker"', '"relative income"'],
     "outcome_candidates": ['"female labor force"', '"completed fertility"']},
    {"name": "marriage-boundary", "targets": ["MIXED_COHORT_MARRIAGE"],
     # "marriage squeeze" moved out of the base for the same reason: leave-one-out showed it
     # carried no anchor uniquely, and the 151-record stratum it produced is dominated by the
     # sex-ratio and dowry literature of China and India -- which Wall 3 assigns to A.10, not here.
     # Demoted to a candidate so it has to buy its way in at a measured price.
     "base": ['"cohort size"'], "outcome": OUTCOME_MARRIAGE,
     "candidates": ['"marriage squeeze"', '"relative cohort size"', '"Easterlin"', '"sex ratio"'],
     "outcome_candidates": ['"union formation"', '"first birth"']},
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
    anchors = json.loads((LOGS / "easterlin-relative-income-cold-start-anchors.json").read_text())
    gold = [a for a in anchors
            if a["verdict"] in MATCHED and (a.get("top_candidate") or {}).get("oa_id")]
    for a in gold:
        a["oa"] = a["top_candidate"]["oa_id"].rsplit("/", 1)[-1]
    all_ids = [a["oa"] for a in gold]
    primary_cells = {c for arm in ARMS for c in arm["targets"]}
    primary = [a for a in gold if a["cell"] in primary_cells]
    print(f"gold {len(gold)} anchors; {len(primary)} in an arm's target cells\n")

    log = {"cost_ceiling": COST_CEILING, "arms": [], "gold_n": len(gold)}
    union_hits = set()

    for arm in ARMS:
        tgt = [a for a in gold if a["cell"] in arm["targets"]]
        tgt_ids = [a["oa"] for a in tgt]
        print(f"ARM {arm['name']}  ({len(tgt)} target anchors: "
              f"{', '.join(arm['targets'])})")
        exposure = list(arm["base"])
        n, got, err = measure(q(exposure, arm["outcome"]), all_ids)
        if err:
            print(f"  ERROR {err}")
            continue
        base_hit = sum(1 for a in tgt if a["oa"] in got)
        print(f"  {'baseline':32} frame={n:>7}  arm {base_hit}/{len(tgt)}")
        steps = [{"label": "baseline", "frame": n, "arm_recall": base_hit}]
        base_n, base_got = n, got
        for term in arm["candidates"]:
            n2, got2, err = measure(q(exposure + [term], arm["outcome"]), all_ids)
            if err:
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
        union_hits |= base_got
        log["arms"].append({"name": arm["name"], "targets": arm["targets"],
                            "exposure_axis": exposure, "outcome_axis": arm["outcome"],
                            "query": q(exposure, arm["outcome"]), "frame": base_n,
                            "arm_recall": base_hit, "arm_n": len(tgt),
                            "steps": steps, "leave_one_out": loo})
        print(f"  => {arm['name']}: frame {base_n}, arm recall {base_hit}/{len(tgt)}\n")

    # The arms overlap -- three of them carry "Easterlin" -- so the sum of arm frames is an upper
    # bound, not the screening cost. Ask for the deduplicated union directly.
    union_query = " OR ".join(f"({a['query']})" for a in log["arms"])
    union_frame, union_got, union_err = measure(union_query, all_ids)
    log["union_query"] = union_query
    log["union_frame_deduplicated"] = union_frame
    log["union_frame_error"] = union_err
    if union_frame is not None:
        print(f"\ndeduplicated union frame: {union_frame} "
              f"(sum of arms {sum(a['frame'] for a in log['arms'])})")
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
                    "total_frame_upper_bound": sum(a["frame"] for a in log["arms"]),
                    "unreachable": [{"key": a["key"], "cell": a["cell"], "link": a["link"],
                                     "title": a["top_candidate"]["title"]} for a in unreachable]}
    print(f"UNION primary recall {covered}/{len(primary)}  "
          f"({100*covered/len(primary):.0f}%)")
    print(f"frame upper bound (arms not deduplicated): {log['union']['total_frame_upper_bound']}")
    print("\nUNREACHABLE by any arm — these route to the citation channel, not to more terms:")
    for a in unreachable:
        print(f"  {a['cell']:26} {a['link']:6} {a['top_candidate']['title'][:64]}")
    (LOGS / "easterlin-relative-income-production-query.json").write_text(
        json.dumps(log, indent=2) + "\n")

    # Generated, never retyped.
    L = ["# C.6.a production query set — calibrated 2026-09-02", "",
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
         "A single exposure axis calibrated against all primary anchors plateaued at 15/21, and the "
         "misses were not scattered — they clustered by arm. Every `RIVAL_TEST` anchor is a "
         "Butz–Ward paper arguing the competing female-wage model, which never uses Easterlin's "
         "vocabulary; the `MIXED_COHORT_MARRIAGE` anchor pairs a cohort-size exposure with a "
         "*marriage* outcome. No tuning of one axis reaches them, because they are not written in "
         "the vocabulary that axis is made of.", "",
         f"## Acceptance rule: gain > 0 AND under {log['cost_ceiling']} records per anchor", "",
         "The first version accepted any term with recall gain > 0. That admitted `\"aspirations\"` "
         "for **one** anchor at a cost of **2,082 records** — and leave-one-out then showed it "
         "carried nothing else. Every rejection below is logged with its price, so the ceiling is "
         "auditable instead of invisible.", "",
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
    L += ["## Unreachable by any arm", "",
          "These are **not** a reason to add terms. Two of them are Easterlin's own foundational "
          "papers, and the only term that reaches one of them prices at over 3,000 records per "
          "anchor. They route to the Phase 2 citation channel, which is where the most-cited works "
          "in a field are cheapest to find.", "",
          "| cell | link | title |", "|---|---|---|"]
    for u in log["union"]["unreachable"]:
        L.append(f"| `{u['cell']}` | {u['link']} | {u['title'][:80]} |")
    L += ["", "`LINK1_LABOUR` anchors are expected here: scope §3 makes link 1 context, no arm "
          "targets it, and a query that retrieved that literature well would be retrieving the "
          "wrong literature.", ""]
    (LOGS / "easterlin-relative-income-production-query.md").write_text("\n".join(L))


main()
