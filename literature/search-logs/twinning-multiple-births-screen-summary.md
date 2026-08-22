# D2 title/abstract screen — twinning-multiple-births (A.12)

**1,376 records screened across 23 batches; coverage asserted, not assumed.** Every worklist record carries exactly one verdict and every verdict id is in the worklist. The check earned its keep on the first assembly, catching a phantom id introduced by a single-digit typo.

**441 RELEVANT · 225 UNCERTAIN · 710 NOT_RELEVANT**

## Cells

| cell | n |
|---|---|
| `OFF_PERINATAL` | 288 |
| `OFF_OTHER` | 252 |
| `EXPOSURE_SERIES` | 241 |
| `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` | 223 |
| `SECONDARY_ART_MULTIPLES` | 149 |
| `OFF_NONHUMAN` | 66 |
| `OFF_ART_CLINICAL` | 58 |
| `SECONDARY_PM_VARIATION` | 35 |
| `OFF_TWINDESIGN` | 31 |
| `PRIMARY_OFFSET_STOPPING` | 14 |
| `OFF_ART_UPTAKE_A17` | 11 |
| `OFF_HOMONYM_ENGINEERING` | 5 |
| `INSUFFICIENT_INFO` | 3 |

## The primary cell is four times the anchor set

**`PRIMARY_OFFSET_STOPPING`: 14 records.** The frozen scope named THREE stopping-offset studies (Alter & Hacker 2024, Robson & Smith 2012, Clark-Cummins-Curtis 2020). The screen finds four times that, and the additions are not marginal — they include a direct published comment on Robson & Smith in the same journal, a Nature Communications study reporting the OPPOSITE sign in pre-industrial Europe, Swedish register childbearing patterns for mothers of twins, 19th-century Dutch maternal life histories, and a JPE paper whose outcome is time to next birth.

This is the Tier-A-anchors-are-studies lesson restated: reporting the anchor set as the evidence base would have understated this cell by a factor of four, and would have concealed that its members DISAGREE.

`PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE`: 223 records, all UNCERTAIN by construction — Wall 8 says the first-stage table is invisible at title/abstract, so these are routed to full text rather than adjudicated here.

## Wall 6 cross-check — does the screen's outcome reading agree with D1's terms?

Wall 6 was re-cut on OUTCOME and D1 was forbidden from applying it, so this is the measurement the re-cut stands or falls on. `outcome_type` was assigned by the screen WITHOUT sight of D1's clinical term-hits.

**Agreement: 85.0%** (344 both clinical, 825 neither).

- **126 records D1 flagged clinical but the screen did not.** These are the false positives a term sieve produces: population twinning-rate papers that mention preterm birth or birthweight in passing.
- **81 records the screen read as clinical but D1's terms missed.**

**The seam itself.** Of the 149 `SECONDARY_ART_MULTIPLES` records, **49 carry a population or registry outcome** (the Wall 6 INCLUDE side) and **100 carry a per-cycle clinical outcome** — the genuine boundary, where the treatment is identical to an excluded study and only the outcome separates them. A further 58 records went to `OFF_ART_CLINICAL`.

**Verdict on the wall: enforceable, but only per-paper.** The screen could separate outcome types record by record. What it could NOT do is infer them from context — the include-side anchor Reynolds 2003 sits at 50.8% clinical vocabulary against the exclude-side Thurin's 60.6%, so any cloud-level or term-level shortcut fails. The wall holds because a human read each abstract's outcome, and the scope should say so.

## Did the bypasses earn their place?

| worklist reason | n | not NOT_RELEVANT | yield |
|---|---|---|---|
| `budget_top` | 800 | 492 | 61.5% |
| `bypass_both_axes` | 324 | 79 | 24.4% |
| `bypass_wall8` | 212 | 93 | 43.9% |
| `bypass_orthogonal` | 40 | 2 | 5.0% |

The Wall 8 bypass is the one to read closely: it was re-gated during D1 after the first version recovered 4 records instead of 212, and its yield here is what that re-gating bought.

## Outcome types

| outcome_type | n |
|---|---|
| `perinatal_health` | 288 |
| `other` | 275 |
| `twinning_rate` | 265 |
| `child_outcome` | 256 |
| `population_births` | 152 |
| `per_cycle_clinical` | 137 |
| `unclear` | 3 |

## Highest-priority full text

| cell | title | why |
|---|---|---|
| `PRIMARY_OFFSET_STOPPING` | Mothers with higher twinning propensity had lower fertility in pre-ind | MAJOR FIND, not in the anchor set. Nature Communications 2022: mothers with higher twinning PROPENSITY had LOWER fertility in pre-industrial Europe. Directly contradicts Robson & Smith 2012  |
| `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` | The causal effect of an additional sibling on completed fertility: An  | STRONGEST first-stage candidate so far and RELEVANT rather than UNCERTAIN: the outcome is COMPLETED FERTILITY and the design is siblings of twins, so the estimand is visible in the abstract  |
| `PRIMARY_OFFSET_STOPPING` | Why is lifetime fertility higher in twinning women? | MAJOR. A direct published COMMENT on Robson & Smith 2012 in the same journal, asking why lifetime fertility is higher in twinning women. The anchor's own controversy, and it was not in the a |
| `PRIMARY_OFFSET_STOPPING` | The Effect of Welfare Payments on the Marriage and Fertility Behavior  | MAJOR, and not in the anchor set. JPE: twin births generate within-state variation in welfare benefits, and the OUTCOME IS TIME TO NEXT BIRTH — i.e. subsequent fertility after a twin birth.  |
| `PRIMARY_OFFSET_STOPPING` | Childbearing patterns for Swedish mothers of twins, 1961-1999 | MAJOR, not in the anchor set. Demographic Research: CHILDBEARING PATTERNS of Swedish mothers of twins, 1961-99 — the offset estimated directly on a population register. |
| `EXPOSURE_SERIES` | Continuing decline in twin births since 2014 | MAJOR for the time-inversion. A published letter in Human Reproduction responding to Monden et al. 2021 (the Twin Peaks anchor) reporting CONTINUING DECLINE SINCE 2014. The anchor's own corr |
| `EXPOSURE_SERIES` | The rate of twin birth is declining | MAJOR for the time-inversion, and its opening sentence is the finding: papers have spent a decade reciting a global RISE that has since reversed. This is v5's error, in the clinical literatu |
| `EXPOSURE_SERIES` | Demographic Analysis of the Variation in the Rates of Multiple Materni | MAJOR EXPOSURE SOURCE: Swedish multiple maternities SINCE 1751 — the longest continuous national twinning series there is, and the one that lets the PM arm be bounded arithmetically |
| `PRIMARY_OFFSET_STOPPING` | Maternal Life-Histories of Multiple Birth Mothers Compared to Singleto | MAJOR, not in the anchor set. Maternal LIFE HISTORIES of multiple-birth vs singleton-only mothers, 19th-early 20th century Netherlands — the offset on historical microdata, i.e. exactly the  |
| `PRIMARY_OFFSET_STOPPING` | Evidence that prenatal testosterone transfer from male twins reduces t | SCOPE GAP. PNAS: prenatal testosterone transfer from a male co-twin REDUCES the female co-twin's fertility. This is an INTERGENERATIONAL offset — twinning lowers the next generation's fertil |
| `EXPOSURE_SERIES` | Effects of Folic Acid Fortification on Twin Gestation Rates | STRONG: folic acid FORTIFICATION is a population-level natural experiment on the twinning rate — one of very few exogenous shocks to the exposure that exist |
| `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` | Twins Studies in Economics | HIGH-PRIORITY FULL TEXT: an Oxford handbook chapter on twins methods IN ECONOMICS. A methods survey is the densest available source of first-stage discussion, and Wall 8 means it cannot be f |
| `SECONDARY_ART_MULTIPLES` | Re-Thinking Elective Single Embryo Transfer: Increased Risk of Monocho | IMPORTANT AND AGAINST THE GRAIN: a systematic review finding eSET RAISES monochorionic (MZ) twinning. eSET cuts DZ multiples but induces MZ ones, so the policy's net effect on m_ART is small |
| `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` | CHILDREN AND THEIR PARENTS: A REVIEW OF FERTILITY AND CAUSALITY | HIGH-VALUE FULL TEXT: a Journal of Economic Surveys review of fertility and causality — a second dense entry point to first stages alongside W2224629890 |
| `SECONDARY_PM_VARIATION` | Évolution et sélection de la gémellité | STRONG PM RECORD: continuous parish records from Artas, France, 1540-1900 — twinning and selection across the whole pre-transition and transition period |
| `EXPOSURE_SERIES` | Body composition, smoking, and spontaneous dizygotic twinning | THIS IS THE HOEKSTRA TRAP, now in the frame. NO ABSTRACT. 'Body composition, smoking, and spontaneous dizygotic twinning', Fertility & Sterility 2008 — the real Hoekstra 2008 paper that v5's |
| `EXPOSURE_SERIES` | An age-dependent ovulatory strategy explains the evolution of dizygoti | MAJOR. Nature Ecology & Evolution: an AGE-DEPENDENT OVULATORY STRATEGY explains the evolution of DZ twinning. This is the mechanism underneath the whole age-twinning gradient, and therefore  |
| `EXPOSURE_SERIES` | The Vanishing Fetus | MAJOR FOR THE IDENTITY. 'The Vanishing Fetus' states the correction directly: ultrasonography confirms that the number of CONCEIVED multiple pregnancies exceeds the number of multiple BIRTHS |
| `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` | Natural “Natural Experiments” in Economics | HIGH-VALUE FULL TEXT: Rosenzweig & Wolpin's JEL review of natural experiments, by the authors of the twin instrument itself. Third dense first-stage entry point alongside W2224629890 and W26 |
| `SECONDARY_ART_MULTIPLES` | What can we learn from a decade of promoting safe embryo transfer prac | STRONG POLICY COMPARISON: UK vs Australia over a decade of transfer policy, holding socio-demography and cost roughly fixed. The closest thing to a controlled comparison on m_ART policy. |
| `EXPOSURE_SERIES` | Twin Deliveries in the United States Over Three Decades: An Age-Period | STRONG: an AGE-PERIOD-COHORT decomposition of three decades of US twin deliveries. The only design in the exposure series that separates maternal-age composition from period effects formally |
| `SECONDARY_ART_MULTIPLES` | Multifetal Pregnancy After Implementation of a Publicly Funded Fertili | STRONG POLICY DESIGN AND A CLEAN CALL 3 CASE: Ontario introduced PUBLIC FUNDING for fertility treatment in 2015 (A.17's access channel) and the measured outcome is MULTIFETAL PREGNANCY (A.12 |
