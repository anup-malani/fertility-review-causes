# C1 production pull — despair-hopelessness-fertility

**Pulled:** 2026-08-19T01:41:25Z · **Status:** **INCOMPLETE — see below**

This pull is **immutable and dated**. It is the input to a paid screen and the denominator of the PRISMA identification box, and OpenAlex is a moving index: a re-pull would not reproduce it and would silently change every downstream count. Re-running produces a NEW pull with a new date, not a refresh of this one.

| | |
|---|---|
| expected universe (measured at query-freeze) | 238,189 |
| records written | **149,200** |
| unique OpenAlex ids | 149,200 |
| pages fetched | 746 |
| shortfall vs expected | 37.36% |
| failed pages | 1 |
| abstracts truncated at | 1200 chars |

**Filter applied:** `,from_publication_date:2000-01-01,type:article|review|book-chapter|report`

A small shortfall against the expected universe is normal — the count was measured at query-freeze and the index moves — but it is reported rather than absorbed, because the difference between *the index held N* and *we fetched N* is exactly what a PRISMA identification count asserts.

## Failed pages — NOT zero results

Each page below failed after retries and its records are **missing from this pull**. The cursor is recorded so the page can be re-fetched; until then the identification count is a lower bound.

- page 746: `Rate limit exceeded Insufficient budget. This request costs $0.001 but you only have $0.0001 remaining. Resets at midnight UTC. Need more? A`

## Why it stopped, and what the partial is

**The OpenAlex daily API budget was exhausted at page 746.** The exact error:

> Rate limit exceeded. Insufficient budget. This request costs $0.001 but you only have $0.0001
> remaining. Resets at midnight UTC.

At $0.001 per request, **the funded key's daily allowance covers roughly 750 requests**, and this
pull needs ~1,191. That is an infrastructure fact rather than a defect in this chapter: **any
production pull above ~150,000 records is inherently multi-day at the current budget**, and every
chapter's C1 inherits the constraint. Completing this pull needs ~445 more requests (~$0.45), which
one further day's allowance covers with room to spare.

The run stopped at the failure rather than skipping the page and continuing. That is deliberate: a
skipped page produces a pull that looks complete and is not, and the identification count is the one
number in a systematic review that must never be quietly wrong.

**The partial is not a random 62% — it is the 62% most relevant.** OpenAlex returned results in
relevance order, and the effect is unmistakable across the fetch:

| position in fetch | median year | mean citations | median citations |
|---|---|---|---|
| first 10% | 2011 | 143.3 | 101 |
| middle 10% | 2017 | 9.3 | 8 |
| last 10% | 2019 | 0.5 | 0 |

This matters twice over. It means the partial **cannot** be described as "62% of the corpus" — it is
the high-relevance head, and the missing 38% is the low-citation, more-recent tail. And it means the
partial is far more useful than 62% suggests:

**197 of the 204 filter-eligible gold records (96.6%) are already retrieved.** The seven that are not
all carry **zero citations**, exactly as relevance ordering predicts.

## Consequence for the identification count

Until the pull is completed, the PRISMA identification box must say **149,200 retrieved of 238,189
identified**, with the reason. It must not say 238,189. The gap is documented, dated, and closeable by
resuming from the checkpointed cursor:

    python source/build/goldset/158_d3c_c1_pull.py --resume
