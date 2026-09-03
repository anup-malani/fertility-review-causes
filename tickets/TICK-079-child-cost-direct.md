# TICK-079: C.2.b Rising Direct Costs of Children
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `child-cost-direct` — HYPOTHESES-v5.md §C.2.b
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/child-cost-direct-*, extraction/child-cost-direct-*, output/chapters/child-cost-direct.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/child-cost-direct.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

Smallest remaining frame on `source/build/goldset/304_candidate_frame_probe.py`, log at
`literature/search-logs/candidate-frame-probe-2026-09-03.md`: **587 records** in the deduplicated
union frame on three vocabularies, against 675 for A.6, 714 for C.2.f, 726 for A.3 and 762 for
C.3.d. Everything else is out on the union-is-a-superset rule — a narrow count already above 675
cannot produce a smaller union — so only six of 37 candidates needed widening at all.

**C.2.b had never been measured before 2026-09-03.** The probe's candidate list covered 24 of the
38 unstarted registry entries while its generated table said "every unstarted candidate"; fifteen
live entries, C.2.b among them, were absent from `NARROW` entirely. Every count the probe produced
was correct and the denominator was wrong, which no re-run of the same script could have found.
`check_coverage()` now parses HYPOTHESES-v5.md and crashes on an entry that is neither STARTED, nor
EXCLUDED with a stated reason, nor a candidate. Recorded as `candidate-list-is-itself-a-filter`.

**587 against A.6's 675 is inside vocabulary noise, so size did not decide this on its own.** The
tiebreak is inherited boundary debt. C.2.b's one flagged neighbour, D.2.d, is a drafted chapter, so
that wall cuts against something finished. A.6 is by construction the residual left after A.2, A.4
and A.5 — all three unstarted — and its stigma-specific axis returns **12** records, so its frame is
almost entirely the loose "stigma OR taboo" vocabulary and the wall it most needs is against three
literatures nobody has scoped.

**The homonym is already measured, not assumed.** "cost of children" returns 740 records
unrestricted and 206 of those intersect the paediatric cost-of-illness vocabulary — the phrase is
genuinely shared. Inside the fertility-restricted frame the illness residue is **10**. The outcome
axis separates the two literatures by itself, as it did for C.6.a's happiness literature. Boundary
probes against the neighbouring cost chapters are also small: C.2.a childcare **28**, C.2.c housing
**11**. The scoping problems below are therefore definitional, not retrieval problems.

## Open rulings to freeze at stage 2

1. **The estimand is a price faced, not an expenditure observed.** Spending per child is jointly
   determined with fertility: a household with one child spends more on that child *because* it has
   one. The raw expenditure–fertility correlation carries that reverse channel at full strength, and
   it is the dominant reading of the descriptive series — USDA/Lino-style cost-of-a-child figures are
   computed *from* observed household budgets conditional on family size, so regressing fertility on
   them recovers the accounting identity rather than a price effect. Freeze before any query that the
   admissible exposure is variation in the **price** of child-specific goods, and that observed
   expenditure levels route out. Nearest precedents: `exposure-estimand-distance-domain` (A.24) and
   `read-the-mechanism-not-the-instrument-name` (C.3.e).
2. **C.2.b vs C.3.d, which the registry itself flags** ("separating direct cost from
   quality-investment cost is an identification challenge"). Under the what-varies rule frozen by
   C.2.c on 2026-07-31: **C.2.b owns variation in the price of child-specific goods; C.3.d owns
   variation in the chosen quality or investment level per child.** A household choosing to spend
   more per child is C.3.d's variation; an exogenous move in the price of a required input is
   C.2.b's. C.3.d is **unstarted**, so this wall is cut against an empty neighbour and the ruling
   must be written in a form C.3.d can inherit rather than re-litigate.
3. **The cost bundle splits at least four ways and three of the four are other chapters.** Childcare
   price is C.2.a (unstarted), housing is C.2.c (written, and its sign is tenure-conditional), the
   mother's time is C.2.e (unstarted), and the norm defining what a proper child requires is D.2.d
   (drafted). Freeze whether C.2.b is (a) the residual after those four — schooling fees, health,
   child-specific consumption, enrichment — or (b) the total direct cost with the neighbours as named
   components. Same shape as B.6's two-way bundle split; decide it at stage 2, not at synthesis.
4. **Two phenomena, and the FDT arm collides with a written chapter.** v5 registers FDT **and** SDT.
   The FDT version of rising direct costs is Caldwell's schooling-cost argument, which is C.3.b's
   variation (child labor restrictions and compulsory schooling — Alexandra's chapter, already
   written). Decide whether the FDT arm is in scope, or whether C.2.b runs SDT-only with the
   cost-of-schooling channel routed to C.3.b. `identified-evidence-in-the-unnamed-arm` says count
   identified designs per arm before scoping one out.
5. **Name the demsig route before searching, per `three-demsig-routes-before-not-assessed`.** C.2.b
   plausibly has a real exposure series — USDA *Expenditures on Children by Families* is annual for
   the US, and CPI components cover child-specific goods — so slope sufficiency is computable the way
   C.6.a's sign test was, without a decomposition denominator. **Pre-register the sign before the
   search:** the hypothesis requires the *real* price of children to have risen across the SDT
   window. If it has not, the SDT cell is settled by the sign and the elasticity estimates are
   irrelevant to it. Build the series, deposit it in `data/raw/` beside `wdi-age-structure/`, and
   note that a nominal series rising is not the claim.
6. **The equivalence-scale sub-literature is a measurement literature, not an effect literature.**
   92 records ask what a child costs, not whether cost changes fertility. Decide whether it enters as
   exposure measurement — a source for the price series under ruling 5 — or is screened out. Do not
   let it inflate the primary cell.

## Assets in hand before the cold start

- **Free seeds.** Port `305_c6a_free_seeds.py`: C.2.c, D.2.d, C.3.b, C.3.e and C.3.c all plausibly
  routed cost-of-children records into their own screen files before this chapter existed. It is
  `snowball-pools-omit-their-own-seeds` in reverse and costs nothing.
- **Resolver.** Port from `307_c6a_cold_start_anchors.py`, the only copy carrying all four TICK-074
  fixes plus the three defects found on C.6.a's *Birth and Fortune* anchor. Do not port from `275_`.
- **Script numbering.** Max across **every branch on origin** is 316, so C.2.b starts at **317**
  (`script-number-collision`: start above every branch, not above main).

## Log

### 2026-09-03 — opened, claimed, and scope drafted with three rulings resolved

- Selected by `304_candidate_frame_probe.py` after the coverage defect was fixed. Union frames on
  three vocabularies: **C.2.b 587**, A.6 675, C.2.f 714, A.3 726, C.3.d 762, C.3.f 1101, C.3.a 1804,
  A.19 2778, C.1.a 6164. Only six of 37 candidates needed widening: a union frame is a superset of
  every axis inside it, so a narrow count already above the incumbent's 675 is out with no further
  queries.
- Scope at `literature/search-logs/child-cost-direct-search-scope.md`. Nine walls, ten estimand
  cells, seven required tags, the pooling rule and the demsig route all frozen before any query.
- **Ruling 1 (the load-bearing one): the estimand is a price faced, not an expenditure observed.**
  Spending per child is quantity-chosen times price-faced, and fertility and quantity-per-child are
  chosen together, so the expenditure–fertility correlation is negative under any quantity-quality
  model with no price change anywhere. The canonical series are outputs of that identity — USDA/Lino
  is computed from CEX budgets *conditional on family size and income*. Admissibility is therefore
  defined on the variation, not the vocabulary, and `EXPENDITURE_ASSOCIATION` exists to quarantine
  the identity. Third instance of the shape behind `exposure-estimand-distance-domain` (A.24),
  `read-the-mechanism-not-the-instrument-name` (C.3.e) and `exposure-outcome-same-sequence` (A.23).
- **Ruling 2 (the bundle): C.2.b is the residual, not the total.** Childcare is C.2.a's, housing
  C.2.c's, the mother's time C.2.e's, the norm D.2.d's, the chosen investment level C.3.d's, and the
  net-of-transfer price C.2.d's. What remains is the out-of-pocket price of child-specific goods and
  services. The total reading is rejected because it would make this chapter's estimate a function of
  five unfinished chapters. Raised as PI Call 1, because C.2.f and C.3.f have the same shape.
- **Ruling 3 (the FDT arm): in scope, restricted to the out-of-pocket half of Caldwell.** Fees here;
  compulsion and forgone child labour to C.3.b, a written chapter. Inseparable cases go to
  `MIXED_PRICE_VALUE`, jointly claimed and unallocated, on C.2.c's `MIXED_PRICE_CREDIT` precedent.
  Not dropped, because `identified-evidence-in-the-unnamed-arm` says count identified designs per arm
  first — and the fee-abolition designs are likely the best-identified variation this chapter sees.
- **Registered before searching: the hypothesis is about a rise and the clean variation is mostly a
  fall.** Fee abolition, free primary education, subsidised uniforms and meals, child health-insurance
  expansion all *lower* the price. `exposure_direction` is a required tag, effects stratify on it
  before the ≥3 poolability test, and the symmetry assumption is PI Call 3.
- **The demsig route is named: slope sufficiency, with the index specified before it is computed** —
  components, deflator, two weighting variants, and three arms (with education, without, education
  alone), because a "price of children" index can be made to rise or fall by choosing components
  after seeing the answer. Carries C.6.a's two guards: a sign condition on any R²
  (`r2-criterion-is-sign-blind`) and a split window as well as endpoints
  (`endpoint-test-nets-a-hump-to-nothing`).
- **Wall 9 is a measured non-threat.** "cost of children" returns 740 records unrestricted and 206 of
  those intersect the paediatric cost-of-illness vocabulary, but only **10** survive inside the
  fertility-restricted frame. The outcome axis separates the literatures on its own and no screen rule
  is spent on it. Neighbour probes are also small: C.2.a 28, C.2.c 11.
- Open for Anup: **PI Call 1** (residual vs total, and it generalises), **PI Call 2** (Caldwell 1976
  is now the seminal citation of four chapters), **PI Call 3** (what to do when the identified
  evidence runs in the opposite direction to the registered claim).


### 2026-09-03 — free seeds (317), and the pre-registered sign test (318)

**Free seeds: 130 records at zero retrieval cost.** Script 317, ported from C.6.a's 305. Scanned
1,136 branch:file pairs (88 unique blobs) across every branch on origin. Dropped 2 as paediatric
cost-of-illness and 5 as peer-review apparatus — three of those five were "Review for", "Decision
letter for" and "Author response for" the *same* paper (`shadow-record-gate`, named qualifiers only).

Two amendments to the scope followed, both recorded in §16:

- **Wall 4 is a vocabulary problem, not only a routing one.** 17 of 130 kept records are C.2.e's
  time-cost / child-penalty literature — 11 of the 33 that `cost of children` returns, and **5 of the
  6** that `cost of childbearing` returns. The hypothesis's own name is the neighbour's name. §8 had
  scored only the cost-of-illness homonym, which turned out to be the harmless one: 2 records against
  17. The exposure axis in script 320 separates them; the screen will not.
- **The fee-abolition vein may identify the wrong estimand.** §7 row 1 called it the largest expected
  source of identified variation and the volume agrees (24 records). But of the 8 carrying a
  fertility outcome, **6 name women's or girls' schooling in the title** — a maternal-education
  channel, which *lowers* fertility, where the mechanism says a price cut should *raise* it. A
  required `channel` tag now gates `SCHOOL_COST_FERTILITY`. Title-level signal only
  (`design-is-not-a-property-of-the-title`); every one is re-read at full text.

**The sign test (script 318) passes on the whole window and the timing runs the other way.**

The whole-window test is nearly uninformative: every arm containing education rises hard in real
terms (education alone +205%, with-education +79% to +132%), and the arm **without** education
**falls** on equal weights (−17%). The composite rises only because of education — the component
ruling 2 puts most in doubt, since college tuition is largely chosen quality (C.3.d) and the BLS K-12
index prices *private* schooling, not the price most US parents face.

Decade by decade, against the share of TFR movement:

| decade | share of all movement | real child price | verdict |
|---|---|---|---|
| 1970–1980 | **46%** | **−13.3%** | **inconsistent** |
| 1980–1990 | 17% | +21.3% (TFR *rose*) | **inconsistent** |
| the other four | 37% | rising | consistent |

**63% of the total decade-to-decade movement in US fertility since 1967 runs against the mechanism.**
The real price of children fell through the decade in which fertility fell fastest, and rose through
the decade in which it recovered.

**A defect caught in our own diagnostic.** The first version of the decade table read only the price
direction and scored the 1980s as *supporting* the hypothesis when price and fertility rose together
— `r2-criterion-is-sign-blind` reproduced in the instrument built to avoid it. The verdict column now
compares both directions.

**Three data deviations from §5, reported and not absorbed:** no education price series before 1967
and no tuition before 1977-12, so the 1965–67 gap is a data absence and not a null; BLS publishes no
long children's apparel series, so all-apparel is substituted and labelled; day care is excluded as
C.2.a's but fetched and reported so the exclusion can be priced. BLS was reached through DBnomics —
`download.bls.gov` returns 403 from Akamai bot defence, and the unregistered BLS API v1 silently
ignores `startyear`/`endyear` and returns only the most recent three years.

**Status: this is co-movement in one country, not identification.** It bounds what the mechanism
could be doing and it is the SDT slope-sufficiency input; it does not settle the cell on its own the
way C.6.a's did. Next: cold-start anchors (319), then the per-arm production query (320).

### 2026-09-03 — anchors (319) and the production query set (320)

**Anchors: 32/32, zero ghost citations.** Controls 18/18, hand 14/14. Script 319 is a direct port of
C.6.a's 307 — the only copy carrying all four TICK-074 fixes plus the three defects C.6.a found on
*Birth and Fortune*. The 18 controls are titles and ids taken **programmatically** from script 317's
harvest, so a failure on one would localise to the resolver before anything was read.

Two inherited fixes earned their keep at once. Espenshade 1984 is indexed as the bare *INVESTING IN
CHILDREN* at Jaccard 0.375 and resolves only through the stem rung and the 3-token head floor; Hotz's
handbook chapter is indexed as *Chapter 7 The economics of fertility...* and resolves only through the
allowlisted structural prefix.

**New resolver defect, reported to TICK-074 as defect 9.** OpenAlex stores some titles with HTML
markup — this chapter's control is `<i>'Two children to make ends meet'</i>: ...` — and stripping
non-alphanumerics turned `<i>` into the token `i` at both ends. Measured cost on that record is small
(Jaccard 0.933 rather than 1.0, verdict unchanged), but it breaks contiguous stem containment
outright, which is the path short titles depend on. Present in every copy of the resolver.

**Twin splitting is heavy: 5 of 32 anchors carry 8 twins.** Doepke's AER 2019 holds 288 citations
against 94 across three earlier twins; Osili 383 against 108; and Hotz's 1993 twin holds *more*
citations than the 1997 chapter, 255 to 234. Both ids kept for every pair.

**Production query: seven arms, union primary recall 13/14 (93%) at a deduplicated frame of 963.**

| arm | frame | recall | |
|---|---|---|---|
| `direct-cost` | 326 | 8/9 | |
| `school-fee` | 269 | 4/6 | the policy-evaluation vocabulary; §7's second channel |
| `anticipated-cost` | 186 | 1/1 | |
| `measurement` | 136 | 2/6 | |
| `health-price` | 21 | 0/1 | **uncalibrated — no valid anchor exists** |
| `boundary-timecost` | 57 | 1/1 | the §16.1 separation arm |
| `boundary-qq` | 683 | 1/2 | calibrated, **not screened** |

- **The health-price arm has no valid anchor.** Currie and Gruber's outcome is infant mortality and
  birth weight, not fertility (`anchor-on-the-estimand-not-the-famous-design`). Its first base,
  `"Medicaid" OR "health insurance"`, cost **2,865 records for zero anchors**. Rebuilt narrow at 21
  and kept in the union anyway, because §7 row 3 registers the variation and an arm that does not
  exist would turn a vocabulary gap into a finding of no evidence.
- **Seven anchors do not measure fertility** — three in primary arms, four in `measurement`, where an
  expenditure outcome is what makes a record measurement rather than effect. Flagged, not deleted, so
  the unreachable table separates *arm not screened* and *outcome is not fertility* from the single
  real vocabulary miss. Counting all 17 unreachable anchors against the query would blame it for the
  anchor list's errors.
- **`boundary-qq` is calibrated but not screened.** §16.1's separation requirement is specific to Wall
  4, whose vocabulary is this chapter's own name; quantity-quality vocabulary shares nothing with
  "cost of children", so 683 records is too dear for a wall that does not leak.

**BLOCKED: the query log files are not on disk.** The final re-run hit OpenAlex's daily budget
mid-calibration (`dailyRemainingUsd` 0.0004, `retryAfter` ~6.5h, resets midnight UTC). The numbers
above are from the last complete run and the calibrated script is committed; **re-run
`320_c2b_production_query.py` after the reset to emit the artefacts** before building the screen
universe.

**New gate in 320, and the reason.** The inherited per-arm `continue` on error is unsound: a refused
arm reports recall 0 and frame 0, and the union is then built from an empty hit set. The
rate-limited run wrote a log in which five already-verified anchors — including both Chicoine
free-primary-education papers — appeared as `VOCABULARY MISS`. The console said "query refused (NOT
an empty literature)"; the file said nothing of the kind, and the file is what survives. 320 now
collects every refusal and exits without writing anything.

Next: re-run 320 after the budget reset, then the screen universe (321).

### 2026-09-03 — screen stage: blocked on the OpenAlex budget, everything else built

**Blocked.** OpenAlex's daily budget for this client is spent — `dailyRemainingUsd` 0, resets
**2026-09-04T00:00:00Z**. The universe cannot be pulled until then.

**A correction I got wrong first.** The keyed path reported `dailyRemainingUsd` 0.0004 while keyless
requests still succeeded, which read as "the `api_key` is the metered path and the keyless polite
pool is free". It is not — 89 keyless requests later the keyless path also reported 0. Same wallet.
What keyless *does* have is an additional limit the keyed path lacks: **queries with more than 5
boolean operators are throttled to 1 request per second per client**. Both failures are worded
`Rate limit exceeded`, so the message body has to be read to tell an exhausted budget (retry
tomorrow) from a throttle (retry in a second). Re-running 320 to test the fallback is what consumed
the remaining allowance. Recorded as `openalex-two-limits-one-error`.

**Built and committed, so the run at reset is a single pass:**

- **`source/lib/openalex.py`** — shared client: pool fallback, boolean-throttle pacing,
  refusal-vs-zero, and a **cache written per measurement**. At roughly 100 requests a day, an
  interrupted run that keeps nothing wastes the whole allowance and two stages cannot run on the same
  day. It exists as a library because that machinery was about to sit in two scripts and `main`
  already carries twelve divergent copies of the anchor resolver.
- **321, the screen-universe builder** — does four things a plain pull does not: counts per arm
  **before** deduplication, so a redundant arm reads as redundant and not as empty; **injects** the 32
  anchors and 130 free seeds and reports how many were already present, which is a recall check on
  the query set; **withholds** the gold flags into a separate file so the screen can measure its own
  sensitivity; and reconstructs abstracts, flagging records that have none as a separate screening
  problem rather than an ordinary row. It refuses to write a partial universe if any arm fails to
  page.
- **The screen rubric, frozen before any record is read** —
  `literature/search-logs/child-cost-direct-screen-rubric.md`. One admissibility question (a price
  faced, not an expenditure observed), the routing order, 13 cells, 8 required tags, the §16.2
  `channel` gate on school-fee records, and the Wall 4 test for telling money spent on a child from
  earnings a parent forgoes.

**Order at reset: run 320 first** (it emits the query artefacts 321 reads), **then 321.** 320's
calibration is ~104 requests and may not fit alongside 321 in one day's budget; the cache makes any
repeat free.

### 2026-09-03 — universe built (1061) and the depth probe screened (150)

**Unblocked by a new API key.** 320 ran clean — 144 requests, zero refusals — and reproduced the
earlier calibration exactly: **union primary recall 13/14 (93%), deduplicated frame 963**.

A correction on the earlier diagnosis: the keyed path read `dailyRemainingUsd` 0.0004 while keyless
requests still worked, which I read as "the key is metered and the polite pool is free". It is the
same wallet — 89 keyless requests later, keyless read 0 too. What keyless *does* have is an extra
limit the keyed path lacks: >5 boolean operators are throttled to 1 request/second. Both are worded
`Rate limit exceeded`. Recorded as `openalex-two-limits-one-error`.

**Universe: 1061 records.** Every arm pulled exactly its declared frame. Two defects in 321 found by
reading its own first output:

- 114 of the 130 free seeds carry a DOI and no OpenAlex id and were being dropped as "DOI-only" —
  the exact failure injection exists to prevent. Matching on a normalised DOI moves it from 2
  present / 14 injected to **31 present / 82 injected / 17 unmatchable**. The first number is the
  interesting one: the query found only **31 of 113** matchable seeds on its own.
- "anchors 16 present / 16 injected" mixed theory and boundary anchors into what is meant to be a
  recall check. Split out: **gold found by the query itself 16/23**.

**266 of 1061 (25%) carry no abstract** and are flagged as a distinct screening problem.

**Depth probe: 5 evenly spaced strata × 30, screened blind.** Per-stratum primary counts head to
tail: **[1, 1, 0, 0, 2]**.

| | s1 | s2 | s3 | s4 | s5 | all |
|---|---|---|---|---|---|---|
| primary | 1 | 1 | 0 | 0 | **2** | **4** |
| context | 10 | 8 | 5 | 8 | 3 | 34 |
| boundary | 4 | 1 | 1 | 5 | 3 | 14 |
| routed / excluded / insufficient | 15 | 20 | 24 | 17 | 22 | 98 |

**The curve is flat, and that is the operational result.** A.18 ran 53% / 9.1% / 3.3% / 0.7%, where
truncating cost almost nothing. Here the tail carries more than the head and the cleanest primary
record in the probe sits in the **last** stratum, so **this screen cannot be truncated** — a
citation-ordered partial pass would have missed both the kibbutz privatisation and the Ghana
scholarship RCT.

Prevalence **4/150 = 2.7%** (Wilson 95% CI 1.0–6.7%) → **11–71 primary records** in the universe,
point estimate 28. Screen sensitivity **8/8 = 100%** on the gold the probe touched; the other 15 gold
are reported UNSCREENED and counted neither way.

**Two cell counts that bear on the scope.** `TIMECOST_BOUNDARY` is **12** against the primary cell's
**4** — §16.1 confirmed quantitatively, C.2.e's literature is three times C.2.b's inside this
universe and arrives in this chapter's own vocabulary. And `COST_SERIES_MEASUREMENT` is the largest
non-excluded cell at **20**: the frame is dominated by work measuring what a child costs rather than
estimating what that cost does to fertility, which is §2's identity appearing as a population
statistic.

**The four primary records:** the Israeli kibbutz privatisation of child costs (exogenous
cross-kibbutz variation, lifetime fertility −0.59); a randomised secondary-school scholarship in
Ghana with 12 years of follow-up; Uganda free primary education; and college tuition and fees against
fertility in Taiwan. Two of the four carry the §16.2 channel risk and go to full text before any is
routed.

Next: screen the remaining 911 records (the flat curve says all of them), then full-text retrieval on
the primary cell.
