# TICK-074: Shared resolver — fold apostrophes and dashes before the ASCII strip
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** n/a — shared scaffold defect found on C.3.g (TICK-073)
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** source/build/goldset/{22,38,49,55,64,69,70,71,72,79,80,81}_*.py, source/lib/textnorm.py, scripts/audit_norm.sh

## The defect

`norm()` folds ASCII and Unicode punctuation ASYMMETRICALLY. An ASCII apostrophe survives NFKD and is
then turned into a SPACE by `[^a-z0-9 ]`, splitting one token in two; a curly apostrophe is
non-ASCII, so `encode("ascii","ignore")` DELETES it and the token stays whole. Indexes store the
curly form and a hand-written candidate carries the straight one, so the same title normalises two
different ways:

    candidate "Can't afford a baby"  -> "can t afford a baby"   (5 tokens)
    index     "Can’t afford a baby"  -> "cant afford a baby"    (4 tokens)

Jaccard 0.70 against a 0.72 floor: **refused, and reported as NO-MATCH — which reads as an absent
work.** The dash class fails in mirror (ASCII hyphen spaced, U+2010 deleted).

On C.3.g's A3 this refused 3 of 24 anchors including the chapter's most-cited primary-cell work.
Fixed there in `201_` and `204_`; **12 inherited copies on `main` still carry the defect** and every
new chapter copies one of them.

## Acceptance criteria
- [x] `source/lib/textnorm.py` carries the canonical `norm()`, the punctuation classes, and
      `punctuation_fold_selftest()` (checks BOTH that the two sides agree AND that they agree on the
      intended string — a fold that deleted everything would pass a symmetry check alone)
- [x] All 12 identity-matching copies on `main` patched, each still parsing and each agreeing with the
      canonical implementation on a shared test vector
- [x] `scripts/verify_norm.py` reports defective copies across every branch, and is correct — the
      first version of this audit returned all zeros because zsh does not word-split unquoted
      expansions, i.e. it was itself a fake zero
- [x] Exposure recorded: which past chapter runs could have lost an anchor to this, and which of
      those are worth re-running

## Log

### Result

**`source/lib/textnorm.py`** is now the canonical fold, with `selftest()` covering 14 fold cases, 5
ASCII-vs-Unicode pair cases and 3 query cases. **`scripts/verify_norm.py`** extracts every `norm()`
in `source/build/goldset` by AST, executes it in isolation, and compares it against the canonical one
on a shared vector. **12 copies checked, 0 drifted; 7 excluded by name with a stated reason.**

**The textual audit was wrong twice, and the behavioural one corrected it both times.**

1. The first audit reported **zero** defective copies on every branch — including the branch that
   carries the fix. zsh does not word-split unquoted expansions, so the loop never ran. A fake zero
   in a tool built to find fake zeros.
2. The corrected textual audit reported 12 copies "defective" by absence of the apostrophe class.
   Running them found something different and larger: **all of them were exposed to the ACCENT
   defect, and only some to the apostrophe one** — and three of the twelve are not identity matchers
   at all.

**The apostrophe asymmetry was INTRODUCED by the accent fix.** Before `NFKD` + `encode("ascii",
"ignore")`, non-ASCII characters and ASCII punctuation both became a space — symmetric, and wrong
about accents. Adding the ASCII fold made non-ASCII characters vanish while ASCII punctuation still
became a space. The second defect is a side effect of repairing the first, which is the argument for
a single canonical implementation rather than twelve hand-copies.

### Exclusions, each with a reason rather than an omission

- `38_`, `71_`, `81_` (`cluster_overlap`) — `norm()` prepares a TITLE+ABSTRACT blob for term
  matching and never lowercases. Substituting the canonical fold would change every cluster-overlap
  number rather than repair a match. **It is still a real defect** (a lowercase term list matched
  against a non-lowercased blob under-matches) and is filed separately, not smuggled in here.
- `26_`, `28_`, `30_` — `norm(d)` takes a **DOI**, not a title. Comparing it against a title fold is
  a category error; the exclusion list records that so it is not rediscovered.
- `84_c2c_ingest_pdfs.py` — a deliberate ligature-aware matcher for `pdftotext` output ("e¤ect" for
  "effect"), documented in place. It already folds accents correctly by stripping combining marks and
  is symmetric on apostrophes; this ticket adds only the non-decomposable translit pass.

### One behaviour change, stated rather than buried

`53_resolve_and_dedupe_pool.py` keyed a title→DOI map on a **squashed** slug with no separators. That
shape is preserved as `norm_slug()`, but its duplicate-merge pass at line 157 does substring
containment between two titles and now runs on the space-separated form. Containment is therefore
**stricter** than before — the squashed form could match across word boundaries. Both sides use the
same function so nothing is compared across forms, and a re-run of `53_` may merge slightly fewer
records than the committed output.

### Exposure in past runs

Every chapter's anchor log was scanned for refusals whose CANDIDATE TITLE carries a non-ASCII
character or an apostrophe. **Two, and neither is a confirmed loss:**

| Chapter | Record | Status |
|---|---|---|
| D.1.b | *Women's empowerment and fertility: A review of the literature* | NO-MATCH at J=0.545; a live re-test does NOT reproduce it, so the cause is unattributed |
| D.3.c | *Labor's Love Lost* | BOOK-NO-DOI, an expected index miss |

**No confirmed anchor loss in any prior run** — and this is a LOWER BOUND, because a case where the
asymmetric fold merely depressed a Jaccard without crossing the floor leaves no trace in these logs.
The first version of this scan also over-reported, matching the log format's own `→` arrow rather
than the titles.

### Workflow impact

New chapters should `from textnorm import norm, oa_search_safe, selftest` rather than copy. Where a
standalone copy is genuinely wanted, `scripts/verify_norm.py` is what keeps it honest, and it belongs
in CI. The exclusion list is part of the artifact: a verifier that silently skips what it cannot
classify is the same failure as the audit that returned zeros.
