#!/usr/bin/env python3
"""
131_b7_extract_retrieved.py — B.7, PROTOCOL stages 6-8 for the records retrieved so far.

Writes the extraction table, the risk-of-bias assessment, and the routing resolutions for every full
text present in literature/pdfs/{slug}/. Extraction is HAND-CODED FROM FULL TEXT and recorded here
rather than in a notebook, so the value, its source, and the judgement behind it stay attached to
each other. The fields are the ones the search scope made mandatory, and the two that decide
everything are INDICATION_DESIGN (whether the estimate speaks to B.7 at all) and ESTIMAND_LEVEL
(which governs poolability).

FOUR FINDINGS FROM THIS BATCH, recorded here rather than buried in a cell:

  1. ONE study in the entire frame estimates a fertility hazard against antidepressant exposure while
     adjusting for the indication: Yland et al. 2022. Its fecundability ratio for current SSRI use is
     0.85 with a confidence interval of [0.65, 1.12] that includes the null, it is male-side, and it
     is one cohort. The chapter's quantitative claim rests on that interval and on nothing else.

  2. THE PAPER SAYS SO ITSELF. Yland et al. state that no studies had evaluated the relationship
     between psychotropic medication use and directly measured fertility outcomes. An independent
     confirmation, from inside the literature, of what the screen found from outside it.

  3. BOTH HELD RECORDS ROUTE OUT AT FULL TEXT, and both were held for the right reason. The
     vilazodone study is in male rats (Wall 7) and the paternal-SSRI cohort measures outcomes in
     13,547 exposed children (Wall 4). Neither could have been settled from its abstract, and
     guessing would have produced one false inclusion and one false exclusion.

  4. THE INDICATION'S EFFECT IS LARGER THAN THE MEDICATION'S AND BETTER MEASURED. The Norwegian
     register puts completed fertility at 1.34 against 1.60 for women with depression through the
     reproductive period, and 0.90 against 1.41 for men. B.7 claims a decrement on top of that.

Output: extraction/{slug}-effects.csv
        extraction/{slug}-risk-of-bias.csv
        extraction/{slug}-routing-resolutions.csv
        literature/search-logs/{slug}-extraction-report.md
"""
import csv, os

SLUG = "antidepressants-ssri-subfecundity"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")

EFFECT_FIELDS = [
    "openalex_id", "doi", "study", "year", "venue", "country", "period", "design", "sample",
    "sex", "cell", "link", "drug_class", "exposure_measure", "indication_design", "estimand_level",
    "outcome", "effect", "effect_units", "ci", "includes_null", "ascertainment",
    "baseline_established", "exposure_duration", "confounders_adjusted", "poolable_with",
    "extractor_note",
]

EFFECTS = [
    dict(openalex_id="W4211211986", doi="10.1177/15579883221075520",
         study="Yland et al.", year=2022, venue="American Journal of Men's Health",
         country="US and Canada", period="2013-2020", design="prospective preconception cohort",
         sample="2,398 men attempting conception <=6 cycles at entry", sex="male",
         cell="PRIMARY_MEDICATION_TO_FERTILITY", link="direct-to-fertility",
         drug_class="SSRI", exposure_measure="self-reported current medication name",
         indication_design="adjusted for depression diagnosis, MDI symptom score, and other "
                           "psychotropic classes; no active comparator and no within-person contrast",
         estimand_level="HAZARD_DECREMENT",
         outcome="fecundability (per-cycle conception probability)",
         effect="0.85", effect_units="fecundability ratio (FR), <1 = reduced",
         ci="[0.65, 1.12]", includes_null="YES",
         ascertainment="n/a (fertility outcome, not a dysfunction measure)",
         baseline_established="yes - MDI measured at baseline",
         exposure_duration="current use at baseline; duration not measured",
         confounders_adjusted="male and female age, race/ethnicity, both educations, METs, alcohol, "
                              "BMI, smoking, prior paternity, other psychotropic classes",
         poolable_with="nothing - it is the only estimate at this level in the frame",
         extractor_note="THE CHAPTER'S ONLY IDENTIFIED ESTIMATE. 104 men (4.3%) were current SSRI "
                        "users. Sensitivity restricting to the incident attempt period attenuates it "
                        "to FR 0.91 [0.66, 1.26]. The interval includes the null at both."),
    dict(openalex_id="W4211211986", doi="10.1177/15579883221075520",
         study="Yland et al.", year=2022, venue="American Journal of Men's Health",
         country="US and Canada", period="2013-2020", design="prospective preconception cohort",
         sample="48 men on SNRI/other antidepressants", sex="male",
         cell="PRIMARY_MEDICATION_TO_FERTILITY", link="direct-to-fertility",
         drug_class="SNRI / tricyclic / atypical", exposure_measure="self-reported current use",
         indication_design="as above", estimand_level="HAZARD_DECREMENT",
         outcome="fecundability", effect="1.03", effect_units="fecundability ratio",
         ci="[0.71, 1.48]", includes_null="YES", ascertainment="n/a",
         baseline_established="yes", exposure_duration="current use at baseline",
         confounders_adjusted="as above",
         poolable_with="not pooled with the SSRI row - different drug class",
         extractor_note="POINT ESTIMATE ABOVE 1. Non-SSRI antidepressants show no decrement and a "
                        "central estimate on the beneficial side. The chapter must not report a "
                        "class-wide effect it does not have."),
    dict(openalex_id="W4211211986", doi="10.1177/15579883221075520",
         study="Yland et al.", year=2022, venue="American Journal of Men's Health",
         country="US and Canada", period="2013-2020", design="mediation analysis within the cohort",
         sample="2,398 men", sex="male", cell="LINK2_FUNCTION_TO_COITAL_FREQUENCY", link="2",
         drug_class="any psychotropic", exposure_measure="self-reported current use",
         indication_design="mediation with exposure-mediator interaction",
         estimand_level="HAZARD_DECREMENT", outcome="proportion of the depression-fecundability "
                                                    "association mediated by intercourse frequency",
         effect="0.17", effect_units="proportion mediated", ci="not reported",
         includes_null="not stated", ascertainment="self-reported intercourse frequency",
         baseline_established="yes", exposure_duration="n/a",
         confounders_adjusted="as the main model",
         poolable_with="nothing",
         extractor_note="THE ONLY QUANTITATIVE LINK-2 EVIDENCE IN THE CHAPTER, and it is a mediation "
                        "proportion for DEPRESSION rather than for medication. 17% of the "
                        "depression-fecundability association runs through intercourse frequency; "
                        "44% runs through psychotropic use and 19% through SSRI use specifically. "
                        "The behavioural pathway the hypothesis is built on is the smallest of the "
                        "three, in the one study that measured all of them."),
    dict(openalex_id="W4394578177", doi="10.3390/jcm13072129",
         study="Al-Zaidi et al.", year=2024, venue="Journal of Clinical Medicine",
         country="not stated in the extracted text", period="not stated",
         design="retrospective comparison, SSRI vs non-SSRI cohorts in an infertility clinic",
         sample="29 infertile men on SSRIs", sex="male", cell="ENDOCRINE_MECHANISM", link="mechanism",
         drug_class="escitalopram, fluoxetine, paroxetine",
         exposure_measure="clinic prescription record",
         indication_design="none - SSRI users compared with non-users within an infertile population",
         estimand_level="HAZARD_DECREMENT",
         outcome="sperm liquefaction, motility, viscosity, count",
         effect="null on all four", effect_units="p-values",
         ci="p = 0.10 / 0.17 / 0.16 / 0.069 respectively", includes_null="YES",
         ascertainment="laboratory semen analysis",
         baseline_established="no", exposure_duration="reported, no significant difference by agent",
         confounders_adjusted="age only",
         poolable_with="the semen-parameter stream, not the primary cell",
         extractor_note="A NULL, retained deliberately. The mechanism stream's positive findings come "
                        "from small clinical series and the counterweight belongs in the record. "
                        "Count is the closest to conventional significance (p = 0.069) and the "
                        "authors flag it. Selected on infertility, so it cannot transport."),
    dict(openalex_id="W7126064928", doi="10.3389/fphar.2026.1765071",
         study="Gong et al.", year=2026, venue="Frontiers in Pharmacology",
         country="international (FAERS and EudraVigilance)",
         period="FAERS 2004Q1-2025Q2; EV 2002-2025",
         design="pharmacovigilance disproportionality, four concordant signal methods",
         sample="1,955 FAERS and 1,384 EV male reproductive-toxicity cases, median age 35",
         sex="male", cell="PRIMARY_MALE_FECUNDITY", link="direct-to-fertility",
         drug_class="multiple, antidepressants among them",
         exposure_measure="spontaneous adverse-event report",
         indication_design="none - disproportionality has no denominator and no comparator",
         estimand_level="HAZARD_DECREMENT",
         outcome="reporting signal for male infertility or sperm abnormality",
         effect="signal present", effect_units="ROR / PRR / IC / EBGM, all four thresholds required",
         ci="reported per drug, not extracted here", includes_null="n/a",
         ascertainment="spontaneous reporting - the weakest ascertainment in the chapter",
         baseline_established="no", exposure_duration="not measured",
         confounders_adjusted="none possible",
         poolable_with="nothing - a disproportionality signal is not an effect size",
         extractor_note="Carried as a SIGNAL and never as a magnitude. Spontaneous-report data cannot "
                        "estimate incidence and are subject to notoriety bias, which for a widely "
                        "publicised side effect runs in the direction of over-reporting."),
]

ROB_FIELDS = ["openalex_id", "study", "tool", "confounding", "selection", "exposure_measurement",
              "missing_data", "outcome_measurement", "reported_result", "overall", "rationale"]

ROB = [
    dict(openalex_id="W4211211986", study="Yland et al. 2022", tool="ROBINS-I",
         confounding="SERIOUS", selection="MODERATE", exposure_measurement="SERIOUS",
         missing_data="LOW", outcome_measurement="LOW", reported_result="LOW",
         overall="SERIOUS",
         rationale="Confounding is serious and irreducible by adjustment: the authors control for "
                   "depression diagnosis and symptom score, which is the best available, but "
                   "prescription is driven by severity and by help-seeking that the MDI does not "
                   "capture, and there is no active comparator or within-person contrast. Exposure "
                   "is self-reported current use with no duration and no adherence. Selection is "
                   "moderate: a volunteer preconception cohort of couples already trying is, by "
                   "construction, the population in which coital frequency is LEAST likely to bind, "
                   "which biases toward the null for the behavioural pathway specifically. Outcome "
                   "ascertainment and reporting are strong. Rated SERIOUS, not CRITICAL, because the "
                   "direction of the residual confounding is arguable rather than certain."),
    dict(openalex_id="W4394578177", study="Al-Zaidi et al. 2024", tool="ROBINS-I",
         confounding="CRITICAL", selection="CRITICAL", exposure_measurement="MODERATE",
         missing_data="MODERATE", outcome_measurement="LOW", reported_result="MODERATE",
         overall="CRITICAL",
         rationale="Sample is 29 exposed men drawn from an infertility clinic, so the population is "
                   "selected on the outcome's antecedent and the comparison is unadjusted beyond "
                   "age. A null from a design this weak is close to uninformative in either "
                   "direction, and is retained for the record rather than for the estimate."),
    dict(openalex_id="W7126064928", study="Gong et al. 2026", tool="ROBINS-I (adapted)",
         confounding="CRITICAL", selection="CRITICAL", exposure_measurement="SERIOUS",
         missing_data="n/a", outcome_measurement="SERIOUS", reported_result="LOW",
         overall="CRITICAL",
         rationale="Spontaneous-report disproportionality has no denominator, no comparator group "
                   "and no exposure time. It can say that a signal exists; it cannot say how large "
                   "the effect is or whether it is causal. Notoriety bias is a first-order concern "
                   "for a side effect with an active patient-advocacy literature. Reported "
                   "methodology is careful, which does not repair the design."),
    dict(openalex_id="W2013874757", study="Tanrikut and Schlegel and predecessors (NOT RETRIEVED)",
         tool="ROBINS-I", confounding="NOT ASSESSED", selection="NOT ASSESSED",
         exposure_measurement="NOT ASSESSED", missing_data="NOT ASSESSED",
         outcome_measurement="NOT ASSESSED", reported_result="NOT ASSESSED",
         overall="PENDING RETRIEVAL",
         rationale="Recorded as pending rather than omitted. Fourteen of the twenty primary-cell "
                   "records could not be retrieved through any open route and are not assessed; a "
                   "risk-of-bias table that silently listed only what was obtainable would read as a "
                   "complete assessment of a complete evidence base."),
]

# Records held at the screen and settled at full text. Both route OUT, and neither could have been
# settled from an abstract.
ROUTING = [
    dict(openalex_id="W2235481714", doi="10.1007/s00213-015-4198-1",
         held_as="INSUFFICIENT_INFO (species undetermined)",
         resolved_to="OFF_ANIMAL",
         evidence="Title and methods: 'sexual behaviors and serotonin transporter and receptors in "
                  "male rats'; Utrecht Institute for Pharmaceutical Sciences.",
         note="Wall 7. The screen refused to guess the species from the venue and the topic, and the "
              "guess would have been wrong in the direction of a false inclusion: this is a "
              "behavioural sexual-function study, which is exactly the link-1 shape the chapter is "
              "short of."),
    dict(openalex_id="W4394957444", doi="10.1111/andr.13646",
         held_as="ROUTING_DEFERRED_TO_FULLTEXT (outcome set not named)",
         resolved_to="OFF_PREGNANCY_SAFETY",
         evidence="Nationwide cohort of 13,547 children exposed via PATERNAL preconception SSRI use; "
                  "outcomes are adverse birth and early-life outcomes in the offspring.",
         note="Wall 4. Paternal preconception exposure sounded like a fertility design and is not: "
              "the sample is conditioned on a birth having occurred and the outcomes belong to the "
              "child. Conclusion is that paternal preconception SSRI use is 'in general safe'."),
]


def write_csv(path, fields, rows):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    os.makedirs(EXTRACT, exist_ok=True)
    write_csv(os.path.join(EXTRACT, f"{SLUG}-effects.csv"), EFFECT_FIELDS, EFFECTS)
    write_csv(os.path.join(EXTRACT, f"{SLUG}-risk-of-bias.csv"), ROB_FIELDS, ROB)
    write_csv(os.path.join(EXTRACT, f"{SLUG}-routing-resolutions.csv"),
              ["openalex_id", "doi", "held_as", "resolved_to", "evidence", "note"], ROUTING)

    primary = [e for e in EFFECTS if e["cell"].startswith("PRIMARY_")]
    identified = [e for e in primary if "adjusted for depression" in e["indication_design"]]

    L = [f"# Extraction report — {SLUG} (B.7)", "",
         f"Extracted from the {len(set(e['openalex_id'] for e in EFFECTS))} records for which full "
         "text was obtainable through an open route. Fourteen of the twenty primary-cell records "
         "could not be retrieved and are listed as pending in the risk-of-bias table rather than "
         "omitted from it.", "",
         "## What the extraction found", "",
         f"**{len(EFFECTS)} effect rows from {len(set(e['openalex_id'] for e in EFFECTS))} studies. "
         f"{len(identified)} of them adjust for the indication at all, and they come from one "
         "cohort.**", "",
         "| study | design | exposure | outcome | effect | includes null |", "|---|---|---|---|---|---|"]
    for e in EFFECTS:
        L.append(f"| {e['study']} {e['year']} | {e['design'][:38]} | {e['drug_class']} | "
                 f"{e['outcome'][:38]} | {e['effect']} {e['ci']} | {e['includes_null']} |")

    L += ["", "## No pooling", "",
          "PROTOCOL 5.9 directs meta-analysis at three or more studies with extractable effect "
          "sizes. The count is met only by counting rows rather than studies, and the rows are not "
          "commensurable: a fecundability ratio, a set of semen-parameter p-values, and a "
          "pharmacovigilance signal do not share an estimand, an outcome scale, or a population. "
          "Pooling them would produce a number with no referent. Narrative synthesis, with the "
          "single identified estimate reported as such.", "",
          "## Both held records route out, and the deferral rule earned its keep", "",
          "| record | held as | resolved to | why it could not be settled earlier |", "|---|---|---|---|"]
    for r in ROUTING:
        L.append(f"| `{r['openalex_id']}` | {r['held_as']} | **{r['resolved_to']}** | "
                 f"{r['note'][:150]} |")
    L += ["",
          "The vilazodone study is the more instructive of the two. Its abstract describes a "
          "comparison of antidepressants on sexual behaviour, which is precisely the link-1 evidence "
          "the chapter is short of, and it is in rats. A screen that inferred species from topic "
          "would have admitted it.", "",
          "## The gap retrieval cannot close", "",
          "The two records that would most change this chapter are both unavailable through any open "
          "route: Yland et al.'s female-side companion in AJOG (PMC11064128, not in the open-access "
          "subset) and the Fertility and Sterility study that names depression and antidepressant "
          "use together against male and female fertility (PMC5973807, likewise). Both have PMC "
          "identifiers and neither is open. This is a library-proxy task, not a scripting task.", "",
          "## Risk of bias, in one sentence", "",
          "Every retrieved estimate is SERIOUS or CRITICAL on ROBINS-I, and the binding domain is "
          "the same one in all of them: nobody has an active comparator, a within-person contrast, "
          "or an instrument for prescribing, so the medication cannot be separated from the reason "
          "it was prescribed."]
    open(os.path.join(LOGS, f"{SLUG}-extraction-report.md"), "w").write("\n".join(L) + "\n")

    print(f"effects={len(EFFECTS)} studies={len(set(e['openalex_id'] for e in EFFECTS))} "
          f"rob={len(ROB)} routing_resolved={len(ROUTING)}")
    print(f"-> extraction/{SLUG}-effects.csv")


if __name__ == "__main__":
    main()
