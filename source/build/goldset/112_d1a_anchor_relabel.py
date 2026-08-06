#!/usr/bin/env python3
r"""
112_d1a_anchor_relabel.py — D.1.a. Correct Tier-A anchor labels that the calibration exposed.

WHY. The first clean calibration scored 7/10 on the decoys, and adjudicating each disagreement
showed the screen was right more often than the anchor set was. Two labels are demonstrably wrong
and a third needs the cell the new moderator rule created. **The calibration was measuring the
anchor set as much as the screen.**

THE TRAP THIS SCRIPT IS BUILT TO AVOID. Correcting only the labels the screen disputed would fit the
gold to the screen: every subsequent calibration would score better by construction and would be
measuring nothing. So all 48 anchors were re-read against the scope, not just the disputed ones, and
the corrections below are keyed to text quoted from the record rather than to any verdict. One
correction (`maternity benefits` -> VALUE_AS_MODERATOR) makes the screen's verdict MORE wrong, not
less, which is the check that this was not a ratification exercise.

THE FLIP RULE, APPLIED CONSERVATIVELY. A label is changed only where the abstract explicitly states
the dependent variable and it is not fertility, or explicitly states the treatment and it is not a
measured value. Everything else -- including several the screen also disputed -- is recorded as
CONTESTED and left untouched for a human rater. Title-only records are never flipped: 34 of the 48
labels were assigned before abstracts were joined, which is how these errors got in, and guessing
harder from the same title is not a repair.

CONTESTED IS NOT A DIPLOMATIC NULL. It is the RA-escalation class: these need a second human rater
per the playbook, and they stay in the gold at their current label until one rules, so the
calibration's denominator is unchanged and no number moves quietly.

Usage:  python3 112_d1a_anchor_relabel.py
Output: literature/search-logs/{slug}-tier-a-relabelled.json   (109_ prefers this when present)
        literature/search-logs/{slug}-anchor-relabel.md
"""
import json, sys
from pathlib import Path

SLUG = "postmaterialism-individualism-secularization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SRC = LOGS / f"{SLUG}-tier-a.json"
OUT = LOGS / f"{SLUG}-tier-a-relabelled.json"
OUT_MD = LOGS / f"{SLUG}-anchor-relabel.md"

# Keyed on a distinctive title fragment, because 6 rows carry `paperId: null`.
CORRECTIONS = [
    {
        "match": "Does individualism promote gender equality",
        "from": {"role": "DECOY", "pair": "S2", "provisional_cell": "OFF_OUTCOME"},
        "to": {"role": "EMPIRICAL", "pair": "S2", "provisional_cell": "PRIMARY_INDIVIDUALISM_S2"},
        "evidence": ("Abstract: \"Individualism is also associated with greater levels of female "
                     "employment and educational attainment, and lower levels of fertility.\" The "
                     "treatment is a measured WVS individualism scale and fertility is a reported "
                     "outcome, so both routing questions are yes."),
        "why_it_was_wrong": ("The DECOY/OFF_OUTCOME label was assigned from the title alone, where "
                             "the only visible outcome is gender equality. The abstract was joined "
                             "to this record only in this run."),
    },
    {
        "match": "Demographic Imperatives and Religious Markets",
        "from": {"role": "EMPIRICAL", "pair": "S3", "provisional_cell": "PRIMARY_SECULAR_S3"},
        "to": {"role": "REVERSE", "pair": "S3", "provisional_cell": "VALUE_CONSTRUCT"},
        "evidence": ("Abstract: the models seek to explain \"the growth and decline of religious "
                     "groups\", with \"switching and fertility\" as the mechanisms of growth. The "
                     "dependent variable is religious-group size and fertility is a regressor -- "
                     "the D.1.a pair inverted."),
        "why_it_was_wrong": ("Labelled a primary S3 estimate on a title that reads as religion-and-"
                             "fertility. It is the reverse arrow and belongs with the "
                             "risk-of-bias material."),
    },
    {
        "match": "How religion mediates the fertility response to maternity benefits",
        "from": {"role": "DECOY", "pair": "DECOY", "provisional_cell": "OFF_OTHER"},
        "to": {"role": "DECOY", "pair": "DECOY", "provisional_cell": "VALUE_AS_MODERATOR"},
        "evidence": ("Abstract: a difference-in-differences on \"a 1982 maternity benefits "
                     "expansion\" comparing \"women who did and did not grow up in religious "
                     "households\". The design moves the benefit; religiosity splits the sample."),
        "why_it_was_wrong": ("Not wrong so much as homeless: OFF_OTHER was the only available "
                             "route-away cell. The rubric's new moderator rule gives it the cell "
                             "that names what it actually is. **This correction makes the "
                             "calibration HARDER, not easier** -- the screen assigned it "
                             "PRIMARY_SECULAR_S3, and it is now scored against a specific cell "
                             "rather than a catch-all."),
    },
]

# Re-read and disputed, but NOT changed: the abstract does not settle it, or there is no abstract.
# These keep their current label and go to a second human rater.
CONTESTED = [
    ("Postmaterialism and voluntary childlessness",
     "Labelled DECOY / NORM_ACCEPTABILITY_DESCRIPTIVE (degenerate under Ruling 2). The abstract says "
     "it asks \"how citizen values relate to decisions to not have children\" using WVS Wave 7 -- "
     "which reads as an S1 value measure against a childlessness outcome, i.e. NOT degenerate. "
     "**Ruling 2 turns on the scale's item content, which the abstract does not give.** This is "
     "exactly the case the rubric binds to UNCERTAIN + needs_full_text; the label cannot be settled "
     "here either."),
    ("The relationship between social status and biological success",
     "Labelled EMPIRICAL / PRIMARY_SECULAR_S3. The title names a social-status gradient as the "
     "regressor, which is D.1.c's treatment, but the setting is a religious hierarchy where rank "
     "may itself proxy religiosity. No abstract. Not flipped on a title."),
    ("Religious Affiliation, Participation and Fertility: A Cautionary Note",
     "Labelled EMPIRICAL / PRIMARY_SECULAR_S3. The abstract is about participation measures being "
     "\"empirically problematic with the typical cross-sectional data set\" -- a methodological note "
     "on reverse ordering. Whether it also reports a usable estimate is not visible."),
    ("Cultural Dynamics and Economic Theories of Fertility Change",
     "Labelled EMPIRICAL / PRIMARY_POSTMATERIAL_S1. The abstract describes theories being "
     "\"correlated\" and \"considered\" and names no data or design, which reads as THEORY, but it "
     "is a 1980s abstract style and absence of a described design is not absence of one."),
    ("Differences in Fertility Patterns between East and West German Women",
     "Labelled EMPIRICAL / PRIMARY_VALUE_EX_ANTE. The abstract disentangles \"cultural background "
     "and institutional context\" using East/West origin -- a place, not a measured value. Wall 7 "
     "(measured versus narrated) may route this out, but the paper may also carry a measured value "
     "covariate the abstract omits."),
]


def main():
    rows = json.loads(SRC.read_text())
    applied, unmatched = [], []
    for c in CORRECTIONS:
        hits = [r for r in rows if c["match"].lower() in (r.get("title") or "").lower()]
        if len(hits) != 1:
            unmatched.append((c["match"], len(hits)))
            continue
        r = hits[0]
        before = {k: r.get(k) for k in c["to"]}
        # Refuse to apply a correction whose stated 'from' does not match what is on disk: the file
        # may have moved under us, and applying a diff to an unexpected base is how a repair
        # silently becomes a corruption.
        mismatch = {k: (r.get(k), v) for k, v in c["from"].items() if r.get(k) != v}
        if mismatch:
            unmatched.append((c["match"], f"stale base {mismatch}"))
            continue
        r.update(c["to"])
        r["_relabelled_from"] = before
        r["_relabel_evidence"] = c["evidence"]
        applied.append((c, before))
    if unmatched:
        raise SystemExit(f"corrections did not apply cleanly: {unmatched}")

    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    L = ["# D.1.a — Tier-A anchor relabelling", "",
         "The first clean calibration scored 7/10 on the decoys. Adjudicating each disagreement "
         "showed **the screen was right more often than the anchor set was** — the calibration was "
         "measuring the anchor set as much as the screen.", "",
         "## The trap this avoids", "",
         "Correcting only the labels the screen disputed would **fit the gold to the screen**: every "
         "later calibration would score better by construction and would be measuring nothing. All "
         "48 anchors were re-read against the scope, and the corrections below are keyed to text "
         "quoted from the record rather than to any verdict. **One correction makes the screen's "
         "verdict more wrong, not less**, which is the check that this was not a ratification.", "",
         "## The flip rule", "",
         "A label changes only where the abstract **explicitly states** the dependent variable and it "
         "is not fertility, or explicitly states the treatment and it is not a measured value. "
         "**Title-only records are never flipped** — 34 of the 48 labels were assigned before "
         "abstracts were joined, which is how these errors got in, and guessing harder from the same "
         "title is not a repair.", "",
         f"- corrections applied: **{len(applied)}**",
         f"- re-read, disputed, and deliberately left alone: **{len(CONTESTED)}**", "",
         "## Corrections", ""]
    for c, before in applied:
        L += [f"### {c['match']}", "",
              f"- **{before} → {c['to']}**",
              f"- evidence: {c['evidence']}",
              f"- why the old label was wrong: {c['why_it_was_wrong']}", ""]
    L += ["## Contested — left at their current label, escalated to a second human rater", "",
          "**`CONTESTED` is not a diplomatic null.** These stay in the gold unchanged, so the "
          "calibration denominator does not move and no number changes quietly. They need a second "
          "rater per the RA playbook.", ""]
    for t, why in CONTESTED:
        L += [f"- **{t}** — {why}", ""]
    OUT_MD.write_text("\n".join(L) + "\n")
    print(f"applied {len(applied)} corrections, {len(CONTESTED)} contested and unchanged",
          file=sys.stderr)
    print(f"wrote {OUT.name} and {OUT_MD.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
