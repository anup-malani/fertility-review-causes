#!/usr/bin/env python3
"""246 — A.18 citation snowball (channels 2 and 3), round 1. TICK-076.

Builds the provenance-based pool by snowballing backward (references) and forward
(citations) from the 25 anchors resolved in 245.

Why provenance and not terms: half the naive topic query for this hypothesis is
livestock reproduction and agronomy, and the *method* vocabulary — heritability,
selection differential, breeder's equation, genetic correlation — is shared
exactly with both clouds, so nothing separates them on the exposure axis. A
term-first frame here would be dominated by dairy cattle. The standing lesson is
to label by citation provenance and use term-mining only to extend.

Design rules carried from the A.23 run:
  * Seeds are tagged by ARM (H2 / H2_MOD / SELECTION / METHOD / THEORY) so the
    frame's balance across the chapter's three synthesis arms can be read off the
    output. Ruling 2 made all three live, so an arm silently missing from the pool
    is a defect, not a preference.
  * Per-rung counts are taken BEFORE dedup as well as after. A rung that finds
    only records another rung already had is REDUNDANT, which is a different
    finding from EMPTY, and dedup-before-counting hides the difference.
  * Forward truncation is explicit. The cap sorts by citation count, so a capped
    seed contributes its high-citation head and NOT a random sample; capped seeds
    are named in the log so the bias is visible to whoever reads the frame.
  * Records with no DOI are kept but flagged. They are candidates, not citations
    to trust.

Usage: python3 source/build/goldset/246_a18_snowball.py
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
ANCHORS = LOGS / "heritability-fertility-genetic-cold-start-anchors.json"
OUT_POOL = LOGS / "heritability-fertility-genetic-snowball-pool.json"
OUT_LOG = LOGS / "heritability-fertility-genetic-snowball-round1.json"
API = "https://api.openalex.org/works"

FORWARD_CAP = 200
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
        # A refusal is JSON too, and a body with no meta is a query that never ran.
        # Never let that fall through to "no results" (245's defect).
        if "error" in d:
            last = str(d["error"])[:80]
            time.sleep(10 * (attempt + 1))
            continue
        if "meta" not in d:
            last = "no meta - query refused, NOT an empty result"
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
    anchors = json.loads(ANCHORS.read_text())
    seeds, errors = [], {}

    # 245 already resolved every anchor to an OpenAlex id; re-resolving would spend
    # 25 queries to learn nothing. Hydrate straight from the stored ids.
    ids = [a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors]
    by_id = {i: a for i, a in zip(ids, anchors)}
    print(f"hydrating {len(ids)} anchors...")
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        d, err = get([("filter", "openalex_id:" + "|".join(batch)),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            errors[f"seed_hydrate:{i}"] = err
            continue
        for w in d.get("results", []):
            oid = w["id"].rsplit("/", 1)[-1]
            a = by_id.get(oid)
            if a is None:
                continue
            seeds.append({
                "openalex": oid,
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "title": w.get("title"),
                "arm": a["arm"],
                "first_author": a["first_author"],
                "refs": w.get("referenced_works") or [],
            })
    print(f"  hydrated {len(seeds)}/{len(ids)}\n")

    pool = {}
    back_ids = defaultdict(set)
    raw_found = {"backward": 0, "forward": 0}      # BEFORE dedup, per rung
    new_by_rung = {"backward": 0, "forward": 0}    # first time this rung added a record

    # --- backward -----------------------------------------------------------
    all_refs = sorted({r.rsplit("/", 1)[-1] for s in seeds for r in s["refs"]})
    for s in seeds:
        for r in s["refs"]:
            back_ids[r.rsplit("/", 1)[-1]].add(s["openalex"])
    raw_found["backward"] = sum(len(s["refs"]) for s in seeds)
    print(f"backward: {raw_found['backward']} reference edges, "
          f"{len(all_refs)} distinct works to hydrate")
    for i in range(0, len(all_refs), 50):
        batch = all_refs[i:i + 50]
        d, err = get([("filter", "openalex_id:" + "|".join(batch)),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            errors[f"backward:{i}"] = err
            continue
        for w in d.get("results", []):
            rec = shape(w)
            if rec["openalex"] not in pool:
                new_by_rung["backward"] += 1
            rec.update({"seeds_backward": sorted(back_ids.get(rec["openalex"], [])),
                        "seeds_forward": [], "first_found_round": 1})
            pool[rec["openalex"]] = rec
        print(f"  hydrated {min(i+50, len(all_refs))}/{len(all_refs)}")

    # --- forward ------------------------------------------------------------
    print(f"\nforward: citations of {len(seeds)} seeds (cap {FORWARD_CAP} each)")
    capped_seeds = []
    for s in seeds:
        d, err = get([("filter", f"cites:{s['openalex']}"),
                      ("per-page", str(FORWARD_CAP)),
                      ("sort", "cited_by_count:desc"), ("select", SELECT)])
        if err:
            errors[f"forward:{s['openalex']}"] = err
            print(f"  FAILED  {s['first_author']} {err}")
            continue
        n = d["meta"]["count"]
        raw_found["forward"] += min(n, FORWARD_CAP)
        if n > FORWARD_CAP:
            capped_seeds.append({"seed": s["first_author"], "arm": s["arm"],
                                 "true_count": n, "taken": FORWARD_CAP})
        for w in d.get("results", []):
            oid = w["id"].rsplit("/", 1)[-1]
            rec = pool.get(oid)
            if rec is None:
                rec = shape(w)
                rec.update({"seeds_backward": [], "seeds_forward": [],
                            "first_found_round": 1})
                pool[oid] = rec
                new_by_rung["forward"] += 1
            if s["openalex"] not in rec["seeds_forward"]:
                rec["seeds_forward"].append(s["openalex"])
        flag = " CAPPED" if n > FORWARD_CAP else ""
        print(f"  {min(n, FORWARD_CAP):4d}/{n:6d}{flag:8s} {s['arm']:10s} {s['first_author']}")

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

    arm_of = {s["openalex"]: s["arm"] for s in seeds}
    records = list(pool.values())
    for r in records:
        srcs = r["seeds_backward"] + r["seeds_forward"]
        r["n_seeds"] = len(srcs)
        r["seed_arms"] = sorted({arm_of[x] for x in srcs if x in arm_of})
        r["no_doi_flag"] = r["doi"] is None
    records.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by"] or 0)))

    reach_by_arm = defaultdict(int)
    only_arm = defaultdict(int)
    for r in records:
        for a in r["seed_arms"]:
            reach_by_arm[a] += 1
        if len(r["seed_arms"]) == 1:
            only_arm[r["seed_arms"][0]] += 1
    seed_cells = defaultdict(int)
    for s in seeds:
        seed_cells[s["arm"]] += 1

    log = {
        "meta": {
            "ticket": "TICK-076", "round": 1,
            "seeds_requested": len(anchors), "seeds_resolved": len(seeds),
            "seed_arms": dict(seed_cells),
            "forward_cap_per_seed": FORWARD_CAP,
            "capped_seeds": capped_seeds,
            "raw_found_before_dedup": raw_found,
            "new_records_by_rung": new_by_rung,
            "pool_size": len(records),
            "reached_by_seed_arm": dict(reach_by_arm),
            "reached_by_exactly_one_arm": dict(only_arm),
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
