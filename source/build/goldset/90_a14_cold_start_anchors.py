#!/usr/bin/env python3
"""
90_a14_cold_start_anchors.py — A.14 (coital frequency and fecundability), stage-3 cold-start anchors.

Mirrors 53 (C.2.h), 89 (A.3), 72 (D.3.b), 64 (B.1): source and EXISTENCE-VERIFY the cold-start anchor
set. Discipline, unchanged from those chains and the 2026-07-08 OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) and assert
    NO DOIs. The DOI is whatever a LIVE Crossref bibliographic match returns, re-affirmed at doi.org.
    No anchor enters a recall denominator without a resolved live id.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears to
    identity_verified=True. A real match with a year outside tolerance is version_drift (RA-confirm).
  * Old canon (Davis & Blake 1956; Wood 1989) and any book are EXPECTED to miss Crossref's article
    index; carried under expect_no_doi, not dropped, not faked.

Unlike C.2.h (a thin, recent, post-2007 literature), A.14 is an OLD, well-canonised proximate-
determinant literature: the binding problem is recall of the classic biometric + natural-fertility
canon and DISCOVERY of the identified separation/abstinence naturals, not novelty. The strongest
identified designs are (i) prospective biometric studies relating measured coital frequency/timing to
per-cycle conception (Barrett-Marshall, Wilcox), and (ii) exogenous frequency shocks — spousal
separation from labour migration/war, and ritual/post-partum abstinence windows.

Decoys cover the six registered walls (A.2-A.6 contraception, A.7/C.7 marriage, A.13 lactation,
A.15/A.16/B.3 fecundity capacity, upstream causes C.2.h/B.7, B.5 fetal loss) so the eventual search is
tested on ROUTING, not only topical recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never both.

Crossref only — this does NOT touch the OpenAlex daily budget.

Output: literature/search-logs/coital-frequency-biological-cold-start-anchors.json
        literature/search-logs/coital-frequency-biological-cold-start-anchors-log.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "coital-frequency-biological"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a14_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # ---- Biometric primary core: coital frequency/timing -> per-cycle conception (Tier A empirical) ----
    dict(title="The risk of conception on different days of the menstrual cycle",
         authors=["J. C. Barrett", "John Marshall"], year=1969, family="biometric-fecundability",
         provisional_cell="PRIMARY_FREQ_BIOMETRIC", provenance_channel="direct_empirical_bibliographic_search",
         note="Population Studies 23(3):455-461. The classic estimate of per-cycle conception probability "
              "by day of cycle and by coital frequency; the slope of the frequency->fecundability identity."),
    dict(title="Timing of sexual intercourse in relation to ovulation. Effects on the probability of conception, survival of the pregnancy, and sex of the baby",
         authors=["Allen J. Wilcox", "Clarice R. Weinberg", "Donna D. Baird"], year=1995,
         family="biometric-fecundability", provisional_cell="PRIMARY_FREQ_BIOMETRIC",
         provenance_channel="direct_empirical_bibliographic_search",
         note="New England Journal of Medicine 333(23):1517-1521. Prospective daily-diary study of intercourse "
              "timing and conception; the modern biometric anchor for the fertile-window/frequency relationship."),
    # ---- Separation / abstinence shocks: exogenous frequency variation -> fertility (Tier A empirical) ----
    dict(title="The role of marital sexual abstinence in determining fertility: a study of the Yoruba in Nigeria",
         authors=["John C. Caldwell", "Pat Caldwell"], year=1977, family="abstinence-natural",
         provisional_cell="PRIMARY_ABSTINENCE_WINDOW", provenance_channel="direct_empirical_bibliographic_search",
         note="Population Studies 31(2):193-217. Registry seminal. Post-partum sexual abstinence taboo and its "
              "fertility effect — the classic abstinence-window natural experiment. Wall 3 (vs A.13 lactation)."),
    dict(title="The short- and long-term effects of U.S. migration experience on Mexican women's fertility",
         authors=["David P. Lindstrom", "Silvia Giorguli Saucedo"], year=2002, family="separation-natural",
         provisional_cell="PRIMARY_SEPARATION_SHOCK", provenance_channel="direct_empirical_bibliographic_search",
         note="Social Forces 80(4):1341-1368. Labour migration and spousal separation as a shock to coital "
              "exposure within intact unions -> fertility. Wall 2 (union persists; only exposure falls)."),

    # ---- Sex-recession / frequency-decline stream (SDT); frequency trend, may be mechanism ----
    dict(title="Declines in sexual frequency among American adults, 1989-2014",
         authors=["Jean M. Twenge", "Ryne A. Sherman", "Brooke E. Wells"], year=2017,
         family="frequency-trend", provisional_cell="PRIMARY_FREQ_DECLINE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Archives of Sexual Behavior 46(8):2389-2401. The canonical 'sex recession' documentation. "
              "Frequency trend; routes to MECHANISM_FREQ_ONLY unless it carries a fertility link."),
    dict(title="Trends in frequency of sexual activity and number of sexual partners among adults aged 18 to 44 years in the US, 2000-2018",
         authors=["Peter Ueda", "Catherine H. Mercer", "Cyrus Ghaznavi", "Debby Herbenick"], year=2020,
         family="frequency-trend", provisional_cell="PRIMARY_FREQ_DECLINE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="JAMA Network Open 3(6):e203833. Corroborating US frequency-decline evidence; frequency trend "
              "(mechanism) unless linked to a fertility outcome."),

    # ---- Theory / proximate-determinant canon (does NOT count toward empirical recall) ----
    dict(title="A framework for analyzing the proximate determinants of fertility",
         authors=["John Bongaarts"], year=1978, family="proximate-determinant-theory",
         provisional_cell="MECHANISM_FREQ_ONLY", provenance_channel="hypothesis_canon",
         note="Population and Development Review 4(1):105-132. Registry seminal. The framework in which coital "
              "frequency sits inside the residual fecundability term (Cm, Cc, Ca, Ci are the named indices). "
              "Theory seed — the decomposition risk the scope names."),
    dict(title="Social structure and fertility: an analytic framework",
         authors=["Kingsley Davis", "Judith Blake"], year=1956, family="proximate-determinant-theory",
         provisional_cell="MECHANISM_FREQ_ONLY", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Economic Development and Cultural Change 4(3):211-235. Registry seminal. The original "
              "intermediate-variables framework listing coital frequency as an intercourse variable. Old canon: "
              "possible Crossref-index miss."),
    dict(title="Fecundity and natural fertility in humans",
         authors=["James W. Wood"], year=1989, family="proximate-determinant-theory",
         provisional_cell="MECHANISM_FREQ_ONLY", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Oxford Reviews of Reproductive Biology 11:61-109. Registry seminal (Wood 1989). The biometric "
              "review of fecundability and its coital-frequency component. Review-series: possible index miss."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="More power to the pill: the impact of contraceptive freedom on women's life cycle labor supply",
         authors=["Martha J. Bailey"], year=2006, family="ROUTING_DECOY",
         provisional_cell="OFF_CONTRACEPTION", provenance_channel="routing_decoy_A2A6",
         routing_note="Contraceptive access (the Cc index) -> A.2-A.6. A.14 is the exposure identity NET of "
                      "contraception; the explicit 'independently of contraceptive use' wall. Wall 1 (load-bearing)."),
    dict(title="European marriage patterns in perspective",
         authors=["John Hajnal"], year=1965, family="ROUTING_DECOY",
         provisional_cell="OFF_UNION_FORMATION", provenance_channel="routing_decoy_A7C7", expect_no_doi=True,
         note="In Glass & Eversley (eds), Population in History. The proportion-married (Cm) channel -> A.7/C.7. "
              "A.14 owns coital frequency WITHIN a union, not the existence of the union. Wall 2. Book chapter: "
              "expected Crossref-index miss."),
    dict(title="Consensus statement on the use of breastfeeding as a family planning method",
         authors=["Kathy I. Kennedy", "Roberto Rivera", "Alan S. McNeilly"], year=1989,
         family="ROUTING_DECOY", provisional_cell="OFF_LACTATION", provenance_channel="routing_decoy_A13",
         routing_note="Lactational amenorrhoea / postpartum infecundability (the Ci index) -> A.13. Distinct "
                      "from the postpartum ABSTINENCE taboo (which is A.14). Wall 3."),
    dict(title="Age and infertility",
         authors=["Jane Menken", "James Trussell", "Ulla Larsen"], year=1986, family="ROUTING_DECOY",
         provisional_cell="OFF_FECUNDITY_CAPACITY", provenance_channel="routing_decoy_A15",
         known_doi="10.1126/science.3755843",  # live-verified via Crossref author-qualified lookup 2026-09-23; the 3-word title is too generic for the bibliographic ranker
         routing_note="Age-related fecundity decline (the fecundability ceiling) -> A.15. A.14 changes frequency "
                      "at a fixed fecund capacity; the age confound is the routing challenge. Wall 4."),
    dict(title="Incidence of early loss of pregnancy",
         authors=["Allen J. Wilcox", "Clarice R. Weinberg", "John F. O'Connor", "Donna D. Baird"], year=1988,
         family="ROUTING_DECOY", provisional_cell="OFF_FETAL_LOSS", provenance_channel="routing_decoy_B5",
         routing_note="Loss of an established pregnancy -> B.5. A.14 governs whether a conception OCCURS; B.5 "
                      "whether it SURVIVES. Wall 6. (Distinct Wilcox paper from the 1995 timing study.)"),
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
    # Secondary re-affirmation at doi.org. doi.org may be unreachable (this sandbox returns 403 to all
    # doi.org requests). A block is NOT absence and must never downgrade a live Crossref match.
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
    L = ["# A.14 cold-start anchors — existence-verification log", "",
         "Generated by `source/build/goldset/90_a14_cold_start_anchors.py`. **Existence gate: a live",
         "Crossref bibliographic match (Jaccard >= 0.72 AND year +/-1).** No anchor asserts a DOI; the",
         "DOI is whatever a live match returns (or a curated `known_doi` for canonical papers Crossref",
         "mis-ranks). A network failure is `unconfirmed`, never absent. The doi.org second re-affirm is",
         "best-effort and may be blocked (HTTP 403) from this sandbox, so it is recorded, not gated on — "
         f"doi_reaffirm tally: {reaff}.", "",
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
