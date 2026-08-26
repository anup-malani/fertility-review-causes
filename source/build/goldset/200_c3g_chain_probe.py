#!/usr/bin/env python3
"""
200_c3g_chain_probe.py — C.3.g follow-up probe. Four questions the recon (199_) raised and could
not answer, each of which changes the scope document rather than merely decorating it.

  Q1. IS THERE ANY POLICY-VARIATION FERTILITY STUDY? 199_ found the identified body (210 records)
      and the fertility body (107) barely intersect (n=2, neither a real estimate). Before the
      chapter concedes that its primary cell is unidentified, the cleanest possible design —
      forgiveness, cancellation, a repayment reform, a tuition-regime change — is searched for
      by name rather than by vocabulary block.

  Q2. HOW THICK IS LINK 1 OF THE CHAIN, really? v5's claim names marriage and homeownership as the
      mechanism, so debt -> household formation is IN scope by the claim's own words. The recon
      counted 5 and 11 identified records on those outcomes; this probe reads the heads to see
      whether they are genuine quasi-experiments or the same three papers indexed repeatedly.

  Q3. WHOSE BALANCE SHEET — the third case. 199_ established that parents saving for a child's
      tuition (C.2.b) barely overlaps C.3.g's vocabulary (n=2). It also surfaced a third holder the
      scope had not enumerated: PARENTS who themselves borrow for a child's education (Parent PLUS).
      That debt sits on the older generation's balance sheet and cannot delay their childbearing.
      Sized here so the wall can be written with a number.

  Q4. THE APOSTROPHE. `title.search` returned ZERO for "Can't afford a baby ..." while the
      author-retry found it immediately at 93 cites. If a punctuation mark in a title query silently
      returns an empty literature, that is a shared-resolver defect, not a C.3.g one, and it belongs
      in the workflow. The probe isolates it: same title, three spellings.

Same discipline as 199_: curl transport, funded key, errors bucketed separately from zero-hits,
syntax guard before any request is spent.

Output: literature/search-logs/student-debt-household-formation-chain-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-chain-probe.md")
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

DEBT = ('("student debt" OR "student loan" OR "student loans" OR "student loan debt" OR '
        '"educational debt" OR "education debt" OR "college debt" OR "student borrowing" OR '
        '"student borrowers" OR "education loans")')
FERT = ('("fertility" OR "childbearing" OR "first birth" OR "birth rates" OR "childlessness" OR '
        '"number of children" OR "transition to parenthood" OR "family size" OR "having children")')

GROUPS = [
    ("Q1 — does any POLICY-VARIATION fertility study exist", [
        ("loan forgiveness or cancellation AND a fertility outcome",
         f'title_and_abstract.search:("loan forgiveness" OR "debt cancellation" OR "debt relief" OR "loan discharge") AND {DEBT} AND {FERT}'),
        ("repayment-plan reform AND a fertility outcome",
         f'title_and_abstract.search:("income-driven repayment" OR "income contingent loan" OR "repayment plan" OR "loan limits") AND {DEBT} AND {FERT}'),
        ("tuition-regime change AND a fertility outcome",
         f'title_and_abstract.search:("tuition increase" OR "tuition-free" OR "free college" OR "state appropriations" OR "tuition deregulation") AND {FERT}'),
        ("student debt AND births as an aggregate outcome",
         f'title_and_abstract.search:{DEBT} AND ("birth rate" OR "total fertility rate" OR "births per woman" OR "aggregate fertility")'),
        ("student loan AND fertility AND a panel or cohort design",
         f'title_and_abstract.search:{DEBT} AND {FERT} AND ("fixed effects" OR "panel data" OR "hazard model" OR "event history" OR "discrete-time")'),
    ]),
    ("Q2 — link 1 of the chain: debt to household formation", [
        ("student debt AND marriage — the identified heads read directly",
         f'title_and_abstract.search:{DEBT} AND ("delay marriage" OR "marriage timing" OR "transition to marriage" OR "marriage formation" OR "likelihood of marriage")'),
        ("student debt AND homeownership — the identified heads read directly",
         f'title_and_abstract.search:{DEBT} AND ("homeownership rate" OR "home purchase" OR "first-time homebuyer" OR "housing tenure" OR "mortgage origination")'),
        ("student debt AND leaving the parental home — the A.23 boundary",
         f'title_and_abstract.search:{DEBT} AND ("living with parents" OR "parental home" OR "boomerang" OR "residential independence" OR "leaving home")'),
        ("student debt AND credit-panel administrative exposure",
         f'title_and_abstract.search:{DEBT} AND ("credit report" OR "credit bureau" OR "administrative data" OR "linked administrative")'),
    ]),
    ("Q3 — whose balance sheet: the third holder", [
        ("PARENT-held education debt for a child's schooling",
         f'title_and_abstract.search:("Parent PLUS" OR "parent borrowers" OR "parental student loans" OR "borrowing for a child") AND ("education" OR "college")'),
        ("parent-held education debt AND a fertility outcome",
         f'title_and_abstract.search:("Parent PLUS" OR "parent borrowers" OR "parental student loans" OR "borrowing for a child") AND {FERT}'),
    ]),
]

# Q4 — the apostrophe test. One work, three spellings, sent to title.search.
APOSTROPHE = [
    ("straight apostrophe", "Can't afford a baby"),
    ("curly apostrophe", "Can’t afford a baby"),
    ("apostrophe removed", "Cant afford a baby"),
    ("word dropped entirely", "afford a baby debt and young Americans"),
    ("subtitle half only", "Debt and young Americans"),
]

errors, results, apos_results = [], [], []

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
                        venue=(loc.get("display_name") or "")))
    return out

SELECT = "id,doi,display_name,publication_year,cited_by_count,type,primary_location"

def guard_syntax():
    bad = []
    for group, probes in GROUPS:
        for label, filt in probes:
            if "?" in filt:
                bad.append((label, "contains '?' — parsed as a wildcard"))
            if "," in filt:
                bad.append((label, "comma inside a filter value"))
            for phrase in filt.split('"')[1::2]:
                first = phrase.strip().split(" ")[0].lower()
                if first in ("not", "and", "or"):
                    bad.append((label, f"phrase opens with boolean '{first}'"))
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
    for group, probes in GROUPS:
        for label, filt in probes:
            n_req += 1
            url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20").replace('"', "%22") +
                   f"&per-page=8&select={SELECT}&sort=cited_by_count:desc&api_key={KEY}")
            d = oa(url)
            if "results" not in d:
                errors.append((label, str(d.get("__err") or d)[:160]))
            else:
                results.append((group, label, filt, d["meta"]["count"], rows_of(d)))
            time.sleep(0.2)

    for label, title in APOSTROPHE:
        n_req += 1
        enc = (title.replace(" ", "%20").replace("'", "%27").replace("’", "%E2%80%99"))
        url = ("https://api.openalex.org/works?filter=title.search:" + enc +
               f"&per-page=3&select={SELECT}&api_key={KEY}")
        d = oa(url)
        if "results" not in d:
            errors.append((label, str(d.get("__err") or d)[:160]))
        else:
            apos_results.append((label, title, d["meta"]["count"], rows_of(d)))
        time.sleep(0.2)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        sys.stderr.write(f"ABORT: {len(errors)}/{n_req} failed ({share:.0%}); not writing.\n")
        sys.exit(1)

    L = [f"# Chain and boundary probe — {SLUG}\n",
         "**Hypothesis:** C.3.g (HYPOTHESES-v5.md) · **Ticket:** TICK-073\n\n",
         "**Generated by:** `source/build/goldset/200_c3g_chain_probe.py`\n\n",
         f"**Requests:** {n_req} · **Failed:** {len(errors)} ({share:.1%})\n\n",
         "Follow-up to `199_c3g_recon_probe.py`. Failed requests are bucketed separately from "
         "zero-hits, so every zero below is an absence.\n"]

    for group in [g for g, _ in GROUPS]:
        L.append(f"\n## {group}\n")
        for g, label, filt, count, rows in results:
            if g != group:
                continue
            L.append(f"\n### {label} — **n = {count:,}**\n\n`{filt}`\n\n")
            if not rows:
                L.append("*(no records)*\n")
                continue
            L.append("| Cites | Year | Title | Venue |\n|---|---|---|---|\n")
            for r in rows:
                L.append(f"| {r['cites']:,} | {r['year']} | {r['title'][:95].replace('|','/')} | "
                         f"{r['venue'][:42].replace('|','/')} |\n")

    L.append("\n## Q4 — the apostrophe test on `title.search`\n\n")
    L.append("One work — Nau, Dwyer and Hodson (2015), 93 cites, resolved instantly by "
             "`raw_author_name.search` — queried five ways.\n\n")
    L.append("| Spelling sent | Query | n | Top match |\n|---|---|---|---|\n")
    for label, title, count, rows in apos_results:
        top = rows[0]["title"][:60].replace("|", "/") if rows else "**— no match —**"
        L.append(f"| {label} | `{title}` | {count} | {top} |\n")

    if errors:
        L.append("\n## Failed requests (excluded from every count above)\n\n")
        for lbl, e in errors:
            L.append(f"- `{lbl}` — {e}\n")

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    open(OUT_MD, "w").write("".join(L))
    print(f"wrote {OUT_MD}  ({n_req} requests, {len(errors)} failed)")

if __name__ == "__main__":
    main()
