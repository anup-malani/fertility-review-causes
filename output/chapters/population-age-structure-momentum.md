# Population Age Structure and Demographic Momentum

**Category:** Proximate cause (A.9) — demographic accounting
**Primary mechanism:** Shifts in the age composition of the population move the crude birth rate and the number of births independently of any change in age-specific fertility, because a birth rate is a ratio whose generating population (women of childbearing age) changes size and shape over time.
**Cross-references:** A.11 tempo effects (the other period-measurement artifact; timing not composition); A.1 child-mortality decline (builds the momentum-laden age structure); A.10 sex-ratio (aggregate-birth outcomes without composition adjustment route here).
**Status:** TICK-089 · drafted 2026-09-20 · **not yet PI-reviewed** · written on 10 of 16 included studies (63%). GRADE band and demographic-significance reporting apply the 2026-09-20 rulings recorded in TICK-080 (items 5–7, 10), pending that ticket's formal PROTOCOL amendment and Anup's sign-off.

---

## 1. The claim

**This chapter explores the effect of population age structure — the age composition of the population, and the demographic momentum it carries — on the crude birth rate and the number of births.**

**1.1** In plain terms: how many babies a country records in a year depends not only on how many children the average woman has, but on how many women there are of the age to have them. When a country has an unusually large group of young adults — often the grown-up children of an earlier high-birth era — it records a great many births even if each woman is having only a few children. When that group shrinks or grows old, births fall even though nothing has changed about how many children women actually want or have. The claim of this chapter is that a large part of the rise and fall of the *number of births* — and of the **crude birth rate** (CBR: annual births divided by total population) — can come from this changing age make-up alone, with individual childbearing held completely fixed.

**1.2** Technically, the claim is an accounting identity plus its dynamic consequence. The CBR is the sum, over age, of age-specific fertility rates weighted by the share of the population in each age group. Holding the age-specific rates fixed, the CBR still moves whenever the age weights move. **Demographic momentum** (the tendency of a population to keep growing, or of its births to keep changing, for decades after age-specific rates reach the replacement level) is the same fact carried forward in time: a young age structure is the legacy of past high fertility, and it keeps births elevated long after fertility per woman has fallen. The parameter of interest is a *share*: of an observed change in the CBR or the birth count, how much is attributable to the age-composition component versus the age-specific-rate component.

## 2. Theoretical mechanism

In the reader's terms, this is a composition effect, not a behavioural response. Write the birth count as `B = Σ_a f_a · W_a`, where `f_a` is the age-specific fertility rate at age `a` (a behavioural object — how many children women of that age have) and `W_a` is the number of women at that age (a stock, inherited from history). A change in `B` between two dates decomposes into a part driven by the `f_a` (the **quantum** and timing of childbearing) and a part driven by the `W_a` (the age composition). A.9 is the claim that the second part is large.

**The identity/behaviour split is the whole chapter.** The decomposition is an identity: it cannot be false, and it needs no study to establish that composition *can* move the CBR. The only thing a study adds is the *magnitude* of the composition part in a particular place and period — a tabulation, not an estimated effect. There is no counterfactual treatment being applied to anyone; the "effect of age structure" is an attribution of an accounting share, not a `ceteris paribus` perturbation of a policy or price. This matters for GRADE (§9): the evidence is arithmetic, and cannot be "well-" or "badly-identified" in the causal sense the review's GRADE ladder measures.

**Margin.** The mechanism is intensive on a *period, per-capita* measure (it moves the level of the CBR) and, by construction, contributes nothing on the *completed-cohort* measure — a real cohort's total children are a property of that cohort's own `f_a`, with age weights irrelevant. It also contributes nothing to a correctly computed **period total fertility rate** (TFR: the children a woman would bear at current age-specific rates), because the TFR sums the `f_a` directly and is already purged of age weights. This is not a limitation to be discovered; it is a property of the measures, and it is what makes the outcome distinction in §8 decisive.

**What would make the hypothesis wrong.** Not "composition has no effect" — the identity forbids that. The hypothesis is *demographically* wrong for a phenomenon if the composition share of that phenomenon's change is small. Since the phenomena are defined on completed fertility (§8), the share there is exactly zero, and the interesting empirical question is confined to the crude/period measures, where the share is what the studies estimate.

## 3. Search strategy

Full detail in `literature/search-logs/population-age-structure-momentum-search-scope.md` (frozen 2026-09-20). The two-axis query intersected a CBR/births/fertility outcome axis with a momentum- and decomposition-specific cause axis. The frame probe established that the generic terms `age structure`/`age composition` are homonym-inflated (32,363 records unrestricted; a core term of population ecology and population genetics), so they were admitted only in co-occurrence with a decomposition or crude-birth-rate term; bare use was excluded.

**Boundary rulings (walls), all enforced at the screen:**
- **A.11 (tempo).** Composition acts on the *age weights*; tempo acts on the *timing of the rates*. A Bongaarts–Feeney tempo adjustment is A.11's; a rate-versus-composition decomposition of the CBR is A.9's. Where a study splits both, the composition component is extracted here and the tempo component cross-refs A.11.
- **Population size/growth as outcome.** The momentum literature's dominant outcome is future population *size*, not a birth rate; those route off-cell (they are context, not an effect on fertility).
- **Fertility decomposition ≠ age-structure decomposition.** Bongaarts proximate-determinant decompositions (marriage, contraception, breastfeeding) and union-composition or preference decompositions route to A.2/A.5/A.7/A.13; only the age-structure-versus-rate split is A.9's. This wall did the most work at the screen.

## 4. PRISMA flow

| Stage | n |
|---|---:|
| Records screened (deduped: keyword tight ∪ refined gated ∪ citation snowball) | 1,299 |
| Excluded — off-topic / topical overlap | 1,001 |
| Excluded — population-size/growth outcome | 123 |
| Excluded — homonym (ecology/parasite/soil/education) | 81 |
| Routed to A.11 (tempo) | 26 |
| Routed to theory stream (formal momentum / stable-population canon) | 38 (+12 canon anchors) |
| **Included — empirical primary** | **16** |
| — of which retrieved and extracted | **10** |

Three features change how the funnel should be read. First, channel 1 (prior systematic reviews / meta-analyses) was **empty** — no one has systematically reviewed A.9, because an accounting identity has no effect literature to synthesise; this is a finding, not a gap. Second, the empirical cell was nearly missed: a first-pass screen on the highest-prior records returned only two studies and a preliminary "empty cell" reading that a targeted recall check then overturned to sixteen — the correction is documented, and it turned on the same "fertility decomposition ≠ age-structure decomposition" wall. Third, **only 10 of the 16 could be retrieved** (six were not procurable, including one for which a same-author different paper was found and set aside); the chapter is written on that 63% and §Provenance says what that costs.

## 5. The ideal design, and the distance from it

**5.1 The ideal estimand.** The share of an observed change in a country's crude birth rate over a stated interval attributable to the change in the age composition of women aged 15–49, holding all age-specific fertility rates fixed at a stated base schedule, reported as a signed percentage of the total CBR change, with the residual (rate) component and any interaction term shown so the parts sum to the whole. Because this is an identity, the "ideal" is not an identification strategy but a *complete and exhaustive* decomposition: no residual left uninterpreted, the base schedule stated, and the outcome a change (not a level) over a named window.

**5.2 The design that would identify it.** No source of exogenous variation is required or meaningful — there is no treatment. The ideal "design" is a **Das Gupta multi-factor standardization** (exhaustive, interaction-free) applied to a birth *rate* or *count*, with single-year age data at both endpoints, reporting the age-composition factor separately from marriage and marital/nonmarital fertility factors, over the phenomenon's full window rather than a short local interval. The falsifiable content is arithmetic consistency (the components sum to the total) and robustness to the base schedule, not an exclusion restriction.

**5.3 Distance table** (retrieved studies; dimensions that matter here are *outcome* — CBR/births vs growth/size; *method* — exhaustive vs residual-bearing; *window* — phenomenon-scale vs study-local; *separation* — is the age-composition factor reported on its own):

| Study | Setting / period | Outcome | Method | Window | Age-comp. factor isolated? | Distance |
|---|---|---|---|---|---|---|
| Freedman 1968 (A9-16) | Hong Kong 1961–65/66 | CBR | standardization | short (5 yr) | yes | near — clean CBR share |
| Palamuleni 2011 (A9-09) | South Africa 1996–2001 | CBR | std./decomposition | short | yes | near |
| Chaurasia 2017 (A9-07) | China/India 1950–2015 | growth / CBR multiplier | Kitagawa (2-factor) | full transition | yes (as `ab`) | near on CBR multiplier; growth outcome for the headline |
| A9-03 | South Korea ~1990–2015 | CBR | additive decomposition | medium | yes | near |
| A9-02 | China 2012–19 | births (count) | multiplicative (4-factor) | short | yes | near on count |
| A9-05 | South Korea –2017 | births (count) | decomposition | medium | yes (qual.) | medium (Korean; number to pin) |
| A9-08 | Malawi 1992–2015 | TFR/CBR | std./decomposition | medium | residual | medium (age factor reported as residual) |
| A9-10 | USA 1970–99 | GFR | 4-component | medium | yes | medium (value to pin) |
| A9-11 | USA 1960–92 | nonmarital fertility ratio | Das Gupta | medium | yes | medium (period-dependent; value to pin) |
| A9-15 | USA 1920–30 | CBR/specific rates | comparative | short | descriptive | far (descriptive) |

No single study matches the ideal on every dimension, but several are close on the CBR outcome (Freedman, Palamuleni, the Korea 2022 study). The **anchor** for the *method* ideal is Chaurasia 2017, the one retrieved study that runs a complete Kitagawa decomposition over the full transition and reports the age-composition factor explicitly.

## 6. Included studies and the estimator question

The ten retrieved studies are tabulated with their extracted age-structure contribution in `output/tables/population-age-structure-momentum-synthesis.md` and `extraction/population-age-structure-momentum.csv`.

**Naive estimator.** The comparison an author makes without thinking hard is to attribute an entire CBR movement to fertility behaviour, ignoring composition — the mirror image of this chapter's mechanism, and the reason the chapter exists. Within the decomposition literature, the recurring error is a *denominator* error rather than an estimator bias: reporting the composition share against the CBR *level*, or against the *study* window, rather than against the phenomenon's change (§8).

**Resolve disagreements, do not average — but here there is little to resolve.** On A.12 (twinning), the template's source chapter, four studies used a biased estimator and one corrected it, and the corrected sign was the truth; averaging would have manufactured a false effect. A.9 is the opposite case, and stating why is itself the finding: the studies do **not** disagree about one parameter. They measure the age-composition share in *different populations over different periods*, and that share genuinely differs — from near zero to near one hundred percent, and in both directions (§7). The dispersion is substantive heterogeneity in the age structures themselves, not an estimator artifact to be reconciled. The only method choice that moves a given study's number is whether the decomposition is exhaustive (Das Gupta, no residual) or two-factor with an interaction term (Kitagawa); this shifts the exact split modestly and never the order of magnitude.

## 7. Quantitative synthesis

**7.1 The answer in plain terms.** How much of a country's change in the number of births comes from its changing age make-up, rather than from women choosing to have more or fewer children? The honest answer is: *it depends entirely on the country and the years*, and it can be almost all or almost none. In Hong Kong in the early 1960s, about **80%** of the fall in the birth rate came from the age make-up alone. In South Africa in the late 1990s, the age make-up actually *pushed the birth rate up* — by about **60%** of the movement — while other forces pulled it down. In Malawi, by contrast, the age make-up explained almost nothing; marriage and marital childbearing did the work. And crucially, none of this changes the number of children a woman completes her life with — that figure is untouched by the age make-up, by definition.

**7.2 The estimate.** Because the estimand is a decomposition share across heterogeneous outcomes (CBR share, birth-count contribution, momentum factor, GFR component) carrying opposite signs, **no pooled estimate is reported** — a variance-weighted average of shares on different scales and signs would be a category error (and is disallowed by the review's outcome-level pooling rule). The synthesis is the distribution and its moderators:

- **Range.** The age-composition share of an observed CBR/birth-count change spans **~0–3%** (Malawi in some intervals; South Korea ~2.9%) to **~60–100%** (South Africa +60%; Hong Kong ~80% of the 1961–65 decline; China/India momentum ~80–100% of the natural growth rate).
- **Sign.** Negative — composition reduced the CBR/births — where a shrinking or ageing reproductive-age population coincided with fertility decline (Hong Kong 1961–65, South Korea, China 2012–19). Positive — composition raised or propped up the CBR — where a youthful, momentum-laden structure inflated the crude rate (South Africa, China/India, and the United States, where the age distribution *compensated* for declining marriage and helped keep the general fertility rate flat from 1970 to 1999).
- **Moderators.** The share is largest where the age structure is furthest from a stationary one (strong positive or negative momentum), over short observation windows (composition dominates short-run CBR movements), and where behaviour is otherwise stable; it is smallest where marriage and marital fertility carry the change.
- **Outcome dependence.** Every non-trivial number above is on a crude or count measure. Chaurasia 2017 confirms analytically (via `f = w × TFR/35`) that the age-composition multiplier is separable from, and leaves untouched, the total fertility rate; and completed cohort fertility is composition-free by construction.

## 8. Demographic significance

**The phenomenon to be explained is measured in completed children per woman (a change in cohort fertility); this mechanism offers a share of movement in the crude birth rate — a period, per-capita measure — and contributes, by construction, exactly zero to completed cohort fertility.**

That single units statement settles the verdict against the review's standard denominator before any arithmetic: the demographic-significance denominator fixed by PROTOCOL §4.2.1 is the change in *completed* fertility over each phenomenon's window, and the age-composition component of that change is identically zero. The chapter therefore reports, per the 2026-09-20 ruling (TICK-080 items 6–7), **two outcomes side by side**: the review-standard completed-fertility outcome (where A.9 is zero by construction) and the crude-birth-rate/birth-count outcome (where the studies live). Printing a single significance label would be a category error.

**8.1 Pre-modern (PM).** **For pre-modern variation, the verdict is NOT ASSESSED, because A.9 is out of scope for PM in the registry (§A.9 lists FDT and SDT only); were it assessed, the near-stationary, high-mortality age structures of pre-modern populations would give momentum little to work on, so the sign would be small.** NOT ASSESSED, not NEGLIGIBLE: no share was computed.

**8.2 First Demographic Transition (FDT).** **For the First Demographic Transition, the verdict is NEGLIGIBLE, because age composition contributes zero to completed cohort fertility — the measure on which the transition is defined — by construction, even though it accounts for as much as ~80% of contemporaneous crude-birth-rate movements.** On the review-standard denominator (the fall in completed fertility, ~1870–1965) the composition share is 0%. On the crude-birth-rate outcome the share is **SUBSTANTIAL to DOMINANT but setting- and period-specific** (e.g., Hong Kong ~80% of a five-year decline), and signed both ways. The reconciliation is that composition and momentum relocate births *in time* and inflate or deflate the *period, per-capita* rate, without changing how many children any cohort completes — which is exactly why the crude birth rate lagged and wobbled around the underlying transition rather than tracking it.

**8.3 Second Demographic Transition (SDT).** **For the Second Demographic Transition, the verdict is NEGLIGIBLE, because age composition again contributes zero to completed cohort fertility by construction, even as negative momentum from population ageing now suppresses the crude birth rate and the birth count.** On completed fertility, 0%. On the crude/count outcome, **MINOR to SUBSTANTIAL and, in the lowest-fertility settings, DOMINANT of short-run birth-count declines** (China 2012–19: the shrinking stock of childbearing-age women subtracted 150,000–340,000 births a year; South Korea: a secondary but non-trivial negative contributor). The sign has flipped relative to the FDT: the momentum that once inflated the CBR now deflates it.

## 9. GRADE rating

Per the 2026-09-20 ruling (TICK-080 item 5), A.9 is rated **NOT RATEABLE — non-effect estimand**, for every phenomenon, and the reason is structural rather than a matter of weak evidence.

| Phenomenon | Rating | Reason |
|---|---|---|
| PM | NOT RATEABLE — non-effect estimand (and no cell: out of registry scope) | The estimand is a decomposition of an identity, not a causal effect; and PM is out of scope. |
| FDT | NOT RATEABLE — non-effect estimand | The GRADE ladder (§4.1) grades identification strategies for a causal effect. A.9's studies are exact decompositions of an accounting identity; they can be arithmetically correct or incorrect, but not well- or badly-*identified*. Rating them "very low: correlational only" would misdescribe sound arithmetic as weak causal inference. |
| SDT | NOT RATEABLE — non-effect estimand | As FDT. |

This is not a downgrade and must not be read as one: the decomposition evidence is, where retrieved, methodologically sound and internally checkable. Certainty about a *share* is simply a different object from certainty about an *effect*, and the review's causal-credibility column does not apply to an identity. (The demographic-significance column, §8, carries the substantive verdict.)

## 10. Verdict

Population age structure and demographic momentum are an **accounting identity, not a behavioural cause of the fertility transitions**. They contribute **exactly zero, by construction, to the change in completed cohort fertility** — the measure on which the First and Second Demographic Transitions are defined — and therefore explain **none** of either transition as the review defines it. This is the one number to carry away: **0% of completed-fertility change.**

At the same time, on the *crude birth rate* and the *number of births* — the period, per-capita measures a casual observer actually sees — the age-composition component is large and highly variable: it ranged, across the ten retrieved studies, from about **0% to about 80–100%** of the observed movement, with the sign running **both ways** (inflating the crude rate under the youthful structures of mid-transition, deflating it under the ageing structures of lowest-low fertility). A.9 is thus best understood as the chapter that tells the rest of the review how much of a *headline* birth-rate movement to set aside as mechanical before attributing the remainder to any behavioural cause — the accounting layer that the behavioural chapters must net out, not a competing explanation. Because its estimand is a decomposition of an identity, it carries **no GRADE rating (NOT RATEABLE)**; its significance is entirely a matter of which outcome one measures.

## 11. Open questions and recommended studies

- **Procure the six unretrieved primaries** (China 2014; South Korea 2023; South Africa 2019 thesis; the China 1991 PDR decomposition, Yi/Vaupel/Wang, `10.2307/1971949`; Mexico 1991, Welti; India 1983, which needs OCR). None is expected to reverse the qualitative pattern, but the East-Asian and Latin American items would sharpen the marriage-versus-composition split, and the China 1991 PDR study is a canonical CBR decomposition.
- **Pin exact age-composition component values** for A9-05 (Korean-language), A9-10, and A9-11 from their decomposition tables (currently qualitative/partial).
- **A study that does not exist and should:** a harmonised, single-method (Das Gupta) decomposition of the crude birth rate into age-composition, nuptiality, and marital/nonmarital-fertility components across a common panel of FDT and SDT countries, over each phenomenon's full window, so the composition share is comparable across settings rather than reconstructed from ten different methods and windows. This is the object the review needs from A.9 and no single retrieved study supplies it.
- **PI calls:** confirm the NOT RATEABLE band and the per-outcome demographic-significance reporting (TICK-080 items 5–7), and confirm that A.9 is designated the accounting layer the behavioural chapters report net of (TICK-080 item 10). Both are applied here provisionally.

## 12. References

Retrieved and extracted (10): Freedman 1968 (Hong Kong, *Population Studies*); Palamuleni 2011 (South Africa, *Southern African Journal of Demography*); Chaurasia 2017 (China/India, *Comparative Population Studies*, `10.12765/CPoS-2017-12en`); [A9-03] 2022 (South Korea, *Journal of Population Research*, `10.1007/s12546-022-09287-3`); [A9-02] 2021 (China, *China Population and Development Studies*, `10.1007/s42379-021-00094-6`); [A9-05] Lee 2019 (South Korea, KJPS); [A9-08] 2024 (Malawi, `10.22146/jp.102685`); [A9-10] 2005 (USA, *Social Biology*, `10.1080/19485565.2002.9989096`); [A9-11] 1996 (USA, *Demography*, `10.2307/2061868`); [A9-15] 1932 (USA, *American Journal of Sociology*, `10.1086/215925`). Theory canon (routed to the JEL theory stream): Keyfitz 1971; Preston, Heuveline & Guillot 2001; Kitagawa 1955; Bongaarts & Bulatao 1999; Lutz, O'Neill & Scherbov 2003; Kim & Schoen 1997; Blue & Espenshade 2011. Full existence-verified anchor set in `literature/search-logs/population-age-structure-momentum-cold-start-anchors.json`.

---

## Provenance and standing caveats

**This chapter is written on 10 of 16 wanted full texts (63%).**

**The findings that would survive full retrieval are** the zero-by-construction contribution to completed cohort fertility (an identity, independent of any study) and the wide, both-signed dispersion of the crude-birth-rate share (established already by studies spanning Hong Kong, South Africa, China, Korea, the US, and Malawi across 1932–2024). **The findings that might not are** the precise upper bound of the share — the ~80–100% cases rest on Hong Kong, South Africa, and the China/India momentum study — and the exact position of the marriage-versus-composition split, which the six unretrieved studies (four of them East Asian or Latin American) could move.

**Numbers sourced from abstracts or first-pass tables rather than full-text tables** and on the residual retrieval list: A9-05 (Korean-language; direction firm, magnitude qualitative), A9-08 (component shares from the abstract), A9-10 and A9-11 (direction firm, exact age-distribution component to be pinned), A9-15 (descriptive). The six unretrieved studies (A9-01, A9-04, A9-06, A9-12, A9-13, A9-14) contribute no numbers.

**Standing methodological dependency:** the GRADE band (NOT RATEABLE) and the per-outcome demographic-significance format are not yet in PROTOCOL; they apply the 2026-09-20 rulings recorded in TICK-080 (items 5–7, 10), which await that ticket's formal amendment and PI sign-off. If those rulings change, §8 and §9 change with them.
