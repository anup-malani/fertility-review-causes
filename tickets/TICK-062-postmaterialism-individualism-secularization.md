# TICK-062: D.1.a Postmaterialism, Individualism, and Secularization
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `postmaterialism-individualism-secularization` — HYPOTHESES-v5.md §D.1.a
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/postmaterialism-individualism-secularization-*, extraction/postmaterialism-individualism-secularization-*, output/chapters/postmaterialism-individualism-secularization.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/postmaterialism-individualism-secularization-search-scope.md` (DRAFT, not frozen; Rulings 2 and 3 need PI sign-off)
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/postmaterialism-individualism-secularization.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
- 2026-08-04 (Shravan/Claude): **C1 production pull started and PAUSED on OpenAlex budget. Five of
  six clusters complete; 11,425 distinct records so far. Resumes on a re-run after the budget
  resets (~23h).** `{slug}-live-corpus.json`, `{slug}-live-search-log.md`; script
  `103_d1a_live_search.py`. **Nothing downstream should start until this reads complete.**
  **(1) A6c's provider recommendation was WRONG and is corrected in the same breath as acting on it.**
  It recommended Semantic Scholar bulk search. Feeding OpenAlex the full cluster query returned
  *"Wildcards (* or ?) require the exact (no-stem) field. `title.search` is stemmed"* — which
  reverses all three premises. **No wildcard expansion is needed** (`childless` and `childlessness`
  both return 2,586, one postings list; the earlier "no prefix matching" reading was measuring
  `fertilit`, which is not a word and stems to nothing). **The whole cluster query fits in one
  request** (two comma-joined filters, 67 OR'd terms), so the 123-narrow-query cost model was
  fiction. And decisively, **S2's counts are title-AND-abstract while the CV selected on title-only
  recall** — 498,007 against 18,123, a 19–39x gap per cluster. Running C1 on S2 would have pulled a
  differently-defined corpus and reported a recall figure that no longer described the query in use.
  **Same trap the OAS chapter documented in `43_live_search.py`.** Caught by a provider's error
  message, not by any metric of ours.
  **(2) State: S1 330/330, S2 841/841, S3 3,058/3,058, S4 2,221/2,221, S5 445/445 complete;
  GENERIC_VALUES 5,000/11,228.** Union 11,425 distinct after DOI-first then title dedup, with 6,698
  records collapsed as cross-cluster overlap — which is the sole-credit structure A6b predicted,
  observed live.
  **(3) Live gold recall is NOT reportable yet and the log says so in a banner.** Current figures
  (B-only 74.0% against the CV's 92.1%) are depressed by the missing 45% of GENERIC_VALUES —
  **the cluster A6b found carries the most sole credit, 176 gold papers no other cluster reaches** —
  so the shortfall is far larger than its record share suggests. Quoting 74% as a result would be
  the truncated-pull-reads-as-complete failure this chapter has now hit five times.
  **(4) Two bugs in my own error handling, both in the direction of looking finished.** First,
  `BudgetExhausted` propagated out of the cluster loop and **discarded the 5,000 records already
  pulled**, and left the failed cluster out of the per-cluster table entirely — so the report showed
  five complete clusters and no row for the one that failed. Union was 6,686 and B-only recall 41.7%;
  after preserving partials, 11,425 and 74.0%. Second, the budget body and a true rate limit share
  HTTP 429, and only the latter is worth retrying — "Insufficient budget" will not clear by waiting
  (`retryAfter` 82,182s ≈ 23h), so it is caught as STOP-AND-RESUME rather than slept on.
  **(5) Resume path: re-run `103_d1a_live_search.py`.** Every page is cached under
  `source/build/goldset/cache/d1a_live_search/`, so completed work costs nothing and the run
  continues at GENERIC_VALUES page 25. Roughly 32 further requests are needed (~$0.03).
- 2026-08-04 (Shravan/Claude): **A6c complete. Production query compiled and frozen; C1 must move
  off OpenAlex.** `{slug}-production-query.json` (C1 consumes this), `{slug}-recall-probe.md`;
  script `102_d1a_production_query.py`. **Phase A is finished — the next stage is C1, the clustered
  keyword search.**
  **(1) Local recall, reported in halves because a single figure would be misleading here.**
  Title-only **91.7%**, title-and-abstract 93.9%. But abstract coverage is 50% and is *not* missing
  at random — providers hold abstracts for well-indexed Anglo-European journals and not for the book
  chapters, regional journals and dissertations in this frame's residue. Split: records **with** an
  abstract go 94.4% → **99.4%**; records **without** stay at **89.8%**. The pooled 93.9% is entirely
  the covered half's behaviour attributed to the whole. **89.8% is what the operationalisation can
  actually promise on the records the search will find hardest**, and that is the number to quote.
  **(2) THE FINDING THAT DECIDES C1: the query's wildcards are not portable, and both providers fail
  silently.** Measured, not assumed. **OpenAlex `title.search` has no prefix matching at all** —
  `fertilit` returns **63** records against **114,008** for `fertility`, and `religio` returns 2,041
  against 16,941 for `religiosity`. Every stem in the query (`fertilit*`, `childless*`, `religio*`,
  `childbear*`, `procreat*`) would have retrieved a small biased fraction **and reported a plausible
  count while doing it**. Fourth instance of this chapter's signature failure mode.
  **(3) The same bug in my own encoder, in the same silent direction.** The S2 term encoder emitted a
  *quoted* stem, which Semantic Scholar reads as an exact phrase with a meaningless trailing star:
  **137** records where unquoted `fertilit*` returns **385,352** (correctly more than the bare word).
  A production pull built on it would have been wrong by three orders of magnitude without erroring.
  Neither provider supports a *phrase* prefix, so the wildcard is dropped from **26** multi-word
  terms — concentrated in S4 and S5, so **the two clusters A6b flagged as earning almost no credit
  are also the two most degraded by this limit**, which sharpens rather than answers that question.
  **(4) Neither provider takes the query whole, and the draft recommendation was wrong.** This script
  was written expecting to recommend "send the conjunction to S2 in one request" — the attempt
  returned **HTTP 400, request line 5,309 bytes against a 4,094 ceiling**. OpenAlex is barred
  separately by the five-operator throttle. So the decision turns on the **decomposition unit**, and
  there the gap is decisive: **OpenAlex needs one metered request per term (123, a floor counting one
  page each, ≈$0.12 for first pages alone); Semantic Scholar needs one free request per cluster (6).**
  **(5) Recommendation, with two conditions.** Run C1 on **Semantic Scholar bulk search**, decomposed
  by cluster and unioned client-side, keeping OpenAlex for targeted count checks. **The S2 API key,
  outstanding since the D.3.b snowball, is now on the critical path rather than a convenience** —
  unauthenticated throttling is the only thing between this plan and a completed pull. And **the
  compiled query must be emitted with wildcards expanded before C1 consumes it**; the artifact still
  carries stems, and a consumer that passes them through reproduces the failure in (2).
  **(6) Cluster universe counts (S2, corrected encoding):** GENERIC_VALUES 343,368; S3 57,144;
  S4 41,291; S2 32,846; S5 15,636; S1 7,722. Sum 498,007 as an **upper bound only** — cluster overlap
  is unmeasured without pulling identifiers, and the sum is labelled as a bound rather than a
  universe size.
- 2026-08-04 (Shravan/Claude): **A6a and A6b complete. Query breadth chosen at (20, 10);
  Recall(B-only) 92.1%, all three Tier-1 natural experiments retrieved.**
  `{slug}-discriminative-terms.{json,md}`, `{slug}-cv-breadth.{json,md}`; scripts
  `100_d1a_discriminative_terms.py`, `101_d1a_cv_breadth.py`. Next is A6c, the production-query refit
  and the live universe counts.
  **(1) The treatment side is six clusters, not one block, and A6a says why.** Ruling 1 makes this
  five treatments against one outcome, so a single mined cause block would have been ranked by
  whichever pair dominates the frame. Measured: **S3 has 28 mineable terms (top z 16.6), S1 has 5,
  S2 has 2, and S4 and S5 have zero.** The sixth cluster is `GENERIC_VALUES`, the treatment-side
  vocabulary that retrieves on-pair work without naming a pair. **It carries more sole credit than S3
  at A6b — 176 against 149** — so a query built only from pair-specific clusters would have been an S3
  query and would have lost roughly a third of the frame. That is the run's most consequential number.
  **(2) Ruling 2 confirmed mechanically by an independent measurement.** S4's zero is not sparsity:
  *every* childlessness term in the ranked set classifies as `OUTCOME` or `BOTH` and none as a pure
  treatment term, because there is no S4 treatment word that is not also the outcome word. The
  degenerate-pair rule was pre-registered in the scope; the term ranker rediscovered it without being
  told. Belongs in the chapter's methods section.
  **(3) A pipeline-ordering bug of my own making, and it inflated four downstream numbers.** `98_`
  deduplicates on the raw snowball title, then enrichment rewrites titles to the provider's canonical
  form — so records that were distinct strings at dedup time become the same work afterwards. **95 of
  495 Tier-B records were duplicates**: case variants, British against American spelling, a book
  indexed once with and once without its author suffix. Tier B is **400 distinct works**, not 495. It
  inflated the Tier-B count, the A6a positive class, the A6b recall denominator, **and the round-2
  saturation yield** — round 2's 1.77 per 50 is overstated by roughly the duplicate share, though not
  enough to change the stop decision, which the depth cap governed anyway. Catchable only after
  enrichment, because before it the two strings genuinely differ.
  **(4) The CV read its own misses and found four omissions from a-priori scope vocabulary** — not
  four discoveries in the data. `baby boom` was **costing a Tier-1 natural experiment** ("Religiously
  inspired baby boom: evidence from Georgia"); `reproductive success`, `postindustrial`, and the whole
  non-English outcome vocabulary were missing too. **The multilingual repair exposed a second bug: the
  normalizer deleted every non-ASCII character, so `fécondité` became `f condit` and the French and
  Spanish terms could never have matched** — the repair would have silently done nothing while
  appearing to be in place. Diacritics are now folded, not deleted.
  **(5) Stated against my own number: Recall(A-only) is no longer out-of-sample.** The repairs were
  informed by A-only misses, so its 68.4% → 89.5% jump is partly fitted and should not be quoted as a
  clean number. **Recall(B-only) moved 91.6% → 92.1%, half a point** — and that is the reassuring
  part, because a repair that gamed the metric would have lifted both. All three Tier-1 design anchors
  now retrieved; S3 100% of 23, S1 80% of 5, S5 50% of 2.
  **(6) The materialism vocabulary trap is a ROUTING problem, not a retrieval one — reversing A6a's
  decision.** A6a withheld bare `materialism` because Inglehart's materialist (S1, security) and the
  consumer-psychology materialist (S5, acquisition) are opposite poles. But both senses are in scope,
  since S1 and S5 are both D.1.a pairs, and the query is a conjunction with the outcome block, so it
  can only retrieve materialism papers already about fertility. Withholding it cost the one
  unambiguous S5 anchor in the gold set. Restored; the disambiguation belongs at extraction from the
  measure's item content, where the generic-values routing already happens.
  **(7) An open cost to re-examine at A6c.** S4 earns **zero** sole credit and S5 earns one. The
  forced backbones return almost nothing on the current gold — which A6a predicted from their zero
  mined terms. Kept on prospective grounds, since the gold is a citation frame around a literature
  that barely studies these pairs. **If they retrieve nothing against the live database either, they
  are buying coverage of a literature that does not exist and the chapter should say so.**
- 2026-08-04 (Shravan/Claude): **A3 complete — gold set assembled and frozen. Tier A 48 anchors (31
  empirical, CV floor 30 cleared); Tier B 495 records taken whole.**
  `literature/search-logs/{slug}-tier-a.json`, `-tier-b-frame.json`, `-tier-ab-log.md`,
  `-tier-b-backfill.md`; scripts `98_d1a_assemble_gold.py`, `99_d1a_backfill_gold.py`; third shared
  module `d1a_titles.py`. **Next stage is A4, term population** — the Tier-A half of step 3, which
  D.1.a has not started: `discriminative-terms` → `cv-breadth` → `production-query` → `tier-a`
  screen → `recall-probe`. B.1 has 17 search-log artifacts at this stage and D.1.a now has 11.
  **(1) Enrichment moved to S2's batch endpoint — three calls instead of 543.** B.1 and D.3.b
  enriched from OpenAlex, which is no longer viable at the free tier. Same substitution the snowball
  made, and it keeps Tier B orthogonal to OpenAlex in infrastructure as well as method.
  **(2) Two defects the assembly did not report and inspection did.** 27 of 495 "titles" were entire
  citation strings — Crossref reference lists carry an `unstructured` field when the publisher
  deposited a formatted reference, and `93_`/`96_` fall back to it. Left alone, every author surname
  and journal name in those strings would have entered the A4 candidate vocabulary as subject matter,
  and the records would have failed the recall probe for reasons unrelated to query quality. Second,
  abstracts reached only 36%; that does not block A4 (titles only, per D.3.b) but binds at A6c, where
  the title-versus-title-and-abstract operationalisation is chosen on measured recall and cannot be
  chosen honestly at 36%. A Crossref backfill took DOIs 385 → 416 and abstracts to **51%**.
  **(3) The guard refused 79 of 110 and the refusals are the evidence it is calibrated.** A hand read
  shows the residue is book chapters, regional and non-English journals, dissertations and conference
  papers that Crossref does not hold — **fourth independent appearance of the same non-Anglo-European
  indexing gap on this chapter**, after the AJRH unregistered DOI, the `NOT_INDEXED` regional reviews,
  and Dutch-language Lesthaeghe and van de Kaa 1986. Carries to §10 alongside the geographic-skew
  limitation. The clearest single refusal: *"Attitudes toward fertility and childbearing among
  childless female teachers in Gorgan"* drew a candidate titled *"...among female University
  students"* at containment **0.78** against a 0.80 bar — same title family, same year, different
  study. **Relaxing the threshold to lift the recovery rate would have assigned a wrong DOI**, which
  is how the OAS run acquired a 40%-ghost Tier B. A low recovery rate is the correct outcome when the
  records genuinely are not indexed.
  **(4) Tier A / Tier B overlap is 19 of 47**, reported because Recall(B) is only a fair yardstick to
  the extent the two channels are orthogonal in fact and not merely in source. Tier A came from the
  OpenAlex keyword probes, Tier B from a Crossref/S2 citation frame.
  **(5) Run order `98_` then `99_` is binding** — 98 writes the frame and 99 rewrites it in place, so
  98 alone silently reverts 31 DOIs and 73 abstracts while the frame still looks complete. Both are
  cached and idempotent. Recorded in both docstrings and the log.
- 2026-08-04 (PI ruling, relayed by Shravan): **whichever stop rule is hit first is the one used.**
  Applied to the round-2 escalation: the PROTOCOL §5.1 two-round depth cap was hit first, since the
  GACS §7.2 yield floor was never reached in either round, so **the cap binds and the snowball is
  closed at round 2.** Round 3 is not run and is not pending. Channel 3 is complete; D.1.a's search
  stage now moves to the Tier-A production query. **Escalated: the convention is general, not
  D.1.a-specific, and needs to land in `PROTOCOL.md`** — it resolves the same conflict wherever a
  yield rule and a depth cap coexist, and a convention no operating file states is inert. Second
  convention this chapter has sent to PROTOCOL, after the treatment × outcome routing definition.
- 2026-08-04 (Shravan/Claude): **channel-3 snowball round 2. 11,610 pulled, 410 new relevant, yield
  1.77 per 50 against a floor of 1.0 — saturation NOT reached, and the depth cap now blocks the
  round the yield rule calls for.** `literature/search-logs/{slug}-snowball-log.md` (rewritten to
  cover both rounds), `{slug}-canon-reresolution.md`; scripts `95_d1a_canon_reresolve.py`,
  `96_d1a_snowball_r2.py`, `97_d1a_rescore_pools.py`; shared modules `d1a_relevance.py`,
  `d1a_fetch.py`. Tier B stands at **495 relevant records** (85 + 410).
  **(1) ESCALATION — two committed rules give opposite answers and I did not pick one.** GACS §7.2
  stops after two consecutive rounds below 1.0 per 50; both rounds are above it and round 2's
  extension leg is at **2.01**. PROTOCOL §5.1 caps snowball depth at **2 rounds** on Wohlin 2014's
  claim that round 3 returns under 5% new material — and that prediction is plainly false here, since
  round 2 returned **7,652** records unseen in round 1 against a round-1 pool of 1,970. Round 3 is
  **not run**: the cap is the narrower committed constraint and spending it is not an RA call.
  **The accompanying caveat is mine and it cuts against my own number:** round 2's 1.77 is not
  comparable to round 1's 1.75, because round 1 was seeded from 9 framework statements and round 2
  from 82 papers already known to be on-pair. A flat yield under a far more on-pair seed set is weak
  evidence of saturation, not strong evidence against it.
  **(2) The round-1 seed error cost much less than round 1 feared, and that is worth saying plainly.**
  van de Kaa 1987 repaired from **2 to 1,316** forward citations (seeded by S2 paperId read from the
  resolver, since three providers now agree the work carries no DOI). But only **22** relevant records
  were reachable *solely* from the repaired seeds — 0.53 per 50, below the floor. The SDT family is
  densely cross-citing and round 1's other five SDT seeds had already covered that neighbourhood.
  **Round 1's yield was not materially biased.** The process change stands; the alarm is retired.
  **(3) All three of round 1's `UNCONFIRMED` seed cells were `NOT_INDEXED`, not retryable.** Round 1
  recorded them as network failures and expected a retry to fix them. It never would have. Fernández's
  *Does Culture Matter?* — the **only** econ-of-culture seed — is absent from Semantic Scholar
  entirely, so round 1 attributed to a failed pull what is actually an indexing gap. Both SSA reviews
  are likewise absent, one of them the unregistered-DOI record `91` already flagged. **Third
  independent hit on the non-Anglo-European indexing gap**, running in the same direction as the
  chapter's geographic-skew limitation. The pull layer now distinguishes four states — `OK`,
  `UNCONFIRMED` (network), `NOT_INDEXED` (index), `NO_REFS_DEPOSITED` (publisher metadata) — because
  a zero that means three different things cannot support any of the three sentences.
  **(4) Three transport bugs, each reporting missing data as measured data, and the second one is the
  same defect this project keeps committing.** (a) S2's 429 body was cached as a successful empty
  pull, because the guard tested equality against a *prefix* of the real message; it surfaced only
  because it hit van de Kaa, where `n=0` was obviously wrong. (b) The fix for (a) scanned bodies for a
  bare `"429"`, **which matched the Unix timestamp `1429894924000` inside a valid Crossref record** —
  the third unanchored-substring bug in this codebase after `hous` in C.2.c and `reproduc\w+` in v1,
  and the first in the transport layer, which is why it presented as a network symptom. Fixed by
  making the HTTP status code the primary signal. (c) Reactive backoff cannot survive an unauthenticated
  rate limit — the run reached gen-2 seed 6 of 82 in seven minutes and would have logged the rest as
  missing literature; proactive per-host pacing finished the same run with **zero** throttle retries.
  **An S2 API key is now the outstanding operational request for the second chapter running.**
  **(5) The relevance filter went to v3, and v3 exists because v2's fix was wrong at scale.** v2 added
  a design-descriptor exclusion (`cross-cultural` is a sampling frame, not a value measure) and was
  validated on the 3 records it touched. At round-2 scale it touched 43, and about half were on-pair
  records being discarded — including Colleran and Mace's *cultural evolution of fertility decline*,
  which is cultural transmission of fertility norms and is precisely this chapter's treatment. v3
  keeps only genuine sampling frames. **The generalisable lesson: each version was validated on the
  sample available when it was written and each was wrong in a way that appeared only at the next
  order of magnitude. The sample that produces a hypothesis cannot also test it.** Both pools are
  re-scored under one filter version by `97_`, since otherwise a yield change is partly a change in
  the literature and partly a change in the ruler.
  **(6) OpenAlex canon resolution is dead, not throttled, and this is not a D.1.a problem.** The
  re-run the round-1 log demanded was performed and returned `UNCONFIRMED` on all sixteen rows: the
  budget *had* reset, but a title search costs $0.001 against a daily free allowance that does not
  cover sixteen of them. `95` re-resolves every row against Crossref **and** S2 and reports agreement
  as its own field. It recovered two v5 seminal names `92` could not confirm (Frejka and Westoff 2008;
  Hagestad and Call 2007) and produced three findings worth propagating: **a Jaccard title gate
  false-negatives on subtitle drops** — Hagestad and Call scored 0.43 against a 0.55 threshold with
  both surnames and the year matching exactly, and every resolver in this tree gates on Jaccard alone;
  **Inglehart and Baker 2000 carries two registered DOIs** with citations split 2,454 / 5,379 across
  JSTOR and SAGE, the C.2.c twin problem now inside the canon seed table; and **cross-provider
  agreement is not a correctness guarantee** — both providers agree on Hofstede 1980 and both resolve
  it to a 1982 book review by a different author.
- 2026-08-03 (Shravan/Claude): **channel-3 snowball round 1. 2,423 pulled, 1,970 distinct, 86
  relevant, yield 1.77 per 50 against a floor of 1.0 — saturation NOT reached, round 2 required.**
  `literature/search-logs/{slug}-snowball-log.md`; scripts `93_d1a_snowball_r1.py`,
  `94_d1a_relabel_pool.py`; canon resolution at `{slug}-canon-seed-resolution.md` (`92_...`).
  **(1) The frame is built off Crossref and Semantic Scholar, not OpenAlex, and this should stay that
  way.** Forced first: **OpenAlex has moved its free tier to a metered budget**, and scripts 89–92
  exhausted a full day's allowance in about an hour. The six UNCONFIRMED rows in 92 are that, not
  missing papers — the three-state rule held twice today. But it is also *better*: PROTOCOL §5.1
  already names both providers, and building Tier B off a different provider than the one that
  produced Tier A makes the frame orthogonal in infrastructure as well as method, so Recall(B) is a
  stronger test. **Request a Semantic Scholar API key before the next chapter's snowball** —
  unauthenticated S2 throttled partway through.
  **(2) The relevance filter was wrong in BOTH directions and a hand audit is the only thing that
  found it.** Bug A: `reproduc\w+` admitted *social* reproduction and reproductive **health** —
  it scored Bourdieu's *Reproduction in Education, Culture and Society* as on-pair. Bug B, worse:
  quoted phrases carried from OpenAlex query syntax into a Python verbose regex, where
  `"second demographic transition"` matches only text containing literal quote characters, so **the
  chapter's most central phrase never matched anything.** Corrected 79 → 86 relevant, 1.63 → 1.77.
  **The lesson sharpens C.2.c's:** a classifier can be wrong in both directions at once, the errors
  partially cancel, and the summary statistic is therefore the last place either shows up. A net
  movement of seven records concealed two errors that each distorted the frame. Read admitted *and*
  rejected samples, not just admitted.
  **(3) A self-inflicted seed error, stated plainly.** van de Kaa 1987 — the most-cited SDT statement
  in the field, ~1,950 citations — contributed **2** forward citations because I hand-typed a DOI into
  the seed table. Script 92 had already resolved it correctly and reported that the work carries **no
  registered DOI**; I did not read my own resolver's output. This is the exact failure the existence
  gate exists to prevent, committed one step after building the gate. Consequences: the round-1 frame
  under-reaches the SDT family by roughly its central work's citation neighbourhood, so **1.77 is a
  lower bound on coverage, not a stable saturation reading**; and **seed tables must be generated from
  resolver output, never typed** — a process change, not just a fix.
  **(4) Seed criterion recorded: specificity of the citation neighbourhood, not fame.** Hofstede 1980
  (15,158c) and Schwartz 1992 both resolve and are deliberately NOT seeded — they are canon for a
  *construct*, not for this pair, and would bury the frame. The obvious alternative, keyword-filtering
  the frame down to fertility papers, is **refused on purpose**: it would inflate Recall(B), which is
  the OAS and C.2.c error. Also: the resolver caught **Schwartz 1992 resolving to the wrong paper**
  entirely, and it carries `RESOLVED_DISCREPANT`.
  **(5) v5 seminal field audited** (`92_...`). Verified: Lesthaeghe 1983, van de Kaa 1987, Lesthaeghe
  and Surkyn 1988, Norris and Inglehart 2004. **Lesthaeghe and van de Kaa 1986 and Hagestad and Call
  2007 did not resolve**; Frejka and Westoff 2008 is UNCONFIRMED on budget exhaustion, not absence.
  Re-run after the OpenAlex reset before drawing any conclusion about the two unresolved names.
- 2026-08-03 (Shravan/Claude): **cold-start anchor set built and existence-gated. 48 anchors, 31
  empirical, the ≥30 CV floor CLEARED, zero ghosts.**
  `literature/search-logs/{slug}-cold-start-anchors.{json,md}`; script
  `source/build/goldset/91_d1a_cold_start_anchors.py`. Composition: 31 EMPIRICAL / 4 THEORY /
  10 DECOY / 2 CHANNEL1_REVIEW / 1 REVERSE. Empirical by pair **S3 23, S1 5, S5 2, S2 1**; by design
  tier **Tier 1: 3, Tier 2: 6, Tier 3: 21, Tier 4: 1**. The composition is the chapter's shape in
  miniature and it matches what Ruling 3 predicted: three-quarters of the anchor set can support
  nothing above Very Low.
  **(1) The existence gate false-ghosted 24 of 45 anchors on its first run, and the bug was mine.**
  The check used `curl -I -L`, which follows doi.org's 302 through to the publisher — and Annual
  Reviews, the AEA, Oxford and Wiley all answer an automated request with **403**. The gate read those
  403s as non-existence and reported Zaidi and Morgan 2017 and Fernández and Fogli 2009 as fabricated,
  an hour after OpenAlex had confirmed both live. **The correct test is whether doi.org KNOWS the
  identifier — 302 registered, 404 unknown — and the redirect must not be followed.** Publisher
  bot-blocking is not evidence about whether a paper exists. This is the same class as the C.2.c
  false-ghost call, and it fails in the direction that looks like diligence: a gate that invents
  ghosts reads as rigour right up until it deletes a real literature.
  **(2) Fixed properly rather than patched: the gate now takes three independent existence witnesses**
  — registered DOI, live Crossref record, PubMed identifier — and calls GHOST only when all three fail.
  **(3) The third witness was not defensive coding; it caught a real case.** "Human fertility and
  religions in sub-Saharan Africa" (*Afr J Reprod Health* 2023) is a real paper carrying PMID 37584963
  whose DOI was never registered with Crossref. Under the resolution rule that is the dead-identifier
  case: keep, key on title, do not drop. Recorded as `VERIFIED_TITLE_KEYED`. **The blind spot is
  systematic, not incidental — a Crossref-plus-doi.org gate false-ghosts journals outside the
  Anglo-European publishing infrastructure**, which would thin the anchor set in exactly the direction
  this chapter's geographic-skew limitation already runs. Worth propagating to the other chapters'
  gates.
  **(4) A reproducibility gap found and closed.** Ten selected anchors were first seen in ad-hoc
  probes run at the terminal rather than in scripts 89 or 90, so they lived in a session transcript
  and nowhere a script could read. The set would not have rebuilt from the repo alone. Fixed with a
  live OpenAlex-by-DOI fallback; bibliographic fields still never come from a hand-typed literal.
- 2026-08-03 (Shravan/Claude): **Tier-1 design probe. Tier 1 exists and it is three studies.**
  `literature/search-logs/{slug}-tier1-design-probe.md`; script
  `source/build/goldset/90_d1a_tier1_design_probe.py`. 24 narrow probes, all under the five-operator
  cap, 257 distinct records unioned client-side — the structure the cap forces, and the pattern the
  production query will have to use.
  **(1) Three credible Tier 1 candidates, all S3, all published since 2018:** Political Islam,
  Marriage and Fertility (*AJS* 2018, `10.1086/696193`); Secularization and low fertility, on declining
  church membership (*Social Science Research* 2026, `10.1016/j.ssresearch.2026.103371`); and a
  religious-leader intervention in Georgia (*JPopE* 2025, `10.1007/s00148-025-01092-5`).
  **(2) The empty shock families are as informative as the full ones, and the chapter should say so.**
  Blue laws and Sunday trading: **zero**. Clergy-scandal shocks: **zero**. State atheism: five hits,
  none with a fertility outcome. The Gruber-Hungerman design family has been applied to religiosity and
  then to drinking, drug use and crime, never to fertility; the Soviet and Albanian campaigns are the
  largest deliberate secularization shocks in history and appear never to have been used to identify a
  fertility effect. That is a specific checkable gap and it belongs in §10 as the recommended study.
  **(3) S1 is not empty of estimates, only of identified ones** — a refinement on the scope. Found
  Lesthaeghe and Surkyn 1988 (*PDR*, 719c, a v5 seminal name now confirmed), an explicit empirical
  horse-race between the competing accounts (*PDR* 2022, `10.1111/padr.12490`, priority read), and a
  German-language postmaterialism-to-fertility study from 1990. So S1 can be *reported* without being
  *rated* above Very Low, which is a better chapter section than "no evidence exists."
  **(4) New question the scope missed: language coverage.** The German study is a reminder that the
  continental European core of this literature is not all in English, and Lesthaeghe's early work is
  partly Dutch and French. An English-only production query would systematically drop exactly the
  FDT-era material Ruling 4 just admitted. Needs a decision at the query build, not a default.
  **(5) The single most useful paper found today is a `REVERSE` record.**
  `10.1093/esr/jcac060`, "Does forming a nuclear family increase religiosity? Longitudinal evidence
  from the BHPS" (*ESR* 2022) sizes the reverse arrow. It carries no effect estimate for this chapter
  and it measures the binding risk-of-bias domain, so it should be cited in the risk-of-bias section
  rather than buried in a context list.
  **(6) Fernández and Fogli 2009 confirmed** (`10.1257/mac.1.1.146`, 1242c) — the most-cited record in
  the whole union, listed as seminal under A.19, and Wall 5 says its routing turns on proxy content.
  Must be read at full text before assignment, never routed from the abstract.
  **(7) The clinical collision recurs inside the design probes** — `design_iv` returned livestock
  reproduction and haemophilia, and the Hutterite probe returned human-genetics work on HLA antigens
  next to the demography. Three separate probe designs now. It is a property of the outcome vocabulary,
  not of any one query, and the production query needs the exclusion built in from the start.
- 2026-08-03 (Shravan/Claude): **cold-start channel-1 probe run, per pair. Channel 1 is empty for
  four of the five pairs.** `literature/search-logs/{slug}-channel1-probe.md`; script
  `source/build/goldset/89_d1a_channel1_probe.py`; raw at `temp/d1a/`.
  **(1) The result inverts the scope's prediction, and the inversion is the finding.** The scope
  expected reviews to exist for secularization and not for postmaterialism, individualism, or
  consumerism. The negative half holds. The positive half does not: `religion AND fertility` with
  `type:review` returns **zero across all fields**, and the only syntheses that exist are two
  sub-Saharan Africa regional ones. Religion and fertility has been studied for a century and never
  systematically synthesised outside one region. So the pair expected to carry the chapter is the
  pair that cannot be bootstrapped from external authority, and its anchors have to come from
  channels 2 and 3.
  **(2) Third chapter running to find channel 1 thin or empty** — D.3.b (literature too new), C.2.c
  (never synthesised), D.1.a (four pairs empty, fifth regional). Three different causes, one outcome.
  **GACS §7 move 5 should now be reported as tested and failing on this leg rather than left open**;
  in practice the bootstrap runs on channels 2 and 3.
  **(3) Two production-query hazards found, both of which have to be fixed in the query rather than
  paid for at screening.** The bare outcome axis collides head-on with clinical medicine — *fertility*
  reads as IVF, *birth* as birth weight, and OpenAlex stemming matched *individualism* to
  "individualiSED dosing of follitropin delta"; the top-cited hit across three separate pairs was a
  systematic review of antenatal care. Same class as C.2.c's `housing AND fertility` against livestock
  housing. Second, **OpenAlex throttles boolean searches above five operators** and returns a rate-limit
  error, which a GACS cause axis with eight OR'd terms exceeds on its own. Worth checking against the
  production-query builders already written for B.1, D.3.b, and C.2.c: a throttled query that still
  returns a plausible count is the failure mode that does not announce itself, which is the shape of
  the C.2.c relevance-filter bug.
  **(4) Positive controls were run before any pair was declared empty**, per the C.2.c lesson that a
  failed lookup usually means a wrong query string. All four pass, including Zaidi and Morgan 2017
  (301c) and Lesthaeghe and Wilson's 1986 Princeton EFP secularization chapter — **the FDT-era anchor
  Ruling 4 was written to admit, now confirmed to exist.**
  **(5) Thirteen S3 anchor candidates surfaced incidentally and none is a natural experiment.** Every
  one is Tier 3 or Tier 4 on the face of its title. The Tier 1 material the chapter needs — church-tax
  reform, blue-law repeal, state secularization campaigns, clergy-scandal shocks — will have to be
  sought by *design* vocabulary rather than by topic. That is the next probe.
- 2026-08-03 (Shravan, PI-relayed guidance): **a hypothesis is a treatment × outcome pair. Mediators
  and mechanisms do not define it and do not route a paper.** Scope doc rewritten onto that spine; the
  cause → effect-plus-mechanism version is at commit `8811c17`. What the rewrite changed:
  **(1) Routing collapsed to a two-question test** — is the regressor a value measure of the specified
  content, and is the dependent variable fertility. Eleven walls became **seven**, because the four
  that existed to adjudicate mediators dissolved: A.3/A.6/A.20 merged into one wall that simply names
  their treatments, and the root-cause-versus-proximate reasoning behind it is gone. D.1.a owns any
  estimate whose regressor is a value measure, including when the fitted effect plainly runs through
  contraceptive use or marriage timing.
  **(2) The non-additivity item is demoted out of the walls.** Under this definition it is **not a
  scoping problem at all** — the treatments differ, so routing is clean and no study is double-counted.
  It reappears only at §7, where overlapping shares of one decline get added. Stays folded into
  TICK-054, out of this chapter's scope.
  **(3) Ruling 2 got sharper, not weaker.** The measure-content bar restates as a **degenerate-pair
  rule**: when the treatment measure and the outcome measure are the same construct, there is no pair.
  Own approval of childlessness against own childlessness is one variable measured twice.
  **(4) A new recommendation falls straight out of the definition.** Five treatments against one
  outcome is **five pairs, hence arguably five hypotheses**, and the master list should probably split
  D.1.a starting with S3 (secularization), the only one with a rateable evidence base. Precedent at
  TICK-032.
  **(5) The convention needs a home in `PROTOCOL.md`.** It changes routing in every chapter, not only
  this one, and a convention no operating file states is inert per the ticket-closing rule. Escalated.
- 2026-08-03 (Shravan/Claude): **scope drafted, deliberately NOT frozen.**
  `literature/search-logs/postmaterialism-individualism-secularization-search-scope.md`. Five strata,
  eleven walls, 25 estimand cells, ten required per-effect tags, five pre-registered rulings. The
  scoping brief was taken from the withdrawn D.1.a ticket, recoverable at
  `git show eecf024:tickets/TICK-060-d1a-search-scope.md`. Five things the drafting settled or
  surfaced beyond that brief:
  **(1) Two rulings cap the chapter's rating before any study is read, and neither is an RA call to
  make alone.** Ruling 2 bars value measures whose item content refers to children or family size
  from the causal pool, because regressing a person's childlessness on their own approval of
  childlessness estimates preference-outcome consistency rather than a causal effect. That removes
  most of `childlessness-as-acceptable-choice`, one of the five sub-claims the master list assigned
  here. Ruling 3 fixes an admissible-design ladder with pre-committed GRADE ceilings and puts
  country-level value-index-versus-TFR co-movement — **the canonical SDT evidence base** — at Tier 4
  with no causal weight, on three joint defects: about fifty units against a dozen collinear
  covariates, GDP among them, and countries not being independent draws because values diffuse across
  borders. Both are flagged for PI sign-off as a freeze condition.
  **(2) The strata are unequal enough that even search budget should not be split evenly.**
  Secularization is the only one of the five with a large individual-level literature and access to
  genuine natural experiments (state atheism campaigns, church-tax and blue-law reform, clergy-scandal
  shocks, compulsory secular schooling). Postmaterialism and individualism have a large theoretical
  and measurement literature and very few fertility estimates above Tier 4. Same shape as C.2.c's
  rent-identified stratum carrying that chapter.
  **(3) Wall 8 is a demonstrated failure, not a hypothetical one — the Lovenheim and Mumford problem
  again.** A.19's seminal list contains Fernández and Fogli 2009 and its `notes` field claims the
  epidemiological approach outright, but that design is the best available tool for D.1.a's claim
  because it holds prices and institutions fixed while culture varies. Resolved on proxy content:
  ancestral *fertility rate* tests persistence and routes to A.19; an ancestral *value measure* tests
  the content claim and routes here. Master-list note recommended for TICK-001, flagged not made.
  **(4) Non-additivity, third instance and materially worse than the first two.** A.10 → A.7 and
  C.2.c → A.23 are each one hypothesis with one mediator. D.1.a is a root cause whose whole pathway
  runs through four or five separately credited chapters (A.3, A.6, A.2/B.1, D.2.b, A.7) — three of
  which name D.1.a as their root cause in their own `notes`. If each proximate chapter claims its
  share and D.1.a claims the reduced form, the shares sum past 100% and the per-hypothesis verdict
  format breaks where a reader adds it up. Folded into the TICK-054 escalation, with the note that it
  is now a defect in the deliverable's format rather than an accounting nuisance.
  **(5) Two concrete search hazards worth catching before the query build.** The word *materialism*
  means opposite things in the two feeding literatures — Inglehart's materialist prioritizes security,
  the consumer-psychology materialist is acquisitive — so an undisambiguated term retrieves both and
  scores them in opposite directions. And much of this literature runs on a handful of survey
  instruments (WVS/EVS, ESS, GSS, DHS), so twenty papers on overlapping waves and countries are not
  twenty independent estimates; `DATA_SOURCE` is a required tag and a clustering variable in any
  pooled analysis.
  Also ruled: FDT-era evidence admitted (Princeton EFP secularization is measurement of the S3
  construct applied to the first transition), with the `phenomena` field escalated to TICK-001 as the
  third instance of the same restriction; and a sign convention orienting every effect toward the
  secular/postmaterialist pole, since S3 is almost always coded the other way and mixing flipped and
  unflipped estimates is a mechanical route to a null.
- 2026-08-03 (Shravan/Claude): opened and claimed. No prior D.1.a artifacts exist in
  `literature/search-logs/`, `extraction/`, or `output/chapters/`; the only inbound material is the
  17 records the D.3.b RA gate routed to `OFF_POSTMATERIALIST_D1a`.