#!/usr/bin/env python3
"""
194_a17_library_wantlist.py — A.17, stage 5. The human handoff, split by WHY the fetch failed.

Inherits `179_a24_library_wantlist.py`, and changes the thing that matters most: the split.

**B.1's WANTLIST WAS ONE UNDIFFERENTIATED LIST OF 71 PDFs AND IT HAS NEVER BEEN CLEARED.** Its pooled
estimate has rested on five studies since July because "needs a human with Zotero and the UChicago
proxy" is a single large ask with no internal ordering and no indication that any part of it is easy.
A.17's failures are not one kind of failure and must not be handed over as though they were.

The fetch measured two populations that look identical in a success/failure column and are completely
different jobs:

  1. BLOCKED-BUT-OPEN. A rung FOUND an open-access URL and the fetch returned HTML instead of PDF
     bytes. Verified by hand on three of them across three publishers (OUP, Wiley, Elsevier): all
     return **403 even with a browser user-agent string**, so this is Cloudflare-class bot defence,
     not authentication. **A human with an ordinary browser and no institutional access at all can
     download these by clicking the link.** No proxy, no library, no Zotero connector required.
  2. NO ROUTE. No rung found any open URL. These are the genuine library job.

Reporting them together would tell an RA that 98 records need a proxy when 67 of them need a browser.
That is the difference between an afternoon and a project that never happens.

**The rung counters behind this split are themselves a correction.** The first version of `193_`
counted only successful fetches per rung, which showed PMC and Unpaywall at zero and would have
retired both from the shared scaffold. Counting URLs FOUND separately showed PMC found 27 candidates
and Unpaywall 65 — live rungs being defeated downstream by publishers. A rung retired on a
publisher's bot-block is refusals-read-as-zeros in retrieval costume.

Output: literature/search-logs/{slug}-library-wantlist.md
        extraction/{slug}-blocked-but-open.txt   (paste-ready URL list)
"""
import csv, json, os
from collections import Counter

SLUG = "art-access-fertility-recovery"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
FETCH = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-library-wantlist.md")
OUT_URLS = os.path.join(EXTRACT, f"{SLUG}-blocked-but-open.txt")

JOB_ORDER = ["A1_COUNTERFACTUAL", "A2_IDENTIFIED", "A3_SHARE", "A4_P5_CONVERSION",
             "A5_P6_BEHAVIOUR", "B_NO_ABSTRACT", "C_EXPOSURE_SERIES"]
JOB_WHY = {
    "A1_COUNTERFACTUAL": "**The chapter's headline number is conditional on this job.** Arm 1 counts "
                         "ART births; that count is an upper bound whose tightness is set by how "
                         "often untreated or dropped-out couples conceive anyway. Retrieve first.",
    "A2_IDENTIFIED": "The only identified evidence in the chapter. Closed here is unrecoverable by "
                     "any other route.",
    "A3_SHARE": "The records that actually report a contribution. Arm 1's numerator.",
    "A4_P5_CONVERSION": "Whether frozen eggs become births. The elective cell's whole verdict.",
    "A5_P6_BEHAVIOUR": "The realized-outcome records. The difference between 'unmeasured' and "
                       "'measured and small'.",
    "B_NO_ABSTRACT": "Title implies an estimate and the screen could not read the record. The "
                     "title-only safeguard was measured inert, so retrieval is the only check.",
    "C_EXPOSURE_SERIES": "Stage 10 inputs. Latest edition per registry family.",
}


def main():
    fetch = list(csv.DictReader(open(FETCH)))
    oa = {r["id"]: r for r in json.load(open(OA))}
    fail = [r for r in fetch if r["ok"] != "True"]
    blocked = [r for r in fail if r["note"] == "route_blocked"]
    noroute = [r for r in fail if r["note"] != "route_blocked"]
    got = [r for r in fetch if r["ok"] == "True"]

    urls = []
    for r in blocked:
        m = oa.get(r["id"]) or {}
        if m.get("best_url"):
            urls.append(m["best_url"])
    open(OUT_URLS, "w").write("\n".join(urls) + "\n")

    def table(rows, header):
        L = ["| job | year | title | venue | DOI | open URL |", "|---|---|---|---|---|---|"]
        for r in sorted(rows, key=lambda x: (JOB_ORDER.index(x["job"]) if x["job"] in JOB_ORDER
                                             else 99, -(oa.get(x["id"], {}).get("year") or 0))):
            m = oa.get(r["id"]) or {}
            u = m.get("best_url") or ""
            L.append(f"| `{r['job'].split('_')[0]}` | {m.get('year')} | "
                     f"{(m.get('title') or '')[:78].replace('|','/')} | "
                     f"{(m.get('venue') or '')[:26].replace('|','/')} | `{r['doi'] or '—'}` | "
                     f"{('[link](' + u + ')') if u else '—'} |")
        return [header, ""] + L + [""]

    pc = lambda a, b: f"{a / max(b, 1):.0%}"
    L = [f"# Stage 5 human handoff — {SLUG} (A.17)", "",
         f"**{len(got)} of {len(fetch)} retrieved automatically ({pc(len(got), len(fetch))}).** The "
         f"remaining {len(fail)} split into TWO DIFFERENT JOBS, and the split is the point of this "
         "document.", "",
         f"| | n | what it needs | who can do it |", "|---|---|---|---|",
         f"| **BLOCKED-BUT-OPEN** | **{len(blocked)}** | a browser | anyone, no institutional access |",
         f"| **NO ROUTE** | **{len(noroute)}** | a library proxy | someone with UChicago access |", "",
         "**Why this split exists.** B.1's wantlist was one undifferentiated list of 71 PDFs and it "
         "has never been cleared — its pooled estimate has rested on five studies since July, because "
         "a single large ask with no internal ordering and no sign that any part is easy is an ask "
         "nobody starts. Two thirds of A.17's failures need no institutional access at all.", "",
         "## 1. BLOCKED-BUT-OPEN — these are free, and a script cannot have them", "",
         f"For each of these an open-access URL was FOUND. The fetch returned HTML rather than PDF "
         "bytes. Checked by hand on three records across three publishers — Oxford University Press, "
         "Wiley and Elsevier — and all three return **403 even with a browser user-agent string**. "
         "This is Cloudflare-class bot defence, not authentication.", "",
         f"**A paste-ready URL list is at `extraction/{SLUG}-blocked-but-open.txt` "
         f"({len(urls)} links).** Opening them in a browser and saving to "
         f"`literature/pdfs/{SLUG}/` is the whole job; the ingest picks up any file dropped there "
         "and the naming convention is `{WID}__{title-slug}.pdf`.", ""]
    L += table(blocked, "### The blocked list, in job order")
    L += ["## 2. NO ROUTE — the genuine library job", "",
          "No rung found any open URL for these. This is where a proxy is actually required.", ""]
    L += table(noroute, "### The library list, in job order")

    L += ["## Damage, by job", "",
          "Read this by row. A gap in A1 changes the chapter's central number; a gap in C changes a "
          "table in stage 10.", "",
          "| job | retrieved | blocked-but-open | no route | why the job matters |",
          "|---|---|---|---|---|"]
    for j in JOB_ORDER:
        g = sum(1 for r in got if r["job"] == j)
        b = sum(1 for r in blocked if r["job"] == j)
        n = sum(1 for r in noroute if r["job"] == j)
        if g + b + n == 0:
            continue
        L.append(f"| `{j}` | {g} | {b} | {n} | {JOB_WHY.get(j, '')} |")
    L += ["",
          "## What the chapter may NOT say until this is cleared", "",
          "Stage 5 is not complete and the write-up must not imply that it is. Specifically:", "",
          "- **No pooled or summary statement about arm 1's counterfactual** until job A1 is in "
          "hand. The upper-bound argument is the chapter's spine and it currently rests on abstracts.",
          "- **No claim that an access margin has or has not been estimated** until job A2 is in "
          "hand, because an unread identified study and a nonexistent one are the same evidence and "
          "opposite conclusions.",
          "- **No verdict on P5's emptiness.** The elective cell's conversion records are the worst-"
          "retrieved job in the chapter, and 'we could not download it' is not 'nobody measured it'.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"retrieved={len(got)} blocked_but_open={len(blocked)} no_route={len(noroute)} "
          f"urls_written={len(urls)}")
    for j in JOB_ORDER:
        g = sum(1 for r in got if r["job"] == j)
        b = sum(1 for r in blocked if r["job"] == j)
        n = sum(1 for r in noroute if r["job"] == j)
        if g + b + n:
            print(f"  {j:22} got={g:>3} blocked={b:>3} noroute={n:>3}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
