#!/usr/bin/env python3
"""
185_a17_recon_probe.py — A.17 (assisted reproductive technology access), pre-scope reconnaissance.

Runs before the scope document. Establishes from live records rather than from memory:

  (a) whether the PRIMARY estimand cell exists — a study that estimates the effect of ART ACCESS
      variation (insurance mandates, public subsidy, reimbursement reform, clinic entry, legal
      eligibility) on a POPULATION fertility quantity. Unlike A.12, the prior here is that the cell
      IS populated and identified: US state infertility-insurance mandates and European
      reimbursement reforms are policy discontinuities of exactly the kind PROTOCOL wants. The probe
      tests that prior instead of assuming it, because the whole case for opening A.17 as the next
      chapter rests on it;

  (b) the size and separability of the CLINICAL decoy — live birth rate per cycle, stimulation
      protocols, embryo culture, transfer technique. This is the largest body sharing A.17's
      vocabulary and it is a HOMONYM cloud: in the clinical literature "fertility" denotes a
      patient's fecundity or a treatment's success rate, not births per woman in a population.
      Per the A.24 lesson, its on-topic rate is measured TWICE — once with a vocabulary containing
      bare "fertility" and once with a population-anchored vocabulary that cannot carry the clinical
      sense — and the gap between the two is itself the finding. A wall justified by the plain
      measurement would be scoring its own justification;

  (c) whether the COUNTERFACTUAL-ACCOUNTING stream is real and citable — the "how much of postponed
      fertility does ART actually recover" literature (Leridon, Habbema, Sobotka, Lazzari). This is
      the stream that produces the chapter's headline number, and it is small enough that its
      absence would change the chapter's shape;

  (d) whether the UPPER-BOUND problem is addressed anywhere in the literature. A.17's naive count is
      "births that would not otherwise exist". That is an upper bound if the availability of ART
      itself induces the postponement whose losses it then repairs. A.12 hit the mirror image of
      this and had to carry it to its verdict; the probe asks whether anyone has estimated the
      behavioral response, or whether the chapter states it as an unquantified bound;

  (e) whether the A.12 boundary holds in the records. A.12's scope-freeze ruled
      ART live births = D_ART x (1 + m_ART), A.17 owning D_ART and A.12 owning m_ART. The probe
      measures how much of the ART-and-multiples body would arrive in A.17's nets, since that body
      must be routed OUT rather than screened in;

  (f) whether an exposure series exists to run demographic significance against — ICMART world
      reports, ESHRE EIM, CDC/SART, ANZARD. The entire demographic-significance stage depends on a
      real, citable ART-births-per-population series, so the probe verifies it rather than
      remembering it.

Discipline carried from prior runs (A.12, A.24, B.5, B.6, B.7, D.2.d, D.3.b, D.3.c):
  * A failed request goes in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the report
    refuses to publish if the error share exceeds ERROR_ABORT_SHARE.
  * HTTPS goes through curl: this interpreter has no CA bundle, so urllib fails every call, and it
    fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone.
  * No search phrase opens with not/and/or; no `?` anywhere in a search value; no comma inside a
    filter value; no phrase whose meaning rests on a stopword. All four are checked before any
    request is spent.

  * PASS-2 RETRIES ARE FIXED HERE, not inherited. Every prior chapter's pass 2 sent
    author-plus-title strings to `filter=title.search:`, which matches the title field only and is
    unsatisfiable by construction — A.24 returned 15 zeros out of 15 and they read as corroboration
    of pass 1. This script sends surnames to `filter=raw_author_name.search:` AND a title term, so a
    zero means the work is absent rather than the query malformed.

Output: literature/search-logs/art-access-fertility-recovery-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "art-access-fertility-recovery"
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
ART = '("assisted reproductive technology" OR "assisted reproduction" OR "in vitro fertilization" OR "in vitro fertilisation" OR "IVF" OR "ICSI" OR "intracytoplasmic sperm injection" OR "fertility treatment" OR "infertility treatment")'
ACCESS = '("insurance mandate" OR "insurance coverage" OR "mandated coverage" OR "reimbursement" OR "public funding" OR "subsidy" OR "subsidised" OR "subsidized" OR "out-of-pocket" OR "access to treatment" OR "eligibility" OR "affordability" OR "cost sharing")'
# POPULATION-ANCHORED outcome vocabulary. Deliberately excludes the bare word "fertility": in the
# clinical ART literature that word means a patient's fecundity or a cycle's success rate. See the
# A.24 homonym lesson — a diagnostic containing the shared word measures the collision, not the
# contamination.
POPFERT = '("total fertility rate" OR "completed fertility" OR "cohort fertility" OR "birth rates" OR "crude birth rate" OR "childbearing" OR "parity transition" OR "number of children" OR "population level fertility")'
# The PLAIN vocabulary, carrying bare "fertility". Used ONLY as the paired half of the homonym
# diagnostic, never to justify a wall.
PLAINFERT = '("fertility" OR "birth rate" OR "births")'
IDENT = '("difference-in-differences" OR "difference in differences" OR "natural experiment" OR "quasi-experimental" OR "instrumental variable" OR "regression discontinuity" OR "event study" OR "policy reform" OR "causal effect")'
CLINICAL = '("live birth rate per cycle" OR "clinical pregnancy rate" OR "implantation rate" OR "ovarian stimulation" OR "embryo culture" OR "blastocyst" OR "luteal phase" OR "gonadotropin" OR "oocyte retrieval" OR "cumulative live birth rate")'
MULTIPLES = '("multiple birth" OR "multiple births" OR "twin" OR "twins" OR "twinning" OR "multiple pregnancy" OR "higher order multiple" OR "single embryo transfer")'
POSTPONE = '("postponement" OR "delayed childbearing" OR "advanced maternal age" OR "age at first birth" OR "reproductive ageing" OR "reproductive aging" OR "fertility postponement")'
PRESERVE = '("oocyte cryopreservation" OR "egg freezing" OR "fertility preservation" OR "social freezing" OR "oncofertility")'
REGISTRY = '("ICMART" OR "ESHRE" OR "European IVF Monitoring" OR "SART" OR "ANZARD" OR "national ART registry" OR "ART surveillance")'
SR = '("systematic review" OR "meta-analysis" OR "scoping review")'

GROUPS = [
    ("The PRIMARY cell — ART ACCESS variation estimated against a POPULATION fertility quantity", [
        ("ART access/coverage AND a population fertility quantity",
         f'title_and_abstract.search:{ART} AND {ACCESS} AND {POPFERT}'),
        ("insurance mandate AND ART, any outcome — the US policy body",
         f'title_and_abstract.search:("infertility insurance mandate" OR "insurance mandate" OR "mandated coverage") AND {ART}'),
        ("ART access AND an explicit identification strategy",
         f'title_and_abstract.search:{ART} AND {ACCESS} AND {IDENT}'),
        ("public funding / reimbursement reform AND birth rates",
         f'title_and_abstract.search:{ART} AND ("public funding" OR "reimbursement" OR "subsidy" OR "co-payment" OR "state funding") AND {POPFERT}'),
        ("cross-country ART utilisation AND fertility rates",
         f'title_and_abstract.search:{ART} AND ("cross-country" OR "cross-national" OR "international comparison" OR "country differences") AND {POPFERT}'),
        ("clinic entry / distance / supply of ART services",
         f'title_and_abstract.search:{ART} AND ("clinic" OR "distance" OR "travel" OR "supply" OR "provider" OR "availability") AND {POPFERT}'),
    ]),
    ("The COUNTERFACTUAL-ACCOUNTING stream — how much of postponed fertility does ART recover", [
        ("can ART compensate for age-related decline",
         f'title_and_abstract.search:{ART} AND ("compensate" OR "offset" OR "recover" OR "recuperation" OR "make up for") AND {POSTPONE}'),
        ("ART contribution to completed fertility / TFR, stated as a contribution",
         f'title_and_abstract.search:{ART} AND ("contribution to" OR "contribution of" OR "share of births" OR "proportion of births" OR "percentage of all births" OR "accounted for")'),
        ("simulation / projection of ART effect on population fertility",
         f'title_and_abstract.search:{ART} AND ("simulation" OR "microsimulation" OR "projection" OR "counterfactual" OR "scenario") AND {POPFERT}'),
        ("ART and the parity transition specifically",
         f'title_and_abstract.search:{ART} AND ("parity transition" OR "first birth" OR "second birth" OR "birth order" OR "progression to")'),
    ]),
    ("Decoy cloud 1 — CLINICAL per-cycle outcomes (the homonym cloud; measured twice, see report)", [
        ("clinical per-cycle vocabulary, all",
         f'title_and_abstract.search:{CLINICAL}'),
        ("PLAIN diagnostic — clinical cloud scored with bare 'fertility' in the vocabulary",
         f'title_and_abstract.search:{CLINICAL} AND {PLAINFERT}'),
        ("ANCHORED diagnostic — same cloud scored with population-only vocabulary",
         f'title_and_abstract.search:{CLINICAL} AND {POPFERT}'),
        ("ART success rates — does the success-rate body separate from the access body",
         f'title_and_abstract.search:{ART} AND ("success rate" OR "success rates" OR "live birth rate") AND ("predictor" OR "prognosis" OR "protocol" OR "randomized" OR "randomised")'),
    ]),
    ("Decoy cloud 2 — ART safety and offspring outcomes", [
        ("ART AND congenital / neonatal / child outcomes",
         f'title_and_abstract.search:{ART} AND ("birth defect" OR "congenital" OR "neonatal outcome" OR "preterm" OR "birth weight" OR "child development" OR "imprinting disorder")'),
        ("ART AND maternal safety / OHSS",
         f'title_and_abstract.search:{ART} AND ("ovarian hyperstimulation" OR "OHSS" OR "maternal complication" OR "maternal morbidity")'),
    ]),
    ("Boundary A.12 — the multiplier, which A.12's scope-freeze already owns and A.17 must route OUT", [
        ("ART AND multiples — the body that must not be screened in",
         f'title_and_abstract.search:{ART} AND {MULTIPLES}'),
        ("ART AND multiples AND a population fertility quantity — the overlap that needs a rule",
         f'title_and_abstract.search:{ART} AND {MULTIPLES} AND {POPFERT}'),
    ]),
    ("Boundary A.15 — postponement, which A.17 offsets rather than explains", [
        ("postponement AND ART, joint treatment",
         f'title_and_abstract.search:{ART} AND {POSTPONE}'),
        ("does ART AVAILABILITY induce postponement — the upper-bound question",
         f'title_and_abstract.search:{ART} AND ("moral hazard" OR "false reassurance" OR "overestimate" OR "reliance on" OR "insurance effect" OR "induced delay" OR "behavioral response" OR "behavioural response") AND {POSTPONE}'),
        ("awareness / beliefs about ART success AND childbearing intentions",
         f'title_and_abstract.search:{ART} AND ("awareness" OR "beliefs" OR "knowledge" OR "perceived" OR "expectations") AND ("intention" OR "intentions" OR "plans" OR "desire")'),
    ]),
    ("Routed body — fertility preservation and egg freezing (named in v5's claim, so routed not cut)", [
        ("fertility preservation / egg freezing, all",
         f'title_and_abstract.search:{PRESERVE}'),
        ("egg freezing AND a population fertility quantity",
         f'title_and_abstract.search:{PRESERVE} AND {POPFERT}'),
        ("egg freezing AND employer coverage / policy",
         f'title_and_abstract.search:{PRESERVE} AND ("employer" OR "workplace" OR "benefit" OR "coverage" OR "policy" OR "subsidy")'),
    ]),
    ("Exposure series for demographic significance", [
        ("ART registries by name",
         f'title_and_abstract.search:{REGISTRY}'),
        ("ART share of national births, reported as a series",
         f'title_and_abstract.search:{ART} AND ("national" OR "nationwide" OR "population-based" OR "register-based" OR "registry") AND ("share" OR "proportion" OR "percentage" OR "trend" OR "trends")'),
        ("ART cycles per capita / utilisation rates across countries",
         f'title_and_abstract.search:{ART} AND ("utilisation" OR "utilization" OR "cycles per" OR "treatment rate" OR "per million" OR "per 1000 women")'),
    ]),
    ("Channel 1 — prior systematic reviews", [
        ("SR/meta — ART access or coverage",
         f'title_and_abstract.search:{SR} AND {ART} AND {ACCESS}'),
        ("SR/meta — ART and population fertility",
         f'title_and_abstract.search:{SR} AND {ART} AND {POPFERT}'),
    ]),
]

# Named candidate works. v5's own seminal list is TESTED here, not accepted — the version-of-record
# gate and the ghost-citation finding both came out of assuming a remembered citation resolves.
NAMED = [
    # v5 A.17's seminal list, as written in HYPOTHESES-v5.md
    "Can assisted reproduction technology compensate for the natural decline in fertility with age",
    "Realizing a desired family size when should couples start",
    "The contribution of assisted reproduction to completed fertility",
    # the accounting stream
    "The contribution of assisted reproductive technology to fertility rates and parity transition",
    "Assisted reproductive technology and the demographic transition",
    "How much does assisted reproductive technology contribute to national birth rates",
    # the access / policy stream
    "Health disparities and infertility impacts of state level insurance mandates",
    "The effects of insurance mandates on choices and outcomes in infertility treatment markets",
    "Coverage of infertility treatment and fertility outcomes",
    "Infertility insurance mandates and fertility",
    "Public funding of in vitro fertilisation and birth rates",
]

# PASS 2 — the fix. Surnames go to raw_author_name.search, never to title.search.
# Each entry is (surname, title term that must also appear).
NAMED_RETRY = [
    ("Leridon", "compensate"),
    ("Habbema", "family size"),
    ("Sobotka", "assisted reproduction"),
    ("Lazzari", "assisted reproductive"),
    ("Chambers", "assisted reproductive"),
    ("Bitler", "infertility"),
    ("Schmidt", "infertility insurance"),
    ("Hamilton", "infertility treatment"),
    ("Machado", "infertility"),
    ("Buckles", "infertility"),
    ("te Velde", "reproductive"),
    ("Präg", "assisted reproduction"),
    ("Goisis", "assisted reproduction"),
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

    Each of these produced a silently wrong COUNT — not an error — in an earlier chapter: a leading
    boolean word inflates to the unrestricted count; a `?` is read as a wildcard and 200s with an
    empty body; a comma inside a filter value truncates the filter and %2C does not save it.
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
        filt = (f"raw_author_name.search:{surname},title_and_abstract.search:{term}")
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
    L.append("**Hypothesis:** A.17 (HYPOTHESES-v5.md) · **Ticket:** TICK-072\n\n")
    L.append("**Generated by:** `source/build/goldset/185_a17_recon_probe.py`\n\n")
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
    L.append("Author surnames are unsatisfiable in `title.search` by construction; every prior "
             "chapter's pass 2 sent them there and read the resulting zeros as corroboration.\n\n")
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
