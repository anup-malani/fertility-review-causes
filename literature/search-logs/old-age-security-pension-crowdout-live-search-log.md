# Live OpenAlex production pull — old-age-security-pension-crowdout

- **universe (meta.count):** 11,738
- **pages pulled:** 59 (cap 300); budget-hit: False
- **records after dedup:** 11,463 (275 duplicates dropped)
- **with usable abstract:** 7,079 (62%)

## Live gold-recall check (does the real universe recover the frozen gold?)

- gold DOIs recovered in the pull: **101 / 162** (62%)
- gold titles recovered (normalized): **103 / 313** (33%)

> This is the universe-level recall (before D1/Haiku/Sonnet screening) — the ceiling the screen funnels down from. Gold not in the universe is a query-coverage miss (feeds query revision); gold in the universe but later dropped is a screening loss.

## Query

    (fertilit OR "birth rate" OR "fertility rate" OR "total fertility rate" OR "cohort fertility rate" OR "completed fertility" OR "lifetime fertility" OR "parity progression" OR childbear OR "number of children" OR fertility OR "endogenous fertility" OR children OR "child care" OR "fertility social" OR "value children" OR "child allowances" OR child OR "family fertility" OR "reform fertility" OR "fertility germany" OR "fertility related" OR "fertility theory" OR "growth fertility" OR "children old") AND (pension OR "social pension" OR "public pension" OR "old age pension" OR "old age assistance" OR "old age security" OR "old age support" OR "social security" OR "social insurance" OR "national insurance" OR "health insurance" OR "provident fund" OR superannuation OR annuities OR retirement OR retire OR "pension benefits" OR "non contributory" OR contributory OR "social grant" OR "social assistance" OR "income maintenance" OR "income support" OR "social safety net" OR "social transfer" OR "cash transfer" OR "conditional cash transfer" OR "unconditional cash transfer" OR "in kind transfer" OR security OR "old age" OR "age security" OR pensions OR intergenerational OR payg OR transfers OR "you pension" OR "payg pensions" OR "pensions endogenous" OR "intergenerational transfers" OR "security endogenous" OR "security hypothesis" OR "security family" OR "age pensions" OR savings OR "security rural" OR "pension system" OR "security saving" OR insurance OR "security reform" OR "public pensions" OR "payg pension" OR "pension systems" OR "pension generosity" OR "insurance family" OR "security population" OR "security old")

*Next: D1 deterministic rank + cutoff (44) → Haiku recall filter → Sonnet precision + estimand extraction → estimand gate + tiers.*
