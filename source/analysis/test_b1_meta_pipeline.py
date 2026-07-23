#!/usr/bin/env python3
"""Unit tests for the B.1 status-fertility meta-analysis pipeline.

The random-effects fixtures use hand-computable inputs so the DerSimonian-Laird math is checked
against values worked out by hand, not against the code's own output.
"""
import math
import unittest

import b1_meta_pipeline as m


class TestHarmonization(unittest.TestCase):
    def test_fisher_z_roundtrip(self):
        for r in (-0.8, -0.1, 0.0, 0.19, 0.5, 0.9):
            self.assertAlmostEqual(m.inv_fisher_z(m.fisher_z(r)), r, places=10)

    def test_fisher_z_value(self):
        # atanh(0.5) = 0.5*ln(3) = 0.549306
        self.assertAlmostEqual(m.fisher_z(0.5), 0.5493061443, places=8)

    def test_zr_row_from_ci(self):
        # von Rueden: Zr = 0.19, 95% CI [0.09, 0.31]; SE = (0.31-0.09)/(2*1.96)
        z, var = m.z_and_var({"effect_type": "zr", "effect_value": "0.19",
                              "ci_lower": "0.09", "ci_upper": "0.31"})
        self.assertAlmostEqual(z, 0.19, places=10)
        self.assertAlmostEqual(math.sqrt(var), (0.31 - 0.09) / (2 * m.Z95), places=8)

    def test_r_row_from_n(self):
        # Pearson r=0.30, n=103 -> z=atanh(.3), var=1/100
        z, var = m.z_and_var({"effect_type": "r", "effect_value": "0.30", "n": "103"})
        self.assertAlmostEqual(z, math.atanh(0.30), places=10)
        self.assertAlmostEqual(var, 1.0 / 100, places=10)

    def test_unusable_returns_none(self):
        self.assertIsNone(m.z_and_var({"effect_type": "beta", "effect_value": "0.4"}))
        self.assertIsNone(m.z_and_var({"effect_type": "zr", "effect_value": ""}))
        self.assertIsNone(m.z_and_var({"effect_type": "r", "effect_value": "0.3"}))  # no n or CI


class TestDerSimonianLaird(unittest.TestCase):
    def test_known_two_study_pool(self):
        # z=[0.2,0.4], v=[0.01,0.01]. Hand-computed: mean_fixed=0.3, Q=2.0, df=1,
        # C=200-20000/200=100, tau2=(2-1)/100=0.01, w*=50 each, pooled=0.3, se=0.1, I2=50%.
        res = m.dersimonian_laird([0.2, 0.4], [0.01, 0.01])
        self.assertAlmostEqual(res["Q"], 2.0, places=10)
        self.assertAlmostEqual(res["tau2"], 0.01, places=10)
        self.assertAlmostEqual(res["pooled_z"], 0.3, places=10)
        self.assertAlmostEqual(res["se_z"], 0.1, places=10)
        self.assertAlmostEqual(res["I2_pct"], 50.0, places=8)
        self.assertAlmostEqual(res["pooled_r"], math.tanh(0.3), places=10)

    def test_homogeneous_has_zero_tau2(self):
        # identical effects -> Q=0 -> tau2=0, pooled equals the common effect
        res = m.dersimonian_laird([0.25, 0.25, 0.25], [0.02, 0.02, 0.02])
        self.assertAlmostEqual(res["tau2"], 0.0, places=12)
        self.assertAlmostEqual(res["I2_pct"], 0.0, places=12)
        self.assertAlmostEqual(res["pooled_z"], 0.25, places=10)


class TestConservativeRule(unittest.TestCase):
    def test_below_min_studies_not_pooled(self):
        rows = [{"study_id": "A", "_z": 0.2, "_var": 0.01},
                {"study_id": "B", "_z": 0.3, "_var": 0.01}]
        out = m.pool_group(rows, "overall")
        self.assertIn("insufficient", out["status"])
        self.assertEqual(out["pooled_r"], "")

    def test_distinct_studies_counted_not_effects(self):
        # three effects but only two distinct studies -> still insufficient
        rows = [{"study_id": "A", "_z": 0.2, "_var": 0.01},
                {"study_id": "A", "_z": 0.25, "_var": 0.01},
                {"study_id": "B", "_z": 0.3, "_var": 0.01}]
        out = m.pool_group(rows, "overall")
        self.assertEqual(out["k_studies"], 2)
        self.assertIn("insufficient", out["status"])

    def test_three_studies_pools(self):
        rows = [{"study_id": s, "_z": 0.2, "_var": 0.01} for s in ("A", "B", "C")]
        out = m.pool_group(rows, "overall")
        self.assertEqual(out["status"], "pooled")
        self.assertEqual(out["k_studies"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
