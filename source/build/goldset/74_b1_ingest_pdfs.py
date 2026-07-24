#!/usr/bin/env python3
"""
74_b1_ingest_pdfs.py — B.1 (TICK-032/033). Identify and rename batch-installed PDFs.

The RA batch-installs PDFs into literature/pdfs/{slug}/ under whatever names their retrieval tool
produced (Zotero author-year, numeric dumps, etc.). This script identifies each one from its OWN
contents — DOI printed on / embedded in the PDF first, title-fuzzy-match as fallback — reconciles it
against the missing-DOI target list, and renames matches to the pipeline's `W<OpenAlexID>__<slug>.pdf`
convention so the effects table (which keys on the OpenAlex study_id) can locate them.

No filename discipline is required of the RA. Nothing is deleted. Renames are DRY-RUN by default; pass
--apply to perform them. Files already in the W<id>__ convention are left untouched.

Identity map: literature-native corpus records (paperId + doi + title) from the screen outputs.
Target set : extraction/{slug}-missing-pdf-dois.txt (the 71 DOIs still to retrieve).

Outputs a reconciliation report to stdout AND to extraction/{slug}-pdf-ingest-report.md:
  - newly identified + (renamed | would-rename)
  - already in W<id> convention (present)
  - PDFs that could NOT be identified (shown with page-1 text head for a manual confirm)
  - target DOIs still missing (of the 71)
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PDFDIR = REPO / "literature" / "pdfs" / SLUG
EXTR = REPO / "extraction"
CORPUS = [REPO / "output" / f"{SLUG}-estimand-ready-set.json",
          REPO / "output" / f"{SLUG}-theory-stream.json"]
TARGETS = EXTR / f"{SLUG}-missing-pdf-dois.txt"

DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', re.I)
SSRN_RE = re.compile(r'ssrn[.\s/=_-]*(?:com/abstract=)?(\d{6,8})', re.I)
WNAME_RE = re.compile(r'^W\d+__')


def norm_doi(d):
    return (d or "").strip().lower().replace("https://doi.org/", "").rstrip(".").rstrip(")")


def doi_variants(raw):
    """A page-scraped DOI often carries trailing junk ('...980896doi:', '...v4', a stray ')'). Yield the
    raw form plus progressively trimmed variants so an exact map hit can still be found."""
    d = norm_doi(raw)
    seen = []
    for v in (d, re.sub(r'doi:?$', '', d), re.sub(r'v\d+$', '', d), d.rstrip(".,;:)]}-_")):
        v = v.rstrip(".,;:)]}-_")
        if v and v not in seen:
            seen.append(v)
    return seen


def norm_title(v):
    v = unicodedata.normalize("NFKD", v or "").encode("ascii", "ignore").decode().lower()
    v = re.sub(r"\s*[:\-–—]\s+.*$", "", v)          # subtitle-insensitive
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", v)).strip()


def title_sim(a, b):
    aa, bb = set(norm_title(a).split()), set(norm_title(b).split())
    return len(aa & bb) / len(aa | bb) if aa and bb else 0.0


def slug_title(t, n=58):
    s = re.sub(r"[^a-z0-9]+", "-", norm_title(t)).strip("-")
    return (s[:n].rstrip("-")) or "untitled"


def read_pdf(path, npages=2):
    """Return (embedded+page-text blob, page-1 head) using pypdf."""
    try:
        from pypdf import PdfReader
        r = PdfReader(str(path))
        meta = " ".join(str(v) for v in (r.metadata or {}).values())
        ptext = " ".join((r.pages[i].extract_text() or "") for i in range(min(npages, len(r.pages))))
        head = (r.pages[0].extract_text() or "")[:400] if r.pages else ""
        return meta + " " + ptext, head
    except Exception as e:
        return "", f"(unreadable: {e})"


def load_map():
    by_doi, by_title = {}, {}
    for f in CORPUS:
        if not f.exists():
            continue
        for rec in json.loads(f.read_text()):
            pid, doi, title = rec.get("paperId"), norm_doi(rec.get("doi")), rec.get("title") or ""
            if not pid:
                continue
            if doi:
                by_doi.setdefault(doi, {"paperId": pid, "title": title})
            if title:
                by_title.setdefault(norm_title(title), {"paperId": pid, "doi": doi, "title": title})
    return by_doi, by_title


def identify(blob, by_doi, by_title):
    # 1) DOI on/in the PDF that matches a known corpus DOI -> authoritative. Each scraped DOI is tried
    #    in raw + trimmed variants (trailing 'doi:', version suffix, stray punctuation).
    found = []
    for raw in DOI_RE.findall(blob):
        for v in doi_variants(raw):
            found.append(v)
            if v in by_doi:
                return by_doi[v]["paperId"], by_doi[v]["title"], v, "doi"
    # 2) SSRN working papers print 'ssrn.com/abstract=<id>', not a 10.x DOI -> reconstruct 10.2139/ssrn.<id>.
    for m in SSRN_RE.findall(blob):
        cand = f"10.2139/ssrn.{m}"
        found.append(cand)
        if cand in by_doi:
            return by_doi[cand]["paperId"], by_doi[cand]["title"], cand, "ssrn-id"
    # 3) Title fuzzy-match against the corpus (for DOI-less scans / working papers). Scan a wider window
    #    than the head so publisher boilerplate ('Electronic copy available at...') doesn't starve it.
    best, bestrec = 0.0, None
    for tkey, rec in by_title.items():
        s = title_sim(blob[:1400], rec["title"])
        if s > best:
            best, bestrec = s, rec
    if bestrec and best >= 0.60:
        return bestrec["paperId"], bestrec["title"], bestrec.get("doi"), f"title({best:.2f})"
    # 4) A DOI was printed but is not in our corpus map (still useful to report).
    return None, None, (found[0] if found else None), "unmatched"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="perform renames (default: dry-run)")
    args = ap.parse_args()

    if not PDFDIR.exists():
        sys.exit(f"PDF dir missing: {PDFDIR}")
    by_doi, by_title = load_map()
    targets = {norm_doi(l) for l in TARGETS.read_text().splitlines()
               if l.strip() and not l.startswith("#")} if TARGETS.exists() else set()

    present_wids = {p.name.split("__")[0] for p in PDFDIR.glob("*.pdf") if WNAME_RE.match(p.name)}
    newly, unmatched, dups, taken, batch_wids = [], [], [], set(), set()
    for pdf in sorted(PDFDIR.glob("*.pdf")):
        if WNAME_RE.match(pdf.name):                 # already in convention -> counted above
            continue
        blob, head = read_pdf(pdf)
        pid, title, doi, how = identify(blob, by_doi, by_title)
        if not pid:
            unmatched.append((pdf.name, doi, re.sub(r"\s+", " ", head)[:140]))
            continue
        # A paper already present (W-named) or already matched earlier this batch = a duplicate copy.
        if pid in present_wids or pid in batch_wids:
            dups.append((pdf.name, pid, doi))
            continue
        batch_wids.add(pid)
        newname = f"{pid}__{slug_title(title)}.pdf"
        newly.append((pdf.name, newname, pid, doi, how, doi in targets if doi else False))
        if args.apply:
            dest = PDFDIR / newname
            if dest.exists() or newname in taken:
                dest = PDFDIR / f"{pid}__{slug_title(title)}-dup.pdf"
            pdf.rename(dest); taken.add(dest.name)

    # target DOIs now present = target ∩ (already-W-named corpus dois ∪ newly-matched dois)
    wid_to_doi = {v["paperId"]: k for k, v in by_doi.items()}
    have = {wid_to_doi.get(w) for w in present_wids} | {n[3] for n in newly if n[3]}
    still_missing = sorted(targets - {norm_doi(d) for d in have if d})

    R = [f"# B.1 PDF ingest reconciliation ({'APPLIED' if args.apply else 'DRY-RUN'})", "",
         f"- already in W<id>__ convention: **{len(present_wids)}**",
         f"- newly identified this pass: **{len(newly)}**  ({sum(1 for n in newly if n[5])} of them on the target list)",
         f"- duplicate copies (paper already present / earlier in batch): **{len(dups)}**",
         f"- could NOT identify: **{len(unmatched)}**",
         f"- target DOIs still missing (of {len(targets)}): **{len(still_missing)}**", ""]
    if newly:
        R += ["## Newly identified", "", "| old name | -> | W-id | via | on target list |", "|---|---|---|---|---|"]
        R += [f"| {o[:40]} | {nn[:46]} | {pid} | {how} | {'yes' if tgt else 'no'} |"
              for (o, nn, pid, doi, how, tgt) in newly]
    if dups:
        R += ["", "## Duplicate copies (not renamed; safe to delete)", ""]
        R += [f"- `{n}` -> {pid} (already present)" for (n, pid, doi) in dups]
    if unmatched:
        R += ["", "## Could NOT identify (manual confirm — I'll show you page 1)", ""]
        R += [f"- `{n}`  doi_seen={d or '(none)'}  head: {h}" for (n, d, h) in unmatched]
    if still_missing:
        R += ["", "## Target DOIs still missing", ""] + [f"- {d}" for d in still_missing]
    report = "\n".join(R) + "\n"
    (EXTR / f"{SLUG}-pdf-ingest-report.md").write_text(report)
    print(report)
    print(f"[{'applied' if args.apply else 'dry-run — re-run with --apply to rename'}] "
          f"present={len(present_wids)} new={len(newly)} unmatched={len(unmatched)} "
          f"still_missing={len(still_missing)}", file=sys.stderr)


if __name__ == "__main__":
    main()
