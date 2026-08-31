#!/usr/bin/env python3
"""260 — A.18 full-text retrieval: discovery and fetch, rung by rung. TICK-076.

Retrieves the 148 primary-cell studies. Rung order is chapter-specific and is set
here from what the prior chapters measured, not inherited wholesale:

  1. **All OA locations** from OpenAlex (`locations[]`, not just `best_oa_location`).
     Free, and on A.12 it beat every fancier rung. Always first.
  2. **PMC BioC.** The standing finding is that for PMC records the PDF 403s, the
     HTML page is a JS shell that returns 200 with ~23 words, and Europe PMC 404s —
     while the BioC endpoint returns full structured text. So PMC is tried as BioC,
     not as PDF.
  3. **Unpaywall** by DOI.
  4. **Publisher landing page** (last, and expected to fail often).

**Two counters per rung, always.** `found` (a URL was located) and `fetched` (bytes
came back). A rung that finds 65 URLs and fetches 0 looks identical to a dead rung
in a single counter, and on A.17 that hid two working rungs.

**A blocked route is not a paywall.** HTTP status is classified into
`paywalled` (401/402/403 with a paywall signature), `bot_blocked` (403/429/503 on
an OPEN url, or a Cloudflare/Incapsula body), `not_found`, and `ok`. The handoff
splits on that distinction because the two need different humans: a bot-blocked
open URL is a browser job, a paywalled one is a proxy job.

**Retrieval rate hides which records.** The summary cross-tabs by estimand cell.
An 80% overall rate that misses `PREDICTED_RESPONSE` — 6 studies, and the only
cell that can carry a demsig number — is a failure, not a success.

Usage: python3 source/build/goldset/260_a18_retrieval.py [--fetch] [--limit N]
"""
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
PDFDIR = TEMP / "fulltext"
OUT = LOGS / "heritability-fertility-genetic-retrieval-log.json"
OUT_MD = LOGS / "heritability-fertility-genetic-retrieval-summary.md"
API = "https://api.openalex.org/works"

DO_FETCH = "--fetch" in sys.argv
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
MAILTO = "shravanh@uchicago.edu"

PAYWALL_SIG = re.compile(r"(purchase|subscribe|sign in to|institutional access|"
                         r"get access|rent this article|buy article)", re.I)
BOT_SIG = re.compile(r"(cloudflare|incapsula|are you a robot|captcha|"
                     r"unusual traffic|access denied|request blocked)", re.I)


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def oa_get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "120", "--get", API]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    for a in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
            except Exception:
                time.sleep(3 * (a + 1)); continue
            if "meta" in d and "error" not in d:
                return d, None
        time.sleep(3 * (a + 1))
    return None, "failed"


def http(url, out=None, timeout=60):
    """Returns (status, kind, bytes). kind in ok/paywalled/bot_blocked/not_found/error."""
    args = ["curl", "-sSL", "--max-time", str(timeout), "-w", "%{http_code}",
            "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120 Safari/537.36",
            "-H", f"From: {MAILTO}", url]
    if out:
        args = args[:1] + ["-o", str(out)] + args[1:]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        return None, "error", 0
    code = (r.stdout or "")[-3:]
    body = "" if out else (r.stdout or "")[:-3]
    n = out.stat().st_size if (out and out.exists()) else len(body)
    if out and out.exists():
        try:
            body = out.read_bytes()[:4000].decode("utf8", "ignore")
        except Exception:
            body = ""
    if code == "200":
        # a 200 that is a login wall or a JS shell is not a retrieval
        if n < 4000 and (PAYWALL_SIG.search(body) or BOT_SIG.search(body)):
            return code, ("bot_blocked" if BOT_SIG.search(body) else "paywalled"), n
        if n < 2000:
            return code, "shell_or_empty", n
        return code, "ok", n
    if code in ("401", "402"):
        return code, "paywalled", n
    if code in ("403", "429", "503"):
        return code, ("bot_blocked" if not PAYWALL_SIG.search(body) else "paywalled"), n
    if code == "404":
        return code, "not_found", n
    return code, "error", n


def main():
    PDFDIR.mkdir(parents=True, exist_ok=True)
    base = json.loads((LOGS / "heritability-fertility-genetic-evidence-base.json").read_text())
    prim = base["primary"]
    if LIMIT:
        prim = prim[:LIMIT]
    ids = [r["openalex"] for r in prim]
    meta = {r["openalex"]: r for r in prim}
    print(f"primary studies: {len(ids)}\n")

    loc = {}
    for i in range(0, len(ids), 50):
        d, e = oa_get([("filter", "openalex_id:" + "|".join(ids[i:i + 50])),
                       ("per-page", "50"),
                       ("select", "id,doi,title,open_access,locations,best_oa_location,ids")])
        if e:
            print(f"  hydrate FAILED at {i}"); continue
        for w in d.get("results", []):
            loc[w["id"].rsplit("/", 1)[-1]] = w
    print(f"hydrated {len(loc)}/{len(ids)}\n")

    rung_found = Counter(); rung_fetched = Counter()
    rows = []
    for oid in ids:
        w = loc.get(oid, {})
        m = meta[oid]
        cands = []
        for l in (w.get("locations") or []):
            if l.get("is_oa"):
                if l.get("pdf_url"):
                    cands.append(("1_oa_pdf", l["pdf_url"]))
                elif l.get("landing_page_url"):
                    cands.append(("1_oa_landing", l["landing_page_url"]))
        pmcid = ((w.get("ids") or {}).get("pmcid") or "")
        if pmcid:
            pid = pmcid.rsplit("/", 1)[-1].replace("PMC", "")
            cands.append(("2_pmc_bioc",
                          f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{pid}/unicode"))
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if doi:
            cands.append(("3_unpaywall", f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}"))
            cands.append(("4_publisher", f"https://doi.org/{doi}"))
        seen = set(); ordered = []
        for rung, u in cands:
            if u not in seen:
                seen.add(u); ordered.append((rung, u))
        for rung, _ in ordered:
            rung_found[rung] += 1

        row = {"openalex": oid, "cell": m["cell"], "arm": m["arm"],
               "title": m.get("title"), "doi": doi or None,
               "is_oa": bool((w.get("open_access") or {}).get("is_oa")),
               "candidates": [{"rung": r, "url": u} for r, u in ordered],
               "attempts": [], "status": "NOT_ATTEMPTED", "file": None}

        if DO_FETCH:
            for rung, u in ordered:
                if rung == "3_unpaywall":
                    code, kind, n = http(u)
                    row["attempts"].append({"rung": rung, "http": code, "kind": kind, "bytes": n})
                    continue
                ext = "json" if "BioC_json" in u else ("pdf" if u.lower().endswith(".pdf") else "html")
                f = PDFDIR / f"{oid}.{ext}"
                code, kind, n = http(u, out=f)
                row["attempts"].append({"rung": rung, "http": code, "kind": kind, "bytes": n})
                if kind == "ok":
                    rung_fetched[rung] += 1
                    row["status"] = "RETRIEVED"; row["file"] = f.name; row["rung"] = rung
                    break
                if f.exists() and f.stat().st_size < 2000:
                    f.unlink(missing_ok=True)
            if row["status"] != "RETRIEVED":
                kinds = [a["kind"] for a in row["attempts"]]
                row["status"] = ("BOT_BLOCKED" if "bot_blocked" in kinds else
                                 "PAYWALLED" if "paywalled" in kinds else
                                 "NO_ROUTE" if not ordered else "FAILED")
        rows.append(row)
        if len(rows) % 25 == 0:
            print(f"  {len(rows)}/{len(ids)}")

    bycell = defaultdict(lambda: Counter())
    for r in rows:
        bycell[r["cell"]][r["status"]] += 1
    summary = {"ticket": "TICK-076", "n": len(rows), "fetched": DO_FETCH,
               "rung_found": dict(rung_found), "rung_fetched": dict(rung_fetched),
               "status": dict(Counter(r["status"] for r in rows)),
               "by_cell": {k: dict(v) for k, v in bycell.items()},
               "oa_share": round(100 * sum(1 for r in rows if r["is_oa"]) / max(len(rows), 1), 1)}
    OUT.write_text(json.dumps({"summary": summary, "records": rows}, indent=1))
    print("\n" + json.dumps(summary, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
