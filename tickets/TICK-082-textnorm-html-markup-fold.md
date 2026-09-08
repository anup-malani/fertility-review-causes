# TICK-082: Canonical `textnorm.norm()` does not strip HTML markup
**Status:** open
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** `source/lib/textnorm.py`, `scripts/verify_norm.py`, `source/build/goldset/{18,22,49,53,55,56c,64,69,70,72,79,80}_*.py`

## The defect

OpenAlex indexes some titles with HTML markup. `norm()` strips non-alphanumerics to spaces, so a tag
survives as spurious tokens on both ends of the string:

```
    "<i>'Two children to make ends meet'</i>: the ideal family size"
      canonical textnorm.norm()  ->  "i two children to make ends meet i the ideal family size"
      the plain-text rendering   ->  "two children to make ends meet the ideal family size"
```

Those spurious `i` tokens deflate Jaccard against a clean candidate title and break contiguous stem
containment outright, so a correct anchor can be refused and recorded as NO-MATCH — which reads as an
absent work (`refusals-read-as-zeros`, `title-stem-indexing-defeats-resolver`).

**This is not a new discovery.** C.2.b found it on its own control record and fixed it in
`319_c2b_cold_start_anchors.py`, reporting it to TICK-074 as *defect 9*. TICK-074 merged on
2026-09-08 **without it**, because C.2.b's branch is unmerged and the fix never propagated. It was
re-found on C.2.f (TICK-081) by diffing the ported resolver's `_fold` against canonical `norm`.

**The interesting part is the shape, not the bug.** The canonical implementation was *already behind
one of the copies it was created to replace*, on the day it became canonical. A shared-library ticket
that lands while twelve chapter branches sit unmerged inherits only the fixes that happen to be on
`main`. See [[queue-board-move-never-lands]].

## Why this is a ticket and not a commit

Attempted on `main` 2026-09-08 and **reverted deliberately**, at two discoveries:

1. **The twelve copies are not textually uniform.** A patch keyed on the exact docstring applied to
   `18_tierb_frame.py` and failed the assertion on `22_cv_breadth.py`, leaving `main` half-modified.
2. **`scripts/verify_norm.py` extracts each `norm()` by AST and executes it in isolation.** Adding a
   new module-level name (`_HTML_TAG`) that the extractor does not know to carry made the patched
   copy raise `NameError` — so the verifier reported it as drifted for the wrong reason.

Fixing canonical alone turns the verifier red across all twelve copies, which is worse than the
defect. `validate-fixes-at-scale`: a fix verified on the case that motivated it is verified against
nothing. This needs the extractor understood first, then all thirteen changed together and
`verify_norm.py` green.

## Acceptance criteria
- [ ] Read `scripts/verify_norm.py`'s AST extraction and record which module-level names it carries
      into the isolated namespace; either extend it, or implement the fix without a new global
- [ ] `source/lib/textnorm.py` strips tags **before** the translit pass
- [ ] Tags are REMOVED, not replaced with a space, so a marked-up title folds to its plain-text
      rendering: `<sup>13</sup>C` renders "13C" and must fold `13c`, not `13 c`
- [ ] `FOLD_CASES` gains the three cases above, and `selftest()` passes
- [ ] All twelve copies patched and `scripts/verify_norm.py` reports **0 drifted**
- [ ] Exposure recorded: which past anchor runs could have refused a correct anchor to this. C.2.b's
      control record is one confirmed instance; OAS, B.1 and D.3.b anchor logs are unaudited
      (`version-of-record-gate` has the same outstanding audit)
- [ ] A note in the ticket on whether the twelve should keep being hand-copies at all, given that
      this is the second sync defect in three weeks

## Log
