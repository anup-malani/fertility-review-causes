# D.1.a — can free metadata shrink the full-text queue? A backfill probe

**The answer is no, and that is the useful result.** `113_` projected ~1,909 UNCERTAIN records, each
one a full-text read, and roughly three-quarters of that pile is a missing or unusable abstract
rather than a contested design. If another free index held those abstracts, the screen's downstream
cost would fall by most of that queue. Crossref and Europe PMC do not hold them.

| stratum | n | hits | rate | crossref | epmc | no DOI | no abstract | errors |
|---|---|---|---|---|---|---|---|---|
| **A — UNCERTAIN, title-only** | 32 | 1 | **3.1%** | 0 | 1 | 10 | 19 | 2 |
| **B — random title-only** | 200 | 18 | **9.0%** | 3 | 15 | 71 | 110 | 1 |

Stratum A is the number that governs. At 3.1%, backfilling every title-only record in
the corpus would remove on the order of tens of reads from a queue of ~1,900. It is not a lever.

## Why the coverage is this bad

OpenAlex is at the practical free-tier ceiling for this corpus, not behind it. Of the
5088 title-only records queued, 1869 (36.7%) carry no
DOI at all and so have no lookup key in any DOI-keyed index. Of those that do, most are the kinds of
record for which publishers never deposited an abstract: pre-1990 articles (19.6% of the stratum),
book chapters, dissertations, and regional journals. Hand-checking misses confirms the absence is
real at Crossref rather than an artefact of this probe.

**One channel is deliberately not tested, and it is bounded.** 187
(3.7%) of title-only records carry DataCite-registered DOIs (Zenodo,
SSRN, OSF), which Crossref returns 404 for and this probe counts as a miss. Even at implausible 100%
recovery that channel is ~187 records, of which ~12% would be UNCERTAIN — roughly
22 reads. It does not change the decision.

## What this settles for the screen decision

The ~1,900-read queue is real and cannot be bought down upstream for free. The screen decision is
therefore what `113_` said it was — volume against a retrieval budget — with the metadata escape
route now closed rather than merely untried.

## An incidental check that came back clean

Title-only records return RELEVANT at 1/127 in the sample against 19/273 for records with abstracts,
a 9× gap that would be alarming if it meant the screen cannot recognise a relevant record without an
abstract. Reading the 94 title-only NOT_RELEVANT decisions, it does not: they are overwhelmingly
query noise matched on bare stems — dairy-cow fertility, "The Birth of Tissue Culture", a Nigerian
admissions advertisement. The gap is the composition of the title-only stratum, not screen
under-detection. Rejects were read, not just admits.
