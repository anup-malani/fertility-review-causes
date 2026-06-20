# Calibration Report: old-age-security-pension-crowdout, Batch 3

**Date:** 2026-06-20
**Primary model (screener):** claude-haiku-4-5-20251001
**Gold standard:** claude-sonnet-4-6
**Papers screened this batch:** 1000
**Stopping criterion:** Haiku FN rate < 3%
**Verdict:** CRITERION MET (FN rate = 0.7%)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Papers compared | 1000 |
| Agreement rate | 73% |
| Both RELEVANT | 41 |
| Both NOT_RELEVANT | 657 |
| Both UNCERTAIN | 32 |
| Haiku FN rate (H=NOT_RELEVANT, S=RELEVANT) | **0.7%** (7 papers) |
| Haiku FP rate (H=RELEVANT, S=NOT_RELEVANT) | 2.3% (23 papers) |
| Haiku confusion (H=UNCERTAIN, S decisive) | 19.3% (193 papers) |
| Sonnet UNCERTAIN rate | 7.9% (79 papers) |
| **Stopping criterion met** | **YES** |

---

## Stopping Criterion

**MET** — Haiku FN rate is 0.7%, well below the 3% threshold. Proceed to routing rule (see routing-rule.md).

---

## False Negatives (Haiku Missed, Sonnet Caught)

7 papers total.

**1. The Demographic Transition: Causes and Consequences** (2011 | DOI: 10.3386/w17057)
- Haiku: NOT_RELEVANT [MEDIUM] — Paper does not address causal link from pensions/old-age security to fertility.
- Sonnet: RELEVANT [HIGH] — Explicitly develops and tests theoretical mechanisms for fertility decline including the old-age security motive, examining whether intergenerational transfers and human capital demand triggered the demographic transition.

**2. Fertility intentions in a cross-cultural view: the value of children reconsidered** (2002 | DOI: 10.4054/mpidr-wp-2002-002)
- Haiku: NOT_RELEVANT [MEDIUM] — Paper does not address causal link from pensions/old-age security to fertility.
- Sonnet: RELEVANT [MEDIUM] — Applies the 'Value of Children' framework to explain fertility intention differences across cultures, which inherently includes old-age security and economic utility of children as components of the value-of-children model.

**3. Fertility, Longevity, and Capital Flows** (n.d.)
- Haiku: NOT_RELEVANT [HIGH] — No apparent connection to pension/old-age security effects on fertility.
- Sonnet: RELEVANT [HIGH] — Incorporates fertility and longevity in an OLG lifecycle savings model where social security (PAYG) shapes inter-generational transfers and capital flows, directly modeling pension systems' interaction with fertility in a framework relevant to the hypothesis.

**4. Does Government Crowds Out the Family?** (n.d.)
- Haiku: NOT_RELEVANT [HIGH] — No apparent connection to pension/old-age security effects on fertility.
- Sonnet: RELEVANT [HIGH] — Title directly addresses the crowding-out hypothesis — whether government provision (including pensions) substitutes for family support — which is the core mechanism of the old-age security hypothesis for fertility decline.

**5. Family formation and the life cycle** (1979 | DOI: 10.2307/2061083)
- Haiku: NOT_RELEVANT [HIGH] — Mathematical analysis of life-cycle fertility and family size conditional on mortality; no pension mechanism.
- Sonnet: RELEVANT [MEDIUM] — Develops mathematical expressions for life-cycle family formation including the probability of having at least one child outlive the mother and expected number of children — directly relevant to the structural old-age security value of children and sequential birth strategies to secure a surviving child.

**6. Female Labour Force Status and Fertility Behaviour-Some Theoretical, Methodological and Policy Issues** (1979 | DOI: 10.30541/v18i4pp.341-357)
- Haiku: NOT_RELEVANT [HIGH] — Discusses female labor force status and fertility; notes women's dependence on children for social security, but no formal pension analysis.
- Sonnet: RELEVANT [MEDIUM] — Explicitly discusses the old-age security motive for fertility: societies where women depend on children for social and economic security tend toward high fertility, placing this paper directly within the hypothesis being reviewed.

**7. Longer Life and Higher Fertility in an OLG Economy with Production** (2013 | DOI: 10.1155/2013/207313)
- Haiku: NOT_RELEVANT [MEDIUM] — OLG model with fertility but without pension or PAYG system component.
- Sonnet: RELEVANT [MEDIUM] — This paper uses an OLG model to study how longevity changes affect fertility, a framework closely related to pension-fertility models where old-age security arrangements and survival probabilities jointly determine equilibrium fertility.

---

## False Positives (Haiku Included, Sonnet Excluded)

23 papers total.

**1. The effect of family formation on the build-up of pension rights among minority ethnic groups and native women in Belgium** (2017 | DOI: 10.1017/s0144686x17000010)
- Haiku: RELEVANT [MEDIUM] — Studies how fertility/family formation patterns affect pension accumulation.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies the reverse direction — how having children affects women's pension accumulation — not whether pension availability affects fertility decisions.

**2. Reducing Food Poverty and Vulnerability among the Rural Elderly with Chronic Diseases: The Role of the New Rural Pension Scheme in China** (2018 | DOI: 10.3390/ijerph15061253)
- Haiku: RELEVANT [MEDIUM] — Studies pension scheme role in elderly welfare amid low fertility and rural-urban migration.
- Sonnet: NOT_RELEVANT [HIGH] — This paper assesses the New Rural Pension Scheme's impact on elderly food poverty, not its effect on fertility or childbearing decisions.

**3. Family and childcare support public expenditures and short-term fertility dynamics** (2013 | DOI: 10.2298/pan1303347e)
- Haiku: RELEVANT [HIGH] — Studies public family support (including social security cash benefits) elasticity to fertility.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies the effect of childcare and family cash benefits on birth rates, not old-age pension systems as a determinant of fertility.

**4. The Quality of Life and Mortality Risk of Elderly People in Rural China** (2013 | DOI: 10.1177/1010539512472362)
- Haiku: RELEVANT [HIGH] — Examines elderly well-being: family care strained by low fertility, limited social security.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines how family support affects elderly well-being in rural China, noting declining fertility strains family care capacity, but does not study pension effects on fertility.

**5. Managing the demographic risk of pension systems** (2016)
- Haiku: RELEVANT [MEDIUM] — Addresses fertility decline as demographic risk to public pension systems.
- Sonnet: NOT_RELEVANT [HIGH] — This paper discusses how demographic changes including fertility decline create financial risk for pension systems, treating fertility as an exogenous input rather than an outcome of pension design.

**6. Widowhood and Retirement Timing: Evidence from the Health and Retirement Study** (2018 | DOI: 10.1515/bejeap-2017-0178)
- Haiku: RELEVANT [MEDIUM] — Examines retirement decisions under low fertility conditions and family shocks.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies how spousal death affects retirement timing, with only passing reference to fertility decline as demographic background.

**7. How Family Status and Social Security Claiming Options Shape Optimal Life Cycle Portfolios** (2013 | DOI: 10.3386/w19583)
- Haiku: RELEVANT [MEDIUM] — Models household decisions under Social Security rules with demographic shocks (marriage, children).
- Sonnet: NOT_RELEVANT [HIGH] — This paper models how Social Security claiming rules and family demographics affect optimal household portfolio decisions, not pension effects on fertility.

**8. Pension Policy in Europe and the United States – Towards a New Public-Private Pension Mix** (2020 | DOI: 10.2139/ssrn.3565087)
- Haiku: RELEVANT [MEDIUM] — Analyzes pension reforms in context of aging population and low fertility.
- Sonnet: NOT_RELEVANT [HIGH] — This paper reviews pension reform agendas in the EU and US in response to population aging and fiscal challenges, treating low fertility as a driver of pension reform rather than the reverse.

**9. The Relationship between the Child Support Grant and Teenage Fertility in Post-Apartheid South Africa** (2013)
- Haiku: RELEVANT [MEDIUM] — Tests whether child support grant (cash transfer, not old-age pension) affects teenage fertility; structure analogous to 'children as assets' mechanism but program is for child support, not retirement.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines whether child support grants incentivize teenage pregnancy in South Africa, studying a different transfer mechanism without the pension-fertility hypothesis.

**10. Features of the functioning of national pension systems of Eastern Europe and Ukraine in the modern conditions** (2019 | DOI: 10.22616/esrd.2019.120)
- Haiku: RELEVANT [HIGH] — Studies pension reform effects on fertility.
- Sonnet: NOT_RELEVANT [HIGH] — This paper describes pension system reforms in Eastern Europe driven by demographic pressures, treating fertility decline as context rather than studying pension effects on fertility.

**11. Does the Comprehensive two-Child Policy Help Improve the Financial Sustainability of Individual Accounts of Basic Pension in China?** (2020 | DOI: 10.36346/sarjhss.2020.v02i06.004)
- Haiku: RELEVANT [MEDIUM] — Links fertility policy to pension sustainability.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines how China's two-child policy affects pension financial sustainability, treating fertility change as an input to pension finance rather than studying pension effects on fertility (reverse direction).

**12. The High Cost of Judges: Reconsidering Judicial Pensions and Retirement in an Ageing Population** (2011 | DOI: 10.22145/flr.39.1.2)
- Haiku: RELEVANT [HIGH] — Discusses both pensions/old-age security and fertility outcomes.
- Sonnet: NOT_RELEVANT [HIGH] — This paper reviews judicial pension costs in the context of Australian population aging, treating demographic change as background rather than studying pension-fertility mechanisms.

**13. Retirement Income Provision and Household Income: Between- and Within-Cohort Inequalities in Germany and the United States since the 1980s** (2016 | DOI: 10.1057/978-1-137-51184-3_7)
- Haiku: RELEVANT [HIGH] — Discusses both pensions/old-age security and fertility outcomes.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies inequality in retirement income provision across cohorts due to pension reform, using fertility decline as a background context rather than studying pension effects on fertility.

**14. Family Histories and Women's Retirement: The Role of Childbearing and Marital Experiences** (2014 | DOI: 10.2139/ssrn.2471444)
- Haiku: RELEVANT [MEDIUM] — Addresses relationship between retirement security and family formation decisions.
- Sonnet: NOT_RELEVANT [MEDIUM] — No abstract; this paper appears to study how childbearing and marital experiences affect women's retirement outcomes — the causal arrow runs from fertility to pension, not the direction under review.

**15. Projecting retirement income of future retirees with panel data: results from the modeling income in the near-term (MINT) project** (1999)
- Haiku: RELEVANT [HIGH] — Discusses both pensions/old-age security and fertility outcomes.
- Sonnet: NOT_RELEVANT [HIGH] — This paper projects retirement income using panel data including fertility history as a predictor variable, but treats fertility as a determinant of retirement income rather than the reverse direction under review.

**16. Household arrangements of the elder elderly** (2010 | DOI: 10.1590/s0104-11692010000100004)
- Haiku: RELEVANT [MEDIUM] — Addresses relationship between retirement security and family formation decisions.
- Sonnet: NOT_RELEVANT [MEDIUM] — This cross-sectional study of living arrangements of the very old in Brazil describes retirement benefit receipt and number of children as descriptive variables but does not analyze pension effects on fertility decisions.

**17. Associations between Childbirth, Hospitalization and Disability Pension: A Cohort Study of Female Twins** (2014 | DOI: 10.1371/journal.pone.0101566)
- Haiku: RELEVANT [MEDIUM] — Addresses relationship between retirement security and family formation decisions.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies whether childbirth leads to higher risk of disability pension in Swedish women — the causal arrow runs from fertility to pension receipt, not the direction under review.

**18. Government funds and demographic transition: alleviating ageing costs in a small open economy** (2008)
- Haiku: RELEVANT [HIGH] — Discusses both pensions/old-age security and fertility outcomes.
- Sonnet: NOT_RELEVANT [HIGH] — This DSGE model paper studies tax smoothing responses to population aging in Finland, treating demographic transition as exogenous rather than studying pension effects on fertility.

**19. Possible Paths for GDP Per Capita – Simulation with a Demographic Growth Model** (2017 | DOI: 10.25201/fer.16.4.3657)
- Haiku: RELEVANT [MEDIUM] — Uses theoretical framework linking intergenerational transfers to fertility.
- Sonnet: NOT_RELEVANT [HIGH] — This OLG-based simulation model treats fertility as exogenous to project GDP per capita paths, not modeling pension effects on fertility.

**20. Universal Transfers, Tax Breaks and Fertility: Evidence from a Regional Reform in Norway** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Examines cash transfers and tax breaks on fertility using a natural experiment; transfers are a form of government support that could substitute for children as old-age security.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies the effect of child benefits and tax breaks (not pension/old-age security) on fertility in Norway.

**21. The Life Cycle Model of the Fertility Choice in Hungary** (n.d.)
- Haiku: RELEVANT [HIGH] — Life-cycle model of fertility decisions incorporating family benefits scheme; directly tests pension/transfer policies on fertility timing.
- Sonnet: NOT_RELEVANT [MEDIUM] — This paper models fertility choices in Hungary using a lifecycle framework, focusing on family benefits and timing of childbearing rather than old-age security motives or pension mechanisms.

**22. Can Land Transfer Alleviate the Poverty of the Elderly? Evidence from Rural China** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Examines poverty support mechanisms for elderly in rural China; relates to old-age security function of assets and family.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines farmland transfer as a poverty alleviation mechanism for rural elderly in China, not the old-age security motive for fertility decisions.

**23. Grandparental Investment** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Reviews theory of grandparental investment; relates to intergenerational support functions and fertility determinants.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines motivations for grandparental childcare investment from evolutionary psychology and economics perspectives, not old-age security motives for fertility.

---

## Haiku Confusion (UNCERTAIN When Sonnet Was Decisive)

193 papers total. Selected examples below.

**1. The Transportation of the American Pension System: Was It Beneficial for Workers?** (2011 | DOI: 10.17848/9780880993906)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines the shift from defined-benefit to defined-contribution pension plans and worker welfare outcomes, with no discussion of fertility or childbearing decisions.

**2. Pension Sytems and the Allocation of Macroeconomic Risk** (2006 | DOI: 10.18452/3996)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This OLG paper focuses on optimal risk-sharing between generations and capital accumulation, with no mention of fertility as an endogenous variable responding to pension arrangements.

**3. Forgotten people: poverty, risk and social security in Indonesia: the case of the Madurese** (2015 | DOI: 10.5860/choice.190286)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This book focuses on livelihoods and risk strategies of poor Indonesians, not on pension systems as a determinant of fertility decisions.

**4. Population Aging and Economic Development: Anxieties and Policy Responses** (2011 | DOI: 10.1007/s12062-011-9053-5)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [MEDIUM] — No abstract available, but the title suggests this paper treats low fertility and population aging as a policy problem to be managed, not as an outcome caused by pension generosity.

**5. Value of Children and the social production of welfare** (2014 | DOI: 10.4054/demres.2014.30.66)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: RELEVANT [MEDIUM] — This paper critically discusses the Value of Children framework, which encompasses old-age security as a key reason parents have children, directly relevant to the children-as-retirement-insurance motive for fertility.

**6. A Social Service Strategy for a Low Birth Rate and an Aged Society** (2015 | DOI: 10.14391/ajhs.9.17)
- Haiku: UNCERTAIN [LOW] — Fertility study; pension connection unclear from title/abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This paper examines South Korean social service policy responses to low birth rates, treating fertility decline as a given problem rather than studying pensions as a cause.

**7. The Influence of Pension Mode on the Mental Health of Older Adults—Evidence from Older Adults in China** (2021 | DOI: 10.3390/ijerph19010119)
- Haiku: UNCERTAIN [LOW] — Pension and demographics mentioned; fertility direction unclear.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies how pension type affects mental health of the elderly, with no connection to fertility or childbearing.

**8. Do workplace interventions reduce disability rates?** (2016 | DOI: 10.1093/occmed/kqw169)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [HIGH] — This paper evaluates workplace interventions for retaining older workers and mentions fertility decline only as demographic background context.

**9. Long Term Impacts of Vouchers for Vocational Training: Experimental Evidence for Colombia** (2015 | DOI: 10.3386/w21390)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [HIGH] — This paper evaluates a vocational training voucher program's effects on labor market outcomes and social security contributions, with no relevance to fertility or old-age security motives.

**10. Financial education: From better personal finance to improved citizenship** (2023 | DOI: 10.1017/flw.2023.7)
- Haiku: UNCERTAIN [LOW] — Pension and demographics mentioned; fertility direction unclear.
- Sonnet: NOT_RELEVANT [HIGH] — This paper is about financial literacy and pension planning competence, not about how pensions affect fertility decisions.

**11. Family Size, Sibling Rivalry and Migration: Evidence from Mexico** (2016 | DOI: 10.2139/ssrn.2796602)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [MEDIUM] — No abstract available, but the title suggests this paper examines family size and migration dynamics rather than pension-driven fertility decisions.

**12. Policy Options for Financing the Future Health and Long-Term Care Costs in Japan** (2006 | DOI: 10.3386/w12427)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [HIGH] — This paper analyzes pre-funding options for Japan's aging-related health costs, treating demographic change as a given rather than examining pension effects on fertility.

**13. Labor Supply Distortion and Capital Accumulation when Public Pension Systems Differ in an Aging Economy** (2015)
- Haiku: UNCERTAIN [LOW] — Pension and demographics mentioned; fertility direction unclear.
- Sonnet: NOT_RELEVANT [HIGH] — This paper compares PAYG and funded pension systems' effects on labor supply and capital accumulation in an aging economy, treating fertility as exogenous rather than as an outcome of pension design.

**14. Essays on public pension systems, with special reference to China** (2010)
- Haiku: UNCERTAIN [LOW] — Pension and demographics mentioned; fertility direction unclear.
- Sonnet: RELEVANT [MEDIUM] — This thesis uses an OLG general equilibrium model to study how demographic changes and pension system design affect individual choices and macroeconomic variables, which likely includes fertility as an endogenous variable.

**15. Socioeconomic disparities in life expectancy gains among retired German men, 1997–2016** (2019 | DOI: 10.1136/jech-2018-211742)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies socioeconomic mortality disparities among retired German men using pension data as a proxy for socioeconomic status, with no relevance to fertility.

**16. Stochastic Infinite Horizon Forecasts for Social Security and Related Studies** (2004 | DOI: 10.3386/w10917)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This paper develops stochastic forecasting methods for Social Security fiscal sustainability, treating demographics as inputs rather than examining pension effects on fertility.

**17. Modeling and Prediction of Birth Rate in China** (2024 | DOI: 10.54254/2754-1169/59/20231010)
- Haiku: UNCERTAIN [LOW] — Fertility study; pension connection unclear from title/abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This is a time-series forecasting paper on China's birth rate with no analysis of pension or old-age security as a causal driver.

**18. The Finnish social security system: Background to the Finnish basic income experiment** (2021 | DOI: 10.4337/9781839104855.00010)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This chapter describes Finland's social protection system in the context of the basic income experiment, with no discussion of effects on fertility.

**19. Gender and vulnerable employment in the developing world: Evidence from global microdata** (2022 | DOI: 10.1016/j.worlddev.2022.106010)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies gender inequality in precarious employment in developing countries, not old-age security or fertility.

**20. Annual DC Pension Statements and the Communications Challenge** (2012 | DOI: 10.1787/5k97gkd06kth-en)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This OECD working paper is about pension communication and statement design, entirely unrelated to fertility.

**21. INSTITUTIONAL STRUCTURE AND POLICY CHANGE: PENSION REFORMS IN BELGIUM, FRANCE, SWEDEN, AND THE UNITED KINGDOM** (2003)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This dissertation studies the political process behind pension reforms in four European countries, with no connection to fertility outcomes.

**22. Poverty Correlates and Indicator-Based Targeting in Eastern Europe and the Former Soviet Union** (1999 | DOI: 10.1596/1813-9450-1942)
- Haiku: UNCERTAIN [LOW] — Pension-fertility connection unclear from available information.
- Sonnet: NOT_RELEVANT [HIGH] — This World Bank paper analyzes poverty patterns and social assistance targeting in transition economies, with no relevance to pension-fertility linkages.

**23. Political Measures against Declining Birthrate—Implication of Good Family Policies and Practice in Sweden or France** (2018 | DOI: 10.1265/jjh.73.322)
- Haiku: UNCERTAIN [LOW] — Fertility study; pension connection unclear from title/abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This paper evaluates family policies that aim to raise birth rates in Sweden and France, not the old-age security motive for childbearing.

**24. Trends and inequalities in maternal and child health in a Brazilian city: methodology and sociodemographic description of four population-based birth cohort studies, 1982–2015** (2018 | DOI: 10.1093/ije/dyy170)
- Haiku: UNCERTAIN [LOW] — Fertility study; pension connection unclear from title/abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This is a methodological paper describing birth cohort studies in Brazil focused on maternal and child health, with no connection to old-age security.

**25. The Effect of Public Pension Wealth on Saving and Expenditure** (2015 | DOI: 10.17848/wp15-223)
- Haiku: UNCERTAIN [LOW] — Pension study; fertility implications unclear from abstract.
- Sonnet: NOT_RELEVANT [HIGH] — This paper studies whether public pension wealth crowds out private saving using Poland's 1999 reform, not whether pensions crowd out fertility.

*(168 additional confusion papers not shown; full list in temp/old-age-security-pension-crowdout-batch-3.json)*

---

## Pattern Analysis

The 7 false negatives share three overlapping patterns.

**Pattern 1: OLG/lifecycle models where fertility is endogenous but pension is not the named variable (4 papers)**

Papers 3 (*Fertility, Longevity, and Capital Flows*), 5 (*Family formation and the life cycle*), and 7 (*Longer Life and Higher Fertility in an OLG Economy with Production*) all use overlapping-generations or lifecycle frameworks in which fertility responds to survival probabilities or intergenerational transfer structures — the core mechanics of the pension-crowdout mechanism — but neither "pension" nor "social security" appears as a named object of analysis. Haiku anchors on the keyword "pension" and correctly notes its absence; Sonnet recognizes that the structural mechanism is equivalent. Paper 4 (*Does Government Crowds Out the Family?*) is the reverse: the title names the exact crowdout mechanism but Haiku failed to connect "government crowding out family" to the pension-fertility channel, probably because "pension" again did not appear in the visible metadata.

**Pattern 2: Value-of-children / old-age support framing without formal pension analysis (2 papers)**

Papers 2 (*Fertility intentions in a cross-cultural view*) and 6 (*Female Labour Force Status and Fertility Behaviour*) discuss the old-age security motive for fertility explicitly — children as social insurance where formal pensions are absent — but neither paper evaluates a pension policy change or formal social security system. Haiku's screening rule appears to require a pension mechanism to be operationalized (a program, reform, or model parameter); Sonnet accepts the old-age security motive stated at any level of formality.

**Pattern 3: Broad demographic-transition reviews where OAS is one of several mechanisms (1 paper)**

Paper 1 (*The Demographic Transition: Causes and Consequences*) is a survey that explicitly develops and empirically tests the old-age security motive alongside other mechanisms for the demographic transition. Haiku's failure here is probably a threshold effect on length and specificity: the abstract of a broad survey paper does not foreground any single mechanism, and Haiku classified it as not addressing the pension-fertility link when the pension mechanism is in fact a named chapter.

---

## Prompt Revision Suggestions

**Change 1:** Broaden recognition of the old-age security motive stated informally.

*Current (inferred):* Screen for papers that analyze a formal pension system, PAYG transfer, or social security program as a causal driver of fertility.

*Revised:* Also classify as RELEVANT papers that discuss the old-age security or "children as insurance" motive for fertility — including papers that invoke this motive through the Value of Children framework, lifecycle survival probabilities, or informal intergenerational support — even if no formal pension program is named.

*Rationale:* Catches FN papers 2 (*Fertility intentions in a cross-cultural view*) and 6 (*Female Labour Force Status*), and a subset of the confusion papers rated RELEVANT by Sonnet under the Value of Children heading (*Value of Children and the social production of welfare*).

**Change 2:** Recognize OLG/lifecycle models where fertility is endogenous and intergenerational transfers are structural.

*Current (inferred):* Requires an explicit pension policy or program as the treatment variable.

*Revised:* Also classify as RELEVANT OLG models in which fertility is an endogenous choice variable and intergenerational transfers — formal or informal, including bequests, PAYG contributions, or survival-contingent child investments — enter the agent's budget constraint or utility function. The structural equivalence to pension-crowdout is sufficient for inclusion.

*Rationale:* Catches FN papers 3 (*Fertility, Longevity, and Capital Flows*), 5 (*Family formation and the life cycle*), and 7 (*Longer Life and Higher Fertility in an OLG Economy with Production*). Will also resolve a substantial fraction of the 193 confusion papers where Haiku is UNCERTAIN on OLG pension papers that Sonnet correctly excludes — the revised rule will help Haiku distinguish OLG models with endogenous fertility (RELEVANT) from OLG models with exogenous fertility used only for macroeconomic projections (NOT_RELEVANT).

**Change 3:** Classify as RELEVANT any paper whose title or abstract directly invokes the government/family crowdout framing.

*Current (inferred):* Titles are not weighted heavily if the abstract does not mention pension or social security.

*Revised:* If a paper's title uses language of "government crowding out family," "state substituting for kin," or "public provision replacing private intergenerational support," classify as RELEVANT regardless of whether "pension" appears, and flag for human review.

*Rationale:* Catches FN paper 4 (*Does Government Crowds Out the Family?*) directly. The crowdout framing is precise enough that title-level signal should be treated as a strong positive indicator.

---

## Recommendation

Stopping criterion met — Haiku FN rate of 0.7% is below the 3% threshold, and the pattern analysis confirms the remaining misses are addressable through prompt refinement rather than model replacement; proceed to full run using routing-rule.md.
