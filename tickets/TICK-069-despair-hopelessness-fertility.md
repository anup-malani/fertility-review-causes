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
- [ ] 3. Literature search and AI screening, both phases (§5.1) — **A3 and A4 done; B1 deferred pending Calls 1-2**
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

### 2026-08-18 — A4, citation frame and term population

**Result.** `150_d3c_tier_ab_frame.py`: Tier B of **10,589 deduplicated records**, 856 multi-seed,
**0 failed requests, no seed truncated** at the raised 5,000 cap. `151_d3c_discriminative_terms.py`:
2,341 candidate terms mined by Fightin' Words over title and abstract.

**The frame reproduces the chapter's central finding by an independent route.** Across every seed's
forward cloud, **30 of 10,769 records (0.28%)** carry a fertility quantity and a despair construct
together. The reconnaissance measured that from keyword counts at the population level; this measures
it in the citation network. The China Syndrome's 4,436 citing works contain zero. Case and Deaton's
two seeds, 3,853 citing works, contain four.

**Wall 1 is now measured rather than argued, and the measurement is unambiguous.** The term mining
labels positives by CITATION PROVENANCE — reached by a primary-cell anchor — not by vocabulary,
because labelling by the despair-and-fertility co-occurrence would have mined the very words used to
draw the line. In a chapter whose primary cell IS a co-occurrence that is not a subtle circularity,
it is the whole result. On that label:

- `MECHANISM_AND_OUTCOME` contains **0 terms**. The primary cell has no mineable vocabulary.
- **0 of the 40 strongest discriminators carry mechanism vocabulary.**
- **`despair` is NEGATIVELY discriminative — z −4.44, 5 occurrences in the primary neighbourhood
  against 635 in the walls'.** The word the hypothesis is named for marks the mortality corpus it has
  to be separated from; in a production query it would pull toward Wall 4's decoy cloud.
- The only precise mechanism term is `future orientation` (z 0.7, 6 positive / 0 negative) — too rare
  to carry a query.

**Unplanned third finding, and it bears on Call 5.** After the topic words the strongest
discriminators are place names — `europe` 16.4, `hungary` 14.4, `poland` 11.5. What most
distinguishes the primary neighbourhood is where its studies were done. A query fitted on this frame
learns to retrieve Central European demography rather than despair research.

**Workflow impact.**

1. **Book seed recovery added.** A DOI-less monograph could not seed the frame at all, and the three
   this chapter lost were the sociological canon — whose neighbourhood is where the opposite-sign
   qualitative literature lives. Each now gets one recovery attempt restricted to bookish types and
   gated by the A3 first-author rule. Edin & Kefalas recovered (`W4242866627`, `book`, 125 cites) and
   seeded normally; Wilson and Cherlin did not, correctly — no `book`-typed record of either exists.
   The Wilson attempt is a live demonstration that the author gate is not optional here: a bookish
   search for *When Work Disappears* returns Johnston & Lordan's unrelated 2014 book above anything
   of Wilson's.
2. **Numeric tokens were entering the term list.** The first run ranked the bare token `233` eighth
   overall (z 20.6, 115 positive occurrences) — volume and page fragments surviving into abstracts.
   A term list feeds a production query, so an unsearchable token is worse than useless; it reads as
   a finding. Now filtered.
3. **The provenance label is worth carrying forward.** Any chapter whose primary cell is defined by a
   co-occurrence of two vocabularies cannot label its term-mining positives by that co-occurrence.
   Citation provenance is a label that owes nothing to the text.

**Recommendation, and it is a change of plan.** B1 cross-validation should NOT run next. It picks a
production query on a recall-versus-budget frontier, and A4 has established that the available
vocabulary cannot separate the primary cell from the walls — so fitting a query on this frame
optimises retrieval of Central European fertility-intentions research. Calls 1 and 2 should go to
Anup now, with A4's measurement attached, and the budget should shift from query precision to
full-text screening capacity, which is the only stage where Wall 1's discriminator is visible.

Scripts 150 and 151.

