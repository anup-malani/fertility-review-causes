# D.3.c — D1 deterministic ranking and budget cutoff

**D1 is a budget control, not a judgement.** Its calibration target is **recall = 1.0 on the gold**, not precision: a D1 false negative is unrecoverable, so the cutoff is the largest budget saving that loses zero gold records. The curve below is printed so that choice is visible rather than asserted.

**Outcome vocabulary is not scored.** The production query is outcome-only, so every record in the pull already carries a fertility-outcome term in its title — it has near-zero discriminating power here. D1 scores the other axes, over title AND abstract, which is information the title-only query never saw.

## Features

| feature | weight | rationale |
|---|---|---|
| mechanism vocabulary | +3 | the chapter's own construct; rarest and most informative |
| treatment vocabulary | +2 | chronic decline / opportunity / uncertainty |
| timing-margin vocabulary | +1 | chapter 2's outcome margin; cheap to spot |
| has an abstract | +1 | a record with an abstract is cheaper for D2a to judge correctly |
| reverse causation, no mechanism | −2 | Wall 5; infertility-distress owns the instruments |
| mortality terms, no outcome | −3 | Wall 4; the largest decoy cloud |
| non-human | −3 | animal studies |

No weight was tuned against the gold — they are ordinal statements of what the walls say matters. Only the CUTOFF is calibrated. Tuning weights on the gold and then measuring recall on that same gold would make the recall figure meaningless.

## Recall versus budget

| threshold | kept | share of frame | gold kept | gold recall |
|---|---|---|---|---|
| -5 | 10,575 | 100.0% | 262/262 | 100.0% |
| -4 | 10,574 | 100.0% | 262/262 | 100.0% |
| -3 | 10,574 | 100.0% | 262/262 | 100.0% |
| -2 | 10,319 | 97.6% | 262/262 | 100.0% |
| -1 | 9,729 | 92.0% | 262/262 | 100.0% **<- chosen** |
| 0 | 9,592 | 90.7% | 260/262 | 99.2% |
| 1 | 6,888 | 65.1% | 214/262 | 81.7% |
| 2 | 4,084 | 38.6% | 119/262 | 45.4% |
| 3 | 3,092 | 29.2% | 63/262 | 24.0% |
| 4 | 749 | 7.1% | 30/262 | 11.5% |
| 5 | 212 | 2.0% | 1/262 | 0.4% |
| 6 | 166 | 1.6% | 0/262 | 0.0% |
| 7 | 16 | 0.2% | 0/262 | 0.0% |

**Chosen threshold: -1** — keeps 9,729 of 10,575 frame records (92.0%) at **100% gold recall** (262/262).

## The orthogonal-channel bypass

**Every record reached through the citation frame bypasses this cutoff and goes straight to D2a, whatever its term score.** The cutoff applies within the keyword channel only. Without the bypass the dumb term-match discards exactly the orthogonal-recall records the architecture exists to catch, and Recall(B) stops measuring anything. On this chapter the bypass set is the whole 10,589-record Tier B frame — a rounding error against a 390,983 pull, and the cheapest insurance in the pipeline.

## Projection to the production pull

At the chosen threshold, **92.0% of the frame survives**, which projects to roughly **359,704 records** of the 390,983-record pull reaching D2a.

**The projection is conservative, and states why.** The gold and the score distribution both come from the Tier B citation frame, which is a citation neighbourhood and therefore ENRICHED relative to an open-database pull: a larger share of it carries mechanism and treatment vocabulary than the pull will. The frame's survivor fraction is thus an **upper bound** on the pull's, and the error runs toward over-estimating cost rather than under-estimating recall. **Re-run this script against the real pull before committing budget** — that is a measurement C1 makes available and this one only approximates.

