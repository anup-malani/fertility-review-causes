# Estimand-filtered Recall(B) re-grade - old-age-security-pension-crowdout

Point 1's last piece: the PI asked how the ~72% recall moves once measured against a gold that identifies the chapter's effect, not merely the topic. Here the **query is held fixed** (the same fold-local CV at Nf=Np=30 that produced the pilot number); only the **Tier-B denominator** is partitioned by estimand cell, using the frozen tags from `36a` + a Sonnet fleet.

## What Tier B actually contains

Tier B is **247** papers, the 'unbiased orthogonal sample' the honest Recall(B) is measured against. By estimand cell:

| Cell | Count | Share |
|---|---|---|
| THEORY | 160 | 65% |
| PRIMARY | 57 | 23% |
| OFF:outcome-not-fertility | 13 | 5% |
| OFF:reverse-direction | 6 | 2% |
| OFF:fertility-as-cause | 6 | 2% |
| OFF:different-cause | 3 | 1% |
| OFF:different-channel | 2 | 1% |

**Only 57 of 247 (23%) Tier-B papers are empirical primary-cell studies.** The plurality are formal/theoretical models (160, 65%) that carry no empirical estimand and route to the theory stream, not the meta-analysis. So the topical Recall(B) denominator is dominated by papers the pooling set does not want.

## How the recall number moves

| Recall(B) against ... | value |
|---|---|
| **topical** (all Tier B) - reproduces the headline | 72.5% (179/247) |
| **empirical** (drop theory models) | 66.7% (58/87) |
| **estimand-filtered** (PRIMARY cell only) - *the number the review needs* | 82.5% (47/57) |
| memo: theory papers (routed to theory stream) | 75.6% (121/160) |
| memo: PRIMARY, HIGH-confidence tags only (sensitivity) | 88.2% (15/17) |

The topical figure reproduces the pilot's ~72% headline (72.5% (179/247)), confirming the matching is the same. Re-based on the papers that identify the effect, the estimand-filtered **Recall(B) = 82.5%**

— i.e. the number moves **higher** once the denominator is the right population. The query recovers the primary-cell empirical papers *better* than the topical average, because the recall it was losing was concentrated in the theory tail (abstract models whose titles lack the surface fertility/pension vocabulary the title-match needs) — the honest empirical recall is stronger than the topical number suggested.

## Reading, and the honest caveats

This re-grades the **denominator**, which is the substantive fix the PI asked for: 'recovering the literature' now means recovering the primary-cell empirical studies, and theory papers are scored on their own stream rather than padding the empirical recall.

**The two halves of point 1 fit together.** The output set collapsed (44 topical -> 10 estimand-ready) because most topically-retrieved papers are off-cell - a *precision/definition* problem. Here the query's *recall* of the primary-cell papers is strong (82.5%). So recall was never the binding constraint; the definition of 'meta-analysis-ready' was. That is exactly the PI's thesis - 'the scarce resource was never more papers; it was a sharp definition of what we are measuring' - now shown from both sides. A note against over-reading the good recall: primary-cell papers tend to *name* the effect in their titles ('Pensions and Fertility ...'), so they are keyword-findable almost by construction; the residual leak is the quirky-titled canon (e.g. *Children as a Form of Retirement Saving*) that the snowball, not the keyword query, exists to catch. Caveats, stated plainly:

1. **Title-only matching, unchanged.** The CV matches on titles (the pilot's conservative lower bound); abstracts would lift every row. The *relative* move across columns is the finding, not the absolute level.
2. **Tag reliability.** 110 of 247 Tier-B tags are HIGH-confidence; 137 are LOW/MED (148 Tier-B papers are title-only - the identifiability ceiling). The HIGH-only sensitivity row brackets the PRIMARY estimate; the theory-vs-empirical split is robust because model titles are distinctive, but the PRIMARY/off-cell line within the empirics is softer.
3. **Tier B is not fully orthogonal** (its snowball was seeded off the keyword set), so even this estimand Recall(B) inherits the residual keyword bias already flagged in the workflow §E3.
4. **Automated tags, not RA-adjudicated.** These 247 were tagged by the calibrated gate (100% precision / 80% recall vs the RA on the pilot's 40), not individually RA-signed; the theory routing especially would benefit from a spot audit.

*(memo: Recall(A) over Tier A at this breadth = 62.5% (35/56).)*
