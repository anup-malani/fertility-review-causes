#!/usr/bin/env python3
"""
133_b6_anchor_retry.py — B.6 follow-up to 132, on two questions the first pass left open.

(1) v5's seminal list for B.6 resolved badly in 132. Three of its four entries did not return the
    work named. This pass retries each on differently-worded titles and on the works most likely to
    have been meant, so the scope document can state a specific correction for TICK-001 rather than
    "several did not resolve". A zero on `title.search` is a statement about wording, not literature.

(2) 132 found the demographic seam close to empty, but one record in it was a quasi-experimental
    study of a contaminated water supply. If a family of PFAS contamination natural experiments
    exists — Ronneby, Veneto, Mid-Ohio Valley, Decatur — it is the only identification this chapter
    could have, and it changes what the search is built to find. That is worth measuring before the
    walls are frozen rather than discovering at screen.

Same discipline as 132: curl transport, funded key, errors bucketed separately from zero-hits.

Output: literature/search-logs/{slug}-anchor-retry.md
"""
import json, os, subprocess, sys, time

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-anchor-retry.md")
ERROR_ABORT_SHARE = 0.20


def openalex_key():
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
PF = '("PFAS" OR "per- and polyfluoroalkyl" OR "perfluoroalkyl" OR "perfluorinated" OR "PFOA" OR "PFOS")'

# --- (1) v5 seminal-list retries. Each group is one v5 citation and the candidates for what it meant.
SEMINAL_RETRY = [
    ("v5 cites: Zhao et al., Fertility & Sterility (2025), microplastics in follicular fluid", [
        "First evidence of microplastics in human ovarian follicular fluid",
        "Detection and characterization of microplastics in human follicular fluid",
        "Microplastics in human follicular fluid and semen",
    ]),
    ("v5 cites: Lancet Commission on Reproductive Health (2025)", [
        "Minderoo-Monaco Commission on Plastics and Human Health",
        "Lancet Countdown plastics health commission",
        "Commission on plastics and human health",
    ]),
    ("v5 cites: Yang et al., Scientific Reports (2025)", [
        "Microplastics in human semen Scientific Reports",
        "Association between microplastics and semen quality",
        "Microplastics detected in human seminal fluid and their association",
    ]),
    ("v5 cites: Shoaito et al., Environment International (2023), placental", [
        "The role of peroxisome proliferator-activated receptor gamma in cytotrophoblast differentiation",
        "Perfluoroalkyl substances and placental trophoblast function",
        "PFOS PFOA human trophoblast differentiation",
    ]),
]

# --- (2) Natural-experiment and contamination-cohort probes. The identification question.
NATEXP = [
    ("PFAS contamination natural experiment / water supply change",
     f'title_and_abstract.search:{PF} AND ("drinking water" OR "water supply" OR "contamination") AND ("fertility" OR "fecundability" OR "time to pregnancy" OR "birth rate" OR "reproductive outcomes")'),
    ("Ronneby (Sweden) high-exposure cohort",
     f'title_and_abstract.search:{PF} AND ("Ronneby" OR "Kallinge" OR "Blekinge")'),
    ("Veneto (Italy) contaminated area",
     f'title_and_abstract.search:{PF} AND ("Veneto" OR "Vicenza" OR "red zone" OR "Italy") AND ("exposure" OR "cohort" OR "residents")'),
    ("C8 Health Project / Mid-Ohio Valley, reproductive endpoints",
     f'title_and_abstract.search:{PF} AND ("C8 Health" OR "Mid-Ohio Valley" OR "Little Hocking" OR "Washington Works") AND ("fertility" OR "pregnancy" OR "birth" OR "reproductive")'),
    ("difference-in-differences / instrumental variable / quasi-experimental",
     f'title_and_abstract.search:{PF} AND ("difference-in-differences" OR "instrumental variable" OR "natural experiment" OR "quasi-experimental" OR "regression discontinuity")'),
    ("PFAS regulation / phase-out as exposure shock",
     f'title_and_abstract.search:{PF} AND ("phase-out" OR "phaseout" OR "regulation" OR "ban" OR "restriction") AND ("serum" OR "exposure" OR "decline") AND ("trend" OR "temporal")'),
    ("economics / demography journals on PFAS or microplastics",
     'title_and_abstract.search:("PFAS" OR "microplastic" OR "microplastics" OR "perfluoroalkyl") AND ("economic" OR "economics" OR "demographic" OR "demography" OR "welfare" OR "cost")'),
    ("ART-clinic derived exposure-outcome (the selection question)",
     f'title_and_abstract.search:({PF} OR "microplastic" OR "microplastics") AND ("follicular fluid" OR "IVF" OR "in vitro fertilization") AND ("oocyte" OR "fertilization rate" OR "clinical pregnancy" OR "live birth")'),
]

errors, seminal_results, natexp_results = [], [], []


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


def main():
    n_req = 0
    for group, titles in SEMINAL_RETRY:
        got = []
        for t in titles:
            n_req += 1
            url = ("https://api.openalex.org/works?filter=title.search:" + t.replace(" ", "%20") +
                   "&per-page=5&select=id,doi,display_name,publication_year,cited_by_count,type,"
                   "primary_location&api_key=" + KEY)
            d = oa(url)
            if "results" not in d:
                errors.append((t[:45], str(d.get("__err") or d)[:160]))
            else:
                got.append((t, d["meta"]["count"], rows_of(d)))
            time.sleep(0.25)
        seminal_results.append((group, got))

    for label, filt in NATEXP:
        n_req += 1
        url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20").replace('"', "%22") +
               "&per-page=8&select=id,doi,display_name,publication_year,cited_by_count,type,"
               "primary_location&sort=cited_by_count:desc&api_key=" + KEY)
        d = oa(url)
        if "results" not in d:
            errors.append((label, str(d.get("__err") or d)[:160]))
        else:
            natexp_results.append((label, filt, d["meta"]["count"], rows_of(d)))
        time.sleep(0.25)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        print(f"ABORT: {len(errors)}/{n_req} failed ({share:.0%}). Report NOT written.", file=sys.stderr)
        for e in errors:
            print("  ", e, file=sys.stderr)
        sys.exit(1)

    L = [f"# Anchor retry and identification probe — {SLUG}", "",
         "Generated by `source/build/goldset/133_b6_anchor_retry.py`, following "
         "`132_b6_recon_probe.py`.", "",
         f"**Requests: {n_req} · failed: {len(errors)} ({share:.0%}) · zero-hit counts are genuine "
         "absences, not refusals.**", "",
         "## Part 1 — what v5's seminal list actually resolves to", "",
         "Three of B.6's four seminal citations failed to resolve in the first pass. Each group below "
         "is one v5 citation and the candidate works it may have meant.", ""]

    for group, got in seminal_results:
        L += [f"### {group}", ""]
        for t, count, rows in got:
            L += [f"**Probe:** `{t}` — n = {count}", ""]
            for r in rows:
                L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                         f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
            L.append("")

    L += ["## Part 2 — is there any quasi-experimental identification?", "",
          "The chapter's credibility ceiling is set here. If the only human evidence is "
          "cross-sectional serum-concentration association, no GRADE rating above Low is reachable "
          "whatever the volume of the literature.", ""]
    for label, filt, count, rows in natexp_results:
        L += [f"### {label}", "", f"`{filt}` — **n = {count:,}**", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    if errors:
        L += ["## Error bucket (failed requests — NOT zero-hits)", ""]
        L += [f"- {a}: {b}" for a, b in errors] + [""]

    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"requests={n_req} failed={len(errors)} seminal_groups={len(seminal_results)} natexp={len(natexp_results)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
