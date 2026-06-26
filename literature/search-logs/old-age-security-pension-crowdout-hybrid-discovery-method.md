# Hybrid Top-Down → Snowball → Filter: an alternative discovery method for OAS

**Date:** 2026-06-25 · **Author:** Shravan (RA), with Claude Code
**Hypothesis:** old-age-security / pension-crowdout (C.3.c)
**Status:** experiment — evaluated against the PI's baseline corpus. Not adopted as the production pipeline; recommended as a *recall complement* to keyword search. Scripts and raw outputs live in the session scratchpad (`oas-altsearch/`), not committed.

---

## 1. Motivation

The PI's baseline discovery pipeline (OpenAlex keyword saturation-screen + 1-hop citation snowball + Sonnet prioritization) produced 542 tiered RELEVANT papers. This experiment asks a different question: **can a citation-first method, anchored on a hand-enumerated seed set, find the OAS literature — including papers the keyword pipeline missed?** It is designed to be measured, not trusted: every step is evaluated by set arithmetic against the baseline and against a held-out gold set.

## 2. The method

```
Top-down seed enumeration (Opus)
    Theory papers + natural experiments + prior meta-analyses/reviews of the
    pension -> fertility relation (causal direction checked at enumeration).
        v
Resolve each seed title -> OpenAlex work, with a TITLE-SIMILARITY GUARD
    Jaccard(requested title, matched title) >= 0.50, else reject.
    (Guards against resolution drift — naive "top hit" matched Neher 1971 to a
    different paper, Cigno 1993 to another. The guard rejects rather than poison.)
        v
Staged citation snowball, ASYMMETRIC:
    Backward (references) from ALL seeds       — high precision, finds ANCESTORS (older)
    Forward  (cites:)     from EMPIRICAL seeds  — high recall,   finds DESCENDANTS (newer)
    Generic theory anchors (Becker-type) are backward-only: forward-citing them
    pulls in all of fertility economics.
        v
Stop on RELEVANCE SATURATION, not a raw count
    Iterate rounds; stop when a round adds < ~5% new screened-relevant papers.
    (Rejected an earlier "stop at 50,000 results" rule: raw count is dominated by
    forward-citations of a few high-citation theory seeds = noise, and is
    non-monotonic in relevance — it can halt mid-round before the precise frontier
    is expanded.)
        v
Bottom-up LLM relevance filter (same screen as baseline) over the universe.
```

### Design decisions and why
- **Saturation stop over raw-50k count.** A 50k universe is the same order of magnitude as the full keyword universe (~80k) — it forfeits the efficiency of saturation and gorges on backward-citation noise. Empirically confirmed below: of 444 round-1 "novel" papers, only ~7 were on-topic.
- **Asymmetric snowball.** Confirmed empirically: round-1 backward reached only the *oldest* gold paper (1990); every other gold hit came via forward. Since the OAS empirical literature is overwhelmingly 2010s–2020s, **forward is the workhorse**.
- **Title-similarity guard on resolution.** Necessary: naive Crossref/OpenAlex top-hit resolution drifted to wrong papers. The guard correctly rejected the drifts instead of seeding from a hallucinated/wrong paper.
- **Join on DOI, not OpenAlex W-ID** (see §4, Finding 2).

## 3. Evaluation design

- **Held-out gold:** 12 canonical Tier-1 papers (theory + the Italian/China/Chile/Bismarck natural experiments + the 1990 econometric classic) **deliberately excluded from the seed set**. The test is whether the snowball *reaches* them.
- **Baseline comparison:** set intersection of the method's universe with the PI's full screened set (papers "saw") and RELEVANT set.
- **Two keys, deliberately:** first W-ID, then **re-run on DOI** after discovering W-IDs are unstable across re-pulls (§4, Finding 2).

## 4. Results

Seeds resolved: **10 / 12** (Neher 1971 & Cigno 1993 dropped by a URL-encoding bug on comma-heavy titles in `title.search`, not by the guard — fixable).

| Metric | Round 1 | Round 2 (cumulative) | Round 2, **DOI-keyed** |
|---|---:|---:|---:|
| Universe size | 677 | 5,245 | 4,336 DOIs |
| Held-out gold reached | 3 / 12 | 5 / 12 (raw) | **4 / 10 valid** (5/11 incl. NRPS) |
| Recovery of PI-relevant | 123 (10%) | 388 (32%) | **263 / 928 = 28%** |
| New relevant added by the round | — | +265 | — |

Round 2 forward-expanded 117 confirmed-relevant papers (held-out gold excluded).

### Findings

**1. Recall improves with rounds but plateaus below complete — a genuine ceiling.**
Recovery climbed 10% → 28–32% across two rounds and was **not saturated** (round 2 still added 265 new relevant). But on the *stable DOI key*, the method genuinely **misses** canonical papers after two rounds from 117 relevant seeds — *Children as a Form of Retirement Saving* (REStud), *Pensions and Fertility in Austria*, the Chile privatization and China social-security studies. These are OpenAlex citation-graph gaps, not distance-in-network. **This is the central argument for keeping citation-snowball as a complement to keyword search, not a replacement: keyword search structurally catches what the citation graph cannot.**

**2. OpenAlex W-ID is an unreliable join key; use DOI.**
OpenAlex merges duplicate works over time and reassigns W-IDs, so the baseline `prioritized.json` W-IDs have drifted (e.g. *Children as a Form of Retirement Saving*: baseline `W2133124695` → live `W2167683892`). Consequences: (a) set-arithmetic between corpora built days apart is noisy at the per-paper level; (b) `cites:<dead-id>` silently returns nothing, so a drifted seed loses its forward edges. **Re-running the comparison on DOI changed the aggregate recovery only marginally (32% → 28%)** — so drift did not swing the headline number — **but it matters for dedup and any per-paper join, and the whole corpus should be re-keyed on DOI.**

**3. The baseline corpus contains corrupted records.**
`W2014516694`, labelled "A Fiscal Theory of Social Security and Family Size," actually resolves in OpenAlex to a *theology* paper ("Heinrich Bullinger and the doctrine of predestination"). Consistent with the batch-2 unmatched-ID investigation. A data-hygiene audit is warranted independent of search method.

**4. A big universe is not a relevant universe.**
Round 1: 444 papers not in the baseline, but only ~7 plausibly on-topic — backward references of theory seeds drag in general economics. Recall must come from forward expansion + hard filtering, not from inflating raw count. (This is the empirical case against the 50k rule.)

**5. The method does find genuine novel papers.**
Examples not in the baseline screened set: *Child Support, Pensions and Endogenous (and Heterogeneous) Fertility* (2017); *How Pension Systems Influence Fertility* (2009); *Mixing Bismarck and child pension systems* (2009); Cigno & Werding, *Children and Pensions*. Citation-network discovery surfaces keyword-disconnected work, as intended.

## 5. Verdict and recommendation

- The hybrid method is sound and the saturation-stop edit is vindicated (recall never reached a clean natural stopping point; a raw count would have been arbitrary).
- As a **standalone** discovery engine it plateaus at ~30% of the baseline's relevant set after two rounds, with a real ceiling from citation-graph incompleteness. **Adopt it as a recall booster layered on keyword search** — i.e. the PI's architecture, upgraded with (a) a richer enumerated + meta-analysis-seeded set, (b) multi-round forward expansion, (c) the saturation stop, (d) the resolution similarity-guard.
- **Two project-wide actions fall out regardless of search method:** (i) re-key the OAS corpus (and the dedup/snowball steps) on **DOI**; (ii) audit for corrupted records like the theology false-positive.

## 6. Reproducibility

Scripts (scratchpad `oas-altsearch/`, read-only against the repo):
- `seeds.json` — enumerated seeds + held-out gold
- `run.py` — resolve (similarity guard) → round-1 snowball → evaluate (`result.json`)
- `characterize.py` — lexical relevance of novel papers (`novel_characterized.json`)
- `round2.py` — round-2 forward expansion + saturation check (`result_round2.json`)
- `doi_compare.py` — DOI-keyed baseline comparison (`doi_compare_result.json`)
- `EVAL-MEMO.md` — running analysis memo

Data source: OpenAlex (live), Crossref. No API key; `mailto` polite-pool. OpenAlex citation edges and reference lists are incomplete for some older/merged works — a material limitation for any citation-based method.
