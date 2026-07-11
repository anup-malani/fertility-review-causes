# Handoff — fertility-review-causes

**Last updated:** 2026-07-11
**PI:** Anup Malani
**RAs:** Alexandra Zhou (zhitongz@uchicago.edu), Shravan Haribalaraman (shravanh@uchicago.edu)

---

## Current OAS Meta-Analysis State — 2026-07-11

The old-age-security/pension-crowdout chapter now has RA-adjudicated effect extraction,
meta-analysis readiness output, and PI-assumed sign orientation for the current extracted rows.
The harmonized effects table adds `pi_approved`, old-age-security treatment direction,
`effect_oriented_more_oas`, oriented SE, orientation method, and harmonized treatment-scale
labels. Pension-cut rows are sign-flipped so oriented effects mean the fertility effect of more
non-child old-age security; broad Social Security Act/baby-boom rows remain unoriented because
the mechanism is mixed.

The current quantitative synthesis is still screening-only, not a coefficient-pooled
meta-analysis. The adopted conservative pooling rule requires the same mechanism cell, outcome
family, harmonized unit, harmonized treatment scale, usable oriented effect/SE, and at least
three independent studies. The two candidate numeric families are one-year birth probability and
completed fertility / children ever born. Both fail the rule because they mix treatment scales,
so the chapter should report Cell A as structured quantitative narrative unless new same-scale
studies are added. The first TFR-based transition classification pass is now complete using
read-only UN TFR data from Alexandra's local `proximate-causes` directory. Brazil is FDT|SDT,
Namibia and postwar United States are FDT, Italy and the China pension/LTCI rows are SDT, China
is flagged as policy-constrained, and Prussia / Imperial Germany / 1850 U.S. rows remain
unclassified by TFR because the local source has no in-window observations. The next highest-value
analytic steps are the broader demographic-significance macro pass and extraction of the
PI-identified Cell C grandparental-childcare studies.

Update: the PI-identified Cell C grandparental-childcare studies have now been retrieved and
extracted: Eibich-Siedler 2020, Ilciukas 2023, and Akyol-Atalay 2025. The OAS
demographic-significance table now treats SDT grandparental childcare as
`partial_pending_slope_scaling`, with all Cell C study windows classified as SDT and the effect
direction positive after orienting to greater grandparent availability. The next highest-value step
is final GRADE/summary adjudication and slope-sufficiency scaling for Cell C, not another Cell A
pooling attempt.

Update: a noob-readable Cell C slope-scaling table now exists at
`output/tables/old-age-security-pension-crowdout-cell-c-slope-scaling.csv`, with a short
interpretation note at `output/old-age-security-pension-crowdout-cell-c-slope-scaling.md`. It
orients every Cell C estimate to "more grandparent availability," labels all 8 extracted effects as
positive on that scale, and explicitly says not to coefficient-pool them because the treatment
scales differ.

Update: Cell C slope sufficiency has been implemented at
`output/tables/old-age-security-pension-crowdout-cell-c-slope-sufficiency.csv`, with a short note
at `output/old-age-security-pension-crowdout-cell-c-slope-sufficiency.md`. Six rows are large
relative to observed TFR declines in the Netherlands and Australia windows. The two Germany rows
are marked `not_applicable_no_observed_decline` because Germany's TFR rises slightly over the
1984-2017 SOEP window, so there is no observed decline denominator. The demographic-significance
row for SDT grandparental childcare now reports `partial_slope_screening_support`. Next step:
translate this into chapter language and finalize GRADE/RA readability review.

Update: the noob-facing meta-analysis language is now integrated into
`output/chapters/old-age-security-pension-crowdout.md`. The chapter explains the no-pooling rule,
reports Cell A as structured quantitative narrative, reports Cell C as a separate SDT structured
quantitative synthesis, and includes a GRADE-style final rating table. A generated GRADE CSV now
exists at `output/tables/old-age-security-pension-crowdout-grade-verdicts.csv`. Next step:
RA/PI readability and risk-of-bias verification; no additional Cell C extraction or slope-scaling
is pending.

Key current outputs:
- `output/tables/old-age-security-pension-crowdout-harmonized-effects.csv`
- `output/tables/old-age-security-pension-crowdout-meta-analysis-readiness.csv`
- `output/tables/old-age-security-pension-crowdout-summary-of-findings.csv`
- `output/tables/old-age-security-pension-crowdout-tfr-transition-classification.csv`
- `output/tables/old-age-security-pension-crowdout-demographic-significance.csv`
- `output/chapters/old-age-security-pension-crowdout.md`
- `decisions/2026-07-11-oas-conservative-pooling-rule.md`

---

## State of the Project

The OAS/pension-crowdout pilot has completed the PI baseline pipeline through prioritization. The prioritized output exists at `literature/search-logs/old-age-security-pension-crowdout-prioritized.json`: **542 scored RELEVANT papers**, with **74 Tier 1** papers for RA review.

Two additional search-method design notes were added by Shravan:
- `old-age-security-pension-crowdout-hybrid-discovery-method.md` — citation-first/top-down snowball experiment, evaluated but not adopted as the primary method.
- `old-age-security-pension-crowdout-gold-anchored-keyword-method.md` — proposed v2 primary method using a DOI-keyed quasi-gold set and cross-validated keyword recall.

Alexandra/Codex also prototyped an anchor-guided query-clustering alternative in ignored `temp/` scripts and documented it in `old-age-security-pension-crowdout-query-clustering-method.md`. This is **not adopted protocol**; it is a comparison candidate.

Anup's meeting feedback on 2026-06-27 clarified two objectives for the revised search design:
- Query clustering is substantively useful because different keyword families help literatures from different disciplines speak to each other, rather than forcing the search through one OpenAlex relevance ranking.
- Canonical theory papers should remain in search outputs because chapters should have a JEL-style theory section, even though the formal meta-analysis/effect-size subset should be empirical.

Shravan will synthesize the free-search methods. The query-clustering note now includes a dedicated synthesis section with the method's inputs, outputs, what worked, what failed, and improvement paths, so it can be combined with the gold-anchored keyword design.

---

## Current Baseline Pipeline Architecture

The old plan (single 12K-paper bulk screen → rank-papers.mjs) was discarded. The current baseline design has three automated phases before any human touches papers:

```
Phase 1 — Sequential Saturation Screen   (sequential-screen.mjs)
    Pull OpenAlex in relevance-ranked batches of 100
    Haiku screens each batch; stop when yield < 5% for 2 consecutive batches
    Output: ~200 RELEVANT seeds
        ↓
Phase 2 — Citation Snowball              (snowball-citations.mjs)
    Backward: referenced_works of top-50 seeds → Haiku screen
    Forward:  papers citing top-15 seeds via OpenAlex + Semantic Scholar → Haiku screen
    Output: ~200-400 additional RELEVANT papers
        ↓
Phase 3 — Prioritization                 (prioritize-papers.mjs)  ← RUN
    Fetch abstracts from OpenAlex for all RELEVANT papers
    Sonnet scores each paper: evidence type (0–4) + identification (0–3) + centrality (0–3)
    Composite 0–10; Tier 1 (≥7) = definitely retrieve; Tier 2 (4–6) = retrieve if needed
    Output: ranked list with tier assignments
        ↓
RA title/abstract review                                           ← NOT YET STARTED
    RAs review Tier 1 papers, flag for full-text retrieval
    Target: ~60–100 papers retrieved
```

Rationale for saturation sampling vs. bulk pull: OpenAlex relevance scores are monotonically decreasing, so the most relevant papers come first. Screening stops when yield drops, rather than pulling all ~79K papers. Full design documented in PROTOCOL.md §5.1. The newer method notes question whether one OpenAlex ranking should be trusted as the primary recall mechanism.

---

## OAS Pilot — Current Numbers

| Phase | Papers screened | RELEVANT | UNCERTAIN |
|-------|---------------:|--------:|----------:|
| Phase 1 — Sequential screen | 1,099 | 194 | 124 |
| Phase 2a — Backward snowball | 517 | 44 | — |
| Phase 2b — Forward snowball | 1,405 | 345 | 532 |
| **Total** | **3,021** | **583** | — |

Phase 1 yield curve (stopped at 1,000-paper hard cap, not natural saturation):

| Batch | Yield | Note |
|-------|------:|------|
| 1 | 36.0% | |
| 2 | 23.0% | |
| 3–5 | 18–25% | persistently high |
| 6 | 8.0% | first drop |
| 7–8 | 13.0% | rebounded |
| 9 | 21.0% | still high |
| 10–11 | 7–8% | finally dropping |

**Implication:** 1,000-paper cap hit before natural saturation. Consider raising to 2,000 for next hypothesis, or running two sequential-screen passes back-to-back.

All RELEVANT papers before prioritization: **583 total**. The committed prioritized file scores **542** papers (all RELEVANT in that file): Tier 1 = **74**, Tier 2 = **255**, Tier 3 = **213**.

---

## Immediate Next Steps

### 1. Decide which search method governs the next pilot

The baseline pipeline is ready for RA review, but three search-method options now need PI choice before generalizing beyond OAS:
- Baseline sequential saturation + snowball + prioritization.
- Shravan's gold-anchored keyword method with cross-validated recall.
- Alexandra/Codex anchor-guided query clustering as an operational alternative or complement.

Meeting update: query clustering should be treated as a way to preserve disciplinary vocabulary diversity, not only as an API-budget device. Theory papers should be retained for theory-section coverage; empirical papers remain the validation anchors and meta-analysis candidates.

Shravan synthesis task: compare the baseline search, citation-snowball complement, gold-anchored keyword method, and query-clustering wrapper. For query clustering, use `old-age-security-pension-crowdout-query-clustering-method.md` §8 as the implementation-facing summary.

### 2. RA title/abstract review

If proceeding with the baseline OAS output, hand RAs the 74 Tier 1 prioritized papers as a CSV or Google Sheet with columns: rank, title, year, journal, doi, compositeScore, scoreRationale, llm_reason. RAs mark each paper: RETRIEVE / EXCLUDE / UNSURE.

### 3. Full-text retrieval

RAs retrieve PDFs for RETRIEVE papers using UChicago library proxy and ILL. Target: 40–80 PDFs.

### 4. Resolve API/rate-limit strategy before reruns

Alternative query-clustering runs encountered OpenAlex `429 Too Many Requests` during repeated anchor resolution, cluster sampling, keyword pulls, and snowball calls. Any production rerun should include caching, resume support, polite throttling, bounded retry/backoff, and DOI-keyed dedup before increasing query volume.

---

## Key Files

| File | Status | Notes |
|------|--------|-------|
| `.claude/workflows/sequential-screen.mjs` | Done | Phase 1 |
| `.claude/workflows/snowball-citations.mjs` | Done | Phase 2 |
| `.claude/workflows/prioritize-papers.mjs` | Done | Phase 3 — output committed |
| `literature/search-logs/old-age-security-pension-crowdout-sequential-screened.json` | Done | 1,099 screened, 194 RELEVANT |
| `literature/search-logs/old-age-security-pension-crowdout-snowball.json` | Done | 1,922 screened, 389 RELEVANT |
| `literature/search-logs/old-age-security-pension-crowdout-prioritized.json` | Done | 542 scored; Tier 1 = 74 |
| `literature/search-logs/old-age-security-pension-crowdout-hybrid-discovery-method.md` | Done | Shravan citation-first experiment; not primary |
| `literature/search-logs/old-age-security-pension-crowdout-gold-anchored-keyword-method.md` | Done | Shravan v2 proposed method |
| `literature/search-logs/old-age-security-pension-crowdout-query-clustering-method.md` | Drafted | Alexandra/Codex alternative prototype |
| `literature/search-logs/llm-screen-prompt.md` | Done (rev 9) | Changes 7–9 applied; tie-breaker = NOT_RELEVANT |
| `PROTOCOL.md` | Done | §5.1 documents two-phase pipeline |

Temp files (ignored, not committed; preserve while evaluating search-method prototypes):
- `temp/old-age-security-pension-crowdout-seq-batch-*.json` — Phase 1 raw batches
- `temp/old-age-security-pension-crowdout-seq-verdicts-batch-*.json` — Phase 1 verdicts
- `temp/old-age-security-pension-crowdout-snowball-*.json` — Phase 2 intermediate files
- `temp/anchor_guided_search_workflow.py` and `temp/*anchor-guided*` — query-clustering prototype and outputs

---

## Design Decisions and Rationale

**Why saturation sampling instead of full cursor pull?**
OpenAlex caps `search=` pagination at ~6,400 results. The prior approach pulled all 6,400 and screened them all (~$30, ~90 min), yielding ~500 RELEVANT. Saturation sampling screens only the top-ranked portion and stops when yield drops; it typically screened ~1,000 papers while the forward snowball recovers papers missed by keyword ranking.

**Why TOP_N_BACKWARD = 50 and TOP_N_FORWARD = 15?**
With 194 seeds, running sequential referenced_works calls for all seeds exceeds the 180s agent timeout. TOP_N_BACKWARD = 50 caps sequential API calls to ~30s. TOP_N_FORWARD = 15 caps the parallel forward agents to a manageable concurrency level (15 agents × forward citations from OpenAlex + Semantic Scholar).

**Why prompt changes 7–9?**
Prior prompt (changes 1–6) had yield of ~8% after 1,000 papers, producing 194 RELEVANT. Combined with snowball this grew to 583. Changes 7–9 tighten the RELEVANT criteria and flip the tie-breaker to NOT_RELEVANT. These changes apply to future hypotheses — not retroactively to OAS since the pilot is already complete.

**Why Sonnet for prioritization, not Haiku?**
Scoring on evidence type and causal identification requires genuine understanding of study design (natural experiment vs. OLS vs. theory). Haiku makes too many errors on this judgment. Sonnet is more expensive but this is a one-time pass over 583 papers, not a bulk-screen.

---

## Open Questions

1. **Primary search method for the next hypothesis.** Should the next pilot use the baseline PI pipeline, Shravan's gold-anchored keyword method, the anchor-guided query-clustering method, or some hybrid?

2. **Gold set construction.** Shravan's v2 method depends on a DOI-keyed quasi-gold set, especially a keyword-disconnected Tier B. This is the binding resource. Empirical papers should validate meta-analysis recall; canonical theory papers should be retained separately for theory-section coverage.

3. **API hygiene.** Repeated experimental runs now trigger OpenAlex 429 rate limits. Future scripts need persistent caches, resume files, and request throttling before larger reruns.

4. **RA role going forward.** RAs have not yet done a human screening pass on the OAS corpus. If the baseline output is accepted, schedule a 2-hour session for RAs to work through the 74 Tier 1 papers and confirm retrieval decisions before ordering PDFs.
