# Snowball log — A.23 co-residence and delayed household formation

**Ticket:** TICK-075 · **Round 1 run:** 2026-08-27
**Scripts:** `217_a23_snowball.py` (pull), `218_a23_pool_diagnostics.py` (measurement)
**Outputs:** `…-snowball-pool.json` (2,584 records), `…-snowball-round1.json`,
`…-pool-diagnostics.json`

Channel 1 came back dry for this hypothesis — no prior systematic review or meta-analysis of the
living arrangement and fertility exists — so channel 3 carries more of the recall burden here than it
normally would, and the production query will be scored mainly against this frame.

## 1. What was run

All 30 anchors that cleared the existence gate were resolved to OpenAlex (30/30) and snowballed
backward and forward. Decoys were seeded in both directions, per the standing rule; the two
configurations of Ruling 1 were seeded and tagged separately so the frame's balance could be read off
the output rather than assumed.

| | |
|---|---|
| Seeds resolved | 30 / 30 |
| Pool after dedup | **2,584** |
| Reached by ≥2 seeds | 282 |
| Duplicates collapsed (normalized title, published version kept) | 77 |
| No DOI | 216 |
| Preprints | 96 |
| Errors | 0 |

## 2. The forward cap, stated rather than buried

The forward pull was capped at 200 citing works per seed, sorted by citation count. **Four seeds hit
the cap and 1,483 citing works were not pulled.**

| Seed | Pulled / total | What it is |
|---|---|---|
| `10.2307/2807972` | 200 / 1,359 | Reher 1998 — theory, and a Wall 3 decoy |
| `10.1353/foc.0.0038` | 200 / 469 | Furstenberg 2010 — the field's nearest thing to a review |
| `10.1002/ijpg.231` | 200 / 253 | *Leaving Home in Europe* — link-1 anchor |
| `10.2307/353569` | 200 / 202 | filial responsibility — elder-support decoy |

Because the sort is by citation count, each capped pull is the **high-citation head, not a sample**.
Two of the four are decoys whose tails this chapter does not want. The two that matter are Furstenberg
and *Leaving Home in Europe*, both on the pre-launch side, and **their tails should be paged in round 2
if pre-launch recall falls short** — which, on §4 below, it is likely to.

## 3. The decoy channel underperformed here, and the measurement says why

The standing expectation, from earlier chapters, is that decoy clouds run far more on-topic than a
theory canon and that refusing to forward-seed them discards the best channel. **On A.23 that does not
replicate.** Scoring on titles — all the pool carries, so every figure is a floor:

| Group | n | exposure (pre-launch) | exposure (extended) | fertility outcome | both axes | elder-care vocabulary |
|---|---|---|---|---|---|---|
| Whole pool | 2,584 | 11.7% | 9.4% | 15.3% | 1.6% | 8.7% |
| **Reached only via decoy seeds** | 489 | 6.5% | 11.0% | 6.7% | **0.6%** | **20.2%** |
| Reached via a non-decoy seed | 2,095 | 12.9% | 9.1% | 17.3% | **1.9%** | 6.1% |
| Reached by ≥2 seeds | 282 | 18.1% | 21.3% | 26.6% | 8.2% | 5.3% |

The decoy-only cloud is roughly three times *less* on-topic than the rest and carries three times the
elder-care vocabulary. The reason is visible in the seed list: two of this chapter's four decoys are
**homonym decoys**, so their citation clouds are the homonym literature itself. A decoy that marks a
*boundary* pulls in boundary cases; a decoy that marks a *homonym* pulls in the other construct.

**The rule to carry forward is not "seed decoys" or "don't" — it is that a decoy's cloud is worth what
the decoy marks.** The 489 records stay in the pool and stay tagged; they are the material the screen
needs to learn the §6 wall on. But they are not a recall channel for this chapter, and round 2 should
not spend seeds there.

## 4. The asymmetry found in anchor sourcing replicates in the citation network

| Cloud | n | fertility outcome in title | both axes in title |
|---|---|---|---|
| From the 3 pre-launch seeds | 219 | 11.4% | **0.0%** |
| From the 15 extended-household seeds | 809 | 30.5% | 4.0% |

**Not one record in the pre-launch cloud carries both an exposure and a fertility term in its title.**
Anchor sourcing found that the identified designs sit almost entirely in the extended-household arm;
the citation network now says the same thing independently, and more starkly. The pre-launch
literature is real and large, and it connects to home-leaving, union formation and the transition to
adulthood — not to births.

This is the §3 problem showing up as a bibliometric fact rather than an argument: the field studies
the transition, not its fertility consequence.

## 5. A route-out the scope did not name, and now must

The pool's centre of gravity — the most-seeded records — is not what either configuration predicted:

```
s=7  Grandparents Caring for their Grandchildren                       (2008)
s=6  Family proximity, childcare, and women's labor force attachment    (2013)
s=6  Grandparenting and mothers' labour force participation             (2012)
s=6  Grandparents' Childcare and Female Labor Force Participation       (2013)
s=6  With strings attached: Grandparent-provided child care and female  (2016)
```

The dominant outcome in the extended-household literature is **maternal labour supply, not fertility.**
Grandparental childcare is studied because it frees mothers to work; whether it changes births is a
secondary question in that field.

Two consequences. First, `OFF_OUTCOME` will be this chapter's largest single route-out, and it needs to
be a **named cell rather than a residue** — the standing lesson that a wall cut on the wrong axis
leaves what looks like ambiguity and is actually a missing category. Add
`OFF_OUTCOME_LABOUR_SUPPLY` explicitly, cross-referencing C.2.e.

Second, it is a warning about the extended-household arm's apparent strength. Its six identified
anchors exploit pension and retirement-age variation — but that literature's *own* estimand is usually
the mother's employment, with fertility as a secondary outcome when it appears at all. **The
identified-design count from anchor sourcing may overstate how much identified evidence exists on
fertility specifically**, and the full-text screen has to check the estimand, not the design. This is
the standing rule that retrieval and design counts hide which records: cross-tabulate design against
the estimand job before believing either.

## 6. What round 2 should do

1. **Page the Furstenberg and *Leaving Home in Europe* forward tails** (269 + 53 works), the two capped
   seeds on the pre-launch side. Do not page the Reher or filial-responsibility tails.
2. **Do not spend new seeds on the decoy cloud** (§3), but keep it tagged in the pool.
3. **Seed the pre-launch arm harder from channel 5**, not from citations — the network says the
   citation channel will not connect that arm to fertility, so the eight named designs of scope §4 are
   the only route to identified pre-launch evidence.
4. Round 2 is a **prerequisite to the production query**, not an optional extra: with channel 1 dry,
   this frame is the recall denominator.
