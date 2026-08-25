#!/usr/bin/env python3
"""
192_a17_pdf_wantlist.py — A.17, stage 5 prep. Build the retrieval wantlist and measure the OA ceiling.

Inherits `177_a24_pdf_wantlist.py`. Checks open-access status LIVE before writing, so the list states
what an automated fetch can reach and what needs a human with a library proxy BEFORE the fetch rather
than after. B.1 learned that the expensive way: its automated ceiling hit 20 of 95 and its pooled
estimate has rested on five studies ever since.

**THE TRIAGE IS BY CELL AND BY ROLE, AND JOB A1 IS NOT A CELL AT ALL.** A.17's difficulty is not that
its literature is small — the screen returned 192 RELEVANT and 212 UNCERTAIN — but that the records
which decide the chapter's headline number are scattered across cells and share only a role. Arm 1
computes ART's contribution by counting ART births; that count is an upper bound whose tightness is
set entirely by how often untreated or dropped-out subfertile couples conceive anyway. Those records
sit in P4, in OFF_OTHER and in Wall 2's neighbourhood, and no cell filter collects them. So the first
job is assembled by ROLE, from the screen notes.

  A1  THE COUNTERFACTUAL SET. Records measuring what happens to subfertile couples who are NOT
      treated, or who stop: the Walcheren untreated-prognosis study, prediction rules for spontaneous
      live birth, seven-in-ten-achieving-parenthood-by-any-route, the Japanese dropout study, the
      Cameroon matched comparison, clinic-dropout follow-ups, and the compliance meta-analysis. **If
      only one job is retrieved, it is this one.** Everything arm 1 reports is conditional on it.
  A2  ARM 2's IDENTIFIED SET — every P1/P2 record carrying a named policy shock or an identification
      strategy. Israel, Quebec, Ontario, Germany, Australia's two downward shocks, Russia, China, the
      US mandate canon, the ERISA record, the AER structural paper, the price-elasticity experiment,
      and the three IVF-as-instrument papers whose FIRST STAGES are A.17's parameter. An OA failure
      here is not recoverable by any other route.
  A3  ARM 1's SHARE SET — P3 records that actually report a share or a contribution, not the ones
      that merely discuss ART's demographic role.
  A4  P5's CONVERSION SET — the return-rate and outcome records. The elective cell's whole verdict
      turns on how many women who freeze eggs come back for them.
  A5  P6's BEHAVIOUR SIDE — the records with a realized outcome rather than an attitude. The scope
      predicted this cell had none; the screen found several, and they are the difference between
      "unmeasured" and "measured and small".
  B   NO-ABSTRACT records whose TITLE implies an estimate. The screen could not read these and the
      compliance check showed the title-only safeguard did not bind, so retrieval is the only thing
      that can settle them. Selected by rule on the title, not by hand.
  C   EXPOSURE SERIES for stage 10 — the LATEST edition per registry plus the cross-national
      syntheses, not every annual report. The US series alone appears in the frame nine times.
  D   DEPRIORITISED — counted, not retrieved, so the chapter can state what it did not read.

**Read the OA rate BY JOB, never in aggregate.** The correlation is severe here and runs against the
chapter: job A2 is economics — NBER and SSRN working papers are freely available while the published
versions are not, so the OA copy may be a superseded draft (the version-of-record problem in
retrieval form). Job A3 is demography, where Demographic Research is diamond OA and Population and
Development Review is not. Jobs A4 and A5 are clinical, where Human Reproduction is hybrid. An
OA-only evidence base would over-represent whichever arm publishes more openly, and for this chapter
that would mean grading the accounting arm on open demography while the identified access arm stayed
behind a paywall.

Target paths follow the house convention `literature/pdfs/{slug}/{WID}__{title-slug}.pdf`, so a file
dropped there is picked up by ingest without renaming. That directory is gitignored.

Output: literature/search-logs/{slug}-pdf-wantlist.md
        extraction/{slug}-retrieval-dois.txt
        extraction/{slug}-oa-status.json
"""
import json, os, re, subprocess, sys, time
from collections import Counter

SLUG = "art-access-fertility-recovery"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-pdf-wantlist.md")
OUT_DOIS = os.path.join(EXTRACT, f"{SLUG}-retrieval-dois.txt")
OUT_OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}


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
errors = []

# ------------------------------------------------------------------------------------------------
# JOB A1 — the counterfactual set, assembled by ROLE from the screen notes. These ids are written out
# explicitly because no cell filter collects them: they sit in P4, OFF_OTHER and Wall 2's
# neighbourhood, and what they share is that each one measures births among the UNTREATED.
# ------------------------------------------------------------------------------------------------
A1_COUNTERFACTUAL = {
    "W2108883609": "Walcheren: spontaneous pregnancy prognosis in UNTREATED subfertile couples",
    "W2098199441": "Prediction rules for spontaneous pregnancy leading to live birth",
    "W2507139686": "7 of 10 IVF couples reach parenthood via treatment, natural conception OR adoption",
    "W3122787169": "Pregnancy after DROPPING OUT of treatment (Japan)",
    "W2284249410": "IVF vs spontaneous pregnancies, matched (Cameroon)",
    "W2056546771": "Follow-up of couples who dropped out of a specialist clinic",
    "W2081677772": "Parenthood during IVF and after discontinuation of unsuccessful IVF",
    "W2017877508": "Likelihood of natural conception FOLLOWING IVF treatment",
    "W2134032204": "SR/meta of ART compliance (dropout) rates",
    "W2589554180": "SR/meta: ~30% of ART patients never achieve parenthood",
    "W2118329020": "When and why subfertile couples discontinue care",
    "W4415618346": "Time to birth for spontaneous and ART births among infertile groups",
    "W2168108597": "Impact of infertility on family size (US NSFG)",
    "W2133367106": "Does biological fertility predict family size",
}

# JOB A2 — arm 2's identified set. Named policy shocks and identification strategies.
A2_IDENTIFIED = {
    "W2990530582": "Israel 1994 free IVF (AEJ:Applied)",
    "W2564237600": "Israel free IVF, working paper",
    "W3048610328": "Israel free IVF and human capital (EER)",
    "W2314649439": "Quebec public funding of IVF (NEJM)",
    "W2123939717": "Quebec publicly funded IVF, public-health assessment",
    "W2959688822": "Ontario Fertility Program",
    "W1781338173": "Germany's ART reimbursement legislation (a DOWNWARD shock)",
    "W2134649289": "Australia 2010 Medicare cut (DOWNWARD)",
    "W2100587346": "Australia: policy that INCREASED consumer costs (DOWNWARD)",
    "W3115571668": "Russia 2014 IVF in state insurance",
    "W4393989606": "China ART insurance coverage",
    "W1576616858": "Effects of infertility insurance mandates on fertility (J Health Econ)",
    "W2058178715": "Utilization of infertility treatments: effects of mandates (NBER)",
    "W1860640930": "Mandated benefits and utilization/outcomes (NBER)",
    "W1490189814": "Coverage and fertility outcomes: DO WOMEN CATCH UP?",
    "W1532475510": "Mandates and the timing of first birth",
    "W1629559921": "Mandates and the timing of first birth (later version)",
    "W4417321594": "ERISA: 65% of workers in self-insured plans exempt from mandates",
    "W2900454867": "AER 2018 structural: access, costs and treatment dynamics",
    "W4297464366": "Price elasticity and WTP for fertility treatment (DCE)",
    "W2566343964": "AER 2017: IVF as an instrument — FIRST STAGE",
    "W1968875567": "JHR 2008: women seeking fertility services — FIRST STAGE",
    "W2616728500": "J Pop Econ 2017: ART and careers — FIRST STAGE",
    "W4392757101": "Optimal fiscal design of ART policy",
    "W2592668891": "Geographic access to ART in the US",
    "W4296031857": "Residential proximity to a fertility clinic",
    "W2289322072": "Technology diffusion and market structure in treatment markets",
    "W4402844916": "Chain ownership and clinic performance (Management Science)",
    "W2429169488": "Israel: unlimited access, age-specific birth rates UNCHANGED",
    "W3191732024": "Household income and help-seeking (Japan)",
    "W4410089921": "Expanded EMPLOYER fertility benefits",
    "W3203572722": "PDR SR of (quasi-)experimental policy-fertility literature",
    "W4404620034": "SR of global infertility insurance coverage",
}

# JOB A3 — arm 1's share set. Records that report a contribution, not ones that discuss it.
A3_SHARE = {
    "W4412170497": "Italy: MAR = 3.7% of TFR (2025)",
    "W4213230270": "Australia: 6.7% of births MAR-conceived, ART/OI split",
    "W4415582085": "UK: ART and egg donation contribution (Population Studies 2025)",
    "W4383264299": "Czechia: ART contribution to TFR",
    "W4206510889": "Czechia: contribution to future live births",
    "W2888653606": "Ukraine: ~1.6% of births",
    "W2602171676": "US by maternal age (JAMA)",
    "W4319939934": "Projecting contribution to completed cohort fertility",
    "W4408763977": "Conceptualizing and MEASURING ART's contribution (PDR 2025)",
    "W7130356274": "Microsimulation: MAR unlikely to compensate (2026)",
    "W2135954933": "Effect of IVF on birth rates in western countries",
    "W2107328043": "Can ART offset population ageing (Denmark, UK)",
    "W7169859806": "Italy: MAR scenarios to 2050",
    "W4318617808": "Australia: completed family size by mode of conception",
    "W4285727228": "Future of US ART live births",
    "W3024120830": "Norway: demographics of ART births",
    "W4397049710": "Educational gradients in MAR birth prevalence",
    "W4387472984": "Second live birth after first natural vs MAR birth",
    "W2156932756": "US fertility treatment use among women with liveborn infants (ART + non-ART)",
    "W4239265505": "Contribution of NON-ART ovulation stimulation to US singleton births",
    "W2521861472": "Population trends and live birth rates by ART strategy (Australia)",
    "W2067328462": "How effective is ART? A model assessment (Leridon)",
    "W2997596347": "The limits to fertility recuperation",
    "W2070636417": "Donor oocyte cycles, US 2000-2010 (JAMA)",
    "W4390964890": "COVID and US MAR live-birth rates",
}

# JOB A4 — P5's conversion set.
A4_P5 = {
    "W3093135554": "Planned OC 10-15 year follow-up: RETURN RATES",
    "W4280516350": "15 years of autologous oocyte thaw outcomes",
    "W3089922486": "BJOG SR: planned OC cost-efficiency and UTILISATION",
    "W2799699728": "Municipally funded oocyte cryopreservation programme (Japan)",
    "W4404361197": "Elective egg freezing financed by the public system",
    "W2899333608": "Reproductive outcomes after oocyte banking",
    "W4391173061": "Japan nationwide preservation survey with reproductive outcomes",
    "W2899325896": "Deliveries after ovarian tissue cryopreservation",
    "W3200409296": "Oocyte cryopreservation to expand the fertile lifespan",
    "W4414889755": "Scoping review split by MEDICAL and NON-MEDICAL reasons",
    "W3165130013": "Planned OC: outcomes and motivations",
}

# JOB A5 — P6's behaviour side.
A5_P6 = {
    "W4408117139": "8-year follow-up after fertility counselling, FAMILY FORMATION outcome",
    "W2561540476": "FAC clinic: prospective 2-year follow-up of 519 women",
    "W3092390609": "FAC 6-year follow-up",
    "W1845556130": "Perpetual postponers? intentions to SUBSEQUENT BEHAVIOUR (BHPS)",
    "W2977192158": "Declining realisation of reproductive intentions with age",
    "W3217467515": "Austria: late intentions rise, chances of a late birth stay low",
    "W3210979915": "Austria: late fertility intentions and fertility",
    "W2909656495": "Running out of time? clock, intentions and union formation",
    "W4392386985": "Change in the PERCEIVED reproductive age window vs delayed fertility",
    "W4205287346": "FertStart RCT protocol — childbearing among the outcomes",
    "W2187215465": "Information provision against INTENTIONS TO DELAY",
    "W2803748719": "Experimental fertility information: benefits AND costs",
    "W1890972813": "RCT of tailored fertility education",
    "W7160175956": "MAR perceptions and postponement: LIMITED EVIDENCE (EJP 2026)",
    "W2021762768": "A persistent misperception: ART can reverse the aged clock",
    "W2765482846": "Postponement, option value and the biological clock (JET)",
}

JOBS = [("A1_COUNTERFACTUAL", A1_COUNTERFACTUAL, "The counterfactual set — if only one job is retrieved, it is this one"),
        ("A2_IDENTIFIED", A2_IDENTIFIED, "Arm 2's identified set — unrecoverable by any other route if closed"),
        ("A3_SHARE", A3_SHARE, "Arm 1's share set — the records that report a contribution"),
        ("A4_P5_CONVERSION", A4_P5, "P5's conversion set — do frozen eggs become births"),
        ("A5_P6_BEHAVIOUR", A5_P6, "P6's behaviour side — realized outcomes, not attitudes")]

# Rule for JOB B: no abstract, and a title that implies an estimate rather than a description.
B_TITLE_RX = re.compile(
    r"\beffect|\bimpact|\baffect|\bcaus|\bassociat|\bmandate|\bcoverage|\bfunding|\bsubsid"
    r"|contribution|utiliz|utilis|access|elasticit|did .* affect", re.I)

# Rule for JOB C: latest edition per registry family, plus cross-national syntheses.
C_REGISTRY_RX = re.compile(r"icmart|eshre|european registr|european ivf|surveillance|anzard"
                           r"|latin american registry|world report|worldwide trends", re.I)


def oa_lookup(wid):
    url = (f"https://api.openalex.org/works/{wid}?select=id,doi,display_name,publication_year,"
           f"type,open_access,best_oa_location,locations,primary_location&api_key={KEY}")
    try:
        r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
        if r.returncode != 0:
            return {"__err": f"curl exit {r.returncode}"}
        return json.loads(r.stdout)
    except Exception as e:
        return {"__err": str(e)[:120]}


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    screened = json.load(open(SCREENED))
    by_id = {m["id"]: m for m in screened}

    assigned, jobs_of = {}, {}
    for name, ids, _ in JOBS:
        for wid, why in ids.items():
            if wid not in assigned:
                assigned[wid] = why
                jobs_of[wid] = name

    # JOB B — rule-selected, never hand-picked.
    for m in screened:
        if m["id"] in jobs_of:
            continue
        if m.get("no_abstract") and B_TITLE_RX.search(m["title"] or "") \
                and m["screen_verdict"] in ("RELEVANT", "UNCERTAIN"):
            jobs_of[m["id"]] = "B_NO_ABSTRACT"
            assigned[m["id"]] = "no abstract; title implies an estimate"

    # JOB C — exposure series, latest per family.
    series = [m for m in screened if m["screen_cell"] == "EXPOSURE_SERIES"
              and C_REGISTRY_RX.search(m["title"] or "")]
    fams = {}
    for m in series:
        t = (m["title"] or "").lower()
        fam = ("icmart" if "icmart" in t or "world report" in t else
               "eshre" if "eshre" in t or "european" in t else
               "cdc" if "surveillance" in t and "united states" in t else
               "anzard" if "anzard" in t or "australia and new zealand" in t else
               "redlara" if "latin american" in t else "other")
        cur = fams.get(fam)
        if cur is None or (m.get("year") or 0) > (cur.get("year") or 0):
            fams[fam] = m
    for fam, m in fams.items():
        if m["id"] not in jobs_of:
            jobs_of[m["id"]] = "C_EXPOSURE_SERIES"
            assigned[m["id"]] = f"latest edition in the frame for the {fam} series"

    wanted = [by_id[w] for w in jobs_of if w in by_id]
    orphans = [w for w in jobs_of if w not in by_id]

    rows, dois = [], []
    for m in wanted:
        d = oa_lookup(m["id"])
        if "id" not in d:
            errors.append((m["id"], str(d.get("__err") or d)[:120]))
            continue
        oa = d.get("open_access") or {}
        best = d.get("best_oa_location") or {}
        locs = [l for l in (d.get("locations") or []) if l.get("is_oa")]
        rows.append(dict(id=m["id"], job=jobs_of[m["id"]], why=assigned[m["id"]],
                         title=(d.get("display_name") or m["title"])[:110],
                         year=d.get("publication_year"), type=d.get("type"),
                         doi=(d.get("doi") or "").replace("https://doi.org/", "") or None,
                         venue=((d.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
                         is_oa=bool(oa.get("is_oa")), status=oa.get("oa_status"),
                         best_url=best.get("pdf_url") or best.get("landing_page_url"),
                         n_open_locations=len(locs),
                         cell=m["screen_cell"], verdict=m["screen_verdict"], arm=m["screen_arm"]))
        if rows[-1]["doi"]:
            dois.append(rows[-1]["doi"])
        time.sleep(0.15)

    json.dump(rows, open(OUT_OA, "w"), indent=2)
    open(OUT_DOIS, "w").write("\n".join(dois) + "\n")

    pc = lambda a, b: f"{a / max(b, 1):.0%}"
    L = [f"# Stage 5 retrieval wantlist — {SLUG} (A.17)", "",
         f"**{len(rows)} records wanted**, triaged into {len(set(r['job'] for r in rows))} jobs. "
         "Open-access status checked LIVE before this list was written, so the ceiling is stated "
         "before the fetch rather than discovered after it.", "",
         f"**Failed OA lookups: {len(errors)}** — these are UNCONFIRMED, not closed.", ""]
    if orphans:
        L += [f"**{len(orphans)} hand-listed ids are not in the screened worklist and were dropped**: "
              f"{', '.join(orphans)}. A typo in a curated id list is silent otherwise.", ""]

    L += ["## The OA ceiling, by job", "",
          "**Read this table by row, never as a total.** The correlation between job and publishing "
          "venue is severe: job A2 is economics, where NBER and SSRN working papers are open while "
          "the published versions are not — so an open copy may be a superseded draft. Job A3 is "
          "demography, where Demographic Research is diamond OA and Population and Development "
          "Review is not. Jobs A4 and A5 are clinical. An OA-only evidence base would grade the "
          "accounting arm on open demography while the identified access arm stayed closed.", "",
          "| job | n | OA | rate | median open locations | what it is |",
          "|---|---|---|---|---|---|"]
    for name, _, desc in JOBS + [("B_NO_ABSTRACT", {}, "No abstract; title implies an estimate"),
                                 ("C_EXPOSURE_SERIES", {}, "Latest edition per registry family")]:
        grp = [r for r in rows if r["job"] == name]
        if not grp:
            continue
        n_oa = sum(1 for r in grp if r["is_oa"])
        locs = sorted(r["n_open_locations"] for r in grp)
        med = locs[len(locs) // 2] if locs else 0
        L.append(f"| `{name}` | {len(grp)} | {n_oa} | **{pc(n_oa, len(grp))}** | {med} | {desc} |")
    tot_oa = sum(1 for r in rows if r["is_oa"])
    L += [f"| **total** | **{len(rows)}** | **{tot_oa}** | {pc(tot_oa, len(rows))} | | |", "",
          "## OA status mix", "", "| status | n |", "|---|---|"]
    for s, k in Counter(r["status"] for r in rows).most_common():
        L.append(f"| `{s}` | {k} |")

    L += ["", "## The closed records, by job", "",
          "These need a human with a library proxy. They are listed in job order because that is the "
          "order in which their absence damages the chapter.", ""]
    for name, _, _ in JOBS + [("B_NO_ABSTRACT", {}, ""), ("C_EXPOSURE_SERIES", {}, "")]:
        closed = [r for r in rows if r["job"] == name and not r["is_oa"]]
        if not closed:
            continue
        L += [f"### `{name}` — {len(closed)} closed", "",
              "| year | title | venue | DOI |", "|---|---|---|---|"]
        for r in sorted(closed, key=lambda x: -(x["year"] or 0)):
            L.append(f"| {r['year']} | {r['title'].replace('|','/')} | "
                     f"{(r['venue'] or '')[:34].replace('|','/')} | `{r['doi'] or '—'}` |")
        L += [""]

    dep = [m for m in screened if m["id"] not in jobs_of
           and m["screen_verdict"] in ("RELEVANT", "UNCERTAIN")]
    L += ["## Deprioritised, and counted", "",
          f"**{len(dep)} records screened RELEVANT or UNCERTAIN are NOT on this list.** They are "
          "counted here so the chapter can state what it did not read rather than implying it read "
          "everything. By cell:", "",
          "| cell | deprioritised |", "|---|---|"]
    for c, k in Counter(m["screen_cell"] for m in dep).most_common():
        L.append(f"| `{c}` | {k} |")
    L += ["",
          "The largest deprioritised group is P6's ATTITUDE literature, which the screen returned in "
          "volume and which cannot carry a demographic quantity. The chapter's P6 section rests on "
          "job A5 — the records with a realized outcome — and says so.", ""]
    if errors:
        L += ["## Failed OA lookups (UNCONFIRMED, not closed)", ""] + [f"- `{a}`: {b}" for a, b in errors]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"wanted={len(rows)} oa={tot_oa} ({pc(tot_oa, len(rows))}) closed={len(rows)-tot_oa} "
          f"orphans={len(orphans)} errors={len(errors)} deprioritised={len(dep)}")
    for name, _, _ in JOBS:
        grp = [r for r in rows if r["job"] == name]
        if grp:
            print(f"  {name:22} n={len(grp):>3} oa={sum(1 for r in grp if r['is_oa']):>3} "
                  f"({pc(sum(1 for r in grp if r['is_oa']), len(grp))})")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
