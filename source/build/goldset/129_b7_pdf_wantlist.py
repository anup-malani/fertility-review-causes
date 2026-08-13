#!/usr/bin/env python3
"""
129_b7_pdf_wantlist.py — B.7, stage 5 prep. Build the retrieval wantlist and measure the OA ceiling.

Emits the human-facing procurement list and a bare DOI file for bulk tools, and — unlike B.5's
equivalent — checks open-access status LIVE before writing, so the list separates what an automated
fetch can get from what needs a human with a library proxy. B.1 discovered that distinction the
expensive way: its automated ceiling hit 20 of 95 and the pooled estimate has rested on five studies
ever since. Measuring the ceiling before the fetch is cheaper than discovering it after.

Three retrieval jobs, kept apart because they answer different questions and have different failure
costs:

  JOB A — the primary cell (20 records). Needed before extraction; these are the only records whose
          effects enter the extraction table and the only ones that earn GRADE credit.
  JOB B — the held records (5). Need only enough full text to settle a routing question. Two of them
          are held on SPECIES, which a methods section settles in one line.
  JOB C — the parameter and baseline set. These do NOT enter the extraction table and earn no GRADE
          credit, but the demographic-significance computation rests entirely on them, and on this
          hypothesis that computation is better identified than the causal claim it multiplies. Each
          entry names WHICH model input it supplies, because a parameter paper retrieved without
          knowing what it is for tends to be read and not used.

Target paths follow the house convention, `literature/pdfs/{slug}/{WID}__{title-slug}.pdf`, so a file
dropped there is picked up by the ingest stage without renaming. That directory is gitignored.

Output: literature/search-logs/{slug}-pdf-wantlist.md
        extraction/{slug}-retrieval-dois.txt
        extraction/{slug}-oa-status.json
"""
import csv, json, os, re, subprocess, time

SLUG = "antidepressants-ssri-subfecundity"
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

# JOB C, named explicitly by the model input each record supplies.
PARAMETER_SET = [
    ("W4387765683", "p: SSRI treatment prevalence BY AGE AND SEX, US. The core exposure parameter."),
    ("W2169730085", "p: prevalence among women of REPRODUCTIVE AGE specifically."),
    ("W3133243241", "p: PATERNAL preconception prescribing, all births. The male-side exposure."),
    ("W1607894683", "p: NCHS national level, 11% of Americans 12+. Anchors the aggregate."),
    ("W2766203803", "d: LONG- vs SHORT-TERM use. Exposure duration is the deflator on the quantum."),
    ("W2135286485", "d: pregnancy-related DISCONTINUATION. Exposure is endogenous to intention."),
    ("W2092207207", "d: failure to FILL e-prescriptions. Prescription is not ingestion."),
    ("W2258651333", "p: Nordic four-country utilisation with switching."),
    ("W2147227021", "p: Danish women of childbearing age by lifestyle."),
    ("W4402773778", "b: own and PARTNER'S depression -> childlessness. The indication's own effect."),
    ("W4307111698", "b: depression -> likelihood of having children, national register."),
    ("W4412476094", "b: mental disorders -> parity-specific BIRTH RATES. The review's own currency."),
    ("W2168144181", "b: psychiatric first admissions, Norway 1936-1975. PRE-EXPOSURE counterfactual."),
    ("W4397024423", "b: preconception depression -> time to pregnancy, couple-based."),
    ("W2811312432", "t: temperature shocks and DYNAMIC ADJUSTMENT in births. The tempo/quantum template."),
    ("W2034438505", "L3: fecundability as a function of COITAL FREQUENCY. The non-linearity."),
    ("W4244745254", "L3: fecundability, coital frequency and ovum viability."),
    ("W2113109551", "L3: joint model of intercourse BEHAVIOUR and fecundability."),
    ("W2128802284", "L3: MISTIMING rather than frequency as the behavioural cause of failure."),
    ("W2394896331", "L2: THE ONLY link-2 record located. Qualitative, n=9."),
    ("W2061870162", "L1: placebo-controlled randomised ejaculation trial. The link-1 ceiling."),
    ("W2034571536", "L1: HEALTHY MEN, so no indication to confound."),
    ("W2135610977", "L1: psychopathology vs treatment, discerned. Wall 1 at link 1."),
    ("W3192373898", "L1/M: RANDOMISED duloxetine trial with semen endpoints."),
    ("W2005028628", "M: sertraline vs BEHAVIOURAL THERAPY, an active comparator on semen."),
    ("W4220843323", "M: NULL semen result. The publication-bias counterweight."),
    ("W4310093763", "M: confounding by indication in SSRI studies, as a subject."),
    ("W1972388161", "M: duration of SPERMATOGENESIS. Fixes the exposure window semen studies need."),
    ("W2024596918", "M: trial-reported vs systematically-elicited dysfunction incidence."),
    ("W1982922243", "M: interview MODE effects on sensitive self-report."),
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

    job_a = [r for r in gate if r["cell"].startswith("PRIMARY_")]
    job_b = [r for r in gate if not r["cell"].startswith("PRIMARY_")]
    job_c = [(by_id[i], why) for i, why in PARAMETER_SET if i in by_id]
    missing_c = [i for i, _ in PARAMETER_SET if i not in by_id]

    status = {}
    for rows in (job_a, job_b):
        for r in rows:
            if r["doi"]:
                status[r["openalex_id"]] = oa_status(r["doi"])
                time.sleep(0.2)
    for rec, _ in job_c:
        if rec.get("doi"):
            status[rec["id"]] = oa_status(rec["doi"])
            time.sleep(0.2)

    OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}
    def is_open(i):
        return status.get(i, ("closed", None, ""))[0] in OPEN
    def unconfirmed(i):
        return status.get(i, ("closed", None, ""))[0] == "UNCONFIRMED"

    dois = []
    for r in job_a + job_b:
        if r["doi"]:
            dois.append(r["doi"])
    for rec, _ in job_c:
        if rec.get("doi"):
            dois.append(rec["doi"])
    open(OUT_DOI, "w").write("\n".join(dict.fromkeys(dois)) + "\n")
    json.dump({k: {"oa_status": v[0], "pdf_url": v[1], "host": v[2]} for k, v in status.items()},
              open(OUT_OA, "w"), indent=2)

    n_a_open = sum(1 for r in job_a if is_open(r["openalex_id"]))
    n_c_open = sum(1 for rec, _ in job_c if is_open(rec["id"]))
    n_unconf = sum(1 for i in status if unconfirmed(i))

    def row_line(wid, doi, year, title, venue, extra=""):
        st, pdf, host = status.get(wid, ("unchecked", None, ""))
        mark = {"closed": "**CLOSED**", "UNCONFIRMED": "*unconfirmed*"}.get(st, f"open ({st})")
        tgt = f"literature/pdfs/{SLUG}/{wid}__{slugify(title)}.pdf"
        return (f"- **{title[:88]}** ({year}, *{venue[:38]}*)  \n"
                f"  `{doi or 'NO DOI'}` · {mark}{' · ' + host[:34] if host else ''}"
                f"{' · ' + extra if extra else ''}  \n  → `{tgt}`")

    L = [f"# Retrieval wantlist — {SLUG} (B.7)", "",
         "Generated by `source/build/goldset/129_b7_pdf_wantlist.py`. Open-access status is checked "
         "live, so this list states the automated ceiling **before** the fetch rather than after. "
         "B.1's automated retrieval stopped at 20 of 95 and its pooled estimate has rested on five "
         "studies since; the point of measuring first is to know how much of this chapter will "
         "depend on a human with a library proxy.", "",
         f"**Job A (primary cell): {len(job_a)} records, {n_a_open} openly available "
         f"({n_a_open / max(len(job_a), 1):.0%}).**  \n"
         f"**Job B (held for routing): {len(job_b)} records.**  \n"
         f"**Job C (parameter, baseline and link support): {len(job_c)} records, {n_c_open} openly "
         f"available ({n_c_open / max(len(job_c), 1):.0%}).**", "",
         f"{n_unconf} OA checks did not complete and are marked *unconfirmed*. An unconfirmed check "
         "is not a closed record — the two are kept apart here for the same reason the reconnaissance "
         "pass kept failed requests out of its zero counts.", "",
         "## Job A — the primary cell", "",
         "These twenty records are the entire causal evidence base for the chapter. Everything else "
         "in this list supports the demographic-significance computation or the mechanism section "
         "and earns no GRADE credit. Ordered with the identification-bearing designs first.", ""]

    order_a = sorted(job_a, key=lambda r: (0 if "KEY RECORD" in r["screen_note"] else 1,
                                           r["cell"], -(int(r["cited_by"] or 0))))
    for r in order_a:
        L.append(row_line(r["openalex_id"], r["doi"], r["year"], r["title"], r["venue"],
                          f"`{r['cell']}`"))
        if r["screen_note"]:
            L.append(f"  *{r['screen_note'][:190]}*")
    L += ["", "## Job B — held records, routing questions only", "",
          "Full text is needed here to answer one question each, not to extract an effect. Three are "
          "held because the SPECIES could not be established from the visible record, which a methods "
          "section settles in a line; one because the outcome set was not named; one because the "
          "record carried no abstract at all.", ""]
    for r in job_b:
        L.append(row_line(r["openalex_id"], r["doi"], r["year"], r["title"], r["venue"],
                          f"`{r['cell']}`"))
        if r["screen_note"]:
            L.append(f"  *{r['screen_note'][:190]}*")

    L += ["", "## Job C — parameter, baseline, and link support", "",
          "Each line names the model input it supplies. Prefixes: `p` exposure prevalence, `d` "
          "exposure duration, `b` the indication's own fertility effect, `t` the tempo/quantum "
          "template, `L1`/`L2`/`L3` the three links, `M` measurement and design.", ""]
    for rec, why in job_c:
        L.append(row_line(rec["id"], rec.get("doi"), rec.get("year"), rec["title"],
                          rec.get("venue", ""), why))
    if missing_c:
        L += ["", f"**{len(missing_c)} Job C records named here are not in the screened set** "
                  f"({', '.join(missing_c)}). They were named from the screen notes and must be "
                  "re-located before they can be cited.", ""]

    L += ["", "## What retrieval cannot fix", "",
          "The gap in this chapter is not a retrieval gap. Job A holds twenty records and the screen "
          "found no study anywhere in a 6,798-record frame that estimates antidepressant exposure "
          "against a population fertility quantity with a design that separates the medication from "
          "the indication. Retrieving all twenty in full does not change that, and the chapter should "
          "not read as though a successful fetch would. What retrieval decides here is whether the "
          "twenty can be *characterised* precisely enough to say what each one does and does not "
          "identify."]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"job_a={len(job_a)} (open {n_a_open}) job_b={len(job_b)} job_c={len(job_c)} "
          f"(open {n_c_open}) unconfirmed={n_unconf} missing_c={len(missing_c)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")
    print(f"-> {os.path.relpath(OUT_DOI, ROOT)}")


if __name__ == "__main__":
    main()
