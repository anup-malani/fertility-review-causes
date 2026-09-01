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

---

## Three further shared-resolver defects, found on C.3.e (TICK-077) 2026-09-01

Same file family, same failure mode — each one manufactures a **false absence**, which is worse than
a wrong match because a NO-MATCH reads as "this work does not exist."

**1. The title channel has never worked, in any chapter.** `title.search` is **not a root OpenAlex
parameter**. Sending `title.search=<title>` as a top-level query param makes the API reject the whole
request — *"title.search is not a valid parameter"* — so the primary title channel returns nothing and
the code silently falls through to `search=`, which ranks by relevance across the entire record and is
much weaker. On C.3.e it failed **18 out of 18** and every single resolution came from the fallback.

It was invisible because the fallback usually finds the right paper anyway. It was caught only by
counting *which channel produced each match*, not by reading the code.

The correct form is `filter=title.search:VALUE`, with the value **wrapped in double quotes** — see
defect 2. After the fix, 0 of 26 C.3.e anchors resolve via the fallback and mean Jaccard is 0.94.
Reference implementation: `source/build/goldset/275_c3e_cold_start_anchors.py`.

**This is inherited from A.18's `245_a18_cold_start_anchors.py` and is in every descendant.** No
earlier chapter's anchor recall was measured against a working title channel.

**2. `%2C` does not escape a comma in a filter value — and the API's own error message says it does.**
A bare comma in a filter VALUE is fatal (known). Sending the percent-encoded form the error message
recommends returns *the identical error*. **Double-quoting the whole value works**, and has the
side benefit of keeping phrase matching instead of degrading to a token AND.

**3. `is_stem` is one-directional.** It tolerates a *dropped subtitle* (candidate is a prefix of the
returned title) but not an *added prefix*. Book chapters carry one — Schultz's Handbook chapter is
indexed as "**Chapter 8** Demand for children in low income countries" — and the test refuses it.
Fix: contiguous containment in **both** directions. This is not the unbounded suffix-containment the
shadow-record gate rejects; the author and year gates still apply on top of a 4+ token contiguous match.

**4. Related, not a defect but a required rung:** a title spanning a colon does not match as a single
stemmed phrase. Pitt 1999 returned 0 on the full quoted title and the fallback ranked an unrelated
systematic review first. A rung quoting only the **pre-colon clause** finds it immediately.

**And a caution for whoever does this work:** OpenAlex's own author metadata can be the error. Pitt
1999 is indexed with a first author of "Mark M. **Pin**". Do not loosen the first-author gate to
membership to accommodate it — route to a human read instead.

