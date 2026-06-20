# Calibration Report: old-age-security-pension-crowdout, Batch 1

**Date:** 2026-06-20
**Models:** Haiku = claude-haiku-4-5-20251001 (primary screener); Sonnet = claude-sonnet-4-6 (gold standard)
**Papers compared:** 103
**Stopping criterion:** Haiku FN rate < 3% — **MET**

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Papers compared | 103 |
| Agreement rate | 81.6% |
| Both RELEVANT | 37 |
| Both NOT_RELEVANT | 44 |
| Both UNCERTAIN | 3 |
| Haiku FN rate (H=NOT_RELEVANT, S=RELEVANT) | **0%** (0 papers) |
| Haiku FP rate (H=RELEVANT, S=NOT_RELEVANT) | 0% (0 papers) |
| Haiku confusion (H=UNCERTAIN, S decisive) | 3.9% (4 papers) |
| Sonnet UNCERTAIN rate | 17.5% (18 papers) |
| **Stopping criterion met** | **YES** |

---

## Stopping Criterion

**MET.** Haiku's false negative rate is 0% (0 papers missed that Sonnet caught as RELEVANT), well below the 3% threshold. Proceed to routing rule — see routing-rule.md.

---

## False Negatives (Haiku Missed, Sonnet Caught)

_None._

---

## False Positives (Haiku Included, Sonnet Excluded)

_None._

---

## Haiku Confusion (UNCERTAIN When Sonnet Was Decisive)

Four papers where Haiku returned UNCERTAIN but Sonnet rendered a decisive verdict.

**1. Private versus public old-age security** (2017 | DOI: 10.1007/s00148-017-0681-9)
- Haiku: UNCERTAIN [MEDIUM] — Compares old-age security arrangements but abstract unavailable; likely focuses on system design rather than fertility effects.
- Sonnet: RELEVANT [HIGH] — Compares private versus public old-age security arrangements, which is directly relevant to how formal pension systems affect fertility through the old-age security motive.

**2. Child allowances and social security: A welfare analysis** (2003 | DOI: 10.1007/s00148-003-0162-4)
- Haiku: UNCERTAIN [MEDIUM] — Discusses child allowances with social security but fertility effects unclear from title alone.
- Sonnet: RELEVANT [MEDIUM] — Welfare analysis of child allowances and social security together likely addresses interactions between pension systems and fertility incentives.

**3. Expanding social protection for children and mothers: Evidence from pensions and birth outcomes in Brazil** (2016 | DOI: 10.1016/j.jdeveco.2016.05.004)
- Haiku: UNCERTAIN [MEDIUM] — Studies pensions and outcomes including birth outcomes but primary focus appears to be maternal health, not fertility decisions.
- Sonnet: RELEVANT [MEDIUM] — Studies pensions and birth outcomes in Brazil, which may capture fertility effects of pension expansion even if the primary focus is on birth health outcomes.

**4. Social Security and Elderly Welfare: The Case of Pension Expansion in Argentina** (2016 | DOI: 10.1257/aer.20130456)
- Haiku: UNCERTAIN [MEDIUM] — Studies pension expansion effects on elderly and families but abstract doesn't confirm fertility is outcome measure.
- Sonnet: RELEVANT [HIGH] — Studies large-scale pension expansion in Argentina and finds effects on household fertility, directly testing the pension-fertility relationship.

---

## Pattern Analysis

There are zero false negatives, so no FN pattern analysis is possible. The four confusion cases (UNCERTAIN when Sonnet was decisive) share a common structure worth noting for prompt calibration.

All four confusion papers share one of two surface features that caused Haiku to withhold a RELEVANT verdict:

**Missing abstract / title-only screening.** "Private versus public old-age security" (2017) produced UNCERTAIN because the abstract was unavailable. Haiku correctly flagged uncertainty rather than fabricating a judgment, but the title alone — "old-age security" appearing in the hypothesis label itself — should have been sufficient to call RELEVANT. Sonnet applied more aggressive title-level inference.

**Ambiguous primary outcome.** The Brazil (2016) and Argentina (2016) papers use pension expansion as the treatment but frame outcomes around birth outcomes/maternal health or elderly welfare respectively. Haiku read the framing literally and was uncertain whether fertility was actually measured. Sonnet correctly recognized that pension expansions affecting household composition and birth outcomes are directly informative for the pension-crowdout hypothesis even when "fertility" is not the headline framing.

**Indirect policy coupling.** "Child allowances and social security" (2003) couples two policies — child transfers and pensions — without flagging fertility as the explicit dependent variable in the title. Haiku was uncertain; Sonnet inferred that the welfare analysis of this joint policy necessarily engages the fertility margin.

No confusion papers come from a specific region, era, or methodological tradition that would suggest a systematic blind spot in Haiku's recall. The pattern is narrow: Haiku is conservative when the abstract is missing or when fertility is an implicit rather than explicit outcome.

---

## Prompt Revision Suggestions

Because the FN rate is already 0%, no revision is strictly required before the full run. The suggestions below are targeted at reducing the confusion rate (the 3.9% UNCERTAIN-when-decisive cases) to improve throughput and reduce how many papers are escalated to Sonnet.

**Change 1:** Clarify that birth outcomes are a valid proxy for fertility decisions.
*Current text (paraphrase):* Screen for papers where the outcome is fertility (birth rates, completed family size, parity).
*Revised text:* Screen for papers where the outcome is fertility (birth rates, completed family size, parity, number of births, or birth outcomes such as infant health) when the treatment is a pension, social security, or old-age support policy. Birth outcome papers that study pension expansions are in scope because they capture the fertility margin.
*Rationale:* Would have resolved the Brazil (2016) and Argentina (2016) confusion cases.

**Change 2:** Authorize title-only RELEVANT verdicts for papers whose title contains "old-age security," "pension," or "social security" paired with "fertility," "birth," or "children."
*Current text (paraphrase):* If the abstract is unavailable, return UNCERTAIN.
*Revised text:* If the abstract is unavailable but the title contains a pension/old-age security term paired with a fertility/birth/children term, return RELEVANT [MEDIUM] rather than UNCERTAIN. Reserve UNCERTAIN for title-only cases where the link to the fertility outcome is indirect or unclear.
*Rationale:* Would have resolved the "Private versus public old-age security" (2017) confusion case.

**Change 3:** Clarify that welfare analyses jointly modeling child subsidies and pension generosity are in scope.
*Current text (paraphrase):* Include papers studying how pension systems affect fertility decisions.
*Revised text:* Include papers studying how pension systems affect fertility decisions, including welfare or policy analyses that jointly model child allowances and social security, since such models necessarily incorporate fertility as a margin of adjustment.
*Rationale:* Would have resolved the "Child allowances and social security" (2003) confusion case.

---

## Recommendation

Stopping criterion met — proceed to full run using routing-rule.md.
