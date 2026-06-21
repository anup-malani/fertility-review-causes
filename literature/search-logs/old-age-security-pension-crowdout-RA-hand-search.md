# RA hand-crafted search — Old-Age Security and Pension Crowdout (C.3.c)

Author: Shravan (RA). Session: pilot-0 literature-search training. Date: 2026-06-20.
Purpose: the three practice-task outputs, built by hand BEFORE consulting the tool's
draft (`old-age-security-pension-crowdout-query-draft.md`). These are the benchmark
against which the tool's queries get compared.

Database probed live during drafting: OpenAlex (`title_and_abstract.search`), free API.

---

## Practice output #1 — hand-crafted search query (two-tier strategy)

### Why two tiers
The central concept ("pension" / "social security") is a lexically common term. A single
recall-first query returns ~4,462 OpenAlex hits — ~10x the 100–500 target — and the volume
comes from the CAUSE side, not effect-side synonym noise (verified by decomposition:
`"pension" AND "fertility"` = 1,886; `"social security" AND "fertility"` = 1,355; whereas
`"old-age security" AND "fertility"` = 172 and the children-side cluster = 45). No single
query achieves both high recall and <=500 hits, so we split into a precise hand-screened
tier and a broad ranked tier. This split is itself the documented search decision.

### Tier 1 — precise, read in full (234 OpenAlex hits, 2026-06-20)
High-signal terms that appear almost only in this literature. Every hit hand-screened.

```
("old-age security" OR "old-age security hypothesis" OR "old-age support motive"
 OR "children as investment" OR "children as assets" OR "returns to children"
 OR "provident funds" OR "notional defined contributions" OR "old-age assistance")
AND
("fertility" OR "childbearing" OR "fertility rate" OR "tfr" OR "total fertility rate"
 OR "desired number of children" OR "realized fertility" OR "desired fertility"
 OR "demand for children" OR "completed fertility")
```

### Tier 2 — broad recall safety net (4,462 OpenAlex hits, 2026-06-20)
NOT hand-screened. Handed to the tool's ranking + AI title/abstract screen to recover
the "pension"/"social security" papers Tier 1 misses. Run, sampled, and documented.

```
("old-age security" OR "pension" OR "social security" OR "retirement insurance"
 OR "old-age assistance" OR "annuitized savings" OR "old-age grants"
 OR "old-age protections" OR "notional defined contributions" OR "funded pensions"
 OR "provident funds" OR "children as investment" OR "intergenerational transfer"
 OR "returns to children" OR "returns to fertility" OR "old-age security hypothesis"
 OR "old-age support motive" OR "children as assets")
AND
("fertility" OR "childbearing" OR "fertility rate" OR "tfr" OR "total fertility rate"
 OR "effective fertility rate" OR "desired number of children" OR "realized fertility"
 OR "desired fertility" OR "child preference" OR "demand for children" OR "parity"
 OR "number of children" OR "completed fertility" OR "family size")
```

### Lessons banked during drafting
- A query is a hypothesis; the live count is the test. v3 looked clean and returned 10x
  the expected volume for a reason neither RA nor Claude predicted in advance.
- Removing overlapping effect synonyms ("parity", "family size", "number of children")
  barely moved the count (4,462 -> 3,350) because those papers also match "fertility".
- The mechanism cluster as a mandatory third AND is a recall killer (drops the canonical
  regress-TFR-on-pension paper); it belongs in reserve, used only to narrow. Even used,
  it only got the broad query to 1,179 — still over target — at real recall cost.
- Abbreviations collide across fields: "ssa" matches Sub-Saharan Africa far more than the
  Social Security Administration in a demography corpus. Dropped.

### Open lever not yet pulled
Could lift Tier-1 recall by matching "pension" in the TITLE only (not abstract) — a
field-restriction lever, distinct from add/remove-term. Worth testing before finalizing.

---

## Practice output #2 — annotated database comparison (C.3.c)

Pipeline note: databases are searched INDEPENDENTLY and the results UNIONED, then
deduplicated. Comprehensiveness comes from the union, not the intersection — each
database's value is the papers the others miss, so intersecting would discard exactly
those unique contributions.

The strongest choice to start with is Semantic Scholar. That enables us to search for
papers that map onto our complete hypothesis (cause + effect) in terms of conceptual
similarity. Resultant entries from this search are likely to be useful because they will
deprioritize and downweight papers that simply use the keywords in our query in passing,
without truly contributing to the literature on the relationship between old-age security
and fertility. Semantic Scholar will make smart, nuanced selection choices.

OpenAlex, in conjunction with Semantic Scholar, will be very useful in terms of mechanical
similarity. While Semantic Scholar upweights the papers that map onto the hypothesis
conceptually, OpenAlex upweights entries that are similar technically, and so will
contribute to precision. Moreover, OpenAlex has a key benefit: its coverage across a large
number of journals spanning economics, demography, etc. Using entries from Semantic
Scholar and entries from OpenAlex, we can build a source of truth that is both rich and
precise.

Crossref's open infrastructure will help make our records more robust and verify that
results from the previous two databases are going to be useful for our hypothesis and
contain the data that we're looking for. Crossref is highly auditable and tractable, which
is most useful for a systematic literature search. Its highly structured nature will
eliminate some of the duplication-related noise coming from OpenAlex and Semantic Scholar
while still contributing the relevant literature. It will clean up our results.

PubMed is less likely to be useful for this particular hypothesis because its focus is on
biological hypotheses, whereas the old-age security hypothesis is a predominantly economic
trade-off. Regardless, because of the low cost in running a PubMed search, it can still be
included without expectations of a large number of matching results.

Weighting for C.3.c: Semantic Scholar + OpenAlex (primary, unioned) -> Crossref (dedup /
enrichment, not discovery) -> PubMed (lowest priority, run as cheap insurance against a
gerontology/public-health recall hole).

---

## Practice output #3 — mock search log entry

Mock counts for Semantic Scholar / PubMed and all post-dedup figures; OpenAlex Tier-1
(234) and Tier-2 (4462) and search_date are real (probed live 2026-06-20). "The query" is
not one string — it is one string per database, because each database is a different
instrument with its own query language.

```json
{
  "hypothesis_slug": "old-age-security-pension-crowdout",
  "search_date": "2026-06-20",
  "databases": ["openalex", "semantic_scholar", "pubmed", "crossref (dedup/enrichment only)"],

  "queries": {
    "openalex": {
      "endpoint": "GET https://api.openalex.org/works?filter=title_and_abstract.search:<Q>",
      "tier1_precise": "(\"old-age security\" OR \"old-age security hypothesis\" OR \"old-age support motive\" OR \"children as investment\" OR \"children as assets\" OR \"returns to children\" OR \"provident funds\" OR \"notional defined contributions\" OR \"old-age assistance\") AND (\"fertility\" OR \"childbearing\" OR \"fertility rate\" OR \"tfr\" OR \"total fertility rate\" OR \"desired number of children\" OR \"realized fertility\" OR \"desired fertility\" OR \"demand for children\" OR \"completed fertility\")",
      "tier2_broad": "(\"old-age security\" OR \"pension\" OR \"social security\" OR \"retirement insurance\" OR \"old-age assistance\" OR \"annuitized savings\" OR \"old-age grants\" OR \"old-age protections\" OR \"notional defined contributions\" OR \"funded pensions\" OR \"provident funds\" OR \"children as investment\" OR \"intergenerational transfer\" OR \"returns to children\" OR \"returns to fertility\" OR \"old-age security hypothesis\" OR \"old-age support motive\" OR \"children as assets\") AND (\"fertility\" OR \"childbearing\" OR \"fertility rate\" OR \"tfr\" OR \"total fertility rate\" OR \"effective fertility rate\" OR \"desired number of children\" OR \"realized fertility\" OR \"desired fertility\" OR \"child preference\" OR \"demand for children\" OR \"parity\" OR \"number of children\" OR \"completed fertility\" OR \"family size\")"
    },
    "semantic_scholar": {
      "endpoint": "GET https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=<Q>  (bulk endpoint: | = OR, + = AND, - = NOT, \"\" = phrase, () = group)",
      "tier1_precise": "(\"old-age security\" | \"old-age security hypothesis\" | \"old-age support motive\" | \"children as investment\" | \"children as assets\" | \"returns to children\" | \"provident funds\" | \"notional defined contributions\" | \"old-age assistance\") + (\"fertility\" | \"childbearing\" | \"fertility rate\" | \"tfr\" | \"total fertility rate\" | \"desired number of children\" | \"realized fertility\" | \"desired fertility\" | \"demand for children\" | \"completed fertility\")",
      "tier2_broad": "(\"old-age security\" | \"pension\" | \"social security\" | \"retirement insurance\" | \"old-age assistance\" | \"annuitized savings\" | \"old-age grants\" | \"old-age protections\" | \"notional defined contributions\" | \"funded pensions\" | \"provident funds\" | \"children as investment\" | \"intergenerational transfer\" | \"returns to children\" | \"returns to fertility\" | \"old-age security hypothesis\" | \"old-age support motive\" | \"children as assets\") + (\"fertility\" | \"childbearing\" | \"fertility rate\" | \"tfr\" | \"total fertility rate\" | \"effective fertility rate\" | \"desired number of children\" | \"realized fertility\" | \"desired fertility\" | \"child preference\" | \"demand for children\" | \"parity\" | \"number of children\" | \"completed fertility\" | \"family size\")"
    },
    "pubmed": {
      "endpoint": "GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<Q>  ([tiab] = title/abstract, [MeSH] = controlled vocab, auto-explodes)",
      "tier1_precise": "(\"old-age security\"[tiab] OR \"old age security\"[tiab] OR \"old-age support motive\"[tiab] OR \"old-age support\"[tiab] OR \"children as investment\"[tiab] OR \"children as assets\"[tiab] OR \"returns to children\"[tiab] OR \"provident funds\"[tiab] OR \"notional defined contribution*\"[tiab] OR \"old-age assistance\"[tiab]) AND (\"Fertility\"[MeSH] OR \"Birth Rate\"[MeSH] OR fertility[tiab] OR childbearing[tiab] OR \"total fertility rate\"[tiab] OR \"demand for children\"[tiab] OR \"completed fertility\"[tiab] OR \"desired fertility\"[tiab])",
      "tier2_broad": "(\"Pensions\"[MeSH] OR \"Social Security\"[MeSH] OR \"Retirement\"[MeSH] OR pension*[tiab] OR \"social security\"[tiab] OR \"old-age security\"[tiab] OR \"retirement insurance\"[tiab] OR \"old-age assistance\"[tiab] OR \"provident funds\"[tiab] OR \"intergenerational transfer*\"[tiab] OR \"children as investment\"[tiab] OR \"children as assets\"[tiab] OR \"old-age support\"[tiab]) AND (\"Fertility\"[MeSH] OR \"Birth Rate\"[MeSH] OR \"Family Characteristics\"[MeSH] OR fertility[tiab] OR childbearing[tiab] OR \"total fertility rate\"[tiab] OR tfr[tiab] OR parity[tiab] OR \"family size\"[tiab] OR \"number of children\"[tiab] OR \"demand for children\"[tiab])"
    },
    "crossref": "NOT a discovery source. Crossref query is relevance-ranked free text with no boolean, so the boolean search is not reproducible there. Used only to resolve/enrich records by DOI and as a dedup authority."
  },

  "inclusion_criteria": [
    "(a) Contains an estimate of the relationship between old-age security/pensions and a fertility outcome. The estimate may be causal OR associative/correlational.",
    "(b) Micro- and macro-level both eligible. Record unit of analysis and identification strategy; flag aggregate studies as more weakly identified than micro studies.",
    "(c) Peer-reviewed OR a credible working paper (NBER/IZA/CEPR-class), with a named data source.",
    "(d) Date range: published 1950 or later (modern pension literature postdates ~1950).",
    "(e) Language: English, Chinese, Spanish, Japanese, Portuguese, French, German.",
    "(f) Study type: must contain a numerical estimate; no purely theoretical papers. (Foundational theory is treated as background, not evidence.)"
  ],

  "exclusion_criteria": [
    "(a) Studies pensions/old-age security but reports no fertility outcome (solvency, fiscal sustainability, portfolio/accounting, replacement rates).",
    "(b) Converse of (a): studies fertility but mentions old-age security only in passing / estimates no pension-fertility relationship.",
    "(c) No numerical estimate of the hypothesized relationship.",
    "(d) Query keyword used in a different sense (e.g. 'parity' as PPP; 'SSA' as Sub-Saharan Africa).",
    "(e) Belongs to a different hypothesis (e.g. quantity-quality / child-as-human-capital); route to that chapter.",
    "(f) Out of scope by date, language, or study type."
  ],

  "raw_counts": {
    "openalex":         {"tier1": 234, "tier2": 4462},
    "semantic_scholar": {"tier1": 150, "tier2": 3000},
    "pubmed":           {"tier1": 40,  "tier2": 800}
  },

  "post_dedup_count": {
    "tier1_union": 360,
    "tier2_union": 5400,
    "note": "Tier-1 union (424 raw) -> 360 after dedup (low overlap, small precise pools). Tier-2 union (8262 raw) -> ~5400; heavy overlap but nowhere near a 97% dup rate."
  },

  "dedup_log": "Method: (1) DOI-keyed exact merge across OpenAlex/Semantic Scholar/PubMed, Crossref used to resolve missing DOIs. (2) Conservative fuzzy fallback on normalized title + author for DOI-less records; high threshold, near-matches FLAGGED for human confirmation rather than auto-dropped (avoids over-merging same-author/near-title-different-paper pairs). Ledger records each drop as: kept_record_id, dropped_record_id, match_basis (doi|title+author), source_db.",

  "notes": "1) Working-paper -> published lifecycle produces same-study/different-DOI/changed-title pairs that survive DOI dedup as under-merges; screener must actively catch these or the same effect size gets extracted twice and double-counts in the meta-analysis. 2) 'intergenerational transfer' is a precision risk (matches inheritance/mobility literatures) -- watch at screening. 3) Tier 1 is hand-screened in full; Tier 2 is NOT hand-screened -- it is ranked + AI title/abstract screened as a recall safety net. 4) Some borderline papers straddle this hypothesis and the quantity-quality tradeoff; route by primary estimand."
}
```
