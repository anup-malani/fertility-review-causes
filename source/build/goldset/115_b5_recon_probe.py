#!/usr/bin/env python3
"""
115_b5_recon_probe.py — B.5 (fetal loss / intrauterine mortality), pre-scope reconnaissance.

Runs before A3. Its job is to establish, from live records rather than from memory, (a) how large the
adjacent clinical literature is relative to the demographic seam this chapter needs, (b) whether the
PRIMARY estimand cell exists at all in the indexed corpus, and (c) which named canonical works resolve
and how (the book-canon trap). The scope document's "Expected shape of the evidence" section quotes
this script's counts, so the counts must be regenerable.

Discipline carried from prior runs:
  * A failed request is counted in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the
    report refuses to publish if the error share exceeds ERROR_ABORT_SHARE. A wrong zero here would
    propagate into the scope document as "this literature does not exist".
  * HTTPS goes through curl: the interpreter on this machine has no CA bundle, so urllib fails every
    call (and would fail as a *transport* error, i.e. as a fake zero).
  * OpenAlex is called with the funded api_key from .env, never with mailto alone — mailto draws on a
    shared anonymous budget that a probe sweep exhausts, and the failure presents as slowness first.

Output: literature/search-logs/{slug}-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "fetal-loss-intrauterine-mortality"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-recon-probe.md")
ERROR_ABORT_SHARE = 0.20
PER_PAGE = 8


def openalex_key():
    """Read the funded key from the environment, then from .env. Never log or cache the value."""
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = openalex_key()

# --- Probe set. Grouped so the report reads as an argument, not as a dump. ---
GROUPS = [
    ("Ambient volume — the adjacent clinical literature", [
        ("fetal loss AND fertility", 'default.search:"fetal loss" AND "fertility"'),
        ("spontaneous abortion AND demography", 'default.search:"spontaneous abortion" AND "demography"'),
        ("pregnancy wastage", 'title_and_abstract.search:"pregnancy wastage"'),
        ("fetal wastage", 'title_and_abstract.search:"fetal wastage"'),
        ("reproductive wastage", 'title_and_abstract.search:"reproductive wastage"'),
    ]),
    ("The demographic seam", [
        ("intrauterine mortality (t+a)", 'title_and_abstract.search:"intrauterine mortality"'),
        ("fetal loss AND natural fertility", 'title_and_abstract.search:"fetal loss" AND "natural fertility"'),
        ("stillbirth AND fertility decline", 'title_and_abstract.search:"stillbirth" AND "fertility decline"'),
        ("proximate determinants of fertility", 'title.search:proximate determinants of fertility'),
        ("fetal mortality AND historical", 'title_and_abstract.search:"fetal mortality" AND ("historical" OR "nineteenth century" OR "parish")'),
    ]),
    ("Does the PRIMARY cell exist? (loss -> live-birth fertility)", [
        ("loss -> TFR / birth rate", 'title_and_abstract.search:("fetal loss" OR "pregnancy loss" OR "intrauterine mortality" OR "fetal mortality") AND ("total fertility rate" OR "birth rate" OR "fertility rate")'),
        ("stillbirth -> completed fertility", 'title_and_abstract.search:"stillbirth" AND ("total fertility rate" OR "completed fertility")'),
        ("loss -> parity progression / interval", 'title_and_abstract.search:("fetal loss" OR "pregnancy loss" OR "miscarriage" OR "stillbirth") AND ("parity progression" OR "birth spacing" OR "birth interval")'),
        ("loss AND completed fertility/family size", 'title_and_abstract.search:"fetal loss" AND ("completed fertility" OR "family size" OR "parity")'),
    ]),
    ("The shock channel (where identification lives)", [
        ("famine -> loss / births", 'title_and_abstract.search:("famine" OR "Hunger Winter" OR "Great Leap") AND ("fetal loss" OR "stillbirth" OR "miscarriage" OR "fetal death")'),
        ("1918 pandemic -> stillbirth", 'title_and_abstract.search:("influenza pandemic" OR "1918") AND ("stillbirth" OR "fetal loss" OR "pregnancy loss")'),
        ("syphilis / penicillin -> stillbirth decline", 'title_and_abstract.search:("syphilis" OR "penicillin" OR "antibiotic") AND "stillbirth" AND ("decline" OR "eradication" OR "campaign")'),
        ("malaria control -> birth outcomes", 'title_and_abstract.search:("malaria" AND ("eradication" OR "control programme" OR "IPTp")) AND ("stillbirth" OR "fetal loss")'),
    ]),
    ("Replacement / compensation (the attenuation parameter)", [
        ("reproductive compensation", 'title_and_abstract.search:"reproductive compensation"'),
        ("interval to next conception after loss", 'title_and_abstract.search:("after miscarriage" OR "after stillbirth" OR "following pregnancy loss") AND ("subsequent pregnancy" OR "next birth" OR "time to conception")'),
    ]),
    ("Measurement (Wall 4 and the risk-of-bias spine)", [
        ("induced reported as spontaneous", 'title_and_abstract.search:("induced abortion" AND ("misreport" OR "underreport" OR "misclassification")) AND ("spontaneous" OR "miscarriage")'),
        ("stillbirth definition comparability", 'title_and_abstract.search:"stillbirth" AND ("definition" OR "gestational age threshold") AND ("comparability" OR "international")'),
        ("survey recall of pregnancy loss", 'title_and_abstract.search:("pregnancy history" OR "birth history") AND ("recall" OR "omission") AND ("fetal loss" OR "pregnancy loss" OR "stillbirth")'),
    ]),
    ("Channel 1 — prior systematic reviews and global estimates", [
        ("SR/meta on loss prevalence", 'title_and_abstract.search:("systematic review" OR "meta-analysis") AND ("miscarriage" OR "pregnancy loss") AND ("prevalence" OR "incidence" OR "risk")'),
        ("global stillbirth estimates", 'title_and_abstract.search:"stillbirth" AND ("national" AND "regional" AND "global") AND ("estimates" OR "trends")'),
    ]),
    ("Wall 7 — the non-human literature", [
        ("embryonic mortality, livestock", 'title_and_abstract.search:("embryonic mortality" OR "reproductive wastage") AND ("cattle" OR "swine" OR "sow" OR "bovine" OR "veterinary")'),
    ]),
]

# Named canonical works: does each resolve, and to the work or to a review of it?
NAMED = [
    "Death before Birth Fetal Health and Mortality in Historical Perspective",
    "Collecting Data on Pregnancy Loss A Review of Evidence from the World Fertility Survey",
    "Human Fertility The Basic Components",
    "Dynamics of Human Reproduction Biology Biometry Demography",
    "A Framework for Analyzing the Proximate Determinants of Fertility",
    "Fertility Biology and Behavior An Analysis of the Proximate Determinants",
    "Maternal age and fetal loss population based register linkage study",
    "Famine social disruption and involuntary fetal loss",
    "Conception to ongoing pregnancy the black box of early pregnancy loss",
]

errors, results, named_results = [], [], []


def oa(url):
    try:
        r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
        if r.returncode != 0:
            return {"__err": f"curl exit {r.returncode}"}
        return json.loads(r.stdout)
    except Exception as e:
        return {"__err": str(e)[:140]}


def rows_of(d):
    out = []
    for w in d.get("results", []):
        loc = (w.get("primary_location") or {}).get("source") or {}
        out.append(dict(title=w.get("display_name") or "", year=w.get("publication_year"),
                        cites=w.get("cited_by_count"), type=w.get("type"),
                        venue=(loc.get("display_name") or ""),
                        doi=(w.get("doi") or "").replace("https://doi.org/", "")))
    return out


def probe(filt, per_page=PER_PAGE, sort="cited_by_count:desc"):
    url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20").replace('"', "%22") +
           f"&per-page={per_page}&select=id,doi,display_name,publication_year,cited_by_count,type,"
           f"primary_location&sort={sort}&api_key={KEY}")
    return oa(url)


def main():
    n_req = 0
    for group, probes in GROUPS:
        for label, filt in probes:
            n_req += 1
            d = probe(filt)
            if "results" not in d:
                errors.append((label, str(d.get("__err") or d)[:160]))
            else:
                results.append((group, label, filt, d["meta"]["count"], rows_of(d)))
            time.sleep(0.25)

    for t in NAMED:
        n_req += 1
        url = ("https://api.openalex.org/works?filter=title.search:" + t.replace(" ", "%20") +
               "&per-page=5&select=id,doi,display_name,publication_year,cited_by_count,type,"
               "primary_location&api_key=" + KEY)
        d = oa(url)
        if "results" not in d:
            errors.append((t[:45], str(d.get("__err") or d)[:160]))
        else:
            named_results.append((t, d["meta"]["count"], rows_of(d)))
        time.sleep(0.25)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        print(f"ABORT: {len(errors)}/{n_req} requests failed ({share:.0%} > {ERROR_ABORT_SHARE:.0%}). "
              "Report NOT written — a zero-hit count cannot be distinguished from a refusal at this "
              "error rate.", file=sys.stderr)
        for e in errors:
            print("  ", e, file=sys.stderr)
        sys.exit(1)

    L = [f"# Pre-scope reconnaissance — {SLUG}", "",
         "Generated by `source/build/goldset/115_b5_recon_probe.py`. Counts are OpenAlex universe sizes "
         "for the stated filter, listed works are the most-cited within it.", "",
         f"**Requests: {n_req} · failed: {len(errors)} ({share:.0%}) · zero-hit counts below are "
         "therefore genuine absences, not refusals.**", "",
         "Why this exists: B.5 is defined by a channel that a very large clinical literature shares "
         "vocabulary with, so the scope document needed a measured picture of the precision problem "
         "before the walls were drawn rather than after the first screen came back.", ""]

    cur = None
    for group, label, filt, count, rows in results:
        if group != cur:
            L += [f"## {group}", ""]
            cur = group
        L += [f"### {label}", "", f"`{filt}` — **n = {count:,}**", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    L += ["## Named canonical works — resolution behaviour", "",
          "Listed in retrieval order. Where a monograph is followed by review records, the book-canon "
          "gate (D.2.d, 2026-08-08) is what keeps the resolver from anchoring the work to its review.", ""]
    for t, count, rows in named_results:
        L += [f"### {t}", "", f"n = {count}", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    if errors:
        L += ["## Error bucket (failed requests — NOT zero-hits)", ""]
        L += [f"- {a}: {b}" for a, b in errors] + [""]

    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"requests={n_req} failed={len(errors)} groups={len(GROUPS)} named={len(named_results)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
