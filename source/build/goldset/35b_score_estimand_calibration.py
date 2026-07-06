#!/usr/bin/env python3
"""
Step 35b - Score the automated estimand gate against the RA ground truth.

Measures how well Sonnet's blind estimand-classification (step 35a + fleet, frozen in
estimand_calib_sonnet.json) agrees with the RA's inclusion decisions on the pilot's 40 reviewed
studies. This is what lets the production gate (which runs on Sonnet, not an RA, for new hypotheses)
carry a MEASURED precision/recall instead of an assumed one.

Two things are scored:
  1. The GATE DECISION (the one that matters): PRIMARY vs OFF. Confusion matrix, precision, recall,
     F1, accuracy, Cohen's kappa. A false positive = an off-cell paper wrongly admitted to the
     pooling set (pollutes the meta-analysis); a false negative = a primary paper wrongly dropped.
  2. The OFF-CELL BUCKET agreement (routing quality): when both agree a paper is off-cell, do they
     agree on WHY (which cell it belongs to instead). Bucket disagreement does not change the gate
     decision but affects which other chapter the paper is routed to.

Inputs
  source/build/goldset/estimand_calib_sonnet.json   Sonnet's blind classifications {id, cell, ...}
  temp/estimand-calib/key.json                      RA ground truth (ra_decision, estimand_cell)
Output
  output/{slug}-estimand-calibration.md
"""
import json, math
from pathlib import Path

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SONNET = HERE / "estimand_calib_sonnet.json"
KEY = REPO / "temp" / "estimand-calib" / "key.json"
OUT = REPO / "output" / f"{SLUG}-estimand-calibration.md"


def main():
    sonnet = {c["id"]: c for c in json.load(open(SONNET))}
    key = json.load(open(KEY))

    rows = []
    for rec_id, truth in key.items():
        s = sonnet.get(rec_id, {})
        ra_primary = truth.get("ra_decision") == "RETRIEVE"
        s_primary = s.get("cell") == "PRIMARY"
        rows.append({
            "id": rec_id, "title": truth.get("title", ""),
            "gold_id": truth.get("gold_id", ""),
            "ra_primary": ra_primary, "ra_cell": truth.get("estimand_cell", ""),
            "s_primary": s_primary, "s_cell": s.get("cell", ""),
            "s_reason": s.get("reason", ""),
        })

    # --- 1. gate decision (PRIMARY vs OFF) ---
    TP = sum(1 for r in rows if r["ra_primary"] and r["s_primary"])
    FP = sum(1 for r in rows if not r["ra_primary"] and r["s_primary"])
    FN = sum(1 for r in rows if r["ra_primary"] and not r["s_primary"])
    TN = sum(1 for r in rows if not r["ra_primary"] and not r["s_primary"])
    n = len(rows)
    precision = TP / (TP + FP) if (TP + FP) else float("nan")
    recall = TP / (TP + FN) if (TP + FN) else float("nan")
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else float("nan")
    accuracy = (TP + TN) / n
    # Cohen's kappa
    po = accuracy
    p_yes = ((TP + FP) / n) * ((TP + FN) / n)
    p_no = ((TN + FN) / n) * ((TN + FP) / n)
    pe = p_yes + p_no
    kappa = (po - pe) / (1 - pe) if (1 - pe) else float("nan")

    # --- 2. off-cell bucket agreement (both agree OFF) ---
    both_off = [r for r in rows if not r["ra_primary"] and not r["s_primary"]]
    bucket_match = sum(1 for r in both_off if r["ra_cell"] == r["s_cell"])

    # --- disagreements ---
    gate_disagree = [r for r in rows if r["ra_primary"] != r["s_primary"]]
    bucket_disagree = [r for r in both_off if r["ra_cell"] != r["s_cell"]]

    L = [f"# Estimand-gate calibration - {SLUG}", "",
         "How well the **automated** estimand gate (Sonnet, judging blind on title+abstract - GACS "
         "§D2b) reproduces the **RA's** inclusion decisions on the pilot's 40 reviewed studies. This "
         "gives the production gate a measured precision for hypotheses where there is no RA pass. "
         "Sonnet never saw the RA decision or the earlier relevance rationale.", "",
         "## 1. Gate decision: PRIMARY vs off-cell (the decision that matters)", "",
         f"- **Precision {precision:.0%}**  (of papers Sonnet admits to the pooling set, the share the RA also admits)",
         f"- **Recall {recall:.0%}**  (of papers the RA admits, the share Sonnet also admits)",
         f"- **Accuracy {accuracy:.0%}**, F1 {f1:.2f}, Cohen's kappa {kappa:.2f}", "",
         "| | RA primary | RA off-cell |", "|---|---|---|",
         f"| **Sonnet primary** | {TP} (TP) | {FP} (FP) |",
         f"| **Sonnet off-cell** | {FN} (FN) | {TN} (TN) |", "",
         f"The gate is **{'safe' if FP == 0 else 'leaky'}**: {FP} false positive"
         f"{'s' if FP != 1 else ''} means an off-cell paper "
         f"{'never enters' if FP == 0 else 'can enter'} the pooling set. The cost sits in the "
         f"{FN} false negative{'s' if FN != 1 else ''} - primary papers Sonnet drops, which a human "
         "gate on boundary cases recovers.", ""]

    if gate_disagree:
        L += ["### Gate disagreements (where a human gate still earns its place)", ""]
        for r in gate_disagree:
            verdict = "RA primary, Sonnet off" if r["ra_primary"] else "RA off, Sonnet primary"
            anc = f" [{r['gold_id']}]" if r["gold_id"] else ""
            L.append(f"- **{r['title']}**{anc} - {verdict}. RA: `{r['ra_cell']}`; Sonnet: "
                      f"`{r['s_cell']}` - \"{r['s_reason']}\"")
        L.append("")

    L += ["## 2. Off-cell bucket agreement (routing quality)", "",
          f"Of {len(both_off)} papers both call off-cell, **{bucket_match} ({bucket_match/len(both_off):.0%}) "
          "agree on which off-cell bucket** (i.e. why it leaves, hence where it routes). Bucket "
          "disagreements do not change the include/exclude decision - both exclude - but they change "
          "which other chapter the paper feeds.", ""]
    if bucket_disagree:
        L += ["Bucket disagreements:", ""]
        for r in bucket_disagree:
            L.append(f"- **{r['title']}** - RA `{r['ra_cell']}` vs Sonnet `{r['s_cell']}`")
        L.append("")

    L += ["## Reading", "",
          f"On the pilot the automated gate is **{precision:.0%} precise / {recall:.0%} recall** against "
          "the RA. High precision means the gate can be trusted to keep the pooling set clean without a "
          "human on every paper; the recall gap is concentrated in genuinely borderline estimands "
          "(direction/mechanism calls the abstract underdetermines), which is exactly the boundary band "
          "GACS reserves for the RA verdict (§D). So for a new hypothesis: run the automated gate, and "
          "route only its off-cell/borderline calls to the RA, not the whole set.", "",
          "**Caveats.** (1) n=40, one hypothesis - a rate, not a guarantee. (2) The RA decisions are "
          "themselves the ground truth; a Sonnet-RA disagreement can be the RA making a generous "
          "judgment call, not Sonnet erring (see the gate disagreements). (3) Classification was "
          "batched 10/agent; papers were judged independently but not in isolation. (4) 3 of 40 were "
          "title-only - the same abstract-dependence flagged for the Tier-B recall re-grade.", ""]

    OUT.write_text("\n".join(L) + "\n")
    print(f"gate: precision {precision:.0%}  recall {recall:.0%}  acc {accuracy:.0%}  kappa {kappa:.2f}")
    print(f"  TP {TP}  FP {FP}  FN {FN}  TN {TN}")
    print(f"bucket agreement (both-off): {bucket_match}/{len(both_off)} ({bucket_match/len(both_off):.0%})")
    print(f"gate disagreements: {len(gate_disagree)}  bucket disagreements: {len(bucket_disagree)}")
    print(f"written -> {OUT.name}")


if __name__ == "__main__":
    main()
