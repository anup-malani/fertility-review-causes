# Blinded title/abstract screening rubric — diffusion & social-learning of fertility control (A.3) — v1

## Review question

Does the paper bear on **A.3** — the claim that fertility control spreads as an *idea* (information
about, and the legitimation of, deliberately limiting births, together with the social learning of it)
through social, linguistic, and religious contact, so that adoption spreads faster and along different
lines than economic conditions alone would predict? A.3's parameter is the effect of **social exposure
or spatial/cultural diffusion of fertility control on its adoption**, net of the economic drivers
(category C), the underlying value shift (D.1), the contraceptive technology (A.2), and exogenous
program supply (A.5). Preserve the formal diffusion / social-learning theory canon and the Princeton
descriptive canon, but route them outside the empirical primary estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states
the estimand verbatim (e.g. "Interaction Diffusion and Fertility Transition in Costa Rica"); route such
a record normally but set `identification_of_diffusion` to `NA` unless the title also names the design.
In every other abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent
a substantive cell for a record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is FDT and SDT** — the historical European marital-fertility transition (~1870–1965)
and the contemporary LMIC / post-transition diffusion (~1965–present). There is NO pre-modern cell: the
mechanism presupposes an innovation that spreads. Do not create a PM cell.

## THE SIX LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs A.20 (Cultural Diffusion Mechanisms, the channels). THE load-bearing wall.** A.3 owns the
diffused *content* — the knowledge and legitimacy of fertility control, and the claim that this content
travels independent of economics. A.20 owns the *channels* — social networks, mass media (radio, TV,
soap operas), and linguistic/cultural community boundaries — "independent of the content of those
norms." The line is content vs. conduit, and it is subtle because A.3's content usually travels through
a network:
- A study in which a **social network / peer group / community is the medium carrying fertility-control
  knowledge or practice specifically**, and the estimand is that exposure to adopters raises one's own
  adoption of fertility control, is **A.3** (`PRIMARY_SOCIAL_EXPOSURE`). The object is fertility control.
- A study of a **content-agnostic channel** — the reach of **mass media** (TV/radio/soap-opera signal),
  or the effect of **network architecture / density on the timing or speed** of *any* norm's spread, or
  a **linguistic border treated as a transmission conduit** — routes to `OFF_CHANNEL_A20`, even when the
  outcome is fertility. Mass-media exposure studies are A.20 by default.
This is a HARD line. When a paper is a mass-media exposure study, route to A.20 regardless of outcome.

**Wall 2 — vs A.2 (Modern Contraceptive Technology and Diffusion).** Both invoke "diffusion." A.2 is the
spread of the physical *methods* (the Pill, IUD, sterilization) that lower the cost of control. A.3 is
the spread of the *idea and its legitimacy*, independent of any new method. A study identifying off the
arrival, cost, or access of a *technology* is `OFF_TECHNOLOGY_A2`.

**Wall 3 — vs A.6 (Reduction in Stigma Around Contraception/Abortion).** A.3 and A.6 share the word
*legitimation*. A.6 is the *level* of stigma / acceptability (a stock) enabling latent demand to be
realized. A.3 is the *spread* of that acceptability across social and cultural space (a flow). A study
identifying off *how acceptable* control is at a place and time is `OFF_STIGMA_LEVEL_A6`; a study
identifying off the *propagation* of acceptability from adopters to non-adopters is A.3
(`PRIMARY_LEGITIMATION_SPREAD`). Legitimation counts for A.3 only when it is the *diffusion* of
acceptability, not its level.

**Wall 4 — vs A.19 (Intergenerational Transmission of Fertility Preferences).** A.19 is *vertical*
transmission within the family — parents' fertility or preferences predicting their children's. A.3 is
*horizontal* social diffusion across peers, cohorts, and communities. A parent-to-child
preference-correlation study (including the epidemiological / country-of-ancestry design) is
`OFF_VERTICAL_A19`.

**Wall 5 — vs A.5 (Organized Family Planning Programs).** A.5 is *exogenous program supply* — a
government/NGO campaign pushing information and access. A.3 is *endogenous* social diffusion that would
occur through ordinary contact absent any program. A program-rollout estimate is `OFF_PROGRAM_A5`. But a
**program-induced diffusion spillover** — a campaign in one place raising adoption in an untreated
neighbour *through social contact* — is A.3 (`PRIMARY_SOCIAL_EXPOSURE`); the spillover is A.3's parameter
even though the shock is A.5's. This is the bridge cell.

**Wall 6 — vs D.1.a / D.1.b (the root cultural cause).** A.3 is proximate: it is the spread of the
control idea, "not what is being spread or why people adopt it." A paper explaining *why* desired family
size fell — a shift toward autonomy, secular authority, Westernization — is `OFF_VALUE_D1`. A.3 is *how*
the resulting practice spread.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_SOCIAL_EXPOSURE | PRIMARY_SPATIAL_DIFFUSION | PRIMARY_CULTURAL_BOUNDARY_CONTENT | PRIMARY_LEGITIMATION_SPREAD | DIFFUSION_THEORY | PRINCETON_CANON | OFF_CHANNEL_A20 | OFF_TECHNOLOGY_A2 | OFF_STIGMA_LEVEL_A6 | OFF_VERTICAL_A19 | OFF_PROGRAM_A5 | OFF_VALUE_D1 | OFF_OTHER | OFF_OUTCOME | REVERSE | INSUFFICIENT_INFO | NA",
  "diffusion_channel": "SOCIAL_NETWORK_PEER | SPATIAL_MIGRATION | CULTURAL_LINGUISTIC_RELIGIOUS | LEGITIMATION_KNOWLEDGE | MASS_MEDIA | NA",
  "outcome": "short phrase or n/a",
  "identification_of_diffusion": "SEPARATES_FROM_COMMON_SHOCK | DESCRIPTIVE_RESIDUAL_ONLY | unclear | NA",
  "evidence_type": "quasi-experimental | observational | structural | qualitative | historical | descriptive | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

**The verdict ↔ cell convention (read first — it is deterministic, do not use your own judgment).**
`RELEVANT` is reserved for papers that bear on **A.3's own** estimand — the four PRIMARY cells and the
two theory cells. A paper that instead routes to a **sibling wall** (any `OFF_*` cell) is
**`NOT_RELEVANT`**, and the `OFF_*` cell records *where it goes*: NOT_RELEVANT here means "excluded from
A.3," not "worthless." Use `UNCERTAIN` when you cannot decide between an A.3 cell and a wall, or when
information is missing. So:

- `RELEVANT` ⇒ cell is one of `PRIMARY_SOCIAL_EXPOSURE`, `PRIMARY_SPATIAL_DIFFUSION`,
  `PRIMARY_CULTURAL_BOUNDARY_CONTENT`, `PRIMARY_LEGITIMATION_SPREAD`, `DIFFUSION_THEORY`,
  `PRINCETON_CANON`. Nothing else.
- `NOT_RELEVANT` ⇒ cell is `NA` (no identifiable estimand — homonym, contentless, bears on none of A.3's
  cells or walls) OR an `OFF_*` routing cell (`OFF_CHANNEL_A20`, `OFF_TECHNOLOGY_A2`,
  `OFF_STIGMA_LEVEL_A6`, `OFF_VERTICAL_A19`, `OFF_PROGRAM_A5`, `OFF_VALUE_D1`, `OFF_OTHER`,
  `OFF_OUTCOME`, `REVERSE`).
- `UNCERTAIN` ⇒ any A.3 cell, any `OFF_*` cell, or `INSUFFICIENT_INFO` when the record is too thin to
  route.

Concretely: a mass-media (A.20) or Pill-access (A.2) paper is `NOT_RELEVANT` with the matching `OFF_*`
cell, **not** RELEVANT. A homonym or a contentless record is `NOT_RELEVANT` / `NA`.

**The two theory cells take `RELEVANT`.** `DIFFUSION_THEORY` and `PRINCETON_CANON` papers may carry no
own fertility estimate, but they are preserved deliberately (RELEVANT), separated downstream, and do
**not** count toward empirical recall — so marking them RELEVANT cannot inflate any pooled estimate.
This is explicit because the theory/empirical split is a common source of screener disagreement; do not
resolve it by your own judgment.

## Estimand cells

- `PRIMARY_SOCIAL_EXPOSURE`: exposure to prior adopters — peers, cohort/community adoption share, network
  position — raises one's own adoption of fertility control or lowers fertility. The medium is a social
  network but the diffused object is fertility control specifically (Wall 1).
- `PRIMARY_SPATIAL_DIFFUSION`: the spread of the fertility decline across regions/provinces over space
  and time, net of development indicators (the Princeton residual; migration-carried diffusion).
- `PRIMARY_CULTURAL_BOUNDARY_CONTENT`: clustering of the transition by language, religion, or culture,
  read as evidence the *idea* of control spread along cultural lines independent of economics.
- `PRIMARY_LEGITIMATION_SPREAD`: the spread of the acceptability or knowledge of fertility control
  (legitimation as a diffusing flow, not a stigma level — Wall 3).
- `DIFFUSION_THEORY`: formal diffusion / social-learning / ideational models (contagion models, the
  Cleland–Wilson ideational thesis, social-interaction theory) with no own fertility estimate.
- `PRINCETON_CANON`: European Fertility Project descriptive volumes and province studies; foundational.
  Empirical only where an identified estimate is actually present.
- `OFF_CHANNEL_A20`: a content-agnostic channel effect — mass-media reach, network-architecture-on-
  timing, a linguistic border as a transmission conduit. Route to A.20 (Wall 1).
- `OFF_TECHNOLOGY_A2`: arrival, cost, or access of a contraceptive *method*. Route to A.2 (Wall 2).
- `OFF_STIGMA_LEVEL_A6`: the *level* of stigma / acceptability of contraception or abortion. Route to
  A.6 (Wall 3).
- `OFF_VERTICAL_A19`: parent-to-child transmission of fertility or preferences, incl. the epidemiological
  country-of-ancestry design. Route to A.19 (Wall 4).
- `OFF_PROGRAM_A5`: exogenous family-planning program supply, with no diffusion-spillover estimand.
  Route to A.5 (Wall 5).
- `OFF_VALUE_D1`: the underlying value shift (postmaterialism, secularization, Westernization) as the
  driver of *why* family size fell. Route to D.1.a / D.1.b (Wall 6).
- `OFF_OTHER`: a non-A.3 determinant of fertility with no sibling-hypothesis home. Use this rather than
  forcing a paper into one of the named `OFF_*` routers.
- `OFF_OUTCOME`: diffusion / social learning as a determinant of some **other** non-fertility outcome
  (general technology adoption, health behaviour, voting), or fertility-control diffusion studied only
  for a non-fertility outcome. Mechanism or context only.
- `REVERSE`: fertility level or transition shaping network structure or information flow. Narrow by
  design; takes `NOT_RELEVANT` unless it also carries a diffusion→fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a diffusion / social-learning mechanism AND a fertility-control-adoption or fertility outcome
   must be present for a PRIMARY cell.
2. **The reflection / common-shock rule (A.3's key identification threat).** A raw spatial or peer
   correlation in which neighbours adopt together is equally consistent with genuine social diffusion
   and with a common economic or cultural shock hitting neighbours at once. Set
   `identification_of_diffusion=SEPARATES_FROM_COMMON_SHOCK` only when the design actually isolates
   social contagion from a common shock (e.g. an instrument for peer exposure, a network experiment, a
   migration/border discontinuity). A descriptive residual — "development does not explain the
   clustering, so it must be diffusion" — is `DESCRIPTIVE_RESIDUAL_ONLY`. Such a paper is still
   `RELEVANT` if it bears on the estimand; the tag records that it is not identified. Never upgrade a
   descriptive residual to an identified diffusion effect.
3. **Wall 1 is decided on medium vs. content.** A social-network study of fertility-control adoption is
   `PRIMARY_SOCIAL_EXPOSURE` (A.3). A mass-media exposure study, or a study whose estimand is the effect
   of network *density/architecture* on the *timing* of any norm, is `OFF_CHANNEL_A20`. When in doubt on
   a mass-media paper, route to A.20.
4. Do not promote an OFF-cell paper to PRIMARY merely because it mentions diffusion or social influence
   as motivation. Conversely, do not demote a genuine diffusion→fertility estimand merely because it
   also reports economic or program covariates.
5. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate, so the cell need not be distorted to keep them
   out. Never force a review into a theory cell merely to exclude it from pooling.
6. **Homonyms are `NOT_RELEVANT` / `NA`.** "Diffusion" in physics/chemistry/finance, "social learning"
   in machine learning or animal behaviour, "cultural transmission" in population genetics/biology, and
   "epidemic/contagion" of disease are out of scope unless the paper is genuinely about the spread of
   *fertility control*. Say which homonym in `reason`.
7. Contentless records — prefaces, front matter, tables of contents, editorial notes — are
   `NOT_RELEVANT` / `NA`, not `UNCERTAIN`. They carry no estimand to be uncertain about.
8. `diffusion_channel` is descriptive, not a router: it records the medium the paper studies so the
   A.3/A.20 seam can be audited downstream. `MASS_MEDIA` on a fertility outcome should co-occur with
   `estimand_cell=OFF_CHANNEL_A20` (Wall 1); a mismatch is a flag for RA review, not an error to hide.
9. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
   verbatim because they drive downstream pooling exclusion: use exactly `review` for ANY review,
   meta-analysis, or systematic review, and exactly `theory` for ANY purely theoretical or formal-model
   paper with no own estimate. For everything else give the closest of `quasi-experimental`,
   `observational`, `structural`, `qualitative`, `historical`, `descriptive`, `mechanism`, or `other` —
   or a short free-text phrase if none fits. Do not force a design into a wrong label to match the menu.
