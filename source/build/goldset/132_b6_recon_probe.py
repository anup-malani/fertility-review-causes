#!/usr/bin/env python3
"""
132_b6_recon_probe.py — B.6 (microplastics and PFAS in reproductive tissues), pre-scope reconnaissance.

Runs before A3. Establishes from live records rather than from memory:
  (a) the size of the adjacent literatures relative to the demographic seam this chapter needs. B.6's
      vocabulary is shared with THREE very large decoy bodies — marine and freshwater ecotoxicology,
      environmental occurrence and remediation chemistry, and the non-reproductive PFAS health
      literature (thyroid, immune, cancer) — none of which estimates a fertility quantity;
  (b) whether the PRIMARY estimand cell (exposure -> a human fertility outcome) exists at all, and
      how much of it is ART-clinic derived, which is the structural selection problem of this chapter:
      follicular fluid is obtainable mainly from IVF patients;
  (c) how much of the corpus is DETECTION (concentration measured in a tissue, no outcome) rather
      than association, since v5's claim for splitting B.6 out of B.2 rests on the detection studies;
  (d) whether the parity/excretion reverse-causation literature — PFAS are cleared by pregnancy,
      menstruation and lactation, so parity determines exposure — is present and named;
  (e) how the works v5 lists as seminal resolve, several of which are 2025 and asserted from memory.

Discipline carried from prior runs:
  * A failed request is counted in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the
    report refuses to publish if the error share exceeds ERROR_ABORT_SHARE. A wrong zero here would
    propagate into the scope document as "this literature does not exist".
  * HTTPS goes through curl: the interpreter on this machine has no CA bundle, so urllib fails every
    call, and it fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone — mailto draws on a
    shared anonymous budget that a probe sweep exhausts, and the failure presents as slowness first.
  * Named-title probes run in two passes. A zero on `title.search` means the remembered wording is
    wrong; only an empty GROUP probe means a literature is absent. The two have opposite consequences.

Output: literature/search-logs/{slug}-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "microplastics-pfas-reproductive"
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

# The two chemical families B.6 owns, and the legacy family B.2 retains. Kept as named constants
# because the B.2/B.6 wall is a chemical-class test and the vocabulary has to be identical in the
# probe and in the scope document that quotes its counts.
MP = '("microplastic" OR "microplastics" OR "nanoplastic" OR "nanoplastics" OR "micro- and nanoplastics")'
PF = '("PFAS" OR "per- and polyfluoroalkyl" OR "perfluoroalkyl" OR "perfluorinated" OR "PFOA" OR "PFOS")'
BOTH = f'({MP} OR {PF})'
LEGACY = '("phthalate" OR "phthalates" OR "bisphenol" OR "BPA" OR "organochlorine" OR "DDT")'
FERT = '("fertility" OR "fecundability" OR "fecundity" OR "time to pregnancy" OR "subfertility" OR "infertility")'

GROUPS = [
    ("Ambient volume — the three decoy literatures", [
        ("microplastics, all", f'title_and_abstract.search:{MP}'),
        ("microplastics AND marine / aquatic organisms", f'title_and_abstract.search:{MP} AND ("marine" OR "aquatic" OR "fish" OR "mussel" OR "zooplankton" OR "sediment")'),
        ("microplastics AND environmental occurrence / removal", f'title_and_abstract.search:{MP} AND ("occurrence" OR "removal" OR "wastewater" OR "soil" OR "atmospheric" OR "degradation")'),
        ("PFAS, all", f'title_and_abstract.search:{PF}'),
        ("PFAS AND drinking water / remediation", f'title_and_abstract.search:{PF} AND ("drinking water" OR "groundwater" OR "remediation" OR "adsorption" OR "treatment")'),
        ("PFAS AND non-reproductive health outcomes", f'title_and_abstract.search:{PF} AND ("thyroid" OR "immune" OR "vaccine" OR "cholesterol" OR "cancer" OR "kidney")'),
    ]),
    ("The demographic seam — does anyone estimate a population fertility quantity?", [
        ("MP/PFAS AND fertility rate / TFR / fertility decline", f'title_and_abstract.search:{BOTH} AND ("total fertility rate" OR "fertility rate" OR "fertility decline" OR "birth rate")'),
        ("MP/PFAS AND childbearing / parity / family size", f'title_and_abstract.search:{BOTH} AND ("childbearing" OR "completed fertility" OR "parity" OR "family size" OR "number of children")'),
        ("MP/PFAS AND population-level / ecological / country-level births", f'title_and_abstract.search:{BOTH} AND ("population-level" OR "ecological" OR "aggregate" OR "country-level" OR "national trends") AND ("births" OR "fertility")'),
        ("environmental chemical exposure AND fertility decline (any family)", 'title_and_abstract.search:("environmental chemical" OR "endocrine disruptor" OR "endocrine-disrupting") AND ("fertility decline" OR "total fertility rate" OR "birth rate")'),
    ]),
    ("Does the PRIMARY cell exist? Human exposure -> a fertility outcome", [
        ("PFAS AND time to pregnancy / fecundability", f'title_and_abstract.search:{PF} AND ("time to pregnancy" OR "time-to-pregnancy" OR "fecundability")'),
        ("PFAS AND infertility / subfecundity", f'title_and_abstract.search:{PF} AND ("infertility" OR "subfecundity" OR "subfertility")'),
        ("microplastics AND time to pregnancy / fecundability", f'title_and_abstract.search:{MP} AND ("time to pregnancy" OR "time-to-pregnancy" OR "fecundability" OR "infertility" OR "subfertility")'),
        ("PFAS AND semen quality / sperm", f'title_and_abstract.search:{PF} AND ("semen quality" OR "sperm count" OR "sperm concentration" OR "spermatogenesis")'),
        ("microplastics AND semen quality / sperm", f'title_and_abstract.search:{MP} AND ("semen quality" OR "sperm count" OR "sperm concentration" OR "spermatogenesis")'),
        ("MP/PFAS AND ovarian reserve / AMH / antral follicle", f'title_and_abstract.search:{BOTH} AND ("ovarian reserve" OR "anti-Mullerian" OR "antral follicle" OR "folliculogenesis")'),
        ("MP/PFAS AND menstrual / ovulation / age at menopause", f'title_and_abstract.search:{BOTH} AND ("menstrual" OR "anovulation" OR "ovulation" OR "menopause")'),
    ]),
    ("The tissue-detection literature — B.6's stated reason for existing", [
        ("microplastics in placenta", f'title_and_abstract.search:{MP} AND ("placenta" OR "placental" OR "meconium")'),
        ("microplastics in follicular fluid", f'title_and_abstract.search:{MP} AND ("follicular fluid" OR "ovarian tissue" OR "ovary")'),
        ("microplastics in semen / seminal plasma / testis", f'title_and_abstract.search:{MP} AND ("seminal plasma" OR "semen" OR "testis" OR "testicular")'),
        ("PFAS in follicular fluid / seminal plasma", f'title_and_abstract.search:{PF} AND ("follicular fluid" OR "seminal plasma" OR "amniotic fluid")'),
        ("microplastics in human blood / tissue generally", f'title_and_abstract.search:{MP} AND ("human blood" OR "human tissue" OR "detected in human")'),
        ("detection method / contamination control (blanks)", f'title_and_abstract.search:{MP} AND ("contamination control" OR "procedural blank" OR "quality assurance" OR "Raman" OR "FTIR" OR "pyrolysis")'),
    ]),
    ("Mechanism stream", [
        ("MP/PFAS AND steroidogenesis / hormone disruption", f'title_and_abstract.search:{BOTH} AND ("steroidogenesis" OR "estradiol" OR "testosterone" OR "gonadotropin" OR "endocrine disruption")'),
        ("MP/PFAS AND implantation / trophoblast / decidua", f'title_and_abstract.search:{BOTH} AND ("implantation" OR "trophoblast" OR "decidua" OR "embryo development")'),
        ("MP/PFAS AND oxidative stress / inflammation, reproductive", f'title_and_abstract.search:{BOTH} AND ("oxidative stress" OR "inflammation" OR "apoptosis") AND ("reproductive" OR "ovarian" OR "testicular")'),
    ]),
    ("Walls — the literatures that must route out", [
        ("Wall: non-human reproduction (rodent, fish, invertebrate)", f'title_and_abstract.search:{BOTH} AND ("rat" OR "mice" OR "murine" OR "zebrafish" OR "Daphnia" OR "medaka") AND ("reproduction" OR "fecundity" OR "sperm" OR "offspring")'),
        ("Wall: in vitro / cell line only", f'title_and_abstract.search:{BOTH} AND ("cell line" OR "in vitro" OR "cultured cells" OR "cytotoxicity")'),
        ("Wall: A.17 — ART / IVF cycle outcome", f'title_and_abstract.search:{BOTH} AND ("in vitro fertilization" OR "in vitro fertilisation" OR "assisted reproductive" OR "ICSI" OR "embryo transfer")'),
        ("Wall: B.5 — miscarriage / spontaneous abortion / stillbirth", f'title_and_abstract.search:{BOTH} AND ("miscarriage" OR "spontaneous abortion" OR "pregnancy loss" OR "stillbirth")'),
        ("Wall: pregnancy safety — birth weight / preterm / neurodevelopment", f'title_and_abstract.search:{BOTH} AND ("birth weight" OR "preterm" OR "gestational age" OR "neurodevelopment" OR "autism")'),
        ("Wall: B.2 sibling — legacy EDCs AND fertility (sizes the sibling)", f'title_and_abstract.search:{LEGACY} AND {FERT}'),
        ("Wall probe: do studies measure BOTH families together (mixtures)?", f'title_and_abstract.search:{BOTH} AND {LEGACY} AND ("mixture" OR "chemical mixture" OR "co-exposure" OR "exposome")'),
    ]),
    ("Identification — the parity/excretion reverse-causation problem", [
        ("PFAS AND parity / pregnancy as determinant of serum level", f'title_and_abstract.search:{PF} AND ("parity" OR "previous pregnancies" OR "gravidity") AND ("serum" OR "plasma" OR "concentration")'),
        ("PFAS AND breastfeeding / lactation / menstruation as excretion route", f'title_and_abstract.search:{PF} AND ("breastfeeding" OR "lactation" OR "menstruation" OR "elimination" OR "half-life" OR "pharmacokinetic")'),
        ("PFAS AND reverse causation / nulliparous restriction", f'title_and_abstract.search:{PF} AND ("reverse causation" OR "reverse causality" OR "nulliparous" OR "primiparous")'),
        ("occupational / high-exposure community cohorts (C8)", f'title_and_abstract.search:{PF} AND ("C8" OR "occupational" OR "Mid-Ohio Valley" OR "contaminated community" OR "highly exposed")'),
    ]),
    ("Exposure prevalence and trend — the parameter the significance test runs on", [
        ("PFAS serum concentration trends / NHANES / biomonitoring", f'title_and_abstract.search:{PF} AND ("NHANES" OR "biomonitoring" OR "temporal trend" OR "serum concentrations") AND ("population" OR "general population")'),
        ("human microplastic intake / exposure estimate", f'title_and_abstract.search:{MP} AND ("human exposure" OR "dietary intake" OR "ingestion" OR "inhalation") AND ("estimate" OR "assessment")'),
        ("plastic production / PFAS production series", 'title_and_abstract.search:("plastic production" OR "global plastics" OR "fluoropolymer production") AND ("trends" OR "growth" OR "historical")'),
    ]),
    ("Channel 1 — prior systematic reviews and meta-analyses", [
        ("SR/meta — PFAS AND fecundity / fertility", f'title_and_abstract.search:("systematic review" OR "meta-analysis") AND {PF} AND {FERT}'),
        ("SR/meta — microplastics AND human reproduction", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND {MP} AND ("reproductive" OR "fertility" OR "sperm" OR "human health")'),
        ("SR/meta — EDCs AND fertility (the B.2 precedent)", f'title_and_abstract.search:("systematic review" OR "meta-analysis") AND {LEGACY} AND {FERT}'),
    ]),
    ("The sperm-count-decline trend literature (outcome trend, not exposure-outcome)", [
        ("temporal trend in sperm count, meta-analysis", 'title_and_abstract.search:("sperm count" OR "sperm concentration") AND ("temporal trend" OR "temporal trends" OR "decline" OR "secular trend")'),
    ]),
]

# Named candidate works. Several are v5's own seminal list, which is 2025-heavy and was asserted
# without resolution; several are titles this analyst can approximate. The probe reports which
# resolve and to what. Nothing enters the scope document that does not resolve here.
NAMED = [
    # v5's seminal list, as written in HYPOTHESES-v5.md B.6
    "Microplastics in human follicular fluid",
    "Lancet Commission on Reproductive Health",
    "Microplastics detected in human semen and follicular fluid",
    "PFAS exposure placenta trophoblast Shoaito",
    # The detection canon
    "Plasticenta First evidence of microplastics in human placenta",
    "Discovery and quantification of plastic particle pollution in human blood",
    # The PFAS fecundability canon
    "Maternal levels of perfluorinated chemicals and subfecundity",
    "Perfluorinated compounds and subfecundity in pregnant women",
    "Association between perfluorinated compounds and time to pregnancy",
    "Perfluoroalkyl acids and time to pregnancy revisited",
    # Male
    "Do perfluoroalkyl compounds impair human semen quality",
    # Reviews and trend
    "Perfluoroalkyl and polyfluoroalkyl substances and human fetal growth reproductive outcomes systematic review",
    "Temporal trends in sperm count a systematic review and meta-regression analysis",
    # B.2 sibling anchor, as a routing decoy
    "Decline in semen quality among fertile men in Paris during the past 20 years",
]

# Second pass: differently-worded guesses at the same works, plus the works whose existence the
# scope document would most like to assert. A zero here is a statement about wording, not literature.
NAMED_RETRY = [
    "Microplastics in human blood",
    "Detection of microplastics in human seminal fluid",
    "Microplastics in the human placenta",
    "Exposure to perfluoroalkyl substances and fecundability",
    "Perfluorooctanoate and perfluorooctane sulfonate and time to pregnancy",
    "Persistent organic pollutants and couple fecundity",
    "PFAS and female reproductive health a review",
    "Microplastics and human reproductive health a systematic review",
    "Per- and polyfluoroalkyl substances and ovarian reserve",
    "Serum PFAS concentrations and semen parameters young men",
    "Reverse causation in studies of perfluoroalkyl substances and time to pregnancy",
    "Plasma concentrations of perfluoroalkyl substances and parity",
    "Global decline in human sperm counts an updated systematic review",
    "Countdown how our modern world is threatening sperm counts",
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
         "Generated by `source/build/goldset/132_b6_recon_probe.py`. Counts are OpenAlex universe "
         "sizes for the stated filter; listed works are the most-cited within it.", "",
         f"**Requests: {n_req} · failed: {len(errors)} ({share:.0%}) · zero-hit counts below are "
         "therefore genuine absences, not refusals.**", "",
         "Why this exists: B.6 was split out of B.2 in v5 on the claim that the 2020s tissue-detection "
         "literature is a step change. That claim is about a literature, so it is checkable before the "
         "search is designed rather than after. The probe also measures how much of the human "
         "exposure-to-fertility evidence is ART-clinic derived, which is the chapter's structural "
         "selection problem: follicular fluid comes mostly from IVF patients.", ""]

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
          "Titles are approximations, several taken from v5's seminal list and several from this "
          "analyst's memory. What resolves here is what may be carried into the scope document; what "
          "does not resolve is not cited.", ""]
    for t, count, rows in named_results:
        L += [f"### {t}", "", f"n = {count}", ""]
        for r in rows:
            L.append(f"- {r['year']} · {r['cites']:,} cites · {r['title'][:110]}  \n"
                     f"  *{r['venue'][:55]}* · `{r['type']}` · {r['doi'] or '(no DOI)'}")
        L.append("")

    L += ["## Named candidate works — second pass on differently-worded titles", "",
          "**A zero on a title probe is not a zero on a literature.** `title.search` is close to exact, "
          "so an unresolved title says the remembered wording is wrong, which is a different and much "
          "more common failure than the cell being empty. The group probes above are what measure "
          "whether a literature exists; these measure whether a citation can be made.", ""]
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
