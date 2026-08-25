#!/usr/bin/env python3
"""
186_a17_strict_anchor_probe.py — A.17, second-stage anchor tightening.

`185_` measured the clinical decoy cloud twice, plain and "anchored", per the A.24 homonym rule.
The gap came out 33,196 vs 10,765 — a 3x narrowing, which looks like the rule working. It is not
working yet. The "anchored" vocabulary still contains **"birth rates"**, **"childbearing"** and
**"number of children"**, and the first of those is a homonym one level below the one the rule was
written for: in the ART clinical literature **"live birth rate" is the per-cycle success measure**,
so `"birth rates"` matches the decoy's core outcome term rather than a population quantity. The
anchored diagnostic was still scoring the collision.

This script re-measures with a STRICT vocabulary in which every term is a population-level
demographic quantity that a per-cycle clinical paper has no occasion to use, and reports the three
rates side by side (plain / anchored / strict). It also sizes the actual search frame under the
strict vocabulary, which is what the scope document needs and what 185's loose counts overstate.

The A.24 lesson said to report the plain and anchored rates side by side because the gap is itself
the finding. The generalisation this run adds: **check the anchored vocabulary for a homonym of its
own before trusting the gap.** One contaminated term in an OR block re-admits the whole cloud.

Also fixes the one failed request in 185: `Präg` was sent to the URL as raw UTF-8 and curl returned
an unparseable body. Non-ASCII author names are percent-encoded here. The failure bucketed correctly
as an ERROR rather than a zero, which is the only reason it is visible at all.

Output: literature/search-logs/art-access-fertility-recovery-strict-anchor.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "art-access-fertility-recovery"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-strict-anchor.md")
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

ART = '("assisted reproductive technology" OR "assisted reproduction" OR "in vitro fertilization" OR "in vitro fertilisation" OR "IVF" OR "ICSI" OR "intracytoplasmic sperm injection" OR "fertility treatment" OR "infertility treatment")'
ACCESS = '("insurance mandate" OR "insurance coverage" OR "mandated coverage" OR "reimbursement" OR "public funding" OR "subsidy" OR "subsidised" OR "subsidized" OR "out-of-pocket" OR "access to treatment" OR "eligibility" OR "affordability" OR "cost sharing")'
CLINICAL = '("live birth rate per cycle" OR "clinical pregnancy rate" OR "implantation rate" OR "ovarian stimulation" OR "embryo culture" OR "blastocyst" OR "luteal phase" OR "gonadotropin" OR "oocyte retrieval" OR "cumulative live birth rate")'

# The three outcome vocabularies, in increasing strictness.
PLAIN = '("fertility" OR "birth rate" OR "births")'
ANCHORED = '("total fertility rate" OR "completed fertility" OR "cohort fertility" OR "birth rates" OR "crude birth rate" OR "childbearing" OR "parity transition" OR "number of children" OR "population level fertility")'
# STRICT: every term denotes a POPULATION quantity. Dropped from ANCHORED and why:
#   "birth rates"        -> matches "live birth rate(s)", the clinical success measure. Fatal.
#   "childbearing"       -> "delayed childbearing", "childbearing age" are clinical-cohort framing.
#   "number of children" -> appears in patient-history and desired-family-size instruments.
STRICT = '("total fertility rate" OR "completed fertility" OR "cohort fertility" OR "crude birth rate" OR "parity transition" OR "period fertility" OR "fertility decline" OR "demographic transition" OR "population fertility")'

PROBES = [
    # --- the three-way homonym diagnostic on the clinical decoy cloud ---
    ("Clinical cloud, unrestricted", f'title_and_abstract.search:{CLINICAL}'),
    ("Clinical cloud x PLAIN vocabulary", f'title_and_abstract.search:{CLINICAL} AND {PLAIN}'),
    ("Clinical cloud x ANCHORED vocabulary (185's version)", f'title_and_abstract.search:{CLINICAL} AND {ANCHORED}'),
    ("Clinical cloud x STRICT vocabulary", f'title_and_abstract.search:{CLINICAL} AND {STRICT}'),
    # --- which single term re-admits the cloud: one probe per suspect ---
    ("Clinical cloud x 'birth rates' alone", f'title_and_abstract.search:{CLINICAL} AND ("birth rates")'),
    ("Clinical cloud x 'childbearing' alone", f'title_and_abstract.search:{CLINICAL} AND ("childbearing")'),
    ("Clinical cloud x 'number of children' alone", f'title_and_abstract.search:{CLINICAL} AND ("number of children")'),
    ("Clinical cloud x 'total fertility rate' alone", f'title_and_abstract.search:{CLINICAL} AND ("total fertility rate")'),
    # --- frame sizing under the strict vocabulary ---
    ("FRAME: ART x STRICT — the whole population-relevant ART body", f'title_and_abstract.search:{ART} AND {STRICT}'),
    ("FRAME: ART x ACCESS x STRICT — the primary cell, strictly drawn", f'title_and_abstract.search:{ART} AND {ACCESS} AND {STRICT}'),
    ("FRAME: ART x ACCESS x ANCHORED — 185's version of the same cell", f'title_and_abstract.search:{ART} AND {ACCESS} AND {ANCHORED}'),
    ("FRAME: ART x ACCESS, no outcome restriction at all", f'title_and_abstract.search:{ART} AND {ACCESS}'),
    # --- the accounting stream, strictly drawn ---
    ("Accounting stream: ART x contribution-language x STRICT",
     f'title_and_abstract.search:{ART} AND ("contribution to" OR "contribution of" OR "share of births" OR "proportion of births" OR "accounted for") AND {STRICT}'),
    # --- does the strict vocabulary keep the known primary-cell studies? recall check ---
    ("RECALL: strict frame x insurance-mandate language",
     f'title_and_abstract.search:{ART} AND ("insurance mandate" OR "mandated coverage" OR "state mandate") AND {STRICT}'),
]

# Named works that MUST survive the strict frame, or the frame is too tight. Checked by DOI-free
# title match, then reported with whether the strict frame would have retrieved them.
RECALL_TITLES = [
    "Can assisted reproduction technology compensate for the natural decline in fertility with age",
    "The Contribution of Assisted Reproduction to Completed Fertility",
    "The contribution of assisted reproductive technology to fertility rates and parity transition",
    "Health disparities and infertility impacts of state-level insurance mandates",
    "THE EFFECTS OF INSURANCE MANDATES ON CHOICES AND OUTCOMES IN INFERTILITY TREATMENT MARKETS",
    "Coverage of infertility treatment and fertility outcomes",
    "Infertility Insurance Mandates and Fertility",
    "Realizing a desired family size when should couples start",
]

# The 185 failure, re-run with percent-encoding.
RETRY_NONASCII = [("Präg", "assisted reproduction"), ("Sobotka", "completed fertility")]

errors, results, recall, retry = [], [], [], []
SELECT = "id,doi,display_name,publication_year,cited_by_count,type,primary_location"


def oa(url):
    try:
        r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
        if r.returncode != 0:
            return {"__err": f"curl exit {r.returncode}"}
        return json.loads(r.stdout)
    except Exception as e:
        return {"__err": str(e)[:140]}


def enc(s):
    """Percent-encode a filter value. Keeps OpenAlex's boolean punctuation intact, encodes
    everything else — including non-ASCII, which is what broke Präg in 185."""
    return urllib.parse.quote(s, safe='():"|+-')


def count_of(filt):
    url = (f"https://api.openalex.org/works?filter={enc(filt)}&per-page=5&select={SELECT}"
           f"&sort=cited_by_count:desc&api_key={KEY}")
    return oa(url)


def guard_syntax():
    bad = []
    for label, filt in PROBES:
        if "?" in filt:
            bad.append((label, "contains '?' — wildcard"))
        if "," in filt:
            bad.append((label, "comma inside a filter value"))
        for phrase in filt.split('"')[1::2]:
            if phrase.strip().split(" ")[0].lower() in ("not", "and", "or"):
                bad.append((label, f'phrase opens with a boolean: "{phrase}"'))
    if bad:
        sys.stderr.write("ABORT: query hazards found; no requests spent.\n")
        for lbl, why in bad:
            sys.stderr.write(f"  {lbl}: {why}\n")
        sys.exit(2)


def main():
    guard_syntax()
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)

    n_req = 0
    for label, filt in PROBES:
        n_req += 1
        d = count_of(filt)
        if "results" not in d:
            errors.append((label, str(d.get("__err") or d)[:160]))
        else:
            results.append((label, filt, d["meta"]["count"]))
        time.sleep(0.2)

    for t in RECALL_TITLES:
        n_req += 1
        url = (f"https://api.openalex.org/works?filter=title.search:{enc(t)}"
               f"&per-page=3&select={SELECT}&api_key={KEY}")
        d = oa(url)
        if "results" not in d:
            errors.append((t[:40], str(d.get("__err") or d)[:160]))
            continue
        rows = d.get("results", [])
        if not rows:
            recall.append((t, None, None, None))
            continue
        w = rows[0]
        wid = (w.get("id") or "").rsplit("/", 1)[-1]
        n_req += 1
        # Does the strict frame actually contain this work? Ask directly, by id.
        f2 = (f'title_and_abstract.search:{ART} AND {STRICT}')
        u2 = (f"https://api.openalex.org/works?filter={enc(f2)},openalex_id:{wid}"
              f"&per-page=1&select=id&api_key={KEY}")
        d2 = oa(u2)
        inframe = None if "results" not in d2 else (d2["meta"]["count"] > 0)
        recall.append((w.get("display_name"), w.get("publication_year"), w.get("cited_by_count"), inframe))
        time.sleep(0.2)

    for surname, term in RETRY_NONASCII:
        n_req += 1
        filt = f"raw_author_name.search:{surname},title_and_abstract.search:{term}"
        url = (f"https://api.openalex.org/works?filter={enc(filt)}&per-page=3&select={SELECT}"
               f"&sort=cited_by_count:desc&api_key={KEY}")
        d = oa(url)
        if "results" not in d:
            errors.append((f"{surname} + {term}", str(d.get("__err") or d)[:160]))
        else:
            rows = d.get("results", [])
            top = rows[0]["display_name"] if rows else "— no match —"
            retry.append((f"{surname} + {term}", d["meta"]["count"], top))
        time.sleep(0.2)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        sys.stderr.write(f"ABORT: {len(errors)}/{n_req} failed ({share:.0%}); not writing.\n")
        sys.exit(1)

    by = {lbl: c for lbl, _, c in results}
    L = []
    L.append(f"# Strict anchor tightening — {SLUG}\n\n")
    L.append("**Hypothesis:** A.17 · **Ticket:** TICK-072 · "
             "**Generated by:** `source/build/goldset/186_a17_strict_anchor_probe.py`\n\n")
    L.append(f"**Requests:** {n_req} · **Failed:** {len(errors)} ({share:.1%})\n\n")

    L.append("## The homonym diagnostic, run three ways\n\n")
    L.append("| Vocabulary | Records inside the clinical decoy cloud | Share of the cloud |\n|---|---|---|\n")
    cloud = by.get("Clinical cloud, unrestricted", 0)
    for lbl in ("Clinical cloud x PLAIN vocabulary",
                "Clinical cloud x ANCHORED vocabulary (185's version)",
                "Clinical cloud x STRICT vocabulary"):
        c = by.get(lbl, 0)
        L.append(f"| {lbl.split('x ')[1]} | {c:,} | {c/max(cloud,1):.1%} |\n")
    L.append(f"\nCloud size: **{cloud:,}** records.\n\n")

    L.append("## Which single term re-admits the cloud\n\n")
    L.append("| Term, alone | Records inside the cloud |\n|---|---|\n")
    for lbl in ("Clinical cloud x 'birth rates' alone", "Clinical cloud x 'childbearing' alone",
                "Clinical cloud x 'number of children' alone",
                "Clinical cloud x 'total fertility rate' alone"):
        L.append(f"| {lbl.split('x ')[1]} | {by.get(lbl,0):,} |\n")

    L.append("\n## Frame sizing\n\n")
    L.append("| Frame | n |\n|---|---|\n")
    for lbl, filt, c in results:
        if lbl.startswith("FRAME") or lbl.startswith("Accounting") or lbl.startswith("RECALL"):
            L.append(f"| {lbl} | {c:,} |\n")

    L.append("\n## Recall check — do the known primary-cell works survive the strict frame\n\n")
    L.append("| Work | Year | Cites | Inside `ART x STRICT` |\n|---|---|---|---|\n")
    for title, yr, cites, inframe in recall:
        if yr is None:
            L.append(f"| {str(title)[:70]} | — | — | **unresolved** |\n")
        else:
            mark = "yes" if inframe else ("**NO**" if inframe is False else "?")
            L.append(f"| {str(title)[:70].replace('|','/')} | {yr} | {cites:,} | {mark} |\n")

    L.append("\n## Non-ASCII retry (the one failed request in 185)\n\n")
    L.append("| Author + term | n | Top match |\n|---|---|---|\n")
    for q, c, top in retry:
        L.append(f"| {q} | {c} | {str(top)[:70].replace('|','/')} |\n")

    L.append("\n## Full probe list\n\n")
    L.append("| Probe | n |\n|---|---|\n")
    for lbl, filt, c in results:
        L.append(f"| {lbl} | {c:,} |\n")

    if errors:
        L.append("\n## Failed requests (excluded from every count above)\n\n")
        for lbl, e in errors:
            L.append(f"- `{lbl}` — {e}\n")

    open(OUT_MD, "w").write("".join(L))
    print(f"wrote {OUT_MD}  ({n_req} requests, {len(errors)} failed)")


if __name__ == "__main__":
    main()
