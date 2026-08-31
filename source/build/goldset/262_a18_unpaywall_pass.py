#!/usr/bin/env python3
"""262 — A.18 Unpaywall recovery: use the rung that was found and never used. TICK-076.

260's log reads `3_unpaywall: found 143, fetched 0`. That is not a dead rung — it
is a rung I located and then never followed. The script queried the Unpaywall API,
recorded the attempt, and `continue`d, so the OA PDF URLs in the response were
discarded. 143 candidate routes went unused.

This is the two-counters-per-rung rule catching my own code rather than someone
else's: with a single "attempted" counter the Unpaywall rung would have looked
exercised. Unpaywall matters here because it indexes OA copies OpenAlex misses —
institutional repositories, author pages, PMC mirrors.

Runs only on records 260 did not retrieve, and reports found vs fetched.

Usage: python3 source/build/goldset/262_a18_unpaywall_pass.py
"""
import json
import subprocess
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
TXT = TEMP / "fulltext"
LOG = LOGS / "heritability-fertility-genetic-retrieval-log.json"
OUT = LOGS / "heritability-fertility-genetic-unpaywall-pass.json"
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")


def fetch(url, out=None, t=60):
    args = ["curl", "-sSL", "--max-time", str(t), "-w", "%{http_code}",
            "-A", UA, "-H", f"From: {MAILTO}"]
    if out:
        args += ["-o", str(out)]
    args += [url]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        return None, "", 0
    code = (r.stdout or "")[-3:]
    body = "" if out else (r.stdout or "")[:-3]
    n = out.stat().st_size if (out and out.exists()) else len(body)
    return code, body, n


def main():
    TXT.mkdir(parents=True, exist_ok=True)
    d = json.loads(LOG.read_text())
    todo = [r for r in d["records"] if r["status"] != "RETRIEVED" and r.get("doi")]
    print(f"unretrieved with a DOI: {len(todo)}\n")

    found = fetched = 0
    rows = []
    for r in todo:
        code, body, _ = fetch(f"https://api.unpaywall.org/v2/{r['doi']}?email={MAILTO}")
        url = None
        try:
            j = json.loads(body)
            best = j.get("best_oa_location") or {}
            url = best.get("url_for_pdf") or best.get("url")
            if not url:
                for l in (j.get("oa_locations") or []):
                    url = l.get("url_for_pdf") or l.get("url")
                    if url:
                        break
        except Exception:
            pass
        row = {"openalex": r["openalex"], "cell": r["cell"], "doi": r["doi"],
               "unpaywall_http": code, "oa_url": url, "fetched": False}
        if url:
            found += 1
            ext = "pdf" if ".pdf" in url.lower() else "html"
            f = TXT / f"{r['openalex']}.up.{ext}"
            c2, _, n = fetch(url, out=f)
            if c2 == "200" and n > 20000:
                fetched += 1
                row["fetched"] = True
                row["file"] = f.name
            elif f.exists():
                f.unlink(missing_ok=True)
            row["fetch_http"] = c2
            row["bytes"] = n
        rows.append(row)
        if len(rows) % 15 == 0:
            print(f"  {len(rows)}/{len(todo)}  found {found} fetched {fetched}")
        time.sleep(0.2)

    bycell = Counter(r["cell"] for r in rows if r["fetched"])
    summary = {"ticket": "TICK-076", "attempted": len(rows),
               "oa_url_found": found, "fetched": fetched,
               "fetched_by_cell": dict(bycell),
               "note": "260 found 143 unpaywall routes and followed none; this follows them."}
    OUT.write_text(json.dumps({"summary": summary, "records": rows}, indent=1))
    print("\n" + json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
