#!/usr/bin/env python3
"""Materialize the verified Shanan primary-study supplement for TICK-031.

The study was an original cold-start anchor but was not part of Alexandra's 16-paper
RA-approved child-value set. Springer exposes the abstract and individual result tables
even when the article PDF/body is subscription-gated.
"""

from __future__ import annotations

import csv
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "extraction" / "compulsory-education-shanan-primary-study.csv"
PDF = "literature/pdfs/compulsory-education/W3174215957__shanan-compulsory-schooling-child-labor-fertility.pdf"
TEXT_OUT = ROOT / "temp" / "compulsory-education-fulltext" / "W3174215957.txt"

FIELDS = [
    "paperId", "doi", "study", "evidence_component", "estimand", "estimate",
    "standard_error", "baseline", "observations", "source_locator", "interpretation",
    "pdf_path", "verification_status",
]

COMMON = {
    "paperId": "W3174215957",
    "doi": "10.1007/s00148-021-00838-1",
    "study": "Shanan (2023), The effect of compulsory schooling laws and child labor restrictions on fertility",
    "pdf_path": PDF,
    "verification_status": "VERIFIED_PUBLISHED_PDF_2026-07-25",
}

ROWS = [
    {**COMMON, "evidence_component": "completed_fertility", "estimand": "Exposure at ages 20-30 to any child-labor restriction; completed fertility", "estimate": "-0.301", "standard_error": "0.044", "baseline": "3.112", "observations": "335861", "source_locator": "Published PDF p. 338, Table 4, column 2", "interpretation": "Controlled cohort specification; about 0.30 fewer children, or 10% of the sample mean."},
    {**COMMON, "evidence_component": "completed_fertility", "estimand": "One-year increase in average school exit age at ages 20-30; completed fertility", "estimate": "-0.108", "standard_error": "0.024", "baseline": "3.112", "observations": "335861", "source_locator": "Published PDF p. 339, Table 5, column 2", "interpretation": "Controlled cohort specification; about 3.5% lower completed fertility per exit-age year."},
    {**COMMON, "evidence_component": "fertility_reduced_form", "estimand": "Exposure at ages 20-30 to any child-labor restriction; annual birth probability", "estimate": "-0.0085", "standard_error": "0.0011", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/7, column 2", "interpretation": "Preferred controlled specification; 0.85 percentage-point lower annual birth probability."},
    {**COMMON, "evidence_component": "fertility_reduced_form", "estimand": "One-year increase in average school exit age at ages 20-30; annual birth probability", "estimate": "-0.0027", "standard_error": "0.0003", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/8, column 2", "interpretation": "Preferred controlled intensity specification; 0.27 percentage-point lower annual birth probability per exit-age year."},
    {**COMMON, "evidence_component": "fertility_joint_policy", "estimand": "Any restriction, conditional on average school exit age; annual birth probability", "estimate": "-0.0050", "standard_error": "0.0013", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/12, column 2", "interpretation": "Extensive-margin restriction effect remains negative when policy intensity is entered jointly."},
    {**COMMON, "evidence_component": "fertility_joint_policy", "estimand": "School exit age, conditional on any restriction; annual birth probability", "estimate": "-0.0018", "standard_error": "0.0004", "baseline": "0.143", "observations": "7241042", "source_locator": "https://link.springer.com/article/10.1007/s00148-021-00838-1/tables/12, column 2", "interpretation": "Policy-intensity effect remains negative when the extensive policy indicator is entered jointly."},
    {**COMMON, "evidence_component": "child_employment_first_stage", "estimand": "Restriction eligibility effect on probability a child is employed", "estimate": "-0.029", "standard_error": "0.008", "baseline": "0.118", "observations": "1369026", "source_locator": "Published PDF p. 337, Table 2, column 2", "interpretation": "Restrictions reduce observed child employment by about 25% of baseline."},
    {**COMMON, "evidence_component": "school_attendance_first_stage", "estimand": "Restriction eligibility effect on probability a child attends school", "estimate": "0.042", "standard_error": "0.008", "baseline": "0.882", "observations": "1369026", "source_locator": "Published PDF p. 337, Table 2, column 4", "interpretation": "Restrictions increase observed school attendance by about 5% of baseline."},
    {**COMMON, "evidence_component": "historical_decomposition", "estimand": "Share of 1900-1930 decline in annual birth probability at age 30 attributable to expanded restriction exposure", "estimate": "0.08", "standard_error": "NOT_REPORTED", "baseline": "Birth probability fell 0.18 to 0.13; exposure rose 0.52 to 1.00", "observations": "NOT_APPLICABLE", "source_locator": "Published PDF p. 341, Section 7", "interpretation": "Author's back-of-envelope calculation: 0.48 * 0.85 / 5 = 8%, below the protocol's 10% threshold."},
]


def main() -> None:
    pdf_path = ROOT / PDF
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    reader = PdfReader(str(pdf_path))
    if len(reader.pages) != 38:
        raise ValueError(f"expected 38 PDF pages, found {len(reader.pages)}")
    text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
    if "eight percent (0.48 * 0.85/5)" not in text:
        raise ValueError("could not verify Shanan's explicit eight-percent calculation")
    TEXT_OUT.parent.mkdir(parents=True, exist_ok=True)
    TEXT_OUT.write_text(text, encoding="utf-8")
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)
    print(f"wrote {len(ROWS)} Shanan primary-study evidence rows to {OUT.relative_to(ROOT)}")
    print(f"wrote {len(text)} extracted characters to {TEXT_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
