#!/usr/bin/env python3
"""
122_b5_extract_retrieved.py — B.5, stages 6-8 for the records retrieved so far.

Writes the extraction table, the retrieval log, and the risk-of-bias assessment for every PDF present
in literature/pdfs/{slug}/. Extraction is HAND-CODED FROM FULL TEXT and recorded here rather than in a
notebook, so that the value, its page, and the judgement behind it stay attached to each other. The
fields are the ones the search scope made mandatory, and the two that decide everything are
ESTIMAND_LEVEL (which governs poolability) and INDUCED_SEPARATION (Wall 4).

Two findings from this batch are recorded in the log rather than buried in a cell:

  1. The Morocco study estimates B.5's primary estimand at the ACCOUNTING_SHARE level, by construction
     — its potential-fertility measure adds fetal deaths to live births, which assumes a lost
     conception would have been a live birth and models no replacement. This is the one published
     estimate of the chapter's headline quantity, and it is the upper bound the chapter argues it is.
  2. Valente REROUTES on retrieval. Its outcomes are fetal loss and sex ratio, not births per woman,
     so under the scope document's rule it is a determinant-to-loss estimate rather than a
     shock-to-births one. The routing gate did what it was built to do; the screen could not have
     known, because the abstract does not say.

Output: extraction/{slug}-effects.csv
        extraction/{slug}-risk-of-bias.csv
        extraction/{slug}-pdf-retrieval-log.csv
        literature/search-logs/{slug}-extraction-report.md
"""
import csv, json, os

SLUG = "fetal-loss-intrauterine-mortality"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)

EFFECT_FIELDS = [
    "openalex_id", "doi", "study", "year", "venue", "country", "period", "design",
    "sample", "cell_at_screen", "cell_at_fulltext", "estimand_level", "outcome",
    "effect", "effect_units", "ci_or_se", "loss_definition", "loss_window_weeks",
    "induced_separation", "replacement_treatment", "fertility_regime", "variation_source",
    "confounders_adjusted", "direction_established", "selection_viability", "poolable_with",
    "page", "extractor_note",
]

EFFECTS = [
    # ---------------- Mourchid & Bakass 2022, Morocco ----------------
    dict(openalex_id="W4283072838", doi="10.25133/jpssv302022.038",
         study="Mourchid & Bakass", year=2022,
         venue="Journal of Population and Social Studies 30:679-702",
         country="Morocco", period="2009-2010", design="Cross-sectional life table + Bongaarts/Leridon accounting",
         sample="National Demographic Survey 2009-2010", cell_at_screen="PRIMARY_LOSS_TO_FERTILITY",
         cell_at_fulltext="PRIMARY_LOSS_TO_FERTILITY", estimand_level="ACCOUNTING_SHARE",
         outcome="Total fertility rate, children per woman",
         effect="-9.4", effect_units="% of potential fertility lost to all intrauterine mortality",
         ci_or_se="none reported",
         loss_definition="IUM = early fetal mortality (EFM, defined by the authors as abortions PLUS miscarriages) + stillbirth (SB)",
         loss_window_weeks="EFM to 27 weeks; SB 28+ weeks (life table by gestational age; IUM quotient 272 per 1000 pregnancies)",
         induced_separation="NOT SEPARATED in the direct method. The authors define EFM as 'abortions + miscarriages'. Their own Bongaarts residual abortion index attributes 0.12 births/woman to INDUCED abortion against 0.14 births/woman for all EFM, so on their own numbers most of the EFM component is induced termination, i.e. A.4's estimand and not B.5's.",
         replacement_treatment="NONE. Potential fertility is constructed by ADDING fetal deaths to live births, so a lost conception is counted as a forgone live birth with no time cost and no replacement. This is why the estimand level is ACCOUNTING_SHARE.",
         fertility_regime="Controlled: TFR 2.17, contraceptive prevalence 67.4%, mean age at first marriage ~28.5",
         variation_source="Cross-sectional variation in reported pregnancy outcomes; urban/rural contrast",
         confounders_adjusted="None (descriptive accounting); urban/rural stratification only",
         direction_established="No. Accounting identity, not an identified effect.",
         selection_viability="Not addressed. Averted losses are treated as surviving births one-for-one.",
         poolable_with="Other ACCOUNTING_SHARE estimates only. NEVER with an identified estimate.",
         page="694-695, Table 4",
         extractor_note="Components: EFM 6.0% (0.14 births/woman), SB 3.8% (0.09), IUM total 9.4% (0.23). "
                        "B.5's CLEAN share is the stillbirth component; the EFM component is contaminated "
                        "by induced abortion on the authors' own Bongaarts estimate. Internal tension worth "
                        "noting: the life-table IUM quotient is 272/1000 pregnancies, but the reported fetal-death "
                        "rates imply only ~10% of pregnancies lost, which is the Casterline/Leridon under-reporting "
                        "problem visible inside a single paper."),
    # ---------------- Valente 2015, Nepal ----------------
    dict(openalex_id="W2009105027", doi="10.1016/j.jhealeco.2014.10.005",
         study="Valente", year=2015, venue="Journal of Health Economics 39:31-50",
         country="Nepal", period="Conceptions c.1996-2006 (Maoist insurgency); DHS 2001 and 2006",
         design="Maternal fixed effects; district x month conflict casualties as the shock",
         sample="11,887 pregnancies (596 miscarriages, 130 stillbirths, 10,846 live births)",
         cell_at_screen="PRIMARY_SHOCK_TO_BIRTHS", cell_at_fulltext="PARAMETER_DETERMINANT_TO_LOSS",
         estimand_level="not applicable (outcome is loss, not births per woman)",
         outcome="Probability a pregnancy ends in miscarriage; probability of stillbirth; sex at birth",
         effect="+0.77", effect_units="percentage points on the probability of miscarriage (11.6% of the mean), moving from mean exposure in low-intensity to high-intensity districts",
         ci_or_se="significant under maternal FE; within-district estimates positive but NOT significant",
         loss_definition="Self-reported pregnancy loss, DHS calendar; miscarriage and stillbirth coded separately",
         loss_window_weeks="Miscarriage: 90% occur in the first five months. Stillbirth reported separately.",
         induced_separation="YES. Losses where the mother reported intent, or gave no answer on intent, are set to missing in order to isolate biological loss.",
         replacement_treatment="Discussed as a threat, not modelled. The author notes women who lose a pregnancy may both try again sooner and under-report a further loss.",
         fertility_regime="High fertility, transitional",
         variation_source="District x month conflict casualties during gestation, within mother",
         confounders_adjusted="Maternal fixed effects; district controls; water, sanitation, housing; maternal education; caste/ethnicity",
         direction_established="Strong for shock->loss. Maternal FE absorb time-invariant maternal frailty, and the effect is concentrated in months 1-5 of gestation as the mechanism predicts.",
         selection_viability="ADDRESSED DIRECTLY. Exposed newborns are neither smaller nor more subject to neonatal mortality, so selection does not dominate scarring.",
         poolable_with="Other determinant-to-loss estimates on a shock exposure. NOT with the Morocco accounting estimate.",
         page="41-42, Tables 4 and 5",
         extractor_note="REROUTED at full text: outcomes are loss and sex ratio, not births per woman. Best-identified "
                        "loss-margin estimate in the corpus. Stillbirth moves the OTHER way (-0.22 ppt), which the "
                        "author reads as conflict-exposed fetuses being lost earlier rather than surviving to stillbirth "
                        "-- compositional movement across the live-birth boundary, i.e. Wall 1 mattering empirically."),
]

ROB = [
    dict(openalex_id="W4283072838", study="Mourchid & Bakass 2022", tool="ROBINS-I (adapted)",
         confounding="Critical", selection="Serious", exposure_measurement="Critical",
         missing_data="Serious", outcome_measurement="Serious", reporting="Moderate",
         overall="Critical",
         rationale="No identification strategy: an accounting identity applied to cross-sectional "
                   "self-reports. The exposure (intrauterine mortality) is measured from retrospective "
                   "pregnancy histories in a setting where induced abortion is illegal, so it is "
                   "contaminated by A.4's variable in the direction of overstating spontaneous loss, "
                   "and the paper's own life-table quotient (272/1000) is irreconcilable with its "
                   "reported fetal-death rates (~100/1000), which indicates substantial omission. "
                   "Rated Critical for the causal claim; still USABLE as an accounting benchmark, "
                   "which is what the chapter uses it for."),
    dict(openalex_id="W2009105027", study="Valente 2015", tool="ROBINS-I (adapted)",
         confounding="Low", selection="Moderate", exposure_measurement="Low",
         missing_data="Moderate", outcome_measurement="Serious", reporting="Low",
         overall="Moderate",
         rationale="Maternal fixed effects with a plausibly exogenous, finely time-varying shock, and "
                   "the effect is concentrated in the gestational window the mechanism predicts. Two "
                   "residual concerns. Outcome measurement: miscarriage is self-reported and the paper "
                   "documents that women who lose a pregnancy may under-report a subsequent loss, "
                   "which biases toward zero. Selection: within-district estimates are positive but "
                   "insignificant, so the result rests on the maternal-FE specification, and the "
                   "author's own explanation for that gap is differential fertility timing by "
                   "conflict intensity -- which is a selection process, not noise."),
]

RETRIEVAL = [
    dict(openalex_id="W4283072838", doi="10.25133/jpssv302022.038", status="RETRIEVED",
         source="user-supplied (Downloads/morocco.pdf)", verified="YES - title, authors, venue, DOI "
         "and volume/page all match the wantlist record on page 1",
         note="Identity checked against the PDF rather than the filename."),
    dict(openalex_id="W2009105027", doi="10.1016/j.jhealeco.2014.10.005", status="RETRIEVED",
         source="user-supplied (Downloads/trivers willard.pdf)",
         verified="YES - Valente, J Health Econ 39:31-50, matches",
         note="Journal volume year is 2015 (online 31 Oct 2014); the index record carries 2014. Same "
              "work, not a version discrepancy. CONFIRMED DUPLICATE of W1977150354 ('Children of the "
              "Revolution', RePEc 2011): same author (Christine Valente), same Nepal Maoist-insurgency "
              "data. Collapsed; the working paper is dropped and the JHE article is the version of record."),
]


def main():
    os.makedirs(EXTRACT, exist_ok=True)
    with open(os.path.join(EXTRACT, f"{SLUG}-effects.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=EFFECT_FIELDS)
        w.writeheader()
        for e in EFFECTS:
            w.writerow({k: e.get(k, "") for k in EFFECT_FIELDS})

    rob_fields = list(ROB[0].keys())
    with open(os.path.join(EXTRACT, f"{SLUG}-risk-of-bias.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rob_fields)
        w.writeheader()
        w.writerows(ROB)

    ret_fields = list(RETRIEVAL[0].keys())
    with open(os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ret_fields)
        w.writeheader()
        w.writerows(RETRIEVAL)

    on_disk = sorted(f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")) if os.path.isdir(PDF_DIR) else []

    L = [f"# Extraction report — {SLUG} (B.5)", "",
         f"**{len(on_disk)} PDFs on disk, {len(EFFECTS)} studies extracted.** Both identities were "
         "verified against page 1 of the file rather than against the filename.", "",
         "## The two findings that matter more than the numbers", "",
         "### 1. The one published estimate of this chapter's headline quantity is an accounting share", "",
         "Mourchid and Bakass estimate that intrauterine mortality reduces Moroccan potential fertility "
         "by **9.4%**, or 0.23 children per woman. That is the chapter's primary estimand, estimated "
         "directly, and it is the only study located that does so. But their potential-fertility measure "
         "is built by **adding fetal deaths to live births**: a lost conception is counted as a forgone "
         "birth, with no time cost and no replacement. It is an `ACCOUNTING_SHARE` by construction.", "",
         "This corroborates the chapter's argument rather than contradicting it. The model's accounting "
         "arm gives about 11% for removing a 10% loss rate outright, against their 9.4% — close enough "
         "to confirm the two are computing the same thing. What the chapter adds is that this number is "
         "an upper bound, and that the behavioural quantity is roughly two and a half times smaller.", "",
         "### 2. Wall 4 fires, and the authors supply the evidence themselves", "",
         "The 9.4% decomposes into 6.0 points from early fetal mortality and 3.8 from stillbirth. The "
         "authors define early fetal mortality as *abortions plus miscarriages*, and their own Bongaarts "
         "residual index attributes **0.12 births per woman to induced abortion against 0.14 for all "
         "early fetal mortality**. On their own numbers, then, most of the larger component is induced "
         "termination — A.4's estimand, not B.5's. **B.5's clean share of the Moroccan estimate is the "
         "stillbirth component, 3.8%.** This is exactly the contamination the scope document predicted "
         "for settings where abortion is legally restricted, and it means the headline 9.4% must not be "
         "quoted as a B.5 effect.", "",
         "A second internal tension is worth recording: the paper's life-table IUM quotient is 272 per "
         "1000 pregnancies, while its reported fetal-death rates imply roughly 100 per 1000. That gap is "
         "the Casterline and Leridon under-reporting problem appearing inside a single study.", "",
         "## Valente reroutes on retrieval", "",
         "Screened as `PRIMARY_SHOCK_TO_BIRTHS`, it becomes `PARAMETER_DETERMINANT_TO_LOSS` at full "
         "text: the outcomes are miscarriage, stillbirth and sex at birth, not births per woman. The "
         "screen could not have known — the abstract does not say — and this is the routing gate "
         "working as designed rather than a screening error.", "",
         "It is nonetheless the **best-identified loss-margin estimate in the corpus**: maternal fixed "
         "effects over 11,887 pregnancies, with district-by-month conflict casualties as the shock, and "
         "the effect concentrated in gestational months one to five as the mechanism predicts. Moving "
         "from low- to high-intensity conflict exposure raises the probability of miscarriage by 0.77 "
         "percentage points, 11.6% of the mean.", "",
         "Three details bear directly on the chapter's identification section:", "",
         "- **Stillbirth moves the other way** (−0.22 ppt). The author reads this as conflict-exposed "
         "fetuses being lost earlier rather than surviving to stillbirth. That is compositional movement "
         "across the live-birth boundary, and it is Wall 1 mattering empirically rather than definitionally.",
         "- **The replacement and reporting threats appear together in the author's own words**: women "
         "who lose a pregnancy may both try again sooner and under-report a further loss. The chapter "
         "flagged both a priori; here they are documented in the setting.",
         "- **The result rests on the maternal-FE specification.** Within-district estimates are positive "
         "but insignificant, and the author's explanation for the gap is differential fertility timing by "
         "conflict intensity — a selection process, not noise. Recorded as a fragility.", "",
         "## Risk of bias", "", "| study | overall | the binding domain |", "|---|---|---|",
         "| Mourchid & Bakass 2022 | **Critical** | Exposure measurement: contaminated by induced "
         "abortion, and the paper's own two loss measures disagree by a factor of nearly three. Usable "
         "as an accounting benchmark, not as causal evidence. |",
         "| Valente 2015 | **Moderate** | Outcome measurement: self-reported miscarriage with documented "
         "differential under-reporting, biasing toward zero. |", "",
         "## Still open", "",
         f"{len(on_disk)} of 51 wantlist items retrieved. The extraction table has {len(EFFECTS)} rows "
         "and no pooling is possible or attempted: one estimate is an accounting share and the other is "
         "a determinant-to-loss effect, so they share neither an estimand nor an outcome.", "",
         "## A duplicate class the pipeline cannot currently catch", "",
         "W1977150354 ('Children of the Revolution: Fetal and Child Health amidst Violent Civil "
         "Conflict', RePEc 2011) is **confirmed** to be Valente's working paper on the same Nepal "
         "insurgency data — same author, same shock, same survey rounds. It collapses into W2009105027, "
         "and the primary-cell count falls from 18 to 17.", "",
         "**The general point is worth carrying to every chapter.** This duplicate is invisible to both "
         "dedup rules in use. DOI dedup misses it because the two records have different DOIs. Title "
         "dedup misses it because the working paper was RETITLED before publication: 'Children of the "
         "Revolution' and 'Civil conflict, gender-specific fetal loss, and selection' share almost no "
         "tokens. The version-of-record gate handles same-title-different-version; this is the mirror "
         "case, different-title-same-work, and only author-plus-data inspection catches it. A cheap "
         "partial guard: flag same-first-author records whose abstracts name the same country and shock "
         "for human review."]
    open(os.path.join(LOGS, f"{SLUG}-extraction-report.md"), "w").write("\n".join(L) + "\n")

    print(f"PDFs on disk: {len(on_disk)}")
    print(f"effects rows: {len(EFFECTS)}  rob rows: {len(ROB)}  retrieval rows: {len(RETRIEVAL)}")
    for e in EFFECTS:
        print(f"  {e['study']} {e['year']}: {e['cell_at_screen']} -> {e['cell_at_fulltext']} "
              f"[{e['estimand_level']}]")


if __name__ == "__main__":
    main()
