#!/usr/bin/env python3
"""264 — A.18: convert retrieved files to text and VERIFY each matches its record. TICK-076.

Three file kinds came back from five routes: BioC JSON (49), publisher/landing HTML
(114) and PDF (39). Extraction needs plain text, and it needs confidence that the
text under a record id is that record's paper.

**Verification is not optional.** The standing rule is to match a retrieved file to
its record by CONTENT, not by filename — a wrong pairing corrupts the extraction
table silently and is nearly impossible to find later. Every file is checked by
title-token overlap against the record's own title, and anything below the floor is
quarantined rather than extracted.

Two failure modes this catches, both seen already in this chapter:
  * an HTML "file" that is a bot-defence page or a JS shell returning 200 — real
    bytes, no paper;
  * an abstract-only landing page, which looks like a hit and cannot support
    extraction of an estimate.

Records are classified `FULL` (methods/results present), `ABSTRACT_ONLY`,
`WRONG_PAPER`, or `JUNK`. Only FULL goes forward to extraction; the rest go back to
the retrieval queue, because an abstract is not a full text and treating it as one
is how a study gets extracted from its own summary.

Usage: python3 source/build/goldset/264_a18_build_text_corpus.py
"""
import json
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
SRC = TEMP / "fulltext"
TXT = TEMP / "text"
OUT = LOGS / "heritability-fertility-genetic-corpus-log.json"

SECTION = re.compile(r"\b(methods?|materials and methods|results|analysis|"
                     r"statistical analys|discussion|supplementary)\b", re.I)


def fold(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def toks(s):
    return {t for t in fold(s).split() if len(t) > 3}


def html_to_text(p):
    """Keeps table cells as delimited text. The first version stripped all markup
    uniformly, so a <table> of heritability estimates collapsed into a run of bare
    numbers with no association to their row or column labels."""
    raw = p.read_bytes().decode("utf8", "ignore")
    raw = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", raw)
    # mark cell and row boundaries before the tags go
    raw = re.sub(r"(?i)</t[dh]>", " | ", raw)
    raw = re.sub(r"(?i)</tr>", " \n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = re.sub(r"&[a-z]+;", " ", raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    return re.sub(r"\n{3,}", "\n\n", raw).strip()


def bioc_to_text(p):
    try:
        d = json.loads(p.read_text())
    except Exception:
        return ""
    out = []
    docs = d if isinstance(d, list) else [d]
    for doc in docs:
        for d2 in (doc.get("documents") or []):
            for pas in (d2.get("passages") or []):
                t = pas.get("text")
                if t:
                    out.append(t)
    return "\n".join(out)


def pdf_to_text(p):
    """-layout preserves column structure. Without it pdftotext linearises tables and
    the estimates they hold -- which is where h2, SE and n usually live -- become
    unrecoverable word soup. Several 50-75k texts yielded no numeric estimate at all
    on the first pass for exactly this reason."""
    r = subprocess.run(["pdftotext", "-q", "-layout", "-enc", "UTF-8", str(p), "-"],
                       capture_output=True, text=True)
    out = r.stdout or ""
    if len(out) < 500:   # fall back if -layout produced nothing usable
        r = subprocess.run(["pdftotext", "-q", "-enc", "UTF-8", str(p), "-"],
                           capture_output=True, text=True)
        out = r.stdout or ""
    return out


def main():
    TXT.mkdir(parents=True, exist_ok=True)
    state = json.loads((LOGS / "heritability-fertility-genetic-retrieval-state.json").read_text())["state"]
    rows, kinds = [], Counter()
    # 265 rewrote the state vocabulary (RETRIEVED -> FULL_TEXT / ABSTRACT_ONLY /
    # BOT_CHALLENGE_PAGE). Keying on the old literal made this stage silently skip
    # every record and emit an empty corpus -- a pipeline that reports nothing rather
    # than failing. Drive off "has files" instead, which is what this stage actually
    # needs, and assert the corpus is non-empty before writing.
    PROCESS = {"RETRIEVED", "FULL_TEXT", "ABSTRACT_ONLY"}
    for oid, s in state.items():
        if s["status"] not in PROCESS and not list(SRC.glob(f"{oid}.*")):
            continue
        files = sorted(SRC.glob(f"{oid}.*"))
        best = None
        for f in files:
            # SNIFF, do not trust the extension. 260 named files by whether the URL
            # ended in ".pdf", so publisher PDFs served from extensionless URLs were
            # written as .html and then run through the tag stripper, turning real
            # full texts into binary garbage that scored 0.00 title overlap and was
            # classified WRONG_PAPER. Four studies were lost that way, one of them in
            # the already-thin H2_MODERATION arm.
            magic = f.read_bytes()[:5]
            if magic[:4] == b"%PDF":
                t = pdf_to_text(f)
            elif f.suffix == ".json":
                t = bioc_to_text(f)
            elif f.suffix == ".pdf":
                t = pdf_to_text(f)
            else:
                t = html_to_text(f)
            if best is None or len(t) > len(best[1]):
                best = (f, t)
        if best is None:
            rows.append({"openalex": oid, "cell": s["cell"], "verdict": "NO_FILE"})
            kinds["NO_FILE"] += 1
            continue
        f, text = best
        title_t = toks(s.get("title"))
        head = toks(text[:6000])
        overlap = (len(title_t & head) / len(title_t)) if title_t else 0.0
        if overlap < 0.4 and title_t:
            # a cover page, a running header, or a journal front matter can push the
            # title past the window; check the whole document before calling it wrong
            overlap = max(overlap, len(title_t & toks(text)) / len(title_t))
        nsec = len(set(m.group(0).lower() for m in SECTION.finditer(text)))
        if len(text) < 1500:
            v = "JUNK"
        elif overlap < 0.4:
            v = "WRONG_PAPER"
        elif len(text) < 12000 or nsec < 2:
            v = "ABSTRACT_ONLY"
        else:
            v = "FULL"
        kinds[v] += 1
        if v == "FULL":
            (TXT / f"{oid}.txt").write_text(text)
        rows.append({"openalex": oid, "cell": s["cell"], "title": s.get("title"),
                     "file": f.name, "chars": len(text),
                     "title_overlap": round(overlap, 2), "sections": nsec, "verdict": v})

    assert rows, ("no files processed -- check that the retrieval state's status "
                  "vocabulary still matches what this stage expects")
    bycell = Counter((r["cell"], r["verdict"]) for r in rows)
    cells = sorted({r["cell"] for r in rows})
    print("verdicts:", dict(kinds))
    print(f"\n{'cell':26s} {'FULL':>5s} {'ABS':>5s} {'WRONG':>6s} {'JUNK':>5s}")
    for c in cells:
        print(f"{c:26s} {bycell[(c,'FULL')]:5d} {bycell[(c,'ABSTRACT_ONLY')]:5d} "
              f"{bycell[(c,'WRONG_PAPER')]:6d} {bycell[(c,'JUNK')]:5d}")
    OUT.write_text(json.dumps({"summary": {"verdicts": dict(kinds),
                                           "by_cell": {f"{c}|{v}": n for (c, v), n in bycell.items()},
                                           "note": "Only FULL proceeds to extraction. ABSTRACT_ONLY "
                                                   "and WRONG_PAPER return to the retrieval queue: an "
                                                   "abstract is not a full text."},
                              "records": rows}, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}; text corpus in {TXT}")


if __name__ == "__main__":
    main()
