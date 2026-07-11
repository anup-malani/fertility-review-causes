#!/usr/bin/env python3
"""Utilities for OAS effect extraction, review, and conservative synthesis."""

from __future__ import annotations

import csv
import math
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
    "pi_approved",
    "old_age_security_treatment_direction",
    "effect_oriented_more_oas",
    "se_oriented_more_oas",
    "orientation_method",
    "treatment_scale_harmonized",
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
    "n_unresolved_needs_pi",
    "n_pi_approved_assumed",
    "n_negative",
    "n_positive",
    "n_zero",
    "effect_min",
    "effect_max",
    "n_with_oriented_effect",
    "n_oriented_negative",
    "n_oriented_positive",
    "n_oriented_zero",
    "oriented_effect_min",
    "oriented_effect_max",
    "screening_fixed_effect",
    "screening_fixed_effect_se",
    "oriented_screening_fixed_effect",
    "oriented_screening_fixed_effect_se",
    "recommended_synthesis",
    "recommended_pooling_rule",
    "recommended_pooling_group_key",
    "recommended_pooled_effect_more_oas",
    "recommended_pooled_se_more_oas",
    "synthesis_decision",
    "primary_pooling_blocker",
    "study_ids",
]

DEMOGRAPHIC_SIGNIFICANCE_COLUMNS = [
    "phenomenon_channel",
    "target_phenomenon",
    "evidence_base",
    "n_cell_a_studies",
    "n_oriented_effects",
    "oriented_effect_direction",
    "coefficient_pooling_status",
    "slope_sufficiency",
    "demographic_significance_verdict",
    "causal_credibility_summary",
    "transition_classification_basis",
    "needs_human_review",
    "rationale",
    "next_required_step",
]

CELL_C_SLOPE_COLUMNS = [
    "effect_id",
    "study_id",
    "pdf_filename",
    "estimand_label",
    "outcome_name",
    "outcome_family",
    "harmonized_outcome_unit",
    "treatment_scale_harmonized",
    "reported_effect",
    "reported_se",
    "availability_orientation",
    "availability_oriented_effect",
    "availability_oriented_se",
    "plain_english_effect",
    "pooling_status",
    "slope_scaling_status",
    "source_locator",
]

CELL_C_SLOPE_SUFFICIENCY_COLUMNS = [
    "effect_id",
    "study_id",
    "country_or_region",
    "period_start",
    "period_end",
    "estimand_label",
    "outcome_name",
    "harmonized_outcome_unit",
    "treatment_scale_harmonized",
    "availability_oriented_effect",
    "availability_oriented_se",
    "tfr_start",
    "tfr_end",
    "observed_tfr_decline",
    "effect_share_of_observed_decline",
    "slope_sufficiency_label",
    "comparison_basis",
    "interpretation",
    "caveat",
]

GRADE_VERDICT_COLUMNS = [
    "phenomenon_channel",
    "causal_credibility",
    "demographic_significance",
    "grade_rationale",
]

OUTCOME_SPECIFIC_POOLED_COLUMNS = [
    "pooled_group",
    "mechanism_cell",
    "outcome_family",
    "harmonized_outcome_unit",
    "effect_orientation",
    "synthesis_type",
    "n_effects",
    "n_studies",
    "n_primary_estimates",
    "n_treatment_scales",
    "treatment_scales",
    "pooled_effect",
    "pooled_se",
    "ci_lower_95",
    "ci_upper_95",
    "z_statistic",
    "p_value",
    "included_effect_ids",
    "included_study_ids",
    "interpretation",
    "caveat",
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


def _format_decimal_6(value: Decimal | None) -> str:
    if value is None:
        return ""
    return _format_decimal(value.quantize(Decimal("0.000001")))


def derive_se_from_test_statistic(effect: Decimal | None, row: dict[str, str]) -> Decimal | None:
    if effect is None:
        return None
    statistic_type = (row.get("test_statistic_type") or "").strip().lower()
    statistic = _decimal(row.get("test_statistic_original", ""))
    if statistic_type != "t_statistic" or statistic in {None, Decimal("0")}:
        return None
    return abs(effect / statistic).quantize(Decimal("0.000001"))


DECREASE_OAS_EFFECT_IDS = {
    "billari_galasso_2009_italy_pension_reforms_e01",
    "billari_galasso_2009_italy_pension_reforms_e02",
}

INCREASE_OAS_EFFECT_IDS = {
    "danzer_zyska_2023_brazil_pensions_e01",
    "danzer_zyska_2023_brazil_pensions_e02",
    "rossi_godard_2022_namibia_pensions_e01",
    "rossi_godard_2022_namibia_pensions_e02",
    "han_tao_wang_zhang_2025_china_ltci_e01",
    "han_tao_wang_zhang_2025_china_ltci_e02",
    "guinnane_streb_2021_prussia_social_security_e01",
    "shen_zheng_yang_2020_china_nrps_e01",
    "shen_zheng_yang_2020_china_nrps_e02",
    "fenge_scheubel_2017_germany_pensions_e01",
    "basso_bodenhorn_cuberes_2014_us_financial_development_e01",
}

MIXED_OR_BROADER_EFFECT_IDS = {
    "galofre_vila_2023_us_baby_boom_e01",
    "galofre_vila_2023_us_baby_boom_e02",
}

INCREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS = {
    "eibich_siedler_2020_germany_parental_retirement_e01",
    "eibich_siedler_2020_germany_parental_retirement_e02",
    "akyol_atalay_2025_australia_grandmothers_pension_e01",
    "akyol_atalay_2025_australia_grandmothers_pension_e02",
}

DECREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS = {
    "ilciukas_2023_netherlands_parental_retirement_e01",
    "ilciukas_2023_netherlands_parental_retirement_e02",
    "ilciukas_2023_netherlands_parental_retirement_e03",
    "ilciukas_2023_netherlands_parental_retirement_e04",
}

TREATMENT_SCALE_BY_EFFECT_ID = {
    "danzer_zyska_2023_brazil_pensions_e01": "pension_expansion_binary_exposure",
    "danzer_zyska_2023_brazil_pensions_e02": "pension_expansion_binary_exposure",
    "rossi_godard_2022_namibia_pensions_e01": "pension_value_continuous_exposure",
    "rossi_godard_2022_namibia_pensions_e02": "pension_value_continuous_exposure",
    "billari_galasso_2009_italy_pension_reforms_e01": "pension_wealth_cut_binary_exposure",
    "billari_galasso_2009_italy_pension_reforms_e02": "pension_wealth_cut_binary_exposure",
    "han_tao_wang_zhang_2025_china_ltci_e01": "ltci_pilot_binary_exposure",
    "han_tao_wang_zhang_2025_china_ltci_e02": "ltci_pilot_binary_exposure",
    "guinnane_streb_2021_prussia_social_security_e01": "historical_social_insurance_group_dd",
    "shen_zheng_yang_2020_china_nrps_e01": "pension_participation_iv_exposure",
    "shen_zheng_yang_2020_china_nrps_e02": "pension_participation_iv_exposure",
    "fenge_scheubel_2017_germany_pensions_e01": "pension_coverage_share_percentage_point",
    "basso_bodenhorn_cuberes_2014_us_financial_development_e01": "financial_access_binary_exposure",
    "galofre_vila_2023_us_baby_boom_e01": "broad_social_spending_exposure",
    "galofre_vila_2023_us_baby_boom_e02": "broad_social_spending_exposure",
    "ci_2024_children_insurance_e01": "children_count_as_treatment_mechanism",
    "eibich_siedler_2020_germany_parental_retirement_e01": "parental_retirement_iv_binary_exposure",
    "eibich_siedler_2020_germany_parental_retirement_e02": "parental_retirement_iv_binary_exposure",
    "ilciukas_2023_netherlands_parental_retirement_e01": "delayed_maternal_retirement_reform_assignment",
    "ilciukas_2023_netherlands_parental_retirement_e02": "one_year_maternal_retirement_delay_iv",
    "ilciukas_2023_netherlands_parental_retirement_e03": "delayed_maternal_retirement_reform_assignment",
    "ilciukas_2023_netherlands_parental_retirement_e04": "one_year_maternal_retirement_delay_iv",
    "akyol_atalay_2025_australia_grandmothers_pension_e01": "maternal_grandmother_pension_eligibility_binary",
    "akyol_atalay_2025_australia_grandmothers_pension_e02": "maternal_grandmother_pension_eligibility_binary",
}


def orient_more_oas_effect(row: dict[str, str]) -> None:
    row["pi_approved"] = "yes_assumed"
    effect_id = row.get("effect_id", "")
    effect = _decimal(row.get("effect_harmonized", ""))
    se = _decimal(row.get("se_harmonized", ""))
    row["treatment_scale_harmonized"] = TREATMENT_SCALE_BY_EFFECT_ID.get(
        effect_id, "uncoded_treatment_scale"
    )

    if effect_id in DECREASE_OAS_EFFECT_IDS:
        row["old_age_security_treatment_direction"] = "decrease_oas"
        row["effect_oriented_more_oas"] = _format_decimal(-effect) if effect is not None else ""
        row["se_oriented_more_oas"] = _format_decimal(se)
        row["orientation_method"] = "sign_flipped_because_treatment_decreases_oas"
        return

    if effect_id in INCREASE_OAS_EFFECT_IDS:
        row["old_age_security_treatment_direction"] = "increase_oas"
        row["effect_oriented_more_oas"] = _format_decimal(effect)
        row["se_oriented_more_oas"] = _format_decimal(se)
        row["orientation_method"] = "as_reported_treatment_increases_oas"
        return

    if effect_id in MIXED_OR_BROADER_EFFECT_IDS:
        row["old_age_security_treatment_direction"] = "mixed_or_broader_oas"
        row["effect_oriented_more_oas"] = ""
        row["se_oriented_more_oas"] = ""
        row["orientation_method"] = "not_oriented_broader_social_spending_mechanism"
        return

    row["old_age_security_treatment_direction"] = "not_oas_fertility_effect"
    row["effect_oriented_more_oas"] = ""
    row["se_oriented_more_oas"] = ""
    row["orientation_method"] = "not_oriented_non_fertility_or_uncoded_effect"


COMPATIBILITY_REQUIRED_REASON = (
    "requires_treatment_scale_followup_target_setting_before_pooling"
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
            "pi_approved": "",
            "old_age_security_treatment_direction": "",
            "effect_oriented_more_oas": "",
            "se_oriented_more_oas": "",
            "orientation_method": "",
            "treatment_scale_harmonized": "",
            "meta_analysis_group": "not_poolable",
            "poolability_reason": "",
        }
    )

    if effect is None:
        out["poolability_reason"] = "missing_or_non_numeric_effect"
        orient_more_oas_effect(out)
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
        elif cell == "C":
            out["poolability_reason"] = "cell_c_separate_grandparent_childcare_track"
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        orient_more_oas_effect(out)
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
        elif cell == "C":
            out["poolability_reason"] = "cell_c_separate_grandparent_childcare_track"
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        orient_more_oas_effect(out)
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
        orient_more_oas_effect(out)
        return out

    out["poolability_reason"] = "unsupported_outcome_family_or_unit"
    orient_more_oas_effect(out)
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
                        "Rows are non-poolable under the strict same-treatment rule "
                        "because outcome units, treatment scales, follow-up windows, "
                        "target settings, standard errors, or mechanism cells are "
                        "incompatible or not yet coded. See the outcome-specific "
                        "pooled-estimates table for looser within-outcome summaries."
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


def _normal_two_sided_p_value(z_statistic: Decimal) -> str:
    p_value = math.erfc(abs(float(z_statistic)) / math.sqrt(2))
    return _format_decimal_6(Decimal(str(p_value)))


def _pooled_interpretation(
    mechanism_cell: str, outcome_family: str, unit: str, pooled: Decimal
) -> str:
    direction = "raises fertility" if pooled > 0 else "lowers fertility" if pooled < 0 else "has no average effect on fertility"
    if mechanism_cell == "A":
        return (
            f"Within the {outcome_family} outcome family, more non-child old-age "
            f"security {direction} on average on the {unit} scale."
        )
    if mechanism_cell == "C":
        return (
            f"Within the {outcome_family} outcome family, more grandparent "
            f"availability {direction} on average on the {unit} scale."
        )
    return (
        f"Within the {outcome_family} outcome family, the pooled estimate "
        f"{direction} on average on the {unit} scale."
    )


def _rows_for_outcome_specific_pooling(
    harmonized_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in harmonized_rows:
        if row.get("mechanism_cell") != "A":
            continue
        effect = _decimal(row.get("effect_oriented_more_oas", ""))
        se = _decimal(row.get("se_oriented_more_oas", ""))
        if effect is None or se in {None, Decimal("0")}:
            continue
        if not row.get("harmonized_outcome_unit"):
            continue
        rows.append(row)
    return rows


def write_outcome_specific_pooled_estimates(
    harmonized_path: Path, pooled_path: Path
) -> None:
    rows = _rows_for_outcome_specific_pooling(read_csv(harmonized_path))
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (
            row.get("mechanism_cell", ""),
            row.get("outcome_family", ""),
            row.get("harmonized_outcome_unit", ""),
        )
        grouped.setdefault(key, []).append(row)

    pooled_rows: list[dict[str, str]] = []
    for (mechanism_cell, outcome_family, unit), group_rows in sorted(grouped.items()):
        if len(group_rows) < 3:
            continue
        effects_and_ses = [
            (
                _decimal(row.get("effect_oriented_more_oas", "")),
                _decimal(row.get("se_oriented_more_oas", "")),
            )
            for row in group_rows
        ]
        usable = [
            (effect, se)
            for effect, se in effects_and_ses
            if effect is not None and se is not None and se != 0
        ]
        if len(usable) < 3:
            continue
        weights = [Decimal("1") / (se * se) for _, se in usable]
        weight_sum = sum(weights)
        pooled = sum(effect * weight for (effect, _), weight in zip(usable, weights)) / weight_sum
        pooled_se = (Decimal("1") / weight_sum).sqrt()
        ci_delta = Decimal("1.96") * pooled_se
        z_statistic = pooled / pooled_se
        treatment_scales = sorted(
            {row.get("treatment_scale_harmonized", "") for row in group_rows}
        )
        n_studies = len({row.get("study_id", "") for row in group_rows})
        synthesis_type = (
            "outcome_specific_fixed_effect_inverse_variance"
            if n_studies >= 3
            else "exploratory_dependent_effect_rows"
        )
        caveat = (
            "Outcome-specific pooled summary; treatment scales differ, so this is "
            "not a single structural treatment effect."
        )
        if n_studies < len(group_rows):
            caveat += " Multiple effects come from at least one study."
        pooled_rows.append(
            {
                "pooled_group": "__".join(
                    [f"cell_{mechanism_cell.lower()}", outcome_family, unit]
                ),
                "mechanism_cell": mechanism_cell,
                "outcome_family": outcome_family,
                "harmonized_outcome_unit": unit,
                "effect_orientation": "effect_of_more_non_child_old_age_security",
                "synthesis_type": synthesis_type,
                "n_effects": str(len(group_rows)),
                "n_studies": str(n_studies),
                "n_primary_estimates": str(
                    sum(1 for row in group_rows if row.get("is_primary_estimate") == "yes")
                ),
                "n_treatment_scales": str(len(treatment_scales)),
                "treatment_scales": ";".join(treatment_scales),
                "pooled_effect": _format_decimal_6(pooled),
                "pooled_se": _format_decimal_6(pooled_se),
                "ci_lower_95": _format_decimal_6(pooled - ci_delta),
                "ci_upper_95": _format_decimal_6(pooled + ci_delta),
                "z_statistic": _format_decimal_6(z_statistic),
                "p_value": _normal_two_sided_p_value(z_statistic),
                "included_effect_ids": ";".join(row.get("effect_id", "") for row in group_rows),
                "included_study_ids": ";".join(
                    sorted({row.get("study_id", "") for row in group_rows})
                ),
                "interpretation": _pooled_interpretation(
                    mechanism_cell, outcome_family, unit, pooled
                ),
                "caveat": caveat,
            }
        )

    write_csv(pooled_path, pooled_rows, OUTCOME_SPECIFIC_POOLED_COLUMNS)


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


def _fixed_effect_screen_for_fields(
    group_rows: list[dict[str, str]], effect_field: str, se_field: str
) -> tuple[str, str]:
    usable: list[tuple[Decimal, Decimal]] = []
    for row in group_rows:
        effect = _decimal(row.get(effect_field, ""))
        se = _decimal(row.get(se_field, ""))
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


def _recommended_pooling(group_rows: list[dict[str, str]]) -> dict[str, str]:
    usable = [
        row
        for row in group_rows
        if _decimal(row.get("effect_oriented_more_oas", "")) is not None
        and _decimal(row.get("se_oriented_more_oas", "")) not in {None, Decimal("0")}
    ]
    rule = (
        "Pool coefficient estimates only when mechanism cell, outcome family, "
        "harmonized unit, treatment scale, and usable "
        "oriented standard errors match across at least three independent studies."
    )
    if len({row.get("study_id", "") for row in usable}) < 3:
        return {
            "recommended_synthesis": "do_not_pool_too_few_usable_effects",
            "recommended_pooling_rule": rule,
            "recommended_pooling_group_key": "",
            "recommended_pooled_effect_more_oas": "",
            "recommended_pooled_se_more_oas": "",
        }

    treatment_scales = {
        row.get("treatment_scale_harmonized", "") for row in usable
    }
    if len(treatment_scales) != 1:
        return {
            "recommended_synthesis": "do_not_pool_mixed_treatment_scales",
            "recommended_pooling_rule": rule,
            "recommended_pooling_group_key": "",
            "recommended_pooled_effect_more_oas": "",
            "recommended_pooled_se_more_oas": "",
        }

    pooled_effect, pooled_se = _fixed_effect_screen_for_fields(
        usable, "effect_oriented_more_oas", "se_oriented_more_oas"
    )
    if not pooled_effect:
        return {
            "recommended_synthesis": "do_not_pool_too_few_usable_effects",
            "recommended_pooling_rule": rule,
            "recommended_pooling_group_key": "",
            "recommended_pooled_effect_more_oas": "",
            "recommended_pooled_se_more_oas": "",
        }

    exemplar = usable[0]
    key_parts = [
        exemplar.get("mechanism_cell", ""),
        exemplar.get("outcome_family", ""),
        exemplar.get("harmonized_outcome_unit", ""),
        exemplar.get("treatment_scale_harmonized", ""),
    ]
    return {
        "recommended_synthesis": "pool_fixed_effect_same_scale",
        "recommended_pooling_rule": rule,
        "recommended_pooling_group_key": "__".join(key_parts),
        "recommended_pooled_effect_more_oas": pooled_effect,
        "recommended_pooled_se_more_oas": pooled_se,
    }


def _readiness_blocker(group_rows: list[dict[str, str]]) -> str:
    reasons = {row.get("poolability_reason", "") for row in group_rows}
    if "requires_treatment_scale_followup_target_setting_before_pooling" in reasons:
        return "treatment_scale_followup_target_setting"
    if "requires_treatment_scale_followup_and_sign_orientation_before_pooling" in reasons:
        return "treatment_scale_followup_target_setting"
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
        oriented_effects = [
            _decimal(row.get("effect_oriented_more_oas", "")) for row in group_rows
        ]
        oriented_effects_present = [
            effect for effect in oriented_effects if effect is not None
        ]
        ses_present = [
            _decimal(row.get("se_harmonized", ""))
            for row in group_rows
            if _decimal(row.get("se_harmonized", "")) is not None
        ]
        screening_effect, screening_se = _fixed_effect_screen(group_rows)
        oriented_screening_effect, oriented_screening_se = _fixed_effect_screen_for_fields(
            group_rows, "effect_oriented_more_oas", "se_oriented_more_oas"
        )
        recommended_pooling = _recommended_pooling(group_rows)
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
                "n_unresolved_needs_pi": str(
                    sum(
                        1
                        for row in group_rows
                        if row.get("needs_pi") == "yes"
                        and row.get("pi_approved") != "yes_assumed"
                    )
                ),
                "n_pi_approved_assumed": str(
                    sum(1 for row in group_rows if row.get("pi_approved") == "yes_assumed")
                ),
                "n_negative": str(sum(1 for effect in effects_present if effect < 0)),
                "n_positive": str(sum(1 for effect in effects_present if effect > 0)),
                "n_zero": str(sum(1 for effect in effects_present if effect == 0)),
                "effect_min": _format_decimal(min(effects_present)) if effects_present else "",
                "effect_max": _format_decimal(max(effects_present)) if effects_present else "",
                "n_with_oriented_effect": str(len(oriented_effects_present)),
                "n_oriented_negative": str(
                    sum(1 for effect in oriented_effects_present if effect < 0)
                ),
                "n_oriented_positive": str(
                    sum(1 for effect in oriented_effects_present if effect > 0)
                ),
                "n_oriented_zero": str(
                    sum(1 for effect in oriented_effects_present if effect == 0)
                ),
                "oriented_effect_min": (
                    _format_decimal(min(oriented_effects_present))
                    if oriented_effects_present
                    else ""
                ),
                "oriented_effect_max": (
                    _format_decimal(max(oriented_effects_present))
                    if oriented_effects_present
                    else ""
                ),
                "screening_fixed_effect": screening_effect,
                "screening_fixed_effect_se": screening_se,
                "oriented_screening_fixed_effect": oriented_screening_effect,
                "oriented_screening_fixed_effect_se": oriented_screening_se,
                **recommended_pooling,
                "synthesis_decision": decision,
                "primary_pooling_blocker": blocker,
                "study_ids": ";".join(sorted({row.get("study_id", "") for row in group_rows})),
            }
        )

    write_csv(readiness_path, readiness_rows, READINESS_COLUMNS)


def write_summary_of_findings(
    summary_path: Path, sof_path: Path, pooled_path: Path | None = None
) -> None:
    summary_rows = read_csv(summary_path)
    pooled_rows = read_csv(pooled_path) if pooled_path is not None and pooled_path.exists() else []
    has_pooled = any(
        row["synthesis_type"] == "fixed_effect_inverse_variance_screening"
        for row in summary_rows
    )
    has_outcome_specific_pooled = bool(pooled_rows)
    pooled_group_summary = "; ".join(
        f"{row['outcome_family']} = {row['pooled_effect']} ({row['harmonized_outcome_unit']})"
        for row in pooled_rows
        if row.get("mechanism_cell") == "A"
    )
    rows = [
        {
            "outcome_or_channel": "Classic old-age-security motive",
            "studies": "Cell A extracted studies",
            "synthesis": (
                "outcome-specific fixed-effect summaries plus structured interpretation"
                if has_outcome_specific_pooled
                else "pooled where compatible"
                if has_pooled
                else "structured quantitative narrative"
            ),
            "certainty": (
                "setting-specific direction; treatment-scale heterogeneity remains"
                if has_outcome_specific_pooled
                else "setting-specific direction; not coefficient-pooled under same-scale rule"
            ),
            "interpretation": (
                "The extracted Cell A set supports a real old-age-security mechanism "
                "after orienting eligible estimates to the effect of more non-child "
                "old-age security. Outcome-specific fixed-effect summaries are "
                f"reported for: {pooled_group_summary}. These are not interpreted "
                "as a single structural treatment effect because treatment scales differ."
                if has_outcome_specific_pooled
                else (
                    "The extracted Cell A set supports a real old-age-security mechanism "
                    "after orienting eligible estimates to the effect of more non-child "
                    "old-age security, but the magnitudes are not coefficient-pooled "
                    "because the candidate numeric families mix treatment scales."
                )
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
            "studies": "Extracted Cell C studies identified by PI review",
            "synthesis": "separate SDT structured quantitative synthesis; not pooled with Cell A",
            "certainty": "moderate for direction; large slope-screening effects in declining-TFR windows",
            "interpretation": (
                "This channel is opposite to the classic old-age-security crowd-out "
                "logic: greater grandparent availability tends to raise fertility, "
                "while delayed retirement tends to lower it. Six Cell C rows are large "
                "relative to observed TFR declines in the Netherlands and Australia; "
                "the two Germany rows are not slope-scaled because Germany's TFR rises "
                "over the SOEP study window."
            ),
        },
        {
            "outcome_or_channel": "Demographic significance",
            "studies": "All extracted studies plus TFR transition classification",
            "synthesis": "structured PM/FDT/SDT demographic-significance table",
            "certainty": "low-to-moderate, channel-specific",
            "interpretation": (
                "Current evidence supports partial FDT relevance for the classic OAS "
                "motive, weak or contextual SDT relevance for the classic motive, "
                "and partial SDT relevance for the grandparental-childcare channel "
                "based on the Cell C slope-sufficiency screen."
            ),
        },
    ]
    write_csv(
        sof_path,
        rows,
        ["outcome_or_channel", "studies", "synthesis", "certainty", "interpretation"],
    )


def _study_transition_map(transition_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("study_id", ""): row for row in transition_rows if row.get("study_id", "")}


def _cell_a_rows_for_transition(
    harmonized_rows: list[dict[str, str]],
    transition_by_study: dict[str, dict[str, str]],
    token: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in harmonized_rows:
        if row.get("mechanism_cell") != "A":
            continue
        transition = transition_by_study.get(row.get("study_id", ""), {})
        label = transition.get("derived_period_target_relevance_tfr", "")
        if token in label:
            rows.append(row)
    return rows


def _cell_c_rows_for_transition(
    harmonized_rows: list[dict[str, str]],
    transition_by_study: dict[str, dict[str, str]],
    token: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in harmonized_rows:
        if row.get("mechanism_cell") != "C":
            continue
        transition = transition_by_study.get(row.get("study_id", ""), {})
        label = transition.get("derived_period_target_relevance_tfr", "")
        if token in label:
            rows.append(row)
    return rows


def _unique_studies(rows: list[dict[str, str]]) -> set[str]:
    return {row.get("study_id", "") for row in rows if row.get("study_id", "")}


def _oriented_effects(rows: list[dict[str, str]]) -> list[Decimal]:
    return [
        effect
        for effect in (_decimal(row.get("effect_oriented_more_oas", "")) for row in rows)
        if effect is not None
    ]


def _harmonized_effects(rows: list[dict[str, str]]) -> list[Decimal]:
    return [
        effect
        for effect in (_decimal(row.get("effect_harmonized", "")) for row in rows)
        if effect is not None
    ]


def _cell_c_effects_oriented_more_grandparent_availability(
    rows: list[dict[str, str]],
) -> list[Decimal]:
    oriented: list[Decimal] = []
    for row in rows:
        effect = _decimal(row.get("effect_harmonized", ""))
        if effect is None:
            continue
        effect_id = row.get("effect_id", "")
        if effect_id in DECREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
            oriented.append(-effect)
        elif effect_id in INCREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
            oriented.append(effect)
    return oriented


def _cell_c_availability_orientation(effect_id: str) -> str:
    if effect_id in DECREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
        return "sign_flipped_delayed_retirement_reduces_availability"
    if effect_id in INCREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
        return "as_reported_treatment_increases_availability"
    return "uncoded_cell_c_orientation"


def _cell_c_oriented_effect(row: dict[str, str]) -> Decimal | None:
    effect = _decimal(row.get("effect_harmonized", ""))
    if effect is None:
        return None
    effect_id = row.get("effect_id", "")
    if effect_id in DECREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
        return -effect
    if effect_id in INCREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
        return effect
    return None


def _cell_c_plain_english(row: dict[str, str], oriented_effect: Decimal | None) -> str:
    unit = row.get("harmonized_outcome_unit", "") or row.get("outcome_unit_original", "")
    formatted = _format_decimal(oriented_effect)
    effect_id = row.get("effect_id", "")
    if not formatted:
        return "Effect is not numerically oriented to grandparent availability."
    if effect_id in DECREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
        return (
            "Delayed retirement/reduced grandparent availability lowers fertility; "
            f"oriented to more grandparent availability, the effect is {formatted} {unit}."
        )
    if effect_id in INCREASE_GRANDPARENT_AVAILABILITY_EFFECT_IDS:
        return (
            "Greater grandparent availability raises fertility; "
            f"the effect is {formatted} {unit}."
        )
    return f"Cell C effect is {formatted} {unit}, but orientation needs review."


def make_cell_c_slope_rows(harmonized_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in harmonized_rows:
        if row.get("mechanism_cell") != "C":
            continue
        oriented_effect = _cell_c_oriented_effect(row)
        se = _decimal(row.get("se_harmonized", ""))
        rows.append(
            {
                "effect_id": row.get("effect_id", ""),
                "study_id": row.get("study_id", ""),
                "pdf_filename": row.get("pdf_filename", ""),
                "estimand_label": row.get("estimand_label", ""),
                "outcome_name": row.get("outcome_name", ""),
                "outcome_family": row.get("outcome_family", ""),
                "harmonized_outcome_unit": row.get("harmonized_outcome_unit", ""),
                "treatment_scale_harmonized": row.get("treatment_scale_harmonized", ""),
                "reported_effect": row.get("effect_harmonized", ""),
                "reported_se": row.get("se_harmonized", ""),
                "availability_orientation": _cell_c_availability_orientation(
                    row.get("effect_id", "")
                ),
                "availability_oriented_effect": _format_decimal(oriented_effect),
                "availability_oriented_se": _format_decimal(se),
                "plain_english_effect": _cell_c_plain_english(row, oriented_effect),
                "pooling_status": "do_not_coefficient_pool_distinct_treatment_scales",
                "slope_scaling_status": "ready_for_manual_or_macro_scale_assumption",
                "source_locator": "; ".join(
                    part
                    for part in [
                        row.get("extract_page", ""),
                        row.get("extract_quote_or_note", ""),
                    ]
                    if part
                ),
            }
        )
    return rows


def write_cell_c_slope_note(rows: list[dict[str, str]], note_path: Path) -> None:
    studies = sorted({row["study_id"] for row in rows if row.get("study_id")})
    units = sorted(
        {row["harmonized_outcome_unit"] for row in rows if row.get("harmonized_outcome_unit")}
    )
    positive = sum(
        1
        for row in rows
        if (_decimal(row.get("availability_oriented_effect", "")) or Decimal("0")) > 0
    )
    negative = sum(
        1
        for row in rows
        if (_decimal(row.get("availability_oriented_effect", "")) or Decimal("0")) < 0
    )
    lines = [
        "# Cell C Slope Scaling",
        "",
        "## What This Table Does",
        "",
        (
            "This is the noob-readable Cell C synthesis table for the OAS chapter. It "
            "takes the extracted grandparental-childcare estimates and orients them to "
            "one interpretation: more grandparent availability."
        ),
        "",
        "## Current Result",
        "",
        f"- {len(studies)} studies and {len(rows)} effect rows are included.",
        f"- Harmonized outcome units present: {', '.join(units) if units else 'none'}.",
        f"- Direction after orientation: {positive} positive, {negative} negative.",
        (
            "- Do not coefficient-pool these rows. The studies use different treatments: "
            "parental retirement, delayed maternal retirement, and grandmother pension "
            "eligibility."
        ),
        "",
        "## How To Read It",
        "",
        (
            "A positive availability-oriented effect means greater grandparent availability "
            "is associated with higher fertility. Ilciukas is sign-flipped because its "
            "treatment is delayed retirement, which reduces grandparent availability."
        ),
        "",
        "## Next Scaling Step",
        "",
        (
            "To turn this into slope sufficiency, choose a policy-scale assumption such as "
            "a one-year retirement-age delay or an observed change in grandmother pension "
            "eligibility, then compare the implied fertility change with the observed SDT "
            "TFR decline in the same setting."
        ),
        "",
    ]
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text("\n".join(lines), encoding="utf-8")


def write_cell_c_slope_scaling(
    harmonized_path: Path, output_path: Path, note_path: Path
) -> None:
    rows = make_cell_c_slope_rows(read_csv(harmonized_path))
    write_csv(output_path, rows, CELL_C_SLOPE_COLUMNS)
    write_cell_c_slope_note(rows, note_path)


def _contribution_label(share: Decimal | None) -> str:
    if share is None:
        return "not_computed"
    if share < Decimal("0.05"):
        return "small"
    if share <= Decimal("0.15"):
        return "moderate"
    return "large"


def _sufficiency_label(
    share: Decimal | None, decline: Decimal | None, effect: Decimal | None
) -> str:
    if decline is not None and decline <= 0:
        return "not_applicable_no_observed_decline"
    if effect is None or decline is None:
        return "not_computed"
    return _contribution_label(share)


def _format_share(value: Decimal | None) -> str:
    if value is None:
        return ""
    return _format_decimal(value.quantize(Decimal("0.0001")))


def make_cell_c_slope_sufficiency_rows(
    slope_rows: list[dict[str, str]], transition_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    transition_by_study = _study_transition_map(transition_rows)
    rows: list[dict[str, str]] = []
    for row in slope_rows:
        transition = transition_by_study.get(row.get("study_id", ""), {})
        effect = _decimal(row.get("availability_oriented_effect", ""))
        tfr_start = _decimal(transition.get("tfr_start", ""))
        tfr_end = _decimal(transition.get("tfr_end", ""))
        decline = None
        share = None
        if tfr_start is not None and tfr_end is not None:
            decline = tfr_start - tfr_end
            if decline > 0 and effect is not None:
                share = abs(effect) / abs(decline)
        country = transition.get("country_or_region", "")
        if share is not None:
            interpretation = (
                f"Effect is about {(share * Decimal('100')).quantize(Decimal('0.1'))}% "
                f"of the observed SDT TFR decline in {country}."
            )
        elif decline is not None and decline <= 0:
            interpretation = (
                f"No slope-sufficiency share computed because TFR did not decline in "
                f"{country} over this study window."
            )
        else:
            interpretation = (
                "Effect share is not computed because the effect or TFR decline is missing."
            )
        label = _sufficiency_label(share, decline, effect)
        rows.append(
            {
                "effect_id": row.get("effect_id", ""),
                "study_id": row.get("study_id", ""),
                "country_or_region": country,
                "period_start": transition.get("period_start", ""),
                "period_end": transition.get("period_end", ""),
                "estimand_label": row.get("estimand_label", ""),
                "outcome_name": row.get("outcome_name", ""),
                "harmonized_outcome_unit": row.get("harmonized_outcome_unit", ""),
                "treatment_scale_harmonized": row.get("treatment_scale_harmonized", ""),
                "availability_oriented_effect": row.get(
                    "availability_oriented_effect", ""
                ),
                "availability_oriented_se": row.get("availability_oriented_se", ""),
                "tfr_start": transition.get("tfr_start", ""),
                "tfr_end": transition.get("tfr_end", ""),
                "observed_tfr_decline": (
                    _format_decimal(decline)
                    if decline is not None and decline > 0
                    else ""
                ),
                "effect_share_of_observed_decline": _format_share(share),
                "slope_sufficiency_label": label,
                "comparison_basis": (
                    "absolute availability-oriented effect divided by absolute observed "
                    "TFR decline over the study window"
                ),
                "interpretation": interpretation,
                "caveat": (
                    "Noob-scale comparison only: outcomes include probabilities and births "
                    "per woman, while observed decline is TFR; use for slope-sufficiency "
                    "screening, not coefficient pooling."
                ),
            }
        )
    return rows


def write_cell_c_slope_sufficiency_note(
    rows: list[dict[str, str]], note_path: Path
) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        label = row.get("slope_sufficiency_label", "not_computed")
        counts[label] = counts.get(label, 0) + 1
    count_text = ", ".join(
        f"{counts[label]} {label}"
        for label in [
            "small",
            "moderate",
            "large",
            "not_applicable_no_observed_decline",
            "not_computed",
        ]
        if counts.get(label)
    )
    lines = [
        "# Cell C Slope Sufficiency",
        "",
        "## What This Adds",
        "",
        (
            "This table compares each Cell C availability-oriented effect with the observed "
            "TFR decline in that study's country and window. It is a first-pass magnitude "
            "screen, not a pooled meta-analysis."
        ),
        "",
        "## Rule",
        "",
        "- Share < 5% of observed TFR decline: small.",
        "- Share between 5% and 15%: moderate.",
        "- Share > 15%: large.",
        "",
        "## Current Result",
        "",
        f"- {len(rows)} Cell C effect rows were compared.",
        f"- Labels: {count_text if count_text else 'none'}.",
        "",
        "## Caveat",
        "",
        (
            "The comparison intentionally keeps the math simple for chapter drafting. It "
            "divides effect magnitudes by observed TFR declines even when the paper outcome "
            "is a birth probability rather than TFR. Treat the labels as slope-sufficiency "
            "screening language, not as exact decomposition shares."
        ),
        "",
    ]
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text("\n".join(lines), encoding="utf-8")


def write_cell_c_slope_sufficiency(
    slope_path: Path, transition_path: Path, output_path: Path, note_path: Path
) -> None:
    rows = make_cell_c_slope_sufficiency_rows(
        read_csv(slope_path), read_csv(transition_path)
    )
    write_csv(output_path, rows, CELL_C_SLOPE_SUFFICIENCY_COLUMNS)
    write_cell_c_slope_sufficiency_note(rows, note_path)


def write_grade_verdicts(output_path: Path) -> None:
    rows = [
        {
            "phenomenon_channel": "PM_classic_oas",
            "causal_credibility": "very_low",
            "demographic_significance": "insufficient_direct_evidence",
            "grade_rationale": (
                "The mechanism is theoretically plausible, but the extracted evidence "
                "does not contain direct pre-modern causal estimates."
            ),
        },
        {
            "phenomenon_channel": "FDT_classic_oas",
            "causal_credibility": "low_to_moderate",
            "demographic_significance": "partial",
            "grade_rationale": (
                "The mechanism is supported in household and historical evidence, but "
                "state pensions are usually late for the Western FDT; the best-timed "
                "version is broader financial-market substitution."
            ),
        },
        {
            "phenomenon_channel": "SDT_classic_oas",
            "causal_credibility": "low",
            "demographic_significance": "not_significant_or_contextual",
            "grade_rationale": (
                "Rich-country pension systems are mostly saturated by the SDT, and "
                "some low-fertility evidence comes from policy-constrained China."
            ),
        },
        {
            "phenomenon_channel": "SDT_grandparental_childcare",
            "causal_credibility": "moderate",
            "demographic_significance": "partial_with_slope_screening_support",
            "grade_rationale": (
                "Three quasi-experimental rich-country studies point in the same "
                "availability-oriented direction, and six slope-sufficiency rows are "
                "large relative to observed TFR declines where a decline denominator exists."
            ),
        },
    ]
    write_csv(output_path, rows, GRADE_VERDICT_COLUMNS)




def _direction_summary(effects: list[Decimal]) -> str:
    if not effects:
        return "not_quantified"
    has_negative = any(effect < 0 for effect in effects)
    has_positive = any(effect > 0 for effect in effects)
    if has_negative and has_positive:
        return "mixed"
    if has_negative:
        return "negative"
    if has_positive:
        return "positive"
    return "zero"


def _any_needs_human_review(
    rows: list[dict[str, str]], transition_by_study: dict[str, dict[str, str]]
) -> str:
    for row in rows:
        transition = transition_by_study.get(row.get("study_id", ""), {})
        if transition.get("needs_human_review") == "yes":
            return "yes"
    return "no"


def _pooling_status(readiness_rows: list[dict[str, str]]) -> str:
    statuses = {row.get("recommended_synthesis", "") for row in readiness_rows}
    if "pool_fixed_effect_same_scale" in statuses:
        return "pooled_same_scale_subset_available"
    if "do_not_pool_mixed_treatment_scales" in statuses:
        return "not_coefficient_pooled_mixed_treatment_scales"
    return "not_coefficient_pooled"


def _transition_basis(
    rows: list[dict[str, str]], transition_by_study: dict[str, dict[str, str]]
) -> str:
    labels = sorted(
        {
            transition_by_study.get(row.get("study_id", ""), {}).get(
                "derived_period_target_relevance_tfr", ""
            )
            for row in rows
            if transition_by_study.get(row.get("study_id", ""), {}).get(
                "derived_period_target_relevance_tfr", ""
            )
        }
    )
    return ";".join(labels)


def write_demographic_significance(
    harmonized_path: Path,
    readiness_path: Path,
    transition_path: Path,
    output_path: Path,
) -> None:
    harmonized_rows = read_csv(harmonized_path)
    readiness_rows = read_csv(readiness_path)
    transition_by_study = _study_transition_map(read_csv(transition_path))
    pooling_status = _pooling_status(readiness_rows)

    fdt_rows = _cell_a_rows_for_transition(harmonized_rows, transition_by_study, "FDT")
    sdt_rows = _cell_a_rows_for_transition(harmonized_rows, transition_by_study, "SDT")
    sdt_cell_c_rows = _cell_c_rows_for_transition(
        harmonized_rows, transition_by_study, "SDT"
    )
    fdt_effects = _oriented_effects(fdt_rows)
    sdt_effects = _oriented_effects(sdt_rows)
    sdt_cell_c_effects = _cell_c_effects_oriented_more_grandparent_availability(
        sdt_cell_c_rows
    )

    rows = [
        {
            "phenomenon_channel": "PM",
            "target_phenomenon": "Pre-modern fertility variation",
            "evidence_base": "No direct pre-modern Cell A causal estimate in the extracted OAS set.",
            "n_cell_a_studies": "0",
            "n_oriented_effects": "0",
            "oriented_effect_direction": "not_quantified",
            "coefficient_pooling_status": "not_applicable",
            "slope_sufficiency": "not_computed_no_direct_estimate",
            "demographic_significance_verdict": "insufficient_direct_evidence",
            "causal_credibility_summary": (
                "Mechanism is theoretically plausible as a background old-age-support motive, "
                "but the current extracted evidence is not pre-modern causal evidence."
            ),
            "transition_classification_basis": "PM not assigned by replacement-status TFR rule.",
            "needs_human_review": "no",
            "rationale": (
                "Children can provide old-age support in pre-modern settings, but this is a "
                "baseline motive rather than a quantified explanation of variation in the "
                "current evidence package."
            ),
            "next_required_step": "Use theory section and historical narrative; do not report a numeric PM contribution from current Cell A effects.",
        },
        {
            "phenomenon_channel": "FDT",
            "target_phenomenon": "First Demographic Transition",
            "evidence_base": "Cell A studies classified as FDT or FDT|SDT by the TFR replacement-status rule.",
            "n_cell_a_studies": str(len(_unique_studies(fdt_rows))),
            "n_oriented_effects": str(len(fdt_effects)),
            "oriented_effect_direction": _direction_summary(fdt_effects),
            "coefficient_pooling_status": pooling_status,
            "slope_sufficiency": "partial_not_formally_scaled",
            "demographic_significance_verdict": "partial",
            "causal_credibility_summary": (
                "Credible household-level OAS effects exist in FDT-like settings, but the "
                "state-pension margin is often late for the classic Western FDT."
            ),
            "transition_classification_basis": _transition_basis(fdt_rows, transition_by_study),
            "needs_human_review": _any_needs_human_review(fdt_rows, transition_by_study),
            "rationale": (
                "The sign-oriented Cell A evidence supports the mechanism in above-replacement "
                "or crossing settings, but treatment scales are not coefficient-pooled and "
                "historical timing limits claims that state pensions initiated the FDT."
            ),
            "next_required_step": "Compute slope sufficiency against observed FDT TFR changes where treatment-scale changes are interpretable.",
        },
        {
            "phenomenon_channel": "SDT_classic_oas",
            "target_phenomenon": "Second Demographic Transition, classic old-age-security motive",
            "evidence_base": "Cell A studies classified as SDT or FDT|SDT by the TFR replacement-status rule.",
            "n_cell_a_studies": str(len(_unique_studies(sdt_rows))),
            "n_oriented_effects": str(len(sdt_effects)),
            "oriented_effect_direction": _direction_summary(sdt_effects),
            "coefficient_pooling_status": pooling_status,
            "slope_sufficiency": "unlikely_or_contextual_not_formally_scaled",
            "demographic_significance_verdict": "not_significant_or_contextual",
            "causal_credibility_summary": (
                "Below-replacement Cell A evidence exists, but China is policy-constrained "
                "and mature rich-country pension systems leave little new classic-OAS margin."
            ),
            "transition_classification_basis": _transition_basis(sdt_rows, transition_by_study),
            "needs_human_review": _any_needs_human_review(sdt_rows, transition_by_study),
            "rationale": (
                "The classic OAS motive can operate below replacement where pension margins "
                "are newly changing, but it is not yet a quantitatively credible explanation "
                "of the rich-country SDT decline."
            ),
            "next_required_step": "Separate policy-constrained China from rich-country SDT before any final SDT demographic-significance claim.",
        },
        {
            "phenomenon_channel": "SDT_grandparental_childcare",
            "target_phenomenon": "Second Demographic Transition, grandparental-childcare channel",
            "evidence_base": "Extracted Cell C studies identified by PI review.",
            "n_cell_a_studies": str(len(_unique_studies(sdt_cell_c_rows))),
            "n_oriented_effects": str(len(sdt_cell_c_effects)),
            "oriented_effect_direction": _direction_summary(sdt_cell_c_effects),
            "coefficient_pooling_status": "not_coefficient_pooled_separate_cell_c_track",
            "slope_sufficiency": "large_screening_effects_but_not_formal_decomposition",
            "demographic_significance_verdict": "partial_slope_screening_support",
            "causal_credibility_summary": (
                "Quasi-experimental evidence from Germany, the Netherlands, and Australia "
                "supports a fertility-relevant grandparental-childcare channel, but the "
                "effects use distinct treatment scales and should not be pooled with Cell A."
            ),
            "transition_classification_basis": _transition_basis(
                sdt_cell_c_rows, transition_by_study
            ),
            "needs_human_review": _any_needs_human_review(
                sdt_cell_c_rows, transition_by_study
            ),
            "rationale": (
                "All extracted Cell C studies are below-replacement rich-country settings. "
                "Their signs indicate that greater grandparent availability raises fertility, "
                "or that delayed retirement lowers it, matching the PI-identified SDT channel."
            ),
            "next_required_step": "Use the Cell C slope-sufficiency table for chapter language; finalize GRADE and RA readability review.",
        },
    ]
    write_csv(output_path, rows, DEMOGRAPHIC_SIGNIFICANCE_COLUMNS)


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
    outcome_pooled_path = tables_dir / f"{SLUG}-outcome-specific-pooled-estimates.csv"
    sof_path = tables_dir / f"{SLUG}-summary-of-findings.csv"
    transition_path = tables_dir / f"{SLUG}-tfr-transition-classification.csv"
    demographic_significance_path = tables_dir / f"{SLUG}-demographic-significance.csv"
    cell_c_slope_path = tables_dir / f"{SLUG}-cell-c-slope-scaling.csv"
    cell_c_note_path = ROOT / "output" / f"{SLUG}-cell-c-slope-scaling.md"
    cell_c_sufficiency_path = tables_dir / f"{SLUG}-cell-c-slope-sufficiency.csv"
    cell_c_sufficiency_note_path = (
        ROOT / "output" / f"{SLUG}-cell-c-slope-sufficiency.md"
    )
    grade_verdicts_path = tables_dir / f"{SLUG}-grade-verdicts.csv"
    evidence_map_path = figures_dir / f"{SLUG}-evidence-map.csv"

    if effects_path.exists():
        make_effect_review_sheet(effects_path, review_path)
        rows = [harmonize_effect_row(row) for row in read_csv(effects_path)]
        write_csv(harmonized_path, rows, HARMONIZED_COLUMNS)
        write_meta_analysis_readiness(harmonized_path, readiness_path)
        write_meta_analysis_summary(harmonized_path, meta_summary_path)
        write_outcome_specific_pooled_estimates(harmonized_path, outcome_pooled_path)
        write_cell_c_slope_scaling(harmonized_path, cell_c_slope_path, cell_c_note_path)
        write_grade_verdicts(grade_verdicts_path)
        if transition_path.exists():
            write_cell_c_slope_sufficiency(
                cell_c_slope_path,
                transition_path,
                cell_c_sufficiency_path,
                cell_c_sufficiency_note_path,
            )
            write_demographic_significance(
                harmonized_path,
                readiness_path,
                transition_path,
                demographic_significance_path,
            )
        write_summary_of_findings(meta_summary_path, sof_path, outcome_pooled_path)
        write_evidence_map(harmonized_path, evidence_map_path)


if __name__ == "__main__":
    main()
