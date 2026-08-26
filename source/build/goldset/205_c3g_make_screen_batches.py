#!/usr/bin/env python3
"""
205_c3g_make_screen_batches.py — C.3.g, stage D2. Prepare the semantic screen.

Writes the screening rubric and cuts the D1 worklist into fixed batches carrying only what a
title/abstract screen is entitled to see: title, venue, year, type, and a truncated abstract.

WITHHELD FROM THE SCREENING RECORD, deliberately:
  * the D1 score and rank — a screener who can see the blind sieve's output anchors on it, which
    collapses two independent sieves into one;
  * the `worklist_reason`. A record told "this arrived through the P2 bypass" invites a screener to
    read a policy design into an abstract that states none. The bypass is a retrieval decision;
    whether the record carries the design is what the screen is being asked;
  * every D1 hit list, so `arm`, `outcome` and `design` are INDEPENDENT readings that assembly can
    cross-check against the term matches rather than merely reproduce.

`arm` IS THE FIELD THIS SCREEN EXISTS FOR. C.3.g's evidence splits into a DIRECT arm (a young
adult's own education debt against a fertility outcome — the registered estimand, and the only thing
GRADE attaches to) and a CHAIN arm (the same exposure against marriage, homeownership or residential
independence — link 1 of the mechanism v5's claim names, whose link 2 belongs to A.7, A.23 and
C.2.c). They must never be pooled. A4 measured the routing as 77% single-outcome-axis within the
frame, so this split IS largely screenable — unlike A.17's, which was decided in methods sections.
`cannot_tell` stays a first-class value: its SHARE is the measurement that decides how much routing
has to move to full text.

`attain_conditioned` IS AN INDEPENDENT RE-READ OF THE CHAPTER'S CENTRAL CONFOUND. Debt is chosen
jointly with schooling and schooling independently lowers fertility, so a study comparing borrowers
to non-borrowers without holding attainment fixed estimates the return to college, not the burden of
financing it. The scope declared this invisible at title/abstract from 8 query-level records; A4
measured it at 28% of in-frame records and the scope was revised to call it a screen FLAG with the
gate still at full text. Having the screener judge it independently is what turns a term count into
a routing decision — and the disagreements are the working set, not errors.

THE NO-ABSTRACT BUCKET IS NOT A NEGATIVE VERDICT. A screener who returns NOT_RELEVANT on a
title-only record has recorded "not visible" as "not relevant" — the refusals-read-as-zeros failure
in another costume. Those records take `info: insufficient` and `UNCERTAIN` unless the TITLE ALONE
is decisive, and a title often is in both directions. This is not hypothetical here: the chapter's
most-cited primary-cell anchor, Nau et al. 2015, has no indexed abstract, and so does the SSRN
preprint that overturned the scope's central finding.

Output: source/build/goldset/c3g_screen_batches/batch_NN.json
        literature/search-logs/{slug}-screen-rubric.md
"""
import json, os, math

SLUG = "student-debt-household-formation"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(ROOT, "literature", "search-logs")
RANKED = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
BATCH_DIR = os.path.join(HERE, "c3g_screen_batches")
RUBRIC = os.path.join(LOGS, f"{SLUG}-screen-rubric.md")
BATCH_SIZE = 55
ABSTRACT_CHARS = 900

RUBRIC_TEXT = """# Title/abstract screening rubric — C.3.g student debt and household formation

**Hypothesis (HYPOTHESES-v5 §C.3.g):** education debt service during prime childbearing years
reduces the household resources available for family formation — delaying or blocking marriage,
homeownership, and childbearing — in cohorts that came of age under the post-2000 student-debt
regime. Target phenomenon: **SDT only**.

You see title, venue, year, type and a truncated abstract. You do NOT see the deterministic score,
the rank, or why the record reached the worklist. That is deliberate: your reading and the term
matches must stay independent so assembly can cross-check them.

Return one JSON object per record, with these fields.

## `verdict` — RELEVANT | UNCERTAIN | NOT_RELEVANT

- **RELEVANT** — reports an empirical relationship between a young adult's OWN education debt and
  fertility, union formation, or housing/residential independence. Include studies whose estimate is
  associational; identification is recorded separately, not required.
- **UNCERTAIN** — plausibly in scope but the abstract does not settle it, OR the record is
  title-only and the title is not decisive.
- **NOT_RELEVANT** — a different exposure, a different outcome, or no empirical relationship at all.

## `exposure` — own_student_debt | parent_held_debt | general_debt | tuition_or_aid_policy | none | cannot_tell

Whose balance sheet the debt sits on is the chapter's sharpest boundary. `parent_held_debt` (Parent
PLUS, borrowing for a child's degree) sits on the older generation and cannot delay the borrower's
own childbearing. `general_debt` is credit-card, mortgage, medical or consumer debt — that is C.3.e
and C.2.c, not this chapter.

## `outcome` — fertility | union_formation | housing_residence | multiple | other | none

`fertility` = births, first birth, completed fertility, childlessness, fertility intentions.
`multiple` = more than one of the three in the estimated outcomes, which is the case that cannot be
routed at screen.

## `arm` — direct | chain | mechanism | off | cannot_tell

- **direct** = own education debt → a FERTILITY outcome. The registered estimand.
- **chain** = own education debt → marriage, homeownership or residential independence. In scope
  because v5's claim names these as the mechanism, but a DIFFERENT proposition.
- **mechanism** = debt → earnings, savings, occupational choice, liquidity. Evidence about the
  resource channel itself; not evidence for a fertility effect.
- **off** = neither.

## `design` — identified | associational | descriptive | qualitative | review | simulation | cannot_tell

`identified` requires a named strategy the abstract states: an experiment, DiD, IV, RD, event study,
policy discontinuity. **The most important record in this frame is titled "Experimental Evidence
on ... Responses to Student Debt Forgiveness"** — a design list that cannot see it is useless.

## `attain_conditioned` — yes | no | cannot_tell

Does the study hold educational ATTAINMENT fixed (compare borrowers to non-borrowers with the same
degree), or does it compare people with different amounts of schooling? Expect `cannot_tell` often;
that is information, not failure.

## `wall` — none | w1_career | w2_general_debt | w3_repayment | w4_access_to_college | w5_6_parent_balance | w7_lmic | w8_reverse

- `w1_career` — health-professions debt studied for SPECIALTY or CAREER choice. **Route by outcome,
  not by topic:** a study of medical students that reports childbearing decisions is IN, and takes
  `wall: none`. Only the ones whose estimated quantity is a career, a specialty or a practice
  location are walled.
- `w7_lmic` — school fees and child marriage in low-income settings. Different exposure, different
  outcome, different phenomenon. Tag it; it is never deleted.
- `w8_reverse` — childbearing as a CAUSE of debt (student parents borrowing more).

## `info` — sufficient | insufficient

`insufficient` whenever the record is title-only and the title is not decisive, or the abstract is
too vague to answer the fields above. **A title-only record is not a negative verdict.** Returning
NOT_RELEVANT because you could not see the abstract records "not visible" as "not relevant".

## `note` — one short clause, only when the record is a boundary case worth an RA's eye

Output format, one line per record:

```json
{"id": "W1234567890", "verdict": "RELEVANT", "exposure": "own_student_debt", "outcome": "fertility",
 "arm": "direct", "design": "associational", "attain_conditioned": "cannot_tell", "wall": "none",
 "info": "sufficient", "note": ""}
```
"""


def main():
    recs = json.load(open(RANKED))
    work = [r for r in recs if r.get("in_worklist")]
    os.makedirs(BATCH_DIR, exist_ok=True)
    for f in os.listdir(BATCH_DIR):
        if f.startswith("batch_") and f.endswith(".json"):
            os.remove(os.path.join(BATCH_DIR, f))

    n = math.ceil(len(work) / BATCH_SIZE)
    for i in range(n):
        chunk = work[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        out = [dict(id=r["id"], title=r["title"], year=r.get("year"), type=r.get("type"),
                    venue=(r.get("venue") or "")[:60],
                    abstract=(r.get("abstract") or "")[:ABSTRACT_CHARS])
               for r in chunk]
        p = os.path.join(BATCH_DIR, f"batch_{i + 1:02d}.json")
        json.dump(out, open(p, "w"), indent=1)
    open(RUBRIC, "w").write(RUBRIC_TEXT)
    n_abs = sum(1 for r in work if r.get("has_abstract"))
    print(f"{len(work)} worklist records -> {n} batches of <= {BATCH_SIZE} in "
          f"{os.path.relpath(BATCH_DIR, ROOT)}")
    print(f"  {n_abs} with abstract, {len(work) - n_abs} title-only "
          f"({(len(work) - n_abs) / max(len(work), 1):.0%})")
    print(f"-> {os.path.relpath(RUBRIC, ROOT)}")


if __name__ == "__main__":
    main()
