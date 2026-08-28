#!/usr/bin/env python3
"""
232_a23_pdf_wantlist.py — A.23, stage 5a. Probe open-access status for the 436-record queue.

The triage is ALREADY DONE and is not redone here. `231_a23_ra_gate_queues.py` assigned every
forwarded record a `retrieval_tier` ordered by what SYNTHESIS needs, and those tiers are this
chapter's jobs. What is missing before a fetcher can run is the other half: for each queued record,
where — if anywhere — a free copy is said to live. That is what this script measures.

WHY A SEPARATE PROBE STAGE AT ALL. The OA flag is a CEILING on what a script can reach, never a
prediction of it: C.3.g probed 61 of 114 as open access and fetched 23, because two open-access
hosts returned 403 to curl on open content. Recording the ceiling before the run is what makes the
gap between ceiling and yield readable afterwards, instead of being absorbed into a single rate.

RUNG-ORDER PREDICTIONS, RECORDED BEFORE THE FETCH, because the standing finding is that rung order
is chapter-specific and must be measured, not inherited. This chapter is demography, sociology and
family economics, and its DOI prefixes say something specific about it:

  * **THE MPIDR PREFIX SHOULD BE NEAR-PERFECT, AND IT IS TWO RUNGS, NOT ONE.** 14 queued records
    carry a `10.4054` DOI, and reading them showed the prefix is shared by two different publishers'
    objects with two different constructions: 8 are `10.4054/DemRes.V.A` journal articles served at
    `demographic-research.org/volumes/volV/A/V-A.pdf`, and 6 are `10.4054/mpidr-{wp,tr}-YYYY-NNN`
    working papers and technical reports served at `demogr.mpg.de/papers/{working,technicalreports}/`.
    A prefix-level rung would have taken the 8 and dropped the 6. Both paths are fixed by the DOI's
    own shape, so both are constructions rather than searches — the deterministic move the NBER/FEDS
    rung made on C.3.g, aimed at the series this literature actually publishes in. C.3.g's version
    of that rung found ONE url; the prediction here is that these two find all fourteen.
  * **An OSF/SocArXiv rung should pay.** 5 records carry `10.31235`, and OSF serves PDFs from an API
    endpoint rather than from a defended page.
  * **PMC is predicted LOW BUT NON-ZERO — the first chapter since B.6 where that is the prediction.**
    22 queued records have `PubMed` as their venue. A.12, A.24 and C.3.g each returned ~zero and the
    rung is one more zero away from retirement; this chapter is the test that should stop that, and
    if it does not, the rung should go.
  * **Expect BLOCKED to dominate CLOSED among the failures**, as on C.3.g and A.17.

**98 QUEUED RECORDS CARRY NO DOI.** They cannot be resolved by Unpaywall, by PMC, or by any
deterministic rung; they have only their OpenAlex locations. They are counted separately at every
step, because a retrieval rate that silently averages them with the resolvable records reports a
capability the pipeline does not have.

Output: extraction/{slug}-oa-status.json
        literature/search-logs/{slug}-wantlist.md
"""
import json, os, re, subprocess, sys, time
from collections import Counter, defaultdict

SLUG = "co-residence-parents-household-delay"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
QUEUE = os.path.join(LOGS, f"{SLUG}-retrieval-queue.json")
OUT_OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-wantlist.md")

TIER_ORDER = ["T1_wall1_packet", "T1_primary_identified", "T2_primary_relevant",
              "T3_primary_uncertain", "T3_link1_identified",
              "T4_insufficient_resolve_at_retrieval", "T5_link1", "T6_theory_stream"]


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
ERRORS = []


def get(url, timeout=45):
    try:
        r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def oa_lookup(wid):
    d = get(f"https://api.openalex.org/works/{wid}?select=id,doi,title,open_access,"
            f"best_oa_location,locations,type,primary_location&api_key={KEY}")
    if not d:
        ERRORS.append((wid, "transport"))
        return None
    try:
        return json.loads(d)
    except Exception:
        ERRORS.append((wid, "unparseable"))
        return None


def deterministic_rung(doi):
    """Which construction-not-search rung, if any, this DOI's shape unlocks.

    Named here rather than in the fetcher so the wantlist can COUNT the rung's population before a
    single request is spent, which is what makes the prediction falsifiable."""
    d = (doi or "").lower()
    if re.match(r"10\.4054/demres\.", d):
        return "demographic_research"
    if re.match(r"10\.4054/mpidr-(wp|tr)-", d):
        return "mpidr_working_paper"
    if d.startswith("10.31235/"):
        return "osf_socarxiv"
    if re.match(r"10\.3386/w\d+$", d):
        return "nber"
    return None


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    q = json.load(open(QUEUE))
    recs = q["queue"]

    rows = []
    for i, r in enumerate(recs, 1):
        m = oa_lookup(r["openalex"])
        loc = (m or {}).get("best_oa_location") or {}
        locs = (m or {}).get("locations") or []
        n_open = sum(1 for l in locs if l.get("is_oa"))
        doi = (r.get("doi") or ((m or {}).get("doi") or "").replace("https://doi.org/", "")) or None
        rows.append(dict(
            id=r["openalex"], tier=r["retrieval_tier"], title=r["title"], year=r.get("year"),
            venue=r.get("venue"), type=r.get("type"), doi=doi,
            is_oa=bool(((m or {}).get("open_access") or {}).get("is_oa")),
            oa_status=((m or {}).get("open_access") or {}).get("oa_status"),
            n_open_locations=n_open,
            best_url=loc.get("pdf_url") or loc.get("landing_page_url"),
            det_rung=deterministic_rung(doi),
            verdict=r.get("verdict"), route=r.get("route"), config=r.get("config"),
            design=r.get("design"), anticipation_flag=r.get("anticipation_flag"),
            probe_ok=m is not None,
        ))
        if i % 25 == 0:
            print(f"  probed {i}/{len(recs)}")
        time.sleep(0.12)

    os.makedirs(EXTRACT, exist_ok=True)
    json.dump(rows, open(OUT_OA, "w"), indent=2)

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    by_tier = defaultdict(list)
    for r in rows:
        by_tier[r["tier"]].append(r)
    n_oa = sum(1 for r in rows if r["is_oa"])
    no_doi = [r for r in rows if not r["doi"]]
    det = Counter(r["det_rung"] for r in rows if r["det_rung"])
    by_design = defaultdict(list)
    for r in rows:
        by_design[r["design"]].append(r)
    ident = [r for r in rows if r["design"] == "identified"]

    L = [f"# Stage 5a retrieval wantlist — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/232_a23_pdf_wantlist.py`", "",
         f"**{len(rows)} queued records probed for open-access status.** "
         f"**{n_oa} ({pc(n_oa, len(rows))}) are open access** by OpenAlex's reckoning. That is a "
         "CEILING on what the fetcher can reach and not a prediction of it — C.3.g probed 54% open "
         "and fetched 20%, because open-access hosts return 403 to scripts. Recording the ceiling "
         "now is what makes the gap readable later.", "",
         "## The ceiling, by tier", "",
         "Tiers are this chapter's retrieval jobs; they were set in `231` by what synthesis needs, "
         "and they are not re-derived here.", "",
         "| Tier | n | Open access | No DOI |", "|---|---|---|---|"]
    for t in TIER_ORDER:
        g = by_tier.get(t, [])
        if not g:
            continue
        o = sum(1 for r in g if r["is_oa"])
        nd = sum(1 for r in g if not r["doi"])
        L.append(f"| `{t}` | {len(g)} | {o} ({pc(o, len(g))}) | {nd} |")
    L += ["", "## The ceiling, by design — the cross-tab the fetch will be judged on", "",
          "A.17's lesson, restated: a retrieval RATE hides WHICH records were missed. The 22 "
          "identified designs in this queue carry whatever GRADE rating each arm gets, and their "
          "open-access ceiling is the number worth watching.", "",
          "| Design | n | Open access |", "|---|---|---|"]
    for d in ["identified", "observational", "descriptive", "cannot_tell", "theory"]:
        g = by_design.get(d, [])
        if not g:
            continue
        o = sum(1 for r in g if r["is_oa"])
        L.append(f"| `{d}` | {len(g)} | {o} ({pc(o, len(g))}) |")
    L += ["", f"Of the **{len(ident)} identified designs**, "
          f"{sum(1 for r in ident if r['is_oa'])} are open and "
          f"{sum(1 for r in ident if not r['doi'])} carry no DOI.", "",
          "## Deterministic rungs — populations counted before any request is spent", "",
          "| Rung | Records | Why it is a construction, not a search |", "|---|---|---|"]
    RUNG_WHY = {
        "demographic_research": "`10.4054/DemRes.V.A` fixes the PDF path exactly; the journal is "
                                "fully open access",
        "mpidr_working_paper": "`10.4054/mpidr-{wp,tr}-YYYY-NNN` fixes the path under "
                               "`demogr.mpg.de/papers/`; SAME PREFIX as the journal, different "
                               "construction",
        "osf_socarxiv": "OSF serves the file from an API endpoint rather than a defended page",
        "nber": "`10.3386/wNNNN` fixes the working-paper PDF path exactly",
    }
    for k, n in det.most_common():
        L.append(f"| `{k}` | {n} | {RUNG_WHY.get(k, '')} |")
    if not det:
        L.append("| — | 0 | no DOI in the queue has a constructible shape |")
    L += ["", f"**{len(no_doi)} queued records carry no DOI** "
          f"({pc(len(no_doi), len(rows))}). Unpaywall, PMC and every deterministic rung need one; "
          "these have only their OpenAlex locations, and they are counted apart at every step so "
          "that no rate quietly averages them with the resolvable records.", "",
          "## Predictions this run is testing", "",
          "1. **The two `10.4054` rungs are near-perfect.** One DOI prefix, two publishers' "
          "objects, two constructions: 8 Demographic Research articles and 6 MPIDR working papers "
          "and technical reports. A rung written at the PREFIX would have taken the 8 and silently "
          "dropped the 6. C.3.g's equivalent deterministic rung found one url; these should find "
          "all fourteen.",
          "2. **PMC is low but non-zero.** 22 records carry a `PubMed` venue. Three chapters running "
          "(A.12, A.24, C.3.g) have returned ~zero; if this one does too, the rung should be retired "
          "from the shared scaffold rather than carried by habit.",
          "3. **Failures are BLOCKED, not closed** — `route_blocked` should exceed `no_url` among "
          "records OpenAlex calls open.", ""]
    if ERRORS:
        L += [f"## Failed probes ({len(ERRORS)}) — excluded from every count above", ""]
        L += [f"- `{w}` — {e}" for w, e in ERRORS[:20]] + [""]
        L += ["A failed probe is an UNKNOWN ceiling, not a closed record. They stay in the fetch "
              "queue and are reported as their own outcome.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"\nwantlist {len(rows)}; OA {n_oa} ({pc(n_oa, len(rows))}); no DOI {len(no_doi)}; "
          f"probe errors {len(ERRORS)}")
    print("det rungs:", dict(det))
    print(f"-> {os.path.relpath(OUT_OA, ROOT)}")


if __name__ == "__main__":
    main()
