# Primary-pool de-duplication, retrieval and first extraction — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Scripts `296`–`299` ·
Outputs: `extraction/credit-constraints-effects.csv`, `credit-constraints-{primary-retrieval,version-pairs,extraction-candidates}.json`

## 1. Three version pairs, and title matching found none of them

`296` de-duplicated the 62-record primary pool on folded title and returned **zero** pairs, in a pool
where two were already known by hand. Both escape title equality, differently:

- *"…Evidence from an Aging **Society**"* (2026) vs *"…Evidence from an Aging **Economy**"* (2024) —
  one word changed between versions.
- *"BEQUEST RECEIPT AND FAMILY SIZE EFFECTS"* (2010) vs *"Do Credit Constraints Explain Family Size
  Effects? Tests Based on Bequest Receipt and Family Earnings"* (2005) — **no shared title**, Jaccard
  about 0.43.

`297` replaces title equality with two author-gated rules — Jaccard ≥ 0.75 **and** first-author
agreement **and** years within ten; or full containment of the shorter title **and** first-author
agreement. Containment without the author gate would be unsound, since a short generic title sits
inside many longer ones.

The rules **re-found both hand-declared pairs**, which is the recall check on the rules, and **proposed
a third that I had missed**: *Impact of the Grameen Bank on Women's Status and Fertility* and
*Assessing the Impact of the Grameen Bank on Women's Status and Fertility*, same first author,
J = 0.875. Nothing is auto-merged; the proposals are printed for a human read.

**Primary pool: 62 records → 59 distinct studies.**

## 2. Retrieval: 12 of 62, and Arm S is retrieval-bound

| Rung | Found a URL | Fetched |
|---|---|---|
| `oa_self` | 23 | 11 |
| `oa_twin` | 3 | 1 |

| Cause of failure | n |
|---|---|
| no open URL at any rung | 36 |
| browser-job (open URL, 403 bot defence) | 9 |
| proxy-job (no open copy) | 5 |

**Arm S: 3 of 16 retrieved.** The thirteen outstanding run 1971–2019 and include the whole classic
insurance-motive literature — *The No-Birth Bonus Scheme* (1980), the Cain risk-and-insurance exchange
(1986), *Savings Behaviour, Fertility and Economic Development in Nineteenth Century Britain* (1987),
*Risk, Consumption Smoothing and the Family* (1991). **Two of the chapter's three FDT-era Arm S records
are unretrieved.** An Unpaywall spot-check on the "no URL" group confirmed the verdict rather than
overturning it: 25 of 36 have a DOI and the ones tested return no OA location.

This is the B.1 problem again — a chapter whose oldest and most on-estimand arm is the least open.

## 3. First extraction rows, and the headline is a sign flip

Four effect rows from three studies. Two matter:

**The sign flip, measured directly.** *Fertility choice and financial development* (145 countries,
1980–2006): an increase in private credit of one standard deviation **decreases fertility by 1.7–5% in
low-income countries and increases it by 3.7–5% in high-income countries.** That is precisely the
question Ruling 1 said makes C.3.e one chapter rather than two — Arm S dominant where finance is thin,
Arm B dominant where it is deep — and here it is inside a single estimate.

**But it is not identified.** Cross-country aggregate panel; endogeneity tested for GDP and female
labour-force participation only, with no instrument for credit. Under the scope memo's rule on
aggregate designs it goes to the **secondary pool**. So the chapter's central claim currently rests on
an unidentified aggregate correlation, alongside Desai and Tarozzi's randomised null. Both belong in
the synthesis and neither can carry it alone.

**The FDT-era Arm S estimate.** *Fertility and Financial Development: US Counties in the 19th Century*:
the presence of a bank in a county around 1850 is associated with a child-woman ratio lower by about
3 percentage points, and a crude birth rate lower by about 5%. OLS on a county cross-section — again
associational. And the authors read it as support for **the old-age-security motive**, which is C.3.c's
under Wall 1. Its routing needs the PI ruling that is already open.

**All four rows are `identified: NO`.** That is the state of the extractable evidence today, and it is
worth stating plainly before any GRADE rating is contemplated.

## 4. A validation script written because I repeated my own mistake

I hand-typed an OpenAlex id into the extraction table **one hour after recording the lesson that says
never to do that**, and it was wrong. Nothing in the CSV would have revealed it: the study name was
right and the estimate was right, and the row would have attached to a nonexistent — or worse, a real
but different — record.

`299` now validates every row: id exists in the retrieval record; the id's stored title matches the
row's study name; `OUTCOME_LEVEL` is from the closed list (blank is not a missing tag here, it is a
missing finding, since this chapter's composite studies carry opposite signs at different outcome
levels); `estimator_class` is from the closed list so an unlisted correction fails loudly rather than
pooling with what it should be separated from; `identified` is YES/NO.

## 5. Next

1. Extract the remaining 10 retrieved texts.
2. **The retrieval handoff is the binding constraint: 50 studies, 9 browser-jobs and 41 needing library
   access.** Arm S cannot be rated until a substantial part of it is read.
3. The PI ruling on Wall 1 now has a concrete case attached — the 19th-century US counties study is an
   Arm S record whose authors frame it as old-age security.

---

## Addendum, 2026-09-01: the first full-text check reversed a screen decision

Shravan retrieved from the Tier 1–3 priority list. **One file arrived** — Lafortune and Lee, *All for
One? Family Size and Children's Educational Distribution under Credit Constraints* (Tier 1, item 5) —
and reading it changed its routing.

**Family size is a regressor, not the outcome.** The dependent variable is children's education:
Table 1 is *"Family Size and Education Level"*, Table 2 *"Birth Order and Years of Education"*, and the
cited follow-on is *"Effect of Family Size and Birth Order on Child Outcomes"*. Credit constraints
enter as a **moderator** of the family-size-to-education relationship. There is no fertility outcome,
so **Wall 6 routes it out**: re-cellled `MECHANISM_NO_FERTILITY`, cross-referenced to C.3.d.

Two corrections follow, both mine:

- **My screen cell was wrong**, and it was wrong in exactly the way the wave-1 log warned about —
  *"design and outcome values are hypotheses until full text."* This is the first of the 62 to be
  checked against its own text, and it did not survive. It is a reason to expect more of the same, and
  an argument for checking outcome direction at full text before any pooling.
- **My priority note oversold it.** I ranked it Tier 1 as a *"top-five journal, design likely the
  strongest in the arm."* It is **AER Papers & Proceedings**, five pages, not a refereed AER article.
  I ranked a venue string rather than a paper.

**Primary pool: 62 → 61 records** (59 → 58 distinct studies after the three version pairs).
Arm B 14 → 13.

**Still outstanding from Tiers 1–3: everything else.** The two named as unavailable are *Public
policy, risk and fertility in Bangladesh* (1983) and *Savings Behaviour, Fertility and Economic
Development in Nineteenth Century Britain* (1987). The Britain paper was Tier 1 item 2, and with it
unavailable **the FDT-era Arm S cell stands at one of three read** — the US-counties study — with the
rainfall-risk paper still the highest-value outstanding item in the chapter.
