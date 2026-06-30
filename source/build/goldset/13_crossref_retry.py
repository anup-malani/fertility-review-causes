#!/usr/bin/env python3
"""
Step 0/1 residual retry, deterministic pass (2026-06-29, post OpenAlex-budget + S2 rate-limit
reset). For each of the 21 Tier-A residuals (retry_input.json):
  1. verify each on-disk candidate DOI via Crossref (the original failure for several was a
     rate-limited/budget-blocked API, not a missing paper);
  2. on no passing candidate, Crossref query.bibliographic title search (year-filtered),
     guard the top hits.
Accept criterion is IDENTICAL to 07_verify_agent_dois.py: title Jaccard >= 0.50 AND
|year delta| <= 3, Crossref-200 primary. Candidate-DOI hits and search hits are tagged so the
provenance is auditable. Whatever stays NOT_FOUND is the input to the agent fleet.

Category A (likely-not-real / chimeric variants of id18) is resolved too but tagged
A_REVIEW on any hit -- never silently folded; generic-title hits are tagged GENERIC_REVIEW.

Input : retry_input.json
Output: retry_crossref_results.json (+ stderr summary)
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.50
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}

def toks(t):
    t=re.sub(r"[^a-z0-9\s]"," ",(t or "").lower())
    return {w for w in t.split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0

def curl_json(url, tag):
    cf=CACHE/f"{tag}_{hashlib.sha1(url.encode()).hexdigest()[:16]}.json"
    if cf.exists(): return json.load(open(cf))
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                      "-A",f"fertility-review/1.0 (mailto:{MAILTO})",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n"); data={"_http":code}
    if code=="200":
        try: data=json.loads(re.sub(r"[\x00-\x1f]"," ",body)); data["_http"]="200"
        except Exception: data={"_http":"PARSE_ERR"}
    json.dump(data,open(cf,"w")); time.sleep(1.0)
    return data

def cr_doi(doi):
    doi=doi.replace("https://doi.org/","").strip().lower()
    return curl_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}","verifydoi")

def cr_search(title, year):
    q=urllib.parse.quote(title)
    url=f"https://api.crossref.org/works?query.bibliographic={q}&rows=5&mailto={MAILTO}"
    if year: url+=f"&filter=from-pub-date:{year-3}-01-01,until-pub-date:{year+3}-12-31"
    return curl_json(url,"crsearch")

def meta_of(m):
    crt=(m.get("title") or [""])[0]
    cry=(m.get("issued",{}).get("date-parts",[[None]])[0][0]) or \
        (m.get("published",{}).get("date-parts",[[None]])[0][0])
    auth="; ".join(f"{a.get('family','')}".strip() for a in (m.get("author") or [])[:4])
    return crt, cry, auth, (m.get("DOI") or "").lower(), (m.get("container-title") or [""])[0]

def guarded(title, year, crt, cry):
    sim=jacc(title,crt)
    yr_ok=(year is None or cry is None or abs((cry or 0)-(year or 0))<=3)
    return sim, yr_ok, (sim>=GUARD and yr_ok)

def main():
    studies=json.load(open(HERE/"retry_input.json"))
    results=[]
    for s in studies:
        sid,title,year,cat=s["id"],s["title"],s.get("year"),s["category"]
        rec={"id":sid,"category":cat,"title":title,"year":year,"hint":s.get("hint"),
             "verdict":None,"final_doi":None,"via":None,"match":None}
        generic = len(toks(title))<=6   # short, generic title -> false-match prone

        # 1) candidate DOIs
        best=None
        for cd in s.get("candidate_dois",[]):
            d=cr_doi(cd)
            if d.get("_http")!="200": continue
            crt,cry,auth,rdoi,ven=meta_of(d.get("message",{}))
            sim,yr_ok,ok=guarded(title,year,crt,cry)
            cand={"doi":cd.lower(),"crossref_title":crt,"crossref_year":cry,"authors":auth,
                  "venue":ven,"jaccard":round(sim,3),"year_ok":yr_ok,"pass":ok}
            if ok and (best is None or sim>best["jaccard"]): best=cand|{"via":"candidate_doi"}
        # 2) bibliographic search fallback
        if best is None:
            d=cr_search(title,year)
            for it in d.get("message",{}).get("items",[]):
                crt,cry,auth,rdoi,ven=meta_of(it)
                sim,yr_ok,ok=guarded(title,year,crt,cry)
                if ok and (best is None or sim>best["jaccard"]):
                    best={"doi":rdoi,"crossref_title":crt,"crossref_year":cry,"authors":auth,
                          "venue":ven,"jaccard":round(sim,3),"year_ok":yr_ok,"pass":ok,"via":"search"}

        # Accept policy. The J>=0.50 guard is trustworthy only when VERIFYING a specific
        # candidate DOI (already disambiguated by a human/agent). For BLIND SEARCH selection
        # it false-matches on common-phrasing titles (observed: id5 Ecuador->Korea J=0.50,
        # id6 rural-China->Zhang J=0.545). So search hits must clear a much higher bar
        # (SEARCH_GUARD) to auto-verify; otherwise they are proposals for review, never folded.
        SEARCH_GUARD=0.80
        if best:
            rec["final_doi"]=best["doi"]; rec["via"]=best["via"]; rec["match"]=best
            auto = best["via"]=="candidate_doi" or best["jaccard"]>=SEARCH_GUARD
            if cat=="A": rec["verdict"]="A_REVIEW"
            elif not auto: rec["verdict"]="SEARCH_PROPOSAL"
            elif generic: rec["verdict"]="GENERIC_REVIEW"
            else: rec["verdict"]="VERIFIED"
        else:
            rec["verdict"]="NOT_FOUND"
        results.append(rec)

    json.dump(results,open(HERE/"retry_crossref_results.json","w"),indent=2)
    c=Counter(r["verdict"] for r in results)
    print("=== deterministic Crossref retry verdicts ===",file=sys.stderr)
    for k,v in c.most_common(): print(f"  {k}: {v}",file=sys.stderr)
    print(f"\n--- HITS (verify-then-fold) ---",file=sys.stderr)
    for r in results:
        if r["final_doi"]:
            m=r["match"]
            print(f"  id{r['id']:>2} [{r['verdict']}] J={m['jaccard']} via {r['via']}  {r['final_doi']}",file=sys.stderr)
            print(f"        -> {m['crossref_title'][:70]} ({m['crossref_year']}; {m['authors']})",file=sys.stderr)
    print(f"\n--- STILL NOT_FOUND (-> agent fleet) ---",file=sys.stderr)
    for r in results:
        if r["verdict"]=="NOT_FOUND":
            print(f"  id{r['id']:>2} [{r['category']}] {r['title'][:58]}",file=sys.stderr)
    print(f"\nwritten -> retry_crossref_results.json",file=sys.stderr)

if __name__=="__main__":
    main()
