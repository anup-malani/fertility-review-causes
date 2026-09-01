#!/usr/bin/env python3
"""277 — C.3.e citation snowball (channels 2 and 3), round 1. TICK-077.

Builds the provenance-based pool by snowballing backward (references) and forward
(citations) from the 26 anchors resolved in 275.

Why provenance and not terms here: the two arms do not share a vocabulary. Arm S is
development economics ("children as insurance", "consumption smoothing", crop insurance)
and Arm B is household finance (LTV caps, credit supply, mortgage rate pass-through).
A single term frame that reaches both would have to be so broad that "access to credit"
and "interest rate" dominate it -- 79% and 70% of their blocks respectively, measured in
276. Citation provenance crosses the two literatures where a term query cannot.

Design rules carried forward:
  * Seeds are tagged by ARM (S / B / composite) AND by ROLE (anchor / decoy / probe /
    theory / version_twin). Both are reported. An arm missing from the pool is a defect,
    not a preference, and Ruling 1 made both arms live.
  * DECOYS ARE SEEDED, deliberately. On earlier chapters decoy clouds ran 29-88% on-topic
    against 1-14% for the theory canon: a boundary case is the nearest neighbour of the
    thing you want, so never-seed-a-decoy discards the best channel. Their yield is
    reported separately so the decision is measurable rather than doctrinal.
  * Per-rung counts are taken BEFORE dedup as well as after. A rung that only finds what
    another rung already had is REDUNDANT, which is a different finding from EMPTY, and
    dedup-before-counting hides the difference.
  * Forward truncation is explicit. The cap sorts by citation count, so a capped seed
    contributes its high-citation head and NOT a random sample; capped seeds are named.
  * The version twin (one study, two DOIs, retitled) is seeded but flagged, so it cannot
    silently double-count in the reach statistics.
  * VERSION TWINS ARE DISCOVERED AND SNOWBALLED WITH THEIR SEED. OpenAlex splits a study
    across its working-paper and published records and the CITATIONS DO NOT FOLLOW the
    version of record: Dettling and Kearney's JPubE article carries 0 citations while its
    NBER twin carries 67. Seeding only the version of record therefore returns a hollow
    forward cloud that reads as a quiet literature. For each seed the twin set is found by
    title, non-study types are excluded, and backward refs and forward citations are taken
    over the union. Records reached ONLY through a twin are counted, so the channel has to
    justify itself rather than be assumed.

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
ANCHORS = LOGS / "credit-constraints-cold-start-anchors.json"
OUT_POOL = LOGS / "credit-constraints-snowball-pool.json"
OUT_LOG = LOGS / "credit-constraints-snowball-round1.json"
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
                "role": a.get("role", "anchor"),
                "key": a.get("key"),
                "first_author": a["first_author"] or (a.get("top_candidate") or {}).get("authors_first") or a.get("key"),
                "refs": w.get("referenced_works") or [],
            })
    print(f"  hydrated {len(seeds)}/{len(ids)}\n")

    # --- version-twin discovery -------------------------------------------------
    NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum",
                 "grant", "retraction", "letter", "other"}
    twin_log = []
    for sd in seeds:
        want = fold(sd["title"])
        # `?` and `!` inside a QUOTED filter value return a silent 0 -- valid meta, no
        # error, just an absence that is not one. It is worse than the known `search=`
        # wildcard refusal, which at least returns an error body. Seven of this chapter's
        # 26 seeds carry a `?` in the title ("Do Rural Banks Matter?", "The Miracle of
        # Microfinance?") and every one of them returned zero twins before this strip.
        q = re.sub(r"[?!]", " ", (sd["title"] or "").replace('"', " "))
        q = re.sub(r"\s+", " ", q).strip()
        d, err = get([("filter", f'title.search:"{q}"'), ("per-page", "10"),
                      ("select", SELECT)])
        sd["twins"] = []
        if err:
            errors[f"twins:{sd['openalex']}"] = err
            continue
        for w in d.get("results", []):
            oid = w["id"].rsplit("/", 1)[-1]
            if oid == sd["openalex"]:
                continue
            if (w.get("type") or "").lower() in NON_STUDY:
                continue
            if fold(w.get("title")) != want:
                continue
            sd["twins"].append({"openalex": oid, "year": w.get("publication_year"),
                                "type": w.get("type"),
                                "cited_by": w.get("cited_by_count"),
                                "refs": w.get("referenced_works") or []})
        if sd["twins"]:
            twin_log.append({"seed": sd["key"], "seed_cited_by_rank": None,
                             "twins": [{k: t[k] for k in ("openalex", "year", "type", "cited_by")}
                                       for t in sd["twins"]]})
            print(f"  twins for {sd['key']}: " +
                  ", ".join(f"{t['openalex']}({t['type']},{t['cited_by']}c)" for t in sd["twins"]))

    pool = {}
    back_ids = defaultdict(set)
    via_twin_only = set()
    raw_found = {"backward": 0, "forward": 0}      # BEFORE dedup, per rung
    new_by_rung = {"backward": 0, "forward": 0}    # first time this rung added a record

    # --- backward -----------------------------------------------------------
    def all_refs_of(sd):
        out = list(sd["refs"])
        for t in sd.get("twins", []):
            out += t["refs"]
        return out

    all_refs = sorted({r.rsplit("/", 1)[-1] for sd in seeds for r in all_refs_of(sd)})
    for sd in seeds:
        own = {r.rsplit("/", 1)[-1] for r in sd["refs"]}
        for r in all_refs_of(sd):
            rid = r.rsplit("/", 1)[-1]
            back_ids[rid].add(sd["openalex"])
            if rid not in own:
                via_twin_only.add(rid)
    raw_found["backward"] = sum(len(all_refs_of(sd)) for sd in seeds)
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
        ids = [s["openalex"]] + [t["openalex"] for t in s.get("twins", [])]
        n, results, failed = 0, [], False
        for j, cid in enumerate(ids):
            d, err = get([("filter", f"cites:{cid}"),
                          ("per-page", str(FORWARD_CAP)),
                          ("sort", "cited_by_count:desc"), ("select", SELECT)])
            if err:
                errors[f"forward:{cid}"] = err
                print(f"  FAILED  {s['first_author']} {err}")
                failed = True
                continue
            n += d["meta"]["count"]
            for w in d.get("results", []):
                if j > 0 and w["id"].rsplit("/", 1)[-1] not in {
                        x["id"].rsplit("/", 1)[-1] for x in results}:
                    via_twin_only.add(w["id"].rsplit("/", 1)[-1])
                results.append(w)
        if failed and not results:
            continue
        d = {"meta": {"count": n}, "results": results}
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
    role_of = {s["openalex"]: s["role"] for s in seeds}
    records = list(pool.values())
    for r in records:
        srcs = r["seeds_backward"] + r["seeds_forward"]
        r["n_seeds"] = len(srcs)
        r["seed_arms"] = sorted({arm_of[x] for x in srcs if x in arm_of})
        r["seed_roles"] = sorted({role_of[x] for x in srcs if x in role_of})
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
    reach_by_role, only_role = defaultdict(int), defaultdict(int)
    for r in records:
        for ro in r["seed_roles"]:
            reach_by_role[ro] += 1
        if len(r["seed_roles"]) == 1:
            only_role[r["seed_roles"][0]] += 1
    # yield per seed: a seed that reaches nothing new is dead weight, and an inherited
    # or doctrinal seed choice is only defensible if its yield was measured.
    per_seed = []
    for sd in seeds:
        reached = sum(1 for r in records
                      if sd["openalex"] in r["seeds_backward"] + r["seeds_forward"])
        uniq = sum(1 for r in records
                   if (r["seeds_backward"] + r["seeds_forward"]) == [sd["openalex"]])
        per_seed.append({"key": sd["key"], "arm": sd["arm"], "role": sd["role"],
                         "reached": reached, "reached_only_by_this_seed": uniq})
    per_seed.sort(key=lambda x: -x["reached"])

    log = {
        "meta": {
            "ticket": "TICK-077", "round": 1,
            "seeds_requested": len(anchors), "seeds_resolved": len(seeds),
            "seed_arms": dict(seed_cells),
            "forward_cap_per_seed": FORWARD_CAP,
            "capped_seeds": capped_seeds,
            "raw_found_before_dedup": raw_found,
            "new_records_by_rung": new_by_rung,
            "pool_size": len(records),
            "reached_by_seed_arm": dict(reach_by_arm),
            "reached_by_exactly_one_arm": dict(only_arm),
            "reached_by_seed_role": dict(reach_by_role),
            "reached_by_exactly_one_role": dict(only_role),
            "no_doi": sum(1 for r in records if r["no_doi_flag"]),
            "preprints": sum(1 for r in records if "preprint" in (r["type"] or "")),
            "multi_seed": sum(1 for r in records if r["n_seeds"] >= 2),
            "duplicates_collapsed": len(dropped),
            "seeds_with_version_twins": len(twin_log),
            "records_reached_only_via_a_twin": len([r for r in records
                                                    if r["openalex"] in via_twin_only]),
            "errors": len(errors),
            "note": "Pool is candidates, not a frame. Nothing here has been screened.",
        },
        "version_twins": twin_log,
        "per_seed_yield": per_seed,
        "duplicates_collapsed": dropped,
        "errors": errors,
    }
    OUT_POOL.write_text(json.dumps(records, indent=1))
    OUT_LOG.write_text(json.dumps(log, indent=1))
    print("\nPER-SEED YIELD (reached / reached-only-by-this-seed)")
    for p in per_seed:
        print(f"  {p['reached']:5d} {p['reached_only_by_this_seed']:5d}  "
              f"{p['arm']:9s} {p['role']:12s} {p['key']}")
    print("\n" + json.dumps(log["meta"], indent=1))
    print(f"wrote {OUT_POOL.relative_to(ROOT)} and {OUT_LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
