# D.1.a — Tier-A anchor relabelling

The first clean calibration scored 7/10 on the decoys. Adjudicating each disagreement showed **the screen was right more often than the anchor set was** — the calibration was measuring the anchor set as much as the screen.

## The trap this avoids

Correcting only the labels the screen disputed would **fit the gold to the screen**: every later calibration would score better by construction and would be measuring nothing. All 48 anchors were re-read against the scope, and the corrections below are keyed to text quoted from the record rather than to any verdict. **One correction makes the screen's verdict more wrong, not less**, which is the check that this was not a ratification.

## The flip rule

A label changes only where the abstract **explicitly states** the dependent variable and it is not fertility, or explicitly states the treatment and it is not a measured value. **Title-only records are never flipped** — 34 of the 48 labels were assigned before abstracts were joined, which is how these errors got in, and guessing harder from the same title is not a repair.

- corrections applied: **3**
- re-read, disputed, and deliberately left alone: **5**

## Corrections

### Does individualism promote gender equality

- **{'role': 'DECOY', 'pair': 'S2', 'provisional_cell': 'OFF_OUTCOME'} → {'role': 'EMPIRICAL', 'pair': 'S2', 'provisional_cell': 'PRIMARY_INDIVIDUALISM_S2'}**
- evidence: Abstract: "Individualism is also associated with greater levels of female employment and educational attainment, and lower levels of fertility." The treatment is a measured WVS individualism scale and fertility is a reported outcome, so both routing questions are yes.
- why the old label was wrong: The DECOY/OFF_OUTCOME label was assigned from the title alone, where the only visible outcome is gender equality. The abstract was joined to this record only in this run.

### Demographic Imperatives and Religious Markets

- **{'role': 'EMPIRICAL', 'pair': 'S3', 'provisional_cell': 'PRIMARY_SECULAR_S3'} → {'role': 'REVERSE', 'pair': 'S3', 'provisional_cell': 'VALUE_CONSTRUCT'}**
- evidence: Abstract: the models seek to explain "the growth and decline of religious groups", with "switching and fertility" as the mechanisms of growth. The dependent variable is religious-group size and fertility is a regressor -- the D.1.a pair inverted.
- why the old label was wrong: Labelled a primary S3 estimate on a title that reads as religion-and-fertility. It is the reverse arrow and belongs with the risk-of-bias material.

### How religion mediates the fertility response to maternity benefits

- **{'role': 'DECOY', 'pair': 'DECOY', 'provisional_cell': 'OFF_OTHER'} → {'role': 'DECOY', 'pair': 'DECOY', 'provisional_cell': 'VALUE_AS_MODERATOR'}**
- evidence: Abstract: a difference-in-differences on "a 1982 maternity benefits expansion" comparing "women who did and did not grow up in religious households". The design moves the benefit; religiosity splits the sample.
- why the old label was wrong: Not wrong so much as homeless: OFF_OTHER was the only available route-away cell. The rubric's new moderator rule gives it the cell that names what it actually is. **This correction makes the calibration HARDER, not easier** -- the screen assigned it PRIMARY_SECULAR_S3, and it is now scored against a specific cell rather than a catch-all.

## Contested — left at their current label, escalated to a second human rater

**`CONTESTED` is not a diplomatic null.** These stay in the gold unchanged, so the calibration denominator does not move and no number changes quietly. They need a second rater per the RA playbook.

- **Postmaterialism and voluntary childlessness** — Labelled DECOY / NORM_ACCEPTABILITY_DESCRIPTIVE (degenerate under Ruling 2). The abstract says it asks "how citizen values relate to decisions to not have children" using WVS Wave 7 -- which reads as an S1 value measure against a childlessness outcome, i.e. NOT degenerate. **Ruling 2 turns on the scale's item content, which the abstract does not give.** This is exactly the case the rubric binds to UNCERTAIN + needs_full_text; the label cannot be settled here either.

- **The relationship between social status and biological success** — Labelled EMPIRICAL / PRIMARY_SECULAR_S3. The title names a social-status gradient as the regressor, which is D.1.c's treatment, but the setting is a religious hierarchy where rank may itself proxy religiosity. No abstract. Not flipped on a title.

- **Religious Affiliation, Participation and Fertility: A Cautionary Note** — Labelled EMPIRICAL / PRIMARY_SECULAR_S3. The abstract is about participation measures being "empirically problematic with the typical cross-sectional data set" -- a methodological note on reverse ordering. Whether it also reports a usable estimate is not visible.

- **Cultural Dynamics and Economic Theories of Fertility Change** — Labelled EMPIRICAL / PRIMARY_POSTMATERIAL_S1. The abstract describes theories being "correlated" and "considered" and names no data or design, which reads as THEORY, but it is a 1980s abstract style and absence of a described design is not absence of one.

- **Differences in Fertility Patterns between East and West German Women** — Labelled EMPIRICAL / PRIMARY_VALUE_EX_ANTE. The abstract disentangles "cultural background and institutional context" using East/West origin -- a place, not a measured value. Wall 7 (measured versus narrated) may route this out, but the paper may also carry a measured value covariate the abstract omits.

