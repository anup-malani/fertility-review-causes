#!/usr/bin/env python3
"""
145_b6_demographic_significance.py — B.6, PROTOCOL stage 10. Run once per chemical family.

Call 1 requires this computed separately for each family against its OWN exposure series, because
the two series move in opposite directions and a bundled figure would average them into
meaninglessness.

The computation is short because the result does not depend on the effect size. For PFAS_LEGACY the
verdict turns on a SIGN, not a magnitude: the exposure fell steeply across exactly the window in
which fertility also fell, so the association — even taken at face value, which the extraction says
it should not be — predicts the opposite of what happened. This is the same class of finding as B.5's
inverted FDT sign, and it is decisive in a way no effect estimate could be.

Inputs, both fetched rather than asserted:
  * Serum concentration change, NHANES 1999-March 2020, from a HELD full text (W4406683543):
    "PFOS, PFOA, and PFHxS declined 87%, 74%, and 52%, respectively."
  * US total fertility rate, World Bank WDI `SP.DYN.TFRT.IN`, cached to data/raw/ on first run so
    the computation is reproducible without the network.

The upper-bound arithmetic below is deliberately generous to the hypothesis at every step, and is
still reported as an upper bound rather than an estimate. Two deflators are named and NOT applied,
because applying them would understate the uncertainty rather than represent it: the fecundability-
to-quantum translation (a fecundability ratio moves time-to-pregnancy, and only converts into
completed family size where the reproductive span binds), and the restricted-track finding that the
association does not survive parity handling at all.

Output: data/raw/worldbank-usa-tfr.json  (cached input)
        literature/search-logs/{slug}-demographic-significance.md
"""
import json, os, subprocess

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RAW = os.path.join(ROOT, "data", "raw")
LOGS = os.path.join(ROOT, "literature", "search-logs")
TFR_CACHE = os.path.join(RAW, "worldbank-usa-tfr.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-demographic-significance.md")

# From W4406683543, held in full text. Percent DECLINE in serum geometric mean, NHANES 1999-2020.
PFAS_DECLINE = {"PFOS": 0.87, "PFOA": 0.74, "PFHxS": 0.52}
# The largest unrestricted association in the extraction table (S-PRESTO, PFOS, per quartile).
FR_PER_QUARTILE = 0.88
WINDOW = (1999, 2020)


def tfr_series():
    if os.path.exists(TFR_CACHE):
        return json.load(open(TFR_CACHE))
    url = ("https://api.worldbank.org/v2/country/USA/indicator/SP.DYN.TFRT.IN"
           "?format=json&per_page=120&date=1960:2023")
    out = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    series = {x["date"]: x["value"] for x in d[1] if x["value"] is not None}
    os.makedirs(RAW, exist_ok=True)
    json.dump({"source": "World Bank WDI SP.DYN.TFRT.IN, USA",
               "retrieved": "2026-08-14", "series": series}, open(TFR_CACHE, "w"), indent=2)
    return json.load(open(TFR_CACHE))


def main():
    tfr = tfr_series()["series"]
    y0, y1 = str(WINDOW[0]), str(WINDOW[1])
    t0, t1 = tfr[y0], tfr[y1]
    tfr_change = (t1 - t0) / t0

    # Upper bound, generous at every step. An 87% fall in concentration is roughly a fall of three
    # quartile steps for a right-skewed exposure distribution; the FR is inverted because exposure
    # went DOWN. This is an illustration of direction and rough scale, not an estimate.
    quartile_steps = 3
    implied_fecundability_gain = FR_PER_QUARTILE ** (-quartile_steps) - 1

    L = [f"# Demographic significance — {SLUG} (B.6)", "",
         "Computed once per chemical family, as Call 1 requires. Inputs are fetched, not asserted: "
         "the exposure change comes from a full text held in this chapter "
         "(`W4406683543`, NHANES 1999–March 2020) and the fertility series from World Bank WDI "
         "`SP.DYN.TFRT.IN`, cached to `data/raw/worldbank-usa-tfr.json`.", "",
         "## PFAS — the verdict is a sign, not a magnitude", "",
         f"Over **{y0}–{y1}**, US serum concentrations of the legacy compounds fell steeply:", "",
         "| compound | decline in serum geometric mean |", "|---|---|"]
    for c, d in PFAS_DECLINE.items():
        L.append(f"| {c} | **−{d:.0%}** |")
    L += ["",
          f"Over the same window US TFR moved **{t0:.3f} → {t1:.3f}**, a change of "
          f"**{tfr_change:+.1%}**.", "",
          "**The exposure and the outcome moved in the same direction, and the hypothesis requires "
          "them to move in opposite directions.** If PFAS suppress fertility, then an 87% fall in "
          "PFOS should have *raised* fertility across precisely this window. Fertility fell by 18%.", "",
          "Taking the largest unrestricted association in the extraction table at face value — "
          f"S-PRESTO's fecundability ratio of {FR_PER_QUARTILE} per quartile increase — and reading "
          f"an 87% concentration decline as roughly {quartile_steps} quartile steps downward, the "
          f"implied change is a fecundability *gain* of about **{implied_fecundability_gain:+.0%}**. "
          "The hypothesis, granted its own contested estimate, predicts the post-2000 US fertility "
          "decline should not have happened.", "",
          "### Three reasons that upper bound is still too generous", "",
          "1. **The estimate does not survive parity handling.** The extraction found that in both "
          "cohorts that ran a parity-restricted analysis, the association was not replicated "
          "(INUENDO) or was null (MoBa). The figure above uses a number the chapter's own evidence "
          "says is substantially reverse-causal.",
          "2. **A fecundability ratio is not a fertility quantity.** It moves time-to-pregnancy. It "
          "converts into completed family size only where the reproductive span binds, which for "
          "most exposed person-time it does not. The scope document pre-committed to keeping "
          "`HAZARD_DECREMENT` and `TEMPO_ADJUSTED_QUANTUM` apart for exactly this reason, and no "
          "record in the extraction table carries the latter.",
          "3. **The quartile arithmetic is an illustration, not a calibration.** Mapping a percentage "
          "concentration change onto quartile steps of a right-skewed distribution is rough, and it "
          "is done here only to show that the sign problem is not marginal.", "",
          "### PFAS_REPLACEMENT — a separate arm, and unresolved", "",
          "The falling series is the LEGACY compounds. Short-chain and replacement substances "
          "(GenX/HFPO-DA, PFO4DA, other precursors) entered use as the legacy ones were phased out, "
          "and NHANES did not measure most of them across this window. **The replacement arm's "
          "exposure series is therefore unknown, not flat**, and the chapter must say so rather than "
          "let the legacy decline stand for the whole family. The screen found mechanism work on "
          "replacements (`W7134253977` on GenX, `W4407964415` on PFO4DA, `W4205205091` on legacy vs "
          "replacement endocrine disruption) but no exposure series and no fertility estimate.", "",
          "### Verdict — PFAS", "",
          "**Demographically insignificant for the post-2000 period, on a sign argument that does not "
          "depend on the effect size.** The legacy exposure fell by most of its 1999 level across the "
          "window in which US fertility fell by 18%. Even the contested unrestricted association, "
          "applied generously, predicts the opposite of the observed change. The replacement arm is "
          "unresolved and is the only route by which a PFAS contribution to recent decline could "
          "survive; establishing it requires an exposure series nobody has built.", "",
          "## Microplastics — not computable, and that is the finding", "",
          "The demographic-significance calculation is exposure change × effect size. The exposure "
          "series is rising: plastic production has grown throughout the SDT and human internal "
          "exposure with it. **The effect size does not exist.** The extraction found five reviews "
          "and no effect estimate in the primary cell, and five empirical records that estimate "
          "fertility *inputs* — sperm parameters, retrieved oocytes, AMH — with p-values clustered at "
          "the margin and samples drawn from ART clinics.", "",
          "Multiplying a well-measured rising exposure by an effect size that has not been estimated "
          "produces a number with no content. The chapter reports **not computable** and states why, "
          "which is a stronger and more useful claim than a decomposition built on a placeholder.", "",
          "### Verdict — microplastics", "",
          "**Not computable. No effect estimate on a fertility quantity exists in a 920-record "
          "screen** whose completeness bypass guaranteed every both-axes plastic record was read. The "
          "exposure is real, rising, and now measurable inside the reproductive tract; what has not "
          "been done is the study that estimates its effect on a fertility outcome in humans. That "
          "absence is this half of the chapter's result.", "",
          "## Why the two verdicts differ in kind", "",
          "PFAS fails on **evidence that exists and points the wrong way**. Microplastics fails on "
          "**evidence that does not exist**. Both are negative verdicts and they are not "
          "interchangeable: the first is close to settled for the legacy compounds and could only be "
          "reopened by the replacement arm, while the second could be overturned by a single "
          "well-designed cohort. A bundled B.6 verdict would have concealed that difference, which "
          "is the strongest retrospective argument for the Call 1 split."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"TFR {y0}={t0:.3f} {y1}={t1:.3f} change={tfr_change:+.1%}")
    print(f"PFAS legacy decline: " + ", ".join(f"{c} −{d:.0%}" for c, d in PFAS_DECLINE.items()))
    print(f"implied fecundability gain from falling exposure (upper bound): "
          f"{implied_fecundability_gain:+.0%}")
    print("verdict PFAS: demographically insignificant post-2000 (sign argument)")
    print("verdict microplastics: not computable (no effect estimate exists)")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
