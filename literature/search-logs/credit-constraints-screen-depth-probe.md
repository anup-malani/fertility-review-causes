# Screening universe, prescreen, and the depth probe — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Scripts `291` (universe), `292` (prescreen + probe) ·
Outputs: `credit-constraints-screen-universe.json`, `credit-constraints-prescreen.json`

---

## 1. The universe, and a defect it exposed

7,327 records after collapsing **397 version pairs**: the repaired 3,512-record frame plus the three
snowball pools plus the hand-sourced studies.

**The hand-sourced studies were missing, and that is the whole reason to check.** A snowball pool
contains what the seeds *reached* — never the seeds themselves. So before this was fixed the universe
did not contain the 2026 *PNAS* provident-fund study that **C.2.c explicitly routed to this chapter**,
Islam et al. 2026, Yang 2026, Cain 1983 or Guinnane 2001. Screen output is not the evidence base;
Tier-A anchors are studies, and they now enter as their own provenance channel (`hand_*`).

A second, quieter trap: three known records were reported absent **by id** while being present as their
**version twins** — the dedup had collapsed them into a keeper with a different id. The recall check now
matches on folded title, not id, and the universe is complete at **34/34 known-relevant**.

**The two discovery channels barely overlap: 91 records, about 2.5%.** That is not a detail — it means
the strata have very different priors and should not be screened in one undifferentiated queue.

## 2. Prescreen: three rules of four survived

Every rule was recall-checked before being allowed to fire, and a rule removing **any** known-relevant
record was rejected outright.

| Rule | Removes | Verdict |
|---|---|---|
| agronomy / soil-fertility homonym | 724 | **accept** |
| veterinary animal reproduction | 20 | **accept** |
| non-study record type | 77 | **accept** |
| no abstract **and** no outcome word in title | 1,335 | **REJECT — harms Prina and Delavallade** |

The rejected rule was the tempting one: it would have removed 1,335 records, 20% of the universe, and it
would have destroyed two known-relevant studies to do it. **7,327 → 6,535 survivors (10.8% removed),
known-relevant retention 34/34.**

## 3. The depth probe: 160 records read across four discovery strata

Rather than screening sequentially and learning the yield curve at the end, 40 records were sampled from
each stratum and read. Yield is my classification of title and abstract against the scope memo's estimand
cells — a **calibration, not the screen**.

| Stratum | Size | Probe yield | Implied relevant | Density vs. cheapest |
|---|---|---|---|---|
| **both_channels** | 80 | **~9 of 40 (23%)** | ~18 | **20×** |
| frame_only | 2,271 | ~2–3 of 40 (6%) | ~135 | 5× |
| snowball_r2_only | 269 | ~1–2 of 40 (4%) | ~10 | 3× |
| snowball_r1_only | 3,815 | **~0–1 of 40 (≈1%)** | ~40 | 1× |

**The screening plan follows the curve, not the record count.** `both_channels` is 1.2% of the survivors
and holds an estimated 10% of the relevant records. `snowball_r1_only` is 58% of the survivors and holds
an estimated 20% — it is the expensive stratum and it goes last, screened at lower depth with a bounded
tail sample rather than exhaustively.

## 4. What the probe already turned up

`both_channels` alone produced, in 40 records:

- **"Fertility and Financial Development: Evidence from U.S. Counties in the 19th Century" (NBER, 2014).**
  The scope memo named the historical FDT cell — savings and credit institutions against parish or county
  fertility — as *"the thinnest and most valuable cell if it exists."* **It exists.**
- **"The No-Birth Bonus Scheme: The Use of Savings Accounts for Family Planning in South India"**
  (*PDR*, 1980) — a savings instrument against fertility. Arm S, and unusually direct.
- **"Loans vs. Lives: Credit Obligations and Childbirth in Russia"** (*Population Research and Policy
  Review*, 2026) — Arm B.
- **"Credit constraints and the trade-off between family size and children's investment"** — Thai
  household panel, Arm B, and it crosses into C.3.d's quantity–quality territory.
- **"The Babies of Financial Deregulation"** (SSRN, 2016) — likely a version twin of *The Babies of
  Mortgage Market Deregulation*; check before counting it separately.
- **"Microfinance Programs and Contraceptive Use: Evidence from Indonesia"**, and a Ghana study on
  informal banking clubs and family-planning practice.

`snowball_r2_only` produced a second systematic review — *Impact of financial inclusion in low- and
middle-income countries* (*Journal of Economic Surveys*, 2020) — to be mined alongside Orton 2016.

A large share of `both_channels` is **C.3.c boundary material** — the old-age-security motive, social
pensions, the AEJ:EP social-pension extension study. Wall 1 routes those out, and the volume confirms
the wall is load-bearing rather than decorative.

## 5. Bounds

- 1,672 records (23%) have **no abstract**; the probe cannot see them, and they need a bounded blind
  sample with hidden controls rather than a guess.
- Yields are one rater's abstract-level read of 40 records per stratum. The confidence interval on 1 in
  40 is wide, and `snowball_r1_only`'s ~1% should be re-estimated at a second depth before that stratum
  is abandoned rather than merely deprioritised.

## 6. Next

1. Screen `both_channels` (80) and `snowball_r2_only` (269) in full — 349 records for an estimated 28 of
   the relevant set.
2. Screen `frame_only` (2,271) in batches, re-measuring yield each wave.
3. `snowball_r1_only`: second depth probe, then a bounded tail sample with hidden gold controls.
4. Mine both systematic reviews before any further snowball round.
