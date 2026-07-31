#!/usr/bin/env python3
"""Merge C.2.c snowball rounds, compute marginal yield against the saturation floor."""
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

MAILTO = "shravanh@uchicago.edu"
ROUND_DIRS = sys.argv[1:]  # e.g. sb sb2

SEED_LABEL = {
    "W3024244835": "r1:dettling-kearney", "W2017790450": "r1:dettling-kearney",
    "W3037455063": "r1:daysal-etal", "W3131143603": "r1:daysal-etal",
    "W2037422701": "r1:mulder-billari",
    "W2035671284": "r1:lovenheim-mumford", "W1578574739": "r1:lovenheim-mumford",
    "W2125780906": "r2:psp-italy", "W2065377959": "r2:mulder-hoform",
    "W1509700920": "r2:nl-formation", "W2131771089": "r2:housing-family-intro",
    "W2532821622": "r2:britain-tenure", "W2099386106": "r2:delay-expensive",
    "W2129646919": "r2:family-dynamics",
}

HOUS = re.compile(r"hous|home|rent|mortgag|propert|dwell|real estate|residen|land price|apartment", re.I)
FERT = re.compile(r"fertil|birth|babie|baby|natal|reproduc|childbear|family size|family formation|parenthood", re.I)


def norm_title(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def curl_json(args):
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-G",
                        "https://api.openalex.org/works"] + args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"results": []}


def collect(d, rnd):
    """Return {wid: record} and {wid: {'backward':set,'forward':set}} for one round dir."""
    pool, chan = {}, defaultdict(lambda: {"backward": set(), "forward": set()})
    for f in glob.glob(os.path.join(d, "fwd_*.jsonl")):
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
    back = defaultdict(set)
    for f in glob.glob(os.path.join(d, "back_W*.json")):
        wid = re.search(r"back_(W\d+)\.json", f).group(1)
        label = SEED_LABEL.get(wid, wid)
        for ref in json.load(open(f)):
            back[ref.rsplit("/", 1)[-1]].add(label)
    need = [k for k in back if k not in pool]
    for i in range(0, len(need), 50):
        data = curl_json(["--data-urlencode", "filter=openalex_id:" + "|".join(need[i:i + 50]),
                          "--data-urlencode", "per-page=50", "--data-urlencode", "mailto=" + MAILTO,
                          "--data-urlencode",
                          "select=id,doi,title,publication_year,type,cited_by_count,primary_location"])
        for w in data.get("results", []):
            pool.setdefault(w["id"].rsplit("/", 1)[-1], w)
    for k, labels in back.items():
        chan[k]["backward"] |= labels
    return pool, chan


merged, mchan, first_round = {}, defaultdict(lambda: {"backward": set(), "forward": set()}), {}
stats = []
for rnd, d in enumerate(ROUND_DIRS, start=1):
    pool, chan = collect(d, rnd)
    core_new = 0
    for k, w in pool.items():
        if k not in merged:
            merged[k] = w
            first_round[k] = rnd
            if HOUS.search(w.get("title") or "") and FERT.search(w.get("title") or ""):
                core_new += 1
    for k, v in chan.items():
        mchan[k]["backward"] |= v["backward"]
        mchan[k]["forward"] |= v["forward"]
    stats.append((rnd, len(pool), sum(1 for k in pool if first_round.get(k) == rnd), core_new))

recs = []
for k, w in merged.items():
    b, f = sorted(mchan[k]["backward"]), sorted(mchan[k]["forward"])
    title = w.get("title") or ""
    recs.append({
        "openalex": k, "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": title, "norm_title": norm_title(title),
        "year": w.get("publication_year"), "type": w.get("type"),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
        "cited_by": w.get("cited_by_count") or 0,
        "seeds_backward": b, "seeds_forward": f, "n_seeds": len(set(b) | set(f)),
        "first_found_round": first_round[k],
        "provisional_relevance": "RELEVANT_CANDIDATE" if (HOUS.search(title) and FERT.search(title)) else "OFF_OR_UNCERTAIN",
    })
recs.sort(key=lambda r: (-r["n_seeds"], -r["cited_by"]))
json.dump(recs, open("literature/search-logs/housing-costs-snowball-pool.json", "w"), indent=1)
tierb = [r for r in recs if r["provisional_relevance"] == "RELEVANT_CANDIDATE"]
for r in tierb:
    r["tier_b_status"] = "candidate_unscreened"
json.dump(tierb, open("literature/search-logs/housing-costs-tier-b-frame.json", "w"), indent=1)

print("round  pulled  new_unique  new_core  new_core_per_50_pulled  vs_floor(1.0)")
for rnd, pulled, newu, core in stats:
    per50 = core / pulled * 50
    print(f"  {rnd}    {pulled:>5}   {newu:>6}    {core:>5}      {per50:>6.2f}"
          f"              {'ABOVE' if per50 >= 1 else 'BELOW'}")
print(f"\nmerged pool: {len(recs)}   Tier-B frame: {len(tierb)}")
by_norm = defaultdict(list)
for r in recs:
    by_norm[r["norm_title"]].append(r)
print(f"normalized-title duplicate groups: {sum(1 for v in by_norm.values() if len(v) > 1)}")
