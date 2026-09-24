# Blinded title/abstract screening rubric — son preference and gender-biased fertility norms (D.2.c) — v1

## Review question

Does the paper bear on **D.2.c** — the claim that a **cultural preference for sons** sustains higher
fertility through **continued childbearing until a son is born (differential stopping)**, with
**sex-selective abortion partially substituting** for the fertility effect where it is available (the
preference then shows up as a skewed **sex ratio at birth** rather than as extra births)? D.2.c's
parameter is the effect of **son preference (its intensity, or the arrival of sex-selection technology)
on realized fertility — parity progression / differential stopping / completed fertility — and its
attenuation by sex-selective abortion**, holding fixed the sex-indifferent desired number of children.

Judge ONLY the supplied title and abstract. Discovery channel and citation count are intentionally
hidden. Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states the
estimand verbatim (e.g. "Son preference and the sex composition of children"); route such a record
normally but set `identification` to `NA` unless the title also names the design. In every other
abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a substantive
cell for a record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is ALL THREE (PM, FDT, SDT).** Son preference raises natural-fertility family size via
differential stopping in pre-modern and historical/high-fertility settings (PM/FDT), remains a live FDT
driver in South and East Asia, and in the SDT is re-expressed as skewed sex ratios at birth once
sex-selection technology arrives. A historical differential-stopping study is IN scope, not out.

## THE SIX LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs A.10 (Sex Ratio Imbalance and Marriage-Market Effects). LOAD-BEARING.** The word "sex
ratio" appears on both sides; the line is WHICH sex ratio and WHICH direction of causation. D.2.c owns son
preference as a CAUSE — of extra births (stopping) and of a skewed SEX RATIO AT BIRTH (the newborn
cohort). A.10 owns the skewed ADULT sex ratio as an EXPOSURE to the marriage market and its effects on
marriage timing, bargaining, and fertility. A study identifying off an already-skewed ADULT sex ratio
acting on marriage/fertility is `OFF_ADULT_SEX_RATIO`. A study on son preference or sex-selection arrival
with fertility or sex-ratio-at-birth as the outcome stays here.

**Wall 2 — vs A.4/A.2 (Abortion / Contraception).** Sex-selective abortion is the TECHNOLOGY through which
son preference substitutes; A.4 owns the general fertility effect of abortion access (removing unwanted
pregnancies of ANY sex). A study on abortion/contraceptive access -> total births regardless of sex is
`OFF_ABORTION_GENERAL`. A study on sex-SELECTIVE abortion as the expression of son preference — differential
fertility by preference, or the sex ratio at birth — stays here.

**Wall 3 — vs A.8 (Parity-Specific Stopping and Spacing).** A.8 owns deliberate stopping at a target
NUMBER of children (the FDT quantum signature), regardless of sex. A study whose stopping rule is a
total-parity target is `OFF_PARITY_STOPPING`. A study whose stopping rule depends on the SEX composition of
the children already born stays here — the sex-composition interaction is the D.2.c fingerprint.

**Wall 4 — vs C.3.c (Old-Age Security and Pension Crowdout).** One economic ROOT of son preference is that
sons provide old-age support under patrilineal norms. A study identifying off pension or formal
old-age-security variation is `OFF_OLD_AGE_SECURITY`. A study identifying off son-preference intensity stays
here. C.3.c is a root cause and is cited as such, but pension-driven fertility change is not D.2.c evidence.

**Wall 5 — vs D.2.a (Female Empowerment and Gender Equity).** Both are "gender norms." D.2.a owns
egalitarian norms and female autonomy that lower fertility BROADLY; D.2.c owns the specific gender-BIASED
preference for sons that raises it (and skews sex ratios). A study identifying off female
education/autonomy or egalitarian-norm diffusion is `OFF_GENDER_EQUITY`. **Bridge:** a study where rising
female autonomy ERODES son preference and thereby changes fertility/sex ratios is `PRIMARY_NORM_INTENSITY`
(D.2.c), because the outcome of interest is son preference and its effect, with D.2.a only the upstream
force.

**Wall 6 — vs A.1 (Child Mortality Decline, Replacement/Insurance).** Under high mortality, couples
continue until a SURVIVING son, mixing son preference with the replacement response to mortality. A study
identifying off mortality decline is `OFF_CHILD_MORTALITY`. A study identifying off the sex preference,
holding survival fixed or controlling for it, stays here. A design that cannot separate "insuring against
son death" from "wanting a son" is `UNCERTAIN`.

## Estimand cells

- `PRIMARY_DIFFERENTIAL_STOPPING`: sex composition of existing children (daughters-only vs has-son), or
  son-preference intensity -> probability of a further birth / parity progression / completed fertility.
- `PRIMARY_SEXSEL_SUBSTITUTION`: arrival/availability/cost of prenatal sex-selection technology
  (ultrasound, amniocentesis) or a policy change -> fertility AND/OR sex ratio at birth (the substitution).
- `PRIMARY_NORM_INTENSITY`: cross-population/cohort variation in son-preference intensity (desired sex
  composition, DHS ideal-sex items; or its erosion by development/autonomy) -> TFR / completed fertility.
- `MECHANISM_PREFERENCE_ONLY`: documents son-preference levels/trends or its correlates with NO fertility
  or sex-ratio-at-birth outcome (e.g. attitudes only, or son preference and child nutrition). Mechanism/context.
- `THEORY`: differential-stopping / sex-preference formal models with no own empirical estimate.
- `OFF_ADULT_SEX_RATIO`: identification off an already-skewed ADULT sex ratio -> marriage/fertility. Route to A.10 (Wall 1).
- `OFF_ABORTION_GENERAL`: abortion/contraceptive access -> total births regardless of sex. Route to A.4/A.2 (Wall 2).
- `OFF_PARITY_STOPPING`: sex-indifferent target-number stopping/spacing. Route to A.8 (Wall 3).
- `OFF_OLD_AGE_SECURITY`: identification off pensions / formal old-age support. Route to C.3.c (Wall 4).
- `OFF_GENDER_EQUITY`: identification off female autonomy / egalitarian-norm diffusion. Route to D.2.a (Wall 5).
- `OFF_CHILD_MORTALITY`: identification off mortality decline / replacement. Route to A.1 (Wall 6).
- `OFF_OUTCOME`: son preference -> a NON-fertility outcome (excess female mortality, child health, schooling,
  nutrition, dowry). Real and important, but not this chapter's parameter. Mechanism / context only.
- `OFF_OTHER`: a non-D.2.c determinant of fertility with no sibling-hypothesis home above.
- `REVERSE`: fertility/family size -> sex preference or sex ratio. Narrow; takes `NOT_RELEVANT` unless it
  also carries a preference -> fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a son-preference exposure (or a sex-selection-technology shock) AND a fertility / parity /
   sex-ratio-at-birth outcome must be present for a PRIMARY cell.
2. **The identification tags.** Set `identification=REVEALED_STOPPING` when the design exploits the
   near-random sex of early births to test parity progression conditional on sex composition. Set
   `identification=NATURAL_EXPERIMENT` when the design uses an exogenous shock — arrival/diffusion of
   ultrasound/amniocentesis, a sex-selection ban or policy reform, or a discontinuity. A stated-preference
   cross-section (DHS desired-sex items correlated with fertility) or a raw correlation is
   `ASSOCIATIONAL_ONLY`. Such a paper is still `RELEVANT` if it bears on the estimand; the tag records that
   it is not cleanly identified. Never upgrade an association to an identified effect.
3. **The substitution rule (Wall 1/Wall 2).** Where sex selection is available, the fertility effect and
   the sex-ratio-at-birth effect move in OPPOSITE directions. A paper reporting the sex ratio at birth as
   the expression of son preference under a fertility constraint is `PRIMARY_SEXSEL_SUBSTITUTION`, NOT an
   A.10 adult-sex-ratio paper.
4. Do not promote an OFF-cell paper to PRIMARY merely because it mentions sons or sex. Conversely, do not
   demote a genuine son-preference -> fertility estimand merely because it also reports mortality or
   autonomy covariates.
5. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate.
6. **Homonyms are `NOT_RELEVANT` / `NA`.** "son" as a surname or given name (Johnson, Robinson, prodigal
   son), "sex"/"gender" in biology or grammar (sex determination, sexual dimorphism, grammatical gender,
   gender identity broadly), and "preference" in economics/consumer choice (revealed preference, time
   preference) are out of scope unless the paper is genuinely about son preference and fertility. Say which
   homonym in `reason`.
7. Contentless records — prefaces, front matter, tables of contents, editorial notes — are `NOT_RELEVANT` /
   `NA`, not `UNCERTAIN`.
8. `sub_mechanism` is descriptive, not a router: `STOPPING`, `SEXSEL_ABORTION`, `NORM_INTENSITY`,
   `MORTALITY_INTERACTION`, or `NA`.
9. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
   verbatim because they drive downstream pooling exclusion: exactly `review` for ANY review/meta-analysis,
   and exactly `theory` for ANY purely theoretical/formal-model paper with no own estimate. Else give the
   closest of `quasi-experimental`, `observational`, `structural`, `qualitative`, `descriptive`,
   `mechanism`, or `other`.

## Output

Return ONLY a JSON array, one object per input record, IN THE SAME ORDER, each with exactly:
`id`, `verdict` (RELEVANT|UNCERTAIN|NOT_RELEVANT), `estimand_cell`, `sub_mechanism`, `outcome` (short
phrase for the fertility/sex-ratio outcome, or "none"), `identification`
(NATURAL_EXPERIMENT|REVEALED_STOPPING|ASSOCIATIONAL_ONLY|UNCLEAR|NA), `evidence_type`, `reason` (one sentence).
