# Blinded title/abstract screening rubric — coital frequency and fecundability (A.14) — v1

## Review question

Does the paper bear on **A.14** — the claim that variation in **coital frequency** (the number of acts
of intercourse per unit time, driven by spousal separation, customary/religious abstinence, health,
age, or the modern "sex recession") alters **monthly fecundability and realized fertility**, through
the frequency -> fecundability -> births identity, INDEPENDENTLY of contraceptive use? A.14's parameter
is the effect of **coital frequency (or an exogenous shock to it) on the per-cycle conception
probability, time-to-pregnancy, or the birth rate**, holding contraception, union status, and fecund
capacity fixed. A.14 is the EXPOSURE gate among the Bongaarts proximate determinants.

Judge ONLY the supplied title and abstract. Discovery channel and citation count are intentionally
hidden. Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states
the estimand verbatim (e.g. "The role of marital sexual abstinence in determining fertility"); route
such a record normally but set `identification` to `NA` unless the title also names the design. In every
other abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a
substantive cell for a record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is ALL THREE (PM, FDT, SDT).** Coital exposure operates in every fertility regime:
spousal separation and post-partum abstinence in pre-modern and historical/natural-fertility
populations (PM/FDT), the "sex recession" in the SDT. A historical parish-reconstitution or
natural-fertility study of abstinence/separation and fertility is IN scope, not out.

## THE SIX LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs A.2-A.6 (Contraception and Abortion, the Cc/Ca indices). LOAD-BEARING.** The claim is
explicit that A.14 operates "independently of contraceptive use." Contraception/abortion change the
probability that intercourse (or a conception) yields a birth, HOLDING FREQUENCY FIXED; A.14 changes the
number of acts, holding contraceptive practice fixed. A study identifying off contraceptive adoption,
method mix, or abortion access is `OFF_CONTRACEPTION`. A frequency study in a natural-fertility /
non-contracepting population is the CLEANEST A.14 evidence (Cc held at baseline) and stays here.

**Wall 2 — vs A.7/C.7/A.23/A.24 (Marriage, Marriage Market, Union/Match Formation, the Cm index).** Cm
is whether a person is in a coital union AT ALL; A.14 is how often intercourse occurs GIVEN a union. A
study whose variation is in the proportion married/partnered, age at marriage, or match formation is
`OFF_UNION_FORMATION`. **Bridge:** a spousal-separation study (migration, war) reduces frequency WITHIN
an intact marriage — that is `PRIMARY_SEPARATION_SHOCK` (A.14), because the union persists and only
exposure falls. When a paper cannot separate "fewer unions" from "less sex within unions", it has not
identified this parameter -> `UNCERTAIN`.

**Wall 3 — vs A.13 (Breastfeeding / Lactational Amenorrhoea, the Ci index).** A.13 suppresses ovulation
post-partum (no fecund cycle to expose); A.14 changes exposure within fecund cycles. A study whose
mechanism is anovulation/amenorrhoea from lactation is `OFF_LACTATION`. The post-partum ABSTINENCE taboo
(reduced intercourse, not lactational anovulation) is `PRIMARY_ABSTINENCE_WINDOW` (A.14).

**Wall 4 — vs A.15/A.16/B.3 (Fecundity Capacity: maternal age, sperm quality, sterilising infection).**
These change the couple's CAPACITY to conceive at any frequency (the fecundability ceiling); A.14
changes the frequency at a fixed capacity. A study identifying off age-related fecundity decline, sperm
quality, or sterilising infection is `OFF_FECUNDITY_CAPACITY`. Age is a confounder A.14 studies must
address (older couples have both lower fecundity AND lower frequency); a design that cannot separate the
two is `UNCERTAIN`.

**Wall 5 — vs the UPSTREAM CAUSES of a frequency change (C.2.h digital leisure, B.7 antidepressants,
D.1.a values).** A.14 owns the frequency -> births identity REGARDLESS of what changed frequency. A
study whose estimand is `cause -> coital frequency` (digital leisure, a drug, a value shift -> less sex)
is `OFF_UPSTREAM_CAUSE`. A study whose estimand is `coital frequency -> fertility/fecundability` stays
here, reading the upstream cause only as the source of exogenous variation.

**Wall 6 — vs B.5 (Fetal Loss / Intrauterine Mortality).** A.14 governs whether a conception OCCURS;
B.5 whether an established conception SURVIVES to a live birth. A study whose outcome is the loss of an
established pregnancy is `OFF_FETAL_LOSS`. A study whose outcome is the per-cycle conception probability,
time-to-pregnancy, or births-per-exposure stays here.

## Estimand cells

- `PRIMARY_FREQ_BIOMETRIC`: measured coital frequency or timing of intercourse relative to ovulation, in
  a fecund non-contracepting sample -> per-cycle conception probability / fecundability / time-to-pregnancy.
- `PRIMARY_SEPARATION_SHOCK`: an exogenous spousal separation (labour/seasonal migration, war
  mobilisation, incarceration, commuter/LAT marriage) -> birth rate / fertility / birth timing.
- `PRIMARY_ABSTINENCE_WINDOW`: customary/religious abstinence (post-partum taboo, Ramadan/Lenten fasting,
  ritual periods) -> birth rate / conception timing / seasonality of births.
- `PRIMARY_FREQ_DECLINE`: a population-level decline in coital frequency (the "sex recession") LINKED to
  a fertility outcome -> TFR / birth rate / childlessness.
- `MECHANISM_FREQ_ONLY`: documents coital-frequency levels/trends or its correlates with NO
  fertility/fecundability outcome (e.g. a pure "sex recession" trend paper, or coital frequency and
  relationship satisfaction). Mechanism/context only.
- `THEORY`: the proximate-determinants / intermediate-variables framework (Bongaarts, Davis & Blake,
  Wood) or fecundability modelling with no own empirical estimate.
- `OFF_CONTRACEPTION`: identification off contraceptive adoption/method mix or abortion access. Route to A.2-A.6 (Wall 1).
- `OFF_UNION_FORMATION`: variation in proportion married/partnered, age at marriage, match formation. Route to A.7/C.7 (Wall 2).
- `OFF_LACTATION`: post-partum anovulation/amenorrhoea from breastfeeding. Route to A.13 (Wall 3).
- `OFF_FECUNDITY_CAPACITY`: age-related fecundity decline, sperm quality, sterilising infection. Route to A.15/A.16/B.3 (Wall 4).
- `OFF_UPSTREAM_CAUSE`: estimand is cause -> coital frequency (digital leisure, antidepressant, value shift). Route to C.2.h/B.7/D.1.a (Wall 5).
- `OFF_FETAL_LOSS`: outcome is loss of an established pregnancy. Route to B.5 (Wall 6).
- `OFF_OUTCOME`: coital frequency -> a NON-fertility outcome (sexual satisfaction, wellbeing, STI,
  relationship quality). Mechanism / context only.
- `OFF_OTHER`: a non-A.14 determinant of fertility with no sibling-hypothesis home above.
- `REVERSE`: fertility/childbearing -> coital frequency (e.g. post-birth frequency change). Narrow;
  takes `NOT_RELEVANT` unless it also carries a frequency -> fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a coital-frequency/exposure variation AND a fertility / fecundability / conception outcome must
   be present for a PRIMARY cell.
2. **The reverse-causality rule (A.14's key identification threat).** Wanting (or not wanting) a child
   changes coital frequency and its timing, so a raw cross-sectional correlation between frequency and
   conception is biased. Set `identification=EXOGENOUS_FREQUENCY_SHOCK` when the design uses a frequency
   shock plausibly unrelated to fertility desire (spousal separation from migration/war/incarceration,
   ritual/post-partum abstinence windows). Set `identification=PROSPECTIVE_MEASUREMENT` when frequency
   (or intercourse timing) is measured prospectively before conception (daily diaries, fertility-window
   studies). A cross-sectional or retrospective-recall correlation is `ASSOCIATIONAL_ONLY`. Such a paper
   is still `RELEVANT` if it bears on the estimand; the tag records that it is not cleanly identified.
   Never upgrade an association to an identified effect.
3. **The age confound (Wall 4).** A study relating frequency to conception that does not separate the
   effect of frequency from age-related fecundity decline has not cleanly identified this parameter; keep
   it `RELEVANT`/`ASSOCIATIONAL_ONLY` if frequency is the estimand, but route to `OFF_FECUNDITY_CAPACITY`
   if the paper's actual estimand is the age/capacity decline.
4. Do not promote an OFF-cell paper to PRIMARY merely because it mentions sex or intercourse. Conversely,
   do not demote a genuine coital-frequency -> fertility estimand merely because it also reports
   contraceptive or age covariates.
5. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate, so the cell need not be distorted.
6. **Homonyms are `NOT_RELEVANT` / `NA`.** "separation" in statistics/chemistry/law (separation of
   variables, phase separation, legal separation), "activity" in physics/biochemistry (enzyme activity,
   physical activity, radioactivity), "migration" in cell biology/ornithology (cell migration, bird
   migration), and "frequency" in physics/signal processing (radio frequency, frequency domain) are out
   of scope unless the paper is genuinely about coital frequency/exposure and fertility. Say which
   homonym in `reason`.
7. Contentless records — prefaces, front matter, tables of contents, editorial notes — are
   `NOT_RELEVANT` / `NA`, not `UNCERTAIN`.
8. `sub_mechanism` is descriptive, not a router: it records the driver of the frequency variation the
   paper speaks to — `SEPARATION`, `ABSTINENCE`, `BIOMETRIC_TIMING`, `FREQUENCY_DECLINE`,
   `LIBIDO_HEALTH`, or `NA`.
9. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
   verbatim because they drive downstream pooling exclusion: exactly `review` for ANY review/
   meta-analysis, and exactly `theory` for ANY purely theoretical/formal-model paper with no own
   estimate. Else give the closest of `quasi-experimental`, `observational`, `prospective`,
   `structural`, `qualitative`, `descriptive`, `mechanism`, or `other`.

## Output

Return ONLY a JSON array, one object per input record, IN THE SAME ORDER, each with exactly:
`id`, `verdict` (RELEVANT|UNCERTAIN|NOT_RELEVANT), `estimand_cell`, `sub_mechanism`, `outcome` (short
phrase for the fertility/fecundability outcome, or "none"), `identification`
(EXOGENOUS_FREQUENCY_SHOCK|PROSPECTIVE_MEASUREMENT|ASSOCIATIONAL_ONLY|UNCLEAR|NA), `evidence_type`,
`reason` (one sentence).
