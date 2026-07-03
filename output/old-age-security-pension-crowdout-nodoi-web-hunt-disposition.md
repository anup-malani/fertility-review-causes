# No-DOI Tier-B studies — web-hunt disposition

**What this is.** The 19 no-DOI, dead-WID studies in the meta-analysis set carried title-keyed metadata from the citation snowball, where ~40% of W-IDs have rotted/drifted. Four web-research agents searched each for the real paper, with a right-paper guard (topic must be old-age-security→fertility; setting/authors must match; no wrong-paper guessing).

**Bottom line.** Only **3 of 19** map to genuinely new retrievable papers. **8 of 19** are corrupted-title **duplicates of studies already in the set** (Shen ×6, Danzer & Zyska ×1, Rossi & Godard ×1). **8 of 19** are **phantom/unverifiable** — no findable real paper, or a real paper on the wrong topic (the snowball's WID-drift corruption mangled titles *and* settings: 'Austria' was Brazil, 'Rural China' was Namibia, 'Ecuador' was Mexico).

| category | n |
|---|--:|
| ✅ new, PDF fetched | 2 |
| 🟡 new, real but PDF unavailable | 1 |
| ♻️ duplicate of an included study | 8 |
| ⛔ phantom / unverifiable | 8 |

> **RA DECISION NEEDED.** The 8 duplicates are medium/low-confidence agent inferences that were NOT auto-merged. If you confirm them, the distinct-study count drops **60 → ~52**, and the same 16 dup+phantom entries should be pruned from Tier B (they inflate the recall denominator). Confidence is flagged per row; the settings are corrupted, so verify before merging.

| # | query title (corrupted) | disposition | conf | maps to / note |
|--:|---|---|:--:|---|
| 1 | Old-age support and fertility in rural China: Does the new | ♻️ duplicate of an included study | medium | `10.1371/journal.pone.0234657` · No exact-title paper found; reads as a garbled variant of the Shen/Zheng/Yang NRPS->fertil |
| 2 | Does Pension Privatization Increase Fertility? Evidence fr | ⛔ phantom / unverifiable | high | — · Extensive search found NO empirical Chile-1981 pension-privatization->fertility study; all |
| 3 | Children as a Form of Retirement Saving: Evidence from a P | ⛔ phantom / unverifiable | high | — · No Chile paper by this title; 'children as retirement saving' appears only as a theory fra |
| 4 | The effect of social insurance on savings and fertility: e | ⛔ phantom / unverifiable | medium | — · No NCMS->savings+fertility paper; nearest real study (Bai & Wu, NCMS & consumption) is off |
| 5 | The Impact of Social Security on Fertility: A Quasi-Experi | ♻️ duplicate of an included study | high | `10.1371/journal.pone.0234657` · Clean topical match to Shen/Zheng/Yang (NRPS, DiD on CFPS). No distinct paper of this titl |
| 6 | The impact of pension reform on fertility: Evidence from C | ♻️ duplicate of an included study | high | `10.1371/journal.pone.0234657` · Garbled variant of the Shen NRPS->fertility study; no separate paper located. |
| 7 | Social Security and Fertility: Evidence from a Pension Ref | ♻️ duplicate of an included study | medium | `10.1371/journal.pone.0234657` · No distinct paper found across RePEc/SSRN/Scholar; best match is the Shen NRPS study (like |
| 8 | Pension Policy Reform and Fertility: Micro Evidence from G | 🟡 new — real, PDF unavailable (retry) | high | — · REAL distinct paper: Zelu, Iranzo & Perez-Laborda, 'Pension Policy Reform and Fertility: M |
| 9 | Social Security as a Commitment Mechanism: Theory and Evid | ⛔ phantom / unverifiable | high | — · No 'social security as a commitment mechanism / rural China' paper locatable; title appear |
| 10 | The impact of social security on fertility: Quasi-experime | ⛔ phantom / unverifiable | medium | — · No quasi-experimental Hungarian pension->fertility study exists; the country in the title  |
| 11 | Pensions and Fertility in Austria | ♻️ duplicate of an included study | medium | `10.1257/pol.20200440` · 'Pensions and Fertility' uniquely identifies Danzer & Zyska (AEJ:EP 2023, IZA DP 13048); s |
| 12 | An analysis of the relationship between old age pension an | ⛔ phantom / unverifiable | medium | — · Zero exact-title hits; setting confirmed not Turkey. Its stored abstract is an organic-che |
| 13 | The Old-Age Security Motive for Fertility: Evidence from t | ♻️ duplicate of an included study | medium | `10.1257/pol.20200466` · Title stem 'The Old-Age Security Motive for Fertility: Evidence from the Extension of...'  |
| 14 | Old-Age Security Hypothesis and Fertility Decisions: Evide | ⛔ phantom / unverifiable | low | — · Loose paraphrase; best thematic match is the Rossi & Godard Namibia paper (i.e. likely a d |
| 15 | Effects of Pension Reform on Household Fertility and Savin | ♻️ duplicate of an included study | medium | `10.1371/journal.pone.0234657` · NRPS setting anchor matches Shen/Zheng/Yang; '...and Saving Behaviors' + 2023 date do not  |
| 16 | Social Security and Fertility: Evidence from China | ♻️ duplicate of an included study | medium | `10.1371/journal.pone.0234657` · Generalized/garbled form of the Shen NRPS->fertility study; no more authoritative match ex |
| 17 | The Consequences of Raising the Retirement Age: Evidence f | ⛔ phantom / unverifiable | high | — · The real 2011 paper with this title (Staubli & Zweimueller) is a LABOR-MARKET study of old |
| 18 | Do Public Transfers Crowd Out Private Support to the Elder | ✅ new — PDF fetched | medium | `10.4284/0038-4038-2013.055` · Real on-topic paper: Amuedo-Dorantes & Juarez, old-age transfers crowding out private gift |
| 19 | The impact of non-contributory pensions : a case study for | ✅ new — PDF fetched | high | — · Real exact-title match: Elizondo, Flores & Quinto (2018), 'The Impact of Non-contributory  |
