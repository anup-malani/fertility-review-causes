#!/usr/bin/env python3
"""TICK-093 stages 6-7: full-text screen + effect extraction for the D.1.d identified-design core.

Materializes the AI-read primary evidence from the identified-core PDFs held on disk (mirrors
98_d2c_extract_core_evidence). Effect values are read from the papers' tables/text with exact source
locators, not derivable from raw data, so they are embedded here with provenance. Four OA-retrievable
identified-core PDFs were full-text read by parallel extraction agents on 2026-09-26; each effect carries
the D.1.d-specific fields the synthesis needs: which estimand cell, whether the design isolates the
IDEOLOGICAL framing from the financial TRANSFER (Wall C.2.d) and from coercive fertility-control
restriction (Wall A.4), whether the outcome is a durable quantum shift or a transient tempo response, the
sign RELATIVE TO the D.1.d prediction, and whether it is poolable.

Full-text screen (stage 6) verdicts, one per study:
  - Aksoy & Billari 2018 (Political Islam, Marriage, and Fertility, AJS 123(5); Turkey close-election RDD):
    SURVIVES — the cleanest identification in the literature (McCrary density + placebo/covariate-balance
    tests pass, replicated across district/province/individual data). Islamist pronatalist rule raised
    fertility (+0.14 births/woman; a-GFR +7.75) and marriage. BUT the authors' own mediation routes the
    effect through MATERIAL welfare (General Health Insurance +0.28) and finds NULL effects on the
    ideational mediators (ideal number of children RD 0.12 n.s.; religiosity RD 0.05 n.s.). The decisive
    D.1.d study: where pronatalist-ideological rule raised fertility, it ran through spending, not framing.
  - Validova 2021 (Pronatalist Policies and Fertility in Russia: Estimating Tempo and Quantum, CPoS 46;
    Russia 2007 maternity-capital package): SURVIVES (descriptive decomposition) — the post-2007 TFR rise
    is 91% tempo / 9% quantum (quantum grows with parity: 1%/13%/42% at parities 1/2/3), then falls after
    2015. No control group, no counterfactual; ideology inseparable from the cash. Tempo-dominant, transient.
  - Wang 2026 (Fertility in Russia at the Turn of Eras; Russia 2003-2023): WEAK/CONTEXT — descriptive
    narrative time-series; argues the rise was mainly STRUCTURAL (large 1980s cohorts) with policy effects
    mostly tempo. No identified estimate; not poolable.
  - Tang, Wong & Batzorig 2022 (Do Financial Incentives on High Parity Birth Affect Fertility? Order of
    Glorious Mother, IUJ WP; Mongolia DiD): SURVIVES (identified DiD) but ROUTES TO C.2.d — the honorific
    "Mother Hero" award is bundled inseparably with a doubled cash annuity; the paper identifies the money,
    not the honour. +4.3/+2.3/+2.6pp birth probability at parities 1/2/3, null/negative at high parities,
    on a 2-year window (tempo not separable). The registered "honorific award" instrument, empirically, is
    a transfer.

NOTE ON THE PAYWALLED / PREPRINT BACKLOG: the marquee framing experiments that would carry the clean
ideational channel (Israel ethnic-threat; "Guns vs. Wombs", South Korea; Christian-nationalism, US) are
OSF/Zenodo preprints whose file GUIDs need browser/API navigation, and the Eastern-European coercion canon
(Ceausescu's Romania; Hungary 1953; Zimbabwe Depo-Provera) is paywalled. They are on the RA proxy/ILL
handoff (nationalism-pronatalist-ideology-missing-pdf-dois.csv) and are characterised at ABSTRACT level in
the chapter, not effect-extracted here. The 140 associational records and the 15 unretrieved identified-core
records are the RA extraction backlog (the A.14/D.2.c precedent). The causal core below rests on one
strongly-identified natural experiment (Aksoy-Billari), one identified DiD that routes to C.2.d (Tang et
al.), and two Russian decomposition/descriptive studies — enough to fix the chapter's direction and its
central identification finding.

Outputs:
  extraction/nationalism-pronatalist-ideology.csv                  (one row per effect; the atomic deliverable)
  extraction/nationalism-pronatalist-ideology-fulltext-screen.csv  (one row per study; stage-6 verdicts)
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EFFECTS = ROOT / "extraction" / "nationalism-pronatalist-ideology.csv"
SCREEN = ROOT / "extraction" / "nationalism-pronatalist-ideology-fulltext-screen.csv"

FIELDS = [
    "effect_id", "study_id", "study", "pdf_filename", "cell", "region", "phenomenon", "estimand",
    "predictor", "outcome", "sample", "period", "design", "isolates_from_transfers_C2d",
    "isolates_from_coercion_A4", "tempo_vs_quantum", "effect_type", "effect_value", "ci_lower",
    "ci_upper", "se", "direction", "significant", "is_primary_estimate", "poolable", "sign_vs_d1d",
    "source_locator", "source_type", "verified_by", "notes",
]

STUDIES = {
    "aksoy_billari_2018": {
        "study": "Aksoy & Billari (2018), Political Islam, Marriage, and Fertility: Evidence from a Natural Experiment, American Journal of Sociology 123(5):1296-1340",
        "pdf": "W2789619723__political-islam-marriage-and-fertility-evidence-from-a-natur.pdf",
        "cell": "MIXED_IDEOLOGY_TRANSFER", "region": "Turkey", "phenomenon": "SDT",
    },
    "validova_2021": {
        "study": "Validova (2021), Pronatalist Policies and Fertility in Russia: Estimating Tempo and Quantum Effects, Comparative Population Studies 46:425-452",
        "pdf": "W3207647903__pronatalist-policies-and-fertility-in-russia-estimating-temp.pdf",
        "cell": "MIXED_IDEOLOGY_TRANSFER", "region": "Russia", "phenomenon": "SDT",
    },
    "wang_2026": {
        "study": "Wang ZiRui (2026), Fertility in Russia at the Turn of Eras: Dynamics and Mechanisms of Demographic Change (2003-2023), Theory and Practice of Social Development No.3:84-89 [in Russian]",
        "pdf": "W7160179369__fertility-in-russia-at-the-turn-of-eras-dynamics-and-mechani.pdf",
        "cell": "MIXED_IDEOLOGY_TRANSFER", "region": "Russia", "phenomenon": "SDT",
    },
    "tang_wong_batzorig_2022": {
        "study": "Tang, Wong & Batzorig (2022), Do Financial Incentives on High Parity Birth Affect Fertility? Evidence from the Order of Glorious Mother in Mongolia, IUJ working paper EMS-2022-01",
        "pdf": "W7145773811__do-financial-incentives-on-high-parity-birth-affect-fertilit.pdf",
        "cell": "MIXED_IDEOLOGY_TRANSFER", "region": "Mongolia", "phenomenon": "SDT",
    },
}

# One row per extracted effect. effect_value/se as reported; blank where the paper reports none.
E = [
    # ---- Aksoy & Billari 2018 (Turkey close-election RDD) — the decisive identified study ----
    dict(study_id="aksoy_billari_2018", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Effect of local Islamist (AK Parti) mayoral rule on district fertility",
         predictor="AK Parti close-election win margin 2004 (RD threshold=0)",
         outcome="adjusted general fertility rate (a-GFR), children 0-4 per 1,000 women, 2006-2010",
         sample="916 districts (N=541 within bandwidth)", period="2004 election -> 2006-2010",
         design="close-election RDD, local-linear, IK optimal bandwidth 0.15",
         isolates_from_transfers_C2d="NO", isolates_from_coercion_A4="YES",
         tempo_vs_quantum="quantum (no offsetting decline 2010-14)",
         effect_type="additional children per 1,000 women", effect_value="7.75", se="3.86",
         direction="positive", significant="yes", is_primary_estimate="yes", poolable="no",
         sign_vs_d1d="supports direction (higher fertility under pronatalist rule)",
         source_locator="Fig. 4 top-left, p.1320", source_type="figure",
         notes="Headline. Clean RD (McCrary density n.s.; pre-2004 placebo n.s.). a-GFR includes child survival."),
    dict(study_id="aksoy_billari_2018", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Effect of local Islamist rule on individual births after 2004",
         predictor="AK Parti province-center win margin 2004 (RD)",
         outcome="number of births after 2005 (individual, TDHS-2013)",
         sample="5,377 women 15-49 (bw 0.18)", period="2004 -> 2013",
         design="close-election RDD, individual", isolates_from_transfers_C2d="NO",
         isolates_from_coercion_A4="YES", tempo_vs_quantum="quantum",
         effect_type="additional births per woman", effect_value="0.14", se="0.07",
         direction="positive", significant="yes", is_primary_estimate="yes", poolable="no",
         sign_vs_d1d="supports direction", source_locator="Fig. 4 top-right, p.1320 (P=.027)",
         source_type="figure", notes="Robust to full covariate controls (0.14, SE .07, P=.047)."),
    dict(study_id="aksoy_billari_2018", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="MECHANISM (material): effect of Islamist rule on health-insurance coverage",
         predictor="AK Parti province-center win margin 2004 (RD)",
         outcome="Pr(General Health Insurance vs none), individual",
         sample="1,240 women (bw 0.19)", period="2004 -> 2013",
         design="close-election RDD, individual (mediation)", isolates_from_transfers_C2d="THIS IS the transfer channel",
         isolates_from_coercion_A4="n/a", tempo_vs_quantum="n/a",
         effect_type="probability", effect_value="0.28", se="0.12",
         direction="positive", significant="yes", is_primary_estimate="no", poolable="no",
         sign_vs_d1d="AGAINST an ideational reading — confirms the effect routes through welfare/transfers",
         source_locator="Fig. 7 bottom, p.1328 (P=.020)", source_type="figure",
         notes="GHI in turn raises births (coef .075, SE .039, P=.053). Effects concentrated in poorer provinces."),
    dict(study_id="aksoy_billari_2018", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="MECHANISM (ideational): effect of Islamist rule on desired fertility",
         predictor="AK Parti province-center win margin 2004 (RD)",
         outcome="ideal number of children (individual, TDHS-2013)",
         sample="TDHS-2013 women", period="2004 -> 2013",
         design="close-election RDD, individual (mediation)", isolates_from_transfers_C2d="n/a",
         isolates_from_coercion_A4="n/a", tempo_vs_quantum="n/a",
         effect_type="RD coefficient (ideal n children)", effect_value="0.12", se="0.24",
         direction="null", significant="no", is_primary_estimate="no", poolable="no",
         sign_vs_d1d="AGAINST the D.1.d ideology mechanism — fertility rose without preferences changing",
         source_locator="Fig. 9 top, p.1332 (P=.612)", source_type="figure",
         notes="DECISIVE null: the ideational channel D.1.d posits (a shift in the desired number) is absent."),
    dict(study_id="aksoy_billari_2018", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="MECHANISM (ideational): effect of Islamist rule on individual religiosity",
         predictor="AK Parti province-center win margin 2004 (RD)",
         outcome="individual religiosity score (TDHS-2013)",
         sample="TDHS-2013 women", period="2004 -> 2013",
         design="close-election RDD, individual (mediation)", isolates_from_transfers_C2d="n/a",
         isolates_from_coercion_A4="n/a", tempo_vs_quantum="n/a",
         effect_type="RD coefficient (religiosity)", effect_value="0.05", se="0.06",
         direction="null", significant="no", is_primary_estimate="no", poolable="no",
         sign_vs_d1d="AGAINST the ideational mechanism (no religiosity shift)",
         source_locator="Fig. 9 bottom, p.1332 (P=.382)", source_type="figure",
         notes="Second ideational null: Islamist rule did not raise religiosity either."),
    dict(study_id="aksoy_billari_2018", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Effect of local Islamist rule on female marriage rate",
         predictor="AK Parti province-center win margin 2004 (RD)",
         outcome="female marriage rate per 1,000 women 16-44, 2006-2013 (province)",
         sample="N=440 (bw 0.22)", period="2004 -> 2006-2013",
         design="close-election RDD", isolates_from_transfers_C2d="NO", isolates_from_coercion_A4="YES",
         tempo_vs_quantum="partly tempo (declines over time, interaction -0.32 P=.039; projected to vanish ~2020)",
         effect_type="extra marriages per 1,000 women", effect_value="4.41", se="1.64",
         direction="positive", significant="yes", is_primary_estimate="no", poolable="no",
         sign_vs_d1d="supports direction (marriage is the proximate route to the fertility effect)",
         source_locator="Fig. 6 middle, p.1326 (P=.007)", source_type="figure",
         notes="Male marriage rate RD 3.82 (SE 1.88, P=.042). Marriage effect is transient (declines to ~0 by 2020)."),

    # ---- Validova 2021 (Russia 2007 package) — tempo/quantum decomposition, descriptive ----
    dict(study_id="validova_2021", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Quantum (completed-fertility) share of the post-2007 TFR rise, all births",
         predictor="2007 pronatalist package (maternity capital + allowances), nationwide",
         outcome="TFR change 2007-2017 decomposed (TFRp*/Sobotka method)",
         sample="Russian Federation (HFD)", period="2007-2017",
         design="descriptive period-fertility decomposition (NO control group, NO counterfactual)",
         isolates_from_transfers_C2d="NO", isolates_from_coercion_A4="no coercion",
         tempo_vs_quantum="quantum only 9% of the change; tempo 91%",
         effect_type="quantum share of TFR change (%)", effect_value="9", se="",
         direction="positive", significant="not reported", is_primary_estimate="yes", poolable="no",
         sign_vs_d1d="weak — the durable component is small and cash-attributed",
         source_locator="Table 1, p.441", source_type="table",
         notes="Tempo:quantum = 91:9. Quantum grows with parity: 1% (P1), 13% (P2), 42% (P3). No SE/CI reported."),
    dict(study_id="validova_2021", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Observed TFR trajectory around the reform (durability check)",
         predictor="2007 pronatalist package", outcome="total fertility rate (observed)",
         sample="Russia (HFD)", period="2006-2018",
         design="descriptive time series (no counterfactual)", isolates_from_transfers_C2d="NO",
         isolates_from_coercion_A4="no coercion", tempo_vs_quantum="transient (rise then fall)",
         effect_type="TFR level", effect_value="1.30 (2006) -> 1.78 (2015) -> 1.57 (2018)", se="",
         direction="positive then reversing", significant="not reported", is_primary_estimate="no",
         poolable="no", sign_vs_d1d="the post-2015 fall undercuts a durable ideology effect",
         source_locator="Fig. 2a, p.438; text p.439", source_type="figure",
         notes="Author's conclusion: policy shifted timing, not completed family size; 'the principal tools ... remain financial.'"),

    # ---- Wang 2026 (Russia narrative) — structural, non-identified ----
    dict(study_id="wang_2026", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Attribution of the 2006-2015 Russian fertility rise (narrative event analysis)",
         predictor="2007 maternity capital + regional payments (transfer bundle)",
         outcome="TFR and absolute births, 2003-2023",
         sample="Russian Federation (Rosstat/HFD)", period="2003-2023",
         design="descriptive narrative time-series ('event analysis'); NO regression, NO counterfactual",
         isolates_from_transfers_C2d="NO (policy = the transfer; ideology not measured)",
         isolates_from_coercion_A4="no coercion",
         tempo_vs_quantum="policy effect mainly tempo; rise mainly STRUCTURAL (1980s cohorts at peak age)",
         effect_type="none (no effect estimate reported)", effect_value="", se="",
         direction="", significant="", is_primary_estimate="no", poolable="no",
         sign_vs_d1d="weakly contradicts — attributes the rise to cohort structure, policy only amplified/retimed",
         source_locator="Results p.3, Discussion p.4, Table 1 p.3", source_type="text",
         notes="Descriptive/background only. Author stresses correlation != causation; rise began before key federal measures."),

    # ---- Tang, Wong & Batzorig 2022 (Mongolia OGM) — identified DiD, routes to C.2.d ----
    dict(study_id="tang_wong_batzorig_2022", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Effect of the 2011 Order-of-Glorious-Mother reform on birth probability, women with 1 child",
         predictor="OGM reform: parity thresholds lowered (8->6, 5->4) + annuity doubled (200k/100k MNT); interaction 2018*C1",
         outcome="P(birth within a 2-year window)",
         sample="Mongolia MICS, 23,623 women 15-49", period="2010 vs 2018 cross-sections",
         design="difference-in-differences (linear probability), full controls; PSM robustness",
         isolates_from_transfers_C2d="NO (the honorific 'Mother Hero' award is inseparable from the cash annuity)",
         isolates_from_coercion_A4="no coercion",
         tempo_vs_quantum="ambiguous (2-year birth-probability window; cannot separate)",
         effect_type="pp change in birth probability", effect_value="0.043", se="0.015",
         direction="positive", significant="yes", is_primary_estimate="yes", poolable="no",
         sign_vs_d1d="supports direction but the identified object is the money, not the honour -> routes to C.2.d",
         source_locator="Table 3 col (4) row 2018*C1, p.23; PSM Table 6 p.29 (0.049**)", source_type="table",
         notes="+2.3pp (P2), +2.6pp (P3); null at the higher 6-child goal (2018*C5 -0.003 n.s.) despite larger transfer; negative at cancelled old thresholds. Response diminishes with parity."),
    dict(study_id="tang_wong_batzorig_2022", cell="MIXED_IDEOLOGY_TRANSFER",
         estimand="Effect of the OGM reform on birth probability at the higher (6-child) first-class goal",
         predictor="OGM reform; interaction 2018*C5",
         outcome="P(birth within a 2-year window)",
         sample="Mongolia MICS, 23,623 women", period="2010 vs 2018",
         design="difference-in-differences (LPM)", isolates_from_transfers_C2d="NO",
         isolates_from_coercion_A4="no coercion", tempo_vs_quantum="ambiguous (2-year window)",
         effect_type="pp change in birth probability", effect_value="-0.003", se="0.028",
         direction="null", significant="no", is_primary_estimate="no", poolable="no",
         sign_vs_d1d="null — no response toward the higher-honour goal despite a much larger prize",
         source_locator="Table 3 col (4) row 2018*C5, p.23", source_type="table",
         notes="Key null: the response diminishes as the (larger-prize, higher-status) goal rises."),
]

# Stage-6 full-text screen verdicts, one row per study.
SCREEN_ROWS = [
    dict(study_id="aksoy_billari_2018", verdict="SURVIVES",
         strength="strong identified (close-election RDD)", cell="MIXED_IDEOLOGY_TRANSFER",
         notes="The decisive D.1.d study: cleanest identification; Islamist pronatalist rule raised fertility "
               "and marriage, but the effect routes through MATERIAL welfare (GHI +0.28) with NULL effects on "
               "the ideational mediators (ideal children 0.12 n.s.; religiosity 0.05 n.s.). Ideology channel rejected; "
               "transfer channel confirmed. No A.4 coercion (national fertility-control law constant)."),
    dict(study_id="validova_2021", verdict="SURVIVES",
         strength="descriptive decomposition (no control)", cell="MIXED_IDEOLOGY_TRANSFER",
         notes="Russia 2007 package: 91% tempo / 9% quantum; quantum grows with parity; TFR falls after 2015. "
               "Ideology inseparable from cash; author concludes tools 'remain financial'. Non-poolable (no SE/CI)."),
    dict(study_id="wang_2026", verdict="WEAK/CONTEXT",
         strength="descriptive narrative (no identification)", cell="MIXED_IDEOLOGY_TRANSFER",
         notes="Russia 2003-2023 narrative: rise mainly structural (1980s cohorts), policy mostly tempo. No estimate; "
               "background only."),
    dict(study_id="tang_wong_batzorig_2022", verdict="SURVIVES",
         strength="identified DiD, but routes to C.2.d", cell="MIXED_IDEOLOGY_TRANSFER",
         notes="Mongolia OGM 'Mother Hero' honorific + doubled cash annuity: +4.3/+2.3/+2.6pp at parities 1/2/3, "
               "null/negative at higher goals, 2-year window (tempo not separable). The registered 'honorific award' "
               "instrument is empirically a transfer — the paper identifies the money, not the honour."),
]


def main() -> None:
    EFFECTS.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, e in enumerate(E, 1):
        s = STUDIES[e["study_id"]]
        row = {k: "" for k in FIELDS}
        row.update(e)
        row["effect_id"] = f"D1D-{i:03d}"
        row["study"] = s["study"]
        row["pdf_filename"] = s["pdf"]
        row["region"] = e.get("region", s["region"])
        row["phenomenon"] = e.get("phenomenon", s["phenomenon"])
        row["verified_by"] = "AI extraction agent (2026-09-26), full text; RA 10% verification owed"
        rows.append(row)
    with open(EFFECTS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    sfields = ["study_id", "study", "pdf_filename", "verdict", "strength", "cell", "notes"]
    with open(SCREEN, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=sfields)
        w.writeheader()
        for r in SCREEN_ROWS:
            s = STUDIES[r["study_id"]]
            w.writerow({"study_id": r["study_id"], "study": s["study"], "pdf_filename": s["pdf"],
                        "verdict": r["verdict"], "strength": r["strength"], "cell": r["cell"],
                        "notes": r["notes"]})

    print(f"wrote {EFFECTS.relative_to(ROOT)} ({len(rows)} effects, {len(STUDIES)} studies)")
    print(f"wrote {SCREEN.relative_to(ROOT)} ({len(SCREEN_ROWS)} study verdicts)")


if __name__ == "__main__":
    main()
