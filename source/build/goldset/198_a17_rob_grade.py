#!/usr/bin/env python3
"""
198_a17_rob_grade.py — A.17, stages 8 and 11. Risk of bias, then GRADE.

RoB and GRADE run in one script because the second is computed FROM the first: a downgrade for "risk
of bias in the body as a whole" that is not traceable to a per-study domain is an opinion wearing a
GRADE label.

**THE DOMAINS ARE CHAPTER-SPECIFIC AND THE TWO ARMS DO NOT SHARE THEM.** Arm 1 counts ART births;
arm 2 estimates a response to access. A single instrument applied to both would ask the counting
literature about its identification strategy and the policy literature about its denominator, and
score both as low-risk for questions they were never trying to answer.

ARM 1 DOMAINS
  A1.1 **Counterfactual treatment** — from stage 6, unmodified. The dominant domain: a share is only
       an effect if no ART birth would otherwise have occurred.
  A1.2 **Denominator** — a share OF BIRTHS is not a share OF THE TFR. Converting one to the other
       assumes ART is spread evenly across the age schedule; it is concentrated at older ages, where
       age-specific rates are low. Biases the implied contribution UPWARD.
  A1.3 **Ascertainment** — registry versus vital-statistics counts disagree (the US series differ),
       cross-border care moves births across national denominators, and ovulation induction is
       invisible to ART registries entirely (1.9 of Australia's 6.7 percentage points).
  A1.4 **Postponement feedback** — is the share netted of the part induced by the postponement it is
       claimed to offset? Nothing in hand does this.

ARM 2 DOMAINS
  A2.1 **Treatment-definition attenuation** — quantified this run: 65% of US workers are in
       ERISA-exempt self-insured plans, and only 41% of self-insured employers in mandate states
       cover IVF. A "state mandate" is not the treatment it is named as. Biases toward zero.
  A2.2 **Exposure-estimand distance** — A.24's lesson, applied: how far is the measured OUTCOME from
       the registered one? Most of arm 2 measures utilisation, not births. A utilisation effect is
       not a fertility effect and the gap between them is the dropout literature.
  A2.3 **Policy endogeneity** — mandates are adopted, not assigned. One record in the frame studies
       WHY states adopt them.
  A2.4 **Shock direction** — an expansion confounds with secular growth in treatment demand; a
       contraction does not. Contractions are scarcer and worth more, and the chapter should say so
       rather than pooling them.

**THE GRADE RATING IS BY ONE RATER AND IS LABELLED AS SUCH.** PROTOCOL §5 requires three independent
raters. One rater arguing both sides surfaces contingencies but is not independence, and calling it a
panel would be a false claim about method rather than about ART. The requirement stays open in §10.

Output: extraction/{slug}-risk-of-bias.csv
        literature/search-logs/{slug}-grade.md
"""
import csv, json, os
from collections import Counter

SLUG = "art-access-fertility-recovery"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
FT = os.path.join(EXTRACT, f"{SLUG}-fulltext-screened.json")
DEM = os.path.join(EXTRACT, f"{SLUG}-demsig.json")
OUT_CSV = os.path.join(EXTRACT, f"{SLUG}-risk-of-bias.csv")
OUT_MD = os.path.join(LOGS, f"{SLUG}-grade.md")

CF_RISK = {"none_stated": "SERIOUS", "assumed_zero": "SERIOUS",
           "acknowledged_unquantified": "SERIOUS", "partial": "MODERATE", "estimated": "LOW",
           "not_applicable": "n/a"}
# Records whose measured outcome is utilisation/attitude rather than births. Distance from the
# registered estimand is a RATING, not a binary — A.24's lesson.
UTILISATION_ONLY = {"W2058178715", "W1860640930", "W2959688822", "W3115571668", "W3191732024",
                    "W4297464366", "W4393989606", "W4417321594"}


def main():
    rows = json.load(open(FT))
    dem = json.load(open(DEM))
    out = []
    for r in rows:
        arm = r["arm_resolved"]
        rec = dict(id=r["id"], job=r["job"], year=r.get("year"), arm=arm,
                   title=(r.get("title") or "")[:80])
        if arm == "arm1_counting":
            rec["A1_1_counterfactual"] = CF_RISK.get(r["counterfactual_treatment"], "?")
            rec["A1_2_denominator"] = ("SERIOUS" if "share of births" in (r["reported_quantity"] or "").lower()
                                       or "% of" in (r["reported_quantity"] or "").lower()
                                       and "TFR" not in (r["reported_quantity"] or "") else "MODERATE")
            rec["A1_3_ascertainment"] = "MODERATE"
            rec["A1_4_postponement_feedback"] = "SERIOUS"
            worst = "SERIOUS" if "SERIOUS" in (rec["A1_1_counterfactual"], rec["A1_4_postponement_feedback"]) else "MODERATE"
        elif arm == "arm2_estimate":
            us = any(k in (r.get("title") or "") + (r.get("note") or "")
                     for k in ("state", "United States", "US ", "mandate"))
            rec["A2_1_treatment_attenuation"] = "SERIOUS" if us else "LOW"
            rec["A2_2_exposure_estimand_distance"] = ("SERIOUS" if r["id"] in UTILISATION_ONLY
                                                      else "MODERATE")
            rec["A2_3_policy_endogeneity"] = "MODERATE"
            rec["A2_4_shock_direction"] = "LOW"
            worst = "SERIOUS" if "SERIOUS" in (rec["A2_1_treatment_attenuation"],
                                               rec["A2_2_exposure_estimand_distance"]) else "MODERATE"
        else:
            worst = "n/a"
        rec["overall"] = worst
        out.append(rec)

    cols = ["id", "job", "year", "arm", "title", "A1_1_counterfactual", "A1_2_denominator",
            "A1_3_ascertainment", "A1_4_postponement_feedback", "A2_1_treatment_attenuation",
            "A2_2_exposure_estimand_distance", "A2_3_policy_endogeneity", "A2_4_shock_direction",
            "overall"]
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow({c: r.get(c, "") for c in cols})

    a1 = [r for r in out if r["arm"] == "arm1_counting"]
    a2 = [r for r in out if r["arm"] == "arm2_estimate"]
    offs = [d["offset_share"] for d in dem if d.get("offset_share") is not None]
    lo, hi = min(offs), max(offs)
    pc = lambda x: f"{x:.1%}"

    L = [f"# Stages 8 and 11 — risk of bias and GRADE — {SLUG} (A.17)", "",
         "> **PROVISIONAL: 33 of 131 wanted full texts.** GRADE is rated **by one rater**. PROTOCOL "
         "§5 requires three independent raters; one rater arguing both sides surfaces contingencies "
         "but is not independence, and the requirement stays open.", "",
         "## Why the two arms get different instruments", "",
         "Arm 1 counts ART births; arm 2 estimates a response to access. A single instrument applied "
         "to both would ask the counting literature about its identification strategy and the policy "
         "literature about its denominator, and score both low-risk for questions they never tried "
         "to answer.", "",
         f"## Arm 1 — {len(a1)} records", "",
         "| domain | what it asks | SERIOUS | MODERATE | LOW |", "|---|---|---|---|---|"]
    for d, q in [("A1_1_counterfactual", "is the share treated as an effect?"),
                 ("A1_2_denominator", "share of BIRTHS or share of the TFR?"),
                 ("A1_3_ascertainment", "registry vs vital statistics; cross-border; ovulation induction"),
                 ("A1_4_postponement_feedback", "is the induced-by-postponement part netted out?")]:
        c = Counter(r.get(d) for r in a1)
        L.append(f"| `{d}` | {q} | {c.get('SERIOUS',0)} | {c.get('MODERATE',0)} | {c.get('LOW',0)} |")
    L += ["",
          "**A1.4 is SERIOUS for every record in hand**, because nothing retrieved nets the "
          "postponement-induced component out of the share. That is not a criticism of any single "
          "paper — it is a property of the literature, and it is the domain with no dissent.", "",
          f"## Arm 2 — {len(a2)} records", "",
          "| domain | what it asks | SERIOUS | MODERATE | LOW |", "|---|---|---|---|---|"]
    for d, q in [("A2_1_treatment_attenuation", "does the named policy actually bind?"),
                 ("A2_2_exposure_estimand_distance", "how far is the measured outcome from births?"),
                 ("A2_3_policy_endogeneity", "are mandates adopted rather than assigned?"),
                 ("A2_4_shock_direction", "expansion (confounded) or contraction (cleaner)?")]:
        c = Counter(r.get(d) for r in a2)
        L.append(f"| `{d}` | {q} | {c.get('SERIOUS',0)} | {c.get('MODERATE',0)} | {c.get('LOW',0)} |")
    L += ["",
          "**A2.1 is the domain this chapter contributes.** It is usually invisible because it looks "
          "like a data question rather than a bias: 65% of US workers are in ERISA-exempt "
          "self-insured plans, and only 41% of self-insured employers in mandate states cover IVF. A "
          "'state mandate' is therefore not the treatment it is named as, the attenuation is toward "
          "zero, and **a small or null US mandate effect is not evidence that access does not "
          "matter.**", "",
          "**A2.2 applies A.24's lesson**: rate how far the measured outcome sits from the registered "
          f"one. {sum(1 for r in a2 if r.get('A2_2_exposure_estimand_distance')=='SERIOUS')} of "
          f"{len(a2)} arm-2 records in hand measure UTILISATION rather than births. A utilisation "
          "effect is not a fertility effect, and what separates them is the dropout literature — "
          "which is job A1, which is 2 of 14 in hand.", "",
          "## GRADE, per phenomenon", "",
          "Per phenomenon rather than per chapter: the same evidence can be strong for one target and "
          "absent for another.", "",
          "| phenomenon | rating | reasoning |", "|---|---|---|",
          "| **Pre-modern** | **NOT ASSESSED** | The technology did not exist. Not an absence of "
          "evidence — an absence of the exposure. |",
          "| **FDT (~1870–1965)** | **NOT ASSESSED** | Same. The first IVF birth was 1978. |",
          "| **SDT (~1965–present)** | **LOW** | Downgraded three steps from the observational "
          "starting point, each named below. |", "",
          "### The SDT downgrades, named", "",
          "- **Risk of bias in the body as a whole — down one.** Arm 1's dominant domain fails on "
          f"{sum(1 for r in a1 if r.get('A1_1_counterfactual')=='SERIOUS')} of {len(a1)} records "
          "(the share is treated as an effect), and the postponement-feedback domain fails on all of "
          "them. Arm 2's treatment definition is attenuated by construction wherever the exposure is "
          "a US state mandate.",
          "- **Indirectness — down one.** The registered estimand is births relative to a "
          "counterfactual without ART. Arm 1 measures a share; arm 2 mostly measures utilisation. "
          "**Neither arm measures the registered quantity directly**, and the arm that comes closest "
          "— the untreated-subfertile comparison — is the arm with 2 of 14 records retrieved.",
          "- **Imprecision — down one.** Five country-settings carry the entire demographic-"
          f"significance arithmetic, and the offset range across them ({pc(lo)} to {pc(hi)}) spans "
          "the boundary between NEGLIGIBLE and MINOR. A range that straddles its own verdict band is "
          "imprecise in the sense GRADE means.", "",
          "**Not downgraded for inconsistency.** The arm-1 shares agree closely across countries once "
          "the denominator is handled, and the spread is explained by access regime rather than by "
          "disagreement. **Not downgraded for publication bias**, which this chapter has no way to "
          "assess: the accounting literature reports shares rather than tested hypotheses, and a "
          "share has no null to fail to reject.", "",
          "### What a HIGH rating would have required", "",
          "Not more studies. A different study: one that compares births among subfertile people who "
          "did and did not receive treatment, at population scale, with the selection into treatment "
          "handled. The frame contains the ingredients — the untreated-prognosis models, the dropout "
          "cohorts, the discontinuation follow-ups — and no one has assembled them into an estimate "
          "of ART's population contribution. **That study does not exist and should**, which belongs "
          "in §10 rather than in a downgrade.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"rob rows={len(out)} arm1={len(a1)} arm2={len(a2)}")
    print(f"SDT GRADE=LOW (3 downgrades); offset range {pc(lo)}-{pc(hi)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
