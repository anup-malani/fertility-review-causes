# A.18 title/abstract screen — interim report, stratum A complete

**TICK-076, 2026-08-31.** Batches 1–3 of 43 screened: **165 records**, the whole of stratum A
(the 317 survivors the citation channel also reached) plus the first of stratum B.

## Yield, and why the stratification was worth building

| stratum | screened | RELEVANT | yield |
|---|---|---|---|
| A — citation intersect | 165 | 88 | **53.3%** |
| C — boolean-only tail (§17 blinded sample) | 136 | 1 | **0.7%** |

A **76× difference**. The citation channel and the boolean channel disagree about where the evidence
is, and the citation channel is right. This is the quantitative case for `label-by-provenance-not-
vocabulary` on this hypothesis, and it is why §17 declined to screen the tail exhaustively.

## The screen audits itself against hidden gold

34 of the 165 records were gold, unmarked in the batches. The screen returned **31 RELEVANT, 1
UNCERTAIN, 2 NOT_RELEVANT — sensitivity 91.2%, or 94.1% counting UNCERTAIN.**

Both "misses" were read back, and at least one indicts the gold rather than the screen:

- *Partner + Children = Happiness?* — a within-MZ twin study whose **outcome is well-being and whose
  exposure is fertility**. Rejecting it is correct for A.18; it is in the gold set only because the
  proxy gold was built on a fertility word in the title. Same failure the §15 recall audit found at
  scale.
- *Relational Aggression and Lifetime Offspring* — predictor is a behavioural disposition, not a
  genetic measure. Wall 3. Defensible, and flagged for the RA gate rather than settled here.

## What the screen found, by cell

| cell | n | |
|---|---|---|
| `H2_FERTILITY` | 26 | conjunct 1 — well populated |
| `SELECTION_DIFFERENTIAL` | 22 | conjunct 2 |
| `H2_MODERATION` | 7 | **the arm the registered claim does not contain** |
| `PREDICTED_RESPONSE` | 4 | **the only cell that can carry a demsig number** |
| `PEDIGREE_RESPONSE` | 3 | the identified historical designs (Ruling 2) |
| `WITHIN_VS_POPULATION` | 1 | the bias-magnitude record |
| | **63** | primary-synthesis total |

Plus 23 `THEORY`/`METHOD` and 7 `LINK_TRAIT` (Wall 4), 41 routed to B.1 as `OFF_STATUS_B1`, 8
`OFF_SPECIES`, and 22 `UNCERTAIN`.

**Two things follow, and both were predicted by the scope but are now measured.**

*The moderation arm is real.* Seven records — Udry 1996, Kohler et al. 2002, Nisén, a
*Genotype × Cohort Interaction* study, a Norwegian *Influence of Societal Changes on the Contribution
of Genetics to Fertility Behavior*, and two demographic-transition-and-selection papers. §4 argued
this arm exists and runs the causal arrow backwards; it does, and it is not a footnote.

*The demsig-bearing cell is the thinnest.* Ruling 1 put demographic significance on the selection
**response**, and `PREDICTED_RESPONSE` has 4 records against `H2_FERTILITY`'s 26. The well-evidenced
half of the claim is the demographically inert half — exactly the asymmetry §3 predicted, now with
counts attached.

## The exposure-distance check (the A.24 lesson)

| `exposure_distance` | n |
|---|---|
| `ANONYMOUS_VARIANCE` (twin h², no variant named) | 43 |
| `NOT_GENETIC` (theory/method records) | 23 |
| `OTHER_CORRELATED_PGS` | 13 |
| **`FERTILITY_PGS`** | **9** |

**Nine records of 88 measure a genotype associated with fertility itself.** Thirteen measure selection
on a *correlated* trait — education, psychiatric liability, cognition. That is Ruling 3's entire
reason for existing, and it is now a table rather than an expectation: the conversion from a
correlated-trait selection differential to children per woman is doing more work in this literature
than any single study does.

`decomposes` among RELEVANT: **yes 80, cannot_tell 8, no 0** — Wall 1 is rejecting at the screen, as
designed.

## The yield curve across all three strata, measured

Batches 1–7 were screened in full (385 records) and the first 28 records of batches 14, 24, 34 and 43
were screened as a **positional probe** of stratum B at increasing depth in the relevance ordering.

| stratum / position | screened | relevant | yield |
|---|---|---|---|
| **A — citation intersect** | 317 | 168 | **53.0%** |
| B — head (first pure-B batch) | 55 | 5 | 9.1% |
| B — depth probes (batches 14/24/34/43) | 91 | 3 | 3.3% |
| C — boolean-only tail (§17 blinded sample) | 136 | 1 | 0.7% |

The depth probes are what the sequential order would have hidden. Batches 14 through 43 are almost
entirely non-human evolutionary biology, plant and livestock breeding, microbiology, and the
**cardiorespiratory-fitness homonym** that `fitness` bought us in §15 — the term that took anchor
recall from 64% to 84% is also the term that fills the tail with exercise physiology. That trade was
made knowingly and it is still the right trade, because recall is unrecoverable downstream and
precision is not; but this is what the precision cost looks like.

**Stratum B holds an estimated 80–100 relevant records** across its ~1,880 unscreened, and the probe
shows most are `METHOD`/`THEORY`/`LINK_TRAIT` rather than primary-cell. It is not empty — batch 24
contained *Genome-Wide Association Study of Parity in Bangladeshi Women*, a genuine `H2_FERTILITY`
record — so it cannot simply be discarded.

## Recommendation: snowball round 2 before screening the rest of stratum B

The citation channel out-yields the boolean channel **16-fold at the head and 53-fold in the tail**
(53.0% vs 3.3%). Stratum A's 168 relevant records include many that were never seeds. Snowballing
*those* is very likely to recover stratum B's relevant records at a small fraction of the cost of
reading 1,880 more abstracts — and it exploits the one thing this chapter has measured repeatedly,
which is that provenance beats vocabulary here.

Screening the remainder of stratum B stays available and is bounded, not abandoned.

## One metadata caution for extraction

`B34-10` (*Heritability of fecundity and post-partum sterility: an isolate-based study*) carries an
abstract in OpenAlex about **building climate-control system identification** — a wrong abstract
attached to a real record. A screen reading abstracts will mis-route such records in both directions,
and extraction must read the record itself, not the indexed abstract. Related to the standing rule
that a hand-retrieved PDF is matched to its record by content, not by filename.

---

# Snowball round 2 (2026-08-31)

Seeded from the **168 screen positives** rather than the 25 typed anchors, on the measured grounds
that the citation channel out-yields the boolean channel 16× at the head and 53× at depth. PROTOCOL
§5.1 caps depth at two rounds; there is no round 3.

| | |
|---|---|
| records reached | 11,641 |
| already known (pool ∪ frame, by id) | 3,349 |
| new by id | 8,292 |
| surviving the adopted prescreen | 4,659 |
| **after proper dedup (258)** | **4,399** |
| reached only from method/theory seeds — separate stratum | 1,875 |
| **substantive screening queue** | **2,524** |
| reached by ≥2 screen positives | 789 |
| API errors | 0 |

**Measured yield, round-2 priority batch: 67.3% RELEVANT, of which 32.7% substantive** (the rest is
method canon, largely already known). Against stratum B's 9.1% head and 3.3% depth, seeding from
screen positives rather than reading more abstracts was the right call by a wide margin.

## Two defects in my own round-2 script, both found by reading the output

**Script 256 deduped only on openalex id.** Batch 1 contained Williams 1957 twice and Charlesworth's
*Evolution in Age-Structured Populations* twice. 254 had already built title-cluster dedup with a
first-author gate **for the frame**, and 256 did not reuse it: a defect fixed once and not carried
forward. That is the same shape as the shared-resolver punctuation bug still sitting unmerged in
TICK-074.

**Version pairs were counted as new material.** A preprint carries a different openalex id from its
published version, so the bioRxiv twins of Beauchamp 2016, of the schizophrenia MR, and of the
*Education and Fertility Postponement* paper were all counted as new when they are the **same study,
already screened**. 133 such pairs. A version pair is one study.

Together these inflated the reported NEW by **260 records**. Corrected before any of it was reported
as a result.

## The seeding decision that was wrong, and is now measured

`THEORY`/`METHOD` seeds — the estimator canon added in §12 (Lande and Arnold, Kingsolver, Schluter,
Kruuk) — reached **2,234 records, the largest single share**. A 16-vs-16 read of what each seed class
reached:

- **method/theory-only reached:** Fisher 1941 on gene substitution, *The American Statistician*,
  *In the Name of Eugenics*, eco-evolutionary responses to climate change, *Foundations of Social
  Theory*. **~2 of 16 adjacent.**
- **thin-arm-only reached:** *Evolution, Fertility and the Ageing Population*, *Maternal Risk of
  Breeding Failure Remained Low throughout the Demographic Transition*, *From the First to the Second
  Demographic Transition*, *Sibling Correlation in Educational Attainment: A Test of Genetic Nurture*,
  *Early fertility decline in Austria-Hungary*. **~9 of 16.**

The lesson generalises past this chapter: **snowball from records whose ESTIMAND matches the
hypothesis, not from the estimator canon.** A methods paper is cited by every field that uses the
method, so forward-seeding it imports those fields wholesale. The estimator canon was right to add as
*anchors* — it supplied §10's threat 1 its formal statement — and wrong to use as *seeds*. Those 1,875
records go to their own stratum, deprioritised and bounded, not deleted.

## What round 2 bought the thin arms

| seed cell | new records reached |
|---|---|
| `H2_FERTILITY` | 1,204 |
| `SELECTION_DIFFERENTIAL` | 1,018 |
| `PEDIGREE_RESPONSE` | 259 |
| `H2_MODERATION` | 229 |
| `PREDICTED_RESPONSE` | 90 |
| `WITHIN_VS_POPULATION` | 4 |

404 records were reached **only** from thin-arm seeds, and batch 1 already promoted five new
`PEDIGREE_RESPONSE` records — including *Social transmission of reproductive behavior increases
frequency of inherited disorders* (Saguenay), *Human longevity and early reproduction in
pre-industrial Sami populations*, and *Human life histories and the demographic transition: Finland*.
These are the historical pedigree designs Ruling 2 widened the chapter to admit, and round 1 had three
of them.

