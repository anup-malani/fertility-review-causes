# Handoff — fertility-review-causes

**Last updated:** 2026-06-23
**PI:** Anup Malani
**RAs:** Alexandra Zhou (zhitongz@uchicago.edu), Shravan Haribalaraman (shravanh@uchicago.edu)

---

## State of the Project

The OAS/pension-crowdout pilot has completed both automated search phases (sequential saturation screen + citation snowball) and produced 583 RELEVANT papers. The `prioritize-papers.mjs` workflow is built and ready to run. The next session should run prioritization, review the tier breakdown, and hand Tier 1 papers to the RAs for full-text retrieval.

---

## Pipeline Architecture (Finalized)

The old plan (single 12K-paper bulk screen → rank-papers.mjs) was discarded. The final design has three automated phases before any human touches papers:

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
Phase 3 — Prioritization                 (prioritize-papers.mjs)  ← NOT YET RUN
    Fetch abstracts from OpenAlex for all RELEVANT papers
    Sonnet scores each paper: evidence type (0–4) + identification (0–3) + centrality (0–3)
    Composite 0–10; Tier 1 (≥7) = definitely retrieve; Tier 2 (4–6) = retrieve if needed
    Output: ranked list with tier assignments
        ↓
RA title/abstract review                                           ← NOT YET STARTED
    RAs review Tier 1 papers, flag for full-text retrieval
    Target: ~60–100 papers retrieved
```

Rationale for saturation sampling vs. bulk pull: OpenAlex relevance scores are monotonically decreasing, so the most relevant papers come first. Screening stops when yield drops, rather than pulling all ~79K papers. Full design documented in PROTOCOL.md §5.1.

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

All RELEVANT papers: **583 total**. This is 5–10× the 60–100 target for RA review, which is why prioritization is the immediate next step.

---

## Immediate Next Steps

### 1. Run prioritize-papers.mjs

```
Workflow({ scriptPath: '.claude/workflows/prioritize-papers.mjs',
           args: { slug: 'old-age-security-pension-crowdout' } })
```

Output: `literature/search-logs/old-age-security-pension-crowdout-prioritized.json`

After it completes, check the tier breakdown. If Tier 1 has 30–80 papers, send that list to RAs. If Tier 1 is too large (>100), filter further by Tier 1 + llm_confidence=HIGH.

### 2. RA title/abstract review

Hand RAs the Tier 1 prioritized list as a CSV or Google Sheet with columns: rank, title, year, journal, doi, compositeScore, scoreRationale, llm_reason. RAs mark each paper: RETRIEVE / EXCLUDE / UNSURE.

### 3. Full-text retrieval

RAs retrieve PDFs for RETRIEVE papers using UChicago library proxy and ILL. Target: 40–80 PDFs.

### 4. Raise hard cap for next hypothesis

Edit `sequential-screen.mjs` line 40: `const HARD_CAP = 2000`. Yield never hit natural saturation at 1,000; 2,000 should catch the tail.

---

## Key Files

| File | Status | Notes |
|------|--------|-------|
| `.claude/workflows/sequential-screen.mjs` | Done | Phase 1 |
| `.claude/workflows/snowball-citations.mjs` | Done | Phase 2 |
| `.claude/workflows/prioritize-papers.mjs` | **Built, not yet run** | Phase 3 — run next |
| `literature/search-logs/old-age-security-pension-crowdout-sequential-screened.json` | Done | 1,099 screened, 194 RELEVANT |
| `literature/search-logs/old-age-security-pension-crowdout-snowball.json` | Done | 1,922 screened, 389 RELEVANT |
| `literature/search-logs/old-age-security-pension-crowdout-prioritized.json` | **Does not exist yet** | Created by prioritize-papers.mjs |
| `literature/search-logs/llm-screen-prompt.md` | Done (rev 9) | Changes 7–9 applied; tie-breaker = NOT_RELEVANT |
| `PROTOCOL.md` | Done | §5.1 documents two-phase pipeline |

Temp files (not committed, safe to delete after prioritization):
- `temp/old-age-security-pension-crowdout-seq-batch-*.json` — Phase 1 raw batches
- `temp/old-age-security-pension-crowdout-seq-verdicts-batch-*.json` — Phase 1 verdicts
- `temp/old-age-security-pension-crowdout-snowball-*.json` — Phase 2 intermediate files

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

1. **Tier 1 size after prioritization.** If the composite score distribution is flat (many papers score 5–6), Tier 1 may be too small or too large. May need to adjust tier thresholds or add a fourth tier.

2. **Phase 1 hard cap.** Yield curve for OAS never hit natural saturation at 1,000 papers. Raise to 2,000 for next hypothesis? Tradeoff: ~2× cost and time, but better recall.

3. **Applying the new pipeline to other hypotheses.** The three workflow files are slug-parameterized and reusable. Next hypothesis to pilot: recommend one with a large empirical literature (e.g., education-fertility or female-labor-supply-fertility) to stress-test the pipeline before running all 65.

4. **RA role going forward.** RAs have not yet done a human screening pass on the OAS corpus. Once Tier 1 is identified, schedule a 2-hour session for RAs to work through titles and confirm retrieval decisions before ordering PDFs.
