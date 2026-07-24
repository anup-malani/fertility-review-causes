#!/usr/bin/env python3
"""
75_d3b_make_screen_batches.py — D.3.b (climate anxiety / eco-doomerism), stage A5 input.

Prepare the full 1,170-candidate Tier-B frame for blinded title/abstract LLM screening. No candidate is
filtered here (keep-and-route): pruning the frame by vocabulary distance from the future production
query would bias Recall(B). Records are deterministically shuffled, stripped of all discovery/gold/
identity provenance (blinding), and split into fixed-size batches. A committed manifest records paths +
SHA-256; batch payloads live in temp/ (reproducible from the committed frame).

Direct mirror of B.1 step 66. Only SLUG, SEED, and the rubric (cell taxonomy + the three frozen D.3.b
boundary walls + the mandatory outcome-level tag) differ. The four routing decoys must surface as
route-away — Lesthaeghe 2010 -> OFF_POSTMATERIALIST_D1a, Adsera 2011 -> OFF_ECON_C5a, the physical
climate-shock paper and the biological repro-health SR -> NOT_RELEVANT/NA — as the routing check.

Inputs : literature/search-logs/{slug}-tier-b-frame.json
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-screen-rubric.md
"""
import hashlib, json, random
from pathlib import Path

SLUG = "climate-anxiety-eco-doomerism"
SEED = 733  # D.3.b
BATCH_SIZE = 40
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

RUBRIC = """# Blinded title/abstract screening rubric — climate anxiety & eco-doomerism (D.3.b)

## Review question

Does the paper bear on **D.3.b** — the claim that fear about the ecological future *suppresses* childbearing,
so that fertility falls **without a fall in the desire for children**? The distinctive D.3.b mechanism is
affective: dread about planetary habitability, or an ethical objection to the emissions an additional child
would add, acting on a desire for children that may itself still be positive. Preserve the anti-natalist /
eco-ethics philosophical stream and the climate-anxiety psychometric stream, but route them outside the
empirical primary estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally hidden.
When the abstract is missing or cannot distinguish a plausible relevant paper, use `UNCERTAIN`; do not
infer findings from author, journal, or title fragments.

Phenomenon scope is **SDT only** — this is a 21st-century mechanism. There is no pre-modern or FDT cell.

## THE THREE LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs D.1.a (postmaterialism / self-actualization).** D.1.a is a *positive* preference shift: the
desire for children has genuinely fallen in favour of autonomy, career, or self-realization. D.3.b is
*fear suppressing a live desire*. A paper is D.3.b only if BOTH (a) the operative content is ecological
fear or eco-ethical concern, AND (b) the desire for children is not simply relabeled freedom/career/
lifestyle preference. A climate-mentioning paper whose actual estimand is a positive child-free
preference routes to `OFF_POSTMATERIALIST_D1a`. This is a HARD line.

**Wall 2 — vs D.3.a (mental-health epidemic).** General clinical anxiety or depression → fertility is
D.3.a. D.3.b requires the feared object to be **specifically ecological/planetary**. A general
psychological-distress measure with no climate content routes to `OFF_CLINICAL_D3a`, even in a paper
that frames itself around climate.

**Wall 3 — vs C.5.a (economic uncertainty).** Same "the future looks bad" shape, different feared object.
If the fear is about the respondent's own job, income, or economic security — or the mechanism is
option-value / wait-and-see on a return to normalcy — it is `OFF_ECON_C5a`. D.3.b's feared object is
planetary habitability or emissions ethics, and its mechanism is affect/dread.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_HABITABILITY_FEAR | PRIMARY_CARBON_ETHICS | PRIMARY_ECO_PESSIMISM | DESIRE_INDEPENDENCE | THEORY | OFF_POSTMATERIALIST_D1a | OFF_CLINICAL_D3a | OFF_ECON_C5a | OFF_OUTCOME | REVERSE | NA",
  "outcome_level": "STATED_INTENTION_OR_ATTITUDE | REALIZED_FERTILITY | BOTH | NA",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "desire_for_children_held_fixed": "yes | no | unclear",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: studies or models ecological fear / eco-doom / carbon-ethics concern as a determinant of
  fertility intention or realized fertility, or evidence that such fear suppresses childbearing while the
  desire for children remains positive.
- `UNCERTAIN`: plausibly belongs, but missing/ambiguous information prevents confident routing.
- `NOT_RELEVANT`: does not bear on the ecological-fear → fertility estimand. General climate-attitude,
  general fertility-decline, and physical-climate-exposure papers are NOT automatically relevant.

## Estimand cells

- `PRIMARY_HABITABILITY_FEAR`: fear that the world will be uninhabitable or dangerous *for one's children*
  → reduced fertility intention or realized fertility.
- `PRIMARY_CARBON_ETHICS`: the ethical concern that an additional child adds emissions / anti-natalism
  for the planet → reduced fertility intention or behavior.
- `PRIMARY_ECO_PESSIMISM`: generalized ecological pessimism or eco-doom about the collective future →
  reduced fertility intention or behavior.
- `DESIRE_INDEPENDENCE`: any of the above, where fertility or intention falls while the *desire* for
  children is positive or explicitly held fixed. This is the value-added cell — use it in preference to
  the three PRIMARY cells whenever the design actually separates fear from desire.
- `THEORY`: anti-natalist / eco-ethics philosophy, or climate-anxiety construct and scale-validation work,
  with no empirical fertility estimate.
- `OFF_POSTMATERIALIST_D1a`: positive self-actualization / autonomy preference or secular value shift with
  no fear content → fertility. Route to D.1.a (Wall 1).
- `OFF_CLINICAL_D3a`: general, non-climate-specific anxiety or depression → reproductive intention or
  fertility. Route to D.3.a (Wall 2).
- `OFF_ECON_C5a`: personal economic / job / income insecurity as the feared object → fertility. Route to
  C.5.a (Wall 3).
- `OFF_OUTCOME`: climate anxiety / eco-worry measured with NO fertility or reproductive-intention outcome.
  Mechanism or context only.
- `REVERSE`: parenthood or fertility status → climate concern / eco-worry.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both an ecological-fear / eco-ethics mechanism AND a fertility or reproductive-intention outcome must
   be present for a PRIMARY or `DESIRE_INDEPENDENCE` cell.
2. `outcome_level` is mandatory on every RELEVANT or UNCERTAIN empirical paper. Stated intentions,
   desires, planned parity, and "climate is a reason I will have fewer children" are
   `STATED_INTENTION_OR_ATTITUDE`; completed or observed births/parity are `REALIZED_FERTILITY`. Both
   levels are in scope; the tag is never a reason to exclude. Use `NA` only for theory and
   `NOT_RELEVANT` records.
3. **Physical climate exposure** — heat, drought, disaster, or pollution → fertility or reproductive
   health, with no affective or attitudinal mechanism — is `NOT_RELEVANT` / `NA`. It belongs to the
   physical-climate-shock and biological-reproductive-health hypotheses, not here. Say so in `reason`.
4. Do not promote an OFF-cell paper to PRIMARY merely because climate change is mentioned as motivation.
   Conversely, do not demote a paper with a genuine ecological-fear estimand merely because it also
   reports economic or political covariates.
5. Reviews may be `RELEVANT` but cannot be PRIMARY; use the best non-primary cell and
   `evidence_type=review`.
6. Set `desire_for_children_held_fixed=yes` only when the design actually holds the desire for children
   constant or reports it as positive alongside the fertility decline. This clause is what separates
   D.3.b's value-added claim from D.1.a's preference-shift claim (Wall 1).
7. A bare climate-anxiety construct or scale paper with no fertility outcome is `THEORY` (if it develops
   the construct) or `OFF_OUTCOME` (if it applies it to a non-fertility outcome) — never PRIMARY.
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
