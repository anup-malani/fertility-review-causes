# Chapter Template

**Status:** Authoritative. Supersedes the section skeleton in `output/chapters/hybrid-chapter-template.md`
and expands `PROTOCOL.md` §6.  
**Companion:** `docs/chapter-writing-style-guide.md` owns prose rules. This document owns structure and
analysis, and defers to that guide for sentence-level style rather than repeating it.  
**Author:** Shravan, 2026-08-22, generalised from A.12 (`twinning-multiple-births`).

This template is built in three layers, and they are meant to be worked in this order:

> **Organizational structure → Statistics, economics and demography → Writing**

Get the sections and their commitments fixed first; then decide what quantity each section must
establish; only then write. A chapter that is written before its estimand is named will describe a
literature instead of answering a question.

---

## 0. Audience, fixed once for the whole review

**Write for a University of Chicago undergraduate who understands economics but not demography.**

That reader has an understanding of price theory, identification, selection, elasticities, margins, and income and substitution effects. They are new to the ideas like total fertility rate, parity, tempo and quantum, cohort versus period measures, or the three target phenomena. The asymmetry is the single most useful fact about the audience and it has two consequences that run through every layer below:

- **Use language the reader is familiar with.** Frame mechanisms in the vocabulary they already own. An
  intensive/extensive margin split, a target-stock income effect, a selection-on-the-dependent-variable
  problem — these cost nothing to introduce.
- **Explicitly define the rest, always.** Every demographic term in every chapter is defined at first use, inline, in one clause.
  Never assume TFR, parity, DZ/MZ, replacement, PM/FDT/SDT, GRADE or eSET.

---

# Layer 1 — Organizational structure

## 1.1 The mandatory sentences

Seven sentences appear, in these forms, in **every** chapter, in the exact place that they are stated to appear in. They are not stylistic. Each forces a
commitment the chapter could otherwise avoid making. The point is to ensure consistency across the different chapters.

| # | Where | Sentence |
|---|---|---|
| **S1** | §1, first line, before anything else | **"This chapter explores the effect of [TREATMENT] on [OUTCOME]."** |
| **S2** | §1.1, opening the plain-terms passage | **"In plain terms: [THE CLAIM, IN ORDINARY LANGUAGE]."** |
| **S3** | §1.2 | **"The parameter this chapter estimates is [ESTIMAND], measured in [UNITS]."** |
| **S4** | §8, before any arithmetic | **"The phenomenon to be explained is measured in [UNITS OF PHENOMENON]; this mechanism offers [UNITS OF MECHANISM]."** |
| **S5** | §8.1, §8.2, §8.3 — once each | **"For [PM / FDT / SDT], the verdict is [NEGLIGIBLE / MINOR / SUBSTANTIAL / DOMINANT / NOT ASSESSED], because [ONE CLAUSE]."** |
| **S6** | Provenance block | **"This chapter is written on [n] of [m] wanted full texts ([p]%)."** |
| **S7** | Provenance block | **"The findings that would survive full retrieval are [X]; the findings that might not are [Y]."** |

Worked from A.12, so the register is visible:

- **S1** — "This chapter explores the effect of the twinning rate on the total fertility rate."
- **S2** — "In plain terms: a woman who has twins ends up with two children from one pregnancy, so
  where twins are more common, women could end up with more children without having to be pregnant
  more often."
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
| **1** | The claim | First, explain the claim in layperson's terms; this means no economic lingo, no fertility lingo. Don't analogize, explain directly the claim using simple vocabulary that anyone can understand. Then, expand on this by explaining the claim in a technical manner. |
| **2** | Theoretical mechanism | Explain the proposed mechanism in the reader's economics vocabulary. Cover the identity/behaviour split if there is one, and explain what kind of behavior would make the hypothesis wrong. |
| **3** | Search strategy | Reproducible; walls and their enforceability; any wall declared unenforceable **in advance**; boundary rulings against neighbouring hypotheses |
| **4** | PRISMA flow | The funnel table, plus the two or three features of it that change how the chapter should be read |
| **5** | The ideal design | **5.1** the ideal estimand, stated precisely enough to be a study protocol; **5.2** the design that would identify it; **5.3** the distance table rating every included study against it. See §2.6 |
| **6** | Included studies | Table with design column; the estimator-disagreement analysis (§2.2 below) |
| **7** | Quantitative synthesis | **7.1 The answer in plain terms first**, then **7.2 The estimate**. Follow the same structure as in 1. |
| **8** | Demographic significance | S4, then 8.1 PM / 8.2 FDT / 8.3 SDT, each carrying S5 |
| **9** | GRADE rating | Per-phenomenon table with every downgrade named |
| **10** | Verdict | Standalone and readable without much context; one number a reader carries away |
| **11** | Open questions | PI calls, retrieval priorities, and studies that do not exist and should |
| **12** | References | |
| — | **Provenance and standing caveats** | S6, S7, any objection over which the chapter was written, and which numbers came from abstracts rather than full text |

**Non-negotiable orderings.** All of these sections come in this exact order. Plain terms precede technical statement in §1 and §7. S4 precedes all
arithmetic in §8. The verdict (§10) is written so it survives being read alone, because it will be.

---

# Layer 2 — Statistics, economics and demography

Now that the structure is fixed, decide what each section must *establish*. This layer is the chapter's spine and it is
where chapters go wrong invisibly.

## 2.1 Name the estimand before reading anything

Three questions, answered in writing before the literature is opened:

1. **What is the parameter, in what units, with what sign convention?** (S3)
2. **What is the counterfactual?** State the precise counterfactual as a ceteris-paribus perturbation. If it cannot be stated
   that way, the parameter is not identified and the chapter must say so and downgrade for
   indirectness — not quietly report a measured share as though it were an estimated effect.
3. **Is this an identity, a behavioural parameter, or both?** If both, they need different treatment and
   the registry entry probably runs them together.

**The identity/behaviour split.** An accounting identity cannot be false and needs no study; the
behavioural response to it is the only place the hypothesis can be wrong. Chapters that miss this
search for effect estimates in a cell populated by statistical tabulations, find none, and wrongly
report the literature as thin.

**Margins.** Say explicitly whether the mechanism moves the extensive margin (a binary change) or the
intensive margin (a level change). Reviewers and readers both track this, and it is the cleanest
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

**Therefore, for every chapter, run this check explicitly and report it in §6:**

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

**Name the denominator, every time. `PROTOCOL.md` §4.2.1 fixes which one.** This is the single most
frequently broken rule in the review — it has been caught in four chapters, breaking in both directions,
and it moves verdicts across band boundaries:

- **A change, never a level.** A mechanism worth 4.5% of the birth *level* is worth roughly twice that
  of a *decline* which is itself about half the level. D.3.b's predecessor reported a share of the level
  in a table banded as a share of the phenomenon; the error understated the mechanism and read as
  reassuring, which is why it survived review.
- **The phenomenon's full window, not the study's.** The old-age-security chapter's Cell C screen
  divided by 0.097 births — a seventeen-year drift in Dutch fertility — and returned shares up to 273%.
  The compulsory-education chapter's share moves from 4.8% to about 10%, across a band boundary, on the
  same choice. **A share above 100% is the diagnostic**: no mechanism explains more than all of the
  thing it explains, so a share above one identifies a wrong denominator, not a large effect.
- **Shared units.** A probability-of-birth effect over a TFR change is not a share of anything.
- **All four of numerator, denominator, source and window, at the point the share is given.** A share
  whose denominator is not named is not reportable.

If only a study-window share exists, report it, label it as such, and **do not band it**. Convert it or
record NOT ASSESSED. Where the denominator cannot be obtained at all — the UN panel is not in this
repository — invert the question and report the **break-even**: the largest phenomenon for which the
mechanism's magnitude still clears a given band. That is computable from the magnitude alone and lets a
reader with the panel substitute the real denominator without redoing the analysis.

**Then the endogeneity check, which is easy to skip and expensive to miss.** Ask whether the mechanism's
movement is itself *caused by* the phenomenon being explained. On A.12 a quarter of the modern twinning
rise is driven by delayed childbearing — which is the very postponement the hypothesis claims to
offset. A feedback of a decline cannot be evidence against the decline's cause, and that component must
be netted out before any offset is claimed.

**Verdict vocabulary, fixed** (used in S5): **NEGLIGIBLE** (<5% of the phenomenon) · **MINOR** (5–20%) ·
**SUBSTANTIAL** (20–50%) · **DOMINANT** (>50%) · **NOT ASSESSED** (no share was computed, either because
the phenomenon is out of scope for this hypothesis in the registry or because the cell is in scope and
empty; say which of the two it is, and say what the sign would be if it were assessed).

NOT ASSESSED is not a weak verdict, and it must not be softened into NEGLIGIBLE. NEGLIGIBLE asserts that
a share was computed and came out under 5%; NOT ASSESSED says no share exists. Reporting an empty cell as
NEGLIGIBLE claims a measurement that was never made.

## 2.5 GRADE

Per phenomenon, not per chapter — the same evidence can be strong for one target and weak for another.
Start from the available designs and downgrade for named defects: **imprecision**, **risk of bias in the
body as a whole**, **indirectness** (the evidence answers a neighbouring question), **inconsistency**,
**publication bias**. Every downgrade names its reason in the table. A chapter with a HIGH rating for a
*negligible* effect is a perfectly coherent and common result — certainty about the size of an effect is
not the same as the effect being large.

**When a phenomenon's cell contains no studies, the rating is No evidence.** It is not VERY LOW. GRADE
rates a body of evidence, and VERY LOW describes one that exists and is badly identified — which
misdescribes an empty cell and makes it look as though the question has been investigated and answered
poorly. A No evidence row names what would have to exist to earn a rating. It pairs with a NOT ASSESSED
demographic-significance verdict.

## 2.6 The ideal design, and the distance from it

**Before reading what the literature did, write down what you wish it had done.** §5 of every chapter
states the study that would answer the question exactly, in enough detail that someone could run it,
and then rates each included study by how far it sits from that study. Written after the literature is
read, this section becomes a description of the best available paper. Written before, it is a fixed
yardstick that does not move when the evidence turns out to be disappointing — which is the whole point.

**5.1 The ideal estimand.** Sharper than S3, which names the parameter. This names the *study*: the
population, the exact treatment contrast including its dose and units, the outcome and the horizon over
which it is observed, and the units of the resulting coefficient. "The effect of pensions on fertility"
is not an estimand. "The change in completed fertility, in births per woman, of a 10-percentage-point
rise in the old-age replacement rate, among women aged 20–35 at exposure in a setting with no prior
formal pension coverage, observed to age 45" is.

**5.2 The design that would identify it.** State, in this order: the **source of variation** (what
assigns the treatment, and why that assignment is independent of the outcome); the **comparison group**;
the **identifying assumption** in a form that could in principle be falsified; the **estimating
equation**; the **data required**, including the panel length the horizon implies; and the **sample size**
the effect's plausible magnitude demands. Name the design class — RD, event study, IV, DiD with a stated
parallel-trends window — rather than gesturing at "a quasi-experiment".

**5.3 The distance table.** One row per included study, scoring how far each sits from §5.1–5.2 on the
dimensions that matter for that chapter. Always score at least: **exposure** (does the study measure the
registered treatment, or a proxy?), **outcome** (the registered outcome, or an intention, an intermediate,
or a different margin?), **horizon** (long enough to observe the estimand?), and **assignment** (the ideal
source of variation, something weaker, or observational?). A study matching on every dimension is the
chapter's anchor and should be named as such wherever its result is used.

**If a study implements the ideal design, say so immediately and by name, in §5.3 and again wherever its
estimate appears.** One study that identifies the registered estimand outranks any number that do not,
and a chapter that buries it in a table sorted alphabetically has thrown away its own best evidence.

**If none does, the gap is a finding and belongs in the verdict.** "No study estimates this chapter's
estimand" is a stronger and more useful statement than a weak pooled number, and it converts §11's
"studies that do not exist and should" from a wish list into a specification.

---

# Layer 3 — Writing

Structure fixed, analysis fixed, now write. **`docs/chapter-writing-style-guide.md` governs
sentence-level style and is not repeated here.** What follows is what that guide does not cover.

## 3.1 Lay comparison before technical comparison — everywhere, not once

Every substantive comparison in the chapter appears **twice**: once in plain terms, once technically, in
that order. This is a structural requirement, which is why §1 and §7 carry mandated plain-terms
subsections and §8 opens with S4.

The plain version is not a summary of the technical one and must not be written afterwards as a
courtesy. It is the argument, stated in quantities the reader can hold — and if it cannot be stated that
way, that is usually a sign the technical version is confused rather than merely difficult.

## 3.2 One plain explanation of the claim, carried through

**Do not analogise.** State what the claim actually says, in ordinary language, using the real objects
of the hypothesis rather than a stand-in for them. A.12's plain passage is about women, pregnancies and
twins; it is not about a factory. An analogy asks the reader to hold two things at once and to trust
that the mapping between them holds — and the mapping is exactly what breaks down at the point where
the chapter gets interesting.

Write the explanation once in §1.1 and return to *that same explanation* whenever the reader needs
re-anchoring, most often at §7.1. The test is that a reader who knows no economics and no demography
could repeat the claim back correctly after reading §1.1 alone.

Three failure modes to avoid: **reaching for an analogy**, which this section forbids; **switching
explanations** mid-chapter, which costs the reader everything they had built; and **smuggling jargon
into the plain passage**, which explains the unfamiliar with the unfamiliar. Economics vocabulary is
welcome from §1.2 onward and does not belong in §1.1.

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

§10 will be read by people who read nothing else. It states what is true, how big it is, what the single
carry-away number is, and what would change it — without requiring §§1–9. Qualifications that change the
verdict belong *in* it; qualifications that do not, belong below it.

---

## Checklist before marking a chapter draft complete

**Layer 1 — structure**

- [ ] S1–S7 present, in the specified sections, in the specified forms
- [ ] Sections appear in the §1.2 order, none omitted and none resequenced
- [ ] S1 is the first line of §1, before anything else
- [ ] §1 and §7 each explain in layperson's terms first — no economics vocabulary, no demographic vocabulary — and only then technically
- [ ] §8 opens with S4, before any arithmetic
- [ ] One plain explanation of the claim, introduced in §1.1 and reused for re-anchoring; **no analogy anywhere**, and no second explanation introduced later

**Layer 2 — analysis**

- [ ] Estimand, units, sign convention and counterfactual named; identity separated from behavioural parameter
- [ ] Margin named: extensive (a binary change) or intensive (a level change)
- [ ] **Ideal estimand written before the literature was read**, precise enough to be a study protocol: population, treatment contrast with dose and units, outcome, horizon, coefficient units
- [ ] **Ideal design named** with its source of variation, comparison group, falsifiable identifying assumption, estimating equation, data and panel length required
- [ ] **Distance table** scoring every included study on exposure, outcome, horizon and assignment; any study matching the ideal named as the chapter's anchor wherever its estimate is used; if none matches, the gap stated in the verdict
- [ ] Naive estimator identified, its bias direction stated, and disagreements **resolved rather than averaged**
- [ ] Attrition ledger run; signs reported; net direction stated in the verdict if they agree
- [ ] Units check before arithmetic; endogeneity of the mechanism to the phenomenon checked
- [ ] **Every share names its numerator, denominator, denominator source and window**; the denominator is a *change* over the phenomenon's *full* window (`PROTOCOL.md` §4.2.1), not a level and not the study window; no share exceeds 100%; study-window shares are labelled and not banded
- [ ] Demographic significance stated per phenomenon in the fixed vocabulary (NEGLIGIBLE / MINOR / SUBSTANTIAL / DOMINANT / NOT ASSESSED)
- [ ] GRADE per phenomenon, every downgrade named; **No evidence** (not VERY LOW) wherever the cell is empty, paired with NOT ASSESSED

**Layer 3 — writing**

- [ ] Every demographic term defined at first use, inline, in one clause; no economics term glossed
- [ ] Retrieval fraction in the status line and again in Provenance; survives/does-not-survive split stated
- [ ] Any objection the chapter was written over is recorded, with who made it
- [ ] Abstract-sourced numbers marked and on the residual retrieval list
- [ ] Verdict readable on its own, without the rest of the chapter
