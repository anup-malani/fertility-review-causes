# Fine-filter procedure (stage 2)

**Status:** DRAFT for Shravan's review — 2026-07-09. The extractability gate (§4) and the
target-parameter definition (§4.1) are the genuinely new design work; §§2–3 assemble vetted
pieces. Decisions flagged **[CONFIRM]** need Shravan's call before implementation.

Companion to `canonical-search-workflow.md` (GACS) and `canonical-search-workflow-estimand-gate.md`.

---

## 1. Where the fine filter sits

The **coarse filter** is everything through the LLM screen and the estimand gate: search → tiers →
the estimand-ready pooling set, RA-signed at the gate (steps 49–52). Its output is a set of papers
that *identify the chapter's effect* — for the OAS pilot, the primary cell **old-age-security motive
→ fertility (forward, fertility-outcome)**.

The **fine filter** takes that in-cell set and produces the **pooling-ready set**: the papers from
which an actual pooled estimate can be computed, with a harmonized effect size per study. It is the
last sieve before meta-analysis.

```
coarse: search → screen → estimand gate → RA gate   →  in-cell set (identifies the effect)
fine:   dedup → existence → EXTRACTABILITY           →  pooling-ready set (yields a poolable number)
```

The fine filter does **three jobs** (the PI's framing): remove duplicates, remove hallucinations,
keep only papers that identify — and *report an extractable estimate of* — the target parameter.
Jobs 1–2 already exist as tested components; job 3 is where the new work is.

---

## 2. Job 1 — Deduplication (assembly)

**Reuse `26c_dedupe_studies.py`.** Study-level dedup by DOI → normalized-title, with the
author-surname+year+title-containment merge that caught the working-paper/published version variants
(Danzer & Zyska, Edmonds) and Shen 2020's six mangled titles. A meta-analysis pools **distinct
studies**, so version variants (NBER WP ↔ published VoR) collapse to one record, preferring the
version of record.

*Pilot state:* the pooling set was already study-level-deduped upstream (44 distinct studies →
estimand gate). For a fresh chapter the fine filter runs this first, before anything expensive.

---

## 3. Job 2 — De-hallucination / existence (assembly)

**The existence-verification gate is now mandatory** (the ghost-citation finding, 2026-07-08). No
paper enters the pooling set without a **resolved live DOI or a confirmed live record** (OpenAlex +
Crossref, both must return a real 200-match; a rate-limit/timeout is *unconfirmed*, never *absent* —
the verifier is three-state). Ghost citations — fabricated snowball forward-citations built from
query vocabulary — get quarantined here. Reuse the de-ghost logic in `44/48` and the
abstract-or-live-DOI gate; keep the **harder forward-vs-backward citation cap** (7/8 known ghosts were
forward-citation records).

*Pilot state:* the corpus was de-ghosted for the recall number; the fine filter re-affirms existence
on the confirmed pool as a cheap guard (any survivor without a live record is pulled).

---

## 4. Job 3 — Extractability (the new work)

The estimand gate answers *"does this paper identify the target relationship?"* Extractability asks
the next question: **"can we pull a poolable estimate of it out of this paper?"** A study can be
squarely in-cell yet contribute nothing to a pooled number — it may report the effect only
qualitatively ("pensions significantly reduced fertility"), or in a form we cannot map onto a common
metric. Those papers inform the **narrative synthesis** but not the **forest plot**. This is the
sharp new line the fine filter draws.

### 4.1 The target parameter **[CONFIRM]**

To pool, every study must reduce to one commensurable quantity. Proposed:

- **Primary estimand:** the **semi-elasticity of fertility with respect to old-age-security /
  pension wealth** — the % (or level) change in a fertility outcome per unit increase in pension
  wealth (or per unit of the reform's wealth-equivalent). This is the economically meaningful
  *crowd-out* object and the structural parameter the chapter is about.
- **Problem:** many identifying studies exploit reforms and report the effect of *eligibility* or
  *exposure*, not of a wealth amount — so the primary semi-elasticity is not directly recoverable
  for them.
- **Proposed fix — two nested extractable sets (mirrors the topical/estimand nesting already in
  GACS §E1):**
  1. **Extractable-primary:** studies reporting (or allowing reconstruction of) the wealth-denominated
     semi-elasticity. Pool these directly → the headline number.
  2. **Extractable-standardized:** the broader set, harmonized to a **standardized effect size**
     (partial correlation coefficient *r*, or a standardized regression coefficient) computable from
     any regression reporting a coefficient + uncertainty + N. Pool these as the main quantitative
     synthesis; the primary subset is a sensitivity/anchor check. Every conversion carries documented
     assumptions.

  **[CONFIRM with Shravan]:** (a) is the semi-elasticity the right primary object, or do you want the
  *elasticity* (%/%) or a per-SD effect? (b) is *r* the right common metric for the broad pool, or a
  standardized mean difference / % effect on the TFR? This choice defines the whole meta-analysis.

### 4.2 What "extractable" requires

A study passes extractability if, for the target relationship, we can obtain **all** of:

| Field | Requirement |
|---|---|
| point estimate | signed magnitude of the effect |
| uncertainty | SE, CI, or t / (p + df) — enough to weight the study |
| treatment definition + units | what varied, in what units (wealth, eligibility, reform dummy) |
| outcome definition + units | TFR, births, parity, completed fertility, etc. |
| sample | N, population, setting, period |
| mapping | direct value of, or a documented conversion to, the chosen effect size (§4.1) |

Miss any of these irrecoverably → **not extractable** → routed to narrative synthesis, recorded, not
pooled. Passing the estimand gate but failing here is expected and fine; it is a real, reported outcome.

### 4.3 Operationalization (calibrated, like the estimand gate)

1. **Extraction pass (Sonnet over full text + results tables).** Emits the §4.2 structured record +
   `can_extract` (bool) + `confidence` + the raw quoted table/sentence the number came from
   (auditability). Full text is required — **abstracts are insufficient for extraction**; this raises
   the PDF-coverage bar (see §5).
2. **Calibrate against an RA-extracted gold subset.** Hand-extract ~15–20 of the confirmed pool, then
   score the LLM on (i) the `can_extract` decision (precision/recall/κ, as with the estimand gate's
   κ≈0.86) and (ii) numeric agreement on the extracted estimate and SE. Report the calibration before
   trusting the automated extraction.
3. **RA verifies every pooled number.** Extraction errors corrupt the estimate directly, so the RA
   confirms the point estimate + uncertainty for each study that enters the pool (the auditable quote
   makes this fast). This is the human gate for stage 2, analogous to the estimand RA gate.

---

## 5. Prerequisite this surfaces: PDF coverage

Extraction needs **results tables, not abstracts**. Current study-level PDF coverage on the OAS pool
is partial (was 28/44). Before the extraction pass we need near-complete full-text coverage on the
*confirmed* pooling set (much smaller than 44 after the RA gate), via the existing acquisition steps
(`27/28/30`) + the want-list. Papers we cannot obtain full text for are extraction-blocked and must be
flagged, not silently dropped (silent drops bias the pool toward easy-to-obtain studies).

---

## 6. Sequence & outputs

```
in-cell set (RA-signed, step 52)
  → 53  study-level dedup            (reuse 26c)
  → 54  existence re-affirm          (reuse 44/48 three-state verifier)
  → 55  PDF coverage reconcile       (reuse 27/28/30; flag extraction-blocked)
  → 56  extraction pass (Sonnet)     + can_extract + auditable quote
  → 57  calibrate vs RA gold subset  (κ + numeric agreement)
  → 58  RA verify pooled numbers     (human gate)
  → 59  assemble pooling-ready set   + per-study harmonized effect size
```

**Outputs:** `{slug}-pooling-ready-set.json/.md` (studies + harmonized effect sizes + provenance
quote per number), `{slug}-extraction-calibration.md` (LLM-vs-RA), `{slug}-narrative-only.md` (in-cell
but not extractable — reported, not pooled), `{slug}-extraction-blocked.md` (no full text).

---

## 7. Honest scope notes

- For **this pilot**, jobs 1–2 are largely done upstream; the live new work is §4 (extractability)
  + §5 (PDF coverage). The procedure is written **general** so it drops onto any future chapter's
  coarse output unchanged.
- Extractability is deliberately *downstream* of the estimand gate: we only try to extract numbers from
  papers already confirmed in-cell, so we never spend extraction effort on off-cell papers.
- The two-nested-set design (§4.1) keeps a defensible economically-meaningful primary estimate without
  throwing away studies that can only support the standardized pool — the same "sharp definition beats
  more papers" logic that drove the estimand gate.

---

## 8. Decisions for Shravan before implementation

1. **[CONFIRM] Target parameter** (§4.1): primary = semi-elasticity of fertility w.r.t. pension
   wealth? And the common metric for the broad pool = partial correlation *r*?
2. **[CONFIRM] Two nested sets** (primary + standardized) vs a single strict pool.
3. **Scope:** run the fine filter on the OAS pool now (after your RA gate), or design-only until the
   pool is finalized?
