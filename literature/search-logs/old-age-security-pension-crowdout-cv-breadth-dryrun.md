# Part 4 CV — breadth-vector dry run · 2026-06-29

**SCAFFOLD / DRY RUN on un-frozen gold.** 10-fold CV, title-only matching (conservative lower bound), backbone fixed + fold-local gold-mined expansion. Real universe size pending OpenAlex wiring + gold freeze.

- gold = 303 (A+B core); negatives = 4,537 (budget proxy)
- **backbone-only recall (Nf=Np=0): 56.4%**  [Recall(A) 51.8% / Recall(B) 57.5% → bias correction -5.7%]  (miss fert-block 68, pens-block 30, both 34)
- **best grid point: Nf=30, Np=30 → CV recall 70.6%**  [Recall(A) 62.5% / Recall(B) 72.5% → **bias correction -10.0%**]

> Recall(A)−Recall(B) is the vocabulary-bias correction — the headline scientific output. Tier A is keyword-sourced (optimistic); Tier B is the unbiased orthogonal sample.

## Dry-run findings (challenge spec assumptions — confirm in Part-4-full)

1. **SIGN FLIP: Recall(A) < Recall(B)** (correction -10% at peak), not the positive value the method assumed. Driver: Tier A now carries the Part-1c theory canon (e.g. Ehrlich–Lui, Boldrin–Jones) whose titles lack surface fertility/pension vocabulary; Tier B (def-1, unbiased — NOT adversarial) is keyword-richer. Reading: the query is not inflated toward keyword-sourced papers; it slightly UNDER-recalls the abstract theory canon.
2. **The FERTILITY block binds, not pension** (held-out misses ~50 fert vs ~25 pens) — opposite of §3's 'pension is the thin block'. Much relevant work says children/sons/value-of-children/family-size, not fertility/birth. → spend fertility-block breadth.
3. **Title-only ceiling ≈ 70%**, saturating near N≈20–30. Abstract matching (Part-4-full) should lift this; it's a conservative lower bound.
4. **Metric decision (Shravan 2026-06-29):** under def-1, **Recall(B) is the PRIMARY** honest estimate; **Recall(A)−Recall(B) is a DIAGNOSTIC** ('is the query inflated toward keyword-sourced papers?' — here: no). The worst-case vocabulary ceiling is reported NOT as a separate def-3 tier but as **Recall(B | title fails the 2-block query), measured via ABSTRACT match** — a hard-tail conditional, reported as a BOUND (n~38, powered for gross gaps not fine tuning; needs abstract matching, so deferred to Part-4-full). Also report empirical-vs-theory recall (where the canon tail lives). Caveat: this bound is itself optimistic (Tier B snowball-seeded off the keyword set).

## Recall surface (CV held-out recall by breadth vector)

| Nf \ Np | 0 | 3 | 6 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|
| **0** | 56% | 57% | 58% | 59% | 60% | 60% | 61% |
| **3** | 59% | 61% | 62% | 63% | 64% | 64% | 65% |
| **6** | 62% | 64% | 65% | 66% | 67% | 67% | 68% |
| **10** | 63% | 64% | 66% | 66% | 67% | 67% | 69% |
| **15** | 64% | 66% | 67% | 68% | 69% | 69% | 70% |
| **20** | 64% | 66% | 67% | 68% | 69% | 69% | 70% |
| **30** | 65% | 66% | 68% | 68% | 69% | 69% | 71% |

## Recall / budget frontier (top-8 recall points; neg_matched = on-disk budget proxy)

| Nf | Np | recall | Rec(A) | Rec(B) | A−B | miss-fert | miss-pens | miss-both | neg-matched |
|---|---|---|---|---|---|---|---|---|---|
| 30 | 30 | 70.6% | 62% | 72% | -10% | 50 | 25 | 14 | 57 |
| 15 | 30 | 70.3% | 62% | 72% | -10% | 51 | 25 | 14 | 56 |
| 20 | 30 | 70.3% | 62% | 72% | -10% | 51 | 25 | 14 | 56 |
| 30 | 15 | 69.0% | 59% | 71% | -12% | 49 | 30 | 15 | 53 |
| 30 | 20 | 69.0% | 59% | 71% | -12% | 49 | 30 | 15 | 57 |
| 10 | 30 | 68.7% | 62% | 70% | -8% | 56 | 25 | 14 | 56 |
| 15 | 15 | 68.7% | 59% | 71% | -12% | 50 | 30 | 15 | 52 |
| 15 | 20 | 68.7% | 59% | 71% | -12% | 50 | 30 | 15 | 56 |

## Reading the diagnostics

- If held-out misses concentrate on ONE block, move breadth budget there (that's the §6 allocation signal). - The pension/OAS block is the thin one (§3a), so expect it to bind.
- Production query (Part-4-full) = refit on FULL gold at the chosen (Nf,Np); quote the CV recall here as the honest out-of-sample estimate. Real budget = OpenAlex universe count.
