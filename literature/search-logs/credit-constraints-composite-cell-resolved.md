# The composite cell, resolved — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Scripts `284`–`286` (+ `285` round 2) ·
PDFs hand-retrieved by Shravan into `temp/c3e-handoff/`
Outputs: `credit-constraints-handoff-install.json`, `credit-constraints-handoff-outcome-scan.json`,
`credit-constraints-snowball-round2.json`

These are **skim-level readings of headline claims, not extraction.** Exact estimates, standard
errors, samples and windows come at stage 7.

---

## 1. Installation: matched by content, because filenames cannot be trusted

Eight PDFs arrived publisher-named — `749desai.pdf`, `1-s2.0-S0304387815000061-main.pdf`, and **two
files both called `EBSCO-FullText-09_01_2026.pdf`**. Installing those by guessing from the filename is
how a wrong pairing enters the extraction table and stays there silently.

`284` matches each PDF on **its own first-page text** against the eight expected records — title-token
overlap, first-author surname, year — and assigns one-to-one. **All eight matched at title overlap
1.00**, and the two opaque EBSCO files were confirmed by hand against their own first pages: one is
Küchler's *Do Microfinance Programs Change Fertility?*, the other Lan et al.'s digital-financial-inclusion
paper.

## 2. The probe bound is closed: 10 of 10, zero fertility outcomes

| Study | Hits | In table / outcome-list context |
|---|---|---|
| Attanasio et al. (Mongolia) | 3 | 0 |
| Bruhn and Love (Mexico) | 0 | 0 |
| Guinnane (credit cooperatives) | 0 | 0 |
| Prina (savings accounts) | 1 | 0 |

All four hits read by hand: *"Number of children in the HH younger than 16 years"* in a
variable-definition table, and a summary-statistics row. **Baseline covariates, not outcomes.**

With the six from `281`, **ten of ten composite and savings-access probes have now been read in full,
and not one estimates a fertility outcome.** The earlier finding is no longer a bound — it is closed.

## 3. And the cell is nevertheless populated — by a different literature

The same scanner, same code path, on the four boundary-spanning candidates:

| Study | Hits | Strong | Design | Headline on fertility |
|---|---|---|---|---|
| Desai and Tarozzi 2011, *Demography* | 340 | 35 | **RCT, credit-only arm separately randomised** | see below |
| Lan, Pan and Yu 2023, *Applied Economics* | 181 | 23 | IV, provincial index | fertility **intentions** positive |
| Steele, Amin and Naved 1998 | 131 | 16 | quasi-experimental panel | "savings- or credit-group membership has **no significant effect** on recent fertility" |
| Küchler 2012 | 122 | 20 | DiD + IV | "**no significant effect** on fertility from participation in or access" |

### Desai and Tarozzi is the identified estimate the stratum needed

The design is four randomly allocated groups: **credit + family planning · credit only · family
planning only · control**. **The credit-only arm is separately randomised**, which is exactly the
condition that makes this a clean composite financial-access estimate rather than a bundled one.

What it finds, on the same experiment:

- **Number of births in the previous three years: all estimates negative, some statistically
  significant, magnitude always small — between −0.106 and −0.166.**
- **Desired family size: microcredit +0.38 to +0.4 (significant at 5%)**; family-planning areas +0.42;
  both-services areas +0.27.
- Intention to use contraception: microcredit −9% (significant at 10%).
- The authors' own reading: *"these results are consistent with microcredit leading to an increase in
  the demand for children."*

## 4. What the stratum now says, and why `OUTCOME_LEVEL` is carrying the chapter

Across the four studies a consistent pattern appears, and it is a pattern **in the outcome level, not
in the exposure**:

- **Realized fertility: null.** Three independent designs — an RCT, a DiD-with-instrument, and a
  quasi-experimental panel — find no significant effect of credit access on births.
- **Stated desires and intentions: positive.** Desired family size rises with microcredit in the RCT;
  fertility intentions rise with digital financial inclusion in the IV study; contraceptive intention
  falls.

So a single composite exposure produces **opposite-signed answers depending on which outcome variable
is read**, and the RCT contains both within itself. Two consequences:

1. **The `OUTCOME_LEVEL` tag pre-registered in the scope memo is not bookkeeping — it is the finding.**
   A synthesis that pooled realized births with stated desires here would average a null against a
   positive and report a small positive that describes neither.
2. **The direction runs against Arm S, not with it.** Arm S predicts that formal saving and insurance
   substitute for children as assets, so access should *lower* desired fertility. In the one randomised
   test available, credit access *raised* desired family size. That is Arm B's sign — liquidity
   relaxed, more children wanted — showing up in the composite cell. It is one experiment in rural
   Ethiopia and it must not be over-read, but it is the opposite of what the registry's PM/FDT
   configuration predicts, and the chapter should say so plainly rather than absorbing it.

**Ruling 1 is unaffected and is, if anything, better supported.** The exposure still cannot be
allocated to an arm — the credit-only arm moves saving and borrowing options together. What has
changed is that the *outcome level*, not the exposure, is what separates the channels' signatures.

## 5. Snowball round 2

Seeded from the four candidates: pool **365**, of which **297 (81%) are new** to round 1 — a
redundancy rate of 18.6%, so the seeds were reaching genuinely unexplored ground, as expected of a
literature round 1's anchors could not see.

**But the yield is heavily contaminated by method citations.** The top new records by citation are
Wooldridge's *Econometric Analysis of Cross Section and Panel Data*, Little and Rubin, Angrist-Imbens-Rubin,
Stock-Yogo, `ivreg2` — backward citations from methods sections, not estimand neighbours. Snowball the
estimand, not the estimator: the round-2 pool needs the method-reference layer stripped before it is
screened. Genuine finds under the noise include Khandker's *Microfinance and Poverty: Evidence Using
Panel Data from Bangladesh*, Montgomery and Casterline's *Social Interactions and Contemporary Fertility
Transitions*, and Goetz and Gupta's *Who Takes the Credit?*.

Note also that Küchler cites Steele et al. — **this literature is internally connected, and round 1
reached none of it.** That is the anchor blind spot measured from the inside.

## 6. Next

1. Strip the method-reference layer from the round-2 pool, then screen it with the round-1 frame.
2. Extract the four composite studies properly, with `OUTCOME_LEVEL` mandatory on every effect.
3. Desai and Tarozzi needs a power read at extraction: a null on births with a 3-year window and a
   small takeup rate may be an uninformative null rather than a precise zero, and the two are recorded
   very differently in GRADE.
