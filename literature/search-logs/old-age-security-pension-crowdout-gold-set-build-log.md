# Gold-Set Build Log — old-age-security / pension-crowdout (C.3.c)

**Purpose:** running, committed log of *implementing* the gold-anchored keyword method
(`old-age-security-pension-crowdout-gold-anchored-keyword-method.md`). This is the
session-to-session checkpoint: what's built, what's decided, what's next. Scripts live in
the session scratchpad (`scratchpad/goldset/`) until the CV validates, then promote to
`.claude/workflows/` (decided 2026-06-28).

**Status:** IN PROGRESS — Task A, Part 1. Step 1a done; 1b resolver built + 14/35 verified;
residual handed to RA; 1c (canon/theory) not started.
**Author:** Shravan (RA), with Claude Code · **Started:** 2026-06-28

> **Note on persistence:** resolver scripts live committed at `source/build/goldset/`
> (prototype — deviates from "scratchpad-only until promote" for session continuity; promote
> to a `.mjs` workflow with the rest later). Data deliverables: `*-tier-a-verified.json`
> (frozen verified core) and `*-tier-a-manual-handoff.md` (RA residual), both in
> `literature/search-logs/`.

---

## Build plan (today = Parts 1–3 of the gold-anchored method)

Task A is implementing the one unbuilt discovery experiment (the gold-anchored keyword
method with cross-validated recall). Today targets:

- **Part 1 — assemble Tier A** (bulk/powered gold tier: keyword-findable studies). ← in progress
- **Part 2 — assemble Tier B** (adversarial / keyword-disconnected gold tier).
- **Part 3 — external term backbone** (from prior-review search strings) + mechanical
  discriminative term extraction vs. the on-disk negatives.

CV over the per-block breadth vector (Part 4) is tomorrow, after promotion.

Language: Python (scratchpad-first, promote to `.mjs` workflow once CV validates).

---

## Part 1 — Tier A assembly

### 1a. Extract + dedup the strong-identification empirical core

- **Source:** `old-age-security-pension-crowdout-prioritized.json` (PI on-disk corpus).
- **Strong-ID empirical core** = `evidenceType==4 AND identification==3`. This is exactly
  one 43-record set (the two conditions coincide perfectly), matching the spec's
  "~44 strong-identification empirical studies."
- **Dedup to distinct studies:** working-paper→published clusters collapsed by normalized
  token-set title key + a fuzzy second pass (token Jaccard ≥ 0.80 auto-merge, [0.60,0.80)
  printed for human audit). Canonical DOI per study = version-of-record preference
  (published journal DOI > SSRN/NBER/WB working-paper DOI); all member DOIs retained so a
  recall check can credit a hit on any version.
- **Result: 43 records → 35 distinct studies.** Auto-merges/clusters confirmed correct;
  the fuzzy pass correctly caught the Bismarck "'s" pair (J=0.90) and correctly did NOT
  merge the genuinely-distinct pairs (Namibia Social-Pensions vs Farm-Families; the two
  China studies; Microeconomic-Evidence vs Germany).
- Script: `scratchpad/goldset/01_dedup_empirical_core.py`

### 1b. DOI resolution + authoritative audit — MAJOR DATA-HYGIENE FINDING

**The on-disk `prioritized.json` DOI field is substantially corrupted and cannot be
trusted as the gold-set key.** Discovered while resolving/verifying DOIs:

- The on-disk `paperId` W-IDs are unstable and some are *wrong-topic*: e.g.
  `W2131777609`, labeled "…Turkey" in the corpus, resolves in OpenAlex to a **chemistry
  paper** (adamantyl cations); two others (`W3046614462`, `W2049018376`) are now **404**
  (deleted/merged). This is the same class as the known theology false-positive.
- The on-disk `doi` field is corrupted in **two** ways:
  1. **Invalid DOIs** that 404 at doi.org and are absent from OpenAlex (fabricated/mangled)
     — e.g. `10.1257/app.20190078`, `10.1007/s00148-019-00750-x`, `10.1080/00324728.2015.1012141`.
  2. **Valid-but-wrong DOIs** that resolve to an entirely different paper — e.g.
     `10.1093/qje/qjac038` (attached to the Italian-pension study) actually belongs to
     "When Should You Adjust Standard Errors for Clustering?" (Abadie et al., QJE).

**Implication:** a gold set keyed on these DOIs would measure recall against phantom
papers. So we **re-resolve every distinct study's DOI authoritatively by title** (OpenAlex
title.search → Crossref query.bibliographic fallback), similarity-guarded (token Jaccard
≥ 0.60), treating the on-disk DOI only as an untrusted hint that we audit. This directly
executes the project-wide action items already on record (re-key on DOI, audit corrupted
records) — now quantified, not anecdotal.

#### Corruption diagnosis — WHERE it occurs (script `09_corruption_diagnostic.py`)

Record-level DOI validity, split by pipeline source (strong-ID core):

| source | with-DOI correct | verdict breakdown |
|---|---|---|
| **phase1** (keyword saturation) | **8/8 = 100%** | 5 more had no DOI |
| **phase2** (citation snowball) | **3/26 = 11%** | 14 invalid-404, 9 wrong-paper, 4 no-DOI |

**It is a DOI/record misalignment in the snowball step, not LLM hallucination.** Every one
of the 9 wrong-paper DOIs is a *real DOI that belongs to a different paper already in this
corpus* (shuffle test: all 9 "elsewhere in corpus = True"). The (title, W-ID) pair stays
correct; only the DOI column is mis-joined. Same-W-ID records confirm it: `W1512976090`
("What Explains Fertility?") carries the correct `ssrn.1406946` in its phase1 row and the
wrong `qje/qjac038` (Abadie clustering-SE paper) in its phase2 row; `W4307711611` (Namibia)
is correct in phase1 (`pol.20200466`) and gets another OAS paper's DOI in phase2.

Refinement: phase2/**forward** rows have intact W-IDs but shuffled DOIs; the few broken
W-IDs (chemistry/404) are phase2/**backward** rows. Bug lives in `snowball-citations.mjs`
(Phase 2b) DOI/metadata assignment.

**Actionable consequences:**
1. **Phase1 DOIs are trustworthy** — fast-track them into the gold set without agent
   resolution. (My dedup's "prefer published over working-paper" rule wrongly preferred the
   corrupt phase2 DOI in several clusters; correct rule for THIS corpus: **prefer the phase1
   DOI**.)
2. **Corpus-wide fix is targeted and cheap:** re-fetch each record's DOI from OpenAlex by its
   (intact, forward-row) W-ID, bypassing the shuffled DOI column — rather than a full re-pull.
3. The headline "~71% of distinct-study DOIs wrong" is real but is an artifact of dedup
   picking phase2 DOIs; the cleaner statement is **phase1 100% clean / phase2 ~11% clean.**

- Scripts: `02_resolve_dois.py` (title→DOI w/ guard), `03_verify_dois.py` (DOI→title
  verification), `04_authoritative_resolve.py` (authoritative by-title re-resolution +
  on-disk corruption audit).

**Corruption rate (on-disk DOI audit, step 04):** of the 28 distinct studies that *had* an
on-disk DOI: **8 correct (29%)**, 20 wrong (71%) — split as 12 invalid-404 + 8
valid-but-wrong-paper. 7 studies had no on-disk DOI at all. Headline: **~71% of on-disk
DOIs are wrong.**

**Authoritative re-resolution result (steps 05 title-pooled + 06 W-ID, union):**
**17/35 auto-resolve** to a guard-passing DOI; **18/35 do not.** Methods overlap heavily
(title-pool 16, W-ID 15, union only 17), so the unresolved 18 are a hard residual, not a
method artifact. Caveat: a few of the 17 are likely **generic-title false positives** (e.g.
"Social Security and Fertility: Evidence from a Pension Reform in China" matched a World
Scientific book-chapter DOI `10.1142/...`; "Do Public Transfers Crowd Out…" matched an
Oxford book-chapter DOI) — so even the "resolved" set needs per-paper verification.

**Conclusion (interim):** the on-disk corpus is too corrupted to seed the gold set
automatically. A trustworthy QGS needs **per-paper verified DOI resolution**, not
guard-based auto-acceptance.

### 1b (resolution) — DECISION + RESULT

**Decision (Shravan, 2026-06-28):** option #1 — *agent proposes → deterministic verifier
disposes → RA adjudicates residual* — built as a **reusable resolver**, scoped to Tier A.
Downsides accepted (correlated LLM-hallucination risk, mitigated by never trusting the
agent's DOI; verification labor not eliminated; non-determinism handled by freezing
outputs). Hard rule: **never** use this method for Tier B (would contaminate findability).

**Result:** ran all 35 through a 5-agent fleet (7 each) → deterministic Crossref verifier
(title Jaccard ≥ 0.50 AND |year-Δ| ≤ 3, agent confidence ignored).
- **14/35 VERIFIED** into the frozen core (`*-tier-a-verified.json`). The fleet
  independently reproduced the corruption finding (candidate DOIs resolving to "Urban Growth
  and Transportation", "Global DSGE models", etc.) and correctly refused to fabricate.
- **21/35 to manual handoff** (`*-tier-a-manual-handoff.md`), categorized: **A** likely-
  not-real/chimeric corrupted records (4 — drop candidates, e.g. ids 16/19 appear to be
  corrupted variants of the one real Namibia paper, id 18); **B** rate-limited (1 — retry
  likely auto-resolves; OpenAlex/S2 were rate-limited mid-run); **C** working-paper-only
  (7); **D** real but needs human lookup / generic title (9).
- id 17 (Billari–Galasso "What Explains Fertility?") was a verifier year-gap false-negative;
  manually accepted at the SSRN WP DOI (`10.2139/ssrn.1406946`).

**Implication for Tier A size:** the nominal "44 strong-ID empirical" collapses to 35
distinct studies, of which only ~14 are cleanly verifiable and ~4 may not be real papers.
The empirical core is materially smaller than the spec assumed — Tier A will lean more on
1c (canon/theory + anchor related-work) to reach the 60–100 target, and the RA residual
pass will recover some of the 21.

### Reusable resolver — agent prompt template (production path)

The fleet prompt (parameterize `IDS` per batch; one batch ≈ 7 studies). Full rules in
`source/build/goldset/README.md`. Core invariants: candidate DOIs are ~71% wrong (verify
independently); NEVER fabricate/guess a DOI (must be retrieved from Crossref/OpenAlex/
publisher and confirmed to resolve to matching title+authors+year); prefer version-of-record
over working paper; return `{id, found, doi, resolved_title, authors, venue, year,
is_working_paper, alt_dois, confidence, evidence, notes}`; confidence=high only if DOI
resolves and title+authors+year all match; write a JSON array to `resolver_agent_{n}.json`.
Then `07_verify_agent_dois.py` re-verifies deterministically (the agent's confidence is not
trusted).

### 1b (corpus data-hygiene) — W-ID re-fetch (`10_wid_refetch.py`, `11_apply_to_goldset.py`)

The phase-2 step shuffled the DOI column but left W-IDs (forward rows) intact, so re-fetch
each record's DOI from OpenAlex by W-ID, title-guarded. Run on the full 542-paper corpus.

- **275 distinct W-ID→DOI corrections recovered** (title-verified), committed as
  `*-wid-doi-corrected-map.json`. Use this to re-key the corpus.
- **Corpus-wide source split CONFIRMED:** of checkable on-disk DOIs, **phase1 = 0% wrong
  (0/110)**, **phase2 = 47% wrong (67/141)**. Independently corroborates step 09 (Crossref:
  phase1 8/8, phase2 3/26). The DOI corruption is a phase-2-only phenomenon.
- **⚠ OpenAlex daily budget exhausted mid-run** (resets midnight UTC). So the broken-W-ID
  tail (~89 "404" + 42 "drift") is **overstated** — a mix of genuinely-dead W-IDs and
  budget-blocked requests. The 275 recoveries are solid; the dead-W-ID counts need a clean
  **rerun after the UTC reset** for true numbers (and likely more recoveries).
- **Did NOT shrink the gold-set residual.** The 21 hard residuals have dead/collided W-IDs
  *and* shuffled DOIs → only title/author resolution works for them (manual or post-reset
  agent retry). Also found a **W-ID collision**: id18 (Namibia) and id19 (Farm Families)
  share W-ID `W4307711611`; naive re-fetch gave id19 the Namibia DOI — caught by a
  uniqueness guard. Gold set stays **14/35** verified.

### 1c. Canon/theory + anchor related-work — NOT STARTED

Per spec §3, Tier A also includes canon (Neher 1971, Nugent 1985, Cigno & Rosati 1996,
Boldrin & Jones 2005, etc.) + anchor related-work (Danzer–Zyska, Boldrin–De Nardi–Jones,
Cigno–Werding, Fenge–Scheubel), DOI-resolved authoritatively the same way, then stratified
(theory / each natural-experiment setting / each era). Target size 80–100, floor 60.

---

## Key decisions (this session)

- **2026-06-28:** scratchpad-first, promote to `.claude/workflows/` once CV validates.
- **2026-06-28:** Python for the build (stats/CV); `.mjs` rewrite deferred to promotion.
- **2026-06-28:** on-disk DOIs are untrusted; all gold DOIs re-resolved authoritatively by
  title with a ≥0.60 token-Jaccard guard. On-disk DOI kept only as an audited hint.
- **2026-06-28:** consensus-pipeline framing agreed (gold set = measurement spine; query
  clusters = search structure/budget; snowball = orthogonal recall auditor + Tier-B feeder;
  Haiku→Sonnet + RA = inclusion). Synthesis doc = Task B.

## Next steps (resume here)

0. **After UTC midnight (OpenAlex budget reset):** rerun `10_wid_refetch.py` (cache will
   skip the 275 done; only the budget-blocked tail re-queries) to get true dead-W-ID counts
   and recover more corpus DOIs. Then a Crossref/web agent-retry on the gold residual.
1. **RA residual pass** on `*-tier-a-manual-handoff.md` (21 studies). Suggested order:
   drop Category A (4) unless Shravan confirms they're real; optional automated **retry**
   on B/C/D (≈17) after API cooldown before hand-resolving (could shrink the pile a lot).
   (W-ID re-fetch did NOT help these — their W-IDs are dead/collided.)
2. **Part 1c** — assemble canon/theory + anchor related-work, resolve via the same resolver,
   then **stratify** the full Tier A and freeze the validation core. Reach 60–100.
3. **Part 2** — Tier B (keyword-disconnected; orthogonal source = snowball + prior-review
   inclusions). **Resolver's agent/web method is banned here.**
4. **Part 3** — external term backbone + discriminative term extraction vs. the 4,540 on-disk
   NOT_RELEVANT negatives.

## Open questions for PI

- The corpus-DOI corruption is project-wide, not OAS-specific (~71% of on-disk DOIs wrong on
  this hypothesis; some records may not be real papers). Recommend a standalone data-hygiene
  ticket to re-key the whole corpus on authoritative DOIs before scaling to other hypotheses.
