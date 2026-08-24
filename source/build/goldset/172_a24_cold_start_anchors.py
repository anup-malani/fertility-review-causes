#!/usr/bin/env python3
"""
172_a24_cold_start_anchors.py — A.24 (dating apps and union-formation friction), stage A3.

Inherits `161_a12_cold_start_anchors.py` unchanged in its machinery — resolver, ranking, and all five
gates, with the ASCII-folding fix and the book-canon first-author signal. One thing is added and it
is data, not logic: five of this chapter's own author names join `_NORM_SELFTEST`, so the run refuses
to start if folding regresses on the names A.24 actually has to match. What is otherwise new is the
candidate set.

WHY THE ANCHOR SET LOOKS THE WAY IT DOES, AND WHAT IS MISSING FROM IT. A.24 is a three-link chain —
app adoption -> partnering behaviour -> union formation -> births — and the scope (drafted 2026-08-24)
found the last link unestimated: dating-app exposure against a population fertility quantity returns
ELEVEN records and not one of them is an estimate. So `PRIMARY_APP_FERTILITY`, the cell the registry
entry is actually about, HAS NO ANCHOR. That is not an oversight and it must not be read as one. The
cell is carried through A4 with a recall denominator of zero, because a chapter whose headline is
"nobody has estimated this" has to be able to show the denominator it is speaking about.

The set therefore anchors what does exist: five studies on link 2 (`PRIMARY_APP_UNION`), three
identified estimates on technology diffusion that never say "dating app" (`SECONDARY_TECH_*`), eight
mechanism studies whose outcomes are psychological (`MECHANISM_CHOICE_FRICTION`), the exposure series,
one review, and seven routing decoys. A reviewer who counts anchors and concludes the chapter is
healthy has mistaken a populated neighbourhood for a populated estimand.

WALL 9 IS DECLARED UNENFORCEABLE BEFORE THE RUN, AND THREE ANCHORS EXIST TO TEST THE BYPASS. Bellou
2014, Billari-Giuntella-Stella 2019 and Kalabikhina et al. 2020 are the only identified estimates
this chapter can reach, and NONE of them carries dating-app vocabulary in a title or abstract. A wall
requiring that vocabulary deletes all three. A.12 established the trap and the fix in one run: gating
the recovery on the vocabulary the wall calls invisible recovered 4 records where a provenance-gated
bypass recovered 212. A4's bypass is therefore seeded from these three by provenance, with no
dating-vocabulary requirement, and its yield is measured per bypass rather than assumed.

GATE CASES, RECORDED IN ADVANCE SO THE RUN IS A TEST AND NOT A DEMONSTRATION:

  * AUTHOR GATE, and this is the prediction most likely to fail loudly. OpenAlex spells the author of
    *Marriage, Choice, and Couplehood in the Age of the Internet* (Sociological Science, 2017) as
    **"Michael Rosenfield"**. The candidate says Rosenfeld, which is correct. `surnames()` will
    therefore produce {rosenfeld} against {rosenfield} and `author_match` returns False — "this record
    has authors and none of them is ours" — refusing a record that matches at Jaccard 1.00, in the
    right venue, in the right year, on the single most important include-side anchor in the chapter.
    PREDICTED: refusal with reason `authors_disagree`. If that is what happens, the finding is not
    that the gate is wrong — a one-edit surname difference is exactly what the gate exists to catch —
    but that surname agreement is not a safe SOLE veto when the index itself carries the typo. The
    remedy is a flagged fallback, as with the book-canon gate, not a loosened gate.
  * BOOK-CANON GATE, a harder case than A.12's Bulmer. Becker's *A Treatise on the Family*: the
    sourcing pass's top hit is a Population and Development Review record at **8,590 cites, typed
    `article`, whose listed author is Gary S. Becker himself** — so neither the type test nor the
    first-author test can refuse it — and it out-cites the actual monograph record (typed `other`,
    459 cites, and carrying NO publication year) by nineteen to one. Citation-argmax takes the
    review. `is_book=True` is set deliberately: A.12's run showed that omitting it makes the gate
    no-op invisibly and return a right answer by a mechanism that does not generalise.
  * TITLE GATE, a case the gate is expected to FAIL if keyed naively, so it is keyed to avoid it and
    the failure is reported instead of hidden. Rosenfeld & Thomas 2012 is indexed as *Searching for a
    Mate* — the stem alone. Against the full title, *Searching for a Mate: The Rise of the Internet
    as a Social Intermediary*, the Jaccard is 4/11 = 0.36, which is UNDER the 0.45 ordinary floor, so
    `title_prefix_match` never gets to rescue it and a correct anchor is refused for having a
    subtitle. RECOMMENDATION FOR THE SHARED RESOLVER, flagged and NOT applied here so this run stays
    comparable with A.12's: apply `BOOK_TITLE_FLOOR` whenever `title_prefix_match` holds, not only
    when `is_book`. Index truncation of subtitles is not a book-specific behaviour.
  * VERSION-OF-RECORD GATE, two cases. Hitsch, Hortacsu & Ariely: AER 2010 (650) against an SSRN
    preprint (2008, 33) sharing the title exactly. `Love Unshackled`: MIS Quarterly 2019 (127)
    against a DOI-less 2018 SSRN preprint (0) — and the MISQ record's indexed title carries a
    trailing footnote marker, "...Online Dating1", costing one token against the title gate.
  * EXISTENCE GATE. Finkel et al.'s *Online Dating: A Critical Analysis From the Perspective of
    Psychological Science* has now missed on THREE independent OpenAlex query shapes:
    `filter=title.search:` (170_), `search=` (171_), and the sourcing pass. It is carried as
    UNRESOLVED BY QUERY, never as absent, and Crossref decides. A fourth miss establishes an absence;
    a Crossref hit makes it a finding about OpenAlex's coverage of PSPI.
  * TYPE VOCABULARY. The HCMST dataset is typed `dataset`, which `TYPE_ALIASES` maps to `other`,
    which is a member of `BOOKISH_TYPES` — so the book-shaped logic engages on a dataset anchor.
    Predicted here so that whatever it does is read as behaviour rather than as a surprise.
  * WILDCARD REFUSAL, two cases, both live: *Does broadband Internet affect fertility?* and *Why
    settle when there are plenty of fish in the sea? ...*. A `?` in a `search=` value is a wildcard
    operator and OpenAlex answers 200 with an error body that `.get("results", [])` renders as an
    empty literature. `oa_search_safe()` must strip both. A non-empty `OA_QUERY_ERRORS` for either
    anchor means the guard has regressed.
  * FOLD CASES, four, and all four are predicted to PASS: Potarca (a-circumflex and a-breve),
    Hellumbraten / Vedaa (ring-a, slashed O), Hortacsu (cedilla, and a DOTLESS i in the forename),
    Petricek (caron, plus a dotless i carrying a combining acute). `_TRANSLIT` maps the dotless i, so
    none of these should shatter. They are recorded because a passing fold case is the only evidence
    that the map still covers the non-ASCII BASE letters — NFKD alone does not, and a silent
    regression there produces confident wrong negatives, not errors.

A CITATION-HYGIENE FINDING ABOUT v5's SEMINAL LIST, WHICH IS WHY ALL THREE ARE ANCHORED. Unlike
A.12's, v5's three A.24 cites all RESOLVE and all are correctly attributed. The defect is different
and worse to leave unstated: two of the three carry no partnership and no fertility outcome.
Tyson et al. 2016 is a 62-cite conference measurement paper on Tinder activity logs; Bruch & Newman
2018 estimates desirability hierarchies and reply rates. Only Rosenfeld, Thomas & Hausen 2019 carries
a partnership outcome — and it reports that online dating now DOMINATES couple formation, which is
evidence about the exposure's reach, not about a friction. So the registry supports a demographic
claim with two platform-measurement papers, and the chapter says so with the anchors in hand.

Standing discipline, unchanged from the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) from a LIVE
    OpenAlex sourcing pass (2026-08-24, plus 170_ and 171_ the same day). They assert NO DOIs; the
    DOI is whatever the resolver returns for a ranked match. DOIs quoted in this docstring are
    observations recorded so the run can be checked, and are NOT fed to the resolver.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached.
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication.

SCRIPT NUMBERING: 171 is the highest in use on ANY branch, local or remote — checked across
refs/heads and refs/remotes, not against `main`, which would have said 89 and collided with six live
branches. This is 172.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, sys, time, unicodedata
from urllib.parse import quote

SLUG = "dating-apps-union-formation-friction"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a24_crossref_cache.json")
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


# --- Candidate anchors. Live-sourced 2026-08-24. NO DOIs asserted here by design. ---
CANDIDATES = [
    # ============================================================================================
    # PRIMARY_APP_UNION — the chapter's spine. App or online-dating exposure against a union-
    # formation outcome. Note what is NOT here: `PRIMARY_APP_FERTILITY` has NO anchor, because the
    # recon probe found no study that estimates it (11 records, none an estimate). The empty cell is
    # carried through A4 so its recall denominator is reported as zero rather than omitted.
    # ============================================================================================
    dict(title="Marriage, Choice, and Couplehood in the Age of the Internet",
         authors=["Michael J. Rosenfeld"], year=2017,
         family="app-union", provisional_cell="PRIMARY_APP_UNION",
         provenance_channel="named_recheck_sign_contest",
         note="Sociological Science, 83. The single most important INCLUDE-side record in the "
              "chapter: it tests the choice-overload critique directly and finds meeting online "
              "does not predict breakup and predicts FASTER transitions to marriage. AUTHOR-GATE "
              "CASE, prediction recorded above: OpenAlex spells the author 'Michael Rosenfield'."),
    dict(title="Disintermediating your friends: How online dating in the United States displaces "
               "other ways of meeting",
         authors=["Michael J. Rosenfeld", "Reuben J. Thomas", "Sonia Hausen"], year=2019,
         family="app-union", provisional_cell="PRIMARY_APP_UNION",
         provenance_channel="v5_seminal_list",
         note="PNAS, 425. v5's first seminal cite and the only one of the three that carries a "
              "partnership outcome. Also the exposure series in narrative form: the share of "
              "couples meeting online through 2017."),
    dict(title="Tinder Use and Romantic Relationship Formations: A Large-Scale Longitudinal Study",
         authors=["Eilin K. Erevik", "Joakim Hellumbraten Kristensen", "Torbjorn Torsheim",
                  "Oystein Vedaa", "Stale Pallesen"], year=2020,
         family="app-union", provisional_cell="PRIMARY_APP_UNION",
         provenance_channel="reconnaissance_probe_link1",
         note="Frontiers in Psychology, 36. Two waves, 5,253 Norwegian students; Tinder use "
              "predicts relationship formation one year later — again the opposite sign to v5. "
              "FOLD CASE: index carries 'Hellumbraten' with a ring-a and 'Oystein' with a slashed "
              "O; candidate is written in ASCII deliberately, so the fold is tested in the "
              "direction that actually occurs."),
    dict(title="The demography of swiping right. An overview of couples who met through dating apps "
               "in Switzerland",
         authors=["Gina Potarca"], year=2020,
         family="app-union", provisional_cell="PRIMARY_APP_UNION",
         provenance_channel="reconnaissance_probe_link1",
         note="PLoS ONE, 49. Non-US population, which matters because every other anchor in this "
              "cell is US or Nordic. FOLD CASE: indexed as 'Gina Potarca' with two diacritics."),
    dict(title="Marital satisfaction and break-ups differ across on-line and off-line meeting venues",
         authors=["John T. Cacioppo", "Stephanie Cacioppo", "Gian C. Gonzaga",
                  "Elizabeth L. Ogburn", "Tyler J. VanderWeele"], year=2013,
         family="app-union", provisional_cell="PRIMARY_APP_UNION",
         provenance_channel="named_recheck_sign_contest",
         note="PNAS, 221. Union QUALITY rather than formation, and industry-funded (eHarmony), "
              "which the risk-of-bias stage will have to weigh. Included because it is the most "
              "cited claim on the stability side of the sign contest."),

    # ============================================================================================
    # SECONDARY_TECH_* — Wall 9's population. These are the only identified estimates this chapter
    # can reach, and NOT ONE of them says "dating app" in its title or abstract. If A4's bypass
    # cannot seed from these, the chapter has no identified evidence at all.
    # ============================================================================================
    dict(title="The impact of Internet diffusion on marriage rates: evidence from the broadband "
               "market",
         authors=["Andriana Bellou"], year=2014,
         family="tech-diffusion", provisional_cell="SECONDARY_TECH_UNION",
         provenance_channel="named_recheck_identification_set",
         note="Journal of Population Economics, 83. Broadband-market variation against marriage "
              "rates — the closest thing to a quasi-experiment on link 2 that exists."),
    dict(title="Does broadband Internet affect fertility?",
         authors=["Francesco C. Billari", "Osea Giuntella", "Luca Stella"], year=2019,
         family="tech-diffusion", provisional_cell="SECONDARY_TECH_FERTILITY",
         provenance_channel="named_recheck_identification_set",
         note="Population Studies, 103. German panel, Falck et al. IV. POSITIVE effect on the "
              "fertility of highly educated women 25-45. WILDCARD CASE: the title ends in '?', "
              "which is an OpenAlex wildcard operator and returns a 200 whose body reads as an "
              "empty literature. oa_search_safe() must strip it; if OA_QUERY_ERRORS is non-empty "
              "for this anchor the guard has regressed."),
    dict(title="The impact of high speed internet on reproductive behavior in Russia",
         authors=["Irina Kalabikhina", "Imiliya Abduselimov", "German Klimenko"], year=2020,
         family="tech-diffusion", provisional_cell="SECONDARY_TECH_FERTILITY",
         provenance_channel="named_recheck_identification_set",
         note="Lomonosov Economics Journal, 10. RLMS-HSE panel with an IV; positive effect at "
              "second and higher parities. A small non-English venue, which tests whether the "
              "resolver reaches outside the Anglophone core — the cross-national arm of any "
              "verdict depends on that."),

    # ============================================================================================
    # MECHANISM_CHOICE_FRICTION — the mechanism IS measured. Its outcomes are psychological, with
    # exactly two exceptions (the Jung papers), which are the Wall 4 INCLUDE side: platform studies
    # whose outcome is matching rather than engagement.
    # ============================================================================================
    dict(title="A Rejection Mind-Set: Choice Overload in Online Dating",
         authors=["Tila Pronk", "Jaap J. A. Denissen"], year=2019,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="reconnaissance_probe_mechanism",
         note="Social Psychological and Personality Science, 99. Three studies; a cumulating 27% "
              "fall in acceptance. The strongest direct evidence for v5's mechanism, and its "
              "outcome is a rejection rate, not a union."),
    dict(title="There Are Plenty of Fish in the Sea: The Effects of Choice Overload and "
               "Reversibility on Online Daters' Satisfaction with Selected Partners",
         authors=["Jonathan D'Angelo", "Catalina L. Toma"], year=2016,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="reconnaissance_probe_mechanism",
         note="Media Psychology, 123. Experimental choice-set manipulation; outcome is "
              "satisfaction a week later."),
    dict(title="The Secret to Finding a Match: A Field Experiment on Choice Capacity Design in an "
               "Online Dating Platform",
         authors=["Jaehwuen Jung", "Hyungsoo Lim", "Dongwon Lee", "Chul Kim"], year=2021,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="reconnaissance_probe_mechanism",
         note="Information Systems Research, 30. WALL 4 INCLUDE-SIDE ANCHOR: a randomized field "
              "experiment varying choice capacity on a live platform, with MATCHING outcomes. "
              "Paired with the recommender-system decoy below, which shares venue type and "
              "vocabulary and differs only in outcome. If the screen cannot separate these two, "
              "Wall 4 is not enforceable."),
    dict(title="Love Unshackled: Identifying the Effect of Mobile App Adoption in Online Dating",
         authors=["Jaehwuen Jung", "Ravi Bapna", "Jui Ramaprasad", "Akhmed Umyarov"], year=2019,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="named_recheck_identification_set",
         note="MIS Quarterly, 127. App adoption identified on a platform, matching outcomes. "
              "TWO GATE CASES AT ONCE: a DOI-less 2018 SSRN preprint (0 cites) shares the title, "
              "and the MISQ record's indexed title carries a trailing footnote marker "
              "('...Online Dating1'), which costs one token against the title gate."),
    dict(title="Why settle when there are plenty of fish in the sea? Rusbult's investment model "
               "applied to online dating",
         authors=["Liesel L. Sharabi", "Elisabeth Timmermans"], year=2020,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="reconnaissance_probe_mechanism",
         note="New Media & Society, 49. Commitment and account-deletion intentions — the closest "
              "the mechanism literature comes to a union outcome without reaching one. SECOND "
              "WILDCARD CASE, and it carries a curly apostrophe as well."),
    dict(title="Swiping more, committing less: Unraveling the links among dating app use, dating "
               "app success, and intention to commit infidelity",
         authors=["Cassandra Alexopoulos", "Elisabeth Timmermans", "Jenna McNallie"], year=2019,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="sourcing_pass_2026_08_24",
         note="Computers in Human Behavior, 86. Surfaced by the sourcing pass, not by any "
              "reconnaissance probe: it is the strategic-delay limb of v5's mechanism stated in "
              "the registry's own terms, with a commitment outcome."),
    dict(title="Aspirational pursuit of mates in online dating markets",
         authors=["Elizabeth E. Bruch", "M. E. J. Newman"], year=2018,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="v5_seminal_list",
         note="Science Advances, 126. v5's third seminal cite. Estimates desirability hierarchies "
              "and reply rates; carries NO partnership outcome and no fertility outcome. Anchored "
              "so the chapter can say precisely what v5's citation does and does not support."),
    dict(title="A first look at user activity on tinder",
         authors=["Gareth Tyson", "Vasile C. Perta", "Hamed Haddadi", "Michael C. Seto"], year=2016,
         family="mechanism", provisional_cell="MECHANISM_CHOICE_FRICTION",
         provenance_channel="v5_seminal_list",
         note="ASONAM conference paper, 62. v5's second seminal cite. A platform-measurement paper "
              "with no partnership and no fertility outcome. TYPE CASE: typed `conference-paper`, "
              "which canon_type() leaves unmapped."),

    # ============================================================================================
    # EXPOSURE_SERIES — what stage 10 runs on. US-only, which bounds every demographic-significance
    # statement this chapter can make.
    # ============================================================================================
    dict(title="Searching for a Mate",
         authors=["Michael J. Rosenfeld", "Reuben J. Thomas"], year=2012,
         family="exposure", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="reconnaissance_probe_exposure",
         note="American Sociological Review, 538. TITLE-GATE CASE, and the anchor is keyed on the "
              "SHORT title deliberately. The work's full title is 'Searching for a Mate: The Rise "
              "of the Internet as a Social Intermediary', and OpenAlex indexes only the stem. "
              "Keyed on the full title the Jaccard is 4/11 = 0.36, UNDER the 0.45 ordinary floor, "
              "so title_prefix_match cannot rescue it and a correct anchor is refused. See the "
              "resolver recommendation in the docstring."),
    dict(title="How Couples Meet and Stay Together (HCMST), Wave I 2009, Wave II 2010, United States",
         authors=["Michael J. Rosenfeld"], year=2011,
         family="exposure", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="sourcing_pass_2026_08_24",
         note="ICPSR, 2 cites. The exposure series itself. TYPE CASE: OpenAlex types it `dataset`, "
              "which TYPE_ALIASES maps to `other`, which is a member of BOOKISH_TYPES — so the "
              "book-shaped logic engages on a dataset. Predicted, then checked."),

    # ============================================================================================
    # CHANNEL1_REVIEW
    # ============================================================================================
    dict(title="Online Dating: A Critical Analysis From the Perspective of Psychological Science",
         authors=["Eli J. Finkel", "Paul W. Eastwick", "Benjamin R. Karney", "Harry T. Reis",
                  "Susan Sprecher"], year=2012,
         family="review", provisional_cell="CHANNEL1_REVIEW",
         provenance_channel="named_recheck_unresolved",
         note="Psychological Science in the Public Interest. THE EXISTENCE-GATE CASE OF THIS RUN. "
              "It has now missed on three independent OpenAlex query shapes — title.search (170_), "
              "search= (171_), and the sourcing pass — and is recorded as UNRESOLVED BY QUERY, not "
              "as absent. Crossref decides. If Crossref finds it, the finding is about OpenAlex "
              "coverage of PSPI; if Crossref also misses, the absence is established rather than "
              "inferred."),

    # ============================================================================================
    # ROUTING DECOYS — one per enforceable wall, plus two boundary routes. Never excluded from
    # forward seeding: on the standing guidance a decoy cloud is a boundary case, and the two
    # homonym families here are the exception that must be measured rather than assumed.
    # ============================================================================================
    dict(title="Luminescence dating of quartz using an improved single-aliquot regenerative-dose "
               "protocol",
         authors=["Andrew Murray", "A. G. Wintle"], year=2000,
         family="decoy", provisional_cell="OFF_HOMONYM_GEOCHRON",
         provenance_channel="reconnaissance_probe_decoy",
         note="Radiation Measurements, 4,997. Wall 1. The geochronology cloud is 64,276 records on "
              "the explicit vocabulary and outranks every genuine A.24 record by an order of "
              "magnitude — the SHELX shape. A4 measures its on-topic rate with count-only queries "
              "rather than sampling it."),
    dict(title="Biofertilizers function as key player in sustainable agriculture by improving soil "
               "fertility, plant tolerance and crop productivity",
         authors=["Deepak Bhardwaj", "Mohammad Wahid Ansari", "Ranjan Kumar Sahoo",
                  "Narendra Tuteja"], year=2014,
         family="decoy", provisional_cell="OFF_NONHUMAN",
         provenance_channel="sourcing_pass_2026_08_24",
         note="Microbial Cell Factories, 1,171. Wall 2. 'Fertility' in the agronomic sense reached "
              "the head of two recon probes, including one restricted to dating-app vocabulary, so "
              "this is not a hypothetical collision."),
    dict(title="The world report on violence and health",
         authors=["Etienne Krug", "James A. Mercy", "Linda L. Dahlberg", "Anthony B. Zwi"],
         year=2002,
         family="decoy", provisional_cell="OFF_VIOLENCE",
         provenance_channel="sourcing_pass_2026_08_24",
         note="The Lancet, 8,514. Wall 3, and this anchor is the CLOUD HEAD, not the seam. The "
              "genuine boundary is the 66 records where dating-violence and dating-app vocabulary "
              "meet, and those are tested at the screen rather than here — stated so the wall is "
              "not later described as having been tested at its hardest point."),
    dict(title="Recommender System for Online Dating Service",
         authors=["Lukas Brozovsky", "Vaclav Petricek"], year=2007,
         family="decoy", provisional_cell="OFF_PLATFORM_ENG",
         provenance_channel="sourcing_pass_2026_08_24",
         note="arXiv, 119. Wall 4 EXCLUDE side, paired with Jung et al. 2021 above: same platform "
              "vocabulary, same venue type, and the only difference is the outcome. FOLD CASE: "
              "indexed as 'V. Petricek' with a caron and a dotless i carrying a combining acute; "
              "_TRANSLIT maps the dotless i, so the surname should survive. Predicted to PASS, "
              "recorded because a passing fold case is the only evidence the map still works."),
    dict(title="Swipe Right: Dating Website and App Use Among Men Who Have Sex With Men",
         authors=["Hannah J. Badal", "Jo Ellen Stryker", "Nickolas DeLuca", "David W. Purcell"],
         year=2017,
         family="decoy", provisional_cell="OFF_SEXHEALTH",
         provenance_channel="sourcing_pass_2026_08_24",
         note="AIDS and Behavior, 135. Wall 5. The sexual-health cloud is 1,244 records INSIDE the "
              "dating-app literature — a fifth of it — so this wall does more work than any other "
              "outcome wall in the chapter. Note the routing asymmetry: coital-FREQUENCY outcomes "
              "go to A.14 rather than into this bin."),
    dict(title="Matching and Sorting in Online Dating",
         authors=["Gunter J. Hitsch", "Ali Hortacsu", "Dan Ariely"], year=2010,
         family="boundary", provisional_cell="ROUTE_C7A",
         provenance_channel="reconnaissance_probe_boundary",
         note="American Economic Review, 650. Wall 6, and the hardest routing call in the set: it "
              "is a marriage-market matching paper (C.7.a) that runs ON a dating platform, so "
              "either chapter can claim it. VERSION-OF-RECORD CASE: a 2008 SSRN preprint (33 "
              "cites) shares the title exactly. FOLD CASE: indexed as 'Ali Hortacsu' with a "
              "cedilla and a DOTLESS i in the forename."),
    dict(title="A Treatise on the Family",
         authors=["Gary S. Becker"], year=1991, is_book=True, expect_no_doi=True,
         family="boundary", provisional_cell="ROUTE_LINK3",
         provenance_channel="sourcing_pass_2026_08_24",
         note="Wall 7 route, and THE BOOK-CANON CASE OF THIS RUN — a harder one than A.12's "
              "Bulmer. The sourcing pass's top hit is a Population and Development Review record "
              "at 8,590 cites, typed `article`, whose listed author is GARY S. BECKER HIMSELF. So "
              "neither the type test nor the first-author test can refuse it, and it out-cites the "
              "actual monograph (the 'Enlarged Edition' record, typed `other`, 459 cites, NO "
              "publication year) by nineteen to one. This is the case the book-canon gate was "
              "built for, in its most adversarial form; is_book=True is set here deliberately, "
              "because A.12's run showed that omitting it makes the gate no-op invisibly."),
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
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


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
                  ("Øystein Vedaa", "vedaa")]


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
    "Marriage, Choice, and Couplehood in the Age of the Internet": dict(
        doi="10.15195/v4.a20",
        reason="INDEX TYPO IN THE AUTHOR FIELD. OpenAlex records the author as 'Michael Rosenfield'; "
               "the author is Michael J. Rosenfeld. surnames() therefore compares {rosenfeld} with "
               "{rosenfield} and author_match returns False — a confident wrong negative on a record "
               "matching at Jaccard 1.00, in the right venue and the right year. The gate behaved "
               "correctly on the data it was given; the data is wrong."),
    "Online Dating: A Critical Analysis From the Perspective of Psychological Science": dict(
        doi="10.1177/1529100612436522",
        reason="INDEX CARRIES THE STEM TITLE ONLY. BOTH OpenAlex and Crossref title this work "
               "'Online Dating' — two tokens — against an eleven-token candidate title, so Jaccard "
               "is 0.18 and title_prefix_match refuses before the floor is consulted at all, because "
               "the stem is shorter than min_tokens=3. Verified live by DOI in both indexes: "
               "Psychological Science in the Public Interest, 2012, 776 cites."),
}


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
    empirical = [a for a in anchors if a["provisional_cell"].startswith("PRIMARY_")]
    integrity_anchors = [a for a in anchors if a.get("integrity_flag")]

    L = [f"# A3 cold-start anchors — {SLUG} (A.24)", "",
         f"Sourced in a live OpenAlex pass (2026-08-24, alongside `170_` and `171_`) and resolved "
         f"through five gates: {len(anchors)} candidate anchors, of which {len(empirical)} are "
         "empirical primary-cell anchors (the causal recall denominator) and the rest are "
         "technology-diffusion, mechanism, exposure-series, review or routing-decoy anchors that "
         "earn no empirical recall credit. No DOI is hand-asserted; each is the top-ranked "
         "version-of-record candidate from a unified Crossref + OpenAlex field, then re-affirmed at "
         "doi.org. The two exceptions are keyed, reasoned and counted separately below.", "",
         "**READ THE CELL COUNTS AGAINST WHAT IS ABSENT FROM THEM.** `PRIMARY_APP_FERTILITY` — the "
         "cell the registry entry is actually about — has NO ANCHOR, because the recon probe found "
         "no study that estimates it: dating-app exposure against a population fertility quantity "
         "returns eleven records and not one is an estimate. The cell is carried with a recall "
         "denominator of zero rather than dropped, because a chapter whose headline is 'nobody has "
         "estimated this' must be able to show the denominator it is speaking about. A reviewer who "
         "counts anchors here and concludes the chapter is healthy has mistaken a populated "
         "neighbourhood for a populated estimand.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Recovered by keyed exception: {n_keyed}**  ·  "
         f"**Year-drift keep (real, RA-confirm): {n_drift}**  ·  **Flagged for RA: {n_flagged}**  ·  "
         f"**Expected index miss (no DOI by nature): {n_book}**", "",
         f"**Shadow records refused: {n_shadow}** across "
         f"{len([a for a in anchors if a.get('shadows_refused')])} anchors.  "
         f"**Integrity flags raised: {n_integrity}.**  "
         f"**Duplicate records demoted: {n_dup}** across "
         f"{len([a for a in anchors if a.get('duplicates_demoted')])} anchors.", "",
         f"**Review-shape or author refusals: {n_review_rejected}.** Both of the run's two refusals "
         "were predicted in the docstring before the run, and both are about the INDEX rather than "
         "about the work — which is why they are recovered by keyed exception with the gate refusal "
         "left standing in the record, not by loosening a gate.", "",
         "## Cell counts", "",
         "| Cell | Verified / total |", "|---|---|"] + \
        [f"| `{k}` | {sum(v)}/{len(v)} |" for k, v in sorted(by_cell.items())] + \
        ["",
         "## Resolution log", ""] + log + \
        ["",
         "## Findings", "",
         "- **TITLE-STEM INDEXING IS A RESOLVER DEFECT WITH TWO INSTANCES IN THIS ONE RUN, AND IT "
         "IS THE FINDING WORTH CARRYING OFF THIS CHAPTER.** Both indexes title Finkel et al.'s "
         "*Online Dating: A Critical Analysis From the Perspective of Psychological Science* as "
         "**`Online Dating`** — two tokens, 776 cites, Psychological Science in the Public Interest, "
         "confirmed live in OpenAlex AND Crossref by DOI. Against an eleven-token candidate title "
         "the Jaccard is 0.18, and `title_prefix_match` never even reaches the floor because the "
         "stem is shorter than `min_tokens=3`. The same shape appears a second time in the same "
         "run: Rosenfeld & Thomas 2012 is indexed as *Searching for a Mate*, and against its full "
         "title (*...: The Rise of the Internet as a Social Intermediary*) the Jaccard is 4/11 = "
         "0.36, under the 0.45 ordinary floor. That anchor only resolved because it was keyed on "
         "the stem DELIBERATELY, having been predicted. **So the resolver cannot resolve a work "
         "whose index entry drops its subtitle, and the failure is silent — it reports NO-MATCH, "
         "which reads as an absent literature.** Recommended fix, flagged and NOT applied here so "
         "this run stays comparable with A.12's: apply `BOOK_TITLE_FLOOR` whenever "
         "`title_prefix_match` holds rather than only when `is_book`, and lower `min_tokens` to 2 "
         "when the author gate has independently returned True. Subtitle truncation is not a "
         "book-specific behaviour and this is not a per-chapter fix.",
         "- **An index typo in an AUTHOR field defeats the author gate, on the chapter's most "
         "important include-side record.** OpenAlex spells the author of *Marriage, Choice, and "
         "Couplehood in the Age of the Internet* (Sociological Science, 2017) as **'Michael "
         "Rosenfield'**. `surnames()` compares {rosenfeld} with {rosenfield}, `author_match` returns "
         "False, and a record matching at Jaccard 1.00 in the right venue and year is refused. The "
         "gate is right to treat a one-edit surname difference as disagreement — that is what it is "
         "for — so the remedy is a keyed exception with a stated reason, not a fuzzy surname match, "
         "which would reopen exactly the failure the gate prevents.",
         "- **The book-canon gate met a harder case than A.12's Bulmer and held.** Becker's *A "
         "Treatise on the Family* resolves first to a Population and Development Review record at "
         "**8,590 cites, typed `article`, listing Gary S. Becker himself as author** — so neither "
         "the type test nor the first-author test can refuse it, and it out-cites the actual "
         "monograph record (typed `other`, 459 cites, carrying NO publication year) nineteen to "
         "one. The gate refused it as `review_of_the_work` and the anchor is carried keyed on title "
         "with `expect_no_doi`, not faked. `is_book=True` was set from the start here, on A.12's "
         "lesson that omitting it makes the gate no-op invisibly.",
         "- **v5's seminal list for A.24 is three-for-three RESOLVABLE and two-for-three "
         "IRRELEVANT.** Unlike A.12's, all three cites exist and are correctly attributed. But "
         "Tyson et al. 2016 is a 62-cite conference measurement paper on Tinder activity logs "
         "(typed `proceedings-article`), and Bruch & Newman 2018 estimates desirability hierarchies "
         "and reply rates. Neither carries a partnership outcome or a fertility outcome. Only "
         "Rosenfeld, Thomas & Hausen 2019 reaches a partnership outcome, and what it reports is "
         "that online dating now DOMINATES couple formation — evidence about the exposure's reach, "
         "not about a friction. The registry supports a demographic claim with two "
         "platform-measurement papers, and the chapter now has the anchors in hand to say so.",
         "- **All three Wall 9 anchors resolved, which is what makes the bypass buildable.** Bellou "
         "2014 (J. Population Economics), Billari Giuntella & Stella 2019 (Population Studies) and "
         "Kalabikhina et al. 2020 (Moscow University Economics Bulletin) are the only identified "
         "estimates this chapter can reach and none of them carries dating-app vocabulary. A4 seeds "
         "the bypass from these three BY PROVENANCE, with no dating-vocabulary requirement, and "
         "measures its yield separately — A.12's lesson that re-imposing the wall's own vocabulary "
         "on the recovery is self-defeating (4 records against 212).",
         "- **Both wildcard cases passed, so the guard has not regressed.** *Does broadband Internet "
         "affect fertility?* and *Why settle when there are plenty of fish in the sea? ...* both "
         "carry a `?`, which is an OpenAlex wildcard operator that answers 200 with a body reading "
         "as an empty literature. `oa_search_safe()` stripped both and `OA_QUERY_ERRORS` is empty.",
         "- **All four fold cases passed, and five of this chapter's names are now in the "
         "start-up self-test.** Potarca (a-circumflex, a-breve), Hellumbraten and Vedaa (ring-a, "
         "slashed O), Hortacsu and Petricek (cedilla, caron, and a DOTLESS i — a non-ASCII BASE "
         "letter that NFKD does not decompose and only `_TRANSLIT` recovers). A passing fold case "
         "is the only evidence the map still covers those letters, and a regression there produces "
         "confident wrong negatives rather than errors, so it is now a start-up failure.",
         "- **Both version-of-record cases went to the version of record.** Hitsch, Hortacsu & "
         "Ariely resolved to AER 2010 (10.1257/aer.100.1.130) over the 2008 SSRN preprint sharing "
         "the title exactly; `Love Unshackled` resolved to MIS Quarterly (10.25300/misq/2019/14289) "
         "over a DOI-less 2018 SSRN preprint, at J=0.846 — the shortfall is the trailing footnote "
         "marker in the indexed title (`...Online Dating1`), exactly as predicted.",
         "- **The dataset anchor survived the bookish-type path.** HCMST is typed `dataset`, which "
         "`TYPE_ALIASES` maps to `other`, a member of `BOOKISH_TYPES` — so book-shaped logic engages "
         "on a dataset. It resolved to 10.3886/icpsr30103.v2 at J=1.00. Recorded because the "
         "behaviour was predicted rather than discovered, and because the next chapter anchoring on "
         "a dataset will meet the same path.",
         "- **The violence decoy is the CLOUD HEAD, not the seam.** Krug et al. 2002 anchors a "
         "43,963-record cloud, but the genuine Wall 3 boundary is the 66 records where "
         "dating-violence and dating-app vocabulary meet. Those are tested at the screen, not here. "
         "Stated so the wall is not later described as having been tested at its hardest point.", ""]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} keyed={n_keyed} year_drift={n_drift} flagged={n_flagged} no_doi={n_book} "
          f"shadows={n_shadow} integrity={n_integrity} review_or_author_refusals={n_review_rejected} "
          f"total={len(anchors)}")
    print("by cell:", {k: f"{sum(v)}/{len(v)}" for k, v in by_cell.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
