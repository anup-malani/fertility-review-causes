#!/usr/bin/env python3
"""
415 — A.6 (TICK-087) stage 6b: apply the full-text decisions for the six library-retrieved records.

`414` ingested six PDFs pulled by hand through the UChicago proxy. Four carry a text layer and were
read; two are Wiley page-image scans with no text layer and are held at `needs_ocr` rather than
screened, because a record that cannot be read is not a record that has been excluded.

What the four say
-----------------
The one that could have been the primary cell was **W1986910339** (Yüceşahin and Özgür 2008),
the only record in this batch with a realized-fertility outcome — provincial TFRs for Turkey,
1980–2000 — estimated by multiple regression. It fails at the *exposure*. The regressor list
(Table 4) is: % illiterate women, % Kurdish women, % Arab women, % Kurdish population, % Arab
population, % women in paid employment, female LFP rate, child mortality rate, GDP per capita.
There is no normative variable in it. Illiteracy is C.2.e's and D.2.a's, child mortality is A.1's,
GDP is C.1.a's, and the ethnicity shares are compositional proxies that dose no norm. Rubric rule 4
fires: `OFF_OTHER`.

**W2187750596** (Ragan 2012) is the most interesting of the four and the closest anything in this
chapter has come. Historical out-of-wedlock childbearing predicts a quarter of demand for the Pill
across Swedish communities, robust to economic, demographic, marriage-market and religion controls
and to community fixed effects. The exposure is genuinely a social-sanction construct and the
design is a real panel. But the outcome is **demand for the Pill** — contraceptive adoption — so
ruling 2 makes it `LINK_NORM_USE`. It also exposes a gap in the rubric: see below.

**W3121483375** (Prettner and Strulik 2017) is a theory paper — two steady states, a separatrix,
numerical simulation — in which social norms against contraception and fertility are jointly
determined. No estimation, so rule 6 gives `CONTEXT_STIGMA_MEASURE` with `estimator_class:
SIMULATION`. It is nonetheless the best available *theoretical* statement of A.6's mechanism and
belongs in the chapter's §2.

**W4403200839** (Yeatman and Sennott 2024) is a conceptual model, so also
`CONTEXT_STIGMA_MEASURE` — but it is the most useful non-study in the corpus, because it
explicitly separates the **acceptability** of contraception from its **accessibility**. That is
wall 4's distinction (A.6 versus A.5), stated by someone else in PDR, and PI call 4 should cite it.

A rubric gap, recorded rather than patched over
-----------------------------------------------
Ragan's exposure is norms about premarital sex and out-of-wedlock childbearing. That is D.2.b's
registered territory (Marriage and Family Norms), not the stigma of fertility control itself, and
the rubric has no `MIXED_NORM_MARRIAGE` cell to route it to. S4 position 84 ("Passing as 'Normal':
Adolescent Girls' Strategies for Escaping Stigma of Premarital Sex and Childbearing") is a second
instance, so this is a class and not a one-off. The rubric's own instruction is to add a cell and
re-run over completed batches. **That is not done here**: adding a rule-5 cell for marriage norms
would reclassify records already screened, and which way it should cut is a scope question about the
A.6/D.2.b boundary that the scope doc never measured — D.2.b is not among its six walls. Raised as
PI call 7 instead, with both records flagged for second read.
"""
import csv, pathlib, sys
from collections import Counter

SLUG = "stigma-reduction-contraception-abortion"
CSVP = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
LOGP = pathlib.Path("literature/search-logs") / f"{SLUG}-screen-log.md"

DECISIONS = {
    "W1986910339": {
        "cell": "OFF_OTHER", "outcome_level": "REALIZED", "dose_unit": "NONE",
        "phenomenon_window": "FDT", "estimator_class": "OLS_ADJUSTED",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "no",
        "note": ("FULL TEXT READ (14,396 words, library proxy). Yucesahin and Ozgur 2008. Has a "
                 "realized-fertility outcome - provincial TFR, Turkey 1980-2000 - by multiple "
                 "regression, and was the only record in the library batch that could have been "
                 "the primary cell. Fails rule 4 on the EXPOSURE: the Table 4 regressor list is "
                 "% illiterate women, % Kurdish women, % Arab women, % Kurdish population, % Arab "
                 "population, % women in paid employment, female LFP, child mortality, GDP per "
                 "capita. No normative variable. Illiteracy is C.2.e/D.2.a, child mortality A.1, "
                 "GDP C.1.a; ethnicity shares are compositional proxies dosing no norm.")},
    "W2187750596": {
        "cell": "LINK_NORM_USE", "outcome_level": "USE", "dose_unit": "NONE",
        "phenomenon_window": "FDT", "estimator_class": "OLS_ADJUSTED",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "yes",
        "note": ("FULL TEXT READ (13,962 words). Ragan 2012, Stockholm School of Economics working "
                 "paper - no DOI, and 412's only recorded URL had 404'd. The closest this chapter "
                 "has come: historical out-of-wedlock childbearing predicts a quarter of Pill "
                 "demand across Swedish communities, robust to economic, demographic, "
                 "marriage-market and religion controls and to community fixed effects, with a "
                 "social-sanction model behind it. Outcome is DEMAND FOR THE PILL, so ruling 2 "
                 "makes it link evidence. RUBRIC GAP: the exposure is premarital-sex and "
                 "out-of-wedlock norms, which is D.2.b's territory, and there is no "
                 "MIXED_NORM_MARRIAGE cell - see PI call 7.")},
    "W3121483375": {
        "cell": "CONTEXT_STIGMA_MEASURE", "outcome_level": "NONE", "dose_unit": "NONE",
        "phenomenon_window": "BOTH", "estimator_class": "SIMULATION",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "no",
        "note": ("FULL TEXT READ (12,754 words). Prettner and Strulik, Rev Dev Econ 21(3) 2017 - "
                 "note the journal year is 2017 though OpenAlex records 2016. A THEORY paper: two "
                 "steady states separated by a separatrix, with a norm against modern "
                 "contraceptives sustained at the traditional steady state, illustrated "
                 "numerically. No estimation, so rule 6 gives context. Nonetheless the best "
                 "theoretical statement of A.6's mechanism found anywhere in the corpus and it "
                 "belongs in the chapter's section 2.")},
    "W4403200839": {
        "cell": "CONTEXT_STIGMA_MEASURE", "outcome_level": "NONE", "dose_unit": "NONE",
        "phenomenon_window": "SDT", "estimator_class": "OTHER_LOUD",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "no",
        "note": ("FULL TEXT READ (14,131 words). Yeatman and Sennott, PDR 2024. A conceptual "
                 "model, so rule 6 gives context - but the most useful non-study in the corpus: it "
                 "explicitly separates the ACCEPTABILITY of contraception from its ACCESSIBILITY, "
                 "which is wall 4's A.6-versus-A.5 distinction stated independently in PDR. Cite "
                 "in PI call 4.")},
}
OCR = {
    "W2112312272": ("Caldwell, PDR 1999 - filename says 2004, watermark and DOI say 1999"),
    "W1976018943": ("Wolff, Studies in Family Planning 2000 - filename says 2003, watermark says "
                    "2000; the one record whose outcome may be parity rather than use"),
}
OCR_NOTE = (" HELD AT needs_ocr: retrieved by proxy but the Wiley PDF is page images with no text "
            "layer (37-38 words/page of watermark only, 1 embedded font). Cannot be screened until "
            "OCR'd; not excluded.")


def main():
    rows = list(csv.DictReader(CSVP.open()))
    fields = list(rows[0].keys())
    done = sum(1 for r in rows if r["id"] in DECISIONS and r["cell"] != "INSUFFICIENT_INFO")
    if done == len(DECISIONS):
        print(f"decisions already applied to {done} rows — regenerating the log only")
    else:
        for r in rows:
            if r["id"] in DECISIONS:
                r.update(DECISIONS[r["id"]])
            elif r["id"] in OCR and "needs_ocr" not in r["note"]:
                r["note"] = r["note"].split("LIBRARY RETRIEVAL")[0].rstrip() + OCR_NOTE
        with CSVP.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"applied {len(DECISIONS)} decisions; {len(OCR)} held at needs_ocr")

    rows = list(csv.DictReader(CSVP.open()))
    tally = Counter(r["cell"] for r in rows)
    primary = [r for r in rows if r["cell"] == "PRIMARY_NORM_FERTILITY"]
    link = [r for r in rows if r["cell"] == "LINK_NORM_USE"]
    blocked = [r for r in rows if r["cell"] == "INSUFFICIENT_INFO"]

    marker = "\n## Library full-text stage (`414`, `415`)\n"
    body = LOGP.read_text().split(marker)[0].rstrip() if LOGP.exists() else ""
    sec = [marker.strip(), "",
           "Shravan pulled all six remaining records by hand through the UChicago proxy. Four",
           "carry a text layer and were read; two are Wiley page-image scans held at `needs_ocr`,",
           "because a record that cannot be read has not been excluded.", "",
           "| id | what it is | cell | why |", "|---|---|---|---|",
           "| `W1986910339` | Yüceşahin and Özgür 2008, provincial TFR in Turkey by multiple regression | `OFF_OTHER` | **the only library record with a realized-fertility outcome, and it fails on the exposure** — no normative regressor in Table 4 |",
           "| `W2187750596` | Ragan 2012, out-of-wedlock norms and Pill demand in Sweden | `LINK_NORM_USE` | the closest the chapter has come; outcome is Pill demand, so ruling 2 applies |",
           "| `W3121483375` | Prettner and Strulik 2017, two-steady-state theory | `CONTEXT_STIGMA_MEASURE` | theory with numerical simulation; no estimation |",
           "| `W4403200839` | Yeatman and Sennott 2024, conceptual model | `CONTEXT_STIGMA_MEASURE` | framework; separates acceptability from accessibility |",
           "", "### The near-miss, stated plainly", "",
           "`W1986910339` is worth dwelling on because it is the mirror image of every other",
           "near-miss in this chapter. Everywhere else the exposure was right and the outcome was",
           "contraceptive use. Here the outcome is right — provincial TFR, 1980–2000 — and the",
           "exposure is wrong: illiteracy, ethnicity shares, female employment, child mortality and",
           "GDP, with no norm dosed at all. The chapter has now failed to find a study with A.6's",
           "exposure and A.6's outcome from both directions.", "",
           "### Rubric gap — PI call 7", "",
           "Ragan's exposure is norms about premarital sex and out-of-wedlock childbearing, which",
           "is **D.2.b**'s registered territory, and the rubric has no `MIXED_NORM_MARRIAGE` cell.",
           "S4 position 84 is a second instance, so this is a class. The rubric says to add a cell",
           "and re-run over completed batches; that is deliberately **not** done here, because",
           "which way an A.6/D.2.b boundary should cut is a scope question and D.2.b is not among",
           "the scope doc's six walls. Both records are flagged for second read.", "",
           f"### `PRIMARY_NORM_FERTILITY`: **{len(primary)}** · `LINK_NORM_USE`: **{len(link)}** · "
           f"still unreadable: **{len(blocked)}**", ""]
    for wid, what in OCR.items():
        sec.append(f"- `{wid}` — {what}")
    sec += ["", f"### Tally across {len(rows)} screened records", "", "| cell | n |", "|---|---|"]
    for c, n in tally.most_common():
        sec.append(f"| `{c}` | {n} |")
    LOGP.write_text(body + "\n\n" + "\n".join(sec) + "\n")

    print(f"PRIMARY_NORM_FERTILITY={len(primary)}  LINK_NORM_USE={len(link)}  "
          f"needs_ocr/blocked={len(blocked)}")
    print(dict(tally))
    return 0


if __name__ == "__main__":
    sys.exit(main())
