# Screen report — antidepressants-ssri-subfecundity (B.7)

**Screened: 420** records (the D1 budget slice plus the orthogonal-channel bypass) out of a 6,798-record deduplicated frame.

| tier | definition | n |
|---|---|---|
| 1 | RELEVANT, found through more than one channel or seed | 116 |
| 2 | RELEVANT, single channel | 79 |
| 3 | UNCERTAIN, retained for audit only | 6 |
| — | NOT_RELEVANT, excluded | 219 |

**Primary-cell records: 20** · **support stream (mechanism, parameter, baseline, measurement, theory, adjacent, reverse): 92** · **held for full-text adjudication: 5**

## The chain, counted

This is the chapter's central result and it is a count rather than an estimate. The hypothesis needs all three links; the literature has supplied them in wildly unequal measure.

| link | proposition | records |
|---|---|---|
| 1 | medication -> sexual function | 71 |
| 2 | sexual function -> coital frequency | 1 |
| 3 | coital frequency -> conception | 12 |

Link 3's records are borrowed from A.14 and are about the parameter rather than about antidepressants. Link 2 is the joint that has to hold for the hypothesis to work, and it is the one nobody has measured in this population.

## Cell distribution

| cell | n |
|---|---|
| `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | 71 |
| `OFF_OUTCOME` | 68 |
| `OFF_OTHER` | 45 |
| `OFF_PREGNANCY_SAFETY` | 40 |
| `OFF_CLINICAL_MANAGEMENT` | 32 |
| `OFF_ANIMAL` | 28 |
| `PARAMETER_PREVALENCE` | 24 |
| `ENDOCRINE_MECHANISM` | 23 |
| `MEASUREMENT_ASCERTAINMENT` | 19 |
| `INDICATION_BASELINE_D3A` | 12 |
| `LINK3_COITAL_TO_CONCEPTION` | 12 |
| `PRIMARY_MALE_FECUNDITY` | 10 |
| `PRIMARY_MEDICATION_TO_FERTILITY` | 10 |
| `REVERSE` | 6 |
| `PARAMETER_DETERMINANT_TO_LOSS` | 4 |
| `INSUFFICIENT_INFO` | 4 |
| `OFF_ART_A17` | 4 |
| `THEORY_SEROTONERGIC` | 3 |
| `OFF_ENVIRONMENTAL_B2B6` | 2 |
| `ROUTING_DEFERRED_TO_FULLTEXT` | 1 |
| `PARAMETER_HAZARD_CLINICAL` | 1 |
| `LINK2_FUNCTION_TO_COITAL_FREQUENCY` | 1 |

## The predictions the scope document made, and what came back

The scope document made four falsifiable predictions before the search ran. All four held, which is a statement that the chapter's evidence problem was correctly diagnosed in advance rather than a vindication of the search.

1. **Precision binds, not recall.** The pregnancy-safety and clinical-management cells together are the largest part of the screened corpus, on a worklist already ranked to demote them.
2. **The measured evidence is male and the hypothesis text is female.** The primary cell divides into a male stratum with semen and fertility outcomes and a female stratum that is almost entirely fecundability cohorts sharing one research group.
3. **Link 1 is abundant, link 2 is empty.** See the chain table above. The single link-2 record located in 420 screened is a qualitative interview study of nine women in a university repository.
4. **The parameter stream is stronger than the causal stream.** Exposure prevalence is measured by national dispensing registries with age and sex detail; the causal claim rests on a handful of cohorts that cannot separate the drug from the indication.

## Validation 1 — anchor recovery on records whose answer was known

Four A3 anchors reappear inside Tier B as cited works, and their correct routing is known independently, so they are a live test of the screen. Two of the four are records A3 could not key to a DOI at all: both index copies of Montejo et al. 2001, whose only DOI-bearing same-title record was a Faculty Opinions shadow, and the NCHS data brief, which carries no DOI because agency series do not.

| record | expected cell | screened cell | agree |
|---|---|---|---|
| `W2229937731` | `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | yes |
| `W1952442899` | `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | yes |
| `W1607894683` | `PARAMETER_PREVALENCE` | `PARAMETER_PREVALENCE` | yes |
| `W2062240933` | `OFF_PREGNANCY_SAFETY` | `OFF_PREGNANCY_SAFETY` | yes |

The citation frame recovered what the anchor resolver could not. A DOI-less record is not an absent one: Montejo et al. 2001 and the NCHS brief are both present in Tier B because the works citing them are, and the OpenAlex ids recovered here should be written back into the anchor file rather than left as an open gap. This is the same lesson the reconnaissance pass taught on titles — an identifier that does not resolve says something about the index, not about the literature.

## Validation 2 — decoy containment

47 screened records depend only on a routing-decoy seed. Of those, **39 (83%) were routed away** as NOT_RELEVANT. The decoys were forward-cited like every other seed, per the D.2.d correction, so their neighbourhoods entered the frame by design; the walls then had to do the work of excluding them, and this figure is how much work they did.

## What the screen deliberately did not decide

No record carries an estimand level and none carries an indication design. `HAZARD_DECREMENT` versus `TEMPO_ADJUSTED_QUANTUM` decides poolability and `INDICATION_DESIGN` decides whether a study speaks to B.7 at all; both are methods facts that abstracts state inconsistently, and both are set at full-text extraction and nowhere earlier. Records whose routing turned on Wall 1 without the design being named took `MIXED_INDICATION_UNRESOLVED`, and two records whose SPECIES could not be established from the visible text took `INSUFFICIENT_INFO` rather than being guessed at — Wall 7 is the one wall where a guess is cheap to make and expensive to be wrong about.

## Next

`extraction/antidepressants-ssri-subfecundity-ra-gate.csv` carries the 25 records a human must adjudicate: every primary-cell record plus everything held at a MIXED or DEFERRED cell. The RA verdict is the inclusion decision; the three deterministic signals only feed it.
