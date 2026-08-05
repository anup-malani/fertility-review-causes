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

## 3. Which provider can run this query

**This is a live question for the first time on this project.** Every previous chapter ran C1 on OpenAlex. Three findings from this chapter make that unsafe here — the free tier is metered and did not cover a sixteen-row canon resolution (`95_`), boolean searches above five operators are throttled (channel-1 probe), and `title.search` has no prefix matching at all (measured above).

| | OpenAlex | Semantic Scholar bulk |
|---|---|---|
| accepts the full conjunction in one request | **no** (operator ceiling) | **no** (4,094-byte request line) |
| decomposition unit | **per term** | **per cluster** |
| requests for the full query | **123** | **6** |
| supports prefix wildcards | **no** | yes (unquoted `stem*`) |
| cost, first page only | **$0.123** | $0 |
| binding constraint | daily budget | unauthenticated throttling |

**Neither provider takes the query whole**, which is not what this script was drafted expecting — the recommendation was going to be "send it to S2 in one request" until the attempt returned HTTP 400. The decision therefore turns on the DECOMPOSITION UNIT, and there the gap is wide: OpenAlex needs one metered request per term (**123**, and that is a floor counting one page each), while S2 needs one free request per cluster (**6**).

**Recommendation: run C1 on Semantic Scholar bulk search**, decomposed by cluster and unioned client-side, with OpenAlex kept for targeted count checks where its metering is affordable. Two conditions attach. First, **the Semantic Scholar API key requested since the D.3.b snowball is now on the critical path**, not a convenience: unauthenticated throttling is the only thing standing between this plan and a completed pull. Second, **whichever provider is used, the compiled query must be emitted with wildcards already expanded** — the artifact this script writes still carries stems, and a consumer that passes them through unexamined reproduces the silent failure measured above.

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

