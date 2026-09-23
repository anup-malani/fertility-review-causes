# Coital Frequency and Fecundability

**Category:** Proximate determinant (biological/behavioural) — the exposure gate in the Bongaarts–Davis–Blake framework
**Primary mechanism:** Conception requires intercourse, and the monthly probability of conceiving rises with how often (and how well-timed) intercourse occurs; so anything that lowers coital frequency — spousal separation, customary or post-partum abstinence, illness, declining libido, or the modern "sex recession" — lowers fecundability and, cumulated over a reproductive life, realized fertility, independently of contraception.
**Cross-references:** A.2–A.6 contraception and abortion (own the deliberate decoupling of sex from conception — the Cc/Ca indices; A.14 is the exposure identity *net of* them) · A.7/C.7/A.23–A.24 marriage and union formation (own whether a coital union exists at all — the Cm index; A.14 owns frequency *within* a union) · A.13 breastfeeding and lactational amenorrhoea (owns post-partum anovulation — the Ci index; distinct from post-partum *abstinence*, which is A.14) · A.15/A.16/B.3 fecundity capacity (own the ability to conceive at any frequency) · C.2.h digital leisure, B.7 antidepressants (own specific upstream *causes* of a frequency change) · B.5 fetal loss (owns whether a conception survives).
**Status:** TICK-091. Drafted against `docs/chapter-template.md` on 2026-09-23. Not PI-reviewed. All screening, gating, extraction and risk-of-bias ratings are single-reader (`ra_verified = no` throughout); the AI title/abstract screen used one model (a stubborn batch was re-screened on a second). Written on 7 of the identified-core full texts read against a pooling set of 307 (identified core 139), of which only 29/307 (10/139 core) were OA-retrievable — so this is an **interim draft on the OA-available core**, and the marquee anchors (Barrett–Marshall 1969, Wilcox 1995, Caldwell & Caldwell 1977, Lindstrom–Saucedo 2002, Twenge 2017) are on the RA proxy/ILL handoff and are not yet effect-extracted.

---

## 1. The claim

This chapter explores the effect of how often people have sex on how many children they have.

### 1.1 In plain terms

In plain terms: no birth happens without intercourse (leaving aside IVF, which is a different chapter), and having sex more often — or at the right time in the cycle — raises the chance of conceiving in any given month. So the claim is simply that when couples have sex less often, they have fewer children, and that this can happen for reasons that have nothing to do with birth control: a husband working away from home for a year, a customary period of abstinence after a birth, illness, age, or simply a long-run drift toward less sex in modern marriages.

This is the most mechanical of all the explanations in this review. It is not really a theory about *why* people want children or *whether* they try to avoid them — it is a piece of plumbing. Coital frequency is one of the handful of "proximate determinants" that every distal cause, economic or cultural, must pass through to change births. If a recession or a value shift lowers fertility, it does so in part by changing marriage, contraception, or how often couples have sex; this chapter is about that last channel.

The subtle part — and the reason the claim is weaker than it first looks — is that the relationship is **saturating**. Once a couple has sex often enough to reliably catch the fertile days (very roughly, more than about once a week), having sex still more often adds little to the monthly chance of conceiving. The chance of conception is only really sensitive to frequency when frequency is *low*. So ordinary differences in how often couples have sex — say, eight times a month versus twelve — barely move fertility, while the frequency going to near-zero (a spouse away for a year, a two-year abstinence taboo) moves it a great deal. The claim therefore lives in the tails, not in the middle of the distribution.

What would make the claim matter for a whole population is if some force pushed a large share of couples *below* that threshold. What would make it a demographic footnote is if frequency, though it varies, mostly stays above the point where it binds.

### 1.2 The claim precisely

The parameter this chapter estimates is the effect of coital frequency (or of an exogenous shock to it) on monthly fecundability — the per-cycle probability of conception — and, cumulated, on realized fertility, holding fixed contraceptive practice, whether a union exists, and the couple's underlying fecund capacity. The coefficient is signed so that a fall in frequency produces a fall in fertility.

The chapter rates the claim against the three target phenomena the review uses throughout: **PM** (pre-modern fertility variation, before roughly 1870), **FDT** (the First Demographic Transition, roughly 1870–1965), and **SDT** (the Second Demographic Transition, roughly 1965 onward). Unlike most of the biological hypotheses in this review, `HYPOTHESES-v5` scopes A.14 to **all three** phenomena, and correctly: coital exposure operates in every fertility regime — through spousal separation and abstinence customs in pre-modern and transitional populations, and through the documented "sex recession" in the contemporary rich world.

**This mechanism is an accounting identity with a behavioural input.** Unlike a demand-for-children argument, nothing here depends on preferences: given fecund capacity and no contraception, fewer acts of intercourse mechanically mean fewer conceptions. That makes the *direction* of the effect near-certain. What is uncertain, and what the chapter must actually weigh, is (i) the *shape* of the relationship — where the saturation threshold sits — and (ii) whether observed variation in frequency is an **autonomous cause** of fertility differences or merely the **channel** through which other causes (contraception, marriage, values) act. The distinction between mediator and cause is the spine of this chapter.

---

## 2. Theoretical mechanism

The formal statement is Bongaarts' proximate-determinants framework and its Davis–Blake ancestor. Fertility is the product of a small number of "intermediate variables," each of which every distal cause must work through: the proportion of women in unions (Cm), contraception (Cc), induced abortion (Ca), post-partum infecundability from lactation (Ci), and the residual "natural fecundability" of exposed, non-contracepting couples. Coital frequency lives inside that last term. Tellingly, it is *not* one of the four named indices — because in most historical populations frequency was high enough not to be the binding constraint, so demographers folded it into a background fecundability parameter rather than tracking it. That modelling choice is itself the chapter's central substantive claim in disguise: coital frequency is treated as a determinant that usually does not vary enough, below its saturation point, to matter.

The biology that sets the saturation point is well established. The fertile window is about six days per cycle, ending on the day of ovulation; sperm survive a few days, the oocyte less than one. A couple having sex two or three times a week will, by chance, cover the fertile window in most cycles; a couple having sex once a month may miss it for many cycles running. This is why the per-cycle conception probability is steeply increasing in frequency at low frequencies and nearly flat at high ones.

The mechanism therefore predicts effects concentrated in three situations, and it is in exactly these that the evidence in §6 lives:

- **Spousal separation** drives frequency within an intact union toward zero for the duration of the absence — labour migration, seasonal work, war mobilisation, incarceration. This is the cleanest natural experiment the literature offers, because the separation is often driven by economic forces plausibly unrelated to the couple's fertility desire.
- **Customary and religious abstinence** — long post-partum abstinence taboos, Ramadan or Lenten periods — lower frequency in identifiable windows, again for reasons exogenous to the individual couple's childbearing plans.
- **The modern "sex recession"** — documented declines in sexual frequency among young and married adults in Japan, Korea, the US and the UK — is the SDT-era candidate, and the one where the mediator-versus-cause problem bites hardest, because falling frequency there is entangled with fewer and later unions.

**What would make the hypothesis wrong as an *explanation*** — as opposed to wrong as biology, which it is not — is if the frequency variation that actually occurs across populations and over time stays mostly above the saturation threshold, so that it is a faithful mediator of other causes but rarely an autonomous driver of the differences we are trying to explain. Much of the chapter's caution is exactly this: the identity is real, but its explanatory bite depends on how often frequency is pushed into the binding region.

---

## 3. Search strategy

Gold-anchored clustered search, documented at `literature/search-logs/coital-frequency-biological-*`. A frame probe (`89_a14_frame_probe.py`) first confirmed the selection: A.14's honestly-built retrieval frame is 769 records, the smallest of the genuinely-unstarted hypotheses and well below the review's ~1,808 "smallest" bar, and the registered-construct completeness test passed (every noun the claim names is representable; the broad terms "sexual activity", "libido" and "sexual intercourse" were shown to annex contraception and sexual-medicine literature the walls route away, and were kept out of the recall block, with the clean synonym "coitus" kept in).

Two orthogonal recall channels were built and merged: a citation-network channel seeded on thirteen existence-verified anchors (1,632 records) and a production keyword channel matching the coital-exposure vocabulary against fertility and fecundability outcomes (1,462 records). The two were nearly disjoint — 59 records in common — so merging was load-bearing for recall, and the union is **3,035 unique records** (2,239 with abstracts). The classic biometric and natural-fertility canon sits almost entirely in the citation channel; the keyword channel adds the modern clinical and sex-recession literature.

The scope declares six boundary walls, each separating A.14 from a neighbour that owns a rival channel, and all six were enforced during screening. A.14 is the exposure gate among the proximate determinants, so it shares an edge with almost every other biological hypothesis:

- **Contraception and abortion (A.2–A.6).** The load-bearing wall, because the claim is explicitly *net of* contraception. A study identifying off contraceptive adoption, method mix, or abortion access was routed out; a frequency study in a non-contracepting population is the cleanest A.14 setting. This wall absorbed 404 screened records.
- **Marriage and union formation (A.7/C.7/A.23–A.24).** Whether a coital union exists at all (Cm) is theirs; how often intercourse occurs *given* a union is A.14's. Spousal-separation studies sit on the A.14 side of the bridge because the union persists and only exposure falls.
- **Breastfeeding and lactational amenorrhoea (A.13).** Post-partum *anovulation* from lactation is theirs; the post-partum *abstinence taboo* is A.14's. These co-occur and, as §6 shows, one study could not separate them.
- **Fecundity capacity (A.15/A.16/B.3).** The couple's ability to conceive at any frequency (maternal age, sperm quality, sterilising infection) is theirs; A.14 holds capacity fixed and varies exposure. The age confound — older couples have both lower capacity and lower frequency — is the routing hazard.
- **Upstream causes of a frequency change (C.2.h, B.7, D.1.a).** A.14 owns the frequency→births link *regardless of what changed frequency*; the specific cause (digital leisure, antidepressants, a value shift) is routed to the cause chapter.
- **Fetal loss (B.5).** Whether a conception occurs is A.14's; whether it survives is theirs.

---

## 4. PRISMA flow

| Stage | Records |
|---|---|
| Identified (citation channel 1,632 + production channel 1,462, deduplicated) | 3,035 |
| Screened on title/abstract (blinded, AI) | 3,035 |
| — RELEVANT | 565 |
| — UNCERTAIN (title-only or unresolved) | 525 |
| — NOT RELEVANT | 1,945 |
| Pooling set (RELEVANT ∩ a primary estimand cell ∩ non-review/theory) | 307 |
| — identified core (exogenous frequency shock or prospective measurement) | 139 |
| Full texts retrieved (pooling set) | 29 of 307 |
| Identified-core full texts read and extracted | 7 |
| Survive full-text screen as A.14 primary evidence | **3 strong + 1 weak** |

Three features of this funnel change how the chapter should be read. First, the pooling set is **large** (307) — an order of magnitude bigger than the recent single-mechanism chapters — because A.14 draws on a fifty-year biometric literature, a natural-fertility/historical-demography literature, and a modern sex-recession literature at once. Full extraction of 307 is a scaling task; this draft rests on the OA-retrievable core, and the residual is an RA extraction backlog. Second, the OA retrieval rate is low (29/307) because much of the canonical literature is old and paywalled: the marquee anchors named in §1 are on the RA proxy/ILL handoff, so the causal core here rests on what was reachable, not on the field's best-known papers. Third, of the seven identified-core full texts read, one was **excluded** (its "timed coitus" is a uniform clinical treatment; its actual predictor is ovarian reserve, which is A.15) and one is a **null with a failed manipulation** — so the confirmatory core reduces to two spousal-separation quasi-experiments and one biometric-timing study, plus a weak natural-fertility study.

---

## 5. The ideal design, and the distance from it

### 5.1 The ideal estimand

The change in completed fertility, in births per woman, caused by an exogenous change in coital frequency, among fecund non-contracepting couples in intact unions, holding contraception, union status, and fecund capacity fixed, observed over enough of the reproductive span to distinguish a permanent reduction in the number of children (quantum) from a mere retiming of them (tempo).

### 5.2 The design that would identify it

There are two credible routes. The first is a **prospective biometric** design: measure coital frequency and its timing relative to ovulation directly, day by day, in a cohort of couples trying to conceive, and relate it to the per-cycle conception probability. This identifies the *slope* of the identity cleanly but in a selected (conception-seeking, often clinical) sample, and it measures fecundability per cycle, not completed fertility. The second is an **exogenous frequency shock**: a source of variation that drives frequency down for reasons unrelated to the couple's fertility desire — spousal separation from labour migration or war, a ritual abstinence period — compared against otherwise-similar couples, with the selection into the shock (who migrates, who separates) explicitly modelled. This identifies the demographic contribution, but usually as a period effect over a short window, so it struggles to distinguish tempo from quantum. The ideal study would combine them: an exogenous frequency shock, in a non-contracepting population, followed long enough to read completed fertility, with selection modelled.

### 5.3 The distance table

| Study | Exposure | Outcome | Holds Cc fixed? | Identification | Distance |
|---|---|---|---|---|---|
| **Clifford (2009), Tajikistan** | Months of spousal absence (male labour migration) | Per-year conception; total births over window | Near-natural-fertility setting (contraception ~30%) | Joint multi-process model of conception + migration (selection estimated) | **Nearest (demographic) — the anchor** |
| **Nie (2020), Fujian China** | Spousal separation / reunification (migration) | Birth-order-specific hazards | No direct control | Multi-process event history; correlated heterogeneity | Near, but modern contracepting setting |
| **Bouchard et al. (2018), N. America** | Fertile-window-timed intercourse (measured) | Cumulative pregnancy | N/A (conception-seekers) | Prospective cohort; internal timing contrast, no control arm | Nearest (biometric slope), but selected sample |
| Mturi (1997), Tanzania | Polygamy / non-co-residence (proxies); abstinence | Conception hazard | Yes (non-contracepting sample) | Cox PH; coital frequency never measured | Off-target (indirect, confounded with A.13) |
| Pleasure&Pregnancy RCT (2022), NL | Randomised programme *intended* to raise frequency | Ongoing pregnancy | N/A | RCT, but manipulation failed | Off-target (frequency did not move) |

No study matches the ideal on all dimensions. The two gaps that recur are the ones the ideal design is built to close: the **quantum-versus-tempo** ambiguity (the separation studies observe period fertility over a few years, so a separated couple's "lost" birth may be recovered later — though Nie's finding of *no* reunification catch-up is direct evidence against recovery in that setting), and **direct measurement of coital frequency in a general population** (the biometric slope is measured cleanly only in selected conception-seekers; the natural-fertility study that reaches the general population never measured frequency at all).

---

## 6. Included studies

| Study | Setting | Design | Effect | Risk of bias | Verdict |
|---|---|---|---|---|---|
| **Clifford (2009)** | Tajikistan, 1998–2002 (TFR ~4, contraception ~30%) | Joint multi-process conception+migration model | Full-year spousal absence **OR 0.25**; adjusted ≥6-month absence **OR 0.58**; 6-month seasonal absence OR 0.98 (ns); cumulative 12–23mo Poisson −0.32 | MODERATE | Supports |
| **Nie (2020)** | Fujian, China; births ~1965–2005 | Multi-process discrete-time event history | 1st-birth separation **OR 0.03–0.26**; 2nd-birth OR 0.12–0.30; **no reunification catch-up** (reunified OR 0.42/0.65) | MODERATE | Supports |
| **Bouchard et al. (2018)** | North America, 2008–2015 (N=256, conception-seekers) | Prospective cohort; internal timing contrast | Fertile-window-timed intercourse **85/100** twelve-month pregnancy vs **1/100** on infertile days | SERIOUS | Supports (the slope) |
| **Mturi (1997)** | Tanzania, 1991/92 DHS (non-contracepting, N=4,860) | Cox proportional hazards on birth intervals | Polygamy HR 0.87; non-co-residence HR 0.62; abstinence-and-amenorrhoea combined HR 0.27 | SERIOUS | Weak / partial |
| **Pleasure&Pregnancy RCT (2022)** | Netherlands, 700 couples (unexplained infertility) | RCT (ITT) | Ongoing pregnancy **RR 0.86** (0.64–1.14); **coital frequency did not change** (fell ~7→6/mo in both arms) | LOW internal / SERIOUS indirectness | Null (failed manipulation) |
| Koo et al. (2018) | Korea (N=202) | Retrospective clinical | Predictor is AMH/ovarian reserve, not coital exposure | — | **Excluded** (routes to A.15) |
| Moriki (2012) | Japan | Mixed-methods, descriptive | Sexless marriage ~24–37% (rising); ~35% sexless even among couples wanting a child | — | Mechanism/context |

**The naive estimator in this literature is a cross-sectional correlation of self-reported coital frequency with recent fertility**, which is biased in both directions at once: couples actively trying to conceive have more sex *and* more births (upward bias on the frequency→fertility slope), while couples who have just had a birth have less sex and are not trying again (downward bias). This is why the credible evidence comes from designs that break the reverse-causality loop — an exogenous shock to frequency (separation), or prospective measurement of frequency *before* conception (the biometric cohorts) — and why the chapter does not pool the 300-odd associational records with the identified core.

**The identified evidence is consistent in direction and organised by the saturation logic of §2.** Where frequency is driven toward zero — a full year of spousal absence — the effect is large (Clifford: OR 0.25; Nie: international separation OR 0.03–0.18). Where the absence is short enough that couples reunite within the year — Clifford's six-month seasonal workers — there is essentially no effect (OR 0.98), exactly the dose-response the mechanism predicts: what matters is whether the fertile windows are missed, not the raw count of absent days. And where intercourse is present but mistimed versus well-timed, the per-cycle contrast is enormous (Bouchard: 85 vs 1 per 100). The pieces fit the identity.

**But the evidence is not poolable, and two limits keep it from settling the demographic question.** A formal meta-analysis is not warranted: the estimands are heterogeneous (birth-order-specific odds ratios by separation duration, per-year conception odds, per-cycle cumulative pregnancy rates, Cox hazards on birth intervals), the outcomes differ (period fertility, fecundability, birth-interval length), and the populations span 1990s Tajikistan to a North American fertility clinic. Averaging them would report a number describing none of them. Beyond poolability, the separation studies identify a **period** effect and mostly cannot see whether the lost births are recovered later — Nie's no-catch-up finding is the one direct piece of quantum evidence, and it comes from a modern contracepting setting rather than a natural-fertility one. And every clean estimate comes from a frequency shock *to near-zero*; none identifies the effect of the ordinary, above-threshold frequency variation that most of a population actually exhibits.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

In plain terms: the basic biology is not in doubt. Couples who have sex more often, and closer to the fertile days, are much more likely to conceive — a well-run study of couples trying to get pregnant found that timing intercourse to the fertile window gave an 85-in-100 chance of pregnancy within a year, against almost nothing for intercourse on the wrong days. And when something drives sex down to near-zero — a husband abroad for a year — births fall sharply, by around three-quarters in the cleanest study, and in one setting they do *not* bounce back when the couple reunites.

The catch is that this only bites hard when sex becomes rare. Most couples, most of the time, have sex often enough to catch the fertile days anyway, so ordinary ups and downs in frequency barely change how many children they have. That is why demographers usually treat coital frequency as a background constant rather than a lever. So the honest summary is: as biology, the effect is real and sometimes large; as an *explanation* for the big historical fertility declines, it matters mainly where some force pushed a lot of couples into the rare-sex tail — labour migration, long post-birth abstinence customs, and, today, the "sexless marriages" now common in places like Japan.

### 7.2 The estimate

No pooled estimate is reported, for the reasons in §6. The chapter instead reports the identity's slope and the demographic anchors separately.

The **slope** — the effect of frequency/timing on the per-cycle probability of conception — is steep at low frequency and flat at high frequency. Bouchard's fertile-window contrast (85 vs 1 per 100 over twelve months) and the corroborating cited trials (Tiplady: 43% for timed intercourse vs 30% for frequent-but-untimed) establish that timing and low-frequency variation matter enormously; the Bongaarts–Potter waiting-time model quantifies the saturation, with once-a-week intercourse implying roughly a twelve-month mean wait to conception and once-a-month stretching that toward forty-three months. Above about weekly, further frequency buys little.

The **demographic anchor** is the spousal-separation evidence, read as the effect of pushing frequency to near-zero for a sustained period. Clifford's fully-adjusted estimate is that a year with at least six months of spousal absence lowers the odds of conception in that year by about 42% (OR 0.58), rising to a roughly 75% reduction for full-year absence (OR 0.25); crucially the selection-corrected estimate is *larger* than the naive one, because in that setting the couples who separate would otherwise have had *higher* fertility. Nie's independent estimates are of the same shape and, for the longest international separations, larger (OR 0.03–0.18), with no recovery on reunification. Both are period effects; whether they represent lost completed fertility (quantum) or postponement (tempo) is settled only in Nie's no-catch-up direction, and only for one setting.

---

## 8. Demographic significance

The phenomenon to be explained is a decline in births — a fall in the total fertility rate over a phenomenon's window. Coital frequency offers a fecundability effect that is demographically large only when frequency is pushed into the low-frequency, binding region. The significance question is therefore not "does frequency matter?" (it does) but "how much did frequency get pushed into the binding region, autonomously, during each phenomenon?"

### 8.1 Pre-modern (PM)

For pre-modern variation the verdict is **MODERATE**. In natural-fertility populations, coital frequency was genuinely pushed into the binding region by two autonomous forces: long post-partum abstinence customs (in parts of sub-Saharan Africa, taboos of one to three years measurably lengthened birth intervals and lowered completed fertility) and spousal separation from labour migration, seasonal work, and warfare. These are real, sometimes large, contributions to fertility *variation across pre-modern societies* — the separation quasi-experiments (Clifford, Nie), though modern, identify the same mechanism operating in near-natural-fertility conditions. The verdict is MODERATE rather than SUBSTANTIAL because these forces were concentrated in specific societies rather than being a universal pre-modern driver, and because the marquee direct evidence (Caldwell & Caldwell's abstinence work) is un-extracted here. Coital frequency was a real autonomous lever in the PM regime, but a locally-acting one.

### 8.2 First Demographic Transition (FDT)

For the First Demographic Transition the verdict is **MINOR**. The historic fall from high to near-replacement fertility (~1870–1965) was overwhelmingly a story of *deliberate marital fertility control* — stopping childbearing through contraception, withdrawal, and abstinence used *as* a contraceptive method (which the review routes to A.2–A.6, not here). There is no extracted evidence that autonomous, non-contraceptive coital-frequency decline drove the transition; within the FDT, coital frequency is a mediator of the deliberate-control story, not an independent cause. Whatever role reduced frequency played was as an instrument of intentional limitation, which belongs to the contraception chapters.

### 8.3 Second Demographic Transition (SDT)

For the Second Demographic Transition the verdict is **MINOR**, with a flagged and unquantified exception. The "sex recession" is real and documented: in Japan, roughly a quarter of married couples reported no marital intercourse in the past year, a share that rose across the 2000s, and — the striking datum — about a third remained sexless even among couples who said they *wanted* a child (Moriki). That last fact is the signature of a genuinely *autonomous* frequency deficit, one not reducible to contraceptive intention or to not wanting children. Mechanically, such couples have fewer children than they intend, which is exactly the A.14 channel.

But the verdict is MINOR for three reasons. First, most SDT fertility decline is driven by contraception, postponement, and fewer and later unions, and a large part of the observed frequency decline is *downstream* of those — fewer people are partnered, and partnered later, so population-average coital frequency falls without any change in behaviour *within* unions. That downstream part is a mediator, not an autonomous cause, and must not be double-counted against the marriage and postponement chapters. Second, no extracted study quantifies the within-union, autonomous component's contribution to below-replacement fertility: Moriki documents the phenomenon but estimates no fertility effect, and the marquee sex-recession anchor (Twenge 2017) is un-extracted. Third, the one internally-clean experiment that tried to *raise* coital frequency (the Pleasure&Pregnancy RCT) failed to move it at all, a caution that the frequency margin may be hard to shift with light-touch interventions. The autonomous within-union component could be **SUBSTANTIAL in the East Asian ultra-low-fertility setting specifically** — Japan and Korea are where sexlessness is most prevalent and fertility lowest — but the review cannot yet put a number on it, so the aggregate SDT verdict is MINOR pending the un-retrieved anchors.

---

## 9. GRADE rating

Rated per phenomenon by three independent raters working from an identical evidence package (`extraction/coital-frequency-biological-grade.json`).

| Phenomenon | Rating | Downgrades named |
|---|---|---|
| PM | **MODERATE** (unanimous, 3/3) | From a HIGH biometric-identity ceiling: **−1 indirectness** (the best evidence is modern spousal-separation quasi-experiments and clinical fecundability cohorts, not direct coital-frequency measurement in a natural-fertility population; the marquee abstinence anchor is un-extracted); **−1 tempo-versus-quantum** (the separation studies identify period effects; completed-fertility persistence is established only by Nie's no-catch-up finding, and only for one setting). Raised above LOW because autonomous exposure shocks (abstinence, separation) act in a contraception-free regime with dose-response and selection-correction. |
| FDT | **VERY LOW** (unanimous, 3/3) | **−2** no extracted study links autonomous coital-frequency variation to the 1870–1965 decline; **−1** strong prior that the FDT is a deliberate-marital-control phenomenon in which frequency is a mediator. Not "No evidence" only because the biometric identity makes any frequency change mechanically consequential. |
| SDT | **LOW** (majority, 2/3; one rater VERY LOW) | **−1** the sex recession is real and documented but Moriki estimates no fertility effect and the marquee anchor (Twenge 2017) is un-extracted; **−1** no quantitative estimate of the autonomous frequency→SDT-fertility effect net of union and contraceptive change; the one internally-clean RCT is null with a **failed manipulation**; indirectness/mediator concern (much of the recession is downstream of fewer/later unions). The dissenting rater put SDT at VERY LOW on the ground that no extracted study quantifies the contribution at all. |

The ratings deserve one sentence of interpretation. They rate the credibility that coital-frequency *variation* **caused** fertility variation in each phenomenon — not the frequency→fecundability identity itself, which is near-certain biology in all three. The identity being certain is compatible with the *explanatory* credibility being only moderate-to-very-low, because coital frequency is mostly the **channel** through which other causes act, and rises to an autonomous cause only where an independent force (separation, abstinence, involuntary sexlessness) pushes frequency into the binding region.

---

## 10. Verdict

Coital frequency is a **certified proximate determinant of fertility whose demographic importance is real but confined to the tails of the frequency distribution**. The biology is not in doubt: the per-cycle probability of conception rises steeply with frequency and its timing when frequency is low (fertile-window-timed intercourse yields an 85-in-100 annual pregnancy rate against 1-in-100 for mistimed intercourse), and driving frequency to near-zero through a year of spousal separation cuts the odds of conception by roughly three-quarters, with — in the one setting that can see it — no recovery on reunification. In that sense the mechanism is among the most secure in this review.

But it is secure as *plumbing*, not as an *explanation*, and the two must not be confused. Because the frequency–fecundability relationship saturates above roughly weekly intercourse, ordinary variation in how often couples have sex barely moves fertility; coital frequency matters demographically only where some force pushes a large share of couples into the low-frequency tail. That happened autonomously in specific pre-modern settings (long post-partum abstinence, labour-migration separation), which is why **PM is MODERATE**; it did not drive the First Transition, which was a deliberate-control story, so **FDT is MINOR / VERY LOW**; and in the Second Transition the documented "sex recession" is partly an autonomous within-union deficit (sexless marriages even among couples who want children) and partly a downstream shadow of fewer and later unions — real, but unquantified and largely mediated — so **SDT is MINOR / LOW**. The per-phenomenon GRADE is **MODERATE / VERY LOW / LOW** for PM / FDT / SDT, and the per-phenomenon demographic significance is **MODERATE (localised) / MINOR / MINOR (with a possible East-Asian exception)**. What would raise the SDT verdict is a single number this review does not yet have: the share of below-replacement fertility attributable to declining coital frequency *within intact unions*, net of contraception and of the marriage and postponement channels.

---

## 11. Open questions

- **Tempo versus quantum.** The separation quasi-experiments identify period effects; only Nie's no-catch-up finding speaks to completed fertility, and only in modern China. Whether autonomous frequency shocks reduce the number of children ever born, or merely retime them, is the single largest open question and a PI call on how much weight the PM verdict can bear.
- **The un-retrieved marquee anchors.** The field's best-known studies — Barrett–Marshall (1969) and Wilcox (1995) on the fertile window, Caldwell & Caldwell (1977) on post-partum abstinence, Lindstrom–Saucedo (2002) on migration and fertility, and Twenge (2017) on the sex recession — were not OA-retrievable and are on the RA proxy/ILL handoff. Extracting them would materially change §6–§8, most of all the SDT verdict, and is the highest-priority retrieval task.
- **Quantifying the autonomous SDT component.** No extracted study estimates the contribution of *within-union* frequency decline to below-replacement fertility, net of union and contraceptive change. A design that decomposes the East Asian ultra-low-fertility case into its union, contraception, and within-union-frequency parts is the missing study.
- **The 307-record pool.** This draft rests on 7 of 139 identified-core studies and 29 of 307 pooling-set retrievals. The associational remainder and the un-retrieved core are an RA extraction backlog; the direction is unlikely to change, but the demographic weight might.
- **Direct frequency measurement in a general population.** The clean slope is measured only in conception-seeking clinical cohorts; the natural-fertility study that reaches the general population never measured frequency. A general-population study that measures coital frequency directly and separates it from lactational amenorrhoea (A.13) would close the largest measurement gap.

---

## 12. References

- Bouchard, T. P., Fehring, R. J., & Schneider, M. (2018). Achieving pregnancy using primary care interventions to identify the fertile window. *Frontiers in Medicine*, 4, 250.
- Clifford, D. (2009). Spousal separation, selectivity and contextual effects: Exploring the relationship between international labour migration and fertility in post-Soviet Tajikistan. *Demographic Research*, 21(32), 945–975.
- Moriki, Y. (2012). Mothering, co-sleeping, and sexless marriages: Implications for the Japanese population structure. *The Journal of Social Science* (ICU), 74, 27–45.
- Mturi, A. J. (1997). The determinants of birth intervals among non-contracepting Tanzanian women. *African Population Studies*, 12(2).
- Nie, W. (2020). The effect of spousal separation and reunification on fertility: Chinese international and internal migration. *Demographic Research*, 43(29), 859–882.
- Pleasure&Pregnancy programme investigators (2022). A web-based programme to improve sexual functioning and increase natural conception in couples with unexplained infertility: RCT. *Human Reproduction* (Netherlands, 700 couples).
- Koo, H.-S., et al. (2018). The likelihood of achieving pregnancy through timed coitus in young infertile women with decreased ovarian reserve. *Clinical and Experimental Reproductive Medicine*, 45(1), 31–37. [Excluded: predictor is ovarian reserve, not coital exposure — routes to A.15.]
- *On the RA proxy/ILL handoff (context, not extracted):* Barrett & Marshall (1969); Wilcox, Weinberg & Baird (1995); Caldwell & Caldwell (1977); Lindstrom & Saucedo (2002); Twenge, Sherman & Wells (2017); Bongaarts (1978); Davis & Blake (1956); Wood (1989).

---

## Provenance and standing caveats

- **Selection.** A.14 was chosen as the smallest genuinely-unstarted hypothesis by measured retrieval frame (769, below the ~1,808 bar), confirmed by the frame probe and its registered-construct completeness test (`89_a14_frame_probe.py`; `literature/search-logs/a14-frame-probe-2026-09-23.md`).
- **Pipeline.** Cold-start anchors (`90`, 13 existence-verified via Crossref) → citation frame (`91`, 1,632) + production frame (`92`, 1,462) → merged screen frame (3,035) → blinded Haiku title/abstract screen, 76 batches (`93`–`95`; one batch re-screened on `claude-sonnet-5` after a Haiku row-drop) → assembly (`96`) → OA retrieval (`97`, 29/307) → full-text extraction of the identified core by parallel agents (`98`) → risk of bias (`99`) → this chapter.
- **Single-reader.** All screening, gating, extraction, and risk-of-bias ratings are single-reader (`ra_verified = no`). Owed: the human RA title/abstract gate, a 5–10% full-text spot-check, and a 10% extraction verification.
- **Interim.** This is an interim draft on the OA-available core (7 of 139 identified-core studies; the marquee anchors un-extracted). The direction of the verdict is unlikely to change; the SDT demographic weight is the most likely to move once the anchors are retrieved.
- **GRADE.** Three independent raters, identical package (`extraction/coital-frequency-biological-grade.json`). PM MODERATE (3/3), FDT VERY LOW (3/3), SDT LOW (2/3, one VERY LOW).
