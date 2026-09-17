# A.6 screen log

Decisions live in `extraction/stigma-reduction-contraception-abortion-screened.csv`.
Cells and tags are defined by
`stigma-reduction-contraception-abortion-screen-rubric.md`. Tallies below are generated
by `source/build/goldset/411_a6_apply_s4_screen.py`; do not edit by hand.

## Batch 1 — S1_DECISIVE, S2_BRIDGE, S3_DESIGN_USE (exhaustive, 12 records)

Hand-screened and recorded directly in the CSV. The whole of S1 is one record.

## Batch 2 — S4_FERT_NODESIGN (exhaustive, 152 records)

Every record read on title, flags and abstract snippet. No cell was added mid-screen:
the rubric's existing cells absorbed all 152, which is itself weak evidence that the
rubric's cell list is adequate to this literature.

## Tally across 164 screened records

| cell | n |
|---|---|
| `CONTEXT_STIGMA_MEASURE` | 63 |
| `OFF_OTHER` | 27 |
| `MIXED_NORM_SUPPLY` | 24 |
| `LINK_NORM_USE` | 24 |
| `MIXED_NORM_DIFFUSION` | 10 |
| `INSUFFICIENT_INFO` | 8 |
| `OFF_HIV_STIGMA` | 3 |
| `MIXED_NORM_SECULAR` | 2 |
| `MIXED_NORM_TECH` | 1 |
| `OFF_OTHER_STIGMA` | 1 |
| `MIXED_NORM_LAW` | 1 |

| stratum | screened |
|---|---|
| `S1_DECISIVE` | 1 |
| `S2_BRIDGE` | 8 |
| `S3_DESIGN_USE` | 3 |
| `S4_FERT_NODESIGN` | 152 |

## `PRIMARY_NORM_FERTILITY`: **0**

Empty. Every stratum in which a primary-cell study could appear has now been read
exhaustively — S1 (exposure + design + fertility outcome), S2 (the citation
bridges), S3 (exposure + design + use outcome) and S4 (exposure + fertility
outcome, no design marker) — 164 records in total, and none estimates the effect of
a normative exposure on realized fertility.

This is the fifth independent channel to agree (scope §15 lists four). It is not yet
a closed result: the records below are unresolved and each could in principle
carry the missing estimate.

## `INSUFFICIENT_INFO` — full text required: **8**

| id | stratum | why |
|---|---|---|
| `W108787496` | S1_DECISIVE | Only S1 record and highest-degree record in the pool (cited by 5 seeds). 2014 dissertation on why fertility preferences diverge from realized fertilit |
| `W2885614896` | S2_BRIDGE | No abstract in index. Title - factors influencing adolescents' access to and utilisation of safe abortion services, Upper East Ghana - points at acces |
| `W2112312272` | S4_FERT_NODESIGN | Fertility outcome across countries; exposure may be normative. FULL TEXT. |
| `W1986910339` | S4_FERT_NODESIGN | Persistent high fertility in the southeast; exposure may be normative. FULL TEXT. |
| `W3121483375` | S4_FERT_NODESIGN | Religious beliefs, contraceptive use and long-run development - the closest thing in S4 to an identified economic estimate. Sits on wall 5 (D.1.a) and |
| `W4403200839` | S4_FERT_NODESIGN | Title alone cannot separate desire from norm, and the outcome may be realized. FULL TEXT. |
| `W1976018943` | S4_FERT_NODESIGN | Partner opposition as exposure AND the decision to STOP CHILDBEARING as an outcome - the one S4 record whose outcome may be parity rather than use. FU |
| `W2187750596` | S4_FERT_NODESIGN | Cultural persistence and the pill; an economics paper that may identify a norm effect separately from the technology. Sits on wall 1. FULL TEXT. |

## Not yet screened

S5_EXPOSURE 515 (120 sampled), S6_WEAK 1,650 (60 sampled), S7_NOABSTRACT 486 (60
sampled) — the sampled tail, plus both term arms from scope §14. The absence claim
rests on the exhaustive strata; the sample exists to bound the chance that the
flagger misrouted a primary-cell study out of them, and it has not yet been read.

## Full-text stage (`412`, `413`)

`412` retrieved **2 of 8** of the unresolved records. Six remain `oa_status: closed` with no PDF in
OpenAlex or Unpaywall; they are on the library wantlist, not resolved.

### The decider, read

`W108787496` — *Essays on Fertility and Fertility Preferences in India* (Rajan, Duke,
2014), 40,538 words, retrieved through the DSpace REST API after the plain bitstream
URL returned HTML.

| chapter | exposure | dependent variable | verdict |
|---|---|---|---|
| ch2 | accounting decomposition of the preference-behaviour gap | realized fertility | a framework, not a norm effect |
| ch3 | education, two-way fixed effects | **Desired Family Size** | `outcome_level: DESIRED`; exposure not normative |
| ch4 | **community norms**, multilevel logit with community-level predictors | **Contraceptive Use** — odds of spacing, odds of stopping | A.6's exposure, but a use outcome |

Chapter 4 is A.6's exposure almost exactly, and its outcome is use. Under ruling 2 the
decider is **`LINK_NORM_USE`** — the best-designed record this chapter has found, and
not an estimate of its parameter. The record with the strongest prior in the whole
2,815-record pool fails the same way every other near-miss failed: on the outcome, not
on the exposure.

### `PRIMARY_NORM_FERTILITY`: **0**

Empty, and now closed as far as retrievable evidence allows. Every stratum that
could contain a primary-cell study has been read exhaustively (164 records), and
the single highest-prior record has been read at full text rather than inferred
from an abstract. Six channels agree: the identified-design share (12/668), the
realized-fertility share (58/668), anchor reachability (0/15 on the stage-2
frame), the citation bridge test (8, none an estimate), the exhaustive screen (0
of 164) and now the full text of the decider.

Per scope §12 the verdict is **UNEVALUATED with the failed route named** — R1 for
want of an identified fertility outcome, R3 for want of a pre-1985 dose series —
and explicitly not 'weak evidence'.

`LINK_NORM_USE` stands at **25** records and is poolable under scope
§12 stratum 3. It must be reported under a heading that disclaims it as the
chapter's parameter.

### Still blocked: **6**

| id | why it is blocked |
|---|---|
| `W2112312272` | Fertility outcome across countries; exposure may be normative. FULL TEXT. |
| `W1986910339` | Persistent high fertility in the southeast; exposure may be normative. FULL TEXT. |
| `W3121483375` | Religious beliefs, contraceptive use and long-run development - the closest thing in S4 to an identified economic estima |
| `W4403200839` | Title alone cannot separate desire from norm, and the outcome may be realized. FULL TEXT. |
| `W1976018943` | Partner opposition as exposure AND the decision to STOP CHILDBEARING as an outcome - the one S4 record whose outcome may |
| `W2187750596` | Cultural persistence and the pill; an economics paper that may identify a norm effect separately from the technology. Si |

### Tally across 164 screened records

| cell | n |
|---|---|
| `CONTEXT_STIGMA_MEASURE` | 63 |
| `OFF_OTHER` | 27 |
| `LINK_NORM_USE` | 25 |
| `MIXED_NORM_SUPPLY` | 25 |
| `MIXED_NORM_DIFFUSION` | 10 |
| `INSUFFICIENT_INFO` | 6 |
| `OFF_HIV_STIGMA` | 3 |
| `MIXED_NORM_SECULAR` | 2 |
| `MIXED_NORM_TECH` | 1 |
| `OFF_OTHER_STIGMA` | 1 |
| `MIXED_NORM_LAW` | 1 |
