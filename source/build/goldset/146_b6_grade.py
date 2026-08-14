#!/usr/bin/env python3
"""
146_b6_grade.py — B.6, PROTOCOL stage 11. GRADE rating and the §4.3 verdict table, per family.

Applies PROTOCOL §4.1's four-level scheme, which is adapted for observational work and keys on the
EVIDENCE PATTERN rather than on study count:

    High      multiple well-identified RCTs or natural experiments converging
    Moderate  quasi-experimental with credible identification, replicated across >=2 settings
    Low       cross-sectional or panel with controls, no clear identification; or one credible
              quasi-experiment without replication
    Very low  correlational only, mechanism speculative, OR EVIDENCE PATTERN INCONSISTENT

Two things this script does NOT do, and says so rather than papering over:

  * IT IS NOT THE THREE-RATER PANEL. PROTOCOL §5.11 requires "a judge panel of 3 independent agent
    raters, disagreements > 1 level escalate to PI". One analyst producing three labelled opinions in
    one pass is not three independent raters — it is one rater writing three times, and recording it
    as a panel would be a false claim about the process. What follows is ONE rating with its
    reasoning exposed per domain so a real panel can disagree with it specifically. The panel is a
    human-in-the-loop gate and remains outstanding.
  * IT DOES NOT COMPUTE A DECOMPOSITION SHARE. PROTOCOL §4.2 offers three routes to a demographic-
    significance verdict — decomposition share >= 10%, slope sufficiency, or conditional R^2 >= 0.15.
    Only slope sufficiency is answerable here, and it is answerable decisively, so it carries the
    verdict alone. A decomposition share computed from an effect estimate the chapter's own evidence
    says is reverse-causal would be arithmetic dressed as a finding.

Output: literature/search-logs/{slug}-grade.md
"""
import os

SLUG = "microplastics-pfas-reproductive"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_MD = os.path.join(LOGS, f"{SLUG}-grade.md")

# domain, PFAS finding, microplastics finding
DOMAINS = [
    ("Design of the best available evidence",
     "Prospective and cross-sectional cohorts with covariate control. No natural experiment, no IV, "
     "no DiD. The one quasi-experimental design in the corpus (Waterfield 2020, Minnesota water "
     "filtration) estimates birth weight and preterm birth, so Wall 2 routes it out — it is reported "
     "as a flagged aside, not as evidence.",
     "Cross-sectional detection-plus-association studies, most drawn at oocyte retrieval or from "
     "andrology clinics. No cohort, no exposure-side variation, no identification."),
    ("Consistency of the evidence pattern",
     "**INCONSISTENT, and this is the rating's hinge.** Both cohorts that ran a parity-restricted "
     "analysis failed to reproduce their own unrestricted result: INUENDO's associations 'could not "
     "be replicated' among primiparous women, and MoBa's restricted estimate is null "
     "(FOR 0.91 [0.71-1.17]). The disagreement is not between studies but WITHIN them, between "
     "analyses of the same data.",
     "Not assessable. There is no set of estimates on a fertility quantity to be consistent or "
     "inconsistent about. On the input cells the p-values cluster at the margin (0.041, 0.056, "
     "0.080, 0.083, 0.091), which is the pattern a literature produces before it settles."),
    ("Directness of the outcome",
     "INDIRECT. Every estimate is a fecundability ratio or a time-to-pregnancy hazard — a "
     "`HAZARD_DECREMENT`. No record in the extraction table carries a "
     "`TEMPO_ADJUSTED_QUANTUM`: completed parity, cohort fertility, TFR. A hazard moves the timing "
     "of a birth; it converts into a birth forgone only where the reproductive span binds.",
     "INDIRECT at one further remove. The measured outcomes are sperm parameters, retrieved oocytes "
     "and AMH — inputs to fertility, not fertility. Converting them requires the "
     "semen-quality-to-fecundability parameter, which is borrowed and non-linear."),
    ("Precision",
     "The restricted track — the one that carries the verdict — rests on 226 primiparous women in "
     "one cohort plus a sensitivity analysis reported without a point estimate in another. That null "
     "does not distinguish 'no effect' from 'underpowered'.",
     "Small samples throughout; the follicular-fluid detection literature's flagship is 18 women."),
    ("Confounding and reverse causation",
     "**The estimand problem, not a nuisance.** PFAS are eliminated through transplacental transfer, "
     "lactation and menstruation, so parity CAUSES exposure. An unrestricted association is "
     "generated in part by elimination running backwards along the arrow the hypothesis draws. Two "
     "further pharmacokinetic artefacts of the same family appear in the corpus and are documented: "
     "glomerular filtration rate (W2463298380) and pregnancy haemodynamics (W2791210587).",
     "Selection, not reverse causation. Follicular fluid is obtained at oocyte retrieval, so the "
     "sampling frame is selected on subfecundity by construction (Wall 4). Contamination control is "
     "a second, unresolved threat: whether procedural blanks were run is not established for the "
     "held records, and for particle detection that is the difference between measuring biology and "
     "measuring the laboratory."),
    ("Mechanism plausibility",
     "Good, and it is the strongest part of the case. Endocrine disruption, ovarian effects and "
     "receptor-level action are demonstrated in human cells and in the ovarian review literature. "
     "Mechanism is not the weak link; identification is.",
     "Plausible and now well evidenced as EXPOSURE: particles are demonstrably present in placenta, "
     "follicular fluid, semen, testis and blood. Presence establishes that the tissue is exposed. It "
     "does not establish an effect, and the flagship detection study found no association with AMH, "
     "fertilization, miscarriage or live birth."),
]

RATING = {
    "PFAS": ("Very low",
             "PROTOCOL §4.1 assigns Very low where the evidence pattern is INCONSISTENT, and this "
             "pattern is inconsistent in the most damaging available way — within cohorts, between "
             "the unrestricted and parity-restricted analyses of the same data. Absent that, the "
             "design profile alone would put it at Low (cohorts with controls, no identification). "
             "It does not clear Low, because the inconsistency is not noise between settings; it is "
             "the signature of the specific confounding the mechanism predicts."),
    "Microplastics": ("Very low",
                      "PROTOCOL §4.1 assigns Very low to correlational-only evidence. Here it is "
                      "weaker than that label usually implies: there is no correlational evidence on "
                      "a fertility quantity at all, only on fertility inputs, from ART-selected "
                      "samples. The rating is Very low rather than 'insufficient data' because "
                      "evidence does exist and points somewhere — it simply does not bear on the "
                      "estimand."),
}


def main():
    L = [f"# GRADE rating and verdict table — {SLUG} (B.6)", "",
         "Applies PROTOCOL §4.1, which keys on the evidence pattern rather than on study count. Run "
         "once per chemical family, as Call 1 requires.", "",
         "> **This is not the three-rater panel.** PROTOCOL §5.11 requires three independent raters "
         "with disagreements greater than one level escalating to the PI. One analyst writing three "
         "labelled opinions in a single pass is one rater, not three, and calling it a panel would "
         "misdescribe the process. What follows is a single rating with its reasoning exposed per "
         "domain, so that a real panel can disagree with it specifically rather than in general. "
         "**The panel remains outstanding and is a human-in-the-loop gate.**", "",
         "## Domain-by-domain", ""]
    for d, pf, mp in DOMAINS:
        L += [f"### {d}", "", f"**PFAS.** {pf}", "", f"**Microplastics.** {mp}", ""]

    L += ["## Ratings", "", "| family | causal credibility | why this level and not the next |",
          "|---|---|---|"]
    for fam, (r, why) in RATING.items():
        L.append(f"| {fam} | **{r}** | {why} |")

    L += ["", "## §4.3 verdict table", "",
          "Both chapters carry the same three-row structure. PM and FDT have no cell: the exposures "
          "existed at negligible volume before 1965 and the phenomena close before the measurement "
          "does. That is a scope decision from the search design, not a finding.", "",
          "### PFAS", "", "| phenomenon | causal credibility | demographic significance |",
          "|---|---|---|",
          "| Pre-modern | — (no cell) | insufficient data |",
          "| FDT | — (no cell) | insufficient data |",
          "| SDT | **Very low** | **not significant** |", "",
          "The SDT demographic-significance verdict rests on PROTOCOL §4.2's slope-sufficiency route "
          "and is decided by a sign rather than a magnitude: serum PFOS fell 87% and PFOA 74% across "
          "1999–2020 while US TFR fell 18.2%, so the exposure moved in the direction that predicts "
          "*higher* fertility across exactly the window fertility fell. Slope sufficiency is not "
          "merely insufficient — it is wrong-signed. No decomposition share is computed, because a "
          "share built on an estimate the evidence says is reverse-causal would be arithmetic "
          "dressed as a finding.", "",
          "**The one live route to a different answer** is the replacement arm. Short-chain and "
          "substitute compounds entered use as the legacy ones were withdrawn; their exposure series "
          "is unknown rather than flat, and no fertility estimate exists for them. A PFAS "
          "contribution to post-2000 decline survives only there.", "",
          "### Microplastics", "", "| phenomenon | causal credibility | demographic significance |",
          "|---|---|---|",
          "| Pre-modern | — (no cell) | insufficient data |",
          "| FDT | — (no cell) | insufficient data |",
          "| SDT | **Very low** | **insufficient data** |", "",
          "Not 'not significant'. The exposure is real, rising and now measurable inside the "
          "reproductive tract; what is missing is any estimate of its effect on a fertility outcome "
          "in humans. Demographic significance is exposure change times effect size, and the second "
          "term has not been estimated. **The two negative verdicts are not the same verdict** — "
          "PFAS fails on evidence that exists and points the wrong way, microplastics on evidence "
          "that does not exist. The first could only be reopened by the replacement arm; the second "
          "could be overturned by one well-designed cohort.", "",
          "## What would change these ratings", "",
          "Stated because a review that cannot say what would falsify it is not a review.", "",
          "**PFAS → Low or Moderate** would require a parity-restricted or nulliparous-only "
          "prospective cohort with preconception exposure measurement and a completed-fertility "
          "outcome, replicated. Or any fertility-outcome study in the contaminated-community cohorts "
          "— Ronneby, Veneto, C8 — which carry the only exogenous exposure variation in this "
          "literature and have never been used for one. `PRIMARY_HIGH_EXPOSURE` was empty across all "
          "920 screened records.", "",
          "**Microplastics → Low** would require one adequately powered human cohort estimating "
          "particle exposure against time-to-pregnancy or completed parity, sampled outside a "
          "fertility clinic, with procedural-blank contamination control reported. None of those "
          "conditions is exotic; none has been met."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    for fam, (r, _) in RATING.items():
        print(f"{fam:<14} causal credibility: {r}")
    print("SDT demographic significance — PFAS: not significant (wrong-signed slope)")
    print("SDT demographic significance — microplastics: insufficient data (no effect estimate)")
    print("3-rater panel (PROTOCOL 5.11): OUTSTANDING — not simulated")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
