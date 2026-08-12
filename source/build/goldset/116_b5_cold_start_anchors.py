#!/usr/bin/env python3
"""
116_b5_cold_start_anchors.py — B.5 (fetal loss / intrauterine mortality), stage A3.

Mirrors `95_d1b_cold_start_anchors.py` and re-implements the book-canon defences that were developed
on D.2.d (TICK-064) but never committed — that script is gone, so the fixes are rebuilt here from the
recorded findings rather than inherited. Three gates, all mandatory, each catching a failure the
others structurally cannot:

  * EXISTENCE gate (OAS, 2026-07-08). No anchor enters a recall denominator without a live DOI or a
    Crossref/OpenAlex record confirming the title exists. Catches ghosts: titles resolving to nothing.
  * VERSION-OF-RECORD gate (D.1.b, 2026-08-07). Candidates are RANKED for version-of-record status
    rather than taken at the title argmax. Catches the mirror failure: a title resolving to something
    real that is not the record meant — a preprint, working paper, reprint, or chapter.
  * BOOK-CANON gate (D.2.d, 2026-08-08). Catches a third thing neither of the above sees: a real,
    correctly-titled, contemporaneous record of a DIFFERENT work, namely a review OF a monograph.

The book gate is load-bearing on this hypothesis and the live sourcing pass (2026-08-11) proves it
rather than assuming it. Five of this chapter's canonical works are books, and every one returns its
own reviews:

    Wood 1994          -> reviews by Leidy (Med Anthro Q), du Toit (AJHB), Tracer (AJPA)
    Leridon 1977       -> PDR and Population Studies records that credit Leridon AND a reviewer
    Sheps & Menken 1973-> a JASA record crediting Cohen (the reviewer) alongside Sheps and Menken
    Woods 2009         -> reviews by Weaver, Nicholson, and Harris, plus the real OUP monograph DOI
    Preston 1978       -> a Contemporary Sociology record crediting Gendell AND Preston

Note what that list means for the defences: for Wood the author check rejects the reviews (Leidy is
not Wood), but for Leridon, Sheps-Menken, and Preston the review records CREDIT THE BOOK'S OWN
AUTHORS alongside the reviewer, so the author check passes and only the review-shape and fallback
flags reject. Both defences are required and neither is redundant — the same conclusion D.2.d reached
on Hays and Zelizer, reproduced here on a different canon.

Same standing discipline as the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) from a LIVE
    OpenAlex sourcing pass (2026-08-11). They assert NO DOIs; the DOI is whatever the resolver
    returns for a ranked match. Author lists are live-sourced too — author lists asserted from memory
    have been wrong every time they were checked.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached, because caching one turns a rate-limited call into a permanent "does not exist".
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication; it
    draws on a shared anonymous budget that this stage exhausts, and the failure presents as
    unexplained slowness before it presents as an error.

Deliberate version-gate test cases in the candidate set, included because a gate with nothing to
catch is a gate that has not been tested: Hernandez-Julian et al. 2014 has an SSRN preprint twin
(10.2139), Zinaman et al. 1996 has a 2019 "Reprint of:" record, and Wilcox et al. 1988 shares its
exact title with a same-year NEJM correspondence item by different authors.

SCRIPT NUMBERING: 88 is the highest on `main`; D.1.b holds 95-102 on unmerged branch 063; the D.2.d
run consumed 103-114. B.5 therefore starts at 115 (the reconnaissance probe) and this is 116.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, time
from urllib.parse import quote

SLUG = "fetal-loss-intrauterine-mortality"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b5_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

TITLE_JACCARD_MIN = 0.72
TITLE_JACCARD_FLOOR = 0.45      # ordinary floor under the subtitle test
BOOK_TITLE_FLOOR = 0.25         # lowered for book short-title probes; SAFE ONLY because the author
                                # gate and the review-shape test carry the discrimination there
YEAR_TOL = 1


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


OA_KEY = openalex_key()


def _oa_auth(url):
    """Append the funded key. Never let the key into a cache key, a log line, or an exception."""
    return url + (f"&api_key={OA_KEY}" if OA_KEY else f"&mailto={MAILTO}")


# --- Candidate anchors. Live-sourced 2026-08-11. NO DOIs asserted here by design. ---
CANDIDATES = [
    # === PRIMARY_SHOCK_TO_BIRTHS — the identification-bearing cell ===
    dict(title="Famine, social disruption, and involuntary fetal loss: Evidence from chinese survey data",
         authors=["Yong Cai", "Feng Wang"], year=2005, family="shock-famine",
         provisional_cell="PRIMARY_SHOCK_TO_BIRTHS",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 42:301-322. The chapter's single best-identified anchor: the Great Leap "
              "famine as exogenous variation in involuntary fetal loss, with birth consequences. "
              "Note the title's lowercase 'chinese' is OpenAlex's, retained for exact matching."),
    dict(title="The Effects of Intrauterine Malnutrition on Birth and Fertility Outcomes",
         authors=["Rey Hernández-Julián", "Hani Mansour", "Christina Peters"], year=2014,
         family="shock-famine", provisional_cell="PRIMARY_SHOCK_TO_BIRTHS",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Demography 51:1775-1796 (1974-75 Bangladesh famine). VERSION-GATE TEST CASE: an SSRN "
              "preprint twin exists at 10.2139/ssrn.2345609 with an identical title and the same "
              "authors, one year earlier. The resolver must return the Demography record."),
    dict(title="Short-Term Birth Sequelae of the 1918-1920 Influenza Pandemic in the United States",
         authors=["Siddharth Chandra", "Julia Christensen", "Svenn-Erik Mamelund", "Nigel Paneth"],
         year=2018, family="shock-epidemic", provisional_cell="PRIMARY_SHOCK_TO_BIRTHS",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Am J Epidemiol 187:2585-2595. Pandemic exposure -> births, running through fetal loss."),
    dict(title="Excess risk of stillbirth during the 1918-1920 influenza pandemic in Japan",
         authors=["Hiroshi Nishiura"], year=2009, family="shock-epidemic",
         provisional_cell="PRIMARY_SHOCK_TO_BIRTHS",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Eur J Obstet Gynecol Reprod Biol. Stillbirth outcome only; the fertility consequence "
              "is inferred, so this may settle at PARAMETER_DETERMINANT_TO_LOSS at full text."),
    dict(title="Famine, Maternal Nutrition and Infant Mortality: A Re-examination of the Dutch Hunger Winter",
         authors=["Nicky Hart"], year=1993, family="shock-famine",
         provisional_cell="PRIMARY_SHOCK_TO_BIRTHS",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Population Studies 47:27-46. The Dutch Hunger Winter, the best-documented nutritional "
              "shock in the historical record, re-examined on the fetal and infant margins."),

    # === PRIMARY_LOSS_TO_FERTILITY ===
    dict(title="Pregnancy Wastage among Married Women in South Korea",
         authors=["Minja Kim Choe", "Seung-Kwon Kim"], year=2007, family="loss-to-fertility",
         provisional_cell="PRIMARY_LOSS_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Asian Population Studies. One of very few records the recon pass found that puts "
              "pregnancy loss and fertility in the same estimand. Wall 4 is live here: Korean "
              "'pregnancy wastage' data mix induced and spontaneous loss."),
    dict(title="The effects of family planning and other factors on fertility, abortion, miscarriage, and stillbirths",
         authors=["John Stover", "William Winfrey"], year=2017, family="accounting",
         provisional_cell="MECHANICAL_ACCOUNTING",
         provenance_channel="direct_empirical_bibliographic_search",
         note="BMC Public Health. A projection model, so ACCOUNTING_SHARE by construction. Carried "
              "to anchor the accounting stratum, and never poolable with an identified estimate."),

    # === REPLACEMENT_COMPENSATION — the attenuation parameter ===
    dict(title="Inbreeding Effects on Fertility in Humans: Evidence for Reproductive Compensation",
         authors=["Carole Ober", "Terry Hyslop", "Walter W. Hauck"], year=1999,
         family="replacement", provisional_cell="REPLACEMENT_COMPENSATION",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Am J Hum Genet 64:225-231. Hutterite data: fetal loss offset by compensating "
              "conceptions, so completed family size moves far less than the loss rate. This is the "
              "chapter's accounting-identity argument measured in a real natural-fertility population."),
    dict(title="The hypothesis of reproductive compensation and its assumptions about mate preferences and offspring viability",
         authors=["Patricia Adair Gowaty", "Wyatt W. Anderson", "Cynthia K. Bluhm", "Lee C. Drickamer"],
         year=2007, family="replacement", provisional_cell="REPLACEMENT_COMPENSATION",
         provenance_channel="hypothesis_canon",
         note="PNAS 104:15023-15027. The formal statement of reproductive compensation and its "
              "assumptions; theory-side of the attenuation parameter."),

    # === PARAMETER_LOSS_LEVEL — the quantities demographic significance needs ===
    dict(title="Incidence of Early Loss of Pregnancy",
         authors=["Allen J. Wilcox", "Clarice R. Weinberg", "John F. O'Connor", "Donna D. Baird"],
         year=1988, family="loss-level", provisional_cell="PARAMETER_LOSS_LEVEL",
         provenance_channel="direct_empirical_bibliographic_search",
         note="NEJM 319:189-194. The canonical hCG-assay estimate of total post-implantation loss, "
              "and the reason LOSS_WINDOW_WEEKS exists as an extraction field. AUTHOR-GATE TEST "
              "CASE: a same-year NEJM correspondence item carries the identical title under "
              "Hertz-Picciotto and Samuels."),
    dict(title="Maternal age and fetal loss: population based register linkage study",
         authors=["Anne-Marie Nybo Andersen"], year=2000, family="loss-level",
         provisional_cell="PARAMETER_LOSS_LEVEL",
         provenance_channel="direct_empirical_bibliographic_search",
         note="BMJ 320:1708-1712. The canonical age gradient; also the Wall 5 confound in its "
              "sharpest form."),
    dict(title="Conception to ongoing pregnancy: the 'black box' of early pregnancy loss",
         authors=["N.S. Macklon"], year=2002, family="loss-level",
         provisional_cell="PARAMETER_LOSS_LEVEL", provenance_channel="direct_empirical_bibliographic_search",
         note="Hum Reprod Update 8:333-343. The conception-to-birth attrition schedule."),
    dict(title="Estimates of human fertility and pregnancy loss",
         authors=["Michael J. Zinaman", "E. D. Clegg", "Charles Brown", "John F. O'Connor"],
         year=1996, family="loss-level", provisional_cell="PARAMETER_LOSS_LEVEL",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Fertil Steril 65:503-509. VERSION-GATE TEST CASE: a 2019 'Reprint of:' record exists "
              "in the same journal at 10.1016/j.fertnstert.2019.08.096."),
    dict(title="Miscarriage matters: the epidemiological, physical, psychological, and economic costs of early pregnancy loss",
         authors=["Siobhan Quenby", "Ioannis Gallos", "Rima Dhillon-Smith", "Marcelina Podesek"],
         year=2021, family="loss-level", provisional_cell="PARAMETER_LOSS_LEVEL",
         provenance_channel="channel1_review_seed",
         note="Lancet 397:1658-1667. Lancet miscarriage-series overview; the privileged channel-1 "
              "seed for loss PREVALENCE. LEAKAGE WALL applies: its search strategy must not be mined "
              "for A6 query terms."),
    dict(title="National, regional, and worldwide estimates of stillbirth rates in 2015, with trends from 2000",
         authors=["Hannah Blencowe", "Simon Cousens", "Fiorella Bianchi-Jassir", "Lale Say"],
         year=2016, family="loss-level", provisional_cell="PARAMETER_LOSS_LEVEL",
         provenance_channel="channel1_review_seed",
         note="Lancet Global Health 4:e98-e108. The stillbirth-rate series and the definitional "
              "threshold problem (28 weeks for comparability) that LOSS_WINDOW_WEEKS records."),

    # === PARAMETER_DETERMINANT_TO_LOSS ===
    dict(title="The role of infection in miscarriage",
         authors=["Sevi Giakoumelou", "Nick Wheelhouse", "Kate Cuschieri", "Gary Entrican"],
         year=2015, family="determinant-infection",
         provisional_cell="PARAMETER_DETERMINANT_TO_LOSS", provenance_channel="channel1_review_seed",
         note="Hum Reprod Update 22:116-133. The infection -> loss channel, which is Wall 2's "
              "B.5-side content: infection acting on survival rather than on conception."),
    dict(title="Stillbirths: rates, risk factors, and acceleration towards 2030",
         authors=["Joy E Lawn", "Hannah Blencowe", "Peter Waiswa", "Agbessi Amouzou"], year=2016,
         family="determinant-infection", provisional_cell="PARAMETER_DETERMINANT_TO_LOSS",
         provenance_channel="channel1_review_seed",
         note="Lancet 387:587-603. Risk-factor decomposition for stillbirth, including syphilis and "
              "malaria — B.5's historical drivers measured in a contemporary setting."),

    # === MEASUREMENT_METHOD — the risk-of-bias spine ===
    dict(title="Collecting Data on Pregnancy Loss: A Review of Evidence from the World Fertility Survey",
         authors=["John B. Casterline"], year=1989, family="measurement",
         provisional_cell="MEASUREMENT_METHOD", provenance_channel="hypothesis_canon",
         note="Studies in Family Planning 20:81-95. HYPOTHESES-v5 seminal entry, and the chapter's "
              "methodological anchor: survey pregnancy-loss data are under-reported non-randomly, "
              "which is the first-order threat to every PM and FDT estimate in this chapter."),

    # === THEORY_PROXIMATE_DETERMINANTS — four of five are books ===
    dict(title="A Framework for Analyzing the Proximate Determinants of Fertility",
         authors=["John Bongaarts"], year=1978, family="theory-proximate",
         provisional_cell="THEORY_PROXIMATE_DETERMINANTS", provenance_channel="hypothesis_canon",
         note="Population and Development Review 4:105-132. The accounting frame in which fetal loss "
              "is a component of the birth interval rather than a multiplier on births."),
    dict(title="Fertility, Biology, and Behavior: An Analysis of the Proximate Determinants",
         authors=["John Bongaarts", "Robert G. Potter"], year=1983, family="theory-proximate",
         provisional_cell="THEORY_PROXIMATE_DETERMINANTS", provenance_channel="hypothesis_canon",
         is_book=True, expect_no_doi=True,
         note="Academic Press monograph; HYPOTHESES-v5 seminal entry. BOOK-CANON CASE: several "
              "same-title records exist in PDR, Studies in Family Planning, and Social Forces, at "
              "least one of which is a review crediting the book's own authors."),
    dict(title="Dynamics of Human Reproduction: Biology, Biometry, Demography",
         authors=["James W. Wood"], year=1994, family="theory-proximate",
         provisional_cell="THEORY_PROXIMATE_DETERMINANTS", provenance_channel="hypothesis_canon",
         is_book=True, expect_no_doi=True,
         note="Aldine de Gruyter; HYPOTHESES-v5 seminal entry. BOOK-CANON CASE: returns reviews by "
              "Leidy, du Toit, and Tracer. Here the author gate does the work, since no reviewer "
              "shares Wood's surname."),
    dict(title="Human Fertility: The Basic Components",
         authors=["Henri Leridon"], year=1977, family="theory-proximate",
         provisional_cell="THEORY_PROXIMATE_DETERMINANTS", provenance_channel="hypothesis_canon",
         is_book=True, expect_no_doi=True,
         note="University of Chicago Press. BOOK-CANON CASE OF THE HARDER KIND: the PDR and "
              "Population Studies records credit Leridon and his translator Helzner alongside a "
              "reviewer, so the author gate PASSES on the reviews and only the review-shape and "
              "fallback flags reject them."),
    dict(title="Mathematical Models of Conception and Birth",
         authors=["Mindel C. Sheps", "Jane Menken"], year=1973, family="theory-proximate",
         provisional_cell="THEORY_PROXIMATE_DETERMINANTS", provenance_channel="hypothesis_canon",
         is_book=True, expect_no_doi=True,
         note="University of Chicago Press. The birth-interval model fetal loss enters as an added "
              "component. BOOK-CANON CASE: the JASA record credits Cohen (the reviewer) alongside "
              "Sheps and Menken."),
    dict(title="Death before Birth: Fetal Health and Mortality in Historical Perspective",
         authors=["Robert Woods"], year=2009, family="historical",
         provisional_cell="PARAMETER_LOSS_LEVEL", provenance_channel="hypothesis_canon",
         is_book=True,
         note="Oxford University Press. The chapter's central FDT-era source: fetal mortality "
              "measured in the historical record. Unlike the other books this one HAS a live "
              "monograph DOI (an OUP acprof id), so it tests that the book gate accepts a real "
              "monograph rather than merely rejecting reviews — it returns three reviews too "
              "(Weaver, Nicholson, Harris)."),
    dict(title="Fertility and Pregnancy: An Epidemiologic Perspective",
         authors=["Allen J. Wilcox"], year=2010, family="theory-proximate",
         provisional_cell="MEASUREMENT_METHOD", provenance_channel="hypothesis_canon",
         is_book=True, expect_no_doi=True,
         note="Oxford University Press. The measurement-theoretic treatment of pregnancy loss "
              "observation windows. BOOK-CANON CASE: its AJE review is titled '... By Allen J "
              "Wilcox', which is the by-line review shape the title test screens for."),

    # === ROUTING DECOYS — must route away; not part of the recall denominator ===
    dict(title="Infertility in sub-Saharan Africa: Estimates and Implications",
         authors=["Odile Frank"], year=1983, family="ROUTING_DECOY",
         provisional_cell="OFF_STERILITY_B3", provenance_channel="routing_decoy_B3",
         routing_note="Wall 2. Infection acting on the CONCEPTION margin (sterility, the infertility "
                      "belt) is B.3's estimand even though its causes and its populations are B.5's."),
    dict(title="Age and Infertility",
         authors=["Jane Menken", "James Trussell", "Ulla Larsen"], year=1986, family="ROUTING_DECOY",
         provisional_cell="OFF_MATERNAL_AGE_A15", provenance_channel="routing_decoy_A15",
         routing_note="Wall 5. Maternal age as the identifying variation routes to A.15, whose claim "
                      "text already owns rising miscarriage risk."),
    dict(title="Abortion Legalization in Uruguay: Effects on Adolescent Fertility",
         authors=["Wanda Cabella", "Cecilia Velázquez"], year=2022, family="ROUTING_DECOY",
         provisional_cell="OFF_INDUCED_ABORTION_A4", provenance_channel="routing_decoy_A4",
         routing_note="Wall 4. Deliberate termination is A.4. Included because the screen must not "
                      "route on the word 'abortion', which B.5's own vocabulary contains."),
    dict(title="The Effects of Infant and Child Mortality on Fertility",
         authors=["Samuel H. Preston"], year=1978, family="ROUTING_DECOY",
         provisional_cell="OFF_CHILD_MORTALITY_A1", provenance_channel="routing_decoy_A1",
         is_book=True, expect_no_doi=True,
         routing_note="Wall 1. Post-natal mortality and the behavioural replacement response are "
                      "A.1's. BOOK-CANON CASE TOO: the Contemporary Sociology record credits Gendell "
                      "AND Preston, so the author gate passes on the review."),
    dict(title="Embryonic Mortality in Farm Animals",
         authors=["J.M. Sreenan", "M. G. Diskin"], year=1986, family="ROUTING_DECOY",
         provisional_cell="OFF_ANIMAL", provenance_channel="routing_decoy_species", is_book=True,
         routing_note="Wall 7. The veterinary reproductive-wastage literature shares B.5's vocabulary "
                      "almost exactly and is large. Cheap to exclude, expensive to discover late."),
    dict(title="ESHRE guideline: recurrent pregnancy loss",
         authors=["Ruth Bender-Atik", "Ole Bjarne Christiansen", "J. Elson"], year=2018,
         family="ROUTING_DECOY", provisional_cell="OFF_CLINICAL_MANAGEMENT",
         provenance_channel="routing_decoy_clinical",
         routing_note="Clinical management of recurrent pregnancy loss: the single densest region of "
                      "the adjacent literature, and the cell expected to dominate the corpus."),
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
    """Szymkiewicz-Simpson, reported as a diagnostic only and NEVER used as a match gate. On D.1.b it
    fired backwards: a four-token generic title scores 1.0 inside any long demography title."""
    A, B = toks(a), toks(b)
    m = min(len(A), len(B))
    return len(A & B) / m if m else 0.0


def title_prefix_match(a, b, min_tokens=3):
    """The subtitle case tested properly: is the shorter title a contiguous LEADING token sequence of
    the longer one? Direction-agnostic, since indexes vary on whether they keep the subtitle."""
    A, B = norm(a).split(), norm(b).split()
    if len(A) > len(B):
        A, B = B, A
    if len(A) < min_tokens:
        return False
    return B[:len(A)] == A


# --------------------------------------------------------------------------------------------
# BOOK-CANON DEFENCES (rebuilt from the D.2.d findings; 103_d2d was never committed).
# --------------------------------------------------------------------------------------------
REVIEW_CONTAINERS = ("choice reviews", "book review", "reviews online", "journal of reviews",
                     "book reviews", "contemporary sociology")
# Title shapes that a review wears and the work itself does not.
REVIEW_TITLE_PATTERNS = (
    r"\(review\)\s*$",                 # "... : ... (review)"
    r"^book review\b",                 # "Book review: ..."
    r"\breviewed by\b",
    r"[-–—]\s*by\s+\w",                # "... – By Robert Woods"
    r"\.\s*by\s+\w",                   # "... . By Allen J Wilcox"
)


def surnames(names):
    """Last whitespace-separated token, folded. Robust to initials, accents stripped by norm(), and
    to index-level first-name corruption — OpenAlex records Preston 1978 as 'Scott Preston'."""
    out = set()
    for n in names or []:
        parts = norm(n).split()
        if parts:
            out.add(parts[-1])
    return out


def author_match(cand_authors, rec_authors):
    """THREE-STATE. True = at least one candidate surname appears among the record's authors.
    False = the record has authors and none matches. None = the record carries no author metadata,
    which is missing information rather than contradicting information and must not reject on its own.

    Collapsing None into False would drop legitimately author-less index records; collapsing it into
    True would restore the failure this gate exists to prevent."""
    if not rec_authors:
        return None
    c, r = surnames(cand_authors), surnames(rec_authors)
    if not c:
        return None
    return bool(c & r)


def looks_like_review(rec_title, container, cand_authors):
    """Is this record a review OF the work rather than the work? Three independent signals, because a
    review that credits the book's own authors defeats the author gate — which is exactly what
    Leridon 1977, Sheps & Menken 1973, and Preston 1978 do in the live index."""
    t = (rec_title or "")
    if any(re.search(p, t, flags=re.I) for p in REVIEW_TITLE_PATTERNS):
        return True
    if any(k in (container or "").lower() for k in REVIEW_CONTAINERS):
        return True
    # "Robert Woods, Death Before Birth: ..." — a review titled with the reviewed author's name first.
    lead = norm(t).split(",")[0] if "," in t else ""
    if lead and surnames(cand_authors) & set(lead.split()):
        return True
    return False


TYPE_RANK = {"journal-article": 100, "monograph": 92, "book": 90, "edited-book": 88,
             "reference-entry": 55, "book-chapter": 50, "book-part": 45, "proceedings-article": 40,
             "report": 30, "posted-content": 20, "dissertation": 20, "book-review": 5, "other": 10}

# Crossref and OpenAlex use DIFFERENT type vocabularies for the same thing, and the scorer reads both
# out of one ranked field. Crossref says "journal-article"; OpenAlex says "article". The first two
# runs of this script left them unmapped, so every OpenAlex record fell to the "other" default of 10
# while its Crossref rival scored 100 — a 90-point gap that no other signal can overcome. The visible
# symptom was Wilcox et al. 1988 and Menken et al. 1986 each resolving to a same-title impostor: the
# correct record was present, ranked first by OpenAlex, and lost on vocabulary rather than on merit.
# Normalize before scoring, never at the call site, so a third source can be added without repeating
# the mistake.
TYPE_ALIASES = {"article": "journal-article", "review": "journal-article", "preprint": "posted-content",
                "paratext": "other", "dataset": "other", "libguides": "other", "editorial": "other",
                "letter": "other", "erratum": "other", "reference-book": "edited-book"}


def canon_type(t):
    t = (t or "other").lower()
    return TYPE_ALIASES.get(t, t)
NON_VOR_PREFIXES = {
    "10.3386": "NBER working paper", "10.2139": "SSRN", "10.21203": "Research Square",
    "10.31235": "SocArXiv", "10.31219": "OSF preprints", "10.1596": "World Bank working paper",
    "10.18235": "IDB working paper", "10.22004": "AgEcon Search", "10.5860": "Choice Reviews",
    "10.31899": "Population Council report", "10.48550": "arXiv",
}
BOOKISH_TYPES = {"book", "monograph", "edited-book", "reference-book", "book-set", "other"}


def _cand_score(cand_title, cand_year, it_title, it_year, it_type, it_container, it_doi,
                auth_state, is_review):
    """Score a candidate for being the VERSION OF RECORD of the anchor. Title fit is a gate rather
    than a score component: among records sharing one title the discriminating information is type,
    venue, year, authorship, and review-shape."""
    score = TYPE_RANK.get(canon_type(it_type), 10)
    prefix = (it_doi or "").split("/")[0]
    if prefix in NON_VOR_PREFIXES:
        score -= 45
    if is_review:
        score -= 80          # a review OF the work is never the work
    if auth_state is False:
        score -= 70          # record has authors and none is ours
    elif auth_state is True:
        score += 15
    else:
        # auth_state is None: the record carries no author metadata. Missing information does not
        # REJECT (that would collapse three states into two), but it must not rank equal to a
        # confirmed authorship match either. The first run of this script scored None as neutral and
        # two anchors resolved to the wrong same-title record for exactly that reason: Wilcox et al.
        # 1988 went to the December NEJM correspondence item rather than the July article, and Menken
        # et al. 1986 went to a Science comment rather than the article. In both the correct record
        # carried authors and the impostor did not, so a penalty here is sufficient and a rejection
        # is not required.
        score -= 25
    if it_year is not None:
        score -= min(40, 4 * abs(it_year - cand_year))
    if "reprint of" in (it_title or "").lower():
        score -= 50
    if it_container:
        score += 5
    return score


def _title_gate(cand_title, it_title, is_book=False):
    j = jaccard(cand_title, it_title)
    ov = overlap_coef(cand_title, it_title)
    floor = BOOK_TITLE_FLOOR if is_book else TITLE_JACCARD_FLOOR
    ok = j >= TITLE_JACCARD_MIN or (title_prefix_match(cand_title, it_title) and j >= floor)
    return ok, round(j, 3), round(ov, 3)


def _openalex_rows(title):
    key = f"OAROWS::{title}"
    if key in cache:
        return cache[key]
    url = _oa_auth(f"https://api.openalex.org/works?search={quote(title)}&per-page=8"
                   "&select=id,doi,title,publication_year,type,authorships,primary_location")
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
    # An empty result is NEVER cached: caching it turns one rate-limited call into a permanent
    # "this work does not exist", which breaks UNCONFIRMED != ABSENT at the cache layer.
    if results:
        cache[key] = results
        json.dump(cache, open(CACHE, "w"), indent=0)
    return results


def _crossref_rows(query_title, year_filter=None, tries=3):
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


def _cr_authors(it):
    return [" ".join(filter(None, [a.get("given"), a.get("family")])) for a in (it.get("author") or [])]


def resolve(cand):
    """Rank every title-passing candidate from Crossref AND OpenAlex in ONE field, then take the best.

    Returns a record carrying `is_fallback`. A fallback is a near-miss diagnostic, NOT a match, and
    main() must never promote one — reading the fallback as a match is one of the three defects that
    let a monograph anchor to its own review on D.2.d."""
    title, year = cand["title"], cand["year"]
    is_book = bool(cand.get("is_book"))
    # EVERY input to the verdict goes in the cache key, authors included. On D.2.d authors were left
    # out, so corrected author lists returned verdicts computed from the stale ones.
    # Cache key version bumped when the scoring rule changes; v2 = the auth-None penalty and the
    # ISBN-safe chapter-ordinal test; v3 = the Crossref/OpenAlex type-vocabulary normalization. A stale cache would otherwise serve verdicts computed under the
    # old rule, which is the same class of error as omitting authors from the key.
    key = f"B5VOR3::{title}::{year}::{is_book}::{'|'.join(cand.get('authors') or [])}"
    if key in cache:
        return cache[key]

    probes = [(title, _crossref_rows(title, cand.get("year_filter")))]
    if is_book and ":" in title:
        probes.append((title.split(":")[0].strip(), _crossref_rows(title.split(":")[0].strip(),
                                                                   cand.get("year_filter"))))
    items = []
    for gate_title, rows in probes:
        for it in rows:
            items.append((gate_title, {
                "doi": it.get("DOI"), "title": (it.get("title") or [""])[0],
                "year": (it.get("issued", {}).get("date-parts", [[None]]) or [[None]])[0][0],
                "container": (it.get("container-title") or [""])[0], "type": it.get("type"),
                "authors": _cr_authors(it), "src": "crossref"}))
    for w in _openalex_rows(title):
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        items.append((title, {
            "doi": doi or None, "title": w.get("title") or "", "year": w.get("publication_year"),
            "container": (((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""),
            "type": w.get("type"),
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])],
            "src": "openalex"}))

    scored, fallback, drops = [], None, []
    for gate_title, it in items:
        ok, j, ov = _title_gate(gate_title, it["title"], is_book)
        auth_state = author_match(cand.get("authors"), it["authors"])
        is_review = looks_like_review(it["title"], it["container"], cand.get("authors"))
        rec = {"doi": it["doi"], "matched_title": it["title"], "jaccard": j, "overlap": ov,
               "cr_year": it["year"], "container": it["container"], "type": it["type"],
               "src": it["src"], "author_match": auth_state, "review_shape": is_review}
        if fallback is None or j > fallback["jaccard"]:
            fallback = {**rec, "is_fallback": True}
        if not ok or not it["doi"]:
            drops.append(("title_or_no_doi", it["title"][:60], it["doi"]))
            continue
        if is_review:
            drops.append(("review_of_the_work", it["title"][:60], it["doi"]))
            continue                                   # never the work
        if auth_state is False:
            drops.append(("authors_disagree", it["title"][:60], it["doi"]))
            continue                                   # has authors, none is ours
        if is_book and (canon_type(it["type"]) not in BOOKISH_TYPES):
            drops.append((f"not_book_shaped:{it['type']}", it["title"][:60], it["doi"]))
            continue                                   # a chapter or an article is not the book
        # Volume DOI with a chapter ordinal appended is a part, not the whole. The test EXCLUDES
        # ISBN-derived book DOIs (10.1007/978-...), whose trailing "-2" is an ISBN check digit rather
        # than a chapter number. The first run refused Sreenan & Diskin 1986 at Jaccard 1.0 on that
        # false positive — the fourth unanchored-pattern bug in this codebase, after `hous`,
        # `reproduc\w+`, and the bare "429" substring.
        if is_book and re.search(r"-\d{1,3}$", it["doi"] or "") and "/978" not in (it["doi"] or ""):
            continue
        rec["score"] = _cand_score(title, year, it["title"], it["year"], it["type"],
                                   it["container"], it["doi"], auth_state, is_review)
        rec["is_fallback"] = False
        scored.append(rec)

    if not scored:
        out = fallback or {"doi": None, "jaccard": 0.0, "is_fallback": True}
        out["is_fallback"] = True
        # Why nothing survived, so the RA auditing a book miss can see what was refused instead of
        # inferring it from the fallback's own flags, which describe a different record.
        out["refused_reasons"] = sorted({d[0] for d in drops})
        out["refused_candidates"] = [{"reason": r, "title": t, "doi": d} for r, t, d in drops[:6]]
        cache[key] = out
        json.dump(cache, open(CACHE, "w"), indent=0)
        return out
    scored.sort(key=lambda r: -r["score"])
    best = scored[0]
    best["n_title_passing"] = len(scored)
    if len(scored) > 1:
        best["rejected_versions"] = [{"doi": r["doi"], "type": r["type"], "year": r["cr_year"],
                                      "container": r["container"], "score": r["score"],
                                      "src": r["src"]} for r in scored[1:5]]
    cache[key] = best
    json.dump(cache, open(CACHE, "w"), indent=0)
    return best


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
    if state != "UNCONFIRMED":          # never cache a transport failure as an answer
        cache[dkey] = state
    return state


def main():
    anchors, log = [], []
    n_verified = n_flagged = n_book = n_drift = n_review_rejected = 0
    for c in CANDIDATES:
        rec = {k: c[k] for k in ("title", "authors", "year", "provenance_channel", "provisional_cell")}
        rec["query_cluster_family"] = c["family"]
        # Carried downstream so A4's resolver applies the same book rule rather than re-running the
        # version error with its own argmax title search.
        rec["is_book"] = bool(c.get("is_book"))
        rec["expect_no_doi"] = bool(c.get("expect_no_doi"))
        for k in ("routing_note", "note"):
            if c.get(k):
                rec["source_note" if k == "note" else k] = c[k]

        r = resolve(c)
        j = r.get("jaccard", 0.0)
        yr_ok = r.get("cr_year") is None or abs(r["cr_year"] - c["year"]) <= YEAR_TOL
        title_ok = j >= TITLE_JACCARD_MIN or title_prefix_match(c["title"], r.get("matched_title") or "")
        # A fallback is a diagnostic, never a match. This is the check whose absence let D.2.d anchor
        # Hays 1996 to a book review at perfect confidence.
        usable = bool(r.get("doi")) and not r.get("is_fallback")
        matched = usable and title_ok and yr_ok
        near_exact = j >= 0.90
        year_drift = usable and (not matched) and near_exact and title_ok and not yr_ok

        if matched or year_drift:
            existence = doi_exists(r["doi"])
            rec.update(doi=r["doi"], identity_source=f"https://doi.org/{r['doi']}",
                       identity_verified=existence == "FOUND", existence=existence,
                       match_jaccard=j, container=r.get("container"), record_type=r.get("type"),
                       resolved_via=r.get("src"), author_match=r.get("author_match"))
            for k in ("n_title_passing", "rejected_versions"):
                if r.get(k) is not None:
                    rec[k] = r[k]
            if matched:
                rec["gold_status"] = "candidate_not_ra_frozen"
                if existence == "FOUND":
                    n_verified += 1
                    status = (f"VERIFIED  doi={r['doi']}  J={j}  [{r.get('type')}]  "
                              f"auth={r.get('author_match')}  ({(r.get('container') or '')[:34]})")
                else:
                    n_flagged += 1
                    status = f"DOI-MATCH-BUT-{existence}  doi={r['doi']}  J={j}"
            else:
                rec["gold_status"] = "candidate_year_drift_ra_confirm"
                rec["cr_year"] = r.get("cr_year")
                rec["note"] = (f"Exact-title match (J={j}) with year drift: candidate {c['year']} vs "
                               f"index {r.get('cr_year')}. Kept keyed on title, per the C3 rule.")
                n_drift += 1
                status = f"YEAR-DRIFT-KEEP  doi={r['doi']}  J={j}  cand={c['year']} idx={r.get('cr_year')}"
        else:
            rec.update(doi=None, identity_verified=False, match_jaccard=j,
                       best_near_miss={"doi": r.get("doi"), "title": r.get("matched_title"),
                                       "jaccard": j, "year": r.get("cr_year"),
                                       "container": r.get("container"), "type": r.get("type"),
                                       "author_match": r.get("author_match"),
                                       "review_shape": r.get("review_shape"),
                                       "is_fallback": r.get("is_fallback")},
                       refused_reasons=r.get("refused_reasons"),
                       refused_candidates=r.get("refused_candidates"),
                       gold_status="unverified_no_doi_match")
            reasons = r.get("refused_reasons") or []
            if ("review_of_the_work" in reasons or "authors_disagree" in reasons
                    or r.get("review_shape") or r.get("author_match") is False):
                n_review_rejected += 1
            if c.get("expect_no_doi"):
                rec["note"] = ("Book or monograph; expected index miss. Carried keyed on title, not "
                               "faked. The near-miss record is retained so an RA can see what the "
                               "resolver refused and why.")
                n_book += 1
                status = (f"BOOK-NO-DOI (expected)  best-J={j}  "
                          f"refused={','.join(r.get('refused_reasons') or ['none_reached_gate'])}")
            else:
                n_flagged += 1
                status = f"NO-MATCH  best-J={j}  best='{(r.get('matched_title') or '')[:42]}'"

        anchors.append(rec)
        log.append(f"- **{c['title'][:68]}** ({c['year']}, {c['family']}) -> {status}")
        time.sleep(0.35)

    json.dump(anchors, open(OUT_JSON, "w"), indent=2)
    by_family, by_cell = {}, {}
    for a in anchors:
        by_family.setdefault(a["query_cluster_family"], []).append(a["identity_verified"])
        by_cell.setdefault(a["provisional_cell"], []).append(a["identity_verified"])
    empirical = [a for a in anchors if a["provisional_cell"].startswith("PRIMARY_")
                 or a["provisional_cell"] == "REPLACEMENT_COMPENSATION"]

    L = [f"# A3 cold-start anchors — {SLUG} (B.5)", "",
         f"Sourced in a live OpenAlex pass (2026-08-11) and resolved through three gates: "
         f"{len(anchors)} candidate anchors, of which {len(empirical)} are empirical primary-cell or "
         "replacement anchors (the causal recall denominator) and the rest are parameter, "
         "measurement, theory, or routing-decoy anchors that earn no empirical recall credit. No DOI "
         "is hand-asserted; each is the top-ranked version-of-record candidate from a unified "
         "Crossref + OpenAlex field, then re-affirmed at doi.org.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Books / expected index miss: {n_book}**", "",
         f"**Records refused as a review of the work, or on authorship: {n_review_rejected}** — the "
         "book-canon gate firing. Each refusal keeps its near-miss record in the JSON so the RA can "
         "audit what was refused rather than trusting that nothing was lost.", "",
         "## Coverage by estimand cell (verified / total)", ""]
    for cell, vs in sorted(by_cell.items()):
        L.append(f"- `{cell}`: {sum(vs)}/{len(vs)}")
    L += ["", "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- {fam}: {sum(vs)}/{len(vs)}")
    L += ["", "## Per-candidate disposition", ""] + log
    L += ["", "## Notes", "",
          "- **Three gates, three distinct failures.** The existence gate catches ghosts (titles "
          "resolving to nothing, the OAS finding). The version gate catches the mirror failure (a "
          "title resolving to a preprint or reprint of the right work, the D.1.b finding). The "
          "book-canon gate catches a third thing: a real, correctly-titled, contemporaneous record of "
          "a DIFFERENT work — a review of the monograph. None of the three substitutes for another.",
          "- **This canon is book-shaped and the reviews credit the books' own authors.** Wood 1994 "
          "is rejected from its reviews by the author gate alone (no reviewer shares his surname), "
          "but Leridon 1977, Sheps & Menken 1973, and Preston 1978 all return review records that "
          "credit the book's authors alongside the reviewer, so for those three only the review-shape "
          "and fallback flags reject. Both defences are load-bearing and neither is redundant, which "
          "is the D.2.d conclusion reproduced on an unrelated canon.",
          "- **Version-gate test cases are in the set deliberately**: Hernandez-Julian et al. 2014 has "
          "an SSRN twin, Zinaman et al. 1996 has a 2019 'Reprint of:' record, and Wilcox et al. 1988 "
          "shares its exact title with a same-year NEJM correspondence item under different authors. "
          "A gate with nothing to catch has not been tested.",
          "- **The decoys carry the walls, not the topic.** Frank 1983 (B.3 conception margin), Menken "
          "et al. 1986 (A.15 maternal age), Cabella & Velazquez 2022 (A.4 induced abortion), Preston "
          "1978 (A.1 post-natal mortality), Sreenan & Diskin 1986 (Wall 7, non-human), and the ESHRE "
          "guideline (clinical management) each sit just across one wall. Per the D.2.d finding, "
          "these are forward-cited like any other seed at A4: a decoy's citation neighbourhood is "
          "where the boundary cases live.",
          "- **LEAKAGE WALL.** Quenby et al. 2021, Blencowe et al. 2016, Lawn et al. 2016, and "
          "Giakoumelou et al. 2015 enter as channel-1 review seeds. Their search strategies must NOT "
          "be mined for A6 query terms, since their included studies feed anchors here.",
          "- **Three defects were found and fixed by auditing this script's own output**, which is why "
          "the run is recorded rather than merely reported. (1) The scorer mixed two type "
          "vocabularies: Crossref says `journal-article`, OpenAlex says `article`, and the unmapped "
          "OpenAlex value fell to the `other` default, so every OpenAlex record lost 90 points to its "
          "Crossref rival regardless of merit. Wilcox et al. 1988 resolved to the December NEJM "
          "correspondence item and Menken et al. 1986 to a Science erratum; both correct records were "
          "present and ranked first by OpenAlex. (2) A missing author list scored neutral, so nothing "
          "discriminated among same-title records when the impostor happened to lack author metadata; "
          "`None` now carries a ranking penalty without becoming a rejection, which would collapse the "
          "three states into two. (3) The chapter-ordinal test `-\\d{1,3}$` matched the ISBN check "
          "digit in `10.1007/978-94-009-5038-2` and refused a correctly-resolved book at Jaccard 1.0 — "
          "the fourth unanchored-pattern bug in this codebase. All three were invisible in the "
          "verified set and visible only in the refused set, which is the standing reason to read "
          "both.",
          "- **Empirical recall denominator.** Only the PRIMARY_* and REPLACEMENT_COMPENSATION anchors "
          "count. The parameter, measurement, and theory anchors are indispensable to the chapter's "
          "demographic-significance computation and are not evidence for the causal claim; scoring "
          "recall against them would measure the wrong thing (scope doc, Call 4)."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} year_drift={n_drift} flagged={n_flagged} books={n_book} "
          f"review_or_author_refusals={n_review_rejected} total={len(anchors)}")
    print("by cell:", {k: f"{sum(v)}/{len(v)}" for k, v in by_cell.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
