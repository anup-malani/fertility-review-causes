#!/usr/bin/env python3
"""Build the C.2.c extraction table from the full-text design read (TICK-055).

The `id_strength` labels in the RA gate were assigned from titles and abstracts. This encodes the
CONFIRMED grade after reading each of the 15 identified PDFs, plus the scope-required per-effect
fields that are determinable from the design sections.

Grades:
  QUASI_EXP     -- a design that isolates exogenous variation (IV, RD, policy DiD)
  WEAK_QUASI    -- an attempt at exogenous variation that does not isolate it: propensity-score
                   matching (selection on observables), or a before/after structural break with no
                   control group. Reported separately rather than folded into either neighbour.
  ASSOCIATIONAL -- fixed effects or time-series association only
  UNREADABLE    -- no text layer; cannot be graded until OCR

Effect sizes are NOT in this pass. Design and routing had to be settled first, because two records
leave the primary pool entirely and one grade decides the FDT cell.
"""
import csv

# work_id: (confirmed_grade, design, treatment_type, tenure_split, outcome_level, period, note)
CONFIRMED = {
    "W3024244835": ("QUASI_EXP", "IV: MSA housing-supply elasticity", "price", "yes: owners vs non-owners",
                    "realized births", "SDT",
                    "The tenure-split anchor the pooling rule is built on. Opposing signs by tenure."),
    "W3037455063": ("QUASI_EXP", "IV: price change of FIRST home purchased, + extensive FE", "price",
                    "owners only (by construction)", "realized births", "SDT",
                    "Danish registers. PREPRINT TWIN in hand -- reconcile against published JPubE before extracting numbers."),
    "W3023795878": ("QUASI_EXP", "IV + city FE + time-varying city controls", "price", "movers vs non-movers",
                    "realized births", "SDT", "China."),
    "W4399107829": ("QUASI_EXP", "IV: house prices instrumented with construction costs and land prices; dynamic panel",
                    "price", "no", "aggregate fertility rate", "FDT+SDT",
                    "Global panel 1870-2012. THE FDT CELL NOW RESTS ON THIS STUDY ALONE (see report)."),
    "W4400391089": ("QUASI_EXP", "regression discontinuity + placebo tests", "housing wealth",
                    "owners (pre-2006 purchasers)", "realized births", "SDT",
                    "Strongest single identification in the pool."),
    "W7171437109": ("QUASI_EXP", "cohort DiD around the 2014 HPF credit-easing reform + IV + PSM + placebo",
                    "ownership-stimulating policy", "owners", "realized births", "SDT",
                    "PNAS. Treatment is a policy that stimulates ownership, so it sits at the C.3.e boundary -- check at extraction whether the variation is price or credit."),
    "W4395680672": ("QUASI_EXP", "house purchase restriction policy variation", "price", "unclear",
                    "realized births", "SDT", "SSRN preprint; no published version located."),
    "W3121393843": ("QUASI_EXP", "IV: initial-area house prices for movers", "price", "yes: owners vs renters",
                    "realized births", "SDT",
                    "Canada. Tenure split present and explicitly predicts opposing signs -- second most useful study for the pooling rule."),
    "W3144108245": ("QUASI_EXP", "difference-in-differences on national HPR policy, 2000-2018", "price",
                    "no", "aggregate birth rate", "SDT", "China."),
    "W2949452997": ("WEAK_QUASI", "propensity-score matching on youth-housing allocation", "rent (policy-allocated)",
                    "renters", "realized births", "SDT",
                    "PSM is selection on observables, not exogenous variation. Demoted from QUASI_EXP."),
    "W3125001667": ("WEAK_QUASI", "1987 housing-price structural break as 'natural experiment' + district and marriage-year FE",
                    "price + tenure options", "yes: owner / renter / with-parents", "timing of first birth", "SDT",
                    "Before/after break with no control group. Demoted from QUASI_EXP. Tenure categories are useful even so."),
    "W2081775216": ("ASSOCIATIONAL", "cointegration / error-correction model on aggregate annual series",
                    "price", "no", "aggregate CBR/TFR", "SDT",
                    "No instrument anywhere in the paper. DEMOTED from QUASI_EXP -- a macro time-series association."),
    "W4395481274": ("ASSOCIATIONAL", "area-level and individual fixed effects", "price", "partial",
                    "realized births", "SDT", "No instrument, no policy shock. DEMOTED from QUASI_EXP."),
    "W2224046657": ("ROUTED_OUT", "IV: shift-share on national building permits x city geography",
                    "housing supply", "n/a", "MARRIAGE (not fertility)", "FDT",
                    "Every estimating table has marriage as the outcome. The '10 percent of the baby-boom rise' figure is the author's DECOMPOSITION applied to a marriage estimate, not an estimated fertility effect. Routes to HOUSING_ONLY_MECHANISM, cross-ref A.7. Retain the decomposition as a demographic-significance input, attributed."),
    "W4308203433": ("UNREADABLE", "unknown -- 21-page image-only scan, no text layer", "rent (public rental housing)",
                    "renters", "birth interval", "SDT",
                    "Korean. Needs OCR + translation. The only policy-assigned-rent design in the pool, so it cannot be dropped for convenience."),
}

gate = {r["openalex"]: r for r in csv.DictReader(open("extraction/housing-costs-ra-gate.csv"))}
out = "extraction/housing-costs-study-extraction.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["work_id", "doi", "year", "venue", "title", "screen_cell",
                "id_strength_screen", "id_strength_confirmed", "design", "treatment_type",
                "tenure_split", "outcome_level", "period", "note",
                "effect_extracted", "extracted_by", "extracted_date"])
    for wid, (grade, design, tt, ts, ol, per, note) in CONFIRMED.items():
        g = gate.get(wid, {})
        w.writerow([wid, g.get("doi", ""), g.get("year", ""), g.get("venue", ""), g.get("title", ""),
                    g.get("ra_verdict", ""), g.get("id_strength", ""), grade, design, tt, ts, ol, per,
                    note, "NO", "Shravan/Claude", "2026-07-31"])

from collections import Counter
c = Counter(v[0] for v in CONFIRMED.values())
print(f"extraction table -> {out}\n")
print("confirmed grade (was 15 QUASI_EXP on title/abstract):")
for k, n in c.most_common():
    print(f"  {n:>3}  {k}")
missing = [w for w in CONFIRMED if w not in gate]
if missing:
    print(f"\nWARNING - work_ids not found in the gate: {missing}")
