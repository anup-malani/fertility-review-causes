#!/usr/bin/env python3
"""Risk-of-bias assessment for the C.2.c identified core (TICK-055).

Domain set follows the house pattern, with TWO domains added that the scope doc argued this
hypothesis specifically needs:

  exclusion_restriction -- for C.2.c the instruments are the weak point, not the first stage. Supply
      elasticity, construction costs, and land prices all plausibly affect fertility through channels
      other than house prices. The scope predicted the RoB pass would concentrate here, and it does.
  endogenous_tenure -- the tenure split that makes an estimate interpretable conditions on a variable
      chosen in anticipation of childbearing (scope doc, Consequence 2). Pre-determined tenure is
      materially better than contemporaneous, and is graded as such.
  anticipatory_sorting -- households move in anticipation of births; area-level price variation is
      contaminated by exactly the outcome under study.

Ratings: low / moderate / serious / critical.
"""
import csv

# study: (confounding, exclusion, anticipatory_sorting, endogenous_tenure, measurement_exposure,
#         measurement_outcome, reporting, overall, rationale)
ROB = {
    "W4400391089": ("low", "n/a (RD)", "low", "moderate", "low", "low", "low", "LOW",
        "Strongest design in the pool. RD on a 2006 policy cutoff with placebo tests at alternative "
        "cutoffs and restricted bandwidths. No instrument, so no exclusion restriction to violate. "
        "ENDOGENOUS TENURE moderate: the sample is households that purchased before 2006, so the "
        "estimate is for owners and does not identify the cost channel. External validity is local to "
        "the cutoff."),
    "W3024244835": ("low", "moderate", "moderate", "low", "low", "low", "low", "MODERATE",
        "The reference study. EXCLUSION moderate: supply-elasticity instruments identify off "
        "topographically constrained MSAs, which differ from elastic ones in industry mix, amenities "
        "and female labour markets; MSA fixed effects and time-varying controls mitigate but do not "
        "close this. ENDOGENOUS TENURE low, and this is a genuine strength -- ownership is measured at "
        "BASELINE and held time-invariant, so it is pre-determined with respect to the price shock. "
        "ANTICIPATORY SORTING moderate: MSA-level aggregation limits individual sorting but does not "
        "remove selective migration into high-price metros."),
    "W3037455063": ("low", "moderate", "low", "serious", "low", "low", "low", "MODERATE",
        "Best measurement in the pool -- Danish population registers, 1.1m observations, outcome is a "
        "register birth. EXCLUSION moderate: uses the price change of the FIRST home purchased, which "
        "removes endogenous moving but still requires that municipal price movements are unrelated to "
        "local fertility determinants. ENDOGENOUS TENURE serious, and the authors say so themselves: "
        "'women in our sample are likely to have a higher fertility rate than the average population "
        "due to selection into home ownership prior to the decision to have a child.' The estimate is "
        "internally credible for owners and does not transport to renters or prospective buyers."),
    "W3023795878": ("moderate", "serious", "moderate", "moderate", "moderate", "moderate", "moderate", "SERIOUS",
        "EXCLUSION serious: an IV strategy is asserted but the instrument's exclusion restriction is "
        "not defended in any depth, and Chinese city-level price movements co-move with land-sale "
        "revenue, migration and local labour demand -- all fertility-relevant. Tenure split is "
        "movers-vs-non-movers rather than owners-vs-renters, which is not the split the pooling rule "
        "needs."),
    "W4399107829": ("moderate", "critical", "low", "n/a", "serious", "moderate", "low", "SERIOUS",
        "THE ONLY IDENTIFIED FDT-PERIOD ESTIMATE, and its instruments are its weakest point. "
        "EXCLUSION critical: house prices are instrumented with CONSTRUCTION COSTS and LAND PRICES. "
        "Land prices are close to the same object as house prices rather than an external shifter, and "
        "construction costs move with wages, materials and the business cycle -- all of which affect "
        "fertility directly. MEASUREMENT serious: a 1870-2012 cross-country house-price series carries "
        "enormous definitional heterogeneity across countries and eras. The finding is valuable as the "
        "only long-run evidence; it should not be read as cleanly identified."),
    "W4395680672": ("moderate", "moderate", "low", "n/a", "moderate", "low", "moderate", "MODERATE",
        "Policy DiD on house purchase restrictions with treated/control prefectures and a spatial-decay "
        "spillover treatment. CONFOUNDING moderate: HPR was imposed on cities with the hottest markets, "
        "so treatment is selected on price dynamics; the design handles this partially through the "
        "comparison with unregulated prefectures. Not peer-reviewed (SSRN), which limits scrutiny but "
        "is not itself a bias domain."),
    "W3121393843": ("moderate", "serious", "moderate", "moderate", "moderate", "moderate", "moderate", "SERIOUS",
        "EXCLUSION serious: initial-area house prices instrument prices for movers, but where a "
        "household starts is not random with respect to its fertility plans. The IV estimate (+11.8% "
        "odds) is roughly six times the OLS estimate (+2.0%), a gap large enough to suggest a weak or "
        "invalid instrument rather than the removal of attenuation bias, and the paper does not resolve "
        "this. Valuable because it reports a tenure split, which few do."),
    "W3144108245": ("serious", "n/a", "serious", "n/a", "serious", "serious", "critical", "CRITICAL",
        "REPORTING critical: the effect is reported as 'birth rates dropped roughly 5.45 unit' with the "
        "unit never defined; the authors describe their own coefficients as 'unlikely and ambiguous' "
        "and ask readers to replicate the work to obtain 'a more accurate and unbiased result'; and the "
        "paper misquotes Dettling & Kearney. Conference proceedings, not peer-reviewed. RECOMMEND "
        "EXCLUSION from the synthesis -- consistent with the demotion already recommended at "
        "extraction pass 2."),
}

study = {r["work_id"]: r for r in csv.DictReader(open("extraction/housing-costs-study-extraction.csv"))}
out = "extraction/housing-costs-risk-of-bias.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["work_id", "short_cite", "year", "design", "confounding", "exclusion_restriction",
                "anticipatory_sorting", "endogenous_tenure", "measurement_exposure",
                "measurement_outcome", "reporting", "overall", "rationale", "ra_verified"])
    for wid, v in ROB.items():
        s = study.get(wid, {})
        w.writerow([wid, s.get("title", "")[:52], s.get("year", ""), s.get("design", "")[:60],
                    *v, "no"])

from collections import Counter
c = Counter(v[7] for v in ROB.values())
print(f"risk of bias -> {out}\n")
for k in ("LOW", "MODERATE", "SERIOUS", "CRITICAL"):
    if c.get(k):
        print(f"  {c[k]:>2}  {k}")
print(f"\nexclusion_restriction domain: "
      f"{dict(Counter(v[1] for v in ROB.values()))}")
