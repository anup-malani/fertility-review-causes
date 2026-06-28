#!/usr/bin/env python3
"""
Tier-A gold set, step 1a: extract the strong-identification empirical core from the
PI on-disk prioritized corpus and deduplicate working-paper -> published clusters into
DISTINCT studies.

Input : literature/search-logs/old-age-security-pension-crowdout-prioritized.json
Output: scratchpad/goldset/tier_a_empirical_clusters.json
        (one record per DISTINCT study; member DOIs/titles retained for audit + recall match)

Design notes:
- "Strong-identification empirical" = evidenceType==4 AND identification==3 (the on-disk
  scoring; this is exactly one 43-record set -- see method doc).
- DOI-keyed per spec. Canonical DOI = version-of-record preference:
  published journal DOI > SSRN (10.2139) / NBER (10.3386) / WB (10.1596) working-paper DOI.
- Recall-match should credit a hit on ANY member DOI, so all member DOIs are kept.
- Near-identical titles (e.g. "Bismarck's" vs "Bismarck") are clustered by a normalized
  token-set key; clusters with >1 member are emitted for human confirmation, never
  silently dropped.
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

REPO = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SRC = REPO / "literature/search-logs/old-age-security-pension-crowdout-prioritized.json"
OUT = Path(__file__).parent / "tier_a_empirical_clusters.json"

STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new"}

def norm_title(t):
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)          # strip punctuation incl. apostrophes
    toks = [w for w in t.split() if w not in STOP]
    return tuple(sorted(toks))                    # token-set: order- & stopword-invariant

def is_working_paper_doi(doi):
    if not doi: return True
    return doi.startswith(("10.2139/ssrn", "10.3386/w", "10.1596/"))

def canonical(records):
    """Pick version-of-record: prefer a published (non-working-paper) DOI, else any DOI, else none."""
    pub = [r for r in records if r.get("doi") and not is_working_paper_doi(r["doi"])]
    pool = pub or [r for r in records if r.get("doi")] or records
    # tie-break: highest compositeScore, then most recent year
    pool.sort(key=lambda r: (r.get("compositeScore") or 0, r.get("year") or 0), reverse=True)
    return pool[0]

def main():
    d = json.load(open(SRC))
    core = [p for p in d["papers"] if p.get("evidenceType")==4 and p.get("identification")==3]
    print(f"strong-ID empirical records: {len(core)}", file=sys.stderr)

    clusters = defaultdict(list)
    for p in core:
        clusters[norm_title(p["title"])].append(p)

    # --- fuzzy second pass: merge near-identical title keys (e.g. "Bismarck's" vs "Bismarck") ---
    # token Jaccard; auto-merge >= 0.80, print [0.60,1.0) for human audit.
    keys = list(clusters.keys())
    def jacc(a, b):
        sa, sb = set(a), set(b)
        return len(sa & sb) / len(sa | sb) if (sa | sb) else 0.0
    merged_into = {}
    print("\n=== fuzzy near-dup audit (token Jaccard in [0.60,1.0)) ===", file=sys.stderr)
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            ki, kj = keys[i], keys[j]
            if ki in merged_into or kj in merged_into:
                continue
            s = jacc(ki, kj)
            if 0.60 <= s < 1.0:
                ti = clusters[ki][0]["title"]; tj = clusters[kj][0]["title"]
                action = "AUTO-MERGE" if s >= 0.80 else "review-only"
                print(f"  J={s:.2f} {action}", file=sys.stderr)
                print(f"        · {ti}", file=sys.stderr)
                print(f"        · {tj}", file=sys.stderr)
                if s >= 0.80:
                    clusters[ki].extend(clusters[kj])
                    merged_into[kj] = ki
    for k in merged_into:
        del clusters[k]

    studies = []
    for key, recs in clusters.items():
        can = canonical(recs)
        member_dois = sorted({r["doi"] for r in recs if r.get("doi")})
        studies.append({
            "canonical_title": can["title"],
            "canonical_doi": can.get("doi"),            # may be None -> needs resolution (step 1b)
            "year": can.get("year"),
            "member_dois": member_dois,
            "n_records": len(recs),
            "member_titles": sorted({r["title"] for r in recs}),
            "needs_doi_resolution": not bool(can.get("doi")),
            "stratum": None,                            # filled in step 1c
            "provenance_tier": "A",
            "source": "on-disk-44",
        })

    studies.sort(key=lambda s: (s["year"] or 0))
    json.dump(studies, open(OUT, "w"), indent=2)

    n_multi = sum(1 for s in studies if s["n_records"] > 1)
    n_nodoi = sum(1 for s in studies if s["needs_doi_resolution"])
    print(f"distinct studies: {len(studies)}  (collapsed from {len(core)})", file=sys.stderr)
    print(f"  clusters with >1 record (confirm): {n_multi}", file=sys.stderr)
    print(f"  studies still needing a DOI: {n_nodoi}", file=sys.stderr)
    print(f"written -> {OUT}", file=sys.stderr)

    print("\n=== multi-record clusters (human confirm) ===", file=sys.stderr)
    for s in studies:
        if s["n_records"] > 1:
            print(f"  [{s['year']}] x{s['n_records']} -> canonical {s['canonical_doi']}", file=sys.stderr)
            for t in s["member_titles"]:
                print(f"        · {t}", file=sys.stderr)
            for dd in s["member_dois"]:
                print(f"        doi: {dd}", file=sys.stderr)

if __name__ == "__main__":
    main()
