#!/usr/bin/env python3
"""
242_a23_demsig_grade.py — A.23, stages 10-11. Demographic significance and the GRADE rating.

Every number in the output table is COMPUTED HERE from the inputs declared at the top, with its
source named, because a hand-typed demographic-significance table on A.17 shipped with the right
offsets against the wrong baselines. The chapter quotes this table; it does not restate it.

**THE UNITS CHECK COMES FIRST AND IT DECIDES MOST OF THE SECTION** (template S4). The phenomenon is
denominated in whole children per woman. The mechanism is denominated in the SHARE OF A POPULATION
living in a particular household arrangement. Converting one to the other needs an effect of the
arrangement on completed fertility per person exposed — and for the configuration the registered
claim actually names, no such estimate exists in this literature.

**THE STRUCTURAL POINT THIS SECTION EXISTS TO MAKE.** A.23's exposure rose. Both configurations of it
rose. And the two configurations have OPPOSITE SIGNS, so they partly cancel — which means a
demographic-significance calculation that counts only the configuration the hypothesis names would
attribute the whole exposure rise to fertility decline while part of the same rise pushes the other
way. That is the arithmetic consequence of Ruling 1, and it is why the ruling was worth taking.

**THE NON-ADDITIVITY IS ENFORCED IN THE TABLE, NOT PROMISED IN PROSE.** Ruling 3 makes the
`MIXED_PRICE_ARRANGEMENT` records shared with C.2.c, so any share computed from them is marked
`SHARED_DO_NOT_ADD` and the chapter states the constraint where the number appears.

Output: output/tables/{slug}-demographic-significance.csv
        output/tables/{slug}-grade.csv
        literature/search-logs/{slug}-demsig-grade-log.md
"""
import csv, json, os

SLUG = "co-residence-parents-household-delay"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TABLES = os.path.join(ROOT, "output", "tables")
LOGS = os.path.join(ROOT, "literature", "search-logs")
EFF = os.path.join(ROOT, "extraction", f"{SLUG}-effects.json")
OUT_DEM = os.path.join(TABLES, f"{SLUG}-demographic-significance.csv")
OUT_GRADE = os.path.join(TABLES, f"{SLUG}-grade.csv")
OUT_MD = os.path.join(LOGS, f"{SLUG}-demsig-grade-log.md")

# ---------------------------------------------------------------- inputs, each with its source
INPUTS = {
    "us_multigen_share_2529_1980": (0.13, "Gihleb, Giuntella & Lonsky 2023 (NBER w31117), quoting "
                                          "the US trend: 13% of individuals aged 25-29 in a "
                                          "multigenerational household in 1980"),
    "us_multigen_share_2529_2019": (0.32, "same source: approximately 32% in 2019"),
    "us_coresidence_share_1829_2000_2021_rise": (0.09, "Acolin, Lin & Wachter 2024 (Real Estate "
                                                       "Economics): a 9-percentage-point rise in "
                                                       "the co-residence share, 2000-2021"),
    "affordability_share_of_that_rise": (0.25, "same source: up to a quarter of that rise "
                                               "attributed to declining housing affordability"),
    "extended_effect_children_per_exposed": (0.137, "Nguyen & Duong 2026 (Demographic Research "
                                                    "54:22), Vietnam VARHS with household fixed "
                                                    "effects: +0.137 children (CI 0.082-0.192) for "
                                                    "the presence of grandparent(s)"),
    "us_tfr_fall_sdt": (0.86, "United States TFR, approximately 2.48 in 1970 to approximately 1.62 "
                              "in 2023. NOT SOURCED FROM THIS CHAPTER'S CORPUS — a standard series "
                              "quoted for scale, and flagged for the PI to replace with the "
                              "review's own HFD/WPP panel"),
}

# ------------------------------------------------------------------------------ the arithmetic
def band(x):
    a = abs(x)
    return ("NEGLIGIBLE" if a < 0.05 else "MINOR" if a < 0.20 else
            "SUBSTANTIAL" if a < 0.50 else "DOMINANT")


def main():
    os.makedirs(TABLES, exist_ok=True)
    v = {k: t[0] for k, t in INPUTS.items()}

    d_share = v["us_multigen_share_2529_2019"] - v["us_multigen_share_2529_1980"]
    extended_effect = d_share * v["extended_effect_children_per_exposed"]
    extended_share = extended_effect / v["us_tfr_fall_sdt"]

    rows = [
        dict(phenomenon="pre_modern", applicable="no", share_of_decline="NOT ASSESSED",
             direction="n/a", needs_human_review="no",
             basis="Ruling 2 keeps the pre-modern niche in A.7 (age at marriage and household "
                   "formation timing), and A.23 cites the parallel rather than estimating it. No "
                   "pre-modern cell was searched, so this is out of scope by decision and not "
                   "empty by finding. If assessed, the sign would be POSITIVE: the historical "
                   "European stem-family regions had extended co-residence and higher marital "
                   "fertility than the neolocal ones."),
        dict(phenomenon="FDT", applicable="yes", share_of_decline="NOT IDENTIFIED",
             direction="mixed", needs_human_review="yes",
             basis="One study reaches the FDT window and it is the chapter's largest: Hacker & "
                   "Roberts, 3.1 million US couples linked between the 1900 and 1910 censuses. It "
                   "gives a co-resident MOTHER an incidence rate ratio of 0.951 and a co-resident "
                   "MOTHER-IN-LAW 1.030 in the same regression — opposite signs inside the same "
                   "cell. Both are dwarfed by adult surname-kin density at 1.283. The paper's own "
                   "conclusion is that declining KIN AVAILABILITY contributed to the US fertility "
                   "transition, which is a different exposure from the living arrangement and "
                   "belongs to whichever chapter owns kin networks. No share can be assigned to "
                   "A.23's variable from one uncorrected cross-section, however large."),
        dict(phenomenon="SDT_prelaunch_registered_claim", applicable="yes",
             share_of_decline="NOT IDENTIFIED", direction="unknown", needs_human_review="yes",
             basis="THE CELL THE REGISTERED CLAIM NAMES CONTAINS NO EFFECT ESTIMATE. Two extracted "
                   "effects, zero identified designs, and neither is an estimate of co-residence "
                   "on fertility: one is an association whose authors write that the desire to "
                   "become a mother favours leaving home, the other is municipality-level. The "
                   "pre-launch literature describes the joint distribution of leaving home and "
                   "childbearing; it does not estimate an effect of one on the other. No share can "
                   "be computed and none is offered."),
        dict(phenomenon="SDT_extended_configuration",
             applicable="yes",
             share_of_decline=f"{extended_share:+.1%} of the SDT fall (ILLUSTRATIVE, WRONG-SIGNED)",
             direction="raises fertility", needs_human_review="yes",
             basis=f"The US multigenerational share at ages 25-29 rose {d_share:.0%} between 1980 "
                   f"and 2019. The only quantum estimate available for this configuration is "
                   f"+{v['extended_effect_children_per_exposed']} children per exposed household "
                   f"(Vietnam, household fixed effects). The product is "
                   f"{extended_effect:+.3f} children, which is {extended_share:+.1%} of a "
                   f"{v['us_tfr_fall_sdt']}-child fall — AND IT RUNS THE WRONG WAY. Rising extended "
                   "co-residence, at the only effect size this chapter can quote, RAISES fertility. "
                   "The inputs are from two countries and the estimate is not identified; this is a "
                   "scale check, not a decomposition. What it establishes is the SIGN of the "
                   "correction, and the sign is what matters: a calculation that counted only the "
                   "configuration the hypothesis names would attribute this share to the decline."),
        dict(phenomenon="SDT_via_housing_affordability", applicable="yes",
             share_of_decline="SHARED_DO_NOT_ADD", direction="n/a", needs_human_review="yes",
             basis=f"Housing affordability accounts for up to "
                   f"{v['affordability_share_of_that_rise']:.0%} of the "
                   f"{v['us_coresidence_share_1829_2000_2021_rise']:.0%}-point rise in US "
                   "co-residence 2000-2021 (Acolin, Lin & Wachter). That is link 1 — a driver "
                   "moving the arrangement — and it is C.2.c's treatment travelling down A.23's "
                   "channel. Under Ruling 3 it is reported by both chapters and its magnitude is "
                   "claimed by neither alone. IT MUST NOT BE ADDED to C.2.c's housing-cost share; "
                   "most of C.2.c's young-adult effect runs through this channel."),
        dict(phenomenon="SDT_tempo_versus_quantum", applicable="yes",
             share_of_decline="BOUNDS THE WHOLE CHAPTER", direction="tempo only",
             needs_human_review="no",
             basis="The best-identified design touching this chain (Bulman, Goodman & Isen, US "
                   "state lotteries on the universe of tax data) finds a pull-forward effect on "
                   "births in the year after a windfall and an effect on TOTAL births at five "
                   "years that is close to zero, ruling out an increase above 0.01 children per "
                   "$100,000. The exposure is money rather than the arrangement, so it is not an "
                   "A.23 estimate — but it establishes that the liquidity channel through which "
                   "housing and household formation are supposed to act moves TIMING and not "
                   "COMPLETED FERTILITY. A.23 is a delay mechanism by construction, so this is the "
                   "reading most likely to survive: a period-measure effect that leaves cohort "
                   "fertility untouched."),
    ]
    with open(OUT_DEM, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["phenomenon", "applicable", "share_of_decline",
                                           "direction", "basis", "needs_human_review"])
        w.writeheader()
        w.writerows(rows)

    grade = [
        dict(phenomenon="pre_modern", rating="NOT ASSESSED", starting_point="n/a", downgrades="n/a",
             reason="Out of scope by Ruling 2; the pre-modern niche is A.7's."),
        dict(phenomenon="FDT", rating="VERY LOW", starting_point="observational",
             downgrades="risk of bias (-1); indirectness (-1); imprecision (-1)",
             reason="One uncorrected cross-section, however large. Risk of bias: no design "
                    "addresses the anticipation problem. Indirectness: the paper's own headline "
                    "exposure is kin availability, not the living arrangement. Imprecision: a "
                    "single study, and the two co-residence coefficients have opposite signs."),
        dict(phenomenon="SDT_prelaunch_registered_claim", rating="VERY LOW",
             starting_point="no estimate exists",
             downgrades="not applicable — there is nothing to downgrade",
             reason="THE RATING IS NOT A JUDGEMENT ABOUT WEAK EVIDENCE; IT RECORDS THE ABSENCE OF "
                    "EVIDENCE. Zero identified designs and zero effect estimates in the cell the "
                    "registered claim names. GRADE has no category for this, and reporting VERY "
                    "LOW without the sentence would misrepresent an empty cell as a weak body."),
        dict(phenomenon="SDT_extended_configuration", rating="LOW",
             starting_point="observational, one partially corrected panel estimate",
             downgrades="risk of bias (-1); inconsistency (-1); indirectness (0, held)",
             reason="Household fixed effects remove time-invariant unobservables and not the "
                    "anticipation problem. Inconsistency: a Tanzanian null, a positive Vietnamese "
                    "panel estimate, a within-cell sign reversal by which parent in the US "
                    "historical data, and one endogeneity-corrected estimate whose sign REVERSES. "
                    "Not downgraded for indirectness: these do measure the arrangement."),
        dict(phenomenon="SDT_mixed_price_arrangement", rating="LOW",
             starting_point="quasi-experimental",
             downgrades="indirectness (-1); risk of bias (-1)",
             reason="Two well-identified designs (Spanish rental subsidy; US lotteries) and one not "
                    "retrieved (Laeven & Popov). Indirectness: none of the three has the living "
                    "arrangement as its treatment — they have a subsidy, a windfall and a price. "
                    "Risk of bias: the Spanish study estimates fertility CONDITIONAL ON BEING "
                    "EMANCIPATED, which is a post-treatment variable the treatment itself moves."),
        dict(phenomenon="link1_driver_to_arrangement", rating="MODERATE",
             starting_point="quasi-experimental",
             downgrades="indirectness (-1)",
             reason="The chapter's strongest evidence, and it is about the wrong link: pension "
                    "discontinuities, DACA eligibility and an employment-protection reform all "
                    "move the living arrangement, cleanly identified. None estimates a fertility "
                    "effect, and the one that looks for one (DACA) reports a NULL."),
    ]
    with open(OUT_GRADE, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["phenomenon", "rating", "starting_point", "downgrades",
                                           "reason"])
        w.writeheader()
        w.writerows(grade)

    L = [f"# Stages 10-11 — demographic significance and GRADE — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/242_a23_demsig_grade.py`", "",
         "## Inputs, each with its source", "", "| Input | Value | Source |", "|---|---|---|"]
    for k, (val, src) in INPUTS.items():
        L.append(f"| `{k}` | {val} | {src} |")
    L += ["", "**One input is not from this chapter's corpus** — the US TFR fall — and it is "
          "flagged in the table for the PI to replace with the review's own HFD/WPP panel. It is "
          "used only as a denominator for scale.", "",
          "## The units check (S4), which decides most of this section", "",
          "The phenomenon is denominated in **whole children per woman**. The mechanism is "
          "denominated in **the share of a population living in a particular household "
          "arrangement**. Converting one into the other requires an effect of the arrangement on "
          "completed fertility per person exposed, and **for the configuration the registered claim "
          "names, no such estimate exists in this literature.**", "",
          "## The arithmetic that is available", "",
          f"US multigenerational share, ages 25-29: {v['us_multigen_share_2529_1980']:.0%} (1980) "
          f"to {v['us_multigen_share_2529_2019']:.0%} (2019) = **{d_share:+.0%}**.", "",
          f"At the only quantum estimate this chapter can quote for the extended configuration "
          f"(+{v['extended_effect_children_per_exposed']} children per exposed household): "
          f"{d_share:.2f} x {v['extended_effect_children_per_exposed']} = "
          f"**{extended_effect:+.3f} children**, or **{extended_share:+.1%}** of a "
          f"{v['us_tfr_fall_sdt']}-child fall — band **{band(extended_share)}**, and **in the "
          "wrong direction**.", "",
          "**That sign is the section's finding.** A.23's exposure rose, both of its configurations "
          "rose, and the two configurations have opposite signs. A demographic-significance "
          "calculation that counted only the configuration the hypothesis names would attribute the "
          "whole exposure rise to fertility decline, while part of the same rise pushes the other "
          "way. That is Ruling 1's arithmetic consequence.", "",
          "## Non-additivity, enforced here rather than promised", "",
          "The housing-affordability row is marked `SHARED_DO_NOT_ADD`. Under Ruling 3 it is "
          "reported by both A.23 and C.2.c and its magnitude is claimed by neither alone; most of "
          "C.2.c's young-adult effect runs down this channel. Adding the two chapters' shares would "
          "double-count one effect inside one review.", "",
          "## GRADE, per phenomenon", "", "| Phenomenon | Rating | Downgrades |", "|---|---|---|"]
    for g in grade:
        L.append(f"| `{g['phenomenon']}` | **{g['rating']}** | {g['downgrades']} |")
    L += ["", "**The pre-launch rating needs its sentence read.** VERY LOW there does not record a "
          "weak body of evidence; it records that the cell contains none. GRADE has no category for "
          "an empty cell, and printing VERY LOW without saying so would let a reader take it for a "
          "poorly identified literature rather than an absent one.", "",
          "**The strongest rating in the table is for the wrong link.** `link1_driver_to_arrangement` "
          "is MODERATE: pension discontinuities, DACA eligibility and an employment-protection "
          "reform all move the living arrangement, cleanly. None of them estimates a fertility "
          "effect, and the one that looks reports a null.", "",
          "**Three independent raters have not been used.** The acceptance criterion asks for them; "
          "this is one rater. The standing rule that one person arguing both sides is not a panel "
          "applies, and the criterion stays open.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"extended-configuration share {extended_share:+.1%} ({band(extended_share)}), wrong sign")
    print(f"-> {os.path.relpath(OUT_DEM, ROOT)}")
    print(f"-> {os.path.relpath(OUT_GRADE, ROOT)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
