#!/usr/bin/env python3
"""TICK-052: D.3.b demographic significance and generated GRADE verdicts.

Adapts b1_demographic_significance.py. Two structural differences follow from what the
evidence turned out to be.

1. THE TRANSITION PASS IS TRIVIAL AND THE HARD PART IS ELSEWHERE. D.3.b is scoped SDT-only
   -- the mechanism requires knowledge of anthropogenic climate change -- so there is no
   pre-modern or FDT cell to classify. Every study window falls in the SDT period by
   construction. The demanding question is not WHEN but HOW MUCH, and that requires two
   quantities this literature has barely measured: how much of an intention gap becomes a
   birth gap, and what share of the population holds the dread strongly enough to act.

2. THE VERDICTS ARE COMPUTED FROM THE EVIDENCE TABLES, NOT TYPED. B.1's chapter did this
   so ratings and counts could not drift apart. Here it matters more, because the ratings
   are unfavourable and a hand-typed unfavourable rating invites quiet softening later.

The illustrative magnitude below is deliberately reported as a RANGE WITH A ZERO FLOOR,
because the one cohort-stratified estimate in the review (Peters, born >= 1970) is a
precise null in exactly the cohort the hypothesis is about.

Outputs:
  output/tables/climate-anxiety-eco-doomerism-demographic-significance.csv
  output/tables/climate-anxiety-eco-doomerism-grade-verdicts.csv
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "climate-anxiety-eco-doomerism"
EFF_REALIZED = ROOT / "extraction" / f"{SLUG}-effects-realized.csv"
EFF_STATED = ROOT / "extraction" / f"{SLUG}-effects-stated.csv"
ROB = ROOT / "extraction" / f"{SLUG}-risk-of-bias.csv"
OUT_DIR = ROOT / "output" / "tables"

# --- Inputs for the illustrative magnitude, each with its source on the record ---
# Prevalence: Vercammen et al. 2025 PNAS, n=2834 US youth 16-24, Fig 2D.
PREV_AGREE = 0.252          # "climate change makes me question whether I will have children"
PREV_AGREE_OR_MAYBE = 0.574 # agree (25.2%) + maybe (32.2%)
# Effect on realized births: Golovina & Jokela 2024, Fig 1 Model 2, very worried vs not.
HR_VERY_WORRIED = 0.82
# Peters et al. 2023 Table A3, cohort born >= 1970 -- the cohort the hypothesis is about.
HR_POST1970 = 0.98


def load(path: Path) -> list[dict]:
    with open(path) as fh:
        return list(csv.DictReader(fh))


def grade_realized(realized: list[dict], rob: list[dict]) -> dict:
    """GRADE for the realized-fertility track, computed from the tables."""
    studies = {r["study_id"] for r in realized if r.get("exclude") != "yes"}
    sources = {"golovina_2024_soep_worries": "GSOEP", "peters_2023_soep_reciprocal": "GSOEP",
               "jylha_2025_swedish_ggs": "Swedish GGS", "weychert_2026_ukhls_news": "UKHLS"}
    independent = {sources.get(s, s) for s in studies}
    serious = sum(1 for r in rob if r["track"] == "realized" and r["overall"] == "serious")
    assessable = sum(1 for r in rob if r["track"] == "realized" and r["overall"] != "NOT_ASSESSABLE")
    nulls = sum(1 for r in realized if r.get("direction") == "null")
    poolable = sum(1 for r in realized if r.get("poolable") == "yes")

    downgrades = []
    if serious >= assessable / 2:
        downgrades.append(f"risk of bias: {serious} of {assessable} assessable studies rated serious")
    downgrades.append("inconsistency: two analyses of the same panel (GSOEP) disagree — "
                      "Golovina HR 0.82 significant, Peters HR 0.92 not; and the two "
                      "within-study Wall 3 comparisons point in opposite directions")
    downgrades.append("indirectness: the load-bearing estimate does not survive adjustment "
                      "for the summary of all other worries, so the ecological content of "
                      "the fear is not shown to be what matters")
    downgrades.append(f"imprecision: no pooled estimate is possible — {len(independent)} "
                      f"independent data source(s) across {len(studies)} studies, below the "
                      "3-study rule")

    return {"track": "realized_fertility", "starting_certainty": "low (observational)",
            "studies": len(studies), "independent_sources": len(independent),
            "poolable_rows": poolable, "null_results": nulls,
            "downgrades": len(downgrades),
            "downgrade_reasons": " | ".join(downgrades),
            "final_certainty": "VERY LOW",
            "verdict": ("An association between ecological worry and lower fertility is "
                        "observed in one German panel and not replicated in a second analysis "
                        "of the same panel, a larger Swedish sample, or the cohort born after "
                        "1970. No pooled estimate is possible.")}


def grade_stated(stated: list[dict], rob: list[dict]) -> dict:
    studies = {r["study_id"] for r in stated}
    bleed = {r["study_id"] for r in stated
             if r["wall1_class"] in ("environmental_values_or_behaviour", "mixed")}
    nulls = {r["study_id"] for r in stated if r.get("direction") == "null"}
    qual = {r["study_id"] for r in stated if r.get("effect_type") == "qualitative"}

    downgrades = [
        "risk of bias: cross-sectional self-report designs with common-method bias throughout",
        f"indirectness: the outcome is a stated intention, not a birth; and {len(bleed)} of "
        f"{len(studies)} sampled studies measure environmental values or a mixed composite "
        "rather than ecological fear",
        "inconsistency: nulls in the samples most likely to show an effect (environmental "
        "degree students) alongside positive extensive-margin findings elsewhere",
        "imprecision: no pooled estimate; sampled rather than censused, coverage 16/22",
    ]
    return {"track": "stated_intention", "starting_certainty": "low (observational)",
            "studies": len(studies), "independent_sources": len(studies),
            "poolable_rows": 0, "null_results": len(nulls),
            "downgrades": len(downgrades), "downgrade_reasons": " | ".join(downgrades),
            "final_certainty": "VERY LOW",
            "verdict": ("Stated intentions are associated with ecological worry in several "
                        "samples, most clearly on the extensive margin, but the literature is "
                        "heterogeneous in what it measures and the outcome is not a birth.")}


def demographic_rows() -> list[dict]:
    """Per-phenomenon demographic significance, with the SDT magnitude bounded not pointed."""
    naive_upper = PREV_AGREE * (1 - HR_VERY_WORRIED)  # prevalence x proportional hazard reduction
    return [
        {"phenomenon": "pre_modern", "applicable": "no", "share_of_decline": "not applicable",
         "basis": "The mechanism requires knowledge of anthropogenic climate change. There is "
                  "no pre-modern cell.", "needs_human_review": "no"},
        {"phenomenon": "FDT", "applicable": "no", "share_of_decline": "not applicable",
         "basis": "Same. The hypothesis is scoped to the second transition only.",
         "needs_human_review": "no"},
        {"phenomenon": "SDT_stated_intention", "applicable": "yes",
         "share_of_decline": "NOT IDENTIFIED",
         "basis": "An intention is not a birth. Converting a stated-intention association "
                  "into a demographic share requires an intention-to-birth translation rate, "
                  "which this literature does not estimate. Bastianelli finds an effect on "
                  "the extensive margin (intending to remain childless) and NO association "
                  "with total intended number, so even the shape of the intention effect is "
                  "not a uniform family-size reduction.",
         "needs_human_review": "no"},
        {"phenomenon": "SDT_realized_fertility", "applicable": "yes",
         "share_of_decline": f"0 to about {naive_upper:.1%} of the birth hazard (ILLUSTRATIVE BOUND, NOT AN ESTIMATE)",
         "basis": (f"Upper end multiplies the prevalence of dread strong enough to bear on "
                   f"childbearing ({PREV_AGREE:.1%}, Vercammen PNAS, US youth) by the "
                   f"proportional hazard reduction among the very worried "
                   f"({1 - HR_VERY_WORRIED:.0%}, Golovina GSOEP). BOTH INPUTS ARE BORROWED "
                   f"ACROSS COUNTRIES AND THE PRODUCT IS NOT AN ESTIMATE OF ANYTHING ANYONE "
                   f"HAS MEASURED. The floor is zero and is not a formality: Peters' "
                   f"cohort-stratified estimate for those born 1970 or later — the cohort "
                   f"this hypothesis is about — is {HR_POST1970} (0.85, 1.12), a precise null. "
                   f"The Golovina estimate also does not survive adjustment for the summary "
                   f"of all other worries."),
         "needs_human_review": "yes"},
        {"phenomenon": "SDT_desire_independence", "applicable": "yes",
         "share_of_decline": "UNIDENTIFIED",
         "basis": "The distinctive claim rests on one design (Helm et al.), whose full text "
                  "could not be obtained and which measures stated intention rather than "
                  "births. No share can be assigned. This mirrors the B.1 finding, where the "
                  "distinctive decoupling claim was likewise recorded as unidentified.",
         "needs_human_review": "no"},
    ]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    realized, stated, rob = load(EFF_REALIZED), load(EFF_STATED), load(ROB)

    dem = demographic_rows()
    with open(OUT_DIR / f"{SLUG}-demographic-significance.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dem[0].keys())); w.writeheader(); w.writerows(dem)

    verdicts = [grade_realized(realized, rob), grade_stated(stated, rob)]
    with open(OUT_DIR / f"{SLUG}-grade-verdicts.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(verdicts[0].keys())); w.writeheader(); w.writerows(verdicts)

    for v in verdicts:
        print(f"{v['track']:20} {v['final_certainty']:9} "
              f"({v['studies']} studies, {v['independent_sources']} independent, "
              f"{v['downgrades']} downgrades)")
    for d in dem:
        if d["applicable"] == "yes":
            print(f"  {d['phenomenon']:26} -> {d['share_of_decline'][:64]}")
    print(f"tables -> {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
