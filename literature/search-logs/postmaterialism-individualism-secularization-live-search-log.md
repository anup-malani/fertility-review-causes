# D.1.a — live production pull (GACS C1)

OpenAlex `title.search`, **title-only**, one cursor-paginated stream per cluster, union across clusters. Title-only because that is the operationalisation A6b's cross-validation selected; abstracts enter at the screen, not the search.

- union corpus: **17,281** distinct records
- sum of per-cluster counts: 18,128 (upper bound — clusters overlap by design)
- overlap collapsed by dedup: **847**
- incomplete clusters: **none**
- budget exhaustion: **none**

| cluster | universe | pulled | pages | complete |
|---|---|---|---|---|
| `S1_POSTMATERIALISM` | 330 | 330 | 2 | yes |
| `S2_INDIVIDUALISM` | 841 | 841 | 5 | yes |
| `S3_SECULARIZATION` | 3,058 | 3,058 | 16 | yes |
| `S4_CHILDLESSNESS_NORM` | 2,221 | 2,221 | 12 | yes |
| `S5_CONSUMERISM` | 445 | 445 | 3 | yes |
| `GENERIC_VALUES` | 11,233 | 11,232 | 57 | yes |

## Live gold recall — does the real universe recover the frozen gold?

A6b measured recall by matching compiled terms against stored titles. This measures whether OpenAlex's stemmed index, its coverage and its title normalisation reproduce that in practice. **A gap is a finding about the index, not about the query.**

| gold channel | n | live recall | A6b CV recall |
|---|---|---|---|
| A-only | 19 | 78.9% | 89.5% (partly fitted) |
| **B-only** | 381 | **80.8%** | **92.1%** |
| both channels | 12 | 91.7% | 100% |

### Gold the live pull did not return

- Secularization and low fertility: How declining church membership changes couples’ childbearing
- Religiously inspired baby boom: evidence from Georgia
- Modes of production secularization and the pace of the fertility decline in Western Europe 1870-1930.
- URBANIZATION, SECULARIZATION, AND BIRTH SPACING: A CASE STUDY OF AN HISTORICAL FERTILITY TRANSITION
- Changing Attitudes toward Marriage and Children in Six Countries
- Secularism and Fertility Worldwide
- B Arpino G Esping-Andersen L Pessin The diffusion of gender egalitarian values and fertility. The Fertility Ga
- Attitudes toward fertility and childbearing among childless female teachers working in the Gorgan education sy
- Navigating fertility, reproduction and modern contraception in the fragile context of South Kivu, Democratic R
- Gender and fertility within the free churches in the Sundsvall region, Sweden, 1860–1921
- Tacit consent: the Church and birth control in northern Italy.
- Religiosity, nuptiality and reproduction in Canada
- Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related b
- The factors of formation of a procreative attitude in the context of demographic transition
- Attitudes that Differentiate Alternative Family Sizes
- Recent fertility decline in Eritrea
- TELEVISION, VALUE CONSTRUCTS, AND REPRODUCTIVE BEHAVIOR IN BRAZILIAN “EXCLUDED” COMMUNITIES
- Religiosität und Fertilität: eine empirische Untersuchung des Einflusses von Religiosität auf Elternschaft und
- Low Fertility in Japan, South Korea, and Singapore
- What Has Religion Got to Do With It?*
- Fertility by ethnic and religious groups in the UK, trends in a trans-national context
- Religion and Fertility in the United States : A Geographic Analysis
- Change in Nuptiality Patterns among Cuban Americans: Evidence of Cultural and Structural Assimilation? 1
- Cultural policy regimes and arts councils. The longue durée perspective, birth of the state, religious traject
- Fertility in Western Europe: the role of religion
- Laamanen VM (2024) Changes in work and family attitudes over birth cohorts and links to childfree ideals in Fi
- Applicability of the second demographic transition in Asia
- The Two-Child Policy and Fertility
- Observations of Chinese Culture of Marriage and Childbearing in the Context of Low Fertility
- Religion and Religiosity

