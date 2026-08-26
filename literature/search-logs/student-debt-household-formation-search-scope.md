# Search scope — student debt and household formation

**Hypothesis:** C.3.g (HYPOTHESES-v5.md)
**Hypothesis slug:** `student-debt-household-formation`
**Target phenomenon:** SDT only, as enumerated. Mass education debt is a post-1990 phenomenon
concentrated in Anglophone systems; there is no PM or FDT exposure to rate. As with A.17, the
chapter states the absence of the exposure rather than rating an absence of evidence.
**Ticket:** TICK-073
**Status:** **DRAFT** (Shravan, 2026-08-26). Eight walls, seven estimand cells, five PI calls. Not
frozen: Calls 1 and 5 change the chapter's shape and should be settled before the production pull.

Counts below are regenerable via `source/build/goldset/199_c3g_recon_probe.py` (55 requests, 0
failed) and `source/build/goldset/200_c3g_chain_probe.py` (16 requests, 0 failed), reported in
`student-debt-household-formation-recon-probe.md` and `-chain-probe.md`.

Built on the A.17 template, which inherits A.12's, D.3.c's, B.7's, B.6's, B.5's, D.2.d's and
D.3.b's. Six constraints carry forward as design decisions rather than being rediscovered:

- the taxonomy carries `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER`;
- a wall whose discriminator is invisible in a title or abstract is declared unenforceable up front
  rather than trusted and audited later;
- an arithmetic statement of the mechanism is an upper bound to be corrected, not the effect;
- a chapter whose evidence sits on a different proposition from its claim rates **the claim**;
- Tier-A anchors are studies in their own right, not an artifact of the screen;
- failed requests are bucketed separately from zero-hit counts, so an absence means absence.

## Causal claim

Education debt service during prime childbearing years reduces the effective household resources
available for family formation — delaying or blocking marriage, homeownership, and childbearing —
in cohorts that came of age under the post-2000 student-debt regime.

## The identified variation and the registered outcome are in different literatures

This is the structural fact that shapes every downstream decision, so it is stated before the walls
rather than discovered during extraction.

| Cell | n | Identified subset |
|---|---|---|
| student debt × a fertility outcome | 107 | **2** |
| student debt × marriage or union formation | 181 | 5 |
| student debt × homeownership or household formation | 169 | 11 |
| student debt × an explicit identification strategy, **any** outcome | 210 | — |

The identified body is real and it is good: Rothstein and Rouse (*JPubE*, 457 cites; indexed 2010, in print 2011) on
occupational choice, Mezza, Ringo, Sherlund and Sommer (2019, *JOLE*, 113) on homeownership using
linked credit-bureau panels, Gicheva (2016, *EER*, 86), Bozick and Estacion (2014, *Demographic
Research*, 61), Addo (2014, *Demography*, 193), Houle and Warner (2017, *Sociology of Education*,
109) on returning to the parental home. **None of it estimates a birth.**

The two records in the identified-fertility cell are a study of graduate *employment* and an
unpublished dissertation. Read directly, the policy-variation cells are empty in the same way:
loan forgiveness or cancellation × fertility returns 5 records, all of them medical debt-management
advice and a veterinary career survey; repayment-plan reform × fertility returns 3, the same
records; student debt × an aggregate birth rate returns 9, none on topic. **There is no natural
experiment in student debt with a fertility outcome anywhere in the indexed literature.**

What the direct cell does contain is a small associational body, and it is a real one: Nau, Dwyer
and Hodson (2015, *RSSM*, 93), Min and Taylor (2018, *Demography*, 31), and four smaller works.
Roughly four to six studies, panel and hazard designs on NLSY/PSID-class data, no exogenous
variation in the exposure.

## Which makes this a chain chapter, and the chain is only partly ours

v5's claim names the intermediate outcomes in its own words — *"delaying or blocking marriage,
homeownership, and childbearing"*. So the chain

```
education debt  →  household formation (marriage, homeownership, residential independence)  →  births
        LINK 1: identified, ~12 studies, C.3.g's own            LINK 2: not C.3.g's parameter
```

is the registered mechanism, not a substitution for it. **This is the distinction from A.24**, where
the identified variation turned out to belong to a neighbouring hypothesis and the chapter had to say
so. Here link 1 is in scope by the claim's own text.

**Link 2 is another chapter's parameter and must be borrowed, not estimated here.** Marriage timing
to births is A.7; co-residence to births is A.23; housing tenure to births is C.2.c, whose chapter is
already run and whose finding was that the sign is tenure-conditional. B.7's lesson governs what the
chain can then support: a three-link chain is only as strong as its thinnest link, and B.7's had one
record in link 2. C.3.g's link 2 is not thin — it is large and *unidentified*, which is a different
failure and produces a different verdict. The chapter reports the two arms separately:

- **Arm 1 — the direct arm.** Student debt → a fertility outcome. Small, associational, and rating
  the claim's own estimand. This is what the GRADE rating attaches to.
- **Arm 2 — the chain arm.** Student debt → household formation, identified, then transported through
  a link-2 elasticity taken from A.7 / A.23 / C.2.c with the borrowing made explicit. **A bound and a
  mechanism demonstration, not an estimate of the claim.** It does not pool with arm 1; the two do not
  share an estimand, let alone an estimator.

## The anchored vocabulary has its own homonym, again

Following the A.17 rule, the tighter-looking vocabulary was scored before it was trusted, and it was
worse than the loose one. The `OWNDEBT` block — designed to isolate the young adult's own burden with
terms like `"debt burden"` and `"loan burden"` — returned 96 records whose citation head is
**sovereign debt**: *The Lost Decades: Developing Countries' Stagnation* (563 cites), *The impact of
COVID-19 on African economies* (123). The bare phrase `"debt burden"` sits in a 1,389-record
developing-country-debt literature. One unanchored term re-admitted a cloud the block existed to
exclude — the same failure as A.17's `"birth rates"`, in a chapter with no clinical literature
anywhere near it.

Two further vocabulary facts, both measured:

- **`"residency"` is a homonym** — medical residency against residential independence. It sits in the
  wall-1 block and the housing block simultaneously and cannot be used in either without the other's
  context.
- **The ecology sense does not reach this frame.** `"student loan" AND ("soil fertility" OR "crop
  yield")` returns 0. The `"fertility"` homonym that dominates A.17 is absent here, so the plain and
  anchored outcome vocabularies can both be used, and the frame is drawn on the loose one.

## Frame sizes, as measured

| Frame | n |
|---|---|
| The whole student-debt literature | 11,379 |
| **Retrieval frame: debt × (fertility ∪ union ∪ housing), deduped** | **394** |
| debt × fertility alone | 107 |
| Health-professions debt × career choice (Wall 1) | 720 |
| Loan default and repayment behaviour (Wall 3) | 706 |
| General household and consumer debt × fertility (Wall 2) | 82 |
| Parents saving for a child's tuition × fertility (Wall 5) | 180 |

**394 records is the whole frame.** It is small enough to screen entire, with no budget slice and no
D1 ranking cutoff — the first chapter in the series where that is true. Screen cost is not the
constraint; it never has been.

## Walls

| # | Wall | Size | Enforceable at title/abstract |
|---|---|---|---|
| 1 | **Health-professions debt studied for career choice.** Specialty choice, practice location, workforce shortages. The outcome is a career, not a birth. | 720 | Yes — **by outcome, not by topic** (see below) |
| 2 | **General household and consumer liabilities.** Mortgage, credit-card, medical, payday debt. This is C.3.e (credit constraints) and C.2.c (housing). | 82 | Yes; overlap with student debt named is 8 records |
| 3 | **Default, delinquency and repayment behaviour** with no household outcome. | 706 | Yes; fertility overlap is 3 records |
| 4 | **Access-to-college effects.** Aid → enrollment, attainment, completion, earnings, with no family outcome. That is the education literature. | — | Yes |
| 5 | **The other balance sheet: parents saving for a child's tuition.** An anticipated cost of a child is C.2.b's exposure. | 180 | Yes — and cheaply: the overlap with student-debt vocabulary is **2 records** |
| 6 | **The third balance sheet: parent-held education debt** (Parent PLUS, borrowing for a child's degree). It sits on the older generation and cannot delay their childbearing. | 57 | Yes |
| 7 | **LMIC school fees and child marriage.** Surfaced by the tuition-regime probe: tuition-free secondary schooling → child marriage and early childbearing in sub-Saharan Africa (*PDR* 2023, 31 cites). Different exposure, different outcome, different phenomenon. Tagged `SECONDARY_LMIC`, not deleted. | 14 | Yes |
| 8 | **The reverse direction.** Childbearing as a *cause* of debt — student parents, borrowing to cover the cost of a child. | 65 | Yes |

**Wall 1 needs a rule, not a boundary,** and it is A.17's rule verbatim: **route by outcome, not by
topic.** The health-professions literature is the largest body sharing this chapter's exposure
vocabulary, and part of it is genuinely in scope — *Medical student debt and major life choices other
than specialty* (118 cites) and *Influence of Student Loan Debt on General Surgery Resident Career and
Lifestyle Decision-Making* (35) both report childbearing decisions. The overlap cell is 19 records. A
paper is in if it reports a family-formation outcome, whatever the sample's occupation; out if the
estimated quantity is a specialty, a practice location, or a workforce count.

**Wall 6 carries a warning about its own probe.** The block used to size it —
`"Parent PLUS" OR "parent borrowers" OR "parental student loans" OR "borrowing for a child"` — is
contaminated: crossed with fertility vocabulary it returns plant-breeding records (*intertribal
somatic hybrids*, *parental combination*, *hybrid sterility*), because "parental" and "sterility" are
plant-genetics terms. The wall is real and near-empty; **the block must not be reused for retrieval.**

**One wall is declared unenforceable at title/abstract up front:**

- **Whether a study conditions on educational attainment.** This is C.3.g's central confound: debt is
  chosen jointly with schooling, and schooling independently lowers fertility (C.3.d, D.2.a), so a
  study that compares borrowers to non-borrowers without holding attainment fixed estimates the
  return to college, not the burden of financing it. Only 8 records in the whole frame name
  attainment-conditioning language anywhere in title or abstract, and the decision lives in a methods
  section. It is a **full-text extraction field and a risk-of-bias domain**, never a screen rule.

## Estimand cells

| Cell | Exposure | Outcome | Expected population |
|---|---|---|---|
| **P1** | Own education debt (balance, incidence, payment) | Births, first birth, completed fertility, childlessness | **Arm 1's core.** 4–6 associational studies; zero identified |
| **P2** | Policy variation in debt (forgiveness, repayment reform, loan limits, tuition regime) | Any fertility outcome | **Measured empty.** Reported as empty, not omitted |
| **P3** | Own education debt | Marriage, cohabitation, union formation | Link 1; identified; Addo, Bozick–Estacion, Gicheva |
| **P4** | Own education debt | Homeownership, housing tenure, residential independence | Link 1; identified; Mezza et al., Houle–Warner, Dettling–Hsu, Goodman–Isen–Yannelis |
| **P5** | Own education debt | Occupational choice, earnings, savings — the resource channel itself | Off-outcome; retained as mechanism evidence only (Rothstein–Rouse) |
| **P6** | Own education debt | Fertility *intentions and expectations* | Small; a stated-preference arm, kept separate from realized fertility |
| **P7** | Debt in a non-US financing regime | Any of the above | Thin and named: England (housing tenure), Japan (family formation), New Zealand |

**P2 being empty is a result, not a gap to apologise for.** The cleanest identification this
hypothesis could have — a forgiveness episode, a repayment-plan discontinuity, a tuition-regime
change — does not exist with a fertility outcome. That fact bounds the GRADE rating before a single
full text is read, and it is the chapter's most transportable finding for anyone proposing to test
this hypothesis next.

**P6 is kept separate on the D.3.b precedent**, where folding intentions into realized fertility was
what made the pool incoherent.

## Anchor sourcing

Tier-A anchors are hand-sourced and are studies in their own right, not screen output — the D.2.d
lesson, where reporting screen output as the evidence base dropped 9 studies to 2. All verified live
in the probes, with citation counts as returned:

*Arm 1 (direct):* Nau, Dwyer and Hodson 2015 (93); Min and Taylor 2018, *Demography* (31); *Social
Norms and Expectations about Student Loans and Family Formation*, *Sociological Inquiry* 2021 (15);
*Parents, Partners, Plans, and Promises*, *Socius* 2020 (19); *Student loan debt and family formation
of youth in Japan*, *Studies in Higher Education* 2024 (3); *Married with Children? The Role of
Student Loan Debt*, SSRN 2019 (2); *The Effects of Student Loan Debt on the Transition to Parenthood*
2012 (1).

*Arm 2 link 1 (identified):* Addo 2014, *Demography* (193); Bozick and Estacion 2014, *Demographic
Research* (61); Gicheva 2016, *EER* (86); Mezza, Ringo, Sherlund and Sommer 2019, *JOLE* (113), with
the 2016/2017 FEDS working versions (21, 47); Houle and Warner 2017, *Sociology of Education* (109);
Dettling and Hsu, *Returning to the Nest*, *Labour Economics* (90; FEDS 2014); Bleemer et al.,
*Debt, Jobs, or Housing* 2014 (66); Goodman, Isen and Yannelis, *A Day Late and a Dollar Short*,
*JFE* 2021 (60); *Does Student Loan Debt Structure Young People's Housing
Tenure? Evidence from England*, *Journal of Social Policy* 2021 (14).

*Mechanism / off-outcome:* Rothstein and Rouse, *JPubE* (457; indexed 2010).

*Reviews:* *Graduate indebtedness: its perceived effects on behaviour and life choices*, Birkbeck
2018 (20) is the only review-shaped record in the frame. **Channel 1 of the cold-start bootstrap is
effectively empty here** — there is no prior systematic review to inherit an included-study list
from — so the gold comes from channels 2 and 3, and the existence gate does more work than usual.

**v5's own seminal list for C.3.g does not resolve and must not be cited from memory.** It names a
policy-institute report ("TICAS / Contemporary Families 2025"), a forthcoming paper ("Butcher and
Goldsmith"), and a tweet. `title.search` for *Student loan debt and fertility* returns 0. None of the
works listed above appear in v5. This is a HYPOTHESES-v5 maintenance item, not only a C.3.g one: the
entry was written from discourse rather than from the literature, and the literature is better than
the entry suggests.

## A resolver defect found here, which belongs to the shared scaffold

Pass-1 `title.search` returned **zero** for *Can't afford a baby? Debt and young Americans* — the
most-cited work in the primary cell — while the pass-2 author retry found it instantly. Isolated in
`200_c3g_chain_probe.py`:

| Spelling sent to `title.search` | n | Top match |
|---|---|---|
| `Can't afford a baby` (straight) | 1 | *the wrong paper* — a neonatal-injury editorial |
| `Can’t afford a baby` (curly) | 1 | *the wrong paper* — same |
| `Cant afford a baby` | 0 | — |
| `afford a baby debt and young Americans` | 1 | **correct, rank 1** |
| `Debt and young Americans` | 8 | **correct, rank 1** |

The apostrophe-bearing token is what breaks the query, and de-punctuating it (`Cant`) makes it worse,
not better. **The rule for the shared resolver: drop the apostrophe-bearing word from a title query;
do not strip the apostrophe inside it.** This compounds the known `norm()` punctuation defect —
there, patterns containing punctuation were dead code; here, punctuation in a *query* returns a
confident wrong match at n=1, which is worse than a zero because it passes a "did we find something"
check. Every chapter's pass-1 named-work resolution is exposed to it.

## PI calls

1. **Does the chapter carry the chain arm at all?** *RA recommendation: yes — both arms, arm 1 rated
   and arm 2 reported as a bound, never pooled, with link 2's elasticity explicitly borrowed from
   A.7 / A.23 / C.2.c and cited as borrowed.* Reporting only arm 1 discards every identified estimate
   in the literature; reporting only arm 2 states another chapter's parameter as this one's finding.
2. **Cohort and period restriction.** v5 restricts the claim to post-2000 cohorts, but the strongest
   arm-1 studies use NLSY79/NLSY97 cohorts borrowing at balances an order of magnitude smaller. Does
   the chapter include them? *RA recommendation: include, tag by exposure era, report separately, and
   do not average across eras — the same reasoning that says disagreeing studies should be resolved
   rather than pooled.*
3. **What identification standard does arm 1 have to meet?** Requiring attainment-conditioning drops
   most of arm 1. *RA recommendation: do not gate on it; extract it as a graded field and let the
   risk-of-bias instrument carry it, with a separate domain for the schooling confound.*
4. **Non-US scope.** The body is US-dominant with three named exceptions. *RA recommendation: rate a
   US parameter, state the bound, and report England, Japan and New Zealand as external-validity
   checks rather than as pooled evidence.* Note that income-contingent systems (England, Australia)
   change the mechanism itself — a repayment obligation that scales with income is a different
   constraint from a fixed one — so they are not simply a different setting.
5. **The demographic-significance denominator, and the arithmetic that precedes it.** Two decisions:
   (a) is the exposed population all women, all college-goers, or all borrowers? These differ by
   roughly a factor of three and change the verdict, not the number. (b) The SDT decline runs from
   1965 and mass education debt is post-2000, so **the share of the SDT decline that predates the
   exposure bounds this mechanism before any effect size is applied** — B.7's arithmetic, where 67.6%
   of the decline predated the exposure. That bound is computable now, from a TFR series and a
   citable debt-exposure series, and it should be computed before extraction rather than after.

## Retrieval risk to flag early

The exposure series this chapter needs — outstanding balances, share of a cohort holding debt,
average balance per borrower — lives in institutional publications (NY Fed Consumer Credit Panel
quarterly reports, the Survey of Consumer Finances, College Board *Trends in Student Aid*) that are
largely **not indexed as works**. The probe's credit-panel cell (193 records) is topic papers citing
those series, not the series. Plan for a hand-sourced, manually cited exposure series, and expect the
A.17 pattern where the demographic-significance table is generated from a computed JSON rather than
typed.

## What runs next

1. **A3** — cold-start anchor resolution and the existence gate over the Tier-A list above, with the
   pass-2 author-retry fix and the new apostrophe rule both applied.
2. **A4** — Tier-B frame construction on the loose vocabulary: the 394-record union frame, deduped
   against version duplicates.
3. **D1/D2** — a two-stage screen over the whole frame with no budget slice, carrying
   `INSUFFICIENT_INFO`, `OFF_OTHER`, and an explicit **arm-1 / arm-2 / link routing field** rather
   than a single relevance verdict. Unlike A.17's, this routing is largely visible at title and
   abstract, because the outcome word is what distinguishes the arms.
4. **Before extraction:** the P2-empty finding and the pre-2000 share-of-decline bound, both computed
   and written into the scope as frozen inputs to stage 10.

## A3 addendum (2026-08-26)

Anchor resolution is run: **24 candidates, 20 verified live, 1 year-drift keep, 1 flagged, 2 expected
index misses** (`201_c3g_cold_start_anchors.py`). The empirical recall denominator is **5** — three
realized-fertility anchors and two intentions — against ten chain-arm anchors. That ratio is the
scope's central finding restated as a count.

Two corrections the run forced, both from sourcing authorship through Crossref rather than memory:
*Returning to the Nest* is **Dettling and Hsu**, not Bleemer et al., and *A Day Late and a Dollar
Short* is **Goodman, Isen and Yannelis**. Both are fixed above. The candidate misattribution rate on
a hand-written anchor set is not zero, and this is the second chapter in a row to measure it.

Three of the run's predicted failures failed as predicted and are load-bearing for the scope:
the **negative control** (*Student loan forgiveness and the timing of first births*) did not resolve,
independently corroborating the measured-empty P2 cell; the **SCF serial** could not be anchored,
confirming the exposure-series retrieval risk; and the **only review-shaped record in the frame** was
refused by the author gate, confirming that Channel 1 of the cold-start bootstrap is empty here.
