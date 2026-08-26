# TICK-073: C.3.g Student Debt and Household Formation Constraint
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `student-debt-household-formation` — HYPOTHESES-v5.md §C.3.g
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/student-debt-household-formation-*, extraction/student-debt-household-formation-*, output/chapters/student-debt-household-formation.md, source/build/goldset/199*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — DRAFT 2026-08-26, not frozen (Calls 1 and 5 open)
- [x] 3. Literature search and AI screening, both phases (§5.1) — C1 + D1 + D2/D3 done 2026-08-26; 610 screened, 114 forward
- [ ] 4. RA title/abstract review — 34 UNCERTAIN + the 22% multiple-outcome routing residue
- [ ] 5. Full-text retrieval — 114 records; the P2 candidate retrieved 2026-08-26, PDF is a browser-job
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/student-debt-household-formation.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-26 — Stage 2 (scope), drafted

Two probes, 71 requests, 0 failures. The frame is 394 records and can be screened whole.
Structural finding: the identified variation (210 records) and the registered outcome do not
intersect — student debt x fertility x identification is 2 records, neither an estimate, and the
policy-variation cell (forgiveness, repayment reform, tuition regime) is measured EMPTY. The
identified body sits on marriage, homeownership and co-residence, which v5's own claim names as the
mechanism, so the chapter is a two-arm chain chapter: arm 1 direct and associational (rated), arm 2
identified on link 1 with link 2 borrowed from A.7/A.23/C.2.c (a bound, not pooled).

Also found: a shared-resolver defect (an apostrophe-bearing word in a `title.search` query returns a
confident WRONG match at n=1, not a zero), and v5's C.3.g seminal list does not resolve at all.

### 2026-08-26 — Stage A3 (cold-start anchors), done

24 anchors, **20 verified live**, 1 year-drift keep, 1 flagged, 2 expected index misses. Empirical
recall denominator is **5** (3 realized fertility + 2 intentions) against 10 chain-arm anchors.

**Found and fixed a shared-resolver defect that refuses correct anchors.** `norm()` folds ASCII and
Unicode punctuation asymmetrically — an ASCII apostrophe becomes a SPACE (splitting a token) while a
curly apostrophe is non-ASCII and is DELETED (leaving it whole) — so a title normalises two different
ways depending on which side wrote it. First pass: 17/24, with three NO-MATCHes at J=0.588–0.700
against a 0.72 floor, including the chapter's most-cited primary-cell work. After folding both
punctuation classes before the ASCII strip: 20/24, all three recovered, the other 17 unchanged.

**This is the same character as the `200_` query defect, at a different stage and with the opposite
symptom** — query: wrong work ranked first; comparison: correct work refused as NO-MATCH. Fixing
either half alone leaves the anchor lost.

**Cross-chapter action outstanding:** the fix lives in this chapter's copy of the resolver. A sweep of
ten prior chapters' anchor logs found ONE refusal carrying the signature (D.1.b, *Women's empowerment
and fertility*), and a live re-test does NOT reproduce it, so its cause is unattributed. Note the
measurement is a LOWER BOUND: a case where the asymmetric fold lowered a Jaccard without crossing the
floor leaves no trace in these logs.

Also corrected: A.17's inherited `startswith("PRIMARY_")` counter, which reports 0 empirical anchors
while carrying twelve. It disengaged rather than failing.

### 2026-08-26 — Stage A4 (Tier A/B citation frame), done

Tier A 21 seeds, **Tier B 2,071 records**, no truncation on any seed. Only 39 (1.9%) of Tier B sit
inside the production query frame — the query and citation channels barely overlap, which is what
makes the recall measurement meaningful.

**THE SCOPE'S CENTRAL FINDING IS PARTLY OVERTURNED, by the channel built to contradict it.** P2 —
policy variation with a fertility outcome — is NOT empty. The citation channel surfaced *Experimental
Evidence on Consumption, Saving, and Family Formation Responses to Student Debt Forgiveness* (SSRN
2022, 10.2139/ssrn.4139814, 1 cite, three independent seeds): a randomized forgiveness evaluation
with a family-formation outcome, i.e. exactly the study the scope said did not exist. `200_` missed
it because its policy block lacked "debt forgiveness" and its outcome block lacked "family
formation", and because the record has no indexed abstract. Scope corrected in place. The surviving
claim: **no PUBLISHED policy-variation study with a fertility outcome; one uncited preprint**, which
must be retrieved before any verdict.

**The frame decision is settled on evidence.** Production frame reaches 13/21 anchors (13/15
empirical); a fertility-only frame reaches 5/21 and loses *every identified study in the chapter*.

**Two anchors are unreachable by the frame**, one of them Nau et al., the most-cited primary-cell
work — no abstract, and a title saying "Debt" and "baby". The priced cost of student-anchoring the
exposure against the sovereign-debt homonym: 2 of 15. Tier A enters the screen by hand.

**Scope revised:** the attainment confound is 28% visible in-frame, not the ~invisible the scope
declared from 8 query-level records. Screen carries a flag; the gate stays at full text.

**A diagnostic refuted by its own output:** `IDENT_TERMS` had "natural experiment" and "randomi" but
no bare "experiment", so it scored the run's most important record — titled *Experimental Evidence* —
as unidentified. 78 Tier-B records name "experiment"; the list missed 46. Fixed and guarded by
`ident_vocab_selftest()`; identified-fertility-with-debt goes 3 -> 5.

### 2026-08-26 — C1 production pull, D1 rank, and the title/abstract screen

Keyword channel pulled 401 of a reported 400; pool = keyword ∪ citation ∪ anchors = **2,426**, of
which 53 were found by BOTH channels and **8 anchors had to be carried in by hand** because the frame
cannot reach them. D1 collapsed 177 version duplicates and cut a **610-record worklist**.

**610 screened, coverage exact: 80 RELEVANT, 34 UNCERTAIN, 496 NOT_RELEVANT. 114 go to full text.**

**The chapter's shape is now counted rather than inferred: direct arm 20 records (4 identified),
chain arm 59 (9 identified).** The registered estimand is the minority of its own evidence base and
identification sits in the neighbouring arm — predicted by the scope, confirmed on read records.

Other results:
- **Routing is screenable but not finishable at screen.** `arm: cannot_tell` is 1 of 80; but
  `outcome: multiple` is 22%, against A4's predicted 23% un-routable share.
- **The no-abstract instruction bound, though the headline looks like it did not.** Title-only and
  abstracted records return NOT_RELEVANT at an identical 81% — the exact signature of the failure the
  rubric prevents. It is not that failure: title-only returned RELEVANT at a HIGHER rate (15% vs 12%)
  and `info: insufficient` fired on 80% of them against 2%.
- **Five RELEVANT records carry no student-debt term at all**, including Nau et al. A4 found this for
  two anchors; the screen finds five. The student-anchored exposure axis cannot reach them and they
  arrived through the citation channel and by hand.
- **Bypass yield measured:** `bypass_keyword_frame` delivered 6 sole-RELEVANT, the score cut 1, and
  the other four delivered ZERO unique records despite the highest precision in the run.

### 2026-08-26 — P2 retrieval: A4's reversal is itself reversed

Retrieved the record that A4 said overturned the chapter's central empty-cell finding. It does not.

*Experimental Evidence on ... Family Formation Responses to Student Debt Forgiveness* (SSRN 2022) is
a **hypothetical vignette** — 1,053 participants asked to IMAGINE forgiveness of $5k/$10k/$20k/all
and report intended behaviour — and it is the **working version of the Socius 2023 article** already
screened RELEVANT in batch 1 (same four authors, same N, same four conditions). Its named outcomes
are emergency savings and a housing down payment; neither abstract names a birth.

**The claim, third and current form: no study in the frame estimates the effect of a debt-policy
change on REALIZED fertility.** Tested now on the query channel, the citation channel, and a full
abstract. The record moves P2 → P6.

Three real policy-variation studies DO sit in this frame — the 2020 loan moratorium, Teacher Loan
Forgiveness (RCT), IDR payment burdens — and every one estimates a labour-market or repayment
outcome. The instruments exist and have been used; nobody has pointed them at a birth.

Two things carried forward:
- **D1's duplicate collapse has a hole:** a version pair whose title changed between preprint and
  publication is invisible to a normalized-title match. Belongs in the shared scaffold.
- **Full text is a browser-job**, not a proxy job: WUSTL's repository and SAGE both 403 on
  open-access content (Cloudflare), while the landing page serves the whole abstract. Outstanding
  question for the full text: does the instrument carry a CHILDBEARING item at all?
