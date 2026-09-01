#!/usr/bin/env python3
"""303 — C.3.e: demographic significance and GRADE, per arm per phenomenon. TICK-077.

DEMOGRAPHIC SIGNIFICANCE. PROTOCOL §4.2.1: the denominator is a CHANGE over the phenomenon's FULL
window, never a level and never the study window; numerator, denominator, source and window are named
at the point the share is given; a share above 100% diagnoses a wrong denominator. This repository
holds no fertility panel, so no share is computable, and C.2.c's precedent applies: report NOT
ASSESSED on the arithmetic, and answer the prior question that IS answerable —

  SLOPE SUFFICIENCY: over the phenomenon's window, did the mechanism's own exposure move, in which
  direction, and does the sign of the estimated effect then push fertility the way the phenomenon went?
  A mechanism whose exposure moved the wrong way cannot explain the phenomenon whatever its elasticity.

For C.3.e that question has an unusually clean answer, and it is the chapter's central result.

GRADE is rated per ARM per PHENOMENON, never per chapter, and an empty cell takes **No evidence** —
never VERY LOW, which asserts a poorly identified literature where there is none.

Usage: python3 303_c3e_demsig_grade.py
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
eff = list(csv.DictReader((ROOT / "extraction" / "credit-constraints-effects.csv").open()))
scr = list(csv.DictReader((ROOT / "extraction" / "credit-constraints-screen.csv").open()))
prim = [r for r in scr if r["cell"].startswith("PRIMARY_")]

# ---------------------------------------------------------------- demographic significance
EXPOSURE_TREND = {
    "note": "Private credit to GDP, the chapter's own exposure, over the SDT window. Source: Filoso "
            "and Papagni's own reported figures, quoted in their text.",
    "high_income": {"from": 0.39, "to": 1.14, "direction": "EXPANDED, roughly threefold"},
    "LDC": {"from": 0.13, "to": 0.31, "direction": "EXPANDED, roughly 2.4x"},
}

demsig = {
 "PM": {"arm_S": "NOT ASSESSED — cell is in scope per the registry and EMPTY of read evidence. "
                 "11 Arm S records, 2 read at full text, both re-routed out or uninformative. "
                 "GRADE: No evidence. Sign if it were assessed: negative (children as assets).",
        "arm_B": "OUT OF SCOPE — borrowing terms require a credit market.",
        "composite": "NOT ASSESSED — no pre-modern study in the pool."},
 "FDT": {"arm_S": "NOT ASSESSED — three FDT-era records identified (19th-c US counties, 19th-c "
                  "Britain, American frontier), ONE read, and it is an unidentified OLS "
                  "cross-section. GRADE: Very low on one study, or No evidence if that study is "
                  "routed to C.3.c on its own framing. Sign if assessed: negative.",
         "arm_B": "NOT ASSESSED — no FDT-era borrowing-terms study in the pool.",
         "composite": "NOT ASSESSED — no FDT-era composite study read."},
 "SDT": {"arm_S": "NOT ASSESSED — no SDT-era Arm S estimate read.",
         "arm_B": "**SIGN IS WRONG FOR THE PHENOMENON.** Over the SDT window the exposure EXPANDED "
                  "(private credit/GDP 0.39 -> 1.14 in high-income countries), and every identified "
                  "estimate says expansion RAISES fertility: +5.4% (US deregulation), +6pp (US "
                  "mortgage deregulation), +9.5pp on a 7.7pp base (Bartik credit shock), one verified "
                  "null (Taiwan). A mechanism whose exposure moved the way that RAISES fertility "
                  "cannot explain a fertility DECLINE. At most it is an OFFSET that made the SDT "
                  "smaller than it would otherwise have been. No share is computed and none should be: "
                  "the sign forecloses the question.",
         "composite": "NOT ASSESSED, and CONTESTED AT THE SIGN. The two aggregate panels disagree for "
                      "developed countries — Filoso and Papagni +3.7 to +5%, Suriani et al. negative "
                      "and significant in all 11 models. Both are unidentified and Suriani's Sargan "
                      "test is rejected throughout. No share is computable and the sign is not agreed."},
}

# ---------------------------------------------------------------- GRADE
def studies(arm, ident=None):
    s = {r["openalex"] for r in eff if r["arm"] == arm and (ident is None or r["identified"] == ident)}
    return len(s)

grade = {
 "PM": {"arm_S": ("No evidence", "cell in scope and empty of read evidence"),
        "arm_B": ("n/a", "out of scope"),
        "composite": ("No evidence", "no pre-modern study")},
 "FDT": {"arm_S": ("Very low", "one unidentified OLS cross-section; downgraded for risk of bias "
                               "(D1 selection SERIOUS, D3 confounded shock SERIOUS) and indirectness "
                               "— the authors frame it as old-age security, C.3.c's motive"),
         "arm_B": ("No evidence", "no FDT-era borrowing-terms study"),
         "composite": ("No evidence", "no FDT-era composite study read")},
 "SDT": {"arm_S": ("No evidence", "no SDT-era Arm S estimate read"),
         "arm_B": ("Moderate", "four identified designs (deregulation timing, Bartik IV, a federal "
                               "regulator ruling, DiD-with-matching), consistent in sign, one with a "
                               "verified first stage. Downgraded once for INDIRECTNESS: the estimates "
                               "answer 'does credit access raise fertility', while the chapter asks "
                               "whether credit constraints explain the SDT DECLINE, and the sign runs "
                               "the wrong way for that question. Not downgraded for inconsistency: "
                               "the null is on the intensive cost margin, the positives on the "
                               "extensive access margin"),
         "composite": ("Very low", "no identified estimate on realized fertility outside the Ethiopian "
                                   "RCT; the two aggregate panels disagree at the SIGN; Sargan "
                                   "rejected in one; D1 selection CRITICAL in two studies")},
}

out = {"demographic_significance": demsig, "grade": grade,
       "exposure_trend": EXPOSURE_TREND,
       "basis": {"primary_pool": len(prim),
                 "studies_extracted": len({r['openalex'] for r in eff}),
                 "effect_rows": len(eff),
                 "identified_studies": studies(None, "YES") if False else
                     len({r['openalex'] for r in eff if r['identified']=='YES'}),
                 "share_of_pool_read": round(len({r['openalex'] for r in eff}) / len(prim), 3)},
       "rater_note": "Rated by one rater. PROTOCOL §5 stage 11 requires three independent raters; "
                     "this is a single-rater draft and must be labelled as such. One rater arguing "
                     "both sides is not a panel."}
(LOGS / "credit-constraints-demsig-grade.json").write_text(json.dumps(out, indent=1))

print("DEMOGRAPHIC SIGNIFICANCE\n" + "="*78)
for ph in ("PM", "FDT", "SDT"):
    print(f"\n{ph}")
    for arm in ("arm_S", "arm_B", "composite"):
        print(f"  {arm:10s} {demsig[ph][arm][:150]}")
print("\n\nGRADE (per arm per phenomenon)\n" + "="*78)
print(f"{'':6s} {'Arm S':>14s} {'Arm B':>14s} {'composite':>14s}")
for ph in ("PM", "FDT", "SDT"):
    print(f"{ph:6s} {grade[ph]['arm_S'][0]:>14s} {grade[ph]['arm_B'][0]:>14s} {grade[ph]['composite'][0]:>14s}")
print(f"\nbasis: {out['basis']['studies_extracted']} studies extracted of {len(prim)} primary "
      f"({out['basis']['share_of_pool_read']:.0%} of the pool), {out['basis']['identified_studies']} identified")
print("RATERS: 1 (protocol requires 3) — this is a single-rater draft")
