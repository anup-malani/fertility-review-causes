# TICK-036: B.1 demographic-significance and target-period pass
**Status:** open
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-037
**Blocked by:** TICK-034, TICK-035
**Touches:** extraction/evolutionary-sex-drive-contraceptive-decoupling-target-period-relevance.csv, output/tables/evolutionary-sex-drive-contraceptive-decoupling-demographic-significance.csv

## Description

Classify each extracted study's window as pre-modern, FDT, or SDT by the replacement-status of fertility
in its country and period, reusing `source/analysis/oas_transition_classification.py` (TFR above vs
below 2.1). For B.1 the demographic-significance question is asymmetric: the status-and-reproduction
stream can be dated and classified, but the distinctive decoupling claim has no identified estimate to
place, so the pass should confirm the timing argument (pill postdates most of the FDT) rather than
attempt a decomposition share for the distinctive claim.

## Acceptance criteria
- [ ] Per-study transition classification from in-window TFR, with unclassifiable historical rows flagged.
- [ ] Demographic-significance table populated for the status-and-reproduction stream.
- [ ] The FDT timing argument (severing technology postdates most of the transition) documented from dates, not asserted.
- [ ] The distinctive-claim cell explicitly recorded as unidentified rather than assigned a share.

## Log
<!-- Append completion note here when done. -->
