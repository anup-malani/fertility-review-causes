# Channel-3 citation snowball — housing costs (C.2.c)

**Run:** 2026-07-31, Shravan (TICK-055). **Rounds 1–5 complete. STOP TEST CLOSED — two consecutive
below-floor rounds. Caveat on the shape of that result in §4.**
**Artifacts:** `housing-costs-snowball-pool.json` (10,915 records) ·
`housing-costs-tier-b-frame.json` (293 candidates, unscreened)

> ### ⚠ Correction (2026-07-31, after round 4)
> An earlier version of this log reported a Tier-B frame of 545, per-round yields of 7.65 / 3.74 /
> 2.93, and concluded from a "stalled decay" that the §7.2 stop rule is **defective**. **That
> conclusion is retracted; the stall was an artifact of a bug in my own relevance filter.**
>
> The filter matched the bare substrings `hous` and `rent`, so it scored **house**hold, pa**rent**,
> cur**rent**, and diffe**rent** as housing terms — admitting the entire fertility-economics and
> transition-to-parenthood literature as "housing core." **58% of the frame (314 of 545 records) were
> false positives**, and the contamination was worst in exactly the rounds that drove the stall claim
> (round 3: 34 → 15; round 4: 342 → 75).
>
> With word boundaries and a `household` negative lookahead (`relabel_pool.py`, and the fix is now in
> both aggregators), the decay is **clean and geometric** and the rule behaves correctly. Corrected
> figures throughout. What survives of the §7.2 critique, and the sharper lesson that replaces it, are
> in §4.
**Scripts:** `source/build/goldset/c2c/{snowball.sh,twins.sh,snowball_r2.sh,snowball_r3.sh,aggregate_rounds.py}`

**Round 1 seeds** — the four `channel2_canon_v5seminal` anchors only: Mulder & Billari 2010,
Dettling & Kearney 2014, Lovenheim & Mumford 2013, Daysal et al. 2021.
**Round 2 seeds** — seven demography-side papers, added because the round-1 seed set was 3
`econ-price` + 1 `macro-comparative` + **zero `demog-tenure`**. They are **citation-discovered in
round 1, not keyword-discovered**: the Tier-B integrity constraint is about keyword bias, and a paper
reached by citation from a canon seed does not reimport it. They sit at hop 2 relative to the original
canon, so round-2 output was checked for drift (§6b).
**Round 3 seeds** — eight papers targeting what rounds 1–2 under-reached: the modern price empirics
(China, Netherlands, US), the space/crowding cell, affordability, and the long-run panel (§6c).

---

## 1. Seed discipline — stated loosely in round 1, tightened in round 3

**Round 1's rule:** keyword-scouted papers excluded as seeds outright, Li 2024 included, on the
grounds that GACS A3 restricts Tier B to channels 1–3 and seeding off keyword-found papers would
centre the citation neighbourhood on the query's own reach.

**That rule was too crude, and round 3 replaced it.** What must be excluded is a paper reachable
**only** by keyword — seeding off one imports the query's blind spots. A paper that is already
**citation-reachable from the canon** (i.e. appears in the merged pool) carries no such bias, whether
or not a keyword sweep also happened to find it. The operational test is therefore *membership in the
pool*, not *method of first discovery*.

Under the tightened rule **Li 2024 qualifies and was seeded in round 3**, which also serves its
admission to the chapter. The round-1 exclusion was conservative rather than wrong, and cost little:
Li's neighbourhood was reached one round later.

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
| Round 4 pool (mechanical confirming sweep, 181 seeds) | 7,840 pulled, 7,037 new |
| Round 5 pool (second mechanical sweep, 75 seeds) | 3,364 pulled, 2,693 new |
| **Merged unique pool** | **10,915** |
| Housing-treatment **and** fertility-outcome core (Tier-B frame) | **293** (93 r1, 48 r2, 15 r3, 75 r4, 62 r5) |

## 3. The headline number, and the honest reading of it

Of the 93-record round-1 housing→fertility core, **18 were already in the 25-record keyword anchor set
and 75 were not — 81% snowball-only.** *(Corrected from 106/87/82% under the buggy filter; the finding
is unchanged, which is itself reassuring — the false positives were spread across the buckets rather
than concentrated in the snowball-only set.)*

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

## 4. Saturation — stop test CLOSED, with a caveat on its shape

| Round | Seeds | Pulled | New unique | New core | Per 50 | vs floor 1.0 | Overlap |
|---|---|---|---|---|---|---|---|
| 1 | 4 canon + 3 twins | 693 | 693 | 93 | **6.71** | ABOVE | 0% |
| 2 | 7 demography | 842 | 675 | 47 | **2.79** | ABOVE | 20% |
| 3 | 8 modern-price / space / long-run | 580 | 367 | 14 | **1.21** | ABOVE | 37% |
| 4 | **181, mechanical** | 7,840 | 7,037 | 69 | **0.44** | **BELOW** | 10% |
| 5 | **75, mechanical** | 3,364 | 2,693 | 55 | **0.82** | **BELOW** | 20% |

*(Counts final as of the second relevance-filter correction — see §4b. The narrowing removed records
from every round, so both below-floor readings moved further below the floor and the stop test is
if anything more securely met than when it was first declared.)*

**The §7.2 rule is satisfied: two consecutive rounds below the floor of 1.0 new relevant per 50
pulled.** The snowball is declared saturated and the Tier-B frame is eligible to freeze.

### The caveat, stated because the numbers do not read as cleanly as the verdict

**Round 5 came in higher than round 4 (0.82 vs 0.44), and not far below the floor.** The sequence is
a dip and a partial rebound, not a monotone decay. The mechanism is understood: round 4 swept 181
seeds that were mostly already-explored territory, while round 5 swept the 75 members round 4 had just
*discovered* — fresher ground, so a higher hit rate. Each mechanical round seeds from the previous
round's new finds, so the frontier keeps widening a little even as the rule closes. The frame grew
203 → 231 → 278 across these rounds, which is real growth, not noise.

**Read honestly, this is a slowly-converging process that has met a pre-registered threshold, not a
process that has visibly exhausted itself.** Both statements are true and the chapter should not
report only the flattering one.

**Why we stop here anyway.** The floor and the two-consecutive requirement were set in advance. Having
watched the numbers come in, deciding that 0.82 is "too close" and demanding a sixth round would be
post-hoc discretion of exactly the kind pre-registration exists to prevent — and it would be
unfalsifiable, since the rebound mechanism means some further round could always be justified. The
disciplined move is to honour the rule, record the caveat where anyone quoting the saturation claim
will see it, and let the **relevance and estimand screen** — the real quality gate — do the rest of
the work. If a sixth round is ever wanted, it should be triggered by a substantive gap the screen
reveals, not by dissatisfaction with a number.

**One asymmetry to note rather than bury:** round 4's seeds were drawn from the *pre-correction*
frame, so some were relevance-filter false positives (*Transition to Parenthood* and similar). That
does not invalidate the round — extra seeds only widen the frontier and make the yield reading more
generous, and it still came in below floor — but rounds 4 and 5 are not drawn from identical
populations and should not be presented as a clean matched pair.

### What the confirming round settled

**The design worked.** Rounds 1–3 each used seeds *I* picked to reach an under-covered area, which
makes their yield a measure of RA imagination as much as of the literature. Round 4 removed my
judgement from seed selection entirely — membership, not choice — and it is the round that produced
the below-floor reading. The distinction between expanding-seed and same-seed rounds is real and
worth writing into §7.2, and **a mechanical confirming round should be required before any snowball
is declared saturated.** That much of the earlier critique stands.

**But the empirical claim that motivated it does not.** The "stalled decay" that I argued showed the
rule was broken was produced by my own relevance bug (see the correction at the top). On corrected
counts the rule behaves exactly as designed. The retraction is total on that point.

**And my proposed fix was wrong.** I recommended reporting the **overlap rate** as "the convergence
signal that survives seed expansion," on the strength of its climb 0% → 20% → 37%. Round 4 refutes
this directly: overlap **fell back to 10%** under mechanical frontier expansion. Overlap measures how
much a seed set revisits ground the *previous seed sets* covered, so it rises when seeds are chosen
near explored territory and falls when the frontier genuinely widens. It is a diagnostic of seed
placement, not of exhaustion. **Do not adopt that recommendation.**

### The lesson that actually generalises

**A stop rule is only as good as the relevance classifier feeding it, and a broken classifier fails in
the direction that looks like more work rather than less.** The bug inflated new-relevant counts,
which held the yield above the floor and made a converging snowball look non-converging. Nothing in
the pipeline would have caught it: the counts were plausible, monotonically decreasing, and the pool
was growing as expected. It surfaced only because round 4's output was eyeballed against the venue
list and the titles were visibly wrong — *Transition to Parenthood*, *Female reproductive ageing*,
*Household bargaining over fertility*.

Concretely, for every hypothesis: **before trusting any saturation number, print a random sample of
the records the relevance filter admitted and read them.** A substring filter over titles is doing
classification work and deserves the scrutiny a classifier gets, not the trust a regex gets. Recommend
adding this as a required check in §7.2 alongside the mechanical confirming round.

## 4b. Second relevance-filter correction, and dedup

**The filter was wrong a second time, found the same way.** After fixing the `hous`/`rent` substring
bug, `\bresiden` was still matching **medical residents** — *"Fertility Knowledge in Obstetrics and
Gynecology Residents"*, *"a didactic intervention among resident physicians"* — and *"residents of X"*
meaning inhabitants. Narrowed to `residential|residence`; **15 further false positives removed**
(frame 293 → 278). Both below-floor readings moved *further* below the floor, so the stop test is more
securely met than when declared, not less.

This is the second time the sample-read caught a classifier error that the counts alone did not. It is
the strongest argument for making that read a required step (§4).

**Normalized-title dedup** (`dedup_frame.py`): frame **278 → 264**, 12 exact-title groups collapsed.
Survivor rule is published article > working paper/preprint > report, then a publisher DOI over an
SSRN/NBER/OSF one, then citation count. Recovered the expected twins — Daysal et al. absorbed three
preprint records, Dettling & Kearney its NBER twin, the *ReStud* mortgage paper its FEDS working paper.

**Near-duplicates are flagged, not merged** (`housing-costs-dedup-review.json`). Two groups share a
55-character prefix: Lovenheim & Mumford's REStat article and its SSRN version, which *is* one paper
(subtitle differs: "…Housing Market" vs "…Housing Market Boom and Bust"); and two genuinely distinct
residential-greenness papers from 2014 and 2021. Auto-merging on prefix would have been right once and
wrong once, which is why it is a review queue rather than a rule.

**43 survivors remain preprint-only or DOI-less** — real grey literature with no published version
found, not dedup failures. They stay in the frame and carry the flag.

## 4c. The filter was wrong three times — and the real error is structural

| Fix | What it was matching | Removed | Frame |
|---|---|---|---|
| 1 | `hous`→**hous**ehold; `rent`→pa**rent**, cur**rent**, diffe**rent** | 314 | 545 → 231 |
| 2 | `residen`→medical **residents**, "**residents** of X" | 15 | 293 → 278 |
| 3 | `hous`→**hous**ework, Hou**ston**; `propert`→psychometric **properties**; `home`→**home**land | 22 | 278 → 256 |

**All three were found by reading a random sample. None was found by the counts**, which stayed
plausible and monotone throughout. Excluded look-alikes now: household, housework, housewife,
housekeeping, Houston, homeland, homework, psychometric properties, medical residents.

**The structural error, which is more useful than any of the three fixes.** GACS Phase D specifies a
*semantic* screen — D1 deterministic ranking, then Haiku for recall, then Sonnet for precision. A
title regex is a **D1-class instrument**: a cheap ranking aid. I used its output as the **definition of
the Tier-B frame**, which is a D2-class job. Every bug above is a symptom of that one substitution.
The lesson is not "write better regexes"; it is that **relevance for a gold set must be decided
semantically, and a substring filter can only ever pre-sort the queue for that decision.**

Two consequences worth carrying to other hypotheses:

1. **Where the polysemy sits determines how much this bites.** C.2.c's cause axis is unusually bad —
   *housing* collides with household, housework and animal housing; *fertility* collides with soil and
   livestock fertility. A hypothesis whose vocabulary is more distinctive will suffer less, but the
   structural point holds regardless.
2. **The direction of the failure matters.** These bugs inflated the relevant count, which held the
   saturation yield above the floor and made a converging snowball look non-converging — the false
   conclusion in §4 that the stop rule was defective. **A relevance filter that over-admits does not
   look like an error; it looks like more work to do.**

*Effect on the stop test: none adverse.* Each correction pushed the below-floor rounds further below
floor (round 4: 0.48 → 0.44 → **0.36**). The test is more securely met at each correction, not less.

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
*(Update, after the gate: this paper did not reach the empirical core — the screen routed it
`AGGREGATE_UNSPLIT`, because its subject is Sweden's public-housing programme rather than a price. It
stays in Tier B and is worth reading at full text, but the framing here oversold it. See the
gold-freeze proposal §4.)*
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

1. ~~Decide the stop~~ — **done. Stop test closed at round 5** (§4), two consecutive below-floor
   rounds, with the shape caveat recorded there.
2. **Normalized-title dedup** across the pool, published version surviving (§5).
3. **Relevance + estimand screen** on the 106-record Tier-B frame, with a second reader on the
   boundary. The Wall 1 credit cases (§6) are where the screen will be tested.
4. **Re-check the ≥30 empirical-anchor floor** on the screened count, then freeze the gold.
5. Only then: fold-local term mining and cross-validation for the production query.
