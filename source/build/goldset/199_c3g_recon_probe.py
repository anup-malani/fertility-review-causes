#!/usr/bin/env python3
"""
199_c3g_recon_probe.py — C.3.g (student debt and household formation), pre-scope reconnaissance.

Runs before the scope document. Establishes from live records rather than from memory:

  (a) whether the PRIMARY estimand cell exists — a study estimating the effect of a young adult's
      OWN education debt on a FERTILITY outcome. C.3.g was opened as the smallest unstarted
      hypothesis (48 records in the exposure x outcome cell), and A.24 is the cautionary case: a
      cell that small can be small because the literature is young, or because it is empty. The
      probe distinguishes those two before the scope is written;

  (b) the EXPOSURE-ESTIMAND DISTANCE, which is this chapter's central design risk. The identified
      designs in this literature (loan-forgiveness episodes, credit-bureau panels, aid-formula
      discontinuities) mostly measure MARRIAGE and HOMEOWNERSHIP, not births. The A.24 lesson is
      that identified variation sitting on a neighbouring outcome belongs to the neighbouring
      chapter unless the chapter can carry the link explicitly. So the probe sizes the fertility
      cell and the union/housing cell SEPARATELY and asks which one the identification lives in;

  (c) whose balance sheet the debt sits on. Two literatures share the vocabulary of college costs
      and have opposite exposures: a young adult's own loan burden (C.3.g) and parents anticipating
      their children's tuition (C.2.b, cost of children). Neither wall is visible from the word
      "college costs" alone, so the split is measured;

  (d) whether the reverse direction is separable. Debt is chosen jointly with schooling, and
      schooling independently lowers fertility (C.3.d, D.2.a). A study that does not condition on
      educational attainment estimates the return to college, not the burden of its financing. The
      probe asks how much of the body carries conditioning or identification language at all;

  (e) whether an EXPOSURE SERIES exists to run demographic significance against — aggregate balances,
      the share of a cohort holding debt, average balance per borrower. C.3.g's demographic ceiling
      is (share of the cohort exposed) x (effect), and the first factor is not close to one, so an
      unsourced series would leave the significance stage with nothing to divide by;

  (f) whether any NON-US evidence exists. v5 flags the hypothesis as concentrated in Anglophone
      settings. If the body is entirely US, that is a stated external-validity bound rather than a
      discovered one.

Discipline carried from prior runs (A.17, A.12, A.24, B.5, B.6, B.7, D.2.d, D.3.b, D.3.c):
  * A failed request goes in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the report
    refuses to publish if the error share exceeds ERROR_ABORT_SHARE.
  * HTTPS goes through curl: this interpreter has no CA bundle, so urllib fails every call, and it
    fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone.
  * No search phrase opens with not/and/or; no `?` anywhere in a search value; no comma inside a
    filter value. All are checked before any request is spent.
  * Pass-2 named retries go to `raw_author_name.search` plus a title term, never to `title.search`,
    which is unsatisfiable for a surname by construction.

Output: literature/search-logs/student-debt-household-formation-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-recon-probe.md")
ERROR_ABORT_SHARE = 0.20
PER_PAGE = 8


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

# ---------------------------------------------------------------------------------------------
# Vocabulary blocks. Named constants because the walls ARE vocabulary tests and the wording has to
# be identical in the probe and in the scope document that quotes its counts.
# ---------------------------------------------------------------------------------------------
DEBT = ('("student debt" OR "student loan" OR "student loans" OR "student loan debt" OR '
        '"educational debt" OR "education debt" OR "college debt" OR "student borrowing" OR '
        '"student borrowers" OR "education loans")')
# The young adult's OWN burden, stated unambiguously. Used to size the part of the body that cannot
# be confused with parents saving for a child's tuition.
OWNDEBT = ('("student loan debt" OR "student debt" OR "student borrowers" OR "loan burden" OR '
           '"debt burden" OR "outstanding student loans")')
# ANCHORED fertility vocabulary: population and life-course birth quantities.
FERT = ('("fertility" OR "childbearing" OR "first birth" OR "birth rates" OR "childlessness" OR '
        '"number of children" OR "transition to parenthood" OR "family size" OR "having children")')
# PLAIN half of the homonym diagnostic. "fertility" here has no large clinical homonym cloud the way
# it does in A.17, but the pairing is run rather than assumed, per the A.24 rule.
PLAINFERT = '("fertility" OR "births")'
UNION = ('("marriage" OR "marital" OR "union formation" OR "cohabitation" OR "partnership formation" OR '
         '"marriage timing" OR "age at marriage")')
HOUSE = ('("homeownership" OR "home ownership" OR "household formation" OR "first-time buyer" OR '
         '"living with parents" OR "residential independence" OR "coresidence")')
IDENT = ('("difference-in-differences" OR "difference in differences" OR "natural experiment" OR '
         '"quasi-experimental" OR "instrumental variable" OR "regression discontinuity" OR '
         '"event study" OR "causal effect" OR "exogenous variation")')
POLICY = ('("loan forgiveness" OR "debt relief" OR "debt cancellation" OR "income-driven repayment" OR '
          '"income contingent" OR "tuition policy" OR "financial aid reform" OR "free tuition" OR '
          '"loan limits" OR "Pell")')
# Wall 1 — professional-school debt studied for CAREER choice rather than family outcomes.
CAREER = ('("specialty choice" OR "career choice" OR "practice location" OR "rural practice" OR '
          '"residency" OR "primary care shortage" OR "physician workforce")')
# Wall 2 — general household liabilities. This is C.3.e and C.2.c, not C.3.g.
GENDEBT = ('("household debt" OR "consumer debt" OR "credit card debt" OR "mortgage debt" OR '
           '"medical debt" OR "payday" OR "unsecured debt")')
# Wall 3 — repayment behaviour with no household outcome.
DEFAULT = ('("loan default" OR "delinquency" OR "repayment behavior" OR "repayment behaviour" OR '
           '"default rates" OR "loan servicing")')
# Wall 5 — the OTHER balance sheet: parents anticipating a child's college costs.
PARENTPAY = ('("saving for college" OR "college savings" OR "paying for college" OR '
             '"parental contribution" OR "cost of raising children" OR "child rearing costs")')
EXPSERIES = ('("Survey of Consumer Finances" OR "Consumer Credit Panel" OR "credit bureau" OR '
             '"Baccalaureate and Beyond" OR "National Postsecondary Student Aid" OR '
             '"aggregate student loan balances" OR "student debt statistics")')
NONUS = ('("United Kingdom" OR "England" OR "Australia" OR "Canada" OR "Japan" OR "South Korea" OR '
         '"Sweden" OR "Norway" OR "Netherlands" OR "Chile" OR "New Zealand")')
SR = '("systematic review" OR "meta-analysis" OR "scoping review" OR "literature review")'

GROUPS = [
    ("The PRIMARY cell — a young adult's own education debt estimated against a FERTILITY outcome", [
        ("student debt AND a fertility outcome",
         f'title_and_abstract.search:{DEBT} AND {FERT}'),
        ("own-burden vocabulary AND a fertility outcome",
         f'title_and_abstract.search:{OWNDEBT} AND {FERT}'),
        ("student debt AND fertility AND an explicit identification strategy",
         f'title_and_abstract.search:{DEBT} AND {FERT} AND {IDENT}'),
        ("student debt AND first birth or transition to parenthood specifically",
         f'title_and_abstract.search:{DEBT} AND ("first birth" OR "transition to parenthood" OR "timing of births" OR "delayed childbearing")'),
        ("debt policy variation AND a fertility outcome",
         f'title_and_abstract.search:{DEBT} AND {POLICY} AND {FERT}'),
    ]),
    ("The ADJACENT cells — where the identified variation may actually live", [
        ("student debt AND marriage or union formation",
         f'title_and_abstract.search:{DEBT} AND {UNION}'),
        ("student debt AND marriage AND identification",
         f'title_and_abstract.search:{DEBT} AND {UNION} AND {IDENT}'),
        ("student debt AND homeownership or household formation",
         f'title_and_abstract.search:{DEBT} AND {HOUSE}'),
        ("student debt AND homeownership AND identification",
         f'title_and_abstract.search:{DEBT} AND {HOUSE} AND {IDENT}'),
        ("student debt AND identification, ANY outcome — the identified body's size",
         f'title_and_abstract.search:{DEBT} AND {IDENT}'),
    ]),
    ("Homonym and vocabulary diagnostic — the anchored/plain pairing", [
        ("PLAIN fertility vocabulary AND student debt",
         f'title_and_abstract.search:{DEBT} AND {PLAINFERT}'),
        ("student debt AND the bare word fertility only",
         'title_and_abstract.search:("student debt" OR "student loan") AND ("fertility")'),
        ("soil/ecology sense check — fertility without any debt term",
         'title_and_abstract.search:("student loan") AND ("soil fertility" OR "crop yield")'),
    ]),
    ("Wall 1 — professional-school debt studied for career choice, not family outcomes", [
        ("education debt AND career/specialty choice",
         f'title_and_abstract.search:{DEBT} AND {CAREER}'),
        ("education debt AND career choice AND a fertility outcome — the overlap that is IN",
         f'title_and_abstract.search:{DEBT} AND {CAREER} AND {FERT}'),
    ]),
    ("Wall 2 — general household liabilities (C.3.e and C.2.c, not C.3.g)", [
        ("general household/consumer debt AND fertility",
         f'title_and_abstract.search:{GENDEBT} AND {FERT}'),
        ("general household debt AND fertility AND student debt named — the overlap",
         f'title_and_abstract.search:{GENDEBT} AND {FERT} AND {DEBT}'),
    ]),
    ("Wall 3 — repayment behaviour with no household outcome", [
        ("student loan default and repayment behaviour",
         f'title_and_abstract.search:{DEBT} AND {DEFAULT}'),
        ("default/repayment AND a fertility outcome — the overlap that is IN",
         f'title_and_abstract.search:{DEBT} AND {DEFAULT} AND {FERT}'),
    ]),
    ("Wall 5 — the other balance sheet: parents anticipating a child's college costs (C.2.b)", [
        ("parental college-cost anticipation AND fertility",
         f'title_and_abstract.search:{PARENTPAY} AND {FERT}'),
        ("parental college-cost anticipation AND fertility AND student debt named",
         f'title_and_abstract.search:{PARENTPAY} AND {FERT} AND {DEBT}'),
    ]),
    ("Direction and conditioning — is the reverse separable", [
        ("student debt AND fertility AND conditioning on attainment",
         f'title_and_abstract.search:{DEBT} AND {FERT} AND ("educational attainment" OR "college completion" OR "degree completion" OR "controlling for education")'),
        ("childbearing as a cause of debt — the reverse direction",
         f'title_and_abstract.search:{DEBT} AND ("student parents" OR "parenting students" OR "having a child" OR "motherhood")'),
    ]),
    ("Exposure series for demographic significance", [
        ("student debt AND a named exposure series or credit panel",
         f'title_and_abstract.search:{DEBT} AND {EXPSERIES}'),
        ("share of a cohort holding student debt",
         f'title_and_abstract.search:{DEBT} AND ("share of borrowers" OR "prevalence of student debt" OR "average debt at graduation" OR "cumulative debt")'),
    ]),
    ("Non-US evidence and external validity", [
        ("student debt AND fertility AND a non-US setting",
         f'title_and_abstract.search:{DEBT} AND {FERT} AND {NONUS}'),
        ("income-contingent repayment systems AND family formation",
         f'title_and_abstract.search:("income contingent" OR "graduate tax" OR "HECS" OR "tuition fees") AND ({UNION} OR {FERT})'),
    ]),
    ("Channel 1 — prior systematic reviews", [
        ("SR/meta — student debt and any household outcome",
         f'title_and_abstract.search:{SR} AND {DEBT} AND ({FERT} OR {UNION} OR {HOUSE})'),
        ("SR/meta — student debt and wellbeing or life course",
         f'title_and_abstract.search:{SR} AND {DEBT} AND ("life course" OR "young adults" OR "wellbeing" OR "well-being")'),
    ]),
]

# Named candidate works. v5's own seminal list for C.3.g is unusually weak — a policy-institute
# report, a "forthcoming" paper, and a tweet — so it is TESTED here, not accepted. The candidates
# below are the works the RA expects to exist; a zero for any of them is a finding either way.
NAMED = [
    # v5 C.3.g's own seminal list, as written
    "Student debt and the transition to adulthood",
    "Student loan debt and fertility",
    # the works the RA expects the primary cell to contain
    "Can't afford a baby debt and young Americans",
    "Racial and ethnic variation in the relationship between student loan debt and the transition to first birth",
    "Do student loans delay marriage",
    "Student loans and marriage",
    "Do student loan burdens influence homeownership",
    "On the effect of student loans on access to homeownership",
    "The effects of student loans on life cycle earnings",
    "Student debt and default the role of institutional and student characteristics",
    "Debt and the transition to adulthood among college students",
    "Student loan debt and the transition to first birth",
]

# PASS 2 — surnames go to raw_author_name.search, never to title.search.
NAMED_RETRY = [
    ("Nau", "debt"),
    ("Dwyer", "debt"),
    ("Addo", "debt"),
    ("Bozick", "student loan"),
    ("Gicheva", "student loan"),
    ("Min", "student loan"),
    ("Mezza", "student loan"),
    ("Sommer", "student loan"),
    ("Chakrabarti", "student loan"),
    ("Yannelis", "student loan"),
    ("Dettling", "debt"),
    ("Sieg", "student"),
    ("Velez", "student loan"),
    ("Houle", "debt"),
]

errors, results, named_results, retry_results = [], [], [], []


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


SELECT = "id,doi,display_name,publication_year,cited_by_count,type,primary_location"


def probe(filt, per_page=PER_PAGE, sort="cited_by_count:desc"):
    url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20").replace('"', "%22") +
           f"&per-page={per_page}&select={SELECT}&sort={sort}&api_key={KEY}")
    return oa(url)


def guard_syntax():
    """Fail loudly before spending requests if any probe carries a known OpenAlex query hazard.

    Each produced a silently wrong COUNT — not an error — in an earlier chapter: a leading boolean
    word inflates to the unrestricted count; a `?` is read as a wildcard and 200s with an empty body;
    a comma inside a filter value truncates the filter and %2C does not save it.
    """
    bad = []
    for group, probes in GROUPS:
        for label, filt in probes:
            if "?" in filt:
                bad.append((label, "contains '?' — parsed as a wildcard"))
            if "," in filt:
                bad.append((label, "comma inside a filter value — truncates the filter"))
            for phrase in filt.split('"')[1::2]:
                first = phrase.strip().split(" ")[0].lower()
                if first in ("not", "and", "or"):
                    bad.append((label, f"phrase opens with boolean '{first}': \"{phrase}\""))
    if bad:
        sys.stderr.write("ABORT: query hazards found; no requests spent.\n")
        for lbl, why in bad:
            sys.stderr.write(f"  {lbl}: {why}\n")
        sys.exit(2)


def main():
    guard_syntax()
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY. Unfunded calls return 'Insufficient budget', "
                         "which this probe would bucket as errors and abort on anyway.\n")
        sys.exit(3)

    n_req = 0
    for group, probes in GROUPS:
        for label, filt in probes:
            n_req += 1
            d = probe(filt)
            if "results" not in d:
                errors.append((label, str(d.get("__err") or d)[:160]))
            else:
                results.append((group, label, filt, d["meta"]["count"], rows_of(d)))
            time.sleep(0.2)

    for t in NAMED:
        n_req += 1
        url = ("https://api.openalex.org/works?filter=title.search:" + t.replace(" ", "%20") +
               f"&per-page=5&select={SELECT}&api_key=" + KEY)
        d = oa(url)
        if "results" not in d:
            errors.append((t[:45], str(d.get("__err") or d)[:160]))
        else:
            named_results.append((t, d["meta"]["count"], rows_of(d)))
        time.sleep(0.2)

    for surname, term in NAMED_RETRY:
        n_req += 1
        filt = f"raw_author_name.search:{surname},title_and_abstract.search:{term}"
        url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20") +
               f"&per-page=5&select={SELECT}&sort=cited_by_count:desc&api_key=" + KEY)
        d = oa(url)
        if "results" not in d:
            errors.append((f"{surname} + {term}", str(d.get("__err") or d)[:160]))
        else:
            retry_results.append((f"{surname} + {term}", d["meta"]["count"], rows_of(d)))
        time.sleep(0.2)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        sys.stderr.write(f"ABORT: {len(errors)}/{n_req} requests failed ({share:.0%}). "
                         "Zero-hit counts are not trustworthy; not writing the report.\n")
        for lbl, e in errors[:12]:
            sys.stderr.write(f"  {lbl}: {e}\n")
        sys.exit(1)

    L = []
    L.append(f"# Reconnaissance probe — {SLUG}\n")
    L.append("**Hypothesis:** C.3.g (HYPOTHESES-v5.md) · **Ticket:** TICK-073\n\n")
    L.append("**Generated by:** `source/build/goldset/199_c3g_recon_probe.py`\n\n")
    L.append(f"**Requests:** {n_req} · **Failed:** {len(errors)} ({share:.1%}) · "
             f"**Abort threshold:** {ERROR_ABORT_SHARE:.0%}\n\n")
    L.append("Every zero below is a genuine absence, not a refused request: failures are counted "
             "separately and the report refuses to publish above the abort threshold. Pass-2 "
             "retries run through `raw_author_name.search` rather than `title.search`, so a zero "
             "there is also an absence rather than a malformed query.\n")

    for group in [g for g, _ in GROUPS]:
        L.append(f"\n## {group}\n")
        for g, label, filt, count, rows in results:
            if g != group:
                continue
            L.append(f"\n### {label} — **n = {count:,}**\n\n")
            L.append(f"`{filt}`\n\n")
            if not rows:
                L.append("*(no records)*\n")
                continue
            L.append("| Cites | Year | Title | Venue |\n|---|---|---|---|\n")
            for r in rows:
                t = r["title"][:95].replace("|", "/")
                v = r["venue"][:42].replace("|", "/")
                L.append(f"| {r['cites']:,} | {r['year']} | {t} | {v} |\n")

    L.append("\n## Named-work resolution — pass 1 (`title.search`)\n\n")
    L.append("| Query | n | Top match | Year | Cites | Type |\n|---|---|---|---|---|---|\n")
    for q, count, rows in named_results:
        if rows:
            r = rows[0]
            L.append(f"| {q[:60]} | {count} | {r['title'][:70].replace('|','/')} | {r['year']} | "
                     f"{r['cites']:,} | {r['type']} |\n")
        else:
            L.append(f"| {q[:60]} | 0 | **— no match —** | | | |\n")

    L.append("\n## Named-work resolution — pass 2 (`raw_author_name.search` + a title term)\n\n")
    L.append("| Author + term | n | Top match | Year | Cites | Type |\n|---|---|---|---|---|---|\n")
    for q, count, rows in retry_results:
        if rows:
            r = rows[0]
            L.append(f"| {q[:45]} | {count} | {r['title'][:70].replace('|','/')} | {r['year']} | "
                     f"{r['cites']:,} | {r['type']} |\n")
        else:
            L.append(f"| {q[:45]} | 0 | **— no match —** | | | |\n")

    if errors:
        L.append("\n## Failed requests (excluded from every count above)\n\n")
        for lbl, e in errors:
            L.append(f"- `{lbl}` — {e}\n")

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    open(OUT_MD, "w").write("".join(L))
    print(f"wrote {OUT_MD}  ({n_req} requests, {len(errors)} failed)")


if __name__ == "__main__":
    main()
