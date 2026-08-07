# Blinded title/abstract screening rubric — cultural westernization and developmental idealism (D.1.b) — v1

## Review question

Does the paper bear on **D.1.b** — the claim that a diffused model of the modern family (nuclear and
conjugal, late-marrying, gender-egalitarian, investing heavily in few children, and therefore small)
reduces fertility **independently of structural economic change**, transmitted through mass schooling,
mass media, development institutions, and direct Western contact? Preserve the Caldwell/Thornton
theoretical canon and the world-society literature, but route them outside the empirical primary
estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are hidden. Do not infer
findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone suffices ONLY when it states the
estimand verbatim (e.g. "Developmental Idealism and Fertility Preferences in Nepal"); route such a
record normally but set `outcome_level` to `NA` unless the title also names the outcome level. In every
other abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a
substantive cell for a record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is FDT and SDT, and the FDT cell is the *diffused* transition only** — societies
entering fertility transition after roughly 1945 under exposure to an external modern model. A study of
the historical Western transition (Europe or North America, roughly 1870–1930) is NOT a case of
westernization; there was no external West to import from. Route such papers `OFF_OTHER` unless they are
theory about the source of the diffused package, which is `DI_THEORY`. There is no pre-modern cell.

## THE SIX LOAD-BEARING BOUNDARY WALLS

The single most common error in this screen will be admitting a paper because it *mentions* modernization,
westernization, or Caldwell. **Judge the estimand, not the framing sentence.**

**Wall 1 — vs C.3.f (intergenerational wealth flows).** Both are Caldwell and share his vocabulary. If
the operative variable is a *flow* — child labour contribution, remittances to parents, old-age support,
transfers between generations, the NTA lifecycle deficit — it is `OFF_WEALTH_FLOWS_C3f`, **even when the
abstract cites Caldwell's cultural argument.** D.1.b's operative variable is a belief, an ideal, or
exposure to an external family model. HARD line.

**Wall 2 — vs D.1.a (postmaterialism).** Internal versus imported. D.1.a is value change endogenous to
affluence in an already-modernized society, with *self*-oriented content: autonomy, self-realization,
freedom from obligation. D.1.b is a *family form* arriving from an identified external reference point.
Individualism and childlessness in Northern Europe is `OFF_POSTMATERIALIST_D1a`. The conjugal-nuclear
ideal spreading in rural Nepal is D.1.b.

*Migrant seam.* Migrant fertility converging on host norms is D.1.b when the estimand is convergence
**with exposure** (duration, generation, host-language acquisition, enclave density). It is `OFF_OTHER`
(routing to A.19) when the estimand is **persistence of origin-country norms** net of environment.

**Wall 3 — vs A.20 (diffusion channels) and A.3 (diffusion of fertility control).** Ask what the
treatment delivers.
- Contraceptive knowledge, availability, or legitimation → `OFF_FERTILITY_CONTROL_A3`.
- A channel whose content is unspecified, or an estimand about the *geometry* of spread — network
  position, distance, linguistic or religious boundaries, media reach as such → `OFF_DIFFUSION_CHANNEL_A20`.
- Depiction of or instruction in a modern family model, with the effect attributed to that aspirational
  content → D.1.b.

*Dual-home rule, confined to this wall.* Media studies (television serials, novelas, cable, radio drama)
where both readings are live take `PRIMARY_MEDIA_WESTERN_MODEL` and set `shared_with: "A.20"`. Use the
shared tag rather than agonizing over exclusivity; downstream assembly handles it.

**Wall 4 — vs D.2.a (female empowerment) and C.2.e (female wage).** Gender equality is *inside* the
developmental-idealism package, so without this wall D.1.b swallows the female-education literature.
Ask *whose* belief is doing the work, and about what. A woman's own autonomy, bargaining position, or
aspiration → `OFF_FEMALE_AUTONOMY_D2a`. The price of her time → `OFF_SCHOOLING_ECONOMIC`. A shared
belief about what modern families look like, held across the community, is D.1.b — including DI
instruments whose every item concerns marriage age or women's work.

**Wall 5 — vs C.3.b (compulsory schooling and child labour), and the human-capital reading of
education.** Same treatment, different mechanism.
- Schooling acting through cost or return, with the mechanism identified → `OFF_SCHOOLING_ECONOMIC`.
- Schooling where the design isolates ideational content — curriculum variation, mission or colonial
  schooling, effects net of literacy and wage returns, spillovers onto people whose own schooling did
  not change → `PRIMARY_SCHOOLING_IDEATIONAL`.
- **Schooling or education → fertility with no mechanism decomposition visible → `MECHANISM_UNRESOLVED_SCHOOLING`,
  verdict `UNCERTAIN`.** This will be a large class. Do not resolve it toward D.1.b. An abstract almost
  never shows a mechanism decomposition, so when in doubt this is the cell.

**Wall 6 — vs D.1.c (cultural evolution).** A formally modelled prestige- or status-biased transmission
process is `OFF_CULTURAL_EVOLUTION_D1c`, even when the copied behaviour is Western. D.1.b's exposure
variable is contact with, or belief about, an external modern society.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_DI_BELIEF | PRIMARY_SCHOOLING_IDEATIONAL | PRIMARY_MEDIA_WESTERN_MODEL | PRIMARY_WESTERN_CONTACT | DIFFUSION_INDEPENDENT_OF_STRUCTURE | DI_THEORY | MECHANISM_UNRESOLVED_SCHOOLING | OFF_WEALTH_FLOWS_C3f | OFF_POSTMATERIALIST_D1a | OFF_DIFFUSION_CHANNEL_A20 | OFF_FERTILITY_CONTROL_A3 | OFF_FEMALE_AUTONOMY_D2a | OFF_SCHOOLING_ECONOMIC | OFF_CULTURAL_EVOLUTION_D1c | OFF_OTHER | OFF_OUTCOME | REVERSE | INSUFFICIENT_INFO | NA",
  "outcome_level": "REALIZED_FERTILITY | STATED_INTENTION_OR_IDEAL | FAMILY_FORMATION_BEHAVIOUR | MULTIPLE | NA",
  "shared_with": "A.20 | none",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "structural_change_held_fixed": "yes | no | unclear",
  "setting_era": "DIFFUSED_FDT | SDT | HISTORICAL_WESTERN_FDT | NA",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: estimates or models exposure to an external model of the modern family as a determinant of
  fertility, fertility intentions, or family-formation behaviour. **`RELEVANT` ALSO covers `DI_THEORY`** —
  see the note below.
- `UNCERTAIN`: plausibly belongs, but missing or ambiguous information prevents confident routing. This
  is the correct verdict for `MECHANISM_UNRESOLVED_SCHOOLING` and `INSUFFICIENT_INFO`.
- `NOT_RELEVANT`: does not bear on **this chapter's** estimand. General modernization narratives,
  general fertility-decline descriptions, and cross-national correlations of development indices with
  TFR are NOT automatically relevant.

**A verdict and a cell answer two different questions, and every `OFF_*` paper needs both.** The
verdict says whether the paper belongs to D.1.b. The cell says where it *does* belong. So:

- **Every `OFF_*` cell takes `NOT_RELEVANT`** — the paper is out of this chapter — **while keeping its
  routing label**, which is how the sibling chapter gets it. `NOT_RELEVANT` + `OFF_WEALTH_FLOWS_C3f`
  is the correct and expected disposition for a wealth-flows paper, and it is not a contradiction.
- **`NA` is only for papers with nowhere to go** — contentless records, and papers on some unrelated
  topic entirely. `NA` always pairs with `NOT_RELEVANT`, but the reverse does not hold.
- `REVERSE` likewise takes `NOT_RELEVANT` unless the paper also carries a forward fertility estimand.

Use `NA` only when no `OFF_*` cell fits. Reaching for `NA` when a routing label applies throws away
the routing information this screen exists to produce.

**The theory stream takes `RELEVANT`.** `DI_THEORY` papers have no fertility estimand by definition, but
they are preserved deliberately and are therefore `RELEVANT`, not `NOT_RELEVANT`. They are separated
downstream and do not count toward empirical recall, so marking them `RELEVANT` cannot inflate any pooled
estimate. This is stated explicitly because it was the largest source of screener disagreement in the
D.3.b pilot — do not resolve it by your own judgment.

## Estimand cells

- `PRIMARY_DI_BELIEF`: measured beliefs that development brings or requires small families, late marriage,
  nuclear residence, or gender equality — Thornton-style developmental-idealism instruments, or any
  survey measure of what respondents think modern or developed societies do about family — as a
  determinant of fertility, intentions, or ideals.
- `PRIMARY_SCHOOLING_IDEATIONAL`: schooling exposure where the design isolates ideational content from
  wage and child-cost returns (see Wall 5).
- `PRIMARY_MEDIA_WESTERN_MODEL`: exposure to media carrying modern-family depictions — television
  serials, novelas, cable, radio drama, film, internet — where the effect is attributed to the depicted
  family model. Set `shared_with: "A.20"` when the channel reading is equally live.
- `PRIMARY_WESTERN_CONTACT`: direct contact with Western institutions or populations — missions, colonial
  administration and its schools, development programmes, return migration, foreign employment, tourism —
  as a determinant of fertility.
- `DIFFUSION_INDEPENDENT_OF_STRUCTURE`: any of the above where the design shows the ideational effect
  **net of, or in the absence of, structural economic change** — income, urbanization, mortality, women's
  employment, or contraceptive access held fixed, or a setting where those did not move. This is the
  value-added cell. Use it in preference to the four PRIMARY cells whenever the design actually separates
  ideation from structure. It requires the DESIGN to do so, not merely an author's claim in the discussion.
- `DI_THEORY`: Caldwell's and Thornton's theoretical statements, developmental-idealism conceptual work,
  world-society and world-polity theory, and modernization-theory critique, with no empirical fertility
  estimate.
- `MECHANISM_UNRESOLVED_SCHOOLING`: education or schooling → fertility with no mechanism decomposition.
  Takes `UNCERTAIN`. Large class by design; see Wall 5.
- `OFF_WEALTH_FLOWS_C3f`: net intergenerational transfers, child labour contribution, old-age support,
  NTA lifecycle deficit. Route to C.3.f (Wall 1).
- `OFF_POSTMATERIALIST_D1a`: internal value change in an already-modernized society, self-oriented
  content. Route to D.1.a (Wall 2).
- `OFF_DIFFUSION_CHANNEL_A20`: the geometry of the diffusion channel with content unspecified. Route to
  A.20 (Wall 3).
- `OFF_FERTILITY_CONTROL_A3`: contraceptive knowledge, availability, or legitimation as what diffuses.
  Route to A.3 (Wall 3).
- `OFF_FEMALE_AUTONOMY_D2a`: women's own autonomy, bargaining power, or aspiration as the operative
  variable. Route to D.2.a (Wall 4).
- `OFF_SCHOOLING_ECONOMIC`: schooling or female wage acting through cost, return, or opportunity cost,
  with the mechanism identified. Route to C.3.b / C.2.e (Wall 5).
- `OFF_CULTURAL_EVOLUTION_D1c`: formally modelled prestige- or status-biased transmission. Route to
  D.1.c (Wall 6).
- `OFF_OTHER`: a non-D.1.b determinant of fertility with no sibling home — and the home for historical
  Western FDT studies and for origin-norm-persistence migrant designs. Use this rather than forcing a
  paper into a named router.
- `OFF_OUTCOME`: developmental-idealism beliefs or Western exposure → a non-family outcome (political
  attitudes, consumption, health, migration). Mechanism or context only.
- `REVERSE`: fertility or family status → developmental-idealism beliefs. Takes `NOT_RELEVANT` unless it
  also carries a fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both an ideational-exposure mechanism AND a fertility, intention, or family-formation outcome must be
   present for a PRIMARY or `DIFFUSION_INDEPENDENT_OF_STRUCTURE` cell.
2. `outcome_level` is mandatory on every RELEVANT empirical paper. Births, parity, and completed family
   size are `REALIZED_FERTILITY`. Intentions, desires, and ideal or desired family size are
   `STATED_INTENTION_OR_IDEAL`. Age at marriage, spouse choice, marriage arrangement, and nuclear
   residence are `FAMILY_FORMATION_BEHAVIOUR` — in scope, because the package is a claim about the whole
   family form, and never pooled with births. Use `NA` for theory and `NOT_RELEVANT` records and for any
   `UNCERTAIN` record whose level you cannot determine. Never guess a level to satisfy the field.
3. **A cross-national correlation between a development index (GDP, HDI, urbanization) and TFR is not
   this hypothesis.** It is the structural claim D.1.b is defined against. `NOT_RELEVANT` / `NA` unless
   the exposure is a measured belief or a measured contact.
4. Do not promote an OFF-cell paper to PRIMARY merely because westernization, modernization, or Caldwell
   is mentioned as motivation. Conversely, do not demote a paper with a genuine ideational estimand
   merely because it also reports economic covariates.
5. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate, so the cell need not be distorted to keep them out.
6. Set `structural_change_held_fixed=yes` only when the design actually adjusts for or eliminates
   structural economic variation, not when the author merely asserts the effect is cultural. This clause
   is the hypothesis's value-added claim; an author's assertion is not a design.
7. `setting_era` is mandatory on every RELEVANT empirical paper, because the FDT restriction is enforced
   on it. A study whose setting is a post-1945 transitional society is `DIFFUSED_FDT`; a low-fertility or
   post-transitional society is `SDT`; historical Europe or North America is `HISTORICAL_WESTERN_FDT` and
   routes to `OFF_OTHER`.
8. Anthropological and ethnographic accounts of family change under Western contact, with no estimate,
   are `DI_THEORY` when they argue the mechanism and `OFF_OUTCOME` when they describe something else.
   Do not give them a PRIMARY cell for want of anywhere better.
9. Contentless records — prefaces, front matter, tables of contents, editorial notes — are
   `NOT_RELEVANT` / `NA`, not `UNCERTAIN`. They carry no estimand to be uncertain about.
10. Papers about "modernization theory" as intellectual history, with no fertility estimand and no
    developmental-idealism mechanism, are `NOT_RELEVANT`, not `DI_THEORY`. The theory cell is for the
    canon this chapter's mechanism rests on, not for the history of a discipline.
