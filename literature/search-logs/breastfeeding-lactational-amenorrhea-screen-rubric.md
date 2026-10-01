# Blinded title/abstract screening rubric — breastfeeding and lactational amenorrhea (A.13) — v1

## Review question

Does the paper bear on **A.13** — the claim that **breastfeeding (suckling intensity and duration)
lengthens POSTPARTUM INFECUNDABILITY through lactational amenorrhea and anovulation, extending the BIRTH
INTERVAL and lowering NATURAL fertility**? A.13's parameter is **the effect of breastfeeding
intensity/duration on the length of lactational amenorrhea / postpartum infecundability and on the birth
interval — the Bongaarts C_i component — NET OF deliberate contraception and NET OF maternal nutrition /
energy balance**. It is a **spacing / quantum** effect on the interval between births, NOT a desired-
family-size effect and NOT a statement about why couples want fewer children.

Judge ONLY the supplied title and abstract. Discovery channel and citation count are intentionally hidden.
Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states the
estimand verbatim (e.g. "Breastfeeding, lactational amenorrhea and birth spacing in rural Bangladesh");
route such a record normally but set `identification` to `NA` unless the title also names the design. In
every other abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a
substantive cell for a record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is PM, FDT, and SDT.** A.13 is a proximate determinant and operates across all three
eras, but asymmetrically: it is the DOMINANT natural child-spacing mechanism in natural-fertility (PM) and
many LMIC (FDT) populations; during the FDT the DECLINE of breastfeeding (urbanization, wet-nursing, early
supplementation, formula) acted as a fertility-RAISING counter-force — that reversed-sign channel is IN
scope; in contracepting SDT populations the C_i contribution is minor and dominated by deliberate control.

## THE KEY AXIS: NATURAL SUCKLING-DRIVEN SPACING vs THE CONFOUNDS

The SAME observation — a longer birth interval among breastfeeding women — can be produced by A.13 (the
suckling -> amenorrhea mechanism), by deliberate contraception used concurrently, by maternal
undernutrition, or by postpartum sexual abstinence. On EVERY wall the discriminator is the MECHANISM the
study identifies, not the topic: **does the study identify the SUCKLING-DRIVEN amenorrhea / infecundability
channel (A.13), or a deliberate-contraception / energy-balance / abstinence / capacity / infant-health
channel (a neighbour)?**

## THE SIX LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs A.2–A.6 (deliberate contraception, family planning, abortion). LOAD-BEARING — the central
wall** (the frame probe put 1,938 records in this overlap). A.13 owns NATURAL, suckling-driven spacing. A
study whose spacing / fertility effect is carried by CONTRACEPTIVE METHOD adoption, access, or a
family-planning program is `OFF_CONTRACEPTION`. The boundary case is the **Lactational Amenorrhea Method
(LAM)**: a study that isolates the amenorrhea MECHANISM (pregnancy risk conditioned on amenorrhea + full
breastfeeding, Bellagio-style) is `LAM_EFFICACY` and stays IN; a study evaluating LAM as a promoted
PROGRAM / method-adoption choice against other methods is `OFF_CONTRACEPTION`. A study that reports a
breastfeeding spacing effect but cannot separate it from concurrent contraception is `MIXED_CONTRACEPTION`
(RELEVANT, a bound).

**Wall 2 — vs A.22 (maternal nutrition / energy balance).** Amenorrhea can be driven by maternal energy
balance (critical fat, undernutrition, caloric stress) rather than by suckling. A study whose amenorrhea /
infecundability estimand is attributed to NUTRITIONAL status / energy balance / body fat rather than to the
nursing regime is `OFF_ENERGY_BALANCE`. A study that identifies the suckling channel (frequency, intensity,
supplementation timing) stays here.

**Wall 3 — vs A.14 (postpartum sexual abstinence / coital frequency).** Postpartum ABSTINENCE is a separate,
behavioural C_i-adjacent channel: couples not resuming intercourse, independent of amenorrhea. A study
identifying the interval effect off postpartum sexual abstinence / taboo / coital frequency is
`OFF_ABSTINENCE`. A study identifying off suckling-driven amenorrhea / anovulation stays here. (Many
natural-fertility papers report both; take the A.13 cell only if the amenorrhea/infecundability component
is the estimand.)

**Wall 4 — vs A.1 (infant / child mortality). The REVERSE / confound wall.** Infant death TERMINATES nursing,
which shortens amenorrhea and the interval and raises the next-birth hazard; and an incoming pregnancy prompts
weaning. A study whose interval / fertility variation is driven by INFANT DEATH (a replacement/biological-
truncation effect) rather than by the exogenous nursing regime is `OFF_REVERSE_MORTALITY`. A study where the
"breastfeeding effect" is really reverse causation from weaning-on-conception is `REVERSE`.

**Wall 5 — vs A.15 / A.16 / B.3 (fecundity capacity).** Declining fecundity from advanced maternal age,
sperm quality, or sterilising infection is a CAPACITY story, not behavioural spacing. A study whose estimand
is age-related subfecundity, ovarian reserve, sperm count, or tubal/infective sterility is
`OFF_FECUNDITY_CAPACITY`.

**Wall 6 — vs the infant-health HOMONYM (the dominant homonym).** The vast breastfeeding literature is about
INFANT and child health — morbidity, growth, nutrition, cognition, infant mortality, allergy, immunity — with
NO maternal fertility / amenorrhea / birth-interval outcome. Any such record is `OFF_INFANT_HEALTH`, even
when it is a large, important breastfeeding study (e.g. breastfeeding -> child survival). A fertility /
amenorrhea / birth-interval / natural-fertility outcome for the MOTHER must be present for any IN cell.

## Estimand cells

- `LAM_EFFICACY`: pregnancy risk / contraceptive protection CONDITIONED on lactational amenorrhea + full
  breastfeeding, the amenorrhea mechanism isolated (Kennedy–Visness / Bellagio design).
- `PRIMARY_AMENORRHEA`: breastfeeding intensity / duration / supplementation -> length of lactational
  amenorrhea / postpartum anovulation / return of menses or ovulation (prospective cohort or hazard).
- `PRIMARY_BIRTH_INTERVAL`: breastfeeding regime -> birth / interbirth / interpregnancy interval, or the
  natural-fertility (C_i) level (micro or historical-reconstitution).
- `PRIMARY_SUCKLING_MECHANISM`: suckling pattern (frequency, night feeds) -> prolactin / ovarian suppression
  -> delayed ovulation (physiological or experimental). RELEVANT; establishes the mechanism.
- `MIXED_CONTRACEPTION`: a breastfeeding spacing / fertility effect that cannot be separated from concurrent
  deliberate contraception. RELEVANT; a bound. Cross-ref A.2.
- `THEORY`: proximate-determinants / C_i model or formal natural-fertility model with no own empirical
  estimate.
- `OFF_CONTRACEPTION`: spacing / fertility effect carried by deliberate contraception / family planning /
  LAM-as-program. Route to A.2–A.6 (Wall 1).
- `OFF_ENERGY_BALANCE`: amenorrhea / infecundability attributed to maternal nutrition / energy balance.
  Route to A.22 (Wall 2).
- `OFF_ABSTINENCE`: interval effect carried by postpartum sexual abstinence / coital frequency. Route to
  A.14 (Wall 3).
- `OFF_REVERSE_MORTALITY`: interval / fertility variation driven by infant death terminating nursing. Route
  to A.1 (Wall 4).
- `OFF_FECUNDITY_CAPACITY`: age / sperm / infection subfecundity. Route to A.15 / A.16 / B.3 (Wall 5).
- `OFF_INFANT_HEALTH`: breastfeeding -> infant / child health, growth, cognition, survival, with no maternal
  fertility outcome (Wall 6).
- `OFF_OUTCOME`: breastfeeding / amenorrhea -> some other non-fertility maternal outcome (maternal weight,
  bone density, breast cancer, mood) only.
- `OFF_OTHER`: a non-A.13 determinant of fertility with no sibling-hypothesis home above.
- `REVERSE`: weaning driven by a new pregnancy presented as a breastfeeding effect; or a shared-environment
  artefact presented as the suckling mechanism. `NOT_RELEVANT` unless it ALSO carries a genuine A.13
  estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a BREASTFEEDING / SUCKLING / LACTATIONAL-AMENORRHEA exposure AND a maternal fertility outcome
   (amenorrhea duration, return of menses/ovulation, birth / interbirth interval, natural-fertility level,
   or pregnancy risk under LAM) must be present for any LAM / PRIMARY / MIXED cell.
2. **The identification tags.** Set `identification=PROSPECTIVE_HAZARD` for a prospective cohort / survival
   analysis of amenorrhea or interval with measured nursing. `EXPERIMENTAL_MECHANISM` for a suckling ->
   prolactin / ovulation physiology study. `NATURAL_FERTILITY_RECON` for a historical reconstitution of
   breastfeeding and spacing. A bare cross-sectional breastfeeding–interval correlation with no such design
   is `ASSOCIATIONAL_ONLY`. `UNCLEAR` or `NA` otherwise.
3. **The contraception rule (Wall 1).** A breastfeeding–spacing effect identifies A.13 only if it is NOT
   carried by deliberate contraception. If the two cannot be separated it is `MIXED_CONTRACEPTION` (a bound),
   not PRIMARY. If the effect IS a contraceptive-method / program effect it is `OFF_CONTRACEPTION`.
4. **The infant-health rule (Wall 6).** Do NOT classify a study as A.13 merely because it is about
   breastfeeding. If the outcome is infant / child health (morbidity, growth, cognition, survival) with no
   maternal fertility / amenorrhea / interval outcome, it is `OFF_INFANT_HEALTH`.
5. Do not promote an OFF-cell paper to PRIMARY merely because it mentions breastfeeding, nursing, or birth.
   Conversely, do not demote a genuine suckling -> amenorrhea -> interval estimand merely because it also
   reports contraception or nutrition covariates.
6. Reviews and syntheses of the core estimand MAY take a LAM/PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate.
7. **Homonyms are `NOT_RELEVANT` / `NA`.** "lactation" in dairy / animal science (milk yield, calving
   interval, sow/litter), "prolactin" in endocrine oncology (prolactinoma), "nursing" in the nursing
   profession / nursing homes, "parity" in physics / statistics / signal processing, and "soil fertility" /
   agricultural fertility are out of scope. Say which homonym in `reason`.
8. Contentless records — prefaces, front matter, tables of contents, editorial notes — are `NOT_RELEVANT` /
   `NA`, not `UNCERTAIN`.
9. `sub_mechanism` is descriptive, not a router: `LACTATIONAL_AMENORRHEA`, `SUCKLING_PROLACTIN`,
   `BIRTH_SPACING`, `LAM_METHOD`, `NATURAL_FERTILITY`, or `NA`.
10. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
    verbatim because they drive downstream pooling exclusion: exactly `review` for ANY review/meta-analysis,
    and exactly `theory` for ANY purely theoretical/formal-model paper with no own estimate. Else give the
    closest of `quasi-experimental`, `observational`, `structural`, `qualitative`, `descriptive`,
    `mechanism`, or `other`.

## Output

Return ONLY a JSON array, one object per input record, IN THE SAME ORDER, each with exactly:
`id`, `verdict` (RELEVANT|UNCERTAIN|NOT_RELEVANT), `estimand_cell`, `sub_mechanism`, `outcome` (short
phrase for the fertility outcome, or "none"), `identification`
(PROSPECTIVE_HAZARD|EXPERIMENTAL_MECHANISM|NATURAL_FERTILITY_RECON|ASSOCIATIONAL_ONLY|UNCLEAR|NA),
`evidence_type`, `reason` (one sentence).
