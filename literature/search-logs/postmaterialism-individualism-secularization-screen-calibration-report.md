# D.1.a — screen calibration against the pre-labelled Tier-A anchors

48 hand-built anchors with known `role`, `pair` and `design_tier`, blinded and shuffled into the same batch format as production. The screen never sees the key.

- verdicts scored: **48**

## The decisive check — do the 10 decoys route away?

These sit exactly on the boundaries the rubric says will be tested: gender-role attitudes (D.2.a), mass-media exposure (D.1.b / A.20), and religion against *contraceptive use* rather than fertility (`OFF_OUTCOME`). **Each must NOT be `RELEVANT`.**

- routed away correctly: **7/10**
- **admitted as RELEVANT (failures): 3**

| decoy | verdict | cell | reason |
|---|---|---|---|
| Does individualism promote gender equality? | RELEVANT | `PRIMARY_INDIVIDUALISM_S2` | Measured individualism instrumented with rainfall and reported to reduce fertili |
| How religion mediates the fertility response to maternity benefits | RELEVANT | `PRIMARY_SECULAR_S3` | Difference-in-differences in which measured religious upbringing conditions the  |
| Postmaterialism and voluntary childlessness | RELEVANT | `VALUE_CONSTRUCT` | Admissible S1 treatment but the dependent variable is the childbearing-duty norm |

> **A decoy admitted as RELEVANT is a mis-calibration in the direction that costs the chapter.** Fix the rubric or the screener before authorising production.


## Empirical anchors — verdict distribution

**A high `UNCERTAIN` rate here is compliance, not failure.** Three of the scope's routing tests turn on the treatment instrument's item content, which titles and abstracts do not state, and the rubric binds those to `UNCERTAIN` + `needs_full_text`. Scoring UNCERTAIN as an error would push a screener toward the confident-verdict-without-basis failure D.3.b already committed.

- RELEVANT 16 · UNCERTAIN 12 · NOT_RELEVANT 3 (of 31 empirical anchors)
- pair agreement where the screen committed to one: **26/31**

### Empirical anchors the screen REJECTED outright — read every one

A known-empirical anchor called `NOT_RELEVANT` is the expensive error: an `UNCERTAIN` costs one full-text read, a wrong `NOT_RELEVANT` costs the study.

- **Demographic Imperatives and Religious Markets: Considering the Individual and Interactive Roles of F** → `OFF_OUTCOME` — Fertility is a right-hand-side mechanism of denominational growth; the dependent variable is group size, not b
- **Religious Affiliation, Participation and Fertility: A Cautionary Note** → `REVERSE` — The empirical exercise is about reverse temporal ordering — births preceding measured participation — rather t
- **The relationship between social status and biological success: A case study of the Mormon religious ** → `OFF_STATUS_D1c` — Title names a status/prestige gradient as the regressor, which is D.1.c's treatment, not a measured religiosit

