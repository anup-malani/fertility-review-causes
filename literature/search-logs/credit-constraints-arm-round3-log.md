# Arm S / Arm B seeded round, and a homonym that was half the frame — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Scripts `288` (staged, superseded), `289` (outcome-axis LOO),
`290` (hand-seeded round 3)

---

## 1. The production query was half homonym, and the outcome axis had never been calibrated

`278` calibrated all three exposure axes term by term and **accepted the outcome axis as a block.**
That gap cost half the frame.

`parity` is in the outcome axis for *birth parity*. `interest rate` is in Arm B's exposure axis. So the
single phrase **"interest rate parity" satisfies both axes at once**, and the first seeded round came
back as a reading list on uncovered interest parity, the forward discount puzzle and exchange-rate
models.

Measured:

| | Records |
|---|---|
| Arm B frame **with** `parity` | 4,291 |
| Arm B frame **without** `parity` | 1,073 |
| Whole frame with `parity` | 7,021 |
| **Whole frame without `parity`** | **3,512** |
| **Gold lost by dropping it** | **none — 10/23 either way** |

`parity` contributed **3,509 records, half the entire production frame, and zero gold.** Demographic
replacements — `birth parity`, `parity progression`, `parity-specific`, `higher-order birth` — return
0–1 records each: that sense simply is not carried in these abstracts. The term is dropped.

**The rule applied, which matters more than the term.** A term is dropped for a **demonstrated homonym
mechanism plus zero gold**, never for zero gold alone. `family size` (+912) and `births` (+796) also
lose no gold against a 23-record anchor set, and they stay: they are semantically on-estimand, and
dropping every term that misses the anchors would overfit the query to the anchors. Query frozen again
at **3,512**.

## 2. The first seeded round selected its own seeds, and that was the error

`288` picked seeds automatically: top-cited among records the abstract classifier scored as arm-matched
and identified. It returned *The legacy of Lionel McKenzie* and a Spanish-language paper on the Mexican
electricity sector.

The classifier is a **triage**. For the composite cell in `283` its output was hand-read before four
seeds were chosen; automating that step here just reproduced the triage's noise, and a snowball
amplifies whatever it is handed. Seeds for `290` are hand-read from `288`'s stage-1 lists and named in
the script, so the judgement is auditable and the round reproducible.

## 3. The round: the yield was the seeds, not their citation clouds

| | |
|---|---|
| Pool | 283 |
| New to rounds 1–2 | 261 |
| Redundancy | 7.8% |
| **New records carrying exposure × fertility outcome** | **1** |
| … and that one is *The Old-Age Security Motive for Fertility* — **C.3.c's under Wall 1** | |
| New records with no abstract | 79 (30%) |

**Two structural caveats on this null.**

- **The backward rung was dead: all six seeds have empty `referenced_works` in OpenAlex.** NBER working
  papers, repository items and book chapters frequently carry no reference list there. So this was a
  **forward-only** round, materially weaker than round 2's test, and the coverage claim below is
  correspondingly weaker.
- 30% of the new records have no abstract, so the scorer cannot see them.

**What the round did produce is the six hand-picked seeds themselves** — found by the term channel at
stage 1, not by any snowball:

| Arm | Study | Why |
|---|---|---|
| S | **AGEP Zambia cluster-RCT** (Austrian, Soler-Hampejsek, Behrman; *BMC Public Health*) | savings-account component, fertility among the outcomes |
| S | Delavallade et al., insurance-versus-savings experiment | saving-pure Arm S exposure, experimental |
| S | Billari and Galasso, Italian pension reforms | 103 cites; pension exposure → **C.3.c under Wall 1**, seeded as a decoy |
| B | **Dettling and Kearney 2025 (NBER), "Did the Modern Mortgage Set the Stage for the U.S. Baby Boom?"** | mortgage **credit**, not house prices — C.3.e's under Wall 2, and the same authors as C.2.c's decoy |
| B | Li, *Fertility and Housing Market: Australian Evidence* | |
| S | Davis-Friedmann, *Old Age Security and the One-child Campaign* | boundary, C.3.c |

These go into screening on their own account.

## 4. What this says about coverage — stated as weakly as the evidence supports

Round 2, seeded on composite, returned **15** new exposure × outcome records. Round 3, seeded on
Arms S and B, returned **1**, and it belongs to a neighbouring chapter.

The natural reading is that **the blind spot was composite-specific**: round 1's composite seeds were
chosen by design celebrity, while its Arm S and Arm B seeds (Cain, Pörtner, Pitt; Cumming, *Babies of
Mortgage Deregulation*, the PNAS provident-fund study) were estimand-matched from the start, so those
arms were already covered.

**That reading is plausible but not established here**, because the round was forward-only and blind to
30% of what it found. A backward pass on version twins with populated reference lists would test it
properly, and until then "the arms are adequately covered" is a working assumption, not a measurement.

## 5. Next

1. Screen the repaired 3,512-record frame — it is half the size it was this morning and the removed
   half was a homonym.
2. Screen the six hand-picked seeds and round 2's 15 as candidates.
3. Mine the Orton 2016 review's included-study list (23 studies) before contemplating a fourth round.
