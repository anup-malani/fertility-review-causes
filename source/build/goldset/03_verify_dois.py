#!/usr/bin/env python3
"""
Tier-A gold set, step 1b-verify: resolve every canonical DOI back through Crossref
(DOI -> metadata) and check the returned title matches our recorded title (Jaccard guard).
Catches corrupted/drifted DOIs BEFORE they enter the frozen gold set -- the same class of
bug as the chemistry/theology W-ID false-positives.

Input : tier_a_empirical_resolved.json
Output: tier_a_empirical_verified.json
Verdicts: VERIFIED (J>=0.60) | TITLE_MISMATCH (DOI resolves but to a different title)
          | DOI_NOT_FOUND (Crossref 404/empty) | NO_DOI (left for manual verification)
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "tier_a_empirical_resolved.json"
OUT = HERE / "tier_a_empirical_verified.json"
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

def crossref_doi(doi):
    doi = doi.replace("https://doi.org/", "").strip()
    key = hashlib.sha1(("DOI:"+doi).encode()).hexdigest()[:16]
    cf = CACHE / f"crossrefdoi_{key}.json"
    if cf.exists():
        return json.load(open(cf))
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    r = subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                        "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
                       capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    data = {"_http": code}
    if code == "200":
        try: data = json.loads(body); data["_http"] = "200"
        except Exception: data = {"_http": "PARSE_ERR"}
    json.dump(data, open(cf, "w")); time.sleep(1.0)
    return data

def main():
    studies = json.load(open(SRC))
    for s in studies:
        doi = s.get("canonical_doi")
        if not doi:
            s["verify"] = {"verdict": "NO_DOI"}
            continue
        data = crossref_doi(doi)
        if data.get("_http") != "200":
            s["verify"] = {"verdict": "DOI_NOT_FOUND", "http": data.get("_http")}
            continue
        msg = data.get("message", {})
        cand = (msg.get("title") or [""])[0]
        sim = jacc(s["canonical_title"], cand)
        s["verify"] = {
            "verdict": "VERIFIED" if sim >= GUARD else "TITLE_MISMATCH",
            "similarity": round(sim, 3),
            "crossref_title": cand,
            "crossref_container": (msg.get("container-title") or [None])[0],
        }
    json.dump(studies, open(OUT, "w"), indent=2)

    from collections import Counter
    c = Counter(s["verify"]["verdict"] for s in studies)
    print("verification verdicts:", dict(c), file=sys.stderr)
    for s in studies:
        v = s["verify"]
        if v["verdict"] in ("TITLE_MISMATCH", "DOI_NOT_FOUND"):
            print(f"\n  !! {v['verdict']}  doi={s.get('canonical_doi')}", file=sys.stderr)
            print(f"     ours    : {s['canonical_title'][:70]}", file=sys.stderr)
            if "crossref_title" in v:
                print(f"     crossref: {v['crossref_title'][:70]}  (J={v['similarity']})", file=sys.stderr)
    print(f"\nwritten -> {OUT}", file=sys.stderr)

if __name__ == "__main__":
    main()
