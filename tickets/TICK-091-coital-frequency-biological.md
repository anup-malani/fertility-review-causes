# TICK-091: A.14 Coital Frequency and Fecundability
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `coital-frequency-biological` — HYPOTHESES-v5.md §A.14
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/coital-frequency-biological-*, extraction/coital-frequency-biological-*, output/chapters/coital-frequency-biological.md

<!-- No ## Description. The slug above is the specification (HYPOTHESES-v5.md §A.14). -->

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/coital-frequency-biological-search-scope.md`
- [x] 3. Literature search and AI screening, both phases (§5.1) — frame probe + completeness test (89), cold-start anchors (90), citation frame (91), production frame (92), blinded Haiku screen 76 batches (93–95), assembled (96). RELEVANT 565 / UNCERTAIN 525 / NOT_RELEVANT 1,945; pooling set 307 (identified core 139)
- [ ] 4. RA title/abstract review
- [~] 5. Full-text retrieval — automated OA pass run (97); RA proxy/ILL handoff for the closed remainder
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/coital-frequency-biological.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-23 — opened; Stage 2 (search strategy and scope) drafted; Stage 3 frame probe + completeness test run.**

*Selection context.* Picked by RA (Shravan) as the smallest genuinely-unstarted hypothesis. An audit
of the board found every "Open" hypothesis row (A.3/088, A.6/087, C.2.f/081, C.3.d/083, C.3.f/086,
A.9/089, C.2.h/090) already carries drafted branch work through ~stage 12 — the recurring stale-board
problem. A.14 has no branch, no chapter, and no prior ticket. A cheap 7-candidate scouting count
(`source/build/goldset/88_a14_candidate_scout.py`, production frame = topic AND fertility/fecundity)
ranked the genuinely-unstarted small candidates: **A.14 = 373**, B.2 endocrine 4,475, A.13 breastfeeding 5,078, B.3
infectious disease 9,442, A.15 maternal-age 15,325, B.4 obesity 21,710, A.16 paternal-age 25,214.
A.14 is an order of magnitude below the field and below the ~1,808 "smallest" bar. D.3.a (anxiety
epidemic) was excluded on sight as a very large literature.

*Stage 2 deliverable* at `literature/search-logs/coital-frequency-biological-search-scope.md`. It
states A.14's single parameter (the coital-frequency → fecundability → births identity, holding
contraception/union/sterility fixed), the two evidence streams (biometric fecundability studies;
exogenous frequency shocks — spousal separation from migration/war/incarceration, and ritual/post-
partum abstinence windows), **six** boundary walls placing A.14 as the exposure gate among the
Bongaarts proximate determinants (vs Cc/Ca contraception A.2–A.6, Cm marriage A.7/C.7, Ci lactation
A.13, fecundity capacity A.15/A.16/B.3, its upstream causes C.2.h/B.7, and fetal loss B.5), an
estimand-cell table with routing, three conjoined query blocks, eligibility rules, and the reverse-
causality / age-confound / Bongaarts-decomposition identification cautions. Per the A.6/A.3 lesson it
carries a **registered-construct completeness check**. A.14 spans **PM/FDT/SDT** (unlike the SDT-only
biological chapters), because coital exposure operates in every fertility regime.

*Stage 3 frame probe* (`source/build/goldset/89_a14_frame_probe.py`, mirrors 52/405) → 55 OpenAlex
counting requests, 0 refusals → `literature/search-logs/a14-frame-probe-2026-09-23.{json,md}`.

**The probe confirms the "smallest" prior — cleanly.** Control housing (a written chapter) reproduced
at 170 (405 got 205, 52 got 181), so the counter is sound. A.14's **honestly-built production frame =
769** (narrow-clean 336), below the 1,808 bar and comparable to A.3's 719.

**The completeness test passes** (unlike A.6, which had omitted its own registered construct). Every
registered A.14 construct is representable. The one genuine under-build is the clean synonym **"coitus"
(+685 → ~1,454, still below the bar)**, which will be added to the recall query block — honest frame
growth. The large gainers are exactly the free-`OR` inflaters the test exists to catch and are NOT
folded in: `activity` +54,806, `desire` +18k, `migration` +14k, `separation` +3,310. The two
borderline synonyms `sexual intercourse` (+1,719) and `libido` (+1,268) broaden into the
contraception / adolescent-fertility / sexual-medicine literature that the **walls route away** — this
is channel-annexation, not a missing construct, so folding them into the frame would inflate it with
off-cell material. Net: the honest A.14 frame is 769–1,454, the smallest genuinely-unstarted candidate
and a *stronger* smallest claim than C.2.h (which sat at/above the bar and was taken as a deliberate
pick).

**Walls all thin and cleanly routable** (overlap / neighbour / overlap-AND-identified): contraception
A.2–A.6 **329 / 37,396 / 4** (the load-bearing "independent of contraception" wall — huge neighbour,
tiny overlap), marriage A.7/C.7 47 / 4,616 / 0, lactation A.13 97 / 3,795 / 0, fecundity-capacity
A.15/A.16/B.3 92 / 19,328 / 4 (the age confound — small overlap), upstream causes C.2.h/B.7 5 / 2,310 /
2, fetal loss B.5 48 / 17,729 / 0. **Homonyms are negligible inside the frame** (separation 0, activity
10, migration 0, frequency 3), so the precise topic terms are clean — no homonym scrub needed on the
core vocabulary. Frame carries **17 identified-design markers (2.2%)** — a thin-but-real potential
core (A.3-shaped); the biometric fecundability stream won't carry IV/DiD markers, so the true
quasi-experimental core is these 17 plus the prospective-diary biometric studies.

*Decision.* A.14 is confirmed the smallest genuinely-unstarted hypothesis; the selection is supported,
not a deviation. Scope is clean, walls are thin, the frame is honestly built.

*Budget.* ~55 of today's ~100-request OpenAlex allowance used on the probe; all cached
(`temp/a14-frame-probe-cache.json`), resumable.

*Next — the budget-heavy Stage-3 remainder (paused for RA checkpoint, per the C.2.h precedent).* Build
cold-start anchors + existence-verify (mirror 53/89; seeds: Bongaarts 1978, Wood 1989, Davis & Blake
1956, Barrett & Marshall 1969, Wilcox et al., plus separation-shock naturals — war-mobilisation and
labour-migration fertility studies), then the Tier-A/B citation frame (mirror 54) merged with the
production keyword frame (add "coitus"/"sexual intercourse" to the block), then the blinded Haiku
title/abstract screen (mirror 56–59). No LLM screen budget spent yet.

**2026-09-23 — Stage 3 completed: cold-start anchors, citation + production frames, blinded screen, assembly.**

*Anchors (90).* 13 existence-verified via Crossref (Jaccard ≥ 0.72 AND year ±1): the biometric core
(Barrett–Marshall 1969, Wilcox 1995), the separation/abstinence naturals (Caldwell & Caldwell 1977
Yoruba post-partum abstinence, Lindstrom–Saucedo 2002 Mexican migration), the sex-recession trend
(Twenge 2017, Ueda 2020), the proximate-determinant canon (Bongaarts 1978, Davis & Blake 1956, Wood
1989), and 5 wall decoys (Bailey→A.2-A.6, Hajnal→A.7, Kennedy→A.13, Menken→A.15, Wilcox 1988→B.5). Menken
"Age and Infertility" pinned via a live author-qualified Crossref lookup (3-word title too generic for
the bibliographic ranker); the biometric methods paper I mis-titled was dropped; Wood 1989 correctly
`expected_no_doi`. doi.org second re-affirm is best-effort and blocked (403) here — Crossref is the gate.

*Citation frame (91).* All 13 anchors resolved to their OpenAlex VoR; forward-seeded the empirical core
only (biometric/separation/abstinence/frequency-trend), theory + decoys backward-only. Tier B = 1,632
(1,330 forward, 302 backward; 1,067 abstracts).

*Production frame (92).* Recall block = the precise A.14 vocabulary + the clean synonym "coitus", with
"sexual intercourse" / "sexual activity" / "libido" / "sexual desire" DROPPED per the completeness test
(their probe gains are dominated by contraception / adolescent-sexuality / STI / sexual-medicine
literature the walls route away; the frequency-focused genuine studies are caught by "frequency of
intercourse" + "coital frequency" + "coitus"). Keyword frame 1,462; **merged screen frame 3,035** (59
in both channels — nearly disjoint, so both were load-bearing for recall).

*Screen (93–96).* 76 batches, blinded {id,title,year,abstract}, Haiku (`claude-haiku-4-5`), resumable /
fail-closed. Haiku's known row-drop failure mode recurred on the harder batches ("expected 40, got 36");
handled by re-running with more retries and re-screening one stubborn batch (46) on `claude-sonnet-5`.
Validator: 76 valid / 0 missing / 0 bad. **RELEVANT 565 / UNCERTAIN 525 / NOT_RELEVANT 1,945.**

*Pooling set = RELEVANT ∩ PRIMARY ∩ non-review/theory = **307*** (identified core — frequency-shock or
prospective — **139**; associational 168). By cell: biometric 129, abstinence 97, separation 44,
frequency-decline 37. **Recall held:** the top identified core by citation is Barrett–Marshall (the
anchor), the day-specific conception-probability biometric literature, Lindstrom–Saucedo (separation),
Caldwell's rural-South-India abstinence study, and "Fecundability, coital frequency and the viability of
ova." Walls absorbed heavily and cleanly (OFF_CONTRACEPTION 404, OFF_FECUNDITY_CAPACITY 206, OFF_OUTCOME
210, OFF_OTHER 307, OFF_UNION_FORMATION 59, OFF_LACTATION 30, OFF_FETAL_LOSS 32). Theory/mechanism
stream 304.

*Scale note.* This pool (307) is an order of magnitude larger than the recent SDT-only biological
chapters (C.2.h pooled 25). A.14 spans PM/FDT/SDT and has a 50-year biometric + natural-fertility +
historical-demography literature. Full extraction of 307 is a scaling task; the chapter will be drafted
on a curated identified core spanning all four primary cells and all three phenomena, with the residual
flagged as an RA extraction backlog (the B.1 precedent).

*Next — Stage 5 retrieval (running) → Stage 7 extraction of the identified core.*
