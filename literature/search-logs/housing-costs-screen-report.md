# Screen report — housing costs (C.2.c)

**Run:** 2026-07-31, Shravan (TICK-055)
**Input:** Tier-B frame, 241 records after normalized-title dedup
**Worklist:** `extraction/housing-costs-screen-worklist.csv`
**Status:** PROVISIONAL. Nothing here is an inclusion decision — the RA gate is the verdict.

---

## 1. What was run

Two passes, both deterministic and both recorded so a bad rule is findable by name.

- **Pass 1 — title only.** Routed 149 of 241; left 92 unrouted. That residual is *correct*, not a
  failure: a title like "Housing and Fertility" or "Housing and First Births in Sweden" does not say
  whether the treatment is a price, a tenure status, or a housing expenditure — and price-vs-tenure is
  precisely what the 2026-07-31 ruling turns on.
- **Pass 2 — title + abstract.** Abstracts fetched from OpenAlex; **66% coverage (158/241)**. Pass 2
  resolved 48 of the 92. The remaining 44 split into `UNCERTAIN_NEEDS_FULLTEXT` (26, has an abstract
  but the treatment is still not stated) and `INSUFFICIENT_INFO` (18, no abstract — carried on title
  and flagged, never dropped, per GACS D2a and the D.3.b precedent).

| Provisional cell | n |
|---|---|
| PRIMARY_COST_RENTER | 48 |
| PRIMARY_WEALTH_OWNER | 28 |
| PRIMARY_SPACE_QUANTITY | 16 |
| PRIMARY_COST_RENT_IDENTIFIED | 16 |
| **PRIMARY subtotal** | **108** |
| OFF_OUTCOME | 29 |
| UNCERTAIN_NEEDS_FULLTEXT | 26 |
| INSUFFICIENT_INFO | 18 |
| REVERSE | 15 |
| HOUSING_ONLY_MECHANISM | 13 |
| AGGREGATE_UNSPLIT | 11 |
| AFFORDABILITY_RATIO | 10 |
| OFF_CREDIT_C3e | 9 |
| OFF_OTHER / OFF_LIVING_ARRANGEMENT_A23 | 2 |

## 2. The PRIMARY counts are inflated — read them as an upper bound

**Do not quote 108 as the empirical base.** A sample read of each cell shows the rules admit papers
that mention a construct rather than *identify off* it. The clearest case is also the most important
one.

**The rent stratum is not 16 studies. It is about four or five.** The scope doc calls
rent-identified estimates the highest-quality stratum, because rent carries no offsetting wealth gain
for the payer and so isolates the cost channel *without* the endogenous tenure split that is C.2.c's
main identification weakness. Reading all 16:

**Rent genuinely the treatment (~4–5):**
- *Do higher rents discourage fertility? Evidence from U.S. cities, 1940–2000* (RSUE)
- *The effect of the price or rental cost of housing on family size* (theoretical + empirical)
- *The Effect of Public Rental Housing on Birth Interval* (policy-assigned rental housing)
- *Working from Home, Land Rents, and Fertility*

**"Renter" as a sample descriptor, not a treatment (~11–12):** the macro multi-country study
(renters as one subgroup), the Korean family-size study (rent as a tenure category), the Swedish
cohort study (rental apartments as a housing *type*), the Guangzhou public-housing studies (renters as
the sample frame), *Housing Expenditure and Births in Italy* (rent as one component of an expenditure
measure — that is an expenditure treatment, not a rent treatment), and several others.

The same over-admission affects `PRIMARY_WEALTH_OWNER`, where the token `homeowner` catches
tenure-*trajectory* papers ("US baby boomers' homeownership trajectories across the life course") that
route out under the price-variation ruling.

**Implication for the chapter, and it is the one the evidence-base posture anticipated.** The cleanest
identification stratum is roughly a handful of studies. Combined with the round-2 finding that the
large `demog-tenure` literature mostly studies tenure and mobility rather than prices, C.2.c is
tracking toward exactly the theory-heavy chapter resting on a small empirical core that was accepted
on 2026-07-31. **This is a finding about the field and belongs in the chapter, alongside the
denominator**, per the standing obligation attached to that posture.

## 3. Three filter corrections, and the structural lesson

The housing-axis relevance filter was wrong three times (snowball log §4c): `hous`→household,
housework, Houston; `rent`→parent, current, different; `residen`→medical residents; `propert`→
psychometric properties; `home`→homeland. Cumulatively **351 false positives**, frame 545 → 241.

**Every one was found by reading a random sample. None was found by the counts**, which stayed
plausible and monotone throughout.

The structural error underneath all three: GACS Phase D specifies a *semantic* screen (D1 ranking →
Haiku recall → Sonnet precision). A title substring filter is a **D1-class instrument** and I used its
output as the **definition of the Tier-B frame**, a D2-class job. The lesson is not "write better
regexes" — it is that **relevance for a gold set must be decided semantically; a substring filter can
only pre-sort the queue for that decision.** C.2.c is an unusually hostile case (housing collides with
household/housework/animal housing; fertility with soil and livestock fertility), but the structural
point is general.

*Direction of failure matters:* every one of these bugs **over-admitted**, which held the snowball's
saturation yield above its floor and produced the (now retracted) conclusion that the §7.2 stop rule
was defective. **A relevance filter that over-admits does not look like an error. It looks like more
work to do.**

## 4. Dedup

Frame **256 → 241**, 13 exact-title groups collapsed; published version survives over preprint.

One dedup miss was caught by the rent-stratum read and fixed: *"Evidence from U.S. Cities"* and
*"Evidence from US Cities"* are the same paper, but stripping punctuation renders one `u s` and the
other `us`, so they never collided. Normalization now collapses runs of single letters. **Found by
reading, again — not by the duplicate count.**

Two near-duplicate groups remain flagged for human review rather than merged
(`housing-costs-dedup-review.json`): Lovenheim & Mumford's REStat article vs its SSRN version, which
*is* one paper; and two genuinely distinct residential-greenness papers. Auto-merging on title prefix
would have been right once and wrong once.

## 5. Next steps

1. **RA gate on the 108 provisional PRIMARY records** — the rent and wealth strata first, since both
   are known to over-admit and both feed the pooling rule. Expect substantial shrinkage; that is the
   intended behaviour of the price-variation ruling, not a defect.
2. **Resolve the 44 unrouted** — 26 need full text, 18 need an abstract or a title-only judgement.
3. **Retrieve full text for the surviving PRIMARY set**, since tenure conditioning, treatment type,
   parity, and tempo-vs-quantum are all full-text facts (scope doc, "When to adjudicate").
4. **Freeze the gold** once the screened count is known, then re-check the ≥30 empirical-anchor CV
   floor before any term mining.
