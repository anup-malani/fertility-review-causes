#!/usr/bin/env python3
"""
123_b7_recon_probe.py — B.7 (antidepressants / pharmacological subfecundity), pre-scope reconnaissance.

Runs before A3. Establishes from live records rather than from memory:
  (a) the size of the adjacent clinical and psychiatric literature relative to the demographic seam
      this chapter needs — B.7's vocabulary is shared with two enormous decoy literatures, SSRI
      sexual side effects and antidepressant safety in pregnancy;
  (b) whether the PRIMARY estimand cell (medication exposure -> a fertility outcome) exists at all in
      the indexed corpus, and on which side of the sex boundary it sits;
  (c) how the named canonical works resolve, including whether the ones this analyst can name from
      memory exist under the titles remembered.

Discipline carried from prior runs:
  * A failed request is counted in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the
    report refuses to publish if the error share exceeds ERROR_ABORT_SHARE. A wrong zero here would
    propagate into the scope document as "this literature does not exist".
  * HTTPS goes through curl: the interpreter on this machine has no CA bundle, so urllib fails every
    call, and it fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone — mailto draws on a
    shared anonymous budget that a probe sweep exhausts, and the failure presents as slowness first.

Output: literature/search-logs/{slug}-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "antidepressants-ssri-subfecundity"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-recon-probe.md")
ERROR_ABORT_SHARE = 0.20
PER_PAGE = 8


def openalex_key():
    """Read the funded key from the environment, then from .env. Never log or cache the value."""
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

AD = '("antidepressant" OR "SSRI" OR "selective serotonin reuptake inhibitor")'

# --- Probe set. Grouped so the report reads as an argument, not as a dump. ---
GROUPS = [
    ("Ambient volume — the two decoy literatures", [
        ("antidepressants AND sexual dysfunction", f'title_and_abstract.search:{AD} AND "sexual dysfunction"'),
        ("antidepressants in pregnancy (safety)", f'title_and_abstract.search:{AD} AND ("pregnancy" OR "prenatal" OR "in utero")'),
        ("antidepressants AND birth outcomes", f'title_and_abstract.search:{AD} AND ("birth outcomes" OR "preterm birth" OR "birth weight" OR "congenital")'),
        ("antidepressants AND depression treatment efficacy", f'title_and_abstract.search:{AD} AND ("efficacy" OR "randomized") AND ("major depressive disorder" OR "depression")'),
    ]),
    ("The demographic seam", [
        ("antidepressants AND fertility", f'title_and_abstract.search:{AD} AND "fertility"'),
        ("antidepressants AND TFR / birth rate", f'title_and_abstract.search:{AD} AND ("total fertility rate" OR "birth rate" OR "fertility decline" OR "fertility rate")'),
        ("antidepressants AND childbearing / parity", f'title_and_abstract.search:{AD} AND ("childbearing" OR "completed fertility" OR "parity" OR "family size")'),
        ("psychotropic medication AND fertility", 'title_and_abstract.search:("psychotropic" OR "psychiatric medication") AND ("fertility" OR "childbearing")'),
        ("pharmaceutical exposure AND population fertility", 'title_and_abstract.search:("pharmaceutical" OR "medication use") AND ("population fertility" OR "fertility decline")'),
    ]),
    ("Does the PRIMARY cell exist? (medication -> fertility outcome)", [
        ("antidepressants AND time to pregnancy / fecundability", f'title_and_abstract.search:{AD} AND ("time to pregnancy" OR "fecundability" OR "time-to-pregnancy")'),
        ("antidepressants AND live birth (cohort)", f'title_and_abstract.search:{AD} AND "live birth" AND ("cohort" OR "register" OR "population-based")'),
        ("antidepressants AND infertility / subfertility", f'title_and_abstract.search:{AD} AND ("infertility" OR "subfertility" OR "subfecundity")'),
        ("antidepressants AND semen quality (male)", f'title_and_abstract.search:{AD} AND ("semen quality" OR "sperm" OR "spermatogenesis")'),
        ("antidepressants AND coital / sexual frequency", f'title_and_abstract.search:{AD} AND ("coital frequency" OR "sexual frequency" OR "frequency of intercourse" OR "sexual activity")'),
    ]),
    ("The endocrine pathway, and the antipsychotic scope question", [
        ("SSRI AND gonadotropins / sex hormones", f'title_and_abstract.search:{AD} AND ("prolactin" OR "gonadotropin" OR "luteinizing hormone" OR "testosterone" OR "estradiol")'),
        ("antipsychotics AND hyperprolactinaemia AND reproduction", 'title_and_abstract.search:("antipsychotic" OR "neuroleptic") AND ("hyperprolactinemia" OR "hyperprolactinaemia") AND ("amenorrhea" OR "amenorrhoea" OR "fertility" OR "menstrual")'),
        ("post-SSRI sexual dysfunction (persistence)", 'title_and_abstract.search:"post-SSRI sexual dysfunction" OR "persistent sexual dysfunction after"'),
    ]),
    ("Exposure prevalence — the parameter the significance test runs on", [
        ("antidepressant use prevalence, women", f'title_and_abstract.search:{AD} AND ("prevalence" OR "utilization" OR "utilisation" OR "trends") AND ("women" OR "reproductive age" OR "childbearing age")'),
        ("antidepressant dispensing trends, national", f'title_and_abstract.search:{AD} AND ("national" OR "nationwide" OR "registry") AND ("dispensing" OR "prescription" OR "defined daily dose")'),
        ("antidepressant use in pregnancy, prevalence trend", f'title_and_abstract.search:{AD} AND "pregnancy" AND ("prevalence" OR "trends") AND ("cohort" OR "registry" OR "claims")'),
    ]),
    ("Identification — confounding by indication (Wall 1 against D.3.a)", [
        ("confounding by indication, antidepressants", f'title_and_abstract.search:{AD} AND ("confounding by indication" OR "active comparator" OR "sibling design" OR "discordant siblings")'),
        ("depression / mental illness AND fertility", 'title_and_abstract.search:("depression" OR "mental illness" OR "psychiatric disorder") AND ("fertility" OR "childbearing" OR "birth rate")'),
        ("severe mental illness AND fertility rates", 'title_and_abstract.search:("schizophrenia" OR "bipolar" OR "severe mental illness") AND ("fertility" OR "reproductive" OR "birth rate")'),
    ]),
    ("Channel 1 — prior systematic reviews and meta-analyses", [
        ("SR/meta on antidepressant sexual dysfunction", f'title_and_abstract.search:("systematic review" OR "meta-analysis") AND {AD} AND ("sexual dysfunction" OR "libido")'),
        ("SR/meta on antidepressants and fertility/semen", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND {AD} AND ("fertility" OR "semen" OR "sperm" OR "reproductive")'),
    ]),
    ("Wall — the non-human literature", [
        ("fluoxetine AND animal reproduction", 'title_and_abstract.search:("fluoxetine" OR "sertraline" OR "SSRI") AND ("rat" OR "mice" OR "murine" OR "zebrafish" OR "fish") AND ("reproduction" OR "fecundity" OR "sperm" OR "offspring")'),
    ]),
    ("The four cells that decide the chapter, probed one at a time", [
        ("fecundability, named", f'title_and_abstract.search:{AD} AND "fecundability"'),
        ("time to pregnancy, named", f'title_and_abstract.search:{AD} AND ("time to pregnancy" OR "time-to-pregnancy")'),
        ("spontaneous abortion / miscarriage (B.5 border)", f'title_and_abstract.search:{AD} AND ("spontaneous abortion" OR "miscarriage")'),
        ("ART / IVF cycle outcome (A.17 border)", f'title_and_abstract.search:{AD} AND ("in vitro fertilization" OR "in vitro fertilisation" OR "assisted reproductive")'),
        ("ovulation / menstrual function", f'title_and_abstract.search:{AD} AND ("anovulation" OR "ovulation" OR "menstrual cycle" OR "amenorrhea")'),
        ("aggregate / ecological births", f'title_and_abstract.search:{AD} AND ("population-level" OR "ecological" OR "aggregate" OR "country-level") AND ("births" OR "fertility")'),
    ]),
]

# Named candidate works. Half of these are titles this analyst can approximate from memory and half
# are guesses at what should exist; the probe reports which resolve and to what, and nothing is
# carried into the scope document that does not resolve here.
NAMED = [
    "Use of selective serotonin reuptake inhibitors reduces fertility in men",
    "Prevalence of sexual dysfunction among newer antidepressants",
    "Antidepressant medications and semen parameters male fertility",
    "Antidepressant use and fecundability",
    "Preconception antidepressant use and time to pregnancy",
    "Selective serotonin reuptake inhibitors and risk of spontaneous abortion",
    "Antidepressant use during pregnancy prevalence trends",
    "Antidepressant utilization trends OECD countries",
    "Sexual dysfunction associated with selective serotonin reuptake inhibitors a critical review",
    "The social construction of female sexual dysfunction",
    "Antidepressants and sexual dysfunction a systematic review and meta-analysis",
    "Psychotropic medication use and reproductive outcomes register based cohort",
]

# Second pass over the titles the first pass could not resolve. `title.search` is close to exact, so a
# zero there means "not under the title this analyst produced" and NOT "no such literature". The two
# readings have opposite consequences for the scope document — one says a cell is empty, the other says
# a memory is wrong — and separating them is the whole point of running the retry.
NAMED_RETRY = [
    "Use of antidepressants during pregnancy and the risk of spontaneous abortion",
    "Antidepressant use in persons aged 12 and over United States",
    "Trends in antidepressant use among adults",
    "Antidepressants and fecundability prospective cohort study",
    "Preconception mental health medication use and fecundability",
    "Female infertility and antidepressant use",
    "Sexual dysfunction during treatment with serotonergic and noradrenergic antidepressants",
    "Incidence of sexual dysfunction associated with antidepressant agents",
    "Effect of selective serotonin reuptake inhibitors on semen quality",
    "Antidepressant use and the risk of infertility",
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


def probe(filt, per_page=PER_PAGE, sort="cited_by_count:desc"):
    url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20").replace('"', "%22") +
           f"&per-page={per_page}&select=id,doi,display_name,publication_year,cited_by_count,type,"
           f"primary_location&sort={sort}&api_key={KEY}")
    return oa(url)


def main():
    n_req = 0
    for group, probes in GROUPS:
        for label, filt in probes:
            n_req += 1
            d = probe(filt)
            if "results" not in d:
                errors.append((label, str(d.get("__err") or d)[:160]))
            else:
                results.append((group, label, filt, d["meta"]["count"], rows_of(d)))
            time.sleep(0.25)

    for lst, sink in ((NAMED, named_results), (NAMED_RETRY, retry_results)):
        for t in lst:
            n_req += 1
            url = ("https://api.openalex.org/works?filter=title.search:" + t.replace(" ", "%20") +
                   "&per-page=5&select=id,doi,display_name,publication_year,cited_by_count,type,"
                   "primary_location&api_key=" + KEY)
            d = oa(url)
            if "results" not in d:
                errors.append((t[:45], str(d.get("__err") or d)[:160]))
            else:
                sink.append((t, d["meta"]["count"], rows_of(d)))
            time.sleep(0.25)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        print(f"ABORT: {len(errors)}/{n_req} requests failed ({share:.0%} > {ERROR_ABORT_SHARE:.0%}). "
              "Report NOT written — a zero-hit count cannot be distinguished from a refusal at this "
              "error rate.", file=sys.stderr)
        for e in errors:
            print("  ", e, file=sys.stderr)
        sys.exit(1)

    L = [f"# Pre-scope reconnaissance — {SLUG}", "",
         "Generated by `source/build/goldset/123_b7_recon_probe.py`. Counts are OpenAlex universe "
         "sizes for the stated filter; listed works are the most-cited within it.", "",
         f"**Requests: {n_req} · failed: {len(errors)} ({share:.0%}) · zero-hit counts below are "
         "therefore genuine absences, not refusals.**", "",
         "Why this exists: B.7 names a medication whose side effects are documented in a very large "
         "clinical literature and whose safety in pregnancy is documented in a second very large one. "
         "Neither estimates a fertility quantity. The scope document needed a measured picture of how "
         "thin the seam between them is before the walls were drawn rather than after the first "
         "screen came back.", ""]

    cur = None
    for group, label, filt, count, rows in results:
        if group != cur:
            L += [f"## {group}", ""]
            cur = group
        L += [f"### {label}", "", f"`{filt}` — **n = {count:,}**", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    L += ["## Named candidate works — resolution behaviour", "",
          "Titles are approximations, several asserted from this analyst's memory. What resolves here "
          "is what may be carried into the scope document; what does not resolve is not cited.", ""]
    for t, count, rows in named_results:
        L += [f"### {t}", "", f"n = {count}", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    L += ["## Named candidate works — second pass on differently-worded titles", "",
          "**A zero on a title probe is not a zero on a literature.** `title.search` is close to exact, "
          "so an unresolved title says the analyst's remembered wording is wrong, which is a different "
          "and much more common failure than the cell being empty. The group probes above are what "
          "measure whether a literature exists; these measure whether a citation can be made.", ""]
    for t, count, rows in retry_results:
        L += [f"### {t}", "", f"n = {count}", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    if errors:
        L += ["## Error bucket (failed requests — NOT zero-hits)", ""]
        L += [f"- {a}: {b}" for a, b in errors] + [""]

    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"requests={n_req} failed={len(errors)} groups={len(GROUPS)} named={len(named_results)} retry={len(retry_results)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
