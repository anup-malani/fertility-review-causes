# D.1.a — live production pull (GACS C1)

OpenAlex `title.search`, **title-only**, one cursor-paginated stream per cluster, union across clusters. Title-only because that is the operationalisation A6b's cross-validation selected; abstracts enter at the screen, not the search.

- union corpus: **17,646** distinct records
- sum of per-cluster counts: 18,521 (upper bound — clusters overlap by design)
- overlap collapsed by dedup: **875**
- incomplete clusters: **none**
- budget exhaustion: **none**

| cluster | universe | pulled | pages | complete |
|---|---|---|---|---|
| `S1_POSTMATERIALISM` | 338 | 338 | 2 | yes |
| `S2_INDIVIDUALISM` | 910 | 910 | 5 | yes |
| `S3_SECULARIZATION` | 3,196 | 3,196 | 16 | yes |
| `S4_CHILDLESSNESS_NORM` | 2,219 | 2,219 | 12 | yes |
| `S5_CONSUMERISM` | 445 | 445 | 3 | yes |
| `GENERIC_VALUES` | 11,413 | 11,413 | 58 | yes |

## Live gold recall — does the real universe recover the frozen gold?

A6b measured recall by matching compiled terms against stored titles. This measures whether OpenAlex's stemmed index, its coverage and its title normalisation reproduce that in practice. **A gap is a finding about the index, not about the query.**

| gold channel | n | live recall | A6b CV recall |
|---|---|---|---|
| A-only | 19 | 94.7% | 89.5% (partly fitted) |
| **B-only** | 381 | **82.4%** | **92.1%** |
| both channels | 12 | 100.0% | 100% |

### Gold the live pull did not return

- Changing Attitudes toward Marriage and Children in Six Countries
- B Arpino G Esping-Andersen L Pessin The diffusion of gender egalitarian values and fertility. The Fertility Ga
- Attitudes toward fertility and childbearing among childless female teachers working in the Gorgan education sy
- Navigating fertility, reproduction and modern contraception in the fragile context of South Kivu, Democratic R
- Gender and fertility within the free churches in the Sundsvall region, Sweden, 1860–1921
- Tacit consent: the Church and birth control in northern Italy.
- Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related b
- Attitudes that Differentiate Alternative Family Sizes
- Recent fertility decline in Eritrea
- TELEVISION, VALUE CONSTRUCTS, AND REPRODUCTIVE BEHAVIOR IN BRAZILIAN “EXCLUDED” COMMUNITIES
- Religiosität und Fertilität: eine empirische Untersuchung des Einflusses von Religiosität auf Elternschaft und
- Low Fertility in Japan, South Korea, and Singapore
- What Has Religion Got to Do With It?*
- Fertility by ethnic and religious groups in the UK, trends in a trans-national context
- Religion and Fertility in the United States : A Geographic Analysis
- Cultural policy regimes and arts councils. The longue durée perspective, birth of the state, religious traject
- Fertility in Western Europe: the role of religion
- Laamanen VM (2024) Changes in work and family attitudes over birth cohorts and links to childfree ideals in Fi
- Applicability of the second demographic transition in Asia
- The Two-Child Policy and Fertility
- Observations of Chinese Culture of Marriage and Childbearing in the Context of Low Fertility
- Religion and Religiosity
- Lappegard, T., Neyer, G., & Vignoli, D. (2015). Three Dimensions of the Relationship between Gender Role Attit
- Écarts de fécondité en fonction du niveau d’instruction : le rôle de la religion en Grande-Bretagne et en Fran
- Peer effects of fertility intentions in the context of the second demographic transition: the impact of social
- Institutional identity, fertility choice and comprehensive two-child policy optimization-evidence from China
- Overview Chapter 6: The diverse faces of the second demographic transition in Europe.
- van de Kaa, D. J. (2001). Postmodern fertility preferences: From changing value orientation to new behavior. P
- Hackett Conrad. 2008. “Religion and Fertility in the United States.” PhD dissertation, Princeton University.
- Akintunde MO, Lawal MO, Simeon O. Religious roles in fertility behaviour among the residents of Akinyele local

