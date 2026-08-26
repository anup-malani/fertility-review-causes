# P2 retrieval — the record that overturned the empty-cell finding, and what it turned out to be

**Hypothesis:** C.3.g · **Ticket:** TICK-073 · **Date:** 2026-08-26

A4 reported that C.3.g's policy-variation cell was **not** empty, on the strength of one record found
through the citation channel: *Experimental Evidence on Consumption, Saving, and Family Formation
Responses to Student Debt Forgiveness* (SSRN 2022, `10.2139/ssrn.4139814`). The scope was corrected
in place to say that no PUBLISHED policy-variation study exists and that the sole candidate was an
uncited preprint which had to be read before any verdict.

It has now been read, and **the correction was wrong in the other direction.**

## Routes tried, in order

| Route | Result |
|---|---|
| OpenAlex `locations` | `green` OA; two locations, both landing pages, **no PDF url** |
| Unpaywall | `is_oa: true`, one repository location, `url_for_pdf: None` |
| Semantic Scholar | points back to the same DOI; no abstract, no PDF |
| WUSTL Open Scholarship landing page (`spi_research/62`) | **200** — and it carries the full abstract |
| WUSTL `viewcontent.cgi` PDF route | **403** on curl, twice, including with a full browser header set and a cookie jar |
| SAGE published version, three URL forms | **403** on all three |
| Chrome, SAGE | Cloudflare "Performing security verification", twice |
| Chrome, WUSTL `viewcontent.cgi` | PDF rendered in the browser's viewer; not extractable as text |

**Both blocks are bot defence on OPEN-ACCESS content, not paywalls** — the landing page and the
journal are both free. This is the third chapter to hit it; the standing lesson holds, and the
remaining full text is a **browser-job for a human**, not a proxy job.

## What the abstract settles

The WUSTL landing page carries the complete abstract. Three things follow, and they matter more than
the PDF would have.

**1. It is a hypothetical vignette, not a policy evaluation.** Participants were asked *"to imagine a
scenario in which the federal government forgave a certain amount of student debt"* and then to
*"report on how this would affect their decisions and behaviors."* 1,053 participants randomly
assigned to $5,000 / $10,000 / $20,000 / complete forgiveness. The randomisation is real and the
outcome is a **stated intention**. That is a **P6** record, not a P2 one.

**2. It is the same study as a record already in the frame.** The Socius 2023 article *Student Debt
Forgiveness and Economic Stability, Social Mobility, and Quality-of-Life Decisions: Results from a
Survey Experiment* (`10.1177/23780231231196778`) has the **same four authors** (Jabbari, Roll,
Despard, Hamilton), the **same N = 1,053**, the **same four conditions**, and a near-identical
abstract. The preprint is its working version. The Socius article was screened RELEVANT in batch 1.

**So the "candidate the query could not have found" was found by the query all along, in its
published form.** The pair evaded D1's duplicate collapse because the two versions have *different
titles* — "Family Formation Responses" against "Quality-of-Life Decisions" — and D1 collapses on
normalized title.

**3. The named outcomes are savings and housing, not children.** Both abstracts name emergency
savings and saving for a down payment. Neither names childbearing or marriage. The preprint's title
says "Family Formation"; the published title does not. **Whether a childbearing item exists in the
instrument is unresolved and needs the full text** — it decides whether this study is a P6 record for
this chapter at all, or only a savings-and-housing record.

## The claim, in its third and current form

- **Original scope:** *"There is no natural experiment in student debt with a fertility outcome
  anywhere in the indexed literature."* — Overstated; asserted from one hand-written vocabulary block.
- **After A4:** *"No published policy-variation study; one uncited preprint exists and must be read."*
  — Wrong: the preprint is published, as a different title, and is not a policy evaluation.
- **Now, after retrieval:** **No study anywhere in the frame estimates the effect of a debt-policy
  change on realized fertility.** What exists is one randomized *vignette* on stated intentions,
  published in *Socius* in 2023, whose preprint title mentions family formation and whose reported
  outcomes are savings and housing. **The P2 cell is empty of realized-fertility evidence** — which
  is the original claim, narrowed to what the evidence supports and now checked on two channels and a
  full abstract rather than on one query.

## Carried forward

1. **Collapse the version pair** at extraction (`W4285198771` ≡ `W4387715571`); count one study.
2. **Re-route the record from P2 to P6.** It is a stated-intention experiment.
3. **Full text stays on the wantlist** for the childbearing-item question, tagged `browser-job`.
4. **D1's duplicate collapse has a hole**: version pairs whose titles were changed between preprint
   and publication are invisible to a normalized-title match. A DOI-cluster or author+year+N check
   would catch this one; recorded rather than patched, because the fix belongs in the shared scaffold.
