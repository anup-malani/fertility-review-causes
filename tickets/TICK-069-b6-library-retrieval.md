# TICK-069: B.6 library retrieval — 118 records two automated passes could not reach
**Status:** open
**Assigned:** Shravan or Alexandra
**Hypothesis:** `microplastics-pfas-reproductive` — HYPOTHESES-v5.md §B.6
**Parallel-safe:** yes
**Blocks:** none — TICK-068 proceeds against the 119 records already held
**Blocked by:** none
**Touches:** literature/pdfs/microplastics-pfas-reproductive/ (gitignored), extraction/microplastics-pfas-reproductive-library-dois.txt

## Description

Needs a human with Zotero and the UChicago proxy. This is the one stage `tickets/README.md` says
earns its own ticket, because it needs different hands and can stall for weeks.

**The list is `literature/search-logs/microplastics-pfas-reproductive-library-wantlist.md`**, ordered
by retrieval value and safe to stop partway through. Save files to
`literature/pdfs/microplastics-pfas-reproductive/{WID}__{title-slug}.pdf` — the name is in the list
against every entry, and ingest picks up that path without renaming.

**State after two automated passes: 119 of 239 readable (50%).** `140` ran the publisher and
repository routes; `141` added an NCBI efetch rung that recovered 27 author-manuscript deposits in
PMC. The 118 remaining split into two groups needing different effort:

- **73 route-blocked** — OpenAlex reports an open version and the publisher refuses scripted
  downloads. **A proxy is usually unnecessary; a browser and a click will often do it.** Elsevier
  titles dominate, *Environment International* most of all.
- **45 closed** — no open version exists. Proxy or ILL.

**Two records are deliberately excluded from procurement** and listed at the foot of the wantlist as
do-not-fetch: a peer-review artefact and a duplicate. Open-peer-review journals mint a DOI per
referee report, so the frame carries them; they are not studies.

### Why the order matters here more than usual

Work Job A first (12 records — the only ones earning causal GRADE credit), and **within it, the PFAS
records before the microplastics ones.** This chapter's design is a comparison between its two
chemical halves, so a retrieval process that reaches one half more completely biases the comparison
itself and not merely the level. Realised retrieval currently runs **PFAS 51% against microplastics
59%** — and it was 38% against 59% before the efetch recovery. Working PFAS first shrinks that gap
instead of entrenching it, and the chapter's limitations paragraph has to quote whatever it ends at.

### The highest-value single record

`Serum perfluoroalkyl acids and time to pregnancy in nulliparous women` (closed). It is the
parity-handled design the Call 2 two-track synthesis is built on — the restricted track's spine.
`Preconception exposure to perfluoroalkyl and polyfluoroalkyl substances and couple fecundity` is
second: preconception measurement, so exposure precedes outcome.

### What this ticket cannot buy

Stated so the effort is spent with clear eyes. Full retrieval would not change three findings the
920-record screen already established: no study estimates either exposure against a population
fertility quantity with an identifying design; `PRIMARY_HIGH_EXPOSURE` is empty, so the
contaminated-community cohorts carrying the only exogenous exposure variation have never been studied
for a fertility outcome; and whether a study handles the parity/excretion reverse-causation problem
is a property of how it was built, which full text reveals but cannot retrofit. What this buys is the
ability to say precisely what each included study does and does not identify.

## Acceptance criteria
- [ ] Job A (12 records) retrieved or marked genuinely unobtainable, PFAS half first
- [ ] Job A2 (32 records — semen and ovarian parameters) attempted
- [ ] Job B (30 records) — each needs only enough full text to settle one routing question: mixture separability (Wall 1) or species/scope (Wall 5)
- [ ] Job C (44 records) attempted; the `r` and `k` prefixes (reverse causation, excretion pharmacokinetics) are the load-bearing ones for Call 2
- [ ] Final by-family retrieval rate recorded in the TICK-068 log, whatever it is — it goes in both chapters' limitations
- [ ] Anything still unobtainable listed with its reason, so the residual is a stated quantity rather than a silence

## Log
