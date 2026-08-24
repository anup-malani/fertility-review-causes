#!/usr/bin/env python3
"""
181_a24_ra_spotcheck.py — A.24, stage 6. The blank RA spot-check sheet for the full-text screen.

PROTOCOL §5 asks for an RA spot-check of 5-10% of full-text screen decisions. This writes the sheet
BLANK — the RA's columns are empty and the pipeline's decision is withheld from the working copy —
because a spot-check that shows the original verdict measures agreement with an anchor rather than
agreement between two readers. The pipeline's decision is kept in a separate key file so the
comparison can be made afterwards without the RA having seen it.

SAMPLING IS SEEDED AND STATED. `random.Random(24)` over the id-sorted list of full-text-screened
records, so the same rows are drawn on any re-run and the draw can be audited. The sample is
deliberately STRATIFIED by cell rather than simple-random: with 13 screened records across six cells,
a simple random 10% would usually draw two records from the two largest cells and check nothing that
matters. Every causal cell contributes at least one record, and `PRIMARY_APP_FERTILITY` — which holds
one study and carries the chapter's headline — is checked with certainty.

Output: extraction/{slug}-ra-fulltext-spotcheck.csv        (blank, for the RA)
        extraction/{slug}-ra-fulltext-spotcheck-key.csv     (the pipeline's decisions, withheld)
"""
import csv, json, os, random
from collections import defaultdict

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
STUDIES = os.path.join(EXTRACT, f"{SLUG}-studies.csv")
OUT = os.path.join(EXTRACT, f"{SLUG}-ra-fulltext-spotcheck.csv")
OUT_KEY = os.path.join(EXTRACT, f"{SLUG}-ra-fulltext-spotcheck-key.csv")

BLANK_COLS = ["row", "paper_id", "doi", "title", "year", "venue", "pdf_filename",
              "ra_cell", "ra_fulltext_decision", "ra_design", "ra_evidence_type",
              "ra_exposure_is_dating_app", "ra_outcome_is_realized_or_intention",
              "ra_reverse_causality_tested", "ra_agrees_with_pipeline", "ra_note"]


def main():
    rows = [r for r in csv.DictReader(open(STUDIES)) if r["extraction_status"] == "extracted"]
    by_cell = defaultdict(list)
    for r in rows:
        by_cell[r["cell"]].append(r)
    rng = random.Random(24)
    picked = []
    for cell in sorted(by_cell):
        cand = sorted(by_cell[cell], key=lambda r: r["paper_id"])
        picked.append(rng.choice(cand))
    # top up to ~30% of the screened set, since 13 records make a 10% sample meaningless
    target = max(4, round(0.30 * len(rows)))
    pool = [r for r in sorted(rows, key=lambda r: r["paper_id"]) if r not in picked]
    while len(picked) < target and pool:
        picked.append(pool.pop(rng.randrange(len(pool))))
    picked.sort(key=lambda r: r["paper_id"])

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=BLANK_COLS)
        w.writeheader()
        for i, r in enumerate(picked, 1):
            w.writerow({"row": i, "paper_id": r["paper_id"], "doi": r["doi"],
                        "title": r["title"], "year": r["year"], "venue": r["venue"],
                        "pdf_filename": r["pdf_filename"]})
    with open(OUT_KEY, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["paper_id", "pipeline_cell", "pipeline_fulltext_decision",
                                           "pipeline_design", "pipeline_evidence_type",
                                           "pipeline_reverse_causality_tested"])
        w.writeheader()
        for r in picked:
            w.writerow({"paper_id": r["paper_id"], "pipeline_cell": r["cell"],
                        "pipeline_fulltext_decision": r["fulltext_decision"],
                        "pipeline_design": r["design"], "pipeline_evidence_type": r["evidence_type"],
                        "pipeline_reverse_causality_tested": r["reverse_causality_tested"]})
    print(f"spot-check sheet: {len(picked)} of {len(rows)} screened records "
          f"({len(picked)/len(rows):.0%}), stratified with one per cell, seed 24")
    for r in picked:
        print(f"  {r['cell']:<26} {r['title'][:56]}")
    print(f"-> {os.path.relpath(OUT, ROOT)}  (blank)")
    print(f"-> {os.path.relpath(OUT_KEY, ROOT)}  (withheld key)")


if __name__ == "__main__":
    main()
