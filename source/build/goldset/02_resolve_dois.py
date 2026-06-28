#!/usr/bin/env python3
"""
Tier-A gold set, step 1b: resolve DOIs for the no-DOI distinct studies via Crossref,
with a TITLE-SIMILARITY GUARD (Jaccard >= 0.60 on token sets) to reject resolution drift.

- Polite pool: mailto in User-Agent + query param.
- Cached: every Crossref response stored under cache/ so reruns are offline & reproducible.
- Never accepts a match below the guard threshold; logs it as UNRESOLVED for manual handling
  rather than poisoning the gold set with a wrong DOI.

Input : tier_a_empirical_clusters.json
Output: tier_a_empirical_resolved.json  (+ prints a resolution report)
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "tier_a_empirical_clusters.json"
OUT = HERE / "tier_a_empirical_resolved.json"
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.60

STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new"}
def toks(t):
    t = re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())
    return {w for w in t.split() if w not in STOP}
def jacc(a, b):
    A, B = toks(a), toks(b)
    return len(A & B)/len(A | B) if (A | B) else 0.0

def crossref_title(title):
    key = hashlib.sha1(title.encode()).hexdigest()[:16]
    cf = CACHE / f"crossref_{key}.json"
    if cf.exists():
        return json.load(open(cf))
    params = urllib.parse.urlencode({"query.bibliographic": title, "rows": 5, "mailto": MAILTO})
    url = f"https://api.crossref.org/works?{params}"
    out = subprocess.run(
        ["curl", "-s", "--max-time", "30", "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
        capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    json.dump(data, open(cf, "w"))
    time.sleep(1.0)  # polite throttle
    return data

def main():
    studies = json.load(open(SRC))
    todo = [s for s in studies if s["needs_doi_resolution"]]
    print(f"resolving {len(todo)} no-DOI studies via Crossref (guard J>={GUARD})\n", file=sys.stderr)
    for s in studies:
        if not s["needs_doi_resolution"]:
            continue
        title = s["canonical_title"]
        try:
            data = crossref_title(title)
        except Exception as e:
            s["resolution"] = {"status": "ERROR", "error": str(e)}
            print(f"  ERROR  {title[:60]}  -> {e}", file=sys.stderr)
            continue
        items = data.get("message", {}).get("items", [])
        best = None
        for it in items:
            cand = (it.get("title") or [""])[0]
            sim = jacc(title, cand)
            if best is None or sim > best[0]:
                best = (sim, it, cand)
        if best and best[0] >= GUARD:
            sim, it, cand = best
            doi = it.get("doi") or it.get("DOI")
            s["canonical_doi"] = doi
            s["needs_doi_resolution"] = False
            s["resolution"] = {
                "status": "RESOLVED", "similarity": round(sim, 3),
                "matched_title": cand,
                "matched_year": (it.get("issued", {}).get("date-parts", [[None]])[0][0]),
                "container": (it.get("container-title") or [None])[0],
            }
            if doi and doi not in s["member_dois"]:
                s["member_dois"].append(doi)
            print(f"  OK J={sim:.2f}  {title[:55]}\n           -> {doi}  [{cand[:55]}]", file=sys.stderr)
        else:
            sim = best[0] if best else 0.0
            cand = best[2] if best else "(no items)"
            s["resolution"] = {"status": "UNRESOLVED", "best_similarity": round(sim,3), "best_candidate": cand}
            print(f"  MISS J={sim:.2f} {title[:55]}\n           best: {cand[:60]}", file=sys.stderr)

    json.dump(studies, open(OUT, "w"), indent=2)
    n_res = sum(1 for s in studies if s.get("resolution",{}).get("status")=="RESOLVED")
    n_un  = sum(1 for s in studies if s.get("resolution",{}).get("status")=="UNRESOLVED")
    n_doi = sum(1 for s in studies if s["canonical_doi"])
    print(f"\nresolved: {n_res}  unresolved: {n_un}", file=sys.stderr)
    print(f"studies with a canonical DOI: {n_doi}/{len(studies)}", file=sys.stderr)
    print(f"written -> {OUT}", file=sys.stderr)

if __name__ == "__main__":
    main()
