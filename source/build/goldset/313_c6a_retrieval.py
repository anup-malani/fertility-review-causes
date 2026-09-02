#!/usr/bin/env python3
"""313 — C.6.a full-text retrieval for the primary + boundary cells. TICK-078.

Queue: every record the screen put in a PRIMARY cell, plus MIXED_COHORT_MARRIAGE (Wall 3 boundary).
LINK1_LABOUR and THEORY are context by scope §3/§9 and are not retrieved in this pass.

Rung order is CHOSEN FOR THIS CHAPTER, not inherited. A.12 carried B.6's whole PMC rung and PMC
returned zero (`recovery-rung-order-is-chapter-specific`). This is an economics and demography
literature, largely pre-2000 and largely in society journals; its open copies live on **RePEc/NBER**,
not in PubMed Central. So:

  1. `oa_locations`  every OA location OpenAlex already knows -- free, no extra call
  2. `repec`         RePEc/EconPapers/IDEAS/NBER landing pages found among ANY location host
  3. `unpaywall`     the DOI-keyed OA index
  4. `pmc_bioc`      kept, because it costs one call and is decisive where it applies
                     (`pmc-bioc-beats-every-other-route`); OpenAlex has no pmcid, so bridge from
                     pmid (`openalex-lacks-pmcid-bridge-from-pmid`)

TWO COUNTERS PER RUNG. `found` (a URL was produced) and `fetched` (a file landed). A rung reported
only by fetches looks dead when it is actually finding plenty and failing at the download
(`rung-found-is-not-rung-fetched`). Counting also happens BEFORE dedup, because a rung that only ever
finds already-covered records is REDUNDANT, which is not the same as EMPTY
(`dedup-before-counting-hides-redundant-rung`).

FAILURES ARE TYPED, never collapsed to "not found". A 403 from bot defence is not a paywall
(`blocked-route-is-not-a-paywall`), and a refusal counted as an absence manufactures a confident
negative (`refusals-read-as-zeros`). The handoff is split by what a human would actually have to do.

Idempotent: re-running skips files already on disk and reports the same rung attribution, because a
cache that erases attribution makes the second run disagree with the first
(`stage-output-must-survive-rerun`).

Usage: python3 source/build/goldset/313_c6a_retrieval.py [--limit N]
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
DEST = ROOT / "temp" / "c6a-fulltext"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

PRIMARY = {"RELATIVE_INCOME_FERTILITY", "COHORT_SIZE_FERTILITY", "BENCHMARK_MEASURED",
           "CYCLE_TEST", "RIVAL_TEST", "INSTITUTIONAL_MODERATION"}
ALSO = {"MIXED_COHORT_MARRIAGE"}
REPEC_HOSTS = re.compile(r"repec|econpapers|ideas\.repec|nber\.org|econstor|"
                         r"papers\.ssrn|iza\.org|cepr\.org", re.I)


def oa(path, params):
    args = ["curl", "-sS", "--max-time", "120", "-G", f"https://api.openalex.org/{path}"]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError:
        return None, f"non-JSON: {r.stdout[:150]}"


PDF_HREF = re.compile(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', re.I)
REDIR = re.compile(r'[?&]u=([^;&"\']+)', re.I)


def unwrap_redir(url):
    """EconPapers/IDEAS wrap the real target in `redir.pf?u=<urlencoded target>`. The wrapper is
    bot-defended; the target usually is not, because it sits on a university web server. Decoding
    the parameter and fetching the target directly is what turned a 403 into a 352 KB PDF for the
    Becker-vs-Easterlin working paper. This is the chapter-specific rung that actually pays here --
    the same shape as `recovery-rung-order-is-chapter-specific`, one level down."""
    m = REDIR.search(url or "")
    if not m:
        return None
    from urllib.parse import unquote
    tgt = unquote(m.group(1))
    return tgt if tgt.startswith("http") else None


def pdf_links_on(url):
    """A landing page is not a dead end. RePEc, EconPapers and NBER pages link the PDF one hop
    away, and 26 records in the first run died as 'landing page' with the document right there."""
    r = subprocess.run(["curl", "-sSL", "--max-time", "60", "-A", UA, url],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout:
        return []
    out = []
    # `citation_pdf_url` is the Highwire/Google-Scholar meta tag, and essentially every repository
    # and journal platform emits it. Looking only for href="*.pdf" missed it entirely: DSpace and
    # bepress serve PDFs from /bitstream/ and /cgi/viewcontent.cgi paths with no .pdf extension,
    # which is why seven institutional-repository records died as "landing page".
    for m in re.finditer(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)',
                         r.stdout, re.I):
        out.append(m.group(1))
    for m in re.finditer(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url',
                         r.stdout, re.I):
        out.append(m.group(1))
    for m in re.finditer(r'href=["\']([^"\']*(?:viewcontent\.cgi|/bitstream/|/download)[^"\']*)',
                         r.stdout, re.I):
        h = m.group(1)
        out.append(h if h.startswith("http") else
                   (re.match(r"(https?://[^/]+)", url).group(1) + h if h.startswith("/") else h))
    for href in REDIR.findall(r.stdout)[:6]:
        from urllib.parse import unquote
        tgt = unquote(href)
        if tgt.startswith("http"):
            out.append(tgt)
    for href in PDF_HREF.findall(r.stdout)[:8]:
        if href.startswith("http"):
            out.append(href)
        elif href.startswith("/"):
            m = re.match(r"(https?://[^/]+)", url)
            if m:
                out.append(m.group(1) + href)
        else:
            out.append(url.rsplit("/", 1)[0] + "/" + href)
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq[:10]


def fetch(url, dest):
    """(ok, http_code, note). A 403 is BLOCKED, never absent."""
    r = subprocess.run(["curl", "-sSL", "--max-time", "90", "-A", UA, "-w", "%{http_code}",
                        "-o", str(dest), url], capture_output=True, text=True)
    code = (r.stdout or "").strip()[-3:]
    if r.returncode != 0:
        return False, code or "curl", f"curl rc={r.returncode}"
    if not dest.exists() or dest.stat().st_size < 12000:
        if dest.exists():
            dest.unlink()
        if code == "403":
            return False, code, "BLOCKED (403) — bot defence on an open URL, NOT a paywall"
        if code == "202":
            return False, code, ("BLOCKED (202 interstitial) — a challenge page, not a paywall. "
                                 "403 is not the only shape bot defence takes")
        if code == "404":
            return False, code, "404 at the recorded location"
        return False, code, "too small — interstitial or error page"
    head = dest.open("rb").read(5)
    if head[:4] != b"%PDF":
        txt = dest.open("rb").read(4000).decode("utf-8", "replace")
        if "<html" in txt.lower():
            dest.unlink()
            return False, code, "landing page or JS shell, not a document"
    return True, code, f"{dest.stat().st_size // 1024} KB"


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    # --ids W123,W456 re-runs just those records. The handoff tells an RA to re-run this script
    # after installing hand-retrieved PDFs; re-attempting all 156 over the network to ingest three
    # new files is waste, and the state merge means a targeted pass no longer shrinks the output.
    only = None
    if "--ids" in sys.argv:
        only = {x.strip() for x in sys.argv[sys.argv.index("--ids") + 1].split(",") if x.strip()}
    res = json.loads((LOGS / "easterlin-relative-income-screen-results.json").read_text())
    import csv
    rows = list(csv.DictReader((ROOT / "extraction" /
                               "easterlin-relative-income-screen.csv").open()))
    queue = [r for r in rows if r["cell"] in PRIMARY or r["cell"] in ALSO]
    if only:
        queue = [r for r in queue if r["openalex"] in only]
    if limit:
        queue = queue[:limit]
    DEST.mkdir(parents=True, exist_ok=True)
    state_path = LOGS / "easterlin-relative-income-retrieval-state.json"
    prior = json.loads(state_path.read_text()) if state_path.exists() else {"records": {}}

    print(f"queue: {len(queue)} records "
          f"({sum(1 for r in queue if r['cell'] in PRIMARY)} primary, "
          f"{sum(1 for r in queue if r['cell'] in ALSO)} boundary)\n")

    ids = [r["openalex"] for r in queue]
    meta = {}
    for i in range(0, len(ids), 50):
        d, err = oa("works", {"filter": f"ids.openalex:{'|'.join(ids[i:i+50])}",
                              "per-page": "200",
                              "select": "id,doi,display_name,publication_year,locations,ids,"
                                        "best_oa_location,open_access"})
        if err:
            print(f"  metadata fetch error: {err}")
            continue
        for w in d.get("results", []):
            meta[w["id"].rsplit("/", 1)[-1]] = w
        time.sleep(0.2)
    print(f"metadata for {len(meta)}/{len(ids)}\n")

    probed = Counter()
    found = Counter()
    fetched = Counter()
    out = {}
    for n, r in enumerate(queue, 1):
        oid = r["openalex"]
        w = meta.get(oid, {})
        dest = DEST / f"{oid}.pdf"
        rungs = []

        # rung 1/2: every location OpenAlex knows, RePEc hosts pulled out as their own rung
        for loc in (w.get("locations") or []):
            for u in (loc.get("pdf_url"), loc.get("landing_page_url")):
                if not u:
                    continue
                rung = "repec" if REPEC_HOSTS.search(u) else "oa_locations"
                # DO NOT gate on loc["is_oa"]. The flag is the index's OPINION; the URL is the
                # fact. Becker vs Easterlin has two locations, both flagged is_oa=False, and one
                # of them is a 352 KB PDF on a university web server that downloads on the first
                # try. Skipping it because a metadata field said "not OA" is a confident absence
                # manufactured from someone else's annotation. Trying costs one HTTP request.
                tgt = unwrap_redir(u)
                if tgt:
                    rungs.append(("repec_direct", tgt))   # the real host, tried before the wrapper
                rungs.append((rung, u))
        # rung 3: unpaywall
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if doi:
            rungs.append(("unpaywall", f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}"))
        # rung 4: PMC via the pmid bridge
        pmid = ((w.get("ids") or {}).get("pmid") or "").rsplit("/", 1)[-1]
        if pmid:
            rungs.append(("pmc_bioc", f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/"
                                      f"pmcoa.cgi/BioC_json/{pmid}/unicode"))

        rec = {"cell": r["cell"], "title": r["title"], "year": r["year"],
               "doi": doi, "rungs_found": sorted({x for x, _ in rungs}), "attempts": []}

        if dest.exists() and dest.stat().st_size > 12000:
            p = prior.get("records", {}).get(oid, {})
            rec["status"] = "have"
            # Never invent a rung. If prior state does not know how this file arrived -- a
            # hand-retrieved PDF dropped in by an RA, or a state file lost -- say so, and keep it
            # OUT of the rung counters. "cached" as a rung name would make the second run's rung
            # table disagree with the first's, which is exactly the failure a re-run is meant to
            # catch, not to cause.
            rec["via"] = p.get("via") or "unknown_provenance"
            rec["attempts"] = p.get("attempts", [])
            if rec["via"] != "unknown_provenance":
                fetched[rec["via"]] += 1
            out[oid] = rec
            continue

        # `probed` = the rung was tried. `found` = the rung actually PRODUCED a URL. Conflating
        # them was this script's own first defect: unpaywall was credited with 114 "found" when 81
        # of those were unpaywall replying that no OA copy exists, and those records were then
        # mislabelled `found_not_fetched` instead of paywalled. Both counters are kept, and both are
        # incremented before any dedup, so a REDUNDANT rung stays distinguishable from an EMPTY one.
        for rung, _ in rungs:
            probed[rung] += 1
        for rung, u in rungs:
            # Neither unpaywall nor PMC BioC can be credited with "found" from a constructed URL.
            # Unpaywall's URL is unknown until it answers; BioC returns HTTP 200 with a tiny
            # "no result" body for anything outside the PMC OA subset, so a 200 there is an
            # ABSENCE, not a download failure. Crediting the constructed URL made this rung read
            # as broken when it is simply empty for an economics literature -- the exact inversion
            # of `rung-found-is-not-rung-fetched`, and worth as much care.
            if rung not in ("unpaywall", "pmc_bioc"):
                found[rung] += 1

        got = False
        for rung, url in rungs:
            if rung == "unpaywall":
                d, err = None, None
                rr = subprocess.run(["curl", "-sS", "--max-time", "60", url],
                                    capture_output=True, text=True)
                try:
                    up = json.loads(rr.stdout)
                except json.JSONDecodeError:
                    rec["attempts"].append({"rung": rung, "note": "unpaywall non-JSON"})
                    continue
                loc = (up or {}).get("best_oa_location") or {}
                url = loc.get("url_for_pdf") or loc.get("url")
                if not url:
                    rec["attempts"].append({"rung": rung, "note": "no OA location in unpaywall"})
                    continue
            if rung == "unpaywall":
                found[rung] += 1        # unpaywall produced a URL only now
            ok, code, note = fetch(url, dest)
            if rung == "pmc_bioc":
                if ok:
                    found[rung] += 1
                else:
                    note = "not in the PMC OA subset (BioC returns 200 with an empty body)"
            rec["attempts"].append({"rung": rung, "url": url[:140], "http": code, "note": note})
            if not ok and "landing page" in note:
                for cand in pdf_links_on(url):
                    ok, code, note = fetch(cand, dest)
                    rec["attempts"].append({"rung": rung + "+hop", "url": cand[:140],
                                            "http": code, "note": note})
                    if ok:
                        rung = rung + "+hop"
                        break
            if ok:
                rec.update({"status": "have", "via": rung})
                fetched[rung] += 1
                got = True
                break
            time.sleep(0.2)
        if not got:
            notes = " | ".join(a.get("note", "") for a in rec["attempts"])
            no_oa = "no OA location in unpaywall" in notes
            # An OA location that answers 200 with a sub-threshold body is an interstitial too --
            # it is the same defence, just quieter. Counting those as "not found" is how a
            # retrievable record becomes a confident absence.
            interstitial = any(a.get("note", "").startswith("too small")
                               and a.get("rung") in ("oa_locations", "repec", "repec_direct")
                               for a in rec["attempts"])
            productive = [a for a in rec["attempts"]
                          if a.get("rung") in ("oa_locations", "repec", "repec_direct")
                          or (a.get("rung") == "unpaywall" and a.get("http"))]
            if "BLOCKED" in notes or interstitial:
                rec["status"] = "blocked"            # BROWSER job: open URL, defeated by defences
            elif "landing page" in notes:
                rec["status"] = "landing_only"       # BROWSER job: the PDF hop also failed
            elif no_oa or not productive:
                rec["status"] = "paywalled"          # PROXY job: no open copy exists
            else:
                rec["status"] = "found_not_fetched"  # genuinely odd; read these individually
        out[oid] = rec
        if n % 25 == 0:
            print(f"  {n}/{len(queue)}...", flush=True)

    # A --limit run must not shrink the state file. Merge into what is already there, and record
    # which records this pass actually touched, so a partial run is legible as partial rather than
    # silently discarding 126 records' rung attribution (`stage-output-must-survive-rerun`).
    merged = dict(prior.get("records", {}))
    merged.update(out)
    state_path.write_text(json.dumps({"n": len(merged), "records": merged,
                                      "last_pass_n": len(queue),
                                      "last_pass_ids": sorted(out),
                                      "probed_per_rung": dict(probed),
                                      "found_per_rung": dict(found),
                                      "fetched_per_rung": dict(fetched)}, indent=1) + "\n")

    st = Counter(v["status"] for v in out.values())
    print("\nSTATUS")
    for k, v in st.most_common():
        print(f"  {k:20} {v}")
    print("\nRUNGS — probed / found / fetched")
    for rung in ("oa_locations", "repec_direct", "repec", "unpaywall", "pmc_bioc"):
        f = found[rung] + fetched.get(rung + "+hop", 0)
        got = fetched[rung] + fetched.get(rung + "+hop", 0)
        note = ""
        if probed[rung] and not found[rung]:
            note = "   rung PROBED but produced no URL — empty for this literature"
        elif found[rung] and not got:
            note = "   found URLs, fetched none — a download problem, not an absence"
        print(f"  {rung:14} probed {probed[rung]:4}  found {found[rung]:4}  fetched {got:4}{note}")
    # Retrieval rate hides WHICH records: cross-tab by cell.
    print("\nBY CELL — a rate is not enough; an empty primary cell is not survivable")
    bycell = defaultdict(Counter)
    for v in out.values():
        bycell[v["cell"]][v["status"]] += 1
    for cell in sorted(bycell):
        c = bycell[cell]
        tot = sum(c.values())
        print(f"  {cell:26} have {c['have']:3}/{tot:3}   "
              f"blocked {c['blocked']:3}  no_oa {c['no_oa_location']:3}  "
              f"found_not_fetched {c['found_not_fetched']:3}")


main()
