#!/usr/bin/env python3
"""
Step 36a - Build the estimand-tagging input for the 247-paper Tier B (the recall denominator).

Point 1's last piece: re-grade Recall(B) against an ESTIMAND-FILTERED Tier B rather than the topical
one. That needs an estimand cell for every Tier-B paper. This step builds the tagging input; a Sonnet
fleet applies the same rubric as the gate calibration (step 35), extended with a THEORY cell because
Tier B -- unlike the reviewed empirical output -- contains formal models and reviews that carry no
empirical estimand and route to the theory stream, not the pooling set.

Honesty constraint carried from the start: only 99 of 247 Tier-B papers have an abstract (the rest are
dead-WID / no-DOI title-only records -- the identifiability ceiling the pilot hit). Title-only estimand
tags are less reliable, so each record carries `has_abstract`, the tagger emits a `confidence`, and the
re-grade (36b) reports a sensitivity band over the low-confidence/title-only tags rather than a single
point number.

Inputs
  {slug}-tier-b-screened.json    the 247 Tier-B gold papers (paperId, title, screen_reason, ...)
  {slug}-oa-enrichment.json      abstracts by paperId (99/247)
Outputs (temp/tierb-estimand/)
  input.json, PROMPT.md, batch-*.json
"""
import json, math
from pathlib import Path

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SL = REPO / "literature" / "search-logs" / f"{SLUG}-"
OUT = REPO / "temp" / "tierb-estimand"
OUT.mkdir(parents=True, exist_ok=True)
BATCH = 42

PROMPT = """# Estimand-and-mechanism tagging for Tier B (old-age-security -> fertility chapter)

Tag each paper by the causal estimand it identifies. These papers are already screened as topically
relevant to pensions/old-age security and fertility; your job is to say WHICH estimand each one carries,
so recall can be measured against the papers that identify THIS chapter's effect.

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
    tb = json.load(open(f"{SL}tier-b-screened.json"))
    enrich = json.load(open(f"{SL}oa-enrichment.json"))

    recs = []
    for t in tb:
        pid = t.get("paperId")
        abstract = enrich.get(pid, {}).get("abstract") if pid else None
        recs.append({
            "id": pid or t.get("doi") or t.get("title"),
            "title": t.get("title"), "year": t.get("year"),
            "screen_reason": t.get("screen_reason"),
            "abstract": abstract, "has_abstract": bool(abstract),
        })

    json.dump(recs, open(OUT / "input.json", "w"), indent=2)
    (OUT / "PROMPT.md").write_text(PROMPT)
    nb = math.ceil(len(recs) / BATCH)
    for i in range(nb):
        json.dump(recs[i*BATCH:(i+1)*BATCH], open(OUT / f"batch-{i+1}.json", "w"), indent=2)

    tl = sum(1 for r in recs if not r["has_abstract"])
    print(f"{len(recs)} Tier-B papers -> {nb} batches of <= {BATCH} ({tl} title-only)")
    print(f"tagging dir: {OUT}")


if __name__ == "__main__":
    main()
