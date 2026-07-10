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
        self.assertIn("effect_original_ra_notes", columns)
        self.assertIn("extract_page_ra_decision", columns)
        self.assertIn("extract_page_ra_notes", columns)
        self.assertNotIn("pdf_filename_ra_decision", columns)
        self.assertNotIn("pdf_filename_ra_notes", columns)

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
                    "effect_original_ra_notes": "Use table 2 estimate.",
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
            self.assertEqual(rows[0]["effect_original_ra_notes"], "Use table 2 estimate.")

    def test_harmonize_percentage_points(self):
        row = {
            "effect_id": "e1",
            "outcome_family": "birth_probability",
            "outcome_unit_original": "percentage_points",
            "effect_original": "-12",
            "se_original": "3",
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
            "requires_treatment_scale_followup_and_sign_orientation_before_pooling",
        )

    def test_cell_a_birth_probability_rows_without_compatibility_metadata_do_not_pool(self):
        rows = [
            {
                "effect_id": "e1",
                "outcome_family": "birth_probability",
                "outcome_unit_original": "percentage_points",
                "effect_original": "-0.9",
                "se_original": "0.3",
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
            {"requires_treatment_scale_followup_and_sign_orientation_before_pooling"},
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
            "requires_treatment_scale_followup_and_sign_orientation_before_pooling",
        )


if __name__ == "__main__":
    unittest.main()
