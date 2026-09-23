#!/usr/bin/env python3
"""TICK-091 stage 8: risk-of-bias assessment for the A.14 identified-core studies.

One row per study (mirrors 66_c2h_risk_of_bias, domains adapted to A.14). The load-bearing domains for
this hypothesis are `confounding_selection_age` (Wall 4: older couples have both lower fecundity AND lower
frequency; and selection into separation/migration) and `contraception_control` (Wall 1: A.14 is the
exposure identity NET of contraception — a study that cannot hold Cc fixed bundles the contraception
channel). `reverse_causality` carries A.14's key threat (fertility desire drives coital frequency and its
timing). `measurement_exposure` is high-stakes because much of the literature infers coital frequency
rather than measuring it. Ratings: LOW / MODERATE / SERIOUS / CRITICAL. Single-reader (ra_verified = no);
RA spot-check owed.

Output: extraction/coital-frequency-biological-risk-of-bias.csv
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "extraction" / "coital-frequency-biological-risk-of-bias.csv"

FIELDS = [
    "study_id", "design", "confounding_selection_age", "contraception_control", "reverse_causality",
    "measurement_exposure", "measurement_outcome", "missing_data", "reporting", "setting_specificity",
    "overall", "supports_a14", "rationale", "ra_verified",
]

ROWS = [
    {
        "study_id": "nie_2020_fujian",
        "design": "Discrete-time logit event-history, multi-process w/ correlated unobserved heterogeneity (aML)",
        "confounding_selection_age": "MODERATE",
        "contraception_control": "SERIOUS",
        "reverse_causality": "MODERATE",
        "measurement_exposure": "MODERATE",
        "measurement_outcome": "LOW",
        "missing_data": "MODERATE",
        "reporting": "LOW",
        "setting_specificity": "SERIOUS",
        "overall": "MODERATE",
        "supports_a14": "yes",
        "rationale": "Separation is an exogenous coital-exposure shock within intact unions and the multi-process "
                     "model explicitly models the correlation between separation and fertility (rho=0.71), so "
                     "couple-level selection is addressed. Contraception SERIOUS: no direct contraceptive-use "
                     "variable; one-child-policy dummies enter only 2nd/3rd-birth models, so the 1st-birth "
                     "estimate cannot rule out that separated couples also contracept differently. Exposure "
                     "MODERATE: separation observed in years, coital frequency itself not measured. Setting "
                     "SERIOUS: one ethnic-migration system (Fujian). The 'no reunification catch-up' finding is "
                     "the strongest internal evidence the effect is a genuine exposure loss, not postponement.",
        "ra_verified": "no",
    },
    {
        "study_id": "clifford_2009_tajikistan",
        "design": "Multilevel bivariate multi-process (joint conception+migration) logit, MCMC",
        "confounding_selection_age": "LOW",
        "contraception_control": "MODERATE",
        "reverse_causality": "MODERATE",
        "measurement_exposure": "MODERATE",
        "measurement_outcome": "LOW",
        "missing_data": "LOW",
        "reporting": "LOW",
        "setting_specificity": "SERIOUS",
        "overall": "MODERATE",
        "supports_a14": "yes",
        "rationale": "Best-identified separation study: the joint model estimates selection directly via the "
                     "cross-process covariance and finds NO couple-level selection and only positive "
                     "community-level selection, so the selection-corrected estimate is MORE negative than the "
                     "naive one (naive underestimates disruption) — confounding LOW. Contraception MODERATE: "
                     "not directly measured, but the setting is near-natural-fertility (modern contraceptive "
                     "prevalence ~30%, TFR ~4), so the Cc channel is small. Reverse causality MODERATE: does not "
                     "model migration timing chosen around childbearing. Setting SERIOUS: one country, dose "
                     "recorded in months. Author cautions the short 1998-2002 window cannot reveal completed-"
                     "fertility catch-up — so this identifies a period/tempo effect, quantum unknown.",
        "ra_verified": "no",
    },
    {
        "study_id": "bouchard_2018_marquette",
        "design": "Prospective single-arm cohort (fertile-window monitoring), Kaplan-Meier; internal timing contrast",
        "confounding_selection_age": "SERIOUS",
        "contraception_control": "LOW",
        "reverse_causality": "MODERATE",
        "measurement_exposure": "LOW",
        "measurement_outcome": "LOW",
        "missing_data": "MODERATE",
        "reporting": "SERIOUS",
        "setting_specificity": "SERIOUS",
        "overall": "SERIOUS",
        "supports_a14": "yes (slope of the identity, clinical setting)",
        "rationale": "Establishes the biometric slope — well-timed fertile-window intercourse yields 85/100 "
                     "vs 1/100 for infertile-day intercourse — with prospective daily exposure measurement "
                     "(exposure LOW). But no randomized/frequent-intercourse control arm, so timing cannot be "
                     "separated from frequency internally (selection/confounding SERIOUS). No CIs/SEs reported "
                     "(reporting SERIOUS). Self-selected, mostly college-educated Catholic conception-seekers, "
                     "not infertility-screened and not a general-population fecundability cohort (setting "
                     "SERIOUS). Direction is unambiguous and corroborated by cited RCTs (Tiplady 43% vs 30%; "
                     "Robinson 22.7% vs 14.4%), so the slope is real; the magnitude is clinical-setting-specific.",
        "ra_verified": "no",
    },
    {
        "study_id": "mturi_1997_tanzania",
        "design": "Cox proportional hazards on birth-to-conception intervals, non-contracepting subsample",
        "confounding_selection_age": "MODERATE",
        "contraception_control": "LOW",
        "reverse_causality": "MODERATE",
        "measurement_exposure": "SERIOUS",
        "measurement_outcome": "MODERATE",
        "missing_data": "MODERATE",
        "reporting": "MODERATE",
        "setting_specificity": "SERIOUS",
        "overall": "SERIOUS",
        "supports_a14": "weak/indirect",
        "rationale": "Contraception LOW by design (sample restricted to non-contraceptors — the cleanest Wall-1 "
                     "setting). But exposure SERIOUS: coital frequency is never measured; the A.14 signal is only "
                     "an indirect proxy (polygamy HR 0.87, no-co-resident-partner HR 0.62), and the direct "
                     "abstinence coefficient is AMALGAMATED with lactational amenorrhoea (A.13), so the headline "
                     "combined HR 0.27 cannot be attributed to coital abstinence. Overall SERIOUS for A.14 "
                     "purposes: directionally supportive but confounded and indirect.",
        "ra_verified": "no",
    },
    {
        "study_id": "pp_rct_2022_nl",
        "design": "RCT (web sexual-health programme vs expectant management), ITT",
        "confounding_selection_age": "LOW",
        "contraception_control": "LOW",
        "reverse_causality": "LOW",
        "measurement_exposure": "SERIOUS",
        "measurement_outcome": "LOW",
        "missing_data": "SERIOUS",
        "reporting": "LOW",
        "setting_specificity": "SERIOUS",
        "overall": "SERIOUS (for A.14 indirectness), LOW as an RCT of its own question",
        "supports_a14": "no (null; failed manipulation)",
        "rationale": "Internally a clean RCT (randomization, allocation concealment, blinded analysis, ITT) — "
                     "low risk of bias for its own question. But for A.14 it is INDIRECT and uninformative about "
                     "the frequency->conception slope, because the manipulation FAILED: coital frequency fell "
                     "equally in both arms (~7->6/month), so the frequency 'first stage' never fired "
                     "(measurement_exposure/indirectness SERIOUS). 57% attrition before completing the programme "
                     "(missing SERIOUS). The intervention targets sexual pleasure/distress, not frequency per se. "
                     "Reads as a caution that light-touch interventions do not raise coital frequency, not as "
                     "evidence against the identity.",
        "ra_verified": "no",
    },
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ROWS)
    print(f"wrote {OUT} ({len(ROWS)} studies)")
    for r in ROWS:
        print(f"  {r['study_id']:26} overall={r['overall'].split(' ')[0]:9} supports_a14={r['supports_a14']}")


if __name__ == "__main__":
    main()
