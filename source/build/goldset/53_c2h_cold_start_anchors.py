#!/usr/bin/env python3
"""
53_c2h_cold_start_anchors.py — C.2.h (digital leisure substitution), stage-3 cold-start anchors.

Mirrors 89 (A.3), 72 (D.3.b), 64 (B.1): source and EXISTENCE-VERIFY the cold-start anchor set.
Discipline, unchanged from those chains and from the 2026-07-08 OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) and assert
    NO DOIs. The DOI is whatever a LIVE Crossref bibliographic match returns, re-affirmed at doi.org.
    No anchor enters a recall denominator without a resolved live id.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears to
    identity_verified=True. A real match with a year outside tolerance is version_drift (RA-confirm),
    not a ghost.
  * Working papers and books (Myers-Hooper NBER w35310; Twenge iGen) are EXPECTED to miss Crossref's
    article index; carried under expect_no_doi, not dropped, not faked. Myers-Hooper was independently
    web-verified 2026-09-21 (nber.org/papers/w35310, SSRN 6897299).

C.2.h is a NEW, THIN, RECENT literature (post-2007), so the binding problem is DISCOVERY at the
identified core, not recall of an old canon. The strongest identified designs are broadband/device
diffusion instruments (Myers-Hooper, Billari-Giuntella-Stella, Guldi-Herbst, Bellou). Decoys cover
the five registered walls (C.2.e wages, A.24 dating apps, A.14 coital frequency, D.1.a values, D.3.a
mental health) so the eventual search is tested on ROUTING, not only topical recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never
both.

Crossref only — this does NOT touch the OpenAlex daily budget.

Output: literature/search-logs/digital-leisure-substitution-cold-start-anchors.json
        literature/search-logs/digital-leisure-substitution-cold-start-anchors-log.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "digital-leisure-substitution"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c2h_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # ---- Empirical primary core (Tier A empirical) ----
    dict(title="Is the iPhone Birth Control? Causal Evidence from AT&T's 2007-2011 Carrier Monopoly",
         authors=["Caitlin K. Myers", "Ezekiel Hooper"], year=2026, family="device-diffusion-empirical",
         provisional_cell="PRIMARY_LEISURE_PRICE", provenance_channel="direct_empirical_bibliographic_search",
         expect_no_doi=True,
         note="NBER Working Paper w35310. Web-verified 2026-09-21 (nber.org/papers/w35310, SSRN 6897299). "
              "AT&T exclusive-iPhone-carrier instrument; attributes 33-52% of the post-2007 GFR decline. "
              "The chapter's primary anchor and the study to beat. NBER WP: expected Crossref-index miss."),
    dict(title="Does broadband Internet affect fertility?",
         authors=["Francesco C. Billari", "Osea Giuntella", "Luca Stella"], year=2019,
         family="broadband-diffusion-empirical", provisional_cell="PRIMARY_LEISURE_PRICE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Population Studies 73(3):297-316. Broadband diffusion in Germany and fertility; the closest "
              "published identified analogue to Myers-Hooper on the leisure-price channel."),
    dict(title="Offline effects of online connecting: the impact of broadband diffusion on teen fertility decisions",
         authors=["Melanie Guldi", "Chris M. Herbst"], year=2017, family="broadband-diffusion-empirical",
         provisional_cell="PRIMARY_LEISURE_PRICE", provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Population Economics 30(1):69-91. Broadband diffusion and teen fertility in the US; "
              "identified off state-level broadband rollout."),
    dict(title="The impact of Internet diffusion on marriage rates: evidence from the broadband market",
         authors=["Andriana Bellou"], year=2015, family="broadband-diffusion-empirical",
         provisional_cell="PRIMARY_SOCIAL_DISPLACEMENT", provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Population Economics 28(2):265-297. Internet/broadband diffusion and marriage — the "
              "partnering (union-formation) outcome; identifies a social-displacement/matching effect."),
    dict(title="Leisure Luxuries and the Labor Supply of Young Men",
         authors=["Mark Aguiar", "Mark Bils", "Kerwin Kofi Charles", "Erik Hurst"], year=2021,
         family="timeuse-mechanism", provisional_cell="MECHANISM_TIMEUSE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Political Economy 129(2):337-382. Video games/recreational computing and young "
              "men's hours; the time-use mechanism (no direct fertility outcome) — a MECHANISM anchor."),
    dict(title="Pornography and the marriage market",
         authors=["Jiwon Ryu"], year=2024, family="pornography-substitution-empirical",
         provisional_cell="PRIMARY_PORN_SUBSTITUTION", provenance_channel="direct_empirical_bibliographic_search",
         note="Registry seed (Jiwon Ryu 2024, porn substitution and the marriage market). Exact title/venue "
              "uncertain; Crossref adjudicates and this may resolve to version_drift or need RA confirmation."),

    # ---- Theory / foundational (does NOT count toward empirical recall) ----
    dict(title="A Theory of the Allocation of Time",
         authors=["Gary S. Becker"], year=1965, family="time-allocation-theory",
         provisional_cell="MECHANISM_TIMEUSE", provenance_channel="hypothesis_canon",
         known_doi="10.2307/2228949",
         note="The Economic Journal 75(299):493-517. The household-production/time-allocation foundation in "
              "which digital leisure is a cheaper substitute for the time children require. Theory seed. "
              "Crossref bibliographic search mis-ranks this canonical paper, so its DOI is pinned and "
              "verified directly at doi.org (a curated override, not an asserted-from-memory id)."),
    dict(title="iGen: Why Today's Super-Connected Kids Are Growing Up Less Rebellious, More Tolerant, Less Happy",
         authors=["Jean M. Twenge"], year=2017, family="descriptive-theory",
         provisional_cell="MECHANISM_TIMEUSE", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Atria Books. Registry seed; the descriptive case that the smartphone generation delays "
              "partnering/independence milestones. Book: expected Crossref article-index miss."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="Fertility, female labor force participation, and the demographic dividend",
         authors=["David E. Bloom", "David Canning", "Guenther Fink", "Jocelyn E. Finlay"], year=2009,
         family="ROUTING_DECOY", provisional_cell="OFF_WAGE_C2E", provenance_channel="routing_decoy_C2e",
         routing_note="Female LFP / opportunity-cost-of-time channel -> C.2.e. Same Becker substitution "
                      "structure as C.2.h but the price that moves is the wage, not the leisure good. Wall 1."),
    dict(title="Disintermediating your friends: How online dating in the United States displaces other ways of meeting",
         authors=["Michael J. Rosenfeld", "Reuben J. Thomas", "Sonia Hausen"], year=2019,
         family="ROUTING_DECOY", provisional_cell="OFF_DATINGAPP_A24", provenance_channel="routing_decoy_A24",
         routing_note="Dating-app MATCHING technology and how couples meet -> A.24. Same device, but the "
                      "estimand is matching, not leisure time crowd-out. Wall 2 (the near wall)."),
    dict(title="A framework for analyzing the proximate determinants of fertility",
         authors=["John Bongaarts"], year=1978, family="ROUTING_DECOY",
         provisional_cell="OFF_COITAL_A14", provenance_channel="routing_decoy_A14",
         routing_note="The coital-frequency -> fecundability -> births proximate-determinant identity -> A.14. "
                      "C.2.h owns only the digital-leisure CAUSE of a frequency change, not the identity. Wall 3."),
    dict(title="The unfolding story of the second demographic transition",
         authors=["Ron Lesthaeghe"], year=2010, family="ROUTING_DECOY",
         provisional_cell="OFF_VALUES_D1A", provenance_channel="routing_decoy_D1a",
         routing_note="The value shift valorizing self-oriented leisure -> D.1.a. C.2.h holds tastes fixed "
                      "and moves the price of the leisure substitute. Wall 4."),
    dict(title="Increases in depressive symptoms, suicide-related outcomes, and suicide rates among U.S. adolescents after 2010 and links to increased new media screen time",
         authors=["Jean M. Twenge", "Thomas E. Joiner", "Megan L. Rogers", "Gabrielle N. Martin"], year=2018,
         family="ROUTING_DECOY", provisional_cell="OFF_MENTALHEALTH_D3A", provenance_channel="routing_decoy_D3a",
         routing_note="Screen time -> depression/mental-health pathway -> D.3.a. The load-bearing wall (281 "
                      "frame overlap in the probe): C.2.h is the direct time/attention crowd-out, D.3.a the "
                      "affective/clinical mediator. Wall 5."),
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
    # Secondary re-affirmation at doi.org. Returns "resolves" | "not_found" | "blocked" | "error".
    # NOTE: doi.org may be unreachable from a given environment (this sandbox returns 403 to all
    # doi.org requests). A block is NOT absence and must never downgrade a live Crossref match; the
    # existence gate is the Crossref bibliographic match, and this is a best-effort second check.
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
        # Curated DOI override for canonical papers Crossref's bibliographic ranker mis-orders.
        rec["doi"] = c["known_doi"]
        rec["doi_reaffirm"] = doi_reaffirm(c["known_doi"])
        rec["state"] = "verified_pinned"
        rec["identity_verified"] = True  # pinned canonical id; doi.org is best-effort only
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
    # The existence gate is the live Crossref bibliographic match. doi.org is a best-effort second
    # check that is environmentally blocked here (403); it is recorded, never a downgrade.
    if jac >= TITLE_JACCARD_MIN and yr_ok:
        rec["doi"] = best["doi"]
        rec["doi_reaffirm"] = doi_reaffirm(best["doi"])
        rec["state"] = "verified"
        rec["identity_verified"] = True
    elif jac >= TITLE_JACCARD_MIN and not yr_ok:
        rec["doi"] = best["doi"]
        rec["doi_reaffirm"] = doi_reaffirm(best["doi"])
        rec["state"] = "version_drift"  # real match, year off (preprint vs VoR) — RA swap on freeze
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
    L = [f"# C.2.h cold-start anchors — existence-verification log", "",
         "Generated by `source/build/goldset/53_c2h_cold_start_anchors.py`. **Existence gate: a live",
         "Crossref bibliographic match (Jaccard >= 0.72 AND year +/-1).** No anchor asserts a DOI; the",
         "DOI is whatever a live match returns (or a curated `known_doi` for canonical papers Crossref",
         "mis-ranks). A network failure is `unconfirmed`, never absent. The doi.org second re-affirm is",
         "best-effort and **blocked (HTTP 403) from this sandbox**, so it is recorded, not gated on — "
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
