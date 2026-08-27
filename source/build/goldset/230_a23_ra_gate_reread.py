#!/usr/bin/env python3
"""
230 — A.23 RA gate, step 2: the re-read, and what it says about the title-only rule.

TICK-075. `229` recovered 35 abstracts from Crossref for records OpenAlex had none
for. Twenty-five of those carried a NOT_RELEVANT verdict reached on the title alone
-- the screen's self-flagged weak point. This script records the re-read of all 25
against the recovered text, and applies the revisions.

THE POINT OF THE EXERCISE IS THE DENOMINATOR, NOT THE REVISIONS. 165 records were
rejected on titles; only 25 of them could be re-tested, because Crossref had nothing
for the other 140. So this is a 15% audit of the bucket, not a clearance of it. What
it can establish is whether the rule FAILS when tested, and in which direction.

One result is worth more than the revisions: the recovered abstract for 'Roadblocks
on the Road to Grandma's House' -- one of the three GOLD records the blinded screen
rejected -- confirms the screen was right. It exploits Italian pension reforms to
shift grandparental childcare supply. The exposure is the grandmother's availability,
not the living arrangement. An independent source vindicated a blinded rejection of a
hand-picked anchor.

Usage: python3 source/build/goldset/230_a23_ra_gate_reread.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SCREENED = LOGS / "co-residence-parents-household-delay-screened.json"
RECOV = LOGS / "co-residence-parents-household-delay-ra-gate-abstracts.json"
OUT = LOGS / "co-residence-parents-household-delay-ra-gate-reread.json"

# Revisions from reading the recovered text. Everything not listed is CONFIRMED.
REVISIONS = {
    "W2615329070": dict(
        verdict="UNCERTAIN", exposure_is_arrangement="yes", config="EXTENDED_COUPLE",
        outcome="fertility", route="PRIMARY_EXTENDED_COUPLE",
        why="The recovered abstract shows the division of domestic labour is measured "
            "with HUSBANDS, PARENTS AND PARENTS-IN-LAW against Korean women's fertility "
            "intentions and behaviour. The in-law term makes it an extended-arm record, "
            "not simply D.2.a's gender-equity story as the title suggested."),
    "W2130191474": dict(
        verdict="UNCERTAIN", exposure_is_arrangement="yes", config="UNSPLIT",
        outcome="other", route="OFF_OUTCOME",
        why="The abstract makes HOUSEHOLD COMPOSITION over the life course the exposure "
            "and the gender division of time the outcome. Arrangement-as-exposure with a "
            "non-fertility outcome, not an off-topic time-use paper."),
    "W7171722536": dict(
        verdict="UNCERTAIN", exposure_is_arrangement="yes", config="PRE_LAUNCH",
        outcome="fertility", route="THEORY",
        why="The abstract places HOUSEHOLD FORMATION and housing markets among the margins "
            "the paper synthesises, and proposes subjective future evaluation as the "
            "underdeveloped one. Theory bearing on this chapter's link 1, and a D.3.c seam."),
}

# Confirmations worth naming in the log, with the reason the recovered text gives.
NOTABLE_CONFIRMATIONS = {
    "W1591887672": "GOLD RECORD, blindly rejected by the screen, and the recovered abstract "
                   "CONFIRMS the rejection: it exploits a decade of Italian pension reforms "
                   "that lengthened the grandparental generation's working horizon, treating "
                   "that as a negative shock to informal childcare SUPPLY. The exposure is "
                   "the grandmother's availability, not the arrangement. An independent "
                   "source vindicating a blinded rejection of a hand-picked anchor.",
    "W3208887223": "Confirms OFF_CHILDCARE_C2a, and the design is stronger than the title "
                   "showed: endogenous switching probit correcting selection and endogeneity "
                   "on grandparental childcare and second birth in China.",
    "W3163582763": "Confirms OFF_CHILDCARE_C2a; propensity-score matching correcting for "
                   "women's fertility choices. Another endogeneity-aware C.2.a design.",
    "W4313157277": "Confirms C.3.b's ownership, but names an identified fertility design: "
                   "staggered state adoption of in-state tuition for undocumented students, "
                   "with LOWER LONG-RUN FERTILITY as an outcome. Report to C.3.b.",
    "W4285525339": "Confirms C.7.a's, and it uses ADMISSION DISCONTINUITIES on Norwegian "
                   "data to separate enrolment from selection in marital matching. Report to "
                   "C.7.a as a design note.",
    "W3014480325": "Confirms NOT_RELEVANT, but it is the eighth record framing the "
                   "arrangement from the PARENTS' budget: children consume a substantial "
                   "share of household income WHILE LIVING AT HOME, against parents' "
                   "retirement saving.",
}


def main():
    doc = json.loads(SCREENED.read_text())
    recov = {r["openalex"]: r for r in json.loads(RECOV.read_text())["records"]}
    worklist = [oid for oid, r in recov.items()
                if r["recovery_status"] == "RECOVERED" and r["verdict"] == "NOT_RELEVANT"]

    log, changed = [], 0
    by_id = {r["openalex"]: r for r in doc["records"]}
    for oid in worklist:
        rec = by_id[oid]
        rev = REVISIONS.get(oid)
        entry = {"openalex": oid, "doi": rec["doi"], "title": rec["title"],
                 "prior_verdict": rec["verdict"], "prior_route": rec["route"]}
        if rev:
            changed += 1
            for k, v in rev.items():
                if k != "why":
                    rec[k] = v
            rec["note"] = (rec["note"] or "") + " | RA GATE RE-READ: " + rev["why"]
            entry.update(outcome_of_reread="REVISED", new_verdict=rev["verdict"],
                         new_route=rev["route"], why=rev["why"])
        else:
            entry.update(outcome_of_reread="CONFIRMED",
                         why=NOTABLE_CONFIRMATIONS.get(oid, "Recovered abstract confirms "
                                                            "the title-based verdict."))
        rec["ra_gate_reread"] = entry["outcome_of_reread"]
        log.append(entry)

    # attach the recovered text to the screened record so extraction has it
    for oid, r in recov.items():
        if r["recovered_abstract"]:
            by_id[oid]["recovered_abstract"] = r["recovered_abstract"]

    doc["meta"]["ra_gate_reread"] = {
        "bucket_rejected_on_title_alone": 165,
        "re_testable": len(worklist),
        "coverage_pct_of_bucket": round(100 * len(worklist) / 165, 1),
        "confirmed": len(worklist) - changed,
        "revised": changed,
        "revised_into_a_primary_cell": sum(
            1 for oid in REVISIONS if REVISIONS[oid]["route"].startswith("PRIMARY")),
        "caveat": "A 15% audit of the bucket, limited by what Crossref holds. It can show "
                  "the rule failing; it cannot clear the 140 records that stayed invisible.",
    }
    SCREENED.write_text(json.dumps(doc, indent=1))
    OUT.write_text(json.dumps({"meta": doc["meta"]["ra_gate_reread"], "reread": log}, indent=1))

    print(json.dumps(doc["meta"]["ra_gate_reread"], indent=1))
    print("\nrevisions:")
    for e in log:
        if e["outcome_of_reread"] == "REVISED":
            print(f"  {e['prior_verdict']} -> {e['new_verdict']} ({e['new_route']})  {e['title'][:60]}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
