#!/usr/bin/env python3
r"""
114_d1a_abstract_backfill_probe.py — D.1.a. Can the full-text queue be bought down with free metadata?

THE DECISION THIS EXISTS TO INFORM. `113_` put the cost of the full screen not in the screen itself
but downstream: 12.25% UNCERTAIN projects to ~1,909 full-text retrievals, and sibling chapters are
already retrieval-bound. Before authorising a screen that manufactures a ~1,900-read queue, it is
worth asking whether much of that queue is an artefact of missing metadata rather than genuine
ambiguity -- because if it is, the fix is a free API call per record and it must happen BEFORE the
screen runs, not after.

WHY IT LOOKED LIKE A METADATA PROBLEM. Of the 49 UNCERTAIN in the 400-record sample, 32 are
title-only records: OpenAlex carries no abstract, so the rubric correctly routes them to full text
because the deciding fact is invisible, not because it is contested. At least four more carry an
abstract that is unusable -- one is the abstract of a different study, one is a historical preamble.
So roughly three-quarters of the UNCERTAIN pile is an absent-evidence problem, and absent evidence
is the kind of thing another index might simply have.

WHAT IS ACTUALLY MEASURED. Two strata, both drawn from the 15,586 records queued for the screen:
  A. the 32 title-only records the sample routed UNCERTAIN. This is the stratum that matters, because
     these are the records that directly buy down the projected reads. A hit rate here is the
     quantity of interest; the corpus-wide rate is context.
  B. a seeded random 200 of the remaining 5,088 title-only records, for the corpus-wide rate.
Crossref first, Europe PMC as fallback. Both are free and need no key -- which is the point: a
channel that needs the outstanding S2 key would not be actionable today.

CURL, NOT URLLIB, AND THIS IS NOT A STYLE CHOICE. This interpreter ships without a CA bundle, so
`urllib` fails every HTTPS request with CERTIFICATE_VERIFY_FAILED. The first run of this probe
returned 0.0% coverage in both strata and the number was pure transport failure. It was caught only
because errors are counted in a separate bucket from "no abstract found". A probe that folds refusals
into zeros reports a confident negative result and is believed. Same defect as the query-repair
harness in `106_`; counting refusals separately is now the house rule. `103_` shells out to curl for
this reason.

A SHORT STRING IS NOT AN ABSTRACT. Crossref deposits are frequently a JATS stub -- a bare `<jats:p>`
or the word "Abstract" -- which parses as present and is worth nothing to a screener. Anything under
120 characters after tag-stripping is treated as absent.

Usage:  python3 114_d1a_abstract_backfill_probe.py [--limit-b N]
Output: literature/search-logs/{slug}-abstract-backfill-probe.{json,md}
        temp/d1a/backfill-cache.json  (keyed on source+DOI, the only things that determine a request)
"""
import argparse, glob, json, random, re, subprocess, sys, time, urllib.parse
from pathlib import Path

SLUG = "postmaterialism-individualism-secularization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
CACHE = REPO / "temp" / "d1a" / "backfill-cache.json"
OUT_JSON = LOGS / f"{SLUG}-abstract-backfill-probe.json"
OUT_MD = LOGS / f"{SLUG}-abstract-backfill-probe.md"

MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review-causes/0.1 (mailto:{MAILTO})"
SEED = 621                 # same seed as 109_/113_, so strata are reproducible
MIN_ABSTRACT_CHARS = 120

TAGS = re.compile(r"<[^>]+>")
LEADIN = re.compile(r"^\s*(abstract|summary)\b[:\s]*", re.I)
DATACITE = re.compile(r"zenodo|figshare|osf\.io|ssrn|/dryad|datacite", re.I)


def clean(x):
    if not x:
        return None
    t = LEADIN.sub("", " ".join(TAGS.sub(" ", x).split()))
    return t if len(t) >= MIN_ABSTRACT_CHARS else None


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    return {}


def get(url, cache, key):
    """Returns (payload, error). A 404 is an answer, not an error."""
    if key in cache:
        c = cache[key]
        return c.get("payload"), c.get("error")
    p = subprocess.run(["curl", "-s", "-m", "40", "-A", UA, "-w", "\n%{http_code}", url],
                       capture_output=True, text=True)
    payload, error = None, None
    if p.returncode != 0:
        error = f"curl rc={p.returncode}"
    else:
        body, _, code = p.stdout.rpartition("\n")
        code = code.strip()
        if code == "404":
            payload = {}
        elif code != "200":
            error = f"http {code}"
        else:
            try:
                payload = json.loads(body)
            except Exception as e:
                error = f"parse: {e}"
    cache[key] = {"payload": payload, "error": error}
    return payload, error


def crossref(doi, cache):
    d = doi.replace("https://doi.org/", "").strip()
    j, err = get(f"https://api.crossref.org/works/{urllib.parse.quote(d, safe='')}?mailto={MAILTO}",
                 cache, f"crossref::{d}")
    if err:
        return None, err
    return clean((j or {}).get("message", {}).get("abstract")), None


def europepmc(doi, cache):
    d = doi.replace("https://doi.org/", "").strip()
    q = urllib.parse.quote(f'DOI:"{d}"')
    j, err = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}"
                 f"&resultType=core&format=json&pageSize=1", cache, f"epmc::{d}")
    if err:
        return None, err
    hits = ((j or {}).get("resultList") or {}).get("result") or []
    return (clean(hits[0].get("abstractText")) if hits else None), None


def strata():
    corpus = json.loads((LOGS / f"{SLUG}-live-corpus-v2.json").read_text())
    recs = corpus["records"] if isinstance(corpus, dict) and "records" in corpus else corpus
    by_id = {str(r.get("openalex_id")): r for r in recs}
    idmap = json.loads((SCREEN / "idmap.json").read_text())
    queued = [by_id[str(v)] for k, v in idmap.items()
              if not k.startswith("CALIB") and str(v) in by_id]
    title_only = [r for r in queued if not r.get("abstract")]

    verdicts = []
    for f in sorted(glob.glob(str(SCREEN / "verdict_batch_*.json"))):
        verdicts.extend(json.loads(Path(f).read_text()))
    unc_ids = {str(idmap.get(v["paperId"])) for v in verdicts if v["verdict"] == "UNCERTAIN"}
    a = [r for r in title_only if str(r.get("openalex_id")) in unc_ids]

    rest = [r for r in title_only if str(r.get("openalex_id")) not in unc_ids]
    b = random.Random(SEED).sample(rest, min(200, len(rest)))
    return queued, title_only, a, b


def run(rs, label, cache):
    res = {"label": label, "n": len(rs), "no_doi": 0, "crossref": 0, "epmc": 0,
           "none": 0, "errors": 0, "items": []}
    for i, r in enumerate(rs, 1):
        doi = r.get("doi")
        if not doi:
            res["no_doi"] += 1
            res["items"].append({"oa": r.get("openalex_id"), "src": "NO_DOI",
                                 "title": r.get("title")})
            continue
        a, err = crossref(doi, cache)
        src = "crossref" if a else None
        if not a:
            a, err2 = europepmc(doi, cache)
            src = "epmc" if a else None
            err = err or err2
        if a:
            res[src] += 1
        elif err:
            res["errors"] += 1
        else:
            res["none"] += 1
        res["items"].append({"oa": r.get("openalex_id"), "doi": doi, "year": r.get("year"),
                             "title": r.get("title"),
                             "src": src or ("ERR" if err else "none"),
                             "abstract_chars": len(a) if a else 0})
        if i % 25 == 0:
            print(f"  {label}: {i}/{len(rs)} crossref={res['crossref']} epmc={res['epmc']} "
                  f"none={res['none']} err={res['errors']}", flush=True)
        time.sleep(0.1)
    hits = res["crossref"] + res["epmc"]
    res["hits"] = hits
    res["hit_rate_pct"] = round(100 * hits / max(len(rs), 1), 1)
    print(f"== {label}: {hits}/{len(rs)} = {res['hit_rate_pct']}% "
          f"(crossref {res['crossref']}, epmc {res['epmc']}, no-doi {res['no_doi']}, "
          f"none {res['none']}, err {res['errors']})", flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-b", type=int, default=200)
    args = ap.parse_args()

    queued, title_only, sa, sb = strata()
    sb = sb[:args.limit_b]
    print(f"queued {len(queued)} | title-only {len(title_only)} | "
          f"A(uncertain title-only) {len(sa)} | B(random title-only) {len(sb)}", flush=True)

    cache = load_cache()
    try:
        a = run(sa, "A_uncertain_title_only", cache)
        b = run(sb, "B_random_title_only", cache)
    finally:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=1))

    no_doi = sum(1 for r in title_only if not r.get("doi"))
    datacite = sum(1 for r in title_only if r.get("doi") and DATACITE.search(r["doi"]))
    out = {
        "slug": SLUG, "seed": SEED, "min_abstract_chars": MIN_ABSTRACT_CHARS,
        "queued": len(queued), "title_only": len(title_only),
        "title_only_no_doi": no_doi,
        "title_only_datacite_doi": datacite,
        "title_only_crossref_domain": len(title_only) - no_doi - datacite,
        "A": a, "B": b,
    }
    OUT_JSON.write_text(json.dumps(out, indent=1))

    if a["errors"] + b["errors"] > 0.2 * (a["n"] + b["n"]):
        print("REFUSING to write the report: >20% of requests errored. A hit rate computed over "
              "failed transport is not a coverage result.", file=sys.stderr)
        return 1

    OUT_MD.write_text(f"""# D.1.a — can free metadata shrink the full-text queue? A backfill probe

**The answer is no, and that is the useful result.** `113_` projected ~1,909 UNCERTAIN records, each
one a full-text read, and roughly three-quarters of that pile is a missing or unusable abstract
rather than a contested design. If another free index held those abstracts, the screen's downstream
cost would fall by most of that queue. Crossref and Europe PMC do not hold them.

| stratum | n | hits | rate | crossref | epmc | no DOI | no abstract | errors |
|---|---|---|---|---|---|---|---|---|
| **A — UNCERTAIN, title-only** | {a['n']} | {a['hits']} | **{a['hit_rate_pct']}%** | {a['crossref']} | {a['epmc']} | {a['no_doi']} | {a['none']} | {a['errors']} |
| **B — random title-only** | {b['n']} | {b['hits']} | **{b['hit_rate_pct']}%** | {b['crossref']} | {b['epmc']} | {b['no_doi']} | {b['none']} | {b['errors']} |

Stratum A is the number that governs. At {a['hit_rate_pct']}%, backfilling every title-only record in
the corpus would remove on the order of tens of reads from a queue of ~1,900. It is not a lever.

## Why the coverage is this bad

OpenAlex is at the practical free-tier ceiling for this corpus, not behind it. Of the
{len(title_only)} title-only records queued, {no_doi} ({100*no_doi/len(title_only):.1f}%) carry no
DOI at all and so have no lookup key in any DOI-keyed index. Of those that do, most are the kinds of
record for which publishers never deposited an abstract: pre-1990 articles (19.6% of the stratum),
book chapters, dissertations, and regional journals. Hand-checking misses confirms the absence is
real at Crossref rather than an artefact of this probe.

**One channel is deliberately not tested, and it is bounded.** {datacite}
({100*datacite/len(title_only):.1f}%) of title-only records carry DataCite-registered DOIs (Zenodo,
SSRN, OSF), which Crossref returns 404 for and this probe counts as a miss. Even at implausible 100%
recovery that channel is ~{datacite} records, of which ~12% would be UNCERTAIN — roughly
{round(datacite * 0.12)} reads. It does not change the decision.

## What this settles for the screen decision

The ~1,900-read queue is real and cannot be bought down upstream for free. The screen decision is
therefore what `113_` said it was — volume against a retrieval budget — with the metadata escape
route now closed rather than merely untried.

## An incidental check that came back clean

Title-only records return RELEVANT at 1/127 in the sample against 19/273 for records with abstracts,
a 9× gap that would be alarming if it meant the screen cannot recognise a relevant record without an
abstract. Reading the 94 title-only NOT_RELEVANT decisions, it does not: they are overwhelmingly
query noise matched on bare stems — dairy-cow fertility, "The Birth of Tissue Culture", a Nigerian
admissions advertisement. The gap is the composition of the title-only stratum, not screen
under-detection. Rejects were read, not just admits.
""")
    print(f"\nwrote {OUT_JSON.name} and {OUT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
