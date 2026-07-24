#!/usr/bin/env python3
"""Build a judgment-blinded second-review sheet for the schooling hypotheses."""

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVIDENCE = REPO / "extraction/compulsory-education-accessible-fulltext-evidence.csv"
OUTPUT = REPO / "output/compulsory-education-second-review-sheet.csv"

SOURCE_FIELDS = [
    "paperId", "title", "workstream", "fulltext_decision", "design", "setting", "reform",
    "schooling_first_stage", "fertility_outcome", "effect_summary", "persistence_or_rebound",
    "completed_fertility", "mechanism", "source_locator", "pdf_path",
]
REVIEW_FIELDS = [
    "reviewer_name", "review_date", "include_decision", "mechanism_classification",
    "confounding", "selection_or_sorting", "treatment_classification", "outcome_measurement",
    "missing_data", "selective_reporting", "overall_risk_of_bias", "rob_rationale",
    "directness_for_assigned_hypothesis", "precision", "consistency_with_stream",
    "publication_bias_concern", "grade_suggested", "grade_rationale",
    "demographic_significance", "demographic_rationale", "needs_pi_decision", "reviewer_notes",
]


def main():
    with EVIDENCE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    empirical = [row for row in rows if not row["completed_fertility"].startswith("MODEL")
                 and "THEORY" not in row["synthesis_status"]]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_FIELDS + REVIEW_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in empirical:
            writer.writerow({field: row.get(field, "") for field in SOURCE_FIELDS + REVIEW_FIELDS})
    print(f"wrote {len(empirical)} judgment-blinded empirical review rows")


if __name__ == "__main__":
    main()
