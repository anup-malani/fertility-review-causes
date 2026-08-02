# Search scope — evolutionary sex drive and contraceptive decoupling

**Hypothesis:** B.1 (HYPOTHESES-v5.md)
**Hypothesis slug:** `evolutionary-sex-drive-contraceptive-decoupling`
**Target phenomenon:** First and Second Demographic Transition (FDT, SDT); the SDT/Pill era is the sharp case
**Status:** cold-start scope drafted before query construction; gold anchors not yet sourced or RA-frozen

## Causal claim

Natural selection wired humans to seek *sex*, not *children*: the proximate motivation is sexual, and
high fertility was historically a by-product of that drive because sex and reproduction were
mechanically coupled. Contraception severs the coupling, so the evolved sex drive continues to operate
without producing births. Because there is no comparably strong *evolved* desire for children to take
up the slack, fertility falls — **even with no change in the preference for children.** This is a
distinct biological *root* cause, not the proximate contraception mechanism.

## The B.1 / A.2 boundary (the load-bearing routing rule)

This is the sharpest and most consequential distinction in the whole scope, because most contraception
papers belong to A.2, not here.

- **A.2 (Modern Contraceptive Technology — proximate) asks:** *given that people want fewer children,
  how does cheap effective contraception help them achieve that target?* Its estimand is closing the
  desired–realized gap.
- **B.1 (this chapter — root) asks:** *why does contraception so effectively depress fertility in the
  first place?* Its estimand is the **decoupling of sex from reproduction** and the **absence of an
  evolved positive demand for children** — fertility falling *without* a fall in child preference.

A paper is B.1-primary only if it speaks to the decoupling / dissociation itself, or to fertility
declining while the preference for children is held fixed or unchanged. A paper showing contraception
reduces *unwanted* births among people who already want fewer children is **A.2**, and routes there.

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_DECOUPLING` | Contraceptive access/adoption as the severing technology, or a natural test of the sex↔reproduction link | Realized fertility dissociating from a determinant of sexual activity/exposure (e.g. status, mating effort, coital frequency, union) | Primary synthesis |
| `PRIMARY_DESIRE_INDEPENDENCE` | Contraceptive access/adoption | Fertility falls holding desired family size / preference for children fixed | Primary synthesis |
| `PROXIMATE_ULTIMATE` | Status, mating effort, or resources (an evolutionary predictor of fertility) | Sexual/mating outcome vs reproductive outcome, pre- vs post-contraception (Pérusse-type) | Primary synthesis, reported as the dissociation test |
| `MOTIVATION_DISTINCTNESS` | — | Evidence that reproductive motivation is a psychological construct distinct from and weaker than sexual motivation | Primary/bridge |
| `THEORY` | Evolutionary / biosocial model of the mismatch, sex drive, or absence of a child-drive | No empirical fertility estimate | Theory stream |
| `TEMPO_EXPOSURE` | Coital frequency or exposure change | Fecundability / birth timing only | Route to A.4 `coital-frequency-biological` unless the decoupling is the object |
| `OFF_EXPOSURE_A2` | Contraceptive availability/cost closing the desired–realized gap | Unwanted births / realized fertility among those wanting fewer | Route to A.2 `contraceptive-technology-diffusion` |
| `OFF_OUTCOME` | Mating psychology, sexual behavior, status–sex link | No fertility outcome | Mechanism/context only |
| `REVERSE` | Fertility affects sexual behavior or contraceptive adoption | Sexual/behavioral outcome | Theory/context, not the effect sought here |
| `CULTURAL_NORMALIZATION` | Postmaterialist / normative legitimation of contraceptive use | Fertility | Cross-ref D.1.a; not the biological estimand |

## Eligibility rules

- Include empirical studies only when the estimate bears on the **decoupling of sex from reproduction**
  or on **fertility falling independently of the preference for children** — not merely on contraception
  reducing unwanted births.
- The evolutionary-theory canon (selfish-gene, parental-investment, evolved-desire, mother-nature
  lineages) seeds the **theory** stream and does **not** count toward empirical recall.
- Preserve both FDT and SDT evidence; the SDT/Pill era is the clean case but pre-Pill decoupling
  (withdrawal, abstinence, coitus-independent stopping) is in scope for the FDT.
- A study identifying the effect purely off contraceptive *cost/availability* with a desired–realized
  gap framing is A.2, even if it mentions evolution in passing.
- Keep theory and off-cell papers discoverable but outside the empirical primary-cell recall denominator.

## When to adjudicate mechanisms

The title/abstract screen decides whether a paper belongs in the empirical decoupling, theory, tempo,
or adjacent-evidence stream. It does **not** require the RA to determine the exact mechanism from an
abstract. Detailed mechanism coding occurs during full-text extraction, before synthesis.

For every included empirical paper, full-text extraction must distinguish:

- `PROXIMATE_ULTIMATE_DISSOCIATION` — an evolutionary predictor (status, mating effort) tracks sexual
  outcomes but not, or inversely, reproductive outcomes once contraception is available;
- `DESIRE_HELD_CONSTANT` — fertility falls with contraceptive access holding desired family size /
  child preference fixed;
- `SEX_FERTILITY_TREND_DECOUPLING` — aggregate or temporal dissociation of sexual activity from births;
- `CONTRACEPTIVE_MEDIATION` — the estimate is identified off contraceptive access/adoption as the
  severing technology;
- `MOTIVATION_DISTINCTNESS` — reproductive motivation shown to be a distinct, weaker construct than
  sexual motivation;
- `MIXED_OR_UNCLEAR` — a total effect with no isolated channel.

Also record the **level of identification**: individual/micro decoupling vs population/aggregate
decoupling; and whether the design holds the **preference for children** fixed (the clause that
separates B.1 from A.2).

Drafting may report only mechanisms supported by these full-text fields. A reduced-form contraception
effect with `MIXED_OR_UNCLEAR` mechanism may support the decoupling relationship but must not be
described as proof of the no-evolved-child-drive claim.

## Expected shape of the evidence (a caution, not a result)

B.1's canonical citations (Dawkins 1976, Trivers 1972, Buss 1994, Hrdy 1999) are **evolutionary
theory, not demographic empirics.** Two consequences to expect and to report honestly:

1. **Channel-1 of the cold-start (prior meta-analyses / systematic-review included-study lists) is
   likely near-empty** — there is unlikely to be a meta-analysis of "sex–reproduction decoupling →
   fertility." A near-empty channel 1 is itself a finding, not a search failure.
2. **The estimand-ready pooling set may be thin or near-empty**, while the theory stream is rich. The
   review should surface this asymmetry rather than manufacture a pooled estimate the literature does
   not support.

## Cold-start channels and leakage wall

1. Direct empirical papers testing the decoupling / desire-independence, identified independently of
   the hypothesis list, seed the empirical Tier-A candidate set.
2. Canonical evolutionary-theory and biosocial-model papers seed the theory set but do not count
   toward empirical recall.
3. References and citations of the independent seeds create the orthogonal Tier-B candidate frame.
4. Production-query terms will not be mined from a paper and then evaluated on that same paper; learned
   extensions must be fold-local after the gold frame exists.

## Pre-query anchor audit (not yet built)

The verified candidate anchor set will be stored in
`evolutionary-sex-drive-contraceptive-decoupling-cold-start-anchors.json`. Every anchor must clear the
**mandatory existence-verification gate** (a live DOI, or a Crossref/publisher record confirming the
title exists) before it enters any recall denominator — no anchor is hand-asserted from memory. The set
will deliberately contain primary-decoupling, motivation, theory, and off-cell anchors so the eventual
search is tested on routing as well as topical retrieval.
