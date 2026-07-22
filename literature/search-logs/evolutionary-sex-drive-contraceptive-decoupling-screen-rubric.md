# Blinded title/abstract screening rubric — evolutionary sex drive & contraceptive decoupling (B.1)

## Review question

Does the paper bear on **B.1** — the claim that human fertility is a by-product of an evolved drive for
*sex*, not for *children*, so that once contraception decouples sex from reproduction, fertility falls
**even with the preference for children held fixed**? Two things are in the primary estimand: (a) the
**decoupling / dissociation of sex from reproduction**, and (b) **fertility falling independently of any
fall in the desire for children**. Preserve the evolutionary-theory and biosocial-model stream, but
route it outside the empirical primary estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. When the abstract is missing or cannot distinguish a plausible relevant paper, use `UNCERTAIN`;
do not infer findings from author, journal, or title fragments.

## THE LOAD-BEARING BOUNDARY (B.1 vs A.2)

Most contraception papers belong to **A.2 (proximate contraceptive technology)**, NOT here.

- **A.2 asks:** given that people want fewer children, how does cheap effective contraception help them
  hit that target? Its estimand is closing the *desired–realized gap* / reducing *unwanted* births.
  Route these to `OFF_EXPOSURE_A2`.
- **B.1 asks:** why does contraception depress fertility *in the first place*? Its estimand is the
  decoupling of sex from reproduction and the *absence of an evolved positive demand for children* —
  fertility falling *without* a fall in child preference.

A paper is B.1-primary ONLY if it speaks to the decoupling/dissociation itself, OR to fertility
declining while the preference for children is held fixed or unchanged. A paper showing contraception
reduces *unwanted* births among people who already want fewer children is **A.2** → `OFF_EXPOSURE_A2`.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_DECOUPLING | PRIMARY_DESIRE_INDEPENDENCE | PROXIMATE_ULTIMATE | MOTIVATION_DISTINCTNESS | THEORY | TEMPO_EXPOSURE | OFF_EXPOSURE_A2 | OFF_OUTCOME | REVERSE | CULTURAL_NORMALIZATION | NA",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "holds_child_preference_fixed": "yes | no | unclear",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: directly studies or models the sex–reproduction decoupling, the dissociation of an
  evolutionary predictor from realized fertility once contraception is available, fertility falling with
  child-preference held fixed, or the distinctness/weakness of reproductive vs sexual motivation.
- `UNCERTAIN`: plausibly belongs, but missing/ambiguous information prevents confident routing.
- `NOT_RELEVANT`: does not bear on the decoupling or the desire-independence estimand. General
  contraception-access, fertility-decline, or evolutionary-psychology papers are NOT automatically
  relevant.

## Estimand cells

- `PRIMARY_DECOUPLING`: contraceptive access/adoption as the severing technology, or a natural test of
  the sex↔reproduction link → realized fertility dissociating from a determinant of sexual
  activity/exposure (status, mating effort, coital frequency, union).
- `PRIMARY_DESIRE_INDEPENDENCE`: contraceptive access/adoption → fertility falls holding desired family
  size / preference for children fixed.
- `PROXIMATE_ULTIMATE`: an evolutionary predictor of fertility (status, wealth, mating effort) → a
  sexual/mating outcome vs a reproductive outcome, especially pre- vs post-contraception (Pérusse-type
  dissociation test).
- `MOTIVATION_DISTINCTNESS`: evidence that reproductive motivation is a psychological construct distinct
  from, and weaker than, sexual motivation (childbearing-motivation / desire-for-children work).
- `THEORY`: evolutionary / biosocial model of the mismatch, sex drive, or absence of a child-drive, with
  no empirical fertility estimate.
- `TEMPO_EXPOSURE`: coital frequency / exposure change → fecundability or birth timing only. Route to
  A.4 (coital-frequency-biological) unless the decoupling itself is the object.
- `OFF_EXPOSURE_A2`: contraceptive availability/cost closing the desired–realized gap → unwanted births
  / realized fertility among those already wanting fewer. Route to A.2.
- `OFF_OUTCOME`: mating psychology, sexual behavior, or the status–sex link with NO fertility outcome;
  or a covered variable → a non-fertility outcome (labor, marriage, education, health). Mechanism/context
  only.
- `REVERSE`: fertility / family size → sexual behavior or contraceptive adoption.
- `CULTURAL_NORMALIZATION`: postmaterialist / normative legitimation of contraceptive use → fertility.
  Cross-ref D.1.a; not the biological estimand.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a decoupling/dissociation OR desire-independence mechanism AND a fertility (or sexual-vs-
   reproductive) outcome must be present for a PRIMARY cell.
2. A contraception→fertility study identified purely off contraceptive cost/availability, framed as
   closing a desired–realized gap, is `OFF_EXPOSURE_A2` even if it mentions evolution in passing.
3. A study of status/wealth → labor, marriage, or education (no fertility or reproductive-success
   outcome) is `OFF_OUTCOME`, even when it cites the pill/contraception as an instrument.
4. Do not promote an `OFF_OUTCOME` or `OFF_EXPOSURE_A2` paper to PRIMARY merely because decoupling or
   evolution is mentioned as motivation.
5. Reviews may be `RELEVANT` but cannot be PRIMARY; use the best non-primary cell and
   `evidence_type=review`.
6. Set `holds_child_preference_fixed=yes` only when the design actually holds desired family size /
   child preference constant; this is the clause that separates B.1 (`PRIMARY_DESIRE_INDEPENDENCE`)
   from A.2 (`OFF_EXPOSURE_A2`).
