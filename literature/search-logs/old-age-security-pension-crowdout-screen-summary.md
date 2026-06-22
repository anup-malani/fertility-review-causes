# LLM Screening Summary: old-age-security-pension-crowdout

**Date:** 2026-06-20
**Pipeline:** Two-stage LLM screen (Haiku primary, Sonnet escalation)
**Primary model:** claude-haiku-4-5-20251001
**Escalation model:** claude-sonnet-4-6
**Hypothesis:** Old-age security / pension crowdout of fertility

## This Run (2026-06-20)

| Metric | Count |
|--------|------:|
| New papers screened | 6,232 |
| RELEVANT | 394 |
| NOT_RELEVANT | 5,709 |
| UNCERTAIN | 129 |

**Next step:** Human title/abstract screen of RELEVANT + UNCERTAIN papers (523 papers: 394 + 129) before full-text retrieval.

## Cumulative Results (Master Output)

| Verdict | Count | Pct |
|---------|------:|----:|
| RELEVANT | 941 | 14.7% |
| NOT_RELEVANT | 4540 | 70.9% |
| UNCERTAIN | 919 | 14.4% |
| **Total** | **6400** | 100% |

## Pipeline Details

- **Papers retrieved:** 6400
- **Stage 1 (Haiku):** 6400 papers screened
- **Stage 2 (Sonnet escalations):** 2763 papers re-screened
- **Final verdict source:** Sonnet for 2763 papers; Haiku for remaining 3637

## Output Files

- Screened JSON: `literature/search-logs/old-age-security-pension-crowdout-screened.json`
- Each record: `{paperId, title, doi, year, journal, url, haiku_verdict, haiku_confidence, llm_verdict, llm_confidence, llm_reason, llm_model}`

## Next Steps

1. **Human title/abstract screen** of RELEVANT + UNCERTAIN papers (1860 papers total)
2. Full-text review of surviving papers
3. Data extraction into `extraction/` database
4. GRADE rating per phenomenon (pre-modern variation, FDT, SDT)
