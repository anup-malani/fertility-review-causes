# Retrieval Guide

## Search Order

1. `literature/AGENT.md` for author goals and prior synthesis.
2. `literature/wiki/paper-index.md` for stable local paths.
3. BibTeX files for citation keys and publication metadata.
4. Markdown summaries and spreadsheets for extracted findings.
5. Cached sidecars in `literature/wiki/extracted-text/` for repeated PDF reading.
6. PDF text extraction with `python3 ~/.codex/skills/draft-literature-review/scripts/extract_pdf_text.py "literature/path/to/paper.pdf" --project-root .`.
7. Filenames only for candidate evidence, marking filename-only inferences as `needs verification`.

## Evidence Rules

- Do not cite a source for a substantive claim unless the source or a trusted note was inspected.
- Prefer `pdftotext`/PyMuPDF text-layer extraction before OCR; use OCRmyPDF only for scanned or empty-text PDFs.
- Record local paths, sidecar paths, extraction methods, and page/section references when available.
- Ask the author for publication outcomes before recommending contribution framing if `publication_outcomes` is unspecified.
