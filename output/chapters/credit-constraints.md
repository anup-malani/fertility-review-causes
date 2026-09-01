# Credit Constraints and Liquidity

**Category:** Economic
**Primary mechanism:** When a household's access to borrowing, saving and insurance changes, both the value of a child as an asset and the timing at which a child is affordable change with it — and the two push fertility in opposite directions.
**Cross-references:** C.3.c (old-age security) owns variation in non-child old-age provision; the boundary between it and this chapter was re-cut on 2026-09-01 and is the chapter's largest open ruling. C.2.c (housing costs) owns variation in house prices, including home-equity collateral effects. C.5.a (economic uncertainty) owns variation in risk exposure where financial instruments are held fixed. C.2.d owns variation in the price of a birth. C.3.g owns the prior education liability. C.3.d owns the quantity–quality trade-off, which absorbed four records whose outcome turned out to be child education or earnings. A.23 owns living arrangements.
**Status:** TICK-077. Drafted 2026-09-01. **Not PI-reviewed. Written on 14 of 65 wanted full texts (22%), by a single GRADE rater where the protocol requires three, and with one boundary ruling applied on RA authority pending Anup.** The chapter should be read as an interim statement of what the retrieved evidence shows, not as a settled verdict.

---

## 1. The claim

This chapter explores the effect of household credit constraints on fertility.

### 1.1 In plain terms

In plain terms: whether a family can borrow money, save it safely, or insure against bad years may change how many children they have — and it may change it in either direction.

Where there are no banks, no insurance and no safe way to put money aside, children do that job instead. Grown children work, send money home, and look after parents who can no longer work. On this account, a family without a bank has a reason to have more children, and giving that family a bank should mean fewer.

But in a place that already has banks, the problem is the opposite one. A young couple who want a child may be unable to afford one now, even though they will be able to afford one later, because nobody will lend them the money against earnings they have not yet received. On this account, easier borrowing means they can start earlier, and so have more children rather than fewer.

Both stories are about the same thing — what a household can do with money across time — and they predict opposite outcomes. That is the whole difficulty of the chapter, and it is why the two are kept apart throughout and never added together.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in a woman's completed fertility — the total number of children she has borne by the end of her childbearing years — caused by an exogenous change in the household's access to credit, saving or insurance, measured in births per woman, signed so that a positive value means more births after a relaxation of the constraint.

The registry entry names two configurations of that exposure with opposite predicted signs, and they are carried as two arms:

- **Arm S, the saving side.** Availability of a formal instrument for moving resources across time and states of the world. It acts on the **value** of a child as an asset: a formal substitute displaces the child. Predicted sign: **negative**.
- **Arm B, the borrowing side.** The terms on which a household can borrow against future income. It acts on the **intertemporal budget constraint**: when a given child is affordable. Predicted sign: **positive**.

**Arms are never pooled and never averaged.** They sit in different settings, draw on different literatures, and have opposite predicted signs; a pooled estimate across them would not estimate anything.

There is a third class of exposure that moves both at once — bank branch expansion, microfinance entry, financial-inclusion reform — and its estimates cannot be allocated to either arm. That class is carried as **composite**, and it is the reason this is one chapter rather than two: no rule can split a bank-branch estimate between the saving channel and the borrowing channel, because the estimate is their net.

**This is a behavioural parameter, not an identity.** There is no accounting relation that must hold. Every link can be false.

**Margin.** Arm S is predicted to move the intensive margin — how many children a woman who is having children has — because it changes the return to an additional child. Arm B is predicted to move both the extensive margin and, heavily, the *timing* of births, which matters because a timing effect and a completed-fertility effect are different quantities and are recorded separately here.

The chapter rates the claim against the review's three target phenomena: **PM** (pre-modern fertility variation, differences between populations before roughly 1870), **FDT** (the First Demographic Transition, the sustained fall across Europe and its offshoots from roughly 1870 to 1965) and **SDT** (the Second Demographic Transition, the further fall to below-replacement levels — under about 2.1 children per woman — from roughly 1965 onward).

---

## 2. Theoretical mechanism

In the standard household model, a child is both a consumption good and, where markets are incomplete, an asset. Arm S operates on the asset return: if a household can hold a claim on future resources through a bank or an insurer, the implicit return to holding that claim through a child falls, and desired fertility falls with it. Arm B operates on the budget set: a household that cannot borrow against future earnings faces a binding constraint in exactly the years when children are biologically cheapest to have, and relaxing that constraint moves births earlier and, if the postponement would otherwise have been permanent, upward.

The two are not rival theories of the same margin. They are statements about different arguments of the same problem, which is why a single change in financial development moves both and why its net effect is ambiguous in theory.

**What would make the hypothesis wrong.** For Arm S: a household in a setting with no formal finance that does not treat children as an asset — that is, whose fertility does not respond when a formal substitute arrives. For Arm B: a household whose fertility does not respond to a relaxation of borrowing terms that demonstrably changed what it could borrow. The second of those has now been observed (§6), which is why the distinction between a verified and an unverified first stage does real work in this chapter.

---

## 3. Search strategy

Reproducible from `literature/search-logs/credit-constraints-search-scope.md` and scripts `275`–`303` in `source/build/goldset/`.

Two channels were run and kept separate: a **term channel** (an exposure axis per arm crossed with a fertility-outcome axis, in OpenAlex `title_and_abstract.search`) and a **provenance channel** (citation snowball, backward and forward, from 26 hand-resolved anchors, then two further rounds). The channels overlapped by only about 2.5% of records, and that disagreement is itself reported: the term channel found a microfinance-and-fertility literature the provenance channel could not see, because the provenance channel's seeds were chosen for design quality rather than for measuring the outcome.

**Six walls were frozen before searching.** The governing rule throughout is that neighbouring hypotheses are separated by *what varies*, not by the mechanism an author narrates.

| Wall | Discriminator |
|---|---|
| **1 — vs C.3.c (old-age security)** | **Re-cut on 2026-09-01.** Originally split on *which risk is insured*; that axis failed because the founding literature does not have it (§11). Now: C.3.c owns variation in non-child **old-age provision**; this chapter owns variation in the availability of a **general financial instrument**, whatever risk it covers. |
| 2 — vs C.2.c (housing) | Variation in house prices or rents is C.2.c's, including home-equity collateral effects. Credit terms at fixed prices are this chapter's. |
| 3 — vs C.3.g (student debt) | A prior education liability already incurred is C.3.g's. |
| 4 — vs C.1.a (income) | Relaxation that raises lifetime resources is C.1.a's; relaxation that changes only their timing is this chapter's. |
| 5 — vs C.5.a (uncertainty) | A binding limit at known income is this chapter's; more variance in expected income at fixed borrowing terms is C.5.a's. |
| 6 — the outcome wall | The outcome must be fertility. Effects on marriage, homeownership, education or earnings are mechanism evidence only. |

**Wall 6 was declared in advance and did the most work.** It was written because a neighbouring chapter's evidence base had failed the same way, and it removed four records at full text whose outcome turned out to be children's education, child earnings, or participation in continuing education, with family size on the right-hand side.

**One vocabulary finding worth carrying.** Arm S's exposure vocabulary is *risk*, not *credit*: the founding insurance-motive literature does not use financial words in its titles. A token filter scoring 24 of 26 known-positive records still could not be used as a gate, because the two it missed included the chapter's most valuable historical record.

---

## 4. PRISMA flow

| Stage | n |
|---|---|
| Term-channel frame (after query repair) | 3,512 |
| Provenance pools (three snowball rounds) | 3,976 + 297 + 261 |
| Hand-sourced anchors, decoys and boundary finds | 130 |
| **Screening universe after de-duplication** (397 version pairs collapsed) | **7,327** |
| Deterministic prescreen (3 rules of 4 survived a recall check) | −792 → 6,535 |
| **Screened at title/abstract** | **2,750** |
| Routed to a primary cell | **65** |
| Verified full text obtained | **14** |
| Studies extracted | **14** (18 effect rows) |
| Of which identified | **5** |

**Three features of this funnel change how the chapter should be read.**

**One stratum of 3,815 records is unscreened.** A blinded 400-record probe put its yield at 1.00%, projecting 38–57 further primary records. It is not screened because it is the least efficient block in the chapter, not because it is empty.

**The screen's cells are hypotheses, and they have not held.** Every primary record with a full text was checked against its own text, and **twelve cells were overturned — eleven by removal.** Where the screen has been tested it has failed about two-thirds of the time. The primary pool of 65 is therefore an upper bound, not a count.

**The two positive-and-negative findings that bear on the sign both come from unrefereed or near-unrefereed venues** (§6), which is a fact about the literature's maturity, not a criticism of the search.

---

## 5. The ideal design

### 5.1 The ideal estimand

Among women aged 20–35 in a defined population, the effect on **completed cohort fertility** of a permanent, exogenous increase in the household's access to a formal financial instrument — one standard deviation of private credit to GDP, or the arrival of a bank branch within a defined travel time — holding income, prices, the returns to children and old-age provision fixed, measured in **births per woman** over a horizon long enough to separate timing from quantum, which means following the cohort to age 45.

### 5.2 The design that would identify it

Staggered, policy-driven expansion of financial access across geographic units, with the timing unrelated to local fertility trends; a comparison of women in units treated earlier against those treated later; the falsifiable assumption that pre-treatment fertility trends are parallel, tested directly, with a placebo on cohorts past the age of family formation; and a panel long enough to follow treated cohorts to completed fertility. Ideally the design separates **access** (can the household borrow or save at all) from **cost** (how expensive it is), because those turn out to be different treatments.

### 5.3 Distance from the ideal

| Study | Exposure distance | Outcome distance | Horizon | Assignment | Overall |
|---|---|---|---|---|---|
| Do credit supply shocks affect fertility (2022) | near — credit supply | near — fertility rate, birth propensity | short | **exogenous** (deregulation timing; Bartik IV) | **closest to the ideal** |
| Hacamo, mortgage-market deregulation | near — credit access | near — probability of a child | short | **exogenous** (regulator ruling) | close |
| Ao et al. (Taiwan) | **cost, not access** | near | short | **exogenous** (policy, first stage verified) | close, different treatment |
| Desai and Tarozzi (Ethiopia) | near — credit arm randomised | near — births in 3 years | 3 years | **randomised** | close on assignment, short on horizon |
| Wang and He (China) | near | near | short | IV, not a policy shock | moderate |
| Grimm, bank-access interaction | far — crude bank counts | near | long | panel FE | far on exposure |
| US counties c.1850 | near — bank presence | near — child–woman ratio | cross-section | **none** | far on assignment |
| Filoso and Papagni; Suriani et al. | aggregate | aggregate | long | **none** | farthest |

**No study matches the ideal**, and the gap is stated in the verdict. The closest is *Do credit supply shocks affect fertility choices?*, which has exogenous assignment and the right outcome but a short horizon, so it cannot separate timing from completed fertility.

---

## 6. Included studies

| Study | Setting | Design | Exposure | Outcome level | Result |
|---|---|---|---|---|---|
| Do credit supply shocks affect fertility (2022) | US | deregulation timing; Bartik IV | credit supply | realized | **+5.4%**; **+9.5 pp** on a 7.7 pp base |
| Hacamo (2016/2020/RFS) | US | federal regulator ruling | mortgage credit access | realized | **+6 pp** |
| Ao, Chen and Tseng (2026) | Taiwan | DiD with matching | mortgage interest subsidy (**cost**) | realized | **null**; first stage verified (burden −7.9%) |
| Wang and He (2025) | China | FE-Poisson + IV | household credit | realized | **inverted U** |
| Desai and Tarozzi (2011) | Ethiopia | **RCT**, credit arm separately randomised | credit access | realized / desired | births **−0.106 to −0.166**; desired family size **+0.38 to +0.40** |
| Küchler (2012) | Bangladesh | DiD | microfinance participation | realized | −0.14, t = −1.54, **ns** |
| Islam, Kamal and Nguyen (2026) | Bangladesh | DiD + matching | microcredit access | realized | lower recent fertility |
| Karim et al. (2016) | Bangladesh | cross-section with controls | NGO membership (**proxy**) | realized | 1.024–1.028\* after 2007, "2 to 3 in 100 more children" |
| Steele, Amin and Naved (1998) | Bangladesh | quasi-experimental panel | savings/credit groups | desired | authors: no significant effect |
| Lan, Pan and Yu (2023) | China | IV | digital financial inclusion | **intention** | +0.136% |
| Grimm (2019) | US frontier | panel FE | banks per county × rainfall risk | realized | negative, small, **insignificant** — author: measures "too crude" |
| US counties c.1850 | US | OLS cross-section | bank presence | realized | child–woman ratio **−3 pp**; CBR **−5%** |
| Filoso and Papagni (2014) | 145 countries | aggregate panel | private credit, +1 SD | realized | **−1.7 to −5%** low-income; **+3.7 to +5%** high-income |
| Suriani et al. (2021) | 42 + 43 countries | system GMM | private credit | realized | **negative in all 11 models in both samples**, developing larger |

### The estimator disagreement, resolved rather than averaged

**The two aggregate panels contradict each other on the developed-country sign.** Filoso and Papagni report a positive high-income effect; Suriani et al. report a negative one in every specification. They are not averaged. Both are unidentified — neither instruments credit — and Suriani's Sargan test is rejected (p = 0.000) in all eleven models in both samples, while Hansen is not. **Neither is given weight against the identified estimates**, and the disagreement is reported as the state of the aggregate evidence rather than resolved by splitting the difference.

**The apparent disagreement among the identified estimates resolves on a distinction, not a compromise.** Three positives and one null: the positives are **access** shocks — deregulation, a regulator ruling, a credit-supply shock, all changing whether a household can borrow — and the null is a **cost** reduction for households already borrowing, with a verified first stage. Access moved fertility; cheapness did not. That is a coherent reading of four studies, and it is testable against the records not yet read.

**Naive estimator.** The naive estimator here is a cross-sectional comparison of constrained and unconstrained households. Its bias is signed and predictable: households that report being credit-constrained differ in income, risk and planned fertility, and the two studies in this pool that come closest to it (Karim; Steele) are the two with CRITICAL selection risk — in Steele's case because, on the authors' own account, joiners were **more likely to have used contraceptives before joining**.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

In plain terms: where it has been measured properly, giving households better access to borrowing has led to **more** children, not fewer — by something like five per cent, in rich countries, when banking rules were loosened. Where households were simply given cheaper loans rather than new access to loans, nothing happened to the number of children at all. And in poorer countries, where the theory says the opposite should happen — that a bank should replace the reason to have children — the few careful studies find very small effects, mostly indistinguishable from nothing, and they disagree with each other about the direction.

The one thing that is clear is that people's *stated wishes* and their *actual births* move in opposite directions. In the single experiment that measured both, families given credit said they wanted more children and had very slightly fewer.

### 7.2 The estimate

**No meta-analysis is reported, and none should be.** Stratifying by arm, outcome level and estimator compatibility before applying the three-study threshold, **not one stratum qualifies**: Arm B realized-identified has four studies across three estimator classes; composite realized-unidentified has five studies across four classes; Arm S realized has two studies. A naive pool would have "qualified" on fourteen studies, and would have averaged an Ethiopian randomised null against a US deregulation elasticity against a cross-country GMM coefficient.

**Arm B, realized fertility, identified:** three positive estimates — +5.4%, +6 pp, +9.5 pp on a 7.7 pp base — and one verified null, all in high-income settings, all on **access** except the null, which is on **cost**.

**Arm S, realized fertility:** two unidentified estimates, one of which (US counties c.1850) its own authors frame as evidence for the old-age-security motive, and one (Grimm) whose author reports the exposure measure is too crude to interpret. **There is no identified Arm S estimate in the chapter.**

**Composite:** one randomised estimate (Desai and Tarozzi), small and negative on realized births; three further low-income estimates, null or negative; and two aggregate panels that disagree at the sign.

**Outcome level is not a nuance here.** Every positive result in the chapter sits on **desires or intentions** — Desai and Tarozzi's +0.38 to +0.40 desired family size, Lan et al.'s +0.136% intentions — while every realized-fertility result in a low- or middle-income setting is null or negative. Pooling across outcome levels would average a null against a positive and report a number describing neither.

---

## 8. Demographic significance

The phenomenon to be explained is measured in births per woman over a century; this mechanism offers percentage changes in birth probabilities over windows of three to ten years.

That mismatch does not by itself settle anything, because a percentage change in a birth probability can be accumulated into completed fertility if the horizon is long enough. What settles the question here is a prior fact about the exposure, and it is available without any denominator.

**The exposure moved, and it moved the wrong way.** Over the SDT window, private credit to GDP rose from **0.39 to 1.14** in high-income countries and from **0.13 to 0.31** in lower-income countries — figures reported by Filoso and Papagni, whose own panel this chapter also uses. Financial access expanded enormously across exactly the period in which fertility fell.

**No share of any phenomenon is computed in this chapter, and no share should be.** The repository holds no fertility panel from which a denominator — a change in births over a phenomenon's full window — could be drawn, so any share would be a share of a study window and would not be reportable under `PROTOCOL.md` §4.2.1. Every cell below is therefore NOT ASSESSED on the arithmetic. But the slope question is answerable and is answered.

### 8.1 Pre-modern

For pre-modern variation, the verdict is **NOT ASSESSED**, because the cell is in scope under the registry and contains no read evidence: eleven Arm S records, two read at full text, and both left the cell on reading.

Arm B is out of scope for PM: borrowing terms presuppose a credit market.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is **NOT ASSESSED**, because the cell contains one read study, an unidentified cross-section whose own authors attribute the result to a neighbouring hypothesis.

Three FDT-era Arm S records were identified — bank presence in US counties around 1850, savings behaviour in nineteenth-century Britain, and rainfall risk on the American frontier. **One has been read.** The Britain paper is unavailable through the library; the frontier paper's Arm S estimate is the imprecise bank-access interaction discussed in §6. If it were assessed, the sign would be negative.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is **NOT ASSESSED**, because no share is computable — **but the sign of the mechanism is wrong for the phenomenon, and that forecloses the question a share would have answered.**

Credit access expanded across the SDT. Every identified estimate says expansion raises fertility. A mechanism whose exposure moved in the direction that raises fertility cannot explain a decline in fertility. At most it is an **offset**: the SDT would have been larger than it was without the expansion of credit.

The composite cell is additionally **contested at the sign** — the only two studies that claim to measure the low-income/high-income difference directly disagree with each other, and neither is identified.

**Endogeneity check.** Is the credit-market change itself caused by the fertility decline? An ageing, low-fertility population has different savings supply and different credit conditions, and one study in this pool (*Falling Real Interest Rates, House Prices, and the Introduction of the Pill*) argues exactly that causal direction and was routed out of the pool for it. The identified estimates used here rest on **policy** shocks — deregulation timing, a regulator ruling — which are not plausibly caused by fertility, so the offset reading survives this check.

---

## 9. GRADE

| | Arm S | Arm B | Composite |
|---|---|---|---|
| **PM** | **No evidence** | n/a — requires a credit market | **No evidence** |
| **FDT** | **Very low** | **No evidence** | **No evidence** |
| **SDT** | **No evidence** | **Moderate** | **Very low** |

**Downgrades named.**

- **SDT / Arm B — Moderate.** Starts high on four identified designs (staggered deregulation timing, a Bartik instrument, a federal regulator ruling, and a difference-in-differences with matching and a verified first stage), consistent in sign. **Downgraded once for indirectness:** the estimates answer whether credit access raises fertility, while the chapter asks whether credit constraints explain the SDT decline, and the sign runs the wrong way for that question. **Not downgraded for inconsistency**, because the null and the positives differ by treatment — cost versus access — rather than by result.
- **FDT / Arm S — Very low.** One study, unidentified, downgraded for risk of bias (selection and confounded shock both SERIOUS) and for indirectness, its authors attributing the finding to C.3.c's motive.
- **SDT / composite — Very low.** No identified estimate on realized fertility outside one randomised trial; the aggregate panels disagree at the sign; one has rejected overidentifying restrictions; two studies carry CRITICAL selection risk.
- **Empty cells take No evidence, never Very low.** Very low would assert a poorly identified literature where there is none.

**Rated by one rater.** `PROTOCOL.md` §5 stage 11 requires three independent raters. This table is a single-rater draft for adjudication, and a single rater arguing both sides is not a panel.

---

## 10. Verdict

**Credit constraints are not an explanation of fertility decline. On the best evidence available, they worked against it.**

Where household credit access has been expanded by something other than households' own choices — American banking deregulation, a federal mortgage ruling, a credit-supply shock — **fertility rose**: by about 5% in the deregulation estimate, and by 6 percentage points on the probability of having a child for the households most exposed to the mortgage ruling. Credit access expanded enormously over the period the Second Demographic Transition covers, roughly tripling relative to income in rich countries. A mechanism that pushes fertility **up**, whose exposure moved **up**, cannot account for fertility going **down**.

The number to carry away is **+5.4%** — the effect of American banking deregulation on the fertility rate — with the sign being the point, not the magnitude.

Two qualifications belong in the same breath. **Cheaper credit is not the same as more credit:** the one policy that reduced the cost of borrowing without extending access, in Taiwan, moved the mortgage burden by 7.9% and moved fertility not at all. And **the poor-country half of the hypothesis has not been tested.** The claim that children serve as savings and insurance where banks do not exist — the configuration on which the pre-modern and First-Transition cases rest entirely — has **no identified evidence in this chapter at all**, and the historical literature that argues it turns out, on reading, to vary risk, land tenure, or the price of a birth rather than access to any financial instrument.

So the chapter's finding is asymmetric and should be reported that way: **for the rich-country transition, credit constraints are refuted as a cause and survive only as an offset; for the pre-modern and historical cases, the hypothesis is unevaluated rather than refuted.**

---

## 11. Open questions

**PI calls.**

1. **Wall 1, applied on RA authority and needing Anup's ruling.** The wall originally split the asset motive by *which risk is insured* — longevity to C.3.c, within-life risk here. Cain's 1986 reply shows that distinction is ours and not the literature's: he defines insurance to cover disability, widowhood, depredation and floods **alongside old age**, and cites Nugent's old-age-security paper approvingly in support. The wall was re-cut on the **instrument** instead, which is consistent with the project's governing rule but routed seven of twelve Arm S records out. Three options were put: merge Arm S into C.3.c; re-cut on the instrument; or accept that Arm S is largely empty of admissible variation. The second was chosen and delivered the third.
2. **Whether a study whose authors attribute their finding to a neighbouring hypothesis stays.** The 19th-century US counties study varies bank presence — this chapter's exposure — but is framed by its authors as evidence for old-age security. On the what-varies rule it is ours; on the authors' reading it is C.3.c's. It is currently the only read FDT-era record in the chapter, so the ruling decides whether FDT/Arm S is *Very low* or *No evidence*.

**Retrieval priorities.** Nine Arm S records are unread and the arm cannot be rated without them; the two studies bearing most directly on the sign question — Thailand's Million Baht Village Fund (negative, middle-income) and a Chinese bank-competition deregulation study (positive) — are in a mathematics-education journal and an unrefereed preprint respectively and need hard reads before either is given weight.

**Studies that do not exist and should.** There is no identified study of a formal savings or insurance instrument becoming available to a low-income population, with completed fertility followed to age 45. The microcredit randomised trials of the 2010s had the design and the settings for it and did not measure fertility: of ten such studies read in full, **not one estimates a fertility outcome anywhere in its text**. That is the single largest gap in this literature, and it is a gap in measurement rather than in method.

---

## 12. References

Full bibliographic detail, with OpenAlex identifiers and DOIs, is in `extraction/credit-constraints-screen.csv` (all 2,750 screened records with routing and reasons) and `extraction/credit-constraints-effects.csv` (all extracted effects). Risk-of-bias judgements per study and domain are in `extraction/credit-constraints-risk-of-bias.csv`.

---

## Provenance and standing caveats

**This chapter is written on 14 of 65 wanted full texts (22%).**

**The findings that would survive full retrieval are** the sign and rough magnitude of the identified Arm B estimates, the access-versus-cost distinction that reconciles them, and the slope argument in §8.3 — which rests on the exposure's own trend and on the sign of four studies, not on any count of records. **The findings that might not are** the arm counts, every GRADE cell that depends on how many studies a cell holds, and the claim that Arm S has no identified evidence, which is a statement about eleven records of which two have been read.

**Objections this chapter was written over.** The chapter was drafted at Shravan's instruction after I advised against it: 22% of the pool is read, and where screen cells have been tested against their own texts they have failed about two-thirds of the time — twelve overturned, eleven by removal. The arm counts in §4 are an upper bound, not a count, and the GRADE table is a single-rater draft where the protocol requires three.

**Numbers taken from abstracts rather than full text**, and on the residual retrieval list: Ao, Chen and Tseng (2026) — the −7.9% mortgage-burden first stage and the null on fertility; Wang and He (2025) — the inverted-U result. Both are marked in the extraction table.

**One boundary ruling is applied on RA authority and is not PI-confirmed**: the Wall 1 re-cut described in §11. It changes which phenomena are in scope, and PM and FDT depend on it.
