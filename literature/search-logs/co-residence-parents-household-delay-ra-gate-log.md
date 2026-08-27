# RA gate log — A.23 co-residence and delayed household formation

**Ticket:** TICK-075 · **Run:** 2026-08-27
**Scripts:** `229` (abstract recovery), `230` (re-read), `231` (queues and Wall 1 packet)

## 1. What the gate was for

The screen report flagged its own weakest point rather than waiting to be caught: 165 of
the 241 records with no OpenAlex abstract were marked NOT_RELEVANT on the title alone. The
rubric permits that only when the title is decisive, and this chapter had already been
bitten once by trusting a title-only record — the anchor whose exposure the 223 audit could
not check.

The gate's first job was therefore not to sample that bucket but to try to **abolish it**.

## 2. Abstract recovery: a 15% audit, not a clearance

`229` asked **Crossref** for an abstract for every no-abstract record with a DOI. Crossref
and OpenAlex are independent enough that the gap was worth testing rather than assumed.

| | n |
|---|---|
| No OpenAlex abstract | 241 |
| — recovered from Crossref | **35** (14.5%) |
| — Crossref has the record but no abstract | 203 |
| — no DOI at all, unreachable by this route | 3 |
| Recovered **and** previously rejected on the title alone | **25** |

So the bucket did not collapse. **206 records remain invisible**, and they are reported in
three parts rather than one, because "absent from Crossref" and "has no DOI" carry different
weight when the gate decides what to do next.

## 3. The re-read: 22 confirmed, 3 revised

`230` re-read all 25 against the recovered text.

- **22 CONFIRMED.** The titles were decisive, as the rubric requires.
- **3 REVISED**, all NOT_RELEVANT → UNCERTAIN, and only **one** into a primary cell:
  a Korean study whose recovered abstract shows the division of domestic labour is measured
  with **husbands, parents and parents-in-law** against fertility intentions — an
  extended-arm record, not the gender-equity story the title implied.

**The title-only rule survived the only test that could be run on it.** That is a 15% audit
of the bucket, and it is stated as such: it can show the rule failing, and it did not; it
cannot clear the 140 rejected records that stayed invisible.

### The result worth more than the revisions

One of the three **gold records the blinded screen rejected** was in this worklist:
*Roadblocks on the Road to Grandma's House*. The recovered abstract confirms the rejection —
it exploits a decade of Italian pension reforms that lengthened the grandparental
generation's working horizon, treating that as a shock to informal childcare **supply**. The
exposure is the grandmother's availability, not the living arrangement.

An independent source vindicated a blinded screen's rejection of a hand-picked anchor. Three
mechanisms — the exposure audit, the blinded screen, and Crossref recovery — have now
converged on the same boundary.

Two further confirmations are worth carrying: the China second-birth childcare record uses
an **endogenous switching probit**, and the female-employment-paradox record uses
**propensity-score matching**, both correcting for the selection this chapter's §3 is about.
The C.2.a literature is more endogeneity-aware than the A.23 literature it borders.

## 4. Retrieval queue

`231` orders the queue by what SYNTHESIS needs, not by what is easy to fetch. B.1 is the
precedent: it stalled at 20 of 95 PDFs and its pooled estimate still rests on five studies.

| Tier | n | why |
|---|---|---|
| T1 Wall 1 packet | 26 | The open ruling; nothing downstream settles before these |
| T1 primary, identified | 6 | These carry the GRADE rating for their arm |
| T2 primary, RELEVANT | 57 | The core of each arm |
| T3 primary, UNCERTAIN | 28 | Cell balance depends on how they resolve |
| T3 link 1, identified | 9 | The only leverage on whether the arrangement responds to anything exogenous |
| T4 INSUFFICIENT_INFO | 34 | Retrieval *is* the screen for these |
| T5 link 1 | 193 | Mechanism; after the primary cells |
| T6 theory | 83 | Read, do not pool |
| **Queued** | **436** | of 1,572 |

**98 queued records have no DOI.** That is the retrieval risk, and it is concentrated in the
older and grey-literature strata rather than spread evenly.

**Report retrieval as a cross-tab of tier by outcome, never as one percentage.** A 70% rate
that misses the six identified primary-cell designs is worse than a 40% rate that gets them.

## 5. What the gate did not do

- **It did not second-read the screen.** The re-read above was done by the same reader who
  screened. That is a consistency check, not independence, and it is labelled as one — the
  standing rule that adversarial re-rating by one rater is not a panel.
- **It did not resolve the 206 still-invisible records.** They sit in their screen verdicts
  and inherit the caveat.
- **It did not settle Wall 1.** `…-wall1-packet.md` assembles the 26 records and the three
  positions available; the choice is the PI's.
