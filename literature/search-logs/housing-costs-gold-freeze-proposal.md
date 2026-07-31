# Gold-freeze proposal — housing costs (C.2.c)

**Drafted:** 2026-07-31, Shravan (TICK-055). **Not yet frozen — needs sign-off.**
**Inputs:** `housing-costs-tier-b-frame-deduped.json` (241), `extraction/housing-costs-ra-gate.csv`
(152 gated, coverage 152/152)

---

## 1. Correcting the question I asked

I flagged that "15 identified studies is below the ≥30 CV floor, so C.2.c may not support a tuned
production query." **That framing was wrong, and the error is worth stating because it confuses two
different objects.**

GACS §7.2's floor reads: *"Bootstrap gold-size floor | ≥ 30 empirical anchors before CV | Below this
the fold-local term mining is too noisy."* The floor sizes the **gold set as a retrieval instrument**
— the anchors that discriminative-term mining and cross-validation run over (A4/B1). It says nothing
about how many studies can be pooled.

The 15 is a **quality stratum inside the estimand cell**, not a different estimand. All 78 surviving
PRIMARY records identify housing price → fertility in the forward direction; 15 of them do so with
credible exogenous variation. Identification quality is the business of risk-of-bias and GRADE, not of
whether a query can be tuned.

**So the correct comparison is 78 against 30, and the floor is comfortably met.**

**And tuning on the 15 would be actively harmful.** Those studies are overwhelmingly recent economics
papers (2010–2026, median 2021). Mining query terms from them would bias the production query toward
well-identified-econ vocabulary and away from the demography, Korean and Chinese literature — which is
precisely the breadth failure the snowball had to correct in rounds 2 and 3. A query tuned to retrieve
only papers we can already tell are well-identified would never surface the ones whose identification
we cannot judge until we read them. **The query's job is retrieval; the estimand gate and the
risk-of-bias pass do the precision work downstream.** That is GACS's own architecture, and the
resolution of the PI's first critique: recall of the target was never the constraint, the target's
definition was.

## 2. Proposed gold

**Tier A — empirical core: 78.** The gated PRIMARY set, every record with a housing-price treatment
and a fertility outcome, carrying its estimand cell and its `id_strength`:

| Cell | n |
|---|---|
| PRIMARY_COST_RENTER | 49 |
| PRIMARY_WEALTH_OWNER | 13 |
| PRIMARY_SPACE_QUANTITY | 11 |
| PRIMARY_COST_RENT_IDENTIFIED | 5 |

**Tier A — theory canon, kept separate: 5.** The `THEORY` verdicts, headed by Mulder & Billari's
homeownership-regime typology. **Does not count toward empirical recall**, per A3.

**Tier B — the unbiased orthogonal sample: the 100 topically-relevant frame records** (78 PRIMARY + 15
`DEMOTE_TENURE` + theory + `AGGREGATE_UNSPLIT` + `AFFORDABILITY_RATIO`). Tier B is a *topical*
yardstick, so the tenure and affordability papers belong in it even though the price-variation ruling
keeps them out of the pooling set.

**Channel integrity holds.** Every frame record is citation-reachable — the frame was built from the
snowball pool, i.e. channel 3 — so Tier B carries no channel-4 keyword contamination. This was the
constraint flagged at anchor-sourcing, and it is satisfied without further pruning.

## 3. Two recall targets, per E3

- **Topical recall** measured against Tier B (100).
- **Estimand-filtered recall** measured against the 78.

**Both should be reported with the caveat established in the snowball log §3:** C.2.c's Tier B is
genuinely keyword-reachable — the 82% snowball-only figure was a breadth miss, not vocabulary
invisibility — so a high Recall(B) here is close to guaranteed and correspondingly uninformative. It
must not be quoted as evidence that GACS generalises.

## 4. The FDT cell is thin and mostly associational — but not empty

*(An earlier draft of this section claimed the FDT cell was **entirely** associational. Checking the
gate before asserting it showed that is false, so the claim is corrected here rather than shipped.)*

The 15 identified studies were published **2010–2026, median 2021**: credible identification in this
literature is overwhelmingly a post-2010 practice. But *publication* year is not *coverage* year, and
two of the fifteen reach back:

- **`Homes and husbands for all: Marriage, housing and the baby boom`** — post-war US housing
  expansion → marriage → the baby boom. Squarely FDT, and in the identified set.
- **`Do surging house prices discourage fertility? Global evidence, 1870–2012`** (Li 2024) — the
  long-run panel, though see §5.1: its QUASI_EXP label is the one most in need of confirmation.

Against that, the rest of the historical material is associational: *Do higher rents discourage
fertility? (US cities 1940–2000)* is a long panel without exogenous variation, and the pre-2000
publications are the crowding and apartment-living studies of 1975–1995.

**A related correction on the 1937 paper.** *Housing and the Birth Rate in Sweden* (ASR, 1937), which
the snowball log flagged as a notable historical find, did **not** reach the gate: the screen routed it
`AGGREGATE_UNSPLIT` on a tenure reading, because its subject is Sweden's **public-housing programme**
rather than a price. It stays in Tier B as topical evidence and should be read at full text, but it is
not currently in the empirical core, and the snowball log's framing of it slightly oversold it.

**So the per-phenomenon shape:**

- **SDT** — 15 identified studies (13 of them SDT-period), opposing tenure channels; a modest but
  defensible base.
- **FDT** — a real literature, but **one clearly identified study plus one contested one**. A GRADE
  rating above *low* would be hard to defend, and the chapter should say so plainly rather than let
  the admitted historical studies imply more weight than they carry.
- **PM** — nothing, as the scope predicted.

Worth putting to Anup alongside the `phenomena` field question, because it clarifies what admitting
FDT evidence buys: coverage and honest description, with a little causal weight, not a second
well-evidenced phenomenon.

## 5. Before the freeze

1. **The `id_strength` labels are provisional.** *(§5.1)* They were assigned from titles and abstracts, and
   design claims need confirming at full text. Li 2024's global 1870–2012 panel in particular is
   marked QUASI_EXP on its framing; if it is panel fixed-effects without an instrument it is
   associational, and it is currently the only pre-2010-coverage study in the identified set.
2. **Retrieve full text for the 78**, prioritising the 15. Tenure conditioning, treatment type,
   parity, and tempo-vs-quantum are all full-text facts (scope doc, "When to adjudicate").
3. **Resolve the 5 remaining `UNCERTAIN_NEEDS_FULLTEXT`.**
4. **Existence-verify every Tier A and Tier B record** against a live DOI before it enters a recall
   denominator. 40 frame survivors are preprint-only or DOI-less and need explicit dispositioning —
   grey literature is kept and flagged, not dropped, but it must be confirmed to exist.
5. **Then freeze**, and only then mine terms.
