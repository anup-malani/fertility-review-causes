# TICK-070: A.12 Twinning Rates and Multiple Births
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `twinning-multiple-births` — HYPOTHESES-v5.md §A.12
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/twinning-multiple-births-*, extraction/twinning-multiple-births-*, output/chapters/twinning-multiple-births.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/twinning-multiple-births-search-scope.md` (2026-08-20). **DRAFTED, NOT FROZEN**: 9 walls, 10 estimand cells, 5 PI calls; calls 1, 3 and 5 gate the production run.
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

