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
