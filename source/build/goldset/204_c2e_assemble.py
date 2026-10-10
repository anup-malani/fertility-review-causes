#!/usr/bin/env python3
"""
204 (c2e) — assemble the blinded screen verdicts and the full-text extractions for C.2.e (TICK-099).

Reads temp/screen/female-wage-opportunity-cost/verdict_*.json (joined to the pool by paperId) and
temp/extraction/c2e/*.json. Emits:
  literature/search-logs/female-wage-opportunity-cost-screen-results.{json,md}
  extraction/female-wage-opportunity-cost.csv                 (one row per extracted full text)
  extraction/female-wage-opportunity-cost-risk-of-bias.csv
  extraction/female-wage-opportunity-cost-missing-pdf-dois.csv (RA proxy wantlist: in-scope, not OA)
"""
import json, csv, glob, os
from collections import Counter

SLUG = "female-wage-opportunity-cost"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
SCREEN = os.path.join(ROOT, "temp", "screen", SLUG)
EXTR = os.path.join(ROOT, "temp", "extraction", "c2e")
POOL = os.path.join(LOGS, f"{SLUG}-pool.json")

pool = {r["id"]: r for r in json.load(open(POOL))["records"]}

verdicts = {}
for vf in sorted(glob.glob(os.path.join(SCREEN, "verdict_*.json"))):
    for v in json.load(open(vf)):
        verdicts[v["paperId"]] = v

man = json.load(open(os.path.join(LOGS, f"{SLUG}-screen-manifest.json")))
for pid in man["noabs_ids"]:
    verdicts.setdefault(pid, {"paperId": pid, "verdict": "UNCERTAIN", "confidence": "low",
                             "reason": "no abstract (RA title/abstract gate)"})
# anchors are in-scope by construction
for pid, r in pool.items():
    if r["source"].startswith("anchor") and pid not in verdicts:
        verdicts[pid] = {"paperId": pid, "verdict": "RELEVANT", "confidence": "high", "reason": "cold-start anchor"}

tally = Counter(v["verdict"] for v in verdicts.values())
relevant_codes = {"RELEVANT", "POOLING"}
rel = [(pid, v) for pid, v in verdicts.items() if v["verdict"] in relevant_codes]
rel_oa = [(pid, v) for pid, v in rel if pool.get(pid, {}).get("oa")]

out = {"tally": dict(tally), "n_total": len(verdicts), "n_relevant": len(rel),
       "n_relevant_oa": len(rel_oa)}
json.dump(out, open(os.path.join(LOGS, f"{SLUG}-screen-results.json"), "w"), indent=1)

with open(os.path.join(LOGS, f"{SLUG}-screen-results.md"), "w") as f:
    f.write("# C.2.e blinded screen results\n\n")
    f.write(f"Pool {len(verdicts)} records. Verdict tally:\n\n")
    for k, n in tally.most_common():
        f.write(f"- {k}: {n}\n")
    f.write(f"\nRELEVANT/POOLING: {len(rel)} ({len(rel_oa)} OA).\n\n")
    f.write("## In-scope, OA (retrievable now)\n\n")
    for pid, v in sorted(rel_oa, key=lambda z: -(pool[z[0]].get("cited_by") or 0)):
        r = pool[pid]
        f.write(f"- [{v['verdict']}] {r['year']} — {r['title'][:90]} (cited {r.get('cited_by')}) doi:{r['doi']}\n")

# RA proxy wantlist: in-scope but not OA
with open(os.path.join(ROOT, "extraction", f"{SLUG}-missing-pdf-dois.csv"), "w", newline="") as f:
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
        "identifies_substitution_effect", "routes_to", "sample_n", "rob_overall"]
with open(os.path.join(ROOT, "extraction", f"{SLUG}.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for r in rows:
        me = r.get("main_effect") or {}
        w.writerow([r.get("study"), r.get("doi"), r.get("year"), r.get("country"), r.get("period"),
                    r.get("design"), r.get("shock"), r.get("shock_type"), r.get("fertility_outcome"),
                    me.get("sign"), me.get("estimate"), me.get("units"), me.get("se"),
                    r.get("elasticity"), r.get("identifies_substitution_effect"), r.get("routes_to"),
                    r.get("sample_n"), (r.get("rob") or {}).get("overall")])

# risk-of-bias CSV from extraction rob sub-objects
with open(os.path.join(ROOT, "extraction", f"{SLUG}-risk-of-bias.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["study", "doi", "design", "shock_type", "confounding", "selection",
                "measurement", "reporting", "overall", "identifies_substitution_effect"])
    for r in rows:
        rob = r.get("rob") or {}
        w.writerow([r.get("study"), r.get("doi"), r.get("design"), r.get("shock_type"),
                    rob.get("confounding"), rob.get("selection"), rob.get("measurement"),
                    rob.get("reporting"), rob.get("overall"), r.get("identifies_substitution_effect")])

print(f"screen tally: {dict(tally)}")
print(f"relevant {len(rel)} ({len(rel_oa)} OA); extracted full texts: {len(rows)}")
print(f"wrote screen-results.{{json,md}}, extraction/{SLUG}.csv, -risk-of-bias.csv, -missing-pdf-dois.csv")
