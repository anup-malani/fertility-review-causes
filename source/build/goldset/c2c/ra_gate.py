#!/usr/bin/env python3
"""RA gate for the C.2.c PRIMARY strata — human verdicts, keyed on title prefix.

The automated screen labels a paper by what it MENTIONS. The gate decides what it IDENTIFIES OFF,
which is the only thing the 2026-07-31 price-variation ruling cares about. Verdicts here were made by
reading title + abstract for every record in the stratum, not by a rule.

Verdict vocabulary:
  KEEP_<cell>          -- identifies off the stated treatment; stays in the primary pool
  DEMOTE_TENURE        -- treatment is homeownership STATUS, not a price. Real housing variable, but
                          not price variation, so it leaves the primary pool under the ruling. Kept in
                          the chapter as context: tenure is chosen in anticipation of children, so
                          these are also part of the endogeneity story.
  OUT_NO_FERT_OUTCOME  -- outcome is homeownership / longevity / housing structure, not fertility
  OUT_OTHER            -- treatment is not a housing variable at all
  THEORY               -- typology or model, no identified estimate; theory stream

Rent stratum note: "renter" as a SAMPLE DESCRIPTOR is not rent-identification. Only papers where the
rent level or a rent-assigning policy is the source of variation stay.
"""
import csv
import json

SRC = "literature/search-logs/housing-costs-screen-pass2.json"
OUT = "extraction/housing-costs-ra-gate.csv"

# title-prefix (lowercased, first ~46 chars) -> (verdict, reason)
VERDICTS = {
    # ---------------- rent stratum (16 screened) ----------------
    "do higher rents discourage fertility": ("KEEP_PRIMARY_COST_RENT_IDENTIFIED", "rent level is the treatment; US cities 1940-2000; no wealth offset, no tenure split needed"),
    "the effect of the price or rental cost of housin": ("KEEP_PRIMARY_COST_RENT_IDENTIFIED", "rental cost as treatment, explicit income vs substitution decomposition"),
    "the effect of public rental housing on birth int": ("KEEP_PRIMARY_COST_RENT_IDENTIFIED", "policy-assigned rental housing; plausibly exogenous rent"),
    "working from home, land rents, and fertility": ("KEEP_PRIMARY_COST_RENT_IDENTIFIED", "land rents as treatment"),
    "housing and fertility: a macro-level, multi-coun": ("DEMOTE_TENURE", "renters are one subgroup; macro tenure composition, not a rent treatment"),
    "the influence of housing on family size in south": ("DEMOTE_TENURE", "rent appears as a tenure category, not a price"),
    "housing context and childbearing in sweden": ("KEEP_PRIMARY_SPACE_QUANTITY", "rental apartment is a housing TYPE here; belongs in the space/type cell"),
    "factors influencing fertility intentions of newl": ("DEMOTE_TENURE", "rental household as a sample category"),
    "perceptions of housing stability and fertility i": ("DEMOTE_TENURE", "public-housing renters are the sample frame; treatment is perceived stability"),
    "the long-term consequences of youth housing for": ("KEEP_PRIMARY_COST_RENT_IDENTIFIED", "allocation of a rental apartment is the treatment; policy variation"),
    "do long commutes discourage fertility intentions": ("OUT_OTHER", "treatment is commute time, not housing price or rent"),
    "housing expenditure and births in italy": ("KEEP_PRIMARY_COST_RENTER", "expenditure treatment bundling rent+mortgage; a cost measure, not rent-identified"),
    "the trifecta of adulthood": ("DEMOTE_TENURE", "rental home as a life-course state"),
    "parental financial support for housing": ("OUT_OTHER", "treatment is parental transfer; renters are the comparison group"),
    "fertility intention and household consumption pa": ("DEMOTE_TENURE", "rental setting is context; treatment is consumption pattern"),
    # ---------------- wealth stratum (28 screened) ----------------
    "housing wealth, fertility intentions and fertili": ("KEEP_PRIMARY_WEALTH_OWNER", "housing wealth as treatment; HILDA"),
    "housing wealth and fertility: evidence from chin": ("KEEP_PRIMARY_WEALTH_OWNER", "housing wealth as treatment"),
    "housing wealth, fertility and children's health": ("KEEP_PRIMARY_WEALTH_OWNER", "RD design; among the stronger identifications in the pool"),
    "impacts of housing booms on fertility in china": ("KEEP_PRIMARY_WEALTH_OWNER", "explicitly separates wealth effect from cost effect by tenure"),
    "the effects of housing wealth on fertility decis": ("KEEP_PRIMARY_WEALTH_OWNER", "housing bust; change in home value as treatment; Japan"),
    "the asymmetric housing wealth effect on childbir": ("KEEP_PRIMARY_WEALTH_OWNER", "directly on the tenure asymmetry the pooling rule is built around; priority read"),
    "housing wealth and fertility: australian evidenc": ("KEEP_PRIMARY_WEALTH_OWNER", "geographic variation in house price changes"),
    "housing wealth, fertility, and child quality": ("KEEP_PRIMARY_WEALTH_OWNER", "housing wealth to fertility and child investment; QQ margin"),
    "the effect of housing wealth on fertility among": ("KEEP_PRIMARY_WEALTH_OWNER", "Korean panel, home-owning households; Korean-language"),
    "two-child policy, housing wealth stratification": ("KEEP_PRIMARY_WEALTH_OWNER", "housing wealth stratification as treatment"),
    "no flat, no child in singapore": ("KEEP_PRIMARY_WEALTH_OWNER", "macro cointegration via housing wealth formation; weak identification, keep flagged"),
    "the changing association between homeownership a": ("DEMOTE_TENURE", "treatment is ownership status, not price or wealth"),
    "homeownership and fertility intentions among mig": ("DEMOTE_TENURE", "ownership status as treatment"),
    "homeownership pathways and fertility in urban ch": ("DEMOTE_TENURE", "tenure pathway as treatment"),
    "the interconnection of homeownership, marriage a": ("DEMOTE_TENURE", "joint life-course states, no price variation"),
    "homeownership and transition to parenthood in it": ("DEMOTE_TENURE", "ownership status as treatment"),
    "living arrangement and homeownership impacts on": ("DEMOTE_TENURE", "ownership status plus living arrangement; also A.23 adjacent"),
    "the effect of financial resources on homeownersh": ("OUT_OTHER", "treatment is a financial-resource shock; homeownership is an OUTCOME here, routes to C.1.a/C.3.e"),
    "homeownership regimes and low fertility": ("THEORY", "regime typology; no identified estimate. Theory stream, does not count toward empirical recall"),
    "the death and life of private landlordism": ("OUT_NO_FERT_OUTCOME", "housing tenure structure; no fertility outcome"),
    "family formation, parental background and young": ("OUT_NO_FERT_OUTCOME", "outcome is entry into homeownership, not fertility"),
    "baby-boomers, baby-busters and the lost generati": ("OUT_NO_FERT_OUTCOME", "generational housing access; no fertility estimate"),
    "intergenerational financial transfers and indire": ("OUT_NO_FERT_OUTCOME", "outcome is homeownership reproduction"),
    "homeownership out of reach?": ("OUT_NO_FERT_OUTCOME", "outcome is homeownership access"),
    "generational variations in the timing of entry i": ("OUT_NO_FERT_OUTCOME", "outcome is homeownership entry timing"),
    "us baby boomers' homeownership trajectories": ("OUT_NO_FERT_OUTCOME", "outcome is ownership trajectory"),
    "comparing regional patterns of homeownership ent": ("OUT_NO_FERT_OUTCOME", "outcome is homeownership entry"),
    "the longevity benefits of homeownership": ("OUT_OUTCOME_HEALTH", "outcome is longevity"),
}

def norm(t):
    """Curly vs straight apostrophes silently broke one prefix match. Normalise both sides."""
    return (t or "").lower().replace("\u2019", "'").replace("\u2018", "'")


frame = json.load(open(SRC))
rows, matched = [], set()
for r in frame:
    t = norm(r["title"])
    verdict = reason = ""
    for pref, (v, why) in VERDICTS.items():
        if t.startswith(norm(pref)):
            verdict, reason = v, why
            matched.add(pref)
            break
    if verdict:
        rows.append((r, verdict, reason))

with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["doi", "openalex", "year", "venue", "title", "screen_cell",
                "ra_verdict", "ra_reason", "gated_by", "gated_date"])
    for r, v, why in sorted(rows, key=lambda x: x[1]):
        w.writerow([r["doi"], r["openalex"], r["year"], r["venue"], r["title"],
                    r["provisional_cell"], v, why, "Shravan/Claude", "2026-07-31"])

from collections import Counter
c = Counter(v for _, v, _ in rows)
print(f"gated: {len(rows)} records (rent + wealth strata)")
for v, n in c.most_common():
    print(f"  {n:>3}  {v}")
unmatched = set(VERDICTS) - matched
if unmatched:
    print(f"\nWARNING - verdict keys that matched nothing ({len(unmatched)}):")
    for u in sorted(unmatched):
        print(f"    {u}")
kept = sum(n for v, n in c.items() if v.startswith("KEEP"))
print(f"\nsurviving primary from these two strata: {kept} (screen had labelled 44)")
print(f"gate -> {OUT}")
