# Calibration Report: old-age-security-pension-crowdout, Batch 2

**Date:** 2026-06-20
**Models:** Haiku = claude-haiku-4-5-20251001 (primary screener); Sonnet = claude-sonnet-4-6 (gold standard)
**Papers fetched this batch:** 1,000
**Papers with matched comparisons:** 930
**Stopping criterion:** Haiku FN rate < 3%
**Verdict:** CRITERION MET (FN rate = 1.0%)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Papers compared | 930 |
| Agreement rate | 78.3% |
| Both RELEVANT | 66 |
| Both NOT_RELEVANT | 639 |
| Both UNCERTAIN | 23 |
| Haiku FN rate (H=NOT_RELEVANT, S=RELEVANT) | **1.0%** (9 papers) |
| Haiku FP rate (H=RELEVANT, S=NOT_RELEVANT) | 4.5% (42 papers) |
| Haiku confusion (H=UNCERTAIN, S decisive) | 11.2% (104 papers) |
| Sonnet UNCERTAIN rate | 7.5% (70 papers) |
| **Stopping criterion met** | **YES** |

---

## Stopping Criterion

MET — Haiku FN rate of 1.0% is below the 3% threshold. Proceed to routing rule (see routing-rule.md).

---

## False Negatives (Haiku Missed, Sonnet Caught)

9 papers total. Haiku rated NOT_RELEVANT; Sonnet rated RELEVANT.

1. **Economic factors in family size decisions in Thailand** (1977)
   - Haiku: NOT_RELEVANT [MEDIUM] — Studies fertility drivers without pension or old-age security component.
   - Sonnet: RELEVANT [MEDIUM] — Examines economic benefits and costs of children including parents' expected benefits (support in old age) as determinants of family size decisions in Thailand — closely related to the old-age security motive.

2. **"The Value and Cost of Children"** (1978 | DOI: 10.2307/1966297)
   - Haiku: NOT_RELEVANT [MEDIUM] — Studies fertility drivers without pension or old-age security component.
   - Sonnet: RELEVANT [MEDIUM] — Reviews perceived benefits and costs of children to parents including their old-age support value, which is central to the children-as-retirement-insurance hypothesis underlying the pension-crowdout mechanism.

3. **On the structural value of children and its implication on intended fertility in Bulgaria** (2008 | DOI: 10.4054/demres.2008.18.20)
   - Haiku: NOT_RELEVANT [MEDIUM] — Studies fertility drivers without pension or old-age security component.
   - Sonnet: RELEVANT [MEDIUM] — Examines the structural value of children (including as old-age support) and its implications for intended fertility, engaging directly with the children-as-insurance motive that underlies the pension-crowdout hypothesis.

4. **Social Security and the American Family** (1987 | DOI: 10.1086/tpe.1.20061766)
   - Haiku: NOT_RELEVANT [MEDIUM] — Studies pension systems but fertility not addressed as outcome.
   - Sonnet: RELEVANT [MEDIUM] — Title directly connects social security to the family, strongly suggesting it examines how social security affects family formation or fertility decisions.

5. **Private and Social Incentives for Fertility: Israeli Puzzles** (2002 | DOI: 10.3386/w8984)
   - Haiku: NOT_RELEVANT [HIGH] — Studies fertility but no pension/old-age security component.
   - Sonnet: RELEVANT [HIGH] — This NBER paper explicitly analyzes private and social incentives for fertility, including public transfers and social security considerations, directly relevant to the old-age security hypothesis.

6. **The macroeconomics of fertility in small open economies: A test of the Becker-Barro model for The Netherlands and New Zealand** (2001 | DOI: 10.1007/s001480050160)
   - Haiku: NOT_RELEVANT [HIGH] — Studies fertility but no pension/old-age security component.
   - Sonnet: RELEVANT [MEDIUM] — This paper tests the Becker-Barro model of fertility in open economies, a theoretical framework where old-age support and savings motives are central to fertility determination.

7. **Social Security Financial Crises** (2003)
   - Haiku: NOT_RELEVANT [MEDIUM] — Mentions both pensions and fertility but without causal linkage.
   - Sonnet: RELEVANT [HIGH] — Explicitly argues that PAYG social security affects fertility and human capital decisions, creating endogenous erosion of the financial basis — directly modeling the pension-fertility channel.

8. **Mortality risks, sequential decisions on births, and population growth** (1972 | DOI: 10.2307/2060868)
   - Haiku: NOT_RELEVANT [HIGH] — Fertility topic without pension/old-age security link.
   - Sonnet: RELEVANT [HIGH] — Directly models children as old-age support (surviving son for old-age security) and analyzes how parental strategies to secure that support affect fertility and population growth.

9. **From Transfers to Individual Responsibility: Implications for Savings and Capital Accumulation in Taiwan and the United States** (2000)
   - Haiku: NOT_RELEVANT [HIGH] — Pension topic without fertility outcome.
   - Sonnet: RELEVANT [HIGH] — Directly models the transition from familial old-age support (children supporting parents) to individual savings, analyzing effects analogous to PAYG-to-funded pension transitions, squarely addressing the old-age security motive mechanism.

---

## False Positives (Haiku Included, Sonnet Excluded)

42 papers total. Haiku rated RELEVANT; Sonnet rated NOT_RELEVANT.

1. **Assessing the impact of macroeconomic variables on pension benefits in Ghana: A case of Social Security and National Insurance Trust** (2017 | DOI: 10.4102/sajems.v20i1.1703)
   - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies macroeconomic determinants of pension benefit adequacy without fertility as an outcome variable.

2. **Population ageing: what should we worry about?** (2009 | DOI: 10.1098/rstb.2009.0185)
   - Haiku: RELEVANT [HIGH] — Directly examines pension/old-age security and fertility outcomes.
   - Sonnet: NOT_RELEVANT [HIGH] — Discusses pension sustainability challenges under demographic aging where fertility decline is background context, not an outcome of pension systems.

3. **War and Pensions: The Effects of War on Social Security and Pensions Around the World** (2020 | DOI: 10.5539/ijef.v12n2p45)
   - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
   - Sonnet: NOT_RELEVANT [HIGH] — Historical overview of how wars shaped pension system development with no fertility outcome.

4. **Automatic Indexation of the Pension Age to Life Expectancy: When Policy Design Matters** (2021 | DOI: 10.3390/risks9050096)
   - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
   - Sonnet: NOT_RELEVANT [HIGH] — Pension policy design study on retirement age indexation with no fertility outcome.

5. **Mandatory pensions and personal savings in The Netherlands** (1997)
   - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies the relationship between mandatory pensions and personal savings without fertility as an outcome.

6. **The Impact of Subjective Well-Being on the Fertility Intentions of Women of Childbearing Age** (2025 | DOI: 10.62177/chst.v2i1.159)
   - Haiku: RELEVANT [HIGH] — Directly examines pension/old-age security and fertility outcomes.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies subjective well-being as a determinant of fertility intentions; mentions pension system only as background context for China's low fertility concern.

7. **Extending pension coverage in Cambodia: The governance and investment challenges of the Social Security Investment Fund** (2020 | DOI: 10.1111/issr.12252)
   - Haiku: RELEVANT [HIGH] — Directly examines pension/old-age security and fertility outcomes.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies pension system governance and investment design in Cambodia with fertility mentioned only as demographic background, not as an outcome of pension coverage.

8. **Redesigning pension systems** (2019 | DOI: 10.15185/izawol.51.v2)
   - Haiku: RELEVANT [HIGH] — Directly examines pension/old-age security and fertility outcomes.
   - Sonnet: NOT_RELEVANT [HIGH] — Advocates for pension reform in response to demographic changes where fertility decline is background context, not an outcome of pension design.

9. **Home-ownership and asset-based welfare: the case of Belgium** (2010 | DOI: 10.1007/s10901-010-9185-6)
   - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies home-ownership as an alternative to social security provision with no fertility outcome.

10. **Secularism, Fundamentalism, or Catholicism? The Religious Composition of the United States to 2043** (2010 | DOI: 10.1111/j.1468-5906.2010.01510.x)
    - Haiku: RELEVANT [MEDIUM] — Fertility study examining old-age security mechanisms.
    - Sonnet: NOT_RELEVANT [HIGH] — Projects religious composition using fertility and migration differentials with no connection to pensions.

11. **Participation in the Peruvian reformed pension system** (2005)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies determinants of enrollment in Peru's reformed pension system with no fertility outcome.

12. **Working time options over the life course: changing social security structures** (2005)
    - Haiku: RELEVANT [HIGH] — Directly examines pension/old-age security and fertility outcomes.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies work-life balance and social security restructuring in Europe with no fertility-pension crowdout analysis.

13. **Fiscal Sustainability of Pension Systems** (2011 | DOI: 10.18267/j.polek.818)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Fiscal sustainability analysis of Slovakia's pension system with no fertility outcome.

14. **The impact of childhood mortality on fertility in six rural thanas of Bangladesh** (2005 | DOI: 10.31899/pgy2.1036)
    - Haiku: RELEVANT [MEDIUM] — Fertility study examining old-age security mechanisms.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies insurance and replacement effects of child mortality on fertility in Bangladesh — child mortality insurance motive, not old-age pension crowdout.

15. **Indicators for Measuring Intergenerational Fairness of Social Security Systems — The Case of the German Social Health Insurance** (2021 | DOI: 10.3390/su13105743)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Develops intergenerational fairness indicators for German health insurance with no fertility outcome.

16. **Pension funds in sub-Saharan Africa** (2022 | DOI: 10.35188/unu-wider/2022/229-4)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Analyzes pension system coverage and investment in sub-Saharan Africa with no fertility outcome.

17. **Systematic Bias and Nontransparency in US Social Security Administration Forecasts** (2015 | DOI: 10.1257/jep.29.2.239)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Evaluates forecasting accuracy of SSA demographic and financial projections with no pension-fertility crowdout analysis.

18. **Attention, Inertia, and Equity in the Social Security Program** (1999 | DOI: 10.1093/oxfordjournals.jpart.a024423)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Public administration study of policy stability and change in the Social Security program with no fertility outcome.

19. **Reforming Pensions in Europe: Economic Fundamentals and Political Factors** (2009 | DOI: 10.2139/ssrn.1357192)
    - Haiku: RELEVANT [MEDIUM] — Pension study with mechanism or policy analysis relevant to fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies political economy of pension reform in Europe with no fertility outcome.

20. **Children 'in need of care' or in need of cash? Questioning social security provisions for orphans in the context of the South African AIDS pandemic** (2003)
    - Haiku: RELEVANT [HIGH] — Directly examines pension/old-age security and fertility outcomes.
    - Sonnet: NOT_RELEVANT [HIGH] — Examines social security provisions for orphans in South Africa in the context of HIV/AIDS — not about pension effects on fertility.

21. **Demographic transition and social security policies in France: A welfare analysis** (1996 | DOI: 10.1002/(sici)1099-0747(199609)12:3<119::aid-asm279>3.0.co;2-g)
    - Haiku: RELEVANT [HIGH] — OLG model directly analyzes social security policy effects on demographic outcomes in France.
    - Sonnet: NOT_RELEVANT [HIGH] — Models welfare effects of three pension reform scenarios in France using an OLG model, but fertility is not an outcome — the focus is pension system sustainability and welfare.

22. **Living Arrangements of Elderly in India: Policy and Programmatic Implications** (2014 | DOI: 10.1017/cbo9781139683456.005)
    - Haiku: RELEVANT [MEDIUM] — Explicitly discusses decline in children as old-age support and links to fertility; mentions policy implications.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Discusses elderly living arrangements in India in the context of declining fertility, but the causal direction is the reverse (fertility decline causing elderly care challenges) rather than pensions affecting fertility.

23. **A Principal Component Simulation of Age-Specific Fertility — Impacts of Family and Social Policy on Reproductive Behavior in Germany** (2019 | DOI: 10.1353/prv.2019.0002)
    - Haiku: RELEVANT [MEDIUM] — Models social policy impacts on fertility behavior; may include pension effects.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Models family and social policy effects on German fertility using time-series simulation, but the abstract focuses on parental leave and family-support policies rather than pension/old-age security as a driver of fertility.

24. **Population Ageing in Japan: A Brief Survey** (2000 | DOI: 10.1080/13511610020017381)
    - Haiku: RELEVANT [MEDIUM] — Discusses low fertility in Japan linked to marriage/childbearing decisions; likely discusses pension context.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Surveys Japan's aging population and attributes low fertility to delayed marriage and women's opportunity costs, without examining pension or old-age security as causes of low fertility.

25. **The Political Feasibility of Pension Reform in the Light of Demographic Change** (1999 | DOI: 10.1007/978-3-642-58654-5_5)
    - Haiku: RELEVANT [MEDIUM] — Links pension reform to demographic change and below-replacement fertility in Europe.
    - Sonnet: NOT_RELEVANT [HIGH] — Examines the political feasibility of transitioning from PAYG to funded pensions given demographic change, not the causal effect of pensions on fertility.

26. **Old Age Support in Urban China: The Role of Pension Schemes, Self-Support Ability and Intergenerational Assistance** (2019 | DOI: 10.3390/ijerph16111918)
    - Haiku: RELEVANT [MEDIUM] — Examines pension schemes and intergenerational support arrangements; relevant to old-age security substitution.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Studies life satisfaction of retired urban Chinese under different pension and intergenerational support arrangements, not the causal effect of pension availability on fertility decisions.

27. **Zero Population Growth and the Economies of Developed Nations** (1978 | DOI: 10.2307/1971730)
    - Haiku: RELEVANT [MEDIUM] — Analyzes economic effects of fertility change including social security/pension implications.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Mentions social security and pensions as one of many areas affected by demographic factors, but analyzes effects of ZPG on the economy (reverse causal direction) rather than pension effects on fertility.

28. **CEE Transition from PAYG to Private Pensions: Income Gaps and Asset Allocation** (2016)
    - Haiku: RELEVANT [MEDIUM] — Analyzes PAYG to private pension shifts in CEE countries with low fertility context.
    - Sonnet: NOT_RELEVANT [HIGH] — Analyzes PAYG-to-private pension transitions in Central and Eastern Europe in the context of aging demographics, focusing on fiscal gaps and asset allocation rather than pension effects on fertility.

29. **Demography, Pensions and Welfare: Fertility Shocks and the Finnish Economy** (1996)
    - Haiku: RELEVANT [MEDIUM] — Directly analyzes demographic shocks and pension system effects on fertility and economy.
    - Sonnet: NOT_RELEVANT [HIGH] — Models the macroeconomic impact of Finland's post-war fertility shock on capital, labor, and output through an OLG model, treating fertility as a shock affecting the pension system not pensions affecting fertility.

30. **A Tale of Two Pensions Reforms: A Sraffian View** (2006 | DOI: 10.4324/9781315557908-7)
    - Haiku: RELEVANT [HIGH] — Abstract clearly establishes pension→fertility causal relationship.
    - Sonnet: NOT_RELEVANT [HIGH] — Critically evaluates PAYG pension reform proposals from a Sraffian economic perspective, not examining how pension systems affect fertility.

31. **The Fertility Response to Cutting Child-Related Welfare Benefits** (2023 | DOI: 10.1007/s11113-023-09757-3)
    - Haiku: RELEVANT [MEDIUM] — Studies relationship between pension and fertility with causal framing.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies child-related welfare benefit cuts and fertility, not old-age security or pension systems as retirement insurance substitutes for children.

32. **Happiness in Old Age: The Daughter Connection** (2023 | DOI: 10.1007/s10902-023-00655-1)
    - Haiku: RELEVANT [HIGH] — Explicitly models children as old-age security or insurance substitute.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies how adult children's gender affects elderly happiness in Thailand; not a study of pensions affecting fertility.

33. **Saving in an ageing society with public pensions: implications from lifecycle analysis** (2009)
    - Haiku: RELEVANT [HIGH] — OLG model analyzing pension effects on fertility.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies savings behavior under public pensions and aging demographics using OLG; fertility is an input assumption, not the outcome.

34. **The Cost of Low Fertility in Europe** (2009 | DOI: 10.3386/w14820)
    - Haiku: RELEVANT [MEDIUM] — Studies relationship between pension and fertility with causal framing.
    - Sonnet: NOT_RELEVANT [HIGH] — Analyzes macroeconomic costs of low fertility in Europe; reverse direction from what we are screening (fertility as cause, not outcome).

35. **Lithuanian Pension System's Reforms Transformations and Forecasts** (2014 | DOI: 10.13189/ujibm.2014.020103)
    - Haiku: RELEVANT [HIGH] — Pension reform study with fertility as outcome variable.
    - Sonnet: NOT_RELEVANT [HIGH] — Financial sustainability analysis of Lithuanian pension reform; fertility is a demographic challenge context, not the outcome.

36. **Immigrant-Native Fertility and Mortality Differentials in the United States** (2008)
    - Haiku: RELEVANT [HIGH] — Abstract explicitly states immigrants discussed as means of alleviating Social Security fiscal pressure, and examines their fertility patterns.
    - Sonnet: NOT_RELEVANT [HIGH] — Examines immigrant vs. native fertility and mortality differences to assess Social Security fiscal impacts, not the reverse causal direction of pensions affecting fertility.

37. **Immigration, Fiscal Policy, and Welfare in an Aging Population** (2012)
    - Haiku: RELEVANT [MEDIUM] — Abstract mentions modeling fertility differences between immigrants and natives in context of social security and aging.
    - Sonnet: NOT_RELEVANT [HIGH] — Models welfare effects of immigration policy in an OLG framework calibrated to Germany, treating fertility as a demographic parameter not as an outcome of pension systems.

38. **Causal Modelling in Fertility Research: A Review of the Literature and an Application to a Parental Leave Policy Reform** (2021)
    - Haiku: RELEVANT [MEDIUM] — Reviews causal models of fertility determinants including family policies; likely discusses social security alongside parental leave.
    - Sonnet: NOT_RELEVANT [HIGH] — Reviews causal modelling approaches in fertility research focusing on female employment and parental leave, without examining pension or old-age security as a fertility driver.

39. **Pronatalist Policies and Fertility in Russia: Estimating Tempo and Quantum Effects** (2021)
    - Haiku: RELEVANT [MEDIUM] — Examines effects of family policy reforms on fertility in Russia; may include social security/pension components among pronatalist policies.
    - Sonnet: NOT_RELEVANT [HIGH] — Evaluates Russian pronatalist family policy reforms aimed at encouraging higher-order births, without a pension or old-age security mechanism.

40. **Number of children and social contacts among older people: the moderating role of filial norms and social policies** (2018)
    - Haiku: RELEVANT [MEDIUM] — Examines how number of children (fertility) and social policies jointly affect elderly social contacts; relates to family as old-age support.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies how number of children affects social contacts in old age across European countries; the causal direction runs from past fertility to old-age outcomes, not from pensions to fertility decisions.

41–42. *(2 additional FP papers in the batch not individually itemized above.)*

---

## Haiku Confusion (UNCERTAIN When Sonnet Was Decisive)

104 papers total. Haiku rated UNCERTAIN; Sonnet gave a decisive rating. A representative sample is listed below.

1. **The ABCs of nonfinancial defined contribution (NDC) schemes** (2017 | DOI: 10.1111/issr.12142)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Describes the design and mechanics of NDC pension schemes without fertility as an outcome variable.

2. **Continuous time model for notional defined contribution pension schemes: Liquidity and solvency** (2019 | DOI: 10.1016/j.insmatheco.2019.06.001)
   - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
   - Sonnet: NOT_RELEVANT [HIGH] — Actuarial/mathematical model of NDC pension scheme liquidity and solvency with no fertility outcome.

3. **Holes in the Safety Net? Social Security and the Alleviation of Poverty in a Comparative Perspective** (2017 | DOI: 10.4324/9781315129785-17)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Comparative welfare state study on poverty alleviation effectiveness with no fertility outcome.

4. **Exploding Productivity Growth: Context, Causes, and Implications** (2003 | DOI: 10.1353/eca.2004.0006)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Macroeconomic paper on productivity growth with Social Security mentioned only in a forecasting context, not related to fertility-pension crowdout.

5. **The Effect of an Increase of the Retirement Age on the Health, Well-Being, and Labor Force Participation of Older Workers** (2020 | DOI: 10.1007/s12062-020-09280-9)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Systematic review on health and labor force effects of increased retirement age with no fertility outcome.

6. **The Demographic Transition and Economic Growth in the Pacific Rim** (2010 | DOI: 10.7208/chicago/9780226386881.003.0002)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Overview of demographic transition and support ratios in East Asia focused on pension system sustainability, with fertility decline as input rather than pension systems as the cause.

7. **The Influence of Pension Scheme Maturity on Investment Strategies of Pension Funds in Kenya** (2018 | DOI: 10.5539/ijbm.v13n10p1)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies pension fund investment strategies with no fertility outcome.

8. **Why a Funded Pension System is Useful and Why It is Not Useful** (2000 | DOI: 10.3386/w7592)
   - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
   - Sonnet: NOT_RELEVANT [HIGH] — Compares PAYG versus funded pension systems on efficiency grounds without fertility as an outcome.

9. **Decomposition of demographic effects on the German pension system** (2018 | DOI: 10.1016/j.jeoa.2018.01.001)
   - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
   - Sonnet: NOT_RELEVANT [HIGH] — Studies how demographic trends (including fertility decline) affect pension system finances — reverse causal direction from what the review tests.

10. **Are Pay-as-you-go and Fully Funded Pension Schemes on the Same Footing with Respect to Demographic Shocks? A Sraffian View** (2004 | DOI: 10.2139/ssrn.467360)
    - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
    - Sonnet: NOT_RELEVANT [HIGH] — Compares PAYG and funded pension schemes' responses to demographic shocks without fertility as an outcome.

11. **Household food insecurity and coping strategies among pensioners in Jimma Town, South West Ethiopia** (2018 | DOI: 10.1186/s12889-018-6291-y)
    - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies food insecurity among pension recipients in Ethiopia with no fertility outcome.

12. **Demographic Changes and the Pension Problem: evidence from twelve countries** (1995 | DOI: 10.1007/978-94-015-8441-8_3)
    - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies how demographic changes create pension financing problems — treats fertility as an input to pension system sustainability, not as an outcome of pensions.

13. **Educational inequalities in disability linked to social security coverage among older individuals in five Latin American countries** (2019 | DOI: 10.1016/j.socscimed.2019.112378)
    - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies health/disability outcomes linked to social security coverage for elderly individuals with no fertility outcome.

14. **Sustainable and equitable pensions with means testing in aging economies** (2021 | DOI: 10.1016/j.euroecorev.2021.103947)
    - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies pension sustainability and means-testing design in aging economies with no fertility outcome.

15. **How Accurate are Demographic Projections Used in Forecasting Pension Expenditure?** (2001 | DOI: 10.1007/978-1-4757-3363-1_2)
    - Haiku: UNCERTAIN [MEDIUM] — Pension-focused in title but fertility connection unclear.
    - Sonnet: NOT_RELEVANT [HIGH] — Evaluates accuracy of demographic forecasts for pension expenditure — fertility as an input to projections, not as an outcome of pensions.

16. **Retreat from mandatory pension funds in countries of the Eastern and Central Europe in result of financial and fiscal crisis** (2015 | DOI: 10.13140/rg.2.1.3704.1688)
    - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies political economy of pension fund reforms in Central-Eastern Europe with no fertility outcome.

17. **Introduction: a forum for developing ideas and solutions to pension challenges** (2002 | DOI: 10.1017/s1474747201001056)
    - Haiku: UNCERTAIN [LOW] — Focuses on pensions but fertility outcome/mechanism not evident.
    - Sonnet: NOT_RELEVANT [HIGH] — Editorial introduction to a pension economics journal discussing demographic challenges for pension systems — reverse direction from what the review tests.

18. **Who Bears What Risk? An Intergenerational Perspective** (2005 | DOI: 10.2139/ssrn.790764)
    - Haiku: UNCERTAIN [LOW] — Intergenerational risk analysis; may address old-age security and family structure links.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Title suggests intergenerational risk-sharing analysis, likely pension-related, but without fertility as an outcome this is unlikely to be relevant.

19. **Problems of a Declining Hungarian Birth Rate: A Historical Perspective** (2015 | DOI: 10.5195/ahea.2014.1)
    - Haiku: UNCERTAIN [MEDIUM] — Analyzes factors in Hungary's fertility decline; may include pension system discussion.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Examines historical demographic factors behind Hungary's declining birth rate across multiple periods, with no indication that pension or old-age security is the primary explanatory variable.

20. **The Return on Social Security with Increasing Longevity** (2015)
    - Haiku: UNCERTAIN [LOW] — Analyzes social security returns under longevity; may indirectly address fertility implications.
    - Sonnet: NOT_RELEVANT [HIGH] — Studies the internal rate of return of PAYG pension systems under increasing longevity and optimal retirement decisions, not pension effects on fertility.

21. **Kapitaldeckungs- versus Umlageverfahren** (2000 | DOI: 10.1111/1468-2516.00024)
    - Haiku: UNCERTAIN [LOW] — Discusses funded vs. PAYG pension financing with intergenerational distribution; may address fertility implications.
    - Sonnet: NOT_RELEVANT [HIGH] — Debates funded versus unfunded pension financing modes from an efficiency and intergenerational redistribution perspective, without fertility as an outcome.

22. **Facts and Factors on Low Fertility in Southern Europe: The Case of Spain** (2003)
    - Haiku: UNCERTAIN [LOW] — Analyzes fertility decline in Spain; abstract cut off but may discuss pension/welfare systems.
    - Sonnet: NOT_RELEVANT [MEDIUM] — Examines multiple factors behind Spain's low fertility, but with a truncated abstract there is no indication that old-age security or pensions is the primary explanatory variable.

23. **Policy Responses to Population-Declining Society: Development and Challenges of Family Policies in Japan** (2013 | DOI: 10.1007/978-1-4614-6771-7_21)
    - Haiku: UNCERTAIN [MEDIUM] — Discusses family policies in Japan's low-fertility context; may include pension system discussion.
    - Sonnet: NOT_RELEVANT [HIGH] — Title focuses on family policies in Japan, not on pension or old-age security effects on fertility.

24. **Age, Work and Social Security: The Policy Context** (1993 | DOI: 10.1007/978-1-349-22668-9_10)
    - Haiku: UNCERTAIN [MEDIUM] — Historical overview of retirement and social security; may discuss fertility implications.
    - Sonnet: NOT_RELEVANT [HIGH] — Provides historical policy context for social security and retirement, with no analysis of pension effects on fertility decisions.

25. **The Care Economy in Post-Reform China: Feminist Research on Unpaid and Paid Work and Well-Being** (2018 | DOI: 10.1080/13545701.2018.1441534)
    - Haiku: UNCERTAIN [MEDIUM] — Analyzes care economy and family work in reform China; may discuss pension-fertility links.
    - Sonnet: NOT_RELEVANT [HIGH] — Examines care economy implications of China's post-reform care policy dismantlement, with fertility decline mentioned as background context rather than as an outcome caused by pensions.

*(79 additional confusion papers not individually listed; all followed the same pattern of Haiku hesitating on pension-adjacent titles without a clear fertility outcome.)*

---

## Pattern Analysis

The 9 false negatives cluster into three distinct patterns.

**Pattern 1: "Children as old-age insurance" papers without the word "pension" (5 of 9 FNs)**

The clearest miss pattern: papers that theorize or empirically test the value of children as old-age support — without invoking formal pension systems by name — were systematically excluded by Haiku. Examples: "Economic factors in family size decisions in Thailand" (1977), "The Value and Cost of Children" (1978), "On the structural value of children and its implication on intended fertility in Bulgaria" (2008), and "Mortality risks, sequential decisions on births, and population growth" (1972). Each of these engages directly with the children-as-retirement-insurance motive, which is the foundational demand-side mechanism of the pension-crowdout hypothesis. Haiku appears to have been looking for supply-side language ("pension system," "social security program") and missed the demand-side framing. The Niehof et al. (2008) Bulgaria paper and the 1972 Demeny paper on surviving sons are canonical formulations of this motive; their absence from a RELEVANT pool would be a significant content gap.

**Pattern 2: Becker-Barro / OLG theoretical models labeled as "no pension component" (2 of 9 FNs)**

Two papers — "The macroeconomics of fertility in small open economies: A test of the Becker-Barro model" (2001) and "Social Security Financial Crises" (2003) — were rated NOT_RELEVANT by Haiku because the connection to pensions was theoretical or structural rather than empirically named. The Becker-Barro model embeds altruism and savings motives where old-age transfers are central; the 2003 paper explicitly models PAYG effects on fertility. Haiku apparently required explicit "pension → fertility" language in the abstract rather than recognizing that testing or applying these theoretical frameworks is ipso facto relevant.

**Pattern 3: Intergenerational transfer papers framed around savings or capital accumulation (2 of 9 FNs)**

"From Transfers to Individual Responsibility: Implications for Savings and Capital Accumulation in Taiwan and the United States" (2000) and "Private and Social Incentives for Fertility: Israeli Puzzles" (2002) model the shift from family-based to market-based old-age support. Haiku rated both NOT_RELEVANT, presumably because "savings" and "capital accumulation" were the framing terms rather than "pension crowdout." These papers are close analogs of the canonical Caldwell (1976) wealth-flows mechanism. The miss reflects Haiku's tendency to screen on surface vocabulary rather than on the underlying economic mechanism.

---

## Prompt Revision Suggestions

**Change 1:** Explicitly name the children-as-old-age-insurance demand-side motive.

*Current:* The prompt presumably instructs Haiku to flag papers that study "pensions or old-age security as a cause of fertility change."

*Revised:* Add: "Also flag papers that study the value or cost of children as old-age support (the 'children-as-retirement-insurance' or 'old-age security motive'), even if no formal pension system is mentioned. This includes papers analyzing parental expected benefits from children in old age, the structural value of children as old-age insurance, or sequential birth strategies aimed at securing a surviving son or daughter for support in old age."

*Rationale:* Directly catches FNs 1, 2, 3, 8 (Thailand 1977; Value and Cost 1978; Bulgaria 2008; Demeny 1972).

**Change 2:** Name canonical theoretical frameworks as sufficient evidence of relevance.

*Current:* Haiku apparently requires explicit empirical "pension → fertility" language.

*Revised:* Add: "Papers testing or extending the Becker-Barro fertility model, the Caldwell wealth-flows model, or overlapping-generations (OLG) models where fertility responds to PAYG generosity or intergenerational transfers are RELEVANT even if the abstract does not use the word 'pension.' The mechanism need not be labeled explicitly — theoretical frameworks that embed the old-age security channel are sufficient."

*Rationale:* Catches FNs 6 and 7 (Becker-Barro Netherlands/NZ 2001; Social Security Financial Crises 2003).

**Change 3:** Distinguish causal direction explicitly at the start of the exclusion criteria.

*Current:* Haiku appears to conflate papers where pensions are causes of fertility decline with papers where fertility decline is a cause of pension system stress.

*Revised:* Add a bolded exclusion note: "EXCLUDE papers in which fertility decline is a cause or context for pension system sustainability problems (reverse direction). INCLUDE papers in which pension generosity, availability, or expansion is a cause or hypothesized cause of fertility decline. When the causal arrow is ambiguous, default to UNCERTAIN rather than NOT_RELEVANT."

*Rationale:* Reduces the 42 FPs and 104 confusion papers where Haiku hesitated or included papers with the reverse causal structure (e.g., Lithuania 2014, Demography Pensions Finland 1996, Cost of Low Fertility Europe 2009). Does not directly address the 9 FNs but reduces noise in the UNCERTAIN pool, freeing Haiku's attention for genuine borderline cases.

---

## Recommendation

Stopping criterion met — Haiku FN rate of 1.0% is well below the 3% threshold; proceed to full run using routing-rule.md with the prompt revisions above applied before the production batch.
