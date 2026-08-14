# A3 cold-start anchors — microplastics-pfas-reproductive (B.6)

Sourced in a live OpenAlex pass (2026-08-14) and resolved through five gates: 32 candidate anchors, of which 9 are empirical primary-cell anchors (the causal recall denominator) and the rest are link-support, mechanism, parameter, measurement, theory, or routing-decoy anchors that earn no empirical recall credit. No DOI is hand-asserted; each is the top-ranked version-of-record candidate from a unified Crossref + OpenAlex field, then re-affirmed at doi.org.

**Verified (live DOI): 32**  ·  **Year-drift keep (real, RA-confirm): 0**  ·  **Flagged for RA: 0**  ·  **Expected index miss (no DOI by nature): 0**

**Shadow records refused: 12** across 5 anchors.  **Integrity flags raised: 1.**

**Duplicate records demoted: 0** across 0 anchors. The duplicate gate is NEW and, on this corpus, UNVALIDATED: the Minderoo-Monaco pair that motivated it turned out to be two different works sharing a title, separated correctly by the author gate. Zero here means the gate did not fire, not that it was confirmed. Each demotion, if any, names the copy kept, the copy set aside and both citation counts, so an RA can check the choice rather than take it on trust.

**Records refused as a review of the work, or on authorship: 0.** Every refusal keeps its record in the JSON so the RA can audit what was refused rather than trusting that nothing was lost.

## Coverage by estimand cell (verified / total)

- `DETECTION_TISSUE`: 7/7
- `ENDOCRINE_MECHANISM`: 1/1
- `MIXTURE_UNSEPARABLE`: 1/1
- `OFF_ANIMAL`: 1/1
- `OFF_LEGACY_EDC_B2`: 1/1
- `OFF_PREGNANCY_SAFETY`: 2/2
- `OUTCOME_TREND_UNATTRIBUTED`: 1/1
- `OVARIAN_PARAMETER`: 1/1
- `PARAMETER_EXPOSURE`: 2/2
- `PARAMETER_PHARMACOKINETIC`: 4/4
- `PRIMARY_EXPOSURE_TO_FERTILITY`: 8/8
- `PRIMARY_HIGH_EXPOSURE`: 1/1
- `SEMEN_PARAMETER`: 2/2

## Coverage by query-cluster family (verified / total)

- channel1: 3/3
- commission: 1/1
- decoy-wall1-b2: 1/1
- decoy-wall1-mixture: 1/1
- decoy-wall2-pregnancy: 2/2
- decoy-wall5-animal: 1/1
- decoy-wall7-trend: 1/1
- detection-mp: 6/6
- detection-pfas: 1/1
- exposure-series: 1/1
- high-exposure: 1/1
- mechanism: 2/2
- pharmacokinetic: 3/3
- primary-pfas-female: 5/5
- primary-pfas-male: 3/3

## Integrity flags — read before using these effect sizes

Raised by the shadow gate, which noticed an Expression of Concern, retraction or correction record sitting on an anchor. These are facts about the work, carried forward to extraction and risk of bias rather than logged and forgotten.

- **The Minderoo-Monaco Commission on Plastics and Human Health** (2023) — integrity: *Correction: The Minderoo-Monaco Commission on Plastics and Human Health* (2023) `10.5334/aogh.4331`
- **The Minderoo-Monaco Commission on Plastics and Human Health** (2023) — integrity: *Correction: The Minderoo-Monaco Commission on Plastics and Human Health* (2023) `10.5334/aogh.4331`

## Per-candidate disposition

- **Maternal levels of perfluorinated chemicals and subfecundity** (2009, primary-pfas-female) -> VERIFIED  doi=10.1093/humrep/den490  J=1.0  [journal-article]  auth=True  (Human Reproduction)
- **Perfluorinated Compounds and Subfecundity in Pregnant Women** (2011, primary-pfas-female) -> VERIFIED  doi=10.1097/ede.0b013e31823b5031  J=1.0  [article]  auth=True  (Epidemiology)
- **Association between perfluorinated compounds and time to pregnancy i** (2012, primary-pfas-female) -> VERIFIED  doi=10.1093/humrep/der450  J=1.0  [journal-article]  auth=True  (Human Reproduction)
- **Perfluoroalkyl acids and time to pregnancy revisited: An update from** (2015, primary-pfas-female) -> VERIFIED  doi=10.1186/s12940-015-0040-9  J=1.0  [journal-article]  auth=True  (Environmental Health)
- **Maternal exposure to perfluorinated chemicals and reduced fecundity:** (2015, primary-pfas-female) -> VERIFIED  doi=10.1093/humrep/deu350  J=1.0  [journal-article]  auth=True  (Human Reproduction)
- **Do Perfluoroalkyl Compounds Impair Human Semen Quality?** (2009, primary-pfas-male) -> VERIFIED  doi=10.1289/ehp.0800517  J=1.0  [journal-article]  auth=True  (Environmental Health Perspectives)
- **Exposure to perfluorinated compounds and human semen quality in arct** (2012, primary-pfas-male) -> VERIFIED  doi=10.1093/humrep/des185  J=1.0  [journal-article]  auth=True  (Human Reproduction)
- **Endocrine Disruption of Androgenic Activity by Perfluoroalkyl Substa** (2018, primary-pfas-male) -> VERIFIED  doi=10.1210/jc.2018-01855  J=1.0  [journal-article]  auth=True  (The Journal of Clinical Endocrinol)
- **Perfluoroalkyl substances (PFAS) in drinking water and risk for poly** (2021, high-exposure) -> VERIFIED  doi=10.1016/j.envint.2021.106819  J=0.789  [journal-article]  auth=True  (Environment International)
- **Plasticenta: First evidence of microplastics in human placenta** (2020, detection-mp) -> VERIFIED  doi=10.1016/j.envint.2020.106274  J=1.0  [article]  auth=True  (Environment International)
- **First evidence of microplastics in human ovarian follicular fluid: A** (2025, detection-mp) -> VERIFIED  doi=10.1016/j.ecoenv.2025.117868  J=1.0  [journal-article]  auth=True  (Ecotoxicology and Environmental Sa)
- **Detection and characterization of microplastics in the human testis ** (2023, detection-mp) -> VERIFIED  doi=10.1016/j.scitotenv.2023.162713  J=1.0  [journal-article]  auth=True  (Science of The Total Environment)
- **Microplastic presence in dog and human testis and its potential asso** (2024, detection-mp) -> VERIFIED  doi=10.1093/toxsci/kfae060  J=1.0  [journal-article]  auth=True  (Toxicological Sciences)
- **Discovery and quantification of plastic particle pollution in human ** (2022, detection-mp) -> VERIFIED  doi=10.1016/j.envint.2022.107199  J=1.0  [journal-article]  auth=True  (Environment International)
- **Detection of Various Microplastics in Human Stool** (2019, detection-mp) -> VERIFIED  doi=10.7326/m19-0618  J=1.0  [journal-article]  auth=True  (Annals of Internal Medicine)
- **Nontargeted identification of per- and polyfluoroalkyl substances in** (2020, detection-pfas) -> VERIFIED  doi=10.1016/j.envint.2020.105686  J=1.0  [journal-article]  auth=True  (Environment International)
- **Half-Life of Serum Elimination of Perfluorooctanesulfonate, Perfluor** (2007, pharmacokinetic) -> VERIFIED  doi=10.1289/ehp.10009  J=1.0  [journal-article]  auth=True  (Environmental Health Perspectives)
- **Determinants of plasma concentrations of perfluoroalkyl substances i** (2013, pharmacokinetic) -> VERIFIED  doi=10.1016/j.envint.2012.12.014  J=1.0  [journal-article]  auth=True  (Environment International)
- **Perfluorinated Alkyl Acids in Blood Serum from Primiparous Women in ** (2012, pharmacokinetic) -> VERIFIED  doi=10.1021/es301168c  J=1.0  [journal-article]  auth=True  (Environmental Science &amp; Techno)
- **Trends in Exposure to Polyfluoroalkyl Chemicals in the U.S. Populati** (2011, exposure-series) -> VERIFIED  doi=10.1021/es1043613  J=1.0  [journal-article]  auth=True  (Environmental Science &amp; Techno)
- **Perfluoroalkyl and polyfluoroalkyl substances and measures of human ** (2016, channel1) -> VERIFIED  doi=10.1080/10408444.2016.1182117  J=1.0  [journal-article]  auth=True  (Critical Reviews in Toxicology)
- **The effects of perfluoroalkyl and polyfluoroalkyl substances on fema** (2022, channel1) -> VERIFIED  doi=10.1016/j.envres.2022.114718  J=1.0  [review]  auth=True  (Environmental Research)
- **Persistent organic pollutants and couple fecundability: a systematic** (2020, channel1) -> VERIFIED  doi=10.1093/humupd/dmaa037  J=1.0  [journal-article]  auth=True  (Human Reproduction Update)
- **Perfluoroalkyl and polyfluoroalkyl substances (PFAS) and their effec** (2020, mechanism) -> VERIFIED  doi=10.1093/humupd/dmaa018  J=1.0  [journal-article]  auth=True  (Human Reproduction Update)
- **Per- and poly-fluoroalkyl substances (PFAS) and female reproductive ** (2021, mechanism) -> VERIFIED  doi=10.1016/j.tox.2021.153031  J=1.0  [article]  auth=True  (Toxicology)
- **The Role of Peroxisome Proliferator-Activated Receptor Gamma (PPARga** (2019, decoy-wall1-b2) -> VERIFIED  doi=10.1289/ehp3730  J=0.895  [journal-article]  auth=True  (Environmental Health Perspectives)
- **Reducing exposure to high levels of perfluorinated compounds in drin** (2020, decoy-wall2-pregnancy) -> VERIFIED  doi=10.1186/s12940-020-00591-0  J=1.0  [journal-article]  auth=True  (Environmental Health)
- **Relationship of Perfluorooctanoic Acid Exposure to Pregnancy Outcome** (2012, decoy-wall2-pregnancy) -> VERIFIED  doi=10.1289/ehp.1104752  J=1.0  [journal-article]  auth=True  (Environmental Health Perspectives)
- **Association between chemical mixtures and female fertility in women ** (2022, decoy-wall1-mixture) -> VERIFIED  doi=10.1016/j.envres.2022.114447  J=1.0  [article]  auth=True  (Environmental Research)
- **Oyster reproduction is affected by exposure to polystyrene microplas** (2016, decoy-wall5-animal) -> VERIFIED  doi=10.1073/pnas.1519019113  J=1.0  [journal-article]  auth=True  (Proceedings of the National Academ)
- **Temporal trends in sperm count: a systematic review and meta-regress** (2017, decoy-wall7-trend) -> VERIFIED  doi=10.1093/humupd/dmx022  J=1.0  [journal-article]  auth=True  (Human Reproduction Update)
- **The Minderoo-Monaco Commission on Plastics and Human Health** (2023, commission) -> VERIFIED  doi=10.5334/aogh.4056  J=1.0  [journal-article]  auth=True  (Annals of Global Health)

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
