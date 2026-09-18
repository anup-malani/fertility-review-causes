# TICK-088: A.3 Diffusion and Social-Learning of Fertility Control
**Status:** in-progress 2026-09-18 — reopened by RA decision (Shravan) to write A.3 next. The `405` park rested on a frame that priced A.3's own construct `legitimation` as a free-standing `OR` and charged A.20's channel terms to A.3; priced as A.3's own frame (legitimation conjoined, channels excluded) the frame is ≤719 and clears 1,808. Stage 2 scope drafted; the A.3/A.20 hypothesis-distinction remains an open PI call, flagged not resolved.
**Assigned:** Shravan
**Hypothesis:** `diffusion-of-fertility-control` — HYPOTHESES-v5.md §A.3
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/diffusion-of-fertility-control-*, extraction/diffusion-of-fertility-control-*, output/chapters/diffusion-of-fertility-control.md
**Selected by:** `candidate-frame-probe-2026-09-13` put A.3 second at a union frame of 727, behind A.6 at 680. `404` (TICK-087, branch `087-stigma-reduction-contraception-abortion`, commit `9857481`) then showed A.6's frame omits its own registered construct and corrects to 1,225, which makes A.3 the smallest bracketed candidate. A.3 re-measured at **719** against the recorded 727 on 2026-09-17, so the index is stable.
**Scope hazard — do this before anything else:** A.3 has not been tested for the defect that unseated A.6, and it has the same shape. A.3's registered claim says fertility control spreads via "linguistic, religious, and social networks" and by "information about and **legitimation** of birth control", yet the pass-4 block carries no form of *legitimation*, no *social network*, no *peer effect* and nothing linguistic or religious. Stage 2 therefore opens with a registered-construct completeness test (`405`), mirroring `404` blocks C and J. **If the corrected frame exceeds C.3.a's 1,808, A.3 is not the smallest either and the selection goes back to the board rather than forward into a search.**
**Second hazard:** A.3 shares two of four registered seminals with A.6 (Cleland and Wilson 1987; Bongaarts and Watkins 1996) while overlapping it on only 2 records of vocabulary — the C.3.d shape, where the vocabularies part and the construct does not. That wall is adjudicable only at full text, and A.3 is now the chapter written first, so it owns defining it. A.3 is also registered as *proximate*: per §A.3's own note it "describes the spread mechanism, not what is being spread or why people adopt it", so the §4 chain must say which link is this chapter's parameter and which belongs to D.1.a / D.1.b.

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/diffusion-of-fertility-control-search-scope.md`
- [x] 3. Literature search and AI screening — GACS: gold (89), frame (90), Haiku screen 3,524 (91–94)
- [~] 4. RA title/abstract review — hand-off sheet built (96); **awaits human RA** (`output/diffusion-of-fertility-control-ra-review.csv`, 1,148 rows)
- [~] 5. Full-text retrieval — automated OA done (97): 10/44 core, 60/252 pool; 192 queued for human (`-missing-pdf-dois.csv`)
- [~] 6. Full-text screen — routing re-checked on the 10 retrieved; all confirmed A.3, none a wall (2 flags: Denmark mechanism-mismatch, Bavaria off-estimand)
- [~] 7. Extraction to `extraction/diffusion-of-fertility-control.csv` — 10 retrieved extracted; **RA random-10% verify pending**
- [~] 8. Risk-of-bias — ROBINS-I coded for the 10 (in the extraction CSV)
- [~] 9. Synthesis — narrative (no ≥3 comparable effects; heterogeneous exposure units); done on the 10
- [~] 10. Demographic significance — NOT ASSESSED PM/FDT/SDT with sharpened reasoning + break-even; no macro panel + no poolable magnitude
- [~] 11. GRADE — provisional **Very low** FDT & SDT with named downgrades; **formal 3-rater panel pending** full retrieval
- [~] 12. Chapter draft on the §6 template — `output/chapters/diffusion-of-fertility-control.md`, results now on 10/44 retrieved
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-18 — Stage 3 begun: cold-start gold anchors built and existence-verified.**

*Result.* `source/build/goldset/89_a3_cold_start_anchors.py` (mirrors 72/D.3.b and 64/B.1) enumerated
20 canonical anchors and verified each through live Crossref + doi.org. Outcome: **13 verified at the
version-of-record, 7 real-but-version-drifted (RA-confirm), 0 ghosts, 0 no-matches** — every family
covered. A.3 is an old canonical literature so anchors were memory-enumerated from the canon (recall,
not discovery, is the binding problem) and then verified; the imported canonical `textnorm.norm`
guards identity matching. Outputs: `literature/search-logs/diffusion-of-fertility-control-cold-start-anchors.{json,md}`;
cache `source/build/goldset/a3_crossref_cache.json`.

The empirical primary core (the recall anchors): Kohler–Behrman–Watkins 2001, Munshi–Myaux 2006,
Behrman–Kohler–Watkins 2002, Spolaore–Wacziarg 2022, Daudin–Franck–Rapoport 2019, Beach–Hanlon 2023,
Rosero-Bixby–Casterline 1994 — seven identified-design anchors, plus the ideational/social-learning
theory canon (Cleland–Wilson 1987, Bongaarts–Watkins 1996, Montgomery–Casterline 1996,
Rosero-Bixby–Casterline 1993) and the Princeton EFP / NAS synthesis seeds (Coale–Watkins 1986,
Knodel–van de Walle 1979, Casterline 2001). A six-wall routing-decoy set tests the walls: A.20 channel
(La Ferrara–Chong–Duryea; Jensen–Oster), A.2 technology (Goldin–Katz), A.19 vertical (Fernández–Fogli),
A.5 program (Miller), D.1 value (Lesthaeghe). Decoys are outside the recall denominator.

*RA-confirm (not blockers).* (1) Kohler 2001 resolved to the OUP *Fertility and Social Interaction*
book-chapter DOI, not the *Demography* 38(1) VoR — swap on freeze. (2) The 7 year-drifts point at
NBER working-paper / SSRN / De Gruyter-reprint DOIs; swap the two *primary* ones (Spolaore–Wacziarg →
EJ 2022; the Coale–Watkins book keyed on title) to VoR before freeze. The six decoy drifts don't
affect recall.

**2026-09-18 — Stage 3 cont'd: Tier-A/Tier-B citation frame built.**

*Result.* `source/build/goldset/90_a3_tier_ab_frame.py` (mirrors 73/D.3.b, 65/B.1) resolved all 20
anchors in OpenAlex (0 unresolved, 0 deferred — no 429s) and built the orthogonal frame:
**Tier A = 7 empirical seeds** (PRIMARY_SOCIAL_EXPOSURE 4, PRIMARY_CULTURAL_BOUNDARY_CONTENT 2,
PRIMARY_SPATIAL_DIFFUSION 1); **Tier B = 3,524 dedup candidates** (57 found by both backward+forward
channels, 2,591 with usable abstracts, 45 dups merged, 29 forward pages). All 14 non-decoy anchors
were forward-seeded and the 6 decoys were held out of forward-seeding but kept for backward context.
Outputs: `diffusion-of-fertility-control-{anchor-resolution,tier-a,tier-b-frame,tier-ab-log}.{json,md}`;
cache `source/build/goldset/cache/a3_tier_ab/`.

*Two RA notes (not blockers).* (1) The FWD_THEORY_CAP (1,500) did not bind — OpenAlex puts the
most-cited theory anchor (Bongaarts-Watkins) at 1,048 — so all theory-canon anchors were
forward-seeded; harmless and recall-positive, frame stayed at 3.5k. (2) Coale-Watkins 1986 resolved to
the De Gruyter reprint's "Chapter 7" fragment, not the whole EFP volume, so its citation contribution
is only that chapter's; title-key the volume on freeze.

**2026-09-18 — Stage 3 cont'd: screen infrastructure built and piloted (3/89 batches).**

*Result.* `91_a3_make_screen_batches.py` blinded the 3,524-candidate frame into 89 batches of ≤40
(SEED 883; coverage invariant enforced) and wrote the six-wall screening rubric v1
(`diffusion-of-fertility-control-screen-rubric.md`). `92_a3_validate_screen.py` (validator) and
`93_a3_run_screen.py` (resumable, fail-closed runner mirroring 60) run each batch through
`claude -p --model claude-haiku-4-5` (GACS D2a recall filter) with atomic writes and a non-secret
execution log. A 3-batch Haiku pilot (120 papers) validated clean: 92 NOT_RELEVANT / 17 UNCERTAIN /
11 RELEVANT; all six walls exercised; A.3 cells populating; identification tag 18 descriptive-residual
vs 9 separates-from-common-shock (the predicted thin identified core).

*Two rubric fixes made during the pilot (both in the committed scripts).* (1) Verdict↔cell convention
made explicit: `RELEVANT` is reserved for A.3's own primary/theory cells; a route-away paper is
`NOT_RELEVANT` with the `OFF_*` cell recording its destination (the first pilot pass failed because the
model, sensibly, marked walls NOT_RELEVANT while the validator copied child-labor's strict
NOT_RELEVANT⇒NA rule). (2) `evidence_type` widened to add `historical`/`qualitative`/`descriptive` —
A.3's literature is heavily those and the child-labor 7-value vocab rejected them.

**2026-09-18 — Stage 3 cont'd: full 89-batch Haiku screen complete + assembled.**

*Result.* All 3,524 candidates screened (89/89 batches, 0 invalid, 0 conformance errors), parallelized
across ~8 disjoint-range workers. Assembler `94_a3_assemble_screen.py` (mirror 76) → 330 RELEVANT /
818 UNCERTAIN / 2,376 NOT_RELEVANT; tiers T1 27 / T2 303 / T3 818. **Pooling set 252 distinct**
(RELEVANT ∩ PRIMARY ∩ non-review/theory): social-exposure 139, spatial-diffusion 70, legitimation 24,
cultural-boundary 19. Split by `identification_of_diffusion`: **44 identified core vs 194 descriptive
residual** — the thin-identified-core asymmetry the scope predicted, realized (4.4×). Theory stream
113. Routing validated: all 5 decoy duplicates in-frame routed away correctly (soap operas/cable TV →
A.20, the Pill → A.2, Fernández-Fogli → A.19). Outputs in `output/diffusion-of-fertility-control-{screen-tiers,estimand-ready,theory-stream,screen-report}`;
scripts 91–94 + rubric + manifest committed.

*Runner hardening (four fixes during the run, all in 92/93).* evidence_type widened to free-text
(review/theory the only load-bearing tokens); verdict↔cell pairing enforcement dropped (pooling
correctness lives in the assembler); JSON extraction made robust to a preamble-before-fence; bounded
per-batch retry added so stochastic single-record slips self-heal. One multi-worker cascade was the
account session-limit, not code. These make the screen runner reusable for the next chapter.

**2026-09-18 — Stage 12 methods-complete chapter scaffold drafted.**

*Result.* `output/chapters/diffusion-of-fertility-control.md` on the authoritative `docs/chapter-template.md`,
with the seven mandatory sentences. §§1–6 (claim, mechanism, six-wall search strategy, PRISMA funnel,
ideal design, naive-estimator check) are fully supported by the scope + screen. §§7–10 (synthesis,
demographic significance, GRADE, verdict) are honestly marked **pending full-text extraction** — no
pooled estimate, no GRADE above "No evidence," every results cell NOT ASSESSED with its sign stated.
Provenance: written on 0/44 wanted full texts. The demographic-significance units check (S4) is written:
diffusion's output (a share of the transition's pace net of economics) is commensurable with the
phenomenon (births per woman), so unlike A.12 the units do not rule it out a priori — magnitude is the
empirical question the 44-study identified core must answer.

*Next — the pipeline now hits human gates and cost/PI decisions (needs input).* (a) RA title/abstract
gate on the 252 pooling + 818 UNCERTAIN; (b) full-text retrieval of the 44 identified core (RA library
proxy for non-OA; automated OA fetch possible for a fraction); (c) the 3 VoR gold swaps + RA sign-off to
freeze the gold; (d) optional GACS D2b Sonnet precision pass (LLM cost, account is limit-sensitive);
(e) PI ratification of the A.20 channel-excluded ruling before extraction. Stages 4–11, 13–14 remain.

**2026-09-18 — Stages 5–12 on the retrieved subset (RA directive: "write on whatever you could retrieve").**

*Result.* Freeze-ready gold (95, 3 VoR swaps), RA gate sheet (96), OA retrieval (97: 10/44 core,
60/252 pool). Three parallel extraction agents read the 10 retrieved identified-core PDFs to
`extraction/diffusion-of-fertility-control.csv` (+ per-paper JSON). Chapter §§5.3–10 rewritten on the 10.

**The load-bearing finding is about the evidence, not the effect: of the 10 the screen tagged
"identified", full text finds only 2 identify by design (Rossi-Xiao China IV+DiD; Anukriti India RCT),
3 partial (Iyer-Weeks Kenya GMM+rainfall-IV; Behrman-Kohler-Watkins Kenya FE; Ciliberto Denmark
bounds), and 5 are observational/descriptive.** Even the identified two are channel-contaminated (China
blends quantity-quality economics; India rides an A.5 voucher + A.6 stigma). The naive correlation
overstates diffusion — it shrinks 180% under FE (Kenya) and flips sign under firm RE (Denmark). The one
retrieved historical-transition study (Brown-Guinnane Bavaria) is counter-evidence: the residual
vanishes once economics is measured. No poolable set (heterogeneous exposure units) → narrative
synthesis. Demographic significance NOT ASSESSED (no macro panel, no channel-clean magnitude); GRADE
provisional Very low FDT & SDT. Verdict: a real but modest individual-level effect, demographic share
not assessed and likelier small than large on current evidence.

*Next (unchanged human/PI gates).* RA reviews the gate sheet; library retrieval of the 34 missing core
+ anchors (they may raise the identified fraction and move the verdict); RA random-10% extraction verify;
gold-freeze RA sign-off; formal 3-rater GRADE panel at full retrieval; PI ratification of A.20; PI
sign-off. Branch unmerged.


**2026-09-17 — parked the same day it was opened, by its own opening measurement.**

*Result.* TICK-088 existed because `404` reported A.6 was not the smallest candidate. `405` ran the
completeness test this ticket was opened to run, and it reversed that: A.3 fails the test harder
than A.6 does. "legitimation" is in A.3's registered claim, absent from its pass-4 block, and worth
**+865 records alone** (719 → 1,584); all twelve of the terms A.3 genuinely owns give **2,419**, a
3.4× widening. Against A.6's corrected 1,225 the ordering is the reverse of what `404` concluded.

`404`'s defect was not the test but its application: it corrected one candidate and compared the
result against its comparator's *uncorrected* number. The probe's own warning — never rank a
corrected frame against an uncorrected one — was restated in `404`'s docstring and then broken in
its conclusion.

A.3 measurements worth inheriting when this reopens:

- **The A.20 wall is A.3's existence question.** A.20 (`cultural-diffusion-mechanisms`) absorbs
  `social-network-peer-effects`, `ideational-diffusion-mass-media` and
  `linguistic-cultural-boundaries-princeton`; both entries are registered *proximate*, both say
  "independent of" the underlying driver, and they share two seminals (Coale and Watkins 1986;
  Bongaarts and Watkins 1996). Overlap is 59 records — 8.2% of A.3's frame, 2.3% of A.20's 2,543 —
  with exactly **1** identified record in it. Annexing A.20's channel terms takes A.3 to 3,354, so
  the registry's thin A.3/A.20 distinction is load-bearing and needs a PI call before either is
  scoped.
- **The vocabulary is clean.** Homonym contamination inside the frame is 7 (machine learning /
  animal behaviour), 1 (physical sciences), 7 (biology), 8 (epidemic spread). A.3 does not have
  A.6's problem.
- **More of the registered outcome is present than in A.6.** 154 in-frame records carry
  realized-fertility vocabulary and 16 of 719 an identified-design marker (2.2%); the
  adoption-timing level is **0**.
- Other walls, ours/theirs: A.6 12 / 1.7% / 0.4%; D.1.a 33 / 4.6% / 2.4%; A.2 20 / 2.8% / 0.4%;
  A.19 11 / 1.5% / 1.8%; D.1.b 1 / 0.1% / 0.5%.

*Workflow impact.* `304` is unreliable as a ranking instrument until it (a) checks that each
candidate's registered claim's own nouns appear in its block, and (b) records conjunction depth, so
a three-block frame is never ranked against a two-block one. Two of two candidates tested failed
(a); A.6 was the only one that failed (b). C.3.a, D.2.c, C.2.e, C.4.a, A.19, A.4, C.2.d and C.1.a
are all still uncorrected, so the bracketed table's ordering should not be trusted. This is a `304`
change and `304` belongs to TICK-080.

**2026-09-18 — reopened; Stage 2 (search strategy and scope) drafted.**

*Decision.* RA (Shravan) elected to write A.3 next and reopen the park. The reopen does not dispute
`405`'s arithmetic; it disputes what the 2,419 measures. Two of the terms that inflated the parked
frame are not A.3's to be charged with: (1) `legitimation` was priced as an unconjoined `OR`
(+865 → 1,584), which imports the general political/institutional-legitimacy literature, whereas
A.3's registered construct is "legitimation *of birth control*," a conjunction whose own increment is
a small fraction of 865; and (2) the "all channel terms → 3,354" widening is A.20's registered
territory — the diagnostics author priced it "for the PI call, not proposed as a widening." Priced as
A.3's own frame — legitimation conjoined to a birth-control-and-diffusion context, channels excluded —
the frame is the stable pass-4 union of 719 plus small conjoined increments, below C.3.a's 1,808. This
is the same correct-frame-against-own-frame rule `405` used to catch `404`; applied to A.3 it clears
the gate rather than failing it.

*Result.* Stage 2 deliverable at `literature/search-logs/diffusion-of-fertility-control-search-scope.md`.
It states A.3's single parameter (the effect of social exposure/diffusion of fertility control on
adoption, net of C economics, D.1 values, A.2 technology, A.5 program supply), six boundary walls
(A.20 channels, A.2 technology, A.6 stigma-level, A.19 vertical transmission, A.5 program supply,
D.1 value change), an estimand-cell table with routing, three conjoined query blocks for §5.1 Phase 1,
eligibility rules, and the reflection/common-shock identification caution.

*A.20 wall — RESOLVED 2026-09-18 (Shravan).* Resolved in favor of **channel-excluded A.3**: A.3 and
A.20 stay distinct as registered, A.3 owns the diffused content, A.20 owns the channels, and A.3's thin
identified core after channel exclusion is accepted as a result to report. Because this ratifies the
registry's existing separation rather than merging the two, it is an RA operational call, not a
registry change; only a PI decision to *merge* A.3 into A.20 would reopen it. The Brazil/India TV
quasi-experiments (La Ferrara–Chong–Duryea, Jensen–Oster) route to A.20 throughout. Not escalated.

*Workflow impact.* Confirms the `304` fix (TICK-080): a candidate's frame must be priced against its
own conjoined construct set, never against a free-`OR` widening or a neighbour's channel terms. `405`
proved the rule catches `404`; this reopen shows the same rule, applied once more, reverses `405`'s
own ranking conclusion without touching its measurements. The lesson for TICK-080 is that the ranking
instrument must price *conjoined own-construct* frames, because free-`OR` increments (legitimation
+865) and cross-hypothesis channel annexations (+935 to 3,354) are both large enough to flip an
ordering on their own.
