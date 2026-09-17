#!/usr/bin/env python3
"""
413 — A.6 (TICK-087) stage 6: apply the full-text screen decisions and close the primary cell as
far as the retrieved evidence allows.

`412` retrieved 2 of the 8 `INSUFFICIENT_INFO` records, including the one that mattered. This script
records what reading them decided, marks the other six as blocked on library retrieval rather than
resolved, and regenerates the tally. `DECISIONS` below is authored judgment; the script attaches it,
refuses to double-apply, and generates the counts.

The decider, read
-----------------
`W108787496` — *Essays on Fertility and Fertility Preferences in India* (Rajan, Duke, 2014), 40,538
words, retrieved through the DSpace REST API. Three empirical chapters:

  ch2  outcome realized fertility; exposure is an accounting DECOMPOSITION of the preference-behaviour
       gap into unwanted births, gender preference and postponement. A framework, not a norm effect.
  ch3  dependent variable **Desired Family Size**; exposure is education, via two-way fixed effects.
       `outcome_level: DESIRED`, and the exposure is not normative.
  ch4  **"Community Norms and the Use of Contraception to Space or Stop"** — dependent variable
       §4.4.1 **Contraceptive Use**, estimated as the odds of spacing and the odds of stopping via
       multilevel logit with community-level independent variables. The author's own summary: "using
       multilevel models, I find that community norms play a strong role".

Chapter 4 is A.6's exposure almost exactly — community norms, community-borne, with method
availability not the varying quantity. Its outcome is contraceptive use. So under ruling 2 the
decider is `LINK_NORM_USE`, not `PRIMARY_NORM_FERTILITY`. It is the best-designed record this
chapter has found and it does not estimate the chapter's parameter.

That is the whole result. The record with the strongest prior in the entire 2,815-record pool —
only member of S1_DECISIVE, cited by 5 of 15 anchors — turns out to fail on the outcome, which is
the same way every other near-miss in this chapter failed. Five channels predicted the empty
primary cell; reading the one record that could have overturned it did not.

What is closed and what is not
------------------------------
Closed: the primary cell is empty across every stratum that could contain it, with the single
highest-prior record now read at full text rather than inferred from an abstract. Not closed: six
records remain unretrievable by open access (all `oa_status: closed`, no PDF anywhere in OpenAlex or
Unpaywall), and the sampled tail S5/S6/S7 is unread. Neither gap is likely to overturn the result,
and both are named in the wantlist rather than glossed.
"""
import csv, pathlib, sys
from collections import Counter

SLUG = "stigma-reduction-contraception-abortion"
CSVP = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
LOGP = pathlib.Path("literature/search-logs") / f"{SLUG}-screen-log.md"
RETRIEVED = pathlib.Path("extraction") / f"{SLUG}-pdf-retrieval-log.csv"

DECISIONS = {
    "W108787496": {
        "cell": "LINK_NORM_USE", "outcome_level": "USE", "dose_unit": "NONE",
        "phenomenon_window": "FDT", "estimator_class": "OLS_ADJUSTED",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "yes",
        "note": ("FULL TEXT READ (40,538 words, DSpace REST). Rajan, Duke 2014. Ch4 'Community "
                 "Norms and the Use of Contraception to Space or Stop' is A.6's exposure almost "
                 "exactly - community norms, community-borne, method availability not the varying "
                 "quantity - estimated by multilevel logit with community-level predictors. But "
                 "its dependent variable (sec 4.4.1) is CONTRACEPTIVE USE, reported as odds of "
                 "spacing and odds of stopping. Ch3's dependent variable is Desired Family Size "
                 "(education exposure, two-way FE). Ch2 has a fertility outcome but its exposure "
                 "is an accounting decomposition, not a norm. So ruling 2 makes this LINK_NORM_USE: "
                 "the best-designed record in the chapter, and not the chapter's parameter. "
                 "Second read flagged because reclassifying the highest-prior record in the pool "
                 "should not rest on one reader.")},
    "W2885614896": {
        "cell": "MIXED_NORM_SUPPLY", "outcome_level": "USE", "dose_unit": "NONE",
        "phenomenon_window": "SDT", "estimator_class": "OTHER_LOUD",
        "stigma_object": "ABORTION", "stigma_bearer": "PROVIDER",
        "second_read_required": "no",
        "note": ("FULL TEXT READ (19,613 words). Aladago 2016, KIT/VU Amsterdam MPH thesis, "
                 "literature-based. Outcome is access to and utilisation of safe abortion "
                 "services; stigma appears as one barrier bundled with distance, cost, provider "
                 "attitudes and legal awareness, with no separate dose on the norm component. "
                 "Rule 5 fires before rule 6: MIXED_NORM_SUPPLY, routed to A.5. estimator_class "
                 "OTHER_LOUD - an MPH review thesis is not one of the listed designs.")},
}
BLOCKED_NOTE = (" LIBRARY RETRIEVAL REQUIRED: oa_status closed, no PDF in OpenAlex or Unpaywall "
                "as of 2026-09-17; see the wantlist.")


def main():
    rows = list(csv.DictReader(CSVP.open()))
    fields = list(rows[0].keys())
    retr = {r["id"]: r for r in csv.DictReader(RETRIEVED.open())} if RETRIEVED.exists() else {}

    applied = sum(1 for r in rows if r["id"] in DECISIONS and r["cell"] != "INSUFFICIENT_INFO")
    if applied == len(DECISIONS):
        print(f"decisions already applied to {applied} rows — regenerating the log only")
    else:
        for r in rows:
            if r["id"] in DECISIONS:
                r.update(DECISIONS[r["id"]])
            elif r["cell"] == "INSUFFICIENT_INFO" and BLOCKED_NOTE.strip() not in r["note"]:
                r["note"] = r["note"].rstrip() + BLOCKED_NOTE
        with CSVP.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"applied {len(DECISIONS)} full-text decisions; "
              f"annotated the remaining blocked records")

    rows = list(csv.DictReader(CSVP.open()))
    tally = Counter(r["cell"] for r in rows)
    primary = [r for r in rows if r["cell"] == "PRIMARY_NORM_FERTILITY"]
    blocked = [r for r in rows if r["cell"] == "INSUFFICIENT_INFO"]
    link = [r for r in rows if r["cell"] == "LINK_NORM_USE"]

    body = LOGP.read_text() if LOGP.exists() else ""
    marker = "\n## Full-text stage (`412`, `413`)\n"
    body = body.split(marker)[0].rstrip()
    sec = [marker.strip(), "",
           f"`412` retrieved **{sum(1 for r in retr.values() if r['status'] == 'retrieved')} of "
           f"{len(retr)}** of the unresolved records. Six remain `oa_status: closed` with no PDF in",
           "OpenAlex or Unpaywall; they are on the library wantlist, not resolved.", "",
           "### The decider, read", "",
           "`W108787496` — *Essays on Fertility and Fertility Preferences in India* (Rajan, Duke,",
           "2014), 40,538 words, retrieved through the DSpace REST API after the plain bitstream",
           "URL returned HTML.", "",
           "| chapter | exposure | dependent variable | verdict |",
           "|---|---|---|---|",
           "| ch2 | accounting decomposition of the preference-behaviour gap | realized fertility | a framework, not a norm effect |",
           "| ch3 | education, two-way fixed effects | **Desired Family Size** | `outcome_level: DESIRED`; exposure not normative |",
           "| ch4 | **community norms**, multilevel logit with community-level predictors | **Contraceptive Use** — odds of spacing, odds of stopping | A.6's exposure, but a use outcome |",
           "",
           "Chapter 4 is A.6's exposure almost exactly, and its outcome is use. Under ruling 2 the",
           "decider is **`LINK_NORM_USE`** — the best-designed record this chapter has found, and",
           "not an estimate of its parameter. The record with the strongest prior in the whole",
           "2,815-record pool fails the same way every other near-miss failed: on the outcome, not",
           "on the exposure.", "",
           f"### `PRIMARY_NORM_FERTILITY`: **{len(primary)}**", ""]
    if not primary:
        sec += ["Empty, and now closed as far as retrievable evidence allows. Every stratum that",
                "could contain a primary-cell study has been read exhaustively (164 records), and",
                "the single highest-prior record has been read at full text rather than inferred",
                "from an abstract. Six channels agree: the identified-design share (12/668), the",
                "realized-fertility share (58/668), anchor reachability (0/15 on the stage-2",
                "frame), the citation bridge test (8, none an estimate), the exhaustive screen (0",
                "of 164) and now the full text of the decider.", "",
                "Per scope §12 the verdict is **UNEVALUATED with the failed route named** — R1 for",
                "want of an identified fertility outcome, R3 for want of a pre-1985 dose series —",
                "and explicitly not 'weak evidence'.", "",
                f"`LINK_NORM_USE` stands at **{len(link)}** records and is poolable under scope",
                "§12 stratum 3. It must be reported under a heading that disclaims it as the",
                "chapter's parameter.", ""]
    sec += [f"### Still blocked: **{len(blocked)}**", "",
            "| id | why it is blocked |", "|---|---|"]
    for r in blocked:
        sec.append(f"| `{r['id']}` | {r['note'].split('LIBRARY RETRIEVAL')[0][:120].strip()} |")
    sec += ["", f"### Tally across {len(rows)} screened records", "", "| cell | n |", "|---|---|"]
    for c, n in tally.most_common():
        sec.append(f"| `{c}` | {n} |")
    LOGP.write_text(body + "\n\n" + "\n".join(sec) + "\n")

    print(f"PRIMARY_NORM_FERTILITY={len(primary)}  LINK_NORM_USE={len(link)}  "
          f"blocked={len(blocked)}")
    print(dict(tally))
    print(f"wrote {LOGP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
