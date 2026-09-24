# Son Preference and Gender-Biased Fertility Norms

**Hypothesis D.2.c** (HYPOTHESES-v5.md §D.2.c) · slug `son-preference-cultural`
**Target phenomena:** PM, FDT, SDT
**GRADE (causal credibility):** PM **LOW** · FDT **MODERATE** · SDT **MODERATE**
**Demographic significance (effect on fertility levels):** PM **MINOR (localised)** · FDT **MINOR–MODERATE (South/East Asia)** · SDT **MINOR**
**Standing:** interim draft on a curated identified core (9 of 380 identified-core studies extracted; 97/380 OA-retrieved). RA title/abstract gate, lay-readability check, and PI sign-off still owed.

---

## 1. The claim

### 1.1 In plain terms

Some couples care about the sex of their children, not only the number. Where a culture prizes sons in
particular — because a son carries the family name, inherits the land, or is the one expected to support
parents in old age — a couple that has reached the family size it wanted but has no son faces a decision a
sex-indifferent couple never faces: stop, or try once more for a boy. Many try again. Added up across a
population, this **differential stopping** raises the average number of births above what the same people
would have had if they valued sons and daughters alike.

There is a twist that decides how much this matters for the birth rate. Once it becomes possible to learn
a baby's sex before it is born and to abort, the same preference can be satisfied without an extra birth:
a couple can abort female foetuses until it conceives a son. The preference then shows up as **too few
girls** — a skewed sex ratio at birth — rather than as **more children**. This is why son preference is a
shape-shifter: in a world without sex selection it pushes fertility up; in a world with cheap sex
selection it stops pushing fertility up and starts skewing the sex ratio instead.

### 1.2 The claim precisely

Son preference raises realized fertility through sex-composition-conditional continuation, holding fixed
the number of children a couple would have chosen absent any sex preference; where prenatal sex-selection
technology is available, that fertility effect is partially or wholly substituted by sex-selective
abortion, which the preference expresses as a skewed sex ratio at birth. The parameter this chapter
seeks is the additional births attributable to the preference for sons — measured as differential parity
progression by the sex composition of existing children, or as completed fertility as a function of
son-preference intensity — and how that number changes when sex selection enters.

The chapter's estimand is the effect on the **number of births**. The effect on the **sex ratio at
birth** is treated only as the substitution expression of that same preference, not as an outcome of
independent interest here; the demographic consequences of the resulting adult sex-ratio imbalance belong
to A.10 (Sex Ratio Imbalance and Marriage-Market Effects), and the non-fertility harms of son preference
(excess female mortality, unequal schooling and nutrition) belong to their own literatures.

---

## 2. Theoretical mechanism

The mechanism is a preference over the joint distribution of the number and sex of children, layered on
top of an ordinary quantity decision. Ben-Porath and Welch's differential-stopping model is the canonical
statement: if couples have a target for sons, those who draw daughters early keep going, so completed
family size becomes a function of the sex sequence realized. Because the sex of each birth is close to a
coin flip, this generates a sharp, testable signature — families that happen to draw only girls end up
larger than families that happen to draw a boy, even though nothing differs between them except luck.

Three roots are usually given for why the preference falls on sons: patrilineal transmission of the
family name and lineage, inheritance and property rules that favour male heirs, and old-age support norms
under which a son (and his wife), not a daughter (who marries out), maintains ageing parents. The last of
these is the economic hinge to C.3.c (old-age security): where the state does not insure old age, sons
are the insurance, and the preference has a material base. This chapter treats those roots as the source
of the norm and estimates the fertility consequence of the norm itself.

The substitution logic is the second half of the mechanism and is what makes the sign regime-dependent.
A couple with a fixed son target has two technologies for hitting it: have more children until a son
arrives (raising fertility), or select the sex of a given birth (holding fertility down but skewing the
sex ratio). When ultrasound and abortion make the second technology cheap, rational couples switch to it,
and the preference's footprint moves from the birth count to the sex ratio. Jayachandran's formalization
makes the same point from the other direction: as desired fertility falls, a fixed son preference must be
concentrated into fewer births, which mechanically raises the sex ratio unless the preference itself
weakens.

---

## 3. Search strategy

The scope is at `literature/search-logs/son-preference-cultural-search-scope.md`. Two §5.1 channels were
run and merged. A production keyword frame (son-preference topic terms — "son preference", "preference for
sons", "sex-selective abortion", "sex selection", "differential stopping", "sex composition" — conjoined
with a fertility or sex-ratio-at-birth outcome) returned 2,490 records. A citation frame, built from 14
existence-verified cold-start anchors (the differential-stopping core, the sex-selection substitution
naturals, and six wall decoys) forward-seeded on the empirical core only, returned 1,948. The merged,
de-duplicated screen frame was **4,035 records** (3,040 with abstracts).

The selecting frame was validated before any screen spend by a frame probe with a registered-construct
completeness test (`89_d2c_frame_probe.py`), the discipline the A.6/A.3 mis-rankings made mandatory. The
honest production frame was 1,696 — the smallest of every un-ticketed candidate and below the ~1,808
"smallest" bar. The completeness test confirmed that the genuine constructs (sex composition, sex ratio
at birth, male preference) widen the frame only modestly, while the words that would have inflated it —
a bare "sex ratio" (which annexes A.10's adult-sex-ratio literature), "preference", "gender", "son" — are
free-`OR` inflaters and were excluded. The load-bearing A.10 wall was clean in the probe (2.7 % frame
overlap, one identified record).

---

## 4. PRISMA flow

| Stage | N |
|---|---|
| Merged screen frame (keyword ∪ citation) | 4,035 |
| Blinded title/abstract screen (Haiku, 101 batches; batch 48 on Sonnet) | 4,035 |
| RELEVANT | 1,509 |
| UNCERTAIN | 771 |
| NOT_RELEVANT | 1,755 |
| Pooling set (RELEVANT ∩ PRIMARY ∩ non-review/theory) | 1,047 |
| — identified core (natural-experiment or revealed-stopping) | 380 |
| — associational | 667 |
| Open-access full text retrieved (identified core) | 97 / 380 |
| Full-text screened + extracted (curated core, this draft) | 9 |
| — SURVIVES / WEAK / CONTEXT | 5 / 2 / 2 |
| Effects extracted | 23 |

The walls absorbed cleanly and correctly: 340 records routed to OFF_OUTCOME (son preference → excess
female mortality, child health, schooling — the non-fertility harms), 44 to A.10 (adult sex ratio), 33 to
A.4 (general abortion), 32 to D.2.a (general gender equity), 24 each to A.8 (sex-indifferent parity
stopping) and C.3.c (old-age security), 7 to A.1 (child mortality). A theory/mechanism stream of 360
records feeds §2. The 283 unretrieved identified-core records and the 667 associational records are the
RA extraction backlog.

---

## 5. The ideal design, and the distance from it

### 5.1 The ideal estimand

The completed fertility of a population under its actual son-preference norm, minus the completed
fertility of the same population under a counterfactual norm that valued sons and daughters equally,
holding constant the desired number of children, contraceptive access, and child survival — reported
separately for regimes with and without sex-selection technology, and separately by region.

### 5.2 The design that would identify it

Exploit variation in the sex of children that is as-good-as-random (the sex of the first or of early
births) to trace parity progression by sex composition; and exploit an exogenous shock to the cost of
sex selection (the staggered arrival of ultrasound, a sex-selection ban, a policy reform) to separate
the fertility channel from the sex-ratio channel. Measure both outcomes — births and the sex ratio at
birth — so the substitution is netted rather than half-observed.

### 5.3 The distance table

| Requirement | Best extracted evidence | Distance |
|---|---|---|
| As-good-as-random sex variation | Dahl & Moretti (GBG vs GBB); Anukriti-Bhalotra-Tam (firstborn sex); Almond-Li-Zhang (firstborn-girl interaction) | **Small** — the core designs meet this |
| Exogenous shock to sex-selection cost | Almond-Li-Zhang (land reform); Anukriti-Bhalotra-Tam (ultrasound diffusion) | **Small–moderate** — quasi-experimental, not a single clean cutoff |
| Both outcomes measured (substitution netted) | Anukriti-Bhalotra-Tam (fertility + attenuation); Almond-Li-Zhang (SRB + fertility null) | **Small** in the two best studies; absent elsewhere |
| Separated from child mortality (surviving-son) | Partial (Almond-Li-Zhang, Anukriti control; Sahni cannot) | **Moderate** |
| Pre-modern / natural-fertility setting | None extracted; all identified core is modern | **Large** — the PM gap |
| Completed (quantum) fertility, not spacing/period | Anukriti (completed sibling size); Dahl-Moretti (near-completed CA) | **Small–moderate** |
| Global coverage weighted by norm intensity | US, China, India, Vietnam, Indonesia, Nigeria extracted | **Moderate** — Asia well covered, PM and Korea/Caucasus un-extracted |

---

## 6. Included studies

Nine curated identified-core studies were full-text read (`extraction/son-preference-cultural.csv`,
`-fulltext-screen.csv`, `-risk-of-bias.csv`). They span the three primary cells and the full regional
gradient from strong preference (China, India) through weak (Nigeria) to absent (Indonesia).

| Study | Region / era | Design | Cell | RoB | Verdict |
|---|---|---|---|---|---|
| Dahl & Moretti 2008 | US + intl / SDT | revealed stopping, sex as-good-as-random | differential stopping | LOW | **SURVIVES** |
| Almond, Li & Zhang 2013 | rural China / SDT | land-reform natural experiment | sex-sel. substitution | LOW | **SURVIVES** |
| Anukriti, Bhalotra & Tam 2021 | India / SDT | DDD, firstborn sex × ultrasound diffusion | stopping + substitution | MODERATE | **SURVIVES** |
| Jiang et al. 2017 | China / SDT | descriptive SRB-by-birth-order decomposition | differential stopping | SERIOUS | **SURVIVES (descriptive)** |
| Kevane & Levine 2003 | Indonesia / SDT | revealed-behaviour tests vs biological benchmark | differential stopping | MODERATE | **SURVIVES (null)** |
| Sahni et al. 2008 | Delhi / SDT | single-hospital SRB time-series | sex-sel. substitution | SERIOUS | **WEAK** |
| Fayehun et al. 2011 | Nigeria / FDT | cross-sectional spacing logistic | differential stopping | SERIOUS | **WEAK (null)** |
| Anukriti 2018 (appendix) | India / SDT | trade-off model + selection tests (main paper on backlog) | substitution | — | **CONTEXT** |
| Iversen & Palmer-Jones 2018 | India / SDT | cable-TV panel (attitudes) | norm intensity | — | **CONTEXT** |

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

Son preference really does cause couples to have more children where the norm is strong, and the best
studies identify it cleanly. In the United States, where the preference is mild, two-daughter families are
2–5 % more likely to have another child than two-son families. Run on the same logic in Asia, the effect
is an order of magnitude larger — China +54 %, Vietnam +24 %. In India, families whose first child was a
girl had 0.155 more births than families whose first child was a boy, before ultrasound. But that same
Indian gap shrank by 40–57 % once ultrasound spread, and in rural China a reform that intensified son
preference raised sex-selective abortion without raising fertility at all. Where couples can choose the
sex of a birth, the preference stops adding children and starts subtracting girls. And the whole effect
is regional: it is absent in Indonesia and weak in Nigeria.

### 7.2 The estimate

The estimates are not poolable — they run across probability-of-next-birth (linear probability), completed
birth counts, sex-ratio levels, and odds ratios, in different regions and regimes. The synthesis is
therefore structured-narrative, organized around the three findings the evidence supports jointly.

**Finding 1 — the differential-stopping effect is real and identified.** Dahl & Moretti, exploiting the
as-good-as-random sex of children, find US all-girl families 2–5 % more likely to have another birth
(two girls vs two boys: +0.89 pp on P(3rd) in the Census, +1.26 pp in near-completed California data; the
clean GBG-vs-GBB estimate is +0.69 pp), with the effect growing at higher parities. Anukriti, Bhalotra &
Tam find a +0.155-birth firstborn-girl gap in India (RoB MODERATE). Both are LOW-to-MODERATE risk of bias.

**Finding 2 — the effect is an order of magnitude larger in Asia, and modest in the West.** The single
most useful number for demographic weight is the cross-country gradient Dahl & Moretti recover with one
design: US +2–5 %, Mexico +2.3 pp, Kenya +2.0 pp, Vietnam +8.7 pp, China +19.9 pp (+54 %). The preference
is a first-order fertility force only in South and East Asia, and even there it moves completed fertility
by a fraction of a child.

**Finding 3 — sex selection substitutes for the fertility effect.** Anukriti, Bhalotra & Tam show the
firstborn-girl fertility gap attenuates 40–57 % as ultrasound diffuses (−0.088 early, −0.112 late).
Almond, Li & Zhang show a land reform that raised the value of sons increased the probability a second
child is male by 3.0 pp (with a clean first-birth placebo null) while leaving fertility unchanged
(−0.027 births, n.s.) — the preference expressed entirely through sex selection. The descriptive
birth-order SRB gradients (Jiang: near-normal first-birth SRB rising to ~159 at third-and-higher births;
Sahni: second-child SRB of 716 girls per 1,000 boys after a firstborn girl) are the mechanism's
fingerprint.

**The two null/absence results discipline the magnitude.** Fayehun finds no national son-preference
spacing effect in Nigeria (and it is confounded with lactational amenorrhoea). Kevane & Levine document
a careful, well-powered *absence* of son preference in Indonesian fertility across stopping, family-size,
and spacing tests — with son-favouring gaps appearing only in schooling and inheritance, not births. Son
preference is not a universal human fertility force; it is a regional norm.

---

## 8. Demographic significance

The verdict distinguishes the effect on **fertility levels** (this chapter's estimand) from the effect on
the **sex ratio at birth** (a composition outcome that belongs to A.10). Son preference's demographic
importance for fertility is real but bounded — by region and by the substitution regime.

### 8.1 Pre-modern (PM)

**MINOR (localised).** In genuine natural-fertility populations couples did little deliberate stopping, so
the differential-stopping channel is weak; the pre-modern expression of a strong son preference was
largely female infanticide and neglect (a mortality margin, A.1/OFF_OUTCOME), not extra births. Where the
norm was strong (historical South and East Asia) it plausibly raised completed fertility modestly through
differential continuation, but no extracted study identifies this in a PM setting. Negligible outside the
strong-preference belt.

### 8.2 First Demographic Transition (FDT)

**MINOR–MODERATE (South/East Asia).** During the fertility transition in strong-preference regions son
preference sustained higher fertility than would otherwise have prevailed — couples kept trying for sons
as they began to limit family size — slowing the transition where the norm was strong. Anukriti-Bhalotra-
Tam's pre-ultrasound +0.155-birth gap and Dahl-Moretti's China/Vietnam extensions size this at a fraction
of a birth per woman, meaningful in the highest-preference settings (rural North India, China, Korea) and
negligible in sub-Saharan Africa (Fayehun) and Southeast Asia (Kevane & Levine).

### 8.3 Second Demographic Transition (SDT)

**MINOR.** In the sex-selection era the preference's contribution to fertility *levels* is small and
shrinking: it is substituted away by sex-selective abortion (Almond-Li-Zhang fertility null; Anukriti
40–57 % attenuation). Its principal SDT footprint is the skewed sex ratio at birth — a composition effect
outside the TFR estimand and the province of A.10. A residual fertility effect persists among couples
without access to or moral acceptance of sex selection, but it is a second-order contributor to any
country's SDT fertility level.

---

## 9. GRADE rating

Three independent raters scored the causal credibility that son-preference variation causes fertility
variation in each phenomenon (`extraction/son-preference-cultural-grade.json`).

| Phenomenon | Consensus | Agreement |
|---|---|---|
| PM | **LOW** | majority (2/3); one VERY LOW dissent (no PM natural-fertility identified estimate) |
| FDT | **MODERATE** | unanimous (3/3) |
| SDT | **MODERATE** | majority (2/3); one LOW dissent (fertility-level effect small and substituted) |

The mechanism is causally secure where the norm is strong — the near-random sex of children and the
staggered arrival of ultrasound give the core studies genuine identification. It is not rated higher as
an *explanation* of the transitions for two reasons the evidence itself supplies: the effect is
regime-dependent (it converts from a fertility cause to a sex-ratio cause once sex selection is available)
and region-specific (null in the two non-Asian settings extracted). PM is held to LOW because the
differential-stopping channel requires the deliberate stopping that natural-fertility populations lacked,
and the extracted identified core is entirely modern.

---

## 10. Verdict

**Son preference is a genuine, well-identified cause of higher fertility — but a regional one that a
technology switches off.** Where the norm is strong and sex selection is unavailable, couples trying for
sons have measurably more children: a few percent in the mild-preference West, tens of percent in South
and East Asia. This is one of the cleaner causal findings in the review, resting on the as-good-as-random
sex of children rather than on contested identifying assumptions. Its demographic weight on fertility
levels, however, is MINOR-to-MODERATE and confined to the strong-preference belt, and in the
sex-selection era it does not so much raise the birth rate as skew the sex ratio at birth — the same
preference, a different footprint. It is not a first-order explanation of any of the three global
transitions; it is a regionally important modifier that slowed fertility decline in Asia and now shows up
in that region's missing girls.

---

## 11. Open questions

- **The quantum contribution, netted against substitution.** No extracted study reports the completed-
  fertility contribution of son preference by region and era *after* netting the sex-selection substitution
  — the number the demographic-significance verdict most needs.
- **The pre-modern channel.** Whether son preference raised PM completed fertility through differential
  continuation, or only skewed survival through female infanticide, is unresolved on extracted evidence and
  requires a natural-fertility study that separates the two.
- **Korea and the Caucasus.** The clearest recent test cases of a rising-then-falling son preference (Chung
  & Das Gupta on Korea; the South Caucasus SRB spike) are on the RA backlog, not extracted.
- **The marquee anchors.** Ben-Porath & Welch 1976, Clark 2000, Arnold-Choe-Roy 1998, Jayachandran 2017
  (VoR), Lin-Liu-Qian 2014, and Ebenstein 2010 are paywalled and un-extracted; they would sharpen the
  FDT and SDT ratings.

---

## 12. References

Core extracted studies (full metadata in `extraction/son-preference-cultural.csv`):

- Dahl, G. B., & Moretti, E. (2008). The Demand for Sons. *Review of Economic Studies* 75(4):1085–1120.
- Almond, D., Li, H., & Zhang, S. (2013/2017). Land Reform and Sex Selection in China. NBER WP 19153.
- Anukriti, S., Bhalotra, S., & Tam, E. H. F. (2021). On the Quantity and Quality of Girls: Fertility,
  Parental Investments, and Mortality. Working paper.
- Jiang, Q., Yu, Q., Yang, S., & Sánchez-Barricarte, J. J. (2017). Changes in Sex Ratio at Birth in China:
  A Decomposition by Birth Order. *Journal of Biosocial Science* 49(6):826–841.
- Kevane, M., & Levine, D. I. (2003). Changing Status of Daughters in Indonesia. CIDER WP C03-126.
- Sahni, M., et al. (2008). Missing Girls in India: Infanticide, Feticide and Made-to-Order Pregnancies.
  *PLoS ONE* 3(5):e2224.
- Fayehun, O. A., Omololu, O. O., & Isiugo-Abanihe, U. C. (2011). Sex of Preceding Child and Birth Spacing
  among Nigerian Ethnic Groups. *African Journal of Reproductive Health* 15(2):79–90.
- Anukriti, S. (2018). Financial Incentives and the Fertility-Sex Ratio Trade-off. *AEJ: Applied Economics*
  10(2):27–57 [online appendix extracted; main paper on backlog].
- Iversen, V., & Palmer-Jones, R. (2018). All You Need is Cable TV? *Journal of Development Studies*.

Registry-seminal anchors on the RA backlog: Ben-Porath & Welch (1976), Das Gupta (1987), Arnold, Choe &
Roy (1998), Clark (2000), Jayachandran (2017), Chung & Das Gupta (2007), Ebenstein (2010),
Lin, Liu & Qian (2014).

---

## Provenance and standing caveats

This chapter was produced by the reproducible pipeline in `source/build/goldset/88_d2c_*`–`99_d2c_*`
(scout → frame probe → cold-start anchors → citation frame → production frame → blinded screen → OA
retrieval → extraction → risk of bias) plus this synthesis. Every count above regenerates from those
scripts and the committed search-logs and extraction CSVs.

**Interim standing.** The draft rests on 9 of 380 identified-core studies (97/380 OA-retrieved); the
marquee paywalled anchors and the 667 associational records are the RA extraction backlog. The direction
and structure of the verdict — a real, well-identified, regionally-bounded effect that sex selection
converts from a fertility cause into a sex-ratio cause — is unlikely to change with more extraction, but
the FDT/SDT demographic-significance magnitudes are the most likely to move once the Asian anchors and the
substitution-netted quantum estimates are in. Single-reader extraction and risk-of-bias; RA 5–10 %
spot-check, the title/abstract gate, lay-readability review, and PI sign-off are all still owed.
