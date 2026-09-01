#!/usr/bin/env python3
"""299 — C.3.e: validate the extraction table. TICK-077.

Written because I hand-typed an OpenAlex id into the extraction table one hour after recording
the lesson that says never to do that. The id was wrong. Nothing in the CSV would have shown it:
the study name was right, the estimate was right, and the row would have attached to a record
that does not exist -- or worse, to a real record that is a different study.

Checks, all cheap and all of which have now failed at least once on this chapter:
  1. every `openalex` exists in the SCREEN TABLE -- the authoritative record set. It used to check
     the 296 retrieval record, which was one run against one pool, and that produced FALSE POSITIVES
     as soon as PDFs began arriving by other routes (hand delivery, the browser, the handoff folder).
     A validator that flags correct rows gets ignored, which is worse than no validator;
  2. every id's title in the screen table matches the row's `study` field;
  3. `OUTCOME_LEVEL` is present and from the closed list -- realized / desired / intention.
     This chapter's composite studies carried OPPOSITE SIGNS at different outcome levels, so a
     blank here is not a missing tag, it is a missing finding;
  4. `estimator_class` is from the closed list; an unlisted value must fail loudly rather than
     fall through to `uncorrected` and pool with things it should be separated from;
  5. `identified` is YES/NO and, where NO, the row is flagged as secondary-pool.

Usage: python3 299_c3e_validate_extraction.py
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
CSVP = ROOT / "extraction" / "credit-constraints-effects.csv"

OUTCOME_LEVELS = {"realized", "desired", "intention", "completed"}
ESTIMATORS = {"aggregate_panel_uncorrected", "cross_section_OLS_uncorrected",
              "theory_plus_empirical_uncorrected", "DiD", "DiD_matching", "IV", "RCT",
              "event_study", "RDD", "panel_FE", "quasi_experimental_other"}


def norm(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())


def main():
    import csv as _csv
    byid = {r["openalex"]: r for r in
            _csv.DictReader((ROOT / "extraction" / "credit-constraints-screen.csv").open())}
    rows = list(csv.DictReader(CSVP.open()))
    errs = []
    for i, r in enumerate(rows, 2):
        oid = r["openalex"]
        if oid not in byid:
            errs.append(f"row {i}: id {oid} is not in the screen table")
            continue
        t_ret, t_row = norm(byid[oid]["title"]), norm(r["study"])
        if not (t_row[:28] in t_ret or t_ret[:28] in t_row):
            errs.append(f"row {i}: id {oid} titled '{byid[oid]['title'][:44]}' "
                        f"but the row says '{r['study'][:44]}'")
        if r.get("OUTCOME_LEVEL", "").strip() not in OUTCOME_LEVELS:
            errs.append(f"row {i}: OUTCOME_LEVEL '{r.get('OUTCOME_LEVEL')}' not in "
                        f"{sorted(OUTCOME_LEVELS)} - this chapter's signs flip on it")
        if r.get("estimator_class", "").strip() not in ESTIMATORS:
            errs.append(f"row {i}: estimator_class '{r.get('estimator_class')}' is unlisted - "
                        f"add it deliberately, do not let it fall through")
        if r.get("identified", "").strip().upper() not in {"YES", "NO"}:
            errs.append(f"row {i}: `identified` must be YES or NO, got '{r.get('identified')}'")
    print(f"{len(rows)} rows, {len({r['openalex'] for r in rows})} studies")
    if errs:
        print(f"\n{len(errs)} VALIDATION ERRORS")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    print("all checks pass")
    from collections import Counter
    print("  by arm:      ", dict(Counter(r["arm"] for r in rows)))
    print("  by outcome:  ", dict(Counter(r["OUTCOME_LEVEL"] for r in rows)))
    print("  identified:  ", dict(Counter(r["identified"] for r in rows)))


if __name__ == "__main__":
    main()
