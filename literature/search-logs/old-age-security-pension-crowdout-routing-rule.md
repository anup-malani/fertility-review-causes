# Routing Rule: old-age-security-pension-crowdout

**Derived from:** 4 calibration batches — stopping criterion met at batch 4
**Models:** Haiku=claude-haiku-4-5-20251001 (primary), Sonnet=claude-sonnet-4-6 (escalation)
**Haiku FN rate at convergence:** 0.7% (below 3% threshold)
**Haiku FP rate:** 4%

## Routing Logic

1. Screen with Haiku (claude-haiku-4-5-20251001)
2. **RELEVANT + HIGH confidence** → pass directly to human screen queue
3. **RELEVANT + MEDIUM confidence** → pass to human screen queue (flagged)
4. **RELEVANT + LOW confidence** → escalate to Sonnet
5. **UNCERTAIN (any confidence)** → escalate to Sonnet; if still UNCERTAIN, pass to human
6. **NOT_RELEVANT + HIGH confidence** → exclude (log DOI to audit file)
7. **NOT_RELEVANT + MEDIUM or LOW confidence** → escalate to Sonnet

## Cost Estimate for Full Run

Total papers in OpenAlex: 79,727
Estimated Sonnet escalation rate: ~8% (~6,617 papers)

| Component | Cost |
|-----------|------|
| Haiku — all 79,727 papers | ~$51.03 |
| Sonnet — escalated ~6,617 papers | ~$15.88 |
| **Total (routing rule)** | **~$66.91** |
| Pure Sonnet baseline | ~$191.34 |

## Calibration History

| Batch | Papers | Agreement | Haiku FN | Haiku FP | Sonnet Uncertain | Criterion |
|-------|--------|-----------|----------|----------|------------------|-----------|
| 4 | 999 | 83.1% | 0.7% | 4% | 7% | MET |

## How to Apply

Run `screen-titles-abstracts.mjs` with `{ slug: 'old-age-security-pension-crowdout', routingRule: true }` (TICK-010). Results written to `literature/search-logs/old-age-security-pension-crowdout.json` with added fields: `llm_verdict`, `llm_confidence`, `llm_reason`, `llm_model` per paper.
