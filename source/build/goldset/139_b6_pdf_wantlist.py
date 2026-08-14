#!/usr/bin/env python3
"""
139_b6_pdf_wantlist.py — B.6, stage 5 prep. Build the retrieval wantlist and measure the OA ceiling.

Inherits `129_b7_pdf_wantlist.py`. Checks open-access status LIVE before writing, so the list states
what an automated fetch can reach and what needs a human with a library proxy BEFORE the fetch rather
than after. B.1 found that distinction the expensive way — its automated ceiling hit 20 of 95 and its
pooled estimate has rested on five studies since.

FOUR retrieval jobs. B.7 had three; B.6 needs a fourth because its evidence depth is not where B.7's
was.

  JOB A  — the primary cells (a fertility quantity). The only records that earn causal GRADE credit.
  JOB A2 — the fertility-INPUT cells (semen and ovarian parameters). NEW for B.6. These are not
           fertility quantities and do not earn causal credit, but they are where this chapter's
           measured biology actually lives: 69 records against 30 in the primary cells, and the
           PFAS/microplastics asymmetry is far starker here (62 vs 7) than in the primary row.
           Treating them as an afterthought, as B.7's structure would, would mis-describe the
           chapter's evidence base.
  JOB B  — the held records. Full text is needed to settle ONE routing question each: mixture
           separability (Wall 1) or species/scope (Wall 5). Not to extract an effect.
  JOB C  — parameter, pharmacokinetic and measurement support. No GRADE credit, but the
           demographic-significance computation and the Call 2 reverse-causation correction rest
           entirely on them. Selected by rule from the screen notes rather than hand-listed, so the
           selection is reproducible; each line names the model input it supplies.

**The OA rate is the number to read first.** D.3.b's ticket flagged it as what decides whether a
chapter avoids B.1's selection problem, and the concern is sharper here: if OA status correlates with
the exposure family — plausible, since the microplastics literature is newer and more often
gold-OA — then an OA-only evidence base would systematically over-represent one half of a chapter
whose whole design is a comparison between the halves. The report breaks the rate down by family for
that reason.

Target paths follow the house convention, `literature/pdfs/{slug}/{WID}__{title-slug}.pdf`, so a file
dropped there is picked up by ingest without renaming. That directory is gitignored.

Output: literature/search-logs/{slug}-pdf-wantlist.md
        extraction/{slug}-retrieval-dois.txt
        extraction/{slug}-oa-status.json
"""
import csv, json, os, re, subprocess, time
from collections import Counter

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")
TIERS = os.path.join(LOGS, f"{SLUG}-screen-tiers.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-pdf-wantlist.md")
OUT_DOI = os.path.join(EXTRACT, f"{SLUG}-retrieval-dois.txt")
OUT_OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")

PRIMARY_CELLS = {"PRIMARY_EXPOSURE_TO_FERTILITY", "PRIMARY_MALE_FECUNDITY", "PRIMARY_HIGH_EXPOSURE"}
INPUT_CELLS = {"SEMEN_PARAMETER", "OVARIAN_PARAMETER"}
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}

# JOB C selection rules. Keyed on the screen note, which already states why each record matters, so
# the set is derived rather than asserted and re-runs identically if the screen is revised.
# Prefix legend used in the report: `x` exposure series, `k` pharmacokinetics/excretion,
# `r` reverse causation, `m` measurement and design, `t` outcome-trend context.
JOB_C_RULES = [
    ("r", "REVERSE", None),
    ("k", "PARAMETER_PHARMACOKINETIC",
     ("excretion", "parity", "half-life", "half-lives", "lactational", "transplacental",
      "breastfeeding", "elimination", "accumulation differences", "postpartum", "pregnancy")),
    ("x", "PARAMETER_EXPOSURE",
     ("trend", "series", "phase-out", "declining", "nhanes", "1972", "1982", "1999",
      "current-use", "c8", "ronneby", "veneto", "firefighter", "intervention")),
    ("m", "MEASUREMENT_METHOD", None),
    ("t", "OUTCOME_TREND_UNATTRIBUTED",
     ("fecundity", "dissent", "misread", "data gaps", "declining human", "crisis")),
]


def oa_status(doi):
    """Live OA check via OpenAlex. Returns (status, best_pdf_url_or_None, host)."""
    url = ("https://api.openalex.org/works/https://doi.org/" + doi +
           "?select=id,open_access,best_oa_location&mailto=" + MAILTO)
    try:
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
    except Exception:
        return "UNCONFIRMED", None, ""      # a failed request is never a "closed" answer
    if "open_access" not in d:
        return "UNCONFIRMED", None, ""
    oa = d.get("open_access") or {}
    loc = d.get("best_oa_location") or {}
    src = (loc.get("source") or {}) if loc else {}
    return (oa.get("oa_status") or "closed"), loc.get("pdf_url"), (src.get("display_name") or "")


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def main():
    gate = list(csv.DictReader(open(GATE)))
    tiers = json.load(open(TIERS))
    by_id = {r["id"]: r for t in tiers.values() for r in t}

    job_a = [r for r in gate if r["cell"] in PRIMARY_CELLS]
    job_a2 = [r for r in gate if r["cell"] in INPUT_CELLS]
    job_b = [r for r in gate if r["cell"] not in PRIMARY_CELLS and r["cell"] not in INPUT_CELLS]

    # JOB C, derived from the screen notes.
    job_c, seen_c = [], set()
    for prefix, cell, keys in JOB_C_RULES:
        for r in by_id.values():
            if r["cell"] != cell or r["tier"] == 0 or r["id"] in seen_c:
                continue
            note = (r.get("screen_note") or "").lower()
            if keys is None or any(k in note for k in keys):
                seen_c.add(r["id"])
                job_c.append((prefix, r))

    status = {}
    for r in job_a + job_a2 + job_b:
        if r["doi"]:
            status[r["openalex_id"]] = oa_status(r["doi"])
            time.sleep(0.15)
    for _, rec in job_c:
        if rec.get("doi") and rec["id"] not in status:
            status[rec["id"]] = oa_status(rec["doi"])
            time.sleep(0.15)

    def st_of(i):
        return status.get(i, ("unchecked", None, ""))[0]

    def is_open(i):
        return st_of(i) in OPEN

    dois = [r["doi"] for r in job_a + job_a2 + job_b if r["doi"]]
    dois += [rec["doi"] for _, rec in job_c if rec.get("doi")]
    open(OUT_DOI, "w").write("\n".join(dict.fromkeys(dois)) + "\n")
    json.dump({k: {"oa_status": v[0], "pdf_url": v[1], "host": v[2]} for k, v in status.items()},
              open(OUT_OA, "w"), indent=2)

    def rate(rows, idkey="openalex_id"):
        n = len(rows)
        o = sum(1 for r in rows if is_open(r[idkey] if idkey in r else r["id"]))
        return o, n, (o / n if n else 0.0)

    a_o, a_n, a_r = rate(job_a)
    a2_o, a2_n, a2_r = rate(job_a2)
    b_o, b_n, b_r = rate(job_b)
    c_o, c_n, c_r = rate([rec for _, rec in job_c], idkey="id")
    n_unconf = sum(1 for i in status if st_of(i) == "UNCONFIRMED")

    # OA rate by chemical family, over the causal evidence base (A + A2). This is the selection test.
    fam = {}
    for r in job_a + job_a2:
        f = r["screen_family"] or "unstated"
        d = fam.setdefault(f, [0, 0])
        d[1] += 1
        if is_open(r["openalex_id"]):
            d[0] += 1

    def row_line(wid, doi, year, title, venue, extra=""):
        st, pdf, host = status.get(wid, ("unchecked", None, ""))
        mark = {"closed": "**CLOSED**", "UNCONFIRMED": "*unconfirmed*"}.get(st, f"open ({st})")
        tgt = f"literature/pdfs/{SLUG}/{wid}__{slugify(title)}.pdf"
        return (f"- **{title[:88]}** ({year}, *{(venue or '')[:38]}*)  \n"
                f"  `{doi or 'NO DOI'}` · {mark}{' · ' + host[:34] if host else ''}"
                f"{' · ' + extra if extra else ''}  \n  → `{tgt}`")

    L = [f"# Retrieval wantlist — {SLUG} (B.6)", "",
         "Generated by `source/build/goldset/139_b6_pdf_wantlist.py`. Open-access status is checked "
         "live, so this list states the automated ceiling **before** the fetch. B.1's automated "
         "retrieval stopped at 20 of 95 and its pooled estimate has rested on five studies since.", "",
         f"**Job A — primary cells (a fertility quantity): {a_n} records, {a_o} open ({a_r:.0%}).**  \n"
         f"**Job A2 — fertility-input cells (semen, ovarian): {a2_n} records, {a2_o} open ({a2_r:.0%}).**  \n"
         f"**Job B — held for a routing question: {b_n} records, {b_o} open ({b_r:.0%}).**  \n"
         f"**Job C — parameter, pharmacokinetic and measurement support: {c_n} records, {c_o} open "
         f"({c_r:.0%}).**", "",
         f"{n_unconf} OA checks did not complete and are marked *unconfirmed*. An unconfirmed check "
         "is not a closed record; the two are kept apart for the same reason the reconnaissance pass "
         "kept failed requests out of its zero counts.", "",
         "## The selection test — OA rate by chemical family", "",
         "This chapter is a comparison between its two halves, so a retrieval process that reaches "
         "one half more completely than the other would bias the comparison itself, not merely the "
         "level. The microplastics literature is newer and more often gold-OA, which is exactly the "
         "condition for that bias. Over the causal evidence base (Jobs A and A2):", "",
         "| family | open | total | rate |", "|---|---|---|---|"]
    for f in ("pfas", "plastic", "both", "unclear", "none", "unstated"):
        if f in fam:
            o, n = fam[f]
            L.append(f"| `{f}` | {o} | {n} | {o / n:.0%} |")
    L += ["",
          "**Read this before reading any effect size.** If the rates differ materially, the "
          "difference is an argument for the library sub-ticket rather than for proceeding on what "
          "the automated fetch happens to reach.", "",
          "## Job A — the primary cells", "",
          "These are the only records that earn causal GRADE credit. Ordered with the records the "
          "screen flagged as important first, then by citation weight.", ""]

    order_a = sorted(job_a, key=lambda r: (0 if "IMPORTANT" in (r["screen_note"] or "") else 1,
                                           r["cell"], -(int(r["cited_by"] or 0))))
    for r in order_a:
        L.append(row_line(r["openalex_id"], r["doi"], r["year"], r["title"], r["venue"],
                          f"`{r['cell']}` · {r['screen_family']}"))
        if r["screen_note"]:
            L.append(f"  *{r['screen_note'][:200]}*")

    L += ["", "## Job A2 — the fertility-input cells", "",
          "Semen and ovarian parameters. Not fertility quantities, and they earn no causal credit — "
          "but this is where the chapter's measured biology is, and the family asymmetry here "
          "(62 PFAS to 7 microplastics) is the sharpest quantitative statement of the Call 1 split. "
          "A semen-parameter decrement becomes a fertility statement only through the translation "
          "parameters in Job C, and the chapter must not elide that step.", ""]
    for r in sorted(job_a2, key=lambda r: (r["screen_family"], -(int(r["cited_by"] or 0)))):
        L.append(row_line(r["openalex_id"], r["doi"], r["year"], r["title"], r["venue"],
                          f"`{r['cell']}` · {r['screen_family']}"))

    L += ["", "## Job B — held records, one routing question each", "",
          "Full text is needed here to answer a single question, not to extract an effect: whether a "
          "mixture index is separable into compound-specific estimates (Wall 1), or what species and "
          "scope a review actually covers (Wall 5). Both are settled by a methods section in a line "
          "or two, so these are cheap retrievals with high routing value.", ""]
    for r in sorted(job_b, key=lambda r: (r["cell"], -(int(r["cited_by"] or 0)))):
        L.append(row_line(r["openalex_id"], r["doi"], r["year"], r["title"], r["venue"],
                          f"`{r['cell']}`"))

    L += ["", "## Job C — parameter, pharmacokinetic and measurement support", "",
          "Selected by rule from the screen notes. Prefixes: `r` reverse causation (the Call 2 "
          "correction), `k` pharmacokinetics and excretion, `x` the exposure series the "
          "demographic-significance computation multiplies, `m` measurement and design, `t` "
          "outcome-trend context.", ""]
    for prefix, rec in sorted(job_c, key=lambda p: (p[0], -(rec_c := p[1])["cited_by_count"] or 0)):
        L.append(row_line(rec["id"], rec.get("doi"), rec.get("year"), rec["title"],
                          rec.get("venue", ""), f"`{prefix}` · `{rec['cell']}`"))
        if rec.get("screen_note"):
            L.append(f"  *{rec['screen_note'][:180]}*")

    L += ["", "## What retrieval cannot fix", "",
          "Retrieval decides how precisely each record can be characterised. It does not change three "
          "facts the screen established over 920 records:", "",
          "1. **No study in the frame estimates either exposure against a population fertility "
          "quantity with a design that identifies it.** Every primary-cell record is a "
          "cross-sectional or prospective cohort association on serum or tissue concentration.",
          "2. **`PRIMARY_HIGH_EXPOSURE` is empty.** The contaminated-community and occupational "
          "cohorts — Ronneby, Veneto, C8, firefighters — carry the only exogenous exposure variation "
          "in this literature and have been studied for cancer, thyroid, lipids, immune function and "
          "birth outcomes, but never for a fertility outcome. Retrieving every PDF on this list will "
          "not produce the study that does not exist.",
          "3. **The reverse-causation problem is a design problem, not a reporting problem.** Whether "
          "an estimate handles parity is a fact about how the study was built. Full text tells us "
          "which studies did; it cannot make the others usable."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"job_a={a_n} (open {a_o}, {a_r:.0%}) job_a2={a2_n} (open {a2_o}, {a2_r:.0%}) "
          f"job_b={b_n} (open {b_o}, {b_r:.0%}) job_c={c_n} (open {c_o}, {c_r:.0%})")
    print("by family (A+A2):", {f: f"{o}/{n}" for f, (o, n) in sorted(fam.items())})
    print(f"unconfirmed={n_unconf} total_dois={len(set(dois))}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
