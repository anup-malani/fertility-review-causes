#!/usr/bin/env python3
"""
b7_demographic_significance.py — B.7 (antidepressants), PROTOCOL stage 10.

Computes the demographic significance of antidepressant exposure against the SDT, and does it twice:
once against the full SDT change as PROTOCOL 4.2 is currently written, and once against the change
that occurred after the exposure existed. The two differ by a factor the chapter cannot ignore, which
is Call 1.

THE THREE THINGS THIS SCRIPT ARGUES

1. THE TIMING WALL. Fluoxetine reached the US market in 1988. Most of the OECD TFR decline the SDT
   names was already complete by then. Scoring B.7 against the full-period denominator credits it
   with variation that finished before its cause existed, so the script reports the pre-exposure
   share explicitly and uses the post-1988 denominator for the verdict.

2. THE ESTIMAND LEVEL. A fecundability ratio is a HAZARD decrement, not a birth. Multiplying
   prevalence by (1 - FR) gives the share of conceptions displaced while exposed; it is an upper
   bound that assumes no recuperation whatsoever, and it is the direct analogue of B.5's
   ACCOUNTING_SHARE. The quantity the review's verdict needs is the tempo-adjusted quantum, which
   requires the deflator below.

3. THE DEFLATOR IS EXPOSURE DURATION AGAINST THE REPRODUCTIVE SPAN. A conception delayed is a birth
   forgone only where the span binds. Antidepressant episodes are short relative to a reproductive
   career, so for most exposed person-time the effect is displacement rather than loss. The deflator
   is derived here from a stated slack model rather than assumed, and it is the weakest parameter in
   the chapter — which is why it is a parameter with a range and a sensitivity surface rather than a
   number in the prose.

PARAMETER PROVENANCE. Every input is traceable to an extracted record or to a macro series in
data/raw. Nothing is asserted from memory; where a parameter could not be retrieved, the script says
so rather than substituting a plausible value.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TFR_JSON = os.path.join(ROOT, "data", "raw", "wdi_tfr_usa_oecd_dnk_nor.json")
OUT_JSON = os.path.join(ROOT, "output", "tables",
                        "antidepressants-ssri-subfecundity-demographic-significance.json")
OUT_MD = os.path.join(ROOT, "output", "tables",
                      "antidepressants-ssri-subfecundity-demographic-significance.md")

SSRI_MARKET_ENTRY = 1988          # fluoxetine, US
SDT_START = 1965                  # PROTOCOL 2
SIG_THRESHOLD = 0.10              # PROTOCOL 4.2 decomposition-share threshold

# --- Parameters, with the record each comes from -------------------------------------------------
PARAMS = {
    "p_exposed": dict(
        central=0.060, low=0.038, high=0.130,
        what="Share of reproductive-age person-time under antidepressant exposure.",
        source="Low: Laugesen et al. 2013 (BMJ Open), 3.8% of Danish women aged 25-44 current SSRI "
               "users. Central: 6.0%, between the Danish female figure and the PRESTO male figure of "
               "4.3% current SSRI / 8.8% any psychotropic (Yland et al. 2022). High: 13%, the US "
               "any-antidepressant adult prevalence implied by Pratt et al. (NCHS). "
               "NOT RETRIEVED: the age-and-sex-specific US series (Kunzel et al. 2023, J Women's "
               "Health) is the right parameter and is behind a paywall; the range here is wider than "
               "it would need to be because of that."),
    "fr_ssri": dict(
        central=0.85, low=0.65, high=1.12,
        what="Fecundability ratio for current SSRI use, adjusted for depression and other "
             "psychotropics. Values BELOW 1 mean reduced fecundability.",
        source="Yland et al. 2022, PRESTO preconception cohort, 2,398 men, FR = 0.85 [0.65, 1.12]. "
               "This is the ONLY estimate located anywhere in a 6,798-record frame that regresses a "
               "fertility hazard on antidepressant exposure while adjusting for the indication. Its "
               "confidence interval includes the null; it is male-side; it is one cohort."),
    "tau": dict(
        central=0.10, low=0.02, high=0.30,
        what="Transmission from a per-cycle fecundability decrement to COMPLETED fertility: the "
             "share of the hazard decrement that converts into a forgone birth rather than a "
             "postponed one.",
        source="Derived below from the slack model, not extracted. This is the chapter's weakest "
               "parameter and the verdict's sensitivity to it is reported in full."),
    "phi": dict(
        central=0.20, low=0.15, high=0.25,
        what="Baseline per-cycle conception probability among couples attempting.",
        source="PRESTO median TTP of 3 cycles and the standard fecundability range; Wilcox et al. "
               "1995 for the day-specific structure underneath it."),
    "k_births_remaining": dict(
        central=2.0, low=1.0, high=3.0,
        what="Conception attempts remaining at the time of exposure.",
        source="Set to the OECD completed-fertility neighbourhood. Enters only through the slack "
               "model."),
    "slack_years_mean": dict(
        central=6.0, low=3.0, high=10.0,
        what="Mean years between when a woman would finish childbearing absent any delay and the "
             "end of her fecund span.",
        source="Assumed, and flagged as assumed. It is the quantity that decides tau and the review "
               "has no extracted estimate of it."),
}


def tfr_series(path=TFR_JSON):
    """OECD-aggregate TFR by year from the cached World Bank pull (SP.DYN.TFRT.IN)."""
    d = json.load(open(path))
    out = {}
    for r in d[1]:
        code = r.get("countryiso3code") or (r.get("country") or {}).get("id")
        if code == "OED" and r.get("value") is not None:
            out[int(r["date"])] = float(r["value"])
    if not out:
        raise ValueError("no OECD TFR rows in the cached World Bank file")
    return out


def timing_wall(tfr, start=SDT_START, entry=SSRI_MARKET_ENTRY, end=None):
    """How much of the SDT decline was already complete when the exposure came into existence.

    Returns a dict. `pre_exposure_share` is the fraction of the total decline that predates market
    entry: the number Call 1 turns on."""
    end = end or max(tfr)
    t0, t1, t2 = tfr[start], tfr[entry], tfr[end]
    total = t0 - t2
    pre = t0 - t1
    post = t1 - t2
    return {
        "start_year": start, "entry_year": entry, "end_year": end,
        "tfr_start": t0, "tfr_entry": t1, "tfr_end": t2,
        "total_decline": total, "pre_exposure_decline": pre, "post_exposure_decline": post,
        "pre_exposure_share": pre / total if total else float("nan"),
        "total_decline_pct": total / t0 if t0 else float("nan"),
        "post_exposure_decline_pct": post / t1 if t1 else float("nan"),
    }


def extra_wait_months(phi, fr):
    """Additional months to conception caused by a proportional fecundability decrement.

    Mean waiting time under a geometric conception process is 1/phi cycles. A ratio fr scales phi, so
    the delay is 1/(fr*phi) - 1/phi. A cycle is taken as one month."""
    if fr <= 0:
        raise ValueError("fecundability ratio must be positive")
    return 1.0 / (fr * phi) - 1.0 / phi


def tau_from_slack(phi, fr, k, slack_years_mean):
    """Share of the hazard decrement that becomes a forgone rather than a postponed birth.

    A delay costs a birth only when it runs past the end of the fecund span. Model a woman's slack --
    the time between finishing childbearing on schedule and the span ending -- as exponential with
    the given mean. She loses a birth when her slack is shorter than the total delay her exposure
    imposes, k * extra_wait. Under the exponential that probability is 1 - exp(-delay/mean).

    The exponential is a choice and a strong one: it puts more mass near zero slack than a realistic
    distribution would, so this is a GENEROUS estimate of tau, which is the right direction for a
    number the chapter uses to argue an effect is small."""
    delay_months = k * extra_wait_months(phi, fr)
    mean_months = slack_years_mean * 12.0
    if delay_months <= 0:
        return 0.0
    return 1.0 - math.exp(-delay_months / mean_months)


def significance(p_exposed, fr, tau, tfr_wall, denominator="post"):
    """The two estimand levels, and the decomposition share against the chosen denominator.

    `mechanical` is the HAZARD_DECREMENT level: the share of conceptions displaced while exposed,
    assuming no recuperation at all. It is an upper bound and is reported only as one.
    `behavioural` is the TEMPO_ADJUSTED_QUANTUM level, which is what PROTOCOL 4.2 needs."""
    mechanical = p_exposed * (1.0 - fr)          # may be negative if fr > 1; that is meaningful
    behavioural = mechanical * tau
    denom = (tfr_wall["post_exposure_decline_pct"] if denominator == "post"
             else tfr_wall["total_decline_pct"])
    return {
        "denominator": denominator,
        "denominator_pct_change": denom,
        "mechanical_share_of_conceptions": mechanical,
        "behavioural_share_of_births": behavioural,
        "decomposition_share_mechanical": mechanical / denom if denom else float("nan"),
        "decomposition_share_behavioural": behavioural / denom if denom else float("nan"),
    }


def verdict(share, threshold=SIG_THRESHOLD):
    if share != share:                      # NaN
        return "insufficient data"
    if share >= threshold:
        return "significant"
    if share >= threshold / 2:
        return "partial"
    return "not significant"


def corner(p_key, fr_key, tau_key, wall, denominator="post"):
    p = PARAMS["p_exposed"][p_key]
    fr = PARAMS["fr_ssri"][fr_key]
    if tau_key == "derived":
        tau = tau_from_slack(PARAMS["phi"]["central"], fr,
                             PARAMS["k_births_remaining"]["central"],
                             PARAMS["slack_years_mean"]["central"])
    else:
        tau = PARAMS["tau"][tau_key]
    return significance(p, fr, tau, wall, denominator), tau


def main():
    tfr = tfr_series()
    wall = timing_wall(tfr)

    tau_derived = tau_from_slack(PARAMS["phi"]["central"], PARAMS["fr_ssri"]["central"],
                                 PARAMS["k_births_remaining"]["central"],
                                 PARAMS["slack_years_mean"]["central"])
    central_post, _ = corner("central", "central", "derived", wall, "post")
    central_full, _ = corner("central", "central", "derived", wall, "full")

    # The corner that most favours the hypothesis: highest prevalence, strongest effect, and no
    # recuperation at all. Reported because a "not significant" verdict is only worth anything if the
    # most favourable reading was computed and stated.
    best_case = significance(PARAMS["p_exposed"]["high"], PARAMS["fr_ssri"]["low"], 1.0, wall, "post")
    best_case_behav = significance(PARAMS["p_exposed"]["high"], PARAMS["fr_ssri"]["low"],
                                   PARAMS["tau"]["high"], wall, "post")

    grid = []
    for pk in ("low", "central", "high"):
        for fk in ("low", "central", "high"):
            s, t = corner(pk, fk, "derived", wall, "post")
            grid.append({"p": pk, "fr": fk, "p_value": PARAMS["p_exposed"][pk],
                         "fr_value": PARAMS["fr_ssri"][fk], "tau": t,
                         "mechanical_share": s["decomposition_share_mechanical"],
                         "behavioural_share": s["decomposition_share_behavioural"],
                         "verdict_behavioural": verdict(s["decomposition_share_behavioural"]),
                         "verdict_mechanical": verdict(s["decomposition_share_mechanical"])})

    result = {
        "hypothesis": "B.7 antidepressants-ssri-subfecundity",
        "phenomena": {"PM": "no cell — the exposure did not exist",
                      "FDT": "no cell — prescribing volumes negligible and the period closes in 1965",
                      "SDT": "the only cell, and restricted to the post-1988 sub-period"},
        "timing_wall": wall,
        "tau_derived": tau_derived,
        "extra_wait_months_central": extra_wait_months(PARAMS["phi"]["central"],
                                                       PARAMS["fr_ssri"]["central"]),
        "central_post_1988": central_post,
        "central_full_sdt": central_full,
        "most_favourable_no_recuperation": best_case,
        "most_favourable_with_recuperation": best_case_behav,
        "sensitivity_grid": grid,
        "verdict_sdt_post1988": verdict(central_post["decomposition_share_behavioural"]),
        "verdict_sdt_full_period": verdict(central_full["decomposition_share_behavioural"]),
        "params": PARAMS,
        "threshold": SIG_THRESHOLD,
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump(result, open(OUT_JSON, "w"), indent=2)

    pct = lambda x: f"{100 * x:.2f}%"
    L = ["# Demographic significance — antidepressants and pharmacological subfecundity (B.7)", "",
         "Generated by `source/analysis/b7_demographic_significance.py`. TFR is the OECD aggregate "
         "from the World Bank series cached at `data/raw/wdi_tfr_usa_oecd_dnk_nor.json`.", "",
         "## 1. The timing wall", "",
         f"| quantity | value |", "|---|---|",
         f"| OECD TFR, {wall['start_year']} (SDT opens) | {wall['tfr_start']:.3f} |",
         f"| OECD TFR, {wall['entry_year']} (fluoxetine reaches market) | {wall['tfr_entry']:.3f} |",
         f"| OECD TFR, {wall['end_year']} | {wall['tfr_end']:.3f} |",
         f"| total SDT decline | {wall['total_decline']:.3f} births ({pct(wall['total_decline_pct'])}) |",
         f"| decline already complete before the exposure existed | {wall['pre_exposure_decline']:.3f} births |",
         f"| **share of the SDT decline predating the exposure** | **{pct(wall['pre_exposure_share'])}** |",
         f"| decline available to B.7 (post-{wall['entry_year']}) | {wall['post_exposure_decline']:.3f} births ({pct(wall['post_exposure_decline_pct'])}) |",
         "",
         f"**{pct(wall['pre_exposure_share'])} of the decline B.7 is assigned to explain was finished "
         "before the first SSRI prescription was written.** Scoring the hypothesis against the full-"
         "period denominator would credit it with that. The verdict below uses the post-1988 "
         "denominator; the full-period figure is reported alongside so a reader applying PROTOCOL "
         "4.2 as literally written can see what it gives.", "",
         "## 2. The two estimand levels", "",
         f"At central parameters a current SSRI user's per-cycle conception probability falls from "
         f"{PARAMS['phi']['central']:.2f} to {PARAMS['fr_ssri']['central'] * PARAMS['phi']['central']:.3f}, "
         f"which lengthens the mean wait to conception by "
         f"**{extra_wait_months(PARAMS['phi']['central'], PARAMS['fr_ssri']['central']):.2f} months** "
         "per attempt. Whether that costs a birth depends on whether the reproductive span binds.", "",
         "| level | what it assumes | share of conceptions or births | share of the post-1988 decline |",
         "|---|---|---|---|",
         f"| `HAZARD_DECREMENT` (upper bound) | no recuperation at all | "
         f"{pct(central_post['mechanical_share_of_conceptions'])} of conceptions | "
         f"**{pct(central_post['decomposition_share_mechanical'])}** |",
         f"| `TEMPO_ADJUSTED_QUANTUM` (the verdict) | recuperation at the derived rate | "
         f"{pct(central_post['behavioural_share_of_births'])} of births | "
         f"**{pct(central_post['decomposition_share_behavioural'])}** |", "",
         f"The deflator is **tau = {tau_derived:.3f}**, derived rather than assumed: a delay of "
         f"{PARAMS['k_births_remaining']['central']:.0f} x "
         f"{extra_wait_months(PARAMS['phi']['central'], PARAMS['fr_ssri']['central']):.2f} months "
         f"costs a birth only for women whose remaining slack is shorter than that, which under an "
         f"exponential slack distribution with a {PARAMS['slack_years_mean']['central']:.0f}-year "
         "mean is a small minority. The exponential puts more mass near zero slack than a realistic "
         "distribution would, so this tau is generous to the hypothesis.", "",
         "## 3. Verdict", "", "| denominator | decomposition share | verdict |", "|---|---|---|",
         f"| post-1988 (used) | {pct(central_post['decomposition_share_behavioural'])} | "
         f"**{verdict(central_post['decomposition_share_behavioural'])}** |",
         f"| full SDT (PROTOCOL 4.2 as written) | {pct(central_full['decomposition_share_behavioural'])} | "
         f"{verdict(central_full['decomposition_share_behavioural'])} |", "",
         "## 4. The most favourable reading, computed rather than dismissed", "",
         "A negative verdict is worth nothing unless the corner of the parameter space that most "
         "favours the hypothesis was computed and stated. Taking the highest prevalence "
         f"({PARAMS['p_exposed']['high']:.0%}), the strongest effect in the confidence interval "
         f"(FR = {PARAMS['fr_ssri']['low']:.2f}), and assuming NO recuperation whatever:", "",
         f"- share of the post-1988 decline: **{pct(best_case['decomposition_share_mechanical'])}** "
         f"→ *{verdict(best_case['decomposition_share_mechanical'])}* under PROTOCOL 4.2's threshold.",
         f"- the same corner with recuperation at tau = {PARAMS['tau']['high']:.2f}: "
         f"{pct(best_case_behav['decomposition_share_behavioural'])} → "
         f"*{verdict(best_case_behav['decomposition_share_behavioural'])}*.", "",
         "So the hypothesis crosses the significance threshold **only** if one simultaneously takes "
         "the highest plausible exposure prevalence, the strong end of a confidence interval that "
         "includes the null, and the assumption that a delayed conception is a lost birth. The "
         "chapter's argument against the third of those is the same argument B.5 makes against "
         "reading (1-p) as an effect on completed fertility, and it does not depend on the first two.",
         "", "## 5. Sensitivity surface (post-1988 denominator)", "",
         "| prevalence | fecundability ratio | mechanical share | behavioural share | verdict |",
         "|---|---|---|---|---|"]
    for g in grid:
        L.append(f"| {g['p_value']:.1%} ({g['p']}) | {g['fr_value']:.2f} ({g['fr']}) | "
                 f"{pct(g['mechanical_share'])} | {pct(g['behavioural_share'])} | "
                 f"{g['verdict_behavioural']} |")
    L += ["", "## 6. What this computation cannot do", "",
          "The effect size is one confidence interval from one cohort of 2,398 men, and it includes "
          "the null. Everything above is arithmetic performed on that interval; the arithmetic is "
          "robust and the input is not. No female-side fecundability estimate adjusted for the "
          "indication was located anywhere in the frame, so the parameter carrying this entire "
          "computation is male and is being applied to a population effect that the hypothesis "
          "locates in women.", "",
          "The indication's own effect is larger than anything B.7 can claim and is measured better. "
          "In the Norwegian population register, depression throughout the reproductive period "
          "corresponds to completed fertility of 1.34 against 1.60 for women with none of the "
          "disorders studied, and 0.90 against 1.41 for men. B.7's claim is that the medication adds "
          "a decrement on top of that, and the only estimate of the addition is FR = 0.85 [0.65, "
          "1.12]."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"pre-exposure share of SDT decline: {wall['pre_exposure_share']:.1%}")
    print(f"tau (derived): {tau_derived:.4f}")
    print(f"central, post-1988: mechanical {central_post['decomposition_share_mechanical']:.2%}, "
          f"behavioural {central_post['decomposition_share_behavioural']:.2%} "
          f"-> {verdict(central_post['decomposition_share_behavioural'])}")
    print(f"most favourable, no recuperation: "
          f"{best_case['decomposition_share_mechanical']:.2%} -> "
          f"{verdict(best_case['decomposition_share_mechanical'])}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
