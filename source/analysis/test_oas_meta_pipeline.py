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
        self.assertEqual(out["meta_analysis_group"], "cell_a_birth_probability")

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
        self.assertIn("missing_standard_error", out["poolability_reason"])


if __name__ == "__main__":
    unittest.main()
