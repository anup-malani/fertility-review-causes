#!/usr/bin/env python3
"""TICK-092 stages 6-7: full-text screen + effect extraction for the D.2.c identified-design core.

Materializes the AI-read primary evidence from the identified-core PDFs held on disk (mirrors
98_a14_extract_core_evidence). Effect values are read from the papers' tables/text with exact source
locators, not derivable from raw data, so they are embedded here with provenance. Nine curated
identified-core PDFs (spanning the three primary cells and the PM/FDT/SDT + regional gradient) were
full-text read by parallel extraction agents on 2026-09-24; each effect carries the D.2.c-specific
fields the synthesis needs: which primary cell, whether the design isolates son preference from
sex-indifferent parity (Wall A.8) and child mortality (Wall A.6), whether the outcome is realized
fertility or the sex-ratio-at-birth substitution expression, the sign RELATIVE TO the D.2.c prediction,
and whether it is poolable.

Full-text screen (stage 6) verdicts, one per study:
  - Dahl & Moretti 2008 (US differential stopping; RES): SURVIVES — the cleanest revealed-stopping design
    (sex of children as-good-as-random); all-girl families 2-5% more likely to have another child;
    reruns the SAME estimand internationally (China +54%, Vietnam +24%, vs US +2-5%) — the magnitude gradient.
  - Almond, Li & Zhang 2013 (China land reform; NBER WP): SURVIVES — land reform x firstborn-girl raises
    P(2nd child male) by 3.0pp (sex selection), a clean first-birth placebo null, and a NULL on fertility:
    here son preference operates via sex selection, not differential continuation. ~58% of 1978-86 rural SRB rise.
  - Anukriti, Bhalotra & Tam 2021 (India; QJE R&R WP): SURVIVES — firstborn-girl families have +0.155 more
    births pre-ultrasound; the gap narrows 40-57% once ultrasound diffuses — differential stopping AND its
    substitution by sex-selective abortion, jointly identified.
  - Jiang et al. 2017 (China SRB by birth order; JBS): SURVIVES (descriptive) — near-normal first-birth SRB
    rising to ~159 at 3rd+ births is the differential-stopping + sex-selection signature; no causal ID, no CIs.
  - Sahni et al. 2008 (Delhi hospital; PLoS ONE): WEAK — second-child SRB after a firstborn girl 716/1000
    (vs ~950), intensifying post-ultrasound; single non-representative hospital, descriptive, selection bias.
  - Fayehun et al. 2011 (Nigeria spacing; AJRH): WEAK — sex-of-preceding-child -> birth interval, national
    effect NULL (OR 0.955 n.s.); confounded with lactational amenorrhoea (A.13). Son preference weak in SSA.
  - Kevane & Levine 2003 (Indonesia; WP): SURVIVES — a documented NULL/ABSENCE of son preference in
    fertility (youngest %boys 0.53 n.s.; family-size ratios ~1; ambiguous spacing). SE-Asian absence.
  - Anukriti 2018 (India Devi Rupak; AEJ:Applied) — CONTEXT: the OA file is the ONLINE APPENDIX only
    (trade-off model + selection tests); the main-paper DD fertility/SRB estimates are on the RA backlog.
  - Iversen & Palmer-Jones 2018 (cable TV; JDS) — CONTEXT: media -> son-preference ATTITUDES (-14pp), no
    norm -> fertility/SRB estimand, underpowered replication of Jensen-Oster.

NOTE ON THE MARQUEE ANCHORS: several canonical D.2.c studies (Ben-Porath & Welch 1976 QJE, Clark 2000
Demography, Arnold-Choe-Roy 1998, Jayachandran 2017 AEJ:Applied VoR, Chung & Das Gupta 2007, Lin-Liu-Qian
2014 JEEA, Ebenstein 2010 JHR) are paywalled and were not OA-retrievable; they are on the RA proxy/ILL
handoff (son-preference-cultural-missing-pdf-dois.csv) and are NOT effect-extracted here. The 667
associational records and the 283 unretrieved identified-core records are the RA extraction backlog (the
A.14/B.1 precedent). The causal core below rests on three strongly-identified quasi-experiments
(Dahl-Moretti, Almond-Li-Zhang, Anukriti-Bhalotra-Tam) plus descriptive mechanism and regional
null/absence evidence — a real and unusually broad base for an interim draft.

Outputs:
  extraction/son-preference-cultural.csv                  (one row per effect; the atomic deliverable)
  extraction/son-preference-cultural-fulltext-screen.csv  (one row per study; stage-6 verdicts)
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EFFECTS = ROOT / "extraction" / "son-preference-cultural.csv"
SCREEN = ROOT / "extraction" / "son-preference-cultural-fulltext-screen.csv"

FIELDS = [
    "effect_id", "study_id", "study", "pdf_filename", "cell", "region", "phenomenon", "estimand",
    "predictor", "outcome", "sample", "period", "design", "isolates_from_parity_A8",
    "isolates_from_mortality_A1", "effect_type", "effect_value", "ci_lower", "ci_upper", "se",
    "direction", "significant", "is_primary_estimate", "poolable", "sign_vs_d2c", "source_locator",
    "source_type", "verified_by", "notes",
]

STUDIES = {
    "dahl_moretti_2008": {
        "study": "Dahl & Moretti (2008), The Demand for Sons, Review of Economic Studies 75(4):1085-1120",
        "pdf": "W2166888609__the-demand-for-sons-evidence-from-divorce-fertility-and-shot.pdf",
        "cell": "PRIMARY_DIFFERENTIAL_STOPPING", "region": "US (+ international)", "phenomenon": "SDT",
    },
    "almond_li_zhang_2013": {
        "study": "Almond, Li & Zhang (2013/2017), Land Reform and Sex Selection in China, NBER WP 19153",
        "pdf": "W1934462296__land-reform-and-sex-selection-in-china.pdf",
        "cell": "PRIMARY_SEXSEL_SUBSTITUTION", "region": "Rural China", "phenomenon": "SDT",
    },
    "anukriti_bhalotra_tam_2021": {
        "study": "Anukriti, Bhalotra & Tam (2021), On the Quantity and Quality of Girls, WP (QJE R&R)",
        "pdf": "W3169860430__on-the-quantity-and-quality-of-girls-fertility-parental-inve.pdf",
        "cell": "PRIMARY_SEXSEL_SUBSTITUTION", "region": "India", "phenomenon": "SDT",
    },
    "jiang_2017": {
        "study": "Jiang, Yu, Yang & Sanchez-Barricarte (2017), Changes in sex ratio at birth in China: a decomposition by birth order, J Biosoc Sci 49(6):826-841",
        "pdf": "W2552766914__changes-in-sex-ratio-at-birth-in-china-a-decomposition-by-bi.pdf",
        "cell": "PRIMARY_DIFFERENTIAL_STOPPING", "region": "China", "phenomenon": "SDT",
    },
    "sahni_2008": {
        "study": "Sahni et al. (2008), Missing Girls in India: Infanticide, Feticide and Made-to-Order Pregnancies, PLoS ONE 3(5):e2224",
        "pdf": "W2023373624__missing-girls-in-india-infanticide-feticide-and-made-to-orde.pdf",
        "cell": "PRIMARY_SEXSEL_SUBSTITUTION", "region": "Delhi, India", "phenomenon": "SDT",
    },
    "fayehun_2011": {
        "study": "Fayehun, Omololu & Isiugo-Abanihe (2011), Sex of preceding child and birth spacing among Nigerian ethnic groups, Afr J Reprod Health 15(2):79-90",
        "pdf": "W1573103718__sex-of-preceding-child-and-birth-spacing-among-nigerian-ethn.pdf",
        "cell": "PRIMARY_DIFFERENTIAL_STOPPING", "region": "Nigeria", "phenomenon": "FDT",
    },
    "kevane_levine_2003": {
        "study": "Kevane & Levine (2003), Changing Status of Daughters in Indonesia, CIDER WP C03-126",
        "pdf": "W2169274775__changing-status-of-daughters-in-indonesia.pdf",
        "cell": "PRIMARY_DIFFERENTIAL_STOPPING", "region": "Indonesia", "phenomenon": "SDT",
    },
    "anukriti_2018_appendix": {
        "study": "Anukriti (2018), Financial Incentives and the Fertility-Sex Ratio Trade-off, AEJ:Applied 10(2):27-57 [ONLINE APPENDIX only retrieved]",
        "pdf": "W2794062870__financial-incentives-and-the-fertility-sex-ratio-trade-off.pdf",
        "cell": "PRIMARY_SEXSEL_SUBSTITUTION", "region": "India (Haryana)", "phenomenon": "SDT",
    },
    "iversen_palmerjones_2018": {
        "study": "Iversen & Palmer-Jones (2018), All You Need is Cable TV?, Journal of Development Studies",
        "pdf": "W2890075677__all-you-need-is-cable-tv.pdf",
        "cell": "PRIMARY_NORM_INTENSITY", "region": "Rural India", "phenomenon": "SDT",
    },
}

# effect rows. Columns:
# (study_id, cell, estimand, predictor, outcome, sample, period, design, isol_A8, isol_A1, eff_type,
#  val, lo, hi, se, direction, sig, primary, poolable, sign_vs_d2c, locator, notes)
E = [
    # ---- Dahl & Moretti 2008 (US differential stopping + international gradient) ----
    ("dahl_moretti_2008", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> P(another birth) via differential stopping",
     "first two children both girls vs both boys", "P(3rd child), families with 2+ children",
     "US Census currently-married mothers 18-40, N=2,326,339", "1940-2000",
     "revealed stopping, sex composition as-good-as-random", "yes", "yes",
     "marginal effect, linear probability", 0.0089, None, None, 0.0009, "supports", True, True, True,
     "+", "Table 8 col (2) p.52",
     "all-boy baseline P=0.382, so +2.34%; the headline US differential-stopping estimate"),
    ("dahl_moretti_2008", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> P(another birth), near-completed fertility",
     "first two children both girls vs both boys", "P(3rd child), families with 2+ children",
     "Longitudinal CA birth certificates, N=231,811", "1989-2001",
     "revealed stopping, longitudinal near-completed fertility", "yes", "yes",
     "marginal effect, linear probability", 0.0126, None, None, 0.0026, "supports", True, False, True,
     "+", "Table 9 col (2) p.54",
     "baseline 0.308, +4.08%; larger than Census because fertility is near-complete"),
    ("dahl_moretti_2008", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> P(another birth), cleanest identification",
     "3rd child girl vs boy conditional on first two = Girl,Boy (GBG vs GBB; 3rd sex random)",
     "P(4th child)", "US Census", "1940-2000",
     "revealed stopping, conditional on sib-sex order (least endogenous)", "yes", "yes",
     "difference in marginal effects", 0.0069, None, None, None, "supports", True, False, False,
     "+", "Table 8 col (3) p.52 / text p.25",
     "the least-endogenous estimate; combined SE not reported so not poolable"),
    ("dahl_moretti_2008", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> P(another birth), CHINA (international extension)",
     "first two children both girls vs both boys", "P(3rd child), families with 2+ children",
     "China census microdata", "c.1990s", "revealed stopping (same estimand as US)", "yes", "yes",
     "marginal effect, linear probability", 0.1990, None, None, 0.0061, "supports", True, False, True,
     "+", "Table 14 p.60",
     "baseline 0.365, +54%; the magnitude gradient — Asia an order of magnitude above the US"),
    ("dahl_moretti_2008", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> P(another birth), VIETNAM (international extension)",
     "first two children both girls vs both boys", "P(3rd child)", "Vietnam census", "c.1990s",
     "revealed stopping (same estimand as US)", "yes", "yes",
     "marginal effect, linear probability", 0.0871, None, None, None, "supports", True, False, False,
     "+", "Table 14 p.60", "baseline 0.4875; Mexico +2.30pp, Kenya +2.02pp, Colombia +0.50pp reported too"),
    ("dahl_moretti_2008", "PRIMARY_NORM_INTENSITY",
     "son preference norm intensity (stated preference)", "respondent is male vs female",
     "P(states preference for a boy | has a preference)", "Gallup 2000/2003 US, N=1,325", "2000-2003",
     "probit on stated preference", "n/a", "n/a", "probit marginal effect", 0.2335, None, None, None,
     "supports", True, False, False, "+", "Table 11 p.57",
     "the demand for sons is father-driven; corroborates but does not measure realized fertility"),

    # ---- Almond, Li & Zhang 2013 (China land reform -> sex selection; fertility null) ----
    ("almond_li_zhang_2013", "PRIMARY_SEXSEL_SUBSTITUTION",
     "son preference (economic value of sons) -> sex ratio at birth via sex selection",
     "land reform x first child is girl", "P(2nd child is male | first is girl)",
     "914 rural counties, 1% 1990 Census", "births 1974-1986; reform 1978-1984",
     "county event-study / DiD (natural experiment)", "yes", "yes",
     "LPM effect on fraction male", 0.030, 0.0222, 0.0378, 0.004, "supports-substitution", True, True,
     False, "+", "Table 1 Panel B col (2) p.13",
     "+3.0pp probability 2nd child male after a firstborn girl; LPM on fraction-male, not log-SRB, so not directly poolable"),
    ("almond_li_zhang_2013", "PRIMARY_SEXSEL_SUBSTITUTION",
     "placebo: sex selection at first birth (should be null)", "land reform x event time, first child",
     "P(first child male)", "914 rural counties", "1974-1986", "county event-study placebo", "yes",
     "yes", "trend break in fraction male", -0.001, -0.0029, 0.0010, 0.001, "null", False, False,
     False, "0", "Table 1 Panel A col (1) p.13",
     "no sex selection at first birth (not subject to son preference given stopping) — validates design"),
    ("almond_li_zhang_2013", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> differential fertility continuation (should be null here)",
     "land reform x first child is girl", "ln(number of second births)",
     "914 rural counties", "1974-1986", "OLS county-by-year", "yes", "yes",
     "OLS coefficient (log births)", -0.027, -0.0976, 0.0436, 0.036, "null", False, True, False,
     "0", "Table 3 col (3) p.17",
     "KEY NULL: land reform raises sex selection but NOT differential continuation — son preference here works through the sex ratio, not extra births (regime-dependence)"),
    ("almond_li_zhang_2013", "PRIMARY_SEXSEL_SUBSTITUTION",
     "aggregate demographic contribution", "land reform (economic value of sons)",
     "share of 1978-86 rural sex-ratio rise attributable to land reform", "rural China", "1978-1986",
     "decomposition", "yes", "yes", "share of aggregate SRB change", 0.58, None, None, None,
     "supports-substitution", True, False, False, "+", "text p.15 / fn 19",
     "~58% of the 1978-86 rise in rural sex ratios (~1 million missing girls); derived quantity, no SE"),

    # ---- Anukriti, Bhalotra & Tam 2021 (India: differential stopping + substitution) ----
    ("anukriti_bhalotra_tam_2021", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> realized fertility via differential stopping (pre-ultrasound)",
     "firstborn girl (quasi-random)", "number of births (completed sibling size)",
     "NFHS + REDS, India", "1973-1984 (pre-ultrasound)", "DDD / DiD (firstborn sex x ultrasound shocks)",
     "yes", "partly", "OLS coefficient (births)", 0.155, None, None, 0.012, "supports", True, True,
     True, "+", "Table 6 col (1) p.43",
     "firstborn-girl families have +0.155 more births (baseline 3.001); headline 0.189 with preference controls (col 3)"),
    ("anukriti_bhalotra_tam_2021", "PRIMARY_SEXSEL_SUBSTITUTION",
     "attenuation of the stopping effect by sex selection (early ultrasound diffusion)",
     "firstborn girl x Post1 (1985-1994 ultrasound imports)", "number of births",
     "NFHS + REDS, India", "1985-1994", "DDD", "yes", "partly", "OLS interaction (births)", -0.088,
     None, None, 0.016, "supports-substitution", True, True, True, "+", "Table 6 col (1) p.43",
     "son-biased fertility gap narrows ~57% after ultrasound imports — substitution of sex selection for extra births"),
    ("anukriti_bhalotra_tam_2021", "PRIMARY_SEXSEL_SUBSTITUTION",
     "attenuation of the stopping effect by sex selection (late ultrasound diffusion)",
     "firstborn girl x Post2 (1995-2005 local production)", "number of births",
     "NFHS + REDS, India", "1995-2005", "DDD", "yes", "partly", "OLS interaction (births)", -0.112,
     None, None, 0.018, "supports-substitution", True, False, True, "+", "Table 6 col (1) p.43",
     "larger attenuation in high-availability late period; pre-ultrasound gap declined 40-50% overall"),
    ("anukriti_bhalotra_tam_2021", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> UNDESIRED (excess) fertility",
     "firstborn girl", "excess fertility (births minus ideal number of children)", "NFHS, India",
     "1973-1984", "DDD", "yes", "partly", "OLS coefficient (births)", 0.115, None, None, 0.043,
     "supports", True, False, True, "+", "Table 6 col (5) p.43",
     "baseline 0.451; undesired fertility gap declined ~74% after ultrasound — the welfare-relevant channel"),

    # ---- Jiang et al. 2017 (China SRB by birth order — descriptive mechanism) ----
    ("jiang_2017", "PRIMARY_DIFFERENTIAL_STOPPING",
     "differential-stopping + sex-selection signature (birth-order SRB gradient)",
     "birth order (1st vs 2nd vs 3rd+), given no prior son", "sex ratio at birth (males per 100 females)",
     "China national census/survey", "2000", "descriptive decomposition (no causal ID)", "yes", "n/a",
     "SRB level by birth order", "SRB1=107; SRB2=152; SRB3+=159", None, None, None, "supports", None,
     True, False, "+", "Table 2 p.830 (2000 Total)",
     "near-normal first-birth SRB rising steeply at higher orders = canonical differential-stopping+sexsel signature; descriptive, no CI/SE, not poolable"),
    ("jiang_2017", "PRIMARY_DIFFERENTIAL_STOPPING",
     "pre-ultrasound baseline (mechanism dating)", "birth order 3rd+ given no prior son, 1981",
     "sex ratio at birth", "China national", "1981", "descriptive", "yes", "n/a", "SRB level",
     "SRB3+=112.6", None, None, None, "supports", None, False, False, "+", "Table 2 p.830 (1981 Total)",
     "1981 gradient is mild (SRB1=105, SRB3+=113) — differential stopping without sex selection before ultrasound; contrast with 2000 dates the sex-selection mechanism"),

    # ---- Sahni et al. 2008 (Delhi hospital — WEAK) ----
    ("sahni_2008", "PRIMARY_SEXSEL_SUBSTITUTION",
     "son preference + sex selection -> low SRB of 2nd child after a firstborn girl",
     "first child is a girl", "sex ratio at birth of 2nd child (girls per 1000 boys)",
     "St Stephens Hospital Delhi, N=3,987 second births", "1905-2005",
     "single-hospital descriptive time-series (selection bias)", "n/a", "n/a",
     "sex ratio (girls per 1000 boys)", 716, 672, 762, None, "supports", True, True, False, "+",
     "Table 4 all-years col B (P<0.001)",
     "vs overall 910; strong son-preference signature but single non-representative hospital — WEAK"),
    ("sahni_2008", "PRIMARY_SEXSEL_SUBSTITUTION",
     "intensification of sex selection after ultrasound", "first child a girl, 1994-95 vs 1974-75",
     "sex ratio at birth of 2nd child (girls per 1000 boys)", "St Stephens Hospital Delhi",
     "1974-75 vs 1994-95", "descriptive time contrast", "n/a", "n/a", "sex ratio (girls per 1000 boys)",
     "610 (1994-95) vs 754 (1974-75)", None, None, None, "supports-substitution", True, False, False,
     "+", "Table 4 year rows B",
     "deficit of female second births after a firstborn girl deepened in the ultrasound era"),

    # ---- Fayehun et al. 2011 (Nigeria spacing — WEAK / null) ----
    ("fayehun_2011", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> shorter interval after a girl (spacing test)",
     "sex of preceding child = female vs male", "odds of longer preceding birth interval (>=24mo)",
     "2008 Nigeria DHS, N=22,752 parity-2+ births", "2003-2008", "logistic, cross-sectional", "partly",
     "yes", "adjusted odds ratio", 0.955, None, None, None, "null", False, True, False, "0",
     "Table 5 Model 4 p.86",
     "national effect null (OR<1 in the son-preference direction but n.s.); confounded with lactational amenorrhoea (A.13). Son preference weak in sub-Saharan Africa"),

    # ---- Kevane & Levine 2003 (Indonesia — SURVIVES as documented null) ----
    ("kevane_levine_2003", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> stopping (test: youngest child more likely a boy)",
     "sex of youngest child among mothers reporting completed fertility",
     "proportion of youngest children who are boys (benchmark 0.5125)", "IFLS Indonesia, N=1,976",
     "1990s cohort", "descriptive stopping test (complex-survey Wald)", "yes", "yes",
     "proportion boys", 0.53, None, None, None, "null", False, True, False, "0",
     "Table 3 p.31 (1990s completed-fertility cohort)",
     "not significantly above the 0.5125 benchmark; documented ABSENCE of stopping-based son preference in Indonesia (SE-Asian null)"),
    ("kevane_levine_2003", "PRIMARY_DIFFERENTIAL_STOPPING",
     "son preference -> girls accumulate in larger families (test)",
     "ratio of family size for boys vs girls", "family-size ratio (son preference predicts <1)",
     "IFLS Indonesia, N=2,341", "1990s cohort", "descriptive", "yes", "yes", "ratio", 1.02, None, None,
     None, "null", False, False, False, "0", "Table 4 p.32 (ever-married mothers)",
     "ratio ~1 => no tendency for girls to be in larger families; null. Only significant family-size cell (siblings, 1.04) is in the WRONG direction for son preference"),

    # ---- Anukriti 2018 appendix (CONTEXT — norm-intensity correlation) ----
    ("anukriti_2018_appendix", "PRIMARY_NORM_INTENSITY",
     "son-preference intensity correlated with fertility (cross-sectional context)",
     "high- vs low-son-preference socioeconomic groups",
     "proportion sons (0.578 vs 0.524) and number of children (2.25 vs 3.05)", "NFHS-2 India",
     "1998-99", "cross-sectional correlation (appendix Table 1)", "no", "no",
     "group means (context, not causal)", "prop sons 0.578 vs 0.524; children 2.25 vs 3.05", None, None,
     None, "supports", None, False, False, "+", "Online Appendix Table 1",
     "CONTEXT ONLY: the OA file is the online appendix; the main-paper DD fertility/SRB estimates are on the RA backlog. Higher-son-preference groups have more sons and fewer children (substitution pattern)"),

    # ---- Iversen & Palmer-Jones 2018 (CONTEXT — media -> attitudes) ----
    ("iversen_palmerjones_2018", "PRIMARY_NORM_INTENSITY",
     "media exposure -> son-preference ATTITUDE (a determinant of the norm, not the estimand)",
     "village has cable TV", "P(states preference for next child = boy)",
     "SARI panel rural India, N=1,699", "2001-2003", "panel FE (replication of Jensen-Oster)", "n/a",
     "n/a", "panel FE coefficient (pp)", -0.14, None, None, 0.068, "null", True, False, False, "0",
     "Table 5 p.10",
     "CONTEXT: media can move son-preference attitudes (-14pp), but no norm->fertility/SRB estimand and severely underpowered; direction coded null w.r.t. the D.2.c estimand"),
]

SCREEN_ROWS = [
    ("dahl_moretti_2008", "SURVIVES", "identified",
     "cleanest revealed-stopping design (sex as-good-as-random); US +2-5%, reruns same estimand internationally (China +54%)"),
    ("almond_li_zhang_2013", "SURVIVES", "identified",
     "land reform x firstborn-girl -> +3.0pp P(2nd male); clean first-birth placebo; NULL on fertility (works via sex selection here)"),
    ("anukriti_bhalotra_tam_2021", "SURVIVES", "identified",
     "firstborn-girl -> +0.155 births; gap narrows 40-57% as ultrasound diffuses — stopping + substitution jointly identified"),
    ("jiang_2017", "SURVIVES", "descriptive",
     "birth-order SRB gradient (107 -> 159) is the differential-stopping + sex-selection signature; descriptive, no causal ID"),
    ("sahni_2008", "WEAK", "descriptive",
     "2nd-child SRB after firstborn girl 716/1000, intensifying post-ultrasound; single non-representative hospital, selection bias"),
    ("fayehun_2011", "WEAK", "observational",
     "sex-of-preceding-child -> interval; national NULL (OR 0.955 n.s.); confounded with A.13; son preference weak in SSA"),
    ("kevane_levine_2003", "SURVIVES", "observational",
     "documented NULL/ABSENCE of son preference in fertility in Indonesia (youngest %boys 0.53 n.s.; family-size ratios ~1)"),
    ("anukriti_2018_appendix", "CONTEXT", "theory",
     "OA file is the online appendix (trade-off model + selection tests); main-paper DD estimates on the RA backlog"),
    ("iversen_palmerjones_2018", "CONTEXT", "quasi-experimental",
     "media -> son-preference attitudes (-14pp); no norm->fertility estimand; underpowered replication"),
]


def main() -> None:
    EFFECTS.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, e in enumerate(E, 1):
        (sid, cell, estimand, predictor, outcome, sample, period, design, isol_a8, isol_a1, etype,
         val, lo, hi, se, direction, sig, primary, poolable, sign, locator, notes) = e
        s = STUDIES[sid]
        rows.append({
            "effect_id": f"d2c_{i:03d}", "study_id": sid, "study": s["study"], "pdf_filename": s["pdf"],
            "cell": cell, "region": s["region"], "phenomenon": s["phenomenon"], "estimand": estimand,
            "predictor": predictor, "outcome": outcome, "sample": sample, "period": period,
            "design": design, "isolates_from_parity_A8": isol_a8, "isolates_from_mortality_A1": isol_a1,
            "effect_type": etype, "effect_value": val, "ci_lower": lo, "ci_upper": hi, "se": se,
            "direction": direction, "significant": sig, "is_primary_estimate": primary,
            "poolable": poolable, "sign_vs_d2c": sign, "source_locator": locator,
            "source_type": "pdf_table_or_text", "verified_by": "ai_extraction_agent_2026-09-24",
            "notes": notes,
        })
    with open(EFFECTS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    with open(SCREEN, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["study_id", "study", "pdf_filename", "cell", "region", "phenomenon",
                    "fulltext_screen", "evidence_type", "screen_reason"])
        for sid, verdict, evtype, reason in SCREEN_ROWS:
            s = STUDIES[sid]
            w.writerow([sid, s["study"], s["pdf"], s["cell"], s["region"], s["phenomenon"],
                        verdict, evtype, reason])

    n_surv = sum(1 for r in SCREEN_ROWS if r[1] == "SURVIVES")
    n_weak = sum(1 for r in SCREEN_ROWS if r[1] == "WEAK")
    n_ctx = sum(1 for r in SCREEN_ROWS if r[1] == "CONTEXT")
    print(f"wrote {EFFECTS.relative_to(ROOT)} ({len(rows)} effects)")
    print(f"wrote {SCREEN.relative_to(ROOT)} ({len(SCREEN_ROWS)} studies: "
          f"{n_surv} SURVIVES, {n_weak} WEAK, {n_ctx} CONTEXT)")


if __name__ == "__main__":
    main()
