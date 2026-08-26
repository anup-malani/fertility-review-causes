# A4 Tier A / Tier B citation frame — student-debt-household-formation (C.3.g)

**Tier A: 21 seeding anchors** — 5 direct-arm (the registered estimand), 10 chain-arm (link 1), 6 mechanism, review, exposure-series, routing-decoy or negative-control.

**Tier B: 2,071 records** — one hop from those anchors, backward and forward, deduplicated on OpenAlex id. 327 (16%) are reached by more than one seed; 1,426 (69%) carry an abstract; 637 (31%) depend on a decoy, review, exposure-series or negative-control seed alone and can be dropped from any recall computation via `seed_ids`.

Every fraction below is computed AFTER retrieval. None was applied as a filter — pruning the forward pull by topic vocabulary would shrink Tier B by distance from the production query and make Recall(B) circular.

## Measurement 1 — is the P2 policy-variation cell really empty?

`200_` measured it empty THROUGH THE QUERY. A query can only report the absence of what its own vocabulary reaches, so the same question is asked here through the citation channel, which is orthogonal to it by construction. The POLICY vocabulary used is deliberately generous — an over-broad list makes the empty-cell finding harder to sustain, which is the direction an honest test errs in.

**Tier-B records carrying DEBT and POLICY and FERTILITY: 1.**  **Of those, naming an identification strategy: 1.**

Listed by title rather than counted, because each one is a candidate the query could not have found and has to be read:

| Cites | Year | Title | Identified |
|---|---|---|---|
| 1 | 2022 | Experimental Evidence on Consumption, Saving, and Family Formation Responses to Student  | yes |

**These are candidates, not findings.** A record carrying all three vocabularies may still be a passing mention, a review, or an LMIC school-fee study (Wall 7). The screen decides. What matters for the scope is whether the list is empty, and it is not — so the empty-cell claim is now a claim about what SURVIVES screening, not about what exists, and the scope must be restated in those terms.

## Measurement 2 — is the arm routing visible at title and abstract?

The scope asserts that C.3.g's arm split is 'largely visible' where A.17's was not, because the outcome word distinguishes the arms. A record carrying exactly ONE of the three outcome vocabularies is routable at screen; one carrying two or three is not.

| Outcome axes carried | All Tier B | Within the production frame |
|---|---|---|
| 0 | 1,618 (78%) | 0 (0%) |
| 1 | 358 (17%) | 30 (77%) |
| 2 | 85 (4%) | 6 (15%) |
| 3 | 10 (0%) | 3 (8%) |

**Within the frame the screen will actually see, 77% of records carry exactly one outcome axis and are routable; 23% carry two or three and must be routed at full text.**

## Measurement 3 — the attainment confound, sized

The scope declared attainment-conditioning unenforceable at title/abstract on the strength of 8 records at query level, and routed it to full-text extraction and a risk-of-bias domain. Across Tier B, 132 records (6.4%) name attainment-conditioning language; within the production frame, 11 of 39 (28.2%).

## Measurement 4 — Recall(A): would the frame reach its own anchors?

| Frame | Reaches, all 21 anchors | Reaches, 15 empirical |
|---|---|---|
| Production: DEBT and (FERT or UNION or HOUSE) | 13/21 | 13/15 |
| Narrower: DEBT and FERT only | 5/21 | 5/15 |

**8 empirical anchors are reachable only through the chain arm's outcome vocabulary** — a fertility-only frame loses them, and with them the chapter's identified evidence:

- *Debt, Cohabitation, and Marriage in Young Adulthood* (P3_MARRIAGE)
- *Student loans or marriage? A look at the highly educated* (P3_MARRIAGE)
- *Student Loans and Homeownership* (P4_HOUSING)
- *On the Effect of Student Loans on Access to Homeownership* (P4_HOUSING)
- *Into the Red and Back to the Nest? Student Debt, College Completion, and Retur* (P4_HOUSING)
- *A Day Late and a Dollar Short: Liquidity and Household Formation among Student* (P4_HOUSING)
- *Does Student Loan Debt Structure Young People's Housing Tenure? Evidence from * (P4_HOUSING)
- *Student Loan Debt, Educational Attainment, and Tenure Choice* (P4_HOUSING)

Tier B under the production frame: 39 records (1.9%); under the fertility-only frame 11 (0.5%). Records naming an identification strategy: 169; naming one AND debt AND a fertility outcome: **5** — the scope's central asymmetry, re-measured on the citation channel.

## Per-seed detail

`frame` = share of the seed's forward citers the production frame would reach. `fert` = share the fertility-only frame would reach. `P2` = count carrying debt, policy and fertility together. A truncated pull is the high-citation HEAD, not a random sample, so any truncated seed also carries an EXACT count from two count-only queries.

| Cell | Anchor | back | fwd | frame | fert-only | ident | policy | P2 | career | gen-debt |
|---|---|---|---|---|---|---|---|---|---|---|
| `P1_DEBT_FERTILITY` | Can't afford a baby? Debt and youn | 63 | 93/93 | 12.9% | 9.7% | 7.5% | 2.2% | 0 | 0.0% | 11.8% |
| `P1_DEBT_FERTILITY` | Racial and Ethnic Variation in the | 57 | 29/29 | 13.8% | 13.8% | 3.4% | 6.9% | 0 | 0.0% | 6.9% |
| `P1_DEBT_FERTILITY` | Student loan debt and family forma | 26 | 3/3 | 0.0% | 0.0% | 0.0% | 33.3% | 0 | 0.0% | 0.0% |
| `P6_INTENTIONS` | Social Norms and Expectations abou | 43 | 15/15 | 6.7% | 0.0% | 0.0% | 6.7% | 0 | 0.0% | 0.0% |
| `P6_INTENTIONS` | Parents, Partners, Plans, and Prom | 43 | 19/19 | 5.3% | 0.0% | 5.3% | 5.3% | 0 | 0.0% | 5.3% |
| `P3_MARRIAGE` | Debt, Cohabitation, and Marriage i | 91 | 193/193 | 8.3% | 4.7% | 3.1% | 0.5% | 0 | 1.0% | 8.3% |
| `P3_MARRIAGE` | Do student loans delay marriage? D | 42 | 61/61 | 21.3% | 14.8% | 11.5% | 8.2% | 1 | 1.6% | 4.9% |
| `P3_MARRIAGE` | Student loans or marriage? A look  | 29 | 85/85 | 17.6% | 10.6% | 11.8% | 12.9% | 0 | 4.7% | 4.7% |
| `P4_HOUSING` | Student Loans and Homeownership | 16 | 110/110 | 9.1% | 3.6% | 10.9% | 15.5% | 0 | 1.8% | 7.3% |
| `P4_HOUSING` | On the Effect of Student Loans on  | 9 | 21/21 | 19.0% | 4.8% | 9.5% | 14.3% | 0 | 0.0% | 9.5% |
| `P4_HOUSING` | Into the Red and Back to the Nest? | 44 | 109/109 | 6.4% | 2.8% | 3.7% | 1.8% | 1 | 1.8% | 6.4% |
| `P4_HOUSING` | Returning to the Nest: Debt and Pa | 12 | 12/12 | 8.3% | 0.0% | 8.3% | 0.0% | 0 | 0.0% | 0.0% |
| `P4_HOUSING` | A Day Late and a Dollar Short: Liq | 71 | 60/60 | 5.0% | 0.0% | 11.7% | 25.0% | 0 | 0.0% | 8.3% |
| `P4_HOUSING` | Does Student Loan Debt Structure Y | 37 | 14/14 | 7.1% | 0.0% | 21.4% | 0.0% | 0 | 0.0% | 0.0% |
| `P4_HOUSING` | Student Loan Debt, Educational Att | 21 | 7/7 | 42.9% | 0.0% | 0.0% | 0.0% | 0 | 0.0% | 0.0% |
| `P5_RESOURCE` | Constrained after college: Student | 35 | 457/457 | 4.2% | 1.8% | 14.9% | 14.0% | 0 | 2.8% | 3.3% |
| `OFF_CAREER_BOUNDARY` | Medical student debt and major lif | 21 | 111/111 | 0.0% | 0.0% | 0.0% | 0.9% | 0 | 44.1% | 0.9% |
| `OFF_WALL3_REPAYMENT` | A Crisis in Student Loans? How Cha | 62 | 280/280 | 4.3% | 0.7% | 10.4% | 16.4% | 0 | 0.4% | 4.3% |
| `OFF_WALL6_PARENT_HELD` | The Other Student Debt Crisis: How | 43 | 18/18 | 5.6% | 5.6% | 11.1% | 16.7% | 1 | 0.0% | 5.6% |
| `OFF_WALL7_LMIC` | Impact of Tuition-Free Education P | 73 | 31/31 | 0.0% | 0.0% | 6.5% | 12.9% | 0 | 0.0% | 0.0% |
| `OFF_WALL2_GENERAL_DEBT` | Does Limited Access to Mortgage De | 59 | 72/72 | 0.0% | 0.0% | 1.4% | 0.0% | 0 | 0.0% | 2.8% |

### DOI-less anchor seed recovery

Every anchor without a DOI gets ONE gated recovery attempt. An anchor that cannot seed is a hole in the frame and is reported as one.

| Anchor | book | recovered | note |
|---|---|---|---|
| Graduate indebtedness: its perceived effects on behaviou | no | **no** | no non-bookish record with first-author agreement |
| Changes in U.S. Family Finances from 2010 to 2013: Evide | no | **no** | no non-bookish record with first-author agreement |
| Student loan forgiveness and the timing of first births | no | **no** | no non-bookish record with first-author agreement |

## Walls, sized inside the citation neighbourhood

`199_` sized each wall against the whole literature. These are their sizes where the screen will actually meet them — inside the frame, not outside it.

| Wall | Share of Tier B | Share within the production frame |
|---|---|---|
| 1 — health-professions career | 79 (3.8%) | 3 (7.7%) |
| 2 — general household debt | 79 (3.8%) | 2 (5.1%) |
| 3 — default and repayment | 55 (2.7%) | 3 (7.7%) |
| 5/6 — parents' balance sheet | 11 (0.5%) | 0 (0.0%) |
| 7 — LMIC school fees | 64 (3.1%) | 0 (0.0%) |

## Findings

*Written after reading the measurements above, then re-run so the log regenerates rather than being
hand-edited.*

- **THE SCOPE'S CENTRAL FINDING IS PARTLY OVERTURNED, AND THE CHANNEL BUILT TO CONTRADICT IT IS WHAT
  DID IT.** The P2 policy-variation cell is not empty. The citation channel surfaced *Experimental
  Evidence on Consumption, Saving, and Family Formation Responses to Student Debt Forgiveness* (SSRN
  2022, `10.2139/ssrn.4139814`, 1 cite, reached independently by THREE seeds) — a randomized
  evaluation of debt forgiveness with a family-formation outcome, which is precisely the study shape
  the scope declared absent from the literature.
- **Why the query missed it, diagnosed rather than guessed.** `200_`'s policy block carried
  `"loan forgiveness"` but not `"debt forgiveness"`; its outcome block carried `"family size"` but
  not `"family formation"`. Adding the first takes that cell from 5 records to 6; adding the second,
  6 to 7. The record has NO indexed abstract, so its title was the only searchable text it ever had.
  **The scope's sentence — "There is no natural experiment in student debt with a fertility outcome
  anywhere in the indexed literature" — is false as written and is corrected.** What survives is
  narrower and still worth reporting: no PUBLISHED, peer-reviewed policy-variation study with a
  fertility outcome exists, and the sole candidate is an uncited preprint that must be retrieved and
  read before any verdict.
- **The generalisable form: an empty-cell finding measured through one hand-written vocabulary block
  is a claim about the block, not about the literature.** It needs a second, orthogonal channel
  before it can be reported as a property of the field. Here the second channel cost one script and
  overturned the first channel's headline.
- **The production frame cannot reach two of its own fifteen empirical anchors, and one is the
  chapter's most-cited primary-cell work.** Nau et al. 2015 scores `debt=False, fert=False`: its
  OpenAlex record carries NO abstract, and its title says *Debt*, not *student debt*, and *baby*,
  not any term in the outcome vocabulary. *Returning to the Nest* fails the same way on the exposure
  axis despite having an abstract. This is the measured price of student-anchoring the exposure,
  which was adopted to defeat the 1,389-record sovereign-debt homonym: the anchoring that defeats
  the homonym also loses the canon. Both rules are right and they conflict; the cost is 2 of 15 and
  it is priced here rather than argued. **Operational consequence: Tier A enters the screen by hand
  and never through the frame.** That is already the practice, and this is the measurement showing
  why it must stay.
- **The identification diagnostic was refuted by its own output.** The first `IDENT_TERMS` carried
  "natural experiment", "quasi-experimental" and "randomi" but no bare "experiment", so it scored the
  run's single most important record — whose title begins *Experimental Evidence* — as NOT
  identified, inside the table built to surface identified policy studies. Across Tier B, 78 records
  name "experiment" and the original list missed 46 of them. Corrected, the count of records carrying
  debt AND a fertility outcome AND an identification strategy goes from 3 to 5.
  `ident_vocab_selftest()` makes a recurrence a start-up failure.
- **Recall(A) settles the two-arm frame decision on evidence rather than on the scope's argument.**
  The production frame reaches 13 of 21 anchors (13 of 15 empirical); a fertility-only frame reaches
  5 of 21. Eight empirical anchors — every identified study in the chapter, Mezza et al., Addo,
  Gicheva and Goodman/Isen/Yannelis among them — are reachable ONLY through the chain arm's outcome
  vocabulary. A frame restricted to the chapter's registered outcome would retrieve none of its
  identified evidence. Same ruling as A.17's loose frame, reached in a different chapter for a
  different reason.
- **The attainment confound is more visible than the scope assumed, and the scope is revised.** It
  was declared unenforceable at title/abstract on the strength of 8 records at query level. Within
  the production frame it is 11 of 39 (28.2%); across Tier B, 6.4%. That is a positive PRIOR at
  screen — the same shape as A.17's Wall 5, where "unenforceable" turned out to be "enforceable with
  an `INSUFFICIENT_INFO` bucket". It stays a full-text extraction field and a risk-of-bias domain,
  and the screen now also carries a flag.
- **The routing-visibility claim holds, on a base too small to lean on.** Within the frame the screen
  will see, 77% of records carry exactly one outcome axis and are routable; 23% carry two or three
  and must be routed at full text. The claim was asserted about vocabulary and is now measured — but
  the base is 39 records, so this is weak confirmation, and the 23% is the number to watch.
- **No seed truncated.** Every forward pull returned its full count, so no exact-rate correction was
  needed and no fraction reported here is a high-citation-head artifact. Stated because the opposite
  has bitten this project, and because a reader cannot tell the difference from the table alone.
- **The two channels barely overlap, which is what makes Recall(B) meaningful here.** Tier B is 2,071
  records and only 39 (1.9%) sit inside the production query frame. 31% depend on a decoy, review,
  exposure-series or negative-control seed alone and are droppable from any recall computation via
  `seed_ids`.
- **One more record for the screen's attention, surfaced by the corrected diagnostic:** *Does the
  Student-Loan Burden Weigh into the Decision to Start a Family?* (2011, 22 cites) carries debt, a
  fertility outcome and identification language. It was visible in `199_` under the marriage cell and
  is a direct-arm candidate, not a chain-arm one.

