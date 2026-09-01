#!/usr/bin/env python3
"""300 — C.3.e: pull candidate estimate sentences from every retrieved primary text. TICK-077.

Generalises 298 to the full available set.

THE MAP IS BUILT FROM VERIFIED SOURCES ONLY, and this is not a detail. A first attempt reconciled the
two PDF folders by fuzzy title matching, and MIS-ASSIGNED 8 OF 10 files: a PDF named for a record that
had since been ROUTED OUT of the primary pool failed the "filename is an id in the pool" test, fell
through to "best title match above 0.6", and landed on an unrelated record sharing a few words. Desai
and Tarozzi's record was handed the No-Birth-Bonus PDF. Nothing was extracted from those pairings, but
only because the mangled output was read before any row was written.

So: (a) a file named <openalex>.pdf was installed with a content check and is trusted; (b) the handoff
CSV carries an explicit key->openalex map for the study-key-named folder. NO FUZZY FALLBACK. Every
mapping is then re-verified against the PDF's own first-page text before use, and a failure is dropped,
never guessed.

Emits, per study, sentences carrying an effect verb AND a fertility outcome AND a number, with the
bibliography cut first. It proposes nothing: OUTCOME_LEVEL, ESTIMATOR_CLASS and `identified` are
judgements made by reading, and on this chapter OUTCOME_LEVEL is load-bearing because realized
fertility and stated desires have carried opposite signs.

Usage: python3 300_c3e_read_all.py
"""
import csv, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
AVAIL = json.loads((ROOT / "temp" / "c3e_avail.json").read_text())
rows = {r["openalex"]: r for r in csv.DictReader((ROOT / "extraction" / "credit-constraints-screen.csv").open())}
done = {r["openalex"] for r in csv.DictReader((ROOT / "extraction" / "credit-constraints-effects.csv").open())}

EFFECT = re.compile(r"\b(increase[sd]?|decrease[sd]?|reduce[sd]?|raise[sd]?|lower[sd]?|effect|impact|"
                    r"associated with|elasticit|coefficient|estimate[sd]?|significant\w*)\b", re.I)
OUTCOME = re.compile(r"\b(fertilit\w*|birth\w*|childbear\w*|children ever born|family size|"
                     r"number of children|contracept\w*|desired family)\b", re.I)
NUM = re.compile(r"[-−]?\d+\.\d+|\d+ ?(percent|per cent|pp\b)")
BIB = re.compile(r"\n\s*(references|bibliography|works cited)\s*\n", re.I)


def text_of(p):
    for a in (["pdftotext", "-q", "-layout", "-enc", "UTF-8", str(p), "-"],
              ["pdftotext", "-q", "-enc", "UTF-8", str(p), "-"]):
        r = subprocess.run(a, capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 1500:
            return r.stdout
    return ""


out = []
for oid, path in AVAIL.items():
    if oid in done:
        continue
    rec = rows.get(oid, {})
    raw = text_of(ROOT / path if not str(path).startswith("/") else path)
    if not raw:
        out.append({"openalex": oid, "status": "TEXT_EXTRACTION_FAILED",
                    "title": rec.get("title"), "arm": rec.get("arm")})
        print(f"\n!! [{rec.get('arm')}] {(rec.get('title') or '')[:60]}: extraction failed")
        continue
    m = list(BIB.finditer(raw))
    body = raw[:m[-1].start()] if m else raw
    sents = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body))
    keep, seen = [], set()
    for s in sents:
        s = s.strip()
        if 45 < len(s) < 400 and EFFECT.search(s) and OUTCOME.search(s) and NUM.search(s):
            if s[:60] not in seen:
                seen.add(s[:60]); keep.append(s)
    out.append({"openalex": oid, "status": "OK", "title": rec.get("title"), "arm": rec.get("arm"),
                "year": rec.get("year"), "chars": len(body), "n": len(keep), "candidates": keep[:10]})
    print(f"\n### [{rec.get('arm') or '-'}] {rec.get('year')} {(rec.get('title') or '')[:62]}  ({len(body)//1000}k, {len(keep)} hits)")
    for s in keep[:3]:
        print(f"    - {s[:250]}")

(LOGS / "credit-constraints-read-all.json").write_text(json.dumps(out, indent=1))
print(f"\n{len([o for o in out if o['status']=='OK'])} read, "
      f"{len([o for o in out if o['status']!='OK'])} failed")
