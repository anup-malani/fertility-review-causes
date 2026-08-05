# Blinded title/abstract screening rubric — D.1.a postmaterialism, individualism, secularization

**Hypothesis:** `postmaterialism-individualism-secularization`, HYPOTHESES-v5.md §D.1.a
**Ticket:** TICK-062 · **Scope:** `{slug}-search-scope.md` (authoritative; this rubric operationalizes it)
**Applies to:** the C1 live corpus (`{slug}-live-corpus.json`) and any later screening batch

---

## The review question, in one test

**A hypothesis is a treatment × outcome pair.** Mediators and mechanisms do not define it and do not
route a paper. Routing is therefore two questions and nothing else:

1. **Is the regressor a measured value orientation** of the content D.1.a specifies — postmaterialism,
   individualism/autonomy/kinship intensity, religiosity/secularity, the childlessness norm, or
   consumption orientation?
2. **Is the dependent variable fertility?**

Both yes → this chapter. Either no → route out by the **treatment** the paper actually uses.

**D.1.a owns the estimate even when the fitted effect plainly travels through contraceptive use,
marriage timing, or migration.** A paper is not routed away because its mechanism belongs to another
chapter; it is routed away because its *treatment* does. Conversely, a study framed in the language of
culture but identified off income, media exposure, or gender attitudes is not this chapter's however
cultural its framing.

Judge **only** the supplied title and abstract. Discovery channel, anchor status, cluster provenance
and citation counts are deliberately withheld — the screen is semantically blind so that recall
measured against the gold stays honest.

---

## ⚠ WHAT THIS SCREEN CANNOT DECIDE, AND MUST NOT PRETEND TO

Three of the scope's routing tests turn on the **item content of the treatment instrument**, which a
title and abstract almost never state. This is the standing lesson from D.3.b, whose screen was asked
to enforce a measure-content wall that was invisible at title/abstract and produced confident verdicts
it had no basis for.

| Rule | What it needs | Visible in an abstract? |
|---|---|---|
| **Ruling 2** — degenerate pair: does the value measure's item content refer to children or family size? | the scale's items | **almost never** |
| **Wall 5** — epidemiological designs: is the ancestral proxy a *fertility rate* or a *value measure*? | the proxy's definition | **sometimes**, often not |
| **Ruling 3** — design tier: what exactly generates variation in the treatment? | the identification section | **partially** |

**When a paper is plausibly in scope but the deciding fact is not on the page, return `UNCERTAIN`
with `needs_full_text` naming the missing fact.** Do not guess, and do not resolve toward
`NOT_RELEVANT` because the abstract is thin. An `UNCERTAIN` costs one full-text read; a wrong
`NOT_RELEVANT` costs the study.

**Named exception, binding:** **Fernández and Fogli 2009** (`10.1257/mac.1.1.146`) and any other
epidemiological/ancestral-culture design **must be read at full text before assignment and must never
be routed from the abstract.** Wall 5 turns entirely on proxy content and this design is claimed by
both D.1.a and A.19.

### Title-only records default to `UNCERTAIN`, never to `NOT_RELEVANT`

**31%** of the C1 corpus carries no abstract (measured below; the Tier-B gold frame runs worse at
50%), and **the missing abstracts are not missing at random**:
providers hold them for well-indexed Anglo-European journals and not for the book chapters, regional
journals, dissertations and non-English work that this chapter has now hit an indexing gap on four
separate times. Screening title-only records as `NOT_RELEVANT` would compound the geographic skew the
scope already lists as a limitation. A title-only record that is plausibly on-pair is `UNCERTAIN` with
`needs_full_text: "no abstract available"`.

---

## Required output

One JSON array, input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "see the cell list below",
  "pair": "S1 | S2 | S3 | S4 | S5 | MULTIPLE | NA",
  "treatment": "the regressor, short phrase, as the abstract states it",
  "outcome": "the dependent variable, short phrase",
  "outcome_is_fertility": "yes | no | unclear",
  "treatment_is_measured_value": "yes | no | unclear",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | descriptive | other",
  "design_tier_guess": "1 | 2 | 3 | 4 | unclear",
  "needs_full_text": "the missing fact, or empty string",
  "reason": "one concise clause grounded only in the title and abstract"
}
```

`treatment_is_measured_value` and `outcome_is_fertility` are the two routing questions recorded
separately from the verdict, so a disagreement can be traced to which question was answered wrong.

---

## Verdict rules

- **`RELEVANT`** — the regressor is a measured value orientation of D.1.a content **and** the
  dependent variable is fertility (realized births, completed fertility, parity, childlessness, or a
  stated intention / ideal family size).
- **`UNCERTAIN`** — plausibly on-pair, but the deciding fact is not on the page. Always populate
  `needs_full_text`. Use this for: no abstract; the value measure named but its items not described
  and Ruling 2 could bite; an ancestral-culture proxy whose content is unstated; "cultural factors"
  asserted without saying what was measured.
- **`NOT_RELEVANT`** — the treatment is something other than a measured value, or the outcome is not
  fertility. Route by naming the correct cell; do not simply reject.

**A paper is not RELEVANT merely for being about fertility decline, about religion, or about the
Second Demographic Transition.** The SDT literature routinely reports value change, gender attitudes
and partnership behaviour as one bundle; the treatment decides.

---

## Estimand cells

Copy the cell name exactly. Full definitions in the scope; the routing column is the treatment.

**Primary — in the causal pool**

| Cell | Route when the treatment is |
|---|---|
| `PRIMARY_POSTMATERIAL_S1` | postmaterialist / self-expression / survival-values measure |
| `PRIMARY_INDIVIDUALISM_S2` | individualism, autonomy, collectivism, kinship-intensity measure |
| `PRIMARY_SECULAR_S3` | religiosity, affiliation, attendance, salience, denomination |
| `PRIMARY_SECULAR_SHOCK_S3` | the same, moved by an exogenous shock — the Tier-1 stratum |
| `PRIMARY_CONSUMERISM_S5` | consumption orientation or material-values scale |
| `PRIMARY_VALUE_EX_ANTE` | any admissible value measure recorded **before** the outcome on childless respondents |
| `NORM_ENVIRONMENT_LEVEL` | a community / cohort / leave-one-out norm, i.e. the norm itself rather than exposure to it |
| `MIXED_CULTURE_PROXY` | ancestral fertility **and** ancestral values jointly — flag, report to A.19 too |

**Reported but not pooled**

| Cell | Route when |
|---|---|
| `NORM_ACCEPTABILITY_DESCRIPTIVE` | own attitude toward childbearing/childlessness/ideal family size → own fertility. **Degenerate under Ruling 2**: one construct measured twice. Descriptive only. |
| `AGGREGATE_COMOVEMENT` | country/region value index → aggregate TFR. Tier 4, never pooled. |
| `SDT_FRAMEWORK_THEORY` | framework statement, elaboration or critique with no estimate |
| `VALUE_CONSTRUCT` | a value measure as the **dependent** variable — scale validation, prevalence, determinants of secularization |

**Route out — name the neighbour**

| Cell | Treatment that belongs to the neighbour |
|---|---|
| `OFF_EXPOSURE_D1b` | exposure to an external modernity package: media reach, missionary contact, migrant return flows |
| `OFF_STATUS_D1c` | a prestige or status gradient in transmission — who imitates whom |
| `OFF_GENDER_D2a` | gender-role attitudes, women's decision-making authority, gender-equity indices |
| `OFF_PARTNERSHIP_D2b` | cohabitation, divorce liberalization, union deinstitutionalization, kinship structure |
| `OFF_PARENTING_D2d` | a parenting-standard measure |
| `OFF_ANCESTRAL_FERTILITY_A19` | ancestral-country **fertility rate** as the proxy |
| `OFF_CONTRACEPTIVE_ATTITUDE_A3_A6` | birth-control information, legitimation, or contraception-specific stigma |
| `OFF_CHANNEL_A20` | media, network or linguistic-boundary **exposure** |
| `OFF_INCOME_SECURITY` | income, growth, affluence, unemployment, job insecurity — Wall 7 |
| `OFF_ECOLOGICAL_FEAR_D3b` | measured ecological fear or eco-ethical concern (D.3.b owns it; a general value orientation with no fear content is D.1.a) |
| `OFF_OUTCOME` | an admissible value measure but the outcome is **not** fertility — contraceptive use, marriage, wellbeing, voting. Mechanism/context only. |
| `OFF_OTHER` | some other fertility determinant with no sibling home |
| `REVERSE` | parenthood or fertility status → values, religiosity, attendance. Context, and it measures the binding risk-of-bias threat. |
| `INSUFFICIENT_INFO` | not determinable on the visible record — pairs **only** with `UNCERTAIN` |

---

## The boundaries that will actually be tested

Ordered by how often they will come up, not by how interesting they are.

1. **D.2.a / D.2.b, the SDT bundle (constant).** *Gender-role attitudes* are D.2.a. *Cohabitation,
   divorce, union deinstitutionalization* are D.2.b — these are **behaviours, not held values**, and
   they stay D.2.b's even when the paper labels them SDT indicators. A general value orientation that
   is not gender-specific is D.1.a's.
2. **Wall 7, measured versus narrated (frequent).** A study identified off income, growth or
   unemployment, with value change narrated but never measured, has income as its treatment →
   `OFF_INCOME_SECURITY`. The test is what is in the regression, not what is in the discussion.
3. **Ruling 2, the degenerate pair (frequent, and usually invisible).** Own approval of childlessness
   regressed on own childlessness is one variable measured twice.
   → `NORM_ACCEPTABILITY_DESCRIPTIVE` when clear, `UNCERTAIN` when the items are not described.
4. **Wall 2, exposure versus value held (moderate).** Setting is a strong prior and never decides
   alone: *measured* secularity in contemporary South Korea is D.1.a; *exposure* of rural Nepal to
   Western family ideals is D.1.b.
5. **Wall 5, proxy content (rare, high stakes).** Ancestral **fertility rate** → A.19. Ancestral
   **value measure** → D.1.a. Both → `MIXED_CULTURE_PROXY`. Never decided from an abstract.

---

## The clinical and veterinary collision — reject on sight

The outcome vocabulary collides head-on with clinical medicine, and this surfaced in three separate
probe designs. *Fertility* reads as IVF, *birth* as birth weight, *reproduction* as livestock
breeding, and OpenAlex stemming matched *individualism* to "individualiSED dosing of follitropin
delta". The top-cited hit across three pairs was a systematic review of antenatal care.

`NOT_RELEVANT` / `OFF_OTHER` on sight: IVF and assisted reproduction, infertility treatment, oocyte
and sperm biology, antenatal and obstetric care, birth weight and preterm birth, maternal mortality,
contraceptive **method** efficacy trials, and all animal or livestock reproduction. **A human
demographic outcome is required.**

Two near-misses that are **not** collisions and must be kept:
- *social reproduction* / *reproductive health services* — reject on outcome grounds, but read first;
  a paper on religiosity and reproductive-health **service use** is `OFF_OUTCOME`, not junk.
- *secular trend* — a demography term of art meaning a long-run trend with **no religious content**.
  It is not an S3 paper.

---

## What the screen does NOT do

Recorded so a screener does not attempt them and an RA does not expect them:

- **The sign convention (Ruling 5).** Orienting every effect toward the secular/postmaterialist pole
  is an extraction task; the screen records the treatment as stated.
- **Design tier assignment (Ruling 3).** `design_tier_guess` is a hint for triage, not a rating. The
  tier is fixed at extraction with the source of variation named.
- **Pair pooling.** The five pairs are never combined; the screen tags `pair` so the pools stay
  separate downstream, and `MULTIPLE` is legitimate when a paper carries several treatments.
- **Demographic significance and GRADE.** Later stages entirely.

---

## Calibration expectations

Set from the cold-start anchors and the A6a term mining, so a screen returning a very different shape
is a signal to check the screen rather than to accept the shape.

- **S3 dominates.** 23 of 31 empirical anchors are S3, against 5 S1, 2 S5, 1 S2. A6a found S3 carries
  44 discriminative terms; S4 and S5 have **zero**.
- **Tier 1 is three studies.** The design probe found exactly three credible natural experiments, all
  S3, all since 2018. Blue-law, Sunday-trading and clergy-scandal shock families are **empty**, and
  state-atheism campaigns have never been used to identify a fertility effect. A screen returning many
  Tier-1 candidates has almost certainly mistaken an observational study for one.
- **Three-quarters of the anchor set supports nothing above Very Low.** Anchors run Tier 1: 3,
  Tier 2: 6, Tier 3: 21, Tier 4: 1. Expect the same shape here.
- **`AGGREGATE_COMOVEMENT` will be common and is worth almost nothing.** Country value index against
  TFR is the canonical SDT evidence base and sits at Tier 4 with no causal weight.

---

## Corpus calibration — measured on the C1 pull, not assumed

Profiled on the 11,425 records retrieved so far. **The pull is incomplete** (`GENERIC_VALUES` at
5,000 of 11,228), so these proportions will shift as the remainder lands; the *shapes* will not.

| | count | share |
|---|---|---|
| records | 11,425 | |
| carry an abstract | 7,842 | 69% |
| **title only → default `UNCERTAIN`** | **3,583** | **31%** |
| clinical / veterinary collision on title | ~856 | 7.5% |
| book reviews (reject: `OFF_OTHER`) | 262 | 2% |
| book chapters + dissertations (keep) | 1,131 | 10% |

Languages: 10,543 English, then Indonesian 173, French 107, Portuguese 41, Czech 33, Japanese 22,
Spanish 21, and 364 untagged. The non-English tail is small but real, and it is the material Ruling 4
was written to admit — do not reject a record for being non-English.

### The collision is concentrated, and one obvious fix would be a disaster

Of ~856 clinical hits, **545 (64%) came in through `GENERIC_VALUES`**, against 164 from S2, 113 from
S3, and single digits from S1. The mechanism is visible in the titles: *"The **value** of cervical
length changes for the prediction of preterm **birth**"* — the generic treatment term `value` meeting
the outcome term `birth` inside a clinical idiom.

**The tempting fix — excluding the phrase "value of" — must not be applied.** It matches 379 records
in this corpus and only **118** of them are clinical. The rest are **"Value of Children"**: *Changing
Value of Children and Fertility Transition in Turkey*, *Determinants of family size: sex-role
orientation and value of children*. That is the Value-of-Children literature, which is squarely
on-pair S1/S5 material and is some of the most useful evidence this chapter has.

Exclude on clinical **content** terms — `cervical`, `preterm`, `neonatal`, `ultrasound`, `gestational`,
`oocyte`, `IVF`, `livestock` — **never on the `value of` phrasing.** This is the third time on this
chapter that a fix aimed at a false-positive class would have manufactured a worse false-negative
class; the pattern is now expected rather than surprising, and any proposed exclusion gets a rejected
sample read before it ships.

### What this implies for screening cost

A 31% title-only rate means roughly a third of the corpus arrives at `UNCERTAIN` by construction, and
those are disproportionately the book chapters, dissertations, regional and non-English records that
the indexing gap already thins. That is the correct outcome — the alternative silently deletes exactly
the material the chapter is weakest on — but it should be **budgeted for at the full-text stage rather
than discovered there**, and it is the strongest argument for running the cheap clinical pre-filter
above before the screen rather than paying an LLM to read 856 obstetrics abstracts.
