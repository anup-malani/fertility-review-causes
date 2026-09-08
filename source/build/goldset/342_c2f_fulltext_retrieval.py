#!/usr/bin/env python3
"""342 — full-text retrieval for C.2.f's primary and boundary cells (TICK-081).

Ported from C.2.b's 324. The machinery is carried unchanged; the RUNG ORDER is re-argued for this
chapter's literature, per `recovery-rung-order-is-chapter-specific` (PMC won 0 on A.12 after carrying
B.6's whole rung, and C.6.a measured it EMPTY at 45 pmids).

**This is not the same literature C.2.b retrieved.** The primary cell is dominated by China, South
Korea, Taiwan and Hong Kong studies published 2024-2026 — *Journal of Population Economics*, *Chinese
Sociological Review*, plus regional venues and dissertations. The predictions, recorded before the
run so the rung report can be read against them:

  - `oa_location` should carry most of it; several are recent and gold/green OA.
  - `wp_host` should do LITTLE. This is not an NBER/IZA literature, and the econ working-paper hosts
    that carried C.2.b will mostly miss. Kept anyway, because a rung that finds nothing is a
    measurement and a rung that was never run is not.
  - `pmc_bioc` should be EMPTY — no biomedical indexing here. Kept for the same reason, and its zero
    will be reported as a zero rather than dropped.
  - The expected failure mode is NOT the paywall it usually is: regional Chinese and Korean venues
    (CNKI, KCI, DBpia) are frequently outside both open access and the UChicago proxy, which makes
    them a THIRD handoff kind, not a `proxy` job. Where that is what a record needs, it is classified
    and counted rather than filed under a bucket that implies the proxy would work.

Three counters per rung, never one: `probed`, `found`, `fetched` are different numbers, and
collapsing them is how PMC and Unpaywall read as dead at 0 fetches while holding 27 and 65 URLs
(`rung-found-is-not-rung-fetched`).

The OA flag is an opinion; the URL is the fact. Nothing is gated on `is_oa`.

A 200 is not a PDF: every download is checked for `%PDF` magic bytes and a plausible size
(`bot-defence-is-not-only-403`).

Failures are classified by WHAT A HUMAN MUST DO — `browser`, `proxy`, `dead`, `none` — because a
blocked route is not a paywall (`blocked-route-is-not-a-paywall`: 67 of A.17's 98 failures were open
URLs killed by bot defence).

**Retrieval RATE is not the number that matters.** `retrieval-rate-hides-which-records`: 23/114 was
survivable on C.3.g and 0 of 4 identified direct-arm records was not. The report cross-tabs
retrieval by CELL, and the number to read is coverage of `TUTORING_POLICY_FERTILITY` and
`REQUIRED_INVESTMENT_FERTILITY` — the cells carrying the boundary-spanning designs.

Usage: python3 source/build/goldset/342_c2f_fulltext_retrieval.py [--tier 1,2,3]
"""
import argparse
import csv
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "source" / "lib"))
from openalex import OpenAlex, POOL                                   # noqa: E402

LOGS = ROOT / "literature" / "search-logs"
PDFS = ROOT / "literature" / "pdfs" / "rising-inequality-and-status-competition"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")
# One definition of "we have the full text", shared by 324/325/326. Three scripts each
# carrying their own status tuple is how `hand_retrieved` silently read as outstanding.
GOT = {"fetched", "already_on_disk", "hand_retrieved"}
PRIMARY_CELLS = {"DISPERSION_FERTILITY", "POSITIONAL_ALLOCATION_FERTILITY",
                 "REQUIRED_INVESTMENT_FERTILITY", "TUTORING_POLICY_FERTILITY"}
CONTEXT_CELLS = {"INEQ_ASSOCIATION", "WRONG_DIRECTION", "PERCEIVED_STATUS"}
# Hosts where a working paper actually lives in economics, tried ahead of the generic OA rung.
WP_HOSTS = ("nber.org", "repec", "ideas.repec", "ssrn.com", "econstor", "iza.org",
            "worldbank.org", "cepr.org", "nbp.pl", "bis.org", "osf.io")


def curl(url, out=None, head=False, timeout=60):
    args = ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA,
            "--max-redirs", "10", "-w", "%{http_code}\\t%{content_type}\\t%{url_effective}"]
    if head:
        args += ["-I", "-o", "/dev/null"]
    elif out:
        args += ["-o", str(out)]
    else:
        args += ["-o", "/dev/null"]
    args.append(url)
    r = subprocess.run(args, capture_output=True, text=True)
    parts = (r.stdout or "").strip().split("\t")
    code = parts[0] if parts else ""
    ctype = parts[1] if len(parts) > 1 else ""
    final = parts[2] if len(parts) > 2 else url
    return code, ctype, final


def body(url, timeout=45):
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout or ""


def is_pdf(path):
    """A 200 is not a PDF. Check the magic bytes and a plausible size."""
    try:
        if path.stat().st_size < 8000:
            return False
        with path.open("rb") as f:
            return f.read(5).startswith(b"%PDF")
    except OSError:
        return False


# Publisher hosts a UChicago proxy can open, vs open hosts that merely defend against curl. The
# distinction is the whole point of the handoff: a proxy job sent to a browser session fails, and a
# browser job sent to the proxy fails (`blocked-route-is-not-a-paywall`).
PAYWALL_HOSTS = ("sciencedirect", "elsevier", "wiley", "springer", "link.springer", "tandfonline",
                 "cambridge.org", "oup.com", "academic.oup", "jstor", "sagepub", "emerald",
                 "journals.uchicago", "nature.com", "sciencemag")
OPEN_BUT_DEFENDED = ("econstor", "repec", "ssrn", "figshare", "osf.io", "repo.nii.ac.jp",
                     "hdl.handle.net", "zenodo", "researchgate")


def classify(code, ctype, final):
    """What must a human DO about this failure?"""
    host = (final or "").lower()
    if any(h in host for h in PAYWALL_HOSTS):
        return "proxy"
    if any(h in host for h in OPEN_BUT_DEFENDED):
        return "browser"
    if code in ("401", "402", "403") and "cloudflare" not in (final or "").lower():
        return "browser" if code == "403" else "proxy"
    if code in ("429", "503", "202"):
        return "browser"
    if code in ("404", "410"):
        return "dead"
    if code.startswith("2") and "html" in (ctype or ""):
        return "browser"          # a 200 HTML body where a PDF was expected: shell or challenge
    if code == "000":
        return "browser"          # connection reset / TLS refusal, usually bot defence
    return "proxy"


def unwrap(u):
    """Redirect wrappers hide the real target."""
    if not u:
        return u
    m = re.search(r"redir\.pf/[^?]*\?.*?url=([^&]+)", u) or re.search(r"[?&]url=(https?[^&]+)", u)
    if m:
        from urllib.parse import unquote
        return unquote(m.group(1))
    return u


def citation_pdf_url(html, base):
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url', html, re.I)
    if not m:
        return None
    u = m.group(1)
    if u.startswith("//"):
        u = "https:" + u
    elif u.startswith("/"):
        from urllib.parse import urljoin
        u = urljoin(base, u)
    return u



# Publishers the UChicago proxy can be expected to reach. A `proxy` handoff tells a human to try the
# library, and telling them that about a venue the library does not license wastes the one expensive
# resource this pipeline has. Classification is by CROSSREF PUBLISHER, looked up per failure, not by
# guessing from the DOI prefix.
PROXY_REACHABLE = ("elsevier", "springer", "wiley", "informa", "taylor", "sage", "oxford",
                   "cambridge", "university of chicago", "de gruyter", "emerald", "jstor",
                   "american economic", "royal society", "nature", "ithaka", "project muse",
                   "duke university", "mit press", "brill", "palgrave", "routledge")


def reclassify_regional(rows):
    """Split `proxy` into `proxy` and `regional` on measured publisher, not on assumption.

    Pre-registered in this script's docstring before the run: regional Chinese and Korean venues
    (CNKI, KCI, DBpia and their DOI registrars) are frequently outside BOTH open access and the
    UChicago proxy, which makes them a third handoff kind. The first run classified `China Soft
    Science` (China Science Publishing & Media) and an Asia Europe Perspective Association title as
    `proxy`, which would have sent a human to a library that does not license them.
    """
    moved = 0
    for r in rows:
        if r.get("handoff") != "proxy" or not r.get("doi"):
            continue
        out = subprocess.run(["curl", "-s", "--max-time", "25",
                              f"https://api.crossref.org/works/{r['doi']}"],
                             capture_output=True, text=True)
        try:
            m = json.loads(out.stdout)["message"]
        except Exception:
            continue                       # a lookup failure is not evidence either way
        pub = (m.get("publisher") or "").lower()
        r["publisher"] = m.get("publisher")
        r["container"] = (m.get("container-title") or [None])[0]
        if pub and not any(k in pub for k in PROXY_REACHABLE):
            r["handoff"] = "regional"
            r["handoff_reason"] = (f"publisher '{m.get('publisher')}' is outside the set the "
                                   f"UChicago proxy can be expected to reach; needs an ILL request "
                                   f"or a direct approach to the venue, not the proxy")
            moved += 1
        time.sleep(0.2)
    return moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default="1,2,3")
    args = ap.parse_args()
    tiers = {int(x) for x in args.tier.split(",")}

    verdicts = {r["screen_id"]: r for r in
                csv.DictReader((ROOT / "extraction" /
                                "rising-inequality-and-status-competition-screen-verdicts.csv").open())}
    uni = json.loads((LOGS / "rising-inequality-and-status-competition-screen-universe.json").read_text())["records"]
    for i, r in enumerate(uni):
        r["screen_id"] = f"C2F{i:04d}"
    by_id = {r["screen_id"]: r for r in uni}

    want = []
    for sid, v in verdicts.items():
        t = (1 if v["verdict"] == "INCLUDE_PRIMARY" else
             2 if (v["verdict"] == "BOUNDARY" and v["cell"] in PRIMARY_CELLS) else
             3 if v["cell"] in CONTEXT_CELLS else None)
        if t in tiers:
            want.append({**by_id[sid], "tier": t, "cell": v["cell"], "verdict": v["verdict"],
                         "note": v["note"]})
    print(f"{len(want)} records to retrieve: " +
          ", ".join(f"tier{t} {n}" for t, n in sorted(Counter(w['tier'] for w in want).items())))

    # ---- metadata with locations, in batches. `ids.openalex:` takes many ids per request.
    oa = OpenAlex(KEY, MAILTO, LOGS / ".cache" / "c2f-retrieval-meta.json")
    SELECT = "id,doi,ids,display_name,publication_year,type,locations,best_oa_location,open_access"
    meta = {}
    oaids = [w["oa_id"] for w in want if w.get("oa_id")]
    for i in range(0, len(oaids), 45):
        chunk = oaids[i:i + 45]
        d, err = oa.get({"filter": f"ids.openalex:{'|'.join(chunk)}", "per-page": "50",
                         "select": SELECT})
        if err:
            sys.exit(f"metadata batch {i // 45} refused, NOTHING WRITTEN: {err[:200]}")
        for w in d.get("results", []):
            meta[(w.get("id") or "").rsplit("/", 1)[-1]] = w
    print(f"metadata for {len(meta)}/{len(oaids)} records\n")

    prior = {}
    pj = LOGS / "rising-inequality-and-status-competition-retrieval.json"
    if pj.exists():
        try:
            prior = {r["screen_id"]: r for r in json.loads(pj.read_text()).get("records", [])}
        except (json.JSONDecodeError, KeyError):
            prior = {}

    PDFS.mkdir(parents=True, exist_ok=True)
    # `sibling_version` is the rung that matters in economics. The journal version is behind
    # Elsevier/Wiley/Cambridge/SSRN bot defence; the SAME STUDY sits open on NBER, IZA, EconStor or
    # RePEc under a different OpenAlex id. version-pair-is-one-study, applied to RETRIEVAL: the unit
    # that must be retrieved is the study, not the record, and a fetched twin covers its siblings.
    rungs = ["wp_host", "oa_location", "sibling_version", "unpaywall", "pmc_bioc"]
    counters = {r: Counter() for r in rungs}
    out = []

    for w in want:
        m = meta.get(w.get("oa_id") or "", {})
        locs = [l for l in (m.get("locations") or []) if l]
        best = m.get("best_oa_location") or {}
        doi = (m.get("doi") or w.get("doi") or "")
        doi = doi.replace("https://doi.org/", "")
        pmid = ((m.get("ids") or {}).get("pmid") or "").rsplit("/", 1)[-1]
        dest = PDFS / f"{w['screen_id']}.pdf"
        rec = {"screen_id": w["screen_id"], "tier": w["tier"], "cell": w["cell"],
               "title": w.get("title"), "year": w.get("year"), "doi": doi or None,
               "attempts": [], "status": None, "path": None, "handoff": None}
        if dest.exists() and is_pdf(dest):
            rec["status"] = "already_on_disk"; rec["path"] = str(dest.relative_to(ROOT))
            pr = prior.get(w["screen_id"]) or {}
            rec["rung"] = pr.get("rung")          # carried forward, never re-invented
            rec["attempts"] = pr.get("attempts", [])
            if not rec["rung"]:
                rec["rung_unknown"] = True
            out.append(rec); continue

        # candidate URLs per rung, working-paper hosts FIRST for this literature
        cand = defaultdict(list)
        for l in locs + ([best] if best else []):
            u = unwrap(l.get("pdf_url") or l.get("landing_page_url"))
            if not u:
                continue
            host = (l.get("source") or {}).get("host_organization_name") or ""
            key = "wp_host" if any(h in u.lower() or h in host.lower() for h in WP_HOSTS) \
                else "oa_location"
            if u not in cand[key]:
                cand[key].append(u)

        got = False
        for rung in rungs:
            if got:
                break
            rec.setdefault("probed", []).append(rung)
            urls = list(cand.get(rung, []))
            if rung == "unpaywall" and doi:
                d = body(f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}", 30)
                try:
                    j = json.loads(d)
                    for loc in ([j.get("best_oa_location")] + (j.get("oa_locations") or [])):
                        if loc and (loc.get("url_for_pdf") or loc.get("url")):
                            urls.append(loc.get("url_for_pdf") or loc.get("url"))
                except (json.JSONDecodeError, TypeError):
                    pass
            if rung == "sibling_version":
                d, err = oa.get({"filter": f'title.search:"{(w.get("title") or "")[:120]}"',
                                 "per-page": "12", "select": SELECT})
                if not err:
                    for sib in d.get("results", []):
                        if (sib.get("id") or "").rsplit("/", 1)[-1] == w.get("oa_id"):
                            continue
                        sl = [x for x in (sib.get("locations") or []) if x]
                        if sib.get("best_oa_location"):
                            sl.append(sib["best_oa_location"])
                        for l in sl:
                            su = unwrap(l.get("pdf_url") or l.get("landing_page_url"))
                            if su:
                                urls.append(su)
                    # open hosts first: they are the reason this rung exists
                    urls.sort(key=lambda u: 0 if any(h in u.lower() for h in WP_HOSTS) else 1)
            if rung == "pmc_bioc" and pmid:
                # OpenAlex carries no pmcid; bridge from pmid (openalex-lacks-pmcid-bridge-from-pmid)
                d = body("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids="
                         f"{pmid}&format=json", 30)
                mm = re.search(r'"pmcid"\s*:\s*"(PMC\d+)"', d)
                if mm:
                    urls.append("https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/"
                                f"BioC_json/{mm.group(1)}/unicode")
            urls = [u for u in dict.fromkeys(urls) if u]
            if urls:
                rec.setdefault("found", []).append(rung)
            for u in urls[:8]:
                code, ctype, final = curl(u, out=dest, timeout=75)
                ok = is_pdf(dest)
                if not ok and code.startswith("2") and "html" in (ctype or ""):
                    # a landing page: ask it for its own PDF
                    pu = citation_pdf_url(body(final or u), final or u)
                    if pu:
                        code, ctype, final = curl(pu, out=dest, timeout=75)
                        ok = is_pdf(dest)
                        u = pu
                rec["attempts"].append({"rung": rung, "url": u[:180],
                                        "final": (final or u)[:180], "http": code,
                                        "ctype": (ctype or "")[:40], "pdf": ok})
                if ok:
                    rec["status"] = "fetched"; rec["rung"] = rung
                    rec["path"] = str(dest.relative_to(ROOT))
                    got = True
                    break
                dest.unlink(missing_ok=True)
                time.sleep(0.4)
        if not got:
            rec["status"] = "failed"
            # classify on where the request LANDED, never on the redirector it started from
            fails = [classify(a["http"], a["ctype"], a.get("final") or a["url"])
                     for a in rec["attempts"]]
            rec["handoff"] = ("none" if not rec["attempts"]
                              else "proxy" if "proxy" in fails
                              else "browser" if "browser" in fails
                              else "dead")
        out.append(rec)
        print(f"  {rec['screen_id']} t{rec['tier']} {rec['status']:16} "
              f"{rec.get('rung') or rec.get('handoff') or '':12} {(w.get('title') or '')[:52]}")

    # Rung table computed from the FINAL record set, so it is the same after a re-run.
    for r in out:
        pr = prior.get(r["screen_id"]) or {}
        for k in ("probed", "found"):
            if not r.get(k) and pr.get(k):
                r[k] = pr[k]
        for rg in r.get("probed", []):
            counters[rg]["probed"] += 1
        for rg in r.get("found", []):
            counters[rg]["found"] += 1
        if r.get("rung"):
            counters[r["rung"]]["fetched"] += 1

    n_ok = sum(1 for r in out if r["status"] in GOT)
    # Studies, not records. Three retrieved records of one Ghana RCT is one study retrieved.
    def fold(t):
        return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()[:60]
    studies = defaultdict(list)
    for r in out:
        studies[fold(r["title"])].append(r)
    covered = {k for k, v in studies.items()
               if any(x["status"] in GOT for x in v)}
    for r in out:
        if r["status"] == "failed" and fold(r["title"]) in covered:
            r["status"] = "covered_by_twin"
            r["handoff"] = None
    (LOGS / "rising-inequality-and-status-competition-retrieval.json").write_text(
        json.dumps({"n": len(out), "retrieved": n_ok,
                    "studies": len(studies), "studies_covered": len(covered),
                    "rungs": {k: dict(v) for k, v in counters.items()},
                    "records": out}, indent=1) + "\n")

    L = ["# C.2.f full-text retrieval", "",
         "Generated by `source/build/goldset/342_c2f_fulltext_retrieval.py`. Do not edit by hand.",
         "", f"**{len(covered)} of {len(studies)} STUDIES retrieved** "
         f"({n_ok} of {len(out)} records).", "",
         "Coverage is counted per STUDY. Three records of the Ghana free-secondary RCT are one "
         "study, and a fetched twin covers its siblings — the unit that has to reach extraction is "
         "the study (`version-pair-is-one-study`).", "",
         "## Per rung: probed, found, fetched", "",
         "Three counters, never one. A rung that produced URLs and fetched nothing is a DIFFERENT "
         "problem from a rung that produced nothing, and collapsing them is how PMC and Unpaywall "
         "read as dead while holding 27 and 65 URLs on A.17 "
         "(`rung-found-is-not-rung-fetched`).", "",
         "Attribution is carried forward across re-runs: a file already on disk keeps the rung "
         "that won it. The first version of this table incremented counters as run-time events, so "
         "a second run reported `fetched 0` on every rung while 25 PDFs sat on disk "
         "(`stage-output-must-survive-rerun`).", "",
         "| rung | probed | found a URL | fetched a PDF |", "|---|---|---|---|"]
    for r in rungs:
        c = counters[r]
        L.append(f"| `{r}` | {c['probed']} | {c['found']} | **{c['fetched']}** |")
    by_tier = defaultdict(Counter)
    for r in out:
        by_tier[r["tier"]][r["status"]] += 1
    L += ["", "## By tier", "", "| tier | n | retrieved | failed |", "|---|---|---|---|"]
    for t in sorted(by_tier):
        c = by_tier[t]
        got = sum(c[k] for k in GOT)
        L.append(f"| {t} | {sum(c.values())} | **{got}** | {c['failed']} |")
    hand = Counter(r["handoff"] for r in out if r["status"] == "failed")
    L += ["", "## Handoff — classified by what a human must DO", "",
          "A blocked route is not a paywall: on A.17, 67 of 98 failures were open URLs killed by bot "
          "defence, and filing them as paywalled would have sent the wrong job to the wrong person "
          "(`blocked-route-is-not-a-paywall`).", "",
          "| job | n | what it needs |", "|---|---|---|",
          f"| `browser` | {hand['browser']} | a logged-in browser session; the URL is open but "
          "defended |",
          f"| `proxy` | {hand['proxy']} | the UChicago proxy; genuinely paywalled |",
          f"| `dead` | {hand['dead']} | 404/410 — find another version or drop |",
          f"| `none` | {hand['none']} | no URL was ever produced by any rung |", "",
          "## Every record", "",
          "| id | tier | cell | status | rung / job | title |", "|---|---|---|---|---|---|"]
    for r in sorted(out, key=lambda r: (r["tier"], r["screen_id"])):
        L.append(f"| {r['screen_id']} | {r['tier']} | `{r['cell']}` | {r['status']} | "
                 f"{r.get('rung') or r.get('handoff') or ''} | {(r['title'] or '')[:52]} |")
    L.append("")
    (LOGS / "rising-inequality-and-status-competition-retrieval.md").write_text("\n".join(L))

    # ---- two actionable handoff files, tier 1 first: the primary cell gates extraction
    moved = reclassify_regional([r for r in out if r.get("status") != "fetched"])
    if moved:
        print(f"  reclassified {moved} proxy -> regional on measured Crossref publisher")

    for job, need in (("proxy", "the UChicago proxy (or a library login)"),
                      ("browser", "a real logged-in browser session; these URLs are OPEN but "
                                  "refuse curl"),
                      ("regional", "an ILL request or a direct approach to the venue. These are "
                                   "regional Chinese/Korean publishers the UChicago proxy cannot "
                                   "be expected to license, measured from the Crossref publisher "
                                   "field rather than assumed — telling a human to 'try the proxy' "
                                   "for these would waste the one expensive resource here")):
        rows_j = sorted([r for r in out if r.get("handoff") == job],
                        key=lambda r: (r["tier"], r["screen_id"]))
        H = [f"# C.2.f retrieval handoff — {job} jobs ({len(rows_j)})", "",
             "Generated by `source/build/goldset/342_c2f_fulltext_retrieval.py`. Do not edit by "
             "hand.", "",
             f"These need **{need}**.", "",
             "**Tier 1 first.** Tier 1 is the primary cell and it gates extraction; tier 2 is the "
             "boundary packet whose `channel` must be read at full text before routing; tier 3 is "
             "context.", "",
             "Save each as `literature/pdfs/rising-inequality-and-status-competition/<id>.pdf`. Script 315's "
             "content-matching installer should be used rather than trusting the publisher's "
             "filename (`handoff-file-match-by-content`).", "",
             "| id | tier | cell | year | DOI | title | last URL tried |",
             "|---|---|---|---|---|---|---|"]
        for r in rows_j:
            last = (r["attempts"][-1].get("final") or r["attempts"][-1]["url"]) if r["attempts"] else ""
            H.append(f"| {r['screen_id']} | {r['tier']} | `{r['cell']}` | {r.get('year') or ''} | "
                     f"{r['doi'] or ''} | {(r['title'] or '')[:60]} | {last[:70]} |")
        H.append("")
        (LOGS / f"rising-inequality-and-status-competition-handoff-{job}.md").write_text("\n".join(H))
    print(f"handoff files written: proxy, browser and regional")
    # Recomputed AFTER reclassify_regional, not carried from the fetch loop: the first version
    # printed the pre-reclassification counter, so the summary disagreed with the files on disk.
    # GOT, not the literal "fetched": a re-run reports `already_on_disk`, and a twin-covered record
    # reports `covered_by_twin`. Checking one literal made this print 0/19 primary coverage against
    # a true 7/19 -- the same shape as the id-format mismatch in 340's enrichment.
    hand_final = Counter(r["handoff"] for r in out
                         if r["status"] not in GOT and r.get("handoff"))
    print(f"\nSTUDIES {len(covered)}/{len(studies)} covered; records {n_ok}/{len(out)}; "
          f"handoff {dict(hand_final)}")
    prim = [r for r in out if r.get("cell") in PRIMARY_CELLS]
    got = sum(1 for r in prim if r["status"] in GOT)
    print(f"PRIMARY CELL coverage {got}/{len(prim)} — read this, not the overall rate "
          f"(`retrieval-rate-hides-which-records`)")
    for c in sorted(PRIMARY_CELLS):
        rs = [r for r in out if r.get("cell") == c]
        if rs:
            g = sum(1 for r in rs if r["status"] in GOT)
            flag = "   <-- EMPTY" if g == 0 else ""
            print(f"    {g}/{len(rs)}  {c}{flag}")
    print(f"requests: {POOL['key']} keyed, {POOL['polite']} keyless, {POOL['refused']} refused")


main()
