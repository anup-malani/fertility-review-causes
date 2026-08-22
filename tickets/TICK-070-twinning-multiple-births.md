# TICK-070: A.12 Twinning Rates and Multiple Births
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `twinning-multiple-births` — HYPOTHESES-v5.md §A.12
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/twinning-multiple-births-*, extraction/twinning-multiple-births-*, output/chapters/twinning-multiple-births.md

## Acceptance criteria
- [x] 2. Search strategy and scope **FROZEN** — `literature/search-logs/twinning-multiple-births-search-scope.md` (drafted 2026-08-20, frozen 2026-08-22). 9 walls, 10 estimand cells. Call 3 decided (split at the margin); calls 1 and 5 adopted as recommended, RA-provisional; calls 2 and 4 open by design and answered during the run.
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [x] 4. RA title/abstract review — D2 complete, 1,376 records, 23 batches (2026-08-22)
- [x] 5. Full-text retrieval — **68 of 253 readable (27%)**; 185 on the library list, banded (2026-08-22)
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/twinning-multiple-births.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [x] 12. Chapter draft on the §6 template — `output/chapters/twinning-multiple-births.md` (2026-08-22), written on 68 readables
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-20 — reconnaissance and scope draft
Pre-scope recon run (`source/build/goldset/160_a12_recon_probe.py`, 63 requests, 0 failed);
report at `literature/search-logs/twinning-multiple-births-recon-probe.md`.

Three findings that set the shape of the chapter:
- **The primary cell is populated by vital-statistics reports, not estimation studies** (n=25, n=93;
  heads are *Births: Final Data for 2013* and *Annual Summary of Vital Statistics*). Correct for an
  accounting identity. The estimable parameter is the *offset* — whether a twin birth displaces
  subsequent fertility — and it has been estimated by name three times (Alter & Hacker 2024
  *Demography*; Robson & Smith 2012 *Proc R Soc B*; Clark, Cummins & Curtis 2020 *Demography*).
- **v5's ART clause is time-inverted.** eSET cut ART multiple-birth rates from the early 2000s;
  the literature already calls the shape a peak (Monden, Smits & Pison 2021, *Twin Peaks*). v5
  describes a monotone offset over a period that has closed.
- **Two of four decoy families are pure homonyms, not boundary cases** — crystallographic twinning
  (SHELX, 87,676 cites) and TWIP steel / digital twin — and are separable lexically. The
  behaviour-genetics cloud (A.18) is a real boundary case and is routed, not excluded.

Script numbered 160 against the cross-branch high-water mark of 159; `main` alone would have said 89
and collided with five live branches.

### 2026-08-22 — Call 3 decided, walls frozen

**Call 3 ruled: split at the margin.** `ART live births = D_ART x (1 + m_ART)`; A.17 owns the
deliveries, A.12 owns the multiplier. Additively separable, so both chapters can report a
contribution without double-counting. Ruled with an explicit caveat, which the chapter carries to its
verdict: **the intensive margin is not identified.** `m_ART` is chosen rather than assigned, it is
jointly determined with `D_ART` (eSET raises cycles per live birth, hence cost per birth, hence `D`),
and the counterfactual "TFR without ART multiples" is not a ceteris-paribus perturbation of `m`.
`SECONDARY_ART_MULTIPLES` therefore yields a measured *share*, not an estimated effect, and is
GRADE-downgraded for indirectness on identification grounds independently of the sign problem.

**The ruling forced a wall re-cut, and the drafted version would have been self-defeating.** Wall 6
hard-excluded "clinical ART practice (transfer protocols, success rates)". Under the split that
discards the eSET policy literature — the only quasi-experimental variation in `m_ART` there is, and
the one Pison, Monden and Smits name as the cause of the post-2000 reversal. Wall 6 is now cut on
**outcome, not treatment**: population multiple-birth-rate outcomes are included, per-cycle clinical
outcomes excluded. Still enforceable at title/abstract, because abstracts name their outcomes.

**A second finding from the same live check: the twinning rise is partly endogenous to the
phenomenon it is claimed to offset.** Pison, Monden and Smits (2015) decompose the developed-country
rise into delayed childbearing and MAR, with MAR about **three times** the age effect. The remaining
quarter is the maternal-age composition shift — i.e. postponement, which is the very SDT mechanism
v5 says twinning offsets. That component is a feedback of the decline, not a force against it, and
only the MAR component is even a candidate offset. Split at extraction.

**Order of magnitude, live and provisional.** Monden, Smits and Pison (2021): global twin delivery
rate 9.1 -> 12.0 per 1,000 deliveries between 1980-85 and 2010-15, so births per delivery moved
~1.0091 -> ~1.0120, a rise of about **0.29% over four decades** — before the stopping offset and
before netting the endogenous age component. Global figure; stage 10 recomputes on the
developed-country HMBD series. Recorded pre-screen so that an apparently large A.12 effect gets
audited rather than believed.

Calls 1 and 5 adopted as recommended and marked RA-provisional. Call 5 is made free to reverse by
**pulling and tagging** the cross-population PM cluster as `SECONDARY_PM_VARIATION` instead of
excluding it, so an overturn costs a re-screen and never a re-search.

Next: A3 cold-start anchor resolution (script 161).

### 2026-08-22 — A3 cold-start anchors (script 161)

25 candidate anchors, **22 verified live, 3 expected index misses, 0 failures, 0 flagged.** Report at
`literature/search-logs/twinning-multiple-births-cold-start-anchors-log.md`. Cells: 8 `PRIMARY_*`
(3 stopping-offset + 5 twin-IV first-stage), 5 `SECONDARY_ART_MULTIPLES`, 5 `EXPOSURE_SERIES`,
1 `SECONDARY_PM_VARIATION`, 5 routing decoys, one per enforceable wall.

**All three of v5's seminal citations for A.12 are defective, and the third is a trap.** Bulmer 1970
resolves but drags five review records. Pison & D'Addato 2006 has the wrong title in v5 (*in
Developed Countries*, not *among the world populations*) and duplicate DOIs. Hoekstra "2008" is
**2007** — `10.1093/humupd/dmm036`, 203 cites — and a real Hoekstra *2008* paper exists (*Body
composition, smoking, and spontaneous dizygotic twinning*, F&S, 50 cites), so trusting v5's year
lands on a different paper by the same first author and reports success.

**Both predicted duplicate catches fired**, 4 records demoted across 2 anchors: Pison & D'Addato
(98/66) and Black, Devereux & Salvanes (1,049/446). **The BDS case is the QJE MIT-Press-to-OUP DOI
migration and generalises** — any chapter anchoring on a pre-migration QJE article meets a split
citation count. Belongs in the shared resolver, not in per-chapter rediscovery.

**Book-canon gate: five review records on Bulmer, only one typed `book-review`.** The gate refuses
three as `review_of_the_work` (Shields in J. Med. Genet., typed `journal-article`; Benirschke in
Teratology; and a **Science** review the sourcing pass missed); the title gate catches two more that
embed the author name. A type-based rule would recover one in five.

**A gate keyed off an optional field disengaged invisibly on the first pass — the finding worth
keeping from this run.** Bulmer was entered with `expect_no_doi=True` but without `is_book=True`, so
the book gate no-opped and the ordinary author gate refused the anchor as `authors_disagree`. The
counters looked right and nothing appeared broken: a right answer by a mechanism that does not
generalise. With the flag set, the reason becomes `review_of_the_work` and three reviews are found
where one was. **Audited across branches rather than assumed** — D.2.d (103), D.1.b (95) and D.3.c
(148) all set the flag, B.1 (64) and D.3.b (72) predate the gate, so no prior chapter is affected.

Two absences established rather than inferred from failures (per the refusals-are-not-zeros rule):
Bronars & Grogger 1994 and Martin et al. 2012 have no DOI in either index — the latter confirmed by
Crossref returning only later NCHS reports under the `10.15620/cdc:` prefix minted after 2012.

One serendipitous on-topic find carried to A4 rather than discarded as a refusal:
`10.2139/ssrn.5258235`, *Does the One-Child Policy Increase Man-Made Twinning Rate?* — policy-induced
twinning, surfaced by no reconnaissance probe.

Next: A4 citation frame (Tier A/B), script 162.

### 2026-08-22 — A4 Tier A/B citation frame (script 162)

**25 Tier A seeds, Tier B 8,701 deduplicated records, 0 failed requests.** 1,029 records found by
more than one seed; 63% carry an abstract. Report at
`literature/search-logs/twinning-multiple-births-tier-ab-log.md`.

**Wall 8's cost is now a number, not a sentence.** The recall denominator is reported two ways:
**9 empirical anchors** (both offset cells — both estimate the estimand) against **3 screenable
anchors** (`PRIMARY_OFFSET_STOPPING` alone). Recall(A) against 9 will look poor by construction
because Wall 8 says twin-IV first stages are unreachable at title/abstract; against 3 it measures the
screen. Both get reported, and the gap is the price of the unenforceable wall.

**The homonym carve-out is confirmed on exact counts rather than a sample.** Rather than pull SHELX's
87,673-record cloud to prove crystallography is not about fertility, each homonym seed carries a
capped pull (for Tier B) plus an EXACT on-topic rate from two count-only queries. SHELX: **13 of
87,673 = 0.0%**. TWIP steel: **0 of 1,810 = 0.0%**. The scope's one carve-out from the
forward-seed-everything rule now rests on a measurement that carries no sampling bias. TWIP is the
clean demonstration of lexical separability — `twin` fires at 30% (TWinning-Induced Plasticity) while
`fert` fires at 0%.

**Wall 3 is enforceable: the dairy seed's cloud is 90% detectable as non-human**, even though `fert`
reads 35% because bare "fertility" means bovine fertility there. The two diagnostics together do the
work that neither does alone.

**Wall 6's re-cut looks enforceable, with one honest caveat.** `clin` separates the clinical cluster
(Thurin 61%, McLernon 53%, Helmerhorst 54%) from the twin-IV canon (0.4-2.2%) and the demography
seeds (13-25%) very cleanly, so outcome type IS visible at title/abstract. **But the INCLUDE-side
anchor Reynolds 2003 also runs `clin` 51%** — so neighbourhood clinical density does not separate
include from exclude. The discriminator is the individual paper's outcome, exactly as the wall is
written, and the screen must not be allowed to shortcut it with a cloud-level prior.

**A.18's cloud is thinner than "boundary case" suggested.** `OFF_TWINDESIGN` (Tropf 2017) runs
`fert` 8.8%, `twin` 7.1%, `BOTH` 1.1% — against the standing decoy-cloud guidance's 29-88% on-topic
range. Routing is unchanged (route, never exclude), but the A.12/A.18 boundary is thin, not busy.

**Two silent defects in the inherited A4 code, found by running it.**

1. **`_fold()` shattered names into characters** — `" ".join(c for c in x ...)` joins CHARACTERS, so
   "Wilson" became "w i l s o n" and `_surname()` returned the last LETTER. The first-author gate was
   comparing final letters and matched any two names ending the same. Audited across every branch:
   the machinery was introduced at D.3.c (`150`) and **A.12 is its only other user**, so no other
   chapter is affected. **But D.3.c's A4 log claims first-author disagreement is what refused
   Johnston & Lordan on the Wilson probe, and its code could not have done that.** A live check finds
   no such record in the citation head (Wilson's own records rank 1st, 2nd, 6th) and the only
   bookish-typed record carries no authors — so the refusal came from the type filter and an empty
   author list. **Flagged for D.3.c re-audit; deliberately not edited here.**
2. **A comma in an OpenAlex FILTER value is fatal, and percent-encoding does not save it** — the edge
   splits filters on commas after decoding, so `%2C` is undone before the split. It killed the
   Martin, Hamilton & Osterman 2012 recovery on the first run. Per the refusals-are-not-zeros rule
   that is UNCONFIRMED, not an unrecoverable anchor, so it was retried rather than recorded. A3
   (`161`) is unaffected — it queries through `search=`, where commas are ordinary.

**DOI-less seed recovery generalised beyond monographs, and it mattered.** The inherited code
recovered only `is_book` anchors. A.12 has three DOI-less anchors and only one is a book. Recovering
the other two added **Bronars & Grogger 1994** (370 forward records, `BOTH` 12.4%) — a twin-IV canon
seed and, under Wall 8, the only reachable channel to `PRIMARY_OFFSET_FIRSTSTAGE` — and **Martin et
al. 2012** (329 forward, `BOTH` 19.1%). Under the inherited code both would have vanished silently.

Next: D1 rank and screening cutoff (script 163).

### 2026-08-22 — D1 deterministic rank and screening cutoff (script 163)

Frame in 8,701; **359 version duplicates collapsed** on normalized title, leaving 8,342 scored.
**Worklist out: 1,376** — 800 budget slice + 40 orthogonal + **212 Wall 8** + 324 both-axes bypasses.
6,966 records go unread, of which 2,064 depend on a homonym seed alone. Nothing is deleted; every
record keeps score, rank and hit lists so the cutoff can be re-cut without re-running retrieval.

**A.12's two axes are anti-correlated, so neither is up-weighted.** Every prior chapter had a
near-universal exposure axis and a scarce outcome axis, and up-weighted the scarce one. Here the
twin-IV half of the frame carries fertility vocabulary WITHOUT twinning vocabulary (Black-Devereux-
Salvanes: twin 6.0%, fert 32.1%) and the demography half carries twinning without a population
fertility quantity (Pison & D'Addato: twin 84.0%, fert 47.0%). Up-weighting either axis would
systematically demote half the chapter, so both carry equal weight and the cross-axis AND does the
discriminating. Head of the ranking is clean — the top 25 is twinning-rate series and two twin-IV
methods papers, and **zero homonym-hit records appear in the top 200**.

**Wall 8 is now a measured quantity, and measuring it fixed a self-defeating bypass.** Of **1,991
records reached from a twin-IV canon seed, only 154 mention a twinning term at all — 92% of this
chapter's identification neighbourhood is invisible to axis 1.** The first version of the Wall 8
bypass required a twinning term alongside the design vocabulary and recovered **4** records; that was
the condition being self-defeating, not the population being small. Requiring a twinning term to find
the Wall 8 population re-imposes exactly the visibility assumption the wall denies. Re-gated on seed
provenance plus two independent design terms and no twinning term, it recovers **212**, and a sample
confirms the shape: quantity-quality, family-size and birth-order papers, none mentioning twins.

Caveat recorded rather than papered over: the bypass admits family-size-IV papers **generally**, not
twin-IV specifically — the instrument is often unnamed in an abstract too, so one-child-policy and
sibling-sex-composition designs come in beside twin designs. Deliberate. Admitting a same-shaped
design that turns out not to use twins costs one screen read; excluding it costs a record no later
stage can recover.

**The clinical penalty is deliberately mild and the homonym penalty deliberately heavy, both on
measured grounds.** A term sieve cannot make Wall 6's outcome-based call — an included and an
excluded transfer-protocol study both say "embryo transfer" — and A4 put the include-side anchor
(Reynolds 2003, clin 50.8%) almost level with the exclude-side one (Thurin, 60.6%), so a heavy
clinical penalty would demote the ART-multiples records Call 3 ruled this chapter owns. The homonym
penalty is the heaviest in any chapter because it is the best evidenced: A4 counted rather than
sampled, SHELX 13 of 87,673 and TWIP 0 of 1,810.

**All 952 both-axes records are in the worklist (100%).** B.6's lesson applies with extra force here:
A.12's headline verdict is a bounded NEGATIVE, and a negative reached by not reading is not a
finding.

Next: D2 semantic screen batches over the 1,376-record worklist (script 164).

### 2026-08-22 — D2 title/abstract screen complete (scripts 164, 165)

**1,376 records screened across 23 batches. 441 RELEVANT · 225 UNCERTAIN · 710 NOT_RELEVANT.**
Coverage is asserted rather than assumed — every worklist record carries exactly one verdict and
every verdict id is in the worklist. The check earned its keep immediately, catching a phantom id I
introduced by a single-digit typo.

**THE PRIMARY CELL IS FOUR TIMES THE ANCHOR SET, AND ITS MEMBERS DISAGREE.** The frozen scope named
three stopping-offset studies. The screen finds **14**, and the additions are not marginal: a
published comment on Robson & Smith in the same journal; a *Nature Communications* study finding the
OPPOSITE sign in pre-industrial Europe; Swedish register childbearing patterns for mothers of twins;
19th-century Dutch maternal life histories; a *JPE* paper whose outcome is time to next birth; and
the Gambian natural-fertility fitness study. This is [[tier-a-anchors-are-studies]] again — reporting
the anchor set as the evidence base would have understated the cell fourfold AND concealed that it is
contested.

**The mechanical arm overstates, for four independent reasons the identity does not carry.** All run
the same direction, and this is structurally the B.5 `(1-p)` error in a new chapter:
1. **Differential twin mortality** — twins are ~2.4% of births but ~12% of neonatal deaths in LDCs.
2. **The vanishing twin** — SEVEN records; conceived multiples exceed delivered multiples. And
   W2096430031 shows the correction is not even constant: SET pregnancies "practically lack vanishing
   twins", so eSET changes the conceived-to-delivered gap itself.
3. **Twin infanticide / cultural suppression** — bites hardest on the PM arm.
4. **The intergenerational channel** — a male co-twin reduces the female co-twin's later fertility
   (PNAS 2007 AND 2019; disputed by an Aberdeen null). **The scope has no cell for this. PI call.**

**The ART arm is not the clean story v5 tells.** eSET has a counter-channel: two independent
meta-analyses find ART raises MONOZYGOTIC twinning, which transferring one embryo does not close. A
further meta-analysis finds SET reduces live birth rates, and an NEJM trial puts the cumulative cost
at 43.9% vs 51.1%. And ovulation induction OUTSIDE IVF causes 40-70% of high-order multiples, a
channel eSET does not touch at all — which bounds what transfer policy can explain.

**Wall 6 verdict: enforceable, but only per-paper.** The screen's independent `outcome_type` agrees
with D1's clinical term-hits on **85.0%** of records. Of 149 `SECONDARY_ART_MULTIPLES` records, 49
carry a population/registry outcome (include side) and 100 a per-cycle clinical outcome — the genuine
seam. The wall holds because a human read each abstract's outcome; every cloud-level or term-level
shortcut fails, exactly as A4 predicted from Reynolds (50.8%) sitting level with Thurin (60.6%).

**Bypass yields, and one of them barely earned its place:**

| bypass | n | survived | yield |
|---|---|---|---|
| budget_top | 800 | 492 | 61.5% |
| **Wall 8** | 212 | 93 | **43.9%** |
| both-axes | 324 | 79 | 24.4% |
| orthogonal (inherited) | 40 | 2 | **5.0%** |

The chapter-specific Wall 8 bypass returned 44%; the INHERITED orthogonal bypass returned 5%. On this
chapter the inherited bypass was nearly dead weight and the re-gated one carried the recall — worth
recording, because the inherited bypass has been carried forward unexamined since B.5.

**A homonym family the scope never enumerated: PHOTOPHYSICS.** Five records where "singlet" and
"TRIPLET" are excited-state terms (OLED emitters in *Science*, Cu(I) and Re(I) complexes). No
reconnaissance probe found it, and D1's `TWIN_CORE` scores "triplet" at 5. Cheap to reject, but
Wall 2 should name it before the next run.

**Two junk record classes:** PeerJ peer-review objects (nine for one paper, carrying the reviewed
paper's abstract so no term sieve can separate them) and one CORRUPTED record whose title and
abstract belong to different papers.

Next: stage 5 full-text retrieval, prioritised on the 14 stopping-offset records and the four dense
first-stage entry points (Oxford handbook on twins methods in economics; Rosenzweig & Wolpin's JEL
review; the J. Economic Surveys review; the twins-data methods paper).

### 2026-08-22 — stage 5 retrieval (scripts 166, 167, 168, 169)

**68 of 253 wantlist records readable (27%). 185 need a human with a library proxy.** The wantlist
was selected by RULE from the screen output — not by hand — so it re-runs identically if the screen
is revised.

**A.12 IS RETRIEVAL-BOUND AFTER ALL, AND THE STANDING NOTE ON THIS CHAPTER NEEDS CORRECTING.** A.12
was picked as the fastest remaining hypothesis because stage 10 runs on the public HMBD rather than on
PDFs behind a proxy. That is still true — the demographic-significance computation is unaffected. But
stage 7, extraction of the *offset* parameter, is bound exactly as B.1 was, and worse in the place it
hurts most: **only 6 of the 14 causal-spine records are readable.** The cell that earns this chapter's
GRADE credit, and whose members disagree with each other, sits at 43% coverage.

**The four JOB B1 methods entry points are ALL still missing, and none was ever open.** They are the
only efficient route into 223 first-stage candidates that Wall 8 makes invisible to screening. Four
PDFs are worth more here than forty anywhere else on the list, and they are P1 on the procurement
list for that reason.

**The retrieval funnel, stated so the loss is visible at each step:**

| step | n | note |
|---|---|---|
| wantlist | 253 | selected by rule from 1,376 screened |
| OpenAlex says open | 142 | 56% |
| fetched on the first pass | 54 | 38% of the nominally-open |
| recovered by rung 2 | +14 | 9 alternate locations, 5 `citation_pdf_url` meta tags |
| **readable** | **68** | **27% of the wantlist** |

**84 of the 88 first-pass failures were HTML interstitials** — a 200 status returning a landing page
instead of a PDF. Per the standing discipline those are BLOCKED ROUTES, not closed papers, which is
why a recovery rung followed rather than a "not obtainable" bucket. The rung recovered 14.

**Rung yields, recorded so the next chapter can order them by evidence rather than guess:**
alternate OA locations 9, `citation_pdf_url` scrape 5, **PMC efetch 0**. B.6 built its recovery rung
around PMC; on A.12's literature PMC returned nothing and the cheap `locations` sweep did the work.
Rung order is chapter-dependent and should be measured, not inherited.

**The procurement list is BANDED, and the banding is the product.** A flat list of 185 DOIs gets
worked from the top and abandoned in the middle, which selects the evidence base by alphabetical
accident. Bands: P0 causal spine (8) · P1 methods entry points (4) · P2 identity corrections (11) ·
P3 ART-arm magnitude (52) · P4 residual (110). A partial run is expected; the instruction is to state
the band reached, so the chapter can say exactly what it read and what it did not.

**Deliberately not retrieved, and reported rather than dropped:** 145 first-stage candidates carrying
the IV-design vocabulary but no twinning term (the honest cost of the Wall 8 bypass's breadth — the
first-stage synthesis must say it did not read them); 82 routine per-cycle ART records; 182
country-year twinning tabulations whose numbers come from the HMBD harmonised.

Next: stage 6/7 — full-text screen and extraction on the 68 readable records, starting with the 6
readable causal-spine studies, while the P0/P1 bands are procured.

### 2026-08-22 — chapter drafted on the 68 readables

`output/chapters/twinning-multiple-births.md`, 5,300 words, PROTOCOL §6 structure. Written to a
brief from Shravan: **lay comparison before technical comparison, and an audience of a UChicago
undergraduate who knows economics but not demography.** Both shaped the structure rather than the
prose. §1.1, §6.1 and §7 each open with a plain-language reading before the technical one; the
organising analogy is a factory whose output is orders times units-per-order, and the mechanism is
framed on the extensive/intensive margin distinction and on target-family-size as an income effect,
which that reader already has. TFR, parity, completed fertility, DZ/MZ, replacement, eSET, ART, GRADE
and the PM/FDT/SDT phenomena are each glossed at first use.

**THE CENTRAL RESULT.** Rickard et al. 2022 (*Nature Communications*, >20,000 pre-industrial European
mothers) shows the entire prior literature rests on an **ecological fallacy**: comparing mothers who
ever had twins with those who never did compares high-fertility with low-fertility women by
construction, because exposure to the risk of twinning accumulates with births. Controlling for
exposure REVERSES the sign — higher twinning propensity gives fewer births (odds × 0.967, CI
0.952–0.983 per additional birth) — and identifies the mechanism as stopping after a twin birth.

Four of the six readable primary studies (Sear 2001 Gambia, Ekamper & van Poppel 2021 Netherlands,
Hur et al. 2024 Nigeria, Hoekstra et al. 2008 Netherlands) use the naive estimator and all four find
twin mothers more fertile. The disagreement is therefore RESOLVED rather than averaged: one unbiased
estimator against four biased ones, with the bias direction demonstrated.

**The offset, quantified from their simulation and re-derived in logs:** mechanical +14.78%,
behavioural −1.66%, net +12.83%. **The offset absorbs ~12% of the mechanical gain; ~88% passes
through.** One simulation, one sample, stated as an order of magnitude.

**Verdicts.** PM **negligible** (max 4.2% multiplier spread across the entire human record — Yoruba
45–50/1000 vs historical East Asia ~6/1000 — which is ~6% of the PM range at the most extreme
comparison available). FDT **not assessed** (out of scope; sign would be negative). SDT **small,
transient, wrong sign now**: ~2% of the Czech decline at its own peak, and five independent national
series show the reversal (Sweden IVF twinning 29%→18.5%; Japan iatrogenic 11.4→8.1 per 1,000; Czechia
>21→falling after the 2012 eSET rule; Iceland PR 0.74; **US twin share of ART infants 38.0%→~21% in
four years**).

**GRADE: PM HIGH for a negligible effect; SDT LOW**, downgraded for indirectness (the intensive
margin is not identified), imprecision (one offset estimate) and risk of bias in the body as a whole.

**A new citation-hygiene finding while verifying authorship.** v5's "Hoekstra et al. 2008" is wrong —
the review is 2007 — and there are **TWO** distinct Hoekstra 2008 papers a resolver can land on
instead, both legitimate and both on this exact topic. A wrong year pointing at two real neighbouring
papers by the same first author is worse than one pointing at nothing, because the resolver reports
success. Three author attributions in the draft were also wrong on first write and corrected against
the PDFs.

**The chapter states its own limitation prominently rather than in a footnote.** It is written on 27%
of wanted evidence with the primary cell at 6 of 14, and the Provenance block records that synthesis
proceeded over an explicit RA objection — Rickard et al. carries §6 almost alone, and the two studies
most likely to contest it (Robson & Smith 2012, which it targets; Alter & Hacker 2024, the only study
designed squarely on the estimand) are both unread. It also separates what would survive full
retrieval (the mechanical bound, the post-2010 reversal) from what might not (the offset magnitude).

Next: stage 13 RA lay-readability check, then PI review. Five PI calls stand, including the
unenumerated intergenerational cell and whether the identity should be computed on surviving children.
