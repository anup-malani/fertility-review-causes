#!/usr/bin/env python3
"""
Step 24b - Collect + validate the parallel scoring-agent outputs into one merged file.

Reads temp/scoring/manifest.json, loads each agent's scores file, validates schema/ranges,
checks every input paperId got a score. Reports any missing/malformed batches (re-dispatch
those before proceeding). Writes {slug}-newscores.json (paperId -> score dict).

compositeScore is computed here (= ET + id + centrality), NOT trusted from the agent, to
guarantee it matches Anup's formula exactly.
"""
import json, sys
from pathlib import Path

SL = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
SC = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/temp/scoring")
SLUG = "old-age-security-pension-crowdout"

def rng(v, lo, hi): return isinstance(v, int) and lo <= v <= hi

def main():
    manifest = json.load(open(SC / "manifest.json"))
    merged = {}; problems = []
    for m in manifest:
        want = {it["paperId"] for it in json.load(open(m["input"]))}
        of = Path(m["output"])
        if not of.exists():
            problems.append(f"batch {m['batch']:02d}: OUTPUT MISSING ({of.name})"); continue
        try:
            raw = of.read_text().strip()
            if raw.startswith("```"): raw = raw.strip("`"); raw = raw[raw.find("["):raw.rfind("]")+1]
            recs = json.loads(raw)
        except Exception as e:
            problems.append(f"batch {m['batch']:02d}: PARSE ERROR {e}"); continue
        got = set()
        for r in recs:
            pid = r.get("paperId")
            if not (rng(r.get("evidenceType"),0,4) and rng(r.get("identification"),0,3) and rng(r.get("centrality"),0,3)):
                problems.append(f"batch {m['batch']:02d} {pid}: bad score ranges {r}"); continue
            merged[pid] = {
                "evidenceType": r["evidenceType"], "identification": r["identification"],
                "centrality": r["centrality"],
                "compositeScore": r["evidenceType"] + r["identification"] + r["centrality"],
                "mechanism": r.get("mechanism"), "scoreRationale": r.get("scoreRationale"),
                "scored_by": "step24-agent",
            }
            got.add(pid)
        miss = want - got
        if miss: problems.append(f"batch {m['batch']:02d}: {len(miss)} paperIds unscored e.g. {list(miss)[:3]}")

    json.dump(merged, open(SL / f"{SLUG}-newscores.json", "w"), indent=2)
    print(f"merged scores: {len(merged)}")
    if problems:
        print("\n!!! PROBLEMS (fix/re-dispatch before step 25):", file=sys.stderr)
        for p in problems: print("  " + p, file=sys.stderr)
        sys.exit(1)
    print("all batches valid, all paperIds scored.")

if __name__ == "__main__":
    main()
