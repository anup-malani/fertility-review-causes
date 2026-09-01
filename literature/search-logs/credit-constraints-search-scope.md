# Search scope — credit constraints and liquidity

**Hypothesis:** C.3.e, slug `credit-constraints`, HYPOTHESES-v5.md §C.3.e
**Ticket:** TICK-077 · branch `077-credit-constraints-liquidity`
**Status:** stage 2, drafted 2026-09-01 (Shravan). Walls frozen below; two PI calls open.
Nothing in this document is a measured result — no query has been run, no anchor resolved.

---

## 1. The claim

The registry entry: *imperfect credit markets alter the value of children: in settings without formal
finance, children serve as savings/insurance vehicles (raising their value and fertility); in richer
settings, liquidity constraints on young households delay and reduce childbearing.* Phenomena: PM,
FDT, SDT. Sign: explicitly ambiguous.

The chapter's parameter is the change in fertility caused by an exogenous change in the completeness
of the credit and insurance market facing a household — holding income, prices, and the returns to
children fixed. It is a behavioural parameter, not an identity: every link can be false, so it needs
studies rather than arithmetic.

---

## 2. Ruling 1 — are the two treatments the same? No. But they are not separable either, and that is
why this is one chapter.

The question was put directly, and the project's governing rule answers it: hypotheses are separated
by **what varies**, not by the mechanism an author narrates (C.2.c, 2026-07-31). Applying that rule
to the registry's two configurations:

| | **Arm S — the saving side** | **Arm B — the borrowing side** |
|---|---|---|
| What varies | Availability of a formal instrument for moving resources across time and states of the world | The terms on which a household can borrow against future income |
| Mechanism | Children are a store of value and a risk buffer; a formal substitute displaces them | Young households cannot bring future income forward to fund a birth now |
| Operates on | The **value** of children (an asset motive) | The **intertemporal budget constraint** (an affordability-timing motive) |
| Predicted sign of financial development | Fertility **falls** | Fertility **rises** |
| Setting | Thin or absent formal finance — PM, FDT, LMIC | Developed credit markets — SDT |

**They are different treatments.** They act on different arguments of the household problem: Arm S
changes the return to a child as an asset, Arm B changes when a given child is affordable. A pure
Arm S shock (a crop-insurance rollout) leaves borrowing terms untouched; a pure Arm B shock (a
loan-to-value cap) leaves the asset menu untouched. So the answer to the question as asked is *no*.

**But the exposure sets overlap, and the overlap is not allocable.** Three classes of variation:

1. **Saving-pure** — crop or health insurance rollout, commitment-savings access, deposit-only
   instruments. Moves Arm S alone.
2. **Borrowing-pure** — LTV/DTI caps, loan ceilings, interest-rate shocks, mortgage or consumer
   credit-supply shocks at fixed collateral values. Moves Arm B alone.
3. **Composite** — bank branch expansion, microfinance entry, financial-inclusion reform, "access to
   formal finance." Moves **both at once**, in opposite directions.

Class 3 is not a nuisance stratum. It is very likely where the best-identified designs in this
literature live, because branch-expansion and microfinance-entry studies are the ones with staggered
policy timing and plausible exogeneity. A two-chapter split would have to allocate each class-3
estimate to one arm or the other, and no rule can do that: the estimate **is** the net of a savings
channel pushing fertility down and a borrowing channel pushing it up. Splitting would force every
class-3 study to be reported as evidence for a sign it only partly identifies.

**Two further reasons the split fails.** First, the scientifically interesting question — does
financial development raise or lower fertility, and does the net sign flip with the level of
development — exists only in the joint chapter. Split, each half reports a sign valid only if the
other channel is shut, and neither can answer it. Second, this inverts the A.23 lesson rather than
repeating it: there, the registry named one configuration of a two-configuration variable and
reporting only the named one selected on the sign. Here the registry names **both**. The fix is to
carry both, not to split them.

**Ruling: one chapter, two pre-registered arms, three strata.** With one binding consequence —

> **Arms are never pooled with each other, and never averaged.** They sit in disjoint settings
> (LMIC/historical vs. rich-country), draw on disjoint literatures (development economics vs.
> household finance), and have opposite predicted signs. A pooled estimate across arms is not an
> estimate of anything. **GRADE and demographic significance are rated separately per arm per
> phenomenon**, following the A.18 multi-arm precedent, and the ≥3-effects test for meta-analysis is
> applied **after** stratification, never before.

The composite stratum is reported as the **net** effect and is the primary evidence for the
sign-flip question. It is not evidence for either arm's own sign on its own.

---

## 3. What C.3.e still owns, after four neighbours have taken their share

This chapter is being written late, and four neighbouring chapters have already claimed variation
that a naive reading of "credit constraints" would sweep in. Enumerating the residual **before**
searching, because if it is thin, that is a finding to state early rather than discover at synthesis:

| Taken by | Variation | Left to C.3.e |
|---|---|---|
| C.2.c (housing) | Housing prices and rents, **including home-equity/collateral channels** — price up, collateral up, borrowing capacity up | Credit terms at **fixed** house prices |
| C.3.g (student debt) | The prior education liability already incurred | General consumer, mortgage and medical debt |
| C.3.c (old-age security) | Non-child old-age security, and its entry explicitly names "money in a bank, an insurance policy" | See Wall 1 — this is the contested one |
| A.23 (co-residence) | Living arrangements, whatever drives them | Credit variation where co-residence is a mediator, not the treatment |

The residual is real and is not empty: financial-access and branch-expansion designs, microfinance,
non-old-age insurance, and borrowing-terms policy shocks — including the 2026 *PNAS* housing-provident-fund
cohort-DiD that C.2.c routed here explicitly (down-payment ratios, interest rates and loan ceilings
moved; prices did not). But the residual's size is an **empirical question this scope does not
answer**, and §12 makes measuring it the first job after anchors.

---

## 4. The boundary walls

**Wall 1 — C.3.e vs C.3.c (`old-age-security-pension-crowdout`): which risk is being insured. The
one that could hollow out an arm.**

This is the chapter's hardest wall and it is worse than the C.2.c one, because C.3.c is **already
written** and its §1.1 claims the substitutes explicitly: "a government pension, money in a bank, an
insurance policy." Read literally, C.3.c has already taken Arm S whole.

- **Discriminator: which risk does the instrument insure?**
  - **Longevity / retirement consumption** — pensions, retirement accounts, old-age transfers →
    **C.3.c**.
  - **Contemporaneous income and health risk, and consumption smoothing within working life** — crop
    insurance, health insurance, savings and credit access for shocks → **C.3.e Arm S**.
- A composite financial-access shock that moves both the old-age and the within-life margins is
  `MIXED_OLDAGE_LIQUIDITY`, reported to both chapters as unallocated, exactly as C.2.c handled
  `MIXED_PRICE_CREDIT`.
- **Risk this wall creates, stated now:** if the literature's asset-motive studies are overwhelmingly
  old-age framed, Arm S empties and this becomes a one-arm liquidity chapter. That is a legitimate
  outcome but must be *measured*, not assumed either way — see PI Call 1 and the §12 probe.

**Wall 2 — C.3.e vs C.2.c (`housing-costs`): source of exogenous variation. Inherited, already
demonstrated to fail without it.**

Frozen by C.2.c on 2026-07-31 and adopted here unchanged:

- Variation in **housing prices or rents** → C.2.c, whatever channel the authors invoke. This
  includes the home-equity/collateral studies: their identifying variation is a price shock.
- Variation in **credit terms holding housing prices fixed** — mortgage credit supply, LTV/DTI caps,
  interest-rate shocks, deposit requirements, loan ceilings → **C.3.e**.
- Inseparable joint price-and-credit shocks are `MIXED_PRICE_CREDIT`, reported to both.

**Wall 3 — C.3.e vs C.3.g (`student-debt-household-formation`): a stock already incurred vs. the
terms available now.** A prior education liability is C.3.g's. General consumer, mortgage and
medical debt is C.3.e's. Frozen by C.3.g; adopted.

**Wall 4 — C.3.e vs C.1.a (`income-effect`): a transfer is not a loan.** Credit relaxation that
raises **lifetime resources** (a grant, a forgiven debt, a cash transfer) is C.1.a's. Credit
relaxation that changes **only the timing** at which given resources are available is C.3.e's. The
hard cases are subsidised loans and microfinance, which do both; tag them `MIXED_INCOME_LIQUIDITY`
and require the study to report whether the interest subsidy was priced.

**Wall 5 — C.3.e vs C.5.a (`economic-uncertainty`): the constraint vs. the risk.** A binding
borrowing limit at known income is C.3.e's. Unchanged borrowing terms with more **variance** in
expected income is C.5.a's. Insurance sits on this line and is routed by what the design moves: if
it moves the *availability of a buffer*, C.3.e Arm S; if it moves *perceived risk* at a fixed
buffer, C.5.a.

**Wall 6 — the outcome wall.** The outcome must be **fertility**: births, parity progression,
completed fertility, or stated intentions (recorded separately). Effects of credit on marriage,
homeownership or household formation with **no fertility outcome** are mechanism evidence only. This
wall is written explicitly because it is where C.3.g's evidence base failed: its identified body sat
on marriage and homeownership, not births. The same failure is likely here, and the screen must
record the outcome variable, not the narrated topic.

---

## 5. Estimand cells

| Cell | Treatment / variation | Arm | Routing |
|---|---|---|---|
| `PRIMARY_SAVE_INSURE` | Saving or insurance instrument availability, non-old-age risk, at fixed borrowing terms | S | Primary — Arm S pool |
| `PRIMARY_BORROW_TERMS` | Borrowing terms at fixed prices and asset menu — LTV/DTI, loan ceilings, rate shocks, credit supply | B | Primary — Arm B pool |
| `PRIMARY_COMPOSITE_ACCESS` | Financial access moving saving and borrowing together — branch expansion, microfinance, inclusion reform | Net | Primary — composite pool, reported as net; the sign-flip evidence |
| `MIXED_OLDAGE_LIQUIDITY` | Moves old-age security and within-life liquidity inseparably | — | Unallocated; reported to C.3.c too |
| `MIXED_PRICE_CREDIT` | Price and credit variation inseparable | — | Unallocated; inherited from C.2.c |
| `MIXED_INCOME_LIQUIDITY` | Changes lifetime resources and timing inseparably | — | Unallocated; reported to C.1.a too |
| `CROSS_SECTION_ONLY` | Constrained-vs-unconstrained comparison with no exogenous variation | — | Recorded, never pooled — see §7 threat 1 |
| `MECHANISM_NO_FERTILITY` | Credit → marriage, homeownership, household formation; no fertility outcome | — | Mechanism/context; Wall 6 |
| `THEORY` | Models of fertility under incomplete markets, no empirical estimate | — | Theory stream |
| `OFF_HOUSING_C2c` | Housing price or rent variation | — | Route to C.2.c |
| `OFF_OLDAGE_C3c` | Old-age security variation | — | Route to C.3.c |
| `OFF_DEBT_C3g` | Student-debt burden | — | Route to C.3.g |
| `OFF_INCOME_C1a` | Pure resource transfer | — | Route to C.1.a |
| `OFF_UNCERTAINTY_C5a` | Income risk at fixed credit terms | — | Route to C.5.a |
| `OFF_OTHER` | Non-C.3.e determinant, no sibling home | — | Route out |
| `INSUFFICIENT_INFO` | Not routable on the visible record | — | Pairs only with `UNCERTAIN` |

---

## 6. Required tags on every included effect

- `ARM` — S / B / composite. **Assigned from the source of variation, never from the narrated
  mechanism.**
- `INSTRUMENT_TYPE` — insurance / savings / borrowing terms / credit supply / composite access.
- `RISK_INSURED` — longevity / income / health / none. Drives Wall 1 and must be recorded even when
  the routing looks obvious.
- `CONSTRAINT_MEASURED` — how the study establishes a constraint *binds*: a policy discontinuity, a
  denial threshold, a self-reported constraint, or assumed. **"Assumed" is not identification**; see
  §7.
- `SETTING_FINANCE_DEPTH` — private credit / GDP or an equivalent, at the study's time and place.
  Required on every effect: it is the moderator the sign-flip question is asked against, and without
  it a composite estimate is not interpretable.
- `TEMPO_OR_QUANTUM` — timing of births vs. completed fertility. Arm B's prediction is largely a
  *timing* prediction, so an Arm B chapter that reports only period effects will overstate its
  quantum significance. Cross-ref A.11; precedent TICK-038.
- `PARITY`, `OUTCOME_LEVEL` (realized births / completed fertility / stated intention),
  `SOURCE_OF_VARIATION`, `ESTIMATOR_CLASS`.
- `ESTIMATOR_CLASS` takes a closed list and **an unlisted correction must fail loudly, not fall
  through to `uncorrected`** — the fall-through pools things that must be kept apart.

---

## 7. Identification threats the risk-of-bias pass is looking for

1. **Constrained status is chosen.** Households that report being credit-constrained differ in
   income, risk and planned fertility. A cross-sectional constrained-vs-unconstrained fertility gap
   identifies nothing; `CROSS_SECTION_ONLY` exists to keep these visible and unpooled.
2. **Reverse causality, and it is strong here.** Planning a birth changes borrowing and saving
   behaviour *before* the birth. A correlation between a mortgage draw-down and a subsequent birth is
   as easily the birth causing the loan.
3. **The composite channel confound is the estimand, not a bias.** In `PRIMARY_COMPOSITE_ACCESS` the
   two channels' netting is what is being measured. Do not "adjust" for it, and do not report a
   composite estimate as evidence for a single arm's sign.
4. **Credit shocks travel with income shocks.** Branch expansions and credit booms raise local income
   and employment. Wall 4 routes the estimand; risk-of-bias asks whether the design actually holds
   income fixed.
5. **Design is not a property of the title** — the screen's `design` values are hypotheses to be
   confirmed at full text. A.23 carried a paper as an administrative allocation through three stages
   and it was IPTW.

---

## 8. Demographic significance, pre-specified

Per `PROTOCOL.md` §4.2.1 and `docs/chapter-template.md`: the denominator is a **change** in the
phenomenon over the phenomenon's **full window**, never a level and never the study window; numerator,
denominator, source and window are named at the point each share is given; a share above 100%
diagnoses a wrong denominator.

Pre-specified per arm and phenomenon, with the sign each would carry:

- **Arm S, PM and FDT.** Numerator: the fertility change implied by the observed spread of formal
  saving/insurance instruments over the window, at the pooled Arm S elasticity. The binding problem
  is expected to be the **exposure series**, not the elasticity — historical financial-access
  coverage for FDT populations may simply not exist. If it does not, report the **break-even**: the
  largest phenomenon for which the magnitude still clears a given band.
- **Arm B, SDT.** Numerator: the fertility change implied by the observed tightening or loosening of
  borrowing terms for childbearing-age households. **Must be net of tempo** — if the effect is
  postponement, the completed-fertility share is far smaller than the period share, and the verdict
  turns on this.
- **Composite, all phenomena.** Reported as the net, and only where `SETTING_FINANCE_DEPTH` is
  recorded.
- **Endogeneity check, before any share is claimed:** is the credit-market change itself *caused by*
  the fertility decline? An ageing, low-fertility population has different savings supply and
  different credit conditions. A feedback of the decline cannot be evidence for the decline's cause,
  and that component nets out first.
- Where a cell is in scope and empty, the verdict is **NOT ASSESSED** with the sign it would carry —
  **never NEGLIGIBLE**, which asserts a computed share under 5%. Empty cells pair with **No
  evidence** in GRADE, not VERY LOW.

---

## 9. Pooling rule (pre-registered)

Stratify first, then count. The ≥3-extractable-effects test for meta-analysis applies **within** a
stratum defined by (`ARM` × `OUTCOME_LEVEL` × `ESTIMATOR_CLASS` compatible), never across arms. A
hazard ratio beside a mean is not a pool. Sign convention: all effects oriented so that **positive =
more fertility after a relaxation of the constraint**, which means Arm S's predicted sign is negative
and Arm B's is positive, and the orientation is recorded per effect rather than inferred.

---

## 10. Where admissible variation could come from — enumerated before searching

Written now so that a null is interpretable later: if the search returns none of these, that is a
finding about the literature; if it returns none of these *and* the enumeration was wrong, it is a
finding about the query.

- Staggered bank-branch or financial-inclusion policy rollouts (composite).
- Microfinance entry and randomised microcredit expansions (composite, some RCT).
- Randomised or quasi-random insurance rollouts — crop, health — with fertility follow-up (Arm S).
- Regulatory borrowing-limit changes: LTV/DTI caps, provident-fund and down-payment rules, loan
  ceilings (Arm B; the routed *PNAS* study sits here).
- Credit-supply shocks: branch deregulation, bank-lending shocks, credit-score discontinuities
  (Arm B).
- Interest-rate or credit-cycle variation interacted with pre-determined household exposure (Arm B).
- Historical: savings-bank and rural-credit-institution founding dates against parish or county
  fertility (Arm S, FDT — the thinnest and most valuable cell if it exists).

---

## 11. Rulings

**Ruling 1 — one chapter, two arms, three strata.** Resolved above (Shravan, 2026-09-01), on the
question put by Anup: the treatments are *not* the same, but their exposure sets overlap in a class
that cannot be allocated, so they cannot be two chapters. Arms are never pooled or averaged; GRADE
and demsig are per arm per phenomenon.

**Ruling 2 — the Lovenheim and Mumford double-listing, now acted on.** C.2.c recommended striking
Lovenheim and Mumford 2013 from C.3.e's `seminal` list and cross-referencing C.2.c instead, and
flagged rather than made the edit because HYPOTHESES-v5.md is under PI review at TICK-001. Authorised
by Anup 2026-09-01; the edit is made on this branch and annotated in place so the PI sees an RA edit
rather than a silent one. The substance: the home-equity channel's identifying variation is a housing
**price** shock, so under Wall 2 the study is C.2.c's.

### PI Call 1 — does C.3.c leave Arm S anything?

C.3.c's written chapter names "money in a bank, an insurance policy" among its substitutes. Wall 1
splits on *which risk is insured* — longevity to C.3.c, within-life risk to C.3.e — but the split is
mine, not the registry's, and it is the difference between a two-arm chapter and a one-arm one. The
alternative ruling is that Arm S **is** C.3.c and should be routed away whole, leaving C.3.e as a
pure liquidity chapter and making the registry's PM/FDT phenomena out of scope. Proceeding under my
split; the §12 probe measures which ruling the literature actually supports before extraction.

### PI Call 2 — inherited and still unanswered from A.24

A.24 left open whether two chapters may both report the same study when a `MIXED_*` class is reported
to both, or whether one must cite the other. This chapter creates three such classes and so cannot
avoid the question. Recommend: both report, both flag as unallocated, and the synthesis nets them
once — but this is a protocol-level call, not a chapter-level one.

---

## 12. Next steps, in order

1. **Cold-start anchors.** Hand-source them; Tier-A anchors are studies and must not be replaced by
   screen output. Score recall **per arm** — a sub-literature that renames the outcome will otherwise
   read as an absence (A.18 lost 7 of 9 SELECTION anchors to "fitness").
2. **The Arm S survival probe, before any production query.** Measure how many asset-motive studies
   are old-age framed. This decides PI Call 1 and is cheap.
3. **Vocabulary, kept in two lists.** The diagnostic list that scores contamination and the retrieval
   list that finds the canon are different lists; every tightening is recall-checked.
4. Anticipated homonyms to measure rather than assume: "fertility" (soil, sperm), "credit"
   (course credit, tax credit — **"child tax credit" is C.2.d and will be dense**), "liquidity"
   (market microstructure).
5. Production query, leave-one-out on each axis, then the screen.
