#!/usr/bin/env python3
"""
195_a17_fulltext_prep.py — A.17, stage 6 prep. Extract text and build the full-text screen records.

**THIS RUNS ON 33 OF 131 WANTED RECORDS AND THE OUTPUT SAYS SO ON EVERY PAGE.** 67 more are
blocked-but-open (a browser, no institutional access) and 31 need a proxy. The prep is written to be
RE-RUN when those arrive: everything is keyed on the OpenAlex id, extraction is skipped for text
already on disk, and no downstream file is overwritten in place with a partial answer. A provisional
pass that cannot be cheaply redone becomes the final answer by default, which is how a partial
retrieval turns into a partial chapter without anyone deciding that it should.

WHAT THE FULL TEXT IS BEING ASKED, AND WHY IT IS NOT "IS THIS RELEVANT". The title/abstract screen
already settled relevance. Full text exists here to answer the three questions the abstract could
not, and each one is a field rather than a judgement:

  1. `arm_resolved` — the routing the D2 screen left at `cannot_tell` for 14.4% of records. Does the
     paper ESTIMATE a response to an access change, or COUNT/PROJECT ART births? This is decided in
     the methods section, which is exactly why it needed full text.

  2. `counterfactual_treatment` — **the field this chapter exists to fill.** For every arm-1 record:
     does the paper state what would have happened WITHOUT ART, and if so, how? The options are not
     good-or-bad but structural: `none_stated` (the share is presented as the effect),
     `assumed_zero` (explicitly assumes ART births are all additional), `partial` (adjusts for
     something — dropout, spontaneous conception, selection), or `estimated` (a counterfactual is
     actually estimated). The DISTRIBUTION of this field across arm 1 is the chapter's central
     result, and it is a property of the literature rather than an opinion about it.

  3. `reported_quantity` — the number the paper actually reports, verbatim, with its units and
     denominator. Extraction cannot start from a remembered magnitude, and A.12's identity arm
     showed what happens when a chapter carries a number whose denominator nobody checked.

EXTRACTION QUALITY IS MEASURED, NOT ASSUMED. `pdftotext -layout` is tried first and pypdf second, and
the character count per page is recorded. **A PDF that yields under ~200 characters per page is a
scan, not a text layer**, and screening it from extracted text would silently produce a "nothing
found" verdict on a paper that says plenty. Those records are flagged `NEEDS_OCR` and excluded from
the screen rather than screened badly — the same reason a failed request is bucketed apart from a
zero result everywhere else in this pipeline.

Output: extraction/{slug}-fulltext/{WID}.txt        (gitignored with the PDFs)
        literature/search-logs/{slug}-fulltext-prep.md
        extraction/{slug}-fulltext-worklist.json
"""
import csv, json, os, re, subprocess, sys
from collections import Counter

SLUG = "art-access-fertility-recovery"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
TXT_DIR = os.path.join(EXTRACT, f"{SLUG}-fulltext")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-fulltext-prep.md")
OUT_WORK = os.path.join(EXTRACT, f"{SLUG}-fulltext-worklist.json")

MIN_CHARS_PER_PAGE = 200

# Probes. Each is a REGEX whose hits are carried into the screening record as located excerpts, so
# the screener reads the paper's own sentences rather than searching from scratch. They are a
# reading aid and NEVER a verdict: absence of a hit is not evidence of absence in the paper.
PROBES = {
    "counterfactual": re.compile(
        r"(?:would (?:not )?have (?:been|occurred|happened)|counterfactual|absent ART|without ART"
        r"|without treatment|in the absence of|spontaneous(?:ly)? concei|natural concei"
        r"|untreated|drop(?:ped)?[- ]out|discontinu|attributable to ART|additional births"
        r"|but for)", re.I),
    "identification": re.compile(
        r"(?:difference[- ]in[- ]difference|natural experiment|instrument(?:al|ed|s)?\b"
        r"|regression discontinuity|event[- ]study|exogenous|control group|parallel trends"
        r"|staggered|placebo test|first[- ]stage)", re.I),
    "quantity": re.compile(
        r"(?:\d+(?:\.\d+)?\s?%[^.]{0,80}(?:of (?:all )?(?:live )?births|of the TFR|of total fertility"
        r"|contribution)|contributed?\s+\d+(?:\.\d+)?|accounted for\s+\d+(?:\.\d+)?"
        r"|increase[d]?\s+(?:the\s+)?(?:TFR|total fertility|birth rate)s?\s+by)", re.I),
    "denominator": re.compile(
        r"(?:per 1,?000 women|per 1,?000 births|of all live births|of all births|live births per"
        r"|denominator|age[- ]specific|total fertility rate)", re.I),
}


def extract(pdf, dest):
    """(chars, pages, tool). pdftotext -layout first; pypdf second. Both are tried before a record
    is called unreadable, because 'no text' from one library is not 'no text'."""
    txt = ""
    tool = ""
    try:
        r = subprocess.run(["pdftotext", "-layout", "-q", pdf, "-"], capture_output=True, text=True,
                           timeout=180)
        if r.returncode == 0 and r.stdout:
            txt, tool = r.stdout, "pdftotext"
    except Exception:
        pass
    if len(txt.strip()) < 400:
        try:
            import pypdf
            rd = pypdf.PdfReader(pdf)
            t2 = "\n".join((p.extract_text() or "") for p in rd.pages)
            if len(t2.strip()) > len(txt.strip()):
                txt, tool = t2, "pypdf"
        except Exception:
            pass
    pages = 0
    try:
        import pypdf
        pages = len(pypdf.PdfReader(pdf).pages)
    except Exception:
        pages = txt.count("\f") + 1
    if txt.strip():
        open(dest, "w", encoding="utf-8", errors="replace").write(txt)
    return len(txt.strip()), max(pages, 1), tool or "none"


def excerpts(txt, rx, n=3, width=260):
    out = []
    for m in rx.finditer(txt):
        s = max(0, m.start() - width // 2)
        frag = re.sub(r"\s+", " ", txt[s:s + width]).strip()
        out.append(frag)
        if len(out) >= n:
            break
    return out


def main():
    os.makedirs(TXT_DIR, exist_ok=True)
    oa = {r["id"]: r for r in json.load(open(OA))}
    screened = {m["id"]: m for m in json.load(open(SCREENED))}
    fetch = {r["id"]: r for r in csv.DictReader(open(os.path.join(
        LOGS, f"{SLUG}-fetch-log.csv")))}

    pdfs = {}
    for f in sorted(os.listdir(PDF_DIR)):
        if f.endswith(".pdf"):
            pdfs[f.split("__")[0]] = os.path.join(PDF_DIR, f)

    work, rows = [], []
    for wid, path in pdfs.items():
        dest = os.path.join(TXT_DIR, f"{wid}.txt")
        if os.path.exists(dest) and os.path.getsize(dest) > 400:
            txt = open(dest, encoding="utf-8", errors="replace").read()
            chars, tool = len(txt.strip()), "cached"
            try:
                import pypdf
                pages = len(pypdf.PdfReader(path).pages)
            except Exception:
                pages = txt.count("\f") + 1
        else:
            chars, pages, tool = extract(path, dest)
            txt = open(dest, encoding="utf-8", errors="replace").read() if chars else ""
        cpp = chars / max(pages, 1)
        readable = cpp >= MIN_CHARS_PER_PAGE
        m = oa.get(wid, {})
        s = screened.get(wid, {})
        rows.append(dict(id=wid, job=fetch.get(wid, {}).get("job", "?"), chars=chars, pages=pages,
                         cpp=round(cpp), tool=tool, readable=readable,
                         title=(m.get("title") or s.get("title") or "")[:90]))
        if not readable:
            continue
        work.append(dict(
            id=wid, job=fetch.get(wid, {}).get("job", "?"), title=m.get("title") or s.get("title"),
            year=m.get("year"), venue=m.get("venue"), doi=m.get("doi"),
            screen_cell=s.get("screen_cell"), screen_arm=s.get("screen_arm"),
            screen_note=s.get("screen_note"),
            pages=pages, chars=chars,
            probe_counterfactual=excerpts(txt, PROBES["counterfactual"]),
            probe_identification=excerpts(txt, PROBES["identification"]),
            probe_quantity=excerpts(txt, PROBES["quantity"]),
            probe_denominator=excerpts(txt, PROBES["denominator"], n=2)))
    json.dump(work, open(OUT_WORK, "w"), indent=2)

    n_pdf, n_read = len(rows), sum(1 for r in rows if r["readable"])
    wanted = len(oa)
    byjob = Counter(r["job"] for r in rows if r["readable"])
    pc = lambda a, b: f"{a / max(b, 1):.0%}"
    L = [f"# Stage 6 prep — full-text extraction — {SLUG} (A.17)", "",
         f"> **PROVISIONAL. This runs on {n_pdf} of {wanted} wanted records ({pc(n_pdf, wanted)}).** "
         f"67 more are blocked-but-open (a browser, no institutional access) and 31 need a proxy. "
         f"**Job A1 — the counterfactual set the chapter's headline number is conditional on — is "
         f"{byjob.get('A1_COUNTERFACTUAL', 0)} of 14 in hand.** Every downstream file is keyed on the "
         "OpenAlex id and skips work already done, so this re-runs cheaply when the rest arrive. A "
         "provisional pass that cannot be cheaply redone becomes the final answer by default.", "",
         f"**{n_read} of {n_pdf} PDFs yielded a usable text layer.**", "",
         "## Extraction quality, measured", "",
         f"A PDF yielding under {MIN_CHARS_PER_PAGE} characters per page is a SCAN, not a text "
         "layer. Screening one from extracted text produces a confident 'nothing found' on a paper "
         "that says plenty, so those records are flagged `NEEDS_OCR` and excluded from the screen "
         "rather than screened badly.", "",
         "| id | job | pages | chars | chars/page | tool | readable |",
         "|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: x["cpp"]):
        L.append(f"| `{r['id']}` | {r['job'].split('_')[0]} | {r['pages']} | {r['chars']:,} | "
                 f"{r['cpp']:,} | {r['tool']} | {'yes' if r['readable'] else '**NEEDS_OCR**'} |")
    L += ["", "## Readable records by job", "", "| job | readable |", "|---|---|"]
    for j, k in sorted(byjob.items()):
        L.append(f"| `{j}` | {k} |")
    L += ["", "## What the full-text screen is being asked", "",
          "Relevance was settled at title/abstract. Full text exists to answer three things the "
          "abstract could not, each recorded as a field:", "",
          "1. **`arm_resolved`** — the routing D2 left at `cannot_tell` for 14.4% of records. "
          "Decided in the methods section, which is why it needed full text.",
          "2. **`counterfactual_treatment`** — *the field this chapter exists to fill.* For every "
          "arm-1 record: `none_stated` / `assumed_zero` / `partial` / `estimated`. The DISTRIBUTION "
          "of this field across arm 1 is the chapter's central result, and it is a property of the "
          "literature rather than an opinion about it.",
          "3. **`reported_quantity`** — the number the paper reports, verbatim, with units and "
          "denominator. A.12 showed what happens when a chapter carries a number whose denominator "
          "nobody checked.", "",
          "Each worklist record carries located excerpts for four probes — counterfactual language, "
          "identification language, a reported quantity, and a denominator — so the screener reads "
          "the paper's own sentences instead of searching from scratch. **The probes are a reading "
          "aid and never a verdict: a probe returning nothing is not evidence that the paper says "
          "nothing.**", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"pdfs={n_pdf} readable={n_read} worklist={len(work)}")
    print("by job:", dict(byjob))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
