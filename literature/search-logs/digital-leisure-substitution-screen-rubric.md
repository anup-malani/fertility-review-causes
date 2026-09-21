# Blinded title/abstract screening rubric — digital leisure substitution (C.2.h) — v1

## Review question

Does the paper bear on **C.2.h** — the claim that the smartphone/app economy sharply lowered the price
and raised the absorptiveness of non-reproductive digital leisure (social media, streaming, gaming,
pornography), inducing a Becker substitution AWAY from the time, attention, and commitment that
partnership and childrearing require, and thereby lowering fertility? C.2.h's parameter is the effect
on **fertility (or its proximate partnering / coital-frequency mediators) of a fall in the price or a
rise in the availability/engagement-intensity of digital leisure**, net of the mother's wage/
opportunity cost (C.2.e), the dating-market matching technology (A.24), the coital-frequency
proximate-determinant identity (A.14), the underlying value shift (D.1.a), and the clinical
mental-health pathway (D.3.a).

Judge ONLY the supplied title and abstract. Discovery channel and citation count are intentionally
hidden. Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states
the estimand verbatim (e.g. "Does broadband Internet affect fertility?"); route such a record normally
but set `identification` to `NA` unless the title also names the design. In every other abstract-less
case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a substantive cell for a
record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is SDT ONLY** — the mechanism presupposes the consumer-internet / smartphone era
(broadly post-2000, concentrated post-2010). There is NO pre-modern and NO FDT cell. A historical or
pre-internet study of leisure and fertility is `NOT_RELEVANT` / `NA`.

## THE FIVE LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs C.2.e (Female Wage / Opportunity Cost of Time).** Both are Becker substitution effects.
C.2.e is a rise in the price of the mother's TIME through the LABOR MARKET (wages, female labor-force
participation). C.2.h is a fall in the price of the LEISURE SUBSTITUTE. A study identifying off wages,
FLFP, or labor-market returns is `OFF_WAGE_C2E`. A study identifying off the price/availability/
engagement of digital leisure stays here.

**Wall 2 — vs A.24 (Dating Apps and Union-Formation Friction). THE near wall.** Same device. A.24 is
the effect of app-mediated MATCHING on couple formation (match quality, search frictions, how couples
meet). C.2.h is digital leisure CROWDING OUT the time and in-person interaction from which partnerships
form. A dating-app / online-dating / matching-market study is `OFF_DATINGAPP_A24`. A study of general
digital-leisure time displacing face-to-face socializing → `PRIMARY_SOCIAL_DISPLACEMENT` (C.2.h). When
the estimand is specifically the matching technology, route to A.24.

**Wall 3 — vs A.14 (Coital Frequency and Fecundability).** A.14 owns the frequency → fecundability →
births IDENTITY, regardless of cause. C.2.h owns the digital-leisure CAUSE of a frequency change. A
study whose estimand is coital frequency → births (the biological determinant) is `OFF_COITAL_A14`. A
study of pornography or digital leisure → coital frequency (or → fertility), with frequency as a
mediator, is `PRIMARY_PORN_SUBSTITUTION` (or another PRIMARY cell) here.

**Wall 4 — vs D.1.a (Postmaterialism / Individualism / Secularization).** D.1.a is the VALUE shift that
makes self-oriented leisure desirable. C.2.h is the PRICE/technology shock, holding tastes fixed. A
study identifying off attitudes/values is `OFF_VALUES_D1A`; a study identifying off a technology/price
shock (network rollout, device/broadband diffusion, data cost) stays here.

**Wall 5 — vs D.3.a (Mental Health and Anxiety Epidemic). Load-bearing (large overlap).** C.2.h is the
DIRECT time/attention crowd-out of partnering and childrearing. D.3.a is the AFFECTIVE/CLINICAL pathway
— diagnosed or subclinical anxiety/depression impairing pair-bonding and reproductive intention. A
study whose estimated mechanism runs THROUGH a measured mental-health state (a depression scale, a
diagnosis, "mediated by anxiety") is `OFF_MENTALHEALTH_D3A`. A study of direct behavioural crowd-out
(time use, motivation, sexual frequency) with no affective mediator stays here. When a screen-time →
fertility paper routes through depression, it is D.3.a.

## Estimand cells

- `PRIMARY_LEISURE_PRICE`: an exogenous fall in the price / rise in availability or engagement of
  digital leisure (network-technology rollout, broadband/smartphone diffusion, data-cost or
  content-supply shock) → fertility / birth rate / TFR.
- `PRIMARY_PORN_SUBSTITUTION`: pornography access/consumption as a substitute for partnered sex →
  coital frequency, partnership, or fertility (Wall 3: frequency is the mediator, not the identity).
- `PRIMARY_SOCIAL_DISPLACEMENT`: digital-leisure time crowding out in-person interaction → couple/union
  formation, marriage, cohabitation, fertility (Wall 2: not the matching technology).
- `MECHANISM_TIMEUSE`: time-use / attention evidence that digital leisure displaces partnering or
  childcare time, with NO fertility (or partnering/coital) outcome. Mechanism/context only.
- `THEORY`: Becker time-allocation / household-production theory or screen-time theory with no own
  estimate.
- `OFF_WAGE_C2E`: identification off wages / FLFP / labor-market opportunity cost. Route to C.2.e (Wall 1).
- `OFF_DATINGAPP_A24`: dating-app / online-dating matching-market mechanics. Route to A.24 (Wall 2).
- `OFF_COITAL_A14`: coital frequency → fecundability → births as the determinant. Route to A.14 (Wall 3).
- `OFF_VALUES_D1A`: the value/attitude shift as the driver. Route to D.1.a (Wall 4).
- `OFF_MENTALHEALTH_D3A`: effect mediated through a measured anxiety/depression state. Route to D.3.a (Wall 5).
- `OFF_OUTCOME`: digital leisure → a NON-fertility, non-partnering outcome (productivity, sleep,
  academic performance, wellbeing). Mechanism / context only.
- `OFF_OTHER`: a non-C.2.h determinant of fertility with no sibling-hypothesis home above.
- `REVERSE`: low fertility / childlessness → more leisure or higher digital consumption. Narrow;
  takes `NOT_RELEVANT` unless it also carries a digital-leisure→fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a digital-leisure exposure AND a fertility / partnering / coital-frequency outcome must be
   present for a PRIMARY cell.
2. **The reverse-causality / common-trend rule (C.2.h's key identification threat).** People with fewer
   children and no partner have more discretionary time and consume more digital leisure, so a raw
   correlation is biased TOWARD the hypothesis; and smartphones diffused over exactly the years wages,
   housing costs, and postponement all intensified, so a national time series cannot separate the
   leisure channel from every other SDT driver. Set `identification=EXOGENOUS_LEISURE_VARIATION` ONLY
   when the design isolates a plausibly-exogenous change in leisure price/availability (a device/network
   rollout instrument such as AT&T's iPhone monopoly or broadband expansion, a staggered-diffusion
   design, a discontinuity). A cross-sectional or time-series correlation is `ASSOCIATIONAL_ONLY`. Such
   a paper is still `RELEVANT` if it bears on the estimand; the tag records that it is not identified.
   Never upgrade an association to an identified effect.
3. **Wall 5 is decided on the mediator.** A screen-time / social-media → fertility study whose mechanism
   is a measured mental-health state is `OFF_MENTALHEALTH_D3A`; direct time/attention crowd-out stays
   here. When in doubt on a study that foregrounds depression/anxiety as the channel, route to D.3.a.
4. Do not promote an OFF-cell paper to PRIMARY merely because it mentions screens or leisure as
   motivation. Conversely, do not demote a genuine digital-leisure→fertility estimand merely because it
   also reports wage or value covariates.
5. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate, so the cell need not be distorted.
6. **Homonyms are `NOT_RELEVANT` / `NA`.** "Substitution" in chemistry/econometrics (elasticity of
   substitution, import substitution), "attention" in machine learning/neuroscience, "screen(ing)" in
   medicine (cancer/prenatal screening), and "gaming" in game theory/gambling are out of scope unless
   the paper is genuinely about digital leisure and fertility/partnering. Say which homonym in `reason`.
7. Contentless records — prefaces, front matter, tables of contents, editorial notes — are
   `NOT_RELEVANT` / `NA`, not `UNCERTAIN`.
8. `sub_mechanism` is descriptive, not a router: it records which of C.2.h's three sub-mechanisms the
   paper speaks to — `SOCIAL_DISPLACEMENT`, `PORNOGRAPHY`, `MOTIVATIONAL_LEISURE`, `TIME_USE`, or `NA`.
9. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
   verbatim because they drive downstream pooling exclusion: exactly `review` for ANY review/
   meta-analysis, and exactly `theory` for ANY purely theoretical/formal-model paper with no own
   estimate. Else give the closest of `quasi-experimental`, `observational`, `structural`,
   `qualitative`, `descriptive`, `mechanism`, or `other`.

## Output

Return ONLY a JSON array, one object per input record, IN THE SAME ORDER, each with exactly:
`id`, `verdict` (RELEVANT|UNCERTAIN|NOT_RELEVANT), `estimand_cell`, `sub_mechanism`, `outcome` (short
phrase for the fertility/partnering/coital outcome, or "none"), `identification`
(EXOGENOUS_LEISURE_VARIATION|ASSOCIATIONAL_ONLY|UNCLEAR|NA), `evidence_type`, `reason` (one sentence).
