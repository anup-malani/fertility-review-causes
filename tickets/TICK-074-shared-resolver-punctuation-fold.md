# TICK-074: Shared resolver — fold apostrophes and dashes before the ASCII strip
**Status:** open
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
- [ ] `source/lib/textnorm.py` carries the canonical `norm()`, the punctuation classes, and
      `punctuation_fold_selftest()` (checks BOTH that the two sides agree AND that they agree on the
      intended string — a fold that deleted everything would pass a symmetry check alone)
- [ ] All 12 defective copies on `main` patched, each still parsing and each agreeing with the
      canonical implementation on a shared test vector
- [ ] `scripts/audit_norm.sh` reports defective copies across every branch, and is correct — the
      first version of this audit returned all zeros because zsh does not word-split unquoted
      expansions, i.e. it was itself a fake zero
- [ ] Exposure recorded: which past chapter runs could have lost an anchor to this, and which of
      those are worth re-running

## Log
