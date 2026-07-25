# TICK-036: B.1 demographic-significance and target-period pass
**Status:** done
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
- [x] Per-study transition classification, with the unclassifiable historical row flagged.
- [x] Demographic-significance table populated for the status-and-reproduction stream.
- [x] The FDT timing argument documented from dates, not asserted.
- [x] The distinctive-claim cell explicitly recorded as unidentified rather than assigned a share.

## Log
**2026-07-25 complete.** `source/analysis/b1_demographic_significance.py` (+16 unit tests) reads
`extraction/{slug}-target-period-relevance.csv` and the meta-analysis summary, and emits
`output/tables/{slug}-{demographic-significance,grade-verdicts}.csv`.

Study windows were read out of the PDFs rather than recalled: Hopcroft 2015 NLSY79 1979-2010,
Kanazawa 2003 GSS waves 1988-1996, Fieder 2005 Vienna database dated 1 August 2001, Hopcroft 2018
SIPP 2014 panel. von Rueden and Jaeggi 2016 has no country-year window (46 studies, 33 nonindustrial
societies) and is assigned to the pre-modern cell by fertility REGIME, flagged `needs_human_review`
because that is an analyst judgement rather than a computation.

Four channels: PM_dissociation insufficient_direct_evidence (k=1); FDT_decoupling
not_significant_mechanism_mistimed; SDT_dissociation real_but_quantitatively_small_and_self_cancelling
(k=4); SDT_distinctive_decoupling unidentified_no_share_assigned (k=0).

The FDT timing argument is now derived rather than asserted, and in a narrower form than the chapter
previously used: zero of four dated pooled studies observe fertility inside the 1870-1965 window, and
the earliest observation window in the pool begins in 1979. That is a checkable property of the
evidence base rather than a claim about licensing dates, and it is pinned by a unit test.

**Deviation from the ticket as written:** the per-study classification is from study dates, NOT from
in-window TFR. `oas_transition_classification.py` needs `UN_TFR.csv` from the sibling
`proximate-causes` checkout, which is not on this machine. The script attempts the cross-check and
records `unavailable` with the missing path rather than skipping silently, so a reader can tell a
missing check from a passed one. Re-run when that checkout is present to add the TFR cross-check.
