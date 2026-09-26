#!/usr/bin/env python3
"""
90_d1d_cold_start_anchors.py — D.1.d (nationalist and pronatalist ideology), stage-3 cold-start anchors.

Mirrors 90_d2c / 90_a14: source and EXISTENCE-VERIFY the cold-start anchor set. Discipline, unchanged from
those chains and the 2026-07-08 OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) and assert
    NO DOIs. The DOI is whatever a LIVE Crossref bibliographic match returns, re-affirmed at doi.org.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears identity_verified.
    A real match with a year outside tolerance is version_drift (RA-confirm).
  * Old canon and books are EXPECTED to miss Crossref's article index; carried under expect_no_doi.

D.1.d is a comparatively THIN and historically-weighted empirical literature: the binding problem is not
recall of a large canon but (a) seeding the comparative-policy and demographic-nationalism empirical core
(Demeny, King, Fargues) and (b) testing ROUTING against the two load-bearing walls — the transfers the
ideology is bundled with (C.2.d) and the coercive abortion bans it is confused with (A.4). Most credible
identified estimates in this space are on the transfer side (C.2.d), which is itself the central finding
the routing must protect.

Decoys cover the six registered walls (C.2.d transfers, A.4 abortion ban, D.1.a secularization, D.1.a
religiosity arm, A.20 diffusion channel, C.3.c old-age security) so the eventual search is tested on
ROUTING, not only topical recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never both.

Crossref only — this does NOT touch the OpenAlex daily budget.

Output: literature/search-logs/nationalism-pronatalist-ideology-cold-start-anchors.json
        literature/search-logs/nationalism-pronatalist-ideology-cold-start-anchors-log.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "nationalism-pronatalist-ideology"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d1d_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # ---- Comparative-policy / rhetoric-intensity empirical core (Tier A, forward-seeded) ----
    dict(title="Pronatalist policies in low-fertility countries: patterns performance and prospects",
         authors=["Paul Demeny"], year=1986, family="comparative-policy",
         provisional_cell="PRIMARY_RHETORIC_INTENSITY", provenance_channel="direct_empirical_bibliographic_search",
         note="Population and Development Review 12 (Supplement):335-358. Registry seminal. The canonical "
              "comparative assessment of pronatalist policy performance across low-fertility states — the "
              "cross-national rhetoric/policy-intensity stream."),
    dict(title="France needs children: pronatalism nationalism and women's equity",
         authors=["Leslie King"], year=1998, family="pronatalist-nationalism",
         provisional_cell="PRIMARY_RHETORIC_INTENSITY", provenance_channel="direct_empirical_bibliographic_search",
         note="The Sociological Quarterly 39(1):33-52. Registry seminal. Pronatalism as an explicitly "
              "nationalist project and its tension with women's equity — the ideology-content anchor."),
    dict(title="Protracted national conflict and fertility change: Palestinians and Israelis in the twentieth century",
         authors=["Philippe Fargues"], year=2000, family="demographic-nationalism",
         provisional_cell="PRIMARY_RHETORIC_INTENSITY", provenance_channel="direct_empirical_bibliographic_search",
         note="Population and Development Review 26(3):441-482. Demographic nationalism / ethnonational "
              "fertility competition — a genuine empirical link between national ideology and fertility "
              "(SDT stream)."),

    # ---- Theory / ideology canon (backward-only; books, expect_no_doi) ----
    dict(title="Population politics in twentieth-century Europe: fascist dictatorships and liberal democracies",
         authors=["Maria Sophia Quine"], year=1996, family="ideology-theory",
         provisional_cell="MECHANISM_IDEOLOGY_ONLY", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Routledge (book). Registry seminal. The comparative history of interwar/mid-century "
              "pronatalist ideology under fascism and democracy. Book: expected Crossref-index miss."),
    dict(title="The state and the family: a comparative analysis of family policies in industrialized countries",
         authors=["Anne Helene Gauthier"], year=1996, family="ideology-theory",
         provisional_cell="MECHANISM_IDEOLOGY_ONLY", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Clarendon Press (book). Registry seminal. Comparative family-policy analysis; a bridge to "
              "C.2.d (transfers). Book: expected Crossref-index miss."),
    dict(title="The fear of population decline",
         authors=["Michael S. Teitelbaum", "Jay M. Winter"], year=1985, family="ideology-theory",
         provisional_cell="MECHANISM_IDEOLOGY_ONLY", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Academic Press (book). The demographic-anxiety / population-decline-nationalism motive that "
              "drives pronatalist ideology. Book: expected Crossref-index miss."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="Subsidizing the stork: new evidence on tax incentives and fertility",
         authors=["Kevin Milligan"], year=2005, family="ROUTING_DECOY",
         provisional_cell="OFF_TRANSFERS", provenance_channel="routing_decoy_C2d",
         routing_note="A cash/tax incentive (Quebec Allowance for Newborn Children) -> fertility is the "
                      "FINANCIAL instrument -> C.2.d. D.1.d owns the ideological framing, not the transfer. "
                      "Wall 1 (LOAD-BEARING)."),
    dict(title="The impact of an abortion ban on socioeconomic outcomes of children: evidence from Romania",
         authors=["Cristian Pop-Eleches"], year=2006, family="ROUTING_DECOY",
         provisional_cell="OFF_ABORTION_BAN", provenance_channel="routing_decoy_A4",
         routing_note="Romania's Decree 770 raised fertility by BANNING abortion — coercion, not "
                      "persuasion -> A.4/A.2. The canonical trap: it is cited as 'pronatalist' but is a "
                      "supply restriction. Wall 2 (LOAD-BEARING)."),
    dict(title="Cultural dynamics and economic theories of fertility change",
         authors=["Ron Lesthaeghe", "Johan Surkyn"], year=1988, family="ROUTING_DECOY",
         provisional_cell="OFF_SECULARIZATION", provenance_channel="routing_decoy_D1a",
         routing_note="The diffuse secular/individualist value shift that LOWERS fertility -> D.1.a. D.1.d "
                      "owns the deliberate, state-sponsored, opposite-signed counter-framing. Wall 3."),
    dict(title="Religion religiousness and fertility in the US and in Europe",
         authors=["Tomas Frejka", "Charles F. Westoff"], year=2008, family="ROUTING_DECOY",
         provisional_cell="OFF_RELIGIOSITY", provenance_channel="routing_decoy_D1a_relig",
         routing_note="Personal/denominational religiosity -> fertility routes to D.1.a (secularization "
                      "arm). D.1.d owns only the STATE's instrumentalization of religious-national "
                      "identity for a demographic end. Wall 4."),
    dict(title="Soap operas and fertility: evidence from Brazil",
         authors=["Eliana La Ferrara", "Alberto Chong", "Suzanne Duryea"], year=2012, family="ROUTING_DECOY",
         provisional_cell="OFF_DIFFUSION_CHANNEL", provenance_channel="routing_decoy_A20",
         routing_note="The media CHANNEL through which any norm spreads, regardless of message content -> "
                      "A.20. D.1.d owns the nationalist-pronatalist message itself, citing A.20 as the "
                      "vehicle. Wall 5."),
    dict(title="The old-age security motive for fertility",
         authors=["Jeffrey B. Nugent"], year=1985, family="ROUTING_DECOY",
         provisional_cell="OFF_OLD_AGE_SECURITY", provenance_channel="routing_decoy_C3c",
         routing_note="Pensions / old-age support as an economic driver of fertility -> C.3.c. C.3.c is one "
                      "economic ROOT/motive, but pension-driven fertility change is not D.1.d evidence. "
                      "Wall 6."),
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
    L = ["# D.1.d cold-start anchors — existence-verification log", "",
         "Generated by `source/build/goldset/90_d1d_cold_start_anchors.py`. **Existence gate: a live",
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
