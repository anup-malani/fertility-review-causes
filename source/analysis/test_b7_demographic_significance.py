#!/usr/bin/env python3
"""Tests for b7_demographic_significance.

The tests that matter here are the ones that would catch a sign error or a denominator swap, because
those are the two mistakes that would flip the chapter's verdict without looking wrong. B.5's run
found an inverted sign only because the arithmetic was tested against a case whose answer was known
independently; the same discipline applies.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b7_demographic_significance as b7


# --- extra_wait_months -------------------------------------------------------------------------
def test_no_effect_means_no_delay():
    assert b7.extra_wait_months(0.20, 1.0) == 0.0


def test_delay_is_positive_when_fecundability_falls():
    assert b7.extra_wait_months(0.20, 0.85) > 0


def test_delay_is_negative_when_fecundability_rises():
    """FR > 1 must produce a NEGATIVE delay, not a positive one. Several records in the frame report
    the effect running the other way (treatment improving function), and a formula that took an
    absolute value would silently convert a benefit into a harm."""
    assert b7.extra_wait_months(0.20, 1.10) < 0


def test_delay_matches_hand_computation():
    # 1/(0.85*0.20) - 1/0.20 = 5.882... - 5 = 0.882...
    assert math.isclose(b7.extra_wait_months(0.20, 0.85), 0.88235, rel_tol=1e-4)


def test_zero_or_negative_ratio_raises():
    for bad in (0.0, -0.5):
        try:
            b7.extra_wait_months(0.20, bad)
        except ValueError:
            continue
        raise AssertionError(f"fr={bad} should raise")


# --- tau_from_slack ----------------------------------------------------------------------------
def test_tau_is_a_probability():
    t = b7.tau_from_slack(0.20, 0.85, 2.0, 6.0)
    assert 0.0 <= t <= 1.0


def test_tau_is_zero_when_there_is_no_delay():
    assert b7.tau_from_slack(0.20, 1.0, 2.0, 6.0) == 0.0


def test_tau_rises_as_slack_shrinks():
    """Less slack means the span binds for more women, so more of the delay becomes lost births."""
    assert b7.tau_from_slack(0.20, 0.85, 2.0, 3.0) > b7.tau_from_slack(0.20, 0.85, 2.0, 10.0)


def test_tau_rises_with_more_remaining_births():
    assert b7.tau_from_slack(0.20, 0.85, 3.0, 6.0) > b7.tau_from_slack(0.20, 0.85, 1.0, 6.0)


def test_tau_is_small_at_central_parameters():
    """The chapter's argument is that this deflator is large. If a change to the model ever made tau
    approach 1, the argument would silently invert while still 'running'."""
    assert b7.tau_from_slack(0.20, 0.85, 2.0, 6.0) < 0.05


# --- timing_wall -------------------------------------------------------------------------------
def test_timing_wall_shares_sum_to_the_whole():
    tfr = {1965: 3.0, 1988: 2.0, 2023: 1.5}
    w = b7.timing_wall(tfr, 1965, 1988, 2023)
    assert math.isclose(w["pre_exposure_decline"] + w["post_exposure_decline"], w["total_decline"])
    assert math.isclose(w["pre_exposure_share"], 1.0 / 1.5)


def test_timing_wall_on_the_real_series():
    """The headline number. If the cached series changes, this test says so rather than the chapter
    quietly reporting a different figure."""
    w = b7.timing_wall(b7.tfr_series())
    assert 0.60 < w["pre_exposure_share"] < 0.75
    assert w["tfr_entry"] < w["tfr_start"]
    assert w["tfr_end"] < w["tfr_entry"]


# --- significance ------------------------------------------------------------------------------
def _wall():
    return b7.timing_wall({1965: 3.0, 1988: 2.0, 2023: 1.5}, 1965, 1988, 2023)


def test_mechanical_exceeds_behavioural_whenever_tau_is_below_one():
    s = b7.significance(0.06, 0.85, 0.10, _wall())
    assert s["mechanical_share_of_conceptions"] > s["behavioural_share_of_births"]


def test_tau_of_one_collapses_the_two_levels():
    s = b7.significance(0.06, 0.85, 1.0, _wall())
    assert math.isclose(s["mechanical_share_of_conceptions"], s["behavioural_share_of_births"])


def test_beneficial_effect_gives_a_negative_share():
    """FR > 1 means the medication RAISES fecundability. The share must come out negative rather than
    being read as a contribution to the decline. This is B.5's inverted-sign lesson: a hypothesis can
    push against its phenomenon and the arithmetic must be able to say so."""
    s = b7.significance(0.06, 1.10, 0.10, _wall())
    assert s["mechanical_share_of_conceptions"] < 0
    assert s["decomposition_share_behavioural"] < 0


def test_the_post_denominator_is_smaller_and_therefore_harsher():
    """The post-1988 denominator is the SMALLER decline, so the same effect is a LARGER share of it.
    Using it is the demanding choice only because it also strips out the pre-exposure period the
    hypothesis cannot have caused; if this ordering ever flips, Call 1's reasoning breaks."""
    w = _wall()
    post = b7.significance(0.06, 0.85, 0.10, w, "post")
    full = b7.significance(0.06, 0.85, 0.10, w, "full")
    assert post["denominator_pct_change"] < full["denominator_pct_change"]
    assert post["decomposition_share_behavioural"] > full["decomposition_share_behavioural"]


def test_zero_prevalence_means_zero_effect():
    s = b7.significance(0.0, 0.85, 0.10, _wall())
    assert s["mechanical_share_of_conceptions"] == 0.0
    assert s["decomposition_share_behavioural"] == 0.0


# --- verdict -----------------------------------------------------------------------------------
def test_verdict_thresholds():
    assert b7.verdict(0.20) == "significant"
    assert b7.verdict(0.10) == "significant"
    assert b7.verdict(0.07) == "partial"
    assert b7.verdict(0.01) == "not significant"
    assert b7.verdict(float("nan")) == "insufficient data"


def test_central_case_is_not_significant():
    """The chapter's headline verdict, pinned. A parameter edit that flips it should fail here and be
    argued for, not discovered in the prose."""
    w = b7.timing_wall(b7.tfr_series())
    s, _ = b7.corner("central", "central", "derived", w, "post")
    assert b7.verdict(s["decomposition_share_behavioural"]) == "not significant"


def test_most_favourable_corner_is_computed_and_is_not_trivially_small():
    """The negative verdict is only credible if the favourable corner was actually computed. This
    asserts that the corner is materially larger than the central case, so the report is comparing
    two different readings rather than restating one."""
    w = b7.timing_wall(b7.tfr_series())
    central, _ = b7.corner("central", "central", "derived", w, "post")
    best = b7.significance(b7.PARAMS["p_exposed"]["high"], b7.PARAMS["fr_ssri"]["low"], 1.0, w, "post")
    assert (best["decomposition_share_mechanical"]
            > 10 * central["decomposition_share_behavioural"])


if __name__ == "__main__":
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith("test_") and callable(f)]
    failed = 0
    for n, f in fns:
        try:
            f()
            print(f"  PASS {n}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {n}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    raise SystemExit(1 if failed else 0)
