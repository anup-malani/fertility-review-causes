#!/usr/bin/env python3
"""
179_a24_library_wantlist.py — A.24, stage 5. The banded procurement list for a human with a proxy.

Inherits `169_a12_library_wantlist.py`. **The BANDING is the product, not the list.** A flat list of
DOIs gets worked from the top and abandoned in the middle, which selects the evidence base by
alphabetical accident. A partial run is expected; the instruction to whoever works it is to state the
band they reached, so the chapter can say exactly what it read and what it did not.

A.24's banding differs from A.12's in one way that matters. A.12's P0 was its causal spine and its P1
was four methods entry points into a cell screening could not see. A.24's P0 is smaller and sharper:
ONE record decides whether the chapter reports an empty cell or a single estimate, and a handful of
identified technology-diffusion estimates decide whether it has any identification at all. Everything
else can be missing without changing a verdict.

The funnel is reported at each step because a bounded retrieval that goes unstated reads as complete
coverage.

Output: literature/search-logs/{slug}-library-wantlist.md
"""
import csv, json, os
from collections import Counter

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
FETCH = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
OUT = os.path.join(LOGS, f"{SLUG}-library-wantlist.md")
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}


def main():
    scr = {r["id"]: r for r in json.load(open(SCREENED))}
    oa = json.load(open(OA))
    got = set()
    fetched = list(csv.DictReader(open(FETCH)))
    for r in fetched:
        if r["fetch"] in ("OK", "CACHED"):
            got.add(r["id"])
    blocked = {r["id"] for r in fetched if r["fetch"] == "FAILED" and "route blocked" in (r["fetch_note"] or "")}

    want = list(oa)
    missing = [w for w in want if w not in got]

    def band(w):
        c = scr[w]["cell"]
        note = scr[w].get("screen_note") or ""
        # P0 is defined by the SCREEN's own judgement, not by cell membership alone. The first
        # version of this rule keyed P0 on `PRIMARY_APP_FERTILITY` plus flagged `SECONDARY_TECH_*`
        # records, and it dropped the Economics Letters Tinder paper — the ONLY identified estimate
        # of app exposure on marriage anywhere in the frame — into P3, because its cell is
        # `PRIMARY_APP_UNION`. A band derived from cell membership cannot see a note that says
        # "IDENTIFIED ESTIMATE ... P0 for retrieval". The note is the judgement; the band reads it.
        if c == "PRIMARY_APP_FERTILITY":
            return "P0"
        if "P0" in note or "IDENTIFIED ESTIMATE" in note or "MOST IMPORTANT" in note:
            return "P0"
        if c.startswith("SECONDARY_TECH") and ("WALL 9 RECORD" in note or "MAJOR" in note):
            return "P0"
        if c.startswith("SECONDARY_TECH"):
            return "P1"
        if "no abstract" in note.lower() and c in ("PRIMARY_APP_UNION", "INSUFFICIENT_INFO"):
            return "P2"
        if c == "PRIMARY_APP_UNION":
            return "P3"
        if c == "REVERSE_DIRECTION":
            return "P3"
        if c == "MECHANISM_CHOICE_FRICTION":
            return "P4"
        return "P5"

    BANDDESC = {
        "P0": "**Decides a verdict.** The `PRIMARY_APP_FERTILITY` journal version, and the identified "
              "technology-diffusion estimates the screen flagged as major. If only one band is "
              "worked, work this one.",
        "P1": "The rest of `SECONDARY_TECH_*` — Wall 9's population. None of it was reachable through "
              "the app axis, so a miss here is unrecoverable by any other route.",
        "P2": "Records the SCREEN COULD NOT READ (no abstract) whose titles imply an identified "
              "design. Retrieval is the only thing that can classify them.",
        "P3": "`PRIMARY_APP_UNION` and `REVERSE_DIRECTION` — the reachable spine and the "
              "reverse-causality set.",
        "P4": "Rule-selected mechanism records.",
        "P5": "Exposure series and residual.",
    }
    bands = {}
    for w in missing:
        bands.setdefault(band(w), []).append(w)

    n_open_nominal = sum(1 for w in want if oa[w].get("status") in OPEN and oa[w].get("url"))
    pc = lambda a, b: f"{(a / b * 100):.0f}%" if b else "n/a"
    L = [f"# Library procurement list — {SLUG} (A.24)", "",
         f"**{len(missing):,} of {len(want):,} wantlist records need a human with a library proxy.** "
         f"{len(got):,} are readable now ({pc(len(got), len(want))}).", "",
         "## The retrieval funnel, stated so the loss is visible at each step", "",
         "| step | n | note |", "|---|---|---|",
         f"| wantlist | {len(want):,} | selected by rule from 887 screened |",
         f"| OpenAlex says open | {n_open_nominal:,} | {pc(n_open_nominal, len(want))} |",
         f"| fetched on the first pass | {sum(1 for r in fetched if r['rung']=='0' and r['fetch']=='OK'):,} | "
         "of the nominally-open |",
         f"| recovered by rungs 1-3 | {sum(1 for r in fetched if r['rung'] in ('1','2','3') and r['fetch']=='OK'):,} | "
         "alternate OA locations, `citation_pdf_url`, PMC |",
         f"| **readable** | **{len(got):,}** | **{pc(len(got), len(want))} of the wantlist** |", "",
         f"**{len(blocked):,} failures were HTML interstitials** — a 200 returning a landing page "
         "rather than a PDF. Per the standing discipline those are BLOCKED ROUTES, not closed papers, "
         "which is why they appear on this list rather than in a 'not obtainable' bucket.", "",
         "**Rung yields, recorded so the next chapter orders its rungs by evidence rather than "
         "guess:** best_oa_location 20, alternate OA locations 6, `citation_pdf_url` 7, **PMC 0**. "
         "The PMC zero was predicted in `178_`'s docstring before the run — this chapter's literature "
         "is economics, sociology and communication, and PMC indexes none of it. B.6 built its "
         "recovery rung around PMC; A.12 measured it at zero; A.24 confirms that the ordering is a "
         "property of the literature, not of the code.", "",
         "## Bands", ""]
    for b in sorted(bands):
        L += [f"### {b} — {len(bands[b])} records", "", BANDDESC.get(b, ""), "",
              "| cell | title | year | doi | route |", "|---|---|---|---|---|"]
        for w in sorted(bands[b], key=lambda x: scr[x]["d1_rank"]):
            m, s = scr[w], oa[w]
            route = "**blocked route**" if w in blocked else (s.get("status") or "closed")
            L.append(f"| `{m['cell']}` | {(m['title'] or '')[:66]} | {m.get('year')} | "
                     f"`{s.get('doi') or m.get('doi') or ''}` | {route} |")
        L.append("")
    L += ["## What is deliberately NOT on this list, and reported rather than dropped", "",
          "159 mechanism records and 42 exposure-series records were deprioritised at `177_` by "
          "rule. The mechanism section must state that it read a rule-selected subset; the "
          "deprioritised exposure records are motive surveys and user-profile studies whose numbers "
          "stage 10 cannot use. Neither group is deleted and both re-select identically if the screen "
          "is revised.", ""]
    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"missing={len(missing)} of {len(want)}; readable={len(got)} ({pc(len(got), len(want))})")
    for b in sorted(bands):
        print(f"  {b}: {len(bands[b])}")
    print(f"-> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
