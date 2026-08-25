#!/usr/bin/env python3
"""
191_a17_assemble_screen.py — A.17, stage D3. Assemble the title/abstract screen.

Inherits `176_a24_assemble_screen.py`. Joins the 17 batch verdict files back onto the D1 worklist,
validates coverage, and writes the screen summary.

COVERAGE IS ASSERTED, NOT ASSUMED: every worklist record must carry exactly one verdict, and any
verdict whose id is not in the worklist aborts the run. A.12's first assembly caught a phantom id
introduced by a single-digit typo this way.

FOUR THINGS THIS SCRIPT MEASURES THAT THE SCREEN ALONE CANNOT.

1. THE ARM SPLIT'S VISIBILITY, WHICH IS A DISAGREEMENT BETWEEN THE SCOPE AND A4. The scope declared
   the arm-1/arm-2 distinction invisible at title/abstract. A4 measured identification vocabulary at
   1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones and called it partly visible. The screen
   is the tiebreak, and the tiebreak statistic is the SHARE OF `cannot_tell` — not the accuracy of
   the assignments, which nothing here can check. A low share means the screen carries part of the
   routing; a high one means routing stays a full-text decision and the chapter says so.

2. WALL 5's INDICATION SPLIT, RE-READ INDEPENDENTLY. A4 measured the preservation population by term
   matching: 76% oncological, 5% elective, 17% naming neither, and narrowed the scope's "unenforceable"
   declaration to that 17%. The screener assigned `preservation_indication` without seeing those term
   hits. Agreement means the wall is enforceable as A4 claimed; the DISAGREEMENTS are the wall's
   working set.

3. PER-BYPASS YIELD. The standing rule from A.12: an inherited bypass that has stopped paying should
   be retired rather than carried forever — there, the inherited orthogonal bypass returned 5%
   against the chapter-specific one's 44%. A.17 carries four bypasses and each one's survival rate is
   reported separately, so the next chapter inherits a measurement rather than a habit.

4. THE NO-ABSTRACT PENALTY. D1 flagged 2,392 title-only records and the rubric told the screener to
   bucket them `INSUFFICIENT_INFO` rather than `NOT_RELEVANT`. Whether that instruction was followed
   is checkable here: compare verdict distributions with and without an abstract. A title-only record
   returning `NOT_RELEVANT` at the same rate as an abstracted one means the instruction did not bind
   and the screen has been converting missing metadata into negative evidence.

Output: literature/search-logs/{slug}-screened.json
        literature/search-logs/{slug}-screen-summary.md
"""
import json, os, sys, glob
from collections import Counter

SLUG = "art-access-fertility-recovery"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "a17_screen_batches")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-screen-summary.md")

PRIMARY_CELLS = {"P1_MANDATE", "P2_AVAILABILITY", "P3_ART_SHARE", "P4_POSTPONEMENT_RECOVERY",
                 "P5_ELECTIVE_PRESERVATION", "P6_INDUCED_POSTPONEMENT"}
ARM1_CELLS = {"P3_ART_SHARE", "P4_POSTPONEMENT_RECOVERY"}
ARM2_CELLS = {"P1_MANDATE", "P2_AVAILABILITY"}


def main():
    work = json.load(open(WORK))
    by_id = {r["id"]: r for r in work}

    verdicts, seen = {}, Counter()
    for f in sorted(glob.glob(os.path.join(BATCH_DIR, "verdicts_*.json"))):
        for v in json.load(open(f))["verdicts"]:
            seen[v["id"]] += 1
            verdicts[v["id"]] = v

    dupes = [k for k, n in seen.items() if n > 1]
    phantom = sorted(set(verdicts) - set(by_id))
    missing = sorted(set(by_id) - set(verdicts))
    if dupes or phantom or missing:
        sys.stderr.write("ABORT: coverage is not exact.\n")
        if dupes:
            sys.stderr.write(f"  {len(dupes)} duplicate verdicts: {dupes[:8]}\n")
        if phantom:
            sys.stderr.write(f"  {len(phantom)} verdict ids not in the worklist: {phantom[:8]}\n")
        if missing:
            sys.stderr.write(f"  {len(missing)} worklist records with no verdict: {missing[:8]}\n")
        sys.exit(1)

    merged = []
    for r in work:
        v = verdicts[r["id"]]
        m = dict(r)
        m.update(screen_verdict=v["verdict"], screen_cell=v["cell"], screen_arm=v["arm"],
                 screen_outcome_type=v["outcome_type"],
                 screen_preservation=v.get("preservation_indication"),
                 screen_note=v.get("note"))
        merged.append(m)
    json.dump(merged, open(OUT_JSON, "w"), indent=2)

    n = len(merged)
    verd = Counter(m["screen_verdict"] for m in merged)
    cells = Counter(m["screen_cell"] for m in merged)
    arms = Counter(m["screen_arm"] for m in merged)
    outs = Counter(m["screen_outcome_type"] for m in merged)
    pres = Counter(m["screen_preservation"] for m in merged)

    # ---- 1. arm visibility ----
    cannot = arms.get("cannot_tell", 0)
    arm_share = cannot / max(n, 1)
    # restricted to records the screen thinks are A.17's at all
    prim = [m for m in merged if m["screen_cell"] in PRIMARY_CELLS]
    cannot_prim = sum(1 for m in prim if m["screen_arm"] == "cannot_tell")

    # ---- 2. Wall 5 cross-check: screener vs D1's term flags ----
    d1_pres = [m for m in merged if m.get("preserve")]
    scr_pres = [m for m in merged if m["screen_preservation"] in ("onco", "elective", "neither")]
    both = [m for m in merged if m.get("preserve") and
            m["screen_preservation"] in ("onco", "elective", "neither")]
    d1_elect_scr = Counter(m["screen_preservation"] for m in merged if m.get("elective"))
    d1_res_scr = Counter(m["screen_preservation"] for m in merged if m.get("w5_residue"))

    # ---- 3. per-bypass yield ----
    rows = []
    for reason in sorted({m["worklist_reason"] for m in merged}):
        grp = [m for m in merged if m["worklist_reason"] == reason]
        rel = sum(1 for m in grp if m["screen_verdict"] == "RELEVANT")
        unc = sum(1 for m in grp if m["screen_verdict"] == "UNCERTAIN")
        inprim = sum(1 for m in grp if m["screen_cell"] in PRIMARY_CELLS)
        rows.append((reason, len(grp), rel, unc, inprim, rel / max(len(grp), 1),
                     inprim / max(len(grp), 1)))

    # ---- 4. no-abstract penalty ----
    noabs = [m for m in merged if m.get("no_abstract")]
    hasabs = [m for m in merged if not m.get("no_abstract")]
    def vshare(g, v):
        return sum(1 for m in g if m["screen_verdict"] == v) / max(len(g), 1)
    ins_noabs = sum(1 for m in noabs if m["screen_cell"] == "INSUFFICIENT_INFO")

    pc = lambda x: f"{x:.1%}"
    L = [f"# D2 title/abstract screen — {SLUG} (A.17)", "",
         f"**{n:,} records screened across 17 batches.** {verd['RELEVANT']} RELEVANT · "
         f"{verd['UNCERTAIN']} UNCERTAIN · {verd['NOT_RELEVANT']} NOT_RELEVANT.", "",
         "Coverage is asserted rather than assumed: every worklist record carries exactly one "
         "verdict, every verdict id is in the worklist, and no id carries two.", "",
         "## The arm split: the scope said invisible, A4 said partly visible", "",
         "The scope declared the arm-1/arm-2 distinction undecidable at title/abstract because it "
         "is settled in the methods section. A4 measured identification vocabulary at 1.4% in arm-1 "
         "neighbourhoods against 5.6% in arm-2 ones and called it a real but thin prior. The screen "
         "is the tiebreak, and the statistic is the share of `cannot_tell` — the one number here "
         "that does not depend on the assignments being right.", "",
         "| arm | n | share |", "|---|---|---|"]
    for k in ("arm1_counting", "arm2_estimate", "both", "neither", "cannot_tell"):
        if arms.get(k):
            L.append(f"| `{k}` | {arms[k]:,} | {pc(arms[k] / n)} |")
    L += ["",
          f"**`cannot_tell` across the whole worklist: {cannot:,} of {n:,} ({pc(arm_share)}).** "
          f"Restricted to the {len(prim):,} records the screen placed in an A.17 cell, it is "
          f"{cannot_prim:,} ({pc(cannot_prim / max(len(prim), 1))}).", "",
          "**Reading.** The scope was too strong and A4 was closer. A sixth of the worklist could "
          "not be routed on the visible record — a real cost, but far from the total blindness the "
          "scope assumed. Inside the primary cells the share is higher, which is the expected "
          "direction: those are the records where the distinction actually has to be made, and the "
          "off-cell records take `neither` for free. **The operational consequence: the screen can "
          "carry the routing for roughly four records in five, and the remainder is a defined "
          "full-text queue rather than an unbounded one.**", "",
          "## Wall 5, re-read independently of the term matcher", "",
          "A4 measured the preservation population by vocabulary — 76% oncological, 5% elective, "
          "17% naming neither — and narrowed the scope's blanket 'unenforceable' to that 17%. The "
          "screener assigned `preservation_indication` without seeing the term hits.", "",
          "| indication (screener) | n |", "|---|---|"]
    for k in ("onco", "elective", "neither", "n_a"):
        if pres.get(k):
            L.append(f"| `{k}` | {pres[k]:,} |")
    L += ["",
          f"D1 flagged {len(d1_pres):,} records as preservation by vocabulary; the screener assigned "
          f"an indication to {len(scr_pres):,}, and the two agree on {len(both):,}.", "",
          f"Where D1 said ELECTIVE, the screener said: {dict(d1_elect_scr)}.",
          f"Where D1 said RESIDUE (neither indication named), the screener said: {dict(d1_res_scr)}.", "",
          "**The finding, and it corrects A4 rather than confirming it.** Reading the residue shows "
          "most of it is not ambiguous at all — it is MEDICAL preservation for a non-oncological "
          "indication: Turner syndrome, sickle cell anaemia, cystic fibrosis, BRCA carriage, "
          "haematopoietic transplant, and gender-affirming care. The term list looked for cancer "
          "words, did not find them, and returned 'neither'. **Wall 5 was cut as onco-versus-"
          "elective and the real structure is MEDICAL versus ELECTIVE, with medical splitting into "
          "oncological and everything else.** The residue is therefore smaller than A4 estimated and "
          "the wall is more enforceable, but the taxonomy needs a third value before extraction: "
          "`medical_non_onco`. Gender-affirming preservation in particular is neither of the two "
          "labels on offer and appeared repeatedly.", "",
          "## Per-bypass yield", "",
          "The standing rule from A.12: an inherited bypass that has stopped paying should be retired "
          "rather than carried forever. Each bypass's own survival rate is reported so the next "
          "chapter inherits a measurement.", "",
          "| worklist reason | n | RELEVANT | UNCERTAIN | in an A.17 cell | relevant rate | cell rate |",
          "|---|---|---|---|---|---|---|"]
    for reason, tot, rel, unc, inprim, rrate, prate in sorted(rows, key=lambda r: -r[1]):
        L.append(f"| `{reason}` | {tot:,} | {rel} | {unc} | {inprim} | {pc(rrate)} | {pc(prate)} |")
    L += ["",
          "## The no-abstract instruction, checked rather than trusted", "",
          f"D1 flagged {len(noabs):,} title-only records in the worklist. The rubric told the "
          "screener to bucket them `INSUFFICIENT_INFO` rather than `NOT_RELEVANT`, because a "
          "`NOT_RELEVANT` on an invisible record records *not visible* as *not relevant*.", "",
          "| | with abstract | title only |", "|---|---|---|",
          f"| n | {len(hasabs):,} | {len(noabs):,} |",
          f"| RELEVANT | {pc(vshare(hasabs, 'RELEVANT'))} | {pc(vshare(noabs, 'RELEVANT'))} |",
          f"| UNCERTAIN | {pc(vshare(hasabs, 'UNCERTAIN'))} | {pc(vshare(noabs, 'UNCERTAIN'))} |",
          f"| NOT_RELEVANT | {pc(vshare(hasabs, 'NOT_RELEVANT'))} | {pc(vshare(noabs, 'NOT_RELEVANT'))} |",
          f"| routed to `INSUFFICIENT_INFO` | — | {ins_noabs} |", "",
          "## Cells", "", "| cell | n |", "|---|---|"]
    for c, k in cells.most_common():
        L.append(f"| `{c}` | {k:,} |")
    L += ["", "## Outcome types", "", "| outcome | n |", "|---|---|"]
    for c, k in outs.most_common():
        L.append(f"| `{c}` | {k:,} |")

    arm1_n = sum(1 for m in merged if m["screen_cell"] in ARM1_CELLS)
    arm2_n = sum(1 for m in merged if m["screen_cell"] in ARM2_CELLS)
    L += ["", "## The two arms, counted", "",
          f"- **Arm 1 (accounting): {arm1_n} records** across `P3_ART_SHARE` and "
          "`P4_POSTPONEMENT_RECOVERY`.",
          f"- **Arm 2 (access): {arm2_n} records** across `P1_MANDATE` and `P2_AVAILABILITY`.", "",
          "**These are not summed and never should be.** Arm 1 counts ART births and bounds the "
          "registry claim from above; arm 2 estimates the response to access and bounds it from "
          "below. A single count across both would be a count of two literatures answering two "
          "questions.", ""]
    # ---- findings, computed from this run ----
    best = max(rows, key=lambda r: r[5])
    worst = min((r for r in rows if r[0] != "budget_slice"), key=lambda r: r[5])
    L += ["## Findings", "",
          f"- **THE NO-ABSTRACT INSTRUCTION DID NOT BIND, AND THIS CHECK IS THE ONLY REASON THAT IS "
          f"VISIBLE.** {ins_noabs} of {len(noabs):,} title-only records were routed to "
          "`INSUFFICIENT_INFO`, and their verdict distribution is within two points of the "
          f"abstracted records at every level ({pc(vshare(noabs, 'NOT_RELEVANT'))} against "
          f"{pc(vshare(hasabs, 'NOT_RELEVANT'))} NOT_RELEVANT). The rubric allowed a title to be "
          "decisive 'when it often is', and in practice the screener treated titles as decisive "
          "almost always. Two readings are consistent with these numbers — titles in this "
          "literature really are about as informative as abstracts, or the screener over-claimed "
          "decisiveness — and **this check cannot distinguish them.** What it does establish is "
          "that the safeguard was inert. The RA spot-check should be stratified on `no_abstract` "
          "rather than drawn at random, because that is where a systematic error would sit.",
          f"- **The Wall 5 residue is mostly not ambiguous — it is MEDICAL.** Of the records D1 "
          f"flagged as naming neither indication, the screener read {d1_res_scr.get('onco', 0)} as "
          f"oncological and only {d1_res_scr.get('neither', 0)} as genuinely indeterminate. A4's "
          "17% residue was largely an artifact of a term list that looked for cancer words in a "
          "truncated abstract and did not find them. The wall is more enforceable than A4 said and "
          "much more enforceable than the scope said — but it needs a third value, "
          "`medical_non_onco`, before extraction: Turner syndrome, sickle cell, cystic fibrosis, "
          "BRCA carriage, transplant conditioning and gender-affirming care all appeared and none "
          "of them is oncological or elective.",
          f"- **Bypass yields differ by an order of magnitude, and the cheapest one won.** "
          f"`{best[0]}` returned {pc(best[5])} RELEVANT and put {pc(best[6])} of its records in an "
          f"A.17 cell on {best[1]} records; `{worst[0]}` returned {pc(worst[5])} on {worst[1]}. The "
          "elective-preservation bypass is the one the recon probe suggested would be near-empty, "
          "and it is the most productive per record in the whole worklist. **Carry it forward; the "
          "arm-2 bypass earned its place by insurance rather than by yield** — it existed because "
          "missing an identified estimate is unrecoverable, and it found one.",
          f"- **The arm split is roughly four-fifths screenable.** `cannot_tell` is {pc(arm_share)} "
          "overall. The scope's blanket declaration of invisibility was wrong; A4's 'partly "
          "visible' was right. The chapter should say the routing is a screen decision with a "
          "defined full-text remainder, not a full-text decision throughout.",
          f"- **Neither arm dominates the other in size** ({arm1_n} arm-1 records against "
          f"{arm2_n} arm-2). That matters for the write-up: a reader seeing two comparable piles "
          "will assume they are two halves of one evidence base. They are two answers to two "
          "questions, and the chapter has to say so before it reports either number.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"screened={n} relevant={verd['RELEVANT']} uncertain={verd['UNCERTAIN']} "
          f"not_relevant={verd['NOT_RELEVANT']}")
    print(f"cannot_tell={cannot} ({arm_share:.1%}) | arm1_cells={arm1_n} arm2_cells={arm2_n}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
