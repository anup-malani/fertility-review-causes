#!/usr/bin/env python3
"""TICK-093 stage 8: risk-of-bias assessment for the D.1.d identified-core studies.

One row per study (mirrors 99_d2c_risk_of_bias, domains adapted to D.1.d). The load-bearing domains for
this hypothesis are:
  - `transfer_isolation` (Wall C.2.d): does the design separate the pronatalist IDEOLOGY/framing from the
    financial TRANSFER it is bundled with? This is the central defect of the whole literature — almost no
    study can, and the one clean natural experiment (Aksoy-Billari) shows, by mediation, that the effect
    runs through the transfer, not the ideology.
  - `coercion_isolation` (Wall A.4): does the design separate persuasion from a coercive abortion/
    contraception restriction? The Eastern-European canon (not in this read set) fails here; the four
    read studies happen to carry no coercion.
  - `outcome_measurement`: is the outcome realized (quantum) fertility, or a transient tempo response, or
    only attitudes/intentions? A short birth-probability window cannot separate tempo from quantum.
  - `reverse_causality`: demographic decline itself causes the adoption of pronatalist politics.
  - `confounding_selection`: the design's internal validity for the effect it does estimate.
Ratings: LOW / MODERATE / SERIOUS / CRITICAL. Single-reader (ra_verified = no); RA spot-check owed.
Note: `overall` rates the internal validity of the effect each study ESTIMATES (e.g. of Islamist rule, or
of the cash package). `supports_d1d` records separately whether that effect identifies the D.1.d estimand
(the ideology channel) — for every study it does not, which is the chapter's central finding.

Output: extraction/nationalism-pronatalist-ideology-risk-of-bias.csv
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "extraction" / "nationalism-pronatalist-ideology-risk-of-bias.csv"

FIELDS = [
    "study_id", "design", "confounding_selection", "transfer_isolation", "coercion_isolation",
    "outcome_measurement", "reverse_causality", "reporting", "setting_specificity", "overall",
    "supports_d1d", "rationale", "ra_verified",
]

ROWS = [
    {
        "study_id": "aksoy_billari_2018",
        "design": "Close-election RDD (AK Parti mayoral win margin 2004), district/province/individual",
        "confounding_selection": "LOW",
        "transfer_isolation": "SERIOUS",
        "coercion_isolation": "LOW",
        "outcome_measurement": "LOW",
        "reverse_causality": "LOW",
        "reporting": "LOW",
        "setting_specificity": "MODERATE",
        "overall": "LOW",
        "supports_d1d": "direction yes, mechanism NO",
        "rationale": "The cleanest identification in the literature: close-election RD passes the McCrary "
                     "density test and multiple pre-2004 placebo/covariate-balance tests, replicated across three "
                     "independent datasets (confounding LOW; reverse_causality LOW — the win margin is exogenous "
                     "to fertility; national fertility-control law is constant so coercion_isolation LOW; outcome "
                     "is realized births with no tempo reversal, LOW). `overall` LOW is for the effect it "
                     "estimates — of Islamist RULE on fertility. But that exposure bundles ideology with a large "
                     "poverty-targeted welfare expansion, and the authors' own mediation routes the effect through "
                     "health-insurance coverage (+0.28) while finding NULL effects on the ideational mediators "
                     "(ideal children 0.12 n.s.; religiosity 0.05 n.s.). So transfer_isolation is SERIOUS and the "
                     "study does NOT identify the D.1.d ideology channel — it is evidence the fertility gain ran "
                     "through spending, not framing.",
        "ra_verified": "no",
    },
    {
        "study_id": "validova_2021",
        "design": "Descriptive period-fertility tempo/quantum decomposition (no control group)",
        "confounding_selection": "SERIOUS",
        "transfer_isolation": "SERIOUS",
        "coercion_isolation": "LOW",
        "outcome_measurement": "MODERATE",
        "reverse_causality": "MODERATE",
        "reporting": "MODERATE",
        "setting_specificity": "MODERATE",
        "overall": "SERIOUS",
        "supports_d1d": "weak, mechanism NO",
        "rationale": "A transparent decomposition, but a nationwide simultaneous rollout leaves no control "
                     "group and no counterfactual (confounding SERIOUS, author-acknowledged); the rise is "
                     "confounded with the large 1980s cohort at peak age and the post-2008 economic cycle "
                     "(reverse/omitted MODERATE). The outcome analysis itself is a strength: it separates tempo "
                     "(91%) from quantum (9%). Ideology is inseparable from the maternity-capital cash "
                     "(transfer_isolation SERIOUS). No standard errors reported (reporting MODERATE). Does not "
                     "identify the ideology channel; its own conclusion is that the tools 'remain financial'.",
        "ra_verified": "no",
    },
    {
        "study_id": "wang_2026",
        "design": "Descriptive narrative time-series ('event analysis'); no regression, no counterfactual",
        "confounding_selection": "CRITICAL",
        "transfer_isolation": "SERIOUS",
        "coercion_isolation": "LOW",
        "outcome_measurement": "SERIOUS",
        "reverse_causality": "SERIOUS",
        "reporting": "SERIOUS",
        "setting_specificity": "MODERATE",
        "overall": "CRITICAL",
        "supports_d1d": "no (background only)",
        "rationale": "No identification of any kind: policy dates are eyeballed against lagged aggregate "
                     "movements, with no control, no regression, and no reported estimate (confounding/outcome/"
                     "reporting CRITICAL/SERIOUS). Useful only as background: it argues the rise was mainly "
                     "structural (cohort size) and policy effects mostly tempo. Not an evidentiary contribution to "
                     "the estimand; carried as context.",
        "ra_verified": "no",
    },
    {
        "study_id": "tang_wong_batzorig_2022",
        "design": "Difference-in-differences (LPM) on the 2011 Order-of-Glorious-Mother reform; PSM robustness",
        "confounding_selection": "MODERATE",
        "transfer_isolation": "SERIOUS",
        "coercion_isolation": "LOW",
        "outcome_measurement": "MODERATE",
        "reverse_causality": "LOW",
        "reporting": "LOW",
        "setting_specificity": "MODERATE",
        "overall": "MODERATE",
        "supports_d1d": "direction yes, mechanism NO (routes to C.2.d)",
        "rationale": "A credible DiD off a discrete reform, with PSM robustness and reported SEs (reporting LOW), "
                     "but parallel trends rest on two cross-sections eight years apart with treatment/control "
                     "defined by parity x time (confounding MODERATE), and the outcome is a two-year birth-"
                     "probability window that cannot separate tempo from quantum (outcome_measurement MODERATE). "
                     "Decisively for D.1.d, the reform bundles the honorific 'Mother Hero' status inseparably with "
                     "a doubled cash annuity and lowered parity thresholds; the paper identifies the money, not the "
                     "honour (transfer_isolation SERIOUS). The registered 'honorific award' instrument is, "
                     "empirically, a transfer — the effect routes to C.2.d.",
        "ra_verified": "no",
    },
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ROWS)
    tally = {}
    for r in ROWS:
        tally[r["overall"]] = tally.get(r["overall"], 0) + 1
    print(f"wrote {OUT.relative_to(ROOT)} ({len(ROWS)} studies)")
    print(f"overall RoB tally: {tally}")
    print("Every study fails transfer_isolation (SERIOUS): none identifies the D.1.d ideology channel.")


if __name__ == "__main__":
    main()
