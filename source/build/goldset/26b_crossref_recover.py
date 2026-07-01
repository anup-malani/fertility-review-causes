#!/usr/bin/env python3
"""
Step 26b - Crossref title-search recovery for the meta-analysis-ready papers whose DOI stayed
UNRESOLVED after the OpenAlex pass (dead/drift W-IDs, or OK-status works with no DOI registered
in OpenAlex, e.g. published papers OpenAlex simply lacks a DOI for).

C2 blind-search discipline: normalize title -> Crossref query.bibliographic (year-windowed) ->
accept the top hit only if title Jaccard >= 0.80 AND |year delta| <= 3 (the 0.80 SELECT
threshold, stricter than the 0.50 VERIFY threshold, because we are selecting from blind search).
Short/generic titles (<=6 content tokens) require an author-surname corroboration to accept.
Reuses the cached, polite Crossref client from 13_crossref_retry.py.

Input : {slug}-metaanalysis-ready-final.json (reads rows with doi_final == null)
Output: {slug}-crossref-recovered.json  (paperId -> {doi, match, cr_title, cr_year})
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path

HERE = Path(__file__).parent
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
SL = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
SLUG = "old-age-security-pension-crowdout"
MAILTO = "shravanh@uchicago.edu"
SELECT = 0.80
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}

def toks(t):
    return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
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

def cr_search(title, year):
    url=f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(title)}&rows=5&mailto={MAILTO}"
    if year: url+=f"&filter=from-pub-date:{year-3}-01-01,until-pub-date:{year+3}-12-31"
    return curl_json(url,"crsearch")

def main():
    rows=json.load(open(SL/f"{SLUG}-metaanalysis-ready-final.json"))
    todo=[r for r in rows if not r.get("doi_final") and r.get("title")]
    print(f"crossref-recovering {len(todo)} unresolved...", file=sys.stderr)
    rec={}; acc=0
    for i,r in enumerate(todo,1):
        title=r["title"]; year=r.get("year"); authors=[a.lower() for a in (r.get("authors") or [])]
        generic=len(toks(title))<=6
        data=cr_search(title,year)
        best=None
        for m in (data.get("message",{}).get("items",[]) if data.get("_http")=="200" else []):
            crt=(m.get("title") or [""])[0]
            cry=(m.get("issued",{}).get("date-parts",[[None]])[0][0])
            sim=jacc(title,crt)
            yr_ok=(year is None or cry is None or abs((cry or 0)-(year or 0))<=3)
            fam=[ (a.get("family") or "").lower() for a in (m.get("author") or []) ]
            auth_ok=(not generic) or any(s in fam for s in authors)
            if sim>=SELECT and yr_ok and auth_ok and (m.get("DOI")):
                if not best or sim>best[0]:
                    best=(sim,(m["DOI"]).lower(),crt,cry)
        if best:
            rec[r["paperId"]]={"doi":best[1],"match":round(best[0],3),"cr_title":best[2],"cr_year":best[3]}
            acc+=1
        if i%25==0: print(f"  {i}/{len(todo)} processed, {acc} recovered", file=sys.stderr)
    json.dump(rec, open(SL/f"{SLUG}-crossref-recovered.json","w"), indent=2)
    print(f"recovered {acc}/{len(todo)} via guarded Crossref search (J>={SELECT})", file=sys.stderr)

if __name__=="__main__":
    main()
