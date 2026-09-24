#!/usr/bin/env python3
"""TICK-092 stage 8: risk-of-bias assessment for the D.2.c identified-core studies.

One row per study (mirrors 99_a14_risk_of_bias, domains adapted to D.2.c). The load-bearing domains for
this hypothesis are:
  - `parity_stopping_isolation` (Wall A.8): does the design separate son-preference-specific stopping
    (conditioned on the SEX composition of existing children) from sex-indifferent target-number stopping?
    The revealed-stopping designs that exploit the near-random sex of early births score best here.
  - `substitution_handling` (Wall 1/2): where sex selection is available the fertility effect and the
    sex-ratio-at-birth effect move in OPPOSITE directions; a study that measures only one understates the
    preference. Designs that measure both (Anukriti-Bhalotra-Tam) or that sit in a no-sex-selection regime
    (Dahl-Moretti US) score best.
  - `mortality_isolation` (Wall A.6/A.1): continuing until a SURVIVING son blends son preference with
    replacement; a design that cannot separate them is downgraded.
  - `measurement_preference`: stated-preference (DHS ideal-sex items) is weaker than revealed behaviour.
  - `reverse_causality`: realized family size and observed sex composition are jointly determined.
Ratings: LOW / MODERATE / SERIOUS / CRITICAL. Single-reader (ra_verified = no); RA spot-check owed.
The 2 CONTEXT studies (Anukriti-2018-appendix, Iversen-Palmer-Jones) are not rated (no primary estimate).

Output: extraction/son-preference-cultural-risk-of-bias.csv
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "extraction" / "son-preference-cultural-risk-of-bias.csv"

FIELDS = [
    "study_id", "design", "confounding_selection", "parity_stopping_isolation", "substitution_handling",
    "mortality_isolation", "measurement_preference", "reverse_causality", "reporting",
    "setting_specificity", "overall", "supports_d2c", "rationale", "ra_verified",
]

ROWS = [
    {
        "study_id": "dahl_moretti_2008",
        "design": "Revealed differential stopping; LPM of P(next birth) on sib-sex composition, sex as-good-as-random",
        "confounding_selection": "LOW",
        "parity_stopping_isolation": "LOW",
        "substitution_handling": "LOW",
        "mortality_isolation": "LOW",
        "measurement_preference": "LOW",
        "reverse_causality": "LOW",
        "reporting": "LOW",
        "setting_specificity": "MODERATE",
        "overall": "LOW",
        "supports_d2c": "yes",
        "rationale": "The cleanest identification in the set. The sex of children is as-good-as-random, and the "
                     "GBG-vs-GBB comparison conditions on sib-sex order so the marginal child's sex is random — "
                     "isolating son-preference stopping from sex-indifferent parity (parity_stopping LOW). No "
                     "sex selection in the in-period US, so no substitution to net out (substitution_handling "
                     "LOW). Low US mortality (mortality LOW). Only downgrade is external validity: the US effect "
                     "is small (2-5%); the same design applied internationally (China +54%) shows the setting-"
                     "specificity, which the paper itself documents.",
        "ra_verified": "no",
    },
    {
        "study_id": "almond_li_zhang_2013",
        "design": "County event-study / DiD exploiting staggered land reform x firstborn-girl (natural experiment)",
        "confounding_selection": "LOW",
        "parity_stopping_isolation": "LOW",
        "substitution_handling": "MODERATE",
        "mortality_isolation": "MODERATE",
        "measurement_preference": "LOW",
        "reverse_causality": "LOW",
        "reporting": "LOW",
        "setting_specificity": "MODERATE",
        "overall": "LOW",
        "supports_d2c": "yes (via the sex-ratio channel; fertility null)",
        "rationale": "Exogenous land-reform timing shifts the economic value of sons; the firstborn-girl "
                     "interaction and the clean first-birth placebo null give strong identification "
                     "(confounding/parity LOW). Substitution MODERATE: measures the SRB effect and the fertility "
                     "effect jointly and finds the preference works through sex selection here, NOT extra births "
                     "(the fertility null is informative, not a failure). Mortality MODERATE: excess female "
                     "mortality is a parallel margin not fully separated. Setting MODERATE: rural China, "
                     "one-child-policy era (horse-raced against OCP and survives).",
        "ra_verified": "no",
    },
    {
        "study_id": "anukriti_bhalotra_tam_2021",
        "design": "DDD/DiD: firstborn sex x ultrasound-availability shocks (import 1985, local production 1995)",
        "confounding_selection": "LOW",
        "parity_stopping_isolation": "LOW",
        "substitution_handling": "LOW",
        "mortality_isolation": "MODERATE",
        "measurement_preference": "LOW",
        "reverse_causality": "MODERATE",
        "reporting": "LOW",
        "setting_specificity": "MODERATE",
        "overall": "MODERATE",
        "supports_d2c": "yes (stopping AND its substitution)",
        "rationale": "The most complete design for the estimand: identifies the differential-stopping effect "
                     "(+0.155 births) AND its attenuation by sex selection (-0.088/-0.112 as ultrasound "
                     "diffuses) in one framework, so substitution is handled directly (substitution LOW). "
                     "Firstborn sex is quasi-random (parity/confounding LOW). Downgrades: the ultrasound-timing "
                     "shocks are national (identified off firstborn-sex interactions, mitigating but not "
                     "eliminating concurrent-trend concerns; reverse_causality MODERATE), and excess female "
                     "mortality is a co-moving margin (mortality MODERATE). Overall MODERATE — strong but "
                     "quasi-experimental, not a clean single-cutoff experiment.",
        "ra_verified": "no",
    },
    {
        "study_id": "jiang_2017",
        "design": "Descriptive Das Gupta / Kitagawa decomposition of SRB by birth order (no causal ID)",
        "confounding_selection": "SERIOUS",
        "parity_stopping_isolation": "MODERATE",
        "substitution_handling": "MODERATE",
        "mortality_isolation": "MODERATE",
        "measurement_preference": "LOW",
        "reverse_causality": "MODERATE",
        "reporting": "SERIOUS",
        "setting_specificity": "MODERATE",
        "overall": "SERIOUS",
        "supports_d2c": "yes (mechanism signature, descriptive)",
        "rationale": "High construct relevance — the birth-order SRB gradient (near-normal first birth rising "
                     "to ~159 at 3rd+) is the canonical differential-stopping + sex-selection signature, and the "
                     "1981-vs-2000 contrast dates the arrival of the sex-selection mechanism. But it is purely "
                     "descriptive: decomposition of published SRB series, no counterfactual, no CIs or "
                     "significance tests (reporting/confounding SERIOUS). Used as corroborating mechanism "
                     "evidence, not as a causal estimate.",
        "ra_verified": "no",
    },
    {
        "study_id": "sahni_2008",
        "design": "Single-hospital descriptive time-series of SRB by first-child sex (retrospective)",
        "confounding_selection": "SERIOUS",
        "parity_stopping_isolation": "MODERATE",
        "substitution_handling": "MODERATE",
        "mortality_isolation": "SERIOUS",
        "measurement_preference": "LOW",
        "reverse_causality": "MODERATE",
        "reporting": "MODERATE",
        "setting_specificity": "SERIOUS",
        "overall": "SERIOUS",
        "supports_d2c": "yes (weak/suggestive)",
        "rationale": "On-estimand (second-child SRB after a firstborn girl 716/1000, deepening post-ultrasound) "
                     "but from a single non-representative Delhi hospital, with two-thirds of Indian births "
                     "occurring at home (selection SERIOUS), no causal identification, and an anomalous "
                     "excess-of-girls-after-a-boy cell the authors cannot explain (possible undercounting of "
                     "live-born girls; mortality/measurement SERIOUS). Suggestive corroboration only.",
        "ra_verified": "no",
    },
    {
        "study_id": "fayehun_2011",
        "design": "Cross-sectional logistic of birth interval on sex of preceding child (DHS)",
        "confounding_selection": "SERIOUS",
        "parity_stopping_isolation": "MODERATE",
        "substitution_handling": "MODERATE",
        "mortality_isolation": "SERIOUS",
        "measurement_preference": "MODERATE",
        "reverse_causality": "MODERATE",
        "reporting": "SERIOUS",
        "setting_specificity": "MODERATE",
        "overall": "SERIOUS",
        "supports_d2c": "no (national null)",
        "rationale": "National effect is null (OR 0.955 n.s.) and the ethnic-level results are internally "
                     "inconsistent (Igbo table vs narrative). The outcome is birth SPACING not quantum, and it "
                     "is heavily confounded with lactational amenorrhoea / postpartum abstinence (A.13), which "
                     "the paper itself invokes (mortality/A.13 SERIOUS). No CIs/SEs reported (reporting "
                     "SERIOUS). Value is as evidence that son preference is weak in much of sub-Saharan Africa.",
        "ra_verified": "no",
    },
    {
        "study_id": "kevane_levine_2003",
        "design": "Descriptive tests vs biological benchmarks + sib-sex regressions (complex-survey), IFLS",
        "confounding_selection": "MODERATE",
        "parity_stopping_isolation": "LOW",
        "substitution_handling": "LOW",
        "mortality_isolation": "MODERATE",
        "measurement_preference": "LOW",
        "reverse_causality": "LOW",
        "reporting": "MODERATE",
        "setting_specificity": "MODERATE",
        "overall": "MODERATE",
        "supports_d2c": "no (documented absence)",
        "rationale": "A careful, well-powered documentation of the ABSENCE of son preference in Indonesian "
                     "fertility across multiple revealed-behaviour tests (youngest-child sex, family-size "
                     "composition, spacing), each benchmarked against the biological null with complex-survey "
                     "inference. The stopping and family-size tests are the right revealed-preference design "
                     "(parity_stopping/substitution LOW; no sex selection active in-period). Sex-favouring gaps "
                     "DO appear in schooling/inheritance (routed to D.2.a, OFF_OUTCOME), reinforcing that the "
                     "fertility null is specific, not measurement failure. Overall MODERATE (descriptive, but "
                     "the informative null is robust across tests).",
        "ra_verified": "no",
    },
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ROWS)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(ROWS)} studies)")
    for r in ROWS:
        print(f"  {r['study_id']:28} overall={r['overall']:9} supports_d2c={r['supports_d2c']}")


if __name__ == "__main__":
    main()
