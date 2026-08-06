#!/usr/bin/env python3
r"""
113_d1a_yield_sample.py — D.1.a. What would the full screen add? Estimated from a 400-record sample.

THE DECISION THIS EXISTS TO INFORM. Screening all 15,586 records is ~390 model invocations and, at
the observed ~215s per batch, roughly a day of serial wall-clock. The question that actually matters
is not what the screen costs but whether it changes any conclusion. This chapter's most valuable
outputs are claims about ABSENCE -- Tier 1 is three studies, whole design families are unused -- and
those are exactly the claims a systematic screen can overturn. So: measure the yield on a sample,
and turn "what would we miss?" from a judgement call into a bound.

THE SAMPLE IS ALREADY RANDOM, AND THAT IS NOT AN ACCIDENT. `109_` shuffles the production records
with a fixed seed BEFORE cutting batches, and the shuffle is blind to content. Batches 1-10 are
therefore a uniform random sample of 400 from 15,586, not the first 400 of anything. No separate
sampling step is needed and none should be added: re-sampling would break the property that the
batches already screened are the sample.

WHY A SIMPLE RANDOM SAMPLE RATHER THAN A STRATIFIED ONE. The quantity wanted is the aggregate yield,
for which simple random is unbiased and adequate. Stratifying by cluster would buy precision per
stratum at the cost of rebuilding the batch structure -- and the per-cluster breakdown is recoverable
POST HOC anyway by joining each record back through `idmap.json` to its cluster provenance, which is
what this script does. Design simplicity, same information.

WILSON INTERVALS, NOT NORMAL APPROXIMATION. At the proportions expected here (a few per cent of 400)
the normal approximation misbehaves and can put the lower bound below zero. Wilson is well behaved in
the tail and needs no dependency.

THE UNCERTAIN RATE IS A COST FORECAST, NOT A FAILURE RATE. The rubric routes a record to UNCERTAIN
whenever the deciding fact is invisible at title/abstract, and 31% of this corpus is title-only. Each
UNCERTAIN is one full-text read that must be budgeted rather than discovered.

Usage:  python3 113_d1a_yield_sample.py
Output: literature/search-logs/{slug}-screen-yield-sample.{json,md}
"""
import json, math, sys
from collections import Counter
from pathlib import Path
import importlib.util

SLUG = "postmaterialism-individualism-secularization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
OUT_JSON = LOGS / f"{SLUG}-screen-yield-sample.json"
OUT_MD = LOGS / f"{SLUG}-screen-yield-sample.md"

PRIMARY = {"PRIMARY_POSTMATERIAL_S1", "PRIMARY_INDIVIDUALISM_S2", "PRIMARY_SECULAR_S3",
           "PRIMARY_SECULAR_SHOCK_S3", "PRIMARY_CONSUMERISM_S5", "PRIMARY_VALUE_EX_ANTE",
           "NORM_ENVIRONMENT_LEVEL", "MIXED_CULTURE_PROXY"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    spec = importlib.util.spec_from_file_location("v", HERE / "110_d1a_validate_screen.py")
    v = importlib.util.module_from_spec(spec)
    sys.argv = [sys.argv[0]]
    spec.loader.exec_module(v)
    cells = v.allowed_cells()

    man = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    idmap = json.loads((SCREEN / "idmap.json").read_text())
    corpus = json.loads((LOGS / f"{SLUG}-live-corpus-v2.json").read_text())
    by_oa = {r["openalex_id"]: r for r in corpus["records"]}
    N = man["production_records"]

    rows, batches = [], 0
    for e in man["manifest"]:
        if e["kind"] != "batch":
            continue
        p = REPO / e["output"]
        if not p.exists():
            continue
        got, errs = v.validate_file(REPO / e["input"], p, cells)
        if errs:
            raise SystemExit(f"{e['output']} has {len(errs)} validation errors; refusing to "
                             f"estimate a yield from unvalidated verdicts")
        rows += got
        batches += 1
    n = len(rows)
    if not n:
        raise SystemExit("no production verdicts present")

    verdicts = Counter(r["verdict"] for r in rows)
    cellc = Counter(r["estimand_cell"] for r in rows)
    pairc = Counter(r["pair"] for r in rows if r["verdict"] != "NOT_RELEVANT")
    tiers = Counter(str(r.get("design_tier_guess")) for r in rows if r["verdict"] == "RELEVANT")

    # Provenance and abstract coverage, recovered post hoc through the id map.
    clusters, no_abs, no_abs_unc = Counter(), 0, 0
    for r in rows:
        oa = idmap.get(r["paperId"])
        rec = by_oa.get(oa) or {}
        for c in (rec.get("clusters") or []):
            if r["verdict"] != "NOT_RELEVANT":
                clusters[c] += 1
        if not (rec.get("abstract") or "").strip():
            no_abs += 1
            if r["verdict"] == "UNCERTAIN":
                no_abs_unc += 1

    n_rel = verdicts["RELEVANT"]
    n_unc = verdicts["UNCERTAIN"]
    n_primary = sum(cellc[c] for c in PRIMARY)
    rel_lo, rel_hi = wilson(n_rel, n)
    unc_lo, unc_hi = wilson(n_unc, n)
    pri_lo, pri_hi = wilson(n_primary, n)

    def proj(lo, hi, point):
        return (round(lo * N), round(hi * N), round(point * N))

    rel_proj = proj(rel_lo, rel_hi, n_rel / n)
    unc_proj = proj(unc_lo, unc_hi, n_unc / n)
    pri_proj = proj(pri_lo, pri_hi, n_primary / n)

    out = {"slug": SLUG, "sample_batches": batches, "sample_n": n, "population_N": N,
           "seeded_shuffle": man["seed"], "verdicts": dict(verdicts),
           "relevant_pct": round(100 * n_rel / n, 2),
           "relevant_ci95_pct": [round(100 * rel_lo, 2), round(100 * rel_hi, 2)],
           "relevant_projected": {"point": rel_proj[2], "lo": rel_proj[0], "hi": rel_proj[1]},
           "uncertain_projected": {"point": unc_proj[2], "lo": unc_proj[0], "hi": unc_proj[1]},
           "primary_cell_projected": {"point": pri_proj[2], "lo": pri_proj[0], "hi": pri_proj[1]},
           "cells": dict(cellc.most_common()), "pairs": dict(pairc.most_common()),
           "design_tier_guess_of_relevant": dict(tiers.most_common()),
           "cluster_provenance_of_kept": dict(clusters.most_common()),
           "title_only_in_sample": no_abs, "title_only_routed_uncertain": no_abs_unc}
    OUT_JSON.write_text(json.dumps(out, indent=2))

    L = [f"# D.1.a — what would the full screen add? A {n}-record estimate", "",
         f"**{batches} batches, {n} records, drawn from {N:,}.** The sample is uniform random by "
         f"construction: `109_` shuffles the production records with seed {man['seed']} *before* "
         f"cutting batches, and the shuffle is blind to content, so batches 1–{batches} are a random "
         f"400 rather than the first 400 of anything.", "",
         "Intervals are Wilson 95%. At these proportions the normal approximation misbehaves and can "
         "put a lower bound below zero.", "",
         "## The number that decides whether to run the full screen", "",
         "| | sample | rate | 95% CI | projected to 15,586 |", "|---|---|---|---|---|",
         f"| **RELEVANT** | {n_rel}/{n} | **{100*n_rel/n:.2f}%** | "
         f"{100*rel_lo:.2f}–{100*rel_hi:.2f}% | **{rel_proj[2]:,}** ({rel_proj[0]:,}–{rel_proj[1]:,}) |",
         f"| in a **primary (poolable) cell** | {n_primary}/{n} | {100*n_primary/n:.2f}% | "
         f"{100*pri_lo:.2f}–{100*pri_hi:.2f}% | **{pri_proj[2]:,}** ({pri_proj[0]:,}–{pri_proj[1]:,}) |",
         f"| UNCERTAIN → full-text read | {n_unc}/{n} | {100*n_unc/n:.2f}% | "
         f"{100*unc_lo:.2f}–{100*unc_hi:.2f}% | **{unc_proj[2]:,}** ({unc_proj[0]:,}–{unc_proj[1]:,}) |",
         f"| NOT_RELEVANT | {verdicts['NOT_RELEVANT']}/{n} | "
         f"{100*verdicts['NOT_RELEVANT']/n:.1f}% | | |", "",
         "**The UNCERTAIN row is a cost forecast, not a failure rate.** The rubric routes a record "
         "there whenever the deciding fact is invisible at title/abstract, and it is the instruction "
         "rather than a shortfall. Each one is a full-text read to be budgeted.", "",
         f"Title-only records in the sample: **{no_abs}/{n}** "
         f"({100*no_abs/n:.0f}%), of which {no_abs_unc} were routed UNCERTAIN as the rubric requires.",
         "", "## Where the kept records land", "",
         "| estimand cell | n |", "|---|---|"]
    L += [f"| `{c}` | {k} |" for c, k in cellc.most_common() if k]
    L += ["", "### Pair, among records not rejected", "", "| pair | n |", "|---|---|"]
    L += [f"| {p} | {k} |" for p, k in pairc.most_common()]
    L += ["", "### Design tier guessed for RELEVANT records", "",
          "The rubric's calibration expectation is that Tier 1 is rare — three studies in the whole "
          "frame — so a sample returning many Tier-1 guesses means the screen has mistaken "
          "observational work for identified work.", "", "| tier | n |", "|---|---|"]
    L += [f"| {t} | {k} |" for t, k in tiers.most_common()]
    L += ["", "### Retrieval cluster of kept records", "",
          "Recovered post hoc through `idmap.json`; no stratified sampling was needed.", "",
          "| cluster | n |", "|---|---|"]
    L += [f"| `{c}` | {k} |" for c, k in clusters.most_common()]
    OUT_MD.write_text("\n".join(L) + "\n")

    print(f"n={n} of {N} | RELEVANT {n_rel} ({100*n_rel/n:.2f}%) -> ~{rel_proj[2]:,} "
          f"[{rel_proj[0]:,}-{rel_proj[1]:,}]", file=sys.stderr)
    print(f"  primary cells ~{pri_proj[2]:,} | UNCERTAIN ~{unc_proj[2]:,} full-text reads",
          file=sys.stderr)
    print(f"wrote {OUT_MD.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
