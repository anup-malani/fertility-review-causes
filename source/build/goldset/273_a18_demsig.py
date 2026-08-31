#!/usr/bin/env python3
"""273 — A.18 demographic significance. TICK-076.

Ruling 1 puts the FDT and SDT demsig arms on the **selection response**, R = h2 x S,
because their §4.2.1 denominators are changes in a mean and a variance component has
no numerator for them. PM gets a variance cell, contingent on the units question
escalated to Anup.

**The result is NOT ASSESSED for FDT and SDT, and the reason is specific.** R needs
two inputs. h2 the chapter has, in quantity. **S — the selection differential on a
fertility-associated genetic measure — is absent from the extracted evidence.** Its
cell, `PREDICTED_RESPONSE`, holds 6 screened studies of which 1 was retrieved and
that one turned out to be a coalescent simulation, so the cell is empty. The three
selection quantities that WERE extracted are on the wrong exposure: a gradient on
height, a gradient on BMI, and an opportunity-for-selection index. None is S on a
fertility genotype.

That is a different verdict from "the effect is small", and the chapter must not
round it to one: **UNEVALUATED, not weak.** GRADE and §4.2 have no category for an
empty cell, and reporting a small number computed from absent inputs would be worse
than reporting none.

What IS computable is the inversion: given the observed h2 range and the §4.2.1
denominator, **how large would S have to be** for the response to reach the 10%
significance threshold? That bound is derived here, because it is the quantity a
reader needs to judge whether the missing evidence could plausibly change the
verdict.

**The denominator is not invented.** §4.2.1 fixes it as the fall in completed
fertility over the phenomenon's full definitional window, sourced from HFD/WPP.
`data/raw/` is empty on this branch, so the denominator is left as a named
parameter and the inversion is reported per unit of it. Substituting a number I did
not source would be the exact failure §4.2.1 rule 4 exists to prevent.

Usage: python3 source/build/goldset/273_a18_demsig.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSVP = ROOT / "extraction" / "heritability-fertility-genetic.csv"
OUT = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-demsig.json"
OUT_MD = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-demsig.md"

USABLE = ("VERIFIED", "VERIFIED_AUTHORS_PREFERRED", "VERIFIED_NULL",
          "VERIFIED_CELL_RECLASSIFIED_FROM_H2_FERTILITY",
          "VERIFIED_SPECIFICATION_DISCORDANT", "VERIFIED_NON_H2_ESTIMAND")
THRESHOLD = 0.10          # §4.2 significance threshold
GENERATIONS_SDT = 2.0     # 1965-2025 at a generation length to be taken from the data
GENERATIONS_FDT = 3.0     # 1870-1965


def main():
    rows = [r for r in csv.DictReader(CSVP.open()) if r["extraction_status"] in USABLE]
    h2 = []
    for r in rows:
        if not r["estimand"].startswith("h2"):
            continue
        try:
            v = float(str(r["estimate"]).split("->")[0])
        except ValueError:
            continue
        h2.append({"study": r["study"][:60], "estimand": r["estimand"],
                   "outcome": r["outcome_measure"], "relatedness": r["relatedness_level"],
                   "h2": v})
    S_rows = [r for r in rows if "selection" in (r["estimand"] or "").lower()
              or "opportunity" in (r["estimand"] or "").lower()]

    vals = sorted(x["h2"] for x in h2)
    hmin, hmax = (vals[0], vals[-1]) if vals else (None, None)
    # inversion: R = h2 * S * G ; share = R / D ; solve for S at share = THRESHOLD
    inv = {}
    for label, G in (("SDT", GENERATIONS_SDT), ("FDT", GENERATIONS_FDT)):
        inv[label] = {
            "generations": G,
            "required_S_per_unit_denominator_at_h2_max": (
                round(THRESHOLD / (hmax * G), 4) if hmax else None),
            "required_S_per_unit_denominator_at_h2_min": (
                round(THRESHOLD / (hmin * G), 4) if hmin else None),
            "reading": ("S must exceed this multiple of the denominator (in children per woman) "
                        "for the genetic response to reach a 10% share"),
        }

    payload = {
        "ticket": "TICK-076",
        "verdict": {
            "PM": "CONTINGENT — a variance cell is opened by Ruling 1 but its units question "
                  "(within-population between-individual variance against a between-population "
                  "range) is escalated to the PI and unresolved.",
            "FDT": "NOT ASSESSED — S is absent from the evidence base.",
            "SDT": "NOT ASSESSED — S is absent from the evidence base.",
        },
        "why_not_assessed": {
            "required_inputs": ["h2 (available)", "S: selection differential on a "
                                "fertility-associated genetic measure (ABSENT)"],
            "predicted_response_cell": "6 screened, 1 retrieved, and that one reclassified out as a "
                                       "coalescent simulation. The cell is empty.",
            "selection_quantities_actually_extracted": [
                {"study": r["study"][:60], "estimand": r["estimand"], "estimate": r["estimate"]}
                for r in S_rows],
            "why_they_do_not_substitute": "gradients on height and BMI and an opportunity-for-"
                                          "selection index are selection on phenotypes, not S on a "
                                          "fertility-associated genotype. Using them would answer a "
                                          "different question.",
            "this_is_not_a_small_effect": "UNEVALUATED, not weak. No number is computed because the "
                                          "inputs are absent, not because they are near zero.",
        },
        "h2_evidence": {"n_estimates": len(h2), "min": hmin, "max": hmax, "estimates": h2},
        "denominator": {
            "status": "NOT SOURCED ON THIS BRANCH",
            "rule": "§4.2.1: the fall in completed fertility over the phenomenon's FULL "
                    "definitional window, from HFD/WPP; data/raw is empty here.",
            "consequence": "the inversion below is reported per unit of denominator, not as a share",
        },
        "inversion_how_large_would_S_have_to_be": inv,
    }
    OUT.write_text(json.dumps(payload, indent=2))

    md = ["# A.18 demographic significance\n",
          "| phenomenon | verdict |\n|---|---|",
          "| PM | **CONTINGENT** — variance cell open, units question with the PI |",
          "| FDT | **NOT ASSESSED** |",
          "| SDT | **NOT ASSESSED** |",
          "\n## Why NOT ASSESSED, precisely\n",
          "R = h² × S needs two inputs. The chapter has h² in quantity "
          f"({len(h2)} estimates, range {hmin}–{hmax}). It does not have **S**, the selection "
          "differential on a fertility-associated genetic measure. `PREDICTED_RESPONSE` held 6 "
          "screened studies; 1 was retrieved; that one was a coalescent simulation and was "
          "reclassified out. The cell is empty.\n",
          "\nThree selection quantities were extracted — a gradient on height, a gradient on BMI, "
          "and an opportunity-for-selection index by wealth class. **None is S on a fertility "
          "genotype**, and substituting one would answer a different question.\n",
          "\n> **This is UNEVALUATED, not weak.** No number is computed because the inputs are "
          "absent, not because they are near zero. Rounding an empty cell to \"small effect\" would "
          "assert a finding the evidence does not contain.\n",
          "\n## How large would S have to be?\n",
          "The denominator is *not* sourced on this branch (`data/raw/` is empty), so the inversion "
          "is per unit of denominator rather than as a share — §4.2.1 rule 4 requires the "
          "denominator be named wherever a share is given.\n",
          "\n| phenomenon | generations | required S at h²=max | required S at h²=min |\n|---|---|---|---|"]
    for k, v in inv.items():
        md.append(f"| {k} | {v['generations']} | {v['required_S_per_unit_denominator_at_h2_max']} | "
                  f"{v['required_S_per_unit_denominator_at_h2_min']} |")
    md.append("\nRead as: S must exceed that multiple of the observed decline, per generation, for "
              "the genetic response to reach a 10% share. Whether any plausible S approaches it is "
              "exactly what the five unretrieved `PREDICTED_RESPONSE` studies would settle.\n")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(json.dumps({"verdict": payload["verdict"],
                      "h2_estimates": len(h2), "h2_range": [hmin, hmax],
                      "S_available": len(S_rows), "inversion": inv}, indent=1))


if __name__ == "__main__":
    main()
