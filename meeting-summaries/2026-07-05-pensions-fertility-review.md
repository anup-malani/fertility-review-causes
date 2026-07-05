# Meeting Summary — Pensions & Fertility Meta-Analysis: Research Review

**Date:** 2026-07-05
**Attendees:** Anup Malani (PI), Alexandra Zhou (RA), Shravan Haribalaraman (RA)
**Source:** Notion meeting notes (Fertility → Fertility-review-cause → Meeting 260705)

---

## Action items

**Shravan**
- Finalize the coarse filter, run the fine filter, and write both up clearly in plain English.
- Apply the coarse-and-fine-filter methodology to the pensions-fertility chapter. If that is finished
  by midweek, apply it to one or two additional hypotheses from the list.

**Alexandra**
- Finish building the meta-analysis infrastructure (Codex trained on Cochrane reviews and JEL
  articles), then apply it to the pensions-fertility chapter by midweek if possible.
- Draft a first draft of the pensions-fertility chapter.

**Anup**
- Finish the independent paper review and send it to Alexandra.
- Send both collaborators the style guide as a markdown file.
- Draft an independent version of the chapter for comparison with Alexandra's draft.

---

## Key substantive findings on pensions & fertility

- **First demographic transition.** Pensions are moderately credible as a driver of the fertility
  decline, but confidence is limited.
- **Second demographic transition.** Pensions appear to work in the *opposite* direction: when
  grandparents receive pensions, they help with childcare, which *increases* their children's
  fertility. This inverse effect was flagged as a novel finding, not part of the standard narrative.
- **Corpus size.** Roughly 10–15 empirical papers carry extractable, comparable effect-size estimates
  on this topic; about 20 if the "retired parents helping with childcare" mechanism is included.

## Paper categorization strategy

- Papers that relate to fertility only indirectly (e.g., pensions → schooling) are hard to categorize
  and may themselves be incomplete, because they skip intermediate causal steps such as the
  quantity-quality channel.
- **Recommendation:** park ambiguous papers in an appendix attached to the relevant chapter (e.g., the
  pensions chapter). Do not discard them, but do not feature them as prominently as the direct studies.
- **Organizing principle:** the treatment variable determines which chapter a paper belongs to.
- Theory papers are included too, per the JEL review model, which reviews both theory and empirical
  evidence.

## Screening and filtering methodology

- Current AI screening is too lenient: it is not filtering out papers unrelated to fertility.
- Two options were weighed. (A) Keep the initial search broad to avoid false negatives, then narrow
  later. (B) Specify treatment and outcome variables strictly up front.
- **Decision: option A.** Use a coarse filter first (broad search), then a fine filter that
  characterizes treatment, outcome, causal direction, time period (pre-modern / first DT / second DT),
  and theory type.
- Document the screening process and the Cochrane-style methodology steps so they can be described
  transparently in the write-up.

## Paper structure and presentation

- The choice was between the economics convention (methods first) and the PNAS/Nature style (results
  first, methods in supplementary materials).
- **Decision:** the likely audience is more consumers than producers of fertility research, so lead
  with a reader-friendly structure — logic and punchline first — and put the Cochrane-style methodology
  in supplementary materials.
- The main paper should still carry, for each causal connection: the theory, a summary of the empirical
  evidence, the time-period applicability, and an evaluation of internal validity, external validity,
  and R-squared.
- Two distinct back-of-paper sections: (1) the *appendix*, a parking lot for ambiguous papers, and
  (2) *supplementary materials*, the methodology detail for producers to scrutinize.

## R-squared and the causal-apportionment challenge

- Evaluating 15–30 causal theories independently may produce R-squareds that sum to more than one,
  because many of the causes overlap conceptually.
- A partial-R-squared approach would be the right fix but is hard in a meta-analytic setting.
- Rough approach: bound the total causal impact, then allocate it across theories by their relative
  R-squareds.
- Many economics papers do not report R-squareds at all, favoring statistical inference over economic
  significance. Where the number is unavailable, the honest answer is to say we do not know and flag it
  as a gap for future research.
