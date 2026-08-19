#!/usr/bin/env python3
"""
148_d3c_cold_start_anchors.py — D.3.c (despair and hopelessness), stage A3.

Inherits `134_b6_cold_start_anchors.py` — resolver, ranking and all five gates — and extends the
book-canon gate, which this chapter's canon breaks in a way no previous chapter did.

Five inherited gates, each catching a failure the others structurally cannot:

  * EXISTENCE gate (OAS, 2026-07-08). No anchor enters a recall denominator without a live DOI or a
    record confirming the title exists. Catches ghosts.
  * VERSION-OF-RECORD gate (D.1.b, 2026-08-07). Candidates are RANKED for version-of-record status
    rather than taken at the title argmax. LIVE HERE on three anchors: Autor-Dorn-Hanson 2019
    (article 480 / preprint 201 / report 52), Kearney-Levine-Pardue 2022 (139 / 11 / 2), and Ruhm
    2018, which exists only as an NBER report and a RePEc preprint with no journal version.
  * BOOK-CANON gate (D.2.d, 2026-08-08; EXTENDED HERE — see below). Catches a real, correctly-titled,
    contemporaneous record of a DIFFERENT work: a review OF a monograph.
  * SHADOW-RECORD gate (B.7, 2026-08-12). Catches a separately-DOI'd record whose title is the target
    plus a leading named qualifier.
  * DUPLICATE-RECORD gate (B.6, 2026-08-14, carried as UNVALIDATED). **It is validated here.** See
    below — this run is its first confirmed catch.

**The book-canon gate needed a fourth signal, and the case that forced it is the strongest yet.**

Author-list MEMBERSHIP was the defence. It is not enough. William Julius Wilson's 1996 monograph
*When Work Disappears: The World of the New Urban Poor* has, as its citation argmax:

    10.2307/3042249 — "When Work Disappears: The World of the New Urban Poor."
    African American Review, 1998, type=article, 3,641 cites
    authorships = [Daryl Michael Scott (first), William Julius Wilson (last)]

That is Scott's review of Wilson's book. It defeats signal 1 (title is the book's title exactly),
signal 2 ("African American Review" is an ordinary journal whose name merely contains the word
Review, and matches none of the review-container substrings), and signal 3 (the lead-name test needs
a comma; this title has a colon). It then defeats `author_match`, which returns **True** because
Wilson is among the authors — so the record is not merely missed by the gate, it is *endorsed* by it
and scored higher for it. At 3,641 cites it beats every other record for this title by a factor of
three, and no `book`-typed record surfaces in the head at all.

The inherited `is_book and canon_type not in BOOKISH_TYPES` rule does refuse it — but as
`not_book_shaped:article`, a right answer for a reason that does not generalise, and it survives as
the *fallback* record carrying `auth=True`, which tells an RA auditing the miss that the authors
agree. Signal 4 fixes the reasoning rather than the symptom: **for a book candidate, the record's
first-position author must be one of the candidate's authors.** A record whose first author is
someone else, with the target author trailing, is a review. Order-robust (set membership, not list
order), fires only for books, and silent when the record carries no author metadata. A self-test
holds it in place and the script refuses to run if it stops firing on Wilson or starts firing on the
legitimate Case & Deaton records.

Same-shape catches from the same probe, all of which signal 4 gets and the type rule alone does not
reason about correctly: Bergen in The Oral History Review (944 cites, type=article, reviewing
Edin & Kefalas), Sulaiman in Europai Tukor (48, reviewing Case & Deaton), Standing in Population and
Development Review and Love & Minnotte in J. Family Theory & Review (both reviewing Cherlin).

**The duplicate-record gate gets its first confirmed catch.** B.6 shipped it unvalidated, noting it
had never fired on a real case. Case & Deaton's *Deaths of Despair and the Future of Capitalism* is
indexed as FOUR distinct `book` records, all Princeton University Press eBooks, all authored Case &
Deaton, with the citations split 1088 / 368 / 284 / 222. Author agreement is present on all four, so
the corrected rule — demotion requires positive author agreement, missing metadata never counts —
demotes correctly and for the right reason. The gate should now be described as validated.

Same standing discipline as the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) from a LIVE
    OpenAlex sourcing pass (2026-08-18). They assert NO DOIs; the DOI is whatever the resolver
    returns for a ranked match.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached, because caching one turns a rate-limited call into a permanent "does not exist".
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication.

**The anchor set is small, and that is the finding rather than the budget.** The reconnaissance
(`147_d3c_recon_probe.py`) established that the treatment-mechanism-outcome intersection is empty:
place-based decline AND fertility returns 1,539, despair vocabulary AND fertility returns 604, and
all three together returns 12, none on topic. So PRIMARY_MEASURED_DESPAIR carries three anchors, all
from one post-communist research family, and the American cell that the hypothesis is actually about
carries **none** — recorded explicitly here rather than backfilled with a reduced-form decline study,
which would let the gap disappear into the recall denominator. If A6 surfaces one, it is a genuine
discovery.

The routing decoys carry one anchor per enforceable wall so the query is tested on routing and not
only on topical retrieval: Sobotka-Skirbekk-Philipov 2011 and Hanappi 2017 and Fahlen-Olah 2018 for
Wall 1 (C.5.a, and note all three were surfaced by forward-citing the PRIMARY anchor — the
citation-reason drift that makes the anomie channel drain into C.5.a), Dikmen 2019 for Wall 5
(reverse causation), Case & Deaton 2015 for Wall 4 (mortality outcome), Autor-Dorn-Hanson 2019 for
Wall 10 (marriage-only outcome), Billingsley 2009 for Call 5's context question.

SCRIPT NUMBERING: 146 is the highest in use on ANY branch, local or remote — not the highest on
`main`, which is the check that has failed twice in this repo. 147 is the reconnaissance probe and
this is 148.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, sys, time, unicodedata
from urllib.parse import quote

SLUG = "despair-hopelessness-fertility"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d3c_crossref_cache.json")
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


# --- Candidate anchors. Live-sourced 2026-08-14. NO DOIs asserted here by design. ---
CANDIDATES = [
    # ============================================================================================
    # PRIMARY_MEASURED_DESPAIR — the only cell where a despair-type construct is actually MEASURED
    # against a fertility quantity. It is small, it is one research family, and it is post-communist
    # rather than American. The scope document treats that mismatch as Call 5 rather than hiding it.
    # ============================================================================================
    dict(title="Soon, later, or ever? The impact of anomie and social capital on fertility "
               "intentions in Bulgaria and Hungary",
         authors=["Dimiter Philipov", "Zsolt Speder", "Francesco C. Billari"], year=2006,
         family="primary-anomie", provisional_cell="PRIMARY_MEASURED_DESPAIR",
         provenance_channel="reconnaissance_probe_primary_cell",
         note="Population Studies. THE anchor of this chapter's primary cell and the most-cited "
              "record in it (211). An anomie scale on the right-hand side, fertility intentions on "
              "the left. Everything the hypothesis claims, measured — in 1990s Bulgaria and Hungary, "
              "not post-industrial America."),
    dict(title="Now or Later? Fertility Intentions in Bulgaria and Hungary and the Impact of "
               "Anomie and Social Capital",
         authors=["Dimiter Philipov", "Zsolt Speder", "Francesco C. Billari"], year=2021,
         family="primary-anomie", provisional_cell="PRIMARY_MEASURED_DESPAIR",
         provenance_channel="reconnaissance_probe_primary_cell",
         note="The 2006 study's companion/reissue (20 cites). Must be extracted as a PAIR with the "
              "2006 record and never pooled with it — same design, same populations."),
    dict(title="Failure to Realize Fertility Intentions: A Key Aspect of the Post-communist "
               "Fertility Transition",
         authors=["Zsolt Speder", "Balazs Kapitany"], year=2013,
         family="primary-anomie", provisional_cell="PRIMARY_MEASURED_DESPAIR",
         provenance_channel="forward_citation_philipov_2006",
         note="Population Research and Policy Review (73). Non-realization of stated intentions in "
              "the post-communist collapse — the outcome D.3.c predicts if forward orientation, not "
              "desire, is what fails. The closest thing to a DESIRE_INDEPENDENCE test here."),

    # ============================================================================================
    # EARLY_FERT_OPPOSITE_SIGN — the same antecedent, the opposite sign. In the PRIMARY synthesis by
    # design (scope, Wall 6): a chapter that searched only for despair-lowers-fertility and reported
    # only what it found would be answering a question it had rigged.
    # ============================================================================================
    dict(title="Income Inequality and Early Nonmarital Childbearing",
         authors=["Melissa S. Kearney", "Phillip B. Levine"], year=2014,
         family="opposite-sign", provisional_cell="PRIMARY_ACCELERATION",
         provenance_channel="reconnaissance_probe_opposite_sign",
         note="Journal of Human Resources. The economics statement of despair-RAISES-early-fertility: "
              "low-SES young women in high-inequality places see a bleak return to delay and do not "
              "delay. DUPLICATE-RECORD GATE TEST CASE: two OpenAlex records, same title, same year, "
              "98 and 38 cites. Author agreement present, so demotion is correct under the corrected "
              "rule; a bare title+year+venue rule would have been right here for the wrong reason."),
    dict(title="Promises I Can Keep: Why Poor Women Put Motherhood before Marriage",
         authors=["Kathryn Edin", "Maria Kefalas"], year=2005, is_book=True, expect_no_doi=True,
         family="opposite-sign", provisional_cell="THEORY_DESPAIR",
         provenance_channel="canon_enumeration",
         note="BOOK-CANON GATE TEST CASE, and a live one. The citation argmax is a Choice Reviews "
              "book-review record (1,238) with NO authors; second is a review in The Oral History "
              "Review typed `article` (944, Bergen) which the type rule alone would not catch and "
              "signal 4 does. Qualitative: theory stream, never an effect source."),

    # ============================================================================================
    # SECONDARY_DECLINE_NO_MECHANISM and MARRIAGE_CHANNEL — the large reduced-form body. Present as
    # anchors so the query is tested on it, cell-tagged so it can never be silently read as primary.
    # ============================================================================================
    dict(title="When Work Disappears: Manufacturing Decline and the Falling Marriage Market Value "
               "of Young Men",
         authors=["David H. Autor", "David Dorn", "Gordon H. Hanson"], year=2019,
         family="decline-reduced-form", provisional_cell="MARRIAGE_CHANNEL",
         provenance_channel="canon_enumeration",
         note="AER: Insights (480). WALL 10 TEST CASE: the outcome is marriage-market value and "
              "fertility, and the fertility side is what routes here — a marriage-only study belongs "
              "to TICK-058. Also a VERSION-OF-RECORD test case: article (480), NBER-style preprint "
              "(201) and report (52) all carry this title. Names no despair mechanism."),
    dict(title="The China Syndrome: Local Labor Market Effects of Import Competition in the "
               "United States",
         authors=["David H. Autor", "David Dorn", "Gordon H. Hanson"], year=2013,
         family="decline-reduced-form", provisional_cell="SECONDARY_DECLINE_NO_MECHANISM",
         provenance_channel="canon_enumeration",
         note="AER (4,434). The treatment-definition anchor for chronic, expected-permanent local "
              "decline — the chronicity that Wall 1 says separates D.3.c from C.5.a. Estimates no "
              "fertility quantity itself; it is the design other studies inherit."),
    dict(title="The Puzzle of Falling US Birth Rates since the Great Recession",
         authors=["Melissa S. Kearney", "Phillip B. Levine", "Luke Pardue"], year=2022,
         family="phenomenon", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="canon_enumeration",
         note="Journal of Economic Perspectives (139). The phenomenon D.3.c proposes to explain, and "
              "the paper that shows the usual economic covariates do NOT explain it — which is the "
              "opening a despair hypothesis is trying to fill. Feeds stage 10, not the effect pool. "
              "VERSION-OF-RECORD test case: article 139 / preprint 11 / report 2."),

    # ============================================================================================
    # THEORY_DESPAIR — including the challenges to the despair reading. A chapter rating a despair
    # mechanism must carry the evidence that the mechanism is misidentified where it was first named.
    # ============================================================================================
    dict(title="Rising morbidity and mortality in midlife among white non-Hispanic Americans in "
               "the 21st century",
         authors=["Anne Case", "Angus Deaton"], year=2015,
         family="deaths-of-despair-canon", provisional_cell="DESPAIR_MORTALITY",
         provenance_channel="canon_enumeration",
         note="PNAS (2,782). WALL 4 TEST CASE: the founding deaths-of-despair paper, whose outcome "
              "is mortality and not fertility. Routed OUT but deliberately SEEDABLE — the uniform "
              "seed rule holds, and forward-citing it is the best available channel into a thin "
              "primary cell. Its forward citations filtered to fertility return 129, of which the "
              "citation-ranked head is life-expectancy work; that near-emptiness IS a finding."),
    dict(title="Deaths of Despair and the Future of Capitalism",
         authors=["Anne Case", "Angus Deaton"], year=2020, is_book=True,
         family="deaths-of-despair-canon", provisional_cell="THEORY_DESPAIR",
         provenance_channel="canon_enumeration",
         note="Princeton UP. v5's seminal, and the chapter's framing text. DUPLICATE-RECORD GATE "
              "TEST CASE and the project's FIRST genuine one: FOUR distinct `book` records, all "
              "Princeton UP eBooks, all authored Case & Deaton, citations split 1088/368/284/222. "
              "Author agreement is present on all four, so the corrected rule demotes correctly. "
              "Also the negative control for book-canon signal 4 — Case is first on all four."),
    dict(title="Declining human fertility and the epidemic of despair",
         authors=["Michael L. Platt", "Peter Sterling"], year=2024,
         family="named-perspective", provisional_cell="THEORY_DESPAIR",
         provenance_channel="v5_seminal_list_corrected",
         note="Nature Mental Health, doi 10.1038/s44220-024-00241-1 (5 cites). v5 cites this to a "
              "EurekAlert press release; this is the paper. It did NOT resolve under title search "
              "and was recovered only by an author-filtered probe, so it is carried here explicitly "
              "to force the resolver to reach it. Apparently a perspective by two neuroscientists, "
              "not an empirical fertility study — class confirmed at retrieval, THEORY_DESPAIR "
              "unless it proves otherwise. Forward citations: 2, neither empirical."),
    dict(title="Deaths of Despair or Drug Problems?",
         authors=["Christopher J. Ruhm"], year=2018,
         family="contested-framework", provisional_cell="THEORY_DESPAIR",
         provenance_channel="reconnaissance_probe_contested",
         note="NBER (94). The load-bearing challenge: the mortality rise is better explained by drug "
              "supply than by despair. If the despair reading fails where it was coined, a fertility "
              "extension of it inherits that weakness. VERSION-OF-RECORD test case: NBER report (94) "
              "and RePEc preprint (0), no journal version surfaced."),
    dict(title="Labor's Love Lost: The Rise and Fall of the Working-Class Family in America",
         authors=["Andrew J. Cherlin"], year=2014, is_book=True, expect_no_doi=True,
         family="sociological-canon", provisional_cell="THEORY_DESPAIR",
         provenance_channel="v5_seminal_list",
         note="Russell Sage. v5's third seminal. BOOK-CANON GATE TEST CASE: resolves to a Choice "
              "Reviews book-review (226, no authors) and to review-shaped `article` records by "
              "Standing (PDR) and Love & Minnotte (J Fam Theory Rev)."),
    dict(title="When Work Disappears: The World of the New Urban Poor",
         authors=["William Julius Wilson"], year=1996, is_book=True, expect_no_doi=True,
         family="sociological-canon", provisional_cell="THEORY_DESPAIR",
         provenance_channel="canon_enumeration",
         note="THE GATE TEST CASE OF THIS RUN, and the reason signal 4 exists. The citation argmax "
              "is 10.2307/3042249 — Daryl Michael Scott's REVIEW in African American Review, 3,641 "
              "cites, type=`article`, WITH WILSON LISTED AS AN AUTHOR. It defeats all three prior "
              "review signals and turns `author_match` into an endorsement of the wrong record. "
              "Separately a TITLE-COLLISION case against Autor-Dorn-Hanson 2019, which opens with "
              "the identical five words and is a different work in a different literature."),

    # ============================================================================================
    # ROUTING DECOYS — one per wall the screen must enforce. A search tested only on topical
    # retrieval is not tested on the thing that actually decides this chapter's corpus.
    # ============================================================================================
    dict(title="Economic Recession and Fertility in the Developed World",
         authors=["Tomas Sobotka", "Vegard Skirbekk", "Dimiter Philipov"], year=2011,
         family="decoy-wall1", provisional_cell="TRANSITORY_SHOCK",
         provenance_channel="forward_citation_philipov_2006",
         note="PDR (865). WALL 1 DECOY, and the sharpest one available: same senior author as the "
              "primary anchor, but the treatment is a TRANSITORY recession with an expected return "
              "to normalcy. Routes to C.5.a. If the screen cannot separate this from Philipov 2006 "
              "it cannot enforce Wall 1 at all — which the scope already concedes it cannot do at "
              "title/abstract, making this a full-text calibration case."),
    dict(title="Changes in Employment Uncertainty and the Fertility Intention-Realization Link: "
               "An Analysis Based on the Swiss Household Panel",
         authors=["Doris Hanappi", "Valerie-Anne Ryser", "Laura Bernardi", "Jean-Marie Le Goff"],
         year=2017,
         family="decoy-wall1", provisional_cell="OFF_UNCERT_C5a",
         provenance_channel="forward_citation_philipov_2006",
         note="European Journal of Population (88). WALL 1 DECOY. Surfaced by forward-citing the "
              "primary anchor AND matching the despair vocabulary — the citation-reason drift that "
              "makes the anomie channel drain into C.5.a. Personal employment uncertainty, not a "
              "collapse of forward orientation."),
    dict(title="Economic uncertainty and first-birth intentions in Europe",
         authors=["Susanne Fahlen", "Livia Sz. Olah"], year=2018,
         family="decoy-wall1", provisional_cell="OFF_UNCERT_C5a",
         provenance_channel="forward_citation_philipov_2006",
         note="Demographic Research (71). Second Wall 1 decoy from the same drift, kept because one "
              "decoy per wall does not measure a routing rule that has to hold across a cluster."),
    dict(title="Stigma, hopelessness and coping experiences of Turkish women with infertility",
         authors=["Zehra Kaya", "Umran Oskay"], year=2019,
         family="decoy-wall5", provisional_cell="REVERSE",
         provenance_channel="reconnaissance_probe_reverse",
         note="J Reprod Infant Psychol (71), Kaya & Oskay. THE AUTHOR GATE'S OWN TEST CASE, passed "
              "against the analyst: this candidate was first entered with the authors guessed as "
              "Dikmen & Terzioglu, the gate refused the correct DOI at Jaccard 1.00 as "
              "`authors_disagree`, and the live record showed the gate was right and the candidate "
              "wrong. Corrected from the record rather than by relaxing the gate. WALL 5 DECOY. The reverse-causation body owns the "
              "validated-instrument literature: every Beck Hopelessness Scale record the probe "
              "surfaced is infertility distress. Childlessness -> hopelessness, the arrow this "
              "chapter is not about."),
    dict(title="The Post-Communist Fertility Puzzle",
         authors=["Sunnee Billingsley"], year=2009,
         family="decoy-context", provisional_cell="SECONDARY_DECLINE_NO_MECHANISM",
         provenance_channel="forward_citation_philipov_2006",
         note="Population Research and Policy Review (143). The context anchor for Call 5: the "
              "post-communist decline as a whole, against which the anomie studies' contribution "
              "has to be judged before their transportability to America is even discussed."),
]


# Latin letters that NFKD does NOT decompose, so they would still be dropped after folding. Nordic,
# Polish and Turkish surnames are common in the European demographic literature this chapter lives in.
_TRANSLIT = str.maketrans({"ø": "o", "Ø": "o", "ß": "ss", "đ": "d", "Đ": "d", "ł": "l", "Ł": "l",
                           "ı": "i", "İ": "i", "æ": "ae", "Æ": "ae", "œ": "oe", "Œ": "oe",
                           "þ": "th", "Þ": "th", "ð": "d", "Ð": "d", "ħ": "h", "ŧ": "t"})


def norm(s):
    """Fold to ASCII FIRST, then strip. The order is the whole point.

    The inherited version ran `re.sub(r"[^a-z0-9 ]", " ", s.lower())` with no folding, which replaces
    each non-ASCII character with a SPACE — so it did not merely fail to match an accented name, it
    SHATTERED it, and `surnames()` then took the last fragment:

        "Zsolt Speder"    vs index "Zsolt Spéder"     -> "speder"    vs "der"
        "Susanne Fahlen"  vs index "Susanne Fahlén"   -> "fahlen"    vs "n"
        "Livia Sz. Olah"  vs index "Lívia Sz. Oláh"   -> "olah"      vs "h"
        "Fusun Terzioglu" vs index "Füsun Terzioğlu"  -> "terzioglu" vs "lu"

    The author gate then returned False — "this record HAS authors and none of them is ours" — which
    is a confident wrong negative, not a missing-data None. On this chapter's first A3 run it refused
    three anchors that had already resolved to exactly the right DOI, at Jaccard 1.00, in the right
    venue and the right year: Speder & Kapitany 2013, Fahlen & Olah 2018, Dikmen & Terzioglu 2019.

    `norm()` also feeds `toks()` -> `jaccard()`, so the same shattering inflates the token count of any
    TITLE carrying a diacritic and depresses its Jaccard against an ASCII candidate. The defect is
    therefore not confined to the author gate, and it is inherited by every chapter that has run this
    resolver. Blast radius is measured in {slug}-anchor-norm-audit.md rather than assumed.

    Same family as the `norm()`-strips-punctuation finding (shadow patterns containing `:` or `,` are
    dead code) — same function, same silence, opposite direction: that one made a rule never fire,
    this one made a rule fire wrongly."""
    s = (s or "").translate(_TRANSLIT)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


_NORM_SELFTEST = [("Zsolt Spéder", "speder"), ("Susanne Fahlén", "fahlen"), ("Lívia Sz. Oláh", "olah"),
                  ("Füsun Terzioğlu", "terzioglu"), ("Tomáš Sobotka", "sobotka"),
                  ("Øystein Kravdal", "kravdal"), ("Wolfgang Lutz", "lutz")]


def norm_selftest():
    """Refuse to run if surname folding regresses. Each case is a real name from this literature."""
    bad = [(raw, want, norm(raw).split()[-1]) for raw, want in _NORM_SELFTEST
           if norm(raw).split()[-1] != want]
    if bad:
        sys.stderr.write("ABORT: norm() folding self-test failed:\n")
        for raw, want, got in bad:
            sys.stderr.write(f"  {raw!r} -> expected surname {want!r}, got {got!r}\n")
        sys.exit(1)


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


def first_author_surname(rec_authors):
    """Surname of the record's FIRST-position author, or None if position metadata is absent."""
    for a in rec_authors or []:
        parts = norm(a).split()
        if parts:
            return parts[-1]
    return None


def looks_like_review(rec_title, container, cand_authors, is_book=False, rec_authors=None):
    """Is this record a review OF the work rather than the work? FOUR independent signals, because a
    review that credits the book's own authors defeats the author gate — which is exactly what
    Leridon 1977, Sheps & Menken 1973, and Preston 1978 do in the live index.

    Signal 4 is NEW (D.3.c, 2026-08-18) and was added against a live case that defeats the other
    three AND defeats the author gate in the strongest way yet seen:

        10.2307/3042249 — "When Work Disappears: The World of the New Urban Poor."
        African American Review, 1998, type=article, **3,641 cites**
        authorships = [Daryl Michael Scott (first), William Julius Wilson (last)]

    That is Scott's REVIEW of Wilson's 1996 monograph. It defeats signal 1 (the title is the book's
    title exactly, no review shape), signal 2 ("African American Review" contains none of the review-
    container substrings — the word "Review" is part of an ordinary journal name), and signal 3 (the
    lead-name test requires a comma and the title has a colon). It then defeats `author_match`, which
    returns **True** because Wilson is listed among the authors — so the record does not merely slip
    past the gate, it is actively endorsed by it and scored higher for it. And it is the citation
    argmax by a factor of three, so any ranking that leans on citations selects it.

    The standing finding was that monographs resolve to their own reviews and that the author gate
    plus a fallback flag were the defence. This case shows author-list MEMBERSHIP is not enough:
    a review indexed this way credits the reviewed author. **Position is the discriminator.** For a
    book candidate, the record's first-position author must be one of the candidate's authors; a
    record whose first author is someone else, with the target author trailing, is a review.

    Order-robust by construction: the test asks whether the record's first author is IN the candidate
    author SET, not whether the two lists are ordered alike, so listing the candidate's authors in any
    order is safe. Verified against the true positives in this corpus — all four Case & Deaton book
    records have Case first — and against the false ones: Bergen in The Oral History Review (944
    cites), Sulaiman in Európai Tükör (48), Standing in Population and Development Review, Sharpe in
    Challenge, Love & Minnotte in J. Family Theory & Review, Eckardt, Guerlain.

    Fires only for `is_book` candidates and only when the record carries author metadata, so an
    author-less index record is still missing information rather than contradicting it."""
    t = (rec_title or "")
    if any(re.search(p, t, flags=re.I) for p in REVIEW_TITLE_PATTERNS):
        return True
    if any(k in (container or "").lower() for k in REVIEW_CONTAINERS):
        return True
    # "Robert Woods, Death Before Birth: ..." — a review titled with the reviewed author's name first.
    lead = norm(t).split(",")[0] if "," in t else ""
    if lead and surnames(cand_authors) & set(lead.split()):
        return True
    # Signal 4 — first-author position, book candidates only. See the Wilson case above.
    if is_book and rec_authors:
        fa = first_author_surname(rec_authors)
        cs = surnames(cand_authors)
        if fa and cs and fa not in cs:
            return True
    return False


_BOOKGATE_SELFTEST = [
    # (rec_title, container, cand_authors, rec_authors, expect_review)
    ("When Work Disappears: The World of the New Urban Poor.", "African American Review",
     ["William Julius Wilson"], ["Daryl Michael Scott", "William Julius Wilson"], True),
    ("Deaths of Despair and the Future of Capitalism", "Princeton University Press eBooks",
     ["Anne Case", "Angus Deaton"], ["Anne Case", "Angus Deaton"], False),
    ("Deaths of Despair and the Future of Capitalism", "Europai Tukor",
     ["Anne Case", "Angus Deaton"], ["Saqer Sulaiman"], True),
    ("Promises I Can Keep: Why Poor Women Put Motherhood Before Marriage", "The Oral History Review",
     ["Kathryn Edin", "Maria Kefalas"], ["Teresa Bergen"], True),
    # Order-robustness: candidate authors listed in the reverse order of the record's.
    ("Promises I Can Keep", "University of California Press",
     ["Maria Kefalas", "Kathryn Edin"], ["Kathryn Edin", "Maria Kefalas"], False),
    # An author-less index record must stay "missing information", never a review by signal 4 alone.
    ("Labor's love lost", "Some Press", ["Andrew Cherlin"], [], False),
]


def bookgate_selftest():
    """Refuse to run on a broken gate. The gate is only load-bearing if it fires on Wilson and stays
    silent on the four legitimate Case & Deaton book records."""
    bad = []
    for t, c, ca, ra, want in _BOOKGATE_SELFTEST:
        got = looks_like_review(t, c, ca, is_book=True, rec_authors=ra)
        if got != want:
            bad.append((t[:44], c[:24], want, got))
    if bad:
        sys.stderr.write("ABORT: book-canon gate self-test failed:\n")
        for t, c, w, g in bad:
            sys.stderr.write(f"  {t!r} [{c}] expected {w}, got {g}\n")
        sys.exit(1)


# --------------------------------------------------------------------------------------------
# SHADOW-RECORD GATE (new, B.7, 2026-08-12).
# --------------------------------------------------------------------------------------------
# A shadow record is a real, separately-DOI'd, correctly-indexed record whose title is the target
# title with a leading qualifier bolted on. It defeats all three inherited gates by construction: it
# exists, it is not a preprint, and it is not a review of a monograph. On the overlap coefficient it
# scores 1.0, because the target title is wholly contained in it.
#
# Two families, and they need different handling:
#   * COMMENTARY shadows ("Editorial Comment to", "Faculty Opinions recommendation of", "Re:") are
#     refused and logged. Nothing about them changes what we believe about the anchor.
#   * INTEGRITY shadows ("Expression of Concern", "Retraction of", "Correction to") are refused as
#     anchors AND recorded as a flag ON the anchor, because their existence is a fact about the work
#     that risk of bias has to see. Refusing them silently would throw that away.
# !! THESE PATTERNS ARE MATCHED AGAINST norm()-ED TITLES. !!
# norm() strips every character outside [a-z0-9 ], so a pattern containing a colon, comma, hyphen or
# apostrophe CANNOT EVER MATCH. Three inherited patterns were written with punctuation and were
# therefore dead code from the day they were added — `^re\s*:`, `^corrections?\s*(:|...)` and the
# `letter to the editor` variant that required "re|regarding|concerning" where the live records use a
# comma. Found 2026-08-14 (B.6) when "Correction: The Minderoo-Monaco Commission on Plastics and
# Human Health" passed the gate, scored 120, and TIED with the article of record — kept out of the
# anchor slot by the tie-break alone. The same three holes exist in `124_b7_cold_start_anchors.py`,
# whose docstring claims a "Re:" catch it cannot have made; flagged in TICK-068 for that branch.
# The self-test below exists so this class of defect cannot return silently.
SHADOW_QUALIFIERS = (
    (r"^editorial\s+comment\s+(to|on)\b", "commentary"),
    (r"^faculty\s+opinions?\s+recommendation\s+of\b", "commentary"),
    (r"^re\b", "commentary"),
    (r"^comment\s+on\b", "commentary"),
    (r"^response\s+to\b", "commentary"),
    (r"^discussion\s+of\b", "commentary"),
    (r"^abstract\s+of\b", "commentary"),
    (r"^reply\s+to\b", "commentary"),
    (r"^in\s+reply\b", "commentary"),
    (r"^authors?\s+response\b", "commentary"),
    (r"^letter\s+to\s+the\s+editors?\b", "commentary"),
    (r"^letter\s+(re|regarding|concerning)\b", "commentary"),
    (r"^correspondence\s+(on|regarding)\b", "commentary"),
    (r"^expressions?\s+of\s+concern\b", "integrity"),
    (r"^retractions?\b", "integrity"),
    (r"^corrections?\b", "integrity"),
    (r"^erratum\b", "integrity"),
    (r"^corrigend(um|a)\b", "integrity"),
    (r"^reprint\s+of\b", "version"),
)

# (record title, candidate title, expected verdict). Every entry is a REAL pair observed live in this
# corpus or B.7's, not a constructed one. A gate is only tested by cases it can fail, and the last
# three are the negatives that keep the bare qualifiers above from eating genuine work.
_SHADOW_SELFTEST = [
    ("Correction: The Minderoo-Monaco Commission on Plastics and Human Health",
     "The Minderoo-Monaco Commission on Plastics and Human Health", "integrity"),
    ("Re: Temporal Trends in Sperm Count: A Systematic Review and Meta-Regression Analysis",
     "Temporal trends in sperm count: a systematic review and meta-regression analysis", "commentary"),
    ("Letter to the editor, discovery and quantification of plastic particle pollution in human blood",
     "Discovery and quantification of plastic particle pollution in human blood", "commentary"),
    ("Faculty Opinions recommendation of Do perfluoroalkyl compounds impair human semen quality?",
     "Do Perfluoroalkyl Compounds Impair Human Semen Quality?", "commentary"),
    ("Editorial Comment to Effect of antidepressant medications on semen parameters",
     "Effect of antidepressant medications on semen parameters", "commentary"),
    # Negatives. A real work whose title merely begins with a qualifier-like word, and a subtitle
    # extension, must both pass through untouched.
    ("Reducing exposure to high levels of perfluorinated compounds in drinking water improves "
     "reproductive outcomes", "Plasticenta: First evidence of microplastics in human placenta", None),
    ("Retention of microplastics in human tissue", "Plasticenta: First evidence of microplastics in "
     "human placenta", None),
    ("Temporal trends in sperm count: a systematic review and meta-regression analysis of samples "
     "collected globally", "Temporal trends in sperm count: a systematic review and meta-regression "
     "analysis", None),
]


def shadow_selftest():
    """Fail loudly at start-up rather than silently under-refusing for a whole run."""
    bad = []
    for rec_t, cand_t, expect in _SHADOW_SELFTEST:
        got = shadow_kind(rec_t, cand_t)
        if got != expect:
            bad.append(f"  shadow_kind({rec_t[:52]!r}) = {got!r}, expected {expect!r}")
    return bad


def shadow_kind(rec_title, cand_title):
    """Return 'commentary' | 'integrity' | 'version' if the record is a shadow of the candidate,
    else None.

    ONE test, deliberately: the record title opens with a named qualifier and continues into the
    target title. The first version of this gate carried a second, general test — the candidate title
    appearing as a proper suffix of a longer record title — and reading its refusals is what killed
    it. On the three-token anchor "Antipsychotic-Induced Hyperprolactinaemia" that rule refused five
    records, and every one was a *distinct work* whose title happens to end in the phrase:
    "Management of antipsychotic-induced hyperprolactinaemia", "Bone mineral density in premenopausal
    women with antipsychotic-induced hyperprolactinaemia", and three others. Suffix containment
    cannot separate a comment on a paper from a different paper about the same thing, and no token
    threshold fixes it, because the shapes are the same length. The named-qualifier list caught every
    genuine shadow in this canon without it; an unnamed shadow shape is left to the author, type and
    version signals rather than bought at the price of refusing real work.

    A record that merely EXTENDS the candidate title with a subtitle the candidate omitted — Wilcox
    1995's "- Effects on the Probability of Conception ..." — is a prefix relation, never a shadow,
    and passes here and at the title gate."""
    rt, ct = norm(rec_title), norm(cand_title)
    if not rt or not ct or rt == ct:
        return None
    for pat, kind in SHADOW_QUALIFIERS:
        if re.search(pat, rt):
            # Only a shadow OF THIS candidate: the qualifier must be followed by the target title, or
            # by enough of it that the index truncation explains the rest.
            tail = re.sub(pat, "", rt).strip(" :-")
            if tail and (tail.startswith(ct[:40]) or ct.startswith(tail[:40])):
                return kind
    return None


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

# Venues that REPUBLISH other journals' articles rather than originating them: digests, surveys and
# yearbooks. Their records are correctly titled, correctly authored, correctly typed and
# contemporaneous, so nothing else in the scorer separates them from the article of record — and on
# the first run of this script that is exactly what went wrong. Alwan et al. 2007 was planted in the
# candidate set as a version-gate test case precisely because it has three such twins, and the gate
# failed it: the NEJM original and the Obstetrical & Gynecological Survey reprint both scored 120 and
# the tie broke on list order. A gate is only tested by a case it can fail.
REPRINT_CONTAINERS = ("obstetrical & gynecological survey", "obstetrical and gynecological survey",
                      "survey of anesthesiology", "yearbook of", "year book of", "journal watch",
                      "obstetric anesthesia digest")


def is_reprint_venue(container):
    c = (container or "").lower()
    return any(k in c for k in REPRINT_CONTAINERS)


def _cand_score(cand_title, cand_year, it_title, it_year, it_type, it_container, it_doi,
                auth_state, is_review):
    """Score a candidate for being the VERSION OF RECORD of the anchor.

    Title fit was previously a pure GATE and no part of the score, on the reasoning that records
    sharing one title are separated by type, venue, year, authorship and review-shape. That holds only
    if everything reaching the scorer really does share the title — and it does not. The gate admits
    down to TITLE_JACCARD_FLOOR (0.45) so that a record differing by a subtitle survives, and a record
    admitted at 0.5 then competed on type alone against a record admitted at 1.0.

    Ruhm 2018, "Deaths of Despair or Drug Problems?", is the case that exposed it. Two candidates:

        J=1.00  10.3386/w24188        report        NBER            <- the work
        J=0.50  10.2307/j.ctvpr7rb2.7 book-chapter  "Deaths of Despair", a chapter of Case &
                                                    Deaton's BOOK — a different work entirely

    `book-chapter` ranks 50 and `report` ranks 30, and the NBER DOI prefix additionally carries the
    non-version-of-record penalty, so the chapter scored 22 against the working paper's 5 and won. The
    anchor was reported NO-MATCH while its exact, live, correctly-titled record sat in the field.

    Title fit is therefore now a bounded score term as well as a gate. It is squared so that the
    penalty concentrates on genuinely poor matches rather than nibbling at subtitle drift, and capped
    at 45 — below the 70-90 point authorship and review-shape penalties, which must stay decisive, but
    comfortably above the type gaps that separate legitimate version-of-record candidates. It does not
    disturb the NBER-versus-journal preference: when both carry the same title they receive the same
    bonus and NON_VOR_PREFIXES still decides, which is the intended behaviour when a journal version
    exists. It only stops a worse-titled record from winning on type.

    This matters beyond one anchor: working papers are the version of record for a large part of the
    economics literature this review draws on, and they are exactly the records the type ranking is
    most sceptical of."""
    score = TYPE_RANK.get(canon_type(it_type), 10)
    score += round(45 * (jaccard(cand_title, it_title) ** 2))
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
    if is_reprint_venue(it_container):
        score -= 40          # a digest republishing the article is not the article
    if it_container:
        score += 5
    return score


def _title_gate(cand_title, it_title, is_book=False):
    j = jaccard(cand_title, it_title)
    ov = overlap_coef(cand_title, it_title)
    floor = BOOK_TITLE_FLOOR if is_book else TITLE_JACCARD_FLOOR
    ok = j >= TITLE_JACCARD_MIN or (title_prefix_match(cand_title, it_title) and j >= floor)
    return ok, round(j, 3), round(ov, 3)


# Titles the OpenAlex query parser refused, kept so a refusal can never be read as an absence.
OA_QUERY_ERRORS = []


def oa_search_safe(title):
    """Strip OpenAlex wildcard operators from a relevance-search string.

    `?` and `*` are WILDCARDS in `search=`. A title containing either is not merely unhelpful as a
    query — it is REJECTED, with a 200 whose body is
        {"error": "Invalid query parameters error.",
         "message": "Wildcards (* or ?) require exact (no-stem) search..."}
    which `.get("results", [])` renders as an empty field. Found on Ruhm 2018, "Deaths of Despair or
    Drug Problems?", whose NBER record 10.3386/w24188 is indexed, live and correctly titled, and which
    this resolver reported as NO-MATCH through three retries. Interrogative titles are common in
    economics and demography, so this is not an edge case in this literature.

    Stripping the characters beats switching to `search.exact=`: relevance search still has to tolerate
    the subtitle and capitalisation drift that exact search does not, and the punctuation carries no
    retrieval signal — `norm()` discards it on both sides before any title comparison is made."""
    return re.sub(r"\s+", " ", re.sub(r"[?*]", " ", title or "")).strip()


def _openalex_rows(title):
    # per-page raised 8 -> 20 for B.6. The duplicate-record gate can only cluster copies it is shown,
    # and at 8 the second Minderoo-Monaco record (10.5334/aogh.4083) never entered the field, so the
    # gate's own test case passed for the wrong reason: the right DOI won on the tie-break rather
    # than on the gate. A gate that is never given the case it was built for has not been tested.
    # Cache key bumped with the page size, or the stale 8-row response would be served forever.
    key = f"OAROWS20::{title}"
    if key in cache:
        return cache[key]
    # cited_by_count is selected for the DUPLICATE-RECORD gate: when one work is indexed twice under
    # two DOIs, the citation count is the only signal that separates the copy the field actually
    # cites from the copy it does not. Crossref carries no equivalent, so cross-source duplicates
    # fall back to score.
    url = _oa_auth(f"https://api.openalex.org/works?search={quote(oa_search_safe(title))}&per-page=20"
                   "&select=id,doi,title,publication_year,type,authorships,primary_location,"
                   "cited_by_count")
    results, api_error = [], None
    for attempt in range(3):
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        try:
            payload = json.loads(out)
        except Exception:
            payload, results = {}, []
        else:
            # A 200 carrying an {"error": ...} body is NOT an empty result set. Reading it through
            # .get("results", []) turns a REFUSED query into a confident "this work does not exist" —
            # the same failure as counting a failed request as a zero hit, reached through the JSON
            # layer rather than the transport layer. Recorded, never silently emptied.
            if isinstance(payload, dict) and payload.get("error"):
                api_error = f"{payload.get('error')} {str(payload.get('message'))[:110]}"
                results = []
            else:
                results = payload.get("results", [])
        if results:
            break
        time.sleep(1.5 * (attempt + 1))
    if api_error:
        OA_QUERY_ERRORS.append((title[:70], api_error))
        sys.stderr.write(f"  OpenAlex REFUSED the query for {title[:50]!r}: {api_error}\n")
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


def _dup_signature(r):
    """Identity of a WORK, deliberately excluding the DOI.

    Title, year and venue together. Two records agreeing on all three and disagreeing on DOI are the
    same work indexed twice, not two works — which is exactly the case DOI-level deduplication cannot
    see. Year is compared exactly rather than within YEAR_TOL: a genuine duplicate pair is registered
    from the same publication event, so a year disagreement is evidence AGAINST duplication and the
    conservative reading is to keep both."""
    return (norm(r.get("matched_title") or ""), r.get("cr_year"), norm(r.get("container") or ""))


def duplicate_groups(scored):
    """Clusters of >1 DISTINCT DOI sharing one work signature AND an agreeing author set.

    A record appearing from both Crossref and OpenAlex under the SAME DOI is one record seen twice by
    the resolver, not a duplicate publication, so grouping is on the distinct-DOI count rather than
    the member count.

    THE AUTHOR-AGREEMENT REQUIREMENT IS LOAD-BEARING AND WAS ADDED AFTER THE GATE'S MOTIVATING CASE
    TURNED OUT TO BE SOMETHING ELSE. `10.5334/aogh.4056` and `10.5334/aogh.4083` share title, year,
    volume and venue and were read as one work deposited twice. They are not: 4056 is the Commission
    report under 48 authors and 4083 is a single-author companion piece by Maria Neira, deposited
    under the identical title. The author gate upstream already separates them, correctly, and this
    gate never saw them.

    Without this requirement the gate would actively cause harm in exactly that case. `author_match`
    returns None — not False — when a record carries no author metadata, so an author-less record
    PASSES upstream; a title+year+venue rule would then demote a legitimately distinct same-title work
    as a duplicate, silently, which is the same defect as the suffix-containment rule the shadow gate
    discarded. Demotion now requires positive evidence that the author sets agree, and missing
    metadata is never that evidence."""
    groups = {}
    for r in scored:
        groups.setdefault(_dup_signature(r), []).append(r)
    out = {}
    for sig, members in groups.items():
        if len({(m.get("doi") or "").lower() for m in members if m.get("doi")}) <= 1:
            continue
        sets = [surnames(m.get("authors") or []) for m in members]
        if any(not s for s in sets):
            continue                      # missing authorship is not evidence of sameness
        if not set.intersection(*sets):
            continue                      # different author sets => different works, same title
        out[sig] = members
    return out


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
    # v4 = the duplicate-record gate, which changes which record can win, so B.7's cached verdicts
    # must not be served here.
    key = f"D3CNORM2::{title}::{year}::{is_book}::{'|'.join(cand.get('authors') or [])}"
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
                "authors": _cr_authors(it), "cites": None, "src": "crossref"}))
    for w in _openalex_rows(title):
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        items.append((title, {
            "doi": doi or None, "title": w.get("title") or "", "year": w.get("publication_year"),
            "container": (((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""),
            "type": w.get("type"),
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])],
            "cites": w.get("cited_by_count"), "src": "openalex"}))

    scored, fallback, drops, integrity = [], None, [], []
    for gate_title, it in items:
        ok, j, ov = _title_gate(gate_title, it["title"], is_book)
        auth_state = author_match(cand.get("authors"), it["authors"])
        is_review = looks_like_review(it["title"], it["container"], cand.get("authors"),
                                      is_book=is_book, rec_authors=it["authors"])
        shadow = shadow_kind(it["title"], title)
        rec = {"doi": it["doi"], "matched_title": it["title"], "jaccard": j, "overlap": ov,
               "cr_year": it["year"], "container": it["container"], "type": it["type"],
               "src": it["src"], "author_match": auth_state, "review_shape": is_review,
               "shadow": shadow}
        # An integrity shadow is recorded BEFORE any refusal, because the point of noticing it is not
        # to keep it out of the anchor slot — it is to keep the fact attached to the anchor.
        if shadow == "integrity":
            integrity.append({"kind": shadow, "title": it["title"], "doi": it["doi"],
                              "year": it["year"], "container": it["container"]})
        # The fallback is a diagnostic and must not become a shadow: reporting "closest match: the
        # Faculty Opinions record" invites exactly the misreading the gate exists to prevent.
        if not shadow and (fallback is None or j > fallback["jaccard"]):
            fallback = {**rec, "is_fallback": True}
        if shadow:
            drops.append((f"shadow_record:{shadow}", it["title"][:60], it["doi"]))
            continue                                   # a comment on the work is never the work
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
        # SCORE FLOOR (D.3.c, 2026-08-18). `_cand_score` returns a NEGATIVE score for a record the
        # ranking actively disbelieves — wrong type for a book, republishing venue, no author support.
        # Nothing downstream refused such a record: with no positively-scored rival it simply won the
        # argmax and was emitted as a year-drift keep. On this chapter's first run Wilson 1996 resolved
        # that way to 10.5040/9798400607950.0151 — score -50, type `other`, a 2014 Bloomsbury reference
        # entry in "African Americans and Criminal Justice", which is not the monograph. The book-canon
        # gate had correctly refused the Scott review just above it; the resolver then took something
        # worse and labelled it a keep. A negative score is a statement that the record is wrong, and
        # it is now treated as one.
        if rec["score"] < 0:
            drops.append((f"negative_score:{rec['score']}", it["title"][:60], it["doi"]))
            continue
        rec["cites"] = it.get("cites")
        rec["authors"] = it.get("authors")     # required by the duplicate gate's author-agreement test
        rec["is_fallback"] = False
        scored.append(rec)

    if not scored:
        out = fallback or {"doi": None, "jaccard": 0.0, "is_fallback": True}
        out["is_fallback"] = True
        # Why nothing survived, so the RA auditing a book miss can see what was refused instead of
        # inferring it from the fallback's own flags, which describe a different record.
        out["refused_reasons"] = sorted({d[0] for d in drops})
        out["refused_candidates"] = [{"reason": r, "title": t, "doi": d} for r, t, d in drops[:6]]
        if integrity:
            out["integrity_flag"] = integrity
        cache[key] = out
        json.dump(cache, open(CACHE, "w"), indent=0)
        return out
    # Ties are broken deterministically rather than by list order. Before this, equal-scoring records
    # resolved by whichever source happened to be appended first, which is not a decision — it is the
    # absence of one, and it is what sent Alwan et al. 2007 to a digest reprint.
    #
    # Order of preference after score: closer title fit, then an originating venue over a
    # republishing one, then the earlier record (a reprint cannot precede its original), then the
    # DOI so the same inputs always give the same answer.
    #
    # The title-fit term was added second, after the first version of this tie-break created its own
    # regression: with only venue and year to go on, Serretti and Chiesa 2009 moved from the Journal
    # of Clinical Psychopharmacology article to a European Psychiatry conference abstract of the same
    # meta-analysis, because both scored 120 and the Elsevier DOI sorts first as a string. The
    # abstract carries an expanded subtitle, so the candidate title matches the article exactly and
    # the abstract only partially — which is the signal that separates them. Deterministic and wrong
    # is not an improvement on accidentally right; the fix is a term that means something, not a
    # different arbitrary key.
    #
    # No pattern for conference-poster codes is included, deliberately. It would catch the same case
    # and would be the fifth unanchored-pattern bug in this codebase; the title-fit term reaches the
    # answer without guessing at a title grammar.
    # DUPLICATE-RECORD GATE (new, B.6, 2026-08-14). Runs BEFORE the sort, because its job is to
    # remove members from the field rather than to reorder it — leaving both copies in and trusting
    # the tie-break would make the winner depend on DOI string order, which is the coin flip the gate
    # exists to eliminate. Within a cluster the canonical copy is the most-cited one: citations are a
    # statement about which record the field actually uses, and score cannot separate copies that
    # agree on title, year, venue and type. Demotions are RECORDED on the anchor, never silent — a
    # silent drop is indistinguishable from a record that was never retrieved.
    dups_demoted = []
    dgroups = duplicate_groups(scored)
    if dgroups:
        demoted_ids = set()
        for _sig, members in dgroups.items():
            members.sort(key=lambda r: (-(r["cites"] if r.get("cites") is not None else -1),
                                        -r.get("score", 0), r.get("doi") or ""))
            canonical = members[0]
            for m in members[1:]:
                if (m.get("doi") or "").lower() == (canonical.get("doi") or "").lower():
                    continue                       # same record seen by both sources, not a duplicate
                demoted_ids.add(id(m))
                dups_demoted.append({"demoted_doi": m.get("doi"), "demoted_cites": m.get("cites"),
                                     "canonical_doi": canonical.get("doi"),
                                     "canonical_cites": canonical.get("cites"),
                                     "title": (m.get("matched_title") or "")[:80],
                                     "year": m.get("cr_year"), "container": m.get("container"),
                                     "src": m.get("src")})
        scored = [r for r in scored if id(r) not in demoted_ids]

    scored.sort(key=lambda r: (-r["score"], -r["jaccard"], is_reprint_venue(r.get("container")),
                               r.get("cr_year") or 9999, r.get("doi") or ""))
    best = scored[0]
    if dups_demoted:
        best["duplicates_demoted"] = dups_demoted
    if integrity:
        best["integrity_flag"] = integrity
    best["shadows_refused"] = [{"reason": r, "title": t, "doi": d}
                               for r, t, d in drops if r.startswith("shadow_record")]
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
    norm_selftest()             # accented surnames must fold, not shatter
    bookgate_selftest()          # refuses to run if the Wilson case stops firing
    failures = shadow_selftest()
    if failures:
        print("ABORT: shadow-gate self-test failed — the gate would under-refuse this whole run.",
              file=sys.stderr)
        for f in failures:
            print(f, file=sys.stderr)
        sys.exit(1)

    anchors, log = [], []
    n_verified = n_flagged = n_book = n_drift = n_review_rejected = 0
    n_shadow = n_integrity = n_dup = 0
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
        # Shadow bookkeeping runs on every candidate whether or not it resolved, because the shadow
        # is evidence about the anchor and not about the match.
        if r.get("shadows_refused"):
            rec["shadows_refused"] = r["shadows_refused"]
            n_shadow += len(r["shadows_refused"])
        if r.get("integrity_flag"):
            rec["integrity_flag"] = r["integrity_flag"]
            n_integrity += 1
        if r.get("duplicates_demoted"):
            rec["duplicates_demoted"] = r["duplicates_demoted"]
            n_dup += len(r["duplicates_demoted"])
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
    empirical = [a for a in anchors if a["provisional_cell"].startswith("PRIMARY_")]
    integrity_anchors = [a for a in anchors if a.get("integrity_flag")]

    L = [f"# A3 cold-start anchors — {SLUG} (D.3.c)", "",
         f"Sourced in a live OpenAlex pass (2026-08-18) and resolved through five gates: "
         f"{len(anchors)} candidate anchors, of which {len(empirical)} are empirical primary-cell "
         "anchors (the causal recall denominator) and the rest are link-support, mechanism, "
         "parameter, measurement, theory, or routing-decoy anchors that earn no empirical recall "
         "credit. No DOI is hand-asserted; each is the top-ranked version-of-record candidate from a "
         "unified Crossref + OpenAlex field, then re-affirmed at doi.org.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Expected index miss (no DOI by nature): {n_book}**", "",
         f"**Shadow records refused: {n_shadow}** across {len([a for a in anchors if a.get('shadows_refused')])} "
         f"anchors.  **Integrity flags raised: {n_integrity}.**", "",
         f"**Duplicate records demoted: {n_dup}** across "
         f"{len([a for a in anchors if a.get('duplicates_demoted')])} anchors. The duplicate gate is "
         "VALIDATED HERE — this run is its first confirmed catch. B.6 shipped it having never fired on a "
         "real case. Case & Deaton's *Deaths of Despair and the Future of Capitalism* is indexed as "
         "four distinct `book` records, all Princeton University Press eBooks, all authored Case & "
         "Deaton, citations split 1088/368/284/222; Kearney & Levine 2014 is indexed twice (98 and "
         "38 cites) under a Project MUSE and a Wisconsin DOI. Author agreement is present in every "
         "case, so the corrected rule — demotion requires positive author agreement, missing "
         "metadata never counts — demotes for the right reason. Each demotion names the copy kept, "
         "the copy set aside and both citation counts, so an RA can check the choice.", "",
         f"**Records refused as a review of the work, or on authorship: {n_review_rejected}.** Every "
         "refusal keeps its record in the JSON so the RA can audit what was refused rather than "
         "trusting that nothing was lost.", "",
         "## Coverage by estimand cell (verified / total)", ""]
    if OA_QUERY_ERRORS:
        i = L.index("## Coverage by estimand cell (verified / total)")
        note = [f"**OpenAlex refused {len(OA_QUERY_ERRORS)} title quer"
                f"{'y' if len(OA_QUERY_ERRORS) == 1 else 'ies'} outright** (wildcard characters in "
                "the search string). A refused query is UNCONFIRMED, never ABSENT; each is named so "
                "that no anchor is recorded as missing on the strength of a query the API declined "
                "to run.", ""]
        note += [f"- `{t}` — {e}" for t, e in OA_QUERY_ERRORS] + [""]
        L[i:i] = note
    for cell, vs in sorted(by_cell.items()):
        L.append(f"- `{cell}`: {sum(vs)}/{len(vs)}")
    L += ["", "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- {fam}: {sum(vs)}/{len(vs)}")
    if integrity_anchors:
        L += ["", "## Integrity flags — read before using these effect sizes", "",
              "Raised by the shadow gate, which noticed an Expression of Concern, retraction or "
              "correction record sitting on an anchor. These are facts about the work, carried "
              "forward to extraction and risk of bias rather than logged and forgotten.", ""]
        for a in integrity_anchors:
            for f in a["integrity_flag"]:
                L.append(f"- **{a['title'][:70]}** ({a['year']}) — {f['kind']}: "
                         f"*{(f.get('title') or '')[:80]}* ({f.get('year')}) `{f.get('doi')}`")
    L += ["", "## Per-candidate disposition", ""] + log
    L += ["", "## Notes", "",
          "- **Five gates, five distinct failures.** Existence catches ghosts — titles resolving to "
          "nothing. Version catches the mirror failure: a title resolving to a preprint, reprint or "
          "repository copy of the right work. Book-canon catches a real, correctly-titled, "
          "contemporaneous record of a *different* work: a review of the monograph — and it carries "
          "FOUR signals as of this run, not three. Shadow catches a separately-DOI'd record whose "
          "title is the target behind a named qualifier. Duplicate catches one work indexed twice "
          "with its citations split. Author agreement underwrites the last two. None substitutes for "
          "another.",
          "- **The book-canon gate needed a fourth signal, and this run is why.** Wilson 1996's "
          "citation argmax is `10.2307/3042249` — Daryl Michael Scott's review in *African American "
          "Review*, 3,641 cites, typed `article`, **with Wilson himself listed as an author**. It "
          "defeats the three inherited review signals (the title is the book's title exactly; the "
          "container is an ordinary journal whose name merely contains the word *Review*; the "
          "lead-name test needs a comma and this title has a colon) and then defeats `author_match`, "
          "which returns True and so *raises* its score. Author-list MEMBERSHIP is not a sufficient "
          "defence for a monograph; POSITION is. Signal 4 requires the record's first author to be "
          "one of the candidate's, and a self-test refuses to let the script run if it stops firing "
          "on Wilson or starts firing on the four legitimate Case & Deaton records.",
          "- **The duplicate-record gate is validated here.** It shipped from B.6 having never fired "
          "on a real case. Case & Deaton's book is indexed as four distinct `book` records, all "
          "Princeton UP eBooks, all authored Case & Deaton, citations split 1088/368/284/222; "
          "Kearney & Levine 2014 is indexed twice, at 98 and 38 cites. Author agreement holds in "
          "every case, so the corrected rule demotes for the right reason.",
          "- **`norm()` shattered accented surnames instead of folding them.** Replacing each "
          "non-ASCII character with a space turned Speder into `sp der` (surname `der`), Fahlen into "
          "`n`, Olah into `h`, Terzioglu into `lu`. The author gate then answered `authors_disagree` "
          "— a confident wrong negative rather than a missing-data None — and refused three anchors "
          "that had already resolved to exactly the right DOI, at Jaccard 1.00, in the right venue "
          "and the right year. The same function feeds the title gate, so accented TITLES were "
          "losing Jaccard as well. Blast radius across earlier chapters is measured in "
          f"`{SLUG}-anchor-norm-audit.md`, not assumed.",
          "- **A refused query is not an empty literature.** OpenAlex reads `?` and `*` in `search=` "
          "as wildcard operators and answers a title containing one with a 200 whose body is an "
          "error object; taking `.get(\"results\", [])` from it renders a REFUSAL as an absence. Ruhm "
          "2018, *Deaths of Despair or Drug Problems?*, was reported NO-MATCH through three retries "
          "while its NBER record sat indexed and live. Wildcards are stripped from the search string "
          "now, and an error body is recorded rather than emptied.",
          "- **Title fit is a score term, not only a gate.** The gate admits down to 0.45 so subtitle "
          "drift survives, after which records competed on type alone: a `book-chapter` of Case & "
          "Deaton's book, matching Ruhm's title at J=0.50, scored 22 and beat Ruhm's own NBER working "
          "paper at J=1.00, which scored 5. Working papers are the version of record for much of the "
          "economics this review draws on, and they are exactly what the type ranking distrusts.",
          "- **The author gate won an argument with the analyst.** The Wall 5 decoy was entered with "
          "its authors guessed as Dikmen and Terzioglu; the gate refused the correct DOI at Jaccard "
          "1.00 as `authors_disagree`, and the live record showed the authors to be Kaya and Oskay. "
          "The candidate was corrected from the record, not the gate relaxed. A gate that only ever "
          "confirms the analyst is not a gate.",
          "- **Three anchors resolve to no DOI at all, and that is the honest outcome.** Wilson 1996, "
          "Edin & Kefalas 2005 and Cherlin 2014 are monographs whose indexed records are reviews of "
          "themselves. They are kept, keyed on title, per A3's rule that a real work with an unusable "
          "identifier is never dropped from the denominator: dropping them would bias recall toward "
          "easy-to-find papers, and this chapter's canon is unusually monograph-heavy.",
          "- **The decoys carry the walls, not the topic.** Sobotka-Skirbekk-Philipov 2011, Hanappi "
          "et al. 2017 and Fahlen & Olah 2018 sit just across Wall 1 (C.5.a), and all three were "
          "surfaced by forward-citing the PRIMARY anchor — the citation-reason drift that makes the "
          "anomie channel drain into economic uncertainty. Kaya & Oskay 2019 sits across Wall 5 "
          "(reverse causation), Case & Deaton 2015 across Wall 4 (mortality outcome), "
          "Autor-Dorn-Hanson 2019 across Wall 10 (marriage-only outcome). Per the D.2.d finding they "
          "are forward-cited like any other seed at A4: a decoy's citation neighbourhood is where "
          "the boundary cases live.",
          "- **The AMERICAN primary cell has no anchor, and the gap is the point.** All three "
          "`PRIMARY_MEASURED_DESPAIR` anchors are post-communist (Bulgaria and Hungary). The "
          "reconnaissance found the treatment-mechanism-outcome intersection empty at n=12, none on "
          "topic, and six targeted title probes for an American despair-to-fertility study returned "
          "nothing. Recording the absence keeps it visible instead of letting a reduced-form decline "
          "study stand in for it. If A6 surfaces one, that is a genuine discovery.",
          "- **LEAKAGE WALL.** Sobotka, Skirbekk and Philipov 2011 and Balbo, Billari and Mills 2013 "
          "enter as channel-1 review seeds. Their search strategies must NOT be mined for A6 query "
          "terms, since their included studies feed anchors here.",
          "- **Empirical recall denominator.** Only the `PRIMARY_*` anchors count. The theory, "
          "phenomenon, exposure-series and routing-decoy anchors are indispensable to the chapter's "
          "demographic-significance computation and to its routing rules, and they are not evidence "
          "for the hypothesis.",
          ]

    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} year_drift={n_drift} flagged={n_flagged} no_doi={n_book} "
          f"shadows={n_shadow} integrity={n_integrity} review_or_author_refusals={n_review_rejected} "
          f"total={len(anchors)}")
    print("by cell:", {k: f"{sum(v)}/{len(v)}" for k, v in by_cell.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
