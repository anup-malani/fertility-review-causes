# Search scope — despair and hopelessness

**Hypothesis:** D.3.c (HYPOTHESES-v5.md)
**Hypothesis slug:** `despair-hopelessness-fertility`
**Target phenomenon:** SDT only, and — as in B.7 — **a restricted sub-period within it**. See
"Phenomenon scope".
**Ticket:** TICK-069
**Status:** **DRAFTED, NOT FROZEN** (Shravan, 2026-08-18). Ten walls and thirteen estimand cells
specified. **Five calls are open for the PI, and two of them are load-bearing**: Call 1 (does the
chapter rate a signed claim?) and Call 2 (does mechanism-silent reduced-form evidence count as
evidence for this hypothesis at all?). Call 2 decides whether the primary evidence base is roughly
two studies or roughly a thousand. Anchors are sourced but not yet resolved through A3/A4.

Built on the B.6 (`microplastics-pfas-reproductive`) template, which inherits B.7's, B.5's, D.2.d's
and D.3.b's. Five constraints carry forward as design decisions rather than being rediscovered: the
taxonomy carries `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER`; **a wall whose discriminator is
invisible in a title or abstract is declared unenforceable up front** rather than trusted and audited
later; the forward-citation seed rule is uniform across seed types with no special case for routing
decoys; an arithmetic statement of the mechanism is an upper bound to be corrected, not the effect;
and **a chapter whose evidence sits on a different proposition from its claim rates the claim, not the
evidence.** The last of these is the governing constraint here, more so than in any chapter so far.

The scope below is written against a live reconnaissance pass over OpenAlex (2026-08-18; 60 probes,
**zero failed requests**, so every zero-hit count reported here is a genuine absence rather than a
refusal). Counts are regenerable via `source/build/goldset/147_d3c_recon_probe.py` and reported in
`despair-hopelessness-fertility-recon-probe.md`.

## Causal claim

In communities that have undergone chronic economic decline, social dissolution and intergenerational
downward mobility, long-term commitments — marriage, home-buying, childbearing — are indefinitely
deferred because the subjective sense of having a viable future has collapsed. Children are the
paradigmatic long-term investment; they require a belief that the future is worth investing in. Where
that belief is gone, childbearing is postponed indefinitely. The claimed channel is **not** rational
uncertainty aversion with a calculable return to normalcy (C.5.a) but a deeper extinction of
forward-looking orientation — the fertility dimension of the "deaths of despair" phenomenon.

D.3.c's difficulty is not B.6's (two hypotheses under one number) and not B.7's (a treatment whose
outcome belongs elsewhere). It is more basic, and the reconnaissance is unambiguous about it.

## The mechanism this chapter is named for is not measured in the literature that studies its treatment

This is the finding that shapes every downstream decision, so it is stated before the walls rather
than discovered during screening.

D.3.c is a claim about a **mechanism** — a subjective collapse of forward orientation — sitting
between a **treatment** (chronic community economic decline) and an **outcome** (deferred
childbearing). The reconnaissance measured all three legs.

| Leg | Probe | n |
|---|---|---|
| Treatment → outcome | place-based decline / deindustrialization / layoffs / China shock **AND** fertility | **1,539** |
| Mechanism → outcome | despair / hopelessness / anomie / fatalism vocabulary **AND** fertility | **604** |
| **Treatment → mechanism → outcome** | **all three together** | **12** |

Twelve. And the twelve do not survive inspection: the citation-ranked head is *Sleep essentialism*
(*Brain*), an *African Arts* essay on village imagery in Uganda, a *Pennsylvania History* article on
union songs, an *Oncology Times* piece on breaking bad news, and two *Oregon Historical Quarterly*
records. The single on-topic item is a **book review of Case and Deaton** in *Population and
Development Review*. There is no study in this intersection.

The same test run against the C.5.a sibling gives the same answer: economic uncertainty **AND**
fertility returns **3,120**, and adding the despair vocabulary cuts it to **20**, whose head is
*Steinbeck Review*, a paper on Bedouin employment, and an Austrian music lexicon. Against D.3.a:
depression/anxiety **AND** fertility returns **9,564**, and the despair-vocabulary intersection is
**164** — the largest of the three, and the one probe where the overlap is real rather than
lexical noise, because clinical hopelessness is a depression construct.

**The consequence, pre-committed rather than discovered.** The literature that estimates D.3.c's
treatment–outcome relationship does not measure, name or test D.3.c's mechanism, and the literature
that measures the mechanism does not estimate the relationship. A reviewer who reads the
place-based-decline papers as evidence *for* the despair channel is supplying the mechanism himself.
That is precisely the error B.7's chapter was built to avoid. Two consequences follow, and both are
enforced by the cell taxonomy below rather than left to the synthesis stage:

1. Mechanism-silent reduced-form studies enter as `SECONDARY_DECLINE_NO_MECHANISM`, are extracted, and
   are reported — but **cannot on their own support a D.3.c verdict**, because the identical estimate
   is C.5.a's evidence with equal claim to it. Whether they may support it *at all* is Call 2.
2. The GRADE rating is a rating of **the claim as stated in v5**, which is a mechanism claim. It is
   not a rating of "does local economic decline reduce births", which is a different and much
   better-evidenced proposition, and which C.5.a already owns.

### Where a measured mechanism does exist

The `PRIMARY_MEASURED_DESPAIR` cell is not empty, but it is small and it is **not American**. The
despair-vocabulary-and-fertility-intentions probe returns **26**, and its head is a single coherent
research family: Philipov, Spéder and Billari, *"Soon, later, or ever? The impact of anomie and social
capital on fertility intentions in Bulgaria and Hungary"* (*Population Studies*, 2006, 211 cites), and
its 2021 companion (20 cites). That is the post-communist transition — a collapse of forward
orientation, measured with an anomie scale, tested on fertility intentions. It is the closest thing in
the literature to a direct test of D.3.c, and it comes from a context v5's entry does not describe:
1990s Eastern Europe, not post-deindustrial working-class America.

The other place a validated despair instrument meets a fertility outcome is the **wrong direction**.
The Beck Hopelessness Scale probe returns **19**, and its entire citation-ranked head is infertility
patients — stigma and hopelessness in Turkish women with infertility, hopelessness among women in IVF
during COVID, art therapy for subfertile women. Every one of those is childlessness *causing* despair.
See Wall 5.

## The sign is not given by the theory

v5's entry states the claim one-directionally: despair → fertility deferred → fewer births. The
reconnaissance shows this is a choice, not an implication, and that the opposite prediction has the
older and larger literature.

A collapse of perceived future opportunity is the standard sociological explanation for **early,
nonmarital childbearing** among the disadvantaged — the "nothing to lose" account, in which
childbearing is not a costly long-term investment to be deferred but an available and immediate source
of meaning, identity and adult status when the alternative life course has been foreclosed. The probes
find this body intact:

- Kearney and Levine, *"Income Inequality and Early Nonmarital Childbearing"* (*Journal of Human
  Resources*, 2014) resolves at 98 cites; the surrounding cluster returns **104**.
- Edin and Kefalas, *Promises I Can Keep: Why Poor Women Put Motherhood before Marriage*, resolves at
  1,238 cites.
- "Socioeconomic Disadvantage as a Social Determinant of Teen Childbearing in the U.S." (239),
  "Teen births, income inequality, and social capital" (*Health & Place*, 118), and — squarely on
  D.3.c's own geography — "Opportunity, Community, and Reckless Lives: **Social Distress Among
  Adolescents in West Virginia**" (1997).
- The despair-vocabulary-and-teen-childbearing probe returns **912**; the narrower no-future-orientation
  probe returns **30**; "children as a source of meaning under constrained futures" returns **486**.

So the *same* antecedent — a foreclosed future in a declining place — is claimed by one literature to
**lower** fertility and by another to **raise early** fertility. These are reconcilable: the
mechanisms differ in whether children are modelled as an investment good (defer) or a meaning good
(accelerate), and the outcomes differ in margin (completed quantum vs timing of first birth). But the
reconciliation is a research finding this chapter must produce, not an assumption it may make.

**Pre-committed consequence.** Every extracted estimate carries a `FERTILITY_MARGIN` tag —
`QUANTUM_COMPLETED`, `PERIOD_RATE`, `TIMING_FIRST_BIRTH`, `INTENTION`, `NONMARITAL_SHARE` — and margins
are **never pooled across the quantum/timing divide**. The opposite-sign studies are in the **primary
synthesis**, not excluded to a discussion section. A chapter that searched for despair-lowers-fertility
and reported only what it found would be answering a question it had rigged. This mirrors C.2.c's
tenure-conditional sign, where the aggregate elasticity was found not to be a transportable parameter;
here the aggregate sign is not even a well-posed quantity until the margin is fixed.

## Phenomenon scope

**SDT only. No PM cell, no FDT cell.** The claim is about post-industrial community collapse and has
no pre-modern or first-transition analogue that v5 asserts.

**A sub-period restriction is required, and this chapter inherits B.7's problem rather than B.6's.**
B.6 needed no restriction because its exposure was older than the phenomenon. Here the exposure is
*younger*: the deaths-of-despair phenomenon Case and Deaton document begins its rise around 1999, and
the sharp American fertility case is the unexplained post-2007 decline. The SDT, as this review defines
it, opens around 1965. Most of the SDT therefore precedes the proposed cause entirely.

**This is not a scope quibble; it is a ceiling on the demographic-significance verdict**, and it is the
same arithmetic that in B.7 established that 67.6% of the SDT decline predated the exposure. The
computation is specified here and executed at stage 10, not asserted now:

- Series required: US TFR 1965–present (HFD, with WPP as the cross-check), and a despair-exposure
  series — county-level deaths-of-despair mortality per Case and Deaton's construction, or a
  survey-based hopelessness/subjective-future series if one with adequate time depth exists.
- Quantity: the share of the total SDT-period fertility decline that occurs **before** the despair
  series begins rising, computed exactly as B.7's was, and reported as an upper bound on what D.3.c
  can explain **before** any effect size is applied.
- The repository holds no macro panels locally (`data/raw/` is empty; `datastore/` holds only
  `studies.json`), so this stage requires a retrieval step of its own. It is flagged here so it is
  budgeted, not discovered at stage 10.

A second ceiling is **population share**. The despair phenomenon is documented in a specific and
minority segment — non-college, working-class, disproportionately rural and small-metro communities.
Even a large effect within that segment is bounded in its contribution to national TFR by that
segment's share of births. The significance computation runs on the segment share, never on the
national population.

**Geographic scope.** The claim as written is American. The reconnaissance finds the only
measured-mechanism evidence in post-communist Eastern Europe. Whether that evidence is admissible as
evidence *for* v5's claim is Call 5 — it is a transportability question, not a screening question, and
it is put to the PI rather than settled by the screener.

## The ten boundary walls

D.3.c is a *root* psychological cause whose empirical signature is nearly indistinguishable from four
well-populated neighbours. Routing is the central screening task.

**Wall 1 — D.3.c vs C.5.a (Economic Uncertainty, `economic-uncertainty-and-unemployment`). The
load-bearing wall, and it is UNENFORCEABLE at title and abstract.**
- **C.5.a asks:** does calculable personal or local income/employment risk induce rational
  option-value postponement, with an expected return to normalcy?
- **D.3.c asks:** does *chronic, expected-permanent* decline extinguish forward orientation, so that
  postponement is indefinite rather than optimally timed?
- **Discriminator:** (i) is the shock modelled as transitory or permanent, and (ii) is a despair-type
  construct measured, or is the mechanism asserted?
- **Why it cannot be enforced at title/abstract:** both discriminators live in the design and results,
  not in the summary. A title reading "Local labour-market shocks and fertility in US counties" is
  compatible with either, and the abstract almost never says which. **Declared unenforceable up front,
  exactly as D.3.b's Wall 1 had to be for measure content.** The screen therefore does *not* attempt
  the C.5.a/D.3.c split; it routes the whole reduced-form body into
  `SECONDARY_DECLINE_NO_MECHANISM` and defers the split to full text. Sampling and auditing a wall the
  screen cannot see was the D.3.b error, and it is not repeated.

**Wall 2 — D.3.c vs D.3.a (Mental Health and Anxiety Epidemic, `mental-health-anxiety-epidemic`).**
- **D.3.a asks:** does rising prevalence of clinical or subclinical disorder impair pair-bonding,
  libido and reproductive intention? Individual, clinical, content-agnostic.
- **D.3.c asks:** does *community-level* collapse of forward orientation, caused by economic decline,
  defer family formation? Ecological, sociological, economically caused.
- **Discriminator:** level of analysis **and** etiology. A study of diagnosed depression in individuals
  → fertility is **D.3.a** even if it uses the word hopelessness. A study of place-level despair
  indicators → place-level birth rates is **D.3.c**. Note the overlap probe returns **164**, the
  largest of the three sibling overlaps, and clinical hopelessness scales are depression instruments;
  expect genuine boundary cases and route them by level first, etiology second.

**Wall 3 — D.3.c vs the resource hypotheses (C.1.a income, C.3.e credit constraints, C.3.g student
debt).** Resources versus motivation. Those hypotheses say people cannot afford children; D.3.c says
people have stopped forming the intention to acquire the resources or to plan at all. **Discriminator:**
is the estimand a budget-constraint quantity (income, price, credit access, debt) or a subjective
orientation quantity? A decline study whose entire mechanism is lost earnings is a resource study.

**Wall 4 — the outcome wall: mortality is not fertility.** The deaths-of-despair literature is
**831** records, of which **491** carry explicitly mortality outcomes, inside a despair-and-mortality
cloud of **10,712**. None of it estimates a fertility quantity. This is the largest decoy cloud the
chapter faces. It routes to `DESPAIR_MORTALITY` — **routed out, but not blacklisted**: per the
decoy-cloud finding from prior runs, these are boundary cases with high on-topic rates for forward
citation seeding, and refusing to seed from them would discard the best available channel into a
literature this thin. The contested-framework subset (**113** — Ruhm-style challenges to the despair
interpretation of the mortality data) is retained as `THEORY_DESPAIR`, because a chapter rating a
despair mechanism must engage the evidence that the mechanism is misidentified in the case where it
was first claimed.

**Wall 5 — the direction wall: childlessness causes despair.** The reverse-causation body returns
**3,756**, and — as noted above — it *owns* the validated-instrument literature: every Beck
Hopelessness Scale study the probe surfaced is an infertility-distress study. **Discriminator:** which
variable is on the left. Infertility or childlessness → distress is `REVERSE`. This wall is enforceable
at abstract in most cases, because infertility-distress abstracts name a patient population.

**Wall 6 — the sign and margin wall.** Set out above. Not a routing-out wall: opposite-sign studies are
`EARLY_FERT_OPPOSITE_SIGN` and belong to the primary synthesis. The wall is against *pooling*, not
against inclusion.

**Wall 7 — the level-of-analysis wall (ecological inference).** Most candidate evidence is
place-level: county despair indicators against county birth rates. A place-level association is
consistent with individual-level despair having no effect, if composition changes. Every estimate
carries a `LEVEL` tag of `INDIVIDUAL`, `PLACE_ECOLOGICAL` or `MULTILEVEL`, and place-level estimates
are never presented as individual-level effects. The place-level despair-and-fertility probe returns
**216**, so this is not a hypothetical.

**Wall 8 — composition versus behaviour.** Declining places lose people, and they lose them
selectively: the young and the employable leave. A falling birth rate in a distressed county may be
migration, not behaviour. The selective-out-migration probe returns **569**. Studies that do not
address compositional change are extracted with a `COMPOSITION_UNADDRESSED` flag, which feeds risk of
bias rather than exclusion.

**Wall 9 — D.3.c vs D.3.b (Climate Anxiety, `climate-anxiety-eco-doomerism`).** Both are "the future
looks bad" hypotheses. **Discriminator:** the content and locus of the feared future — planetary
habitability and emissions ethics (D.3.b) versus the respondent's own community's economic and social
prospects (D.3.c) — and the demographic skew, D.3.b running young, higher-education and left-leaning,
D.3.c running non-college and working-class. D.3.b's scope froze this wall from its side; this
statement is its mirror and must stay consistent with it.

**Wall 10 — the marriage-channel wall.** Union formation is D.3.c's most-studied proximate channel —
decline and marriageability returns **1,724**, the marriageable-men literature **405**, the
retreat-from-marriage literature **340**, and Autor, Dorn and Hanson's *"When Work Disappears:
Manufacturing Decline and the Falling Marriage Market Value of Young Men"* resolves at 480 cites. But a
study whose only outcome is marriage or cohabitation estimates no fertility quantity and belongs to the
marriage-market workstream (TICK-058). **Discriminator:** is a fertility or childbearing outcome
reported? If not, it is `MARRIAGE_CHANNEL` — mechanism and context, never a D.3.c effect estimate.

## What the title/abstract screen can and cannot enforce

Stated up front, per the constraint carried from B.6.

| Wall | Enforceable at title/abstract? | Handling |
|---|---|---|
| 1 — vs C.5.a (transitory vs chronic; mechanism measured?) | **No** | Not attempted. Whole body → `SECONDARY_DECLINE_NO_MECHANISM`, split at full text |
| 2 — vs D.3.a (level and etiology) | Partly | Individual-clinical language usually visible; boundary cases to full text |
| 3 — vs resource hypotheses | Partly | Budget-constraint estimands usually named in the abstract |
| 4 — mortality vs fertility outcome | **Yes** | Outcome is nearly always named |
| 5 — reverse causation | **Yes** | Infertility-patient populations are named |
| 6 — sign and margin | **Yes** for margin | `FERTILITY_MARGIN` assignable from the outcome named |
| 7 — level of analysis | **Yes** | Unit of analysis is nearly always named |
| 8 — composition | **No** | Full-text only; becomes a risk-of-bias flag, not a screen decision |
| 9 — vs D.3.b (feared object) | **Yes** | Climate content is lexically distinctive |
| 10 — marriage-only outcome | **Yes** | Outcome is named |

Two of ten walls are unenforceable at screen and one is partly so. The screen is therefore designed to
be **over-inclusive by construction** on Walls 1 and 8, with the cost paid at full text. That is a
deliberate allocation, and it means the screen's precision figure will look worse than D.3.b's without
indicating a worse screen.

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_MEASURED_DESPAIR` | A measured despair / hopelessness / anomie / foreshortened-future construct | Fertility, intentions, or completed quantum | **Primary** |
| `PRIMARY_DECLINE_WITH_MECHANISM` | Chronic place-level economic decline, with a despair-type mediator measured or tested | Fertility | **Primary** |
| `SECONDARY_DECLINE_NO_MECHANISM` | Chronic place-level decline, mechanism asserted or absent | Fertility | Bridge — extracted, reported, cannot alone carry the verdict (Call 2) |
| `EARLY_FERT_OPPOSITE_SIGN` | Foreclosed future / despair / limited opportunity | **Early**, teen or nonmarital childbearing — sign-opposite | **Primary**, never pooled across the margin divide |
| `TRANSITORY_SHOCK` | Recession, layoff or unemployment spell modelled as transitory | Fertility | Route to C.5.a; retained as the contrast case for chronicity |
| `MARRIAGE_CHANNEL` | Decline or despair | Marriage / union formation only, no fertility outcome | Mechanism and context (Wall 10) |
| `DESPAIR_MORTALITY` | Despair or decline | Mortality, suicide, overdose | Route out; **seedable** for forward citation |
| `THEORY_DESPAIR` | Theoretical, normative or commentary treatment of despair and reproduction, incl. challenges to the despair interpretation | No empirical fertility estimate | Theory stream |
| `EXPOSURE_SERIES` | Despair indicators, subjective-wellbeing trends, geography of distress | No fertility outcome | Feeds stage 10, not the effect synthesis |
| `OFF_CLINICAL_D3a` | Individual clinical depression or anxiety | Fertility | Route to D.3.a |
| `OFF_RESOURCE` | Income, price, credit, debt as the estimand | Fertility | Route to C.1.a / C.3.e / C.3.g |
| `OFF_CLIMATE_D3b` | Ecological or planetary feared object | Fertility | Route to D.3.b |
| `REVERSE` | Childlessness or infertility | Despair, distress, wellbeing | `REVERSE` (Wall 5) |
| `COMPOSITION` | Selective migration or population loss | Place-level fertility composition | Context; feeds Wall 8 |
| `OFF_OTHER` | Non-D.3.c determinant with no sibling home | Fertility | Route out; no sibling queue |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

Every extracted estimate additionally carries `FERTILITY_MARGIN` (Wall 6) and `LEVEL` (Wall 7). Neither
is a routing cell; both are mandatory, and pooling rules key off them.

## Eligibility rules

- **Included designs:** any design reporting a quantitative association between a despair-type
  construct or a chronic-decline treatment and a fertility outcome. Given how thin the primary cells
  are, no design floor is imposed at screening; design quality enters through risk of bias, not
  eligibility. Qualitative work (Edin and Kefalas, Cherlin) is **not** an effect source but **is**
  admitted to the theory stream, because the mechanism claim is theirs.
- **Excluded:** mortality-only outcomes; marriage-only outcomes; infertility-distress studies
  (`REVERSE`); studies of despair with no reproductive outcome of any kind.
- **Time:** no publication-date floor. The opposite-sign literature is substantially older than the
  deaths-of-despair framing and would be lost to a post-2015 window.
- **Geography:** no restriction at screening. The US/non-US question is a synthesis question (Call 5),
  and restricting at screening would foreclose it.
- **Language:** English-language full text required for extraction; non-English records are logged, not
  silently dropped.

## Cold-start channels and leakage wall

The corpus is small enough that channel diversity matters more than query precision.

1. **Prior reviews.** Economic-conditions-and-fertility reviews return **652**; despair-or-distress-
   and-fertility reviews **378**. Both are read for reference-mining, and neither is treated as an
   effect source.
2. **The anomie family.** Forward and backward citations from Philipov, Spéder and Billari (2006) —
   the densest known concentration of the primary cell.
3. **The decline canon.** Autor–Dorn–Hanson and the "When Work Disappears" line, forward-cited for
   fertility outcomes.
4. **The opposite-sign canon.** Kearney–Levine and Edin–Kefalas, forward-cited.
5. **The mortality cloud, seeded deliberately.** Case and Deaton forward citations, filtered to
   fertility outcomes. The uniform seed rule applies: decoy-cloud membership does not disqualify a seed.
6. **The named perspective piece.** Platt and Sterling (2024), forward and backward.

**Leakage wall.** Records already screened under D.3.b, D.3.a or C.5.a are checked against those
corpora before entering this one, and a record's prior routing decision is carried forward as an input
rather than re-derived, so the three D.3 chapters cannot silently disagree about the same paper.

**Corpus-hygiene hazard, observed.** The 2023–2026 slice of the despair-and-birth-rates probe is
contaminated by near-duplicate, apparently machine-generated preprints (e.g. two identical records of
"The Substrate Collapse: Hemispheric Decoherence, Mirror Neuron Atrophy…", 0 cites). The
duplicate-record gate applies with its corrected rule — same title and year is not sufficient, author
agreement is required — and preprint version stacks are collapsed to a single version of record.

## Pre-query anchor audit

Resolved live, 2026-08-18. **v5's seminal list for D.3.c is three items and all three need correction
or qualification.**

| v5 seminal | Resolves to | Verdict |
|---|---|---|
| Case and Deaton (2020), *Deaths of Despair* | `book`, 2020, 1,088 cites | **Clean.** Companion articles also resolve: 2015 PNAS (2,782), 2017 (1,457) |
| **Platt and Sterling EurekAlert (2024)** | **Platt, M.L. and Sterling, P. (2024), "Declining human fertility and the epidemic of despair", *Nature Mental Health*, doi 10.1038/s44220-024-00241-1, 5 cites** | **Citation defect in v5, not a ghost.** v5 cites a press-release aggregator; the underlying paper exists and is cited above. It did not resolve under title search — it was recovered only through an author-filtered probe. Note it appears to be a perspective/comment by two neuroscientists, not an empirical fertility study; class to be confirmed at retrieval, and it is `THEORY_DESPAIR` unless it proves otherwise |
| Cherlin (2014), *Labor's Love Lost* | `book-review`, 226 cites | **Book-canon resolver failure.** The monograph resolves to a review of itself |

Edin and Kefalas, *Promises I Can Keep*, has the same failure — `book-review`, 1,238 cites. **The
author gate and the fallback flag are both required here**, per the standing finding on book canons;
two of this chapter's four named monographs resolve to their own reviews, the highest rate of any
chapter so far. A monograph-heavy anchor set is expected for a hypothesis whose canon is sociological
rather than econometric, so this is a design parameter of D.3.c, not an accident.

Also recorded: the resolver's type-vocabulary mismatch applies (Crossref `journal-article` vs OpenAlex
`article`), and the A4 path is the one that recovers books where A3 refuses.

**Anchors that do not exist.** Under both probe passes, and under targeted retries, there is **no
match** for: "hopelessness and fertility intentions"; "despair and fertility decline United States";
"economic despair and the decline in US births"; "county-level deaths of despair and birth rates";
"subjective future expectations and fertility behavior"; "teen childbearing and economic despair". The
only records under "deaths of despair and family formation" are four 2026 preprints from a single
author on Korean trade integration, uncited, including a pre-analysis plan. **The canonical American
despair-to-fertility study does not exist**, and the chapter should not be written as though a search
failure is why it has not been found.

## Scope calls for the PI

**Call 1 (load-bearing). Does this chapter rate a signed claim?** v5 states despair lowers fertility.
The reconnaissance finds a larger and older literature in which foreclosed futures *raise* early and
nonmarital childbearing. Options: (a) rate v5's claim as written, and report the opposite-sign
evidence as evidence against it; (b) restate D.3.c as a *margin-conditional* claim — despair lowers
completed quantum while accelerating first-birth timing — and rate that; (c) rate two sub-claims
separately. **Recommendation: (b), falling back to (a).** (b) is what the evidence is actually shaped
like, and it is the same move C.2.c made when the housing elasticity turned out to be
tenure-conditional. This does not block the search; it blocks synthesis.

**Call 2 (load-bearing). Does mechanism-silent reduced-form evidence count as evidence for D.3.c?**
The treatment–mechanism–outcome intersection is empty (n=12, none on topic). If mechanism-silent
decline studies count, the evidence base is on the order of a thousand records and D.3.c is largely
indistinguishable from C.5.a. If they do not, the primary base is the anomie family plus whatever
retrieval adds — a handful of studies. **Recommendation: they are extracted and reported but rated as
indirect, and the GRADE certainty is downgraded for indirectness rather than the studies being
excluded.** This preserves the C.5.a/D.3.c distinction the hypothesis list draws.

**Call 3. Sub-period and the demographic-significance ceiling.** Confirm that D.3.c is evaluated
against the post-1999 (or post-2007) sub-period rather than the whole SDT, and that the share of the
SDT decline predating the despair rise is reported as an explicit upper bound, as in B.7.

**Call 4. Referral to TICK-001, not a decision for this chapter and not blocking.** v5's D.3.c seminal
list should cite Platt and Sterling's *Nature Mental Health* paper rather than the EurekAlert release.
Separately, C.5.a's cross-reference field still labels despair "D.3.b"; D.3.b's scope flagged this in
July and it is still unfixed.

**Call 5. Is the post-communist anomie evidence admissible for an American claim?** It is the only
measured-mechanism evidence that exists. Admitting it makes the chapter's primary evidence a
transportability argument; excluding it leaves the primary cell close to empty. **Recommendation:
admit, tagged `CONTEXT_POSTCOMMUNIST`, and let the transportability weakness be visible in the GRADE
indirectness domain rather than hidden by an exclusion.**

## Next step

A3/A4 anchor resolution over the anchor set above, with the author gate active for the four
monographs. Then the discriminative-term pass and the production query. **Nothing downstream of the
production query should start before Calls 1 and 2 are answered**, because they determine which cells
are primary and therefore what the screen is optimising for.
