# D.1.a — does OpenAlex execute the query we validated?

A6b cross-validated the production query **offline**, matching compiled terms against stored titles, and reported Recall(B-only) **92.1%**. The live C1 pull returned **80.8%**. `103_d1a_live_search.py` anticipated a gap and called it *"a finding about the index rather than about the query"*. It is neither. **The validated query and the executed query are different queries.**

The frozen query carries wildcard stems. OpenAlex rejects a star outright, so the pull strips it and sends the bare stem. That is safe only when the stem is itself a word that stems to the same root as its inflections.

- wildcard terms in the frozen query: **45**
- **dead stems** (retrieve under 200 records): **24**

## Failure mode (a) — dead stems

| cluster | query term | sent as | live count |
|---|---|---|---|
| `OUTCOME` | `childbear*` | `childbear` | **0** |
| `OUTCOME` | `fertilit*` | `fertilit` | **63** |
| `OUTCOME` | `generative* verhalten` | `generative verhalten` | **32** |
| `OUTCOME` | `nuptialit*` | `nuptialit` | **0** |
| `OUTCOME` | `procreat*` | `procreat` | **0** |
| `OUTCOME` | `reproductive intention*` | `reproductive intention` | **124** |
| `S1_POSTMATERIALISM` | `emancipative value*` | `emancipative value` | **61** |
| `S1_POSTMATERIALISM` | `post-materialis*` | `post-materialis` | **25** |
| `S1_POSTMATERIALISM` | `postmaterial value*` | `postmaterial value` | **47** |
| `S1_POSTMATERIALISM` | `postmaterialis*` | `postmaterialis` | **0** |
| `S1_POSTMATERIALISM` | `self-expression value*` | `self-expression value` | **66** |
| `S2_INDIVIDUALISM` | `extended famil*` | `extended famil` | **5** |
| `S3_SECULARIZATION` | `evangelic*` | `evangelic` | **71** |
| `S3_SECULARIZATION` | `secularis*` | `secularis` | **26** |
| `S4_CHILDLESSNESS_NORM` | `acceptability of childless*` | `acceptability of childless` | **2** |
| `S4_CHILDLESSNESS_NORM` | `approval of childless*` | `approval of childless` | **0** |
| `S4_CHILDLESSNESS_NORM` | `attitudes toward childless*` | `attitudes toward childless` | **26** |
| `S4_CHILDLESSNESS_NORM` | `attitudes towards childless*` | `attitudes towards childless` | **18** |
| `S4_CHILDLESSNESS_NORM` | `childfree identit*` | `childfree identit` | **0** |
| `S4_CHILDLESSNESS_NORM` | `intentional childless*` | `intentional childless` | **13** |
| `S4_CHILDLESSNESS_NORM` | `norm* about childless*` | `norm about childless` | **0** |
| `S4_CHILDLESSNESS_NORM` | `stigma of childless*` | `stigma of childless` | **34** |
| `S5_CONSUMERISM` | `consumption aspiration*` | `consumption aspiration` | **90** |
| `S5_CONSUMERISM` | `lifestyle aspiration*` | `lifestyle aspiration` | **64** |

## Failure mode (b) — live but wrong, and invisible to a count

A healthy count does not mean the stem covers the inflection it was written for. **`secular` returns 34,326 records and does not match "Secularization"; `religio` returns 2,041 and does not match "Religiously".** A count-only audit passes both. Only a membership test against a known paper catches it.

Conjunctive test: `filter=doi:<doi>,title.search:<term>` — count 1 means the term retrieves that paper.

**Secularization and low fertility: how declining church membership changes childbearing**  
`10.1016/j.ssresearch.2026.103371`

| term | retrieves it? |
|---|---|
| `secular` | no |
| `secularization` | **yes** |
| `secularisation` | no |
| `church` | **yes** |
| `church attendance` | no |
| `fertility` | **yes** |
| `childbearing` | **yes** |
| `childbear` | no |

**Religiously inspired baby boom: evidence from Georgia**  
`10.1007/s00148-025-01092-5`

| term | retrieves it? |
|---|---|
| `religio` | no |
| `religious` | no |
| `religiously` | **yes** |
| `religiosity` | no |
| `baby boom` | **yes** |
| `fertility` | no |

**Political Islam, Marriage and Fertility (retrieved -- negative control)**  
`10.1086/696193`

| term | retrieves it? |
|---|---|
| `islam` | **yes** |
| `marriage` | **yes** |
| `fertility` | **yes** |

## What this costs the chapter

1. **Two of the three Tier-1 natural experiments are missing from the live corpus.** The entire Tier-1 stratum is three studies, so this is not a rounding error in a recall percentage — it is most of the chapter's only high-credibility evidence.
2. **`postmaterialis*` retrieves zero.** S1 is a named stratum of this hypothesis and its central term is dead.
3. **S4 is dead almost end to end** — 8 of its 9 wildcard terms. A6b recorded that S4 earns zero sole credit and asked whether it is 'buying coverage of a literature that does not exist'. **That question now has a different answer: the terms retrieve nothing because they are broken, not because the literature is absent.** A methods artifact was one step from being written into the chapter as a substantive claim about the field.

## This corrects the correction at `654a491`

That commit retracted A6c's *"no prefix matching"* reading on the evidence that `childless` and `childlessness` both return 2,586 — one postings list — and concluded no wildcard expansion was needed. **The generalisation was drawn from a single pair.** It holds for inflection (childless/childlessness) and fails for derivation (secular/secularization, religious/religiously), which is most of this query's vocabulary. Sixth instance of this chapter's signature failure, and the first inside the frozen artifact that everything downstream consumes.

## The repair

Expand every wildcard into its explicit morphological variants before the query is frozen, and **verify each expansion against a live count rather than assuming the index stems it**. The compiled query must not leave a star for a consumer to strip: A6c already recorded that requirement — *"the compiled query must be emitted with wildcards expanded before C1 consumes it"* — and it was not enforced.

