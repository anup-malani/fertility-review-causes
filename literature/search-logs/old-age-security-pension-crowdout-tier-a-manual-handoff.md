# Tier-A manual handoff — old-age-security gold set

Verified automatically: **14/35**. Residual below: **21** studies the agent fleet + deterministic verifier could not pin to a trustworthy DOI.

Categories: **A** likely-not-real corrupted records (consider dropping, not resolving); **B** rate-limited (a retry pass after OpenAlex cooldown will likely auto-resolve); **C** working-paper-only (accept the WP DOI or title-key the gold item); **D** real but needs a human lookup (generic title; author name disambiguates).

## Category LIKELY-NOT-REAL (drop candidate)  (4)

| id | year | title | verifier reason / agent note | unverified candidate DOIs |
|---|---|---|---|---|
| 15 | 2021 | Does Pension Privatization Increase Fertility? Evidence from | Could not locate or verify any real paper with this exact title. Needs manual attention (possibly an unindexed/obscure w | 10.1007/s13524-021-00979-w, 10.1596/1813-9450-7482 |
| 16 | 2021 | The Old-Age Security Motive for Fertility: Evidence from the | WARNING: this appears to be a corrupted/chimeric variant of the only verifiable paper in this title family, ID 18 'The O | 10.1257/app.20190078 |
| 19 | 2022 | The Old-Age Security Motive for Fertility: Evidence from the | WARNING: appears to be a corrupted/chimeric variant of ID 18 (Rossi & Godard Namibia paper). Did NOT assign that DOI her | 10.1257/app.20210035 |
| 20 | 2022 | Social Security as a Commitment Mechanism: Theory and Eviden | Could not locate or verify any real paper with this exact title. Needs manual attention (possibly an unindexed working p | 10.1007/s11150-022-09622-6 |

## Category RATE-LIMITED (retry likely resolves)  (1)

| id | year | title | verifier reason / agent note | unverified candidate DOIs |
|---|---|---|---|---|
| 31 | 2025 | The effect of social insurance on savings and fertility: evi | Could not locate a real DOI via Crossref, web search, OpenAlex (budget exhausted) or Semantic Scholar (rate-limited). Un | 10.1111/1468-0297.12904 |

## Category WORKING-PAPER (accept WP DOI or title-key)  (7)

| id | year | title | verifier reason / agent note | unverified candidate DOIs |
|---|---|---|---|---|
| 0 | None | Old-Age Security Hypothesis and Fertility Decisions: Evidenc | Exact title 'Old-Age Security Hypothesis and Fertility Decisions: Evidence from a Social Pension Reform' not located in  | — |
| 10 | 2019 | Pensions and Fertility in Austria | Candidate DOI 10.1007/s00148-019-00750-x is INVALID (doi.org returns 404; not in Crossref). Could not locate a verifiabl | 10.1007/s00148-019-00750-x |
| 21 | 2022 | The impact of social security on fertility: Quasi-experiment | Candidate DOI fabricated/invalid. Could not locate any published or working-paper version of 'The impact of social secur | 10.1016/j.euroecorev.2022.104153 |
| 28 | 2024 | Pension Policy Reform and Fertility: Micro Evidence from Gha | Working-paper-only; no published version-of-record DOI located. Authors confirmed via conference program and ECO-SOS WP  | — |
| 30 | 2025 | Pension Reforms and Fertility: Evidence from a Natural Exper | Distinct from the classic Billari-Galasso 'What Explains Fertility?' (id 17). Unverified candidate ssrn.5026726 left UNU | 10.2139/ssrn.5026726 |
| 32 | 2025 | Social Security and Fertility: Evidence from a Pension Refor | Per instructions, this generic China title is high-risk for false matches; left found=false because the candidate does n | 10.2139/ssrn.5244394 |
| 33 | 2025 | The Impact of Social Security on Fertility: A Quasi-Experime | Do NOT confuse with Shen/Zheng/Yang 2020 'The fertility effects of public pension' (PLOS One). Unverified candidate left | 10.2139/ssrn.5397327 |

## Category NEEDS HUMAN LOOKUP (generic title / author needed)  (9)

| id | year | title | verifier reason / agent note | unverified candidate DOIs |
|---|---|---|---|---|
| 1 | None | Pensions and Fertility: Evidence from Germany | STRONG CANDIDATE FOR MANUAL REVIEW, not returned because title does not match: Fenge & Scheubel, 'Pensions and fertility | — |
| 3 | 2007 | An analysis of the relationship between old age pension and  | Exact title 'An analysis of the relationship between old age pension and fertility: Evidence from a New Pension in Turke | — |
| 4 | 2012 | Children as a Form of Retirement Saving: Evidence from a Pen | Exact title 'Children as a Form of Retirement Saving: Evidence from a Pension Reform in Chile' (year_hint 2012) not loca | 10.1093/restud/rds010 |
| 5 | 2014 | Do Public Transfers Crowd Out Private Support to the Elderly | Exact title 'Do Public Transfers Crowd Out Private Support to the Elderly? Evidence from a Randomized Experiment in Ecua | 10.3386/w20429 |
| 6 | 2015 | Old-age support and fertility in rural China: Does the new r | Exact title 'Old-age support and fertility in rural China: Does the new rural pension scheme matter?' (year_hint 2015) n | 10.1080/00324728.2015.1012141 |
| 11 | 2019 | Social Security and Fertility: Evidence from China | Candidate DOI 10.1111/1756-2171.12296 is WRONG (resolves to Neeman/Ory/Yu 'The benefit of collective reputation', RAND J | 10.1111/1756-2171.12296 |
| 22 | 2022 | The impact of pension reform on fertility: Evidence from Chi | Candidate DOI points to an unrelated paper. Title 'The impact of pension reform on fertility: Evidence from China' is ge | 10.1016/j.chieco.2022.101765 |
| 26 | 2023 | The Consequences of Raising the Retirement Age: Evidence fro | Candidate DOI points to an unrelated paper. Could not locate 'The Consequences of Raising the Retirement Age: Evidence f | 10.1016/j.red.2023.01.001 |
| 27 | 2024 | Effects of Pension Reform on Household Fertility and Saving  | Candidate DOI fabricated/invalid. Could not locate 'Effects of Pension Reform on Household Fertility and Saving Behavior | 10.1007/s11205-024-03315-0 |
