# D.1.a — what would the full screen add? A 400-record estimate

**10 batches, 400 records, drawn from 15,586.** The sample is uniform random by construction: `109_` shuffles the production records with seed 621 *before* cutting batches, and the shuffle is blind to content, so batches 1–10 are a random 400 rather than the first 400 of anything.

Intervals are Wilson 95%. At these proportions the normal approximation misbehaves and can put a lower bound below zero.

## The number that decides whether to run the full screen

| | sample | rate | 95% CI | projected to 15,586 |
|---|---|---|---|---|
| **RELEVANT** | 20/400 | **5.00%** | 3.26–7.60% | **779** (508–1,184) |
| in a **primary (poolable) cell** | 26/400 | 6.50% | 4.47–9.35% | **1,013** (697–1,458) |
| UNCERTAIN → full-text read | 49/400 | 12.25% | 9.39–15.83% | **1,909** (1,464–2,467) |
| NOT_RELEVANT | 331/400 | 82.8% | | |

**The UNCERTAIN row is a cost forecast, not a failure rate.** The rubric routes a record there whenever the deciding fact is invisible at title/abstract, and it is the instruction rather than a shortfall. Each one is a full-text read to be budgeted.

Title-only records in the sample: **127/400** (32%), of which 32 were routed UNCERTAIN as the rubric requires.

## Where the kept records land

| estimand cell | n |
|---|---|
| `OFF_OTHER` | 251 |
| `INSUFFICIENT_INFO` | 35 |
| `OFF_OUTCOME` | 25 |
| `PRIMARY_SECULAR_S3` | 19 |
| `OFF_CONTRACEPTIVE_ATTITUDE_A3_A6` | 16 |
| `VALUE_CONSTRUCT` | 11 |
| `SDT_FRAMEWORK_THEORY` | 11 |
| `NORM_ACCEPTABILITY_DESCRIPTIVE` | 9 |
| `OFF_GENDER_D2a` | 6 |
| `OFF_INCOME_SECURITY` | 5 |
| `NORM_ENVIRONMENT_LEVEL` | 3 |
| `OFF_PARTNERSHIP_D2b` | 2 |
| `PRIMARY_POSTMATERIAL_S1` | 2 |
| `REVERSE` | 1 |
| `PRIMARY_INDIVIDUALISM_S2` | 1 |
| `AGGREGATE_COMOVEMENT` | 1 |
| `PRIMARY_CONSUMERISM_S5` | 1 |
| `OFF_PARENTING_D2d` | 1 |

### Pair, among records not rejected

| pair | n |
|---|---|
| NA | 28 |
| S3 | 25 |
| S4 | 6 |
| S1 | 5 |
| MULTIPLE | 2 |
| S2 | 2 |
| S5 | 1 |

### Design tier guessed for RELEVANT records

The rubric's calibration expectation is that Tier 1 is rare — three studies in the whole frame — so a sample returning many Tier-1 guesses means the screen has mistaken observational work for identified work.

| tier | n |
|---|---|
| 3 | 16 |
| 4 | 4 |

### Retrieval cluster of kept records

Recovered post hoc through `idmap.json`; no stratified sampling was needed.

| cluster | n |
|---|---|
| `GENERIC_VALUES` | 42 |
| `S3_SECULARIZATION` | 20 |
| `S4_CHILDLESSNESS_NORM` | 10 |
| `S1_POSTMATERIALISM` | 5 |
| `S2_INDIVIDUALISM` | 2 |
