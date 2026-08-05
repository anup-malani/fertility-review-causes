#!/usr/bin/env python3
"""
d1a_titles.py — the ONE set of title-matching primitives for D.1.a. No network, no I/O.

Third shared module on this chapter, extracted for the reason the first two were: `95_` and `99_` both
need to decide whether a retrieved record is the work that was asked for, and two copies of a matching
rule is how they drift. The relevance filter and the fetcher each shipped a bug that lived in a
duplicated copy; this one is extracted before that happens rather than after.

TWO METRICS, BECAUSE ONE IS NOT ENOUGH AND THE FAILURE IS ASYMMETRIC.

  jaccard(a, b)   — shared tokens over the UNION. The default identity test. Its blind spot is any
                    case where one string legitimately carries tokens the other never had, because
                    those tokens inflate the denominator. It scored Hagestad and Call 2007 at 0.43 --
                    under the 0.55 gate -- purely because the query title carried a subtitle the index
                    had dropped, and would have recorded a real v5 seminal work as nonexistent.

  containment(a,b)— shared tokens over the SHORTER string. Reads "is one of these essentially inside
                    the other", which is the right question for subtitle drops and, in `99_`, for a
                    Crossref reference-list entry that stored a whole citation string where the title
                    should be: "Jeffery, P., & Jeffery, R. (2000). Religion and fertility in India.
                    Economic and Political Weekly, 35(35)". Jaccard against that is hopeless; the real
                    title's tokens are almost entirely contained in it.

CONTAINMENT ALONE IS NOT AN IDENTITY TEST AND MUST NEVER BE USED AS ONE. Short generic titles are
contained in enormous numbers of strings -- "Religion and fertility" sits inside dozens of the
citation strings in this frame alone, belonging to different papers by different authors in different
decades. So `containment_match` requires corroboration: a minimum number of content tokens, and an
agreeing year where one can be recovered. That is the same discipline as `95_`'s subtitle gate, which
accepts a sub-threshold Jaccard only when BOTH author surname and year match exactly.
"""
import re

STOPWORDS = frozenset(
    "the a an of and in on for from to its by is with as at or be this that these those".split())


def tokens(t):
    return set(re.findall(r"[a-z0-9]+", re.sub(r"<[^>]+>", " ", (t or "").lower())))


def content_tokens(t):
    return tokens(t) - STOPWORDS


def jaccard(a, b):
    A, B = tokens(a), tokens(b)
    return len(A & B) / len(A | B) if A and B else 0.0


def containment(a, b):
    """Shared tokens over the shorter of the two token sets."""
    A, B = tokens(a), tokens(b)
    return len(A & B) / min(len(A), len(B)) if A and B else 0.0


def year_in(s):
    """The most plausible publication year mentioned in a string, or None.

    Reference strings carry volume numbers, page ranges and issue numbers that look like years to a
    naive `\\d{4}`. Restricted to a range that is plausible for this literature and preferring a
    parenthesised year, which is what a citation format actually uses.
    """
    m = re.search(r"\((1[6-9]\d{2}|20[0-2]\d)\)", s or "")
    if m:
        return int(m.group(1))
    yrs = [int(y) for y in re.findall(r"\b(1[6-9]\d{2}|20[0-2]\d)\b", s or "")]
    return yrs[0] if yrs else None


def containment_match(candidate_title, source_string, cand_year=None,
                      min_contain=0.80, min_content_tokens=4, year_tol=1):
    """Is `candidate_title` the work that `source_string` refers to?

    Returns (bool, containment, reason). Requires containment AND enough content to be discriminating
    AND, when a year is recoverable from the source string, agreement on it. Any one of those alone
    admits the wrong paper.
    """
    c = containment(candidate_title, source_string)
    nct = len(content_tokens(candidate_title))
    if nct < min_content_tokens:
        return False, c, f"title too short to be discriminating ({nct} content tokens)"
    if c < min_contain:
        return False, c, f"containment {c:.2f} below {min_contain}"
    sy = year_in(source_string)
    if sy is not None and cand_year is not None and abs(sy - cand_year) > year_tol:
        return False, c, f"year mismatch: source says {sy}, candidate is {cand_year}"
    return True, c, ("contained, year agrees" if sy else "contained, no year in source to check")
