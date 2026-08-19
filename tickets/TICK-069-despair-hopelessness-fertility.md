# TICK-069: D.3.c Despair and Hopelessness
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `despair-hopelessness-fertility` — HYPOTHESES-v5.md §D.3.c
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/despair-hopelessness-fertility-*, extraction/despair-hopelessness-fertility-*, output/chapters/despair-hopelessness-fertility-{deferral,acceleration}.md, source/build/goldset/14[7-9]*, source/build/goldset/15[01]*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — **drafted, not frozen**; 5 PI calls, 2 load-bearing
- [ ] 3. Literature search and AI screening, both phases (§5.1) — **A3, A4, B1 done; C1 partial (149,200/238,189, budget-truncated); screen staged and costed at ~$35; BLOCKED on an Anthropic credential**
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/despair-hopelessness-fertility.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise — **run once per chapter, never pooled across the split**
- [ ] 10. Demographic significance against PM / FDT / SDT — **once per chapter**
- [ ] 11. GRADE rating, 3 independent raters — **once per chapter**
- [ ] 12. Chapter drafts on the §6 template — **two chapters** (deferral, acceleration) per the Call 1 ruling
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

### 2026-08-18 — PI ruling on Calls 1 and 2

**Call 2 — decided as recommended.** Mechanism-silent reduced-form decline studies are extracted and
reported, rated **indirect**, with GRADE certainty downgraded for indirectness rather than the studies
excluded. Preserves the C.5.a/D.3.c distinction the hypothesis list draws instead of collapsing it.

**Call 1 — decided against the recommendation, and the ruling is better than the options tabled.**
The scope offered (a) rate v5's claim as written, (b) restate as a single margin-conditional claim,
(c) rate two sub-claims; the recommendation was (b). The PI's ruling is a fourth option: the deferral
and acceleration mechanisms are **different hypotheses with different treatments**, and D.3.c produces
**two chapters**. (b) would have kept one verdict spanning two treatments, which is the thing the
evidence will not support.

**One correction to the ruling's stated axis, made before implementing it.** The ruling described the
split as despair about *the present* (deferral) versus despair about *the future* (acceleration). Both
mechanisms are in fact forward-looking: v5's own wording for the deferral claim is that "the
subjective sense of having a viable future disappears", and Kearney & Levine's abstract locates their
mechanism in the *return to postponing* a birth. Applied literally, a present/future axis would put
v5's own claim on the acceleration side. The split is therefore drawn on **what the despair is
about** — the capacity to provide (defer) versus the return to postponing (accelerate) — which
preserves the ruling's substance, that these are two treatments, and matches the sources. Flagged for
the PI; relabelling is cheap if he disagrees, since nothing downstream keys on the wording.

**Structure follows B.6's precedent:** one hypothesis entry, one ticket, one search; two chapters split
at extraction on a `CHAPTER` tag; PRISMA one flow with a terminal split; risk of bias, synthesis,
demographic significance and GRADE run twice. Written up as
`decisions/2026-08-18-one-hypothesis-two-chapters.md`, which generalises the rule across B.6 and D.3.c
and states the boundary case that stays one chapter (C.2.c's tenure-conditional elasticity: one
treatment, conditional sign, not two mechanisms).

**A fortunate asymmetry.** The chapter split runs on **outcome margin**, which A4's enforceability
table marks as visible at title and abstract — unlike Wall 1, which is not. The chapter's hardest wall
is invisible to the screen; its chapter split is not, which is what makes the split cheap.

`EARLY_FERT_OPPOSITE_SIGN` renamed to `PRIMARY_ACCELERATION` across scripts 148, 150 and 151, and the
pipeline re-run: it reproduces identically (Tier B 10,589; 2,341 terms; 0 mechanism terms in the top
40), so the rename is cosmetic to the computation, which is the right outcome. The old name encoded
the framing the ruling supersedes — it is not the opposite sign of one hypothesis, it is the primary
cell of the second — and carrying it into extraction would have caused confusion later.

**Also fixed:** the scope document's status line still read "A4 is next" after A4 had run. The A4
commit's edit silently failed to apply because the replace string carried a line break the file did
not. Corrected here.

**New Call 6, open, referral to TICK-001 for v6, not blocking:** should the two mechanisms become
separate entries (D.3.c.i, D.3.c.ii) in the hypothesis list? The ruling calls them different
hypotheses, which is an argument that they should; the split is taken at synthesis for B.6's reason.

### 2026-08-18 — PI ruling on Calls 3, 5 and 6

**Call 3 — per chapter, as proposed.** The demographic-significance computation runs once per chapter,
each against its own exposure series and its own denominator: total births and completed quantum for
deferral, teen and nonmarital births for acceleration. Working through the implication surfaced a trap
worth naming before stage 10: **an accelerating mechanism works against the decline the review is
explaining**, so the two chapters' magnitudes are netted, never added. A verdict that summed them
would double-count in the wrong direction. Carries a data dependency — `data/raw/` is empty, so the
US TFR series needs its own retrieval step.

**Call 5 — admissible, tagged.** The post-communist anomie evidence is admitted with
`CONTEXT_POSTCOMMUNIST` on every affected estimate. The transportability weakness is scored in the
GRADE indirectness domain, and no pooled estimate may mix tagged and untagged studies without
reporting both separately. Excluding it would have left chapter 1's primary cell close to empty while
making the chapter look better-evidenced than it is. Bears almost entirely on chapter 1; chapter 2's
canon is American.

The extraction schema now carries four mandatory tags rather than two — `CHAPTER`, `FERTILITY_MARGIN`,
`LEVEL`, `CONTEXT_POSTCOMMUNIST` — each with its pooling consequence stated in the scope, so the rules
are in the schema rather than in a reviewer's memory at synthesis.

**Call 6 — no registry change.** Two chapters is the whole of the split; `HYPOTHESES-v5.md §D.3.c`
stays one entry. This is the first time the registry question has been ANSWERED rather than deferred
(B.6's equivalent is still standing for v6), so
`decisions/2026-08-18-one-hypothesis-two-chapters.md` was updated: the default for the next bundle is
split at synthesis, do not renumber. Recorded as a default rather than a bar — if a bundle's halves
ever stop sharing a search, the case for two entries becomes a case for two tickets, and that is when
to reopen it.

**Call 4 is now the only open call**, and it is a citation-hygiene referral to TICK-001: v5 should cite
Platt and Sterling's *Nature Mental Health* paper rather than the EurekAlert release, and C.5.a's
cross-reference still labels despair "D.3.b". Both are edits to TICK-001's file and are not made from
this branch.

### 2026-08-18 — B1, cross-validation and production query

**Run on the recommendation rather than the inherited rule**, at the PI's instruction. The inherited
B1 picks breadth at the knee of the recall-versus-budget curve; this run maximises recall and moves
routing to the screen, because A4 established that precision cannot be bought with vocabulary here.

**Result: the two-block conjunction is strictly dominated, which is stronger than the recommendation
assumed.** It is not a trade-off. At the CV-chosen breadth the conjunction retrieves 37 of 247 gold
against the outcome block's 247, **and** has lower frame precision (16.5% vs 20.9%). Requiring a
treatment term admits proportionally more decoy-cloud than gold, because decline, inequality and
uncertainty vocabulary saturates the Case & Deaton and China Syndrome neighbourhoods — the seeds whose
clouds carry no fertility quantity. Its only remaining effect is a smaller pile of the wrong records.

Diagnosis, same as A4's but in retrieval terms: outcome-block misses **0** (the backbone is complete),
treatment-block misses **205 of 247**. **83% of primary-neighbourhood fertility papers name no
treatment or mechanism in their title.** `MECHANISM` fires on 3 gold papers; `UNCERTAINTY_GENERIC` —
C.5.a's vocabulary — fires on 17.

**Two pull-reduction options measured, one taken.** The polysemy trim (bare `tempo` = 79,809 records
of music and physics, `parity` = 39,631, `natality` = 37,677, replaced by phrase forms) cuts the live
universe 546,674 -> **390,983, −28%, at zero gold cost**. A 1990 date floor would cut a further ~15%
but costs 5 of 243 gold, and the records it drops are precisely the ones the eligibility rule
anticipated — Duncan & Hoffman (1990) and the early-1990s teen-childbearing literature that is
chapter 2's canon. **Refused**: a date floor is a chapter-1 convenience paid for by chapter 2. The
distinction that makes the trim legitimate and the floor not is the axis: the trim narrows on the
OUTCOME axis, removing strings that do not denote the outcome in any chapter, which is a different
operation from the mechanism-axis precision A4 ruled out.

**Deliverable: `title.search` universe = 390,983; `title_and_abstract` = 1,894,348 (4.8x).** Measured,
not extrapolated. Recommend the title pull, with the 68 known abstract-only primary-neighbourhood
records recorded as a quantified gap to reopen after the first screening wave.

**Two honesty guards written into the outputs.** (1) Local recall is 100% by construction — the gold
is defined by a title outcome term and the query is a list of title outcome terms — so the table is
labelled a **build assertion**, not a result, and the report states that the real recall figure cannot
exist until a relevance determination is made. (2) The recall denominator is provenance-defined (Tier
B reached by a primary anchor + carrying an outcome term), because A3's snowball-*relevant* set does
not exist for this chapter; the consequence, that the outcome block's recall is uninformative and only
the treatment block's is not, is stated where the number is quoted.

**One self-inflicted error caught in the first CV run:** gold was defined on title+abstract while
matching was title-only, which put records into the denominator that no title query could reach.
Recall read 11.2% and the misses were dominated by the outcome block. Corrected to title-only, and
the 68 excluded abstract-only records are now reported as the measured cost of the title-only
convention rather than hidden inside a low recall number.

Scripts 152 and 153. **C1 is the next stage and its size needs a decision before it runs.**

### 2026-08-18 — Phase D, two-stage screen designed and costed

**D1 (`154_`) cannot shrink this pull.** At strictly-lossless gold recall it removes **8%**; the
recall-versus-budget curve has no knee — threshold 0 buys nothing (90.7% kept / 99.2% recall) and
threshold 1 costs **18% of the gold**. Primary-neighbourhood papers largely don't carry mechanism or
treatment vocabulary, which is A4's term-ranking finding and B1's conjunction finding arriving a third
time, now at record level. The paid stages absorb ~360,000 records.

**And the cost turns out to be ~$134** (`155_`): D2a Haiku 4.5 over ~360k for **$70**, D2b Sonnet 5
over ~54k survivors for **$65**, both on the Batch API's 50% discount with the rubric served from
prompt cache. At a 40% D2a pass rate it is still under a few hundred. **Screening cost is not this
chapter's constraint** — the 390,983 figure sounded like a budget problem and isn't one. RA time on
the uncertain band and full-text retrieval remain the real limits.

**Deadline worth naming:** Sonnet 5's introductory pricing ($2/$10 vs $3/$15 per MTok) ends
**2026-08-31**, worth 33% of D2b.

**Honest limit on the numbers.** This session had no Anthropic credential — no key, no `ant`, no SDK —
so token counts are **estimated from exactly-measured characters**, not counted with
`count_tokens()`. A sensitivity band is printed, the direction of error is stated (the 4.0 chars/token
divisor under-counts, so it under-states cost), and `tiktoken` is not used anywhere. Re-measure before
spending.

**Deliverables.** Rubric frozen at `{slug}-screen-rubric.md` — read from disk by the harness so the
text that ran is the text in version control, and byte-identical for caching. Harness `156_d3c_screen.py`:
Batch API, structured outputs (no prose parsing), results keyed by `custom_id` never by position,
resumable, thinking disabled on both stages as a stated cost decision.

**The screen is gated on a measured number.** `calibrate` runs D2a over the 243 id-carrying gold
records for a few cents; the full run does not start below 98% recall. A D2a false negative is
unrecoverable and invisible — that gate is the only thing between this design and a silent loss.

Two rubric rules written against measured corpus properties: **never reject a record for lacking an
abstract** (33% have none, concentrated in the older monographs and grey literature that are chapter
2's canon), and **`SECONDARY_DECLINE_NO_MECHANISM` is an inclusion** per Call 2.

**C1 is now the only blocker** — `stage1` refuses to run without the pull.

Scripts 154, 155, 156.

### 2026-08-18 — lower-recall pull priced, and rejected in favour of a better lever

Asked to price a lower-recall pull. Priced eight options against live counts and the 243-record gold
(`157_`), and the frontier is bad at every point: the most aggressive (year >= 2000 + four types)
saves **$52** and costs **39 of 243 gold records (16%)**; the gentlest that saves anything meaningful
(1990 + broad types) saves $34 for 8 records.

**Then found the cost is not where the corpus is.** Output tokens are **67% of the bill** — $90 of
$134 — and output verbosity has nothing to do with how many records are screened or how well. The
schema was emitting `"PRIMARY_MEASURED_DESPAIR"` rather than `"PMD"`, and a one-sentence rationale on
every record rather than only on the uncertain band an RA actually reads.

| route to ~$82 | gold recall |
|---|---|
| cut the corpus (year >= 2000 + mid types) | **84.0%** |
| compress the output schema | **100%** |

**The corpus-cutting options are strictly dominated** — same price, sixteen points more recall — and
none should be taken. Implemented the compression in `156_`: short cell codes on the wire, expanded
back to full names at collection so nothing downstream sees a code, and the rationale kept exactly
where it is read (`UNCERTAIN` verdicts, the RA gate's band) rather than dropped wholesale.

**Result: ~$82-90 at 100% recall**, against $134 before and the project's documented ~$37 line.

That ~$37 figure (`decisions/2026-06-20-llm-screening-pipeline.md`) assumes a conjunction-narrowed
corpus of 50K-100K records — which is precisely what this chapter could not have, since B1 found the
conjunction strictly dominated. It is stale in one direction: it silently assumes narrowing always
works. Worth restating as per-100K-records rather than per-hypothesis so the next unnarrowable chapter
does not read as an overrun.

Script 157.

### 2026-08-18 — PI decision: restrict the pull to 2000+ and four record types

**Decided and implemented.** The production query now carries
`from_publication_date:2000-01-01,type:article|review|book-chapter|report`. Universe **390,983 ->
238,189**; with the compressed schema the screen costs **~$50** against $82 unfiltered.

**Measured cost: 39 of 243 gold records (16.0%)** — 17 to the date floor alone, 19 to the type filter
alone, 3 to both. Enumerated in full in the scope so the loss is a list, not a percentage.

Two things the enumeration surfaced that were not visible when the option was chosen:

1. **The type filter does more damage than the date floor** (19 records against 17), and what it drops
   is mostly grey literature — 12 preprints, 5 dissertations — including recent on-cell work
   ("When a Strike Strikes Twice", 2022; "Privatization and the Postsocialist Fertility Decline",
   2020). This sits awkwardly against B1's own finding that working papers are the version of record
   for much of this economics: the filter keeps `report` (NBER) and drops `preprint` (SSRN, RePEc).
2. **Relaxing types to the broad set costs $6.** 2000 + broad types is 263,621 records at ~$56 and
   loses 20 gold rather than 39. The narrow set buys $6 for 19 records. Flagged once; the narrow set
   is implemented as decided.

**The scope's eligibility rule was reversed and says so.** It previously declined a date floor on the
ground that the acceleration chapter's canon is older than the deaths-of-despair framing; that
reasoning was correct and the decision overrides it deliberately. What the floor drops is a coherent
body — the 1990s welfare-and-nonmarital-childbearing literature (Duncan & Hoffman 1990, and the
1993-1998 chain), which is chapter 2's direct antecedent and Kearney & Levine's own lineage.

**Write-up consequences, recorded now so they are not discovered at drafting:** this is a restricted
search. The PRISMA identification box must state the restriction; the demographic-significance section
must not claim pre-2000 coverage; both chapters' limitations must carry the 16% loss and its
composition. A reader cannot infer a date-and-type floor from a record count.

### 2026-08-19 — screen staged on the partial pull; blocked on credentials

Asked to screen the partial. **I cannot run it: this environment has no Anthropic credential** — no
`ANTHROPIC_API_KEY`, no `ANTHROPIC_AUTH_TOKEN`, no `~/.config/anthropic` profile, no `ant` CLI, and
the `anthropic` SDK is not installed. The `CLAUDE_CODE_*` variables present are this session's own
harness plumbing, not an API key, and are not repurposed. Everything short of the API calls is done
and the screen is one command behind a key.

**D1 re-calibrated on real retrieval (`159_`), which `154_` said was owed.** `154_` picked its
threshold on the Tier B citation frame and flagged that the frame is enriched, so its survivor share
was an upper bound needing redoing against a real pull. Redone:

| | frame (154_) | real pull (159_) |
|---|---|---|
| corpus | 10,575 | **149,200** |
| survivors at lossless recall | 92.0% | **93.7%** |
| gold recall | 100% | **100%** |

D1 removes 6.3% of the real pull — even less than on the frame, and for the same reason it removed
little there. It is a budget control that this chapter's corpus does not reward, and it is kept only
because it costs nothing and its recall is measured rather than assumed.

**Screening the partial costs ~$35** (139,866 D1 survivors, compressed schema, batched), against $37
with no D1 filter at all.

**A counting bug found and fixed in `159_`, worth recording because it flattered a decision.** The
first version counted pull *records* whose title matched a gold key and reported **239** gold present
against a gold set of 243 — which made the 2000+/type retrieval filter look nearly free. It is not:
the index holds several records per work (preprint and published version, editions, reissues), so one
gold work matches two or three pull records. The distinct count is **205-209**, and the filter's cost
stands at roughly the 16% reported when it was chosen. A separate check confirmed the original figure:
of the 39 gold predicted lost, **6 are recoverable through an alternate version** (a preprint's
published article, a later edition) and 33 are genuinely absent.

**Staged for execution.** `159_` writes `temp/d3c-screen/stage1-input.jsonl` (139,866 records) and
`156_ stage1` now consumes it. With a key, the sequence is:

    python source/build/goldset/156_d3c_screen.py calibrate     # ~$0.05, gates on 98% gold recall
    python source/build/goldset/156_d3c_screen.py collect <id>
    python source/build/goldset/156_d3c_screen.py stage1        # ~$18
    python source/build/goldset/156_d3c_screen.py stage2        # ~$17

**Reminder of what the partial is** (`{slug}-c1-manifest.md`): the high-relevance head, not a random
62%. PRISMA identification must read 149,200 retrieved of 238,189 identified until the pull is
resumed.

