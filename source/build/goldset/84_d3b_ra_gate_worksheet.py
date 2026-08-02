#!/usr/bin/env python3
"""TICK-047: build the D.3.b RA gate worksheet.

The screen verdicts in output/climate-anxiety-eco-doomerism-screen-tiers.json are
AUTOMATED. This script emits the worksheet a human signs off on, in three strata with
different urgencies, and records the sampling rule on the face of the output so the
gate is reproducible rather than an ad hoc read-through.

Strata:
  A. DECISIVE_12       -- the 8 realized-fertility studies + the 4 DESIRE_INDEPENDENCE
                          studies. Gates TICK-049 extraction. Full census, not sampled.
  B. WALL1_D1A_SAMPLE  -- a seeded sample of the 50 records routed OFF_POSTMATERIALIST_D1a.
                          The left-politics/education/secularism confound is at once the
                          Wall 1 routing rule and the chapter's central identification
                          threat, so a misroute here and a confounded estimate are the
                          same error. This is where a screening mistake costs most.
  C. INSUFFICIENT_INFO -- all 122 records the screen could not resolve from title alone.
                          Full census; disposition each to a cell, to full text, or out.

Also emitted, unsampled and for reference: the two other walls (C.5.a 33, D.3.a 1), since
the ticket asks for an overturn rate BY WALL and D.3.a's single record is the whole
population of that wall.

Sampling rule: deterministic. Records are sorted by (year desc, paperId) and every
record is included when the stratum is a census; the Wall 1 sample takes a fixed-seed
random draw of WALL1_SAMPLE_N, with the seed and n written into the log so the same
draw reproduces. No unseeded randomness anywhere.

Outputs:
  extraction/climate-anxiety-eco-doomerism-ra-gate.csv
  literature/search-logs/climate-anxiety-eco-doomerism-ra-gate-log.md
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

SLUG = "climate-anxiety-eco-doomerism"
ROOT = Path(__file__).resolve().parents[3]
TIERS = ROOT / "output" / f"{SLUG}-screen-tiers.json"
POOL_STATED = ROOT / "output" / f"{SLUG}-estimand-ready-stated.json"
POOL_REALIZED = ROOT / "output" / f"{SLUG}-estimand-ready-realized.json"
GATE = ROOT / "extraction" / f"{SLUG}-ra-gate.csv"
GATE_LOG = ROOT / "literature" / "search-logs" / f"{SLUG}-ra-gate-log.md"

WALL1_SEED = 20260727
WALL1_SAMPLE_N = 15

# The two classification calls TICK-047 asks to resolve before extraction, pre-loaded
# into the worksheet so they are decided rather than rediscovered at TICK-049.
PREFLAGGED = {
    "10.1111/sjpe.12125": (
        "Formal endogenous-growth model; no empirical realized fertility. "
        "Candidate move to theory stream."
    ),
    "10.1257/pandp.20251127": (
        "Identifies from air-pollution exposure, not expressed ecological dread. "
        "Precision-rule 3 boundary."
    ),
}

COLUMNS = [
    "stratum",
    "priority",
    "work_id",
    "doi",
    "year",
    "venue",
    "screen_verdict",
    "screen_cell",
    "screen_route_to",
    "outcome_level",
    "evidence_type",
    "desire_for_children_held_fixed",
    "screen_reason",
    "preflagged_issue",
    # --- RA fills these ---
    "ra_verdict",
    "ra_cell",
    "ra_route_to",
    "agree_or_overturn",
    "ra_reason",
    "send_to_fulltext",
    "ra_initials",
    "ra_date",
    "title",
]


def row(rec: dict, stratum: str, priority: int) -> dict:
    doi = rec.get("doi") or ""
    return {
        "stratum": stratum,
        "priority": priority,
        "work_id": rec.get("paperId", ""),
        "doi": doi,
        "year": rec.get("year"),
        "venue": rec.get("venue") or "",
        "screen_verdict": rec.get("verdict"),
        "screen_cell": rec.get("cell"),
        "screen_route_to": rec.get("route_to") or "",
        "outcome_level": rec.get("outcome_level"),
        "evidence_type": rec.get("evidence_type"),
        "desire_for_children_held_fixed": rec.get("desire_for_children_held_fixed"),
        "screen_reason": (rec.get("reason") or "")[:300],
        "preflagged_issue": PREFLAGGED.get(doi, ""),
        "ra_verdict": "",
        "ra_cell": "",
        "ra_route_to": "",
        "agree_or_overturn": "",
        "ra_reason": "",
        "send_to_fulltext": "",
        "ra_initials": "",
        "ra_date": "",
        "title": (rec.get("title") or "")[:160],
    }


def main() -> None:
    tiers = json.load(open(TIERS))
    by_id = {r["paperId"]: r for r in tiers}

    realized_ids = [r["paperId"] for r in json.load(open(POOL_REALIZED))]
    stated = json.load(open(POOL_STATED))
    di_ids = [r["paperId"] for r in stated if r.get("cell") == "DESIRE_INDEPENDENCE"]

    rows: list[dict] = []
    seen: set[str] = set()

    def add(pid: str, stratum: str, priority: int) -> None:
        if pid in seen or pid not in by_id:
            return
        seen.add(pid)
        rows.append(row(by_id[pid], stratum, priority))

    # A. Decisive 12 -- census.
    for pid in realized_ids:
        add(pid, "A_DECISIVE_12_realized", 0)
    for pid in di_ids:
        add(pid, "A_DECISIVE_12_desire_independence", 0)

    # B. Wall 1 sample -- seeded draw from the 50 D.1.a route-aways.
    wall1 = sorted(
        (r for r in tiers if r.get("cell") == "OFF_POSTMATERIALIST_D1a"),
        key=lambda r: (-(r.get("year") or 0), r["paperId"]),
    )
    rng = random.Random(WALL1_SEED)
    wall1_sample = sorted(
        rng.sample(wall1, min(WALL1_SAMPLE_N, len(wall1))),
        key=lambda r: (-(r.get("year") or 0), r["paperId"]),
    )
    for r in wall1_sample:
        add(r["paperId"], "B_WALL1_D1A_SAMPLE", 1)

    # C. INSUFFICIENT_INFO -- census.
    insuff = sorted(
        (r for r in tiers if r.get("cell") == "INSUFFICIENT_INFO"),
        key=lambda r: (-(r.get("year") or 0), r["paperId"]),
    )
    for r in insuff:
        add(r["paperId"], "C_INSUFFICIENT_INFO", 2)

    # D. Other walls -- census, small; needed for the by-wall overturn rate.
    other_walls = sorted(
        (r for r in tiers if r.get("cell") in ("OFF_ECON_C5a",) or r.get("route_to") == "D.3.a"),
        key=lambda r: (-(r.get("year") or 0), r["paperId"]),
    )
    for r in other_walls:
        add(r["paperId"], "D_OTHER_WALLS", 3)

    rows.sort(key=lambda r: (r["priority"], r["stratum"], -(r["year"] or 0), r["work_id"]))

    GATE.parent.mkdir(parents=True, exist_ok=True)
    with open(GATE, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=COLUMNS)
        wtr.writeheader()
        wtr.writerows(rows)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["stratum"]] = counts.get(r["stratum"], 0) + 1

    GATE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(GATE_LOG, "w") as fh:
        fh.write(f"""# RA gate worksheet — {SLUG} (TICK-047)

Generated by `source/build/goldset/84_d3b_ra_gate_worksheet.py` from the frozen screen
(`output/{SLUG}-screen-tiers.json`, 1,170 records). The screen verdicts are AUTOMATED;
this worksheet is the human sign-off over them.

Worksheet: `extraction/{SLUG}-ra-gate.csv` — {len(rows)} rows.

## Strata and why each exists

| Stratum | Rows | Census or sample | Why |
|---|---|---|---|
| A_DECISIVE_12_realized | {counts.get('A_DECISIVE_12_realized', 0)} | census | The realized-fertility pool. Gates TICK-049. |
| A_DECISIVE_12_desire_independence | {counts.get('A_DECISIVE_12_desire_independence', 0)} | census | The hypothesis's distinctive claim. Gates TICK-049. |
| B_WALL1_D1A_SAMPLE | {counts.get('B_WALL1_D1A_SAMPLE', 0)} | sample of {len(wall1)} | Wall 1 misroutes are the costliest screening error. |
| C_INSUFFICIENT_INFO | {counts.get('C_INSUFFICIENT_INFO', 0)} | census | Could not be screened from title alone. |
| D_OTHER_WALLS | {counts.get('D_OTHER_WALLS', 0)} | census | Needed for a by-wall overturn rate; C.5.a is 33 and D.3.a is 1. |

## Sampling rule

Deterministic and reproducible. Strata A, C, and D are censuses. Stratum B is a
fixed-seed draw: `random.Random({WALL1_SEED}).sample(wall1, {WALL1_SAMPLE_N})` over the
{len(wall1)} `OFF_POSTMATERIALIST_D1a` records sorted by (year desc, paperId). Re-running
this script reproduces the identical draw. No unseeded randomness is used anywhere.

Stratum B is a sample rather than a census because its purpose is to *estimate* the Wall 1
misroute rate, not to correct every Wall 1 call. If the sampled overturn rate is
non-trivial, the right response is to widen stratum B to a census before TICK-049 —
record that decision here rather than quietly proceeding.

## Order of work

Priority column, ascending. Stratum A first: it is the only stratum that blocks
extraction, and until it is signed off nothing downstream may start. Strata B, C, and D
can proceed alongside TICK-048 retrieval.

## Pre-flagged classification calls

Two records in the realized-fertility 8 carry a known issue, pre-loaded into the
`preflagged_issue` column so they are decided here rather than discovered at extraction:

- `10.1111/sjpe.12125` (Scottish J. Political Economy 2017) — formal endogenous-growth
  model with no empirical realized fertility in it.
- `10.1257/pandp.20251127` (AEA P&P 2025) — identifies from air-pollution exposure rather
  than expressed ecological dread; the precision-rule 3 boundary.

If both are set aside the empirical realized base is 6, two of them not peer-reviewed.
That number propagates into chapter sections 1, 5.2, 10, and 12, and any change must be
written back into `output/{SLUG}-screen-report.md` as well as the chapter, so the
generated report and the prose cannot drift.

## Columns the RA fills

`ra_verdict`, `ra_cell`, `ra_route_to`, `agree_or_overturn`, `ra_reason`,
`send_to_fulltext`, `ra_initials`, `ra_date`. Everything to the left of `ra_verdict` is
generated and should not be edited by hand — if a generated value is wrong, the fix
belongs in the screen or in this script.
""")

    print(f"gate worksheet -> {GATE.relative_to(ROOT)} ({len(rows)} rows)")
    for s, n in sorted(counts.items()):
        print(f"  {s}: {n}")
    print(f"log            -> {GATE_LOG.relative_to(ROOT)}")
    print(f"Wall 1 population {len(wall1)}, sampled {len(wall1_sample)}, seed {WALL1_SEED}")


if __name__ == "__main__":
    main()
