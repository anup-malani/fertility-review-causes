# Co-Residence with Parents and Delayed Household Formation

**Category:** A — Demographic and family-structure explanations · **Registry:** HYPOTHESES-v5.md §A.23

**Primary mechanism.** Young adults who remain in the parental home form unions later and start
childbearing later, so a rise in the share living with parents lowers period fertility.

**Cross-references:** C.2.c housing costs · A.7 age at marriage and union timing · C.2.a childcare
cost and availability · C.5.a economic uncertainty · C.3.g student debt · D.2.b family norms

**Status:** TICK-075. Drafted 2026-08-28 by Shravan with Claude Code. **Not PI-reviewed.** Five
rulings are taken and pending confirmation. Written on 101 of 436 wanted full texts (23%); 89 of
those are machine-readable.

---

## 1. The claim

### 1.1 In plain terms

In plain terms: the argument is that the parental home is a waiting room, and that the longer people
sit in it the fewer children they have.

The picture behind the hypothesis is familiar and it is roughly true as description. In Italy and
Spain, and increasingly in the United States, people in their twenties live with their parents in
numbers that would have been unusual in 1970. Nearly one in two Americans aged 18 to 29 now lives
with a parent, against slightly more than one in four in 1960. Over the same decades fertility fell.
The hypothesis proposes that the first fact helps cause the second: you cannot easily start a family
in your childhood bedroom, so a household that never forms is a family that never starts.

There is a second thing the same words describe, and it is the reason this chapter is more
complicated than the paragraph above. In much of East Asia and Southern Europe, "living with
parents" means a married couple sharing a house with a parent or parent-in-law who cooks, minds the
baby, and makes a second child affordable. That arrangement is a subsidy to childbearing, not an
obstacle to it. The same three words name a constraint in one setting and a support in another, and
they are frequently the same three words in the same dataset.

### 1.2 The claim precisely

**This chapter explores the effect of co-residence with parents on fertility.**

**The parameter this chapter estimates is the change in a person's births caused by living in a
parental household rather than an independent one, measured in births per person exposed.**

The registry entry describes only the first configuration — an unpartnered, childless young adult
who has not yet left home. This chapter covers both, and reports a verdict conditional on which one
is meant, for a reason that is decided rather than discovered: restricting the chapter to the
configuration the hypothesis names would report only the estimates whose direction agrees with the
claim. That is selection on the outcome of the review.

The claim decomposes into two links that must be established separately.

1. **Something moves the arrangement.** A price, a policy or a labour market changes how many young
   adults live with a parent.
2. **The arrangement moves fertility.** Living with a parent changes whether and when a person has a
   child, holding everything else fixed.

The hypothesis is a claim about link 2. Most of the evidence, as this chapter will show, is about
link 1.

---

## 2. Theoretical mechanism

For the reader with price theory: co-residence changes the shadow price of a child in two directions
at once, and which direction wins depends on who is in the household.

**Where the co-resident is a young adult who has not formed a couple**, the parental home raises the
cost of the *union* that normally precedes the birth. Privacy, autonomy and the ability to form a
household with a partner are inputs to childbearing that the parental home rations. The predicted
effect is a reduction in fertility, running through delay rather than through a decision never to
have children.

**Where the co-resident is a couple living with a parent or parent-in-law**, the parent supplies
childcare and household labour at close to zero marginal cost. That lowers the price of a child
directly. The predicted effect is an increase in fertility, and it is the modal arrangement in the
East Asian literature and a substantial part of the Southern European one.

**What would make the hypothesis wrong.** Three things, and the chapter finds evidence bearing on
each. First, the association could run backwards: people who intend to have a child leave home in
order to do so, which produces the observed correlation with no causal effect of the arrangement.
Second, the association could be produced by a third factor — youth unemployment, housing costs,
student debt — that moves both the arrangement and the birth. Third, the effect could be entirely
about timing: if living with parents delays a first birth by two years but leaves completed family
size unchanged, the mechanism moves a period measure of fertility and explains none of the decline
in the number of children people eventually have.

**The exposure and the outcome are events in the same life-course sequence.** Leaving home,
partnering and having a first child usually happen within a few years of each other and in that
order. A comparison of people who have left home with people who have not will find a fertility
difference under the null hypothesis that the arrangement does nothing, because the comparison is
partly a comparison of people further along the same sequence. This is the chapter's central
identification problem and it is why the design requirements below are strict.

---

## 3. Search strategy

The search is documented in full in `literature/search-logs/`. Three features of it change how the
results should be read.

**No prior systematic review of this exposure exists.** The search for one came back empty in two
independent vocabularies. That removes the usual external-authority source for the anchor set, so
the chapter's seed studies were assembled from a neighbouring finished chapter's routed-out records
and from citation snowballing.

**The boundary with housing costs was inherited rather than drawn here.** The housing-costs chapter
owns variation in prices; this chapter owns variation in the arrangement. Where a policy changes a
price *in order to* change the arrangement — a subsidy conditional on renting, for instance — the
record is reported by both chapters and its magnitude is claimed by neither alone. That decision
matters more than boundary decisions usually do, and §5 explains why.

**One wall could not be enforced at the title and abstract stage, and this was stated in advance.**
"Co-residence with parents" is also the standard term for an adult child housing an elderly parent —
a large gerontology literature in which the dependency runs the other way. Distinguishing the two
requires knowing the ages and the direction of support, which is usually a fact about a table of
descriptive statistics rather than about an abstract. The screen routed 148 records to that
literature on the visible evidence and the boundary was re-checked at full text.

---

## 4. PRISMA flow

| Stage | n |
|---|---|
| Records in the production frame | 1,572 |
| Screened at title and abstract | 1,572 |
| Judged relevant | 78 |
| Judged uncertain | 400 |
| Routed out | 1,094 |
| Queued for retrieval, ordered by what the synthesis needs | 436 |
| Full texts obtained | 101 |
| Machine-readable | 89 |
| Effects extracted | 16 |

**Two features of this funnel change how the chapter should be read.**

The retrieval rate is 23%, and the rate is not the problem — its shape is. The tier holding the
open boundary question was retrieved at 19% and the identified designs at 41%, against 23% overall.
The records publishers defend hardest are the ones this chapter most needed.

The second feature is the gap between 78 records judged relevant and 16 extracted effects. It is not
attrition through retrieval. It is that most records in this literature describe the joint
distribution of living arrangements and childbearing without estimating an effect of one on the
other.

---

## 5. Included studies

Sixteen effects from thirteen studies. The full table with the sentence each number was read from is
in `extraction/co-residence-parents-household-delay.csv`.

| Configuration | Effects | Identified designs |
|---|---|---|
| Young adult in the parental home (the registered claim) | 2 | **0** |
| Couple with a parent or parent-in-law | 6 | 1 |
| Residential proximity without co-residence | 1 | 0 |
| Policies changing a price to change the arrangement | 3 | 2 |
| Drivers moving the arrangement, no birth outcome | 4 | 4 |

### 5.1 The naive estimator, and what correcting it does

The comparison an author makes without thinking hard is between people who live with a parent and
people who do not, at a point in time. In this literature that comparison is contaminated in a
specific and knowable way: the arrangement and the birth are events in the same sequence, so the
comparison partly compares people at different stages of one life course.

One included study corrects for it. Chu, Xie and Yu, in *Demography*, treat co-residence with a
husband's parents and the wife's labour supply as jointly determined with the timing of a first
birth, using Taiwanese data on women born between 1933 and 1968. **Correcting for that joint
determination reverses the direction of the co-residence effect.** Uncorrected, living with the
husband's parents looks as though it brings a first birth forward. Corrected, it delays it.

That single result governs how the rest of the evidence is treated. A body containing one corrected
estimate and several uncorrected ones is not heterogeneous evidence about one quantity; it is one
biased estimator and one corrected one. Averaging them would produce a number whose direction
depends on how many uncorrected studies happen to be included.

The chapter cannot report the corrected magnitude, because the full text sits behind a subscription
wall and the direction comes from the abstract. That is the most consequential single item on the
outstanding retrieval list.

### 5.2 The exposure is not one variable, and one study shows it inside one dataset

Hacker, Helgertz, Nelson and Roberts link 3.1 million American couples between the 1900 and 1910 censuses. In the same
regression, a co-resident mother is associated with about 5% lower fertility and a co-resident
mother-in-law with about 3% higher.

Two coefficients, opposite directions, same household type, same data, same specification. Any
estimate of "living with a parent" averages across that contrast, and the average it produces is a
fact about which parent happens to be in the sample rather than a parameter that transfers to
another setting.

The same study reports a far larger coefficient on the density of adult kin living nearby but not in
the household — about 28% higher fertility — and its own conclusion is that declining kin
availability contributed to the American fertility transition. That is a different exposure from the
living arrangement, and the chapter records it as evidence about a neighbouring question.

### 5.3 The best-identified evidence is about the wrong link

Four studies identify an effect cleanly, and all four estimate how something moves the living
arrangement rather than how the arrangement moves fertility. China's rural pension scheme, evaluated
at the eligibility age with a regression discontinuity, sharply reduces the probability that an adult
son lives with his parents in the poorer of two provinces — estimates run from −0.27 to −0.39 on a
probability scale — and has no detectable effect in the richer one. Deferred Action for Childhood Arrivals changes the living arrangements of
eligible young immigrants in the United States. Italy's 2015 employment-protection reform raises
household-formation intentions.

The Deferred Action study is the only one of the four that looks for a fertility effect, and it
reports none.

### 5.4 The one study that estimates both, and it is not retrieved

Laeven and Popov instrument the American housing boom with the predetermined industrial structure of
each metropolitan economy and estimate the effect on home ownership, household formation and
fertility together. Estimating all three under one instrument is what a decomposition of this
chapter's central accounting problem would require, and no other study in the frame does it. The
published article is paywalled and the working-paper version was not retrieved, so only the
direction is in hand: in metropolitan areas with large price increases, the youngest households were
less likely to buy a home, to marry, or to have a child.

### 5.5 A large positive result that is excluded, and why

One study reports an effect far larger than anything else in this chapter: a one-standard-deviation
increase in the prevalence of extended families raises fertility by about 1.07 children per woman,
identified by instrumenting family structure with ancestral plough agriculture.

It is excluded from every part of the synthesis, and the reason is a rule the search strategy set
before this study was found. The unit of observation is a society rather than a household, and the
variation is cross-cultural. Societies that adopted the plough differ from those that did not in
women's participation in agricultural work, in inheritance rules and in gender norms — that is the
main finding of the literature the instrument comes from. For the instrument to identify the effect
of family structure, plough adoption would have to affect fertility only through family structure,
and the adjacent literature is largely about the other channels. The magnitude is itself a reason for
caution: more than a whole child per standard deviation is larger than any household-level estimate
in the chapter by an order of magnitude.

It is recorded here rather than dropped silently, because a reader who finds it will want to know
whether the chapter saw it.

### 5.6 A defect in the chapter's best design

Aparicio-Fenoll and Oppedisano evaluate a Spanish rental subsidy paid from a person's twenty-second
birthday, comparing 22-year-olds with 21-year-olds before and after. The subsidy raised the share
living away from parents by about 1 to 2 percentage points and the probability of having a child by
about 5 to 8 percentage points.

The fertility estimate is conditional on having moved out — and moving out is what the subsidy
caused. Conditioning the outcome on a variable the treatment moves reintroduces exactly the
selection the design was built to remove. The estimate the chapter needs is the unconditional effect
of the subsidy on childbearing, and it is not the one reported.

---

## 6. Quantitative synthesis

### 6.1 The answer in plain terms

Nothing pools, and the reason is worth more than a pooled number would have been.

Sixteen effects sound like enough for a meta-analysis. Grouping them by which configuration they
measure, then by whether the outcome is a birth or an intention, then by whether the estimator
corrects for the sequence problem, leaves groups of at most three. Reading those groups shows that
even three is illusory. One puts a hazard ratio for the age at first birth beside two differences in
the average number of children ever born, which are not the same quantity. The other puts together
three studies whose treatments are a rental subsidy, a lottery win and a house price — none of which
is the living arrangement.

Adding those two distinctions as grouping rules leaves no group larger than two.

### 6.2 The estimate

There is no pooled estimate, and for the configuration the registered claim names there is no
estimate at all.

What the chapter can report is the following.

**For a couple living with a parent, the direction of the association is positive and the
best-corrected estimate reverses it.** A Vietnamese household panel with fixed effects finds the
presence of a grandparent associated with 0.14 additional children (confidence interval 0.08 to
0.19). A Tanzanian comparison finds no difference. An American historical dataset finds the
direction depends on which parent. A Taiwanese study that treats the arrangement as jointly
determined with the birth finds a delay.

**For a young adult in the parental home, there is no effect estimate in the literature.** Two
records reach extraction. One reports an association between leaving home and motherhood whose
authors write, in the same paper, that the desire to become a mother probably causes people to leave
home. The other is measured on Mexican municipalities rather than people.

**The strongest evidence in the chapter concerns whether the arrangement responds to anything
exogenous, and the answer is that it does.** Pensions, immigration status and employment protection
all move it, cleanly identified. None of those studies estimates a fertility effect, and the one
that looks for one finds nothing.

---

## 7. Demographic significance

**The phenomenon to be explained is measured in whole children per woman; this mechanism offers a
shift in the share of a population living in a particular household arrangement.**

Converting the second into the first requires an effect of the arrangement on completed fertility
per person exposed. For the configuration the hypothesis names, no such estimate exists, so the
conversion cannot be performed for the claim as registered. The arithmetic below is therefore a
scale check on the configuration that does have an estimate, and it produces a result the hypothesis
does not predict.

### 7.1 Pre-modern fertility variation

**For pre-modern variation, the verdict is NOT ASSESSED, because the pre-modern household-formation
question was assigned to the chapter on age at marriage and union timing, and no pre-modern evidence
was searched here.**

If it were assessed, the direction would run against the hypothesis: the historical European regions
with stem-family co-residence had higher marital fertility than the regions where couples set up
independent households at marriage.

### 7.2 The first demographic transition

**For the first demographic transition, the verdict is NOT IDENTIFIED, because the only study
reaching the period estimates two co-residence coefficients with opposite directions and attributes
its own headline finding to a different exposure.**

Hacker and colleagues cover 1900 to 1910 with 3.1 million linked couples, which is by far the largest
sample in the chapter. It is also an uncorrected cross-section, its two co-residence coefficients
point in opposite directions, and the coefficient it emphasises is on the availability of kin nearby
rather than on the living arrangement. One study of that shape cannot support a share of a
transition.

### 7.3 The second demographic transition

**For the second demographic transition, the verdict is NEGLIGIBLE and wrong-signed for the
configuration that has an estimate, and NOT IDENTIFIED for the configuration the hypothesis names.**

The share of Americans aged 25 to 29 living in a multigenerational household rose from 13% in 1980
to about 32% in 2019, a rise of 19 percentage points. Applying the only estimate of completed
fertility available for that configuration — 0.14 additional children per exposed household — gives
0.19 × 0.137 = **0.026 additional children**, against a fall in the American total fertility rate of
about 0.86 children over the same era. That is **3% of the decline, in the direction of raising
fertility rather than lowering it.**

The inputs come from two countries and the estimate is not identified, so this is a check on
magnitude and direction rather than a decomposition. The direction is the part that matters. **The
exposure rose; both of its configurations rose; and the two configurations push fertility in
opposite directions.** A calculation that counted only the configuration the hypothesis names would
have credited the whole rise to the decline, while part of the same rise was pushing the other way.

**Two constraints bind any number in this section.**

The first is that a share of this mechanism belongs to another chapter and must not be added to it.
Housing affordability accounts for up to a quarter of the 9-percentage-point rise in American
co-residence between 2000 and 2021. That is the housing-costs chapter's treatment travelling down
this chapter's channel. Both chapters report it; neither claims it alone; adding the two would
double-count one effect inside one review.

The second is that the best-identified evidence anywhere near this chain says the channel moves
timing rather than family size. Bulman, Goodman and Isen use American state lottery wins on the
universe of tax records and find that a windfall pulls a birth forward in the year after the win,
while the effect on total births after five years is close to zero — precise enough to rule out an
increase above 0.01 children per $100,000. The exposure is money rather than the arrangement, so
this is not an estimate of the hypothesis. It bounds it: the financial channel through which housing
and household formation are supposed to work changes when children are born and not how many. A
mechanism that operates through delay is exactly the kind that can move a period fertility measure
and leave completed family size where it was.

---

## 8. GRADE

| Target | Rating | Downgraded for |
|---|---|---|
| Pre-modern variation | NOT ASSESSED | Out of scope by ruling |
| First demographic transition | VERY LOW | Risk of bias; indirectness; imprecision |
| Second transition — young adult in the parental home | VERY LOW | *See note* |
| Second transition — couple with a parent | LOW | Risk of bias; inconsistency |
| Second transition — price-and-arrangement policies | LOW | Indirectness; risk of bias |
| Whether the arrangement responds to anything exogenous | MODERATE | Indirectness |

**The pre-launch rating needs its note read.** VERY LOW there does not describe a weak body of
evidence. It records that there is none: zero identified designs and zero effect estimates in the
cell the registered claim names. GRADE has no category for an empty cell, and a reader who sees VERY
LOW without this sentence will take it for a poorly identified literature rather than an absent one.

**The highest rating in the table is for the wrong question.** The evidence that something moves the
living arrangement is genuinely good. The evidence that the living arrangement moves fertility is
not.

---

## 9. Verdict

The claim that young adults living with their parents is a cause of low fertility is, on the
evidence assembled here, **unevaluated rather than refuted**. The literature that appears to be about
it is mostly about something else: it describes the joint timing of leaving home, partnering and
childbearing, or it estimates what makes young people stay at home. Neither answers whether staying
at home changes how many children they have.

Three findings should carry out of this chapter.

**The variable takes two forms with opposite effects, and one dataset shows the split inside a single
regression.** In 3.1 million American couples in 1900, a co-resident mother goes with lower fertility
and a co-resident mother-in-law with higher. An estimate of "living with a parent" is an average over
whichever parents are in the sample, and it transfers to no other setting.

**The one study that corrects for the fact that the arrangement and the birth are chosen together
reverses the direction of the effect.** Uncorrected estimates say living with a husband's parents
brings a first birth forward. Corrected, it delays it. The literature is not heterogeneous evidence
about one quantity; it is mostly one biased comparison, repeated.

**The channel probably moves timing rather than family size.** The best-identified design in the
vicinity — American lottery wins on administrative tax data — pulls births forward and leaves the
five-year total unchanged. If living with parents works the way housing costs and liquidity work, it
changes when people have children and not how many, which would make it a contributor to the fall in
period fertility measures and not to the fall in completed family size.

**The one number to carry away:** applying the only completed-fertility estimate this chapter has for
the growing configuration to the growth in that configuration accounts for **3% of the American
fertility decline, in the wrong direction**.

---

## 10. Open questions

**For the PI.** Five rulings are taken and unconfirmed, and they should be read as a batch rather
than one at a time: that this chapter owns both configurations; that the pre-modern niche stays with
the chapter on age at marriage; that policies changing a price to change the arrangement are shared
with the housing-costs chapter and non-additive; the pooling rule; and six scope amendments the
screen generated. The first is the most consequential — it is why §7.3 reports a wrong-signed
contribution instead of a supporting one.

**Retrieval priorities, in order.** Chu, Xie and Yu (*Demography*) for the corrected magnitude that
§5.1 turns on; Laeven and Popov for the only joint estimate of household formation and fertility
under one instrument; and Kucheva (*Demography*) for the administrative housing-allocation design.
All three are subscription-walled and need the institutional proxy rather than a browser.

**Studies that do not exist and should.** An estimate of the unconditional effect of a
household-formation subsidy on childbearing — the Spanish design without the conditioning on having
moved out. A design that instruments the living arrangement itself and follows completed cohort
fertility rather than a first birth. And a study that measures which parent is in the household,
since the historical American data says the answer determines the direction.

---

## 11. References

Acolin, A., Lin, D., & Wachter, S. M. (2024). Why do young adults coreside with their parents?
*Real Estate Economics*, 52(1), 7–44.

Aparicio-Fenoll, A., & Oppedisano, V. (2014). Fostering household formation: Evidence from a Spanish
rental subsidy. *B.E. Journal of Economic Analysis & Policy*.

Becca, F., & Esteve, A. (2026). "Family-anchored" transitions to adult life in Mexico.
*Demographic Research*, 54(2), 37–70.

Bulman, G., Goodman, S., & Isen, A. (2022). The effect of financial resources on homeownership,
marriage, and fertility: Evidence from state lotteries. NBER Working Paper 30743.

Cerruti, G., Mazzarella, G., & Migliavacca, M. (2022). Employment protection legislation and
household formation: Evidence from Italy. *Review of Economics of the Household*.

Chen, X., Eggleston, K., & Sun, A. (2017). The impact of social pensions on intergenerational
relationships: Comparative evidence from China. *The Journal of the Economics of Ageing*.

Chu, C. Y. C., Xie, Y., & Yu, R. R. (2014). Coresidence with husband's parents, labor supply, and
duration to first birth. *Demography*, 51(1), 185–204.

del Rey, A., García-Gómez, J., Orfao, G., & Wu, M. (2025). Transitions to motherhood in a
low-fertility country.

Du, J., Huang, Y., Bai, P.-P., Zhou, L., Myers, S., Page, A. E., & Mace, R. (2023). Post-marital
residence patterns and the timing of reproduction. *Proceedings of the Royal Society B*, 290,
20230159.

Gihleb, R., Giuntella, O., & Lonsky, J. (2023). Dreaming of leaving the nest? Immigration status and
the living arrangements of DACAmented. NBER Working Paper 31117.

Hacker, J. D., Helgertz, J., Nelson, M., & Roberts, E. (2021). The influence of kin proximity on
the reproductive success of American couples, 1900–1910. *Demography*.

Kucheva, Y. (2018). Subsidized housing and the transition to adulthood. *Demography*, 55(2),
617–642.

Laeven, L., & Popov, A. (2017). Waking up from the American dream. *Journal of Money, Credit and
Banking*; ECB Working Paper 1910.

Mulema, J. (2025). Family forms and reproductive behaviour in Morogoro region. *International
Journal of Geography, Geology and Environment*, 7(7), 16–21.

Nguyễn, H. A. K., & Dương, N. K. T. (2026). The impact of household structure on fertility: A study
in Vietnam. *Demographic Research*, 54(22), 677–718.

Núñez Medina, G. (2022). Modelación espacial bayesiana de la estructura de los hogares y la
fecundidad en municipios de México. *Población y Salud en Mesoamérica*, 20(1).

Ustyuzhanin, V., Zinkina, J., & Korotayev, A. (2025). Extended family structures exert a causal
influence on fertility. Working paper.

---

## Provenance and standing caveats

**This chapter is written on 101 of 436 wanted full texts (23%).** Of those, 89 are
machine-readable; 5 are in a non-Latin script and were read but not text-mined, 5 could not be
separated from font corruption automatically, and 2 are scans without a text layer.

**The findings that would survive full retrieval are** the emptiness of the pre-launch cell, the
within-cell direction reversal by which parent, and the tempo-versus-quantum bound. Each rests on
records that are in hand, and additional retrieval can only add to a cell that currently has nothing
in it.

**The findings that might not survive are** the demographic-significance magnitude, which rests on a
single Vietnamese panel estimate transported to the United States, and the characterisation of the
identified evidence as being entirely about the wrong link. Three subscription-walled studies —
Chu, Laeven and Popov, and Kucheva — could each change that second finding, and Chu could change the
direction reported in §6.2.

**Numbers that come from abstracts rather than full text** are the direction of the Chu, Xie and Yu
result, the direction of the Laeven and Popov result, and the Acolin, Lin and Wachter share of the
co-residence rise. They are marked as such in the extraction table.

**One input to §7.3 is not from this chapter's corpus.** The fall in the American total fertility
rate is quoted from a standard series as a denominator for scale, and should be replaced with the
review's own population panel before publication.

**Verification that has not happened.** No second extractor has checked a sample of the extraction
table. The full-text screen and the title-abstract screen were done by the same reader, so the
consistency check between them is not independence. The GRADE ratings are one rater's, not three.
All three are acceptance criteria that remain open, and none of them is a formality: the Wall 1
reclassification in §5 moved two of the most-cited records in the packet out of the primary cell on
one reader's judgement.
