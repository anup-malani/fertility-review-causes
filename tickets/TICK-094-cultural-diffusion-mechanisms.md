# TICK-094: A.20 Cultural Diffusion Mechanisms
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `cultural-diffusion-mechanisms` — HYPOTHESES-v5.md §A.20
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/cultural-diffusion-mechanisms-*, extraction/cultural-diffusion-mechanisms-*, output/chapters/cultural-diffusion-mechanisms.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/cultural-diffusion-mechanisms-search-scope.md`
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/cultural-diffusion-mechanisms.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**Selection rationale (2026-09-28).** Picked as the next-smallest genuinely-unstarted hypothesis by
measured frame. The board's "Open" list is stale — every listed ticket 086–093 has a live branch with
commits and a unique chapter (verified against `git branch`, not the board). Among unclaimed
candidates, TICK-092/093's extended scout ranked A.20 next after D.1.d (1,720, now TICK-093) at a
scout frame of **~1,968** (next A.19 2,414, B.2 4,475).

**Caveat carried into stage 3 (the A.6/A.3 lesson).** A.20 is a proximate/mechanism hypothesis that
per HYPOTHESES-v5 "absorbs" `social-network-peer-effects`, `ideational-diffusion-mass-media`, and
`linguistic-cultural-boundaries-princeton`, and shares its seminal set (Coale & Watkins 1986,
Bongaarts & Watkins 1996) with **A.3 Diffusion and Social-Learning of Fertility Control — already
drafted as TICK-088** (`diffusion-of-fertility-control`). Stage 3 must run the full frame probe +
registered-construct completeness test and read the A.3 wall from both sides before the "smallest"
claim is trusted: A.20 owns the *channels of spread* (network architecture, media reach, community
boundaries) independent of norm content, whereas A.3 owns the *social-learning of fertility control
itself*. The scout number is a prior to be hardened, not a settled measurement.

**2026-09-28 — Stage 2 done; Stage 3 prepared, PAUSED before the OpenAlex spend.**
- **Stage 2 scope drafted:** `literature/search-logs/cultural-diffusion-mechanisms-search-scope.md`.
  Parameter = the effect of the diffusion *channel* (social-network architecture, mass-media reach,
  linguistic/cultural community boundaries) on fertility and on the pace/geography of its change, holding
  fixed the *content* of the diffusing norm and the *reason* demand changed. Three streams: media channel
  (Brazil *novela*, India cable TV), social-network/peer channel (Kohler-Behrman-Watkins), linguistic-
  boundary channel (Princeton). FDT + SDT, no PM. Six walls declared; discriminator = channel vs.
  content/cause on every one.
- **The A.3 redundancy worry is largely resolved in A.20's favour before spending a cent:** A.3's own
  Wall 1 (resolved 2026-09-18, TICK-088) deliberately routed the cleanest identified estimates —
  La Ferrara/Chong/Duryea 2012 (Brazil) and Jensen/Oster 2009 (India) — **to A.20**. Those are A.20's
  registered seminals and its identified core; A.20 owns the well-identified media-channel literature A.3
  excluded as content-agnostic. Stage 3's job is to confirm the *identified* overlap with A.3 is thin.
- **Stage 3 probe PREPARED, NOT RUN:** `source/build/goldset/89_a20_frame_probe.py` (ported from
  `89_d1d`; py_compiled, all query terms comma-free, control-housing counter retained to validate on a
  known positive). It prices the A.20 frame against its own conjoined constructs (completeness test),
  reads all six walls from both sides, and counts the homonym load (physics `diffusion`, social-network
  *analysis*, marketing `media`). **Paused before execution per the standing "pause before OpenAlex
  spend" checkpoint** (405/52/89_d2c/89_d1d precedent) — awaiting the go-ahead to run.

**2026-09-28 — Stage 3 (part 1): frame probe RUN; the "smallest" prior holds and the A.3 worry is
refuted.** Artifacts `literature/search-logs/a20-frame-probe-2026-09-28.{json,md}`. Counter sound
(control housing 166, matching 89_d1d). **Honest production frame = 2,040** (scout ~1,968) — A.20 stays
the next-smallest genuinely-unstarted candidate, below A.19 (2,414) and B.2 (4,475). **Completeness test
passes:** specific channel constructs add ~0 (linguistic boundary +2, language group +32, cultural
boundary +44, spatial diffusion +43, social learning +99); every large gain is a generic free-OR
inflater correctly excluded (network +13,836, media +9,604, communication +8,593, diffusion +2,184).
`social network` (+940) and `social media` (+1,503) are genuine-but-noisy registered constructs — held
out of the *selecting* frame, folded in at screen with the SNA/platform homonym filtered. **Walls thin,
decisively on A.3:** A.3 84/2,040 raw (4.1%), **identified overlap 3** — A.20's identified core is
essentially disjoint from A.3's, as A.3's Wall-1 resolution predicted. Others (raw/neighbour/identified):
A.19 11/1,194/0, A.2 89/10,217/1, A.5 94/3,074/4, D.1.a 24/722/0, D.1.d 20/1,294/0. Homonym load low
(physics diffusion 0, SNA-method 8, marketing 50 ≈ 2.8%); 56 frame records carry an identified-design
marker. **Decision:** A.20 confirmed the next-smallest genuinely-unstarted candidate on the hardened
frame; the walls behave as the scope predicted; the frame is honestly built. **Next (paused for
checkpoint):** the budget-heavy Stage-3 remainder — cold-start anchors → citation frame → production
frame → blinded Haiku screen — the point at which D.1.d paused for the RA/PI checkpoint.
