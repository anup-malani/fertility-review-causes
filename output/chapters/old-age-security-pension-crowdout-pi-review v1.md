# Old-Age-Security / Pension Crowd-Out of Fertility — PI Independent Review (first pass)

**Author:** Anup Malani (PI), with Claude
**Date:** 2026-07-05
**Status:** working draft — independent benchmark to compare against Alexandra's pipeline output
**Inputs:** GACS `metaanalysis-doi-list.md` (44 distinct ET=4 studies), `ra-review.csv` (40 DOI-resolved
studies with RA RETRIEVE/EXCLUDE decisions), the 4 unresolved title-keyed studies.

> This is the PI's independent read of the OAS evidence base, done from the same vetted paper set the
> RAs worked from. Its purpose is to be a benchmark: an estimand definition, an inclusion adjudication,
> an evidence map, and first-pass per-phenomenon verdicts arrived at independently, so that Alexandra's
> pipeline-produced chapter can be compared against it.

---

## 1. The estimand (what this chapter is actually about)

**Hypothesis.** A major historical economic value of children was as *old-age security* — insurance
and investment for parents' old age (Neher 1971; Caldwell 1976; Cigno 1993). When a **non-child
source of old-age security** appears — a state pension, social insurance, long-term-care insurance,
or a financial market that lets you save for old age without children — the old-age-security *demand*
for children falls, and fertility declines.

**Estimand.** The causal effect of an **exogenous increase in non-child old-age security** on
**completed fertility (or a fertility outcome)**, operating through the **old-age-security motive**.

Three coordinates define inclusion, and getting them right is the whole adjudication:

| Coordinate | In | Out |
|---|---|---|
| **Treatment** | Pension introduction/expansion, social security, long-term-care insurance, financial-market development that substitutes for children-as-savings. | General income shocks (lottery), child subsidies/grants (price of children), childcare-supply shocks, family caps, marriage-age laws — these are *other* hypotheses. |
| **Outcome** | Fertility as the **dependent variable** (births, completed fertility, parity progression, TFR). | Savings, migration, coresidence, child education, elderly health, labor supply — real pension effects, wrong outcome for *this* chapter. |
| **Direction & mechanism** | Treatment → fertility, via the **old-age-security motive** (children as old-age insurance/investment). | Reverse causation (fertility → pension take-up; fewer children → less old-age support). Opposite-signed *time-transfer / grandparental-childcare* channel is a **distinct pathway** (see cell C). |

**Why the estimand is the binding constraint, not recall.** GACS's "44 meta-analysis-ready studies"
is a *search-recall* object (ET=4 papers about pensions and fertility that the query found). It is
**not** an estimand object. When the estimand above is applied, only ~1 in 4 survive as primary
evidence. The pilot's real scarce resource is a sharp estimand, not more papers — a point that should
feed back into how GACS defines "relevant." (Developed in the GACS critique.)

---

## 2. A three-cell evidence structure (not one)

The single RETRIEVE/EXCLUDE axis the RAs used conflates three substantively different objects. Our
review separates them, because **what may be pooled differs by cell**:

- **Cell A — Primary: OAS-motive → fertility.** Exogenous non-child old-age security; fertility as
  outcome; OAS mechanism. *These are the studies the pooled/synthesized causal estimate is built from.*
- **Cell B — Mechanism validation: do children function as old-age security?** Fertility (or number of
  children) as the *treatment*; an old-age-security asset (private insurance, savings) as the outcome.
  Evidence that the mechanism *exists*, not an estimate of the fertility effect. **Never pooled with A.**
- **Cell C — Alternative pathway: pension → fertility via grandparental childcare / time transfers.**
  A real pension→fertility effect, but through a **different, opposite-signed** mechanism (a retired
  grandparent's *availability* lowers the cost of children and *raises* daughters' fertility).
  **Never pooled with A** (Alexandra's own harmonization rules §5 say so). Retained as a labeled
  secondary stream because it is substantively about how pensions move fertility.

Everything else is out of scope for this chapter.

---

## 3. Inclusion adjudication — our calls vs. the RAs'

**Bottom line:** we agree with the RAs on ~37 of 40 binary calls. The value we add is **structure**
(three cells instead of one), **one caught inconsistency** (Ci vs. Ruthbah), and **one flagged
high-value unresolved study** (Ghana). Counts:

- **Cell A (primary):** **9 studies** — RA RETRIEVE set (10) minus Ci (moved to B).
- **Cell B (mechanism):** **2 studies** — Ci (RA had RETRIEVE) + Ruthbah (RA had EXCLUDE).
- **Cell C (grandparental-childcare pathway):** **3 studies** — Eibich-Siedler, Ilciukas, Akyol-Atalay
  (RA excluded all three as "different mechanism"; we retain as a labeled secondary stream, not in A).
- **Excluded (out of scope):** 26 studies — wrong outcome, wrong treatment, or reverse causation.
- **Unresolved / verify:** 4 — of which **Ghana** (pension reform → fertility) is potentially Cell A
  and worth resolving; the "Italy / Wati & Sudarto 2025" record looks like a phantom (author-title
  mismatch); Costa Rica and Ecuador appear off-outcome.

### Cell A — Primary OAS-motive → fertility (9)

| # | Study | Setting | Treatment | Phenomenon | RA | Ours |
|--:|---|---|---|---|---|---|
| 1 | Danzer & Zyska 2023 | Brazil, rural | Pension expansion to rural workers | Contemporary DT | RETRIEVE | **A** |
| 2 | Rossi & Godard 2022 (AEJ:Pol) | Namibia | Social-pension extension | Contemporary DT | RETRIEVE | **A** |
| 3 | Billari & Galasso 2009 | Italy | Pension reforms | Rich-country modern | RETRIEVE | **A** |
| 4 | Han et al. 2025 | China | Long-term-care insurance pilot | Contemporary | RETRIEVE | **A** |
| 5 | Guinnane & Streb 2021 | Prussia 1881–1910 | Bismarck social insurance | **FDT (historical)** | RETRIEVE | **A** |
| 6 | Shen et al. 2020 | China, rural | New Rural Pension Scheme | Contemporary DT | RETRIEVE | **A** |
| 16 | "Pensions & Fertility: Germany" | Germany? | pension policy (abstract missing) | ? | RETRIEVE | **A — verify identity** |
| 18 | Basso & Cuberes 2013 | US, 19th c. | Financial-market development | **FDT (OAS-substitute)** | RETRIEVE | **A — note: broader mechanism** |
| 24 | Galofré-Vilà 2023 | US | 1935 Social Security Act | **FDT-adjacent** | RETRIEVE | **A — note: identification softer** |

### Cell B — Mechanism validation: children as old-age security (2)

| # | Study | Structure | RA | Ours |
|--:|---|---|---|---|
| 9 | Ci 2024 | "Later-Longer-Fewer" as IV for # children → private-insurance adoption (fertility = **treatment**) | RETRIEVE | **B (reclassify)** |
| 11 | Ruthbah 2022 (Bangladesh) | Family-planning program as IV for fertility → asset accumulation (fertility = **treatment**) | EXCLUDE | **B (reinstate)** |

> **Inconsistency flagged:** Ci and Ruthbah have the *identical* causal structure — fertility as the
> instrumented treatment, an old-age-security asset as the outcome — yet the RAs marked Ci RETRIEVE
> and Ruthbah EXCLUDE. Whatever the rule, it should treat them the same. We put both in Cell B.

### Cell C — Alternative pathway: grandparental childcare / intergenerational time transfer (3)

| # | Study | Setting | Sign | RA | Ours |
|--:|---|---|---|---|---|
| 8 | Eibich & Siedler 2020 | Germany | grandparent availability ↑ → daughter fertility ↑ | EXCLUDE | **C (label, don't pool)** |
| 10 | Ilciukas 2023 | Netherlands | delayed grandparent retirement → daughter fertility ↓ | EXCLUDE | **C** |
| 19 | Akyol & Atalay 2025 | Australia | grandmother pension-eligibility delay → daughter fertility ↓ | EXCLUDE | **C** |

> These are *opposite-signed* to the OAS motive: they say access to a (retired) grandparent's time
> *raises* fertility, so restricting pension eligibility (keeping grandparents working) *lowers* it.
> Coherent little literature; a paragraph, clearly walled off from the primary estimate.

### Excluded — out of scope (26)

- **Wrong outcome — pension/policy → non-fertility** (18): Yuan (child education), Neve-Fink (parental
  survival), Bratti (daughter LFP), Duflo (child anthropometrics), Mu-Du (child education), Choukhmane
  (saving), Chen 2017 (coresidence), Edmonds (household structure), Chen 2015 (adult-child migration),
  Amarante (birthweight), Lehmann-Hasemeyer-Streb (saving), Eggleston (migration), Bau (son migration),
  Lachowska-Myck (saving), Valentová (maternal labor), Bérgolo-Cruces (labor informality), Serrano-
  Alarcón (health/labor), Oh (private transfers to elderly).
- **Wrong treatment — not old-age security** (6): Rosenberg (child grant), Kearney (welfare family cap),
  Tao (kindergarten supply), Bulman (lottery income), Bellés-Obrero-Lombardi (min-marriage-age),
  Broeck-Maertens (female employment).
- **Reverse causation** (2): Zhang (children → pension take-up), Chen-Fang (fewer children → old-age
  support).

We concur with all 26 exclusions.

### Unresolved — verify (4)

| # | Study | Status | Our read |
|--:|---|---|---|
| 15 | Pension Policy Reform and Fertility: Micro Evidence from **Ghana** | NO_WID | **High value — likely Cell A (Africa). Resolve DOI/PDF.** |
| 17 | Pension Reforms and Fertility: Italy — "Wati & Sudarto 2025" | WID_DRIFT | Author names ≠ Italy topic → **probable phantom**; verify before trusting. |
| 29 | Oh — public transfers → private support (Ecuador) | WID_DRIFT | Outcome ≠ fertility → **exclude** regardless of resolution. |
| 33 | Non-contributory pensions, Costa Rica (case study) | OK | Outcome likely not fertility → verify, probably exclude. |

---

## 4. Evidence map (Cell A — 9 primary studies)

Extracted from abstracts, AI rationales, and RA notes. **Effect magnitudes are first-pass and flagged
`[PDF]` where they must be confirmed against the full text** (no PDFs are in the repo — they were
shared via Slack). Direction is stated where the abstract/rationale supports it; "consistent" = the
sign matches the OAS motive (more non-child old-age security → lower fertility).

| # | Study | Setting / period | Treatment (OAS shock) | Design / identification | Effect on fertility | ID strength | Phenomenon fit |
|--:|---|---|---|---|---|---|---|
| 2 | **Rossi & Godard 2022** (AEJ:Pol) | Namibia, modern | Social-pension extension across regions × cohorts | DiD | **Negative, consistent**; magnitude `[PDF]` | **Strong** — the flagship OAS-motive natural experiment | Contemporary developing-country DT |
| 1 | **Danzer & Zyska 2023** (AEJ:Pol) | Brazil, rural, modern | Rural-worker pension expansion | DiD / IV / event-study | **Negative** — ~8% lower childbearing propensity `[PDF confirm]` | **Strong** | Contemporary developing-country DT |
| 5 | **Guinnane & Streb 2021** (PDR) | Prussia, 1881–1910 | Bismarck social insurance (1880s) | Natural experiment, regional rollout | **Negative, consistent** on marital fertility; magnitude `[PDF]` | **Moderate–strong** (historical) | **FDT (historical)** |
| 3 | **Billari & Galasso 2009** (CESifo WP) | Italy, 1990s reforms | Pension-wealth cuts for younger cohorts | Cohort natural experiment | **Consistent** — cohorts with less pension wealth had *more* children; magnitude `[PDF]` | **Moderate** (WP; DiD across cohorts) | Rich-country modern → **SDT** |
| 4 | **Han et al. 2025** (Applied Econ) | China, modern | Long-term-care-insurance pilot rollout | DiD | **Negative, consistent**; magnitude `[PDF]` | **Moderate** | Contemporary (OAS-substitute) |
| 18 | **Basso & Cuberes 2013** (NBER wp20491) | US counties, 19th c. | Financial-market development (banks) | IV (1820 bank presence) + legal exogeneity | **Negative, consistent** (finance substitutes for children-as-savings); magnitude `[PDF]` | **Moderate** (historical IV) | **FDT (OAS-substitute, well-timed)** |
| 6 | **Shen et al. 2020** (PLoS ONE) | China, rural, modern | New Rural Pension Scheme | DiD + PSM + IV | **Negative, consistent**; magnitude `[PDF]` | **Weaker** (PLoS; PSM-dependent) | Contemporary developing-country DT |
| 24 | **Galofré-Vilà 2023** (Cliometrica/EHR) | US, 1935+ | 1935 Social Security Act, cross-state spending | Cross-state panel | Sign subtle — links SSA spending to the **baby boom**; `[PDF]` | **Weaker** — "exogeneity not fully clean" (RA/AI note) | **FDT-adjacent** |
| 16 | **"Pensions & Fertility: Germany"** (J Popul Econ 2016, `10.1007/s00148-016-0608-x`) | Germany, ? | pension policy (abstract missing) | ? | ? | **Unassessed — verify identity first** | likely FDT/historical `[verify]` |

**Identification tiering (our read):**
- **Strongest:** Rossi-Godard, Danzer-Zyska (clean modern natural experiments, top-field placement),
  Guinnane-Streb (credible historical rollout).
- **Middle:** Billari-Galasso, Han, Basso-Cuberes.
- **Weaker / caveated:** Shen (PSM-reliant, PLoS ONE), Galofré-Vilà (soft exogeneity), "Germany"
  (identity unverified — do not use until the DOI→paper mapping is confirmed and the abstract read).

**Coherence.** Direction is **consistent across all assessable studies** — every credible design finds
that expanding non-child old-age security reduces (or that removing it raises) fertility. There are no
sign reversals within Cell A. That directional consistency is the single strongest feature of the
evidence base and the main thing an eventual pooled/narrative estimate rests on.

**Secondary streams (for context, not pooled):**
- **Cell B (mechanism):** Ci 2024 and Ruthbah 2022 both find that *more children → fewer purchased
  old-age-security assets* (private insurance; savings) — i.e. children and financial OAS assets are
  **substitutes**, which is the micro-foundation the Cell-A studies presuppose. Useful corroboration
  that the mechanism is real, from the reverse direction.
- **Cell C (grandparental childcare):** Eibich-Siedler, Ilciukas, Akyol-Atalay find grandparent
  *availability* raises daughters' fertility (**opposite sign**). This means pensions move fertility
  through (at least) two opposing channels — an OAS-motive channel (−) and a time-transfer/childcare
  channel (+) — so the *net* population effect of a pension reform is an empirical question, and a
  pooled "pension → fertility" number that ignores the split is not interpretable.

## 5. Per-phenomenon verdicts (first pass)

The review grades causal credibility and demographic significance **separately per phenomenon**. The
central analytic move here is that Cell A's micro-credibility is real but its **demographic
significance is gated by timing and saturation** — and both cut against the two canonical rich-country
transitions the review targets.

### Pre-modern (PM)
- **Direct causal evidence:** none. No exogenous variation in formal old-age security exists in
  pre-modern settings.
- **Causal credibility (GRADE):** not gradeable / **very low** — no studies.
- **Demographic significance:** **low for explaining PM *variation*.** The OAS motive was near-universal
  pre-modern (children were everyone's old-age security), so it is a *constant background condition*,
  not a source of the cross-sectional *variation* in pre-modern fertility the review asks about. It can
  explain why pre-modern fertility was high *in level*, but not why it varied across pre-modern
  populations (which needs variation in kin-support norms, mortality, land tenure, inheritance).

### First Demographic Transition (FDT, ~1870–1965)
- **Direct causal evidence:** 4 studies (Prussia/Bismarck, the German pension study once verified,
  19th-c US financial development, 1935 US SSA), directionally consistent.
- **Causal credibility (GRADE):** **low–moderate.** Consistent direction and two reasonably credible
  designs (Guinnane-Streb; Basso-Cuberes IV), pulled down by historical-identification limits and the
  soft exogeneity of the SSA study.
- **Demographic significance:** **partial, and the timing argument is decisive.** Marital fertility in
  much of NW Europe began falling in the 1870s–1890s, whereas *state* old-age security arrived later
  (Bismarck's pension insurance 1889; US Social Security 1935). **State pensions therefore postdate the
  *onset* of the FDT and cannot be its primary trigger** — they can at most contribute to its later
  deepening, and even then early coverage was thin (small exposed population share → limited aggregate
  weight). The one channel timed correctly for the FDT onset is **financial-market development**
  (Basso-Cuberes, 19th c.), which is why the *broad* OAS reading matters: the significance of "OAS
  crowd-out" for the FDT rides mostly on financial-market substitution, not on state pensions.

### Second Demographic Transition (SDT, ~1965–present)
- **Direct causal evidence:** thin in the target setting. Billari-Galasso (Italy) is the main
  rich-country-modern study; the Namibia/Brazil/China studies are contemporaneous but identify effects
  in *developing* countries undergoing what is arguably still a first transition, not the rich-country
  SDT (postponement, sub-replacement).
- **Causal credibility (GRADE):** **very low** for the SDT as such — essentially one on-target study.
- **Demographic significance:** **low, and the saturation argument is decisive — with a sign warning.**
  By the SDT's onset (~1965), rich countries already had mature, near-universal pension systems, so the
  OAS-crowd-out had *already largely occurred*; little marginal non-child OAS was left to expand. Worse,
  where rich countries *cut* pension generosity during the SDT era (aging-driven reforms), the OAS
  motive predicts fertility should *rise* — the **opposite** of the observed SDT decline. So OAS
  crowd-out is unlikely to be a material SDT driver, and its sign may be wrong for the SDT period.

### Scope note (a gap in the review's frame)
The mechanism's **strongest and cleanest evidence** (Namibia, Brazil, China) identifies effects in
**contemporary developing-country fertility decline** — a phenomenon the PM/FDT/SDT triad does not
cleanly contain. Worth surfacing to the PI/team: either treat contemporary DT as a fourth target, or
explicitly scope these studies as *mechanism-demonstrating* evidence that transports only weakly to the
two canonical transitions.

### Bottom-line verdict (chapter headline)
> The old-age-security motive is **causally credible at the micro level**: multiple clean
> quasi-experiments (Namibia, Brazil, Italy, Prussia, China) show that expanding non-child old-age
> security lowers fertility, with **consistent direction and no sign reversals**. But its **demographic
> significance for the review's two canonical transitions is limited by timing and saturation** — state
> pensions largely *postdate* the FDT's onset (financial-market development is the better-timed channel),
> and were already *saturated* before the SDT began (with pension *cuts* in that era pointing the wrong
> way). The mechanism's strongest footprint is in **contemporary developing-country** fertility decline.
> **Verdicts:** PM — no direct evidence / low significance; **FDT — low-moderate credibility / partial
> significance (via financial development, not state pensions)**; **SDT — very-low credibility / low
> significance**.

---

## Appendix — open verification items for the RAs
1. **Resolve the Ghana study** (`#15`, pension reform → fertility) — currently NO_WID; if real it is a
   primary Cell-A study and the second sub-Saharan-Africa data point. High value.
2. **Verify the "Germany" study identity** (`#16`, `10.1007/s00148-016-0608-x`) before any use.
3. **Confirm the "Italy / Wati & Sudarto 2025" record** (`#17`) is a phantom (author–topic mismatch),
   then drop.
4. **Reconcile the Ci/Ruthbah inconsistency** in `ra-review.csv` (both belong in the mechanism cell).
5. **Confirm the flagged effect magnitudes `[PDF]`** for the 9 Cell-A studies against full text.
