#!/usr/bin/env python3
"""Aggregate the C.2.c snowball into one candidate pool with channel provenance."""
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

OUT = sys.argv[1]
MAILTO = "shravanh@uchicago.edu"

SEED_LABEL = {
    "W3024244835": "dettling-kearney",
    "W3037455063": "daysal-etal",
    "W2037422701": "mulder-billari",
    "W2035671284": "lovenheim-mumford",
    "W2017790450": "dettling-kearney",      # NBER twin
    "W1578574739": "lovenheim-mumford",     # SSRN twin
    "W3131143603": "daysal-etal",           # NBER twin
}


def norm_title(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return re.split(r"\b(evidence from|the impact of the real estate)\b", t)[0].strip() or t


def curl_json(url_args):
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-G",
                        "https://api.openalex.org/works"] + url_args,
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"results": []}


pool = {}          # wid -> record
chan = defaultdict(lambda: {"backward": set(), "forward": set()})

# ---- forward citations (seeds + twins) ----
for f in glob.glob(os.path.join(OUT, "fwd_*.jsonl")):
    wid = re.search(r"fwd_(?:twin_)?(W\d+)\.jsonl", f).group(1)
    label = SEED_LABEL.get(wid, wid)
    for line in open(f):
        line = line.strip()
        if not line:
            continue
        try:
            blk = json.loads(line)
        except Exception:
            continue
        for w in blk.get("results", []):
            k = w["id"].rsplit("/", 1)[-1]
            pool.setdefault(k, w)
            chan[k]["forward"].add(label)

# ---- backward references (need metadata fetch) ----
back_ids = defaultdict(set)
for f in glob.glob(os.path.join(OUT, "back_W*.json")):
    wid = re.search(r"back_(W\d+)\.json", f).group(1)
    label = SEED_LABEL.get(wid, wid)
    for ref in json.load(open(f)):
        back_ids[ref.rsplit("/", 1)[-1]].add(label)

need = [k for k in back_ids if k not in pool]
print(f"fetching metadata for {len(need)} backward refs...", file=sys.stderr)
for i in range(0, len(need), 50):
    batch = need[i:i + 50]
    data = curl_json(["--data-urlencode", "filter=openalex_id:" + "|".join(batch),
                      "--data-urlencode", "per-page=50",
                      "--data-urlencode", "mailto=" + MAILTO,
                      "--data-urlencode",
                      "select=id,doi,title,publication_year,type,cited_by_count,primary_location"])
    for w in data.get("results", []):
        pool.setdefault(w["id"].rsplit("/", 1)[-1], w)

for k, labels in back_ids.items():
    chan[k]["backward"] |= labels

# ---- assemble ----
recs = []
for k, w in pool.items():
    b, f = sorted(chan[k]["backward"]), sorted(chan[k]["forward"])
    recs.append({
        "openalex": k,
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": w.get("title") or "",
        "norm_title": norm_title(w.get("title")),
        "year": w.get("publication_year"),
        "type": w.get("type"),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
        "cited_by": w.get("cited_by_count") or 0,
        "seeds_backward": b,
        "seeds_forward": f,
        "n_seeds": len(set(b) | set(f)),
        "channels": (["backward"] if b else []) + (["forward"] if f else []),
    })

recs.sort(key=lambda r: (-r["n_seeds"], -r["cited_by"]))
json.dump(recs, open(os.path.join(OUT, "pool.json"), "w"), indent=1)

# normalized-title duplicate groups (the preprint-twin hazard)
by_norm = defaultdict(list)
for r in recs:
    by_norm[r["norm_title"]].append(r)
dupes = {k: v for k, v in by_norm.items() if len(v) > 1}

print(f"\npool size: {len(recs)}")
print(f"  backward-only: {sum(1 for r in recs if r['channels'] == ['backward'])}")
print(f"  forward-only : {sum(1 for r in recs if r['channels'] == ['forward'])}")
print(f"  both channels: {sum(1 for r in recs if len(r['channels']) == 2)}")
print(f"  >=2 seeds    : {sum(1 for r in recs if r['n_seeds'] >= 2)}")
print(f"  no DOI       : {sum(1 for r in recs if not r['doi'])}")
print(f"  normalized-title duplicate groups: {len(dupes)} "
      f"({sum(len(v) for v in dupes.values())} records)")
