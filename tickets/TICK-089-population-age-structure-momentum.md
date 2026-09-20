# TICK-089: A.9 Population Age Structure and Demographic Momentum
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `population-age-structure-momentum` — HYPOTHESES-v5.md §A.9
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/population-age-structure-momentum-*, extraction/population-age-structure-momentum-*, output/chapters/population-age-structure-momentum.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/population-age-structure-momentum-search-scope.md` (DRAFT, not frozen)
- [x] 3. Literature search and AI screening, both phases (§5.1) — production query + full PRISMA pass; `…-screen-report.md`, 16 included
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/population-age-structure-momentum.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [x] 9. Structured quantitative synthesis (NOT pooled — decomposition shares across heterogeneous outcomes/signs); `output/tables/population-age-structure-momentum-synthesis.md`
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

Nominated as the smallest open **A. Proximate Causes** candidate. The three obviously-small
proximate determinants that would otherwise lead the ranking — A.12 twinning (TICK-070), A.17 ART
(TICK-072), A.18 heritability (TICK-076) — are already claimed, as are A.3 (TICK-088), A.6 (TICK-087,
parked), A.23 (TICK-075) and A.24 (TICK-071). A.11 tempo is drafted. Of what remains open (A.1, A.2,
A.4, A.5, A.7, A.8, A.9, A.13, A.14, A.15, A.16, A.19, A.20), A.9 is the only one whose mechanism is
an **accounting identity** (age composition → CBR / period TFR, holding age-specific rates fixed)
rather than a contested behavioural or biological literature; its registry note calls it "largely
accounting/measurement," and its seminal set (Keyfitz 1971; Bongaarts & Bulatao 1999; Lutz et al.
2003) is small and uncontested. It parallels the already-drafted **A.11 tempo-effects** chapter — the
same "measurement/mechanical determinant" shape — so we reuse that template for the hard part, which
is framing a mechanical determinant against PM / FDT / SDT.

**Caveats to resolve in stage 2, before trusting the "smallest" claim:**

1. **The frame probe has not measured A.9.** `source/build/goldset/304_candidate_frame_probe.py` and
   its 09-10 / 09-13 runs live on the unmerged TICK-080 branch and do not yet include A.9. Smallness
   here is qualitative (registry note + seminal set), not a measured union-frame/anchored-core count.
   Run A.9 through the probe as the first scope step and record its union frame, anchored core, and the
   core-of-union ratio (the C.2.f / C.3.d "anchored literature" signature).
2. **Registered-construct completeness test.** A.6 and A.3 each placed first on raw count and were
   passed over because their selecting frame omitted the registry's own construct and undercounted the
   literature (`404`, TICK-087/TICK-088). A.9 must be cleared of the same defect: confirm the frame
   carries the registry's construct vocabulary (demographic momentum, age-structure / population-age
   composition, tempo-vs-quantum-adjacent decomposition terms) before its count is trusted.
3. **Homonym load.** "Momentum" and "age structure" are heavily overloaded outside demography
   (physics, finance, population-genetics age structure). Run the homonym residue check inside the
   fertility-restricted frame, as C.3.f did.
4. **Boundary with A.11 tempo.** Momentum (a stock/composition effect on completed and period
   fertility) and tempo (a timing distortion of period TFR) are distinct but adjacent and both live in
   the period-vs-cohort measurement debate. Measure the A.9↔A.11 wall and state the scope split
   explicitly; A.11 is drafted so that wall is inherited, not litigated.

**Phenomena:** registry §A.9 lists **FDT, SDT** (not PM), so stage 10 assesses two phenomena. The
likely verdict is near-determinate — momentum/composition moves CBR and short-run period TFR but not
completed cohort fertility — which is the reason this is a low-risk pass through the full pipeline
rather than a novel-evidence chapter. `empty-cell-is-the-result` / `empty-cell-needs-second-channel`
apply if the identified-design cell is thin.

## Log

**2026-09-20 (Shravan) — stage 2 search scope drafted.**

*Result.* Drafted `literature/search-logs/population-age-structure-momentum-search-scope.md` (DRAFT,
not frozen). Key rulings:
- A.9 is a **non-effect estimand** (decomposition/accounting + demographic momentum), not a treatment.
  Two constructs held apart: age-composition effects on period *counts/CBR*, and Keyfitz-style
  demographic momentum.
- **Load-bearing correction:** the composition effect lands on the **CBR and birth counts**, is **zero
  by construction on the period TFR** (which is already age-standardized) and **zero on completed cohort
  fertility.** The v5 claim text ("...crude birth rates and period TFR...") is imprecise on the TFR
  clause — flagged for TICK-001; tempo (A.11), not composition, is what moves period TFR.
- Four boundary walls: **W1 A.9 vs A.11 tempo** (composition/weights vs timing/rates — the sharpest),
  **W2 A.9 as the shared accounting residual** (A.10's Wall 4 already routes `MECHANICAL_COMPOSITION →
  A.9`; A.9's CBR verdict is *not additive* with other chapters), **W3 A.9 vs population-size/growth
  outcomes** (`OFF_OUTCOME_POP`, expected largest cell), **W4 A.9 vs A.1 mortality** (determinant of the
  age structure).
- Adopts TICK-080 §5–6 provisionally: GRADE **NOT RATEABLE — non-effect estimand**; demographic
  significance reported **per outcome** (CBR/births large-by-construction → report magnitude not
  pass/fail; period TFR = 0; CCF = 0), not a single label.

*Escalations to Anup (recorded here; no repo-wide escalation-log.md exists — same practice as A.10 /
TICK-054):*
1. **Non-additive proximate causes / mechanical-composition ownership.** Does A.9 own and *define* the
   mechanical-composition component that A.1/A.7/A.8/A.10 then report *net of*? Same item TICK-054
   (A.10 Wall 2) and TICK-080 raise; A.9 is the natural place to land the rule. **Blocks freeze.**
2. **Rating a non-effect estimand.** Confirm GRADE "NOT RATEABLE" and the per-outcome demsig reporting
   for A.9 (this is the concrete case behind TICK-080 §5–6). **Blocks freeze.**

*Workflow impact.* First chapter whose primary estimand is an accounting identity; it is the test case
for TICK-080's non-effect-estimand GRADE band and per-outcome demsig reporting, and the landing site
for the review-wide non-additivity rule. Reusable: the "the outcome is not the period TFR" three-way
outcome split parallels A.11 tempo and should be cross-linked when both are finalized.

*Next.* Stage 2 open items before freeze: run the frame probe (`304_candidate_frame_probe.py`, on the
TICK-080 branch) on A.9; registered-construct completeness test; homonym-residue check ("momentum",
"age structure"); second read on Wall 1; then anchor sourcing (channels 1–3, existence-gated).

**2026-09-20 (Shravan) — frame probe run (literature sized).**

*Result.* `population-age-structure-momentum-frame-probe.{md,json}`. Reused 304's exact `count()`
mechanics; control C.3.e = 85 (matches 304's 09-13 run). A.9 is a **small literature**: anchored
momentum core (`population momentum`/`demographic momentum` ∩ fertility) = **192**; working frame
(+`population age structure`) = **502**. The WIDE frame (~3,636) is **homonym-inflated** and discarded
— the generic pair `age structure`/`age composition` is 3,213 of it and 32,363 unrestricted (an
ecology / population-genetics term; 106 ecology records leak in even with the fertility gate). Momentum
vocabulary itself is clean (`demographic momentum` = 85 even unrestricted). A.11-tempo overlap inside
the frame = 136 (bounded; split at component level per Wall 1). This closes stage-2 item 1; homonym
check (item 3) is effectively answered by the same run.

*Workflow impact.* The homonym decomposition is the reusable lesson: a candidate whose WIDE frame is
7× its core is a vocabulary artifact, not a literature — here `age structure`/`age composition` must be
gated by a decomposition/CBR co-term, never admitted bare. Production cause axis (stage 3) anchors on
momentum-specific vocabulary; expect the estimand-ready cell to be a small fraction even of the ~200
core because much of the momentum literature's outcome is population size/growth, not a birth rate
(Wall 3 / `OFF_OUTCOME_POP`; `empty-cell-is-the-result` live).

*Still open before freeze:* registered-construct completeness test (item 2), Wall 1 second read, and
the two PI escalations above. Then anchor sourcing.

**2026-09-20 (Shravan) — cold-start anchor sourcing (channels 1–2), existence-gated.**

*Result.* `population-age-structure-momentum-cold-start-anchors.{json,log.md}`: 17 records, **all
existence-verified against OpenAlex** (no DOI asserted from memory), 15 identity-verified. Findings:
- **Channel 1 empty** — no systematic review / meta-analysis of A.9→fertility exists (only off-topic
  `type:review` hit). Third chapter in a row (D.3.b, C.2.c, A.9), and for A.9 it's the thesis, not an
  accident: an accounting identity has no effect literature to synthesize. First confirmation of the
  non-effect-estimand framing at the evidence stage.
- **Channel 2: 12 verified anchors**, but the empirical birth-rate/count decomposition cell has **one**
  (Preston & Guillot); the rest is momentum theory (Keyfitz 1971 v5-seminal, Kim–Schoen, Kitagawa
  method, PHG textbook, …) or population-size projection (Bongaarts–Bulatao, Lutz et al., both v5
  seminal, both OFF_OUTCOME_POP-tensioned). **`empty-cell-is-the-result` is live**; gold is far below
  the ≥30 CV floor by nature — production cause axis will come from the frame-probe vocabulary, not
  fold-local mining (no CV term-learning on a one-item cell).
- **Existence gate fired twice:** dropped a non-resolving "Espenshade correspondence" title (ghost risk)
  and the Das Gupta 1993 Census manual (no DOI); replaced/covered by verified Krishnamoorthy 1981 and
  Kitagawa 1955.
- **Decoys carried for routing** (A.9's binding constraint): Bongaarts–Feeney 1998 (→A.11),
  Lutz–Sanderson–Scherbov 2008 (→OFF_OUTCOME_POP), Caswell/matrix-models (→ ecology homonym).

*Workflow impact.* A.9 is shaping up as a theory-plus-decomposition synthesis chapter, not a
meta-analysis — the meta-analytic branch of the pipeline (stage 9) will almost certainly resolve to
narrative synthesis. This is the cleanest instance yet of the accounting-identity / non-effect-estimand
pattern the scope and TICK-080 items 6–7 + 10 describe.

*Next.* Channel 3 (citation snowball off the channel-2 seeds, forward-capped hard on the broad theory
anchors) → Tier-B frame; run at stage 3 once the scope is frozen (pending the two PI escalations + Wall
1 second read).

**2026-09-20 (Shravan) — channel 3 snowball → Tier-B frame.**

*Result.* `population-age-structure-momentum-snowball-{tierb.json,log.md}`: **199-record Tier-B frame**,
deduped vs the 12 seeds, all OpenAlex-sourced (existence intrinsic). Backward = refs co-cited by ≥2
seeds (16 of 114; the 98 single-seed refs held as expansion reserve); forward = the 5 topic-specific
momentum seeds only, capped at top-50 by citations. **Forward NOT run on the broad theory anchors**
(Keyfitz 201, PHG 1772, Kitagawa 562 citing) — the explosion guard held. Composition: 18 MOMENTUM
(orthogonal recall working), 119 OFF_OTHER (math-demography theory canon — Lotka/Keyfitz backbone, will
re-tag to theory stream), 41 FERT_OTHER, 13 OFF_OUTCOME_POP, 6 OFF_TEMPO_A11 (Wall 1 confirmed live in
the citation graph), 2 homonym/ambig.

*Workflow impact.* Third independent confirmation (frame probe → anchors → snowball) that A.9's
empirical birth-rate-decomposition cell is nearly empty and the literature is theory + projection —
`empty-cell-is-the-result`, narrative synthesis not meta-analysis. Tier B kept whole (unbiased-sample
definition) as the future Recall(B) yardstick; noted not-fully-orthogonal per the standing GACS caveat.

*Cold-start anchor sourcing (channels 1–3) is now complete.* Remaining before the production search:
freeze the scope (two PI escalations + Wall 1 second read + registered-construct completeness test),
then stage 3 (screen the frame, Haiku→Sonnet→RA).

**2026-09-20 (Shravan) — escalations resolved; scope FROZEN.**

*Resolutions (directing the work; formal PROTOCOL amendment + `decisions/` entry are TICK-080's):*
1. **A.9 owns and defines the mechanical-composition component.** The other proximate chapters
   (A.1/A.7/A.8/A.10) report their aggregate-count effects *net of* it; A.9's CBR/births verdict is
   "the mechanical share of observed change," never an independent additive contribution. Carried into
   TICK-080 item 10 (accounting layer netted out, not a competing tier).
2. **GRADE = NOT RATEABLE — non-effect estimand; demsig reported per outcome** (CBR/births = report the
   composition-share magnitude, not pass/fail; period TFR = 0 by construction; CCF = 0). Adopted, not
   provisional (TICK-080 items 6–7).
3. **Wall 1 (A.9 vs A.11) confirmed as drafted** — composition/weights vs timing/rates, component-level
   split.
Completeness test + homonym check were already satisfied by the frame probe.

*Result.* `population-age-structure-momentum-search-scope.md` **FROZEN**. All stage-2 gates cleared.

*Next.* Stage 3 — production keyword search (momentum-anchored cause axis per the frame probe; generic
age-structure terms gated by a decomposition/CBR co-term) + screen the 199-record Tier-B frame and the
keyword pull through Haiku→Sonnet→RA; report Recall(B) against the Tier-B frame.

**2026-09-20 (Shravan) — production query built + keyword pull; stage-3 screen not yet run.**

*Result.* `population-age-structure-momentum-production-query.json` (frozen) and
`…-production-search-log.md`. Tight momentum axis = 570; **the gated generic age-structure extension
(324) was tested and DROPPED** — even co-term-gated it is mostly epidemiological rate-standardization,
~19 true birth-rate-decomposition hits. Effective frame = tight axis (**565** after seed removal) ∪
Tier-B (**199**) ≈ **700 to screen**. Worklist (`…-screen-worklist.json`): ~45 plausibly-primary (35
MOMENTUM + 9 PRIMARY_COMPOSITION + 1 ambig), 81 OFF_OUTCOME_POP, 6 OFF_TEMPO_A11, 21 multi-channel
Tier-1 core candidates; the rest topical-overlap noise. Fourth confirmation that the empirical cell is
near-empty.

*Checkpoint.* Everything up to the screen is done. Stage 3's LLM screen (~700 records, D1→Haiku→Sonnet→RA)
is the biggest compute step and there is **no `sequential-screen.mjs`/`snowball-citations.mjs` on this
branch** — it is an inline LLM effort or needs that tooling. Also open: the protocol-level rulings
(escalations 1–2) were made to unblock A.9 but the **formal PROTOCOL amendment + `decisions/` entry
remain TICK-080's**, and Anup's sign-off at a sync is the clean closure. Paused here for a go-ahead.

**2026-09-20 (Shravan) — core-first screen (62 highest-prior records).**

*Result.* `…-core-screen-{results.json,report.md}`. Screened the plausibly-primary cells + 21
multi-channel Tier-1 candidates on title+abstract: **2 RELEVANT_PRIMARY, 1 UNCERTAIN, 37
RELEVANT_THEORY, 22 OFF.** The empirical A.9 cell is **~2 studies** — both China age-structure→CBR/births
decompositions ("…Age Structure Changes on the Crude Birth Rate in China" 2014; "Declining number of
births in China: a decomposition" 2021). **`empty-cell-is-the-result` confirmed** on the actual
records, not just predicted.

*Load-bearing routing finding:* "fertility decomposition" ≠ "age-structure decomposition." The other
decomposition papers route OUT of A.9 — Bongaarts proximate determinants (Nigeria, Egypt → A.2/A.5/A.13),
union composition (→ A.7), preference disparities (off). A.9 owns only the age-structure-vs-rate split.
The momentum literature (37) is formal theory (→ JEL theory stream) or population-growth outcomes
(OFF_OUTCOME_POP).

*Consequence:* stage 9 = narrative synthesis, not meta-analysis; demsig verdict rests on the 2
decompositions + accounting/momentum theory (near-determinate per outcome). The full ~700 pass is
unlikely to move the verdict (recommendation in the report: targeted recall check on the residual
"decomposition"-titled records, then full-text the 2–3 primaries and draft on the empty-cell finding).

*Next (decision):* (i) targeted recall check, (ii) full PRISMA pass, or (iii) proceed to full-text
retrieval of the 2–3 primary candidates and draft. Plus the standing TICK-080 formalization + Anup
sign-off before the verdict grid is final.

**2026-09-20 (Shravan) — targeted recall check: EMPTY-CELL FINDING RETRACTED.**

*Result.* `…-recall-check-{results.json,report.md}`. Focused queries at the empirical cell found **~15
genuine A.9 primaries**, not ~2 — multi-component CBR/birth-count decompositions (China, Korea ×3, South
Africa ×2, Malawi, Mexico, India, US ×3 incl. a 1932 study) from which the **age-structure contribution
share** is one extractable component (other components → A.7/A.2 at component level).

*Correction (mine to own).* The core-screen `empty-cell-is-the-result` call was **wrong**, from (a) a
title-only heuristic on the high-prior subset and (b) my dropping the gated generic axis wholesale — it
held the real decompositions mixed with epidemiological rate-standardization noise. The recall check
(the user's chosen path) caught it before any verdict was written. Production query updated: the gated
axis is **refined, not dropped** (age-structure term must co-occur with a birth/fertility term AND a
decomposition term). Retracted the empty-cell language in the scope and core-screen report.

*What changes.* Stage 9 is now a **quantitative synthesis of the composition-share magnitude** across
~15 studies, not narrative-only; the demsig CBR/births cell is empirically anchored, not just
definitional. GRADE stays NOT RATEABLE (decomposition shares, not effect sizes); demsig still per
outcome.

*Next.* Full-text retrieval of the ~15 primaries (several non-English/no-DOI → likely RA/library
procurement), then extract the age-structure share (magnitude, sign, period, setting, method, outcome
level) → `extraction/population-age-structure-momentum.csv`. A full PRISMA pass over the remaining
worklist is now clearly worthwhile.

**2026-09-20 (Shravan) — full PRISMA pass; included set finalized at 16.**

*Result.* `…-screen-{full.json,report.md}`, `…-included-studies.json`. Screened the full deduped universe
(**1,299** records = tight 738 ∪ refined-gated 434 ∪ Tier-B 199, seeds removed). PRISMA: **16 included
empirical primaries**, 38 → JEL theory stream (+12 canon anchors), 26 → A.11 (tempo), 123 pop-growth
off-cell, 81 homonym, ~1,001 off/topical. The full pass added exactly **one** primary beyond the recall
check (Hong Kong 1968) → the included set is stable and near-complete. Included spread: China ×3, Korea
×3, USA ×3, South Africa ×2, + China/India, Malawi, Mexico, India; 1932–2024.

*Stage 3 complete (acceptance criterion 3 checked).* RA procurement flagged for the no-DOI / non-English
items (South Africa 2019/2011, China 2014, Mexico 1991, Korean/Chinese-language).

*Next.* Stages 5–7: full-text retrieval (AI-accessible first) → extract the age-structure contribution
share into `extraction/population-age-structure-momentum.csv` (magnitude, sign, period, setting, method,
CBR vs births), RA verifies 10%. Then stage 9 quantitative synthesis of the composition share.

**2026-09-20 (Shravan) — extraction started (stages 5–7); OA subset.**

*Result.* `extraction/population-age-structure-momentum.csv` (16 rows) +
`…-RA-procurement.csv` (13 closed items). OA availability: **only 3/16 are open access**; 13 closed →
RA/library queue (several non-English: Korea ×3, China 2014, Mexico 1991).
- **1 study fully extracted** — Chaurasia 2017 (China/India, *Comparative Population Studies*, OA):
  Kitagawa two-component decomposition; **age-composition (momentum) component ≈ 80% of India's natural
  growth rate 2010-15, >100% for China** (intrinsic ~0); age-composition multiplier on the CBR (ab)
  **1.01–1.21** (inflated CBR up to ~21%). Confirms the A.9 signal is large for CBR/growth; the paper's
  own `f = w × TFR/35` confirms period TFR is composition-free (our by-construction claim).
- 2 OA PDFs in hand (Malawi 2024, India 1983) pending extraction; 13 need RA procurement.

*Workflow impact.* Extraction is feasible and the numbers are real; the binding constraint is now PDF
access (PROTOCOL stage-5 human gate), not screening. The first extracted magnitude already anchors the
CBR/growth demsig cell empirically.

*Next.* Extract the 2 OA PDFs in hand; hand the 13-item procurement list to the RA; then extract those
as PDFs arrive → stage 9 quantitative synthesis + stage 10 per-outcome demsig + stage 11 GRADE
(NOT RATEABLE) + stage 12 chapter. TICK-080 formalization + Anup sign-off still precede the final verdict grid.

**2026-09-20 (Shravan) — extraction from Shravan-procured PDFs (`~/Downloads/A9/`).**

*Result.* `extraction/population-age-structure-momentum-extraction-report.md` + updated CSV.
**10/16 now have extracted data** (6 numeric: A9-02/03/07/08/09/16; 2 qualitative: A9-05/10; 2 partial:
A9-11/15). A9-14 (India 1983) is a **scanned PDF → needs OCR**. **5 still to procure** (A9-01 China
2014, A9-04 Korea 2023, A9-06 SA 2019, A9-12 China 1991 PDR, A9-13 Mexico 1991). Three downloaded files
are **not A.9** and excluded: a China age-structure→*economic-growth* paper, a Korean old-housing→birth-
rate spatial paper (→ C.2.c), and Zeng Yi et al. *Genus* 1993 (parity decomposition; a different paper
than A9-12, which it cites — so A9-12 is real and still needed).

*Emerging synthesis signal.* The age-structure contribution to CBR/birth-count change is **large but
highly setting/period-dependent and signed both ways**: dominant in momentum-heavy transitions
(Hong Kong ~80%, South Africa +60%, China/India ~80–100% of growth), secondary where marriage/marital
fertility carry the decline (Malawi ~0–20%, Korea, China 2021), compensating/positive in the US GFR;
**zero by construction for period TFR / CCF** (A9-07 confirms). This is the per-outcome, per-setting
verdict the scope + TICK-080 anticipated — report the *distribution* of the composition share, not one
number.

*Next.* OCR A9-14; procure the 5 missing; pin exact numbers for A9-05/10/11; then stage 9.

**2026-09-20 (Shravan) — stage 9 quantitative synthesis (on 10/16; 6 unprocurable).**

*Result.* `output/tables/population-age-structure-momentum-synthesis.md`. 6 studies marked
`not_retrieved` (unavailable per Shravan); synthesis runs on the 10 in hand. **Not pooled** — the
estimands are decomposition shares across heterogeneous outcomes with opposite signs, so a `metafor`
number would be a category error (TICK-080 item 8 + non-effect estimand). Reported as the
distribution + moderators instead.

*Finding.* The age-structure share of an observed CBR/birth-count movement spans **~0–3% (Malawi, Korea)
to ~60–100% (South Africa +60%, Hong Kong ~80%, China/India momentum ~80–100% of growth)**, and is
**signed both ways** — negative where a shrinking/aging reproductive-age population coincides with
decline (Korea, China, HK), positive where a youthful/momentum-laden structure inflates or props up the
CBR (South Africa, China/India, US GFR compensation). Moderators: momentum/distance-from-stationarity,
window length, and whether marriage/marital fertility carry the change. **Zero by construction for period
TFR and CCF** (Chaurasia confirms analytically). The dispersion *is* the result — no central "A.9 effect."

*Next.* Stage 10 demsig (per outcome: CBR/births significant-but-setting-specific, both signs; TFR/CCF
zero by construction) → stage 11 GRADE (NOT RATEABLE) → stage 12 chapter draft (+ signed dot/range figure,
not a forest plot). TICK-080 formalization + Anup sign-off precede the final verdict grid.
