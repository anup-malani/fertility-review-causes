#!/usr/bin/env python3
"""255 — A.18 title/abstract screen: rubric and batches. TICK-076.

Cuts the prescreen survivors into fixed batches carrying only what a title/abstract
screen is entitled to see, and writes the rubric the screener works from.

**Priority strata**, because the frame cannot be screened whole (29,394 survivors)
and §17 bounded what that leaves unread:

  A  CITATION_INTERSECT  survivors the snowball pool also reached. Highest prior.
  B  RELEVANCE_HEAD      the boolean relevance ordering's head, which the §16 curve
                         shows carries gold at many times the uniform rate.
  C  TAIL                everything else — NOT batched. §17 bounds it at ~213
                         relevant records (95% CI 37–1,176) by blinded sample.

WITHHELD FROM THE SCREENING RECORD, deliberately:
  * anchor / gold status. A screener who can see a record is gold will not reject
    it, and the point of knowing the gold was to audit the screen afterwards.
  * pool membership and stratum. Reaching a record twice says something about the
    channels and nothing about the record.
  * relevance rank. It would license "it ranked low, so it is probably noise".

`decomposes` IS THE FIELD THIS SCREEN EXISTS FOR. Wall 1 is what decides whether
this chapter has a primary pool: a parent–child fertility correlation is A.19's and
is NOT evidence for A.18, because it is equally consistent with pure social
transmission. Only a design that ATTRIBUTES variance to genotype counts. §15's
recall audit found 13 of 37 gold-set misses were exactly this error, so it will be
present at scale here.

`exposure_distance` is the A.24 lesson carried forward: on present reading this
literature is EDUCATION_PGS-heavy while the registered exposure is fertility-
associated genotype. That distribution must be visible in a table, not discovered
at synthesis.

THE NO-ABSTRACT BUCKET IS NOT A NEGATIVE VERDICT. A screener returning
NOT_RELEVANT on a title-only record has recorded "not visible" as "not present".
Those take info=insufficient and UNCERTAIN unless the TITLE ALONE is decisive —
and a title often is, in both directions.

Usage: python3 source/build/goldset/255_a18_make_screen_batches.py [--head N] [--size N]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
BATCHDIR = TEMP / "a18_screen_batches"
RUBRIC = LOGS / "heritability-fertility-genetic-screen-rubric.md"
MANIFEST = LOGS / "heritability-fertility-genetic-screen-manifest.json"

HEAD = int(sys.argv[sys.argv.index("--head") + 1]) if "--head" in sys.argv else 2000
SIZE = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 55

RUBRIC_TEXT = """# A.18 title/abstract screen rubric

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
"""


def main():
    BATCHDIR.mkdir(parents=True, exist_ok=True)
    for f in BATCHDIR.glob("batch_*.json"):
        f.unlink()

    frame = {r["openalex"]: r for r in
             json.loads((TEMP / "heritability-fertility-genetic-frame-deduped.json").read_text())["records"]}
    surv = set(json.loads((LOGS / "heritability-fertility-genetic-prescreen.json").read_text())["survivor_ids"])
    pool = {r["openalex"] for r in
            json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())}

    A = [frame[i] for i in surv if i in pool]
    rest = sorted((r for r in (frame[i] for i in surv) if r["openalex"] not in pool),
                  key=lambda r: r.get("rank") or 10**9)
    B = rest[:HEAD]

    for r in A:
        r["_stratum"] = "A"
    for r in B:
        r["_stratum"] = "B"
    todo = A + B

    batches = []
    for i in range(0, len(todo), SIZE):
        chunk = todo[i:i + SIZE]
        n = i // SIZE + 1
        recs = [{"ref": f"B{n:02d}-{j:02d}",
                 "openalex": r["openalex"],
                 "title": r.get("title"), "venue": r.get("venue"),
                 "year": r.get("year"), "type": r.get("type"),
                 "abstract": (r.get("abstract") or "")[:1100] or None}
                for j, r in enumerate(chunk, 1)]
        (BATCHDIR / f"batch_{n:02d}.json").write_text(json.dumps(
            {"batch": n, "of": (len(todo) + SIZE - 1) // SIZE,
             "slug": "heritability-fertility-genetic", "ticket": "TICK-076",
             "rubric": "literature/search-logs/heritability-fertility-genetic-screen-rubric.md",
             "records": recs}, indent=1))
        batches.append({"batch": n, "n": len(recs),
                        "strata": {"A": sum(1 for r in chunk if r["_stratum"] == "A"),
                                   "B": sum(1 for r in chunk if r["_stratum"] == "B")}})

    RUBRIC.write_text(RUBRIC_TEXT)
    MANIFEST.write_text(json.dumps({
        "ticket": "TICK-076",
        "survivors": len(surv),
        "stratum_A_citation_intersect": len(A),
        "stratum_B_relevance_head": len(B),
        "stratum_C_tail_not_batched": len(surv) - len(A) - len(B),
        "batch_size": SIZE, "batches": len(batches),
        "blinding": "gold/anchor status, pool membership, stratum and relevance rank withheld",
        "batch_index": batches}, indent=1))
    print(f"survivors {len(surv):,}")
    print(f"  stratum A (citation intersect): {len(A):,}")
    print(f"  stratum B (relevance head):     {len(B):,}")
    print(f"  stratum C (tail, NOT batched):  {len(surv)-len(A)-len(B):,}  — bounded by §17")
    print(f"\n{len(batches)} batches of {SIZE} in {BATCHDIR}")
    print(f"rubric: {RUBRIC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
