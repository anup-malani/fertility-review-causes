# datastore/ — bibliographic source of truth

`studies.json` is the **single source of truth** for every study in the review. The
bibliography (`literature/bib/*.bib`) is a *generated build artifact* — run `make bib`,
never hand-edit the `.bib` files.

## Why repo-native instead of Zotero

The pipeline finds papers through structured scholarly APIs (OpenAlex, Semantic Scholar,
Crossref, PubMed), which already return DOIs + metadata. So the "library" is a
machine-maintained registry, not a human-curated reference manager. Keeping it in git makes
the bibliography versioned, diffable in PRs (where the RA citation-check happens), and
directly readable/writable by Claude or Codex agents. A Zotero group may be added later
*only* as an optional shared PDF store; if so it exports into `literature/bib/` and is never
the system of record. See `PROTOCOL.md` §7.

## Record schema (one object per study)

```json
{
  "doi": "10.1086/250042",                    // normalized: lowercase, no https://doi.org/ prefix. Primary key.
  "citekey": "becker1960demographic",          // BibTeX key: firstauthorYYYYfirstword
  "type": "article",                           // BibTeX entry type (article, book, incollection, ...)
  "title": "An Economic Analysis of Fertility",
  "authors": ["Becker, Gary S."],              // "Last, First" each
  "year": 1960,
  "venue": "Demographic and Economic Change in Developed Countries",
  "hypotheses": ["quantity-quality-tradeoff"], // hypothesis slugs this study is screened into
  "phenomena": ["FDT"],                        // PM | FDT | SDT
  "screen_status": "included",                 // candidate | ta_screened | included | excluded
  "exclude_reason": null,                      // required iff screen_status == "excluded"
  "pdf_path": "literature/pdfs/quantity-quality-tradeoff/becker-1960-economic-analysis.pdf",
  "source_api": "openalex",                    // where the record was first found
  "openalex_id": "W2095...",
  "added_by": "claude",                        // claude | codex | <RA name>
  "verified": false                            // set true after RA citation-check passes
}
```

## Rules

- **DOI is the primary key.** Dedup on normalized DOI before appending. No DOI → use a
  stable surrogate key `nodoi:<citekey>` and flag for the source-procurer.
- One study can map to multiple `hypotheses` and `phenomena`.
- `make bib` writes one `.bib` per hypothesis slug into `literature/bib/`, containing every
  study whose `hypotheses` array includes that slug and whose `screen_status == "included"`.
- Agents append/update records; humans verify in code review and flip `verified`.
