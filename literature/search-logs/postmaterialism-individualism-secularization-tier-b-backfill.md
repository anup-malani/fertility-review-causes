# D.1.a — Tier-B frame backfill

Run by `99_d1a_backfill_gold.py` against Crossref, repairing two defects found by inspecting the assembled frame rather than reported by the assembly.

| | before | after |
|---|---|---|
| records with a DOI | 385 | **321** |
| records with an abstract | 178 (35%) | **202 (50%)** |
| titles that are really citation strings | 27 | **22** |
| distinct works after post-enrichment dedup | 495 | **400** |

- duplicate works removed by pass 3: **95** — enrichment rewrites titles to the provider's canonical form, so records that were distinct strings when `98_` deduplicated become the same work afterwards. This inflated the Tier-B count, the A6a positive class, the A6b recall denominator, and the round-2 saturation yield.
- DOIs recovered by bibliographic query: **31** of 110 attempted
- of those, citation strings replaced with the real title: **5**
- abstracts added: **73**
- refused by the matching guard, kept title-keyed: **79**

Records the guard refused are **kept in the frame and in the recall denominator**, keyed on their original string. Dropping them would bias recall toward easy-to-find papers, and assigning them a best-guess DOI is how the OAS run acquired a 40%-ghost Tier B.

## Refused by the guard (sample of 15)

- B Arpino G Esping-Andersen L Pessin The diffusion of gender egalitarian values and fertility. The Fertility Gap in Europe: Singularities of   — `no Crossref candidate cleared the guard`
- Policy implications of cultural shifts and enduring low fertility in Iran  — `no Crossref candidate cleared the guard`
- The social and cultural determinants of the fertility rate among Congolese refugee women living in the inner city of Durban, South Africa.  — `no Crossref candidate cleared the guard`
- Attitudes toward fertility and childbearing among childless female teachers working in the Gorgan education system in 2023  — `no Crossref candidate cleared the guard`
- Fertility and religious belief: Old and new relationships in Slovakia  — `no Crossref candidate cleared the guard`
- What is the influence of childhood exposure to cultural norms? The role of segregation and community composition in explaining migrant ferti  — `no Crossref candidate cleared the guard`
- The Contraceptive Revolution and the Second Demographic Transition: An Economic Model of Sex, Fertility, and Marriage  — `no Crossref candidate cleared the guard`
- Fertility norms in a dynamic and cross-national perspective  — `no Crossref candidate cleared the guard`
- Politics, Culture and Fertility Trends.  — `no Crossref candidate cleared the guard`
- Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related behaviour  — `no Crossref candidate cleared the guard`
- Attitudes that Differentiate Alternative Family Sizes  — `no Crossref candidate cleared the guard`
- Very Low Fertility in Japan and Value Change Hypotheses  — `no Crossref candidate cleared the guard`
- Postmodern fertility preferences: from changing value orientation to new behaviour  — `no Crossref candidate cleared the guard`
- Religion work-family gender ideology and fertility.  — `no Crossref candidate cleared the guard`
- WOMEN'S FERTILITY, RELIGION AND EDUCATION  — `no Crossref candidate cleared the guard`

## Recovered (sample of 15)

- How Do Changes in Gender Role Attitudes Towards Female Employment Influence Fertility? A Macro-Level Analysis  → `10.1093/esr/jcv002` (containment 0.91, contained, no year in source to check)
- Fertility and Faith: The Demographic Revolution and the Transformation of World Religions by Philip Jenkins  → `10.1353/lut.2021.0108` (containment 1.0, contained, no year in source to check)
- Recent fertility decline in Eritrea  → `10.4054/demres.2008.18.2` (containment 0.8, contained, no year in source to check)
- The Role of Cultural Changes in the Tendency to Childbearing Among Women  → `10.32598/jrh.10.2.6` (containment 1.0, contained, no year in source to check)
- Is There a Stronger Association Between Children and Happiness Among the Religious? Religion as a Moderator in  → `10.1007/s10902-016-9798-x` (containment 0.89, contained, no year in source to check)
- Religion and fertility: The French connection  → `10.4054/demres.2015.32.13` (containment 1.0, contained, no year in source to check)
- Religion and Fertility: Arab Christian-Muslim Differentials.  → `10.2307/2174061` (containment 1.0, contained, no year in source to check)
- Low Fertility in Japan, South Korea, and Singapore  → `10.1007/978-981-15-2830-9` (containment 0.88, contained, no year in source to check)
- What Has Religion Got to Do With It?*  → `10.1097/ccm.0000000000001920` (containment 0.88, contained, no year in source to check)
- Demographic fertility research: a question of disciplinary beliefs and methods  → `10.1332/policypress/9781847420411.003.0008` (containment 1.0, contained, no year in source to check)
- Religiousness and Fertility among European Muslims  → `10.1111/j.1728-4457.2007.00197.x` (containment 0.83, contained, no year in source to check)
- The Influence of Changes in Women's Religious Affiliation on Contraceptive Use and Fertility Among the Kassena  → `10.1111/j.1728-4465.2009.00194.x` (containment 0.9, contained, no year in source to check)
- Applicability of the second demographic transition in Asia  → `10.1007/s42379-022-00120-1` (containment 0.88, contained, no year in source to check)
- The Two-Child Policy and Fertility  → `10.4324/9781003429661-10` (containment 0.83, contained, no year in source to check)
- Relationship Between the Attitude and Motivation of Nurses and Midwives Working in Ahvaz Hospitals Regarding C  → `10.32598/qums.20.1577.4` (containment 0.83, contained, no year in source to check)

