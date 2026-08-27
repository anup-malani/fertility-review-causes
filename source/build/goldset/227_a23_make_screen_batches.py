#!/usr/bin/env python3
"""
227 — A.23 title/abstract screen: rubric and batches.

TICK-075. Cuts the 1,572-record frame into fixed batches carrying only what a
title/abstract screen is entitled to see -- title, venue, year, type, language and
a truncated abstract -- and writes the rubric the screener works from.

WITHHELD FROM THE SCREENING RECORD, deliberately:
  * whether a record is a gated ANCHOR, and whether it is gold. A screener who can
    see that a record is gold will not reject it, and the whole point of marking
    gold in the frame was to audit the screen against it afterwards. Showing it
    destroys the audit.
  * whether a record was HAND-ADDED (the two from 226). A record told "the query
    missed this one and we put it in on purpose" invites a screener to find it
    relevant.
  * whether the record is also in the snowball pool. Reaching a record twice says
    something about the channels, nothing about the record.

`exposure_is_arrangement` IS THE FIELD THIS SCREEN EXISTS FOR. The calibration in
222/223 found that 8 of 19 gold candidates -- every one of the pension-reform
"identified designs" -- carried no living-arrangement exposure at all. Their
treatment is the grandmother's time, which is C.2.a's variation. If that error
survived a hand-built anchor set, it will certainly be present at scale in a
1,572-record frame, and it is the single most consequential routing judgement here.

`config` IS THE RULING-1 SPLIT, and it is expected to be hard. The scope's §6
established that pre-launch and extended-household co-residence are separated by
WHO DEPENDS ON WHOM at WHAT LIFE STAGE, which is often a sample-restriction or
table-of-descriptives fact rather than an abstract one. `cannot_tell` is therefore
a first-class value and its SHARE is a measurement: it decides how much of the
routing has to move to the RA gate and to full text. Do not guess to avoid it.

THE NO-ABSTRACT BUCKET IS NOT A NEGATIVE VERDICT. 240 of the 1,572 records (15.3%)
have no indexed abstract. A screener returning NOT_RELEVANT on a title-only record
has recorded "not visible" as "not relevant". Those take `info: insufficient` and
`UNCERTAIN` unless the TITLE ALONE is decisive -- and a title often is, in both
directions.

Output: source/build/goldset/a23_screen_batches/batch_NN.json
        literature/search-logs/{slug}-screen-rubric.md
"""
import json
import math
from pathlib import Path

SLUG = "co-residence-parents-household-delay"
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LOGS = ROOT / "literature" / "search-logs"
FRAME = LOGS / f"{SLUG}-frame.json"
BATCH_DIR = HERE / "a23_screen_batches"
RUBRIC = LOGS / f"{SLUG}-screen-rubric.md"
BATCH_SIZE = 55
ABSTRACT_CHARS = 900

RUBRIC_TEXT = """# Title/abstract screening rubric — A.23 co-residence and delayed household formation

**Hypothesis (HYPOTHESES-v5 §A.23):** extended co-residence of young adults with parents delays or
prevents fertility by blocking independent household formation — privacy, sexual autonomy, and the
sense of being an adult with a household of one's own. **Target phenomenon: SDT.**

**Ruling 1 (2026-08-27) widens this.** A.23 owns variation in the living arrangement in *both* of its
configurations, which have opposite predicted signs:

- **PRE_LAUNCH** — an unpartnered, childless young adult living in the parental home. Predicted sign
  on fertility: **negative**. This is the configuration the registered claim describes.
- **EXTENDED_COUPLE** — a couple, usually already partnered, living with a parent or parent-in-law,
  where the parent supplies childcare and household labour. Predicted sign: **positive**. This is the
  modal configuration in the East Asian literature.

They share a phrase and nothing else, and they are never pooled.

You see title, venue, year, type, language and a truncated abstract. You do **not** see whether the
record is an anchor, whether it is gold, whether it was hand-added, or whether the snowball pool also
reached it. That is deliberate: the frame marks gold so the screen can be audited against it
afterwards, and a screener who can see the marking destroys the audit.

Return one JSON object per record with the fields below.

## `exposure_is_arrangement` — yes | no | cannot_tell

**The field this screen exists for.** Does the record's *exposure* — the thing that varies, the
treatment, the independent variable — involve the LIVING ARRANGEMENT: who lives with whom?

Say **no** when the exposure is something else, even when the paper is about parents and children and
fertility. The commonest case, and the one that has already produced a real error in this chapter's
own anchor set:

> A pension reform delays a grandmother's retirement, so she provides less childcare, so her
> daughter has fewer children. **The exposure is the grandmother's TIME, not the living
> arrangement.** Nobody moved house. That is C.2.a's variation (childcare availability), and the
> record routes to `OFF_CHILDCARE_C2a`.

Eight of nineteen hand-selected gold candidates failed exactly this test. Expect it at scale. The
question is not "is this paper about families" — it is "does the arrangement VARY".

Say **no** also when the arrangement is only a control variable, a sample description, or a phrase in
the motivation, with something else being estimated.

## `config` — PRE_LAUNCH | EXTENDED_COUPLE | ELDER_SUPPORT | PROXIMITY | UNSPLIT | cannot_tell

Which configuration of the arrangement is being studied.

- `ELDER_SUPPORT` — an adult child housing a *dependent elderly* parent. Different construct,
  dependency runs the other way; routes out. Do not use the words "elderly" or "ageing" alone to
  decide this: a couple living with a healthy 62-year-old who minds the baby is `EXTENDED_COUPLE`,
  and the same household ten years later is `ELDER_SUPPORT`.
- `PROXIMITY` — living *near* parents without co-residing. Different treatment, pooled separately.
- `UNSPLIT` — the study genuinely pools configurations.
- `cannot_tell` — **a first-class answer, not a failure.** The distinguishing facts are often in a
  sample restriction or a descriptives table. Its share across the frame is a measurement this
  chapter needs. Do not guess to avoid it.

## `outcome` — fertility | union_only | arrangement_only | labour_supply | other | cannot_tell

- `fertility` — births, parity progression, completed fertility, childlessness, fertility intentions.
- `union_only` — marriage, cohabitation, partnership formation, and no birth outcome. This is link 1
  of the chain and is real evidence about it, but it is not a fertility estimate.
- `arrangement_only` — the outcome IS the living arrangement (who leaves home, when). Link 1's other
  half; establishes the exposure trend.
- `labour_supply` — maternal employment, hours, wages. **Expected to be the largest single route-out**:
  the extended-household literature's own estimand is usually the mother's job, with fertility
  secondary or absent. Routes to `OFF_OUTCOME_LABOUR_SUPPLY`, cross-ref C.2.e.

## `design` — identified | observational | descriptive | theory | cannot_tell

`identified` means an explicit source of exogenous variation: a policy discontinuity, an instrument,
a natural experiment, a difference-in-differences. **Controls are not identification**, and neither
is a longitudinal design on its own. When in doubt, `observational`.

## `anticipation_flag` — yes | no | cannot_tell

Does the record appear to address the chapter's central threat: that leaving home, forming a union
and having a first child are ordered jointly, so people move out *in order to* have a child? A design
using pre-determined arrangement, an instrument, or an event-history with time-varying covariates
gets `yes`. Silence gets `no`. This is a flag, not a gate; the gate is at full text.

## `route` — the estimand cell

One of: `PRIMARY_PRELAUNCH`, `PRIMARY_EXTENDED_COUPLE`, `PRIMARY_PROXIMITY`,
`LINK1_ARRANGEMENT_TO_UNION`, `LINK1_DRIVER_TO_ARRANGEMENT`, `MIXED_PRICE_ARRANGEMENT`,
`AGGREGATE_UNSPLIT`, `OFF_OUTCOME_LABOUR_SUPPLY`, `ELDER_SUPPORT`, `OFF_PRICE_C2c`,
`OFF_UNION_TIMING_A7`, `OFF_NORMS_D2b`, `OFF_UNCERTAINTY_C5a`, `OFF_DEBT_C3g`, `OFF_CHILDCARE_C2a`,
`OFF_OUTCOME`, `THEORY`, `REVERSE`, `INSUFFICIENT_INFO`.

## `verdict` — RELEVANT | UNCERTAIN | NOT_RELEVANT

`RELEVANT` requires `exposure_is_arrangement: yes` **and** a fertility outcome. Everything else that
is on-topic but off-cell is `UNCERTAIN` with a route, not `NOT_RELEVANT`. Reserve `NOT_RELEVANT` for
records that are not about this subject at all.

## `info` — sufficient | insufficient

`insufficient` whenever there is no abstract and the title is not decisive, or the abstract is present
but silent on the fields above. `insufficient` pairs with `UNCERTAIN`, never with `NOT_RELEVANT`.

## `note` — one sentence

What decided it. If you routed the record out, name the exposure you think it actually has.
"""


def main():
    doc = json.loads(FRAME.read_text())
    records = doc["records"]
    BATCH_DIR.mkdir(exist_ok=True)
    for old in BATCH_DIR.glob("batch_*.json"):
        old.unlink()

    # Stable order that does not encode any withheld signal: year then openalex id.
    records = sorted(records, key=lambda r: (r["year"] or 0, r["openalex"]))

    n = math.ceil(len(records) / BATCH_SIZE)
    no_abs = 0
    for i in range(n):
        chunk = records[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        out = []
        for r in chunk:
            abs_text = r.get("abstract")
            if not abs_text:
                no_abs += 1
            out.append({
                "openalex": r["openalex"],
                "doi": r["doi"],
                "title": r["title"],
                "venue": r["venue"],
                "year": r["year"],
                "type": r["type"],
                "language": r["language"],
                "abstract": (abs_text[:ABSTRACT_CHARS] + "…")
                            if abs_text and len(abs_text) > ABSTRACT_CHARS else abs_text,
                "abstract_present": bool(abs_text),
            })
        (BATCH_DIR / f"batch_{i + 1:02d}.json").write_text(json.dumps(
            {"batch": i + 1, "of": n, "slug": SLUG, "ticket": "TICK-075",
             "rubric": f"literature/search-logs/{SLUG}-screen-rubric.md",
             "records": out}, indent=1))

    RUBRIC.write_text(RUBRIC_TEXT)
    print(f"frame {len(records)} records -> {n} batches of {BATCH_SIZE}")
    print(f"  records with no abstract: {no_abs} ({round(100 * no_abs / len(records), 1)}%)")
    print(f"  batches: {BATCH_DIR.relative_to(ROOT)}")
    print(f"  rubric:  {RUBRIC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
