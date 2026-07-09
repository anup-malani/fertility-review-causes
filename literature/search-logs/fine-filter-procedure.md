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

### 4.1 Two nested sets — CONFIRMED 2026-07-09 (Shravan)

Not one metric but **two sets**, split by what each study can support, and mapped to the two verdicts
the review owes every hypothesis:

- **Causal set (inner) → causal-credibility (GRADE).** Studies that credibly identify OAS → fertility.
  Parameter of interest = the **identified effect on fertility itself** (a level change in TFR /
  completed fertility / births), *not* a semi-elasticity. Because the ~10 reform studies and the
  wealth studies express treatment on different scales, the causal set is pooled in **sub-groups by
  treatment type** (reform, pension-wealth, eligibility, …), reported side by side — no forced
  conversion to a single grand mean.
- **R² set (outer) → demographic-significance.** All extractable studies, reporting the **partial R² /
  partial correlation** — the share of fertility variance the OAS measure explains once controls are
  in. Recoverable from almost any regression's t-stat + df, so the 28 observational studies are usable.

**Nesting:** causal ⊆ R². Every causal study yields an association too, so it appears in **both** — its
identified effect in the inner forest plot, its explained-variance in the outer table. Association-only
studies (no clean identification) sit in the outer set alone.

**Two asymmetries, kept honest:**
- The **causal set gets a real pooled estimate** (random-effects, by treatment-type subgroup). The
  **R² set does NOT pool** the same way — it is synthesized **descriptively** (a tabulated distribution
  of explanatory power across studies), not averaged into one number.
- **Partial R² is the *extracted* quantity** for the outer set. **Share of the actual fertility decline
  attributable to OAS** — the most demographically meaningful number — is *derived downstream*
  (effect-size × change-in-OAS-exposure), **not** an extraction target, because studies rarely report it.

### 4.2 What "extractable" requires — two records per study

The extraction pulls **up to two records** from each study: a **causal-effect record** (only if the
study credibly identifies the effect) and an **R² record** (if any regression on fertility is reported).

**Causal-effect record** passes if, for the target relationship, we can obtain **all** of:

| Field | Requirement |
|---|---|
| point estimate | signed level effect on the fertility outcome |
| uncertainty | SE, CI, or t / (p + df) — enough to weight the study |
| treatment definition + **type** | what varied, in what units, tagged: reform / pension-wealth / eligibility / coverage / other (sets the subgroup) |
| outcome definition + units | TFR, births, parity, completed fertility, etc. |
| sample | N, population, setting, period |
| identification | the design that makes it causal (DiD, RD, IV, natural experiment) |
| **reported_magnitude** | the authors' own demographic-magnitude statement if any ("0.65 fewer children", "~10% of the decline") — feeds the derived attributable share (§4.4) |

**R² record** passes if the study reports a regression of a fertility outcome on the OAS measure with
enough to recover a **partial R² / partial correlation** (coefficient + t or SE + df, or a reported
R²/ΔR²). This is a lower bar, so most of the 28 observational studies clear it.

Miss the causal record but clear the R² record → the study is **R²-set only**. Miss both irrecoverably
→ routed to **narrative synthesis**, recorded, not pooled. Passing the estimand gate but failing
extraction is expected and fine; it is a real, reported outcome.

### 4.3 Operationalization (calibrated, like the estimand gate)

1. **Extraction pass (Sonnet over full text + results tables).** Emits, per study, up to two structured
   records (§4.2) each with `can_extract` (bool) + `confidence` + the **raw quoted table/sentence** the
   number came from (auditability), plus the causal record's `treatment_type` subgroup tag. Full text is
   required — **abstracts are insufficient for extraction**; this raises the PDF-coverage bar (see §5).
2. **Calibrate against an RA-extracted gold subset.** Hand-extract ~15–20 of the confirmed pool, then
   score the LLM on (i) the `can_extract` decision (precision/recall/κ, as with the estimand gate's
   κ≈0.86) and (ii) numeric agreement on the extracted estimate and SE. Report the calibration before
   trusting the automated extraction.
3. **RA verifies every pooled number.** Extraction errors corrupt the estimate directly, so the RA
   confirms the point estimate + uncertainty for each study that enters the pool (the auditable quote
   makes this fast). This is the human gate for stage 2, analogous to the estimand RA gate.

**Two hygiene guards learned on the pilot (2026-07-09):**
- *Existence check must hit doi.org, not Crossref.* DataCite DOIs (SSRN 10.2139, EconStor 10.4419,
  university theses 10.25549/10.7907) 404 on the Crossref API but resolve fine — a Crossref-only check
  false-flags live papers as absent (the recurring "couldn't confirm ≠ confirmed negative" trap). Check
  the DOI resolver.
- *PDF-text quality must be screened before extraction.* Some PDFs embed custom-encoded fonts with no
  ToUnicode map; pymupdf then returns constant-offset gibberish. Screen by common-English-word ratio
  (clean ≈ 0.30, corrupt < 0.10) and route corrupt files to re-acquisition/OCR — never feed gibberish
  to the extractor (step 56a `looks_corrupt`).

### 4.4 Demographic significance — the derived attributable share (CONFIRMED 2026-07-09)

Partial R² is **not** the demographic-significance measure: at micro-panel N (10⁶) it collapses to ~0
even for a precisely-estimated effect, so it tracks statistical precision, not explanatory magnitude.
Significance is instead a **derived** quantity:

> **attributable decline = (per-unit causal effect) × (actual change in OAS exposure)**,
> **share = attributable decline ÷ total observed fertility decline**, over the setting/period.

- Ingredient 1 (per-unit effect) comes from the **causal set**. Ingredients 2–3 (OAS-exposure change,
  total fertility decline) are **external macro facts** (ILO World Social Protection coverage/spending;
  HFD/WPP TFR series; pension-introduction dates for the historical FDT cases) — not in the study.
- **Anchor with `reported_magnitude`:** many papers already state their own counterfactual (Namibia
  "0.65 fewer children" / "3 children over 25 yrs"; Brazil "~1.3 fewer / ~10% decline"; China "0.119
  fewer"). Extract it; use it to sanity-check our reconstruction.
- **Two altitudes.** The **per-setting share** (how much of *that* setting's decline OAS explains) is
  the solid primitive — effect valid in its own setting, data exist. The **per-transition verdict**
  (FDT / SDT / pre-modern — what the review owes) is a **bounded synthesis** on top: reason from the
  setting-level shares + how far/fast OAS actually expanded in that transition; report a range ("X–Y%
  where OAS expanded substantially; negligible where it didn't"), **never** a mechanical average of one
  country's coefficient extrapolated worldwide.
- **The R² set is demoted** from "the significance verdict" to an **associational corroboration layer** —
  its real job is housing the ~28 observational-only studies that can't enter the causal set, showing
  whether a fertility~OAS association appears and its sign. The significance number comes from the
  derived shares, not partial R².
- **External input flagged:** the OAS-exposure-over-time dataset is real assembly work; **deferred**
  until all 40 effects are extracted, so we build coverage series only for the settings we actually have.

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
in-cell set (RA-signed, step 52; the 40-study confirmed pool)
  → 53  resolve W-IDs → DOIs + study-level dedup   (reuse 26/26c corrected-maps; FREE, no OpenAlex)
  → 54  existence re-affirm                         (reuse 44/48 three-state verifier)
  → 55  PDF coverage reconcile                      (reuse 27/28/30; flag extraction-blocked)
  → 56  extraction pass (Sonnet)                    two records/study + can_extract + auditable quote
  → 57  calibrate vs RA gold subset                 (κ on can_extract + numeric agreement)
  → 58  RA verify pooled numbers                    (human gate)
  → 59  assemble the two sets                       causal (by treatment subgroup) + R² (descriptive)
```

**Outputs:** `{slug}-causal-set.json/.md` (identified effects on fertility, tagged by treatment type,
+ provenance quote per number), `{slug}-r2-set.json/.md` (partial-R² table, descriptive), `{slug}-
extraction-calibration.md` (LLM-vs-RA), `{slug}-narrative-only.md` (in-cell, neither record extractable),
`{slug}-extraction-blocked.md` (no full text).

---

## 7. Honest scope notes

- For **this pilot**, jobs 1–2 are largely done upstream; the live new work is §4 (extractability)
  + §5 (PDF coverage). The procedure is written **general** so it drops onto any future chapter's
  coarse output unchanged.
- Extractability is deliberately *downstream* of the estimand gate: we only try to extract numbers from
  papers already confirmed in-cell, so we never spend extraction effort on off-cell papers.
- The two-nested-set design (§4.1) splits the pool along the two verdicts the review owes each
  hypothesis — causal set → causal-credibility, R² set → demographic-significance — so the fine filter's
  output feeds both halves of the chapter directly, not just a forest plot.

---

## 8. Decisions — RESOLVED 2026-07-09 (Shravan)

1. **Target parameter:** causal set = **identified effect on fertility** (level, TFR/completed
   fertility/births), pooled by **treatment-type subgroup**; outer set = **partial R²**. Share-of-decline
   is derived downstream, not extracted.
2. **Structure:** **two nested sets** (causal ⊆ R²). Causal set = random-effects meta-analysis; R² set =
   descriptive synthesis (no single pooled R²).
3. **Scope:** run on the 40-study OAS pool now — start with the decision-independent steps 53–55 while
   building the extraction gate (56).
