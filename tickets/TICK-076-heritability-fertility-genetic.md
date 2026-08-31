# TICK-076: A.18 Genetic and Heritable Variation in Fertility
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `heritability-fertility-genetic` — HYPOTHESES-v5.md §A.18
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/heritability-fertility-genetic-*, extraction/heritability-fertility-genetic-*, output/chapters/heritability-fertility-genetic.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/heritability-fertility-genetic-search-scope.md` (2026-08-31). **FROZEN:** Rulings 1–4 resolved; 5 routed to TICK-001. Stage 3 unblocked.
- [x] 3. Literature search and AI screening, both phases (§5.1) — 696 distinct studies screened; stratum A complete, stratum B bounded, snowball rounds 1–2 done (§5.1 caps depth at 2)
- [ ] 4. RA title/abstract review
- [~] 5. Full-text retrieval — **56/148 (37.8%) usable full text**; 92 handed off (browser-job 87 / proxy-job 5). The earlier 73% counted bot-challenge pages as retrievals
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [~] 7. Extraction to `extraction/heritability-fertility-genetic.csv` — table generated, 6 rows verified from 4 chapter-critical studies, 52 pending second pass; RA 10% verification outstanding
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-08-31 (Shravan) — stage 2.** Scope memo drafted; 25/25 cold-start anchors resolved against
OpenAlex, no ghost citations (`245_a18_cold_start_anchors.py`).

Three things the scope work turned up that are not local to this chapter:

1. **A.18's primary estimand is a variance component, not an effect.** Heritability cannot enter a
   PROTOCOL §4.2.1 demographic-significance calculation — there is no numerator. Ruling 1 puts the
   demsig arm on the selection *response* (a mean shift) instead. A.9, the other non-effect entry in
   the master list, will need the same treatment.
2. **The registered SDT-only phenomenon drops the identified evidence.** The best-identified
   selection-response designs are historical parish pedigrees (Milot 2011, Courtiol 2012); the
   contemporary arm is UK Biobank and HRS, the weakest designs in the set. Ruling 2 asks to admit
   PM/FDT as evidence arms with SDT still carrying the verdict. Blocks the production query.
3. **The resolver defect is still shipping.** A script written today reproduced the OpenAlex `?`
   wildcard refusal *and* recorded it as an absence. Fixed here; belongs in the shared resolver
   alongside TICK-074, which is unmerged.

Next: PI answers on Rulings 2 and 4, then stage 3.

**2026-08-31 (Shravan) — Rulings 1–4 resolved, scope frozen, stage 3 unblocked.**

1. **Demsig arm.** FDT and SDT compute on the selection response R = h² × S. **A PM cell for h² is
   opened**, which reverses the draft's flat claim that heritability has no §4.2.1 numerator anywhere:
   PM's denominator is a *range*, not a change, so a variance share is the right kind of quantity for
   it. Contingent on a protocol answer about units (below). Carries a written caution: the PM share is
   near-definitional, will clear the 10% threshold on almost any twin estimate, and means far less
   there than "significant" means in any other chapter.
2. **Phenomena.** Three-phenomenon chapter, verdicts wherever the arithmetic exists. The halfway
   version first proposed — PM/FDT as evidence, SDT-only verdicts — would have left the
   best-identified designs in the literature permanently unable to move a verdict cell.
3. **`EDUCATION_PGS`.** PGS standard units primary; conversion to children per woman a labelled
   secondary with the r_g interval propagated.
4. **Fecundity traits.** `LINK_TRAIT` unless the same study links the trait to realized births.
5. **Master-list edit confirmed necessary** and drafted in §13 for TICK-001 — `phenomena` widens to
   PM/FDT/SDT, and the `claim` becomes three clauses matching the three arms, including the moderation
   finding the registered text omits.

**Two questions escalated to Anup as protocol-level, neither blocking:** whether PM's §4.2.1
denominator admits a within-population between-individual variance numerator (binds stage 10, and A.9
has the same problem), and the fact that GRADE §4.1 has no band for a non-effect estimand, so a
competent twin design scores "Very low: correlational only" (binds stage 11; proposed
`NOT RATEABLE — non-effect estimand`).

Next: stage 3 — build the frame from anchor provenance, then the production query.

**2026-08-31 (Shravan) — stage 3 begun: provenance pool and its diagnostics.**

`246` snowballed the 25 anchors backward and forward into a **3,140-record pool**, zero API errors.
Both rungs productive (backward 1,328 new, forward 2,032), so neither is redundant. All three Ruling-2
arms are reached with large exclusive sets — SELECTION 1,168 records reached by no other arm, H2 830,
THEORY 312, METHOD 196, H2_MOD 193 — so no arm is silently missing. Five seeds were forward-capped at
200 and are named in the log; their contribution is the high-citation head, not a sample.

`247` measured the homonym on two channels that fail differently. **Species contamination in the pool
is 1.6%** against roughly half the naive term space — the provenance-first decision, quantified.

Three things worth carrying off this chapter:

1. **The filter nearly deleted our own estimator canon.** Reading rejects rather than admits showed 59
   of the first run's 112 flags were the selection-methods literature the SELECTION arm is built on —
   Lande and Arnold 1983 among them, reached by five of our own seeds. Six method anchors added to §12
   as a result, and Rausher 1992 now supplies §10 threat 1 its formal statement.
2. **A patch that changed nothing looked like it worked.** Removing the offending subfield from the
   cloud list left all 59 flags in place, because a field-level fallback swept the parent field anyway.
   Caught only because the total barely moved. Right answer, wrong mechanism.
3. **The real wall is phenotype, not species** — the pool is behaviour genetics and sociogenomics, and
   its off-target mass is other phenotypes (education, cognition, psychiatric traits). **66% of records
   name no phenotype in the title**, so a title-only screen cannot enforce that wall. The screen runs
   on abstracts; silence goes to `INSUFFICIENT_INFO`, not to reject.

Re-ran `247` end to end: byte-identical output. Next: production query, calibrated against the pool.

**2026-08-31 (Shravan) — production query adopted.** `(GENETIC) AND (FERTILITY)`, frame 45,491,
84% anchor floor, **87.3% pool recall net of wall route-outs** (`248`–`250`, scope memo §15).

The first candidate scored 64% anchor recall and lost seven of nine SELECTION anchors. Cause: **in
the evolutionary-selection literature the fertility outcome is called `fitness`** — Kong, Beauchamp,
Byars, Sanjak and Milot measure selection on lifetime reproductive success without ever using the
word "fertility". Adding `fitness`, `twins` and `genotype` took anchor recall to 84%.

Two anchors (Byars 2009, Sanjak 2017) are unreachable by any boolean — their abstracts name no
fertility outcome at all — so **for the SELECTION arm the citation channel is co-equal with the
boolean channel, not a supplement**, and PRISMA must report the asymmetry per arm rather than one
pooled recall number.

The raw 59.8% pool figure was the gold's fault: of 37 misses, 13 are Wall 1 route-outs to A.19,
8 are Wall 3 route-outs to B.1, 8 have no genetic exposure, and only 8 are genuine A.18 candidates.
Classifications are title-keyed hypotheses for the RA gate.

Leave-one-out on every term: `parity` dropped (240,805 frame, zero anchors), `pedigree` dropped,
three stemming duplicates dropped; six zero-yield terms KEPT because each names a §5 enumerated
design at under 250 records of frame cost.

Next: pull the frame and run the §5.1 two-phase screen on abstracts (§6 — the phenotype wall is
title-invisible).

**2026-08-31 (Shravan) — frame pulled, prescreened, and the unscreened tail bounded.**

Frame pulled whole: **45,568 records** (`251`), 18.4% with no indexed abstract.

**PROTOCOL §5.1's saturation stopping rule fails here** (scope memo §16). Measured gold-recall curve:
at the 1,000-record stopping rule this chapter would capture **31.7%** of its known gold, and the
curve is still climbing at 26% of the frame. Escalated to Anup as protocol-level — the rule was
calibrated on the OAS pilot and never re-tested, and **every chapter that already used it has an
unmeasured recall problem rather than a clean PRISMA**. One relevance-ordered pull per chapter checks it.

Prescreen (`252`): only two of six candidate rules survive a gold recall check — non-human organism
(-25.0%) and no-fertility-outcome-in-abstract (-5.5%). Survivors **31,960**, gold 65/65. Title-only
screening would cut 62% but destroy 8 gold: the §6 title-invisibility claim, now measured.

The tempting reduction — keep only the 320 survivors the citation channel also reached, holding 64
of 65 gold — is **circular** and was refused: the gold is pool-derived, so that statistic is a
tautology.

Instead `253` sampled the tail blind, with 12 hidden gold controls. **Sensitivity 12/12 (100%)**;
tail prevalence **1/150 = 0.7%**, implying **≈210 relevant records (95% CI 37–1,164)** unscreened.
PRISMA reports that bound rather than claiming completeness.

Next: screen the citation-channel intersection (320) plus the boolean relevance head, and run
snowball round 2 from whatever the screen promotes.

**2026-08-31 (Shravan) — dedup correction.** Two of my own outputs disagreed (32,126 survivors as a
list vs 31,960 as a set of ids), which surfaced duplication in the pull: **236 repeated openalex ids**
plus **2,996 titles shared across distinct ids, 3,282 records** — one Figshare item deposited **159
times**. `254` collapses both, with **first-author agreement required** to merge a title cluster; 393
clusters were kept apart because it failed. An unreadable (fully non-Latin) author name folds to ""
and would have merged every such record together, so each gets a unique sentinel: an author we cannot
read must prevent a merge, not license one.

Corrected: frame **42,050 distinct works** (not 45,568), prescreen survivors **29,394** (not 32,126),
tail population **29,077**, tail prevalence **1/136**, unscreened estimate **213 (95% CI 37–1,176)**.
All prescreen conclusions hold — same two rules adopted, gold 65/65 retained, title-only still
destroys 8 gold. Raw frame dumps moved to `temp/a18/` and gitignored: the 75MB frame should never have
been committed.

**2026-08-31 (Shravan) — screen batches 1–3 (stratum A complete), 165 records.**

Yield **53.3%** in the citation-intersect stratum against **0.7%** in the boolean-only tail — a 76x
difference, and the quantitative case for building the frame from provenance.

Screen audited against 34 hidden gold records: **sensitivity 91.2%** (94.1% counting UNCERTAIN). Both
"misses" read back; one indicts the gold — *Partner + Children = Happiness?* has well-being as the
outcome and fertility as the exposure, so rejecting it is correct and it is gold only because the
proxy set was built on a title word.

63 primary-synthesis records so far: `H2_FERTILITY` 26, `SELECTION_DIFFERENTIAL` 22,
**`H2_MODERATION` 7**, **`PREDICTED_RESPONSE` 4**, `PEDIGREE_RESPONSE` 3, `WITHIN_VS_POPULATION` 1.

Two scope predictions now measured. **The moderation arm is real** (7 records) — the arm the
registered claim does not contain. And **the demsig-bearing cell is the thinnest**: Ruling 1 put
demographic significance on `PREDICTED_RESPONSE`, which has 4 records against H2's 26. The
well-evidenced half of the claim is the inert half.

Exposure distance: **only 9 of 88 RELEVANT measure a fertility-associated genotype**; 13 measure
selection on a correlated trait and 43 are anonymous twin variance. Ruling 3's conversion is doing
more work than any single study.

Next: batches 4–43 (stratum B).

**2026-08-31 (Shravan) — screen batches 4–7 plus positional depth probes; yield curve complete.**

Full yield curve across strata: **A 53.0%** (317 screened, 168 relevant, complete) · **B head 9.1%** ·
**B depth 3.3%** (probes at batches 14/24/34/43) · **C tail 0.7%**.

The depth probes are the point: batches 14–43 are almost entirely non-human evolutionary biology,
plant and livestock breeding, and the **cardiorespiratory-fitness homonym**. `fitness` took anchor
recall from 64% to 84% and also filled the tail with exercise physiology — the right trade, since
recall is unrecoverable and precision is not, but this is what it cost.

Stratum B holds an estimated 80–100 relevant records in ~1,880 unscreened, mostly METHOD/THEORY/
LINK_TRAIT. Not empty — batch 24 held *GWAS of Parity in Bangladeshi Women*, a real `H2_FERTILITY`
record — so it is bounded, not discarded.

**Recommendation: snowball round 2 from stratum A's 168 relevant records before screening the rest of
stratum B.** The citation channel out-yields the boolean channel 16x at the head and 53x in the tail;
many of the 168 were never seeds.

Metadata caution: `B34-10` carries an OpenAlex abstract about building climate-control systems
attached to a real fecundity-heritability paper. Extraction must read the record, not the index.

**2026-08-31 (Shravan) — snowball round 2 complete.** Seeded from the 168 screen positives. Reached
11,641; 4,399 new after prescreen and proper dedup; **substantive queue 2,524** with 1,875
method-only-reached records set aside. Zero API errors. **Priority-batch yield 67.3% relevant (32.7%
substantive)** against stratum B's 9.1% — seeding from screen positives beat reading more abstracts.

Two defects in my own script, both caught by reading the output. `256` deduped on openalex id only, so
Williams 1957 and Charlesworth appeared twice — `254` had already built title-cluster dedup with a
first-author gate for the frame and `256` did not reuse it. And **133 version pairs** (bioRxiv twins of
Beauchamp 2016, the schizophrenia MR, the postponement paper) were counted as new when they are the
same study already screened. Combined inflation 260 records, corrected by `258` before reporting.

**A seeding decision was wrong and is now measured.** The estimator canon (Lande & Arnold, Kingsolver,
Schluter, Kruuk) reached 2,234 records — the largest share — and a 16-vs-16 read put method-only-reached
material at ~2/16 adjacent against ~9/16 for thin-arm-reached. Snowball from records whose ESTIMAND
matches the hypothesis, not from the estimator canon: a methods paper is cited by every field that uses
the method. Right to add as anchors, wrong to use as seeds.

Round 2 fed the thin arms: 404 records reached only from thin-arm seeds, and batch 1 alone promoted five
new `PEDIGREE_RESPONSE` records (Saguenay inherited disorders, pre-industrial Sami, Finland demographic
transition) against round 1's three.

**2026-08-31 (Shravan) — screening consolidated; search stage closed.**

**696 distinct studies screened. 262 RELEVANT, 57 UNCERTAIN. 148 primary-cell studies**, plus 114
method/theory/LINK records that are not included studies.

`H2_FERTILITY` 66 · `SELECTION_DIFFERENTIAL` 45 · `PEDIGREE_RESPONSE` 16 · `H2_MODERATION` 13 ·
**`PREDICTED_RESPONSE` 6** · `WITHIN_VS_POPULATION` 2. Round 2 supplied 34 of the 148.

**Exposure distance is the chapter's sharpest structural finding: only 9 of 148 primary studies
(6.1%) measure a genotype associated with fertility itself.** 36 (24.3%) measure selection on a
correlated trait — education, psychiatric liability, cognition — and 102 (68.9%) decompose an
anonymous variance component naming no variant. Ruling 3's conversion is load-bearing for a quarter
of the evidence, not a footnote.

Wall 1: `decomposes` yes 141 / cannot_tell 7 / **no 0**.

**Synthesis expectation, recorded before extraction:** `PREDICTED_RESPONSE`, the only cell that can
carry a demsig number under Ruling 1, has 6 studies against H2's 66. The ≥3 pooling test applies AFTER
stratification, and 6 studies across different populations, generation lengths and genetic measures
may not survive it. Expect a computed point estimate reported narratively, not a meta-analytic pool.

Next: RA title/abstract review (stage 4) on the 57 UNCERTAIN plus a 10% sample of the 148, then
full-text retrieval.

**2026-08-31 (Shravan) — full-text retrieval: 108/148 (73.0%).** 40 outstanding, split into a
**browser job (35)** and a **proxy/ILL job (5)** — different work for different people, so the
handoff does not conflate them.

Routes, as *net new* retrievals: OA pdf 37 · publisher 32 · OA landing 30 · **PMC BioC 6** ·
unpaywall-retry 3. Note the PMC figure carefully: BioC **fetched 49 full texts**, but 43 were for
studies another route had already got, so it added 6 net. Both numbers are worth keeping — the 43
overlaps are an upgrade rather than waste, because BioC structured text extracts far more reliably
than a publisher PDF, and extraction should prefer it where both exist.

**The PMC rung was reported dead twice and was neither time empty.** First, OpenAlex populates
`ids.pmcid` for **0 of 148** records while carrying `ids.pmid` for 102 — the rung was unreachable by
the route used, not absent. Then the NCBI ID converter 301-redirected to a new host and my curl
lacked `-L`, so the redirect HTML parsed as "unparseable" and printed `pmcid_found: 0`. Then the
response returns `pmid` as an **integer** against string keys, so every match failed and it printed
zero a third time. Fixed: **52 PMCIDs found, 49 BioC full texts fetched** — a 94% fetch rate on the
rung that three separate defects had reported as dead.

**Unpaywall was found-143 / fetched-0 in `260` because I never followed the URLs** — the script
recorded the API attempt and `continue`d. Following them (262) yielded 13 OA URLs and 0 fetches, and
that zero IS genuine: 403 from SSRN and publisher CDNs, 429 from bioRxiv. The 429s are rate limits,
not blocks, and 3 of 4 recovered on backoff.

**Cell cross-tab, which the overall rate hides:** `SELECTION_DIFFERENTIAL` 80.0% · `PEDIGREE_RESPONSE`
75.0% · `H2_FERTILITY` 72.7% · `PREDICTED_RESPONSE` 66.7% (4/6) · **`H2_MODERATION` 53.8% (7/13)** ·
`WITHIN_VS_POPULATION` 50%. The moderation arm — the chapter's distinctive finding — remains the
worst-retrieved, and its outstanding records are at the front of the browser-job queue.

**2026-08-31 (Shravan) — CORRECTION: retrieval is 56/148 (37.8%), not 108/148 (73.0%).**

Converting every retrieved file to text (`264`) showed that **46 of the 108 "retrievals" are
bot-challenge pages** — Cloudflare *Client Challenge*, *Just a moment… Enable JavaScript and cookies*
— served with **HTTP 200** and enough raw markup to clear a byte threshold, stripping to 11–303
characters of text. A further 6 are abstract-only landing pages. HTTP 200 plus bytes is not a
retrieval; the only test that works is whether the text contains a paper. Those 46 are not paywalled
and not fetched — they are bot-blocked, and the browser-job queue was 43 records short.

Two further defects the text conversion exposed, both recovering real studies:
- **Four PDFs were saved with a `.html` extension** because `260` named files from the URL suffix
  rather than the content type, so the tag-stripper turned real full texts into binary garbage that
  scored 0.00 title overlap and was filed `WRONG_PAPER`. Sniffing `%PDF` magic bytes recovered all
  four — one of them in the thin `H2_MODERATION` arm.
- The title-match window of 6,000 chars missed titles sitting behind a cover page; it now falls back
  to the whole document before calling a file the wrong paper.

**The binding constraint is now explicit: `PREDICTED_RESPONSE` has 1 full text of 6 studies (16.7%)**
— and it is the only cell that can carry a demsig number under Ruling 1. Cell rates:
`WITHIN_VS_POPULATION` 50% · `SELECTION_DIFFERENTIAL` 46.7% · `PEDIGREE_RESPONSE` 43.8% ·
`H2_MODERATION` 38.5% · `H2_FERTILITY` 31.8% · **`PREDICTED_RESPONSE` 16.7%**.

The handoff is regenerated and ordered by cell, with the demsig arm at the front.

**2026-08-31 (Shravan) — extraction begun against the 56 full texts.**

`264` built the text corpus (BioC / PDF / HTML → text, with content verification), `266` harvested
candidate quantities, `267` generates `extraction/heritability-fertility-genetic.csv`. Every numeric
cell carries the **verbatim sentence it came from**, so the RA's 10% check verifies a claim against
its own source rather than against my transcription.

**The most consequential extraction result is a study that refutes its own headline estimate.**
Ísleifsson et al. (Iceland, national genealogy 1700–1920 + deCODE) reports narrow-sense **h² = 0.137
(SE 0.02)** for lifetime reproductive success from IBD-based REML on 8,456 full sibling pairs. Adding
a family effect and letting it compete with relatedness gives **f² = 0.129 (0.03) and a genetic effect
of 0.00 (0.05)** — and the authors conclude, in their own words, that "the heritability estimate
(h2 = 0.137) was based solely on shared family effects among full siblings and was not due to shared
genes." **Extracting the headline 0.137 would have recorded the opposite of what the study found.**
Both rows are carried with `estimate_superseded_by_authors` set. This is the largest pedigree design
in the chapter.

Other verified rows: **Tropf et al. mega-analysis** — h²_SNP for NEB **0.038 (SE 0.0097)** baseline,
rising **fivefold to 0.22 (SE 0.026)** once population and demographic cohort are modelled, which is
the §4 moderation claim quantified. **Within-family UK Biobank** — number of children **h² = 0.27
(SE 0.11)**, the assortative-mating- and stratification-robust estimate. **Quebec (Galor & Klemp)** —
time from marriage to first birth h² = 0.04.

**A defect in my own table, caught by row reconciliation.** I hand-typed the four `openalex` join keys
instead of resolving them from the corpus, and every one was wrong: the verified rows became orphans
and the pending count silently read 56 instead of 52. The ids are now resolved by title from the
corpus and the builder asserts that verified + pending reconciles against corpus size. A corrupted
join key in an extraction table is the quiet failure the match-by-content rule exists to stop, and it
appeared in the key column itself.

**2026-08-31 (Shravan) — extraction, second pass: table recovery and two reclassifications.**

**`PREDICTED_RESPONSE` has ZERO usable full texts, not one.** Its only retrieved text — Brandenburg
et al., *fertility transmission and coalescent trees* — is an individual-based **coalescent
simulation** whose outcomes are genealogy imbalance and effective population size. No empirical h², S
or R. It was screened in on title/abstract, and the full text refutes that: `design-is-not-a-property-
of-the-title`. **No demographic-significance number is computable from anything currently in hand.**
Also reclassified out: Sgrò & Hoffmann, a *Heredity* review of correlated selection response in
insects and plants, screened as `PEDIGREE_RESPONSE`.

**PMC BioC drops table bodies** — the rung that won this chapter's retrieval returns body text and no
tables, and heritability estimates live almost entirely in tables. On the Genotype × Cohort paper the
BioC text says "Table 1 reports the parameter estimates" and contains none of them. PMC's efetch XML
does carry `<table-wrap>`; `268` appends them, recovering tables for **28 studies**, all with numeric
values. BioC is excellent for screening and insufficient for extraction on its own.

**A second defect that hid the first: behaviour-genetics papers write coefficients without a leading
zero** — `.350 (.424)`, `.498 (.105)***`. A diagnostic anchored on `0\.` reports a table-rich paper as
numberless, which is exactly what mine did.

**The recovered table changed a substantive reading.** Briley et al.'s cohort-interaction term for
completed fertility is **−.032 (.014)\* under the spline specification and +.016 (.009)† under the
quartic — opposite signs in the same table.** Whether the heritability of completed fertility rises or
falls across the 1920–1955 cohorts is specification-dependent in this study. Both rows are carried as
`VERIFIED_SPECIFICATION_DISCORDANT`; taking either silently would report a direction the paper's own
alternative specification contradicts. This bears directly on §4's moderation claim.

Extraction now: 10 verified/reclassified rows, 49 pending.

**2026-08-31 (Shravan) — extraction pass 3: 16 rows resolved, 43 pending.**

Verified this pass: **Framingham** CEB h² = 0.09 (P = 0.03), AFB 0.18 · **Day et al.** SNP-h² for AFB
0.290 (SE 0.015), AFS 0.248 men / 0.242 women · **childlessness GREML** overall h² 0.455
(CI 0.341–0.569, N = 9,942; female 0.591, male 0.563) · **Tropf 2015** h²_SNP NEB 0.10 (SE 0.05), AFB
0.15 (SE 0.04) · **Brigos-Barrios et al.** h²_SNP reproductive success 0.03 (SE 0.0014).

**A version pair that title dedup structurally cannot catch.** *Why do we get sick? …* (medRxiv 2025)
and *Genetic trade-offs in fertility and longevity …* (Nat Ecol Evol 2026) are the same study, same
authors, same estimate — **retitled on publication**, so no title match exists. Both sat in the 148
primary studies; the preprint is now marked `DUPLICATE_OF_W7169878769_DO_NOT_POOL`. Every
preprint-bearing chapter in this review has the same exposure.

**`269` is a FAILED diagnostic and is marked as such in its own docstring.** I tried numeric
fingerprinting to find retitled pairs at scale: it scored **zero recall on the one pair known to be
real** — the preprint writes `1.4 × 10⁻³` where the published version formats it differently, so the
fingerprints never intersect — while emitting 18 false positives pairing plainly unrelated papers.
A diagnostic that scores 0 on its only known positive is not evidence about the corpus, and its
output must not be used. The confirmed pair is merged by hand; the general risk goes to the RA gate,
where a human comparing author lists and cohorts sees what a regex cannot.

