#!/usr/bin/env python3
"""
207_c3g_pdf_wantlist.py — C.3.g, stage 5a. Build the retrieval wantlist and probe OA status.

The screen sent 114 records forward (80 RELEVANT + 34 UNCERTAIN). This assigns each to a RETRIEVAL
JOB, probes its open-access status, and writes the wantlist the fetcher works from.

JOBS ARE TRIAGED BY ROLE, NOT BY CELL — the A.17 practice. A cell tells you which estimand a record
belongs to; a job tells you what breaks if it is not retrieved. They are different questions and the
second is the one that should order a retrieval queue.

  J1  THE DIRECT ARM. Own debt against a fertility outcome — the chapter's registered estimand and
      the only thing GRADE attaches to. 20 records, of which 4 read as identified. **If only one job
      is retrieved, it is this one**: the chapter can report a chain-arm bound without full texts,
      but it cannot rate its own claim without these.
  J2  THE DECISIVE TITLE-ONLY RECORDS. Records whose verdict rests on a title because the index
      carries no abstract, and whose titles promise something the chapter turns on — a HECS fertility
      study, a long-run federal-loan fertility study, an explicit "Education, Not Student Debt"
      negative. A title-only RELEVANT is a claim about a title; retrieval is what makes it a claim
      about a study.
  J3  THE IDENTIFIED CHAIN ARM. The quasi-experimental link-1 evidence — Mezza, Gicheva, Goodman,
      the tuition-instrument records. Better identified than anything in J1 and answering a
      neighbouring question, so it is retrieved second, not first.
  J4  P6 / INTENTIONS. Stated norms, expectations and vignettes, kept apart from realized fertility
      on the D.3.b precedent.
  J5  THE REST OF THE CHAIN ARM. Associational housing and union records.
  J6  UNCERTAIN. Everything the screen could not settle; retrieval is how it gets settled.

RUNG-ORDER PREDICTION, RECORDED BEFORE THE RUN because the standing finding is that rung order is
chapter-specific and must be measured rather than inherited. A.17 predicted PMC would finally pay on
a clinical literature; C.3.g predicts the opposite and something else instead:

  * **PMC should return ~zero.** This is economics, sociology and household finance — NBER, FEDS,
    SSRN, RePEc, JOLE, Demography, Socius. PMC indexes biomedicine. If it returns zero here that is
    a third chapter's evidence for retiring the rung from the shared scaffold, after A.12 and A.24.
  * **The WORKING-PAPER rung should pay unusually well.** An unusual share of this chapter's records
    exist as free NBER, FEDS, SSRN or institutional-repository copies of paywalled articles — the
    version-pair structure that has already shown up throughout this chapter. That rung is added here
    and measured separately so it can be justified or dropped on evidence.
  * **Expect a high BLOCKED share, not a high closed share.** The P2 retrieval already met it: WUSTL
    Open Scholarship and SAGE both returned 403 to curl on OPEN-ACCESS content, while the landing
    page served the whole abstract. A 200 carrying HTML is a blocked route, not a closed paper, and
    the two go to different humans downstream.

Output: extraction/{slug}-oa-status.json
        literature/search-logs/{slug}-wantlist.md
"""
import json, os, re, subprocess, sys, time
from collections import Counter

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-wantlist.md")


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

# Titles whose retrieval the chapter turns on, named rather than derived, because "decisive" is a
# judgement about the argument and not a property visible in the metadata.
DECISIVE_TITLE_ONLY = [
    "hecs on fertility",                      # Australia, income-contingent regime
    "long-run effects of federal student loans on fertility",
    "transition to parenthood",               # the 2012 direct-arm record
    "education, not student debt",            # the explicit negative on the confound
    "changing nature of the association",     # exposure-era heterogeneity, PI call 2
    "echoes of rising tuition",               # tuition instrument WITH attainment
    "student loan relief and home purchase",  # policy variation on a household outcome
    "married with children",
    "role of student debt, consumer debt",    # separates debt types
    "impact of student debt on education, career, and marriage",
]


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


def job_of(r):
    """One job per record, first match wins. Order encodes retrieval priority."""
    t = (r.get("title") or "").lower()
    decisive = any(k in t for k in DECISIVE_TITLE_ONLY)
    if r["screen_verdict"] == "UNCERTAIN":
        return "J6_UNCERTAIN"
    if r["screen_arm"] == "direct" and r["screen_outcome"] != "other":
        return "J1_DIRECT_ARM"
    if decisive and not r.get("has_abstract"):
        return "J2_DECISIVE_TITLE_ONLY"
    if r["screen_arm"] == "chain" and r["screen_design"] == "identified":
        return "J3_IDENTIFIED_CHAIN"
    if r["screen_outcome"] == "other" or r["screen_arm"] == "direct":
        return "J4_INTENTIONS"
    return "J5_CHAIN_REST"


JOB_NOTE = {
    "J1_DIRECT_ARM": "the registered estimand; GRADE attaches here and nowhere else",
    "J2_DECISIVE_TITLE_ONLY": "verdict currently rests on a title the chapter turns on",
    "J3_IDENTIFIED_CHAIN": "quasi-experimental link 1 — better evidence, different question",
    "J4_INTENTIONS": "P6; stated intentions, kept apart from realized fertility",
    "J5_CHAIN_REST": "associational housing and union records",
    "J6_UNCERTAIN": "the screen could not settle these; retrieval is how they settle",
}


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    recs = json.load(open(SCREENED))
    fwd = [r for r in recs if r.get("screen_verdict") in ("RELEVANT", "UNCERTAIN")]

    rows = []
    for i, r in enumerate(fwd, 1):
        m = oa_lookup(r["id"])
        loc = (m or {}).get("best_oa_location") or {}
        n_open = sum(1 for l in ((m or {}).get("locations") or []) if l.get("is_oa"))
        rows.append(dict(
            id=r["id"], job=job_of(r), title=r["title"], year=r.get("year"),
            venue=r.get("venue"), type=r.get("type"),
            doi=(r.get("doi") or ((m or {}).get("doi") or "").replace("https://doi.org/", "")) or None,
            is_oa=bool(((m or {}).get("open_access") or {}).get("is_oa")),
            oa_status=((m or {}).get("open_access") or {}).get("oa_status"),
            n_open_locations=n_open,
            best_url=loc.get("pdf_url") or loc.get("landing_page_url"),
            screen_verdict=r["screen_verdict"], screen_arm=r["screen_arm"],
            screen_outcome=r["screen_outcome"], screen_design=r["screen_design"],
            has_abstract=bool(r.get("has_abstract")), is_anchor=bool(r.get("is_anchor")),
        ))
        if i % 20 == 0:
            print(f"  probed {i}/{len(fwd)}")
        time.sleep(0.15)

    os.makedirs(EXTRACT, exist_ok=True)
    json.dump(rows, open(OUT_OA, "w"), indent=2)

    jobs = Counter(r["job"] for r in rows)
    oa_by_job = {j: [r for r in rows if r["job"] == j] for j in jobs}
    n_oa = sum(1 for r in rows if r["is_oa"])
    no_doi = [r for r in rows if not r["doi"]]
    types = Counter(r["type"] for r in rows)
    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"

    L = [f"# Stage 5a retrieval wantlist — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/207_c3g_pdf_wantlist.py`", "",
         f"**{len(rows)} records** forward from the screen ({sum(1 for r in rows if r['screen_verdict'] == 'RELEVANT')} "
         f"RELEVANT + {sum(1 for r in rows if r['screen_verdict'] == 'UNCERTAIN')} UNCERTAIN). "
         f"**{n_oa} ({pc(n_oa, len(rows))}) are open access** by OpenAlex's reckoning — which is a "
         "CEILING on what the automatic fetch can get, not a prediction of it: the P2 retrieval "
         "already found two open-access hosts returning 403 to a script.", "",
         "## Jobs, in retrieval order", "",
         "| Job | n | OA | What breaks without it |", "|---|---|---|---|"]
    for j in sorted(jobs):
        g = oa_by_job[j]
        o = sum(1 for r in g if r["is_oa"])
        L.append(f"| `{j}` | {len(g)} | {o} ({pc(o, len(g))}) | {JOB_NOTE[j]} |")
    L += ["", f"**{len(no_doi)} records carry no DOI at all.** A record with no DOI cannot be "
          "resolved by Unpaywall or PMC and has only its OpenAlex locations; they are the ones most "
          "likely to end in a human's hands.", "",
          "| Record type | n |", "|---|---|"]
    for t, n in types.most_common():
        L.append(f"| {t} | {n} |")
    L += ["", "## The prediction this run is testing", "",
          "Recorded before the fetch, per the standing rule that rung order is chapter-specific:",
          "",
          "1. **PMC returns ~zero.** Economics, sociology and household finance; PMC indexes "
          "biomedicine. A third zero after A.12 and A.24 is grounds to retire the rung.",
          "2. **The working-paper rung pays unusually well** — NBER, FEDS, SSRN, RePEc and "
          "institutional repositories carry free copies of this literature's paywalled articles, "
          "and the version-pair structure has recurred throughout this chapter.",
          "3. **Failures are BLOCKED, not closed.** Expect `route_blocked` to dominate `no_url`.", ""]
    if ERRORS:
        L += ["", f"## Failed probes ({len(ERRORS)}) — excluded from every count above", ""]
        L += [f"- `{w}` — {e}" for w, e in ERRORS[:20]] + [""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"wantlist {len(rows)} records; OA {n_oa} ({pc(n_oa, len(rows))}); no DOI {len(no_doi)}; "
          f"probe errors {len(ERRORS)}")
    print("jobs:", dict(jobs))
    print(f"-> {os.path.relpath(OUT_OA, ROOT)}")


if __name__ == "__main__":
    main()
