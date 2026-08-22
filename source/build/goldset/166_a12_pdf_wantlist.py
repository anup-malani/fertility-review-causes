#!/usr/bin/env python3
"""
166_a12_pdf_wantlist.py — A.12, stage 5 prep. Build the retrieval wantlist and measure the OA ceiling.

Inherits `139_b6_pdf_wantlist.py`. Checks open-access status LIVE before writing, so the list states
what an automated fetch can reach and what needs a human with a library proxy BEFORE the fetch rather
than after. B.1 found that distinction the expensive way — its automated ceiling hit 20 of 95 and its
pooled estimate has rested on five studies since.

**THE JOB THAT SHAPES THIS SCRIPT IS JOB B, AND IT IS A DIFFERENT PROBLEM FROM ANY PRIOR CHAPTER.**
The screen produced 223 `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` records, every one of them UNCERTAIN by
construction: Wall 8 declares the first-stage table invisible at title and abstract, so nothing in the
visible record can tell us which of the 223 actually estimates the completed-fertility response to a
twin birth. The honest options are to retrieve all 223, or to state a priority rule and record what it
deprioritises. Retrieving 223 full texts to harvest a nuisance table is not proportionate, so this
script states the rule:

  B1  the METHODS entry points. Four records that survey the twin instrument itself — an Oxford
      handbook chapter on twins methods in economics, Rosenzweig & Wolpin's own JEL review of natural
      experiments, a Journal of Economic Surveys review of fertility and causality, and a twins-data
      methods paper. A methods survey discusses many first stages at once, which is the only
      efficient route into a cell the screen cannot see into. HIGHEST priority.
  B2  records carrying BOTH a twinning term and the IV-design vocabulary (`twin_iv_shape` from D1).
      These plausibly run the twin design specifically.
  B3  records carrying the design vocabulary but NO twinning term. The bypass admitted these
      deliberately — instruments go unnamed in abstracts too — but they include sibling-sex-composition
      and one-child-policy designs that have no twin first stage at all. DEPRIORITISED, and the count
      is reported rather than quietly dropped.

B3 is the honest cost of the Wall 8 bypass's deliberate breadth, and it is stated here so that the
chapter's first-stage synthesis can say what it did not read.

THE OTHER JOBS:
  A  `PRIMARY_OFFSET_STOPPING` (all). The causal spine, the only cell earning GRADE credit, and the
     cell the screen grew from 3 to 14. All are retrieved, including the ones that disagree with each
     other — especially those.
  C  `SECONDARY_ART_MULTIPLES`, split by outcome. The population/registry arm is the Wall 6 include
     side and is retrieved in full; the per-cycle arm is retrieved only for the highest-grade designs
     (randomised trials, meta-analyses, Cochrane, national policy evaluations) because 100 per-cycle
     records cannot each carry a demographic quantity.
  D  `EXPOSURE_SERIES`, selected by RULE from the screen notes rather than hand-listed, so the set is
     reproducible and re-runs identically if the screen is revised. The rule targets the records that
     carry the identity's CORRECTIONS (vanishing twin, twin mortality, measurement) and the age/ART
     DECOMPOSITION — not the hundreds of country-year tabulations, whose numbers come from the HMBD
     directly and do not need a PDF.
  E  `SECONDARY_PM_VARIATION`, a bounded sample. Call 5 reduces the PM arm to a bounded arithmetic
     statement, so the retrieval is sized to bound a range, not to synthesise a literature.

**Read the OA rate by job, not in aggregate.** If OA status correlates with job — and it will, since
JOB B is economics working papers and preprints while JOB C is clinical journals — then an OA-only
evidence base would systematically over-represent whichever arm publishes more openly. The report
breaks the rate down for that reason.

Target paths follow the house convention `literature/pdfs/{slug}/{WID}__{title-slug}.pdf`, so a file
dropped there is picked up by ingest without renaming. That directory is gitignored.

Output: literature/search-logs/{slug}-pdf-wantlist.md
        extraction/{slug}-retrieval-dois.txt
        extraction/{slug}-oa-status.json
"""
import json, os, re, subprocess, time
from collections import Counter

SLUG = "twinning-multiple-births"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
RANKED = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-pdf-wantlist.md")
OUT_DOI = os.path.join(EXTRACT, f"{SLUG}-retrieval-dois.txt")
OUT_OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}

# JOB B1 — the four methods entry points, named because they are individually identified rather than
# rule-selected: a survey of the instrument is the only thing that reads many first stages at once.
B1_IDS = {"W2224629890": "Oxford handbook chapter, twins methods in economics",
          "W2150439610": "Rosenzweig & Wolpin, JEL review of natural experiments — by the twin instrument's own authors",
          "W2604712881": "Journal of Economic Surveys, fertility and causality",
          "W2013583398": "social-science methods for twins data"}

# JOB D selection rules, keyed on the screen note so the set is derived and reproducible.
# Legend: `v` vanishing twin, `d` age/ART decomposition, `m` measurement and zygosity method,
# `g` DZ genetics and mechanism, `h` historical/long series, `r` registry.
D_RULES = [("v", ("vanishing", "VANISHING", "conceived multiple", "foetal reduction", "fetal reduction")),
           ("d", ("decompos", "AGE-PERIOD-COHORT", "delayed childbearing", "age-twinning",
                  "age gradient", "maternal age", "age-dependent", "endogeneity finding")),
           ("m", ("Weinberg", "measurement", "MEASUREMENT", "ascertain", "under-registration",
                  "risk-of-bias", "RISK-OF-BIAS", "epigenetic")),
           ("g", ("GWAS", "heritability", "DZ heritability", "polygenic", "ovulation", "FSH",
                  "endocrine", "linkage")),
           ("h", ("1751", "1841", "1540", "historical", "longest", "series since", "18th", "19th")),
           ("r", ("registry", "surveillance", "vital-statistics", "HMBD"))]

HIGH_GRADE = ("RANDOMISED", "randomised", "RANDOMIZED", "meta-analysis", "META-ANALYSIS",
              "COCHRANE", "Cochrane", "systematic review", "POLICY", "LEGISLATION", "guideline",
              "policy comparison", "CALL 3 CASE", "INCLUDE SIDE", "bounds", "BOUNDS", "quantifies",
              "QUANTIFIES")


def oa_lookup(ids):
    """Batch OpenAlex for OA status. A failed request is UNCONFIRMED, never 'closed'."""
    out = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        url = ("https://api.openalex.org/works?filter=openalex_id:" + "|".join(chunk) +
               "&per-page=50&select=id,doi,open_access,best_oa_location,type,primary_location"
               f"&mailto={MAILTO}")
        payload = None
        for attempt in range(3):
            r = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, url],
                               capture_output=True, text=True)
            try:
                d = json.loads(r.stdout)
            except Exception:
                d = {}
            if "results" in d:
                payload = d
                break
            time.sleep(1.5 * (attempt + 1))
        if payload is None:
            for c in chunk:
                out[c] = {"status": "UNCONFIRMED", "url": None,
                          "note": "request failed — not evidence of closure"}
            continue
        seen = set()
        for w in payload["results"]:
            wid = (w.get("id") or "").rsplit("/", 1)[-1]
            seen.add(wid)
            oa = w.get("open_access") or {}
            loc = w.get("best_oa_location") or {}
            out[wid] = {"status": (oa.get("oa_status") or "closed"),
                        "url": loc.get("pdf_url") or loc.get("landing_page_url"),
                        "doi": w.get("doi"), "type": w.get("type")}
        for c in chunk:
            if c not in seen:
                out[c] = {"status": "not_in_index", "url": None}
        time.sleep(0.3)
    return out


def main():
    rows = json.load(open(SCREENED))
    ranked = {r["id"]: r for r in json.load(open(RANKED))}
    for r in rows:
        d1 = ranked.get(r["id"], {})
        r["twin_iv_shape"] = bool(d1.get("twin_iv_shape"))
        r["twin_hits"] = d1.get("twin_hits") or []

    jobs = {}
    def put(job, r, why):
        jobs.setdefault(job, []).append({**r, "why": why})

    for r in rows:
        cell, note, ot = r["cell"], (r.get("screen_note") or ""), r.get("outcome_type")
        if cell == "PRIMARY_OFFSET_STOPPING":
            put("A", r, "causal spine")
        elif cell == "PRIMARY_MECHANICAL_IDENTITY":
            put("A", r, "mechanical identity")
        elif cell == "PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE":
            if r["id"] in B1_IDS:
                put("B1", r, B1_IDS[r["id"]])
            elif r["twin_iv_shape"] or r["twin_hits"]:
                put("B2", r, "carries a twinning term with the IV-design vocabulary")
            else:
                put("B3", r, "design vocabulary but NO twinning term — deprioritised")
        elif cell == "SECONDARY_ART_MULTIPLES":
            if ot in ("population_births", "twinning_rate"):
                put("C1", r, "Wall 6 INCLUDE side: population or registry outcome")
            elif any(t in note for t in HIGH_GRADE):
                put("C2", r, "per-cycle, retained for design grade")
            else:
                put("C3", r, "per-cycle, routine design — deprioritised")
        elif cell == "EXPOSURE_SERIES":
            tags = [k for k, pats in D_RULES if any(p in note for p in pats)]
            if tags:
                put("D", r, "exposure-series rule: " + "".join(sorted(set(tags))))
            else:
                put("D_skip", r, "country-year tabulation — numbers come from HMBD, no PDF needed")
        elif cell == "SECONDARY_PM_VARIATION":
            put("E", r, "PM bound")

    want = [x for j in ("A", "B1", "B2", "C1", "C2", "D", "E") for x in jobs.get(j, [])]
    ids = [x["id"] for x in want]
    oa = oa_lookup(ids)
    for x in want:
        x["oa"] = oa.get(x["id"], {"status": "UNCONFIRMED", "url": None})
    json.dump({x["id"]: x["oa"] for x in want}, open(OUT_OA, "w"), indent=2)
    with open(OUT_DOI, "w") as fh:
        for x in want:
            if x.get("doi"):
                fh.write(x["doi"].replace("https://doi.org/", "") + "\n")

    def rate(items):
        n = len(items)
        o = sum(1 for x in items if x["oa"]["status"] in OPEN)
        u = sum(1 for x in items if x["oa"]["status"] == "UNCONFIRMED")
        return n, o, u, (f"{o/n*100:.0f}%" if n else "n/a")

    JOBDESC = [
        ("A", "the causal spine — every stopping-offset record, including the ones that disagree"),
        ("B1", "methods entry points into the Wall 8 cell"),
        ("B2", "first-stage candidates carrying a twinning term"),
        ("C1", "ART multiples, Wall 6 INCLUDE side (population/registry outcome)"),
        ("C2", "ART multiples, per-cycle but high design grade"),
        ("D", "exposure-series records carrying the identity's CORRECTIONS and the decomposition"),
        ("E", "PM variation, sized to bound a range"),
    ]
    L = [f"# Stage 5 retrieval wantlist and OA ceiling — {SLUG} (A.12)", "",
         f"**{len(want)} records to retrieve**, out of {len(rows):,} screened. Selection is by rule "
         "from the screen output, not by hand, so it re-runs identically if the screen is revised.", "",
         "| job | what it is | n | open | UNCONFIRMED | OA rate |", "|---|---|---|---|---|---|"]
    for j, desc in JOBDESC:
        n, o, u, pct = rate(jobs.get(j, []))
        L.append(f"| **{j}** | {desc} | {n} | {o} | {u} | **{pct}** |")
    n, o, u, pct = rate(want)
    L += [f"| | **TOTAL** | **{n}** | **{o}** | **{u}** | **{pct}** |", "",
          "A request that failed is recorded as `UNCONFIRMED`, never as closed. A publisher that "
          "blocks a scripted lookup has not made the paper closed; it has made this route closed, and "
          "the record belongs on the human procurement list rather than in a 'not obtainable' bucket.", "",
          "## What is deliberately NOT retrieved, and what that costs", "",
          "| set | n | why |", "|---|---|---|",
          f"| `B3` first-stage candidates with NO twinning term | {len(jobs.get('B3', []))} | The Wall 8 "
          "bypass admitted these deliberately, because instruments go unnamed in abstracts too. But the "
          "set includes sibling-sex-composition and one-child-policy designs that have no twin first "
          "stage at all. **This is the honest cost of the bypass's breadth, and the chapter's "
          "first-stage synthesis must state that it did not read them.** |",
          f"| `C3` routine per-cycle ART records | {len(jobs.get('C3', []))} | 100 per-cycle records "
          "cannot each carry a demographic quantity; the high-grade designs are retained in C2. |",
          f"| `D_skip` country-year twinning tabulations | {len(jobs.get('D_skip', []))} | Their numbers "
          "come from the Human Multiple Births Database directly. Retrieving a PDF to read a rate the "
          "HMBD already publishes harmonised would be work without a product. |", "",
          "## Retrieval list", ""]
    for j, desc in JOBDESC:
        items = sorted(jobs.get(j, []), key=lambda x: -(x.get("cited_by_count") or 0))
        if not items:
            continue
        L += [f"### JOB {j} — {desc} ({len(items)})", "",
              "| OA | year | title | why |", "|---|---|---|---|"]
        for x in items:
            st = x["oa"]["status"]
            mark = "**open**" if st in OPEN else ("?" if st == "UNCONFIRMED" else "closed")
            L.append(f"| {mark} | {x.get('year')} | {(x.get('title') or '')[:64]} | {x['why'][:96]} |")
        L.append("")
    L += ["## Target paths", "",
          f"`literature/pdfs/{SLUG}/{{WID}}__{{title-slug}}.pdf` (gitignored). A file dropped there "
          "is picked up by ingest without renaming."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"wantlist={len(want)}  open={sum(1 for x in want if x['oa']['status'] in OPEN)}  "
          f"unconfirmed={sum(1 for x in want if x['oa']['status']=='UNCONFIRMED')}")
    for j, _ in JOBDESC:
        n, o, u, pct = rate(jobs.get(j, []))
        print(f"  {j:<3} n={n:<4} open={o:<4} ({pct})")
    print(f"  deprioritised: B3={len(jobs.get('B3',[]))} C3={len(jobs.get('C3',[]))} "
          f"D_skip={len(jobs.get('D_skip',[]))}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
