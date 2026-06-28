#!/usr/bin/env python3
"""
Corpus-wide DOI recovery (data-hygiene fix). The phase-2 snowball shuffled the DOI column
but the W-IDs (esp. forward rows) are intact, so re-fetch each record's DOI from OpenAlex
by its W-ID, bypassing the corrupt DOI field. Guard every re-fetch by title-match so drifted
W-IDs (e.g. the chemistry false-positive) are flagged, not trusted.

Input : old-age-security-pension-crowdout-prioritized.json (542)
Output: prioritized_doi_corrected.json (per-record corrected_doi + status) + wid_doi_map.json
Batched: OpenAlex filter=openalex_id:W|W|... (<=50/call) + single-lookup fallback for merges.
"""
import json, re, time, hashlib, urllib.parse, subprocess, sys
from pathlib import Path
from collections import Counter
HERE=Path(__file__).parent; CACHE=HERE/"cache"; CACHE.mkdir(exist_ok=True)
PRIOR=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs/old-age-security-pension-crowdout-prioritized.json")
MAILTO="shravanh@uchicago.edu"; GUARD=0.5
STOP={"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}
def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def curl(url):
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","40","-A",f"fr/1.0 (mailto:{MAILTO})",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n")
    if code=="200":
        try: return json.loads(re.sub(r"[\x00-\x1f]"," ",body))
        except Exception: return None
    return None
def wid_of(work): return (work.get("id") or "").rsplit("/",1)[-1]

def batch_fetch(wids):
    """W-ID -> {doi,title,year} via batched filter, single-lookup fallback for merges/misses."""
    out={}
    wl=list(wids)
    for i in range(0,len(wl),50):
        chunk=wl[i:i+50]
        ck=CACHE/f"oabatch_{hashlib.sha1('|'.join(chunk).encode()).hexdigest()[:16]}.json"
        if ck.exists(): data=json.load(open(ck))
        else:
            # correct multi-ID filter is ids.openalex:W|W|... ('openalex_id' is silently ignored).
            # NOTE: OpenAlex enforces a daily $ budget; a run that exhausts it mid-stream will
            # return errors that look like 404s. Re-run after the UTC reset to get true counts.
            url=f"https://api.openalex.org/works?filter=ids.openalex:{'|'.join(chunk)}&per-page=50&mailto={MAILTO}"
            data=curl(url) or {"results":[]}; json.dump(data,open(ck,"w")); time.sleep(1.0)
        for w in data.get("results",[]):
            out[wid_of(w)]={"doi":(w.get("doi") or "").replace("https://doi.org/","") or None,
                            "title":w.get("display_name"),"year":w.get("publication_year")}
        print(f"  batch {i//50+1}: cumulative {len(out)} resolved", file=sys.stderr)
    missing=[w for w in wids if w not in out]
    print(f"  single-lookup fallback for {len(missing)} (merged/missing)", file=sys.stderr)
    for w in missing:
        cf=CACHE/f"oaid_{w}.json"
        if cf.exists(): d=json.load(open(cf))
        else:
            d=curl(f"https://api.openalex.org/works/{w}?mailto={MAILTO}") or {"_http":"404"}
            json.dump(d,open(cf,"w")); time.sleep(0.7)
        if d.get("id"):
            out[w]={"doi":(d.get("doi") or "").replace("https://doi.org/","") or None,
                    "title":d.get("display_name"),"year":d.get("publication_year"),"_redirected_to":wid_of(d)}
    return out

def main():
    papers=json.load(open(PRIOR))["papers"]
    wids={p["paperId"] for p in papers if (p.get("paperId") or "").startswith("W")}
    print(f"resolving {len(wids)} distinct W-IDs...", file=sys.stderr)
    m=batch_fetch(wids)

    recs=[]; cnt=Counter(); changed=same=0
    for p in papers:
        pid=p.get("paperId",""); od=(p.get("doi") or "").replace("https://doi.org/","").lower() or None
        rec={"paperId":pid,"title":p["title"],"ondisk_doi":od,"source":p.get("source")}
        if not pid.startswith("W"):
            rec["status"]="NO_WID"; rec["corrected_doi"]=None; cnt["NO_WID"]+=1; recs.append(rec); continue
        info=m.get(pid)
        if not info:
            rec["status"]="WID_404"; rec["corrected_doi"]=None; cnt["WID_404"]+=1; recs.append(rec); continue
        sim=jacc(p["title"], info.get("title") or "")
        rec["refetched_title"]=info.get("title"); rec["title_match"]=round(sim,3)
        if sim<GUARD:
            rec["status"]="WID_DRIFT"; rec["corrected_doi"]=None; cnt["WID_DRIFT"]+=1
        elif info.get("doi"):
            rec["status"]="RECOVERED_DOI"; rec["corrected_doi"]=info["doi"].lower(); cnt["RECOVERED_DOI"]+=1
            if od and od!=rec["corrected_doi"]: changed+=1
            elif od and od==rec["corrected_doi"]: same+=1
        else:
            rec["status"]="RECOVERED_NO_DOI"; rec["corrected_doi"]=None; cnt["RECOVERED_NO_DOI"]+=1
        recs.append(rec)

    json.dump(recs, open(HERE/"prioritized_doi_corrected.json","w"), indent=2)
    json.dump({r["paperId"]:r["corrected_doi"] for r in recs if r.get("corrected_doi")},
              open(HERE/"wid_doi_map.json","w"), indent=2)
    print("\n=== corpus-wide W-ID re-fetch ===", file=sys.stderr)
    for k,v in cnt.most_common(): print(f"  {k}: {v}", file=sys.stderr)
    print(f"\nrecords with a recovered DOI: {cnt['RECOVERED_DOI']}/{len(papers)}", file=sys.stderr)
    print(f"of records that HAD an on-disk DOI: {changed} got a DIFFERENT (corrected) DOI, {same} matched", file=sys.stderr)
    print(f"written -> prioritized_doi_corrected.json, wid_doi_map.json", file=sys.stderr)

if __name__=="__main__":
    main()
