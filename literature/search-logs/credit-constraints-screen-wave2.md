# Screen, wave 2: `frame_only` — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Output: `extraction/credit-constraints-screen.csv`

All 2,271 `frame_only` records read at title level, with abstracts read wherever a title was
ambiguous. Zero validation errors. **2,620 records now screened across the three strata.**

## The depth probe failed on this stratum, and the reason is instructive

| Stratum | n | Probe predicted | **Actual primary** |
|---|---|---|---|
| `both_channels` | 80 | ~23% | **25.0%** |
| `snowball_r2_only` | 269 | ~4% | **2.2%** |
| `frame_only` | 2,271 | ~6% | **1.6%** |

The probe held to within two points where the yield was high and **overestimated `frame_only` by
roughly four times**. Two causes, and only one of them is my sampling:

1. **A 40-record probe cannot measure a 1.6% base rate.** The expected count is 0.6 records; I read
   2–3 as relevant. That is noise, not an estimate, and no amount of care in reading fixes it.
2. **The probe counted "relevant" loosely** — theory, boundary and uncertain cases included — while
   the full screen applied the estimand cells strictly.

**The rule this yields:** a depth probe is a planning instrument for dense strata and a coin-flip for
sparse ones. Where the probe returns 0–2 hits in 40, treat the stratum as *unmeasured*, not as
low-yield, and either probe far deeper or screen it and find out. Doing the latter here cost one
session and changed the arm balance materially.

## The primary pool doubled and the arms rebalanced

| Cell | After wave 1 | **After wave 2** |
|---|---|---|
| `PRIMARY_COMPOSITE_ACCESS` | 19 | **32** |
| `PRIMARY_SAVE_INSURE` (Arm S) | 3 | **16** |
| `PRIMARY_BORROW_TERMS` (Arm B) | 4 | **14** |
| **Primary total** | 26 | **62** |

Arm S went from 3 records to 16. **The judgement in wave 1 that "Arm S is the thinnest arm and that is
a finding" was premature** — it was an artefact of which stratum had been screened, and the arm that
looked at risk of an UNEVALUATED verdict is now the second largest.

## Three things worth naming

**A third FDT-era Arm S record.** *Savings Behaviour, Fertility and Economic Development in Nineteenth
Century Britain* joins the US-counties financial-development study and the American-frontier
rainfall-risk paper. The historical cell that the scope memo expected to be empty now has three
members, and they span two countries and two distinct sources of variation (institutional access and
risk exposure).

**The Arm S exposure vocabulary is "risk", not "credit".** Four of the new Arm S records come from the
Cain debate — *Risk and Fertility: A Reply to Robinson*, *Public policy, risk and fertility in
Bangladesh*, the landholding exchange — and none carries a finance token in its title. This is why the
token filter had 24/26 recall and why it could not be used as a gate: the sub-literature that argues
the insurance motive most directly does not use the word credit.

**Two more version pairs, both inside the primary pool.** *Bequest Receipt and Family Size Effects*
alongside *Do Credit Constraints Explain Family Size Effects? Tests Based on Bequest Receipt*, and
*Do Mortgage Interest Subsidies Affect Fertility* appearing twice. Both are flagged in the table; the
chapter has now hit five version pairs, and de-duplication before extraction is not optional.

**And 37 records now route to C.3.c** — up from 15. One is flagged for the same revisit as the
antebellum paper: *Bismarck in the bedroom? Pension reform and fertility, 1870–2010* is FDT-era with a
long panel, and if C.3.c declines it, it belongs here.

## Bounds

- Title-level screening. Design and outcome values are hypotheses until full text.
- 2,486 records are recorded as `OFF_OTHER_read_not_routed` — an explicit residual. Much of it is
  development-economics noise that the query's `access to credit` and `family size` terms admit
  incidentally: smallholder credit access, loan repayment, food security, agricultural adoption.
- `snowball_r1_only` (3,815 records) is untouched, as is the no-abstract residue.

## Next

1. `snowball_r1_only` at ~1% predicted — but that prediction now carries the caveat above, so it needs
   a deeper probe (200+ records) before being deprioritised, not a 40-record one.
2. Retrieve and extract the 62-record primary pool; de-duplicate the five version pairs first.
3. Mine the three systematic reviews.
