#!/usr/bin/env python3
"""84_c2c_ingest_pdfs.py — C.2.c (TICK-056). Identify and rename hand-retrieved PDFs.

The C.2.c analogue of 83_d3b_ingest_pdfs.py. A human retrieves the closed and bot-blocked PDFs via
Zotero + the UChicago proxy, in whatever filenames the browser produced. This script identifies each
file from its OWN contents -- the DOI printed in the text first, a subtitle-insensitive title match as
fallback -- and renames matches to the pipeline's `W<OpenAlexID>__<slug>.pdf` convention, which the
retrieval log and the extraction tables key on.

No filename discipline is required of the retriever. Nothing is deleted. Renames are DRY-RUN by
default; pass --apply. Files already in the W<id>__ convention are left alone.

The identity map is the full gated set, not just the priority 11, so a PDF that turns out to be an
associational-stratum paper is still identified rather than reported as unknown.

  python3 source/build/goldset/84_c2c_ingest_pdfs.py --source ~/Downloads/c2c           # dry run
  python3 source/build/goldset/84_c2c_ingest_pdfs.py --source ~/Downloads/c2c --apply

Writes a reconciliation report to stdout and to extraction/housing-costs-pdf-ingest-report.md,
and updates housing-costs-pdf-retrieval-log.csv so the log and the directory cannot drift.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import unicodedata

SLUG = "housing-costs"
GATE = "extraction/housing-costs-ra-gate.csv"
LOG = f"extraction/{SLUG}-pdf-retrieval-log.csv"
PDFDIR = f"literature/pdfs/{SLUG}"
REPORT = f"extraction/{SLUG}-pdf-ingest-report.md"


LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
             "¤": "ff", "­": ""}


def norm(t: str) -> str:
    """Normalise for matching.

    pdftotext mangles ligatures in LaTeX-set papers -- economics working papers routinely come out
    with 'e¤ect' for 'effect', 'bene…t' for 'benefit'. Exact title matching can never work against
    that, which is why matching below is containment-scored on tokens rather than substring.
    """
    t = (t or "")
    for k, v in LIGATURES.items():
        t = t.replace(k, v)
    t = unicodedata.normalize("NFKD", t.lower())
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


STOP = {"the", "a", "an", "of", "on", "in", "and", "for", "to", "from", "evidence", "study",
        "analysis", "effects", "effect", "impact", "case"}


def toks(t: str) -> set:
    return {w for w in norm(t).split() if len(w) > 2 and w not in STOP}


def best_title_match(head: str, gate: dict):
    """Containment of the title's distinctive tokens in the PDF head text.

    Returns (work_id, score) for the best candidate. Requires a clear margin over the runner-up so a
    generic title cannot win on ambient vocabulary -- the same concern GACS §5 raises about naive
    word-overlap on a topic-homogeneous corpus.
    """
    h = toks(head)
    if not h:
        return None, 0.0
    scored = []
    for wid, r in gate.items():
        tt = toks(r["title"])
        if len(tt) < 3:
            continue
        scored.append((len(tt & h) / len(tt), wid))
    if not scored:
        return None, 0.0
    scored.sort(reverse=True)
    top, runner = scored[0], (scored[1] if len(scored) > 1 else (0.0, None))
    if top[0] >= 0.70 and (top[0] - runner[0]) >= 0.10:
        return top[1], top[0]
    return None, top[0]


def title_slug(t: str) -> str:
    t = re.sub(r"<[^>]+>", "", t or "").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60].rstrip("-")


def head_text(path: str, pages: int = 2) -> str:
    try:
        p = subprocess.run(["pdftotext", "-q", "-l", str(pages), path, "-"],
                           capture_output=True, text=True, timeout=60)
        return p.stdout or ""
    except Exception:
        pass
    try:                                      # fallback if poppler is absent
        from pypdf import PdfReader
        r = PdfReader(path)
        return "\n".join((r.pages[i].extract_text() or "") for i in range(min(pages, len(r.pages))))
    except Exception:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="folder of hand-retrieved PDFs")
    ap.add_argument("--apply", action="store_true", help="perform the copies (default: dry run)")
    args = ap.parse_args()

    gate = {r["openalex"]: r for r in csv.DictReader(open(GATE)) if r["ra_verdict"].startswith("KEEP")}
    by_doi = {r["doi"].lower(): wid for wid, r in gate.items() if r["doi"]}

    os.makedirs(PDFDIR, exist_ok=True)
    present = {f.split("__")[0] for f in os.listdir(PDFDIR) if f.startswith("W")}

    identified, skipped, unknown = [], [], []
    for fn in sorted(os.listdir(args.source)):
        if not fn.lower().endswith(".pdf"):
            continue
        src = os.path.join(args.source, fn)
        if re.match(r"^W\d+__", fn):
            skipped.append((fn, "already in convention"))
            continue
        txt = head_text(src)
        wid, how = None, ""
        for cand in re.findall(r"\b10\.\d{4,9}/[^\s\"'<>,;)\]]+", txt)[:15]:
            c = cand.rstrip(".,;").lower()
            if c in by_doi:
                wid, how = by_doi[c], f"doi:{c}"
                break
        if not wid:
            cand_wid, score = best_title_match(txt[:2000], gate)
            if cand_wid:
                wid, how = cand_wid, f"title~{score:.2f}"
        if not wid:
            unknown.append((fn, (txt[:100] or "").replace("\n", " ")))
            continue
        if wid in present:
            skipped.append((fn, f"target exists for {wid}"))
            continue
        dest = os.path.join(PDFDIR, f"{wid}__{title_slug(gate[wid]['title'])}.pdf")
        identified.append((fn, how, wid, gate[wid]["title"], dest, (txt[:110] or "").replace("\n", " ")))
        if args.apply:
            shutil.copy2(src, dest)
            present.add(wid)

    if args.apply and identified:
        rows = list(csv.DictReader(open(LOG)))
        done = {wid for _, _, wid, _, _, _ in identified}
        for r in rows:
            if r["work_id"] in done:
                dest = [d for _, _, w, _, d, _ in identified if w == r["work_id"]][0]
                r.update({"download_status": "ok", "detail": "hand_retrieved_zotero",
                          "bytes": os.path.getsize(dest), "file": os.path.basename(dest),
                          "version": r.get("version") or "published"})
        with open(LOG, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    out = [f"# PDF ingest report — {SLUG}\n",
           f"Source: `{args.source}` — {'APPLIED' if args.apply else 'DRY RUN'}\n",
           f"Identified: {len(identified)} · skipped: {len(skipped)} · unidentified: {len(unknown)}\n",
           "## Identified\n", "| Source file | Matched by | work_id | Title |", "|---|---|---|---|"]
    for fn, how, wid, title, _, _ in identified:
        out.append(f"| `{fn[:52]}` | {how} | {wid} | {title[:66]} |")
    out.append("\n### Page-1 head of each identified file (verify the match)\n")
    for fn, how, wid, _, _, head in identified:
        out.append(f"- **{wid}** ← `{fn[:60]}` ({how})\n  > {head}\n")
    if skipped:
        out.append("## Skipped\n")
        out += [f"- `{fn}` — {why}" for fn, why in skipped]
    if unknown:
        out.append("\n## Unidentified — needs a human look\n")
        out += [f"- `{fn}`\n  > {head}" for fn, head in unknown]
    text = "\n".join(out) + "\n"
    open(REPORT, "w").write(text)
    print(text)
    if not args.apply:
        print("DRY RUN — nothing copied. Re-run with --apply once the matches above look right.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
