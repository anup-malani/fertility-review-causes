# Marriage Market and Assortative Mating

**Category:** Economic
**Primary mechanism:** The quality and compatibility of available partners affect whether people form unions, when they form them, and whether those unions produce children.
**Cross-references:** A.10 sex-ratio imbalance (which owns a raw shortage of men or women; this chapter owns partner *characteristics*) · A.7 age at marriage and marriage timing · female wage and opportunity cost of time · C.5.a economic uncertainty and labour-market insecurity · `compulsory-education-child-economic-value.md` · A.24 dating apps and union-formation friction (which owns search *technology*; this chapter owns pool *composition*).
**Status:** **Pre-evidence scaffold.** Rewritten against `docs/chapter-template.md` on 2026-08-29; previous scoping draft 2026-08-01. Hypothesis approval and OSF preregistration remain open. The production search, human screening, full-text extraction, risk-of-bias review, demographic scaling and GRADE panel **have not occurred**. Written on 0 of 0 wanted full texts — no full text has yet been requested.

> **How to read this chapter.** Sections 1–5 are complete and are the deliverable at this stage: they fix the claim, the estimand and the design the production search must look for. Sections 6–10 are empty, and empty is their correct state. Nothing in them should be read as a finding, and the 14 scoping candidates named in §6 are a map of where to look, not an included-study set.

---

## 1. The claim

This chapter explores the effect of the supply of suitable partners on fertility.

### 1.1 In plain terms

In plain terms: most people have children with someone else, so whether they can find that someone else affects how many children get born.

Imagine a woman who wants two children and also wants a partner with steady work and similar ideas about family life. Her city may have exactly as many men as women and still have very few men who fit. She can wait, lower her requirements, have a child on her own, or end up with fewer children than she wanted. Nobody moved away and the headcount never changed — but the set of people she would actually partner with got smaller.

The claim is that when that set shrinks, births fall. What makes it hard to check is that people adapt. They live together without marrying, they partner across educational lines they might once have avoided, they have children outside marriage. Each of those adjustments absorbs some of the effect, so a shortage of preferred partners might reduce births a great deal, or hardly at all, and looking at who ends up with whom cannot tell the difference.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in completed fertility, in births per woman, caused by a change in the supply of partners meeting a person's matching criteria, holding the raw sex ratio fixed, signed so that a negative value means fewer births.

The chapter is scoped to **FDT** (the First Demographic Transition, roughly 1870–1965) and **SDT** (the Second Demographic Transition, roughly 1965 onward). **PM** (pre-modern fertility variation, before roughly 1870) is out of scope in the registry.

**The boundary with the sex-ratio chapter is concrete, not a matter of emphasis.** One hundred men and one hundred women give a balanced headcount, and the partner market may still be unbalanced if many of the men lack the employment, education or other traits women seek, or if men and women disagree about how paid work and childcare should be divided. A raw headcount imbalance is A.10's. Composition is this chapter's.

**This is a behavioural parameter, and it is a mediated one.** The claim is a chain:

> partner-pool composition changes → union formation changes → fertility changes

**A study that establishes only the first two links has not estimated this chapter's parameter,** and §5 shows that most of the candidate literature stops there. The middle link is also where adaptation happens, so a design that observes union formation and stops will systematically overstate the fertility consequence.

**Margin.** The mechanism is predicted to act mainly on the extensive margin — whether a union forms and therefore whether any children are born — with a smaller intensive-margin effect through later starts. Because adaptation may convert a quantum effect into a tempo one, the estimand is specified on **completed** fertility.

---

## 2. Theoretical mechanism

In the reader's own vocabulary: this is a search-and-matching problem with a two-sided market and non-transferable elements. A partnership creates a surplus neither party can obtain alone — shared housing, mutual income insurance, division of paid and unpaid labour, joint child-rearing. Each person compares that surplus against the value of remaining single and searching on. A rise in the arrival rate of acceptable partners raises match formation; a fall in the acceptable share of the pool lowers it.

Three features make the fertility prediction less clean than the matching prediction.

**Reservation levels are endogenous.** If the acceptable pool shrinks, people can lower their standards. Matching theory predicts exactly this, and it means a compositional shock is partly absorbed before it reaches fertility. Educational hypogamy — partnering "downward" in schooling — is the observable form.

**Union form is substitutable for union existence.** Cohabitation and non-marital childbearing let births occur without the match the model treats as necessary. Where childbearing has decoupled from marriage, a marriage-market shock may move marriage a great deal and fertility very little.

**The shock is usually sex-specific and therefore hits both sides at once.** A collapse in young men's employment lowers women's pool of acceptable partners *and* lowers men's own income, which is C.5.a's mechanism. Separating them is the identification problem, not a refinement of it.

**What would make the hypothesis wrong.** It is wrong if compositional shocks that verifiably shrink the acceptable partner pool leave completed fertility unchanged — which is exactly what full adaptation through cohabitation, hypogamy and non-marital childbearing would produce. That is a live possibility rather than a formality, and no scoping candidate rules it out.

---

## 3. Search strategy

**The 2026-08-01 search was preparatory and its counts are not PRISMA counts.** Six routes were used: marriage-market theory; educational sorting; education-gap mismatch; partner economic prospects; gender-specific labour demand; and fertility observed by couple type. Queries joined `marriage market`, `marriageable men`, `assortative mating`, `educational hypogamy` and `partner mismatch` with `fertility`, `birth`, `parity` and `childlessness`, across AEA, NBER, IZA, *Demographic Research*, Springer and Oxford Academic.

| Wall | Rule | Enforceable at title/abstract? |
|---|---|---|
| **W1 Outcome** | The outcome must be a birth. Marriage, union formation or spouse type alone routes to the mechanism stream. | Yes |
| **W2 Treatment** | The variation must be in partner-pool **composition**, not raw sex ratio (A.10) and not search technology (A.24). | Partially |
| **W3 Exogeneity** | Comparing fertility across observed couple types is descriptive. An external event must have changed the match. | No — a design property |
| **W4 Channel** | A schooling reform routes to an education chapter unless the design identifies the pathway *through partner composition* rather than through wages, preferences, time in school or contraceptive knowledge. | **No — declared unenforceable in advance.** This is the wall that will decide the chapter, and it is invisible outside the specification. |

W4 is worth stating plainly now, before the production search: **any education-based instrument moves at least four channels, and this chapter owns one of them.** A design that cannot separate the matching pathway from the others is evidence for an education chapter, not this one.

---

## 4. PRISMA flow

| Stage | Records |
|---|---:|
| Preliminary scoping candidates mapped | 14 |
| Production records identified | **Pending** |
| Deduplicated records screened | **Pending** |
| Full texts assessed | **Pending** |
| Studies included in synthesis | **Pending** |

The one feature of this table worth stating is that it is empty by status rather than by finding. **No conclusion in this chapter rests on evidence, because no evidence has been screened.** The 14 candidates are the output of a preparatory scan intended to establish that the hypothesis is worth reviewing, and they are listed in `literature/search-logs/marriage-market-economics-scoping-candidates.csv` with an identifier, source link, evidence role and verification status.

---

## 5. The ideal design

This section is the chapter's actual deliverable at this stage. Every other chapter in the review writes it before reading the literature and then measures what exists against it; here there is no literature yet, so §5 is a **specification for the production search** rather than a yardstick applied after the fact.

### 5.1 The ideal estimand

The change in **completed fertility**, in births per woman observed at age 45, caused by an exogenous reduction in the supply of partners meeting prevailing matching criteria, **holding the raw sex ratio and the person's own economic circumstances fixed**, together with the changes in the intervening outcomes for the same cohort: singlehood, cohabitation, marriage, age at first birth, and non-marital births.

Three clauses carry the weight. *Holding the raw sex ratio fixed* is the boundary with A.10. *Holding own economic circumstances fixed* is the boundary with C.5.a, and it is the hard one, because the shocks that degrade a partner pool usually also degrade the incomes of the people searching in it. And *the intervening outcomes for the same cohort* is what distinguishes a fertility effect from an adaptation: without them, a null on births is uninterpretable — it could mean the shock did not bind, or that it bound and was absorbed.

### 5.2 The design that would identify it

**Source of variation.** A **sex-specific** shock to the economic characteristics that make a partner acceptable, hitting one side of a local marriage market and not the other, and not chosen by the people whose fertility is measured. Candidates: a trade or automation shock concentrated in male-dominated industries; a sex-asymmetric schooling expansion; a mass-incarceration change. The shock must be sex-specific, because a shock hitting both sides symmetrically changes incomes without changing relative pool composition.

**Comparison group.** People in local marriage markets not exposed, with the market boundary defined **before** the shock and defended — commuting zone, marriage market by age-education cell, or similar. Market definition is a first-order choice here, not a robustness check.

**Identifying assumption.** The shock is uncorrelated with local fertility determinants other than through partner composition. Falsifiable four ways: pre-trends in fertility and in union formation; a placebo on people already partnered before the shock, for whom the pool is irrelevant; a test that the *own-income* channel is small for the affected sex's counterparts; and an explicit check that the raw sex ratio did not move.

**Estimating equation.** An event study or shift-share IV on completed fertility, estimated on the same sample as a parallel set on singlehood, cohabitation, marriage and non-marital births, so that **the adaptation margins are measured rather than assumed**. The intervening outcomes are part of the estimand, not robustness.

**Data required.** Linked administrative or long-panel data with local labour-market exposure, partnership histories, and fertility to age 45. Horizon is the binding constraint: 20 to 25 years from exposure.

**Sample size.** Detecting 0.1 births per woman needs roughly 2,650 per arm; local-market designs with clustered exposure need far more, so administrative coverage is required.

**What the ideal design excludes.** Comparing fertility across observed couple types — the sorting-and-mismatch literature — which conditions on the match and therefore on an outcome of the treatment. And any schooling instrument that cannot separate matching from wages, preferences and contraceptive knowledge (W4).

### 5.3 Distance from the ideal — an advance assessment

No study can be scored, because none has been screened. What can be said is which of the three scoping streams could in principle reach the ideal, and this materially affects how the production search should be run.

| Scoping stream | Example candidates | Fertility outcome? | Sex-specific shock? | Adaptation margins? | Can it reach §5.1? |
|---|---|---|---|---|---|
| Gender-specific economic shocks | Schaller (2016); Kearney and Wilson (2018); Autor, Dorn and Hanson (2019) | Yes | **Yes** | Partly | **Yes — the only stream that can** |
| Schooling shocks with matching outcomes | Lavy and Zablotsky (2015); Geruso and Royer (2018) | Yes | Sometimes | No | Only if W4 is satisfied, which is rare |
| Sorting and mismatch | Schwartz and Mare (2005); Raymo and Iwasawa (2005); Lichter, Price and Swigert (2020) | **No** | No | Describes them | **No — conditions on the match** |

**Two of the three streams cannot answer this chapter's question however many papers they contain**, and the third is small. That is a prediction, made before screening, that the production search should be built to test: if the included set ends up dominated by sorting-and-mismatch studies, the chapter will have a large evidence base and an unidentified estimand.

**The scoping candidates already show the adaptation problem is real.** Autor, Dorn and Hanson find trade shocks reducing young men's relative employment reduce both marriage and fertility. Kearney and Wilson find the reverse shock — the fracking boom — raises births but **does not raise marriage**. Taken together those two results say the marriage channel is not the whole mechanism and may not be the main one, which is precisely why §5.1 requires the intervening outcomes rather than treating marriage as the pathway.

---

## 6. Included studies

**None.** No study is formally included; no full text has been assessed; no extraction, risk-of-bias coding or verification has been performed.

The 14 scoping candidates are mapped in §5.3 by evidence stream. That table ranks nothing and confirms nothing: full texts must first establish each candidate's treatment, outcome, estimate and mechanism claim. **A candidate map is not an evidence base**, and the three example studies named in §5.3 are cited there for what their *designs* imply about reachability, not for their results.

The naive-estimator analysis the template requires at §6.1 cannot be completed without the included set, but its shape is already visible and should be written into the screening rubric: the naive estimator here is **comparing fertility across observed couple types**, which conditions on the match — an outcome of the treatment — and therefore selects on the dependent variable. The entire sorting-and-mismatch stream is built on it. Its bias direction is not signed in advance, because who partners with whom under a shrinking pool depends on which margins adapt.

---

## 7. Quantitative synthesis

**None, and none is possible.** No pooled estimate is justified from scoping evidence, and none is attempted.

Were the candidate causal studies pooled today, they would combine trade competition, fracking booms and broader gender-specific labour demand, reporting total births, marital births, non-marital births and births in particular age ranges. Combining those coefficients would produce a precise-looking number with no stable interpretation — the failure this review exists to prevent.

The production extraction will test whether at least three independent studies share a treatment direction, outcome family, unit and usable standard error, **stratified by estimand class** as well as outcome family. If no comparable set exists, the chapter will report estimates side by side and say why they cannot be pooled.

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — the FDT is a fall of roughly three births per woman and the SDT roughly one and a half; this mechanism currently offers no estimate in any unit.

No demographic significance can be assessed. Doing so requires two quantities on compatible scales — a credible fertility response to a matching treatment, and the actual change in that treatment over the relevant population's fertility decline — and the chapter has neither. **The second is worth flagging now**, because it is a measurement problem the production search will not solve on its own: "the change in the supply of acceptable partners" has no standard series, and constructing one for a decomposition will be a substantive task in its own right.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is NOT ASSESSED, because the phenomenon is out of scope for this hypothesis in the registry rather than an empty in-scope cell.

Were it assessed, the expected sign would be negative — the European Marriage Pattern is in part a story about partner availability — but that mechanism currently sits in A.7.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is NOT ASSESSED, because no evidence has been screened; the cell is in scope, and its emptiness reflects work not yet done rather than a literature that was searched and found wanting.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NOT ASSESSED, on the same ground.

The SDT is where the scoping candidates concentrate — recent high-income settings — so this is the cell most likely to become assessable first. It is also the cell where adaptation is strongest, since childbearing has substantially decoupled from marriage in exactly these settings, so a large union-formation effect may coexist with a small fertility one.

---

## 9. GRADE rating

| Phenomenon | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM | **No evidence** | Out of scope in the registry. | NOT ASSESSED |
| FDT | **No evidence** | No body of evidence to rate: nothing screened, extracted or assessed. Not VERY LOW, which would wrongly describe a literature that had been examined and found weak. | NOT ASSESSED |
| SDT | **No evidence** | Same. | NOT ASSESSED |

The protocol requires full-text extraction, risk-of-bias assessment and three independent ratings before causal credibility can be judged. None has occurred.

---

## 10. Verdict

**No verdict.** This chapter has not been reviewed.

The hypothesis is worth reviewing, and the scoping search establishes that much: gender-specific economic shocks with fertility outcomes exist, are quasi-experimental, and disagree with each other in an informative way. Autor, Dorn and Hanson find that shocks reducing young men's relative employment reduce marriage and fertility together; Kearney and Wilson find that a shock raising young men's earnings raises births **without** raising marriage. That pair is the reason the review should happen and the reason it will be difficult: the marriage channel this hypothesis runs through is demonstrably not the only route from partner-market conditions to births.

**What would produce a verdict:** the production search and screen, then extraction against the estimand in §5.1. **What would produce a good verdict** is the design in §5.2 — a sex-specific shock to partner characteristics, a defended market definition, and completed fertility observed alongside singlehood, cohabitation, marriage and non-marital births for the same cohort.

---

## 11. Open questions

**PI calls required.**

1. **Hypothesis approval and OSF preregistration remain open.** The production search cannot begin until they close.
2. **Is a pre-evidence chapter the right artefact for `output/chapters/`?** This file conforms to the template on §§1–5 and is necessarily empty on §§6–10. It is useful — §5 specifies the search — but a reader encountering it in a directory of completed chapters may mistake a scaffold for a review. It may belong under `docs/` or a `scoping/` path until the production search runs.
3. **Confirm the A.10 and A.24 boundaries in the registry.** This chapter owns pool *composition*; A.10 owns the raw sex ratio; A.24 owns search *technology*. The three are easy to conflate at screening.
4. **How should the treatment be measured for a decomposition?** "The supply of acceptable partners" has no standard series (§8). This needs deciding before extraction, not after.

**Search and design priorities.**

5. Build the screening rubric around W4 now: an education-based instrument identifies this chapter's channel only if it separates matching from wages, preferences, time in school and contraceptive knowledge.
6. Test §5.3's prediction explicitly — that the sorting-and-mismatch stream, however large, cannot reach the estimand because it conditions on the match.
7. Require the adaptation margins in extraction. A null on births with no measurement of cohabitation and non-marital childbearing is uninterpretable.

**Studies that do not exist and should.** The design in §5.2 in full. The scoping candidates each have part of it: Autor, Dorn and Hanson have the sex-specific shock and the fertility outcome but not completed fertility; Kearney and Wilson have the adaptation evidence but the opposite shock. None has the whole sequence for one cohort.

---

## 12. References

References remain provisional until candidates pass production screening and enter `datastore/studies.json`. Verified identities and source links for the 14 scoping candidates are in `literature/search-logs/marriage-market-economics-scoping-candidates.csv`. Draft queries, inclusion rules and boundary decisions are in `literature/search-logs/marriage-market-economics-search-scope.md`.

---

## Provenance and standing caveats

This chapter is written on 0 of 0 wanted full texts — no full text has yet been requested, because the production search has not run.

**The finding that would survive full retrieval** is §5: the estimand, the design that would identify it, and the advance judgement that two of the three candidate evidence streams cannot reach it. Those are analytic and do not depend on which papers the search returns. **There are no other findings.** Sections 6 through 10 are empty by status, and every cell in §8 and §9 records work not yet done rather than evidence weighed.

**Objection over which this chapter was written.** None recorded. The chapter is, however, published into a directory of completed chapters while being a scaffold, and PI call 2 asks whether that is right.

**Numbers sourced from abstracts rather than full text.** All of them. Every characterisation of a scoping candidate in §5.3 and §10 comes from abstracts and titles; **no full text has been read**. The three studies named — Schaller, Kearney and Wilson, Autor, Dorn and Hanson — are cited for what their designs imply about reachability, and their results are reported as scoping impressions that extraction may overturn.

**Figures not derived from project data.** The FDT and SDT decline magnitudes in §8 are conventional and are not computed here.

**Generated inputs.** None. Nothing in this chapter is generated from an extraction table, because no extraction table exists.
