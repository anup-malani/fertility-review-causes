#!/usr/bin/env python3
"""
103_d2d_cold_start_anchors.py — D.2.d (child-centered intensive parenting norms), stage A3.

Descends from `72_d3b_cold_start_anchors.py` via `95_d1b_cold_start_anchors.py`, keeping their
discipline and fixing three defects that D.2.d's canon exposes and D.1.b's did not:

  * Candidates below carry (title, authors, year, family, provisional_cell, provenance_channel) drawn
    from a LIVE sourcing pass over OpenAlex and Crossref (2026-08-08), not from unaided memory. They
    assert NO DOIs; the DOI is whatever the indexes return for a bibliographic match.
  * Every DOI is re-affirmed at doi.org. Mandatory existence gate: no anchor enters a recall
    denominator without a resolved live id.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT.

WHY THIS SCRIPT DIVERGES FROM 95_d1b. The version-of-record problem is not a minority case here; for
this canon it is the DEFAULT, and D.1.b's resolver fails on it three separate ways. Measured in the
live pass:

  1. AUTHORS ARE THE ONLY DISCRIMINATOR, AND D.1.b HAS NO AUTHOR SIGNAL. Two same-title-different-book
     collisions in a four-book canon:
       - Lareau 2003 "Unequal Childhoods" -> the real UC Press record (10.1525/9780520949904) and
         Penn 2005 "Unequal Childhoods" (10.4324/9780203465349) BOTH score Jaccard 0.29.
       - Zelizer 1985 "Pricing the Priceless Child" attracts "Pricing the Priceless" by Newhouse
         (MIT 2002, J=0.33) and by Banzhaf (CUP 2023, J=0.33) — unrelated books that a subtitle-prefix
         test admits.
     Jaccard cannot separate 0.29 from 0.29. Author surnames separate every one of these cleanly, so
     `_author_match` is now a GATE for book anchors and a score component everywhere.

  2. THE TITLE FLOOR IS TUNED FOR ARTICLES AND SILENTLY DROPS MONOGRAPHS. Publishers deposit books
     under the pre-subtitle short title, so the TRUE match sits far below D.1.b's 0.45 floor:
     Lareau at 0.29, Doepke & Zilibotti "Love, Money, and Parenting" at 0.31. The first book probe of
     this session missed Lareau entirely for exactly this reason. Book anchors therefore use
     TITLE_JACCARD_FLOOR_BOOK, which is only reachable WITH an author match — the floor is lowered and
     the author gate takes over the discriminating work, rather than the floor being lowered alone.

  3. THE YEAR PENALTY PUNISHES BOOKS FOR THEIR OWN EBOOK DEPOSITS. Lareau 2003's UC Press DOI is
     stamped 2019; D.1.b's -4/year (capped -40) would hit the correct record with the maximum penalty.
     Year is near-uninformative for monographs and is down-weighted for book-shaped types.

FOUR ANCHORS ARE GENUINELY UNREACHABLE and are carried keyed on title, not faked. Hays 1996, Zelizer
1985, and Aries 1962 return ONLY reviews of themselves in both indexes — Hays produces six separate
review records at Jaccard 1.00 (Contemporary Sociology, Social Forces, Choice, PDR, JMF, J Clin
Psychiatry) and no monograph. An argmax resolver anchors this chapter's central theoretical statement
to a book review with perfect confidence. That is the failure this file exists to prevent.

SCRIPT NUMBERING: 88 is the highest on `main`; 89-94 are the D.1.a chain and 95-102 the D.1.b chain,
both on unmerged branches. D.2.d therefore starts at 103. Checked against all remote branches
2026-08-08.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, time

SLUG = "child-centeredness-intensive-parenting"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d2d_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1


def _openalex_key():
    """Ported from 96_d1b_tier_ab_frame.py. `mailto` identifies the caller but does not authenticate:
    it draws on a shared anonymous budget that a citation-frame build exhausts in minutes. Env first,
    then .env, then None — never inline, and never into a cache key or an exception message."""
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envf = os.path.join(ROOT, ".env")
    if os.path.exists(envf):
        for line in open(envf):
            if line.strip().startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


OA_KEY = _openalex_key()


def _oa_auth():
    return f"&api_key={OA_KEY}" if OA_KEY else ""


# --- Candidate anchors. NO DOIs here by design; the DOI is whatever the indexes return. ------------
CANDIDATES = [
    # === Family 1 — the parenting norm as measured exposure: the value-added empirical family ===
    dict(title="Ready for Parenthood? On Intensive Parenting Ideals and Fertility",
         authors=["Kerstin Ruckdeschel"], year=2024,
         family="norm-exposure", provisional_cell="PRIMARY_NORM_EXPOSURE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Journal of Family Issues. The single closest paper to this chapter's estimand found in "
              "the live pass: intensive-parenting IDEALS on the right-hand side, fertility on the left."),
    dict(title="Do Socioeconomic Differences in Family Size Reflect Cultural Differences in Confidence and Support for Parenting?",
         authors=["Lareen A. Newman"], year=2009,
         family="norm-exposure", provisional_cell="PRIMARY_NORM_EXPOSURE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Population Research and Policy Review 28. Asks whether the class gradient in family size "
              "runs through parenting norms rather than through prices, which is Wall 3 and Wall 2 in "
              "one design."),
    dict(title="How much do norms matter for quantity and quality of children?",
         authors=["Zainab Iftikhar"], year=2025,
         family="norm-exposure", provisional_cell="COST_INDEPENDENCE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="World Development. THE value-added-cell candidate: races norms against the Q-Q "
              "mechanism on the same data, which is exactly the Wall 1 separation the scope doc "
              "predicted would be rare. If COST_INDEPENDENCE is non-empty, it starts here."),

    # === Family 2 — measured parenting time and intensity ===
    dict(title="Intensive Parenting: Fertility and Breastfeeding Duration in the United States",
         authors=["Vida Maralani", "Samuel Stabler"], year=2018,
         family="time-intensity", provisional_cell="PRIMARY_TIME_INTENSITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 55. Title-level match to the hypothesis. Direction must be checked at "
              "extraction: this may well be a REVERSE design (fertility -> intensity), and it is "
              "carried partly BECAUSE it tests whether the screen can tell the two apart."),
    dict(title="The Time Cost of Raising Children in Different Fertility Contexts: Evidence from France and Italy",
         authors=["Anne Solaz", "Maria Letizia Tanturri"], year=2018,
         family="time-intensity", provisional_cell="PRIMARY_TIME_INTENSITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="European Journal of Population 34. Time cost per child across two fertility regimes — "
              "the cleanest available separation of the time-quantity channel from the wage channel "
              "(Wall 4)."),

    # === Family 3 — the perceived standard ===
    dict(title="Costly children: the motivations for parental investment in children in a low fertility context",
         authors=["Anne H. Gauthier", "Petra W. de Jong"], year=2021,
         family="perceived-standard", provisional_cell="PRIMARY_PERCEIVED_STANDARD",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Genus 77. Open access. Motivations for investment in a low-fertility setting; the "
              "standard is the object of measurement rather than an inferred residual."),
    dict(title="The good parent: Emerging themes and gender convergence in narrating fertility choices",
         authors=["Alessandra Minello", "Concetta Russo"], year=2025,
         family="perceived-standard", provisional_cell="PRIMARY_PERCEIVED_STANDARD",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Family Relations. Qualitative; respondents narrate fertility choice in terms of what a "
              "good parent owes a child. Outcome level will be STATED_INTENTION_OR_ATTITUDE."),

    # === Theory canon — RELEVANT, but does NOT count toward empirical recall ===
    dict(title="The Cultural Contradictions of Motherhood",
         authors=["Sharon Hays"], year=1996, family="theory-canon",
         provisional_cell="PARENTING_NORM_THEORY", provenance_channel="hypothesis_canon",
         expect_no_doi=True, is_book=True,
         note="Yale University Press. The founding statement of intensive mothering as an ideology. "
              "UNREACHABLE: both indexes return only REVIEWS — six at Jaccard 1.00 in OpenAlex "
              "(Contemporary Sociology, Social Forces, Choice, PDR, JMF, J Clin Psychiatry) and zero "
              "book-shaped Crossref records. Carried keyed on title."),
    dict(title="Unequal Childhoods: Class, Race, and Family Life",
         authors=["Annette Lareau"], year=2003, family="theory-canon",
         provisional_cell="PARENTING_NORM_THEORY", provenance_channel="hypothesis_canon",
         is_book=True,
         note="University of California Press; concerted cultivation. REACHABLE but only via the "
              "short-title + author path: the true record scores Jaccard 0.29, tied with Penn 2005's "
              "different book of the same name. This anchor is the reason `_author_match` is a gate."),
    dict(title="Love, Money, and Parenting: How Economics Explains the Way We Raise Our Kids",
         authors=["Matthias Doepke", "Fabrizio Zilibotti"], year=2019, family="theory-canon",
         provisional_cell="PARENTING_NORM_THEORY", provenance_channel="hypothesis_canon",
         is_book=True,
         note="Princeton University Press. Two records for one book — 10.1515/9780691184210 (2018 "
              "edited-book deposit) and 10.2307/j.ctvc77fr1 (2019 monograph); the 2019 monograph is "
              "the VoR. Short-title Jaccard 0.31. Three separate review records also exist."),
    dict(title="Parenting With Style: Altruism and Paternalism in Intergenerational Preference Transmission",
         authors=["Matthias Doepke", "Fabrizio Zilibotti"], year=2017, family="theory-canon",
         provisional_cell="PARENTING_NORM_THEORY", provenance_channel="hypothesis_canon",
         note="Econometrica 85. The formal model behind the book. FOUR non-VoR records share this "
              "title at Jaccard 1.00 (NBER w20214, three SSRN deposits); the Econometrica record is "
              "the anchor. A pure argmax resolver picks among these five at random."),
    dict(title="Social Class, Gender, and Contemporary Parenting Standards in the United States",
         authors=["Patrick Ishizuka"], year=2019, family="theory-canon",
         provisional_cell="PARENTING_NORM_CONSTRUCT", provenance_channel="hypothesis_canon",
         note="Social Forces 98. Survey-experimental measurement of the parenting STANDARD itself. "
              "Indexed under publication_year 2018 (online-first), so this anchor exercises the "
              "year-tolerance path deliberately."),
    dict(title="The Rug Rat Race",
         authors=["Garey Ramey", "Valerie A. Ramey"], year=2010, family="theory-canon",
         provisional_cell="PARENTING_NORM_CONSTRUCT", provenance_channel="hypothesis_canon",
         note="Brookings Papers on Economic Activity. The time-use documentation of rising childcare "
              "time concentrated among the college-educated. SEVEN competing records at Jaccard 1.00 "
              "(NBER w15284, SSRN, four RePEc); the Brookings article is the VoR."),
    dict(title="“If I’m Going to Do It, I’m Going to Do It Right”: Intensive Mothering Ideologies among Childless Women",
         authors=["Kit Myers"], year=2017, family="theory-canon",
         provisional_cell="PARENTING_NORM_CONSTRUCT", provenance_channel="direct_empirical_bibliographic_search",
         note="Gender & Society 31. Intensive-mothering ideology among CHILDLESS women, which is the "
              "rare design where the norm cannot be a post-hoc rationalization of realized parity — "
              "directly relevant to the reverse-causation caution."),

    # === FDT context stream — Call 1. RELEVANT, never pooled, outside the SDT denominator. ===
    dict(title="Pricing the Priceless Child: The Changing Social Value of Children",
         authors=["Viviana A. Zelizer"], year=1985, family="fdt-context",
         provisional_cell="FDT_SENTIMENTALIZATION_CONTEXT", provenance_channel="hypothesis_canon",
         expect_no_doi=True, is_book=True,
         note="Basic Books / Princeton. The 1870-1930 revaluation of the child from economically "
              "useful to emotionally priceless. UNREACHABLE: six review records at Jaccard 1.00 and "
              "no monograph. Also attracts two FALSE short-title matches — 'Pricing the Priceless' by "
              "Newhouse (MIT 2002) and by Banzhaf (CUP 2023) — which only the author gate rejects."),
    dict(title="Centuries of Childhood: A Social History of Family Life",
         authors=["Philippe Ariès"], year=1962, family="fdt-context",
         provisional_cell="FDT_SENTIMENTALIZATION_CONTEXT", provenance_channel="hypothesis_canon",
         expect_no_doi=True, is_book=True,
         note="Knopf. The invention-of-childhood thesis. UNREACHABLE: reviews only, plus a 2018 Macat "
              "study-guide ABOUT the book (10.4324/9781912281305) that a naive resolver would take."),

    # === Routing decoys — MUST route away. One per wall. Not part of the recall denominator. ===
    dict(title="On the Interaction between the Quantity and Quality of Children",
         authors=["Gary S. Becker", "H. Gregg Lewis"], year=1973, family="ROUTING_DECOY",
         provisional_cell="OFF_QQ_C3d", provenance_channel="routing_decoy_C3d_wall1",
         routing_note="Wall 1. The founding Q-Q statement. Operative variable is the shadow price of "
                      "quality, not a norm. Routes to C.3.d — and it is the decoy most likely to be "
                      "wrongly admitted, because every D.2.d paper cites it."),
    dict(title="Why did rich families increase their fertility? Inequality and marketization of child care",
         authors=["Moshe Hazan", "Hosny Zoabi"], year=2018, family="ROUTING_DECOY",
         provisional_cell="OFF_INEQUALITY_C2f", provenance_channel="routing_decoy_C2f_wall2",
         routing_note="Wall 2. Identifies off inequality and the price of marketized childcare. Its "
                      "narrative is entirely about parenting intensity, which is precisely why it "
                      "routes to C.2.f and not here. The Call-2 rule in operation."),
    dict(title="Parenting on a budget",
         authors=["Severin Rapp", "Olivier Thévenon"], year=2025, family="ROUTING_DECOY",
         provisional_cell="OFF_DIRECT_COST_C2b", provenance_channel="routing_decoy_C2b_wall3",
         routing_note="Wall 3. A money aggregate — expenditure per child — with no norm measured. "
                      "Routes to C.2.b however intensive-parenting-flavored the framing."),
    dict(title="Completed Fertility and its Timing: An Economic Analysis of U.S. Experience Since World War II",
         authors=["William P. Butz", "Michael P. Ward"], year=1979, family="ROUTING_DECOY",
         provisional_cell="OFF_TIMECOST_C2e", provenance_channel="routing_decoy_C2e_wall4",
         routing_note="Wall 4. The price of the mother's time, not the quantity the norm demands. "
                      "Routes to C.2.e."),
    dict(title="Home Alone: Exploring Childcare Options to Remove Barriers to Second Childbearing",
         authors=["Kamila Ishchanova"], year=2022, family="ROUTING_DECOY",
         provisional_cell="OFF_CHILDCARE_C2a", provenance_channel="routing_decoy_C2a_wall5",
         routing_note="Wall 5. Childcare supply and options as the intervention. Routes to C.2.a. "
                      "Distinguished from D.2.d's claim that the norm makes parental care "
                      "non-substitutable, which is a belief and not a supply curve."),
    dict(title="Women’s housework decreases fertility",
         authors=["Anneli Miettinen", "Lassi Lainiala", "Anna Rotkirch"], year=2015, family="ROUTING_DECOY",
         provisional_cell="OFF_GENDER_D2a", provenance_channel="routing_decoy_D2a_wall6",
         routing_note="Wall 6. The division of domestic labour BETWEEN partners, not the level of "
                      "care a child is owed. Routes to D.2.a."),
    dict(title="Trade-offs in modern parenting: a longitudinal study of sibling competition for parental care",
         authors=["David W. Lawson", "Ruth Mace"], year=2009, family="ROUTING_DECOY",
         provisional_cell="REVERSE", provenance_channel="routing_decoy_reverse",
         routing_note="The reverse-causation decoy, and the most important one in the set. Parity "
                      "DRIVES investment per child here — the arithmetic identity the scope doc names "
                      "as the first-order threat. A screen that admits this as PRIMARY_TIME_INTENSITY "
                      "has inverted the hypothesis."),
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
    """Szymkiewicz-Simpson. Diagnostic only, never a match gate — see 95_d1b's note on why a
    set-containment test cannot tell a subtitle from a scatter of generic words."""
    A, B = toks(a), toks(b)
    m = min(len(A), len(B))
    return len(A & B) / m if m else 0.0


def title_prefix_match(a, b, min_tokens=3):
    """Is the shorter title a contiguous LEADING token sequence of the longer one? That is what a
    publisher's short-title deposit looks like and what a scattered word-subset does not.

    Necessary but NOT sufficient here, which is the D.2.d correction: 'Pricing the Priceless' is a
    true prefix of 'Pricing the Priceless Child: The Changing Social Value of Children' and is a
    different book by a different author. The author gate is what rejects it."""
    A, B = norm(a).split(), norm(b).split()
    if len(A) > len(B):
        A, B = B, A
    if len(A) < min_tokens:
        return False
    return B[:len(A)] == A


def _surnames(authors):
    """Last whitespace-delimited token of each author string, lowercased and de-accented enough for
    comparison. Crossref returns `family` directly; our candidates carry full names."""
    out = set()
    for a in authors or []:
        parts = norm(a).split()
        if parts:
            out.add(parts[-1])
    return out


def _author_match(cand_authors, item_authors):
    """Three-state, because absence of author metadata is not disagreement.

    Returns True (a surname overlaps), False (both sides have authors and NONE overlap), or None
    (one side has no author metadata — uninformative, must not be treated as a rejection). D.1.b has
    no author signal at all; on this canon that is the difference between anchoring Lareau 2003 and
    anchoring a different book with the same title."""
    A, B = _surnames(cand_authors), _surnames(item_authors)
    if not A or not B:
        return None
    return bool(A & B)


# ---------------------------------------------------------------------------------------------
# VERSION-OF-RECORD PREFERENCE. Inherited from 95_d1b (decisions/2026-08-07-version-of-record-gate.md)
# and extended with the author signal and book-aware thresholds motivated in the module docstring.
# ---------------------------------------------------------------------------------------------

TYPE_RANK = {"journal-article": 100, "monograph": 92, "book": 90, "edited-book": 88,
             "reference-entry": 55, "book-chapter": 50, "book-part": 45, "proceedings-article": 40,
             "report": 30, "posted-content": 20, "dissertation": 20, "other": 10}
NON_VOR_PREFIXES = {
    "10.3386": "NBER working paper", "10.2139": "SSRN", "10.21203": "Research Square",
    "10.31235": "SocArXiv", "10.31219": "OSF preprints", "10.1596": "World Bank working paper",
    "10.18235": "IDB working paper", "10.22004": "AgEcon Search", "10.5860": "Choice Reviews",
    "10.31899": "Population Council report", "10.48550": "arXiv",
}
REVIEW_CONTAINERS = ("choice reviews", "book review", "reviews online", "journal of reviews",
                     "book reviews", "contemporary sociology")
BOOKISH_TYPES = {"book", "monograph", "edited-book", "reference-book", "book-set"}

TITLE_JACCARD_FLOOR = 0.45          # articles: the D.1.b floor, unchanged
TITLE_JACCARD_FLOOR_BOOK = 0.25     # books: reachable ONLY with a positive author match


def _cand_score(cand_title, cand_year, cand_authors, it_title, it_year, it_type,
                it_container, it_doi, it_authors):
    """Score a candidate for being the VERSION OF RECORD. Title fit is a gate, not a score component:
    every candidate reaching here has passed it, and among identical titles the discriminating
    information is author, type, venue, and year."""
    score = TYPE_RANK.get(it_type or "other", 10)
    prefix = (it_doi or "").split("/")[0]
    if prefix in NON_VOR_PREFIXES:
        score -= 45
    if any(k in (it_container or "").lower() for k in REVIEW_CONTAINERS):
        score -= 60          # a review OF the work is never the work
    am = _author_match(cand_authors, it_authors)
    if am is True:
        score += 35          # decisive on this canon; see module docstring
    elif am is False:
        score -= 70          # same title, different author = a different work
    if it_year is not None:
        # Books are deposited as ebooks years or decades after publication (Lareau 2003 -> a 2019
        # UC Press DOI). Year is near-uninformative for them and is down-weighted accordingly.
        per_year = 1 if (it_type in BOOKISH_TYPES) else 4
        cap = 12 if (it_type in BOOKISH_TYPES) else 40
        score -= min(cap, per_year * abs(it_year - cand_year))
    if it_container:
        score += 5
    return score


def _title_gate(cand_title, it_title, is_book=False, author_state=None):
    """Pass on a strong Jaccard, OR on a genuine short-title/subtitle relation with a floor in force.

    For books the floor drops to TITLE_JACCARD_FLOOR_BOOK, but ONLY when the author check is
    positive. Lowering the floor alone would admit the Zelizer decoys; the author gate is what makes
    the lower floor safe."""
    j = jaccard(cand_title, it_title)
    ov = overlap_coef(cand_title, it_title)
    floor = TITLE_JACCARD_FLOOR
    if is_book and author_state is True:
        floor = TITLE_JACCARD_FLOOR_BOOK
    ok = j >= TITLE_JACCARD_MIN or (title_prefix_match(cand_title, it_title) and j >= floor)
    return ok, round(j, 3), round(ov, 3)


def _openalex_rows(title):
    """Raw OpenAlex rows for a title, cached and retried. Never caches an empty result: caching []
    turns one rate-limited call into a permanent 'this paper does not exist'."""
    key = f"OAROWS::{title}"
    if key in cache:
        return cache[key]
    from urllib.parse import quote
    url = (f"https://api.openalex.org/works?search={quote(title)}&per-page=8&mailto={MAILTO}"
           f"{_oa_auth()}"
           "&select=id,doi,title,publication_year,type,primary_location,authorships")
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
    if results:
        cache[key] = results
        json.dump(cache, open(CACHE, "w"), indent=0)
    return results


def _oa_authors(w):
    return [(a.get("author") or {}).get("display_name") or "" for a in (w.get("authorships") or [])]


def openalex_lookup(title, year, authors, is_book=False):
    """Second opinion. OpenAlex indexes the version of record more reliably for article-shaped work,
    and its `type` field distinguishes article from preprint from book-chapter."""
    key = f"OA4::{title}::{year}::{is_book}::{'|'.join(sorted(_surnames(authors)))}"
    if key in cache:
        return cache[key]
    best, best_s = None, None
    for w in _openalex_rows(title):
        it_auth = _oa_authors(w)
        am = _author_match(authors, it_auth)
        ok, j, ov = _title_gate(title, w.get("title") or "", is_book, am)
        if not ok:
            continue
        if is_book and (w.get("type") not in BOOKISH_TYPES):
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
        container = (((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")
        s = _cand_score(title, year, authors, w.get("title"), w.get("publication_year"),
                        w.get("type"), container, doi, it_auth)
        if doi and (best_s is None or s > best_s):
            best, best_s = {"doi": doi, "matched_title": w.get("title"), "jaccard": j,
                            "overlap": ov, "cr_year": w.get("publication_year"),
                            "container": container, "type": w.get("type"), "score": s,
                            "author_match": am}, s
    cache[key] = best or {"doi": None, "jaccard": 0.0}
    json.dump(cache, open(CACHE, "w"), indent=0)
    return cache[key]


def _crossref_rows(query_title, year_filter=None, bookish=False, tries=3):
    """Retried, because a single empty response is not evidence that Crossref holds nothing."""
    q = re.sub(r"\s+", "+", norm(query_title))
    filt = ""
    if year_filter:
        filt += f"&filter=from-pub-date:{year_filter}-01-01,until-pub-date:{year_filter}-12-31"
    elif bookish:
        # Book-shaped types only. Without this the monograph query returns its own reviews, which
        # is how Hays 1996 and Zelizer 1985 acquire six perfect-scoring wrong answers each.
        filt += "&filter=type:monograph,type:book,type:edited-book,type:reference-book"
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=10&select=DOI,title,author,issued,container-title,type,publisher{filt}")
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


def _cr_authors(it):
    return [f"{a.get('given','')} {a.get('family','')}".strip() for a in (it.get("author") or [])]


def crossref_lookup(title, year, authors, year_filter=None, is_book=False):
    """Rank ALL title-passing candidates by version-of-record score, then take the best."""
    # The key must cover EVERY input to the result. Authors became an input when `_author_match`
    # became a gate, and omitting them meant a corrected author list silently returned the verdict
    # computed from the wrong one — four anchors kept reporting author_match=False after their names
    # were fixed. Version suffix bumps whenever the accept/reject semantics change.
    key = f"VOR-D2D3::{title}::{year}::{year_filter}::{is_book}::{'|'.join(sorted(_surnames(authors)))}"
    if key in cache:
        return cache[key]
    try:
        probes = [(title, _crossref_rows(title, year_filter, bookish=is_book))]
        if is_book and ":" in title:
            short = title.split(":")[0].strip()
            probes.append((short, _crossref_rows(short, year_filter, bookish=True)))
    except Exception as e:
        cache[key] = {"error": str(e)[:120]}
        return cache[key]
    items = [(gt, it, _cr_authors(it)) for gt, rows in probes for it in rows]
    # OpenAlex rows enter the SAME ranked field rather than acting as a fallback consulted only on
    # failure. A second source used only on failure cannot correct a confident wrong answer.
    for w in _openalex_rows(title):
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if not doi:
            continue
        items.append((title, {"DOI": doi, "title": [w.get("title") or ""],
                              "issued": {"date-parts": [[w.get("publication_year")]]},
                              "container-title": [(((w.get("primary_location") or {}).get("source")
                                                    or {}).get("display_name") or "")],
                              "type": w.get("type"), "_src": "openalex"}, _oa_authors(w)))
    scored, fallback = [], None
    for gate_title, it, it_auth in items:
        ct = (it.get("title") or [""])[0]
        yr = None
        try:
            yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        except Exception:
            pass
        am = _author_match(authors, it_auth)
        ok, j, ov = _title_gate(gate_title, ct, is_book, am)
        rec = {"doi": it.get("DOI"), "matched_title": ct, "jaccard": j, "overlap": ov,
               "cr_year": yr, "container": (it.get("container-title") or [""])[0],
               "type": it.get("type"), "author_match": am}
        if fallback is None or j > fallback["jaccard"]:
            fallback = rec
        if is_book and (it.get("type") not in BOOKISH_TYPES):
            continue          # a review of a book, or a chapter, is not the book
        if is_book and re.search(r"-\d{1,3}$", it.get("DOI") or ""):
            continue          # volume DOI with a chapter ordinal appended: a part, not the whole
        if am is False and j < TITLE_JACCARD_MIN:
            continue          # same-ish title, contradicted author: a different work
        if ok and it.get("DOI"):
            rec["score"] = _cand_score(title, year, authors, ct, yr, it.get("type"),
                                       rec["container"], rec["doi"], it_auth)
            scored.append(rec)
    if not scored:
        oa_only = openalex_lookup(title, year, authors, is_book)
        oa_container = (oa_only.get("container") or "").lower()
        oa_is_review = any(k in oa_container for k in REVIEW_CONTAINERS)
        if oa_only.get("doi") and not oa_is_review and (not is_book or oa_only.get("type") in BOOKISH_TYPES):
            oa_only = {**oa_only, "version_source": "openalex_only_crossref_empty"}
            cache[key] = oa_only
            json.dump(cache, open(CACHE, "w"), indent=0)
            return cache[key]
        # NO acceptable candidate. Hand back the best-Jaccard row as a DIAGNOSTIC only, explicitly
        # flagged. D.1.b returns this same row unflagged and its main() treats any dict carrying a
        # DOI as a match — which on this canon silently promotes a book review to a verified anchor:
        # Hays 1996's Contemporary Sociology review is a perfect-title, one-year-off near-miss and
        # was accepted as the monograph on the first run of this script.
        cache[key] = {**(fallback or {"doi": None, "jaccard": 0.0}), "is_fallback": True}
        json.dump(cache, open(CACHE, "w"), indent=0)
        return cache[key]
    scored.sort(key=lambda r: -r["score"])
    best = scored[0]
    best["n_title_passing"] = len(scored)
    if len(scored) > 1:
        best["rejected_versions"] = [{"doi": r["doi"], "type": r["type"], "year": r["cr_year"],
                                      "container": r["container"], "score": r["score"],
                                      "author_match": r.get("author_match")}
                                     for r in scored[1:5]]
    oa = openalex_lookup(title, year, authors, is_book)
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
    n_verified = n_flagged = n_book = n_drift = n_vor_sub = n_auth_rescue = 0
    for c in CANDIDATES:
        rec = {k: c[k] for k in ("title", "authors", "year", "provenance_channel", "provisional_cell")}
        rec["query_cluster_family"] = c["family"]
        # Carried downstream so stage A4's resolver can apply the same book-shape and author rules.
        rec["is_book"] = bool(c.get("is_book"))
        rec["expect_no_doi"] = bool(c.get("expect_no_doi"))
        if c.get("routing_note"):
            rec["routing_note"] = c["routing_note"]
        if c.get("note"):
            rec["source_note"] = c["note"]
        cr = crossref_lookup(c["title"], c["year"], c.get("authors") or [],
                             c.get("year_filter"), is_book=bool(c.get("is_book")))
        yr_ok = cr.get("cr_year") is None or abs(cr["cr_year"] - c["year"]) <= YEAR_TOL
        # Books get the wide year tolerance their ebook deposits require, and only when the author
        # check is positive — the same trade as the title floor.
        if c.get("is_book") and cr.get("author_match") is True:
            yr_ok = True
        j = cr.get("jaccard", 0.0)
        ov = cr.get("overlap", 0.0)
        am = cr.get("author_match")
        title_ok = (j >= TITLE_JACCARD_MIN
                    or (ov >= 0.90 and len(toks(c["title"])) >= 5)
                    or (bool(c.get("is_book")) and am is True and j >= TITLE_JACCARD_FLOOR_BOOK))
        # A flagged fallback is a near-miss report, never a match. See crossref_lookup.
        usable = bool(cr.get("doi")) and not cr.get("is_fallback")
        # BOOK RULE: a book anchor needs a POSITIVE author match, whatever the Jaccard. Title alone
        # cannot do this work here — the short-title probe scores "Pricing the Priceless Child"
        # against Newhouse's unrelated "Pricing the Priceless" at 0.75, above TITLE_JACCARD_MIN, so
        # the ordinary gate would admit a different book by a different author on title alone.
        if c.get("is_book") and am is not True:
            usable = False
        matched = usable and title_ok and yr_ok
        near_exact = j >= 0.90 or (ov >= 0.98 and len(toks(c["title"])) >= 5)
        # The drift path took no author signal at all, which is how Zelizer 1985 acquired an MIT
        # Press book by Newhouse and Aries 1962 acquired a Macat study guide ABOUT the book. A
        # contradicted author is disqualifying on the drift path exactly as on the matched path.
        year_drift = ((not matched) and usable and near_exact and title_ok and not yr_ok
                      and am is not False)
        if matched:
            existence = doi_exists(cr["doi"])
            rec["doi"] = cr["doi"]
            rec["identity_source"] = f"https://doi.org/{cr['doi']}"
            rec["identity_verified"] = existence == "FOUND"
            rec["existence"] = existence
            rec["match_jaccard"] = j
            rec["author_match"] = am
            rec["container"] = cr.get("container")
            rec["record_type"] = cr.get("type")
            for k in ("n_title_passing", "rejected_versions", "version_source", "crossref_pick",
                      "openalex_alternative"):
                if cr.get(k) is not None:
                    rec[k] = cr[k]
            rec["gold_status"] = "candidate_not_ra_frozen"
            # A book that cleared only because the author gate lowered the floor: the new path.
            if c.get("is_book") and am is True and j < TITLE_JACCARD_FLOOR:
                rec["resolution_path"] = "book_short_title_author_gated"
                n_auth_rescue += 1
            if existence == "FOUND":
                n_verified += 1
                if cr.get("version_source") == "openalex_override":
                    n_vor_sub += 1
                status = (f"VERIFIED  doi={cr['doi']}  J={j}  auth={am}  [{cr.get('type')}]  "
                          f"({(cr.get('container') or '')[:34]})"
                          + ("  <- VoR substituted" if cr.get("version_source") else "")
                          + ("  <- author-gated short title" if rec.get("resolution_path") else ""))
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
            rec["author_match"] = am
            rec["container"] = cr.get("container")
            rec["cr_year"] = cr.get("cr_year")
            rec["record_type"] = cr.get("type")
            for k in ("n_title_passing", "rejected_versions", "version_source", "crossref_pick"):
                if cr.get(k) is not None:
                    rec[k] = cr[k]
            rec["gold_status"] = "candidate_year_drift_ra_confirm"
            rec["note"] = (f"Exact-title match (J={j}) with year drift: candidate {c['year']} vs index "
                           f"{cr.get('cr_year')} (preprint/WP-vs-VoR or reissued volume). Kept keyed on title.")
            n_drift += 1
            status = f"YEAR-DRIFT-KEEP  doi={cr['doi']}  J={j}  cand={c['year']} idx={cr.get('cr_year')}"
        else:
            rec["doi"] = None
            rec["identity_verified"] = False
            rec["match_jaccard"] = j
            rec["author_match"] = am
            rec["crossref_best"] = {"doi": cr.get("doi"), "title": cr.get("matched_title"),
                                    "jaccard": j, "year": cr.get("cr_year"),
                                    "author_match": am, "is_fallback": bool(cr.get("is_fallback"))}
            rec["gold_status"] = "unverified_no_doi_match"
            if c.get("is_book") and am is False:
                rec["rejected_reason"] = ("Best near-miss is a different work sharing the title: "
                                          "author surnames do not overlap.")
            if c.get("expect_no_doi"):
                rec["note"] = ("Book or monograph reachable only as reviews of itself; expected index "
                               "miss. Carried keyed on title, not faked.")
                n_book += 1
                status = f"BOOK-NO-DOI (expected)  best-J={j}  auth={am}"
            else:
                n_flagged += 1
                status = f"NO-MATCH  best-J={j}  best='{(cr.get('matched_title') or '')[:42]}'"
        anchors.append(rec)
        log.append(f"- **{c['title'][:66]}** ({c['year']}, {c['family']}) -> {status}")
        json.dump(cache, open(CACHE, "w"), indent=0)
        time.sleep(0.4)

    json.dump(anchors, open(OUT_JSON, "w"), indent=2)
    by_family = {}
    for a in anchors:
        by_family.setdefault(a["query_cluster_family"], []).append(a["identity_verified"])
    empirical = [a for a in anchors if a["provisional_cell"].startswith("PRIMARY_")
                 or a["provisional_cell"] == "COST_INDEPENDENCE"]
    L = [f"# A3 cold-start anchors — {SLUG} (D.2.d)", "",
         f"Sourced in a live OpenAlex + Crossref pass (2026-08-08) and existence-verified: "
         f"{len(anchors)} candidate anchors, of which {len(empirical)} are empirical (the recall "
         f"denominator) and the rest are theory canon, FDT context, or routing decoys. Every DOI "
         f"pulled from a live index match then re-affirmed at doi.org; no DOI hand-asserted. "
         "Three-state gate: network failure = UNCONFIRMED, never ABSENT.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Books unreachable except as reviews (expected): {n_book}**", "",
         f"**Version-of-record substitutions: {n_vor_sub}**  ·  "
         f"**Books resolved only via the author-gated short-title path: {n_auth_rescue}** — "
         "these would have been recorded as absent by the D.1.b resolver.", "",
         f"OpenAlex auth: {'api_key present' if OA_KEY else 'MAILTO ONLY (shared anonymous budget)'}.", "",
         "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- `{fam}`: {sum(1 for v in vs if v)} / {len(vs)}")
    L += ["", "## Per-anchor resolution", ""] + log
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print("\n".join(log))
    print(f"\nverified={n_verified} drift={n_drift} flagged={n_flagged} book_no_doi={n_book} "
          f"vor_sub={n_vor_sub} author_gated_books={n_auth_rescue}")
    print(f"wrote {OUT_JSON}\nwrote {OUT_LOG}")


if __name__ == "__main__":
    main()
