# Blinded depth probe on `snowball_r1_only` — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Script `295_c3e_blind_probe.py` ·
Outputs: `credit-constraints-r1-probe-{batch,key,result}.json`

Wave 2 established that a 40-record probe cannot resolve a ~2% base rate. This is the properly
powered version: **400 records sampled at random from the 3,815-record stratum, plus 20 records
already routed to a PRIMARY cell mixed in as hidden controls**, shuffled, with the key written to a
separate file.

## Result: the stratum is real but thin

| | |
|---|---|
| Sample | 400 |
| Primary found | **4 (1.00%)** |
| Plus uncertain, needing full text | 2 (1.50% upper) |
| Theory | 2 |
| **Projected primary in the 3,815-record stratum** | **38 – 57** |

The four: *Risk-sensitive fertility* (Arm S — the insurance motive directly); *Microfinance
participation and contraceptive use: does control over resources matter*; *Household and
Intrahousehold Impact of the Grameen Bank and Similar Targeted Credit Programs*; and *Does
intergenerational financial support increase fertility willingness* (China). The two uncertain are a
community-based microcredit programme in rural India and a **cluster-randomised** credit-with-health-education
trial in Benin — the second is worth the full-text check on its own, since a randomised credit arm is
what the composite cell is short of.

**This confirms the 1% estimate the 40-record probe gave, but that agreement is luck**: the earlier
probe's precision at this base rate was no better than a coin flip, as `frame_only` demonstrated when
the same method overestimated fourfold.

## The sensitivity arm failed, and the design flaw is mine

The 20 hidden controls were supposed to measure **my own miss rate** — if I fail to re-flag known
primary records mixed into a batch, the stratum's apparent emptiness is partly my sensitivity, not the
literature's. It did not work, for two reasons:

1. **I recorded verdicts only for new positives, not for every record in the batch.** Sensitivity
   cannot be scored from a positives-only record. The batch needed a verdict per row.
2. **Self-blinding is not possible here anyway.** I screened these same 20 records earlier in the same
   session; recognising them measures memory, not judgement.

So the probe reports **prevalence only**. A real sensitivity measure needs a second screener, or the
same screener after enough separation, and it needs a verdict on every row.

## And a data-integrity catch worth keeping

The screening sheets print a truncated id, and I reconstructed full OpenAlex ids by hand for the
verdict file. **All eight were wrong.** Five were recovered by title matching, three by a second pass;
none would have survived silently, because the ingest validates every verdict id against the batch and
rejects anything not on the sheet. Without that check, three verdicts — including the Benin RCT —
would have vanished, and four would have attached to the wrong records.

**Never hand-type a record id.** Copy it from the sheet, and keep the validation that refuses an id the
sheet does not contain.

## Recommendation: screen it, last

38–57 primary records for 3,815 title reads is the worst return in the chapter — `both_channels`
returned 20 in 80, `frame_only` 36 in 2,271. But it is not negligible against a primary pool that
currently stands at 62, and the four found here include one direct Arm S record and one randomised
composite trial, which are the two cells with the least evidence.

Screen it, but after the 62-record pool is retrieved and extracted: those 62 determine whether the
chapter can rate its arms at all, and 38 more marginal records will not change that answer.
