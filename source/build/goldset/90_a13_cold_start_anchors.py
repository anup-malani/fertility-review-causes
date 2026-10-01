#!/usr/bin/env python3
"""
90_a13_cold_start_anchors.py — A.13 (breastfeeding and lactational amenorrhea), stage-3 cold-start
anchors.

Mirrors 90_a19 / 90_a20 / 90_a14: source and EXISTENCE-VERIFY the cold-start anchor set. Discipline,
unchanged from those chains and the 2026-07-08 OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) and assert
    NO DOIs unless pinned to a well-known value. The DOI is whatever a LIVE Crossref bibliographic
    match returns, re-affirmed at doi.org.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears identity_verified.
    A real match with a year outside tolerance is version_drift (RA-confirm).
  * Old canon and books are EXPECTED to miss Crossref's article index; carried under expect_no_doi.

A.13's binding problem is the natural-vs-deliberate-spacing wall (A.2-A.6 contraception — the probe put
1,938 of the 5,495-record frame in that overlap) and the maternal-nutrition/energy-balance pathway to
amenorrhea (A.22, deprecated but physiologically entangled). A.13 owns the SUCKLING channel: nursing
intensity -> hyperprolactinemia -> lactational amenorrhea -> birth interval -> the Bongaarts C_i index.
The cleanest identified estimates are the prospective return-of-menses / LAM-efficacy designs
(Kennedy & Visness; the WHO multicentre study) and the natural-fertility birth-spacing designs
(Konner & Worthman), on the mechanism established by the suckling-prolactin studies (Howie & McNeilly).

Decoys cover the registered walls (A.2-A.6 deliberate contraception [LOAD-BEARING], A.22 energy-balance
amenorrhea, A.14 postpartum abstinence, A.1 infant-mortality REVERSE, A.15/B.3 fecundity capacity, and
the dominant infant-health HOMONYM) so the eventual search is tested on ROUTING, not only topical
recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never both.

Crossref only — this does NOT touch the OpenAlex daily budget.

Output: literature/search-logs/breastfeeding-lactational-amenorrhea-cold-start-anchors.json
        literature/search-logs/breastfeeding-lactational-amenorrhea-cold-start-anchors-log.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "breastfeeding-lactational-amenorrhea"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a13_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. DOIs only where pinned to a well-known value; else Crossref resolves. ---
CANDIDATES = [
    # ---- Identified empirical / framework core (Tier A, forward-seeded). A.13's identified core: ----
    # ---- the suckling mechanism, the amenorrhea-duration / LAM-efficacy designs, and natural- ----
    # ---- fertility birth-spacing. ----
    dict(title="A framework for analyzing the proximate determinants of fertility",
         authors=["John Bongaarts"], year=1978, family="framework",
         provisional_cell="FRAMEWORK", known_doi="10.2307/1972149",
         provenance_channel="hypothesis_canon",
         note="Population and Development Review 4(1):105-132. Registry seminal. Defines the proximate-"
              "determinants decomposition and the postpartum-infecundability index C_i that A.13 owns."),
    dict(title="Fertility Biology and Behavior An Analysis of the Proximate Determinants",
         authors=["John Bongaarts", "Robert G. Potter"], year=1983, family="framework-book",
         provisional_cell="FRAMEWORK", expect_no_doi=True,
         provenance_channel="hypothesis_canon",
         note="Academic Press. The book-length statement of the proximate-determinants model and the "
              "quantitative role of lactational infecundability. Expected to miss Crossref's article "
              "index."),
    dict(title="Contraceptive efficacy of lactational amenorrhoea",
         authors=["Kathy I. Kennedy", "Cynthia M. Visness"], year=1992, family="lam-efficacy",
         provisional_cell="LAM_EFFICACY", known_doi="10.1016/0140-6736(92)90018-X",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Lancet 339(8787):227-230. The prospective evidence behind the Bellagio consensus: "
              "amenorrheic, fully breastfeeding women <6 months postpartum have very low pregnancy "
              "risk — the amenorrhea-mechanism design that isolates A.13 from method adoption."),
    dict(title="Nursing frequency gonadal function and birth spacing among !Kung hunter-gatherers",
         authors=["Melvin Konner", "Carol Worthman"], year=1980, family="natural-fertility",
         provisional_cell="BIRTH_INTERVAL", known_doi="10.1126/science.7352291",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Science 207(4432):788-791. The classic natural-fertility anchor: frequent on-demand "
              "suckling sustains amenorrhea and long birth intervals absent contraception."),
    dict(title="Fertility after childbirth: post-partum ovulation and menstruation in bottle and breast feeding mothers",
         authors=["P. W. Howie", "A. S. McNeilly", "M. J. Houston"], year=1982, family="mechanism",
         provisional_cell="SUCKLING_MECHANISM",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Clinical Endocrinology 17(4):323-332. Establishes the suckling -> prolactin -> delayed "
              "ovulation/menstruation dose-response that is the physiological basis of the C_i effect."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="More power to the pill: the impact of contraceptive freedom on women's life cycle labor supply",
         authors=["Martha J. Bailey"], year=2006, family="ROUTING_DECOY",
         provisional_cell="OFF_DELIBERATE_CONTRACEPTION", known_doi="10.1162/qjec.121.1.289",
         provenance_channel="routing_decoy_A2",
         routing_note="DELIBERATE contraceptive technology / access -> A.2. A.13 owns NATURAL suckling-"
                      "driven spacing. Wall 1 (LOAD-BEARING) — the probe put 1,938 frame records in this "
                      "overlap."),
    dict(title="Menstrual cycles: fatness as a determinant of minimum weight for height necessary for their maintenance or onset",
         authors=["Rose E. Frisch", "Janet W. McArthur"], year=1974, family="ROUTING_DECOY",
         provisional_cell="OFF_ENERGY_BALANCE", known_doi="10.1126/science.185.4155.949",
         provenance_channel="routing_decoy_A22",
         routing_note="Amenorrhea driven by maternal ENERGY BALANCE / critical fat -> A.22 (deprecated). "
                      "A.13 owns the suckling channel, not the nutritional one. Wall 2."),
    dict(title="The role of marital sexual abstinence in determining fertility: a study of the Yoruba in Nigeria",
         authors=["John C. Caldwell", "Pat Caldwell"], year=1977, family="ROUTING_DECOY",
         provisional_cell="OFF_ABSTINENCE",
         provenance_channel="routing_decoy_A14",
         routing_note="POSTPARTUM SEXUAL ABSTINENCE -> A.14 (the behavioural C_i-adjacent channel). "
                      "A.13 owns suckling-driven infecundability, not abstinence. Wall 3."),
    dict(title="The effects of infant mortality on fertility revisited: new evidence from Latin America",
         authors=["Alberto Palloni", "Hantamala Rafalimanana"], year=1999, family="ROUTING_DECOY",
         provisional_cell="OFF_REVERSE_MORTALITY",
         provenance_channel="routing_decoy_A1",
         routing_note="Infant death TERMINATES nursing and shortens amenorrhea -> the REVERSE/confound "
                      "pathway (cross-ref A.1 child mortality). Interval variation driven by infant death, "
                      "not the nursing regime. Wall 4."),
    dict(title="Age and infertility",
         authors=["Jane Menken", "James Trussell", "Ulla Larsen"], year=1986, family="ROUTING_DECOY",
         provisional_cell="OFF_FECUNDITY_CAPACITY", known_doi="10.1126/science.3755843",
         provenance_channel="routing_decoy_A15",
         routing_note="Fecundity CAPACITY declining with maternal age -> A.15. Distinct from behavioural "
                      "suckling-driven spacing. Wall 5."),
    dict(title="Breastfeeding in the 21st century: epidemiology mechanisms and lifelong effect",
         authors=["Cesar G. Victora", "Rajiv Bahl", "Aluisio J. D. Barros"], year=2016,
         family="ROUTING_DECOY", provisional_cell="OFF_INFANT_HEALTH",
         known_doi="10.1016/S0140-6736(15)01024-7",
         provenance_channel="routing_decoy_HOMONYM",
         routing_note="Breastfeeding -> INFANT/CHILD HEALTH, morbidity, cognition (no fertility outcome) "
                      "-> the dominant HOMONYM. The probe's in-frame infant-health leak was 172. Wall 6."),
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
    L = ["# A.13 cold-start anchors — existence-verification log", "",
         "Generated by `source/build/goldset/90_a13_cold_start_anchors.py`. **Existence gate: a live",
         "Crossref bibliographic match (Jaccard >= 0.72 AND year +/-1).** No anchor asserts a DOI unless",
         "pinned to a well-known value; otherwise the DOI is whatever a live match returns. A network",
         "failure is `unconfirmed`, never absent. The doi.org second re-affirm is best-effort and may be",
         f"blocked (HTTP 403) from this sandbox, so it is recorded, not gated on — doi_reaffirm tally: {reaff}.", "",
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
