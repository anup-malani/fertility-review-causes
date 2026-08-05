#!/usr/bin/env python3
r"""
d1a_relevance.py — the ONE definition of snowball relevance for D.1.a. No network, no I/O.

Relevance here means "on the treatment x outcome pair", per the PI-relayed definition recorded on
TICK-062: a hypothesis is a treatment x outcome pair, so a record is on-pair when the blob carries a
value-measure term AND a fertility-outcome term. This is a FRAME filter feeding the saturation
statistic, not the router -- it decides what counts as a relevant record for the yield denominator,
and it is deliberately more permissive than the eventual screening walls.

Extracted from 93_d1a_snowball_r1.py, which held the only copy. Round 2 needed the same filter and
"two definitions is how they drift" was already the stated reason 94 imported from 93 rather than
re-typing. A third consumer is the point at which that stops being tenable, so it lives here and 93
imports it. 93's docstring keeps the round-1 bug history; the patterns are here.

VERSION HISTORY -- every entry is a defect a hand read found, and the aggregate never showed any of
them. This is the chapter's running demonstration that a relevance filter is read, not trusted.

  v1 (2026-08-03, in 93). Wrong in BOTH directions at once, which is why the yield looked reasonable.
    Bug A, false positives: `reproduc\w+` admitted SOCIAL reproduction and REPRODUCTIVE HEALTH; it
    scored Bourdieu's *Reproduction in Education, Culture and Society* as on-pair. Narrowed to the
    phrases that actually denote fertility.
    Bug B, false negatives: quoted phrases were carried from OpenAlex query syntax into a Python
    verbose regex, so `"second\s+demographic\s+transition"` matched only text containing literal
    double-quote characters and the chapter's most central phrase never matched anything.
    Net 79 -> 86 relevant, 1.63 -> 1.77 per 50. Six removed, thirteen gained; the errors partially
    cancelled and the summary statistic was the last place either would have shown up.

  v2 (2026-08-04, here). A third class, found by the hand read of v1's own corrected admitted set --
    the audit sample 94 wrote and told the next reader to read before quoting the yield.
    Bug C: `culture|cultural` matches DESIGN AND THEORY DESCRIPTORS, where the word describes how the
    study was conducted rather than what it measured. `cross-cultural` is a sampling frame,
    `cultural evolutionary` is a theoretical tradition, and neither is a value measure. It admitted
    "Sociosexual orientation, life history strategy, and reproductive success: A large-scale
    cross-cultural study" (treatment: sociosexual orientation, an evolutionary-psychology construct
    that is not this chapter's) and a cultural-evolution paper on kin networks.
    Seventeen of the 86 v1-relevant records hung on `culture`/`cultural` alone, so the exposure was
    a fifth of the frame even though only two records were actually wrong.

    THE FIX HAD TO BE SCOPED, AND THE NAIVE VERSION WAS TESTED AND REJECTED. Excluding any record
    containing a design descriptor drops "Introduction to Special Section for Journal of
    Cross-Cultural Psychology: Value of Children" -- which is squarely on-pair, and whose descriptor
    is in the VENUE NAME. So the fix for a false-positive class manufactures a false-negative class:
    the same both-directions-at-once shape as v1, this time inside a single one-line fix.

  v3 (2026-08-04, here). v2's own fix, over-scoped, caught by the round-2 hand read at 14x the sample
    size. v2 treated `socio-cultural` and `cultural evolution` as design descriptors alongside
    `cross-cultural`. At round-1 scale that decision touched 3 records and looked right. At round-2
    scale it touched 43, and reading them showed roughly half were on-pair records being thrown away:
    "Socio-Cultural Practices and Fertility Behavior among Banyankole Families", "How socio-cultural
    factors and opportunity costs shape the transition to a third child", "'Children are a blessing
    from god': a qualitative study exploring the socio-cultural factors", "The cultural evolution of
    fertility decline".

    The distinction v2 missed: `cross-cultural` describes the SAMPLE (a study run across cultures),
    while `socio-cultural` is an ordinary adjective meaning "social and cultural" and is routinely the
    thing being measured. `cultural evolution` reads as a theoretical tradition in the abstract, but
    in fertility research it names cultural transmission of fertility norms -- a treatment. Both are
    removed from the idiom list; only genuine sampling-frame descriptors remain.

    THE GENERAL LESSON, AND IT IS THE MOST TRANSFERABLE THING IN THIS FILE. Each version of this
    filter was validated on the sample available when it was written, and each was wrong in a way that
    only appeared at the next order of magnitude. v1 was audited on 45 records and shipped two bugs.
    v2 was validated on the 3 records its change touched and shipped a false-negative class that
    needed 43 records to become visible. A fix verified on the cases that motivated it has been
    verified against nothing -- the sample that produced the hypothesis cannot also test it.

STRIP-THEN-REMATCH. v1 handled its one known idiom (`secular trend`, a demography term of art for a
long-run trend with no religious content) with a special case that inspected only the FIRST treatment
match and happened to be correct by luck. v2 replaces it with the general operation the idiom problem
actually calls for: DELETE the idiom spans from the blob, then test the remainder. A record survives
if a treatment term survives, so the JCCP record is admitted on `Value of Children` after the venue's
`Cross-Cultural` is removed, and no per-idiom special case is needed for the next one found.
"""
import re

VERSION = 3

# Value-measure terms. WORD-BOUNDARY ANCHORED, deliberately: the C.2.c run's headline failure was a
# filter matching bare `hous` and `rent`, which scored hOUSEhold, paRENT and diffeRENT as housing
# terms, made 58% of that frame false positives, and turned a converging snowball into a
# non-converging one. D.1.a's near-misses are worse, not better -- `value` matches evaluation,
# `individual` matches "individual-level", `material` matches materials science.
TREATMENT = re.compile(r"""\b(
    religio\w* | secular(?:ism|ization|isation|ity)\b | church\w* | denominational?\b | faith\b |
    postmaterialis\w* | post-materialis\w* | individualism\b | individualist\w* |
    individuali[sz]ation\b | collectivism\b | autonomy\b | kinship\b |
    ideational\b | second\s+demographic\s+transition | consumerism\b | materialism\b |
    values?\b | norms?\b | culture\b | cultural\b | attitudes?\b | belief\w*
)""", re.I | re.X)

# Fertility-outcome terms. `reproduc\w+` is NOT here; see bug A.
OUTCOME = re.compile(r"""\b(
    fertility\b | fertilit\w+ | birth\b | births\b | birthrate\b | childbearing\b | childless\w* |
    childfree\b | parity\b | natality\b | family\s+size | number\s+of\s+children |
    tfr\b | nuptialit\w+ | procreat\w+ |
    reproductive\s+(?:behavio\w+|success|intention\w*|decision\w*|career|outcome\w*)
)""", re.I | re.X)

# Spans that LOOK like treatment terms but describe the study rather than what it measured. Deleted
# from the blob before matching, never used to reject a record outright -- see bug C.
#
# THE LIST IS DELIBERATELY SHORT AND ONLY HOLDS SAMPLING FRAMES. `socio-cultural` and
# `cultural evolution` were here in v2 and are gone: the first is an ordinary adjective for the thing
# being measured ("Socio-Cultural Practices and Fertility Behavior"), the second names cultural
# transmission of fertility norms, which is this chapter's treatment ("The cultural evolution of
# fertility decline"). Anything added here must describe HOW THE STUDY WAS RUN, not what it is about.
IDIOM = re.compile(r"""(
    secular\s+(?:trend|decline|increase|change\s+in\s+height)  |  # demography term of art
    cross[-\s]cultural  |  intercultural  |  multicultural        # sampling frames
)""", re.I | re.X)


def relevant(rec):
    """(is_relevant, reason) for a pool record. Requires BOTH axes -- the treatment x outcome test."""
    blob = f"{rec.get('title', '')} {rec.get('venue', '')}"
    if not blob.strip():
        return False, "no title"
    stripped = IDIOM.sub(" ", blob)
    t, o = TREATMENT.search(stripped), OUTCOME.search(stripped)
    if t and o:
        return True, f"treatment={t.group(0)}; outcome={o.group(0)}"
    if not t:
        # Distinguish "never had a treatment term" from "had only a design descriptor". The second is
        # a real finding about the record, and collapsing them hides what the idiom strip is doing.
        if TREATMENT.search(blob):
            return False, f"treatment term is a design descriptor only ({IDIOM.search(blob).group(0).strip()})"
        return False, "no treatment term"
    return False, "no outcome term"
