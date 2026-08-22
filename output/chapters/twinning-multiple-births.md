# Chapter A.12: Twinning Rates and Multiple Births

**Category:** Demographic / Biological (proximate determinant)
**Primary mechanism:** Not every pregnancy produces exactly one baby, so a population's births exceed its deliveries by the twinning rate — and any behavioural response to a twin birth partly gives that gain back.
**Cross-references:** A.17 (ART Access) · A.18 (Heritable Variation) · A.8 (Parity-Specific Stopping) · A.15 (Maternal Age) · B.5 (Fetal Loss)
**Status:** RA draft, 2026-08-22 (TICK-070). Not yet PI-reviewed. **Written on 68 of 253 wanted full texts (27%), including only 6 of the 14 primary-cell studies — see Provenance.**

---

## 1. The claim

### 1.1 In plain terms first

Start with a firm rather than a population. Suppose you want to explain why a factory's annual output of widgets fell by a third, and someone proposes: *the boxes got smaller*. That is a coherent proposal. Output is orders times units-per-order, so units-per-order is a real term in a real identity, and if it moved, output moved with it. But before doing any econometrics you would want to know two things. **How much can units-per-order actually move?** If it is always between 1.01 and 1.05, it cannot explain a one-third fall no matter how it behaves. And **does anyone respond to it?** If customers who accidentally receive two widgets order less next time, then even the movement you do observe is partly cancelled.

That is this chapter in full. Births are deliveries times babies-per-delivery. Babies-per-delivery is the twinning rate, it has never in any recorded human population strayed far outside 1.01 to 1.05, and parents who get two babies at once may well stop earlier. The first fact bounds how much A.12 can possibly explain. The second decides how much of that bound is even realised.

The economics reader has a ready-made name for the distinction that organises everything below. Deliveries are the **extensive margin** — how many times a woman becomes pregnant and carries to term. Twinning is the **intensive margin** — how many children each of those events yields. A.12 is the only hypothesis in this review that is purely and exclusively an intensive-margin story, and it is bounded by biology in a way that no extensive-margin hypothesis is.

### 1.2 The claim precisely

HYPOTHESES-v5 §A.12 states that variation in twinning rates — genetic across populations, and induced by **assisted reproductive technology (ART: IVF and related fertility treatment)** within the modern period — modestly affects the **total fertility rate** (TFR: the number of children a woman would bear if she experienced current age-specific birth rates throughout her reproductive life) by raising live births per pregnancy, "with ART-induced multiples partially offsetting postponement-driven SDT declines."

This decomposes into two claims that need entirely different treatment, and the registry entry runs them together.

**The mechanical claim is an accounting identity.** If a fraction *t* of deliveries produce twins, live births exceed deliveries by a factor of approximately (1 + *t*). This cannot be false. It requires no study, and — as the reconnaissance for this chapter confirmed rather than assumed — essentially no study estimates it. Identities get tabulated, not identified.

**The behavioural claim is a real parameter and the only place A.12 can be wrong.** The identity gives the effect on *births*. The effect on *completed fertility* — the number of children a woman actually finishes with — is smaller by whatever subsequent childbearing a twin birth displaces. If households target a family size, a twin birth overshoots the target and they stop earlier. The mechanical uplift is therefore an **upper bound**, and the size of the offset is the quantity worth estimating.

This chapter therefore estimates one parameter (the offset), computes one arithmetic quantity (the mechanical uplift), and reports a bounded verdict on their product.

## 2. Theoretical mechanism

### 2.1 The identity, and why it is not a hypothesis

Let *D* be deliveries and *t* the share of deliveries producing twins. Ignoring higher-order multiples, which are rare enough to be a second-order correction almost everywhere:

> Live births *B* = *D*(1 − *t*) + 2*Dt* = *D*(1 + *t*)

Recorded human twinning rates run from roughly 6 per 1,000 deliveries in historical East Asia to 45–50 per 1,000 among the Yoruba of south-western Nigeria, the highest rate ever documented. The multiplier (1 + *t*) therefore spans about **1.006 to 1.050** across the entire observed human record. That is the whole range within which this hypothesis operates, and it is fixed before any behaviour is considered.

An economist will recognise the structure: this is a decomposition, not a model. Writing *B* = *D*(1 + *t*) no more explains fertility than writing revenue = price × quantity explains revenue. What it does is bound the contribution of one term.

### 2.2 The behavioural offset, as an income effect

The interesting question is whether *t* and *D* are independent. They are not, if households have a target family size.

Frame it the way a labour economist frames a windfall. A couple who want two children and receive two in one delivery have met their target one birth early. The twin birth is an unanticipated positive shock to the stock of the thing they were accumulating, and the standard prediction is that they reduce subsequent accumulation. In demographic language, they **stop** — they cease progressing to the next **parity** (parity is simply the number of live births a woman has had). The offset is the derivative of subsequent births with respect to an exogenous twin birth, and it runs between 0 (no response; the full mechanical gain passes through) and −1 (complete offset; the twin birth is entirely absorbed and completed fertility is unchanged).

Three things make this parameter harder to estimate than it looks, and all three surfaced in the evidence.

**First, twinning is not random across women.** Dizygotic twinning — the kind that varies, from two eggs released and separately fertilised — rises steeply with maternal age, runs in families, and is elevated in taller and heavier women. (Monozygotic twinning, from a single embryo splitting, is roughly constant everywhere at about 3–4 per 1,000 and is not what varies.) So women who bear twins differ systematically from women who do not, in ways that also predict their fertility.

**Second, and this is the finding that reorganises the chapter, the naive comparison is subject to an exposure bias.** A woman who has six births has six opportunities to have twins; a woman who has two has two. Comparing "mothers who ever had twins" with "mothers who never did" therefore compares high-fertility women with low-fertility women *by construction*, before any biology is involved. This is a selection-on-the-dependent-variable problem of a particularly clean kind, and §5 shows that it has driven essentially the entire prior literature.

**Third, the fertility question and the population question are not the same question.** Even a complete offset at the individual level would leave the mechanical uplift intact in any single cross-section of births, because the offset operates on *subsequent* births — which is why the demographic-significance computation in §7 is done on the identity and not on the offset alone.

## 3. Search strategy

Gold-anchored clustered search following `canonical-search-workflow.md`; full logs at `literature/search-logs/twinning-multiple-births-*`, scope frozen 2026-08-22.

**The scope is unusual in one respect and it is worth stating.** Reconnaissance established before any screening that the primary cell would be populated by *vital-statistics reports* rather than estimation studies — the citation-ranked head of the primary probes is *Births: Final Data* and *Annual Summary of Vital Statistics*. That is the correct state of the world for an identity, and a screener expecting effect estimates would have read the cell as empty. It is not empty; it is a different kind of literature, and the chapter's mechanical arm is a computation run on it rather than a synthesis of it.

**Nine walls were frozen.** Three are pure homonyms with no on-topic content, and their scale is worth recording because it shaped every downstream cutoff: crystallographic twinning (a crystal lattice defect — *A short history of SHELX* alone has 87,676 citations and outranks every genuine A.12 record by two orders of magnitude), TWIP steel and "digital twins", and — found only at screening, enumerated by no probe — **photophysics, where "singlet" and "triplet" are excited states.** Each was measured rather than assumed: an exact count over SHELX's entire 87,673-record citation cloud found 13 records carrying any fertility vocabulary, a rate of 0.0%. TWIP steel returned 0 of 1,810.

**One wall was declared unenforceable in advance, and it governs the chapter.** Twin births are the canonical instrument for family size in economics — Rosenzweig & Wolpin (1980), Bronars & Grogger (1994), Black, Devereux & Salvanes (2005), Angrist, Lavy & Schlosser (2010). Every one of those papers estimates A.12's parameter *in its first stage* and reports it as a nuisance quantity on the way to a result about schooling or earnings. No abstract reveals a first-stage table. Measured on this chapter's citation frame: **of 1,991 records reached from a twin-IV canon seed, only 154 mention a twinning term at all.** Ninety-two per cent of this chapter's identification neighbourhood is invisible to a title/abstract screen, which is why those records were routed to full text rather than screened.

**One boundary was ruled at scope-freeze.** ART's contribution splits at the margin: ART live births = ART deliveries × (1 + *m*). **A.17 owns the deliveries; A.12 owns only the multiplier *m*.** The split is additively separable so the two chapters can be summed without double-counting — but it is an *accounting* split, not a causal one, and §8 downgrades the ART arm for exactly that reason.

## 4. PRISMA flow

| Stage | n |
|---|---|
| Cold-start anchors (existence-verified) | 25 |
| Tier B citation frame (one hop, forward + backward) | 8,701 |
| After normalised-title dedup | 8,342 |
| D1 deterministic rank → screening worklist | 1,376 |
| Title/abstract screen: RELEVANT | 441 |
| Title/abstract screen: UNCERTAIN (routed to full text) | 225 |
| Retrieval wantlist (rule-selected) | 253 |
| **Full texts readable** | **68 (27%)** |
| — of which primary-cell (offset) studies | **6 of 14** |

Three features of this funnel change how the chapter should be read.

**The primary cell is four times the size the anchor set implied.** Scope-freeze named three studies estimating the offset. The screen found **fourteen** — and the additions are not marginal. They include a published comment on the principal anchor *in the same journal*, a *Nature Communications* study reporting the opposite sign, a Swedish population-register study of the childbearing of mothers of twins, and a *Journal of Political Economy* paper whose outcome variable is time to next birth. Reporting the anchor set as the evidence base would have understated the cell fourfold and concealed that its members disagree.

**Retrieval is the binding constraint, and this chapter was selected on the belief that it would not be.** A.12 was chosen as the fastest remaining hypothesis because its demographic-significance stage runs on a public database rather than on PDFs behind a proxy. That remains true. But extraction of the *offset* is bound as tightly as any chapter in this review, and worst in the cell that carries the verdict: eight of the fourteen primary studies are unread, and all four of the methods surveys that would have opened the 223 first-stage candidates are closed.

**145 first-stage candidates were deliberately not retrieved.** They carry the IV-design vocabulary but no twinning term, and the set is known to contain sibling-sex-composition and one-child-policy designs with no twin first stage at all. This is the honest cost of a deliberately broad retrieval rule, and the synthesis below does not read them.

## 5. Included studies

Six primary-cell studies are readable. They divide cleanly by **design**, and the division explains the entire disagreement.

| Study | Setting | Design | Finding on twin mothers' fertility | RoB |
|---|---|---|---|---|
| **Rickard et al. 2022**, *Nat. Comms.* | >20,000 pre-industrial European mothers, multi-population | Controls exposure to twinning risk; individual-level | **Lower.** Odds of twinning × **0.967** (95% CI 0.952–0.983) per additional birth | **LOW** |
| Sear et al. 2001, *J. Evol. Biol.* | Rural Gambia, natural fertility | Naive comparison, ever-twinned vs never | Higher: shorter intervals, higher age-specific fertility, more surviving children | HIGH |
| Ekamper & van Poppel 2021, *Hist. Life Course Stud.* | Netherlands, 19th–20th c., HSN/LINKS | Naive comparison | Higher: earlier first birth, later last birth, longer span, higher lifetime fertility | HIGH |
| Hur et al. 2024, *Twin Res. Hum. Genet.* | Nigeria, 972 mothers of DZ twins vs 525 controls | Naive comparison | Higher: younger at first child, higher parity | HIGH |
| Hoem & Strandberg 2004, *Demographic Research* | Sweden, population register, 1961–99 | Within-register, matched on parity | **Longer waits; otherwise like mothers of two singletons** | MODERATE |
| Hoekstra et al. 2008, *Am. J. Med. Genet. A* | Netherlands, mothers of MZ/DZ/ART twins | Descriptive, ART arm separated | Higher (uncontrolled) | HIGH |

**Four of the six find that twin mothers are more fertile. All four use the naive comparison, and Rickard et al. demonstrate that the naive comparison cannot support the inference.**

Their argument is the exposure bias of §2.2, stated formally as an ecological fallacy: a mother's *lifetime twinning status* confounds her twinning **propensity** with her **exposure** to the risk of twinning, and exposure accumulates with the number of births she has. Their own analogy is exact — taxi drivers have more road accidents because they drive more, not because they drive worse. On more than 20,000 pre-industrial European mothers, once exposure is controlled, the sign reverses: women with higher per-birth twinning probability had **fewer** total births. And the mechanism they identify is precisely this chapter's parameter — "mothers were more likely to cease reproduction after a twinning event, irrespective of the underlying cause."

Hoem & Strandberg's Swedish register study is the only other design that escapes the bias, by comparing at fixed parity rather than over lifetimes. Their result is the behavioural prediction of §2.2 almost exactly: mothers of twins wait noticeably longer before the next child, and mothers whose first birth was a twin pair have subsequent fertility "very similar to women who have two singletons at their first two births." A twin birth is treated by the household as two children, which is what target-family-size behaviour predicts and what a pure biological-fecundity story does not.

**This resolves the disagreement rather than averaging it.** The four positive findings and the two corrected ones are not two readings of one parameter; they are one biased estimator and one unbiased one, and the bias has a known sign and a demonstrated mechanism.

**A citation-hygiene note belongs here rather than in a footnote.** HYPOTHESES-v5 lists "Hoekstra et al. 2008" among A.12's seminal works. The review it means is *Dizygotic twinning*, *Human Reproduction Update*, **2007**. There are at least **two** distinct Hoekstra 2008 papers a resolver can land on instead — the Dutch mothers-of-twins study in the table above, and *Body composition, smoking, and spontaneous dizygotic twinning* in *Fertility and Sterility* — and both are legitimate records on this exact topic. A wrong year that points at nothing is a nuisance; a wrong year that points at two real neighbouring papers by the same first author is a trap, because the resolver reports success.

**One caveat is load-bearing.** Rickard et al. is a pre-industrial European sample. Its transportability to the modern period — where contraception makes stopping cheap and effective, and where a large share of twins are iatrogenic — is untested, and the eight unread primary studies are disproportionately the modern ones.

## 6. Quantitative synthesis

### 6.1 The answer in plain terms first

Return to the factory. We want to know: when the boxes get bigger, does total output rise by the full amount, or do customers order less often and cancel part of it out?

The readable evidence says **customers do order less often, but only a little.** Of every ten extra babies that twinning mechanically adds, roughly nine survive the household's own response and one is given back through earlier stopping. The behavioural offset is real — it is not zero, and the households in the data do respond — but it is nowhere near large enough to cancel the mechanism. The identity is close to the truth.

That single sentence is the chapter's quantitative result. The rest of this section is how it was obtained and how much weight it will bear.

### 6.2 The estimate

Only one readable study yields a transportable estimate of the offset, so no pooling is possible and none is attempted. What Rickard et al. do provide is a simulation that converts their estimate into the quantity this chapter needs.

Holding everything else fixed and raising the twinning rate roughly tenfold, from 16.7 to 167 per 1,000 births, their simulated mothers end with:

| | baseline (t = 16.7‰) | 10× twinning (t = 167‰) |
|---|---|---|
| mean total **births** | 4.83 | **4.75** |
| mean total **offspring** | 4.91 | **5.54** |

Read the two rows together, because their difference is the whole result.

- The **mechanical** effect is the multiplier: (1 + 0.167)/(1 + 0.0167) − 1 = **+14.8%** on offspring per birth.
- The **behavioural** offset shows up as fewer births: 4.75 versus 4.83, or **−1.7%**.
- The **net** effect on completed offspring is +12.8%.

**The offset absorbs about 12% of the mechanical gain. Roughly 88% passes through.**

(The decomposition is in logs, which is why the three rows add: ln(1+t) rises by 0.138, ln(births) falls by 0.017, and ln(offspring) rises by 0.121. In levels the pass-through is 87%, which is the same answer.)

That is the chapter's central number, and its provenance should be stated plainly: it is one simulation, from one study, on one pre-industrial European sample, calibrated on a tenfold change in twinning far larger than any observed between real populations. It is an order of magnitude, not a pooled estimate. But its direction is unambiguous and it is the only such quantity the readable evidence supports: **the offset is real, it is small, and the identity is close to the truth.**

Three further corrections, each documented in the screen and each running in the same direction — the identity as written **overstates** — are not yet quantified and are carried to §10:

1. **Differential twin mortality.** Twins are about 2.4% of births in less developed countries but about 12% of neonatal deaths. Births per delivery is not surviving children per delivery.
2. **The vanishing twin.** Ultrasonography confirms that conceived multiple pregnancies exceed delivered ones. Seven readable records address this; one shows the correction is not even constant, since single-embryo-transfer pregnancies "practically lack vanishing twins."
3. **Twin infanticide and cultural suppression.** Where practised, realised twin contribution falls below the biological rate. This bites hardest on the pre-modern arm.

## 7. Demographic significance

The three target phenomena, for readers new to the vocabulary: **pre-modern (PM)** variation is the spread in fertility across populations before any sustained decline; the **First Demographic Transition (FDT, ~1870–1965)** is the fall from roughly 5–7 children per woman to about replacement; the **Second Demographic Transition (SDT, ~1965–present)** is the fall from replacement to well below it. "Replacement" is about 2.1 children per woman, the level at which a population reproduces itself.

**The plain-language version of this whole section, before any arithmetic.** The thing we are trying to explain is measured in whole children — populations differ by four children, and the modern decline is about one child. The thing A.12 offers is measured in percentage points of a multiplier that has never left the range 1.01–1.05. Those are quantities two orders of magnitude apart. The arithmetic below is not close, and it was never going to be: this is a case where knowing the *units* of the proposed explanation settles the question before any estimate is needed. What the arithmetic adds is the precise size of the gap, and one genuine surprise — that in the period v5 describes, the term is not merely small but moving the wrong way.

### 7.1 Pre-modern — **NEGLIGIBLE**

Take the extreme comparison the record allows: Yoruba Nigeria at 45–50 twin deliveries per 1,000 against historical East Asia at about 6. The multipliers are 1.048 and 1.006. The maximum difference in births per delivery between the highest- and lowest-twinning human populations ever recorded is therefore about **4.2%**.

Pre-modern fertility varies across populations by whole children — from roughly 4 to roughly 8. On a TFR of 6, a 4.2% multiplier difference is **0.25 children**, or about 6% of a 4-child range, and that is the extreme-versus-extreme comparison. For any typical pair of populations it is a fraction of one per cent. Apply the ~88% pass-through from §6 and net twin mortality, and it falls further.

Twinning cannot explain pre-modern fertility variation, and no arithmetic makes it a candidate. What the pre-modern twinning literature *is* good for is testing a different hypothesis: Clark, Cummins & Curtis (2020) use twin births to ask whether pre-transition populations practised parity-dependent stopping and conclude they did not. **That study is routed to A.8, where it is a first-order finding, rather than counted here as evidence for A.12.** Note that Rickard et al., on pre-industrial European data, find mothers *did* cease reproduction after a twin birth — a direct tension that A.8 rather than A.12 should adjudicate.

### 7.2 FDT — **NOT ASSESSED**

HYPOTHESES-v5 does not scope A.12 to the FDT and this chapter does not claim it. The relevant fact is that developed-country dizygotic twinning **fell** through most of the FDT and into the 1970s — a decline documented across eleven countries in the 1960s and in Sweden from the 19th century — so the sign of any FDT contribution is negative, not positive. Establishing its magnitude would require the long national series (Sweden from 1751, Australia from 1853) that are on the residual retrieval list.

### 7.3 SDT — **SMALL, TRANSIENT, AND NOW OF THE WRONG SIGN**

Here the registry entry is testable and here it fails, in three separate ways.

**The magnitude, at its maximum.** Czechia is the modal case: twin deliveries rose from under 10 per 1,000 in the early 1990s to over 21 per 1,000 by 2010. The multiplier moved from 1.010 to 1.021, a rise of **1.1%** in births per delivery. On a TFR of 1.7 that is **0.019 children**. Czech TFR fell by roughly one child over the same era. Twinning offset about **2%** of the decline at its own peak.

Globally the number is smaller still. The twin delivery rate rose from 9.1 to 12.0 per 1,000 between 1980–85 and 2010–15, moving births per delivery from 1.0091 to 1.0120 — a rise of **0.29% over four decades**.

**The direction, after 2010.** v5 describes the ART-multiples term in the present tense and as a growing offset. Every readable national series says that period closed:

| Setting | Peak | After |
|---|---|---|
| Sweden, IVF twinning rate | 29% (1991) | 18.5% (2001), −40% |
| Japan, iatrogenic multiples per 1,000 births | 11.4 (2005) | 8.1 (2009) |
| Czechia, twin deliveries per 1,000 | >21 (2010) | rapid decline after the 2012 rule mandating **elective single embryo transfer** (eSET — implanting one embryo per IVF cycle instead of two or three) |
| Iceland, twin birth rate | 1997–2002 baseline | prevalence ratio **0.74** (0.64–0.86) in 2009–13 and 2014–18 |
| US, twin share of ART-conceived infants | 38.0% (2014) | 34.0%, 30.4%, 25.5%, ~21% (2015–18) |

The US series is the sharpest: the twin share of ART infants nearly halved in four years. **For the post-2010 period the sign of v5's clause is wrong.**

**The attribution, which is worse than the sign.** Pison, Monden & Smits decompose the developed-country twinning rise into two sources — delayed childbearing and medically assisted reproduction — and find MAR about three times the age effect. The remaining quarter is the maternal-age composition shift. But **postponement is the SDT mechanism that A.12's clause is supposed to offset.** That quarter is not an independent force acting against the decline; it is a mechanical consequence of it. A feedback of a decline cannot be evidence against the decline's cause, and only the MAR component is even a candidate offset.

Nor is the MAR component a clean lever. Two independent meta-analyses find ART *raises* monozygotic twinning through embryo splitting, a route that transferring one embryo does not close; the Czech data attribute international heterogeneity in twinning "primarily to differences in national ART practices rather than the overall volume of ART treatment"; and ovulation induction *outside* IVF causes 40–70% of high-order multiples, a channel single-embryo-transfer policy does not touch at all.

## 8. GRADE rating

GRADE is the standard scheme for rating how much confidence a body of evidence supports, running HIGH / MODERATE / LOW / VERY LOW. Ratings start from the study designs available and are *downgraded* for specific defects — imprecision, risk of bias, indirectness (the evidence answers a neighbouring question rather than the one asked).

| Phenomenon | Certainty | Reasoning |
|---|---|---|
| **PM** | **HIGH** for a negligible effect | The bound is arithmetic and needs no study. The offset estimate is weak, but no plausible offset value changes a verdict of "negligible" when the mechanical ceiling is 4.2% at the extreme. |
| **FDT** | **NOT ASSESSED** | Out of scope in v5; the sign is negative if assessed. |
| **SDT** | **LOW** | Downgraded three steps. **Indirectness:** the intensive margin is not identified — *m* is chosen by clinicians and patients, jointly determined with ART uptake, and "TFR without ART multiples" is not a ceteris-paribus counterfactual, so the ART arm yields a measured *share* rather than an estimated effect. **Imprecision:** one offset estimate, from one pre-industrial sample, extrapolated to the modern period. **Risk of bias in the body as a whole:** four of six readable primary studies use an estimator demonstrated to be biased. |

The offset parameter itself is rated **LOW**: one low-risk-of-bias study against four high-risk ones whose design it refutes, with eight of fourteen primary studies unread.

## 9. Verdict

**A.12 is true, small, and — for the period v5 describes — pointing the wrong way.**

The mechanical arm cannot be wrong and does not need defending. It is bounded by biology at roughly 1.01–1.05 babies per delivery across the entire human record, which makes it too small to explain any of the three target phenomena. Pre-modern: **negligible**, at most 6% of the observed range under the most extreme comparison available and a fraction of a per cent typically. SDT: **about 2% of the decline at its own historical peak**, and negative since roughly 2010.

The behavioural arm is where the hypothesis could have been wrong, and the readable evidence says it is not, but by a smaller margin than the prior literature suggested. The offset is **real but partial** — roughly 12% of the mechanical gain absorbed, about 88% passing through. The published consensus that twin mothers are simply more fertile is an artefact of an exposure bias that the one study correcting for it reverses outright.

Three qualifications belong in the verdict rather than beneath it. **The identity overstates**, for three separate documented reasons — twin mortality, vanishing twins, cultural suppression — none of which is yet quantified and all of which cut the same way. **The registry entry's ART clause is defective in three independent ways at once**: time-inverted, unidentified, and one-quarter composed of a feedback from the very postponement it claims to offset. And **the chapter is written on 27% of its wanted evidence**, with the primary cell at 6 of 14, so every number above is provisional in a stated direction: the unread studies are disproportionately modern, and the modern period is where the offset is most likely to be large.

A precisely bounded negative is a deliverable. This one is bounded, and it is negative.

## 10. Open questions and recommended studies

**Five for the PI.**

1. **The scope has no cell for the intergenerational channel, and it needs one.** Two PNAS papers, twelve years apart, report that prenatal testosterone transfer from a male co-twin *reduces the female co-twin's later fertility*; a third study finds a null. If real, twinning lowers the *next* generation's fertility, so the mechanical uplift is partly undone one generation later. This is a scope amendment, not an RA call.
2. **Should the mechanical arm be computed on surviving children rather than live births?** The three attrition corrections all run the same way. This is structurally the (1−p) accounting error that B.5 shipped, and A.12's own scope named that error as its governing constraint before finding it again.
3. **Do twin-IV first stages count as included studies?** 223 candidates, 145 of them deliberately unread, and four closed methods surveys standing between the chapter and the rest.
4. **Rate v5's ART clause as written, or amend the registry?** This chapter rates it as written and reports the inversion, following the D.3.c precedent.
5. **Does the PM arm survive as anything more than a bounded arithmetic statement?** This chapter says no, and routes Clark, Cummins & Curtis to A.8.

**Retrieval, in priority order.** P0: the eight unread primary studies, especially Alter & Hacker (2024, *Demography*) and Robson & Smith (2012, *Proc. R. Soc. B*), the latter being the paper Rickard et al. effectively overturn. P1: the four methods surveys — an Oxford handbook chapter on twins methods in economics, Rosenzweig & Wolpin's own JEL review of natural experiments, a *Journal of Economic Surveys* review, and a twins-data methods paper. Four PDFs there are worth more than forty anywhere else on the list.

**One study that does not exist and should.** No one has estimated the offset on modern register data with the Rickard et al. exposure correction. Sweden, Denmark and Finland all have the linked registers to do it, and Hoem & Strandberg (2004) is the design sitting one step away.

## 11. References

Full bibliography at `literature/bib/`. Records readable in full text at `literature/pdfs/twinning-multiple-births/`; the retrieval log and banded procurement list are at `extraction/twinning-multiple-births-pdf-retrieval-log.csv` and `literature/search-logs/twinning-multiple-births-library-wantlist.md`.

---

### Provenance and standing caveats

**Written on 68 of 253 wanted full texts (27%).** The primary cell — the only cell earning GRADE credit — is at **6 of 14**, and its readable members disagree with each other. Retrieval failed not because the papers are closed but because 84 of 88 first-pass failures were HTML interstitials, a blocked route rather than a closed paper; a recovery rung reclaimed 14.

**The synthesis was written under an explicit objection.** The RA's stage-5 note recommended holding synthesis until the P0 and P1 procurement bands were filled, on the grounds that a spine at 6 of 14 with members in open disagreement risks settling that disagreement by accident of retrieval. Writing was directed anyway. The risk is concrete and stated here rather than buried: **Rickard et al. 2022 carries the §6 estimate almost alone, and the two studies most likely to contest it — Robson & Smith 2012, which it targets, and Alter & Hacker 2024, the only study designed squarely on the estimand — are both unread.**

**What is *not* provisional.** The mechanical bound in §7.1 and §7.3 rests on arithmetic and on twinning-rate series, not on the unread studies, and no plausible offset value overturns it. The direction of the post-2010 reversal rests on five independent national series, all readable. Those two findings would survive full retrieval; the offset magnitude in §6 might not.

**Numbers sourced from abstracts rather than full text** are marked as such in the search logs; the global 9.1→12.0 per 1,000 series and the Pison–Monden–Smits three-to-one decomposition are from the abstracts of record, verified live at scope-freeze, and both are on the residual retrieval list.
