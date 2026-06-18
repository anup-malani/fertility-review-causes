# Decision: Two-tier hypothesis organization — Proximate Causes + Root Causes

**Date:** 2026-06-14
**Author:** Anup Malani (PI)
**Status:** Active — governs HYPOTHESES.md structure and all downstream chapter organization
**Review date:** 2026-12-14

## Context

The initial `enumerate-hypotheses.mjs` workflow organized 65 hypotheses into four symmetric categories: Demographic, Economic, Biological, Cultural. During PI review of the draft HYPOTHESES.md (TICK-001), it became clear that "Demographic" plays a different logical role than the other three: the demography literature describes *mechanisms* (how fertility changes) rather than *root causes* (why people want more or fewer children). Treating them as four parallel categories obscures this distinction.

Examples:
- Child mortality decline — a mechanism by which desired-family-size dynamics play out, with an insurance/replacement motive rooted in economic reasoning.
- Diffusion of fertility control — a mechanism of social spread; the underlying question of *why* people adopt new norms is Cultural.
- Age at marriage — a proximate behavioral lever that can be driven by economic, cultural, or biological forces simultaneously.

## Decision

Replace the four-category flat structure with a two-tier structure:

1. **Proximate Causes** — mechanisms and behavioral pathways through which fertility changes. Not further subdivided. Each entry carries a `cross-ref` field naming which root-cause category (or categories) supplies the deeper explanation.
2. **Root Causes** — three categories of underlying drivers:
   - **Economic** — price, income, opportunity-cost, and incentive-based explanations
   - **Biological** — physiological, evolutionary, and health-based explanations
   - **Cultural** — norm, preference, ideational, and cultural-evolution explanations

The former "Demographic" category is renamed "Proximate Causes." The Economic, Biological, and Cultural categories are unchanged in content; their framing is now explicitly "root causes."

## Rationale

- Readers can ask two distinct questions: "by what mechanism did fertility fall?" (proximate) and "what ultimately drove people to want fewer children?" (root cause). The two-tier structure maps cleanly onto those questions.
- The `cross-ref` field on proximate entries makes the linkage explicit without forcing an artificial single-category assignment for mechanisms that are genuinely multi-causal.
- Avoids the alternative of sub-dividing Proximate by root-cause type, which would either force arbitrary classification decisions or produce redundant entries.

## Consequences

- HYPOTHESES.md: `## Demographic` → `## Proximate Causes`; preamble updated to explain the two tiers.
- Chapter template: the per-phenomenon GRADE rating and demographic-significance verdict are unchanged; only the organizing category label changes for entries that were in the Demographic section.
- handoff.md: update description to reflect the new category count (1 proximate + 3 root-cause = 4 top-level sections, but conceptually two tiers).
- The slug and all other metadata for existing entries are unchanged.
