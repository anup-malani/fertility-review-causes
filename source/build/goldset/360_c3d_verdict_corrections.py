#!/usr/bin/env python3
"""360 — apply the corrections the verdict audit (359) surfaced, each with its reason recorded.

359 found 21 hard violations in the hand-entered screen. This applies the fixes. Corrections are
listed explicitly, one row at a time, with the reason -- never a blanket rewrite, because the thing
being corrected is a judgement and a script that silently re-judges destroys the audit trail.

THREE CLASSES, and the second is the one that changes a headline number.

1. SHADOW RECORDS THAT REACHED AN ESTIMAND CELL. Fourteen paratext records are in the universe:
   peer reviews, comments, and three "Replication data for: <parent title>" deposits. The deposits
   carry the parent study's title verbatim, so I read the title and gave the DEPOSIT the parent's
   cell -- one landed in SHOCK_FERTILITY, one in QQ_SUBSTITUTION, one in THEORY.
   `replication-deposits-are-shadow-records`: same title, same authors, same year, so the title
   gate, the author gate and the year gate all pass and none of them discriminates. All fourteen
   are OFF_TOPIC.

   ROOT CAUSE, and it is a repo defect rather than a screening slip: 348 (free seeds) runs a SHADOW
   gate; 353 (screen universe) does not. The gate was written for the mining path and never applied
   to the query pull. Fixed in 353 in the same commit.

2. PRIMARY CELLS WITHOUT A FERTILITY OUTCOME. Ten rows sat in RETURN_FERTILITY or SHOCK_FERTILITY
   while carrying outcome_object OTHER or INVESTMENT_PER_CHILD. That combination cannot be right:
   a primary cell is primary BECAUSE its dependent variable is fertility, and a demographic-
   significance share needs a fertility numerator (scope §2, §5). Re-read individually below. Eight
   are trade/technology shocks whose outcome is infant health, talent allocation or manufacturing
   -- link 1 evidence with no link 3 -- and two are the Production-of-Human-Capital pair, which
   estimates the joint determination but reports investment per child, so it belongs in link 2.

   This lowers the primary count. That is the point of auditing before writing a verdict.

3. `design` FILLED ON OFF_TOPIC ROWS. Cosmetic: eleven excluded rows carry design=REVIEW. Set to NA
   so the invariant holds and the design counts mean what they say.

Output: rewrites the verdict CSV in place and writes
literature/search-logs/quantity-quality-tradeoff-verdict-corrections.md
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
VERD = ROOT / "extraction" / "quantity-quality-tradeoff-screen-verdicts.csv"
FIELDS = ["screen_id", "direction", "cell", "design", "wall_risk", "outcome_object",
          "title_only", "confidence", "note", "rater"]

# (screen_id, new cell, new direction, new outcome_object, reason)
CORRECTIONS = [
    # --- 1. shadow records given an estimand cell
    ("C3D2222", "OFF_TOPIC", "NA", "NA",
     "REPLICATION DATA DEPOSIT for Aaronson et al, not the study; it carried the parent title "
     "verbatim and was routed to SHOCK_FERTILITY on that basis"),
    ("C3D2275", "OFF_TOPIC", "NA", "NA",
     "replication data deposit for the economic and demographic transition paper, not the study"),
    ("C3D2279", "OFF_TOPIC", "NA", "NA",
     "replication data deposit for All for One, not the study; was in QQ_SUBSTITUTION"),

    # --- 2. primary cells whose dependent variable is not fertility
    ("C3D1633", "OFF_OTHER", "NA", "OTHER",
     "Brazil commodities-for-manufactures boom; the outcome is manufacturing, not fertility. "
     "Link-1 evidence with no link 3"),
    ("C3D2379", "OFF_OTHER", "NA", "OTHER",
     "SSRN copy of the Brazil trade boom; same reason"),
    ("C3D1667", "OFF_OTHER", "NA", "OTHER",
     "import competition and INFANT HEALTH; a trade shock with a child-health outcome, so neither "
     "a fertility numerator nor a family-size exposure"),
    ("C3D0625", "OFF_OTHER", "NA", "OTHER",
     "journal copy of the Brazil trade reform and infant health; same reason"),
    ("C3D0465", "OFF_OTHER", "NA", "OTHER",
     "population density migration and returns to human capital and land; measures the return but "
     "reports no fertility outcome"),
    ("C3D2263", "OFF_OTHER", "NA", "OTHER",
     "skill-biased imports and the allocation of talent; the SBTC exposure with no fertility "
     "outcome -- link 1 only"),
    ("C3D3059", "OFF_OTHER", "NA", "OTHER",
     "anticipated children -> the PARENT's educational investment; that is fertility driving "
     "education, the reverse of the registered claim"),
    ("C3D3169", "OFF_OTHER", "NA", "OTHER",
     "how demography shapes the returns to automation; the reverse direction"),
    ("C3D0110", "QQ_SUBSTITUTION", "BOTH", "INVESTMENT_PER_CHILD",
     "The Production of Human Capital estimates endowments, investments AND fertility jointly, but "
     "its reported dependent variable is investment per child, so it is link-2 mechanism evidence "
     "and cannot carry a demsig numerator"),
    ("C3D0526", "QQ_SUBSTITUTION", "BOTH", "INVESTMENT_PER_CHILD",
     "RePEc copy of the same paper; same reason"),
]

# 3. design must be NA on excluded rows
DESIGN_NA_ON_OFFTOPIC = True


def main():
    rows = list(csv.DictReader(VERD.open()))
    by_id = {r["screen_id"]: r for r in rows}
    applied, missing = [], []

    for sid, cell, direction, outcome, reason in CORRECTIONS:
        r = by_id.get(sid)
        if r is None:
            missing.append(sid)
            continue
        applied.append({"screen_id": sid, "from_cell": r["cell"], "to_cell": cell,
                        "from_outcome": r["outcome_object"], "to_outcome": outcome,
                        "reason": reason})
        r["cell"], r["direction"], r["outcome_object"] = cell, direction, outcome
        if cell in ("OFF_TOPIC", "OFF_OTHER"):
            r["design"] = "NA" if cell == "OFF_TOPIC" else r["design"]
        r["note"] = (r["note"] + " [CORRECTED by 360: " + reason[:70] + "]")[:300]

    n_design = 0
    if DESIGN_NA_ON_OFFTOPIC:
        for r in rows:
            if r["cell"] == "OFF_TOPIC" and r["design"] != "NA":
                r["design"] = "NA"
                n_design += 1

    if missing:
        raise SystemExit(f"correction targets not present in the verdict file: {missing}")

    with VERD.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})

    L = ["# C.3.d verdict corrections", "",
         "Generated by `source/build/goldset/360_c3d_verdict_corrections.py`. Do not edit by hand.",
         "",
         f"**{len(applied)} routing corrections** from the 359 audit, plus **{n_design}** rows "
         "where `design` was cleared on an excluded row.", "",
         "Each correction is listed with its reason. The audit found these as INVARIANT violations "
         "— a primary cell whose dependent variable is not fertility cannot be primary, because a "
         "demographic-significance share needs a fertility numerator.", "",
         "| screen id | from | to | reason |", "|---|---|---|---|"]
    L += [f"| `{a['screen_id']}` | `{a['from_cell']}` | `{a['to_cell']}` | {a['reason']} |"
          for a in applied]
    L.append("")
    (LOGS / "quantity-quality-tradeoff-verdict-corrections.md").write_text("\n".join(L))
    (LOGS / "quantity-quality-tradeoff-verdict-corrections.json").write_text(
        json.dumps({"corrections": applied, "design_cleared": n_design}, indent=2) + "\n")
    print(f"{len(applied)} routing corrections applied; {n_design} design fields cleared")
    for a in applied:
        print(f"  {a['screen_id']}  {a['from_cell']:18} -> {a['to_cell']:16} {a['reason'][:60]}")


main()
