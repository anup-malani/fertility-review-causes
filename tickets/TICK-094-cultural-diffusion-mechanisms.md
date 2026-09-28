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
