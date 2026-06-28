# Output paper tiers — gold-anchored method (instantiated on existing data)

**Date:** 2026-06-28 · **Author:** Shravan (RA), with Claude Code
**Status:** DEMONSTRATION. The production keyword query has not run yet (its measuring
instrument, the gold set, is still being built). These counts instantiate the tier *logic*
on the **existing** screened corpus (PI keyword pull + sequential saturation + snowball);
the real numbers change when the tuned 2-block query runs. Data: `*-tiers.json`.
Script: `source/build/goldset/12_instantiate_tiers.py`.

## The 3 tiers (definition)

Per-paper signals: **G** = gold anchor; **K** = keyword channel; **S** = snowball channel;
**V** = two-stage screen verdict+confidence (Haiku→Sonnet, calibrated routing rule, 0.7% FN).

| Tier | Rule | Meaning / RA action |
|---|---|---|
| **1 — Core** | `G` OR (`V=RELEVANT-HIGH` & multi-channel `K&S`) | Near-certain. RA reads all; primary meta-analysis inputs. |
| **2 — Confirmed single-channel** | `V=RELEVANT`, not Tier 1 (single-channel, or RELEVANT-MED) | The union's unique contributions. RA title/abstract pass each. |
| **3 — Recall safety net** | `V=UNCERTAIN` OR (`V=NOT_RELEVANT` & conf=LOW) | RA **samples** to bound false negatives; tied to the gold-set recall estimate. |
| (excluded) | `V=NOT_RELEVANT` & conf HIGH/MED | PRISMA excluded. |

Within each tier, secondary sort = Anup `compositeScore` (evidence quality), then channel-count.

**Distinct basis from the other two methods (so it's the consensus, not a 4th scheme):**
Anup tiers by *evidence quality* (compositeScore); Alexandra by *lexical/triage relevance*.
This tiers by **convergence of independent inclusion signals + gold-anchoring**, and consumes
both of theirs as inputs (compositeScore = intra-tier sort; cluster/channel provenance = K/S).
**Final meta-analysis list = Tier 1 + (Tier 2 surviving RA + full-text screen).**

## Instantiated counts (existing corpus, universe = 8,087 screened, deduped by paperId)

Channels: keyword K = 6,401 · snowball S = 1,922 · multi-channel K∩S = 236 · gold anchors = 17 paperIds (14 distinct studies).

| Tier | n | composition |
|---|---:|---|
| **1 — Core** | **83** | 17 gold-anchor + 66 multi-channel RELEVANT-HIGH |
| **2 — Confirmed single** | **1,126** | 1,071 single-channel RELEVANT + 55 multi-channel RELEVANT-MED |
| **3 — Recall net** | **1,531** | 1,408 UNCERTAIN + 123 low-conf NOT_RELEVANT |
| excluded | 5,347 | NOT_RELEVANT (HIGH/MED) |

Total RELEVANT in universe = 1,208. **Strongest meta-analysis inputs** (Tier 1+2 with
compositeScore ≥ 7) = **69** — comparable to Anup's Tier-1 (74).

Tier-1 channel mix: K&S 72 / K 8 / S 3. Tier-2: K 807 / S 264 / K&S 55.

## What the instantiation demonstrates

**The orthogonal-channel design pays off, visibly.** The Tier-2 **single-channel-snowball**
bin contains canonical OAS papers the **keyword channel missed**: *Children as a Form of
Retirement Saving* (Chile), *Does Pension Privatization Increase Fertility?*, *Old-age support
and fertility in rural China*. These are exactly the keyword-disconnected papers the snowball
exists to catch — and the tiering surfaces them as confirmed-relevant rather than burying them.
(They're also our gold-residual hard cases — independent corroboration that they're real and
relevant.) An intersection-based scheme would have dropped them; the union + channel-count
tiering keeps and ranks them.

## Caveats

- **Demonstration only.** Universe = the existing PI corpus, not this method's production query.
  The real run uses the tuned 2-block gold-anchored query, so Tier 2/3 will be smaller and
  higher-precision. Tier counts here inherit any corruption/verdict noise in the existing data.
- **Channel mapping is approximate.** K = screened.json (PI keyword pull) ∪ sequential
  saturation; S = snowball.json. A cleaner run records channel provenance natively.
- Gold-anchor set is only the 14 verified studies so far (Part 1c canon will grow it).
