#!/usr/bin/env python3
"""
Step 25 - Merge evidence scores over the full T1uT2 candidate set and apply the evidence bar.

Meta-analysis-ready subset = (T1 u T2) n empirical-meeting-evidence-bar, operationalized as
evidenceType >= 2 (effect-size-able: observational econometrics, proxy/IV, or natural experiment;
excludes ET 0 qualitative and ET 1 theory). Scores come from Anup's prioritized.json (474) +
step-24 agent scores (735); compositeScore = ET + id + centrality throughout.

Also emits the theory stream (ET==1) and qualitative/other (ET==0) counts for the E2 routing
report, and flags candidates that remained unscored (should be none after step 24b).

Input : {slug}-metaanalysis-candidates.json, prioritized.json, {slug}-newscores.json, {slug}-oa-enrichment.json
Output: {slug}-metaanalysis-ready.json  (the ET>=2 set, enriched), {slug}-routing-counts.json
"""
import json, sys
from pathlib import Path
from collections import Counter

SL = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
SLUG = "old-age-security-pension-crowdout"
BAR = 4  # evidence bar: ET==4 natural/quasi-experiments only (re-scoped 2026-07-01 to the 50-80 target)

def main():
    cands = json.load(open(SL / f"{SLUG}-metaanalysis-candidates.json"))
    prio = {p["paperId"]: p for p in json.load(open(SL / f"{SLUG}-prioritized.json"))["papers"]}
    new = json.load(open(SL / f"{SLUG}-newscores.json"))
    enrich = json.load(open(SL / f"{SLUG}-oa-enrichment.json"))

    unscored = []; rows = []
    for c in cands:
        pid = c["paperId"]
        if pid in prio:
            p = prio[pid]
            et, idn, cen = p.get("evidenceType"), p.get("identification"), p.get("centrality")
            mech, rat, src = p.get("scoreRationale"), p.get("scoreRationale"), "anup-prioritized"
        elif pid in new:
            s = new[pid]
            et, idn, cen = s["evidenceType"], s["identification"], s["centrality"]
            mech, rat, src = s.get("mechanism"), s.get("scoreRationale"), s["scored_by"]
        else:
            unscored.append(pid); continue
        if et is None:
            unscored.append(pid); continue
        e = enrich.get(pid, {})
        rows.append({
            "paperId": pid, "title": c.get("title") or e.get("oa_title"),
            "authors": e.get("authors", []), "year": e.get("year"),
            "tier": c["tier"], "channel": c.get("channel"), "in_gold": c.get("in_gold", False),
            "evidenceType": et, "identification": idn, "centrality": cen,
            "compositeScore": et + idn + cen,
            "mechanism": mech, "scoreRationale": rat, "score_source": src,
            "doi": e.get("doi"), "oa_urls": e.get("oa_urls", []), "wid_status": e.get("status"),
        })

    ready = [r for r in rows if r["evidenceType"] >= BAR]
    ready.sort(key=lambda r: (r["tier"], -r["compositeScore"], -(r["evidenceType"])))
    json.dump(ready, open(SL / f"{SLUG}-metaanalysis-ready.json", "w"), indent=2)

    routing = {
        "total_T1uT2": len(cands),
        "scored": len(rows),
        "unscored_remaining": len(unscored),
        "meta_analysis_ready_ET>=2": len(ready),
        "empirical_ET4_natural_experiment": sum(1 for r in rows if r["evidenceType"] == 4),
        "empirical_ET3_proxy_iv": sum(1 for r in rows if r["evidenceType"] == 3),
        "empirical_ET2_observational": sum(1 for r in rows if r["evidenceType"] == 2),
        "theory_ET1": sum(1 for r in rows if r["evidenceType"] == 1),
        "qualitative_ET0": sum(1 for r in rows if r["evidenceType"] == 0),
        "ready_by_tier": dict(Counter(r["tier"] for r in ready)),
        "ready_gold": sum(1 for r in ready if r["in_gold"]),
        "ready_with_doi": sum(1 for r in ready if r["doi"]),
        "ready_with_oa_pdf": sum(1 for r in ready if r["oa_urls"]),
    }
    json.dump(routing, open(SL / f"{SLUG}-routing-counts.json", "w"), indent=2)
    print(json.dumps(routing, indent=2))
    if unscored:
        print(f"\n!!! {len(unscored)} candidates still unscored - rerun step 24 for them", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
