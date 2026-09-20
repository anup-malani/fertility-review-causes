# Channel-3 citation snowball (Tier-B frame) — A.9 population age structure and demographic momentum

**Run:** 2026-09-20, Shravan (TICK-089). **Artifact:**
`population-age-structure-momentum-snowball-tierb.json` — 199 records, deduped vs the 12 channel-2
seeds. All records are OpenAlex works (existence intrinsic).

## Method (GACS C2)

Seeds = the 12 identity-verified channel-2 anchors (decoys and the channel-1 near-miss excluded).

- **Backward:** `referenced_works` pulled for every seed; the Tier-B backward core is the references
  **co-cited by ≥ 2 seeds** (16 of 114 unique references). The 98 single-seed references are a
  documented **expansion reserve**, not pulled now — they carry the weakest orthogonal signal and would
  add noise to a scope-stage frame.
- **Forward:** `cites:` run **only on the 5 topic-specific momentum seeds** (Bongaarts–Bulatao 1999,
  Lutz et al. 2003, Kim–Schoen 1997, Blue–Espenshade 2011, Krishnamoorthy 1981), capped at the top 50
  by citation count each. **Forward cites were deliberately NOT run** on the broad theory anchors —
  Keyfitz 1971 (201 citing), Preston–Heuveline–Guillot (1,772), Kitagawa 1955 (562), Schoen–Kim 1991,
  Frejka, Chesnais, Coale, Preston–Guillot — which would explode the frame (the GACS forward-citation
  caution; those are backward-only).

## Result — 199-record Tier-B frame

Provisional cells (title heuristic only; the real Haiku→Sonnet→RA screen happens at stage 3):

| Provisional cell | n |
|---|---:|
| OFF_OTHER (mostly mathematical-demography theory canon) | 119 |
| FERT_OTHER (fertility-related, needs screening) | 41 |
| MOMENTUM | 18 |
| OFF_OUTCOME_POP (population aging/size) | 13 |
| OFF_TEMPO_A11 (tempo boundary) | 6 |
| OFF_OTHER_ECOLOGY_HOMONYM / AGE_STRUCT_AMBIG | 2 |

## Findings

1. **Orthogonal momentum recall works.** 18 momentum-tagged records surfaced that are not in the seed
   set (e.g., "Momentum and the growth-free segment of a population"), plus the top co-citations are the
   formal-demography backbone the momentum literature rests on — Lotka ("Théorie Analytique des
   Associations Biologiques"; "Introduction to the Mathematics of Population"), Keyfitz ("Applied
   Mathematical Demography"), Coale ("The Relation Between Actual and Intrinsic Growth Rates"). These are
   theory-stream anchors (my heuristic parked them in OFF_OTHER; re-tag at screen). The snowball is doing
   its job as the orthogonal channel.
2. **The A.11 boundary is real in the citation network (6 tempo records).** Confirms Wall 1 is a live
   routing task, not a hypothetical — the frame probe's 136 in-frame tempo overlap has a citation-graph
   counterpart. These route to A.11 at the component level.
3. **The empirical birth-rate/count decomposition cell stays nearly empty even through the network.**
   Nothing in the top co-citations is an identified decomposition estimate; the network is theory +
   projection. Third independent confirmation (frame probe, channel-1/2 anchors, now channel-3) that
   `empty-cell-is-the-result` is the likely outcome and A.9 is a theory-plus-decomposition chapter.
4. **The frame is kept whole (unbiased-sample Tier B).** No keyword pruning — the 119 OFF_OTHER and 41
   FERT_OTHER stay in, because Tier B is the recall yardstick precisely because it was not curated to
   match the query. Provisional tags are for triage, not exclusion.

## Caveats

- Provisional cells are title-only heuristics; several OFF_OTHER records are theory canon that will
  re-tag to the theory stream, and FERT_OTHER needs the real screen.
- Tier B is co-citation-thresholded backward + capped forward, so it inherits a mild bias toward
  high-citation nodes and toward the momentum seeds' neighbourhood; the single-seed backward tail (98)
  and uncapped forward cites are the expansion reserve if stage-3 recall against this frame looks thin.
- Because the seeds' snowball was seeded off the same canon the keyword frame draws on, Tier B is **not
  fully orthogonal** to the keyword query — state this wherever Recall(B) is quoted (the standing GACS
  caveat).

## Next

At stage 3 (after the scope freezes — pending the two PI escalations + the Wall 1 second read), screen
the 199-record frame (Haiku→Sonnet→RA), use it as the orthogonal Recall(B) yardstick against the
momentum-anchored production query, and re-tag the theory-canon backbone into the JEL theory stream.
