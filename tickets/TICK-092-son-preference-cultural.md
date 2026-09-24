# TICK-092: D.2.c Son Preference and Gender-Biased Fertility Norms
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `son-preference-cultural` — HYPOTHESES-v5.md §D.2.c
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/son-preference-cultural-*, extraction/son-preference-cultural-*, output/chapters/son-preference-cultural.md

<!-- No ## Description. The slug above is the specification (HYPOTHESES-v5.md §D.2.c). -->

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/son-preference-cultural-search-scope.md`
- [x] 3. Literature search and AI screening, both phases (§5.1) — frame probe + completeness test (89), cold-start anchors (90), citation frame (91), production frame (92), blinded Haiku screen 101 batches (93–96; batch 48 on Sonnet). RELEVANT 1,509 / UNCERTAIN 771 / NOT_RELEVANT 1,755; pooling set 1,047 (identified core 380)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/son-preference-cultural.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-24 — opened; Stage 2 (search strategy and scope) drafted; Stage 3 frame probe + completeness test run.**

*Selection context.* Picked by RA (Shravan) as the smallest genuinely-unstarted hypothesis. A.14/TICK-091
took the previous smallest slot; every other "Open" hypothesis row on the board (A.3/088, A.6/087,
C.2.f/081, C.3.d/083, C.3.f/086, A.9/089, C.2.h/090) already carries drafted branch work through ~stage 12
— the recurring stale-board problem. D.2.c has no branch, no chapter, and no prior ticket. TICK-091's scout
(`88_a14_candidate_scout.py`) had only ranked the biological/proximate un-started set; the un-ticketed
**cultural/demographic** candidates were never measured. An extended scout on the same fertility outcome
axis (reused `count()`; anchors reproduced: B.2=4,475 exact) ranked them: **D.2.c = 1,134**, D.1.d
nationalist/pronatalist 1,720, A.20 cultural-diffusion 1,968, A.19 intergenerational-transmission 2,414,
B.2 endocrine 4,475, A.13 breastfeeding 5,079. D.2.c is the smallest of the whole un-ticketed field and
the only clear candidate below the ~1,808 "smallest" bar besides D.1.d. The big canonical un-ticketed
literatures (child mortality, contraceptive tech, abortion, family planning, marriage timing, female
wage, income effect, urbanization, female empowerment) were excluded on sight.

*Stage 2 deliverable* at `literature/search-logs/son-preference-cultural-search-scope.md`. It states
D.2.c's single parameter (son preference → sex-composition-conditional continuation (differential
stopping) → fertility, holding the sex-indifferent desired number fixed, and its attenuation by
sex-selective abortion where available), the three evidence streams (differential stopping / parity
progression by sibling sex composition; the sex-selection substitution regime where fertility falls and
the sex ratio at birth rises; cross-population norm-intensity variation), **six** boundary walls (A.10
adult sex ratio / marriage market — the load-bearing "sex ratio" wall; A.4/A.2 general abortion; A.8
sex-indifferent parity stopping; C.3.c old-age security as the economic root; D.2.a general gender equity;
A.1 child mortality / replacement), a 14-row estimand-cell table with routing, three conjoined query
blocks, eligibility rules, and the reverse-causality / substitution-confound / mortality-confound /
external-validity cautions. Per the A.6/A.3 lesson it carries a **registered-construct completeness
check**. D.2.c spans **PM/FDT/SDT** (natural-fertility differential stopping in PM/early-FDT high-fertility
settings; sex-selection substitution in FDT/SDT South and East Asia).

*Stage 3 frame probe* (`source/build/goldset/89_d2c_frame_probe.py`, mirrors 89_a14/52/405) → 41 OpenAlex
counting requests, 0 refusals → `literature/search-logs/d2c-frame-probe-2026-09-24.{json,md}`.

**The probe confirms the "smallest" prior.** Control housing (a written chapter) reproduced at 170 (405
got 205, 52 got 181, A.14 got 170), so the counter is sound. D.2.c's honest **production frame = 1,696**
(narrow-clean 994), at the ~1,808 bar — the smallest available un-ticketed candidate, in the C.2.h
"deliberate pick" regime rather than an order of magnitude below the bar like A.14 (769).

**The completeness test passes.** Every registered D.2.c construct is representable with a modest honest
gain: sex composition +358, sex ratio at birth +354 (the substitution-expression outcome), male preference
+134, stopping behavior +31/+15. The large gainers are exactly the free-`OR` inflaters the test exists to
catch and are NOT folded in: `sex ratio` +7,595 (annexes A.10's adult-sex-ratio marriage literature),
`preference` +10,667, `gender` +20,362, `son` +5,326 (surnames). Two borderline terms — `prenatal
diagnosis` +977 and `amniocentesis` +481 — broaden into general prenatal-screening/genetics; the genuine
sex-selection substitution studies are already caught by "sex-selective abortion" / "sex selection" /
"prenatal sex selection", so these are channel-adjacent and left out. Honest frame growth adds only the
clean constructs (sex composition, sex ratio at birth, male preference, stopping behavior/behaviour).

**Walls all thin and cleanly routable** (overlap / neighbour / overlap-AND-identified): **A.10 the
load-bearing "sex ratio" wall 45 / 667 / 1** (2.7% of frame, one identified overlap — the frame's
son-preference topic terms keep the adult-sex-ratio marriage literature out cleanly), A.8 parity stopping
123 / 5,688 / 4, C.3.c old-age security 44 / 3,060 / 1, D.2.a gender equity 111 / 3,256 / 10, A.1 child
mortality 139 / 6,895 / 9. The one **thick** boundary is **A.4/A.2 521 / 39,521 / 14** — expected, because
sex-selective abortion is genuinely D.2.c's substitution stream and shares "abortion"/"family planning"
vocabulary; the identified overlap is only 14 and the discriminator (sex-*selective* vs general access)
resolves at full-text. **Homonyms negligible inside the frame** (son-as-name 6, sex/gender biology 53,
preference-economics 2), so no homonym scrub is needed on the core vocabulary. Frame carries **64
identified-design markers (3.8%)** — a thin-but-real quasi-experimental core (differential-stopping
designs off the near-random sex of early births; ultrasound/amniocentesis-diffusion event studies),
larger in share than A.14's 2.2%.

*Decision.* D.2.c is confirmed the smallest available genuinely-unstarted hypothesis; the selection is
supported, not a deviation. Scope is clean, the load-bearing A.10 wall is clean, the A.4/A.2 substitution
boundary is thick-but-routable, and the frame is honestly built.

*Budget.* 41 of today's ~100-request OpenAlex allowance used on the probe; all cached
(`temp/d2c-frame-probe-cache.json`), resumable.

*Next — the budget-heavy Stage-3 remainder (paused for RA checkpoint, per the C.2.h/A.14 precedent).*
Build cold-start anchors + existence-verify (mirror 90_a14; seeds: Ben-Porath & Welch 1976, Das Gupta
1987, Arnold Choe & Roy 1998, Clark 2000, Jayachandran 2017, plus the substitution naturals — Chung & Das
Gupta 2007, Ebenstein 2010, Lin Liu & Qian 2014, and wall decoys → A.10/A.4/A.8/C.3.c/D.2.a/A.1), then the
Tier-A/B citation frame merged with the production keyword frame (add the clean completeness-test gainers:
sex composition, sex ratio at birth, male preference, stopping behavior/behaviour), then the blinded Haiku
title/abstract screen. No LLM screen budget spent yet.

**2026-09-24 — Stage 3 completed: cold-start anchors, citation + production frames, blinded screen, assembly.**

*Anchors (90).* 14 existence-verified via Crossref (11 verified, 3 version-drift, all identity_verified):
the differential-stopping core (Ben-Porath & Welch 1976, Clark 2000, Arnold-Choe-Roy 1998), the
sex-selection substitution naturals (Ebenstein 2010, Lin-Liu-Qian 2014, Jayachandran 2017 → resolved to
its NBER w20272 preprint, the drift), the norm-intensity trend (Chung & Das Gupta 2007), the son-preference
norm canon (Das Gupta 1987), and 6 wall decoys (Angrist 2002 → A.10, Pop-Eleches 2006 → A.4, Knodel 1987 →
A.8, Nugent 1985 → C.3.c, Jejeebhoy 1995 → D.2.a, Preston 1978 → A.1).

*Citation frame (91).* All 14 anchors resolved to their OpenAlex VoR; forward-seeded the empirical core only
(differential-stopping / substitution / norm-intensity), theory + decoys backward-only. Tier B = 1,948
(1,652 forward, 296 backward; 1,298 abstracts).

*Production frame (92).* Recall block = the scope vocabulary + the clean completeness-test gainers ("sex
composition", "sex ratio at birth", "male preference", "stopping behavior/behaviour"); the free-OR inflaters
("sex ratio", "preference", "gender", "son") DROPPED. Outcome axis added the substitution-expression outcome
"sex ratio at birth" so pure sex-selection papers are caught. Keyword frame 2,490; **merged screen frame
4,035** (403 in both channels; 3,040 abstracts).

*Screen (93–96).* 101 batches, blinded {id,title,year,abstract}, Haiku (`claude-haiku-4-5`), resumable /
fail-closed. Haiku's known row-drop failure recurred on batches 8/32/42/48 ("expected 40, got N"); handled
by re-running with more retries; batch 48 (stubborn) re-screened on `claude-sonnet-5`. Validator: 101 valid /
0 missing / 0 bad. **RELEVANT 1,509 / UNCERTAIN 771 / NOT_RELEVANT 1,755.**

*Pooling set = RELEVANT ∩ PRIMARY ∩ non-review/theory = **1,047*** (identified core — natural-experiment or
revealed-stopping — **380**; associational 667). By cell: differential stopping 471, sex-selection
substitution 291, norm intensity 285. Walls absorbed cleanly and correctly: OFF_OUTCOME 340 (son preference
→ excess female mortality / child health / schooling — routed out), OFF_ADULT_SEX_RATIO 44 (A.10),
OFF_ABORTION_GENERAL 33 (A.4), OFF_GENDER_EQUITY 32 (D.2.a), OFF_PARITY_STOPPING 24 (A.8),
OFF_OLD_AGE_SECURITY 24 (C.3.c), OFF_CHILD_MORTALITY 7 (A.1), REVERSE 12, OFF_OTHER 148. Theory/mechanism
stream 360.

*Scale note.* This pool (1,047) and identified core (380) are an order of magnitude larger than the recent
SDT-only chapters and larger than A.14 (307). D.2.c spans PM/FDT/SDT and has a 50-year South/East-Asian
demographic-economics literature. Full extraction of the identified core is a scaling task; the chapter will
be drafted on a curated identified core spanning all three primary cells and all three phenomena, with the
residual flagged as an RA extraction backlog (the A.14/B.1 precedent).

*Next — Stage 5 retrieval → Stage 7 extraction of a curated identified core.*
