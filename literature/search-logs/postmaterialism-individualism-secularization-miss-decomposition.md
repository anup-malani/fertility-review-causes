# D.1.a — why the remaining gold is missing: query hole or index gap?

The v2 pull recovered all three Tier-1 natural experiments and took Recall(A-only) to 94.7% and both-channels to 100%, but Recall(B-only) moved only 80.8 → 82.4. **Before another repair round, the residue has to be split**, because the halves point opposite ways: a query hole is fixable and argues for iterating, an index gap is a ceiling no query can pass and belongs in §10.

Entity lookup by DOI is **free** under OpenAlex's pricing, so every missed record carrying a DOI is checked directly. A provider refusal is recorded as `UNCONFIRMED` and counted as neither half — a refusal is not an absence.

- gold records: **412**
- missing from the corpus: **68**
- **INDEX_GAP** (not in OpenAlex at all — unfixable by any query): **0**
- **QUERY_HOLE** (in OpenAlex, query did not reach it — fixable): **21**
- **INDEX_GAP_PROBABLE** (no DOI, and no title match either): **19**
- **GOLD_DEFECT** (the stored 'title' is a citation string — cannot match by title, and is a defect in our gold set rather than in OpenAlex): **24**
- unconfirmed (provider refused): 4

**Recall ceiling: between 88.6% and 100.0%.** Reported as a bound rather than a number, because 28 record(s) could not be tested either way and the width IS the uncertainty. Treating untested records as present would give a falsely clean ceiling.

## Query holes — in OpenAlex, not retrieved — 21

*These are the addressable ones. The OpenAlex title is shown because it is what the query would have had to match, and it is often not the title the gold set stored.*

- Changing Attitudes toward Marriage and Children in Six Countries
- Navigating fertility, reproduction and modern contraception in the fragile context of South Kivu, Democratic Republic of
- Gender and fertility within the free churches in the Sundsvall region, Sweden, 1860–1921
- Tacit consent: the Church and birth control in northern Italy.
- Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related behaviour
  - OpenAlex holds it as: *Reproductive decision-making in a macro-micro perspective: report on analysis of ESS data on cross-national differences *
- Recent fertility decline in Eritrea
- Religiosität und Fertilität: eine empirische Untersuchung des Einflusses von Religiosität auf Elternschaft und Kinderzah
- Low Fertility in Japan, South Korea, and Singapore
  - OpenAlex holds it as: *Low fertility in Japan, South Korea, and Singapore : population policies and their effectiveness*
- Cultural policy regimes and arts councils. The longue durée perspective, birth of the state, religious trajectories and 
  - OpenAlex holds it as: *Cultural policy regimes and arts councils. The<i>longue durée</i>perspective, birth of the state, religious trajectories*
- Applicability of the second demographic transition in Asia
- Religion and Religiosity
  - OpenAlex holds it as: *Psychological Perspectives on Religion and Religiosity*
- Overview Chapter 6: The diverse faces of the second demographic transition in Europe.
- Marriage and Fertility Behaviour in Japan
- Between legacy and change: second-child fertility intentions among Chinese mothers in the post-one-child era.
- Kinship and fertility: Brother and sibling effects on births in a patrilineal system
- Between identity and assimilation: Jewish fertility in nineteenth-century Venice
- Sex roles, values of children, and fertility
  - OpenAlex holds it as: *Sex Roles, Value Of Children And Fertility*
- Changing value of children: An action theory of fertility behavior, intergenerational relationships in cross-cultural co
- Female Labour Market Participation and Cultural Variables
- Religion, spirituality and the social sciences
- Polygyny and reproductive behavior in sub-saharan Africa: A contextual analysis

## Probably not indexed — no DOI and no title match — 19

*Stated as PROBABLE and never as proven: an unindexed title and a title our normaliser cannot match look identical from here.*

- Attitudes toward fertility and childbearing among childless female teachers working in the Gorgan education system in 20
- Attitudes that Differentiate Alternative Family Sizes
- TELEVISION, VALUE CONSTRUCTS, AND REPRODUCTIVE BEHAVIOR IN BRAZILIAN “EXCLUDED” COMMUNITIES
- Fertility by ethnic and religious groups in the UK, trends in a trans-national context
- Religion and Fertility in the United States : A Geographic Analysis
- Fertility in Western Europe: the role of religion
- The Two-Child Policy and Fertility
- Observations of Chinese Culture of Marriage and Childbearing in the Context of Low Fertility
- Écarts de fécondité en fonction du niveau d’instruction : le rôle de la religion en Grande-Bretagne et en France
- Hackett Conrad. 2008. “Religion and Fertility in the United States.” PhD dissertation, Princeton University.
- Akintunde MO, Lawal MO, Simeon O. Religious roles in fertility behaviour among the residents of Akinyele local governmen
- Dalla Zuanna, G. (2004a). Few children in strong families: Values and low fertility in Italy. Genus, 60, 39–70.
- Book Translations as Idea Flows: The Effects of the 42 Other literature has studied the spread of fertility norms throug
- Value of children and fertility strategies in cross-cultural comparison. Ideal family size and targeted fertility in ele
- De invloed van levensloopkenmerken en waardenoriëntaties op vrijwillige kinderloosheid [The influence of life course cha
- Development, value of children, and fertility: A multiple indicator approach
- Barbara Anderson, "Regional and Cultural Factors in the Decline of Marital Fertility in Europe," in The Decline of Ferti
- The e ect of norms on fertility and its implications for for the quantity-quality trade-o in Pakistan
- Fertilität in Israel und Palästina. Ein Erklärungsbeitrag der value of children-Forschung

## Gold-set defects — the stored title is a citation string — 24

*A3 found 27 of these; they cannot match by title however complete the index is. They depress measured Recall(B-only) without saying anything about coverage, and they should be repaired in the gold set rather than chased in the query.*

- B Arpino G Esping-Andersen L Pessin The diffusion of gender egalitarian values and fertility. The Fertility Gap in Europ
- Laamanen VM (2024) Changes in work and family attitudes over birth cohorts and links to childfree ideals in Finnish wome
- Lappegard, T., Neyer, G., & Vignoli, D. (2015). Three Dimensions of the Relationship between Gender Role Attitudes and F
- van de Kaa, D. J. (2001). Postmodern fertility preferences: From changing value orientation to new behavior. Population 
- Lutz W (1987) Culture, religion, and fertility: a global view. Genus 15–35
- Abbasi-Shavazi, M., & Khajehsalehi, Z. (2020). An assessment on the impact of women’s autonomy, education and social par
- Jeffery, P., & Jeffery, R. (2000). Religion and fertility in India. Economic and Political Weekly, 35, 3253–3259.
- Mahmoudian, H., & Nobakht, R. (2010). Religion and fertility: Analysis of fertility behavior of Sunni and Shiite religio
- Jeppsen, C. (2015). Religion, gender equality, and fertility. [Unpublished Doctoral Dissertation]. The Pennsylvania Stat
- Kaufmann, E. (2009). Islamism, religiosity and fertility in the Muslim world. Paper presented at the annual meeting of t
- Simons, J. (1986). How conservative are british attitudes to childbearing. Quarterly Journal of Social Affairs, 2, 415–4
- Ishak, P. W., and Gradstein, M. 2022. Losing my Religion (or Maybe not): Religion and Fertility Patterns in Africa.
- Westoff, C. F., and Bietsch, K. 2015. Religion and Reproductive Behavior in Sub-Saharan Africa. DHS Analytical Studies. 
- Larsson, M. (1984). Fruktsamhetsmönster, produktionsstruktur och sekularisering: en jämförelse mellan 69 härader vid 180
- Lesthaeghe, R. & Wilson, C. (1986). Modes of production secularization and the pace of the fertility decline in Western 
- Voas, D., & Doebler, S. (2011). Secularization in Europe: Religious change between and within birth cohorts. Religion an
- Pearce, L. D. (2000). The multidimensional impact of religion on childbearing preferences and behavior in Nepal. Ph.D., 
- Suwal, J. V. (2001). Socio-cultural dynamics of first birth intervals in Nepal. Contribution to Nepalese Studies, 28(1),
- Fawcett, J.T. ( 1976). The value and cost of children: Converging theory and research. In L. T. Ruzicka (Ed.), The econo
- Nauck, B. ( 2005). Changing value of children: An action theory of fertility behavior and intergenerational relationship
- Heineck, G. (2006). The relationship between religion and fertility: Evidence for Austria. PER Working Paper 06-01.
- van de Kaa, D. (1998). Postmodern fertility preferences: From changing value orientation to new behaviour. Working Paper
- Berghammer, C. (2009). Causality between religiosity and childbearing: Evidence from a Dutch panel study. Paper presente
- Liefbroer, A. C., & Merz, E.-M. (2009). Report on analysis of ESS data on cross-national differences in perceived norms 

## Unconfirmed — the provider refused — 4

*A refusal is not an absence. Counted as neither half.*

- What Has Religion Got to Do With It?*
- Peer effects of fertility intentions in the context of the second demographic transition: the impact of social interacti
- Institutional identity, fertility choice and comprehensive two-child policy optimization-evidence from China
- Gegen den Strom der Zeit? Vom Einfluss der religiösen Zugehörigkeit und Religiosität auf die Geburt von Kindern und die 

