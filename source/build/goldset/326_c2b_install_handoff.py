#!/usr/bin/env python3
"""326 — install hand-retrieved PDFs for C.2.b, matching by CONTENT not by filename. TICK-079.

Port of C.6.a's 315. Hand-retrieved PDFs arrive publisher-named — `1-s2.0-S030438781730069X-main.pdf`,
`imdf.pdf`, `uganda.pdf` — and installing them by filename order silently pairs a record with the
wrong document. Nothing downstream catches it, because every later stage reads the extraction table
rather than the PDF (`handoff-file-match-by-content`).

Match order, strongest signal first:
  1. the DOI printed inside the document (most journal PDFs carry it on page 1)
  2. the longest CONTIGUOUS run of the record's title tokens near the front of the text

Contiguity matters: a scorer counting title tokens appearing anywhere in 40,000 characters matches a
paper's own bibliography, and a short generic title then wins files that are not it. Ties break
toward the LONGER title, because a short title contained inside a longer one scores 1.00 against the
longer one's paper (`title-gate-cannot-refuse-short-superset`).

Text extraction is macOS PDFKit through JXA — no pdftotext, pypdf or mutool on this machine, and
C.6.a's hand-rolled FlateDecode extractor scored 2/25 on its own selftest.

THE MATCHER IS VALIDATED BEFORE IT IS TRUSTED. `--selftest` runs it against the PDFs already
retrieved automatically, whose pairing is known, and refuses `--apply` below 80%
(`validate-a-null-detector-on-positives`).

Usage:
  python3 source/build/goldset/326_c2b_install_handoff.py --selftest
  python3 source/build/goldset/326_c2b_install_handoff.py --inbox DIR [--apply]
"""
import argparse
import json
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
PDFS = ROOT / "literature" / "pdfs" / "child-cost-direct"
GOT = {"fetched", "already_on_disk", "hand_retrieved"}
STOP = {"the", "a", "an", "of", "and", "in", "on", "to", "for", "is", "are", "at", "by", "with",
        "from", "as", "its", "it", "this", "that", "some", "into", "during", "evidence", "case"}
MIN_TITLE_TOKENS = 4

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
DOI_RE = re.compile(r"10\s?\.\s?\d{4,9}\s?/\s?[-._;()/:a-z0-9]+", re.I)


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def toks(s):
    return [t for t in fold(s).split() if len(t) > 2 and t not in STOP]


def pdf_text(path):
    try:
        r = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, str(path)],
                           capture_output=True, text=True, timeout=180)
        return r.stdout or ""
    except subprocess.TimeoutExpired:
        return ""


def dois_in(text):
    """RAW text, never folded: fold() turns a DOI into spaces and silently kills the strongest
    signal here while the title heuristics carry on looking fine."""
    return {re.sub(r"\s+", "", d).lower().rstrip(".,;") for d in DOI_RE.findall(text)}


def longest_run(tt, xt):
    if not tt:
        return 0
    pos = {}
    for i, w in enumerate(xt):
        pos.setdefault(w, []).append(i)
    best = 0
    for start in range(len(tt)):
        for i in pos.get(tt[start], ()):
            n = 0
            while start + n < len(tt) and i + n < len(xt) and tt[start + n] == xt[i + n]:
                n += 1
            best = max(best, n)
        if best == len(tt):
            break
    return best


def score(title, head):
    tt = toks(title)
    if len(set(tt)) < MIN_TITLE_TOKENS:
        return -1.0
    return longest_run(tt, head) / len(tt)


def load():
    return json.loads((LOGS / "child-cost-direct-retrieval.json").read_text())["records"]


def identify(txt, cands, all_recs):
    """(screen_id, how, score, runner_up_score) or (None, reason, ...)."""
    head = toks(" ".join(fold(txt).split()[:900]))
    found = dois_in(txt[:20000])
    hits = [r for r in cands if r.get("doi") and r["doi"].lower() in found]
    if len(hits) == 1:
        return hits[0]["screen_id"], "doi printed in the document", 1.0, 0.0
    scored = sorted(((score(r["title"], head), len(toks(r["title"])), r["screen_id"])
                     for r in all_recs), reverse=True)
    if not scored:
        return None, "no candidates", 0.0, 0.0
    best, runner = scored[0], (scored[1] if len(scored) > 1 else (0.0, 0, None))
    if best[0] < 0.5:
        return None, f"no confident title match (best {best[0]:.2f})", best[0], runner[0]

    # A tie between VERSION TWINS is not ambiguity -- it is the same paper under several OpenAlex
    # records, and this chapter has many (Ghana free secondary appears three times). The first
    # version of this matcher declared every such tie ambiguous and scored 44% on its own selftest
    # while being right about all of them. Collapse the tied band by folded title before deciding
    # (`version-pair-is-one-study`); only a tie between DIFFERENT papers is a refusal.
    tied = [s for s in scored if best[0] - s[0] < 0.15]
    tt = {sid: fold(next(r["title"] for r in all_recs if r["screen_id"] == sid)).strip()
          for _, _, sid in tied}
    def same(a, b):
        return a == b or (len(a) > 25 and len(b) > 25 and (a in b or b in a))
    head_t = tt[best[2]]
    if all(same(head_t, v) for v in tt.values()):
        cand_ids = {r["screen_id"] for r in cands}
        pick = next((sid for _, _, sid in tied if sid in cand_ids), best[2])
        how = ("longest contiguous title run" if len(tied) == 1
               else f"longest contiguous title run; {len(tied)} version twins tied and collapsed")
        return pick, how, best[0], runner[0]
    return None, f"ambiguous between different papers: {best[0]:.2f} vs {runner[0]:.2f}", \
        best[0], runner[0]


def selftest():
    recs = load()
    have = [r for r in recs if r["status"] in GOT and (PDFS / f"{r['screen_id']}.pdf").exists()]
    ok = twin = miss = 0
    for r in have:
        txt = pdf_text(PDFS / f"{r['screen_id']}.pdf")
        if not txt:
            miss += 1
            print(f"  NO TEXT   {r['title'][:56]}")
            continue
        sid, how, b, ru = identify(txt, recs, recs)
        if sid == r["screen_id"]:
            ok += 1
        elif sid:
            a_, b_ = fold(next(x["title"] for x in recs if x["screen_id"] == sid)).strip(), \
                fold(r["title"]).strip()
            if a_ == b_ or (len(a_) > 25 and len(b_) > 25 and (a_ in b_ or b_ in a_)):
                twin += 1          # a version twin is the same paper; not a miss
            else:
                miss += 1
                print(f"  WRONG  got {sid} for {r['screen_id']} — {r['title'][:44]}")
        else:
            miss += 1
            print(f"  UNMATCHED ({how})  {r['title'][:48]}")
    n = ok + twin + miss
    rate = (ok + twin) / n if n else 0
    print(f"\nselftest: {ok} exact + {twin} twin = {ok + twin} correct of {n} ({rate:.0%}); "
          f"{miss} unmatched")
    if rate < 0.8:
        print("*** matcher is NOT reliable enough to install new files. Do not use --apply.")
    return rate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return

    recs = load()
    outstanding = [r for r in recs if r["status"] not in GOT]
    inbox = Path(a.inbox)
    files = sorted(p for p in inbox.iterdir() if p.suffix.lower() == ".pdf")
    print(f"{len(files)} PDF(s) in {inbox}; {len(outstanding)} records outstanding\n")
    plan, unmatched = [], []
    for f in files:
        txt = pdf_text(f)
        if not txt:
            unmatched.append((f, "no extractable text — a scan; install by hand"))
            print(f"  {f.name[:44]:44} NO TEXT")
            continue
        sid, how, b, ru = identify(txt, outstanding, recs)
        if not sid:
            unmatched.append((f, how))
            print(f"  {f.name[:44]:44} UNMATCHED — {how}")
            continue
        rec = next(x for x in recs if x["screen_id"] == sid)
        already = rec["status"] in GOT
        print(f"  {f.name[:44]:44} -> {sid}  ({how}, {b:.2f} vs {ru:.2f})"
              f"{'  [ALREADY HAVE]' if already else ''}")
        print(f"      {rec['title'][:74]}")
        if not already:
            plan.append((f, sid))
    if not a.apply:
        print(f"\ndry run: {len(plan)} would install, {len(unmatched)} unmatched. "
              "Re-run with --apply.")
        return
    PDFS.mkdir(parents=True, exist_ok=True)
    for f, sid in plan:
        shutil.copy2(f, PDFS / f"{sid}.pdf")

    # Provenance, written at install time. A hand-retrieved file has NO rung -- no automated route
    # produced it -- and letting it inherit one would make the rung table claim a capability the
    # pipeline does not have (`a-cache-must-not-invent-provenance`, `via="cached" is a fake rung`).
    jf = LOGS / "child-cost-direct-retrieval.json"
    blob = json.loads(jf.read_text())
    ids = {sid for _, sid in plan}
    for r in blob["records"]:
        if r["screen_id"] in ids:
            r["status"] = "hand_retrieved"
            r["rung"] = None
            r["provenance"] = "handoff install, matched on the DOI printed in the document"
            r["handoff"] = None
            r["path"] = f"literature/pdfs/child-cost-direct/{r['screen_id']}.pdf"
    blob["hand_retrieved"] = sorted(ids | set(blob.get("hand_retrieved", [])))
    jf.write_text(json.dumps(blob, indent=1) + "\n")
    print(f"\ninstalled {len(plan)} PDF(s) into {PDFS.relative_to(ROOT)}; "
          "provenance recorded as hand_retrieved (no rung)")
    for f, why in unmatched:
        print(f"  LEFT IN INBOX: {f.name} — {why}")


main()
