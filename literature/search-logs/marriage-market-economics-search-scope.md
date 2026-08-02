# Preliminary search scope: marriage market and assortative mating

**Hypothesis slug:** `marriage-market-economics`  
**Category:** Economic  
**Target phenomena:** FDT and SDT  
**Prepared:** 2026-08-01  
**Status:** Preliminary scoping search under TICK-058. This is not the preregistered production
search. Formal screening, PRISMA counts, and evidentiary verdicts wait for TICK-001 and TICK-006.

## Causal claim

The hypothesis asks whether the characteristics of available partners and the cost of finding a
suitable match change union formation and fertility. The primary treatment is match quality or a
quality-weighted pool of potential partners: education, earnings, employment, incarceration status,
or another characteristic that affects the gains from forming a household. The primary outcome is
fertility per woman or man, preferably completed fertility; marriage and assortative matching are
mediators or mechanism outcomes.

The sign is not fixed. Better male economic prospects may increase births through household income
and a larger pool of partners whom women are willing to marry. Better female prospects may reduce
births through the opportunity cost of child-rearing, increase births through income, or change
partner selection. Educational mismatch can delay union formation, but adaptation through
hypogamy, cohabitation, or nonmarital childbearing can weaken the fertility effect.

## Boundary walls

1. **Raw headcount versus partner quality.** A raw adult or operational sex ratio belongs to
   `sex-ratio-marriage-market`. A ratio restricted by education, employment, earnings, or
   incarceration belongs here because the treatment is the quality of available partners. Mixed
   incarceration designs must be tagged `MIXED_HEADCOUNT_QUALITY`.
2. **Marriage timing as treatment versus mediator.** A study of age at marriage causing fertility
   belongs to `marriage-timing-age-at-marriage`. A partner-quality shock that changes marriage and
   fertility belongs here, even when marriage timing mediates the effect.
3. **Education itself versus the match.** A schooling reform belongs primarily to the education or
   compulsory-schooling chapter. It enters this chapter as primary evidence only when the design
   identifies a partner-composition or matching channel, rather than merely reporting spouse
   education as another outcome.
4. **Labor demand itself versus marriage-market value.** Gender-neutral income shocks belong to the
   income or uncertainty chapters. Gender-specific shocks enter here when the study tests relative
   economic standing in the partner market and reports fertility.
5. **Sorting versus fertility.** A study that measures homogamy or hypogamy without fertility is
   mechanism evidence. It cannot establish the causal claim by itself.

## Estimand cells

| Cell | Treatment | Outcome | Role |
|---|---|---|---|
| `PRIMARY_QUALITY_FERTILITY` | Exogenous change in potential partners' earnings, employment, education, or availability conditional on quality | Birth rate, parity, childlessness, or completed fertility | Primary synthesis |
| `PRIMARY_MATCH_FERTILITY` | Exogenous change in match type or match quality | Fertility | Primary synthesis; expected to be sparse |
| `MEDIATION_MATCH` | Exogenous upstream change | Fertility plus union formation or spouse characteristics | Bridge evidence; mediation claim requires an identified decomposition |
| `MECHANISM_UNION` | Partner quality or educational composition | Marriage, cohabitation, spouse type, or search duration only | Mechanism stream |
| `DESCRIPTIVE_SORTING_FERTILITY` | Observed couple type | Observed fertility | Descriptive association; selection is unresolved |
| `THEORY_MATCHING` | Formal matching or household-production model | Theoretical prediction | Theory stream |
| `OFF_RAW_SEX_RATIO` | Raw partner headcount | Any | Route to `sex-ratio-marriage-market` |
| `OFF_EDUCATION_DIRECT` | Own education | Fertility | Route to education hypothesis unless match channel is identified |
| `OFF_LABOR_DIRECT` | Gender-neutral labor-market condition | Fertility | Route to income, uncertainty, or female-wage hypothesis |
| `REVERSE` | Fertility or parenthood changes matching | Match outcome | Context only |

## Draft eligibility rules

- Include quantitative primary evidence only when a fertility outcome and a marriage-market
  treatment or identified matching pathway appear in the same study.
- Preserve married, unmarried, and total births separately. A rise in births need not imply more
  marriage, as Kearney and Wilson's fracking design illustrates.
- Preserve male and female treatments separately. Schaller and Autor, Dorn, and Hanson show why a
  pooled labor-demand coefficient would erase the hypothesis's main comparison.
- Treat spouse education and couple type as endogenous unless a design supplies exogenous variation.
- Record whether fertility is period, cohort, completed, marital, nonmarital, first birth, or higher
  parity. Do not pool these outcomes without a predeclared harmonization rule.
- Include FDT evidence only when the study window and fertility regime are verified. Calendar year
  alone does not determine the transition.

## Preliminary query clusters

These strings are drafts for later translation into OpenAlex, Semantic Scholar, Crossref, and
field-journal syntax.

1. `("marriage market" OR "marriageable men" OR partner availability) AND (fertility OR birth* OR childlessness OR parity)`
2. `("assortative mating" OR educational homogamy OR educational hypogamy OR marital sorting) AND (fertility OR birth* OR completed fertility)`
3. `("education gap" OR "marriage squeeze" OR partner mismatch) AND (union formation OR marriage) AND (fertility OR birth*)`
4. `((male earnings OR male employment OR incarceration OR manufacturing decline) AND marriage) AND (fertility OR birth*)`
5. `("gender-specific labor demand" OR "relative economic stature") AND (marriage OR family formation) AND fertility`
6. `("spouse education" OR partner education) AND (natural experiment OR instrumental variable OR regression discontinuity) AND fertility`

The production search must also search Demography, Demographic Research, Population Studies,
Population and Development Review, European Journal of Population, Journal of Marriage and Family,
JHR, Review of Economics and Statistics, AEA journals, NBER, and IZA. Forward and backward citation
searches should begin from Becker (1973), Schwartz and Mare (2005), Raymo and Iwasawa (2005),
Schaller (2016), Kearney and Wilson (2018), and Autor, Dorn, and Hanson (2019).

## Search trail for the scoping pass

The 2026-08-01 pass searched publisher and working-paper sites through web queries restricted where
possible to AEA, NBER, IZA, Demographic Research, Springer, Oxford Academic, and journal or
institutional repositories. The candidate map is
`literature/search-logs/marriage-market-economics-scoping-candidates.csv`. Bibliographic identities
were checked against publisher, DOI, NBER, or institutional pages. Abstract-level findings remain
preliminary until full texts are retrieved and extracted.

## Main uncertainty after scoping

The literature strongly establishes sorting and changing partner composition. The causal fertility
evidence found so far is narrower and often identifies a shock to gender-specific earnings rather
than assortative mating itself. The production review should therefore report two evidence streams
and resist treating a change in spouse similarity as though it were an identified change in births.

