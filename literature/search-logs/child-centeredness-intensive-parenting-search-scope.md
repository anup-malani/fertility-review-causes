# Search scope — child-centered intensive parenting norms

**Hypothesis:** D.2.d (HYPOTHESES-v5.md)
**Hypothesis slug:** `child-centeredness-intensive-parenting`
**Target phenomenon:** Second Demographic Transition (SDT) only for the pooled synthesis; the FDT-era
sentimentalization literature is preserved as context and never pooled — see "Phenomenon scope".
**Ticket:** TICK-064
**Status:** **DRAFT** (Shravan, 2026-08-08). Six boundary walls specified, three scope calls raised
with recommendations (§ "Scope calls"). Anchors not yet sourced. Not yet frozen; walls freeze after the
PI answers Call 1 and Call 2, or after a decision to proceed on the recommendations. Anchor sourcing
(A3) is **not** blocked by the freeze.

Built on the D.3.b (`climate-anxiety-eco-doomerism`) template, which is the run this chapter mirrors.
Two lessons from that run are carried forward as design constraints rather than discovered again:
the taxonomy needs `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER` from the start (D.3.b's wave-1
audit, defects 2 and 3), and a wall whose discriminator is invisible in a title/abstract cannot be
enforced by the screen and must be declared unenforceable up front rather than trusted and later
audited (D.3.b Wall 1).

## Causal claim

The prevailing normative standard of what a parent owes a child has shifted — from children growing up
alongside an adult household to a standard under which good parenting means sustained attention,
deliberate enrichment, supervision, and emotional labor. Where that standard is held, each child costs
far more time and psychological effort, and parents who have internalized it conclude they can only
meet it for a small number of children. Desired and then realized fertility fall.

The distinguishing feature, and the whole difficulty of this chapter, is the claim's position in the
causal chain. D.2.d does not claim that children became more expensive; C.2.b claims that. It does not
claim that the return to investing in a child rose; C.3.d claims that. It claims that **the normative
standard itself moved, and would have raised the cost per child even holding prices, wages, and returns
to child human capital fixed.** The norm is the root cause; its effect travels through a cost channel
that three economic hypotheses in this review already own. HYPOTHESES-v5 says exactly this in the D.2.d
notes field, and it is why routing, not retrieval, is the central task here.

## Phenomenon scope

**PM: no cell.** The mechanism requires a diffused normative standard of intensive parental investment.
No such standard is documented for pre-modern populations, and the pre-modern variation in parental
investment that does exist is filed at C.3.a (mode of production and child economic value).

**SDT: the primary and only pooled cell.** The measurable phenomenon — rising parental childcare time
per child despite falling family size, the concerted-cultivation standard, the intensive-mothering
ideology — is documented from roughly 1965 onward in time-use series and from the 1990s onward in
attitude measures. This is where the estimates are.

**FDT: context stream only, not pooled.** See Call 1 below. The sentimentalization-of-childhood
literature (Zelizer, Ariès, Shorter, Stone) describes the same mechanism — a normative revaluation of
the child that raises investment per child — displaced roughly a century. It is captured under
`FDT_SENTIMENTALIZATION_CONTEXT`, discussed in the chapter's history section, and kept out of the SDT
recall denominator and out of every pool.

## The six boundary walls

D.2.d borders four economic hypotheses that share its outcome, its cost channel, and much of its
vocabulary, plus two cultural ones. The walls below all reduce to one question, asked six ways:
**what does the estimate actually vary?** A paper routes on its source of variation, not on its
framing, and not on whose theory it cites.

**Wall 1 — D.2.d vs C.3.d (Quantity-Quality Tradeoff, `quantity-quality-tradeoff`).** The sharpest,
because Q-Q is the economics of exactly this substitution and has a fifty-year head start on
vocabulary.
- **C.3.d asks:** given a rise in the *return* to child human capital, do parents substitute quality
  for quantity? The operative variable is a price or a return — skill premia, returns to schooling,
  technology shocks.
- **D.2.d asks:** does a shift in the *normative standard* of adequate parenting reduce fertility,
  whether or not any return has moved?
- **Discriminator:** a study whose identifying variation is in returns to skill, schooling returns, or
  the price of quality routes to `OFF_QQ_C3d` **even when it is framed as being about parenting
  intensity or parenting style.** D.2.d claims the estimate only when what moves is the standard, the
  norm, or exposure to it.

**Wall 2 — D.2.d vs C.2.f (Inequality and Status Competition, `rising-inequality-and-status-competition`).**
The two are defined into near-duplication by v5: C.2.f's own notes say "the status competition norm is
Cultural; the mechanism through which it reduces fertility is cost," and its cross-ref names D.2.d as
"the norm driving competition." A hard line is required or both chapters will claim the same papers.
- **C.2.f asks:** does rising *inequality* raise required investment per child and lower fertility?
  Operative variable: an inequality measure, a relative-position measure, or a status-competition
  shock.
- **D.2.d asks:** does the parenting standard reduce fertility, holding the inequality that may have
  produced it fixed?
- **Discriminator:** variation in inequality, relative rank, or local status pressure → `OFF_INEQUALITY_C2f`.
  Variation in the parenting norm, standard, or an individual's endorsement of it → D.2.d. **The
  Doepke–Zilibotti framework is a joint claim spanning both** (inequality and returns cause the
  parenting style, which reduces fertility); a Doepke–Zilibotti-style paper routes to D.2.d only when
  the estimate isolates the parenting-style link separately from the inequality shock that drives it.
  This is Call 2.

**Wall 3 — D.2.d vs C.2.b (Rising Direct Costs of Children, `child-cost-direct`).**
- **C.2.b asks:** does rising out-of-pocket expenditure per child — tuition, health, enrichment
  spending, the goods a child consumes — lower fertility? The operative variable is money.
- **D.2.d asks** about the standard that decides what must be bought and, more centrally, what must be
  *done*: time, attention, and emotional labor.
- **Discriminator:** measured expenditure per child, cost-of-raising-a-child estimates, and price
  indices route to `OFF_DIRECT_COST_C2b`. Measured parental time, supervision, enrichment
  *activity*, or endorsement of a parenting standard is D.2.d. The two are genuinely entangled — v5's
  C.2.b notes already concede that separating direct cost from quality-investment cost is an
  identification problem — so a paper that measures only a money aggregate goes to C.2.b even when its
  narrative is about intensive parenting.

**Wall 4 — D.2.d vs C.2.e (Female Wage and Opportunity Cost of Time, `female-wage-opportunity-cost`).**
Intensive parenting is time-intensive, and the time is disproportionately the mother's, so the two
hypotheses predict correlated things through the same input.
- **C.2.e asks:** does a rise in the *price* of the mother's time raise the effective price of a child?
  Operative variable: a wage.
- **D.2.d asks:** does a rise in the *quantity of time the norm demands* raise the effective price of a
  child, at a fixed wage?
- **Discriminator:** wage variation, labor-demand shocks, and returns-to-female-labor variation route
  to `OFF_TIMECOST_C2e`. Variation in required or actual caregiving hours per child, at fixed wages, is
  D.2.d.

**Wall 5 — D.2.d vs C.2.a (Childcare Cost and Availability, `childcare-availability-cost`).**
Part of D.2.d's content is that the norm designates *parental* care as non-substitutable — that
outsourced care does not discharge the obligation. That claim is D.2.d's; the price and supply of
childcare are C.2.a's.
- **Discriminator:** variation in childcare price, subsidy, or supply → `OFF_CHILDCARE_C2a`. A study of
  whether parents believe non-parental care is adequate, or of norms about maternal employment and
  child wellbeing, is D.2.d.

**Wall 6 — D.2.d vs D.2.a (Female Empowerment and Gender Equity, `female-empowerment-gender-equity`).**
Intensive-mothering ideology is a gendered norm, and D.2.a already owns the double-burden argument in
its gender-revolution form.
- **D.2.a asks:** does the distribution of domestic and care work *between partners*, or a norm about
  women's roles, affect fertility?
- **D.2.d asks:** does the *total* standard of care a child is owed affect fertility, irrespective of
  who supplies it?
- **Discriminator:** a study whose variation is in gender-role attitudes, the division of housework, or
  partner care-sharing routes to `OFF_GENDER_D2a`. A study whose variation is in the level of care a
  child is held to require is D.2.d. Papers on intensive *mothering* specifically will often straddle;
  route on which term the design varies, and where neither is isolated use `MIXED_NORM_UNRESOLVED`.

## What the title/abstract screen can and cannot enforce

This is carried forward from D.3.b, where the screen was trusted to enforce a wall it structurally
could not, and the RA gate had to sample 50 misroutes to find out. Every wall above discriminates on
the estimate's **source of variation**, which is frequently absent from an abstract.

| Wall | Enforceable at title/abstract? | Why |
|---|---|---|
| 1 (C.3.d) | **No** | Returns-to-skill variation vs. norm variation is a design fact, usually stated only in the methods section. |
| 2 (C.2.f) | **No** | Whether the parenting-style link is isolated from the inequality shock is invisible in an abstract. |
| 3 (C.2.b) | Partly | The measured object (money vs. time) is usually named in the abstract. |
| 4 (C.2.e) | Partly | "Wage" and "maternal employment" are usually named; "hours per child at fixed wages" is not. |
| 5 (C.2.a) | **Yes** | Childcare price/subsidy/supply is a named intervention. |
| 6 (D.2.a) | **No** | Gender-role variation vs. care-level variation is a design fact. |

**Consequence, pre-committed rather than discovered:** the screen assigns a *provisional* cell, and
four of the six walls are adjudicated at full text, not at screening. Any record whose routing turns on
Wall 1, 2, or 6 and whose abstract does not name the source of variation takes
`ROUTING_DEFERRED_TO_FULLTEXT` rather than a substantive `OFF_*` cell. This costs retrieval volume and
is worth it: an `OFF_*` label assigned on an abstract that could not support it is a silent
false-negative, and on this hypothesis the `OFF_*` cells are where most of the corpus will land.

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_NORM_EXPOSURE` | Exposure to, or internalization of, an intensive / child-centered parenting norm | Reduced fertility intention or realized fertility | Primary synthesis |
| `PRIMARY_TIME_INTENSITY` | Measured parental time, supervision, or enrichment activity required or supplied per child | Reduced fertility intention or realized fertility | Primary synthesis |
| `PRIMARY_PERCEIVED_STANDARD` | Perceived standard of adequate parenting — what respondents believe a child is owed | Reduced fertility intention or realized fertility | Primary synthesis |
| `COST_INDEPENDENCE` | Any of the above, where the design holds money price, wages, **and** returns to child human capital fixed | Fertility falls attributable to the norm alone | Primary / bridge — **the value-added cell**; this is what separates D.2.d from C.2.b, C.2.f, and C.3.d |
| `PARENTING_NORM_CONSTRUCT` | Intensive parenting / concerted cultivation / intensive mothering as the **object** of study — construct development, scale validation, prevalence, trends, class gradients | No fertility outcome | Theory stream |
| `PARENTING_NORM_THEORY` | Normative, historical, or theoretical argument about child-centeredness and family size | No empirical fertility estimate | Theory stream |
| `FDT_SENTIMENTALIZATION_CONTEXT` | Historical revaluation of the child (sentimentalization, "priceless child", invention of childhood) in the FDT era | Any | Context stream; never pooled — see Call 1 |
| `OFF_QQ_C3d` | Returns to child human capital, skill premia, price of quality | Fertility | Route to C.3.d |
| `OFF_INEQUALITY_C2f` | Income inequality, relative position, status-competition shock | Fertility | Route to C.2.f |
| `OFF_DIRECT_COST_C2b` | Money expenditure per child | Fertility | Route to C.2.b |
| `OFF_TIMECOST_C2e` | Female wage, labor-demand shock, price of maternal time | Fertility | Route to C.2.e |
| `OFF_CHILDCARE_C2a` | Childcare price, subsidy, or supply | Fertility | Route to C.2.a |
| `OFF_GENDER_D2a` | Gender-role attitudes, division of domestic labor, partner care-sharing | Fertility | Route to D.2.a |
| `MIXED_NORM_UNRESOLVED` | Parenting-norm and gender-norm variation present, neither isolated | Fertility | Held; adjudicated at full text |
| `ROUTING_DEFERRED_TO_FULLTEXT` | Routing turns on Wall 1, 2, or 6 and the abstract does not name the source of variation | Fertility | Held; adjudicated at full text |
| `OFF_OTHER` | Non-D.2.d determinant with no sibling-hypothesis home | Fertility | Route out; no sibling queue |
| `OFF_OUTCOME` | Parenting intensity / style as a determinant of some **other** non-fertility outcome — child development, attainment, parental wellbeing, maternal mental health | No fertility outcome | Mechanism / context only |
| `REVERSE` | Family size or parity affecting parenting intensity per child | Parenting-intensity outcome | Context — and see the identification caution, where this is the central threat |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

`INSUFFICIENT_INFO`, `OFF_OTHER`, and the split of theory into two cells are present from v1 of this
taxonomy rather than added after a wave-1 audit; they are D.3.b's three approved amendments, inherited.
Both theory cells and the FDT context cell carry verdict `RELEVANT` and are separated downstream — they
do **not** count toward empirical recall.

## The realized-vs-intended level tag (not a routing cell, but mandatory)

Every included empirical paper carries an outcome-level tag: `STATED_INTENTION_OR_ATTITUDE` (desired
family size, ideal number of children, reproductive intention, "I could not do this again") versus
`REALIZED_FERTILITY` (completed or observed parity). Both are in scope.

**Synthesis rule:** stated-intention outcomes are retained as a first-class part of the primary
synthesis and are not relegated to context, but every estimate, figure, and pooled number built on them
carries the standing caveat that it measures stated intention. A realized-fertility pool is reported
separately where the evidence exists. **The two levels are never combined into one pooled estimate.**
This is the D.3.b rule, unchanged.

## Eligibility rules

- Include empirical studies only where the estimate bears on **a parenting norm, standard, or measured
  parenting intensity → fertility intention or behavior.** Parenting-intensity studies with a
  non-fertility outcome are `OFF_OUTCOME` and are context, however central to the parenting literature.
- The intensive-parenting canon that has no fertility outcome — Hays-style ideology work, concerted-
  cultivation ethnography, parenting-attitude scale validation, time-use trend description — seeds the
  **theory** stream and does not count toward empirical recall.
- Phenomenon is **SDT** for everything pooled. FDT-era sentimentalization material is retained under
  `FDT_SENTIMENTALIZATION_CONTEXT` and reported in the chapter's history section only. No PM cell.
- A study identifying the effect off returns to skill, inequality, money expenditure, female wages,
  childcare prices, or gender-role attitudes routes to C.3.d / C.2.f / C.2.b / C.2.e / C.2.a / D.2.a
  respectively, **even when its framing is entirely about parenting norms.**
- Where the abstract cannot support the routing call, defer rather than guess — `ROUTING_DEFERRED_TO_FULLTEXT`.
- Maternal education, income, and social class are **recorded on every included empirical paper** as
  candidate confounders: they predict both endorsement of intensive-parenting standards and low
  fertility.
- Keep theory, context, and off-cell papers discoverable but outside the empirical primary-cell recall
  denominator.

## When to adjudicate mechanisms

The title/abstract screen decides only which stream a paper belongs to, and — given the enforceability
table above — is not asked to determine the source of identifying variation from an abstract. Mechanism
coding happens at full-text extraction, before synthesis.

For every included empirical paper, full-text extraction must record:

- `NORM_MEASURE` — what was actually measured: an attitude scale, a time-use quantity, a perceived
  social standard, a policy or media exposure, or an inferred norm with no direct measure;
- `VARIATION_SOURCE` — what generates the identifying variation, in the authors' own terms; this is the
  field that settles Walls 1, 2, 4, and 6, and it is the reason those walls are deferred to full text;
- `HELD_FIXED` — which of {money price per child, wages/time price, returns to child human capital,
  childcare price, gender-role attitudes} the design actually holds fixed. `COST_INDEPENDENCE` requires
  the first three;
- `DIRECTION_ESTABLISHED` — how, if at all, the design rules out reverse causation from parity to
  parenting intensity;
- outcome level (stated intention/attitude vs. realized fertility);
- the candidate confounder set actually adjusted for.

Drafting may report only mechanisms these fields support. A cross-sectional correlation between
endorsement of intensive-parenting attitudes and low fertility intention, adjusting for none of the
confounders and establishing no direction, may document the association — it must not be described as
evidence that the norm *causes* the fertility reduction.

## The identification caution: reverse causation is the first-order threat

On D.3.b the central threat was a confound (the D.1.a value shift predicting both climate concern and
low fertility). Here the central threat is **reverse causation, and it is partly mechanical.** Parental
time and attention per child are a quantity divided by the number of children. A parent of one child
supplies more hours per child than a parent of four almost by construction, and can more easily meet
any intensive standard. So:

1. Any cross-sectional association between parenting intensity per child and low fertility is
   contaminated by an arithmetic identity, before any behavioral story is told.
2. Selection compounds it: people who intend few children may adopt the intensive standard *because*
   they have the slack for it, exactly inverting the claimed direction.
3. A norm-endorsement measure is less mechanically contaminated than a time-use measure, but is
   vulnerable to post-hoc rationalization — parents justify the family size they have.

Designs that can survive this are those with variation in the norm that is external to the parent's own
fertility: cohort or period shifts in the standard, media or policy exposure, migration between norm
regimes, or sibling/twin designs holding family resources fixed. `DIRECTION_ESTABLISHED` exists to
record which, if any, a study achieves. **Expect few to achieve it.**

## Expected shape of the evidence (a caution, not a result)

D.2.d's canonical sources are ethnographic and theoretical. Hays (1996) and Lareau (2003) are
qualitative studies of parenting ideology with no fertility outcome. Doepke and Zilibotti (2019) is a
theoretical and descriptive account of parenting style whose fertility content is largely an
implication of the model. Ishizuka (2019) measures parenting standards, not births. Four consequences
to expect and to report honestly:

1. **`OFF_OUTCOME` will be the largest cell by a wide margin.** The intensive-parenting literature is
   overwhelmingly about child development, attainment, and parental — especially maternal — wellbeing.
   That is a fact about the literature and not a screening defect.
2. **Cold-start channel 1 (prior meta-analyses and systematic-review included-study lists) is likely
   near-empty** for the norm → fertility estimand, while being rich for parenting style → child
   outcomes. A near-empty channel 1 is itself a finding.
3. **The `COST_INDEPENDENCE` cell may be empty or close to it.** Isolating the norm from money price,
   time price, and returns to human capital simultaneously is a demanding design, and the economics
   literature has had little reason to attempt it — its interest is in the prices. If that cell comes
   back empty, the honest chapter finding is that the *distinctively cultural* content of D.2.d is
   substantially untested, and that the evidence usually offered for it is evidence for C.2.b, C.2.f,
   or C.3.d. This should be stated, not papered over with a pooled estimate assembled from studies that
   identify off prices.
4. **The realized-fertility pool will be thinner than the stated-intention pool**, as on D.3.b, though
   less extremely: time-use and parity data coexist in several panel surveys.

## Cold-start channels and leakage wall

1. Direct empirical papers estimating a parenting norm, standard, or measured parenting intensity →
   fertility intention or behavior, identified independently of the hypothesis list, seed the empirical
   Tier-A candidate set.
2. Parenting-ideology theory, concerted-cultivation ethnography, and parenting-standard psychometrics
   seed the theory set and do not count toward empirical recall.
3. References and citations of the independent seeds create the orthogonal Tier-B candidate frame.
4. Production-query terms will not be mined from a paper and then evaluated on that same paper; learned
   extensions must be fold-local after the gold frame exists.

## Pre-query anchor audit (not yet built)

The verified candidate anchor set will be stored in
`child-centeredness-intensive-parenting-cold-start-anchors.json`. Two gates apply, both mandatory:

- **Existence gate** (OAS, 2026-07-08): a live DOI, or a Crossref/publisher record confirming the title
  exists. No anchor is hand-asserted from memory.
- **Version-of-record gate** (D.1.b, 2026-08-07 — `decisions/2026-08-07-version-of-record-gate.md`):
  an anchor that resolves to a working paper, preprint, reprint, review *of* the work, or a single
  chapter of the volume meant is a **failure**, even though it passes the existence gate at title
  Jaccard 1.0. This gate is especially load-bearing here, because D.2.d's canon is **books** — Hays
  1996, Lareau 2003, Doepke and Zilibotti 2019 — and monographs resolve to reviews, editions, and
  chapters far more readily than articles do.

The set will deliberately contain norm-exposure, time-intensity, perceived-standard, theory, FDT-context,
and off-cell (C.3.d / C.2.f / C.2.b / C.2.e / C.2.a / D.2.a) decoy anchors, so the eventual search is
tested on routing as well as on topical retrieval. Given the enforceability table, the decoys are the
more important half: a search that retrieves the parenting literature is easy, and a screen that routes
it correctly is the whole problem.

## Scope calls for the PI

**Call 1 — the FDT sentimentalization literature. Recommended: context stream, not a pooled cell.**
v5 assigns D.2.d to SDT alone. But Zelizer's *Pricing the Priceless Child* (1985) documents a normative
revaluation of the child between roughly 1870 and 1930 — from economically useful to emotionally
priceless — which is D.2.d's mechanism displaced a century, and Ariès, Shorter, and Stone make adjacent
claims. Three options were considered:
- *(a) Recommended.* SDT-only for everything pooled; the FDT material is retained under
  `FDT_SENTIMENTALIZATION_CONTEXT`, discussed in the chapter's history section, excluded from the recall
  denominator and from every pool. Rationale: the FDT-era shift in the child's economic role is already
  owned by C.3.a (mode of production and child economic value) and C.3.b (child labor restrictions and
  compulsory schooling, Alexandra's run), so a pooled FDT cell duplicates two live chapters; but
  dropping Zelizer entirely loses the only historical evidence that this norm *moves*, which is
  material to the SDT claim's plausibility.
- *(b)* Open a full FDT cell. Rejected: duplicates C.3.a and C.3.b, and hands this chapter a large
  historical corpus whose fertility estimates are not identified.
- *(c)* Strict SDT-only, Zelizer routed to `OFF_OTHER`. Rejected: discards relevant evidence to keep a
  boundary tidy.

**Call 2 — Doepke–Zilibotti-type joint claims. Recommended: route on the isolated link, and accept a
small D.2.d.** The framework holds that inequality and returns to education cause the intensive
parenting style, which reduces fertility. It is simultaneously C.2.f, C.3.d, and D.2.d. Recommendation:
D.2.d claims the estimate only where the parenting-style link is identified separately from the
inequality or returns shock that drives it; otherwise the paper routes to C.2.f or C.3.d with a
cross-reference. The consequence, stated in advance so it is not read later as a search failure, is
that D.2.d may be left with very few identified estimates and a chapter whose main finding is that the
norm channel is asserted more than it is tested — which is the correct finding if it is true. The
alternative, letting D.2.d claim every paper that mentions parenting style, would make this chapter and
C.2.f near-duplicates and would inflate both.

**Call 3 — the C.2.f boundary is a definitional problem in v5, not only a screening problem.** C.2.f's
notes already state that its norm is cultural and its mechanism is cost, which is D.2.d's entire
description of itself. Wall 2 above is a workable operational line, but the two entries should probably
be re-worded in v5 so the distinction is in the entries rather than only in this scope doc. Flagged for
TICK-001 (PI review of HYPOTHESES.md); does not block this run.

## Next step

A3 — source and dual-gate the cold-start anchors
(`source/build/goldset/103_d2d_cold_start_anchors.py`). Script numbering starts at **103**: 88 is the
highest on `main`, and D.1.b holds 95–102 on an unmerged branch.
