# Gold-set DOI resolver (prototype)

Reusable resolver for turning a list of paper titles into **verified, authoritative DOIs**
for a gold-standard validation set. Built 2026-06-28 while assembling Tier A of the OAS
gold set. **Prototype status:** Python, calls live APIs (OpenAlex/Crossref polite pool),
scratchpad-origin. To be promoted to a `.claude/workflows/*.mjs` step once the gold-anchored
CV validates. Outputs are frozen as committed artifacts so the gold set is reproducible even
though the resolution process (web/agent lookups) is not bit-deterministic.

## Why it exists

The PI on-disk corpus (`*-prioritized.json`) has a **~71% DOI corruption rate** (invalid
DOIs + valid-but-wrong-paper DOIs) and unstable W-IDs. A gold set keyed on those DOIs would
measure recall against phantom papers. So DOIs are re-resolved authoritatively from titles
and independently verified.

## Production path (the reusable resolver)

```
01_dedup_empirical_core.py   strong-ID empirical core (evidenceType==4 & identification==3),
                             dedup working-paper→published clusters → distinct studies
        │  (emit resolver_input.json: {id, title, title_variants, year_hint, unverified_candidate_dois})
        ▼
AGENT FLEET (proposes)       N general-purpose agents, ~7 studies each. Prompt template in the
                             gold-set build log §"resolver agent prompt". Each agent does
                             Crossref/OpenAlex/web lookups, returns {doi, authors, venue, year,
                             confidence, evidence} and is told: NEVER fabricate a DOI; the
                             candidate DOIs are ~71% wrong; prefer version-of-record.
                             → writes resolver_agent_{n}.json
        ▼
07_verify_agent_dois.py      DETERMINISTIC DISPOSER. Re-resolves every agent DOI via Crossref;
                             accepts only if title Jaccard ≥ 0.50 AND |year-Δ| ≤ 3. Agent
                             confidence is NOT trusted. → tier_a_verified_final.json
        ▼
08_build_deliverables.py     frozen verified set + categorized manual-handoff sheet
```

## Exploratory steps (kept for provenance/audit; NOT the production path)

`02`–`06` are the journey that established the corruption finding and showed pure-API
resolution tops out ~17/35 (title-pool + W-ID-redirect). They motivated the agent-fleet
approach. `03`/`04` contain the on-disk DOI corruption audit (the doi.org/OpenAlex
cross-checks). Keep for the data-hygiene write-up; don't run them as the method.

## Key design rules (carry to the `.mjs` promotion)

- Agent proposes → deterministic verifier disposes → human adjudicates residual.
- DOI-keyed, never W-ID. Recall-match credits any member/alt DOI.
- Title-similarity guard on every resolution (reject drift; the chemistry/theology W-IDs).
- **Do NOT use the agent-fleet/web method to resolve Tier B** (keyword-disconnected tier) —
  it would contaminate Tier B toward findability and break the Recall(A)−Recall(B) correction.
- Freeze outputs; provenance every DOI (source + evidence).
