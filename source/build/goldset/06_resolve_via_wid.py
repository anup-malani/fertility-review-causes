#!/usr/bin/env python3
"""
Tier-A gold set, step 1b (W-ID path): resolve each distinct study by looking up its on-disk
OpenAlex W-ID(s) directly. OpenAlex by-ID lookups follow merge-redirects, so most W-IDs
still resolve to the live work even though the W-ID *value* may have drifted. Accept the
DOI only if the resolved work's title matches our title (token-Jaccard >= GUARD); otherwise
the W-ID is corrupted (e.g. the chemistry/theology false-positives) and we reject it.

Merges with the pooled title-based result (05) so every study gets the best available
authoritative DOI. Output: tier_a_resolved_final.json + report.
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import defaultdict, Counter

HERE = Path(__file__).parent
PRIOR = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs/old-age-security-pension-crowdout-prioritized.json")
POOLED = HERE / "tier_a_authoritative.json"   # output of step 05 (title-based)
OUT = HERE / "tier_a_resolved_final.json"
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.60
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with"}

def toks(t):
    t = re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())
    return {w for w in t.split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0

def oa_id(wid):
    cf = CACHE / f"oaid_{wid}.json"
    if cf.exists(): return json.load(open(cf))
    url=f"https://api.openalex.org/works/{wid}?mailto={MAILTO}"
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                      "-A",f"fertility-review/1.0 (mailto:{MAILTO})",url],
                     capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n")
    data={"_http":code}
    if code=="200":
        try: data=json.loads(re.sub(r"[\x00-\x1f]"," ",body)); data["_http"]="200"
        except Exception: data={"_http":"PARSE_ERR"}
    json.dump(data,open(cf,"w")); time.sleep(0.8)
    return data

def norm_key(t):
    return tuple(sorted(toks(t)))

def main():
    # build: study canonical_title -> set of member on-disk W-IDs (from the 43 core records)
    prior = json.load(open(PRIOR))
    core = [p for p in prior["papers"] if p.get("evidenceType")==4 and p.get("identification")==3]
    title_to_wids = defaultdict(set)
    for p in core:
        pid = p.get("paperId","")
        if pid.startswith("W"):
            title_to_wids[norm_key(p["title"])].add(pid)

    studies = json.load(open(POOLED))
    for s in studies:
        # gather member W-IDs by matching member_titles
        wids=set()
        for mt in s.get("member_titles",[s["canonical_title"]]):
            wids |= title_to_wids.get(norm_key(mt), set())
        s["member_wids"]=sorted(wids)
        wid_hit=None
        for wid in s["member_wids"]:
            d=oa_id(wid)
            if d.get("_http")!="200" or not d.get("id"): continue
            sim=jacc(s["canonical_title"], d.get("display_name") or "")
            if sim>=GUARD:
                wid_hit={"wid":wid,"resolved_id":d.get("id"),
                         "doi":(d.get("doi") or "").replace("https://doi.org/","") or None,
                         "title":d.get("display_name"),"sim":round(sim,3),
                         "year":d.get("publication_year")}
                break
        s["wid_resolution"]=wid_hit or {"status":"no clean W-ID match"}

        # choose final authoritative DOI: prefer a W-ID-confirmed DOI, else the pooled title DOI
        final_doi=None; final_src=None
        if wid_hit and wid_hit["doi"]:
            final_doi=wid_hit["doi"]; final_src="wid"
        elif s.get("authoritative_doi"):
            final_doi=s["authoritative_doi"]; final_src=s["authoritative"]["src"]
        s["final_doi"]=final_doi
        s["final_doi_source"]=final_src or ("wid-no-doi" if wid_hit else "UNRESOLVED")

    json.dump(studies, open(OUT,"w"), indent=2)

    have=sum(1 for s in studies if s["final_doi"])
    src=Counter(s["final_doi_source"] for s in studies)
    print(f"FINAL: studies with authoritative DOI: {have}/{len(studies)}", file=sys.stderr)
    print("by source:", dict(src), file=sys.stderr)
    print("\n=== still UNRESOLVED after W-ID path ===", file=sys.stderr)
    for s in studies:
        if not s["final_doi"]:
            print(f"  [{s['year']}] {s['canonical_title'][:62]}  (wids={s['member_wids']})", file=sys.stderr)
    print(f"\nwritten -> {OUT}", file=sys.stderr)

if __name__=="__main__":
    main()
