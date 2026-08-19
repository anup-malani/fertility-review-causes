# D.3.c — lower-recall pull options, priced

The full pull is **390,983** records and its screen costs **~$134** (155_), against the project's documented **~$37 per hypothesis** (`decisions/2026-06-20-llm-screening-pipeline.md`). This table prices the ways of buying that down. Pull sizes are **live counts**; gold costs are computed against the 243 gold records carrying an id, using each record's own year and type; dollars re-run 155_'s model at the reduced volume.

| option | pull | vs base | gold recall | gold lost | screen cost | saving |
|---|---|---|---|---|---|---|
| baseline — full recall | 390,983 | +0% | 100.0% | 0 | $134 | $0 |
| year >= 1990 | 328,585 | -16% | 97.9% | 5 | $113 | $21 |
| year >= 2000 | 298,287 | -24% | 91.8% | 20 | $103 | $32 |
| type: broad (7 types) | 346,311 | -11% | 98.8% | 3 | $119 | $15 |
| type: mid (4 types) | 315,678 | -19% | 90.9% | 22 | $109 | $26 |
| 1990 + broad types | 290,603 | -26% | 96.7% | 8 | $100 | $35 |
| 1990 + mid types | 263,335 | -33% | 89.3% | 26 | $91 | $44 |
| 2000 + mid types | 238,189 | -39% | 84.0% | 39 | $82 | $53 |

## What the table says

**The most aggressive option measured — 2000 + mid types — saves $53 and costs 39 of 243 gold records (16.0%).** Every option is a poor trade, and the reason is that the levers available are orthogonal to what makes this corpus big.

A date floor and a type filter both cut *volume*, and volume is cheap: the screen is $134 for 390,983 records, so a 39% volume cut saves about $50. What they cost is *recall*, and recall is the only thing in this chapter that cannot be bought back later. The exchange rate is bad in both directions at once.

## The percentage is the wrong unit

**A recall loss expressed as a percentage is a poor guide when the target cell is small.** The open-database ceiling on this chapter's actual claim — a fertility outcome, a despair construct and an economic treatment together — is **65 records**, and the primary cell is some subset of those. "8% of gold" is a statement about a 243-record provenance proxy; against a 65-record ceiling the same filter might remove five of the studies the chapter rests on, or none. At that scale the variance matters more than the mean, and none of these filters is chosen on the mean.

The date floor is also **not neutral between the two chapters**. B1 measured which records a 1990 floor drops: Duncan and Hoffman (1990) on welfare, economic opportunity and out-of-wedlock births, and the early-1990s teen-childbearing literature — chapter 2's canon, not chapter 1's. The deaths-of-despair framing is recent; the acceleration mechanism's evidence is not. A date floor is a chapter-1 convenience paid for by chapter 2, and the PI's Call 1 ruling made chapter 2 a first-class deliverable rather than an appendix.

## The better lever: cut cost per record, not records

Every option above trades recall for money. **That trade turned out to be unnecessary**, because the
cost is not where the corpus is.

| | input | output | total |
|---|---|---|---|
| D2a (Haiku, ~360k records) | $34 | **$36** | $70 |
| D2b (Sonnet, ~54k records) | $11 | **$54** | $65 |
| | $45 | **$90** | **$134** |

**Output tokens are 67% of the bill.** They are also the one input to the cost that has nothing to do
with how many records are screened or how good the screen is — it is purely how verbose the response
schema is. Emitting `"PRIMARY_MEASURED_DESPAIR"` instead of `"PMD"`, and a one-sentence rationale on
every record instead of only on the uncertain ones, is a budget decision that was never taken
deliberately.

| schema | D2a tok/rec | D2b tok/rec | cost | gold recall |
|---|---|---|---|---|
| verbose (as designed) | 40 | 200 | $134 | 100% |
| short codes | 20 | 200 | $116 | 100% |
| short codes + rationale on `UNCERTAIN` only | 15 | 120 | **$90** | 100% |
| minimal | 12 | 100 | **$82** | 100% |

**$82 at 100% recall against $82 at 84% recall.** The compressed schema reaches the same price as the
most aggressive corpus cut in the table above and gives up nothing. The corpus-cutting options are
strictly dominated and none of them should be taken.

Two details make this safe rather than merely cheap. The codes are expanded back to full cell names
**at collection**, so nothing downstream ever sees a code and no later stage has to know the table.
And the rationale is kept exactly where it is read — on `UNCERTAIN` verdicts, which is the band the RA
gate exists to adjudicate — rather than dropped wholesale.

## Recommendation

**Run the full pull with the compressed schema: ~$82-90, 100% recall.** Implemented in
`156_d3c_screen.py`.

None of the corpus-cutting options should be taken. If the ~$37 line in
`decisions/2026-06-20-llm-screening-pipeline.md` is a hard ceiling rather than a planning figure, the
honest fix is to amend the line — it assumes a conjunction-narrowed corpus of 50K-100K records, which
is exactly what this chapter could not have — and the compressed schema closes most of the gap anyway.
