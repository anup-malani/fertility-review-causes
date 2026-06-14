# TICK-009: Implement literature-search.mjs
**Status:** blocked
**Assigned:** any
**Parallel-safe:** yes (with other TICK-009+ work once unblocked)
**Blocks:** TICK-010
**Blocked by:** TICK-001 (need approved pilot hypothesis)

## Description

Implement `.claude/workflows/literature-search.mjs` (workflow #2 in the pipeline).

**Input:** a single approved hypothesis slug from `HYPOTHESES.md`  
**Output:** `literature/search-logs/{slug}.json` — deduplicated list of papers with DOI,
title, abstract, year, venue, relevance score

**Steps the workflow must execute:**

1. Generate search query strings for the hypothesis (3-5 queries per database, varying
   keyword specificity)
2. Execute searches against:
   - OpenAlex (free, no key required)
   - Semantic Scholar (free tier)
   - Crossref (DOI lookup + keyword search)
   - PubMed (for biological hypotheses)
3. Deduplicate by DOI (then by normalized title for DOI-less results)
4. Write to `literature/search-logs/{slug}.json` with schema:
   ```json
   {
     "slug": "...",
     "generated": "ISO-8601",
     "queries": [...],
     "results": [{"doi": "...", "title": "...", "abstract": "...", "year": ..., "venue": "...", "sources": [...]}]
   }
   ```
5. Append to `prisma/{slug}-search-log.md` for PRISMA flow tracking

**Pilot hypothesis:** `old-age-security-pensions`. Run this workflow on that hypothesis
first as calibration before scaling. (Q-Q tradeoff was the original choice but is
high-complexity; old-age security is mid-complexity and better suited for teaching the pipeline.)

## Acceptance criteria
- [ ] Workflow script implemented and not a stub
- [ ] Tested end-to-end on `old-age-security-pensions`
- [ ] Output file written to `literature/search-logs/old-age-security-pensions.json`
- [ ] PRISMA log entry written
- [ ] Results look reasonable (not empty, not hallucinated)
- [ ] Committed

## Log
<!-- Append completion note here when done. -->
