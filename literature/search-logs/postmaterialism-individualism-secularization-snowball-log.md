# D.1.a — channel-3 citation snowball

**Hypothesis:** D.1.a, slug `postmaterialism-individualism-secularization`
**Stage:** GACS Phase A3, channel 3 — the orthogonal Tier-B frame
**Scripts:** `93_d1a_snowball_r1.py` (round 1), `96_d1a_snowball_r2.py` (round 2),
`97_d1a_rescore_pools.py` (re-score both pools, no network),
`95_d1a_canon_reresolve.py` (seed resolution)
**Shared modules:** `d1a_relevance.py` (the one relevance definition), `d1a_fetch.py` (the one fetcher)
**Raw:** `temp/d1a/snowball-r{1,2}-pool-scored.json`, `temp/d1a/rescore-audit.md`

---

## Both rounds, scored under relevance filter v3

| | Round 1 | Round 2 |
|---|---|---|
| Records pulled | 2,423 | 11,610 |
| Distinct after normalized-title dedup | 1,970 | 8,558 |
| New vs. the previous round | — | 7,652 |
| **Relevant (new)** | **85** | **410** |
| **Yield per 50 pulled** | **1.75** | **1.77** |
| Stop floor (GACS §7.2) | 1.0 | 1.0 |
| **Saturation** | not reached | **not reached** |

Round 2 splits into a repair leg and an extension leg, and they are measured separately because they
answer different questions.

| Leg | Pulled | New relevant | Yield / 50 |
|---|---|---|---|
| **A — repair of round 1's incomplete pull** | 2,080 | 22 | 0.53 |
| **B — generation 2** (8 new canon seeds + 82 round-1 relevant records) | 9,530 | 383 | 2.01 |

Tier B now stands at **495 relevant records** (85 + 410).

---

## The stop rule and the depth cap now disagree, and it needs a PI decision

Two committed rules give opposite answers here and the conflict has not arisen before because no
previous chapter reached round 2 above the floor.

- **GACS §7.2** stops on *two consecutive rounds* below 1.0 new relevant per 50. Both rounds are
  above it, and round 2's extension leg is at 2.01 — the frame is not converging, it is accelerating.
- **PROTOCOL §5.1** caps snowball depth at **2 rounds**, citing Wohlin 2014, on the grounds that
  "round 3 returns less than 5% new material." That prediction is false here: round 2 returned 7,652
  records unseen in round 1, against a round-1 pool of 1,970.

So the depth cap says stop and the yield rule says continue. **Round 3 is not run** — the cap is the
narrower committed constraint and an RA should not spend it unilaterally — and the choice is escalated
with the numbers attached. The substantive question is whether the D.1.a frame is genuinely
non-convergent or whether generation-2 seeding inflates yield mechanically, since seeding 82 on-pair
papers guarantees on-pair neighbourhoods. **The honest reading is that round 2's 1.77 is not
comparable to round 1's 1.75**: round 1 was seeded from 9 framework statements and reviews, round 2
from 82 papers already known to be on-pair. A yield that stays flat while the seed set becomes far
more on-pair is weak evidence of saturation, not strong evidence against it. Recorded as a limitation
on the statistic rather than resolved here.

---

## The repair leg: the round-1 seed error cost less than it looked like it would

Round 1 recorded that van de Kaa 1987 — the most-cited SDT statement in the field — contributed **2**
forward citations because the seed table carried a hand-typed DOI for a work that has none, and that
its 1.75 was therefore "a lower bound on coverage, not a stable saturation reading."

**Repaired: 2 → 1,316 forward citations**, seeded by Semantic Scholar paperId read from `95`'s
resolver output. Lesthaeghe and Surkyn 1988, which hit round 1's 600-record cap, was pulled uncapped
to 764. Both were pulled uncapped on purpose; fixing a seed and then truncating it at 46% of its
neighbourhood would have left the same gap, smaller.

**The result is reassuring and slightly deflating: only 22 relevant records were reachable *solely*
from the repaired seeds**, a yield of 0.53 per 50 — below the floor. The SDT demography family is
densely cross-citing, so round 1's other five SDT seeds had already covered most of van de Kaa's
neighbourhood. **Round 1's 1.75 was therefore not materially biased by the seed error.** That does not
retire the process change it produced — seed tables are generated from resolver output, never typed,
and `96` reads its seeds from `95`'s JSON — but it does size the damage honestly rather than leaving
the round-1 warning standing as if unresolved.

---

## Four states, not two: what a zero in this table means

Round 1 reported seed cells as `OK` or `UNCONFIRMED`. That is too few states, and collapsing them
manufactured absences. Round 2 distinguishes:

| State | Meaning | Cells |
|---|---|---|
| `OK` | the provider answered with records | — |
| `UNCONFIRMED` | the provider did not answer — a fact about the **network** | **0** |
| `NOT_INDEXED` | the provider answered and does not hold this work — a fact about the **index** | 9 |
| `NO_REFS_DEPOSITED` | Crossref holds the work; the publisher deposited no reference list | 15 |

**All three of round 1's `UNCONFIRMED` cells were actually `NOT_INDEXED`.** They were never going to
resolve on a retry, and the round-1 log's hope that they would was misplaced:

- **Fernández, *Does Culture Matter?*** — Semantic Scholar does not index this Handbook chapter at
  all. It was the economics-of-culture family's **only** seed, and round 1 attributed that family's
  under-reach to a failed pull. It is an indexing gap, not a thin literature, and the fix was to seed
  the family through Enke 2019 instead.
- **Both sub-Saharan Africa reviews** are absent from the provider each was queried against. The AJRH
  2023 review is the same record `91` recorded as `VERIFIED_TITLE_KEYED` — a real paper whose DOI was
  never registered with Crossref. **This chapter has now hit the non-Anglo-European indexing gap from
  three independent directions**, and it runs in exactly the direction of the geographic-skew
  limitation already in the scope.

`NO_REFS_DEPOSITED` matters for the same reason. Lesthaeghe 1983 in *PDR* returns zero references and
obviously has them; Crossref reference deposition is optional and widely skipped. A backward count of
0 is a statement about a publisher's metadata, never about a paper citing nothing.

---

## Three transport bugs, each of which reported missing data as measured data

All three were found in one session, and all three fail in the direction that looks like a finding.

**1. A throttle cached as a successful empty pull.** Semantic Scholar answers a rate limit with
`{"message": "Too Many Requests. Please wait and try again...", "code": "429"}`. The guard tested
`message == "Too Many Requests"` — equality against a *prefix* of the real message. It never fired, so
the 429 body was cached as a valid response and the caller read `data or []` off it and recorded zero.
It surfaced only because the first seed it hit was van de Kaa, where `n=0` was obviously wrong; on any
of the 82 generation-2 seeds it would have looked entirely normal.

**2. A rate-limit detector that matched a timestamp.** The fix for (1) scanned response bodies for
markers including a bare `"429"`. That substring occurs inside the Unix timestamp `1429894924000` in
Crossref's record for Inglehart 1977, so valid responses were classified as throttles, retried six
times, and recorded as `UNCONFIRMED`. **This is the third instance in this codebase of an unanchored
substring match against text that was never meant to be searched** — after `hous` matching
h*ous*ehold in C.2.c and `reproduc\w+` matching social reproduction in this chapter's v1 filter — and
the first inside the transport layer, which is why it presented as a network symptom rather than a
screening error. Fixed by making the **HTTP status code** the primary signal and demoting body
sniffing to a fallback for providers that answer 200 with an error payload.

**3. Reactive backoff cannot survive an unauthenticated rate limit.** Exponential backoff alone meant
that once S2 began refusing, every subsequent request also refused and burned the full retry ladder
(~113s) before returning `UNCONFIRMED`. The run reached generation-2 seed 6 of 82 in seven minutes and
would have recorded most of the remainder as missing literature. Replaced with **proactive pacing** —
a minimum interval per host — after which the same run completed with **zero** throttle retries.
**An API key for Semantic Scholar remains the outstanding operational request**, now for the second
chapter running.

---

## The relevance filter, versions 2 and 3, and why a fix is not evidence for itself

The standing requirement from C.2.c — read a sample of what the filter admits *and* rejects before
trusting any saturation number — has now caught a defect on all three passes.

**v2** came out of hand-reading the audit sample v1 left behind. `culture|cultural` was matching
**design descriptors**: `cross-cultural` is a sampling frame and not a value measure, and it had
admitted a sociosexual-orientation paper whose treatment belongs to a different chapter. Seventeen of
round 1's 86 relevant records hung on `culture`/`cultural` alone, so a fifth of the frame was exposed
even though only two records were actually wrong. The naive fix — reject anything containing a design
descriptor — was **tested and rejected**, because it drops *"Journal of Cross-Cultural Psychology:
Value of Children"*, which is squarely on-pair and whose descriptor sits in the venue name. Replaced
by **strip-then-rematch**: delete the idiom spans, then test what survives.

**v3 corrects v2, and the reason is the most transferable thing here.** v2 also treated
`socio-cultural` and `cultural evolution` as design descriptors. Across round 1's 3 affected records
that looked right. Across round 2's 43 it was plainly wrong — roughly half were on-pair records being
discarded: *"Socio-Cultural Practices and Fertility Behavior among Banyankole Families"*, *"How
socio-cultural factors and opportunity costs shape the transition to a third child"*, and Colleran and
Mace's *"The cultural evolution of fertility decline"*, which is cultural transmission of fertility
norms and is exactly this chapter's treatment. `cross-cultural` describes the **sample**;
`socio-cultural` is an ordinary adjective for the **thing measured**.

**Each version was validated on the sample available when it was written, and each was wrong in a way
that only appeared at the next order of magnitude.** v1 was audited on 45 records and shipped two
bugs. v2 was validated on the 3 records its change touched and shipped a false-negative class that
needed 43 records to become visible. The sample that produces a hypothesis cannot also test it.

Both pools are re-scored under v3 by `97_`, because round 1 at v2 and round 2 at v3 would produce a
change in yield that is partly a change in the literature and partly a change in the ruler.

---

## Seed-level detail, round 2

| Seed | Leg | Family | Backward | Forward | Note |
|---|---|---|---|---|---|
| van de Kaa 1987 | A | demography-SDT | 0 | **1,316** | repaired; seeded by S2 paperId, no DOI exists |
| Lesthaeghe & Surkyn 1988 | A | demography-SDT | — | 764 | round-1 cap lifted |
| Fernández, *Does Culture Matter?* | A | econ-of-culture | — | `NOT_INDEXED` | not in S2 at all |
| SSA religions review 2023 | A | sociology-of-religion | `NOT_INDEXED` | — | unregistered DOI |
| SSA religion/religiosity 2021 | A | sociology-of-religion | — | `NOT_INDEXED` | OSF preprint |
| Frejka & Westoff 2008 | B1 | sociology-of-religion | 47 | 194 | v5 seminal; `92` left it UNCONFIRMED |
| McQuillan 2004 | B1 | sociology-of-religion | 106 | 463 | |
| Hagestad & Call 2007 | B1 | sociology-of-religion | 50 | 82 | v5 seminal; rescued by `95`'s subtitle gate |
| Lesthaeghe 1983 | B1 | demography-SDT | `NO_REFS` | 600 (cap) | v5 seminal, resolved in `92`, never seeded |
| Enke 2019 | B1 | econ-of-culture | `NO_REFS` | 68 | the family round 1 reached with one dead seed |
| Voas 2009 | B1 | sociology-of-religion | 11 | 474 | **judgement call** |
| Inglehart 1977 | B1 | values-psychology | `NO_REFS` | 600 (cap) | **judgement call** |
| Inglehart & Baker 2000 | B1 | values-psychology | 57 | 600 (cap) | **judgement call**; twin DOIs, both pulled |
| 82 round-1 relevant records | B2 | gen2 | — | — | forward capped at 200 each |

**Seeds truncated by a cap, named rather than buried:** Lesthaeghe 1983, Inglehart 1977, Inglehart &
Baker 2000, and two generation-2 seeds (*Cultural and Economic Approaches to Fertility*, *When Does
Religion Influence Fertility*). Two round-1 relevant records carried neither a DOI nor an S2 id and
could not be seeded at all.

**The three judgement calls are recorded as judgement calls.** Voas 2009 and the two Inglehart works
sit closer to construct canon than to pair canon, which is the criterion round 1 used to exclude
Hofstede and Schwartz. They were seeded anyway because postmaterialism and individualism have no
channel-1 review and no seed of any kind, so refusing them makes those strata unreachable through
channel 3 entirely. They did not swamp the frame. Round 1's exclusion criterion — **specificity of the
citation neighbourhood, not fame** — otherwise holds unchanged, and it is worth noting that all four
construct-canon works excluded under it are also the four that failed to resolve cleanly in `95`.

---

## Canon seed resolution moved off OpenAlex permanently

Round 1 recorded six `UNCONFIRMED` rows in `92` as OpenAlex budget exhaustion and instructed the next
session to re-run after the reset. **That re-run was attempted and returned `UNCONFIRMED` on all
sixteen rows.** The budget had reset; it is simply too small to run the resolver — a title search
costs $0.001 against a daily free allowance that does not cover sixteen of them, while a single-work
fetch by ID still succeeds.

So the finding is sharper than round 1's "OpenAlex has moved to a metered budget": **the free tier can
no longer support channel-2 canon resolution at all, and no amount of waiting fixes it.** Every
chapter's resolver needs to move, not just this one's. `95` re-resolves every row against **both**
Crossref and Semantic Scholar, and reports cross-provider agreement as its own field. Full detail in
`{slug}-canon-reresolution.md`; four results matter here.

**1. Two v5 seminal names that `92` could not confirm are real.** Frejka and Westoff 2008 resolves on
both providers. Hagestad and Call 2007 resolves on Crossref with 82 citations — see (2).

**2. A Jaccard title gate false-negatives on subtitle drops, and this one nearly cost a v5 seminal
name.** Hagestad and Call was queried as *"Pathways to childlessness: a life course perspective"* and
is indexed as *"Pathways to Childlessness"*. Jaccard divides by the union, so four extra query tokens
against three shared ones gives 0.43 — under the 0.55 gate — for a record whose **both author surnames
and year match exactly**. It would have been recorded as a second v5 seminal name that does not exist.
Containment of the shorter title is 1.0. **Every resolver in this tree gates on Jaccard alone and will
fail the same way**; worth propagating alongside `91`'s false-ghost fix.

**3. One work, two registered DOIs, citations split across them.** Inglehart and Baker 2000 is
`10.2307/2657288` (JSTOR, 2,454 citations) and `10.1177/000312240006500103` (SAGE, 5,379) — one *ASR*
article. This is the NBER/SSRN twin problem from C.2.c appearing **inside the canon seed table**.
Both are seeded; dropping either loses whatever share of the forward neighbourhood cites that version.

**4. Cross-provider agreement is not a correctness guarantee, demonstrated in the run that introduced
it.** Crossref and S2 **agree** on Hofstede 1980 — and both resolve it to a 1982 *Design Studies* book
review by Sydney Gregory rather than to Hofstede's book. Providers sharing upstream metadata agree on
shared errors. Hofstede is deliberately not seeded, so nothing operational turns on it, but the caveat
belongs next to the method.

---

## Round 3, if it is authorised

1. Seed the families still reached through a single work: econ-of-culture rests on Enke 2019 alone
   now that Fernández is known to be unindexed.
2. Re-seed the two `NOT_INDEXED` regional reviews by title against a provider that holds them, rather
   than by DOI against one that does not.
3. Lift the generation-2 forward cap on the two truncated gen-2 seeds and on the three capped canon
   seeds before treating any yield number as converged.
