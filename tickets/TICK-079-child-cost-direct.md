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
