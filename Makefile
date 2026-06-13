.PHONY: bib

# Generate per-hypothesis BibTeX from the DOI-keyed registry (datastore/studies.json).
# The .bib files in literature/bib/ are build artifacts — never hand-edit them.
bib:
	python3 scripts/make_bib.py
