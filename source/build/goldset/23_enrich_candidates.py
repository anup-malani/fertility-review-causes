#!/usr/bin/env python3
"""
Step 23 - Assemble the T1uT2 meta-analysis CANDIDATE set and enrich it from OpenAlex.

Task-B / GACS output stage (E), run on the OAS pilot via the legacy-migration path:
the meta-analysis-ready subset = (T1 u T2) n empirical-meeting-evidence-bar (ET>=2).
T1uT2 = 1,209 papers; 474 already carry Sonnet evidence scores (Anup's prioritized.json),
735 do not and must be scored in step 24. Abstracts for the 735 are not on disk, so we do
ONE OpenAlex pass over the whole candidate set to pull, per work:
  - abstract_inverted_index  -> reconstructed abstract (feeds step 24 Sonnet scoring)
  - doi                      -> fresh DOI (feeds step 26 DOI resolution, C3 production)
  - best_oa_location/open_access/primary_location -> OA pdf urls (feeds step 27 PDF fetch)
  - authorships              -> author surnames (C2 author+year gate; DOI-list citation)
  - publication_year, display_name
Dead/drifted W-IDs (this corpus has ~40% W-ID rot) are recorded, not trusted: a title
guard (Jaccard) flags drift exactly as in 10_wid_refetch.py.

Reuses the cache/budget/curl/guard machinery of 10_wid_refetch.py (project-level cache dir,
resumable, polite mailto, tolerant of the OpenAlex daily-budget 404 mode).

Inputs : ../../.. /literature/search-logs/{slug}-{tiers,prioritized}.json
Outputs: {slug}-metaanalysis-candidates.json   (1,209 candidate records + provenance + scored flag)
         {slug}-oa-enrichment.json             (paperId -> {doi,title,year,abstract,authors,oa_urls,status})
         (stderr) coverage + W-ID rot report
"""
import json, re, time, hashlib, subprocess, sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
SL = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
SLUG = "old-age-security-pension-crowdout"
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.5  # title-Jaccard drift guard, same threshold as 10_wid_refetch.py
SELECT = "id,display_name,publication_year,doi,abstract_inverted_index,authorships,best_oa_location,open_access,primary_location"

STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}
def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]", " ", (t or "").lower()).split() if w not in STOP}
def jacc(a, b):
    A, B = toks(a), toks(b); return len(A & B) / len(A | B) if (A | B) else 0.0

def curl(url):
    r = subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","40",
                        "-A",f"fr/1.0 (mailto:{MAILTO})",url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    if code == "200":
        try: return json.loads(re.sub(r"[\x00-\x1f]", " ", body))
        except Exception: return None
    return None

def wid_of(work): return (work.get("id") or "").rsplit("/", 1)[-1]

def deinvert(inv):
    """abstract_inverted_index {token:[positions]} -> plain text."""
    if not inv: return None
    pos = {}
    for tok, idxs in inv.items():
        for i in idxs: pos[i] = tok
    if not pos: return None
    return " ".join(pos[i] for i in sorted(pos))[:4000]

def oa_urls(w):
    urls = []
    for loc in (w.get("best_oa_location"), w.get("primary_location")):
        if loc and loc.get("pdf_url"): urls.append(loc["pdf_url"])
    oa = w.get("open_access") or {}
    if oa.get("oa_url"): urls.append(oa["oa_url"])
    seen, out = set(), []
    for u in urls:
        if u not in seen: seen.add(u); out.append(u)
    return out

def surnames(w):
    out = []
    for a in (w.get("authorships") or [])[:12]:
        nm = ((a.get("author") or {}).get("display_name") or "").strip()
        if nm: out.append(nm.split()[-1])
    return out

def fetch(wids):
    """W-ID -> full enrichment dict. Batched ids.openalex filter + single-lookup fallback."""
    raw = {}
    wl = list(wids)
    for i in range(0, len(wl), 50):
        chunk = wl[i:i+50]
        ck = CACHE / f"oaenrich_{hashlib.sha1('|'.join(chunk).encode()).hexdigest()[:16]}.json"
        if ck.exists():
            data = json.load(open(ck))
        else:
            url = (f"https://api.openalex.org/works?filter=ids.openalex:{'|'.join(chunk)}"
                   f"&select={SELECT}&per-page=50&mailto={MAILTO}")
            data = curl(url) or {"results": []}
            json.dump(data, open(ck, "w")); time.sleep(1.0)
        for w in data.get("results", []):
            raw[wid_of(w)] = w
        print(f"  batch {i//50+1}/{(len(wl)+49)//50}: cumulative {len(raw)} resolved", file=sys.stderr)
    missing = [w for w in wids if w not in raw]
    print(f"  single-lookup fallback for {len(missing)} (merged/missing)", file=sys.stderr)
    for w in missing:
        cf = CACHE / f"oaenrich1_{w}.json"
        if cf.exists(): d = json.load(open(cf))
        else:
            d = curl(f"https://api.openalex.org/works/{w}?select={SELECT}&mailto={MAILTO}") or {"_http":"404"}
            json.dump(d, open(cf, "w")); time.sleep(0.7)
        if d.get("id"): raw[w] = d
    return raw

def main():
    tiers = json.load(open(SL / f"{SLUG}-tiers.json"))
    prio = {p["paperId"]: p for p in json.load(open(SL / f"{SLUG}-prioritized.json"))["papers"]}

    cands = [t for t in tiers if t["tier"] in (1, 2)]
    wids = {c["paperId"] for c in cands if (c.get("paperId") or "").startswith("W")}
    print(f"T1uT2 candidates: {len(cands)} ({len(wids)} W-IDs) | already scored: "
          f"{sum(1 for c in cands if c['paperId'] in prio)} | to-score: "
          f"{sum(1 for c in cands if c['paperId'] not in prio)}", file=sys.stderr)

    print(f"OpenAlex enrichment pass over {len(wids)} W-IDs...", file=sys.stderr)
    raw = fetch(wids)

    enrich = {}; cnt = Counter()
    for c in cands:
        pid = c["paperId"]; disk_title = c.get("title", "")
        w = raw.get(pid)
        if not pid.startswith("W"):
            status = "NO_WID"
        elif not w:
            status = "WID_404"
        else:
            sim = jacc(disk_title, w.get("display_name") or "")
            status = "OK" if sim >= GUARD else "WID_DRIFT"
        cnt[status] += 1
        rec = {"paperId": pid, "disk_title": disk_title, "status": status}
        if w and status in ("OK", "WID_DRIFT"):
            rec.update({
                "oa_title": w.get("display_name"),
                "year": w.get("publication_year"),
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "abstract": deinvert(w.get("abstract_inverted_index")),
                "authors": surnames(w),
                "oa_urls": oa_urls(w),
                "title_match": round(jacc(disk_title, w.get("display_name") or ""), 3),
            })
        enrich[pid] = rec

    # candidate records carry tier/channel/verdict provenance + scored flag + abstract availability
    out = []
    for c in cands:
        pid = c["paperId"]; p = prio.get(pid); e = enrich[pid]
        out.append({
            "paperId": pid, "title": c.get("title"),
            "tier": c["tier"], "channel": c.get("channel"),
            "verdict": c.get("verdict"), "confidence": c.get("confidence"),
            "in_gold": c.get("in_gold", False),
            "compositeScore": (p or {}).get("compositeScore"),
            "evidenceType": (p or {}).get("evidenceType"),
            "identification": (p or {}).get("identification"),
            "scored": p is not None,
            "wid_status": e["status"],
            "has_abstract": bool(e.get("abstract")) or bool((p or {}).get("abstract")),
        })

    json.dump(out, open(SL / f"{SLUG}-metaanalysis-candidates.json", "w"), indent=2)
    json.dump(enrich, open(SL / f"{SLUG}-oa-enrichment.json", "w"), indent=2)

    print("\n=== W-ID enrichment status ===", file=sys.stderr)
    for k, v in cnt.most_common(): print(f"  {k}: {v}", file=sys.stderr)
    to_score = [c for c in out if not c["scored"]]
    print(f"\nto-score (735 expected): {len(to_score)} | of those with abstract: "
          f"{sum(1 for c in to_score if c['has_abstract'])} | title-only: "
          f"{sum(1 for c in to_score if not c['has_abstract'])}", file=sys.stderr)
    print(f"written -> {SLUG}-metaanalysis-candidates.json, {SLUG}-oa-enrichment.json", file=sys.stderr)

if __name__ == "__main__":
    main()
