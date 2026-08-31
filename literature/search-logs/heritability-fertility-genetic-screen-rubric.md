# A.18 title/abstract screen rubric

**Question.** Does this record estimate a **genetic** contribution to a **realized fertility
outcome** in **humans**?

## verdict
- `RELEVANT` — plausibly in scope on the visible record.
- `NOT_RELEVANT` — out of scope on the visible record.
- `UNCERTAIN` — cannot decide. Pairs with `info: insufficient`.

## The walls, stated as rejections
- **Wall 1 (→ A.19).** A parent–child fertility correlation with **no decomposition** is
  NOT_RELEVANT here. It is equally consistent with pure social transmission and is therefore not
  evidence for A.18. Set `decomposes: no`.
- **Wall 3 (→ B.1).** Phenotypic **status** → fertility is NOT_RELEVANT. The predictor must be a
  genetic measure, not an achieved characteristic.
- **Wall 4 (→ A.15/A.16/B.3/B.4).** Heritability of a **fecundity trait** — age at menopause, PCOS,
  sperm concentration — with no realized-birth outcome is `LINK_TRAIT`, not a primary record.
- **Wall 5.** A genetic study of a **non-fertility phenotype** (education, cognition, height,
  psychiatric) is NOT_RELEVANT unless fertility is an outcome.
- **Wall 6.** Non-human study organism is NOT_RELEVANT.

## Fields
- `cell` — one of: `H2_FERTILITY`, `H2_MODERATION`, `SELECTION_DIFFERENTIAL`, `ALLELE_FREQ_TREND`,
  `PEDIGREE_RESPONSE`, `PREDICTED_RESPONSE`, `WITHIN_VS_POPULATION`, `LINK_TRAIT`, `UNDECOMPOSED`,
  `OFF_STATUS_B1`, `OFF_SPECIES`, `THEORY`, `INSUFFICIENT_INFO`.
- `arm` — `H2` / `H2_MOD` / `SELECTION` / `METHOD` / `THEORY` / `NONE`.
- `decomposes` — `yes` / `no` / `cannot_tell`. **The field this screen exists for.**
- `phenotype` — `FERTILITY_OUTCOME` / `FECUNDITY_TRAIT` / `OTHER_PHENOTYPE` / `NONE_VISIBLE`.
- `exposure_distance` — `FERTILITY_PGS` / `AFB_PGS` / `EDUCATION_PGS` / `OTHER_CORRELATED_PGS` /
  `ANONYMOUS_VARIANCE` (twin h², no variant named) / `NOT_GENETIC`.
- `info` — `sufficient` / `insufficient`.

## Standing instructions
- **`cannot_tell` and `insufficient` are first-class.** Their SHARE is a measurement: it decides how
  much routing moves to the RA gate and to full text. Do not guess to avoid them.
- **No abstract is not a negative verdict.** Title-only records take `info: insufficient` unless the
  title alone is decisive.
- Phenomenon (PM/FDT/SDT) is NOT screened here. Ruling 2 made all three live and the window is a
  full-text fact.
