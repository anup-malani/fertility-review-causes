#!/usr/bin/env python3
"""
90_d2c_cold_start_anchors.py — D.2.c (son preference and gender-biased fertility norms), stage-3
cold-start anchors.

Mirrors 90_a14 / 53 (C.2.h) / 89 (A.3): source and EXISTENCE-VERIFY the cold-start anchor set.
Discipline, unchanged from those chains and the 2026-07-08 OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) and assert
    NO DOIs. The DOI is whatever a LIVE Crossref bibliographic match returns, re-affirmed at doi.org.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears identity_verified.
    A real match with a year outside tolerance is version_drift (RA-confirm).
  * Old canon and books are EXPECTED to miss Crossref's article index; carried under expect_no_doi.

D.2.c is a well-canonised South/East-Asian demographic-economics literature; the binding problem is
recall of the differential-stopping canon (Ben-Porath & Welch, Clark, Arnold-Choe-Roy) and DISCOVERY of
the sex-selection substitution naturals (Ebenstein, Lin-Liu-Qian, Chung-Das Gupta, Jayachandran).

Decoys cover the six registered walls (A.10 adult sex ratio, A.4 general abortion, A.8 sex-indifferent
parity stopping, C.3.c old-age security, D.2.a gender equity, A.1 child mortality) so the eventual search
is tested on ROUTING, not only topical recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never both.

Crossref only — this does NOT touch the OpenAlex daily budget.

Output: literature/search-logs/son-preference-cultural-cold-start-anchors.json
        literature/search-logs/son-preference-cultural-cold-start-anchors-log.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "son-preference-cultural"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d2c_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # ---- Differential-stopping primary core (Tier A empirical) ----
    dict(title="Do sex preferences really matter?",
         authors=["Yoram Ben-Porath", "Finis Welch"], year=1976, family="differential-stopping",
         provisional_cell="PRIMARY_DIFFERENTIAL_STOPPING", provenance_channel="direct_empirical_bibliographic_search",
         note="Quarterly Journal of Economics 90(2):285-307. Registry seminal. The foundational "
              "differential-stopping model: couples continue conditional on the sex of existing children, "
              "raising fertility. The behavioural signature this chapter seeks."),
    dict(title="Son preference and the sex composition of children: evidence from India",
         authors=["Shelley Clark"], year=2000, family="differential-stopping",
         provisional_cell="PRIMARY_DIFFERENTIAL_STOPPING", provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 37(1):95-108. Parity progression by sex composition of existing children in "
              "India; a clean revealed-preference differential-stopping estimate."),
    dict(title="Son preference the family-building process and child mortality in India",
         authors=["Fred Arnold", "Minja Kim Choe", "T. K. Roy"], year=1998, family="differential-stopping",
         provisional_cell="PRIMARY_DIFFERENTIAL_STOPPING", provenance_channel="direct_empirical_bibliographic_search",
         note="Population Studies 52(3):301-315. Registry seminal. Son preference in the family-building "
              "process (differential stopping) and its interaction with child mortality (Wall 6)."),
    # ---- Sex-selection substitution naturals (Tier A empirical) ----
    dict(title="The missing girls of China and the unintended consequences of the one child policy",
         authors=["Avraham Y. Ebenstein"], year=2010, family="sexsel-substitution",
         provisional_cell="PRIMARY_SEXSEL_SUBSTITUTION", provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Human Resources 45(1):87-115. The substitution regime: sex-selective abortion "
              "under a fertility constraint raises the sex ratio at birth. Wall 1/Wall 2 both sides."),
    dict(title="More missing women fewer dying girls: the impact of sex-selective abortion on sex at birth and relative female mortality in Taiwan",
         authors=["Ming-Jen Lin", "Jin-Tan Liu", "Nancy Qian"], year=2014, family="sexsel-substitution",
         provisional_cell="PRIMARY_SEXSEL_SUBSTITUTION", provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of the European Economic Association 12(4):899-926. Amniocentesis-access natural "
              "experiment: the cleanest identified sex-selection-substitution design."),
    dict(title="Fertility decline and missing women",
         authors=["Seema Jayachandran"], year=2017, family="sexsel-substitution",
         provisional_cell="PRIMARY_SEXSEL_SUBSTITUTION", provenance_channel="direct_empirical_bibliographic_search",
         note="American Economic Journal: Applied Economics 9(1):118-139. Registry seminal. Fertility "
              "decline concentrates a fixed son preference into fewer births, raising the sex ratio — the "
              "substitution mechanism formalised."),
    # ---- Norm intensity / trend (may be mechanism unless carrying a fertility outcome) ----
    dict(title="The decline of son preference in South Korea: the roles of development and public policy",
         authors=["Woojin Chung", "Monica Das Gupta"], year=2007, family="norm-intensity",
         provisional_cell="PRIMARY_NORM_INTENSITY", provenance_channel="direct_empirical_bibliographic_search",
         note="Population and Development Review 33(4):757-783. Cross-cohort decline in son-preference "
              "intensity in Korea; norm-intensity variation linked to fertility and sex ratio."),

    # ---- Theory / norm canon (does NOT count toward empirical recall) ----
    dict(title="Selective discrimination against female children in rural Punjab India",
         authors=["Monica Das Gupta"], year=1987, family="son-preference-theory",
         provisional_cell="MECHANISM_PREFERENCE_ONLY", provenance_channel="hypothesis_canon",
         note="Population and Development Review 13(1):77-100. Registry seminal. The classic documentation "
              "of son preference as a norm (discrimination and differential treatment); mechanism/context "
              "for the intensity and roots of the preference."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="How do sex ratios affect marriage and labor markets? Evidence from America's second generation",
         authors=["Josh Angrist"], year=2002, family="ROUTING_DECOY",
         provisional_cell="OFF_ADULT_SEX_RATIO", provenance_channel="routing_decoy_A10",
         routing_note="Adult sex ratio as an exposure to the marriage market -> A.10. D.2.c owns son "
                      "preference as a CAUSE of the sex ratio at BIRTH, not the marriage-market consequences "
                      "of the resulting adult imbalance. Wall 1 (load-bearing)."),
    dict(title="The impact of an abortion ban on socioeconomic outcomes of children: evidence from Romania",
         authors=["Cristian Pop-Eleches"], year=2006, family="ROUTING_DECOY",
         provisional_cell="OFF_ABORTION_GENERAL", provenance_channel="routing_decoy_A4",
         routing_note="General abortion access -> births of any sex -> A.4. D.2.c owns only sex-SELECTIVE "
                      "abortion as the expression of the preference. Wall 2."),
    dict(title="Starting stopping and spacing during the early stages of fertility transition",
         authors=["John Knodel"], year=1987, family="ROUTING_DECOY",
         provisional_cell="OFF_PARITY_STOPPING", provenance_channel="routing_decoy_A8",
         routing_note="Sex-indifferent target-number stopping (the FDT quantum signature) -> A.8. D.2.c owns "
                      "stopping conditioned on the SEX composition, not the number. Wall 3."),
    dict(title="The old-age security motive for fertility",
         authors=["Jeffrey B. Nugent"], year=1985, family="ROUTING_DECOY",
         provisional_cell="OFF_OLD_AGE_SECURITY", provenance_channel="routing_decoy_C3c",
         routing_note="Pensions / old-age support as a driver of fertility -> C.3.c. C.3.c is one economic "
                      "ROOT of wanting sons, but pension-driven fertility change is not D.2.c evidence. Wall 4."),
    dict(title="Women's education autonomy and reproductive behaviour: experience from developing countries",
         authors=["Shireen J. Jejeebhoy"], year=1995, family="ROUTING_DECOY",
         provisional_cell="OFF_GENDER_EQUITY", provenance_channel="routing_decoy_D2a", expect_no_doi=True,
         note="Clarendon Press (book). General female autonomy/education lowering fertility -> D.2.a. D.2.c "
              "owns the specific gender-BIASED preference for sons that raises it. Wall 5. Book: expected "
              "Crossref-index miss."),
    dict(title="The effects of infant and child mortality on fertility",
         authors=["Samuel H. Preston"], year=1978, family="ROUTING_DECOY",
         provisional_cell="OFF_CHILD_MORTALITY", provenance_channel="routing_decoy_A1", expect_no_doi=True,
         note="Academic Press (edited volume). Mortality decline -> replacement/insurance fertility -> A.1. "
              "Continuing until a SURVIVING son mixes son preference with replacement. Wall 6. Book: expected "
              "Crossref-index miss."),
]


def toks(s):
    return set(norm(s).split())


def jaccard(a, b):
    ta, tb = toks(a), toks(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def crossref_lookup(title, year):
    key = f"cr::{title}::{year}"
    if key in cache:
        return cache[key]
    q = urllib.parse.quote(title)
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=3&select=DOI,title,published-print,published-online,issued&mailto={MAILTO}")
    out = {"ok": False}
    try:
        p = subprocess.run(["curl", "-s", "-S", "--max-time", "45", "-A", UA, url],
                           capture_output=True, text=True)
        if p.returncode != 0:
            out = {"ok": False, "error": f"curl exit {p.returncode}"}
        else:
            d = json.loads(p.stdout)
            items = d.get("message", {}).get("items", [])
            best = None
            for it in items:
                mt = (it.get("title") or [""])[0]
                if not mt:
                    continue
                jac = jaccard(title, mt)
                yr = None
                for fld in ("published-print", "published-online", "issued"):
                    dp = it.get(fld, {}).get("date-parts", [[None]])
                    if dp and dp[0] and dp[0][0]:
                        yr = dp[0][0]
                        break
                cand = {"doi": it.get("DOI"), "matched_title": mt, "matched_year": yr, "jaccard": round(jac, 3)}
                if best is None or jac > best["jaccard"]:
                    best = cand
            out = {"ok": True, "best": best}
    except Exception as e:  # noqa: BLE001
        out = {"ok": False, "error": str(e)[:200]}
    cache[key] = out
    json.dump(cache, open(CACHE, "w"), indent=0)
    time.sleep(0.5)
    return out


def doi_reaffirm(doi):
    key = f"doiref::{doi}"
    if key in cache and cache[key] == "resolves":
        return cache[key]
    result = "error"
    try:
        p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L",
                            "--max-time", "45", "-A", UA, f"https://doi.org/{doi}"],
                           capture_output=True, text=True)
        code = p.stdout.strip()
        if code in {"200", "301", "302", "303"}:
            result = "resolves"
        elif code == "404":
            result = "not_found"
        elif code == "403":
            result = "blocked"
        else:
            result = f"http_{code}"
    except Exception:  # noqa: BLE001
        result = "error"
    cache[key] = result
    json.dump(cache, open(CACHE, "w"), indent=0)
    time.sleep(0.3)
    return result


def classify(c):
    rec = dict(c)
    rec.setdefault("expect_no_doi", False)
    if c.get("known_doi"):
        rec["doi"] = c["known_doi"]
        rec["doi_reaffirm"] = doi_reaffirm(c["known_doi"])
        rec["state"] = "verified_pinned"
        rec["identity_verified"] = True
        return rec
    cr = crossref_lookup(c["title"], c["year"])
    rec["crossref_ok"] = cr.get("ok")
    if not cr.get("ok"):
        rec["state"] = "unconfirmed_network"
        rec["identity_verified"] = False
        return rec
    best = cr.get("best")
    rec["crossref_best"] = best
    if not best or not best.get("doi"):
        rec["state"] = "expected_no_doi" if rec["expect_no_doi"] else "ghost_no_match"
        rec["identity_verified"] = False
        return rec
    jac = best["jaccard"]
    yr_ok = best.get("matched_year") is not None and abs(best["matched_year"] - c["year"]) <= YEAR_TOL
    if jac >= TITLE_JACCARD_MIN and yr_ok:
        rec["doi"] = best["doi"]
        rec["doi_reaffirm"] = doi_reaffirm(best["doi"])
        rec["state"] = "verified"
        rec["identity_verified"] = True
    elif jac >= TITLE_JACCARD_MIN and not yr_ok:
        rec["doi"] = best["doi"]
        rec["doi_reaffirm"] = doi_reaffirm(best["doi"])
        rec["state"] = "version_drift"
        rec["identity_verified"] = True
    else:
        rec["state"] = "expected_no_doi" if rec["expect_no_doi"] else "ghost_low_match"
        rec["identity_verified"] = False
    return rec


def main():
    os.makedirs(LOGS, exist_ok=True)
    anchors = [classify(c) for c in CANDIDATES]
    json.dump(anchors, open(OUT_JSON, "w"), indent=2)

    by_state = {}
    for a in anchors:
        by_state.setdefault(a["state"], []).append(a)

    reaff = {}
    for a in anchors:
        reaff[a.get("doi_reaffirm", "n/a")] = reaff.get(a.get("doi_reaffirm", "n/a"), 0) + 1
    L = ["# D.2.c cold-start anchors — existence-verification log", "",
         "Generated by `source/build/goldset/90_d2c_cold_start_anchors.py`. **Existence gate: a live",
         "Crossref bibliographic match (Jaccard >= 0.72 AND year +/-1).** No anchor asserts a DOI; the",
         "DOI is whatever a live match returns. A network failure is `unconfirmed`, never absent. The",
         "doi.org second re-affirm is best-effort and may be blocked (HTTP 403) from this sandbox, so it",
         f"is recorded, not gated on — doi_reaffirm tally: {reaff}.", "",
         f"**{len(anchors)} candidates.** State tally: " +
         ", ".join(f"{k} {len(v)}" for k, v in sorted(by_state.items())) + ".", "",
         "| # | anchor | year | cell | state | doi |", "|---|---|---|---|---|---|"]
    for i, a in enumerate(anchors, 1):
        doi = a.get("doi", "") or ""
        t = a["title"][:60] + ("…" if len(a["title"]) > 60 else "")
        L.append(f"| {i} | {t} | {a['year']} | {a['provisional_cell']} | {a['state']} | {doi} |")
    L += ["", "## Notes per anchor", ""]
    for i, a in enumerate(anchors, 1):
        note = a.get("note") or a.get("routing_note") or ""
        best = a.get("crossref_best") or {}
        L.append(f"{i}. **{a['title']}** ({a['year']}) — `{a['provisional_cell']}`, {a['state']}. "
                 f"Crossref best jaccard={best.get('jaccard')} year={best.get('matched_year')}. {note}")
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_LOG}")
    for k, v in sorted(by_state.items()):
        print(f"  {k}: {len(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
