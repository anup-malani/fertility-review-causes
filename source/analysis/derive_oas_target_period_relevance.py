#!/usr/bin/env python3
"""Derive OAS target-period relevance from verified study windows.

This pilot script uses the RA-verified country/region and study-window fields
from the OAS study extraction table. It writes a derivation audit table and
updates period_target_relevance in the source extraction table.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDIES = ROOT / "extraction/old-age-security-pension-crowdout-studies.csv"
OUT = ROOT / "extraction/old-age-security-pension-crowdout-target-period-relevance.csv"


# Pilot-specific fertility context. These labels are intentionally conservative:
# the fertility-level rule is mechanical where possible, and ambiguity is explicit.
DERIVATIONS = {
    "danzer_zyska_2023_brazil_pensions": {
        "label": "FDT|SDT",
        "basis": "Brazil sample window spans high/transition fertility in the 1980s and near/below-replacement fertility by the 2010s.",
        "needs_human_review": "no",
    },
    "rossi_godard_2022_namibia_pensions": {
        "label": "FDT",
        "basis": "Namibia remains above replacement during the verified 1990-2012 study window; this is a late first-transition setting.",
        "needs_human_review": "no",
    },
    "billari_galasso_2009_italy_pension_reforms": {
        "label": "SDT",
        "basis": "Italy is already a low-fertility, below-replacement setting during the verified 1998-2004 analysis window.",
        "needs_human_review": "no",
    },
    "han_tao_wang_zhang_2025_china_ltci": {
        "label": "SDT",
        "basis": "China is below replacement during 2012-2020, but the one-child/two-child-policy environment means SDT interpretation should be treated cautiously.",
        "needs_human_review": "yes",
    },
    "guinnane_streb_2021_prussia_social_security": {
        "label": "FDT",
        "basis": "Prussia 1881-1910 falls in the classic first demographic transition window.",
        "needs_human_review": "no",
    },
    "shen_zheng_yang_2020_china_nrps": {
        "label": "SDT",
        "basis": "China is below replacement during 2010-2014, but fertility is policy-constrained; SDT interpretation should be treated cautiously.",
        "needs_human_review": "yes",
    },
    "ci_2024_children_insurance": {
        "label": "SDT",
        "basis": "China is below replacement during 2010-2018; this row is mechanism evidence with a non-fertility outcome, so target-period relevance is contextual.",
        "needs_human_review": "yes",
    },
    "fenge_scheubel_2017_germany_pensions": {
        "label": "FDT",
        "basis": "Imperial Germany 1895-1907 is a first-demographic-transition setting.",
        "needs_human_review": "no",
    },
    "basso_bodenhorn_cuberes_2014_us_financial_development": {
        "label": "PM|FDT",
        "basis": "United States 1850 is pre-1870 and directly adjacent to the nineteenth-century fertility transition.",
        "needs_human_review": "no",
    },
    "galofre_vila_2023_us_baby_boom": {
        "label": "FDT",
        "basis": "United States 1940-1960 is before the project SDT boundary and sits within the late first-transition/baby-boom period.",
        "needs_human_review": "no",
    },
}


def main() -> None:
    with STUDIES.open(newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if "period_target_relevance" not in fieldnames:
        fieldnames.append("period_target_relevance")

    audit_fields = [
        "study_id",
        "country_or_region",
        "period_start",
        "period_end",
        "primary_outcome_family",
        "derived_period_target_relevance",
        "needs_human_review",
        "derivation_basis",
    ]
    audit_rows = []

    for row in rows:
        study_id = row["study_id"]
        derivation = DERIVATIONS.get(study_id)
        if derivation is None:
            row["period_target_relevance"] = "UNCLASSIFIED"
            label = "UNCLASSIFIED"
            needs_review = "yes"
            basis = "No pilot derivation rule found for this study_id."
        else:
            label = derivation["label"]
            needs_review = derivation["needs_human_review"]
            basis = derivation["basis"]
            row["period_target_relevance"] = label

        audit_rows.append(
            {
                "study_id": study_id,
                "country_or_region": row.get("country_or_region", ""),
                "period_start": row.get("period_start", ""),
                "period_end": row.get("period_end", ""),
                "primary_outcome_family": row.get("primary_outcome_family", ""),
                "derived_period_target_relevance": label,
                "needs_human_review": needs_review,
                "derivation_basis": basis,
            }
        )

    with STUDIES.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fieldnames} for row in rows)

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=audit_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(audit_rows)


if __name__ == "__main__":
    main()
