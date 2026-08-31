#!/usr/bin/env python3
"""263 — A.18 retrieval consolidation and split handoff. TICK-076.

Merges the three retrieval passes into one state, retries the genuinely retryable
failures, and writes a handoff split by WHAT KIND OF HUMAN can clear each record.

  260  OA locations + publisher      99/148
  261  PMC via PMID->PMCID + BioC    49 more (the rung twice reported as dead)
  262  Unpaywall follow-through      13 URLs, 0 fetched — genuine 403/429 blocks

**429 is not 403.** Four records rate-limited on bioRxiv; that is retryable with
backoff and is not a block. Retried here before anything is handed to a human.

**The handoff splits on failure kind, because the two need different people:**
  * `BROWSER_JOB` — an OPEN url killed by bot defence (SSRN, publisher CDNs).
    A human with a browser clears these in one session; a proxy will not help.
  * `PROXY_JOB` — genuinely paywalled, or no route located at all. Needs the
    UChicago proxy, ILL, or an author email.

Both lists are ordered by **estimand cell**, not by convenience: `H2_MODERATION`
retrieved at 46% against a 67% average, and it is the arm carrying the chapter's
distinctive finding. `PREDICTED_RESPONSE` is the only cell that can bear a demsig
number. Those go to the front regardless of how easy the rest are.

Usage: python3 source/build/goldset/263_a18_retrieval_consolidate.py
"""
import json
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
TXT = TEMP / "fulltext"
OUT = LOGS / "heritability-fertility-genetic-retrieval-state.json"
OUT_MD = LOGS / "heritability-fertility-genetic-retrieval-handoff.md"
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
PRIORITY = ["PREDICTED_RESPONSE", "H2_MODERATION", "WITHIN_VS_POPULATION",
            "PEDIGREE_RESPONSE", "SELECTION_DIFFERENTIAL", "H2_FERTILITY"]


def main():
    base = {r["openalex"]: r for r in
            json.loads((LOGS / "heritability-fertility-genetic-evidence-base.json").read_text())["primary"]}
    r260 = json.loads((LOGS / "heritability-fertility-genetic-retrieval-log.json").read_text())
    r261 = json.loads((LOGS / "heritability-fertility-genetic-pmc-recovery.json").read_text())
    r262 = json.loads((LOGS / "heritability-fertility-genetic-unpaywall-pass.json").read_text())

    state = {}
    for r in r260["records"]:
        state[r["openalex"]] = {"cell": r["cell"], "arm": r["arm"], "title": r.get("title"),
                                "doi": r.get("doi"),
                                "status": "RETRIEVED" if r["status"] == "RETRIEVED" else r["status"],
                                "route": r.get("rung") if r["status"] == "RETRIEVED" else None,
                                "file": r.get("file"),
                                "blocked_urls": [c["url"] for c in r.get("candidates", [])
                                                 if c["rung"] != "3_unpaywall"]}
    for r in r261.get("records", []):
        if r.get("ok") and state.get(r["openalex"], {}).get("status") != "RETRIEVED":
            state[r["openalex"]].update({"status": "RETRIEVED", "route": "2_pmc_bioc",
                                         "file": f"{r['openalex']}.bioc.json"})
    up = {r["openalex"]: r for r in r262["records"]}

    # --- retry the 429s (rate-limited, not blocked) ------------------------
    retried = 0
    for oid, r in up.items():
        if r.get("fetch_http") == "429" and state[oid]["status"] != "RETRIEVED":
            url = r.get("oa_url")
            for attempt, wait in enumerate((3, 10, 25)):
                time.sleep(wait)
                f = TXT / f"{oid}.retry.pdf"
                p = subprocess.run(["curl", "-sSL", "--max-time", "90", "-o", str(f),
                                    "-w", "%{http_code}", "-A", UA,
                                    "-H", f"From: {MAILTO}", url],
                                   capture_output=True, text=True)
                code = (p.stdout or "")[-3:]
                n = f.stat().st_size if f.exists() else 0
                if code == "200" and n > 20000:
                    state[oid].update({"status": "RETRIEVED", "route": "3b_unpaywall_retry",
                                       "file": f.name})
                    retried += 1
                    break
                if f.exists():
                    f.unlink(missing_ok=True)

    for oid, s in state.items():
        if s["status"] == "RETRIEVED":
            continue
        u = up.get(oid, {})
        if s["status"] == "NO_ROUTE" and not u.get("oa_url"):
            s["job"] = "PROXY_JOB"; s["reason"] = "no open route located"
        elif s["status"] in ("BOT_BLOCKED",) or u.get("fetch_http") in ("403", "429"):
            s["job"] = "BROWSER_JOB"; s["reason"] = "open URL refused by bot defence"
        else:
            s["job"] = "PROXY_JOB"; s["reason"] = "paywalled"
        if u.get("oa_url"):
            s["blocked_urls"] = [u["oa_url"]] + s.get("blocked_urls", [])

    got = [s for s in state.values() if s["status"] == "RETRIEVED"]
    todo = [s for s in state.values() if s["status"] != "RETRIEVED"]
    bycell = defaultdict(lambda: Counter())
    for oid, s in state.items():
        bycell[s["cell"]]["got" if s["status"] == "RETRIEVED" else "todo"] += 1

    summary = {"ticket": "TICK-076", "primary_studies": len(state),
               "retrieved": len(got),
               "rate": round(100 * len(got) / len(state), 1),
               "by_route": dict(Counter(s["route"] for s in got)),
               "outstanding": len(todo),
               "jobs": dict(Counter(s["job"] for s in todo)),
               "retried_429_recovered": retried,
               "by_cell": {c: {"retrieved": bycell[c]["got"], "outstanding": bycell[c]["todo"],
                               "rate": round(100 * bycell[c]["got"] /
                                             max(bycell[c]["got"] + bycell[c]["todo"], 1), 1)}
                           for c in PRIORITY if c in bycell}}
    OUT.write_text(json.dumps({"summary": summary, "state": state}, indent=1))

    md = ["# A.18 full-text retrieval — state and handoff\n",
          f"**{len(got)} of {len(state)} primary studies retrieved ({summary['rate']}%).** "
          f"{len(todo)} outstanding.\n",
          "\n## By route\n\n| route | studies |\n|---|---|"]
    for r, n in Counter(s["route"] for s in got).most_common():
        md.append(f"| `{r}` | {n} |")
    md += ["\n## By estimand cell — read this before the overall rate\n",
           "| cell | retrieved | outstanding | rate |\n|---|---|---|---|"]
    for c in PRIORITY:
        if c in bycell:
            b = summary["by_cell"][c]
            md.append(f"| `{c}` | {b['retrieved']} | {b['outstanding']} | {b['rate']}% |")
    for job, label, who in (("BROWSER_JOB", "Browser job", "a human with a logged-in browser; a proxy will NOT help"),
                            ("PROXY_JOB", "Proxy / ILL job", "UChicago proxy, ILL, or an author email")):
        rows = [s for s in todo if s["job"] == job]
        rows.sort(key=lambda s: (PRIORITY.index(s["cell"]) if s["cell"] in PRIORITY else 99))
        md += [f"\n## {label} — {len(rows)} records\n", f"*Needs {who}.*\n",
               "| cell | title | DOI | first blocked URL |\n|---|---|---|---|"]
        for s in rows:
            u = (s.get("blocked_urls") or [""])[0]
            md.append(f"| `{s['cell']}` | {(s['title'] or '')[:70]} | "
                      f"{s.get('doi') or '—'} | {u[:70]} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(json.dumps(summary, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
