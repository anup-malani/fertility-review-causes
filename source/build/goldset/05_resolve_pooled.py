#!/usr/bin/env python3
"""
Tier-A gold set, step 1b (robust): pool candidates across multiple queries/sources per
study and pick the best title-guarded match. Single-query-per-source was too brittle
(OpenAlex title.search needs distinctive tokens; plain search= drowns short titles).

Candidate sources per study:
  - OpenAlex search=<title>            (relevance, top 25)
  - OpenAlex filter=title.search:<t>   (AND-ish, top 10)
  - Crossref query.bibliographic       (top 8)
Pick candidate with max token-Jaccard vs our title; accept if >= GUARD.

Cached, polite, throttled. Output: tier_a_authoritative.json (overwrites with robust pass).
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
SRC = HERE / "tier_a_empirical_clusters.json"
OUT = HERE / "tier_a_authoritative.json"
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.60
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with"}

def toks(t):
    t = re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())
    return {w for w in t.split() if w not in STOP}
def jacc(a, b):
    A, B = toks(a), toks(b)
    return len(A & B)/len(A | B) if (A | B) else 0.0

def _get(url, key):
    cf = CACHE / f"{key}.json"
    if cf.exists(): return json.load(open(cf))
    r = subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                        "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
                       capture_output=True, text=True)
    body,_,code = r.stdout.rpartition("\n")
    data={"_http":code}
    if code=="200":
        try: data=json.loads(re.sub(r"[\x00-\x1f]"," ",body)); data["_http"]="200"
        except Exception: data={"_http":"PARSE_ERR"}
    json.dump(data, open(cf,"w")); time.sleep(1.0)
    return data

def candidates(title):
    """Return list of (similarity, doi, matched_title, source, year)."""
    h = hashlib.sha1(title.encode()).hexdigest()[:16]
    q = urllib.parse.quote(title)
    qt = urllib.parse.quote(" ".join(title.split()[:14]))
    cands=[]
    # OpenAlex search= (relevance)
    d = _get(f"https://api.openalex.org/works?search={q}&per-page=25&mailto={MAILTO}", "oas_"+h)
    for r in d.get("results",[]) or []:
        cands.append((jacc(title, r.get("display_name") or ""),
                      (r.get("doi") or "").replace("https://doi.org/","") or None,
                      r.get("display_name"), "openalex:search", r.get("publication_year")))
    # OpenAlex title.search filter
    d = _get(f"https://api.openalex.org/works?filter=title.search:{qt}&per-page=10&mailto={MAILTO}", "oat_"+h)
    for r in d.get("results",[]) or []:
        cands.append((jacc(title, r.get("display_name") or ""),
                      (r.get("doi") or "").replace("https://doi.org/","") or None,
                      r.get("display_name"), "openalex:title", r.get("publication_year")))
    # Crossref bibliographic
    p = urllib.parse.urlencode({"query.bibliographic": title, "rows": 8, "mailto": MAILTO})
    d = _get(f"https://api.crossref.org/works?{p}", "crb_"+h)
    for it in d.get("message",{}).get("items",[]) or []:
        cands.append((jacc(title, (it.get("title") or [""])[0]),
                      it.get("DOI"), (it.get("title") or [""])[0], "crossref",
                      (it.get("issued",{}).get("date-parts",[[None]])[0][0])))
    return sorted(cands, key=lambda x: x[0], reverse=True)

def main():
    studies = json.load(open(SRC))
    for s in studies:
        cs = candidates(s["canonical_title"])
        top = cs[0] if cs else None
        if top and top[0] >= GUARD:
            s["authoritative_doi"] = top[1]
            s["authoritative"] = {"src": top[3], "doi": top[1], "matched": top[2],
                                  "sim": round(top[0],3), "year": top[4]}
        else:
            s["authoritative_doi"] = None
            s["authoritative"] = {"src":"UNRESOLVED",
                                  "best_sim": round(top[0],3) if top else 0.0,
                                  "best_cand": top[2] if top else None}
    json.dump(studies, open(OUT,"w"), indent=2)

    res = Counter(s["authoritative"]["src"] for s in studies)
    have = sum(1 for s in studies if s["authoritative_doi"])
    nodoi_but_matched = sum(1 for s in studies if s["authoritative"]["src"]!="UNRESOLVED" and not s["authoritative_doi"])
    print("=== authoritative resolution source ===", file=sys.stderr)
    for k,v in res.most_common(): print(f"  {k}: {v}", file=sys.stderr)
    print(f"\nstudies with authoritative DOI: {have}/{len(studies)}", file=sys.stderr)
    print(f"matched a work but it has no DOI: {nodoi_but_matched}", file=sys.stderr)
    print("\n=== UNRESOLVED (manual/agent verification) ===", file=sys.stderr)
    for s in studies:
        if s["authoritative"]["src"]=="UNRESOLVED":
            a=s["authoritative"]
            print(f"  [{s['year']}] {s['canonical_title'][:60]}", file=sys.stderr)
            print(f"        best J={a['best_sim']}: {str(a['best_cand'])[:60]}", file=sys.stderr)
    print(f"\nwritten -> {OUT}", file=sys.stderr)

if __name__=="__main__":
    main()
