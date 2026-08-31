#!/usr/bin/env python3
"""261 — A.18 PMC recovery via PMID→PMCID conversion. TICK-076.

260's PMC rung reported **0 routes found**, which would have read as "these papers
are not in PMC". They are: OpenAlex simply does not populate `ids.pmcid` for any of
the 148 primary studies, while **102 of them carry `ids.pmid`**. The rung was
unreachable by the route used, not empty — a fake zero on the rung that B.6 and
A.23 both found beats every other for full text.

The bridge is NCBI's ID Converter (pmid -> pmcid), then the BioC endpoint, which
returns full structured text where the PMC PDF 403s and the HTML page is a JS
shell returning 200 with a couple of dozen words.

Reports `found` and `fetched` separately, per rung, as 260 does.

Usage: python3 source/build/goldset/261_a18_pmc_recovery.py [--fetch]
"""
import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
TXTDIR = TEMP / "fulltext"
OUT = LOGS / "heritability-fertility-genetic-pmc-recovery.json"
# The v1.0 path 301-redirects to this. The first run used curl WITHOUT -L, so it
# parsed the redirect HTML, logged "unparseable", and reported pmcid_found: 0 --
# which reads as "these papers are not in PMC" when the request never ran. Third
# instance this session of a refusal rendering as an empty result; -L added below.
IDCONV = "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/"
BIOC = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{}/unicode"
MAILTO = "shravanh@uchicago.edu"
DO_FETCH = "--fetch" in sys.argv


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def main():
    TXTDIR.mkdir(parents=True, exist_ok=True)
    base = json.loads((LOGS / "heritability-fertility-genetic-evidence-base.json").read_text())
    prim = base["primary"]
    ids = [r["openalex"] for r in prim]
    meta = {r["openalex"]: r for r in prim}

    pmid_of = {}
    for i in range(0, len(ids), 50):
        args = ["curl", "-sS", "--max-time", "120", "-G", "https://api.openalex.org/works",
                "--data-urlencode", "filter=openalex_id:" + "|".join(ids[i:i + 50]),
                "--data-urlencode", "per-page=50", "--data-urlencode", "select=id,ids",
                "--data-urlencode", f"api_key={KEY}"]
        d = json.loads(subprocess.run(args, capture_output=True, text=True).stdout)
        for w in d.get("results", []):
            p = (w.get("ids") or {}).get("pmid")
            if p:
                pmid_of[w["id"].rsplit("/", 1)[-1]] = p.rsplit("/", 1)[-1]
    print(f"records with a PMID: {len(pmid_of)}/{len(ids)}")

    # --- convert pmid -> pmcid, batched -----------------------------------
    pmcid_of, rev, failed_batches = {}, {v: k for k, v in pmid_of.items()}, []
    pl = sorted(set(pmid_of.values()))
    for i in range(0, len(pl), 190):
        batch = pl[i:i + 190]
        args = ["curl", "-sSL", "--max-time", "120", "-G", IDCONV,
                "--data-urlencode", "ids=" + ",".join(batch),
                "--data-urlencode", "format=json",
                "--data-urlencode", f"email={MAILTO}",
                "--data-urlencode", "tool=fertility-review"]
        r = subprocess.run(args, capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception:
            # Loud, and distinct from "no records": a request that did not run is
            # not evidence about PMC coverage.
            print(f"  idconv batch {i} REQUEST FAILED (not an empty result): "
                  f"{r.stdout[:120]!r}")
            failed_batches.append(i)
            continue
        for rec in d.get("records", []):
            # The API returns `pmid` as an INTEGER while our keys are strings, so a
            # direct `in` test is False for every record and the rung reports zero.
            # Match on `requested-id`, which is echoed back as the string we sent.
            key = str(rec.get("requested-id") or rec.get("pmid") or "")
            if rec.get("pmcid") and key in rev:
                pmcid_of[rev[key]] = rec["pmcid"]
        time.sleep(0.5)
    print(f"converted to a PMCID: {len(pmcid_of)}  "
          f"({100*len(pmcid_of)/max(len(pmid_of),1):.1f}% of PMID-bearing records)\n")

    found_by_cell = Counter(); fetched_by_cell = Counter()
    for oid in pmcid_of:
        found_by_cell[meta[oid]["cell"]] += 1

    rows, fetched = [], 0
    if DO_FETCH:
        for oid, pmcid in pmcid_of.items():
            f = TXTDIR / f"{oid}.bioc.json"
            args = ["curl", "-sSL", "--max-time", "90", "-o", str(f), "-w", "%{http_code}",
                    "-H", f"From: {MAILTO}", BIOC.format(pmcid)]
            r = subprocess.run(args, capture_output=True, text=True)
            code = (r.stdout or "")[-3:]
            n = f.stat().st_size if f.exists() else 0
            ok = code == "200" and n > 5000
            if ok:
                fetched += 1
                fetched_by_cell[meta[oid]["cell"]] += 1
            elif f.exists():
                f.unlink(missing_ok=True)
            rows.append({"openalex": oid, "pmcid": pmcid, "cell": meta[oid]["cell"],
                         "http": code, "bytes": n, "ok": ok})
            if len(rows) % 20 == 0:
                print(f"  fetched {fetched}/{len(rows)}")

    summary = {"ticket": "TICK-076",
               "primary_studies": len(ids),
               "with_pmid": len(pmid_of),
               "pmcid_found": len(pmcid_of),
               "bioc_fetched": fetched if DO_FETCH else None,
               "found_by_cell": dict(found_by_cell),
               "fetched_by_cell": dict(fetched_by_cell) if DO_FETCH else None,
               "idconv_failed_batches": failed_batches,
               "note": "OpenAlex populates no pmcid for any of these records; the rung is "
                       "reachable only by converting from pmid. found != fetched. A failed "
                       "conversion batch is reported separately and is NOT a zero."}
    OUT.write_text(json.dumps({"summary": summary, "records": rows}, indent=1))
    print("\n" + json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
