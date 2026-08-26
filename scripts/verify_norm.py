#!/usr/bin/env python3
"""
verify_norm.py — assert every copy of `norm()` in the pipeline agrees with the canonical one.

The pipeline's scripts each carry their own copy of `norm()`, because they are run standalone from
varying working directories and an import path is one more thing to get wrong. That is a defensible
choice ONLY if the copies are kept in sync, and hand-copied functions drift silently — twice now,
in the same function, in ways that produce confident wrong answers rather than errors:

  * an unfolded accent SHATTERS a surname (Spéder -> "der"), so the author gate returns "this record
    HAS authors and none of them is ours" — a wrong negative, not a missing-data None (found on
    D.3.c);
  * an ASCII apostrophe becomes a SPACE while a curly one is DELETED, so a title normalises two
    different ways depending on which side wrote it and a correct anchor is refused as NO-MATCH —
    which reads as an absent work (found on C.3.g, where it cost 3 of 24 anchors).

This script is what makes the copies safe: it extracts each `norm` by AST, executes it in isolation,
and compares it against `source/lib/textnorm.norm` on the full shared vector. Run it in CI, or at
least before any stage that resolves anchors.

KNOWN AND DELIBERATE EXCLUSIONS (see EXCLUDED below). Not every function named `norm` is doing
identity matching, and "fix them all" would change outputs rather than repair a defect.
"""
import ast, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm as canonical, FOLD_CASES, PAIR_CASES, selftest   # noqa: E402

GOLDSET = os.path.join(ROOT, "source", "build", "goldset")

# `norm()` in these scripts prepares a TITLE+ABSTRACT blob for term matching. It never lowercases
# and never strips punctuation, so it is not an identity matcher and swapping in the canonical fold
# would change every downstream cluster-overlap number rather than fix a match. It IS a real defect
# — a lowercase term list matched against a non-lowercased blob under-matches — but it is a
# different one, and it is filed separately rather than smuggled into this fix.
EXCLUDED = {
    # `norm()` here prepares a TITLE+ABSTRACT blob for term matching. It never lowercases and never
    # strips punctuation, so it is not an identity matcher, and swapping in the canonical fold would
    # change every downstream cluster-overlap number rather than repair a match. It IS a real defect
    # — a lowercase term list matched against a non-lowercased blob under-matches — but a different
    # one, filed separately rather than smuggled into this fix.
    "38_cluster_overlap.py", "71_b1_cluster_overlap.py", "81_d3b_cluster_overlap.py",
    # These take a DOI, not a title: `norm(d)` strips the doi.org prefix and lowercases. Comparing
    # them against a title fold is a category error, which this list exists to record rather than
    # rediscover.
    "26_finalize_dois.py", "28_acquire_pass2.py", "30_acquire_pass3.py",
    # A deliberate ligature-aware matcher for pdftotext output ('e¤ect' for 'effect'), documented in
    # place. It already folds accents correctly by stripping combining marks, and it is symmetric on
    # apostrophes. TICK-074 adds only the non-decomposable translit pass and leaves its shape alone.
    "84_c2c_ingest_pdfs.py",
}

VECTOR = [c[0] for c in FOLD_CASES] + [s for pair in PAIR_CASES for s in pair] + [
    "", None, "  MIXED   Case  ", "Sanz-de-Galdeano", "O'Brien", "Müller–Lyer", "naïve café",
]


def norm_of(path):
    """Extract `norm` and only the module-level constants it needs, then execute in isolation.

    Deliberately NOT `import`: these scripts do work at import time and several compute paths from
    `__file__`. The AST route takes the function and its named constants and nothing else, so a
    verifier run can never trigger a pipeline stage."""
    src = open(path).read()
    tree = ast.parse(src)
    WANTED = {"_TRANSLIT", "_APOSTROPHE_CLASS", "_DASH_CLASS", "LIGATURES", "STOP",
              "_TRANSLIT_84"}
    consts, fn_node = [], None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in WANTED for t in node.targets):
            consts.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == "norm":
            fn_node = node
    if fn_node is None:
        return None
    ns = {"re": re, "unicodedata": unicodedata}
    exec(ast.unparse(ast.Module(body=consts + [fn_node], type_ignores=[])), ns)
    return ns["norm"]


def main():
    selftest()          # the canonical implementation must be right before anything is compared to it
    checked = drifted = 0
    problems = []
    for fn in sorted(os.listdir(GOLDSET)):
        if not fn.endswith(".py") or fn in EXCLUDED:
            continue
        path = os.path.join(GOLDSET, fn)
        try:
            f = norm_of(path)
        except Exception as e:
            problems.append(f"  {fn}: could not extract norm() — {type(e).__name__}: {e}")
            continue
        if f is None:
            continue
        checked += 1
        bad = []
        for v in VECTOR:
            try:
                got, want = f(v), canonical(v)
            except Exception as e:
                bad.append(f"    {v!r}: raised {type(e).__name__}")
                continue
            if got != want:
                bad.append(f"    {v!r}: {got!r} != canonical {want!r}")
        if bad:
            drifted += 1
            problems.append(f"  {fn} DRIFTED:\n" + "\n".join(bad[:4]))
    print(f"checked {checked} copies of norm() in {os.path.relpath(GOLDSET, ROOT)}; "
          f"{drifted} drifted; {len(EXCLUDED)} excluded by name")
    if problems:
        print("\n".join(problems))
        return 1
    print("all copies agree with source/lib/textnorm.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
