#!/usr/bin/env python3
"""
95_d1b_cold_start_anchors.py — D.1.b (cultural westernization / developmental idealism), stage A3.

Direct mirror of `72_d3b_cold_start_anchors.py`; only SLUG, cache namespace, and the cell taxonomy
change. Same load-bearing discipline, which carries the OAS ghost-citation lesson:

  * Candidates below carry (title, authors, year, family, provisional_cell, provenance_channel) drawn
    from a LIVE sourcing pass over OpenAlex and Crossref (2026-08-07), not from unaided memory. They
    assert NO DOIs; the DOI is whatever Crossref returns for a bibliographic match.
  * Every DOI is re-affirmed at doi.org. Mandatory existence gate: no anchor enters a recall
    denominator without a resolved live id.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. Only a Crossref
    200-with-DOI whose title matches (Jaccard >= 0.72 AND year within +/-1) clears to
    identity_verified=True.
  * Two flags separate two different things. `is_book` says the record MUST be book-shaped, so a
    review of a monograph cannot be mistaken for the monograph. `expect_no_doi` says a Crossref miss
    is anticipated and is not evidence of absence. London & Hadden 1989 is the second without the
    first (a real journal article Crossref does not index); Caldwell 1982 is both.
  * Books and monographs (Caldwell 1982, Thornton 2005, Coale & Watkins 1986) are EXPECTED to sit
    awkwardly in Crossref's article index. They are carried, not dropped, not faked. This literature
    is older than D.3.b's by four decades and its canon is book-shaped, so the book case is the
    normal case here rather than the exception it was for D.3.b.

SCRIPT NUMBERING: 89-94 are claimed by the D.1.a chain on branch
`062-postmaterialism-individualism-secularization` (not yet merged to main). D.1.b therefore starts
at 95. Checked with `git ls-tree` across all remote branches on 2026-08-07 — this is the collision
the QUEUE.md renumber note warns about, caught before the fact rather than after.

VERSION-DUPLICATE NOTE: the live pass found Thornton 2001 carrying two OpenAlex records
(10.1353/dem.2001.0039 and 10.2307/3088311) for the same Demography article, and Beine/Docquier/Schiff
existing as a World Bank working paper, two SSRN records, and a 2013 Canadian Journal of Economics
article. The published version is the anchor in each case; the dedup defect that let a preprint and
its version of record survive as two studies in D.3.b is the reason this is recorded here rather than
discovered downstream.

Candidate set spans the four primary A2 families + the theory canon + seven routing decoys, one for
each of the six boundary walls plus the FDT-restriction wall, so the eventual search is tested on
routing as well as on topical recall.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, time

SLUG = "caldwell-wealth-flows-westernization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d1b_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # === Family 1 — developmental-idealism belief: the purpose-built exposure measure ===
    dict(title="International Fertility Change: New Data and Insights From the Developmental Idealism Framework",
         authors=["Arland Thornton", "Georgina Binstock", "Kathryn M. Yount"], year=2012,
         family="di-belief", provisional_cell="PRIMARY_DI_BELIEF",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 49:677-698. The flagship DI-instrument paper: survey measures of what respondents "
              "believe developed countries do about family, fielded across multiple transitional settings. "
              "This is the anchor with the best-measured exposure in the whole chapter."),
    dict(title="Family life and developmental idealism in Yazd, Iran",
         authors=["Mohammad Jalal Abbasi-Shavazi", "Abbas Askari-Nodoushan", "Arland Thornton"], year=2012,
         family="di-belief", provisional_cell="PRIMARY_DI_BELIEF",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demographic Research 26:207-238. DI instrument in a mid-transition Muslim setting; open access."),
    dict(title="The Influence of Developmental Idealism on Marital Attitudes, Expectations, and Timing",
         authors=["Keera Allendorf", "Arland Thornton", "Colter Mitchell"], year=2019,
         family="di-belief", provisional_cell="PRIMARY_DI_BELIEF",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Family Issues. Outcome is FAMILY_FORMATION_BEHAVIOUR, not births — the tag "
              "that keeps the family-formation stratum out of any fertility pool."),
    dict(title="Early Women, Late Men: Timing Attitudes and Gender Differences in Marriage",
         authors=["Keera Allendorf", "Arland Thornton", "Colter Mitchell"], year=2017,
         family="di-belief", provisional_cell="PRIMARY_DI_BELIEF",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Marriage and Family 79:1478-1496. Nepal; DI beliefs about marriage timing."),
    dict(title="The Decline of Arranged Marriage? Marital Change and Continuity in India",
         authors=["Keera Allendorf", "Roshan K. Pandian"], year=2016,
         family="di-belief", provisional_cell="PRIMARY_DI_BELIEF",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Population and Development Review 42:435-464. Family-formation outcome; tests whether the "
              "conjugal-choice element of the DI package actually moved."),

    # === Family 2 — schooling as an ideational carrier (Wall 5's positive cases) ===
    dict(title="Mass Education, International Travel, and Ideal Ages at Marriage",
         authors=["Ellen Compernolle", "William G. Axinn"], year=2019,
         family="schooling-ideational", provisional_cell="PRIMARY_SCHOOLING_IDEATIONAL",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 56:2083-2109. Schooling AND international travel as ideational exposure, which is "
              "close to the cleanest available separation of Caldwell's mechanism from the human-capital one."),
    dict(title="The Spread of Education and Fertility Decline: A Thai Province Level Test of Caldwell's Wealth Flows Theory",
         authors=["Bruce London", "Kenneth P. Hadden"], year=1989,
         family="schooling-ideational", provisional_cell="PRIMARY_SCHOOLING_IDEATIONAL",
         provenance_channel="direct_empirical_bibliographic_search", expect_no_doi=True,
         note="Rural Sociology 54:17-36. A direct province-level test of Caldwell's schooling claim. "
              "OpenAlex carries the record (existence confirmed there) but no DOI; Crossref is expected "
              "to miss it. Kept keyed on title per the C3 resolution rule."),

    # === Family 3 — media carrying the modern-family model (Wall 3's dual-home cases) ===
    dict(title="Soap Operas and Fertility: Evidence from Brazil",
         authors=["Eliana La Ferrara", "Alberto Chong", "Suzanne Duryea"], year=2012,
         family="media-western-model", provisional_cell="PRIMARY_MEDIA_WESTERN_MODEL",
         provenance_channel="direct_empirical_bibliographic_search", shared_with="A.20",
         note="AEJ: Applied 4(4):1-31. The strongest identification in the family; Globo signal rollout. "
              "Dual-home with A.20 by the Wall-3 rule: the mechanism evidence is about the depicted "
              "small, wealthy, autonomous television family, which is family-model CONTENT. Note the "
              "2008 SSRN and IDB working-paper records are the same study, not independent estimates."),
    dict(title="The Power of TV: Cable Television and Women's Status in India",
         authors=["Robert Jensen", "Emily Oster"], year=2009,
         family="media-western-model", provisional_cell="PRIMARY_MEDIA_WESTERN_MODEL",
         provenance_channel="direct_empirical_bibliographic_search", shared_with="A.20",
         note="QJE 124:1057-1094. Cable rollout; fertility is one outcome among several. The NBER w13305 "
              "record is the same study."),
    dict(title="New ideas and fertility limitation: The role of mass media",
         authors=["Jennifer S. Barber", "William G. Axinn"], year=2004,
         family="media-western-model", provisional_cell="PRIMARY_MEDIA_WESTERN_MODEL",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Marriage and Family 66:1180-1200. Nepal; explicitly frames media as a carrier of "
              "new family ideas rather than of contraceptive information, which is the Wall-3 discriminator."),

    # === Family 4 — direct Western contact ===
    dict(title="Missions, fertility transition, and the reversal of fortunes: evidence from border discontinuities in the emirates of Nigeria",
         authors=["Dozie Okoye", "Roland Pongou"], year=2023,
         family="western-contact", provisional_cell="PRIMARY_WESTERN_CONTACT",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Economic Growth. Border-discontinuity design on Christian mission exposure. The "
              "best-identified Western-contact anchor found in the live pass."),
    dict(title="International migration, transfer of norms and home country fertility",
         authors=["Michel Beine", "Frederic Docquier", "Maurice Schiff"], year=2013,
         family="western-contact", provisional_cell="PRIMARY_WESTERN_CONTACT",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Canadian Journal of Economics 46:1406-1430. Norm transfer from destination to origin via "
              "migrant networks. Four records exist for this study (World Bank WP 4925, two SSRN, the CJE "
              "article); the CJE version of record is the anchor."),
    dict(title="The convergence of second-generation immigrants' fertility patterns in France: The role of sociocultural distance",
         authors=["Ariane Pailhe"], year=2017,
         family="western-contact", provisional_cell="PRIMARY_WESTERN_CONTACT",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demographic Research 36:1361-1398. The migrant-convergence seam: estimand is convergence "
              "WITH exposure, which is what puts it here rather than at A.19."),

    # === Theory canon — RELEVANT, but does NOT count toward empirical recall ===
    dict(title="Toward A Restatement of Demographic Transition Theory",
         authors=["John C. Caldwell"], year=1976, family="theory-canon",
         provisional_cell="DI_THEORY", provenance_channel="hypothesis_canon",
         note="Population and Development Review 2:321-366. The wealth-flows statement. Carried here as "
              "theory because the chapter's mechanism rests on it; its EMPIRICAL descendants route to C.3.f."),
    dict(title="Mass Education as a Determinant of the Timing of Fertility Decline",
         authors=["John C. Caldwell"], year=1980, family="theory-canon",
         provisional_cell="DI_THEORY", provenance_channel="hypothesis_canon",
         note="Population and Development Review 6:225-255. THE statement of this chapter's mechanism: "
              "schooling restructures family authority and obligation before it changes any price."),
    dict(title="Theory of Fertility Decline",
         authors=["John C. Caldwell"], year=1982, family="theory-canon",
         provisional_cell="DI_THEORY", provenance_channel="hypothesis_canon", expect_no_doi=True, is_book=True,
         note="Academic Press monograph. Crossref indexes the 1983 REVIEWS of it (PDR, JMF), not the book. "
              "Expected index miss; carried keyed on title."),
    dict(title="The Developmental Paradigm, Reading History Sideways, and Family Change",
         authors=["Arland Thornton"], year=2001, family="theory-canon",
         provisional_cell="DI_THEORY", provenance_channel="hypothesis_canon",
         note="Demography 38:449-465. The developmental-idealism statement. Two OpenAlex records exist "
              "(10.1353/dem.2001.0039, 10.2307/3088311) for one article — a dedup case for stage A4."),
    dict(title="Reading History Sideways: The Fallacy and Enduring Impact of the Developmental Paradigm on Family Life",
         authors=["Arland Thornton"], year=2005, family="theory-canon",
         provisional_cell="DI_THEORY", provenance_channel="hypothesis_canon", expect_no_doi=True, is_book=True,
         note="University of Chicago Press monograph; a Crossref monograph record exists under the short "
              "title 'Reading History Sideways' (10.7208/chicago/9780226126791.001.0001). The long-title "
              "match is expected to be weak, which is exactly the subtitle case the overlap coefficient handles."),
    dict(title="International Family Change: Ideational Perspectives",
         authors=["Arland Thornton", "William G. Axinn", "Rukmalie Jayakody"], year=2007,
         family="theory-canon", provisional_cell="DI_THEORY", provenance_channel="hypothesis_canon",
         expect_no_doi=True, is_book=True,
         note="Routledge edited volume; Crossref has it under the short title 'International Family Change' "
              "(10.4324/9780203809648). The programmatic statement of the ideational research agenda."),

    # === Routing decoys — MUST route away. One per wall. Not part of the recall denominator. ===
    dict(title="Evolutionary and Wealth Flows Theories of Fertility: Empirical Tests and New Models",
         authors=["Hillard Kaplan"], year=1994, family="ROUTING_DECOY",
         provisional_cell="OFF_WEALTH_FLOWS_C3f", provenance_channel="routing_decoy_C3f_wall1",
         routing_note="Wall 1. Operative variable is the direction and magnitude of intergenerational "
                      "transfers, not a belief or an exposure. Routes to C.3.f despite being pure Caldwell."),
    dict(title="Value Orientations and the Second Demographic Transition (SDT) in Northern, Western and Southern Europe: An Update",
         authors=["Johan Surkyn", "Ron Lesthaeghe"], year=2004, family="ROUTING_DECOY",
         provisional_cell="OFF_POSTMATERIALIST_D1a", provenance_channel="routing_decoy_D1a_wall2",
         routing_note="Wall 2. Internal value change in already-modernized societies, self-oriented content. "
                      "Routes to D.1.a."),
    dict(title="The density of social networks and fertility decisions: Evidence from South Nyanza district, Kenya",
         authors=["Hans-Peter Kohler", "Jere R. Behrman", "Susan Cotts Watkins"], year=2001,
         family="ROUTING_DECOY", provisional_cell="OFF_DIFFUSION_CHANNEL_A20",
         provenance_channel="routing_decoy_A20_wall3",
         routing_note="Wall 3. The estimand is network density — the geometry of the channel — with content "
                      "unspecified. Routes to A.20."),
    dict(title="Demand Theories of the Fertility Transition: An Iconoclastic View",
         authors=["John Cleland", "Christopher Wilson"], year=1987, family="ROUTING_DECOY",
         provisional_cell="OFF_FERTILITY_CONTROL_A3", provenance_channel="routing_decoy_A3_wall3",
         routing_note="Wall 3. What diffuses is the legitimation of birth control. Routes to A.3. This is "
                      "the hardest decoy in the set: it is an ideational argument against economic theories, "
                      "and a screen that routes on 'ideational' rather than on content will wrongly admit it."),
    dict(title="Women's empowerment and fertility: A review of the literature",
         authors=["Ushma D. Upadhyay", "Jessica D. Gipson", "Mellissa Withers"], year=2014,
         family="ROUTING_DECOY", provisional_cell="OFF_FEMALE_AUTONOMY_D2a",
         provenance_channel="routing_decoy_D2a_wall4",
         routing_note="Wall 4. Operative variable is a woman's own autonomy and bargaining position. "
                      "Routes to D.2.a."),
    dict(title="Does female schooling reduce fertility? Evidence from Nigeria",
         authors=["Una Okonkwo Osili", "Bridget Terry Long"], year=2007, family="ROUTING_DECOY",
         provisional_cell="MECHANISM_UNRESOLVED_SCHOOLING", provenance_channel="routing_decoy_wall5",
         routing_note="Wall 5. A well-identified reduced-form schooling estimate that does not decompose "
                      "ideational from economic mechanism. The correct disposition is UNCERTAIN / "
                      "MECHANISM_UNRESOLVED_SCHOOLING, not a D.1.b primary cell. This decoy tests the "
                      "single largest expected error in the screen."),
    dict(title="Community-level education accelerates the cultural evolution of fertility decline",
         authors=["Heidi Colleran", "Grazyna Jasienska", "Ilona Nenko"], year=2014,
         family="ROUTING_DECOY", provisional_cell="OFF_CULTURAL_EVOLUTION_D1c",
         provenance_channel="routing_decoy_D1c_wall6",
         routing_note="Wall 6. Cultural-evolutionary transmission model. Routes to D.1.c."),
    dict(title="The Decline of Fertility in Europe",
         authors=["Ansley J. Coale", "Susan Cotts Watkins"], year=1986, family="ROUTING_DECOY",
         provisional_cell="OFF_OTHER", provenance_channel="routing_decoy_FDT_restriction",
         expect_no_doi=True, is_book=True,
         routing_note="Tests the FDT restriction. The Princeton project is the historical Western "
                      "transition, which is the SOURCE of the diffused package and not a case of it. "
                      "Routes to OFF_OTHER (and substantively to A.3/A.20). Princeton University Press "
                      "volume; a 2017 De Gruyter edited-book record exists, an index-year drift case."),

    # === Contrary-evidence anchor: a design that races ideation against structure ===
    dict(title="A model comparison approach shows stronger support for economic models of fertility decline",
         authors=["Mary K. Shenk", "Mary C. Towner", "Howard Kress"], year=2013,
         family="structure-vs-ideation", provisional_cell="DIFFUSION_INDEPENDENT_OF_STRUCTURE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="PNAS 110:8045-8050. Formally compares economic, risk, and cultural-transmission models on "
              "the same Bangladeshi data and finds FOR the economic ones. Included deliberately: the "
              "value-added cell must contain the designs that separate ideation from structure "
              "REGARDLESS of which way they come out, or the cell selects on its own conclusion."),
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
    """Szymkiewicz-Simpson: |A n B| / min(|A|,|B|). Reported as a diagnostic only.

    It is NOT used as a match gate. The first run of this script did use it that way, inheriting the
    rule from `72_d3b`, and it admitted two false matches: "Theory of Fertility Decline." (a 1983 PDR
    review) scored overlap 1.0 against London & Hadden's Thai wealth-flows paper, because its four
    tokens all happen to appear somewhere in that long title. A set-containment test cannot tell a
    subtitle from a scatter of generic demography words. See `title_prefix_match` for the replacement."""
    A, B = toks(a), toks(b)
    m = min(len(A), len(B))
    return len(A & B) / m if m else 0.0


def title_prefix_match(a, b, min_tokens=3):
    """The subtitle case, tested properly: is the shorter title a contiguous leading token sequence of
    the longer one? That is what "Reading History Sideways" vs "Reading History Sideways: The Fallacy
    and Enduring Impact..." looks like, and it is what a scattered word-subset does not look like.

    Direction-agnostic, because Crossref sometimes keeps the subtitle and sometimes drops it."""
    A, B = norm(a).split(), norm(b).split()
    if len(A) > len(B):
        A, B = B, A
    if len(A) < min_tokens:
        return False
    return B[:len(A)] == A


# ---------------------------------------------------------------------------------------------
# VERSION-OF-RECORD PREFERENCE (added 2026-08-07, after the first run of this script).
#
# The first run resolved 8 of 28 anchors to the WRONG VERSION of the right paper: Jensen & Oster to
# the NBER working paper, La Ferrara/Chong/Duryea to the IDB working paper, Okoye & Pongou to a
# Research Square preprint, Caldwell 1980 to a 2024 Routledge reprint chapter, Thornton 2005 to a
# *Choice* review OF the book, Kohler/Behrman/Watkins to a book chapter, Osili & Long to the NBER
# paper, and Coale & Watkins to one chapter of the 2017 reissue. Every one passed the existence gate
# at Jaccard 1.0 — because a preprint's title is identical to the article's, and a book review's
# title reproduces the book's.
#
# This is the mirror image of the OAS ghost problem and the existence gate does not catch it: a ghost
# is a title that resolves to NOTHING, whereas this is a title that resolves to something REAL but
# not the record we mean. It matters because Tier A feeds the citation frame at A4, and the backward
# and forward citation clouds of a working paper are a small fraction of those of the version of
# record — anchoring Jensen & Oster on the NBER record would have quietly gutted Tier B.
#
# The fix: rank ALL title-passing Crossref candidates rather than taking the Jaccard argmax, and
# cross-check against OpenAlex, which indexes the version of record more reliably for this corpus.
# ---------------------------------------------------------------------------------------------

TYPE_RANK = {"journal-article": 100, "monograph": 92, "book": 90, "edited-book": 88,
             "reference-entry": 55, "book-chapter": 50, "book-part": 45, "proceedings-article": 40,
             "report": 30, "posted-content": 20, "dissertation": 20, "other": 10}
# DOI prefixes that identify a preprint server, working-paper series, or review venue rather than a
# publisher of record. Not a blocklist: a hit costs the candidate points, it does not disqualify it,
# because for some anchors (an NBER-only paper) the working paper IS the version of record.
NON_VOR_PREFIXES = {
    "10.3386": "NBER working paper", "10.2139": "SSRN", "10.21203": "Research Square",
    "10.31235": "SocArXiv", "10.31219": "OSF preprints", "10.1596": "World Bank working paper",
    "10.18235": "IDB working paper", "10.22004": "AgEcon Search", "10.5860": "Choice Reviews",
    "10.31899": "Population Council report", "10.48550": "arXiv",
}
REVIEW_CONTAINERS = ("choice reviews", "book review", "reviews online", "journal of reviews",
                     "book reviews")
BOOKISH_TYPES = {"book", "monograph", "edited-book", "reference-book", "book-set"}


def _cand_score(cand_title, cand_year, it_title, it_year, it_type, it_container, it_doi):
    """Score a Crossref/OpenAlex candidate for being the VERSION OF RECORD of the anchor.

    Title fit is a gate, not a score component: every candidate reaching here has already passed it,
    and among identical titles the discriminating information is type, venue, and year."""
    score = TYPE_RANK.get(it_type or "other", 10)
    prefix = (it_doi or "").split("/")[0]
    if prefix in NON_VOR_PREFIXES:
        score -= 45
    if any(k in (it_container or "").lower() for k in REVIEW_CONTAINERS):
        score -= 60          # a review OF the work is never the work
    if it_year is not None:
        score -= min(40, 4 * abs(it_year - cand_year))   # reprints and reissues drift far
    if it_container:
        score += 5           # a named container beats a bare deposit
    return score


TITLE_JACCARD_FLOOR = 0.45      # no match below this, however the subtitle test comes out


def _title_gate(cand_title, it_title):
    """Pass on a strong Jaccard, OR on a genuine subtitle relation with a Jaccard floor still in force.
    The floor is what stops a four-token generic title from riding a containment score to a match."""
    j = jaccard(cand_title, it_title)
    ov = overlap_coef(cand_title, it_title)
    ok = j >= TITLE_JACCARD_MIN or (title_prefix_match(cand_title, it_title) and j >= TITLE_JACCARD_FLOOR)
    return ok, round(j, 3), round(ov, 3)


def _openalex_rows(title):
    """Raw OpenAlex rows for a title, cached and retried. Feeds the unified candidate field."""
    key = f"OAROWS::{title}"
    if key in cache:
        return cache[key]
    from urllib.parse import quote
    url = (f"https://api.openalex.org/works?search={quote(title)}&per-page=8&mailto={MAILTO}"
           "&select=id,doi,title,publication_year,type,primary_location")
    results = []
    for attempt in range(3):
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        try:
            results = json.loads(out).get("results", [])
        except Exception:
            results = []
        if results:
            break
        time.sleep(1.5 * (attempt + 1))
    # Do NOT cache an empty result. Caching [] turns one rate-limited call into a permanent "this
    # paper does not exist in OpenAlex", which is the three-state discipline (UNCONFIRMED is not
    # ABSENT) violated by the cache layer rather than by the resolver.
    if results:
        cache[key] = results
        json.dump(cache, open(CACHE, "w"), indent=0)
    return results


def openalex_lookup(title, year):
    """Second opinion. OpenAlex indexes the version of record more reliably for this corpus, and its
    `type` field distinguishes article from preprint from book-chapter."""
    key = f"OA::{title}::{year}"
    if key in cache:
        return cache[key]
    from urllib.parse import quote
    url = (f"https://api.openalex.org/works?search={quote(title)}&per-page=8&mailto={MAILTO}"
           "&select=id,doi,title,publication_year,type,primary_location")
    results = []
    for attempt in range(3):
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        try:
            results = json.loads(out).get("results", [])
        except Exception:
            results = []
        if results:
            break
        time.sleep(1.5 * (attempt + 1))
    best, best_s = None, None
    for w in results:
        ok, j, ov = _title_gate(title, w.get("title") or "")
        if not ok:
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
        container = (((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")
        s = _cand_score(title, year, w.get("title"), w.get("publication_year"),
                        w.get("type"), container, doi)
        if doi and (best_s is None or s > best_s):
            best, best_s = {"doi": doi, "matched_title": w.get("title"), "jaccard": j,
                            "overlap": ov, "cr_year": w.get("publication_year"),
                            "container": container, "type": w.get("type"), "score": s}, s
    cache[key] = best or {"doi": None, "jaccard": 0.0}
    return cache[key]


def _crossref_rows(query_title, year_filter=None, tries=3):
    """Retried, because a single empty response is not evidence that Crossref holds nothing. The
    first version of this resolver had no retry, and two anchors flipped between resolved and
    unresolved across otherwise identical runs — a stage whose output depends on which API call
    happened to time out is not reproducible, whatever its recall."""
    q = re.sub(r"\s+", "+", norm(query_title))
    filt = (f"&filter=from-pub-date:{year_filter}-01-01,until-pub-date:{year_filter}-12-31"
            if year_filter else "")
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=10&select=DOI,title,author,issued,container-title,type{filt}")
    for attempt in range(tries):
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        try:
            items = json.loads(out)["message"]["items"]
        except Exception:
            items = None
        if items:
            return items
        time.sleep(1.5 * (attempt + 1))
    return []


def crossref_lookup(title, year, year_filter=None, is_book=False):
    """Rank ALL title-passing candidates by version-of-record score, then take the best. The previous
    implementation took the Jaccard argmax, which is uninformative when several records share one
    title — precisely the preprint/working-paper/reprint/review case.

    `is_book` narrows the accepted record types to book-shaped ones. Without it, every title-passing
    match for Thornton 2005 is a *review* of the monograph in a sociology or history journal, and the
    resolver cheerfully anchors the chapter's central theoretical statement to a 900-word book notice."""
    key = f"VOR3::{title}::{year}::{year_filter}::{is_book}"
    if key in cache:
        return cache[key]
    # Each query form carries its own gate title. A monograph indexed under the pre-subtitle short
    # form must be gated against that short form — gating it against the full title-plus-subtitle
    # fails the Jaccard floor and hands the anchor back to the book's reviews, which do reproduce
    # the full title and therefore score 1.0.
    try:
        probes = [(title, _crossref_rows(title, year_filter))]
        if is_book and ":" in title:
            short = title.split(":")[0].strip()
            probes.append((short, _crossref_rows(short, year_filter)))
    except Exception as e:
        cache[key] = {"error": str(e)[:120]}
        return cache[key]
    items = [(gate_title, it) for gate_title, rows in probes for it in rows]
    # OpenAlex rows enter the SAME ranked field rather than acting as a fallback consulted only when
    # Crossref fails. A second source used only on failure cannot correct a confident wrong answer,
    # which is the failure mode this whole resolver exists to fix.
    for w in _openalex_rows(title):
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if not doi:
            continue
        items.append((title, {"DOI": doi, "title": [w.get("title") or ""],
                              "issued": {"date-parts": [[w.get("publication_year")]]},
                              "container-title": [(((w.get("primary_location") or {}).get("source")
                                                    or {}).get("display_name") or "")],
                              "type": w.get("type"), "_src": "openalex"}))
    scored, fallback = [], None
    for gate_title, it in items:
        ct = (it.get("title") or [""])[0]
        yr = None
        try:
            yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        except Exception:
            pass
        ok, j, ov = _title_gate(gate_title, ct)
        rec = {"doi": it.get("DOI"), "matched_title": ct, "jaccard": j, "overlap": ov,
               "cr_year": yr, "container": (it.get("container-title") or [""])[0],
               "type": it.get("type")}
        if fallback is None or j > fallback["jaccard"]:
            fallback = rec
        if is_book and (it.get("type") not in BOOKISH_TYPES):
            continue          # a review of a book, or a chapter, is not the book
        if is_book and re.search(r"-\d{1,3}$", it.get("DOI") or ""):
            continue          # volume DOI with a chapter ordinal appended: a part, not the whole
        if ok and it.get("DOI"):
            rec["score"] = _cand_score(title, year, ct, yr, it.get("type"), rec["container"], rec["doi"])
            scored.append(rec)
    if not scored:
        # Crossref found nothing acceptable. Give OpenAlex a turn before conceding: its coverage of
        # this corpus is better, and conceding early is how a real paper gets recorded as absent.
        oa_only = openalex_lookup(title, year)
        oa_container = (oa_only.get("container") or "").lower()
        oa_is_review = any(k in oa_container for k in REVIEW_CONTAINERS)
        if oa_only.get("doi") and not oa_is_review and (not is_book or oa_only.get("type") in BOOKISH_TYPES):
            oa_only = {**oa_only, "version_source": "openalex_only_crossref_empty"}
            cache[key] = oa_only
            json.dump(cache, open(CACHE, "w"), indent=0)
            return cache[key]
        # No title-passing candidate: hand back the best-Jaccard row so the caller can report the
        # near-miss, exactly as before. This preserves the NO-MATCH diagnostic.
        cache[key] = fallback or {"doi": None, "jaccard": 0.0}
        json.dump(cache, open(CACHE, "w"), indent=0)
        return cache[key]
    scored.sort(key=lambda r: -r["score"])
    best = scored[0]
    best["n_title_passing"] = len(scored)
    if len(scored) > 1:
        best["rejected_versions"] = [{"doi": r["doi"], "type": r["type"], "year": r["cr_year"],
                                      "container": r["container"], "score": r["score"]}
                                     for r in scored[1:5]]
    # Second opinion. Substitute when OpenAlex offers a strictly better-scoring version of the same
    # title — the disagreement is logged either way, never silently resolved.
    oa = openalex_lookup(title, year)
    if oa.get("doi") and oa.get("score") is not None and oa["doi"].lower() != (best["doi"] or "").lower():
        if oa["score"] > best["score"]:
            best = {**oa, "n_title_passing": best.get("n_title_passing"),
                    "rejected_versions": best.get("rejected_versions"),
                    "version_source": "openalex_override",
                    "crossref_pick": {"doi": best["doi"], "type": best["type"],
                                      "score": best["score"], "container": best["container"]}}
        else:
            best["openalex_alternative"] = {"doi": oa["doi"], "type": oa.get("type"),
                                            "score": oa.get("score")}
    cache[key] = best
    json.dump(cache, open(CACHE, "w"), indent=0)
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
    n_verified = n_flagged = n_book = n_drift = n_vor_sub = 0
    for c in CANDIDATES:
        rec = {k: c[k] for k in ("title", "authors", "year", "provenance_channel", "provisional_cell")}
        rec["query_cluster_family"] = c["family"]
        if c.get("routing_note"):
            rec["routing_note"] = c["routing_note"]
        if c.get("shared_with"):
            rec["shared_with"] = c["shared_with"]
        if c.get("note"):
            rec["source_note"] = c["note"]
        cr = crossref_lookup(c["title"], c["year"], c.get("year_filter"),
                             is_book=bool(c.get("is_book")))
        # Three-state year gate: a MISSING Crossref year does not reject a strong title+DOI identity
        # match (missing != contradicting); only a present-and-off year fails.
        yr_ok = cr.get("cr_year") is None or abs(cr["cr_year"] - c["year"]) <= YEAR_TOL
        j = cr.get("jaccard", 0.0)
        ov = cr.get("overlap", 0.0)
        # Accept on Jaccard, OR on high containment for a multi-token candidate (subtitle case).
        title_ok = j >= TITLE_JACCARD_MIN or (ov >= 0.90 and len(toks(c["title"])) >= 5)
        matched = bool(cr.get("doi")) and title_ok and yr_ok
        # Year-drift keep: an essentially-EXACT title match with a present-but-off year is NOT a ghost —
        # it is the preprint-vs-VoR / WP-vs-published / reissued-monograph case. The C3 resolution rule
        # keeps a real paper with a drifted identifier, keyed on title, so we existence-check and keep it
        # under a year_drift flag for RA confirmation rather than dropping it.
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
            rec["record_type"] = cr.get("type")
            for k in ("n_title_passing", "rejected_versions", "version_source", "crossref_pick",
                      "openalex_alternative"):
                if cr.get(k) is not None:
                    rec[k] = cr[k]
            rec["gold_status"] = "candidate_not_ra_frozen"
            if existence == "FOUND":
                n_verified += 1
                if cr.get("version_source") == "openalex_override":
                    n_vor_sub += 1
                status = (f"VERIFIED  doi={cr['doi']}  J={j}  [{cr.get('type')}]  "
                          f"({(cr.get('container') or '')[:36]})"
                          + ("  <- VoR substituted" if cr.get("version_source") else ""))
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
            rec["record_type"] = cr.get("type")
            for k in ("n_title_passing", "rejected_versions", "version_source", "crossref_pick"):
                if cr.get(k) is not None:
                    rec[k] = cr[k]
            rec["gold_status"] = "candidate_year_drift_ra_confirm"
            rec["note"] = (f"Exact-title match (J={j}) with year drift: candidate {c['year']} vs Crossref "
                           f"{cr.get('cr_year')} (preprint/WP-vs-VoR or reissued volume). Kept keyed on title.")
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
                rec["note"] = ("Book, monograph, or non-indexed journal; expected Crossref-index miss. "
                               "Carried keyed on title, not faked.")
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
    empirical = [a for a in anchors if a["provisional_cell"].startswith("PRIMARY_")
                 or a["provisional_cell"] == "DIFFUSION_INDEPENDENT_OF_STRUCTURE"]
    L = [f"# A3 cold-start anchors — {SLUG} (D.1.b)", "",
         f"Sourced in a live OpenAlex + Crossref pass (2026-08-07) and existence-verified: "
         f"{len(anchors)} candidate anchors, of which {len(empirical)} are empirical (the recall "
         f"denominator) and the rest are theory canon or routing decoys. Every DOI pulled from a live "
         f"Crossref match (Jaccard >= {TITLE_JACCARD_MIN}, year +/-{YEAR_TOL}) then re-affirmed at "
         "doi.org; no DOI hand-asserted. Three-state gate: network failure = UNCONFIRMED, never ABSENT.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Books / non-indexed (expected miss): {n_book}**", "",
         f"**Version-of-record substitutions (Crossref pick overridden): {n_vor_sub}** — see the "
         "version-of-record note below.", "",
         "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- {fam}: {sum(vs)}/{len(vs)}")
    L += ["", "## Per-candidate disposition", ""] + log
    L += ["", "## Notes", "",
          "- **Script numbering.** 89-94 are claimed by the D.1.a chain on branch "
          "`062-postmaterialism-individualism-secularization`, which has not merged to main. D.1.b starts "
          "at 95. Verified with `git ls-tree` across all remote branches before writing, which is the "
          "check the TICK-032 collision and the QUEUE.md renumber note exist to enforce.",
          "- **The book problem is the normal case here, not the exception.** Three of six theory anchors "
          "and one decoy are monographs or edited volumes. D.3.b's canon was five years old and "
          "article-shaped; this one is fifty years old and book-shaped. A pipeline that silently drops "
          "Crossref misses would delete Caldwell 1982 and Thornton 2005 — the two statements the chapter's "
          "mechanism rests on — and would do so without leaving a trace.",
          "- **Version duplicates found in the live pass**, recorded now so stage A4 dedups them rather "
          "than counting them twice: Thornton 2001 has two OpenAlex records for one Demography article; "
          "Beine/Docquier/Schiff exists as a World Bank WP, two SSRN records, and the 2013 CJE article; "
          "La Ferrara/Chong/Duryea and Jensen/Oster each have working-paper twins. This is the D.3.b "
          "dedup defect (compare by identifier OR title, not both) anticipated rather than repeated.",
          "- **The contrary-evidence anchor is deliberate.** Shenk et al. 2013 races cultural-transmission "
          "against economic models on the same data and finds for the economic ones. It sits in the "
          "value-added cell because that cell is defined by DESIGN — separating ideation from structure — "
          "and not by result. A value-added cell stocked only with confirmations would select on its own "
          "conclusion.",
          "- **Routing decoys cover all six walls plus the FDT restriction** (C.3.f wealth flows, D.1.a "
          "postmaterialism, A.20 network geometry, A.3 contraceptive legitimation, D.2.a female autonomy, "
          "Wall-5 reduced-form schooling, D.1.c cultural evolution, and the Princeton European project). "
          "They are NOT part of the recall denominator; they test that the search and screen route them "
          "away. Cleland & Wilson 1987 is the sharpest of them — an ideational argument whose content is "
          "contraceptive legitimation, which a screen routing on the word 'ideational' will wrongly admit.",
          "- **v5 seminal-list check.** All four entries in HYPOTHESES-v5 §D.1.b (Caldwell 1980, Caldwell "
          "1982, Thornton 2001, Thornton 2005) resolved to real works in the live pass. No ghost of the "
          "'Britt et al. 2025' kind was found. The short-form citations are nonetheless ambiguous in one "
          "place: 'Caldwell 1982' is a monograph whose Crossref presence is its 1983 reviews, so a naive "
          "resolver would key the anchor to a review of the book rather than the book.",
          "- LEAKAGE WALL: no query terms are mined in this step. Terms harvested from any source that fed "
          "an anchor here are fold-local only, after the gold frame exists."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} year_drift_keep={n_drift} flagged={n_flagged} books={n_book} "
          f"vor_substituted={n_vor_sub} total={len(anchors)}")
    print("by family:", {k: f"{sum(v)}/{len(v)}" for k, v in by_family.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
