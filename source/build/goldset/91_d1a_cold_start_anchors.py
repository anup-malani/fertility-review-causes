#!/usr/bin/env python3
"""
91_d1a_cold_start_anchors.py — D.1.a, stage A3. Assemble and EXISTENCE-VERIFY the anchor set.

Selection discipline. The candidate keys below are DOIs that the live probes in 89 and 90 returned,
plus a handful from the D.3.b RA-gate CSV (also live-sourced, at screen time). The script LOOKS THEM
UP in those stored probe payloads rather than carrying a hand-typed title or year, because
re-typing a bibliographic record is itself a way to manufacture a ghost. What this file contributes
is the RA JUDGEMENT — which candidate belongs to which pair, which provisional estimand cell, which
design tier, and which are decoys — and nothing else.

Existence gate (mandatory, standing rule from the 2026-07-08 run that found ~40% of the frozen OAS
Tier B was fabricated):
  * doi.org must resolve the identifier live.
  * Crossref must return a record whose title matches the probe title (Jaccard >= 0.72) and whose year
    is within +/-1.
  * Three states, never two: VERIFIED / PARTIAL (id resolves, bibliographic match fails or is absent)
    / GHOST (resolves nowhere). A network failure is UNCONFIRMED and is NOT a ghost.
  * Records with no DOI are KEPT and keyed on title, per the resolution rule. Dropping them would bias
    the recall denominator toward recent, easily found work -- which in this literature means biasing
    it toward SDT framework papers and away from the FDT-era empirical material Ruling 4 admits.

Theory anchors and decoys are carried but flagged: under the GACS Tier-A rule they do NOT count toward
the empirical recall denominator, and the >=30 empirical-anchor cross-validation floor is measured on
the empirical set alone.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import csv, json, os, re, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d1a_crossref_cache.json")

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# key -> (pair, provisional_cell, design_tier, role, note)
# role: EMPIRICAL (counts toward recall) | THEORY | DECOY | CHANNEL1_REVIEW | REVERSE
SELECTION = {
    # ---------- S3 Tier 1: the only material that can support a Moderate rating ----------
    "10.1086/696193": ("S3", "PRIMARY_SECULAR_SHOCK_S3", 1, "EMPIRICAL",
                       "self-described natural experiment; treatment runs toward the religious pole so Ruling 5 flip applies"),
    "10.1016/j.ssresearch.2026.103371": ("S3", "PRIMARY_SECULAR_SHOCK_S3", 1, "EMPIRICAL",
                                         "declining church membership; surfaced by the church-tax probe"),
    "10.1007/s00148-025-01092-5": ("S3", "PRIMARY_SECULAR_SHOCK_S3", 1, "EMPIRICAL",
                                   "religious-leader intervention, Georgia; a dateable discrete shock"),

    # ---------- S3 Tier 2: treatment measured before the outcome ----------
    "10.1007/s10680-015-9371-z": ("S3", "PRIMARY_VALUE_EX_ANTE", 2, "EMPIRICAL", "cohort trends, GB/FR/NL"),
    "10.1007/s10680-009-9185-y": ("S3", "PRIMARY_VALUE_EX_ANTE", 2, "EMPIRICAL", "religious socialisation -> third birth, NL"),
    "10.1002/psp.2433": ("S3", "PRIMARY_VALUE_EX_ANTE", 2, "EMPIRICAL", "realisation of intentions, 8 countries"),
    "10.12765/cpos-2010-02": ("S3", "PRIMARY_VALUE_EX_ANTE", 2, "EMPIRICAL", "East/West German divergence"),
    "10.1007/s11150-007-9011-4": ("S3", "PRIMARY_VALUE_EX_ANTE", 2, "EMPIRICAL", "parental religiosity -> daughters' fertility"),

    # ---------- S3 Tier 3: the topical core ----------
    "10.1111/j.1728-4457.2004.00002.x": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "PDR 2004, the field's most-cited synthesis-style article"),
    "10.1353/sof.0.0000": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "US, role of fertility intentions"),
    "10.2307/2061727": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "Demography 1992"),
    "10.1007/s10680-007-9121-y": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "US vs Europe comparison"),
    "10.4054/demres.2008.18.8": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "affiliation vs religiosity, male and female"),
    "10.1007/s001480050013": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "JPopE 1996, marital fertility"),
    "10.1007/s00148-011-0401-9": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "cultural transmission model plus evidence"),
    "10.1007/s11113-021-09685-0": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "Turkey; separates modernization from secularization"),
    "10.1080/00324728.2014.995695": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "Nepal; outcome is family-size PREFERENCE, check Ruling 2"),
    "10.1111/j.1468-5906.2011.01580.x": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "religious markets"),
    "10.2307/1386953": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "JSSR 1988, explicitly a cautionary methodological note"),
    "10.1016/0162-3095(85)90017-2": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "Mormon status and reproductive success"),

    # ---------- S3 FDT-era, admitted by Ruling 4 ----------
    "10.1515/9781400886692-011": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL",
                                  "Lesthaeghe and Wilson, Princeton EFP chapter reissue -- the FDT anchor Ruling 4 was written for"),
    "10.1007/1-4020-5190-5_5": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "Dutch fertility transition 1845-1945, denominational"),
    "10.1111/j.1533-8525.1986.tb00248.x": ("S3", "PRIMARY_SECULAR_S3", 3, "EMPIRICAL", "historical, urbanization and secularization"),

    # ---------- S1 ----------
    "10.2307/1972499": ("S1", "PRIMARY_POSTMATERIAL_S1", 4, "EMPIRICAL",
                        "Lesthaeghe and Surkyn 1988, a v5 seminal name; 719c; likely Tier 4 on inspection"),
    "10.1111/padr.12490": ("S1", "PRIMARY_POSTMATERIAL_S1", 3, "EMPIRICAL",
                           "empirical horse-race between competing postindustrial accounts -- priority read"),
    "10.1515/zfsoz-1990-0105": ("S1", "PRIMARY_POSTMATERIAL_S1", 3, "EMPIRICAL", "German-language; the language-coverage flag"),
    "10.1080/0032472031000149016": ("S1", "PRIMARY_POSTMATERIAL_S1", 3, "EMPIRICAL", "values and fertility change, Japan"),
    "10.31235/osf.io/uhgnx_v1": ("S1", "PRIMARY_POSTMATERIAL_S1", 3, "EMPIRICAL", "preprint; needs a published-version check"),

    # ---------- S2 ----------
    "10.1257/mac.1.1.146": ("S2", "MIXED_CULTURE_PROXY", 2, "EMPIRICAL",
                            "Fernandez and Fogli 2009, 1242c. WALL 5: routing turns on proxy content, read at full text before assigning"),
    "10.1016/b978-0-444-53187-2.00011-5": ("S2", "SDT_FRAMEWORK_THEORY", None, "THEORY", "Fernandez, Does Culture Matter? survey"),
    "10.1016/j.worlddev.2019.104627": ("S2", "OFF_OUTCOME", None, "DECOY",
                                       "individualism instrumented, but outcome is gender equality -- OFF_OUTCOME, kept as an instrument source"),

    # ---------- S5 ----------
    "10.1007/s11205-010-9665-9": ("S5", "PRIMARY_CONSUMERISM_S5", 3, "EMPIRICAL",
                                  "uses materialism in the consumer-psychology sense -- the polysemic pole"),
    "10.1525/sop.2010.53.2.179": ("S5", "PRIMARY_CONSUMERISM_S5", 3, "EMPIRICAL", "six-country attitudes toward marriage and children"),

    # ---------- Theory canon (channel 2). Does NOT count toward empirical recall. ----------
    "10.1146/annurev-soc-060116-053442": ("ALL", "SDT_FRAMEWORK_THEORY", None, "THEORY", "Zaidi and Morgan, the critical appraisal"),
    "10.1186/s41118-020-00077-4": ("ALL", "SDT_FRAMEWORK_THEORY", None, "THEORY", "Lesthaeghe 2020 Genus retrospective"),
    "10.1073/pnas.1420441111": ("ALL", "SDT_FRAMEWORK_THEORY", None, "THEORY", "Lesthaeghe 2014 PNAS overview; from the D.3.b inbound queue"),

    # ---------- Channel-1 reviews (regional, S3 only) ----------
    "10.29063/ajrh2023/v27i1.11": ("S3", "SDT_FRAMEWORK_THEORY", None, "CHANNEL1_REVIEW", "sub-Saharan Africa review of publications"),
    "10.31237/osf.io/sezdq": ("S3", "SDT_FRAMEWORK_THEORY", None, "CHANNEL1_REVIEW", "sub-Saharan Africa; preprint, needs published-version check"),

    # ---------- REVERSE: sizes the binding risk-of-bias threat ----------
    "10.1093/esr/jcac060": ("S3", "REVERSE", None, "REVERSE",
                            "family formation -> religiosity, BHPS. Carries no effect estimate for this chapter and measures threat 1"),

    # ---------- Routing decoys: the anchor set must test routing, not only topical recall ----------
    "10.1162/qjec.2009.124.3.1057": ("DECOY", "OFF_CHANNEL_A20", None, "DECOY", "Jensen and Oster, cable TV -- A.20 by treatment"),
    "10.1111/jeea.12181": ("DECOY", "OFF_CHANNEL_A20", None, "DECOY", "mass media and social change -- A.20"),
    "10.1111/j.0022-2445.2004.00086.x": ("DECOY", "OFF_CHANNEL_A20", None, "DECOY", "new ideas and fertility limitation via mass media -- A.20"),
    "10.1093/esr/jcv002": ("DECOY", "OFF_GENDER_D2a", None, "DECOY", "gender-role attitudes -> fertility -- D.2.a"),
    "10.1186/s41118-021-00126-6": ("DECOY", "OFF_GENDER_D2a", None, "DECOY", "gender-role attitudes and intentions -- D.2.a"),
    "10.4054/demres.2024.50.21": ("DECOY", "OFF_CONTRACEPTIVE_ATTITUDE_A3_A6", None, "DECOY", "religion -> contraceptive USE, not fertility -- A.6 / OFF_OUTCOME"),
    "10.2307/1966780": ("DECOY", "OFF_CONTRACEPTIVE_ATTITUDE_A3_A6", None, "DECOY", "religious factors -> contraceptive use -- A.6"),
    "10.1111/ecin.70041": ("DECOY", "OFF_OTHER", None, "DECOY",
                           "treatment is maternity benefits with religion as moderator -- C.2.d by treatment; a clean Wall 7 test"),
    "10.1080/13229400.2025.2450030": ("S4", "NORM_ACCEPTABILITY_DESCRIPTIVE", None, "DECOY",
                                      "'Postmaterialism and voluntary childlessness'; from the D.3.b queue. A direct Ruling 2 test"),
}


# --------------------------------------------------------------------------- helpers
def norm_title(t):
    t = re.sub(r"<[^>]+>", " ", t or "").lower()
    return set(re.findall(r"[a-z0-9]+", t))


def jaccard(a, b):
    A, B = norm_title(a), norm_title(b)
    return len(A & B) / len(A | B) if A and B else 0.0


def load_probe_records():
    """Every bibliographic field comes from stored LIVE probe output, never from this file."""
    recs = {}
    for fn in ("channel1-probe.json", "tier1-design-probe.json"):
        p = os.path.join(TMP, fn)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        pools = []
        if "pairs" in d:
            for rec in d["pairs"].values():
                for fr in rec["forms"].values():
                    pools.extend(fr.get("hits", []))
        pools.extend(d.get("union", []))
        for pid, rec in d.get("probes", {}).items():
            pools.extend(rec.get("hits", []))
        for h in pools:
            if h.get("doi"):
                recs.setdefault(h["doi"], h)
    # D.3.b RA-gate CSV: also live-sourced (at D.3.b screen time), used for the inbound queue records.
    gate = os.path.join(ROOT, "extraction", "climate-anxiety-eco-doomerism-ra-gate.csv")
    if os.path.exists(gate):
        for row in csv.DictReader(open(gate)):
            doi = (row.get("doi") or "").strip()
            if doi and doi not in recs:
                recs[doi] = {"doi": doi, "title": row.get("title", ""),
                             "year": int(row["year"]) if (row.get("year") or "").isdigit() else None,
                             "venue": row.get("venue", ""), "cited_by": None, "authors": [],
                             "work_id": row.get("work_id", ""), "source": "d3b_ra_gate"}
    return recs


cache = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}


def openalex_by_doi(doi):
    """Live OpenAlex lookup for a selected DOI absent from the stored probe payloads.

    REPRODUCIBILITY GAP FOUND 2026-08-03. Ten of the selected anchors were first seen in ad-hoc
    interactive probes run at the terminal rather than in 89 or 90, so they existed in the session
    transcript and nowhere a script could read. That is a silent dependence on a human's scrollback,
    and it would have made this anchor set unreproducible from the repo alone. Fixed by fetching the
    record live here: bibliographic fields still come from the API, never from a hand-typed literal.
    """
    key = f"oa2::{doi}"
    if key in cache:
        return cache[key]
    url = ("https://api.openalex.org/works/https://doi.org/"
           + urllib.parse.quote(doi) + f"?mailto={MAILTO}")
    for _ in range(3):
        out = subprocess.run(["curl", "-s", "-m", "40", "-A", UA, url], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip().startswith("{"):
            try:
                w = json.loads(out.stdout)
            except Exception:  # noqa: BLE001
                break
            if w.get("id"):
                s = (w.get("primary_location") or {}).get("source") or {}
                ids = w.get("ids") or {}
                rec = {"doi": doi, "title": w.get("title") or "",
                       "pmid": (ids.get("pmid") or "").rsplit("/", 1)[-1] or None,
                       "year": w.get("publication_year"), "type": w.get("type"),
                       "venue": s.get("display_name") or "",
                       "cited_by": w.get("cited_by_count"),
                       "work_id": (w.get("id") or "").rsplit("/", 1)[-1],
                       "source": "openalex_direct_lookup"}
                cache[key] = rec
                return rec
        time.sleep(2)
    return None


def doi_resolves(doi):
    """Ask doi.org whether the identifier is REGISTERED. Do not follow the redirect.

    BUG FOUND AND FIXED 2026-08-03, first run of this script. The original check used `curl -I -L`,
    which follows doi.org's 302 through to the publisher's page -- and Annual Reviews, the AEA, Oxford
    University Press and Wiley all answer an automated request with **403**. The gate read those 403s
    as non-existence and reported **24 of 45 anchors as GHOSTS**, including Zaidi and Morgan 2017 and
    Fernandez and Fogli 2009, both of which had been confirmed live by OpenAlex an hour earlier.

    The test that is actually wanted is whether doi.org KNOWS the identifier: a 301/302 means
    registered, a 404 means unknown. Publisher-side bot blocking is not evidence about a paper's
    existence, and conflating the two produces false ghosts in exactly the direction that looks like
    diligence. Same class of error as the C.2.c run's "my first Crossref probe returned nothing and it
    looked like a ghost; the query string was simply wrong."
    """
    key = f"resolve2::{doi}"
    if key in cache:
        return cache[key]
    for _ in range(3):
        out = subprocess.run(["curl", "-s", "-I", "-o", "/dev/null", "-w", "%{http_code}",
                              "-m", "30", "-A", UA, f"https://doi.org/{doi}"],
                             capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip().isdigit():
            code = int(out.stdout.strip())
            if code:
                cache[key] = code
                return code
        time.sleep(2)
    return None


def crossref(doi):
    key = f"cr::{doi}"
    if key in cache:
        return cache[key]
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    for _ in range(3):
        out = subprocess.run(["curl", "-s", "-m", "40", "-A", UA, url], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip().startswith("{"):
            try:
                m = json.loads(out.stdout)["message"]
            except Exception:  # noqa: BLE001
                break
            dp = (m.get("issued") or {}).get("date-parts") or [[None]]
            res = {"title": (m.get("title") or [""])[0],
                   "year": dp[0][0] if dp and dp[0] else None,
                   "container": (m.get("container-title") or [""])[0],
                   "type": m.get("type")}
            cache[key] = res
            return res
        time.sleep(2)
    return None


def main():
    probe = load_probe_records()
    anchors, missing = [], []
    for doi, (pair, cell, tier, role, note) in SELECTION.items():
        rec = probe.get(doi) or openalex_by_doi(doi)
        if rec is None:
            missing.append(doi)
            continue
        code = doi_resolves(doi)
        cr = crossref(doi)
        # THREE independent existence witnesses: a registered DOI (301/302 from doi.org), a live
        # Crossref record, and a PubMed identifier carried on the OpenAlex record. GHOST requires ALL
        # THREE to fail. Any one alone is sufficient evidence that the paper is real, which is what
        # stops publisher bot-blocking and unregistered DOIs from manufacturing ghosts.
        #
        # PMID was added after the second run false-ghosted "Human fertility and religions in
        # sub-Saharan Africa" (Afr J Reprod Health 2023). The paper is real and carries PMID 37584963;
        # its DOI is simply not registered with Crossref. That is the resolution rule's "dead or drifted
        # identifier" case -- KEEP, keyed on title -- and not the fabricated-title case. The blind spot
        # is systematic rather than incidental: a Crossref-plus-doi.org gate false-ghosts journals
        # outside the Anglo-European publishing infrastructure, so it would have thinned the anchor set
        # in exactly the direction this chapter's geographic-skew limitation already runs.
        registered = code is not None and code < 400
        pmid = (rec.get("pmid") or "") or None
        if pmid is None and rec.get("source") != "d3b_ra_gate":
            oa = openalex_by_doi(doi) or {}
            pmid = oa.get("pmid")
        if code is None and cr is None and not pmid:
            status, why = "UNCONFIRMED", "neither doi.org nor Crossref answered (transport, not absence)"
        elif not registered and cr is None and not pmid:
            status, why = "GHOST", f"doi.org returned {code}, Crossref has no record, no PMID"
        elif not registered and cr is None and pmid:
            status, why = f"VERIFIED_TITLE_KEYED", (
                f"doi.org returned {code} and Crossref has no record, but PubMed carries it "
                f"({pmid}). Real paper, unregistered identifier -- kept and keyed on title.")
        elif cr is None:
            status, why = "PARTIAL", f"doi.org {code} (registered); Crossref returned no record"
        elif not registered:
            status, why = "PARTIAL", f"Crossref has a record but doi.org returned {code}"
        else:
            j = jaccard(rec.get("title", ""), cr["title"])
            yr_ok = (rec.get("year") is None or cr["year"] is None
                     or abs(rec["year"] - cr["year"]) <= YEAR_TOL)
            if j >= TITLE_JACCARD_MIN and yr_ok:
                status, why = "VERIFIED", f"doi.org {code}; Crossref title J={j:.2f}, year ok"
            else:
                status, why = "PARTIAL", f"doi.org {code}; Crossref J={j:.2f}, year_ok={yr_ok}"
        anchors.append({"doi": doi, "pair": pair, "provisional_cell": cell, "design_tier": tier,
                        "role": role, "rа_note": note, "title": rec.get("title"),
                        "year": rec.get("year"), "venue": rec.get("venue"),
                        "cited_by": rec.get("cited_by"), "work_id": rec.get("work_id"),
                        "identity_status": status, "identity_evidence": why,
                        "crossref_title": (cr or {}).get("title"),
                        "crossref_container": (cr or {}).get("container")})
        print(f"{status:12s} {doi:45s} {(rec.get('title') or '')[:52]}", file=sys.stderr)
        time.sleep(0.25)

    json.dump(cache, open(CACHE_PATH, "w"), indent=1)

    emp = [a for a in anchors if a["role"] == "EMPIRICAL"]
    emp_ok = [a for a in emp if a["identity_status"] == "VERIFIED"]
    by_status = {}
    for a in anchors:
        by_status[a["identity_status"]] = by_status.get(a["identity_status"], 0) + 1

    out = {"slug": SLUG, "built": "2026-08-03", "gate": "doi.org + Crossref title/year match",
           "title_jaccard_min": TITLE_JACCARD_MIN, "year_tol": YEAR_TOL,
           "counts": {"selected": len(SELECTION), "resolved_from_probe": len(anchors),
                      "not_found_in_probe_payloads": missing, "by_status": by_status,
                      "empirical_total": len(emp), "empirical_verified": len(emp_ok),
                      "cv_floor": 30, "floor_cleared": len(emp_ok) >= 30},
           "anchors": anchors}
    json.dump(out, open(OUT_JSON, "w"), indent=1)

    L = [f"# D.1.a cold-start anchor set — existence-gate results", "",
         f"Built 2026-08-03 by `91_d1a_cold_start_anchors.py`. Gate: doi.org resolution plus a Crossref",
         f"title match (Jaccard >= {TITLE_JACCARD_MIN}) and year within +/-{YEAR_TOL}.", "",
         f"- selected: **{len(SELECTION)}**",
         f"- verified: **{by_status.get('VERIFIED', 0)}** | partial: {by_status.get('PARTIAL', 0)} | "
         f"ghost: {by_status.get('GHOST', 0)} | unconfirmed: {by_status.get('UNCONFIRMED', 0)}",
         f"- **empirical anchors verified: {len(emp_ok)}** against the >=30 cross-validation floor — "
         f"{'CLEARED' if len(emp_ok) >= 30 else 'NOT CLEARED'}", ""]
    if missing:
        L += ["Selected but absent from the stored probe payloads (needs a targeted probe): "
              + ", ".join(f"`{m}`" for m in missing), ""]
    for role in ("EMPIRICAL", "REVERSE", "CHANNEL1_REVIEW", "THEORY", "DECOY"):
        rows = [a for a in anchors if a["role"] == role]
        if not rows:
            continue
        L += [f"## {role} ({len(rows)})", "",
              "| status | pair | tier | cell | year | title | DOI |", "|---|---|---|---|---|---|---|"]
        for a in sorted(rows, key=lambda x: (x["pair"], x["design_tier"] or 9)):
            t = (a["title"] or "")[:70].replace("|", "/")
            L.append(f"| {a['identity_status']} | {a['pair']} | {a['design_tier'] or '-'} | "
                     f"{a['provisional_cell']} | {a['year']} | {t} | `{a['doi']}` |")
        L.append("")
    open(OUT_LOG, "w").write("\n".join(L))
    print(f"\nempirical verified={len(emp_ok)} / floor 30\nwrote {OUT_JSON}\nwrote {OUT_LOG}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
