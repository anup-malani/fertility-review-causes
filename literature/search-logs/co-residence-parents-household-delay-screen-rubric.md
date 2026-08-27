# Title/abstract screening rubric — A.23 co-residence and delayed household formation

**Hypothesis (HYPOTHESES-v5 §A.23):** extended co-residence of young adults with parents delays or
prevents fertility by blocking independent household formation — privacy, sexual autonomy, and the
sense of being an adult with a household of one's own. **Target phenomenon: SDT.**

**Ruling 1 (2026-08-27) widens this.** A.23 owns variation in the living arrangement in *both* of its
configurations, which have opposite predicted signs:

- **PRE_LAUNCH** — an unpartnered, childless young adult living in the parental home. Predicted sign
  on fertility: **negative**. This is the configuration the registered claim describes.
- **EXTENDED_COUPLE** — a couple, usually already partnered, living with a parent or parent-in-law,
  where the parent supplies childcare and household labour. Predicted sign: **positive**. This is the
  modal configuration in the East Asian literature.

They share a phrase and nothing else, and they are never pooled.

You see title, venue, year, type, language and a truncated abstract. You do **not** see whether the
record is an anchor, whether it is gold, whether it was hand-added, or whether the snowball pool also
reached it. That is deliberate: the frame marks gold so the screen can be audited against it
afterwards, and a screener who can see the marking destroys the audit.

Return one JSON object per record with the fields below.

## `exposure_is_arrangement` — yes | no | cannot_tell

**The field this screen exists for.** Does the record's *exposure* — the thing that varies, the
treatment, the independent variable — involve the LIVING ARRANGEMENT: who lives with whom?

Say **no** when the exposure is something else, even when the paper is about parents and children and
fertility. The commonest case, and the one that has already produced a real error in this chapter's
own anchor set:

> A pension reform delays a grandmother's retirement, so she provides less childcare, so her
> daughter has fewer children. **The exposure is the grandmother's TIME, not the living
> arrangement.** Nobody moved house. That is C.2.a's variation (childcare availability), and the
> record routes to `OFF_CHILDCARE_C2a`.

Eight of nineteen hand-selected gold candidates failed exactly this test. Expect it at scale. The
question is not "is this paper about families" — it is "does the arrangement VARY".

Say **no** also when the arrangement is only a control variable, a sample description, or a phrase in
the motivation, with something else being estimated.

## `config` — PRE_LAUNCH | EXTENDED_COUPLE | ELDER_SUPPORT | PROXIMITY | UNSPLIT | cannot_tell

Which configuration of the arrangement is being studied.

- `ELDER_SUPPORT` — an adult child housing a *dependent elderly* parent. Different construct,
  dependency runs the other way; routes out. Do not use the words "elderly" or "ageing" alone to
  decide this: a couple living with a healthy 62-year-old who minds the baby is `EXTENDED_COUPLE`,
  and the same household ten years later is `ELDER_SUPPORT`.
- `PROXIMITY` — living *near* parents without co-residing. Different treatment, pooled separately.
- `UNSPLIT` — the study genuinely pools configurations.
- `cannot_tell` — **a first-class answer, not a failure.** The distinguishing facts are often in a
  sample restriction or a descriptives table. Its share across the frame is a measurement this
  chapter needs. Do not guess to avoid it.

## `outcome` — fertility | union_only | arrangement_only | labour_supply | other | cannot_tell

- `fertility` — births, parity progression, completed fertility, childlessness, fertility intentions.
- `union_only` — marriage, cohabitation, partnership formation, and no birth outcome. This is link 1
  of the chain and is real evidence about it, but it is not a fertility estimate.
- `arrangement_only` — the outcome IS the living arrangement (who leaves home, when). Link 1's other
  half; establishes the exposure trend.
- `labour_supply` — maternal employment, hours, wages. **Expected to be the largest single route-out**:
  the extended-household literature's own estimand is usually the mother's job, with fertility
  secondary or absent. Routes to `OFF_OUTCOME_LABOUR_SUPPLY`, cross-ref C.2.e.

## `design` — identified | observational | descriptive | theory | cannot_tell

`identified` means an explicit source of exogenous variation: a policy discontinuity, an instrument,
a natural experiment, a difference-in-differences. **Controls are not identification**, and neither
is a longitudinal design on its own. When in doubt, `observational`.

## `anticipation_flag` — yes | no | cannot_tell

Does the record appear to address the chapter's central threat: that leaving home, forming a union
and having a first child are ordered jointly, so people move out *in order to* have a child? A design
using pre-determined arrangement, an instrument, or an event-history with time-varying covariates
gets `yes`. Silence gets `no`. This is a flag, not a gate; the gate is at full text.

## `route` — the estimand cell

One of: `PRIMARY_PRELAUNCH`, `PRIMARY_EXTENDED_COUPLE`, `PRIMARY_PROXIMITY`,
`LINK1_ARRANGEMENT_TO_UNION`, `LINK1_DRIVER_TO_ARRANGEMENT`, `MIXED_PRICE_ARRANGEMENT`,
`AGGREGATE_UNSPLIT`, `OFF_OUTCOME_LABOUR_SUPPLY`, `ELDER_SUPPORT`, `OFF_PRICE_C2c`,
`OFF_UNION_TIMING_A7`, `OFF_NORMS_D2b`, `OFF_UNCERTAINTY_C5a`, `OFF_DEBT_C3g`, `OFF_CHILDCARE_C2a`,
`OFF_OUTCOME`, `THEORY`, `REVERSE`, `INSUFFICIENT_INFO`.

## `verdict` — RELEVANT | UNCERTAIN | NOT_RELEVANT

`RELEVANT` requires `exposure_is_arrangement: yes` **and** a fertility outcome. Everything else that
is on-topic but off-cell is `UNCERTAIN` with a route, not `NOT_RELEVANT`. Reserve `NOT_RELEVANT` for
records that are not about this subject at all.

## `info` — sufficient | insufficient

`insufficient` whenever there is no abstract and the title is not decisive, or the abstract is present
but silent on the fields above. `insufficient` pairs with `UNCERTAIN`, never with `NOT_RELEVANT`.

## `note` — one sentence

What decided it. If you routed the record out, name the exposure you think it actually has.
