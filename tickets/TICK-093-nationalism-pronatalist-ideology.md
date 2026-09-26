# TICK-093: D.1.d Nationalist and Pronatalist Ideology
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `nationalism-pronatalist-ideology` — HYPOTHESES-v5.md §D.1.d
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/nationalism-pronatalist-ideology-*, extraction/nationalism-pronatalist-ideology-*, output/chapters/nationalism-pronatalist-ideology.md

<!-- No ## Description. The slug above is the specification (HYPOTHESES-v5.md §D.1.d). -->

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/nationalism-pronatalist-ideology-search-scope.md`
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/nationalism-pronatalist-ideology.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-26 — opened and claimed; Stage 2 (search strategy and scope) drafted.**

*Selection context.* Picked as the next-smallest genuinely-unstarted hypothesis. The QUEUE's "Open" board
is stale — every hypothesis row on it (091, 090, 089, 088, 087, 086, 083, 081) already carries a
complete-but-unmerged branch through ~stage 12, including A.14/091 and D.2.c/092 which are done. Of the
non-deprecated slugs, the genuinely-unstarted set is dominated by the big canonical literatures excluded on
sight (child mortality, abortion, family planning, income effect, female wage, urbanization, female
empowerment, marriage timing). Among the small scouted candidates, TICK-092's extended cultural/demographic
scout ranked D.1.d next after D.2.c (now done) at a production frame of **1,720** — below the ~1,808
"smallest" bar (next A.20 1,968, A.19 2,414, B.2 4,475). Per the user (2026-09-26) the fresh cross-field
candidate scout was **skipped** and D.1.d taken directly on that prior. **Caveat carried into stage 3:** the
scout was partitioned (biological-only on 091, cultural/demographic-only on 092) and never measured the
economic C-section candidates (C.2.d tax-transfer, C.2.a childcare, C.6.b dynastic altruism) against D.1.d,
so the "smallest" claim is a prior to be hardened by the stage-3 frame probe, not a settled measurement.

*Stage 2 deliverable* at `literature/search-logs/nationalism-pronatalist-ideology-search-scope.md`. It
states D.1.d's single parameter (state-sponsored nationalist/pronatalist **ideology** → fertility via
patriotic-duty framing, holding fixed the accompanying transfers and any coercive fertility-control
restriction, and distinguishing a durable quantum shift from a transient tempo response), the three
evidence streams (campaign/propaganda exposure with transfers fixed; cross-national rhetoric-intensity
net of policy; individual patriotic-duty framing incl. experiments), **six** boundary walls — the two
load-bearing ones being **C.2.d** (the transfers the ideology is bundled with) and **A.4/A.2** (regimes
that raised fertility by *banning* abortion/contraception, e.g. Romania 1966, not by persuasion) — plus
D.1.a (secularization), religiosity, A.20 (diffusion channel), and the state's motives. A 15-row
estimand-cell table adds two explicit bundled-treatment cells (`MIXED_IDEOLOGY_TRANSFER`,
`MIXED_IDEOLOGY_COERCION`) read as upper bounds, and a load-bearing **REVERSE** cell (fertility decline
*causes* pronatalist politics — a sign-flipping confound unusually strong here). Three conjoined query
blocks, eligibility rules, and five identification cautions. Per the A.6/A.3 lesson it carries a
**registered-construct completeness check**; two catch-all homonyms are singled out for conjoined-only
entry — `national*` ("national fertility rate" = a country's TFR; nationality) and `population policy`
(sweeps in C.2.d transfers and A.4 bans). Phenomena: **FDT/SDT only** (no PM — organized
nationalist-pronatalism is a modern-state phenomenon): interwar/mid-century authoritarian natalism in the
FDT, contemporary "demographic nationalism" in the SDT.

*Next — the budget-heavy Stage 3 (paused here for the RA/PI checkpoint, per the C.2.h/A.14/D.2.c
precedent of pausing before OpenAlex spend).* Stage 3 needs the frame-probe infrastructure
(`count()` helper, `89_*_frame_probe.py`, the anchor/citation-frame scripts), which lives on the unmerged
recent branches (092), **not on `main`** — the merge debt bites here. First step of stage 3 is to port
that infrastructure onto this branch, then run the frame probe + registered-construct completeness test to
harden the "smallest" prior (particular attention to the `national*` and `population policy` homonyms and
the C.2.d/A.4 wall bleed), before any LLM screen budget is spent.

**2026-09-26 — Stage 3 (part 1): frame probe run; the "smallest" prior holds at 1,751.**

*Infra port.* The shared `count()` machinery (`source/lib/openalex.py`, `textnorm.py`) turned out to be
already on `main` — only the probe script needed writing. Added `source/build/goldset/89_d1d_frame_probe.py`
(mirrors `89_d2c`/`89_a14`/405): control-housing counter check, narrow/production frame, registered-construct
completeness test, six walls read from both sides, homonym readings inside the frame. 41 OpenAlex counting
requests + ~16 decomposition requests, 0 refusals, all cached (`temp/d1d-frame-probe-cache.json`, resumable).

*Result — the prior is confirmed, after one leak fix.* The **first** run reported a production frame of
**4,374**, well above the ~1,808 bar — a red flag. Decomposition traced the whole excess to bare
**`natalism`** (2,677 AND-fertility, 22% of it leaking into the perinatal medical literature —
neonatal/prenatal/postnatal — via `natal` stemming) and to **`pro-natal`** (redundant: the hyphen folds to
`pronatalism`). Dropping both (and keeping `natalist`, which is clean at 2 medical overlaps) gives the honest
**production frame = 1,751** — at/just below the ~1,808 bar and matching TICK-092's 1,720 scout. The
medical-natal homonym inside the frame fell 530 → 12. Control housing reproduced at 166 (405/52/89_d2c got
205/181/170), so the counter is sound.

*Completeness test passes.* Every genuine registered construct adds ~0 to the frame (patriotic duty +4,
national duty +6, duty to the nation +2, population campaign +1, motherhood medal 0, mother heroine +2,
population politics +54) — they are already covered or vanishingly small. The large gains are all the
free-`OR` inflaters the test exists to catch, and are NOT folded in: `national` +38,040, `population policy`
+2,339, `natalism` +2,623 (the medical leak), `propaganda` +304, `nationalism` +283, `nationalist` +247,
`patriotism` +67. So the honest frame is genuinely a pronatalist-ideology frame, not an annexed neighbour.

*Walls (overlap with our frame / neighbour frame / identified-overlap).* **C.2.d 117 / 1,733 / 4**
(6.7% of frame — thin; the transfers are a distinct literature that the ideology frame does not annex),
**A.4/A.2 360 / 39,417 / 3** (21% of frame — the one thick boundary, expected: abortion bans genuinely
entangle with the coercive-pronatalism episodes, but only 3 identified overlaps and the persuasion-vs-
prohibition discriminator resolves them at full text), D.1.a 24 / 724 / 0, religiosity 192 / 11,233 / 3
(religious pronatalism brushes the frame; routable), A.20 35 / 3,715 / 0, C.3.c 37 / 3,015 / 0. Frame carries
**37 identified-design markers (2.1%)** — a thin-but-real quasi-experimental core, comparable to A.14's 2.2%.

*Decision.* D.1.d is confirmed the next-smallest genuinely-unstarted candidate on the hardened frame; the
selection is supported. Scope is clean, the two load-bearing walls (C.2.d transfers, A.4/A.2 coercion)
behave as the scope predicted, and the frame is honestly built. Artifacts:
`literature/search-logs/d1d-frame-probe-2026-09-26.{json,md}`.

*Budget.* ~57 of today's ~100-request OpenAlex allowance used; all cached.

*Next — the budget-heavy Stage-3 remainder (PAUSED for RA/PI checkpoint, per the C.2.h/A.14/D.2.c
precedent).* Build cold-start anchors + existence-verify (mirror `90_d2c`; seeds from the registry —
Demeny 1986, Gauthier 1996, Quine 1996, King 1998 — plus the natural-experiment naturals for the two
load-bearing walls: Romania Decree 770 / Pop-Eleches 2006 as the A.4-coercion decoy, and the C.2.d
transfer canon — Milligan 2005, Cohen-Dehejia-Romanov 2013 — as the transfer decoy), then the Tier-A/B
citation frame merged with the production keyword frame, then the blinded Haiku title/abstract screen. No
LLM screen budget spent yet.
