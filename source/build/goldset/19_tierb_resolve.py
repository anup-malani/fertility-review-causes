#!/usr/bin/env python3
"""
Part 2 (Tier B) — resolve the frame via the OpenAlex citation graph (the orthogonal channel;
agent/web resolver BANNED for Tier B, spec §3/§8). For each frame W-ID, fetch DOI + year +
abstract + authors from OpenAlex, title-guarded (Jaccard >= 0.5) so drifted W-IDs are flagged
not trusted. Abstract is reconstructed from OpenAlex's inverted index (used downstream for the
relevance audit).

Input : old-age-security-pension-crowdout-tier-b-frame.json (319)
Output: old-age-security-pension-crowdout-tier-b-resolved.json (+ stderr stats)
Batched filter=ids.openalex:W|... (<=50/call), single-lookup fallback for merges/misses.
"""
import json,re,sys,time,hashlib,subprocess
from pathlib import Path
from collections import Counter
HERE=Path(__file__).parent; CACHE=HERE/"cache"; CACHE.mkdir(exist_ok=True)
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
MAILTO="shravanh@uchicago.edu"; GUARD=0.5
STOP={"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}
def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def curl(url):
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","40","-A",f"fr/1.0 (mailto:{MAILTO})",url],
                     capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n")
    if code=="200":
        try: return json.loads(re.sub(r"[\x00-\x1f]"," ",body))
        except Exception: return None
    return None
def wid_of(w): return (w.get("id") or "").rsplit("/",1)[-1]
def abstract_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))[:1500]
def info_of(w):
    return {"doi":(w.get("doi") or "").replace("https://doi.org/","") or None,
            "title":w.get("display_name"),"year":w.get("publication_year"),
            "venue":((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "authors":"; ".join(a.get("author",{}).get("display_name","") for a in (w.get("authorships") or [])[:5]),
            "is_wp":(w.get("type")=="preprint") or False,
            "abstract":abstract_of(w)}

def batch_fetch(wids):
    out={}; wl=list(wids)
    SEL="id,display_name,doi,publication_year,type,primary_location,authorships,abstract_inverted_index"
    for i in range(0,len(wl),50):
        chunk=wl[i:i+50]
        ck=CACHE/f"tbbatch_{hashlib.sha1('|'.join(chunk).encode()).hexdigest()[:16]}.json"
        if ck.exists(): data=json.load(open(ck))
        else:
            url=f"https://api.openalex.org/works?filter=ids.openalex:{'|'.join(chunk)}&per-page=50&select={SEL}&mailto={MAILTO}"
            data=curl(url) or {"results":[]}; json.dump(data,open(ck,"w")); time.sleep(1.0)
        for w in data.get("results",[]): out[wid_of(w)]=info_of(w)
        print(f"  batch {i//50+1}: cumulative {len(out)}",file=sys.stderr)
    missing=[w for w in wids if w not in out]
    print(f"  single-lookup fallback for {len(missing)}",file=sys.stderr)
    for w in missing:
        cf=CACHE/f"tbid_{w}.json"
        if cf.exists(): d=json.load(open(cf))
        else:
            d=curl(f"https://api.openalex.org/works/{w}?select={SEL}&mailto={MAILTO}") or {"_404":1}
            json.dump(d,open(cf,"w")); time.sleep(0.7)
        if d.get("id"): out[w]=info_of(d)|{"_redirected_to":wid_of(d)}
    return out

def main():
    frame=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-b-frame.json"))
    wids=[p["paperId"] for p in frame if (p.get("paperId") or "").startswith("W")]
    print(f"resolving {len(wids)} W-IDs via OpenAlex citation graph...",file=sys.stderr)
    m=batch_fetch(wids)
    out=[]; cnt=Counter()
    for p in frame:
        rec=dict(p); info=m.get(p["paperId"])
        if not info: rec["resolve_status"]="WID_404"; cnt["WID_404"]+=1; out.append(rec); continue
        sim=jacc(p["title"],info.get("title") or "")
        rec["oa_title"]=info["title"]; rec["title_match"]=round(sim,3)
        rec["year"]=info["year"]; rec["venue"]=info["venue"]; rec["authors"]=info["authors"]
        rec["is_working_paper"]=info["is_wp"]; rec["abstract"]=info["abstract"]
        if sim<GUARD:
            rec["resolve_status"]="WID_DRIFT"; rec["doi"]=None; cnt["WID_DRIFT"]+=1
        elif info["doi"]:
            rec["resolve_status"]="RESOLVED_DOI"; rec["doi"]=info["doi"].lower(); cnt["RESOLVED_DOI"]+=1
        else:
            rec["resolve_status"]="NO_DOI"; rec["doi"]=None; cnt["NO_DOI"]+=1
        out.append(rec)
    json.dump(out,open(LOGS/"old-age-security-pension-crowdout-tier-b-resolved.json","w"),indent=2)
    print("\n=== Tier B resolution ===",file=sys.stderr)
    for k,v in cnt.most_common(): print(f"  {k}: {v}",file=sys.stderr)
    ab=sum(1 for r in out if r.get("abstract"))
    print(f"  with abstract (for relevance audit): {ab}/{len(out)}",file=sys.stderr)
    print(f"\nwritten -> old-age-security-pension-crowdout-tier-b-resolved.json",file=sys.stderr)
if __name__=="__main__": main()
