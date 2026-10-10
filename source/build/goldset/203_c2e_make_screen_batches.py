#!/usr/bin/env python3
"""
203 (c2e) — build the blinded title/abstract screen batches + manifest for C.2.e (TICK-099).

Reads the pool (202 output). Abstract-BEARING records are split into blinded batches of 40
(idx, paperId, title, abstract only — discovery channel and anchor status hidden). Abstract-LESS
records are routed to the RA title/abstract gate (manifest noabs_ids) and screened as UNCERTAIN at
assembly, never guessed. Writes:
  temp/screen/female-wage-opportunity-cost/batch_*.json
  literature/search-logs/female-wage-opportunity-cost-screen-manifest.json
"""
import json, os, hashlib

SLUG = "female-wage-opportunity-cost"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
SCREEN = os.path.join(ROOT, "temp", "screen", SLUG)
POOL = os.path.join(LOGS, f"{SLUG}-pool.json")
BATCH_SIZE = 40

os.makedirs(SCREEN, exist_ok=True)
records = json.load(open(POOL))["records"]

withabs = [r for r in records if (r.get("abstract") or "").strip()]
noabs = [r for r in records if not (r.get("abstract") or "").strip()]

# Stable order (by id) so re-runs are deterministic and batches reproducible.
withabs.sort(key=lambda r: r["id"])
noabs.sort(key=lambda r: r["id"])

batches = []
for bi in range(0, len(withabs), BATCH_SIZE):
    chunk = withabs[bi:bi + BATCH_SIZE]
    recs = [{"idx": j, "paperId": r["id"], "title": r["title"], "abstract": (r["abstract"] or "")[:1500]}
            for j, r in enumerate(chunk)]
    path = os.path.join(SCREEN, f"batch_{bi // BATCH_SIZE + 1:03d}.json")
    blob = json.dumps(recs, indent=1)
    json.dump(recs, open(path, "w"), indent=1)
    batches.append({"batch": bi // BATCH_SIZE + 1,
                    "path": os.path.relpath(path, ROOT), "n": len(recs),
                    "sha256": hashlib.sha256(blob.encode()).hexdigest()[:16]})

man = {"slug": SLUG, "n_withabs": len(withabs), "n_noabs": len(noabs),
       "noabs_ids": [r["id"] for r in noabs], "batch_size": BATCH_SIZE, "batches": len(batches)}
# keep the manifest list of batch descriptors too
man_full = dict(man)
man_full["batches"] = batches
json.dump(man_full, open(os.path.join(LOGS, f"{SLUG}-screen-manifest.json"), "w"), indent=1)

print(f"withabs {len(withabs)} -> {len(batches)} batches of {BATCH_SIZE}; noabs {len(noabs)} -> RA gate")
print(f"wrote {SCREEN}/batch_*.json and {SLUG}-screen-manifest.json")
