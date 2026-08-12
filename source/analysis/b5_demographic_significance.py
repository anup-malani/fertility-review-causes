#!/usr/bin/env python3
"""
b5_demographic_significance.py — B.5 (fetal loss / intrauterine mortality), PROTOCOL stage 10.

Computes the demographic significance of intrauterine mortality for the pre-modern (PM) and First
Demographic Transition (FDT) phenomena, under the two estimand levels the scope document requires to
be kept apart:

  ACCOUNTING_SHARE  births proportional to (1 - p). The mechanical share. An UPPER BOUND that assumes
                    a woman gets one conception and that a lost conception is a lost birth.
  BEHAVIORAL_NET    births implied by the birth-interval model, in which a loss costs TIME rather than
                    a birth. This is the quantity PROTOCOL section 4.2 actually asks for.

THE MODEL. In a natural-fertility population the mean closed birth interval decomposes additively
(Sheps and Menken 1973; Bongaarts 1978; Bongaarts and Potter 1983):

    BI = i + w + g + TA(p)

  i   postpartum infecundable interval, driven by breastfeeding
  w   mean waiting time to conception, = 1/fecundability
  g   gestation, 9 months
  TA  time added by intrauterine mortality

Each recognised loss consumes the gestation elapsed before it, a short recovery period, and a fresh
waiting time. The expected number of losses per live birth is p/(1-p), so

    TA(p) = [p / (1 - p)] * (g_L + r + w)

Births over an exposed reproductive span T are then T / BI, and the elasticity of births with respect
to p follows. THE CRITICAL PROPERTY: the effect operates only where the SPAN binds. Where a parity
target binds instead, a couple replaces the loss and completed fertility is unchanged, so the model
returns the target and the elasticity is zero by construction. The chapter's central claim is that
this regime dependence is the whole story, and it is imposed here rather than assumed away.

PARAMETERS come from the screened corpus and each carries its source in PARAM_SOURCES below. Ranges,
not points: every headline number is reported as an interval from a Monte Carlo draw over the
parameter ranges, because the inputs are genuinely uncertain and a point estimate would misrepresent
them.

Run: python3 source/analysis/b5_demographic_significance.py
Test: python3 source/analysis/test_b5_demographic_significance.py
"""
import json
import os
import random
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_MD = os.path.join(ROOT, "output", "tables",
                      "fetal-loss-intrauterine-mortality-demographic-significance.md")
OUT_JSON = os.path.join(ROOT, "output", "tables",
                        "fetal-loss-intrauterine-mortality-demographic-significance.json")

GESTATION = 9.0          # months, live birth
N_DRAWS = 20000
SEED = 20260811          # fixed: this stage must be reproducible bit-for-bit

# --- Parameter ranges (low, high). Sources in PARAM_SOURCES. ---
PARAMS = {
    # Mean waiting time to conception, months. Natural-fertility fecundability ~0.15-0.25/month.
    "w": (4.0, 7.0),
    # Postpartum infecundable interval, months. Long-breastfeeding regimes sit high in this range.
    "i": (9.0, 18.0),
    # Mean gestation elapsed at a recognised loss, months. Most recognised loss is first-trimester;
    # the stillbirth tail pulls the mean up modestly.
    "g_L": (2.5, 4.0),
    # Recovery / infecundable period after a loss, months.
    "r": (1.0, 2.5),
    # Exposed reproductive span in a natural-fertility marriage, months (roughly age 20-40).
    "T": (216.0, 264.0),
}

PARAM_SOURCES = {
    "w": "Fecundability 0.15-0.25/month in natural-fertility populations; Wood 1994 (Dynamics of "
         "Human Reproduction), Hutterite fecundability by age and parity (Demography 1993).",
    "i": "Bongaarts 1978 proximate-determinants framework; postpartum infecundability is the "
         "dominant interval component under prolonged breastfeeding. Cross-refs A.13.",
    "g_L": "Gestational distribution of recognised loss: Wilcox et al. 1988 (NEJM), Macklon et al. "
           "2002 (Hum Reprod Update), 'Biological Causes of Foetal Loss' (1993).",
    "r": "Time added per loss, Bongaarts and Potter 1983; recovery interval after early loss, "
         "Schisterman et al. 2016 (Obstet Gynecol, trying to conceive after an early loss).",
    "T": "Exposed span within marriage under the European and non-European marriage patterns; "
         "cross-refs A.7.",
}

# --- Loss-rate scenarios. p = probability a RECOGNISED conception ends in loss. ---
# The window matters and is stated: these are clinically recognised losses (roughly 6 weeks onward),
# NOT total post-implantation loss, which Wilcox et al. 1988 put near 31% and which is invisible in
# every historical source. Using the total-loss figure here would inflate every number below.
SCENARIOS = {
    "PM_high_morbidity": (0.20, 0.28),
    "PM_low_morbidity": (0.10, 0.15),
    "FDT_start_c1870": (0.16, 0.24),
    "FDT_end_c1965": (0.09, 0.13),
    "contemporary": (0.11, 0.15),
}

SCENARIO_SOURCES = {
    "PM_high_morbidity": "Upper end anchored on populations with endemic malaria, syphilis and "
                         "undernutrition; WFS-era estimates across eight countries (Social Biology "
                         "1989) and the Varanasi pregnancy-wastage cohort. Under-reporting means "
                         "recorded rates are floors, so the range is drawn wide.",
    "PM_low_morbidity": "Recognised-loss rates in low-morbidity natural-fertility populations; "
                        "Hutterite prospective series.",
    "FDT_start_c1870": "Late-fetal death alone ran 40-50 per 1000 births in nineteenth-century "
                       "Europe (Woods 2009); early loss is unobserved and is inferred from "
                       "contemporary recognised-loss rates plus a morbidity premium.",
    "FDT_end_c1965": "Stillbirth rates fell to roughly 10-15 per 1000 by the 1960s in northern "
                     "Europe (Danish post-1940 decline, Population Studies 2010); early-loss "
                     "component assumed near contemporary levels.",
    "contemporary": "Blencowe et al. 2016 stillbirth estimates; Quenby et al. 2021 miscarriage "
                    "prevalence; NSFG self-reported loss trend 1990-2011.",
}


def draw(rng, lo, hi):
    return rng.uniform(lo, hi)


def time_added(p, g_L, r, w):
    """Months added to the mean birth interval per live birth by intrauterine mortality."""
    if p >= 1.0:
        raise ValueError("p must be below 1")
    return (p / (1.0 - p)) * (g_L + r + w)


def birth_interval(p, i, w, g_L, r):
    return i + w + GESTATION + time_added(p, g_L, r, w)


def births_span_binding(p, i, w, g_L, r, T):
    """Births when the reproductive SPAN binds: exposure divided by the mean interval."""
    return T / birth_interval(p, i, w, g_L, r)


def accounting_share(p_hi, p_lo):
    """The mechanical (1-p) calculation: the upper bound the chapter reports only as one."""
    return (1.0 - p_lo) / (1.0 - p_hi) - 1.0


def simulate(p_from, p_to, n=N_DRAWS, seed=SEED):
    """Proportional change in births moving from loss rate p_from to p_to, both levels."""
    rng = random.Random(seed)
    net, acct, bi_from, bi_to = [], [], [], []
    for _ in range(n):
        pr = {k: draw(rng, *v) for k, v in PARAMS.items()}
        pf, pt = draw(rng, *p_from), draw(rng, *p_to)
        b_from = births_span_binding(pf, pr["i"], pr["w"], pr["g_L"], pr["r"], pr["T"])
        b_to = births_span_binding(pt, pr["i"], pr["w"], pr["g_L"], pr["r"], pr["T"])
        net.append(b_to / b_from - 1.0)
        acct.append(accounting_share(pf, pt))
        bi_from.append(birth_interval(pf, pr["i"], pr["w"], pr["g_L"], pr["r"]))
        bi_to.append(birth_interval(pt, pr["i"], pr["w"], pr["g_L"], pr["r"]))
    return {"net": net, "accounting": acct, "bi_from": bi_from, "bi_to": bi_to}


def band(xs):
    xs = sorted(xs)
    lo = xs[int(0.025 * len(xs))]
    hi = xs[int(0.975 * len(xs))]
    return statistics.median(xs), lo, hi


def pct(x):
    return f"{100 * x:+.1f}%"


def main():
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    results = {}

    # --- PM: cross-population variation between high- and low-morbidity regimes ---
    pm = simulate(SCENARIOS["PM_high_morbidity"], SCENARIOS["PM_low_morbidity"])
    # --- FDT: the within-population decline in loss, c.1870 to c.1965 ---
    fdt = simulate(SCENARIOS["FDT_start_c1870"], SCENARIOS["FDT_end_c1965"])

    for name, sim in (("PM", pm), ("FDT", fdt)):
        n_med, n_lo, n_hi = band(sim["net"])
        a_med, a_lo, a_hi = band(sim["accounting"])
        bif = band(sim["bi_from"])[0]
        bit = band(sim["bi_to"])[0]
        results[name] = {
            "behavioral_net": {"median": n_med, "lo": n_lo, "hi": n_hi},
            "accounting_share": {"median": a_med, "lo": a_lo, "hi": a_hi},
            "mean_birth_interval_months": {"from": bif, "to": bit},
            "overstatement_ratio": a_med / n_med if n_med else None,
        }

    # --- FDT contribution as a share of the observed TFR decline ---
    # Observed FDT decline: TFR roughly 5.5 to 3.0 in the transitioning West (PROTOCOL section 2).
    TFR_START, TFR_END = 5.5, 3.0
    observed_change = TFR_END - TFR_START            # negative: a decline
    fdt_net_med = results["FDT"]["behavioral_net"]["median"]
    fdt_tfr_effect = TFR_START * fdt_net_med          # positive: loss decline RAISES births
    fdt_share_abs = abs(fdt_tfr_effect / observed_change)
    results["FDT_vs_observed"] = {
        "tfr_start": TFR_START, "tfr_end": TFR_END,
        "observed_change": observed_change,
        "b5_tfr_effect": fdt_tfr_effect,
        "share_of_observed_magnitude": fdt_share_abs,
        "sign": "OPPOSES the observed decline",
    }

    # --- Regime dependence: the same loss change under a binding parity target ---
    results["target_binding_regime"] = {
        "behavioral_net": 0.0,
        "note": "Where a parity target binds and the span does not, the couple replaces the loss and "
                "completed fertility is unchanged. The model returns the target by construction, "
                "which is the point: B.5's effect is a property of the fertility regime, not of the "
                "loss rate alone.",
    }

    json.dump({"params": PARAMS, "param_sources": PARAM_SOURCES, "scenarios": SCENARIOS,
               "scenario_sources": SCENARIO_SOURCES, "n_draws": N_DRAWS, "seed": SEED,
               "results": results}, open(OUT_JSON, "w"), indent=2)

    pmn, fdtn = results["PM"]["behavioral_net"], results["FDT"]["behavioral_net"]
    pma, fdta = results["PM"]["accounting_share"], results["FDT"]["accounting_share"]

    L = [f"# Demographic significance — fetal loss and intrauterine mortality (B.5)", "",
         f"Generated by `source/analysis/b5_demographic_significance.py` "
         f"({N_DRAWS:,} Monte Carlo draws, seed {SEED}). Every figure is a median with a 95% interval "
         "across the parameter ranges, because the inputs are genuinely uncertain and a point "
         "estimate would misrepresent them.", "",
         "## The two estimand levels, side by side", "",
         "| phenomenon | loss-rate change | ACCOUNTING_SHARE (upper bound) | BEHAVIORAL_NET (the "
         "quantity PROTOCOL 4.2 asks for) | overstatement |", "|---|---|---|---|---|",
         f"| **Pre-modern** | {SCENARIOS['PM_high_morbidity'][0]:.2f}-{SCENARIOS['PM_high_morbidity'][1]:.2f} "
         f"to {SCENARIOS['PM_low_morbidity'][0]:.2f}-{SCENARIOS['PM_low_morbidity'][1]:.2f} | "
         f"{pct(pma['median'])} ({pct(pma['lo'])} to {pct(pma['hi'])}) | "
         f"{pct(pmn['median'])} ({pct(pmn['lo'])} to {pct(pmn['hi'])}) | "
         f"{results['PM']['overstatement_ratio']:.1f}x |",
         f"| **FDT** | {SCENARIOS['FDT_start_c1870'][0]:.2f}-{SCENARIOS['FDT_start_c1870'][1]:.2f} "
         f"to {SCENARIOS['FDT_end_c1965'][0]:.2f}-{SCENARIOS['FDT_end_c1965'][1]:.2f} | "
         f"{pct(fdta['median'])} ({pct(fdta['lo'])} to {pct(fdta['hi'])}) | "
         f"{pct(fdtn['median'])} ({pct(fdtn['lo'])} to {pct(fdtn['hi'])}) | "
         f"{results['FDT']['overstatement_ratio']:.1f}x |", "",
         "The gap between the two columns is the chapter's central quantitative finding. The "
         "mechanical calculation overstates the effect on completed fertility by a factor of roughly "
         f"{results['PM']['overstatement_ratio']:.0f}, because a loss consumes a fraction of a birth "
         "interval rather than a whole birth. The mean interval moves from "
         f"{results['PM']['mean_birth_interval_months']['from']:.1f} to "
         f"{results['PM']['mean_birth_interval_months']['to']:.1f} months across the pre-modern "
         "contrast, and births are exposure divided by that interval.", "",
         "## Pre-modern", "",
         f"Moving a natural-fertility population from a high-morbidity recognised-loss rate to a "
         f"low-morbidity one raises completed fertility by **{pct(pmn['median'])}** "
         f"({pct(pmn['lo'])} to {pct(pmn['hi'])}). Against pre-modern total fertility of roughly 6 "
         f"births, that is about {6 * pmn['median']:.2f} of a birth per woman.", "",
         "**Verdict: partial.** The effect is real, is not trivial, and is smaller than the "
         "proximate-determinants literature's other components — postpartum infecundability and the "
         "waiting time to conception each move the interval more. It clears no single threshold in "
         "PROTOCOL 4.2 decisively on its own.", "",
         "## FDT", "",
         f"The decline in intrauterine mortality across the transition raises births by "
         f"**{pct(fdtn['median'])}** ({pct(fdtn['lo'])} to {pct(fdtn['hi'])}) where the span binds. "
         f"Applied to a starting TFR of {TFR_START}, that is **{fdt_tfr_effect:+.3f} births per "
         f"woman**, against an observed decline of {observed_change:+.1f}.", "",
         f"**The sign is inverted.** B.5 pushes fertility UP across a period in which it fell by "
         f"half, so the hypothesis does not explain the FDT. Its magnitude is "
         f"**{100 * fdt_share_abs:.1f}%** of the observed change, meaning the behavioural component "
         f"of the FDT decline was larger than the raw TFR series shows by about that much. This is "
         "the scoring problem raised as Call 1 in the search scope, and it is why the FDT verdict is "
         "reported as a magnitude with an explicit sign rather than as a contribution.", "",
         "## The regime dependence is the finding", "",
         "Where a parity target binds rather than the reproductive span, the couple replaces the "
         "loss and completed fertility is unchanged. The model returns zero by construction, and "
         "that is not a modelling artefact: it is the mechanism. B.5's effect is a property of the "
         "fertility REGIME as much as of the loss rate, which predicts a large pre-modern effect "
         "decaying to nothing as fertility comes under control. That prediction is independently "
         "testable against the Danish registry study of early pregnancy complications and completed "
         "family size, which observes a controlled-fertility population and should therefore find "
         "little or nothing.", "",
         "## Slope sufficiency", "",
         "| phenomenon | sufficient to produce the observed variation? |", "|---|---|",
         f"| Pre-modern | **Partial.** {pct(pmn['median'])} against cross-population pre-modern TFR "
         "variation of roughly 4 to 8 births. Contributory, not sufficient. |",
         f"| FDT | **Insufficient, and wrong-signed.** {pct(fdtn['median'])} upward against a decline "
         "of roughly 45%. |", "",
         "## Parameters and their sources", "", "| parameter | range | source |", "|---|---|---|"]
    for k, (lo, hi) in PARAMS.items():
        L.append(f"| `{k}` | {lo}-{hi} months | {PARAM_SOURCES[k]} |")
    L += ["", "| scenario | recognised-loss rate | source |", "|---|---|---|"]
    for k, (lo, hi) in SCENARIOS.items():
        L.append(f"| `{k}` | {lo:.2f}-{hi:.2f} | {SCENARIO_SOURCES[k]} |")
    L += ["", "## What would change these numbers", "",
          "- **The observation window.** These are CLINICALLY RECOGNISED losses. Total "
          "post-implantation loss is near 31% (Wilcox et al. 1988), but pre-recognition loss cannot "
          "lengthen a birth interval by much, because a conception lost before recognition costs "
          "little more than one cycle. Using the total figure would inflate every number here, and "
          "is the single most common way this calculation is done wrong.",
          "- **The historical early-loss rate is unobserved.** Nineteenth-century sources record "
          "stillbirths, not miscarriages, so the FDT starting value is part inference. The reported "
          "interval reflects that, and it is the largest single source of uncertainty in the FDT row.",
          "- **Under-reporting biases recorded rates downward**, so the historical contrast may be "
          "understated. Casterline 1989 and Leridon 1976 both find substantial and non-random "
          "omission; the correction factors in the 2023 53-country survey analysis would sharpen this.",
          "- **Induced abortion contaminates the measured series** wherever it is illegal or "
          "stigmatised (Wall 4), and in the direction of overstating spontaneous loss."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"PM   net {pct(pmn['median'])} [{pct(pmn['lo'])}, {pct(pmn['hi'])}]  "
          f"accounting {pct(pma['median'])}  overstatement {results['PM']['overstatement_ratio']:.1f}x")
    print(f"FDT  net {pct(fdtn['median'])} [{pct(fdtn['lo'])}, {pct(fdtn['hi'])}]  "
          f"accounting {pct(fdta['median'])}  overstatement {results['FDT']['overstatement_ratio']:.1f}x")
    print(f"FDT effect on TFR {fdt_tfr_effect:+.3f} births vs observed {observed_change:+.1f} "
          f"({100 * fdt_share_abs:.1f}% of the magnitude, OPPOSITE sign)")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
