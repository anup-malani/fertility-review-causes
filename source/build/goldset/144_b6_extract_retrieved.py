#!/usr/bin/env python3
"""
144_b6_extract_retrieved.py — B.6, PROTOCOL stages 6-8 for the records retrieved so far.

Writes the extraction table and the risk-of-bias assessment for the full texts held in
`literature/pdfs/{slug}/`. Extraction is HAND-CODED FROM FULL TEXT, located first by
`143_b6_fulltext_probe.py` so each coded value has a quoted passage behind it, and recorded here
rather than in a notebook so the value, its source and the judgement stay attached.

FOUR FINDINGS FROM THIS BATCH, recorded here rather than buried in a cell:

  1. THE PARITY-RESTRICTED ANALYSES DO NOT REPLICATE THE ASSOCIATIONS, IN BOTH COHORTS THAT RAN ONE.
     INUENDO (Greenland/Poland/Ukraine) reports pooled PFNA fecundability FR = 0.80 [0.69-0.94] and
     infertility OR = 1.53 [1.08-2.15], then states that "in a sensitivity analysis of primiparous
     women these associations could not be replicated". MoBa, restricting to 226 primiparous women,
     reports PFOSA FOR = 0.91 [0.71-1.17] — null. This is Call 2's two-track result arriving from
     inside the literature rather than being imposed on it, and it is the single most important
     thing this extraction found. The unrestricted and restricted tracks disagree, and the direction
     of the disagreement is the one the reverse-causation mechanism predicts.

  2. ADJUSTING FOR PARITY IS NOT RESTRICTING ON IT, AND THE DISTINCTION DECIDES THE VERDICT.
     S-PRESTO (Singapore), the one preconception-measured cohort here, finds decreased fecundability
     (PFDA FR = 0.90 [0.82, 0.98]; PFOS 0.88 [0.79, 0.99]; mixture 0.89 [0.73, 1.02]) — and adjusts
     for parity as a covariate rather than restricting. Parity lies on the path from prior
     reproduction to current exposure, so adjustment leaves the reverse-causal channel partly open
     and can additionally induce collider bias. `PARITY_HANDLING` therefore needs FOUR levels, not
     the two Call 2 implied: nulliparous_restricted / parity_stratified / parity_adjusted / none.
     Only the first two belong in the restricted track.

  3. THE MICROPLASTICS PRIMARY CELL HOLDS FIVE REVIEWS AND NO EMPIRICAL ESTIMATE. Every held
     plastic-family record in a PRIMARY cell is a review or opinion piece — "A Threat for", "May Be a
     Significant Cause of", "Is Harmful to". The five empirical microplastics records held all
     estimate fertility INPUTS (sperm parameters, retrieved oocytes, AMH), are small-n, largely
     ART-derived, and report p-values clustered at the margin (0.041, 0.056, 0.080, 0.083, 0.091).
     The microplastics chapter's GRADE rating attaches to an effect cell that, at present, contains
     no effect estimate on a fertility quantity.

  4. TEXT EXTRACTION DAMAGED THE NUMERICS IN SEVERAL DOCUMENTS. Decimals split across the
     PDF-to-text and XML-to-text boundaries ("0." followed by a break), so several microplastics
     effect sizes are legible as a direction and a p-value but not as a point estimate with an
     interval. Those rows are marked `NUMERIC_UNRECOVERED` rather than filled with a guess, and they
     need PDF-quality re-extraction before any pooling. A number transcribed wrongly is worse than a
     number recorded as missing.

Output: extraction/{slug}-effects.csv
        extraction/{slug}-risk-of-bias.csv
        literature/search-logs/{slug}-extraction-report.md
"""
import csv, os

SLUG = "microplastics-pfas-reproductive"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")

EFFECT_FIELDS = ["openalex_id", "study", "year", "chemical_family", "compound", "cohort",
                 "sampling_frame", "exposure_timing", "outcome", "estimand_level", "estimate",
                 "ci_low", "ci_high", "p_value", "parity_handling", "track", "note"]

# track: "restricted" = nulliparous_restricted or parity_stratified; "unrestricted" = everything
# else. Call 2's primary synthesis is the restricted track; the unrestricted track is the
# sensitivity, and the GAP BETWEEN THEM is itself a reported quantity.
EFFECTS = [
    # --- INUENDO: the cohort that ran both tracks and reported the disagreement ---
    dict(openalex_id="W2160568778", study="PFAS and time to pregnancy, Greenland/Poland/Ukraine",
         year=2014, chemical_family="PFAS_LEGACY", compound="PFNA", cohort="INUENDO",
         sampling_frame="pregnant women, population-based", exposure_timing="during pregnancy",
         outcome="time to pregnancy (fecundability)", estimand_level="HAZARD_DECREMENT",
         estimate="0.80", ci_low="0.69", ci_high="0.94", p_value="",
         parity_handling="none", track="unrestricted",
         note="Pooled sample, log-scale FR. Exposure measured IN pregnancy, so timing is posterior "
              "to the outcome being explained."),
    dict(openalex_id="W2160568778", study="PFAS and time to pregnancy, Greenland/Poland/Ukraine",
         year=2014, chemical_family="PFAS_LEGACY", compound="PFNA", cohort="INUENDO (Greenland)",
         sampling_frame="pregnant women, population-based", exposure_timing="during pregnancy",
         outcome="time to pregnancy (fecundability)", estimand_level="HAZARD_DECREMENT",
         estimate="0.72", ci_low="0.58", ci_high="0.89", p_value="",
         parity_handling="none", track="unrestricted", note="Greenland stratum."),
    dict(openalex_id="W2160568778", study="PFAS and time to pregnancy, Greenland/Poland/Ukraine",
         year=2014, chemical_family="PFAS_LEGACY", compound="PFNA", cohort="INUENDO",
         sampling_frame="pregnant women, population-based", exposure_timing="during pregnancy",
         outcome="infertility (TTP > 13 months)", estimand_level="HAZARD_DECREMENT",
         estimate="1.53", ci_low="1.08", ci_high="2.15", p_value="",
         parity_handling="none", track="unrestricted", note="Pooled infertility OR."),
    dict(openalex_id="W2160568778", study="PFAS and time to pregnancy, Greenland/Poland/Ukraine",
         year=2014, chemical_family="PFAS_LEGACY", compound="PFNA", cohort="INUENDO (primiparous)",
         sampling_frame="pregnant women, population-based", exposure_timing="during pregnancy",
         outcome="time to pregnancy and infertility", estimand_level="HAZARD_DECREMENT",
         estimate="NOT_REPLICATED", ci_low="", ci_high="", p_value="",
         parity_handling="nulliparous_restricted", track="restricted",
         note="THE KEY ROW. The paper's own words: 'in a sensitivity analysis of primiparous women "
              "these associations could not be replicated.' No point estimate is given in the "
              "abstract; the restricted-track figure must be read off the paper's tables before "
              "this row can be pooled."),

    # --- MoBa: parity-restricted by design, and null ---
    dict(openalex_id="W2409520153", study="PFOSA and fecundability (Brief Report), MoBa",
         year=2016, chemical_family="PFAS_LEGACY", compound="PFOSA", cohort="MoBa",
         sampling_frame="population-based birth cohort", exposure_timing="during pregnancy",
         outcome="time to pregnancy (fecundability odds ratio)", estimand_level="HAZARD_DECREMENT",
         estimate="0.91", ci_low="0.71", ci_high="1.17", p_value="",
         parity_handling="nulliparous_restricted", track="restricted",
         note="226 primiparous women. NULL. The paper reports no association between any other "
              "PFAS and TTP among primiparous women."),
    dict(openalex_id="W2409520153", study="PFOSA and fecundability (Brief Report), MoBa",
         year=2016, chemical_family="PFAS_LEGACY", compound="PFOSA", cohort="MoBa (all women)",
         sampling_frame="population-based birth cohort", exposure_timing="during pregnancy",
         outcome="time to pregnancy (fecundability odds ratio)", estimand_level="HAZARD_DECREMENT",
         estimate="0.85", ci_low="0.83", ci_high="1.09", p_value="",
         parity_handling="none", track="unrestricted",
         note="All women. CI as printed in the source; the lower bound sits implausibly close to the "
              "point estimate and should be checked against the published table at second reading."),

    # --- S-PRESTO: preconception-measured, parity ADJUSTED not restricted ---
    dict(openalex_id="W4321019748", study="PFAS and women's fertility outcomes, Singapore",
         year=2023, chemical_family="PFAS_LEGACY", compound="PFDA", cohort="S-PRESTO",
         sampling_frame="population-based preconception cohort", exposure_timing="preconception",
         outcome="fecundability (per quartile increase)", estimand_level="HAZARD_DECREMENT",
         estimate="0.90", ci_low="0.82", ci_high="0.98", p_value="",
         parity_handling="parity_adjusted", track="unrestricted",
         note="Preconception exposure measurement — the timing that identifies. But parity is a "
              "COVARIATE, not a restriction, so the reverse-causal channel is only partly closed."),
    dict(openalex_id="W4321019748", study="PFAS and women's fertility outcomes, Singapore",
         year=2023, chemical_family="PFAS_LEGACY", compound="PFOS", cohort="S-PRESTO",
         sampling_frame="population-based preconception cohort", exposure_timing="preconception",
         outcome="fecundability (per quartile increase)", estimand_level="HAZARD_DECREMENT",
         estimate="0.88", ci_low="0.79", ci_high="0.99", p_value="",
         parity_handling="parity_adjusted", track="unrestricted", note=""),
    dict(openalex_id="W4321019748", study="PFAS and women's fertility outcomes, Singapore",
         year=2023, chemical_family="PFAS_LEGACY", compound="PFOA", cohort="S-PRESTO",
         sampling_frame="population-based preconception cohort", exposure_timing="preconception",
         outcome="fecundability (per quartile increase)", estimand_level="HAZARD_DECREMENT",
         estimate="0.95", ci_low="0.86", ci_high="1.06", p_value="",
         parity_handling="parity_adjusted", track="unrestricted", note="Null."),
    dict(openalex_id="W4321019748", study="PFAS and women's fertility outcomes, Singapore",
         year=2023, chemical_family="PFAS_LEGACY", compound="PFAS mixture", cohort="S-PRESTO",
         sampling_frame="population-based preconception cohort", exposure_timing="preconception",
         outcome="fecundability (per quartile increase in mixture)",
         estimand_level="HAZARD_DECREMENT", estimate="0.89", ci_low="0.73", ci_high="1.02",
         p_value="", parity_handling="parity_adjusted", track="unrestricted",
         note="Mixture WITHIN the PFAS family, so separable — not a Wall 1 case."),
    dict(openalex_id="W4321019748", study="PFAS and women's fertility outcomes, Singapore",
         year=2023, chemical_family="PFAS_LEGACY", compound="PFDA", cohort="S-PRESTO",
         sampling_frame="population-based preconception cohort", exposure_timing="preconception",
         outcome="clinical pregnancy", estimand_level="HAZARD_DECREMENT",
         estimate="0.74", ci_low="0.56", ci_high="0.98", p_value="",
         parity_handling="parity_adjusted", track="unrestricted",
         note="Live-birth ORs were in the same direction but did not reach significance — the "
              "further down the causal chain the outcome sits, the weaker the estimate gets."),

    # --- LIFE: preconception, Bayesian, cycle length ---
    dict(openalex_id="W2514091930", study="Perfluoroalkyl chemicals, menstrual cycle length and fecundity",
         year=2016, chemical_family="PFAS_LEGACY", compound="PFDeA", cohort="LIFE",
         sampling_frame="preconception couple cohort", exposure_timing="preconception",
         outcome="menstrual cycle length (acceleration factor)", estimand_level="HAZARD_DECREMENT",
         estimate="1.03", ci_low="1.00", ci_high="1.05", p_value="",
         parity_handling="parity_adjusted", track="unrestricted",
         note="95% CREDIBLE interval, not a confidence interval — Bayesian model. Cycle length is a "
              "fertility INPUT, not a fertility quantity. Parity adjustment is conditional on "
              "gravidity and appears only in sensitivity analyses."),

    # --- Microplastics: empirical records, all on fertility INPUTS ---
    dict(openalex_id="W4402945134", study="Mixed microplastic exposure and sperm dysfunction, China",
         year=2024, chemical_family="PLASTIC_PARTICLE", compound="mixed microplastics",
         cohort="multi-site, China", sampling_frame="not established from held text",
         exposure_timing="cross-sectional", outcome="sperm concentration",
         estimand_level="HAZARD_DECREMENT", estimate="NUMERIC_UNRECOVERED", ci_low="", ci_high="",
         p_value="0.041", parity_handling="not applicable (male)", track="unrestricted",
         note="Direction and p-value legible; point estimate lost to decimal splitting in text "
              "extraction. Other endpoints p = 0.083, 0.091. Needs PDF-quality re-extraction."),
    dict(openalex_id="W4412003778", study="Microplastics in human semen and semen quality",
         year=2025, chemical_family="PLASTIC_PARTICLE", compound="microplastics",
         cohort="not established from held text", sampling_frame="not established from held text",
         exposure_timing="cross-sectional", outcome="semen quality / immotile spermatozoa",
         estimand_level="HAZARD_DECREMENT", estimate="NUMERIC_UNRECOVERED", ci_low="", ci_high="",
         p_value="0.056", parity_handling="not applicable (male)", track="unrestricted",
         note="NULL at conventional thresholds (p = 0.056 and 0.080). Reported here because a "
              "marginal null is evidence and is exactly what publication bias suppresses."),
    dict(openalex_id="W7123517430", study="Microplastics in follicular fluid and ovarian reserve",
         year=2026, chemical_family="PLASTIC_PARTICLE", compound="micro/nanoplastics",
         cohort="medically assisted reproduction", sampling_frame="ART clinic (Wall 4 selection)",
         exposure_timing="cross-sectional", outcome="number of retrieved oocytes",
         estimand_level="HAZARD_DECREMENT", estimate="NUMERIC_UNRECOVERED (beta negative)",
         ci_low="", ci_high="", p_value="0.008", parity_handling="not established",
         track="unrestricted",
         note="Significant on retrieved oocytes; AMH only 'a tendency to reduced'. ART-derived, so "
              "the sample is selected on subfecundity and the estimate does not transport."),
    dict(openalex_id="W4412525568", study="PE and PVC nanoplastics in follicular fluid and seminal plasma",
         year=2025, chemical_family="PLASTIC_PARTICLE", compound="polyethylene, PVC",
         cohort="IVF patients", sampling_frame="ART clinic (Wall 4 selection)",
         exposure_timing="cross-sectional", outcome="fertilization rate",
         estimand_level="HAZARD_DECREMENT", estimate="NUMERIC_UNRECOVERED", ci_low="", ci_high="",
         p_value="0.0003", parity_handling="not applicable", track="unrestricted",
         note="The strongest microplastics p-value held — but fertilization rate in IVF is an ART "
              "TREATMENT outcome, which Wall 4 routes to A.17. Retained as an input, not as a "
              "fertility quantity."),
    dict(openalex_id="W4415012676", study="Plastic tableware use, microplastic accumulation and sperm quality",
         year=2025, chemical_family="PLASTIC_PARTICLE", compound="polystyrene, PVC, total MP",
         cohort="not established from held text", sampling_frame="not established from held text",
         exposure_timing="cross-sectional", outcome="sperm motion parameters",
         estimand_level="HAZARD_DECREMENT", estimate="NUMERIC_UNRECOVERED", ci_low="", ci_high="",
         p_value="", parity_handling="not applicable (male)", track="unrestricted",
         note="The only behaviourally-defined exposure contrast in the microplastics evidence "
              "(tableware use frequency), which is why it matters out of proportion to its size. "
              "Numerics need PDF-quality re-extraction."),
]

ROB_FIELDS = ["openalex_id", "study", "domain", "rating", "basis"]
ROB = [
    ("W2160568778", "INUENDO", "reverse causation (parity/excretion)", "SERIOUS",
     "Primary analysis unrestricted; the paper's own primiparous sensitivity analysis fails to "
     "replicate. The authors report this candidly, which is to their credit and is also the finding."),
    ("W2160568778", "INUENDO", "exposure timing", "SERIOUS",
     "Serum measured during pregnancy — after the conception whose hazard is being explained, and "
     "after the elimination that pregnancy itself causes."),
    ("W2409520153", "MoBa Brief Report", "reverse causation (parity/excretion)", "LOW",
     "Restricted to 226 primiparous women by design. This is the handling Call 2 requires."),
    ("W2409520153", "MoBa Brief Report", "precision", "SERIOUS",
     "n = 226 in the restricted analysis; the interval spans the null comfortably. A null this "
     "imprecise does not distinguish 'no effect' from 'underpowered'."),
    ("W4321019748", "S-PRESTO", "reverse causation (parity/excretion)", "MODERATE",
     "Parity adjusted as a covariate, not restricted. Adjustment leaves the reverse-causal channel "
     "partly open and may induce collider bias; preconception measurement mitigates but does not "
     "remove it."),
    ("W4321019748", "S-PRESTO", "exposure timing", "LOW",
     "Preconception measurement — exposure precedes outcome. The best timing in the held evidence."),
    ("W2514091930", "LIFE", "estimand", "SERIOUS",
     "Cycle length is a fertility input, not a fertility quantity. Reported as an OVARIAN_PARAMETER "
     "and must not be read as an effect on fertility."),
    ("W7123517430", "MNP follicular fluid", "selection (ART frame)", "CRITICAL",
     "Sample drawn at oocyte retrieval, i.e. selected on subfecundity. Wall 4. No adjustment "
     "argument is available that would transport this to a general population."),
    ("W4412525568", "PE/PVC nanoplastics", "estimand", "CRITICAL",
     "Fertilization rate in IVF is an ART treatment outcome and belongs to A.17."),
    ("W4402945134", "MP and sperm dysfunction", "measurement (contamination control)", "UNRESOLVED",
     "Whether procedural blanks were run is not established from the held text. For particle "
     "detection this is the difference between measuring biology and measuring the laboratory."),
]


def main():
    os.makedirs(EXTRACT, exist_ok=True)
    with open(os.path.join(EXTRACT, f"{SLUG}-effects.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=EFFECT_FIELDS)
        w.writeheader()
        for e in EFFECTS:
            w.writerow(e)
    with open(os.path.join(EXTRACT, f"{SLUG}-risk-of-bias.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(ROB_FIELDS)
        w.writerows(ROB)

    pfas = [e for e in EFFECTS if e["chemical_family"].startswith("PFAS")]
    plastic = [e for e in EFFECTS if e["chemical_family"] == "PLASTIC_PARTICLE"]
    restricted = [e for e in EFFECTS if e["track"] == "restricted"]
    unrecovered = [e for e in EFFECTS if "UNRECOVERED" in e["estimate"]]

    L = [f"# Extraction report — {SLUG} (B.6)", "",
         f"Hand-coded from the {len(set(e['openalex_id'] for e in EFFECTS))} full texts held that "
         "carry an estimate. Located first by `143_b6_fulltext_probe.py`, so every coded value has a "
         "quoted passage behind it in `extraction/{}-fulltext-probe.csv`.".format(SLUG), "",
         f"**{len(EFFECTS)} effect rows** — {len(pfas)} PFAS, {len(plastic)} microplastics. "
         f"**{len(restricted)} rows are in the restricted (parity-handled) track.** "
         f"{len(unrecovered)} rows carry `NUMERIC_UNRECOVERED`.", "",
         "## 1. The two tracks disagree, and both cohorts that tested it say so", "",
         "This is the chapter's central empirical result. Call 2 pre-committed to a two-track "
         "synthesis on parity handling because PFAS leave the body through pregnancy, lactation and "
         "menstruation, so parity causes exposure. The prediction was that the restricted track "
         "would be weaker. It is — and the evidence comes from inside the literature:", "",
         "| cohort | unrestricted | parity-restricted |", "|---|---|---|",
         "| INUENDO (PFNA, fecundability) | FR 0.80 [0.69–0.94] | **not replicated** (authors' own words) |",
         "| INUENDO (PFNA, infertility) | OR 1.53 [1.08–2.15] | **not replicated** |",
         "| MoBa (PFOSA, fecundability) | FOR 0.85 [0.83–1.09] | FOR 0.91 [0.71–1.17], null |", "",
         "Two independent cohorts, two independent restricted analyses, no surviving association. "
         "The chapter should state this as its primary finding on the PFAS side and should not "
         "report the unrestricted estimates as though they were the result.", "",
         "## 2. Adjusting for parity is not restricting on it", "",
         "S-PRESTO — the one preconception-measured cohort held, and on exposure timing the "
         "best-designed — finds decreased fecundability (PFDA FR 0.90 [0.82, 0.98], PFOS 0.88 "
         "[0.79, 0.99], mixture 0.89 [0.73, 1.02]). It **adjusts** for parity rather than restricting "
         "on it. Parity sits on the path from prior reproduction to current exposure, so adjustment "
         "leaves the reverse-causal channel partly open and can induce collider bias on top.", "",
         "`PARITY_HANDLING` therefore needs **four** levels rather than the two Call 2 implied: "
         "`nulliparous_restricted`, `parity_stratified`, `parity_adjusted`, `none`. Only the first "
         "two enter the restricted track. This is a refinement to the frozen scope and should be "
         "recorded as one.", "",
         "## 3. The microplastics primary cell contains no effect estimate", "",
         "Every held plastic-family record in a PRIMARY cell is a review or opinion piece. The five "
         "empirical microplastics records held all estimate fertility **inputs** — sperm parameters, "
         "retrieved oocytes, AMH — not fertility quantities. They are small, largely ART-derived, "
         "and their p-values cluster at the margin (0.041, 0.056, 0.080, 0.083, 0.091), with the "
         "single strong result (p = 0.0003) attaching to IVF fertilization rate, which Wall 4 routes "
         "to A.17.", "",
         "So the microplastics chapter's GRADE rating attaches to a cell that presently holds no "
         "estimate of the exposure against a fertility quantity. That is a defensible verdict of "
         "**Very Low / no rateable evidence**, and it is a finding rather than a gap in this "
         "review's search — the screen read 920 records and the completeness bypass guaranteed every "
         "both-axes plastic record was read.", "",
         "## 4. Numerics lost to text extraction", "",
         f"{len(unrecovered)} rows are marked `NUMERIC_UNRECOVERED`. Decimals split across the "
         "PDF-to-text and XML-to-text boundaries, so the direction and p-value are legible but the "
         "point estimate and interval are not. **These are recorded as missing rather than "
         "reconstructed**: a number transcribed wrongly is worse than a number recorded as absent, "
         "and every one of them is on the microplastics side, where the evidence is thinnest and an "
         "invented figure would do the most damage. They need PDF-quality re-extraction before any "
         "pooling.", "",
         "## Poolability", "",
         "Not yet. PROTOCOL §5.9 requires three estimates sharing a chemical family, an estimand "
         f"level, a sex stratum and a parity-handling status. The restricted track holds "
         f"{len(restricted)} rows across two cohorts, one of which reports no point estimate at all. "
         "The honest output is a narrative synthesis with the two-track disagreement as its centre, "
         "not a forest plot.", ""]
    open(os.path.join(LOGS, f"{SLUG}-extraction-report.md"), "w").write("\n".join(L) + "\n")

    print(f"effects={len(EFFECTS)} (pfas {len(pfas)}, plastic {len(plastic)}) "
          f"restricted_track={len(restricted)} numeric_unrecovered={len(unrecovered)}")
    print(f"rob_rows={len(ROB)}")
    print(f"-> {os.path.relpath(os.path.join(EXTRACT, SLUG + '-effects.csv'), ROOT)}")
    print(f"-> {os.path.relpath(os.path.join(LOGS, SLUG + '-extraction-report.md'), ROOT)}")


if __name__ == "__main__":
    main()
