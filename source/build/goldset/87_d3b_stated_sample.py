#!/usr/bin/env python3
"""TICK-049: draw the stratified random sample of the stated-intention pool.

WHY A SAMPLE RATHER THAN A CENSUS OR A CONVENIENCE SET
------------------------------------------------------
The stated pool holds 60 studies after the TICK-047 gate. Extracting all of them means
retrieving ~39 more PDFs from publishers that have already bot-blocked us, which is weeks
of work. Extracting only the ones that happen to be open-access is worse than doing
nothing: that is precisely what capped the B.1 chapter, whose pooled estimate rests on 5
of 52 studies selected by OA availability rather than at random, and it would repeat a
failure already diagnosed in this repository.

What the chapter most needs from the stated literature is not a pooled effect -- the
realized track cannot pool either -- but the **Wall 1 bleed-in rate**: the share of studies
that measure environmental values or behaviour rather than ecological fear. On the realized
track that rate was 2 of 8. A random sample estimates it with a reportable interval. A
convenience sample estimates nothing, because open-access status plausibly correlates with
publisher, field, and study age.

DESIGN
------
- The DESIRE_INDEPENDENCE cell is CENSUSED, not sampled. It carries the hypothesis's
  distinctive claim and after the gate holds only 2 studies; sampling it would be absurd.
- The other three cells get a proportional stratified sample of SAMPLE_N, allocated by
  largest remainder so the allocation is reproducible rather than hand-rounded.
- The draw is seeded. Re-running reproduces it exactly.
- Sampling happens BEFORE retrieval, over the whole frame including studies already in
  hand. Sampling only the unretrieved would reintroduce the selection problem this design
  exists to avoid.

Outputs:
  extraction/{slug}-stated-sample.csv
  extraction/{slug}-stated-sample-retrieval-list.csv
  literature/search-logs/{slug}-stated-sample-log.md
"""
from __future__ import annotations

import csv
import json
import random
from collections import Counter
from pathlib import Path

SLUG = "climate-anxiety-eco-doomerism"
ROOT = Path(__file__).resolve().parents[3]
POOL_STATED = ROOT / "output" / f"{SLUG}-estimand-ready-stated.json"
RETRIEVAL_LOG = ROOT / "extraction" / f"{SLUG}-pdf-retrieval-log.csv"
OUT_SAMPLE = ROOT / "extraction" / f"{SLUG}-stated-sample.csv"
OUT_RETRIEVE = ROOT / "extraction" / f"{SLUG}-stated-sample-retrieval-list.csv"
LOG = ROOT / "literature" / "search-logs" / f"{SLUG}-stated-sample-log.md"

SEED = 20260727
SAMPLE_N = 20
CENSUS_CELLS = {"DESIRE_INDEPENDENCE"}

# TICK-047 gate outcomes affecting stated-pool membership.
ROUTED_OUT = {
    "W4414495777": "routed to D.1.a (Wall 1: exposure is government environmental spending support)",
    "W4412706512": "routed to theory stream (interpretive humanities, no estimand)",
}
CELL_REASSIGNED = {
    "W4402549764": "PRIMARY_ECO_PESSIMISM",  # respondent-attributed gap, not a DI design
}


def largest_remainder(counts: dict[str, int], total: int) -> dict[str, int]:
    """Proportional allocation without hand-rounding."""
    grand = sum(counts.values())
    if grand == 0:
        return {k: 0 for k in counts}
    exact = {k: v * total / grand for k, v in counts.items()}
    alloc = {k: int(v) for k, v in exact.items()}
    remaining = total - sum(alloc.values())
    order = sorted(counts, key=lambda k: (-(exact[k] - alloc[k]), k))
    for k in order[:remaining]:
        alloc[k] += 1
    return alloc


def main() -> None:
    pool = json.load(open(POOL_STATED))

    frame = []
    for rec in pool:
        pid = rec["paperId"]
        if pid in ROUTED_OUT:
            continue
        rec = dict(rec)
        rec["cell_post_gate"] = CELL_REASSIGNED.get(pid, rec["cell"])
        frame.append(rec)

    by_cell: dict[str, list[dict]] = {}
    for rec in frame:
        by_cell.setdefault(rec["cell_post_gate"], []).append(rec)
    for cell in by_cell:
        by_cell[cell].sort(key=lambda r: (-(r.get("year") or 0), r["paperId"]))

    census = {c: v for c, v in by_cell.items() if c in CENSUS_CELLS}
    sampled_cells = {c: v for c, v in by_cell.items() if c not in CENSUS_CELLS}
    alloc = largest_remainder({c: len(v) for c, v in sampled_cells.items()}, SAMPLE_N)

    rng = random.Random(SEED)
    selected: list[tuple[dict, str]] = []
    for cell, recs in census.items():
        for r in recs:
            selected.append((r, "census"))
    for cell in sorted(sampled_cells):
        recs = sampled_cells[cell]
        n = min(alloc[cell], len(recs))
        for r in sorted(rng.sample(recs, n), key=lambda r: (-(r.get("year") or 0), r["paperId"])):
            selected.append((r, "sampled"))

    have = {}
    if RETRIEVAL_LOG.exists():
        for r in csv.DictReader(open(RETRIEVAL_LOG)):
            have[r["work_id"]] = r
    already = lambda pid: bool(have.get(pid, {}).get("file"))

    rows = []
    for rec, how in selected:
        pid = rec["paperId"]
        lg = have.get(pid, {})
        rows.append({
            "work_id": pid, "selection": how, "cell_post_gate": rec["cell_post_gate"],
            "doi": rec.get("doi") or "", "year": rec.get("year"),
            "venue": rec.get("venue") or "", "evidence_type": rec.get("evidence_type"),
            "desire_for_children_held_fixed": rec.get("desire_for_children_held_fixed"),
            "pdf_in_hand": "yes" if already(pid) else "no",
            "oa_status": lg.get("oa_status", "unknown"),
            "access_class": ("in_hand" if already(pid)
                             else "closed" if lg.get("oa_status") == "closed"
                             else "oa_but_blocked"),
            "title": (rec.get("title") or "")[:130],
        })
    rows.sort(key=lambda r: (r["pdf_in_hand"] == "yes", r["cell_post_gate"], -(r["year"] or 0)))

    with open(OUT_SAMPLE, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    need = [r for r in rows if r["pdf_in_hand"] == "no"]
    with open(OUT_RETRIEVE, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["access_class", "cell_post_gate", "doi", "work_id",
                                           "year", "venue", "title"])
        w.writeheader()
        for r in sorted(need, key=lambda r: (r["access_class"] != "oa_but_blocked",
                                             r["cell_post_gate"])):
            w.writerow({k: r[k] for k in
                        ["access_class", "cell_post_gate", "doi", "work_id", "year", "venue", "title"]})

    cell_tbl = "\n".join(
        f"| {c} | {len(by_cell[c])} | {'census' if c in CENSUS_CELLS else alloc.get(c, 0)} |"
        for c in sorted(by_cell))
    acc = Counter(r["access_class"] for r in rows)

    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"""# Stated-intention pool — stratified random sample (TICK-049)

Generated by `source/build/goldset/87_d3b_stated_sample.py`. Seed `{SEED}`, target
{SAMPLE_N} sampled plus a census of {'/'.join(sorted(CENSUS_CELLS))}.

## Why a sample

Extracting all {len(frame)} stated studies means retrieving ~{sum(1 for r in frame if not already(r['paperId']))}
more PDFs from publishers that have already bot-blocked this project. Extracting only the
open-access ones is worse than not extracting: that is what capped the B.1 chapter, whose
pooled estimate rests on 5 of 52 studies selected by availability rather than at random.

What the chapter needs from this literature is the **Wall 1 bleed-in rate** — the share of
studies measuring environmental values or behaviour rather than ecological fear. On the
realized track that rate was 2 of 8. A random sample estimates it with a reportable
interval; a convenience sample estimates nothing.

## Frame and allocation

Frame is the frozen stated pool of 62, less {len(ROUTED_OUT)} routed out by the TICK-047 gate:

{chr(10).join(f'- `{k}` — {v}' for k, v in ROUTED_OUT.items())}

leaving **{len(frame)}**. One cell reassignment is applied
(`W4402549764` → PRIMARY_ECO_PESSIMISM, respondent-attributed gap rather than a DI design).

| Cell (post-gate) | In frame | Drawn |
|---|---:|---:|
{cell_tbl}

`DESIRE_INDEPENDENCE` is censused rather than sampled: it carries the hypothesis's
distinctive claim and holds only {len(by_cell.get('DESIRE_INDEPENDENCE', []))} studies after
the gate. Sampling it would be absurd.

Allocation across the other cells is proportional by largest remainder, so it is
reproducible rather than hand-rounded. The draw is
`random.Random({SEED}).sample(...)` over records sorted by (year desc, paperId).

## Sampling happened before retrieval

The draw runs over the whole frame, including studies already in hand. Sampling only the
unretrieved would reintroduce exactly the selection problem this design avoids.

| | n |
|---|---:|
| Selected (census + sample) | {len(rows)} |
| Already in hand | {acc['in_hand']} |
| To retrieve — free, bot-blocked | {acc['oa_but_blocked']} |
| To retrieve — genuinely closed | {acc['closed']} |

Retrieval list: `extraction/{SLUG}-stated-sample-retrieval-list.csv`, ordered
`oa_but_blocked` first — those need a browser, not entitlements.

## What this sample can and cannot support

**Can:** an estimate of the Wall 1 bleed-in rate with an interval; a characterisation of
designs, instruments, and populations; the share adjusting for the D.1.a confound.

**Cannot:** a pooled stated-intention effect representative of all {len(frame)}. The chapter
should present the stated track as a characterised map with a measured bleed-in rate, not
as a synthesis — consistent with the realized track, which TICK-051 also declined to pool.

**Non-response is a live threat.** If a large share of the sampled studies cannot be
retrieved, the realised sample stops being random and the estimate loses its warrant.
Record the retrieval rate over the SAMPLE specifically and report it; if it falls below
about two-thirds, say so rather than presenting the bleed-in rate as a clean estimate.
""")

    print(f"frame after gate: {len(frame)} (from {len(pool)})")
    for c in sorted(by_cell):
        tag = "census" if c in CENSUS_CELLS else f"draw {alloc.get(c, 0)}"
        print(f"  {c}: {len(by_cell[c])} in frame, {tag}")
    print(f"selected: {len(rows)} | in hand {acc['in_hand']} | "
          f"to retrieve {acc['oa_but_blocked']} blocked + {acc['closed']} closed")
    print(f"sample    -> {OUT_SAMPLE.relative_to(ROOT)}")
    print(f"retrieval -> {OUT_RETRIEVE.relative_to(ROOT)}")
    print(f"log       -> {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
