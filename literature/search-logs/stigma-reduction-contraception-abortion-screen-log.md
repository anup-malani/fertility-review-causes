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

## Library full-text stage (`414`, `415`)

Shravan pulled all six remaining records by hand through the UChicago proxy. Four
carry a text layer and were read; two are Wiley page-image scans held at `needs_ocr`,
because a record that cannot be read has not been excluded.

| id | what it is | cell | why |
|---|---|---|---|
| `W1986910339` | Yüceşahin and Özgür 2008, provincial TFR in Turkey by multiple regression | `OFF_OTHER` | **the only library record with a realized-fertility outcome, and it fails on the exposure** — no normative regressor in Table 4 |
| `W2187750596` | Ragan 2012, out-of-wedlock norms and Pill demand in Sweden | `LINK_NORM_USE` | the closest the chapter has come; outcome is Pill demand, so ruling 2 applies |
| `W3121483375` | Prettner and Strulik 2017, two-steady-state theory | `CONTEXT_STIGMA_MEASURE` | theory with numerical simulation; no estimation |
| `W4403200839` | Yeatman and Sennott 2024, conceptual model | `CONTEXT_STIGMA_MEASURE` | framework; separates acceptability from accessibility |

### The near-miss, stated plainly

`W1986910339` is worth dwelling on because it is the mirror image of every other
near-miss in this chapter. Everywhere else the exposure was right and the outcome was
contraceptive use. Here the outcome is right — provincial TFR, 1980–2000 — and the
exposure is wrong: illiteracy, ethnicity shares, female employment, child mortality and
GDP, with no norm dosed at all. The chapter has now failed to find a study with A.6's
exposure and A.6's outcome from both directions.

### Rubric gap — PI call 7

Ragan's exposure is norms about premarital sex and out-of-wedlock childbearing, which
is **D.2.b**'s registered territory, and the rubric has no `MIXED_NORM_MARRIAGE` cell.
S4 position 84 is a second instance, so this is a class. The rubric says to add a cell
and re-run over completed batches; that is deliberately **not** done here, because
which way an A.6/D.2.b boundary should cut is a scope question and D.2.b is not among
the scope doc's six walls. Both records are flagged for second read.

### `PRIMARY_NORM_FERTILITY`: **0** · `LINK_NORM_USE`: **26** · still unreadable: **2**

- `W2112312272` — Caldwell, PDR 1999 - filename says 2004, watermark and DOI say 1999
- `W1976018943` — Wolff, Studies in Family Planning 2000 - filename says 2003, watermark says 2000; the one record whose outcome may be parity rather than use

### Tally across 164 screened records

| cell | n |
|---|---|
| `CONTEXT_STIGMA_MEASURE` | 65 |
| `OFF_OTHER` | 28 |
| `LINK_NORM_USE` | 26 |
| `MIXED_NORM_SUPPLY` | 25 |
| `MIXED_NORM_DIFFUSION` | 10 |
| `OFF_HIV_STIGMA` | 3 |
| `MIXED_NORM_SECULAR` | 2 |
| `INSUFFICIENT_INFO` | 2 |
| `MIXED_NORM_TECH` | 1 |
| `OFF_OTHER_STIGMA` | 1 |
| `MIXED_NORM_LAW` | 1 |

## Primary cell closed (`416`, `417`)

All **8 of 8** unresolved records are now read — 2 by open access, 6 by hand through the UChicago proxy, 2 of those 6 only after OCR.

### The last two

| id | what it is | cell |
|---|---|---|
| `W1976018943` | Wolff et al., *Stud Fam Plann* 2000 — **partner opposition** and unmet need in Uganda | `LINK_NORM_USE` |
| `W2112312272` | Caldwell, *PDR* 1999 — moral and religious disapproval and the delayed Western decline | `CONTEXT_STIGMA_MEASURE` |

Wolff is the closest match to A.6's registered exposure in the whole pool: partner
opposition itself, quantified at roughly 15% of unmet need overall. Its outcome is
unmet need and method mix. **The authors name the missing study themselves** — the
question A.6 asks "would require a prospective study over time to observe the fertility
outcomes of disagreement", which they did not do and which nothing in these 164
screened records has done.

Caldwell is the only substantial **FDT** treatment of A.6's mechanism in the corpus, and
the FDT cell is otherwise empty. It argues the case historically — zero regressions, one
table — rather than estimating it.

### `PRIMARY_NORM_FERTILITY`: **0** — closed

Empty, with **every retrievable record read**. Seven channels agree:

| channel | result |
|---|---|
| identified-design share of the frame | 12 / 668 |
| realized-fertility share of the frame | 58 / 668 |
| anchor reachability, stage-2 frame | 0 / 15 |
| citation bridges | 8, none an estimate |
| exhaustive screen | 0 / 164 |
| full text of the decider | `LINK_NORM_USE` |
| full text of the remaining 7 | 0 primary |

The finding is not that the evidence is weak. It is that the study A.6 requires —
normative exposure, fertility outcome, identification — does not exist in this
literature, and two of its best papers say so in their own words: Wolff by naming
the prospective study nobody has run, Caldwell by arguing the case historically
instead of estimating it.

Per scope §12 the verdict is **UNEVALUATED with the failed route named** — R1 for
want of an identified fertility outcome, R3 for want of a pre-1985 dose series —
and explicitly not "weak evidence". `LINK_NORM_USE` stands at **27** and
is poolable as stratum 3 under a heading that disclaims it as the parameter.

### What is still open

- **5 records flagged for second read**, per the rubric's asymmetric
  rule: `W108787496` and `W2187750596` (reclassifications of the two highest-prior records), plus the batch-1 provisional calls.
- **PI call 7** — the `MIXED_NORM_MARRIAGE` rubric gap on the A.6/D.2.b boundary.
- **The sampled tail** (S5/S6/S7, 240 of 2,651 records) is unread. It bounds the
  chance the flagger misrouted a primary-cell study out of the exhaustive strata;
  that bound is not yet established.
- **OCR noise**: `416` recovered 548 and 821 words/page, ample for screening, but
  Wiley's vertical watermark interleaves with body text and two-column pages mix
  across line breaks. Cell assignments rest on abstracts, headings and table
  structure, which survived cleanly. **Any quotation from those two must be checked
  against the PDF before it reaches a chapter.**

### Tally across 164 screened records

| cell | n |
|---|---|
| `CONTEXT_STIGMA_MEASURE` | 66 |
| `OFF_OTHER` | 28 |
| `LINK_NORM_USE` | 27 |
| `MIXED_NORM_SUPPLY` | 25 |
| `MIXED_NORM_DIFFUSION` | 10 |
| `OFF_HIV_STIGMA` | 3 |
| `MIXED_NORM_SECULAR` | 2 |
| `MIXED_NORM_TECH` | 1 |
| `OFF_OTHER_STIGMA` | 1 |
| `MIXED_NORM_LAW` | 1 |

## Second read (`418`)

**This was not an independent second read.** The same reader made all five first-pass
calls, and the point of a second reader is independence. What was done is an
*adversarial self-re-read*: for each record the question was not "is my call
defensible" but "what is the strongest case that this is `PRIMARY_NORM_FERTILITY`, and
does it survive the text". It caught two errors. It cannot substitute for independence,
so `output/stigma-reduction-contraception-abortion-second-review-sheet.csv` is emitted with the first-pass cell **withheld**, for Alexandra or Anup.

| id | first pass | after second read | basis |
|---|---|---|---|
| `W108787496` | `LINK_NORM_USE` | **confirmed** | only DVs are Desired Family Size and Contraceptive Use; no table pairs a norm regressor with a fertility outcome |
| `W1976018943` | `LINK_NORM_USE` | **confirmed** | only DVs are unmet need and method mix; "number of children" appears only as a survey attitude item |
| `W2187750596` | `LINK_NORM_USE` | **confirmed** | Tables 2–6 each state Pill demand is the DV; out-of-wedlock births are the regressor |
| `W4224236986` | `MIXED_NORM_SECULAR` | **CHANGED to `LINK_NORM_USE`** | the paper decomposes religiosity and separately doses "moral opposition to birth control" on a 0–4 scale |
| `W4403613268` | `CONTEXT_STIGMA_MEASURE` | **CHANGED to `INSUFFICIENT_INFO`** | the call rested on the title; closed at Springer, no OA copy, so it cannot be resolved |

### The change that matters

`W4224236986` (McLoughlin Brooks and Weitzman, *Demography* 2022) was routed wholly to
D.1.a on the reasoning that religiosity is a value. That was too crude. The paper
decomposes religiosity, and among its separately measured mediators is **"moral
opposition to birth control" on a 0–4 scale**, with disapproval of premarital sex,
anticipated guilt after sex, and fear of being stigmatised. Wall 5 gives D.1.a *what
people value* and A.6 *what they can be seen doing at fixed values* — this paper
measures both and separates them. It is a weekly longitudinal panel with a mediation
design and it cites Bongaarts and Watkins 1996, one of A.6's four registered seminals.
It is now the **best-designed record in `LINK_NORM_USE`**, and it makes PI call 5
answerable from evidence rather than from taste.

It was also **gold open access all along** and should have been retrieved at stage 5;
`412` never fetched it because the screen had not flagged it as `INSUFFICIENT_INFO`.
That is a gap in the pipeline, not in this record: **a borderline routing call can need
full text just as much as an unresolved one**, and only the latter was queued for
retrieval.

### `PRIMARY_NORM_FERTILITY`: **0** — unchanged by the second read

`LINK_NORM_USE` rises to **28**. Unresolved returns to **1**
(`W4403613268`, closed at Springer).

### Tally across 164 screened records

| cell | n |
|---|---|
| `CONTEXT_STIGMA_MEASURE` | 65 |
| `LINK_NORM_USE` | 28 |
| `OFF_OTHER` | 28 |
| `MIXED_NORM_SUPPLY` | 25 |
| `MIXED_NORM_DIFFUSION` | 10 |
| `OFF_HIV_STIGMA` | 3 |
| `INSUFFICIENT_INFO` | 1 |
| `MIXED_NORM_TECH` | 1 |
| `OFF_OTHER_STIGMA` | 1 |
| `MIXED_NORM_SECULAR` | 1 |
| `MIXED_NORM_LAW` | 1 |
