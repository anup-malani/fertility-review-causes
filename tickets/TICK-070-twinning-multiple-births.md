# TICK-070: A.12 Twinning Rates and Multiple Births
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `twinning-multiple-births` — HYPOTHESES-v5.md §A.12
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/twinning-multiple-births-*, extraction/twinning-multiple-births-*, output/chapters/twinning-multiple-births.md

## Acceptance criteria
- [x] 2. Search strategy and scope **FROZEN** — `literature/search-logs/twinning-multiple-births-search-scope.md` (drafted 2026-08-20, frozen 2026-08-22). 9 walls, 10 estimand cells. Call 3 decided (split at the margin); calls 1 and 5 adopted as recommended, RA-provisional; calls 2 and 4 open by design and answered during the run.
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/twinning-multiple-births.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-20 — reconnaissance and scope draft
Pre-scope recon run (`source/build/goldset/160_a12_recon_probe.py`, 63 requests, 0 failed);
report at `literature/search-logs/twinning-multiple-births-recon-probe.md`.

Three findings that set the shape of the chapter:
- **The primary cell is populated by vital-statistics reports, not estimation studies** (n=25, n=93;
  heads are *Births: Final Data for 2013* and *Annual Summary of Vital Statistics*). Correct for an
  accounting identity. The estimable parameter is the *offset* — whether a twin birth displaces
  subsequent fertility — and it has been estimated by name three times (Alter & Hacker 2024
  *Demography*; Robson & Smith 2012 *Proc R Soc B*; Clark, Cummins & Curtis 2020 *Demography*).
- **v5's ART clause is time-inverted.** eSET cut ART multiple-birth rates from the early 2000s;
  the literature already calls the shape a peak (Monden, Smits & Pison 2021, *Twin Peaks*). v5
  describes a monotone offset over a period that has closed.
- **Two of four decoy families are pure homonyms, not boundary cases** — crystallographic twinning
  (SHELX, 87,676 cites) and TWIP steel / digital twin — and are separable lexically. The
  behaviour-genetics cloud (A.18) is a real boundary case and is routed, not excluded.

Script numbered 160 against the cross-branch high-water mark of 159; `main` alone would have said 89
and collided with five live branches.

### 2026-08-22 — Call 3 decided, walls frozen

**Call 3 ruled: split at the margin.** `ART live births = D_ART x (1 + m_ART)`; A.17 owns the
deliveries, A.12 owns the multiplier. Additively separable, so both chapters can report a
contribution without double-counting. Ruled with an explicit caveat, which the chapter carries to its
verdict: **the intensive margin is not identified.** `m_ART` is chosen rather than assigned, it is
jointly determined with `D_ART` (eSET raises cycles per live birth, hence cost per birth, hence `D`),
and the counterfactual "TFR without ART multiples" is not a ceteris-paribus perturbation of `m`.
`SECONDARY_ART_MULTIPLES` therefore yields a measured *share*, not an estimated effect, and is
GRADE-downgraded for indirectness on identification grounds independently of the sign problem.

**The ruling forced a wall re-cut, and the drafted version would have been self-defeating.** Wall 6
hard-excluded "clinical ART practice (transfer protocols, success rates)". Under the split that
discards the eSET policy literature — the only quasi-experimental variation in `m_ART` there is, and
the one Pison, Monden and Smits name as the cause of the post-2000 reversal. Wall 6 is now cut on
**outcome, not treatment**: population multiple-birth-rate outcomes are included, per-cycle clinical
outcomes excluded. Still enforceable at title/abstract, because abstracts name their outcomes.

**A second finding from the same live check: the twinning rise is partly endogenous to the
phenomenon it is claimed to offset.** Pison, Monden and Smits (2015) decompose the developed-country
rise into delayed childbearing and MAR, with MAR about **three times** the age effect. The remaining
quarter is the maternal-age composition shift — i.e. postponement, which is the very SDT mechanism
v5 says twinning offsets. That component is a feedback of the decline, not a force against it, and
only the MAR component is even a candidate offset. Split at extraction.

**Order of magnitude, live and provisional.** Monden, Smits and Pison (2021): global twin delivery
rate 9.1 -> 12.0 per 1,000 deliveries between 1980-85 and 2010-15, so births per delivery moved
~1.0091 -> ~1.0120, a rise of about **0.29% over four decades** — before the stopping offset and
before netting the endogenous age component. Global figure; stage 10 recomputes on the
developed-country HMBD series. Recorded pre-screen so that an apparently large A.12 effect gets
audited rather than believed.

Calls 1 and 5 adopted as recommended and marked RA-provisional. Call 5 is made free to reverse by
**pulling and tagging** the cross-population PM cluster as `SECONDARY_PM_VARIATION` instead of
excluding it, so an overturn costs a re-screen and never a re-search.

Next: A3 cold-start anchor resolution (script 161).
