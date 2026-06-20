# Calibration Report: old-age-security-pension-crowdout, Batch 4

**Date:** 2026-06-20
**Primary screener:** claude-haiku-4-5-20251001 (Haiku)
**Gold standard:** claude-sonnet-4-6 (Sonnet)
**Papers fetched this batch:** 1,000
**Papers compared (matched):** 999
**Stopping criterion:** Haiku FN rate < 3%
**Verdict:** STOPPING CRITERION MET

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Papers compared | 999 |
| Agreement rate | 83.1% |
| Both RELEVANT | 46 |
| Both NOT_RELEVANT | 760 |
| Both UNCERTAIN | 24 |
| Haiku FN rate (H=NOT_RELEVANT, S=RELEVANT) | **0.7%** (7 papers) |
| Haiku FP rate (H=RELEVANT, S=NOT_RELEVANT) | 4.0% (40 papers) |
| Haiku confusion (H=UNCERTAIN, S decisive) | 7.6% (76 papers) |
| Sonnet UNCERTAIN rate | 7.0% (70 papers) |

---

## Stopping Criterion

**MET** — Haiku FN rate of 0.7% is well below the 3% threshold. Proceed to routing rule (see routing-rule.md).

---

## False Negatives (Haiku Missed, Sonnet Caught)

7 papers total.

**1. Social Norms and Economic Behavior in Traditional Communities** (n.d.)
- Haiku: NOT_RELEVANT [LOW] — No clear pension-fertility causal relationship
- Sonnet: RELEVANT [HIGH] — Explicitly analyzes the asymmetry between public (institutionalized) old-age transfers and private investment in children, directly addressing the crowdout dynamic where public eldercare substitutes for private family-based support.

**2. Fiscal Decentralization and Public Service Delivery** (n.d.)
- Haiku: NOT_RELEVANT [LOW] — No clear pension-fertility causal relationship
- Sonnet: RELEVANT [HIGH] — OLG model paper explicitly studying how delayed retirement (a pension policy parameter) affects birth rates through caregiving resource constraints, directly modeling retirement policy as a cause of fertility change.

**3. Insurance Markets and Adverse Selection** (n.d.)
- Haiku: NOT_RELEVANT [LOW] — No clear pension-fertility causal relationship
- Sonnet: RELEVANT [HIGH] — Studies whether Bismarck's social insurance system crowded out private savings using Prussian savings bank data, directly testing the crowdout hypothesis for social security — structurally parallel to pension crowdout of children-as-savings.

**4. Land Use Patterns and Environmental Sustainability** (n.d.)
- Haiku: NOT_RELEVANT [LOW] — No clear pension-fertility causal relationship
- Sonnet: RELEVANT [HIGH] — The foundational Barro-Becker paper reformulating the economic theory of fertility using dynastic utility maximization, explicitly modeling intergenerational transfers and fertility as an endogenous choice — the core theoretical framework underlying the pension-crowdout hypothesis.

**5. Family Size, Economics and Child Gender Preference: A Case Study in the Nyeri District of Kenya** (2003 | DOI: 10.22004/ag.econ.105583)
- Haiku: NOT_RELEVANT [MEDIUM] — Studies fertility but no connection to pensions or old-age security
- Sonnet: RELEVANT [MEDIUM] — Reviews economic theories of fertility in Kenya including the old-age security motive as a reason for high desired family size, directly engaging children as retirement support in a developing country without formal pensions.

**6. Trends and transitions in children's coresidence with older adults in Beijing municipality** (2004 | DOI: 10.31899/pgy2.1024)
- Haiku: NOT_RELEVANT [MEDIUM] — Studies fertility but no connection to pensions or old-age security
- Sonnet: RELEVANT [MEDIUM] — Studies declining coresidence of elderly with adult children in Beijing, examining the erosion of traditional family support for the elderly that forms the structural basis of the old-age security fertility motive in China.

**7. The Inherited Inequality: How Demographic Aging and Pension Reforms can Change the Intergenerational Transmission of Wealth** (n.d.)
- Haiku: NOT_RELEVANT [HIGH] — Studies pension reform effects on inheritance and wealth transmission; reverse causal direction (aging affects pensions, not fertility)
- Sonnet: RELEVANT [MEDIUM] — Analyzes how demographic aging and pension reforms affect intergenerational wealth transmission in OLG-style models; discusses how annuitization and fertility interact to determine bequests and inherited wealth shares, touching on structural equivalence between pension systems and intergenerational transfer motives.

---

## False Positives (Haiku Included, Sonnet Excluded)

40 papers total.

**1. Diminishing America's Demographic Dilemma Through Pre-Funding Social Security** (n.d.)
- Haiku: RELEVANT [HIGH] — Explicit statement: pensions substitute for or affect fertility
- Sonnet: NOT_RELEVANT [HIGH] — OLG model studying how pre-funding Social Security would affect future generations' welfare under demographic transition, with fertility treated as exogenous input rather than an endogenous outcome of pension policy.

**2. Sustainability of Pension Systems in the New EU Member States and Croatia: Coping with Aging Challenges and Fiscal Pressures** (n.d.)
- Haiku: RELEVANT [HIGH] — Explicit statement: pensions substitute for or affect fertility
- Sonnet: NOT_RELEVANT [HIGH] — European pension reform report treating lower fertility as a cause of pension sustainability challenges; reverse causal direction.

**3. Coping with the effects of population ageing on public finances in the European Union and China** (n.d.)
- Haiku: RELEVANT [HIGH] — Explicit statement: pensions substitute for or affect fertility
- Sonnet: NOT_RELEVANT [HIGH] — Analyzes pension reform pressures from aging populations in the EU and China, treating low fertility as a demographic driver of pension sustainability challenges rather than studying pensions as a cause of fertility change.

**4. Key issues in the effectiveness of public financial tools to support childbearing the example of Hungary during the COVID-19 crisis** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies public financial tools supporting childbearing, including state support substituting for private arrangements
- Sonnet: NOT_RELEVANT [MEDIUM] — Studies public financial instruments to encourage childbearing in Hungary; focuses on pro-natalist subsidies rather than old-age security/pension crowdout.

**5. Effects of incentive-based population policies on sustainability of China's recent maternity insurance system reform: a system dynamics simulation** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies how maternity insurance system affects fertility and sustainability
- Sonnet: NOT_RELEVANT [HIGH] — Studies sustainability of China's maternity insurance system under different fertility incentive policies; focuses on financing pro-natalist policies, not pension crowdout.

**6. The Reforms in the Israeli Pension System 1995–2015** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies pension reforms and labor market responses in Israel
- Sonnet: NOT_RELEVANT [HIGH] — Studies Israeli employees' responses to mandatory pension contributions and labor market effects; fertility is not examined.

**7. Shall we have another? Effects of daycare benefits on fertility, a case study in a region in Northeastern Italy** (n.d.)
- Haiku: RELEVANT [HIGH] — Directly studies how public family benefits (daycare subsidies) affect fertility decisions
- Sonnet: NOT_RELEVANT [HIGH] — Studies whether daycare subsidies increase subsequent childbearing in Italy; focuses on childcare costs, not old-age security or pension crowdout.

**8. Paid Childcare Leave, Fertility, and Female Labor Supply in South Korea** (n.d.)
- Haiku: RELEVANT [HIGH] — Directly studies paid childcare leave (government support) effects on fertility and labor supply
- Sonnet: NOT_RELEVANT [MEDIUM] — Studies paid childcare leave effects on fertility and female labor supply in South Korea; focuses on maternity/parental leave policy, not old-age security or pension crowdout.

**9. The Long-Run Effects of California's Paid Family Leave Act on Women's Careers and Childbearing: New Evidence from a Regression Discontinuity Design and US Tax Data** (n.d.)
- Haiku: RELEVANT [HIGH] — Directly tests paid family leave (government support) effects on childbearing and career outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Studies long-run effects of California's Paid Family Leave Act on employment, earnings, and childbearing; focuses on parental leave, not pension or old-age security motives.

**10. How Should Retirement Policy Adjust to the Baby Bust** (n.d.)
- Haiku: RELEVANT [HIGH] — OLG model analyzing optimal retirement policy responses to fertility decline
- Sonnet: NOT_RELEVANT [HIGH] — Studies optimal retirement age and pension policy adjustments to cope with fertility decline; treats low fertility as an exogenous shock that pension policy must respond to, not as an outcome of pension generosity.

**11. Effects of Early Childhood Intervention on Fertility and Maternal Employment: Evidence from a Randomized Controlled Trial** (n.d.)
- Haiku: RELEVANT [HIGH] — Directly tests public childcare intervention effects on fertility and maternal employment
- Sonnet: NOT_RELEVANT [HIGH] — Studies RCT effects of early childhood intervention on subsequent fertility and maternal employment; no pension or old-age security motive component.

**12. Slovakia: Seeking New Approaches to the Sustainability of the Social System in the Impact of Demographic Challenges** (2023 | DOI: 10.54171/2023.nj.sotsss_9)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Reviews Slovak social security law and demographic challenges but treats fertility decline as context for pension sustainability, not as an outcome caused by pensions.

**13. Demographic Dynamics And Sustainability Of Public Pension Expenditures Within European Union-15 Member States** (2012)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Studies how demographic variables including fertility affect pension expenditure sustainability; causal arrow runs from fertility to pension costs, the reverse of what is under review.

**14. Programs without alternative: Public pensions in the OECD** (2001)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Argues for the continued necessity of public pensions in the face of demographic aging, treating falling birth rates as context for pension financing pressures rather than as an outcome of pensions.

**15. [Relationship between fertility policy and family policy].** (1985)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [MEDIUM] — Distinguishes fertility policy from family policy using ISSA definitions but focuses on normative birth-rate regulation rather than the old-age security mechanism linking pensions to fertility.

**16. 3. Social Security, Retirement, and Employment of the Young in Denmark** (2010 | DOI: 10.7208/9780226309507-005)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Studies whether earlier retirement of older workers creates jobs for young workers in Denmark; no connection to fertility or old-age security motives for childbearing.

**17. Number of children and disability pension due to mental and musculoskeletal disorders: A longitudinal register-based study in Norway** (2023 | DOI: 10.1080/00324728.2023.2195847)
- Haiku: RELEVANT [MEDIUM] — Studies pensions and fertility connection
- Sonnet: NOT_RELEVANT [HIGH] — Studies how parity affects disability pension risk; causal direction is reversed from the hypothesis under review.

**18. THE IMPACT OF THE CHILD SUPPORT GRANT ON PARTICIPATION IN THE LABOUR MARKET IN RURAL EASTERN CAPE** (2014 | DOI: 10.15270/49-1-80)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Studies whether the South African child support grant affects labor market participation, not whether pensions affect fertility.

**19. Extending the Scope of ALM to Social Investment: Investing in Population Growth to Enhance Sustainability of the Korean National Pension Service** (2021 | DOI: 10.3390/su13010401)
- Haiku: RELEVANT [MEDIUM] — Studies pensions and fertility connection
- Sonnet: NOT_RELEVANT [HIGH] — Proposes investing pension funds to stimulate population growth as an asset-liability management strategy; causal direction is pension sustainability driving fertility investment, not pension generosity affecting fertility choices.

**20. Simulated Replacement Rates for CPP Reform Options** (2014 | DOI: 10.55016/ojs/sppp.v7i1.42459)
- Haiku: RELEVANT [MEDIUM] — Studies pensions and fertility together
- Sonnet: NOT_RELEVANT [HIGH] — Simulates replacement rates under Canadian Pension Plan reform options for middle-income earners; no connection to fertility decisions.

**21. Spatial Modeling of Social Expenditure in EU Countries** (1970 | DOI: 10.33422/jarss.v2i4.253)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Models spatial patterns of social expenditure in EU countries, treating fertility decline as background context for social policy reform rather than as an outcome of pension generosity.

**22. When Do We Start? Pension reform in aging Japan** (2016)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Simulates pension reform scenarios in Japan to reduce replacement rates given demographic aging; fertility is an exogenous input to pension sustainability projections, not an outcome.

**23. The EU's Regulatory Commitment to a European Harmonized Pension Product (PEPP): The Portability of Pension Rights vis-à-vis the Free Movement of Capital** (2019 | DOI: 10.1093/jfr/fjz005)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Examines regulation of pan-European personal pension products, with fertility decline mentioned only as demographic context for financial market reform.

**24. Working Longer, Learning Longer** (2015 | DOI: 10.1093/ppar/prv025)
- Haiku: RELEVANT [HIGH] — Studies pension/old-age security systems and fertility outcomes
- Sonnet: NOT_RELEVANT [HIGH] — Discusses delaying retirement and extending labor force participation to address demographic aging; fertility decline is background context, not an outcome studied.

**25. Supportive families versus support from families: The decision to have a child in the Netherlands** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies how family support affects fertility decisions, relevant to examining intergenerational support mechanisms that pensions might crowd out
- Sonnet: NOT_RELEVANT [MEDIUM] — Studies how family support (childcare help, financial transfers from kin) affects fertility decisions in the Netherlands; focuses on contemporary informal family support as a fertility determinant, not on children as old-age insurance for parents.

**26. Children's Filial Piety Changes Life Satisfaction of the Left-Behind Elderly in Rural Areas in China?** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies children's support for elderly in context of family separation
- Sonnet: NOT_RELEVANT [HIGH] — Studies how children's filial piety affects elderly life satisfaction in rural China; while related to intergenerational support, does not study fertility decisions or the old-age security motive for childbearing.

**27. The Impact of the New Rural Pension Scheme on Retirement Sustainability in China: Evidences of Regional Differences in Formal and Informal Labor Supply** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies New Rural Pension Scheme impact on labor supply; may indicate behavioral response to pension availability
- Sonnet: NOT_RELEVANT [HIGH] — Evaluates China's rural pension scheme on labor supply and retirement sustainability; outcome variable is labor supply not fertility decisions.

**28. CHILD SUBSIDIES AND THE CROSS-SECTIONAL FERTILITY PATTERN** (n.d.)
- Haiku: RELEVANT [HIGH] — Develops OLG model examining how child subsidies affect fertility patterns
- Sonnet: NOT_RELEVANT [HIGH] — Studies how child subsidies (not pension/old-age security) affect fertility in an OLG model; the policy instrument is childcare subsidies and child tax credits, not pension generosity.

**29. A journey without maps—Understanding the costs of caring for dependent older people in Nigeria, China, Mexico and Peru** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Studies family care costs for elderly in absence of formal systems
- Sonnet: NOT_RELEVANT [MEDIUM] — Studies economic burden of family caregiving for dependent elderly in developing countries; examines caregiving costs rather than old-age security as a motive for fertility.

**30. China's aging population: A review of living arrangement, intergenerational support, and wellbeing** (n.d.)
- Haiku: RELEVANT [MEDIUM] — Reviews intergenerational support and living arrangements in aging China
- Sonnet: NOT_RELEVANT [MEDIUM] — Reviews living arrangements and intergenerational support for elderly in China; focuses on elderly wellbeing rather than how such arrangements affect fertility decisions.

**31. Contribution of demography to economic growth** (2017 | DOI: 10.1007/s13209-017-0164-y)
- Haiku: RELEVANT [MEDIUM] — OLG model with endogenous fertility incorporating educational heterogeneity and life-cycle optimization
- Sonnet: NOT_RELEVANT [HIGH] — OLG model studying demographic change's contribution to economic growth; fertility decline is treated as an exogenous historical fact, not an outcome of old-age security arrangements.

**32. Social differentials in speed-premium effects in childbearing in Sweden** (2005 | DOI: 10.4054/mpidr-wp-2005-027)
- Haiku: RELEVANT [HIGH] — Directly examines how parental-leave allowances affect birth spacing and fertility decisions
- Sonnet: NOT_RELEVANT [HIGH] — Examines how parental-leave allowance rules create incentives for birth spacing (speed premium) in Sweden; unrelated to old-age security or pension crowdout.

**33. Fertility and Labor Supply Responses to Child Allowances: The Introduction of Means-Tested Benefits in France** (2023 | DOI: 10.1215/00703370-10965926)
- Haiku: RELEVANT [HIGH] — Directly examines fertility responses to changes in family allowance benefits
- Sonnet: NOT_RELEVANT [HIGH] — Studies fertility responses to child allowance policies (pronatalist transfers to parents), not old-age security or pension crowdout of the retirement motive for having children.

**34. Social Challenges of the New Pension Reform in the Current Demographic Situation in Rossiya** (2019 | DOI: 10.19181/1999-9836-2019-10054)
- Haiku: RELEVANT [HIGH] — Uses policy variation to estimate causal effect of pension on fertility
- Sonnet: NOT_RELEVANT [HIGH] — Studies social challenges of Russian pension reform in the context of demographic aging, treating falling birth rates as a driver of reform needs rather than studying pension effects on fertility.

**35. An Analysis on Views of Iranian Women about Incentive Policies on Childbearing Decision-making** (2016 | DOI: 10.21276/ambi.2016.03.sp1.ga01)
- Haiku: RELEVANT [MEDIUM] — Tests whether government incentive policies affect childbearing desires
- Sonnet: NOT_RELEVANT [HIGH] — Examines women's views on pro-natalist incentive policies affecting childbearing, not the role of pension or old-age security systems in reducing fertility.

**36. Trade-Offs in Children's Time Allocation: Mixed Support for Embodied Capital Models of the Demographic Transition in Tanzania** (2018 | DOI: 10.1086/699880)
- Haiku: RELEVANT [MEDIUM] — Tests embodied capital theory linking parental investment in child education to fertility transitions
- Sonnet: NOT_RELEVANT [HIGH] — Uses embodied capital theory and schooling opportunity costs to explain fertility transitions in Tanzania; no old-age security or pension component.

**37. Some State Financial Segments of the Childbirth and Family Support System in Slovakia** (2021 | DOI: 10.35551/pfq_2021_4_2)
- Haiku: RELEVANT [MEDIUM] — Analyzes government childbirth and family support systems in Slovakia
- Sonnet: NOT_RELEVANT [HIGH] — Analyzes pro-natalist tax and financial support instruments for childbearing in Slovakia, not pension systems as substitutes for children as old-age security.

**38. Housing Wealth, Fertility, and Child Quality** (2022 | DOI: 10.53383/100334)
- Haiku: RELEVANT [HIGH] — Directly tests wealth effects on fertility and child quality; housing wealth as substitute for intergenerational transfers similar to pension-crowdout mechanism
- Sonnet: NOT_RELEVANT [HIGH] — Studies how housing wealth changes affect fertility and child quality in China, focusing on wealth effects rather than old-age security or pension crowdout mechanisms.

**39. The Sensitivity of Family-Related Behaviors to Economic and Social Turbulence in Post-Socialist Countries, 1970-2010** (2023 | DOI: 10.12765/cpos-2023-19)
- Haiku: RELEVANT [MEDIUM] — Tests sensitivity of family events to economic and institutional transitions in post-socialist countries where pension systems changed
- Sonnet: NOT_RELEVANT [MEDIUM] — Examines how post-socialist economic transitions affected family formation behaviors including fertility across Eastern Europe and Central Asia, but does not specifically focus on pension system availability as a cause of fertility change.

**40. Women's Career Strategy Choices and Fertility in Finland** (2013 | DOI: 10.23979/fypr.40931)
- Haiku: RELEVANT [MEDIUM] — Tests association between women's career strategies and fertility; family policy context influences fertility choices
- Sonnet: NOT_RELEVANT [HIGH] — Studies the association between women's labor market career strategies and fertility in Finland; no pension or old-age security mechanism analyzed.

---

## Haiku Confusion (UNCERTAIN When Sonnet Was Decisive)

76 papers total. Representative examples below.

**1. The Impact of the Demographic Ice Age on Economic Growth, Public Policy, and the Sustainability of Pension Systems** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Treats declining fertility as a cause of pension sustainability challenges rather than pensions causing fertility change; reverse causal direction.

**2. The pension system in China: an empirical study of the money's worth ratio of annuities** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Studies the actuarial value of annuities in China's pension system; mentions low fertility and aging as demographic context but does not study pensions as a cause of fertility change.

**3. Le ricadute dell'invecchiamento della popolazione sul Welfare, sul mercato del lavoro e sulla solidarietà intergenerazionale** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Italian paper on population aging and welfare discussing pension spending and birth rate as a challenge but treating fertility decline as given demographic context.

**4. Early Life Origins of All-Cause and Cause-Specific Disability Pension: Findings from the Helsinki Birth Cohort Study** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Epidemiological study examining birth weight as a predictor of disability pension uptake in adulthood; no connection to fertility decisions or old-age security motives.

**5. Making provision for ageing populations.** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — OECD policy article treating low birth rates as a cause of aging population challenges for pension financing, not studying pensions as a cause of fertility change.

**6. China will get rich before it grows old.** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Analyzes China's demographic dividend with low fertility and aging as demographic context, not studying pension effects on fertility decisions.

**7. Demographics and the pension system.** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Italian demographic overview using low fertility and population aging as context for pension system challenges; treats fertility as a cause of pension financing problems, not the reverse.

**8. Lithuanian pension system: Alternatives and proposals for the future. A summary report by The Phare Study Group** (n.d.)
- Haiku: UNCERTAIN [LOW] — Both pension and fertility mentioned but causal direction unclear
- Sonnet: NOT_RELEVANT [HIGH] — Policy report on Lithuanian pension reform treating declining fertility as a demographic challenge for pension sustainability, not studying pensions as a cause of fertility change.

**9. WP 2017-358** (n.d.)
- Haiku: UNCERTAIN [LOW] — Title truncated and abstract cut off; appears to discuss Chilean pension system but cannot assess fertility relevance
- Sonnet: NOT_RELEVANT [MEDIUM] — Appears to analyze Chile's privatized pension system performance; focuses on pension adequacy and coverage, not effects on fertility or old-age security motives.

**10. Do means-tested benefits reduce the demand for annuities? - Evidence from Switzerland** (n.d.)
- Haiku: UNCERTAIN [MEDIUM] — Studies how old-age income floors affect savings and annuity demand; related to old-age security but unclear if fertility is addressed
- Sonnet: NOT_RELEVANT [HIGH] — Studies how means-tested old-age benefits affect demand for pension annuities in Switzerland; no connection to fertility or childbearing.

**11. Institutional Design and Incentives for Migrant Workers to Participate in Social Insurance in China: Evidence From a Policy Experiment in Chengdu City** (n.d.)
- Haiku: UNCERTAIN [MEDIUM] — Studies social insurance participation by migrant workers; may involve old-age insurance but unclear if fertility effects studied
- Sonnet: NOT_RELEVANT [HIGH] — Studies migrant worker participation in social insurance in China; no connection to fertility or old-age security motives for childbearing.

**12. The Life-Cycle Effects of Pension Reforms: A Structural Approach** (n.d.)
- Haiku: UNCERTAIN [MEDIUM] — Structural lifecycle model of pension reform effects; may include fertility as endogenous choice variable
- Sonnet: NOT_RELEVANT [HIGH] — Estimates life-cycle welfare effects of Italian pension reforms on saving, portfolio choice, and retirement timing; fertility is not modeled as an endogenous outcome.

**13. OECD Reviews of Labour Market and Social Policies: Russian Federation 2011** (2011 | DOI: 10.1787/9789264118720-en)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Broad labor market and social policy review of Russia; fertility effects of pensions are not a focus.

**14. ARE ELDERLY PEOPLE LIVING IN OLD-AGE HOME, LESS DEPRESSED THAN THOSE OF COMMUNITY? FINDINGS FROM A COMPARATIVE STUDY** (2012)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Compares depression rates among elderly in old-age homes versus community settings in Nepal; no connection to fertility or pension effects.

**15. Winning the War: Poverty from the Great Society to the Great Recession** (2013 | DOI: 10.3386/w18718)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Examines long-run US poverty trends and anti-poverty program effectiveness; no focus on pensions affecting fertility.

**16. The Case Against Intergenerational Accounting: The Accounting Campaign Against Social Security and Medicare** (2009)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Critiques intergenerational accounting methods applied to federal budgeting; no connection to fertility or old-age security motives for childbearing.

**17. The willingness and influencing factors to choose institutional elder care among rural elderly: an empirical analysis based on the survey data of Shandong Province** (2024 | DOI: 10.1186/s12877-023-04615-5)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Studies acceptance of institutional care by rural elderly in China; fertility is not an outcome variable.

**18. China's uncertain demographic present and future** (2007 | DOI: 10.1553/populationyearbook2007s37)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Collection of essays on European and Chinese demographic futures, treating fertility decline as a demographic fact rather than studying pension effects on fertility.

**19. The Fiscal Consequences of Shrinking and Ageing Populations** (2017 | DOI: 10.1007/s12126-017-9306-6)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Study of fiscal consequences of demographic decline, treating fertility as a cause of fiscal pressure; the reverse of the hypothesis under review.

**20. The Pandemic in India and Its Impact on Footloose Labour** (2020 | DOI: 10.1007/s41027-020-00285-8)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Studies the impact of COVID-19 on migrant labor in India; no connection to fertility or pensions.

**21. Where Is the Money? The Intersectionality of the Spirit World and the Acquisition of Wealth** (2019 | DOI: 10.3390/rel10030146)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Theoretical treatment of spiritual economies and cybercrime in Nigeria; entirely unrelated to pensions or fertility.

**22. State of the art of Indonesian agriculture and the introduction of innovation for added value of cassava** (2020 | DOI: 10.1007/s11816-020-00605-w)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Paper about agricultural innovation for cassava in Indonesia; entirely unrelated to pensions or fertility.

**23. European Populations** (1999 | DOI: 10.1007/978-94-010-9022-3)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [LOW] — Appears to be a reference book on European populations; without an abstract, unclear whether it covers pension effects on fertility, but the broad demographic scope makes it unlikely to be specifically relevant.

**24. Forms of wealth and parent-offspring conflict** (1979 | DOI: 10.1016/0140-1750(79)90021-6)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: RELEVANT [MEDIUM] — Directly addresses parental motivations for having children including children as a form of wealth or old-age security in the context of parent-offspring conflict; structurally central to the Caldwell wealth-flows model relevant to this review.

**25. Work and Family Directions in the USA and Australia: A Policy Research Agenda** (2007 | DOI: 10.1177/0022185607072241)
- Haiku: UNCERTAIN [LOW] — Insufficient information to assess relevance clearly
- Sonnet: NOT_RELEVANT [HIGH] — Comparative paper on work-family policy in Australia and the USA focusing on care gaps and labor market participation, not on pension-fertility mechanisms.

---

## Pattern Analysis

### False Negatives: What Haiku Missed

The 7 false negatives cluster into three recognizable patterns.

**Pattern 1: Papers where the pension-crowdout mechanism is implicit or structurally embedded, not surface-level.** Haiku consistently assigned NOT_RELEVANT when the title contained no lexical cues to pensions or old-age security — even when the paper was centrally about the theoretical or empirical relationship between formal eldercare systems and childbearing. Examples: *Land Use Patterns and Environmental Sustainability* (actually the Barro-Becker dynastic utility paper) and *Insurance Markets and Adverse Selection* (actually a Bismarck crowdout test using Prussian savings data). Haiku appears to have been screening on title vocabulary rather than inferring the relevance of the content from context clues in the abstract.

**Pattern 2: Papers on children-as-old-age-support in developing or transitional settings without formal pensions.** Haiku missed both the Kenya fertility study (FN 5) and the Beijing coresidence paper (FN 6), each of which engages the old-age security motive directly but through the lens of what happens in the *absence* of formal pensions — the structural complement to the crowdout hypothesis. These papers document the mechanism that pensions are hypothesized to displace. Haiku treated "no pension mentioned" as disqualifying.

**Pattern 3: OLG or intergenerational transfer papers where fertility is an endogenous channel rather than the explicit outcome variable.** FN 2 (*Fiscal Decentralization and Public Service Delivery*, an OLG model linking delayed retirement to birth rates) and FN 7 (*The Inherited Inequality*, which studies annuitization and fertility interactions in OLG models) both address the crowdout mechanism at a structural level. Haiku flagged these as reverse-direction or off-topic because "fertility" was not the headline outcome, even though the fertility channel was modeled.

### Summary of Haiku Confusion (UNCERTAIN, Sonnet Decisive)

The bulk of the 76 confusion papers share a single pattern: co-occurrence of "pension" and "fertility/birth rate" as demographic context for pension sustainability papers, where the causal arrow runs from fertility to pension costs, not from pensions to fertility choices. Haiku was appropriately uncertain about causal direction from title and abstract cues alone; Sonnet resolved these decisively as NOT_RELEVANT by identifying which variable was endogenous. One true positive was recovered from the confusion set: *Forms of wealth and parent-offspring conflict* (1979), which Sonnet correctly classified as RELEVANT for its treatment of children as a form of parental wealth accumulation.

---

## Prompt Revision Suggestions

**Change 1: Add a positive cue for structural mechanism papers where pensions are implicit.**

*Current:* [Assume prompt includes language like: "Mark RELEVANT if the paper studies whether pensions or formal old-age security reduces fertility, or reduces the demand for children as old-age support."]

*Revised:* Append — "Also mark RELEVANT if the paper provides foundational theoretical framework for the pension-crowdout mechanism (e.g., dynastic utility models, intergenerational transfer theory, wealth-flows models) even if pensions are not named explicitly, OR if it empirically tests whether any formal insurance system crowds out private precautionary saving in a context structurally parallel to children-as-savings."

*Rationale:* Catches FN 1 (OAS/informal transfer asymmetry), FN 3 (Bismarck crowdout of private savings), and FN 4 (Barro-Becker dynastic utility paper), all of which were missed because the titles were misleading and Haiku did not infer structural relevance from abstract content.

**Change 2: Add a positive cue for developing-country or pre-pension settings where the old-age security motive is documented in the absence of formal pensions.**

*Current:* [Assume prompt focuses on formal pension systems as the treatment variable.]

*Revised:* Append — "Also mark RELEVANT if the paper documents children-as-old-age-support as a fertility motive in a setting with weak or absent formal pension coverage (e.g., sub-Saharan Africa, rural China, pre-transition societies), since such papers establish the baseline mechanism that formal pensions are hypothesized to crowd out."

*Rationale:* Catches FN 5 (Kenya old-age security motive review) and FN 6 (Beijing coresidence erosion) — both directly relevant to the hypothesis but missed because no formal pension system was the studied treatment.

**Change 3: Add a negative cue explicitly excluding pension sustainability papers where fertility is an exogenous input.**

*Current:* [Assume prompt identifies reverse-direction as exclusion criterion, but without enough precision.]

*Revised:* Append — "Mark NOT_RELEVANT if the paper's central question is how low fertility or population aging creates fiscal challenges for pension systems (fertility → pension sustainability), even if both pensions and fertility rates appear prominently. The hypothesis under review requires pensions to be the cause and fertility to be the outcome, not the reverse."

*Rationale:* Would reduce FP rate substantially. The single largest FP pattern — 15+ papers on EU/OECD/Japan/Russia pension sustainability treating fertility as a demographic input — would be captured by this exclusion rule. Also reduces Haiku confusion on the 76-paper uncertain set, most of which share this exact reverse-direction structure.

---

## Recommendation

Stopping criterion met — Haiku FN rate is 0.7%, well below the 3% threshold; proceed to full batch run using the routing rule specified in routing-rule.md, optionally incorporating the three prompt revisions above before the production run to further reduce false positive rate.
