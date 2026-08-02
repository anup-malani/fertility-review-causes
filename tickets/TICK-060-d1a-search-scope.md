# TICK-060: D.1.a search scope — postmaterialism, individualism, secularization
**Status:** open
**Assigned:** Shravan
**Parallel-safe:** yes (no file overlap with the live D.3.b, C.2.c, or A.10 work)
**Blocks:** D.1.a cold-start anchors, D.1.a query build (tickets not yet opened)
**Blocked by:** none
**Touches:** `literature/search-logs/postmaterialism-individualism-secularization-search-scope.md`, `tickets/QUEUE.md`

## Description

Open D.1.a (Postmaterialism, Individualism, and Secularization, slug
`postmaterialism-individualism-secularization`, SDT) at GACS Phase A1/A2, producing the same scope
artifact that opened D.3.b, A.10, and C.2.c.

D.1.a is the canonical SDT framework and the hardest causal-credibility case in the master list. Five
problems the scope has to settle before any search runs.

**1. The hypothesis is criticized as descriptive rather than causal, and the scope has to say what
would count as evidence.** The v5 `notes` field concedes it directly: "Criticized as descriptive
rather than causal and hard to separate from income/security mechanisms." Lesthaeghe and van de Kaa
document a bundle of changes that moved together across postwar Europe, which is a characterization of
the transition rather than an identified claim about one input to it. A GRADE rating needs an estimand
and a source of exogenous variation. If the scope cannot pre-register both, the honest outcome is a
theory-heavy chapter with a very low or no-evidence rating, and that verdict should be reachable by
design rather than discovered at extraction. Decide the admissible design classes up front.

**2. The entry absorbs five sub-claims measured five different ways, so a pooling rule is required.**
Per the v5 `notes`, D.1.a absorbs `secular-ideational-shift`, `individualism-rise`,
`secularization-religiosity-decline`, `childlessness-as-acceptable-choice`, and
`consumerism-aspirational-lifestyles`. Their measures are the Inglehart WVS postmaterialism battery,
religious affiliation and service attendance, individualism indices, attitudes toward voluntary
childlessness, and consumption-orientation scales. Those are distinct constructs with distinct
validity records, and an effect size on one is not exchangeable with an effect size on another.
Pooling them yields a number whose meaning depends on the measure mix in the sample, which is the same
structural defect the C.2.c tenure ruling identified. Treat the sub-claims as separate estimand
strata with a pre-registered rule on what may combine.

**3. Secularization is the stratum most likely to carry the chapter.** It is the one sub-claim with a
quantitative empirical literature that uses instruments and natural experiments rather than
contemporaneous correlation, so it can produce estimates the other four cannot. This is the same shape
as the C.2.c finding that rent-identified estimates isolate the cost channel without the endogenous
tenure split. Budget the search accordingly instead of spreading effort evenly across five sub-claims.

**4. Reverse causality is the binding risk-of-bias domain, not a caveat.** Values and fertility are
measured contemporaneously in most of this literature, and the causal arrow plausibly runs backward:
people who have not had children may report more self-oriented values partly because they have not had
children. The childfree literature is especially exposed, since stated value orientations there are
often collected after the fertility outcome is realized. This should enter the scope as a named
risk-of-bias domain in the way the endogenous-tenure threat did for C.2.c.

**5. The period restriction needs a PI ruling, and this is the third instance.** The v5 `phenomena`
field scopes D.1.a to SDT alone, but ideational and secularization accounts are central to FDT
scholarship, including the Princeton European Fertility Project. The same question arose for C.2.c
(Li 2024, FDT-era evidence against an SDT-only field) and for A.10. Three chapters hitting one
restriction makes this a master-list question for TICK-001 rather than a third case-by-case exception.

**Adopt the D.3.b wall verbatim rather than re-deriving it.** Wall 1 of the D.3.b scope already
specifies the D.1.a boundary from the other side: D.1.a covers a genuine fall in the desire for
children driven by competing adult goals, while D.3.b covers a live desire suppressed by ecological
dread. Restating that boundary in D.1.a's own words risks two chapters with subtly different rules and
papers that satisfy both or neither. Walls between paired hypotheses should be written once and
referenced, which is a general point worth recording if it holds.

**There is an inbound queue, and it is a biased sample.** The D.3.b RA gate routed 17 distinct records
to the `OFF_POSTMATERIALIST_D1a` cell, 15 carrying DOIs (15 at screen, 2 more added at RA gate; see
`extraction/climate-anxiety-eco-doomerism-ra-gate.csv`). They include Lesthaeghe's own 2014 SDT
overview and a run of voluntary-childlessness studies from 1999 to 2026. Useful as cold-start
material, but they are what a climate-anxiety query happened to surface, so they over-represent
childfree and voluntary-childlessness work and under-represent secularization and the postmaterialism
measurement literature. Under the C.2.c Tier-B integrity constraint they are Tier-A eligible only and
must not enter Tier B, or the recall number inherits D.3.b's query shape.

Walls also needed against D.1.b (external cultural transmission to societies mid-transition versus
internal value change in already-modernized ones), D.2.a (the gender-equity norm channel), D.2.b
(marriage and family norms), C.5.a and C.1.a (the income and security mechanisms the v5 notes flag as
hard to separate), and C.2.h (digital leisure as a newer expression of the same preference).

## Acceptance criteria
- [ ] `postmaterialism-individualism-secularization-search-scope.md` written to
      `literature/search-logs/`, following the D.3.b, A.10, and C.2.c scope structure.
- [ ] An explicit statement of what counts as causal evidence for an ideational hypothesis, listing
      the admissible design classes and conceding which sub-claims cannot supply them.
- [ ] Five sub-claim strata defined separately, each with its measure family and validity notes.
- [ ] A pooling rule barring cross-measure combination, with the measure recorded as a required tag on
      every effect.
- [ ] The secularization stratum identified as the likely quantitative core, with its own search
      channel budgeted.
- [ ] Reverse causality entered as a named risk-of-bias domain, with the childfree literature's
      after-the-fact measurement called out specifically.
- [ ] Wall vs D.3.b adopted by reference to the D.3.b scope's Wall 1, not restated.
- [ ] Walls vs D.1.b, D.2.a, D.2.b, C.5.a, C.1.a, C.2.h, each with an operational discriminator.
- [ ] The 17 routed records logged as Tier-A-eligible cold-start material, with the sampling bias and
      the Tier-B exclusion recorded.
- [ ] The SDT-only period restriction escalated to TICK-001 as a master-list question, citing the
      C.2.c and A.10 precedents.
- [ ] Tempo-vs-quantum tag required on every included effect (cross-ref A.11).

## Log
<!-- On close, write date + who, then fill in the two notes below (see tickets/README.md, "Closing a ticket"). -->

**Result.** <One or two sentences: what you decided or produced.>

**Workflow impact / future behavior.**
- Changes future behavior? <yes / no>
- Implemented in: <repo file(s) that enact the change>
- Do differently: <what future humans or AI assistants should now do.>
