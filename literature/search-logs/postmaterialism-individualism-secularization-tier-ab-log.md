# D.1.a — Tier A and Tier B gold set (GACS A3)

Built by `98_d1a_assemble_gold.py`. Enriched on Semantic Scholar's batch endpoint, not OpenAlex, whose free tier can no longer support bulk work.

## Tier A — anchors, from the existence-gated cold start

- total anchors: **48**
- **empirical (the recall denominator): 31** — CV floor is 30, cleared
- theory and channel-1 reviews (excluded from empirical recall, per A3): 6
- decoys (never counted): 10
- abstracts recovered: 14 of 48
- unresolved, kept title-keyed: 6

## Tier B — the snowball-relevant set, taken whole

- total records: **495** (85 from round 1, 410 new in round 2)
- abstracts recovered: **178** of 495 (36%)
- DOIs present: 385 of 495
- unresolved, kept title-keyed: 62

**Not filtered for keyword-absence**, per A3 and per the round-1 seed decision: filtering Tier B toward keyword-reachable work is what inflated Recall(B) on the OAS and C.2.c runs.

## Tier A / Tier B overlap: 19 records

19 of the 47 Tier-A anchors were also reached independently by the snowball. Tier A was sourced from the OpenAlex keyword probes in `89_`/`90_` and Tier B from a Crossref/S2 citation frame, so the two are orthogonal in source; this number is how far that orthogonality holds in fact, and it is reported because Recall(B) is only a fair yardstick to the extent it does.


---

## Post-backfill state (the frozen numbers)

Appended by `99_d1a_backfill_gold.py`. **Run order `98_` then `99_` is binding** — 98 rewrites this file and the frame from scratch, so 98 alone reverts everything below. Both are cached and idempotent.

| Tier B | at assembly | frozen |
|---|---|---|
| records | 495 | **400** |
| with a DOI | 385 | **321** |
| with an abstract | 178 | **202** (50%) |
| titles that are really citation strings | 27 | **22** |

**95 duplicate works removed post-enrichment.** `98_` deduplicates on the raw snowball title and enrichment then rewrites titles to the provider's canonical form, so records that were distinct strings at dedup time become the same work afterwards — case variants, British against American spelling, and a book indexed once with and once without its author suffix. This inflated the Tier-B count, the A6a positive class, the A6b recall denominator, and the round-2 saturation yield. It can only be caught after enrichment, because before it the two strings genuinely differ.

**79 of 110 no-DOI records were refused by the resolution guard and are kept**, keyed on their original string, because dropping them biases recall toward easy-to-find papers. A hand read shows the residue is book chapters, regional and non-English journals, dissertations and conference papers that Crossref does not hold — the fourth appearance of the same indexing gap on this chapter. The threshold is calibrated rather than merely strict: one refusal at containment 0.78 was a different study with an almost identical title, so relaxing the bar to lift the recovery rate would have assigned a wrong DOI.
