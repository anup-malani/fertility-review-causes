#!/usr/bin/env python3
"""TICK-049: multi-aggregator retrieval sweep for the stated-sample shortfall.

`82_d3b_retrieve_pdfs.py` queries OpenAlex and Unpaywall. That is two sources, and the
D.3.b run has already shown once that "no PDF" from those two can mean "no `pdf_url`
field", not "no copy exists" — three gold/diamond-OA studies were being logged unreachable
because OpenAlex returned only landing pages.

Before declaring the sampled studies unobtainable and handing 14 DOIs to a human, this
script sweeps every aggregator that indexes full text and reports, per DOI, every candidate
it found and whether that candidate actually yields a verified PDF:

  OpenAlex locations · Unpaywall oa_locations · Semantic Scholar openAccessPdf ·
  CORE v3 · Europe PMC · OpenAIRE · publisher/repository URL templates

Non-response is the live threat to the sample (see the stated-sample log): if retrieval
over the SAMPLE falls below about two thirds, the realised sample is no longer random and
the Wall 1 bleed-in estimate loses its warrant. So the marginal PDF here is worth more than
the same PDF elsewhere in the corpus, and it is worth querying six sources rather than two.

Outputs:
  extraction/{slug}-deep-retrieval-report.md
  literature/pdfs/{slug}/  (any PDF recovered, in the W<id>__ convention)
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import time
from pathlib import Path

SLUG = "climate-anxiety-eco-doomerism"
ROOT = Path(__file__).resolve().parents[3]
TARGETS = ROOT / "extraction" / f"{SLUG}-stated-sample-retrieval-list.csv"
PDF_DIR = ROOT / "literature" / "pdfs" / SLUG
REPORT = ROOT / "extraction" / f"{SLUG}-deep-retrieval-report.md"
MAILTO = "shravanh@uchicago.edu"
UA = "Mozilla/5.0 (fertility-review-causes; mailto:shravanh@uchicago.edu)"


def curl_json(url: str, timeout: int = 35) -> dict:
    try:
        p = subprocess.run(["curl", "-sL", "--max-time", str(timeout), "-A", UA, url],
                           check=True, capture_output=True)
        return json.loads(p.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}


def slugify(t: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")
    return s[:60] or "untitled"


def from_openalex(doi: str) -> list[str]:
    w = curl_json(f"https://api.openalex.org/works/doi:{doi}"
                  f"?select=open_access,best_oa_location,primary_location,locations&mailto={MAILTO}")
    out = []
    for loc in (w.get("locations") or []):
        if loc.get("pdf_url"):
            out.append(loc["pdf_url"])
    for k in ("best_oa_location", "primary_location"):
        if (w.get(k) or {}).get("pdf_url"):
            out.append(w[k]["pdf_url"])
    if (w.get("open_access") or {}).get("oa_url"):
        out.append(w["open_access"]["oa_url"])
    return out


def from_unpaywall(doi: str) -> list[str]:
    d = curl_json(f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}")
    out = []
    for loc in (d.get("oa_locations") or []):
        for k in ("url_for_pdf", "url"):
            if loc.get(k):
                out.append(loc[k])
    return out


def from_semanticscholar(doi: str) -> list[str]:
    d = curl_json(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
                  "?fields=openAccessPdf,externalIds")
    out = []
    if (d.get("openAccessPdf") or {}).get("url"):
        out.append(d["openAccessPdf"]["url"])
    return out


def from_core(doi: str) -> list[str]:
    d = curl_json(f"https://api.core.ac.uk/v3/search/works?q=doi:%22{doi}%22&limit=3")
    out = []
    for r in (d.get("results") or []):
        for k in ("downloadUrl", "fullTextIdentifier"):
            if r.get(k):
                out.append(r[k])
        for u in (r.get("sourceFulltextUrls") or []):
            out.append(u)
    return out


def from_europepmc(doi: str) -> list[str]:
    d = curl_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                  f"?query=DOI:%22{doi}%22&resultType=core&format=json")
    out = []
    for r in ((d.get("resultList") or {}).get("result") or []):
        pmcid = r.get("pmcid")
        if pmcid:
            out.append(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextPDF")
        for ft in ((r.get("fullTextUrlList") or {}).get("fullTextUrl") or []):
            if ft.get("url"):
                out.append(ft["url"])
    return out


def from_openaire(doi: str) -> list[str]:
    try:
        p = subprocess.run(
            ["curl", "-sL", "--max-time", "35", "-A", UA,
             f"https://api.openaire.eu/search/publications?doi={doi}&size=3"],
            check=True, capture_output=True)
        body = p.stdout.decode("utf-8", "ignore")
    except subprocess.CalledProcessError:
        return []
    return [u for u in re.findall(r"<url>(https?://[^<]+)</url>", body)]


def templates(doi: str) -> list[str]:
    out = []
    m = re.match(r"10\.21203/rs\.3\.(rs-\d+)/v(\d+)", doi)
    if m:
        out.append(f"https://www.researchsquare.com/article/{m.group(1)}/v{m.group(2)}.pdf")
    if doi.startswith("10.1371/"):
        out.append(f"https://journals.plos.org/plosone/article/file?id={doi}&type=printable")
    return out


SOURCES = [("openalex", from_openalex), ("unpaywall", from_unpaywall),
           ("semanticscholar", from_semanticscholar), ("core", from_core),
           ("europepmc", from_europepmc), ("openaire", from_openaire),
           ("template", lambda d: templates(d))]


def try_download(url: str, dest: Path) -> tuple[bool, str]:
    tmp = dest.with_suffix(".part")
    try:
        subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, "-o", str(tmp), url],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return False, f"curl_{e.returncode}"
    if not tmp.exists() or tmp.stat().st_size < 1024:
        tmp.unlink(missing_ok=True)
        return False, "empty"
    with open(tmp, "rb") as fh:
        head = fh.read(4)
    if head != b"%PDF":
        tmp.unlink(missing_ok=True)
        return False, "not_pdf"
    tmp.rename(dest)
    return True, "ok"


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    targets = list(csv.DictReader(open(TARGETS)))
    results = []

    for t in targets:
        doi, wid = t["doi"], t["work_id"]
        dest = PDF_DIR / f"{wid}__{slugify(t['title'])}.pdf"
        if dest.exists():
            results.append({**t, "outcome": "already_present", "via": "", "tried": 0})
            continue
        found: list[tuple[str, str]] = []
        for name, fn in SOURCES:
            try:
                for u in fn(doi):
                    if u and (name, u) not in found:
                        found.append((name, u))
            except Exception:
                pass
            time.sleep(0.25)

        seen, outcome, via, why = set(), "failed", "", []
        for name, url in found:
            if url in seen:
                continue
            seen.add(url)
            ok, reason = try_download(url, dest)
            why.append(f"{name}:{reason}")
            if ok:
                outcome, via = "RECOVERED", f"{name} -> {url[:90]}"
                break
            time.sleep(0.2)
        if not found:
            outcome, why = "no_candidates", ["no aggregator returned any URL"]
        results.append({**t, "outcome": outcome, "via": via,
                        "tried": len(seen), "detail": "; ".join(why[:8])})

    rec = [r for r in results if r["outcome"] == "RECOVERED"]
    pres = [r for r in results if r["outcome"] == "already_present"]
    fail = [r for r in results if r["outcome"] in ("failed", "no_candidates")]

    lines = [f"# Deep retrieval sweep — stated sample — {SLUG}", "",
             "Generated by `source/build/goldset/88_d3b_deep_retrieve.py`. Seven sources per DOI:",
             "OpenAlex, Unpaywall, Semantic Scholar, CORE, Europe PMC, OpenAIRE, and publisher",
             "templates. Run because this project has already seen OpenAlex report gold OA as",
             "closed when it held only a landing page, and because non-response is the live",
             "threat to the sample's randomness.", "",
             f"**Recovered {len(rec)} · already present {len(pres)} · still missing {len(fail)}**", ""]
    if rec:
        lines += ["## Recovered", "", "| DOI | Venue | Found via |", "|---|---|---|"]
        lines += [f"| `{r['doi']}` | {r['venue'][:34]} | {r['via'][:80]} |" for r in rec]
        lines.append("")
    if fail:
        lines += ["## Still missing — needs a human", "",
                  "| Access | DOI | Venue | What was tried |", "|---|---|---|---|"]
        lines += [f"| {r['access_class']} | `{r['doi']}` | {r['venue'][:28]} | "
                  f"{r.get('detail','')[:90]} |" for r in fail]
        lines += ["",
                  "`oa_but_blocked` rows are free to read and refuse only a non-browser client —",
                  "a browser gets them with no entitlement. `closed` rows need the UChicago proxy",
                  "or ILL, or an author request.", ""]
    lines += ["## Effect on the sample", "",
              "Non-response threshold from the stated-sample log: below about two thirds retrieval",
              "over the sample, the realised sample is no longer random and the Wall 1 bleed-in",
              "rate loses its warrant. Recompute against the 22 selected after any retrieval round."]
    REPORT.write_text("\n".join(lines) + "\n")

    print(f"recovered {len(rec)} | already present {len(pres)} | still missing {len(fail)}")
    for r in rec:
        print(f"  + {r['doi']}  via {r['via'][:70]}")
    for r in fail:
        print(f"  - {r['doi']} ({r['access_class']}) tried={r['tried']}")
    print(f"report -> {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
