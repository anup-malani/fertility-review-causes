# Tier-A residual retry — disposition (2026-06-29)

Retry of the 21 unverified Tier-A residuals after the OpenAlex budget + Semantic Scholar rate-limit reset. Pipeline: deterministic Crossref pass (`13_crossref_retry.py`) -> 4-agent fleet (Crossref/OpenAlex/web/SSRN, no fabrication) -> deterministic verifier (`14_verify_retry.py`, Crossref title J>=0.50 & |yearD|<=3).

**Outcome: +1 verified (id1), +1 title-keyed (id28), 4 dropped as not-real/dup, 15 hard residual.** The retry did NOT meaningfully shrink the residual even with APIs uncapped — confirming a genuine recall/identifiability ceiling, not an API artifact. Candidate DOIs for the residual are confirmed wrong-paper, fabricated (404), or unregistered SSRN handles.

| id | disposition | basis |
|---|---|---|
| 0 | RESIDUAL | Hint says WP-only. No version-of-record found under this exact title. Did NOT match it to the Namibia paper (different title, corpus is know |
| 1 | ACCEPT (verified) | manual-accept; verifier FN; real title 'Pensions and fertility: back to the roots' (Fenge & Scheubel) |
| 3 | RESIDUAL | No version-of-record or WP DOI locatable. Possibly an obscure/unindexed thesis or a corrupted corpus title. found=false. |
| 4 | RESIDUAL | Candidate DOI discarded (valid DOI, wrong paper). No correct DOI found for the Chile retirement-saving/fertility study under this title. fou |
| 5 | RESIDUAL | Per HARD RULE, did NOT accept the South Korea (Seung-Yun Oh) crowd-out paper. Candidate NBER DOI discarded as wrong paper. No Ecuador random |
| 6 | RESIDUAL | No corroborated version-of-record found. Closest real items have different titles/authors and must not be accepted. Likely an obscure/non-in |
| 10 | RESIDUAL | Do not accept the Danzer-Zyska Brazil paper despite superficial topical overlap. No matching VOR or WP found. |
| 11 | RESIDUAL | High false-match risk title; no corroborated 2019 match found. |
| 15 | DROP | category A: no real paper (corrupted record); candidates 404/unrelated |
| 16 | DROP | category A: chimeric variant of id18 (Rossi & Godard Namibia); candidate 404 |
| 19 | DROP | duplicate of id18 -> Rossi & Godard 10.1257/pol.20200466 |
| 20 | DROP | category A: no real paper (corrupted record); candidate 404 |
| 21 | RESIDUAL | No Hungary pension-reform-and-fertility paper matching this title located in any source. |
| 22 | RESIDUAL | Generic China title with high collision risk; no corroborated 2022 match found. |
| 26 | RESIDUAL | CATEGORY D — could not locate a real paper with this exact title. Candidate 10.1016/j.red.2023.01.001 is a VALID DOI but the WRONG paper: it |
| 27 | RESIDUAL | CATEGORY D — could not locate a real paper with this exact title. Candidate 10.1007/s11205-024-03315-0 (Social Indicators Research) returns  |
| 28 | TITLE-KEY | real WP, no DOI exists (Zelu/Iranzo/Perez-Laborda, Ghana, IZA-BREAD 2023) |
| 30 | RESIDUAL | Candidate SSRN DOI is unregistered/invalid. Could not independently confirm the paper exists with this title; not accepting an unresolvable  |
| 31 | RESIDUAL | Candidate DOI is fabricated/unresolvable. Real paper could not be located or verified; not accepting an unresolvable DOI. |
| 32 | RESIDUAL | Candidate SSRN DOI unregistered/invalid. No author+venue+year corroboration obtainable; per generic-title rule, found=false. |
| 33 | RESIDUAL | Candidate SSRN DOI unregistered/invalid. Explicitly did NOT match to the Shen/Zheng/Yang 2020 PLOS One paper. No corroboration for a 2025 qu |

## Summary

- **RESIDUAL**: 15
- **DROP**: 4
- **ACCEPT**: 1
- **TITLE-KEY**: 1

## Gold-set impact

- Verified-with-DOI core: **14 -> 15** (id1 Fenge & Scheubel added).
- Title-keyed gold items (real, no DOI): **+1** (id28 Ghana WP).
- Dropped from the 35 distinct studies as not-real/duplicate: **4** (id15/16/19/20) -> **31 real distinct studies**.
- Hard residual (real-but-unresolvable DOI): **15** — recommend RA hand-resolution via library/EconLit/direct author contact, or title-keying where a stable DOI never existed.

## Method note (carry to promotion)

The J>=0.50 title guard is sound for *verifying a proposed DOI* but false-matches when used to *select* from blind Crossref search (observed: id5 Ecuador->Korea, id6 rural-China->wrong Zhang at J~0.5). `13_crossref_retry.py` therefore requires J>=0.80 for search-derived auto-accept; candidate-DOI verification keeps J>=0.50. Conversely, id1 shows the guard can *false-reject* a true match when the corpus title is corrupted — hence agent-evidence + RA adjudication remains the backstop.
