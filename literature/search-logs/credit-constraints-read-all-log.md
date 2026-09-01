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

---

## Addendum: yes, the tables can be read — and one of them breaks the sign flip

The zero-hit problem was my sentence-level regex, not the documents. Estimates in these papers live in
tables, and tables are readable two ways: `pdftotext -layout` preserves the grid well enough to locate
a caption, and the PDF pages themselves can be read directly. Locating every table caption containing
a fertility term found results tables in 6 of the 12 apparently unreadable papers.

### The aggregate panels contradict each other on the developed-country sign

**Suriani et al. 2021, *Does Financial Development Contribute to Fertility Decline in Developed and
Developing Countries?*** — two-step system GMM, lagged dependent variable, 42 developed countries
(252 obs) and 43 developing (258 obs), read from Tables 3 and 4:

| Sample | Private credit → TFR |
|---|---|
| **Developed** | **−0.00634\*\*\* to −0.0318\*\*\*** (t = −4.02 to −12.19), negative and significant in **all 11 models** |
| **Developing** | **−0.0137\*\*\* to −0.0372\*\*\*** (t = −5.01 to −14.88), negative and significant in all 11, and **larger** |

**This directly contradicts Filoso and Papagni**, whose cross-country panel put high-income countries
at **+3.7 to +5%**. Here the developed-country effect is negative in every specification, and the
story is monotone — financial depth lowers fertility everywhere, more so where finance is shallow —
**not a sign flip**.

**So the sign flip rests on one unidentified aggregate panel and is contradicted by another.** It can
no longer be presented as the structure the chapter's two-arm logic implies; it is one of at least
three rival readings, alongside the within-setting inverted U and this monotone-negative account.

*Specification note recorded with the row:* the Sargan test p-value is 0.000 in all 11 models — the
overidentifying restrictions are rejected — while Hansen sits at 0.16–0.29. The table marks the Sargan
p-value with significance stars, which reads as though rejection were a result.

### Bangladesh, from Table 5

**Karim et al. 2016**: major NGO membership (a **proxy** for microfinance participation) against
children ever born, six surveys 1993–2011 — incidence ratios 1.007, 1.011, 1.020, 0.978, 1.028\*,
1.024\*. Positive and significant **only after 2007**, and tiny: "NGO members having 2 to 3 in 100 more
children." The authors conclude membership "has either no effect on or **increases** fertility."
Opposite in sign to Islam et al. on the same country — and the exposure is a self-selected proxy, so
it is an association with controls, not an identified estimate.

### The extraction table, sorted by setting

**17 rows, 13 studies, 7 identified.** Sorting the realized-fertility rows by income level:

- **High-income, identified:** +5.4%, +9.5 pp, +6 pp, and one verified null. **Positive or null, never
  negative.**
- **Low/middle-income, identified:** small negatives (Desai and Tarozzi −0.106 to −0.166), an inverted
  U, and Thailand's negative. **Never positive.**
- **Aggregate panels, unidentified:** one says flip, one says monotone negative.

The identified estimates are consistent with a sign difference by income level. **The aggregate panels
— the only sources that claim to measure the flip directly — disagree with each other.** That is the
honest state of the chapter's central claim.
