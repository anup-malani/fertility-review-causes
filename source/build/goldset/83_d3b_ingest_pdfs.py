#!/usr/bin/env python3
"""83_d3b_ingest_pdfs.py — D.3.b (TICK-048). Identify and rename batch-installed PDFs.

The D.3.b analogue of 74_b1_ingest_pdfs.py. A human retrieves the bot-blocked and closed
PDFs by hand, in whatever names the browser produced ('430mcmullen.pdf', 'J of Marriage
and Family - 2026 - Ivanova - ....pdf'). This script identifies each file from its OWN
contents -- DOI printed in the text first, subtitle-insensitive title match as fallback
-- and renames matches to the pipeline's `W<OpenAlexID>__<slug>.pdf` convention, which
is what the retrieval log and the effects table key on.

No filename discipline is required of the retriever. Nothing is deleted. Renames are
DRY-RUN by default; pass --apply. Files already in the W<id>__ convention are untouched.

Identity map: both pooling sets plus the theory stream, so a PDF that turns out to be a
theory-stream paper is still identified rather than reported as unknown.

  python3 83_d3b_ingest_pdfs.py --source ~/Downloads/b1/d3b            # dry run
  python3 83_d3b_ingest_pdfs.py --source ~/Downloads/b1/d3b --apply

Outputs a reconciliation report to stdout and to
extraction/{slug}-pdf-ingest-report.md.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

SLUG = "climate-anxiety-eco-doomerism"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PDFDIR = REPO / "literature" / "pdfs" / SLUG
EXTR = REPO / "extraction"
CORPUS = [
    REPO / "output" / f"{SLUG}-estimand-ready-stated.json",
    REPO / "output" / f"{SLUG}-estimand-ready-realized.json",
    REPO / "output" / f"{SLUG}-theory-stream.json",
]
REPORT = EXTR / f"{SLUG}-pdf-ingest-report.md"

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)
WNAME_RE = re.compile(r"^W\d+__")


def norm_doi(d: str) -> str:
    return (d or "").strip().lower().replace("https://doi.org/", "").rstrip(".").rstrip(")")


def doi_variants(raw: str) -> list[str]:
    """A page-scraped DOI often carries trailing junk ('...12345doi:', a stray ')', a
    version suffix). Yield the raw form plus trimmed variants so an exact hit survives."""
    d = norm_doi(raw)
    out: list[str] = []
    for v in (d, re.sub(r"doi:?$", "", d), re.sub(r"v\d+$", "", d), d.rstrip(".,;:)]}-_")):
        v = v.rstrip(".,;:)]}-_")
        if v and v not in out:
            out.append(v)
    return out


def norm_title(v: str) -> str:
    v = unicodedata.normalize("NFKD", v or "").encode("ascii", "ignore").decode().lower()
    v = re.sub(r"\s*[:\-–—]\s+.*$", "", v)  # subtitle-insensitive
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", v)).strip()


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return s[:60] or "untitled"


def pdf_text(path: Path, pages: int = 3) -> str:
    try:
        p = subprocess.run(
            ["pdftotext", "-q", "-l", str(pages), str(path), "-"],
            capture_output=True, timeout=60,
        )
        return p.stdout.decode("utf-8", "ignore")
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def load_corpus() -> tuple[dict[str, dict], dict[str, dict]]:
    by_doi: dict[str, dict] = {}
    by_title: dict[str, dict] = {}
    for f in CORPUS:
        if not f.exists():
            continue
        for rec in json.load(open(f)):
            for v in doi_variants(rec.get("doi") or ""):
                by_doi.setdefault(v, rec)
            t = norm_title(rec.get("title") or "")
            if t:
                by_title.setdefault(t, rec)
    return by_doi, by_title


def identify(path: Path, by_doi: dict, by_title: dict) -> tuple[dict | None, str]:
    text = pdf_text(path)
    if not text.strip():
        return None, "no_extractable_text"
    for raw in DOI_RE.findall(text)[:60]:
        for v in doi_variants(raw):
            if v in by_doi:
                return by_doi[v], f"doi:{v}"
    head = norm_title(" ".join(text.split()[:60]))
    for t, rec in by_title.items():
        if len(t) > 25 and t in head:
            return rec, "title_match"
    return None, "unidentified"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="directory of hand-retrieved PDFs")
    ap.add_argument("--apply", action="store_true", help="perform the copies")
    args = ap.parse_args()

    src = Path(args.source).expanduser()
    if not src.is_dir():
        raise SystemExit(f"source not a directory: {src}")
    PDFDIR.mkdir(parents=True, exist_ok=True)
    by_doi, by_title = load_corpus()

    ingested, already, unknown = [], [], []
    for f in sorted(src.glob("*.pdf")):
        if WNAME_RE.match(f.name):
            already.append((f, "already in convention"))
            continue
        rec, how = identify(f, by_doi, by_title)
        if not rec:
            unknown.append((f, how, " ".join(pdf_text(f, 1).split())[:180]))
            continue
        dest = PDFDIR / f"{rec['paperId']}__{slugify(rec.get('title',''))}.pdf"
        if dest.exists():
            already.append((f, f"target exists: {dest.name}"))
            continue
        if args.apply:
            shutil.copy2(f, dest)
        ingested.append((f, rec, how, dest, " ".join(pdf_text(f, 1).split())[:200]))

    mode = "APPLIED" if args.apply else "DRY RUN (pass --apply to copy)"
    lines = [f"# PDF ingest report — {SLUG}", "",
             f"Source: `{src}` — {mode}", "",
             f"Identified and copied: {len(ingested)} · already present: {len(already)} · "
             f"unidentified: {len(unknown)}", ""]

    if ingested:
        lines += ["## Identified", "",
                  "| Source file | Matched by | work_id | Title |", "|---|---|---|---|"]
        for f, rec, how, dest, _ in ingested:
            lines.append(f"| `{f.name[:52]}` | {how} | {rec['paperId']} | "
                         f"{(rec.get('title') or '')[:70]} |")
        lines.append("")
        # Page-1 head for every match, so a mis-identification is visible in review
        # rather than buried under a confident-looking rename.
        lines += ["### Page-1 head of each identified file (verify the match)", ""]
        for f, rec, how, dest, head in ingested:
            lines += [f"- **{rec['paperId']}** ← `{f.name}` ({how})", f"  > {head}", ""]
    if unknown:
        lines += ["## Unidentified — needs a manual look", "",
                  "| File | Why | Page-1 head |", "|---|---|---|"]
        for f, how, head in unknown:
            lines.append(f"| `{f.name[:46]}` | {how} | {head[:100]} |")
        lines.append("")
    if already:
        lines += ["## Skipped", ""]
        for f, why in already:
            lines.append(f"- `{f.name[:60]}` — {why}")
        lines.append("")

    REPORT.write_text("\n".join(lines))
    print("\n".join(lines[:6]))
    for f, rec, how, dest, _ in ingested:
        print(f"  {'copied' if args.apply else 'would copy'}: {f.name[:44]} -> {dest.name}")
    for f, how, _ in unknown:
        print(f"  UNIDENTIFIED: {f.name[:60]} ({how})")
    print(f"report -> {REPORT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
