# A3 cold-start anchors — antidepressants-ssri-subfecundity (B.7)

Sourced in a live OpenAlex pass (2026-08-12) and resolved through four gates: 24 candidate anchors, of which 2 are empirical primary-cell anchors (the causal recall denominator) and the rest are link-support, mechanism, parameter, measurement, theory, or routing-decoy anchors that earn no empirical recall credit. No DOI is hand-asserted; each is the top-ranked version-of-record candidate from a unified Crossref + OpenAlex field, then re-affirmed at doi.org.

**Verified (live DOI): 22**  ·  **Year-drift keep (real, RA-confirm): 0**  ·  **Flagged for RA: 0**  ·  **Expected index miss (no DOI by nature): 2**

**Shadow records refused: 5** across 4 anchors — the new gate firing.  **Integrity flags raised: 1.**

**Records refused as a review of the work, or on authorship: 0.** Every refusal keeps its record in the JSON so the RA can audit what was refused rather than trusting that nothing was lost.

## Coverage by estimand cell (verified / total)

- `ADJACENT_PSYCHOTROPIC`: 1/1
- `ENDOCRINE_MECHANISM`: 4/4
- `INDICATION_BASELINE_D3A`: 2/2
- `LINK1_MEDICATION_TO_SEXUAL_FUNCTION`: 3/4
- `LINK3_COITAL_TO_CONCEPTION`: 2/2
- `MEASUREMENT_ASCERTAINMENT`: 1/1
- `OFF_ANIMAL`: 1/1
- `OFF_ART_A17`: 1/1
- `OFF_CLINICAL_MANAGEMENT`: 1/1
- `OFF_PREGNANCY_SAFETY`: 1/1
- `PARAMETER_DETERMINANT_TO_LOSS`: 1/1
- `PARAMETER_PREVALENCE`: 1/2
- `PRIMARY_MALE_FECUNDITY`: 1/1
- `PRIMARY_MEDICATION_TO_FERTILITY`: 1/1
- `THEORY_SEROTONERGIC`: 1/1

## Coverage by query-cluster family (verified / total)

- ascertainment: 1/1
- baseline: 2/2
- decoy-animal: 1/1
- decoy-art: 1/1
- decoy-clinical: 1/1
- decoy-pregnancy-safety: 1/1
- decoy-psychotropic: 1/1
- link1: 3/4
- link3: 2/2
- loss-parameter: 1/1
- mechanism-semen: 3/3
- prevalence: 1/2
- primary-female: 1/1
- primary-male: 2/2
- theory: 1/1

## Integrity flags — read before using these effect sizes

Raised by the shadow gate, which noticed an Expression of Concern, retraction or correction record sitting on an anchor. These are facts about the work, carried forward to extraction and risk of bias rather than logged and forgotten.

- **Sperm DNA Damage and Semen Quality Impairment After Treatment With Sel** (2008) — integrity: *Expression of Concern: Sperm DNA Damage and Semen Quality Impairment After Treat* (2023) `10.1097/ju.0000000000003115`

## Per-candidate disposition

- **The effect of antidepressants on fertility** (2016, primary-female) -> VERIFIED  doi=10.1016/j.ajog.2016.01.170  J=1.0  [journal-article]  auth=True  (American Journal of Obstetrics and)
- **Use of selective serotonin reuptake inhibitors reduces fertility in ** (2016, primary-male) -> VERIFIED  doi=10.1111/andr.12184  J=1.0  [journal-article]  auth=True  (Andrology)
- **Effect of antidepressant medications on semen parameters and male fe** (2019, primary-male) -> VERIFIED  doi=10.1111/iju.14111  J=1.0  [journal-article]  auth=True  (International Journal of Urology)
- **Prevalence of Sexual Dysfunction Among Newer Antidepressants** (2002, link1) -> VERIFIED  doi=10.4088/jcp.v63n0414  J=1.0  [journal-article]  auth=True  (The Journal of Clinical Psychiatry)
- **Incidence of sexual dysfunction associated with antidepressant agent** (2001, link1) -> BOOK-NO-DOI (expected)  best-J=1.0  refused=shadow_record:commentary,title_or_no_doi
- **Treatment-Emergent Sexual Dysfunction Related to Antidepressants** (2009, link1) -> VERIFIED  doi=10.1097/jcp.0b013e3181a5233f  J=1.0  [journal-article]  auth=True  (Journal of Clinical Psychopharmaco)
- **Antidepressant-Induced Sexual Dysfunction During Treatment With Mocl** (2000, link1) -> VERIFIED  doi=10.4088/jcp.v61n0406  J=1.0  [journal-article]  auth=True  (The Journal of Clinical Psychiatry)
- **Sexual dysfunction before antidepressant therapy in major depression** (1999, baseline) -> VERIFIED  doi=10.1016/s0165-0327(99)00050-6  J=1.0  [journal-article]  auth=True  (Journal of Affective Disorders)
- **Fecundity of Patients With Schizophrenia, Autism, Bipolar Disorder, ** (2013, baseline) -> VERIFIED  doi=10.1001/jamapsychiatry.2013.268  J=1.0  [journal-article]  auth=True  (JAMA Psychiatry)
- **Timing of Sexual Intercourse in Relation to Ovulation - Effects on t** (1995, link3) -> VERIFIED  doi=10.1056/nejm199512073332301  J=1.0  [journal-article]  auth=True  (New England Journal of Medicine)
- **The risk of conception on different days of the menstrual cycle** (1969, link3) -> VERIFIED  doi=10.1080/00324728.1969.10405297  J=1.0  [journal-article]  auth=True  (Population Studies)
- **Adverse effect of paroxetine on sperm** (2009, mechanism-semen) -> VERIFIED  doi=10.1016/j.fertnstert.2009.04.039  J=1.0  [article]  auth=True  (Fertility and Sterility)
- **Sperm DNA Damage and Semen Quality Impairment After Treatment With S** (2008, mechanism-semen) -> VERIFIED  doi=10.1016/j.juro.2008.07.034  J=1.0  [journal-article]  auth=True  (Journal of Urology)
- **Antidepressant-Associated Changes in Semen Parameters** (2007, mechanism-semen) -> VERIFIED  doi=10.1016/j.urology.2006.10.034  J=1.0  [journal-article]  auth=True  (Urology)
- **Dopamine and serotonin: influences on male sexual behavior** (2004, theory) -> VERIFIED  doi=10.1016/j.physbeh.2004.08.018  J=1.0  [journal-article]  auth=True  (Physiology &amp; Behavior)
- **National Patterns in Antidepressant Medication Treatment** (2009, prevalence) -> VERIFIED  doi=10.1001/archgenpsychiatry.2009.81  J=1.0  [journal-article]  auth=True  (Archives of General Psychiatry)
- **Antidepressant Use among Persons Aged 12 and Over: United States, 20** (2017, prevalence) -> BOOK-NO-DOI (expected)  best-J=0.706  refused=title_or_no_doi
- **Use of antidepressants during pregnancy and the risk of spontaneous ** (2010, loss-parameter) -> VERIFIED  doi=10.1503/cmaj.091208  J=1.0  [journal-article]  auth=True  (Canadian Medical Association Journ)
- **The ELIXIR study: evaluation of sexual dysfunction in 4557 depressed** (2003, ascertainment) -> VERIFIED  doi=10.1185/030079902125001461  J=1.0  [journal-article]  auth=True  (Current Medical Research and Opini)
- **Use of Selective Serotonin-Reuptake Inhibitors in Pregnancy and the ** (2007, decoy-pregnancy-safety) -> VERIFIED  doi=10.1056/nejmoa066584  J=1.0  [article]  auth=True  (New England Journal of Medicine)
- **Depression, anxiety, and antidepressant treatment in women: associat** (2016, decoy-art) -> VERIFIED  doi=10.1016/j.fertnstert.2016.01.036  J=1.0  [journal-article]  auth=True  (Fertility and Sterility)
- **Antipsychotic-Induced Hyperprolactinaemia** (2004, decoy-psychotropic) -> VERIFIED  doi=10.2165/00003495-200464200-00003  J=1.0  [journal-article]  auth=True  (Drugs)
- **Inhibition of egg production in zebrafish by fluoxetine and municipa** (2009, decoy-animal) -> VERIFIED  doi=10.1016/j.aquatox.2009.04.011  J=1.0  [journal-article]  auth=True  (Aquatic Toxicology)
- **A Placebo-Controlled Trial of Bupropion SR as an Antidote for Select** (2004, decoy-clinical) -> VERIFIED  doi=10.4088/jcp.v65n0110  J=1.0  [journal-article]  auth=True  (The Journal of Clinical Psychiatry)

## Notes

- **Four gates, four distinct failures.** The existence gate catches ghosts: titles resolving to nothing. The version gate catches the mirror failure: a title resolving to a preprint, reprint or repository copy of the right work. The book-canon gate catches a real, correctly-titled, contemporaneous record of a *different* work — a review of the monograph. The shadow gate, added here, catches a fourth: a real, separately-DOI'd record whose title *contains* the target title behind a qualifier. None substitutes for another.
- **The shadow gate was not designed in the abstract.** Five shadows sit on this chapter's own anchors, in four shapes: `Editorial Comment to ...` on Beeder and Samplaski 2019, `Faculty Opinions recommendation of ...` on Montejo et al. 2001 and Serretti and Chiesa 2009, `Re: ...` on Tanrikut et al. 2009, and `Expression of Concern: ...` on Safarinejad 2008. The Montejo case is the sharpest: neither index record of the study itself carries a DOI, while the Faculty Opinions record does, so a DOI-preferring resolver without this gate anchors a 1,022-patient incidence study to a one-paragraph post-publication comment.
- **An integrity shadow is evidence, not noise.** The Expression of Concern on Safarinejad 2008 is refused as an anchor and recorded as a flag on the anchor. A gate that merely refused it would have discarded the most consequential thing the index knows about one of this chapter's mechanism sources; risk of bias reads the flag before the effect size is used.
- **Version-gate test cases are in the set deliberately.** Casilla-Lennon et al. has three co-existing records including a repository copy; Alwan et al. 2007 has three reprint-shaped twins in survey and yearbook venues, one of them credited to a different author entirely; Wilcox et al. 1995 has an *Obstetrical & Gynecological Survey* twin; Hull et al. 2004 carries two DOIs in one journal. A gate with nothing to catch has not been tested.
- **The decoys carry the walls, not the topic.** Alwan et al. 2007 (Wall 4, pregnancy safety), Cesta et al. 2016 (Wall 5, ART), Haddad and Wieck 2004 (Wall 6, antipsychotics), Lister et al. 2009 (Wall 7, non-human), Power et al. 2013 (Wall 1, the disorder rather than the drug), and Clayton et al. 2004 (clinical management of the side effect) each sit just across one wall. Per the D.2.d finding, these are forward-cited like any other seed at A4: a decoy's citation neighbourhood is where the boundary cases live. The Clayton 2004 decoy shares an author with two link-1 anchors on purpose, so the routing test cannot be passed by author-based topical similarity.
- **LINK2 has no anchor, and the gap is the point.** Two live probes for records estimating sexual dysfunction against coital frequency returned nothing on target. The scope document predicted the chain's second joint would be unmeasured; recording the absence keeps it visible instead of letting a link-1 record stand in for it.
- **Three defects were found and fixed by auditing this script's own output**, which is why the run is recorded rather than merely reported, and all three were visible only in the *refused* set. (1) The shadow gate's general containment rule — candidate title appearing as a suffix of a record title — refused five records on the three-token anchor 'Antipsychotic-Induced Hyperprolactinaemia', and every one was a distinct paper rather than a comment on this one. Suffix containment cannot tell a comment from a different work, and no token threshold fixes it; the rule was removed and the named-qualifier list kept. (2) Alwan et al. 2007 resolved to the *Obstetrical & Gynecological Survey* reprint rather than the NEJM original — the exact failure that candidate was planted to test. The original and the digest scored identically on every existing signal and the tie broke on list order, so republishing venues now carry an explicit penalty and ties are broken by a stated rule. (3) That fix immediately created its own regression, moving Serretti and Chiesa 2009 from the journal article to a European Psychiatry conference abstract, because the new tie-break's last term was DOI string order. Deterministic and wrong is not an improvement on accidentally right; title fit was added ahead of it, which is a term that means something.
- **LEAKAGE WALL.** Beeder and Samplaski 2019 and Serretti and Chiesa 2009 enter as channel-1 review seeds. Their search strategies must NOT be mined for A6 query terms, since their included studies feed anchors here.
- **Empirical recall denominator.** Only the `PRIMARY_*` anchors count. The link-support, mechanism, parameter, measurement and theory anchors are indispensable to the chapter's demographic-significance computation and to its mechanism section, and they are not evidence for the causal claim; scoring recall against them would measure the wrong thing (scope doc, Call 4).
