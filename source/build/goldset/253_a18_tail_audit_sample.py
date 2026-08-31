#!/usr/bin/env python3
"""253 — A.18 boolean-only tail audit: a blinded sample with hidden controls. TICK-076.

The prescreen leaves 31,960 survivors, ~595 in-session screening batches. The
obvious reduction — keep only records the citation channel also reached (320
records holding 64 of 65 gold) — CANNOT be justified on that number, because the
gold set is pool-derived: the anchors seeded the pool and the pool-gold are pool
members by construction. "The pool contains the gold" is a tautology here, not
evidence. A gold set built from one channel cannot evaluate that channel.

So the question "what is in the 31,640 boolean-only records?" has to be answered by
looking. This draws a random sample of them for screening, and mixes in hidden
positive controls drawn from known gold.

BLINDED, per the A.23 lesson: the sample carries no flag saying which records are
controls, which came from the pool, or which are anchors. A screener who can see
that a record is gold will not reject it, which destroys the audit. The key is
written to a SEPARATE file that is not read until verdicts are recorded.

Two things get measured:
  * prevalence of relevant records in the boolean-only tail -- which decides
    whether that tail can be deprioritised, and with what stated bound;
  * the screener's own recall on the hidden controls -- because a prevalence
    estimate from a screen of unknown sensitivity is not an estimate.

Usage: python3 source/build/goldset/253_a18_tail_audit_sample.py [--n 150] [--controls 12]
"""
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "heritability-fertility-genetic-tail-audit-sample.json"
KEY = LOGS / "heritability-fertility-genetic-tail-audit-KEY.json"

N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 150
NC = int(sys.argv[sys.argv.index("--controls") + 1]) if "--controls" in sys.argv else 12
SEED = 20260831


def main():
    frame = json.loads((LOGS / "heritability-fertility-genetic-frame.json").read_text())["records"]
    surv = set(json.loads((LOGS / "heritability-fertility-genetic-prescreen.json").read_text())["survivor_ids"])
    pool_ids = {r["openalex"] for r in
                json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())}
    anchors = json.loads((LOGS / "heritability-fertility-genetic-cold-start-anchors.json").read_text())
    aid = {a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}
    audit = json.loads((LOGS / "heritability-fertility-genetic-recall-audit.json").read_text())
    routed = {m["openalex"] for m in audit["missed"] if m["miss_class"] != "A18_CANDIDATE"}
    pool = json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())
    FT = re.compile(r"\b(fertility|births?|children|childless|parity|family size|"
                    r"offspring|reproductive success|fecundity|childbearing)\b", re.I)
    pg = {r["openalex"] for r in pool if r["n_seeds"] >= 3 and FT.search(r["title"] or "")} - routed
    gold = aid | pg

    byid = {r["openalex"]: r for r in frame}
    tail = sorted(surv - pool_ids)                      # boolean-only stratum
    controls_avail = sorted((gold & surv) - set(tail))  # known gold, all pool-reached

    rng = random.Random(SEED)
    sample_ids = rng.sample(tail, min(N, len(tail)))
    ctrl_ids = rng.sample(controls_avail, min(NC, len(controls_avail)))

    rows = []
    for oid in sample_ids + ctrl_ids:
        r = byid[oid]
        rows.append({
            "ref": None,  # filled after shuffle so ordering leaks nothing
            "openalex": oid,
            "title": r.get("title"),
            "venue": r.get("venue"), "year": r.get("year"), "type": r.get("type"),
            "abstract": (r.get("abstract") or "")[:900] or None,
        })
    rng.shuffle(rows)
    for i, r in enumerate(rows, 1):
        r["ref"] = f"R{i:03d}"

    key = {r["ref"]: {"openalex": r["openalex"],
                      "stratum": "CONTROL_GOLD" if r["openalex"] in ctrl_ids else "TAIL",
                      "is_anchor": r["openalex"] in aid}
           for r in rows}

    OUT.write_text(json.dumps({
        "meta": {"ticket": "TICK-076", "seed": SEED,
                 "tail_population": len(tail),
                 "n_sampled": len(sample_ids), "n_controls": len(ctrl_ids),
                 "blinding": "Stratum and gold status are withheld. Key is in a separate file "
                             "and must not be read until verdicts are written.",
                 "task": "For each record decide RELEVANT / NOT_RELEVANT / INSUFFICIENT_INFO "
                         "for A.18: does it estimate a GENETIC contribution to a realized "
                         "FERTILITY outcome in humans? A parent-child fertility correlation "
                         "with no decomposition is NOT_RELEVANT (Wall 1). Phenotypic status "
                         "-> fertility is NOT_RELEVANT (Wall 3). A non-fertility phenotype is "
                         "NOT_RELEVANT. No abstract and an undecisive title is INSUFFICIENT_INFO."},
        "records": [{k: v for k, v in r.items() if k != "openalex"} for r in rows]},
        indent=1))
    KEY.write_text(json.dumps(key, indent=1))
    print(f"tail population: {len(tail):,}")
    print(f"wrote {len(rows)} blinded records ({len(sample_ids)} tail + {len(ctrl_ids)} hidden controls)")
    print(f"  sample: {OUT.relative_to(ROOT)}")
    print(f"  key:    {KEY.relative_to(ROOT)}  <-- do not read until verdicts are written")


if __name__ == "__main__":
    main()
