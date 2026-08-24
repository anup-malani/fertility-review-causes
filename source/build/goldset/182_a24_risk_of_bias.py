#!/usr/bin/env python3
"""
182_a24_risk_of_bias.py — A.24, stage 8. Risk-of-bias instrument and scaffold.

Seven domains: five standard for observational fertility evidence, and TWO CHAPTER-SPECIFIC ones that
exist because A.24's evidence has two defects the standard instrument cannot see.

**DOMAIN 6 — REVERSE CAUSALITY, given its own domain rather than folded into confounding.** D.3.b
added a common-method-bias domain for the same kind of reason. Here the justification is not a
worry but a measurement: the single study in `PRIMARY_APP_FERTILITY` tests the reverse arrow itself
and finds fertility intentions predicting subsequent online partnering at β = 0.22 against its own
forward coefficient of 0.07 — the reverse association is about THREE TIMES the forward one, in the
same sample. People who want children go looking for a partner online. Treating that as ordinary
confounding would rate it alongside "did they adjust for education", and it is not that kind of
problem: it is the arrow pointing the other way. The domain asks three things — was the reverse
direction TESTED, was it FOUND, and does the design (panel lag, exogenous variation) do anything to
break it.

**DOMAIN 7 — EXPOSURE-ESTIMAND DISTANCE.** This is Wall 9's cost restated as bias. A.24's registered
exposure is DATING APPS. Almost none of the evidence measures that: it measures broadband access,
internet access, media use, online-meeting venue, or matchmaking-platform intermediation. Each step
away from the registered exposure buys identification and loses construct validity, and the trade is
systematic rather than random — the better-identified a study is, the further its exposure sits from
the hypothesis. A body of evidence can be individually sound and collectively off-target, and no
standard domain records that. Levels: `direct_app` / `online_meeting` / `internet_access` /
`media_or_content` / `platform_intermediation` / `other_technology`.

Ratings follow the house convention: Low / Moderate / Serious / Critical / No information.

Output: extraction/{slug}-risk-of-bias.csv
"""
import csv, os

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
STUDIES = os.path.join(EXTRACT, f"{SLUG}-studies.csv")
OUT = os.path.join(EXTRACT, f"{SLUG}-risk-of-bias.csv")

COLS = ["study_id", "paper_id", "cell", "d1_confounding", "d2_selection", "d3_exposure_measurement",
        "d4_outcome_measurement", "d5_selective_reporting", "d6_reverse_causality",
        "d6_reverse_tested", "d6_reverse_found", "d7_exposure_estimand_distance",
        "d7_distance_level", "overall", "rationale"]


def main():
    studies = [r for r in csv.DictReader(open(STUDIES)) if r["extraction_status"] == "extracted"]
    if os.path.exists(OUT):
        print(f"{os.path.relpath(OUT, ROOT)} exists; not overwriting")
        return
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in studies:
            w.writerow({"study_id": r["study_id"], "paper_id": r["paper_id"], "cell": r["cell"]})
    print(f"scaffolded {len(studies)} risk-of-bias rows -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
