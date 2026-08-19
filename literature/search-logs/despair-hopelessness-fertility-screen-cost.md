# D.3.c — two-stage screen: cost model

**Token counts are ESTIMATED from measured characters, not counted.** This environment has no Anthropic credential, so `count_tokens()` — the only correct way to count tokens for a Claude model — could not be run. Character counts are measured exactly over this chapter's 10,589-record Tier B frame and converted at 4.0 chars/token. A sensitivity band is printed because the central value is a guess, and `tiktoken` is not used anywhere: it is OpenAI's tokenizer and undercounts Claude tokens. **Re-run with a key before committing budget.**

## Measured inputs

| quantity | value | source |
|---|---|---|
| production pull | 390,983 | B1, live `title.search` count |
| D1 survivors (projected) | **359,704** | 154, frame survivor share x pull |
| mean title+abstract chars | 725 | measured over the frame |
| abstract coverage | 67% | measured over the frame |
| D2a pass rate (assumed) | 15% | **assumption** — sensitivity below |

## The cascade

**D1 (free)** removes only 8% — see `despair-hopelessness-fertility-d1-rank.md`. It cannot do more without losing gold, because primary-neighbourhood papers largely do not carry mechanism or treatment vocabulary. That is A4's and B1's finding restated at the record level, and it means the paid stages absorb essentially the whole pull.

**D2a — Haiku 4.5, recall-preserving.** 359,704 records in 17,985 batched requests of 20. Rubric (1,500 tokens) is byte-identical across requests and served from cache at ~0.1x after the first.

**D2b — Sonnet 5, precision + extraction.** 53,956 survivors at the assumed pass rate, with the full estimand schema.

## Cost

| conversion | D2a (Haiku) | D2b (Sonnet, intro) | **total (intro)** | total (standard) |
|---|---|---|---|---|
| dense (3.3 c/t) | $76.85 | $66.62 | $143 | $177 |
| **central (4.0 c/t)** | $69.93 | $64.55 | **$134** | $167 |
| light (4.5 c/t) | $66.31 | $63.46 | $130 | $162 |

All figures include the **Batch API's 50% discount**, which applies to the whole job — screening is not latency-sensitive, so there is no reason to pay list price for it.

**Central estimate: $134** for the complete two-stage screen of a 390,983-record pull.

## Two things that move the number more than the estimate error

**1. Sonnet 5's introductory pricing ends 2026-08-31.** $2/$10 per MTok now against $3/$15 after — $64.55 against $96.82 for D2b, a 33% saving on that stage. Today is 2026-08-18, so that is a 13-day window, and it is the one deadline in this chapter that money rather than method depends on.

**2. The D2a pass rate is an assumption, not a measurement.** Everything downstream scales linearly in it:

| D2a pass rate | D2b records | D2b cost (intro) | total |
|---|---|---|---|
| 5% | 17,985 | $21.52 | $91.45 |
| 10% | 35,970 | $43.03 | $113 |
| 15% (assumed) | 53,956 | $64.55 | $134 |
| 25% | 89,926 | $108 | $178 |
| 40% | 143,882 | $172 | $242 |

Even at a 40% pass rate the total stays under a few hundred dollars. **The screening cost is not the constraint on this chapter — which is worth saying plainly, because a 390,983-record pull sounds like it should be.** The binding constraints remain RA time on the boundary cases and the retrieval step for full texts.

## What must be re-measured before spending

1. **Token counts**, with `count_tokens()` against `claude-haiku-4-5` and `claude-sonnet-5` on a representative sample. Everything here scales linearly in that number.
2. **The D1 survivor share**, re-run against the real pull rather than the citation frame (154 states why the frame's share is an upper bound).
3. **The D2a pass rate**, from a calibration run on a few thousand records — which also produces the recall figure D2a is actually gated on.

