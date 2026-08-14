#!/usr/bin/env python3
"""
134_b6_cold_start_anchors.py — B.6 (microplastics and PFAS in reproductive tissues), stage A3.

Inherits `124_b7_cold_start_anchors.py` unchanged in its resolver and its four gates, and adds a
fifth that this chapter's literature makes necessary. Five gates, all mandatory, each catching a
failure the others structurally cannot:

  * EXISTENCE gate (OAS, 2026-07-08). No anchor enters a recall denominator without a live DOI or a
    Crossref/OpenAlex record confirming the title exists. Catches ghosts: titles resolving to nothing.
  * VERSION-OF-RECORD gate (D.1.b, 2026-08-07). Candidates are RANKED for version-of-record status
    rather than taken at the title argmax. Catches a title resolving to something real that is not
    the record meant — a preprint, working paper, reprint, repository copy, or chapter. LIVE HERE:
    the follicular-fluid anchor exists as a 2024 medRxiv preprint and a 2025 journal article whose
    titles differ only in capitalisation.
  * BOOK-CANON gate (D.2.d, 2026-08-08). Catches a real, correctly-titled, contemporaneous record of
    a DIFFERENT work: a review OF a monograph. Little to do here — B.6's canon is journal-shaped —
    and kept so the inheritance stays honest.
  * SHADOW-RECORD gate (B.7, 2026-08-12). Catches a real, indexed, separately-DOI'd record whose
    title is the target title plus a leading qualifier. LIVE HERE on three anchors: two "Faculty
    Opinions recommendation of ...", one "Letter to the editor, ...", one "Re: ..." in J Urol.
  * DUPLICATE-RECORD gate (NEW, B.6, 2026-08-14, and UNVALIDATED — read below). Aims at what none of
    the four above sees: the SAME work indexed twice under DIFFERENT DOIs, with the citation count
    split between the copies. Both copies pass existence, version, book and shadow, so DOI-level
    deduplication passes both and double-counts the anchor.

**The case that motivated this gate turned out not to be an instance of it, and the correction is
worth more than the gate.** The Minderoo-Monaco Commission — what HYPOTHESES-v5 means by its
non-existent "Lancet Commission on Reproductive Health (2025)" — is indexed as:

    10.5334/aogh.4056   Ann Glob Health 2023, vol 89   447 cites   48 authors, Landrigan et al.
    10.5334/aogh.4083   Ann Glob Health 2023, vol 89    41 cites   ONE author, Maria Neira
    10.5334/aogh.4331   "Correction: ..."               26 cites   (caught by the shadow gate)

Same title, same year, same volume, same venue — and NOT the same work. 4083 is a single-author
companion piece deposited under the report's title. The AUTHOR gate already separates them, correctly
and without help, so this gate never saw the case it was built for.

That finding also exposed a way the gate could do harm. `author_match` returns None — not False — for
a record carrying no author metadata, so such a record passes upstream; a bare title+year+venue rule
would then silently demote a legitimately distinct same-title work as a duplicate. That is the same
defect as the suffix-containment rule the shadow gate discarded, arrived at from a different
direction. Demotion therefore requires positive author agreement, and missing metadata never counts
as agreement.

**Status: the gate has zero confirmed catches in this corpus and is retained as an unvalidated
safeguard**, cheap to run, incapable of firing without author agreement, and recording rather than
dropping whatever it does demote. Same-work-under-two-DOIs is real in commission and consensus
literature; it simply is not what was happening here. It should not be described as validated until
something trips it.

Same standing discipline as the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) from a LIVE
    OpenAlex sourcing pass (2026-08-14). They assert NO DOIs; the DOI is whatever the resolver
    returns for a ranked match. Author lists are live-sourced too — and this chapter is the strongest
    case yet for that rule. THREE of HYPOTHESES-v5's four seminal citations for B.6 do not resolve as
    written: "Zhao et al., Fertility & Sterility (2025)" conflates Zhao et al. 2023 (Sci Total
    Environ, testis and semen) with Montano et al. 2025 (Ecotox Environ Saf, follicular fluid); the
    "Lancet Commission" does not exist; "Yang et al., Scientific Reports (2025)" resolves to nothing;
    and "Shoaito et al., Environment International (2023)" is Shoaito et al. 2019 in EHP, on a
    PHTHALATE — the B.2 side of the wall that defines B.6.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached, because caching one turns a rate-limited call into a permanent "does not exist".
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication.

Deliberate gate test cases in the candidate set, included because a gate with nothing to catch is a
gate that has not been tested: Montano et al. 2025 (preprint twin, version gate); Landrigan et al.
2023 (double-DOI'd plus a correction record, duplicate and shadow gates); Leslie et al. 2022 (a
"Letter to the editor, ..." twin and a Faculty Opinions twin); Levine et al. 2017 (a "Re: ..." twin
in J Urol and two Faculty Opinions twins); Joensen et al. 2009 (Faculty Opinions twin).

**The routing decoys carry one anchor per wall**, so the search is tested on routing and not only on
topical retrieval: Shoaito 2019 for Wall 1 (B.2 phthalate), Waterfield 2020 for Wall 2 (pregnancy
safety, and the Call 3 `ASIDE_EXTRACTED` instance), Savitz 2012 for Wall 2 in its C8 form, Bellavia
2022 for Wall 1's mixture case and Wall 4's ART frame, Sussarellu 2016 for Wall 5 (oyster
ecotoxicology), Levine 2017 for Wall 7 (unattributed outcome trend).

**The microplastics PRIMARY cell has no anchor, and that is a result rather than an omission.** The
reconnaissance found no human study estimating microplastic exposure against a fertility quantity;
the closest records are tissue detection with no outcome, or rodent work. The scope document
predicted this and the anchor set records the absence explicitly rather than substituting a detection
record and letting the gap disappear. If A6 later surfaces one, it is a genuine discovery.

SCRIPT NUMBERING: 88 is the highest on `main`, but the unmerged branches collide — D.1.b holds
95-102, D.1.a 95-115, D.2.d 103-108, B.5 115-122, B.7 123-131. This run starts above every number in
use on ANY branch, local or remote; note that D.1.a's 115 sits on an unpushed local branch and is
invisible to a scan of `origin`. 132 is the reconnaissance probe, 133 the anchor retry, and this
is 134.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, sys, time
from urllib.parse import quote

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b6_crossref_cache.json")
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
    # === PRIMARY_EXPOSURE_TO_FERTILITY — PFAS. The identification-bearing cell, and the only one
    # === of the two families that populates it at all.
    dict(title="Maternal levels of perfluorinated chemicals and subfecundity",
         authors=["C. Fei", "Joseph K. McLaughlin", "Loren Lipworth", "Jorn Olsen"], year=2009,
         family="primary-pfas-female", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Hum Reprod. The founding estimate of the PFAS-subfecundity literature and the most "
              "cited record in the chapter's primary cell. Danish National Birth Cohort. Its own "
              "cohort re-analysed it six years later (Bach et al. 2015) once the parity problem was "
              "understood, so the two must be extracted as a pair and never pooled."),
    dict(title="Perfluorinated Compounds and Subfecundity in Pregnant Women",
         authors=["Kristina W. Whitworth", "Line Smastuen Haug", "Donna D. Baird", "Georg Becher",
                  "Jane A. Hoppin"], year=2011,
         family="primary-pfas-female", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Epidemiology. MoBa. THE PARITY-HANDLING ANCHOR: stratifies by parity and finds the "
              "association concentrated among parous women, which is the signature of elimination "
              "running backwards rather than of a causal effect. Call 2's two-track synthesis is "
              "built on the distinction this paper made operational."),
    dict(title="Association between perfluorinated compounds and time to pregnancy in a prospective cohort of Danish couples attempting to conceive",
         authors=["Sys Vestergaard", "Flemming Nielsen", "Anna-Maria Andersson",
                  "Niels Henrik Hjollund", "Philippe Grandjean"], year=2012,
         family="primary-pfas-female", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Hum Reprod. Preconception-measured and restricted to couples attempting to conceive "
              "— the design that avoids measuring exposure after the outcome. Null."),
    dict(title="Perfluoroalkyl acids and time to pregnancy revisited: An update from the Danish National Birth Cohort",
         authors=["Cathrine Carlsen Bach", "Zeyan Liew", "Bodil Hammer Bech", "Ellen A. Nohr",
                  "Chunyuan Fei"], year=2015,
         family="primary-pfas-female", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Environ Health. The correction to Fei et al. 2009 from inside the same cohort, and "
              "the single most informative record for Call 2: it shows what happens to the estimate "
              "when parity is handled. Shares an author with the original."),
    dict(title="Maternal exposure to perfluorinated chemicals and reduced fecundity: the MIREC study",
         authors=["Maria P. Velez", "Tye E. Arbuckle", "William D. Fraser"], year=2015,
         family="primary-pfas-female", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Hum Reprod. Canadian MIREC cohort; independent population, so it carries weight the "
              "three Danish/Norwegian records cannot add to each other."),

    # === PRIMARY_MALE_FECUNDITY and SEMEN_PARAMETER — PFAS ===
    dict(title="Do Perfluoroalkyl Compounds Impair Human Semen Quality?",
         authors=["Ulla Nordstrom Joensen", "Rossana Bossi", "Henrik Leffers",
                  "Allan Astrup Jensen", "Niels E. Skakkebaek"], year=2009,
         family="primary-pfas-male", provisional_cell="SEMEN_PARAMETER",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Environ Health Perspect. The male anchor. SHADOW-GATE TEST CASE: a 'Faculty Opinions "
              "recommendation of Do perfluoroalkyl compounds impair human semen quality?' record "
              "exists at its own DOI and resolves at overlap 1.0."),
    dict(title="Exposure to perfluorinated compounds and human semen quality in arctic and European populations",
         authors=["Gunnar Toft", "Bo Jonsson", "Christian Lindh", "Aleksander Giwercman",
                  "Maria Spano"], year=2012,
         family="primary-pfas-male", provisional_cell="SEMEN_PARAMETER",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Hum Reprod. Cross-population design; the INUENDO cohort."),
    dict(title="Endocrine Disruption of Androgenic Activity by Perfluoroalkyl Substances: Clinical and Experimental Evidence",
         authors=["Andrea Di Nisio", "Iva Sabovic", "Umberto Valente", "Simone Tescari",
                  "Maria Santa Rocca"], year=2018,
         family="primary-pfas-male", provisional_cell="ENDOCRINE_MECHANISM",
         provenance_channel="direct_empirical_bibliographic_search",
         note="J Clin Endocrinol Metab. Veneto high-exposure young men — Wall 9 population with a "
              "measured reproductive-endocrine endpoint. One of very few records that pairs an "
              "exogenous exposure contrast with a reproductive outcome in humans."),

    # === PRIMARY_HIGH_EXPOSURE — Wall 9, the only exogenous exposure variation that exists ===
    dict(title="Perfluoroalkyl substances (PFAS) in drinking water and risk for polycystic ovarian syndrome, uterine leiomyoma, and endometriosis",
         authors=["Sofia Hammarstrand", "Kristina Jakobsson", "Eva Andersson", "Yiyi Xu", "Ying Li"],
         year=2021, family="high-exposure", provisional_cell="PRIMARY_HIGH_EXPOSURE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Environ Int. Ronneby, Sweden: a municipal water supply contaminated by firefighting "
              "foam, giving serum levels one to two orders of magnitude above background. The "
              "outcomes are gynaecological morbidity rather than a fertility quantity, so this "
              "anchor also tests whether the screen holds the estimand line under a very strong "
              "design — the temptation this chapter must resist."),

    # === DETECTION_TISSUE — the cell v5 built the split on. Earns NO causal recall. ===
    dict(title="Plasticenta: First evidence of microplastics in human placenta",
         authors=["Antonio Ragusa", "Alessandro Svelato", "Criselda Santacroce", "Piera Catalano",
                  "Valentina Notarstefano"], year=2020,
         family="detection-mp", provisional_cell="DETECTION_TISSUE",
         provenance_channel="hypothesis_canon",
         note="Environ Int. The most-cited record in the whole B.6 corpus and the origin of the "
              "'microplastics are in the reproductive tract' claim. No fertility outcome estimated."),
    dict(title="First evidence of microplastics in human ovarian follicular fluid: An emerging threat to female fertility",
         authors=["Luigi Montano", "Salvatore Raimondo", "Marina Piscopo", "Maria Ricciardi",
                  "Antonino Guglielmino"], year=2025,
         family="detection-mp", provisional_cell="DETECTION_TISSUE",
         provenance_channel="hypothesis_canon",
         note="Ecotox Environ Saf. What HYPOTHESES-v5 miscites as 'Zhao et al., Fertility & "
              "Sterility (2025)'. VERSION-GATE TEST CASE: a 2024 medRxiv preprint carries the same "
              "title differing only in capitalisation, and a 2026 Fertility and Sterility record "
              "carries a near-identical title. Substantively the Call 5 anchor: 18 women at a "
              "Salerno IVF centre, particles in 14, and NO association with AMH, fertilization, "
              "miscarriage or live birth. Presence is exposure, not effect."),
    dict(title="Detection and characterization of microplastics in the human testis and semen",
         authors=["Qiancheng Zhao", "Long Zhu", "Jiaming Weng", "Zirun Jin", "Yalei Cao"], year=2023,
         family="detection-mp", provisional_cell="DETECTION_TISSUE",
         provenance_channel="hypothesis_canon",
         note="Sci Total Environ. The real Zhao et al. — 2023, not 2025, and testis/semen, not "
              "follicular fluid. Half of v5's conflated first citation."),
    dict(title="Microplastic presence in dog and human testis and its potential association with sperm count and weights of testis and epididymis",
         authors=["Chelin Jamie Hu", "Marcus A. Garcia", "Alexander Nihart", "Rui Liu", "Lei Yin"],
         year=2024, family="detection-mp", provisional_cell="DETECTION_TISSUE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Toxicol Sci. The closest thing in the MP literature to a detection-plus-association "
              "study in humans, and it is cross-sectional, small, and part canine. Tests whether "
              "the screen keeps DETECTION_TISSUE separate from SEMEN_PARAMETER when one record "
              "straddles both."),
    dict(title="Discovery and quantification of plastic particle pollution in human blood",
         authors=["H.A. Leslie", "Martin J. M. van Velzen", "Sicco H. Brandsma", "D. Vethaak",
                  "Juan J. Garcia-Vallejo"], year=2022,
         family="detection-mp", provisional_cell="DETECTION_TISSUE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Environ Int. Systemic bioavailability — the record that makes reproductive-tissue "
              "detection mechanistically unsurprising. SHADOW-GATE TEST CASE: both a 'Letter to the "
              "editor, discovery and quantification of plastic particle pollution in human blood' "
              "and a 'Faculty Opinions recommendation of ...' twin exist at their own DOIs."),
    dict(title="Detection of Various Microplastics in Human Stool",
         authors=["Philipp Schwabl", "Sebastian Koppel", "Philipp Konigshofer", "Theresa Bucsics",
                  "Michael Trauner"], year=2019,
         family="detection-mp", provisional_cell="DETECTION_TISSUE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Ann Intern Med. The first human-burden detection record; anchors the exposure-"
              "assessment stream's start date."),
    dict(title="Nontargeted identification of per- and polyfluoroalkyl substances in human follicular fluid and their blood-follicle transfer",
         authors=["Qiyue Kang", "Fumei Gao", "Xiaohua Zhang", "Lei Wang", "Jiaying Liu"], year=2020,
         family="detection-pfas", provisional_cell="DETECTION_TISSUE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Environ Int. The PFAS counterpart to the MP follicular-fluid work, and five years "
              "earlier — evidence that 'detected inside the reproductive system itself' is not the "
              "novelty v5 claims for the split, at least not for PFAS."),

    # === PARAMETER_PHARMACOKINETIC — load-bearing for Call 2's reverse-causation correction ===
    dict(title="Half-Life of Serum Elimination of Perfluorooctanesulfonate, Perfluorohexanesulfonate, and Perfluorooctanoate in Retired Fluorochemical Production Workers",
         authors=["Geary W. Olsen", "Jean M. Burris", "David J. Ehresman", "John W. Froehlich",
                  "Andrew M. Seacat"], year=2007,
         family="pharmacokinetic", provisional_cell="PARAMETER_PHARMACOKINETIC",
         provenance_channel="parameter_stream",
         note="Environ Health Perspect. The half-life estimates on which every claim about exposure "
              "windows and elimination rests."),
    dict(title="Determinants of plasma concentrations of perfluoroalkyl substances in pregnant Norwegian women",
         authors=["Anne Lise Brantsaeter", "Kristina W. Whitworth", "Trond A. Ydersbond",
                  "Line Smastuen Haug", "Margaretha Haugen"], year=2013,
         family="pharmacokinetic", provisional_cell="PARAMETER_PHARMACOKINETIC",
         provenance_channel="parameter_stream",
         note="Environ Int. THE REVERSE-CAUSATION ANCHOR: parity and breastfeeding history as "
              "determinants of serum concentration. This is the paper that makes 'parity causes "
              "exposure' a measured fact rather than a mechanism story."),
    dict(title="Perfluorinated Alkyl Acids in Blood Serum from Primiparous Women in Sweden: Serial Sampling during Pregnancy and Nursing, And Temporal Trends 1996-2010",
         authors=["Anders Glynn", "Urs Berger", "Anders Bignert", "Shahid Ullah", "Marie Aune"],
         year=2012, family="pharmacokinetic", provisional_cell="PARAMETER_PHARMACOKINETIC",
         provenance_channel="parameter_stream",
         note="Environ Sci Technol. Serial within-woman sampling through pregnancy and nursing — "
              "the elimination pathway measured directly, in the population the fertility studies "
              "sample."),

    # === PARAMETER_EXPOSURE — the series the demographic-significance test multiplies ===
    dict(title="Trends in Exposure to Polyfluoroalkyl Chemicals in the U.S. Population: 1999-2008",
         authors=["Kayoko Kato", "Lee-Yang Wong", "Lily Jia", "Zsuzsanna Kuklenyik"], year=2011,
         family="exposure-series", provisional_cell="PARAMETER_EXPOSURE",
         provenance_channel="parameter_stream",
         note="Environ Sci Technol. NHANES. The record that falsifies v5's 'the exposure is "
              "structurally rising' for legacy PFAS: PFOS and PFHxS trend DOWN after production "
              "was discontinued, PFOA is flat from 2003, only PFNA trends up. Compound-specific, "
              "which is why CHEMICAL_FAMILY has a PFAS_REPLACEMENT level."),

    # === Channel 1 — prior systematic reviews. Exists for PFAS, absent for microplastics. ===
    dict(title="Perfluoroalkyl and polyfluoroalkyl substances and measures of human fertility: a systematic review",
         authors=["Cathrine Carlsen Bach", "Anne Vested", "Kristian Tore Jorgensen",
                  "Jens Peter Bonde", "Tine Brink Henriksen"], year=2016,
         family="channel1", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="channel1_review_seed",
         note="Crit Rev Toxicol. The prior review on this chapter's exact estimand. LEAKAGE WALL "
              "APPLIES: its search strategy must not be mined for A6 query terms, since it is also "
              "the benchmark against which Recall(A) is computed."),
    dict(title="The effects of perfluoroalkyl and polyfluoroalkyl substances on female fertility: A systematic review and meta-analysis",
         authors=["Wei Wang", "Xiang Hong", "Fanqi Zhao", "Jingying Wu", "Bei Wang"], year=2022,
         family="channel1", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="channel1_review_seed",
         note="Environ Res. The only meta-analysis on the primary estimand. LEAKAGE WALL APPLIES."),
    dict(title="Persistent organic pollutants and couple fecundability: a systematic review",
         authors=["Linda G. Kahn", "Kim G. Harley", "Eva Siegel", "Yeyi Zhu", "Pam Factor-Litvak"],
         year=2020, family="channel1", provisional_cell="PRIMARY_EXPOSURE_TO_FERTILITY",
         provenance_channel="channel1_review_seed",
         note="Hum Reprod Update. Broader than B.6 — spans B.2 and B.6 families — so it is also a "
              "Wall 1 test: the resolver keeps it, the screen must mark it MIXTURE_UNSEPARABLE "
              "unless compound-specific estimates are recoverable. LEAKAGE WALL APPLIES."),
    dict(title="Perfluoroalkyl and polyfluoroalkyl substances (PFAS) and their effects on the ovary",
         authors=["Ning Ding", "Sioban D. Harlow", "John F. Randolph", "Rita Loch-Caruso",
                  "Sung Kyun Park"], year=2020,
         family="mechanism", provisional_cell="OVARIAN_PARAMETER",
         provenance_channel="channel1_review_seed",
         note="Hum Reprod Update. The ovarian mechanism review."),
    dict(title="Per- and poly-fluoroalkyl substances (PFAS) and female reproductive outcomes: PFAS elimination, endocrine-mediated effects, and disease",
         authors=["Brittany P. Rickard", "Imran Rizvi", "Suzanne E. Fenton"], year=2021,
         family="mechanism", provisional_cell="PARAMETER_PHARMACOKINETIC",
         provenance_channel="channel1_review_seed",
         note="Toxicology. Names elimination as a competing explanation for the observed "
              "associations in its own title — the clearest statement in the literature that this "
              "chapter's central identification threat is recognised by the field."),

    # === ROUTING DECOYS — one per wall, so routing is tested and not only topical retrieval ===
    dict(title="The Role of Peroxisome Proliferator-Activated Receptor Gamma (PPARgamma) in Mono(2-ethylhexyl) Phthalate (MEHP)-Mediated Cytotrophoblast Differentiation",
         authors=["Hussein Shoaito", "Julia Petit", "Audrey Chissey", "Nicolas Auzeil",
                  "Jean Guibourdenche"], year=2019,
         family="decoy-wall1-b2", provisional_cell="OFF_LEGACY_EDC_B2",
         provenance_channel="routing_decoy",
         note="Environ Health Perspect. WALL 1 DECOY, and the live instance of v5's fourth seminal "
              "citation being a B.2 paper: MEHP is a phthalate metabolite. Wrong year and wrong "
              "journal in v5 as well. If the screen routes this into B.6 the wall that defines the "
              "chapter is not being enforced."),
    dict(title="Reducing exposure to high levels of perfluorinated compounds in drinking water improves reproductive outcomes: evidence from an intervention in Minnesota",
         authors=["Gina Waterfield", "Martha Rogers", "Philippe Grandjean",
                  "Maximilian Auffhammer", "David L. Sunding"], year=2020,
         family="decoy-wall2-pregnancy", provisional_cell="OFF_PREGNANCY_SAFETY",
         aside_extracted=True,
         provenance_channel="routing_decoy",
         note="Environ Health. WALL 2 DECOY and the Call 3 instance. The only difference-in-"
              "differences design in the corpus — the 2006 Oakdale water filtration installation — "
              "and its outcomes are birth weight and preterm birth, so it routes OUT of synthesis. "
              "Flagged ASIDE_EXTRACTED: extract the estimate, report it in a named aside with the "
              "estimand mismatch stated, and keep it out of every pooled quantity and every recall "
              "denominator. Note the author list is half environmental economists, which is why it "
              "is the best-identified study here and also why it answers a different question."),
    dict(title="Relationship of Perfluorooctanoic Acid Exposure to Pregnancy Outcome Based on Birth Records in the Mid-Ohio Valley",
         authors=["David A. Savitz", "Cheryl R. Stein", "Beth Elston", "Gregory A. Wellenius",
                  "Scott M. Bartell"], year=2012,
         family="decoy-wall2-pregnancy", provisional_cell="OFF_PREGNANCY_SAFETY",
         provenance_channel="routing_decoy",
         note="Environ Health Perspect. WALL 2 DECOY in its C8 form. The high-exposure cohorts have "
              "been studied for birth outcomes far more than for fertility, so this is the shape "
              "most Wall 9 records actually take — a strong design pointed at the wrong estimand."),
    dict(title="Association between chemical mixtures and female fertility in women undergoing assisted reproduction in Sweden and Estonia",
         authors=["Andrea Bellavia", "Runyu Zou", "Richelle D. Bjorvang", "Kristine Roos",
                  "Ylva Sjunnesson"], year=2022,
         family="decoy-wall1-mixture", provisional_cell="MIXTURE_UNSEPARABLE",
         provenance_channel="routing_decoy",
         note="Environ Res. Tests TWO walls at once: a mixture index spanning B.2 and B.6 families "
              "(Wall 1) measured in an ART population (Wall 4). The correct disposition is "
              "MIXTURE_UNSEPARABLE with the ART frame flagged, not admission to either chapter's "
              "pooled estimate."),
    dict(title="Oyster reproduction is affected by exposure to polystyrene microplastics",
         authors=["Rossana Sussarellu", "Marc Suquet", "Yoann Thomas", "Christophe Lambert",
                  "Caroline Fabioux"], year=2016,
         family="decoy-wall5-animal", provisional_cell="OFF_ANIMAL",
         provenance_channel="routing_decoy",
         note="PNAS. WALL 5 DECOY. Sits at the very top of the citation ranking for microplastics "
              "paired with reproduction and fecundity — this is the expected head of the ranking, "
              "not a tail risk, and the screen must check species on every record."),
    dict(title="Temporal trends in sperm count: a systematic review and meta-regression analysis",
         authors=["Hagai Levine", "Niels Jorgensen", "Anderson Joel Martino-Andrade",
                  "Jaime Mendiola", "Dan Weksler-Derri"], year=2017,
         family="decoy-wall7-trend", provisional_cell="OUTCOME_TREND_UNATTRIBUTED",
         provenance_channel="routing_decoy",
         note="Hum Reprod Update. WALL 7 DECOY: a measured decline in an outcome with NO exposure "
              "measured. It is the phenomenon B.2, B.6 and A.16 compete to explain, not evidence "
              "for any of them. SHADOW-GATE TEST CASE: a 'Re: Temporal Trends in Sperm Count' "
              "letter in J Urol and two 'Faculty Opinions recommendation of ...' records all share "
              "the title."),
    dict(title="The Minderoo-Monaco Commission on Plastics and Human Health",
         authors=["Philip J. Landrigan", "Herve Raps", "Maureen Cropper", "Caroline Bald",
                  "Manuel Brunner"], year=2023,
         family="commission", provisional_cell="PARAMETER_EXPOSURE",
         provenance_channel="hypothesis_canon",
         note="Ann Glob Health. What v5 means by its non-existent 'Lancet Commission on "
              "Reproductive Health (2025)'. DUPLICATE-RECORD GATE TEST CASE and the reason the "
              "gate exists: indexed at 10.5334/aogh.4056 (447 cites) AND 10.5334/aogh.4083 (41 "
              "cites), same title, year and venue, plus a 'Correction: ...' record at aogh.4331 "
              "that the shadow gate should catch separately."),
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
    url = _oa_auth(f"https://api.openalex.org/works?search={quote(title)}&per-page=20"
                   "&select=id,doi,title,publication_year,type,authorships,primary_location,"
                   "cited_by_count")
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
    key = f"B6DUP7::{title}::{year}::{is_book}::{'|'.join(cand.get('authors') or [])}"
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
        is_review = looks_like_review(it["title"], it["container"], cand.get("authors"))
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

    L = [f"# A3 cold-start anchors — {SLUG} (B.6)", "",
         f"Sourced in a live OpenAlex pass (2026-08-14) and resolved through five gates: "
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
         "NEW and, on this corpus, UNVALIDATED: the Minderoo-Monaco pair that motivated it turned out "
         "to be two different works sharing a title, separated correctly by the author gate. Zero "
         "here means the gate did not fire, not that it was confirmed. Each demotion, if any, names "
         "the copy kept, the copy set aside and both citation counts, so an RA can check the choice "
         "rather than take it on trust.", "",
         f"**Records refused as a review of the work, or on authorship: {n_review_rejected}.** Every "
         "refusal keeps its record in the JSON so the RA can audit what was refused rather than "
         "trusting that nothing was lost.", "",
         "## Coverage by estimand cell (verified / total)", ""]
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
          "- **Four gates, four distinct failures.** The existence gate catches ghosts: titles "
          "resolving to nothing. The version gate catches the mirror failure: a title resolving to a "
          "preprint, reprint or repository copy of the right work. The book-canon gate catches a "
          "real, correctly-titled, contemporaneous record of a *different* work — a review of the "
          "monograph. The shadow gate, added here, catches a fourth: a real, separately-DOI'd record "
          "whose title *contains* the target title behind a qualifier. None substitutes for another.",
          "- **The shadow gate was not designed in the abstract.** Five shadows sit on this chapter's "
          "own anchors, in four shapes: `Editorial Comment to ...` on Beeder and Samplaski 2019, "
          "`Faculty Opinions recommendation of ...` on Montejo et al. 2001 and Serretti and Chiesa "
          "2009, `Re: ...` on Tanrikut et al. 2009, and `Expression of Concern: ...` on Safarinejad "
          "2008. The Montejo case is the sharpest: neither index record of the study itself carries a "
          "DOI, while the Faculty Opinions record does, so a DOI-preferring resolver without this "
          "gate anchors a 1,022-patient incidence study to a one-paragraph post-publication comment.",
          "- **An integrity shadow is evidence, not noise.** The Expression of Concern on Safarinejad "
          "2008 is refused as an anchor and recorded as a flag on the anchor. A gate that merely "
          "refused it would have discarded the most consequential thing the index knows about one of "
          "this chapter's mechanism sources; risk of bias reads the flag before the effect size is "
          "used.",
          "- **Version-gate test cases are in the set deliberately.** Casilla-Lennon et al. has three "
          "co-existing records including a repository copy; Alwan et al. 2007 has three "
          "reprint-shaped twins in survey and yearbook venues, one of them credited to a different "
          "author entirely; Wilcox et al. 1995 has an *Obstetrical & Gynecological Survey* twin; Hull "
          "et al. 2004 carries two DOIs in one journal. A gate with nothing to catch has not been "
          "tested.",
          "- **The decoys carry the walls, not the topic.** Alwan et al. 2007 (Wall 4, pregnancy "
          "safety), Cesta et al. 2016 (Wall 5, ART), Haddad and Wieck 2004 (Wall 6, antipsychotics), "
          "Lister et al. 2009 (Wall 7, non-human), Power et al. 2013 (Wall 1, the disorder rather "
          "than the drug), and Clayton et al. 2004 (clinical management of the side effect) each sit "
          "just across one wall. Per the D.2.d finding, these are forward-cited like any other seed "
          "at A4: a decoy's citation neighbourhood is where the boundary cases live. The Clayton 2004 "
          "decoy shares an author with two link-1 anchors on purpose, so the routing test cannot be "
          "passed by author-based topical similarity.",
          "- **LINK2 has no anchor, and the gap is the point.** Two live probes for records estimating "
          "sexual dysfunction against coital frequency returned nothing on target. The scope document "
          "predicted the chain's second joint would be unmeasured; recording the absence keeps it "
          "visible instead of letting a link-1 record stand in for it.",
          "- **Three defects were found and fixed by auditing this script's own output**, which is "
          "why the run is recorded rather than merely reported, and all three were visible only in "
          "the *refused* set. (1) The shadow gate's general containment rule — candidate title "
          "appearing as a suffix of a record title — refused five records on the three-token anchor "
          "'Antipsychotic-Induced Hyperprolactinaemia', and every one was a distinct paper rather "
          "than a comment on this one. Suffix containment cannot tell a comment from a different "
          "work, and no token threshold fixes it; the rule was removed and the named-qualifier list "
          "kept. (2) Alwan et al. 2007 resolved to the *Obstetrical & Gynecological Survey* reprint "
          "rather than the NEJM original — the exact failure that candidate was planted to test. The "
          "original and the digest scored identically on every existing signal and the tie broke on "
          "list order, so republishing venues now carry an explicit penalty and ties are broken by a "
          "stated rule. (3) That fix immediately created its own regression, moving Serretti and "
          "Chiesa 2009 from the journal article to a European Psychiatry conference abstract, "
          "because the new tie-break's last term was DOI string order. Deterministic and wrong is "
          "not an improvement on accidentally right; title fit was added ahead of it, which is a "
          "term that means something.",
          "- **LEAKAGE WALL.** Beeder and Samplaski 2019 and Serretti and Chiesa 2009 enter as "
          "channel-1 review seeds. Their search strategies must NOT be mined for A6 query terms, "
          "since their included studies feed anchors here.",
          "- **Empirical recall denominator.** Only the `PRIMARY_*` anchors count. The link-support, "
          "mechanism, parameter, measurement and theory anchors are indispensable to the chapter\'s "
          "demographic-significance computation and to its mechanism section, and they are not "
          "evidence for the causal claim; scoring recall against them would measure the wrong thing "
          "(scope doc, Call 4)."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} year_drift={n_drift} flagged={n_flagged} no_doi={n_book} "
          f"shadows={n_shadow} integrity={n_integrity} review_or_author_refusals={n_review_rejected} "
          f"total={len(anchors)}")
    print("by cell:", {k: f"{sum(v)}/{len(v)}" for k, v in by_cell.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
