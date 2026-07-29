# Restricted pooled summaries — B.15, Old-Age Security and Pension Crowd-Out

Computed 2026-07-29 in response to the PI's answer to Phase 2 question Q2, option (b): *"Report the pooled numbers only for the studies in the settings the claim is about, and report Italy separately."*

## Method, and the check that it is the same method

Inverse-variance weighting, `w = 1/SE²`, on the retirement-asset channel only. Billari and Galasso is sign-flipped because its treatment is a pension **cut**, so its raw positive coefficient becomes negative once oriented to "more non-child old-age security." Han's standard error is not stored in `effects.csv` and is recovered from the reported coefficient and t-statistic, 4.0 / 3.27 = 1.223, exactly as the extraction note says the original harmonization did.

Both published summaries reproduce to six decimal places under this method, which is the warrant for trusting the restricted figures below:

| | reproduced | chapter reports |
|---|---|---|
| Birth probability | −0.006954 (SE 0.002037) | −0.006954 (SE 0.002037) |
| Completed fertility | −0.067672 (SE 0.026971) | −0.067672 (SE 0.026971) |

Membership matches the chapter's: five studies in the birth-probability pool, three in completed fertility, with Galofré-Vilà excluded from the latter.

## The restriction

"The settings the claim is about" means places where children still plausibly insure old age, so formal pensions, private savings and insurance markets are incomplete. Four studies qualify: Brazil (Danzer and Zyska), Namibia (Rossi and Godard), rural China (Shen and coauthors), and the Chinese long-term-care pilot (Han and coauthors). Italy is a mature pension system in a below-replacement setting, which is the case the chapter says the mechanism does **not** fit, so it is reported on its own.

## Birth probability

| | estimate | SE | 95% CI |
|---|---|---|---|
| Published, 5 studies | −0.006954 | 0.002037 | [−0.010946, −0.002963] |
| **Restricted, 4 studies** | **−0.007278** | **0.002901** | **[−0.012963, −0.001593]** |
| Italy alone, oriented | −0.006640 | 0.002860 | — |

Restriction barely moves this summary. Italy carried 50.7% of the weight, but its own oriented estimate, −0.006640, sits almost exactly on the restricted pool, so removing it changes the point estimate by three ten-thousandths and widens the interval. The concentration of weight was real and immaterial here.

## Completed fertility

| | estimate | SE | 95% CI |
|---|---|---|---|
| Published, 3 studies | −0.067672 | 0.026971 | [−0.120536, −0.014808] |
| **Restricted, 2 studies** | **−0.179337** | **0.078907** | **[−0.333996, −0.024679]** |
| Italy alone, oriented | −0.052900 | 0.028700 | — |

Restriction nearly triples this summary, by a factor of 2.65. Italy carried 88.3% of the weight at −0.0529, and removing it lets the two claim-relevant studies speak: rural China at −0.169 (SE 0.079) and Namibia at −4.58 (SE 1.63), the latter contributing almost nothing on weight but pulling in the same direction.

**This strengthens the chapter's argument rather than weakening it.** The chapter claims the mechanism operates where children still insure old age and has little room where pension systems are mature. Its published headline number was, arithmetically, an Italian estimate from a mature below-replacement system — the case the chapter says the mechanism does not fit. Restricted to the settings the claim is actually about, the effect is two and a half times larger.

## The problem with the restricted completed-fertility pool

**Two studies is below the review's own threshold for pooling.** `PROTOCOL.md` §5 stage 9: *"Meta-analysis (R `metafor`) if ≥3 studies with extractable effect sizes; narrative synthesis otherwise."*

So option (b), executed faithfully, produces a completed-fertility summary the protocol would not sanction. Three ways out, and the choice is the PI's:

1. **Report the two estimates narratively and give no pooled completed-fertility number.** Protocol-compliant, and it costs the chapter its headline figure for that outcome.
2. **Report the restricted pool with the k = 2 breach disclosed** as a deviation under §8. Keeps the number, states plainly that it falls below the review's own rule.
3. **Admit Danzer and Zyska's completed-fertility estimate** of −1.3 births per woman, which is claim-relevant Brazil and would make k = 3, but carries no standard error in `effects.csv` and no recoverable test statistic. It cannot be weighted without a new extraction, and the PDF is not on this machine.

Route 3 is the only one that both keeps a pooled number and satisfies the threshold, and it requires retrieval this working tree cannot do.

## Note on Han

Han's estimate is +4.0 percentage points and enters the birth-probability pool unflipped, so a long-term-care insurance expansion is associated with **higher** fertility. That runs against the retirement-asset channel's predicted direction inside a summary the chapter offers as evidence for it. It carries 2.8% of the weight, so it does not drive the result, and the anomaly is worth stating rather than smoothing. Q6 already directs that the wrong-way reading go on the record.

## Reproduction

The figures above come from `extraction/old-age-security-pension-crowdout-effects.csv`. The published pools reproduce exactly from that file under the method described, so no separate analysis script was needed to verify them.
