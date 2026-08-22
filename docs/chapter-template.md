# Chapter Template

**Status:** Authoritative. Supersedes the section skeleton in `output/chapters/hybrid-chapter-template.md`
and expands `PROTOCOL.md` §6.
**Companion:** `docs/chapter-writing-style-guide.md` owns prose rules. This document owns structure and
analysis, and defers to that guide for sentence-level style rather than repeating it.
**Author:** Shravan + Claude Code, 2026-08-22, generalised from A.12 (`twinning-multiple-births`).

This template is built in three layers, and they are meant to be worked in this order:

> **Organizational structure → Statistics, economics and demography → Writing**

Get the sections and their commitments fixed first; then decide what quantity each section must
establish; only then write. A chapter that is written before its estimand is named will describe a
literature instead of answering a question.

---

## 0. Audience, fixed once for the whole review

**Write for a University of Chicago undergraduate who understands economics but not demography.**

That reader arrives with price theory, identification, selection, elasticities, margins, and income and
substitution effects. They do not arrive with total fertility rate, parity, tempo and quantum, cohort
versus period measures, or the three target phenomena. The asymmetry is the single most useful fact
about the audience and it has two consequences that run through every layer below:

- **Spend the reader's existing capital.** Frame mechanisms in the vocabulary they already own. An
  intensive/extensive margin split, a target-stock income effect, a selection-on-the-dependent-variable
  problem — these land immediately and cost nothing to introduce.
- **Buy the rest explicitly.** Every demographic term is glossed at first use, inline, in one clause.
  Never assume TFR, parity, DZ/MZ, replacement, PM/FDT/SDT, GRADE or eSET.

---

# Layer 1 — Organizational structure

## 1.1 The mandatory sentences

Seven sentences appear, in these forms, in **every** chapter. They are not stylistic. Each forces a
commitment the chapter could otherwise avoid making, and a chapter that cannot complete one of them has
found a real gap rather than a wording problem.

| # | Where | Sentence |
|---|---|---|
| **S1** | §1, first line | **"This chapter explores the effect of [TREATMENT] on [OUTCOME]."** |
| **S2** | §1.1, opening the plain-terms passage | **"In plain terms: [ANALOGY]."** |
| **S3** | §1.2 | **"The parameter this chapter estimates is [ESTIMAND], measured in [UNITS]."** |
| **S4** | §7, before any arithmetic | **"The phenomenon to be explained is measured in [UNITS OF PHENOMENON]; this mechanism offers [UNITS OF MECHANISM]."** |
| **S5** | §7.1, §7.2, §7.3 — once each | **"For [PM / FDT / SDT], the verdict is [NEGLIGIBLE / MINOR / SUBSTANTIAL / DOMINANT / NOT ASSESSED], because [ONE CLAUSE]."** |
| **S6** | Provenance block | **"This chapter is written on [n] of [m] wanted full texts ([p]%)."** |
| **S7** | Provenance block | **"The findings that would survive full retrieval are [X]; the findings that might not are [Y]."** |

Worked from A.12, so the register is visible:

- **S1** — "This chapter explores the effect of the twinning rate on the total fertility rate."
- **S2** — "In plain terms: output is orders times units-per-order, and twinning is units-per-order."
- **S3** — "The parameter this chapter estimates is the change in a mother's subsequent births caused by
  a twin birth, measured in births per twin birth."
- **S4** — "The phenomenon to be explained is measured in whole children; this mechanism offers
  percentage points of a multiplier bounded between 1.01 and 1.05."
- **S5** — "For pre-modern variation, the verdict is NEGLIGIBLE, because the largest multiplier
  difference between any two recorded human populations is 4.2% against a range of four children."
- **S6** — "This chapter is written on 68 of 253 wanted full texts (27%)."
- **S7** — "The findings that would survive full retrieval are the mechanical bound and the post-2010
  reversal; the finding that might not is the offset magnitude."

**S4 is the one to write first, before the literature is read.** On A.12 it settled the question before
any estimate existed: a mechanism denominated in percentage points of a multiplier cannot explain a
phenomenon denominated in whole children, and no study could have changed that. Writing S4 early tells
you how much estimation the chapter actually needs.

## 1.2 Section order

| § | Section | Must contain |
|---|---|---|
| — | Header block | Category · Primary mechanism (one sentence) · Cross-references · Status line naming the ticket, the date, whether PI-reviewed, and the retrieval fraction |
| **1** | The claim | **1.1 In plain terms first** (S2, the organising analogy) then **1.2 The claim precisely** (S1, S3, the registry wording quoted, and the decomposition into separable sub-claims) |
| **2** | Theoretical mechanism | The mechanism in the reader's economics vocabulary; the identity/behaviour split if there is one; what would make the hypothesis wrong |
| **3** | Search strategy | Reproducible; walls and their enforceability; any wall declared unenforceable **in advance**; boundary rulings against neighbouring hypotheses |
| **4** | PRISMA flow | The funnel table, plus the two or three features of it that change how the chapter should be read |
| **5** | Included studies | Table with design column; the estimator-disagreement analysis (§2.2 below) |
| **6** | Quantitative synthesis | **6.1 The answer in plain terms first**, then **6.2 The estimate** |
| **7** | Demographic significance | S4, then 7.1 PM / 7.2 FDT / 7.3 SDT, each carrying S5 |
| **8** | GRADE rating | Per-phenomenon table with every downgrade named |
| **9** | Verdict | Standalone and readable cold; one number a reader carries away |
| **10** | Open questions | PI calls, retrieval priorities, and studies that do not exist and should |
| **11** | References | |
| — | **Provenance and standing caveats** | S6, S7, any objection over which the chapter was written, and which numbers came from abstracts rather than full text |

**Non-negotiable orderings.** Plain terms precede technical statement in §1 and §6. S4 precedes all
arithmetic in §7. The verdict (§9) is written so it survives being read alone, because it will be.

---

# Layer 2 — Statistics, economics and demography

Structure fixed, decide what each section must *establish*. This layer is the chapter's spine and it is
where chapters go wrong invisibly.

## 2.1 Name the estimand before reading anything

Three questions, answered in writing before the literature is opened:

1. **What is the parameter, in what units, with what sign convention?** (S3)
2. **What is the counterfactual?** State it as a ceteris-paribus perturbation. If it cannot be stated
   that way, the parameter is not identified and the chapter must say so and downgrade for
   indirectness — not quietly report a measured share as though it were an estimated effect.
3. **Is this an identity, a behavioural parameter, or both?** If both, they need different treatment and
   the registry entry probably runs them together.

**The identity/behaviour split.** An accounting identity cannot be false and needs no study; the
behavioural response to it is the only place the hypothesis can be wrong. Chapters that miss this
search for effect estimates in a cell populated by statistical tabulations, find none, and wrongly
report the literature as thin.

**Margins.** Say explicitly whether the mechanism moves the extensive margin (how many events) or the
intensive margin (how much per event). Reviewers and readers both track this, and it is the cleanest
way to separate two hypotheses that touch the same aggregate.

## 2.2 Identification, and the rule that matters most

**Resolve disagreements; do not average them.**

When included studies disagree, the first question is never "what is the pooled estimate" — it is
**"do these studies use the same estimator?"** If some use a design with a known bias and others
correct for it, the body is not heterogeneous evidence about one parameter. It is one biased estimator
and one unbiased one, and the correct synthesis names the bias, gives its direction, and reports the
corrected estimate. Averaging in that situation manufactures a false middle.

On A.12 this was the whole chapter: four of six primary studies compared mothers who ever bore twins
against mothers who never did, which compares high-fertility with low-fertility women *by construction*,
because exposure to the risk of twinning accumulates with births. One study controlled for exposure and
the sign reversed. A pooled estimate would have reported a positive effect that does not exist.

**Therefore, for every chapter, run this check explicitly and report it in §5:**

- What is the **naive estimator** in this literature — the comparison an author would make without
  thinking hard?
- Does it condition on the outcome, or on something that accumulates with the outcome?
- What is the **direction** of the resulting bias?
- How many included studies use it?

## 2.3 The attrition ledger

For any mechanism stated as a rate or an identity, enumerate the attrition between the event that is
*counted* and the quantity that is *demographically relevant*, before computing anything.

The generic ledger, with A.12's entries as illustration:

| Stage | Question | A.12 |
|---|---|---|
| Conception → delivery | What is lost before the counted event? | Vanishing twin: conceived multiples exceed delivered multiples |
| Delivery → survival | Is the counted unit the surviving unit? | Twins are ~2.4% of births in poorer countries but ~12% of neonatal deaths |
| Survival → next generation | Does the mechanism affect the *next* cohort's fertility? | Prenatal testosterone transfer from a male co-twin may reduce the female co-twin's later fertility |
| Realised → biological | Is the measured rate the underlying rate? | Twin infanticide and under-registration |

Each entry has a sign. If they all run the same way, the headline arithmetic is biased in a known
direction and the chapter must say so in the verdict rather than the appendix. A.12's four entries all
pointed the same way, which is structurally the (1−p) accounting error B.5 shipped.

## 2.4 Demographic significance — the order of operations

**First the units check (S4).** Compare the units of the phenomenon with the units of the mechanism. If
they differ by orders of magnitude, the verdict follows immediately and everything after it is
quantifying a gap rather than testing a hypothesis. Say that plainly; it is a finding, not a shortcut.

**Then, per phenomenon, whichever of these the evidence supports:**

- **Decomposition share** — what fraction of the observed change does the mechanism account for, holding
  the rest fixed? Show the arithmetic inline; the reader should be able to check it.
- **Slope sufficiency** — is the mechanism's own movement large enough, at the estimated elasticity, to
  generate the observed change?
- **Variance share** — across populations or periods, how much of the variance in the outcome does
  variation in the mechanism explain?

**Then the endogeneity check, which is easy to skip and expensive to miss.** Ask whether the mechanism's
movement is itself *caused by* the phenomenon being explained. On A.12 a quarter of the modern twinning
rise is driven by delayed childbearing — which is the very postponement the hypothesis claims to
offset. A feedback of a decline cannot be evidence against the decline's cause, and that component must
be netted out before any offset is claimed.

**Verdict vocabulary, fixed** (used in S5): **NEGLIGIBLE** (<5% of the phenomenon) · **MINOR** (5–20%) ·
**SUBSTANTIAL** (20–50%) · **DOMINANT** (>50%) · **NOT ASSESSED** (out of scope in the registry; say so
and say what the sign would be if assessed).

## 2.5 GRADE

Per phenomenon, not per chapter — the same evidence can be strong for one target and weak for another.
Start from the available designs and downgrade for named defects: **imprecision**, **risk of bias in the
body as a whole**, **indirectness** (the evidence answers a neighbouring question), **inconsistency**,
**publication bias**. Every downgrade names its reason in the table. A chapter with a HIGH rating for a
*negligible* effect is a perfectly coherent and common result — certainty about the size of an effect is
not the same as the effect being large.

---

# Layer 3 — Writing

Structure fixed, analysis fixed, now write. **`docs/chapter-writing-style-guide.md` governs
sentence-level style and is not repeated here.** What follows is what that guide does not cover.

## 3.1 Lay comparison before technical comparison — everywhere, not once

Every substantive comparison in the chapter appears **twice**: once in plain terms, once technically, in
that order. This is a structural requirement, which is why §1 and §6 carry mandated plain-terms
subsections and §7 opens with S4.

The plain version is not a summary of the technical one and must not be written afterwards as a
courtesy. It is the argument, stated in quantities the reader can hold — and if it cannot be stated that
way, that is usually a sign the technical version is confused rather than merely difficult.

## 3.2 One organising analogy, economics-native, carried through

Choose a single analogy in §1.1 and reuse it whenever the reader needs re-anchoring. It must come from
the reader's own field. A.12 used a factory whose output is orders times units-per-order, returned to it
at §6.1, and never introduced a second analogy.

Two failure modes to avoid: **switching analogies** mid-chapter, which costs the reader everything they
had built; and **analogies from demography**, which explain the unfamiliar with the unfamiliar.

## 3.3 Gloss demographic vocabulary at first use, inline

One clause, in the sentence where the term first appears — not a glossary, not a footnote. "the **total
fertility rate** (TFR: the number of children a woman would bear if she experienced current age-specific
birth rates throughout her reproductive life)". Assume none of: TFR, parity, completed and cohort
fertility, tempo and quantum, replacement, DZ/MZ, PM/FDT/SDT, ART, eSET, GRADE, PRISMA.

Economics vocabulary needs no gloss. Do not explain what an instrument is.

## 3.4 State limits in the text, at the point where they bite

Three specific obligations, all of which A.12 exercised:

- **Retrieval fraction in the status line and again in Provenance** (S6). A chapter written on a
  quarter of its evidence is a different object from one written on all of it, and the reader learns
  that in the header, not on page nine.
- **Separate what survives from what does not** (S7). Not every finding depends equally on the unread
  material. Saying which is which converts an unqualified caveat into usable information.
- **If the chapter was written over a stated objection, record the objection and who made it.** A
  disagreement about whether the evidence was sufficient belongs in the document, not only in the
  ticket.

Additionally, **mark numbers sourced from abstracts rather than full text**, and list them on the
residual retrieval list. An abstract-sourced number is usable and should be used; it is not the same
evidence as a read result and the reader is entitled to know which is which.

## 3.5 The verdict must survive being read alone

§9 will be read by people who read nothing else. It states what is true, how big it is, what the single
carry-away number is, and what would change it — without requiring §§1–8. Qualifications that change the
verdict belong *in* it; qualifications that do not, belong below it.

---

## Checklist before marking a chapter draft complete

- [ ] S1–S7 present, in the specified sections, in the specified forms
- [ ] §1.1 and §6.1 lead with plain terms; §7 opens with S4 before any arithmetic
- [ ] One organising analogy, economics-native, introduced in §1.1 and reused
- [ ] Every demographic term glossed at first use, inline
- [ ] Estimand, units and counterfactual named; identity separated from behavioural parameter
- [ ] Naive estimator identified, its bias direction stated, and disagreements **resolved rather than averaged**
- [ ] Attrition ledger run; signs reported; net direction stated in the verdict if they agree
- [ ] Units check before arithmetic; endogeneity of the mechanism to the phenomenon checked
- [ ] GRADE per phenomenon, every downgrade named
- [ ] Retrieval fraction in the status line and Provenance; survives/does-not-survive split stated
- [ ] Abstract-sourced numbers marked and on the residual retrieval list
- [ ] Verdict readable cold
