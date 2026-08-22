# A3 cold-start anchors — twinning-multiple-births (A.12)

Sourced in a live OpenAlex pass (2026-08-22) and resolved through five gates: 25 candidate anchors, of which 9 are empirical primary-cell anchors (the causal recall denominator) and the rest are exposure-series, ART-multiples, PM-variation or routing-decoy anchors that earn no empirical recall credit. No DOI is hand-asserted; each is the top-ranked version-of-record candidate from a unified Crossref + OpenAlex field, then re-affirmed at doi.org.

**Read the cell counts with the chapter's structure in mind.** A.12 is an accounting identity with a behavioral offset. The mechanical arm is arithmetic that no study estimates, so a small `PRIMARY_*` count is the CORRECT state of the world here and not a thin literature. The load-bearing cell for the verdict is `EXPOSURE_SERIES`, which feeds the stage-10 computation.

**Verified (live DOI): 22**  ·  **Year-drift keep (real, RA-confirm): 0**  ·  **Flagged for RA: 0**  ·  **Expected index miss (no DOI by nature): 3**

**Shadow records refused: 0** across 0 anchors.  **Integrity flags raised: 0.**

**Duplicate records demoted: 4** across 2 anchors. Two independent catches were predicted before the run. Pison & D'Addato 2006 carries 10.1375/twin.9.2.250 (98 cites) and 10.1375/183242706776382338 (66) with identical title, year, venue and authors. Black, Devereux & Salvanes 2005 carries 10.1162/0033553053970179 (1,049) and 10.1093/qje/120.2.669 (446) — the QJE MIT-Press-to-OUP DOI migration. **The QJE case generalises beyond this chapter**: any hypothesis anchoring on a pre-migration QJE article will meet a split citation count, and it should be handled in the shared resolver rather than rediscovered per chapter.

**Review-shape or author refusals: 1.** The book-canon gate meets its strongest case in the project here, and the run surfaced more than the sourcing pass did. Bulmer 1970 carries **FIVE** distinct review records. The book gate refuses three as `review_of_the_work` — Shields 1970 in Journal of Medical Genetics (typed `journal-article`), Benirschke 1971 in Teratology (typed `book-review`), and a **Science** review at 10.1126/science.170.3961.965 that the sourcing pass did not find. Two more are caught upstream by the title gate because they embed the author's name in the title (10.2307/1295801, 10.1086/406989). Only one record in five is typed `book-review`, so a type-based rule would recover one case in five. The Science review is the one that matters most: highest visibility of the group, and the worst contaminant of a citation frame.

## Cell counts

| Cell | Verified / total |
|---|---|
| `EXPOSURE_SERIES` | 3/5 |
| `OFF_HOMONYM_CRYSTAL` | 1/1 |
| `OFF_HOMONYM_ENGINEERING` | 1/1 |
| `OFF_NONHUMAN` | 1/1 |
| `OFF_PERINATAL` | 1/1 |
| `OFF_TWINDESIGN` | 1/1 |
| `PRIMARY_OFFSET_FIRSTSTAGE` | 5/6 |
| `PRIMARY_OFFSET_STOPPING` | 3/3 |
| `SECONDARY_ART_MULTIPLES` | 5/5 |
| `SECONDARY_PM_VARIATION` | 1/1 |

## Resolution log

- **The Impact of Multiple Births on Fertility: Stopping and Spacing in ** (2024, primary-offset) -> VERIFIED  doi=10.1215/00703370-11577526  J=0.778  [journal-article]  auth=True  (Demography)
- **Parity progression ratios confirm higher lifetime fertility in women** (2012, primary-offset) -> VERIFIED  doi=10.1098/rspb.2012.0436  J=1.0  [journal-article]  auth=True  (Proceedings of the Royal Society B)
- **Twins Support the Absence of Parity-Dependent Fertility Control in P** (2020, primary-offset) -> VERIFIED  doi=10.1007/s13524-020-00898-0  J=1.0  [journal-article]  auth=True  (Demography)
- **Testing the Quantity-Quality Fertility Model: The Use of Twins as a ** (1980, twin-iv-canon) -> VERIFIED  doi=10.2307/1912026  J=1.0  [journal-article]  auth=True  (Econometrica)
- **The More the Merrier? The Effect of Family Size and Birth Order on C** (2005, twin-iv-canon) -> VERIFIED  doi=10.1162/0033553053970179  J=1.0  [journal-article]  auth=True  (Quarterly Journal of Economics)
- **Multiple Experiments for the Causal Link between the Quantity and Qu** (2010, twin-iv-canon) -> VERIFIED  doi=10.1086/653830  J=1.0  [journal-article]  auth=True  (Journal of Labor Economics)
- **The Economic Consequences of Unwed Motherhood: Using Twin Births as ** (1994, twin-iv-canon) -> BOOK-NO-DOI (expected)  best-J=1.0  refused=title_or_no_doi
- **Do Population Control Policies Induce More Human Capital Investment?** (2009, twin-iv-canon) -> VERIFIED  doi=10.1111/j.1467-937x.2009.00563.x  J=1.0  [journal-article]  auth=True  (Review of Economic Studies)
- **Increasing the credibility of the twin birth instrument** (2018, twin-iv-canon) -> VERIFIED  doi=10.1002/jae.2616  J=1.0  [journal-article]  auth=True  (Journal of Applied Econometrics)
- **Twin Peaks: more twinning in humans than ever before** (2021, art-multiples) -> VERIFIED  doi=10.1093/humrep/deab029  J=1.0  [journal-article]  auth=True  (Human Reproduction)
- **Twinning Rates in Developed Countries: Trends and Explanations** (2015, art-multiples) -> VERIFIED  doi=10.1111/j.1728-4457.2015.00088.x  J=1.0  [journal-article]  auth=True  (Population and Development Review)
- **Trends in Multiple Births Conceived Using Assisted Reproductive Tech** (2003, art-multiples) -> VERIFIED  doi=10.1542/peds.111.s1.1159  J=0.786  [journal-article]  auth=True  (Pediatrics)
- **Elective Single-Embryo Transfer versus Double-Embryo Transfer in In ** (2004, eset-policy) -> VERIFIED  doi=10.1056/nejmoa041032  J=1.0  [journal-article]  auth=True  (New England Journal of Medicine)
- **Clinical effectiveness of elective single versus double embryo trans** (2010, eset-policy) -> VERIFIED  doi=10.1136/bmj.c6945  J=1.0  [journal-article]  auth=True  (BMJ)
- **The Human Multiple Births Database (HMBD)** (2023, exposure-series) -> VERIFIED  doi=10.4054/demres.2023.48.4  J=1.0  [journal-article]  auth=True  (Demographic Research)
- **Three decades of twin births in the United States, 1980-2009** (2012, exposure-series) -> BOOK-NO-DOI (expected)  best-J=1.0  refused=title_or_no_doi
- **The Biology of Twinning in Man** (1970, exposure-series) -> BOOK-NO-DOI (expected)  best-J=1.0  refused=review_of_the_work,title_or_no_doi
- **Frequency of Twin Births in Developed Countries** (2006, exposure-series) -> VERIFIED  doi=10.1375/twin.9.2.250  J=1.0  [journal-article]  auth=True  (Twin Research and Human Genetics)
- **Dizygotic twinning** (2007, exposure-series) -> VERIFIED  doi=10.1093/humupd/dmm036  J=1.0  [article]  auth=True  (Human Reproduction Update)
- **Twinning across the Developing World** (2011, pm-variation) -> VERIFIED  doi=10.1371/journal.pone.0025239  J=1.0  [journal-article]  auth=True  (PLoS ONE)
- **A short history of SHELX** (2007, decoy-crystallography) -> VERIFIED  doi=10.1107/s0108767307043930  J=1.0  [article]  auth=True  (Acta Crystallographica Section A F)
- **High strength Fe-Mn-(Al, Si) TRIP/TWIP steels development - properti** (2000, decoy-engineering) -> VERIFIED  doi=10.1016/s0749-6419(00)00015-2  J=0.769  [journal-article]  auth=True  (International Journal of Plasticit)
- **An Observational Analysis of Twin Births, Calf Sex Ratio, and Calf M** (2007, decoy-nonhuman) -> VERIFIED  doi=10.3168/jds.s0022-0302(07)71614-4  J=1.0  [journal-article]  auth=True  (Journal of Dairy Science)
- **Hidden heritability due to heterogeneity across seven populations** (2017, decoy-twindesign) -> VERIFIED  doi=10.1038/s41562-017-0195-1  J=1.0  [journal-article]  auth=True  (Nature Human Behaviour)
- **Perinatal outcome of singletons and twins after assisted conception:** (2004, decoy-perinatal) -> VERIFIED  doi=10.1136/bmj.37957.560278.ee  J=1.0  [journal-article]  auth=True  (BMJ)

## Findings this run is designed to test, recorded in advance

- **v5's seminal list for A.12 is three-for-three defective, and the third is a trap.** Bulmer 1970 resolves but carries three review records. Pison & D'Addato 2006 has the wrong title in v5 (*in Developed Countries*, not *among the world populations*) and duplicate DOIs. Hoekstra 'et al. 2008' is **2007** — *Dizygotic twinning*, Human Reproduction Update, 10.1093/humupd/dmm036, 203 cites. A real Hoekstra 2008 paper exists (*Body composition, smoking, and spontaneous dizygotic twinning*, Fertility & Sterility, 50 cites), so a resolver trusting v5's year lands on a DIFFERENT paper by the same first author and reports success. A wrong year pointing at a real neighbouring paper is more dangerous than one pointing at nothing.
- **Wall 6 was re-cut on OUTCOME before this run, and three anchors sit on the seam.** PI Call 3 (split at the margin) made the drafted treatment-based Wall 6 self-defeating: it excluded transfer-protocol studies, which are the only quasi-experimental variation in the multiplier that exists. Reynolds et al. 2003 is the INCLUDE side (population multiple-birth outcome); Thurin et al. 2004 and McLernon et al. 2010 are the genuine boundary (per-cycle clinical outcomes reported ALONGSIDE multiple-birth rates); Helmerhorst et al. 2004 is the EXCLUDE side and the sharpest test, sitting on three walls at once. If the screen cannot separate these four, the wall is not enforceable and the scope must be amended to say so.
- **The version-of-record gate meets an inverted-citation case.** Rosenzweig & Zhang's SSRN preprint (2006, 65 cites) out-cites the Review of Economic Studies version of record (2009, 11). Citation-argmax ranking takes the preprint. Separately, the reconnaissance reported a 348-cite 'Rosenzweig & Zhang 2008, Demography' record that the sourcing pass could not reproduce — flagged for RA and NOT assumed to be the same paper.
- **The author gate must handle a record with NO authors.** One of the two 2005 Obstetrical & Gynecological Survey reprints of Thurin et al. carries an empty author list. Missing metadata is missing data and must never be scored as disagreement.
- **Two decoy families are pure homonyms, which is this chapter's carve-out from the standing decoy-cloud guidance.** Crystallographic twinning (SHELX, 87,694 cites) and TWIP steel have zero on-topic content and take hard exclusions, not routing decisions. The guidance that decoy clouds are boundary cases running 29-88% on-topic does not apply to a homonym. The behaviour-genetics family (Tropf et al. 2017, A.18) IS an ordinary boundary case and is routed, not excluded.
- **The primary cell's head is a 2024 paper.** Alter & Hacker carries six cites. Forward-citation seeding from the chapter's most on-estimand study will return almost nothing at A4, and that is a property of the literature rather than a failure of the seeding.
- **A gate keyed off an optional field can disengage invisibly, and did on this run's first pass.** `is_book` is optional and the book-canon gate reads it through `cand.get("is_book")`. Bulmer was first entered with `expect_no_doi=True` but WITHOUT `is_book=True`, so the gate silently no-opped and the ordinary author gate refused the anchor instead, as `authors_disagree`. The summary counters looked correct and nothing appeared broken — a right answer by a mechanism that does not generalise. Setting the flag changes the refusal reason to `review_of_the_work` and finds three reviews where the author gate found one. Audited across branches rather than assumed: D.2.d (103), D.1.b (95) and D.3.c (148) all set the flag; B.1 (64) and D.3.b (72) predate the gate. No prior chapter is affected.
- **One serendipitous on-topic find, recorded so it is not lost.** The Bulmer probe refused `10.2139/ssrn.5258235`, *Does the One-Child Policy Increase Man-Made Twinning Rate?*, on the title gate. It is not a Bulmer record, but it IS on A.12's topic — policy-induced twinning — and it did not surface in any reconnaissance probe. Carried forward to A4/A6 as a seed rather than discarded as a refusal.
- **Empirical recall denominator.** Only the `PRIMARY_*` anchors count. The exposure-series, ART-multiples, PM-variation and routing-decoy anchors are indispensable to the stage-10 computation and to the routing rules, and they are not evidence for the hypothesis. Per the Tier-A finding, they are studies in their own right and are not an artifact of the screen.
