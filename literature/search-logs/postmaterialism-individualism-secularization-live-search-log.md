# D.1.a — live production pull (GACS C1)

OpenAlex `title.search`, **title-only**, one cursor-paginated stream per cluster, union across clusters. Title-only because that is the operationalisation A6b's cross-validation selected; abstracts enter at the screen, not the search.

- union corpus: **11,425** distinct records
- sum of per-cluster counts: 18,123 (upper bound — clusters overlap by design)
- overlap collapsed by dedup: **6,698**
- incomplete clusters: **['GENERIC_VALUES']**
- budget exhaustion: **GENERIC_VALUES: {"cluster": "GENERIC_VALUES", "pages_done": 25, "records_kept": 5000, "universe": 11228}**

| cluster | universe | pulled | pages | complete |
|---|---|---|---|---|
| `S1_POSTMATERIALISM` | 330 | 330 | 2 | yes |
| `S2_INDIVIDUALISM` | 841 | 841 | 5 | yes |
| `S3_SECULARIZATION` | 3,058 | 3,058 | 16 | yes |
| `S4_CHILDLESSNESS_NORM` | 2,221 | 2,221 | 12 | yes |
| `S5_CONSUMERISM` | 445 | 445 | 3 | yes |
| `GENERIC_VALUES` | 11,228 | 5,000 | 25 | **NO** |

> ## ⚠ THE PULL IS INCOMPLETE — THE RECALL FIGURES BELOW ARE NOT RESULTS

> `GENERIC_VALUES` stopped on OpenAlex budget exhaustion, and the budget resets in roughly 23 hours (`retryAfter` 82,182s). **`GENERIC_VALUES` is the cluster A6b found carries the most sole credit — 176 gold papers no other cluster reaches — so a partial pull of it depresses gold recall far more than its share of records suggests.** Re-run to resume; cached pages cost nothing. Do not quote these percentages until every cluster reads `complete: yes`.


## Live gold recall — does the real universe recover the frozen gold?

A6b measured recall by matching compiled terms against stored titles. This measures whether OpenAlex's stemmed index, its coverage and its title normalisation reproduce that in practice. **A gap is a finding about the index, not about the query.**

| gold channel | n | live recall | A6b CV recall |
|---|---|---|---|
| A-only | 19 | 73.7% | 89.5% (partly fitted) |
| **B-only** | 381 | **74.0%** | **92.1%** |
| both channels | 12 | 91.7% | 100% |

### Gold the live pull did not return

- Secularization and low fertility: How declining church membership changes couples’ childbearing
- Religiously inspired baby boom: evidence from Georgia
- Modes of production secularization and the pace of the fertility decline in Western Europe 1870-1930.
- URBANIZATION, SECULARIZATION, AND BIRTH SPACING: A CASE STUDY OF AN HISTORICAL FERTILITY TRANSITION
- Self-Fulfilment and Fertility Intentions: The Interplay of Cultural Values and Expected Welfare State Support
- Changing Attitudes toward Marriage and Children in Six Countries
- Sex, digital media, and fertility intentions in China: A chain mediation analysis of media use and gender role
- Tradition and transition: social media evidence on fertility attitudes and gender differences in China
- Secularism and Fertility Worldwide
- B Arpino G Esping-Andersen L Pessin The diffusion of gender egalitarian values and fertility. The Fertility Ga
- The social and cultural determinants of the fertility rate among Congolese refugee women living in the inner c
- Attitudes toward fertility and childbearing among childless female teachers working in the Gorgan education sy
- Navigating fertility, reproduction and modern contraception in the fragile context of South Kivu, Democratic R
- Gender and fertility within the free churches in the Sundsvall region, Sweden, 1860–1921
- The Contraceptive Revolution and the Second Demographic Transition: An Economic Model of Sex, Fertility, and M
- Tacit consent: the Church and birth control in northern Italy.
- Religiosity, nuptiality and reproduction in Canada
- The Influence of Popular Beliefs about Childbirth on Fertility Patterns in Mid-Twentieth-Century Netherlands
- Fertility norms in a dynamic and cross-national perspective
- Politics, Culture and Fertility Trends.
- Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related b
- The fertility gap in Taiwan: housework division, gender role attitudes, and their gender-specific associations
- Continuing the Family Lineage? Primary Family Members’ Traditional Fertility Values and Fertility in Rural Chi
- The factors of formation of a procreative attitude in the context of demographic transition
- Attitudes that Differentiate Alternative Family Sizes
- Recent fertility decline in Eritrea
- TELEVISION, VALUE CONSTRUCTS, AND REPRODUCTIVE BEHAVIOR IN BRAZILIAN “EXCLUDED” COMMUNITIES
- Capital in Pronatalist Fields: Exploring the Influence of Economic, Social, Cultural and Symbolic Capital on C
- Beyond Belief: How Membership in Congregations Affects the Fertility of U.S. Mormons and Jews
- Religiosität und Fertilität: eine empirische Untersuchung des Einflusses von Religiosität auf Elternschaft und

