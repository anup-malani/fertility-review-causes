# TICK-050: D.3.b risk-of-bias assessment
**Status:** open
**Assigned:** any
**Parallel-safe:** yes (with TICK-051)
**Blocks:** TICK-052
**Blocked by:** TICK-049
**Touches:** extraction/climate-anxiety-eco-doomerism-risk-of-bias.csv

## Description

Assess risk of bias per extracted study, reusing the B.1 nine-domain schema
(`extraction/evolutionary-sex-drive-contraceptive-decoupling-risk-of-bias.csv`) plus three domains that
D.3.b's design distribution makes load-bearing. The chapter's §9 already names all three.

**Confounding**, and not as a generic caution. Left political orientation, higher education, and
secularism each predict both climate concern and low fertility. A study regressing fertility intention
on climate worry without holding those fixed has not identified this chapter's mechanism; it has
measured D.1.a's. This domain should read directly off the adjustment field added in TICK-049.

**Reverse causality.** Parenthood changes how people appraise the ecological future, so the direction
of a cross-sectional association is genuinely ambiguous. One retrieved study — "Too worried about the
environment to have children? Or more worried after having them?" (2023) — is designed around exactly
this and is the most valuable design in the realized set. The rest are not, and should be rated
accordingly rather than given the benefit of the doubt.

**Common-method bias.** This is the domain B.1's schema does not have and D.3.b needs. Most studies
here measure exposure and outcome by self-report in a single survey instrument, often with the items
adjacent, which inflates the association between them. It applies to most of the stated-intention
stream and it is a well-understood problem in survey psychology, so an unrated study is an omission
rather than a judgement call.

Expect the ratings to cluster at serious, as B.1's did (4 of 5). That is an input that caps the GRADE
rating downstream, and it should be reported as such rather than softened.

## Acceptance criteria
- [ ] One row per extracted study across the inherited nine domains.
- [ ] Confounding domain populated from the TICK-049 D.1.a-adjustment field, so the RoB rating and the
      extraction record cannot disagree.
- [ ] Reverse-causality domain populated, with designs that actually address it distinguished from
      those that assume it away.
- [ ] Common-method-bias domain populated for every stated-intention study.
- [ ] Overall risk (low / moderate / serious) with a one-line rationale per study.
- [ ] Ratings reported separately for the stated and realized tracks, since they feed two separate
      syntheses and two separate certainty ratings.

## Log
- 2026-07-27 (Claude): opened.
