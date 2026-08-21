# Search scope — twinning rates and multiple births

**Hypothesis:** A.12 (HYPOTHESES-v5.md)
**Hypothesis slug:** `twinning-multiple-births`
**Target phenomena:** PM and SDT as enumerated. The SDT arm is further restricted to a **bounded
sub-period** — see "v5's ART clause is time-inverted". The PM arm survives only in a reduced form —
see "The PM arm is real but it belongs to A.8".
**Ticket:** TICK-070
**Status:** **DRAFTED, NOT FROZEN** (Shravan, 2026-08-20). Nine walls, ten estimand cells, five PI
calls. The reconnaissance is run; the scope below is written against it rather than against memory.

Built on the D.3.c (`despair-hopelessness-fertility`) template, which inherits B.6's, B.7's, B.5's,
D.2.d's and D.3.b's. Six constraints carry forward as design decisions rather than being
rediscovered:

- the taxonomy carries `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER`;
- **a wall whose discriminator is invisible in a title or abstract is declared unenforceable up
  front** rather than trusted and audited later;
- the forward-citation seed rule is uniform across seed types, with no special case for routing
  decoys;
- **an arithmetic statement of the mechanism is an upper bound to be corrected, not the effect** —
  this constraint, inherited from B.5's `(1-p)` accounting error, is the governing one here;
- a chapter whose evidence sits on a different proposition from its claim rates **the claim**;
- Tier-A anchors are studies in their own right, not an artifact of the screen.

The scope is written against a live reconnaissance pass over OpenAlex (2026-08-20; **63 probes, zero
failed requests**, so every zero-hit count reported here is a genuine absence rather than a refusal).
Counts are regenerable via `source/build/goldset/160_a12_recon_probe.py` and reported in
`twinning-multiple-births-recon-probe.md`.

## Causal claim

Variation in the twinning rate — genetic across populations, ART-induced within the modern period —
raises live births per pregnancy and therefore raises the total fertility rate above what the same
number of pregnancies would otherwise produce. v5 adds a directional clause: ART-induced multiples
**partially offset** postponement-driven SDT declines.

## A.12 is an accounting identity with a behavioral offset, and only the offset is estimable

This is the finding that shapes every downstream decision, so it is stated before the walls rather
than discovered during screening.

The mechanism decomposes into two parts that need completely different treatment, and v5's entry
runs them together.

**The mechanical part is an identity.** If a fraction *t* of deliveries produce twins, live births
exceed deliveries by approximately a factor of (1 + *t*). Twinning rates in developed countries have
run between roughly 1% and 4% of deliveries across the whole observed record. The implied uplift on
TFR is therefore on the order of one to four percent. This is arithmetic. It cannot be wrong, it
requires no study to establish, and no study estimates it — which the reconnaissance confirms
directly rather than by assumption:

| Probe | n | What sits at the citation-ranked head |
|---|---|---|
| twinning rate **AND** population fertility quantity | **25** | *Births: Final Data for 2013*; *Annual Summary of Vital Statistics* |
| multiple births **AND** TFR / completed fertility | **93** | the same vital-statistics series |
| twinning as an explicit determinant of fertility level | **10** | Greek twin-birth trends; **four veterinary papers on ewes, goats and cattle** |

The primary cell is populated by **statistical reports, not estimation studies**. That is the correct
state of the world for an identity: identities get tabulated, not identified. A reviewer who screens
this cell expecting effect estimates will find none and conclude the literature is thin. It is not
thin — it is a different kind of literature, and the chapter's mechanical arm is a computation run on
it, not a synthesis of it.

**The behavioral part is a real estimable parameter, and it is the only place A.12 can be wrong.**
The identity gives the effect on *births*. The effect on *completed fertility* is smaller by whatever
subsequent fertility a twin birth displaces: if parents target a family size, a twin birth overshoots
the target and they stop earlier. The mechanical uplift is therefore an **upper bound**, and the
offset is the quantity worth estimating.

That parameter has been estimated, by name, three times:

- **Alter and Hacker (2024), *Demography*** — "The Impact of Multiple Births on Fertility: Stopping
  and Spacing in the United States During the Twentieth Century" (`10.1215/00703370-11577526`). This
  is the primary-cell study, and it is squarely on the estimand. Six citations; published last year.
- **Robson and Smith (2012), *Proceedings of the Royal Society B*** — "Parity progression ratios
  confirm higher lifetime fertility in women who bear twins" (`10.1098/rspb.2012.0436`). The offset
  is **incomplete**: mothers of twins finish with higher lifetime fertility, not the same.
- **Clark, Cummins and Curtis (2020), *Demography*** — "Twins Support the Absence of
  Parity-Dependent Fertility Control in Pretransition Populations" (`10.1007/s13524-020-00898-0`).
  In pre-transition populations there is **no** stopping response, so the mechanical uplift passes
  through in full.

Note what the third one is actually doing, because it decides the PM arm below.

## The largest relevant literature reports our parameter as a nuisance

The twin-birth-as-instrument literature is the biggest body the probes touched that bears on A.12 at
all — 228 records on the instrument probe, with a canon that is unambiguous:

| Cites | Work |
|---|---|
| 1,049 | Black, Devereux and Salvanes (2005), *QJE* — "The More the Merrier?" |
| 716 | Rosenzweig and Wolpin (1980), *Econometrica* — "Testing the Quantity-Quality Fertility Model" |
| 537 | Angrist, Lavy and Schlosser (2010), *JOLE* — "Multiple Experiments for the Causal Link…" |
| 368 | Bronars and Grogger (1994), *AER* — "The Economic Consequences of Unwed Motherhood" |
| 348 | Rosenzweig and Zhang (2008), *Demography* — quantity-quality in China |
| 27 | Farbmacher, Guber and Vikström (2018), *J. Applied Econometrics* — "Increasing the credibility of the twin birth instrument" |

Every one of these uses a twin birth as exogenous variation in family size in order to estimate the
effect of family size on **child outcomes**. None is a study of twinning's effect on fertility. For
A.12's purposes the body is a decoy — **except for its first stage**, which is precisely the offset
parameter, estimated on large administrative samples with clean identification, and reported as a
nuisance quantity on the way to the result the authors cared about.

**This is a wall that cannot be enforced at title or abstract.** Whether a paper's first-stage table
reports the completed-fertility response to a twin birth is invisible in its metadata; the abstract
talks about education and earnings. D.3.b taught this lesson at cost — measure content is not visible
to a title/abstract screen, and a wall that depends on it must be declared unenforceable up front
rather than trusted and audited later. Here the consequence is concrete and is **PI call 2**:
recovering these estimates means routing the twin-IV canon to full-text first-stage extraction, not
screening it out and not screening it in.

## v5's ART clause is time-inverted

v5 states that ART-induced multiples "partially offset postponement-driven SDT declines" — present
tense, and framed as a growing term. The reconnaissance says that description fits a period that has
closed.

The elective-single-embryo-transfer literature is large and settled: 1,942 records, headed by the
*NEJM* 2004 randomized trial of elective single- versus double-embryo transfer (600 cites) and a
BMJ individual-patient-data meta-analysis (397). eSET spread through practice and regulation from the
early 2000s, and ART multiple-birth rates fell sharply behind it. The demographic literature has
already named the shape: **Monden, Smits and Pison (2021), "Twin Peaks: more twinning in humans than
ever before"** (229 cites) — a peak, not a trend — alongside **Pison, Monden and Smits (2015),
*Population and Development Review*, "Twinning Rates in Developed Countries: Trends and
Explanations"** (129 cites).

So the ART-multiples term rose to a maximum in the 1990s–2000s and has been shrinking since. Over the
SDT as a whole it is not a monotone offset to postponement; it is a hump. Rating v5's clause as
written means rating a claim that is **period-dependent and, for the post-2010 period, the wrong
sign**. Following the D.3.c precedent, the chapter rates the claim as stated and reports the
inversion, rather than quietly amending the registry entry — that is **PI call 4**.

## The PM arm is real but it belongs to A.8

Twinning cannot explain pre-modern fertility variation. Cross-population twinning-rate differences
are genuinely large in relative terms — the West African dizygotic literature is real, with *Twinning
across the Developing World* (PLoS ONE 2011, 305 cites) as its anchor — but they are differences
between roughly 1% and roughly 2% of deliveries. Against PM fertility variation measured in whole
children per woman, a one-percentage-point difference in the twinning rate is not a candidate
explanation, and no arithmetic makes it one.

What the PM twinning literature is actually good for is **testing A.8**. Clark, Cummins and Curtis
use twin births exactly as an instrument to ask whether pre-transition populations practiced
parity-dependent stopping, and conclude they did not. That is a first-order finding for
`parity-progression-stopping-behavior`, and only incidentally about twinning. The same is true of the
evolutionary-fitness cluster the probes surfaced — *Natural selection on human twinning* (Nature
1998), *The fitness of twin mothers: evidence from rural Gambia* (2001) — which asks whether bearing
twins raises maternal fitness, a different question again.

The recommendation, which is **PI call 5**, is that A.12's PM arm reduces to a bounded arithmetic
statement plus an explicit cross-reference, and that Clark, Cummins and Curtis is routed to A.8 as a
Tier-A anchor there rather than being extracted here as evidence for A.12.

## Decoy clouds: homonyms are not boundary cases

The standing guidance from the decoy-cloud work is that a decoy cloud is usually a *boundary case* —
on-topic rates of 29–88% against 1–14% for the theory canon — and that refusing to forward-seed from
decoys discards the best available channel. A.12 is the first chapter where that guidance needs a
carve-out, because two of its four decoy families are not boundary cases at all. They are **pure
homonyms with no on-topic content whatever**, and the reconnaissance is emphatic about their size:

| Family | What "twinning" or "fertility" means there | Evidence from the probes |
|---|---|---|
| **Crystallography** | a crystal lattice defect | *A short history of SHELX* (**87,676 cites**), *SHELXT* (29,184), *PLATON SQUEEZE* (3,788) — these outrank every genuine A.12 record by two orders of magnitude and sit at the head of three separate probes |
| **Materials and systems engineering** | TWIP steel = *Twinning*-Induced Plasticity; "Digital Twin" | Fe–Mn–(Al,Si) TRIP/TWIP steels (1,812); *Digital Twin-driven framework for fatigue lifecycle management of steel bridges* |
| **Animal science and agronomy** | ewe, cow, mare, goat reproduction; soil fertility | Awassi ewes, Merino flocks, Holstein cattle, mule deer, thoroughbred mares — **four of the eight** records in the "twinning as a determinant of fertility level" head |
| **Behaviour genetics** | twins as a research *design*, not a rate | 155,480 records on the design vocabulary; 3,340 once "fertility" is added |

The first three are separable lexically, because the discriminating vocabulary genuinely does not
overlap: a crystallography paper never says "total fertility rate", and a sheep paper never says
"completed fertility". They get a **hard exclusion** in the production query and a labelled cell, not
a routing decision.

The fourth is a boundary case in the ordinary sense and gets the ordinary treatment. Behaviour
genetics is A.18's territory (`heritability-fertility-genetic`), it shares real substance with A.12
at the edges — the heritability of dizygotic twinning is a genuine A.12 input — and it must be routed
rather than excluded.

**One probe design error is recorded here so the production query does not repeat it.** The
"contribution or share of multiple births" probe returned **43,319** records headed by SHELX,
because `"contribution to"` and `"accounted for"` are generic English rather than discriminative
terms. Non-discriminative anchors do not narrow a query; they hand it to whatever cloud is largest.

## Walls

| # | Wall | Enforceable at title/abstract | Treatment |
|---|---|---|---|
| 1 | Crystallographic twinning | **Yes** | hard exclude → `OFF_HOMONYM_CRYSTAL` |
| 2 | TWIP steel / digital twin | **Yes** | hard exclude → `OFF_HOMONYM_ENGINEERING` |
| 3 | Non-human fertility (veterinary, agronomy, soil) | **Yes** | hard exclude → `OFF_NONHUMAN` |
| 4 | Twin *design* studies (A.18) | Partly | route → `OFF_TWINDESIGN`, forward-seed retained |
| 5 | Perinatal/obstetric outcomes **of** being a multiple | **Yes** | exclude → `OFF_PERINATAL` |
| 6 | Clinical ART practice (transfer protocols, success rates) | **Yes** | exclude → `OFF_ART_CLINICAL` |
| 7 | ART's total fertility contribution (A.17) | Partly | route → PI call 3 |
| 8 | **First-stage offset estimates inside the twin-IV canon** | **NO — declared unenforceable** | route to full-text extraction |
| 9 | Twinning as *outcome* (determinants: age, parity, ART, nutrition) | **Yes** | route → `EXPOSURE_SERIES`, not excluded |

Wall 8 is the one that matters, and it is declared unenforceable on the D.3.b precedent rather than
trusted and audited after the fact.

## Estimand cells

| Cell | Contents | Extractable |
|---|---|---|
| `PRIMARY_MECHANICAL_IDENTITY` | the arithmetic uplift from twinning rate series | **Computed, not searched** |
| `PRIMARY_OFFSET_STOPPING` | effect of a twin birth on subsequent/completed fertility | yes — Alter-Hacker, Robson-Smith, Clark et al. |
| `PRIMARY_OFFSET_FIRSTSTAGE` | the same parameter inside twin-IV first stages | yes, full-text only (Wall 8) |
| `SECONDARY_ART_MULTIPLES` | ART's contribution to the multiple-birth rate and thence to TFR | yes; overlaps A.17 |
| `SECONDARY_PM_VARIATION` | cross-population twinning variation | bounded statement only |
| `EXPOSURE_SERIES` | twinning-rate determinants and compilations | not an effect; feeds stage 10 |
| `OFF_HOMONYM_CRYSTAL` / `OFF_HOMONYM_ENGINEERING` / `OFF_NONHUMAN` | homonym clouds | — |
| `OFF_TWINDESIGN` | behaviour genetics → A.18 | — |
| `OFF_PERINATAL` / `OFF_ART_CLINICAL` | health outcomes and clinical practice | — |
| `INSUFFICIENT_INFO` / `OFF_OTHER` | | — |

## What demographic significance runs on — confirmed live, not remembered

The stage-10 computation does not depend on PDF retrieval, which is what makes this chapter cheap and
is the reason it was selected. Both inputs were verified against live records:

- **The Human Multiple Births Database.** Torres, Caporali and Pison (2023), *Demographic Research*,
  "The Human Multiple Births Database (HMBD)" — plus a **static data deposit on Figshare (2022)** by
  the same authors. Country-year twinning rates, harmonized, from the INED group that produced the
  PDR trend papers. This is the exposure series, it is open, and it is citable.
- **ART registry reporting.** ICMART world reports, ESHRE European registers, and CDC/SART
  surveillance in the United States, all of which the probes resolved to real high-citation records.

No stage of this chapter is retrieval-bound in the way B.1 was — the binding input is a public
database, not 95 PDFs behind a proxy.

## Citation hygiene — two findings against v5's seminal list

Per the version-of-record gate, v5's three seminal citations were tested rather than accepted.

1. **Bulmer 1970, *The Biology of Twinning in Man*** — resolves correctly (book, 563 cites). But the
   author-wording retry resolved instead to a **1971 book review** of it (4 cites). This is the
   book-canon hazard exactly as recorded: monographs resolve to their own reviews, and the
   first-author gate is what separates them.
2. **Pison and D'Addato 2006** — the correct title is *Frequency of Twin Births in **Developed**
   Countries* (*Twin Research and Human Genetics*), not "among the world populations" as v5's list
   implies. It carries **two DOIs** — `10.1375/twin.9.2.250` (98 cites) and
   `10.1375/183242706776382338` (66) — same title, year, venue **and authors**. Under the corrected
   duplicate-record gate, author agreement makes this a genuine duplicate record with a split
   citation count, and dedup must merge it.
3. **Hoekstra et al. 2008, "Dizygotic twinning"** — the record the probes surfaced is *Human
   Reproduction Update* **2007**, 203 cites. Year needs confirming at anchor sourcing; flagged, not
   yet resolved.

A note for whoever reads the probe report: the fifteen zeros in **pass 2** of the named-work table
are **not** evidence of absent literature. Pass 2 queries carry author surnames, and `title.search`
matches titles only. They are a wording test, and their zeros mean the wording was wrong — which is
the documented two-pass design, not a finding.

## Open PI calls

1. **Is A.12 a hypothesis or an accounting correction?** Its mechanical arm cannot be wrong and its
   behavioral arm is really a test of A.8. The options are a short chapter with a bounded
   "demographically trivial" verdict, or demotion to a measurement-appendix note plus a methods input
   to A.8. *Recommendation: keep the chapter.* The review promises a per-hypothesis verdict for every
   enumerated hypothesis, and a precisely bounded negative is a deliverable, not a non-result.
2. **Do twin-IV first stages count as included studies?** They estimate our parameter but report it
   as a nuisance, and Wall 8 means they cannot be found by screening. *Recommendation: yes, routed to
   full-text first-stage extraction* — this is where the chapter's identification actually lives.
3. **Who owns ART multiples, A.12 or A.17?** They are a sub-channel of ART's total fertility
   contribution and must not be counted twice.
4. **Rate v5's ART clause as written, or amend the registry?** *Recommendation: rate as written and
   report the inversion*, following D.3.c.
5. **Does the PM arm survive?** *Recommendation: reduce to a bounded arithmetic statement and route
   Clark, Cummins and Curtis to A.8.*

Calls 1, 3 and 5 change what gets searched and so should be answered before the production run.
Calls 2 and 4 change what gets extracted and reported, and can be answered during the run.
