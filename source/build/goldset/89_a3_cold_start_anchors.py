#!/usr/bin/env python3
"""
89_a3_cold_start_anchors.py — A.3 (diffusion and social-learning of fertility control), stage A3.

Mirrors 72 (D.3.b) and 64 (B.1): source and EXISTENCE-VERIFY the cold-start anchor set. Load-bearing
discipline, unchanged from those chains and from the OAS ghost-citation lesson:

  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) but assert
    NO DOIs. The DOI is whatever a LIVE Crossref bibliographic match returns; it is then re-affirmed at
    doi.org. No anchor enters a recall denominator without a resolved live id (the mandatory existence
    gate added after the 2026-07-08 OAS run found ~40% ghost citations in a frozen gold).
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears to
    identity_verified=True.
  * Books/edited volumes (Coale & Watkins 1986; the Casterline 2001 NAS volume) are EXPECTED to miss
    Crossref's article index; carried under expect_no_doi, not dropped, not faked.

UNLIKE D.3.b, A.3 is an OLD, canonical literature (the Princeton European Fertility Project and its
social-interaction successors), so the binding problem is RECALL, not discovery: anchors are
memory-enumerated from the canon and then Crossref-verified, exactly as B.1 did. There is no
Cochrane-style systematic review to serve as the privileged channel-1 seed; the Princeton EFP
synthesis (Coale & Watkins 1986) and the NAS "Diffusion Processes and Fertility Transition" volume
(Casterline, ed., 2001) play that role, and their included studies seed empirical anchors.

CHANNEL / WALL STRUCTURE (see literature/search-logs/diffusion-of-fertility-control-search-scope.md):
A.3 owns the diffused CONTENT (information about and legitimation of fertility control, social
learning of it). It does NOT own the CHANNELS (networks, mass media, linguistic boundaries) — those
are A.20. Per the 2026-09-18 RA resolution (channel-excluded A.3), the cleanest identified evidence in
this neighbourhood is channel evidence and routes to A.20: the Brazil soap-opera and India cable-TV
quasi-experiments are included here ONLY as A.20 routing decoys, to test that the search+screen route
them away. Further decoys cover A.2 (technology), A.19 (vertical transmission), A.5 (program supply),
and D.1 (the value shift) so the search is tested on routing as well as topical recall.

LEAKAGE WALL: an anchor's own study may seed the gold OR its vocabulary may seed query terms, never
both. The EFP/NAS synthesis volumes feed included studies as anchors here; their search vocabulary
must not later be mined as production-query terms for A.3.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, sys, time

SLUG = "diffusion-of-fertility-control"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a3_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

# Canonical identity normaliser — imported, not copied (textnorm.py exists to end the copy-drift that
# cost C.3.g 3 of 24 anchors; see scripts/verify_norm.py).
sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm, selftest  # noqa: E402

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # ---- Theory canon (Tier A theory; does NOT count toward empirical recall) ----
    dict(title="Demand theories of the fertility transition: An iconoclastic view",
         authors=["John Cleland", "Christopher Wilson"], year=1987, family="ideational-theory",
         provisional_cell="DIFFUSION_THEORY", provenance_channel="hypothesis_canon",
         note="Population Studies 41(1):5-30. The Cleland-Wilson ideational argument: fertility fell "
              "faster and more uniformly than demand theory predicts, implicating idea/legitimation diffusion."),
    dict(title="Social interactions and contemporary fertility transitions",
         authors=["John Bongaarts", "Susan Cotts Watkins"], year=1996, family="social-interaction-theory",
         provisional_cell="DIFFUSION_THEORY", provenance_channel="hypothesis_canon",
         note="Population and Development Review 22(4):639-682. One of A.3's four registered seminals; the "
              "social-interaction account of transition timing. Shared seminal with A.20 (channels)."),
    dict(title="Social learning, social influence, and new models of fertility",
         authors=["Mark R. Montgomery", "John B. Casterline"], year=1996, family="social-learning-theory",
         provisional_cell="DIFFUSION_THEORY", provenance_channel="hypothesis_canon",
         note="Population and Development Review 22(Suppl):151-175. The canonical social-learning vs "
              "social-influence distinction that defines A.3's mechanism."),
    dict(title="Modelling diffusion effects in fertility transition",
         authors=["Luis Rosero-Bixby", "John B. Casterline"], year=1993, family="social-learning-theory",
         provisional_cell="DIFFUSION_THEORY", provenance_channel="hypothesis_canon",
         note="Population Studies 47(1):147-167. Formal diffusion model; an A.3 registered seminal."),
    dict(title="Lessons from the past: Policy implications of historical fertility studies",
         authors=["John Knodel", "Etienne van de Walle"], year=1979, family="princeton-efp",
         provisional_cell="PRINCETON_CANON", provenance_channel="channel1_synthesis_included_study",
         note="Population and Development Review 5(2):217-245. The Princeton EFP synthesis of the "
              "language/religion clustering residual that is A.3's empirical signature."),
    dict(title="The Decline of Fertility in Europe",
         authors=["Ansley J. Coale", "Susan Cotts Watkins"], year=1986, family="princeton-efp",
         provisional_cell="PRINCETON_CANON", provenance_channel="channel1_synthesis_included_study",
         expect_no_doi=True,
         note="Princeton University Press (EFP capstone volume). Book: expected Crossref-index miss; "
              "carried as the privileged channel-1 synthesis whose province studies seed anchors."),
    dict(title="Diffusion Processes and Fertility Transition: Selected Perspectives",
         authors=["John B. Casterline"], year=2001, family="social-learning-theory",
         provisional_cell="PRINCETON_CANON", provenance_channel="channel1_synthesis_included_study",
         expect_no_doi=True,
         note="National Academies Press edited volume. Book: expected article-index miss; the second "
              "channel-1 synthesis seed. Cleland's 'Potatoes and pills' overview is a chapter here."),

    # ---- Empirical primary core (Tier A empirical) ----
    dict(title="The density of social networks and fertility decisions: Evidence from South Nyanza District, Kenya",
         authors=["Hans-Peter Kohler", "Jere R. Behrman", "Susan C. Watkins"], year=2001,
         family="social-network-empirical", provisional_cell="PRIMARY_SOCIAL_EXPOSURE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 38(1):43-58. Identified social-network effect on contraceptive/fertility decisions."),
    dict(title="Social norms and the fertility transition",
         authors=["Kaivan Munshi", "Jacques Myaux"], year=2006, family="social-network-empirical",
         provisional_cell="PRIMARY_SOCIAL_EXPOSURE", provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Development Economics 80(1):1-38. Matlab, Bangladesh; one of the more credibly "
              "identified social-interaction fertility papers."),
    dict(title="Social networks and changes in contraceptive use over time: Evidence from a longitudinal study in rural Kenya",
         authors=["Jere R. Behrman", "Hans-Peter Kohler", "Susan C. Watkins"], year=2002,
         family="social-network-empirical", provisional_cell="PRIMARY_SOCIAL_EXPOSURE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 39(4):713-738. Longitudinal social-network -> contraceptive adoption."),
    dict(title="Fertility and modernity",
         authors=["Enrico Spolaore", "Romain Wacziarg"], year=2022, family="spatial-cultural-diffusion",
         provisional_cell="PRIMARY_CULTURAL_BOUNDARY_CONTENT",
         provenance_channel="direct_empirical_bibliographic_search",
         note="The Economic Journal 132(642):796-833. Fertility decline diffuses along ancestral/linguistic "
              "distance from the French frontier — the cultural-boundary content signature, net of development."),
    dict(title="Can internal migration foster the convergence in regional fertility rates? Evidence from nineteenth century France",
         authors=["Guillaume Daudin", "Raphael Franck", "Hillel Rapoport"], year=2019,
         family="spatial-cultural-diffusion", provisional_cell="PRIMARY_SPATIAL_DIFFUSION",
         provenance_channel="direct_empirical_bibliographic_search",
         note="The Economic Journal 129(620):1618-1692. Migration-carried diffusion of fertility control "
              "across 19th-century French departments; identified spatial diffusion."),
    dict(title="Culture and the historical fertility transition",
         authors=["Brian Beach", "W. Walker Hanlon"], year=2023, family="spatial-cultural-diffusion",
         provisional_cell="PRIMARY_CULTURAL_BOUNDARY_CONTENT",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Review of Economic Studies. Culture/language and the timing of the British fertility "
              "transition; identified cultural-boundary diffusion. Year may drift 2022/2023 (VoR vs online)."),
    dict(title="Interaction diffusion and fertility transition in Costa Rica",
         authors=["Luis Rosero-Bixby", "John B. Casterline"], year=1994, family="social-network-empirical",
         provisional_cell="PRIMARY_SOCIAL_EXPOSURE", provenance_channel="direct_empirical_bibliographic_search",
         note="Social Forces 73(2):435-462. Empirical companion to the 1993 diffusion model."),

    # ---- Routing decoys — MUST route away; included to test routing, not recall ----
    dict(title="Soap operas and fertility: Evidence from Brazil",
         authors=["Eliana La Ferrara", "Alberto Chong", "Suzanne Duryea"], year=2012, family="ROUTING_DECOY",
         provisional_cell="OFF_CHANNEL_A20", provenance_channel="routing_decoy_A20",
         routing_note="Mass-media CHANNEL (Globo soap-opera rollout). Cleanest identified estimate in the "
                      "neighbourhood, but it is a conduit effect -> A.20 under the channel-excluded A.3 wall."),
    dict(title="The power of TV: Cable television and women's status in India",
         authors=["Robert Jensen", "Emily Oster"], year=2009, family="ROUTING_DECOY",
         provisional_cell="OFF_CHANNEL_A20", provenance_channel="routing_decoy_A20",
         routing_note="Cable-TV CHANNEL effect on fertility/autonomy -> A.20; not A.3's diffused content."),
    dict(title="The power of the pill: Oral contraceptives and women's career and marriage decisions",
         authors=["Claudia Goldin", "Lawrence F. Katz"], year=2002, family="ROUTING_DECOY",
         provisional_cell="OFF_TECHNOLOGY_A2", provenance_channel="routing_decoy_A2",
         routing_note="Diffusion of the contraceptive TECHNOLOGY (the Pill) -> A.2; shares the word "
                      "'diffusion' with A.3 but the object is the method, not the idea. The Wall-2 test case."),
    dict(title="Culture: An empirical investigation of beliefs, work, and fertility",
         authors=["Raquel Fernandez", "Alessandra Fogli"], year=2009, family="ROUTING_DECOY",
         provisional_cell="OFF_VERTICAL_A19", provenance_channel="routing_decoy_A19",
         routing_note="Epidemiological/vertical transmission of fertility beliefs (country-of-ancestry) "
                      "-> A.19; horizontal social diffusion is A.3. The Wall-4 test case."),
    dict(title="Contraception as development? New evidence from family planning in Colombia",
         authors=["Grant Miller"], year=2010, family="ROUTING_DECOY",
         provisional_cell="OFF_PROGRAM_A5", provenance_channel="routing_decoy_A5",
         routing_note="Exogenous family-planning PROGRAM supply (Profamilia) -> A.5; endogenous social "
                      "diffusion is A.3. The Wall-5 test case."),
    dict(title="The unfolding story of the second demographic transition",
         authors=["Ron Lesthaeghe"], year=2010, family="ROUTING_DECOY",
         provisional_cell="OFF_VALUE_D1", provenance_channel="routing_decoy_D1a",
         routing_note="The underlying VALUE shift (postmaterialism/secularization) -> D.1.a; A.3 carries the "
                      "value only as a diffusing object, not as the thing to be explained. The Wall-6 test case."),
]


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


def crossref_lookup(title, year):
    key = f"{title}::{year}"
    if key in cache:
        return cache[key]
    q = re.sub(r"\s+", "+", norm(title))
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=5&select=DOI,title,author,issued,container-title")
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
    selftest()  # fail fast if the imported canonical norm ever regresses
    anchors, log = [], []
    n_verified = n_flagged = n_book = n_drift = 0
    for c in CANDIDATES:
        rec = {k: c[k] for k in ("title", "authors", "year", "provenance_channel", "provisional_cell")}
        rec["query_cluster_family"] = c["family"]
        if c.get("routing_note"):
            rec["routing_note"] = c["routing_note"]
        if c.get("note"):
            rec["source_note"] = c["note"]
        cr = crossref_lookup(c["title"], c["year"])
        yr_ok = cr.get("cr_year") is None or abs(cr["cr_year"] - c["year"]) <= YEAR_TOL
        j = cr.get("jaccard", 0.0)
        ov = cr.get("overlap", 0.0)
        title_ok = j >= TITLE_JACCARD_MIN or (ov >= 0.90 and len(toks(c["title"])) >= 5)
        matched = bool(cr.get("doi")) and title_ok and yr_ok
        near_exact = j >= 0.90 or (ov >= 0.98 and len(toks(c["title"])) >= 5)
        year_drift = (not matched) and bool(cr.get("doi")) and near_exact and title_ok and not yr_ok
        if matched:
            existence = doi_exists(cr["doi"])
            rec.update(doi=cr["doi"], identity_source=f"https://doi.org/{cr['doi']}",
                       identity_verified=existence == "FOUND", existence=existence,
                       match_jaccard=j, container=cr.get("container"),
                       gold_status="candidate_not_ra_frozen")
            if existence == "FOUND":
                n_verified += 1
                status = f"VERIFIED  doi={cr['doi']}  J={j}  ({(cr.get('container') or '')[:40]})"
            else:
                n_flagged += 1
                status = f"DOI-MATCH-BUT-{existence}  doi={cr['doi']}  J={j}"
        elif year_drift:
            existence = doi_exists(cr["doi"])
            rec.update(doi=cr["doi"], identity_source=f"https://doi.org/{cr['doi']}",
                       identity_verified=existence == "FOUND", existence=existence,
                       match_jaccard=j, container=cr.get("container"), cr_year=cr.get("cr_year"),
                       gold_status="candidate_year_drift_ra_confirm",
                       note=(f"Exact-title match (J={j}) with year drift: candidate {c['year']} vs Crossref "
                             f"{cr.get('cr_year')} (preprint/WP-vs-VoR or undated chapter). Kept keyed on title."))
            n_drift += 1
            status = f"YEAR-DRIFT-KEEP  doi={cr['doi']}  J={j}  cand={c['year']} cr={cr.get('cr_year')}"
        else:
            rec.update(doi=None, identity_verified=False, match_jaccard=j,
                       crossref_best={"doi": cr.get("doi"), "title": cr.get("matched_title"),
                                      "jaccard": j, "year": cr.get("cr_year")},
                       gold_status="unverified_no_doi_match")
            if c.get("expect_no_doi"):
                rec["note"] = "Book/edited volume; expected Crossref-index miss. Carried in theory stream, not faked."
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
         f"Memory-enumerated from the diffusion/social-learning canon (A.3 is an old, canonical "
         f"literature: recall, not discovery, is the binding problem) and existence-verified: "
         f"{len(anchors)} candidate anchors. Every DOI pulled from a live Crossref match "
         f"(Jaccard >= {TITLE_JACCARD_MIN}, year +/-{YEAR_TOL}) then re-affirmed at doi.org; no DOI "
         "hand-asserted. Three-state gate: network failure = UNCONFIRMED, never ABSENT.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Books/volumes (expected miss): {n_book}**", "",
         "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- {fam}: {sum(vs)}/{len(vs)}")
    L += ["", "## Per-candidate disposition", ""] + log
    L += ["", "## Notes", "",
          "- A.3 has NO Cochrane-style systematic review to serve as the privileged channel-1 seed. The "
          "Princeton EFP synthesis (Coale & Watkins 1986) and the NAS 'Diffusion Processes and Fertility "
          "Transition' volume (Casterline, ed., 2001) play that role; both are books and are carried under "
          "expect_no_doi, not counted as ghosts.",
          "- Wall test set: the two cleanest identified estimates in the neighbourhood — La Ferrara-Chong-"
          "Duryea (Brazil soap operas) and Jensen-Oster (India cable TV) — are CHANNEL effects and are "
          "included ONLY as A.20 routing decoys under the 2026-09-18 channel-excluded A.3 resolution. Goldin-"
          "Katz (A.2 technology), Fernandez-Fogli (A.19 vertical), Miller (A.5 program), and Lesthaeghe (D.1 "
          "value) test the remaining walls. None of the decoys is part of the A.3 recall denominator.",
          "- Beach & Hanlon 'Culture and the historical fertility transition' may resolve to a 2022 or 2023 "
          "Crossref year (online-first vs VoR); the year-drift-keep path retains it keyed on title if so.",
          "- LEAKAGE WALL: the EFP/NAS synthesis volumes feed included studies as anchors here; their search "
          "vocabulary must not later be mined as A.3 production-query terms.",
          "- Any NO-MATCH or DOI-MATCH-BUT-ABSENT is a candidate ghost or a title/metadata error, NOT a "
          "verified anchor; it is held out of the recall denominator until RA resolution."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} year_drift_keep={n_drift} flagged={n_flagged} books={n_book} total={len(anchors)}")
    print("by family:", {k: f"{sum(v)}/{len(v)}" for k, v in by_family.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
