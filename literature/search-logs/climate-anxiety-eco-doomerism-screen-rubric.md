# Blinded title/abstract screening rubric — climate anxiety & eco-doomerism (D.3.b) — v2

## Review question

Does the paper bear on **D.3.b** — the claim that fear about the ecological future *suppresses* childbearing,
so that fertility falls **without a fall in the desire for children**? The distinctive D.3.b mechanism is
affective: dread about planetary habitability, or an ethical objection to the emissions an additional child
would add, acting on a desire for children that may itself still be positive. Preserve the anti-natalist /
eco-ethics philosophical stream and the climate-anxiety psychometric stream, but route them outside the
empirical primary estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally hidden.
Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states the
estimand verbatim (e.g. "Are Environmental Concerns Deterring People from Having Children?"); route such
a record normally but set `outcome_level` to `NA` unless the title also names the outcome level. In every
other abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a
substantive cell for a record you know nothing about — that corrupts the cell counts.

Phenomenon scope is **SDT only** — this is a 21st-century mechanism. There is no pre-modern or FDT cell.

## THE THREE LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs D.1.a (postmaterialism / self-actualization).** D.1.a is a *positive* preference shift: the
desire for children has genuinely fallen in favour of autonomy, career, or self-realization. D.3.b is
*fear suppressing a live desire*. A paper is D.3.b only if BOTH (a) the operative content is ecological
fear or eco-ethical concern, AND (b) the desire for children is not simply relabeled freedom/career/
lifestyle preference. A climate-mentioning paper whose actual estimand is a positive child-free
preference routes to `OFF_POSTMATERIALIST_D1a`. This is a HARD line.

*Framing vs reported reasons.* A paper that **motivates** on ecological catastrophe but whose **reported
operative reasons** are financial, career, or freedom-related routes off under Wall 1. Judge the reported
reasons, not the framing sentence. (If the abstract shows only the framing and truncates before the
results, that is an `UNCERTAIN`.)

**Wall 2 — vs D.3.a (mental-health epidemic).** General clinical anxiety or depression → fertility is
D.3.a. D.3.b requires the feared object to be **specifically ecological/planetary**. A general
psychological-distress measure with no climate content routes to `OFF_CLINICAL_D3a`, even in a paper
that frames itself around climate.

**Wall 3 — vs C.5.a (economic uncertainty).** Same "the future looks bad" shape, different feared object.
If the fear is about the respondent's own job, income, or economic security — or the mechanism is
option-value / wait-and-see on a return to normalcy — it is `OFF_ECON_C5a`. D.3.b's feared object is
planetary habitability or emissions ethics, and its mechanism is affect/dread.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_HABITABILITY_FEAR | PRIMARY_CARBON_ETHICS | PRIMARY_ECO_PESSIMISM | DESIRE_INDEPENDENCE | ECO_ETHICS_THEORY | ANXIETY_CONSTRUCT | OFF_POSTMATERIALIST_D1a | OFF_CLINICAL_D3a | OFF_ECON_C5a | OFF_OTHER | OFF_OUTCOME | REVERSE | INSUFFICIENT_INFO | NA",
  "outcome_level": "STATED_INTENTION_OR_ATTITUDE | REALIZED_FERTILITY | BOTH | NA",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "desire_for_children_held_fixed": "yes | no | unclear",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: studies or models ecological fear / eco-doom / carbon-ethics concern as a determinant of
  fertility intention or realized fertility, or evidence that such fear suppresses childbearing while the
  desire for children remains positive. **`RELEVANT` ALSO covers the two theory cells** — see the note
  immediately below.
- `UNCERTAIN`: plausibly belongs, but missing/ambiguous information prevents confident routing.
- `NOT_RELEVANT`: does not bear on the ecological-fear → fertility estimand. General climate-attitude,
  general fertility-decline, and physical-climate-exposure papers are NOT automatically relevant.

**The theory streams take `RELEVANT`.** `ECO_ETHICS_THEORY` and `ANXIETY_CONSTRUCT` papers have no
fertility estimand by definition, but they are preserved deliberately and are therefore `RELEVANT`, not
`NOT_RELEVANT`. They are separated downstream and do **not** count toward empirical recall, so marking
them `RELEVANT` cannot inflate any pooled estimate. This instruction is explicit because it was the single
largest source of screener disagreement in the v1 pilot — do not resolve it by your own judgment.

## Estimand cells

- `PRIMARY_HABITABILITY_FEAR`: fear that the world will be uninhabitable or dangerous *for one's children*
  → reduced fertility intention or realized fertility.
- `PRIMARY_CARBON_ETHICS`: the ethical concern that an additional child adds emissions / anti-natalism
  for the planet → reduced fertility intention or behavior.
- `PRIMARY_ECO_PESSIMISM`: generalized ecological pessimism or eco-doom about the collective future →
  reduced fertility intention or behavior.
- `DESIRE_INDEPENDENCE`: any of the above, where fertility or intention falls while the *desire* for
  children is positive or explicitly held fixed. This is the value-added cell — use it in preference to
  the three PRIMARY cells whenever the design actually separates fear from desire. It requires the
  DESIGN to separate fear from desire, not merely a respondent subgroup saying so; a subgroup report is
  the relevant PRIMARY cell instead.
- `ECO_ETHICS_THEORY`: anti-natalist / eco-ethics philosophy and normative argument about procreation and
  the planet, with no empirical fertility estimate. Must carry **ecological** content — non-ecological
  anti-natalism (harm-of-existence, Benatar/Kantian) is NOT this cell, it is `OFF_OTHER`.
- `ANXIETY_CONSTRUCT`: climate anxiety / eco-distress as the **object** of study — construct development,
  scale validation, prevalence, latent profiles, or predictors of climate-anxiety scores. Climate anxiety
  is the dependent variable and there is no fertility outcome.
- `OFF_POSTMATERIALIST_D1a`: positive self-actualization / autonomy preference or secular value shift with
  no fear content → fertility. Route to D.1.a (Wall 1).
- `OFF_CLINICAL_D3a`: general, non-climate-specific anxiety or depression → reproductive intention or
  fertility. Route to D.3.a (Wall 2).
- `OFF_ECON_C5a`: personal economic / job / income insecurity as the feared object → fertility. Route to
  C.5.a (Wall 3).
- `OFF_OTHER`: a non-D.3.b determinant of fertility with no sibling-hypothesis home — conflict/war
  insecurity, partisanship, religious law, gender and care institutions, non-ecological anti-natalism.
  Use this rather than forcing a paper into one of the three named `OFF_*` routers.
- `OFF_OUTCOME`: ecological fear / eco-concern as a determinant of some **other** non-fertility outcome
  (migration, consumption, politics, mental health). Mechanism or context only. Also the home for
  reverse-direction papers running through parenthood *experience* rather than status.
- `REVERSE`: parenthood or fertility **status** → climate concern / eco-worry. Narrow by design; takes
  verdict `NOT_RELEVANT` unless it also carries a fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both an ecological-fear / eco-ethics mechanism AND a fertility or reproductive-intention outcome must
   be present for a PRIMARY or `DESIRE_INDEPENDENCE` cell.
2. `outcome_level` is mandatory on every RELEVANT empirical paper. Stated intentions, desires, planned
   parity, and "climate is a reason I will have fewer children" are `STATED_INTENTION_OR_ATTITUDE`;
   completed or observed births/parity are `REALIZED_FERTILITY`. Both levels are in scope; the tag is
   never a reason to exclude. Use `NA` for theory and `NOT_RELEVANT` records **and for any `UNCERTAIN`
   record whose outcome level you cannot determine** — never guess a level to satisfy the field.
3. **Physical climate exposure** — heat, drought, disaster, or pollution → fertility or reproductive
   health, with no affective or attitudinal mechanism — is `NOT_RELEVANT` / `NA`. It belongs to the
   physical-climate-shock and biological-reproductive-health hypotheses, not here. Say so in `reason`.
   **Seam rule:** if the treatment is physical exposure but the OUTCOME is a reproductive *intention or
   attitude* (e.g. disasters → intention to remain childless), the outcome side wins and the paper is IN
   scope — D.3.b's estimand is about reproductive intention forming under ecological threat.
4. Do not promote an OFF-cell paper to PRIMARY merely because climate change is mentioned as motivation.
   Conversely, do not demote a paper with a genuine ecological-fear estimand merely because it also
   reports economic or political covariates.
5. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate, so the cell need not be distorted to keep them
   out. Never force a review into a theory cell or into `DESIRE_INDEPENDENCE` merely because rule 5 once
   forbade PRIMARY.
6. Set `desire_for_children_held_fixed=yes` only when the design actually holds the desire for children
   constant or reports it as positive alongside the fertility decline. This clause is what separates
   D.3.b's value-added claim from D.1.a's preference-shift claim (Wall 1).
7. Climate-anxiety papers with no fertility outcome split on what the anxiety IS in the design:
   climate anxiety as the dependent variable (prevalence, profiles, predictors, scale validation) is
   `ANXIETY_CONSTRUCT`; climate anxiety as a determinant of some other non-fertility outcome is
   `OFF_OUTCOME`. Neither is ever PRIMARY.
8. Generic future-pessimism whose feared object is named as neither ecological nor economic ("the
   turbulent state of the world") is `UNCERTAIN`. Do not resolve it toward D.3.b; the walls require the
   feared object to be identifiable.
9. Contentless records — prefaces, front matter, tables of contents, editorial notes — are
   `NOT_RELEVANT` / `NA`, not `UNCERTAIN`. They carry no estimand to be uncertain about.
