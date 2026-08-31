#!/usr/bin/env python3
"""272 — A.18 risk of bias. TICK-076.

ROBINS-I is written for interventions and does not fit a variance decomposition:
"confounding" and "deviation from intended intervention" have no referent when the
estimand is a variance component. So the instrument is built from the chapter's own
§10 identification threats, which is what ROBINS-I's domains would have to be
translated into anyway. Each domain is rated LOW / MODERATE / SERIOUS / CRITICAL
with the reason recorded.

Domains (scope memo §10):
  D1 gene-environment correlation — does the estimand absorb education, health and
     partnering upstream of fertility? Unavoidable for anonymous-variance designs;
     the rating turns on whether the study acknowledges and bounds it.
  D2 population stratification / dynastic effects — POPULATION-level molecular
     estimates are inflated by ancestry structure and genetic nurture;
     WITHIN_FAMILY designs are not.
  D3 equal-environments assumption — classical twin designs only.
  D4 sample selection — volunteer biobanks and survivor cohorts select on traits
     correlated with fertility.
  D5 censoring — an estimate on incomplete cohorts is biased toward early reproducers.
  D6 reverse causation on h2 itself — h2 is an OUTCOME of the regime (§4), so any
     cross-cohort comparison is descriptive.
  D7 replication asymmetry — candidate-gene-era estimates.

Ratings are assigned from the extraction table's recorded tags, not re-read from
the papers, so they are reproducible from the table and change when it changes.

Usage: python3 source/build/goldset/272_a18_risk_of_bias.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSVP = ROOT / "extraction" / "heritability-fertility-genetic.csv"
OUT = ROOT / "extraction" / "heritability-fertility-genetic-risk-of-bias.csv"
OUT_MD = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-risk-of-bias.md"

USABLE = ("VERIFIED", "VERIFIED_AUTHORS_PREFERRED", "VERIFIED_NULL",
          "VERIFIED_CELL_RECLASSIFIED_FROM_H2_FERTILITY",
          "VERIFIED_SPECIFICATION_DISCORDANT", "VERIFIED_NON_H2_ESTIMAND")
ORDER = {"LOW": 0, "MODERATE": 1, "SERIOUS": 2, "CRITICAL": 3}


def rate(r):
    d, why = {}, {}
    dc = (r["design_class"] or "").lower()
    rel = r["relatedness_level"] or ""
    dist = r["exposure_distance"] or ""
    sel = (r["sample_selection"] or "").lower()

    # D1 gene-environment correlation
    if dist == "ANONYMOUS_VARIANCE":
        d["D1_gene_environment_correlation"] = "SERIOUS"
        why["D1_gene_environment_correlation"] = (
            "anonymous variance component: absorbs the heritability of education, health and "
            "partnering upstream of fertility; the estimand is genotype's total association, "
            "not a genetic effect holding the life course fixed")
    else:
        d["D1_gene_environment_correlation"] = "MODERATE"
        why["D1_gene_environment_correlation"] = "named genetic measure; rGE still present but bounded"

    # D2 stratification / dynastic effects
    if rel == "WITHIN_FAMILY":
        d["D2_stratification_dynastic"] = "LOW"
        why["D2_stratification_dynastic"] = "within-family contrast removes ancestry structure and genetic nurture"
    elif rel == "POPULATION":
        d["D2_stratification_dynastic"] = "SERIOUS"
        why["D2_stratification_dynastic"] = (
            "population-level estimate: inflated by ancestry structure, assortative mating and "
            "genetic nurture; the within-family comparison in this chapter is 0.27 against "
            "population SNP estimates of 0.03-0.10")
    else:
        d["D2_stratification_dynastic"] = "MODERATE"
        why["D2_stratification_dynastic"] = "relatedness level not recorded"

    # D3 equal environments
    if "twin" in dc:
        d["D3_equal_environments"] = "SERIOUS"
        why["D3_equal_environments"] = "classical twin design; EEA untestable and load-bearing"
    else:
        d["D3_equal_environments"] = "LOW"
        why["D3_equal_environments"] = "not a classical twin design"

    # D4 sample selection
    if "volunteer" in sel:
        d["D4_sample_selection"] = "SERIOUS"
        why["D4_sample_selection"] = "volunteer biobank: healthy-volunteer selection correlates with fertility"
    elif "genealog" in sel or "parish" in sel or "register" in sel:
        d["D4_sample_selection"] = "LOW"
        why["D4_sample_selection"] = "population register or complete genealogy"
    else:
        d["D4_sample_selection"] = "MODERATE"
        why["D4_sample_selection"] = "cohort or registry sample; selection plausible but not extreme"

    # D5 censoring
    cc = (r["cohort_complete"] or "").lower()
    d["D5_censoring"] = {"yes": "LOW", "unclear": "SERIOUS"}.get(cc, "MODERATE")
    why["D5_censoring"] = ("reproduction complete" if cc == "yes" else
                           "completeness not established: an estimate on incomplete cohorts is "
                           "biased toward early reproducers")

    # D6 reverse causation on h2
    if r["cell"] == "H2_MODERATION":
        d["D6_reverse_causation_on_h2"] = "SERIOUS"
        why["D6_reverse_causation_on_h2"] = (
            "cross-cohort comparison of h2 is descriptive: §4 argues h2 is an OUTCOME of the "
            "regime, so the arrow runs from the transition to the heritability")
    else:
        d["D6_reverse_causation_on_h2"] = "LOW"
        why["D6_reverse_causation_on_h2"] = "not a cross-regime comparison"

    # D7 replication asymmetry
    yr = int(r["year"] or 0)
    if yr and yr < 2012 and "GREML" not in (r["design_class"] or ""):
        d["D7_replication_asymmetry"] = "MODERATE"
        why["D7_replication_asymmetry"] = "pre-2012; candidate-gene-era publication asymmetry plausible"
    else:
        d["D7_replication_asymmetry"] = "LOW"
        why["D7_replication_asymmetry"] = "post-2012 or genome-wide method"

    overall = max(d.values(), key=lambda v: ORDER[v])
    return d, why, overall


def main():
    rows = [r for r in csv.DictReader(CSVP.open()) if r["extraction_status"] in USABLE]
    doms = ["D1_gene_environment_correlation", "D2_stratification_dynastic",
            "D3_equal_environments", "D4_sample_selection", "D5_censoring",
            "D6_reverse_causation_on_h2", "D7_replication_asymmetry"]
    out, overalls = [], Counter()
    for r in rows:
        d, why, ov = rate(r)
        overalls[ov] += 1
        out.append({"openalex": r["openalex"], "study": r["study"][:70], "cell": r["cell"],
                    "estimand": r["estimand"], **d, "overall": ov,
                    "worst_domain_reason": why[max(d, key=lambda k: ORDER[d[k]])]})
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    md = ["# A.18 risk of bias\n",
          f"{len(out)} usable estimates rated on the chapter's own §10 threat domains. "
          "ROBINS-I's intervention domains have no referent for a variance component, so the "
          "instrument is built from the identification threats instead.\n",
          "\n## Overall\n\n| rating | estimates |\n|---|---|"]
    for k in ("LOW", "MODERATE", "SERIOUS", "CRITICAL"):
        if overalls[k]:
            md.append(f"| {k} | {overalls[k]} |")
    md.append("\n## By domain\n\n| domain | LOW | MODERATE | SERIOUS |\n|---|---|---|---|")
    for dm in doms:
        c = Counter(o[dm] for o in out)
        md.append(f"| `{dm}` | {c['LOW']} | {c['MODERATE']} | {c['SERIOUS']} |")
    md.append("\n**No estimate in this chapter is at low overall risk of bias.** The binding domain "
              "is D1: for the two-thirds of the evidence that is an anonymous variance component, "
              "gene-environment correlation is not a flaw in the studies but a property of the "
              "quantity, and it cannot be designed away.\n")
    OUT_MD.write_text("\n".join(md) + "\n")
    print("overall:", dict(overalls))
    for dm in doms:
        print(f"   {dm:34s} {dict(Counter(o[dm] for o in out))}")


if __name__ == "__main__":
    main()
