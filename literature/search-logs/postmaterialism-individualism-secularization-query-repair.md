# D.1.a — production query repair (v1 → v2)

`105_` established that 24 of v1's 45 wildcard terms retrieve almost nothing once the star is stripped, and that `secular` and `religio` return healthy counts while failing to match the inflections they were written for. Two of the chapter's three Tier-1 natural experiments are absent from the C1 corpus as a result. A6c already specified this fix and it was not enforced.

**The expansions are harvested, not invented.** Candidates come from the **gold titles** (Tier A + Tier B, query-independent, and therefore containing the vocabulary of the papers the query missed), the live corpus titles, and rule-based English suffixes. Every candidate is then verified against a live count, and the assembled query is verified conjunctively against the DOIs of the papers v1 missed.

- wildcard terms expanded: **45**
- live-verified variants added: **130**
- plain (non-wildcard) terms dropped as dead: **2**
- outcome terms: 67 → **82**

| cluster | v1 terms | v2 terms |
|---|---|---|
| `S1_POSTMATERIALISM` | 20 | **30** |
| `S2_INDIVIDUALISM` | 16 | **23** |
| `S3_SECULARIZATION` | 29 | **44** |
| `S4_CHILDLESSNESS_NORM` | 12 | **15** |
| `S5_CONSUMERISM` | 16 | **27** |
| `GENERIC_VALUES` | 20 | **23** |

## Acceptance gate — does v2 retrieve what v1 missed?

The production filter itself with a DOI pinned to it: `filter=doi:<doi>,title.search:<outcome>,title.search:<cluster>`. This is the only test that answers the question; a count per term does not.

| paper | retrieved by | verdict |
|---|---|---|
| Secularization and low fertility | `S3_SECULARIZATION` | **PASS** |
| Religiously inspired baby boom: Georgia | `S3_SECULARIZATION` | **PASS** |
| Political Islam, Marriage and Fertility (control, was retrieved) | `S3_SECULARIZATION` | **PASS** |

## Per-term repair

`dropped` variants retrieved fewer than 5 records and would only lengthen the filter.

- **DEAD PLAIN TERM** `S2_INDIVIDUALISM` / `kinship tightness` — count 2, removed
- **DEAD PLAIN TERM** `S3_SECULARIZATION` / `canonical secularization` — count 0, removed

- `OUTCOME` / `childbear*` → `childbearing` (9,641), `childbearing-age` (3,978)
- `OUTCOME` / `childless*` → `childlessness` (2,586), `childless` (2,586)
- `OUTCOME` / `fertilit*` → `fertility` (114,038), `fertilite` (363), `fertilitat` (39), `fertilit` (63)
- `OUTCOME` / `fertility intention*` → `fertility intentions` (950), `fertility intention` (331)
- `OUTCOME` / `fertility preference*` → `fertility preferences` (780), `fertility preference` (780), `fertility preference-based` (25), `fertility preference-aligned` (7)
- `OUTCOME` / `generative* verhalten` → `generatives verhalten` (32), `generative verhalten` (32)
- `OUTCOME` / `nuptialit*` → `nuptiality` (1,759), `nuptialites` (28)
- `OUTCOME` / `procreat*` → `procreative` (2,452), `procreation` (2,452), `procreate` (2,452)
- `OUTCOME` / `reproductive decision*` → `reproductive decisions` (1,891), `reproductive decision` (1,891), `reproductive decisional` (1,891), `reproductive decision-making` (678), `reproductive decision-aid` (23)
- `OUTCOME` / `reproductive intention*` → `reproductive intentions` (204), `reproductive intention` (124), `reproductive intentionally` (14), `reproductive intentional` (14)
- `OUTCOME` / `want* children` → `want children` (856), `wanted children` (856), `wants children` (77), `wanting children` (45)
- `S1_POSTMATERIALISM` / `emancipative value*` → `emancipative value` (61), `emancipative values` (61), `emancipative valued` (61)
- `S1_POSTMATERIALISM` / `post-materialis*` → `post-materialis` (25), `post-materialises` (14)
- `S1_POSTMATERIALISM` / `postmaterial value*` → `postmaterial value` (47), `postmaterial values` (47), `postmaterial valued` (47)
- `S1_POSTMATERIALISM` / `postmaterialis*` → `postmaterialism` (234), `postmaterialismus` (29)
- `S1_POSTMATERIALISM` / `self-expression value*` → `self-expression value` (66), `self-expression values` (66), `self-expression valued` (66)
- `S1_POSTMATERIALISM` / `survival value*` → `survival value` (2,876), `survival values` (2,876), `survival valued` (2,876), `survival value-based` (136), `survival value-added` (52)
- `S1_POSTMATERIALISM` / `value orientation*` → `value orientation` (8,053), `value orientations` (8,053)
- `S2_INDIVIDUALISM` / `extended famil*` → `extended family` (3,210), `extended families` (3,210), `extended familial` (101), `extended familiales` (101), `extended familialism` (101), `extended familiarity` (13), `extended family-size` (10), `extended family-owned` (9)
- `S2_INDIVIDUALISM` / `individualist*` → `individualist` (945), `individualistes` (173)
- `S3_SECULARIZATION` / `denomination*` → `denomination` (2,455), `denominations` (2,455), `denominational` (1,478)
- `S3_SECULARIZATION` / `evangelic*` → `evangelical` (15,951), `evangelic` (71)
- `S3_SECULARIZATION` / `islam*` → `islamic` (407,036), `islam` (407,036), `islamism` (407,036), `islamization` (407,036), `islamist` (4,459), `islamies` (182)
- `S3_SECULARIZATION` / `religio*` → `religion` (255,119), `religions` (255,119), `religious` (213,875), `religiousness` (213,875), `religiosity` (16,945), `religio` (2,041), `religiously` (1,526), `religiosen` (149)
- `S3_SECULARIZATION` / `secular*` → `secular` (34,326), `secularity` (34,326), `secularism` (6,193), `secularization` (4,657), `secularist` (378)
- `S3_SECULARIZATION` / `secularis*` → `secularism` (6,193), `secularist` (378), `secularises` (999), `secularis` (26)
- `S4_CHILDLESSNESS_NORM` / `acceptability of childless*` → **nothing survived**
- `S4_CHILDLESSNESS_NORM` / `approval of childless*` → **nothing survived**
- `S4_CHILDLESSNESS_NORM` / `attitudes toward childless*` → `attitudes toward childlessness` (26), `attitudes toward childless` (26)
- `S4_CHILDLESSNESS_NORM` / `attitudes towards childless*` → `attitudes towards childlessness` (18), `attitudes towards childless` (18)
- `S4_CHILDLESSNESS_NORM` / `childfree identit*` → `childfree identity` (21), `childfree identities` (21)
- `S4_CHILDLESSNESS_NORM` / `intentional childless*` → `intentional childlessness` (13), `intentional childless` (13)
- `S4_CHILDLESSNESS_NORM` / `norm* about childless*` → **nothing survived**
- `S4_CHILDLESSNESS_NORM` / `stigma of childless*` → `stigma of childlessness` (34), `stigma of childless` (34)
- `S4_CHILDLESSNESS_NORM` / `voluntary childless*` → `voluntary childlessness` (295), `voluntary childless` (295)
- `S5_CONSUMERISM` / `acquisitive*` → `acquisitive` (805)
- `S5_CONSUMERISM` / `consumption aspiration*` → `consumption aspirations` (90), `consumption aspiration` (90)
- `S5_CONSUMERISM` / `lifestyle aspiration*` → `lifestyle aspirations` (64), `lifestyle aspiration` (64)
- `S5_CONSUMERISM` / `material value*` → `material value` (6,478), `material values` (6,478), `material valued` (6,478), `material value-added` (626), `material value-based` (620)
- `S5_CONSUMERISM` / `materialistic value*` → `materialistic value` (339), `materialistic values` (339), `materialistic valued` (339)
- `S5_CONSUMERISM` / `possession*` → `possession` (15,980), `possessions` (15,980), `possession-based` (241)
- `S5_CONSUMERISM` / `status good*` → `status good` (946), `status goods` (305), `status goodness` (8)
- `GENERIC_VALUES` / `belief*` → `beliefs` (163,415), `belief` (163,415), `belief-desire` (567)
- `GENERIC_VALUES` / `gender attitude*` → `gender attitudes` (8,559), `gender attitude` (8,559)
- `GENERIC_VALUES` / `gender role attitude*` → `gender role attitudes` (2,044), `gender role attitude` (2,044)
