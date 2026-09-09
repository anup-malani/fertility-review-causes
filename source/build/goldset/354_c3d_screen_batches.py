#!/usr/bin/env python3
"""354 — emit blinded screening batches for C.3.d, and a depth probe across the universe.

Direct port of C.2.f's 341 (itself C.2.b's 322).

`--probe K N` takes N records from each of K evenly spaced strata of the citation-ranked universe.
Screening front-to-back tells you the yield of the head and nothing about the tail, and a truncated
pass then reports the head as if it were the population
(`citation-sorted-head-is-not-the-population`). Spaced part-batches map the whole curve for the cost
of two (`probe-depth-dont-screen-sequentially`: A.18 went 53% / 9.1% / 3.3% / 0.7%).

Batches are BLINDED: no gold flag, no provenance, no arm membership. **The arm predicts the cell**,
so showing it would make the screen agree with the query rather than judge the record — and on this
chapter the arm predicts the DIRECTION, which is scope §2's ruling and the single most consequential
field in the table. A screen told that a row came from the `backward` arm would route it backward
without reading it.

Every emitted row must come back with a verdict, including the obvious excludes: hidden controls
need a verdict on every row or sensitivity cannot be computed
(`a-positives-only-screen-cannot-measure-sensitivity`).

`title_only` is carried on each row. 692 of 3,254 records (21%) have no abstract, and a title-only
judgement is a weaker judgement that must be visible as one.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = ROOT / "extraction" / "quantity-quality-tradeoff-screen-batches"
ABSTRACT_CHARS = 460


def load():
    d = json.loads((LOGS / "quantity-quality-tradeoff-screen-universe.json").read_text())
    return d["records"]


def emit(rows, name):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(
        {"name": name, "n": len(rows), "records": rows}, indent=1) + "\n")
    L = [f"# Screen batch `{name}` — {len(rows)} records", "",
         "Blinded: no gold flag, no provenance, no arm. Apply "
         "`literature/search-logs/quantity-quality-tradeoff-screen-rubric.md`. **Every row needs a verdict**, "
         "including obvious excludes.", ""]
    for i, r in enumerate(rows, 1):
        ab = (r.get("abstract") or "").strip()
        ab = (ab[:ABSTRACT_CHARS] + "…") if len(ab) > ABSTRACT_CHARS else (ab or "**NO ABSTRACT**")
        L += [f"### {i}. `{r['screen_id']}` — {r.get('title') or '(untitled)'}",
              f"*{r.get('year') or '?'} · {r.get('venue') or 'no venue'} · "
              f"{r.get('type') or '?'} · cited {r.get('cited_by') if r.get('cited_by') is not None else '?'}*",
              "", ab, ""]
    (OUT / f"{name}.md").write_text("\n".join(L))
    print(f"wrote {name}: {len(rows)} records -> {OUT.relative_to(ROOT)}/{name}.{{json,md}}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", nargs=2, type=int, metavar=("STRATA", "PER"))
    ap.add_argument("--batch", nargs=2, type=int, metavar=("INDEX", "SIZE"))
    ap.add_argument("--arms", metavar="A,B",
                    help="screen the named arms EXHAUSTIVELY, mixed with size-matched decoys from "
                         "the rest of the universe and shuffled. An evenly spaced probe samples the "
                         "universe in proportion, so a small arm gets few rows and its yield is "
                         "estimated from almost nothing -- `forward-shock` is 686 of 3,254 and holds "
                         "the registered forward estimand. Decoys exist because a pure single-arm "
                         "batch would tell the screen every row's arm, and the arm predicts the "
                         "DIRECTION, which is the field scope §2 turns on.")
    ap.add_argument("--decoy-ratio", type=float, default=0.5,
                    help="decoys as a fraction of the targeted rows (default 0.5)")
    ap.add_argument("--remaining", type=int, metavar="SIZE",
                    help="emit every record with no verdict yet, in batches of SIZE. Whether the "
                         "remainder can be truncated is a question for the probe's yield curve, not "
                         "an assumption -- on C.2.b it was flat and the best record was in the LAST "
                         "stratum (`a-flat-yield-curve-forbids-truncation`).")
    a = ap.parse_args()
    recs = load()
    for i, r in enumerate(recs):
        r["screen_id"] = f"C3D{i:04d}"          # stable, position-based, reveals nothing.
        # The prefix is the chapter, not the port source. C.2.f had to fix this after inheriting
        # C.2.b's literal, which would have collided in any shared extraction table.
    keep = ("screen_id", "title", "year", "venue", "type", "cited_by", "abstract")
    slim = [{k: r.get(k) for k in keep} for r in recs]

    if a.arms:
        import random
        want = {x.strip() for x in a.arms.split(",")}
        by_id = {r["screen_id"]: r for r in recs}
        tgt = [r["screen_id"] for r in recs if want & set(r.get("arms") or [])]
        rest = [r["screen_id"] for r in recs if not (want & set(r.get("arms") or []))]
        random.seed(83)                      # reproducible mix; the seed is the ticket number
        decoys = random.sample(rest, min(len(rest), int(len(tgt) * a.decoy_ratio)))
        ids = tgt + decoys
        random.shuffle(ids)                  # so no row's arm is inferable from its position
        rows = [{k: by_id[i].get(k) for k in keep} for i in ids]
        for j in range(0, len(rows), 60):
            emit(rows[j:j + 60], f"arms-{'-'.join(sorted(want))}-{j // 60}")
        print(f"\n{len(tgt)} records in {sorted(want)} (exhaustive) + {len(decoys)} decoys "
              f"= {len(ids)} rows, shuffled. Arm membership is NOT in the emitted rows.")
        return

    if a.probe:
        k, per = a.probe
        span = len(slim) / k
        for s in range(k):
            lo = int(s * span)
            emit(slim[lo:lo + per], f"probe-s{s + 1}-of-{k}")
        print(f"\n{k} strata x {per} = {k * per} of {len(slim)} records "
              f"({100 * k * per / len(slim):.0f}% of the universe), evenly spaced by citation rank")
    elif a.remaining:
        import csv
        done = set()
        vp = ROOT / "extraction" / "quantity-quality-tradeoff-screen-verdicts.csv"
        if vp.exists():
            with vp.open() as f:
                done = {r["screen_id"] for r in csv.DictReader(f)}
        left = [r for r in slim if r["screen_id"] not in done]
        print(f"{len(done)} already screened, {len(left)} remaining of {len(slim)}")
        for i in range(0, len(left), a.remaining):
            emit(left[i:i + a.remaining], f"rest-{i // a.remaining:02d}")
    elif a.batch:
        i, size = a.batch
        emit(slim[i * size:(i + 1) * size], f"batch-{i:03d}")
    else:
        ap.error("give --probe, --remaining or --batch")


main()
