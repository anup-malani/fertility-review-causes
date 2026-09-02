#!/usr/bin/env python3
"""316 — emit focused extraction excerpts for the retrieved C.6.a full texts. TICK-078.

Extraction reads for the ESTIMATE and its provenance, not the prose. This pulls, per record:
  - the head (title, authors, abstract, opening) where the design is usually declared;
  - paragraphs carrying result markers -- coefficients, elasticities, significance, R2, "table";
  - paragraphs carrying the EXPOSURE vocabulary, because scope §4's `exposure_distance` turns on
    what the study actually measured rather than what it says it measured.

It does not decide anything. `design` in particular is a hypothesis until a human reads the text --
A.23 carried a paper through three stages as an administrative allocation when it was IPTW
(`design-is-not-a-property-of-the-title`).

Usage: python3 source/build/goldset/316_c6a_extraction_sheets.py --cell BENCHMARK_MEASURED [--chars N]
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
DEST = ROOT / "temp" / "c6a-fulltext"

JXA = """
function run(argv){
  ObjC.import("Quartz");
  const u = $.NSURL.fileURLWithPath(argv[0]);
  const d = $.PDFDocument.alloc.initWithURL(u);
  if (!d.js) return "";
  const s = ObjC.unwrap(d.string);
  return s ? s : "";
}
"""

RESULT = re.compile(r"coefficient|elasticit|statistically significant|significant at|"
                    r"\bR2\b|R-squared|adjusted r|standard error|t-statistic|p\s?<|"
                    r"per cent|percent|estimat|regression|table \d|column \(", re.I)
EXPOSURE = re.compile(r"relative income|relative cohort|cohort size|aspiration|parental|"
                      r"father'?s income|two generations|relative economic status|"
                      r"crowding|young.{0,12}(men|adults|workers)", re.I)


def pdf_text(path):
    r = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, str(path)],
                       capture_output=True, text=True, timeout=180)
    return r.stdout or ""


def paras(txt):
    """Overlapping fixed windows, not blank-line paragraphs.

    PDFKit returns text with no blank lines between paragraphs, so a blank-line splitter returned
    ONE paragraph per paper and the result/exposure filters selected the whole document every time.
    Windows are cheap and do not depend on the PDF preserving structure it never had."""
    txt = re.sub(r"\s+", " ", txt).strip()
    W, STEP = 700, 500
    return [txt[i:i + W] for i in range(0, max(1, len(txt) - 200), STEP)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", required=True)
    ap.add_argument("--chars", type=int, default=1500)
    ap.add_argument("--per-para", type=int, default=340)
    ap.add_argument("--max-paras", type=int, default=9)
    a = ap.parse_args()

    st = json.loads((LOGS / "easterlin-relative-income-retrieval-state.json").read_text())["records"]
    recs = [(o, v) for o, v in st.items()
            if v["status"] == "have" and v["cell"] == a.cell]
    recs.sort(key=lambda kv: kv[1]["year"] or "")
    for oid, v in recs:
        f = DEST / f"{oid}.pdf"
        print("\n" + "=" * 100)
        print(f"{oid}  [{v['cell']}]  {v['year']}  {v['title']}")
        print("=" * 100)
        txt = pdf_text(f)
        if not txt.strip():
            print("  *** NO TEXT LAYER — this is a scan. Extraction needs a human read or OCR.")
            continue
        print("--- HEAD ---")
        print(re.sub(r"\s+", " ", txt)[:a.chars])
        ps = paras(txt)[3:]          # skip the head, already printed above
        def pick(rx, pool, n):
            out = []
            for w in pool:
                if rx.search(w) and not any(w[:120] in o or o[:120] in w for o in out):
                    out.append(w)
                if len(out) >= n:
                    break
            return out
        # Prefer windows dense in numbers: that is where an estimate lives.
        scored = sorted(ps, key=lambda w: -sum(c.isdigit() for c in w))
        res = pick(RESULT, scored, a.max_paras)
        exp = pick(EXPOSURE, ps, 5)
        print("\n--- RESULT-BEARING ---")
        for p in res:
            print("  * " + p[:a.per_para])
        print("\n--- EXPOSURE-BEARING ---")
        for p in exp:
            print("  * " + p[:a.per_para])


main()
