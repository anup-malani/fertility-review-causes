# Channel-3 citation snowball — housing costs (C.2.c)

**Run:** 2026-07-31, Shravan (TICK-055), round 1 of ≥2
**Artifacts:** `housing-costs-snowball-pool.json` (693 records) ·
`housing-costs-tier-b-frame.json` (106 candidates, unscreened)
**Seeds:** the four `channel2_canon_v5seminal` anchors only — Mulder & Billari 2010,
Dettling & Kearney 2014, Lovenheim & Mumford 2013, Daysal et al. 2021.

---

## 1. Why only four seeds

Keyword-scouted papers were **deliberately excluded as seeds**, including Li 2024 despite its
admission to the chapter. GACS A3 restricts Tier B to channels 1–3; seeding a snowball off
keyword-found papers would centre the citation neighbourhood on the query's own reach and reimport the
bias Tier B exists to escape. Considered and declined explicitly so the choice is on the record.

Cost: the seed set is unbalanced — three `econ-price`, one `macro-comparative` (Mulder & Billari, in
*Housing Studies*), **zero pure `demog-tenure`**. The demography family is reached only through Mulder
& Billari. Round 2 should add channel-2 canon seeds on that side.

## 2. Yield

| | |
|---|---|
| Backward references (≤1 hop, all four seeds) | 187 unique |
| Forward citations (≤1 hop, seeds + twins) | 551 |
| Found by both channels | 15 |
| Found by ≥2 seeds | 93 |
| **Total unique pool** | **693** |
| Housing-treatment **and** fertility-outcome core | 106 |
| Records with no DOI | 40 (2 in the Tier-B frame) |

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

## 4. Saturation: NOT reached — round 2 is required

The §7.2 stop rule is <1 new relevant paper per 50 records pulled, sustained over 2 consecutive
rounds. Round 1 pulled 693 records and returned 87 new relevant ones — **≈6.3 per 50, roughly six
times the floor.** The snowball is nowhere near exhausted and **must not be stopped here.** Round 2:
add `demog-tenure` canon seeds (§1), re-run backward and forward, and re-measure the marginal yield.

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

Within the pool the problem recurs: 46 normalized-title duplicate groups spanning 105 records. The
worst is *Partisan Fertility and Presidential Elections*, present **five times** (AER: Insights, three
SSRN records, one OSF preprint). 21 of the 106 Tier-B candidates are preprint-only records.
Normalized-title dedup is mandatory before this frame is frozen, and the **published** version must be
the survivor.

## 6. What the round found that changes the chapter

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

## 7. Anchor count against the CV floor

Pre-snowball: ~20 empirical anchors, below the ≥30 floor. The 63 new peer-reviewed housing→fertility
articles clear it comfortably **once screened** — but they are `candidate_unscreened`, and the count
that matters is post-screen. The floor should be re-checked after the relevance pass, not declared met
now.

## 8. Next steps, in order

1. **Round 2 of the snowball** — saturation is not reached (§4). Add `demog-tenure` canon seeds.
2. **Normalized-title dedup** across the pool, published version surviving (§5).
3. **Relevance + estimand screen** on the 106-record Tier-B frame, with a second reader on the
   boundary. The Wall 1 credit cases (§6) are where the screen will be tested.
4. **Re-check the ≥30 empirical-anchor floor** on the screened count, then freeze the gold.
5. Only then: fold-local term mining and cross-validation for the production query.
