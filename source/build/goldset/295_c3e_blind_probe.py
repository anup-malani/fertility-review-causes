#!/usr/bin/env python3
"""295 — C.3.e: blinded depth probe on `snowball_r1_only`. TICK-077.

Wave 2 showed a 40-record probe cannot resolve a ~2% base rate: it predicted ~6% for
`frame_only` and the true primary yield was 1.6%. `snowball_r1_only` is 3,815 records and was
written off on exactly such a probe, so it gets a properly powered one.

Two things are measured here, and only the first is the base rate:

  1. PREVALENCE — primary-cell yield in a 400-record random sample. At 1% that is 4 expected
     records and at 3% it is 12, which is enough to separate "screen it" from "sample it".
  2. MY OWN SENSITIVITY — 20 records already routed to a PRIMARY cell in waves 1-2 are mixed in
     as HIDDEN CONTROLS and shuffled with the sample. If I fail to re-flag them here, the
     stratum's apparent emptiness is partly my miss rate, not the literature's. A screen that
     cannot show its own sensitivity cannot support a claim of absence.

The controls are written to a separate file that is NOT printed with the batch, so the screening
pass is genuinely blind; 296 unblinds and scores.

Usage: python3 295_c3e_blind_probe.py
"""
import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SAMPLE_N, CONTROL_N, SEED = 400, 20, 295
random.seed(SEED)

U = json.loads((LOGS / "credit-constraints-screen-universe.json").read_text())
res = json.loads((LOGS / "credit-constraints-screen-results.json").read_text())
screened = {r["openalex"] for r in res["rows"]}
primary = [r for r in res["rows"] if r["cell"].startswith("PRIMARY_")]

import re
AGRO = re.compile(r"soil fertilit|fertiliz|fertilis|crop yield|agronom|nitrogen|livestock|"
                  r"cattle|poultry|maize|wheat yield", re.I)
VET = re.compile(r"\b(cow|sow|bovine|porcine|dairy herd|broiler)\b", re.I)
NON = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter", "retraction"}


def txt(r):
    return ((r.get("title") or "") + " . " + (r.get("abstract") or "")).lower()


def stratum(r):
    p = set(r["provenance"])
    if any(x.startswith("hand_") for x in p):
        return "hand_sourced"
    d = {x for x in p if not x.startswith("hand_")}
    if "frame" in d and len(d) > 1:
        return "both_channels"
    if "frame" in d:
        return "frame_only"
    if "snowball_r2" in d:
        return "snowball_r2_only"
    return "snowball_r1_only"


pool = [r for r in U["records"]
        if stratum(r) == "snowball_r1_only"
        and not AGRO.search(txt(r)) and not VET.search(txt(r))
        and (r.get("type") or "").lower() not in NON]
print(f"stratum size after prescreen: {len(pool)}")

sample = random.sample(pool, min(SAMPLE_N, len(pool)))
by_id = {r["openalex"]: r for r in U["records"]}
ctrl_rows = random.sample(primary, min(CONTROL_N, len(primary)))
controls = []
for c in ctrl_rows:
    rec = by_id.get(c["openalex"])
    if rec:
        controls.append({"openalex": rec["openalex"], "title": rec.get("title"),
                         "year": rec.get("year"), "venue": rec.get("venue"),
                         "true_cell": c["cell"]})

batch = [{"openalex": r["openalex"], "title": r.get("title"), "year": r.get("year"),
          "venue": r.get("venue"), "abstract": (r.get("abstract") or "")[:300]}
         for r in sample]
batch += [{"openalex": c["openalex"], "title": c["title"], "year": c["year"],
           "venue": c["venue"], "abstract": (by_id[c["openalex"]].get("abstract") or "")[:300]}
          for c in controls]
random.shuffle(batch)

(LOGS / "credit-constraints-r1-probe-batch.json").write_text(json.dumps(batch, indent=1))
(LOGS / "credit-constraints-r1-probe-key.json").write_text(json.dumps(
    {"seed": SEED, "stratum_size": len(pool), "sample_n": len(sample),
     "controls": controls}, indent=1))
print(f"batch of {len(batch)} written ({len(sample)} sampled + {len(controls)} hidden controls)")
print("key written separately and NOT printed with the batch")
