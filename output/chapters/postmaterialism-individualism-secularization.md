# Chapter: Postmaterialism, Individualism, and Secularization

**Category:** Cultural
**Primary mechanism:** As material security becomes assured and religious authority recedes, people come to value autonomy and self-expression over obligation and continuity, and want fewer children.
**Target phenomena:** First demographic transition (secularization stratum only) and second demographic transition. No pre-modern cell.
**Cross-references:** exposure to an external modernity package (D.1.b, where the treatment is contact rather than the value held); prestige-biased transmission (D.1.c); gender-role attitudes (D.2.a); union deinstitutionalization (D.2.b); ancestral-culture persistence (A.19, which shares this chapter's best-identified design and is separated from it by proxy content); ecological dread (D.3.b, whose treatment is a fear rather than a value orientation).
**Draft status:** **PARTIAL — SCOPE, SEARCH, AND METHODS ONLY.** Sections 1–4 and 8–11 are drafted. **Sections 5 through 7 — included studies, synthesis, demographic significance, and the GRADE ratings — are deliberately empty**, and Section 4 explains exactly why: the systematic screen has not been run, so no claim about what this literature contains or lacks can yet be made. Two of this chapter's five rulings also await PI sign-off, and one of them fixes GRADE ceilings before any study is read.
**Last updated:** 2026-08-05

---

## 1. The claim

Fertility fell because what people want changed. In the strong form, rising material security shifts
priorities from survival toward self-expression (Inglehart), religious authority over family life
weakens (Lesthaeghe), and the resulting value orientation lowers desired family size — so fertility
falls without any change in prices, income, or the technology of contraception.

The claim's ambition is also its difficulty. Values are not assigned, they are measured; they move
with the same modernization that moves everything else in the frame; and they are usually recorded
after the fertility they are meant to explain. This chapter's job is to find the estimates that
escape those problems, and to say plainly how few of them there are.

## 2. The five pairs, and why this is not one hypothesis

**A hypothesis is a treatment × outcome pair.** Mediators do not define it and do not route a paper.
Applying that rule to D.1.a as the master list inherited it dissolves it into **five distinct
treatments against one outcome**:

| | Treatment | Status |
|---|---|---|
| **S1** | postmaterialist / self-expression / survival-values measures | large theory and measurement literature, very few fertility estimates |
| **S2** | individualism, autonomy, collectivism, kinship intensity | same |
| **S3** | religiosity, affiliation, attendance, salience, denomination | **the only stratum with a large individual-level literature and access to natural experiments** |
| **S4** | the childlessness norm | mostly degenerate — see Ruling 2 |
| **S5** | consumption orientation, material-values scales | very thin |

These are never pooled. The strata are unequal enough that even search budget was not split evenly
between them, and the recommendation on record is that the master list should probably **split D.1.a
into separate hypotheses**, beginning with S3.

Two consequences follow immediately, and both are stated here rather than buried in limitations.

**Ruling 2, the degenerate pair.** When the treatment measure and the outcome measure are the same
construct, there is no pair. Regressing a person's childlessness on their own approval of
childlessness estimates preference-outcome consistency, not a causal effect: it is one variable
measured twice. This removes most of S4 from the causal pool. It was pre-registered in the scope, and
independent confirmation arrived from an unexpected direction — a term-mining pass over the corpus
found that **every** childlessness term classifies as outcome vocabulary or as both, and none as a
pure treatment word, because there is no S4 treatment word that is not also the outcome word.

**Ruling 3, the design ladder.** Admissible designs are ranked with GRADE ceilings fixed in advance.
The consequential entry is that **country-level value-index-versus-TFR co-movement sits at Tier 4
with no causal weight** — on three joint defects: roughly fifty units against a dozen collinear
covariates with GDP among them, and countries that are not independent draws because values diffuse
across borders. That is the canonical SDT evidence base. Excluding it from the causal pool is the
single most consequential decision in this chapter and **it is not an RA call**; it is flagged for PI
sign-off as a freeze condition.

## 3. Search strategy

Four channels, in the order run. Everything is reproducible from `source/build/goldset/` scripts
`89_` through `112_`; the artifacts are in `literature/search-logs/`.

**Channel 1 — existing syntheses — is empty for four of the five pairs, and the emptiness is a
finding.** The scope predicted reviews would exist for secularization and not for the others. The
negative half held; the positive half did not. `religion AND fertility` restricted to reviews returns
**zero across all fields**, and the only syntheses that exist are two sub-Saharan-Africa regional
ones. **Religion and fertility has been studied for a century and never systematically synthesised
outside one region.** The pair expected to carry the chapter cannot be bootstrapped from external
authority.

**Channel 2 — design-vocabulary probes.** Because the S3 anchors surfaced by topic vocabulary were
uniformly Tier 3 or Tier 4, the natural experiments had to be sought by *design* words rather than
subject words. Twenty-four narrow probes returned **three credible Tier-1 candidates, all S3, all
published since 2018** (Section 10).

**Channel 3 — citation snowball**, seeded on works chosen for the specificity of their citation
neighbourhood rather than fame: Hofstede 1980 and Schwartz 1992 both resolve and are deliberately not
seeded, being canon for a *construct* rather than for this pair. Two rounds, closed by the PROTOCOL
§5.1 depth cap. The resulting Tier-B frame is built off Crossref and Semantic Scholar rather than
OpenAlex, so that it is orthogonal to Tier A in infrastructure as well as in method — which makes
Recall(B) a stronger test than it would otherwise be.

**Channel 4 — the clustered production query**, run against OpenAlex `title.search`, title-only,
one cursor-paginated stream per cluster, unioned client-side. Six clusters: the five pairs plus a
`GENERIC_VALUES` cluster of treatment-side vocabulary that retrieves on-pair work without naming a
pair. That sixth cluster carries **more sole credit than the secularization cluster** — 176 gold
papers no other cluster reaches — so a query built only from pair-specific vocabulary would have been
an S3 query and would have lost roughly a third of the frame.

**Yield: 17,646 distinct records**, reduced to **15,586** by a deterministic pre-filter that removes
the clinical/veterinary/agronomic collision and routes book reviews to a retrieval worklist. Recall
against the frozen gold set is **84.2%**, or **87.2%** after repairing gold rows whose stored title
was an entire citation string.

### 3.1 The query was wrong once, and the correction is part of the record

The first production pull returned 17,281 records and a plausible-looking recall of 81.8%. It was
missing **two of the chapter's three Tier-1 natural experiments**.

The cause was that the query carried wildcard stems (`secular*`, `religio*`, `procreat*`) and
OpenAlex rejects any request containing a star, so the pull stripped the star and sent the bare stem.
That is safe only when the stem is itself a word: `childless` and `childlessness` resolve to one
postings list, but **`procreat`, `nuptialit`, `childbear` and `postmaterialis` retrieve nothing at
all**. Twenty-four of forty-five wildcard terms were dead. Worse, and invisible to any count-based
audit, `secular` returns 34,326 records while failing to match *"Secularization"*, and `religio`
returns 2,041 while failing to match *"Religiously"*.

Two things are worth carrying out of this beyond the repair itself.

The first is that **the failure was one step from becoming a substantive claim about demography.**
The childlessness-norm cluster earns almost no unique credit, and the standing question was whether
it was "buying coverage of a literature that does not exist." Eight of that cluster's nine wildcard
terms were dead. The stratum retrieved nothing because its terms were broken, not because the field
is empty.

The second is that **a high term count does not mean a term contributes anything.** OpenAlex stems
`seculared`, `secularing` and `seculares` all back to `secular`, so each returns the same 34,326
records under a different spelling and each outranks the genuine `secularization` at 4,657. Selecting
query variants by retrieval count therefore filled every slot with noise and discarded the one derived
form the repair existed to recover.

### 3.2 What the search cannot reach

Of the gold records the completed search does not return, **19 appear not to be indexed by the
provider at all** — a ceiling no query can pass. They are book chapters, dissertations, regional and
non-English journals: the sixth independent appearance of a non-Anglo-European indexing gap on this
chapter, after an unregistered DOI at *African Journal of Reproductive Health*, two regional reviews
absent from Semantic Scholar, Dutch-language Lesthaeghe and van de Kaa 1986, the Crossref backfill
residue, and reviews of on-pair monographs surviving only as reviews. This runs in the same direction
as the chapter's geographic-skew limitation and is not independent of it.

A further **21 records are in the index and the query does not reach them** — addressable, worth
perhaps five recall points, and a candidate for a third query round.

Language coverage is a live constraint rather than a hypothetical one. The continental European core
of this literature is not all in English: Lesthaeghe's early work is partly Dutch and French, and a
German-language postmaterialism-to-fertility study from 1990 is among the few S1 estimates that exist.
An English-only query would systematically drop exactly the FDT-era material Ruling 4 was written to
admit.

## 4. PRISMA flow — INCOMPLETE, and why that blocks Sections 5–7

| Stage | N | Status |
|---|---|---|
| Records identified (channel 4, union across six clusters) | 17,646 | complete |
| Cross-cluster overlap collapsed by deduplication | 6,698 → included above | complete |
| Removed by deterministic pre-filter (clinical, veterinary, agronomic, book reviews) | 1,855 | complete |
| Routed to book-review retrieval worklist | 205 | complete, not yet chased |
| **Entering blinded title/abstract screen** | **15,586** | **staged, not run** |
| After title/abstract screen | — | **blocked** |
| Full text retrieved | — | blocked |
| Included in synthesis | — | blocked |

**Nothing downstream of the screen can be written yet, and the reason is not merely that numbers are
missing.** This chapter's most valuable outputs are claims about *absence* — that Tier 1 is three
studies, that whole design families are unused, that S1 can be reported but not rated. An absence
claim made against a citation frame and then contradicted by a systematic screen is not updated, it
is retracted. The frame is a snowball from nine framework statements and eighty-two on-pair papers,
which tilts it toward the well-cited Anglo-European SDT core — precisely the direction this chapter is
weakest. Writing Sections 5–7 from it now would bake that tilt into the synthesis and would leave §12
understating the limitation, because the quantity that measures it — what the systematic search adds
beyond the citation frame — would never have been observed.

### 4.1 What the full screen would add, estimated from 400 records

A uniform random sample of **400 of the 15,586** queued records was screened under the frozen rubric
(`113_d1a_yield_sample.py`). The sample is random by construction: the production records are shuffled
under a fixed seed before batching, so the first ten batches are a random 400 rather than the first
400 of anything.

| | sample | rate | 95% CI (Wilson) | projected to 15,586 |
|---|---|---|---|---|
| `RELEVANT` | 20/400 | **5.0%** | 3.3–7.6% | **≈780** (508–1,184) |
| assigned a primary, poolable cell | 26/400 | 6.5% | 4.5–9.3% | ≈1,010 |
| `UNCERTAIN` → a full-text read | 49/400 | 12.3% | 9.4–15.9% | ≈1,910 |
| `NOT_RELEVANT` | 331/400 | 82.8% | | |

**The count settles the question of whether to run the screen: it would add several hundred studies,
so no claim about the size of this literature can be made without it.** But the composition qualifies
which absence claims were at risk, and it is the more interesting result.

**Not one record in the sample was guessed above Tier 3.** Of the twenty `RELEVANT` records, sixteen
were judged Tier 3 and four Tier 4; **zero Tier 1 and zero Tier 2**. The screen would therefore add
volume without adding credibility. The chapter's claims about *identified* evidence — that Tier 1 is
three studies, that blue-law, Sunday-trading and clergy-scandal designs are unused, that state atheism
was never used to identify a fertility effect — are not the claims this sample threatens. The claim
that was at risk is the weaker and more ordinary one about how much has been *studied*.

The distribution also reproduces the shape predicted from the anchor set, which is the best available
evidence that the screen is calibrated rather than merely productive: **S3 supplies 19 of the 26
primary-cell records**, against 2 for S1, 1 for S2 and 1 for S5 — close to the 23/5/1/2 split of the
hand-built empirical anchors. And `GENERIC_VALUES` is the single largest source of kept records (42),
confirming live what the breadth analysis predicted: a query built only from pair-specific vocabulary
would have lost roughly a third of the frame.

One expectation was not met. The rubric anticipated that `AGGREGATE_COMOVEMENT` — country-level value
index against TFR, the canonical SDT evidence base — would be **common**. It appears once in 400. The
likely reason is that a title and abstract rarely reveal that the unit of analysis is the country, so
these are routing to `UNCERTAIN` rather than to their cell; if so the count will reappear at full
text. It is recorded here as an open discrepancy rather than a finding.

**The binding constraint is downstream of the screen, not the screen itself.** ~1,910 `UNCERTAIN`
records is ~1,910 full-text retrievals, and sibling chapters are already retrieval-bound. Screening is
about a day of unattended compute; the reads it generates are the real budget.

## 5. Included studies

**Blocked pending the screen.** See Section 4.

## 6. Quantitative synthesis

**Blocked pending the screen.** Two constraints on the eventual synthesis are already known and are
recorded now so they are not discovered late.

**Estimates are not independent draws.** Much of this literature runs on a handful of survey
instruments — WVS/EVS, ESS, GSS, DHS. Twenty papers on overlapping waves and countries are not twenty
independent estimates. `DATA_SOURCE` is a required extraction tag and a clustering variable in any
pooled analysis.

**Signs must be oriented before pooling.** S3 is almost always coded toward religiosity while S1 and
S2 are coded toward self-expression. Mixing flipped and unflipped estimates is a mechanical route to
a null. Every effect is oriented toward the secular/postmaterialist pole at extraction (Ruling 5).

## 7. Demographic significance

**Blocked pending the screen**, and additionally exposed to a defect in the deliverable format that is
larger than this chapter.

D.1.a is a root cause whose causal pathway runs through four or five separately credited chapters —
contraceptive diffusion, education, women's employment, union deinstitutionalization, child quality.
Three of them name D.1.a as their root cause in their own notes. **If each proximate chapter claims
its share of one fertility decline and D.1.a claims the reduced form, the shares sum past 100% and the
per-hypothesis verdict format breaks where a reader adds it up.** This is not an accounting nuisance
to be resolved inside this chapter; it is escalated as a defect in the review's output format.

## 8. Risk of bias and identification quality

Four domains bind, in roughly this order of severity.

**Reverse causation is the binding threat and it is measured, not assumed.** Parenthood plausibly
increases religiosity as much as religiosity increases parenthood. One study sizes the arrow directly:
using the British Household Panel Survey, *"Does forming a nuclear family increase religiosity?"*
(European Sociological Review 2022) asks how entering cohabitation, marriage, and first and second
births affect religious salience, attendance, and organizational activity. It carries no effect
estimate for this chapter's pair and it belongs in this section rather than in a context list,
because it is the best available measurement of the domain that most limits every S3 estimate.

**Selection on the measure's timing.** A value recorded after the outcome cannot support a causal
reading. `PRIMARY_VALUE_EX_ANTE` exists as a separate estimand cell precisely to isolate the studies
that recorded the value orientation on childless respondents *before* the fertility outcome.

**Measured versus narrated treatment (Wall 7).** A study identified off income, growth or
unemployment, with value change narrated in the discussion but never entered in the regression, has
income as its treatment. The test is what is in the regression, not what is in the framing.

**The moderator boundary.** A value measure interacted with a policy, price or shock passes both
routing questions and is still not this chapter's estimate: the quantity identified is the effect of
the other treatment. A difference-in-differences on a 1982 Baltic maternity-benefits expansion,
comparing women who did and did not grow up in religious households, estimates the effect of the
benefit. Religiosity was never moved. These are recorded as `VALUE_AS_MODERATOR` — genuinely
informative that values condition responsiveness, and not a causal estimate of value on fertility.

**Wall 5, the epidemiological design, is the one place where the best-identified evidence is
contested between chapters.** Second-generation designs hold prices and institutions fixed while
culture varies, which makes them the strongest tool available for a claim about content. They are
also claimed by A.19. The separation is on proxy content: an ancestral *fertility rate* tests
persistence and routes to A.19; an ancestral *value measure* tests the content claim and routes here;
both together are flagged. Fernández and Fogli (2009), the most-cited record in the whole union,
proxies culture with ancestral female labour-force participation **and** ancestral total fertility,
and is therefore bound never to be routed from its abstract.

## 9. External validity and transportability

Deferred to the synthesis, with one constraint already fixed. Ruling 4 admits FDT-era evidence: the
Princeton European Fertility Project's secularization work is measurement of the S3 construct applied
to the first transition, so this chapter's S3 stratum spans two target phenomena rather than one.
Whether an estimate from nineteenth-century Europe transports to the contemporary SDT is a question
for the synthesis, not a reason to exclude it at scope.

## 10. Open questions and recommended studies

**The empty design families are as informative as the full ones, and they are the most actionable
output this chapter has so far.** The Tier-1 probe searched by design vocabulary and returned:

- **Blue laws and Sunday trading restrictions: zero.** The Gruber–Hungerman design family has been
  applied to religiosity, and then to drinking, drug use and crime — never to fertility.
- **Clergy-scandal shocks: zero.**
- **State atheism campaigns: five hits, none with a fertility outcome.** The Soviet and Albanian
  campaigns are the largest deliberate secularization shocks in recorded history and appear never to
  have been used to identify a fertility effect.

Each is a specific, checkable gap with an existing design ready to be transported. These are stated
as provisional: they rest on targeted probes rather than on the completed screen, and the screen may
yet find one. That is exactly why the screen has to run before Sections 5–7 are written.

**Three Tier-1 candidates exist and all three are S3, all published since 2018:** political-party
variation in Turkey (*American Journal of Sociology* 2018), declining church membership in Finland
(*Social Science Research* 2026), and a religious-leader intervention in Georgia (*Journal of
Population Economics* 2025). If the eventual pool sustains that count, **the chapter's headline is
that a century-old literature contains three studies that identify anything**, and that all of them
concern religion.

**S1 is not empty of estimates, only of identified ones** — a refinement on the scope worth stating,
because "no evidence exists" and "no identified evidence exists" are different chapters. An explicit
empirical horse-race between the competing accounts exists (*Population and Development Review* 2022)
and is a priority read.

## 11. Reproducibility appendix

| Stage | Script | Artifact |
|---|---|---|
| Channel-1 probe | `89_d1a_channel1_probe.py` | `{slug}-channel1-probe.md` |
| Tier-1 design probe | `90_d1a_tier1_design_probe.py` | `{slug}-tier1-design-probe.md` |
| Cold-start anchors + existence gate | `91_d1a_cold_start_anchors.py` | `{slug}-cold-start-anchors.json` |
| Canon resolution | `92_`, `95_` | `{slug}-canon-reresolution.md` |
| Snowball rounds 1–2 | `93_`, `96_`, `97_` | `{slug}-snowball-log.md` |
| Gold assembly | `98_`, `99_` | `{slug}-tier-a.json`, `-tier-b-frame.json` |
| Term mining and breadth CV | `100_`, `101_` | `{slug}-cv-breadth.md` |
| Production query v1 | `102_` | `{slug}-production-query.json` |
| Live pull | `103_` | `{slug}-live-corpus-v2.json` |
| Pre-filter | `104_` | `{slug}-prefilter-log-v2.md` |
| Stem audit (why v1 failed) | `105_` | `{slug}-stem-audit.md` |
| Query repair v2 | `106_` | `{slug}-production-query-v2.json` |
| Miss decomposition | `107_` | `{slug}-miss-decomposition.md` |
| Gold repair | `108_` | `{slug}-gold-repair.md` |
| Screen batching / validation / runner | `109_`, `110_`, `111_` | `{slug}-screen-manifest.json` |
| Anchor relabelling | `112_` | `{slug}-anchor-relabel.md` |

Run order is binding at two points: `98_` before `99_`, and `106_` before `103_ --query v2`.

## 12. Limitations

1. **Geographic and language skew**, six independent confirmations, with a measured floor: 19 gold
   records are not in the searched index at all.
2. **The canonical SDT evidence base is excluded from the causal pool** by Ruling 3. A reader who
   disagrees with that ruling will disagree with every rating in this chapter, which is why it is
   stated in Section 2 rather than in a footnote.
3. **Most of S4 is degenerate** under Ruling 2 and is reported descriptively.
4. **Estimates cluster on a few survey instruments** and are not independent.
5. **The shares do not add up** across the proximate chapters this one runs through (Section 7).
6. **Two rulings are unsigned.** The scope is DRAFT.

## 13. References

Deferred until the included-studies table exists. Works named in this draft are anchors and
context — Lesthaeghe (1983); van de Kaa (1987); Lesthaeghe and Surkyn (1988); Inglehart and Baker
(2000); Norris and Inglehart (2004); Fernández and Fogli (2009); Zaidi and Morgan (2017) — and their
appearance here is not a claim that they are included studies.
