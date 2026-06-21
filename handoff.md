# Handoff — fertility-review-causes

**Last updated:** 2026-06-20 (evening)
**PI:** Anup Malani
**RAs:** Alexandra Zhou (zhitongz@uchicago.edu), Shravan Haribalaraman (shravanh@uchicago.edu)

---

## State of the Project

We completed the first full LLM screening pass on the OAS/pension-crowdout hypothesis and discovered a fundamental protocol problem: the current two-stage pipeline (Boolean search → LLM screen → human review) produces ~2,000 papers per hypothesis for human review. With 65 hypotheses, that is 130,000 human-reviewed abstracts — completely unworkable for two RAs.

The session ended with a decision to redesign the LLM pipeline to a three-stage process that brings each hypothesis down to ~100 papers for human review before any human eyes touch it.

---

## What Was Accomplished This Session

### calibrate-screen.mjs — built and validated (4 batches)

`calibrate-screen.mjs` is fully implemented. It fetches 1K papers from OpenAlex, dual-screens with Haiku + Sonnet in parallel 100-paper chunks, computes divergence statistics, and writes a calibration report + routing rule.

Four calibration batches completed on `old-age-security-pension-crowdout`:

| Batch | Papers | Agreement | Haiku FN | Haiku FP | Confusion | Criterion |
|-------|--------|-----------|----------|----------|-----------|-----------|
| 1 | 103 | 81.6% | 0% | 0% | 3.9% | MET |
| 2 | 930 | 78.3% | 1.0% | 4.5% | 7.5% | MET |
| 3 | 1,000 | 73% | 0.7% | 2.3% | 19.3% | MET |
| 4 | 999 | 83.1% | 0.7% | 4.0% | 7.6% | MET |

Six prompt revisions applied across batches (see `literature/search-logs/llm-screen-prompt.md`, validation header). paperId fix applied: OpenAlex work ID (`W1234567890`) used as primary key, eliminating batch-2 unmatched-paper bug.

### full-screen-oas.mjs — built and run twice

**Run 1** (combined query, 200-paper Haiku chunks — buggy):
- 6,400 papers fetched (OpenAlex `search=` cursor cap hit)
- 59% escalation rate due to chunk-size bug; results inflated
- 1,480 flagged for human review (not reliable)

**Run 2** (sub-query decomposition, 100-paper Haiku chunks — correct):
- 9 parallel sub-queries (one per CAUSE term), 12,369 unique papers
- 523 flagged for human review (credible)

**Combined master screened.json:** 12,508 papers total; 2,003 for human review (but Run 1 numbers are inflated — see below).

### OpenAlex cursor cap discovery

`search=` caps cursor pagination at ~6,400 results regardless of the 79,727 total. Sub-query decomposition (9 searches, one per CAUSE term, deduplicated by OpenAlex work ID) doubled coverage to ~12,369 unique papers but still cannot reach all 79,727. Remaining papers are lower-relevance by OpenAlex ranking.

### RA emails and repo access

- Shravan (`shravanh7472`): repo was never pushed; fixed, replied with instructions.
- Alexandra (`AlexandraZ27`): GitHub invite expired while traveling; new invite sent, email sent with repo link.
- Both have Write access (confirmed via `gh` CLI).
- Both assigned `literature-search-training.md` exercise due 2026-06-21 10am.

---

## NEXT SESSION: Protocol Redesign + Re-screen

### The Core Problem

Current pipeline delivers ~2,000 papers/hypothesis for human review. At 65 hypotheses = 130,000 abstracts. Unworkable.

**Target:** ~100 papers/hypothesis for human review, with LLM doing the heavy filtering.

### New Three-Stage LLM Pipeline

```
Boolean search (OpenAlex sub-query decomposition)
    ↓  ~12,000 papers
Stage 1: Haiku strict screen  (tightened prompt)
    ↓  ~300–500 papers
Stage 2: Sonnet relevance ranking  (new rank-papers.mjs)
    ↓  top 100 papers
Stage 3: Human title/abstract review
    ↓  ~20–30 papers flagged
Stage 4: LLM full-text analysis
```

### Stage 1: Tighten llm-screen-prompt.md

**Flip the uncertainty tie-breaker.** Change:
> "When uncertain: lean toward RELEVANT (false negatives are more costly than false positives in this pipeline)."

To:
> "When uncertain: mark NOT_RELEVANT. Only mark RELEVANT if there is clear evidence in the title or abstract that the paper directly studies the causal effect of pension/old-age security systems on fertility or childbearing decisions. If you cannot tell, exclude."

**Tighten RELEVANT criteria.** The paper must:
- Directly estimate the pension→fertility effect (empirical study with pension as the treatment variable), OR
- Develop a structural/theoretical model where pension policy is the explicit causal driver of equilibrium fertility

**Demote or remove** criteria that pulled in background/foundation papers:
- OLG models where fertility is endogenous but no pension policy named → NOT_RELEVANT
- VOC framework papers mentioning OAS as one component among many → NOT_RELEVANT unless OAS is the primary focus
- Broad demographic transition surveys → NOT_RELEVANT

**Expected outcome:** pass rate drops from ~8% to ~2–4%, yielding ~250–500 survivors from 12,500 papers.

### Stage 2: Build rank-papers.mjs (does not exist yet)

`.claude/workflows/rank-papers.mjs` — takes `{ slug, inputPath, topN }`:

1. Reads RELEVANT + UNCERTAIN papers from screened.json
2. Sonnet scores each paper on three dimensions (0–10):
   - **Causal quality**: RCT/natural experiment=10, structural estimation=8, panel IV=7, DiD=6, panel OLS=4, cross-sectional=2
   - **Hypothesis directness**: pension/OAS is primary treatment and fertility is primary outcome=10; one of several=5; background=1
   - **Influence**: top journal + seminal status (Neher, Nugent, Ehrlich, Boldrin, Cigno etc.)=10
3. Keep top `topN` (default 100), write ranked list to `literature/search-logs/{slug}-ranked.md`
4. Flag top 20 as priority reads

### Implementation Order Next Session

1. **Revise `llm-screen-prompt.md`** — flip tie-breaker, tighten RELEVANT criteria
2. **Run calibration batch 5** (`calibrate-screen.mjs`, `batchNumber: 5`) to validate new prompt:
   - Target: FN rate still < 3%
   - Target: pass rate drops from ~8% to ~2–4%
   - If FN spikes > 5%, loosen one criterion at a time
3. **Clear Run 1 inflated records** from screened.json (or delete and re-screen fresh):
   ```bash
   # Option: delete and start fresh
   rm literature/search-logs/old-age-security-pension-crowdout-screened.json
   ```
4. **Re-run full-screen-oas.mjs** with new prompt on all 12K papers
5. **Build rank-papers.mjs** and run on survivors → get to ~100
6. **Update PROTOCOL.md §5** to document three-stage design

### Key Files

| File | Status | Notes |
|------|--------|-------|
| `.claude/workflows/calibrate-screen.mjs` | Done | `{ slug, batchNumber, promptPath }` |
| `.claude/workflows/full-screen-oas.mjs` | Done | Sub-query decomp, 100-paper chunks, appends to screened.json |
| `.claude/workflows/rank-papers.mjs` | **NOT YET BUILT** | Build next session — see spec above |
| `literature/search-logs/llm-screen-prompt.md` | Needs revision | Flip tie-breaker, tighten criteria |
| `literature/search-logs/old-age-security-pension-crowdout-screened.json` | Exists (Run 1 inflated) | Clear before re-screen |
| `literature/search-logs/old-age-security-pension-crowdout-routing-rule.md` | Done | Update after batch 5 |
| `PROTOCOL.md §5` | Needs update | Add Stage 2 (LLM ranking) |

### Open Questions for PI

1. **Acceptable FN rate with tighter prompt?** Tightening will increase FNs. Current 0.7% FN was with lenient prompt. Acceptable range with strict prompt: 3–5%? (Missed papers are borderline by definition.) PI should decide the tradeoff before batch 5.

2. **Target N for human review per hypothesis?** Proposal is 100. If tighter screen yields 200–300 survivors, use ranking stage to cut to 100, or accept larger pile?

3. **Re-screen Run 1 papers?** Run 1's 1,480 flagged records are inflated by the 200-chunk bug. Recommend clearing and re-screening all 12K papers with new prompt (~$5 in tokens, ~60 min). Confirm before doing.

---

## RA Meeting — 2026-06-21 10am

Both RAs should arrive with:
1. A hand-crafted boolean search query for ≥2 databases
2. A one-paragraph annotated comparison of the four databases
3. A mock search log entry for their query

Do NOT share queries with each other before the meeting. Anup has the machine-generated version for comparison.

Agenda:
- Compare three query versions (Anup's machine version + Shravan's + Alexandra's)
- Decide on final approved query
- Discuss the new three-stage pipeline and what RA role looks like at Stage 3 (human review of top 100)
