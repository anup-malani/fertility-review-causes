# TICK-090: C.2.h Digital Leisure Substitution
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `digital-leisure-substitution` — HYPOTHESES-v5.md §C.2.h
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/digital-leisure-substitution-*, extraction/digital-leisure-substitution-*, output/chapters/digital-leisure-substitution.md

<!-- No ## Description. The slug above is the specification (HYPOTHESES-v5.md §C.2.h). -->

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/digital-leisure-substitution-search-scope.md`
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/digital-leisure-substitution.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-21 — opened and Stage 2 (search strategy and scope) drafted.**

*Selection context.* Picked by RA (Shravan) as the smallest *genuinely-unstarted* hypothesis after an
audit found every "Open" hypothesis row on the board (A.3/088, A.6/087, C.2.f/081, C.3.d/083,
C.3.f/086) already carries substantial unpushed branch work — A.3 in particular is drafted through
stage 12 on branch `088` (pushed to origin 2026-09-21 to un-strand it). C.2.h has no branch, no
chapter, and no prior ticket. It is a NEW-v5, SDT-only hypothesis anchored on essentially one
identified design, so it is a reasoned smallest, not a measured one. **The frame probe + registered-
construct completeness test still owe (stage 3);** the "smallest" claim is provisional until they run.

*Result.* Stage 2 deliverable at `literature/search-logs/digital-leisure-substitution-search-scope.md`.
It states C.2.h's single parameter (effect of a fall in the price / rise in the absorptiveness of
digital leisure on fertility and its partnering/coital mediators, net of C.2.e wages, A.24 matching,
A.14 coital-frequency identity, D.1.a values, D.3.a clinical distress), five boundary walls, an
estimand-cell table with routing, three conjoined query blocks for §5.1, eligibility rules, and the
reverse-causality/common-trend identification cautions. Per the A.6/A.3 lesson it carries a
**registered-construct completeness check** confirming every noun the §C.2.h claim names is in the
topic block and none is priced as a free-standing `OR`.

*Anchor verified.* Primary seed existence-checked live: Myers & Hooper, "Is the iPhone Birth
Control?", NBER w35310 (2026), nber.org/papers/w35310 + SSRN 6897299 — AT&T 2007–2011 exclusive
iPhone-carrier instrument, 33–52% of the post-2007 GFR decline, with time-use corroboration of all
three registered sub-mechanisms (social displacement, pornography, lower sexual frequency). The
registry's "3G carrier rollout" gloss is imprecise and is corrected in the scope.

*Next (stage 3, heavy infrastructure).* Cold-start anchor build + existence-verify (mirror script
89), Tier-A/B citation frame (mirror 90), and the blinded LLM title/abstract screen (91–94). These
need OpenAlex/Crossref API access and LLM screen budget. Checkpoint with RA before spending it.

**2026-09-21 — Stage 3 frame probe run (the cheap confirmatory step, before any screen spend).**

*Result.* `source/build/goldset/52_c2h_frame_probe.py` (mirrors A.3's `405`) measured C.2.h's own
conjoined frame and its walls in ~43 OpenAlex counting requests, 0 refusals →
`literature/search-logs/c2h-frame-probe-2026-09-21.{json,md}`.

**The probe refutes the "smallest" prior — as intended.** C.2.h's own frame is **1,592** (narrow,
fertility-only) to **1,911** (production, partnering outcomes included), against A.3 = 719, A.6
corrected = 1,225, and C.3.a's 1,808 "smallest" bar. Housing (a written chapter) reproduced at 181
vs. `405`'s 205, so the counter is sound. **C.2.h is a mid-sized literature, not the smallest** — it
sits at/above the C.3.a bar and above both parked A-section candidates.

**But the completeness test passes cleanly** (unlike A.6/A.3): every registered construct is already
in the frame (smartphone / social media / screen time / video game each +0 marginal), the genuine
additions are legitimate C.2.h territory (streaming +1,674, gaming +1,075, pornography +142), and the
two generic design words are correctly caught as free-OR inflaters and excluded (`substitution`
+4,891, `attention` +19,348). There is no missing-construct or channel-annexation defect — the frame
is honestly built, it is just not small.

**Walls:** C.2.e (overlap 3 / neighbour 1,337 / identified 0), A.24 (16 / 75 / 1 — A.24's whole
frame is only 75), A.14 (9 / 8,521 / 1), D.1.a (15 / 849 / 0) are thin and cleanly routable. **D.3.a
(mental health) is load-bearing: 281 overlap, 23 identified** — the screen-time→anxiety→fertility
literature is the routing challenge and Wall 5 will be exercised hard. Frame carries 73 identified-
design markers (3.8%) — a thin-but-real potential core, A.3-shaped.

*Decision needed (returns to the board rule).* Per the A.3/A.6 precedent, a frame at/above the 1,808
bar means the "smallest" selection is not supported. C.2.h is still genuinely unstarted, cleanly
scoped, and well-anchored, so it is a defensible *deliberate* pick — but it is a deviation from
smallest-first, and the honest alternative is to cheaply probe other unstarted candidates (D.3.a,
B.4, A.16) before spending screen budget. Paused here for RA call; no screen spend yet.

**2026-09-21 — RA (Shravan) elected to proceed with C.2.h as a deliberate pick** despite the mid-size
frame (second deviation from strict smallest-first this session; the first was A.3/088). Stage 3
continues.

**2026-09-21 — Stage 3 cold-start anchors built and existence-verified.**

*Result.* `source/build/goldset/53_c2h_cold_start_anchors.py` (mirrors 89/A.3, 64/B.1) enumerated 13
anchors — no DOIs asserted — and verified each via live Crossref bibliographic match (Jaccard ≥ 0.72
AND year ±1). Outcome: **6 verified, 1 verified-pinned (Becker 1965, DOI curated because Crossref's
bibliographic ranker mis-orders it), 5 version-drift (real papers whose top Crossref hit is the
SSRN/NBER preprint, not the VoR — swap on freeze), 1 ghost (Ryu 2024).** So **12 of 13 are
existence-verified**; identity is Crossref-gated. Outputs:
`literature/search-logs/digital-leisure-substitution-cold-start-anchors.{json,md}`; cache
`source/build/goldset/c2h_crossref_cache.json`.

*Environment note (recorded, not gated on).* doi.org re-affirmation returns HTTP 403 from this
sandbox for every DOI (including canonical ones like Becker's JSTOR id), so the second re-affirm gate
is unavailable here; the existence gate is the live Crossref match, and doi.org status is logged as
`blocked`. An RA on an unblocked network should spot-check the resolved DOIs on freeze.

*Anchor set.* Empirical core (all verified): Myers–Hooper 2026 (w35310, the primary), Billari–
Giuntella–Stella 2019 (broadband→fertility), Guldi–Herbst 2017 (broadband→teen fertility), Bellou
2015 (internet→marriage), Aguiar–Bils–Charles–Hurst 2021 (video games→young-men hours; MECHANISM).
Theory: Becker 1965 (time allocation), Twenge 2017 iGen. Five wall decoys, one per registered wall,
all resolved: Bloom et al. 2009 (C.2.e wage), Rosenfeld et al. 2019 (A.24 dating apps), Bongaarts
1978 (A.14 coital-frequency identity), Lesthaeghe 2010 (D.1.a values), Twenge et al. 2018 (D.3.a
screen-time→depression).

*Two RA items (not blockers).* (1) The five version-drift DOIs point at preprints; swap to VoR before
gold freeze. (2) `PRIMARY_PORN_SUBSTITUTION` has only the registry's imprecise "Ryu 2024" seed, which
ghosted at Jaccard 0.2 — the correct citation must be hand-found; the porn strand is otherwise
unanchored.

*Next — the budget-heavy stage-3 remainder.* Tier-A/B citation frame (mirror 90: resolve anchors in
OpenAlex, backward+forward citation snowball) then the blinded LLM title/abstract screen (91–94). The
citation frame is a large OpenAlex spend (highly-cited theory anchors like Becker/Bongaarts/Lesthaeghe
need a forward-citation cap) and ~43 of today's ~100-request allowance is already used on the probe,
so the frame + screen are the next work session on fresh budget. Paused here.
