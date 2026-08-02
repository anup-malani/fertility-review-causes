#!/usr/bin/env python3
"""Fetch abstracts for the C.2.c Tier-B frame so the screen is not title-only.

Title-only screening cannot decide C.2.c's routing questions. "Housing and Fertility" does not say
whether the treatment is a price, a tenure status, or a housing expenditure -- and price-vs-tenure is
the whole boundary the 2026-07-31 ruling turns on. Abstracts do not fully resolve it either (the scope
doc is clear that tenure conditioning and tempo-vs-quantum are usually full-text facts), but they move
a large share of the UNCERTAIN pile.

OpenAlex stores abstracts as an inverted index; reconstruct to plain text.
Per GACS D2a, a paper with no abstract is NOT dropped -- it is flagged `no_abstract` and carried to
the screen on its title, exactly as the D.3.b INSUFFICIENT_INFO stratum was.
"""
import json
import subprocess
import sys

FRAME = "literature/search-logs/housing-costs-prescreen.json"
OUT = "literature/search-logs/housing-costs-frame-abstracts.json"
MAILTO = "shravanh@uchicago.edu"


def deinvert(idx):
    if not idx:
        return ""
    pos = [(p, w) for w, ps in idx.items() for p in ps]
    pos.sort()
    return " ".join(w for _, w in pos)


frame = json.load(open(FRAME))
ids = [r["openalex"] for r in frame]
abstracts = {}

for i in range(0, len(ids), 50):
    batch = ids[i:i + 50]
    r = subprocess.run(
        ["curl", "-s", "--max-time", "60", "-G", "https://api.openalex.org/works",
         "--data-urlencode", "filter=openalex_id:" + "|".join(batch),
         "--data-urlencode", "per-page=50",
         "--data-urlencode", "mailto=" + MAILTO,
         "--data-urlencode", "select=id,abstract_inverted_index"],
        capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except Exception:
        print(f"  batch {i} failed", file=sys.stderr)
        continue
    for w in data.get("results", []):
        abstracts[w["id"].rsplit("/", 1)[-1]] = deinvert(w.get("abstract_inverted_index"))
    print(f"  ...{min(i + 50, len(ids))}/{len(ids)}", file=sys.stderr)

n_with = 0
for r in frame:
    a = abstracts.get(r["openalex"], "")
    r["abstract"] = a
    r["has_abstract"] = bool(a and len(a) > 80)
    n_with += r["has_abstract"]

json.dump(frame, open(OUT, "w"), indent=1)
print(f"\nframe: {len(frame)}")
print(f"with usable abstract (>80 chars): {n_with} ({n_with / len(frame):.0%})")
print(f"no abstract -- carried on title, flagged: {len(frame) - n_with}")
unc = [r for r in frame if r["prescreen_rule"] == "unmatched"]
print(f"\nof the {len(unc)} UNCERTAIN records, {sum(1 for r in unc if r['has_abstract'])} now have an abstract")
