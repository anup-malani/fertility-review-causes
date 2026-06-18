# Master Hypothesis List

Status: DRAFT -- produced by .claude/workflows/enumerate-hypotheses.mjs. Awaiting PI review and approval. After approval, this file becomes the authoritative input to literature-search.mjs (workflow #2).

Phenomena codes: PM = pre-modern, FDT = First Demographic Transition, SDT = Second Demographic Transition.

**Organization:** Hypotheses are divided into two tiers. *Proximate causes* are mechanisms — the behavioral and biological pathways through which fertility changes, but which do not themselves explain *why* people want fewer (or more) children. *Root causes* are the underlying drivers: Economic, Biological, and Cultural. A proximate cause may be linked to one or several root-cause categories via its `cross-ref` field; that linkage is recorded there rather than by sub-dividing the Proximate section. Decision recorded in `decisions/2026-06-14-proximate-vs-root-cause-categories.md`.

[Claude. In addition to looking for explanations in the literature, we should also review my X bookmarks. There are a lot of explanations floating around, some of which have papers (for example, the recent iPhone paper), but many do not.

We should start by going through the X bookmarks and then develop a plan for where else to look for explanations we may have missed. Right now we seem more underinclusive than overinclusive, and it is possible we do not have all the explanations yet and will add them iteratively.

This comment is mainly motivated by recent literature and media on iPhones. You could make the same argument for climate change doomerism, which is also on X and in social media, although I do not know of any paper that supports it.]

## Proximate Causes

### Child Mortality Decline (Replacement and Insurance Effects)
- **slug:** `child-mortality-decline-replacement`
- **claim:** Falling infant and child mortality reduces desired and realized fertility through reduced replacement births and reduced hoarding/insurance births, lowering TFR roughly in proportion to the gap between gross and net reproduction rates.
- **why:** When more children survive to adulthood, parents who want N surviving children need fewer births to reach that target. They also have less reason to 'hoard' extra births as insurance against losing some. Both effects push down realized fertility once mortality drops, though there is typically a lag.
- **phenomena:** PM, FDT, SDT
- **seminal:** Notestein 1945, Preston 1978, Schultz 1997, Galor and Weil 2000, Doepke 2005
- **cross-ref:** Economic
- **notes:** Canonical FDT mechanism; timing problems (mortality often falls before fertility) and weak macro identification. Doepke 2005 distinguishes replacement/hoarding/q-q channels.

 Claude:  this is correct.  child mortality decline affects proximate causes because it triggers an insurance effect (either an economic or evolutionary argument). Even if people were risk-neutral, they would still want to have more births to offset the decline, which could be driven by a preference for a certain number of surviving kids or something else 

### Modern Contraceptive Technology and Diffusion
- **slug:** `contraceptive-technology-diffusion`
- **claim:** Introduction and diffusion of cheap, effective, reversible contraception (the Pill, IUDs, modern sterilization) lowers the cost of fertility control and reduces unwanted births, lowering TFR.
- **why:** Cheap, effective, reversible methods like the Pill and IUDs dramatically lower the effort and uncertainty of avoiding a birth. Couples who already wanted fewer kids can now actually achieve that target, and unplanned pregnancies fall. The result is realized fertility moving closer to desired fertility, which in modern settings means lower TFR.
- **phenomena:** FDT, SDT
- **seminal:** Westoff and Ryder 1977, Goldin and Katz 2002, Bailey 2006, Bongaarts 1978, Michael 1973
- **cross-ref:** Economic
- **notes:** Micro-identified (Comstock laws, state-level Pill access); Pritchett 1994 contests macro significance. Often interacts with FLFP and education. Merged with the Economic "falling price of fertility control" framing — same underlying technology shock.

 Claude, I think this is the right place because contraception technology diffusion can be seen as an economic explanation (people want lower fertility, and contraception is the way they get it), but it fits with any theory, not just economic ones. It also works well as a biological explanation: contraception severs the link between reproduction and fertility. 

### Diffusion and Social-Learning of Fertility Control
- **slug:** `diffusion-of-fertility-control`
- **claim:** Fertility decline spreads through linguistic, religious, and social networks via diffusion of information about and legitimation of birth control, independent of underlying socioeconomic conditions.
- **why:** Even holding economics constant, knowing that birth control exists, that it is socially acceptable, and that neighbors are using it has to spread before people adopt it. The idea travels through shared language, religion, and social ties faster than through economic boundaries. Fertility falls where the information and legitimation arrive, regardless of local income.
- **phenomena:** FDT, SDT
- **seminal:** Coale and Watkins 1986, Cleland and Wilson 1987, Bongaarts and Watkins 1996, Rosero-Bixby and Casterline 1993
- **cross-ref:** Cultural
- **notes:** Princeton project's residual explanation; closely related to ideational/SDT cultural story. Primary mechanism is behavioral spread, hence Demographic primary.

[ Claude, is this very similar to the contraception, or is it something different? Is it closer to the idea that the social value of family planning was promoted by the UN as a way to control population?

What do you mean by this particular project? I want to separate the use of contraception or other family planning techniques from the idea that it is a good idea to do so, and distinguish it from proximate cause. Is it something deeper, like cultural or social learning ]

### Induced Abortion Access and Legalization
- **slug:** `induced-abortion-access`
- **claim:** Legalization and access to safe induced abortion lowers TFR by removing unwanted pregnancies that would otherwise result in live births, with effects documented around Roe v. Wade and Eastern European liberalizations.
- **why:** Legal, safe abortion lets women end unwanted pregnancies that otherwise would have become live births. When access expands, some fraction of conceptions no longer convert into babies, so TFR falls mechanically. The size of the effect depends on how much contraception was already preventing those pregnancies upstream.
- **phenomena:** FDT, SDT
- **seminal:** Levine et al. 1999, Pop-Eleches 2006, Bongaarts 1978, Westoff et al. 1981
- **cross-ref:** --
- **notes:** Crucial in Eastern Europe, Japan postwar, USSR; ambiguous for Western FDT (mostly illegal). Substitution with contraception complicates net effect.

[Claude:  there will be many different types of family planning and how they affect fertility. Can we group everything under a broad “family planning” category, with subsets for specific types (e.g., abortion, specific contraception)?  ]

### Organized Family Planning Programs and Access
- **slug:** `family-planning-programs`
- **claim:** Government and NGO family-planning programs expanding contraceptive supply, information, and subsidies reduce unmet need and lower TFR independent of demand-side changes.
- **why:** Even where people want fewer kids, contraceptives can be expensive, far away, or surrounded by misinformation. Government and NGO programs that hand out supplies, train providers, and run outreach close this 'unmet need' gap. Births fall because supply-side frictions, not preferences, were the binding constraint.
- **phenomena:** FDT, SDT
- **seminal:** Bongaarts et al. 1990, Pritchett 1994, Joshi and Schultz 2013, Miller 2010, Cleland et al. 2006
- **cross-ref:** --
- **notes:** Pritchett argues demand dominates; Matlab and Profamilia quasi-experiments show meaningful supply effects. Salient for LMIC FDT.

### Age at Marriage and Marriage Timing (European Marriage Pattern)
- **slug:** `marriage-timing-age-at-marriage`
- **claim:** Later female age at first marriage and higher proportions never marrying mechanically reduce exposure to childbearing and lower TFR, with cross-population variation in the Hajnal pattern explaining substantial PM and early-FDT fertility differences.
- **why:** Most births in pre-modern and early-modern settings happened inside marriage, so the years a woman spends unmarried are years she is not exposed to pregnancy. Societies where women marry late (or never) mechanically have lower fertility, even with no contraception. Shifts in age at first marriage are a powerful lever on TFR by themselves.
- **phenomena:** PM, FDT, SDT
- **seminal:** Hajnal 1965, Coale 1973, Wrigley and Schofield 1981, De Moor and van Zanden 2010
- **cross-ref:** Cultural
- **notes:** Core PM mechanism (Malthusian preventive check); marriage decline weakened FDT relevance; non-marital fertility rise complicates SDT mapping.

### Parity-Specific Stopping and Spacing Behavior
- **slug:** `parity-progression-stopping-behavior`
- **claim:** Adoption of deliberate parity-specific stopping (rather than spacing) within marriage is the proximate behavioral signature of the FDT, and its diffusion accounts for the bulk of marital fertility decline.
- **why:** Couples can lower fertility in two ways: by spacing births further apart, or by deciding 'we are done' after a target number of kids and stopping entirely. The FDT is characterized by the spread of deliberate stopping at low parities. Once couples treat family size as a target to hit and then halt, average completed fertility drops sharply.
- **phenomena:** FDT
- **seminal:** Coale and Watkins 1986, Henry 1961, Knodel 1979, Cleland and Wilson 1987
- **cross-ref:** Cultural
- **notes:** Princeton European Fertility Project; methodological backbone (m and M indices). Often treated as outcome rather than cause — frame as proximate mechanism.

### Population Age Structure and Demographic Momentum
- **slug:** `population-age-structure-momentum`
- **claim:** Shifts in the age structure (share of women in peak reproductive ages) drive crude birth rates and period TFR independent of any change in age-specific fertility, generating mechanical fertility movements.
- **why:** The crude birth rate depends not just on how many kids women are having, but on how many women are currently of childbearing age. A population with a big bulge of 20-30 year olds will produce many births even at low per-woman fertility, and vice versa. These compositional swings move headline fertility numbers without any change in underlying behavior.
- **phenomena:** FDT, SDT
- **seminal:** Keyfitz 1971, Bongaarts and Bulatao 1999, Lutz et al. 2003
- **cross-ref:** --
- **notes:** Largely accounting/measurement; matters for interpreting CBR and short-run TFR but not for completed cohort fertility.

### Sex Ratio Imbalance and Marriage Market Effects
- **slug:** `sex-ratio-marriage-market`
- **claim:** Skewed adult sex ratios (war, migration, sex-selective abortion) shift marriage rates and bargaining power, affecting marriage timing and marital fertility.
- **why:** If wars, migration, or sex-selective abortion leave one sex in short supply, marriage markets clear differently: some people cannot find partners, marriage gets delayed, and bargaining power inside marriages shifts. These changes feed through to whether and when couples form, and how many kids they have together. Fertility responds to the imbalance even though nothing changed about individual desires.
- **phenomena:** PM, FDT, SDT
- **seminal:** Guttentag and Secord 1983, Angrist 2002, Abramitzky et al. 2011
- **cross-ref:** Economic
- **notes:** Mostly local/short-run shocks; matters for postwar cohorts and sex-selection-affected Asian populations.

[ Claude, I think this is a proximate cause because it raises the question of why the sex ratio imbalance occurred. Sometimes it’s culture, sometimes it’s war. As far as I can tell, nobody thinks it has had a first-order effect on total fertility, because globally sex ratios tend to be close to the so-called natural rate .  tell me if I'm wrong ]

### Tempo Effects and Birth Postponement
- **slug:** `tempo-effects-birth-postponement`
- **claim:** Rising mean age at first birth depresses period TFR mechanically during the postponement transition, accounting for a meaningful share of measured low SDT fertility without an equivalent change in completed cohort fertility.
- **why:** If every woman delays her first birth by a few years, then during the transition period there is a stretch of calendar time when fewer births are recorded — even though each cohort may eventually have the same number of kids. The period TFR drops mechanically because births get pushed into the future. Once the delay stabilizes, measured fertility partly rebounds, so part of 'low fertility' is really a timing artifact, not a true drop in family size.
- **phenomena:** SDT
- **seminal:** Bongaarts and Feeney 1998, Sobotka 2004, Goldstein et al. 2009, Lesthaeghe 2010, Goldin 2006, Gustafsson 2001
- **cross-ref:** Economic
- **notes:** Distinguishes quantum from tempo; central to SDT measurement debate. Tempo-adjusted TFR often closer to replacement. Merged with the Economic "tempo postponement" framing (rising returns to schooling/career as driver of timing).

### Twinning Rates and Multiple Births
- **slug:** `twinning-multiple-births`
- **claim:** Variation in twinning rates (genetic, ART-induced) modestly affects TFR by raising live births per pregnancy, with ART-induced multiples partially offsetting postponement-driven SDT declines.
- **why:** Each pregnancy doesn't have to produce exactly one baby — twins and higher-order multiples raise the births-per-pregnancy ratio. Populations with higher twinning rates (whether from genetics or, today, from IVF) get a small boost to TFR for free. The effect is real but small, and now partly offsets the SDT trend through ART-assisted multiples.
- **phenomena:** PM, SDT
- **seminal:** Bulmer 1970, Pison and D'Addato 2006, Hoekstra et al. 2008
- **cross-ref:** Biological
- **notes:** Small magnitude; included for completeness. PM variation across ethnic groups (Yoruba) documented.

## Economic

### Mode of Production and Child Economic Value
- **slug:** `agricultural-mode-of-production`
- **claim:** Differences in production technology across hunter-gatherer, pastoralist, and agriculturalist economies generate different optimal fertility through child labor value and dependency length.
- **why:** In hunter-gatherer, pastoralist, and farming economies, children produce different amounts of useful labor and become economically self-sufficient at different ages. Where kids start helping in the fields young and the cost of feeding them is low, parents gain more from having many. Where children are economically idle for longer (or where mothers can't carry them while working), the optimal number falls.
- **phenomena:** PM
- **seminal:** Boserup 1965, Kaplan 1994, Sellen and Mace 1997, Gibson and Mace 2006
- **cross-ref:** Cultural
- **notes:** Important for PM cross-population variation; overlaps with anthropological evolutionary ecology.

### Childcare Cost and Availability
- **slug:** `childcare-availability-cost`
- **claim:** Lower-cost or higher-quality formal childcare reduces the opportunity cost of working mothers' fertility, raising completed fertility.
- **why:** A big share of the cost of a child is the parent's time, especially the mother's. When subsidized daycare or high-quality preschools are widely available, mothers can keep earning instead of stepping out of the labor force, so an extra child no longer means giving up a career. That lowers the effective price of children and nudges fertility up.
- **phenomena:** SDT
- **seminal:** Blau and Robins 1989, Del Boca 2002, Bauernschuster Hener and Rainer 2016, Olivetti and Petrongolo 2017
- **cross-ref:** --
- **notes:** Closely tied to female-wage channel; positive effects most evident in continental Europe.

### Rising Direct Costs of Children
- **slug:** `child-cost-direct`
- **claim:** Rising direct expenditures required per child (schooling, health, consumption norms) reduce fertility by raising the price of children.
- **why:** Modern children require more out-of-pocket spending than they used to: tuition, doctors, clothes, activities, gadgets, all the things social norms say a 'proper' child needs. As these per-child outlays rise, the budget supports fewer kids at the standard parents feel obligated to meet, so family size shrinks.
- **phenomena:** FDT, SDT
- **seminal:** Caldwell 1976, Lino 2017, Folbre 2008, Doepke and Kindermann 2019
- **cross-ref:** Cultural
- **notes:** Often blended with q-q; separating direct from quality-investment cost is identification challenge.

[ Claude, we should organize the explanations under “child care cost” into clear categories within economics. One category could be “child cost,” with sub-explanations under that heading.

We should also create a table of contents that organizes everything properly so readers can easily find the different explanations. It looks like variations on “children are more costly” should be grouped together. We should separate explanations where child care is costly from other issues, like “the value of children has changed,” which is a different issue than rising care costs.

With urbanization, there are arguments on both sides. On one hand, urbanization could lead to cultural changes that make children valued less. On the other hand, urbanization has a more direct effect through child care costs. I think the latter is probably more important, but that is just something to keep in mind. ]
### Child Labor Restrictions and Compulsory Schooling
- **slug:** `child-labor-laws-and-schooling`
- **claim:** Legal restrictions on child labor and compulsory schooling lower the economic return to children and raise their cost, reducing fertility.
- **why:** When governments ban child labor and require kids to be in school, children stop being a source of family income and instead become a long-running expense. The whole calculation flips: an extra child no longer pays his or her own way through farm or factory work, so parents want fewer of them.
- **phenomena:** FDT
- **seminal:** Doepke 2004, Doepke and Zilibotti 2005, Hazan and Berdugo 2002, Galor and Moav 2006
- **cross-ref:** --
- **notes:** Tightly linked to q-q; policy-driven variation provides identification.

[ Claude, this one looks like it's not so much child cost as much as decreasing the value of children.  that should be the broad category within economics that this particular one falls under. Lower value of children as opposed to lower cost of children]

### Credit Constraints and Liquidity
- **slug:** `credit-constraints`
- **claim:** Imperfect credit markets force families to use children as savings/insurance vehicles or, conversely, delay childbearing when young households cannot borrow against future income.
- **why:** Without good banks or insurance, children themselves act as a savings account and old-age safety net, which pushes poor households to have more. But in richer settings, young couples can't borrow against their future earnings to buy a house or fund a family early, so they delay having kids, sometimes long enough that the delay becomes a permanent reduction.
- **phenomena:** PM, FDT, SDT
- **seminal:** Becker 1981, Lehrer and Nerlove 1986, Lino 2017, Lovenheim and Mumford 2013
- **cross-ref:** --
- **notes:** Sign ambiguous: insurance motive pushes fertility up in poor settings, liquidity constraint pushes it down for young SDT households.

[ Claude, this one belongs under value of children ]

### Dynastic Altruism (Becker-Barro)
- **slug:** `dynastic-altruism-becker-barro`
- **claim:** Parents choose fertility to maximize dynastic utility under altruism, so changes in the interest rate, mortality, or per-child cost shift fertility via the Euler condition on descendants.
- **why:** Treat parents as choosing not just how happy they are but how well their whole line of descendants does. Then fertility is a normal economic decision shaped by interest rates, child survival, and the cost of raising each kid. Anything that makes future generations more expensive or less valuable in this calculus, like cheaper alternative investments or rising child costs, reduces the optimal number of descendants.
- **phenomena:** PM, FDT, SDT
- **seminal:** Barro and Becker 1989, Becker and Barro 1988, Alvarez 1999, Jones and Schoonbroodt 2010
- **cross-ref:** --
- **notes:** Framework rather than testable mechanism; nests q-q and income effects; useful for macro calibration.

[ Claude, I think you make a good point in the notes that this is really about a modeling choice, not so much a particular cause.

We should decide what to do with these. They are not proximate causes. They are more like a framework or model, and that might belong under “Economic,” but they could also be treated as proximate causes, like proximate causes are: a different category of theories, explanations, or methodologies, not necessarily one of the root causes or a proximate cause. What do you think]

### Easterlin Relative Income / Cohort Size
- **slug:** `easterlin-relative-income`
- **claim:** Fertility rises when a cohort's earnings prospects are favorable relative to the consumption aspirations formed in their parents' household, generating endogenous fertility cycles.
- **why:** People judge their economic prospects by comparing their earnings to the lifestyle they grew up in. A small generation entering a strong labor market feels rich relative to that benchmark and has lots of kids; a large generation crowding into a weaker market feels poor and has fewer. This produces fertility cycles driven by cohort size rather than absolute income.
- **phenomena:** SDT
- **seminal:** Easterlin 1961, Easterlin 1976, Macunovich 1998
- **cross-ref:** Demographic
- **notes:** Originally proposed to explain US baby boom/bust; weaker post-1980 empirical support.

[ claude: this is the Easterlin Cycling Hypothesis, which I do think is a separate one and nicely falls under economic .  do I have that right?]

### Economic Uncertainty and Labor-Market Insecurity
- **slug:** `economic-uncertainty-and-unemployment`
- **claim:** Higher job insecurity, unemployment risk, and temporary contracts induce postponement and reduction of fertility.
- **why:** Having a child is a long-term commitment that's hard to reverse, so couples want some confidence about future income before taking it on. When jobs are precarious, contracts are temporary, or recessions hit, people postpone childbearing. Enough postponement turns into fewer total kids because biology and life plans don't wait forever.
- **phenomena:** SDT
- **seminal:** Adsera 2004, Adsera 2011, Sobotka Skirbekk and Philipov 2011, Schneider 2015
- **cross-ref:** --
- **notes:** Salient explanation for post-2008 fertility decline and Southern European lowest-low fertility.

### Female Wage and Opportunity Cost of Time
- **slug:** `female-wage-opportunity-cost`
- **claim:** Rising female wages raise the opportunity cost of child-rearing time, reducing fertility.
- **why:** Raising children takes time, and that time is mostly the mother's. As women's wages rise, every hour spent on childcare means more forgone earnings, so kids effectively get more expensive. Even if higher income makes families want more of every normal good, the time-cost effect on the mother typically dominates and fertility falls.
- **phenomena:** FDT, SDT
- **seminal:** Mincer 1963, Becker 1965, Willis 1973, Butz and Ward 1979, Schultz 1985
- **cross-ref:** Cultural
- **notes:** Workhorse Beckerian channel; income vs. substitution effect contested; Butz-Ward business-cycle reframing important.

[ Claude, the cost of children is a category that can include this because there is a time cost. I think it is better to put this under income and its effect on children: as incomes rise, you have two effects: an income effect and a substitution effect.

The substitution effect is the rising cost of raising children because it requires time. As wages rise, the cost of that time input increases a little. In that sense, it could go under both income and the cost of children, but I think it generally falls under income. We should think of it as income and substitution effects, not in the traditional sense, but in the peculiar effects that operate through time budget constraints.

Within that, we could talk about how that has an effect on females but not otherwise. That is where I would put this. I know it is a close call, because you could also put it under female wages or feminization, but I do not think that is really going on here. It is mainly an economic point about the opportunity cost of women’s time and, more broadly, the opportunity cost of child-rearing time.

You could say there is an income effect and you want to treat that differently than the time cost effect, putting the time cost effect in the cost of children. We could do that, but we should make that a deliberate choice and, in any case, put a cross-reference in both the income and the time cost sections to point towards which one has this rising opportunity cost of child-rearing time explanation ]

### Trade, Globalization, and Sectoral Reallocation
- **slug:** `globalization-and-trade`
- **claim:** Trade-induced shifts in labor demand (toward female-intensive services or away from manufacturing) change the gender wage structure and household fertility.
- **why:** Trade reshuffles which industries grow and shrink. When growth happens in services and other sectors that hire women, female wages and employment rise, raising the opportunity cost of staying home with kids. When manufacturing jobs that supported male breadwinners disappear, household incomes and marriage rates fall, which also reduces fertility through a different channel.
- **phenomena:** SDT
- **seminal:** Do Levchenko and Raddatz 2016, Autor Dorn Hanson Pettersson and Song 2019, Anukriti and Kumler 2019
- **cross-ref:** --
- **notes:** Recent literature; relevant for cross-country SDT variation and US 'China shock' fertility effects.

[ this seems second-order because it explains why female wages are rising, not how that affects the number of kids. We should probably fold this into the time opportunity or the opportunity cost of raising children for whoever takes care of the children. Do you object ?]
### Housing Costs and Space Constraints
- **slug:** `housing-costs`
- **claim:** Higher house prices and rents raise the cost of the space input to child-rearing, reducing fertility.
- **why:** Kids need physical space, so a bigger family usually means a bigger home. When house prices and rents spiral upward, the implicit price of having another child rises sharply, and young couples either delay parenthood until they can afford the space or settle for fewer kids. Existing homeowners feel this less because rising prices also make them wealthier.
- **phenomena:** SDT
- **seminal:** Mulder and Billari 2010, Dettling and Kearney 2014, Lovenheim and Mumford 2013, Daysal Lovenheim and Wasser 2021
- **cross-ref:** --
- **notes:** Recent macro narrative for SDT; ambiguous sign because home-equity wealth effect partially offsets.

[ Claude, this too falls under the cost of raising children.  it should be categorized within economics under the cost of children explanations  ]

### Income Effect on Fertility
- **slug:** `income-effect-normal-good`
- **claim:** Holding prices constant, higher household income raises desired fertility because children are a normal good.
- **why:** If children are like other things people enjoy, you'd expect richer households to have more of them, just as they have more vacations and bigger houses. This is the baseline prediction, and it's important precisely because reality contradicts it: fertility fell as incomes rose, which is the central puzzle other economic theories try to explain.
- **phenomena:** PM, FDT, SDT
- **seminal:** Malthus 1798, Becker 1960, Jones Schoonbroodt and Tertilt 2011, Clark 2007
- **cross-ref:** --
- **notes:** Important as the counterfactual: secular fertility decline despite rising income is the puzzle the other economic hypotheses try to resolve.

### Land and Resource Constraints (Malthusian)
- **slug:** `land-and-resource-constraints-malthusian`
- **claim:** In pre-modern settings, fixed land and diminishing returns generate a positive check linking real wages and fertility/mortality.
- **why:** In a pre-modern economy, output depends on a fixed stock of farmland, so more people means less food per person. When wages fall below subsistence, people delay marriage and starvation rises, pulling population back down. Fertility moves with real wages because couples adjust marriage timing to economic conditions.
- **phenomena:** PM
- **seminal:** Malthus 1798, Lee 1980, Clark 2007, Ashraf and Galor 2011
- **cross-ref:** Demographic
- **notes:** Foundation for PM variation; preventive vs positive check distinction matters.

[ Claude, this is a distinct point from the cost of children, so I’m glad we have it broken out. It should be in its own category under Economics. I do like that there’s a cross-reference to demographics, though ]

### Marriage Market and Assortative Mating
- **slug:** `marriage-market-economics`
- **claim:** Changes in marriage market matching (sex ratios, education gaps, search frictions) alter union formation and thereby fertility.
- **why:** Fertility mostly happens inside partnerships, so anything that makes it harder to form or sustain a match reduces births. Skewed sex ratios, mismatches in education between men and women, or longer search times for the 'right' partner all delay marriage and union formation. Delay then directly translates into fewer kids per person.
- **phenomena:** FDT, SDT
- **seminal:** Becker 1973, Wilson 1987, Schwartz and Mare 2005, Greenwood Guner Kocharkov and Santos 2014
- **cross-ref:** Demographic
- **notes:** Bridges to demographic nuptiality channel; relevant for delayed/foregone childbearing.

[ Claude, I’m not sure how to think about this. If we assume marriage is a precondition for having children because it makes childrearing more productive, then marriage becomes less common for some reason, which could reduce the number of children. Should we still count that as an economic explanation?

The argument is that marriage makes childrearing more efficient, but it also reduces the productivity of raising children. It’s more that it increases the cost, a particular type of cost. Am I getting that wrong?   it's not about the value of children as much as the cost of producing children.

if I think about it by analogizing to a firm, profit is equal to p f(x) - c(x) where p is the value of the output, f is the output that you get from inputs x, and c is the cost of inputs x .  here, profit is what you get from having kids. P is the value of the kids. F is the productivity of raising kids, and C is the cost of the inputs into raising kids.

In that context, you could separate out benefit and cost, and then, within benefit, talk about the productivity versus the actual return to each child. In that case, the marriage probably still goes into cost rather than productivity, I assume, but it’s not clear it could go into productivity. I don’t know if that’s too nuanced and not worth explaining, but maybe it works for clarifying how different explanations relate to one another]

### Old-Age Security and Pension Crowd-Out
- **slug:** `old-age-security-pension-crowdout`
- **claim:** Public pensions and formal old-age insurance substitute for children as a retirement-support asset, reducing fertility.
- **why:** In societies without formal retirement systems, adult children are how parents survive old age, which gives a strong economic motive for high fertility. When governments provide pensions or formal insurance, that motive evaporates, and parents no longer need many kids to insure against destitution in old age.
- **phenomena:** FDT, SDT
- **seminal:** Neher 1971, Nugent 1985, Cigno and Rosati 1996, Boldrin Jones and Khitatrakun 2005, Billari and Galasso 2009
- **cross-ref:** Demographic
- **notes:** Causal identification difficult; some natural experiments (pension expansions) support it.

[ Claude, this is clearly about the value of children, but you go under that category within economics]

### Quantity-Quality Tradeoff
- **slug:** `quantity-quality-tradeoff`
- **claim:** Rising returns to child human capital raise the shadow price of an additional child relative to investing more in each existing child, lowering desired fertility.
- **why:** As returns to education and human capital rise, parents shift spending toward fewer, more-invested children rather than many less-invested ones. The marginal value of each child's quality rises faster than the value of an extra quantity child, so equilibrium family size falls.
- **phenomena:** FDT, SDT
- **seminal:** Becker 1960, Becker and Lewis 1973, Becker and Tomes 1976, Galor and Weil 2000, Doepke 2004
- **cross-ref:** --
- **notes:** Canonical economic mechanism; micro evidence mixed (Black-Devereux-Salvanes 2005 finds little tradeoff); macro role central in unified growth theory.

[ Claude, this goes under the value children ]

### Inequality and Status Competition in Child Investment
- **slug:** `rising-inequality-and-status-competition`
- **claim:** Rising income inequality raises the required quality investment per child to maintain relative status, lowering fertility.
- **why:** When inequality is high, the gap between succeeding and falling behind grows, and parents feel they must pour more resources into each child to keep them competitive (the 'rug-rat race'). Raising one kid to the new higher standard becomes so expensive that even well-off families can afford only a couple, pushing fertility down.
- **phenomena:** SDT
- **seminal:** Easterlin 1976, de la Croix and Doepke 2003, Kearney and Levine 2014, Doepke Hannusch Kindermann and Tertilt 2022
- **cross-ref:** Cultural
- **notes:** Easterlin's relative-income hypothesis lives here; recent revival in 'rug-rat race' literature.

[ Claude, this falls under the cost of children. Status competition increases the amount of time people feel they need to devote to children, which means they have fewer children.

One interesting byproduct is that, to some extent, it could lead to having fewer children, and it could also change cultural norms. It will be interesting to see what happens in the future. That is not directly relevant to our discussion here, but it is an interesting side effect of that line of thinking .  also, I'm not sure why the relative income hypothesis lives here if I understand the Easterlin hypothesis to be about cycling. It's related, but that's not exactly where it sits ]

### Skill-Biased Technical Change and Returns to Education
- **slug:** `skill-biased-technical-change`
- **claim:** Rising returns to human capital induce parents to substitute toward fewer, higher-investment children.
- **why:** When technology raises the wage premium for educated workers, the return to investing heavily in each child's schooling grows. Parents reallocate from having many kids to giving fewer kids the long, expensive education that now pays off. The shift in the labor market shows up one generation later as smaller families.
- **phenomena:** FDT, SDT
- **seminal:** Galor and Weil 2000, Galor and Moav 2002, Greenwood Seshadri and Vandenbroucke 2005
- **cross-ref:** --
- **notes:** Macro driver behind q-q in unified growth theory; SDT relevance through rising college premium.

[ Claude, this is essentially the QW argument in a different format. We should group all of these together under quality-quantity and not treat them as separate points, since they are all saying we make the quality-quantity tradeoff differently for different technological reasons ]

### Tax and Transfer Pronatal Policies
- **slug:** `tax-and-transfer-pronatalism`
- **claim:** Child allowances, parental leave, childcare subsidies, and tax credits raise fertility by lowering the net cost of children.
- **why:** Governments can lower the net price of children by writing checks: child allowances, paid parental leave, subsidized daycare, tax credits. By making each child cheaper to raise, these policies should raise fertility. In practice the effects are usually small and often shift the timing of births rather than the total number.
- **phenomena:** SDT
- **seminal:** Gauthier and Hatzius 1997, Milligan 2005, Laroque and Salanié 2014, Cohen Dehejia and Romanov 2013
- **cross-ref:** --
- **notes:** Effect sizes generally small; tempo vs quantum debate; useful as policy counterfactual.

[ Claude, this belongs in the cost of children. sometimes the government adopts policies that change the value of kids, not by lowering the cost of having them, but by changing how much families value having kids. For example:

- UN population control policies or climate terrorism that make people feel like kids are a bad thing
- A policy that provides state pensions or reduces the value of children

This is really about changing the cost of raising them, I think. Tell me if I’m wrong ]

### Urbanization and Rural-Urban Residential Shift
- **slug:** `urbanization-residential-shift`
- **claim:** Migration from high-fertility rural to lower-fertility urban environments mechanically lowers aggregate TFR through composition, exposes migrants to urban conditions (housing costs, weaker kin support), and devalues child labor in urban production, lowering fertility.
- **why:** Cities and farms call for different family sizes. On a farm, children help with chores from a young age and housing is cheap; in a city, kids contribute little economically, apartments are small and expensive, and grandparents are far away. As populations move from countryside to city, both the composition shift and the changed economics of children pull fertility down.
- **phenomena:** PM, FDT, SDT
- **seminal:** Notestein 1945, Davis 1963, United Nations 1987, Galor 2011, de la Croix and Doepke 2003
- **cross-ref:** Demographic
- **notes:** Composition vs. behavioral effects must be decomposed; large literature shows urban TFR < rural TFR robustly. Merged demographic (composition/residence) and economic (child-labor devaluation) framings — primary mechanism is the economic value of children in urban vs. rural production.

[Claude, does this belong in “Cost” or “Value of Children”?

I think it belongs in “Cost,” since urbanization changes the cost. You could also argue that moving to an urban area changes the value of having more kids, especially if those kids have higher human capital, or that there is a cultural aspect as well. We should identify both primary and secondary places where this could belong, but I think the main home is “Cost,” with cross-references to other subcategories under “Economic.” ]

### Intergenerational Wealth Flows Reversal
- **slug:** `wealth-flows-reversal`
- **claim:** Modernization reverses the net direction of intergenerational transfers from child-to-parent to parent-to-child, eliminating the economic rationale for high fertility.
- **why:** In traditional economies, resources flow upward from children to parents: kids work, support elderly parents, and provide insurance. Modernization flips the arrow downward, with parents now subsidizing children for decades through school and beyond. Once children are net cost centers instead of income sources, the economic logic for having many of them disappears.
- **phenomena:** FDT
- **seminal:** Caldwell 1976, Caldwell 1982, Kaplan 1994, Lee 2000, Thornton 2001
- **cross-ref:** Cultural
- **notes:** Caldwell's theory; empirically contested but widely cited; overlaps with old-age security. Thornton's 'developmental idealism' is the cultural-channel extension (see `developmental-idealism`).

[Claude, I think this belongs in value of children ]

## Biological

### Age at Menarche and Reproductive Span
- **slug:** `age-at-menarche`
- **claim:** Secular decline in age at menarche (driven by nutrition and health) lengthens the reproductive span, raising potential fertility, while later age at first birth offsets this in modern settings.
- **why:** Better nutrition and health make girls become biologically capable of childbearing at younger ages, which lengthens the window over which they can in principle bear children. A longer reproductive window mechanically raises the ceiling on how many births a woman can have. In modern settings this effect is largely neutralized because women now choose to delay first birth, so the extra years at the front of the window go unused.
- **phenomena:** PM, FDT
- **seminal:** Tanner 1981, Wyshak and Frisch 1982, Eveleth and Tanner 1990
- **cross-ref:** --
- **notes:** Mostly raises potential fertility; competes with behavioral postponement in net effect on TFR.

[ Claude, this is an interesting point, but is it explaining why fertility fell, or is it just saying that, because the age of menarche fell due to better nutrition, the age at which you start having children is later?

I understand it relates to potential fertility, but I do not see how it directly relates to actual fertility unless potential fertility is actually the constraint. If that is the case, we should put this in “biological” and deprecate it, since it is really about potential fertility, not actual fertility 

 as an aside, I don't see why, if you lower the age of menarche, you will delay the date of your first birth, because it is not a binding constraint ]
### Assisted Reproductive Technology Access
- **slug:** `art-access-fertility-recovery`
- **claim:** Availability and affordability of ART (IVF, ICSI, egg freezing) partially offsets age-related fecundity decline and enables completion of postponed fertility, raising TFR relative to counterfactual without ART.
- **why:** IVF and related technologies let couples who postponed childbearing or face fecundity problems still produce a birth they otherwise could not. Cheap and accessible ART partially undoes the biological penalty of trying to conceive at older ages, so realized fertility ends up closer to desired fertility. The aggregate boost is small because ART accounts for only a few percent of births, but it grows as postponement spreads.
- **phenomena:** SDT
- **seminal:** Leridon 2004, Habbema et al. 2009, Sobotka et al. 2008
- **cross-ref:** Economic
- **notes:** Quantitative contribution small (<5% of births in most OECD) but growing; interacts with postponement hypothesis. Larger in Israel, Denmark. Merged with the Demographic enumerator's `assisted-reproductive-technology` entry — same mechanism.

[Claude, two things:

1. Assisted reproductive technology access. This seems like it’s the same kind of thing as the contraception points above, allowing you to bridge the gap between desired fertility and actual fertility. It doesn’t necessarily mean that desired fertility has fallen, so we need to keep those two concepts separate. It seems like it’s more of the same thing, and I’m not sure whether it belongs under biology or under approximate cause. I think it might belong under approximate cause, because it still leaves open the question of why desired fertility changes over time, and we should explain why that happens.
2.  one potential explanation I haven’t seen yet but that is relevant is that people hypothesize pollution has decreased sperm count, or that something else has. That could be a cause too. I’m skeptical that it is one, though. Have you seen any literature on this, or has it been mentioned on X or in other social media posts ]

### Breastfeeding and Lactational Amenorrhea
- **slug:** `breastfeeding-lactational-amenorrhea`
- **claim:** Longer and more intensive breastfeeding suppresses ovulation via lactational amenorrhea, lengthens birth intervals, and lowers natural fertility; shortening of breastfeeding duration (urbanization, wet-nursing, formula) raises fertility.
- **why:** Intensive breastfeeding suppresses the hormones that drive ovulation, so a nursing mother is naturally less likely to conceive. Long breastfeeding therefore spaces births further apart and lowers a woman's lifetime total even without any deliberate contraception. When wet-nursing, formula, or earlier weaning shorten breastfeeding, this natural brake weakens and fertility rises.
- **phenomena:** PM, FDT
- **seminal:** Bongaarts 1978, Bongaarts and Potter 1983, Konner and Worthman 1980, Wood 1994, Knodel and van de Walle 1967
- **cross-ref:** Cultural
- **notes:** Core 'proximate determinant' in Bongaarts framework; key for explaining hunter-gatherer vs. agriculturalist fertility differences; weakens as wet-nursing/formula spread. Merged with the Demographic enumerator's identical entry.

[Claude, this seems more like a proximate cause than an actual cause. Historically, breastfeeding has actually decreased over time, not increased. The only increase you see is a brief period when people started prioritizing formula over breastfeeding over the last few decades, but now you’ve seen a reversion.

I’m not sure how high it is relative to history, but that point about the long-term trend is a different question from whether it’s a root cause or a proximate cause. I think it’s proximate because it just begs the question of why breastfeeding itself has increased or decreased.

 historically, breastfeeding suppressed fertility because both breastfeeding and having kids were energetically intense, and you could only do one or the other. In the modern world, energy is not really a constraint, so in theory you could do both.

It is possible that, as humans evolved, we adapted a switch between fertility and lactation, which is why that switch still exists even though energy is not a constraint. It is worth keeping that in the background ]

### Coital Frequency and Fecundability
- **slug:** `coital-frequency-biological`
- **claim:** Variation in coital frequency — driven by health, age, cohabitation patterns, spousal separation (labor migration, war), and customary abstinence — alters monthly fecundability and thus realized fertility independently of contraceptive use.
- **why:** Each act of intercourse during a fertile window carries some chance of conception, so a couple's monthly probability of pregnancy scales with how often they have sex. Anything that lowers frequency — long workdays, labor migration that separates spouses, war, illness, customary periods of abstinence, declining libido — mechanically reduces births even when no one is using contraception. This is invoked in recent discussions of falling fertility in Japan, Korea, and the US.
- **phenomena:** PM, FDT, SDT
- **seminal:** Bongaarts 1978, Wood 1989, Leridon 2008, Davis and Blake 1956, Caldwell and Caldwell 1977
- **cross-ref:** Cultural
- **notes:** Bongaarts proximate determinant; declining coital frequency invoked in recent Japan/Korea/US discussions. Merged with the Demographic enumerator's `spousal-separation-coital-frequency` — separation is one driver of the same biological proximate determinant.

[ Claude, this also seems like a proximate cause of people having sex less often. The question is why they are having sex less often, not just that having sex less often means reproducing less often.

If a theory just begs the question of why, and we are left with “why x” every time instead of some explanation (like there is no primitive behind x), then we think of it as a proximate cause. If it just begs the question of why, it is probably a proximate cause ]
### Endocrine Disruptors and Environmental Toxins
- **slug:** `endocrine-disruptors-environmental-toxins`
- **claim:** Exposure to endocrine-disrupting chemicals (phthalates, BPA, pesticides) and other environmental pollutants impairs male and female reproductive function, lowering fecundity and contributing to SDT-era fertility decline.
- **why:** Industrial chemicals like phthalates, BPA, and certain pesticides mimic or block human reproductive hormones, which can lower sperm quality, disrupt ovulation, and impair implantation. If a growing share of the population is biologically less able to conceive, realized fertility falls even when desired fertility does not. Individual-level harm is documented, but whether the cumulative exposure is large enough to move national TFR is contested.
- **phenomena:** SDT
- **seminal:** Colborn et al. 1996, Skakkebaek et al. 2016, Swan et al. 2021
- **cross-ref:** --
- **notes:** Mechanistically plausible at individual level; macro contribution to TFR change highly contested.

### Fetal Loss and Intrauterine Mortality
- **slug:** `fetal-loss-intrauterine-mortality`
- **claim:** Variation in spontaneous abortion and stillbirth rates, driven by maternal health, infection, and nutrition, mechanically alters live-birth fertility across populations and time.
- **why:** Not every pregnancy ends in a live birth — miscarriages and stillbirths intervene at rates that depend on maternal health, infection, and nutrition. Populations with worse maternal conditions lose more pregnancies and therefore record fewer births per woman, even at the same conception rate. Improving maternal health raises the share of conceptions that survive to delivery, mechanically lifting fertility.
- **phenomena:** PM, FDT
- **seminal:** Bongaarts and Potter 1983, Wood 1994, Casterline 1989
- **cross-ref:** --
- **notes:** Proximate determinant; modest aggregate effect but matters for cross-population PM comparisons.

[ Claude, is this a variation on the idea that higher mortality leads to higher fertility? I think we should focus less on which factors are driving the decline in fertility and more on what is driving the decline in the effective fertility rate (i.e., births times survival probability). Otherwise, you just get the translation of how mortality affects fertility, and that falls under that. This is really about what is driving the mortality changes. This is saying fetal loss is one . the question you’re probably asking is: Where does this go? It goes wherever drivers of child mortality go. This is mixing two things:

1. Something that causes a change in child mortality (or mortality more broadly)
2. The translation of mortality into fertility

The translation of mortality into fertility is about the desire for a number of surviving children, with or without an insurance motive. Conceptually, that belongs under drivers of mortality (the proximate cause). When we talk about how that translates into fertility, we’re getting to something deeper about the demand for surviving children, not the number of children, which should be thought of as a preference in economics. I’d put that under evolutionary stuff, which then belongs in biology]

### Genetic and Heritable Variation in Fertility
- **slug:** `heritability-fertility-genetic`
- **claim:** Heritable variation in fertility-related traits (and selection on them) explains a portion of between-individual and between-population fertility differences and may produce a partial fertility rebound over generations.
- **why:** Twin and family studies show that traits influencing how many children people have — fecundity, age at first birth, preferences for large families — are partly inherited. If low-fertility behavior reduces fitness, natural selection should over many generations favor genes associated with higher fertility, producing a slow rebound. The mechanism is real at the individual level but the implied macro effect operates over centuries, not decades.
- **phenomena:** SDT
- **seminal:** Kohler et al. 1999, Kohler et al. 2002, Kosova et al. 2010, Tropf et al. 2015
- **cross-ref:** --
- **notes:** Twin studies show heritability ~0.2-0.4; macro implication speculative; mostly relevant to SDT trajectory.

[ Claude, the fact that variability in fertility rates leads to differences in population growth rates makes sense. A larger population with higher fertility will grow faster, and if it starts larger, the effect will be slightly faster as well. That said, the question is why variability exists in the first place.

I see this as a proximate cause or mechanism. The deeper question is whether there is something that drives some groups to have higher fertility than others. My general sense is that culture might be part of it, but this literature does not really get into the causes of the variability as much as it does the impact of variability ]

### Infectious Disease and Sterility
- **slug:** `infectious-disease-sterility`
- **claim:** Sexually transmitted (gonorrhea, chlamydia, syphilis) and other infections (TB, malaria, schistosomiasis) reduce fecundity through tubal damage, fetal loss, and amenorrhea; disease eradication raised fertility in mid-20th century.
- **why:** Sexually transmitted infections like gonorrhea and chlamydia scar the fallopian tubes, and chronic infections like TB and malaria damage general reproductive function, leaving many women unable to conceive or carry to term. Populations with heavy disease burdens therefore show pockets of involuntary infertility — the sub-Saharan 'infertility belt' is the classic example. When antibiotics and public health campaigns clear these infections, fertility rebounds without any change in desires.
- **phenomena:** PM, FDT
- **seminal:** Romaniuk 1968, Romaniuk 1980, Caldwell and Caldwell 1983, Frank 1983, Retel-Laurentin 1974
- **cross-ref:** --
- **notes:** Central to explaining sub-Saharan 'infertility belt' and post-1950 fertility rebound; minor for Western FDT/SDT. Merged Demographic `infecundity-pathological-sterility` into this Biological entry — same mechanism, biological is primary.

### Maternal Age and Fecundity Decline
- **slug:** `maternal-age-fecundity-decline`
- **claim:** Postponement of childbearing into the 30s and 40s reduces realized fertility because fecundity declines and miscarriage risk rises sharply with maternal age, producing unintended childlessness and lower completed fertility.
- **why:** A woman's monthly chance of conceiving falls steeply after her early 30s, and miscarriage risk rises, so couples who try to have children later end up with fewer than they wanted. When the cultural shift toward later childbearing collides with this biological clock, some intended births simply never happen and unintended childlessness rises. This converts what looks like a behavioral postponement into a real, permanent loss of completed fertility.
- **phenomena:** SDT
- **seminal:** Menken 1985, Leridon 2004, te Velde and Pearson 2002, Schmidt et al. 2012
- **cross-ref:** Demographic
- **notes:** Mechanism for SDT 'postponement transition'; quantitatively important for childlessness rates.

[ Claude, this is a proximate cause. Later maternal age does decrease fecundity, but just begs the question of why maternal age is increasing ]

### Nutrition and Energy Availability
- **slug:** `nutrition-energy-availability`
- **claim:** Higher caloric intake and energy balance raise fecundity (lowering age at menarche, raising ovulatory frequency, reducing fetal loss), increasing fertility; conversely chronic undernutrition suppresses it.
- **why:** Reproduction is energetically expensive, so a woman whose body is short on calories ovulates less reliably, conceives less easily, and is more likely to miscarry. As populations move from chronic undernutrition to adequate or abundant food, women hit menarche earlier, ovulate more regularly, and lose fewer pregnancies, raising natural fertility. The mechanism matters most for pre-modern populations near subsistence; the precise calorie threshold is disputed.
- **phenomena:** PM, FDT
- **seminal:** Frisch 1978, Frisch and McArthur 1974, Ellison 2001, Bongaarts 1980
- **cross-ref:** Economic
- **notes:** Frisch hypothesis is contested at the threshold level; Bongaarts 1980 critiques magnitude; relevant to PM variation and possibly FDT timing.

[ Claude, this is a biological argument for sure, and it’s a deep cause: the availability of energy. The problem is that energy availability is rising at the same time fertility is falling .  we should conclude the explanation, but deprecate it because it does not seem like a first-order, plausible one. A systematic review would likely be very short]

### Obesity and Metabolic Subfecundity
- **slug:** `obesity-metabolic-subfecundity`
- **claim:** Rising obesity and metabolic syndrome impair ovulation, sperm quality, and pregnancy outcomes, reducing realized fertility in late-SDT populations.
- **why:** Severe obesity and the metabolic disorders that travel with it disrupt the hormonal signals that drive ovulation and sperm production, and raise the rate of pregnancy complications. As obesity prevalence climbs in rich countries, a growing share of couples take longer to conceive or fail to conceive at all. The individual-level biology is well established but the aggregate dent in national TFR is probably small.
- **phenomena:** SDT
- **seminal:** Pasquali et al. 2007, Jensen et al. 2004, Practice Committee ASRM 2015
- **cross-ref:** --
- **notes:** Individual-level effects well-documented; aggregate TFR contribution likely modest.

### Paternal Age and Sperm Quality Decline
- **slug:** `paternal-age-sperm-quality`
- **claim:** Rising paternal age and declining sperm count/quality over recent decades reduce couple fecundity and raise time-to-pregnancy, contributing to lower realized fertility in the SDT.
- **why:** Sperm count, motility, and DNA quality decline with male age, and several studies report that average sperm counts have fallen over recent decades across rich countries. Lower sperm quality lengthens the time it takes a couple to conceive and raises the chance they give up before succeeding, especially when paired with older mothers. Whether the trend is real (versus a measurement artifact) and large enough to matter for TFR is debated.
- **phenomena:** SDT
- **seminal:** Carlsen et al. 1992, Levine et al. 2017, Sharpe 2010
- **cross-ref:** --
- **notes:** Sperm-count decline trend disputed methodologically; quantitative contribution to TFR likely small but invoked.

[ in this example, the fact that higher paternal age is associated with lower sperm quality is a proximate cause because it raises the question of why paternal age is increasing. If the reason for lower sperm quality is some environmental factor, that would be a deeper cause (an environmental or biological cause, depending on how we categorize it). Since this example just raises the question of why, it fits the proximate-cause category .  if most of this literature only says sperm quality is falling without explaining why, it would still count as a proximate cause. That’s because it would still leave open the question of why sperm quality is falling ]

## Cultural

### Caldwell Wealth Flows and Cultural Westernization
- **slug:** `caldwell-wealth-flows-westernization`
- **claim:** Mass schooling and Western cultural diffusion reverse the direction of intergenerational wealth flows from upward (children to parents) to downward, eliminating the economic rationale for high fertility through cultural rather than purely economic channels.
- **why:** In traditional settings, children work and support aging parents, so the net flow of resources runs from kids to adults — making big families a good deal. Mass schooling and exposure to Western family ideals flip the script: children become dependents you invest in, not earners who pay you back. Once that cultural reframing takes hold, the rationale for many children evaporates regardless of whether the underlying economics actually changed.
- **phenomena:** FDT
- **seminal:** Caldwell 1976, Caldwell 1980, Caldwell 1982, Thornton 2001
- **cross-ref:** Economic
- **notes:** Thornton's 'developmental idealism' extension is the cultural-mechanism version; Caldwell's underlying wealth-flows theory is filed under Economic (`wealth-flows-reversal`).

### Rise of Child-Centered, Intensive Parenting Norms
- **slug:** `child-centeredness-intensive-parenting`
- **claim:** Cultural shift toward intensive, child-centered parenting raises the time and emotional cost of each child and reduces desired quantity.
- **why:** When the prevailing norm shifts from 'children grow up alongside the household' to 'good parenting means constant attention, enrichment, and emotional investment,' each child becomes vastly more time- and stress-expensive. Parents who internalize this standard feel they can only do it 'right' for a small number of kids. The result is fewer children per couple, not because of explicit prices but because the cultural definition of adequate parenting absorbs more resources per child.
- **phenomena:** SDT
- **seminal:** Hays 1996, Lareau 2003, Doepke and Zilibotti 2019, Ishizuka 2019
- **cross-ref:** Economic
- **notes:** Close to quantity-quality but proximate mechanism is norm change; Doepke-Zilibotti formalize.

### Normalization of Voluntary Childlessness
- **slug:** `childlessness-as-acceptable-choice`
- **claim:** Declining normative pressure to have children at all raises the share of voluntarily childless adults and lowers cohort fertility.
- **why:** Historically, adults who never had children faced social disapproval, pity, or assumptions of failure, which pushed many reluctant parents into childbearing. As that stigma fades, people who do not particularly want children feel free to opt out entirely. This pulls down average fertility through a rising zero-child share rather than through smaller families among parents.
- **phenomena:** SDT
- **seminal:** Hagestad and Call 2007, Merz and Liefbroer 2012, Tanturri and Mencarini 2008, Rowland 2007
- **cross-ref:** --
- **notes:** Distinct from delay; childlessness rising in many SDT settings.

### Consumerism and Aspirational Lifestyles
- **slug:** `consumerism-aspirational-lifestyles`
- **claim:** Diffusion of consumerist aspirations raises the relative valuation of non-child consumption goods and reduces desired fertility (Easterlin relative-income variant with cultural taste shifter).
- **why:** As advertising, media, and peer groups elevate the appeal of travel, dining, gadgets, and status goods, these compete with children for limited budgets and life-narrative space. When 'the good life' is increasingly defined by personal consumption, children look more like a sacrifice of that lifestyle. Tastes — not just prices or wages — shift against family size.
- **phenomena:** FDT, SDT
- **seminal:** Easterlin 1976, Lesthaeghe and Surkyn 1988, Freedman 1979, Caldwell 1976
- **cross-ref:** Economic
- **notes:** Overlaps Easterlin relative-income and Caldwell wealth-flows; primary mechanism here is preference/taste.

### Cultural Evolution and Maladaptive Low Fertility
- **slug:** `cultural-evolution-demographic-transition`
- **claim:** Prestige-biased cultural transmission causes low-fertility behaviors of high-status individuals to spread through the population, producing sub-replacement fertility despite reduced fitness.
- **why:** People imitate high-status individuals: their careers, lifestyles, and family choices. If elites and educated urbanites have fewer children, that low-fertility pattern spreads downward through the population as others copy them, even though copying it reduces the imitators' biological success. Cultural transmission, in this view, can drive fertility well below what evolution would 'want.'
- **phenomena:** FDT, SDT
- **seminal:** Boyd and Richerson 1985, Richerson and Boyd 2005, Newson et al. 2005, Colleran 2016
- **cross-ref:** Biological
- **notes:** Evolutionary-cultural account of why fertility falls below replacement; complements Lesthaeghe.

### Deinstitutionalization of Marriage and Family
- **slug:** `deinstitutionalization-of-marriage`
- **claim:** Weakening of marriage as a normative institution (rising cohabitation, divorce, nonmarital childbearing acceptance) decouples partnership from childbearing and lowers completed fertility on net through delay and partnership instability, while recomposing the share of births outside marriage.
- **why:** When marriage was the near-universal gateway to sex, cohabitation, and childbearing, weakening it would just shift births outside marriage. But the decline of marriage also brings less stable partnerships, more time spent searching or single, and more postponement of commitments — and births tend to happen inside stable unions. On net, the looser linkage between partnership and parenthood lowers completed fertility, even where nonmarital childbearing rises.
- **phenomena:** SDT
- **seminal:** Cherlin 2004, Lesthaeghe 1995, van de Kaa 1987, Perelli-Harris et al. 2010, Kiernan 2001, Lesthaeghe and van de Kaa 1986
- **cross-ref:** Demographic
- **notes:** Tightly bound to SDT; effect on TFR ambiguous in some Nordic settings (high cohabiting fertility). Merged with the Demographic enumerator's `marriage-decline-cohabitation` — same SDT phenomenon, cultural framing is primary.

### Developmental Idealism
- **slug:** `developmental-idealism`
- **claim:** Global diffusion of a package of beliefs equating modernity with the nuclear family, gender equality, late marriage, and low fertility causes fertility decline independently of structural change.
- **why:** A bundle of beliefs — that being 'modern' means small nuclear families, gender equality, late marriage, and educated children — has spread globally through schools, media, and development institutions. Once people in a society absorb this package as the definition of progress, they aspire to it regardless of whether their local economy has actually modernized. Fertility falls because people want to look modern, not necessarily because incomes or technology changed.
- **phenomena:** FDT, SDT
- **seminal:** Thornton 2001, Thornton 2005, Binstock and Thornton 2007
- **cross-ref:** --
- **notes:** Explicitly cultural-diffusion theory; testable via attitude surveys across cohorts/countries.

[ Claude, Developmental Idealism overlaps to some extent with some of the items in the cultural category you summarized earlier. Let’s make sure we are not creating too many different explanations that are essentially the same but phrased slightly differently. See whether this should be folded into one of the ones above  within the culture category ]

### Female Education as Cultural Empowerment
- **slug:** `female-education-empowerment-norm-channel`
- **claim:** Female schooling reduces fertility through its effect on aspirations, autonomy, and ideational change, beyond the wage/opportunity-cost channel.
- **why:** Schooling does more than raise a woman's wages: it changes how she sees herself, what she thinks is possible, and how much say she has in household decisions. Educated women are more likely to question inherited expectations about big families and to negotiate for contraception, later marriage, and their own ambitions. This ideational shift lowers fertility above and beyond the pure opportunity-cost-of-time story.
- **phenomena:** FDT, SDT
- **seminal:** Jejeebhoy 1995, Basu 2002, Kravdal 2002, Lutz and Skirbekk 2014
- **cross-ref:** Economic
- **notes:** Primary education effect on fertility is hard to explain via wages alone -> empowerment/ideational channel.

[ Claude, isn't this just another feminism argument or feminism explanation within culture? It just so happens that the mechanism is female, like education, right ?]
### Gender Equity Norms and Female Autonomy
- **slug:** `gender-equity-norms`
- **claim:** Diffusion of egalitarian gender norms increases female bargaining power and autonomy over reproductive decisions, reducing fertility under FDT and raising it under SDT once household-level equity catches up (gender revolution U-curve).
- **why:** As norms move toward treating women as equal in public life — school, work, politics — women gain leverage over reproductive choices and often cut fertility. But if home life stays unequal (women still do all the housework and childcare), having kids becomes punishingly costly for women, pushing fertility very low. Only when equity also reaches inside the household do births recover, producing a U-shape between gender equality and fertility.
- **phenomena:** FDT, SDT
- **seminal:** Mason 1987, McDonald 2000, Goldscheider Bernhardt Lappegard 2015, Esping-Andersen and Billari 2015
- **cross-ref:** Economic
- **notes:** Two-stage 'gender revolution' hypothesis; tests U-shape in cross-country TFR-vs-equity.

[ Claude, this could be broadly folded into feminism  which is one of the cultural explanations ]
### Norms Governing Premarital Sex and Nonmarital Fertility
- **slug:** `honor-shame-premarital-sex-norms`
- **claim:** Cultural norms restricting premarital sex and stigmatizing nonmarital fertility raise age at marriage and channel fertility into marriage, lowering completed fertility where marriage is delayed or forgone.
- **why:** In cultures that strictly forbid sex outside marriage and stigmatize nonmarital births, the only legitimate path to children runs through wedlock. If marriage is delayed (waiting to afford a household) or some never marry, those years and people produce no births at all. Channeling all reproduction through marriage thus mechanically depresses total fertility wherever marriage is hard to enter.
- **phenomena:** PM, FDT, SDT
- **seminal:** Hajnal 1965, Laslett 1977, Goode 1963, Wrigley and Schofield 1981
- **cross-ref:** Demographic
- **notes:** Mechanism behind European Marriage Pattern; cross-references to nuptiality.

[ Claude, can this be folded into the decline in value of marriage, etc., or is it distinct? There are a bunch of specific flavors of the idea that marriage is not central to life, or that having children is not highly valued, and this is related to that . ]

### Ideational Diffusion via Mass Media
- **slug:** `ideational-diffusion-mass-media`
- **claim:** Exposure to mass media (radio, TV, soap operas) diffuses small-family norms and aspirational lifestyles incompatible with high fertility, lowering desired and actual fertility.
- **why:** Radio, television, and especially serialized dramas show viewers aspirational lives — small families, working women, urban consumption — that quietly reframe what a normal family looks like. Exposure shifts viewers' own desired family size downward, even controlling for income and education. Media essentially imports low-fertility norms into places they had not previously reached.
- **phenomena:** FDT, SDT
- **seminal:** Westoff and Bankole 1997, La Ferrara Chong Duryea 2012, Jensen and Oster 2009, Kearney and Levine 2015
- **cross-ref:** --
- **notes:** Brazil/India quasi-experimental evidence is strong micro-causal; macro share contested.

[ Claude, same argument here. This seems to overlap a bit. The main thing that might distinguish it from Western idealism or development idealism above is that it points out a mechanism for dispersion (TV), so it is really a mechanism within the cultural argument, right?]

### Rise of Individualism and Self-Realization
- **slug:** `individualism-rise`
- **claim:** Cultural shift toward individualism and self-realization raises the perceived opportunity cost of children relative to non-family pursuits and reduces fertility.
- **why:** As culture elevates personal autonomy, self-realization, and 'living one's own life' over duty to family or lineage, children look less like a natural life stage and more like one option that trades off against others. The same person who in an earlier era would have had three kids without much deliberation now weighs whether parenthood fits their identity. Fertility falls because the calculus itself becomes individual rather than ascribed.
- **phenomena:** FDT, SDT
- **seminal:** Lesthaeghe 1983, Lesthaeghe and Surkyn 1988, Surkyn and Lesthaeghe 2004, Coale 1973
- **cross-ref:** Economic
- **notes:** Coale's 'fertility within calculus of conscious choice' precondition; overlaps with SDT thesis.

[ Claude, same as above. There’s a lot of overlap here. We should synthesize these into a smaller number of categories and explain the different flavors within each one, rather than breaking each one out into a separate stream ]
### Intergenerational Transmission of Fertility Preferences
- **slug:** `intergenerational-transmission-fertility`
- **claim:** Fertility preferences and family-size norms are transmitted vertically from parents to children, producing persistence and slow adjustment of fertility across generations.
- **why:** Kids absorb their parents' attitudes about ideal family size, gender roles, and the meaning of children, and they tend to reproduce those patterns when they become adults. This vertical transmission makes fertility sticky: a society with high-fertility grandparents takes generations to fully adjust, even after underlying conditions change. It explains persistence and slow convergence rather than the direction of change.
- **phenomena:** PM, FDT, SDT
- **seminal:** Murphy 1999, Murphy and Knudsen 2002, Kolk 2014, Fernandez and Fogli 2009
- **cross-ref:** --
- **notes:** Epidemiological approach (Fernandez-Fogli) uses immigrants to isolate culture from environment.

[Claude, I buy that this is true. The thing is, it doesn’t tell you whether you’ll have an increase or a decrease. It’s more of a mechanism or an approximate cause than anything else.]
### Kinship Systems and Family Structure
- **slug:** `kinship-systems-family-structure`
- **claim:** Pre-existing kinship structures (nuclear vs. joint family, patrilineal vs. bilateral, European Marriage Pattern) shape baseline fertility and the timing and pace of transitions.
- **why:** How a society organizes families — whether young couples form their own households or join the husband's parents, whether inheritance flows through one line or both — sets the baseline cost and benefit of children. Joint patrilineal systems with early universal marriage tend to produce high fertility; nuclear systems requiring couples to accumulate resources before marriage produce later marriage and lower fertility. These deep structures shape where transitions start and how fast they move.
- **phenomena:** PM, FDT
- **seminal:** Hajnal 1965, Hajnal 1982, Das Gupta 1999, Todd 1985, Reher 1998
- **cross-ref:** Demographic
- **notes:** Hajnal line and European Marriage Pattern central to PM variation; Reher 'strong/weak family' for SDT variation.

[ Claude, this does belong within culture, except that it's more historical than present, I think. Tell me if I'm wrong ]

### Linguistic and Cultural Boundaries (Princeton European Fertility Project)
- **slug:** `linguistic-cultural-boundaries-princeton`
- **claim:** Onset and pace of the fertility transition cluster along linguistic, religious, and cultural boundaries rather than economic ones, implying culture-driven diffusion of fertility control.
- **why:** When researchers mapped the timing of European fertility decline, they found it lined up with language and religion more than with industrialization or income. Neighboring regions at similar economic levels but different cultures transitioned decades apart, while culturally similar regions transitioned together even when economically different. This pattern suggests fertility control spread as an idea through cultural communities, not as a mechanical response to economic conditions.
- **phenomena:** FDT
- **seminal:** Coale and Watkins 1986, Knodel and van de Walle 1979, Lesthaeghe 1977, Watkins 1991
- **cross-ref:** --
- **notes:** Foundational empirical case for culture; subsequent reanalyses (Brown-Guinnane, Galor-Klemp) qualify.

[Claude, this point is mainly about how culture matters more than other things, so it falls under the culture category, but it is not a specific explanation. It is more about the mechanisms within culture. ]

### Nationalist and Pronatalist Ideology
- **slug:** `nationalism-pronatalist-ideology`
- **claim:** State-sponsored nationalist and pronatalist ideology raises fertility by normatively framing childbearing as patriotic duty (e.g., interwar Europe, postwar baby booms, contemporary Hungary/Russia).
- **why:** States sometimes frame having children as a patriotic act — bolstering the nation, the race, or the workforce — through propaganda, awards, and moral rhetoric. When citizens internalize this framing, some who would otherwise have stopped at fewer children have an additional one. Effects tend to be modest and short-lived, though, because ideology alone does not pay the bills of raising the extra child.
- **phenomena:** FDT, SDT
- **seminal:** Quine 1996, King 1998, Demeny 1986, Gauthier 1996
- **cross-ref:** Economic
- **notes:** Hard to separate ideology from accompanying transfers; mostly small/transient effects in modern data.

### Secular Ideational Shift (Second Demographic Transition Thesis)
- **slug:** `secular-ideational-shift`
- **claim:** A secular shift from materialist/conformist values toward postmaterialist values emphasizing self-actualization, autonomy, and individual choice reduces desired fertility and delays/forgoes childbearing.
- **why:** Postwar affluence freed people from worrying about survival, and values shifted toward self-expression, autonomy, and personal fulfillment. In that value system, children — especially many of them — compete with adult goals like career, travel, and self-discovery. Fertility falls because the underlying picture of a good life no longer centers on a large family.
- **phenomena:** SDT
- **seminal:** Lesthaeghe and van de Kaa 1986, van de Kaa 1987, Lesthaeghe 1983, Lesthaeghe 2010, Inglehart 1977
- **cross-ref:** --
- **notes:** Canonical SDT framework; criticized as descriptive rather than causal; hard to separate from income/security mechanisms.

[ Claude, again, there’s a lot of overlap even with this one and the prior ones. The main difference here is that this is the canonical explanation for the second demographic transition. Beyond that, it’s just cultural explanations. Within culture, you might have some focused on the first transition or the second transition, but overall it’s still a culture of a particular type (secularization, autonomy, etc.) ]
### Secularization and Decline of Religiosity
- **slug:** `secularization-religiosity-decline`
- **claim:** Declining religious belief, practice, and authority of pronatalist religious institutions lowers fertility by weakening normative prescriptions against contraception, nonmarital sex, and small families.
- **why:** Most major religions actively encourage childbearing and discourage contraception, abortion, and nonmarital sex. As religious belief and the authority of clergy fade, these prescriptions lose their grip, and people feel free to limit family size and use whatever methods are available. Religion's retreat thus removes a normative floor under fertility.
- **phenomena:** FDT, SDT
- **seminal:** Lesthaeghe and Wilson 1986, McQuillan 2004, Frejka and Westoff 2008, Norris and Inglehart 2004
- **cross-ref:** --
- **notes:** Strong cross-sectional gradient; reverse causality (low fertility -> less religion) is a concern.

[While I'm seeing my comments above, I'm repeating myself.]
### Social Network and Peer Effects on Fertility
- **slug:** `social-network-peer-effects`
- **claim:** Fertility behavior diffuses through peer and kin networks via social learning and social influence, generating contagion in birth timing and parity.
- **why:** People decide when and whether to have kids partly by watching their siblings, friends, and coworkers — both for information ('the IUD worked fine for her') and for social cues ('everyone is waiting until 32 now'). This creates contagion: once a few people in a network shift behavior, others follow, and birth timing or family size moves in clusters. The mechanism explains why fertility transitions can accelerate suddenly rather than tracking economic fundamentals smoothly.
- **phenomena:** PM, FDT, SDT
- **seminal:** Bongaarts and Watkins 1996, Kohler 2001, Kohler Behrman Watkins 2001, Montgomery and Casterline 1996, Balbo and Barban 2014
- **cross-ref:** --
- **notes:** Mechanism behind diffusion models; identification of peer effects vs. correlated environments is hard.

[ Claude, this shows the culture is important. It's more about the mechanism showing the culture matters, not so much saying what part of culture has changed ]
### Son Preference and Gender-Biased Fertility Norms
- **slug:** `son-preference-cultural`
- **claim:** Cultural preference for sons sustains higher fertility (continued childbearing until a son is born) and shapes parity progression, sex-selective stopping rules, and sex-selective abortion practices.
- **why:** In cultures where sons carry the family name, inherit, or support parents in old age, couples who only have daughters keep trying for a boy. This 'try until you get a son' rule mechanically raises fertility above what couples would choose if they were indifferent to sex. When sex-selective abortion becomes available, the same preference shows up as skewed sex ratios instead of more births, partly defusing the fertility effect.
- **phenomena:** PM, FDT, SDT
- **seminal:** Das Gupta 1987, Arnold Choe Roy 1998, Clark 2000, Jayachandran 2017, Ben-Porath and Welch 1976
- **cross-ref:** Demographic
- **notes:** Quantitatively large in South/East Asia; eroded by sex-selective abortion in SDT settings. Merged with the Demographic enumerator's `son-preference-stopping-rules` — same mechanism, cultural primacy.

### Reduction in Stigma Around Contraception and Abortion
- **slug:** `stigma-reduction-contraception-abortion`
- **claim:** Cultural legitimation of contraception and abortion (independent of technological availability) lowers fertility by enabling latent demand for fertility control to be realized.
- **why:** Even when contraception is technically available, people often will not use it if their neighbors, clergy, or families would judge them harshly. As cultural disapproval of contraception and abortion fades, latent demand for fertility control finally translates into actual use. Fertility falls not because the technology changed but because the social cost of using it dropped.
- **phenomena:** FDT, SDT
- **seminal:** Cleland and Wilson 1987, Bongaarts and Watkins 1996, Goldin and Katz 2002, Lesthaeghe 1983
- **cross-ref:** Biological
- **notes:** Cleland-Wilson 'ideational' argument vs. Easterlin demand-side; distinguishing norm from technology is hard.

---

## Merge notes

- Total proposed across all 4 enumerators: 75 (Demographic 18 + Economic 23 + Biological 12 + Cultural 22)
- After dedup/normalization: 60 (Demographic 12 + Economic 21 + Biological 12 + Cultural 15)
- Cross-category resolutions:
  - `breastfeeding-lactational-amenorrhea` — proposed by both Demographic and Biological enumerators. Kept under Biological (proximate biological mechanism per Bongaarts); cross-ref Cultural (wet-nursing/formula norms).
  - `infectious-disease-sterility` (Biological) absorbed Demographic's `infecundity-pathological-sterility`. Kept under Biological; same mechanism (STI/disease-induced sterility), biological is primary.
  - `coital-frequency-biological` (Biological) absorbed Demographic's `spousal-separation-coital-frequency`. Spousal separation is a behavioral driver of the same biological proximate determinant (fecundability); kept under Biological with cross-ref Cultural.
  - `art-access-fertility-recovery` (Biological) absorbed Demographic's `assisted-reproductive-technology`. Same mechanism; biological primary, cross-ref Economic (access/cost).
  - `tempo-effects-birth-postponement` (Demographic) absorbed Economic's `tempo-postponement-economic`. Demographic accounting framing is primary; economic drivers of timing folded into notes/seminal; cross-ref Economic.
  - `contraceptive-technology-diffusion` (Demographic) absorbed Economic's `contraception-cost-economic`. Same technology shock; demographic primary, cross-ref Economic.
  - `urbanization-residential-shift` (Economic) merged with Demographic's `urbanization-residential-shift`. Per PROTOCOL §3 the primary mechanism is the economic value of children in urban production; filed under Economic, demographic listed as cross-ref. Slug kept; scope expanded to include composition + child-labor devaluation.
  - `son-preference-cultural` (Cultural) absorbed Demographic's `son-preference-stopping-rules`. Cultural preference is the primary mechanism; sex-selective stopping is the behavioral expression. Cross-ref Demographic.
  - `deinstitutionalization-of-marriage` (Cultural) absorbed Demographic's `marriage-decline-cohabitation`. Same SDT phenomenon; cultural normative shift is primary mechanism. Cross-ref Demographic.
  - `wealth-flows-reversal` (Economic) and `caldwell-wealth-flows-westernization` (Cultural) kept as **separate** entries: economic version is Caldwell's structural-economic mechanism; cultural version is Thornton's developmental-idealism extension. Each cross-refs the other to make the distinction explicit. Borderline call — flag for PI.
  - `marriage-timing-age-at-marriage` (Demographic), `kinship-systems-family-structure` (Cultural), and `honor-shame-premarital-sex-norms` (Cultural) overlap on the European Marriage Pattern but operate at different layers (proximate nuptiality vs. structural kinship vs. sexual norms). Kept as three entries with mutual cross-refs.
  - `diffusion-of-fertility-control` (Demographic, behavioral spread), `stigma-reduction-contraception-abortion` (Cultural, norm legitimation), `social-network-peer-effects` (Cultural, peer mechanism), and `ideational-diffusion-mass-media` (Cultural, media channel) are related but mechanistically distinct (channel: networks vs. norms vs. media). Kept as four entries.
  - `easterlin-relative-income` (Economic), `rising-inequality-and-status-competition` (Economic), and `consumerism-aspirational-lifestyles` (Cultural) all invoke relative consumption/aspiration. Kept as three entries since the proximate driver differs (cohort size vs. inequality level vs. cultural taste).
- Hypotheses surprising in their absence:
  - **War, conscription, and military mobilization** as a direct fertility shock (vs. only via sex ratios) — not enumerated despite a large historical-demography literature.
  - **Famine and acute mortality crises** as proximate fertility suppressors in PM (Wrigley/Schofield short-run dynamics) — only implicit in Malthusian-land hypothesis.
  - **Climate and ecological shocks** (drought, monsoon failure) as PM/early-modern fertility drivers — absent despite Galor-Ashraf-style literature.
  - **State capacity, conscription registries, and vital statistics infrastructure** as enabling/constraining factors — absent.
  - **Epidemics and pandemics** (Black Death, 1918 flu, AIDS) as fertility shocks — only implicit under infectious-disease-sterility, which focuses on chronic STI burden.
  - **Air pollution and ambient environmental quality** as fecundity reducers (distinct from endocrine disruptors) — not separated out.
  - **Religious-pronatalist subgroup high fertility** (Haredi, LDS, Amish) as a counter-SDT force — absent.
  - **Same-sex partnership and LGBTQ family formation** effects on aggregate fertility — absent.
  - **Migration and immigrant fertility convergence/divergence** — absent as a distinct hypothesis despite large literature.
  - **Polygyny** as a PM fertility-suppressing institution (co-wife competition for coital access) — absent.
