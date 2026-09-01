#!/usr/bin/env python3
"""296 — C.3.e: de-duplicate the primary pool, then retrieve it. TICK-077.

Extraction cannot start without full text, so this is the step before it. Two jobs:

  1. DE-DUPLICATE FIRST. The chapter has hit five version pairs and two of them sit inside the
     primary pool (the bequest-receipt papers; the mortgage-interest-subsidy papers). A pair
     counted twice inflates the evidence base and, if the versions disagree, contributes a
     spurious "replication". Collapse on folded title, keep the published record, and carry the
     twin's id so its full text can still be used when the version of record is closed.

  2. RETRIEVE, WITH THE TWIN RUNG. On this chapter the twin rung produced 5 of 6 fetches for the
     probe set: the published record is usually the closed one and its citations and its PDF both
     live on the working paper. Two counters per rung, and failures split by CAUSE -- a 403 on an
     open URL is a browser job, no open copy is a proxy job, and lumping them hides the fix.

Usage: python3 296_c3e_primary_retrieval.py
"""
import importlib.util, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"
DEST = ROOT / "temp" / "c3e-primary-fulltext"
OUT = LOGS / "credit-constraints-primary-retrieval.json"


def load(n, p):
    spec = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[n] = m
    spec.loader.exec_module(m)
    return m


m283 = load("m283", GOLD / "283_c3e_boundary_hunt.py")
m280 = load("m280", GOLD / "280_c3e_probe_retrieval.py")
m277 = load("m277", GOLD / "277_c3e_snowball.py")
get, fold, SELECT = m283.get, m277.fold, m283.SELECT
NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter", "retraction"}


def main():
    res = json.loads((LOGS / "credit-constraints-screen-results.json").read_text())
    prim = [r for r in res["rows"] if r["cell"].startswith("PRIMARY_")]
    print(f"primary pool before dedup: {len(prim)}")

    # ---- 1. de-duplicate on folded title; published record survives -------------
    groups = {}
    for r in prim:
        groups.setdefault(fold(r["title"]), []).append(r)
    kept, collapsed = [], []
    for t, g in groups.items():
        if len(g) == 1:
            kept.append(dict(g[0]))
            continue
        g.sort(key=lambda r: (not r.get("doi"), -(int(r["year"]) if str(r["year"]).isdigit() else 0)))
        k = dict(g[0])
        k["version_twins"] = [x["openalex"] for x in g[1:]]
        kept.append(k)
        for x in g[1:]:
            collapsed.append({"kept": k["openalex"], "dropped": x["openalex"],
                              "title": x["title"], "cell": x["cell"]})
        print(f"  version pair collapsed: {t[:64]}  ({len(g)} records)")
    print(f"primary pool after dedup: {len(kept)}  ({len(collapsed)} twins folded in)\n")

    # ---- 2. retrieve ------------------------------------------------------------
    DEST.mkdir(parents=True, exist_ok=True)
    rung_found = {"oa_self": 0, "oa_twin": 0}
    rung_fetched = {"oa_self": 0, "oa_twin": 0}
    out = []
    for rec in kept:
        oid = rec["openalex"]
        r = {"openalex": oid, "title": rec["title"], "year": rec["year"], "cell": rec["cell"],
             "arm": rec["arm"], "doi": rec.get("doi"), "attempts": [], "fetched_path": None,
             "rung": None}

        # discover twins by title (strip ? and ! -- inside a quoted filter value they return a
        # SILENT zero, which cost this chapter every `?` seed's twins on round 1)
        ids = [(oid, "oa_self")]
        qt = re.sub(r"\s+", " ", re.sub(r"[?!]", " ", (rec["title"] or "").replace('"', " "))).strip()
        dt, et = get([("filter", f'title.search:"{qt}"'), ("per-page", "10"), ("select", SELECT)])
        if not et:
            for tw in dt.get("results", []):
                tid = tw["id"].rsplit("/", 1)[-1]
                if tid != oid and (tw.get("type") or "").lower() not in NON_STUDY \
                        and fold(tw.get("title")) == fold(rec["title"]):
                    ids.append((tid, "oa_twin"))

        for wid, rung in ids:
            if r["fetched_path"]:
                break
            d, err = m280.oa(f"works/{wid}", [("select", "id,title,locations,best_oa_location,doi")])
            if err or d is None:
                continue
            urls, seen = [], set()
            for loc in (d.get("locations") or []):
                u = loc.get("pdf_url") or (loc.get("landing_page_url") if loc.get("is_oa") else None)
                if u and u not in seen:
                    seen.add(u)
                    urls.append((u, bool(loc.get("is_oa"))))
            urls.sort(key=lambda x: not x[1])
            if urls:
                rung_found[rung] += 1
            for u, isoa in urls[:5]:
                dest = DEST / f"{oid}.pdf"
                ok, code, note = m280.fetch(u, dest)
                r["attempts"].append({"id": wid, "rung": rung, "http": code, "ok": ok,
                                      "note": note, "url": u[:120]})
                if ok:
                    r["fetched_path"] = str(dest.relative_to(ROOT))
                    r["rung"] = rung
                    rung_fetched[rung] += 1
                    break
                dest.unlink(missing_ok=True)
                time.sleep(0.3)

        if not r["fetched_path"]:
            codes = [a.get("http") for a in r["attempts"]]
            r["handoff"] = ("browser-job (open URL, 403 bot defence)" if "403" in codes
                            else "proxy-job (no open copy at any rung)" if codes
                            else "no url produced at any rung")
        print(f"  {'OK ' if r['fetched_path'] else '-- '} {r['cell'][:20]:20s} "
              f"[{r['year']}] {(r['title'] or '')[:52]}"
              f"{'' if r['fetched_path'] else '  -> ' + r['handoff'][:34]}")
        out.append(r)

    fetched = [r for r in out if r["fetched_path"]]
    from collections import Counter
    summary = {"primary_before_dedup": len(prim), "version_pairs_collapsed": len(collapsed),
               "primary_after_dedup": len(kept),
               "fetched": len(fetched), "fetch_rate": round(len(fetched) / len(kept), 3),
               "rung_found": rung_found, "rung_fetched": rung_fetched,
               "fetched_by_arm": dict(Counter(r["arm"] for r in fetched)),
               "outstanding_by_arm": dict(Counter(r["arm"] for r in out if not r["fetched_path"])),
               "handoff_by_cause": dict(Counter(r.get("handoff", "") for r in out
                                                if not r["fetched_path"]))}
    OUT.write_text(json.dumps({"summary": summary, "collapsed": collapsed, "records": out},
                              indent=1))
    print("\n" + json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
