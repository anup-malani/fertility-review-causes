#!/usr/bin/env python3
"""Unit tests for the B.1 demographic-significance pass.

Fixtures are hand-built windows rather than the real extraction, so the window arithmetic is
checked against cases worked out by hand and not against the code's own output. The FDT timing
test is the load-bearing one: TICK-036 requires that argument to come from dates, so a
regression that silently dated a study into the transition window has to fail here.
"""

import unittest

import b1_demographic_significance as d


class TestWindowOverlap(unittest.TestCase):
    def test_overlap_inclusive_at_both_edges(self):
        self.assertTrue(d.overlaps(1960, 1970, d.FDT_START, d.FDT_END))
        self.assertTrue(d.overlaps(1965, 1965, d.FDT_START, d.FDT_END))
        self.assertTrue(d.overlaps(1870, 1870, d.FDT_START, d.FDT_END))

    def test_no_overlap_outside_window(self):
        self.assertFalse(d.overlaps(1966, 2014, d.FDT_START, d.FDT_END))
        self.assertFalse(d.overlaps(1800, 1869, d.FDT_START, d.FDT_END))

    def test_undated_windows_never_match(self):
        self.assertFalse(d.overlaps(None, None, d.FDT_START, d.FDT_END))
        self.assertFalse(d.overlaps(1900, None, d.FDT_START, d.FDT_END))
        self.assertFalse(d.overlaps(None, 1900, d.FDT_START, d.FDT_END))


class TestClassifyWindow(unittest.TestCase):
    def test_post_1965_is_sdt(self):
        row = {"period_start": "1979", "period_end": "2010"}
        self.assertEqual(d.classify_window(row), "SDT")

    def test_window_spanning_the_close_of_the_fdt_gets_both(self):
        row = {"period_start": "1950", "period_end": "1990"}
        self.assertEqual(d.classify_window(row), "FDT|SDT")

    def test_pre_1870_window_is_pm(self):
        row = {"period_start": "1750", "period_end": "1800"}
        self.assertEqual(d.classify_window(row), "PM")

    def test_undated_row_falls_back_to_the_recorded_assignment(self):
        row = {
            "period_start": "",
            "period_end": "",
            "derived_period_target_relevance": "PM_analog_by_regime",
        }
        self.assertEqual(d.classify_window(row), "PM_analog_by_regime")

    def test_undated_row_with_no_recorded_assignment_is_unclassified(self):
        self.assertEqual(
            d.classify_window({"period_start": "", "period_end": ""}),
            "unclassified_no_window",
        )


class TestFdtTiming(unittest.TestCase):
    def test_counts_dated_undated_and_in_window(self):
        rows = [
            {"period_start": "1979", "period_end": "2010"},
            {"period_start": "2014", "period_end": "2014"},
            {"period_start": "", "period_end": ""},
        ]
        got = d.fdt_timing_evidence(rows)
        self.assertEqual(got["n_dated"], 2)
        self.assertEqual(got["n_undated"], 1)
        self.assertEqual(got["n_in_fdt"], 0)
        self.assertEqual(got["earliest_start"], 1979)

    def test_a_study_inside_the_transition_is_counted(self):
        rows = [
            {"period_start": "1900", "period_end": "1930"},
            {"period_start": "1979", "period_end": "2010"},
        ]
        got = d.fdt_timing_evidence(rows)
        self.assertEqual(got["n_in_fdt"], 1)
        self.assertEqual(got["earliest_start"], 1900)

    def test_real_extraction_has_no_study_inside_the_transition(self):
        """The chapter's timing claim, checked against the committed extraction."""
        got = d.fdt_timing_evidence(d.read_csv(d.TARGET_PERIODS))
        self.assertEqual(got["n_in_fdt"], 0)
        self.assertGreaterEqual(got["earliest_start"], d.SDT_START)


class TestVarianceExplained(unittest.TestCase):
    def test_r_squared_as_percent(self):
        # 0.0854^2 = 0.00729... -> 0.73 percent
        self.assertEqual(d._variance_explained({"pooled_r": "0.0854"}), "0.73")
        # -0.1275^2 = 0.01625... -> 1.63 percent
        self.assertEqual(d._variance_explained({"pooled_r": "-0.1275"}), "1.63")

    def test_unpooled_group_yields_empty(self):
        self.assertEqual(d._variance_explained({"pooled_r": ""}), "")
        self.assertEqual(d._variance_explained(None), "")


class TestDistinctiveClaimNeverGetsAShare(unittest.TestCase):
    """TICK-036 acceptance criterion: the distinctive claim is unidentified, not scored."""

    def test_distinctive_row_is_unidentified_and_empty(self):
        sig_rows, grade_rows, _ = d.run()
        row = next(
            r for r in sig_rows if r["phenomenon_channel"] == "SDT_distinctive_decoupling"
        )
        self.assertEqual(row["n_studies"], 0)
        self.assertEqual(row["pooled_estimate"], "unidentified")
        self.assertEqual(row["variance_explained_pct"], "")
        self.assertIn("unidentified", row["demographic_significance_verdict"])

    def test_grade_table_channels_match_significance_table(self):
        sig_rows, grade_rows, _ = d.run()
        self.assertEqual(
            [r["phenomenon_channel"] for r in sig_rows],
            [r["phenomenon_channel"] for r in grade_rows],
        )


class TestTfrCrossCheckIsHonest(unittest.TestCase):
    def test_reports_a_status_either_way(self):
        got = d.tfr_cross_check()
        self.assertIn(got["status"], {"available", "unavailable"})
        self.assertTrue(got["detail"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
