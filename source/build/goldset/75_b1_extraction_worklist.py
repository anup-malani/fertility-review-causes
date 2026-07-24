#!/usr/bin/env python3
"""B.1 TICK-033 step 75: build the full-text extraction worklist.

Joins the PDFs that have actually landed in `literature/pdfs/<slug>/` (named in the
`W<openalex_id>__<slug>.pdf` convention laid down by `74_b1_ingest_pdfs.py`) against
the frozen estimand-ready screening set, and reports which of them still owe an
effect-size extraction.

The output is the RA/PI worklist for TICK-033: one row per landed PDF, ordered so
that the poolable core (PROXIMATE_ULTIMATE, the status -> reproductive-success
dissociation cell that Section 6 of the chapter is waiting on) comes first.

Usage
-----
    python3 source/build/goldset/75_b1_extraction_worklist.py [--pdf-dir DIR]

`literature/pdfs/` is gitignored, so when this is run from a git worktree the PDFs
live in the primary checkout; pass `--pdf-dir` to point at them.

Outputs
-------
    extraction/<slug>-extraction-worklist.csv
    extraction/<slug>-extraction-worklist.md
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"

# Cell ordering: the poolable status -> reproductive-success core first, because that
# is the cell the chapter's PENDING pooled number depends on. MOTIVATION_DISTINCTNESS
# is a separate (mostly scale-validation) stream that does not feed the same pool.
CELL_PRIORITY = {
    "PROXIMATE_ULTIMATE": 0,
    "PRIMARY_DECOUPLING": 1,
    "PRIMARY_DESIRE_INDEPENDENCE": 2,
    "MOTIVATION_DISTINCTNESS": 3,
}

PDF_RE = re.compile(r"^(W\d+)__(.+)\.pdf$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_screen_set(root: Path) -> dict[str, dict]:
    path = root / "output" / f"{SLUG}-estimand-ready-set.json"
    records = json.loads(path.read_text())
    return {r["paperId"]: r for r in records}


def load_theory_stream(root: Path) -> dict[str, dict]:
    path = root / "output" / f"{SLUG}-theory-stream.json"
    if not path.exists():
        return {}
    return {r["paperId"]: r for r in json.loads(path.read_text())}


def load_effects(root: Path) -> dict[str, list[dict]]:
    path = root / "extraction" / f"{SLUG}-effects.csv"
    by_study: dict[str, list[dict]] = {}
    if not path.exists():
        return by_study
    with path.open() as fh:
        for row in csv.DictReader(fh):
            by_study.setdefault(row["study_id"], []).append(row)
    return by_study


def extraction_status(rows: list[dict]) -> str:
    """Collapse a study's effect rows into one worklist status."""
    if not rows:
        return "TODO"
    if all((r.get("exclude") or "").strip().lower() == "yes" for r in rows):
        return "EXCLUDED"
    live = [r for r in rows if (r.get("exclude") or "").strip().lower() != "yes"]
    if any((r.get("needs_pi") or "").strip().lower() == "yes" for r in live):
        return "NEEDS_PI"
    if any((r.get("effect_value") or "").strip() for r in live):
        return "EXTRACTED"
    return "NEEDS_PI"


def main() -> None:
    root = repo_root()
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--pdf-dir",
        default=str(root / "literature" / "pdfs" / SLUG),
        help="directory holding the W<id>__<slug>.pdf files",
    )
    args = ap.parse_args()

    pdf_dir = Path(args.pdf_dir).expanduser()
    if not pdf_dir.is_dir():
        raise SystemExit(f"pdf dir not found: {pdf_dir}")

    screen = load_screen_set(root)
    theory = load_theory_stream(root)
    effects = load_effects(root)

    landed: dict[str, str] = {}
    for pdf in sorted(pdf_dir.glob("W*__*.pdf")):
        m = PDF_RE.match(pdf.name)
        if m:
            landed[m.group(1)] = pdf.name

    rows = []
    for work_id, filename in landed.items():
        rec = screen.get(work_id)
        stream = "estimand_ready"
        if rec is None:
            rec = theory.get(work_id)
            stream = "theory" if rec else "unmatched"
        cell = (rec or {}).get("cell", "")
        rows.append(
            {
                "study_id": work_id,
                "pdf_filename": filename,
                "stream": stream,
                "cell": cell,
                "tier": (rec or {}).get("tier", ""),
                "both_channel": (rec or {}).get("both_channel", ""),
                "year": (rec or {}).get("year", ""),
                "title": (rec or {}).get("title", ""),
                "venue": (rec or {}).get("venue", ""),
                "doi": (rec or {}).get("doi", ""),
                "evidence_type": (rec or {}).get("evidence_type", ""),
                "holds_child_preference_fixed": (rec or {}).get(
                    "holds_child_preference_fixed", ""
                ),
                "extraction_status": extraction_status(effects.get(work_id, [])),
                "n_effect_rows": len(effects.get(work_id, [])),
            }
        )

    rows.sort(
        key=lambda r: (
            CELL_PRIORITY.get(r["cell"], 9),
            {"TODO": 0, "NEEDS_PI": 1, "EXTRACTED": 2, "EXCLUDED": 3}[
                r["extraction_status"]
            ],
            str(r["year"]),
        )
    )

    out_csv = root / "extraction" / f"{SLUG}-extraction-worklist.csv"
    with out_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    by_status = Counter(r["extraction_status"] for r in rows)
    by_cell = Counter(r["cell"] or "(unmatched)" for r in rows)

    # Which estimand-ready papers are still missing a PDF, by cell -- this is what
    # remains of TICK-032 retrieval, and it bounds how large the pool can get.
    missing_by_cell = Counter(
        r["cell"] for pid, r in screen.items() if pid not in landed
    )

    lines = [
        f"# B.1 full-text extraction worklist (TICK-033)",
        "",
        f"- PDFs landed in convention: **{len(rows)}**",
        f"- estimand-ready set: **{len(screen)}** papers; "
        f"**{sum(1 for r in rows if r['stream'] == 'estimand_ready')}** of them have a PDF",
        "",
        "## Extraction status",
        "",
        "| status | n |",
        "|---|---|",
    ]
    for status in ("TODO", "NEEDS_PI", "EXTRACTED", "EXCLUDED"):
        lines.append(f"| {status} | {by_status.get(status, 0)} |")
    lines += [
        "",
        "## Landed PDFs by estimand cell",
        "",
        "| cell | landed | still missing a PDF |",
        "|---|---|---|",
    ]
    for cell in sorted(by_cell, key=lambda c: CELL_PRIORITY.get(c, 9)):
        lines.append(
            f"| {cell} | {by_cell[cell]} | {missing_by_cell.get(cell, 0)} |"
        )

    lines += ["", "## Worklist (poolable core first)", ""]
    lines += [
        "| # | status | cell | study | year | title | venue |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        title = (r["title"] or "(no screen record)")[:80]
        lines.append(
            f"| {i} | {r['extraction_status']} | {r['cell']} | {r['study_id']} | "
            f"{r['year']} | {title} | {(r['venue'] or '')[:40]} |"
        )
    lines.append("")

    out_md = root / "extraction" / f"{SLUG}-extraction-worklist.md"
    out_md.write_text("\n".join(lines))

    print(f"landed PDFs: {len(rows)}")
    print(f"status: {dict(by_status)}")
    print(f"cells: {dict(by_cell)}")
    print(f"wrote {out_csv}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
