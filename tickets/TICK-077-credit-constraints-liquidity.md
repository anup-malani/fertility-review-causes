# TICK-077: C.3.e Credit Constraints and Liquidity
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `credit-constraints` — HYPOTHESES-v5.md §C.3.e
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/credit-constraints-*, extraction/credit-constraints-*, output/chapters/credit-constraints.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/credit-constraints.csv`, RA verifies a random 10%
- [x] 8. Risk-of-bias assessment per study
- [x] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [x] 10. Demographic significance against PM / FDT / SDT
- [~] 11. GRADE rating, 3 independent raters
- [x] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Inherited boundary work

Three finished chapters have already routed evidence into this one. Read these before drafting scope:

- **C.2.c (housing).** Froze the boundary rule on 2026-07-31: neighbouring hypotheses are separated by
  *what varies*, not by the mechanism an author narrates. **C.2.c owns variation in housing prices;
  C.3.e owns variation in liquidity and credit terms; A.23 owns variation in co-residence.** Under that
  rule C.2.c routed out a 2026 *PNAS* cohort-DiD of a Chinese housing-provident-fund reform (the reform
  moved down-payment ratios, interest rates and loan ceilings, not prices) and created a
  `MIXED_PRICE_CREDIT` class, flagged unallocated and to be reported here. See
  `literature/search-logs/housing-costs-search-scope.md` §Wall 1 and `output/chapters/housing-costs.md` §6.
- **C.3.g (student debt).** General consumer, mortgage and medical debt is C.3.e's; C.3.g keeps only the
  prior education liability already spent.
- **A.23 (co-residence).** Owns living-arrangement variation whatever drives it.

## Open rulings to freeze at stage 2

1. **The registered claim names two configurations with opposite signs** — children as a savings/insurance
   vehicle where formal finance is absent (PM/FDT), and liquidity constraints on young households
   delaying births (SDT). Decide whether these are one chapter with two arms or two chapters, and freeze
   it before searching, not at synthesis.
2. **Registry defect inherited from C.2.c, still unfixed:** Lovenheim and Mumford 2013 is listed as
   seminal for both C.2.c and C.3.e. C.2.c's recommendation was to drop it from C.3.e's seminal list and
   cross-ref C.2.c instead; it was flagged, not acted on. This chapter resolves it.

## Log

### 2026-09-01 — scope drafted, both rulings resolved

- `literature/search-logs/credit-constraints-search-scope.md`. Six walls frozen; estimand cells,
  required tags, pooling rule and the demsig pre-specification written before any query.
- **Ruling 1 (asked by Shravan: are the two treatments the same?): no, but they are not separable.**
  Arm S (saving/insurance instrument availability) acts on the *value* of children; Arm B (borrowing
  terms) acts on the *intertemporal budget constraint*; a pure shock to either leaves the other
  untouched. But composite financial-access designs — branch expansion, microfinance, inclusion
  reform — move both at once in opposite directions, and their estimates cannot be allocated to
  either arm. So: **one chapter, two arms, three strata; arms never pooled or averaged; GRADE and
  demsig per arm per phenomenon** (A.18 multi-arm precedent), ≥3-effects test applied after
  stratification.
- **Ruling 2 (RA-authorised by Shravan; awaiting PI confirmation): acted on.** Lovenheim and Mumford 2013 struck from C.3.e's
  `seminal` list in HYPOTHESES-v5.md and cross-referenced to C.2.c, with an in-place RA-edit
  annotation for PI confirmation at TICK-001. C.2.c had recommended and flagged this on 2026-07-31.
- **Two PI calls opened.** Call 1: C.3.c's written chapter already claims "money in a bank, an
  insurance policy" as its substitutes, so Wall 1 — longevity risk to C.3.c, within-life risk to
  C.3.e — is the difference between a two-arm chapter and a one-arm one. Proceeding under the split,
  with a cheap probe to measure it before extraction. Call 2: inherited from A.24, unanswered —
  whether two chapters may both report the same study from a `MIXED_*` class.
- Next: cold-start anchors (hand-sourced, recall scored **per arm**), then the Arm S survival probe.

### 2026-09-01 — anchors resolved 26/26, PI Call 1 answered, shared resolver found dead

- `275_c3e_cold_start_anchors.py`, `276_c3e_arm_s_probe.py`; log at
  `literature/search-logs/credit-constraints-cold-start-anchors-log.md`.
- **26 candidates, 26 resolved, zero absences.** Nine Arm B anchors were inherited
  already-screened from C.2.c's `OFF_CREDIT_C3e` cell, plus the 2026 PNAS provident-fund study
  C.2.c routed here and had already extracted.
- **`title.search` is not a root OpenAlex parameter — the title channel failed 18/18 and every
  resolution silently fell through to `search=`.** Inherited from A.18's script 245, so every
  chapter's anchor resolution ran on the fallback. Fixed here with a quoted `filter=title.search:`
  rung; after the fix 0 of 26 resolve via the fallback. **Flagged to TICK-074** as a shared-resolver
  defect. Also: `%2C` does not escape a comma in a filter value, and the API's own error message
  recommends `%2C`.
- Two further false-absence defects fixed: `is_stem` was one-directional and refused book chapters
  carrying an added "Chapter 8" prefix; a colon-spanning title does not match as one stemmed phrase,
  so a head-quoted rung was added. Both surfaced real anchors that had read as missing.
- **PI Call 1 answered: Arm S survives.** On the on-estimand asset-motive vocabulary the frame is
  262 records, of which 36 (13.7%) are old-age framed — C.3.c has not taken the arm. The first
  measurement said 6.2% and was not usable: "health insurance" alone carried 90% of that block and
  is A.17's estimand, so it is banned from Arm S retrieval.
- One inherited record is a **version pair** (Xi Yang, two DOIs) whose headline sign flips between
  versions, from "More Credit, Fewer Babies?" to "More Credit, More Babies?" — one study, and the
  version of record decides its sign. C.2.c's stored snapshot is stale against the live record.
- Next: snowball the 26 anchors including decoys; production query per arm with per-arm recall.

### 2026-09-01 — snowball (pool 3,810) and production query frozen (frame 7,021)

- `277_c3e_snowball.py`, `278_c3e_production_query.py`, `279_c3e_query_repair.py`; log at
  `credit-constraints-snowball-and-query-log.md`.
- **Snowball pool 3,810, zero errors.** Reach by arm S 2,080 / composite 1,163 / B 745. Decoys were
  seeded deliberately and returned ~340 uniquely-reached records.
- **Four seeds reached 0-1 records because the resolver had matched "Replication data for:" deposits**
  — `dataset` records sharing the article's title, authors AND year, so the author and year gates gave
  no protection. My own bidirectional `is_stem` fix admitted them and its safety justification was
  wrong. Restricted to an allowlist of structural prefixes (chapter/part/section/volume), non-study
  types refused outright, citation count as tiebreak. 0 shadow records after; those seeds now reach
  211-346 each.
- **Version twins add 617 records, 16% of the pool.** Citations do not follow the version of record:
  Dettling and Kearney's JPubE article has 0 citations, its NBER twin 67. Twins found for 12 of 26
  seeds and snowballed with them.
- **Production query frozen at 7,021 records.** Anchor recall 8/11 (S 3/4, B 5/6, composite 0/1).
  Four repair terms kept of 26 candidates, each on gold recovered, not frame growth; `mortgage` was
  refused at +622 records and no gold.
- **A measurement bug in the repair loop, caught and fixed:** candidates were scored against a frozen
  baseline while the kept set grew, so later terms inherited earlier terms' recoveries. It had accepted
  17 terms and 737 records of frame for zero gold.
- **Probes recall 0/9, and that is the composite stratum's answer.** None of the microcredit RCTs,
  savings experiments or branch-expansion studies mentions fertility in its abstract, because none
  measures it. `PRIMARY_COMPOSITE_ACCESS` may be empty — which would leave the sign-flip question
  without direct evidence. Full-text check on the nine before any such statement.

### 2026-09-01 — probe full-text check: 6 of 10 read, zero fertility outcomes

- `280_c3e_probe_retrieval.py`, `281_c3e_probe_outcome_scan.py`, `282_c3e_scan_control.py`; log at
  `credit-constraints-probe-fulltext-check.md`.
- **Zero fertility or birth outcomes in six probe full texts** (~450k chars). The two apparent hits
  were "purchasing power parity" and "place of birth". Two independent channels — abstract indexing and
  full text — now agree, and they fail for unrelated reasons.
- **The scan was validated on positive controls first**: Cumming and Dettling 175 hits / 17 strong,
  Dettling and Kearney 243 / 15, correctly classified. A detector that fires on nothing is
  indistinguishable from a broken one.
- **`?` and `!` inside a QUOTED filter value return a silent zero** — valid meta, no error. All seven
  seeds with a `?` in the title returned zero twins. After the strip: twins for 16 seeds not 12, pool
  3,976, and 870 records (22%) twin-only. Banerjee's OA twin appeared only after this fix.
- Retrieval 6/10, and the twin rung produced 5 of the 6 fetches. Four outstanding, split by cause:
  **browser-job** (Attanasio, Bruhn — open URLs killed by bot defence, 403) and **proxy-job**
  (Guinnane, Prina — no open copy).
- **Status of the composite cell: UNRESOLVED, not empty.** 6 of 10 checked, 0 positive. If the last
  four come back negative, `PRIMARY_COMPOSITE_ACCESS` is empty and the sign-flip question that made
  this one chapter has no direct evidence — UNEVALUATED with GRADE No evidence. Ruling 1 is unaffected:
  the arms stay unpoolable either way.

### 2026-09-01 — the composite cell is NOT empty; four boundary-spanning candidates

- `283_c3e_boundary_hunt.py`; log at `credit-constraints-boundary-hunt-log.md`.
- **Correction to the previous entry.** Six probes reading zero made "the composite cell is empty" the
  natural inference; it is wrong. Four studies pair a financial-access exposure with a fertility
  outcome under an identified design: **Desai and Tarozzi 2011 (Demography, randomized field
  experiment crossing credit with family planning; outcomes contraceptive use, fertility, family-size
  preferences)**, Steele/Amin/Naved 1998 (quasi-experimental panel), Kuchler 2012 (DiD + IV), Lan et
  al. 2023 (IV, fertility intentions).
- **Why it nearly stuck: the anchors were chosen by design celebrity, not by estimand.** The ten probes
  were the 2015 AEJ:Applied microcredit symposium and friends. The microfinance-and-fertility literature
  is a different literature, in Demography and development journals.
- **The channel split is the diagnostic: 112 term-only, 2 provenance-only, 5 both.** The 3,976-record
  snowball found almost none of this, because it was built from the same wrong anchors. A provenance
  channel inherits its anchors' blind spot and cannot confirm a null those anchors caused.
- Bound: 1,463 of 6,018 records have no abstract, so the triage is blind to them.
- All four are retrieval-blocked (2 browser-job, 2 proxy-job). **Handoff is now eight studies**;
  Desai and Tarozzi is the highest-priority item in the chapter.
- Next: the handoff; snowball round 2 seeded from the four new candidates (unexplored neighbourhood);
  fold `banked`/`unbanked` into the frame on the gold-recovered test.

### 2026-09-01 — all eight retrieved; probe bound CLOSED; composite cell has an identified estimate

- Shravan hand-retrieved all eight. `284` installed them by **content**, not filename — two files both
  named `EBSCO-FullText-09_01_2026.pdf`; all eight matched at title overlap 1.00 and the two opaque
  ones were confirmed by hand. `286` scanned them on the 281 code path.
- **Probe bound closed: 10 of 10 read, zero fertility outcomes.** Attanasio 3 hits, Prina 1, Bruhn 0,
  Guinnane 0 — every hit a baseline covariate ("Number of children in the HH") or a summary-stats row.
- **The composite cell has an identified estimate.** Desai and Tarozzi 2011 (*Demography*) randomly
  allocated areas to credit+FP / **credit only** / FP only / control. The credit-only arm is separately
  randomised. Findings: births in the previous three years **−0.106 to −0.166** (small, some
  significant); **desired family size +0.38 to +0.4, significant at 5%**; contraceptive intention −9%.
  Authors: *"consistent with microcredit leading to an increase in the demand for children."*
- **The pattern across all four is in the OUTCOME LEVEL, not the exposure.** Realized fertility: null
  in three independent designs (RCT, DiD+IV, quasi-exp panel). Stated desires/intentions: positive in
  two. Pooling across outcome levels would average a null against a positive and report a number
  describing neither — the pre-registered `OUTCOME_LEVEL` tag is the finding, not bookkeeping.
- **The direction runs AGAINST Arm S.** Arm S predicts access lowers desired fertility; the one
  randomised test raised desired family size. That is Arm B's sign appearing in the composite cell.
  One experiment in rural Ethiopia — not to be over-read, but to be said plainly.
- **Round 2**: pool 365, 297 new (81%), redundancy 18.6%. Heavily contaminated by method citations
  (Wooldridge, Little and Rubin, Stock-Yogo) — strip the method-reference layer before screening.
  Kuchler cites Steele: this literature is internally connected and round 1 reached none of it.
- Next: strip and screen round 2; extract the four with `OUTCOME_LEVEL` mandatory; **power-read Desai
  and Tarozzi** — an uninformative null and a precise zero are recorded very differently in GRADE.

### 2026-09-01 — round 2 screened: 15 composite candidates, and a sign refinement

- `287_c3e_round2_screen.py`; log at `credit-constraints-round2-screen-log.md`.
- **Correction: the method layer is 8.4% (25 of 297), not "heavy".** I read a citation-sorted top-20 as
  if it described the pool; econometrics textbooks own the head of any citation-ordered list. Measured
  and reported as a flag, not used as a gate — the estimand classifier does the screening.
- **15 records pair an exposure with a fertility outcome; all 15 composite, 0 Arm S, 0 Arm B.** Round 2
  extended only the composite cell and is not evidence about the other two arms.
- **Islam, Kamal and Nguyen 2026 (JDS)**: purpose-built 1997-2005 microcredit panel, DiD + matching,
  finds **lower recent fertility and fewer births**. Third version pair in this chapter — the title
  query resolves first to a Figshare deposit; the JDS article is the version of record.
- **Orton et al. 2016 (Bulletin of the WHO)**: systematic review of group-based microfinance health
  impacts over 1 cluster-RCT + 22 quasi-experimental studies. An external-authority anchor source with
  a 23-study base — cheaper than a third snowball round.
- **Sign refinement, against what I said earlier.** "The direction runs against Arm S" came from the
  desires arm alone and was too strong. On REALIZED fertility: two negatives (Desai-Tarozzi RCT, Islam
  et al.) and two nulls (Kuchler, Steele) — Arm S's predicted sign. On STATED desires: positive
  (desired family size +0.38-0.40; intentions up). The two outcome levels carry **opposite signs from
  the same exposure**, so `OUTCOME_LEVEL` is load-bearing for the verdict, not for bookkeeping.
- Bound: **85 of 297 (29%) have no abstract**; the 15 is a floor.
- Next: screen the 15; mine the Orton review's included-study list; retrieve Islam et al. (JDS version);
  **run a separate round seeded from Arm S and Arm B** — they still rest on round 1.

### 2026-09-01 — outcome axis was never calibrated; `parity` was half the frame

- `289_c3e_outcome_axis_loo.py`, `290_c3e_arm_round3.py`; log at `credit-constraints-arm-round3-log.md`.
- **278 calibrated the three exposure axes term by term and accepted the OUTCOME axis as a block.**
  `parity` (for birth parity) plus `interest rate` (Arm B exposure) means **"interest rate parity"
  satisfies both axes with one phrase**. Arm B frame 4,291 with it, 1,073 without.
- **`parity` contributed 3,509 records — half the whole production frame — and ZERO gold.** Dropped.
  Frame re-frozen at **3,512** (was 7,021), recall unchanged at 10/23. Demographic replacements
  return 0-1 records each; that sense is not in these abstracts.
- **Rule applied:** drop for a demonstrated homonym mechanism PLUS zero gold, never zero gold alone —
  `family size` (+912) and `births` (+796) also miss the 23 anchors but are on-estimand and stay.
  Dropping every term that misses the anchors overfits the query to the anchors.
- **288 auto-selected its seeds and returned junk** ("The legacy of Lionel McKenzie"). The classifier
  is a triage; 283 hand-read it before choosing composite seeds, and automating that step reproduced
  the noise. 290's seeds are hand-read and named in the script.
- **Round 3: pool 283, 261 new, and exactly ONE new exposure x outcome record — which is C.3.c's.**
  Two caveats: **all six seeds have empty `referenced_works`**, so it was forward-only and weaker than
  round 2's test; and 30% of new records have no abstract.
- **The yield was the six seeds themselves**, found by the term channel: AGEP Zambia cluster-RCT,
  Delavallade insurance-vs-savings experiment, **Dettling and Kearney 2025 NBER "Did the Modern
  Mortgage Set the Stage for the U.S. Baby Boom?"** (mortgage credit, C.3.e's under Wall 2), Li
  Australia, plus two C.3.c boundary decoys.
- **Coverage reading, held weakly:** round 2 (composite) returned 15, round 3 (S and B) returned 1, so
  the blind spot looks composite-specific — round 1's S and B seeds were estimand-matched from the
  start. Not established: the round was forward-only and 30% blind.

### 2026-09-01 — screening universe 7,327; prescreen; depth probe over 160 records

- `291_c3e_build_screen_universe.py`, `292_c3e_prescreen.py`; log at
  `credit-constraints-screen-depth-probe.md`.
- **The hand-sourced studies were missing from the universe.** A snowball pool holds what the seeds
  REACHED, not the seeds. The 2026 PNAS study C.2.c explicitly routed here, Islam et al. 2026, Yang
  2026, Cain 1983 and Guinnane were all absent until injected as a `hand_*` channel. Also: three known
  records read as absent by ID while present as their version twins — the recall check now matches on
  folded title. Universe complete at 34/34.
- **The two discovery channels overlap by only ~2.5% (91 records).**
- **Prescreen: 3 of 4 rules survived the recall check.** The rejected one would have removed 1,335
  records (20%) and destroyed Prina and Delavallade. 7,327 -> 6,535, retention 34/34.
- **Depth probe, 160 records read.** Yields: `both_channels` ~23% (80 recs), `frame_only` ~6% (2,271),
  `snowball_r2_only` ~4% (269), `snowball_r1_only` ~1% (3,815). The cheapest stratum is 58% of the
  survivors and ~20% of the relevant records; screening order follows the curve, not the count.
- **The probe already found the historical FDT cell the scope memo called the most valuable if it
  existed: "Fertility and Financial Development: Evidence from U.S. Counties in the 19th Century"
  (NBER 2014).** Also "The No-Birth Bonus Scheme: Savings Accounts for Family Planning in South India"
  (PDR 1980, Arm S), "Loans vs. Lives: Credit Obligations and Childbirth in Russia" (2026, Arm B),
  a Thai credit-constraints/family-size panel, and a second systematic review (J Economic Surveys 2020).
- Bounds: 1,672 records (23%) have no abstract; yields are one rater at n=40 per stratum.

### 2026-09-01 — screen wave 1: 349 records, primary pool of 26

- `293_c3e_emit_screen_sheets.py`, `294_c3e_ingest_screen.py`; log at
  `credit-constraints-screen-wave1.md`; routed table at `extraction/credit-constraints-screen.csv`.
- **349 screened, zero validation errors** (no verdict for an off-sheet id, nothing routed twice, all
  349 accounted for with 292 as an explicit `OFF_OTHER_read_not_routed` residual).
- **The probe's yield curve held to within two points:** `both_channels` predicted ~23%, actual 25.0%
  primary; `snowball_r2_only` predicted ~4%, actual 2.2%. The `frame_only` ~6% and `snowball_r1_only`
  ~1% estimates can now be planned against.
- **Primary pool 26: composite 19, Arm B 4, Arm S 3.** The composite cell, empty this morning, is now
  the chapter's largest.
- **The FDT cell has two members, both Arm S**: the 19th-century US counties study and "Rainfall risk,
  fertility and development: farm settlements during the American frontier" (children as a buffer stock
  of labour against rainfall risk).
- **Arm S is the thinnest arm at 3 primary records.** If that survives the remaining waves its GRADE
  rests on very little and PM may end UNEVALUATED.
- **Wall 1 is load-bearing: 15 records routed to C.3.c**, 19% of `both_channels`, through to the 2022
  AEJ:EP Namibian social-pension study. One flagged to revisit if C.3.c declines it: "Old-age security
  motives, labor markets, and farm family fertility in antebellum America" — FDT-era, Arm S setting.
- **One `REVERSE` record**: "Children as insurance revisited" estimates children -> insurance adoption.
  Direct measured evidence that reverse causality here is real, not merely possible — risk-of-bias
  material, not pool material.
- Bounds: title/abstract only, design values are hypotheses; the 269 were screened on titles so 2.2% is
  a floor; 23% of the universe still has no abstract.

### 2026-09-01 — screen wave 2: all 2,271 `frame_only` records; primary pool now 62

- Log at `credit-constraints-screen-wave2.md`; table at `extraction/credit-constraints-screen.csv`.
  **2,620 screened across three strata, zero validation errors.**
- **The depth probe FAILED on this stratum: predicted ~6%, actual 1.6% primary — a 4x overestimate.**
  It held to two points on `both_channels` (25.0% vs ~23%) and `snowball_r2_only` (2.2% vs ~4%). Cause:
  a 40-record probe cannot measure a 1.6% base rate (expected count 0.6), and the probe counted
  "relevant" loosely while the screen applied the cells strictly. **Rule: where a probe returns 0-2 of
  40, the stratum is UNMEASURED, not low-yield.**
- **Primary pool 26 -> 62** (composite 19->32, Arm S 3->16, Arm B 4->14).
- **Wave 1's "Arm S is the thinnest arm and that is a finding" was PREMATURE** — an artefact of which
  stratum had been screened. Arm S is now the second largest.
- **A third FDT-era Arm S record**: *Savings Behaviour, Fertility and Economic Development in
  Nineteenth Century Britain*, joining the US-counties and American-frontier papers. Two countries,
  two distinct sources of variation.
- **Arm S's exposure vocabulary is "risk", not "credit"** — four new Arm S records come from the Cain
  debate and carry no finance token in the title. This is why the token filter (24/26 recall) could
  not be used as a gate.
- **Two more version pairs inside the primary pool** (bequest-receipt papers; mortgage-interest-subsidy
  papers). Five in the chapter so far; de-dup before extraction is not optional.
- 37 records now route to C.3.c. Flagged to revisit with the antebellum paper: *Bismarck in the
  bedroom? Pension reform and fertility 1870-2010* — FDT-era, long panel.
- Next: `snowball_r1_only` needs a 200+ record probe, not a 40; retrieve and extract the 62; mine the
  three reviews.

### 2026-09-01 — blinded 400-record probe on `snowball_r1_only`

- `295_c3e_blind_probe.py`; log at `credit-constraints-r1-probe-log.md`.
- **4 primary in 400 = 1.00%** (1.50% counting two that need full text). **Projected 38-57 primary in
  the 3,815-record stratum.** Finds include *Risk-sensitive fertility* (direct Arm S) and a
  **cluster-randomised credit-with-health-education trial in Benin** — a randomised credit arm is
  exactly what the composite cell lacks.
- This matches the earlier 40-record estimate, **but that agreement is luck** — the same method
  overestimated `frame_only` fourfold.
- **The sensitivity arm FAILED and the design flaw was mine**: I recorded verdicts only for new
  positives, so the 20 hidden controls cannot be scored, and self-blinding was impossible anyway since
  I had screened those records hours earlier. Prevalence only. A real sensitivity measure needs a
  verdict on every row and a second screener.
- **Data-integrity catch: I hand-typed OpenAlex ids for the verdict file and all eight were wrong.**
  The ingest validation (reject any id not on the sheet) caught every one; three would otherwise have
  vanished and four attached to the wrong records. Never hand-type a record id.
- **Recommendation: screen this stratum LAST**, after the 62-record primary pool is retrieved and
  extracted. 38-57 marginal records will not change whether the arms can be rated; the 62 will.

### 2026-09-01 — primary pool de-duped, retrieved 12/62, first extraction rows

- `296`-`299`; log at `credit-constraints-extraction-wave1.md`; table at
  `extraction/credit-constraints-effects.csv`.
- **Three version pairs; folded-title dedup found ZERO of them.** One pair differs by a single word
  ("Aging Society" vs "Aging Economy"), the other shares no title at all (Jaccard 0.43). `297` uses
  author-gated Jaccard OR author-gated containment, re-found both hand-declared pairs, and **proposed
  a third I had missed** (two Grameen Bank papers, same first author, J=0.875). **62 records -> 59
  distinct studies.**
- **Retrieval 12 of 62.** 36 have no open URL at any rung (Unpaywall spot-check confirms), 9 are
  browser-jobs, 5 proxy-jobs. **Arm S is retrieval-bound at 3 of 16**, and TWO OF THE THREE FDT-era
  Arm S records are unretrieved. This is the B.1 problem again.
- **THE SIGN FLIP IS MEASURED.** *Fertility choice and financial development* (145 countries,
  1980-2006): +1 SD private credit **decreases fertility 1.7-5% in low-income countries and increases
  it 3.7-5% in high-income countries** — exactly the question Ruling 1 rests on. **But it is not
  identified**: aggregate cross-country panel, no instrument for credit, secondary pool per the scope
  memo. All four extracted rows are `identified: NO`.
- The FDT-era Arm S estimate (US counties c.1850): bank presence associated with a child-woman ratio
  ~3pp lower, crude birth rate ~5% lower, OLS cross-section. **Its authors frame it as the
  old-age-security motive — C.3.c's under Wall 1**, so PI Call 1 now has a concrete case attached.
- **`299` written because I hand-typed an OpenAlex id into the extraction table one hour after
  recording the lesson that says never to.** It was wrong and the CSV would not have shown it. The
  script now validates id existence, title agreement, `OUTCOME_LEVEL` against a closed list, and
  `estimator_class` against a closed list.
- Next: extract the remaining 10 retrieved; **the 50-study retrieval handoff is the binding
  constraint** on rating Arm S.

### 2026-09-01 — first full-text check REVERSED a screen decision

- One file arrived from the Tier 1-3 priority list: Lafortune and Lee, *All for One? Family Size and
  Children's Educational Distribution under Credit Constraints* (AER P&P 2014).
- **Re-routed PRIMARY_BORROW_TERMS -> MECHANISM_NO_FERTILITY.** Family size is a **regressor**; the
  dependent variable is children's education, with credit constraints as a moderator. No fertility
  outcome, so Wall 6 routes it out; cross-ref C.3.d.
- **Two corrections, both mine.** (1) The screen cell was wrong in precisely the way the wave-1 log
  warned — design and outcome values are hypotheses until full text — and this is the FIRST of the 62
  checked against its own text. Expect more. (2) My priority note ranked it Tier 1 as a "top-five
  journal, design likely strongest in the arm"; it is **AER Papers & Proceedings, 5 pages**, not a
  refereed AER article. I ranked a venue string, not a paper.
- **Primary pool 62 -> 61** (58 distinct studies). Arm B 14 -> 13.
- **Everything else in Tiers 1-3 is still outstanding.** Unavailable: the 1983 Bangladesh comment and
  **19th-c Britain (Tier 1 #2)** — so the FDT-era Arm S cell stands at **1 of 3 read**, and the
  rainfall-risk paper (`10.1093/jeg/lbz039`) remains the highest-value outstanding item in the chapter.

### 2026-09-01 — the first four Arm S full texts: NONE survived as C.3.e

- Log at `credit-constraints-arm-s-structural-problem.md`. **FOR ANUP; supersedes PI Call 1.**
- Ridker 1980 (No-Birth Bonus) and Ridker 1971 (tea estates) are **one study**, and the scheme pays
  into a savings account **for each year without a birth** — "compensation for the loss incurred in
  forgoing additional children". What varies is the **price of a birth**; the savings account is the
  payment vehicle. → **C.2.d**. (The design is otherwise decent: DiD across 18 estates, Type I CBR
  39.5→25.4 vs Type III 39.2→33.0; the author's own verdict is cautious.)
- Stokes/Schutjer/Bulatao 1986 is about **landholding** → **C.4.a**.
- Cain 1986 is a conceptual reply with no estimate → THEORY, **and it breaks Wall 1**: Cain defines
  insurance broadly, names disability/widowhood/depredation/floods **alongside old age** as one
  concept, and **cites Nugent's old-age-security paper approvingly**. The founding literature treats
  old-age security as ONE INSTANCE of the insurance motive, so Wall 1 cuts on an axis its own sources
  do not have. The 276 probe missed this because it measured VOCABULARY (13.7% old-age words), not
  what the studies vary.
- **Arm S 16 → 12. Primary pool 61 → 57.**
- **Three options for Anup**: (1) merge Arm S into C.3.c; (2) re-cut Wall 1 on the INSTRUMENT (C.3.c =
  old-age provision, C.3.e = general financial instruments) rather than the risk; (3) accept Arm S is
  mostly empty of admissible variation. **I recommend 2 and expect it to deliver 3.**
- Ruling 1 is unaffected — composite exposures still cannot be allocated, so this is still one
  chapter — and Arm B is untouched.
- Caveat: four full texts, chosen as the best cases, so not random — but that cuts against Arm S.
  The ruling can wait for the rainfall-risk paper (`10.1093/jeg/lbz039`), still the highest-value
  outstanding retrieval.

### 2026-09-01 — Wall 1 re-cut on the instrument (option 2). Arm S 12 -> 5.

- **Shravan voted option 2; applied as an RA ruling, PI confirmation from Anup still required** (it
  changes which phenomena are in scope). C.3.c owns old-age PROVISION; C.3.e Arm S owns availability
  of a general financial instrument whatever risk it covers; C.5.a owns risk EXPOSURE with instruments
  fixed; C.4.a land; C.2.d the price of a birth.
- **Applied honestly it routed 7 of 12 out. Arm S 12 -> 5; primary pool 57 -> 50** (B 13, composite 32,
  S 5). This is the outcome-3 I predicted from option 2.
- **It demotes the rainfall paper** (`10.1093/jeg/lbz039`) — the highest-priority outstanding retrieval
  and the only plausibly identified Arm S design — to **C.5.a**, because what varies is rainfall risk,
  not instrument access. Consistency requires it. Still worth retrieving, for C.5.a.
- Arm S survivors: US counties c.1850 (retrieved, extracted; survives BECAUSE bank presence is an
  instrument, though its authors frame it as old-age security), 19th-c Britain (**unavailable**),
  Risk/Consumption Smoothing 1991, Family size and life-cycle saving 1991, Consumption smoothing 2024.
- **Arm S cannot support a GRADE rating at 5 records with 1 read. PM and FDT hang on it** — if it stays
  here the honest verdict is UNEVALUATED + GRADE No evidence. Ruling 1 stands; Arm B and composite
  untouched.
- **Downloads still outstanding:** rainfall `10.1093/jeg/lbz039` (never arrived); credit supply shocks
  `10.1016/j.jbef.2022.100633` (**ScienceDirect Cloudflare block** — the `main.html` file); bequest
  receipt `10.1111/j.1465-7295.2008.00208.x` (**Wiley JS eReader shell**, not a PDF). Two confirmed
  unavailable: 19th-c Britain, 1983 Bangladesh comment.

### 2026-09-01 — Wall 1 re-cut on the instrument (option 2); Arm S 12 -> 6

- **Shravan voted option 2; applied as an RA ruling, PI confirmation from Anup still required** (it
  changes which phenomena are in scope). C.3.c owns old-age PROVISION; C.3.e Arm S owns availability
  of a general financial instrument whatever risk it covers; C.5.a owns risk EXPOSURE with instruments
  fixed; C.4.a land; C.2.d the price of a birth.
- Applied to the 12 remaining Arm S records it routed **7 out** (5 to C.5.a, 1 to C.3.c, 1 to THEORY).
  The outcome-3 I predicted from option 2, and it arrived immediately.
- **Then the rainfall paper arrived and corrected the ruling's first casualty.** I had routed Grimm's
  *Rainfall risk, fertility and development* to C.5.a **on its title**. The full text SPLITS: the
  headline effect (rainfall variance x farm/non-farm differential) is C.5.a's, but **Table 4 cols
  (5)-(6) interact rainfall variability with ACCESS TO FINANCIAL SERVICES (banks per county, banks per
  farm, time-varying)** — which is Arm S's estimand exactly. **Retained in Arm S for that estimate;
  main effect cross-refs C.5.a. Split by estimate, not routed wholesale.**
- **That Arm S estimate is an UNINFORMATIVE null**: negative in sign, "economically small and
  statistically insignificant", and the author says it is "hard to say whether financial services could
  not or were not used ... or whether the available measures ... are simply too crude." Recorded as
  imprecise, NOT as evidence of no effect. Note the contrast in the same table: irrigation and
  machinery interactions DO attenuate the buffer effect.
- **Arm S 12 -> 6; primary pool 57 -> 51** (B 13, composite 32, S 6). Two of the six retrieved and
  extracted, one unavailable, three unread. **Arm S still cannot support a GRADE rating; PM and FDT
  hang on it.** All five extracted rows remain `identified: NO`.
- **Three routings overturned by full text today** — the AER paper (family size a regressor), Ridker
  (savings account a payment vehicle), Grimm (a second estimand hidden in the paper). The error runs
  BOTH ways: full text has removed studies and rescued one the ruling had just discarded.
- **Still outstanding:** credit supply shocks `10.1016/j.jbef.2022.100633` (**ScienceDirect Cloudflare
  block** — the `main.html` file is the failed save); bequest receipt
  `10.1111/j.1465-7295.2008.00208.x` (**Wiley JS eReader shell**, not a PDF). Confirmed unavailable:
  19th-c Britain, 1983 Bangladesh comment.

### 2026-09-01 — last two priority PDFs: one routed out, one is the first identified estimate

- **Bequest receipt (Grawe) routed OUT.** The outcome is **child earnings**, family size is the
  regressor — the identical failure to the AER P&P paper, and both were Arm B records screened on a
  title containing "family size". Wall 6; cross-ref C.3.d. Applies to both members of the version pair.
  **Arm B 13 -> 11.**
- **"Do credit supply shocks affect fertility choices?" is the chapter's FIRST IDENTIFIED ESTIMATE.**
  Two shocks in one paper: US banking deregulation of the 1980s (exogenous state adoption timing) gives
  **+5.4% on the fertility rate**; the Great Recession with a **Bartik IV** on pre-recession bank share
  gives **+9.5 pp on a 7.7 pp base** for the propensity to give birth. One SD of credit = 0.121 SD of
  birth propensity. Stronger for young women and families with unemployed husbands.
- **Sign positive — Arm B's predicted direction — and it corroborates the high-income half of the sign
  flip**: Filoso-Papagni's unidentified panel says +3.7 to +5% for high-income countries; this says
  +5.4%, identified. Two very different designs, same sign and magnitude.
- **The low-income half of the flip still has NO identified support** — only the aggregate panel,
  Desai-Tarozzi's randomised null, and Grimm's imprecise bank interaction. The chapter has an
  identified estimate for the arm it needs least and none for the arm PM/FDT depends on.
- **Primary pool 49** (B 11, composite 32, S 6). Extraction: 7 rows, 5 studies, **2 identified**.

### 2026-09-01 — Arm B browser jobs: 4 listed, 1 dissolved, 1 withdrawn, 2 read

- Log at `credit-constraints-armb-browser-jobs.md`.
- **"The Babies of Financial Deregulation" was never a separate study** — Isaac Hacamo, same
  federal-regulator-ruling design as the delivered SSRN paper and the RFS article. **One study, three
  versions.** Extracted: **+6 pp** on the probability of having a child for fully-exposed young
  households. **Second identified estimate.** Author rejects income and housing-wealth channels and
  points to ACCESS TO SPACE — a C.2.c boundary note.
- **The 2024 mortgage-subsidy posting is WITHDRAWN from SSRN**; the 2026 posting is the version of
  record, published in Academia Economic Papers 54(1) 71-105. Version pair resolved.
- **Ao/Chen/Tseng 2026 is the chapter's FIRST IDENTIFIED NULL** — DiD with matching, Taiwan; first
  stage verified (mortgage burden **-7.9%**, -17.6% outside the priciest cities) but **no effect on
  home purchase or fertility**. An INFORMATIVE null, unlike Grimm's.
- **A candidate reconciliation:** the two positive identified estimates are credit SUPPLY/ACCESS shocks
  (extensive margin — can you borrow); this null is a COST reduction for people already borrowing
  (intensive margin). Access moves fertility; cheapness may not. Test it against the remaining Arm B
  records rather than assuming it.
- **Wang and He 2025**: FE-Poisson + IV on China Family Panel Studies 2018-2022, **inverted-U** effect
  of credit on fertility — a within-setting nonlinearity echoing the cross-setting sign flip, and the
  first time the chapter has that theme from an identified design.
- **Extraction table: 10 rows, 8 studies, 5 identified.** Arm B has 5 estimates, 4 identified, and they
  DISAGREE: two positive access shocks, one null cost reduction, one inverted U. Primary pool 48.
- Both new rows are **abstract-sourced** and on the residual retrieval list; do not pool before the
  full texts are read.

### 2026-09-01 — the hand-sourced stratum was never screened; primary pool 48 -> 69

- Log at `credit-constraints-handsourced-screen.md`.
- **130 hand-sourced records had no cell assignment.** The sheets covered only the three discovery
  strata. Excluded from the pool were **Desai and Tarozzi** (the chapter's only randomised estimate,
  which I had retrieved, scanned and reasoned about all day), Steele, Kuchler, Lan, **Islam et al.**,
  the inherited C.2.c Arm B anchors including **the PNAS provident-fund study C.2.c routed here**, and
  the Arm S anchors (Cain 1981/1983, Portner, Pitt, Delavallade, AGEP).
- **Third time hand-sourced studies have fallen out of an accounting in this chapter** — missing from
  the universe (fixed in 291), absent-by-id when present as twins (fixed in 292), now missing from the
  screen. The rule that catches all three: **reconcile against the hand-sourced list at EVERY stage,
  as a check that fails loudly.**
- **Primary pool 48 -> 69** (B 10->17, composite 32->40, S 6->12). Total screened 2,750.
- **Two genuinely new IDENTIFIED records, both what the search phase was going to hunt for:**
  **Million Baht Village Fund, Thailand** (IV+FE panel, **negative** — the missing identified support
  for the low-income half of the sign flip; caveat: The Mathematics Enthusiast, 0 cites) and
  **Financing Fertility through Bank Competition, China** (deregulation shock, **positive**; caveat:
  Research Square preprint, 0 cites).
- **Seven identified/quasi-identified estimates now, and they disagree.** TWO structures are on the
  table, not one: the cross-setting **sign flip** and the within-setting **inverted U**. Do not blur
  them in synthesis.
- **Orton review mined:** 5 of 56 references carry a fertility term, 3 already in the pool. An
  independent review contains almost nothing we lack — corroboration that the composite cell is
  saturated, from a channel owing nothing to our query.
- **Benin RCT resolved NEGATIVE:** no fertility term in the abstract, and the 2x2 varies credit-product
  FEATURES, not access. Not a C.3.e estimate.

### 2026-09-01 — read everything retrievable; 11 of 69 extracted

- Log at `credit-constraints-read-all-log.md`; script `300_c3e_read_all.py`.
- **"Read all the studies" is bounded by retrieval: 69 primary records, 18 with a verified full text,
  51 without.**
- **A mis-mapping was caught before it corrupted anything.** Reconciling the two PDF folders by fuzzy
  title match **mis-assigned 8 of 10 files** — a PDF named for a record that had been ROUTED OUT fell
  through to "best title match above 0.6" and landed on an unrelated record. Desai and Tarozzi's record
  was handed the No-Birth-Bonus PDF. Caught because the candidate sentences read wrong; no extraction
  row was written from a bad pairing. The map is now filename-is-an-id or the handoff CSV's explicit
  map, **no fuzzy fallback**, each re-verified against the PDF's first page.
- **Desai and Tarozzi had never been extracted** — retrieved this morning, quoted in four write-ups as
  the centrepiece, no row. Now two rows: realized births **-0.106 to -0.166** (small, some significant)
  and desired family size **+0.38 to +0.40** (5%). Context: fertility ROSE in the study area over the
  period (TFR 5.5->6.0), which is a time trend, NOT a treatment effect.
- Also extracted: **Kuchler 2012** (recent fertility -0.14, t=-1.54, ns) and **Lan et al. 2023**
  (+0.136% fertility INTENTIONS per 1% digital financial inclusion).
- **Extraction table: 14 rows, 11 studies, 7 identified; outcome levels 12 realized / 1 desired /
  1 intention.** The pattern is now visible in the table: **every positive result sits on desires or
  intentions, and every realized-fertility result in a low- or middle-income setting is null or
  negative.** The realized positives are all high-income Arm B credit-access shocks.
- **12 retrieved texts returned zero candidate sentences** — a method limit, not a finding: pdftotext
  shreds two-column layouts and these estimates live in TABLES. They need hand reading.
- **Honest state: 11 of 69 extracted (16%).** A synthesis today would report on a sixth of the pool.

### 2026-09-01 — every retrievable text read; 12 screen cells overturned

- **All primary records with a verified full text have now been read.** Extraction table **18 rows,
  14 studies, 7 identified** (15 realized / 2 desired / 1 intention).
- **Twelve screen cells overturned by reading the paper: eleven removals, one rescue.** Primary pool
  **69 -> 65** (B 14, composite 40, S 11).
- **Four of the eleven removals are the SAME failure: fertility or family size on the right-hand
  side.** The AER P&P paper, Grawe (both versions), and the credit-constraints/continuing-education
  paper all regress a non-fertility outcome on family size or childbearing.
  **Screening rule to add:** a title naming family size or childbearing ALONGSIDE a second
  non-fertility noun is a warning, not a match — the second noun is usually the dependent variable.
- Other removals: an OLG theory model; a reversed-arrow paper (pill -> fertility -> cohort size ->
  interest rates and house prices); an Indonesian survey whose exposures are transfer expectations and
  a pension scheme (C.3.c) with an uninformative pension null (no pension exists for those households).
- **Implication for the 51 unread primary records: where screen cells have been tested they failed
  about two-thirds of the time, almost always by removal. The current arm counts are an UPPER BOUND,
  and no synthesis should rest on screen cells alone.**
- New table extractions: **Suriani et al. 2021** (developed AND developing both NEGATIVE, developing
  larger — contradicts the Filoso-Papagni sign flip), **Karim et al. 2016** (NGO membership proxy,
  positive only after 2007, tiny), **Steele et al. 1998** (fertility DESIRES, authors' own reading is
  no significant effect; severe self-selection, joiners more likely to have used contraception before
  joining).

### 2026-09-01 — stages 8-11 run on the texts in hand (22% of the pool)

- `301` poolability, `302` risk of bias, `303` demsig + GRADE; synthesis at
  `credit-constraints-interim-synthesis.md`. **Not a chapter draft — see below.**
- **Stage 9: NO META-ANALYSIS. Not one stratum qualifies.** A naive pool would have "qualified" on 14
  studies; stratified by arm x outcome-level x estimator, every cell fails on study count or estimator
  heterogeneity. Narrative synthesis.
- **Stage 8: risk of bias — LOW 1, MODERATE 5, SERIOUS 6, CRITICAL 2.** D1 selection fails hardest
  (Steele's joiners were more likely to have used contraception BEFORE joining). D5 first-stage-verified
  separates the informative null (Ao, burden -7.9%) from the uninformative one (Grimm, measures "too
  crude").
- **Stage 10: every cell NOT ASSESSED on the arithmetic** (no fertility panel in the repo; C.2.c's
  precedent). **But slope sufficiency answers the prior question and it is decisive:** over the SDT the
  exposure EXPANDED (private credit/GDP 0.39->1.14 high-income, 0.13->0.31 LDC) and every identified
  estimate says expansion RAISES fertility. **A mechanism whose exposure moved the way that raises
  fertility cannot explain a fertility decline.** For the SDT, Arm B is an OFFSET, not a cause. The
  composite cell is CONTESTED AT THE SIGN (Filoso-Papagni +3.7 to +5% vs Suriani negative throughout).
- **Stage 11 GRADE (single rater; protocol needs three):** PM — S No evidence / B n/a / composite No
  evidence. FDT — S Very low / B No evidence / composite No evidence. SDT — S No evidence /
  **B Moderate** (four identified designs, downgraded once for indirectness) / composite Very low.
- **THE RESULT: C.3.e's best-identified evidence does not support C.3.e as an explanation of fertility
  decline — it supports the opposite.** The registry's PM/FDT configuration has no read evidence at all.
- **§6 chapter draft deliberately NOT written.** 22% of the pool read; where screen cells were tested
  they failed ~2/3 of the time; arm counts are an upper bound. Three things would move the verdict:
  Arm S retrieval (9 unread), the two weak-venue identified sign-relevant studies, and Anup's Wall 1
  ruling.

### 2026-09-01 — chapter drafted at `output/chapters/credit-constraints.md`

- **Drafted at Shravan's instruction after I advised against it**; the objection is recorded in the
  chapter's Provenance block as the template requires.
- Conforms to `docs/chapter-template.md`: S1-S7 present and in place, sections 1-12 in order, plain
  terms before technical in §1 and §7, S4 before arithmetic in §8, no analogy, verdict standalone.
- **Verdict: credit constraints are NOT an explanation of fertility decline; on the best evidence they
  worked against it.** Carry-away number **+5.4%** (US banking deregulation on the fertility rate),
  with the SIGN being the point. Two qualifications in the same breath: cheaper credit is not more
  credit (Taiwan null, first stage verified), and the poor-country half of the hypothesis is
  UNEVALUATED rather than refuted.
- GRADE: SDT/Arm B **Moderate** (downgraded for indirectness); FDT/Arm S Very low; everything else
  **No evidence**. Demsig: NOT ASSESSED in all nine cells on the arithmetic, with the SDT cell
  foreclosed by the sign rather than by the missing denominator.
- Stage 11 marked **partial**: one rater, protocol requires three.
- §11 records the two PI calls (the Wall 1 re-cut applied on RA authority; whether the US-counties
  study stays given its authors attribute it to C.3.c) and names the largest gap in the literature:
  **of ten microcredit RCTs read in full, not one estimates a fertility outcome anywhere in its text.**

