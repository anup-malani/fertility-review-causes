#!/usr/bin/env python3
"""
419 — A.6 (TICK-087): correct the audit trail for W4224236986, which was reclassified on evidence
thinner than the note claimed.

Why this script exists at all. `418` moved this record from `MIXED_NORM_SECULAR` to
`LINK_NORM_USE` and wrote a note asserting a "weekly longitudinal panel with a mediation design"
in which "moral opposition to birth control" is measured "on a 0-4 scale". Those claims were made
from **ten keyword greps and roughly 2,500 characters of context windows** out of a 9,619-word
paper. The abstract, the measures section, the model specification and the tables were not read.
The conclusion happened to be right; the basis for it was not adequate, and a note that overstates
its basis is worse than a wrong cell, because a later reader has no way to tell which claims were
verified.

What the verified read establishes
----------------------------------
Design, confirmed from the Data and Methods section: the Relationship Dynamics and Social Life
study (RDSL), women aged 18-19 at baseline in Genesee County, Michigan, sampled from driver's
licence records; a 60-minute baseline interview followed by five-minute weekly journal surveys for
2.5 years, with attitudes and perceived norms refreshed every 12 weeks. Analytic sample **39,806
person-weeks across 680 women**, restricted to Christian denominations and to weeks when
unmarried and not pregnant. Mediation is the paper's own framing: religiosity's relationship to
these behaviours "operates largely through women's reproductive attitudes, anticipated feelings of
guilt after sex, and past sexual or contraceptive behaviors".

Measures, corrected. The 0-4 item is *"birth control is **morally wrong**"*, assessed every 12
weeks — a real repeatedly-measured variable in the Attitudes and Emotions block, not a descriptive
aside, so the reclassification stands. But it is an **internal moral belief**, which under wall 5
is nearer to D.1.a's "what people value" than to A.6's "what they can be seen doing". The measure
that is squarely A.6's construct is one `418` never saw: **"friends' approval of sex without birth
control"** on a 0-5 scale, alongside parents' and friends' approval of sex — the normative-
environment block. That is social cost borne by others' judgment, which is A.6's exposure proper.

So the record contains **both** sides of wall 5, separately measured: private moral belief (D.1.a)
and perceived social approval (A.6). That is a stronger basis for `LINK_NORM_USE` than `418` gave,
and it is also the cleanest empirical statement of the A.6/D.1.a distinction found anywhere in the
corpus — which is what PI call 5 needs.

One substantive wrinkle worth carrying into the chapter. The paper's "contraceptive work-around"
mechanism runs *against* A.6's predicted sign: because a nonmarital pregnancy would expose
stigmatised sexual activity, highly religious women who do have sex may use hormonal contraception
**more**, to conceal it. Stigma therefore pushes contraceptive use in both directions depending on
what is being hidden. A.6's registered claim assumes destigmatisation raises use; here stigma of a
*different object* (premarital sex) raises use too. Flag for §11.
"""
import csv, pathlib, sys

SLUG = "stigma-reduction-contraception-abortion"
CSVP = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
LOGP = pathlib.Path("literature/search-logs") / f"{SLUG}-screen-log.md"
WID = "W4224236986"

NOTE = ("VERIFIED FULL-TEXT READ (9,619 words, Europe PMC PMC9177776). Supersedes the note written "
        "by 418, which reached the right cell from keyword greps and ~2,500 characters of context "
        "and asserted more than it had read. McLoughlin Brooks and Weitzman, Demography 59(3) "
        "2022. DESIGN: RDSL, women 18-19 at baseline, Genesee County MI, weekly journal surveys "
        "over 2.5 years with attitudes refreshed every 12 weeks; analytic sample 39,806 "
        "person-weeks across 680 women, Christian denominations, unmarried and non-pregnant weeks. "
        "Mediation is the paper's own framing. MEASURES, corrected: the 0-4 item is 'birth control "
        "is MORALLY WRONG', an internal moral belief and therefore nearer D.1.a under wall 5. The "
        "measure that is squarely A.6's construct is one 418 never saw - 'friends' approval of sex "
        "WITHOUT birth control' on a 0-5 scale, with parents' and friends' approval of sex - the "
        "normative-environment block, i.e. social cost borne by others' judgment. The record "
        "therefore contains BOTH sides of wall 5, separately measured, which is a stronger basis "
        "for LINK_NORM_USE than 418 gave and the cleanest empirical statement of the A.6/D.1.a "
        "distinction in the corpus. Outcome remains weekly intercourse, hormonal contraceptive use "
        "and condom use, so ruling 2 keeps it link evidence. WRINKLE FOR SECTION 11: the paper's "
        "'contraceptive work-around' runs against A.6's predicted sign - religious women who do "
        "have sex may use hormonal contraception MORE, to conceal stigmatised nonmarital activity, "
        "so stigma of premarital sex raises use while stigma of contraception lowers it.")


def main():
    rows = list(csv.DictReader(CSVP.open()))
    fields = list(rows[0].keys())
    hit = next((r for r in rows if r["id"] == WID), None)
    if not hit:
        print(f"{WID} not in {CSVP}", file=sys.stderr)
        return 2
    if hit["note"].startswith("VERIFIED FULL-TEXT READ"):
        print("already corrected — regenerating the log only")
    else:
        hit["note"] = NOTE
        hit["dose_unit"] = "DERIVABLE"
        hit["stigma_bearer"] = "COMMUNITY"     # the A.6-apt measure is others' approval, not self
        with CSVP.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"corrected the note for {WID}; stigma_bearer SELF -> COMMUNITY")

    marker = "\n## Correction to the second read (`419`)\n"
    base = LOGP.read_text().split(marker)[0].rstrip() if LOGP.exists() else ""
    sec = [marker.strip(), "",
           f"`{WID}` was reclassified by `418` on **ten keyword greps and roughly 2,500 characters",
           "of context windows** out of a 9,619-word paper. The abstract, measures, specification",
           "and tables were not read, yet the note asserted a design and a measurement scale. The",
           "cell was right; the basis was not adequate, and a note that overstates what was read is",
           "worse than a wrong cell, because a later reader cannot tell which claims were checked.",
           "", "Verified read, and what changed:", "",
           "| claim in `418`'s note | status after reading |",
           "|---|---|",
           "| weekly longitudinal panel | **confirmed** — RDSL, 39,806 person-weeks across 680 women, weekly journals over 2.5 years |",
           "| mediation design | **confirmed** — the paper's own framing: religiosity \"operates largely through women's reproductive attitudes, anticipated feelings of guilt after sex\" |",
           "| \"moral opposition to birth control\" on a 0–4 scale | **corrected** — the item is *\"birth control is morally wrong\"*, a real repeatedly-measured variable, but an **internal moral belief**, which wall 5 puts nearer D.1.a |",
           "| A.6's construct is separately dosed | **confirmed on a different measure** — *\"friends' approval of sex without birth control\"* (0–5), with parents' and friends' approval: the normative-environment block, i.e. social cost |",
           "",
           "The reclassification to `LINK_NORM_USE` therefore stands, on **stronger** grounds than",
           "`418` gave: the record separately measures both sides of wall 5 — private moral belief",
           "(D.1.a) and perceived social approval (A.6) — which makes it the cleanest empirical",
           "statement of that distinction in the corpus and the natural evidence base for PI call 5.",
           "`stigma_bearer` corrected from `SELF` to `COMMUNITY` accordingly.", "",
           "### A wrinkle for §11, found only by reading it", "",
           "The paper's **\"contraceptive work-around\"** mechanism runs *against* A.6's predicted",
           "sign. Because a nonmarital pregnancy would expose stigmatised sexual activity, highly",
           "religious women who do have sex may use hormonal contraception **more**, to conceal it.",
           "So stigma attached to *premarital sex* raises contraceptive use while stigma attached to",
           "*contraception* lowers it, and a study that does not separate the two objects can",
           "recover either sign. A.6's registered claim assumes only the second. This belongs in the",
           "chapter's identification-threats section and would not have been found from an abstract.",
           ""]
    LOGP.write_text(base + "\n\n" + "\n".join(sec) + "\n")
    print(f"wrote the correction into {LOGP.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
