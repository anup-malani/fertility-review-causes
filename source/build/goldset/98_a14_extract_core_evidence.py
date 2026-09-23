#!/usr/bin/env python3
"""TICK-091 stages 6-7: full-text screen + effect extraction for the A.14 identified-design core.

Materializes the AI-read primary evidence from the identified-core PDFs held on disk (mirrors
65_c2h_extract_core_evidence / 83_extract_shanan_primary_evidence — effect values are read from the
papers' tables/text with exact source locators, not derivable from raw data, so they are embedded here
with provenance). Seven identified-core PDFs were full-text read by parallel extraction agents on
2026-09-23; each effect carries the A.14-specific fields the synthesis needs: which primary cell, whether
the spec holds contraception fixed (the load-bearing Wall 1) and age (Wall 4), the sign RELATIVE TO the
A.14 prediction, and whether it is poolable.

Full-text screen (stage 6) verdicts, one per study:
  - Nie 2020 (spousal separation-reunification, China): SURVIVES — strong support, no reunification catch-up.
  - Clifford 2009 (spousal separation, Tajikistan): SURVIVES — selection-corrected; naive models underestimate.
  - Bouchard/Fehring/Schneider 2018 (fertile-window, N=256): SURVIVES — the biometric timing slope (85 vs 1).
  - Mturi 1997 (non-contracepting birth intervals, Tanzania): WEAK/PARTIAL — abstinence confounded with
    lactational amenorrhoea (A.13); only indirect polygamy/absence proxies isolate A.14.
  - Pleasure&Pregnancy RCT 2022 (Netherlands): NULL + FAILED MANIPULATION — the intervention did not raise
    coital frequency, so it is a null test of the whole chain, not a clean slope estimate. Non-confirmatory.
  - Koo 2018 (timed coitus, Korea): FAILS — timed coitus applied uniformly; predictor is AMH/ovarian
    reserve (A.15), not coital exposure. Zero A.14 effects.
  - Moriki 2012 (sexless marriage, Japan): MECHANISM/CONTEXT — descriptive sexless prevalence + a CITED
    Bongaarts-Potter fecundability model; no original effect estimate. Feeds the SDT mechanism section.

NOTE ON THE MARQUEE ANCHORS: the canonical A.14 studies (Barrett-Marshall 1969, Wilcox 1995, Caldwell &
Caldwell 1977, Lindstrom-Saucedo 2002, Twenge 2017) are OLD/paywalled and were not OA-retrievable; they
are on the RA proxy/ILL handoff (coital-frequency-biological-missing-pdf-dois.csv) and are NOT
effect-extracted here. The causal core below therefore rests on two spousal-separation quasi-experiments
plus the biometric timing evidence — a real but partial base (the B.1 precedent).

Outputs:
  extraction/coital-frequency-biological.csv                  (one row per effect; the atomic deliverable)
  extraction/coital-frequency-biological-fulltext-screen.csv  (one row per study; stage-6 verdicts)
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EFFECTS = ROOT / "extraction" / "coital-frequency-biological.csv"
SCREEN = ROOT / "extraction" / "coital-frequency-biological-fulltext-screen.csv"

FIELDS = [
    "effect_id", "study_id", "study", "pdf_filename", "cell", "estimand", "predictor", "outcome",
    "sample", "period", "design", "adjusts_contraception", "adjusts_age", "effect_type",
    "effect_value", "ci_lower", "ci_upper", "se", "direction", "significant", "is_primary_estimate",
    "poolable", "sign_vs_a14", "source_locator", "source_type", "verified_by", "notes",
]

STUDIES = {
    "nie_2020_fujian": {
        "study": "Nie (2020), Effect of spousal separation and reunification on fertility, Demographic Research 43(29)",
        "pdf": "W3086522635__the-effect-of-spousal-separation-and-reunification-on-fertil.pdf",
        "cell": "PRIMARY_SEPARATION_SHOCK",
    },
    "clifford_2009_tajikistan": {
        "study": "Clifford (2009), Spousal separation, selectivity and contextual effects, Demographic Research 21(32)",
        "pdf": "W2012967441__spousal-separation-selectivity-and-contextual-effects-explor.pdf",
        "cell": "PRIMARY_SEPARATION_SHOCK",
    },
    "bouchard_2018_marquette": {
        "study": "Bouchard, Fehring & Schneider (2018), Achieving Pregnancy Using Primary Care Interventions to Identify the Fertile Window, Front Med 4:250",
        "pdf": "W2783646223__achieving-pregnancy-using-primary-care-interventions-to-iden.pdf",
        "cell": "PRIMARY_FREQ_BIOMETRIC",
    },
    "mturi_1997_tanzania": {
        "study": "Mturi (1997), Determinants of Birth Intervals Among Non-Contracepting Tanzanian Women, African Population Studies 12(2)",
        "pdf": "W2263484717__the-determinants-of-birth-intervals-among-non-contracepting-.pdf",
        "cell": "PRIMARY_ABSTINENCE_WINDOW",
    },
    "pp_rct_2022_nl": {
        "study": "Pleasure&Pregnancy web-programme RCT (2022), Netherlands, unexplained infertility, 700 couples",
        "pdf": "W4403055433__the-web-based-pleasure-pregnancy-programme-in-the-treatment-.pdf",
        "cell": "PRIMARY_FREQ_DECLINE",
    },
}

# effect rows: (study_id, estimand, predictor, outcome, sample, period, design, adj_contra, adj_age,
#               eff_type, val, lo, hi, se, direction, sig, primary, poolable, sign_vs_a14, locator, notes)
E = [
    # --- Nie 2020 (China, Fujian) — spousal separation as coital-exposure shock ---
    ("nie_2020_fujian", "1st birth odds, internal separation 0-3y vs cohabiting", "internal migration separation 0-3y", "odds of 1st marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process (aML)", "partial (no direct control; family-policy dummies for 2nd/3rd only)", "yes", "odds ratio", 0.26, 0.18, 0.37, "", "reduces births", "p<0.01", "TRUE", "FALSE", "supports", "Table 3 Panel 1, multi-process col", "~74% lower odds of first birth under short internal separation"),
    ("nie_2020_fujian", "1st birth odds, international separation 0-3y vs cohabiting", "international migration separation 0-3y", "odds of 1st marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial", "yes", "odds ratio", 0.03, 0.00, 0.25, "", "reduces births", "p<0.01", "TRUE", "FALSE", "supports", "Table 3 Panel 1", "long-distance separation more strongly depresses fertility; small cells"),
    ("nie_2020_fujian", "1st birth odds, international separation >3y vs cohabiting", "international migration separation >3y", "odds of 1st marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial", "yes", "odds ratio", 0.18, 0.08, 0.42, "", "reduces births", "p<0.01", "TRUE", "FALSE", "supports", "Table 3 Panel 1", "~82% lower odds"),
    ("nie_2020_fujian", "1st birth odds, reunified vs never separated", "reunified after separation", "odds of 1st marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial", "yes", "odds ratio", 0.42, 0.29, 0.61, "", "reduces births", "p<0.01", "TRUE", "FALSE", "supports", "Table 3 Panel 1 (reunified)", "KEY: no fertility catch-up after reunification (H2 rejected)"),
    ("nie_2020_fujian", "2nd birth odds, internal separation 0-3y vs cohabiting", "internal migration separation 0-3y", "odds of 2nd marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial (family-policy dummies)", "yes", "odds ratio", 0.30, 0.14, 0.68, "", "reduces births", "p<0.01", "FALSE", "FALSE", "supports", "Table 3 Panel 2", "~70% lower"),
    ("nie_2020_fujian", "2nd birth odds, international separation vs cohabiting", "international migration separation", "odds of 2nd marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial", "yes", "odds ratio", 0.12, 0.02, 0.65, "", "reduces births", "p<0.05", "FALSE", "FALSE", "supports", "Table 3 Panel 2", "annual 2nd-birth odds ~12% of unseparated"),
    ("nie_2020_fujian", "2nd birth odds, reunified vs never separated", "reunified after separation", "odds of 2nd marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial", "yes", "odds ratio", 0.65, 0.44, 0.97, "", "reduces births", "p<0.05", "FALSE", "FALSE", "supports", "Table 3 Panel 2 (reunified)", "no catch-up for 2nd birth either"),
    ("nie_2020_fujian", "3rd birth odds, separated vs cohabiting", "separated due to migration", "odds of 3rd marital birth", "632 Fujianese couples, China", "~1965-2005", "discrete-time logit multi-process", "partial", "yes", "odds ratio", 0.83, 0.53, 1.29, "", "null", "ns", "FALSE", "FALSE", "null", "Table 3 Panel 3", "3rd-birth effect not significant; small cells"),
    # --- Clifford 2009 (Tajikistan) — selection-corrected separation ---
    ("clifford_2009_tajikistan", "higher-order conception, full-year (12mo) spousal absence (single-process)", "spousal absence 12 months", "odds of higher-order conception in year", "3,509 couples, Tajikistan TLSS 2003 (TFR~4, contraception ~30%)", "1998-2002", "multilevel single-process logit", "no", "yes", "odds ratio", 0.25, "", "", 0.404, "reduces conception", "p<0.01", "TRUE", "FALSE", "supports", "Table 4, row 'Spousal absence 12'", "75% lower odds for full-year absence; SE on log-odds scale"),
    ("clifford_2009_tajikistan", "higher-order conception, >=6mo spousal absence, fully adjusted multi-process", "spousal absence 6-12 months (ref 0-5)", "odds of higher-order conception in year", "3,509 couples, Tajikistan; 1999-2002 couple-years", "1999-2002", "multilevel bivariate multi-process logit (selection-corrected)", "no", "yes", "odds ratio", 0.58, "", "", 0.164, "reduces conception", "p<0.01", "TRUE", "FALSE", "supports", "Table 7 multi-process col (author preferred)", "~42% lower; multi-process MORE negative than single-process (positive community selection biases naive toward 0)"),
    ("clifford_2009_tajikistan", "total live-birth conceptions, cumulative 12-23mo separation over window", "cumulative months of spousal separation 12-23mo", "count of conceptions leading to live births 1998-2002", "3,509 couples, Tajikistan", "1998-2002", "single-process Poisson", "no", "yes", "Poisson log-count coefficient", -0.32, "", "", 0.127, "reduces births", "p<0.05", "TRUE", "FALSE", "supports", "Table 5", "period effect over short window; completed-fertility catch-up unknown"),
    ("clifford_2009_tajikistan", "higher-order conception, 6mo (seasonal) spousal absence", "spousal absence 6 months", "odds of higher-order conception", "3,509 couples, Tajikistan", "1998-2002", "multilevel single-process logit", "no", "yes", "odds ratio", 0.98, "", "", 0.248, "null", "ns", "FALSE", "FALSE", "null", "Table 4, row 'Spousal absence 6'", "seasonal workers reunite each winter → no disruption; dose-response supports mechanism"),
    # --- Bouchard 2018 (N=256) — biometric timing slope ---
    ("bouchard_2018_marquette", "12mo cumulative pregnancy: fertile-window (High/Peak-day) vs infertile (Low-day) intercourse", "intercourse timed to High/Peak fertile days vs Low days", "cumulative pregnancy per 100 women, 12mo", "256 N. American conception-seekers (self-selected, not infertility-screened)", "2008-2015", "prospective single-arm cohort (internal timing contrast)", "NA (trying to conceive)", "no", "pregnancy rate per 100 women", 85.0, "", "", "", "raises conception", "reported", "TRUE", "FALSE", "supports", "Results p.5 (High/Peak 85 vs Low 1)", "strongest internal biometric slope; no CI; clinical sample; timing vs frequency not internally separable"),
    ("bouchard_2018_marquette", "CITED Tiplady 2013 RCT: LH-timed vs frequent intercourse", "ovulation-timed intercourse vs frequent intercourse (every 2-3d)", "pregnancy rate", "cited RCT", "2013", "RCT (cited/secondary)", "NA", "no", "pregnancy rate (two-group)", 43.0, "", "", "", "raises conception", "reported", "FALSE", "FALSE", "supports", "Intro p.2 (ref 34): 43% vs 30%", "external RCT directly contrasting timing vs frequency-only; cited, not primary"),
    # --- Mturi 1997 (Tanzania) — natural fertility, weak/indirect ---
    ("mturi_1997_tanzania", "conception hazard, polygamous vs monogamous (author-interpreted reduced coital frequency)", "polygamous marriage (coital-frequency proxy)", "monthly hazard of conception (birth interval)", "4,860 birth intervals, non-contracepting Tanzanian women, 1991/92 DHS", "1987-1992", "Cox proportional hazards", "NA (non-contracepting sample)", "yes", "hazard ratio", 0.87, 0.781, 0.966, "", "reduces conception", "p<0.05", "FALSE", "FALSE", "supports (indirect)", "Table 2, 'Polygamous'", "coital frequency not measured, inferred from polygamy; also captures unmeasured abstinence customs"),
    ("mturi_1997_tanzania", "conception hazard, not-married/not-stated vs monogamous (possible spousal absence)", "no co-resident partner (absence proxy)", "monthly hazard of conception", "4,860 birth intervals, non-contracepting Tanzania", "1987-1992", "Cox proportional hazards", "NA", "yes", "hazard ratio", 0.62, 0.540, 0.723, "", "reduces conception", "p<0.05", "FALSE", "FALSE", "supports (indirect)", "Table 2, 'Not married/not stated'", "conflates true absence with censored status; low confidence"),
    ("mturi_1997_tanzania", "conception hazard, amenorrhoea AND/OR abstinence (combined) vs neither", "postpartum amenorrhoea and/or abstinence (AMALGAMATED)", "monthly hazard of conception", "4,860 birth intervals, non-contracepting Tanzania", "1987-1992", "Cox PH, time-varying", "NA", "yes", "hazard ratio", 0.27, 0.232, 0.323, "", "reduces conception", "p<0.05", "FALSE", "FALSE", "confounded (A.13+A.14)", "Table 2, amenorrhoea/abstinence row", "abstinence (A.14) NOT separable from lactational amenorrhoea (A.13); do not attribute to A.14 alone"),
    # --- Pleasure&Pregnancy RCT (Netherlands) — NULL + failed manipulation ---
    ("pp_rct_2022_nl", "intervention effect on naturally-conceived ongoing pregnancy (ITT)", "randomization to eHealth programme intended to raise coital frequency", "ongoing pregnancy (>=12wk) within 6mo", "700 couples, unexplained infertility, Netherlands", "2016-2022", "RCT (ITT)", "NA (trying to conceive)", "no (randomized)", "risk ratio", 0.86, 0.64, 1.14, "", "null", "ns", "TRUE", "FALSE", "null", "Table 2", "NULL on pregnancy"),
    ("pp_rct_2022_nl", "manipulation check: intervention effect on coital frequency (the mediator)", "randomization to eHealth programme", "coital frequency (men-reported, per month), baseline→6mo", "700 couples, Netherlands", "2016-2022", "RCT (mixed model)", "NA", "no", "between-arm change in acts/month", 0.25, "", "", "", "null", "ns (group P=0.47)", "FALSE", "FALSE", "failed manipulation", "Table 3 (frequency fell ~7→6 both arms)", "the frequency→conception first stage never fired → null test of the whole chain, not a slope estimate"),
]


def main() -> None:
    EFFECTS.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, e in enumerate(E, 1):
        (sid, estimand, predictor, outcome, sample, period, design, adj_c, adj_a, etype, val, lo, hi,
         se, direction, sig, primary, poolable, sign, locator, notes) = e
        s = STUDIES[sid]
        rows.append({
            "effect_id": f"A14-{i:03d}", "study_id": sid, "study": s["study"], "pdf_filename": s["pdf"],
            "cell": s["cell"], "estimand": estimand, "predictor": predictor, "outcome": outcome,
            "sample": sample, "period": period, "design": design, "adjusts_contraception": adj_c,
            "adjusts_age": adj_a, "effect_type": etype, "effect_value": val, "ci_lower": lo,
            "ci_upper": hi, "se": se, "direction": direction, "significant": sig,
            "is_primary_estimate": primary, "poolable": poolable, "sign_vs_a14": sign,
            "source_locator": locator, "source_type": "pdf_table_or_text_read",
            "verified_by": "ai_fulltext_extraction_2026-09-23_single_reader", "notes": notes,
        })
    with open(EFFECTS, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    screen_rows = [
        ("nie_2020_fujian", STUDIES["nie_2020_fujian"]["study"], "W3086522635", "PRIMARY_SEPARATION_SHOCK", "SURVIVES", "Spousal separation is an exogenous coital-exposure shock within intact unions; large negative effects on 1st/2nd birth odds; multi-process model; no reunification catch-up."),
        ("clifford_2009_tajikistan", STUDIES["clifford_2009_tajikistan"]["study"], "W2012967441", "PRIMARY_SEPARATION_SHOCK", "SURVIVES", "Joint multi-process model separates disruption from selection; full-year absence OR 0.25, adjusted >=6mo OR 0.58; naive models underestimate; completed-fertility catch-up unassessed."),
        ("bouchard_2018_marquette", STUDIES["bouchard_2018_marquette"]["study"], "W2783646223", "PRIMARY_FREQ_BIOMETRIC", "SURVIVES", "Prospective cohort; fertile-window-timed intercourse 85/100 vs 1/100 on infertile days — the biometric timing slope. No frequency control arm; clinical self-selected sample."),
        ("mturi_1997_tanzania", STUDIES["mturi_1997_tanzania"]["study"], "W2263484717", "PRIMARY_ABSTINENCE_WINDOW", "WEAK/PARTIAL", "Non-contracepting (clean on Wall 1) but abstinence amalgamated with lactational amenorrhoea (A.13); only indirect polygamy (HR 0.87) and absence (HR 0.62) proxies isolate A.14."),
        ("pp_rct_2022_nl", STUDIES["pp_rct_2022_nl"]["study"], "W4403055433", "PRIMARY_FREQ_DECLINE", "NULL/NON-CONFIRMATORY", "RCT null on pregnancy (RR 0.86); manipulation FAILED (coital frequency fell equally in both arms), so it is a null test of the whole chain, not a clean slope estimate; intervention targets pleasure/distress not frequency."),
        ("koo_2018_korea", "Koo et al. (2018), Likelihood of achieving pregnancy through timed coitus in young infertile women with decreased ovarian reserve, Clin Exp Reprod Med 45(1)", "W2796931555", "OFF_FECUNDITY_CAPACITY", "FAILS", "Timed coitus applied uniformly as a treatment; coital frequency/timing never varied or measured as a predictor. Actual predictor is serum AMH/ovarian reserve (A.15). Zero A.14 effects."),
        ("moriki_2012_japan", "Moriki (2012), Mothering, Co-sleeping, and Sexless Marriages, J Social Science ICU 74", "W633189275", "MECHANISM_FREQ_ONLY", "MECHANISM/CONTEXT", "Documents high/rising Japanese sexless-marriage prevalence (~25% no marital sex past year; ~a third and rising) and argues a Bongaarts-Potter frequency→fecundability link, but provides no original effect estimate. SDT mechanism/context."),
    ]
    with open(SCREEN, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["study_id", "study", "work_id", "cell", "fulltext_screen_verdict", "reason"])
        w.writerows(screen_rows)

    n_support = sum(1 for r in rows if r["sign_vs_a14"].startswith("supports"))
    print(f"wrote {EFFECTS} ({len(rows)} effects; {n_support} supportive, "
          f"{sum(1 for r in rows if r['sign_vs_a14']=='null')} null)")
    print(f"wrote {SCREEN} ({len(screen_rows)} study-level verdicts)")
    print("survivors: Nie 2020, Clifford 2009, Bouchard 2018 (+ Mturi 1997 weak); "
          "null: P&P RCT; excluded: Koo 2018; context: Moriki 2012")
    print("NOT poolable (heterogeneous estimands: birth-order ORs vs conception ORs vs per-cycle "
          "pregnancy rates vs Cox HRs) → narrative synthesis per PROTOCOL step 9")


if __name__ == "__main__":
    main()
