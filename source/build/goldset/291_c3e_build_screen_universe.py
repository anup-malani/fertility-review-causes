#!/usr/bin/env python3
"""291 — C.3.e: build the screening universe. TICK-077.

Merges the repaired 3,512-record production frame with the three snowball pools, keeping
PROVENANCE per record rather than dissolving it in a dedup. Two reasons:

  1. A channel that only re-finds what another channel already had is REDUNDANT, which is a
     different finding from EMPTY, and dedup-before-counting hides the difference. Round 1's
     Unpaywall rung on an earlier chapter read as found=0 for exactly this reason.
  2. 283 measured the channels disagreeing violently -- 112 term-only hits against 2
     provenance-only -- and that disagreement is a property worth carrying into the screen,
     because a term-only record and a provenance-only record are not equally likely to be
     on-estimand.

Dedup is by folded title, with the PUBLISHED version surviving a version pair (this chapter has
hit three of them), and the losing record's provenance merged into the keeper rather than lost.

Usage: python3 291_c3e_build_screen_universe.py
"""
import importlib.util, json, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"
OUT = LOGS / "credit-constraints-screen-universe.json"


def load(n, p):
    spec = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[n] = m
    spec.loader.exec_module(m)
    return m


m283 = load("m283", GOLD / "283_c3e_boundary_hunt.py")
m277 = load("m277", GOLD / "277_c3e_snowball.py")
get, shape, fold, SELECT = m283.get, m283.shape, m277.fold, m283.SELECT


def main():
    rep = json.loads((LOGS / "credit-constraints-query-repair.json").read_text())
    OUTCOME, EXPO = rep["final"]["outcome_axis"], rep["final"]["exposure_axes"]
    allexpo = [t for v in EXPO.values() for t in v]
    f = f"title_and_abstract.search:{m283.blk(allexpo)} AND {m283.blk(OUTCOME)}"

    recs, cursor = {}, "*"
    while cursor:
        d, err = get([("filter", f), ("per-page", "200"), ("cursor", cursor),
                      ("select", SELECT)])
        if err:
            print(f"FRAME PULL FAILED: {err}", file=sys.stderr)
            break
        for w in d["results"]:
            r = shape(w)
            r["provenance"] = ["frame"]
            recs[r["openalex"]] = r
        cursor = d["meta"].get("next_cursor")
        print(f"  frame: {len(recs)}/{d['meta']['count']}")
        if not d["results"]:
            break
    frame_n = len(recs)

    # HAND-SOURCED STUDIES GO IN EXPLICITLY. A snowball pool contains what the seeds REACHED,
    # never the seeds themselves, so every hand-sourced anchor, decoy and candidate was absent
    # from the universe -- including the 2026 PNAS provident-fund study that C.2.c explicitly
    # routed to this chapter, and Islam et al. 2026, the strongest composite find. Tier-A anchors
    # are studies: screen output is not the evidence base.
    hand = {}
    anchors = json.loads((LOGS / "credit-constraints-cold-start-anchors.json").read_text())
    for a in anchors:
        tc = a.get("top_candidate") or {}
        if tc.get("oa_id"):
            hand[tc["oa_id"].rsplit("/", 1)[-1]] = f"hand_anchor_{a.get('role','anchor')}"
    hunt = json.loads((LOGS / "credit-constraints-boundary-hunt.json").read_text())
    for h in hunt["hits"][:120]:
        if h.get("has_outcome") and h.get("has_composite"):
            hand.setdefault(h["openalex"], "hand_boundary_hunt")
    r2 = json.loads((LOGS / "credit-constraints-round2-screen.json").read_text())
    for r in r2.get("identified", []):
        hand.setdefault(r["openalex"], "hand_round2")
    for oid in ("W3011170043", "W3122525178", "W1512976090", "W4407312762",
                "W2998507442", "W2476864819", "W7163997065"):
        hand.setdefault(oid, "hand_arm_seed")
    need_hand = [k for k in hand if k not in recs]
    print(f"\n  injecting {len(hand)} hand-sourced studies "
          f"({len(need_hand)} absent from frame+pools)")
    for i in range(0, len(need_hand), 50):
        d, err = get([("filter", "openalex_id:" + "|".join(need_hand[i:i + 50])),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            print(f"    hand batch {i} FAILED: {err}", file=sys.stderr)
            continue
        for w in d["results"]:
            r = shape(w)
            r["provenance"] = [hand[r["openalex"]]]
            recs[r["openalex"]] = r
    for oid, tag in hand.items():
        if oid in recs and tag not in recs[oid]["provenance"]:
            recs[oid]["provenance"].append(tag)

    pools = [("snowball_r1", LOGS / "credit-constraints-snowball-pool.json", None),
             ("snowball_r2", LOGS / "credit-constraints-snowball-round2.json", "records"),
             ("snowball_r3", LOGS / "credit-constraints-arm-round3.json", "candidates")]
    pool_stats = {}
    for name, path, key in pools:
        if not path.exists():
            continue
        raw = json.loads(path.read_text())
        rows = raw if key is None else raw.get(key, [])
        added = 0
        for r in rows:
            oid = r["openalex"]
            if oid in recs:
                if name not in recs[oid]["provenance"]:
                    recs[oid]["provenance"].append(name)
            else:
                rec = dict(r)
                rec.setdefault("abstract", "")
                rec["provenance"] = [name]
                recs[oid] = rec
                added += 1
        pool_stats[name] = {"rows": len(rows), "added_new": added,
                            "already_present": len(rows) - added}
        print(f"  {name}: {len(rows)} rows, {added} new, "
              f"{len(rows) - added} already in the universe")

    # hydrate abstracts for anything that arrived without one
    need = [k for k, v in recs.items() if not v.get("abstract")]
    print(f"\nhydrating {len(need)} records lacking an abstract")
    for i in range(0, len(need), 50):
        d, err = get([("filter", "openalex_id:" + "|".join(need[i:i + 50])),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            continue
        for w in d["results"]:
            oid = w["id"].rsplit("/", 1)[-1]
            s = shape(w)
            if s.get("abstract"):
                recs[oid]["abstract"] = s["abstract"]
            for fld in ("title", "year", "venue", "type", "cited_by", "doi", "authors"):
                recs[oid].setdefault(fld, s.get(fld))

    # dedup by folded title; published survives; provenance merges
    by_title = defaultdict(list)
    for r in recs.values():
        t = fold(r.get("title") or "")
        if t:
            by_title[t].append(r)
    collapsed = []
    for t, group in by_title.items():
        if len(group) < 2:
            continue
        group.sort(key=lambda r: (r.get("doi") is None,
                                  "preprint" in (r.get("type") or ""),
                                  -(r.get("cited_by") or 0)))
        keep = group[0]
        for lose in group[1:]:
            for p in lose["provenance"]:
                if p not in keep["provenance"]:
                    keep["provenance"].append(p)
            if not keep.get("abstract") and lose.get("abstract"):
                keep["abstract"] = lose["abstract"]
            collapsed.append({"kept": keep["openalex"], "dropped": lose["openalex"],
                              "title": lose.get("title")})
            recs.pop(lose["openalex"], None)

    out = list(recs.values())
    prov = defaultdict(int)
    for r in out:
        prov["+".join(sorted(r["provenance"]))] += 1
    summary = {"frame_pulled": frame_n, "pool_merge": pool_stats,
               "universe_before_dedup": len(out) + len(collapsed),
               "version_pairs_collapsed": len(collapsed),
               "UNIVERSE": len(out),
               "no_abstract": sum(1 for r in out if not r.get("abstract")),
               "by_provenance": dict(sorted(prov.items(), key=lambda kv: -kv[1]))}
    OUT.write_text(json.dumps({"summary": summary, "collapsed": collapsed[:200],
                               "records": out}, indent=1))
    print("\n" + json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
