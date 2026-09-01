#!/usr/bin/env python3
"""287 — C.3.e: strip the method layer from round 2 and screen the rest. TICK-077.

285 returned 297 records new to round 1, and its top yield by citation was Wooldridge,
Little and Rubin, Stock-Yogo and `ivreg2` -- backward citations from methods sections, not
estimand neighbours. Snowball the estimand, not the estimator.

Two things are done here, and they are deliberately kept apart:

  1. THE METHOD LAYER IS MEASURED, NOT SILENTLY DELETED. A record is flagged methodological on
     its own title and venue. The flag is reported as a share so the contamination is a number
     in the log rather than an impression, and flagged records are still scored -- if one turns
     out to carry an estimand, the flag was wrong and the log will show it.
  2. THE ESTIMAND CLASSIFIER FROM 283 DOES THE ACTUAL SCREENING. It is the operative test:
     Wooldridge fails it for having no fertility outcome, not for being a textbook. A filter
     that leans on the method flag would be doing by vocabulary what provenance should do.

Usage: python3 287_c3e_round2_screen.py
"""
import importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"
OUT = LOGS / "credit-constraints-round2-screen.json"

spec = importlib.util.spec_from_file_location("m283", GOLD / "283_c3e_boundary_hunt.py")
m283 = importlib.util.module_from_spec(spec)
sys.modules["m283"] = m283
spec.loader.exec_module(m283)          # importing runs nothing: 283 guards on __main__

# Method-layer detector. Title-level and deliberately conservative -- it is a REPORTING flag,
# not a gate, so a miss costs a line in the log and a false positive costs nothing at all.
METHOD_TITLE = re.compile(
    r"econometric|estimator|estimation of|standard error|weak instrument|"
    r"identification of causal effects|missing data|factor analysis|"
    r"singular value decomposition|limited-dependent|qualitative variables|"
    r"generalized method of moments|\bgmm\b|bootstrap|monte carlo|"
    r"regression models?\b|statistical analysis|sampling|\bstata\b|software|"
    r"handbook of econometrics|panel data\b(?!.*fertilit)", re.I)
METHOD_VENUE = re.compile(r"econometrica|journal of econometrics|stata journal|"
                          r"econometric (theory|reviews)|biometrika", re.I)


def main():
    d = json.loads((LOGS / "credit-constraints-snowball-round2.json").read_text())
    recs = d["records"]
    print(f"{len(recs)} records new to round 1; hydrating abstracts")

    ids = [r["openalex"] for r in recs]
    hydrated = {}
    for i in range(0, len(ids), 50):
        dd, err = m283.get([("filter", "openalex_id:" + "|".join(ids[i:i + 50])),
                            ("per-page", "50"), ("select", m283.SELECT)])
        if err:
            print(f"  batch {i} FAILED: {err}", file=sys.stderr)
            continue
        for w in dd["results"]:
            hydrated[w["id"].rsplit("/", 1)[-1]] = m283.shape(w)
    print(f"  hydrated {len(hydrated)}/{len(ids)}")

    out = []
    for r in recs:
        h = hydrated.get(r["openalex"], {})
        rec = dict(r)
        rec["abstract"] = h.get("abstract", "")
        rec.update(m283.score(rec))
        title = rec.get("title") or ""
        rec["method_layer"] = bool(METHOD_TITLE.search(title)
                                   or METHOD_VENUE.search(rec.get("venue") or "")
                                   or (rec.get("type") or "") == "book")
        rec["no_abstract"] = not rec["abstract"]
        out.append(rec)

    n = len(out)
    method = [r for r in out if r["method_layer"]]
    onestimand = [r for r in out
                  if r["has_outcome"] and (r["has_composite"] or r["has_S"] or r["has_B"])]
    identified = [r for r in onestimand if r["has_ident"]]
    method_and_estimand = [r for r in method if r in onestimand]

    summary = {
        "round2_new_records": n,
        "hydrated": len(hydrated),
        "no_abstract": sum(1 for r in out if r["no_abstract"]),
        "method_layer_flagged": len(method),
        "method_layer_share": round(len(method) / n, 3) if n else None,
        "method_flagged_that_also_carry_an_estimand": len(method_and_estimand),
        "exposure_x_outcome": len(onestimand),
        "…_and_identification": len(identified),
        "by_arm_of_the_identified": {
            "composite": sum(1 for r in identified if r["has_composite"]),
            "S": sum(1 for r in identified if r["has_S"]),
            "B": sum(1 for r in identified if r["has_B"])},
    }
    identified.sort(key=lambda r: -(r["cited_by"] or 0))
    OUT.write_text(json.dumps({"summary": summary, "identified": identified[:80],
                               "method_flagged_titles": [r["title"] for r in method][:60]},
                              indent=2))
    print("\n" + json.dumps(summary, indent=1))
    print("\nIDENTIFIED CANDIDATES from round 2 (exposure x fertility outcome x identification)\n")
    for r in identified[:30]:
        arms = "".join(a for a, f in (("C", r["has_composite"]), ("S", r["has_S"]),
                                      ("B", r["has_B"])) if f)
        flag = " [method-flagged]" if r["method_layer"] else ""
        print(f"  {r['year']} {arms:3s} cites{(r['cited_by'] or 0):6d} | "
              f"{(r['title'] or '')[:80]}{flag}")
        print(f"        {r['venue']}")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
