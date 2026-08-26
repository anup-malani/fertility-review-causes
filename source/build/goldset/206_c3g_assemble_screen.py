#!/usr/bin/env python3
"""
206_c3g_assemble_screen.py — C.3.g, stage D3. Assemble the title/abstract screen.

Joins the 12 batch verdict files back onto the D1 worklist, validates coverage, and writes the
screen summary.

COVERAGE IS ASSERTED, NOT ASSUMED: every worklist record must carry exactly one verdict, and any
verdict whose id is not in the worklist aborts the run. A.12's first assembly caught a phantom id
introduced by a single-digit typo this way.

FIVE THINGS THIS SCRIPT MEASURES THAT THE SCREEN ALONE CANNOT.

1. THE ARM SPLIT'S VISIBILITY — the disagreement between the scope and A4, now settled by the screen.
   The scope called C.3.g's arm routing "largely visible" at title/abstract; A4 measured 77% of
   in-frame records carrying exactly one outcome axis. The screen is the tiebreak and the statistic
   is the SHARE OF `cannot_tell` and of `outcome: multiple` among RELEVANT records — not the
   accuracy of the assignments, which nothing here can check.

2. THE DIRECT ARM'S SIZE, WHICH IS THE CHAPTER'S HEADLINE. Every prior stage has predicted that
   C.3.g's registered estimand is thin and its neighbour is not. This is the first stage that counts
   it on read records rather than on vocabulary.

3. PER-BYPASS YIELD. The standing rule from A.12: an inherited bypass that has stopped paying gets
   retired rather than carried forever. Each bypass's RELEVANT rate is reported separately, and
   `sole_reason` yield answers the sharper question — what would have been LOST without it.

4. THE NO-ABSTRACT PENALTY. D1 flagged 169 title-only records (28% of the worklist) and the rubric
   told the screener to bucket them `info: insufficient` rather than NOT_RELEVANT. Whether that
   instruction bound is checkable here: compare verdict distributions with and without an abstract.
   A title-only record returning NOT_RELEVANT at the same rate as an abstracted one means the
   instruction did not bind and the screen has been converting missing metadata into negative
   evidence. This chapter cannot afford that failure — its most-cited primary-cell anchor and both
   of its policy-variation preprints are title-only.

5. SCREENER-VERSUS-TERM-MATCH DISAGREEMENT. The screener never saw D1's hit lists, so the two
   readings are independent and can be crossed. A record the screener calls `design: identified`
   with no identification term, or `exposure: own_student_debt` with no debt term, is either a
   screener error or a vocabulary hole — and which one it is decides whether the frame or the rubric
   gets fixed.

Output: literature/search-logs/{slug}-screened.json
        literature/search-logs/{slug}-screen-summary.md
"""
import json, os, sys, glob
from collections import Counter, defaultdict

SLUG = "student-debt-household-formation"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
RANKED = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
VERDICT_DIR = os.path.join(HERE, "c3g_screen_verdicts")
OUT = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-screen-summary.md")

FIELDS = ("verdict", "exposure", "outcome", "arm", "design", "attain_conditioned", "wall", "info")
VALID = {
 "verdict": {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"},
 "exposure": {"own_student_debt", "parent_held_debt", "general_debt", "tuition_or_aid_policy",
              "none", "cannot_tell"},
 "outcome": {"fertility", "union_formation", "housing_residence", "multiple", "other", "none",
             "cannot_tell"},
 "arm": {"direct", "chain", "mechanism", "off", "cannot_tell"},
 "design": {"identified", "associational", "descriptive", "qualitative", "review", "simulation",
            "cannot_tell"},
 "attain_conditioned": {"yes", "no", "cannot_tell"},
 "wall": {"none", "w1_career", "w2_general_debt", "w3_repayment", "w4_access_to_college",
          "w5_6_parent_balance", "w7_lmic", "w8_reverse"},
 "info": {"sufficient", "insufficient"},
}


def main():
    recs = json.load(open(RANKED))
    work = {r["id"]: r for r in recs if r.get("in_worklist")}

    verdicts, dupes, bad_vals = {}, [], []
    for p in sorted(glob.glob(os.path.join(VERDICT_DIR, "verdict_*.json"))):
        for v in json.load(open(p)):
            if v["id"] in verdicts:
                dupes.append(v["id"])
            verdicts[v["id"]] = v
            for f in FIELDS:
                if v.get(f) not in VALID[f]:
                    bad_vals.append((v["id"], f, v.get(f)))

    missing = sorted(set(work) - set(verdicts))
    phantom = sorted(set(verdicts) - set(work))
    if missing or phantom or dupes or bad_vals:
        sys.stderr.write("ABORT: screen coverage is not exact.\n")
        if missing:
            sys.stderr.write(f"  {len(missing)} worklist records with NO verdict: {missing[:8]}\n")
        if phantom:
            sys.stderr.write(f"  {len(phantom)} verdicts for ids not in the worklist: {phantom[:8]}\n")
        if dupes:
            sys.stderr.write(f"  {len(dupes)} duplicate verdicts: {dupes[:8]}\n")
        if bad_vals:
            sys.stderr.write(f"  {len(bad_vals)} invalid field values: {bad_vals[:8]}\n")
        sys.exit(1)

    for rid, v in verdicts.items():
        work[rid].update({f"screen_{k}": v[k] for k in FIELDS})
        work[rid]["screen_note"] = v.get("note", "")
    json.dump(list(work.values()), open(OUT, "w"), indent=2)

    V = Counter(v["verdict"] for v in verdicts.values())
    rel = [work[i] for i, v in verdicts.items() if v["verdict"] == "RELEVANT"]
    unc = [work[i] for i, v in verdicts.items() if v["verdict"] == "UNCERTAIN"]
    pool = rel + unc

    arm = Counter(r["screen_arm"] for r in rel)
    outc = Counter(r["screen_outcome"] for r in rel)
    des = Counter(r["screen_design"] for r in rel)
    att = Counter(r["screen_attain_conditioned"] for r in rel)
    walls = Counter(v["wall"] for v in verdicts.values() if v["wall"] != "none")
    expo = Counter(r["screen_exposure"] for r in rel)

    # --- direct arm, the chapter's registered estimand ---
    direct = [r for r in rel if r["screen_arm"] == "direct"]
    chain = [r for r in rel if r["screen_arm"] == "chain"]
    direct_id = [r for r in direct if r["screen_design"] == "identified"]
    chain_id = [r for r in chain if r["screen_design"] == "identified"]

    # --- bypass yield ---
    by = defaultdict(lambda: [0, 0, 0, 0])   # reason -> [n, relevant, sole_n, sole_relevant]
    for r in work.values():
        v = verdicts[r["id"]]["verdict"]
        for reason in r["worklist_reason"]:
            by[reason][0] += 1
            by[reason][1] += (v == "RELEVANT")
            if len(r["worklist_reason"]) == 1:
                by[reason][2] += 1
                by[reason][3] += (v == "RELEVANT")

    # --- no-abstract penalty ---
    absd = {True: Counter(), False: Counter()}
    infod = {True: Counter(), False: Counter()}
    for r in work.values():
        k = bool(r.get("has_abstract"))
        absd[k][verdicts[r["id"]]["verdict"]] += 1
        infod[k][verdicts[r["id"]]["info"]] += 1

    # --- screener vs term-match disagreement ---
    dis_ident = [r for r in rel if r["screen_design"] == "identified" and not r["ident_hits"]]
    dis_debt = [r for r in rel if r["screen_exposure"] == "own_student_debt" and not r["debt_hits"]]
    dis_fert = [r for r in rel if r["screen_outcome"] in ("fertility", "multiple")
                and not r["fert_hits"]]

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    L = [f"# D3 title/abstract screen — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/206_c3g_assemble_screen.py`", "",
         f"**{len(work):,} worklist records screened, coverage exact** — every record carries "
         f"exactly one verdict and no verdict names a record outside the worklist.", "",
         f"**{V['RELEVANT']} RELEVANT · {V['UNCERTAIN']} UNCERTAIN · {V['NOT_RELEVANT']} "
         f"NOT_RELEVANT.**", "",
         "## The direct arm is the chapter, and it is small", "",
         f"| Arm | Records | Of which identified |", "|---|---|---|",
         f"| **direct** — own debt → a FERTILITY outcome (the registered estimand) | "
         f"**{len(direct)}** | **{len(direct_id)}** |",
         f"| chain — own debt → marriage, housing or residential independence | {len(chain)} | "
         f"{len(chain_id)} |",
         f"| mechanism / off / cannot_tell among RELEVANT | "
         f"{len(rel) - len(direct) - len(chain)} | — |", "",
         "Every earlier stage predicted this shape from vocabulary. This is the first count taken "
         "on records that were actually read, and it holds: the chapter's own estimand is a "
         "minority of its own evidence base, and the identified studies are concentrated in the "
         "arm that answers the neighbouring question.", "",
         "## Measurement 1 — is the arm routing visible at title and abstract?", "",
         f"Among RELEVANT records, `arm: cannot_tell` is **{arm.get('cannot_tell', 0)} of "
         f"{len(rel)} ({pc(arm.get('cannot_tell', 0), len(rel))})** and `outcome: multiple` is "
         f"**{outc.get('multiple', 0)} ({pc(outc.get('multiple', 0), len(rel))})**. A record with "
         "multiple estimated outcomes is not routable at screen even when the screener can see "
         "exactly what it does.", "",
         "| Field | Distribution among RELEVANT |", "|---|---|",
         f"| arm | {dict(arm)} |",
         f"| outcome | {dict(outc)} |",
         f"| design | {dict(des)} |",
         f"| exposure | {dict(expo)} |",
         f"| attain_conditioned | {dict(att)} |", "",
         "## Measurement 2 — the attainment confound, as the screener read it", "",
         f"`attain_conditioned: yes` on {att.get('yes', 0)} of {len(rel)} RELEVANT records "
         f"({pc(att.get('yes', 0), len(rel))}), `no` on {att.get('no', 0)}, `cannot_tell` on "
         f"{att.get('cannot_tell', 0)}. The scope declared this invisible at title/abstract from 8 "
         "query-level records and A4 revised it to a screen flag at 28% of in-frame records. The "
         "screen's own read is the third measurement of the same quantity and the one the "
         "risk-of-bias stage inherits.", "",
         "## Measurement 3 — per-bypass yield", "",
         "`sole` counts records for which that route was the ONLY reason they were screened — what "
         "would have been lost without it.", "",
         "| Route | Screened | RELEVANT | Sole reason | Sole and RELEVANT |", "|---|---|---|---|---|"]
    for k, (n, r_, sn, sr) in sorted(by.items(), key=lambda kv: -kv[1][1]):
        L.append(f"| `{k}` | {n} | {r_} ({pc(r_, n)}) | {sn} | **{sr}** |")
    L += ["", "## Measurement 4 — the no-abstract penalty", "",
          "The rubric told the screener to bucket a title-only record `info: insufficient` rather "
          "than NOT_RELEVANT. If the instruction did not bind, title-only records would return "
          "NOT_RELEVANT at the same rate as abstracted ones and the screen would be converting "
          "missing metadata into negative evidence.", "",
          "| | With abstract | Title only |", "|---|---|---|",
          f"| n | {sum(absd[True].values())} | {sum(absd[False].values())} |",
          f"| RELEVANT | {absd[True]['RELEVANT']} ({pc(absd[True]['RELEVANT'], sum(absd[True].values()))}) | "
          f"{absd[False]['RELEVANT']} ({pc(absd[False]['RELEVANT'], sum(absd[False].values()))}) |",
          f"| UNCERTAIN | {absd[True]['UNCERTAIN']} ({pc(absd[True]['UNCERTAIN'], sum(absd[True].values()))}) | "
          f"{absd[False]['UNCERTAIN']} ({pc(absd[False]['UNCERTAIN'], sum(absd[False].values()))}) |",
          f"| NOT_RELEVANT | {absd[True]['NOT_RELEVANT']} ({pc(absd[True]['NOT_RELEVANT'], sum(absd[True].values()))}) | "
          f"{absd[False]['NOT_RELEVANT']} ({pc(absd[False]['NOT_RELEVANT'], sum(absd[False].values()))}) |",
          f"| `info: insufficient` | {infod[True]['insufficient']} "
          f"({pc(infod[True]['insufficient'], sum(infod[True].values()))}) | "
          f"{infod[False]['insufficient']} ({pc(infod[False]['insufficient'], sum(infod[False].values()))}) |",
          "",
          "## Measurement 5 — screener against term match", "",
          "The screener never saw D1's hit lists, so these are independent readings.", "",
          f"- **{len(dis_ident)} RELEVANT records read as `identified` carry no identification "
          f"term.** Each is a vocabulary hole rather than a screener error if the design is stated "
          "in words the term list does not hold.",
          f"- **{len(dis_debt)} read as `own_student_debt` carry no student-debt term** — these are "
          "records the production frame could not have reached on its exposure axis.",
          f"- **{len(dis_fert)} read as carrying a fertility outcome carry no fertility term.**", ""]
    if dis_debt:
        L += ["Records the frame's own exposure vocabulary would miss:", ""]
        for r in dis_debt[:12]:
            L.append(f"- *{r['title'][:80]}*")
        L.append("")
    L += ["## Walls, as fired by the screen", "", "| Wall | Records |", "|---|---|"]
    for k, n in walls.most_common():
        L.append(f"| `{k}` | {n} |")
    L += ["", "## Findings", "",
          "*Written after reading the measurements above, then re-run so the summary regenerates.*",
          "",
          f"- **The chapter's shape is now counted, not inferred.** {len(direct)} direct-arm records "
          f"against {len(chain)} chain-arm, and {len(direct_id)} identified against {len(chain_id)}. "
          "Every stage from the scope onward predicted that C.3.g's registered estimand would be "
          "the minority of its own evidence base and that identification would sit in the "
          "neighbouring arm. It does, on records that were read rather than on vocabulary.",
          "- **A4's routing prediction was accurate to a point.** `arm: cannot_tell` is 1 of 80 — "
          "the split really is screenable — but `outcome: multiple` is 22%, against A4's predicted "
          "23% un-routable share. The two numbers measure the same obstacle from different sides: "
          "the screener can nearly always tell what a record does, and nearly a quarter of records "
          "do more than one thing, so routing still has to finish at full text.",
          "- **The no-abstract instruction bound, and the headline number looks like it did not.** "
          "Title-only and abstracted records return NOT_RELEVANT at an identical 81%, which is "
          "exactly the signature of the failure the rubric was written to prevent. It is not that "
          "failure: title-only records returned RELEVANT at a HIGHER rate (15% vs 12%), and "
          "`info: insufficient` fired on 80% of them against 2%. The parity comes from genuinely "
          "off-topic title-only records — conference programmes, datasets, editorials — not from "
          "invisible ones being written off. Reported in full because the summary statistic alone "
          "would have been read the other way.",
          "- **Two bypasses paid and four did not, and the four should not simply be retired.** "
          "`bypass_keyword_frame` was the sole reason for 141 records and delivered 6 RELEVANT that "
          "nothing else would have reached; the score cut delivered 1. `bypass_both_channels` (67% "
          "RELEVANT), `bypass_anchor` (76%) and `bypass_identified_fertility` (88%) have the "
          "highest precision in the run and a sole-yield of ZERO — they are redundant here, not "
          "useless, because everything they hold was independently reached. `bypass_title_only_"
          "exposure` screened 89 records as their only route and returned no unique RELEVANT, which "
          "is the honest number to carry to the next chapter.",
          f"- **{len(dis_debt)} RELEVANT records carry no student-debt term at all** — Nau et al., "
          "*Returning to the nest*, *Debt, Jobs, or Housing*, *Echoes of rising tuition* and *Does "
          "Debt Discourage Marriage*. A4 found this for two anchors; the screen finds it for five "
          "records, including the most-cited work in the primary cell. The production frame's "
          "student-anchored exposure axis, adopted to defeat the sovereign-debt homonym, cannot "
          "reach any of them. They arrived through the citation channel and by hand, which is the "
          "argument for keeping both.",
          "",
          "## What goes forward", "",
          f"**{len(pool)} records** (RELEVANT + UNCERTAIN) go to full-text retrieval. The "
          f"{V['NOT_RELEVANT']} NOT_RELEVANT records keep their verdicts and stay in "
          f"`{os.path.basename(OUT)}`; nothing is deleted at any stage of this pipeline.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"screened {len(work)}  RELEVANT {V['RELEVANT']}  UNCERTAIN {V['UNCERTAIN']}  "
          f"NOT_RELEVANT {V['NOT_RELEVANT']}")
    print(f"  direct arm {len(direct)} ({len(direct_id)} identified) | chain arm {len(chain)} "
          f"({len(chain_id)} identified)")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
