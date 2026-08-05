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

`99_d1a_backfill_gold.py` rewrites the Tier-B frame in place after this script builds it. **The run
order `98_` then `99_` is binding** — 98 alone silently reverts the backfill and the frame still looks
complete. Both are cached and idempotent, so the pair reproduces the frozen artifact exactly.

| Tier B | at assembly | frozen |
|---|---|---|
| records | 495 | 495 |
| with a DOI | 385 | **416** |
| with an abstract | 178 (36%) | **251 (51%)** |
| titles that were really citation strings | 27 | **22** |

## What the unresolvable residue actually is, and why it is kept

79 of the 110 records without a DOI were **refused** by the resolution guard and are kept in the frame
and in the recall denominator, keyed on their original string. A hand read of the refusals shows they
are overwhelmingly **book chapters, regional and non-English journals, dissertations, and conference
papers** — Crossref does not hold them, and no threshold change would recover them. This is the fourth
independent appearance of the same non-Anglo-European, non-journal indexing gap on this chapter, after
the AJRH unregistered DOI in `91_`, the `NOT_INDEXED` regional reviews in `96_`, and the
Dutch-language Lesthaeghe and van de Kaa 1986 that three providers could not resolve. It runs in the
same direction as the scope's geographic-skew limitation and should be carried into §10.

**The guard's threshold is calibrated, and the rejected sample is what shows it.** The clearest case:
*"Attitudes toward fertility and childbearing among childless female teachers ... in Gorgan"* drew a
Crossref candidate titled *"Attitudes toward fertility and childbearing among female University
students"* at containment **0.78**, just under the 0.80 bar. Same title family, same year, **different
study and different population**. Relaxing the threshold to 0.75 to lift the recovery rate would have
assigned that record the wrong DOI — which is precisely how the OAS run acquired a 40%-ghost Tier B.
A low recovery rate is the correct outcome when the records genuinely are not indexed.
