#!/usr/bin/env python3
"""281 — C.3.e: does any composite/savings probe ESTIMATE a fertility outcome? TICK-077.

280 fetched full texts. This scans them, but the question is not "does the word fertility
appear" -- it is "is a fertility or birth variable on the left-hand side of an estimate".
Three things separate those, and all three are enforced here:

  1. THE BIBLIOGRAPHY IS CUT FIRST. A cited paper with "fertility" in its title is not an
     outcome. Scanning a whole PDF for a word and reporting a hit count is how a passing
     mention becomes a finding.
  2. CONTEXT IS PRINTED, NOT COUNTED. Every hit is emitted with surrounding text for a human
     read. The script proposes a class; it does not decide.
  3. TABLE AND OUTCOME-LIST CONTEXTS ARE FLAGGED SEPARATELY from prose. A fertility outcome
     that exists only in a table is exactly the case this whole check was built for -- the
     abstract never says it, so nothing upstream of the full text could see it.

Usage: python3 281_c3e_probe_outcome_scan.py
"""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
RET = json.loads((LOGS / "credit-constraints-probe-retrieval.json").read_text())
OUT = LOGS / "credit-constraints-probe-outcome-scan.json"

# Outcome vocabulary, deliberately wider than the production query's: this is a within-document
# scan, so the precision cost of a broad list is a few lines to read, not a screening burden.
OUTCOME = [r"fertilit\w*", r"\bbirths?\b", r"birth rate", r"childbearing", r"child-bearing",
           r"children ever born", r"number of children", r"family size", r"family planning",
           r"contracept\w*", r"pregnan\w*", r"\bparity\b", r"birth spacing", r"total fertility"]
OUT_RE = re.compile("|".join(OUTCOME), re.I)

# a hit inside one of these is a candidate ESTIMATE, not a mention
TABLE_RE = re.compile(r"table\s+\d|panel\s+[a-d]\b|dependent variable|outcome variable|"
                      r"\(1\)\s+\(2\)|standard error|std\. err|\bs\.e\.\b", re.I)
OUTCOMELIST_RE = re.compile(r"outcomes?\s+(are|include|were|we\s+measure)|"
                            r"we\s+(measure|examine|estimate|report)\s+", re.I)
# bibliography cut
BIB_RE = re.compile(r"\n\s*(references|bibliography|works cited)\s*\n", re.I)


def text_of(pdf):
    for args in (["pdftotext", "-q", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                 ["pdftotext", "-q", "-enc", "UTF-8", str(pdf), "-"]):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 2000:
            return r.stdout
    return ""


def main():
    results = []
    for rec in RET["records"]:
        if not rec.get("fetched_path"):
            results.append({"key": rec["key"], "status": "NOT_RETRIEVED",
                            "handoff": rec.get("handoff")})
            continue
        raw = text_of(ROOT / rec["fetched_path"])
        if not raw:
            results.append({"key": rec["key"], "status": "TEXT_EXTRACTION_FAILED"})
            print(f"\n### {rec['key']}: TEXT EXTRACTION FAILED")
            continue

        m = list(BIB_RE.finditer(raw))
        body = raw[:m[-1].start()] if m else raw
        cut = "bibliography cut" if m else "NO bibliography heading found - whole doc scanned"

        hits = []
        for mo in OUT_RE.finditer(body):
            a, b = max(0, mo.start() - 130), min(len(body), mo.end() + 130)
            ctx = re.sub(r"\s+", " ", body[a:b]).strip()
            klass = ("TABLE" if TABLE_RE.search(ctx) else
                     "OUTCOME_LIST" if OUTCOMELIST_RE.search(ctx) else "PROSE")
            hits.append({"term": mo.group(0), "class": klass, "context": ctx})

        strong = [h for h in hits if h["class"] in ("TABLE", "OUTCOME_LIST")]
        results.append({"key": rec["key"], "status": "SCANNED", "chars_body": len(body),
                        "bib": cut, "n_hits": len(hits), "n_strong": len(strong),
                        "hits": hits[:80]})
        print(f"\n### {rec['key']}  ({cut}; body {len(body)//1000}k chars)")
        print(f"    outcome-vocabulary hits: {len(hits)}   in TABLE/OUTCOME_LIST context: {len(strong)}")
        for h in strong[:6]:
            print(f"      [{h['class']}] ...{h['context'][:190]}...")
        if not strong:
            for h in hits[:4]:
                print(f"      [prose] ...{h['context'][:170]}...")

    OUT.write_text(json.dumps(results, indent=2))
    print("\n" + "=" * 78)
    for r in results:
        if r["status"] == "SCANNED":
            print(f"  {r['key']:36s} hits {r['n_hits']:4d}  strong {r['n_strong']:3d}")
        else:
            print(f"  {r['key']:36s} {r['status']}")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
