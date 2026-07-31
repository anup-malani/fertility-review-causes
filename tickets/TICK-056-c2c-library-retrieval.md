# TICK-056: C.2.c library retrieval of the 59 missing PDFs — needs a human with Zotero + UChicago proxy
**Status:** identified core DONE (15/15) · associational remainder open
**Assigned:** Shravan or Alexandra
**Parallel-safe:** yes (no overlap with the D.3.b or B.1 chains)
**Blocks:** C.2.c extraction, risk of bias, meta-analysis, chapter
**Blocked by:** none — the automated ceiling is already hit
**Touches:** literature/pdfs/housing-costs/, extraction/housing-costs-retrieval-handoff.csv, extraction/housing-costs-pdf-retrieval-log.csv

## Description

Automated open-access retrieval for C.2.c is exhausted at **19/78 overall and 4/15 on the identified
core**. Three passes were run and each is documented in
`extraction/housing-costs-pdf-retrieval-report.md`: direct OA links, preprint-twin siblings, and OA
landing pages via `citation_pdf_url`. The ceiling matches B.1's (20/95) closely enough to suggest it
is a property of the literature and the OA infrastructure rather than of the scripts.

**The binding problem is that the identified studies are the closed ones.** The 15 quasi-experimental
papers sit in *Journal of Public Economics*, *Review of Economics and Statistics*, *Economic Inquiry*,
*Review of Economic Studies* and *Journal of Health Economics*. Eleven are still missing. Until they
are in hand:

- no pooled estimate can be produced;
- the `id_strength` labels cannot be confirmed, because QUASI_EXP vs ASSOCIATIONAL was assigned from
  titles and abstracts — so **the identified-vs-associational split itself is provisional**;
- the tenure-conditioning, parity, and tempo-vs-quantum fields the scope requires are all full-text
  facts and cannot be filled.

This is the same wall B.1 hit at TICK-041, where the pooled estimate rested on 5 studies until a human
moved it.

## Worklist

`extraction/housing-costs-retrieval-handoff.csv` — all 59 missing records, **priority-ordered with the
11 QUASI_EXP first**, each carrying its DOI link, OA status, and the specific reason automation
failed (`closed`, `publisher blocked automated fetch (403)`, `link returned HTML, not a PDF`, …).
Columns `retrieved_by` / `retrieved_date` / `notes` are there to be filled in as you go.

Retrieve the 11 QUASI_EXP first. They are the chapter; the remaining 48 are the associational stratum
and can follow.

## How to do it (Zotero)

**Filenames do not matter.** Save whatever the browser gives you into one folder; the ingest script
identifies each PDF from its own contents and renames it. Do not rename by hand.

1. **Proxy first.** Zotero → Settings → General → *Library Lookup* / OpenURL resolver set to
   UChicago's, and sign in to the library proxy in the same browser Zotero Connector uses. Without
   this, every Elsevier/Wiley/OUP link returns a paywall page and the connector saves an HTML stub
   rather than a PDF.
2. **Bulk-add by identifier.** Zotero → **Add Item by Identifier** (the green *magic wand*). It accepts
   **multiple DOIs pasted at once, one per line**. Paste:
   - `extraction/housing-costs-retrieval-dois-priority.txt` — **the 11 identified studies. Do these
     first; they are the chapter.**
   - `extraction/housing-costs-retrieval-dois-all.txt` — the remaining 52, when you get to them.
3. **Pull the PDFs.** Select the new items → right-click → **Find Available PDFs**. This is where the
   proxy earns its keep. Expect a handful to fail even so — SSRN and some Korean journals block it.
4. **Mop up the failures by hand.** For anything still without an attachment, open the DOI link in the
   proxied browser and use the Connector, or download and drag the file into the item.
5. **Seven records have no DOI** and cannot be added by identifier — search them by title in Zotero or
   the library catalogue. They are listed in the handoff CSV with an empty `doi` column.
6. **Export to a folder.** Select the items → right-click → **Export Items…** → *Zotero RDF* with
   *Export Files* ticked, or simply drag the attachments out. Any folder is fine, e.g. `~/Downloads/c2c`.
7. **Ingest.** From the repo root:
   ```
   python3 source/build/goldset/84_c2c_ingest_pdfs.py --source ~/Downloads/c2c          # dry run
   python3 source/build/goldset/84_c2c_ingest_pdfs.py --source ~/Downloads/c2c --apply
   ```
   The dry run prints a table of what it matched, how (DOI or title score), and the first line of each
   PDF so you can eyeball the match before anything is copied. `--apply` copies into
   `literature/pdfs/housing-costs/`, renames to `W<id>__<slug>.pdf`, and updates the retrieval log so
   the log and the directory cannot drift. Nothing is deleted and it is safe to re-run.
8. **Check the report.** `extraction/housing-costs-pdf-ingest-report.md` lists anything unidentified —
   usually a wrong download or a paper outside the gated set. Those need a human look.

**Two things the script already handles**, because both broke it in testing:
working papers frequently print **no DOI** at all, and `pdftotext` mangles ligatures in LaTeX-set
economics papers (one file's title extracts as *"The asymmetric housing wealth e¤ect on childbirth"*).
Matching is therefore token-containment scored, not exact — verified end-to-end on four real PDFs
renamed to `download(1).pdf` etc., all four identified.

## Acceptance criteria
- [ ] All 11 missing QUASI_EXP records retrieved, or each recorded as genuinely unobtainable with the
      route tried.
- [ ] PDFs land in `literature/pdfs/housing-costs/` as `W<id>__<title-slug>.pdf`, matching the
      convention already used by the 19 retrieved files.
- [ ] `housing-costs-pdf-retrieval-log.csv` updated so the log and the directory cannot drift.
- [ ] **The two `version=preprint_twin` files reconciled against their published versions**
      (`10.1016/j.jpubeco.2021.104366`, and the asymmetric-housing-wealth paper). Specifications
      change between working paper and article; neither may supply an extracted number until checked.
- [ ] Retrieval rate reported by stratum, since a systematically lower rate for the associational
      stratum would bias the chapter toward the identified studies — which is the *right* direction
      substantively, but must be stated rather than happen silently.

## Log
- 2026-07-31 (Shravan retrieved, Claude ingested): **the 11 missing QUASI_EXP retrieved and filed —
  the identified core is now 15/15 and extraction is no longer retrieval-bound.** All gated PRIMARY
  30/78; the outstanding 48 are the associational stratum and do not move the central estimates.
  Ingest identified 10 of 11 automatically (8 by DOI in text, 2 by title containment on files called
  `4808554.pdf` and `pdf.pdf`). **`34574.pdf` — the Korean public-rental-housing paper — is a 21-page
  image-only scan with no text layer**, so no content matcher could identify it; assigned by
  elimination through a new `--assign FILE=WORKID` option that records the call as `assigned(manual)`
  rather than leaving an untracked copy. **Two flags for extraction: that paper needs OCR and
  translation (and it is the only policy-assigned-rent design in the pool, so it cannot be dropped for
  convenience), and Daysal et al. is still the preprint twin and may not supply a number until
  reconciled against the published JPubE version.**
- 2026-07-31 (Shravan/Claude): opened. Automated ceiling reached at 19/78 (4/15 priority) after three
  passes. Report: `extraction/housing-costs-pdf-retrieval-report.md`.
