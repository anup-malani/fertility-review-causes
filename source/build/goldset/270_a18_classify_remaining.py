#!/usr/bin/env python3
"""270 — A.18: resolve the remaining pending extractions by ESTIMAND TYPE. TICK-076.

Reading the 39 outstanding full texts produced a result that changes the synthesis
plan: **not one of them reports a heritability estimate for a fertility outcome.**
They report other quantities entirely —

  GWAS loci                       what variants associate, not how much variance
  genetic correlations (r_g)      between fertility and another trait
  PGS-fertility associations      effect per SD of a polygenic score
  odds / hazard ratios            for childlessness or a transition

Those are legitimate evidence and they belong in the chapter, but they are not the
estimand `H2_FERTILITY` pools, and counting a cell's studies is not counting its
poolable estimates. The >=3 pooling test is applied AFTER stratification by
estimand, so this is the step where the difference becomes visible.

Each row is written with the quantity the study actually reports, so nothing is
silently defaulted into the h2 pool it does not belong to.

Usage: python3 source/build/goldset/270_a18_classify_remaining.py
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
CSVP = ROOT / "extraction" / "heritability-fertility-genetic.csv"
OUT = LOGS / "heritability-fertility-genetic-estimand-classification.json"

FERTW = (r"(?:children ever born|number of children|completed fertility|age at first birth|"
         r"childless\w*|reproductive success|parity|fertility|NEB|AFB|CEB)")
V = r"(?<![\d.])[-−]?\d?\.\d{2,4}(?![\d])"
TESTS = [
    ("h2_on_fertility", re.compile(r"(?:heritabilit\w*|h\s*2|h²)[^.]{0,60}" + FERTW +
                                   r"[^.]{0,80}?" + V + r"|" + FERTW +
                                   r"[^.]{0,60}(?:heritabilit\w*|h\s*2)[^.]{0,80}?" + V, re.I)),
    ("selection_gradient", re.compile(r"selection (?:gradient|differential)[^.]{0,140}?" + V, re.I)),
    ("pgs_fertility_assoc", re.compile(r"(?:polygenic (?:score|index)|PGS|PRS)[^.]{0,130}" +
                                       FERTW + r"[^.]{0,110}?" + V, re.I)),
    ("genetic_correlation", re.compile(r"genetic correlation[^.]{0,120}?" + V, re.I)),
    ("gwas_loci", re.compile(r"(?:genome[- ]wide significan|identif\w+ \d+ (?:loci|variants|signals))", re.I)),
    ("odds_or_hazard", re.compile(r"(?:odds ratio|hazard ratio|OR\s*=|HR\s*=)[^.]{0,60}?" + V, re.I)),
]

# Hand-verified values, read from the full text. Quantity is named explicitly so no
# row can drift into the h2 pool.
VERIFIED = {
    "W2795856187": ("pgs_variance_explained", "0.015",
                    "Figure 1. Variance Explained by AFB and NEB Polygenic Scores ... R2 ~0.015 "
                    "at the best p-value threshold — the AFB/NEB polygenic scores explain about "
                    "1.5% of variance"),
    "W2950098314": ("pgs_fertility_beta", "-0.045",
                    "a positive, but non-significant association between the PGS and fertility "
                    "(beta = -0.045, p = .11), [while] educational attainment and fertility "
                    "(beta = -0.32, p < .001)"),
    "W2955592702": ("pgs_fertility_correlation", "-0.031",
                    "PGS ... Number of children -.031 | Number of grandchildren -.018 "
                    "(male subsample n = 2617)"),
    "W2969099478": ("genetic_correlation_ADHD_AFB", "-0.68",
                    "the PRS of attention-deficit/hyperactivity disorder (ADHD) were strongly "
                    "associated with age at first birth (AFB) (genetic correlation of -0.68"),
    "W2625700093": ("pgs_number_of_children_beta", "0.054",
                    "(b = 0.054, P = 0.29). However, they have a greater variance in number of "
                    "children (b = 1.112, P = 0.02)"),
}
# Second retitled version pair, found by reading (exact-title dedup requires identical
# folded titles, so one differing word defeats it).
DUPES = {"W3166912545": "W4220783065"}


def main():
    rows = list(csv.DictReader(CSVP.open()))
    fields = rows[0].keys()
    cand = {r["openalex"]: r for r in json.loads((TEMP / "extraction-candidates.json").read_text())}
    classification, counts = {}, Counter()
    for r in rows:
        if r["extraction_status"] != "PENDING_SECOND_PASS":
            continue
        oid = r["openalex"]
        f = TEMP / "text" / f"{oid}.txt"
        if not f.exists():
            r["extraction_status"] = "NO_FULL_TEXT"; continue
        t = re.sub(r"\s+", " ", f.read_text())
        got = [n for n, p in TESTS if p.search(t)]
        classification[oid] = got
        if oid in DUPES:
            r["extraction_status"] = f"DUPLICATE_OF_{DUPES[oid]}_DO_NOT_POOL"
            r["source_quote"] = ("Preprint of the published version, retitled on publication "
                                 "('Provides New Evidence' vs 'provides evidence'), so exact-title "
                                 "dedup could not pair them.")
            counts["duplicate"] += 1
            continue
        if oid in VERIFIED:
            q, val, quote = VERIFIED[oid]
            r["estimand"], r["estimate"], r["source_quote"] = q, val, quote
            r["extraction_status"] = "VERIFIED_NON_H2_ESTIMAND"
            counts["verified_non_h2"] += 1
            continue
        if "h2_on_fertility" in got:
            r["extraction_status"] = "PENDING_H2_PRESENT"; counts["h2_present"] += 1
        elif got:
            r["estimand"] = "|".join(got)
            r["extraction_status"] = "NO_H2_REPORTS_OTHER_ESTIMAND"
            r["source_quote"] = ("Reports " + ", ".join(got) + " — not a heritability estimate for "
                                 "a fertility outcome. Evidence for the chapter, not for the h2 pool.")
            counts["other_estimand"] += 1
        else:
            r["extraction_status"] = "NO_EXTRACTABLE_ESTIMATE"
            r["source_quote"] = ("No heritability, selection-gradient, PGS-association or genetic-"
                                 "correlation estimate on a fertility outcome located in the full "
                                 "text. Narrative/contextual only.")
            counts["none"] += 1

    with CSVP.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields))
        w.writeheader()
        w.writerows(rows)
    OUT.write_text(json.dumps({"summary": {
        "ticket": "TICK-076", "pending_resolved": sum(counts.values()),
        "breakdown": dict(counts),
        "studies_reporting_h2_on_fertility_among_the_39": sum(
            1 for v in classification.values() if "h2_on_fertility" in v),
        "note": "Not one of the 39 reports a heritability estimate for a fertility outcome. "
                "A cell's study count is not its poolable-estimate count."},
        "classification": classification}, indent=1))
    print("resolved:", dict(counts))
    print("status now:", dict(Counter(r["extraction_status"] for r in rows)))


if __name__ == "__main__":
    main()
