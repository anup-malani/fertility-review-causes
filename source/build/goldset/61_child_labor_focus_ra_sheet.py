#!/usr/bin/env python3
"""Create the focused pre-gold RA screen for TICK-031.

The complete 1,255-record screened frame remains the audit census. This sheet retains
only records routed to the chapter's empirical quantum, tempo, or theory streams.
Adjacent/off-outcome records remain in the census and can be recalled later if a primary
study needs mechanism support.
"""

import csv
import json
from collections import Counter
from pathlib import Path

SLUG = "child-labor-laws-and-schooling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUTPUT = REPO / "output"
KEEP_CELLS = {
    "PRIMARY_CS_QUANTUM",
    "PRIMARY_CL_QUANTUM",
    "PRIMARY_JOINT_QUANTUM",
    "TEMPO",
    "THEORY",
}
KEEP_VERDICTS = {"RELEVANT", "UNCERTAIN"}


def main():
    source = LOGS / f"{SLUG}-screened.json"
    rows = json.loads(source.read_text())
    focused = [
        row for row in rows
        if row["screen"]["verdict"] in KEEP_VERDICTS
        and row["screen"]["estimand_cell"] in KEEP_CELLS
    ]
    order = {
        "PRIMARY_CL_QUANTUM": 0,
        "PRIMARY_CS_QUANTUM": 1,
        "PRIMARY_JOINT_QUANTUM": 2,
        "TEMPO": 3,
        "THEORY": 4,
    }
    focused.sort(key=lambda row: (
        order[row["screen"]["estimand_cell"]],
        0 if row["screen"]["verdict"] == "RELEVANT" else 1,
        -(row.get("year") or 0),
        row.get("title") or "",
    ))

    destination = OUTPUT / f"{SLUG}-focused-ra-review.csv"
    fields = [
        "paperId", "doi", "title", "year", "authors", "venue",
        "verdict", "estimand_cell", "evidence_type", "treatment", "outcome",
        "direction", "reason", "abstract", "discovery_channels",
        "ra_decision", "ra_corrected_verdict", "ra_corrected_estimand_cell", "ra_note",
    ]
    with destination.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in focused:
            screen = row["screen"]
            writer.writerow({
                "paperId": row.get("paperId"),
                "doi": row.get("doi") or "",
                "title": row.get("title") or "",
                "year": row.get("year") or "",
                "authors": row.get("authors") or "",
                "venue": row.get("venue") or "",
                "verdict": screen.get("verdict"),
                "estimand_cell": screen.get("estimand_cell"),
                "evidence_type": screen.get("evidence_type"),
                "treatment": screen.get("treatment"),
                "outcome": screen.get("outcome"),
                "direction": screen.get("direction"),
                "reason": screen.get("reason"),
                "abstract": row.get("abstract") or "",
                "discovery_channels": ";".join(row.get("discovery_channels") or []),
                "ra_decision": "",
                "ra_corrected_verdict": "",
                "ra_corrected_estimand_cell": "",
                "ra_note": "",
            })

    counts = Counter(row["screen"]["estimand_cell"] for row in focused)
    print(f"wrote {destination.relative_to(REPO)}: {len(focused)} records")
    for cell in order:
        print(f"  {cell}: {counts[cell]}")


if __name__ == "__main__":
    main()
