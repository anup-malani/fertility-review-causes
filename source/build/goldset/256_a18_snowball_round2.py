#!/usr/bin/env python3
"""256 — A.18 citation snowball, round 2. TICK-076.

Round 1 (246) seeded from the 25 typed anchors. Round 2 seeds from the **screen
positives**: the 168 records the title/abstract screen marked RELEVANT in stratum
A, most of which were never round-1 seeds.

Why this rather than screening the rest of stratum B: the measured yield curve
puts the citation channel at 53.0% against the boolean channel's 9.1% at the head
and 3.3% at depth. Reading 1,880 more abstracts to find ~90 relevant records is
the expensive route to the same place.

PROTOCOL §5.1 caps snowball depth at 2 rounds (Wohlin 2014); this is round 2 and
there will not be a round 3.

Design rules carried forward:
  * Seeds are tagged by the CELL the screen assigned, so the new material can be
    attributed to an arm rather than pooled. The thin arms -- H2_MODERATION and
    PREDICTED_RESPONSE -- are the ones this round exists to feed.
  * Per-rung counts BEFORE dedup as well as after: a rung that only re-finds what
    another rung had is REDUNDANT, which is not EMPTY.
  * "New" means new against **pool ∪ frame** -- everything round 1 and the boolean
    query already reached. Anything less overstates the gain.
  * Growth is not gain. The new records are run through the adopted prescreen
    rules (252: non-human organism, no-fertility-outcome) and BOTH numbers are
    reported, because a round that adds 5,000 records of livestock genetics has
    added nothing.

Usage: python3 source/build/goldset/256_a18_snowball_round2.py [--cap N]
"""
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
OUT_POOL = TEMP / "heritability-fertility-genetic-snowball-pool-r2.json"
OUT_LOG = LOGS / "heritability-fertility-genetic-snowball-round2.json"
API = "https://api.openalex.org/works"

FORWARD_CAP = int(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 100
SELECT = ("id,doi,title,publication_year,type,cited_by_count,primary_location,"
          "authorships,referenced_works,abstract_inverted_index")

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}
NONHUMAN = re.compile(r"\b(cattle|dairy cow|bull|heifer|bovine|sow|boar|piglet|swine|porcine|"
    r"poultry|broiler|laying hen|sheep|ewe|ovine|goat|caprine|buffalo|equine|salmon|tilapia|"
    r"shrimp|aquaculture|silkworm|honeybee|drosophila|nematode|zebrafish|arabidopsis|maize|"
    r"barley|sorghum|soybean|cultivar|male sterility|pollen|anther|agronom|soil fertility|"
    r"livestock|herd|breeding value|inbred lines?|wild population|song sparrow|red deer|great tit)\b", re.I)
FERT = re.compile(r"\b(fitness|reproduc\w+|fertility|fertilit\w*|births?|childbearing|"
    r"children ever born|childless\w*|parity|famil\w+ size|offspring|fecundity|fecundabilit\w*|"
    r"age at first birth|number of children|natalit\w*|birth rate|nulliparous|parous)\b", re.I)


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def fold(s):
    if not s:
        return ""
    s = s.lower()
    for k, v in TRANSLIT.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "150", "--get", API]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
            except Exception:
                time.sleep(4 * (attempt + 1)); continue
            if "meta" in d and "error" not in d:
                return d, None
        time.sleep(4 * (attempt + 1))
    return None, "failed"


def unroll(inv):
    if not inv:
        return None
    n = max(max(v) for v in inv.values()) + 1
    w = [""] * n
    for k, vs in inv.items():
        for v in vs:
            w[v] = k
    return " ".join(w).strip()


def shape(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    ab = unroll(w.get("abstract_inverted_index"))
    return {"openalex": w["id"].rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "title": w.get("title"), "norm_title": fold(w.get("title")),
            "year": w.get("publication_year"), "type": w.get("type"),
            "venue": src.get("display_name"), "cited_by": w.get("cited_by_count"),
            "authors": "; ".join(a["author"]["display_name"]
                                 for a in (w.get("authorships") or [])[:4]),
            "abstract": ab[:1200] if ab else None}


def main():
    TEMP.mkdir(parents=True, exist_ok=True)
    # --- seeds: screen positives ------------------------------------------
    seeds = {}
    for bf in sorted((TEMP / "a18_screen_batches").glob("batch_*.json")):
        n = int(bf.stem.split("_")[1])
        vf = TEMP / "a18_screen_verdicts" / f"verdict_{n:02d}.json"
        if not vf.exists():
            continue
        b = json.loads(bf.read_text())
        v = json.loads(vf.read_text())["verdicts"]
        for r in b["records"]:
            d = v.get(r["ref"])
            if d and d["verdict"] == "RELEVANT":
                seeds[r["openalex"]] = {"cell": d["cell"], "arm": d["arm"],
                                        "title": r["title"]}
    print(f"seeds: {len(seeds)} screen positives")
    print("  by cell:", dict(Counter(s["cell"] for s in seeds.values())))

    known = set(json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text()) and
                [r["openalex"] for r in json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())])
    frame = json.loads((TEMP / "heritability-fertility-genetic-frame-deduped.json").read_text())["records"]
    known |= {r["openalex"] for r in frame}
    print(f"already known (pool ∪ frame): {len(known):,}\n")

    ids = sorted(seeds)
    hydrated, errors = [], {}
    for i in range(0, len(ids), 50):
        d, e = get([("filter", "openalex_id:" + "|".join(ids[i:i + 50])),
                    ("per-page", "50"), ("select", SELECT)])
        if e:
            errors[f"seed:{i}"] = e; continue
        hydrated += d.get("results", [])
    print(f"hydrated {len(hydrated)}/{len(ids)} seeds")

    pool, back_src, raw = {}, defaultdict(set), {"backward": 0, "forward": 0}
    new_by_rung = {"backward": 0, "forward": 0}

    all_refs = sorted({r.rsplit("/", 1)[-1] for w in hydrated
                       for r in (w.get("referenced_works") or [])})
    for w in hydrated:
        sid = w["id"].rsplit("/", 1)[-1]
        for r in (w.get("referenced_works") or []):
            back_src[r.rsplit("/", 1)[-1]].add(sid)
    raw["backward"] = sum(len(w.get("referenced_works") or []) for w in hydrated)
    print(f"backward: {raw['backward']:,} edges, {len(all_refs):,} distinct works")
    for i in range(0, len(all_refs), 50):
        d, e = get([("filter", "openalex_id:" + "|".join(all_refs[i:i + 50])),
                    ("per-page", "50"), ("select", SELECT)])
        if e:
            errors[f"backward:{i}"] = e; continue
        for w in d.get("results", []):
            rec = shape(w)
            if rec["openalex"] not in pool:
                new_by_rung["backward"] += 1
            rec.update({"seeds_backward": sorted(back_src.get(rec["openalex"], [])),
                        "seeds_forward": [], "round": 2})
            pool[rec["openalex"]] = rec
        if i % 1000 == 0:
            print(f"  {min(i+50, len(all_refs)):,}/{len(all_refs):,}")

    print(f"\nforward: citations of {len(hydrated)} seeds (cap {FORWARD_CAP})")
    capped = []
    for j, w in enumerate(hydrated, 1):
        sid = w["id"].rsplit("/", 1)[-1]
        d, e = get([("filter", f"cites:{sid}"), ("per-page", str(FORWARD_CAP)),
                    ("sort", "cited_by_count:desc"), ("select", SELECT)])
        if e:
            errors[f"forward:{sid}"] = e; continue
        n = d["meta"]["count"]
        raw["forward"] += min(n, FORWARD_CAP)
        if n > FORWARD_CAP:
            capped.append({"seed": sid, "true_count": n, "taken": FORWARD_CAP})
        for x in d.get("results", []):
            oid = x["id"].rsplit("/", 1)[-1]
            rec = pool.get(oid)
            if rec is None:
                rec = shape(x)
                rec.update({"seeds_backward": [], "seeds_forward": [], "round": 2})
                pool[oid] = rec
                new_by_rung["forward"] += 1
            if sid not in rec["seeds_forward"]:
                rec["seeds_forward"].append(sid)
        if j % 25 == 0:
            print(f"  {j}/{len(hydrated)} seeds, pool {len(pool):,}")

    # --- what is actually NEW ---------------------------------------------
    new = [r for r in pool.values() if r["openalex"] not in known]
    for r in new:
        txt = f"{r.get('title') or ''} {r.get('venue') or ''} {r.get('abstract') or ''}"
        r["prescreen_nonhuman"] = bool(NONHUMAN.search(txt))
        r["prescreen_no_fert"] = bool(r.get("abstract")) and not FERT.search(txt)
        srcs = r["seeds_backward"] + r["seeds_forward"]
        r["n_seeds"] = len(srcs)
        r["seed_cells"] = sorted({seeds[s]["cell"] for s in srcs if s in seeds})
    survivors = [r for r in new if not r["prescreen_nonhuman"] and not r["prescreen_no_fert"]]
    survivors.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by"] or 0)))

    cell_reach = Counter()
    for r in survivors:
        for c in r["seed_cells"]:
            cell_reach[c] += 1

    log = {"meta": {
        "ticket": "TICK-076", "round": 2,
        "seeds": len(seeds), "seeds_hydrated": len(hydrated),
        "seed_cells": dict(Counter(s["cell"] for s in seeds.values())),
        "forward_cap": FORWARD_CAP, "capped_seeds": len(capped),
        "raw_found_before_dedup": raw, "new_records_by_rung": new_by_rung,
        "reached_total": len(pool),
        "already_known_pool_or_frame": len(pool) - len(new),
        "NEW": len(new),
        "new_after_prescreen": len(survivors),
        "new_dropped_nonhuman": sum(1 for r in new if r["prescreen_nonhuman"]),
        "new_dropped_no_fertility_outcome": sum(1 for r in new if r["prescreen_no_fert"]),
        "survivors_by_seed_cell": dict(cell_reach),
        "multi_seed_survivors": sum(1 for r in survivors if r["n_seeds"] >= 2),
        "errors": len(errors),
        "note": "Growth is not gain: NEW counts records nobody had; survivors are those "
                "that also clear the adopted prescreen. Nothing here is screened."},
        "capped_seeds": capped[:40], "errors": errors}
    OUT_POOL.write_text(json.dumps(survivors, indent=1))
    OUT_LOG.write_text(json.dumps(log, indent=1))
    print("\n" + json.dumps(log["meta"], indent=1))
    print(f"\nwrote {OUT_POOL} and {OUT_LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
