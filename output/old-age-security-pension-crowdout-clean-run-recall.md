# Clean end-to-end run — recall on the frozen gold · old-age-security-pension-crowdout

The canonical workflow's §7 move-2 number chain, on the **frozen** gold (Tier A 56, Tier B 257, frozen 2026-07-08), replacing the dry-run/fixed-N/legacy stand-ins. CV selects breadth on the recall/budget frontier; the production query is refit on the full frozen gold at that breadth; estimand-filtered Recall(B) is graded against the **pre-registered** bar (`old-age-security-pension-crowdout-recall-preregistration.md`, committed before this ran).

## Selected breadth (recall/budget frontier)

- **Nf = 15, Np = 30**  ·  CV held-out recall 68.4%  ·  budget proxy 56 negatives matched

## Recall on the frozen gold

| Recall(B) against ... | value | pre-reg bar | verdict |
|---|---|---|---|
| **estimand-filtered (PRIMARY cell)** — the adoption metric | 82.5% (47/57) | ≥ 80% | **PASS** |
| topical (all Tier B) | 70.0% (180/257) | ≥ 72% | BELOW |
| empirical (drop theory) | 65.9% (58/88) | — | — |
| memo: theory (routed to theory stream) | 72.2% (122/169) | — | — |
| memo: PRIMARY, HIGH-confidence only (sensitivity) | 88.2% (15/17) | — | — |
| memo: Recall(A) over frozen Tier A | 60.7% (34/56) | — | — |

## Tier-B composition (frozen, by estimand cell)

| Cell | Count | Share |
|---|---|---|
| THEORY | 169 | 66% |
| PRIMARY | 57 | 22% |
| OFF:outcome-not-fertility | 13 | 5% |
| OFF:reverse-direction | 6 | 2% |
| OFF:fertility-as-cause | 6 | 2% |
| OFF:different-cause | 3 | 1% |
| OFF:different-channel | 2 | 1% |
| OFF | 1 | 0% |

## Verdict

Estimand-filtered Recall(B) = **82.5%** vs the pre-registered **80%** bar → **PASS**. The frozen refit reproduces the audited ~82% (envelope 81.8–83.0%); GACS clears its own recall adoption bar. Search remains one leg — the estimand gate, not recall, is the binding precision constraint (the §7.1 head-to-head finding stands).

**On the topical secondary bar (70.0% vs 72%).** This is freeze arithmetic, not a query regression. The identical query at the pilot breadth (Nf=Np=30) gives the *same* 70.0% on the frozen gold; the 72% bar was set against the 247-paper *pre-freeze* denominator. Freezing added 10 RA-adjudicated promotions to Tier B (247→257), all THEORY/OFF and mostly title-unmatched, so the topical denominator grew and topical recall dropped ~2pp by construction. The estimand metric is denominator-neutral (PRIMARY stayed 57), which is why it reproduces 82.5% exactly. So the query recovers the same papers; only the topical denominator moved.

**Frontier finding.** Nf=15 and Nf=30 (at Np=30) tie on both CV recall and budget — fertility-block breadth beyond 15 recovers no additional gold, so the frontier rule correctly selects the cheaper Nf=15. Pension-block breadth Np=30 does the work (Np<30 costs recall).

**Still deferred (live OpenAlex, budget-gated — Part-4-full):** the real universe-size denominator via `openalex_universe()` and the fresh production-corpus pull. Separable from this frozen-gold recall result by design; a daily-cap hit cannot invalidate the number above.

*Title-only matching throughout (conservative lower bound); abstracts would lift every row.*
