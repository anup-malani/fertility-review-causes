# D.1.a — channel-3 citation snowball

**Hypothesis:** D.1.a, slug `postmaterialism-individualism-secularization`
**Stage:** GACS Phase A3, channel 3 — the orthogonal Tier-B frame
**Scripts:** `93_d1a_snowball_r1.py` (pull), `94_d1a_relabel_pool.py` (re-score, no network)
**Raw:** `temp/d1a/snowball-r1-pool.json`, `-relabelled.json`, `relabel-diff.md`

---

## Round 1 — complete, with two corrections and one acknowledged gap

| Quantity | Value |
|---|---|
| Records pulled | 2,423 |
| Distinct after normalized-title dedup | 1,970 |
| Relevant (corrected) | **86** |
| Yield per 50 pulled | **1.77** |
| Stop floor (§7.2) | 1.0 |
| Multi-seed overlap | 105 |
| **Saturation** | **not reached — round 2 required** |

Nine seeds, all channel-1 or channel-2. Backward citations from Crossref reference lists, forward
citations from Semantic Scholar.

---

## Provider change: the frame is built off Crossref and Semantic Scholar, not OpenAlex

**Forced.** OpenAlex has moved its free tier to a metered budget. The probe runs in scripts 89 to 92
exhausted a full day's allowance in roughly an hour, and the API began answering `{"error":"Rate
limit exceeded","message":"Insufficient budget ... Resets at midnight UTC"}`. A snowball is an order
of magnitude more requests than a probe, so it could not run there. **The six `UNCONFIRMED` rows in
the canon-seed resolution (92) are this, not missing papers** — the three-state discipline held the
line correctly, for the second time in one day.

**Also better, and worth keeping after the budget resets.** PROTOCOL §5.1 already names Semantic
Scholar and Crossref as Phase 2b citation sources. Building the Tier-B frame on a *different provider*
than the one that produced Tier A makes the frame orthogonal in infrastructure as well as in method,
so Recall(B) measured against it is a stronger test than one measured inside OpenAlex's own graph.
Recommended as the standing arrangement rather than a workaround.

**Operational note for every chapter:** unauthenticated Semantic Scholar throttles hard and returned
`Too Many Requests` partway through this run. An API key should be requested before the next chapter's
snowball.

---

## The relevance filter was wrong in both directions, and a hand audit is what caught it

The C.2.c run left a standing requirement: read a random sample of what the relevance filter admits
before trusting any saturation number. A 45-record hand read found two bugs.

**Bug A — false positives.** `reproduc\w+` on the outcome axis admits *social* reproduction and
*reproductive health*, neither of which is a fertility outcome. It scored Bourdieu's *Reproduction in
Education, Culture and Society* as an on-pair record, along with church-led adolescent
sexual-and-reproductive-health programmes and an anthropological critique titled "Culture and
Reproduction." Left alone it would have admitted the whole sociology-of-education and SRH-services
literatures. This is D.1.a's version of the C.2.c bug where bare `hous` and `rent` matched
h**ous**ehold and pa**rent**.

**Bug B — false negatives, and the more damaging of the two.** Quoted phrases were carried from
OpenAlex query syntax into a Python verbose regex, where `"second\s+demographic\s+transition"` matches
only text containing literal double-quote characters. **The chapter's single most central phrase
therefore never matched anything.** "An alternative perspective on the Second Demographic Transition
in East Asia" was rejected for having no treatment term. `"family size"` and `"number of children"`
failed the same way on the outcome axis.

**Corrected: 79 → 86 relevant, yield 1.63 → 1.77 per 50.** Six removed, thirteen gained, both sets
hand-checked in `temp/d1a/relabel-diff.md`. The net movement is small and the *direction* is the
point: the filter was simultaneously admitting the sociology of education and rejecting every paper
that named the Second Demographic Transition. An aggregate that moves by seven records concealed two
errors that would each have distorted the frame.

**The generalisable lesson is a narrower version of C.2.c's.** That run concluded a stop rule is only
as good as the relevance classifier feeding it. This run adds: a classifier can be wrong in both
directions at once, and the two errors partially cancel in the aggregate, so the summary statistic is
the last place either will show up. Only a hand read of admitted *and* rejected records finds both.

---

## Seed error, self-inflicted, and the gap it leaves

**van de Kaa 1987 — the most-cited SDT statement in the field, roughly 1,950 citations — contributed
2 forward citations to this round, because the seed DOI was wrong.** The canon resolver in script 92
had resolved it correctly and reported that the work carries **no registered DOI** (OpenAlex
`W63025791`). I then hand-typed `10.2307/2057518` into the seed table rather than reading the
resolver's output. It resolved to a different record.

This is the identical failure the whole existence-gate discipline exists to prevent, committed inside
my own seed table one step after building the gate. Two things follow:

1. **The round-1 frame under-reaches the SDT demography family** by approximately the citation
   neighbourhood of its central work. The 1.77 yield is measured on an incomplete pull and should be
   read as a lower bound on coverage, not as a stable saturation reading.
2. **Seed tables must be generated from resolver output, never typed.** The fix for round 2 is to have
   93 read its seeds from `temp/d1a/canon-seeds.json` and to seed identifier-less works by Semantic
   Scholar title lookup rather than by a fabricated DOI. Recorded as a process change, not just a
   correction.

Round 2 must therefore do three things: re-seed van de Kaa properly, add the round-1 relevant records
as second-generation seeds, and re-measure yield on the completed pull.

---

## Seed selection: canonical status is not the criterion

Hofstede 1980 (15,158 citations) and Schwartz 1992 both resolve, and neither is seeded. Their citation
neighbourhoods are the management and cross-cultural-psychology literatures — they are canon for a
*construct*, not for this treatment × outcome pair — and seeding them would bury the frame in off-pair
records and make the yield statistic meaningless. **The seed criterion is the specificity of the
citation neighbourhood, not the fame of the work.**

The obvious alternative fix, keyword-filtering the frame down to fertility papers, is **refused on
purpose**: it would bias Tier B toward keyword-reachable work and inflate Recall(B), which is exactly
the error the OAS and C.2.c runs were burned by. A frame that is expensive to screen is the price of a
frame that can measure recall honestly.

Separately, the resolver flagged **Schwartz 1992 as resolving to the wrong paper** — "Individual
values and delinquency" (2016, 35 citations) rather than the 1992 *Advances in Experimental Social
Psychology* chapter. It carries `RESOLVED_DISCREPANT` and must not be treated as verified.

---

## Seed-level detail

| Seed | Channel | Family | Backward | Forward |
|---|---|---|---|---|
| Zaidi & Morgan 2017 | ch2 | demography-SDT | 118 | 257 |
| Lesthaeghe 2020 (Genus) | ch2 | demography-SDT | 99 | 21 |
| Lesthaeghe 2014 (PNAS) | ch2 | demography-SDT | 22 | 571 |
| Fernández, *Does Culture Matter?* | ch2 | econ-of-culture | 52 | UNCONFIRMED |
| SSA religions review 2023 | ch1 | sociology-of-religion | UNCONFIRMED | 9 |
| SSA religion/religiosity review 2021 | ch1 | sociology-of-religion | 0 | UNCONFIRMED |
| **van de Kaa 1987** | ch2 | demography-SDT | 0 | **2 — WRONG SEED, see above** |
| Lesthaeghe & Surkyn 1988 | ch2 | demography-SDT | 0 | 600 (cap) |
| Norris & Inglehart 2004 | ch2 | sociology-of-religion | 515 | 157 |

Three `UNCONFIRMED` cells are Semantic Scholar throttling and one is the unregistered-DOI review;
none is evidence of absence. Lesthaeghe & Surkyn hit the 600 forward cap and has more available.

---

## What round 1 tells us about the literature

**The overlap rate is 105 of 1,970, about 5%.** C.2.c found overlap rate is not a convergence signal
under expanding seeds, so it is recorded here as a descriptive statistic rather than a stop criterion.
At 5% the nine seeds are reaching largely disjoint neighbourhoods, which is consistent with the
scope's prediction of four barely-overlapping vocabulary families and argues against declaring
saturation early.

**The frame is dominated by demography-SDT.** Six of nine seeds sit in that family, and the
sociology-of-religion empirical literature is reached mainly through Norris and Inglehart. The
economics-of-culture family is represented by one seed whose forward pull failed. Round 2 needs seeds
from the under-reached families, which is the same correction C.2.c had to make after its round 1.
