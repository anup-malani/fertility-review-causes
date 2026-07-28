#!/usr/bin/env python3
"""Tests for d3b_demographic_significance.

The load-bearing assertions are that the pipeline cannot silently produce a FAVOURABLE
verdict or a POINT estimate of demographic share. Both are the failure modes that matter
when the underlying evidence is thin and the temptation is to round toward a finding.
"""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "ds", Path(__file__).resolve().parent / "d3b_demographic_significance.py")
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)


def eff(sid, direction="negative", poolable="no", exclude="no", wall1="ecological_fear",
        etype="hazard_ratio"):
    return {"study_id": sid, "direction": direction, "poolable": poolable,
            "exclude": exclude, "wall1_class": wall1, "effect_type": etype}


def rob(sid, track="realized", overall="serious"):
    return {"study_id": sid, "track": track, "overall": overall}


class TestNoPrePremodernOrFDTCell(unittest.TestCase):
    def test_premodern_and_fdt_are_not_applicable(self):
        rows = {r["phenomenon"]: r for r in ds.demographic_rows()}
        self.assertEqual(rows["pre_modern"]["applicable"], "no")
        self.assertEqual(rows["FDT"]["applicable"], "no")
        self.assertEqual(rows["pre_modern"]["share_of_decline"], "not applicable")

    def test_no_fabricated_share_for_inapplicable_cells(self):
        for r in ds.demographic_rows():
            if r["applicable"] == "no":
                self.assertNotIn("%", r["share_of_decline"])


class TestSharesAreNotPointEstimates(unittest.TestCase):
    def test_realized_share_is_a_bound_with_a_zero_floor(self):
        row = {r["phenomenon"]: r for r in ds.demographic_rows()}["SDT_realized_fertility"]
        self.assertIn("0 to", row["share_of_decline"])
        self.assertIn("ILLUSTRATIVE BOUND", row["share_of_decline"])
        self.assertEqual(row["needs_human_review"], "yes")

    def test_realized_basis_names_the_post1970_null(self):
        row = {r["phenomenon"]: r for r in ds.demographic_rows()}["SDT_realized_fertility"]
        self.assertIn("0.98", row["basis"])
        self.assertIn("precise null", row["basis"])

    def test_stated_and_distinctive_cells_are_unidentified(self):
        rows = {r["phenomenon"]: r for r in ds.demographic_rows()}
        self.assertIn("NOT IDENTIFIED", rows["SDT_stated_intention"]["share_of_decline"])
        self.assertIn("UNIDENTIFIED", rows["SDT_desire_independence"]["share_of_decline"])


class TestGradeRealized(unittest.TestCase):
    def test_actual_evidence_yields_very_low(self):
        realized = [eff("golovina_2024_soep_worries", poolable="yes"),
                    eff("peters_2023_soep_reciprocal", direction="null", poolable="yes"),
                    eff("jylha_2025_swedish_ggs", direction="null"),
                    eff("weychert_2026_ukhls_news")]
        r = ds.grade_realized(realized, [rob("golovina_2024_soep_worries"),
                                         rob("jylha_2025_swedish_ggs", overall="moderate"),
                                         rob("peters_2023_soep_reciprocal", overall="moderate"),
                                         rob("weychert_2026_ukhls_news")])
        self.assertEqual(r["final_certainty"], "VERY LOW")
        self.assertEqual(r["independent_sources"], 3)
        self.assertGreaterEqual(r["downgrades"], 3)

    def test_shared_panel_collapses_independent_source_count(self):
        realized = [eff("golovina_2024_soep_worries"), eff("peters_2023_soep_reciprocal")]
        r = ds.grade_realized(realized, [rob("golovina_2024_soep_worries")])
        self.assertEqual(r["independent_sources"], 1)

    def test_imprecision_downgrade_always_cites_the_source_count(self):
        r = ds.grade_realized([eff("golovina_2024_soep_worries")], [rob("golovina_2024_soep_worries")])
        self.assertIn("independent data source", r["downgrade_reasons"])

    def test_excluded_rows_do_not_count_as_studies(self):
        realized = [eff("a"), eff("b", exclude="yes")]
        r = ds.grade_realized(realized, [rob("a")])
        self.assertEqual(r["studies"], 1)


class TestGradeStated(unittest.TestCase):
    def test_bleed_in_appears_in_the_indirectness_downgrade(self):
        stated = [eff("a", wall1="environmental_values_or_behaviour"),
                  eff("b", wall1="mixed"), eff("c")]
        r = ds.grade_stated(stated, [])
        self.assertIn("2 of 3", r["downgrade_reasons"])
        self.assertIn("environmental values", r["downgrade_reasons"])

    def test_stated_track_is_very_low(self):
        r = ds.grade_stated([eff("a")], [])
        self.assertEqual(r["final_certainty"], "VERY LOW")

    def test_stated_track_never_reports_poolable_rows(self):
        r = ds.grade_stated([eff("a", poolable="yes")], [])
        self.assertEqual(r["poolable_rows"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
