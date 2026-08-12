#!/usr/bin/env python3
"""
124_b7_cold_start_anchors.py — B.7 (antidepressants / pharmacological subfecundity), stage A3.

Inherits `116_b5_cold_start_anchors.py` unchanged in its resolver and its first three gates, and adds
a fourth that this chapter's literature makes necessary. Four gates, all mandatory, each catching a
failure the others structurally cannot:

  * EXISTENCE gate (OAS, 2026-07-08). No anchor enters a recall denominator without a live DOI or a
    Crossref/OpenAlex record confirming the title exists. Catches ghosts: titles resolving to nothing.
  * VERSION-OF-RECORD gate (D.1.b, 2026-08-07). Candidates are RANKED for version-of-record status
    rather than taken at the title argmax. Catches a title resolving to something real that is not
    the record meant — a preprint, working paper, reprint, repository copy, or chapter.
  * BOOK-CANON gate (D.2.d, 2026-08-08). Catches a real, correctly-titled, contemporaneous record of
    a DIFFERENT work: a review OF a monograph. Retained rather than removed — B.7's canon is
    journal-shaped, so this gate has little to do here and is kept only so the inheritance stays
    honest.
  * SHADOW-RECORD gate (NEW, B.7, 2026-08-12). Catches something none of the three above sees: a
    real, indexed, separately-DOI'd record whose title is the target title plus a leading qualifier.
    It passes the existence gate (it exists), the version gate (it is not a preprint), and the
    book gate (it is not a review of a book), and it resolves at overlap 1.0.

The shadow gate is not speculative. The live sourcing pass (2026-08-12) found four distinct shapes of
it sitting on this chapter's most important anchors:

    Beeder & Samplaski 2019  -> "Editorial Comment to Effect of antidepressant medications on ..."
    Montejo et al. 2001      -> "Faculty Opinions recommendation of Incidence of sexual dysfunc..."
    Serretti & Chiesa 2009   -> "Faculty Opinions recommendation of Treatment-emergent sexual d..."
    Tanrikut et al. 2009     -> "Re: Adverse Effect of Paroxetine on Sperm"  (J Urol letter)
    Safarinejad 2008         -> "Expression of Concern: Sperm DNA Damage and Semen Quality Imp..."

The last of those is not only a resolver hazard. An Expression of Concern is a fact about the anchor,
so the gate records an `integrity_flag` on the anchor rather than merely refusing the shadow, and the
flag is carried into extraction and risk of bias. Silently dropping the shadow would have discarded
the single most consequential thing the index knows about one of this chapter's mechanism anchors.

Same standing discipline as the predecessors:
  * Candidates carry (title, authors, year, family, provisional_cell, provenance_channel) from a LIVE
    OpenAlex sourcing pass (2026-08-12). They assert NO DOIs; the DOI is whatever the resolver
    returns for a ranked match. Author lists are live-sourced too — author lists asserted from memory
    have been wrong every time they were checked, and were wrong again this run: HYPOTHESES-v5 cites
    the male-fertility review as "Beeder and Bhatt (2025)", and the record is Beeder and Samplaski,
    International Journal of Urology, 2019.
  * Three-state discipline: a network failure is UNCONFIRMED, never ABSENT. An empty API result is
    never cached, because caching one turns a rate-limited call into a permanent "does not exist".
  * OpenAlex is called with the funded api_key from .env. `mailto` alone is not authentication.

Deliberate gate test cases in the candidate set, included because a gate with nothing to catch is a
gate that has not been tested: Casilla-Lennon et al. has three co-existing records (AJOG 2016,
Fertility and Sterility 2015, and a UNC repository copy); Alwan et al. 2007 has three reprint-shaped
twins in survey and yearbook venues; Wilcox et al. 1995 has an Obstetrical & Gynecological Survey
twin; Hull et al. 2004 is double-DOI'd in one journal; Montejo et al. 2001 and Pratt et al. 2017
carry no DOI at all.

**LINK2 has no anchor and that is a result, not an omission.** Two live probes for records estimating
sexual dysfunction -> coital frequency returned nothing on target. The scope document predicted the
chain's second joint would be the unmeasured one; the anchor set records the absence explicitly
rather than substituting a link-1 record and letting the gap disappear.

SCRIPT NUMBERING: 88 is the highest on `main`, but the unmerged branches collide — D.1.a holds
95-115, D.1.b 95-102, D.2.d 103-108, B.5 115-122 — so 103-115 is claimed three times over. This run
starts above every number in use on any branch. 123 is the reconnaissance probe and this is 124.

Output: literature/search-logs/{slug}-cold-start-anchors.json
        literature/search-logs/{slug}-cold-start-anchors-log.md
"""
import json, os, re, subprocess, time
from urllib.parse import quote

SLUG = "antidepressants-ssri-subfecundity"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b7_crossref_cache.json")
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


# --- Candidate anchors. Live-sourced 2026-08-12. NO DOIs asserted here by design. ---
CANDIDATES = [
    # === PRIMARY_MEDICATION_TO_FERTILITY — the identification-bearing cell ===
    dict(title="The effect of antidepressants on fertility",
         authors=["Marianne Casilla-Lennon", "Samantha Meltzer-Brody", "Anne Z. Steiner"], year=2016,
         family="primary-female", provisional_cell="PRIMARY_MEDICATION_TO_FERTILITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Am J Obstet Gynecol. The only human record the reconnaissance located that estimates "
              "antidepressant exposure against a female fertility quantity. VERSION-GATE TEST CASE "
              "and the hardest in the set: three co-existing records share this title — an AJOG 2016 "
              "article, a Fertility and Sterility 2015 record with a different author list, and a UNC "
              "repository copy at 10.17615/w7rn-zb69. The resolver must return the AJOG record."),
    dict(title="Use of selective serotonin reuptake inhibitors reduces fertility in men",
         authors=["Lynette Norr", "Birgit Egedal Bennedsen", "Jens Fedder", "Erik Roj Larsen"],
         year=2016, family="primary-male", provisional_cell="PRIMARY_MALE_FECUNDITY",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Andrology. The chapter's best-identified primary anchor and the one HYPOTHESES-v5 "
              "cites correctly. Male stratum, which is where the measured fertility evidence sits."),
    dict(title="Effect of antidepressant medications on semen parameters and male fertility",
         authors=["Lauren Beeder", "Mary K. Samplaski"], year=2019, family="primary-male",
         provisional_cell="ENDOCRINE_MECHANISM",
         provenance_channel="channel1_review_seed",
         note="Int J Urol. HYPOTHESES-v5 cites this as 'Beeder and Bhatt PMC scoping review (2025)'; "
              "authors, venue and year are all wrong in v5 (Call 5). SHADOW-GATE TEST CASE: the "
              "index carries 'Editorial Comment to Effect of antidepressant medications on semen "
              "parameters and male fertility' under a different author at its own DOI. LEAKAGE WALL "
              "applies — its search strategy must not be mined for A6 query terms."),

    # === LINK1_MEDICATION_TO_SEXUAL_FUNCTION ===
    dict(title="Prevalence of Sexual Dysfunction Among Newer Antidepressants",
         authors=["Anita H. Clayton", "James F. Pradko", "Harry A. Croft", "C. Brendan Montano"],
         year=2002, family="link1", provisional_cell="LINK1_MEDICATION_TO_SEXUAL_FUNCTION",
         provenance_channel="hypothesis_canon",
         note="J Clin Psychiatry. Named in HYPOTHESES-v5's seminal list and verified here."),
    dict(title="Incidence of sexual dysfunction associated with antidepressant agents: a prospective multicenter study of 1022 outpatients",
         authors=["Angel L. Montejo", "Gines Llorca", "Juan Izquierdo", "Fernando Rico-Villademoros"],
         year=2001, family="link1", provisional_cell="LINK1_MEDICATION_TO_SEXUAL_FUNCTION",
         expect_no_doi=True,
         provenance_channel="direct_empirical_bibliographic_search",
         note="J Clin Psychiatry 62 Suppl 3:10-21. The direct-questioning incidence study, and the "
              "reason ASCERTAINMENT is an extraction field: measured incidence here is several times "
              "the spontaneously-reported rate. Two index records, NEITHER carrying a DOI. "
              "SHADOW-GATE TEST CASE: a 'Faculty Opinions recommendation of ...' record exists at "
              "10.3410/f.718446934.793496193 and is the only same-title record that HAS a DOI, so a "
              "resolver without the shadow gate anchors this study to a post-publication review."),
    dict(title="Treatment-Emergent Sexual Dysfunction Related to Antidepressants",
         authors=["Alessandro Serretti", "Alberto Chiesa"], year=2009, family="link1",
         provisional_cell="LINK1_MEDICATION_TO_SEXUAL_FUNCTION",
         provenance_channel="channel1_review_seed",
         note="J Clin Psychopharmacol. The link-1 meta-analysis, with agent-by-agent rates. SHADOW "
              "and VERSION test case: an abstract twin in European Psychiatry, a conference-poster "
              "twin, and a Faculty Opinions record all share the title. LEAKAGE WALL applies."),
    dict(title="Antidepressant-Induced Sexual Dysfunction During Treatment With Moclobemide, Paroxetine, Sertraline, and Venlafaxine",
         authors=["Sidney H. Kennedy", "Beata S. Eisfeld", "Susan E. Dickens", "Jason R. Bacchiochi",
                  "R. Michael Bagby"], year=2000, family="link1",
         provisional_cell="LINK1_MEDICATION_TO_SEXUAL_FUNCTION",
         provenance_channel="direct_empirical_bibliographic_search",
         note="J Clin Psychiatry. Within-agent comparison with a measured pre-treatment baseline."),

    # === The pre-treatment baseline — Wall 1's counterfactual, measured ===
    dict(title="Sexual dysfunction before antidepressant therapy in major depression",
         authors=["Sidney H. Kennedy", "Susan E. Dickens", "Beata S. Eisfeld", "R. Michael Bagby"],
         year=1999, family="baseline", provisional_cell="INDICATION_BASELINE_D3A",
         provenance_channel="direct_empirical_bibliographic_search",
         note="J Affect Disord. The record that makes Wall 1 operational rather than rhetorical: "
              "sexual dysfunction is already prevalent in untreated major depression, so a "
              "medicated-versus-healthy contrast attributes the disorder's effect to the drug."),
    dict(title="Fecundity of Patients With Schizophrenia, Autism, Bipolar Disorder, Depression, Anorexia Nervosa, or Substance Abuse vs Their Unaffected Siblings",
         authors=["Robert A. Power", "Simon Kyaga", "Rudolf Uher", "James H. MacCabe",
                  "Niklas Langstrom"], year=2013, family="baseline",
         provisional_cell="INDICATION_BASELINE_D3A",
         provenance_channel="routing_decoy",
         note="JAMA Psychiatry. Swedish register, sibling-controlled: the disorder's own fertility "
              "effect, which is D.3.a's estimand and the quantity B.7 must net out. YEAR-DRIFT TEST "
              "CASE: the index dates it 2012 against a 2013 DOI stem."),

    # === LINK3_COITAL_TO_CONCEPTION — borrowed from A.14, no recall credit ===
    dict(title="Timing of Sexual Intercourse in Relation to Ovulation - Effects on the Probability of Conception, Survival of the Pregnancy, and Sex of the Baby",
         authors=["Allen J. Wilcox", "Clarice R. Weinberg", "Donna D. Baird"], year=1995,
         family="link3", provisional_cell="LINK3_COITAL_TO_CONCEPTION",
         provenance_channel="sibling_hypothesis_parameter",
         note="NEJM. The parameter that decides how much of a desire decrement survives into a "
              "conception decrement, and the source of the non-linearity Wall 2 turns on. "
              "VERSION-GATE TEST CASE: an Obstetrical & Gynecological Survey 1996 twin exists."),
    dict(title="The risk of conception on different days of the menstrual cycle",
         authors=["John C. Barrett", "John Marshall"], year=1969, family="link3",
         provisional_cell="LINK3_COITAL_TO_CONCEPTION",
         provenance_channel="sibling_hypothesis_parameter",
         note="Population Studies. The demographic-side statement of the same parameter, and the one "
              "the review's own literature will cite."),

    # === ENDOCRINE_MECHANISM ===
    dict(title="Adverse effect of paroxetine on sperm",
         authors=["Cigdem Tanrikut", "Adam S. Feldman", "Margaret Altemus", "Darius A. Paduch",
                  "Peter N. Schlegel"], year=2009, family="mechanism-semen",
         provisional_cell="ENDOCRINE_MECHANISM",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Fertil Steril. SHADOW-GATE TEST CASE, two shapes at once: a J Urol letter titled "
              "'Re: Adverse Effect of Paroxetine on Sperm' and a Faculty Opinions record."),
    dict(title="Sperm DNA Damage and Semen Quality Impairment After Treatment With Selective Serotonin Reuptake Inhibitors Detected Using Semen Analysis and Sperm Chromatin Structure Assay",
         authors=["Mohammad Reza Safarinejad"], year=2008, family="mechanism-semen",
         provisional_cell="ENDOCRINE_MECHANISM",
         provenance_channel="direct_empirical_bibliographic_search",
         note="J Urol. INTEGRITY FLAG: the index carries a 2023 'Expression of Concern' record for "
              "this article in the same journal. The shadow gate refuses the EoC record as an anchor "
              "and records the flag on this one; risk of bias must read it before this study's "
              "effect size is used."),
    dict(title="Antidepressant-Associated Changes in Semen Parameters",
         authors=["Cigdem Tanrikut", "Peter N. Schlegel"], year=2007, family="mechanism-semen",
         provisional_cell="ENDOCRINE_MECHANISM",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Urology. VERSION-GATE TEST CASE: a 2008 Fertility and Sterility record carries the "
              "same title under an expanded author list."),

    # === THEORY_SEROTONERGIC ===
    dict(title="Dopamine and serotonin: influences on male sexual behavior",
         authors=["Elaine M. Hull", "John W. Muschamp", "Satoru Sato"], year=2004, family="theory",
         provisional_cell="THEORY_SEROTONERGIC", provenance_channel="hypothesis_canon",
         note="Physiol Behav. The mechanism statement B.7's 'why' paragraph paraphrases. DUPLICATE- "
              "RECORD TEST CASE: two DOIs in the same journal for the same article."),

    # === PARAMETER_PREVALENCE — what the significance computation multiplies ===
    dict(title="National Patterns in Antidepressant Medication Treatment",
         authors=["Mark Olfson", "Steven C. Marcus"], year=2009, family="prevalence",
         provisional_cell="PARAMETER_PREVALENCE",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Arch Gen Psychiatry. The US treatment-prevalence series."),
    dict(title="Antidepressant Use among Persons Aged 12 and Over: United States, 2011-2014",
         authors=["Laura A. Pratt", "Debra J. Brody", "Qiuping Gu"], year=2017, family="prevalence",
         provisional_cell="PARAMETER_PREVALENCE", expect_no_doi=True,
         provenance_channel="statistical_agency_source",
         note="NCHS Data Brief 283. Carries NO DOI, which is expected for an agency series and is "
              "why expect_no_doi exists. This is the age-and-sex-specific prevalence figure the "
              "demographic-significance computation runs on, and it is a statistical publication "
              "rather than a study — the distinction is recorded so the chapter does not treat an "
              "agency estimate as evidence for the causal claim."),

    # === PARAMETER_DETERMINANT_TO_LOSS — cross-filed to B.5 under Wall 3 ===
    dict(title="Use of antidepressants during pregnancy and the risk of spontaneous abortion",
         authors=["Hamid Reza Nakhai-Pour", "Perrine Broy", "Anick Berard"], year=2010,
         family="loss-parameter", provisional_cell="PARAMETER_DETERMINANT_TO_LOSS",
         provenance_channel="routing_decoy",
         note="CMAJ. Sits exactly on Wall 3: B.7's treatment, B.5's channel, no fertility outcome. "
              "Cross-filed to B.5 and counted toward neither chapter's causal recall. GHOST-CHECK "
              "NOTE: the first reconnaissance pass could not resolve this study from a remembered "
              "title and it resolved on the second pass under different wording — an unresolved "
              "title is a wrong memory, not an absent literature."),

    # === MEASUREMENT_ASCERTAINMENT ===
    dict(title="The ELIXIR study: evaluation of sexual dysfunction in 4557 depressed patients in France",
         authors=["M. Bonierbale", "Christophe Lancon", "Jean Tignol"], year=2003,
         family="ascertainment", provisional_cell="MEASUREMENT_ASCERTAINMENT",
         provenance_channel="direct_empirical_bibliographic_search",
         note="Curr Med Res Opin. Large systematic-inquiry ascertainment, against which "
              "spontaneous-report rates can be benchmarked."),

    # === ROUTING DECOYS — one per wall, forward-cited like any other seed at A4 ===
    dict(title="Use of Selective Serotonin-Reuptake Inhibitors in Pregnancy and the Risk of Birth Defects",
         authors=["Sura Alwan", "Jennita Reefhuis", "Sonja A. Rasmussen", "Richard S. Olney",
                  "Jan M. Friedman"], year=2007, family="decoy-pregnancy-safety",
         provisional_cell="OFF_PREGNANCY_SAFETY", provenance_channel="routing_decoy",
         note="NEJM. Wall 4, and the paradigm of the largest cell in the corpus. VERSION-GATE TEST "
              "CASE with three twins: Obstetrical & Gynecological Survey, a Yearbook digest under a "
              "different author, and Survey of Anesthesiology."),
    dict(title="Depression, anxiety, and antidepressant treatment in women: association with in vitro fertilization outcome",
         authors=["Carolyn E. Cesta", "Alexander Viktorin", "Henrik Olsson", "Viktoria Johansson"],
         year=2016, family="decoy-art", provisional_cell="OFF_ART_A17",
         provenance_channel="routing_decoy",
         note="Fertil Steril. Wall 5. Also the closest thing in the literature to a design that "
              "separates the disorder from the medication, which is why it is a decoy rather than an "
              "exclusion: it may be admissible as PARAMETER_HAZARD_CLINICAL at full text."),
    dict(title="Antipsychotic-Induced Hyperprolactinaemia",
         authors=["Peter Haddad", "Angelika Wieck"], year=2004, family="decoy-psychotropic",
         provisional_cell="ADJACENT_PSYCHOTROPIC", provenance_channel="routing_decoy",
         note="Drugs. Wall 6 and Call 3: a mechanistically stronger fecundity pathway than anything "
              "serotonergic, at lower prevalence. TITLE-COLLISION TEST CASE: a 2011 ANZ J Psychiatry "
              "article carries the identical title under different authors."),
    dict(title="Inhibition of egg production in zebrafish by fluoxetine and municipal effluents: A mechanistic evaluation",
         authors=["Andrea Lister", "Christine Regan", "Jessica Van Zwol", "Glen Van Der Kraak"],
         year=2009, family="decoy-animal", provisional_cell="OFF_ANIMAL",
         provenance_channel="routing_decoy",
         note="Aquat Toxicol. Wall 7, and not a token decoy: on the fecundity-term probes this "
              "literature outranks the human work on citations, so the screen is tested against the "
              "material that actually occupies the top of the ranking."),
    dict(title="A Placebo-Controlled Trial of Bupropion SR as an Antidote for Selective Serotonin Reuptake Inhibitor-Induced Sexual Dysfunction",
         authors=["Anita H. Clayton", "Julia K. Warnock", "Susan G. Kornstein", "Relana Pinkerton"],
         year=2004, family="decoy-clinical", provisional_cell="OFF_CLINICAL_MANAGEMENT",
         provenance_channel="routing_decoy",
         note="J Clin Psychiatry. Treating the side effect rather than measuring its consequence. "
              "Shares an author with two link-1 anchors, so the decoy tests routing rather than "
              "author-based topical similarity."),
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
SHADOW_QUALIFIERS = (
    (r"^editorial\s+comment\s+(to|on)\b", "commentary"),
    (r"^faculty\s+opinions?\s+recommendation\s+of\b", "commentary"),
    (r"^re\s*:", "commentary"),
    (r"^comment\s+on\b", "commentary"),
    (r"^response\s+to\b", "commentary"),
    (r"^discussion\s+of\b", "commentary"),
    (r"^abstract\s+of\b", "commentary"),
    (r"^reply\s+to\b", "commentary"),
    (r"^in\s+reply\b", "commentary"),
    (r"^author'?s?\s+response\b", "commentary"),
    (r"^letter\s+(to\s+the\s+editor\s+)?(re|regarding|concerning)\b", "commentary"),
    (r"^correspondence\s+(on|regarding)\b", "commentary"),
    (r"^expressions?\s+of\s+concern\b", "integrity"),
    (r"^retraction\b", "integrity"),
    (r"^corrections?\s+(to|for)\b", "integrity"),
    (r"^erratum\b", "integrity"),
    (r"^reprint\s+of\b", "version"),
)


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
    key = f"B7SHADOW3::{title}::{year}::{is_book}::{'|'.join(cand.get('authors') or [])}"
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
    scored.sort(key=lambda r: (-r["score"], -r["jaccard"], is_reprint_venue(r.get("container")),
                               r.get("cr_year") or 9999, r.get("doi") or ""))
    best = scored[0]
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
    anchors, log = [], []
    n_verified = n_flagged = n_book = n_drift = n_review_rejected = 0
    n_shadow = n_integrity = 0
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

    L = [f"# A3 cold-start anchors — {SLUG} (B.7)", "",
         f"Sourced in a live OpenAlex pass (2026-08-12) and resolved through four gates: "
         f"{len(anchors)} candidate anchors, of which {len(empirical)} are empirical primary-cell "
         "anchors (the causal recall denominator) and the rest are link-support, mechanism, "
         "parameter, measurement, theory, or routing-decoy anchors that earn no empirical recall "
         "credit. No DOI is hand-asserted; each is the top-ranked version-of-record candidate from a "
         "unified Crossref + OpenAlex field, then re-affirmed at doi.org.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Year-drift keep (real, RA-confirm): {n_drift}**  ·  "
         f"**Flagged for RA: {n_flagged}**  ·  **Expected index miss (no DOI by nature): {n_book}**", "",
         f"**Shadow records refused: {n_shadow}** across {len([a for a in anchors if a.get('shadows_refused')])} "
         f"anchors — the new gate firing.  **Integrity flags raised: {n_integrity}.**", "",
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
