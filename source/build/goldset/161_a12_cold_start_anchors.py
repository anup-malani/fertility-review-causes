#!/usr/bin/env python3
"""
161_a12_cold_start_anchors.py — A.12 (twinning rates and multiple births), stage A3.

Inherits `148_d3c_cold_start_anchors.py` unchanged in its machinery — resolver, ranking, and all five
gates, with the norm() ASCII-folding fix and the book-canon first-author signal. Nothing in the gate
logic is modified here. What is new is the candidate set, and A.12 turns out to be the chapter that
exercises the inherited gates hardest: every one of the five fires on a real case, and two of them
fire on cases stronger than the ones they were written against.

WHY THE ANCHOR SET LOOKS THE WAY IT DOES. A.12 is an accounting identity with a behavioral offset
(scope doc, frozen 2026-08-22). The mechanical arm is arithmetic and no study estimates it, so the
`PRIMARY_*` cells here are NOT the bulk of the set: they are three named studies of the stopping
offset, plus the twin-IV canon whose first stages estimate the same parameter as a nuisance. The
large remainder is `EXPOSURE_SERIES` and `SECONDARY_*` — vital-statistics compilations and twinning-
rate series that feed the stage-10 computation and are not evidence for the hypothesis. A reviewer
who counts anchors and concludes the chapter is thin has mistaken an identity for a hypothesis.

WALL 6 WAS RE-CUT BEFORE THIS RUN, AND THE ANCHOR SET TESTS THE RE-CUT. PI Call 3 was decided
"split at the margin": A.17 owns ART deliveries, A.12 owns only the multiplier. That ruling made the
drafted Wall 6 self-defeating — it hard-excluded transfer-protocol studies, which are the only
quasi-experimental variation in the multiplier that exists. Wall 6 now cuts on OUTCOME. Three anchors
sit deliberately on that seam: Reynolds et al. 2003 (population multiple-birth outcome -> INCLUDE),
Thurin et al. 2004 and McLernon et al. 2010 (per-cycle clinical outcomes alongside multiple-birth
rates -> the genuine boundary). If the screen cannot separate these three, the wall is not
enforceable and the scope must say so.

FOUR GATE CASES, RECORDED IN ADVANCE SO THE RUN IS A TEST AND NOT A DEMONSTRATION:

  * BOOK-CANON gate, strongest case yet — and the run found MORE than the sourcing pass did.
    Bulmer 1970 *The Biology of Twinning in Man* (book, 563 cites, no DOI) carries **FIVE** distinct
    review records. Three are refused by the book gate as `review_of_the_work`: Shields 1970 in
    J. Medical Genetics (`10.1136/jmg.7.4.426-b`, typed **`journal-article`**), Benirschke 1971 in
    Teratology (`10.1002/tera.1420040214`, typed `book-review`), and — not found in the sourcing
    pass — a **Science** review (`10.1126/science.170.3961.965`). Two more are caught upstream by the
    title gate because they embed the author's name in the title: `10.2307/1295801` ("Twins The
    Biology of Twinning in Man M. G. Bulmer") and `10.1086/406989`. Only one of the five is typed
    `book-review`, so a type-based rule recovers one case in five. The Science review matters most:
    it is the highest-visibility record of the group and would contaminate a citation frame worst.
  * DUPLICATE-RECORD gate, two independent catches. Pison & D'Addato 2006 carries two DOIs
    (`10.1375/twin.9.2.250`, 98 cites; `10.1375/183242706776382338`, 66) with identical title, year,
    venue and authors. Black, Devereux & Salvanes 2005 likewise carries two (`10.1162/0033553053970179`,
    1,049; `10.1093/qje/120.2.669`, 446) — the QJE MIT-Press-to-OUP migration, which will recur in
    EVERY chapter that anchors on QJE and is therefore worth its own note rather than a local fix.
  * VERSION-OF-RECORD gate, inverted-citation case. Rosenzweig & Zhang: the SSRN preprint (2006, 65
    cites) OUT-CITES the Review of Economic Studies version of record (2009, 11). Ranking by citation
    argmax would take the preprint. Angrist, Lavy & Schlosser has the same shape at lower stakes
    (JOLE 537 vs SSRN 1). Thurin et al. 2004 adds a third shape: the NEJM original (600) alongside
    two 2005 Obstetrical & Gynecological Survey reprints (100 and 24), one of which carries NO
    authors at all.
  * EXISTENCE gate, two cases. Bronars & Grogger 1994 (AER, 368) has NO DOI in the index and
    degraded author metadata ("Bronars Sg"). Martin, Hamilton & Osterman 2012 (NCHS, 329) likewise
    has none, and the absence is ESTABLISHED rather than inferred from a failure: the record matches
    at Jaccard 1.00 with author agreement, and Crossref returns only LATER NCHS reports, all under
    the `10.15620/cdc:` prefix CDC began minting after 2012. Both are carried keyed on title with
    `expect_no_doi`, not faked.

A SELF-INFLICTED FAILURE FROM THIS RUN'S FIRST PASS, KEPT BECAUSE THE SHAPE GENERALISES.
`is_book` is an OPTIONAL candidate field, and the book-canon gate reads it via
`cand.get("is_book")`. The first pass set `expect_no_doi=True` on Bulmer but omitted `is_book=True`,
so the gate silently no-opped: `looks_like_review(..., is_book=True, ...)` was never reached and the
book-specific title floor never applied. Bulmer was still refused — by the ORDINARY author gate, as
`authors_disagree` — so the summary counters looked correct and nothing appeared broken. That is the
dangerous part: a gate keyed off an optional field disengages **invisibly**, and the run reports a
right answer reached by a mechanism that does not generalise. With `is_book=True` set, the refusal
reason changes from `authors_disagree` to `review_of_the_work` and the gate finds three reviews where
the ordinary author gate found one.
A cross-branch audit was run rather than assumed: D.2.d (103), D.1.b (95) and D.3.c (148) all set
`is_book=True` on their book anchors, and B.1 (64) and D.3.b (72) predate the gate entirely. **No
prior chapter is affected.** The hazard is real but the convention was already being followed; this
was a local slip, not a systemic defect.

A CITATION-HYGIENE FINDING THAT IS WORSE THAN A TYPO, AND IS WHY v5's LIST IS NOT TRUSTED HERE.
v5 §A.12 lists three seminal works. All three are defective, and the third is a trap:

  1. Bulmer 1970 — correct, but see the three review records above.
  2. Pison & D'Addato 2006 — v5 implies the title *Frequency of Twin Births among the World
     Populations*. The real title is *Frequency of Twin Births in DEVELOPED Countries*. Plus the
     duplicate DOIs.
  3. Hoekstra et al. "2008" — RESOLVED HERE, and v5 has the wrong year. The review is *Dizygotic
     twinning*, Human Reproduction Update, **2007** (`10.1093/humupd/dmm036`, 203 cites). A real
     Hoekstra 2008 paper exists — *Body composition, smoking, and spontaneous dizygotic twinning*,
     Fertility & Sterility, 50 cites — so a resolver that trusts v5's year lands on a DIFFERENT paper
     by the same first author and reports success. A wrong year that points at a real neighbouring
     paper is more dangerous than a wrong year that points at nothing.

Standing discipline, unchanged from the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) from a LIVE
    OpenAlex sourcing pass (2026-08-22). They assert NO DOIs; the DOI is whatever the resolver
    returns for a ranked match. The DOIs quoted in this docstring are observations from the sourcing
    pass, recorded so the run can be checked, and are NOT fed to the resolver.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached.
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication.

SOURCING-PASS HAZARDS HIT AND WORKED AROUND (all previously recorded, all still live):
  * "The More the Merrier?" returned n=0 on a full-title probe. Stopword-dropping reduces the phrase
    to "merrier", and the `?` is a wildcard. `title.search:merrier family size birth order` finds it.
  * "Dizygotic twinning" alone returns 1,148 records and the target is NOT in the citation head;
    it needs an author-qualified retry.

SCRIPT NUMBERING: 160 is the highest in use on ANY branch, local or remote — checked across
refs/heads and refs/remotes, not against `main`, which would have said 88. This is 161.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, sys, time, unicodedata
from urllib.parse import quote

SLUG = "twinning-multiple-births"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a12_crossref_cache.json")
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


# --- Candidate anchors. Live-sourced 2026-08-22. NO DOIs asserted here by design. ---
CANDIDATES = [
    # ============================================================================================
    # PRIMARY_OFFSET_STOPPING — the ONLY place A.12 can be wrong. The mechanical uplift is an
    # identity; the estimable parameter is whether a twin birth displaces subsequent fertility,
    # making that uplift an upper bound. Estimated by name exactly three times, and the three
    # disagree with each other in a way that is itself the chapter's finding.
    # ============================================================================================
    dict(title="The Impact of Multiple Births on Fertility: Stopping and Spacing in the United "
               "States During the Twentieth Century",
         authors=["George Alter", "J. David Hacker"], year=2024,
         family="primary-offset", provisional_cell="PRIMARY_OFFSET_STOPPING",
         provenance_channel="reconnaissance_probe_primary_cell",
         note="Demography. THE study squarely on the estimand: a multiple birth as a shock to a "
              "stopping-and-spacing process. Six cites, published last year — the primary cell's "
              "head is a NEW paper, which is unusual and means forward-citation seeding at A4 will "
              "return almost nothing from it."),
    dict(title="Parity progression ratios confirm higher lifetime fertility in women who bear twins",
         authors=["Shannen L. Robson", "Ken R. Smith"], year=2012,
         family="primary-offset", provisional_cell="PRIMARY_OFFSET_STOPPING",
         provenance_channel="reconnaissance_probe_primary_cell",
         note="Proceedings of the Royal Society B. The offset is INCOMPLETE — mothers of twins "
              "finish with HIGHER lifetime fertility, not the same. If it replicates, the mechanical "
              "uplift is not merely an upper bound that partly survives; it under-states."),
    dict(title="Twins Support the Absence of Parity-Dependent Fertility Control in Pretransition "
               "Populations",
         authors=["Gregory Clark", "Neil Cummins", "Matthew Curtis"], year=2020,
         family="primary-offset", provisional_cell="PRIMARY_OFFSET_STOPPING",
         provenance_channel="reconnaissance_probe_primary_cell",
         note="Demography. NO stopping response in pre-transition populations, so the uplift passes "
              "through in full there. Note what this paper is actually doing: it uses twins to test "
              "PARITY-DEPENDENT STOPPING, which is A.8's hypothesis, not A.12's. Under PI Call 5 it "
              "is routed to A.8 as a Tier-A anchor there. Retained here because it pins the PM-arm "
              "arithmetic, not because it is evidence FOR A.12."),

    # ============================================================================================
    # PRIMARY_OFFSET_FIRSTSTAGE — Wall 8, DECLARED UNENFORCEABLE at title/abstract. Every one of
    # these estimates our parameter in its first stage and reports it as a nuisance on the way to a
    # child-outcome result. No abstract reveals a first-stage table. They are here so that A4
    # forward-citation seeding reaches the canon; they can never be recovered by screening.
    # ============================================================================================
    dict(title="Testing the Quantity-Quality Fertility Model: The Use of Twins as a Natural "
               "Experiment",
         authors=["Mark R. Rosenzweig", "Kenneth I. Wolpin"], year=1980,
         family="twin-iv-canon", provisional_cell="PRIMARY_OFFSET_FIRSTSTAGE",
         provenance_channel="reconnaissance_probe_instrument_cell",
         note="Econometrica, 716. The origin of the twin instrument. Its first stage is the "
              "completed-fertility response to a twin birth."),
    dict(title="The More the Merrier? The Effect of Family Size and Birth Order on Children's "
               "Education",
         authors=["Sandra E. Black", "Paul J. Devereux", "Kjell G. Salvanes"], year=2005,
         family="twin-iv-canon", provisional_cell="PRIMARY_OFFSET_FIRSTSTAGE",
         provenance_channel="reconnaissance_probe_instrument_cell",
         note="QJE, the most-cited record the instrument probe touched (1,049). DUPLICATE-RECORD "
              "CASE: also indexed at 10.1093/qje/120.2.669 with 446 cites — the QJE MIT-Press-to-OUP "
              "DOI migration. Same title, year, venue, authors. SOURCING HAZARD: the full title "
              "returns n=0 because stopwords collapse 'The More the Merrier' to 'merrier' and '?' "
              "is a wildcard."),
    dict(title="Multiple Experiments for the Causal Link between the Quantity and Quality of "
               "Children",
         authors=["Joshua D. Angrist", "Victor Lavy", "Analia Schlosser"], year=2010,
         family="twin-iv-canon", provisional_cell="PRIMARY_OFFSET_FIRSTSTAGE",
         provenance_channel="reconnaissance_probe_instrument_cell",
         note="Journal of Labor Economics, 537. VERSION-OF-RECORD CASE: an SSRN preprint (2006, 1 "
              "cite) shares the title. Low stakes here; the same shape at high stakes is "
              "Rosenzweig & Zhang below."),
    dict(title="The Economic Consequences of Unwed Motherhood: Using Twin Births as a Natural "
               "Experiment",
         authors=["Stephen G. Bronars", "Jeff Grogger"], year=1994,
         family="twin-iv-canon", provisional_cell="PRIMARY_OFFSET_FIRSTSTAGE",
         provenance_channel="reconnaissance_probe_instrument_cell",
         expect_no_doi=True,
         note="American Economic Review, 368. EXISTENCE-GATE CASE: no DOI in the index, and the "
              "author metadata is degraded to 'Bronars Sg', which will stress the author gate. "
              "Carried keyed on title with expect_no_doi rather than faked."),
    dict(title="Do Population Control Policies Induce More Human Capital Investment? Twins, Birth "
               "Weight and China's One-Child Policy",
         authors=["Mark R. Rosenzweig", "Junsen Zhang"], year=2009,
         family="twin-iv-canon", provisional_cell="PRIMARY_OFFSET_FIRSTSTAGE",
         provenance_channel="reconnaissance_probe_instrument_cell",
         note="Review of Economic Studies. VERSION-OF-RECORD CASE, INVERTED CITATIONS — the SSRN "
              "preprint (2006) carries 65 cites and the journal version of record carries 11. "
              "Citation-argmax ranking takes the preprint; the gate must not. NOTE ALSO: the "
              "reconnaissance reported a 348-cite 'Rosenzweig & Zhang 2008, Demography' record that "
              "the sourcing pass could not reproduce. Flagged for RA — it may be a third version or "
              "a different paper, and it is NOT assumed to be this one."),
    dict(title="Increasing the credibility of the twin birth instrument",
         authors=["Helmut Farbmacher", "Raphael Guber", "Johan Vikstrom"], year=2018,
         family="twin-iv-canon", provisional_cell="PRIMARY_OFFSET_FIRSTSTAGE",
         provenance_channel="reconnaissance_probe_instrument_cell",
         note="Journal of Applied Econometrics, 27. The methods paper on the instrument's validity "
              "and therefore the best single entry point to the first-stage literature. A RePEc "
              "preprint (2016) shares the title."),

    # ============================================================================================
    # SECONDARY_ART_MULTIPLES — the arm PI Call 3 assigned to A.12 (the multiplier, not the
    # deliveries). Three of these five sit deliberately on the RE-CUT Wall 6 seam and test whether
    # an outcome-based discriminator is enforceable at title/abstract.
    # ============================================================================================
    dict(title="Twin Peaks: more twinning in humans than ever before",
         authors=["Christiaan Monden", "Gilles Pison", "Jeroen Smits"], year=2021,
         family="art-multiples", provisional_cell="SECONDARY_ART_MULTIPLES",
         provenance_channel="reconnaissance_probe_art_cell",
         note="Human Reproduction, 229. The global twinning series: 9.1 -> 12.0 twin deliveries per "
              "1,000 between 1980-85 and 2010-15. This is the record that makes v5's ART clause "
              "time-inverted — a peak, not a trend."),
    dict(title="Twinning Rates in Developed Countries: Trends and Explanations",
         authors=["Gilles Pison", "Christiaan Monden", "Jeroen Smits"], year=2015,
         family="art-multiples", provisional_cell="SECONDARY_ART_MULTIPLES",
         provenance_channel="reconnaissance_probe_art_cell",
         note="Population and Development Review, 129. THE stage-10 input. Decomposes the rise into "
              "delayed childbearing and MAR, with MAR about THREE TIMES the age effect — which is "
              "how we know roughly a quarter of A.12's SDT arm is a feedback from postponement "
              "itself. Also dates the post-2000 plateau-and-reversal to MAR policy change."),
    dict(title="Trends in Multiple Births Conceived Using Assisted Reproductive Technology, United "
               "States, 1997-2000",
         authors=["Meredith A. Reynolds", "Laura A. Schieve", "Joyce A. Martin"], year=2003,
         family="art-multiples", provisional_cell="SECONDARY_ART_MULTIPLES",
         provenance_channel="sourcing_pass_wall6_recut",
         note="Pediatrics, 306. WALL 6 RE-CUT TEST, INCLUDE side: an ART-practice paper whose "
              "outcome is a POPULATION multiple-birth share. Under the drafted wall this was "
              "excluded as 'clinical ART practice'; under the re-cut wall it is squarely in "
              "SECONDARY_ART_MULTIPLES. If the screen excludes it, the re-cut has not taken."),
    dict(title="Elective Single-Embryo Transfer versus Double-Embryo Transfer in In Vitro "
               "Fertilization",
         authors=["Ann Thurin", "Jon Hausken", "Torbjorn Hillensjo"], year=2004,
         family="eset-policy", provisional_cell="SECONDARY_ART_MULTIPLES",
         provenance_channel="sourcing_pass_wall6_recut",
         note="NEJM, 600. THE genuine Wall 6 boundary case, and the only randomized variation in "
              "the multiplier that exists. Reports BOTH a per-cycle live-birth rate (Wall 6 exclude "
              "side) and a multiple-birth rate (include side), so the outcome discriminator must "
              "handle a paper carrying one of each. VERSION-OF-RECORD CASE: two 2005 Obstetrical & "
              "Gynecological Survey reprints (100 and 24 cites), and the 24-cite record carries NO "
              "AUTHORS AT ALL, which the author gate must treat as missing data, never as "
              "disagreement."),
    dict(title="Clinical effectiveness of elective single versus double embryo transfer: "
               "meta-analysis of individual patient data from randomised trials",
         authors=["David J. McLernon", "Kirsten Harrild", "Christina Bergh"], year=2010,
         family="eset-policy", provisional_cell="SECONDARY_ART_MULTIPLES",
         provenance_channel="sourcing_pass_wall6_recut",
         note="BMJ, 397, typed `review`. The IPD meta-analysis of the eSET trials — the pooled "
              "version of the only identification this arm has. Same dual-outcome boundary shape as "
              "Thurin."),

    # ============================================================================================
    # EXPOSURE_SERIES — twinning-rate compilations and determinants. NOT effects, and they earn no
    # empirical recall credit. They are what the stage-10 demographic-significance computation
    # actually runs on, which for this chapter is the load-bearing input.
    # ============================================================================================
    dict(title="The Human Multiple Births Database (HMBD)",
         authors=["Catalina Torres", "Arianna Caporali", "Gilles Pison"], year=2023,
         family="exposure-series", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="stage10_input_verified_live",
         note="Demographic Research, 9 cites. The harmonized country-year twinning series and the "
              "single most important record in this file for the chapter's verdict. Note the "
              "companion Figshare static deposit (2022) lists Caporali FIRST while the article "
              "lists Torres first — author-ORDER divergence across versions of the same resource, "
              "which is why the author gate tests set membership and not list position."),
    dict(title="Three decades of twin births in the United States, 1980-2009",
         authors=["Joyce A. Martin", "Brady E. Hamilton", "Michelle J. K. Osterman"], year=2012,
         family="exposure-series", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="sourcing_pass_wall9", expect_no_doi=True,
         note="329 cites. The US series, and the archetype of the finding that the primary cell is "
              "headed by VITAL-STATISTICS REPORTS rather than estimation studies. Also the Wall 9 "
              "anchor: twinning as OUTCOME, routed rather than excluded. NO DOI, AND THE ABSENCE IS "
              "ESTABLISHED RATHER THAN INFERRED FROM A FAILURE: the OpenAlex record matches at "
              "Jaccard 1.00 with author agreement and container `PubMed` and carries no DOI, and a "
              "Crossref bibliographic query returns only LATER NCHS reports, all minted under the "
              "`10.15620/cdc:` prefix that CDC began issuing after this report. Marked "
              "expect_no_doi so it is counted as an index miss and not as a resolver failure."),
    dict(title="The Biology of Twinning in Man",
         authors=["M. G. Bulmer"], year=1970,
         family="exposure-series", provisional_cell="EXPOSURE_SERIES",
         expect_no_doi=True, is_book=True,
         provenance_channel="v5_seminal_list",
         note="Clarendon Press, 563 cites, no DOI. BOOK-CANON GATE, strongest case in the project so "
              "far: THREE distinct review records, and only ONE is typed `book-review` (Benirschke "
              "1971, Teratology). The other two are typed `article` — Shields 1970 in J. Medical "
              "Genetics and Allen 1971 in Europe PMC — and defeat any type-based rule. Signal 4 "
              "(first-position author must be one of ours) refuses all three."),
    dict(title="Frequency of Twin Births in Developed Countries",
         authors=["Gilles Pison", "Agata V. D'Addato"], year=2006,
         family="exposure-series", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="v5_seminal_list",
         note="Twin Research and Human Genetics. DUPLICATE-RECORD GATE: two DOIs, "
              "10.1375/twin.9.2.250 (98) and 10.1375/183242706776382338 (66), identical title, year, "
              "venue and authors — so author agreement is present and the corrected rule demotes "
              "correctly. ALSO A v5 TITLE ERROR: v5 implies 'among the world populations'; the real "
              "title says 'in Developed Countries', which matters because the developed-country "
              "restriction is exactly what the PM arm cannot use."),
    dict(title="Dizygotic twinning",
         authors=["Chantal Hoekstra", "Zhen Zhao", "Cornelius B. Lambalk"], year=2007,
         family="exposure-series", provisional_cell="EXPOSURE_SERIES",
         provenance_channel="v5_seminal_list_year_corrected",
         note="Human Reproduction Update, 203 cites. v5 SAYS 2008 AND v5 IS WRONG — this is the "
              "2007 review. The danger is that a real Hoekstra 2008 paper exists ('Body composition, "
              "smoking, and spontaneous dizygotic twinning', Fertility & Sterility, 50 cites), so "
              "trusting v5's year lands on a different paper by the same first author and reports "
              "success. SOURCING HAZARD: 'dizygotic twinning' alone returns 1,148 records and this "
              "one is NOT in the citation head; it needs an author-qualified retry."),

    # ============================================================================================
    # SECONDARY_PM_VARIATION — PULLED AND TAGGED, NOT EXCLUDED. PI Call 5 is adopted RA-provisional
    # (reduce the PM arm, route Clark et al. to A.8). Keeping this cluster in hand makes an overturn
    # cost a re-screen instead of a re-search.
    # ============================================================================================
    dict(title="Twinning across the Developing World",
         authors=["Jeroen Smits", "Christiaan Monden"], year=2011,
         family="pm-variation", provisional_cell="SECONDARY_PM_VARIATION",
         provenance_channel="reconnaissance_probe_pm_cell",
         note="PLoS ONE, 305. The cross-population twinning literature's anchor, including the West "
              "African dizygotic excess. Retained to bound the PM arm arithmetically: the spread is "
              "roughly 1% to 2% of deliveries, which against PM fertility measured in whole children "
              "is not a candidate explanation. Bounding it is the deliverable; it is not evidence."),

    # ============================================================================================
    # ROUTING DECOYS — one per ENFORCEABLE wall, so the production query is tested on routing and
    # not only on topical retrieval. Per the D.2.d finding these are forward-cited like any other
    # seed at A4: a decoy's citation neighbourhood is where the boundary cases live. Two of these
    # are PURE HOMONYMS rather than boundary cases, which is this chapter's carve-out from the
    # standing decoy-cloud guidance, and they are here to prove the lexical separation holds.
    # ============================================================================================
    dict(title="A short history of SHELX",
         authors=["George M. Sheldrick"], year=2007,
         family="decoy-crystallography", provisional_cell="OFF_HOMONYM_CRYSTAL",
         provenance_channel="reconnaissance_probe_decoy_cloud_1",
         note="Acta Crystallographica A, 87,694 cites. Wall 1. Outranks every genuine A.12 record by "
              "two orders of magnitude and heads three separate probes. A pure homonym — "
              "'twinning' is a crystal lattice defect — with zero on-topic content, so it takes a "
              "HARD exclusion. If this record survives the production query, the query is broken."),
    dict(title="High strength Fe-Mn-(Al, Si) TRIP/TWIP steels development - properties - "
               "application",
         authors=["O. Grassel", "L. Kruger", "G. Frommeyer"], year=2000,
         family="decoy-engineering", provisional_cell="OFF_HOMONYM_ENGINEERING",
         provenance_channel="reconnaissance_probe_decoy_cloud_2",
         note="International Journal of Plasticity, 1,812. Wall 2. TWIP = TWinning-Induced "
              "Plasticity. Second pure homonym."),
    dict(title="An Observational Analysis of Twin Births, Calf Sex Ratio, and Calf Mortality in "
               "Holstein Dairy Cattle",
         authors=["Noelia Silva del Rio", "Steven Stewart", "Paul Rapnicki"], year=2007,
         family="decoy-nonhuman", provisional_cell="OFF_NONHUMAN",
         provenance_channel="sourcing_pass_wall3",
         note="Journal of Dairy Science, 221. Wall 3. The veterinary cloud is NOT a homonym — these "
              "papers really are about twinning and really are about fertility — but the species is "
              "wrong. Four of the eight records in the reconnaissance's 'twinning as a determinant "
              "of fertility level' head were ewes, goats or cattle. Lexically separable because a "
              "dairy paper never says 'completed fertility'."),
    dict(title="Hidden heritability due to heterogeneity across seven populations",
         authors=["Felix C. Tropf", "Sang Hong Lee", "Renske M. Verweij"], year=2017,
         family="decoy-twindesign", provisional_cell="OFF_TWINDESIGN",
         provenance_channel="sourcing_pass_wall4",
         note="Nature Human Behaviour, 184. Wall 4 and A.18's territory. This is the ONE decoy "
              "family here that is a genuine boundary case in the ordinary sense: twins as a "
              "research DESIGN, not a rate — but the heritability of dizygotic twinning is a real "
              "A.12 input. Routed, never excluded. Note v5 §A.18 lists Tropf et al. 2015; this is "
              "the 2017 record."),
    dict(title="Perinatal outcome of singletons and twins after assisted conception: a systematic "
               "review of controlled studies",
         authors=["Frans M. Helmerhorst", "Denise A. M. Perquin", "Diana Donker"], year=2004,
         family="decoy-perinatal", provisional_cell="OFF_PERINATAL",
         provenance_channel="sourcing_pass_wall5",
         note="BMJ, 1,117. Wall 5, and the hardest routing case in this file because it sits on "
              "THREE walls at once: it is perinatal outcomes (Wall 5 exclude), it is ART (Wall 6), "
              "and it compares twins to singletons (Wall 4 shape). Its outcome is health, not a "
              "birth count, so the outcome-based discriminator should send it to OFF_PERINATAL. "
              "It is the sharpest single test of whether the re-cut Wall 6 is enforceable."),
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

    L = [f"# A3 cold-start anchors — {SLUG} (A.12)", "",
         f"Sourced in a live OpenAlex pass (2026-08-22) and resolved through five gates: "
         f"{len(anchors)} candidate anchors, of which {len(empirical)} are empirical primary-cell "
         "anchors (the causal recall denominator) and the rest are exposure-series, ART-multiples, "
         "PM-variation or routing-decoy anchors that earn no empirical recall credit. No DOI is "
         "hand-asserted; each is the top-ranked version-of-record candidate from a unified Crossref "
         "+ OpenAlex field, then re-affirmed at doi.org.", "",
         "**Read the cell counts with the chapter's structure in mind.** A.12 is an accounting "
         "identity with a behavioral offset. The mechanical arm is arithmetic that no study "
         "estimates, so a small `PRIMARY_*` count is the CORRECT state of the world here and not a "
         "thin literature. The load-bearing cell for the verdict is `EXPOSURE_SERIES`, which feeds "
         "the stage-10 computation.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Expected index miss (no DOI by nature): {n_book}**", "",
         f"**Shadow records refused: {n_shadow}** across {len([a for a in anchors if a.get('shadows_refused')])} "
         f"anchors.  **Integrity flags raised: {n_integrity}.**", "",
         f"**Duplicate records demoted: {n_dup}** across "
         f"{len([a for a in anchors if a.get('duplicates_demoted')])} anchors. Two independent "
         "catches were predicted before the run. Pison & D'Addato 2006 carries 10.1375/twin.9.2.250 "
         "(98 cites) and 10.1375/183242706776382338 (66) with identical title, year, venue and "
         "authors. Black, Devereux & Salvanes 2005 carries 10.1162/0033553053970179 (1,049) and "
         "10.1093/qje/120.2.669 (446) — the QJE MIT-Press-to-OUP DOI migration. **The QJE case "
         "generalises beyond this chapter**: any hypothesis anchoring on a pre-migration QJE article "
         "will meet a split citation count, and it should be handled in the shared resolver rather "
         "than rediscovered per chapter.", "",
         f"**Review-shape or author refusals: {n_review_rejected}.** The book-canon gate meets its "
         "strongest case in the project here, and the run surfaced more than the sourcing pass did. "
         "Bulmer 1970 carries **FIVE** distinct review records. The book gate refuses three as "
         "`review_of_the_work` — Shields 1970 in Journal of Medical Genetics (typed "
         "`journal-article`), Benirschke 1971 in Teratology (typed `book-review`), and a **Science** "
         "review at 10.1126/science.170.3961.965 that the sourcing pass did not find. Two more are "
         "caught upstream by the title gate because they embed the author's name in the title "
         "(10.2307/1295801, 10.1086/406989). Only one record in five is typed `book-review`, so a "
         "type-based rule would recover one case in five. The Science review is the one that matters "
         "most: highest visibility of the group, and the worst contaminant of a citation frame.", "",
         "## Cell counts", "",
         "| Cell | Verified / total |", "|---|---|"] + \
        [f"| `{k}` | {sum(v)}/{len(v)} |" for k, v in sorted(by_cell.items())] + \
        ["",
         "## Resolution log", ""] + log + \
        ["",
         "## Findings this run is designed to test, recorded in advance", "",
         "- **v5's seminal list for A.12 is three-for-three defective, and the third is a trap.** "
         "Bulmer 1970 resolves but carries three review records. Pison & D'Addato 2006 has the wrong "
         "title in v5 (*in Developed Countries*, not *among the world populations*) and duplicate "
         "DOIs. Hoekstra 'et al. 2008' is **2007** — *Dizygotic twinning*, Human Reproduction "
         "Update, 10.1093/humupd/dmm036, 203 cites. A real Hoekstra 2008 paper exists (*Body "
         "composition, smoking, and spontaneous dizygotic twinning*, Fertility & Sterility, 50 "
         "cites), so a resolver trusting v5's year lands on a DIFFERENT paper by the same first "
         "author and reports success. A wrong year pointing at a real neighbouring paper is more "
         "dangerous than one pointing at nothing.",
         "- **Wall 6 was re-cut on OUTCOME before this run, and three anchors sit on the seam.** PI "
         "Call 3 (split at the margin) made the drafted treatment-based Wall 6 self-defeating: it "
         "excluded transfer-protocol studies, which are the only quasi-experimental variation in "
         "the multiplier that exists. Reynolds et al. 2003 is the INCLUDE side (population "
         "multiple-birth outcome); Thurin et al. 2004 and McLernon et al. 2010 are the genuine "
         "boundary (per-cycle clinical outcomes reported ALONGSIDE multiple-birth rates); "
         "Helmerhorst et al. 2004 is the EXCLUDE side and the sharpest test, sitting on three walls "
         "at once. If the screen cannot separate these four, the wall is not enforceable and the "
         "scope must be amended to say so.",
         "- **The version-of-record gate meets an inverted-citation case.** Rosenzweig & Zhang's "
         "SSRN preprint (2006, 65 cites) out-cites the Review of Economic Studies version of record "
         "(2009, 11). Citation-argmax ranking takes the preprint. Separately, the reconnaissance "
         "reported a 348-cite 'Rosenzweig & Zhang 2008, Demography' record that the sourcing pass "
         "could not reproduce — flagged for RA and NOT assumed to be the same paper.",
         "- **The author gate must handle a record with NO authors.** One of the two 2005 "
         "Obstetrical & Gynecological Survey reprints of Thurin et al. carries an empty author list. "
         "Missing metadata is missing data and must never be scored as disagreement.",
         "- **Two decoy families are pure homonyms, which is this chapter's carve-out from the "
         "standing decoy-cloud guidance.** Crystallographic twinning (SHELX, 87,694 cites) and "
         "TWIP steel have zero on-topic content and take hard exclusions, not routing decisions. "
         "The guidance that decoy clouds are boundary cases running 29-88% on-topic does not apply "
         "to a homonym. The behaviour-genetics family (Tropf et al. 2017, A.18) IS an ordinary "
         "boundary case and is routed, not excluded.",
         "- **The primary cell's head is a 2024 paper.** Alter & Hacker carries six cites. Forward-"
         "citation seeding from the chapter's most on-estimand study will return almost nothing at "
         "A4, and that is a property of the literature rather than a failure of the seeding.",
         "- **A gate keyed off an optional field can disengage invisibly, and did on this run's "
         "first pass.** `is_book` is optional and the book-canon gate reads it through "
         "`cand.get(\"is_book\")`. Bulmer was first entered with `expect_no_doi=True` but WITHOUT "
         "`is_book=True`, so the gate silently no-opped and the ordinary author gate refused the "
         "anchor instead, as `authors_disagree`. The summary counters looked correct and nothing "
         "appeared broken — a right answer by a mechanism that does not generalise. Setting the flag "
         "changes the refusal reason to `review_of_the_work` and finds three reviews where the "
         "author gate found one. Audited across branches rather than assumed: D.2.d (103), D.1.b "
         "(95) and D.3.c (148) all set the flag; B.1 (64) and D.3.b (72) predate the gate. No prior "
         "chapter is affected.",
         "- **One serendipitous on-topic find, recorded so it is not lost.** The Bulmer probe "
         "refused `10.2139/ssrn.5258235`, *Does the One-Child Policy Increase Man-Made Twinning "
         "Rate?*, on the title gate. It is not a Bulmer record, but it IS on A.12's topic — "
         "policy-induced twinning — and it did not surface in any reconnaissance probe. Carried "
         "forward to A4/A6 as a seed rather than discarded as a refusal.",
         "- **Empirical recall denominator.** Only the `PRIMARY_*` anchors count. The exposure-"
         "series, ART-multiples, PM-variation and routing-decoy anchors are indispensable to the "
         "stage-10 computation and to the routing rules, and they are not evidence for the "
         "hypothesis. Per the Tier-A finding, they are studies in their own right and are not an "
         "artifact of the screen.",
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
