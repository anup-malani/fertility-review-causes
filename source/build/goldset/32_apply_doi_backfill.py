#!/usr/bin/env python3
"""
Step 32 - Propagate DOIs backfilled during PDF acquisition (step 30, OpenAlex title-search
re-resolution of dead-WID papers) into the finalized meta-analysis set, so the DOI LIST picks
them up. Guarded: only fills records that are currently UNRESOLVED (doi_final is null) - never
overwrites a trusted DOI. The backfill source already applied the C2 J>=0.80 + year gate at
search time, so these are guarded matches; tagged as such for provenance.

After this, re-run 26c (regenerate studies + DOI list) and 31 (reconcile PDF coverage/want-list).

Input : {slug}-metaanalysis-ready-final.json, {slug}-doi-backfill.json
Output: {slug}-metaanalysis-ready-final.json (updated in place)
"""
import json, sys
from pathlib import Path

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
SLUG = "old-age-security-pension-crowdout"

def main():
    final_p = SL / f"{SLUG}-metaanalysis-ready-final.json"
    bf_p = SL / f"{SLUG}-doi-backfill.json"
    rows = json.load(open(final_p))
    backfill = json.load(open(bf_p)) if bf_p.exists() and bf_p.stat().st_size > 2 else {}
    if not backfill:
        print("no DOI backfill to apply.", file=sys.stderr); return

    applied = 0
    for r in rows:
        pid = r["paperId"]
        if not r.get("doi_final") and pid in backfill and backfill[pid]:
            r["doi_final"] = backfill[pid].replace("https://doi.org/", "").strip().lower()
            r["doi_trust"] = "openalex-search(guarded)"
            r["doi_flag"] = None
            applied += 1
            print(f"  + {r['doi_final']}  <-  {(r.get('title') or '')[:55]}", file=sys.stderr)
    json.dump(rows, open(final_p, "w"), indent=2)
    print(f"applied {applied} backfilled DOIs to {final_p.name}", file=sys.stderr)

if __name__ == "__main__":
    main()
