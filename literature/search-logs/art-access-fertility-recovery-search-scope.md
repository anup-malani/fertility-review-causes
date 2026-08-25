# Search scope — assisted reproductive technology access

**Hypothesis:** A.17 (HYPOTHESES-v5.md)
**Hypothesis slug:** `art-access-fertility-recovery`
**Target phenomenon:** SDT only, as enumerated. ART does not exist before 1978 and is demographically
negligible before the mid-1990s, so PM and FDT are not merely unsupported here — they are outside the
technology's existence. The chapter states that rather than rating an absence.
**Ticket:** TICK-072
**Status:** **DRAFT** (Shravan, 2026-08-25). Eight walls, six estimand cells, five PI calls. The
reconnaissance is run and the scope below is written against it rather than against memory. Not
frozen: Call 1 changes what the chapter *concludes*, not what it retrieves, but Calls 2 and 3 change
the frame and should be settled before the production pull.

Built on the A.12 (`twinning-multiple-births`) template, which inherits D.3.c's, B.6's, B.7's, B.5's,
D.2.d's and D.3.b's. Six constraints carry forward as design decisions rather than being
rediscovered:

- the taxonomy carries `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER`;
- **a wall whose discriminator is invisible in a title or abstract is declared unenforceable up
  front** rather than trusted and audited later;
- **an arithmetic statement of the mechanism is an upper bound to be corrected, not the effect** —
  inherited from B.5's `(1-p)` error and A.12's identity arm; it is the governing constraint here too;
- a chapter whose evidence sits on a different proposition from its claim rates **the claim**;
- Tier-A anchors are studies in their own right, not an artifact of the screen;
- failed requests are bucketed separately from zero-hit counts, so an absence means absence.

Counts below are regenerable via `source/build/goldset/185_a17_recon_probe.py` (53 requests, 1 failed,
1.9%) and `source/build/goldset/186_a17_strict_anchor_probe.py` (32 requests, 0 failed), reported in
`art-access-fertility-recovery-recon-probe.md` and `-strict-anchor.md`.

## Causal claim

Availability and affordability of ART (IVF, ICSI, egg freezing) partially offsets age-related
fecundity decline and enables completion of postponed fertility, raising TFR relative to the
counterfactual without ART.

## A.17 has two arms that answer different questions, and they must not be pooled

This is the finding that shapes every downstream decision, so it is stated before the walls rather
than discovered during extraction. It is the same shape as A.12's identity-plus-offset split, and it
is inherited knowingly.

**Arm 1 — the accounting arm.** National registries report ART-conceived births. Divide by all births
and you have ART's share: a real, well-measured, directly citable number. The literature that
produces it is verified present and canonical — Sobotka et al. (2008) on Danish data (71 cites),
Lazzari, Gray and Chambers (2021) on fertility rates and parity transition (35), Leridon (2004) on
whether ART can compensate for age-related decline (519), Habbema et al. (2015) on when couples
should start (146), Leridon and Slama (2008) on fecundity decline and postponement (151).

**Arm 1 answers "how many births are ART births", which is not the claim.** The claim is about a
counterfactual: births *relative to the counterfactual without ART*. Treating the ART share as the
effect assumes every ART birth would otherwise not have occurred — that no couple would have
conceived later without treatment, paid out of pocket instead, adopted, or succeeded on a subsequent
unassisted cycle. **The share is an upper bound on the effect**, in exactly the way A.12's `(1 + t)`
identity was an upper bound on twinning's contribution and B.5's `(1 - p)` accounting overstated by
2.5x. The chapter computes it, labels it a bound, and does not call it an estimate.

**Arm 2 — the access arm.** A distinct and much smaller literature estimates what happens to births
when ART *access* changes: US state infertility-insurance mandates and European reimbursement
reforms. This body is identified, and the reconnaissance confirms it exists rather than assuming it —
Bitler and Schmidt (2006), *Fertility and Sterility*, 215 cites; Hamilton and McManus (2011), *Health
Economics*, 91; Schmidt (2005), "Infertility Insurance Mandates and Fertility", 34; Machado and
Sanz-de-Galdeano (2015), "Coverage of infertility treatment and fertility outcomes", 20; Jain et al.
(2007) on mandates and treatment trends, 132; and an NBER working paper (2024), "The Economics of
Infertility: Evidence from Reproductive Medicine". The insurance-mandate body runs to 195 records.

**Arm 2 estimates the marginal response to access, which is also not the claim, but is closer.**
A mandate moves the inframarginal user's price, not the technology's existence. Its estimate answers
"what would one more unit of access buy", not "what would the absence of ART have cost". The two arms
therefore bracket the quantity v5 asks about — arm 1 from above, arm 2 from below — and the chapter's
job is to report the bracket honestly rather than to pool two numbers that are not estimates of the
same parameter. **The question to ask of two numbers is whether they share an estimator before pooling them**,
and here they do not even share an estimand.

**Neither arm is retrievable by the other's vocabulary**, which is why the frame below is drawn
loosely and the separation is done by screen. Arm 2's economics papers do not say "total fertility
rate"; arm 1's demography papers do not say "difference-in-differences".

## The anchored vocabulary had a homonym of its own

A.24's lesson says a decoy cloud that shares a word with the outcome axis cannot be measured with a
vocabulary containing that word. A.17's decoy cloud is the clinical per-cycle literature — 204,210
records — where **"fertility" denotes a patient's fecundity and "live birth rate" denotes a cycle's
success probability**. Following the rule, the cloud was measured twice. The result said the rule was
working:

| Vocabulary used to score the clinical cloud | Records | Share of cloud |
|---|---|---|
| PLAIN — contains bare "fertility" | 33,196 | 16.3% |
| ANCHORED — population terms, A.24's prescription | 10,765 | 5.3% |
| **STRICT — every term a population quantity** | **142** | **0.1%** |

It was not working. The "anchored" vocabulary contained **`"birth rates"`**, and in this cloud that
matches *live* birth rate, the decoy's own core measure. One term carried 10,143 of the 10,765
anchored hits — **94% of the contamination the anchored vocabulary was supposed to have removed**:

| Term, scored alone against the clinical cloud | Records |
|---|---|
| `"birth rates"` | 10,143 |
| `"childbearing"` | 619 |
| `"number of children"` | 68 |
| `"total fertility rate"` | 7 |

**The generalisation, which belongs to the workflow and not only to this chapter:** applying the
homonym rule once is not enough. The anchored vocabulary is itself a vocabulary, and it needs the
same check — is any term here a substring or a sense-neighbour of the decoy's own outcome measure?
A single contaminated term in an OR block re-admits the entire cloud, and the resulting 3x narrowing
*looks* like the rule succeeding.

## …and the strict vocabulary cannot be used to retrieve

The obvious move — draw the frame on the strict vocabulary, since it is 500x cleaner — fails a recall
check, and fails it on the canon:

| Work | Year | Cites | Inside `ART × STRICT` |
|---|---|---|---|
| Leridon, "Can ART compensate for the natural decline in fertility with age?" | 2004 | 519 | **NO** |
| Habbema et al., "Realizing a desired family size: when should couples start?" | 2015 | 146 | **NO** |
| Bitler and Schmidt, "Health disparities and infertility: state-level insurance mandates" | 2006 | 215 | **NO** |
| Hamilton and McManus, "The effects of insurance mandates … infertility treatment markets" | 2011 | 91 | **NO** |
| Schmidt, "Infertility Insurance Mandates and Fertility" | 2005 | 34 | **NO** |
| Sobotka et al., "The Contribution of Assisted Reproduction to Completed Fertility" | 2008 | 71 | yes |
| Lazzari, Gray and Chambers, "…contribution of ART to fertility rates and parity transition" | 2021 | 35 | yes |
| Machado and Sanz-de-Galdeano, "Coverage of infertility treatment and fertility outcomes" | 2015 | 20 | yes |

**Five of eight known primary-cell works fall outside it**, including the most-cited work in the
literature. A frame that loses the canon is unusable at any precision.

**A4 re-ran this check at the next order of magnitude, and the eight-case version was the optimistic
end.** Measured against every empirical anchor and the whole 7,589-record Tier-B frame: the strict
vocabulary reaches **4 of 12 anchors** where the loose vocabulary reaches all 12, and finds **2
primary-cell records against loose's 148**. In the two largest arm-2 clouds — Bitler & Schmidt and
Henne & Bundorf — population vocabulary runs 68% and 64% loose against **2% strict**, and their
strict primary cells are zero. The economics-of-access literature does not use demographers' words
for demographers' quantities, and a frame built on those words does not rank it low, it excludes it.

**The ruling: the diagnostic vocabulary and the retrieval vocabulary are separate objects, and this
scope keeps them separate by name.** `STRICT` is a measuring instrument, used to score clouds and to
size bodies. The frame is drawn on the loose vocabulary and the decoy is removed by screening, not by
querying. The cost of that choice is a screen over roughly 5,000 records rather than 51 — which is
about two dollars of batched LLM screening — screening cost has never been the binding constraint
in this project, and it is not one here.
The cost of the alternative is losing Leridon.

This is the first chapter in the series to state the split explicitly. Every prior chapter used one
vocabulary for both jobs, and the failure mode is silent in both directions: a frame tight enough to
score well loses the canon, and a vocabulary loose enough to retrieve scores its own decoy as signal.

## Frame sizes, as measured

| Frame | n |
|---|---|
| ART × ACCESS, no outcome restriction — **the retrieval frame for arm 2** | 5,039 |
| ART × ACCESS × ANCHORED | 939 |
| ART × ACCESS × STRICT | 51 |
| ART × STRICT — the whole population-relevant ART body | 412 |
| ART × contribution-language × STRICT — **arm 1's core** | 72 |
| Insurance-mandate body, any outcome | 195 |
| Clinical per-cycle cloud (Wall 1) | 204,210 |
| ART × safety and offspring outcomes (Wall 2) | 10,649 |
| ART × multiples (Wall 3, routed to A.12) | 11,580 |
| Fertility preservation and egg freezing (Wall 5) | 16,376 |

## Walls

| # | Wall | Size | Enforceable at title/abstract |
|---|---|---|---|
| 1 | **Clinical per-cycle outcomes.** Protocols, stimulation, embryo culture, transfer technique, success prediction. The outcome is a cycle's probability of success, not a population's births. | 204,210 | Yes — vocabulary and venue are both diagnostic |
| 2 | **ART safety and offspring outcomes.** Birth defects, preterm, birth weight, child development, OHSS, maternal morbidity. | 10,649 | Yes |
| 3 | **The multiplier.** ART's multiple-birth rate is A.12's, by the scope-freeze ruling: ART live births = D_ART × (1 + m_ART), A.17 owns D_ART. Routed to A.12, **not** screened out. | 11,580 | Partly — see below |
| 4 | **Infertility etiology and prevalence.** Why infertility rose is B.2/B.4/B.6/B.7's question. A.17 begins after the diagnosis. | — | Yes |
| 5 | **Oncofertility and medical fertility preservation.** Preservation before gonadotoxic treatment is a clinical indication, not a population-fertility mechanism. Elective ("social") egg freezing is **in** — v5's claim names it. | 16,376 | **No** — see below |
| 6 | **Payer-perspective cost-effectiveness.** Cost per live birth, budget impact, QALY analyses, where no birth count is reported. | — | Yes |
| 7 | **Postponement itself.** Why age at first birth rose is A.15's. A.17 takes postponement as given and asks what ART recovers from it. | 5,955 | Yes |
| 8 | **Non-OECD access and equity.** Real and important, but the SDT target is the rich-country transition. Pulled and tagged `SECONDARY_LMIC` rather than excluded, so a reversal is a re-screen and never a re-search. | — | Yes |

**Two walls are declared unenforceable at title/abstract up front**, per the D.3.b lesson:

- **Wall 5** was declared unenforceable here on the reasoning that "fertility preservation" does not
  say whether the indication was oncological or elective. **A4 measured it and the declaration was
  too broad.** Across the 910 preservation records in the Tier-B frame, 693 (76%) name an
  oncological indication in the title or abstract and 46 (5%) name an elective one; **152 (17%) name
  neither.** Wall 5 is therefore a screen rule with an `INSUFFICIENT_INFO` bucket sized at about one
  record in six, not a blanket full-text routing rule. The residue is what goes to full text.
  Note also what the same measurement says about PI call 2: the elective cell is ~46 records in the
  whole frame before screening, so it is likely to come back near-empty.
- **The arm-1/arm-2 split is itself invisible** — whether a paper *counts* ART births or *estimates*
  a response to access is often decided in the methods section, the same shape as A.12's twin-IV
  first stage. Both arms are retrieved together and separated at full-text routing, with the routing
  decision recorded per study. **A4 qualifies this in one direction.** Identification vocabulary runs
  1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones — a 4x ratio — while counting vocabulary is
  nearly flat (3.9% vs 6.0%). So identification language is a usable positive *prior* at the screen:
  a record carrying it is disproportionately arm 2. It is not a filter, since 94% of arm-2's own
  neighbourhood carries none of it. The split cannot be screened out; it is not wholly invisible.

**Wall 3 needs a rule, not just a boundary.** A single paper can report both deliveries and the
multiple-birth rate — Buckles (2012), "Infertility Insurance Mandates and Multiple Births" (31
cites), is precisely that case, and it was returned by this probe. The rule: **route by outcome, not
by topic.** If the estimated quantity is the multiple-birth *rate per delivery*, it is A.12's. If it
is deliveries, births, or a parity transition, it is A.17's. A paper reporting both is extracted by
both chapters, on different rows, and the two chapters' contributions still sum without
double-counting because the decomposition is additively separable.

## Estimand cells

| Cell | Exposure | Outcome | Expected population |
|---|---|---|---|
| **P1** | ART insurance mandate / public funding / reimbursement change | Births, birth rates, first births, parity progression | Small and identified; the 195-record mandate body is where it lives |
| **P2** | ART availability (clinic entry, distance, supply, legal eligibility) | Same | Thin — the probe's supply-side cell was almost entirely clinical noise |
| **P3** | ART utilisation (cycles, ART births) as measured | ART share of all births; contribution to TFR or completed fertility | Arm 1's core; 72 records under strict scoring, canon verified |
| **P4** | Postponement, with and without ART | Involuntary childlessness; completed fertility shortfall | Leridon, Habbema, te Velde — simulation studies, not estimates |
| **P5** | Elective egg freezing / oocyte cryopreservation availability | Later births, completed fertility | Likely near-empty; measured, not assumed |
| **P6** | ART availability | **Postponement itself** — the upper-bound channel | See below |

**P6 is the cell that decides how the chapter reads.** If the availability of ART induces some of the
postponement whose losses it then repairs, then part of arm 1's count is ART repairing damage
partly attributable to ART, and the bound tightens from above. The probe found the cell thin: 87
records on the moral-hazard/induced-delay framing, and the citation head is a *fertility-awareness*
literature (Lampic et al. 2006, 122 cites; Bretherick et al. 2010; Daniluk 2012, 287) showing that
young adults substantially **overestimate** ART's success rates. That literature establishes the
belief but does not estimate the behavioral response. **The mechanism is measured on the belief side
and unmeasured on the behavior side** — the same structure D.3.c hit, where the mechanism was
unmeasured in its own treatment literature. It is stated in the chapter as a signed, unquantified
bound rather than dropped.

## Anchor sourcing

Tier-A anchors are hand-sourced and are studies in their own right, not screen output — the D.2.d
lesson, where reporting screen output as the evidence base dropped 9 studies to 2. Verified live in
the probe and carried as the cold-start set:

*Arm 1:* Leridon 2004; Leridon and Slama 2008; Sobotka et al. 2008; Habbema et al. 2012 and 2015;
Lazzari, Gray and Chambers 2021.
*Arm 2:* Schmidt 2005; Bitler and Schmidt 2006; Jain et al. 2007; Hamilton and McManus 2011; Machado
and Sanz-de-Galdeano 2015; NBER w-series 2024.
*Exposure series:* ICMART world reports (Zegers-Hochschild et al. 2009, 1,860 cites); ESHRE European
IVF Monitoring, "ART in Europe" annual series (2018 edition, 648); CDC/SART ART Surveillance
(MMWR 2015, 530); ANZARD. Präg and Mills, "ART in Europe: usage and regulation in the context of
cross-border reproductive care" (2017, 124) covers the cross-border problem named in Call 3.

Two of v5's remembered citations did not resolve and should not be cited from memory:
"Assisted reproductive technology and the demographic transition" and "How much does ART contribute
to national birth rates" both returned zero on `title.search`. They are treated as unverified until
someone produces a DOI — the ghost-citation finding, applied.

## PI calls

1. **Does the chapter report arm 1 at all, given that it is a bound and not an estimate?**
   *RA recommendation: yes, both arms, with arm 1 explicitly labelled an upper bound and arm 2 a
   lower one.* Reporting only arm 2 discards the one well-measured quantity in the chapter;
   reporting only arm 1 states an upper bound as an effect, which is the B.5 error.
2. **Is elective egg freezing in scope?** v5's claim names it, but the literature is overwhelmingly
   oncological and the elective cell may be empty. *RA recommendation: in, tagged, and reported as
   empty if empty.*
3. **Cross-border reproductive care.** Registry series count treatments by clinic country, and births
   by residence country. For small countries with heavy outbound treatment flows the two denominators
   disagree, and the ART share of births is wrong in a known direction. Does the chapter correct,
   restrict to large countries, or report the discrepancy? *This is a scope decision, not an RA call.*
4. **The demographic-significance denominator.** ART births / all births, or ART's estimated
   contribution to TFR? These are different numbers and A.12's arm must be summable with whichever
   is chosen.
5. **Rate v5's claim as written, or amend?** v5 says ART raises TFR "relative to the counterfactual
   without ART" and puts the contribution at <5% of OECD births and growing. The <5% figure is
   arm 1's, i.e. a bound. Following the D.3.c and A.12 precedent, this chapter rates the claim as
   written and reports the distinction.

## What runs next

1. Cold-start anchor resolution and existence-verification over the Tier-A list (A3/A4 gates, with
   the first-author rule and the accent-folding fix both already in the shared resolver).
2. Tier-B frame construction on the **loose** vocabulary — ART × ACCESS (5,039) plus ART ×
   contribution-language, deduped.
3. Two-stage LLM screen with the taxonomy above, carrying `INSUFFICIENT_INFO` and `OFF_OTHER`, and
   an explicit arm-1/arm-2 routing field rather than a single relevance verdict.
