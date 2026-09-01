# Reading the retrieved studies — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Script `300_c3e_read_all.py`

## What "read all the studies" could actually mean

**69 primary records. 18 have a verified full text. 51 do not.** Reading is retrieval-bound, and the
gap is not evenly spread: Arm S has 12 records, composite 40, Arm B 17, and the retrieved 18 are
concentrated in the studies that were easiest to get, not the ones that matter most.

## A mis-mapping caught before it corrupted anything

The first pass reconciled the two PDF folders — one names files by OpenAlex id, the other by study key
— using fuzzy title matching, and **mis-assigned 8 of 10 files.** A PDF named for a record that had
since been **routed out** of the primary pool failed the "filename is an id in the pool" test, fell
through to "best title match above 0.6", and landed on an unrelated record sharing a few words.
**Desai and Tarozzi's record was handed the No-Birth-Bonus PDF.**

It was caught because the candidate sentences read wrong — a paper on Ethiopian microcredit returning
text about South Indian tea estates. **No extraction row was written from a bad pairing.** The map is
now built from verified sources only — filename-is-an-id, or the handoff CSV's explicit key→id map —
with no fuzzy fallback, and every mapping re-verified against the PDF's own first page.

## And the chapter's only randomised estimate had never been extracted

**Desai and Tarozzi was not in the extraction table.** Retrieved this morning, scanned, quoted in four
separate write-ups as the centrepiece of the composite cell — and never given a row. Now extracted, in
two rows, because it carries two outcome levels with opposite signs:

| Outcome level | Estimate |
|---|---|
| births in the previous three years (**realized**) | all estimates negative, **−0.106 to −0.166**, small, some significant |
| desired family size (**desired**) | **+0.38 to +0.40**, significant at 5% |

**Context that changes how the null reads:** fertility *rose* in the study area over the period — TFR
5.5 → 6.0, births in the last three years 0.51 → 0.55, both significant — and the authors write that
the rise in contraceptive use "does not appear to have had much effect on fertility." Those are
sample-wide time trends, **not** treatment effects, and must not be read as such.

## Two more extracted

**Küchler 2012** (Bangladesh panel): recent fertility coefficient **−0.14, t = −1.54, not
significant**; prospective fertility p = 0.29. A negative point estimate that does not clear
significance, alongside a sample-wide fall in the probability of a birth from 0.55 to 0.48 between
rounds.

**Lan, Pan and Yu 2023** (China): a 1% rise in the provincial digital-financial-inclusion index is
associated with **+0.136% in fertility intentions** — an *intention* outcome, positive, consistent
with Desai and Tarozzi's desires arm and inconsistent with the realized nulls.

## The extraction table now

**14 rows, 11 studies, 7 identified.** Outcome levels: 12 realized, 1 desired, 1 intention.

The realized/desired split is now visible inside the table rather than as an argument: **every
positive result in the chapter sits on desires or intentions, and every realized-fertility result in a
low- or middle-income setting is null or negative.** The positives on realized fertility are all
high-income Arm B credit-access shocks.

## What could not be read, and why

Twelve retrieved texts returned **zero** candidate estimate sentences. That is a limitation of the
method, not a finding about the papers: `pdftotext` linearises two-column journal PDFs so that
sentences spanning columns are shredded, and the estimates in these papers live in **tables**, which
sentence-level extraction cannot reach. Reading them properly means reading the tables by hand.

**The honest state: 11 of 69 primary records extracted, 18 retrieved, 51 unretrieved.** Anyone
reporting a synthesis today would be reporting on 16% of the pool.
