#!/usr/bin/env python3
"""298 — C.3.e: pull candidate estimate sentences from the retrieved primary texts. TICK-077.

Extraction proper is a human read; this narrows where to read. For each retrieved PDF it emits
sentences that carry BOTH an effect verb and a fertility outcome, plus any sentence naming a
coefficient with a standard error, with the bibliography cut first.

Deliberately does NOT decide anything. The required tags in the scope memo -- ARM, OUTCOME_LEVEL,
TEMPO_OR_QUANTUM, ESTIMATOR_CLASS, SETTING_FINANCE_DEPTH, CONSTRAINT_MEASURED -- are judgements
made at full text, and `OUTCOME_LEVEL` in particular is load-bearing for this chapter: realized
fertility and stated desires carried OPPOSITE signs in the composite studies read so far, so an
extraction that does not record which one an estimate refers to is worse than none.

Usage: python3 298_c3e_extract_candidates.py
"""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "credit-constraints-extraction-candidates.json"

EFFECT = re.compile(r"\b(increase[sd]?|decrease[sd]?|reduce[sd]?|raise[sd]?|lower[sd]?|"
                    r"effect|impact|associated with|elasticit|coefficient|estimate[sd]?)\b", re.I)
OUTCOME = re.compile(r"\b(fertilit\w*|birth\w*|childbear\w*|children ever born|family size|"
                     r"number of children|contracept\w*|parity|desired family)\b", re.I)
NUMBER = re.compile(r"[-−]?\d+\.\d+")
SE = re.compile(r"\((\s*[\d.]+\s*)\)|standard error|s\.e\.", re.I)
BIB = re.compile(r"\n\s*(references|bibliography|works cited)\s*\n", re.I)


def text_of(p):
    for args in (["pdftotext", "-q", "-layout", "-enc", "UTF-8", str(p), "-"],
                 ["pdftotext", "-q", "-enc", "UTF-8", str(p), "-"]):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 2000:
            return r.stdout
    return ""


def main():
    ret = json.loads((LOGS / "credit-constraints-primary-retrieval.json").read_text())
    out = []
    for rec in ret["records"]:
        if not rec.get("fetched_path"):
            continue
        raw = text_of(ROOT / rec["fetched_path"])
        if not raw:
            out.append({**{k: rec[k] for k in ("openalex", "title", "year", "arm", "cell")},
                        "status": "TEXT_EXTRACTION_FAILED"})
            print(f"!! {rec['title'][:60]}: text extraction failed")
            continue
        m = list(BIB.finditer(raw))
        body = raw[:m[-1].start()] if m else raw
        sents = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body))
        hits = [s.strip() for s in sents
                if 40 < len(s) < 420 and EFFECT.search(s) and OUTCOME.search(s)
                and (NUMBER.search(s) or SE.search(s))]
        seen, keep = set(), []
        for s in hits:
            k = s[:70]
            if k not in seen:
                seen.add(k)
                keep.append(s)
        out.append({**{k: rec[k] for k in ("openalex", "title", "year", "arm", "cell")},
                    "status": "OK", "chars": len(body), "n_candidates": len(keep),
                    "candidates": keep[:12]})
        print(f"\n### [{rec['arm']}] {rec['year']} {(rec['title'] or '')[:66]}")
        print(f"    body {len(body)//1000}k chars, {len(keep)} candidate estimate sentences")
        for s in keep[:4]:
            print(f"      - {s[:230]}")
    OUT.write_text(json.dumps(out, indent=1))
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
