# TICK-069: D.3.c Despair and Hopelessness
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `despair-hopelessness-fertility` — HYPOTHESES-v5.md §D.3.c
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/despair-hopelessness-fertility-*, extraction/despair-hopelessness-fertility-*, output/chapters/despair-hopelessness-fertility.md, source/build/goldset/147*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — **drafted, not frozen**; 5 PI calls, 2 load-bearing
- [ ] 3. Literature search and AI screening, both phases (§5.1) — **A3 done, A4 next**
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/despair-hopelessness-fertility.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-18 — stage 2, scope drafted

**Result.** Reconnaissance (`source/build/goldset/147_d3c_recon_probe.py`, 60 probes, 0 failed) and a
scope document at `literature/search-logs/despair-hopelessness-fertility-search-scope.md`: ten
boundary walls, thirteen estimand cells, five PI calls.

Three findings changed the chapter's shape:

1. **The mechanism is not measured in the literature that studies its treatment.** Place-based decline
   AND fertility = 1,539. Despair vocabulary AND fertility = 604. All three legs together = **12**, and
   the twelve are noise apart from one book review of Case and Deaton. Same test on C.5.a: 3,120 falls
   to 20. The reduced-form literature never names the mechanism D.3.c is about.
2. **The sign is not given by the theory.** A foreclosed future is the standard explanation for
   *higher* early and nonmarital childbearing (Kearney-Levine, Edin-Kefalas, the West Virginia social-
   distress line). Same antecedent, opposite sign, different margin. Estimates now carry a mandatory
   `FERTILITY_MARGIN` tag and the opposite-sign cell sits in the primary synthesis.
3. **v5's Platt and Sterling seminal is a citation defect, not a ghost.** v5 cites a EurekAlert press
   release; the paper is Platt and Sterling (2024), *Nature Mental Health*, doi
   10.1038/s44220-024-00241-1. Recovered only by author-filtered probe — title search returns zero.
   Cherlin and Edin-Kefalas both resolve to reviews of themselves (book-canon resolver failure).

**Workflow impact.** A quoted search phrase whose first word is `not` is parsed by OpenAlex as a
boolean NOT, and the enclosing AND then returns the **unrestricted** count instead of erroring — the
contested-framework probe reported 831 where the truth is 113. The failure inflates, so it reads as a
large literature. Fixed in 147 with a comment at the site; a sweep of every `source/build/**/*.py` on
every branch found no other instance.

Script numbering starts at 147, above the max of 146 across all branches, not above main's max.

### 2026-08-18 — A3, cold-start anchor resolution

**Result.** `source/build/goldset/148_d3c_cold_start_anchors.py` (inherits B.6's resolver and five
gates) over 19 live-sourced candidates: **16 verified to live DOIs, 0 flagged, 3 monographs kept
keyed on title.** Every estimand cell the screen must route is anchored. `PRIMARY_MEASURED_DESPAIR`
is 3/3 and all three are post-communist — the American cell has no anchor, recorded as an absence.

All three Wall 1 decoys were surfaced by forward-citing the PRIMARY anchor. Philipov's forward
citations cite him for the fertility-intentions framework, not for anomie, so the one channel that
reaches this chapter's primary cell drains into C.5.a. That is the empirical case for declaring Wall 1
unenforceable at title/abstract rather than auditing it later.

**Workflow impact — four resolver defects, three of them inherited by every chapter that has run this
resolver.** All four were visible only in the *refused* set.

1. **`norm()` shattered accented surnames instead of folding them.** Each non-ASCII character was
   replaced by a space, so `Spéder` -> `sp der` -> surname `der`; `Fahlén` -> `n`; `Oláh` -> `h`;
   `Terzioğlu` -> `lu`. The author gate then answered `authors_disagree` — a confident wrong negative,
   not a missing-data `None` — and refused three anchors that had already resolved to exactly the
   right DOI at Jaccard 1.00. The same function feeds the title gate. Fixed with NFKD folding plus a
   transliteration map for the letters NFKD does not decompose (ø, ł, ı, ß, æ), and a self-test.
   Blast radius measured, not assumed, in `149_d3c_anchor_norm_audit.py`: 4 exposed anchors across 2
   chapters, **0 attributable** — the defect was live everywhere but had not yet cost an anchor,
   because D.3.c is the first corpus whose primary cell is a Central European research family.
2. **A refused query was read as an empty literature.** OpenAlex parses `?` and `*` in `search=` as
   wildcards and answers with a 200 whose body is an error object; `.get("results", [])` renders that
   as absence. Ruhm 2018, *Deaths of Despair or Drug Problems?*, was reported NO-MATCH through three
   retries while its NBER record sat indexed and live. Third instance of refusals-read-as-zeros in
   this project, and the first at the JSON layer rather than the transport layer.
3. **Title fit was a gate but not a score term.** The gate admits down to J=0.45 so subtitle drift
   survives, after which records competed on type alone: a `book-chapter` of Case & Deaton's book
   matching Ruhm's title at J=0.50 scored 22 and beat Ruhm's own NBER working paper at J=1.00, which
   scored 5. Working papers are the version of record for much of the economics this review uses.
4. **A negatively-scored record could still win.** With no positively-scored rival it took the argmax
   and was emitted as a year-drift keep — Wilson 1996 resolved that way to a 2014 Bloomsbury
   reference entry at score -50. A negative score is a statement that the record is wrong.

**And an extension to the book-canon gate.** Author-list MEMBERSHIP is not a sufficient defence for a
monograph. Wilson 1996's citation argmax is `10.2307/3042249` — Scott's review in *African American
Review*, 3,641 cites, typed `article`, **with Wilson listed as an author** — which defeats all three
inherited review signals and turns `author_match` into an endorsement of the wrong record. Signal 4
requires the record's FIRST author to be one of the candidate's; a self-test refuses to run if it
stops firing on Wilson or starts firing on the legitimate Case & Deaton records.

**The duplicate-record gate is now validated.** B.6 shipped it having never fired on a real case. Case
& Deaton's book is four distinct `book` records with citations split 1088/368/284/222; Kearney & Levine
2014 is indexed twice at 98 and 38. Author agreement holds in every case, so the corrected rule
demotes for the right reason.

One candidate-metadata error was caught **by** the gates rather than by me: the Wall 5 decoy was
entered with guessed authors (Dikmen & Terzioğlu), the author gate refused the correct DOI at Jaccard
1.00, and the live record showed the authors are Kaya & Öskay. Corrected from the record.

Scripts 148 and 149; numbering starts above 146, the max in use on any branch.

