#!/usr/bin/env python3
"""Normalized-title dedup of the C.2.c Tier-B frame.

DOI-keyed dedup cannot catch this literature's duplicates: NBER, SSRN and OSF preprints carry
genuinely different DOIs from the published article, and OpenAlex splits citation counts across the
versions. See the snowball log §5 -- the Dettling & Kearney JPubE record shows cited_by 0 while its
NBER twin shows 67.

Survivor rule: published journal article beats working paper / preprint / report; then a real
publisher DOI beats an SSRN/NBER/OSF/RePEc one; then higher citation count; then earlier year
(the published version is usually later, but citations already broke the tie).

Exact normalized-title collisions are merged automatically. Near-duplicates -- same first 55
characters, different full title, typically a subtitle variant like "... Evidence from the Housing
Market" vs "... Evidence from the Housing Market Boom and Bust" -- are NOT merged. They are written
to a review file, because collapsing them automatically would silently drop genuinely distinct
papers that share an opening clause.
"""
import json
import re
from collections import defaultdict

FRAME = "literature/search-logs/housing-costs-tier-b-frame.json"
OUT = "literature/search-logs/housing-costs-tier-b-frame-deduped.json"
REVIEW = "literature/search-logs/housing-costs-dedup-review.json"

PREPRINT_PREFIX = ("10.2139", "10.3386", "10.31235", "10.31219", "10.4054/mpidr", "10.21203")
TYPE_RANK = {"article": 0, "book-chapter": 1, "conference-paper": 2, "report": 3, "preprint": 4,
             "dataset": 5, "other": 6}


def rank(r):
    return (
        TYPE_RANK.get(r.get("type") or "other", 6),
        1 if (not r["doi"] or r["doi"].startswith(PREPRINT_PREFIX)) else 0,
        -(r.get("cited_by") or 0),
    )


frame = json.load(open(FRAME))
groups = defaultdict(list)
for r in frame:
    groups[r["norm_title"]].append(r)

survivors, merged_log = [], []
for key, rows in groups.items():
    rows.sort(key=rank)
    keep, drop = rows[0], rows[1:]
    if drop:
        keep = dict(keep)
        keep["merged_duplicates"] = [
            {"doi": d["doi"], "type": d["type"], "venue": d["venue"], "cited_by": d["cited_by"]}
            for d in drop
        ]
        keep["cited_by_merged"] = max(r.get("cited_by") or 0 for r in rows)
        merged_log.append({"norm_title": key, "kept": keep["doi"] or keep["openalex"],
                           "kept_type": keep["type"],
                           "dropped": [d["doi"] or d["openalex"] for d in drop]})
    survivors.append(keep)

# near-duplicate detection: same 55-char prefix, different normalized title
byprefix = defaultdict(list)
for r in survivors:
    byprefix[r["norm_title"][:55]].append(r)
near = [{"prefix": p,
         "candidates": [{"doi": x["doi"], "year": x["year"], "title": x["title"],
                         "venue": x["venue"], "type": x["type"]} for x in rows]}
        for p, rows in byprefix.items() if len(rows) > 1]

survivors.sort(key=lambda r: -(r.get("cited_by_merged") or r.get("cited_by") or 0))
json.dump(survivors, open(OUT, "w"), indent=1)
json.dump({"auto_merged": merged_log, "near_duplicates_for_review": near},
          open(REVIEW, "w"), indent=1)

print(f"frame in            : {len(frame)}")
print(f"exact-title groups  : {len(groups)}  ({len(merged_log)} had duplicates)")
print(f"frame out (deduped) : {len(survivors)}")
print(f"records removed     : {len(frame) - len(survivors)}")
print(f"near-dup groups flagged for review (NOT merged): {len(near)}")
print()
pre = sum(1 for r in survivors if r["doi"].startswith(PREPRINT_PREFIX) or not r["doi"])
print(f"survivors still preprint-only or DOI-less: {pre}")
for m in merged_log[:8]:
    print(f"  kept {m['kept']:<34} ({m['kept_type']}) <- {', '.join(m['dropped'])[:70]}")
