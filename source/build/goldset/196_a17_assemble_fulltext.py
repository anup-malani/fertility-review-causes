#!/usr/bin/env python3
"""
196_a17_assemble_fulltext.py — A.17, stage 6. Assemble the full-text screen.

**PROVISIONAL BY CONSTRUCTION.** This assembles 33 of 131 wanted records. The report leads with that
fraction, states it per cell, and refuses to print a verdict sentence for any cell whose retrieval is
too thin to support one. A provisional pass whose output reads like a finished one becomes the
chapter by default.

THE ONE NUMBER THIS STAGE EXISTS TO PRODUCE is the distribution of `counterfactual_treatment` across
ARM 1. Arm 1 computes ART's contribution by counting ART births. That count equals the causal effect
only if no ART birth would have occurred otherwise. Whether each paper CONFRONTS that — and how — is
a property of the literature, readable from its methods section, and not an opinion about it.

A FIFTH VALUE WAS ADDED FROM THE DATA, and it is the interesting one. The prep script defined
`none_stated` / `assumed_zero` / `partial` / `estimated`. The Czech contribution paper fits none of
them: it concedes in a single clause that some ART-attributed births would have happened anyway,
cites the spontaneous-conception literature for it, characterises the overestimate as 'low' WITHOUT A
NUMBER, and then subtracts anyway. That is not silence and it is not an adjustment. It is
`acknowledged_unquantified`, and it is likely the modal case in a literature that knows about the
problem and has no way to price it. Same shape as the `medical_non_onco` value the D2 assembly had to
add to Wall 5: when a residue does not fit the taxonomy, check whether the taxonomy is short a value
before concluding the records are ambiguous.

Output: literature/search-logs/{slug}-fulltext-summary.md
        extraction/{slug}-fulltext-screened.json
"""
import json, os, sys
from collections import Counter

SLUG = "art-access-fertility-recovery"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
WORK = os.path.join(EXTRACT, f"{SLUG}-fulltext-worklist.json")
VERD = os.path.join(HERE, "a17_fulltext", "verdicts_fulltext.json")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OUT_JSON = os.path.join(EXTRACT, f"{SLUG}-fulltext-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-fulltext-summary.md")

JOB_TARGET = {"A1_COUNTERFACTUAL": 14, "A2_IDENTIFIED": 33, "A3_SHARE": 25,
              "A4_P5_CONVERSION": 11, "A5_P6_BEHAVIOUR": 16, "B_NO_ABSTRACT": 27,
              "C_EXPOSURE_SERIES": 5}
CF_ORDER = ["none_stated", "assumed_zero", "acknowledged_unquantified", "partial", "estimated"]
CF_GLOSS = {
    "none_stated": "the share is presented without any statement of what would have happened otherwise",
    "assumed_zero": "explicitly derives non-ART births by subtraction, so every ART birth is treated as additional",
    "acknowledged_unquantified": "**concedes the problem, cites the literature for it, gives no number, and subtracts anyway**",
    "partial": "adjusts for or conditions on something — dropout, conception mode, selection",
    "estimated": "a counterfactual is actually estimated or a comparison group is used",
}


def main():
    work = {r["id"]: r for r in json.load(open(WORK))}
    oa = {r["id"]: r for r in json.load(open(OA))}
    raw = json.load(open(VERD))["verdicts"]

    placeholders = [v for v in raw if v["reported_quantity"] == "NOT RETRIEVED"]
    verdicts = [v for v in raw if v["reported_quantity"] != "NOT RETRIEVED"]

    missing = sorted(set(work) - {v["id"] for v in verdicts})
    phantom = sorted({v["id"] for v in verdicts} - set(work))
    if missing or phantom:
        sys.stderr.write("ABORT: coverage is not exact.\n")
        if missing:
            sys.stderr.write(f"  {len(missing)} readable records with no verdict: {missing[:8]}\n")
        if phantom:
            sys.stderr.write(f"  {len(phantom)} verdicts not in the worklist: {phantom[:8]}\n")
        sys.exit(1)

    merged = []
    for v in verdicts:
        m = dict(work[v["id"]])
        m.update({k: v[k] for k in ("arm_resolved", "counterfactual_treatment",
                                    "reported_quantity", "note")})
        merged.append(m)
    json.dump(merged, open(OUT_JSON, "w"), indent=2)

    n = len(merged)
    arm1 = [m for m in merged if m["arm_resolved"] == "arm1_counting"]
    arm2 = [m for m in merged if m["arm_resolved"] == "arm2_estimate"]
    cf = Counter(m["counterfactual_treatment"] for m in arm1)
    byjob = Counter(m["job"] for m in merged)
    pc = lambda a, b: f"{a / max(b, 1):.0%}"

    L = [f"# Stage 6 full-text screen — {SLUG} (A.17)", "",
         f"> **PROVISIONAL: {n} of 131 wanted records.** 67 are blocked-but-open (a browser, no "
         "institutional access) and 31 need a proxy. Every section below states its own retrieval "
         "fraction, and cells too thin to support a verdict say so instead of stating one.", "",
         "## Retrieval by job — read every result below against this table", "",
         "| job | in hand | wanted | share | what a gap here costs |", "|---|---|---|---|---|"]
    COST = {"A1_COUNTERFACTUAL": "**the chapter's headline number is conditional on this job**",
            "A2_IDENTIFIED": "the only identified evidence; unrecoverable by another route",
            "A3_SHARE": "arm 1's numerator",
            "A4_P5_CONVERSION": "P5's entire verdict",
            "A5_P6_BEHAVIOUR": "the difference between 'unmeasured' and 'measured and weak'",
            "B_NO_ABSTRACT": "records the screen could not read at all",
            "C_EXPOSURE_SERIES": "stage 10 inputs"}
    for j, t in JOB_TARGET.items():
        g = byjob.get(j, 0)
        L.append(f"| `{j}` | {g} | {t} | {pc(g, t)} | {COST.get(j, '')} |")
    L += ["",
          "## The result this stage exists to produce", "",
          f"**Arm 1 has {len(arm1)} records in hand. How each one handles the counterfactual:**", "",
          "| treatment | n | what it means |", "|---|---|---|"]
    for k in CF_ORDER:
        if cf.get(k):
            L.append(f"| `{k}` | {cf[k]} | {CF_GLOSS[k]} |")
    confront = cf.get("partial", 0) + cf.get("estimated", 0)
    L += ["",
          f"**{cf.get('none_stated',0) + cf.get('assumed_zero',0) + cf.get('acknowledged_unquantified',0)} "
          f"of {len(arm1)} arm-1 records in hand report a contribution WITHOUT confronting the "
          f"counterfactual; {confront} confront it.**", "",
          "This is the chapter's central finding in its provisional form, and it is a statement "
          "about the literature rather than about ART. Arm 1's number is a share of births. Reading "
          "it as an effect requires that no ART birth would have occurred otherwise, and most of "
          "this literature does not argue that — it does not raise it.", "",
          "### The exhibit", "",
          "The Czech contribution paper is the case worth quoting, because it is not ignorance. It "
          "builds a `TFR_nonART` series by pure subtraction, stated as its equation (1). It also "
          "concedes, in one clause, that 'the albeit low overestimation of the number of ART births "
          "due to the possibility that some women became pregnant via sexual intercourse following "
          "ART cannot be excluded', and cites for it a five-year follow-up of couples who "
          "DISCONTINUED ICSI treatment. The words 'spontaneous', 'discontinued', and that author's "
          "name appear **zero times in the body of the paper**. The overestimate is called 'low' and "
          "never given a number.", "",
          "**The counterfactual literature is known to the accounting literature, cited by it, "
          "characterised without measurement, and not used.** That is a sharper and more citable "
          "finding than unawareness would have been — and it is why the fifth taxonomy value, "
          "`acknowledged_unquantified`, had to be added from the data.", "",
          f"**The gate: job A1 is {byjob.get('A1_COUNTERFACTUAL', 0)} of 14 in hand.** The chapter "
          "cannot yet say how large the correction should be — only that the literature mostly does "
          "not make one. Those are different claims and only the second is currently supported.", "",
          "## The arm split, resolved", "",
          f"D2 left 14.4% of the worklist at `cannot_tell`. Full text resolved every record it "
          f"reached: **{len(arm1)} arm-1, {len(arm2)} arm-2**, "
          f"{sum(1 for m in merged if m['arm_resolved'] == 'neither')} neither, "
          f"{sum(1 for m in merged if m['arm_resolved'] == 'cannot_tell')} still undecidable.", "",
          "Three D2 `cannot_tell` records resolved in ways worth recording: the Israeli "
          "unlimited-access study and the Russian insurance study both resolved to **arm 2**, and "
          "China's ART coverage analysis resolved **against the cell** — it is a feasibility and "
          "costing exercise for a prospective policy, not an estimate of a birth response.", "",
          "## What is now supportable, and what is not", ""]
    L += ["**Supportable on what is in hand:**", "",
          "- Most of the arm-1 literature reports ART's share of births without confronting the "
          "counterfactual, and at least one paper cites the contrary literature while declining to "
          "quantify it.",
          "- Arm 2 has real identified variation, and at least one setting — Israel under unlimited "
          "publicly funded access — shows treatment expanding at ages 40-44 with **no substantial "
          "change in age-specific birth rates** and a falling yield of live births per treatment.",
          "- Every US mandate estimate is attenuated by construction: **65% of workers are in "
          "self-insured plans exempt under ERISA, and only 41% of self-insured employers in mandate "
          "states cover IVF.** A small or null mandate effect is therefore not evidence that access "
          "does not matter.",
          "- P6 is better characterised as **measured and weak** than as unmeasured. The one direct "
          "individual-level test finds the postponement association in the key age band is **not "
          "statistically significant**, finds no effect before the thirties, and its authors call "
          "the pathway 'possible but weak'.",
          "- v5's clause that ART's contribution is growing is not supported by the projection in "
          "hand: Italy's MAR share is projected essentially flat, 3.9% to 4.3%, to 2050.", "",
          "**NOT supportable, and the chapter must not imply otherwise:**", "",
          f"- **Any magnitude for the counterfactual correction.** Job A1 is "
          f"{byjob.get('A1_COUNTERFACTUAL', 0)} of 14.",
          "- **Any verdict on P5.** The decisive record — the 10-15 year return-rate follow-up — is "
          "blocked-but-open and not in hand. The three P5 records retrieved report very small live-"
          "birth yields, but 'we could not download it' is not 'nobody measured it'.",
          "- **Any pooled statement across the two arms.** They answer different questions and the "
          f"counts ({len(arm1)} and {len(arm2)}) are of two literatures, not two halves of one.", ""]
    if placeholders:
        L += ["## Recorded absences", "",
              "Records named in the verdict file as NOT RETRIEVED, so their absence appears in the "
              "cell summaries rather than passing silently:", ""]
        for p in placeholders:
            L.append(f"- `{p['id'].replace('_ABSENT','')}` ({p['job']}) — {p['note']}")
        L += [""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"screened={n} arm1={len(arm1)} arm2={len(arm2)}")
    print("counterfactual across arm 1:", dict(cf))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
