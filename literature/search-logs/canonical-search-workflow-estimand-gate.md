# Implementing the Estimand Gate — Response to PI Critique #1

**Author:** Shravan (RA)
**Date:** 2026-07-06
**Companion to:** `canonical-search-workflow.md` (§E1, §E3), `canonical-search-workflow-pi-critique.md`
**Build step:** `source/build/goldset/34_estimand_gate.py` (deterministic; re-run reproduces every artifact)

---

## The critique this answers

The PI's first and deepest objection: GACS was built and graded to recover papers **on the topic**
(pensions and fertility), but the review's binding constraint is narrower — does a paper **identify the
chapter's effect**: the old-age-security motive → fertility, forward direction, with fertility as the
outcome? Those are different populations. Grade the search against the topical population and it looks
strong; apply the actual inclusion criterion and most of what it "found" is out of scope. In the PI's
words, "the scarce resource in this pilot was never more papers. It was a sharp definition of what we
are trying to measure."

The fix he named: fold an estimand-and-mechanism gate into what "meta-analysis-ready" means, and
measure recall against an estimand-filtered gold rather than a topical one. This document implements
the gate and reports the collapse. It uses the RA's own inclusion adjudication (the `-ra-review.csv`
sheet: `RETRIEVE` = primary cell, `EXCLUDE` + a plain reason = off-cell) as the ground truth, and
classifies each decision into a primary-vs-off-cell taxonomy.

## Result 1 — the output set collapses: 44 topical → 10 estimand-ready

Of the 44 distinct topical "meta-analysis-ready" studies, 40 are DOI-resolved and RA-reviewed. Under
the estimand gate, **10 are estimand-ready** (identify the primary cell) and **30 are off-cell.** The
10 are the set that can share a pooled estimate:

| Study | Year | Gold anchor |
|---|---|---|
| Pensions and Fertility: Evidence from Germany | 2016 | E1 |
| What Explains Fertility? Evidence from Italian Pension Reforms | 2009 | E17 |
| Fertility and Financial Development: Evidence from U.S. Counties in the 19th Century | 2013 | — |
| The fertility effects of public pension: new rural pension scheme in China | 2020 | E12 |
| The Introduction of Bismarck's Social Security System … Prussia | 2021 | E14 |
| The Old-Age Security Motive for Fertility: … Social Pensions in Namibia | 2022 | E18 |
| Pensions and Fertility: Microeconomic Evidence | 2023 | E24 |
| The US baby boom and the 1935 Social Security Act | 2023 | — |
| Children as insurance revisited: … private insurance adoption among older parents | 2024 | E29 |
| The impact of long-term care insurance on family fertility behaviour: China | 2025 | E34 |

The 30 off-cell studies are **not junk** — they are real, well-identified papers that measure a
different quantity, and they are retained (routed to their own chapters' cells), not discarded. They
leave the primary cell for six distinct reasons:

| Why it leaves the primary cell | Count |
|---|---|
| **Outcome is not fertility** (schooling, parental survival, labor supply, savings, migration, health, birth weight, coresidence) | 16 |
| **Different cause / treatment** (child-grant subsidy, lottery income, female employment, kindergarten supply, welfare family cap) | 5 |
| **Fertility is the cause, not the effect** (fertility on the right-hand side) | 3 |
| **Different channel** (grandparental childcare — moves fertility the *opposite* way, and is central to the Second Transition) | 3 |
| **Reverse direction** (effect of children on old-age support / pension take-up) | 2 |
| **Not about old-age security** | 1 |

Full per-study tags are in `output/{slug}-estimand-adjudication.csv`; the pooling set is in
`output/{slug}-estimand-ready-set.md`.

## Result 2 — the corrected scorecard: 7 of the gold anchors are off-cell

This is the sharper half, because it repairs the **measuring instrument**, not just the output. The
recall number was computed against a gold set of anchor studies "the query must recover." Among the 16
strong-identification empirical anchors, **15 appear in the reviewed set, and 7 of them are off-cell:**

| Off-cell anchor | Leaves the cell because | Bucket |
|---|---|---|
| E8 — Intergenerational education spillovers of pension reform (Yuan) | fertility treated as exogenous; outcome is child schooling | fertility-as-cause |
| E23 — Are children substitutes for assets? Bangladesh (Ruthbah) | fertility is the treatment, instrumented | fertility-as-cause |
| E9 — Children's education and parental old-age survival (Neve–Fink) | outcome is parental survival | outcome≠fertility |
| E7 — Grandparental childcare and maternal labor supply, Italy (Bratti) | outcome is maternal labor supply | outcome≠fertility |
| E2 — Grandmothers and Granddaughters, South Africa (Duflo) | outcome is child anthropometrics | outcome≠fertility |
| E13 — Retirement, intergenerational time transfers, fertility (Eibich–Siedler) | grandparental-childcare channel (opposite sign) | different-channel |
| E25 — Fertility and parental retirement (Ilciukas) | grandparental-childcare channel (opposite sign) | different-channel |

This reconciles exactly with the PI's independent review ("7 of 14"). His "14" is the top-14 by rank;
keying on DOI and title (E2/Duflo matches only via a title-Jaccard fallback, a version-variant that
DOI matching drops) gives **15 anchors in review, 8 primary, 7 off-cell** — the same seven papers he
named. So **the instrument the query was tuned to maximize recall against pointed, for nearly half its
anchors, at studies outside the cell.** A method optimized against that instrument was partly optimized
to recover out-of-scope work. The estimand-filtered anchor set (the 8 primary-cell anchors) is written
to `source/build/goldset/estimand_filtered_gold.json` as the corrected recall denominator.

## What this does to the 72% recall

The pilot's ~72% is **topical** recall — recovery of topical anchors. Two things follow, one measured
now and one still owed:

- **Measured now:** the estimand filter removes 7 of 15 adjudicated empirical anchors (47%). So a
  topical recall figure credits the query, at roughly that rate among its anchors, for recovering
  papers the chapter cannot use. The headline number was recall toward a partly out-of-scope
  population — exactly the PI's charge.
- **Now measured (the Tier-B re-grade).** The estimand-filtered **Recall(B)** has been computed
  (`36a`/`36b`, report `output/{slug}-estimand-recall-regrade.md`). All 247 Tier-B papers were
  estimand-tagged by the calibrated gate, then the pilot's exact CV title-matching was re-run with the
  query held fixed and only the denominator partitioned by cell. Two findings:
  - **Tier B is mostly not the pooling population.** Of 247, **160 (65%) are theoretical models** and
    only **57 (23%) are empirical primary-cell studies**; the rest are off-cell empirics. The topical
    Recall(B) denominator is dominated by papers the meta-analysis does not want.
  - **The number moves *up*, not down: topical Recall(B) 72.5% → estimand-filtered 82.5%** (88% on
    high-confidence tags). The re-grade reproduces the 72.5% headline exactly on the full denominator,
    so the matching is identical; re-based on the primary cell it *rises*, because the recall the query
    was losing sat in the theory/off-cell tail, not in the papers that identify the effect.

  **The two halves of point 1 fit together and both land on the PI's thesis.** The *output* set
  collapsed (44 → 10) — a precision/definition problem — while *recall* of the primary-cell papers is
  strong (82.5%). So recall was never the binding constraint; the definition of "meta-analysis-ready"
  was. "The scarce resource was never more papers; it was a sharp definition of what we are measuring,"
  shown now from both sides. (Caveat against over-reading the good recall: primary-cell papers tend to
  *name* the effect in their titles, so they are keyword-findable almost by construction; the residual
  leak is the quirky-titled canon the snowball exists to catch.)

## How the gate runs in production (future hypotheses)

On the pilot the gate reads the RA's `RETRIEVE`/`EXCLUDE` decisions — high-quality human adjudication.
For a new hypothesis the same gate runs on **Sonnet's extracted fields** (evidence type, outcome,
mechanism/channel, causal direction — GACS §D2b), testing each candidate for membership in the
chapter's declared primary cell before it is called meta-analysis-ready. The pilot's RA decisions are
the calibration set for that automated gate.

**Calibration result (done).** Sonnet classified all 40 reviewed studies **blind** — title + abstract
only, no RA decision and no earlier relevance rationale (steps `35a_make_estimand_batches.py` +
a 4-way Sonnet fleet + `35b_score_estimand_calibration.py`; full report
`output/{slug}-estimand-calibration.md`). Against the RA ground truth the automated gate scores
**100% precision / 80% recall on the primary-vs-off-cell decision** (accuracy 95%, Cohen's κ = 0.86):

- **Zero false positives** — no off-cell paper was admitted to the pooling set. The gate is *safe*:
  it will not silently pollute a meta-analysis on a hypothesis with no RA pass.
- **Two false negatives**, both genuinely borderline: *Children as insurance revisited* (E29), where
  the design instruments the number of children — Sonnet read it as reverse-direction, which is
  defensible; and *The US baby boom and the 1935 Social Security Act*, whose abstract foregrounds
  family allowances (positive sign) rather than the old-age pension motive. These are exactly the
  boundary-band cases GACS already reserves for the RA verdict (§D).
- **Off-cell bucket (routing) agreement: 83%** (25/30) — disagreements are within-off-cell (which
  *other* cell a paper routes to), not gate flips.

So the production recipe is measured, not assumed: **run the automated gate, trust its PRIMARY
admissions (100% precise), and route only its off-cell and borderline calls to the RA** — not the
whole set. Caveats (n=40, one hypothesis; RA decisions are themselves the yardstick; 10-per-agent
batching; 3 title-only) are in the calibration report.

## Artifacts

**The gate (step `34_estimand_gate.py`, deterministic):**
- `output/{slug}-estimand-ready-set.md` — the 10 primary-cell studies + the off-cell taxonomy.
- `output/{slug}-estimand-adjudication.csv` — all 40 reviewed studies, each with `estimand_cell`,
  `off_cell_reason`, and `is_gold_anchor`.
- `source/build/goldset/estimand_filtered_gold.json` — the 8 primary-cell empirical anchors (the
  corrected recall denominator) and the 7 off-cell anchors with reasons.

**Automated-gate calibration (steps `35a`/`35b` + a 4-way Sonnet fleet):**
- `output/{slug}-estimand-calibration.md` — the 100% precision / 80% recall report + every disagreement.
- `source/build/goldset/estimand_calib_sonnet.json` — the frozen blind Sonnet classifications.

**Tier-B re-grade (steps `36a`/`36b` + a 6-way Sonnet fleet):**
- `output/{slug}-estimand-recall-regrade.md` — the recall move (72.5% → 82.5%) + Tier-B cell mix.
- `source/build/goldset/estimand_tierb_tags.json` — the frozen estimand tag for all 247 Tier-B papers.

## Honest limitations

1. **The Tier-B re-grade uses automated tags, not RA sign-off.** The estimand-filtered Recall(B)
   (82.5%) is now computed, but the 247 Tier-B tags come from the calibrated gate (100% precision / 80%
   recall vs the RA), not individual RA adjudication; 148 Tier-B papers are title-only, so the
   theory-vs-empirical split is robust (model titles are distinctive) but the primary/off-cell line
   within the empirics is softer (the HIGH-confidence sensitivity brackets it at 88%). A spot audit of
   the theory routing would harden the number.
2. **One anchor (E28) is not in the reviewed set** — it is "Pension Policy Reform and Fertility: Micro
   Evidence from Ghana" (2024), a no-DOI working paper that never reached the DOI-resolved review sheet.
   Its title places it in the primary cell, but it is unadjudicated here; this is a resolution gap
   (§7's PDF/DOI acquisition), not an estimand-tagging gap. 15 of 16 anchors are covered.
3. **The primary cell is drawn narrowly on purpose.** The grandparental-childcare channel (E13, E25)
   is a *real* pension→fertility effect of the opposite sign; excluding it from this cell is correct
   for pooling but those papers are load-bearing elsewhere (they are, per the PI, central to the Second
   Transition). The gate routes rather than discards them.
4. **Estimand tags for future hypotheses are only as good as Sonnet's extraction** — now *measured*
   (100% precision / 80% recall vs the RA; see the calibration section). The residual risk is the
   recall gap on borderline estimands, which the RA boundary-gate covers; the automated gate should
   not be run fully unsupervised on a hypothesis whose primary cell is subtle without spot-checking
   its off-cell calls.
