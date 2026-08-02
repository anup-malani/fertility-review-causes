#!/usr/bin/env python3
"""
66_b1_make_screen_batches.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A5 input.

Prepare the full 4,900-candidate Tier-B frame for blinded title/abstract LLM screening. No candidate is
filtered here (keep-and-route, per the A4 audit). Records are deterministically shuffled, stripped of
all discovery/gold/identity provenance (blinding), and split into fixed-size batches. A committed
manifest records paths + SHA-256; batch payloads live in temp/ (reproducible from the committed frame).

Mirrors child-labor step 58. Rubric routes on the FROZEN B.1/A.2 boundary; the two routing decoys must
surface as route-away (Pritchett -> OFF_EXPOSURE_A2, Wilcox -> TEMPO_EXPOSURE) as the routing check.

Inputs : literature/search-logs/{slug}-tier-b-frame.json
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-screen-rubric.md
"""
import hashlib, json, random
from pathlib import Path

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
SEED = 811  # B.1
BATCH_SIZE = 40
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

RUBRIC = """# Blinded title/abstract screening rubric — evolutionary sex drive & contraceptive decoupling (B.1)

## Review question

Does the paper bear on **B.1** — the claim that human fertility is a by-product of an evolved drive for
*sex*, not for *children*, so that once contraception decouples sex from reproduction, fertility falls
**even with the preference for children held fixed**? Two things are in the primary estimand: (a) the
**decoupling / dissociation of sex from reproduction**, and (b) **fertility falling independently of any
fall in the desire for children**. Preserve the evolutionary-theory and biosocial-model stream, but
route it outside the empirical primary estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. When the abstract is missing or cannot distinguish a plausible relevant paper, use `UNCERTAIN`;
do not infer findings from author, journal, or title fragments.

## THE LOAD-BEARING BOUNDARY (B.1 vs A.2)

Most contraception papers belong to **A.2 (proximate contraceptive technology)**, NOT here.

- **A.2 asks:** given that people want fewer children, how does cheap effective contraception help them
  hit that target? Its estimand is closing the *desired–realized gap* / reducing *unwanted* births.
  Route these to `OFF_EXPOSURE_A2`.
- **B.1 asks:** why does contraception depress fertility *in the first place*? Its estimand is the
  decoupling of sex from reproduction and the *absence of an evolved positive demand for children* —
  fertility falling *without* a fall in child preference.

A paper is B.1-primary ONLY if it speaks to the decoupling/dissociation itself, OR to fertility
declining while the preference for children is held fixed or unchanged. A paper showing contraception
reduces *unwanted* births among people who already want fewer children is **A.2** → `OFF_EXPOSURE_A2`.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_DECOUPLING | PRIMARY_DESIRE_INDEPENDENCE | PROXIMATE_ULTIMATE | MOTIVATION_DISTINCTNESS | THEORY | TEMPO_EXPOSURE | OFF_EXPOSURE_A2 | OFF_OUTCOME | REVERSE | CULTURAL_NORMALIZATION | NA",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "holds_child_preference_fixed": "yes | no | unclear",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: directly studies or models the sex–reproduction decoupling, the dissociation of an
  evolutionary predictor from realized fertility once contraception is available, fertility falling with
  child-preference held fixed, or the distinctness/weakness of reproductive vs sexual motivation.
- `UNCERTAIN`: plausibly belongs, but missing/ambiguous information prevents confident routing.
- `NOT_RELEVANT`: does not bear on the decoupling or the desire-independence estimand. General
  contraception-access, fertility-decline, or evolutionary-psychology papers are NOT automatically
  relevant.

## Estimand cells

- `PRIMARY_DECOUPLING`: contraceptive access/adoption as the severing technology, or a natural test of
  the sex↔reproduction link → realized fertility dissociating from a determinant of sexual
  activity/exposure (status, mating effort, coital frequency, union).
- `PRIMARY_DESIRE_INDEPENDENCE`: contraceptive access/adoption → fertility falls holding desired family
  size / preference for children fixed.
- `PROXIMATE_ULTIMATE`: an evolutionary predictor of fertility (status, wealth, mating effort) → a
  sexual/mating outcome vs a reproductive outcome, especially pre- vs post-contraception (Pérusse-type
  dissociation test).
- `MOTIVATION_DISTINCTNESS`: evidence that reproductive motivation is a psychological construct distinct
  from, and weaker than, sexual motivation (childbearing-motivation / desire-for-children work).
- `THEORY`: evolutionary / biosocial model of the mismatch, sex drive, or absence of a child-drive, with
  no empirical fertility estimate.
- `TEMPO_EXPOSURE`: coital frequency / exposure change → fecundability or birth timing only. Route to
  A.4 (coital-frequency-biological) unless the decoupling itself is the object.
- `OFF_EXPOSURE_A2`: contraceptive availability/cost closing the desired–realized gap → unwanted births
  / realized fertility among those already wanting fewer. Route to A.2.
- `OFF_OUTCOME`: mating psychology, sexual behavior, or the status–sex link with NO fertility outcome;
  or a covered variable → a non-fertility outcome (labor, marriage, education, health). Mechanism/context
  only.
- `REVERSE`: fertility / family size → sexual behavior or contraceptive adoption.
- `CULTURAL_NORMALIZATION`: postmaterialist / normative legitimation of contraceptive use → fertility.
  Cross-ref D.1.a; not the biological estimand.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a decoupling/dissociation OR desire-independence mechanism AND a fertility (or sexual-vs-
   reproductive) outcome must be present for a PRIMARY cell.
2. A contraception→fertility study identified purely off contraceptive cost/availability, framed as
   closing a desired–realized gap, is `OFF_EXPOSURE_A2` even if it mentions evolution in passing.
3. A study of status/wealth → labor, marriage, or education (no fertility or reproductive-success
   outcome) is `OFF_OUTCOME`, even when it cites the pill/contraception as an instrument.
4. Do not promote an `OFF_OUTCOME` or `OFF_EXPOSURE_A2` paper to PRIMARY merely because decoupling or
   evolution is mentioned as motivation.
5. Reviews may be `RELEVANT` but cannot be PRIMARY; use the best non-primary cell and
   `evidence_type=review`.
6. Set `holds_child_preference_fixed=yes` only when the design actually holds desired family size /
   child preference constant; this is the clause that separates B.1 (`PRIMARY_DESIRE_INDEPENDENCE`)
   from A.2 (`OFF_EXPOSURE_A2`).
"""


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = LOGS / f"{SLUG}-tier-b-frame.json"
    records = json.loads(source.read_text())
    ids = [r.get("paperId") for r in records]
    if any(not v for v in ids) or len(ids) != len(set(ids)):
        raise SystemExit("frame must have unique, nonblank paperId values")

    shuffled = list(records)
    random.Random(SEED).shuffle(shuffled)
    (SCREEN / "RUBRIC.md").write_text(RUBRIC)
    manifest, assigned = [], []
    for start in range(0, len(shuffled), BATCH_SIZE):
        number = start // BATCH_SIZE + 1
        batch = []
        for row in shuffled[start:start + BATCH_SIZE]:
            batch.append({
                "paperId": row["paperId"],
                "title": row.get("title") or "",
                "year": row.get("year"),
                "abstract": (row.get("abstract") or "")[:3500],
            })
            assigned.append(row["paperId"])
        ip = SCREEN / f"batch_{number:03d}.json"
        ip.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
        manifest.append({"batch": number, "n": len(batch),
                         "input": str(ip.relative_to(REPO)), "input_sha256": sha256(ip),
                         "output": str((SCREEN / f"verdict_{number:03d}.json").relative_to(REPO))})
    if len(assigned) != len(records) or set(assigned) != set(ids):
        raise SystemExit("batch coverage invariant failed")

    committed = {"slug": SLUG, "stage": "blinded_title_abstract_screen_input",
                 "source": str(source.relative_to(REPO)), "source_sha256": sha256(source),
                 "seed": SEED, "batch_size": BATCH_SIZE, "records": len(records), "batches": len(manifest),
                 "records_with_abstract": sum(bool((r.get("abstract") or "").strip()) for r in records),
                 "blinded_fields": ["doi", "authors", "venue", "cited_by_count",
                                    "discovery_channels", "seed_ids", "gold_status"],
                 "coverage_verified": True, "manifest": manifest}
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(json.dumps(committed, indent=2, ensure_ascii=False))
    (LOGS / f"{SLUG}-screen-rubric.md").write_text(RUBRIC)
    print(f"{len(records)} records -> {len(manifest)} blinded batches of <= {BATCH_SIZE}; "
          f"abstracts {committed['records_with_abstract']}; coverage verified")


if __name__ == "__main__":
    main()
