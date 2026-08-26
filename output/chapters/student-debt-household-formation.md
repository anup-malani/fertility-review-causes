# C.3.g — Student Debt and Household Formation

**Category:** Economic · Value of Children (C.3)
**Primary mechanism:** Education debt service during prime childbearing years consumes the household
cash flow that family formation requires, delaying or preventing marriage, homeownership and
childbearing.
**Cross-references:** C.3.e (credit constraints — distinct: this is a prior liability already spent,
not a limit on future borrowing) · C.2.c (housing costs) · A.23 (co-residence with parents) ·
A.7 (marriage timing) · C.3.d (quantity–quality, which owns the schooling channel this chapter must
hold fixed)
**Status:** INTERIM. Ticket TICK-073, drafted 2026-08-26. Not PI-reviewed. Written on **30 of 114
wanted full texts (26%)**, and — the number that matters more — on **1 of 4** identified direct-arm
records.

---

## 1. The claim

### 1.1 In plain terms

**In plain terms: a student loan is a lien on the first years of an adult's earnings, and family
formation is paid for out of the same account.**

The thought is ordinary. A graduate leaves university owing money. The repayment comes out of income
before rent, before saving for a deposit, before anything discretionary. Marriage, a house and a
child all need cash at roughly the same age, and the loan gets there first. If that is right, the
generation that borrowed most should form households latest, and the effect should scale with the
balance.

What makes the claim harder than it looks is that the people who borrow are the people who went to
university — and going to university lowers fertility on its own, for reasons that have nothing to
do with debt. Everything in this chapter turns on separating those two.

### 1.2 The claim precisely

**This chapter explores the effect of a young adult's own education debt on completed fertility.**

The registry (HYPOTHESES-v5 §C.3.g) states it as: *education debt service during prime childbearing
years reduces the effective household resources available for family formation — delaying or
blocking marriage, homeownership, and childbearing — in cohorts that came of age under the post-2000
student-debt regime.* Target phenomenon: **SDT only** (the Second Demographic Transition, the
post-1965 fall in rich-country fertility).

**The parameter this chapter estimates is the change in a woman's probability of a first birth
caused by an additional $1,000 of her own education debt, holding educational attainment fixed,
measured in percentage points per $1,000.**

The registry's wording bundles three outcomes, and they separate cleanly:

| | Exposure | Outcome | Who owns it |
|---|---|---|---|
| **Direct** | own education debt | births | **this chapter** |
| **Chain, link 1** | own education debt | marriage, homeownership, leaving home | this chapter |
| **Chain, link 2** | marriage, homeownership, leaving home | births | A.7, C.2.c, A.23 |

The chain is in scope because the registry names it. But link 2 is not this chapter's parameter to
estimate, and the chapter borrows it rather than pretending to measure it. That distinction does
more work here than in any chapter of this review so far, for a reason set out in §6.

Two boundaries, drawn on **whose balance sheet** the debt sits on. Parents borrowing for a child's
degree (Parent PLUS) sits on the older generation and cannot delay the borrower's own childbearing —
that is C.2.b's exposure. General consumer, mortgage and medical debt is C.3.e and C.2.c.

---

## 2. Theoretical mechanism

In the reader's vocabulary: student debt is a **negative endowment shock realised at labour-market
entry**, with a repayment schedule that is fixed in nominal terms and largely non-dischargeable. It
shifts the intertemporal budget constraint down over exactly the ages when the fixed costs of family
formation are paid. If children are a normal good and household formation has a lumpy entry cost — a
deposit, a wedding, a larger dwelling — a binding claim on early cash flow delays entry.

The mechanism is a **cost** channel, not a **value** channel. It does not claim children have become
less valuable; it claims they have become harder to afford at a particular age. That places it in
C.3 by the registry's filing but it behaves like C.2: it moves the price of entry, not the return.

**What would make the hypothesis wrong**, stated in advance:

1. **If the effect is attainment, not debt.** Borrowers are graduates. Graduates have fewer children.
   Any comparison that does not hold schooling fixed will find a debt "effect" that is the education
   effect wearing a different label.
2. **If other debts behave the same way.** A pure resource-constraint story predicts that any large
   liability at the same age delays family formation. If mortgage and credit-card debt instead run
   *with* childbearing, the mechanism is not simply about resources.
3. **If the effect is tempo, not quantum.** Delaying a first birth from 26 to 31 changes period
   fertility without changing completed families. The registry's claim is about the level of
   fertility, and a hazard model that stops observing people at 30 cannot tell the two apart.

All three turn out to be live, and (2) fails in the mechanism's own data.

---

## 3. Search strategy

Reproducible from `literature/search-logs/student-debt-household-formation-search-scope.md` and
scripts `199_`–`210_` in `source/build/goldset/`.

Two channels, deliberately vocabulary-independent. **Keyword:** student-anchored exposure terms
crossed with the union of fertility, union-formation and housing vocabulary — 401 records.
**Citation:** one hop out from 21 verified anchors, backward and forward — 2,071 records. The two
overlap by only 53 records, which is what makes a recall claim against the citation channel mean
anything.

**The exposure vocabulary is student-anchored on purpose, and it costs something.** A bare "debt
burden" reaches a 1,389-record sovereign-debt literature. Anchoring removes it — and also loses
records whose titles say only "Debt", including the most-cited work in the primary cell. Five
RELEVANT records carry no student-debt term at all. They arrived through the citation channel and by
hand, which is the argument for running both.

**Eight walls**, sized where the screen meets them: health-professions debt studied for career
choice (720 records at query level; **routed by outcome, not by topic** — a study of medical students
that reports childbearing is in); general household liabilities; default and repayment behaviour;
access-to-college effects; parents saving for a child's tuition; parent-held education debt; LMIC
school fees and child marriage (tagged, never deleted); and the reverse direction, childbearing as a
cause of debt.

**One wall was declared unenforceable in advance and the declaration was wrong.** Whether a study
holds educational attainment fixed is decided in a methods section, so the scope routed it to
full-text extraction. Measured, attainment-conditioning language appears in 28% of in-frame records
and the screener read it as present in 32% of relevant ones. It is a usable screen flag with a large
`cannot_tell` bucket, and the gate still lives at full text.

---

## 4. PRISMA flow

| Stage | n | |
|---|---|---|
| Keyword channel | 401 | of 400 reported |
| Citation channel (Tier B) | 2,071 | one hop from 21 anchors |
| Pool, deduplicated | 2,426 | 53 found by both channels; 8 anchors added by hand |
| After collapsing version duplicates | 2,249 | 177 collapsed |
| Screening worklist | 610 | score cut plus six bypasses |
| Screened | 610 | coverage asserted exact |
| RELEVANT / UNCERTAIN / NOT RELEVANT | 80 / 34 / 496 | |
| Forward to retrieval | 114 | |
| **Full text or abstract obtained** | **30** | **26%** |

Three features of this funnel change how the chapter should be read.

**The two channels barely overlap.** 53 records of 2,426. The citation channel is doing genuinely
independent work, which is why it was able to contradict a query-level finding (§10).

**8 anchors could not be reached by the production frame at all** — including Nau et al., the
most-cited work in the primary cell, whose OpenAlex record has no abstract and whose title says
"Debt" and "baby". Tier A entered the screen by hand.

**Retrieval is the binding constraint, and it is biased.** 26% overall is survivable. That the
missing records are the *identified* ones is not: the free retrieval rungs resolve to open sociology
journals, theses and repositories, while identified economics sits in SSRN, NBER and Cloudflare-
fronted journals. The bias runs in the same direction as the chapter's own asymmetry.

---

## 5. Included studies

Thirty records are in hand. Ten sit in the direct arm, three are the identified chain-arm studies,
and the rest are chain-arm associational work, mechanism evidence and uncertain records.

| Study | Design | Exposure | Outcome | Result |
|---|---|---|---|---|
| **Nau, Dwyer & Hodson 2015**, *RSSM* | Discrete-time hazard, NLSY97, women | student loan balance | annual probability of first birth | Predicted annual risk **4.3% at $0 → 2.8% at $50k → 2.5% at $60k**; ≈**1.2% lower per $1,000** among debtors |
| **Robb & Schreiber 2019**, SSRN | **IV: in-state tuition**, B&B 2008:12, four-year graduates | cumulative undergraduate loans | marriage; first birth | **−1.3% marriage per $1,000; first birth NOT SIGNIFICANT** |
| Hua 2024, SSRN | Calibrated heterogeneous-agent OLG model | federal loan availability | fertility, mobility | Loans reduce fertility — **by simulation** |
| Addo 2014, *Demography* | Competing-risks hazard, NLSY97 | education vs credit-card debt | cohabitation, marriage | Education debt → women **delay marriage, shift to cohabitation**; credit-card debt → **more** cohabitation |
| Bozick & Estacion 2014, *Demographic Research* | Event history, NLSY97 | loan repayment | marriage | Debt associated with delayed marriage for women |
| **Mezza, Ringo, Sherlund & Sommer 2019**, *JOLE* | **IV: in-state tuition**, credit-bureau panel | student loan balance | homeownership | **−1.8pp per $1,000** (public four-year) |
| **Goodman, Isen & Yannelis 2021**, *JFE* | **RD: 24th-birthday loan-limit discontinuity** | federal loan access | household formation | Liquidity affects early household formation |
| Dettling & Hsu (FEDS 2014 / *Labour Econ*) | Credit panel, fixed effects | debt burden, delinquency | parental co-residence | Debt portfolios predict **30%** of the rise in flows into co-residence |
| Houle & Warner 2017, *Sociology of Education* | Discrete-time event history, NLSY97 | student debt | returning to the parental home | **NOT associated in the full sample**; stronger for Black youth |
| Rohlfing et al. 2014, *Med Educ Online* | Cross-sectional survey, medical students | education debt | non-career life decisions | Debt reported as delaying family decisions |
| Kuperberg & Mazelis 2021, *Sociological Inquiry* | Survey, N=2,990 | student loans | **stated** norms | Half believe childbearing *should* be delayed with debt |
| Baek & Cho 2024, SSRN | COVID forbearance, 2022 SCF | debt relief | home purchase | +71% likelihood — an order of magnitude above the identified literature |

*(Full extraction table: `extraction/student-debt-household-formation-oa-status.json`. Twelve further
records — theses, simulations and uncertain items — are held and not yet extracted.)*

### 5.1 The estimator disagreement, and it is not a disagreement about magnitude

**The naive estimator in this literature compares borrowers with non-borrowers.** That comparison
conditions on going to university. Graduates have fewer children than non-graduates, earlier
education delays first birth mechanically through years spent enrolled, and the correlation between
attainment and borrowing is close to mechanical. **The bias runs in one direction: it makes debt look
more fertility-suppressing than it is**, because it charges the education effect to the loan.

Three of the strongest records handle it, and they do so differently. Robb & Schreiber restrict the
sample to four-year graduates, so attainment is fixed by construction. Nau et al. include education
indicators as controls, and report those controls behaving as expected — "higher education indicators
being associated with a delay in fertility" — which is the confound visible inside their own table.
Mezza et al. instrument the balance with in-state tuition changes, which moves debt without moving
the decision to enrol.

**But the disagreement that matters in this chapter is not between a biased and an unbiased estimate
of the same parameter. It is that the identified studies and the fertility outcome barely
intersect.** Two measurements, on two different frames, say the same thing. In the keyword frame,
**210 records name an identification strategy against 107 that carry a fertility outcome, and the
identified subset of the fertility cell is 2** — neither of which is an estimate. In the citation
neighbourhood, **5 records carry debt, a fertility outcome and an identification strategy together**.
And among the 80 records the screen called relevant, thirteen are identified — **nine of them in the
chain arm**. That is not heterogeneity to be pooled. It is a literature that has aimed its good
designs at a neighbouring question.

### 5.2 The mechanism fails a test in its own data

If the mechanism were a resource constraint — money owed now, less money for a family — then any
large liability at the same age should push the same way. Nau et al. test exactly this, and it does
not hold. In the same models, on the same women, **credit-card debt and home mortgages are
*positively* associated with the transition to motherhood** while student loans are negatively
associated. The authors call the first two "fellow travellers".

Two readings survive. The authors' own: student loans differ because their payoff is deferred, so
they signal a career investment not yet realised, while a mortgage signals a household already being
built. The sceptical reading: debt type is proxying for life-course orientation, and the student-loan
coefficient is picking up who postpones rather than what postponement costs. Neither reading is a
simple resource constraint, and the chapter should stop describing the mechanism as one.

---

## 6. Quantitative synthesis

### 6.1 The answer in plain terms

**The best-identified study that looks at both outcomes finds that student debt delays marriage and
does not detectably delay a first birth.**

Robb & Schreiber instrument loan balances with in-state tuition rates among four-year graduates.
Marriage: a $1,000 increase in cumulative undergraduate debt lowers the likelihood of marrying in
the first four years after college by about 1.3%. First birth: no significant effect. One team, one
instrument, one sample, two outcomes — and the effect appears on the outcome this chapter borrows and
not on the outcome it registers.

That is the chapter's central finding, and it is stronger evidence than any count of records, because
the two arms cannot be blamed on different data, different methods or different authors.

### 6.2 The estimate

**No pooled estimate is reported, and the reason is not thin data.** The direct arm contains one
identified estimate, which is a null; one hazard model reporting a strong association; one calibrated
simulation; and a set of stated-intention surveys. Pooling a null, an association and a model output
would manufacture a number that estimates nothing.

What can be stated:

- **The strongest published association, on realized first births.** Nau et al.: predicted annual
  probability of a first birth falls from **4.3% at zero student debt to 2.5% at $60,000** — a 42%
  relative reduction — among women in the NLSY97, observed to about age 30. The effect is
  concentrated at high balances; at moderate balances it is small. Among women with loans, **6% carry
  more than $60,000** by age 25.
- **The one identified estimate, on realized first births.** Robb & Schreiber: **not significant**,
  within four years of graduation.
- **The identified chain-arm estimates.** Mezza et al.: **−1.8 percentage points of homeownership per
  $1,000**. Dettling & Hsu: changing debt portfolios predict **30%** of the rise in flows into
  parental co-residence. Houle & Warner: **no association** with returning home in the full sample.
- **The stated-intention arm, held apart.** Kuperberg & Mazelis find nearly half of indebted students
  believe childbearing *should* be delayed. Robb & Schreiber's own subjective analysis has students
  naming debt as a reason for delay — in the same paper whose empirical analysis finds none. Stated
  and revealed diverge inside one study, on the same respondents.

**The bound on the null.** Robb & Schreiber observe four years after graduation, roughly ages 22–26.
Completed fertility is unobserved and postponement into the thirties is invisible by construction.
The null is a null about *early* first births. It should not be reported as "no effect on fertility",
and this chapter does not.

---

## 7. Demographic significance

**S4. The phenomenon to be explained is measured in completed children per woman; this mechanism
offers a percentage change in the annual probability of a first birth among people holding student
debt, observed to about age 30.**

Those units differ in three ways at once, and each gap flatters the mechanism: a first birth is not a
completed family; a hazard truncated at 30 cannot separate postponement from foregone children; and
an effect among borrowers is not an effect on a population. The arithmetic below crosses all three
gaps in the generous direction on purpose. A mechanism that is small when measured generously is
robust to the corrections not yet made.

All figures computed by `211_c3g_demographic_significance.py` from the World Bank US TFR series and
the published inputs named above.

### 7.1 Pre-modern

**For pre-modern variation, the verdict is NOT ASSESSED, because mass education debt did not exist.**
This is an absence of the exposure, not an absence of evidence.

### 7.2 First Demographic Transition

**For the FDT, the verdict is NOT ASSESSED, because mass education debt did not exist.** Had it
existed, the sign would be the same as in the SDT.

### 7.3 Second Demographic Transition

Two bounds, the first of which needs no effect size at all.

**Bound 1 — most of the decline predates the exposure.**

| | |
|---|---|
| US TFR 1965 | 2.913 |
| US TFR 2000 | 2.056 |
| US TFR 2024 | 1.627 |
| Total decline | **1.286 children** |
| Decline after 2000 | 0.429 children |
| **Share predating the exposure** | **66.6%** |

A mechanism restricted to post-2000 cohorts could explain at most a third of the US SDT decline even
if it explained the whole of its own era. (B.7 reached 67.6% by the same route; the arithmetic is
not chapter-specific, it is what a post-2000 exposure does against a 1965 baseline.)

**Bound 2 — the strongest association, applied generously.** Cumulating Nau's annual hazards over ten
years gives a first-birth probability of 35.6% at zero debt against 22.4% for the heaviest borrowers.
Multiplying that difference by the share of women exposed at each debt level, and treating a first
birth as a whole child:

| Scenario | Exposed share | Effect (children/woman) | Share of total decline |
|---|---|---|---|
| Heaviest borrowers (>$60k), 6% of borrowers | 40% | 0.0032 | 0.2% |
| Heavy borrowers (>$50k), 9% of borrowers | 40% | 0.0039 | 0.3% |
| **Every borrower at the >$50k effect** | **50%** | **0.0542** | **4.2%** |

**The largest figure the arithmetic supports is 4.2%, and it comes from the least defensible row** —
every borrower assigned the effect estimated for borrowers above $50,000, at the highest plausible
exposure. The defensible rows sit an order of magnitude lower.

**For the SDT, the verdict is NEGLIGIBLE, because the most generous arithmetic the strongest
published association supports reaches 4.2% of the decline, two-thirds of that decline predates the
exposure entirely, and the one identified estimate of the effect on births is a null.**

---

## 8. GRADE

Rated per phenomenon. The direct arm is rated; the chain arm is reported but does not carry the
rating, because it estimates a different parameter.

| Phenomenon | Starting level | Downgrades | **Final** |
|---|---|---|---|
| PM | — | exposure does not exist | **NOT ASSESSED** |
| FDT | — | exposure does not exist | **NOT ASSESSED** |
| **SDT** | LOW (observational body) | **−1 indirectness**: the identified evidence estimates marriage and homeownership, not births · **−1 imprecision**: one identified direct estimate, a null, on a four-year window · **−1 risk of bias**: the attainment confound is unhandled in most of the body and the mechanism fails its own cross-debt test | **VERY LOW** |

Certainty is low about the *size* of the effect. Certainty is considerably higher that the effect is
**not large**, which is a different statement and the one the verdict rests on: the units check and
the pre-2000 share bound the mechanism without needing the literature to be settled.

**One rater.** PROTOCOL §5 requires three independent GRADE raters. This is a single-rater assessment
and the requirement remains open.

---

## 9. Verdict

**Student debt is a real constraint on household formation and a negligible cause of the fertility
decline, and the same literature shows both.**

The identified evidence is good and it is about the wrong outcome. Debt reduces homeownership by
about 1.8 percentage points per $1,000 (Mezza et al.), predicts 30% of the rise in young adults
moving back in with parents (Dettling & Hsu), and lowers the probability of marrying by about 1.3%
per $1,000 (Robb & Schreiber). The same instrument, in the same paper, on the same sample, finds **no
significant effect on the birth of a first child**.

The one number to carry away: **4.2%**. That is the largest share of the post-1965 US fertility
decline this mechanism can account for under arithmetic built to flatter it, and the defensible
figure is nearer 0.3%. Two-thirds of the decline happened before the exposure existed.

The finding beneath the number is structural, and it is about the field rather than about debt.
**Four policy-variation studies sit in this frame — the 2020 federal loan moratorium, Teacher Loan
Forgiveness with a randomised trial, income-driven repayment discontinuities, and the COVID
forbearance — and every one of them measures employment, repayment or housing. Not one measures a
birth.** The instruments this hypothesis needs exist, have been built, and have been pointed
somewhere else.

---

## 10. Open questions

**PI calls carried from the scope, still open.**

1. **Does the chapter report the chain arm at all?** It does here, as a bound, never pooled with the
   direct arm, with link 2 explicitly borrowed from A.7 / A.23 / C.2.c.
2. **Cohort and period restriction.** The strongest records use NLSY97 cohorts borrowing at balances
   far below today's. Tagged by exposure era; not averaged across eras.
3. **What identification standard should the direct arm meet?** Not gated on it here; extracted as a
   field and carried into risk of bias.
4. **Non-US scope.** The rated parameter is US. The screen surfaced a **Korean-language literature**
   the scope had not counted — four records on debt, marriage and independence from parents — plus
   England, Japan and New Zealand. Income-contingent systems change the mechanism itself, not just
   the setting: a repayment that scales with income is a different constraint from a fixed one.
5. **The demographic-significance denominator.** Computed here over a range of exposed shares
   precisely because the exposure series was never retrieved; the verdict does not change across the
   range, so the missing series does not bind.

**The correction this chapter had to make twice, recorded because the sequence is the finding.**
The scope reported that no natural experiment in student debt with a fertility outcome exists
anywhere. The citation channel appeared to refute it with an SSRN preprint titled *Experimental
Evidence on … Family Formation Responses to Student Debt Forgiveness*. Retrieval refuted the
refutation: that paper is a **hypothetical vignette** — participants asked to *imagine* forgiveness
and report intended behaviour — and it is the working version of a record the query had already
found. The claim in its checked form: **no study in the frame estimates the effect of a debt-policy
change on realized fertility.** An empty-cell finding measured through one hand-written vocabulary
block is a claim about the block; this one has now been tested on two channels and a full abstract.

**Retrieval priorities, in order.** The three unretrieved identified direct-arm records — the
FAFSA-IV dissertation chapter, the tuition-IV *Debt burden after college*, and the Socius survey
experiment. Then the Korean-language records, which are the only non-Anglophone realized-fertility
evidence in the frame.

**The study that does not exist and should.** A first-birth and completed-fertility outcome attached
to any of the four policy shocks already exploited in this literature. The data are administrative,
the variation is already validated in published work, and the marginal cost is an outcome variable.

---

## 11. References

Addo, F. R. (2014). Debt, cohabitation, and marriage in young adulthood. *Demography* 51(5), 1677–1701.
Baek, H. Y., & Cho, D. (2024). Student loan relief and home purchase. SSRN 4846753.
Bozick, R., & Estacion, A. (2014). Do student loans delay marriage? *Demographic Research* 30(69), 1865–1891.
Dettling, L. J., & Hsu, J. W. (2014/2018). Returning to the nest. FEDS 2014-80; *Labour Economics*.
de Gayardon, A., Callender, C., & DesJardins, S. L. (2021). Does student loan debt structure young people's housing tenure? *Journal of Social Policy*.
Goodman, S., Isen, A., & Yannelis, C. (2021). A day late and a dollar short. *Journal of Financial Economics*.
Houle, J. N., & Warner, C. (2017). Into the red and back to the nest? *Sociology of Education* 90(1), 89–108.
Hua, Y. (2024). The long-run effects of federal student loans on fertility and social mobility. SSRN 4747952.
Kuperberg, A., & Mazelis, J. M. (2021). Social norms and expectations about student loans and family formation. *Sociological Inquiry*.
Mezza, A., Ringo, D., Sherlund, S., & Sommer, K. (2019). Student loans and homeownership. *Journal of Labor Economics* 37(1).
Nau, M., Dwyer, R. E., & Hodson, R. (2015). Can't afford a baby? Debt and young Americans. *Research in Social Stratification and Mobility* 42, 114–122.
Robb, C., & Schreiber, S. L. (2019). Married with children? The role of student loan debt. SSRN 3458547.
Rohlfing, J., et al. (2014). Medical student debt and major life choices other than specialty. *Medical Education Online* 19, 25603.
Rothstein, J., & Rouse, C. E. (2011). Constrained after college. *Journal of Public Economics* 95(1–2), 149–163.

---

## Provenance and standing caveats

**S6. This chapter is written on 30 of 114 wanted full texts (26%).**

**S7. The findings that would survive full retrieval are the units check, the 66.6% pre-exposure
share, and the structural finding that the identified designs measure marriage and housing rather
than births; the finding that might not is the direct arm's magnitude, which currently rests on one
hazard model and one abstract.**

**Numbers taken from abstracts rather than full text**, and flagged wherever used: Robb & Schreiber
(SSRN abstract — the central result of §6), Hua, Baek & Cho. Robb & Schreiber's full text is a
browser-job; its retrieval is the single highest-value outstanding item in this chapter.

**Retrieval is biased, not merely incomplete.** Zero of four identified direct-arm records were
retrieved automatically; three of nine identified chain-arm records were. The free rungs resolve to
open sociology journals and repositories while identified economics sits behind bot defence, so the
missing evidence is systematically the better-identified evidence. A reader should treat the direct
arm's magnitude as provisional in a specific direction: the records most likely to change it are the
ones not yet read.

**One rater on GRADE**; PROTOCOL §5 requires three. **Not PI-reviewed.**

**An objection this chapter was written over.** The registry's claim names marriage and homeownership
as the mechanism, so a reader may reasonably hold that evidence on those outcomes *is* evidence for
the claim. The chapter's position is that link 2 — from household formation to births — is a real and
largely unestimated parameter belonging to other chapters, and that a chain is only as strong as the
link nobody has measured. If the PI rules the other way, §6's verdict changes and §7's does not: the
units check and the pre-exposure share are untouched by which arm is credited.
