#!/usr/bin/env python3
"""
417 — A.6 (TICK-087) stage 6c: apply the last two full-text decisions and close the primary cell.

With `416`'s OCR, all 8 of the records the screen left unresolved have now been read. These are the
final two, and they complete the pattern the whole chapter has traced.

`W1976018943` — Wolff, Blanc and Ssekamatte-Ssebuliba, *Studies in Family Planning* 31(2), 2000.
**Partner opposition** as the exposure: not a proxy for it, the thing itself, and the closest match
to A.6's registered construct found anywhere in 2,815 candidates. Quantified, too — partner
opposition accounts for roughly 20% of unmet need in urban Uganda, 12% rural, 15% overall, with a
shift in method mix toward traditional methods. And the outcome is **unmet need and contraceptive
mix**, so ruling 2 makes it link evidence.

The authors say why, themselves. Examining the question A.6 actually asks "would require a
prospective study over time to observe the fertility outcomes of disagreement" — a study they did
not do and, as far as this chapter's 164 screened records show, nobody has. That sentence is the
chapter's single best citation: the best-matched exposure study in the literature states in its own
words that the fertility outcome is unobserved.

`W2112312272` — Caldwell, *PDR* 1999. A historical-interpretive essay on why the fertility decline
in English-speaking countries lagged the French one, and its answer is A.6's mechanism: moral and
religious disapproval of contraception ("moral" 39 times, "religious"/"religion" 22, "taboo" 3,
"acceptability" 4) held back a decline that economic conditions had already made inevitable. No
estimation — zero regressions and one table — so rule 6 gives context. It matters anyway, because
it is the **only substantial FDT-phenomenon treatment of A.6 in the corpus**, and the chapter's FDT
cell is otherwise entirely empty. It belongs in §2 alongside Prettner and Strulik.

So the primary cell closes empty with every retrievable record read. The chapter's finding is not
that the evidence is weak. It is that the study A.6 requires — a normative exposure, a fertility
outcome, and identification — does not exist in this literature, and two of its best papers say so
in their own words: Wolff by naming the prospective study nobody has run, Caldwell by arguing the
case historically rather than estimating it.

A caveat on the OCR, recorded because it bears on how these two may be used. `416` recovered 548
and 821 words per page, which is ample for screening, but the text is noisy: Wiley's vertical
download watermark interleaves with the body text and two-column pages mix across line breaks. The
cell assignments here rest on abstracts, section headings and table structure, all of which survived
cleanly. **Any quotation from these two must be checked against the PDF before it reaches a
chapter.**
"""
import csv, pathlib, sys
from collections import Counter

SLUG = "stigma-reduction-contraception-abortion"
CSVP = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
LOGP = pathlib.Path("literature/search-logs") / f"{SLUG}-screen-log.md"
RETR = pathlib.Path("extraction") / f"{SLUG}-pdf-retrieval-log.csv"

DECISIONS = {
    "W1976018943": {
        "cell": "LINK_NORM_USE", "outcome_level": "USE", "dose_unit": "REPORTED",
        "phenomenon_window": "FDT", "estimator_class": "OLS_ADJUSTED",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "PARTNER",
        "second_read_required": "yes",
        "note": ("FULL TEXT READ after OCR (11,505 words, 821/page). Wolff, Blanc and "
                 "Ssekamatte-Ssebuliba, Stud Fam Plann 31(2) 2000, Uganda NRO 1995-96. PARTNER "
                 "OPPOSITION as the exposure - the thing itself, not a proxy - and the closest "
                 "match to A.6's registered construct in 2,815 candidates. Quantified: partner "
                 "opposition accounts for ~20% of unmet need in urban areas, 12% rural, 15% "
                 "overall, plus a shift in method mix toward traditional methods. Outcome is unmet "
                 "need and method mix, so ruling 2 makes it link evidence. dose_unit REPORTED: the "
                 "share-of-unmet-need-attributable figure is convertible toward section 5's unit. "
                 "THE CHAPTER'S BEST CITATION - the authors state that the question A.6 asks "
                 "'would require a prospective study over time to observe the fertility outcomes "
                 "of disagreement', which they did not do and nobody in this corpus has.")},
    "W2112312272": {
        "cell": "CONTEXT_STIGMA_MEASURE", "outcome_level": "REALIZED", "dose_unit": "NONE",
        "phenomenon_window": "FDT", "estimator_class": "OTHER_LOUD",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "no",
        "note": ("FULL TEXT READ after OCR (19,183 words, 548/page). Caldwell, PDR 1999 - note "
                 "OpenAlex and the Wiley filename disagree on the year; the watermark and DOI say "
                 "1999. A historical-interpretive essay arguing that MORAL AND RELIGIOUS "
                 "disapproval of contraception delayed the decline in English-speaking countries "
                 "below what economic conditions had already made inevitable: 'moral' 39 times, "
                 "'religious'/'religion' 22, 'taboo' 3, 'acceptability' 4. Zero regressions and "
                 "one table, so rule 6 gives context. Matters anyway as the ONLY substantial "
                 "FDT-phenomenon treatment of A.6 in the corpus; belongs in chapter section 2 "
                 "beside Prettner and Strulik.")},
}


def main():
    rows = list(csv.DictReader(CSVP.open()))
    fields = list(rows[0].keys())
    done = sum(1 for r in rows if r["id"] in DECISIONS and r["cell"] != "INSUFFICIENT_INFO")
    if done == len(DECISIONS):
        print(f"decisions already applied — regenerating the log only")
    else:
        for r in rows:
            if r["id"] in DECISIONS:
                r.update(DECISIONS[r["id"]])
        with CSVP.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"applied {len(DECISIONS)} decisions")

    rows = list(csv.DictReader(CSVP.open()))
    tally = Counter(r["cell"] for r in rows)
    primary = [r for r in rows if r["cell"] == "PRIMARY_NORM_FERTILITY"]
    link = [r for r in rows if r["cell"] == "LINK_NORM_USE"]
    unread = [r for r in rows if r["cell"] == "INSUFFICIENT_INFO"]
    retr = list(csv.DictReader(RETR.open())) if RETR.exists() else []
    got = sum(1 for r in retr if r["status"] == "retrieved")
    second = [r for r in rows if r["second_read_required"] == "yes"]

    marker = "\n## Primary cell closed (`416`, `417`)\n"
    body = LOGP.read_text().split(marker)[0].rstrip() if LOGP.exists() else ""
    sec = [marker.strip(), "",
           f"All **{got} of {len(retr)}** unresolved records are now read — 2 by open access, 6 by "
           f"hand through the UChicago proxy, 2 of those 6 only after OCR.", "",
           "### The last two", "",
           "| id | what it is | cell |", "|---|---|---|",
           "| `W1976018943` | Wolff et al., *Stud Fam Plann* 2000 — **partner opposition** and unmet need in Uganda | `LINK_NORM_USE` |",
           "| `W2112312272` | Caldwell, *PDR* 1999 — moral and religious disapproval and the delayed Western decline | `CONTEXT_STIGMA_MEASURE` |",
           "",
           "Wolff is the closest match to A.6's registered exposure in the whole pool: partner",
           "opposition itself, quantified at roughly 15% of unmet need overall. Its outcome is",
           "unmet need and method mix. **The authors name the missing study themselves** — the",
           "question A.6 asks \"would require a prospective study over time to observe the fertility",
           "outcomes of disagreement\", which they did not do and which nothing in these 164",
           "screened records has done.", "",
           "Caldwell is the only substantial **FDT** treatment of A.6's mechanism in the corpus, and",
           "the FDT cell is otherwise empty. It argues the case historically — zero regressions, one",
           "table — rather than estimating it.", "",
           f"### `PRIMARY_NORM_FERTILITY`: **{len(primary)}** — closed", ""]
    if not primary and not unread:
        sec += ["Empty, with **every retrievable record read**. Seven channels agree:", "",
                "| channel | result |", "|---|---|",
                "| identified-design share of the frame | 12 / 668 |",
                "| realized-fertility share of the frame | 58 / 668 |",
                "| anchor reachability, stage-2 frame | 0 / 15 |",
                "| citation bridges | 8, none an estimate |",
                "| exhaustive screen | 0 / 164 |",
                "| full text of the decider | `LINK_NORM_USE` |",
                "| full text of the remaining 7 | 0 primary |", "",
                "The finding is not that the evidence is weak. It is that the study A.6 requires —",
                "normative exposure, fertility outcome, identification — does not exist in this",
                "literature, and two of its best papers say so in their own words: Wolff by naming",
                "the prospective study nobody has run, Caldwell by arguing the case historically",
                "instead of estimating it.", "",
                "Per scope §12 the verdict is **UNEVALUATED with the failed route named** — R1 for",
                "want of an identified fertility outcome, R3 for want of a pre-1985 dose series —",
                f"and explicitly not \"weak evidence\". `LINK_NORM_USE` stands at **{len(link)}** and",
                "is poolable as stratum 3 under a heading that disclaims it as the parameter.", "",
                "### What is still open", "",
                f"- **{len(second)} records flagged for second read**, per the rubric's asymmetric",
                "  rule: `W108787496` and `W2187750596` (reclassifications of the two "
                "highest-prior records), plus the batch-1 provisional calls.",
                "- **PI call 7** — the `MIXED_NORM_MARRIAGE` rubric gap on the A.6/D.2.b boundary.",
                "- **The sampled tail** (S5/S6/S7, 240 of 2,651 records) is unread. It bounds the",
                "  chance the flagger misrouted a primary-cell study out of the exhaustive strata;",
                "  that bound is not yet established.",
                "- **OCR noise**: `416` recovered 548 and 821 words/page, ample for screening, but",
                "  Wiley's vertical watermark interleaves with body text and two-column pages mix",
                "  across line breaks. Cell assignments rest on abstracts, headings and table",
                "  structure, which survived cleanly. **Any quotation from those two must be checked",
                "  against the PDF before it reaches a chapter.**", ""]
    sec += [f"### Tally across {len(rows)} screened records", "", "| cell | n |", "|---|---|"]
    for c, n in tally.most_common():
        sec.append(f"| `{c}` | {n} |")
    LOGP.write_text(body + "\n\n" + "\n".join(sec) + "\n")

    print(f"PRIMARY_NORM_FERTILITY={len(primary)}  LINK_NORM_USE={len(link)}  "
          f"unread={len(unread)}  full_text={got}/{len(retr)}  second_read_owed={len(second)}")
    print(dict(tally))
    return 0


if __name__ == "__main__":
    sys.exit(main())
