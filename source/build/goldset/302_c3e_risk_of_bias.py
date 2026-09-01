#!/usr/bin/env python3
"""302 — C.3.e: risk of bias, per study. TICK-077.

Domains are the identification threats the scope memo named before any study was read, plus two the
extraction has since forced. Judgements are recorded per study with the reason, not scored into a
single number: a summary score would hide which domain fails, and on this chapter the domains fail
very differently.

  D1 SELECTION INTO EXPOSURE — is participation/exposure chosen? Steele et al. report joiners were
     more educated and MORE LIKELY TO HAVE USED CONTRACEPTION BEFORE JOINING; that is the domain
     failing in its clearest possible form.
  D2 REVERSE CAUSALITY — planning a birth changes borrowing and saving before the birth.
  D3 CONFOUNDED SHOCK — credit shocks travel with income and employment shocks.
  D4 OUTCOME MEASUREMENT — realized births from registers/surveys vs self-reported desires or
     intentions. On this chapter the level is not a nuance: signs differ across it.
  D5 FIRST STAGE VERIFIED — for a null, did the exposure demonstrably move? An unverified first stage
     makes a null uninformative. This is the domain that separates Ao et al. from Grimm.
  D6 EXPOSURE IS THE REGISTERED ONE — does the study vary a financial instrument, or something else
     that a title made look like one? Four records failed this at full text.

Usage: python3 302_c3e_risk_of_bias.py
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "extraction" / "credit-constraints-risk-of-bias.csv"
rows = list(csv.DictReader((ROOT / "extraction" / "credit-constraints-effects.csv").open()))

# per-study judgements: LOW / MODERATE / SERIOUS / CRITICAL / NA, with the reason
J = {
 "W4214485069": ("Do credit supply shocks affect fertility choices?",
   "LOW","LOW","MODERATE","LOW","NA","LOW",
   "Two exogenous shocks (deregulation timing; Bartik IV). D3 moderate: deregulation plausibly moves "
   "local income and employment, which the paper addresses but cannot fully rule out."),
 "W2514518411": ("The Babies of Mortgage Market Deregulation",
   "LOW","LOW","MODERATE","LOW","NA","MODERATE",
   "Federal regulator ruling gives geographic heterogeneity. D6 moderate: the author's own tests point "
   "to ACCESS TO SPACE as the mechanism, which is C.2.c's object even though credit is what varies."),
 "W7154967232": ("Do Mortgage Interest Subsidies Affect Fertility (Taiwan)",
   "LOW","LOW","LOW","LOW","LOW","LOW",
   "DiD with matching; FIRST STAGE VERIFIED (mortgage burden -7.9%). The strongest null in the pool."),
 "W4417408273": ("Credit Availability, Intergenerational Interactions (China)",
   "MODERATE","MODERATE","MODERATE","LOW","NA","LOW",
   "FE-Poisson + IV, but the instrument is not a policy shock and the first stage is unseen. "
   "Abstract-sourced; full text on the residual list."),
 "W2039710642": ("Desai and Tarozzi (Ethiopia RCT)",
   "LOW","LOW","LOW","LOW","MODERATE","LOW",
   "Randomised, credit arm separately allocated. D5 moderate: contraceptive use did not move much, so "
   "for the FP arms the first stage is weak; the credit arm's own first stage is take-up, not "
   "contraception. Small magnitudes on a rising-fertility background."),
 "W2995686300": ("Grimm, rainfall risk (bank-access interaction)",
   "MODERATE","LOW","MODERATE","LOW","SERIOUS","LOW",
   "D5 SERIOUS and decisive: the author says the access measures 'are simply too crude', so the null "
   "on the bank interaction is uninformative rather than a zero."),
 "W1601642119": ("Fertility and Financial Development, US counties c.1850",
   "SERIOUS","MODERATE","SERIOUS","LOW","NA","LOW",
   "OLS on a county cross-section; bank presence is not randomly placed. D3 serious: banks locate "
   "where commerce is, and commerce moves fertility."),
 "W2119295186": ("Filoso and Papagni, Fertility choice and financial development",
   "SERIOUS","SERIOUS","SERIOUS","LOW","NA","LOW",
   "Cross-country aggregate panel; endogeneity tested for GDP and FLFP only, no instrument for credit."),
 "W3210507281": ("Suriani et al., developed vs developing",
   "SERIOUS","MODERATE","SERIOUS","LOW","NA","LOW",
   "Two-step system GMM. SARGAN REJECTED (p=0.000) in all 11 models in both samples; Hansen 0.16-0.29. "
   "The overidentifying restrictions do not hold."),
 "W3125880351": ("Kuchler, Do Microfinance Programs Change Fertility?",
   "SERIOUS","MODERATE","MODERATE","LOW","NA","LOW",
   "DiD on programme participation; participation is self-selected and the paper's own null is on a "
   "falling-fertility background."),
 "W2613324243": ("Steele, Amin and Naved",
   "CRITICAL","MODERATE","MODERATE","MODERATE","NA","LOW",
   "D1 CRITICAL by the authors' own account: joiners were more educated, married to better-educated "
   "men, and MORE LIKELY TO HAVE USED CONTRACEPTIVES BEFORE JOINING. Outcome is desires."),
 "W2385528357": ("Karim et al., NGO membership proxy",
   "CRITICAL","MODERATE","MODERATE","LOW","NA","MODERATE",
   "D1 critical: NGO membership self-selected. D6 moderate: membership is a PROXY for credit receipt."),
 "W4385666598": ("Lan, Pan and Yu, digital financial inclusion",
   "MODERATE","MODERATE","SERIOUS","MODERATE","NA","LOW",
   "Provincial index; D3 serious - digital financial inclusion tracks regional development. Outcome is "
   "INTENTIONS."),
 "W4313814222": ("Access to credit and capital markets, China",
   "MODERATE","MODERATE","MODERATE","LOW","NA","MODERATE",
   "Theory-plus-empirics; the claim extracted is an interaction sign rather than a level effect."),
}
D = ["D1_selection", "D2_reverse", "D3_confounded_shock", "D4_outcome_measurement",
     "D5_first_stage_verified", "D6_exposure_is_registered"]
with OUT.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["openalex", "study"] + D + ["overall", "note"])
    for oid, v in J.items():
        study, *dom, note = v
        sev = {"LOW": 0, "MODERATE": 1, "SERIOUS": 2, "CRITICAL": 3, "NA": -1}
        worst = max(dom, key=lambda x: sev[x])
        w.writerow([oid, study] + dom + [worst, note])

from collections import Counter
print(f"{len(J)} studies assessed across 6 domains\n")
for i, d in enumerate(D):
    c = Counter(v[1 + i] for v in J.values())
    print(f"  {d:26s} " + "  ".join(f"{k}:{n}" for k, n in sorted(c.items())))
sev = {"LOW": 0, "MODERATE": 1, "SERIOUS": 2, "CRITICAL": 3, "NA": -1}
overall = Counter(max(v[1:7], key=lambda x: sev[x]) for v in J.values())
print(f"\n  OVERALL (worst domain)     " + "  ".join(f"{k}:{n}" for k, n in sorted(overall.items())))
print(f"\nwritten: {OUT.relative_to(ROOT)}")
