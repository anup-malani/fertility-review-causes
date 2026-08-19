# Decision: when one hypothesis becomes two chapters, and where the split goes

**Date:** 2026-08-18
**Author:** Anup Malani (PI) ruling on D.3.c Call 1; drafted by Shravan + Claude Code session
**Status:** Active — applies to any hypothesis whose entry bundles two mechanisms
**Review date:** at v6 of `HYPOTHESES.md`, when the registry question (below) is taken up

## Context

Two hypotheses have now turned out to bundle two things under one number, and the second one forced
the general question.

**B.6 (microplastics and PFAS), 2026-08-14.** One entry covering two chemical families whose
evidence bases fail in opposite directions — PFAS has a real human fertility epidemiology and a
*falling* exposure series; microplastics has a fast-growing tissue-detection literature, a *rising*
exposure series, and almost no human fertility epidemiology. A bundled rating would have averaged a
measured-but-shrinking exposure against an unmeasured-but-growing one and described neither.

**D.3.c (despair and hopelessness), 2026-08-18.** One entry whose stated claim is that despair defers
childbearing, against a larger and older literature in which foreclosed futures *accelerate* early and
nonmarital childbearing. Reconnaissance and the A4 citation frame both established that these are not
two readings of one estimate: they have different treatments (chronic place-level decline versus low
perceived individual opportunity), different outcome margins (completed quantum versus timing of first
birth), and different canons.

The recurring temptation in both cases was to rate one number and note the tension in prose. That
produces a verdict that describes neither half.

## Options

1. **One chapter, one signed verdict, tension noted in discussion.** Cheapest. Rejected: the verdict
   would be an average over two treatments, which is not a quantity anyone asked about.
2. **One chapter, a margin-conditional or family-conditional verdict.** This was the D.3.c scope's own
   recommendation before the ruling. Rejected by the PI: it keeps a single verdict over two
   treatments, and a conditional statement of one parameter is not the same as two parameters.
3. **Promote to two entries in the hypothesis list** (B.6.a/B.6.b, D.3.c.i/D.3.c.ii) and run two
   tickets. Rejected on cost, not on principle — see Consequences.
4. **One hypothesis entry, one ticket, one search — two chapters, split at extraction.** Adopted.

## Decision

**A hypothesis splits into two chapters when its bundle carries two treatments, or two evidence bases
that fail in different directions, such that no single rating could describe both. The split happens
at synthesis, not in the registry.**

Concretely, and identically in both cases so far:

- **The search is one search.** Walls, estimand cells, cold-start channels, anchor set and
  title/abstract screen are shared. Splitting the search doubles screening cost and produces two
  corpora that each have to enforce the same walls.
- **The split happens at extraction, on one tagged field** — `CHEMICAL_FAMILY` for B.6, `CHAPTER`
  (deferral/acceleration, assigned on outcome margin) for D.3.c.
- **The split field must be assignable at title and abstract.** Both cases satisfy this, and D.3.c's
  is the instructive one: its hardest wall (despair versus economic uncertainty) is *not* visible in a
  summary, but its chapter split runs on outcome margin, which is. A split on an invisible field would
  push the partition into full text and make the screen unable to route.
- **Risk of bias, synthesis, demographic significance and GRADE run twice.** No bundled rating at any
  stage; no pooled estimate across the split.
- **PRISMA is one flow with a terminal split.** Identification, screening and eligibility are counted
  once; the included-studies box divides. Two separate diagrams would misreport the screening
  denominator as if each half had been searched independently.
- **Records assigned to the other chapter are not exclusions.** They are a different disposition and
  must not be recorded in the PRISMA exclusion counts.
- **Unassignable records appear in both chapters and are pooled in neither**, reported identically in
  each so a reader of one is not misled about what was set aside.
- **Neither chapter's rating may borrow from the other.** On D.3.c the two halves are not equally
  evidenced — the deferral chapter's mechanism is unmeasured in the literature that studies its
  treatment, while the acceleration chapter's canon estimates its mechanism against its outcome
  directly — and a reader of the pair must not come away thinking otherwise.

## Consequences

**The registry question is deferred, deliberately and each time.** Whether the halves should become
separate numbered entries is real, and the D.3.c ruling ("these seem like different hypotheses") is an
argument that they should. It is not taken here because renumbering `HYPOTHESES.md` propagates into
every in-flight branch's `HYPOTHESES-v5.md §X` reference, and the taxonomy belongs to TICK-001. Each
split therefore carries a standing referral to the PI for v6, in reduced form: *should this entry
become two?* B.6 carries one (Call 1); D.3.c carries one (Call 6).

**Cost.** Roughly one extra chapter's worth of synthesis, risk-of-bias and GRADE work per split, and
no extra search or screening cost. That ratio is what makes option 4 preferable to option 3.

**Risk.** Chapter proliferation if the rule is read loosely. The test is *two treatments or two
incompatible evidence bases*, not *two subgroups* or *heterogeneous effects*. A moderator is not a
second hypothesis. C.2.c's tenure-conditional housing elasticity is the boundary case that stays ONE
chapter: renters and owners face the same treatment (a price change) and the sign differs by who is
exposed — that is a conditional parameter, not two mechanisms.
