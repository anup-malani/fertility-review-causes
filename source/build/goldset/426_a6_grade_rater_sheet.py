#!/usr/bin/env python3
"""
426 — A.6 (TICK-087): build the judgment-blinded GRADE rating sheet for raters 2 and 3.

`PROTOCOL.md` §5.1 step 11 requires three independent raters. §9 of the chapter is the work of one,
and the same reader made every screening and full-text call beneath it. Simulating two further
raters would manufacture agreement, so the structure for real independence is built instead — the
same move the screen log makes for the second read.

What is withheld and what is not. The sheet carries the **design facts** a rater needs — study,
design, exposure, outcome, n, setting, period, and the cell each study sits in — and the **domain
prompts** from `PROTOCOL.md` §4.1 and the chapter template §2.5. It withholds every rating, every
downgrade, every starting level and rater 1's reasoning. A rater who can see "Low − 2, VERY LOW"
is not an independent rater.

One thing is deliberately *not* blinded: the note that §4.1's **Low** band already prices in "no
clear identification". That is not a judgment, it is how the instrument works, and a rater who
downgrades again for absence of a design is double-counting rather than disagreeing. Withholding
it would generate spurious disagreement instead of measuring real disagreement.

Emits one row per phenomenon plus one for the link stratum, since §4.1 is rated per phenomenon and
the same body can be strong for one target and weak for another.
"""
import csv, pathlib, sys
from collections import Counter

SLUG = "stigma-reduction-contraception-abortion"
SCREENED = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
OUT = pathlib.Path("output") / f"{SLUG}-grade-rater-sheet.csv"
EVIDENCE = pathlib.Path("output") / f"{SLUG}-grade-evidence-brief.md"

ROWS = [
    {"rating_target": "FDT (First Demographic Transition, ~1870-1965)",
     "cell": "PRIMARY_NORM_FERTILITY", "n_studies": "1",
     "designs_present": "one multivariate regression on annual change in a national time series "
                        "with controls; no IV, DiD, RD or event study; no comparison population",
     "settings": "1 (Sweden)", "periods": "1 (1911-1974)",
     "exposure_measured": "a measure of normative pressure to legitimate by marriage births "
                          "conceived out of wedlock, dosed separately from sexual activity, "
                          "birth-control practice and women's status",
     "outcome_measured": "age-specific illegitimacy rates per 1,000 unmarried women",
     "result_as_reported": "legitimation measure significant at all age groups except teenagers; "
                           "annual-change R2 34% (teens) to 66% (ages 20-24, 25-29)",
     "known_facts_a_rater_should_weigh":
         "(a) the exposure measures pressure to MARRY, not the social cost of controlling "
         "fertility; (b) the outcome may be a recomposition of births between marital and "
         "nonmarital rather than a change in their number; (c) reverse causation is structural and "
         "bidirectional over the estimation window, since falling fertility normalises fertility "
         "control; (d) the estimate is not reported in the chapter's dose unit and cannot be "
         "converted without the age-specific unmarried share"},
    {"rating_target": "PM (pre-modern)", "cell": "PRIMARY_NORM_FERTILITY", "n_studies": "0",
     "designs_present": "none", "settings": "0", "periods": "0",
     "exposure_measured": "n/a", "outcome_measured": "n/a", "result_as_reported": "n/a",
     "known_facts_a_rater_should_weigh":
         "the registry does not open PM for A.6, and the claim concerns control within unions; "
         "pre-modern illegitimacy and premarital-sex norms are registered to D.2.b and A.7"},
    {"rating_target": "SDT (Second Demographic Transition, ~1965-present)",
     "cell": "PRIMARY_NORM_FERTILITY", "n_studies": "0",
     "designs_present": "none", "settings": "0", "periods": "0",
     "exposure_measured": "n/a", "outcome_measured": "n/a", "result_as_reported": "n/a",
     "known_facts_a_rater_should_weigh":
         "none of 166 screened records pairs a normative exposure with a fertility level in the "
         "SDT window; the 28 link records are SDT-heavy but all take contraceptive use as the "
         "outcome; the one primary record closes in 1974"},
    {"rating_target": "LINK stratum (stigma -> contraceptive use; NOT the chapter's parameter)",
     "cell": "LINK_NORM_USE", "n_studies": "28",
     "designs_present": "24 cross-sectional with controls; 1 weekly longitudinal panel with a "
                        "mediation design (39,806 person-weeks); 1 community fixed-effects panel; "
                        "2 other adjusted observational",
     "settings": "multiple (Uganda, Sweden, India, US, Egypt, Kenya, others)",
     "periods": "1995-2022 predominantly",
     "exposure_measured": "partner opposition; community norms; moral opposition to birth control; "
                          "perceived approval of use; historical out-of-wedlock norms",
     "outcome_measured": "contraceptive use, uptake, method mix, unmet need",
     "result_as_reported": "partner opposition accounts for ~15% of unmet need overall in Uganda "
                           "(20% urban, 12% rural); other effects non-commensurable across studies",
     "known_facts_a_rater_should_weigh":
         "(a) exposure and outcome are self-reported by the same respondent in the same instrument "
         "in 24 of 28; (b) apparent sign disagreement across studies is explained by the stigma "
         "OBJECT - stigma of contraception lowers use while stigma of premarital sex can raise it - "
         "and the synthesis refuses to pool across it; (c) effect measures are not commensurable"},
]

RATER_FIELDS = ["rater_name", "rater_date", "starting_level_and_why",
                "risk_of_bias_downgrade", "risk_of_bias_reason",
                "indirectness_downgrade", "indirectness_reason",
                "imprecision_downgrade", "imprecision_reason",
                "inconsistency_downgrade", "inconsistency_reason",
                "publication_bias_downgrade", "publication_bias_reason",
                "final_rating", "rater_notes"]


def main():
    if not SCREENED.exists():
        print(f"{SCREENED} missing", file=sys.stderr)
        return 2
    tally = Counter(r["cell"] for r in csv.DictReader(SCREENED.open()))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ROWS[0].keys()) + RATER_FIELDS
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in ROWS:
            w.writerow({**r, **{k: "" for k in RATER_FIELDS}})

    brief = [f"# A.6 GRADE evidence brief for independent raters", "",
             "Generated by `source/build/goldset/426_a6_grade_rater_sheet.py`. Complete",
             f"`{OUT.name}` without reading §9 of the chapter.", "",
             "## Why you are being asked", "",
             "`PROTOCOL.md` §5.1 step 11 requires three independent GRADE raters. One rating exists,",
             "made by the same reader who made every screening and full-text call beneath it.",
             "Simulating the other two would manufacture agreement, so this sheet exists to get",
             "two real ones. **Please do not read chapter §9 first** — it states a starting level,",
             "the downgrades taken, and the reasoning, and seeing them is the whole problem.", "",
             "## The instrument", "",
             "`PROTOCOL.md` §4.1 fixes the bands **by design class**:", "",
             "| rating | evidence pattern |", "|---|---|",
             "| High | multiple well-identified RCTs or natural experiments converging, across settings |",
             "| Moderate | quasi-experimental (IV, DiD, RD, event study) with credible identification, replicated across ≥2 settings |",
             "| Low | cross-sectional or panel with controls, **no clear identification**; or one credible quasi-experiment without replication |",
             "| Very low | correlational only, mechanism speculative, or evidence pattern inconsistent |",
             "",
             "**One non-blinded note, because it is mechanical rather than a judgment.** The Low",
             "band already prices in \"no clear identification\". If you start at Low and then",
             "downgrade again for the absence of an identification strategy, you have counted the",
             "same defect twice. Take downgrades only for defects *beyond* the ones the band",
             "already encodes. Rate the **causal claim**, not the existence of a correlation.", "",
             "**Empty cells are rated `No evidence`, not `Very low`** (template §2.5): Very low",
             "describes a body that exists and is badly identified, which misdescribes nothing at",
             "all. A `No evidence` row should name what would have to exist to earn a rating.", "",
             "## What is in the chapter's cells", "", "| cell | n |", "|---|---|"]
    for c, n in tally.most_common():
        brief.append(f"| `{c}` | {n} |")
    brief += ["", "## Rows to rate", "",
              "Four: one per phenomenon (PM, FDT, SDT) plus the link stratum, which is **not** the",
              "chapter's parameter and is rated only because the chapter reports it and an unrated",
              "reported body invites misreading. §4.1 is rated per phenomenon because the same",
              "evidence can be strong for one target and weak for another.", "",
              "Full texts for every study named are under",
              f"`literature/pdfs/{SLUG}/`; the screening decisions and their reasons are in",
              f"`extraction/{SLUG}-screened.csv`.", "",
              "## After both ratings are in", "",
              "Disagreements are **resolved, not averaged** (template §2.2). Where two raters differ,",
              "the reason for the difference is recorded in the chapter alongside the final band."]
    EVIDENCE.write_text("\n".join(brief) + "\n")

    leak = [f for f in fields if any(k in f.lower() for k in
                                     ("final_rating", "downgrade", "starting"))
            and f not in RATER_FIELDS]
    print(f"wrote {OUT} — {len(ROWS)} rows, {len(RATER_FIELDS)} blank rater fields")
    print(f"wrote {EVIDENCE}")
    print(f"blinding check: rater-1 judgment columns present in source fields: {leak or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
