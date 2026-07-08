# Live search exposes ghost citations in the frozen gold's recall denominator

**Date:** 2026-07-08. **Trigger:** the Part-4-full live OpenAlex production pull (`43_live_search.py`).
**Status:** the clean-run **82.5% estimand-filtered Recall(B) PASS is retracted as an artifact** pending a
de-ghosting pass. The method (GACS) is not invalidated; the *frozen gold's Tier-B recall denominator* is.

## What happened

The live pull searched OpenAlex `title.search` for the frozen production query and returned an 11,738-work
universe (11,463 after dedup, 7,079 with abstracts) — in line with Anup's ~6.4k baseline. But the
universe-level gold-recall check came in far below the validated 82.5%, so we probed the misses directly
against OpenAlex instead of proceeding to screen.

**The PRIMARY-cell gold anchors that the live search "missed" do not exist.** Of the 57 PRIMARY-cell
frozen-gold anchors:

| | count | note |
|---|---|---|
| with a DOI | 12 | real; recovered in the live pull |
| **no DOI** | **45** | the ghost-suspect stratum |
| — probed on OpenAlex `title.search` (36 of the 45) | | **35 return count = 0**, 1 real-under-variant-title |

So **~35 of 57 (≈60%) PRIMARY-cell anchors are ghost citations** — plausible-sounding titles built from the
topic vocabulary (e.g. *"Pension generosity and fertility: Evidence from Poland"*, *"Old-Age Security and
Fertility in Sub-Saharan Africa"*, *"Do social security reforms affect fertility?"*) that have no
corresponding OpenAlex record. They entered via the snowball's forward-citation hallucination — the exact
ghost-citation mechanism the pilot evaluation §5 already flagged (7 of 8 pilot ghosts were forward
citations) — and were kept as title-only "gold" under the (well-intentioned) rule that title-only anchors
are never dropped so the recall denominator stays unbiased.

## Why the 82.5% was an artifact

Estimand-filtered Recall(B) was measured by the CV's **title-substring match**: a gold paper counts as
"recovered" iff the query terms match its title string. A ghost title like *"Pensions and Fertility in
Germany"* is *built from* query vocabulary, so it matches by construction and counts as recovered — even
though no real search can retrieve a paper that does not exist. The 47/57 = 82.5% therefore counted ~35
un-retrievable ghosts as hits. **Recall against a denominator that contains fictional papers is not a
recall estimate.**

## Why neither the CV nor the tag audit caught it

- The **CV** (title-match) never checks existence — it matches query terms to a stored title string, which
  ghosts pass trivially.
- The **Tier-B tag audit** (`39a`/`39b`, κ 0.84) checked *tag accuracy* (PRIMARY vs THEORY vs OFF) by
  re-reading title+abstract. A ghost with a plausible title and a hallucinated abstract passes as a
  correctly-tagged PRIMARY. The audit even re-flagged "corrupted/injected abstracts" but treated them as
  text to clean, not as evidence the whole record is fictional.

This is a textbook vindication of the PI's critique #3 ("validated in components, not end to end"):
**component checks structurally could not detect ghosts, because none of them tested existence against a
real corpus. The first live end-to-end pull found it immediately.** Insisting on the live run was the
control that mattered.

## Contamination is concentrated in Tier B (the snowball tier), by cell

Tier-B no-DOI share (the ghost-exposed stratum): **PRIMARY 45/57 (79%)**, THEORY 86/169 (51%), OFF 12/31
(39%). **Tier A is clean** (6/56 no-DOI, 11%) — it went through the 01–17 DOI-resolver pipeline. The rot is
where we'd predict: the orthogonally-sourced snowball tier.

## What this does and does not change

- **Does not invalidate GACS** (the architecture), the estimand gate, the head-to-head, or the cluster
  test. Those stand.
- **Does invalidate** the specific frozen-gold Tier-B recall denominator and therefore every recall number
  measured against it — topical 70/72.5%, empirical, and estimand-filtered 82.5%. All must be re-graded
  after de-ghosting.
- **The live corpus (11,463 real records) is sound** and is the correct universe to screen — but screening
  is on hold until the gold is de-ghosted, because the screen's recall would be graded against the same
  contaminated denominator.

## Required next step: de-ghost the gold, then re-grade

1. **Existence-verify every no-DOI Tier-B anchor** against OpenAlex + Crossref (title.search with an
   author/year gate, per the §5 title-matching machinery). Papers that resolve → keep, keyed on the found
   DOI. Papers that return no match → **quarantine as ghost** (do not silently drop; record them, because
   the ghost rate is itself a finding about the snowball).
2. **Re-freeze** Tier B on the de-ghosted set and **re-run `42`** to re-grade estimand-filtered Recall(B)
   against the real denominator, versus the pre-registered 0.80 bar. *This* number is the honest one.
3. **Then** proceed to screen the live corpus (Haiku→Sonnet→RA) and emit tiers.
4. **Method fix (carry to every chapter):** add a mandatory existence-verification gate to gold-set
   construction — no anchor enters the recall denominator without a resolved live DOI (or an explicit
   RA-signed "real but un-indexed" exception). This is the abstract-or-live-DOI gate the PI asked for,
   applied to the *anchor records* and not just their abstracts.
