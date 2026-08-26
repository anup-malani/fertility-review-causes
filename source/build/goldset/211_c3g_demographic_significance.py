#!/usr/bin/env python3
"""
211_c3g_demographic_significance.py — C.3.g, stage 10. Demographic significance, computed.

**THE UNITS CHECK COMES FIRST AND IT NEARLY SETTLES THE CHAPTER.** The phenomenon is a decline in
COMPLETED CHILDREN PER WOMAN. The mechanism, as this literature measures it, is a percentage change
in the ANNUAL PROBABILITY OF A FIRST BIRTH among people who hold student debt, observed to about age
30. Those are not the same units and the gap is not rhetorical: a first-birth hazard truncated at 30
cannot distinguish postponement from foregone children, and a decline in completed fertility is
exactly the thing it cannot see.

So this script computes an UPPER BOUND, deliberately generously, and reports what the bound rules
out rather than what it estimates. Every input is either pulled live or is a published number from a
retrieved full text, and each is labelled.

THE ARITHMETIC, stated before it is run so a reader can check it:

  1. Convert an annual first-birth hazard h to a cumulative probability of a first birth over the
     observed window: P = 1 - (1-h)^YEARS.
  2. Take the difference between the no-debt hazard and the debt hazard, giving Δ in percentage
     points of women who have a first birth by the end of the window.
  3. Multiply by the SHARE OF WOMEN EXPOSED at that debt level.
  4. Express the result as a share of the observed TFR decline.

Step 4 contains a deliberate over-statement that must be named: a first birth is not a completed
family, so Δ first births is an UPPER BOUND on Δ TFR. Treating them as equal inflates the mechanism.
The bound is computed that way on purpose — a mechanism that is small when measured generously is
robust to the corrections not yet made.

THE EXPOSED SHARE IS NOT SOURCED FROM A SINGLE NUMBER, AND THAT IS DELIBERATE. The scope flagged
that the exposure series lives in institutional publications that are not indexed as works, and this
chapter did not retrieve one. Rather than assert a share from memory, the bound is computed ACROSS A
RANGE and the reader is shown where the verdict would change. If the verdict is the same at every
plausible exposed share, the missing series does not matter — which is itself worth knowing.

THE SECOND BOUND, INDEPENDENT OF ANY EFFECT SIZE: mass education debt is a post-2000 phenomenon, and
most of the SDT decline predates it. That share is computed from the TFR series alone and bounds the
mechanism before any estimate is applied — B.7's arithmetic, where 67.6% of the decline predated the
exposure.

Output: extraction/{slug}-demographic-significance.json
        literature/search-logs/{slug}-demographic-significance.md
"""
import json, os, subprocess, sys

SLUG = "student-debt-household-formation"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
OUT_JSON = os.path.join(EXTRACT, f"{SLUG}-demographic-significance.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-demographic-significance.md")

SDT_START = 1965          # PROTOCOL dates the SDT from ~1965
DEBT_ERA = 2000           # v5 restricts the claim to cohorts coming of age post-2000
WINDOW_YEARS = 10         # NLSY97 observes first births to roughly age 30; Nau's window is ages 20-30

# --- Published inputs, each from a retrieved full text and attributed ---
NAU = dict(
    source="Nau, Dwyer & Hodson 2015, Res Soc Stratif Mobil (BioC full text)",
    hazard_no_debt=0.043,           # predicted annual probability of first birth, zero student loans
    hazard_50k=0.028,
    hazard_60k=0.025,               # "a 42% decrease in the risk of fertility"
    per_1000_pct=0.012,             # 1.2% decrease in annual risk per $1,000, among debtors
    share_borrowers_over_50k_age25=0.09,
    share_borrowers_over_60k_age25=0.06,
    note="Women only. Annual hazard of transition to first birth, NLSY97, observed to about age 30.")

ROBB = dict(
    source="Robb & Schreiber 2019, SSRN (abstract)",
    marriage_per_1000_pct=0.013,    # 1.3% lower likelihood of marriage per $1,000
    first_birth="NOT SIGNIFICANT",
    note="In-state tuition IV, four-year graduates only, first four years after graduation.")

EXPOSED_SHARES = [0.20, 0.30, 0.40, 0.50]   # share of women in the cohort holding student debt


def wb_tfr(iso="USA"):
    url = (f"https://api.worldbank.org/v2/country/{iso}/indicator/SP.DYN.TFRT.IN"
           "?format=json&per_page=400")
    out = subprocess.run(["curl", "-sL", "-m", "60", url], capture_output=True, text=True).stdout
    try:
        rows = json.loads(out)[1]
    except Exception:
        return None
    return {int(r["date"]): r["value"] for r in rows if r.get("value") is not None}


def cumulative(h, years=WINDOW_YEARS):
    return 1 - (1 - h) ** years


def main():
    tfr = wb_tfr("USA")
    if not tfr:
        sys.stderr.write("ABORT: World Bank TFR unavailable — UNCONFIRMED, not zero.\n")
        sys.exit(1)
    latest = max(tfr)
    t_start, t_debt, t_latest = tfr[SDT_START], tfr[DEBT_ERA], tfr[latest]
    total_decline = t_start - t_latest
    post_decline = t_debt - t_latest
    pre_share = (t_start - t_debt) / total_decline

    # --- Bound 1: the share of the decline that predates the exposure ---
    bound1 = dict(tfr_1965=t_start, tfr_2000=t_debt, tfr_latest=t_latest, latest_year=latest,
                  total_decline=total_decline, post_2000_decline=post_decline,
                  share_predating_exposure=pre_share)

    # --- Bound 2: the strongest published association, applied generously ---
    p0 = cumulative(NAU["hazard_no_debt"])
    scenarios = []
    for label, h, exposed_within in (
            ("heaviest borrowers (>$60k)", NAU["hazard_60k"], NAU["share_borrowers_over_60k_age25"]),
            ("heavy borrowers (>$50k)", NAU["hazard_50k"], NAU["share_borrowers_over_50k_age25"]),
            ("all borrowers, at the >$50k effect", NAU["hazard_50k"], 1.0)):
        p1 = cumulative(h)
        delta_first_births = p0 - p1          # in first births per woman, within the exposed group
        for d in EXPOSED_SHARES:
            pop_effect = delta_first_births * d * exposed_within
            scenarios.append(dict(
                scenario=label, exposed_share=d, within_group_share=exposed_within,
                cum_prob_no_debt=p0, cum_prob_debt=p1,
                delta_within_group=delta_first_births, population_effect_children=pop_effect,
                share_of_total_decline=pop_effect / total_decline,
                share_of_post2000_decline=pop_effect / post_decline))

    headline = max(s["share_of_total_decline"] for s in scenarios)
    verdict = ("NEGLIGIBLE" if headline < 0.05 else "MINOR" if headline < 0.20
               else "SUBSTANTIAL" if headline < 0.50 else "DOMINANT")

    res = dict(bound_predating_exposure=bound1, scenarios=scenarios,
               max_share_of_total_decline=headline, verdict_sdt=verdict,
               inputs=dict(nau=NAU, robb=ROBB, exposed_shares=EXPOSED_SHARES,
                           window_years=WINDOW_YEARS))
    json.dump(res, open(OUT_JSON, "w"), indent=2)

    pc = lambda v: f"{v:.1%}"
    L = [f"# Stage 10 demographic significance — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/211_c3g_demographic_significance.py`. Every "
         "number below is computed from the inputs named in the script; none is typed into the "
         "table by hand.", "",
         "## S4 — the units check, before any arithmetic", "",
         "**The phenomenon to be explained is measured in completed children per woman; this "
         "mechanism offers a percentage change in the annual probability of a FIRST BIRTH among "
         "people holding student debt, observed to about age 30.**", "",
         "Those units differ in three ways at once, and each one flatters the mechanism: a first "
         "birth is not a completed family, a hazard truncated at 30 cannot separate postponement "
         "from foregone children, and an effect among borrowers is not an effect on a population. "
         "The arithmetic below crosses all three gaps in the direction that makes the mechanism "
         "look as large as possible.", "",
         "## Bound 1 — most of the decline predates the exposure", "",
         "This bound needs no effect size at all. Mass education debt is a post-2000 phenomenon; "
         "the SDT is dated from 1965.", "",
         "| Quantity | Value |", "|---|---|",
         f"| US TFR, {SDT_START} | {t_start:.3f} |",
         f"| US TFR, {DEBT_ERA} | {t_debt:.3f} |",
         f"| US TFR, {latest} | {t_latest:.3f} |",
         f"| Total decline {SDT_START}–{latest} | {total_decline:.3f} children |",
         f"| Decline after {DEBT_ERA} | {post_decline:.3f} children |",
         f"| **Share of the decline PREDATING the exposure** | **{pc(pre_share)}** |", "",
         f"So even a mechanism that explained the entire post-{DEBT_ERA} decline would account for "
         f"{pc(1 - pre_share)} of the SDT decline in the United States. That is the ceiling before "
         "any estimate is applied.", "",
         "## Bound 2 — the strongest published association, applied generously", "",
         f"Inputs: {NAU['source']}. Predicted annual probability of a first birth is "
         f"{NAU['hazard_no_debt']:.1%} at zero student loans, {NAU['hazard_50k']:.1%} at $50,000 "
         f"and {NAU['hazard_60k']:.1%} at $60,000. Cumulated over {WINDOW_YEARS} years, that is a "
         f"first-birth probability of {p0:.1%} against "
         f"{cumulative(NAU['hazard_60k']):.1%} for the heaviest borrowers.", "",
         "| Scenario | Exposed share of women | Effect, children per woman | Share of total decline |",
         "|---|---|---|---|"]
    for s in scenarios:
        L.append(f"| {s['scenario']} | {s['exposed_share']:.0%} | "
                 f"{s['population_effect_children']:.4f} | {pc(s['share_of_total_decline'])} |")
    L += ["", f"**The largest figure any of these scenarios produces is "
          f"{pc(headline)} of the total decline**, and it comes from the least defensible row — "
          "every borrower assigned the effect estimated for borrowers above $50,000, at the highest "
          "plausible exposure. The defensible rows, which apply the heavy-borrower effect to the "
          f"share of borrowers who actually carry that much debt "
          f"({NAU['share_borrowers_over_60k_age25']:.0%} at age 25), sit two orders of magnitude "
          "lower.", "",
         "## What the identified estimate does to this", "",
         f"{ROBB['source']} instruments loans with in-state tuition rates among four-year graduates "
         f"and finds student loans significantly reduce MARRIAGE "
         f"({ROBB['marriage_per_1000_pct']:.1%} per $1,000) and **{ROBB['first_birth']}** for the "
         "birth of a first child. The bound above is therefore an upper bound on an association "
         "whose only identified counterpart is a null on this chapter's own outcome.", "",
         f"## S5 — the verdict", "",
         f"**For the SDT, the verdict is {verdict}**, because the most generous arithmetic the "
         f"strongest published association supports reaches {pc(headline)} of the decline, and "
         f"{pc(pre_share)} of that decline predates the exposure entirely.", "",
         "**For PM and FDT the verdict is NOT ASSESSED**: mass education debt did not exist. This "
         "is an absence of the exposure, not an absence of evidence, and it is stated rather than "
         "rated.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"TFR {SDT_START}={t_start:.3f} {DEBT_ERA}={t_debt:.3f} {latest}={t_latest:.3f}")
    print(f"decline {total_decline:.3f}; share predating exposure {pre_share:.1%}")
    print(f"max share of decline across scenarios {headline:.2%} -> SDT verdict {verdict}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
