#!/usr/bin/env python3
"""
217 — A.23 citation snowball (channel 3), round 1.

TICK-075. Builds the orthogonal Tier-B frame by snowballing backward (references)
and forward (citations) from the 30 anchors that cleared the existence gate in 216.

Channel 1 came back dry for this hypothesis — no prior review exists — so this
channel carries more of the recall burden than it usually does, and the frame it
produces is the main thing the production query will be scored against.

Two rules the design follows:

  * DECOYS ARE SEEDED, forward as well as backward. The standing lesson is that
    refusing to forward-seed a decoy discards the best channel: measured decoy
    clouds have run 29-88% on-topic against 1-14% for a theory canon. A decoy sits
    on a boundary, and the works around it are the boundary cases the screen most
    needs to see. Provenance is tagged so the split stays visible.
  * BOTH CONFIGURATIONS are seeded (Ruling 1). The pre-launch and extended-household
    anchors are tagged separately so the frame's balance between them can be read
    off the output rather than assumed.

Dedup is by folded title, and the PUBLISHED version survives a preprint pair.
Records with no DOI are kept but flagged: they are candidates, not citations to
trust, and the OAS run that found ~40% of a frozen Tier B was fabricated is why.

Usage: python3 source/build/goldset/217_a23_snowball.py
"""
import json
import re
import subprocess
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
ANCHORS = LOGS / "co-residence-parents-household-delay-cold-start-anchors.json"
OUT_POOL = LOGS / "co-residence-parents-household-delay-snowball-pool.json"
OUT_LOG = LOGS / "co-residence-parents-household-delay-snowball-round1.json"
API = "https://api.openalex.org/works"

FORWARD_CAP = 200          # per seed, highest-cited first
SELECT = ("id,doi,title,publication_year,type,cited_by_count,primary_location,"
          "authorships,referenced_works")

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def fold(s):
    """Accent-tolerant fold that transliterates. Never maps a letter to a space."""
    if not s:
        return ""
    s = s.lower()
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "150", "--get", API]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}"
            time.sleep(5 * (attempt + 1))
            continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            last = "parse"
            time.sleep(5 * (attempt + 1))
            continue
        if "error" in d:
            last = str(d["error"])[:60]
            time.sleep(10 * (attempt + 1))
            continue
        return d, None
    return None, last


def shape(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    return {
        "openalex": w["id"].rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "title": w.get("title"),
        "norm_title": fold(w.get("title")),
        "year": w.get("publication_year"),
        "type": w.get("type"),
        "venue": src.get("display_name"),
        "cited_by": w.get("cited_by_count"),
        "authors": "; ".join(a["author"]["display_name"]
                             for a in (w.get("authorships") or [])[:4]),
    }


def main():
    anchors = json.loads(ANCHORS.read_text())["anchors"]
    seeds, errors = [], {}

    # --- resolve each anchor DOI to an OpenAlex work -------------------------
    print(f"resolving {len(anchors)} anchors to OpenAlex...")
    for a in anchors:
        d, err = get([("filter", f"doi:{a['doi']}"), ("per-page", "1"), ("select", SELECT)])
        if err or not d.get("results"):
            errors[f"resolve:{a['doi']}"] = err or "no_openalex_record"
            print(f"  UNRESOLVED  {a['doi']}")
            continue
        w = d["results"][0]
        seeds.append({
            "doi": a["doi"], "openalex": w["id"].rsplit("/", 1)[-1],
            "title": w.get("title"),
            "cell": a["provisional_cell"],
            "is_decoy": a["provenance_channel"] == "decoy",
            "refs": w.get("referenced_works") or [],
        })
    print(f"  resolved {len(seeds)}/{len(anchors)}\n")

    pool = {}
    back_ids = defaultdict(set)   # openalex id -> seed dois that reference it

    # --- backward: hydrate the union of referenced_works ---------------------
    all_refs = sorted({r.rsplit("/", 1)[-1] for s in seeds for r in s["refs"]})
    for s in seeds:
        for r in s["refs"]:
            back_ids[r.rsplit("/", 1)[-1]].add(s["doi"])
    print(f"backward: {len(all_refs)} distinct referenced works to hydrate")
    for i in range(0, len(all_refs), 50):
        batch = all_refs[i:i + 50]
        d, err = get([("filter", "openalex_id:" + "|".join(batch)),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            errors[f"backward:{i}"] = err
            continue
        for w in d.get("results", []):
            rec = shape(w)
            rec.update({"seeds_backward": sorted(back_ids.get(rec["openalex"], [])),
                        "seeds_forward": [], "first_found_round": 1})
            pool[rec["openalex"]] = rec
        print(f"  hydrated {min(i+50, len(all_refs))}/{len(all_refs)}")

    # --- forward: works citing each seed -------------------------------------
    print(f"\nforward: citations of {len(seeds)} seeds (cap {FORWARD_CAP} each)")
    for s in seeds:
        d, err = get([("filter", f"cites:{s['openalex']}"),
                      ("per-page", str(FORWARD_CAP)),
                      ("sort", "cited_by_count:desc"), ("select", SELECT)])
        if err:
            errors[f"forward:{s['doi']}"] = err
            print(f"  FAILED  {s['doi']}")
            continue
        n = d["meta"]["count"]
        for w in d.get("results", []):
            rec = pool.get(w["id"].rsplit("/", 1)[-1])
            if rec is None:
                rec = shape(w)
                rec.update({"seeds_backward": [], "seeds_forward": [], "first_found_round": 1})
                pool[rec["openalex"]] = rec
            if s["doi"] not in rec["seeds_forward"]:
                rec["seeds_forward"].append(s["doi"])
        capped = " CAPPED" if n > FORWARD_CAP else ""
        print(f"  {min(n, FORWARD_CAP):4d}/{n:5d}{capped:7s} {s['doi']}")

    # --- dedup by folded title; the PUBLISHED version survives ---------------
    by_title = defaultdict(list)
    for rec in pool.values():
        if rec["norm_title"]:
            by_title[rec["norm_title"]].append(rec)
    dropped = []
    for norm, group in by_title.items():
        if len(group) < 2:
            continue
        group.sort(key=lambda r: (r["doi"] is None,
                                  "preprint" in (r["type"] or ""),
                                  -(r["cited_by"] or 0)))
        keeper = group[0]
        for loser in group[1:]:
            keeper["seeds_backward"] = sorted(set(keeper["seeds_backward"]) | set(loser["seeds_backward"]))
            keeper["seeds_forward"] = sorted(set(keeper["seeds_forward"]) | set(loser["seeds_forward"]))
            dropped.append({"dropped": loser["openalex"], "kept": keeper["openalex"],
                            "title": loser["title"], "reason": "normalized-title duplicate"})
            pool.pop(loser["openalex"], None)

    records = list(pool.values())
    for r in records:
        r["n_seeds"] = len(r["seeds_backward"]) + len(r["seeds_forward"])
        r["no_doi_flag"] = r["doi"] is None
    records.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by"] or 0)))

    seeded_by_decoy = {s["doi"] for s in seeds if s["is_decoy"]}
    only_decoy = sum(1 for r in records
                     if set(r["seeds_backward"] + r["seeds_forward"]) <= seeded_by_decoy
                     and r["n_seeds"] > 0)
    cells = defaultdict(int)
    for s in seeds:
        cells[s["cell"]] += 1

    log = {
        "meta": {
            "ticket": "TICK-075", "round": 1,
            "seeds_requested": len(anchors), "seeds_resolved": len(seeds),
            "seed_cells": dict(cells),
            "forward_cap_per_seed": FORWARD_CAP,
            "pool_size": len(records),
            "reached_only_via_decoy_seeds": only_decoy,
            "no_doi": sum(1 for r in records if r["no_doi_flag"]),
            "preprints": sum(1 for r in records if "preprint" in (r["type"] or "")),
            "multi_seed": sum(1 for r in records if r["n_seeds"] >= 2),
            "duplicates_collapsed": len(dropped),
            "errors": len(errors),
            "note": "Pool is candidates, not a frame. Nothing here has been screened.",
        },
        "duplicates_collapsed": dropped,
        "errors": errors,
    }
    OUT_POOL.write_text(json.dumps(records, indent=1))
    OUT_LOG.write_text(json.dumps(log, indent=1))
    print("\n" + json.dumps(log["meta"], indent=1))
    print(f"wrote {OUT_POOL.relative_to(ROOT)} and {OUT_LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
