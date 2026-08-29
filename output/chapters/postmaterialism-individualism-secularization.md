# Postmaterialism, Individualism, and Secularization

**Category:** Cultural
**Primary mechanism:** As material security becomes assured and religious authority recedes, people come to value autonomy and self-expression over obligation and continuity, and want fewer children.
**Cross-references:** D.1.b exposure to an external modernity package (where the treatment is contact rather than the value held) · D.1.c prestige-biased transmission · D.2.a gender-role attitudes · D.2.b union deinstitutionalization · A.19 ancestral-culture persistence (which shares this chapter's best-identified design and is separated from it by proxy content) · D.3.b ecological dread (whose treatment is a fear rather than a value orientation).
**Status:** TICK-062. **PARTIAL — scope, search and methods only.** Rewritten against `docs/chapter-template.md` on 2026-08-29; previous draft 2026-08-05. §§6–9 are deliberately empty: the systematic screen is staged and has not been run, so no claim about what this literature contains or lacks can yet be made. Two of five rulings await PI sign-off, and one fixes GRADE ceilings before any study is read. Written on 0 of 0 wanted full texts — none has been requested.

> **How to read this chapter.** §§1–5 and §§10–12 are complete and are the deliverable at this stage. §§6–9 are blocked, and blocked is their correct state; §4 explains exactly why writing them now would corrupt the chapter's most valuable outputs.

---

## 1. The claim

This chapter explores the effect of secular and self-expression values on fertility.

### 1.1 In plain terms

In plain terms: people used to have children partly because that was simply what one did. Family, church and neighbours expected it, and not doing it took explaining. The claim is that this stopped being true — that as life got safer and richer and religion loosened its hold, people came to care more about making their own choices and less about doing what was expected, and that one of the choices they made was to have fewer children.

What makes this claim hard to check is not that it is vague. It is that nobody hands out values. A researcher cannot make one group of people more religious and another less and see what happens to their families. Values have to be measured by asking people, and the people who answer that they value independence are also, usually, richer, better educated, living in cities, and marrying later — all of which affect how many children they have for reasons that have nothing to do with what they value. Worse, values are usually measured *after* the children have or have not arrived, and having children changes what people value.

So the chapter's real task is narrower than it sounds. It is to find the handful of cases where something outside a person's own life moved their values, and then to see what happened to their families.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in completed fertility, in births per woman, caused by an exogenous shift toward secular and self-expression values, signed so that a negative value means fewer births.

The chapter is scoped to **FDT** (the First Demographic Transition, roughly 1870–1965, secularization stratum only) and **SDT** (the Second Demographic Transition, roughly 1965 onward). There is no **PM** (pre-modern) cell.

**This is not one hypothesis, and saying so is the chapter's first substantive act.** A hypothesis is a treatment × outcome pair; mediators do not define it and do not route a paper. Applying that rule dissolves D.1.a into **five distinct treatments against one outcome**:

| | Treatment | Status |
|---|---|---|
| **S1** | postmaterialist / self-expression / survival-values measures | large theory and measurement literature, very few fertility estimates |
| **S2** | individualism, autonomy, collectivism, kinship intensity | same |
| **S3** | religiosity, affiliation, attendance, salience, denomination | **the only stratum with a large individual-level literature and access to natural experiments** |
| **S4** | the childlessness norm | mostly degenerate — see below |
| **S5** | consumption orientation, material-values scales | very thin |

**These are never pooled**, search budget was not split evenly between them, and the standing recommendation is that the master list should **split D.1.a into separate hypotheses, beginning with S3**.

**Ruling 2 — the degenerate pair.** When the treatment measure and the outcome measure are the same construct, there is no pair. Regressing a person's childlessness on their own approval of childlessness estimates preference-outcome consistency, not a causal effect: it is one variable measured twice. This removes most of S4 from the causal pool. It was pre-registered, and independent confirmation arrived from an unexpected direction — a term-mining pass found that **every** childlessness term classifies as outcome vocabulary or as both, and none as a pure treatment word, because there is no S4 treatment word that is not also the outcome word.

**This is a behavioural parameter with no identity arm.** Nothing here holds by accounting.

**Margin.** Predicted to act on both margins, with the strongest theoretical claim on the extensive margin — whether to have children at all — which is precisely where S4's degeneracy bites hardest.

**The counterfactual** is a ceteris-paribus perturbation: hold income, education, urbanisation, prices and contraceptive access fixed, and shift the value orientation. §5 specifies the designs that could deliver it and §10 reports that three of the four best are unused.

---

## 2. Theoretical mechanism

In the reader's own vocabulary: this hypothesis moves the preference parameter rather than the budget set. Every other economic account of the fertility decline works through prices, income, or the technology of contraception; this one holds all three fixed and asserts that the indifference curves themselves changed. Inglehart supplies the mechanism for the shift — rising material security reweights priorities from survival toward self-expression — and Lesthaeghe supplies the institutional half, in which religious authority over family life weakens.

**The claim's ambition is also its difficulty, and it is worth being precise about why.** A preference shift is observationally equivalent to a price shift unless the analyst can hold prices fixed. Values move with the same modernization that moves everything else in the frame, and they are usually recorded after the fertility they are meant to explain. Those three problems — collinearity, endogeneity and timing — are not separable in aggregate data, which is why §5 insists on designs that break at least one of them from outside.

**Ruling 3 — the design ladder, and the most consequential decision in this chapter.** Admissible designs are ranked with GRADE ceilings fixed in advance. The consequential entry: **country-level value-index-versus-TFR co-movement sits at Tier 4 with no causal weight**, on three joint defects — roughly fifty units, a dozen collinear covariates with GDP among them, and countries that are not independent draws because values diffuse across borders. **That is the canonical SDT evidence base.** Excluding it from the causal pool is not an RA call; it is flagged for PI sign-off as a freeze condition, and a reader who rejects the ruling will reject every rating that follows.

**What would make the hypothesis wrong.** It is wrong if exogenous shifts in religiosity or self-expression values leave fertility unmoved; if the association disappears once income, education and urbanisation are held fixed; or if the arrow runs predominantly from parenthood to values rather than the reverse. §9 reports that the third is measured, not assumed, and is the binding threat.

---

## 3. Search strategy

Four channels, in the order run, reproducible from `source/build/goldset/` scripts `89_` through `113_`.

| Wall | Rule | Enforceable at title/abstract? |
|---|---|---|
| **W1 Pair identity** | Treatment must be one of S1–S5; the outcome must be fertility. | Partially — S1/S2 vocabulary is diffuse |
| **W2 Non-degeneracy** | Treatment and outcome must not be the same construct (Ruling 2). | Yes |
| **W3 Measured, not narrated** | A study identified off income, growth or unemployment with value change narrated only in the discussion has **income** as its treatment. The test is what is in the regression. | **No** — requires the specification |
| **W4 Not a moderator** | A value measure interacted with a policy or price identifies the *other* treatment's effect. Recorded as `VALUE_AS_MODERATOR`. | **No** — requires the specification |
| **W5 Proxy content (vs A.19)** | An ancestral *fertility rate* proxy tests persistence and routes to A.19; an ancestral *value measure* tests content and routes here. | **No** — Fernández and Fogli (2009) uses both and is bound never to route from its abstract |

**Channel 1 — existing syntheses — is empty for four of five pairs, and the emptiness is a finding.** `religion AND fertility` restricted to reviews returns **zero across all fields**; the only syntheses are two sub-Saharan-Africa regional ones. **Religion and fertility has been studied for a century and never systematically synthesised outside one region.** The pair expected to carry the chapter cannot be bootstrapped from external authority.

**Channel 2 — design-vocabulary probes.** Because S3 anchors surfaced by topic vocabulary were uniformly Tier 3 or 4, natural experiments had to be sought by *design* words rather than subject words. Twenty-four narrow probes returned **three credible Tier-1 candidates, all S3, all published since 2018**.

**Channel 3 — citation snowball**, seeded on works chosen for the specificity of their citation neighbourhood rather than fame. Hofstede 1980 and Schwartz 1992 both resolve and are deliberately *not* seeded, being canon for a *construct* rather than for this pair. Built off Crossref and Semantic Scholar rather than OpenAlex, so the Tier-B frame is orthogonal to Tier A in infrastructure as well as method — which makes Recall(B) a stronger test.

**Channel 4 — the clustered production query.** Six clusters: the five pairs plus a `GENERIC_VALUES` cluster of treatment-side vocabulary that retrieves on-pair work without naming a pair. **That sixth cluster carries more sole credit than the secularization cluster** — 176 gold papers no other cluster reaches — so a query built only from pair-specific vocabulary would have been an S3 query and would have lost roughly a third of the frame.

**Yield: 17,646 distinct records**, reduced to **15,586** by a deterministic pre-filter. Recall against the frozen gold set is **84.2%**, or **87.2%** after repairing gold rows whose stored title was an entire citation string.

### 3.1 The query was wrong once, and the correction is part of the record

The first production pull returned 17,281 records and a plausible 81.8% recall. It was missing **two of the chapter's three Tier-1 natural experiments**.

The cause: the query carried wildcard stems (`secular*`, `religio*`, `procreat*`), and OpenAlex rejects any request containing a star, so the pull stripped the star and sent the bare stem. That is safe only when the stem is itself a word. `childless` and `childlessness` resolve to one postings list, but **`procreat`, `nuptialit`, `childbear` and `postmaterialis` retrieve nothing at all** — twenty-four of forty-five wildcard terms were dead. Worse and invisible to any count-based audit, `secular` returns 34,326 records while failing to match *"Secularization"*, and `religio` returns 2,041 while failing to match *"Religiously"*.

Two things carry beyond the repair.

**The failure was one step from becoming a substantive claim about demography.** The childlessness-norm cluster earns almost no unique credit, and the standing question was whether it was buying coverage of a literature that does not exist. Eight of that cluster's nine wildcard terms were dead. **The stratum retrieved nothing because its terms were broken, not because the field is empty.**

**A high term count does not mean a term contributes anything.** OpenAlex stems `seculared`, `secularing` and `seculares` all back to `secular`, so each returns the same 34,326 records under a different spelling and each outranks the genuine `secularization` at 4,657. Selecting query variants by retrieval count filled every slot with noise and discarded the one derived form the repair existed to recover.

### 3.2 What the search cannot reach

**19 gold records appear not to be indexed by the provider at all** — a ceiling no query can pass. Book chapters, dissertations, regional and non-English journals: the sixth independent appearance of a non-Anglo-European indexing gap on this chapter, after an unregistered DOI at *African Journal of Reproductive Health*, two regional reviews absent from Semantic Scholar, Dutch-language Lesthaeghe and van de Kaa 1986, the Crossref backfill residue, and reviews of on-pair monographs surviving only as reviews.

A further **21 records are in the index and the query does not reach them** — addressable, worth perhaps five recall points.

**Language coverage is a live constraint, not a hypothetical.** Lesthaeghe's early work is partly Dutch and French, and a German-language postmaterialism-to-fertility study from 1990 is among the few S1 estimates that exist. An English-only query would systematically drop exactly the FDT-era material Ruling 4 was written to admit.

---

## 4. PRISMA flow — incomplete, and why that blocks §§6–9

| Stage | Records | Status |
|---|---:|---|
| Records identified (channel 4, union across six clusters) | 17,646 | complete |
| Cross-cluster overlap collapsed by deduplication | 6,698 | complete |
| Removed by deterministic pre-filter (clinical, veterinary, agronomic, book reviews) | 1,855 | complete |
| Routed to book-review retrieval worklist | 205 | complete, not chased |
| **Entering blinded title/abstract screen** | **15,586** | **staged, not run** |
| After title/abstract screen | — | **blocked** |
| Full text retrieved | — | blocked |
| Included in synthesis | — | blocked |

**Nothing downstream of the screen can be written, and the reason is not merely that numbers are missing.** This chapter's most valuable outputs are claims about *absence* — that Tier 1 is three studies, that whole design families are unused, that S1 can be reported but not rated. **An absence claim made against a citation frame and then contradicted by a systematic screen is not updated; it is retracted.** The frame is a snowball from nine framework statements and eighty-two on-pair papers, which tilts toward the well-cited Anglo-European SDT core — precisely where this chapter is weakest. Writing §§6–9 from it now would bake that tilt into the synthesis and leave §12 understating the limitation, because the quantity that measures it — what the systematic search adds beyond the citation frame — would never have been observed.

### 4.1 What the full screen would add, estimated from 400 records

A uniform random sample of **400 of the 15,586** was screened under the frozen rubric (`113_d1a_yield_sample.py`). The sample is random by construction: records are shuffled under a fixed seed before batching, so the first ten batches are a random 400 rather than the first 400 of anything.

| | sample | rate | 95% CI (Wilson) | projected to 15,586 |
|---|---|---|---|---|
| `RELEVANT` | 20/400 | **5.0%** | 3.3–7.6% | **≈780** (508–1,184) |
| assigned a primary, poolable cell | 26/400 | 6.5% | 4.5–9.3% | ≈1,010 |
| `UNCERTAIN` → a full-text read | 49/400 | 12.3% | 9.4–15.9% | ≈1,910 |
| `NOT_RELEVANT` | 331/400 | 82.8% | | |

**The count settles whether to run the screen — it would add several hundred studies, so no claim about the size of this literature can be made without it. But the composition qualifies which absence claims were ever at risk, and that is the more interesting result.**

**Not one record in the sample was guessed above Tier 3.** Of twenty `RELEVANT` records, sixteen were Tier 3 and four Tier 4; **zero Tier 1 and zero Tier 2**. The screen would add volume without adding credibility. The chapter's claims about *identified* evidence — that Tier 1 is three studies, that blue-law, Sunday-trading and clergy-scandal designs are unused, that state atheism was never used to identify a fertility effect — are not the claims this sample threatens. The claim at risk is the weaker, more ordinary one about how much has been *studied*.

The distribution also reproduces the shape predicted from the anchor set, the best available evidence that the screen is calibrated rather than merely productive: **S3 supplies 19 of the 26 primary-cell records**, against 2 for S1, 1 for S2 and 1 for S5 — close to the 23/5/1/2 split of the hand-built anchors. And `GENERIC_VALUES` is the single largest source of kept records (42).

**One expectation was not met.** The rubric anticipated `AGGREGATE_COMOVEMENT` — country-level value index against TFR — would be common. It appears once in 400. The likely reason is that a title and abstract rarely reveal that the unit of analysis is the country, so these route to `UNCERTAIN` rather than to their cell. Recorded as an open discrepancy, not a finding.

**The binding constraint is downstream of the screen, not the screen itself.** ~1,910 `UNCERTAIN` records is ~1,910 full-text retrievals, and sibling chapters are already retrieval-bound. Screening is about a day of unattended compute; the reads it generates are the real budget.

---

## 5. The ideal design

Written before the literature was read — which here is literal, since the screen has not run. This section is a **specification for what the screen should be looking for**, and §10 reports that the three best instances of it appear not to exist.

### 5.1 The ideal estimand

The change in **completed fertility**, in births per woman at age 45, caused by an exogenous reduction in religiosity — measured as attendance, salience or affiliation — among adults of childbearing age, holding income, education, urbanisation and contraceptive access fixed.

The estimand is written for **S3** deliberately. S3 is the only stratum with both a large individual-level literature and access to natural experiments; S1, S2 and S5 have no instrument in prospect, and §10 records that S1 is not empty of estimates, only of identified ones. A single estimand for "value change" would be unbuildable, which is the concrete form of the argument in §1.2 that this is five hypotheses.

### 5.2 The design that would identify it

**Source of variation.** An institutional shock to religious practice that is not itself a response to family formation. Four design families qualify, and naming them is the point of this section:

- **Blue laws and Sunday-trading restrictions.** Repeal changes the opportunity cost of attendance without touching prices facing families. The Gruber–Hungerman design.
- **Clergy-scandal shocks.** A locally timed collapse in religious authority, plausibly unrelated to local fertility trends.
- **State atheism campaigns.** The Soviet and Albanian campaigns are the largest deliberate secularization shocks in recorded history.
- **Religious-leader interventions**, where content is assigned rather than chosen.

**Comparison group.** Populations in adjacent jurisdictions or cohorts not exposed, with religiosity measured **before** the shock.

**Identifying assumption.** The shock moved religiosity and did not independently move income, marriage-market conditions or contraceptive access. Falsifiable: a **first stage on religiosity itself** — the shock must be shown to have moved the treatment, which distinguishes these designs from every Tier-3 study in the field; pre-trends in fertility; and placebo outcomes.

**Estimating equation.** A difference-in-differences or event study on completed fertility with the religiosity first stage reported alongside, plus the **reverse-arrow test**: whether the shock's timing relative to family formation matters.

**Data required.** Administrative or long-panel fertility linked to a pre-shock religiosity measure, with a horizon reaching completed fertility — 20 years or more.

**Sample size.** Detecting 0.1 births per woman needs roughly 2,650 per arm; jurisdiction-level shocks with clustered exposure need far more.

**What the ideal design excludes**, by Ruling 3: country-level value-index-versus-TFR co-movement, at Tier 4 with no causal weight. And by W4: a value measure *interacted* with a policy, which identifies the policy's effect. A difference-in-differences on a 1982 Baltic maternity-benefits expansion, comparing women who did and did not grow up in religious households, estimates the effect of the benefit — religiosity was never moved.

### 5.3 Distance from the ideal — an advance assessment

No study can be scored, because none has been screened. What the design probe already establishes is which of the four design families has ever been used:

| Design family | Applied to religiosity? | Applied to **fertility**? | Distance |
|---|---|---|---|
| Blue laws / Sunday trading | **Yes** — and then to drinking, drug use and crime | **Zero** | The design exists, transported everywhere except here |
| Clergy scandals | Yes | **Zero** | Same |
| State atheism campaigns | Five hits | **None with a fertility outcome** | The largest secularization shocks in history, never used |
| Religious-leader intervention | Yes | **One** — Georgia, *Journal of Population Economics* 2025 | **The closest thing to the ideal design that exists** |

**Three Tier-1 candidates exist and all three are S3, all published since 2018:** political-party variation in Turkey (*American Journal of Sociology* 2018), declining church membership in Finland (*Social Science Research* 2026), and the Georgian religious-leader intervention. **If the eventual pool sustains that count, the chapter's headline is that a century-old literature contains three studies that identify anything, and that all of them concern religion.**

These are provisional: they rest on targeted probes rather than the completed screen, and the screen may yet find one more. That is exactly why the screen must run before §§6–9 are written.

---

## 6. Included studies

**Blocked pending the screen.** See §4.

The naive-estimator analysis the template requires here can nonetheless be stated in advance, because it is a property of the field rather than of the included set. **The naive estimator is a cross-sectional regression of fertility on a survey value measure.** It is confounded three ways at once, all running the same direction: income, education and urbanisation each predict both secular values and low fertility. It is additionally contaminated by reverse causation (§9) and by measurement timing, since the value is usually recorded after the fertility. **Every bias runs toward the hypothesis**, and Ruling 3's Tier 4 exists to keep the resulting estimates out of the causal pool.

---

## 7. Quantitative synthesis

**Blocked pending the screen.** Two constraints on the eventual synthesis are already known and recorded now so they are not discovered late.

**Estimates are not independent draws.** Much of this literature runs on a handful of survey instruments — WVS/EVS, ESS, GSS, DHS. Twenty papers on overlapping waves and countries are not twenty independent estimates. `DATA_SOURCE` is a required extraction tag and a clustering variable in any pooled analysis.

**Signs must be oriented before pooling.** S3 is almost always coded toward religiosity while S1 and S2 are coded toward self-expression. Mixing flipped and unflipped estimates is a mechanical route to a null. Every effect is oriented toward the secular/postmaterialist pole at extraction (Ruling 5).

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — the FDT is a fall of roughly three births per woman and the SDT roughly one and a half; this mechanism currently offers no estimate in any unit, because the screen that would produce one has not been run.

**Blocked pending the screen — and additionally exposed to a defect in the deliverable format that is larger than this chapter.**

D.1.a is a root cause whose causal pathway runs through four or five separately credited chapters — contraceptive diffusion, education, women's employment, union deinstitutionalization, child quality. Three of them name D.1.a as their root cause in their own notes. **If each proximate chapter claims its share of one fertility decline and D.1.a claims the reduced form, the shares sum past 100% and the per-hypothesis verdict format breaks where a reader adds it up.**

This is worth stating precisely against `PROTOCOL.md` §4.2.1, which was added to fix a different denominator problem. §4.2.1 makes each chapter's share well defined *within* itself: a change, over the phenomenon's full window, in shared units, with the denominator named. **It does not stop two chapters from claiming the same births.** A root cause and its proximate channels can each satisfy §4.2.1 exactly and still double-count, because the rule governs the denominator and the double-counting is in the numerators. This is escalated as a defect in the review's output format rather than resolved here.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is NOT ASSESSED, because the phenomenon is out of scope for this hypothesis in the registry rather than an empty in-scope cell.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is NOT ASSESSED, because the cell is in scope and the screen that would populate it has not been run; its emptiness reflects work not yet done rather than a literature searched and found wanting.

Ruling 4 admits FDT-era evidence, so this cell is live rather than nominal: the Princeton European Fertility Project's secularization work is measurement of the S3 construct applied to the first transition, and the S3 stratum therefore spans two target phenomena rather than one.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NOT ASSESSED, on the same ground.

One thing about this cell is already fixed and should be read before any future number: **Ruling 3 excludes the canonical SDT evidence base from the causal pool.** Country-level value-index-versus-TFR co-movement is what most readers have in mind when they think this hypothesis is well supported, and it sits at Tier 4 with no causal weight. Whatever share this cell eventually carries will be computed from a much smaller and much better-identified body of evidence than the field's own impression of itself.

---

## 9. GRADE rating

| Phenomenon | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM | **No evidence** | Out of scope in the registry. | NOT ASSESSED |
| FDT | **No evidence** | No body of evidence to rate: the screen is staged and unrun, and nothing has been extracted. Not VERY LOW, which would describe a literature examined and found weak. | NOT ASSESSED |
| SDT | **No evidence** | Same. | NOT ASSESSED |

**Ruling 3 fixes GRADE ceilings before any study is read**, which is unusual and deliberate: Tier 4 designs cannot exceed VERY LOW however many of them exist. The ruling is unsigned, and a PI who rejects it changes every rating this chapter will ever carry.

**Four risk-of-bias domains bind, in roughly this order of severity**, and they are recorded now because they shape extraction rather than follow it.

**Reverse causation is the binding threat, and it is measured rather than assumed.** Parenthood plausibly increases religiosity as much as religiosity increases parenthood. One study sizes the arrow directly: using the British Household Panel Survey, *"Does forming a nuclear family increase religiosity?"* (*European Sociological Review* 2022) asks how entering cohabitation, marriage, and first and second births affect religious salience, attendance and organizational activity. It carries no effect estimate for this pair and belongs here rather than in a context list, because it is the best available measurement of the domain that most limits every S3 estimate.

**Selection on the measure's timing.** A value recorded after the outcome cannot support a causal reading. `PRIMARY_VALUE_EX_ANTE` exists as a separate estimand cell precisely to isolate studies that recorded the value orientation on childless respondents *before* the fertility outcome.

**Measured versus narrated treatment (W3).** The test is what is in the regression, not what is in the framing.

**The moderator boundary (W4).** `VALUE_AS_MODERATOR` estimates are genuinely informative that values condition responsiveness to other treatments, and are not causal estimates of value on fertility.

---

## 10. Verdict

**No verdict.** This chapter has not been synthesised, and the screen that would allow it is staged and unrun.

What the chapter can already say is worth more than a premature rating, and it is mostly about what is absent.

**The one number to carry away: three.** That is the number of Tier-1 studies the design probe located — all S3, all published since 2018: political-party variation in Turkey, declining church membership in Finland, and a religious-leader intervention in Georgia. If the screen sustains that count, a century-old literature contains three studies that identify anything, and all three concern religion rather than values in general.

Three qualifications belong inside this.

**The empty design families are the most actionable output.** Blue laws, clergy scandals and state atheism campaigns have all been used to study religiosity — and, in the blue-law case, drinking, drug use and crime — and never fertility. Each is a specific, checkable gap with an existing design ready to be transported.

**The canonical evidence base is excluded from the causal pool** by Ruling 3, which is unsigned. A reader who disagrees with that ruling disagrees with every rating this chapter will carry.

**This is five hypotheses wearing one name**, and the recommendation on record is to split it, beginning with S3.

**What would produce a verdict:** run the staged screen, then absorb the ~1,910 full-text reads it generates. **What would produce a good verdict** is any one of the three unused design families in §5.2 applied to a fertility outcome.

---

## 11. Open questions

**PI calls required.**

1. **Ruling 3 — excluding country-level value-index-versus-TFR co-movement from the causal pool.** The single most consequential decision in the chapter, and not an RA call. It fixes GRADE ceilings before any study is read.
2. **Ruling 4 and the remaining unsigned ruling.** The scope is DRAFT until both are signed.
3. **Should D.1.a be split into separate hypotheses, beginning with S3?** §1.2 argues it is five treatment × outcome pairs; the search budget was already not split evenly between them.
4. **The shares-sum-past-100% defect (§8).** A root cause and its proximate channels can each satisfy `PROTOCOL.md` §4.2.1 and still double-count the same births. This is a review-format defect, escalated rather than resolved here.

**Search and screening priorities.**

5. **Run the staged screen.** Everything downstream is blocked on it, and §4.1 establishes it would add several hundred studies without adding credibility above Tier 3.
6. Budget the ~1,910 full-text reads the screen generates. That, not the screen, is the constraint.
7. A third query round is worth perhaps five recall points on the 21 in-index records the query does not reach.
8. Chase the 205 book reviews on the retrieval worklist, and address language coverage — an English-only query drops exactly the FDT-era material Ruling 4 admits.
9. Read the explicit empirical horse-race between the competing accounts (*Population and Development Review* 2022). **S1 is not empty of estimates, only of identified ones**, and that refinement matters: "no evidence exists" and "no identified evidence exists" are different chapters.

**Studies that do not exist and should.** The three unused design families in §5.3, applied to completed fertility with a religiosity first stage: blue-law repeal, clergy scandal, and state atheism campaigns.

---

## 12. References

Deferred until the included-studies table exists. Works named in this draft are anchors and context — Lesthaeghe (1983); van de Kaa (1987); Lesthaeghe and Surkyn (1988); Inglehart and Baker (2000); Norris and Inglehart (2004); Fernández and Fogli (2009); Zaidi and Morgan (2017) — and their appearance is not a claim that they are included studies.

---

## Provenance and standing caveats

This chapter is written on 0 of 0 wanted full texts — none has been requested, because the screen that would identify them has not been run. The screen is projected to generate **≈1,910** full-text reads.

**The findings that would survive the screen** are the ones §4.1 was run to test: that Tier 1 is three studies, that three design families are unused, and that S1 has estimates but no identified ones. The 400-record sample returned zero Tier-1 and zero Tier-2 records, so the screen is expected to add volume without adding credibility. **The finding that would not survive** is any claim about how much has been *studied* — that is the ordinary claim the sample shows is at risk, and it is why §§6–9 are blocked rather than drafted from the citation frame.

**Objection over which this chapter was written.** None recorded from the PI, and two rulings await sign-off — including Ruling 3, which fixes GRADE ceilings before any study is read.

**Numbers sourced from abstracts rather than full text.** All Tier-1 candidate characterisations in §5.3 and §10 come from design probes over titles and abstracts. **No full text has been read.**

**Figures not derived from project data.** The FDT and SDT decline magnitudes in §8 are conventional and not computed here.

**Limitations, carried forward.** Geographic and language skew, with six independent confirmations and a measured floor of 19 gold records outside the searched index. The canonical SDT evidence base excluded by an unsigned ruling. Most of S4 degenerate under Ruling 2 and reported descriptively. Estimates clustered on a few survey instruments and not independent. The shares that do not add up across proximate chapters. And a scope that remains DRAFT.

**Generated inputs.** Search, screening and sampling artifacts are reproducible from `source/build/goldset/89_` through `113_`, with run order binding at two points: `98_` before `99_`, and `106_` before `103_ --query v2`. Artifacts in `literature/search-logs/postmaterialism-individualism-secularization-*`.
