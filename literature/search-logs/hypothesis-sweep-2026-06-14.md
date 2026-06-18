# Hypothesis Sweep — 2026-06-14

**Purpose:** Identify explanations for fertility decline appearing in X bookmarks and recent literature that are missing from or underspecified in HYPOTHESES-v4.md. Output feeds HYPOTHESES-v5.md after PI review.

**PI review required before v5 is written.**

---

## 1. Sources Searched

| Source | Description | Scope |
|--------|-------------|-------|
| `mybookmarks_20240611_163413.csv` | X bookmark export (June 2024) | 222 tweets total, 134 fertility-relevant |
| `XBookmarksExporter_26_2026-02-04_10-57-59.xlsx` | X bookmark export (Feb 2026) | 26 tweets, all urban-economics / unrelated to fertility |
| Literature sweep via Explore agent | Web search of recent academic and grey literature (2020–2026) | ~30 sources reviewed |

**Note on the XLSX:** This file appears to be a general academic bookmark export (urbanization, public housing, cartels), not a fertility-curated set. Zero entries are fertility-relevant. The CSV is the fertility-curated source.

---

## 2. Bookmark Hypotheses Mapped to v4

The 134 fertility-relevant tweets from the CSV cluster around the following hypothesis themes. Most map cleanly to existing v4 entries; the rightmost column flags what is genuinely new.

| # | Theme | Handles / Evidence | v4 Mapping | Status |
|---|---|---|---|---|
| 1 | Tempo vs. quantum accounting | @lymanstoneky (thread) | A.11 Tempo Effects | ✓ in v4 |
| 2 | Housing costs → lower fertility | @MoreBirths, @lymanstoneky, @PhilWalkable | C.2.c Housing Costs | ✓ in v4 |
| 3 | Housing regulations restrict supply → cost → fertility | @lymanstoneky (NLSY paper; zoning regulation paper) | C.2.c | ✓ in v4 |
| 4 | Childcare availability / deregulation | @VincentGeloso, @lymanstoneky, @MoreBirths | C.2.a Childcare Cost | ✓ in v4 |
| 5 | Income effect and fertility (J-curve, normal good puzzle) | @MoreBirths, @lymanstoneky | C.1.a Income Effect | ✓ in v4 |
| 6 | Female labor force participation / child penalty | @s8mb, @cremieuxrecueil | C.2.e Female Wage | ✓ in v4 |
| 7 | Parental leave / pronatalist policy transfers | @SteveStuWill, @WestminsterPup, @MoreBirths | C.2.d Tax and Transfer | ✓ in v4 |
| 8 | Heritability of fertility preferences | @jonatanpallesen, @cremieuxrecueil, @robinhanson, @DouthatNYT | A.18 Genetic/Heritable Variation | ✓ in v4 |
| 9 | Prestige-bias cultural evolution | @robinhanson (Richerson & Boyd thread) | D.1.c Cultural Evolution | ✓ in v4 |
| 10 | Female empowerment / second-wave feminism ended baby boom | @NoahCarl90 | D.2.a Female Empowerment | ✓ in v4 |
| 11 | Marriage timing and union formation | @cremieuxrecueil (1940–79 cohort timing shifts) | A.7 Marriage Timing | ✓ in v4 |
| 12 | Marriage market and exposure to marriage | @robinhanson ("decline directly attributed to decreasing exposure to marriage") | C.7.a Marriage Market | ✓ in v4 |
| 13 | Culture beats policy (relative effectiveness) | @RuxandraTeslo, @robinhanson, @MoreBirths | D.1 (general) | ✓ in v4 — not a hypothesis, a finding |
| 14 | East Asian development model (strong states vs. econ vs. culture) | @_alice_evans | C, D multiple | ✓ covered across entries |
| 15 | Child mortality and insurance demand | — | A.1 Child Mortality Decline | ✓ in v4 |
| 16 | Son preference | — | D.2.c Son Preference | ✓ in v4 |
| 17 | Pronatalist policies effectiveness | @_alice_evans (Hungary, Czech, Poland), @MoreBirths | C.2.d + D.1.d | ✓ in v4 |
| 18 | Contraception / abortion access | @MoreBirths (Roe v. Wade effect), @lymanstoneky (Africa RCT) | A.2–A.5 | ✓ in v4 |
| 19 | Unfulfilling romance → childless singles | @_alice_evans ("if romance is unfulfilling, we should anticipate steep rise in childless singles") | Partially A.7 + C.7.a | ⚠ UNDERSPECIFIED — relationship quality as distinct mechanism |
| 20 | **Student debt → fewer children** | @MoreBirths ("having student debt results in significantly fewer children than women without") | C.3.e Credit Constraints (partial) | **NEW — deserves own entry** |
| 21 | **Co-residence with parents / not living independently** | @jonatanpallesen ("one of the larger factors of low birth rates is young adults not living alone"), @MoreBirths (group quarters) | C.2.c + C.2.g (partial) | **NEW — distinct proximate or cost mechanism** |
| 22 | **Population density / apartment living as fertility reducer** | @s8mb, @bswud, @MoreBirths, @lymanstoneky (extensive density debate) | C.2.g Urbanization (partial, but urbanization ≠ density per se) | **UNDERSPECIFIED — density effect distinct from urbanization shift** |
| 23 | **Divorce liberalization → fertility decline** | @MoreBirths ("following divorce liberalization starting in 1970, birth rates fell") | D.2.b Marriage Norms (partial) | ⚠ UNDERSPECIFIED — partnership instability as explicit mechanism |
| 24 | Childlessness mostly involuntary | @lymanstoneky ("best predictor of childlessness is not having a partner, not wanting to be childless") | A.7 + C.7.a | ✓ covered as finding, not root cause |
| 25 | Ozempic / GLP-1 restoring fertility via weight | @lymanstoneky | B.4 Obesity/Metabolic (reverse channel) | ⚠ INTERESTING — a mitigating intervention, not a root cause |
| 26 | Urbanization / East Asian megacity model | @lymanstoneky, @MoreBirths | C.2.g Urbanization | ✓ in v4 |

---

## 3. Novel Hypotheses from Literature Sweep (Not in v4)

These were identified via web search and academic database query (Explore agent). Each has at least one citable source published 2016–2026.

| # | Hypothesis | Mechanism | Key Sources | Proposed v5 Location |
|---|---|---|---|---|
| L1 | **Smartphone / digital leisure substitution** | Smartphones replace in-person social interaction, reduce coital frequency, and substitute leisure time that would otherwise produce couple-time and sex → lower fertility; also reduces spontaneous couple-formation. Causal identification: AT&T 3G carrier rollout IV. | Myers & Hooper NBER w35310 (2026): accounts for 33–52% of US decline since 2007 | C (economic, leisure opportunity cost) or new Section F (Technology) |
| L2 | **Climate anxiety / eco-doomerism** | Intentional childlessness driven by negative future orientation, fear that the world will be uninhabitable for the next generation, or ethical concerns about carbon footprint of additional humans | Bastianelli et al. (2025, *J. Marriage & Family*); Britt et al. (2025, *Genus*); OSCE PA 2025 | D.1 (Values, Ideology) — new entry D.1.e |
| L3 | **Dating app matching failure** | Online dating platforms increase contact volume but reduce conversion to committed partnerships (match-abundance paradox, paradox of choice, commodification of partners) → lower union formation rates → lower fertility | Wharton Knowledge (2026); @MoreBirths; academic work on online dating and partnership stability | A (proximate: union formation mechanism) or C.7.a expansion |
| L4 | **Mental health / anxiety epidemic** | Population-level rise in diagnosed and undiagnosed mood/anxiety disorders impairs pair-bond formation, sexual function, and reproductive intention, reducing fertility independently of economic channels | IFS (2024); *Human Reproduction Open* (2024); OSCE PA 2025 | New entry — bridges D and C; possibly D.1.e or new D.3 (Psychological Distress) |
| L5 | **Despair and hopelessness** | Case-Deaton "deaths of despair" framework applied to fertility: in populations experiencing declining economic and social prospects, long-term commitments (marriage, children) are rationally deferred indefinitely. Distinct from general economic uncertainty (C.5.a) because the channel is subjective hopelessness, not objective risk. | Platt & Sterling EurekAlert 2024; Case & Deaton 2020 extended to fertility | C.5 expansion or new D.3 (Psychological Distress) |
| L6 | **Antidepressants / pharmacological subfecundity** | SSRI and related psychiatric medications cause sexual dysfunction (behavioral: reduced libido, delayed orgasm) and potentially endocrine suppression (biological: altered hormone levels), reducing coital frequency and biological fecundity | Nørr et al. *Andrology* 2016; Beeder & Bhatt PMC scoping review 2025; Tiefer 2001 | B (Biological) — new B.6 |
| L7 | **Microplastics / PFAS** | Microplastics and per- and polyfluoroalkyl substances (PFAS) detected in follicular fluid, seminal plasma, and placental tissue; associated with lower sperm quality, disrupted ovarian folliculogenesis, and impaired implantation; exposure is ubiquitous and rising | Zhao et al. *Fertility & Sterility* (2025); *Lancet* Commission on Reproductive Health (2025); Scientific Reports 2025 | B.2 expansion OR new B.6/B.7 (separate from existing B.2) |
| L8 | **Student debt** | Education debt service during prime childbearing years raises the effective cost of household formation, displacing funds that could cover the direct costs of a child; delays marriage and homeownership, which delays fertility | Contemporary Families / TICAS (2025); Future Family 2024; @MoreBirths tweet confirmed | C.3.e expansion OR new C.2.h |
| L9 | **Political polarization / ideological sorting on the mating market** | Increasing gender gap in partisan affiliation (women shifting left, men shifting right) reduces the pool of compatible partners along ideological lines → fewer cross-partisan couples form → lower aggregate fertility | Dahl & Lu UCSD working paper 2024; IFS policy brief 2024; YouGov data | C.7.a expansion or new Cultural entry D.1.e or D.2.e |
| L10 | **Loneliness / social isolation** | Rising structural loneliness (fewer friendships, less community participation) reduces casual encounters that could develop into romantic partnerships, lowers coital frequency among singles, and reduces the emotional context that makes childbearing desirable | OSCE PA 2025; IFS UK 2024 | Proximate (A) or Cultural (D) — overlaps with L3 (dating apps) and L1 (smartphones) |
| L11 | **Declining biological fecundity (idiopathic)** | Population-level trend toward lower unassisted conception rates across both sexes that cannot be fully explained by behavioral postponement, identified exposures, or known pathology; separate from existing B entries which identify a specific toxin/condition | *Lancet* Commission on Reproductive Health 2025; *Fertility & Sterility* 2025; Scientific Reports 2025 | Section B reframe or new B entry |
| L12 | **Remote work (mitigating / protective factor)** | Flexible work arrangements reduce work-family conflict and time pressure, enabling higher fertility among women who want children; not a cause of decline but a policy-relevant mitigant | VoxEU/CEPR (Amici et al. 2025): +0.32 estimated effect; King's College 2025 | C.2.e note (mitigating intervention, not root cause) |

---

## 4. Structural Questions for PI

Before writing v5, three design decisions need to be made:

### Q1: Should Technology be a new root-cause section (Section F)?

**The case for F:** Smartphones, dating apps, and pornography share a common upstream cause — digital technology reshaping the behavioral ecology of sex, partnership, and reproduction. This is mechanistically distinct from Economic (opportunity cost), Biological (fecundity), and Cultural (values). If we plan to give each mechanism a full GRADE chapter, they are different enough to warrant a dedicated section.

**The case against:** These mechanisms are arguably economic (time cost, leisure substitution) and cultural (changing norms around dating/sex). Creating a new section for technology means every new technology wave would argue for a new section. Dating apps → C.7.a. Smartphones → C.2.e or C.5.a. Pornography → A.14 (coital frequency mechanism). Distribute into existing categories.

**Recommendation:** If the goal is to cover whether technology itself is a new class of root cause, create Section F. If each technology is a specific instrument for a more general mechanism already in the taxonomy, distribute.

---

### Q2: Should Psychological Distress become a new sub-section (D.3)?

**Four candidates cluster:** Climate anxiety (L2), Mental health epidemic (L4), Despair/hopelessness (L5), Loneliness/social isolation (L10). They share the mechanism: psychological state → reduced reproductive intention or impaired partnership formation. This is distinct from:
- Economic uncertainty (C.5.a) — which is objective risk, not subjective affect
- Postmaterialism (D.1.a) — which is a value shift, not a pathology
- Cultural evolution (D.1.c) — which is about imitation, not distress

**Recommendation:** Create **D.3 — Psychological and Existential Distress** with entries for climate anxiety, mental health epidemic, and social isolation (group despair/hopelessness with economic uncertainty or make it a D.3 entry depending on how strong the Case-Deaton evidence is for fertility specifically).

---

### Q3: Microplastics/PFAS — expand B.2 or separate entry?

**Current B.2** covers "endocrine disruptors and environmental toxins" with seminals: Colborn 1996, Skakkebaek 2016, Swan 2021. These mostly concern phthalates, BPA, pesticides, and the general sperm-count trend.

**New literature (2025):** Microplastics and PFAS have been detected directly in reproductive tissue (follicular fluid, seminal plasma, placenta), representing a distinct exposure class with different kinetics, ubiquity, and regulatory profile. *Fertility & Sterility* 2025 is a major new source.

**Recommendation:** Split into **B.2** (legacy synthetic organic endocrine disruptors: phthalates, BPA, pesticides, organic solvents) and **B.6** (microplastics and PFAS: ubiquitous persistent exposures in reproductive tissues, 2020s literature). Two entries because the literatures have diverged and PFAS/microplastic exposure pathways and regulatory implications are different from legacy chemical exposure.

---

## 5. Proposed v5 Additions

The following are the entries I recommend adding to HYPOTHESES-v5.md. The proposals are ordered from highest- to lowest-priority (assessed by: quality of causal evidence, conceptual distinctness from existing entries, likely demographic magnitude, and relevance to all three phenomena).

Each entry includes: proposed outline code · slug · 1-sentence claim · key seminals · cross-refs · note on what's new.

---

### HIGH PRIORITY (add to v5)

**C.3.g — Student Debt and Household Formation Constraint**
- **slug:** `student-debt-household-formation`
- **claim:** Education debt service during prime childbearing years raises the effective cost of household formation — delaying marriage, homeownership, and childbearing — and produces lower completed fertility in cohorts that entered adulthood under the post-2000 student-debt regime.
- **seminal:** TICAS / Contemporary Families 2025; Future Family 2024; Butcher & Goldsmith (forthcoming)
- **cross-ref:** C.3.e (Credit Constraints — related but distinct: student debt is a specific asset-sheet liability, not a market friction); C.2.c (Housing Costs — compounded delay)
- **note:** Distinct from C.3.e because the mechanism is prior-debt burden (a liability on the balance sheet), not current inability to borrow. Confirmed by @MoreBirths tweet ("Having student debt at the end of college results in women having significantly fewer children").

---

**A.23 — Co-Residence with Parents and Delayed Household Formation**
- **slug:** `co-residence-parents-household-delay`
- **claim:** Extended co-residence of young adults with parents — driven by housing costs, weak labor markets, or cultural norms — delays the formation of independent households and thereby delays or prevents fertility.
- **seminal:** Baizan 2006; Fokkema and Liefbroer 2008; @jonatanpallesen (X thread 2024); @MoreBirths (X thread 2024)
- **cross-ref:** C.2.c (Housing Costs — one driver); A.7 (Marriage Timing — delayed union formation); C.2.g (Urbanization — strong in Southern Europe and East Asia)
- **note:** Prominently flagged in the X discourse by @jonatanpallesen ("one of the larger factors") and @MoreBirths. Distinct from housing costs per se (C.2.c): the mechanism here is that co-residence prevents partnership formation and sexual autonomy independently of the cost channel.

---

**L1 → New entry: C.2.h or F.1 — Smartphone / Digital Leisure Substitution**
*(see Q1 above for section decision)*
- **slug:** `smartphone-digital-leisure-substitution`
- **claim:** Widespread smartphone adoption substitutes screen-based leisure for in-person social interaction, reduces spontaneous couple-formation encounters, lowers coital frequency among partnered adults, and raises the opportunity cost of child-rearing attention time — producing lower fertility through at least three behavioral pathways.
- **seminal:** Myers & Hooper NBER w35310 (2026): 33–52% of US TFR decline 2007–2022 attributable to smartphone diffusion (AT&T rollout IV); Twenge 2017 (iGen)
- **cross-ref:** A.14 (Coital Frequency — one proximate pathway); C.7.a (Marriage Market — reduced couple-formation); D.1.a (Postmaterialism — cultural complementarity with screen lifestyle)
- **note:** Already flagged in v4's "Items for future addition." The Myers & Hooper NBER paper provides the strongest causal identification yet. Three distinct mechanisms (social isolation, pornography substitution, doomscrolling leisure) could be sub-entries.

---

**D.1.e — Climate Anxiety and Eco-Doomerism**
- **slug:** `climate-anxiety-eco-doomerism`
- **claim:** A growing share of reproductive-age adults cite climate change as a reason to forgo or limit childbearing, citing fear of an uninhabitable future for their children, ethical concerns about per-capita carbon footprint, or a generalized ecological pessimism — producing intentional childlessness that is distinct from economic or career motivations.
- **seminal:** Bastianelli et al. (2025, *J. Marriage & Family*); Britt et al. (2025, *Genus*); YouGov surveys 2020–2024 (UK, Italy, US)
- **cross-ref:** D.1.a (Postmaterialism — shares anti-natalist value orientation); D.3.a (Mental Health / Anxiety — may co-occur clinically)
- **note:** New ideational channel distinct from postmaterialism (D.1.a): the mechanism is fear/pessimism about the future world, not a positive preference for self-actualization. Literature emerging 2020–2025; strongest in younger cohorts and more educated women.

---

**B.6 — Microplastics and PFAS in Reproductive Tissues**
*(conditional on Q3 approval to split B.2)*
- **slug:** `microplastics-pfas-reproductive`
- **claim:** Microplastic particles and per- and polyfluoroalkyl substances (PFAS) have been detected in follicular fluid, seminal plasma, and placental tissue; in vitro and epidemiological evidence associates these exposures with reduced sperm quality, impaired ovarian folliculogenesis, and lower implantation rates — a distinct and rapidly emerging class of endocrine-disrupting exposure.
- **seminal:** Zhao et al. *Fertility & Sterility* (2025); *Lancet* Commission on Reproductive Health (2025); Yang et al. *Scientific Reports* (2025)
- **cross-ref:** B.2 (Endocrine Disruptors — legacy synthetic organics; now distinguished from PFAS/microplastics); A.16 (Paternal Age and Sperm Quality — sperm quality outcome)
- **note:** Distinct from B.2 because (a) the chemical class, exposure pathway, and elimination kinetics differ substantially; (b) tissue-level detection is a step change from blood-serum association studies; (c) regulatory implications differ. 2025 literature warrants a dedicated entry.

---

### MEDIUM PRIORITY (add to v5 with shorter entries)

**D.3.a — Psychological Distress and Mental Health Epidemic**
*(conditional on Q2 approval to create D.3)*
- **slug:** `mental-health-anxiety-epidemic`
- **claim:** Rising prevalence of clinically diagnosed and subclinical anxiety, depression, and related mental health conditions impairs the pair-bonding, sexual function, and reproductive intention of reproductive-age adults, reducing fertility through psychological pathways distinct from economic uncertainty.
- **seminal:** IFS (2024); *Human Reproduction Open* (2024); APA 2023 annual survey data
- **cross-ref:** C.5.a (Economic Uncertainty — partially overlapping but distinct channel); D.1.e (Climate Anxiety — specific ideational variant)
- **note:** The mechanism is clinical/psychological, not cultural or economic. May partially mediate other hypotheses (smartphones → isolation → depression → lower fertility).

**D.3.b — Despair, Hopelessness, and Reproductive Deferral**
*(conditional on Q2)*
- **slug:** `despair-hopelessness-fertility`
- **claim:** In communities experiencing declining economic prospects, social dissolution, and intergenerational downward mobility, long-term commitments including marriage and childbearing are indefinitely deferred — a fertility dimension of the "deaths of despair" phenomenon.
- **seminal:** Case & Deaton (2020); Platt & Sterling (2024)
- **cross-ref:** C.5.a (Economic Uncertainty — shares objective economic channel); D.3.a (Mental Health — shares psychological channel)
- **note:** Differs from C.5.a: the mechanism is subjective hopelessness about the future, not rational uncertainty aversion. Differs from D.3.a: applies at community/population level, not individual clinical level.

**B.6 / B.7 — Antidepressants and Pharmacological Subfecundity**
- **slug:** `antidepressants-ssri-subfecundity`
- **claim:** SSRI and related antidepressant medications commonly reduce libido and delay or prevent orgasm (behavioral pathway) and may suppress gonadotropin and testosterone levels (endocrine pathway), reducing coital frequency and biological fecundity in a growing share of the reproductive-age population.
- **seminal:** Nørr et al. *Andrology* (2016); Beeder & Bhatt PMC scoping review (2025); Clayton et al. *J. Clinical Psychiatry* (2002)
- **cross-ref:** A.14 (Coital Frequency — behavioral proximate outcome); B.2 (Endocrine Disruptors — analogous endocrine pathway); D.3.a (Mental Health — the condition treated)
- **note:** Bridges biological and proximate sections: the medication is a biological/pharmacological cause; the proximate outcome is coital frequency. SSRI prevalence has grown substantially in the SDT era, especially among women of reproductive age.

---

### LOWER PRIORITY / DISCUSS WITH PI

**C.7.b or A.24 — Dating App Matching Failure**
- **slug:** `dating-app-matching-failure`
- **claim:** Online and app-based dating increases the volume of potential contacts but reduces conversion to committed partnerships, via match-abundance effects, strategic delay, and commodification of partners — reducing union formation rates and fertility.
- **seminal:** Rosenfeld & Thomas 2012 (online dating and relationship stability, early era); @MoreBirths discourse; Wharton Knowledge 2026
- **cross-ref:** C.7.a (Marriage Market — related mechanism); A.7 (Marriage Timing — proximate outcome); L1 Smartphones (technology-upstream driver)
- **note:** The causal chain runs from the technology (smartphones/apps) to a proximate mechanism (reduced union formation). Whether this is an independent hypothesis or a sub-mechanism of the smartphone entry depends on Q1 above. Consider as F.1.b if Technology section is created.

**D.2.e or C.7.b — Political Polarization and Ideological Sorting on the Mating Market**
- **slug:** `political-polarization-mating-market`
- **claim:** Growing gender-partisan sorting — women shifting left, men shifting right, at historically large magnitudes — reduces the pool of politically compatible partners for cross-partisan couples, reducing match rates and fertility.
- **seminal:** Dahl & Lu UCSD working paper (2024); IFS 2024; YouGov UK/US data
- **cross-ref:** C.7.a (Marriage Market — a new friction in market clearing); D.1.a (Postmaterialism — related ideational polarization)
- **note:** Quantitative evidence emerging (Dahl & Lu); mechanism is plausible but causal identification is challenging. Evidence stronger for US than Europe. Consider as an expansion of C.7.a or a sub-entry under a D.3 or D.2.e cultural entry.

**C.2.g-note or new entry — Population Density and Apartment Living**
- **slug:** `population-density-apartment-living`
- **claim:** Higher residential population density reduces fertility through several channels: space constraints on raising children (apartment living vs. single-family homes), reduced outdoor play areas, and the high cost-per-square-foot of additional family space in dense cities.
- **seminal:** Mulder & Billari 2010 (Europe density-fertility); @MoreBirths and @lymanstoneky (active debate on X 2024); @s8mb (Works in Progress 2024 debunking paper)
- **cross-ref:** C.2.c (Housing Costs — cost channel); C.2.g (Urbanization — composition channel)
- **note:** There is active empirical debate in the X discourse: @s8mb wrote a Works in Progress piece arguing the density-fertility correlation doesn't hold in longitudinal data; @lymanstoneky finds no person-level NLSY effect. This may be a spurious relationship or confounded by income/housing markets. Include as an entry but note the contested status.

---

## 6. What Does Not Belong in v5

The following were identified in bookmarks or literature but are **not candidates for new v5 entries**:

| Item | Reason |
|---|---|
| Remote work as protective factor (L12) | A mitigating policy intervention, not a root cause of fertility decline; note under C.2.e if at all |
| Ozempic / GLP-1 restoring fertility | A medical intervention restoring fertility via obesity channel; belongs as a note under B.4, not a new entry |
| Sports team winning → birth rates | A behavioral curiosity (leisure substitution, coital frequency); too narrow and transient for a hypothesis chapter |
| Childlessness mostly involuntary | An empirical finding about the proximate determinant of childlessness, not a new root-cause hypothesis |
| Culture beats policy | A meta-finding about relative effectiveness; not a hypothesis about why fertility falls |
| Immigration / emigration (small-country population drain) | Population-level flow, not a cause of per-woman fertility change; outside scope |

---

## 7. Summary: New Entries for v5

**Definite adds (8):**
1. C.3.g — Student Debt and Household Formation Constraint
2. A.23 — Co-Residence with Parents and Delayed Household Formation
3. New entry — Smartphone / Digital Leisure Substitution *(section TBD pending Q1)*
4. D.1.e — Climate Anxiety and Eco-Doomerism
5. B.6 — Microplastics and PFAS in Reproductive Tissues *(contingent on splitting B.2)*
6. B.7 — Antidepressants and Pharmacological Subfecundity *(or B.6 if B.2 not split)*
7. D.3.a — Mental Health / Anxiety Epidemic *(contingent on Q2)*
8. D.3.b — Despair and Hopelessness *(contingent on Q2)*

**Discuss with PI (3):**
- Dating App Matching Failure
- Political Polarization / Ideological Sorting on Mating Market
- Population Density / Apartment Living (contested empirically)

**V4 flagged items to add while we're at it:**
- War / conscription / military mobilization (already flagged in v4)
- Epidemics and pandemics as fertility shocks (already flagged in v4; COVID data now available)
- Air pollution as fecundity reducer (already flagged in v4; could merge with B entry)
- Migration / immigrant fertility convergence (already flagged in v4)

---

*Prepared by Claude Code, 2026-06-14. Awaiting PI review before v5 is produced.*
