# Channel-3 citation snowball — housing costs (C.2.c)

**Run:** 2026-07-31, Shravan (TICK-055). **Rounds 1–3 complete. See §4 — the stop rule itself is
defective, and that is the main methodological result of this run.**
**Artifacts:** `housing-costs-snowball-pool.json` (1,735 records) ·
`housing-costs-tier-b-frame.json` (203 candidates, unscreened)
**Scripts:** `source/build/goldset/c2c/{snowball.sh,twins.sh,snowball_r2.sh,aggregate_rounds.py}`

**Round 1 seeds** — the four `channel2_canon_v5seminal` anchors only: Mulder & Billari 2010,
Dettling & Kearney 2014, Lovenheim & Mumford 2013, Daysal et al. 2021.
**Round 2 seeds** — seven demography-side papers, added because the round-1 seed set was 3
`econ-price` + 1 `macro-comparative` + **zero `demog-tenure`**. They are **citation-discovered in
round 1, not keyword-discovered**: the Tier-B integrity constraint is about keyword bias, and a paper
reached by citation from a canon seed does not reimport it. They sit at hop 2 relative to the original
canon, so round-2 output was checked for drift (§6b).

---

## 1. Seed discipline

Keyword-scouted papers were **deliberately excluded as seeds**, including Li 2024 despite its
admission to the chapter. GACS A3 restricts Tier B to channels 1–3; seeding a snowball off
keyword-found papers would centre the citation neighbourhood on the query's own reach and reimport the
bias Tier B exists to escape. Considered and declined explicitly so the choice is on the record.

Cost, in round 1: the seed set was unbalanced — three `econ-price`, one `macro-comparative` (Mulder &
Billari, in *Housing Studies*), **zero pure `demog-tenure`**, so the demography family was reached only
through Mulder & Billari. **Round 2 closed that gap** with seven citation-discovered demography seeds
(header, §6b).

## 2. Yield

| | |
|---|---|
| Round 1 pool (4 canon seeds + twins) | 693 |
| Round 2 pool (7 demography seeds) | 842 pulled, 675 new |
| Round 3 pool (8 modern-price / space / affordability / long-run seeds) | 580 pulled, 367 new |
| **Merged unique pool** | **1,735** |
| Housing-treatment **and** fertility-outcome core (Tier-B frame) | **203** (106 r1, 63 r2, 34 r3) |
| Normalized-title duplicate groups | 82 |

## 3. The headline number, and the honest reading of it

Of the 106-record housing→fertility core, **19 were already in the 25-record keyword anchor set and 87
were not — 82% snowball-only**, of which **63 are peer-reviewed journal articles**.

**But that 82% is a breadth miss, not a vocabulary-invisibility miss, and the distinction matters.** I
checked directly: the 215 fertility-term-only, 188 housing-term-only, and 129 neither-term records
were scanned for housing→fertility papers hiding from the vocabulary, and there are essentially
**none**. Those buckets are other chapters' literature — the fertility-economics canon (income effects
→ C.1.a, job displacement → C.5.a, financial incentives → C.2.d, Becker's time allocation → Section E)
and the lowest-low-fertility demography canon. So the keyword sweep missed 87 papers **that do carry
both terms in their titles**; it missed them because it ran a handful of query forms and took the top
25 by citation, not because the papers were unreachable.

Two consequences:

- **The production query can in principle reach this literature.** The recall problem for C.2.c is
  *breadth within the housing axis* (`econ-price` vs `demog-tenure` vocabulary), not title-invisible
  papers. That is a much more tractable problem than the one OAS faced.
- **Recall(B) will be a weaker test here than it was on the pilot, and should be reported as such.**
  GACS E3 already warns that Tier B "inherits a residual keyword bias it cannot fully escape." For
  C.2.c the issue is sharper in a different direction: Tier B is genuinely keyword-reachable, so a
  high Recall(B) is close to guaranteed and correspondingly uninformative. **Do not quote a C.2.c
  Recall(B) as evidence the method generalises** without this caveat attached at the point of use.

## 4. Saturation — and a defect in the §7.2 stop rule that this run exposed

The §7.2 stop rule is <1 new relevant paper per 50 records pulled, sustained over **2 consecutive**
rounds.

| Round | Pulled | New unique | New relevant (core) | New core per 50 | vs floor 1.0 | Pulled records already seen |
|---|---|---|---|---|---|---|
| 1 | 693 | 693 | 106 | **7.65** | ABOVE | 0% |
| 2 | 842 | 675 | 63 | **3.74** | ABOVE | 20% |
| 3 | 580 | 367 | 34 | **2.93** | ABOVE | **37%** |

**The decay stalled.** Round 1→2 nearly halved the yield (ratio 0.49); round 2→3 barely moved it
(0.78). On the round-1→2 trend, round 3 should have landed near 1.8; it landed at 2.93.

**The reason is that these are not saturation rounds, and the rule does not notice.** Each round I
added *new seeds chosen to reach an under-covered sub-area* — round 2 the demography family, round 3
the modern price empirics, the space/crowding cell, affordability, and the long-run panel. That is
**coverage expansion**, not exhaustion of a fixed frontier. The yield stays above floor because each
round deliberately opens new territory, so the measured quantity is "is there more literature
reachable from a *broader* seed set," which stays positive as long as the RA can still name an
under-reached area.

**§7.2 is ambiguous between two readings and they terminate very differently:**

- *Same-seed reading* — another hop from a fixed seed set. Under this reading the snowball would have
  stopped at **round 2**, since a second hop from the canon four mostly re-finds round-1 papers.
- *Expanding-seed reading* — new seeds each round. Under this reading the rule **may never terminate**,
  because termination depends on RA judgement about what is under-reached rather than on a threshold.

Neither is stated in §7.2, and the difference is not cosmetic: it decides whether this snowball is
finished. **Recommended rule amendment, for the PI and for every hypothesis, not just C.2.c:**

1. Report **new-core-per-50 and the overlap rate** (share of pulled records already in the pool)
   together. The overlap rate is the mechanical convergence signal that survives seed expansion:
   here it climbs **0% → 20% → 37%**, which is honest evidence of convergence even while the
   yield-per-50 stays high.
2. Require the stop test to be run **same-seed** — a confirming round that adds no new seeds. That is
   the only version of the test that measures exhaustion rather than the RA's imagination.
3. Treat "no under-reached sub-area can be named" as an explicit, recorded stopping condition in its
   own right, since that is what is actually doing the work.

**Current status under each reading:** stopped and saturated (same-seed); not stopped (expanding-seed).
The Tier-B frame is therefore **still not frozen**, and §8 sets out what would earn the freeze.

## 5. Preprint twins degraded the snowball, measurably

The dedup hazard flagged at anchor-sourcing did real damage on this run, not hypothetical damage.

**The Dettling & Kearney *Journal of Public Economics* record carries `cited_by_count = 0`.** All 67 of
its forward citations sit on the NBER working-paper record under a different DOI. A snowball run off
published DOIs alone would have pulled **zero** forward citations from one of the four canon seeds —
silently, with no error. Same pattern for Lovenheim & Mumford (14 citations on the SSRN twin) and
Daysal et al. (4 on the NBER twin).

The run was repaired by pulling forward citations from the twins as well and merging (`twins.sh`);
twins are treated as citation sources, never as separate anchors. **This should be a standing step in
the pipeline, not a C.2.c fix** — every economics hypothesis in this review will hit it, because NBER
and SSRN preprints are where economics citations accumulate.

Within the merged pool the problem recurs at scale: **70 normalized-title duplicate groups spanning
156 records.** The worst is *Partisan Fertility and Presidential Elections*, present **five times**
(AER: Insights, three SSRN records, one OSF preprint); round 2 added another instance in Kulu & Vikat
2007, whose MPIDR working paper (`10.4054/mpidr-wp-2007-014`) and *Demographic Research* article are
both in the frame. **23 of the 169 Tier-B candidates are preprint-only records and 8 carry no DOI at
all.** Normalized-title dedup is mandatory before this frame is frozen, and the **published** version
must be the survivor.

## 6. What round 1 found that changes the chapter

- **`10.1007/s11150-016-9355-8` — "The asymmetric housing wealth effect on childbirth"** (*Review of
  Economics of the Household*). Directly on the tenure-asymmetry that structures the scope doc's
  pooling rule. A priority read.
- **`10.1093/restud/rdad034` — "Monetary Policy and Birth Rates: The Effect of Mortgage Rate
  Pass-Through on Fertility"** (*Review of Economic Studies*). A clean **Wall 1 test**: the
  identifying variation is mortgage rates, i.e. credit terms, so under the 2026-07-31 ruling it routes
  to **C.3.e** despite a housing-market framing. Add to the decoy set.
- **`10.1093/rfs/hhaa073` — "The Babies of Mortgage Market Deregulation"** (*Review of Financial
  Studies*). Same wall, same routing.
- **`10.1016/j.jue.2025.103812` — "Impact of fertility relaxation on the housing market outcomes"**
  (*Journal of Urban Economics*). `REVERSE`; pairs with the Gong & Yao decoy.
- A substantial **Korean-language and Korean-setting cluster**, and Chinese, Italian, Dutch,
  Bulgarian, and Iranian settings. The geographic skew flagged in the scope is real, and the
  non-Anglophone tail is larger than expected — relevant to the ownership-rate moderator, since these
  settings span very different tenure regimes.
- Several **A.23 boundary cases** (boomerang moves, returning to the nest, parental co-residence,
  leaving home) that route out under the ruling but confirm the mediator wall will get heavy traffic.

## 6b. What round 2 changed — and a substantive problem it exposed

The demography seeds worked as intended. The Tier-B frame's venue profile is now genuinely
two-family: *Population Space and Place* (11), *Housing Studies* (8), *Demographic Research* (5),
*Demography* (3), *European Sociological Review* (2), *Population Research and Policy Review* (3)
alongside the economics venues. Round 2 also reached back further in time than round 1 managed —
including a 1975 *American Journal of Sociology* paper on the fertility-inhibiting effect of crowded
apartment living, and a 1995 *Sociological Spectrum* paper on housing tenure and fertility.

**But the round exposed a problem with the chapter's own boundary, and it is not a search problem.**
The `demog-tenure` family largely **does not study prices.** Its centre of gravity is housing *tenure*,
housing *type*, housing *conditions*, and above all **residential mobility** — "fertility intentions
and residential relocations," "residential mobility of couples around family formation,"
"fertility-intention-induced relocation." Under the 2026-07-31 ruling that C.2.c owns **price**
variation, a large share of this family routes **out** of the chapter: to A.23, to
`HOUSING_ONLY_MECHANISM`, or to `REVERSE` — and the relocation papers are `REVERSE` almost by
construction, since they model moving as a *response* to intended fertility.

Two consequences, both for the PI rather than for the search:

1. **C.2.c may end up a predominantly economics chapter**, with the demography literature entering as
   mechanism, context, and identification-threat documentation rather than as pooled evidence. That is
   a defensible outcome of the ruling, not a defect — but it should be a decision made with eyes open,
   because it means the chapter's evidence base is narrower than the topical literature suggests.
2. **The relocation cluster is the anticipatory-sorting threat, documented by the field itself.** These
   papers are direct evidence that households move in anticipation of childbearing, which is threat 1
   in the scope's identification list. They are more valuable to the chapter as a threat model than
   they would be as effect estimates, and §9 should use them that way.

*Drift check (the hop-2 concern):* round-2 additions do drift toward residential mobility and
migration. The drift is real but interpretable — it is the demography family's actual subject matter,
not the snowball wandering off topic — and the routing rules catch it. No seed pruning needed.

## 6c. Round 3 — the most valuable round, and it vindicates two scope calls

Round 3 targeted what rounds 1–2 under-reached, and returned the two clusters the scope doc had
already singled out as decisive.

**The rent stratum now exists.** `10.1016/j.regsciurbeco.2008.08.007` — *"Do higher rents discourage
fertility? Evidence from U.S. cities, 1940–2000"* (*Regional Science and Urban Economics*; SSRN twin
`10.2139/ssrn.1098847`). This is close to the ideal C.2.c study: **rent-identified**, so it isolates
the cost channel with no wealth offset and **no endogenous tenure split required** — the scope's
"highest-quality stratum" — over a **60-year US panel**. It should be a priority read alongside the
wealth-asymmetry paper.

**The historical/FDT cluster now exists, which retrospectively supports the Li 2024 ruling.**
`10.2307/2084364` — *"Housing and the Birth Rate in Sweden"*, **American Sociological Review, 1937**.
Plus the rent panel's 1940 start, `10.2307/2061200` (apartment living and fertility, *Demography*
1978), `10.1080/19485565.1992.9988818` (household crowding and reproductive behaviour), and
`10.1080/19485565.1995.9988902` (multi-family housing and marital fertility, Iran, 1995).

That matters for the period question. The 2026-07-31 ruling admitted Li 2024 as a single exception
while leaving the v5 `phenomena` field at SDT. Round 3 shows Li is **not an isolated case**: there is a
housing-and-fertility literature reaching back to the 1930s. Under the ruling's own terms — "if further
FDT-era evidence accumulates, the field needs a formal update rather than a second case-by-case
exception" — **that threshold is now met, and the `phenomena` field should go to the PI.**

**A seed-rule correction, recorded.** The round-3 script states that Yi & Zhang 2010 (*Economic
Inquiry*, Hong Kong) is keyword-only and not citation-reachable. That was true of the canon-four
neighbourhood but is **false in general**: it surfaced in round 3 via the modern-price seeds. The
comment in `snowball_r3.sh` is wrong on that point and the finding it rested on should not be carried
forward — citation-reachability is a property of the seed set, not of the paper.

The rest of round 3's core is the space/crowding cell (now with genuine historical depth) and further
China-cluster affordability work.

## 7. Anchor count against the CV floor

Pre-snowball: ~20 empirical anchors, below the ≥30 floor. The 63 new peer-reviewed housing→fertility
articles clear it comfortably **once screened** — but they are `candidate_unscreened`, and the count
that matters is post-screen. The floor should be re-checked after the relevance pass, not declared met
now.

## 8. Next steps, in order

1. **Round 3 of the snowball** — saturation is still not reached after round 2 (§4).
2. **Normalized-title dedup** across the pool, published version surviving (§5).
3. **Relevance + estimand screen** on the 106-record Tier-B frame, with a second reader on the
   boundary. The Wall 1 credit cases (§6) are where the screen will be tested.
4. **Re-check the ≥30 empirical-anchor floor** on the screened count, then freeze the gold.
5. Only then: fold-local term mining and cross-validation for the production query.
