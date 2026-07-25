#!/usr/bin/env python3
"""Materialize the verified Shanan primary-study supplement for TICK-031.

The study was an original cold-start anchor but was not part of Alexandra's 16-paper
RA-approved child-value set. Springer exposes the abstract and individual result tables
even when the article PDF/body is subscription-gated.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "extraction" / "compulsory-education-shanan-primary-study.csv"

FIELDS = [
    "paperId", "doi", "study", "evidence_component", "estimand", "estimate",
    "standard_error", "baseline", "observations", "source_locator", "interpretation",
    "verification_status",
]

COMMON = {
    "paperId": "W3174215957",
    "doi": "10.1007/s00148-021-00838-1",
    "study": "Shanan (2023), The effect of compulsory schooling laws and child labor restrictions on fertility",
    "verification_status": "VERIFIED_PUBLISHER_TABLE_PAGE_2026-07-25",
}

ROWS = [
    {**COMMON, "evidence_component": "fertility_reduced_form", "estimand": "Exposure at ages 20-30 to any child-labor restriction; annual birth probability", "estimate": "-0.0085", "standard_error": "0.0011", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/7, column 2", "interpretation": "Preferred controlled specification; 0.85 percentage-point lower annual birth probability."},
    {**COMMON, "evidence_component": "fertility_reduced_form", "estimand": "One-year increase in average school exit age at ages 20-30; annual birth probability", "estimate": "-0.0027", "standard_error": "0.0003", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/8, column 2", "interpretation": "Preferred controlled intensity specification; 0.27 percentage-point lower annual birth probability per exit-age year."},
    {**COMMON, "evidence_component": "fertility_joint_policy", "estimand": "Any restriction, conditional on average school exit age; annual birth probability", "estimate": "-0.0050", "standard_error": "0.0013", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/12, column 2", "interpretation": "Extensive-margin restriction effect remains negative when policy intensity is entered jointly."},
    {**COMMON, "evidence_component": "fertility_joint_policy", "estimand": "School exit age, conditional on any restriction; annual birth probability", "estimate": "-0.0018", "standard_error": "0.0004", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/12, column 2", "interpretation": "Policy-intensity effect remains negative when the extensive policy indicator is entered jointly."},
    {**COMMON, "evidence_component": "child_employment_first_stage", "estimand": "Child-labor restriction effect on child employment; literate-mother subgroup", "estimate": "-0.029", "standard_error": "0.008", "baseline": "0.092", "observations": "1115971", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/13, column 1", "interpretation": "Restrictions reduce observed child employment; subgroup estimates are generally negative, with heterogeneous precision."},
    {**COMMON, "evidence_component": "school_attendance_first_stage", "estimand": "Child-labor restriction effect on school attendance; literate-mother subgroup", "estimate": "0.036", "standard_error": "0.008", "baseline": "0.912", "observations": "1115971", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/14, column 1", "interpretation": "Restrictions increase observed school attendance; subgroup estimates are consistently positive."},
]


def main() -> None:
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)
    print(f"wrote {len(ROWS)} Shanan primary-study evidence rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
