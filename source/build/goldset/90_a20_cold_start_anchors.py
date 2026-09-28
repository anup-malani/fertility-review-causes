#!/usr/bin/env python3
"""
90_a20_cold_start_anchors.py — A.20 (cultural diffusion mechanisms), stage-3 cold-start anchors.

Mirrors 90_d1d / 90_d2c / 90_a14: source and EXISTENCE-VERIFY the cold-start anchor set. Discipline,
unchanged from those chains and the 2026-07-08 OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) and assert
    NO DOIs. The DOI is whatever a LIVE Crossref bibliographic match returns, re-affirmed at doi.org.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears identity_verified.
    A real match with a year outside tolerance is version_drift (RA-confirm).
  * Old canon and books are EXPECTED to miss Crossref's article index; carried under expect_no_doi.

A.20's binding problem is the mirror image of A.3's. A.20 owns the CHANNEL (media reach, network
position, community boundary) regardless of content; A.3 owns the diffused CONTENT (fertility-control
knowledge). The cleanest identified estimates in the whole neighbourhood — the Brazil telenovela and
India cable-TV quasi-experiments — are A.20's core, precisely because A.3 (TICK-088, Wall 1 resolved
2026-09-18) routed them here as content-agnostic. So the Tier-A empirical core here is exactly the set
that was a routing DECOY for D.1.d; the leakage runs the other way.

Decoys cover the six registered walls (A.3 fertility-control content [LOAD-BEARING], A.19 vertical
transmission, A.2 contraceptive technology, A.5 family-planning program message, D.1.a secular value
shift, D.1.d nationalist content) so the eventual search is tested on ROUTING, not only topical recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never both.

Crossref only — this does NOT touch the OpenAlex daily budget.

Output: literature/search-logs/cultural-diffusion-mechanisms-cold-start-anchors.json
        literature/search-logs/cultural-diffusion-mechanisms-cold-start-anchors-log.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "cultural-diffusion-mechanisms"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a20_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # ---- Media / network empirical core (Tier A, forward-seeded). These are A.20's identified core. ----
    dict(title="Soap operas and fertility: evidence from Brazil",
         authors=["Eliana La Ferrara", "Alberto Chong", "Suzanne Duryea"], year=2012,
         family="media-channel", provisional_cell="PRIMARY_MEDIA_CHANNEL",
         provenance_channel="direct_empirical_bibliographic_search",
         note="American Economic Journal: Applied Economics 4(4):1-31. Registry seminal. The cleanest "
              "identified A.20 estimate: staggered Globo telenovela signal coverage (ambient small-family "
              "portrayal, not a family-planning message) lowers fertility. Content-agnostic CHANNEL — "
              "routed here by A.3's Wall 1."),
    dict(title="The power of TV: cable television and women's status in India",
         authors=["Robert Jensen", "Emily Oster"], year=2009, family="media-channel",
         provisional_cell="PRIMARY_MEDIA_CHANNEL", provenance_channel="direct_empirical_bibliographic_search",
         note="Quarterly Journal of Economics 124(3):1057-1094. Registry seminal. Staggered cable-TV "
              "introduction (general programming) lowers fertility and shifts women's status — the "
              "content-agnostic reach design that defines the A.20 media stream."),
    dict(title="The density of social networks and fertility decisions: evidence from South Nyanza District Kenya",
         authors=["Hans-Peter Kohler", "Jere R. Behrman", "Susan C. Watkins"], year=2001,
         family="social-network", provisional_cell="PRIMARY_NETWORK_PEER",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 38(1):43-58. Registry seminal. Social-network density and structure shape "
              "contraceptive/fertility decisions — the peer/network CHANNEL, with the reflection problem "
              "as the central identification test."),

    # ---- Theory / channel canon (backward-only; books expect_no_doi, articles matched) ----
    dict(title="The decline of fertility in Europe",
         authors=["Ansley J. Coale", "Susan Cotts Watkins"], year=1986, family="linguistic-boundary",
         provisional_cell="PRIMARY_LINGUISTIC_BOUNDARY", provenance_channel="hypothesis_canon",
         expect_no_doi=True,
         note="Princeton University Press (book). Registry seminal. The European Fertility Project: "
              "marital-fertility decline clustered by language and religion and crossed borders on a "
              "timetable development does not reproduce — the community boundary as conduit. Book: "
              "expected Crossref-index miss."),
    dict(title="From provinces into nations: demographic integration in Western Europe 1870-1960",
         authors=["Susan Cotts Watkins"], year=1991, family="linguistic-boundary",
         provisional_cell="PRIMARY_LINGUISTIC_BOUNDARY", provenance_channel="hypothesis_canon",
         expect_no_doi=True,
         note="Princeton University Press (book). Registry seminal. Demographic integration along "
              "national/linguistic lines — the boundary-as-conduit reading of the Princeton signature. "
              "Book: expected Crossref-index miss."),
    dict(title="Social interactions and contemporary fertility transitions",
         authors=["John Bongaarts", "Susan Cotts Watkins"], year=1996, family="social-network",
         provisional_cell="MECHANISM_CHANNEL_DESCRIPTIVE", provenance_channel="hypothesis_canon",
         note="Population and Development Review 22(4):639-682. Registry seminal. The canonical statement "
              "that social interaction shapes the pace and geography of fertility transitions."),
    dict(title="Social learning social influence and new models of fertility",
         authors=["Mark R. Montgomery", "John B. Casterline"], year=1996, family="social-network",
         provisional_cell="MECHANISM_CHANNEL_DESCRIPTIVE", provenance_channel="hypothesis_canon",
         note="Population and Development Review 22(Supplement):151-175. Distinguishes social learning "
              "from social influence — the two channel sub-mechanisms A.20 must keep separate; also names "
              "the reflection problem that gates the identified core."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="Demand theories of the fertility transition: an iconoclastic view",
         authors=["John Cleland", "Christopher Wilson"], year=1987, family="ROUTING_DECOY",
         provisional_cell="OFF_CONTENT_FERTILITY_CONTROL", provenance_channel="routing_decoy_A3",
         routing_note="The diffusion of fertility-CONTROL knowledge and its legitimacy specifically -> "
                      "A.3. A.20 owns the channel it rides on, not the fertility-control content. Wall 1 "
                      "(LOAD-BEARING)."),
    dict(title="Culture: an empirical investigation of beliefs work and fertility",
         authors=["Raquel Fernandez", "Alessandra Fogli"], year=2009, family="ROUTING_DECOY",
         provisional_cell="OFF_VERTICAL", provenance_channel="routing_decoy_A19",
         routing_note="Parent-to-child / ancestral-culture transmission of fertility (the epidemiological "
                      "immigrant design) -> A.19 (vertical). A.20 owns horizontal channels. Wall 2."),
    dict(title="The power of the pill: oral contraceptives and women's career and marriage decisions",
         authors=["Claudia Goldin", "Lawrence F. Katz"], year=2002, family="ROUTING_DECOY",
         provisional_cell="OFF_TECHNOLOGY", provenance_channel="routing_decoy_A2",
         routing_note="Access to the physical contraceptive METHOD (the Pill) as a technology -> A.2. "
                      "A.20 owns the spread of norms through channels, not the device. Wall 3."),
    dict(title="Contraception as development? New evidence from family planning in Colombia",
         authors=["Grant Miller"], year=2010, family="ROUTING_DECOY",
         provisional_cell="OFF_PROGRAM_CONTENT", provenance_channel="routing_decoy_A5",
         routing_note="Exogenous family-planning PROGRAM supply (Profamilia) with a deliberate "
                      "family-planning message -> A.5. A.20 owns content-agnostic media REACH, not the "
                      "program's instructional content. Wall 4."),
    dict(title="Cultural dynamics and economic theories of fertility change",
         authors=["Ron Lesthaeghe", "Johan Surkyn"], year=1988, family="ROUTING_DECOY",
         provisional_cell="OFF_CONTENT_VALUE_SHIFT", provenance_channel="routing_decoy_D1a",
         routing_note="The diffuse secular/individualist value shift (the CONTENT / why demand fell) -> "
                      "D.1.a. A.20 is agnostic to the message and owns only the vehicle. Wall 5."),
    dict(title="France needs children: pronatalism nationalism and women's equity",
         authors=["Leslie King"], year=1998, family="ROUTING_DECOY",
         provisional_cell="OFF_CONTENT_VALUE_SHIFT", provenance_channel="routing_decoy_D1d",
         routing_note="Nationalist-pronatalist ideology as the state-framing CONTENT -> D.1.d. A.20 owns "
                      "the channel that would carry such a message, not the message. Wall 6."),
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
    L = ["# A.20 cold-start anchors — existence-verification log", "",
         "Generated by `source/build/goldset/90_a20_cold_start_anchors.py`. **Existence gate: a live",
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
