# Search scope — genetic and heritable variation in fertility

**Hypothesis:** A.18 (HYPOTHESES-v5.md)
**Hypothesis slug:** `heritability-fertility-genetic`
**Ticket:** TICK-076
**Target phenomenon:** SDT (as registered). **§4 argues the registered phenomenon is wrong and asks
for a ruling.**
**Status:** DRAFT (Shravan, 2026-08-31) — walls, estimand cells and the demsig computation proposed,
**not frozen.** Five rulings below are marked *PI decision required*; Rulings 1 and 2 are load-bearing
for the query and cannot be deferred past stage 3. Anchors are resolved (§12); the frame is not yet
measured.

---

## 1. The claim

A.18 as registered says two things joined by "and":

> Heritable variation in fertility-related traits explains a portion of between-individual fertility
> differences **and** may produce a partial fertility rebound over generations as selection favors
> high-fertility genotypes.

The first conjunct is a variance decomposition: of the differences between people in how many children
they have, some fraction tracks genotype. The second is a projection about the mean: because fertility
is heritable and people differ in fertility, selection acts, the population's mean genetic propensity
to reproduce rises, and fertility partially recovers on its own.

These are not two statements about one quantity. They are statements about different moments of the
distribution, they are estimated by different literatures using different data, and — this is the
chapter's organizing problem — **only the second one is a claim about fertility decline at all.**

## 2. What makes this chapter different in kind: the primary estimand is not an effect

Every chapter written so far estimates a treatment effect: a change in an exposure produces a change in
births, and demographic significance asks how much of the observed decline that change accounts for
(PROTOCOL §4.2.1). A.18's first conjunct has no such structure. Heritability is a ratio of variance
components within a population at a point in time. There is no counterfactual in which the genotype is
withdrawn, no dose, and no sign. A population can have h² = 0.4 for completed fertility with a TFR of
6 or a TFR of 1.3; h² is silent about which.

It follows that **a heritability estimate cannot enter a demographic-significance calculation**, and
the numerator PROTOCOL §4.2.1 requires does not exist for it. This is not a reason to exclude the h²
literature — it is the evidentiary basis for the second conjunct, and the chapter needs it — but it
fixes what that literature is *for*.

> **Ruling 1 — the demsig arm is computed on the selection response, never on h². (Shravan,
> 2026-08-31; PI decision required.)**
> h² studies are evidence for a **precondition** of the rebound claim and are reported as such. The
> only quantity that can carry a demographic-significance number is a **shift in the mean** — the
> per-generation response to selection. Concretely, §11 pre-specifies R = h² × S and scales it against
> the §4.2.1 denominator. A chapter that pooled h² and reported "genes explain 30% of fertility
> variation" against a denominator of observed TFR decline would be committing a category error in the
> review's own headline units, and it is the error a reader is most likely to make on this chapter's
> behalf if the chapter does not pre-empt it.

The A.9 precedent (`population-age-structure-momentum`, still unwritten) is the neighbouring case: an
entry whose content is an accounting identity rather than a causal effect. A.18 is the variance-
decomposition version of the same shape. Whatever is settled here should be reused there.

## 3. The two conjuncts have different literatures, and the review should expect them to disagree

| | Conjunct 1 — heritability | Conjunct 2 — selection response |
|---|---|---|
| Quantity | variance ratio h², or h²_SNP | mean shift per generation |
| Data | twin registries, pedigrees, sibling pairs, GWAS/GREML | genotyped cohorts with completed fertility |
| Typical result | non-zero, moderate, well replicated | non-zero, directionally consistent, **very small** |
| Bears on the SDT? | no — see §2 | yes, in principle |

The v5 entry's own note already concedes the magnitude problem: "operates over centuries, not decades."
The chapter's likely finding is therefore visible from here, and stating it in advance is a commitment,
not a conclusion: **the well-evidenced half of the claim is demographically inert, and the half that
would matter is estimated at a magnitude that cannot move the SDT.** The synthesis has to be built so
that this outcome is reportable without reading as a dismissal of a literature that is, on its own
terms, careful and successful.

## 4. The moderation finding, where the causal arrow runs backwards — and the phenomenon problem

There is a third proposition in this literature that the registered claim does not contain, and it is
the one with the most scientific content. Udry (1996) and Kohler, Rodgers and Christensen (1999, 2002)
report that the heritability of fertility is **not constant across cohorts** — it is larger where
fertility is under individual control and smaller where it is set by norms and constraint. The
mechanism is intelligible: when everyone is doing what the village does, phenotype does not express
individual disposition; when fertility becomes a choice, it does.

If that is right, then h² is an **outcome of the demographic transition, not a cause of it.** The arrow
runs from the SDT to the heritability, which is the reverse of the direction A.18 is registered to test.

This is worth the chapter's attention rather than a footnote, and it changes the phenomenon assignment:

> **Ruling 2 — A.18 is not an SDT-only chapter. (Shravan, 2026-08-31; PI decision required.)**
> Two independent reasons.
> (a) The moderation finding is a *contrast across regimes* — pre-transition versus post-transition
> cohorts — so it cannot be estimated inside the SDT window alone. It needs PM/FDT cohorts as the
> comparison arm.
> (b) The best-identified selection-response evidence in the entire literature is **historical**:
> Milot et al. (2011) on Île aux Coudres and Courtiol et al. (2012) on pre-industrial Finland use
> complete parish pedigrees with observed multi-generational reproductive histories — data no
> contemporary cohort can match. Restricting to SDT drops the identified arm and leaves the chapter
> resting on UK Biobank and HRS, which are the *weakest* designs in the set (§10).
> This is the A.23 pattern exactly (`identified-evidence-in-the-unnamed-arm`): count identified designs
> per arm before scoping one out. Proposed: **PM and FDT admitted as evidence arms; SDT remains the
> only arm carrying a demographic-significance verdict.** Requires a v5 `phenomena` edit; flagged to
> TICK-001, not made here.

## 5. Where admissible variation could come from — enumerated before searching

Per the C.3.g lesson (`empty-cell-needs-second-channel`), each design is named now and becomes a
required search string, so that an empty cell is empty against an auditable list.

**For conjunct 1 (decomposition):**
1. **Classical twin designs** — MZ/DZ comparison on completed fertility, AFB, childlessness.
2. **Adoption and reared-apart designs** — the only decomposition that breaks gene–environment
   correlation by construction. Rare for fertility; specifically hunted.
3. **Extended-family / children-of-twins designs** — separate vertical transmission from genotype.
4. **Molecular GREML / SNP-heritability** on unrelated individuals.
5. **Within-sibship GWAS** (Howe et al. 2022) — the design that strips population stratification and
   assortative-mating inflation. The gap between population and within-family estimates is itself a
   finding and must be extractable.

**For conjunct 2 (selection response):**
6. **Polygenic-score selection differentials** — regress relative fitness on a PGS in a cohort with
   completed fertility.
7. **Observed multi-generational pedigrees** — measured trait change across generations with known
   kinship (Milot, Courtiol).
8. **Predicted response via the breeder's equation** from an independently estimated h² and S.
9. **Allele-frequency change over time** in genotyped samples across birth cohorts (Kong et al.).

## 6. The homonym, measured

"Fertility" is one of the worst homonyms in the review, and it collides with A.18's *method* vocabulary
rather than being separable from it. A fulltext probe on 2026-08-31 (OpenAlex `search=`, counts
indicative of the contaminated space, not of the frame):

| Probe | Count |
|---|---|
| `heritability of fertility` | 45,488 |
| `heritability of fertility dairy cattle` | 8,819 |
| `soil fertility heritability` | 15,211 |
| `heritability number of children ever born` | 6,880 |

Roughly half of the naive topic query is livestock reproduction and agronomy. Both clouds use
*heritability*, *selection differential*, *breeder's equation*, *genetic correlation* and *fertility*
in their ordinary technical senses. There is no term that separates them from A.18 on the exposure
axis, because the exposure vocabulary is shared exactly.

Two consequences, both from lessons already recorded. Per `homonym-shares-outcome-vocabulary`, the
discriminating vocabulary must be scored **without** the shared word — the separator here is the
*outcome unit* (children ever born, parity, age at first birth, childlessness) and the *species*, not
the method. And per `label-by-provenance-not-vocabulary`, the frame is built from the citation
provenance of the §12 anchors first, with term-mining used only to extend it; a term-first frame on
this topic will be dominated by cattle.

The animal and plant clouds are **route-outs, not decoys to be forward-seeded** — but note
`decoy-clouds-are-boundary-cases`: human-adjacent quantitative genetics (primate demography,
hunter-gatherer pedigree studies) sits between them and is the boundary worth sampling.

## 7. The boundary walls

**Wall 1 — A.18 vs A.19 (`intergenerational-transmission-fertility`): the decomposition wall.**
This is the wall that will move the most records. A.19 owns the parent–child fertility correlation as a
social phenomenon. A.18 owns **only the portion of that correlation that a design attributes to
genotype.** Discriminator: does the design decompose? A raw intergenerational correlation, however
well measured, is A.19's and is **not evidence for A.18** — it is equally consistent with pure social
transmission. Twin, adoption, children-of-twins, sibling and molecular designs are A.18's.

**Wall 2 — A.18 vs D.1.c (`cultural-evolution-demographic-transition`): the transmission-channel wall.**
v5 already cross-refs these two. D.1.c is prestige-biased *cultural* transmission; A.18 is genetic
transmission. They are competing explanations of the same observable, so a study that cannot separate
them belongs to neither and is `UNDECOMPOSED`. Dual-inheritance models that estimate both channels are
reported to both chapters, unallocated.

**Wall 3 — A.18 vs B.1 (`evolutionary-sex-drive-contraceptive-decoupling`): closed chapter, live seam.**
B.1's estimand is status → fertility; A.18's is genotype → fertility. Fieder and Huber (2007) and the
Stulp–Barrett line sit on the seam. Discriminator: **is the predictor a genetic measure?** If the
predictor is phenotypic status, it is B.1's, even where the paper's framing is evolutionary. B.1 is
signed off pending PI review, so any record that would change its pool is flagged, not silently
absorbed.

**Wall 4 — A.18 vs A.15 / A.16 / B.3 / B.4: the fecundity-trait wall.**
Heritability of a *clinical fecundity trait* — age at menopause, PCOS, endometriosis, sperm
concentration — is not heritability of fertility. Proposed: a heritability estimate whose phenotype is
a fecundity trait with **no fertility outcome** is `LINK_TRAIT` context; the trait's own effect on
births belongs to A.15/A.16/B.3/B.4. A.18 owns heritability of **realized reproductive outcomes**.
*PI decision required:* this is a defensible narrowing but it is a narrowing, and it removes a
sizeable literature.

**Wall 5 — A.18 vs C.3.d / D.2.a and the education literature: the correlated-trait wall.**
See §9 `EXPOSURE_DISTANCE`. A study measuring selection on an **educational-attainment** polygenic
score is measuring a correlated trait, not "high-fertility genotypes." It stays in A.18 (it is the bulk
of the identified evidence) but it is tagged at a distance from the registered exposure and cannot
silently stand in for it.

**Wall 6 — species.** Non-human populations are out, with the human-adjacent boundary sampled per §6.

## 8. Estimand cells

| Cell | Estimand | Routing |
|---|---|---|
| `H2_FERTILITY` | h² (or h²_SNP) of a realized fertility outcome | Conjunct-1 pool. **Never enters demsig** (Ruling 1) |
| `H2_MODERATION` | h² estimated separately by cohort, regime, or contraceptive availability | Conjunct-3 pool (§4). Reported prominently; **arrow runs backwards**, excluded from demsig |
| `SELECTION_DIFFERENTIAL` | Covariance of a genetic measure with realized relative fitness | Conjunct-2 pool — **the demsig arm** |
| `ALLELE_FREQ_TREND` | Change in a genetic measure across birth cohorts | Conjunct-2 pool, separate stratum (different estimator) |
| `PEDIGREE_RESPONSE` | Observed multi-generational trait change with known kinship | Conjunct-2 pool, separate stratum. Mostly PM/FDT (Ruling 2) |
| `PREDICTED_RESPONSE` | R computed by the authors from their own h² and S | Conjunct-2, flagged derived — do not pool with directly estimated R |
| `WITHIN_VS_POPULATION` | Same phenotype estimated both within-family and population-wide | Bias-magnitude record (§10); reported as a ratio |
| `LINK_TRAIT` | h² of a fecundity trait, no fertility outcome | Context; cross-ref A.15/A.16/B.3/B.4 (Wall 4) |
| `UNDECOMPOSED` | Parent–child fertility correlation with no decomposition | Route out to A.19 (Wall 1) |
| `OFF_STATUS_B1` | Phenotypic status → fertility | Route to B.1 (Wall 3) |
| `OFF_SPECIES` | Non-human | Route out (Wall 6) |
| `THEORY` | Quantitative-genetic and dual-inheritance theory, no estimate | Theory stream |
| `INSUFFICIENT_INFO` | Not routable on the visible record | Pairs only with `UNCERTAIN` |

## 9. Required tags on every included empirical effect

- `DESIGN_CLASS` — twin / adoption / children-of-twins / sibling / GREML / within-sibship GWAS /
  population GWAS / pedigree / PGS-fitness regression. **The list is a gate**: an unlisted design must
  fail loudly rather than fall through to a default, per `estimator-class-list-is-a-gate`. A
  within-family estimate pooled with a population estimate is the specific error this prevents.
- `RELATEDNESS_LEVEL` — `WITHIN_FAMILY` / `POPULATION`. Drives the §10 bias correction and is the
  single most important stratifier in the chapter.
- `EXPOSURE_DISTANCE` — how far the measured genetic exposure sits from the registered one:
  `FERTILITY_PGS` / `AFB_PGS` / `EDUCATION_PGS` / `OTHER_CORRELATED_PGS` / `ANONYMOUS_VARIANCE` (twin
  h², where no variant is named). Adopted from A.24, where the discovery that *zero* studies measured
  the registered exposure was the chapter's finding. On present reading A.18 will be
  `EDUCATION_PGS`-heavy and that must be visible in a table, not in prose.
- `OUTCOME_MEASURE` — completed fertility / children ever born at survey / AFB / childlessness /
  grandoffspring count. Pooled separately.
- `COHORT_COMPLETE` — whether reproduction is complete for the sample. An S computed on incomplete
  cohorts is censored and biased toward early reproducers; per
  `identity-arms-need-a-survival-correction`, the attrition is enumerated before any R is computed.
- `SAMPLE_SELECTION` — volunteer biobank / population register / clinical / parish. UK Biobank's
  healthy-volunteer selection and HRS's survivor selection both correlate with fertility.
- `ASSORTATIVE_MATING_HANDLED` — whether the design corrects for it. Assortative mating inflates
  classical h² and is strong on education and AFB.
- `PHENOMENON_WINDOW` — PM / FDT / SDT birth cohorts covered (Ruling 2).

## 10. Identification threats

1. **Gene–environment correlation.** "Heritability of number of children" absorbs the heritability of
   everything upstream — education, health, partnering. The estimand is genotype's *total* association,
   not a genetic effect on fertility holding the life course fixed. This is a property of the quantity,
   not a flaw in the studies, and it must be stated in the chapter's own words rather than inherited
   from the papers' abstracts.
2. **Population stratification and dynastic effects.** Population-level PGS associations are inflated by
   ancestry structure and by parental environment correlated with transmitted genotype. Howe et al.
   (2022) is the correction; the within-family/population ratio is extracted wherever both exist.
3. **The equal-environments assumption** in classical twin designs.
4. **Selection on the sample.** See `SAMPLE_SELECTION`. A selection differential estimated in a
   volunteer cohort is estimated in a sample selected on traits correlated with the outcome.
5. **Censoring.** See `COHORT_COMPLETE`.
6. **Reverse causation on h² itself.** §4 — the moderation finding means h² is an outcome. Any
   cross-cohort comparison of h² is descriptive, never causal, for A.18's purposes.
7. **Publication and replication asymmetry** in molecular results, which the pre-2015 candidate-gene
   layer of this literature has in an acute form. Candidate-gene-era estimates are extracted but
   stratified out of the primary pool.

## 11. The demographic-significance computation, pre-specified

Fixed now so the arithmetic is not chosen after the numbers are known.

- **Numerator.** Per-generation response to selection, R = h² × S, in units of children per woman,
  where S is the selection differential on the fertility-relevant genetic measure in a cohort with
  completed reproduction. Where a study reports R directly (pedigree designs), that is used and
  `PREDICTED_RESPONSE` estimates are not pooled with it.
- **Generations.** SDT window 1965–2025 at a mean generation length taken from the data, not assumed —
  roughly two generations. The cumulative genetic contribution is R × G.
- **Denominator.** The observed TFR decline over the same window in the same reference population, per
  PROTOCOL §4.2.1. **The denominator rule is binding and is not restated loosely here.**
- **Sign.** A rebound is a *positive* contribution against a *negative* observed change. The chapter
  reports it as an offset, and the sign convention is written into the table generator, because
  A.23's demsig was wrong-signed and B.5's FDT sign was inverted.
- **Output.** Emitted from computed JSON by the table generator, never hand-typed
  (`generate-result-tables-never-retype`).

> **Ruling 3 — an `EDUCATION_PGS` selection differential may not be converted into a fertility
> response without an explicit, stated genetic correlation. (PI decision required.)**
> Most of the identified evidence measures selection on education-associated variants. Turning that
> into "children per woman" requires r_g between the education PGS and fertility, which is itself an
> estimate with a confidence interval. Either the conversion is done transparently with that interval
> propagated, or the arm reports selection in PGS standard units and declines to convert. The chapter
> must not present an unstated conversion.

## 12. Cold-start anchors — resolved 2026-08-31, all 25 confirmed

Candidates in `literature/search-logs/heritability-fertility-genetic-anchor-candidates.json`, resolved by `source/build/goldset/245_a18_cold_start_anchors.py` →
`literature/search-logs/heritability-fertility-genetic-cold-start-anchors.json`. 25 candidates typed
from the literature, 25 `MATCH` after the fix in the note below. No ghost citations. Years are
OpenAlex's and correct several of the candidate list's: Briley 2016, Byars 2009, Sanjak 2017,
Nisén 2013.

Spine of the set: Kohler et al. 1999 (*PDR*) and Rodgers et al. 2001 (*Demography*) for the twin
decomposition; Udry 1996 (*PDR*), Kohler et al. 2002 and Nisén et al. 2013 for moderation; Tropf et al.
2015 (*Population Studies*), 2017 (*Nat Hum Behav*), Briley et al. 2016, Zietsch et al. 2014,
Barban et al. 2016 (*Nat Genet*) and Mills et al. 2021 for the molecular layer; Beauchamp 2016,
Kong et al. 2017, Byars et al. 2009, Sanjak et al. 2017, Conley et al. 2016 and Hugh-Jones and
Abdellaoui 2022 for contemporary selection; Milot et al. 2011 and Courtiol et al. 2012 for the
historical pedigree designs that Ruling 2 turns on; Howe et al. 2022 for the within-family correction;
Stearns et al. 2010, Mills and Tropf 2020 and Stulp and Barrett 2016 as reviews.

> **Note on the resolver — a known defect reproduced in new code.** The first run returned two
> `NO_RESULTS`, both titles containing a question mark. OpenAlex reads `?` in a search value as a
> wildcard and refuses the query with a 200 and a JSON body carrying no `meta.count`; the script's
> error check looked only for non-JSON, so a refusal was recorded as an absence — `refusals-read-as-zeros`
> and `openalex-wildcard-refusal` in one place, in a script written the same day both lessons were
> available. Both are fixed at source: `?` and `!` are stripped from search values, and a response
> without `meta.count` now returns `QUERY_REFUSED`, which is a distinct verdict from `NO_RESULTS` and
> is never reported as an absence. **This belongs in the shared resolver, not here** — filed alongside
> TICK-074, which is already the shared-resolver punctuation ticket and is unmerged.

**Cold-start channels, in order.**
1. *Reviews as authority.* Stearns et al. 2010, Mills and Tropf 2020, Sear/Stulp-adjacent surveys —
   harvest reference lists. `no-review-exists-is-a-finding` does not apply: reviews plainly exist here.
2. *Backward citations* of the 25 anchors.
3. *Forward citations* of Kohler 1999, Barban 2016, Kong 2017 and Howe 2022 — the four the field builds
   on, chosen to span all three arms rather than the most-cited.
4. *Registry vocabulary.* The Danish, Swedish, Finnish and Icelandic twin/population registers are named
   channels; the `policy-literatures-indexed-in-local-vocabulary` lesson generalises — register-based
   demography indexes under the register's name.
5. *Method vocabulary as a second channel*, per `channels-must-fail-differently`: GREML, LD-score
   regression, within-sibship, breeder's equation, selection gradient. This channel must fail for
   unrelated reasons to the topical one, and it is tested on a known positive (Sanjak 2017) first.

## 13. Rulings requiring PI sign-off

| # | Ruling | Where | Blocks |
|---|---|---|---|
| 1 | demsig computed on the selection response, never on h² | §2 | synthesis, and the A.9 precedent |
| 2 | admit PM/FDT as evidence arms; SDT alone carries the verdict | §4 | **the production query** — cannot be deferred |
| 3 | no unstated `EDUCATION_PGS` → fertility conversion | §11 | demsig |
| 4 | fecundity-trait heritability is `LINK_TRAIT`, not A.18 | Wall 4 | screen rubric |
| 5 | v5 `claim` and `phenomena` fields need editing to match Rulings 1–2 | §1, §4 | TICK-001, not this ticket |

Rulings 2 and 4 change what the query must reach and what the screen admits, so stage 3 does not start
until they are answered. Rulings 1 and 3 bind at synthesis and can run behind.

## 14. When to adjudicate

Boundary calls are batched and read against the **outcome** axis, not the exposure axis — the A.23
`wall-packet-sorted-on-exposure` lesson, which turned 26 records into 7 studies and made the expensive
ruling the cheap one. Wall 1 (A.18 vs A.19) is the packet that matters and is assembled first, because
it is the wall that determines whether this chapter has a primary pool at all.
