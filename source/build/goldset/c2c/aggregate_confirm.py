#!/usr/bin/env python3
"""Fold the C.2.c confirming round (round 4) into the merged pool and score the stop test.

The confirming round pulls a flat backward-ref list and a flat forward-citation stream rather than
per-seed files, so it needs its own reader. Everything else -- relevance regex, dedup key, pool
schema -- matches aggregate_rounds.py so the round-4 row is commensurable with rounds 1-3.
"""
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

MAILTO = "shravanh@uchicago.edu"
CONFIRM_DIR = sys.argv[1]
ROUND = int(os.environ.get("ROUND", "4"))  # set ROUND=N for successive mechanical rounds
POOL = "literature/search-logs/housing-costs-snowball-pool.json"
FRAME = "literature/search-logs/housing-costs-tier-b-frame.json"

# NB: bare "hous"/"rent" matched household, parent, current, different -- 58% false positives.
# Word boundaries + a household negative-lookahead are load-bearing, not cosmetic.
HOUS = re.compile(r"\bhous(?!ehold)|\bhome|\brent|\bmortgag|\bpropert|\bdwell|\breal estate|\bresiden|\bapartment|\bland price", re.I)
FERT = re.compile(r"fertil|birth|babie|baby|natal|reproduc|childbear|family size|family formation|parenthood", re.I)


def norm_title(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def is_core(title):
    return bool(HOUS.search(title or "") and FERT.search(title or ""))


def curl_json(args):
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-G",
                        "https://api.openalex.org/works"] + args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"results": []}


existing = json.load(open(POOL))
known = {r["openalex"] for r in existing}

# ---- forward citations from the confirming sweep ----
fwd = {}
fpath = os.path.join(CONFIRM_DIR, "fwd_all.jsonl")
if os.path.exists(fpath):
    for line in open(fpath):
        line = line.strip()
        if not line:
            continue
        try:
            blk = json.loads(line)
        except Exception:
            continue
        for w in blk.get("results", []):
            fwd[w["id"].rsplit("/", 1)[-1]] = w

# ---- backward refs ----
back_ids = set()
bpath = os.path.join(CONFIRM_DIR, "backrefs_all.txt")
if os.path.exists(bpath):
    back_ids = {ln.strip() for ln in open(bpath) if ln.strip()}

pulled_unique = set(fwd) | back_ids
new_ids = pulled_unique - known
print(f"confirming round: {len(pulled_unique)} unique records pulled, {len(new_ids)} not already in pool")

# ---- metadata for new backward-only ids ----
need = [k for k in new_ids if k not in fwd]
print(f"fetching metadata for {len(need)} new backward refs...")
meta = {}
for i in range(0, len(need), 50):
    data = curl_json(["--data-urlencode", "filter=openalex_id:" + "|".join(need[i:i + 50]),
                      "--data-urlencode", "per-page=50", "--data-urlencode", "mailto=" + MAILTO,
                      "--data-urlencode",
                      "select=id,doi,title,publication_year,type,cited_by_count,primary_location"])
    for w in data.get("results", []):
        meta[w["id"].rsplit("/", 1)[-1]] = w
    if (i // 50) % 20 == 0:
        print(f"  ...{i}/{len(need)}")

new_core = 0
for k in new_ids:
    w = fwd.get(k) or meta.get(k)
    if not w:
        continue
    title = w.get("title") or ""
    existing.append({
        "openalex": k, "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": title, "norm_title": norm_title(title),
        "year": w.get("publication_year"), "type": w.get("type"),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
        "cited_by": w.get("cited_by_count") or 0,
        "seeds_backward": [], "seeds_forward": [], "n_seeds": 0,
        "first_found_round": ROUND,
        "provisional_relevance": "RELEVANT_CANDIDATE" if is_core(title) else "OFF_OR_UNCERTAIN",
    })
    if is_core(title):
        new_core += 1

existing.sort(key=lambda r: (-r["n_seeds"], -r["cited_by"]))
json.dump(existing, open(POOL, "w"), indent=1)
frame = [r for r in existing if r["provisional_relevance"] == "RELEVANT_CANDIDATE"]
for r in frame:
    r.setdefault("tier_b_status", "candidate_unscreened")
json.dump(frame, open(FRAME, "w"), indent=1)

pulled = len(pulled_unique)
per50 = new_core / pulled * 50 if pulled else 0
overlap = 1 - len(new_ids) / pulled if pulled else 0
print(f"\n=== ROUND {ROUND} (mechanical confirming round) ===")
print(f"  pulled (unique)      : {pulled}")
print(f"  new unique           : {len(new_ids)}")
print(f"  new relevant (core)  : {new_core}")
print(f"  new core per 50      : {per50:.2f}   floor = 1.00   -> {'ABOVE' if per50 >= 1 else 'BELOW'}")
print(f"  overlap rate         : {overlap:.0%}")
print(f"\nmerged pool: {len(existing)}   Tier-B frame: {len(frame)}")
