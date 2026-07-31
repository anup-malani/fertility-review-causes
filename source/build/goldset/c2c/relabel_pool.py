#!/usr/bin/env python3
"""Re-apply the corrected relevance filter to the existing C.2.c pool and rewrite the Tier-B frame.

Run after fixing the HOUS regex. No re-pull needed -- relabelling only, since the correction is in
the classifier and not in the retrieved records.
"""
import json
import re

POOL = "literature/search-logs/housing-costs-snowball-pool.json"
FRAME = "literature/search-logs/housing-costs-tier-b-frame.json"

HOUS = re.compile(r"\bhous(?!ehold)|\bhome|\brent|\bmortgag|\bpropert|\bdwell|\breal estate|\bresiden|\bapartment|\bland price", re.I)
FERT = re.compile(r"fertil|birth|babie|baby|natal|reproduc|childbear|family size|family formation|parenthood", re.I)
PULLED = {1: 693, 2: 842, 3: 580, 4: 7840}

recs = json.load(open(POOL))
before = sum(1 for r in recs if r["provisional_relevance"] == "RELEVANT_CANDIDATE")
for r in recs:
    t = r["title"] or ""
    r["provisional_relevance"] = "RELEVANT_CANDIDATE" if (HOUS.search(t) and FERT.search(t)) else "OFF_OR_UNCERTAIN"
json.dump(recs, open(POOL, "w"), indent=1)

frame = [r for r in recs if r["provisional_relevance"] == "RELEVANT_CANDIDATE"]
for r in frame:
    r.setdefault("tier_b_status", "candidate_unscreened")
json.dump(frame, open(FRAME, "w"), indent=1)

print(f"frame: {before} -> {len(frame)}  ({before - len(frame)} false positives removed)")
print("\nround  pulled  new core  per 50   vs floor 1.0")
for rnd in sorted(PULLED):
    n = sum(1 for r in frame if r["first_found_round"] == rnd)
    per = n / PULLED[rnd] * 50
    print(f"  {rnd}    {PULLED[rnd]:>5}   {n:>6}   {per:>5.2f}   {'ABOVE' if per >= 1 else 'BELOW'}")
