# TICK-076: A.18 Genetic and Heritable Variation in Fertility
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `heritability-fertility-genetic` — HYPOTHESES-v5.md §A.18
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/heritability-fertility-genetic-*, extraction/heritability-fertility-genetic-*, output/chapters/heritability-fertility-genetic.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/heritability-fertility-genetic-search-scope.md` (2026-08-31). **FROZEN:** Rulings 1–4 resolved; 5 routed to TICK-001. Stage 3 unblocked.
- [~] 3. Literature search and AI screening, both phases (§5.1) — snowball pool built (3,140 records, 246) and diagnosed (247); production query and screen outstanding
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/heritability-fertility-genetic.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-08-31 (Shravan) — stage 2.** Scope memo drafted; 25/25 cold-start anchors resolved against
OpenAlex, no ghost citations (`245_a18_cold_start_anchors.py`).

Three things the scope work turned up that are not local to this chapter:

1. **A.18's primary estimand is a variance component, not an effect.** Heritability cannot enter a
   PROTOCOL §4.2.1 demographic-significance calculation — there is no numerator. Ruling 1 puts the
   demsig arm on the selection *response* (a mean shift) instead. A.9, the other non-effect entry in
   the master list, will need the same treatment.
2. **The registered SDT-only phenomenon drops the identified evidence.** The best-identified
   selection-response designs are historical parish pedigrees (Milot 2011, Courtiol 2012); the
   contemporary arm is UK Biobank and HRS, the weakest designs in the set. Ruling 2 asks to admit
   PM/FDT as evidence arms with SDT still carrying the verdict. Blocks the production query.
3. **The resolver defect is still shipping.** A script written today reproduced the OpenAlex `?`
   wildcard refusal *and* recorded it as an absence. Fixed here; belongs in the shared resolver
   alongside TICK-074, which is unmerged.

Next: PI answers on Rulings 2 and 4, then stage 3.

**2026-08-31 (Shravan) — Rulings 1–4 resolved, scope frozen, stage 3 unblocked.**

1. **Demsig arm.** FDT and SDT compute on the selection response R = h² × S. **A PM cell for h² is
   opened**, which reverses the draft's flat claim that heritability has no §4.2.1 numerator anywhere:
   PM's denominator is a *range*, not a change, so a variance share is the right kind of quantity for
   it. Contingent on a protocol answer about units (below). Carries a written caution: the PM share is
   near-definitional, will clear the 10% threshold on almost any twin estimate, and means far less
   there than "significant" means in any other chapter.
2. **Phenomena.** Three-phenomenon chapter, verdicts wherever the arithmetic exists. The halfway
   version first proposed — PM/FDT as evidence, SDT-only verdicts — would have left the
   best-identified designs in the literature permanently unable to move a verdict cell.
3. **`EDUCATION_PGS`.** PGS standard units primary; conversion to children per woman a labelled
   secondary with the r_g interval propagated.
4. **Fecundity traits.** `LINK_TRAIT` unless the same study links the trait to realized births.
5. **Master-list edit confirmed necessary** and drafted in §13 for TICK-001 — `phenomena` widens to
   PM/FDT/SDT, and the `claim` becomes three clauses matching the three arms, including the moderation
   finding the registered text omits.

**Two questions escalated to Anup as protocol-level, neither blocking:** whether PM's §4.2.1
denominator admits a within-population between-individual variance numerator (binds stage 10, and A.9
has the same problem), and the fact that GRADE §4.1 has no band for a non-effect estimand, so a
competent twin design scores "Very low: correlational only" (binds stage 11; proposed
`NOT RATEABLE — non-effect estimand`).

Next: stage 3 — build the frame from anchor provenance, then the production query.

**2026-08-31 (Shravan) — stage 3 begun: provenance pool and its diagnostics.**

`246` snowballed the 25 anchors backward and forward into a **3,140-record pool**, zero API errors.
Both rungs productive (backward 1,328 new, forward 2,032), so neither is redundant. All three Ruling-2
arms are reached with large exclusive sets — SELECTION 1,168 records reached by no other arm, H2 830,
THEORY 312, METHOD 196, H2_MOD 193 — so no arm is silently missing. Five seeds were forward-capped at
200 and are named in the log; their contribution is the high-citation head, not a sample.

`247` measured the homonym on two channels that fail differently. **Species contamination in the pool
is 1.6%** against roughly half the naive term space — the provenance-first decision, quantified.

Three things worth carrying off this chapter:

1. **The filter nearly deleted our own estimator canon.** Reading rejects rather than admits showed 59
   of the first run's 112 flags were the selection-methods literature the SELECTION arm is built on —
   Lande and Arnold 1983 among them, reached by five of our own seeds. Six method anchors added to §12
   as a result, and Rausher 1992 now supplies §10 threat 1 its formal statement.
2. **A patch that changed nothing looked like it worked.** Removing the offending subfield from the
   cloud list left all 59 flags in place, because a field-level fallback swept the parent field anyway.
   Caught only because the total barely moved. Right answer, wrong mechanism.
3. **The real wall is phenotype, not species** — the pool is behaviour genetics and sociogenomics, and
   its off-target mass is other phenotypes (education, cognition, psychiatric traits). **66% of records
   name no phenotype in the title**, so a title-only screen cannot enforce that wall. The screen runs
   on abstracts; silence goes to `INSUFFICIENT_INFO`, not to reject.

Re-ran `247` end to end: byte-identical output. Next: production query, calibrated against the pool.

**2026-08-31 (Shravan) — production query adopted.** `(GENETIC) AND (FERTILITY)`, frame 45,491,
84% anchor floor, **87.3% pool recall net of wall route-outs** (`248`–`250`, scope memo §15).

The first candidate scored 64% anchor recall and lost seven of nine SELECTION anchors. Cause: **in
the evolutionary-selection literature the fertility outcome is called `fitness`** — Kong, Beauchamp,
Byars, Sanjak and Milot measure selection on lifetime reproductive success without ever using the
word "fertility". Adding `fitness`, `twins` and `genotype` took anchor recall to 84%.

Two anchors (Byars 2009, Sanjak 2017) are unreachable by any boolean — their abstracts name no
fertility outcome at all — so **for the SELECTION arm the citation channel is co-equal with the
boolean channel, not a supplement**, and PRISMA must report the asymmetry per arm rather than one
pooled recall number.

The raw 59.8% pool figure was the gold's fault: of 37 misses, 13 are Wall 1 route-outs to A.19,
8 are Wall 3 route-outs to B.1, 8 have no genetic exposure, and only 8 are genuine A.18 candidates.
Classifications are title-keyed hypotheses for the RA gate.

Leave-one-out on every term: `parity` dropped (240,805 frame, zero anchors), `pedigree` dropped,
three stemming duplicates dropped; six zero-yield terms KEPT because each names a §5 enumerated
design at under 250 records of frame cost.

Next: pull the frame and run the §5.1 two-phase screen on abstracts (§6 — the phenotype wall is
title-invisible).

**2026-08-31 (Shravan) — frame pulled, prescreened, and the unscreened tail bounded.**

Frame pulled whole: **45,568 records** (`251`), 18.4% with no indexed abstract.

**PROTOCOL §5.1's saturation stopping rule fails here** (scope memo §16). Measured gold-recall curve:
at the 1,000-record stopping rule this chapter would capture **31.7%** of its known gold, and the
curve is still climbing at 26% of the frame. Escalated to Anup as protocol-level — the rule was
calibrated on the OAS pilot and never re-tested, and **every chapter that already used it has an
unmeasured recall problem rather than a clean PRISMA**. One relevance-ordered pull per chapter checks it.

Prescreen (`252`): only two of six candidate rules survive a gold recall check — non-human organism
(-25.0%) and no-fertility-outcome-in-abstract (-5.5%). Survivors **31,960**, gold 65/65. Title-only
screening would cut 62% but destroy 8 gold: the §6 title-invisibility claim, now measured.

The tempting reduction — keep only the 320 survivors the citation channel also reached, holding 64
of 65 gold — is **circular** and was refused: the gold is pool-derived, so that statistic is a
tautology.

Instead `253` sampled the tail blind, with 12 hidden gold controls. **Sensitivity 12/12 (100%)**;
tail prevalence **1/150 = 0.7%**, implying **≈210 relevant records (95% CI 37–1,164)** unscreened.
PRISMA reports that bound rather than claiming completeness.

Next: screen the citation-channel intersection (320) plus the boolean relevance head, and run
snowball round 2 from whatever the screen promotes.

**2026-08-31 (Shravan) — dedup correction.** Two of my own outputs disagreed (32,126 survivors as a
list vs 31,960 as a set of ids), which surfaced duplication in the pull: **236 repeated openalex ids**
plus **2,996 titles shared across distinct ids, 3,282 records** — one Figshare item deposited **159
times**. `254` collapses both, with **first-author agreement required** to merge a title cluster; 393
clusters were kept apart because it failed. An unreadable (fully non-Latin) author name folds to ""
and would have merged every such record together, so each gets a unique sentinel: an author we cannot
read must prevent a merge, not license one.

Corrected: frame **42,050 distinct works** (not 45,568), prescreen survivors **29,394** (not 32,126),
tail population **29,077**, tail prevalence **1/136**, unscreened estimate **213 (95% CI 37–1,176)**.
All prescreen conclusions hold — same two rules adopted, gold 65/65 retained, title-only still
destroys 8 gold. Raw frame dumps moved to `temp/a18/` and gitignored: the 75MB frame should never have
been committed.

