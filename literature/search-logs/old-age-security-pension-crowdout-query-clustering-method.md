# Anchor-Guided Query Clustering: an alternative search method for OAS

**Date:** 2026-06-27 · **Author:** Alexandra (RA), with Codex  
**Hypothesis:** old-age-security / pension-crowdout (C.3.c)  
**Status:** prototype — implemented in ignored `temp/` scripts and evaluated on OAS. Not adopted as the production pipeline.

---

## 1. Motivation

The PI baseline pipeline uses OpenAlex's default relevance ranking for the first discovery phase, then
uses citation snowballing and LLM prioritization to recover and rank papers. Shravan's subsequent
method notes identified two separate concerns:

1. A citation-first method can miss canonical papers because OpenAlex's citation graph has real gaps.
2. A keyword method needs a way to measure and improve recall rather than simply trust one broad query.

This prototype asks a narrower operational question: **can we reduce dependence on one OpenAlex query
ranking by searching multiple vocabulary clusters separately, using anchor papers to allocate search
budget across clusters, and ranking papers before any LLM screening?**

The method deliberately does **not** scrape Google Scholar. Google Scholar can be useful for manual
anchor discovery, but scraping it is fragile, hard to reproduce, and likely to hit blocking/CAPTCHA
constraints. The prototype uses OpenAlex only.

## 2. The method

```
Hand-built anchor set
    canon + theory + natural experiments, assigned to query clusters
        v
Resolve anchors in OpenAlex with DOI-first lookup and title-similarity guard
        v
Score each query cluster:
    anchor recovery + local sample yield - noise
        v
Allocate a fixed keyword-search budget across clusters
        v
Run clustered keyword search
    formal pensions / social security-PAYG / old-age-security motive /
    children-as-support / intergenerational transfers
        v
Deduplicate by OpenAlex ID, DOI, then normalized title
        v
Rank papers deterministically before LLM:
    anchor relation + cluster overlap + title/abstract terms + citations +
    causal-design terms - reverse-direction penalties
        v
Select cluster-balanced snowball seeds
        v
Backward + forward OpenAlex snowball
        v
Final ranked list + top-100 RA/LLM handoff
```

### Design decisions and why

- **Union, not intersection.** Requiring papers to appear in multiple clusters would drop genuine
  papers that use only one vocabulary family. Cluster overlap is used as a priority signal, not an
  exclusion rule.
- **Anchor-guided budget allocation.** Clusters that recover assigned anchors and show high local
  yield get more search budget. This makes the allocation observable rather than relying on a single
  broad query ranking.
- **Title-similarity guard for anchors.** OpenAlex title resolution can drift. The workflow accepts a
  resolved anchor only when DOI matches or Jaccard title similarity is at least 0.50.
- **Pre-LLM deterministic ranking.** The workflow ranks records before any LLM call so that a later
  Haiku/Sonnet screen can be run on the highest-value records first.

## 3. Prototype implementation

Scripts and outputs are in ignored `temp/` files:

- `temp/anchor_guided_search_workflow.py`
- `temp/test_anchor_guided_search_workflow.py`
- `temp/anchor-guided-search-workflow-report.md`
- `temp/old-age-security-pension-crowdout-anchor-guided-final-ranked.csv`
- `temp/old-age-security-pension-crowdout-anchor-guided-ra-handoff.csv`

The implementation uses conservative caps:

- total keyword budget: 900 requested records
- cluster floor: 100
- batch size: 50
- seeds per cluster: 3
- backward references per seed: 20
- forward citations per seed: 20

## 4. Results from the latest prototype run

The cleanest completed report is `temp/anchor-guided-search-workflow-report.md`.

| Metric | Count |
|---|---:|
| Anchors resolved | 12 / 12 |
| Keyword union after deduplication | 356 |
| Snowball union after deduplication | 132 |
| Final ranked union | 466 |
| Duplicates identified | 215 |
| RA/LLM handoff rows | 100 |

Top-100 handoff composition:

| Tier | Count |
|---|---:|
| Tier 1 | 87 |
| Tier 2 | 13 |

Final deterministic labels:

| Label | Count |
|---|---:|
| relevant | 46 |
| maybe_relevant | 111 |
| not_relevant | 309 |

The top ranked records include expected anchors and closely related papers: Nugent (1985), Namibia
social pensions, Italian pension reforms, China NRPS, Cigno children/pensions, old-age security
models, and social-security/fertility theory papers.

## 5. Limitation exposed: API rate limits

The prototype hit OpenAlex `429 Too Many Requests` during repeated anchor resolution, cluster
sampling, keyword pulls, and snowball calls. This is not a query error; it means OpenAlex temporarily
refused more requests from the client. One response included an extremely large `Retry-After` value,
which would have made the script sleep for hours if not interrupted.

The script was patched to add request throttling and capped retry/backoff. That avoids accidental
multi-hour sleeps, but a production version needs stronger infrastructure:

- persistent request cache
- resumable stage outputs
- DOI-keyed dedup throughout
- polite request scheduling
- bounded retry/backoff
- separate dry-run and production modes

## 6. Comparison to Shravan's method notes

**Versus the hybrid top-down → snowball method:** this is not citation-first. Citation snowballing is
used only after clustered keyword search and anchor-guided ranking. That avoids making OpenAlex's
citation graph the main recall bottleneck.

**Versus the gold-anchored keyword method:** this is more operational and less statistically
defensible. It uses anchors to score clusters and allocate budget, but it does not yet build a frozen
DOI-keyed quasi-gold set, run 10-fold cross-validation, or estimate Tier A versus Tier B recall.

The natural synthesis would be:

```
Gold-anchored method supplies the validation framework.
Query clustering supplies the operational search structure and budget allocation.
```

## 7. Verdict and recommendation

The prototype is useful as a **search-routing and prioritization design**, not yet as a replacement
for the production pipeline. Its main value is that it makes search budget allocation explicit across
vocabulary families and produces a ranked top-100 handoff without scraping Google Scholar.

Recommended next step:

1. Add persistent caching/resume support.
2. Rerun after the OpenAlex rate limit cools down.
3. Compare the top-ranked output against Shravan's proposed DOI-keyed quasi-gold set.
4. If recall is competitive, fold query clustering into the gold-anchored keyword method as the
   cluster/budget-allocation layer.

## 8. Reproducibility

The prototype is reproducible from the ignored temp script while the files remain local:

```
python3 temp/anchor_guided_search_workflow.py
python3 -m unittest temp/test_anchor_guided_search_workflow.py
```

Because the script calls the live OpenAlex API, exact results may vary over time and the run may fail
or partially complete under rate limits. The committed method note records the run design and the
observed diagnostics; it is not a frozen production corpus.
