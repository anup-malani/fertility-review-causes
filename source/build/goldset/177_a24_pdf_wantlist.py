#!/usr/bin/env python3
"""
177_a24_pdf_wantlist.py — A.24, stage 5 prep. Build the retrieval wantlist and measure the OA ceiling.

Inherits `166_a12_pdf_wantlist.py`. Checks open-access status LIVE before writing, so the list states
what an automated fetch can reach and what needs a human with a library proxy BEFORE the fetch rather
than after. B.1 learned that the expensive way: its automated ceiling hit 20 of 95 and its pooled
estimate has rested on five studies ever since.

**THE JOB THAT SHAPES THIS CHAPTER'S RETRIEVAL IS JOB A2, AND IT IS THE OPPOSITE OF A.12's PROBLEM.**
A.12 had to retrieve 223 records to harvest a nuisance table nobody advertised. A.24's difficulty is
that its causal literature is SMALL and its mechanism literature is LARGE: the screen returned 94
causal records against 193 mechanism records, and the cell the registry entry is actually about holds
TWO. So the rule here is not triage-by-sampling but triage-by-cell:

  A1  `PRIMARY_APP_FERTILITY` — both records. They are one German study and its own working paper,
      and between them they decide whether this chapter reports an empty cell or a single estimate.
      Nothing else on the list matters as much.
  A2  `SECONDARY_TECH_*` — all of them. This is Wall 9's population and it is where the chapter's
      identification actually lives: broadband on teen fertility, broadband and cell phones on
      marriage and divorce, internet exposure on age at first marriage, and the post-2007 digital
      technology paper. None of these was reachable through the app axis, so an OA failure here is
      not recoverable by any other route.
  A3  `PRIMARY_APP_UNION` — all. The reachable spine, including the records that disagree with each
      other about the SIGN, which are the ones that matter most.
  A4  `REVERSE_DIRECTION` — all three. Small, and the risk-of-bias section needs them.

  B   NO-ABSTRACT records whose TITLE implies an identified design, from any cell. The screen could
      not read these and said so; retrieval is the only thing that can. Selected by rule on the
      title, not by hand.

  C   `MECHANISM_CHOICE_FRICTION`, rule-selected from the screen notes. 193 records cannot each carry
      a demographic quantity and retrieving them all to support one section is not proportionate. The
      rule targets (C1) the mechanism canon and its meta-analysis, (C2) the Wall 4 include side —
      platform studies whose outcome is MATCHING rather than engagement, and (C3) records whose note
      records a partnership or singlehood outcome. The remainder is DEPRIORITISED and counted, so the
      mechanism section can state what it did not read.

  D   `EXPOSURE_SERIES`, rule-selected for stage 10: the records carrying an adoption SERIES or a
      share-of-couples-meeting-online quantity, not the motive surveys and user-profile studies whose
      numbers stage 10 cannot use.

**Read the OA rate by job, not in aggregate.** It will correlate with job here even more than it did
on A.12: JOB A2 is economics journals and working papers, JOB C is psychology and communication, JOB
D is surveys and encyclopedia entries. An OA-only evidence base would systematically over-represent
whichever arm publishes more openly, and for this chapter that would mean grading the mechanism
literature while the identification literature stayed behind a paywall.

Target paths follow the house convention `literature/pdfs/{slug}/{WID}__{title-slug}.pdf`, so a file
dropped there is picked up by ingest without renaming. That directory is gitignored.

Output: literature/search-logs/{slug}-pdf-wantlist.md
        extraction/{slug}-retrieval-dois.txt
        extraction/{slug}-oa-status.json
"""
import json, os, re, subprocess, time
from collections import Counter

SLUG = "dating-apps-union-formation-friction"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-pdf-wantlist.md")
OUT_DOI = os.path.join(EXTRACT, f"{SLUG}-retrieval-dois.txt")
OUT_OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}

CAUSAL_JOBS = [("A1", {"PRIMARY_APP_FERTILITY"}),
               ("A2", {"SECONDARY_TECH_UNION", "SECONDARY_TECH_FERTILITY"}),
               ("A3", {"PRIMARY_APP_UNION"}),
               ("A4", {"REVERSE_DIRECTION"})]

# JOB B — title vocabulary that implies an identified design. Applied ONLY to records the screen
# could not read (no abstract reached it), so this rule never overrides a human reading.
B_DESIGN = ("impact of", "effect of", "effects of", "evidence from", "causal", "field experiment",
            "natural experiment", "randomized", "randomised", "quasi-experiment",
            "difference-in-differences", "instrument")

# JOB C selection rules, keyed on the screen note so the set is DERIVED and re-runs identically if
# the screen is revised. Legend: `k` the mechanism canon and its meta-analysis, `w` the Wall 4
# include side (matching outcomes), `p` a partnership or singlehood outcome named in the note.
C_RULES = [("k", ("CORE MECHANISM", "FOUNDATIONAL", "CRITICAL", "META-ANALYTIC", "DIRECTLY RE-EXAMINES")),
           ("w", ("WALL 4 INCLUDE SIDE", "matching outcome", "MATCHING", "congestion", "popularity")),
           ("p", ("still single", "STILL SINGLE", "singlehood", "SINGLEHOOD", "partnership",
                  "conversion", "first date", "FIRST DATE", "offline meeting", "MEETING"))]

# JOB D selection rules, same convention. `s` an adoption or meeting-share series, `n` nationally
# representative, `r` a prior review whose included studies can be mined.
D_RULES = [("s", ("adoption", "prevalence", "share of", "trend", "series", "how couples meet",
                  "meeting-channel", "meeting online", "where", "NATSAL", "HCMST")),
           ("n", ("nationally representative", "NATIONALLY REPRESENTATIVE", "national", "US-wide",
                  "one in ten", "Pew")),
           ("r", ("SYSTEMATIC REVIEW", "systematic review", "meta-synthesis", "literature review",
                  "review of the online-dating literature", "DEMOGRAPHIC perspective"))]


def oa_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = oa_key()
errors = []


def oa_batch(ids):
    """OA status for up to 50 ids in one request. Pipes are OR in an OpenAlex filter; commas would be
    fatal inside a filter value and are never used here."""
    url = ("https://api.openalex.org/works?filter=openalex_id:" + "|".join(ids) +
           "&per-page=50&select=id,doi,open_access,best_oa_location,locations,primary_location,type"
           f"&api_key={KEY}")
    try:
        out = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, url],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
    except Exception as e:
        errors.append(("batch", str(e)[:100]))
        return []
    if not isinstance(d, dict) or d.get("error") or "results" not in d:
        errors.append(("batch", str(d)[:120]))
        return []
    return d["results"]


def note_match(note, pats):
    n = note or ""
    return any(p in n for p in pats)


def main():
    rows = json.load(open(SCREENED))
    by_id = {r["id"]: r for r in rows}
    want = {}   # id -> (job, reason)

    for job, cells in CAUSAL_JOBS:
        for r in rows:
            if r["cell"] in cells:
                want[r["id"]] = (job, f"cell {r['cell']}")

    # JOB B: the screen could not read these; the title says it might be a design.
    for r in rows:
        if r["id"] in want:
            continue
        no_abstract = "No abstract" in (r.get("screen_note") or "") or \
                      "no abstract" in (r.get("screen_note") or "")
        t = (r["title"] or "").lower()
        if no_abstract and any(p in t for p in B_DESIGN):
            want[r["id"]] = ("B", "no abstract; title implies an identified design")

    c_defer, d_defer = [], []
    for r in rows:
        if r["id"] in want:
            continue
        if r["cell"] == "MECHANISM_CHOICE_FRICTION":
            tags = [t for t, pats in C_RULES if note_match(r.get("screen_note"), pats)]
            if tags:
                want[r["id"]] = ("C" + "".join(tags), "mechanism rule " + "/".join(tags))
            else:
                c_defer.append(r)
        elif r["cell"] == "EXPOSURE_SERIES":
            tags = [t for t, pats in D_RULES if note_match(r.get("screen_note"), pats)]
            if tags:
                want[r["id"]] = ("D" + "".join(tags), "exposure rule " + "/".join(tags))
            else:
                d_defer.append(r)

    ids = sorted(want)
    print(f"wantlist {len(ids)} records; checking OA status live")
    oa = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        for w in oa_batch(chunk):
            wid = w["id"].rsplit("/", 1)[-1]
            best = w.get("best_oa_location") or {}
            locs = [l for l in (w.get("locations") or []) if l.get("pdf_url") or l.get("landing_page_url")]
            oa[wid] = {"status": (w.get("open_access") or {}).get("oa_status"),
                       "is_oa": (w.get("open_access") or {}).get("is_oa"),
                       "url": best.get("pdf_url") or best.get("landing_page_url"),
                       "pdf_url": best.get("pdf_url"),
                       "n_locations": len(locs),
                       "alt_pdfs": [l.get("pdf_url") for l in locs if l.get("pdf_url")][:6],
                       "alt_landing": [l.get("landing_page_url") for l in locs
                                       if l.get("landing_page_url")][:6],
                       "type": w.get("type"), "doi": (w.get("doi") or "").replace("https://doi.org/", "")}
        time.sleep(0.2)
    for wid in ids:
        oa.setdefault(wid, {"status": None, "is_oa": None, "url": None, "pdf_url": None,
                            "n_locations": 0, "alt_pdfs": [], "alt_landing": [], "type": None,
                            "doi": by_id[wid].get("doi")})
    json.dump(oa, open(OUT_OA, "w"), indent=1)
    with open(OUT_DOI, "w") as fh:
        for wid in ids:
            d = oa[wid].get("doi") or by_id[wid].get("doi")
            if d:
                fh.write(d + "\n")

    def jobkey(w):
        return want[w][0]
    jobs = sorted({jobkey(w) for w in ids})
    openable = lambda w: (oa[w].get("status") in OPEN) and bool(oa[w].get("url"))
    n_open = sum(1 for w in ids if openable(w))

    pc = lambda a, b: f"{(a / b * 100):.0f}%" if b else "n/a"
    L = [f"# Retrieval wantlist and OA ceiling — {SLUG} (A.24)", "",
         f"**{len(ids):,} records on the wantlist**, selected BY RULE from the screen output so the "
         "list re-runs identically if the screen is revised. Nothing here was hand-picked except the "
         "cell assignments the screen already made.", "",
         f"**OpenAlex reports {n_open:,} of {len(ids):,} ({pc(n_open, len(ids))}) as open with a "
         "reachable location.** That is a ceiling on what an automated fetch can attempt, not a "
         "prediction of what it will get — A.12's nominally-open set delivered 38% on the first "
         "pass, the rest returning HTML landing pages.", "",
         "## The OA ceiling by job — read this, not the aggregate", "",
         "| job | what it is | n | open | rate |", "|---|---|---|---|---|"]
    JOBDESC = {"A1": "`PRIMARY_APP_FERTILITY` — the cell that decides the headline",
               "A2": "`SECONDARY_TECH_*` — Wall 9's population, where the identification lives",
               "A3": "`PRIMARY_APP_UNION` — the reachable spine",
               "A4": "`REVERSE_DIRECTION` — risk of bias",
               "B": "no abstract; title implies an identified design"}
    for j in jobs:
        sel = [w for w in ids if jobkey(w) == j]
        o = sum(1 for w in sel if openable(w))
        desc = JOBDESC.get(j) or ("mechanism, rule-selected" if j.startswith("C")
                                  else "exposure series, rule-selected" if j.startswith("D") else j)
        L.append(f"| `{j}` | {desc} | {len(sel)} | {o} | **{pc(o, len(sel))}** |")
    L += ["", f"**Deprioritised and counted rather than dropped: {len(c_defer):,} mechanism records "
          f"and {len(d_defer):,} exposure-series records.** The mechanism section must state that it "
          "read a rule-selected subset; the deprioritised exposure records are motive surveys and "
          "user-profile studies whose numbers stage 10 cannot use.", "",
          "## Records, by job", "",
          "| job | oa | cell | title | year | doi |", "|---|---|---|---|---|---|"]
    for w in sorted(ids, key=lambda x: (jobkey(x), by_id[x]["d1_rank"])):
        m, s = by_id[w], oa[w]
        flag = "**open**" if openable(w) else (s.get("status") or "closed")
        L.append(f"| `{jobkey(w)}` | {flag} | `{m['cell']}` | {(m['title'] or '')[:70]} | "
                 f"{m.get('year')} | `{s.get('doi') or m.get('doi') or ''}` |")
    if errors:
        L += ["", "## Failed requests (NOT closed access)", ""] + [f"- {a}: `{b}`" for a, b in errors]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"wantlist={len(ids)} open={n_open} ({pc(n_open, len(ids))}) "
          f"deferred_mechanism={len(c_defer)} deferred_exposure={len(d_defer)} errors={len(errors)}")
    for j in jobs:
        sel = [w for w in ids if jobkey(w) == j]
        print(f"  {j:<5} n={len(sel):<4} open={sum(1 for w in sel if openable(w))}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
