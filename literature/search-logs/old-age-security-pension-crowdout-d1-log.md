# D1 deterministic ranking + cutoff — old-age-security-pension-crowdout

- corpus: 11,463 records
- candidates (both blocks present in title or abstract): 8,857
- **LLM pool after cutoff: 1,100** (cutoff ~1100, plus bypass for gold + title-both)
  - gold members (bypass): 118
  - title-both (bypass): 1100
  - with abstract: 995 (90%)

Next: Haiku recall filter over this pool -> Sonnet precision + estimand extraction -> estimand gate -> tiers.
