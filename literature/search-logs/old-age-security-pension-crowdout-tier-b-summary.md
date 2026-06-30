# Tier B — screened (Part 2)  ·  2026-06-29

Unbiased orthogonally-sourced relevant set (definition 1), DOI-resolved via the OpenAlex citation graph, then precision-audited by a 6-agent relevance screen. Dead/drifted-W-ID papers retained as title-keyed (unbiasedness decision). Agent/web DOI resolver BANNED here.

## Counts

- frame (resolved): 319
- **Tier B core (RELEVANT): 247**  (DOI-keyed 114, title-keyed 133)
- UNCERTAIN -> RA adjudication queue: 52
- NOT_RELEVANT dropped (citation noise): 20

## Combined gold set

- Tier A (draft): 56
- Tier B core: 247
- **Total gold (A + B core): 303**  (+ 52 Tier-B UNCERTAIN pending RA)

## Caveats

- ~40% of the frame is title-keyed (snowball-corpus W-ID rot); title-based recall matching is fuzzier than DOI matching. Resolution-failure was retained (not dropped) to avoid biasing Tier B toward findable papers.
- The snowball was seeded off the (keyword-sourced) PI relevant set, so Tier B is *less* keyword-biased than Tier A but not perfectly independent — state this when reporting Recall(A)-Recall(B).
- UNCERTAINs are NOT in the frozen core; RA must adjudicate them into R/NR before the final recall numbers, since auto-dropping would reintroduce findability bias.
