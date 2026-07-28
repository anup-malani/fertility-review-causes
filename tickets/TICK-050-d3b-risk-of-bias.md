# TICK-050: D.3.b risk-of-bias assessment
**Status:** first pass done on the 5 assessable studies; Helm NOT_ASSESSABLE (no full text); second reader outstanding
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
- 2026-07-27 (Claude): 6 rows in `extraction/climate-anxiety-eco-doomerism-risk-of-bias.csv`
  over the inherited nine domains plus the three D.3.b additions (D.1.a-specific
  confounding, reverse causality, common-method bias) and one further column this ticket
  did not anticipate: **`ecological_specificity`**, added because the gate and extraction
  both showed the Wall 2 discrimination failing *inside* studies rather than across them.

  **Ratings: 3 serious, 2 moderate, 1 not assessable.**

  | Study | Overall | The binding domain |
  |---|---|---|
  | Golovina & Jokela | serious | `ecological_specificity` — climate worry does not survive adjustment for the summary of all other worries. Confounding is *low* (adjusts for political attitudes); the study fails on specificity, not on confounding |
  | Jylhä et al. | moderate | Reverse causality, acknowledged by the authors; the null is well powered and credible |
  | Peters et al. | moderate | D.1.a confounding serious (no political controls); reverse causality **low** and uniquely so — the only two-directional design in the review |
  | Weychert et al. | serious | Exposure measurement (news volume, not dread) and reporting (no CIs anywhere, null main effect) |
  | Saha et al. | serious | Serious on nearly every domain; retained for transportability, not for an effect size |
  | Helm et al. | **NOT_ASSESSABLE** | Full text unobtainable. Risk of bias must not be graded from an abstract |

  Note the pattern worth carrying to TICK-053: the best-confounded-controlled study is the
  one that fails ecological specificity, and the one with the cleanest reverse-causality
  design has no political controls. No study in the realized stratum is strong on both.
- 2026-07-27 (Claude): opened.
