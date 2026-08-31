#!/usr/bin/env python3
"""267 — A.18 extraction table. TICK-076.

Emits `extraction/heritability-fertility-genetic.csv` from verified full-text
reads. The table is GENERATED, never hand-typed: every numeric cell carries the
quoted sentence it came from, so an RA verifying the 10% sample checks a claim
against its own source rather than against my transcription.

Fields follow scope-memo §9. `design_class` is a GATE: a study whose design does
not match one of the listed classes is written as `UNLISTED_*` and fails loudly
rather than defaulting into the nearest class and pooling with it.

**The most important row in this file is a study that refutes its own headline
estimate.** Ísleifsson et al. on Iceland reports narrow-sense h² = 0.137 (SE 0.02)
for lifetime reproductive success from IBD-based REML on 8,456 full sibling pairs
— and then, adding a family effect and letting it compete with relatedness,
reports f² = 0.129 (0.03) and **a genetic effect of 0.00 (0.05)**, concluding in
its own words that "the heritability estimate (h2 = 0.137) was based solely on
shared family effects among full siblings and was not due to shared genes."
Extracting the headline 0.137 would record the OPPOSITE of what the study found.
Both values are carried, with `estimate_superseded_by_authors` set.

Usage: python3 source/build/goldset/267_a18_build_extraction_table.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
OUT = ROOT / "extraction" / "heritability-fertility-genetic.csv"

FIELDS = ["openalex", "study", "year", "cell", "arm", "design_class",
          "relatedness_level", "exposure_distance", "outcome_measure",
          "estimand", "estimate", "se", "units", "n", "cohort_window",
          "phenomenon_window", "cohort_complete", "sample_selection",
          "assortative_mating_handled", "estimate_superseded_by_authors",
          "extraction_status", "source_quote"]

# Verified by full-text read, 2026-08-31. Each `source_quote` is the sentence the
# number was read from, quoted verbatim from the retrieved text.
#
# The openalex ids below are RESOLVED FROM THE CORPUS BY TITLE, not typed from
# memory. The first draft of this file hand-typed them and every one was wrong,
# which silently produced 4 orphan rows and 56 (not 52) "pending" ones -- the join
# key corrupted in exactly the way the match-by-content rule exists to prevent.
# The row count is the check: verified + pending must equal the corpus size.
ROWS = [
    dict(openalex="W4414345371", study="Within-family heritability estimates, UK Biobank",
         year=2025, cell="WITHIN_VS_POPULATION", arm="METHOD",
         design_class="sibling_IBD_regression", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="children_ever_born",
         estimand="h2_within_family", estimate="0.27", se="0.11", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="unclear",
         sample_selection="volunteer_biobank", assortative_mating_handled="yes",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="We find substantial heritability for smoking initiation (0.34 +/- 0.05), "
                      "alcohol consumption (0.18 +/- 0.04), number of children (0.27 +/- 0.11)"),
    dict(openalex="W2337218734", study="Tropf et al., mega-analysis of 31,396 across 6 countries",
         year=2016, cell="H2_MODERATION", arm="H2_MOD",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="children_ever_born",
         estimand="h2_SNP_baseline", estimate="0.038", se="0.0097", units="variance_share",
         n="31396", cohort_window="1903-1958", phenomenon_window="FDT|SDT",
         cohort_complete="yes", sample_selection="population_register_and_cohort",
         assortative_mating_handled="no", estimate_superseded_by_authors="no",
         extraction_status="VERIFIED",
         source_quote="For NEB, h2SNP is 0.038 (SE = 0.0097, p-value = 2.0x10-5) and for AFB "
                      "it is 0.053 (SE = 0.019)"),
    dict(openalex="W2337218734", study="Tropf et al., mega-analysis of 31,396 across 6 countries",
         year=2016, cell="H2_MODERATION", arm="H2_MOD",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="children_ever_born",
         estimand="h2_SNP_with_cohort_and_population_interaction", estimate="0.22", se="0.026",
         units="variance_share", n="31396", cohort_window="1903-1958",
         phenomenon_window="FDT|SDT", cohort_complete="yes",
         sample_selection="population_register_and_cohort", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="The overall h2SNP for NEB increases almost fivefold, from 0.04 (SE = 0.01; "
                      "Model 1) to 0.22 (SE = 0.026), when population and demographic cohort are "
                      "taken into account"),
    dict(openalex="W2573112139", study="Isleifsson et al., parental investment and LRS, Iceland",
         year=2017, cell="PEDIGREE_RESPONSE", arm="SELECTION",
         design_class="pedigree_IBD_REML", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="lifetime_reproductive_success",
         estimand="h2_narrow_sense_no_family_effect", estimate="0.137", se="0.02",
         units="variance_share", n="8456_sibling_pairs", cohort_window="1700-1920",
         phenomenon_window="PM|FDT", cohort_complete="yes",
         sample_selection="national_genealogy_plus_deCODE",
         assortative_mating_handled="no",
         estimate_superseded_by_authors="YES — see the row below; the authors show this value is "
                                        "shared family environment, not genes",
         extraction_status="VERIFIED_BUT_SUPERSEDED",
         source_quote="A restricted maximum likelihood model (REML) entering the precise "
                      "coefficients of relatedness for 8,456 pairs of full siblings yielded a "
                      "narrow sense heritability estimate (h2) of 0.137 with a standard error of (0.02)"),
    dict(openalex="W2573112139", study="Isleifsson et al., parental investment and LRS, Iceland",
         year=2017, cell="PEDIGREE_RESPONSE", arm="SELECTION",
         design_class="pedigree_IBD_REML", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="lifetime_reproductive_success",
         estimand="h2_narrow_sense_family_effect_competing", estimate="0.00", se="0.05",
         units="variance_share", n="8456_sibling_pairs", cohort_window="1700-1920",
         phenomenon_window="PM|FDT", cohort_complete="yes",
         sample_selection="national_genealogy_plus_deCODE", assortative_mating_handled="no",
         estimate_superseded_by_authors="no — THIS is the authors' preferred estimate",
         extraction_status="VERIFIED_AUTHORS_PREFERRED",
         source_quote="revealed a family effect (f2) of 0.129 (0.03) and a genetic effect of 0.00 "
                      "(0.05) This suggests that the heritability estimate (h2 = 0.137) was based "
                      "solely on shared family effects among full siblings and was not due to shared genes"),
    dict(openalex="W1562851158", study="Quebec biocultural origins of human capital (Galor & Klemp)",
         year=2014, cell="PEDIGREE_RESPONSE", arm="SELECTION",
         design_class="pedigree_parent_offspring", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="time_to_first_birth",
         estimand="h2_narrow_sense", estimate="0.04", se="", units="variance_share",
         n="", cohort_window="1660-1685", phenomenon_window="PM", cohort_complete="yes",
         sample_selection="parish_genealogy", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="In the Quebec sample the time from marriage to first birth is heritable "
                      "(h2 = 0.04)"),
    dict(openalex="W2033634275", study="Briley/Harden/Tucker-Drob, Genotype x Cohort Interaction",
         year=2014, cell="H2_MODERATION", arm="H2_MOD",
         design_class="twin_MZDZ", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="completed_fertility",
         estimand="additive_genetic_path_cohort_linear_term_SPLINE", estimate="-0.032", se="0.014",
         units="path_coefficient_per_cohort_year", n="5600", cohort_window="1920-1955",
         phenomenon_window="FDT|SDT", cohort_complete="yes", sample_selection="twin_registry",
         assortative_mating_handled="no",
         estimate_superseded_by_authors="no — but SIGN-DISCORDANT with the quartic specification "
                                        "in the same table; see the row below",
         extraction_status="VERIFIED_SPECIFICATION_DISCORDANT",
         source_quote="a .350 (.424) | a-prime -.032 (.014) * [Completed Fertility, Spline] "
                      "(PMC Table 1; standard errors in parentheses)"),
    dict(openalex="W2033634275", study="Briley/Harden/Tucker-Drob, Genotype x Cohort Interaction",
         year=2014, cell="H2_MODERATION", arm="H2_MOD",
         design_class="twin_MZDZ", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="completed_fertility",
         estimand="additive_genetic_path_cohort_linear_term_QUARTIC", estimate="0.016", se="0.009",
         units="path_coefficient_per_cohort_year", n="5600", cohort_window="1920-1955",
         phenomenon_window="FDT|SDT", cohort_complete="yes", sample_selection="twin_registry",
         assortative_mating_handled="no",
         estimate_superseded_by_authors="no — SIGN-DISCORDANT with the spline row above",
         extraction_status="VERIFIED_SPECIFICATION_DISCORDANT",
         source_quote="a .498 (.105) *** | a-prime .016 (.009) dagger [Completed Fertility, "
                      "Quartic] (PMC Table 1)"),
    dict(openalex="W2169871877", study="Brandenburg et al., fertility transmission and coalescent trees",
         year=2012, cell="THEORY", arm="THEORY",
         design_class="UNLISTED_coalescent_simulation", relatedness_level="",
         exposure_distance="NOT_GENETIC", outcome_measure="genealogy_imbalance_and_Ne",
         estimand="none_empirical", estimate="", se="", units="", n="",
         cohort_window="", phenomenon_window="", cohort_complete="",
         sample_selection="simulation", assortative_mating_handled="",
         estimate_superseded_by_authors="",
         extraction_status="RECLASSIFIED_OUT_OF_PREDICTED_RESPONSE",
         source_quote="Individual-based coalescent simulation; outcomes are coalescent-tree "
                      "imbalance and effective population size, not a human fertility estimate. "
                      "Screened into PREDICTED_RESPONSE on title/abstract; the full text shows no "
                      "empirical h2, S or R. PREDICTED_RESPONSE therefore has ZERO usable full texts."),
    dict(openalex="W2084434401", study="Sgro & Hoffmann, Genetic correlations, tradeoffs and environmental variation",
         year=2004, cell="OFF_SPECIES", arm="NONE",
         design_class="UNLISTED_review_nonhuman", relatedness_level="",
         exposure_distance="NOT_GENETIC", outcome_measure="",
         estimand="none_human", estimate="", se="", units="", n="",
         cohort_window="", phenomenon_window="", cohort_complete="",
         sample_selection="", assortative_mating_handled="",
         estimate_superseded_by_authors="",
         extraction_status="RECLASSIFIED_OUT_OF_PEDIGREE_RESPONSE",
         source_quote="Heredity review of correlated response to selection in insects and plants "
                      "(grain yield, egg size, larval food environments). No human pedigree data. "
                      "Screen design value was a hypothesis; the full text refutes it."),
    dict(openalex="W2128269372", study="Wang et al., post-reproductive lifespan and family size, Framingham",
         year=2013, cell="SELECTION_DIFFERENTIAL", arm="SELECTION",
         design_class="pedigree_parent_offspring", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="children_ever_born",
         estimand="h2_narrow_sense", estimate="0.09", se="", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="yes",
         sample_selection="cohort_study_Framingham", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="the heritabilities of most major life-history traits differed significantly "
                      "from zero, including age at death (h2 = 0.12, P = 0.01), CEB (h2 = 0.09, "
                      "P = 0.03), age at first birth (h2 = 0.18, P < 0.001)"),
    dict(openalex="W2342100485", study="Day et al., determinants of reproductive onset and success",
         year=2016, cell="H2_FERTILITY", arm="H2",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="age_at_first_birth",
         estimand="h2_SNP", estimate="0.290", se="0.015", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="unclear",
         sample_selection="volunteer_biobank", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="moderate heritability for AFS both in men (h=0.248, s.e. 0.010) and in "
                      "women (h=0.242, s.e. 0.010), and also moderate heritability for AFB "
                      "(h=0.290, s.e. 0.015, women only)"),
    dict(openalex="W2731861498", study="Sexual dimorphism in the genetic influence on childlessness",
         year=2017, cell="H2_FERTILITY", arm="H2",
         design_class="GREML_SNP", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="childlessness",
         estimand="h2_GREML_twin_sample", estimate="0.455", se="CI 0.341-0.569",
         units="variance_share", n="9942", cohort_window="", phenomenon_window="SDT",
         cohort_complete="yes", sample_selection="twin_registry",
         assortative_mating_handled="no", estimate_superseded_by_authors="no",
         extraction_status="VERIFIED",
         source_quote="Table 3 GREML analysis on childlessness in the twin sample ... Overall h2 "
                      "0.455*** 0.341 0.569 9942 | Female h2 0.591*** 0.413 0.769 5408 | Male h2 "
                      "0.563*** 0.394 0.732 4534"),
    dict(openalex="W590852753", study="Tropf et al., Human fertility, molecular genetics and natural selection",
         year=2015, cell="H2_FERTILITY", arm="H2",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="children_ever_born",
         estimand="h2_SNP", estimate="0.10", se="0.05", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="yes",
         sample_selection="population_cohort", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="Both traits have a significant genetic component, with h2SNP for NEB of "
                      "0.10 (SE 0.05) and for the AFB of 0.15 (SE 0.04)"),
    dict(openalex="W7169878769", study="Brigos-Barrios et al., genetic trade-offs in fertility and longevity",
         year=2026, cell="SELECTION_DIFFERENTIAL", arm="SELECTION",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="FERTILITY_PGS", outcome_measure="reproductive_success",
         estimand="h2_SNP", estimate="0.03", se="0.0014", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="unclear",
         sample_selection="volunteer_biobank", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="SNP-based heritability of reproductive success was modest but significant "
                      "(h2 = 0.03, s.e. = 1.4 x 10-3)"),
    dict(openalex="W4411477116", study="Why do we get sick? [medRxiv preprint of W7169878769]",
         year=2025, cell="SELECTION_DIFFERENTIAL", arm="SELECTION",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="FERTILITY_PGS", outcome_measure="reproductive_success",
         estimand="h2_SNP", estimate="0.03", se="0.0014", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="unclear",
         sample_selection="volunteer_biobank", assortative_mating_handled="no",
         estimate_superseded_by_authors="",
         extraction_status="DUPLICATE_OF_W7169878769_DO_NOT_POOL",
         source_quote="medRxiv preprint of the Nature Ecology & Evolution paper, RETITLED on "
                      "publication so title-based dedup could not pair them. Same authors, same "
                      "estimate (h2 = 0.03, s.e. 1.4e-3). One study, counted twice in the 148."),
    dict(openalex="W2110308604", study="Unraveling the intergenerational transmission of fertility (DF models, historical cohorts)",
         year=2013, cell="H2_MODERATION", arm="H2_MOD",
         design_class="sibling_DeFries_Fulker", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="completed_fertility",
         estimand="h2_by_birth_cohort_FEMALE_sibs", estimate="0.39->0.46", se="0.25->0.16",
         units="variance_share_per_cohort", n="", cohort_window="1810-1860",
         phenomenon_window="FDT", cohort_complete="yes", sample_selection="historical_parish_sibs",
         assortative_mating_handled="no",
         estimate_superseded_by_authors="no — but SEX-DISCORDANT, see the row below",
         extraction_status="VERIFIED_CELL_RECLASSIFIED_FROM_H2_FERTILITY",
         source_quote="Table 2 ... Female sibs 1810 .. 0.39 0.25 | 1840 0.30 0.13 0.02 | "
                      "1850 0.46 0.13 0.00 | 1860 0.46 0.16 0.01 (simple DF, h2 columns). "
                      "NB the source renders minus signs as '2' (e.g. '20.05' = -0.05)."),
    dict(openalex="W2110308604", study="Unraveling the intergenerational transmission of fertility (DF models, historical cohorts)",
         year=2013, cell="H2_MODERATION", arm="H2_MOD",
         design_class="sibling_DeFries_Fulker", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="completed_fertility",
         estimand="h2_by_birth_cohort_MALE_sibs", estimate="0.37->0.07", se="0.29->0.17",
         units="variance_share_per_cohort", n="", cohort_window="1810-1860",
         phenomenon_window="FDT", cohort_complete="yes", sample_selection="historical_parish_sibs",
         assortative_mating_handled="no",
         estimate_superseded_by_authors="no — OPPOSITE trend to the female row above",
         extraction_status="VERIFIED_CELL_RECLASSIFIED_FROM_H2_FERTILITY",
         source_quote="Table 2 ... Male sibs 1810 .. 0.37 0.29 0.20 | 1820 0.47 0.16 0.00 | "
                      "1850 0.21 0.15 0.15 | 1860 0.07 0.17 0.67 (simple DF, h2 columns)"),
    dict(openalex="W2052070884", study="Genome-Wide Association Study of Parity in Bangladeshi Women",
         year=2015, cell="H2_FERTILITY", arm="H2",
         design_class="GREML_SNP", relatedness_level="POPULATION",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="children_ever_born",
         estimand="h2_SNP", estimate="0.149", se="0.24", units="variance_share",
         n="", cohort_window="", phenomenon_window="SDT", cohort_complete="unclear",
         sample_selection="population_cohort_Bangladesh", assortative_mating_handled="no",
         estimate_superseded_by_authors="no — NOT significant (p = 0.265); a null, and the only "
                                        "non-European-ancestry estimate in the set so far",
         extraction_status="VERIFIED_NULL",
         source_quote="children (hg2 = 0.149, SE = 0.24, p-value = 0.265) and number of pregnancies "
                      "(hg2 = 0.007, SE = 0.22, p-value = 0.487)"),
    dict(openalex="W2092739320", study="Byars/Stearns, demographic transition, variance in fitness, selection on height and BMI",
         year=2013, cell="H2_MODERATION", arm="H2_MOD",
         design_class="pedigree_parent_offspring", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="reproductive_success",
         estimand="standardized_linear_selection_gradient_via_fertility_HEIGHT",
         estimate="-0.0469", se="", units="standardized_gradient", n="812",
         cohort_window="pre/post 1974", phenomenon_window="SDT", cohort_complete="yes",
         sample_selection="cohort_study", assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="Table 1 Time Changes in Linear Selection by Fitness Components ... "
                      "Fertility -4.69 x 10-2 +4.44 x 10-3 +0.36 0.01 [height]"),
    dict(openalex="W1985105482", study="Pettay et al., natural selection on female life-history by socio-economic class, Finland",
         year=2007, cell="PEDIGREE_RESPONSE", arm="SELECTION",
         design_class="pedigree_parent_offspring", relatedness_level="WITHIN_FAMILY",
         exposure_distance="ANONYMOUS_VARIANCE", outcome_measure="lifetime_reproductive_success",
         estimand="opportunity_for_selection_I_LRS_by_wealth", estimate="0.287|0.357|0.660",
         se="", units="variance_in_relative_fitness", n="", cohort_window="18th-19th century",
         phenomenon_window="PM|FDT", cohort_complete="yes", sample_selection="parish_genealogy",
         assortative_mating_handled="no",
         estimate_superseded_by_authors="no", extraction_status="VERIFIED",
         source_quote="Rich Middle-class Poor chi2 P | I LRS 0.287 0.357 0.660 5.99 0.003 | "
                      "I fec 0.197 0.266 0.504 2.80 0.06 (pre-industrial Finnish women)"),
]


def main():
    cand = {r["openalex"]: r for r in json.loads((TEMP / "extraction-candidates.json").read_text())}
    done = {r["openalex"] for r in ROWS}
    rows = list(ROWS)
    for oid, c in cand.items():
        if oid in done:
            continue
        rows.append({**{f: "" for f in FIELDS}, "openalex": oid,
                     "study": (c.get("title") or "")[:120], "cell": c.get("cell"),
                     "arm": c.get("arm"),
                     "exposure_distance": c.get("screen_exposure_distance"),
                     "design_class": ("UNRESOLVED_MULTIPLE_MARKERS"
                                      if c.get("design_class_UNRESOLVED") else
                                      (c.get("design_markers") or ["UNLISTED_NONE_DETECTED"])[0]),
                     "extraction_status": "PENDING_SECOND_PASS",
                     "source_quote": ""})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({f: r.get(f, "") for f in FIELDS})
    from collections import Counter
    orphans = [r["openalex"] for r in ROWS if r["openalex"] not in cand]
    assert not orphans, (f"openalex ids not present in the corpus: {orphans} — the join key is "
                         f"wrong; resolve ids from the corpus, do not type them")
    assert len(rows) == len(cand) + (len(ROWS) - len({r["openalex"] for r in ROWS})), \
        "row count does not reconcile against the corpus"
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(rows)} rows)")
    print("status:", dict(Counter(r.get("extraction_status") for r in rows)))
    print("verified rows by cell:",
          dict(Counter(r["cell"] for r in rows if str(r.get("extraction_status", "")).startswith("VERIFIED"))))


if __name__ == "__main__":
    main()
