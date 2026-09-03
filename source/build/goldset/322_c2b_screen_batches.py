#!/usr/bin/env python3
"""322 — emit blinded screening batches for C.2.b, and a depth probe across the universe.

Two modes.

`--probe K N` takes N records from each of K evenly spaced strata of the citation-ranked universe.
Screening front-to-back tells you the yield of the head and nothing about the tail, and a truncated
or abandoned pass then reports the head as if it were the population
(`citation-sorted-head-is-not-the-population`). Spaced part-batches map the whole curve for the cost
of two (`probe-depth-dont-screen-sequentially`: A.18 went 53% / 9.1% / 3.3% / 0.7% across strata).

`--batch I SIZE` emits one sequential batch for the full pass.

Batches are BLINDED: no gold flag, no provenance, no arm membership. The arm a record arrived on
predicts its cell, so showing it would make the screen agree with the query rather than judge the
record. Every emitted row must come back with a verdict, including the obvious excludes — hidden
controls need a verdict on every row or sensitivity cannot be computed
(`a-positives-only-screen-cannot-measure-sensitivity`).

Usage:
  python3 source/build/goldset/322_c2b_screen_batches.py --probe 5 30
  python3 source/build/goldset/322_c2b_screen_batches.py --batch 0 120
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = ROOT / "extraction" / "child-cost-direct-screen-batches"
ABSTRACT_CHARS = 700


def load():
    d = json.loads((LOGS / "child-cost-direct-screen-universe.json").read_text())
    return d["records"]


def emit(rows, name):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(
        {"name": name, "n": len(rows), "records": rows}, indent=1) + "\n")
    L = [f"# Screen batch `{name}` — {len(rows)} records", "",
         "Blinded: no gold flag, no provenance, no arm. Apply "
         "`literature/search-logs/child-cost-direct-screen-rubric.md`. **Every row needs a verdict**, "
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
    a = ap.parse_args()
    recs = load()
    for i, r in enumerate(recs):
        r["screen_id"] = f"C2B{i:04d}"          # stable, position-based, reveals nothing
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
    elif a.batch:
        i, size = a.batch
        emit(slim[i * size:(i + 1) * size], f"batch-{i:03d}")
    else:
        ap.error("give --probe or --batch")


main()
