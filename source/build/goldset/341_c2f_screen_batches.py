#!/usr/bin/env python3
"""341 — emit blinded screening batches for C.2.f, and a depth probe across the universe.

Direct port of C.2.b's 322.

`--probe K N` takes N records from each of K evenly spaced strata of the citation-ranked universe.
Screening front-to-back tells you the yield of the head and nothing about the tail, and a truncated
pass then reports the head as if it were the population
(`citation-sorted-head-is-not-the-population`). Spaced part-batches map the whole curve for the cost
of two (`probe-depth-dont-screen-sequentially`: A.18 went 53% / 9.1% / 3.3% / 0.7%).

`--batch I SIZE` emits one sequential batch for the full pass.

Batches are BLINDED: no gold flag, no provenance, no arm membership. The arm predicts the cell, so
showing it would make the screen agree with the query rather than judge the record — and on this
chapter that matters more than usual, because the `dispersion` arm is 851 of 1,366 rows and scope §3
measured its vocabulary as 89% off-mechanism.

Every emitted row must come back with a verdict, including the obvious excludes: hidden controls need
a verdict on every row or sensitivity cannot be computed
(`a-positives-only-screen-cannot-measure-sensitivity`).

`title_only` is carried on each row. 313 of 1,366 records have no abstract, and a title-only
judgement is a weaker judgement that must be visible as one.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = ROOT / "extraction" / "rising-inequality-and-status-competition-screen-batches"
ABSTRACT_CHARS = 460


def load():
    d = json.loads((LOGS / "rising-inequality-and-status-competition-screen-universe.json").read_text())
    return d["records"]


def emit(rows, name):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(
        {"name": name, "n": len(rows), "records": rows}, indent=1) + "\n")
    L = [f"# Screen batch `{name}` — {len(rows)} records", "",
         "Blinded: no gold flag, no provenance, no arm. Apply "
         "`literature/search-logs/rising-inequality-and-status-competition-screen-rubric.md`. **Every row needs a verdict**, "
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
    ap.add_argument("--remaining", type=int, metavar="SIZE",
                    help="emit every record with no verdict yet, in batches of SIZE. The probe "
                         "returned a FLAT yield curve, so the remainder cannot be truncated: the "
                         "cleanest primary record in the probe was in the last stratum.")
    a = ap.parse_args()
    recs = load()
    for i, r in enumerate(recs):
        r["screen_id"] = f"C2F{i:04d}"          # stable, position-based, reveals nothing.
        # Prefix was C2B until 2026-09-08: the port carried C.2.b's literal, which would have
        # collided with that chapter's ids in any shared extraction table.
    keep = ("screen_id", "title", "year", "venue", "type", "cited_by", "abstract")
    slim = [{k: r.get(k) for k in keep} for r in recs]

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
        vp = ROOT / "extraction" / "rising-inequality-and-status-competition-screen-verdicts.csv"
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
