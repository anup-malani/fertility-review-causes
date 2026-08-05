# D.1.a — production query and recall probe (GACS A6c)

Refit on the full gold at the A6b breadth **(outcome 20, treatment 10)**. Structure: **(OUTCOME) AND (any of six treatment clusters)**. 67 outcome terms, 123 treatment terms across six clusters.

## 1. Local recall, reported in halves

| gold subset | n | title only | title + abstract |
|---|---|---|---|
| all gold | 412 | 91.7% | 93.9% |
| has an abstract | 177 | 94.4% | 99.4% |
| **no abstract** | 235 | 89.8% | 89.8% |

**The single title-and-abstract figure is not usable on this chapter and is shown only for comparability with B.1 and D.3.b.** Abstract coverage is 50% and is not missing at random: providers hold abstracts for well-indexed Anglo-European journals and not for the book chapters, regional journals and dissertations that make up this frame's unresolvable residue. Quoting the pooled number would measure the covered half and attribute its behaviour to the whole. **The `no abstract` row is what the operationalisation can actually promise on the records the search will have the hardest time with.**

## 2. Live universe counts

| cluster | Semantic Scholar (bulk, full boolean) |
|---|---|
| `S1_POSTMATERIALISM` | 7,722 |
| `S2_INDIVIDUALISM` | 32,846 |
| `S3_SECULARIZATION` | 57,144 |
| `S4_CHILDLESSNESS_NORM` | 41,291 |
| `S5_CONSUMERISM` | 15,636 |
| `GENERIC_VALUES` | 343,368 |
| **sum of clusters (upper bound, overlap unmeasured)** | **498,007** |

The single-request union returns `None`: the encoded query is 5309 bytes and Semantic Scholar's bulk endpoint is a GET with a 4,094-byte request-line ceiling. **The query cannot be sent whole to either provider** — but S2 decomposes by CLUSTER (six requests) where OpenAlex decomposes by TERM, which is the comparison that decides C1.

### OpenAlex, and these are NOT universe counts

Each row is `title.search:fertility` conjoined with the cluster's **lead term as the query writes it** — that is, as a stem. They are reproduced here because the numbers demonstrate the portability failure below, not because they measure anything about the literature.

| cluster | lead term (stem) | OpenAlex count |
|---|---|---|
| `S1_POSTMATERIALISM` | `postmaterialis` | 0 |
| `S2_INDIVIDUALISM` | `individualism` | 3 |
| `S3_SECULARIZATION` | `religio` | 1 |
| `S4_CHILDLESSNESS_NORM` | `voluntary childless` | 4 |
| `S5_CONSUMERISM` | `consumerism` | 38 |
| `GENERIC_VALUES` | `values` | 607 |

## The finding that decides C1: the query's wildcards are not portable, and both providers fail silently

Measured this run, not assumed. Both failures return a plausible non-zero count rather than an error, which is this chapter's signature failure mode for the fourth time.

| term as written | OpenAlex `title.search` | Semantic Scholar bulk |
|---|---|---|
| `fertility` | 114,008 | 373,817 |
| `fertilit` (stem, no operator) | **63** | 137 |
| `fertilit*` (unquoted prefix) | *not supported* | **385,352** |
| `"fertilit"*` (quoted stem) | — | **137** |
| `religiosity` | 16,941 | 45,753 |
| `religio` (stem) | **2,041** | — |

**OpenAlex has no prefix matching at all.** `fertilit` returns 63 records against 114,008 for `fertility`. Every stem in this query — `fertilit*`, `childless*`, `religio*`, `childbear*`, `procreat*` — would retrieve a small biased fraction and report a plausible count while doing it. Running C1 there requires enumerating every stem into explicit surface forms first.

**Semantic Scholar does support prefix matching, and this script's first encoder got the syntax wrong in the same silent direction.** It emitted a QUOTED stem, which S2 reads as an exact phrase with a meaningless trailing star: 137 records. Unquoted `fertilit*` returns 385,352, correctly more than the bare word. A pull built on the quoted form would have been wrong by three orders of magnitude and would not have announced it.

**Neither provider supports a phrase prefix**, so the wildcard is dropped from **26** multi-word terms, which are narrower than intended as a result. These are concentrated in S4 and S5, whose backbones are almost entirely multi-word phrases — so the two clusters A6b already flagged as earning almost no credit are also the two most degraded by this limit.

## 3. Which provider can run this query — CORRECTED

**This section reverses the conclusion this script was drafted to reach, and the reversal came from an error message.** The draft recommended Semantic Scholar bulk search on the grounds that OpenAlex needed one metered request per term. Feeding OpenAlex the full cluster query returned: *"Wildcards (* or ?) require the exact (no-stem) field. `title.search` is stemmed."* — which says the field does at index time what the query was using wildcards to do at search time.

Three consequences, each measured:

1. **No wildcard expansion is needed on OpenAlex.** `childless` and `childlessness` both return 2,586 — the same postings list. The earlier reading that OpenAlex "has no prefix matching", inferred from `fertilit` returning 63 against 114,008 for `fertility`, was measuring the wrong thing: `fertilit` is not a word and stems to nothing.
2. **The whole cluster query fits in one request** — two comma-joined filters, 67 OR'd outcome terms against the cluster's terms, accepted without complaint. The 123-narrow-query cost model does not apply.
3. **And the decisive one: the Semantic Scholar counts are title-AND-ABSTRACT and are not comparable to the CV.** A6b selected this query on TITLE-ONLY recall. S2's bulk endpoint cannot restrict to titles, so its numbers describe a different operationalisation than the one that was validated. Running C1 there would not be the query the CV measured.

| cluster | OpenAlex, title-only (faithful to CV) | Semantic Scholar, title+abstract |
|---|---|---|
| `S1_POSTMATERIALISM` | **330** | 7,722 (23x) |
| `S2_INDIVIDUALISM` | **841** | 32,846 (39x) |
| `S3_SECULARIZATION` | **3,058** | 57,144 (19x) |
| `S4_CHILDLESSNESS_NORM` | **2,221** | 41,291 (19x) |
| `S5_CONSUMERISM` | **445** | 15,636 (35x) |
| `GENERIC_VALUES` | **11,228** | 343,368 (31x) |
| **sum (upper bound, overlap unmeasured)** | **18,123** | 498,007 |

The gap is 19x to 39x per cluster. **This is the same trap the OAS chapter documented** in `43_live_search.py`: "title_and_abstract.search on the same terms returns 251,950 because bare mined singles ... precise as title tokens ... explode across abstracts; title.search returns ~11.7k." Terms selected for title precision are not title-and-abstract terms, and a universe count taken on the wrong field overstates the pull by more than an order of magnitude.

**Corrected recommendation: run C1 on OpenAlex `title.search`**, one request per cluster, cursor-paginated, against a title-only universe of **18,123** records before dedup. That is affordable under the metered tier at roughly one request per 200 records, it is the operationalisation the CV validated, and it needs no wildcard expansion. Semantic Scholar remains the right provider for citation work (the snowball) and for records OpenAlex does not index, where its abstract-inclusive matching is a feature rather than a confound.

**What was nearly shipped.** Had the S2 recommendation stood, C1 would have pulled against a 498,007-record title-and-abstract universe, retrieved a differently-defined corpus than the one the CV measured, and reported a recall figure that no longer described the query in use. The error was caught by a provider's error message, not by the metric.

## Gold the compiled query misses even with abstracts

- Postmaterialismus und generatives Verhalten
- Changing Attitudes toward Marriage and Children in Six Countries
- Gender and fertility within the free churches in the Sundsvall region, Sweden, 1860–1921
- Attitudes that Differentiate Alternative Family Sizes
- Recent fertility decline in Eritrea
- Is There a Stronger Association Between Children and Happiness Among the Religious? Religion as a Moderator in
- Low Fertility in Japan, South Korea, and Singapore
- What Has Religion Got to Do With It?*
- Cultural policy regimes and arts councils. The longue durée perspective, birth of the state, religious traject
- Rituals of Birth and Efforts to Preserving Cultural Identity in Cisaar Hamlet, Majalengka, Amidst the Tide of 
- Applicability of the second demographic transition in Asia
- The Two-Child Policy and Fertility
- Religion and Religiosity
- Institutional identity, fertility choice and comprehensive two-child policy optimization-evidence from China
- When Formal Laws and Informal Norms Collide: Lineage Networks versus Birth Control Policy in China1
- Overview Chapter 6: The diverse faces of the second demographic transition in Europe.
- Marriage and Fertility Behaviour in Japan
- Kinship and fertility: Brother and sibling effects on births in a patrilineal system
- Between identity and assimilation: Jewish fertility in nineteenth-century Venice
- Suwal, J. V. (2001). Socio-cultural dynamics of first birth intervals in Nepal. Contribution to Nepalese Studi
- Gegen den Strom der Zeit? Vom Einfluss der religiösen Zugehörigkeit und Religiosität auf die Geburt von Kinder
- Female Labour Market Participation and Cultural Variables
- Religion, spirituality and the social sciences
- Religious Participation, Religious Affiliation, and Engagement With Children Among Fathers Experiencing the Bi
- Polygyny and reproductive behavior in sub-saharan Africa: A contextual analysis

