#!/usr/bin/env python3
"""
Step 39a - Build the Tier-B estimand-tag SPOT AUDIT sample (hardens the residual on PI critique #1).

The 247 Tier-B estimand tags that underpin the estimand-filtered Recall(B) = 82.5% were assigned by the
calibrated automated gate (step 36a), not individually RA-signed. The canonical workflow (§7, move 3)
flags this: "the Tier-B tags are automated, not RA-signed - a spot audit of the theory routing would
harden the 82.5%." This step draws the audit set and emits BLIND second-reader batches (double-screening,
the Cochrane standard): a fresh reader re-tags with the same rubric, blind to the automated cell, then
disagreements are adjudicated (39b).

Design choice - CENSUS the adjudicable stratum, SAMPLE the rest:
  - All 99 abstract-bearing Tier-B papers are audited (no sampling noise where a real re-read is possible).
  - A fixed-seed random 30 of the 148 title-only papers characterizes the title-only ceiling (where both
    the auto-tagger and the auditor are inferring the estimand from a title, so agreement measures tagger
    consistency, not ground-truth correctness).
The audit is deliberately weighted toward THEORY and PRIMARY, the two cells the 82.5% turns on.

Inputs
  temp/tierb-estimand/input.json                 247 records (id,title,year,screen_reason,abstract,has_abstract)
  source/build/goldset/estimand_tierb_tags.json  the automated tags (the answer key, held back from readers)
Outputs (temp/tierb-audit/)
  sample.json     the audited ids + stratum + held-back auto tag (answer key, NOT shown to readers)
  PROMPT.md       the blind re-tag rubric (same cells as 36a)
  batch-*.json    blind reader input (id,title,year,screen_reason,abstract) - NO auto cell
"""
import json, random, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
INP = REPO / "temp" / "tierb-estimand" / "input.json"
TAGS = HERE / "estimand_tierb_tags.json"
OUT = REPO / "temp" / "tierb-audit"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260707
N_TITLE_ONLY = 30
BATCH = 22

# Same rubric as 36a (verbatim cells) so auto and audit are commensurable; only the framing changes to
# "you are a second, independent reader" and the answer is not shown.
PROMPT = """# Independent re-tag (spot audit) - Tier B, old-age-security -> fertility chapter

You are a SECOND, INDEPENDENT reader. Each paper was already screened as topically relevant to pensions/
old-age security and fertility and was assigned an estimand cell by an automated tagger. You do NOT see
that assignment. Re-tag each paper from scratch by the causal estimand it identifies.

**Primary cell** = the causal effect of the **old-age-security motive** (pensions / social security /
children-as-old-age-support) **ON fertility**: fertility is the OUTCOME, direction is forward
(cause -> fertility), mechanism is old-age-security crowd-out of the demand for children.

For each paper extract `outcome`, `direction` (forward | reverse | fertility-as-cause), `mechanism`,
then assign exactly one `cell`:
- `PRIMARY` -- empirical study of OAS motive -> fertility (forward, fertility is the outcome).
- `THEORY` -- a formal/theoretical model, simulation, or pure literature review with NO empirical
  estimation of the effect (even if it is exactly about pensions and fertility). Routes to the theory
  stream, not the pooling set.
- `OFF:outcome-not-fertility` -- fertility is NOT the outcome (schooling, parental survival, labor
  supply, savings, migration, health, birth weight, coresidence, ...).
- `OFF:different-channel` -- pension/retirement affects fertility, but through a channel OTHER than OAS
  crowd-out -- classically grandparental childcare (raises daughters' fertility: opposite sign).
- `OFF:fertility-as-cause` -- fertility is the treatment / right-hand-side variable, not the outcome.
- `OFF:reverse-direction` -- estimates the effect of children/fertility ON old-age support, pension
  take-up, or savings.
- `OFF:different-cause` -- the treatment is NOT old-age security/pensions (child-grant subsidy, lottery
  income, female employment, kindergarten supply, welfare family cap, minimum-marriage-age, ...).
- `OFF:off-topic` -- not about old-age security at all.

Many records are TITLE-ONLY (no abstract). Judge on the title and the short screen_reason; set
`confidence` to "HIGH" (abstract or an unambiguous title), "MED", or "LOW" (title underdetermines the
estimand). Be explicit rather than guessing PRIMARY: if a title only says the topic is pensions and
fertility but does not reveal whether it is empirical vs a model, or the direction, prefer THEORY or a
LOW-confidence best guess and say why.

Return a JSON array, one object per input id, preserving every id:
[{"id":"<id>","outcome":"<...>","direction":"forward|reverse|fertility-as-cause",
  "mechanism":"<short>","cell":"PRIMARY|THEORY|OFF:...","confidence":"HIGH|MED|LOW",
  "reason":"<=160 chars"}]
Output ONLY the JSON array.
"""


def main():
    inp = {r["id"]: r for r in json.load(open(INP))}
    tags = {t["id"]: t for t in json.load(open(TAGS))}

    abs_ids = [i for i, r in inp.items() if r["has_abstract"]]
    tit_ids = [i for i, r in inp.items() if not r["has_abstract"]]
    rnd = random.Random(SEED)
    tit_sample = rnd.sample(sorted(tit_ids), N_TITLE_ONLY)
    audited = sorted(abs_ids) + sorted(tit_sample)

    sample = []
    for i in audited:
        r, t = inp[i], tags[i]
        sample.append({
            "id": i, "title": r["title"], "year": r["year"],
            "screen_reason": r["screen_reason"], "has_abstract": r["has_abstract"],
            "stratum": ("THEORY" if t["cell"] == "THEORY" else "PRIMARY" if t["cell"] == "PRIMARY" else "OFF")
                       + ("/abs" if r["has_abstract"] else "/title"),
            "auto_cell": t["cell"], "auto_conf": t.get("confidence"),  # answer key - held back from readers
        })
    json.dump(sample, open(OUT / "sample.json", "w"), indent=2)
    (OUT / "PROMPT.md").write_text(PROMPT)

    # Blind reader batches: NO auto_cell / stratum / auto_conf.
    blind = [{"id": r["id"], "title": inp[r["id"]]["title"], "year": inp[r["id"]]["year"],
              "screen_reason": inp[r["id"]]["screen_reason"], "abstract": inp[r["id"]]["abstract"]}
             for r in sample]
    nb = math.ceil(len(blind) / BATCH)
    for b in range(nb):
        json.dump(blind[b*BATCH:(b+1)*BATCH], open(OUT / f"batch-{b+1}.json", "w"), indent=2)

    from collections import Counter
    strata = Counter(r["stratum"] for r in sample)
    print(f"audited {len(sample)} of 247: all {len(abs_ids)} abstract + {N_TITLE_ONLY} of {len(tit_ids)} title-only")
    for k in sorted(strata):
        print(f"  {k:16s} {strata[k]}")
    print(f"-> {nb} blind batches of <= {BATCH} in {OUT}")


if __name__ == "__main__":
    main()
