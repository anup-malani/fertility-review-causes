#!/usr/bin/env python3
"""
textnorm.py — the canonical title/name normaliser for every stage of the search pipeline.

WHY THIS FILE EXISTS. `norm()` was copied into each chapter's scripts by hand, and it carried a
defect that silently refused correct anchors. Found on C.3.g (TICK-073, `201_`), where it cost 3 of
24 anchors including the chapter's most-cited primary-cell work; 12 inherited copies on `main` had
it. A function that decides whether two titles are the same work should exist once.

THE TWO DEFECTS IT FIXES, both of which are silent and both of which produce CONFIDENT WRONG
ANSWERS rather than errors:

1. ACCENT SHATTERING (found on D.3.c). The original ran `re.sub(r"[^a-z0-9 ]", " ", s.lower())` with
   no folding, replacing each non-ASCII character with a SPACE — so it did not merely fail to match
   an accented name, it SHATTERED it, and `surnames()` then took the last fragment:

       "Zsolt Speder"  vs index "Zsolt Spéder"  -> "speder"  vs "der"
       "Susanne Fahlen" vs index "Susanne Fahlén" -> "fahlen" vs "n"

   The author gate then returned False — "this record HAS authors and none is ours" — a confident
   wrong negative rather than a missing-data None.

2. ASYMMETRIC PUNCTUATION (found on C.3.g). An ASCII apostrophe survives NFKD and is then turned
   into a SPACE, splitting one token in two; a curly apostrophe is non-ASCII, so
   `encode("ascii","ignore")` DELETES it and the token stays whole. Indexes store the curly form and
   a hand-written candidate carries the straight one:

       candidate "Can't afford a baby" -> "can t afford a baby"   (5 tokens)
       index     "Can’t afford a baby" -> "cant afford a baby"    (4 tokens)

   Jaccard 0.70 against a 0.72 floor: refused, and reported as NO-MATCH, which reads as an absent
   work. The dash class fails in mirror — an ASCII hyphen becomes a space while U+2010 is deleted,
   so "Tuition-Free" and "Tuition‐Free" disagree by a token boundary.

The rule that covers both: **fold every character class BEFORE the ASCII strip, and fold the two
spellings of a class to the SAME thing.** Which thing matters less than that they agree — apostrophes
are deleted so both sides yield "cant", dashes become a space so both sides yield two words. Neither
carries retrieval signal; `norm()` discards punctuation on both sides before any comparison is made.

USE: `from textnorm import norm, oa_search_safe, selftest` — and call `selftest()` at start-up. A
guard that silently stops firing is worse than no guard.
"""
import re
import sys
import unicodedata

# Non-ASCII BASE letters that NFKD does not decompose. Without these, a dotless i or a stroked
# letter is DELETED rather than folded, which shortens a surname instead of fixing it.
_TRANSLIT = {
    ord("ø"): "o", ord("Ø"): "O", ord("đ"): "d", ord("Đ"): "D",
    ord("ð"): "d", ord("Ð"): "D", ord("þ"): "th", ord("Þ"): "Th",
    ord("ı"): "i", ord("İ"): "I", ord("ł"): "l", ord("Ł"): "L",
    ord("æ"): "ae", ord("Æ"): "Ae", ord("œ"): "oe", ord("Œ"): "Oe",
    ord("ß"): "ss", ord("ħ"): "h", ord("Ħ"): "H", ord("ŋ"): "n", ord("Ŋ"): "N",
}

# U+0027 apostrophe, U+2018/U+2019 curly quotes, U+02BC modifier letter, U+00B4 acute used as an
# apostrophe, U+0060 backtick. All six occur in indexed titles.
_APOSTROPHE_CLASS = re.compile("['‘’ʼ´`]")
# U+002D hyphen-minus, U+2010-U+2015 the dash block, U+2212 minus, U+00AD soft hyphen.
_DASH_CLASS = re.compile("[-‐‑‒–—―−­]")


def norm(s):
    """Fold to a comparable ASCII token string. Order is load-bearing: translit, then punctuation
    classes, then NFKD, then the strip."""
    s = (s or "").translate(_TRANSLIT)
    s = _APOSTROPHE_CLASS.sub("", s)
    s = _DASH_CLASS.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def oa_search_safe(title):
    """Make a title safe to send as an OpenAlex relevance-search string.

    TWO hazards, both answering 200 and neither looking like an error.

    (1) WILDCARDS. `?` and `*` are wildcard operators in `search=`. A title containing either is
    REJECTED with a 200 whose body is an {"error": ...} object that `.get("results", [])` renders as
    an empty field. Interrogative titles are common in economics and demography.

    (2) APOSTROPHES. An apostrophe-bearing token does not get the query refused; it gets it ANSWERED
    WRONG. `search=` for "Can't afford a baby Debt and young Americans" returns 8,633 records led by
    an unrelated paper on compulsive buying; drop the token and the correct work is rank 1 of 18,783.
    Stripping the apostrophe INSIDE the token ("Cant") is worse: 0 hits on `title.search`.

    Measured on three titles across both apostrophe forms before being generalised — dropping was
    decisive twice and harmless once."""
    t = re.sub(r"[?*]", " ", title or "")
    t = " ".join(w for w in t.split() if not _APOSTROPHE_CLASS.search(w))
    return re.sub(r"\s+", " ", t).strip()


# (input, expected) — names go through the accent path, titles through the punctuation path.
FOLD_CASES = [
    ("Zsolt Spéder", "zsolt speder"), ("Susanne Fahlén", "susanne fahlen"),
    ("Lívia Sz. Oláh", "livia sz olah"), ("Füsun Terzioğlu", "fusun terzioglu"),
    ("Tomáš Sobotka", "tomas sobotka"), ("Øystein Kravdal", "oystein kravdal"),
    ("Gina Potârcă", "gina potarca"), ("Alı Hortaçsu", "ali hortacsu"),
    ("Patrick Präg", "patrick prag"), ("Rémy Slama", "remy slama"),
    ("Can't afford a baby", "cant afford a baby"),
    ("a Child's College Education", "a childs college education"),
    ("Young People's Housing Tenure", "young peoples housing tenure"),
    ("Tuition-Free Education Policy", "tuition free education policy"),
]

# Pairs that must fold IDENTICALLY from the ASCII side and the Unicode side. This is the check the
# defect would fail; the FOLD_CASES above are the check that the agreed form is the intended one.
PAIR_CASES = [
    ("Can't afford a baby", "Can’t afford a baby"),
    ("a Child's College Education", "a Child’s College Education"),
    ("Young People's Housing Tenure", "Young People’s Housing Tenure"),
    ("Tuition-Free Education Policy", "Tuition‐Free Education Policy"),
    ("Sanz-de-Galdeano", "Sanz–de–Galdeano"),
]

QUERY_CASES = [
    ("Can't afford a baby? Debt and young Americans", "afford a baby Debt and young Americans"),
    ("Realizing a desired family size: when should couples start?",
     "Realizing a desired family size: when should couples start"),
    ("Debt, Cohabitation, and Marriage in Young Adulthood",
     "Debt, Cohabitation, and Marriage in Young Adulthood"),
]


def selftest(die=True):
    """Return a list of failures; exit non-zero if `die` and any exist."""
    bad = []
    for raw, want in FOLD_CASES:
        got = norm(raw)
        if got != want:
            bad.append(f"  fold: {raw!r} -> expected {want!r}, got {got!r}")
    for a, u in PAIR_CASES:
        na, nu = norm(a), norm(u)
        if na != nu:
            bad.append(f"  pair: {a!r} -> {na!r}   BUT   {u!r} -> {nu!r}")
    for raw, want in QUERY_CASES:
        got = oa_search_safe(raw)
        if got != want:
            bad.append(f"  query: {raw!r} -> expected {want!r}, got {got!r}")
    if bad and die:
        sys.stderr.write("ABORT: textnorm self-test failed; titles would normalise asymmetrically "
                         "and correct anchors would be reported as NO-MATCH:\n")
        sys.stderr.write("\n".join(bad) + "\n")
        sys.exit(1)
    return bad


if __name__ == "__main__":
    failures = selftest(die=False)
    if failures:
        print("FAIL")
        print("\n".join(failures))
        sys.exit(1)
    print(f"textnorm self-test PASS — {len(FOLD_CASES)} fold, {len(PAIR_CASES)} pair, "
          f"{len(QUERY_CASES)} query cases")
