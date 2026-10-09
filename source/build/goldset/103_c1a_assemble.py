#!/usr/bin/env python3
"""
103 (c1a) — assemble the blinded screen verdicts and the full-text extractions.

Reads temp/screen/income-effect-normal-good/verdict_*.json (joined to the pool by paperId) and
temp/extraction/c1a/*.json. Emits:
  literature/search-logs/income-effect-normal-good-screen-results.{json,md}
  extraction/income-effect-normal-good.csv              (one row per extracted full text)
  extraction/income-effect-normal-good-missing-pdf-dois.csv  (RA proxy wantlist: in-scope, not OA)
"""
import json, csv, glob, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
SCREEN = os.path.join(ROOT, "temp", "screen", "income-effect-normal-good")
EXTR = os.path.join(ROOT, "temp", "extraction", "c1a")
POOL = os.path.join(LOGS, "income-effect-normal-good-pool.json")

pool = {r["id"]: r for r in json.load(open(POOL))["records"]}

verdicts = {}
for vf in sorted(glob.glob(os.path.join(SCREEN, "verdict_*.json"))):
    for v in json.load(open(vf)):
        verdicts[v["paperId"]] = v

man = json.load(open(os.path.join(LOGS, "income-effect-normal-good-screen-manifest.json")))
for pid in man["noabs_ids"]:
    verdicts.setdefault(pid, {"paperId": pid, "verdict": "UNCERTAIN", "confidence": "low",
                             "reason": "no abstract (RA title/abstract gate)"})
# anchors are in-scope by construction
for pid, r in pool.items():
    if r["source"].startswith("anchor") and pid not in verdicts:
        verdicts[pid] = {"paperId": pid, "verdict": "RELEVANT", "confidence": "high", "reason": "cold-start anchor"}

tally = Counter(v["verdict"] for v in verdicts.values())
relevant_codes = {"RELEVANT", "RELEVANT_HISTORICAL", "POOLING"}
rel = [(pid, v) for pid, v in verdicts.items() if v["verdict"] in relevant_codes]
rel_oa = [(pid, v) for pid, v in rel if pool.get(pid, {}).get("oa")]

out = {"tally": dict(tally), "n_total": len(verdicts), "n_relevant": len(rel),
       "n_relevant_oa": len(rel_oa)}
json.dump(out, open(os.path.join(LOGS, "income-effect-normal-good-screen-results.json"), "w"), indent=1)

with open(os.path.join(LOGS, "income-effect-normal-good-screen-results.md"), "w") as f:
    f.write("# C.1.a blinded screen results\n\n")
    f.write(f"Pool {len(verdicts)} records. Verdict tally:\n\n")
    for k, n in tally.most_common():
        f.write(f"- {k}: {n}\n")
    f.write(f"\nRELEVANT/POOLING/HISTORICAL: {len(rel)} ({len(rel_oa)} OA).\n\n")
    f.write("## In-scope, OA (retrievable now)\n\n")
    for pid, v in sorted(rel_oa, key=lambda z: -(pool[z[0]].get("cited_by") or 0)):
        r = pool[pid]
        f.write(f"- [{v['verdict']}] {r['year']} — {r['title'][:90]} (cited {r.get('cited_by')}) doi:{r['doi']}\n")

# RA proxy wantlist: in-scope but not OA
with open(os.path.join(ROOT, "extraction", "income-effect-normal-good-missing-pdf-dois.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["paperId", "year", "title", "doi", "verdict", "cited_by", "source"])
    for pid, v in sorted(rel, key=lambda z: -(pool[z[0]].get("cited_by") or 0)):
        r = pool[pid]
        if not r.get("oa"):
            w.writerow([pid, r["year"], r["title"], r["doi"], v["verdict"], r.get("cited_by"), r["source"]])

# extraction CSV from full-text reads
rows = []
for ef in sorted(glob.glob(os.path.join(EXTR, "*.json"))):
    try:
        rows.append(json.load(open(ef)))
    except Exception as e:
        print("skip", ef, e)

cols = ["study", "doi", "year", "country", "period", "design", "shock", "shock_type",
        "fertility_outcome", "sign", "estimate", "units", "se", "elasticity",
        "identifies_pure_income_effect", "routes_to", "sample_n", "rob_overall"]
with open(os.path.join(ROOT, "extraction", "income-effect-normal-good.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for r in rows:
        me = r.get("main_effect") or {}
        w.writerow([r.get("study"), r.get("doi"), r.get("year"), r.get("country"), r.get("period"),
                    r.get("design"), r.get("shock"), r.get("shock_type"), r.get("fertility_outcome"),
                    me.get("sign"), me.get("estimate"), me.get("units"), me.get("se"),
                    r.get("elasticity"), r.get("identifies_pure_income_effect"), r.get("routes_to"),
                    r.get("sample_n"), (r.get("rob") or {}).get("overall")])

# risk-of-bias CSV from extraction rob sub-objects
with open(os.path.join(ROOT, "extraction", "income-effect-normal-good-risk-of-bias.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["study", "doi", "design", "shock_type", "confounding", "selection",
                "measurement", "reporting", "overall", "identifies_pure_income_effect"])
    for r in rows:
        rob = r.get("rob") or {}
        w.writerow([r.get("study"), r.get("doi"), r.get("design"), r.get("shock_type"),
                    rob.get("confounding"), rob.get("selection"), rob.get("measurement"),
                    rob.get("reporting"), rob.get("overall"), r.get("identifies_pure_income_effect")])

print(f"screen tally: {dict(tally)}")
print(f"relevant {len(rel)} ({len(rel_oa)} OA); extracted full texts: {len(rows)}")
print("wrote screen-results.{json,md}, extraction/income-effect-normal-good.csv, -missing-pdf-dois.csv")
