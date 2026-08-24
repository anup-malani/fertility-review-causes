# TICK-071: A.24 Dating Apps and Union-Formation Friction
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `dating-apps-union-formation-friction` — HYPOTHESES-v5.md §A.24
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/dating-apps-union-formation-friction-*, extraction/dating-apps-union-formation-friction-*, output/chapters/dating-apps-union-formation-friction.md

## Acceptance criteria
- [x] 2. Search strategy and scope **DRAFTED, not frozen** — `literature/search-logs/dating-apps-union-formation-friction-search-scope.md` (2026-08-24). 9 walls, 9 estimand cells, 5 PI calls open.
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/dating-apps-union-formation-friction.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-24 — reconnaissance and scope draft

Pre-scope recon (`source/build/goldset/170_a24_recon_probe.py`, 65 requests, 0 failed) plus a
named-work re-check (`171_a24_named_recheck.py`, 17 requests, 0 failed). Reports at
`literature/search-logs/dating-apps-union-formation-friction-{recon-probe,named-recheck}.md`;
scope at `-search-scope.md`.

Four findings that set the shape of the chapter:

- **The primary cell is empty and it was measured, not assumed.** Dating-app exposure against a
  population fertility quantity returns **11 records**, and no record among them estimates the
  effect; the citation-ranked head is a marriage-market paper, a popular history of romance, and two
  survey data-resource profiles. A.24 is a three-link chain (apps -> partnering -> unions -> births)
  and only the middle link has been estimated. Same shape as B.7.
- **Where field evidence exists it runs AGAINST the hypothesis.** Rosenfeld 2017 (*Sociological
  Science*) tests the choice-overload critique directly and finds meeting online does not predict
  breakup and predicts *faster* transitions to marriage; Billari Giuntella & Stella 2019
  (*Population Studies*) and Kalabikhina et al. 2020 both find *positive* broadband effects on
  fertility. The theory does not give the sign and the screen may not presume it.
- **The mechanism and the outcome live in disjoint literatures.** Choice overload is genuinely
  measured — Pronk & Denissen's rejection mind-set (27% fall in acceptance), D'Angelo & Toma,
  and one randomized field experiment with matching outcomes (Jung et al. 2021, *ISR*) — but the
  friction literature reaches a demographic outcome in 34 records, whose head is economic
  search-friction theory, a different sense of the word. This is what a Low GRADE for indirectness
  will rest on.
- **The identified variation for this chapter is C.2.h's variation.** App-specific quasi-experiments:
  33 records, none a design. Every reachable estimate runs on broadband/3G/cellular rollout and none
  says "dating app" in its abstract, so Wall 9 is **declared unenforceable** and bypassed on seed
  provenance with no dating-vocabulary requirement — A.12's Wall 8 lesson applied before the fact
  rather than after.

**Workflow finding, inherited defect.** 170_'s pass-2 named-work retries returned **zero for all
fifteen** queries. `filter=title.search:` matches the title field only, so any retry carrying an
author surname is unsatisfiable by construction, and 171_ shows `search=` does not match author names
either. Every chapter's recon script carries this pass-2 pattern, inherited from B.5, so every one of
them has been generating fake zeros. The fix (retry via `raw_author_name.search:` or by DOI) belongs
in the shared scaffold; flagged, not edited from this branch.

Two citation-hygiene items carried to A3: OpenAlex indexes Rosenfeld 2017's author as **"Michael
Rosenfield"**, which an author gate will refuse on one of the chapter's most important include-side
anchors; and both `Love Unshackled` and Ortega & Hergovich resolve to preprint/version-of-record
splits. Finkel et al.'s review resolved on neither endpoint and is recorded as **unresolved by query,
not absent**.

Scripts numbered 170-171 against the cross-branch high-water mark of 169; `main` alone would have
said 89 and collided with six live branches.

Next: A3 cold-start anchor resolution (script 172), 25 anchors, one routing decoy per enforceable
wall.

### 2026-08-24 — A3 cold-start anchors (script 172)

**26 candidate anchors, 25 resolved (23 verified live + 2 recovered by keyed exception), 1 expected
book miss, 0 flagged, 0 failed requests.** Report at
`literature/search-logs/dating-apps-union-formation-friction-cold-start-anchors-log.md`. Cells:
5 `PRIMARY_APP_UNION` · 3 `SECONDARY_TECH_*` · 8 `MECHANISM_CHOICE_FRICTION` · 2 `EXPOSURE_SERIES` ·
1 `CHANNEL1_REVIEW` · 7 routing decoys, one per enforceable wall. Machinery inherited from `161_`
unchanged; the only addition is data — five of this chapter's author names joined `_NORM_SELFTEST`.

**`PRIMARY_APP_FERTILITY` HAS NO ANCHOR AND THAT IS THE POINT.** The cell the registry entry is
actually about is carried through A4 with a recall denominator of zero rather than dropped, so the
chapter can show the denominator it is speaking about when it says nobody has estimated this.

**THE FINDING WORTH CARRYING OFF THIS CHAPTER: title-stem indexing defeats the resolver, twice in
one run.** Both OpenAlex and Crossref title Finkel et al.'s *Online Dating: A Critical Analysis From
the Perspective of Psychological Science* as **`Online Dating`** — two tokens, 776 cites, confirmed
live by DOI in both indexes. Jaccard 0.18, and `title_prefix_match` never reaches the floor because
the stem is shorter than `min_tokens=3`. The same shape appears again on Rosenfeld & Thomas 2012,
indexed as *Searching for a Mate* (full-title Jaccard 4/11 = 0.36, under the 0.45 floor); that anchor
resolved only because the stem keying was predicted in advance and used. **So the resolver cannot
resolve a work whose index entry drops its subtitle, and it fails SILENTLY — NO-MATCH reads as an
absent literature.** Recommended fix flagged, not applied, so this run stays comparable with A.12's:
apply `BOOK_TITLE_FLOOR` whenever `title_prefix_match` holds rather than only when `is_book`, and
lower `min_tokens` to 2 when the author gate has independently returned True. Belongs in the shared
resolver.

**An index TYPO in an author field defeats the author gate on the chapter's most important
include-side record.** OpenAlex spells Rosenfeld 2017's author "Michael **Rosenfield**", so
`author_match` returns False against a Jaccard-1.00 record in the right venue and year. Predicted in
the docstring before the run. The gate is right to treat a one-edit surname difference as
disagreement, so the remedy is a **keyed exception with a stated reason** — recovery applied only
after refusal, counted in its own bucket, with the gate refusal left standing in the record. Loosening
the gate would reopen exactly the failure it prevents.

**The book-canon gate met a harder case than A.12's Bulmer and held.** Becker's *A Treatise on the
Family* resolves first to a PDR record at 8,590 cites, typed `article`, **listing Becker himself as
author** — neither the type test nor the first-author test can refuse it — and it out-cites the actual
monograph record (typed `other`, 459 cites, no publication year) nineteen to one. Refused as
`review_of_the_work`; carried keyed on title with `expect_no_doi`.

**v5's seminal list is three-for-three resolvable and two-for-three irrelevant.** All three cites
exist and are correctly attributed — the defect is different from A.12's and worse to leave unstated.
Tyson et al. 2016 is a 62-cite conference measurement paper on Tinder activity logs; Bruch & Newman
2018 estimates desirability hierarchies and reply rates. Neither carries a partnership or fertility
outcome. Only Rosenfeld, Thomas & Hausen 2019 reaches a partnership outcome, and it reports that
online dating now *dominates* couple formation — evidence about the exposure's reach, not a friction.

**All three Wall 9 anchors resolved, so the bypass is buildable.** Bellou 2014, Billari Giuntella &
Stella 2019 and Kalabikhina et al. 2020 are the only identified estimates the chapter can reach and
none carries dating-app vocabulary. A4 seeds from them by provenance with no dating-vocabulary
requirement, and measures the bypass yield separately.

**Guards that were tested and passed, recorded because a passing guard is the only evidence it still
works:** both `?`-bearing titles resolved (`oa_search_safe` stripped the wildcard; `OA_QUERY_ERRORS`
empty); all four fold cases resolved, including two names carrying a DOTLESS i, which NFKD does not
decompose and only `_TRANSLIT` recovers; both version-of-record cases went to the version of record
(AER 2010 over the 2008 SSRN preprint; MIS Quarterly over a DOI-less preprint, at J=0.846, the
shortfall being the trailing footnote marker in the indexed title).

**A defect in this script's own first pass, fixed before the log was published.** The inherited log
writer carries A.12's narrative as hardcoded prose, so the first run emitted Bulmer, Pison and the
QJE DOI migration as findings *under A.24's slug*. Caught on read-back and replaced. Any chapter
mirroring a predecessor's A3 must diff the log writer, not just the candidate set.

Next: A4 citation frame (Tier A/B), script 173 — Wall 9 bypass seeded by provenance, and exact
count-only on-topic rates for the geochronology and dating-violence clouds rather than samples.

### 2026-08-24 — A4 Tier A/B citation frame (script 173)

**25 Tier A seeds, Tier B 11,001 deduplicated records, 0 failed requests.** 748 records found by more
than one seed. Report at `literature/search-logs/dating-apps-union-formation-friction-tier-ab-log.md`.

**WALL 9'S COST IS NOW A NUMBER, AND SO IS THE SIZE OF THIS CHAPTER'S IDENTIFICATION NEIGHBOURHOOD —
which is the more sobering half.** Across the **277 records reachable from any `SECONDARY_TECH_*`
seed**, 21 (7.6%) carry an outcome and no app vocabulary — the bypass population — against 7 (2.5%)
carrying app vocabulary. So the provenance bypass triples what an app-axis screen can see there, and
Billari et al.'s cloud carries **0% app vocabulary**, which is Wall 9's premise confirmed rather than
asserted. But the whole identification neighbourhood is **277 records**. A.12's equivalent was 1,991.
The bypass is cheap and correct and it is not going to rescue this chapter: the identified literature
on A.24's exposure is thin in absolute terms, and the chapter should say so in those words.

**THE OUTCOME AXIS SPLITS EXACTLY WHERE THE SCOPE PREDICTED.** Inside the 8 empirical seeds' clouds
(1,008 records), **25.6% carry a union construct and 9.5% carry a fertility quantity.** That gap is
the chapter's central empirical claim restated as a property of the literature rather than as an
argument: the evidence base reaches partnership and stops short of births.

**A substring bug fired inside the one cloud whose purpose is to have a zero.** `"dating app"` was
matched as a bare substring and hit **nine luminescence-dating papers** — *"dating applications"* —
putting the app axis at 0.9% inside the geochronology cloud. Word-boundary matching takes it to
**0.0%**. Sixth instance of the unanchored-pattern family in this codebase, and the worst-placed:
a false positive inside a decoy family reads as evidence that the carve-out is unsafe. The other term
blocks stay on substring matching deliberately — their entries are long phrases or intentional stems
(`geochronolog`, `agronom`) where a boundary breaks the match rather than sharpens it.

**A HOMONYM FAMILY THAT SHARES A WORD WITH THE OUTCOME AXIS CANNOT BE MEASURED WITH A VOCABULARY
CONTAINING THAT WORD.** The agronomic seed's exact on-outcome rate came back at **16.8%**, which
under the rule written into this script would REFUTE the Wall 2 carve-out and force an uncapped
re-pull. It refutes nothing. The outcome vocabulary contains the bare word "fertility", and in a
biofertilizer cloud "fertility" means SOIL fertility — the measurement was scoring Wall 2's own
justification as evidence against Wall 2. Re-measured on a human-anchored vocabulary the rate is
**0.1%**, and geochronology is **0.0%**. Both carve-outs stand. Both rates are now computed and both
reported, because the gap between them is the finding.

**The violence seed demonstrates the other half of the sampling argument.** Its exact rate (5.5%) is
LOWER than its sampled rate (8.2%): a capped pull returns the high-citation head, and the head of an
IPV literature is likelier to carry a marriage or partnership word than its tail. A cap does not
merely lose records, it loses them non-randomly, in the direction that flatters the diagnostic. This
run therefore computes the exact rate for **any truncated seed**, not only the homonym ones — A.12
computed it for homonyms alone.

**Wall separability, measured.** The violence cloud (8,497 citing, 5,000 pulled) carries **0.0% app
vocabulary**, so Wall 3 is separable on the exposure axis at retrieval even though the wall itself is
cut on outcome. `OFF_PLATFORM_ENG` runs 21% app and `OFF_SEXHEALTH` 43% — both share this chapter's
exposure vocabulary heavily, which is why Walls 4 and 5 have to be adjudicated per paper on outcome
and cannot be shortcut with a term sieve. That is A.12's Wall 6 lesson arriving on schedule.

**68% of the frame is decoy-dependent** (7,460 of 11,001 records reachable only from a routing-decoy
seed; 2,159 only from a homonym seed). `seed_ids` provenance is retained on every record so Recall(B)
can be recomputed without either group.

Next: D1 deterministic rank and screening cutoff (script 174). The anti-correlation to watch is the
mirror of A.12's — here the app axis is dense in the mechanism clouds and absent from the identified
ones, so up-weighting the exposure axis would demote precisely the evidence the chapter needs.

### 2026-08-24 — D1 deterministic rank and screening cutoff (script 174)

**Frame in 11,001; 262 version duplicates collapsed on normalized title, leaving 10,739 scored.
Worklist out: 887** — 800 budget slice + 83 orthogonal + 3 Wall 9 + 1 both-axes + **0 empty-cell**.
9,852 records go unread, of which 7,401 depend on a routing decoy alone and 2,151 on a homonym seed
alone. Nothing is deleted; every record keeps score, rank and hit lists so the cutoff can be re-cut
without re-running retrieval. Report at
`literature/search-logs/dating-apps-union-formation-friction-d1-log.md`.

**THE EMPTY CELL'S CANDIDATE POOL IS EIGHT RECORDS IN A FRAME OF 10,739, AND READING THEM IS THE
HEADLINE.** Records carrying app vocabulary AND a fertility term: 8. All eight already sat inside the
top 800, so the empty-cell bypass added nothing — it was insurance that cost nothing, which is the
right outcome and not a reason to remove it. Their titles are the chapter in miniature: a 2025
partnership-formation paper, a *philosophy* paper on whether state-run dating apps are morally
desirable, two mid-life/older-adult dating studies, a JOLE marriage-market paper on the costs of
ageing, and — **the one worth flagging — "Wanting or having children predicts age preferences in
online dating", which runs the causal arrow BACKWARDS.** Fertility intentions predicting dating
behaviour is the reverse-causality exemplar this chapter will need in its risk-of-bias section, and
it surfaced from the ranker rather than from a hypothesis about what we would find. This is the
frame's count, not the literature's; C1's production pull is what will test it at index scale.

**Both-axes completeness holds: 183 of 183 in the worklist, 0 unread.** Only 183 records in 10,739
(1.7%) carry the exposure and an outcome together — the frame is overwhelmingly decoy material, which
the score distribution confirms: 5,172 records score 0-4 and 3,379 score negative, so **80% of the
frame is at or below 4** against a budget margin of 28 and a top score of 132.

**The demotions did their job and the head is clean.** In the top 800: **0 homonym-only records, 0
carrying any geochronology term**, and 23 decoy-only. The head itself is 25 on-topic
dating-app/partnership records with no leakage at all. Rank 1 is *Dating apps and marriage rates*
(2026, 0 cites) — a brand-new paper squarely on link 2, invisible to any citation-weighted ranking,
and P0 for retrieval.

**Wall 9's bypass added 3 records, and that is the honest measure of it.** The tech-diffusion
neighbourhood is small enough that the ranker had already surfaced most of it. Combined with A4's
count of 277 records in the whole identification neighbourhood, the conclusion stands as stated
there: the bypass is correct, nearly free, and does not change this chapter's evidentiary position.
It recovers what is there; what is there is thin, and the chapter says so.

**The inherited orthogonal bypass returned 83 records** — larger than A.12's 40. Its yield is measured
separately at D2 per the standing rule: on A.12 the inherited bypass returned 5% against the
chapter-specific one's 44%, and an inherited bypass that has stopped paying should be retired rather
than carried forever.

Next: D2 semantic screen over the 887-record worklist (scripts 175, 176), with per-bypass yields
reported.

### 2026-08-24 — D2 title/abstract screen complete (scripts 175, 176)

**887 records screened across 15 batches. 342 RELEVANT · 23 UNCERTAIN · 522 NOT_RELEVANT.** Coverage
asserted, not assumed: every worklist record carries exactly one verdict and every verdict id is in
the worklist. Reports at `literature/search-logs/dating-apps-union-formation-friction-screen-{rubric,summary}.md`.

**THE OUTCOME AXIS SPLITS EXACTLY AS THE SCOPE PREDICTED, NOW COUNTED IN STUDIES RATHER THAN WORDS:
140 records report a partnership outcome, 56 report a fertility quantity, and TWO report both.** A4
measured the same gap in vocabulary (25.6% vs 9.5%); the screen measures it in outcomes and it
survives. The `both` count is the join A.24's claim actually requires, and it is 2 — which is really
ONE study, since the pair is a German cohort paper and its own working paper ("Meeting online and
family-related outcomes: evidence from three German cohorts" / "Online partnering and family related
outcomes in Germany"). **The chapter's headline is now a measured fact rather than an expectation.**

**Causal cells: 94 records** — 65 `PRIMARY_APP_UNION`, **2 `PRIMARY_APP_FERTILITY`**, 27
`SECONDARY_TECH_*`. A further 193 are mechanism records, which carry the mechanism section and earn
no causal recall credit. The mechanism literature is four times the size of the entire causal
literature and twenty times the size of the fertility cell.

**THE EMPTY-CELL BYPASS FAILED IN BOTH DIRECTIONS, AND THAT IS THE FINDING WORTH CARRYING OFF THIS
STAGE.** D1 flagged 8 candidates by requiring app vocabulary AND a fertility term. **Precision 0 of
8** — on reading, two were partnership studies, three ran the arrow backwards, two were
marriage-market papers whose fertility content was age-related fecundity acting as a preference, and
one was a philosophy paper. **Recall 0 of 2** — NEITHER real record was flagged, because neither
carries any app vocabulary at all: they say *"meeting online"* and *"online partnering"*, and the
exposure axis is written in noun form (`dating app`, `online dating`, `met online`). The gerund and
verb forms are not in it. Both records survived only because the ranker scored them on the outcome
axis and seed provenance. **A bypass built to protect the chapter's defining cell would have
protected nothing; the cell was saved by the ordinary ranking.** The lesson generalises past this
chapter: an exposure axis assembled from noun phrases misses the records that describe the exposure
as an action, and those are disproportionately the demographic papers, because demographers write
about *meeting* rather than about *dating apps*.

**Wall 9's population is larger and better than A4's neighbourhood measurement suggested.** 27
records reached a `SECONDARY_TECH_*` cell, and the identified estimates among them are the chapter's
real evidence base: broadband diffusion on TEEN FERTILITY (J. Population Economics), broadband and
cell phone access on MARRIAGE AND DIVORCE in the US, internet exposure in adolescence on AGE AT FIRST
MARRIAGE (J. Asian Economics), broadband on DIVORCE in China, broadband access on FERTILITY DECISIONS
(J. Asian Economics 2025), and — the single most important record the screen found — **"WIDE AND
SHALLOW: DIGITAL TECHNOLOGY AND THE POST-2007 FERTILITY DECLINE"**, which names this chapter's
exposure, its outcome and its pre-registered timing bound in one title. Every one of these was
invisible to the app axis, which is Wall 9 vindicated as a scope decision.

**Bypass yields, measured so the next chapter inherits a number rather than a habit:**

| bypass | n | survived | yield | reached a causal cell |
|---|---|---|---|---|
| budget_top | 800 | 352 | **44.0%** | 89 |
| bypass_orthogonal (inherited) | 83 | 12 | **14.5%** | 4 |
| bypass_wall9 | 3 | 1 | **33.3%** | 1 |
| bypass_both_axes | 1 | 0 | 0.0% | 0 |

The inherited orthogonal bypass returned 14.5% against the budget slice's 44% — better than A.12's
5% but still the weakest channel, and it cost 83 reads to buy 4 causal records. The Wall 9 bypass
added exactly ONE record beyond the budget slice, and that record is a P0 (`How broadband internet
access shapes fertility decisions`). A one-record bypass looks like waste until you notice which
record it was.

**Walls 4 and 5 are enforceable, but only per paper.** The screen's independent `outcome_type` agrees
with D1's term-hits on **85.8%** of records for Wall 4 and **94.9%** for Wall 5. 110 records were cut
to `OFF_PLATFORM_ENG` while a set of platform studies with MATCHING outcomes was kept — Jung et al.'s
choice-capacity field experiment, the ISR congestion and demand-disclosure experiments, the
Management Science one-way-mirror and "So, Who Likes You?" experiments, the Marketing Science
popularity-information paper. The wall held because a human read each abstract's outcome; the 85.8%
figure is almost identical to A.12's 85.0% on its own outcome-cut wall.

**Two junk-record classes and one contamination cluster.** Index records titled "References",
"Index" and "Foreword" with no content; and **four records with near-consecutive OpenAlex ids from a
single Norwegian strategic-communication volume** (AI fact-checking, a public-relations club history,
NGO influence, management communication) — an entire edited volume leaked into the frame through one
seed's reference list.

Next: stage 5 full-text retrieval, prioritised on the 2 `PRIMARY_APP_FERTILITY` records, the Wall 9
identified estimates, and the two no-abstract records whose titles imply identified designs
(`The Impact of Dating Apps on Young Adults: Evidence From Tinder`; `What Happens When Dating Goes
Online? Evidence from U.S. Marriage Markets`).
