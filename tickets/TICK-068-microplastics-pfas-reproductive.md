# TICK-068: B.6. Microplastics and PFAS in Reproductive Tissues
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `microplastics-pfas-reproductive` — HYPOTHESES-v5.md §B.6
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/microplastics-pfas-reproductive-*, extraction/microplastics-pfas-reproductive-*, output/chapters/microplastics-pfas-reproductive-{pfas,microplastics}.md, source/build/goldset/13*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3a. A3 cold-start anchors sourced and gated — **done 2026-08-14, 32/32 verified**
- [ ] 3b. A4 Tier A / Tier B citation frame — **done 2026-08-14, 14,561 records, 0 failed requests**
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/microplastics-pfas-reproductive.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise — **run twice, once per chemical family; never pooled across**
- [ ] 10. Demographic significance against SDT — **run twice, each family against its own exposure series**
- [ ] 11. GRADE rating, 3 independent raters — **run twice; no bundled B.6 rating at any stage**
- [ ] 12. Chapter drafts on the §6 template — **two chapters** (Call 1, decided 2026-08-14):
  - [ ] 12a. `output/chapters/microplastics-pfas-reproductive-pfas.md`
  - [ ] 12b. `output/chapters/microplastics-pfas-reproductive-microplastics.md`
- [ ] 13. RA lay-readability check, both chapters
- [ ] 14. PI review and sign-off, both chapters

## Log

**2026-08-14 — opened (Shravan).** Scripts for this hypothesis start at
`source/build/goldset/132_b6_*`. 131 is the highest number in use anywhere — it is on the
unmerged `066-antidepressants-ssri-subfecundity` branch, and 115 is on `062-postmaterialism-…`,
which exists only locally and is invisible from `origin`. Numbering above `main` alone would have
collided a third time.

**2026-08-14 — stage 2 done (Shravan): search strategy and scope drafted.**
`literature/search-logs/microplastics-pfas-reproductive-search-scope.md`, built on the B.7 template,
against two live OpenAlex passes (`132_b6_recon_probe.py`, 72 probes; `133_b6_anchor_retry.py`, 20
probes; **zero failed requests in both**, so the zero counts are absences and not refusals). Nine
walls specified, five scope calls raised with recommendations. Three findings drive the design:

1. **B.6 bundles two hypotheses with opposite profiles.** PFAS has real human fertility epidemiology
   (time-to-pregnancy n = 127, two prior meta-analyses) and a *falling* legacy exposure series —
   NHANES reports PFOS and PFHxS declining after production was discontinued. Microplastics has the
   new tissue-detection literature and a *rising* series, but essentially no human fertility
   epidemiology. v5's note that "the exposure is structurally rising" is false for the half that
   carries the evidence. Call 1 asks for per-family verdicts.
2. **No quasi-experimental estimate of either exposure on a fertility quantity exists.** The only
   natural experiment found (Waterfield et al. 2020, a difference-in-differences on a Minnesota water
   filtration plant) has birth weight and preterm birth as outcomes, so Wall 2 routes it out. The
   GRADE ceiling is set before the search runs, on design rather than volume.
3. **Three of v5's four seminal citations do not resolve as written**, including one that is a
   phthalate paper — i.e. on the B.2 side of the wall that defines B.6. Detailed in Call 4 for
   TICK-001, with a recommendation to re-verify the other v5-era entries on the same gates.

**2026-08-14 — Call 1 decided; walls frozen.** B.6 stays **one hypothesis, one entry in
`HYPOTHESES-v5.md`, one ticket, one search**, and produces **two chapters** — one per chemical
family. The split lands at extraction, on `CHEMICAL_FAMILY`; everything upstream (walls, screen,
anchors, PRISMA identification and screening counts) is shared, and stages 9–14 run twice. Promoting
the families to B.6.a/B.6.b in the hypothesis list was considered and **not** done: the taxonomy is
TICK-001's to change, and renumbering the master list propagates into every in-flight branch's
`HYPOTHESES-v5.md §X` reference. The registry question goes to the PI for v6 alongside the Call 4
citation corrections, since both edit the same entry. With Call 1 answered, **the nine walls are
frozen**; Calls 2, 3 and 5 remain open and none of them blocks the search.

**2026-08-14 — Calls 2, 3 and 5 decided; A3 anchors done (32/32 verified).** Call 2: two-track
synthesis on `PARITY_HANDLING`, with the gap between tracks reported as a quantity of interest.
Call 3: Waterfield et al. (2020) stays excluded from synthesis but is **extracted and reported as a
flagged aside** under a new `ASIDE_EXTRACTED` disposition — a routed-out record carrying stronger
identification than anything included, reported with its estimand mismatch stated in the same
sentence as its estimate, and barred from every pooled quantity and recall denominator. Candidate
rule for PROTOCOL §5.9, flagged not added. Call 5: detection rated as exposure, never as effect.

A3 (`134_b6_cold_start_anchors.py`) resolved 32 anchors, all verified live, across 13 estimand cells
with one routing decoy per wall. Two defects in the **inherited** B.7 resolver surfaced, both found
by testing the new gate rather than by reading:

1. **Three shadow patterns were dead code.** They are matched against `norm()`-stripped titles, which
   remove all punctuation, so `^re\s*:`, `^corrections?\s+(to|for)` and the `letter to the editor`
   variant could never match the live forms `Re: X`, `Correction: X`, `Letter to the editor, X`. The
   miss surfaced because "Correction: The Minderoo-Monaco Commission…" scored 120, **tied with the
   article of record**, and was kept out of the anchor slot only by the tie-break. Fixed; shadow
   catches went 7 → 12 with one integrity flag. A start-up self-test on eight real pairs now aborts
   the run if the gate under-refuses. **`124_b7_cold_start_anchors.py` has the same three holes and
   its docstring claims a "Re:" catch it cannot have made** — needs fixing on the 066 branch.
2. **The duplicate-record gate's motivating case was misdiagnosed, and the gate could have caused
   harm.** `aogh.4056` and `aogh.4083` share title, year, volume and venue but are *different works* —
   48 authors under Landrigan versus a single-author companion piece by Maria Neira — and the author
   gate separates them correctly on its own. Since `author_match` returns None (passes) when a record
   has no author metadata, a bare title+year+venue rule would have silently demoted legitimately
   distinct same-title works. Demotion now requires positive author agreement. The gate has **zero
   confirmed catches** and is retained only as an unvalidated safeguard.

**2026-08-14 — A4 Tier A/B frame built (`135_b6_tier_ab_frame.py`).** 14,561 deduplicated Tier B
records from 32 seeds, **zero failed requests**, 60% carrying an abstract. Three changes on B.7's
builder: a second per-seed diagnostic (`animal >=`, a lower bound on the non-human share, because
Wall 5 is this chapter's biggest precision threat and it deserves a number); review seeds
forward-cited but **excluded from the empirical count**, which drops the causal recall denominator
from 9 to **6** — filing the three channel-1 reviews under a primary cell was right for the estimand
and wrong for the denominator; and the forward cap raised 1200 → 2000 for B.6's much larger clouds.

Three findings worth carrying into A5/A6:

1. **The routing decoys are the richest fertility-dense channels in the frame, by a wide margin.**
   The Wall 7 decoy (Levine 2017, sperm-count trend) runs **77% on-topic** — the highest of any seed —
   and the Wall 1 mixture decoy (Bellavia 2022) **51%**, against 22–47% for the PFAS primary seeds.
   1,849 Tier B records (13%) depend on a decoy seed alone and **would not exist under the inherited
   never-forward-seed-a-decoy rule.** This is the strongest confirmation yet of the D.2.d correction.
2. **The two families separate cleanly on the diagnostic.** PFAS primary seeds: 22–47% on-topic.
   Microplastics detection seeds: **2–19%**, with Plasticenta at 2.6%, Leslie at 2.5% and Schwabl at
   2.4%. The MP half of the chapter has no fertility literature to find, measured rather than
   asserted, and this is independent evidence for the Call 1 split.
3. **Wall 5's floor is 6–42% depending on seed**, highest on the oyster decoy as designed. Even the
   PFAS clouds carry 6–22% visibly non-human, so species must be checked on every record at screen.

Three seeds hit the 2,000 cap (Plasticenta, Leslie, Olsen half-life); the log now estimates the cost
at ~76 on-topic records unseen against a frame of 14,561, all three being 2.5–5% yield seeds.

Also filed earlier as a **duplicate-record gate** (the Minderoo-Monaco Commission carries two DOIs with different
citation counts plus an erratum, so DOI-level dedup double-counts it), and a correction to B.7's
scope, which wrongly lists B.6 among the hypotheses whose exposure post-dates its phenomenon — B.6's
exposure is older than the SDT; only its *measurement* is recent.
