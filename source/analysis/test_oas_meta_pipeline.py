import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from oas_meta_pipeline import (
    EFFECT_REQUIRED_COLUMNS,
    REVIEW_FIELDS,
    harmonize_effect_row,
    make_effect_review_columns,
    make_effect_review_sheet,
    validate_required_columns,
    write_csv,
    write_demographic_significance,
    write_meta_analysis_readiness,
)


class OASMetaPipelineTests(unittest.TestCase):
    def test_validate_required_columns_rejects_missing_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "effects.csv"
            path.write_text("effect_id,study_id\nx,y\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing required columns"):
                validate_required_columns(path, EFFECT_REQUIRED_COLUMNS)

    def test_make_effect_review_columns_adds_decision_columns(self):
        columns = make_effect_review_columns()
        self.assertIn("pdf_filename", columns)
        self.assertIn("effect_original", columns)
        self.assertIn("effect_original_ra_decision", columns)
        self.assertIn("effect_original_source", columns)
        self.assertIn("extract_page_ra_decision", columns)
        self.assertIn("extract_page_source", columns)
        self.assertNotIn("pdf_filename_ra_decision", columns)
        self.assertNotIn("pdf_filename_source", columns)
        self.assertNotIn("effect_original_ra_notes", columns)

    def test_make_effect_review_sheet_preserves_existing_annotations(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            effects_path = tmp_path / "effects.csv"
            review_path = tmp_path / "review.csv"
            effect_row = {column: "" for column in EFFECT_REQUIRED_COLUMNS}
            effect_row.update(
            {
                "effect_id": "e1",
                "study_id": "s1",
                "pdf_filename": "study.pdf",
                "effect_original": "-12",
                "extract_page": "PDF page 12, Table 2",
                "test_statistic_original": "",
                "test_statistic_type": "",
            }
            )
            with effects_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=EFFECT_REQUIRED_COLUMNS)
                writer.writeheader()
                writer.writerow(effect_row)

            review_columns = make_effect_review_columns()
            review_row = {column: "" for column in review_columns}
            review_row.update(
                {
                    "effect_id": "e1",
                    "study_id": "s1",
                    "pdf_filename": "study.pdf",
                    "effect_original": "-10",
                    "effect_original_ra_decision": "FIX",
                }
            )
            with review_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=review_columns)
                writer.writeheader()
                writer.writerow(review_row)

            make_effect_review_sheet(effects_path, review_path)

            with review_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["effect_original"], "-12")
            self.assertEqual(rows[0]["effect_original_ra_decision"], "FIX")
            self.assertEqual(rows[0]["effect_original_source"], "PDF page 12, Table 2")
            self.assertNotIn("effect_original_ra_notes", rows[0])

    def test_harmonize_percentage_points(self):
        row = {
            "effect_id": "e1",
            "outcome_family": "birth_probability",
            "outcome_unit_original": "percentage_points",
            "effect_original": "-12",
            "se_original": "3",
            "test_statistic_original": "",
            "test_statistic_type": "",
            "mechanism_cell": "A",
            "needs_pi": "no",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["harmonized_outcome_unit"], "probability_of_birth")
        self.assertEqual(out["effect_harmonized"], "-0.12")
        self.assertEqual(out["se_harmonized"], "0.03")
        self.assertEqual(out["meta_analysis_group"], "not_poolable")
        self.assertEqual(
            out["poolability_reason"],
            "requires_treatment_scale_followup_target_setting_before_pooling",
        )

    def test_harmonize_derives_se_from_t_statistic(self):
        row = {
            "effect_id": "e1",
            "outcome_family": "birth_probability",
            "outcome_unit_original": "percentage_points",
            "effect_original": "4.0",
            "se_original": "",
            "test_statistic_original": "3.27",
            "test_statistic_type": "t_statistic",
            "mechanism_cell": "A",
            "needs_pi": "no",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["effect_harmonized"], "0.04")
        self.assertEqual(out["se_harmonized"], "0.01223242")
        self.assertEqual(
            out["harmonization_method"],
            "percentage_points_divided_by_100_se_derived_from_t_statistic",
        )

    def test_orients_pension_cut_as_more_old_age_security_effect(self):
        row = {
            "effect_id": "billari_galasso_2009_italy_pension_reforms_e01",
            "outcome_family": "birth_probability",
            "outcome_unit_original": "percentage_points",
            "effect_original": "0.664",
            "se_original": "0.286",
            "test_statistic_original": "",
            "test_statistic_type": "",
            "mechanism_cell": "A",
            "treatment_scale_original": "Affected by pension reform discontinuity",
            "followup_window": "+/- 7 years around contribution thresholds",
            "needs_pi": "yes",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["pi_approved"], "yes_assumed")
        self.assertEqual(out["old_age_security_treatment_direction"], "decrease_oas")
        self.assertEqual(out["effect_oriented_more_oas"], "-0.00664")
        self.assertEqual(out["se_oriented_more_oas"], "0.00286")
        self.assertEqual(out["orientation_method"], "sign_flipped_because_treatment_decreases_oas")

    def test_orients_pension_expansion_without_sign_flip(self):
        row = {
            "effect_id": "rossi_godard_2022_namibia_pensions_e01",
            "outcome_family": "birth_probability",
            "outcome_unit_original": "percentage_points",
            "effect_original": "-17.3",
            "se_original": "4.3",
            "test_statistic_original": "",
            "test_statistic_type": "",
            "mechanism_cell": "A",
            "treatment_scale_original": "Post x InitialNeeds in thousand rands",
            "followup_window": "Post pension extension",
            "needs_pi": "no",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["old_age_security_treatment_direction"], "increase_oas")
        self.assertEqual(out["effect_oriented_more_oas"], "-0.173")
        self.assertEqual(out["se_oriented_more_oas"], "0.043")
        self.assertEqual(out["orientation_method"], "as_reported_treatment_increases_oas")

    def test_cell_a_birth_probability_rows_without_compatibility_metadata_do_not_pool(self):
        rows = [
            {
                "effect_id": "e1",
                "outcome_family": "birth_probability",
                "outcome_unit_original": "percentage_points",
                "effect_original": "-0.9",
                "se_original": "0.3",
                "test_statistic_original": "",
                "test_statistic_type": "",
                "mechanism_cell": "A",
                "treatment_scale_original": "Rural pension reform exposure",
                "followup_window": "Short run after reform",
                "needs_pi": "no",
            },
            {
                "effect_id": "e2",
                "outcome_family": "birth_probability",
                "outcome_unit_original": "percentage_points",
                "effect_original": "-17.3",
                "se_original": "4.3",
                "test_statistic_original": "",
                "test_statistic_type": "",
                "mechanism_cell": "A",
                "treatment_scale_original": "Post x InitialNeeds",
                "followup_window": "Post pension extension",
                "needs_pi": "no",
            },
            {
                "effect_id": "e3",
                "outcome_family": "birth_probability",
                "outcome_unit_original": "percentage_points",
                "effect_original": "0.664",
                "se_original": "0.286",
                "mechanism_cell": "A",
                "treatment_scale_original": "Pension-cut reform discontinuity",
                "followup_window": "+/- 7 years around thresholds",
                "needs_pi": "no",
            },
        ]

        outputs = [harmonize_effect_row(row) for row in rows]

        self.assertTrue(all(row["effect_harmonized"] for row in outputs))
        self.assertTrue(all(row["se_harmonized"] for row in outputs))
        self.assertEqual(
            {row["meta_analysis_group"] for row in outputs}, {"not_poolable"}
        )
        self.assertEqual(
            {
                row["poolability_reason"]
                for row in outputs
            },
            {"requires_treatment_scale_followup_target_setting_before_pooling"},
        )

    def test_harmonize_non_poolable_completed_fertility_without_se(self):
        row = {
            "effect_id": "e2",
            "outcome_family": "completed_fertility",
            "outcome_unit_original": "births_per_woman",
            "effect_original": "-1.3",
            "se_original": "",
            "mechanism_cell": "A",
            "needs_pi": "no",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["harmonized_outcome_unit"], "births_per_woman")
        self.assertEqual(out["effect_harmonized"], "-1.3")
        self.assertEqual(out["meta_analysis_group"], "not_poolable")
        self.assertEqual(
            out["poolability_reason"],
            "requires_treatment_scale_followup_target_setting_before_pooling",
        )

    def test_meta_analysis_readiness_reports_screening_only_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            harmonized_path = tmp_path / "harmonized.csv"
            readiness_path = tmp_path / "readiness.csv"
            rows = [
                {
                    "effect_id": "e1",
                    "study_id": "s1",
                    "mechanism_cell": "A",
                    "outcome_family": "birth_probability",
                    "harmonized_outcome_unit": "probability_of_birth",
                    "effect_harmonized": "-0.10",
                    "se_harmonized": "0.05",
                    "effect_oriented_more_oas": "-0.10",
                    "se_oriented_more_oas": "0.05",
                    "old_age_security_treatment_direction": "increase_oas",
                    "treatment_scale_harmonized": "pension_expansion_binary_exposure",
                    "is_primary_estimate": "yes",
                    "pi_approved": "yes_assumed",
                    "needs_pi": "no",
                    "poolability_reason": (
                        "requires_treatment_scale_followup_target_setting_before_pooling"
                    ),
                },
                {
                    "effect_id": "e2",
                    "study_id": "s2",
                    "mechanism_cell": "A",
                    "outcome_family": "birth_probability",
                    "harmonized_outcome_unit": "probability_of_birth",
                    "effect_harmonized": "-0.20",
                    "se_harmonized": "0.05",
                    "effect_oriented_more_oas": "-0.20",
                    "se_oriented_more_oas": "0.05",
                    "old_age_security_treatment_direction": "increase_oas",
                    "treatment_scale_harmonized": "pension_value_continuous_exposure",
                    "is_primary_estimate": "yes",
                    "pi_approved": "yes_assumed",
                    "needs_pi": "no",
                    "poolability_reason": (
                        "requires_treatment_scale_followup_target_setting_before_pooling"
                    ),
                },
                {
                    "effect_id": "e3",
                    "study_id": "s3",
                    "mechanism_cell": "A",
                    "outcome_family": "birth_probability",
                    "harmonized_outcome_unit": "probability_of_birth",
                    "effect_harmonized": "0.00",
                    "se_harmonized": "0.10",
                    "effect_oriented_more_oas": "0.00",
                    "se_oriented_more_oas": "0.10",
                    "old_age_security_treatment_direction": "increase_oas",
                    "treatment_scale_harmonized": "ltci_pilot_binary_exposure",
                    "is_primary_estimate": "no",
                    "pi_approved": "yes_assumed",
                    "needs_pi": "yes",
                    "poolability_reason": (
                        "requires_treatment_scale_followup_target_setting_before_pooling"
                    ),
                },
            ]
            write_csv(harmonized_path, rows, list(rows[0].keys()))
            write_meta_analysis_readiness(harmonized_path, readiness_path)

            with readiness_path.open(newline="", encoding="utf-8") as handle:
                readiness_rows = list(csv.DictReader(handle))
            self.assertEqual(len(readiness_rows), 1)
            row = readiness_rows[0]
            self.assertEqual(row["n_effects"], "3")
            self.assertEqual(row["n_studies"], "3")
            self.assertEqual(row["n_with_harmonized_se"], "3")
            self.assertEqual(row["n_unresolved_needs_pi"], "0")
            self.assertEqual(row["n_pi_approved_assumed"], "3")
            self.assertEqual(row["n_negative"], "2")
            self.assertEqual(row["n_zero"], "1")
            self.assertEqual(row["n_with_oriented_effect"], "3")
            self.assertEqual(row["n_oriented_negative"], "2")
            self.assertEqual(row["n_oriented_zero"], "1")
            self.assertEqual(row["screening_fixed_effect"], "-0.133333")
            self.assertEqual(row["oriented_screening_fixed_effect"], "-0.133333")
            self.assertEqual(row["synthesis_decision"], "screening_only_not_pooled")
            self.assertEqual(
                row["primary_pooling_blocker"],
                "treatment_scale_followup_target_setting",
            )
            self.assertEqual(row["recommended_synthesis"], "do_not_pool_mixed_treatment_scales")
            self.assertEqual(row["recommended_pooled_effect_more_oas"], "")

    def test_readiness_recommends_pooling_same_treatment_scale_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            harmonized_path = tmp_path / "harmonized.csv"
            readiness_path = tmp_path / "readiness.csv"
            rows = [
                {
                    "effect_id": "e1",
                    "study_id": "s1",
                    "mechanism_cell": "A",
                    "outcome_family": "birth_probability",
                    "harmonized_outcome_unit": "probability_of_birth",
                    "old_age_security_treatment_direction": "increase_oas",
                    "treatment_scale_harmonized": "pension_expansion_binary_exposure",
                    "effect_harmonized": "-0.10",
                    "se_harmonized": "0.05",
                    "effect_oriented_more_oas": "-0.10",
                    "se_oriented_more_oas": "0.05",
                    "is_primary_estimate": "yes",
                    "pi_approved": "yes_assumed",
                    "needs_pi": "no",
                    "poolability_reason": (
                        "requires_treatment_scale_followup_target_setting_before_pooling"
                    ),
                },
                {
                    "effect_id": "e2",
                    "study_id": "s2",
                    "mechanism_cell": "A",
                    "outcome_family": "birth_probability",
                    "harmonized_outcome_unit": "probability_of_birth",
                    "old_age_security_treatment_direction": "increase_oas",
                    "treatment_scale_harmonized": "pension_expansion_binary_exposure",
                    "effect_harmonized": "-0.20",
                    "se_harmonized": "0.05",
                    "effect_oriented_more_oas": "-0.20",
                    "se_oriented_more_oas": "0.05",
                    "is_primary_estimate": "yes",
                    "pi_approved": "yes_assumed",
                    "needs_pi": "no",
                    "poolability_reason": (
                        "requires_treatment_scale_followup_target_setting_before_pooling"
                    ),
                },
                {
                    "effect_id": "e3",
                    "study_id": "s3",
                    "mechanism_cell": "A",
                    "outcome_family": "birth_probability",
                    "harmonized_outcome_unit": "probability_of_birth",
                    "old_age_security_treatment_direction": "increase_oas",
                    "treatment_scale_harmonized": "pension_expansion_binary_exposure",
                    "effect_harmonized": "0.00",
                    "se_harmonized": "0.10",
                    "effect_oriented_more_oas": "0.00",
                    "se_oriented_more_oas": "0.10",
                    "is_primary_estimate": "yes",
                    "pi_approved": "yes_assumed",
                    "needs_pi": "no",
                    "poolability_reason": (
                        "requires_treatment_scale_followup_target_setting_before_pooling"
                    ),
                },
            ]
            write_csv(harmonized_path, rows, list(rows[0].keys()))
            write_meta_analysis_readiness(harmonized_path, readiness_path)

            with readiness_path.open(newline="", encoding="utf-8") as handle:
                readiness_rows = list(csv.DictReader(handle))
            row = readiness_rows[0]
            self.assertEqual(row["recommended_synthesis"], "pool_fixed_effect_same_scale")
            self.assertEqual(row["recommended_pooled_effect_more_oas"], "-0.133333")
            self.assertEqual(row["recommended_pooled_se_more_oas"], "0.033333")

    def test_write_demographic_significance_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            harmonized_path = tmp_path / "harmonized.csv"
            readiness_path = tmp_path / "readiness.csv"
            transition_path = tmp_path / "transition.csv"
            output_path = tmp_path / "demographic.csv"

            harmonized_rows = [
                {
                    "study_id": "fdt_study",
                    "mechanism_cell": "A",
                    "effect_oriented_more_oas": "-0.10",
                    "se_oriented_more_oas": "0.05",
                },
                {
                    "study_id": "sdt_study",
                    "mechanism_cell": "A",
                    "effect_oriented_more_oas": "-0.20",
                    "se_oriented_more_oas": "0.05",
                },
                {
                    "study_id": "mechanism_study",
                    "mechanism_cell": "B",
                    "effect_oriented_more_oas": "",
                    "se_oriented_more_oas": "",
                },
            ]
            readiness_rows = [
                {
                    "analysis_group": "g_birth",
                    "recommended_synthesis": "do_not_pool_mixed_treatment_scales",
                }
            ]
            transition_rows = [
                {
                    "study_id": "fdt_study",
                    "derived_period_target_relevance_tfr": "FDT",
                    "needs_human_review": "no",
                },
                {
                    "study_id": "sdt_study",
                    "derived_period_target_relevance_tfr": "SDT",
                    "needs_human_review": "yes",
                },
                {
                    "study_id": "mechanism_study",
                    "derived_period_target_relevance_tfr": "SDT_contextual",
                    "needs_human_review": "yes",
                },
            ]
            write_csv(harmonized_path, harmonized_rows, list(harmonized_rows[0].keys()))
            write_csv(readiness_path, readiness_rows, list(readiness_rows[0].keys()))
            write_csv(transition_path, transition_rows, list(transition_rows[0].keys()))

            write_demographic_significance(
                harmonized_path, readiness_path, transition_path, output_path
            )

            with output_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            by_key = {row["phenomenon_channel"]: row for row in rows}
            self.assertEqual(
                set(by_key),
                {"PM", "FDT", "SDT_classic_oas", "SDT_grandparental_childcare"},
            )
            self.assertEqual(by_key["FDT"]["n_cell_a_studies"], "1")
            self.assertEqual(by_key["FDT"]["oriented_effect_direction"], "negative")
            self.assertEqual(by_key["FDT"]["demographic_significance_verdict"], "partial")
            self.assertEqual(by_key["SDT_classic_oas"]["n_cell_a_studies"], "1")
            self.assertEqual(by_key["SDT_classic_oas"]["needs_human_review"], "yes")
            self.assertEqual(
                by_key["SDT_grandparental_childcare"]["demographic_significance_verdict"],
                "insufficient_data_pending_cell_c_extraction",
            )


if __name__ == "__main__":
    unittest.main()
