# Cold-start anchors and the Arm S survival probe — C.3.e

**TICK-077 · 2026-09-01 · Shravan**
Scripts: `source/build/goldset/275_c3e_cold_start_anchors.py`, `276_c3e_arm_s_probe.py`
Outputs: `credit-constraints-anchor-candidates.json`, `credit-constraints-cold-start-anchors.json`,
`credit-constraints-arm-s-probe.json`

---

## 1. Anchors: 26 candidates, 26 resolved

| Verdict | n |
|---|---|
| `MATCH` | 17 |
| `MATCH_BY_ID` (inherited from C.2.c, resolved by id) | 8 |
| `MATCH_TITLE_AUTHOR_DISAGREES` (read by hand, confirmed correct — see §3) | 1 |
| `NO_RESULTS` / `QUERY_REFUSED` | **0** |

By arm: Arm S 9 (of which 1 decoy), Arm B 10 (of which 2 decoys and 1 version twin),
composite 5, theory 2. **Nine of the Arm B anchors were inherited already-screened from
C.2.c's `OFF_CREDIT_C3e` cell**, plus the 2026 *PNAS* housing-provident-fund study C.2.c
routed here explicitly and had already extracted (+2.73pp on a 0.1314 baseline).

Tier-A anchors are studies, hand-sourced. The inherited nine are seeds and anchors at once;
they are not a substitute for hand-sourcing, and Arm S was sourced from scratch because
C.2.c's channel could not have surfaced development economics.

---

## 2. The title channel was dead, in this script and every earlier one

**`title.search` is not a root OpenAlex parameter.** The resolver inherited from A.18
(script 245) sent `title.search=<title>` as a top-level query parameter. OpenAlex rejects
the entire request — *"title.search is not a valid parameter"* — so the primary title
channel **failed 18 times out of 18** and every resolution silently fell through to
`search=`, which ranks by relevance across the whole record and is far weaker.

This was invisible because the fallback usually returns the right paper anyway. It was
caught only by counting which channel each match actually came from, which is the
[behavioural audit] rule: the code path being present is not evidence it ran.

The correct form is `filter=title.search:VALUE`. Three further facts, all measured here:

- **A bare comma in a filter value is fatal.** Known.
- **`%2C` does not save it — and the API's own error message tells you to use `%2C`.**
  Sending the recommended encoding returns the identical error. The documented fix is wrong.
- **Wrapping the value in double quotes works**, and keeps phrase matching rather than
  degrading to a token AND. That is now the first rung.

**After the fix:** 17 resolve via `filter_title_quoted`, 1 via a new head-quoted rung, 8 by
id, and **0 via `search=`** — the fallback is no longer carrying the run. Mean top-candidate
Jaccard 0.94.

**This is a shared-resolver defect, not a C.3.e one.** Every chapter that ran an anchor
resolution resolved on the fallback channel. Nothing is known to be *wrong* in those runs —
the fallback found real papers — but no earlier chapter's anchor recall was measured against
a working title channel, and a refusal reads as an absence. Flagged to **TICK-074**.

---

## 3. Two further resolver defects, both of which manufacture false absences

**`is_stem` was one-directional.** It tolerated a *dropped subtitle* (candidate is a prefix
of the returned title) but not an *added prefix*. Book chapters carry one: Schultz's Handbook
chapter is indexed as **"Chapter 8 Demand for children in low income countries"**, and the
one-directional test refused it. Containment is now checked in both directions, contiguous.
This is not the unbounded suffix-containment the shadow-record gate rejects — the author and
year gates still have to pass on top of a 4+ token contiguous match.

**A title spanning a colon does not match as one stemmed phrase.** Pitt 1999's full title
returned 0 on the quoted rung and 0 on the bare rung, and `search=` ranked a Campbell
systematic review about disability interventions at the top. The paper exists, in *Demography*,
with 151 citations. A rung that quotes only the pre-colon clause finds it immediately. This
literature's titles are long and colon-heavy, so the rung earns its place.

**And OpenAlex's own author metadata can be the error.** Pitt 1999 resolved at Jaccard 0.905
with the correct venue and year, but is flagged `MATCH_TITLE_AUTHOR_DISAGREES` because
**OpenAlex records the first author as "Mark M. Pin"**, not Pitt. Read by hand: the record is
correct and the index is wrong. The gate was not loosened — first-author agreement is still
required, and membership is still not accepted — but the verdict routes to a human read rather
than to a refusal, and the candidate now reports whether the wanted author appears anywhere in
the list as *evidence for that read*, never as an auto-pass.

Correction to the candidate list, from the resolver: the true title is "Are the reported causal
**relationships** the result of heterogeneity bias?", not "causal effects".

---

## 4. A version pair, and its headline sign flips

Two inherited records, two DOIs, one author (Xi Yang):

| | OpenAlex | DOI | Year | Title as C.2.c stored it | Title live, 2026-09-01 |
|---|---|---|---|---|---|
| v1 | W4381108710 | 10.2139/ssrn.4473936 | 2023 | More Credit, **Fewer** Babies? | More Credit, **More** Babies? |
| v2 | W7128532933 | 10.2139/ssrn.6213441 | 2026 | — | More Credit, **More** Babies? |

Same first author, same subtitle, so under the duplicate-record rule (which requires author
agreement) this is **one study in two versions, not two studies**, and it must not be counted
twice. Two consequences:

1. **The headline conclusion reversed between versions**, from fewer babies to more. Which
   version is the version of record decides the sign this study contributes. Settle it at
   full text before extraction; do not extract from the title.
2. **C.2.c's stored snapshot is stale** — it holds the old title, and the live record has been
   retitled underneath it. Any chapter reading titles out of another chapter's stored JSON is
   reading a frozen copy. The by-id rung now records `title_drift` for exactly this reason, and
   it fired on two of the eight inherited records.

---

## 5. The Arm S survival probe — PI Call 1 is answered, and Arm S survives

**Question.** C.3.c's written chapter claims "money in a bank, an insurance policy" among its
substitutes. If the asset-motive literature is overwhelmingly old-age framed, Wall 1 hands Arm S
to C.3.c and C.3.e collapses to a one-arm liquidity chapter with PM and FDT out of scope.

**First answer, and why it was not usable.** The within-life-risk block returned 2,431 records
of which 151 (6.2%) were old-age framed — an apparently decisive survival. But the per-term
counts show **"health insurance" alone contributes 2,195 of those 2,431 (90%)**, and
"health insurance AND fertility" is overwhelmingly about insurance *coverage of reproductive
services* — 208 of it explicitly IVF and ART, which is **A.17's estimand**, and most of the
rest maternity and prenatal coverage. A block dominated by an off-estimand homonym scores the
homonym, not the question. This is why every term is counted alone.

**Second answer, on the on-estimand vocabulary** (`children as insurance`, `insurance motive`,
`consumption smoothing`, `risk sharing`, `crop insurance`, `income risk`, `precautionary saving`,
each × the fertility block, `health insurance` dropped):

| | n |
|---|---|
| Arm S on-estimand frame | **262** |
| of which old-age framed | **36 (13.7%)** |

**Ruling: Arm S survives.** Some 86% of the on-estimand asset-motive frame is not old-age
framed, so C.3.c has not taken the arm whole and the Wall 1 split is doing real work rather
than dividing an empty set. The chapter proceeds with two arms.

**Three cautions this probe also bought.**

- **Arm S is small — 262 records before screening.** It is a real cell, not a large one. If the
  identified subset is thin, the honest verdict for PM and FDT is UNEVALUATED, not weak.
- **`health insurance` is banned from the Arm S retrieval vocabulary** unqualified. It is a
  9-to-1 contaminant and it collides with A.17.
- **The same single-term dominance appears on the other axes** and must be handled at query
  design: `interest rate` carries 435 of the borrowing block's 620 (70%), and
  `access to credit` + `credit access` carry 1,059 of the financial-access block's 1,344 (79%).
  Neither block has been recall-checked yet; the diagnostic vocabulary above is **not** the
  retrieval vocabulary, and the two are kept separate.

---

## 6. What is next

1. Snowball the 26 anchors, forward and backward, seeding the decoys as well — decoy clouds are
   boundary cases and on earlier chapters ran far more on-topic than the theory canon.
2. Build the production query per arm, leave-one-out on each axis, and score recall **per arm**
   against the anchor set. Arm S and Arm B do not share a vocabulary; a pooled recall number
   would hide a dead arm.
3. Carry the C.2.c `MIXED_PRICE_CREDIT` records in as unallocated from the start.
