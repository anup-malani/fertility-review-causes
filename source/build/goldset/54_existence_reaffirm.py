#!/usr/bin/env python3
"""
54_existence_reaffirm.py — fine filter, Job 2 (de-hallucination / existence).

Cheap re-affirm that every DOI-resolved study in the confirmed pool is a LIVE
record. The pool was already de-ghosted upstream and each paper was RA-read at
the gate, so this is a belt-and-suspenders guard, not a discovery pass. Uses the
same three-state discipline as 44/48: FOUND / ABSENT / UNCONFIRMED — a network
failure is UNCONFIRMED, never ABSENT (the bug that poisoned the earlier de-ghost).
Only a real Crossref 200-with-DOI counts as ABSENT-clearing. Title-keyed studies
(no DOI) are carried as UNCONFIRMED-existence pending resolution — never dropped.

Deterministic given the cache. No OpenAlex. Quarantines nothing on its own; it
flags, and any true ABSENT is surfaced for the RA.
"""
import json, os, subprocess

SLUG = "old-age-security-pension-crowdout"
MAILTO = "shravanh@uchicago.edu"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)
GS = lambda f: rp("source", "build", "goldset", f)

studies = json.load(open(rp("output", f"{SLUG}-fine-resolved.json")))
CACHE = GS("doi_existence_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def doi_exists(doi):
    """Existence via the DOI resolver (doi.org), NOT Crossref — doi.org is
    registration-agency-agnostic, so DataCite DOIs (SSRN, EconStor, university
    theses: 10.2139/10.4419/10.25549/10.7907) that are absent from Crossref's
    index but perfectly live still resolve. A live DOI 30x-redirects to its
    landing page; 404 is a true negative; anything else is UNCONFIRMED."""
    if doi in cache:
        return cache[doi]
    try:
        code = subprocess.run(
            ["curl", "-s", "-I", "-o", "/dev/null", "-w", "%{http_code}", "-m", "25",
             "-A", f"fertility-review/1.0 (mailto:{MAILTO})",
             f"https://doi.org/{doi}"],
            capture_output=True, text=True).stdout.strip()
        if code.startswith("3") or code == "200":
            state = "FOUND"
        elif code == "404":
            state = "ABSENT"
        else:                       # 429/000/5xx/timeout -> not a real negative
            state = "UNCONFIRMED"
    except Exception:
        state = "UNCONFIRMED"
    cache[doi] = state
    return state

found = absent = unconf = titlekeyed = 0
for r in studies:
    if not r.get("doi"):
        r["existence"] = "UNCONFIRMED_NO_DOI"; titlekeyed += 1; continue
    st = doi_exists(r["doi"])
    r["existence"] = st
    found += st == "FOUND"; absent += st == "ABSENT"; unconf += st == "UNCONFIRMED"

json.dump(cache, open(CACHE, "w"), indent=1)
json.dump(studies, open(rp("output", f"{SLUG}-fine-resolved.json"), "w"),
          ensure_ascii=False, indent=1)

print(f"existence re-affirm over {len(studies)} distinct studies:")
print(f"  FOUND {found} | ABSENT {absent} | UNCONFIRMED {unconf} | title-keyed(no DOI) {titlekeyed}")
if absent:
    print("  ⚠ ABSENT (surfaced for RA — do NOT auto-drop):")
    for r in studies:
        if r.get("existence") == "ABSENT":
            print(f"    - {r['doi']}  {(r['title'] or '')[:60]}")
else:
    print("  no ABSENT records — the resolved pool is clean.")
