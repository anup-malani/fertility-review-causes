#!/usr/bin/env python3
"""Utilities for OAS effect extraction, review, and conservative synthesis."""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


SLUG = "old-age-security-pension-crowdout"
ROOT = Path(__file__).resolve().parents[2]

EFFECT_REQUIRED_COLUMNS = [
    "effect_id",
    "study_id",
    "pdf_path",
    "pdf_filename",
    "mechanism_cell",
    "estimand_label",
    "is_primary_estimate",
    "outcome_name",
    "outcome_family",
    "outcome_unit_original",
    "effect_original",
    "se_original",
    "ci_lower_original",
    "ci_upper_original",
    "p_value",
    "n_observations",
    "n_clusters",
    "model_specification",
    "comparison_group",
    "treatment_scale_original",
    "followup_window",
    "subgroup",
    "extract_page",
    "extract_quote_or_note",
    "extracted_by",
    "ra_verified",
    "needs_pi",
]

REVIEW_FIELDS = [
    "mechanism_cell",
    "estimand_label",
    "is_primary_estimate",
    "outcome_name",
    "outcome_family",
    "outcome_unit_original",
    "effect_original",
    "se_original",
    "ci_lower_original",
    "ci_upper_original",
    "p_value",
    "model_specification",
    "treatment_scale_original",
    "followup_window",
    "subgroup",
    "extract_page",
    "extract_quote_or_note",
    "needs_pi",
]

HARMONIZED_COLUMNS = EFFECT_REQUIRED_COLUMNS + [
    "harmonized_outcome_unit",
    "effect_harmonized",
    "se_harmonized",
    "harmonization_method",
    "meta_analysis_group",
    "poolability_reason",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def validate_required_columns(path: Path, required: list[str]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    missing = [column for column in required if column not in fieldnames]
    if missing:
        raise ValueError(f"Missing required columns in {path}: {', '.join(missing)}")


def make_effect_review_columns() -> list[str]:
    context = ["effect_id", "study_id", "pdf_filename"]
    columns: list[str] = context[:]
    for field in REVIEW_FIELDS:
        columns.extend([field, f"{field}_ra_decision", f"{field}_ra_notes"])
    return columns


def _decimal(value: str) -> Decimal | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def _format_decimal(value: Decimal | None) -> str:
    if value is None:
        return ""
    normalized = value.normalize()
    return format(normalized, "f")


COMPATIBILITY_REQUIRED_REASON = (
    "requires_treatment_scale_followup_and_sign_orientation_before_pooling"
)


def harmonize_effect_row(row: dict[str, str]) -> dict[str, str]:
    out = dict(row)
    effect = _decimal(row.get("effect_original", ""))
    se = _decimal(row.get("se_original", ""))
    family = row.get("outcome_family", "")
    unit = row.get("outcome_unit_original", "")
    cell = row.get("mechanism_cell", "")

    out.update(
        {
            "harmonized_outcome_unit": "",
            "effect_harmonized": "",
            "se_harmonized": "",
            "harmonization_method": "",
            "meta_analysis_group": "not_poolable",
            "poolability_reason": "",
        }
    )

    if effect is None:
        out["poolability_reason"] = "missing_or_non_numeric_effect"
        return out

    if family == "birth_probability" and unit == "percentage_points":
        out["harmonized_outcome_unit"] = "probability_of_birth"
        out["effect_harmonized"] = _format_decimal(effect / Decimal("100"))
        out["se_harmonized"] = _format_decimal(se / Decimal("100")) if se is not None else ""
        out["harmonization_method"] = "percentage_points_divided_by_100"
        if cell == "A":
            out["poolability_reason"] = COMPATIBILITY_REQUIRED_REASON
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        return out

    if family == "completed_fertility" and unit == "births_per_woman":
        out["harmonized_outcome_unit"] = "births_per_woman"
        out["effect_harmonized"] = _format_decimal(effect)
        out["se_harmonized"] = _format_decimal(se)
        out["harmonization_method"] = "already_births_per_woman"
        if cell == "A":
            out["poolability_reason"] = COMPATIBILITY_REQUIRED_REASON
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        return out

    if family in {"tfr", "crude_birth_rate", "child_woman_ratio"}:
        out["harmonized_outcome_unit"] = unit
        out["effect_harmonized"] = _format_decimal(effect)
        out["se_harmonized"] = _format_decimal(se)
        out["harmonization_method"] = "preserved_original_aggregate_unit"
        out["poolability_reason"] = "aggregate_or_historical_unit_not_pooled_with_micro_estimates"
        return out

    out["poolability_reason"] = "unsupported_outcome_family_or_unit"
    return out


def make_effect_review_sheet(effects_path: Path, review_path: Path) -> None:
    validate_required_columns(effects_path, EFFECT_REQUIRED_COLUMNS)
    rows = read_csv(effects_path)
    review_columns = make_effect_review_columns()
    annotation_columns = [
        column
        for column in review_columns
        if column.endswith("_ra_decision") or column.endswith("_ra_notes")
    ]
    existing_annotations: dict[str, dict[str, str]] = {}
    if review_path.exists():
        for row in read_csv(review_path):
            effect_id = row.get("effect_id", "")
            if effect_id:
                existing_annotations[effect_id] = {
                    column: row.get(column, "") for column in annotation_columns
                }

    review_rows: list[dict[str, str]] = []
    for row in rows:
        effect_id = row.get("effect_id", "")
        saved_annotations = existing_annotations.get(effect_id, {})
        review_row: dict[str, str] = {}
        for column in review_columns:
            if column.endswith("_ra_decision") or column.endswith("_ra_notes"):
                review_row[column] = saved_annotations.get(column, "")
            else:
                review_row[column] = row.get(column, "")
        review_rows.append(review_row)
    write_csv(review_path, review_rows, review_columns)


def write_meta_analysis_summary(harmonized_path: Path, summary_path: Path) -> None:
    rows = read_csv(harmonized_path)
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row.get("meta_analysis_group", "not_poolable"), []).append(row)

    summary_rows: list[dict[str, str]] = []
    for group, group_rows in sorted(groups.items()):
        if group == "not_poolable":
            summary_rows.append(
                {
                    "meta_analysis_group": group,
                    "n_effects": str(len(group_rows)),
                    "synthesis_type": "structured_narrative",
                    "pooled_effect": "",
                    "pooled_se": "",
                    "rationale": (
                        "Rows are non-poolable because outcome units, treatment scales, "
                        "follow-up windows, sign orientation, standard errors, or "
                        "mechanism cells are incompatible or not yet coded."
                    ),
                }
            )
            continue

        effects = [_decimal(row.get("effect_harmonized", "")) for row in group_rows]
        ses = [_decimal(row.get("se_harmonized", "")) for row in group_rows]
        usable = [
            (effect, se)
            for effect, se in zip(effects, ses)
            if effect is not None and se is not None and se != 0
        ]
        if len(usable) < 3:
            summary_rows.append(
                {
                    "meta_analysis_group": group,
                    "n_effects": str(len(group_rows)),
                    "synthesis_type": "not_pooled",
                    "pooled_effect": "",
                    "pooled_se": "",
                    "rationale": "Fewer than three compatible effects with standard errors.",
                }
            )
            continue

        weights = [Decimal("1") / (se * se) for _, se in usable]
        weight_sum = sum(weights)
        pooled = sum(
            effect * weight for (effect, _), weight in zip(usable, weights)
        ) / weight_sum
        pooled_se = (Decimal("1") / weight_sum).sqrt()
        summary_rows.append(
            {
                "meta_analysis_group": group,
                "n_effects": str(len(usable)),
                "synthesis_type": "fixed_effect_inverse_variance_screening",
                "pooled_effect": _format_decimal(pooled),
                "pooled_se": _format_decimal(pooled_se),
                "rationale": (
                    "Screening estimate only; random-effects synthesis should replace "
                    "this if heterogeneity warrants and enough comparable estimates exist."
                ),
            }
        )

    write_csv(
        summary_path,
        summary_rows,
        [
            "meta_analysis_group",
            "n_effects",
            "synthesis_type",
            "pooled_effect",
            "pooled_se",
            "rationale",
        ],
    )


def write_summary_of_findings(summary_path: Path, sof_path: Path) -> None:
    summary_rows = read_csv(summary_path)
    has_pooled = any(
        row["synthesis_type"] == "fixed_effect_inverse_variance_screening"
        for row in summary_rows
    )
    rows = [
        {
            "outcome_or_channel": "Classic old-age-security motive",
            "studies": "Cell A extracted studies",
            "synthesis": (
                "pooled where compatible"
                if has_pooled
                else "structured quantitative narrative"
            ),
            "certainty": (
                "setting-specific direction; magnitude pending RA verification "
                "and sign orientation"
            ),
            "interpretation": (
                "The extracted Cell A set supports a real old-age-security mechanism, "
                "but its sign is not yet pooled or uniformly oriented across pension "
                "expansions, pension cuts, LTCI, historical social insurance, and "
                "baby-boom-era estimates."
            ),
        },
        {
            "outcome_or_channel": "Children as old-age-security assets",
            "studies": "Cell B mechanism studies",
            "synthesis": "not pooled with fertility effects",
            "certainty": "low-to-moderate",
            "interpretation": (
                "Mechanism evidence supports children and purchased old-age security "
                "as substitutes, but it does not estimate fertility effects."
            ),
        },
        {
            "outcome_or_channel": "Grandparental childcare",
            "studies": "Cell C studies identified by PI review",
            "synthesis": "separate SDT track outside current quantitative package",
            "certainty": "not quantified in current quantitative package",
            "interpretation": (
                "This channel is opposite-signed and should not be pooled with the "
                "classic OAS motive."
            ),
        },
        {
            "outcome_or_channel": "Demographic significance",
            "studies": "All extracted studies plus target-period derivation",
            "synthesis": "slope-sufficiency pending macro-data pass",
            "certainty": "low pending computation",
            "interpretation": (
                "Current evidence supports a real mechanism but does not yet quantify "
                "its share of PM, FDT, or SDT fertility change."
            ),
        },
    ]
    write_csv(
        sof_path,
        rows,
        ["outcome_or_channel", "studies", "synthesis", "certainty", "interpretation"],
    )


def write_evidence_map(harmonized_path: Path, evidence_map_path: Path) -> None:
    rows = read_csv(harmonized_path)
    fields = [
        "effect_id",
        "study_id",
        "mechanism_cell",
        "outcome_family",
        "harmonized_outcome_unit",
        "effect_harmonized",
        "meta_analysis_group",
        "poolability_reason",
        "needs_pi",
    ]
    write_csv(evidence_map_path, rows, fields)


def main() -> None:
    effects_path = ROOT / "extraction" / f"{SLUG}-effects.csv"
    review_path = ROOT / "output" / f"{SLUG}-effect-extraction-review.csv"
    tables_dir = ROOT / "output" / "tables"
    figures_dir = ROOT / "output" / "figures"
    harmonized_path = tables_dir / f"{SLUG}-harmonized-effects.csv"
    meta_summary_path = tables_dir / f"{SLUG}-meta-analysis-summary.csv"
    sof_path = tables_dir / f"{SLUG}-summary-of-findings.csv"
    evidence_map_path = figures_dir / f"{SLUG}-evidence-map.csv"

    if effects_path.exists():
        make_effect_review_sheet(effects_path, review_path)
        rows = [harmonize_effect_row(row) for row in read_csv(effects_path)]
        write_csv(harmonized_path, rows, HARMONIZED_COLUMNS)
        write_meta_analysis_summary(harmonized_path, meta_summary_path)
        write_summary_of_findings(meta_summary_path, sof_path)
        write_evidence_map(harmonized_path, evidence_map_path)


if __name__ == "__main__":
    main()
