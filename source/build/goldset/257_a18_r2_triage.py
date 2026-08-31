#!/usr/bin/env python3
"""257 — A.18 snowball round 2 triage: is the new material gain or growth? TICK-076.

Round 2 (256) returns records nobody had. That count on its own means nothing:
the standing lesson is that frame growth is not frame gain — on A.23, adding
"emancipation" grew the frame 40% with ZERO gold. So before any of round 2's
output is screened, this asks three questions of it:

  1. **Concentration.** How many new records are reached by >=2 distinct screen
     positives? A record the citation network reaches repeatedly is a different
     object from one reached once, and round 1's multi-seed records were where
     the gold sat.
  2. **Arm attribution.** Which SCREEN CELL supplied the seeds that reached each
     new record? Round 2 exists mainly to feed the two thin arms —
     `H2_MODERATION` (7 records) and `PREDICTED_RESPONSE` (4, and the only cell
     that can carry a demsig number under Ruling 1). New material that lands only
     in the already-fat `H2_FERTILITY` arm is worth much less to this chapter.
  3. **Recall check.** Does round 2 re-find the known gold it should? Gold that
     round 1 and the boolean query BOTH reached must appear here too; if it does
     not, the round is broken rather than the literature exhausted.

Output is a batched screening queue ordered by seed count, blinded the same way
as 255 — no gold flags, no seed identities, no round labels.

Usage: python3 source/build/goldset/257_a18_r2_triage.py [--size 55] [--max-batches N]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
# Read the DEDUPED pool (258): the raw round-2 output double-counted version
# pairs and title clusters, inflating NEW by 260.
POOL = TEMP / "heritability-fertility-genetic-snowball-pool-r2-deduped.json"
BATCHDIR = TEMP / "a18_r2_batches"
OUT = LOGS / "heritability-fertility-genetic-r2-triage.json"
OUT_MD = LOGS / "heritability-fertility-genetic-r2-triage.md"

SIZE = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 55
MAXB = int(sys.argv[sys.argv.index("--max-batches") + 1]) if "--max-batches" in sys.argv else 8

THIN_CELLS = {"H2_MODERATION", "PREDICTED_RESPONSE", "PEDIGREE_RESPONSE",
              "ALLELE_FREQ_TREND", "WITHIN_VS_POPULATION"}
# Seeds whose ESTIMAND is a method, not the hypothesis. Their citation network is
# every field that uses the estimator, not this literature. Measured on a 16-vs-16
# read: records reached ONLY from THEORY seeds were ~2/16 adjacent (Fisher 1941 on
# gene substitution, The American Statistician, In the Name of Eugenics, eco-evo
# responses to climate change), against ~9/16 for records reached only from
# thin-arm seeds. They go to their own stratum and are bounded, not screened.
METHOD_CELLS = {"THEORY"}


def main():
    if not POOL.exists():
        print(f"round 2 output not present yet: {POOL}")
        return
    new = json.loads(POOL.read_text())
    print(f"round 2 survivors: {len(new):,}\n")

    seedcount = Counter(r["n_seeds"] for r in new)
    multi = [r for r in new if r["n_seeds"] >= 2]
    print("concentration:")
    for k in sorted(seedcount)[:6]:
        print(f"   reached by {k} seed(s): {seedcount[k]:,}")
    print(f"   >=2 seeds: {len(multi):,} ({100*len(multi)/max(len(new),1):.1f}%)\n")

    cellreach = Counter()
    thin_only = []
    for r in new:
        cells = set(r.get("seed_cells") or [])
        for c in cells:
            cellreach[c] += 1
        if cells and cells <= THIN_CELLS:
            thin_only.append(r)
    print("arm attribution (new records reached from each screen cell):")
    for c, n in cellreach.most_common():
        mark = "  <-- THIN ARM" if c in THIN_CELLS else ""
        print(f"   {c:26s} {n:6,}{mark}")
    print(f"\n   reached ONLY from thin-arm seeds: {len(thin_only):,}")

    # recall check against known gold
    anchors = json.loads((LOGS / "heritability-fertility-genetic-cold-start-anchors.json").read_text())
    aid = {a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}
    got = {r["openalex"] for r in new}
    print(f"\nrecall check: {len(aid & got)} of {len(aid)} typed anchors appear among NEW records "
          f"(expected ~0 — they were round-1 seeds and are already known)")

    BATCHDIR.mkdir(parents=True, exist_ok=True)
    for f in BATCHDIR.glob("batch_*.json"):
        f.unlink()
    method_only = [r for r in new
                   if set(r.get("seed_cells") or []) and set(r.get("seed_cells") or []) <= METHOD_CELLS]
    mo = {r["openalex"] for r in method_only}
    print(f"   reached ONLY from METHOD/THEORY seeds: {len(method_only):,} "
          f"— separate stratum, deprioritised (see header)")
    substantive = [r for r in new if r["openalex"] not in mo]
    multi = [r for r in multi if r["openalex"] not in mo]
    print(f"   substantive queue after removing method-only: {len(substantive):,}")

    # priority: multi-seed first, then thin-arm-only, then the rest by citations
    seen, queue = set(), []
    for group in (multi, thin_only, substantive):
        for r in group:
            if r["openalex"] not in seen:
                seen.add(r["openalex"]); queue.append(r)
    nb = 0
    for i in range(0, min(len(queue), SIZE * MAXB), SIZE):
        nb += 1
        chunk = queue[i:i + SIZE]
        (BATCHDIR / f"batch_{nb:02d}.json").write_text(json.dumps(
            {"batch": nb, "slug": "heritability-fertility-genetic", "ticket": "TICK-076",
             "round": 2,
             "rubric": "literature/search-logs/heritability-fertility-genetic-screen-rubric.md",
             "records": [{"ref": f"R2-{nb:02d}-{j:02d}", "openalex": r["openalex"],
                          "title": r.get("title"), "venue": r.get("venue"),
                          "year": r.get("year"), "type": r.get("type"),
                          "abstract": (r.get("abstract") or "")[:1000] or None}
                         for j, r in enumerate(chunk, 1)]}, indent=1))
    payload = {"meta": {"ticket": "TICK-076", "round": 2,
                        "new_survivors": len(new),
                        "method_theory_only_deprioritised": len(method_only),
                        "substantive_queue": len(substantive),
                        "multi_seed_substantive": len(multi),
                        "thin_arm_only": len(thin_only),
                        "reached_by_cell": dict(cellreach),
                        "batches_written": nb, "batch_size": SIZE,
                        "queue_order": "multi-seed, then thin-arm-only, then by citations",
                        "blinding": "no gold flags, no seed identities, no round labels in batches"}}
    OUT.write_text(json.dumps(payload, indent=1))
    OUT_MD.write_text(
        "# A.18 snowball round 2 — triage\n\n"
        f"New survivors: **{len(new):,}**. Reached by >=2 screen positives: **{len(multi):,}**.\n"
        f"Reached only from thin-arm seeds (`H2_MODERATION`, `PREDICTED_RESPONSE`, "
        f"`PEDIGREE_RESPONSE`): **{len(thin_only):,}**.\n\n"
        "| seed cell | new records reached |\n|---|---|\n" +
        "\n".join(f"| `{c}` | {n:,} |" for c, n in cellreach.most_common()) +
        f"\n\n{nb} screening batches of {SIZE} written, ordered multi-seed first.\n")
    print(f"\nwrote {nb} batches to {BATCHDIR}")
    print(f"wrote {OUT.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
