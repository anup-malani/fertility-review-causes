# Estimand-gate calibration - old-age-security-pension-crowdout

How well the **automated** estimand gate (Sonnet, judging blind on title+abstract - GACS §D2b) reproduces the **RA's** inclusion decisions on the pilot's 40 reviewed studies. This gives the production gate a measured precision for hypotheses where there is no RA pass. Sonnet never saw the RA decision or the earlier relevance rationale.

## 1. Gate decision: PRIMARY vs off-cell (the decision that matters)

- **Precision 100%**  (of papers Sonnet admits to the pooling set, the share the RA also admits)
- **Recall 80%**  (of papers the RA admits, the share Sonnet also admits)
- **Accuracy 95%**, F1 0.89, Cohen's kappa 0.86

| | RA primary | RA off-cell |
|---|---|---|
| **Sonnet primary** | 8 (TP) | 0 (FP) |
| **Sonnet off-cell** | 2 (FN) | 30 (TN) |

The gate is **safe**: 0 false positives means an off-cell paper never enters the pooling set. The cost sits in the 2 false negatives - primary papers Sonnet drops, which a human gate on boundary cases recovers.

### Gate disagreements (where a human gate still earns its place)

- **Children as insurance revisited: Impact of children on private insurance adoption among older parents** [E29] - RA primary, Sonnet off. RA: `PRIMARY`; Sonnet: `OFF:reverse-direction` - "Estimates effect of number of children on parents' private insurance adoption -- the reverse chain, not pension/OAS causing fertility."
- **The US baby boom and the 1935 Social Security Act** - RA primary, Sonnet off. RA: `PRIMARY`; Sonnet: `OFF:different-cause` - "Treatment is SSA-era family allowances/social spending, not old-age pension motive; positive effect contradicts OAS crowd-out."

## 2. Off-cell bucket agreement (routing quality)

Of 30 papers both call off-cell, **25 (83%) agree on which off-cell bucket** (i.e. why it leaves, hence where it routes). Bucket disagreements do not change the include/exclude decision - both exclude - but they change which other chapter the paper feeds.

Bucket disagreements:

- **The intergenerational education spillovers of pension reform** - RA `OFF:fertility-as-cause` vs Sonnet `OFF:outcome-not-fertility`
- **Are children substitutes for assets? Evidence from Bangladesh** - RA `OFF:fertility-as-cause` vs Sonnet `OFF:reverse-direction`
- **The One-Child Policy and Household Saving** - RA `OFF:outcome-not-fertility` vs Sonnet `OFF:fertility-as-cause`
- **The impact of parental leave policy on the intensity of labour-market participation of mothers: Do the number of children and pre-birth work engagement matter?** - RA `OFF:outcome-not-fertility` vs Sonnet `OFF:off-topic`
- **Will You Marry Me, Later?** - RA `OFF:off-topic` vs Sonnet `OFF:different-cause`

## Reading

On the pilot the automated gate is **100% precise / 80% recall** against the RA. High precision means the gate can be trusted to keep the pooling set clean without a human on every paper; the recall gap is concentrated in genuinely borderline estimands (direction/mechanism calls the abstract underdetermines), which is exactly the boundary band GACS reserves for the RA verdict (§D). So for a new hypothesis: run the automated gate, and route only its off-cell/borderline calls to the RA, not the whole set.

**Caveats.** (1) n=40, one hypothesis - a rate, not a guarantee. (2) The RA decisions are themselves the ground truth; a Sonnet-RA disagreement can be the RA making a generous judgment call, not Sonnet erring (see the gate disagreements). (3) Classification was batched 10/agent; papers were judged independently but not in isolation. (4) 3 of 40 were title-only - the same abstract-dependence flagged for the Tier-B recall re-grade.

