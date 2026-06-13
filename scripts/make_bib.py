#!/usr/bin/env python3
"""Generate per-hypothesis BibTeX files from the DOI-keyed registry.

Source of truth:   datastore/studies.json
Generated output:  literature/bib/<hypothesis-slug>.bib  (one entry per included study)

Run via `make bib`. Do not hand-edit the .bib files — they are overwritten on every run.
Only studies with screen_status == "included" are emitted. A study mapped to N hypotheses
appears in N .bib files.
"""
from __future__ import annotations

import json
import pathlib
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "datastore" / "studies.json"
BIB_DIR = ROOT / "literature" / "bib"


def bib_escape(value: str) -> str:
    return str(value).replace("{", r"\{").replace("}", r"\}")


def to_bibtex(study: dict) -> str:
    entry_type = study.get("type", "article")
    citekey = study["citekey"]
    fields = {
        "title": study.get("title", ""),
        "author": " and ".join(study.get("authors", [])),
        "year": study.get("year", ""),
        "journal": study.get("venue", ""),
        "doi": study.get("doi", ""),
    }
    lines = [f"@{entry_type}{{{citekey},"]
    for key, val in fields.items():
        if val:
            lines.append(f"  {key} = {{{bib_escape(val)}}},")
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    if not REGISTRY.exists():
        print(f"error: {REGISTRY} not found", file=sys.stderr)
        return 1

    data = json.loads(REGISTRY.read_text())
    studies = data.get("studies", [])

    by_hypothesis: dict[str, list[dict]] = defaultdict(list)
    for study in studies:
        if study.get("screen_status") != "included":
            continue
        for slug in study.get("hypotheses", []):
            by_hypothesis[slug].append(study)

    BIB_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for slug, items in sorted(by_hypothesis.items()):
        items.sort(key=lambda s: s.get("citekey", ""))
        out = BIB_DIR / f"{slug}.bib"
        out.write_text("\n\n".join(to_bibtex(s) for s in items) + "\n")
        print(f"  wrote {out.relative_to(ROOT)} ({len(items)} entries)")
        total += len(items)

    n_hyp = len(by_hypothesis)
    print(f"make bib: {total} included studies across {n_hyp} hypotheses")
    if total == 0:
        print("  (registry has no included studies yet — nothing to generate)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
