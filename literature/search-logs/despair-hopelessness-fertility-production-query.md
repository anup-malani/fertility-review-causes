# D.3.c — production query (B1)

**Design: OUTCOME BLOCK ONLY. No treatment conjunction.** The CV established that the conjunction is not a recall-precision trade-off but is strictly dominated — it loses 85% of the gold and has lower precision (16.5% against 20.9%), because decline, inequality and uncertainty vocabulary saturates the decoy clouds of Case & Deaton and the China Syndrome, whose neighbourhoods carry no fertility quantity. All routing moves to the screen.

**49 terms** — 43 a-priori backbone plus the top 10 fold-mined: `fertility`, `fertility intentions`, `childbearing`, `childbearing intentions`, `childlessness`, `term fertility`, `nonmarital`, `teenage`, `births`, `birth`.

## Local recall — tautological here, and reported anyway so that it cannot be misread

**These numbers are 100% by construction and are not evidence that the query is good.** The gold is defined as records carrying a fertility-outcome term in the title, and the query is a list of fertility-outcome terms; the two are the same object viewed twice. A reader seeing four rows of 100% should conclude nothing about retrieval quality.

They are computed and printed for one reason: a value BELOW 100% would mean the compiled query had failed to reproduce its own definition — a compilation or normalisation bug — and that is worth a standing check. Read the table as a build assertion, not a result.

**The real recall number does not exist yet, and cannot until a relevance determination is made.** Tier B is the raw one-hop citation neighbourhood; A3's spec wants the snowball-*relevant* subset as the denominator, and no screen has run. The first honest recall estimate for this chapter comes after the screening wave, measured against records an RA or the screen has judged relevant — not here.

Abstract coverage on the frame is 67% and is **not missing at random** — it is absent for the older sociological monographs, regional journals and grey literature this chapter's canon is unusually full of. One blended title-and-abstract number would measure the covered half and attribute its behaviour to the whole.

| measurement | recall |
|---|---|
| title-only, all gold | 100.0% |
| title-only, records WITH an abstract | 100.0% |
| title-only, records WITHOUT an abstract | 100.0% |
| title+abstract, records WITH an abstract | 100.0% |

(Within that construction the third row is still the one that would bound the operationalisation if the numbers were informative: for records with no abstract the title is all there is, and no amount of abstract-side matching can help them.)

A further **68** primary-neighbourhood records name a fertility outcome in their abstract but not their title. A title-only production query cannot reach them at any breadth; searching title-and-abstract is what buys them, at the cost measured below.

## Two ways to cut the pull: one free, one refused

**The polysemy trim, applied.** Three backbone terms do not denote a fertility outcome when they stand alone as title words, and they are expensive: measured live, bare `tempo` returns 79,809 records (music, physics), bare `parity` 39,631 (physics, computing) and bare `natality` 37,677. They are replaced by the phrase forms that do denote the outcome (`parity progression`, `birth parity`, `tempo effect`, `tempo of fertility`, `crude birth rate`).

This is a different operation from the precision-buying A4 ruled out, and the distinction is the justification. A4 showed no vocabulary separates this chapter's mechanism from its neighbours', so narrowing on the MECHANISM axis costs recall for nothing. This narrows on the OUTCOME axis, removing strings that are not about the outcome in any chapter. **Measured: 546,674 -> 390,983 (28%) at ZERO gold cost**, 247 of 247 matched either way. A trim that costs nothing is not a trade-off.

**The year floor, refused.** The scope's eligibility rule already declined a publication-date floor, on the ground that the acceleration chapter's canon is substantially older than the deaths-of-despair framing. That was an argument; here is the measurement:

| floor | gold lost | share |
|---|---|---|
| 1980 | 1 / 243 | 0.4% |
| 1990 | 5 / 243 | 2.1% |
| 2000 | 20 / 243 | 8.2% |
| 2007 | 38 / 243 | 15.6% |

A 1990 floor would cut the pull by roughly 15% and lose 2% of the gold — and the records it loses are precisely the ones the eligibility rule anticipated: Duncan and Hoffman (1990) on welfare benefits, economic opportunities and out-of-wedlock births, and the early-1990s teen-childbearing literature that is chapter 2's canon. **Not applied.** The deaths-of-despair framing is recent; the acceleration mechanism's evidence is not, and a date floor is a chapter-1 convenience paid for by chapter 2.

## The pull this implies — the deliverable

| operationalisation | live universe | frame records fired |
|---|---|---|
| `title.search` | 390,983 | 1,199 of 10,589 |
| `title_and_abstract.search` | 1,894,348 | 1,601 of 10,589 |

These are **measured counts, not extrapolations** from the citation frame. They are the screening load B1 exists to produce.

The abstract-side operationalisation multiplies the pull by **4.8x** (390,983 -> 1,894,348). Against that it buys the 68 abstract-only records in the frame's primary neighbourhood, plus their unmeasured equivalents in the wider universe.

**Recommendation: run `title.search` for the production pull, and treat the abstract-only residue as a known, quantified gap** rather than paying a 4.8x screening bill to close part of it. The gap is recorded here so it can be revisited if the screen's yield comes in below expectation — which is a decision to take on evidence, after the first screening wave, rather than now.

## What this query is and is not

It is a **recall instrument**. It carries no mechanism vocabulary, makes no attempt at Wall 1, and does not distinguish the two chapters — the chapter split runs on outcome margin at extraction, and the margin terms for both chapters are in the backbone so neither is systematically dropped at retrieval.

It is **not** a precise query and should not be reported as one. Its precision against the provenance-defined gold is ~21% on the frame, and the frame is a citation neighbourhood already enriched for this topic, so precision in the open database will be lower. That is the intended design and its cost is the screening load above.

