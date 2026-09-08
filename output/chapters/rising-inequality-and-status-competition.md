# C.2.f — Inequality and Status Competition in Child Investment

**Category:** Economic · **Primary mechanism:** rising income inequality raises the investment
required per child to hold a given relative position, making children more expensive and lowering
fertility. **Cross-references:** C.3.d (quantity–quality), C.6.a (Easterlin), D.2.d (intensive
parenting), C.1.a (income effect), C.5.a (uncertainty), C.2.b (direct costs), D.3.c (despair).
**Status:** TICK-081 · drafted 2026-09-08 · **not PI-reviewed** · written on 15 of 19 wanted full
texts (79%).

---

## 1. The claim

This chapter explores the effect of income inequality on the number of children people have.

### 1.1 In plain terms

In plain terms: when the gap between doing well and doing badly gets wider, parents feel they have to
spend more on each child just to keep that child in the running — more tutoring, more coaching, more
of everything — and once raising one child to that standard gets expensive enough, people have fewer
of them.

The distinctive part of this claim is not that children are expensive. It is that the expense comes
from *competition*. If every parent spends more, no child ends up better placed than before, because
what matters is rank: who gets the university place, not how much was spent getting there. Everyone
runs faster and nobody moves forward. That is why this is sometimes called an arms race, and it is
the reason the claim is not simply a restatement of "children cost money."

### 1.2 Technically

The parameter this chapter estimates is the change in completed fertility caused by an exogenous rise
in the dispersion of the income distribution facing prospective parents, operating through the
investment per child required to hold a given relative position, measured in children per woman.

Three clauses in that sentence do the work, and each corresponds to a boundary with a neighbouring
hypothesis. *Dispersion*, not own income, separates this from C.1.a. *Relative position*, not the
return to schooling, separates it from C.3.d. *The contemporaneous distribution*, not the parental
cohort's standard, separates it from C.6.a.

---

## 2. Theoretical mechanism

The mechanism is a **positional externality**. Suppose university places, or places at good schools,
are allocated by rank rather than by an absolute standard. Then a parent's spending on tutoring buys
their child a better position only by displacing someone else's child. Each family's spending is
privately rational and collectively self-cancelling: in equilibrium everyone spends more and the
allocation is unchanged. What has changed is the price of a child, which now includes whatever it
costs to stay in the race.

Rising inequality enters because it raises the stakes. When the gap between the top and bottom of the
distribution widens, the cost of slipping a rank rises, and the investment a parent will make to
avoid slipping rises with it.

**The identity/behaviour split.** There is no accounting identity here. Nothing forces fertility to
fall when inequality rises; the entire claim is behavioural, which means it can be wrong in a way
that a mechanical claim cannot.

**What would make the hypothesis wrong.** Three things, and all three turn out to be live:

1. **If inequality raised fertility rather than lowering it.** It is perfectly possible for a wider
   distribution to make people *less* ambitious for their children rather than more — to lower
   aspirations, cut the perceived cost of a child, and raise fertility. Two studies in this chapter
   find exactly that (§7).
2. **If the effect were really the return to schooling.** If parents invest more because education
   pays better, not because rank got dearer, this is C.3.d's mechanism wearing C.2.f's clothes. Only
   one study in the evidence base separates the two (§6).
3. **If the competition never intensified during the fertility decline.** The mechanism requires the
   race to have got fiercer while births fell. The most complete formal model of the mechanism
   concludes it did not (§8.3).

---

## 3. Search strategy

Reproducible from `source/build/goldset/335`–`341`; logs in `literature/search-logs/`.

The search was built as **six arms** rather than one query, because the mechanism's literature is
written in two vocabularies that share almost no terms: the economics-of-inequality vocabulary
(Gini, top shares, relative deprivation) and the East Asian education-competition vocabulary (shadow
education, private tutoring, cram school, "double reduction"). Calibrated against 35 resolved
anchors, the union reached **92% recall on the primary anchors** at a frame of 1,016 records.

**A scoping correction made mid-chapter, and it changed the result.** The scope's first pass probed
the mechanism's full chain — inequality → required investment → fertility — in economics-of-
inequality vocabulary and found **2 records**, and concluded the chapter should expect an empty
primary cell. The same chain in education-competition vocabulary returns **56**. The finding was a
vocabulary artefact, not an absence, and it was caught only because the query calibration failed
against controls that turned out not to contain the arm's own terms. Recorded as scope §4A.

### Walls, and their enforceability

| wall | rule | measured contamination |
|---|---|---|
| **C.3.d** quantity–quality | C.3.d owns the **return** to child quality; C.2.f owns the **reference standard**. | 8 |
| C.6.a Easterlin | C.6.a is relative income against the **parental cohort**; C.2.f against the **contemporaneous distribution**. | 15 |
| **C.1.a** income effect | C.1.a owns **own income**; C.2.f owns **position**. The largest wall. | 90 |
| C.5.a uncertainty | C.5.a owns individual **risk**; C.2.f owns cross-sectional **dispersion**. | 70 |
| D.2.d intensive parenting | D.2.d owns the **norm**; C.2.f owns the dispersion that moves the required level. | 3 |
| D.3.c despair | Kearney–Levine's teen-childbearing result is D.3.c's estimand. | 21 |
| gender-inequality homonym | "Inequality" meaning **gender** equity is D.2.a's. | 30 |
| direction of causation | Differential fertility *causing* inequality is context, not evidence. | 25 |

**Two walls were declared unenforceable at title/abstract in advance, and the declaration held.**
Whether a study separates the return from the reference standard (C.3.d), and whether it holds own
income fixed (C.1.a), are invisible in an abstract. They were carried as screen fields with `UNCLEAR`
as an explicit legitimate value, and resolved only at full text — where the first turned out to
decide the chapter (§6).

**One term was refused with its reason recorded.** *Involution* (Chinese *neijuan*), the popular name
for the competition this chapter is about, returns 398 records against the fertility axis and they
are the veterinary and obstetric homonym — uterine involution in dairy cattle, thymic involution in
pregnancy.

---

## 4. PRISMA flow

| stage | n |
|---|---|
| free seeds harvested from neighbouring chapters' pools | 393 |
| anchor candidates resolved | 35 / 35 |
| production query union frame (92% anchor recall) | 1,016 |
| screen universe after injecting anchors and seeds | **1,366** |
| — of which carrying no abstract | 313 (23%) |
| records screened | 330 |
| → primary cell | **19** |
| → boundary packet | 30 |
| → context | 32 |
| → excluded | 249 |
| primary records retrieved at full text | **15 / 19 (79%)** |
| extraction rows (15 records; one version pair) | 14 |
| **identified estimates surviving full text** | **2** |

**Three features of this funnel change how the chapter should be read.**

First, **the 19-to-2 collapse is the story.** Nine of the fifteen retrieved records changed cell or
status once read. The screen's own rubric warned that a `design` value read off an abstract is a
hypothesis; this chapter is what that warning costs.

Second, **the yield was in the small arms, not the big one.** A depth probe across the citation-ranked
universe returned 2 primary records in 150 (1.3%). Screening the two small arms exhaustively returned
18 in 134 (13.4%), against **0 in 67** decoys drawn from the rest. The 851-record `dispersion` arm —
83% of the frame — produced almost nothing.

Third, **23% of the universe has no abstract**, so those records were screened on title alone and are
flagged; the six primary records that were title-only are the ones most likely to be re-celled again.

---

## 5. The ideal design

### 5.1 The ideal estimand

The change in **completed cohort fertility** caused by an exogenous increase in the dispersion of the
income distribution in a prospective parent's reference group, holding own income and the return to
child human capital fixed, operating through the investment required to hold a given relative rank.

### 5.2 The design that would identify it

A policy that changes **how tightly rank determines allocation**, without changing either the return
to education or family income — and with fertility observed afterwards for long enough to distinguish
quantum from tempo. Concretely: a jurisdiction that replaces exam-ranked admission to selective
schooling with a lottery of the same capacity, compared against jurisdictions that do not, with
completed fertility followed for the affected cohorts. Such a design would move the reference standard
while holding the return fixed by construction, because a lottery does not change what education is
worth — only what it costs to secure.

**No such study exists.** The nearest real approximation is a ban on the *inputs* to the race rather
than a change in the allocation rule.

### 5.3 Distance from the ideal

| study | design | distance from ideal |
|---|---|---|
| C2F0428 tutoring ban | policy shock to required investment + DID on realized births | **closest**: moves required investment without moving the return, but changes inputs rather than the allocation rule, and the headline outcome is stated intention |
| C2F0592 Korea FE-IV | instrumented provincial spending → TFR | realized national outcome, but the exposure is expenditure and cannot separate return from standard |
| C2F1348 lottery model | calibrated structural model | estimates the *ideal* counterfactual exactly — but simulates it |
| C2F0357, Meng & Xie | IV on relative deprivation | exposure is a dispersion index that mixes own income with the distribution |
| C2F1264, C2F1217 | FE panels | associational; authors say so |
| C2F1327, C2F0593 | cross-sectional OLS | no identification |

---

## 6. Included studies

| id | study | design | outcome | direction |
|---|---|---|---|---|
| C2F0428 | Meng, Wang, Yang & Zhang (2025), China tutoring ban | within-subject experiment + city DID on **actual births** | intended **and realized** | **supports** |
| C2F0592 | Kim (2026), *J Pop Econ* | **FE-IV**, provincial | **realized TFR** | **supports** |
| C2F0357 | (2024), China | IV 2SLS on relative deprivation | intended | **against** |
| C2F1346/1212 | Meng & Xie (2026), version pair | IV, CFPS | realized | **against** |
| C2F1264 | Lee (2026), *Pop Space Place* | spatial panel FE + multilevel | realized | supports (associational) |
| C2F1217 | Xu & Wu (2025), proceedings | two-way FE | fertility gap | supports (associational) |
| C2F1327 | Lu, Wei & Fan (2026), *Demographic Research* | cross-sectional OLS | realized siblings | supports (association) |
| C2F0593 | Chen, Sun & Cui (2025), *China Soft Science* | OLS + mediation | intended | supports (association) |
| C2F1279 | Zhou, Shao & Zhang (2026), *Applied Economics* | IV + **calibrated simulation** | intended | supports (empirical arm only) |
| C2F1348 | Kim (2026), arXiv | **calibrated structural model** | simulated completed fertility | mixed |
| C2F1343 | Young (2026), CSU dissertation | PSM/AIPW on **spending** + model | no fertility outcome | link 1 only |
| C2F0066 | Johansson (1987), *PDR* | conceptual essay | — | supports conceptually |
| C2F0850 | Lee (2019), Korean | policy essay | — | supports rhetorically |
| C2F0259 | (2018), Iran | multilevel | intended | **re-routed to D.2.a** |

### Estimator disagreement, and it is not noise

Two studies find the effect and two find its opposite, and **they do not share an exposure.**

- The two that **support** measure required educational investment: a tutoring ban, and provincial
  shadow-education spending.
- The two that **run against** measure income inequality: an individual relative-deprivation index,
  and regional Gini with relative deprivation.

Before averaging anything, ask whether disagreeing studies share an estimator — here they do not even
share a treatment. Pooling them would produce a number describing no mechanism at all. **The ≥3 test
fails in every stratum, so this chapter is a narrative synthesis and not a meta-analysis.**

### Risk of bias

Nine studies assessed: **2 MODERATE, 7 HIGH**. One domain dominates everything else:

> **Separating the return from the reference standard is achieved in exactly one of nine studies.**

Only the tutoring ban clears it, and it clears it structurally: banning tutoring does not change what
education is worth, only what it costs to keep pace. Every other study measures spending or
dispersion, both of which move under C.3.d's mechanism just as readily as under C.2.f's.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

The competition story holds up where it has been tested directly, and the inequality story does not.

When someone measures the thing the theory is actually about — how much parents must spend to keep
their child in the race — the evidence lines up: China banned private tutoring in 2021, and in the
cities where the ban bit hardest, people said they wanted more children and somewhat more children
were actually born. Korea shows the same relationship running the other way: where families spend
more on tutoring, fewer babies arrive.

When someone instead measures income inequality itself, the relationship reverses. Two studies find
that people in more unequal places have *more* children, not fewer — and the reason they give is the
opposite of this chapter's: wider inequality made parents give up on the race rather than run
harder, and a child you are not trying to push to the top is a cheaper child.

Both things can be true at once, and that is the most useful thing this chapter has to say. Being
made to compete is expensive. Being surrounded by inequality does not reliably make you compete.

### 7.2 The estimate

**Supporting, identified:**

- **C2F0428** — China's 2021 tutoring ban raises expected total fertility by **7–8%**, larger where
  pre-policy tutoring density was higher. A difference-in-differences on **actual city birth rates**
  finds higher-intensity cities recorded significantly greater increases. The channel decomposition
  puts **perceived reduction in educational competition first**, ahead of parental health, and ahead
  of the money (−34.5%) and time (−18.1%) savings. That ordering is what makes the result C.2.f's
  rather than C.2.b's.
- **C2F0592** — a 1% rise in provincial shadow-education spending lowers Korea's **total fertility
  rate by 0.18–0.26%**, with larger effects at higher birth orders.

**Opposing, identified:**

- **C2F0357** — an increase in income inequality **raises** fertility intentions, robust to 2SLS,
  through channels the authors name as "build hopes on children" and **"put less value on children's
  education."**
- **Meng & Xie** — inequality **amplifies** fertility, mediated by educational aspirations that
  *fall* as inequality rises, cutting the anticipated cost of a child.

---

## 8. Demographic significance

The phenomenon to be explained is measured in children per woman; this mechanism offers a
percentage change in spending on tutoring.

That sentence sets the exchange rate the rest of this section has to establish, and it also names the
problem: nothing about a tutoring market is denominated in children until an elasticity converts it.
Two independent conversions are available, and a third route asks whether the exposure moved at all.

### 8.1 Pre-modern variation

For pre-modern variation, the verdict is **NOT ASSESSED**, because the registry scopes this
hypothesis to the SDT alone and no pre-modern cell was searched.

### 8.2 The First Demographic Transition

For the First Demographic Transition, the verdict is **NOT ASSESSED**, because the registry scopes
this hypothesis to the SDT alone; the FDT-era inequality-and-fertility literature is the
differential-fertility literature, which runs the causal arrow the other way and belongs to A.19 and
C.3.a.

### 8.3 The Second Demographic Transition

For the Second Demographic Transition, the verdict is **MINOR**, because two independent routes put
the education-competition mechanism at roughly an eighth of Korea's fertility decline, while the
registered exposure — income inequality — has the wrong sign in 8 of the 21 countries whose fertility
fell.

**Route 1 — did the exposure even move the right way?** Fertility fell in all 21 SDT-core countries.
The Gini trend **rises in 13 and falls in 8** (France, the Netherlands, Japan, Canada, Switzerland,
Portugal, Greece, Ireland). In 38% of the core, the thing this hypothesis names as the cause moved in
the wrong direction. On a long-run top-share series, a median **69%** of the SDT decline was already
complete before inequality turned upward — an upper bound, since a tempo correction cuts it to about
32% in the countries where that correction computes.

**Route 2 — the elasticity.** Korea's real private-education spending per student rose about 31%
between 2007 and 2023 while its TFR fell from 1.26 to 0.72. At C2F0592's elasticity, that spending
increase implies a TFR fall of 0.059–0.085 — **11% to 16%** of the observed decline.

**Route 3 — the counterfactual.** C2F1348 simulates that replacing score-based assignment with a
capacity-preserving lottery would raise completed fertility by 0.24 children per couple, which is
**12%** of Korea's post-1980 decline of 2.07.

**Routes 2 and 3 share no data and no method, and they converge on about an eighth.** That is the
carry-away number, and its scope is Korea.

**The most important qualification comes from the model that most supports the mechanism.** C2F1348
formalises the positional externality more completely than any other work in this chapter — and its
own cohort decomposition concludes that **preference shifts, not a fiercer race, explain the decline
across cohorts.** The mechanism is real, it is expensive, and on its strongest advocate's own
accounting it is not what drove the fall.

---

## 9. GRADE

| phenomenon | arm | rating | downgrades |
|---|---|---|---|
| PM | — | **No evidence** | out of registry scope; no cell searched |
| FDT | — | **No evidence** | out of registry scope; the FDT-era literature answers a different question |
| **SDT** | **required educational investment** | **LOW** | −1 imprecision (two identified estimates); −1 indirectness (both East Asian, one outcome is a stated intention) |
| **SDT** | **income inequality (as registered)** | **VERY LOW** | −1 risk of bias (all HIGH); −1 inconsistency (identified estimates split in sign); −1 indirectness (the exposure mixes own income with the distribution) |

**This chapter is rated on two arms, which is a departure from the template** and is flagged as a PI
call (§11). GRADE assumes one body of evidence per outcome. Here the body splits by *exposure*, the
two halves point in opposite directions, and a single rating would have to average a supported narrow
mechanism with a refuted broad one — which would misdescribe both.

A No evidence row names what would earn a rating: for PM and FDT, any study measuring positional
investment pressure against fertility before 1965.

---

## 10. Verdict

**Rising income inequality is not established as a cause of the Second Demographic Transition, and
the identified evidence on that exposure points the other way. What survives is narrower and better
supported: where competition for ranked school places raises the investment required per child,
fertility falls — and in Korea that mechanism is worth roughly an eighth of the decline.**

The distinction matters because the two are routinely treated as the same claim. They are not.
Measured as the dispersion of incomes, the mechanism reverses: two identified studies find people in
more unequal places have *more* children, because inequality lowered what they thought they had to
give each one. Measured as the investment required to stay in an educational race, it works: a
tutoring ban raised births, and higher tutoring spending lowers the total fertility rate.

The single number to carry away is **12%** — the share of Korea's post-1980 fertility decline that
removing the educational arms race entirely would recover, on two independent calculations that
agree. It is a real effect, it is not the largest thing in the room, and it has been demonstrated in
one part of the world.

The evidence base for all of this is **two identified studies**, and only **one of nine** studies in
the chapter can tell this mechanism apart from the quantity–quality tradeoff it sits next to.

---

## 11. Open questions

1. **Does C.2.f survive as its own hypothesis, or should the registry re-specify its exposure?** The
   registered claim names income inequality. The evidence supports required educational investment.
   These are different treatments, and the chapter currently answers a question the registry did not
   ask. **PI call.**
2. **Is a two-arm GRADE rating acceptable?** §9 departs from the template. **PI call.**
3. **Is the C.3.d boundary tenable at all**, given that eight of nine studies cannot separate the
   return from the reference standard? If it is not, C.2.f and C.3.d may need to be one chapter with
   two arms rather than two chapters. **PI call, and C.3.d is unstarted, so it is decidable now.**
4. **Retrieval priorities.** Four primary records outstanding: a ProQuest dissertation (Taiwan 1979,
   relative deprivation and fertility), a Springer chapter, a CNKI article, and one dead URL.
5. **Studies that do not exist and should.** The §5.2 design — a lottery replacing ranked admission,
   with completed fertility followed afterwards — has never been run. Korea's 1980 tutoring ban and
   its later lifting is the closest natural experiment in existence and **no study in this pool uses
   it**; every retrieved policy study uses China 2021.

---

## 12. References

Full bibliographic detail in `extraction/rising-inequality-and-status-competition-extraction.csv`.

---

## Provenance and standing caveats

This chapter is written on 15 of 19 wanted full texts (79%).

The findings that would survive full retrieval are the sign split between the two exposures and the
risk-of-bias result that only one study separates the return from the reference standard; the finding
that might not is the 12% carry-away, which rests on a single elasticity and a single calibrated
model, both from Korea.

**Numbers taken from abstracts rather than full text:** none in the primary cell; all 15 retrieved
records were read.

**Written over these objections.** (i) The two-arm GRADE rating in §9 is a departure from the
template and a reviewer may reject it. (ii) The 12% figure uses Korean private-education spending
growth that is **hand-entered from KOSIS** and not machine-read — it is the only unautomated number
in the computation and must be replaced before sign-off. (iii) Route 2 transports a *provincial*
elasticity to a *national* time series. (iv) The routing of C2F0259 out of the primary cell, on the
ground that "relative status of women" means gender status rather than position in the income
distribution, is a judgement made against that paper's own placement in the search results.

**GRADE was rated by one assessor, not three.** PROTOCOL requires three independent raters. One rater
arguing both sides surfaces contingencies but is not independence, and the requirement remains open.
