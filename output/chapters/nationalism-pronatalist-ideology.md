# Chapter D.1.d: Nationalist and Pronatalist Ideology

**Category:** Cultural
**Primary mechanism:** The state frames childbearing as a patriotic or national duty — through propaganda, rhetoric, and honours for large families — and citizens who internalise the framing have more children than they otherwise would.
**Cross-references:** C.2.d (Tax and Transfer Pronatalism — the money the ideology is bundled with); A.4/A.2 (Abortion / Contraception — the coercion the ideology is confused with); D.1.a (Postmaterialism, Individualism, and Secularization — the diffuse, opposite-signed value shift); A.20 (Cultural Diffusion Mechanisms — the channels that carry the message); C.3.c (Old-Age Security — one economic root/motive).
**Status:** TICK-093 · drafted 2026-09-26 · **not PI-reviewed** · written on 4 of 19 identified-core full texts (21%).

## 1. The claim

This chapter explores the effect of state-sponsored nationalist and pronatalist ideology on realized fertility.

### 1.1 In plain terms

In plain terms: sometimes a government tries to get people to have more children not by paying them and not by banning birth control, but by *persuading* them that having children is a duty to the nation — through propaganda posters, patriotic speeches, medals for mothers of large families, and warnings that the nation will shrink without them. The claim is that this message, on its own, makes some couples who would have stopped have another child. This chapter asks whether that is true, and how much it matters — and the hard part, which runs through everything below, is that governments almost never try only persuasion: they hand out cash and restrict abortion at the same time, so the persuasion has to be separated from the money and the coercion before we can say the message did anything.

The test that would prove the claim wrong: if fertility rises only when the government also pays families or restricts abortion, and does not budge when the message is delivered without those, then the ideology on its own does nothing.

### 1.2 Technically

The parameter this chapter estimates is the change in realized fertility caused by state-sponsored pronatalist ideology, holding financial transfers and coercive fertility-control restrictions fixed, measured in births per woman.

The exposure is the *ideational* instrument specifically — propaganda, patriotic-duty framing, honorific awards, the rhetorical construction of childbearing as a national project — not the fiscal instruments (child allowances, baby bonuses, parental leave, childcare) that belong to **C.2.d**, and not the supply restriction of abortion or contraception that belongs to **A.4/A.2**. The counterfactual is the same population, with the same budget constraint and the same access to fertility control, not exposed to the pronatalist message. The outcome of first interest is *completed* (cohort) fertility — the number of children a woman actually finishes her reproductive life with — because the registry's own qualifier is that pronatalist effects are "modest and mostly transient," and a transient effect is one that moves the *timing* of births (a **tempo** effect) without changing the completed total (the **quantum** effect). This is a behavioural parameter, not an accounting identity: the ideology can only work by changing what couples choose, so the place it can be false is in that behavioural response. The margin is the intensive one — an extra birth to a couple that would otherwise have stopped — rather than the extensive margin of whether to have any children at all.

## 2. Theoretical mechanism

The mechanism is a preference-shifter operating through norms rather than through the budget constraint. In the reader's vocabulary: **C.2.d changes the price of a child; D.1.d tries to change the taste for children.** A pronatalist state uses propaganda and honours to raise the psychic return to childbearing — to make an additional child feel like a contribution to a valued collective (the nation, the ethnic group, the race) rather than a private consumption-versus-cost decision. If citizens internalise the framing, their desired number of children rises, and realized fertility follows. Demeny's (1986) comparative assessment of pronatalist policy, Quine's (1996) history of interwar population politics, and King's (1998) study of French pronatalism-as-nationalism are the formative statements: each treats the ideology as a deliberate state project distinct from, though usually paired with, material inducement.

There is no accounting identity here, so the whole hypothesis lives in the behavioural response, and there are three ways it can be — and empirically tends to be — confounded into invisibility:

- **The transfer confound (the load-bearing one).** Pronatalist campaigns travel with money. A regime that exhorts also pays, so a fertility rise after a campaign is consistent both with the message working and with the cash working. Separating them requires either a setting where the message moved without the money, or a design that measures the ideational mediator (desired fertility) directly.
- **The coercion confound.** The most dramatic historical "pronatalist" fertility responses — Ceausescu's Romania after Decree 770 (1966), Hungary after the 1953 abortion ban — were produced by *removing* the means of avoiding birth, which is an **A.4** supply restriction, not persuasion. The propaganda that accompanied the ban is D.1.d only if its effect can be read off separately from the ban.
- **Reverse causality.** Demographic decline is itself a powerful *cause* of pronatalist politics: states adopt pronatalism *because* fertility is low. So a cross-section showing that pronatalist regimes have low fertility has the arrow backwards, and even a before/after comparison is contaminated unless the exposure is assigned independently of the fertility trend.

What would make the hypothesis wrong, stated as the mechanism predicts: if exposure to pronatalist ideology raises fertility **without** raising the desired number of children, the effect is not running through the taste-shift the theory posits — it is running through something else (money, coercion, or a constraint the campaign happened to relax). Hold that test in mind; the cleanest study in the literature runs exactly it.

## 3. Search strategy

Reproducible from `source/build/goldset/89_d1d_frame_probe.py` through `96_d1d_assemble_screen.py`; the scope is `literature/search-logs/nationalism-pronatalist-ideology-search-scope.md`.

The retrieval frame was built by a stage-3 **frame probe** that priced every candidate term as a marginal gain over a baseline (the A.6/A.3 lesson: never charge a frame by a term's own size). The honest production frame is **1,751 records** — below the review's ~1,808 "smallest unstarted candidate" bar, confirming the selection of D.1.d as the next-smallest genuinely-unstarted hypothesis. One instructive correction: the term `natalism` inflated the first frame to 4,374, but 22% of its records were the perinatal *medical* literature (neonatal/prenatal/postnatal) leaking in through stemming; it was dropped, along with the redundant `pro-natal` (which folds to `pronatalism`), while `natalist` was kept (clean). The completeness test confirmed that the genuine registered constructs (`patriotic duty`, `national duty`, `population campaign`) add essentially nothing to the frame, while the tempting generic words are free-`OR` inflaters that annex neighbour literatures and were excluded: bare `national` (+38,040 — national income, "national fertility rate"), `population policy` (+2,339 — family planning), `propaganda` (+304 — including anti-natalist family-planning propaganda, the opposite sign).

Two production channels were merged: a keyword frame (2,217 records) and a citation frame (693 records, forward- and backward-seeded from ten existence-verified anchors — Demeny 1986, King 1998, Fargues 2000, plus wall decoys). The merged 2,867 records were screened blind by a title/abstract classifier (Claude Haiku, 72 batches) that routed each record to one of the estimand cells or to a boundary wall.

**Walls and their enforceability.** Six walls were declared in advance. The two load-bearing ones — **C.2.d** (transfers) and **A.4/A.2** (abortion/contraception coercion) — are declared *only partly enforceable at the screening stage and not at all at the estimand stage*: the screen can route a paper that is purely about cash to C.2.d, but it cannot separate the ideology from the money *inside* a study that bundles them, and most do. That un-enforceability is not a defect of the search; it is the central finding of the chapter, and it is why two "MIXED" cells (ideology+transfer, ideology+coercion) were created to hold the bundled studies as explicit upper bounds rather than silently crediting them to ideology. The screen absorbed 179 records to C.2.d, 51 to A.4/A.2, 64 to religiosity (→D.1.a), 43 to secularization (→D.1.a), 11 to A.20, 17 to C.3.c, and 51 to a REVERSE cell (fertility decline → pronatalist politics).

## 4. PRISMA flow

| Stage | Records |
|---|---|
| Identified (merged keyword + citation frame) | 2,867 |
| Screened (blind title/abstract) | 2,867 |
| RELEVANT (T1) | 478 |
| Pooling set (RELEVANT ∩ PRIMARY-or-MIXED ∩ non-review/theory) | 159 |
| — clean primary (ideology isolable) | 60 |
| — bundled/MIXED (ideology + transfer or + coercion; upper bounds) | 99 |
| Identified core (natural experiment or framing experiment) | 19 |
| Full-text retrieved and extracted | **4** |

Three features of this funnel change how the chapter should be read. First, the pooling set is dominated by the **MIXED** cells (99 of 159): the modal study is a bundle, exactly as the mechanism section warned. Second, the **clean primary** identified evidence is thin, and much of it is very recent framing experiments whose outcome is an *attitude or intention*, not a birth. Third, the retrieval fraction is low (4 of 19 identified core) because the marquee clean-ideology studies are OSF/Zenodo preprints requiring browser navigation, and the historical coercion canon is paywalled — both are on the RA proxy/ILL handoff (`extraction/nationalism-pronatalist-ideology-missing-pdf-dois.csv`).

## 5. The ideal design

### 5.1 The ideal estimand

The change in completed cohort fertility, in births per woman, caused by exposure to a state pronatalist-ideology campaign — propaganda, patriotic-duty framing, honours — among women of reproductive age at exposure, **holding constant** the household budget constraint (no coincident transfer) and access to abortion and contraception (no coincident restriction), observed to the end of the reproductive span (age 45). "The effect of pronatalism on fertility" is not an estimand; this is.

### 5.2 The design that would identify it

The **source of variation** would be differential exposure to a pronatalist campaign that is itself assigned independently of local fertility trends — for example, the staggered geographic rollout of a state propaganda apparatus (radio/TV reach, poster campaigns, patriotic-motherhood ceremonies) whose timing is driven by infrastructure or administrative boundaries rather than by where fertility is falling fastest — with **no** coincident change in family benefits or abortion law. The **comparison group** is equivalent regions reached later or not at all. The **identifying assumption**, falsifiable via pre-trends, is that treated and control regions were on parallel completed-fertility paths absent the campaign. The **estimating equation** is a difference-in-differences (or event study) on cohort completed fertility, with the campaign's intensity as the treatment. The **data required** are cohort-fertility histories long enough to observe completion, linked to campaign exposure; the **sample** must be large enough to detect the "modest" effect the registry anticipates — on the order of a tenth of a child. Critically, the design must also measure the **ideational mediator** (desired number of children) directly, so that a fertility response can be attributed to a taste-shift rather than to an unmeasured constraint.

### 5.3 The distance table

| Study | Exposure | Outcome | Horizon | Assignment | Distance from ideal |
|---|---|---|---|---|---|
| **Aksoy & Billari 2018** (Turkey RDD) | Islamist pronatalist *rule* (ideology + welfare bundle), not ideology alone | Realized births (quantum) + marriage | Medium (2006–2013) | **Ideal-class** (exogenous close elections, passes McCrary + placebo) | Closest on assignment; **fails on exposure** — identifies the bundle, and its own mediation routes the effect to transfers with a null on the ideational mediator |
| **Tang, Wong & Batzorig 2022** (Mongolia DiD) | "Mother Hero" honour bundled with doubled cash annuity | Birth probability, 2-yr window (tempo/quantum not separable) | Short | Reform-based DiD (two cross-sections 8 yrs apart) | Targets the registered "honorific award" instrument, but empirically identifies the money |
| **Validova 2021** (Russia decomposition) | 2007 maternity-capital package (transfer + rhetoric) | TFR, decomposed tempo vs quantum | Medium | None (nationwide, no control) | Strong on the tempo/quantum question, weak on identification and on isolating ideology |
| **Wang 2026** (Russia narrative) | Same package | TFR, births | Long series | None (narrative) | Far — background only |

No study matches the ideal on exposure. The gap is itself the chapter's finding: **there is no study that identifies the effect of pronatalist ideology on fertility with the transfer and coercion channels held fixed.** The closest on *assignment* (Aksoy-Billari) is, for our estimand, the most informative precisely because it can test the mediator — and the mediator test fails.

## 6. Included studies

| Study | Setting | Design | Effect (as reported) | RoB (for its own estimand) |
|---|---|---|---|---|
| Aksoy & Billari 2018 (AJS) | Turkey, 2004→2013 | Close-election RDD | Islamist rule: +0.14 births/woman (SE .07); a-GFR +7.75 (SE 3.86); via health-insurance +0.28; **null on ideal children (0.12, n.s.) and religiosity (0.05, n.s.)** | LOW (for the rule effect) |
| Tang, Wong & Batzorig 2022 (IUJ WP) | Mongolia, 2010 vs 2018 | DiD (LPM) + PSM | Award reform: +4.3/+2.3/+2.6 pp birth prob. at parities 1/2/3; **null at higher goals** | MODERATE |
| Validova 2021 (CPoS) | Russia, 2007–2017 | Period decomposition | 2007 package: **91% tempo / 9% quantum**; TFR 1.30→1.78→1.57 | SERIOUS |
| Wang 2026 (in Russian) | Russia, 2003–2023 | Narrative time-series | Rise mainly structural (cohort); policy mostly tempo | CRITICAL (background) |

**The naive estimator, and its bias.** The comparison an author reaches for without thinking hard is *pronatalist regimes/periods versus others* — do states that push pronatalism have higher fertility? This estimator is biased in a **known, negative** direction by reverse causality: states adopt pronatalism *because* their fertility is low, so the naive cross-section shows pronatalist regimes with *lower* fertility (Aksoy & Billari report exactly this — near-zero-to-negative raw correlations at province, district and individual level, p.1314). A researcher who stops there wrongly concludes pronatalism reduces fertility. The RDD reverses the sign by making exposure as-good-as-random. This is the A.12 lesson in a different literature: the bodies do not disagree about one parameter; the naive and the identified estimators measure different things, and averaging them would manufacture a false near-zero. The correct synthesis discards the naive correlation and reports the identified estimate — while noting that the identified estimate is of the *bundle*, not the ideology.

## 7. Quantitative synthesis

The evidence is not poolable: the estimands are heterogeneous (a birth-per-woman RD coefficient, a tempo/quantum share, a two-year birth-probability change) and every one bundles ideology with transfers or coercion, so a pooled number would average incommensurable and confounded quantities. The synthesis is narrative.

### 7.1 The answer in plain terms

In plain terms: when a pronatalist government comes to power, births do go up — but when researchers look closely at *why*, the increase comes from the things the government spends money on (health insurance, cash), not from people wanting more children. In the one place this was tested directly — Turkey, where a party with an openly pro-family, religious-nationalist platform barely won some local elections and barely lost others — fertility rose in the places it won, but the people there did not say they wanted more children than before, and were not more religious than before; what changed was that they got health coverage. In Russia, the much-publicised post-2007 baby increase turned out to be mostly people having children *sooner*, not *more* children, and it faded after 2015. In Mongolia, a medal-plus-cash award for large families raised births a little — but no one could tell whether it was the medal or the cash, and the effect shrank, not grew, as the medals got more prestigious. And the newest studies that test the pure message — telling people their nation is shrinking — move their stated *attitudes* about childbearing without yet showing a single extra birth. So the honest summary is: the message, separated from the money, has not been shown to produce children.

### 7.2 The estimate

The four full-text studies, read against the estimand:

- **Aksoy & Billari (2018)** is the decisive study. A close-election regression-discontinuity design (comparing districts where an Islamist, explicitly pronatalist party barely won to those where it barely lost — an "as-if-random" assignment) finds local Islamist rule raised individual fertility by **+0.14 births per woman** (SE .07) and district fertility by **+7.75 per 1,000 women** (SE 3.86), with higher marriage rates. This is real and cleanly identified. But the paper's mediation analysis then dismantles the *ideological* reading: the effect runs through a large expansion of **General Health Insurance** (+0.28 probability, which in turn raises births), is concentrated in poor provinces, and shows a **null effect on the ideal number of children** (RD 0.12, SE .24, p=.61) and a **null effect on individual religiosity** (RD 0.05, SE .06, p=.38). Fertility rose without the taste for children rising — precisely the pattern §2 said would falsify the ideational mechanism. Marriage effects, moreover, decline over time and are projected to vanish by ~2020, so even the proximate channel is partly tempo.
- **Validova (2021)** decomposes Russia's post-2007 TFR rise into **91% tempo and 9% quantum** overall (the quantum share growing with birth order: 1%, 13%, 42% at parities 1, 2, 3), with the period TFR rising 1.30→1.78 and then falling to 1.57 by 2018. The durable (quantum) component is small and, being produced by a cash-and-rhetoric package with no control group, cannot be attributed to the rhetoric rather than the cash. The author's own conclusion is that "the principal tools ... remain financial."
- **Tang, Wong & Batzorig (2022)** evaluate Mongolia's "Order of Glorious Mother" — the honorific-medal instrument the D.1.d claim names explicitly — and find birth-probability rises of +4.3/+2.3/+2.6 pp at low parities, but a **null** at the higher-prestige six-child goal despite a larger prize, and negatives where the old award was cancelled. Because the medal is bundled with a doubled cash annuity, the study identifies the money, not the honour; the registered "award" instrument is, empirically, a transfer. The two-year outcome window cannot separate tempo from quantum.
- **Wang (2026)** is a descriptive narrative arguing Russia's rise was mainly structural (the large 1980s cohorts reaching peak reproductive age), with policy effects mostly on timing. It carries no estimate and is background only.

Beyond the read set, the identified core (abstract level) reinforces the picture: the historical FDT-era cases (**Ceausescu's Romania, Hungary 1953, Zimbabwe's Depo-Provera ban**) all bundle pronatalist ideology with an abortion/contraception restriction — they are A.4 coercion effects wearing pronatalist rhetoric — and the newest **framing experiments** (Israel ethnic-threat; "Guns vs. Wombs," South Korea; Christian-nationalism, US) randomise a national/demographic-duty message and move pronatalist *attitudes and intentions*, but none yet demonstrates an effect on realized fertility. The direction across the whole body is consistent (pronatalist regimes/policies in power are associated with higher fertility); the *mechanism*, wherever it has been tested, is not the ideology.

## 8. Demographic significance

The phenomenon to be explained is measured in the fall in completed fertility across the transition — on the order of one child per woman over the Second Demographic Transition (SDT, the fall in completed fertility from roughly 1965 to the present); this mechanism offers, at most, localised and largely temporary fractions of a birth per woman, of which the part attributable to ideology rather than to money or coercion is unidentified and, where directly tested, zero.

That units comparison largely settles the question before any share is computed: a mechanism whose *identified* magnitude is a local tenth-of-a-child (and whose ideology-specific component is not distinguishable from zero) cannot account for a phenomenon denominated in whole children per woman. The per-phenomenon verdicts:

### 8.1 Pre-modern

For pre-modern variation, the verdict is **NOT ASSESSED**, because organized nationalist-pronatalist ideology is a modern-state phenomenon with no pre-modern expression — the cell is out of scope in the registry (which lists FDT/SDT only), not empty-but-in-scope. Were it assessable, the sign would be nil: there is no pre-modern state pronatalist apparatus to have had an effect.

### 8.2 First Demographic Transition

For the FDT (the fall in completed fertility across the transition, roughly 1870–1965), the verdict is **NOT ASSESSED**, because no retrieved study isolates an FDT-window effect of pronatalist ideology: the famous interwar and mid-century cases (Fascist Italy's "Battle for Births," Nazi and Soviet natalism, the Eastern-European pronatalist programmes) are documented but were not full-text retrieved, and where their effects are cited they are inseparable from coincident abortion bans (A.4) and transfers (C.2.d). Were it assessed, the sign would be a small positive, and — on the consistent evidence that such effects are tempo-dominated and reversible — most likely NEGLIGIBLE-to-MINOR against the roughly two-to-three-child FDT decline; the interwar campaigns conspicuously failed to reverse the transition in any country. No share is computed because no numerator in the read set shares units with the denominator; this is recorded as NOT ASSESSED rather than softened to NEGLIGIBLE.

### 8.3 Second Demographic Transition

For the SDT, the verdict is **NEGLIGIBLE**, because the ideology channel's identified contribution is not distinguishable from zero, and the largest *aggregate* pronatalist effect that is cleanly identified is a local one-seventh of a child (Turkey, +0.14 births/woman) that runs through welfare, not framing. Taking that as an upper bound and dividing by the SDT denominator — a fall of roughly one child per woman in completed fertility since 1965 (numerator: +0.14 births/woman, local, transfer-driven; denominator: ≈1 birth/woman; source: cohort completed-fertility series for the relevant middle-income settings; window: 1965–present) — gives ≈14% *only if* the effect were global and attributable to ideology, and it is neither: it is confined to the districts an Islamist party governed, and its own mediation assigns it to health insurance. The ideology-specific share is below 5% (indeed, indistinguishable from zero), and Russia's much larger apparent effect is 91% tempo and reversed after 2015. Pronatalist ideology has nowhere durably reversed the SDT. The break-even statement for a reader with a global denominator: even the most generous reading of the identified magnitude clears only a MINOR band, and only by mis-attributing a transfer effect to ideology; the honest ideology-specific verdict is NEGLIGIBLE.

## 9. GRADE rating

Rated per phenomenon for the causal claim that pronatalist *ideology*, net of transfers and coercion, raises fertility (`extraction/nationalism-pronatalist-ideology-grade.json`; 3 independent raters).

| Phenomenon | Rating | Downgrades named |
|---|---|---|
| Pre-modern | **No evidence** | Cell out of scope / empty — no body of evidence exists to rate (not Very low). Pairs with NOT ASSESSED. |
| FDT | **Very low** (2/3; one No evidence) | Risk of bias (descriptive/poorly-identified historical cases); indirectness (the cases bundle ideology with abortion bans and transfers); no isolation of the ideology channel. |
| SDT | **Very low** (2/3; one Low) | Indirectness (the strong designs identify the pronatalist-rule/policy *bundle*, and the one clean mediation test routes the effect to welfare with a null on the ideational mediator); risk of bias (the transfer/ideology confound is SERIOUS in every study); imprecision/transience (the largest decomposed effect is 91% tempo and reverses). |

No cell shows a greater-than-one-level disagreement, so no GRADE-panel escalation to the PI is triggered. The dominant downgrade throughout is **indirectness**: the review's question is the ideology channel, and the literature — even at its most rigorous — identifies the bundle.

## 10. Verdict

**Nationalist and pronatalist ideology is a real state project with, so far, no demonstrated power to raise fertility on its own.** Pronatalist regimes and policies in power are reliably associated with somewhat higher fertility, and the association survives clean identification (a close-election natural experiment in Turkey). But wherever the *mechanism* has been tested, the fertility gain runs through the material inducements — health insurance, cash transfers — that accompany the ideology, not through the ideology itself: the one direct test of the ideational channel finds no shift in the desired number of children. The larger apparent effects (Russia) are mostly a change in the timing of births, not the total, and fade. The instrument the claim names most specifically — honours for large families — turns out, on examination, to be a cash transfer with a medal attached. The single number to carry away: in the cleanest study, pronatalist-ideological rule raised fertility by about **one-seventh of a child per woman**, and **none of it** is attributable to the ideology once the welfare channel is accounted for.

| | Causal credibility (GRADE) | Demographic significance |
|---|---|---|
| Pre-modern | No evidence | NOT ASSESSED (out of scope) |
| FDT | Very low | NOT ASSESSED |
| SDT | Very low | NEGLIGIBLE |

What would change the verdict: a study that moves pronatalist rhetoric while holding transfers and abortion access fixed and measures *completed* fertility — and finds a quantum effect. No such study yet exists.

## 11. Open questions and recommended studies

- **Retrieve the clean-ideology preprints (highest priority).** The three framing experiments (Israel ethnic-threat; "Guns vs. Wombs," South Korea; Christian-nationalism, US) are the only studies that manipulate the *message* alone. They are OSF/Zenodo preprints requiring browser/API navigation. They currently move attitudes/intentions only; whether any links the manipulation to a realized birth is the question that would most change this chapter.
- **Retrieve the FDT coercion canon** (Ceausescu's Romania; Hungary 1953; the Eastern-European pronatalist programmes; Fascist/Nazi natalism) via the UChicago proxy/ILL, and re-route the abortion-ban component to A.4 so the residual ideology component (if any) can be isolated.
- **PI calls.** (1) Confirm the routing of the Mongolia "Order of Glorious Mother" study to C.2.d, given the honorific instrument is registered under D.1.d but empirically identifies the cash. (2) Confirm FDT as NOT ASSESSED versus a MINOR sign-only verdict once the coercion canon is read. (3) Confirm treatment of religious-nationalist rule (Turkey AK Parti) as in-scope for D.1.d given the mediation routes it to transfers.
- **The study that should exist:** a staggered-rollout design on a pure propaganda apparatus (poster/broadcast campaigns assigned by infrastructure, no coincident benefit change), with cohort completed fertility as the outcome and desired fertility measured as the mediator. Until it exists, the ideology channel is unidentified.

## 12. References

- Aksoy, C. G., & Billari, F. C. (2018). Political Islam, Marriage, and Fertility: Evidence from a Natural Experiment. *American Journal of Sociology*, 123(5), 1296–1340.
- Demeny, P. (1986). Pronatalist Policies in Low-Fertility Countries: Patterns, Performance, and Prospects. *Population and Development Review*, 12(Suppl.), 335–358.
- Fargues, P. (2000). Protracted National Conflict and Fertility Change: Palestinians and Israelis in the Twentieth Century. *Population and Development Review*, 26(3), 441–482.
- Gauthier, A. H. (1996). *The State and the Family: A Comparative Analysis of Family Policies in Industrialized Countries*. Oxford: Clarendon Press.
- King, L. (1998). "France Needs Children": Pronatalism, Nationalism and Women's Equity. *The Sociological Quarterly*, 39(1), 33–52.
- Quine, M. S. (1996). *Population Politics in Twentieth-Century Europe: Fascist Dictatorships and Liberal Democracies*. London: Routledge.
- Tang, Wong & Batzorig (2022). Do Financial Incentives on High Parity Birth Affect Fertility? Evidence from the Order of Glorious Mother in Mongolia. IUJ Working Paper EMS-2022-01.
- Teitelbaum, M. S., & Winter, J. M. (1985). *The Fear of Population Decline*. Academic Press.
- Validova, A. (2021). Pronatalist Policies and Fertility in Russia: Estimating Tempo and Quantum Effects. *Comparative Population Studies*, 46, 425–452.
- Wang, ZiRui (2026). Fertility in Russia at the Turn of Eras: Dynamics and Mechanisms of Demographic Change (2003–2023). *Theory and Practice of Social Development*, No. 3, 84–89 [in Russian].
- *Abstract-level (not full-text read; RA retrieval backlog):* Ceausescu's Romania fertility-policy studies; Hungary 1953 abortion-ban studies; Eastern-European pronatalist-programme assessments; the Israel ethnic-threat, "Guns vs. Wombs," and Christian-nationalism framing experiments.

---

## Provenance and standing caveats

**This chapter is written on 4 of 19 wanted identified-core full texts (21%)** — 4 of the 159-record full pooling set. All four full-text studies fall in the SDT window; the FDT evidence is abstract-level only.

**The findings that would survive full retrieval are** the direction (pronatalist regimes/policies in power are associated with higher fertility) and the central identification finding (where tested, the effect runs through transfers/coercion, not the ideological framing — anchored on Aksoy-Billari's mediation nulls and Validova's tempo decomposition). **The findings that might change are** the FDT-era magnitudes (which require the paywalled coercion canon) and the size of any residual ideational channel (which the OSF framing experiments would sharpen — if any links a message manipulation to a realized birth, the SDT verdict could move from NEGLIGIBLE toward MINOR).

**Numbers sourced from abstracts rather than full text** (marked for the RA retrieval list): all characterisations of the Eastern-European coercion canon and the three framing experiments in §7.2 and §11 are abstract-level, from the blinded screen, not read results. The four studies in §6 and their numeric estimates are full-text read.

**Objection the chapter was written over:** the "smallest unstarted candidate" selection rests on a *partitioned* scout (the economic C-section candidates were never measured against D.1.d); this was flagged in TICK-093's log and accepted by the user (2026-09-26) in place of a fresh cross-field scout. The frame probe confirmed D.1.d at 1,751, below the bar, but did not rule out a smaller unmeasured economic candidate.
