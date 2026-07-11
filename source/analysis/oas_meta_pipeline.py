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
    "test_statistic_original",
    "test_statistic_type",
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
    "test_statistic_original",
    "test_statistic_type",
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

READINESS_COLUMNS = [
    "analysis_group",
    "mechanism_cell",
    "outcome_family",
    "harmonized_outcome_unit",
    "n_effects",
    "n_studies",
    "n_with_harmonized_effect",
    "n_with_harmonized_se",
    "n_primary_estimates",
    "n_needs_pi",
    "n_negative",
    "n_positive",
    "n_zero",
    "effect_min",
    "effect_max",
    "screening_fixed_effect",
    "screening_fixed_effect_se",
    "synthesis_decision",
    "primary_pooling_blocker",
    "study_ids",
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
        columns.extend([field, f"{field}_ra_decision", f"{field}_source"])
    return columns


def make_effect_source_note(row: dict[str, str], field: str) -> str:
    value = (row.get(field) or "").strip()
    if field == "needs_pi":
        return "Codex extraction flag based on ambiguity or PI-needed judgment."
    if field == "mechanism_cell":
        return "Protocol mechanism-cell coding; checked against extracted estimate context."
    if field == "extract_page":
        return "PDF locator recorded during extraction."
    if field == "extract_quote_or_note":
        return "Extraction note from the cited PDF location."
    if not value:
        return "Not reported in extracted estimate."

    locator = (row.get("extract_page") or "").strip()
    note = (row.get("extract_quote_or_note") or "").strip()
    if locator:
        return locator
    if note:
        return note[:137] + "..." if len(note) > 140 else note
    return "Extracted from the cited PDF."


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


def derive_se_from_test_statistic(effect: Decimal | None, row: dict[str, str]) -> Decimal | None:
    if effect is None:
        return None
    statistic_type = (row.get("test_statistic_type") or "").strip().lower()
    statistic = _decimal(row.get("test_statistic_original", ""))
    if statistic_type != "t_statistic" or statistic in {None, Decimal("0")}:
        return None
    return abs(effect / statistic).quantize(Decimal("0.000001"))


COMPATIBILITY_REQUIRED_REASON = (
    "requires_treatment_scale_followup_and_sign_orientation_before_pooling"
)


def harmonize_effect_row(row: dict[str, str]) -> dict[str, str]:
    out = dict(row)
    effect = _decimal(row.get("effect_original", ""))
    se = _decimal(row.get("se_original", ""))
    derived_se = derive_se_from_test_statistic(effect, row) if se is None else None
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
        source_se = se if se is not None else derived_se
        out["se_harmonized"] = (
            _format_decimal(source_se / Decimal("100")) if source_se is not None else ""
        )
        out["harmonization_method"] = (
            "percentage_points_divided_by_100"
            if derived_se is None
            else "percentage_points_divided_by_100_se_derived_from_t_statistic"
        )
        if cell == "A":
            out["poolability_reason"] = COMPATIBILITY_REQUIRED_REASON
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        return out

    if family == "completed_fertility" and unit == "births_per_woman":
        out["harmonized_outcome_unit"] = "births_per_woman"
        out["effect_harmonized"] = _format_decimal(effect)
        out["se_harmonized"] = _format_decimal(se if se is not None else derived_se)
        out["harmonization_method"] = (
            "already_births_per_woman"
            if derived_se is None
            else "already_births_per_woman_se_derived_from_t_statistic"
        )
        if cell == "A":
            out["poolability_reason"] = COMPATIBILITY_REQUIRED_REASON
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        return out

    if family in {"tfr", "crude_birth_rate", "child_woman_ratio"}:
        out["harmonized_outcome_unit"] = unit
        out["effect_harmonized"] = _format_decimal(effect)
        out["se_harmonized"] = _format_decimal(se if se is not None else derived_se)
        out["harmonization_method"] = (
            "preserved_original_aggregate_unit"
            if derived_se is None
            else "preserved_original_aggregate_unit_se_derived_from_t_statistic"
        )
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
        if column.endswith("_ra_decision")
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
            if column.endswith("_ra_decision"):
                review_row[column] = saved_annotations.get(column, "")
            elif column.endswith("_source"):
                field = column[: -len("_source")]
                review_row[column] = make_effect_source_note(row, field)
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


def _analysis_group(row: dict[str, str]) -> str:
    cell = row.get("mechanism_cell") or "unknown_cell"
    family = row.get("outcome_family") or "unknown_outcome"
    unit = row.get("harmonized_outcome_unit") or row.get("outcome_unit_original") or "unharmonized"
    return f"cell_{cell.lower()}__{family}__{unit}"


def _fixed_effect_screen(group_rows: list[dict[str, str]]) -> tuple[str, str]:
    usable: list[tuple[Decimal, Decimal]] = []
    for row in group_rows:
        effect = _decimal(row.get("effect_harmonized", ""))
        se = _decimal(row.get("se_harmonized", ""))
        if effect is not None and se is not None and se != 0:
            usable.append((effect, se))
    if len(usable) < 3:
        return "", ""
    weights = [Decimal("1") / (se * se) for _, se in usable]
    weight_sum = sum(weights)
    pooled = sum(effect * weight for (effect, _), weight in zip(usable, weights)) / weight_sum
    pooled_se = (Decimal("1") / weight_sum).sqrt()
    return (
        _format_decimal(pooled.quantize(Decimal("0.000001"))),
        _format_decimal(pooled_se.quantize(Decimal("0.000001"))),
    )


def _readiness_blocker(group_rows: list[dict[str, str]]) -> str:
    reasons = {row.get("poolability_reason", "") for row in group_rows}
    if "requires_treatment_scale_followup_and_sign_orientation_before_pooling" in reasons:
        return "treatment_scale_followup_and_sign_orientation"
    if "aggregate_or_historical_unit_not_pooled_with_micro_estimates" in reasons:
        return "aggregate_or_historical_unit"
    if "unsupported_outcome_family_or_unit" in reasons:
        return "unsupported_outcome_family_or_unit"
    if "missing_or_non_numeric_effect" in reasons:
        return "missing_or_non_numeric_effect"
    if "missing_standard_error_or_wrong_cell" in reasons:
        return "missing_standard_error_or_wrong_cell"
    return ";".join(sorted(reason for reason in reasons if reason)) or "not_assessed"


def write_meta_analysis_readiness(harmonized_path: Path, readiness_path: Path) -> None:
    rows = read_csv(harmonized_path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(_analysis_group(row), []).append(row)

    readiness_rows: list[dict[str, str]] = []
    for group, group_rows in sorted(grouped.items()):
        effects = [_decimal(row.get("effect_harmonized", "")) for row in group_rows]
        effects_present = [effect for effect in effects if effect is not None]
        ses_present = [
            _decimal(row.get("se_harmonized", ""))
            for row in group_rows
            if _decimal(row.get("se_harmonized", "")) is not None
        ]
        screening_effect, screening_se = _fixed_effect_screen(group_rows)
        blocker = _readiness_blocker(group_rows)
        if screening_effect:
            decision = "screening_only_not_pooled"
        elif effects_present:
            decision = "structured_narrative_only"
        else:
            decision = "mechanism_or_unsupported_outcome_only"

        readiness_rows.append(
            {
                "analysis_group": group,
                "mechanism_cell": group_rows[0].get("mechanism_cell", ""),
                "outcome_family": group_rows[0].get("outcome_family", ""),
                "harmonized_outcome_unit": group_rows[0].get("harmonized_outcome_unit", ""),
                "n_effects": str(len(group_rows)),
                "n_studies": str(len({row.get("study_id", "") for row in group_rows})),
                "n_with_harmonized_effect": str(len(effects_present)),
                "n_with_harmonized_se": str(len(ses_present)),
                "n_primary_estimates": str(
                    sum(1 for row in group_rows if row.get("is_primary_estimate") == "yes")
                ),
                "n_needs_pi": str(sum(1 for row in group_rows if row.get("needs_pi") == "yes")),
                "n_negative": str(sum(1 for effect in effects_present if effect < 0)),
                "n_positive": str(sum(1 for effect in effects_present if effect > 0)),
                "n_zero": str(sum(1 for effect in effects_present if effect == 0)),
                "effect_min": _format_decimal(min(effects_present)) if effects_present else "",
                "effect_max": _format_decimal(max(effects_present)) if effects_present else "",
                "screening_fixed_effect": screening_effect,
                "screening_fixed_effect_se": screening_se,
                "synthesis_decision": decision,
                "primary_pooling_blocker": blocker,
                "study_ids": ";".join(sorted({row.get("study_id", "") for row in group_rows})),
            }
        )

    write_csv(readiness_path, readiness_rows, READINESS_COLUMNS)


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
                "setting-specific direction; magnitude pending PI adjudication "
                "of needs_pi rows and sign orientation"
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
    readiness_path = tables_dir / f"{SLUG}-meta-analysis-readiness.csv"
    meta_summary_path = tables_dir / f"{SLUG}-meta-analysis-summary.csv"
    sof_path = tables_dir / f"{SLUG}-summary-of-findings.csv"
    evidence_map_path = figures_dir / f"{SLUG}-evidence-map.csv"

    if effects_path.exists():
        make_effect_review_sheet(effects_path, review_path)
        rows = [harmonize_effect_row(row) for row in read_csv(effects_path)]
        write_csv(harmonized_path, rows, HARMONIZED_COLUMNS)
        write_meta_analysis_readiness(harmonized_path, readiness_path)
        write_meta_analysis_summary(harmonized_path, meta_summary_path)
        write_summary_of_findings(meta_summary_path, sof_path)
        write_evidence_map(harmonized_path, evidence_map_path)


if __name__ == "__main__":
    main()
