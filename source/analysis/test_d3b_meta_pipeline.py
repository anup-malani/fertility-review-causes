#!/usr/bin/env python3
"""Tests for d3b_meta_pipeline.

The tests that matter here are the ones asserting the pipeline REFUSES to pool when the
conservative rule is not met. A synthesis pipeline that pools whenever it has rows is the
failure mode this script exists to prevent, so the refusal path is tested harder than the
happy path.
"""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "d3b", Path(__file__).resolve().parent / "d3b_meta_pipeline.py")
d3b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d3b)


def row(sid, eff="0.90", lo="0.80", hi="1.00", metric="hazard_ratio",
        poolable="yes", exclude="no", primary="yes"):
    return {"study_id": sid, "effect_value": eff, "ci_lower": lo, "ci_upper": hi,
            "effect_type": metric, "poolable": poolable, "exclude": exclude,
            "is_primary_estimate": primary, "effect_id": sid + "_1",
            "sample": "Total", "model": "m", "significant": "no",
            "adjusts_politics": "no", "predictor_wall1_class": "ecological_fear"}


class TestIndependence(unittest.TestCase):
    def test_shared_data_source_collapses_to_one_unit(self):
        units = d3b.independent_units(
            {"golovina_2024_soep_worries", "peters_2023_soep_reciprocal"})
        self.assertEqual(units, {"GSOEP"})

    def test_distinct_sources_stay_distinct(self):
        units = d3b.independent_units(
            {"golovina_2024_soep_worries", "jylha_2025_swedish_ggs", "weychert_2026_ukhls_news"})
        self.assertEqual(len(units), 3)

    def test_unknown_study_is_its_own_unit(self):
        self.assertEqual(d3b.independent_units({"some_new_study"}), {"some_new_study"})


class TestPoolingRefusal(unittest.TestCase):
    def test_two_studies_one_panel_is_refused(self):
        """The actual D.3.b situation: 2 studies, 1 data source."""
        d = d3b.assess_pooling(
            [row("golovina_2024_soep_worries"), row("peters_2023_soep_reciprocal")], "realized")
        self.assertEqual(d["pool_permitted"], "no")
        self.assertEqual(d["independent_units"], 1)
        self.assertIn("independent data source", d["reasons_withheld"])
        self.assertIn("GSOEP", d["reasons_withheld"])
        self.assertIn("NOT a pooled estimate", d["output_type"])

    def test_three_studies_sharing_one_panel_still_refused(self):
        """Row count is not the test -- independence is."""
        rows = [row("golovina_2024_soep_worries"), row("peters_2023_soep_reciprocal"),
                row("jylha_2025_swedish_ggs")]
        d = d3b.assess_pooling(rows, "realized")
        self.assertEqual(d["independent_units"], 2)
        self.assertEqual(d["pool_permitted"], "no")

    def test_mixed_metrics_refused_even_with_enough_sources(self):
        rows = [row("a"), row("b"), row("c", metric="unstandardized_b")]
        d = d3b.assess_pooling(rows, "realized")
        self.assertEqual(d["pool_permitted"], "no")
        self.assertIn("not harmonised", d["reasons_withheld"])

    def test_missing_ci_refused(self):
        rows = [row("a"), row("b"), row("c", lo="NR", hi="NR")]
        d = d3b.assess_pooling(rows, "realized")
        self.assertEqual(d["pool_permitted"], "no")
        self.assertIn("no reported CI", d["reasons_withheld"])

    def test_three_independent_harmonised_studies_permitted(self):
        d = d3b.assess_pooling([row("a"), row("b"), row("c")], "realized")
        self.assertEqual(d["pool_permitted"], "yes")
        self.assertEqual(d["reasons_withheld"], "")
        self.assertEqual(d["output_type"], "random-effects pool")


class TestRowSelection(unittest.TestCase):
    def test_excluded_and_nonpoolable_rows_dropped(self):
        rows = [row("a"), row("b", poolable="no"), row("c", exclude="yes")]
        self.assertEqual({r["study_id"] for r in d3b.primary_poolable(rows)}, {"a"})

    def test_one_estimate_per_study(self):
        """Three estimates from one study must not count as three."""
        rows = [row("a", primary="no"), row("a", primary="yes"), row("a", primary="no")]
        picked = d3b.primary_poolable(rows)
        self.assertEqual(len(picked), 1)
        self.assertEqual(picked[0]["is_primary_estimate"], "yes")


class TestHazardConversion(unittest.TestCase):
    def test_log_hr_and_se(self):
        lg, se = d3b.hr_to_log({"effect_value": "0.82", "ci_lower": "0.75", "ci_upper": "0.90"})
        self.assertAlmostEqual(lg, -0.19845, places=4)
        self.assertGreater(se, 0)

    def test_non_numeric_returns_none(self):
        self.assertIsNone(d3b.hr_to_log(
            {"effect_value": "NOT_SIGNIFICANT", "ci_lower": "NR", "ci_upper": "NR"}))

    def test_nonpositive_returns_none(self):
        self.assertIsNone(d3b.hr_to_log(
            {"effect_value": "0", "ci_lower": "0", "ci_upper": "1"}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
