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

---

## Three further shared-resolver defects, found on C.6.a (TICK-078) 2026-09-02

Found by porting `275_c3e_cold_start_anchors.py` — the *fixed* copy — to C.6.a as `307_`. All three
are in 275 and therefore in every copy on `main`. All three showed up on a single anchor, Easterlin's
*Birth and Fortune*, and each one alone is enough to lose it.

**5. `is_stem` is fixed in one direction only.** It tolerates the index carrying a LONGER title than
the candidate (subtitle the candidate omitted). The mirror case is not handled: the index carries the
SHORTER title. *Birth and Fortune: The Impact of Numbers on Personal Welfare* is indexed as **Birth
and fortune** — Jaccard 0.33 — while four reviews of the book carry its full title at Jaccard 1.00.
`title-stem-indexing-defeats-resolver` had only ever been fixed one way round. Fix:
`is_stem_reversed`, gated behind the first-author test, since that direction admits more.

**6. The first-author gate is a scoring weight, so it can refuse but cannot promote.** Book reviews
list the reviewed author as a co-author, so they fail only the first-author test — and on score they
beat the book **1.20 to 0.83**. The gate refused the winner and had no mechanism to promote the
correct record sitting in the same result set. Fix: rank on the gate first — passing an applicable
first-author gate outranks everything, failing one outranks nothing. This is the promotion half of
`book-canon-first-author`, which until now only had the refusal half.

**7. The early exit is conditioned on a different test than the verdict — and this is the one that
does the damage.** The rung loop breaks when any candidate scores ≥ 1.0, including one the gate is
certain to refuse, so the later rungs never run. Fixing 5 and 6 alone left the anchor unresolved
because the rung that can reach a truncated book title was never reached. **An early exit must be
conditioned on the same gate the verdict uses.** Generalises past the resolver: any short-circuit
scored on a different criterion than the accept test can terminate on a record it is about to reject.

**8. Smaller, same family:** the pre-colon head rung requires a 4-token head. *Birth and Fortune* is
three tokens. Lowered to 3 where a first author is available to gate on.

**And a new verdict class worth adopting shared: `MATCH_VERSION_TWIN`.** Same title, same FIRST
author, year outside the ±1 gate = a working-paper/version-of-record pair, not a different study.
Butz and Ward's *Emergence of Countercyclical U.S. Fertility* exists twice — the record OpenAlex
dates 1977 carries **438** citations, the 1979 record carries **0** — so a candidate naming either
year fails the gate against the other. Five of C.6.a's 31 anchors have twins and the citation split
is severe: Welch's twin holds **0** of 659. Reference implementation:
`source/build/goldset/307_c6a_cold_start_anchors.py`.

