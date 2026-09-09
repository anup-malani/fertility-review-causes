# TICK-083: C.3.d Quantity-Quality Tradeoff
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `quantity-quality-tradeoff` — HYPOTHESES-v5.md §C.3.d
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/quantity-quality-tradeoff-*, extraction/quantity-quality-tradeoff-*, output/chapters/quantity-quality-tradeoff.md, source/build/goldset/34[4-9]*, source/build/goldset/35*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/quantity-quality-tradeoff-search-scope.md`, 2026-09-09
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/quantity-quality-tradeoff.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

**Not the smallest frame — the largest of the three finalists, and chosen anyway.** On the 2026-09-03
probe (`literature/search-logs/candidate-frame-probe-2026-09-03.md`, still only on the 078 branch)
the union frames of the finalists were C.2.b **587**, A.6 **675**, C.2.f **714**, A.3 **726**, C.3.d
**762**. C.2.b (TICK-079) and C.2.f (TICK-081) are both drafted. Of what is left the spread is A.6
675 → C.3.d 762, **13%**, and TICK-079 set the precedent that 15% is inside vocabulary noise. Size
does not decide this. The tiebreak does, and it runs three ways at once.

**A.6 and A.3 lose on inherited boundary debt, which is TICK-081's argument unchanged.** A.6's
stigma-specific axis returns **12** records against a 675 union and A.3's core is **26** of 726 — both
frames are almost entirely loose general-purpose vocabulary rather than an anchored literature. A.6 is
by construction the residual left after A.2, A.4 and A.5. Checked 2026-09-09: none of those three has
a branch on `origin`, so all remain unstarted and the diagnosis stands a second time.

**C.3.d's core is 567 of 762** — an anchored literature, the same signature that made C.2.f preferable
to A.6 a week ago.

**Both of C.3.d's walls are already written, by chapters that are already drafted.** C.2.b's scope
ruling 2 was deliberately drafted in a form C.3.d could inherit. C.2.f's ruling 1 states the split
directly: C.3.d owns variation in the *return* to child quality, C.2.f owns variation in the
*reference standard*. This chapter inherits both rather than re-litigating either.

**The decisive reason is that C.2.f's PI call 3 is a question about C.3.d that gets more expensive
every week it waits.** The C.2.f chapter (drafted 2026-09-08) found that **eight of its nine studies
cannot separate the return from the reference standard**, and asked whether the C.2.f/C.3.d boundary
is tenable at all — flagging explicitly that it is decidable *because C.3.d is unstarted*. Once
chapters exist on both sides of that wall, reopening it means rewriting both.

**No frame number goes in this ticket until the homonym check runs.** The 09-03 probe ran a homonym
check for C.2.b only, and TICK-081 opened with the same gap. "Quality" is a far larger and more
general word than "inequality" was, and C.2.f's own shape — a 690-record core against a 24-record
social-comparison sub-literature — is the signature of a frame carried by one general-purpose axis.
Per `anchored-vocabulary-has-own-homonym`, score each anchor term alone before trusting the block;
per `calibrate-the-outcome-axis-too`, the outcome axis needs the same treatment. Re-run `304_` first
so the numbers this chapter is scoped against are current rather than six days old and on a branch.

## Open rulings to freeze at stage 2

1. **C.3.d vs C.2.f, inherited but now under active challenge.** The registered split is return
   (C.3.d) vs reference standard (C.2.f). C.2.f measured that split and found only one of nine studies
   could honour it. Do not simply re-assert the wall: measure it on C.3.d's own pool the way C.2.f
   did, and if it fails from this side too, that is a finding about the registry, not about the
   search. C.2.f's PI call 3 is the place it lands.
2. **C.3.d vs C.2.b.** C.2.b owns the *price faced* for a child at fixed quality; C.3.d owns the
   *shadow price of quantity* induced by the return to quality. C.2.b's ruling 2 is the inheritable
   form. Name what happens to studies that measure total expenditure per child without decomposing
   it — that is C.2.b's estimand or neither's, and `read-the-mechanism-not-the-instrument-name`
   applies.
3. **The registry absorbs SBTC into this entry, and that decision needs operationalizing.** The notes
   say skill-biased technical change is "the technology shock that raises the return to human
   capital" — the same mechanism in another framing. Decide at stage 2 whether SBTC-exposure studies
   (routine-task displacement, computerization, trade shocks) that estimate fertility effects belong
   in the primary cell or are a separate arm. They will not share a vocabulary with the Becker
   literature, so this decides a whole search axis, not just a routing rule.
4. **The exposure is not one variable, and the QQ literature knows it.** Returns to schooling, family
   size shocks (twins, sibling sex composition), compulsory-schooling reforms and unified-growth
   calibrations are four different estimands wearing one name. `stratify-before-counting-poolable`
   applies at extraction, but the strata must be derivable from a required-tags list decided here.
   Note that the twin-instrument literature is A.12's exposure used as C.3.d's instrument — `A.12`
   is drafted, so check its pool before building one.
5. **The famous micro result runs against the hypothesis, and the macro literature is calibrated
   rather than estimated.** Black-Devereux-Salvanes 2005 finds little tradeoff; the registry says so
   itself. Galor-Weil and Galor-Moav are unified-growth calibrations, not identified estimates.
   Decide before searching how calibrated macro models are treated — `anchor-on-the-estimand-not-the-famous-design`
   says the celebrated designs may not measure the outcome at all, and on C.3.e that was exactly
   right.
6. **FDT *and* SDT, which is unusual here and doubles the demsig work.** Most recent chapters have
   been SDT-only. Per `three-demsig-routes-before-not-assessed`, name the live route for each
   phenomenon separately at stage 2. Returns-to-schooling series for the FDT window are thin and
   country-specific; say now what would make the FDT cell computable rather than discovering at
   stage 10 that it is not.

## Assets in hand before the cold start

- **Free seeds.** C.2.b, C.2.f, C.3.e, C.3.f, C.3.g, D.2.d and A.12 all plausibly routed
  QQ records into their own screen files. Port the free-seed harvester (`335_c2f_free_seeds.py`,
  the newest copy); `snowball-pools-omit-their-own-seeds` in reverse, and it costs nothing.
- **Shared libraries are canonical on `main` now.** `source/lib/textnorm.py` (TICK-074, merged
  2026-09-08) and `source/lib/openalex.py` (merged 2026-09-08). **Import them; do not copy a
  `norm()` or an OpenAlex client.** Note TICK-082 is open against `textnorm.norm()` — it does not
  strip HTML markup — so expect that defect rather than rediscovering it.
- **Anchor resolver.** Port from `336_c2f_cold_start_anchors.py`, the newest copy.
- **Script numbering.** Max across **every branch on origin** is 343, so C.3.d starts at **344**
  (`script-number-collision`: start above every branch, not above main).
- **Merge debt is a live hazard.** The frame probe (`304_`) and every script this ticket ports sit
  on unmerged branches. Note what gets ported and from where, or the next chapter re-derives it.

## Log

### 2026-09-09 — opened, claimed, and stage-2 diagnostics run

**Chosen against a re-run probe, not the six-day-old one.** Ported
`304_candidate_frame_probe.py` from the 078 branch (it had never been on `main`) and re-ran it with
C.2.b and C.2.f moved into `STARTED`. Union frames of the three remaining bracketed finalists:
A.6 **680**, A.3 **727**, C.3.d **762**, against 675 / 726 / 762 on 09-03. The spread is 12%, inside
the 15% band TICK-079 set as vocabulary noise, so the ranking does not overturn the tiebreak in
*Why this one now*. Control (C.3.e, chapter written) returned 85.

**A silent no-op in the probe, fixed.** Every row in the script's `HOMONYM` pass belonged to C.2.b
or C.6.a, both now started, so `keep()` stripped the whole pass and the generated table printed a
`## Homonym check` heading over an empty table. The list is per-candidate and is not maintained
forward. Both the console and the markdown now say so rather than reading as a clean check —
`safeguards-must-be-measured-not-trusted`.

**344 — the exposure axis. C.3.d is not C.2.f's shape.** Its dominant term is the mechanism's own
name rather than a general-purpose word: `quantity-quality` 494 of the 762 frame, `child quality`
243, `quantity quality tradeoff` 95, `child investment` 40, `human capital of children` 31,
`sibsize` 27. Dropping `child quality` costs 176; dropping `child investment` costs 30, so the
ticket's worry about that term is real but nearly free either way. Candidate terms were priced by
**marginal gain** over the axis rather than by their own size, so no boolean `NOT` was needed;
`quality-quantity`, the reversed hyphenation, is worth **+138** and is a candidate, not yet a term.
0 of 47 requests refused.

**345 — the outcome axis. One worry cleared.** "Fertility" is a soil-science and animal-husbandry
word and `quantity-quality` is a stock phrase in both, so 344's 8,154 → 494 drop could have been the
restriction selecting a different species. Non-human residue inside the frame is **43 of 762
(5.6%)**, and 42 of the 43 sit under the single outcome word `fertility` — the other five outcome
terms carry 0, 0, 0, 2, 0. On A.24 this pattern was 16.8%, so it was worth the queries.

**345 — the finding that defines the chapter, and it lands on rulings 4 and 5.**

| measured inside the 762-record frame | n |
|---|---|
| forward: returns-to-skill exposure **and** a fertility outcome | **8** |
| backward: child-outcome vocabulary | 200 |
| backward **with an identified family-size design** attached | 35 |
| the twins / sex-composition literature paired with child outcomes, **outside** the axis | 1,562 |

C.3.d's registered claim runs forward — rising returns to child human capital lower desired
fertility. Eight records inside its own frame carry both halves of that. The literature that exists
tests the **backward** direction (does exogenously larger family size lower per-child investment),
which is a different estimand and does not answer the registered claim; that is the direction
Black-Devereux-Salvanes runs, and the registry cites it as evidence *about C.3.d*. And 344 already
showed only 61 of 4,690 family-size-shock records use C.3.d vocabulary at all.

**So the theory's own vocabulary does not index the studies that test the theory** — both tests are
named after their designs, not after Becker. A production query built from the C.3.d axis retrieves
the theoretical literature and misses the empirical one.

**Ruling 3 is answered and the answer is not "empty".** Channel controls returned 66 and 1,570, so
the detector works. The SBTC arm is 9 on a technology→return→fertility vocabulary and 24 on
demand-for-skill, but the same shock indexed as unified growth returns **85** and as a trade shock
**88**. Import-competition and China-shock papers estimating fertility effects are identified
designs on exactly this mechanism. 344's 3-and-5 would have been written up as an empty cell on one
vocabulary — `empty-cell-needs-second-channel`, again.

**What this fixes about the scope draft, which is the next task.** The production query needs at
least three axes and not one: the theory vocabulary (762), a **design** axis (twins, sibling sex
composition, schooling reforms), and a **shock** axis (trade/import competition, unified growth,
skill premium). Ruling 4's required-tags list is now derivable rather than guessed, and it has to
carry **direction** as a tag, because forward and backward are not poolable and the famous result is
in the arm that does not answer the claim.

**Two things NOT yet done, and neither should be assumed.** The forward-arm count of 8 is one
vocabulary; it needs its own second channel before any sentence calls the primary cell thin
(`a-thin-cell-may-be-an-unscreened-cell`). And the small vocabulary overlaps against the drafted
neighbours — C.2.f 9, C.2.b 12, D.2.d 0, C.3.f 11 — bound the shared **words**, not the shared
**estimand**: C.2.f found eight of its nine studies could not separate the return from the reference
standard, and found it at full text. Ruling 1 is not discharged by those numbers.

Scripts: `304` (ported), `344`, `345`. Logs: `candidate-frame-probe-2026-09-09.*`,
`c3d-term-diagnostics-2026-09-09.*`, `c3d-outcome-axis-2026-09-09.*`.

### 2026-09-09 (later) — second channel run first, then the scope drafted

**The forward arm's 8 was not allowed to become a sentence.** 345 measured the registered forward
estimand at 8 records and that was about to be the chapter's most consequential claim, on one
vocabulary. C.2.f wrote exactly that sentence into its scope §4 — "expect an empty or near-empty
primary cell" — and retracted it the same week. So `346` ran the second channel **before** the scope
was drafted rather than after.

**The forward arm is not empty. It is large, and it is elsewhere.** Channel 1 (economics-of-education
vocabulary) is 16 inside the frame and **231** unrestricted — 93% already outside. Channel 2 asked
for the *shocks* that move the return, each in its own local words, every control firing non-zero:
occupational structure 329, historical industrialization 275, schooling supply 188, trade 88,
technology 27, local labour demand 23. The channel-2 axis crossed with fertility is **770 records, of
which 15 are in the C.3.d frame and 8 in channel-1 vocabulary** — 98% invisible to both. Their
pairwise crossovers are 0, 0, 2, 11, 1, 3: `channels-must-fail-differently` is satisfied about as
strongly as it can be, so a null on both would have meant something. 35 carry an identified-design
marker.

**Walls measured from both sides**, since an overlap read from one side says only which frame is
bigger. Every vocabulary overlap is ≤8% of the frame: A.12 60, A.1 38, C.1.a 20, C.2.e 13, C.2.b 12,
C.3.f 11, C.2.f 9, compulsory schooling 6, D.2.d 0.

**Scope drafted: `literature/search-logs/quantity-quality-tradeoff-search-scope.md`.** Acceptance
criterion 2 met. What it freezes:

- **§2, the ruling that decides the chapter — DIRECTION.** Forward (return → fertility) is the
  primary cell; backward (family size → child outcomes) is mechanism evidence on link 2, never pooled
  and never a demsig numerator. The registry cites the backward literature as evidence about C.3.d.
- **§4** — a three-link conjunction whose middle link's best identification (twins) runs *against*
  the mechanism. Recorded as a prediction before searching.
- **§3** — three production axes (theory, design, shock), recall checked per axis. Ten candidate
  terms priced by marginal gain; none accepted until scored for gold.
- **§5** — demsig routes named per phenomenon. SDT: R2 elasticity gated on an R1 sign test expected
  to **split by country** rather than settle the cell as C.2.f's did. FDT: R1 first, with the
  conditions for computability stated now so stage 10 does not discover them.
- **§8** — ten walls. **Wall 2 (C.2.e) is new**: C.3.d owns the return to the *child's* human capital,
  C.2.e the *parent's*, and the largest forward row moves both. **Wall 5** separates A.12's
  twinning-as-exposure from C.3.d's twins-as-instrument.
- **§9–§12** — nine estimand cells, ten required tags led by `direction`, and a pooling rule that
  stratifies before counting.
- **§13** — five PI calls. Call 2 has a deadline: C.2.f's PI call 3 is answerable only while C.3.d is
  unstarted, and C.3.d is now started.

**`347` asserts all 75 figures quoted in the scope against the JSON the scripts wrote**, and was
verified to fire by mutating an expected value. A scope is prose and cannot be generated, but its
numbers can be tested, so re-running 344–346 now fails loudly if the prose goes stale.

**Not yet done.** No production query, no anchor resolved, no record screened. Stage 3 next: build
the three-axis query, resolve the Tier-A canon (Becker 1960, Becker–Lewis 1973, Becker–Tomes 1976,
Galor–Weil 2000, Galor–Moav 2002, Doepke 2004, Greenwood–Seshadri–Vandenbroucke 2005, plus
Black–Devereux–Salvanes 2005 and Angrist–Lavy–Schlosser 2010 on the backward arm), and harvest free
seeds from C.2.b, C.2.f, C.3.e, C.3.f, C.3.g, D.2.d and A.12.

Scripts: `344`, `345`, `346`, `347`. Scope: `quantity-quality-tradeoff-search-scope.md`.

### 2026-09-09 (stage 3 begun) — free seeds, anchors, and the seed set

**Free seeds: 515 records (`348`), after two measured corrections.** The first run kept 1,653 and
was wrong in a way worth recording, because the error was in the port's *design*, not in a word
list. `family-size instrument` returned 608 records (586 flagged A.12) and `skill shock` 457. A
**random** sample of what each caught alone was A.12's twin-obstetrics corpus (twin gestational
size, conjoined twins, twin speaker verification) and a trade-and-automation labour corpus with no
fertility or child outcome anywhere — about 1 of 12 and 0 of 12 usable.

The cause: those patterns came from the scope's **three-axis production query**, where the design
and shock axes are intersected with an outcome axis. Mining a neighbour's pool has no such
intersection, so they match the *donor's* corpus instead. `diagnostic-and-retrieval-vocabularies-differ`.

- **Fix 1, the two-tier keep rule.** Theory terms are self-sufficient; design and shock terms are
  half a record and must co-occur with a fertility or child outcome. 1,653 → 639. Audited at scale
  per `validate-fixes-at-scale`, reading **rejected as well as admitted**: 16 random admits on-topic,
  16 random refusals genuine half-records, no clear loss.
- **Fix 2, found by scoring the outcome list's own terms alone.** Bare `births?` admitted 124
  records at **0.8% precision** — A.12 twin epidemiology reaching the outcome tier through "twin
  births" — with one real C.3.d record among them. 639 → 515. `anchored-vocabulary-has-own-homonym`
  applies to the outcome list, not just the exposure axis.
- **Filter order.** With the half-record rule first, the soil/livestock counter fell from 12 to 0 —
  not because contamination had gone but because an earlier filter was eating it. DROP and SHADOW
  now run first (`dedup-before-counting-hides-redundant-rung`). Kept set identical; only the counter
  was lying.

**Anchors: 82/82 (`349` builds, `350` resolves).** 65 controls taken programmatically from 348,
stratified ≤6 per free-seed term; 17 hand Tier-A anchors split 8 THEORY / 5 BACKWARD / 4 FORWARD.
`control 65/65`, `hand 17/17` — **no ghost citations in the canon**, and the clean controls are what
makes that statement mean anything. 350 imports canonical `textnorm` with one documented wrapper for
TICK-082's HTML gap.

**Scope §2 is confirmed on the canon, not just on record counts.** Hand anchors only, so the counts
are comparable:

| direction | anchors | total cites | median |
|---|---|---|---|
| BACKWARD | 5 | **2,898** | 538 |
| FORWARD | 4 | **491** | 141 |

The backward arm carries roughly **six times** the citation weight of the registered forward
estimand. The field's identified empirical work on "the quantity-quality tradeoff" is overwhelmingly
the direction that does not answer the registry.

**Wall 2 is already visible and it lands on PI call 3.** Of the 26 resolved controls whose title
carries a fertility outcome, **5 name female or maternal education or earnings** — the *parent's*
return, which is C.2.e's estimand. Most arrived through the `schooling reform` seed term, scope §7
row 3, the largest forward row. **19% is a floor, not an estimate**: the count needs the parent named
in the title, and an "education and fertility" paper can be about maternal schooling without saying
so. PI call 3 is not hypothetical.

**Snowball seeds (`351`): 92 records from 82 anchors, and the version of record is the wrong seed
twice.** Seeding on versions of record alone reaches 10,843 citing works; the full version pairs
reach 11,848 (+9.3%).

- Galor & Moav 2002 — QJE article **1** cite vs SSRN preprint **93**
- Doepke 2004 — JEG article **11** vs SSRN preprint **145**

**This is not the QJE DOI migration**, though that shape is here too: Black-Devereux-Salvanes carries
`10.1162/…` at 1,051 alongside `10.1093/qje/…` at 446, and the twin gate caught it. A.12 documented
that case and wrote it "will recur in EVERY chapter that anchors on QJE and is therefore worth its
own note rather than a local fix" — it never got one, it recurred here, and **TICK-084 now opens it**.
The Galor-Moav shape is worse: `filter=doi:10.1093/qje/117.4.1133` returns *no* record, so there is
no twin to merge. OpenAlex's citation graph never attached to the published version.

**Next:** the three-axis production query (scope §3) and its calibration against these 82 anchors,
with recall checked **per axis**.

Scripts: `348`, `349`, `350`, `351`.

### 2026-09-09 (stage 3 cont.) — production query calibrated

**Five arms, union frame 2,926 records** (`352`). The outcome axis differs by direction per scope §2.

| arm | frame | recall of reachable | outcome axis |
|---|---|---|---|
| `theory` | 838 | 15/19 (79%) | fertility |
| `forward-shock` | 699 | 7/12 (58%) | fertility |
| `forward-design` | 500 | 6/6 (100%) | fertility |
| `backward` | 1,006 | 7/7 (100%) | child outcomes |
| `c2e-boundary` | 2,080 | — | **not screened** — Wall 2, C.2.e's chapter |

**Union recall on the Tier-A canon — the number that matters: BACKWARD 5/5, FORWARD 3/4, THEORY 3/8.**

**Three defects found, two of them mine.**

1. `PRIMARY_ARMS` holds *arm names*; anchors carry the `arm` values those arms **target**. On C.2.f
   the two vocabularies coincided and the ported expression worked by accident. Here it selected
   **zero** primary anchors, and the only reason it was caught is that it then divided by zero
   instead of printing a wrong percentage.
2. The ported gold filter is `a.get("outcome_is_fertility", True)`. `349` writes that field as
   `None` on all 65 controls, meaning *not known* — and `None` is falsy, so every control would have
   been silently dropped from the primary denominator. `optional-field-gate-disengages`.
3. **The reachability ceiling**, new here and worth porting back. A query is (exposure AND outcome),
   so an anchor the **outcome axis alone** cannot return can never be returned by the conjunction —
   counting it as a miss blames the query for a property of the anchor list. The controls were
   harvested on an *exposure* vocabulary, so many have no fertility outcome at all. The backward
   arm's raw 7/29 is **7/7 of what is reachable**. C.2.f set this by hand on 14 anchors; at 82 it has
   to be measured. The unreachable-reason report now consults the ceiling too — it had been
   relabelling structural zeros as vocabulary misses, the same defect one screen further down.

**One widening measured and reverted.** The ceiling showed the child-outcome axis could not reach two
of its own five Tier-A anchors, so I widened it — and priced properly, every candidate bought **zero**
canon recall (`+ "education"` cost +9,423 records for nothing). The gain the widening did show was
all *controls*, at ~1,600 records per anchor against a 400 ceiling; putting it in the **base** axis
rather than in `outcome_candidates` is what let it bypass the script's own acceptance rule. The two
anchors were never an axis problem: Rosenzweig-Wolpin and Angrist-Lavy-Schlosser say "quantity and
quality", not "family size", so they arrive through the **theory** axis — and the union reaches both.
`a-recall-miss-can-indict-the-anchors`: read the missed record before widening the query.

**THEORY 3/8 is expected and is not a query problem.** Becker 1960, Becker-Lewis 1973 and
Becker-Tomes 1976 are title-only records whose titles carry neither half of any conjunction. Scope §9
puts calibrated theory in a context-only cell; they are resolved as anchors (`350`) and are snowball
seeds (`351`), so the citation channel is their route **by design**. Recorded so it is not
rediscovered at stage 4.

**Next:** build the screen universe from the union query, then the screening rubric and depth probe.

Scripts: `352`. Log: `quantity-quality-tradeoff-production-query.{json,md}`.

### 2026-09-09 (stage 3–4) — universe, rubric, probe, and the forward-arm screen begun

**Screen universe: 3,254 records** (`353`), four arms paged to exhaustion, **no arm redundant**.
Anchors 41 present / 41 injected; free seeds 186 present / 289 injected / 40 unmatchable. 692 rows
(21%) are title-only — verified real, not a broken rung: an independent re-query of 40 randomly
sampled no-abstract records returned all 40 and **none** carries an abstract in OpenAlex.

The same two ported defects 352 hit were in this script too (`None`-is-falsy on the 65 controls;
arm *names* compared against anchor arm *values*), both fixed. Abstract enrichment now has **two
counters per rung** — the ported version returned one combined pair, so a rung that attempted 655
and filled 48 was indistinguishable from one never attempted.

**Rubric frozen** (`quantity-quality-tradeoff-screen-rubric.md`). Its first question is DIRECTION,
and it states plainly that the screen **routes** but does not adjudicate walls 1, 2 and 4.

**Depth probe, 150 records across 6 evenly spaced strata** (`354`, scored by `355`):

| stratum | n | primary | in scope | off-topic | fwd | back |
|---|---|---|---|---|---|---|
| 1 | 25 | **0** | 14 | 11 | 6 | 7 |
| 2 | 25 | 3 | 16 | 9 | 7 | 9 |
| 3 | 25 | 2 | 7 | 17 | 2 | 5 |
| 4 | 25 | 2 | 5 | 18 | 4 | 1 |
| 5 | 25 | 1 | 9 | 9 | 3 | 7 |
| 6 | 25 | **0** | 5 | 13 | 3 | 2 |

Primary 8/150 (5.3%), in scope 56/150 (37.3%).

**The most-cited stratum holds ZERO primary records.** Stratum 1 is Becker, Becker-Lewis, Galor-Weil,
Rosenzweig-Wolpin, Black-Devereux-Salvanes and Angrist-Lavy-Schlosser — theory and the backward
canon. Every primary record is in strata 2–5. **A front-to-back screen truncated at the head would
have found not one record of the registered forward estimand** and reported that as the finding.
The curve is also non-monotone (14, 16, 7, 5, 9, 5), so the remainder cannot be truncated.

**Sensitivity 10/10** on the withheld gold — BACKWARD 3/3, THEORY 4/4, UNKNOWN 3/3.

**And the blinded screen caught an error in my gold key.** It routed *"Genetics of twin birth rate in
German Holstein"* to OFF_TOPIC; that record was **in** the key, so it first scored as the run's only
miss. It is a dairy-cattle paper — the screen was right and the key was wrong. It reached the seed
table on "twin birth" + "birth rate" because `348`'s livestock filter had `dairy (cow|cattle)` but no
**breed name**. `blinded-screen-audits-the-anchors`, exactly as on A.23. The filter is widened and
verified by **executing** it against the whole 515-record seed table (removes this row, nothing
else); **not re-run here**, because `screen_id` is a universe position and re-running would
invalidate 150 hand-screened verdicts to remove one bad control.

**Forward-arm screen begun: 2 of 30 batches** (`356` bounds it rather than counting it).

| population | n | primary | rate | 95% CI |
|---|---|---|---|---|
| forward arms (target) | 80 | 6 | 7.5% | 3.5–15.4% |
| decoys (rest of universe) | 40 | 4 | 10.0% | 4.0–23.1% |

Projected primary in the forward arms: **41–182 of 1,184**.

**Wall 2 is the headline, and it is far bigger than the anchors implied.** Among records whose
exposure moves a *return* and whose outcome is *fertility*, **7 of 12 (58%)** are the **parent's**
return — C.2.e's estimand. `350` put the floor at 19% and said it was a floor. **PI call 3 now sizes
this chapter's primary cell rather than tidying its edges.**

Second reading, held loosely: the decoy rate is not lower than the target rate and the intervals
overlap almost entirely, so the forward arms are **not enriched** relative to the rest of the
universe. On 120 rows that is a flag to re-read, not a conclusion.

**Where this stops.** 28 batches (1,656 rows) of the same manual screening remain. That is bulk
labour, not a decision — and `screen-cost-is-not-the-constraint` says to cost a batched two-stage
LLM screen before treating it as a bottleneck.

Scripts: `353`, `354`, `355`, `356`. Rubric + probe score + prevalence logs beside them.
