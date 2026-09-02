# WDI age structure and fertility — provenance

Pulled 2026-09-02T16:32:58+00:00 by `source/build/306_c6a_cohort_size_series.py` for TICK-078 (C.6.a).

Source: World Bank World Development Indicators API, `api.worldbank.org/v2`, 1960–2024, 18 countries: USA, GBR, FRA, DEU, ITA, ESP, JPN, SWE, NLD, CAN, AUS, DNK, NOR, FIN, BEL, AUT, CHE, KOR.

One file per indicator, unmodified API responses. Age-band indicators (`SP.POP.<band>.<sex>.5Y`) are percentages **of that sex's population**, so they must be weighted by `SP.POP.TOTL.<sex>.IN` before the sexes are summed.

WDI age structure derives from UN WPP; it is an interpolation, not a register count.

This directory was empty before this pull, despite `CLAUDE.md` describing it as holding the macro panels. Later chapters needing age structure or TFR should read from here rather than re-pulling. Re-pull with `--refresh`.
