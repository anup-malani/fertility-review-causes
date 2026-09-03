# TICK-079: C.2.b Rising Direct Costs of Children
**Status:** open
**Assigned:** Shravan
**Hypothesis:** `child-cost-direct` — HYPOTHESES-v5.md §C.2.b
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/child-cost-direct-*, extraction/child-cost-direct-*, output/chapters/child-cost-direct.md

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
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
