# TICK-077: C.3.e Credit Constraints and Liquidity
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `credit-constraints` — HYPOTHESES-v5.md §C.3.e
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/credit-constraints-*, extraction/credit-constraints-*, output/chapters/credit-constraints.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/credit-constraints.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Inherited boundary work

Three finished chapters have already routed evidence into this one. Read these before drafting scope:

- **C.2.c (housing).** Froze the boundary rule on 2026-07-31: neighbouring hypotheses are separated by
  *what varies*, not by the mechanism an author narrates. **C.2.c owns variation in housing prices;
  C.3.e owns variation in liquidity and credit terms; A.23 owns variation in co-residence.** Under that
  rule C.2.c routed out a 2026 *PNAS* cohort-DiD of a Chinese housing-provident-fund reform (the reform
  moved down-payment ratios, interest rates and loan ceilings, not prices) and created a
  `MIXED_PRICE_CREDIT` class, flagged unallocated and to be reported here. See
  `literature/search-logs/housing-costs-search-scope.md` §Wall 1 and `output/chapters/housing-costs.md` §6.
- **C.3.g (student debt).** General consumer, mortgage and medical debt is C.3.e's; C.3.g keeps only the
  prior education liability already spent.
- **A.23 (co-residence).** Owns living-arrangement variation whatever drives it.

## Open rulings to freeze at stage 2

1. **The registered claim names two configurations with opposite signs** — children as a savings/insurance
   vehicle where formal finance is absent (PM/FDT), and liquidity constraints on young households
   delaying births (SDT). Decide whether these are one chapter with two arms or two chapters, and freeze
   it before searching, not at synthesis.
2. **Registry defect inherited from C.2.c, still unfixed:** Lovenheim and Mumford 2013 is listed as
   seminal for both C.2.c and C.3.e. C.2.c's recommendation was to drop it from C.3.e's seminal list and
   cross-ref C.2.c instead; it was flagged, not acted on. This chapter resolves it.

## Log

### 2026-09-01 — scope drafted, both rulings resolved

- `literature/search-logs/credit-constraints-search-scope.md`. Six walls frozen; estimand cells,
  required tags, pooling rule and the demsig pre-specification written before any query.
- **Ruling 1 (asked by Shravan: are the two treatments the same?): no, but they are not separable.**
  Arm S (saving/insurance instrument availability) acts on the *value* of children; Arm B (borrowing
  terms) acts on the *intertemporal budget constraint*; a pure shock to either leaves the other
  untouched. But composite financial-access designs — branch expansion, microfinance, inclusion
  reform — move both at once in opposite directions, and their estimates cannot be allocated to
  either arm. So: **one chapter, two arms, three strata; arms never pooled or averaged; GRADE and
  demsig per arm per phenomenon** (A.18 multi-arm precedent), ≥3-effects test applied after
  stratification.
- **Ruling 2 (RA-authorised by Shravan; awaiting PI confirmation): acted on.** Lovenheim and Mumford 2013 struck from C.3.e's
  `seminal` list in HYPOTHESES-v5.md and cross-referenced to C.2.c, with an in-place RA-edit
  annotation for PI confirmation at TICK-001. C.2.c had recommended and flagged this on 2026-07-31.
- **Two PI calls opened.** Call 1: C.3.c's written chapter already claims "money in a bank, an
  insurance policy" as its substitutes, so Wall 1 — longevity risk to C.3.c, within-life risk to
  C.3.e — is the difference between a two-arm chapter and a one-arm one. Proceeding under the split,
  with a cheap probe to measure it before extraction. Call 2: inherited from A.24, unanswered —
  whether two chapters may both report the same study from a `MIXED_*` class.
- Next: cold-start anchors (hand-sourced, recall scored **per arm**), then the Arm S survival probe.

### 2026-09-01 — anchors resolved 26/26, PI Call 1 answered, shared resolver found dead

- `275_c3e_cold_start_anchors.py`, `276_c3e_arm_s_probe.py`; log at
  `literature/search-logs/credit-constraints-cold-start-anchors-log.md`.
- **26 candidates, 26 resolved, zero absences.** Nine Arm B anchors were inherited
  already-screened from C.2.c's `OFF_CREDIT_C3e` cell, plus the 2026 PNAS provident-fund study
  C.2.c routed here and had already extracted.
- **`title.search` is not a root OpenAlex parameter — the title channel failed 18/18 and every
  resolution silently fell through to `search=`.** Inherited from A.18's script 245, so every
  chapter's anchor resolution ran on the fallback. Fixed here with a quoted `filter=title.search:`
  rung; after the fix 0 of 26 resolve via the fallback. **Flagged to TICK-074** as a shared-resolver
  defect. Also: `%2C` does not escape a comma in a filter value, and the API's own error message
  recommends `%2C`.
- Two further false-absence defects fixed: `is_stem` was one-directional and refused book chapters
  carrying an added "Chapter 8" prefix; a colon-spanning title does not match as one stemmed phrase,
  so a head-quoted rung was added. Both surfaced real anchors that had read as missing.
- **PI Call 1 answered: Arm S survives.** On the on-estimand asset-motive vocabulary the frame is
  262 records, of which 36 (13.7%) are old-age framed — C.3.c has not taken the arm. The first
  measurement said 6.2% and was not usable: "health insurance" alone carried 90% of that block and
  is A.17's estimand, so it is banned from Arm S retrieval.
- One inherited record is a **version pair** (Xi Yang, two DOIs) whose headline sign flips between
  versions, from "More Credit, Fewer Babies?" to "More Credit, More Babies?" — one study, and the
  version of record decides its sign. C.2.c's stored snapshot is stale against the live record.
- Next: snowball the 26 anchors including decoys; production query per arm with per-arm recall.

### 2026-09-01 — snowball (pool 3,810) and production query frozen (frame 7,021)

- `277_c3e_snowball.py`, `278_c3e_production_query.py`, `279_c3e_query_repair.py`; log at
  `credit-constraints-snowball-and-query-log.md`.
- **Snowball pool 3,810, zero errors.** Reach by arm S 2,080 / composite 1,163 / B 745. Decoys were
  seeded deliberately and returned ~340 uniquely-reached records.
- **Four seeds reached 0-1 records because the resolver had matched "Replication data for:" deposits**
  — `dataset` records sharing the article's title, authors AND year, so the author and year gates gave
  no protection. My own bidirectional `is_stem` fix admitted them and its safety justification was
  wrong. Restricted to an allowlist of structural prefixes (chapter/part/section/volume), non-study
  types refused outright, citation count as tiebreak. 0 shadow records after; those seeds now reach
  211-346 each.
- **Version twins add 617 records, 16% of the pool.** Citations do not follow the version of record:
  Dettling and Kearney's JPubE article has 0 citations, its NBER twin 67. Twins found for 12 of 26
  seeds and snowballed with them.
- **Production query frozen at 7,021 records.** Anchor recall 8/11 (S 3/4, B 5/6, composite 0/1).
  Four repair terms kept of 26 candidates, each on gold recovered, not frame growth; `mortgage` was
  refused at +622 records and no gold.
- **A measurement bug in the repair loop, caught and fixed:** candidates were scored against a frozen
  baseline while the kept set grew, so later terms inherited earlier terms' recoveries. It had accepted
  17 terms and 737 records of frame for zero gold.
- **Probes recall 0/9, and that is the composite stratum's answer.** None of the microcredit RCTs,
  savings experiments or branch-expansion studies mentions fertility in its abstract, because none
  measures it. `PRIMARY_COMPOSITE_ACCESS` may be empty — which would leave the sign-flip question
  without direct evidence. Full-text check on the nine before any such statement.

### 2026-09-01 — probe full-text check: 6 of 10 read, zero fertility outcomes

- `280_c3e_probe_retrieval.py`, `281_c3e_probe_outcome_scan.py`, `282_c3e_scan_control.py`; log at
  `credit-constraints-probe-fulltext-check.md`.
- **Zero fertility or birth outcomes in six probe full texts** (~450k chars). The two apparent hits
  were "purchasing power parity" and "place of birth". Two independent channels — abstract indexing and
  full text — now agree, and they fail for unrelated reasons.
- **The scan was validated on positive controls first**: Cumming and Dettling 175 hits / 17 strong,
  Dettling and Kearney 243 / 15, correctly classified. A detector that fires on nothing is
  indistinguishable from a broken one.
- **`?` and `!` inside a QUOTED filter value return a silent zero** — valid meta, no error. All seven
  seeds with a `?` in the title returned zero twins. After the strip: twins for 16 seeds not 12, pool
  3,976, and 870 records (22%) twin-only. Banerjee's OA twin appeared only after this fix.
- Retrieval 6/10, and the twin rung produced 5 of the 6 fetches. Four outstanding, split by cause:
  **browser-job** (Attanasio, Bruhn — open URLs killed by bot defence, 403) and **proxy-job**
  (Guinnane, Prina — no open copy).
- **Status of the composite cell: UNRESOLVED, not empty.** 6 of 10 checked, 0 positive. If the last
  four come back negative, `PRIMARY_COMPOSITE_ACCESS` is empty and the sign-flip question that made
  this one chapter has no direct evidence — UNEVALUATED with GRADE No evidence. Ruling 1 is unaffected:
  the arms stay unpoolable either way.

