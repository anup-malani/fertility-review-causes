"""
201_c3g_cold_start_anchors.py — C.3.g (student debt and household formation), stage A3.

Inherits `187_a17_cold_start_anchors.py` in its machinery — resolver, ranking, and all five gates,
with the ASCII fold, the book-canon first-author signal, the corrected duplicate rule, the shadow
record gate, and the subtitle title-gate fix. Three things change.

ONE NEW GUARD, MEASURED BEFORE IT WAS GENERALISED. `200_c3g_chain_probe.py` found that an
APOSTROPHE-BEARING WORD corrupts an OpenAlex query. It does not refuse it — it answers, with the
wrong work ranked first, which is worse than a zero because every "did we find something" check
passes. The motivating case is this chapter's most-cited anchor: `search=` for *Can't afford a baby
Debt and young Americans* returns 8,633 records led by a paper on compulsive buying; drop the word
`Can't` and the correct work is rank 1 of 18,783. Stripping the apostrophe INSIDE the word
(`Cant`) is worse still — 0 on `title.search`.

The fix was then checked at the next order of magnitude rather than on the case that motivated it,
because a fix verified on its own motivating case is verified against nothing:

  | title | apostrophe word kept | word dropped |
  |---|---|---|
  | Can't afford a baby (contraction) | wrong work rank 1 | **correct, rank 1** |
  | ... a Child's College Education (possessive) | wrong work rank 1 | **correct, rank 1** |
  | ... Young People's Housing Tenure (possessive) | correct, rank 1 | correct, rank 1 |

Dropping is decisive twice and harmless once, across both apostrophe types, so `oa_search_safe()`
now drops the whole token. Guarded by `apostrophe_selftest()`. Six anchors in this set carry an
apostrophe, an interrogative, or both, so the guard is exercised by the run rather than asserted.

ONE INHERITED DEFECT FIXED. A.17's A3 log opens with "23 candidate anchors, of which **0** are
empirical primary-cell anchors" — which is false; it had twelve. The count tests
`provisional_cell.startswith("PRIMARY_")`, a naming convention no chapter has used since the cells
were renamed `P1_`, `P2_`, ... The gate did not fail, it DISENGAGED, and the surrounding counters
looked healthy. `PRIMARY_CELLS` is now an explicit set, and the log states which cells it counts.

WHY THE ANCHOR SET LOOKS THE WAY IT DOES. The scope found that C.3.g's identified variation and its
registered outcome are in different literatures: debt x fertility is 107 records with an identified
subset of 2 (neither an estimate), while the 210-record identified body sits on marriage,
homeownership and parental co-residence. Because v5's claim names those outcomes as the mechanism,
the chapter runs two arms that must not be pooled — a DIRECT arm (P1, P6) that is small and
associational and is what GRADE attaches to, and a CHAIN arm (P3, P4) that is identified on link 1
only, with link 2 borrowed from A.7 / A.23 / C.2.c. The anchor set holds that split open. A reviewer
who counts 24 anchors and concludes the evidence base is healthy has counted two literatures
answering different questions, one of which does not answer this chapter's.

AUTHORSHIP PROVENANCE, STATED BECAUSE IT BEARS ON WHAT THE AUTHOR GATE PROVES. Candidate authorship
was sourced from CROSSREF on 2026-08-26, not from RA memory and not from OpenAlex. Taking it from
OpenAlex would make the gate compare a record against itself, since the resolver ranks a unified
Crossref + OpenAlex field. Crossref sourcing is a CROSS-INDEX consistency check — weaker than
independent bibliographic knowledge, stronger than circular — and it is recorded per anchor as
`provenance_channel="crossref_author_sourced"`. It already earned its keep: it corrected two
attributions this RA had wrong, assigning *Returning to the Nest* to Dettling & Hsu (not Bleemer et
al.) and *A Day Late and a Dollar Short* to Goodman, Isen & Yannelis.

GATE CASES, RECORDED IN ADVANCE SO THE RUN IS A TEST AND NOT A DEMONSTRATION:

  * APOSTROPHE CASES, six, live: Nau et al. (contraction, the motivating case), de Gayardon et al.
    (possessive AND interrogative), Walsemann et al. (possessive), plus three interrogatives. A
    NO-MATCH on Nau et al. means `apostrophe_selftest` passed and the guard still regressed.
  * WILDCARD CASES, six, live: Bozick & Estacion, Gicheva, Houle & Warner, Looney & Yannelis,
    de Gayardon et al. and Martins & Villanueva all end in or contain `?`. A non-empty
    `OA_QUERY_ERRORS` for any of them means `oa_search_safe()` has regressed on the older half of
    its job.
  * NEAR-TITLE COLLISION, predicted. *Student Loans and Homeownership* (Mezza, Ringo, Sherlund and
    Sommer, JOLE) shares its title with *Student Loans and Homeownership TRENDS* (Sommer, Sherlund
    and Mezza, FEDS Notes 2014) — overlapping authors, one extra token, different work. Crossref's
    top hit for the candidate title is the FEDS Note. NOTE WHAT THE TITLE GATE CAN AND CANNOT DO
    HERE: it ADMITS the Note at J=0.80, because a four-token title admits every five-token superset
    of itself. That is the short-title instability, not a regression — 0.80 clears the ORDINARY 0.72
    floor and the subtitle fix plays no part. Separation must come from the year and
    version-of-record gates, and the log reports which fired. A run that anchors the FEDS Note has
    put a policy brief in place of the chapter's best-identified estimate.
  * VERSION-OF-RECORD CASE, live. *Constrained after college* is carried at its 2011 JPubE year;
    Crossref's top hit is the 2007 NBER report of the same title. This is the case the
    version-of-record gate exists for, and it has never been graded on a working-paper/article pair
    in this series.
  * SERIAL-TITLE CASE, expected to FAIL and carried for what the failure shows. The SCF bulletin is
    the exposure series the demographic-significance stage needs, and it cannot be anchored as a
    work: Crossref returns the 2019-2022 edition for a 2010-2013 query, with an EMPTY author list,
    because it is a drifting-title serial. `expect_no_doi=True`. This is the evidence for the
    retrieval risk the scope flagged, not an anchor.
  * CROSSREF MISS, live. *Graduate indebtedness* — the only review-shaped record in the entire
    394-record frame — does not resolve in Crossref, which returns a different work by a different
    author. Carried with its Crossref-returned authorship deliberately left WRONG so the author gate
    is given something to refuse. A VERIFIED here is a finding about the gate.
  * NEGATIVE CONTROL. *Student loan forgiveness and the timing of first births*, authors
    ["Anonymous"], `expect_no_doi=True`. It should NOT resolve — `200_` measured the entire
    policy-variation-with-a-fertility-outcome cell as empty, so this plausible title names a study
    that does not exist. A resolution here is a finding about the resolver's willingness to attach a
    DOI to a well-formed title, and it would also undercut the scope's central empty-cell result.

Standing discipline, unchanged from the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel). They
    assert NO DOIs; the DOI is whatever the resolver returns for a ranked match. Citation counts in
    the notes are observations from `199_`/`200_`, recorded so the run can be checked, never fed to
    the resolver.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached.
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication.

SCRIPT NUMBERING: 198 was the highest in use on ANY branch, local or remote, when this chain opened
(`main` would have said 88 and collided with nine live branches). 199 and 200 are this chapter's
probes. This is 201.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, sys, time, unicodedata
from urllib.parse import quote

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c3g_crossref_cache.json")
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


# --- Candidate anchors. Live-sourced 2026-08-25 via 185_ and 186_. NO DOIs asserted here. ---
# Cells that count toward EMPIRICAL primary-cell recall. Explicit, because a prefix convention
# changed under A.17's feet and its log reported zero while carrying twelve.
# P1 and P6 only: the DIRECT arm is what the chapter's claim is about. P3 and P4 are the chain arm —
# identified, better evidence, and evidence for a DIFFERENT proposition. Counting them here would
# reproduce at the anchor stage exactly the conflation the scope exists to prevent.
PRIMARY_CELLS = {"P1_DEBT_FERTILITY", "P6_INTENTIONS"}

CANDIDATES = [
    # ============================================================================================
    # DIRECT ARM (P1, P6) — the claim's own estimand: a young adult's own education debt against a
    # fertility outcome. Small, associational, and the set GRADE attaches to. Every one of these was
    # hand-anchored from `199_`; none would be recoverable from the identified-body vocabulary,
    # because none of them is identified.
    # ============================================================================================
    dict(title="Can't afford a baby? Debt and young Americans",
         authors=["Michael Nau", "Rachel E. Dwyer", "Randy Hodson"], year=2015,
         family="debt-fertility-direct", provisional_cell="P1_DEBT_FERTILITY",
         provenance_channel="crossref_author_sourced",
         note="Research in Social Stratification and Mobility, 93 cites. The most-cited work in the "
              "primary cell and the chapter's central associational estimate. APOSTROPHE CASE, and "
              "the one that motivated the guard: with `Can't` in the query the correct work is not "
              "rank 1 of 8,633; without it, rank 1 of 18,783. ALSO a wildcard case — the title "
              "carries a '?'. If this anchor comes back NO-MATCH the guard has regressed and the "
              "self-test did not catch it."),
    dict(title="Racial and Ethnic Variation in the Relationship Between Student Loan Debt and the "
               "Transition to First Birth",
         authors=["Stella Min", "Miles G. Taylor"], year=2018,
         family="debt-fertility-direct", provisional_cell="P1_DEBT_FERTILITY",
         provenance_channel="crossref_author_sourced",
         note="Demography, 31 cites. The only primary-cell work in a top demography journal, and "
              "the only one carrying a hazard model on a national panel. Its heterogeneity finding "
              "is why the chapter cannot report a single pooled coefficient even within arm 1."),
    dict(title="Student loan debt and family formation of youth in Japan",
         authors=["Jie Wang", "Hideo Akabayashi", "Masayuki Kobayashi", "Shinpei Sano"], year=2024,
         family="debt-fertility-direct", provisional_cell="P1_DEBT_FERTILITY",
         provenance_channel="crossref_author_sourced",
         note="Studies in Higher Education, 3 cites. The ONLY non-Anglophone primary-cell study in "
              "the frame (JASSO loans). Carries PI call 4 on its own: if the chapter rates a US "
              "parameter, this is the external-validity check, and it is a single study."),

    dict(title="Social Norms and Expectations about Student Loans and Family Formation",
         authors=["Arielle Kuperberg", "Joan Maya Mazelis"], year=2021,
         family="debt-fertility-direct", provisional_cell="P6_INTENTIONS",
         provenance_channel="crossref_author_sourced",
         note="Sociological Inquiry, 15 cites. Stated expectations, not realized fertility. Kept in "
              "its own cell on the D.3.b precedent, where folding intentions into realized outcomes "
              "is what made the pool incoherent."),
    dict(title="Parents, Partners, Plans, and Promises: The Relational Work of Student Loan "
               "Borrowing",
         authors=["Abby Stivers", "Elizabeth Popp Berman"], year=2020,
         family="debt-fertility-direct", provisional_cell="P6_INTENTIONS",
         provenance_channel="crossref_author_sourced",
         note="Socius, 19 cites. Qualitative/relational; anchored for the mechanism, not for an "
              "effect size. COMMA-DRIFT CASE: Crossref indexes it without the Oxford comma "
              "('Plans and Promises'), OpenAlex with it, so the two indexes disagree by one token."),

    # ============================================================================================
    # CHAIN ARM, LINK 1 — MARRIAGE AND UNION FORMATION (P3). Identified, and answering a different
    # question from the one the chapter rates. In scope because v5's claim names the outcome; NOT
    # counted toward empirical primary-cell recall, and never pooled with the direct arm.
    # ============================================================================================
    dict(title="Debt, Cohabitation, and Marriage in Young Adulthood",
         authors=["Fenaba R. Addo"], year=2014,
         family="debt-union-link1", provisional_cell="P3_MARRIAGE",
         provenance_channel="crossref_author_sourced",
         note="Demography, 193 cites — the most-cited work anywhere in this chapter's frame. Note "
              "what it is: it estimates debt against UNION FORMATION, not births. A reader who sees "
              "the citation count and infers a well-evidenced fertility literature has been misled "
              "by the frame, which is why it is anchored in the chain arm."),
    dict(title="Do student loans delay marriage? Debt repayment and family formation in young "
               "adulthood",
         authors=["Robert Bozick", "Angela Estacion"], year=2014,
         family="debt-union-link1", provisional_cell="P3_MARRIAGE",
         provenance_channel="crossref_author_sourced",
         note="Demographic Research, 61 cites. WILDCARD CASE: interrogative title."),
    dict(title="Student loans or marriage? A look at the highly educated",
         authors=["Dora Gicheva"], year=2016,
         family="debt-union-link1", provisional_cell="P3_MARRIAGE",
         provenance_channel="crossref_author_sourced",
         note="Economics of Education Review, 86 cites. The identified end of link 1. WILDCARD "
              "CASE. Also a SHADOW-RECORD risk: an earlier working paper circulates under the "
              "title 'In Debt and Alone? Examining the Causal Link between Student Loans and "
              "Marriage', which `199_` returned separately at 17 cites."),

    # ============================================================================================
    # CHAIN ARM, LINK 1 — HOUSING AND RESIDENTIAL INDEPENDENCE (P4). The densest identified cell in
    # the chapter, and the furthest from its outcome.
    # ============================================================================================
    dict(title="Student Loans and Homeownership",
         authors=["Alvaro Mezza", "Daniel Ringo", "Shane Sherlund", "Kamila Sommer"], year=2019,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="Journal of Labor Economics, 113 cites. The best-identified study in the chapter: "
              "linked credit-bureau panel with tuition-driven variation. NEAR-TITLE COLLISION, "
              "predicted: Crossref's top hit for this title is 'Student Loans and Homeownership "
              "TRENDS' (FEDS Notes 2014, Sommer/Sherlund/Mezza) — one extra token, three shared "
              "authors, a different work. The title gate CANNOT refuse it (J=0.80 clears the "
              "0.72 floor); the year and version-of-record gates have to."),
    dict(title="On the Effect of Student Loans on Access to Homeownership",
         authors=["Alvaro Mezza", "Daniel Ringo", "Kamila Sommer", "Shane Sherlund"], year=2016,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="FEDS working paper, 21 cites, with a duplicate conference record at 18 (`199_` "
              "returned both). DUPLICATE-RECORD CASE: same title, near years, agreeing author sets "
              "— the corrected rule should demote one. Also the working version of the JOLE paper "
              "above, so the VERSION-OF-RECORD gate has a live pair to separate."),
    dict(title="Into the Red and Back to the Nest? Student Debt, College Completion, and Returning "
               "to the Parental Home",
         authors=["Jason N. Houle", "Cody Warner"], year=2017,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="Sociology of Education, 109 cites. The A.23 boundary in one record: the outcome is "
              "returning to the parental home. WILDCARD CASE."),
    dict(title="Returning to the Nest: Debt and Parental Co-Residence Among Young Adults",
         authors=["Lisa J. Dettling", "Joanne W. Hsu"], year=2014,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="Labour Economics (2018) / FEDS 2014, 90 cites. ATTRIBUTION CORRECTION: this RA had "
              "it as Bleemer et al., who wrote the adjacent 'Debt, Jobs, or Housing'. Crossref "
              "sourcing caught it before it reached the chapter — which is the argument for not "
              "writing an anchor set from memory. VERSION CASE: FEDS working paper vs the journal "
              "article, four years apart, so a year-drift keep is the expected good outcome."),
    dict(title="A Day Late and a Dollar Short: Liquidity and Household Formation among Student "
               "Borrowers",
         authors=["Sarena Goodman", "Adam Isen", "Constantine Yannelis"], year=2021,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="Journal of Financial Economics, 60 cites (FEDS version 17). The cleanest liquidity "
              "test in the chapter and the one that speaks most directly to the mechanism v5 "
              "names, since it separates the repayment BURDEN from the debt STOCK."),
    dict(title="Does Student Loan Debt Structure Young People's Housing Tenure? Evidence from "
               "England",
         authors=["Ariane de Gayardon", "Claire Callender", "Stephen L. DesJardins"], year=2021,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="Journal of Social Policy, 14 cites. The English income-contingent regime, which is a "
              "different constraint from a fixed obligation and therefore tests PI call 4's premise "
              "rather than just its geography. DOUBLE GATE CASE: possessive apostrophe AND "
              "interrogative. Crossref returns the author names in ALL CAPS, which the fold must "
              "survive."),
    dict(title="Student Loan Debt, Educational Attainment, and Tenure Choice",
         authors=["Joshua Miller", "Silda Nikaj"], year=2017,
         family="debt-housing-link1", provisional_cell="P4_HOUSING",
         provenance_channel="crossref_author_sourced",
         note="Education Economics / SSRN, 7 cites. Anchored because it is the rare record that "
              "names the attainment-conditioning problem IN ITS TITLE — the confound the scope "
              "declared unenforceable at screen and routed to full-text extraction."),

    # ============================================================================================
    # MECHANISM / OFF-OUTCOME (P5). The resource channel itself. Retained as mechanism evidence and
    # explicitly not as evidence for a fertility effect.
    # ============================================================================================
    dict(title="Constrained after college: Student loans and early-career occupational choices",
         authors=["Jesse Rothstein", "Cecilia Elena Rouse"], year=2011,
         family="debt-resource-mechanism", provisional_cell="P5_RESOURCE",
         provenance_channel="crossref_author_sourced",
         note="Journal of Public Economics, 457 cites — the most-cited identified study in the "
              "whole frame, and it estimates OCCUPATIONAL CHOICE. It establishes that debt binds "
              "on real decisions, which is the mechanism's first premise and not its conclusion. "
              "VERSION-OF-RECORD CASE, live: Crossref's top hit is the 2007 NBER report of the "
              "same title; the candidate is carried at the 2011 journal year."),

    # ============================================================================================
    # REVIEW, EXPOSURE SERIES, ROUTING DECOYS, NEGATIVE CONTROL. None earns empirical recall credit.
    # ============================================================================================
    dict(title="Graduate indebtedness: its perceived effects on behaviour and life choices",
         authors=["Lei Zhang"], year=2018,
         family="review", provisional_cell="REVIEW",
         provenance_channel="crossref_author_sourced_WRONG_ON_PURPOSE",
         note="The only review-shaped record in the 394-record frame (Birkbeck repository, 20 "
              "cites). CROSSREF MISS, live: Crossref does not have it and returns Lei Zhang's "
              "'Effects of College Educational Debt on Graduate School Attendance' instead. The "
              "authorship above is that WRONG record's, carried deliberately so the author gate is "
              "given something it must refuse. A VERIFIED here is a finding about the gate, not "
              "about the review. Channel 1 of the cold-start bootstrap is empty for this chapter, "
              "and this anchor is the evidence for that claim."),
    dict(title="Changes in U.S. Family Finances from 2010 to 2013: Evidence from the Survey of "
               "Consumer Finances",
         authors=["Board of Governors of the Federal Reserve System"], year=2014,
         family="exposure-series", provisional_cell="EXPOSURE_SERIES", expect_no_doi=True,
         provenance_channel="crossref_sourced_no_author_list",
         note="SERIAL-TITLE CASE, expected to fail and carried for what the failure shows. The SCF "
              "bulletin is the exposure series the demographic-significance stage needs, and it "
              "cannot be anchored as a work: a 2010-2013 query returns the 2019-2022 edition, with "
              "an EMPTY author list, because the title drifts by edition. This is the measured "
              "evidence for the scope's retrieval risk — the exposure series is institutional and "
              "must be hand-sourced and hand-cited, not resolved."),

    dict(title="Medical student debt and major life choices other than specialty",
         authors=["James Rohlfing", "Ryan Navarro", "Omar Z. Maniya", "Byron D. Hughes",
                  "Derek K. Rogalsky"], year=2014,
         family="routing-decoy", provisional_cell="OFF_CAREER_BOUNDARY",
         provenance_channel="crossref_author_sourced",
         note="Medical Education Online, 118 cites. Wall 1's BOUNDARY case, not its decoy: the "
              "sample is medical students and the topic is career, but it reports childbearing "
              "decisions, so the 'route by outcome, not by topic' rule admits it. Anchored so the "
              "screen is tested against the hard case rather than the easy one."),
    dict(title="A Crisis in Student Loans? How Changes in the Characteristics of Borrowers and in "
               "the Institutions They Attended Contributed to Rising Loan Defaults",
         authors=["Adam Looney", "Constantine Yannelis"], year=2015,
         family="routing-decoy", provisional_cell="OFF_WALL3_REPAYMENT",
         provenance_channel="crossref_author_sourced",
         note="Brookings Papers on Economic Activity, 280 cites. Wall 3 decoy — the 706-record "
              "default and repayment body, whose overlap with any fertility outcome is 3 records. "
              "Highly cited and highly off-estimand: exactly the shape that survives a relevance "
              "ranking. WILDCARD CASE."),
    dict(title="The Other Student Debt Crisis: How Borrowing to Pay for a Child's College "
               "Education Relates to Parents' Retirement Savings",
         authors=["Katrina M Walsemann", "Jennifer A Ailshire", "Caroline Sten Hartnett"], year=2019,
         family="routing-decoy", provisional_cell="OFF_WALL6_PARENT_HELD",
         provenance_channel="crossref_author_sourced",
         note="Journals of Gerontology Series B, 18 cites. Wall 6 decoy — the THIRD balance sheet. "
              "The debt is education debt and the borrower is a parent, so it cannot delay the "
              "borrower's own childbearing. DOUBLE APOSTROPHE CASE ('Child's', 'Parents'')."),
    dict(title="Impact of Tuition-Free Education Policy on Child Marriage and Early Childbearing",
         authors=["Pragya Bhuwania", "Kate Huh", "Jody Heymann"], year=2023,
         family="routing-decoy", provisional_cell="OFF_WALL7_LMIC",
         provenance_channel="crossref_author_sourced",
         note="Population and Development Review, 31 cites. Wall 7 decoy, and the most dangerous "
              "one in the set: it is a genuine quasi-experiment linking an education-financing "
              "policy to childbearing, which is the exact shape C.3.g's empty P2 cell is missing. "
              "It is a different exposure (a child's school fees), a different outcome (adolescent "
              "childbearing) and a different phenomenon (not SDT). Tagged SECONDARY_LMIC, not "
              "deleted. If the screen admits this to P2, the chapter reports a natural experiment "
              "it does not have."),
    dict(title="Does Limited Access to Mortgage Debt Explain Why Young Adults Live with Their "
               "Parents?",
         authors=["Nuno C. Martins", "Ernesto Villanueva"], year=2009,
         family="routing-decoy", provisional_cell="OFF_WALL2_GENERAL_DEBT",
         provenance_channel="crossref_author_sourced",
         note="Journal of the European Economic Association, 34 cites (SSRN version 72). Wall 2 "
              "decoy: right outcome, right age group, wrong liability — this is C.3.e/C.2.c's "
              "exposure. WILDCARD CASE. Also a live VERSION pair, SSRN 2006 vs JEEA 2009, whose "
              "titles differ by more than a year ('Limited Access' vs 'High Cost')."),

    dict(title="Student loan forgiveness and the timing of first births",
         authors=["Anonymous"], year=2021,
         family="negative-control", provisional_cell="NEGATIVE_CONTROL", expect_no_doi=True,
         provenance_channel="fabricated_negative_control",
         note="NEGATIVE CONTROL. A well-formed, entirely plausible title for the study this chapter "
              "would most like to have. `200_` measured the whole policy-variation-with-a-fertility-"
              "outcome cell as empty, so no such study exists. It must NOT resolve. A resolution "
              "would be a finding about the resolver AND would undercut the scope's central "
              "empty-cell result, so it is checked here rather than assumed."),
]


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
    # PUNCTUATION CLASSES, folded BEFORE the ASCII strip and DELETED rather than spaced. Added for
    # C.3.g, where this defect refused three anchors outright — including the chapter's most-cited
    # primary-cell work — at Jaccard 0.588-0.700, just under the 0.72 floor.
    #
    # The mechanism is an ASYMMETRY between the two sides of a comparison. An ASCII apostrophe
    # survives NFKD and is then turned into a SPACE by the [^a-z0-9 ] rule, splitting one token in
    # two; a curly apostrophe (U+2019) is non-ASCII, so `encode("ascii", "ignore")` DELETES it and
    # the token stays whole. Indexes store the curly form and a hand-written candidate carries the
    # straight one, so the same title normalises two different ways:
    #
    #     candidate "Can't afford a baby"  -> "can t afford a baby"   (5 tokens)
    #     index     "Can’t afford a baby"  -> "cant afford a baby"    (4 tokens)
    #
    # Jaccard 0.70, refused, reported as NO-MATCH — which reads as an absent work. The same split
    # hits every possessive ("Child's", "Young People's") and the dash class does it in the mirror
    # direction: an ASCII hyphen becomes a space while U+2010 is deleted, so "Tuition-Free" and
    # "Tuition‐Free" disagree by a token boundary.
    #
    # Apostrophes are deleted so both sides yield "cant"; dashes are mapped to a space so both
    # sides yield two words. Neither carries retrieval signal, and the choice matters only in that
    # it must be the SAME on both sides.
    s = _APOSTROPHE_CLASS.sub("", s)
    s = _DASH_CLASS.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


# U+0027 apostrophe, U+2018/U+2019 curly quotes, U+02BC modifier letter, U+00B4 acute accent used as
# an apostrophe, U+0060 backtick. All six occur in indexed titles.
_APOSTROPHE_CLASS = re.compile("[\u0027\u2018\u2019\u02bc\u00b4\u0060]")
# U+002D hyphen-minus, U+2010-U+2015 the dash block, U+2212 minus, U+00AD soft hyphen.
_DASH_CLASS = re.compile("[\u002d\u2010\u2011\u2012\u2013\u2014\u2015\u2212\u00ad]")


_NORM_SELFTEST = [("Zsolt Spéder", "speder"), ("Susanne Fahlén", "fahlen"), ("Lívia Sz. Oláh", "olah"),
                  ("Füsun Terzioğlu", "terzioglu"), ("Tomáš Sobotka", "sobotka"),
                  ("Øystein Kravdal", "kravdal"), ("Wolfgang Lutz", "lutz"),
                  # A.24's own names, added 2026-08-24. Every one of these is an author the resolver
                  # has to match on this chapter, and two of them (Hortaçsu, Petřı́ček) carry a
                  # DOTLESS i — a non-ASCII BASE letter, which NFKD does not decompose and which only
                  # _TRANSLIT recovers. A regression in that map is silent and produces confident
                  # wrong negatives, so it is made a start-up failure instead.
                  ("Gina Potârcă", "potarca"), ("Alı Hortaçsu", "hortacsu"),
                  ("V. Petřı́ček", "petricek"), ("Joakim Hellumbråten Kristensen", "kristensen"),
                  ("Øystein Vedaa", "vedaa"),
                  # A.17's own names, added 2026-08-25. Präg is the one that actually failed in
                  # 185_ — not the fold, but the URL: raw UTF-8 in a query string returned an
                  # unparseable body. It bucketed as an ERROR rather than a zero, which is the only
                  # reason it was visible. Karlström and Tydén exercise ordinary diacritics; Rémy
                  # Slama an acute; Tomáš Sobotka a caron.
                  ("Patrick Präg", "prag"), ("Peter Karlström", "karlstrom"),
                  ("Tanja Tydén", "tyden"), ("Rémy Slama", "slama")]


def norm_selftest():
    """Refuse to run if surname folding regresses. Each case is a real name from this literature."""
    bad = [(raw, want, norm(raw).split()[-1]) for raw, want in _NORM_SELFTEST
           if norm(raw).split()[-1] != want]
    if bad:
        sys.stderr.write("ABORT: norm() folding self-test failed:\n")
        for raw, want, got in bad:
            sys.stderr.write(f"  {raw!r} -> expected surname {want!r}, got {got!r}\n")
        sys.exit(1)


def punctuation_fold_selftest():
    """norm() must fold a title the SAME way from the ASCII side and the Unicode side.

    Separate from `norm_selftest`, which checks NAMES through `surnames()` and therefore compares
    only the last token. These are TITLE cases and have to be checked on the whole string, which is
    the level at which the defect bites: `toks()` -> `jaccard()` sees the whole title, and a single
    token boundary that disagrees between candidate and index costs enough Jaccard to cross the
    refusal floor. On C.3.g's first A3 run this refused three anchors at 0.588-0.700 against a floor
    of 0.72, one of them the chapter's most-cited primary-cell work, and every refusal was reported
    as NO-MATCH — which reads as an absent work rather than a normalisation defect."""
    pairs = [
        ("Can't afford a baby", "Can\u2019t afford a baby"),
        ("a Child's College Education", "a Child\u2019s College Education"),
        ("Young People's Housing Tenure", "Young People\u2019s Housing Tenure"),
        ("Tuition-Free Education Policy", "Tuition\u2010Free Education Policy"),
    ]
    bad = []
    for ascii_side, unicode_side in pairs:
        a, u = norm(ascii_side), norm(unicode_side)
        if a != u:
            bad.append(f"  {ascii_side!r} -> {a!r}   BUT   {unicode_side!r} -> {u!r}")
    # And the folded forms must be the ones we intend, not merely equal to each other: a fold that
    # deleted everything would pass the symmetry check above.
    expected = [("Can't afford a baby", "cant afford a baby"),
                ("a Child's College Education", "a childs college education"),
                ("Tuition-Free Education Policy", "tuition free education policy")]
    for raw, want in expected:
        got = norm(raw)
        if got != want:
            bad.append(f"  {raw!r} -> expected {want!r}, got {got!r}")
    if bad:
        sys.stderr.write("ABORT: punctuation fold self-test failed; titles would normalise "
                         "asymmetrically and correct anchors would be reported as NO-MATCH:\n")
        sys.stderr.write("\n".join(bad) + "\n")
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
    """A.24's flagged fix, applied here.

    The inherited gate consulted BOOK_TITLE_FLOOR only when `is_book`. That made subtitle truncation
    a book-specific concession, which it is not: indexes drop subtitles from journal articles too.
    A.24 met the failure twice in one run — *Online Dating: A Critical Analysis...* indexed as
    *Online Dating* (J=0.18) and Rosenfeld & Thomas 2012 indexed as *Searching for a Mate* (J=0.36,
    under the 0.45 ordinary floor) — and reported NO-MATCH, which reads as an absent literature.

    The fix: the lower floor governs whenever `title_prefix_match` holds, book or not. The floor is
    safe there for the same reason it is safe for books — a contiguous leading-token match is a much
    stronger signal than Jaccard, and the author gate and review-shape test still carry the
    discrimination. `min_tokens` is NOT lowered here; that half of A.24's recommendation would admit
    two-token stems and is left for the shared resolver with its own evidence.

    A.17 needs this: Sobotka et al. 2008 is *The Contribution of Assisted Reproduction to Completed
    Fertility: An Analysis of Danish Data*, exactly the shape that fails."""
    j = jaccard(cand_title, it_title)
    ov = overlap_coef(cand_title, it_title)
    prefix = title_prefix_match(cand_title, it_title)
    floor = BOOK_TITLE_FLOOR if (is_book or prefix) else TITLE_JACCARD_FLOOR
    ok = j >= TITLE_JACCARD_MIN or (prefix and j >= floor)
    return ok, round(j, 3), round(ov, 3)


def title_gate_selftest():
    """A loosened gate must not be able to pass unnoticed, so the fix carries its own controls.

    Case 1 is A.24's, which the inherited gate refused and this one must admit. Cases 2 and 3 are
    negative controls that must STILL be refused: a shared prefix is not a match when the candidate
    is a different work, and a low Jaccard with no prefix relation stays refused."""
    cases = [
        # (candidate, indexed, is_book, expected_ok, why)
        ("Searching for a Mate: The Rise of the Internet as a Social Intermediary",
         "Searching for a Mate", False, True,
         "A.24's case: index drops the subtitle on a journal article"),
        ("The Contribution of Assisted Reproduction to Completed Fertility: An Analysis of Danish Data",
         "The Contribution of Assisted Reproduction to Completed Fertility", False, True,
         "A.17's case: same shape, this chapter's anchor"),
        ("Infertility Insurance Mandates and Fertility",
         "Infertility Insurance Mandates and Multiple Births", False, False,
         "NEGATIVE CONTROL: shared four-token prefix, different work, different outcome — this is "
         "the Wall 3 routing decoy and admitting it would merge two chapters' estimands"),
        ("Assisted Reproductive Technology Surveillance - United States, 2013",
         "Perinatal outcome of singletons and twins after assisted conception", False, False,
         "NEGATIVE CONTROL: no prefix relation, low Jaccard"),
        ("Student Loans and Homeownership",
         "Student Loans and Homeownership Trends", False, True,
         "C.3.g STRUCTURAL LIMIT, recorded rather than patched. The JOLE article against the FEDS "
         "Note that adds one token and shares three of four authors. The title gate ADMITS it "
         "(J=0.80 > TITLE_JACCARD_MIN=0.72) and cannot do otherwise: a four-token title admits "
         "every five-token superset of itself. That is the short-title instability the workflow "
         "warns about, NOT a regression from the subtitle fix — 0.80 clears the ORDINARY floor. "
         "This expectation was first written False and the self-test refused the run, which is the "
         "guard working on the RA rather than on the code. Separation of the live pair is carried "
         "downstream by the year gate (2019 vs 2014, outside YEAR_TOL) and the version-of-record "
         "gate; the run log reports which one fired"),
    ]
    bad = []
    for cand, idx, isbk, want, why in cases:
        got, j, _ = _title_gate(cand, idx, is_book=isbk)
        if got != want:
            bad.append(f"  {cand[:52]!r} vs {idx[:52]!r}: expected ok={want}, got ok={got} (J={j}) — {why}")
    if bad:
        sys.stderr.write("ABORT: title-gate self-test failed; the subtitle fix has regressed:\n")
        sys.stderr.write("\n".join(bad) + "\n")
        sys.exit(1)


# Titles the OpenAlex query parser refused, kept so a refusal can never be read as an absence.
OA_QUERY_ERRORS = []


def oa_search_safe(title):
    """Make a title safe to send as an OpenAlex relevance-search string.

    TWO hazards, both of which answer 200 and neither of which looks like an error.

    (1) WILDCARDS. `?` and `*` are wildcard operators in `search=`. A title containing either is
    REJECTED, with a 200 whose body is
        {"error": "Invalid query parameters error.",
         "message": "Wildcards (* or ?) require exact (no-stem) search..."}
    which `.get("results", [])` renders as an empty field. Found on Ruhm 2018, "Deaths of Despair or
    Drug Problems?". Interrogative titles are common in economics and demography — six anchors in
    THIS set carry one — so it is not an edge case in this literature.

    (2) APOSTROPHES, added for C.3.g and measured in `200_c3g_chain_probe.py`. An apostrophe-bearing
    token does not get the query refused; it gets it ANSWERED WRONG. `search=` for *Can't afford a
    baby Debt and young Americans* returns 8,633 records led by an unrelated paper on compulsive
    buying. Drop the token and the correct work — 93 cites, the most-cited work in this chapter's
    primary cell — is rank 1. Stripping the apostrophe inside the token (`Cant`) is worse: 0 hits on
    `title.search`. So the whole token goes.

    The token is DROPPED rather than de-punctuated, and dropped for possessives as well as
    contractions: checked on three anchors across both forms, where dropping was decisive twice and
    harmless once (see the module docstring's table). Titles are short and the surrounding tokens
    carry the retrieval signal; `norm()` discards punctuation on both sides before any title
    comparison, so nothing downstream depends on the dropped token."""
    t = re.sub(r"[?*]", " ", title or "")
    t = " ".join(w for w in t.split() if not APOSTROPHE_RE.search(w))
    return re.sub(r"\s+", " ", t).strip()


# U+0027 apostrophe, U+2019 right single quote, U+02BC modifier letter apostrophe. Indexes are not
# consistent about which they store, and the failure is identical for all three.
APOSTROPHE_RE = re.compile("[\u0027\u2019\u02bc]")


def apostrophe_selftest():
    """A guard that silently stops firing is worse than no guard, so it carries its own controls.

    Case 1 is the motivating contraction. Cases 2 and 3 are possessives, the form the fix was
    GENERALISED to and therefore the form that has to be checked. Case 4 is a negative control: a
    title with no apostrophe must pass through byte-identical, or the guard is eating clean input."""
    cases = [
        ("Can't afford a baby? Debt and young Americans",
         "afford a baby Debt and young Americans"),
        ("The Other Student Debt Crisis: How Borrowing to Pay for a Child's College Education",
         "The Other Student Debt Crisis: How Borrowing to Pay for a College Education"),
        ("Does Student Loan Debt Structure Young People\u2019s Housing Tenure? Evidence from England",
         "Does Student Loan Debt Structure Young Housing Tenure Evidence from England"),
        ("Debt, Cohabitation, and Marriage in Young Adulthood",
         "Debt, Cohabitation, and Marriage in Young Adulthood"),
    ]
    bad = []
    for raw, want in cases:
        got = oa_search_safe(raw)
        if got != want:
            bad.append(f"  {raw[:54]!r}\n    expected {want!r}\n    got      {got!r}")
    if bad:
        sys.stderr.write("ABORT: apostrophe guard self-test failed; queries would return "
                         "confidently wrong rank-1 matches rather than errors:\n")
        sys.stderr.write("\n".join(bad) + "\n")
        sys.exit(1)


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
    key = f"A12NORM1::{title}::{year}::{is_book}::{'|'.join(cand.get('authors') or [])}"
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


# --------------------------------------------------------------------------------------------
# KEYED EXCEPTIONS — recovery for anchors the gates refuse for a reason that is about the INDEX
# rather than about the work. Applied only AFTER resolve() has refused, counted in their own bucket,
# and each carries a stated reason an RA can check in one click. The gates are NOT loosened: a gate
# that can be talked out of a refusal by the same run that triggered it is not a gate. Same shape as
# the book-canon gate's "author gate + fallback flag, both needed".
#
# Both entries were verified live at doi.org AND against both indexes on 2026-08-24 before being
# written here. Neither is a remembered DOI.
# --------------------------------------------------------------------------------------------
KEYED_EXCEPTIONS = {
    # EMPTY BY DESIGN. A.24's two entries were both about A.24's index records and neither applies
    # here. More importantly, one of them — the Finkel title-stem case — is exactly what the
    # `_title_gate` fix above now handles in the gate itself, so carrying it forward as a keyed
    # exception would hide whether the fix works. A keyed exception is a last resort with a stated
    # reason an RA can check in one click; it is not a place to park a defect the gate should own.
    # If this run produces a refusal that is about the INDEX rather than about the work, it gets an
    # entry here, verified live at doi.org first, and counted in its own bucket.
}


# Findings are written here AFTER the first run and the script is then re-run, so the log is
# regenerable rather than hand-edited. Empty on the first pass by design.
FINDINGS = [
    "- **THE RUN FOUND A DEFECT IN `norm()` THAT HAS BEEN REFUSING CORRECT ANCHORS IN EVERY "
    "CHAPTER THAT HAS USED THIS RESOLVER.** The first pass verified 17 of 24 and reported three "
    "NO-MATCHes at J=0.588-0.700 against a 0.72 floor: Nau et al. 2015 — the most-cited work in "
    "this chapter's primary cell — plus Walsemann et al. 2019 and Bhuwania et al. 2023. None was "
    "an absent work. `norm()` folds ASCII and Unicode punctuation ASYMMETRICALLY: an ASCII "
    "apostrophe survives NFKD and is then turned into a SPACE, splitting one token in two, while a "
    "curly apostrophe is non-ASCII and is DELETED, leaving the token whole. Indexes store the "
    "curly form; a hand-written candidate carries the straight one. So `Can't afford a baby` "
    "normalises to five tokens and `Can\u2019t afford a baby` to four, Jaccard 0.70, refused. The "
    "dash class does the same thing in the mirror direction, which is what refused the "
    "`Tuition-Free` / `Tuition\u2010Free` pair.",
    "- **The fix recovered all three and disturbed nothing else: 17 verified -> 20, with the other "
    "17 unchanged.** Both punctuation classes are now folded before the ASCII strip, apostrophes "
    "deleted and dashes spaced, and the choice is guarded by `punctuation_fold_selftest()`, which "
    "checks BOTH that the two sides agree and that they agree on the intended string — a fold that "
    "deleted everything would pass a symmetry check alone.",
    "- **The same punctuation broke two different stages with opposite symptoms, and fixing one "
    "would not have fixed the other.** In the QUERY (`200_`) an apostrophe token returns the wrong "
    "work ranked first out of 8,633. In the COMPARISON (this run) it refuses the correct work at "
    "J=0.70 and reports NO-MATCH. Had only the query half been fixed, the correct record would "
    "have been retrieved, ranked first, and then rejected — and the log would have read "
    "`NO-MATCH`, which is indistinguishable from an absent literature. Both halves are the same "
    "character and neither is visible without the other.",
    "- **Predictions 1 and 2 confirmed in production.** Nau et al. resolved at J=1.00 to "
    "10.1016/j.rssm.2015.05.003 with `auth=True`, and `OA_QUERY_ERRORS` is empty across six "
    "interrogative titles. The apostrophe guard and the older wildcard guard both held.",
    "- **Prediction 3 confirmed, and it matters WHICH gate did it.** The near-title collision "
    "resolved to the Journal of Labor Economics article (10.1086/704609), not the FEDS Note. The "
    "title gate ADMITTED the Note, exactly as recorded in advance — J=0.80 clears the 0.72 floor "
    "and a four-token title admits every five-token superset of itself — so the separation was "
    "carried by year and version-of-record, as predicted. A chapter that reads only the outcome "
    "would conclude the title gate is discriminating here. It is not.",
    "- **Prediction 4 confirmed, but the SAME gate went the other way on a second version pair, "
    "and Crossref sourcing is why.** *Constrained after college* resolved to the 2011 JPubE "
    "article over the 2007 NBER report. *Returning to the Nest* resolved to the FEDS WORKING PAPER "
    "(10.17016/feds.2014.80) rather than the Labour Economics article — because the candidate year "
    "was 2014, which is the year Crossref's top hit carries. **Sourcing candidate metadata from "
    "Crossref steers the resolver toward whichever version Crossref ranked first.** That is the "
    "price of the non-circularity bought in the docstring, it is worth paying, and it has to be "
    "recorded: the anchor points at the working paper and extraction must read the journal "
    "version.",
    "- **Prediction 8 NOT confirmed — the duplicate gate did not fire at all.** `duplicates_"
    "demoted` is 0. The conference duplicate of *On the Effect of Student Loans on Access to "
    "Homeownership* that `199_` returned never entered the top-20 field, so the gate was never "
    "shown its case. Recorded as untested rather than as passing, on the B.6 precedent where a "
    "gate passed for the wrong reason because the record it was built for was never in the field.",
    "- **All three predicted failures failed, and one failed narrowly enough to be worth stating.** "
    "The negative control was refused at best-J 0.455 with `authors_disagree` — no study named "
    "*Student loan forgiveness and the timing of first births* exists, which independently "
    "corroborates `200_`'s measurement that the whole policy-variation-with-a-fertility-outcome "
    "cell is empty. The SCF serial was refused with `none_reached_gate`, confirming that the "
    "exposure series must be hand-cited rather than anchored. And *Graduate indebtedness* was "
    "refused at J=0.769 — above the ordinary floor — purely by the author gate, on the "
    "deliberately-wrong Crossref authorship. Prediction 6 held: the gate was the only thing "
    "standing between a wrong attribution and a VERIFIED anchor.",
    "- **The empirical recall denominator is 5, not 24, and the inherited counter would have said "
    "0.** A.17's log still reports \"0 are empirical primary-cell anchors\" while carrying twelve, "
    "because the test was `startswith(\"PRIMARY_\")` against cells renamed `P1_`, `P2_` several "
    "chapters ago. It did not fail; it DISENGAGED, and every counter around it looked healthy. "
    "`PRIMARY_CELLS` is now an explicit set and the header names the cells it counts. Of the five, "
    "three are realized fertility and two are stated intentions, kept apart on the D.3.b "
    "precedent.",
    "- **The Wall 7 decoy verified, and it is the one to watch at screen.** Bhuwania et al. 2023 "
    "(*PDR*, 31 cites) is a genuine quasi-experiment linking an education-financing policy to "
    "childbearing — the exact shape of the study C.3.g's empty P2 cell does not have. Different "
    "exposure (a child's school fees), different outcome (adolescent childbearing), different "
    "phenomenon (not SDT). If the screen admits it to P2, the chapter will report a natural "
    "experiment it does not have.",
    "- **One year-drift keep, on a routing decoy.** Martins and Villanueva resolved at J=1.00 to "
    "the 2006 SSRN record against a 2009 candidate. Carried for RA confirmation rather than "
    "silently accepted; nothing downstream turns on it.",
]


def main():
    norm_selftest()             # accented surnames must fold, not shatter
    apostrophe_selftest()        # apostrophe tokens must be dropped, not de-punctuated
    punctuation_fold_selftest()  # ASCII and Unicode punctuation must fold identically
    title_gate_selftest()        # the subtitle fix, with its negative controls
    bookgate_selftest()          # refuses to run if the Wilson case stops firing
    failures = shadow_selftest()
    if failures:
        print("ABORT: shadow-gate self-test failed — the gate would under-refuse this whole run.",
              file=sys.stderr)
        for f in failures:
            print(f, file=sys.stderr)
        sys.exit(1)

    anchors, log = [], []
    n_verified = n_flagged = n_book = n_drift = n_review_rejected = n_keyed = 0
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

        # Keyed-exception recovery. Runs only on a refusal, never on a match, and is counted in its
        # own bucket so that "23 verified" never quietly becomes "25 verified".
        if not rec.get("identity_verified") and c["title"] in KEYED_EXCEPTIONS:
            ex = KEYED_EXCEPTIONS[c["title"]]
            existence = doi_exists(ex["doi"])
            if existence == "FOUND":
                rec.update(doi=ex["doi"], identity_source=f"https://doi.org/{ex['doi']}",
                           identity_verified=True, existence=existence,
                           gold_status="recovered_keyed_exception",
                           keyed_exception_reason=ex["reason"])
                n_keyed += 1
                if not c.get("expect_no_doi"):
                    n_flagged -= 1
                status = (f"RECOVERED-BY-KEYED-EXCEPTION  doi={ex['doi']}  "
                          f"(the gate refusal stands and is recorded: {status})")
            else:
                status = f"KEYED-EXCEPTION-{existence}  doi={ex['doi']}  ({status})"

        anchors.append(rec)
        log.append(f"- **{c['title'][:68]}** ({c['year']}, {c['family']}) -> {status}")
        time.sleep(0.35)

    json.dump(anchors, open(OUT_JSON, "w"), indent=2)
    by_family, by_cell = {}, {}
    for a in anchors:
        by_family.setdefault(a["query_cluster_family"], []).append(a["identity_verified"])
        by_cell.setdefault(a["provisional_cell"], []).append(a["identity_verified"])
    # Explicit set, not a name prefix. A.17's log reported "0 are empirical primary-cell anchors"
    # while carrying twelve, because this test was `startswith("PRIMARY_")` against cells that have
    # been named P1_, P2_, ... for several chapters: the check DISENGAGED rather than failing, and
    # every surrounding counter still looked healthy.
    empirical = [a for a in anchors if a["provisional_cell"] in PRIMARY_CELLS]
    integrity_anchors = [a for a in anchors if a.get("integrity_flag")]

    L = [f"# A3 cold-start anchors — {SLUG} (C.3.g)", "",
         f"Sourced live on 2026-08-26 (titles via `199_`/`200_`, authorship via Crossref) and resolved "
         f"through five gates: {len(anchors)} candidate anchors, of which {len(empirical)} are "
         "empirical primary-cell anchors (cells " + ", ".join(f"`{c}`" for c in sorted(PRIMARY_CELLS)) + " — the causal recall denominator) and the rest are "
         "chain-arm, mechanism, exposure-series, review, routing-decoy or negative-control anchors "
         "that earn no empirical recall credit. No DOI is hand-asserted; each is the top-ranked "
         "version-of-record candidate from a unified Crossref + OpenAlex field, then re-affirmed at "
         "doi.org. The two exceptions are keyed, reasoned and counted separately below.", "",
         "**READ THE CELL COUNTS AGAINST WHAT THEY ARE COUNTING.** C.3.g has two arms answering "
         "different questions, and this anchor set holds the split open rather than closing it. "
         "`P1_DEBT_FERTILITY` and `P6_INTENTIONS` are the DIRECT arm — a young adult's own debt "
         "against a fertility outcome. That is the chapter's registered estimand and the only thing "
         "GRADE attaches to, and it is five anchors, none of them identified. `P3_MARRIAGE` and "
         "`P4_HOUSING` are the CHAIN arm — ten anchors, better evidence, quasi-experimental, and "
         "answering a question one link upstream of the claim. The chain arm is in scope because "
         "v5's claim names marriage and homeownership as the mechanism; it is NOT the recall "
         "denominator, and a reader who counts 24 anchors and concludes the fertility evidence is "
         "healthy has counted the wrong literature. The most-cited anchor in this set, Addo 2014 at "
         "193 cites, does not estimate a birth. Neither does the second, Rothstein and Rouse at "
         "457.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Recovered by keyed exception: {n_keyed}**  ·  "
         f"**Year-drift keep (real, RA-confirm): {n_drift}**  ·  **Flagged for RA: {n_flagged}**  ·  "
         f"**Expected index miss (no DOI by nature): {n_book}**", "",
         f"**Shadow records refused: {n_shadow}** across "
         f"{len([a for a in anchors if a.get('shadows_refused')])} anchors.  "
         f"**Integrity flags raised: {n_integrity}.**  "
         f"**Duplicate records demoted: {n_dup}** across "
         f"{len([a for a in anchors if a.get('duplicates_demoted')])} anchors.", "",
         f"**Review-shape or author refusals: {n_review_rejected}.** No keyed exception was used in "
         "this run, and none should be: every refusal here is about the WORK or the CANDIDATE, not "
         "about the index. The review anchor's authorship was carried deliberately wrong; the "
         "negative control names a study that does not exist; the exposure series is a "
         "drifting-title serial. A keyed exception is for an index defect, and there was none to "
         "recover from.", "",
         "## Cell counts", "",
         "| Cell | Verified / total |", "|---|---|"] + \
        [f"| `{k}` | {sum(v)}/{len(v)} |" for k, v in sorted(by_cell.items())] + \
        ["",
         "## Resolution log", ""] + log + \
        ["",
         "## Predictions recorded before the run", "",
         "Written into the script before it was run, not into the report afterwards. A run that "
         "confirms them is a test; a run whose report explains what happened is a demonstration.",
         "",
         "1. **Apostrophe guard (retrieval half).** Six anchors carry an apostrophe, an "
         "interrogative, or both. `oa_search_safe()` now DROPS an apostrophe-bearing token rather "
         "than de-punctuating it, after the fix was checked on three titles across both apostrophe "
         "forms. A NO-MATCH on Nau et al. means the guard regressed and `apostrophe_selftest` "
         "failed to catch it.",
         "2. **Wildcard guard.** Six interrogative titles. A non-empty `OA_QUERY_ERRORS` for any of "
         "them means `oa_search_safe()` regressed on the older half of its job.",
         "3. **Near-title collision.** *Student Loans and Homeownership* (JOLE 2019) against "
         "*Student Loans and Homeownership Trends* (FEDS Notes 2014). The title gate CANNOT "
         "separate them — J=0.80 clears the 0.72 floor, and a four-token title admits every "
         "five-token superset of itself — so the year and version-of-record gates have to. "
         "Anchoring the FEDS Note puts a policy brief in place of the chapter's best-identified "
         "estimate.",
         "4. **Version-of-record.** *Constrained after college* is carried at its 2011 JPubE year "
         "while Crossref's top hit is the 2007 NBER report of the same title.",
         "5. **Serial-title case, expected to FAIL.** The SCF bulletin cannot be anchored as a "
         "work: a 2010-2013 query returns the 2019-2022 edition with an empty author list. The "
         "failure is the evidence for the scope's exposure-series retrieval risk.",
         "6. **Crossref miss.** *Graduate indebtedness*, the only review-shaped record in the "
         "394-record frame, is absent from Crossref, which returns a different author's work. Its "
         "authorship is carried deliberately WRONG so the author gate has something to refuse. A "
         "VERIFIED here is a finding about the gate.",
         "7. **Negative control.** *Student loan forgiveness and the timing of first births*, "
         "authors `Anonymous`, must NOT resolve. `200_` measured that entire cell as empty, so a "
         "resolution would undercut the scope's central result as well as indicting the resolver.",
         "8. **Duplicate-record gate.** *On the Effect of Student Loans on Access to Homeownership* "
         "has a FEDS record and a conference record, same title, agreeing authors. One should be "
         "demoted rather than admitted as a second anchor.", "",
         "## Findings", "",
         "*Written after reading the resolution log above, then re-run so the artifact regenerates.*",
         ""] + FINDINGS + [""]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} keyed={n_keyed} year_drift={n_drift} flagged={n_flagged} no_doi={n_book} "
          f"shadows={n_shadow} integrity={n_integrity} review_or_author_refusals={n_review_rejected} "
          f"total={len(anchors)}")
    print("by cell:", {k: f"{sum(v)}/{len(v)}" for k, v in by_cell.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
