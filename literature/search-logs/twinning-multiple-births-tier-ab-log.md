# A4 Tier A / Tier B citation frame — twinning-multiple-births (A.12)

**Tier A: 25 seeding anchors.** The causal recall denominator is reported TWO ways, and the gap between them is the measured cost of Wall 8:

- **9 empirical anchors** — `PRIMARY_OFFSET_STOPPING` + `PRIMARY_OFFSET_FIRSTSTAGE`. Both cells estimate this chapter's estimand, so both belong in a causal denominator.
- **3 screenable anchors** — `PRIMARY_OFFSET_STOPPING` alone. Wall 8 declares the twin-IV first stages unreachable by title/abstract screening, because no abstract about schooling and earnings reveals its first-stage table. Recall(A) computed against the 9-anchor denominator will therefore look poor by construction; computed against the 3-anchor denominator it measures the screen. **Report both. The difference is not a screen failure, it is the price of an unenforceable wall, and it should appear as a number rather than as a sentence in the scope document.**

**Tier B frame: 8,701 deduplicated records** — 1,029 found by more than one seed, 5,515 carrying an abstract (63%).

**Records depending ONLY on a routing-decoy seed: 3,500** (40%), of which **2,073 depend only on a HOMONYM seed** and are the crystallography and metallurgy material the scope predicted. `seed_ids` provenance lets Recall(B) be recomputed without either group.

**Failed requests: 0** — listed at the foot. A failed request is not an empty result, and the frame is smaller than the index by exactly what those failures cost.

## Per-seed yield

Every fraction is a SEED-SELECTION DIAGNOSTIC computed after retrieval. None is applied as a filter: filtering the forward fetch by topic vocabulary would prune Tier B by distance from the production query and make Recall(B) circular.

`fert` = carries a fertility quantity. `twin` = carries a twinning/multiple-birth construct. **`BOTH`** = the density of A.12's primary cell in that neighbourhood — and for an accounting identity this reads high relative to the estimable literature, because any vital-statistics report tabulates twin births beside a birth rate without estimating anything. `hom` and `nonh` measure Walls 1-3. **`clin`** measures Walls 5-6: the share whose outcome is per-cycle or perinatal rather than a population birth count. All are LOWER BOUNDS — a paper counts only when it names the thing in its title or abstract.

| seed | cell | back | fwd | fwd total | trunc | fert | twin | **BOTH** | n | hom | nonh | **clin** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Perinatal outcome of singletons and twins after assi | `OFF_PERINATAL` | 41 | 1097 | 1097 | no | 35.9% | 28.4% | **14.2%** | 156 | 0.1% | 0.3% | **53.8%** |
| The More the Merrier? The Effect of Family Size and  | `PRIMARY_OFFSET_FIRSTSTAGE` | 30 | 1051 | 1051 | no | 32.1% | 6.0% | **3.7%** | 39 | 0.0% | 0.0% | **2.2%** |
| A short history of SHELX | `OFF_HOMONYM_CRYSTAL` | 52 | 1000 | 87673 | **yes** | 0.0% | 2.7% | **0.0%** | 0 | 42.5% | 1.3% | **0.0%** |
| High strength Fe-Mn-(Al, Si) TRIP/TWIP steels develo | `OFF_HOMONYM_ENGINEERING` | 21 | 1000 | 1810 | **yes** | 0.0% | 29.9% | **0.0%** | 0 | 76.4% | 0.0% | **0.0%** |
| Testing the Quantity-Quality Fertility Model: The Us | `PRIMARY_OFFSET_FIRSTSTAGE` | 7 | 717 | 717 | no | 58.4% | 13.7% | **10.9%** | 78 | 0.0% | 0.0% | **1.1%** |
| Elective Single-Embryo Transfer versus Double-Embryo | `SECONDARY_ART_MULTIPLES` | 28 | 596 | 596 | no | 32.0% | 38.8% | **20.6%** | 123 | 0.3% | 0.2% | **60.6%** |
| The Biology of Twinning in Man | `EXPOSURE_SERIES` | 0 | 563 | 563 | no | 29.0% | 70.3% | **25.4%** | 143 | 0.0% | 1.6% | **13.5%** |
| Multiple Experiments for the Causal Link between the | `PRIMARY_OFFSET_FIRSTSTAGE` | 40 | 536 | 536 | no | 46.1% | 10.1% | **8.0%** | 43 | 0.2% | 0.0% | **0.4%** |
| Clinical effectiveness of elective single versus dou | `SECONDARY_ART_MULTIPLES` | 59 | 395 | 395 | no | 33.9% | 28.4% | **15.2%** | 60 | 0.3% | 0.3% | **52.9%** |
| The Economic Consequences of Unwed Motherhood: Using | `PRIMARY_OFFSET_FIRSTSTAGE` | 17 | 370 | 370 | no | 50.8% | 15.1% | **12.4%** | 46 | 0.0% | 0.0% | **0.5%** |
| Three decades of twin births in the United States, 1 | `EXPOSURE_SERIES` | 10 | 329 | 329 | no | 22.2% | 66.9% | **19.1%** | 63 | 0.3% | 0.3% | **44.1%** |
| Trends in Multiple Births Conceived Using Assisted R | `SECONDARY_ART_MULTIPLES` | 12 | 307 | 307 | no | 47.9% | 56.7% | **32.9%** | 101 | 0.0% | 0.0% | **50.8%** |
| Twinning across the Developing World | `SECONDARY_PM_VARIATION` | 40 | 294 | 294 | no | 32.0% | 81.6% | **28.9%** | 85 | 0.0% | 1.4% | **47.6%** |
| An Observational Analysis of Twin Births, Calf Sex R | `OFF_NONHUMAN` | 32 | 221 | 221 | no | 34.8% | 36.2% | **20.4%** | 45 | 0.0% | 90.0% | **30.3%** |
| Twin Peaks: more twinning in humans than ever before | `SECONDARY_ART_MULTIPLES` | 45 | 212 | 212 | no | 30.2% | 79.7% | **23.1%** | 49 | 0.5% | 0.0% | **45.3%** |
| Dizygotic twinning | `EXPOSURE_SERIES` | 128 | 197 | 197 | no | 46.2% | 78.7% | **41.1%** | 81 | 0.0% | 3.0% | **17.3%** |
| Hidden heritability due to heterogeneity across seve | `OFF_TWINDESIGN` | 51 | 182 | 182 | no | 8.8% | 7.1% | **1.1%** | 2 | 0.0% | 3.3% | **1.6%** |
| Twinning Rates in Developed Countries: Trends and Ex | `SECONDARY_ART_MULTIPLES` | 51 | 129 | 129 | no | 39.5% | 75.2% | **30.2%** | 39 | 0.8% | 1.6% | **28.7%** |
| Frequency of Twin Births in Developed Countries | `EXPOSURE_SERIES` | 17 | 88 | 88 | no | 46.6% | 84.1% | **43.2%** | 38 | 0.0% | 2.3% | **25.0%** |
| Increasing the credibility of the twin birth instrum | `PRIMARY_OFFSET_FIRSTSTAGE` | 48 | 27 | 27 | no | 33.3% | 55.6% | **29.6%** | 8 | 0.0% | 0.0% | **3.7%** |
| Twins Support the Absence of Parity-Dependent Fertil | `PRIMARY_OFFSET_STOPPING` | 53 | 13 | 13 | no | 84.6% | 23.1% | **15.4%** | 2 | 0.0% | 0.0% | **0.0%** |
| Parity progression ratios confirm higher lifetime fe | `PRIMARY_OFFSET_STOPPING` | 4 | 12 | 12 | no | 83.3% | 33.3% | **25.0%** | 3 | 0.0% | 0.0% | **8.3%** |
| Do Population Control Policies Induce More Human Cap | `PRIMARY_OFFSET_FIRSTSTAGE` | 18 | 11 | 11 | no | 63.6% | 18.2% | **18.2%** | 2 | 0.0% | 0.0% | **9.1%** |
| The Human Multiple Births Database (HMBD) | `EXPOSURE_SERIES` | 21 | 9 | 9 | no | 22.2% | 66.7% | **22.2%** | 2 | 0.0% | 0.0% | **44.4%** |
| The Impact of Multiple Births on Fertility: Stopping | `PRIMARY_OFFSET_STOPPING` | 5 | 6 | 6 | no | 50.0% | 0.0% | **0.0%** | 0 | 0.0% | 0.0% | **16.7%** |

## Primary-cell density of the whole frame

Across every seed's forward cloud, **1,208 of 9,362 records (12.90%) carry a fertility quantity and a twinning construct together.** Read it as which seeds can reach the cell at all, not as a count of studies: for an identity the co-occurrence is cheap, and the scope already establishes that the cell's population is vital-statistics reports rather than estimation studies.

## Homonym seeds — exact on-topic rate, not a sampled one

The scope froze crystallographic twinning and TWIP steel as PURE HOMONYMS rather than boundary cases, which is this chapter's one carve-out from the standing rule that a decoy cloud is a boundary case worth forward-seeding in full. A carve-out asserted is worth nothing, and a carve-out measured on a capped sample is worth little more — a truncated OpenAlex pull is a head, not a random sample. So each homonym seed also carries an EXACT rate from two count-only queries. The 1,000-record cap governs only what enters Tier B; the rate below is computed over the entire cloud.

| seed | on-topic (exact) | total citing | exact rate | sampled rate (capped pull) |
|---|---|---|---|---|
| A short history of SHELX | 13 | 87673 | **0.0%** | 0.0% |
| High strength Fe-Mn-(Al, Si) TRIP/TWIP steels develo | 0 | 1810 | **0.0%** | 0.0% |

A near-zero exact rate confirms the carve-out. A materially non-zero one would REFUTE it, and the correct response would be to restore the homonym seeds to a full uncapped pull and re-run — the cap is a budget decision that the measurement is entitled to overturn.

## DOI-less seed recovery — generalised beyond monographs

A DOI-less anchor cannot seed, so each got ONE recovery attempt gated by first-author agreement. **The inherited code attempted this only for monographs**, which on this chapter would have silently dropped Bronars & Grogger 1994 — a twin-IV canon seed — and with it the only channel to `PRIMARY_OFFSET_FIRSTSTAGE`, since Wall 8 says those first stages cannot be reached by screening at all. The type restriction is inverted rather than dropped: a book must resolve to a bookish record and a non-book must not, so a monograph still cannot be seeded from a journal review of itself.

| anchor | book? | recovered | record | cites |
|---|---|---|---|---|
| The Economic Consequences of Unwed Motherhood: Using Twi | no | **yes** | `W1964550926` The economic consequences of unwed motherhoo | 368 |
| Three decades of twin births in the United States, 1980- | no | **yes** | `W2409722585` Three decades of twin births in the United S | 329 |
| The Biology of Twinning in Man | yes | **yes** | `W1591194821` The biology of twinning in man | 563 |

The first-author gate itself needed a fix to survive this chapter, recorded because the failure mode is silent. `_surname()` took the LAST token of a name, assuming Given-then-Surname order. OpenAlex renders Bronars & Grogger's first author as **"Bronars Sg"** — surname first, initials last — so the last token is `sg`, which matches no candidate surname, and the gate returned a CONFIDENT wrong negative. It now tests the full token set, which still refuses a reviewer (a different person shares no token with our authors' surnames) while accepting degraded metadata. A self-test holds both directions and the script refuses to run if either regresses.

## Truncation

2 seed(s) were truncated and are reported here rather than silently capped — a bounded pull that is not stated reads as complete coverage:
- **A short history of SHELX** (`OFF_HOMONYM_CRYSTAL`, 1,000 homonym cap): pulled 1,000 of 87,673 citing works, on-topic 0.0% — **86,673 unpulled, an estimated 0 on-topic records not seen.**
- **High strength Fe-Mn-(Al, Si) TRIP/TWIP steels develo** (`OFF_HOMONYM_ENGINEERING`, 1,000 homonym cap): pulled 1,000 of 1,810 citing works, on-topic 0.0% — **810 unpulled, an estimated 0 on-topic records not seen.**

**Estimated on-topic records lost to caps in total: ~0**, against a frame of 8,701. The estimate assumes the unpulled tail resembles the pulled head, which a cursor-paged truncation cannot guarantee — which is exactly why the homonym seeds carry an exact count above rather than relying on this estimate.
