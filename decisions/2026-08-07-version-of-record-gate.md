# Anchor resolution needs a version gate, not only an existence gate

**Date:** 2026-08-07
**Author:** Shravan (RA)
**Status:** proposed — adopted in D.1.b (`95_d1b_cold_start_anchors.py`), pending PI sign-off for the
other chapters
**Found in:** TICK-063, D.1.b stage A3

## What happened

The existence-verification gate that came out of the 2026-07-08 OAS clean run is mandatory in gold
construction: no anchor enters a recall denominator without a live DOI or a Crossref record. D.1.b's
anchor script inherited it verbatim from `72_d3b_cold_start_anchors.py`.

On the first run it reported 20 of 28 anchors verified with a live DOI, most at title Jaccard 1.0.
Reading the resolved DOIs rather than the pass counts, **eight were the wrong version of the right
paper**:

| Anchor | Resolved to | Should have been |
|---|---|---|
| Jensen & Oster 2009 | NBER working paper `10.3386/w13305` | QJE `10.1162/qjec.2009.124.3.1057` |
| La Ferrara, Chong & Duryea 2012 | IDB working paper `10.18235/0010891` | AEJ:Applied `10.1257/app.4.4.1` |
| Okoye & Pongou 2023 | Research Square preprint | J Econ Growth `10.1007/s10887-023-09231-x` |
| Osili & Long 2007 | NBER working paper | JDE `10.1016/j.jdeveco.2007.10.003` |
| Caldwell 1980 | 2024 Routledge reprint chapter | PDR `10.2307/1972729` |
| Thornton 2005 | a *Choice* review of the book | the Chicago monograph |
| Kohler, Behrman & Watkins 2001 | a book chapter | Demography `10.2307/3088287` |
| Coale & Watkins 1986 | one chapter of the 2017 reissue | the volume |

Every one passed the existence gate, because every one is a real record that really resolves. A
preprint's title is identical to the article's; a book review's title reproduces the book's.

## Why the existing gate cannot catch this

The existence gate and the version problem are mirror images, and the first does not imply the second:

- A **ghost** is a title that resolves to *nothing*. The existence gate is exactly the right
  instrument, and it is what the OAS run needed.
- A **wrong version** is a title that resolves to something *real but not the record we mean*. Every
  existence check passes. Every title check passes, because the titles are the same string.

The resolver made it worse by taking the Jaccard argmax over Crossref rows. When five records share
one title, title similarity carries no information about which of them is meant, so the argmax is
effectively arbitrary — and Crossref's bibliographic ranking tends to surface working papers and
reviews above the version of record.

## Why it matters beyond tidiness

Anchors feed the Tier A/B citation frame. The backward and forward citation clouds of a working paper
are a small fraction of the version of record's: the NBER copy of Jensen & Oster carries roughly a
seventh of the citations of the QJE article. Anchoring on the working paper would have quietly shrunk
Tier B — the orthogonal recall yardstick — and the resulting Recall(B) would have looked fine, because
the denominator would have shrunk along with it. This is the same class of failure as the ghost gold:
a measurement instrument that is wrong in a way its own diagnostics cannot see.

For the theory canon the stake is different and worse. Thornton 2005 and Caldwell 1982 are the two
statements this chapter's mechanism rests on. Resolving them to a 900-word book notice in *Choice*
would have put a review in the gold set in place of the work.

## The rule

**Anchor resolution ranks candidates for being the version of record; it does not take the best title
match.** Concretely, as implemented in `95_d1b_cold_start_anchors.py`:

1. **Title fit is a gate, not a score.** Among records sharing a title, the discriminating information
   is type, venue, and year — so score on those and use the title only to decide who is eligible.
2. **Rank by record type,** journal article and monograph above chapter, report, and posted content.
3. **Penalize non-version-of-record DOI prefixes** — NBER, SSRN, Research Square, arXiv, SocArXiv,
   World Bank, IDB — as a cost, not a disqualification, because for some works the working paper *is*
   the version of record.
4. **Reject review venues outright.** A review of a work is never the work.
5. **Penalize year distance,** which is what separates a 2024 reprint from the 1980 original.
6. **Query both sources and rank them in one field.** OpenAlex indexes the version of record more
   reliably for this corpus. A second source consulted only when the first fails cannot correct a
   confident wrong answer, and a confident wrong answer is the whole failure mode here.
7. **Book-shaped anchors carry an `is_book` flag** requiring a book-shaped record, and are additionally
   queried on the pre-subtitle short title, since that is how monographs are indexed.

Two flags, not one: `is_book` (the record must be book-shaped) and `expect_no_doi` (a Crossref miss is
anticipated and is not evidence of absence). London & Hadden 1989 is the second without the first — a
real journal article Crossref does not index. Caldwell 1982 is both.

## A second finding, from fixing the first

The first fix admitted three *new* false matches. The inherited resolver had a containment escape
hatch — accept a match if the Szymkiewicz–Simpson overlap exceeds 0.90 — meant for the subtitle case,
where Crossref keeps a subtitle the candidate drops. Applied as a set test it fires in reverse: the
four tokens of "Theory of Fertility Decline" all appear somewhere in "The Spread of Education and
Fertility Decline: A Thai Province Level Test of Caldwell's Wealth Flows Theory", so a 1983 book
review scored containment 1.0 against a 1989 empirical paper on a different continent.

A set-containment test cannot tell a subtitle from a scatter of generic demography words, and in a
topic-homogeneous corpus most words are generic. The replacement tests whether the shorter title is a
**contiguous leading token sequence** of the longer — which is what a subtitle relation actually is —
with a Jaccard floor of 0.45 still in force underneath it.

**The general lesson is the one already written down after the B.1 filter work: a fix verified on the
cases that motivated it is verified against nothing.** The version-of-record ranking was checked
against the eight anchors that provoked it and looked like a clean success. Reading the other twenty
is what surfaced the three it broke.

## Also fixed, and worth stating separately

Two defects found while making the above stable, both of which would have produced silently wrong
output rather than an error:

- **No retry.** Two anchors flipped between resolved and unresolved across otherwise identical runs.
  A stage whose output depends on which API call happened to time out is not reproducible, whatever
  its recall.
- **Empty results were cached.** One rate-limited call became a permanent "this paper is not in
  OpenAlex". That is the three-state discipline — UNCONFIRMED is not ABSENT — being violated by the
  cache layer rather than by the resolver, which is precisely where nobody looks for it.

## It recurred one stage later, which is the point

Stage A3's resolver was rewritten. Stage A4 (`96_d1b_tier_ab_frame.py`) resolves anchors *again*, in
OpenAlex, and its title path was left as the original argmax. It promptly reproduced the failure:
Caldwell's 1982 monograph resolved to the 1983 PDR review of the book at similarity 1.0.

The specifics are worth recording, because they show how convincing the wrong answer looks. OpenAlex
holds **no record at all** for the monograph. It holds the review stub, typed `article`, carrying
**zero** `referenced_works` — and with the book's **1,338 citations attributed to it**. So the frame
log reported the anchor as resolved, with a citation count in the thousands, while the anchor
contributed nothing whatsoever to Tier B. Nothing in the counts would have shown this: an anchor with
an empty reference list looks identical to an anchor whose references were all already in the frame.

Fixed by carrying an `is_book` flag from A3 into A4 and requiring a book-shaped record there too. The
anchor is now reported as `book_no_openalex_record` — carried keyed on title, contributing nothing —
which is the true state.

**The transferable lesson: a resolution rule has to hold at every stage that resolves.** Fixing it
where the bug was found leaves it live everywhere else the same operation happens, and the second
site is harder to notice precisely because the first one now looks clean.

## What this implies for the other chapters

The OAS, B.1, and D.3.b gold sets were built with the argmax resolver and have **not** been re-graded
against a version gate. D.3.b's own log records version-duplicate records surviving into its corpus,
so at least some contamination is known to be there. The recommended follow-up is a re-resolution pass
over the frozen anchor sets of those three chapters, reporting how many anchors move — a cheap check,
since the resolver is written and the caches exist. **This is a proposal, not a completed check: no
claim is made here about how large the problem is in those chapters.** Opening it as its own ticket
is preferable to folding it into D.1.b, since it touches frozen gold in three other workstreams.

## Related

- `literature/search-logs/canonical-search-workflow.md` §A3 (the existence-verification gate this
  extends) and §5 (title-matching machinery, whose containment rule is amended here)
- `decisions/2026-07-11-tfr-replacement-transition-classification.md` (the other place where a
  three-state discipline is load-bearing)
