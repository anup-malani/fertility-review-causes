# Rulings 4–5 and the six scope amendments — A.23

**Ticket:** TICK-075 · **Taken:** 2026-08-28 (Shravan; PI confirmation pending)

Ruling 3 (Wall 1) is in `…-wall1-ruling.md`. This settles the pooling rule and disposes of
the six amendments the screen generated, so that the scope can be frozen and stage 6 can run
against a fixed instrument. **Every one of these is reversible on a PI word; none is silent.**

---

## Ruling 4 — the pooling rule

> **Estimates are pooled only within a cell, and within a cell only within an estimator class.
> (Shravan, 2026-08-28; PI confirmation pending.)**

Three strata, applied in order. An estimate that cannot be placed is reported and not pooled.

**1. Configuration.** `PRE_LAUNCH`, `EXTENDED_COUPLE` and `PRIMARY_PROXIMITY` pool separately and
are never combined, per Ruling 1. `AGGREGATE_UNSPLIT` is secondary and enters no pool unless the
life-stage composition of the sample is reported, because without it the estimate's sign is a
property of the sample's mix.

**2. Outcome level.** Realized births and stated intentions pool separately, on the standing D.3.b
rule. One Wall 1 record (`10.7454/jessd.v6i1.1145`) is an intention study and is the reason this
stratum binds here rather than being inherited boilerplate.

**3. Estimator class — and this is the stratum this chapter turns on.** Within a configuration,
estimates that correct for the endogeneity of the arrangement do **not** pool with estimates that do
not.

The reason is a specific record, not a general principle. Chu, Xie and Yu's *Coresidence With
Husband's Parents, Labor Supply, and Duration to First Birth* (Demography) reports that treating
co-residence as endogenous **reverses the sign** on time to first birth: uncorrected, co-residence
looks like it accelerates childbearing; corrected, it delays it. The chapter's §3 says the exposure
and the outcome are events in the same life-course sequence, so this is the expected failure and not
a curiosity.

**Averaging across that boundary would produce a number no study estimates and whose sign is set by
how many uncorrected studies happen to be in the pool.** This is the A.12 rule — ask whether
disagreeing estimates share an estimator before pooling them — arriving with a worked instance.
`ANTICIPATION_CONTROL` is already a required tag (§9); it is now also a pooling stratum, and its
distribution is reported whether or not anything is pooled.

**Consequence, stated in advance.** On the counts available, no cell will hold three
estimator-matched effects. **The chapter should expect narrative synthesis, not meta-analysis**,
and the acceptance criterion's "meta-analysis if ≥3 extractable effects" is met by the ≥3 test
applied *after* stratification, not before.

---

## Ruling 5 — the six amendments

### 1. A configuration §6 does not have — **ADOPTED**

Latin American records show young adults co-residing with parents *while* forming a first
partnership and having a first child. The birth happens inside the parental household. That is
neither `PRE_LAUNCH` (which presumes childlessness) nor `EXTENDED_COUPLE` (which presumes a formed
couple that moved in).

`LIFE_STAGE_CONFIG` takes a fourth value, **`COFORMING`**, and it pools separately.

This is not bookkeeping. §3's whole difficulty is that the exposure precedes the outcome in one
sequence; `COFORMING` is the case where **there is no ordering to exploit**, because union
formation, the birth and the arrangement are simultaneous. Estimates from it cannot be read as
"co-residence delayed the birth" under any design, and folding them into `PRE_LAUNCH` — which is
where an unamended screen would have put them — would have imported that unreadability into the
cell carrying the registered claim. Same shape as the A.17 finding that an "ambiguous" residue was
a missing category rather than genuine ambiguity.

### 2. The parents' side of the mechanism — **ADOPTED, as a recorded field, not a cell**

Seven records treat the arrangement as a cost to the *parents* — their budget, their retirement
timing, their wellbeing. §1 is written entirely from the young adult's autonomy.

Recorded as `MECHANISM_SIDE` ∈ {`child`, `parent`, `both`} on every included effect. It does not
create an estimand cell: the estimand is still the arrangement's effect on fertility, and whose
utility the mechanism runs through is a heterogeneity fact. It is worth recording because a
chapter that only ever states the child's side will read the extended-household sign as puzzling
when it is not.

### 3. Living-apart-together — **ADOPTED, as a setting flag**

Six records across Spain, Sweden, France and the Netherlands describe partnered couples who do not
co-reside. This breaks the assumed equivalence between forming a union and forming a household —
the same equivalence `SETTING_COHABITATION_NORM` (§9) exists to test in the other direction.

The tag is widened to three values: `cohabitation_common`, `cohabitation_rare_marriage_is_the_event`,
`lat_prevalent`. Where LAT is prevalent, "left the parental home" and "formed a union" come apart in
a third way and the chapter must not treat leaving home as a union proxy.

### 4. Six designs §4 never enumerated — **ADOPTED into §4**

DACA eligibility cutoffs; ancestral matrilocality as an instrument; apartheid-era legal constraints
on household formation; a parent's own age at leaving home; compulsory-schooling reform interacted
with patrilocality; and geology as a determinant of household formation rules.

§4 enumerated eight admissible sources of variation before searching, which was the right order.
These six are what the literature actually used, and **one of them is already retrieved**: Grogan's
Vietnam study instruments household formation rules with the suitability of land for plough
agriculture. It is the frame's only instrument for the *arrangement itself* rather than for a
price — the thing §4 said it wanted and did not expect to find.

Adopting them is not retrospective query-fitting: the frame is already pulled and screened, and
these records are in it. What adopting changes is the chapter's §4 table and its statement of what
identified variation exists, which currently understates it.

### 5. Named data resources — **ADOPTED WITH A SCOPE LIMIT**

The CORESIDENCE Database (harmonised, multi-decade, cross-national, on exactly this exposure) and
the UNECE FFS / GGS families, which carry the arrangement and the birth in one instrument.

**They are recorded for the demographic-significance section's exposure-trend input and for the
research-agenda section. They are not a new empirical exercise inside this chapter.** A systematic
review that estimates its own effect stops being one. The honest use is: the exposure trend needed
for §10 has a harmonised source, so the chapter's exposure series does not have to be assembled
from the studies' own descriptives — which would inherit their selection.

### 6. Two measurement warnings — **ADOPTED into risk-of-bias**

Both become named items in the stage-8 instrument rather than prose.

- **Own-children fertility estimation requires the child to co-reside with the mother.** In a
  chapter about co-residence, the measurement error in the *outcome* is correlated with the
  *exposure*. Any study using an own-children estimator is flagged high risk on outcome
  measurement, and the direction is signed: it will tend to overstate fertility precisely in
  households where co-residence is high.
- **Co-residence trend series are contaminated by rising childlessness among elders**, who have no
  co-residence option to exercise. A rising share of "adults not living with a parent" partly
  measures the disappearance of the parent. This bites the exposure trend in §10, not the study
  estimates.

---

## What is now frozen, and what is not

**Frozen for stage 6:** the four configurations, the estimand cells as amended, the pooling rule,
the required tags as widened, and Wall 1 under Ruling 3.

**Not frozen, and flagged:** every ruling on this page and Rulings 1–3 are marked *PI confirmation
pending*. Five rulings taken by one RA is a lot of unconfirmed load-bearing structure, and it should
be read as a batch rather than one at a time. The v5 `claim` field edit (Ruling 1) is still open
with TICK-001.
