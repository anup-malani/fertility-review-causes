#!/usr/bin/env python3
"""Tests for b5_demographic_significance.py.

The properties tested are the ones the chapter's argument rests on. If any fails, the chapter's
central quantitative claim is wrong, not merely imprecise.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b5_demographic_significance as m


class TestBirthIntervalModel(unittest.TestCase):

    def test_zero_loss_adds_no_time(self):
        self.assertEqual(m.time_added(0.0, 3.0, 1.5, 5.0), 0.0)

    def test_time_added_increases_in_loss_rate(self):
        prev = -1.0
        for p in (0.05, 0.10, 0.20, 0.30, 0.40):
            ta = m.time_added(p, 3.0, 1.5, 5.0)
            self.assertGreater(ta, prev)
            prev = ta

    def test_expected_losses_per_live_birth_is_odds_not_probability(self):
        """p/(1-p), not p. At p=0.5 a woman expects one loss per live birth, not half of one."""
        self.assertAlmostEqual(m.time_added(0.5, 2.0, 1.0, 3.0), 6.0)

    def test_loss_rate_at_or_above_one_is_rejected(self):
        with self.assertRaises(ValueError):
            m.time_added(1.0, 3.0, 1.5, 5.0)

    def test_births_fall_as_loss_rises(self):
        hi = m.births_span_binding(0.10, 12.0, 5.0, 3.0, 1.5, 240.0)
        lo = m.births_span_binding(0.30, 12.0, 5.0, 3.0, 1.5, 240.0)
        self.assertGreater(hi, lo)

    def test_birth_interval_components_are_additive(self):
        bi = m.birth_interval(0.0, 12.0, 5.0, 3.0, 1.5)
        self.assertAlmostEqual(bi, 12.0 + 5.0 + m.GESTATION)


class TestEstimandLevels(unittest.TestCase):

    def test_accounting_share_is_the_naive_ratio(self):
        # 0.25 -> 0.10 loss: (0.90/0.75) - 1 = +20%
        self.assertAlmostEqual(m.accounting_share(0.25, 0.10), 0.2, places=10)

    def test_accounting_share_strictly_exceeds_behavioral_net(self):
        """The chapter's central claim: the mechanical calculation is an upper bound, always."""
        for p_from, p_to in ((0.30, 0.10), (0.25, 0.15), (0.20, 0.12), (0.15, 0.05)):
            acct = m.accounting_share(p_from, p_to)
            b_from = m.births_span_binding(p_from, 12.0, 5.0, 3.0, 1.5, 240.0)
            b_to = m.births_span_binding(p_to, 12.0, 5.0, 3.0, 1.5, 240.0)
            net = b_to / b_from - 1.0
            self.assertGreater(acct, net,
                               f"accounting {acct:.4f} should exceed net {net:.4f} for {p_from}->{p_to}")

    def test_overstatement_is_substantial_not_marginal(self):
        """If the two levels were within a few percent the distinction would not be worth drawing."""
        acct = m.accounting_share(0.25, 0.10)
        b_from = m.births_span_binding(0.25, 12.0, 5.0, 3.0, 1.5, 240.0)
        b_to = m.births_span_binding(0.10, 12.0, 5.0, 3.0, 1.5, 240.0)
        net = b_to / b_from - 1.0
        self.assertGreater(acct / net, 2.0)


class TestSimulation(unittest.TestCase):

    def test_simulation_is_reproducible(self):
        a = m.simulate((0.20, 0.28), (0.10, 0.15), n=500, seed=1)
        b = m.simulate((0.20, 0.28), (0.10, 0.15), n=500, seed=1)
        self.assertEqual(a["net"], b["net"])

    def test_falling_loss_raises_births(self):
        sim = m.simulate((0.20, 0.28), (0.10, 0.15), n=2000, seed=7)
        self.assertGreater(m.band(sim["net"])[0], 0)

    def test_band_returns_ordered_interval(self):
        med, lo, hi = m.band([float(i) for i in range(1000)])
        self.assertLess(lo, med)
        self.assertLess(med, hi)

    def test_no_draw_produces_a_negative_birth_interval(self):
        sim = m.simulate((0.20, 0.28), (0.10, 0.15), n=2000, seed=11)
        self.assertTrue(all(x > 0 for x in sim["bi_from"] + sim["bi_to"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
