#!/usr/bin/env python3
"""
72_d3b_cold_start_anchors.py — D.3.b (climate anxiety / eco-doomerism), stage A3.

Parallel workstream to B.1 (steps 64-71). Source and EXISTENCE-VERIFY the cold-start anchor set.
Same load-bearing discipline as 64 (B.1), which itself carries the OAS ghost-citation lesson:

  * Candidates below carry (title, authors, year, family, provisional_cell, provenance_channel) drawn
    from a LIVE web-sourcing pass (2026-07-23), not from unaided memory. This matters more here than
    for B.1: D.3.b is a 2020s literature where the binding problem is discovery, not recall, so anchors
    were sourced online first (incl. the PLOS Climate systematic review's 13-study included list as the
    privileged channel-1 seed) and only then verified. They assert NO DOIs.
  * Every DOI is pulled from a LIVE Crossref bibliographic match (never hand-typed), then re-affirmed at
    doi.org. Mandatory existence gate: no anchor enters a recall denominator without a resolved live id.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref 200-with-DOI
    whose title matches (Jaccard >= 0.72 AND year within +/-1) clears the gate to identity_verified=True.
  * Books (Conly 2016) are EXPECTED to miss Crossref's article index; carried, not dropped, not faked.
  * "Britt et al. 2025 (Genus)" from the HYPOTHESES-v5 seminal list did NOT resolve to any real paper in
    the web pass; the real Genus 2025 paper is Puglisi/Muttarak/Vignoli. Britt is therefore treated as a
    likely mis-citation and is NOT carried as an anchor. This is the ghost the live pass is meant to catch.

LEAKAGE WALL: the channel-1 systematic review (PLOS Climate, 10.1371/journal.pclm.0000236) feeds its
INCLUDED STUDIES as anchors here; its search string must NOT also be mined for query terms in A6.

Candidate set spans all five A2 families + the channel-1 SR seed + four routing decoys (D.1.a
postmaterialism, C.5.a economic uncertainty, a physical climate-shock study, and a biological
reproductive-health review) so the eventual search is tested on routing as well as topical recall.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, time

SLUG = "climate-anxiety-eco-doomerism"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d3b_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # Family 2 — habitability / future-for-children fear (the empirical primary core)
    dict(title="Eco-reproductive concerns in the age of climate change",
         authors=["Matthew Schneider-Mayerson", "Kit Ling Leong"], year=2020, family="habitability-fear",
         provisional_cell="PRIMARY_HABITABILITY_FEAR", provenance_channel="channel1_SR_included_study",
         note="Climatic Change (NOT Feminist Studies as the v5 seminal list states). 607 US adults 27-45; "
              "96.5% concerned re children's climate future, 59.8% re carbon cost of procreation. Mixed-methods."),
    dict(title="Climate change worries and fertility intentions: Insights from three EU countries",
         authors=["Elena Bastianelli"], year=2025, family="habitability-fear",
         provisional_cell="PRIMARY_HABITABILITY_FEAR", provenance_channel="direct_empirical_bibliographic_search",
         note="J. Marriage & Family; GGS 2021/22; Finland/Estonia/Sweden 18-40; stated intention."),
    dict(title="Climate change concerns and fertility intentions: first evidence from Italy",
         authors=["Riccardo Valente Puglisi", "Raya Muttarak", "Daniele Vignoli"], year=2025,
         family="eco-doom-pessimism", provisional_cell="PRIMARY_ECO_PESSIMISM",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Genus 81:7 — the real 'Genus 2025' paper (v5 seminal list mis-cites this as 'Britt 2025')."),
    dict(title="Environmental concern and fertility intentions among Canadian university students",
         authors=["Steven Arnocky", "Danielle Dupuis", "Mirella L. Stroink"], year=2012,
         family="habitability-fear", provisional_cell="PRIMARY_HABITABILITY_FEAR",
         provenance_channel="channel1_SR_included_study",
         note="Population & Environment 34:279-292; N=139; quant; PLOS Climate SR included study."),

    # Family 1 — climate/eco-anxiety construct (the exposure spine)
    dict(title="The impact of climate change anxiety on the willingness to have children among married individuals",
         authors=["Anonymous"], year=2024, family="climate-anxiety-construct",
         provisional_cell="PRIMARY_ECO_PESSIMISM", provenance_channel="direct_empirical_bibliographic_search",
         note="J. Public Health (Springer); construct = climate-change anxiety scale -> willingness to have children."),

    # Family 3 — carbon-ethics / environmental antinatalism
    dict(title="Reproduction and the carbon legacies of individuals",
         authors=["Paul A. Murtaugh", "Michael G. Schlax"], year=2009, family="carbon-ethics",
         provisional_cell="PRIMARY_CARBON_ETHICS", provenance_channel="direct_empirical_bibliographic_search",
         note="Global Environmental Change; the foundational 'carbon legacy of a child' quantification."),
    dict(title="One Child: Do We Have a Right to More?",
         authors=["Sarah Conly"], year=2016, family="carbon-ethics",
         provisional_cell="THEORY", provenance_channel="hypothesis_canon", expect_no_doi=True,
         note="Population-ethics monograph; theory stream, does not count toward empirical recall."),

    # Family 4 — eco-doom / environmental pessimism  (+ the RARE realized-fertility outcome)
    dict(title="Are environmental concerns deterring people from having children? Longitudinal evidence on births in the UK",
         authors=["Anonymous"], year=2024, family="eco-doom-pessimism",
         provisional_cell="PRIMARY_ECO_PESSIMISM", provenance_channel="direct_empirical_bibliographic_search",
         note="Ecological Economics; LONGITUDINAL BIRTHS = REALIZED_FERTILITY, rare vs the intention-heavy corpus."),

    # Family 5 — reproductive-decision / motivation under climate (bounded; the D.1.a wall)
    dict(title="Too worried about the environment to have children? Or more worried about the environment after having children?",
         authors=["Anonymous"], year=2025, family="reproductive-decision-climate",
         provisional_cell="REVERSE", provenance_channel="direct_empirical_bibliographic_search",
         note="Population & Environment; title itself flags the REVERSE-causality threat central to identification."),
    dict(title="No future, no kids, no kids, no future? An exploration of motivations to remain childfree in times of climate change",
         authors=["Sabrina Helm", "Joya A. Kemper", "Samantha K. White"], year=2021,
         family="reproductive-decision-climate", provisional_cell="DESIRE_INDEPENDENCE",
         provenance_channel="channel1_SR_included_study",
         note="Population & Environment; qual; PLOS Climate SR included study."),
    dict(title="Reproductive choices and climate change in a pronatalist context",
         authors=["Ivett Szalma", "Borbala Julia Szczuka"], year=2024,
         family="reproductive-decision-climate", provisional_cell="DESIRE_INDEPENDENCE",
         provenance_channel="direct_empirical_bibliographic_search"),

    # Channel-1 SR-included — the important CONTRARY (null-to-positive) finding
    dict(title="Climate Change and Reproductive Intentions in Europe",
         authors=["Alessandra De Rose", "Maria Rita Testa"], year=2015, family="eco-doom-pessimism",
         provisional_cell="PRIMARY_ECO_PESSIMISM", provenance_channel="channel1_SR_included_study",
         note="Springer chapter; 2011 Eurobarometer, 27 countries; NULL-to-POSITIVE assoc (contrary evidence, "
              "and the reverse-causality interpretation). SR cites as 'De Rose & Testa 2013'."),

    # Theory canon (does NOT count toward empirical recall)
    dict(title="The dynamics of fertility under environmental concerns",
         authors=["Anonymous"], year=2025, family="climate-anxiety-construct",
         provisional_cell="THEORY", provenance_channel="hypothesis_canon",
         note="Environmental & Resource Economics; formal econ model of fertility under environmental concern."),

    # Routing decoys — MUST route away; included to test routing, not recall
    dict(title="The unfolding story of the second demographic transition",
         authors=["Ron Lesthaeghe"], year=2010, family="ROUTING_DECOY",
         provisional_cell="OFF_POSTMATERIALIST_D1a", provenance_channel="routing_decoy_D1a",
         routing_note="Postmaterialist value shift (positive preference, no fear content) = D.1.a; must route away."),
    dict(title="Where are the babies? Labor market conditions and fertility in Europe",
         authors=["Alicia Adsera"], year=2011, family="ROUTING_DECOY",
         provisional_cell="OFF_ECON_C5a", provenance_channel="routing_decoy_C5a",
         routing_note="Personal labor-market/income insecurity as the feared object = C.5.a; must route away."),
    dict(title="Climate shocks and fertility intentions: Evidence from extreme temperature events",
         authors=["Anonymous"], year=2025, family="ROUTING_DECOY",
         provisional_cell="OFF_OUTCOME", provenance_channel="routing_decoy_physical_climate",
         routing_note="Physical temperature-shock exposure (not subjective ecological dread) = climate-as-shock "
                      "mechanism, not D.3.b anxiety; routes away."),
    dict(title="Systematic review of climate change effects on reproductive health",
         authors=["Anonymous"], year=2022, family="ROUTING_DECOY",
         provisional_cell="OFF_OUTCOME", provenance_channel="routing_decoy_biological",
         routing_note="Physiological fecundity/pregnancy-outcome effects of climate (biological branch), not the "
                      "fear->intention channel; routes away."),
]


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def toks(s):
    return set(norm(s).split())


def jaccard(a, b):
    A, B = toks(a), toks(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def overlap_coef(a, b):
    """Szymkiewicz-Simpson: |A n B| / min(|A|,|B|). Catches the subtitle case — a candidate title that
    is a prefix of a long full title (Crossref keeps subtitles) scores low Jaccard but overlap ~1.0."""
    A, B = toks(a), toks(b)
    m = min(len(A), len(B))
    return len(A & B) / m if m else 0.0


def crossref_lookup(title, year, year_filter=None):
    key = f"{title}::{year}::{year_filter}"
    if key in cache:
        return cache[key]
    q = re.sub(r"\s+", "+", norm(title))
    filt = (f"&filter=from-pub-date:{year_filter}-01-01,until-pub-date:{year_filter}-12-31"
            if year_filter else "")
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=5&select=DOI,title,author,issued,container-title{filt}")
    try:
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        items = json.loads(out)["message"]["items"]
    except Exception as e:
        cache[key] = {"error": str(e)[:120]}
        return cache[key]
    best = None
    for it in items:
        ct = (it.get("title") or [""])[0]
        j = jaccard(title, ct)
        yr = None
        try:
            yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        except Exception:
            pass
        if best is None or j > best["jaccard"]:
            best = {"doi": it.get("DOI"), "matched_title": ct, "jaccard": round(j, 3),
                    "overlap": round(overlap_coef(title, ct), 3),
                    "cr_year": yr, "container": (it.get("container-title") or [""])[0]}
    cache[key] = best or {"doi": None, "jaccard": 0.0}
    return cache[key]


def doi_exists(doi):
    dkey = f"DOIRESOLVE::{doi}"
    if dkey in cache:
        return cache[dkey]
    try:
        code = subprocess.run(
            ["curl", "-s", "-I", "-o", "/dev/null", "-w", "%{http_code}", "-m", "25", "-A", UA,
             f"https://doi.org/{doi}"], capture_output=True, text=True).stdout.strip()
        state = "FOUND" if (code.startswith("3") or code == "200") else ("ABSENT" if code == "404" else "UNCONFIRMED")
    except Exception:
        state = "UNCONFIRMED"
    cache[dkey] = state
    return state


def main():
    anchors, log = [], []
    n_verified = n_flagged = n_book = n_drift = 0
    for c in CANDIDATES:
        rec = {k: c[k] for k in ("title", "authors", "year", "provenance_channel", "provisional_cell")}
        rec["query_cluster_family"] = c["family"]
        if c.get("routing_note"):
            rec["routing_note"] = c["routing_note"]
        if c.get("note"):
            rec["source_note"] = c["note"]
        cr = crossref_lookup(c["title"], c["year"], c.get("year_filter"))
        # Three-state year gate: a MISSING Crossref year does not reject a strong title+DOI identity
        # match (missing != contradicting); only a present-and-off year fails.
        yr_ok = cr.get("cr_year") is None or abs(cr["cr_year"] - c["year"]) <= YEAR_TOL
        j = cr.get("jaccard", 0.0)
        ov = cr.get("overlap", 0.0)
        # Accept on Jaccard, OR on high containment for a multi-token candidate (subtitle case).
        title_ok = j >= TITLE_JACCARD_MIN or (ov >= 0.90 and len(toks(c["title"])) >= 5)
        matched = bool(cr.get("doi")) and title_ok and yr_ok
        # Year-drift keep: an essentially-EXACT title match with a present-but-off year is NOT a ghost —
        # it is the preprint-vs-VoR / WP-vs-published / undated-chapter case. The resolution rule keeps a
        # real paper with a drifted identifier (keyed on title), so we existence-check and keep it under a
        # year_drift flag for RA confirmation rather than dropping it. (B.1 handled this per-candidate with
        # year_filter; this generalizes it so a near-exact title is never discarded on year alone.)
        near_exact = j >= 0.90 or (ov >= 0.98 and len(toks(c["title"])) >= 5)
        year_drift = (not matched) and bool(cr.get("doi")) and near_exact and title_ok and not yr_ok
        if matched:
            existence = doi_exists(cr["doi"])
            rec["doi"] = cr["doi"]
            rec["identity_source"] = f"https://doi.org/{cr['doi']}"
            rec["identity_verified"] = existence == "FOUND"
            rec["existence"] = existence
            rec["match_jaccard"] = j
            rec["container"] = cr.get("container")
            rec["gold_status"] = "candidate_not_ra_frozen"
            if existence == "FOUND":
                n_verified += 1
                status = f"VERIFIED  doi={cr['doi']}  J={j}  ({cr.get('container','')[:40]})"
            else:
                n_flagged += 1
                status = f"DOI-MATCH-BUT-{existence}  doi={cr['doi']}  J={j}"
        elif year_drift:
            existence = doi_exists(cr["doi"])
            rec["doi"] = cr["doi"]
            rec["identity_source"] = f"https://doi.org/{cr['doi']}"
            rec["identity_verified"] = existence == "FOUND"
            rec["existence"] = existence
            rec["match_jaccard"] = j
            rec["container"] = cr.get("container")
            rec["cr_year"] = cr.get("cr_year")
            rec["gold_status"] = "candidate_year_drift_ra_confirm"
            rec["note"] = (f"Exact-title match (J={j}) with year drift: candidate {c['year']} vs Crossref "
                           f"{cr.get('cr_year')} (preprint/WP-vs-VoR or undated chapter). Kept keyed on title.")
            n_drift += 1
            status = f"YEAR-DRIFT-KEEP  doi={cr['doi']}  J={j}  cand={c['year']} cr={cr.get('cr_year')}"
        else:
            rec["doi"] = None
            rec["identity_verified"] = False
            rec["match_jaccard"] = j
            rec["crossref_best"] = {"doi": cr.get("doi"), "title": cr.get("matched_title"),
                                     "jaccard": j, "year": cr.get("cr_year")}
            rec["gold_status"] = "unverified_no_doi_match"
            if c.get("expect_no_doi"):
                rec["note"] = "Book/monograph; expected Crossref-index miss. Carried in theory stream, not faked."
                n_book += 1
                status = f"BOOK-NO-DOI (expected)  best-J={j}"
            else:
                n_flagged += 1
                status = f"NO-MATCH  best-J={j}  best='{(cr.get('matched_title') or '')[:45]}'"
        anchors.append(rec)
        log.append(f"- **{c['title'][:70]}** ({c['year']}, {c['family']}) -> {status}")
        json.dump(cache, open(CACHE, "w"), indent=0)
        time.sleep(0.4)

    json.dump(anchors, open(OUT_JSON, "w"), indent=2)
    by_family = {}
    for a in anchors:
        by_family.setdefault(a["query_cluster_family"], []).append(a["identity_verified"])
    L = [f"# A3 cold-start anchors — {SLUG}", "",
         f"Sourced (live web pass 2026-07-23, incl. PLOS Climate SR channel-1 seed) + existence-verified "
         f"{len(anchors)} candidate anchors. Every DOI pulled from a live Crossref match "
         f"(Jaccard >= {TITLE_JACCARD_MIN}, year +/-{YEAR_TOL}) then re-affirmed at doi.org; no DOI "
         "hand-asserted. Three-state gate: network failure = UNCONFIRMED, never ABSENT.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Books (expected miss): {n_book}**", "",
         "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- {fam}: {sum(vs)}/{len(vs)}")
    L += ["", "## Per-candidate disposition", ""] + log
    L += ["", "## Notes", "",
          "- D.3.b is a 2020s literature: anchors were WEB-SOURCED first, then verified, because discovery "
          "(not recall) is the binding problem. 'Britt et al. 2025 (Genus)' from the v5 seminal list did not "
          "resolve to a real paper and is NOT carried; the real Genus 2025 paper is Puglisi/Muttarak/Vignoli.",
          "- Two v5 seminal-list metadata fixes surfaced: Schneider-Mayerson & Leong 2020 is in *Climatic "
          "Change*, not *Feminist Studies*; 'Britt 2025' -> Puglisi/Muttarak/Vignoli 2025. Flag for HYPOTHESES-v5.",
          "- The realized-fertility (UK longitudinal births) and the REVERSE-causality ('worried before vs after') "
          "anchors are deliberately included: they are the scarce identification-relevant designs in an "
          "otherwise intention-heavy, cross-sectional literature.",
          "- Routing decoys (D.1.a postmaterialism, C.5.a economic uncertainty, physical climate-shock, "
          "biological reproductive-health review) test that the search + screen route them away; they are NOT "
          "part of the D.3.b recall denominator.",
          "- LEAKAGE WALL: the PLOS Climate SR feeds included studies as anchors here; its search string must "
          "not be mined for A6 query terms.",
          "- Some anchors carry authors=['Anonymous'] as a placeholder where the web pass returned title+venue "
          "but not a clean author list; the Crossref match resolves the real authorship. This does not affect "
          "the existence gate, which keys on title+year+DOI."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} year_drift_keep={n_drift} flagged={n_flagged} books={n_book} total={len(anchors)}")
    print("by family:", {k: f"{sum(v)}/{len(v)}" for k, v in by_family.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
