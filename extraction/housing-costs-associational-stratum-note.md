# The associational stratum — what we can and cannot say (C.2.c, TICK-056)

**Run:** 2026-07-31 · Closes the retrieval remainder of TICK-056.

## 1. Automated retrieval is exhausted at 30/78

A second full pass (preprint-twin siblings, then OA landing pages) over the 48 outstanding records
recovered **nothing**. Combined with the three passes run before hand retrieval, that is five distinct
automated routes with no further yield.

All 48 outstanding are **ASSOCIATIONAL**; 38 are `closed`, and 7 have no DOI at all. **The identified
core remains complete at 15/15**, so the chapter's central estimates are not affected.

## 2. Why these 48 were wanted, and what that implies

They cannot enter the pooled estimates — the chapter is explicit that they document association
without identification. Their value was to let us characterise the stratum: **does the large
uncontrolled literature point the same way as the identified core?** If it does, that is weak
corroboration; if it does not, the identified core is an outlier and the chapter must say so.

## 3. The automated direction tally FAILED validation and is not reported

A regex classifier over title + abstract produced: 14 negative, 12 mixed, 6 positive, 46 unclear.
**Those numbers are withdrawn.** A sample read found a plain false positive — *"The relationship
between apartment living and fertility…"* was classified POSITIVE when its abstract states that
apartment dwellers **"reduced their fertility"**. The classifier is the fourth substring-based
instrument in this chapter to fail a sample read, after the three relevance-filter corrections.

The artifact is retained at `housing-costs-associational-tally.csv` with its column renamed
`direction_HEURISTIC_REJECTED` and every row marked `REJECTED`, so it is auditable but cannot be
picked up and quoted by mistake.

## 4. What a manual read of the 45 available abstracts does support

A hand read was done. It does **not** support a vote count: most abstracts do not state a direction in
their first 175 characters, and inferring one from a truncated abstract would manufacture precision.
Producing a defensible tally requires the full texts, which are the ones we cannot get.

One qualitative observation is robust and worth carrying into the chapter, because it comes from the
abstracts' own framing rather than from a classifier:

> **Several studies in the associational stratum explicitly frame the effect as tenure-conditional or
> theoretically ambiguous.** Clark and Ferrer state that "higher housing prices will cause renters to
> desire fewer additional children, but home owners to desire more"; *Impacts of Housing Booms on
> Fertility in China* opens "due to the nexus of wealth effect and cost effect, the impact of housing
> price on fertility is ambiguous in theory."

**The field itself recognises the opposing-channels structure that this chapter's pooling rule is
built on.** That is independent corroboration of the framing — weaker than an estimate, but it is not
nothing, and it is the honest version of what the associational stratum can contribute without its
PDFs.

## 5. Recommendation

**Do not spend a human retrieval session on the 48.** They cannot change the pooled estimates, the
identified core is complete, and the characterisation they would support needs full texts for a
result that would remain a vote count — an instrument that ignores precision and sample size and that
this review should not lean on regardless.

If the stratum is to be characterised properly, the cheaper route is to retrieve a **random sample**
of perhaps 10–15, read them fully, and report the sample with its selection rule stated — rather than
retrieve all 48 for a weaker instrument.
