# D.1.a — Tier-1 design probe: hunting identification, not topic

**Hypothesis:** D.1.a, slug `postmaterialism-individualism-secularization`
**Stage:** GACS Phase A3, cold-start channels 2 and 4, targeted at design rather than subject
**Run:** 2026-08-03 (Shravan/Claude), live OpenAlex
**Script:** `source/build/goldset/90_d1a_tier1_design_probe.py`
**Raw output:** `temp/d1a/tier1-design-probe.json`, `temp/d1a/tier1-design-probe.md`

24 probes, all under the five-operator cap, 257 distinct records in the union. Candidates only:
nothing below has cleared the existence gate.

---

## Why the probe was run this way

The channel-1 probe returned thirteen S3 candidates and not one was a natural experiment. A topical
probe sorted by citation returns the field's canon, and this field's canon is cross-sectional, so
sorting by topic cannot find Tier 1 material even when it exists. This probe searched instead for the
**vocabulary of the design** (natural experiment, instrument, difference-in-differences, regression
discontinuity) and for the **names of specific shocks** (church tax, blue laws, state atheism,
clergy scandal, religious deregulation, secular schooling).

The five-operator cap discovered on the channel-1 run forced the structure: 24 narrow probes with the
union assembled client-side, rather than one wide boolean. That worked, and every probe returned. It
is the pattern the production query will have to adopt.

---

## Result: Tier 1 exists, and it is very small

**Three credible Tier 1 candidates, all in S3, all published in the last eight years.**

| Candidate | Design | Note |
|---|---|---|
| `10.1086/696193` — "Political Islam, Marriage, and Fertility: Evidence from a Natural Experiment," *American Journal of Sociology* 2018, 33c | Self-described natural experiment | The strongest-looking Tier 1 candidate found. Treatment direction is toward the religious pole, so Ruling 5's sign flip applies |
| `10.1016/j.ssresearch.2026.103371` — "Secularization and low fertility: How declining church membership changes couples' childbearing," *Social Science Research* 2026, 0c | Church-membership decline | Surfaced by the church-tax probe. Brand new, uncited, and directly on the pair |
| `10.1007/s00148-025-01092-5` — "Religiously inspired baby boom: evidence from Georgia," *Journal of Population Economics* 2025, 2c | Religious-leader intervention | A discrete, dateable shock to religious practice with a fertility outcome |

**Four named-shock families came back empty or near-empty**, and the negative results are as
informative as the positive ones because they tell the chapter what the literature has never done:

- **Blue laws and Sunday trading: zero hits.** The Gruber-Hungerman design family has been applied to
  religiosity and to drinking, drug use, and crime, and apparently never to fertility.
- **Clergy-scandal shocks: zero hits.** Same story.
- **Secular schooling as a religiosity shock: two hits**, both versions of one Turkish working paper
  ("For the Love of the Republic: Education, Secularism, and Empowerment"), and its treatment is a
  schooling reform, so it likely routes out under Wall 7 and the schooling entries.
- **State atheism campaigns: five hits, none usable.** The probe returned cultural history of Soviet
  and Chinese anti-religious campaigns with no fertility outcome. The Soviet and Albanian episodes are
  the largest deliberate secularization shocks in history and appear not to have been used to identify
  a fertility effect.

**The chapter should report this.** The best-identified designs available for moving religiosity
exogenously have been applied to other outcomes and not to fertility. That is a specific, checkable
statement about a gap, and it belongs in §10 as the recommended study.

---

## What the probe changed in the scope's expectations

**1. S1 is not empty of estimates. It is empty of *identified* estimates.** The scope predicted very
few fertility estimates for postmaterialism. The probe found several, and they are real studies rather
than framework statements:

- `10.2307/1972499` — Lesthaeghe and Surkyn, "Cultural Dynamics and Economic Theories of Fertility
  Change," *PDR* 1988, **719c**. A v5 `seminal` name, now confirmed to exist.
- `10.1111/padr.12490` — "Theories of Postindustrial Fertility Decline: An Empirical Examination,"
  *PDR* 2022. An explicit empirical horse-race between the competing accounts, which makes it a
  priority read: it is the closest thing the literature has to a test of D.1.a against its rivals.
- `10.1515/zfsoz-1990-0105` — "Postmaterialismus und generatives Verhalten," *Zeitschrift für
  Soziologie* 1990. A direct postmaterialism-to-fertility study, in German.
- "Postmodern fertility preferences: from changing value orientation to new behaviour," *PDR* 1998,
  242c, **no DOI** — keyed on title under the resolution rule, not dropped.

The refinement matters for the rating. S1 will have studies to include, and on their face they are
Tier 3, so the pair can be *reported* without being *rated* above Very Low. That is a different and
more defensible chapter section than "no evidence exists."

**2. A language-coverage question the scope did not raise.** The German-language postmaterialism study
is a reminder that this literature's core European material is not all in English, and Lesthaeghe's
own early work is partly Dutch and French. An English-only production query would systematically drop
the FDT-era and continental European material that Ruling 4 just admitted. Flagged for the query
build; it needs a decision, not a default.

**3. The reverse-causality threat now has a measurement, and it is inside the pool.**
`10.1093/esr/jcac060` — "Does forming a nuclear family increase religiosity? Longitudinal evidence
from the British Household Panel Survey," *European Sociological Review* 2022 — estimates the arrow
running the other way. Under the scope this is a `REVERSE` cell record and carries no effect estimate
for the chapter, but it is the single most useful paper found today, because threat 1 is this
chapter's binding risk-of-bias domain and this paper sizes it. Priority read, and it should be cited
in the risk-of-bias section rather than buried in a context list.

**4. The Tier 2 ex-ante cell is populated, which was not guaranteed.** `PRIMARY_VALUE_EX_ANTE` is the
scope's value-added cell, and the probe found real candidates for it: religious socialisation and
third births in the Netherlands (`10.1007/s10680-009-9185-y`), religiosity and the realisation of
fertility intentions across eight European countries (`10.1002/psp.2433`), and cohort trends in
Britain, France and the Netherlands (`10.1007/s10680-015-9371-z`). The chapter will have a Tier 2
stratum even if Tier 1 stays at three studies.

**5. Fernández and Fogli 2009 is confirmed and Wall 5 is live.** `10.1257/mac.1.1.146` — "Culture: An
Empirical Investigation of Beliefs, Work, and Fertility," *AEJ: Macroeconomics*, **1242c**. It is the
most-cited record in the entire union, it is listed as seminal under A.19, and its routing turns on
whether the culture proxy is ancestral fertility or an ancestral value measure. It must be read at
full text before it is assigned, not routed from the abstract.

---

## The clinical collision recurs inside the design probes

Filtering by design vocabulary did not escape the problem the channel-1 run found. `design_iv`
returned livestock reproduction, ART multiple births, and haemophilia; `group_high_fertility_sects`
returned human-genetics work on Hutterite HLA antigens and inbreeding alongside the demography. The
Hutterite case is the sharpest illustration: the same population is studied by demographers for
natural-fertility norms and by geneticists for consanguinity, and both literatures use the words
*Hutterite* and *fertility*.

This is now observed in three separate probe designs. It is a property of the outcome vocabulary
rather than of any one query, and the production query needs an explicit exclusion or field strategy
built in from the start.

---

## Candidate pool assembled (not verified, not frozen)

257 distinct records across 24 probes, spanning all five pairs plus three decoy families (A.20 media
exposure, D.2.a gender-role attitudes, A.6 contraceptive stigma). The decoys are deliberate: the
anchor set has to test routing as well as topical retrieval, and routing is this chapter's dominant
screening cost.

**Next step is the existence gate.** Every candidate that will enter a recall denominator must resolve
through a live Crossref bibliographic match and a doi.org re-affirmation, per the standing rule from
the 2026-07-08 run. Candidates carrying no DOI — the 1998 *PDR* postmodern-fertility-preferences paper,
the 1953 Hutterite demography paper, several RePEc working papers — are kept and keyed on title rather
than dropped, since dropping them would bias the denominator toward recent and easily found work.
