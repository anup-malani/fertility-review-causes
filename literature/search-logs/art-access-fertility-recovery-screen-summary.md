# D2 title/abstract screen — art-access-fertility-recovery (A.17)

**1,020 records screened across 17 batches.** 192 RELEVANT · 212 UNCERTAIN · 616 NOT_RELEVANT.

Coverage is asserted rather than assumed: every worklist record carries exactly one verdict, every verdict id is in the worklist, and no id carries two.

## The arm split: the scope said invisible, A4 said partly visible

The scope declared the arm-1/arm-2 distinction undecidable at title/abstract because it is settled in the methods section. A4 measured identification vocabulary at 1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones and called it a real but thin prior. The screen is the tiebreak, and the statistic is the share of `cannot_tell` — the one number here that does not depend on the assignments being right.

| arm | n | share |
|---|---|---|
| `arm1_counting` | 50 | 4.9% |
| `arm2_estimate` | 78 | 7.6% |
| `neither` | 745 | 73.0% |
| `cannot_tell` | 147 | 14.4% |

**`cannot_tell` across the whole worklist: 147 of 1,020 (14.4%).** Restricted to the 347 records the screen placed in an A.17 cell, it is 127 (36.6%).

**Reading.** The scope was too strong and A4 was closer. A sixth of the worklist could not be routed on the visible record — a real cost, but far from the total blindness the scope assumed. Inside the primary cells the share is higher, which is the expected direction: those are the records where the distinction actually has to be made, and the off-cell records take `neither` for free. **The operational consequence: the screen can carry the routing for roughly four records in five, and the remainder is a defined full-text queue rather than an unbounded one.**

## Wall 5, re-read independently of the term matcher

A4 measured the preservation population by vocabulary — 76% oncological, 5% elective, 17% naming neither — and narrowed the scope's blanket 'unenforceable' to that 17%. The screener assigned `preservation_indication` without seeing the term hits.

| indication (screener) | n |
|---|---|
| `onco` | 134 |
| `elective` | 51 |
| `neither` | 17 |
| `n_a` | 818 |

D1 flagged 208 records as preservation by vocabulary; the screener assigned an indication to 202, and the two agree on 190.

Where D1 said ELECTIVE, the screener said: {'elective': 32, 'n_a': 8, 'onco': 8, 'neither': 1}.
Where D1 said RESIDUE (neither indication named), the screener said: {'n_a': 10, 'elective': 18, 'neither': 13, 'onco': 85}.

**The finding, and it corrects A4 rather than confirming it.** Reading the residue shows most of it is not ambiguous at all — it is MEDICAL preservation for a non-oncological indication: Turner syndrome, sickle cell anaemia, cystic fibrosis, BRCA carriage, haematopoietic transplant, and gender-affirming care. The term list looked for cancer words, did not find them, and returned 'neither'. **Wall 5 was cut as onco-versus-elective and the real structure is MEDICAL versus ELECTIVE, with medical splitting into oncological and everything else.** The residue is therefore smaller than A4 estimated and the wall is more enforceable, but the taxonomy needs a third value before extraction: `medical_non_onco`. Gender-affirming preservation in particular is neither of the two labels on offer and appeared repeatedly.

## Per-bypass yield

The standing rule from A.12: an inherited bypass that has stopped paying should be retired rather than carried forever. Each bypass's own survival rate is reported so the next chapter inherits a measurement.

| worklist reason | n | RELEVANT | UNCERTAIN | in an A.17 cell | relevant rate | cell rate |
|---|---|---|---|---|---|---|
| `budget_slice` | 800 | 170 | 194 | 317 | 21.2% | 39.6% |
| `bypass_wall5_residue` | 105 | 4 | 8 | 10 | 3.8% | 9.5% |
| `bypass_arm1_accounting` | 69 | 9 | 3 | 6 | 13.0% | 8.7% |
| `bypass_arm2_identified` | 23 | 1 | 0 | 1 | 4.3% | 4.3% |
| `bypass_elective_preservation` | 23 | 8 | 7 | 13 | 34.8% | 56.5% |

## The no-abstract instruction, checked rather than trusted

D1 flagged 234 title-only records in the worklist. The rubric told the screener to bucket them `INSUFFICIENT_INFO` rather than `NOT_RELEVANT`, because a `NOT_RELEVANT` on an invisible record records *not visible* as *not relevant*.

| | with abstract | title only |
|---|---|---|
| n | 786 | 234 |
| RELEVANT | 19.0% | 18.4% |
| UNCERTAIN | 20.4% | 22.2% |
| NOT_RELEVANT | 60.7% | 59.4% |
| routed to `INSUFFICIENT_INFO` | — | 0 |

## Cells

| cell | n |
|---|---|
| `OFF_OTHER` | 270 |
| `OFF_ONCOFERTILITY` | 144 |
| `P6_INDUCED_POSTPONEMENT` | 107 |
| `P1_MANDATE` | 81 |
| `OFF_CLINICAL` | 56 |
| `P4_POSTPONEMENT_RECOVERY` | 48 |
| `ROUTE_B_SUBFECUNDITY` | 45 |
| `P3_ART_SHARE` | 43 |
| `P5_ELECTIVE_PRESERVATION` | 43 |
| `ROUTE_A15_POSTPONEMENT` | 40 |
| `OFF_SAFETY` | 38 |
| `EXPOSURE_SERIES` | 38 |
| `ROUTE_A12_MULTIPLES` | 30 |
| `P2_AVAILABILITY` | 25 |
| `OFF_COST_EFFECTIVENESS` | 12 |

## Outcome types

| outcome | n |
|---|---|
| `other` | 399 |
| `population_fertility` | 170 |
| `belief_or_attitude` | 154 |
| `utilisation_only` | 112 |
| `per_cycle_clinical` | 46 |
| `safety` | 42 |
| `postponement` | 38 |
| `multiple_birth_rate` | 26 |
| `cost` | 20 |
| `none_visible` | 13 |

## The two arms, counted

- **Arm 1 (accounting): 91 records** across `P3_ART_SHARE` and `P4_POSTPONEMENT_RECOVERY`.
- **Arm 2 (access): 106 records** across `P1_MANDATE` and `P2_AVAILABILITY`.

**These are not summed and never should be.** Arm 1 counts ART births and bounds the registry claim from above; arm 2 estimates the response to access and bounds it from below. A single count across both would be a count of two literatures answering two questions.

## Findings

- **THE NO-ABSTRACT INSTRUCTION DID NOT BIND, AND THIS CHECK IS THE ONLY REASON THAT IS VISIBLE.** 0 of 234 title-only records were routed to `INSUFFICIENT_INFO`, and their verdict distribution is within two points of the abstracted records at every level (59.4% against 60.7% NOT_RELEVANT). The rubric allowed a title to be decisive 'when it often is', and in practice the screener treated titles as decisive almost always. Two readings are consistent with these numbers — titles in this literature really are about as informative as abstracts, or the screener over-claimed decisiveness — and **this check cannot distinguish them.** What it does establish is that the safeguard was inert. The RA spot-check should be stratified on `no_abstract` rather than drawn at random, because that is where a systematic error would sit.
- **The Wall 5 residue is mostly not ambiguous — it is MEDICAL.** Of the records D1 flagged as naming neither indication, the screener read 85 as oncological and only 13 as genuinely indeterminate. A4's 17% residue was largely an artifact of a term list that looked for cancer words in a truncated abstract and did not find them. The wall is more enforceable than A4 said and much more enforceable than the scope said — but it needs a third value, `medical_non_onco`, before extraction: Turner syndrome, sickle cell, cystic fibrosis, BRCA carriage, transplant conditioning and gender-affirming care all appeared and none of them is oncological or elective.
- **Bypass yields differ by an order of magnitude, and the cheapest one won.** `bypass_elective_preservation` returned 34.8% RELEVANT and put 56.5% of its records in an A.17 cell on 23 records; `bypass_wall5_residue` returned 3.8% on 105. The elective-preservation bypass is the one the recon probe suggested would be near-empty, and it is the most productive per record in the whole worklist. **Carry it forward; the arm-2 bypass earned its place by insurance rather than by yield** — it existed because missing an identified estimate is unrecoverable, and it found one.
- **The arm split is roughly four-fifths screenable.** `cannot_tell` is 14.4% overall. The scope's blanket declaration of invisibility was wrong; A4's 'partly visible' was right. The chapter should say the routing is a screen decision with a defined full-text remainder, not a full-text decision throughout.
- **Neither arm dominates the other in size** (91 arm-1 records against 106 arm-2). That matters for the write-up: a reader seeing two comparable piles will assume they are two halves of one evidence base. They are two answers to two questions, and the chapter has to say so before it reports either number.

