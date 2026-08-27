# Title/abstract screen report — A.23 co-residence and delayed household formation

**Ticket:** TICK-075 · **Screen run:** 2026-08-27 · **Frame:** 1,572 records, 29 batches
**Scripts:** `227` (rubric and batches), `228` (assembly and gold audit)
**Outputs:** `…-screened.json`, 29 verdict files under `source/build/goldset/a23_screen_verdicts/`

Every record in the frame was screened. Nothing was sampled, capped or deferred.

## 1. Outcome

| Verdict | n | share |
|---|---|---|
| NOT_RELEVANT | 1,097 | 69.8% |
| UNCERTAIN | 397 | 25.3% |
| RELEVANT | 78 | 5.0% |

| Estimand cell | n |
|---|---|
| `PRIMARY_EXTENDED_COUPLE` | 48 |
| `PRIMARY_PRELAUNCH` | 38 |
| `MIXED_PRICE_ARRANGEMENT` | 26 |
| `PRIMARY_PROXIMITY` | 4 |
| `LINK1_DRIVER_TO_ARRANGEMENT` | 191 |
| `LINK1_ARRANGEMENT_TO_UNION` | 11 |
| `ELDER_SUPPORT` (the homonym) | 148 |
| `OFF_CHILDCARE_C2a` | 44 |
| `OFF_OUTCOME` / `OFF_OUTCOME_LABOUR_SUPPLY` | 86 / 14 |
| `THEORY` | 82 |
| `REVERSE` | 17 |
| `INSUFFICIENT_INFO` | 34 |
| other route-outs (`OFF_OTHER`, D.2.b, A.7, C.3.g) | 829 |

**116 records reach the four primary cells.** 574 records have the living arrangement
as their exposure; of those, 19 carry an identified design.

## 2. The gold audit, which is what the blinding was for

The frame recorded which records were gated anchors and which were decoys. The batches
withheld both, so the screen's treatment of them is an out-of-sample test of the rubric.

**Decoys: 4 in frame, 0 marked RELEVANT.** The routing test passes.

**Gold: 12 in frame, 9 kept, 3 rejected.** And the three rejections are the finding, not
the failure. All three route to `OFF_CHILDCARE_C2a`:

- *Fertility cost, grandparental childcare, and female employment*
- *Roadblocks on the Road to Grandma's House: Fertility Consequences of Delayed Retirement*
- *Stay at Home with Grandma, Mom Is Going to Work*

These are the same error class the 222/223 calibration was already correcting: the
exposure is the grandmother's TIME, not the living arrangement. Two of the three survived
the 223 exposure audit only because that audit had no abstract to read; the third had
co-residence language in its abstract but not as the treatment. **A blinded screen,
reading only titles and abstracts, independently extended the reclassification by three
records.** On the corrected gold set the screen's recall is 9 of 9.

The same test on the nine anchors already reclassified: five are in the frame, and the
screen says `exposure_is_arrangement: no` on four of them without being told. The fifth
is the title-only record whose abstract-bearing duplicate is what caught the error in the
first place — so even the disagreement is the known limitation, not a new one.

**The rubric's central test works at scale.** That was not obvious in advance: it was
built from nine hand-audited anchors and it held across 1,572 records screened blind.

## 3. What the screen measured that the scope had only predicted

**§6 was too pessimistic about the configuration split.** The scope said the pre-launch
versus extended-household distinction turns on who depends on whom at what life stage,
and would therefore usually be a full-text fact. Among the 574 records whose exposure is
the arrangement, `config` came back `cannot_tell` **6.8%** of the time. The split is
mostly visible at title and abstract, and the RA gate inherits far less routing work than
§13 budgeted.

**The elder-support homonym is the single largest on-topic route-out: 148 records.**
Larger than every primary cell combined bar one. §6's warning was correct in kind and
understated in size.

**`OFF_OUTCOME_LABOUR_SUPPLY` came in at 14, not the largest route-out** the snowball log
predicted. The prediction was drawn from the most-seeded records of the citation pool,
which over-represented the grandparental-childcare-and-employment literature; on the
frame, `OFF_CHILDCARE_C2a` (44) and the arrangement-with-a-non-fertility-outcome bucket
(86) are the bigger drains.

**The no-abstract rule was applied 68% of the time in the direction the rubric warned
against.** 241 records have no indexed abstract; 165 were marked NOT_RELEVANT on the title
alone. The rubric permits this only when the title is decisive, and in the large majority
it plainly is — 109 of the 165 route to `OFF_OTHER` (hip stems, soil mapping, LLM
distillation). But the share is high enough that it is recorded here rather than assumed
benign: **the RA gate should re-read a stratified sample of the no-abstract NOT_RELEVANTs**,
because that bucket is where a title-only false negative would hide, and this chapter has
already been bitten once by trusting a title-only record.

**Both hand-added records screened RELEVANT.** The two records the boolean query provably
could not reach — the urban Mexico household-structure paper and the Indonesian living
arrangement and homeownership paper — were kept by a screener who did not know they had
been added by hand. The 226 supplement earned itself back.

## 4. Scope amendments the screen generated

Recorded here for the freeze; none are made unilaterally.

1. **A configuration §6 does not have.** *"Family-anchored" transitions to adult life in
   Mexico* (Demographic Research) documents young adults CO-RESIDING WITH PARENTS WHILE
   forming a first partnership and becoming a parent. The birth happens INSIDE the parental
   household. That is neither `PRE_LAUNCH` (which presumes childlessness) nor
   `EXTENDED_COUPLE` (which presumes a formed couple), and it dissolves the ordering §3 is
   built on rather than complicating it. Latin American records repeatedly show this shape.
2. **The parents' side of the mechanism**, in at least seven records: the arrangement as a
   cost to the parents' budget, retirement timing, and wellbeing. §1 is written entirely
   from the young adult's autonomy.
3. **Living-apart-together**, in six records across Spain, Sweden, France and the
   Netherlands: partnered without co-residing, which breaks the assumed equivalence between
   forming a union and forming a household.
4. **Designs §4 never enumerated**, all with real papers behind them: DACA eligibility
   cutoffs; ancestral matrilocality as an instrument; apartheid-era legal constraints on
   household formation; a parent's own age at leaving home; compulsory-schooling reform
   interacted with patrilocality; and geology as a determinant of household formation rules.
5. **Named data resources** the chapter should use directly: the CORESIDENCE Database
   (harmonised, multi-decade, cross-national, on this exact exposure) and the UNECE FFS /
   GGS families that carry the arrangement and the birth in one instrument.
6. **Two measurement warnings** for extraction: own-children fertility estimation requires
   the child to co-reside with the mother, so in a chapter about co-residence the
   measurement error is correlated with the exposure; and co-residence trend series are
   contaminated by rising childlessness among elders, who have no co-residence option.

## 5. What this leaves for the RA gate

- **116 primary-cell records** and 202 link-1 records to route confirm.
- **34 `INSUFFICIENT_INFO`** plus 71 no-abstract UNCERTAINs to resolve at retrieval.
- **A stratified re-read of the no-abstract NOT_RELEVANTs** (§3 above).
- **26 `MIXED_PRICE_ARRANGEMENT` records**, which are not an RA decision at all: they are
  the Wall 1 second-read packet, and they now contain most of the identified evidence
  bearing on the registered claim.
