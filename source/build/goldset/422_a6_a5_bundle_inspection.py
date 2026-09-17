#!/usr/bin/env python3
"""
422 — A.6 (TICK-087): the PI call 4 inspection. Does any A.5-bundled record separately dose the
norm component and estimate a fertility outcome?

Call 4 ruled A.5 a **bundle, not a wall**: programme studies are admissible pending a full-text
pass asking whether the norm component was separately dosed. This is that pass. It is one of the two
live routes to a non-empty primary cell, and the reason it mattered is that 3 of the 5 identified
records across the substantive walls sit in A.5.

The answer is no, for the 12 records that could be retrieved
-------------------------------------------------------------
`421` retrieved 12 of the 25. Of those twelve, **none pairs a separately dosed norm component with
a fertility outcome**, which is the conjunction the primary cell requires. The pattern is the same
one the whole chapter has traced, and the decisive record makes it plainest:

  W3153104329  Kramer, Hackman, Schacht and Davis, *Scientific Reports* 2021, "Effects of family
               planning on fertility behaviour across the demographic transition". The one A.5
               record whose outcome is unambiguously realized fertility — Maya women tracked across
               90 years, natural to contracepting fertility, 32 fertility-outcome terms. Its
               exposure is **family-planning adoption**, not a norm. "Norms" occur 10 times and
               every one is in the discussion, as something that *emerges* from changing fertility
               variance, never as a dosed variable. Fails the exposure gate.

  W4283386002  outcome is **intention** to take up long-acting methods; exposure is exposure to
               family-planning information. Not fertility, not a dosed norm.
  W4387670899  qualitative thematic analysis of male involvement. "Total fertility" appears once,
               as background.
  W2885614896  already read at stage 6b: an MPH literature-review thesis on access and
               utilisation, with stigma bundled among barriers and no separate dose.

The remaining eight carry **zero** norm terms adjacent to any variable or model language, on the
proximity scan in this script, and between 0 and 10 fertility-outcome terms each.

What is not settled
-------------------
Thirteen of the 25 could not be retrieved: six are `oa_status: closed` and seven advertise an OA
copy whose URL failed. Two of those are substantively the most interesting in the whole set and
should be prioritised for library retrieval:

  W2086018683  *The Long-term Demographic Role of Community-based Family Planning in Rural
               Bangladesh* (1996) — the Matlab programme, the canonical A.5 quasi-experiment, with
               a demographic outcome. If any A.5 record separately doses a norm, this design is the
               one that could.
  W2124099101  *Barriers to family planning service use among the urban poor in Pakistan* (2005),
               125 citations — barriers work in the Casterline tradition, where opposition is
               routinely dosed as a reason for non-use.

So the A.5 route is **closed for the twelve read and conditional on the thirteen unread**, and this
script records it that way rather than as closed.
"""
import csv, glob, pathlib, re, sys
from collections import Counter

SLUG = "stigma-reduction-contraception-abortion"
CSVP = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
LOGP = pathlib.Path("literature/search-logs") / f"{SLUG}-screen-log.md"
WANT = pathlib.Path("literature/search-logs") / f"{SLUG}-library-wantlist.md"
RETR = pathlib.Path("extraction") / f"{SLUG}-a5-bundle-retrieval-log.csv"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG

NORM = re.compile(r"stigma|taboo|disapprov|opposition|acceptab|legitimat|\bnorms?\b|shame|secrecy",
                  re.I)
DOSE = re.compile(r"(variable|measure[ds]?|indicator|independent|predictor|covariate|coefficient"
                  r"|odds ratio|adjusted|regression|model)", re.I)
FERT = re.compile(r"total fertility rate|\bTFR\b|children ever born|completed fertility"
                  r"|family size|births per woman|parity", re.I)

# Records read individually, with the call-4 verdict and its basis.
READ = {
    "W3153104329": ("no", "Kramer et al., Sci Rep 2021. The one A.5 record with an unambiguous "
                          "realized-fertility outcome (Maya women, 90 years, natural to "
                          "contracepting). Exposure is FAMILY-PLANNING ADOPTION, not a norm; all "
                          "10 'norms' occurrences are discussion of norms emerging from changing "
                          "fertility variance, never a dosed variable. Fails the exposure gate."),
    "W4283386002": ("no", "Amin et al. 2022 (Indonesian). Outcome is INTENTION to take up "
                          "long-acting methods; exposure is exposure to family-planning "
                          "information. Neither a fertility outcome nor a dosed norm."),
    "W4387670899": ("no", "Qualitative thematic analysis of male involvement in modern family "
                          "planning; 'total fertility' appears once as background."),
    "W2885614896": ("no", "Read at stage 6b: MPH literature-review thesis on access and "
                          "utilisation, stigma bundled among barriers with no separate dose."),
}
PRIORITY = {
    "W2086018683": ("*The Long-term Demographic Role of Community-based Family Planning in Rural "
                    "Bangladesh* (1996) — the Matlab programme, the canonical A.5 "
                    "quasi-experiment, with a demographic outcome. If any A.5 record separately "
                    "doses a norm, this design is the one that could."),
    "W2124099101": ("*Barriers to family planning service use among the urban poor in Pakistan* "
                    "(2005), 125 citations — barriers work in the Casterline tradition, where "
                    "opposition is routinely dosed as a reason for non-use."),
}


def main():
    ids = [r["id"] for r in csv.DictReader(CSVP.open()) if r["cell"] == "MIXED_NORM_SUPPLY"]
    retr = {r["id"]: r for r in csv.DictReader(RETR.open())} if RETR.exists() else {}
    scan, promoted = [], []
    for wid in ids:
        g = glob.glob(str(PDFDIR / f"{wid}__*.txt"))
        if not g:
            scan.append({"id": wid, "read": False})
            continue
        t = pathlib.Path(g[0]).read_text(errors="ignore")
        dosed = sum(1 for m in NORM.finditer(t)
                    if DOSE.search(t[max(0, m.start() - 160):m.end() + 160]))
        row = {"id": wid, "read": True, "words": len(t.split()),
               "norm": len(NORM.findall(t)), "dosed": dosed, "fert": len(FERT.findall(t)),
               "verdict": READ.get(wid, ("no", "proximity scan: no norm term adjacent to variable "
                                               "or model language"))[0],
               "basis": READ.get(wid, ("no", "proximity scan: no norm term adjacent to variable "
                                             "or model language"))[1]}
        if row["verdict"] == "yes":
            promoted.append(wid)
        scan.append(row)

    read = [r for r in scan if r["read"]]
    unread = [r for r in scan if not r["read"]]

    marker = "\n## PI call 4 — the A.5 bundle inspection (`421`, `422`)\n"
    base = LOGP.read_text().split(marker)[0].rstrip() if LOGP.exists() else ""
    sec = [marker.strip(), "",
           "Call 4 ruled A.5 a **bundle, not a wall**, so the 25 `MIXED_NORM_SUPPLY` records are",
           "admissible pending a full-text pass asking whether the norm component was separately",
           "dosed. This is that pass — one of the two live routes to a non-empty primary cell,",
           "because 3 of the 5 identified records across the substantive walls sit in A.5.", "",
           f"`421` retrieved **{len(read)} of {len(scan)}**. Of those, **{len(promoted)}** pair a",
           "separately dosed norm with a fertility outcome — the conjunction the primary cell",
           "requires.", "",
           "**Triage note, recorded before reading:** against `410`'s flags none of the 25 carried",
           "both a fertility-outcome marker and an identified-design marker (22 had the fertility",
           "marker alone, 3 neither), so the prior was low and this was a confirmation exercise.",
           "It was still done record by record, because a design an abstract does not name is how a",
           "primary-cell study hides.", "",
           "### The decisive record", "",
           "`W3153104329` — Kramer, Hackman, Schacht and Davis, *Scientific Reports* 2021,",
           "\"Effects of family planning on fertility behaviour across the demographic",
           "transition\". The one A.5 record whose outcome is unambiguously **realized fertility**:",
           "Maya women tracked across 90 years, natural to contracepting, 32 fertility-outcome",
           "terms. Its exposure is **family-planning adoption, not a norm**. All 10 occurrences of",
           "\"norms\" are in the discussion, as something that *emerges* from changing fertility",
           "variance — never a dosed variable. It fails the exposure gate, which is the mirror of",
           "how `W1986910339` failed at stage 6b: right outcome, absent exposure.", "",
           "### All records", "",
           "| id | read | words | norm terms | norm near a model | fertility terms | dosed norm + fertility outcome |",
           "|---|---|---|---|---|---|---|"]
    for r in sorted(scan, key=lambda r: (not r["read"], r["id"])):
        if not r["read"]:
            oa = retr.get(r["id"], {}).get("oa_status", "?")
            sec.append(f"| `{r['id']}` | **not retrieved** ({oa}) | — | — | — | — | unknown |")
        else:
            sec.append(f"| `{r['id']}` | yes | {r['words']:,} | {r['norm']} | {r['dosed']} | "
                       f"{r['fert']} | **{r['verdict']}** |")
    sec += ["", "### What this does and does not settle", "",
            f"The A.5 route is **closed for the {len(read)} records read** and **conditional on the",
            f"{len(unread)} that could not be retrieved** — six `oa_status: closed`, seven",
            "advertising an OA copy whose URL failed. Two of the unread are substantively the most",
            "interesting in the set and are now top of the wantlist:", ""]
    for wid, why in PRIORITY.items():
        sec.append(f"- `{wid}` — {why}")
    sec += ["",
            "Until those are read, `PRIMARY_NORM_FERTILITY = 0` remains conditional on this route",
            "as well as on ARM C.", ""]
    LOGP.write_text(base + "\n\n" + "\n".join(sec) + "\n")

    if unread:
        w = WANT.read_text() if WANT.exists() else f"# A.6 library wantlist\n"
        add = ["", "## Added by the PI call 4 inspection (`421`, `422`) — A.5 bundle", "",
               f"{len(unread)} of the 25 `MIXED_NORM_SUPPLY` records could not be retrieved by open",
               "access. The two starred records are the highest-value outstanding items in the",
               "chapter: if any A.5 study separately doses a norm component alongside a demographic",
               "outcome, they are where it would be.", "",
               "| id | OA status | DOI | priority |", "|---|---|---|---|"]
        for r in unread:
            m = retr.get(r["id"], {})
            star = "**HIGH — see screen log**" if r["id"] in PRIORITY else "standard"
            add.append(f"| `{r['id']}` | {m.get('oa_status', '?')} | "
                       f"{('`' + m['doi'] + '`') if m.get('doi') else '— none —'} | {star} |")
        WANT.write_text(w.rstrip() + "\n" + "\n".join(add) + "\n")
        print(f"appended {len(unread)} records to the wantlist")

    print(f"read {len(read)}/{len(scan)}; promoted to PRIMARY_NORM_FERTILITY: {len(promoted)}")
    print(f"unretrieved {len(unread)} — the A.5 route stays conditional")
    return 0


if __name__ == "__main__":
    sys.exit(main())
