#!/usr/bin/env python3
"""280 — C.3.e: retrieve full text for the ten unreached composite/savings probes. TICK-077.

Why this exists: 279 found that NONE of the microcredit RCTs, savings-access experiments or
branch-expansion studies is reachable by an exposure x fertility query, because none mentions
fertility in its abstract. That is either (a) the composite stratum is empty, which is the
chapter's most consequential possible finding, or (b) these papers estimate a fertility or
birth outcome in a table whose abstract never says so. Abstract indexing and full-text tables
fail for unrelated reasons, so the full text is a genuinely independent channel -- a search
null is only worth something when the channels do not fail together.

Retrieval rules carried in:
  - TWO COUNTERS PER RUNG: `found` (a URL was produced) and `fetched` (bytes arrived). A rung
    that finds 65 URLs and fetches 0 is not an empty rung, and reporting one number hides it.
  - A BLOCKED ROUTE IS NOT A PAYWALL. A 403 from bot defence on an open URL is a different
    problem from a paywall, and it is fixable by a human with a browser. Status codes are
    recorded per attempt and the handoff is split by cause, not lumped as "unavailable".
  - VERSION TWINS ARE PART OF THE RUNG SET, not a retry. The published record is frequently
    the closed one while its working-paper twin is open; 277 already found twins for 12 of 26
    seeds and they carried 16% of the pool.
  - Rung order is chapter-specific: free OA locations first, then twins' OA locations, then
    Unpaywall. This is economics, so PMC is not in the ladder at all -- carrying another
    chapter's rung wholesale is how A.12 spent a pass on a route that returned nothing.

Usage: python3 280_c3e_probe_retrieval.py
"""
import json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
DEST = ROOT / "temp" / "c3e-probe-fulltext"
OUT = LOGS / "credit-constraints-probe-retrieval.json"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

TARGETS = ["angelucci-2015-compartamos", "attanasio-2015-mongolia", "banerjee-2015-miracle",
           "bruhn-2014-mexico", "burgess-2005-rural-banks", "crepon-2015-morocco",
           "dupas-2013-savings-constraints", "guinnane-credit-cooperatives",
           "prina-2015-banking-the-poor", "rosenzweig-1989-consumption-smoothing"]


def oa(path, params):
    args = ["curl", "-sS", "--max-time", "90", "-G", f"https://api.openalex.org/{path}"]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError:
        return None, "non-JSON"


def fetch(url, dest):
    """Return (ok, http_status, note). A 403 is recorded as BLOCKED, never as absent."""
    r = subprocess.run(
        ["curl", "-sSL", "--max-time", "120", "-A", UA, "-w", "%{http_code}",
         "-o", str(dest), url],
        capture_output=True, text=True)
    code = (r.stdout or "").strip()[-3:]
    if r.returncode != 0:
        return False, code or "curl", f"curl rc={r.returncode}"
    if not dest.exists() or dest.stat().st_size < 20000:
        note = "too small - probably an interstitial or an error page"
        if code == "403":
            note = "BLOCKED (403) - open URL refused by bot defence, not a paywall"
        return False, code, note
    head = dest.open("rb").read(5)
    if head[:4] != b"%PDF":
        return False, code, "not a PDF (landing page or JS shell)"
    return True, code, f"{dest.stat().st_size // 1024} KB"


def main():
    anchors = json.loads((LOGS / "credit-constraints-cold-start-anchors.json").read_text())
    by_key = {a["key"]: a for a in anchors}
    snow = json.loads((LOGS / "credit-constraints-snowball-round1.json").read_text())
    twins_of = {t["seed"]: [x["openalex"] for x in t["twins"]] for t in snow["version_twins"]}

    rung_found = {"oa_self": 0, "oa_twin": 0}
    rung_fetched = {"oa_self": 0, "oa_twin": 0}
    out = []

    for key in TARGETS:
        a = by_key[key]
        self_id = a["top_candidate"]["oa_id"].rsplit("/", 1)[-1]
        ids = [(self_id, "oa_self")] + [(t, "oa_twin") for t in twins_of.get(key, [])]
        rec = {"key": key, "title": a["top_candidate"]["title"], "arm": a["arm"],
               "role": a.get("role"), "attempts": [], "fetched_path": None, "rung": None}

        for oid, rung in ids:
            d, err = oa(f"works/{oid}", [("select", "id,title,locations,best_oa_location,doi")])
            if err or d is None:
                rec["attempts"].append({"id": oid, "rung": rung, "error": err or "no data"})
                continue
            urls = []
            for loc in (d.get("locations") or []):
                if loc.get("pdf_url"):
                    urls.append((loc["pdf_url"], bool(loc.get("is_oa"))))
                elif loc.get("is_oa") and loc.get("landing_page_url"):
                    urls.append((loc["landing_page_url"], True))
            seen, ordered = set(), []
            for u, isoa in urls:
                if u not in seen:
                    seen.add(u)
                    ordered.append((u, isoa))
            ordered.sort(key=lambda x: not x[1])          # OA first
            if ordered:
                rung_found[rung] += 1
            for u, isoa in ordered[:6]:
                if rec["fetched_path"]:
                    break
                dest = DEST / f"{key}__{oid}.pdf"
                ok, code, note = fetch(u, dest)
                rec["attempts"].append({"id": oid, "rung": rung, "url": u[:150],
                                        "is_oa": isoa, "http": code, "ok": ok, "note": note})
                print(f"  {'OK ' if ok else '-- '} {key[:34]:34s} {rung:8s} {code:4s} {note[:52]}")
                if ok:
                    rec["fetched_path"] = str(dest.relative_to(ROOT))
                    rec["rung"] = rung
                    rung_fetched[rung] += 1
                else:
                    dest.unlink(missing_ok=True)
                time.sleep(0.4)
            if rec["fetched_path"]:
                break
        if not rec["fetched_path"]:
            codes = [x.get("http") for x in rec["attempts"] if x.get("http")]
            rec["handoff"] = ("browser-job (open URL refused by bot defence)"
                              if "403" in codes else
                              "proxy-job (no open copy found)" if codes else
                              "no url produced at any rung")
            print(f"  ** {key}: NOT FETCHED -> {rec['handoff']}")
        out.append(rec)

    summary = {"targets": len(TARGETS),
               "fetched": sum(1 for r in out if r["fetched_path"]),
               "rung_found": rung_found, "rung_fetched": rung_fetched,
               "handoff": {r["key"]: r.get("handoff") for r in out if not r["fetched_path"]}}
    OUT.write_text(json.dumps({"summary": summary, "records": out}, indent=2))
    print("\n" + json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
