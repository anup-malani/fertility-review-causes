#!/usr/bin/env python3
"""315 — install hand-retrieved PDFs, matching by CONTENT not by filename. TICK-078.

Hand-retrieved PDFs arrive publisher-named: `2061498.pdf`, `sdarticle.pdf`, `download`. Installing
them by filename order, or by trusting whatever the downloader called them, silently pairs a record
with the wrong document — and nothing downstream catches it, because every later stage reads the
extraction table rather than the PDF (`handoff-file-match-by-content`).

So each file is opened, its text extracted, and scored against the TITLE of every outstanding record.
A file installs only if it matches one record clearly and beats the runner-up by a margin. Anything
ambiguous is left in the inbox and reported.

There is no pdftotext, pypdf or mutool on this machine, so the extractor is written here: PDF content
streams are FlateDecode-compressed, which zlib handles, and the text operands sit in parentheses
before Tj/TJ. That is crude and would be wrong for a typesetting job, but it is more than enough to
decide which of 131 titles a document is.

THE EXTRACTOR IS VALIDATED BEFORE IT IS TRUSTED. `--selftest` runs it against the PDFs already
retrieved automatically, whose record pairing is known from the retrieval state, and reports how many
it re-identifies. A matcher that cannot recover a known-correct pairing must not be used to create
new ones (`validate-a-null-detector-on-positives`).

Usage:
  python3 source/build/goldset/315_c6a_install_handoff.py --selftest
  python3 source/build/goldset/315_c6a_install_handoff.py [--inbox DIR] [--apply]
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
DEST = ROOT / "temp" / "c6a-fulltext"
INBOX = ROOT / "temp" / "c6a-inbox"

STOP = {"the", "a", "an", "of", "and", "in", "on", "to", "for", "is", "are", "at", "by", "with",
        "from", "as", "its", "it", "this", "that", "some", "into", "during"}


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def toks(s):
    return [t for t in fold(s).split() if len(t) > 2 and t not in STOP]


JXA = """
function run(argv){
  ObjC.import("Quartz");
  const u = $.NSURL.fileURLWithPath(argv[0]);
  const d = $.PDFDocument.alloc.initWithURL(u);
  if (!d.js) return "";
  const s = ObjC.unwrap(d.string);
  return s ? s.substring(0, 40000) : "";
}
"""


def pdf_text(path):
    """macOS PDFKit via JXA. No install, and it reads what a person would see.

    The first version of this script hand-rolled a FlateDecode + Tj/TJ extractor because no
    pdftotext, pypdf or mutool is on this machine. Its selftest scored 2/25 -- it returned nothing
    at all for several files and garbage for others. The selftest is the only reason that never
    reached a real install."""
    r = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, str(path)],
                       capture_output=True, text=True, timeout=120)
    # RAW, not folded. fold() turns "10.1111/j.1728-4457..." into spaces, so folding here silently
    # killed the DOI matcher -- the strongest signal in this script -- while the title heuristics
    # carried on and made the selftest look fine. An upstream normalisation destroying a downstream
    # key is the same shape as `norm-strips-punctuation-dead-patterns`. Callers fold what they need.
    return r.stdout or ""


MIN_TITLE_TOKENS = 4


def longest_run(title_toks, text_toks):
    """Longest CONTIGUOUS run of the title's tokens inside the text's tokens."""
    if not title_toks:
        return 0
    pos = {}
    for i, w in enumerate(text_toks):
        pos.setdefault(w, []).append(i)
    best = 0
    for start in range(len(title_toks)):
        for i in pos.get(title_toks[start], ()):
            n = 0
            while (start + n < len(title_toks) and i + n < len(text_toks)
                   and title_toks[start + n] == text_toks[i + n]):
                n += 1
            best = max(best, n)
        if best == len(title_toks):
            break
    return best


def score(title, text_toks):
    """Longest contiguous title-token run, as a fraction of the title.

    The first scorer counted title tokens appearing ANYWHERE in 40,000 characters, and a reference
    list contains dozens of other papers' titles: a short generic title like "Did the Baby Boom
    Cause the US Divorce Boom" scored 1.00 against almost every fertility PDF in the set and won
    seven files that were not it. Requiring the tokens to appear CONSECUTIVELY, and near the front
    of the document where a title actually sits, is what separates the paper from its own
    bibliography."""
    tt = toks(title)
    if len(set(tt)) < MIN_TITLE_TOKENS:
        return -1.0
    return longest_run(tt, text_toks) / len(tt)


DOI_RE = re.compile(r"10\s?\.\s?\d{4,9}\s?/\s?[-._;()/:a-z0-9]+", re.I)


def dois_in(text):
    """DOIs printed in the document itself. Stronger than any title heuristic, and most journal
    PDFs carry theirs on page 1 -- I reached for title matching first and should have reached for
    this. Whitespace is stripped because PDF text extraction splits them across line breaks."""
    return {re.sub(r"\s+", "", d).lower().rstrip(".,;") for d in DOI_RE.findall(text)}


def load_records():
    st = json.loads((LOGS / "easterlin-relative-income-retrieval-state.json").read_text())["records"]
    rows = {r["openalex"]: r for r in
            csv.DictReader((ROOT / "extraction" / "easterlin-relative-income-screen.csv").open())}
    return st, rows


def selftest():
    st, _ = load_records()
    have = {o: v for o, v in st.items() if v["status"] == "have"}
    ok = amb = miss = 0
    titles = {o: v["title"] for o, v in st.items()}
    for oid, v in have.items():
        f = DEST / f"{oid}.pdf"
        if not f.exists():
            continue
        txt = pdf_text(f)
        if not txt:
            print(f"  NO TEXT   {v['title'][:58]}")
            miss += 1
            continue
        head = toks(" ".join(fold(txt).split()[:900]))   # tokenised AS THE TITLE IS
        found_dois = dois_in(txt[:20000])
        doi_hit = [o for o, v2 in st.items()
                   if v2.get("doi") and v2["doi"].lower() in found_dois]
        if len(doi_hit) == 1:
            if doi_hit[0] == oid:
                ok += 1
            else:
                miss += 1
                print(f"  WRONG (by DOI) {titles[doi_hit[0]][:40]!r} for {v['title'][:40]!r}")
            continue
        # A SHORT title contained inside a longer one scores 1.00 against the longer one's paper --
        # "Relative Cohort Size and Fertility" is a prefix of "...in Latin America and the
        # Caribbean" and won its PDF. `title-gate-cannot-refuse-short-superset`, in a scorer. When
        # scores tie, the LONGER title is the more specific evidence and wins.
        scored = sorted(((score(t, head), len(toks(t)), o) for o, t in titles.items()),
                        reverse=True)
        best, runner = (scored[0][0], scored[0][2]), (scored[1][0], scored[1][2])
        # A version twin is the SAME PAPER under a second record. No content matcher can separate
        # them and none should have to -- five of this chapter's anchors have twins, and the
        # citation split between them is what `citations-dont-follow-version-of-record` is about.
        # Counting a twin hit as a miss would have condemned a matcher that was working.
        a_, b_ = fold(titles[best[1]]).strip(), fold(v["title"]).strip()
        twin = a_ == b_ or (len(a_) > 25 and len(b_) > 25 and (a_ in b_ or b_ in a_))
        if best[0] < 0.5:
            miss += 1
            print(f"  NO CONFIDENT MATCH (best {best[0]:.2f})  {v['title'][:50]}")
        elif (best[1] == oid or twin) and best[0] - runner[0] >= 0.15:
            ok += 1
        elif best[1] == oid or twin:
            amb += 1
        else:
            miss += 1
            print(f"  WRONG     best={titles[best[1]][:40]!r} for {v['title'][:40]!r}")
    n = ok + amb + miss
    print(f"\nselftest: {ok} clean + {amb} twin/thin = {ok+amb} correct of {n}; "
          f"{miss} unmatched (scans with no text layer) ")
    if n and (ok + amb) / n < 0.8:
        print("*** matcher is not reliable enough to install new files. Do not use --apply.")
    return ok, amb, miss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox", default=str(INBOX))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return

    st, rows = load_records()
    outstanding = {o: v["title"] for o, v in st.items() if v["status"] != "have"}
    inbox = Path(a.inbox)
    files = sorted([p for p in inbox.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]) \
        if inbox.exists() else []
    if not files:
        print(f"no PDFs in {inbox}")
        return
    print(f"{len(files)} file(s) in {inbox}; {len(outstanding)} records outstanding\n")
    plan = []
    for f in files:
        txt = pdf_text(f)
        if not txt:
            print(f"  {f.name[:40]:40} NO EXTRACTABLE TEXT — a scan; install by hand")
            continue
        head = toks(" ".join(fold(txt).split()[:900]))
        found_dois = dois_in(txt[:20000])
        doi_hit = [o for o, v2 in st.items()
                   if v2["status"] != "have" and v2.get("doi")
                   and v2["doi"].lower() in found_dois]
        if len(doi_hit) == 1:
            oid = doi_hit[0]
            print(f"  {f.name[:40]:40} -> OK (matched on the DOI printed in the document)")
            print(f"      {st[oid]['title'][:64]}")
            plan.append((f, oid))
            continue
        scored = sorted(((score(t, head), len(toks(t)), o) for o, t in outstanding.items()),
                        reverse=True)
        best, runner = (scored[0][0], scored[0][2]), (scored[1][0], scored[1][2])
        oid = best[1]
        verdict = ("OK" if best[0] >= 0.6 and best[0] - runner[0] >= 0.15
                   else "NO TEXT LAYER / NO MATCH — install by hand" if best[0] < 0.5
                   else "AMBIGUOUS (likely a version twin) — confirm before installing")
        print(f"  {f.name[:40]:40} -> {verdict}")
        print(f"      {best[0]:.2f} {st[oid]['title'][:64]}")
        print(f"      runner-up {runner[0]:.2f} {st[runner[1]]['title'][:56]}")
        if verdict == "OK":
            plan.append((f, oid))
    print()
    if not a.apply:
        print(f"{len(plan)} would install. Re-run with --apply to copy them in.")
        return
    for f, oid in plan:
        shutil.copy2(f, DEST / f"{oid}.pdf")
        print(f"  installed {oid}.pdf  <- {f.name}")
    print(f"\n{len(plan)} installed. Now: python3 source/build/goldset/313_c6a_retrieval.py "
          f"--ids {','.join(o for _, o in plan)}")


main()
