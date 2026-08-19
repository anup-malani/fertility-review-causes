# D.3.c — D1 re-calibrated on the real pull

`154_` calibrated D1 on the Tier B citation frame because C1 had not run, and said in its own output that the frame is enriched, that its survivor share was therefore an upper bound, and that the calibration had to be redone against real retrieval before budget was committed. This is that redo, over the **149,200** records C1 actually returned.

**Recall is measured against the gold present in the pull**, not against the full gold set — 209 distinct gold works of 243 were retrieved. Charging D1 for records C1 never returned would credit it with losses it did not cause and hide the ones it did.

**Distinct works, not matching records.** The index holds several records per work (preprint and published version, editions, reissues), so one gold work can match two or three pull records. A first version of this script counted records and reported 239 gold in the pull against a set of 243 — which made the retrieval filter look nearly free. It is not: the distinct count is 205, and the filter's cost stands at roughly the 16% reported when it was chosen.

| | frame (154_) | **real pull (this run)** |
|---|---|---|
| corpus | 10,575 | **149,200** |
| gold present | 262 | **209** |
| chosen threshold | -1 | **-1** |
| survivors | 9,729 (92.0%) | **139,866 (93.7%)** |
| gold recall | 100% | **100%** |

## Recall versus budget, on real retrieval

| threshold | kept | share | gold kept | recall |
|---|---|---|---|---|
| -5 | 149,200 | 100.0% | 209/209 | 100.0% |
| -4 | 149,152 | 100.0% | 209/209 | 100.0% |
| -3 | 147,991 | 99.2% | 209/209 | 100.0% |
| -2 | 146,651 | 98.3% | 209/209 | 100.0% |
| -1 | 139,866 | 93.7% | 209/209 | 100.0% **<- chosen** |
| 0 | 132,758 | 89.0% | 207/209 | 99.0% |
| 1 | 95,990 | 64.3% | 175/209 | 83.7% |
| 2 | 24,458 | 16.4% | 95/209 | 45.5% |
| 3 | 10,588 | 7.1% | 55/209 | 26.3% |
| 4 | 5,417 | 3.6% | 28/209 | 13.4% |
| 5 | 1,079 | 0.7% | 3/209 | 1.4% |
| 6 | 385 | 0.3% | 0/209 | 0.0% |
| 7 | 126 | 0.1% | 0/209 | 0.0% |

## What it costs

Mean title+abstract length on the real pull is **852 characters** (the frame's was 724), so the per-record cost transfers with a small adjustment.

| | records to D2a | screen cost |
|---|---|---|
| no D1 filter | 149,200 | $37 |
| **D1 at threshold -1** | **139,866** | **$35** |
| D1 saves | 9,334 records | **$2** |

Token counts remain **estimated from measured characters** — this environment still has no Anthropic credential, so `count_tokens()` has not been run. The character counts are now real retrieval rather than a citation-frame proxy, which removes one of the two approximations but not the other.

## Screen input written

`temp/d3c-screen/stage1-input.jsonl` — **139,866 records**, the D1 survivors at threshold -1. This is what `156_d3c_screen.py stage1` consumes.

