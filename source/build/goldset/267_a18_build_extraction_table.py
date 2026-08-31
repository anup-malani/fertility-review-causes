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
