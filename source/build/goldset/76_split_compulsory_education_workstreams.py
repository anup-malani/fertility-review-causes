#!/usr/bin/env python3
"""Split the combined compulsory-education retrieval handoff into two workstreams.

This is a routing step, not full-text extraction. It creates separate retrieval manifests and
pre-populated study-level extraction templates for:

1. compulsory education -> lower child economic value -> completed fertility; and
2. compulsory education -> continued enrollment -> fewer teenage births.

Studies may appear in both workstreams when the existing record explicitly reports both a quantum
and a teenage-birth outcome. Blank extraction fields must be completed from full text.
"""

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = REPO / "output/child-labor-laws-and-schooling-metaanalysis-doi-retrieval.csv"

A_SLUG = "compulsory-education-child-economic-value"
B_SLUG = "compulsory-education-teenage-births"

# The combined handoff assigns Geruso-Royer to quantum because it reports completed fertility,
# but its abstract also explicitly reports teen fertility. Full text must therefore be screened
# for both hypotheses. Add future dual-outcome records here only with an auditable reason.
DUAL_ROUTE = {
    "W2185731654": "Abstract explicitly reports teen fertility and completed fertility.",
}

IDENTITY_FIELDS = [
    "study_id", "source_retrieval_id", "paper_id", "doi", "title", "authors", "year", "venue",
    "pdf_path", "fulltext_status", "fulltext_decision", "fulltext_decision_ra_decision",
    "fulltext_decision_source",
]

A_FIELDS = IDENTITY_FIELDS + [
    "reform_or_law", "reform_or_law_ra_decision", "reform_or_law_source",
    "setting", "setting_ra_decision", "setting_source",
    "study_period", "study_period_ra_decision", "study_period_source",
    "design", "design_ra_decision", "design_source",
    "whose_schooling_changed", "whose_schooling_changed_ra_decision", "whose_schooling_changed_source",
    "schooling_first_stage", "schooling_first_stage_ra_decision", "schooling_first_stage_source",
    "child_work_first_stage", "child_work_first_stage_ra_decision", "child_work_first_stage_source",
    "quantum_outcome", "quantum_outcome_ra_decision", "quantum_outcome_source",
    "effect_estimate", "effect_estimate_ra_decision", "effect_estimate_source",
    "standard_error", "standard_error_ra_decision", "standard_error_source",
    "effect_unit", "effect_unit_ra_decision", "effect_unit_source",
    "mechanism_classification", "mechanism_classification_ra_decision", "mechanism_classification_source",
    "mechanism_directness", "mechanism_directness_ra_decision", "mechanism_directness_source",
    "fdt_relevance", "fdt_relevance_ra_decision", "fdt_relevance_source",
    "notes",
]

B_FIELDS = IDENTITY_FIELDS + [
    "reform_or_law", "reform_or_law_ra_decision", "reform_or_law_source",
    "setting", "setting_ra_decision", "setting_source",
    "study_period", "study_period_ra_decision", "study_period_source",
    "design", "design_ra_decision", "design_source",
    "school_enrollment_first_stage", "school_enrollment_first_stage_ra_decision", "school_enrollment_first_stage_source",
    "tempo_outcome_type", "tempo_outcome_type_ra_decision", "tempo_outcome_type_source",
    "age_threshold", "age_threshold_ra_decision", "age_threshold_source",
    "effect_estimate", "effect_estimate_ra_decision", "effect_estimate_source",
    "standard_error", "standard_error_ra_decision", "standard_error_source",
    "effect_unit", "effect_unit_ra_decision", "effect_unit_source",
    "pregnancy_or_live_birth", "pregnancy_or_live_birth_ra_decision", "pregnancy_or_live_birth_source",
    "mediator", "mediator_ra_decision", "mediator_source",
    "effect_duration", "effect_duration_ra_decision", "effect_duration_source",
    "later_birth_rebound", "later_birth_rebound_ra_decision", "later_birth_rebound_source",
    "completed_fertility_followup", "completed_fertility_followup_ra_decision", "completed_fertility_followup_source",
    "transition_relevance", "transition_relevance_ra_decision", "transition_relevance_source",
    "notes",
]

MANIFEST_FIELDS = [
    "hypothesis_slug", "study_id", "source_retrieval_id", "paper_id", "doi", "doi_url", "title",
    "authors", "year", "venue", "source_outcome_family", "source_estimand_cell", "route_basis",
    "also_routed_to_other_hypothesis", "pdf_status",
]


def read_rows():
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def manifest_row(row, slug, index, basis, shared):
    prefix = "CEV" if slug == A_SLUG else "CETB"
    return {
        "hypothesis_slug": slug,
        "study_id": f"{prefix}-{index:03d}",
        "source_retrieval_id": row["retrieval_id"],
        "paper_id": row["paperId"],
        "doi": row["doi"],
        "doi_url": row["doi_url"],
        "title": row["title"],
        "authors": row["authors"],
        "year": row["year"],
        "venue": row["venue"],
        "source_outcome_family": row["outcome_family"],
        "source_estimand_cell": row["estimand_cell"],
        "route_basis": basis,
        "also_routed_to_other_hypothesis": "YES" if shared else "NO",
        "pdf_status": "NOT_RETRIEVED",
    }


def extraction_row(manifest):
    return {
        "study_id": manifest["study_id"],
        "source_retrieval_id": manifest["source_retrieval_id"],
        "paper_id": manifest["paper_id"],
        "doi": manifest["doi"],
        "title": manifest["title"],
        "authors": manifest["authors"],
        "year": manifest["year"],
        "venue": manifest["venue"],
        "pdf_path": "",
        "fulltext_status": "not_started",
        "fulltext_decision": "",
        "fulltext_decision_ra_decision": "",
        "fulltext_decision_source": "",
    }


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_rows()
    if len(rows) != 15:
        raise SystemExit(f"Expected 15 focused retrieval studies; found {len(rows)}")

    a_source = [row for row in rows if row["outcome_family"] == "FERTILITY_QUANTUM"]
    b_source = [row for row in rows if row["outcome_family"] == "FERTILITY_TEMPO"]
    by_id = {row["paperId"]: row for row in rows}
    missing_dual = sorted(set(DUAL_ROUTE) - set(by_id))
    if missing_dual:
        raise SystemExit(f"Dual-route records missing from source: {missing_dual}")
    b_source.extend(by_id[paper_id] for paper_id in DUAL_ROUTE if by_id[paper_id] not in b_source)

    a_manifest = []
    for index, row in enumerate(a_source, 1):
        shared = row["paperId"] in DUAL_ROUTE
        a_manifest.append(manifest_row(
            row, A_SLUG, index,
            "Quantum record; candidate reduced-form evidence pending full-text mechanism coding.",
            shared,
        ))

    b_manifest = []
    for index, row in enumerate(b_source, 1):
        shared = row["paperId"] in DUAL_ROUTE
        basis = DUAL_ROUTE.get(row["paperId"], "Tempo record in the RA-approved focused handoff.")
        b_manifest.append(manifest_row(row, B_SLUG, index, basis, shared))

    if len(a_manifest) != 6 or len(b_manifest) != 10:
        raise SystemExit(f"Unexpected routing counts: A={len(a_manifest)}, B={len(b_manifest)}")

    write_csv(REPO / f"output/{A_SLUG}-retrieval.csv", MANIFEST_FIELDS, a_manifest)
    write_csv(REPO / f"output/{B_SLUG}-retrieval.csv", MANIFEST_FIELDS, b_manifest)
    write_csv(REPO / f"extraction/{A_SLUG}-study-extraction.csv", A_FIELDS,
              [extraction_row(row) for row in a_manifest])
    write_csv(REPO / f"extraction/{B_SLUG}-study-extraction.csv", B_FIELDS,
              [extraction_row(row) for row in b_manifest])

    print(f"{A_SLUG}: {len(a_manifest)} candidate studies")
    print(f"{B_SLUG}: {len(b_manifest)} candidate studies")
    print(f"dual-routed: {sum(row['also_routed_to_other_hypothesis'] == 'YES' for row in a_manifest)}")


if __name__ == "__main__":
    main()
