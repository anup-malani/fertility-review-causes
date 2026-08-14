# TICK-068: B.6. Microplastics and PFAS in Reproductive Tissues
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `microplastics-pfas-reproductive` — HYPOTHESES-v5.md §B.6
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/microplastics-pfas-reproductive-*, extraction/microplastics-pfas-reproductive-*, output/chapters/microplastics-pfas-reproductive-{pfas,microplastics}.md, source/build/goldset/13*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/microplastics-pfas-reproductive.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise — **run twice, once per chemical family; never pooled across**
- [ ] 10. Demographic significance against SDT — **run twice, each family against its own exposure series**
- [ ] 11. GRADE rating, 3 independent raters — **run twice; no bundled B.6 rating at any stage**
- [ ] 12. Chapter drafts on the §6 template — **two chapters** (Call 1, decided 2026-08-14):
  - [ ] 12a. `output/chapters/microplastics-pfas-reproductive-pfas.md`
  - [ ] 12b. `output/chapters/microplastics-pfas-reproductive-microplastics.md`
- [ ] 13. RA lay-readability check, both chapters
- [ ] 14. PI review and sign-off, both chapters

## Log

**2026-08-14 — opened (Shravan).** Scripts for this hypothesis start at
`source/build/goldset/132_b6_*`. 131 is the highest number in use anywhere — it is on the
unmerged `066-antidepressants-ssri-subfecundity` branch, and 115 is on `062-postmaterialism-…`,
which exists only locally and is invisible from `origin`. Numbering above `main` alone would have
collided a third time.

**2026-08-14 — stage 2 done (Shravan): search strategy and scope drafted.**
`literature/search-logs/microplastics-pfas-reproductive-search-scope.md`, built on the B.7 template,
against two live OpenAlex passes (`132_b6_recon_probe.py`, 72 probes; `133_b6_anchor_retry.py`, 20
probes; **zero failed requests in both**, so the zero counts are absences and not refusals). Nine
walls specified, five scope calls raised with recommendations. Three findings drive the design:

1. **B.6 bundles two hypotheses with opposite profiles.** PFAS has real human fertility epidemiology
   (time-to-pregnancy n = 127, two prior meta-analyses) and a *falling* legacy exposure series —
   NHANES reports PFOS and PFHxS declining after production was discontinued. Microplastics has the
   new tissue-detection literature and a *rising* series, but essentially no human fertility
   epidemiology. v5's note that "the exposure is structurally rising" is false for the half that
   carries the evidence. Call 1 asks for per-family verdicts.
2. **No quasi-experimental estimate of either exposure on a fertility quantity exists.** The only
   natural experiment found (Waterfield et al. 2020, a difference-in-differences on a Minnesota water
   filtration plant) has birth weight and preterm birth as outcomes, so Wall 2 routes it out. The
   GRADE ceiling is set before the search runs, on design rather than volume.
3. **Three of v5's four seminal citations do not resolve as written**, including one that is a
   phthalate paper — i.e. on the B.2 side of the wall that defines B.6. Detailed in Call 4 for
   TICK-001, with a recommendation to re-verify the other v5-era entries on the same gates.

**2026-08-14 — Call 1 decided; walls frozen.** B.6 stays **one hypothesis, one entry in
`HYPOTHESES-v5.md`, one ticket, one search**, and produces **two chapters** — one per chemical
family. The split lands at extraction, on `CHEMICAL_FAMILY`; everything upstream (walls, screen,
anchors, PRISMA identification and screening counts) is shared, and stages 9–14 run twice. Promoting
the families to B.6.a/B.6.b in the hypothesis list was considered and **not** done: the taxonomy is
TICK-001's to change, and renumbering the master list propagates into every in-flight branch's
`HYPOTHESES-v5.md §X` reference. The registry question goes to the PI for v6 alongside the Call 4
citation corrections, since both edit the same entry. With Call 1 answered, **the nine walls are
frozen**; Calls 2, 3 and 5 remain open and none of them blocks the search.

Also new: a **duplicate-record gate** (the Minderoo-Monaco Commission carries two DOIs with different
citation counts plus an erratum, so DOI-level dedup double-counts it), and a correction to B.7's
scope, which wrongly lists B.6 among the hypotheses whose exposure post-dates its phenomenon — B.6's
exposure is older than the SDT; only its *measurement* is recent.
