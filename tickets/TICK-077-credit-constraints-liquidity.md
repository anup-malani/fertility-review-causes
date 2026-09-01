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
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
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

