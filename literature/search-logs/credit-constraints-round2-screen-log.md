# Snowball round 2, screened — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Scripts `285` (snowball), `287` (screen) ·
Outputs: `credit-constraints-snowball-round2.json`, `credit-constraints-round2-screen.json`

Skim-level readings of headline claims. Not extraction.

---

## 1. A correction to my own reading of round 2

I described round 2 as *"heavily contaminated by method citations"* on the strength of its top-20 by
citation count — Wooldridge, Little and Rubin, Angrist-Imbens-Rubin, Stock-Yogo, `ivreg2`.

**Measured, the method layer is 25 of 297 records — 8.4%.** The impression was an artefact of sorting
by citations: an econometrics textbook has tens of thousands of citations, so the method layer owns the
head of a citation-ordered list while being a small minority of the pool. Reading a citation-sorted
head as if it described the population is the same error as reading a relevance-ordered truncated pull
as a random sample.

The method layer was therefore **measured and reported, not silently deleted**. Two of the 25 flagged
records also carry an estimand, so the flag is imperfect — which is exactly why it is a reporting flag
and not a gate. The operative screen is the estimand classifier: Wooldridge fails it for having no
fertility outcome, not for being a textbook.

## 2. What round 2 actually yielded

| | n |
|---|---|
| New to round 1 | 297 |
| Hydrated | 297 |
| **No abstract at all** | **85 (29%)** |
| Method layer flagged | 25 (8.4%) |
| **Exposure × fertility outcome** | **15** |
| … and identification vocabulary in the abstract | 3 |

By arm, the 15 are **composite 15, Arm S 0, Arm B 0** — as expected, since all four seeds were
composite. **Round 2 does not extend Arms S or B and must not be read as evidence about them.**

The identification filter is unreliable at this level and is reported, not applied: these are small
development and public-health journals whose abstracts often do not name the estimator. All 15 go
forward to screening.

## 3. The stratum that was "empty" three hours ago

Round 2's 15 include a coherent sub-literature on microfinance and fertility that round 1 reached none
of. Two are worth naming now.

**Islam, Kamal and Nguyen 2026, *Journal of Development Studies* — "Microcredit Participation and
Fertility: Evidence from Bangladesh".** A household panel for 1997–2005 *designed specifically to
evaluate microcredit programmes*, using difference-in-differences combined with matching. It finds
**access to microcredit associated with lower recent fertility and fewer births**. (Caution: the title
query resolves first to a Figshare deposit, `10.6084/m9.figshare.32612390`. The *JDS* article is the
version of record and the two must not be counted twice — the third version pair this chapter has hit.)

**Orton, Pennington, Nayak et al. 2016, *Bulletin of the WHO* — a systematic review of health impacts
of group-based microfinance**, over "one cluster-randomized control trial and 22 quasi-experimental
studies". A review of an adjacent outcome set, but it is an **external-authority anchor source with a
23-study evidence base**, and whether it carries fertility or contraceptive outcomes should be checked
directly — that is a cheaper route to the remaining studies than another snowball round.

Also present: *Financial Inclusion and Its Impact on Fertility* (2023), *Does financial development
influence fertility rate in South Asian economies?* (2020), two papers on microfinance participation
and contraceptive use (2016, 2018), and a Kenya paper on financial inclusion and fertility decline
(2022).

## 4. Refinement to the sign reading, which moves against what I said earlier

With Islam et al. added, the composite stratum's realized-fertility evidence is:

| Study | Design | Realized fertility |
|---|---|---|
| Desai and Tarozzi 2011 | RCT, credit-only arm | −0.106 to −0.166 (small, some significant) |
| Islam, Kamal and Nguyen 2026 | DiD + matching, purpose-built panel | lower recent fertility, fewer births |
| Küchler 2012 | DiD + IV | no significant effect |
| Steele et al. 1998 | quasi-experimental panel | no significant effect |

Against desires and intentions: Desai and Tarozzi's **desired family size +0.38 to +0.40**, Lan et al.'s
fertility intentions positive.

**So the earlier statement that "the direction runs against Arm S" was drawn from the desires arm alone
and is too strong.** On *realized* fertility the evidence leans to Arm S's predicted negative — two
negatives and two nulls. On *stated desires* it goes the other way. The outcome-level split is
therefore sharper than first reported, not weaker: the two outcome levels do not merely differ in
magnitude, they carry **opposite signs from the same exposure**, and `OUTCOME_LEVEL` is load-bearing
for the chapter's verdict rather than for its bookkeeping.

## 5. Bounds

- **85 of 297 round-2 records (29%) have no abstract**, so the scorer cannot see them. The 15 is a
  floor, not a count.
- Every reading above is from abstracts or a skim of headline sentences. Signs, magnitudes and
  significance are extraction-stage facts and three of these four are not yet retrieved.

## 6. Next

1. Screen the 15 properly, and pull the Orton review's included-study list — a 23-study review is a
   cheaper anchor mine than a third snowball round.
2. Retrieve Islam et al. 2026 (*JDS* version of record, not the Figshare deposit).
3. **Arms S and B still rest on round 1.** Round 2 extended only the composite cell; a round seeded
   from Arm S and Arm B candidates is a separate job and should not be skipped because this one paid.
