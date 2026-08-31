#!/usr/bin/env python3
"""251 — A.18 frame pull, in relevance order, with the saturation curve measured. TICK-076.

The adopted query's frame is 45,491 records. A.23 screened 1,572 in 29 batches;
screening this frame whole would be ~840 batches, and PROTOCOL §5.1 does not ask
for it — Phase 1 is a sequential saturation search over relevance-ordered results,
stopping on yield.

But saturation rests on an assumption that has bitten this project before: a
truncated OpenAlex pull is the **high-citation, high-relevance head**, not a random
sample, so "yield fell below 5%" can mean "the good records are all behind the
truncation" rather than "the literature is exhausted". The standing instruction is
to MEASURE gold recall in the partial before trusting the stopping rule.

So this script pulls in relevance order and records, for every page, how much of
the known gold has appeared so far:

  * the 25 resolved anchors (the floor set), and
  * the 63 wall-surviving pool-gold records from 250 (the independent set,
    excluding the 29 records 250 classified as Wall 1 / Wall 3 / no-exposure
    route-outs -- including them would score the query against records the walls
    exist to remove).

The output is a curve, not a number: cumulative gold recall against records pulled.
Where it flattens is where saturation is safe; if it is still climbing at the cap,
saturation is NOT safe for this hypothesis and the screen has to take more of the
frame. Reported either way.

Cursor paging, not `page=`: the page parameter caps at 10,000 records and would
impose exactly the truncation this script exists to measure.

Usage: python3 source/build/goldset/251_a18_pull_frame.py [--cap N]
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "heritability-fertility-genetic-frame.json"
OUT_CURVE = LOGS / "heritability-fertility-genetic-saturation-curve.json"
API = "https://api.openalex.org/works"
PER_PAGE = 200
CAP = int(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 12000

SELECT = ("id,doi,title,publication_year,type,language,cited_by_count,"
          "primary_location,authorships,abstract_inverted_index")


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def get(params, tries=4):
    args = ["curl", "-sS", "--max-time", "180", "--get", API]
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
            if "error" in d:
                return None, str(d["error"])[:120]
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


def main():
    rep = json.loads((LOGS / "heritability-fertility-genetic-production-query-repaired.json").read_text())
    Q = rep["query"]

    anchors = json.loads((LOGS / "heritability-fertility-genetic-cold-start-anchors.json").read_text())
    anchor_ids = {a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}

    audit = json.loads((LOGS / "heritability-fertility-genetic-recall-audit.json").read_text())
    routed_out = {m["openalex"] for m in audit["missed"]
                  if m["miss_class"] in ("WALL1_A19_TRANSMISSION", "WALL3_B1_STATUS",
                                         "NO_GENETIC_EXPOSURE")}
    pool = json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())
    FERT = re.compile(r"\b(fertility|births?|children|childless|parity|family size|"
                      r"offspring|reproductive success|fecundity|childbearing)\b", re.I)
    gold_ids = {r["openalex"] for r in pool
                if r["n_seeds"] >= 3 and FERT.search(r["title"] or "")} - routed_out

    print(f"frame query frame_size={rep['frame_size']:,}  cap={CAP:,}")
    print(f"gold: {len(anchor_ids)} anchors, {len(gold_ids)} wall-surviving pool gold\n")

    records, curve = [], []
    seen_anchor, seen_gold = set(), set()
    cursor, page, no_abstract = "*", 0, 0
    while cursor and len(records) < CAP:
        d, err = get([("filter", f"title_and_abstract.search:{Q}"),
                      ("per-page", str(PER_PAGE)), ("cursor", cursor),
                      ("select", SELECT)])
        if err:
            print(f"  page {page+1} FAILED: {err}")
            break
        page += 1
        res = d.get("results", [])
        if not res:
            break
        for w in res:
            oid = w["id"].rsplit("/", 1)[-1]
            ab = unroll(w.get("abstract_inverted_index"))
            if not ab:
                no_abstract += 1
            src = ((w.get("primary_location") or {}).get("source") or {})
            records.append({
                "openalex": oid,
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "title": w.get("title"), "year": w.get("publication_year"),
                "type": w.get("type"), "language": w.get("language"),
                "venue": src.get("display_name"), "cited_by": w.get("cited_by_count"),
                "authors": "; ".join(a["author"]["display_name"]
                                     for a in (w.get("authorships") or [])[:4]),
                "abstract": ab[:2000] if ab else None,
                "rank": len(records) + 1,
            })
            if oid in anchor_ids:
                seen_anchor.add(oid)
            if oid in gold_ids:
                seen_gold.add(oid)
        curve.append({"page": page, "records": len(records),
                      "anchors_found": len(seen_anchor),
                      "anchor_recall_pct": round(100 * len(seen_anchor) / len(anchor_ids), 1),
                      "pool_gold_found": len(seen_gold),
                      "pool_gold_recall_pct": round(100 * len(seen_gold) / len(gold_ids), 1)})
        if page % 5 == 0 or page <= 3:
            c = curve[-1]
            print(f"  page {page:3d}  {c['records']:6,} records   "
                  f"anchors {c['anchors_found']:2d}/{len(anchor_ids)} ({c['anchor_recall_pct']:5.1f}%)   "
                  f"pool gold {c['pool_gold_found']:2d}/{len(gold_ids)} ({c['pool_gold_recall_pct']:5.1f}%)")
        cursor = (d.get("meta") or {}).get("next_cursor")

    last = curve[-1] if curve else {}
    # Is the curve still climbing? Compare the last fifth of pages to the one before it.
    tail = curve[-max(len(curve)//5, 1):]
    prev = curve[-2*max(len(curve)//5, 1):-max(len(curve)//5, 1)] or [curve[0]]
    # Only meaningful when the pull was actually TRUNCATED. On a complete pull nothing
    # can still be arriving, so "flat at the cap" would read as a pass for the
    # stopping rule when it is just an artefact of having taken everything.
    truncated = len(records) < rep["frame_size"] * 0.98
    still_climbing = truncated and (tail[-1]["pool_gold_found"] - prev[-1]["pool_gold_found"]) > 0

    meta = {
        "ticket": "TICK-076", "query": Q, "frame_size": rep["frame_size"],
        "pulled": len(records), "pages": page, "cap": CAP,
        "coverage_of_frame_pct": round(100 * len(records) / rep["frame_size"], 1),
        "no_abstract": no_abstract,
        "no_abstract_pct": round(100 * no_abstract / max(len(records), 1), 1),
        "anchors_in_pull": f"{len(seen_anchor)}/{len(anchor_ids)}",
        "pool_gold_in_pull": f"{len(seen_gold)}/{len(gold_ids)}",
        "gold_still_arriving_at_cap": still_climbing,
        "truncated": truncated,
        "verdict": ("SATURATION UNSAFE - gold still arriving at the cap; the screen "
                    "cannot stop on yield alone" if still_climbing else
                    ("COMPLETE PULL - saturation not tested by this run; see the 12,000-cap "
                     "run for the curve" if not truncated else
                     "gold recall flat at the cap - saturation defensible")),
    }
    OUT.write_text(json.dumps({"meta": meta, "records": records}, indent=1))
    OUT_CURVE.write_text(json.dumps({"meta": meta, "curve": curve}, indent=1))
    print("\n" + json.dumps(meta, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)} and {OUT_CURVE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
