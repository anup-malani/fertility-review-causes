#!/usr/bin/env python3
"""274 — A.18 GRADE rating. TICK-076.

Two things must be said before any rating is read.

**1. The panel requirement is NOT met.** PROTOCOL §5 step 11 requires three
independent agent raters, with disagreements greater than one level escalated to
the PI. This file contains **one rater**. One model arguing several positions is
not independence — it surfaces contingencies and it does not produce a panel — so
the ratings below are labelled single-rater and the requirement stays open. They
are an input to the panel, not a substitute for it.

**2. GRADE §4.1 has no band for two of the three arms.** Its levels are defined by
identification strategy — RCT, natural experiment, IV/DiD/RD, "correlational only".
A classical twin design or a GREML decomposition is none of those, so the letter of
the table puts a well-executed variance decomposition at *Very low: correlational
only*, which tells a reader the literature is badly identified when the truth is
that it answers a different question competently. This chapter therefore uses
`NOT RATEABLE — non-effect estimand` for the h2 arms, which is the value escalated
to Anup and still unresolved. Recording *Very low* instead would be a false
statement about a careful literature.

Usage: python3 source/build/goldset/274_a18_grade.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSVP = ROOT / "extraction" / "heritability-fertility-genetic.csv"
ROB = ROOT / "extraction" / "heritability-fertility-genetic-risk-of-bias.csv"
OUT = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-grade.json"
OUT_MD = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-grade.md"


def main():
    rob = list(csv.DictReader(ROB.open()))
    serious = sum(1 for r in rob if r["overall"] == "SERIOUS")

    arms = {
        "conjunct_1_heritability": {
            "claim": "Heritable variation accounts for a portion of between-individual differences "
                     "in realized fertility.",
            "rating": "NOT RATEABLE — non-effect estimand",
            "why": "The estimand is a variance component. GRADE §4.1's bands are identification "
                   "strategies for a causal effect and none applies; the nearest available label "
                   "('Very low: correlational only') would misdescribe a competently executed "
                   "literature. Escalated to the PI as a protocol amendment.",
            "if_forced_onto_the_existing_bands": "Very low — and that would be the wrong answer for "
                                                 "the right reason.",
            "evidence": "13 h2 estimates, range 0.00-0.455, every one at SERIOUS or MODERATE risk "
                        "of bias; 0 of 21 strata poolable.",
        },
        "conjunct_2_selection_response": {
            "claim": "Selection on fertility-associated genotypes produces a change in mean "
                     "fertility across generations.",
            "rating": "NO EVIDENCE — cell empty",
            "why": "PREDICTED_RESPONSE held 6 screened studies; 1 was retrieved and reclassified "
                   "out as a coalescent simulation. No S on a fertility-associated genetic measure "
                   "was extracted. GRADE rates the certainty of evidence; there is none to rate.",
            "if_forced_onto_the_existing_bands": "Not 'Very low'. Very low describes weak evidence; "
                                                 "this is absent evidence, and the distinction is "
                                                 "the whole point.",
            "evidence": "0 usable estimates.",
        },
        "conjunct_3_moderation": {
            "claim": "The heritability of fertility varies with the degree to which fertility is "
                     "under individual control.",
            "rating": "LOW",
            "why": "This arm HAS an effect-like estimand — a difference in h2 across regimes — so "
                   "the bands apply. Multiple studies, consistent in kind: h2_SNP rising fivefold "
                   "once cohort and population are modelled (Tropf), h2 rising across 1810-1860 "
                   "female cohorts and falling for males in the same data, and a cohort-interaction "
                   "term whose SIGN flips between two specifications in one paper (Briley). "
                   "Direction is not stable; existence of moderation is better supported than its "
                   "sign. No design here is quasi-experimental, so Low is the ceiling.",
            "if_forced_onto_the_existing_bands": "Low (applied as written).",
            "evidence": "7 estimates across 4 studies; sign-discordant within and between studies.",
        },
    }

    payload = {
        "ticket": "TICK-076",
        "PANEL_REQUIREMENT_NOT_MET": {
            "protocol": "§5 step 11 — three independent agent raters, >1 level disagreement to PI",
            "actual": "one rater (this file)",
            "why_not_simulated": "one model arguing several positions surfaces contingencies but is "
                                 "not independence; labelling it a panel would misrepresent the "
                                 "process. The requirement stays open.",
        },
        "GRADE_BAND_PROBLEM": {
            "issue": "§4.1's bands are identification strategies; a variance decomposition matches "
                     "none of them",
            "value_used": "NOT RATEABLE — non-effect estimand",
            "status": "escalated to the PI, unresolved",
        },
        "arms": arms,
        "per_phenomenon": {
            "PM": "credibility NOT RATEABLE (h2 arm) / demsig CONTINGENT",
            "FDT": "credibility NOT RATEABLE (h2) and NO EVIDENCE (response) / demsig NOT ASSESSED",
            "SDT": "credibility NOT RATEABLE (h2) and NO EVIDENCE (response) / demsig NOT ASSESSED",
        },
        "risk_of_bias_input": {"serious": serious, "of": len(rob)},
    }
    OUT.write_text(json.dumps(payload, indent=2))

    md = ["# A.18 GRADE\n",
          "> **The three-rater panel required by PROTOCOL §5 step 11 has NOT been run.** This is one "
          "rater. One model arguing several positions is not independence, so these ratings are an "
          "input to the panel, not a substitute for it.\n",
          "\n> **GRADE §4.1 has no band for a variance decomposition.** Its levels are identification "
          "strategies; the nearest available label would put a competent twin or GREML study at "
          "*Very low: correlational only*, which misdescribes it. `NOT RATEABLE — non-effect "
          "estimand` is used instead and is escalated to the PI.\n",
          "\n| arm | rating | basis |\n|---|---|---|"]
    for k, a in arms.items():
        md.append(f"| {k.replace('_', ' ')} | **{a['rating']}** | {a['evidence']} |")
    md.append("\n## Per phenomenon\n\n| phenomenon | causal credibility | demographic significance |\n|---|---|---|")
    md.append("| PM | NOT RATEABLE (h²) | CONTINGENT — units question with the PI |")
    md.append("| FDT | NOT RATEABLE (h²) · NO EVIDENCE (response) | NOT ASSESSED |")
    md.append("| SDT | NOT RATEABLE (h²) · NO EVIDENCE (response) | NOT ASSESSED |")
    md.append("\n**The moderation arm is the only one that takes an ordinary GRADE band, and it "
              "rates Low.** It is also the arm the registered claim does not contain.\n")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(json.dumps({k: v["rating"] for k, v in arms.items()}, indent=1))
    print("\nper phenomenon:", json.dumps(payload["per_phenomenon"], indent=1))
    print(f"\nrisk of bias: {serious}/{len(rob)} SERIOUS")


if __name__ == "__main__":
    main()
