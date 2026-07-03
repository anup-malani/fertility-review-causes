# Evaluating GACS on the OAS Pilot

**Companion to:** `canonical-search-workflow.md` (the Gold-Anchored Clustered Search methodology)
**Author:** Shravan (RA)
**Status:** draft (2026-07-02) — for PI review
**Testbed:** old-age-security / pension-crowdout of fertility (chapter C.3.c), the pilot hypothesis

---

## 1. What this evaluates, and the honest caveat up front

This document asks a single question: **does GACS do what a systematic-review search method is supposed to do** — recover the relevant literature, at a defensible and *measured* recall, at a cost we can pay across ~all the review's hypotheses — and where does it break?

The central caveat frames everything below. **GACS has been validated in its components, not yet as one end-to-end production run.** Three separate exercises stand in for a full run:

1. a **10-fold cross-validation dry run** of the query calibration (Part 4), on the *un-frozen* gold set, with *title-only* matching (a deliberate conservative lower bound);
2. a **tier-logic instantiation** on the *existing* PI corpus (a demonstration of the output stage, not the production query's output); and
3. an **actual Phase-E run on the OAS corpus** (the legacy-migration path) that produced the two shippable artifacts — the DOI list and the PDF folder.

No single run yet goes gold-freeze → tuned query → fresh screen → tiers with the real OpenAlex budget wired in. So the numbers here are **directional evidence that the design works**, not a final performance certificate. Reading them as "GACS recovers 71% of the literature" would over-claim; reading them as "each load-bearing part of GACS demonstrably pulls its weight, and we can see where the residual risk sits" is right. Closing this gap is what Part-4-full and a second-hypothesis replication are for (§7).

## 2. Does it recover what it should? — Recall

The measurement instrument is the frozen gold set: **303 anchor studies** (Tier A = 56 empirical-core + theory-canon; Tier B = 247 unbiased orthogonal sample), against which the calibrated query's recall is cross-validated out-of-sample.

**Headline CV result (dry run, title-only, un-frozen gold):**

| Query | CV recall | Recall(A) | Recall(B) | A − B |
|---|---|---|---|---|
| Backbone only (Nf=Np=0) | 56.4% | 51.8% | 57.5% | −5.7% |
| Best breadth (Nf=Np=30) | **70.6%** | 62.5% | 72.5% | **−10.0%** |

Three things this establishes, and one it warns about.

**(a) The gold-mined breadth extension buys real recall.** Moving from the leakage-free external backbone alone to the CV-tuned breadth vector lifts recall ~56% → ~71% — a **+14-point** gain, purchased by exactly the OAS-theory vocabulary the policy-review backbone lacked (`intergenerational transfers`, `payg`, `value of children`, broader `child*`). This is the method's core bet — that fold-local discriminative-term mining adds recall a fixed external string can't — and the CV surface confirms it, saturating around N≈20–30. Because the mining is **fold-local** (terms harvested only from the training fold's gold, recall measured on the held-out fold), the gain is not the circular self-recall that mining-and-measuring on the same papers would produce.

**(b) Recall(B) is the honest primary estimate, and A−B is a working diagnostic — which fired.** Under the def-1 unbiased Tier B, **Recall(B) ≈ 72%** is the headline. The **A−B gap is the vocabulary-bias diagnostic**: it asks "is the query inflated toward the keyword-sourced papers?" The dry run produced a genuine, useful surprise — **the sign flipped negative** (Recall(A) < Recall(B)). Tier A now carries the Part-1c theory canon (Ehrlich–Lui, Boldrin–Jones), whose *titles* lack surface fertility/pension vocabulary, while the def-1 Tier B is keyword-richer. So the query does **not** over-fit to keyword-reachable work; if anything it slightly *under*-recalls the abstract theory tail. That the diagnostic can detect and sign the direction of vocabulary bias is itself evidence the instrument works.

**(c) The calibration is a genuine allocator, and it overturned a prior belief.** The per-block miss diagnostics said the **fertility block binds, not the pension block** (~50 vs ~25 held-out misses at the frontier) — the *opposite* of the Part-3 prior that pension was the thin block. The reason is substantive: much relevant work names the outcome as *children / sons / value of children / family size*, not *fertility / birth*. GACS caught this because the CV *measures* where recall leaks instead of guessing — precisely the upgrade over a single hand-built query.

**(d) Warning: this is a title-only lower bound.** Matching on titles alone ceilings around ~70% and saturates by N≈30; abstract matching (deferred to Part-4-full) should lift it. So 71% is conservative, but it is also **un-frozen and un-abstracted** — the number will move in both directions when the gold freezes and abstracts come in. Do not quote it as final.

## 3. Does the architecture earn its parts?

The design claim is that three contributed refinements each harden a distinct leg of Anup's skeleton. Each shows a measurable payoff on the pilot.

**The orthogonal snowball earns its place — visibly.** The tier instantiation surfaced canonical OAS papers the **keyword channel entirely missed**, held in the single-channel-snowball bin: *Children as a Form of Retirement Saving* (Chile), *Does Pension Privatization Increase Fertility?*, *Old-age support and fertility in rural China*. An intersection-based scheme drops these; GACS's union + channel-convergence tiering keeps them **and** ranks them as confirmed-relevant. That these same papers are our hardest gold residuals is independent corroboration they are real, relevant, and keyword-unreachable — i.e. exactly the recall the snowball exists to buy. This is the single most convincing piece of evidence in the pilot.

**The clustering + CV leg earns it** via the fertility-block-binds finding (§2c): structure-and-measure beat guess, and redirected breadth budget to where recall actually leaked.

**The measurement leg earns it** by making every other claim in this document *quantified* rather than asserted. Without the frozen gold there is no recall number, no A−B diagnostic, no saturation stop calibration — the method would be a search with no way to know how much it missed.

**The tier logic behaves as designed.** Verdict-gated, convergence-tiered, with `compositeScore` demoted to intra-tier sort: on the existing corpus this yielded Tier-1 = 83 (17 gold + 66 multi-channel) and a strongest-inputs set (T1∪T2, score ≥ 7) of 69 — comparable to Anup's Tier-1 of 74, i.e. it reproduces the PI's high-precision core while additionally *labelling why* each paper is in it (gold / K∧S / single-channel).

## 4. What it costs

The evaluation has to price the method, because it runs ~once per hypothesis across the whole review.

- **OpenAlex is the binding budget.** A hard daily request/$ cap governs enrichment, resolution, and snowball. It was **exhausted twice** during Task-A construction, and the search endpoint was **anonymously rate-limited** during the pilot's PDF acquisition. This is the real scaling constraint — hence the substrate mandate: project-level persistent cache, resumable stages, a hard per-run budget cap with graceful resume, and a **free OpenAlex API key** to lift the anonymous rate limit.
- **LLM screening is cheap and controlled.** The Haiku→Sonnet cascade is a cost-*control* (Haiku recall-filters so Sonnet runs only on survivors), landing at ~tens of dollars per hypothesis — not the binding cost.
- **RA time is the other real cost**, concentrated in the uncertain band (the 52 Tier-B UNCERTAINs still awaiting adjudication; Tier-A sign-off). The design minimizes it deliberately (RA is the verdict gate on boundary cases only), but it does not eliminate it, and it is the reason the gold is not yet frozen.

## 5. Where it is fragile — limitations, stated plainly

This is the Shapiro–Gentzkow "honest treatment of limitations" section, and it is the most important one.

1. **OpenAlex W-ID rot is severe and structural — and it corrupts *content*, not just IDs.** ~40% of the snowball frame is title-keyed because its W-IDs are dead or drifted (OpenAlex merges works and reassigns IDs over time). Set-arithmetic across corpora built at different times understates overlap; `cites:<dead-id>` silently loses forward edges. **Mitigation applied:** re-key everything on DOI; retain unresolvable papers title-keyed (dropping them would bias recall toward findable work). **Residual risk, now quantified and cleaned.** A targeted web hunt over the 19 no-DOI dead-WID studies in the meta-analysis-ready set found only **3 genuinely new retrievable papers**; **8 corrupted-title duplicates of studies already in the set** (one underlying paper, Shen et al. 2020, appeared under *six* mangled titles); and **8 phantom entries with no real paper behind them**. The drift corrupts *titles and settings together* — "Austria" was really Brazil, "Rural China" was Namibia, "Ecuador" was Mexico — and, in the tell-tale case, *content too*: the one phantom that carried an abstract (a "New Pension in Turkey" study) turned out to have an **organic-chemistry abstract** mis-joined onto it. Seven of the eight phantoms are **forward-citation** records with no abstract and no web footprint — the classic signature of a hallucinated citation ingested upstream (LLM-fabricated reference lists → OpenAlex → the snowball), not a paper our pipeline invented. After RA adjudication the 8 duplicates were merged and the 8 phantoms dropped, taking the pilot's distinct-study count **60 → 44**. This is the single most important data-quality finding: the title-keyed snowball tail was ~30% junk (duplicates + ghosts), so DOI-keying, an *abstract-or-live-DOI* gate, and a **harder cap on forward vs. backward citations** (7 of 8 ghosts were forward; the lone backward one was real) are not optional hygiene — they are load-bearing for both the study counts and the Tier-B recall denominator.
2. **The baseline corpus had corrupted DOIs — a specific, pinned bug.** ~47% of phase-2 snowball records carried a mis-joined DOI (the DOI *column* was shuffled onto the wrong record; titles and W-IDs stayed correct). Not LLM hallucination — a join bug in `snowball-citations.mjs` Phase 2b. **Mitigation applied:** W-ID refetch produced 275 title-verified corrections; a propose→Crossref-verify→RA-adjudicate resolver, scoped to Tier A and banned for Tier B. **Residual risk:** this needs a PI data-hygiene ticket to fix at the source; until then every downstream corpus inherits it.
3. **Tier B is less keyword-biased, but not perfectly independent.** The snowball that feeds it was seeded off the (keyword-sourced) PI relevant set. So Recall(B), while the honest primary, still rests on a not-fully-orthogonal sample — and the hard-tail recall bound built on it is correspondingly *optimistic*. Stated wherever the number is reported.
4. **The gold is not frozen.** 52 Tier-B UNCERTAINs await RA adjudication and Tier-A needs sign-off. Every recall figure above is therefore provisional by construction. Auto-dropping the UNCERTAINs is explicitly forbidden (it would reintroduce findability bias), so this is RA work, not a script.
5. **PDF acquisition walls are now diagnosed, not guessed.** After cleaning, **44 distinct studies** remain, of which **28 have a PDF** (open-access copies, including working-paper versions of paywalled published articles, 2 recovered by the web hunt). The 16-study retrieval residual is now honestly typed: **15 paywalled-published** (real DOIs, no green-OA copy → institutional-proxy pull) and **1 verified-real working paper** (Ghana) whose OA host was transiently down. Two diagnostic points earned along the way: (a) the no-DOI papers were first suspected to be a rate-limit artifact — paying for a working OpenAlex key (and cross-checking Crossref) proved instead a genuine **identifiability ceiling**, so "unresolvable" must be tested against an unthrottled channel before it is believed; and (b) the one Crossref title that crossed the J≥0.80 gate was a *false* match to a different paper, vindicating the C2 threshold + independent-metadata rule. Net: the obtainable-vs-paywalled split is measured, and the study set no longer carries the 16 dup/ghost entries that made it look larger than it is.
6. **Title-only dedup has a version-variant blind spot — found and patched.** The distinct-study collapse originally keyed on normalized title alone, which silently kept two working-paper/published pairs as separate studies (a hyphenation variant, and a WP whose title was a subtitle-extended version of the journal title). Caught on manual review; fixed with hyphen-normalization + a conservative author+year+title-containment merge (62→60 studies). A reminder that automated dedup needs a human eyeball on the headline count.
7. **Single-hypothesis evidence.** Everything here is OAS. The method is *designed* to generalize (constant effect-core + swappable cause-clusters, data-derived cluster count, the unified stop principle), but generalization is a claim, not yet a result. One more hypothesis — ideally a well-studied one with prior meta-analyses to exercise the cold-start bootstrap — is what would convert it.

## 6. Net assessment

On the pilot, **GACS's load-bearing design choices each show a measurable payoff**: the orthogonal snowball recovers canonical keyword-unreachable papers and the tiering surfaces rather than buries them; the CV calibration measures where recall leaks and reallocated breadth correctly (overturning a wrong prior); the frozen-gold instrument is what makes any of this a *number* instead of an assertion; and the A−B diagnostic can detect and sign vocabulary bias. Recall of ~72% (Recall(B), conservative title-only lower bound) with a negative, well-understood bias correction is a credible early result for a first calibrated run.

The honest counterweight: the strongest numbers come from a **dry run on un-frozen gold and a demonstration on the legacy corpus**, not a single production run; the corpus substrate (W-ID rot, the DOI-shuffle bug, ~half of Tier B title-keyed) injects real noise the method *manages* but has not *eliminated*; and it is all one hypothesis.

**Verdict:** the architecture is sound and the pilot supports it, but the performance claim should be stated as *validated-in-components, pending-a-clean-production-run-and-a-freeze*, not as a finished benchmark.

## 7. What would raise confidence (in priority order)

1. **Freeze the gold** — RA-adjudicate the 52 Tier-B UNCERTAINs and sign off Tier A. Everything downstream is provisional until this happens.
2. **Part-4-full** — wire the real `openalex_universe()` budget, add abstract matching, refit at the chosen breadth on the frozen gold, and produce the actual production query. Converts the dry-run recall into a real out-of-sample estimate.
3. **One clean end-to-end production run** on OAS (freeze → tuned query → fresh screen → tiers), replacing the component stand-ins with a single number chain.
4. **Second-hypothesis replication** exercising the cold-start bootstrap (a well-studied hypothesis with prior meta-analyses), to convert "designed to generalize" into "generalizes."
5. **PI data-hygiene ticket** — fix the phase-2 DOI-shuffle at source and adopt DOI re-keying corpus-wide, so future hypotheses don't inherit the noise.
6. **Finish the PDF acquisition** with the free OpenAlex + Semantic Scholar keys, to replace the current OA-only split with a true obtainable-vs-paywalled accounting.

---

*Inputs: `*-cv-breadth-dryrun.md` (Part 4 CV), `*-tiers-summary.md` (tier instantiation), `*-tier-b-summary.md` (gold Tier B), `*-part3-term-sourcing-summary.md` (term sourcing), `*-gold-set-build-log.md` (Parts 1–4 + Phase-E run), `*-metaanalysis-doi-list.md` and the PDF manifest (pilot outputs).*
