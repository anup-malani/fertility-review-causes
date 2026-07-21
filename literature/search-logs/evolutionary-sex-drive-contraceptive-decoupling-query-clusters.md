# Query clusters — evolutionary sex drive and contraceptive decoupling

**Hypothesis:** B.1 (`HYPOTHESES-v5.md`) · slug `evolutionary-sex-drive-contraceptive-decoupling`
**Stage:** A2 (cause-axis clustering) — written after A1 scope, before A3 anchor sourcing
**Status:** provisional five-family design; the operational count is confirmed or collapsed by the
post-A3 §7.2 retrieval-overlap test, not here.

---

## 1. Why cluster

Following the OAS clustering method (`old-age-security-pension-crowdout-query-clustering-method.md`
§2): decompose the hypothesis into vocabulary families so economics, demography, evolutionary biology,
and the psychology of fertility are each searched *on their own terms*, and so the eventual search
budget is allocated across families observably rather than spent on one broad relevance query. Union,
not intersection — a paper written in only one disciplinary vocabulary is retained, not dropped.

## 2. The effect axis (shared — held out of every overlap test)

The fertility outcome vocabulary is constant across all cause-axis families and is therefore **held
out** of the pairwise overlap computation (per `38_cluster_overlap.py`: including the shared axis
would wash every Jaccard toward 1):

- realized fertility, births, TFR, completed fertility, number of children, offspring count;
- **B.1-specific extension:** desired vs. realized/wanted fertility, ideal family size, intended
  parity — the "preference held fixed" clause that distinguishes B.1 from A.2.

## 3. The five cause-axis families

| # | Family | Discriminative term core | Scope cell(s) | Counts toward empirical recall? | Discipline |
|---|---|---|---|---|---|
| 1 | **evolutionary-biosocial-theory** | selfish gene, parental investment, inclusive fitness, life-history, r/K, evolutionary mismatch, maladaptive fertility, Darwinian × fertility, natural selection × fertility | `THEORY` | No — theory stream | evolutionary biology, biosocial demography |
| 2 | **proximate-ultimate dissociation** | proximate vs ultimate, sex drive, mating effort, *mating success vs reproductive success*, status/wealth × fertility reversal, social vs reproductive success | `PROXIMATE_ULTIMATE` | Yes | evolutionary psychology, human behavioral ecology |
| 3 | **decoupling / severing** | decoupling, dissociation, severing, uncoupling, sex without conception/reproduction, delink, break/sever the link, disconnect fertility from | `PRIMARY_DECOUPLING`, `SEX_FERTILITY_TREND_DECOUPLING` | Yes | demography, sociology of the SDT |
| 4 | **childbearing-motivation / demand-for-children** | childbearing motivation, desire for children, traits-desires-intentions (TDIB), positive/negative childbearing motivation, procreative drive, no maternal instinct, nurturance | `MOTIVATION_DISTINCTNESS`, `PRIMARY_DESIRE_INDEPENDENCE` | Yes | psychology of fertility |
| 5 | **contraception-as-severing-technology** (bounded) | contraceptive access/adoption *as the severing technology*, the Pill, oral contraceptive, fertility-control technology — with the **A.2 wall** | `CONTRACEPTIVE_MEDIATION` | Yes | demography, economics of contraception |

## 4. Design-time overlap read (provisional — empirical test is post-A3)

The binding §7.2 test — Jaccard ≥ 0.60 on *retrieved gold sets* — cannot run until A3 builds the gold.
What follows is the a-priori conceptual/vocabulary read that fixes the provisional count; A3's gold
confirms or collapses it.

- **3 ↔ 5 (decoupling ↔ contraception-technology) — the watch-pair.** Decoupling is the outcome;
  contraception is the mechanism that produces it, so many papers name both. Most likely to collapse to
  one operational cluster on the post-A3 Jaccard. Kept as two *search* buckets anyway, because family 5
  is exactly where **A.2 leakage** enters and needs its own bounded vocabulary and the routing wall,
  whereas family 3's dissociation terms are B.1-clean by construction. *Separate at search, expect
  merge at budget.*
- **1 ↔ 2 (theory ↔ proximate-ultimate) — semantic overlap held apart on purpose.** Family 2 is the
  empirical instantiation of family 1's ultimate claim and shares "evolution/Darwinian" vocabulary, but
  1 pulls pure theory (no fertility estimate, does not count toward recall) and 2 pulls the
  status→sex-vs-reproduction empirical tests (Pérusse-type) that do. The recall/theory-stream wall in
  the scope keeps them distinct even where vocabulary overlaps.
- **4 is cleanly its own family** — Miller's TDIB vocabulary shares almost nothing with the other four;
  it is the bridge to "child preference held fixed."

**Provisional operational count: five vocabulary families.** Honest expectation for the post-A3 budget
count: **3–4** (3+5 the probable merge; 1+2 a vocabulary overlap the recall wall deliberately
preserves). The five-way split is carried into A3 so anchor sourcing samples every family — at least
one primary-decoupling, one proximate-ultimate, one motivation, one theory, and one bounded-
contraception anchor — and the eventual search is tested on routing across all five, not just topical
retrieval.

## 5. Caveats

1. This is a **conceptual/vocabulary** overlap read, not the retrieval-overlap test. Two families that
   mean different things can still be one operational cluster if they pull the same papers; only the
   post-A3 gold Jaccard settles that.
2. Term cores are the discriminative centers of each family; broadening them shifts individual cells
   but not the block structure (near-synonym pairs stay high, genuinely distinct families stay low).
3. The five semantic families are worth naming in the query log for vocabulary coverage even if the
   operational budget count collapses to three or four.
