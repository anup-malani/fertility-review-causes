import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from oas_transition_classification import (
    classify_replacement_window,
    nearest_tfr_in_window,
    write_transition_classification,
)


class OASTransitionClassificationTests(unittest.TestCase):
    def test_classifies_above_replacement_window_as_fdt(self):
        result = classify_replacement_window(5.2, 3.4, primary_outcome_family="fertility")
        self.assertEqual(result["replacement_status_start"], "above_replacement")
        self.assertEqual(result["replacement_status_end"], "above_replacement")
        self.assertEqual(result["derived_period_target_relevance_tfr"], "FDT")

    def test_classifies_below_replacement_window_as_sdt(self):
        result = classify_replacement_window(1.3, 1.4, primary_outcome_family="fertility")
        self.assertEqual(result["replacement_status_start"], "below_replacement")
        self.assertEqual(result["replacement_status_end"], "below_replacement")
        self.assertEqual(result["derived_period_target_relevance_tfr"], "SDT")

    def test_classifies_crossing_window_as_fdt_and_sdt(self):
        result = classify_replacement_window(3.9, 1.8, primary_outcome_family="fertility")
        self.assertEqual(result["replacement_status_start"], "above_replacement")
        self.assertEqual(result["replacement_status_end"], "below_replacement")
        self.assertEqual(result["derived_period_target_relevance_tfr"], "FDT|SDT")

    def test_flags_missing_tfr_without_guessing(self):
        result = classify_replacement_window(None, None, primary_outcome_family="fertility")
        self.assertEqual(result["replacement_status_start"], "missing_tfr")
        self.assertEqual(result["replacement_status_end"], "missing_tfr")
        self.assertEqual(result["derived_period_target_relevance_tfr"], "unclassified_no_tfr")

    def test_non_fertility_outcome_is_contextual(self):
        result = classify_replacement_window(1.6, 1.5, primary_outcome_family="non_fertility")
        self.assertEqual(result["derived_period_target_relevance_tfr"], "SDT_contextual")

    def test_nearest_tfr_stays_inside_window_when_available(self):
        tfr = {("Italy", 1998): 1.2, ("Italy", 2004): 1.34, ("Italy", 2010): 1.44}
        self.assertEqual(nearest_tfr_in_window(tfr, "Italy", 1998, 2004, prefer="start"), (1998, 1.2))
        self.assertEqual(nearest_tfr_in_window(tfr, "Italy", 1998, 2004, prefer="end"), (2004, 1.34))

    def test_write_transition_classification_uses_tfr_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "target.csv"
            output_path = tmp_path / "out.csv"
            rows = [
                {
                    "study_id": "s_brazil",
                    "country_or_region": "Brazil",
                    "period_start": "1981",
                    "period_end": "2014",
                    "primary_outcome_family": "fertility",
                },
                {
                    "study_id": "s_historical",
                    "country_or_region": "Prussia",
                    "period_start": "1881",
                    "period_end": "1910",
                    "primary_outcome_family": "fertility",
                },
            ]
            with input_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)

            tfr = {
                ("Brazil", 1981): 3.9,
                ("Brazil", 2014): 1.8,
            }
            write_transition_classification(input_path, output_path, tfr)

            with output_path.open(newline="", encoding="utf-8") as handle:
                out = list(csv.DictReader(handle))
            self.assertEqual(out[0]["study_id"], "s_brazil")
            self.assertEqual(out[0]["tfr_start"], "3.9")
            self.assertEqual(out[0]["tfr_end"], "1.8")
            self.assertEqual(out[0]["derived_period_target_relevance_tfr"], "FDT|SDT")
            self.assertEqual(out[1]["derived_period_target_relevance_tfr"], "unclassified_no_tfr")
            self.assertEqual(out[1]["needs_human_review"], "yes")


if __name__ == "__main__":
    unittest.main()
