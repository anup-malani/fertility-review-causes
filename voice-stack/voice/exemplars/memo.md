---
name: Memo-voice exemplar bank — POLICY-MEMO register (Anup Malani)
register: CMS policy-memo prose — direct, assertive, decision-oriented. Leads with the finding or recommendation before background; states a crisp problem; lays out options and weighs tradeoffs; marshals evidence for one claim at a time; closes by bounding what can be done and naming the next step. Reasons like an economist (incidence, incentives, selection, marginal return, counterfactual) rather than in political categories.
purpose: Curated paragraphs of Anup Malani's own CMS policy-memo prose in his MOST AUTHENTIC (least AI-influenced) voice, for live injection into an LLM's context as models to imitate when drafting in his memo register.
scope: Internal CMS policy memos, briefings, and reports (Dec 2025–2026), addressed to the Administrator, center directors, NEC staff, and internal readers. Own-authored, hand-written-from-scratch finals preferred; hand-edited (-am/-AM) finals second.
sources: Combined memo corpus at assistants/research-manager/projects/style-analysis/corpus/memo/ (50 memos, manifest.csv) + work-laptop package (_worklaptop/, MANIFEST.md, EXCLUDED.md).
date: 2026-07-26
selection_basis: Weighted toward the EARLIEST, hand-written-from-scratch memos (Dec 2025–Feb 2026), which predate his adoption of AI drafting, and toward the paragraphs closest to his academic register. This deliberately DOES NOT optimize for "passes the ai-tells screen." See "What changed" below.
supersedes: memo-v1-recent-corpus.md (the prior bank, which over-selected clean late-2026 paragraphs and was partly AI-contaminated).
structure: CORE (5, one per archetype — default injection) + EXTENDED (10 additional keepers).
---

# Memo Voice — CMS Policy-Memo Register (Anup Malani)

**This file replaces a contaminated predecessor.** The prior bank (`memo-v1-recent-corpus.md`) was
built by preferring clean, em-dash-free, tell-free paragraphs. But Anup adopted AI drafting only
*later* in his CMS work, so his most recent memos are partly AI-written. Optimizing for "clean and
tell-free" therefore selected the *most AI-like* paragraphs, not the ones most in his own voice.
This rebuild corrects that: it selects for authentic voice even when it is less polished, weighting
toward (1) the earliest, hand-written memos and (2) the paragraphs closest to his academic register.

Paragraphs below are quoted **verbatim** from Anup Malani's own CMS policy memos (combined corpus at
`assistants/research-manager/projects/style-analysis/corpus/memo/`, `manifest.csv`). Each teaches a
distinct memo move. **CORE** is the default injection set, one paragraph per archetype. **EXTENDED**
holds additional non-redundant keepers.

**Transcription conventions.** Footnote-reference markers are dropped (`[^1]`, `[4]`, `[1,2]`, and the
like). Markdown backslash-escapes from the `.docx`→`.md` conversion are removed (`CMS\'s` → `CMS's`,
`\$2 trillion` → `$2 trillion`). Markdown-escaped em-dashes (`\-\-\-`, `---`) are rendered as the true
em-dash `—`. His own genuine typos and slips (`counterfactural`, `MEMORANDOM`, `tend to ones`, `risk
or being struck`) are kept **verbatim** as authenticity signals and flagged inline — they are his hand,
not a model to imitate. No other change.

**Register note (READ THIS — this bank was rebuilt to correct a false "restraint" signal).** The
prior bank claimed his memo voice carries "zero em-dashes and zero rhetorical questions," and treated
that as a fact about his voice. It was not. It was an artifact of selecting AI-clean paragraphs. His
authentic hand-written memos **do** use the em-dash, almost always as an **appositive or definitional
pair** ("the individual market — where the MOOP actually matters — is a small fraction…"), at roughly
his academic-register rate. Per the flag-not-exclude rule inherited from the law and econ banks
(`academic-law.md`, `academic-econ.md`), authentic appositive em-dashes are **kept and flagged, not
dropped**. CORE 1, 3, 5 and EXT 7, 10, 12 contain them; each is flagged. The memo register is still
the direct, decision-first, lead-with-the-verdict register; it is simply not the em-dash-free register
the prior bank invented. If a dash is doing dramatic-pause work (not appositive), still recast it.

---

## Prioritization note — sources, dates, and what was skipped

**Recovered chronology.** The combined corpus runs from **December 1–2, 2025** (internal dates on the
two earliest memos; `2025-12-05` in the manifest) through **July 22, 2026**. Nothing earlier than
December 2025 survived into the corpus. The AI-drafting era begins to dominate around **June–July
2026**, where the prior bank drew nearly all its CORE picks.

**The "fall report."** Anup recalled a report he wrote "in the fall" that models his unassisted voice.
The best match is **`tech-healthcare-data-liquidity-v1`**, internally dated **"Version: December 2,
2025"** — the single earliest document in the corpus, and a market-structure *report* (Part I / Part II,
no To/From block) rather than a memo. It is unmistakably hand-written and pre-AI: first-person "By
history, I mean… By counterfactual, I mean…", a coined four-part market-development framework, stub
outline sections, and authentic typos (`counterfactural`, `HER` for EHR, "data or and the grey").
Its internal date is early December (late fall), and the drafting likely began earlier; it is treated
here as the prime unassisted-voice source and supplies CORE 5 and EXT 11.

**Authenticity ranking used.** (1) Hand-written-from-scratch, earliest (Dec 2025–Feb 2026) — strongest
signal. Six such memos anchor this bank: `tech-healthcare-data-liquidity-v1` (Dec 2), `cciio-aca-
problems-and-reforms-251211` (Dec 1), `cciio-moop-av-conflict-solutions` (Jan 31), `oa-hassett-nec-
meeting-briefing-v4` (Feb 5), `cmcs-sdoh-evidence-assessment-v9` (Feb 25). (2) Hand-edited `-am`/`-AM`
finals, even when late — his hand is on them; `oa-value-of-medical-innovation-v7-am` (Jul 13, on his
own research) is the one late memo authentic enough to quote. **Caveat learned in this rebuild:** a late
`-am` is *not* automatically authentic. `oa-ma-payment-differential-v2-am` (Feb 7, `-am`) reads *more*
AI than the December hand-written memos — bolded-fragment topic labels, em-dashes as dramatic pauses.
The `-am` suffix can mean "hand-edited an AI draft." Hand-written-from-scratch beats a late `-am`.

**Skipped for sensitivity or authorship (read, not quoted).** The work-laptop `EXCLUDED.md` held back
four files needing a human decision (a coverage handoff with live staff emails, an undocumented-enrollee
estimate, a contractor source-selection evaluation, an HCBS briefing naming private individuals); none
was resurrected. Beyond that: the Hassett briefing's Medicare-Advantage "apparent deal" section (line
65–77) speculates about a pre-decisional internal CMS/UnitedHealthcare trade and is **not quoted**; the
personal-care-fraud options section (named states and an intermediary) is **not quoted**; the
`cm-ffs-bimodal-health-om-v1-am` memo body is a Claude draft carrying visible `[CLAUDE:]`/`[ANUP:]`
editing dialogue (Anup even instructs it to "use strong topic sentences") — its body is machine prose
and is **not quoted**, though the `[ANUP:]` interjections corroborate his reasoning voice. The
`cciio-open-enrollment-2026-decline-v11-am-pn` memo is co-authored with Peter Nelson (first author) and
is a technical projection product; **not quoted**. Everything quoted below is analytical/argumentative
and free of PII/PHI and beneficiary-level data.

**Through-line (one line):** an economist writing to decision-makers, who states the verdict or the
governing constraint early, reduces a messy policy question to a few economic variables or an
efficacy-ranked set of options, walks one clean mechanism or worked example for one claim at a time,
and closes by bounding what the agency can do on its own authority (versus what needs Congress) and
naming the venue — in plain declaratives, with the occasional appositive em-dash and the occasional
honest typo.

---

## CORE

### 1. Recommendation-first opener — answer the ask, verdict then caveat
**Source:** `cmcs-sdoh-evidence-assessment-v9`, Executive Summary (Center for Medicaid & CHIP Services / SDOH; **Feb 25, 2026, hand-written-from-scratch**, to Administrator Oz). Authentic: early, first-person briefing register, direct verdict.

> You asked me to examine the value of SDOH (social determinants of health) interventions like medically tailored meals. Only three SDOH interventions — medically tailored meals, case management, and modernized non-emergency medical transportation (NEMT) — show credible evidence of cost-neutrality, and even their evidence is contested by recent randomized controlled trials (RCTs). Fraud risk in community-delivered services is substantial and growing. I recommend selective pilots with strict evaluation and program integrity controls, not broad expansion, consistent with CMS's March 2025 rescission of the prior HRSN framework.

*Move:* his real briefing habit — name the commission ("You asked me…"), state the finding in one
sentence, then give the recommendation, all in the first person. The verdict and its qualification
("even their evidence is contested") arrive together. **Flag (authentic, kept):** one appositive
em-dash pair around the three-item list; "not broad expansion" is a full contrastive clause carrying
the recommendation (the permitted form, ai-tells §1), not a slogan.

---

### 2. Problem statement — the crisp two-part partition
**Source:** `cciio-aca-problems-and-reforms-251211`, opening (CCIIO ACA reform; **internally dated December 1, 2025 — the earliest memo in the corpus, hand-written, "AM to PN"**). Authentic: earliest date, pre-AI, his signature two-effect partition.

> The ACA was intended to expand insurance coverage and lower insurance premiums (especially for high-risk individuals) in the individual insurance market. Its provisions, however, had two counterproductive effects. One is adverse selection, which lowered coverage of low-risk populations. The other is higher insurance costs. Moreover, COVID-era emergency premium subsidies expire in plan year (PY) 2026, which increases in out-of-pocket premiums.

*Move:* states the goal, then partitions the failure into exactly two named effects ("One is… The
other is…") before any analysis. The purest early specimen of his problem-statement opener. **Flag
(authentic, kept):** the closing sentence has a grammatical slip ("which increases in out-of-pocket
premiums" — his hand, not to imitate), and "Moreover," is a soft connective (ai-tells §8) that here
introduces a real added fact (the subsidy cliff). Both preserved as pre-AI authenticity signals.

---

### 3. Options / tradeoff analysis — the two-by-two, then the sequenced synthesis
**Source:** `cciio-moop-av-conflict-solutions`, Executive Summary (CCIIO MOOP; **Jan 31, 2026, hand-written**, "MEMORANDOM"/"staturoty" typos in source). Authentic: early, and this is the exact paragraph the prior bank **dropped for its em-dash**.

> Neither mechanism alone is sufficient. MOOP flexibility without a corrected PAP leaves the agency permanently waiving a statutory provision. A corrected PAP without MOOP flexibility solves the problem prospectively but does nothing about the existing gap; it arrests the problems of Bronze plans becoming more infeasible but does not repopulate the Bronze tier. The recommended approach sequences both: adopt MOOP flexibility now as a transitional bridge, correct the PAP methodology through the next Payment Notice cycle, and phase out the transitional provision as the corrected MOOP closes the gap. This sequencing is also the strongest legal posture — each mechanism covers the other's weakness.

*Move:* the two-by-two done in prose — each option carried with its own weakness ("solves X but does
nothing about Y"), then synthesized into a sequence where each covers the other's gap. **This is the
flagship correction of this rebuild:** the prior bank recorded that it "dropped" this MOOP two-by-two
"in favor of clean alternatives, per the strict-register rule," because it used a dash. That was the
contamination in miniature. It is restored to CORE for its **structure** (the two-by-two done in
prose, each option carried with its own weakness, then the sequenced synthesis), **not its dash
rate.** **Flag (authentic, kept, density NOT to be emulated):** one appositive em-dash on the final
clause. In ~130 words that is ≈8 per 1,000 at the paragraph level, which reads dash-dense in
isolation. The memo drafting target is ~1 per 1,000 words (voice-registry); the corpus rate is
AI-inflated and not his verified hand (pending the memo-dating run). The appositive dash is authentic
and fine at the target rate; this paragraph's per-paragraph density is not the model.

---

### 4. Evidence for a claim — the payment mechanism, magnitude at the close
**Source:** `oa-hassett-nec-meeting-briefing-v4`, §C (Office of the Administrator, briefing for the NEC Director meeting; **Feb 5, 2026, hand-written**, to Administrator Oz). Authentic: early, clean, reasons purely from incentives. **No em-dash.**

> The premium tax credit equals the gap between a household's expected contribution and the second-lowest silver plan premium in its rating area. In concentrated insurance markets, a single insurer can often determine the federal subsidy for every enrollee in that market. The benchmark insurer faces a perverse incentive: raising its premium does not cost it subsidized enrollees, because the subsidy rises dollar for dollar. Other insurers can price above the benchmark without penalty. This mechanism has inflated ACA premiums by roughly 25 percent.

*Move:* argues the claim entirely from a payment structure — how the benchmark is set, why the
benchmark insurer faces a perverse incentive, why rivals free-ride on it — and only then states the
magnitude ("roughly 25 percent"). The clearest early "reasons like an economist" specimen: mechanism
first, number last, no statistic doing the arguing on its own.

---

### 5. Bounded close — define the terms, name the counterfactual test
**Source:** `tech-healthcare-data-liquidity-v1` (**"the fall report," internally dated December 2, 2025** — earliest document in the corpus; a market-structure report), framework close. Authentic: earliest, hand-written, pure academic-econ voice, first-person definitional move.

> Finally, when developing the healthcare data market, it is important to understand history and the counterfactual. By history, I mean that there is an existing market and the government is not writing on a blank slate. It must account for existing structures and practices, otherwise it will not be able to attract participants to the market it develops. By counterfactural, I mean understand what would happen in the absence of government efforts to forge a market. Private parties will develop a private market without further government involvement. The value of government policy should be judged by whether it yields an outcome better than purely private development of a market.

*Move:* his academic register applied to a policy report — coin-and-define the two terms he needs
("By history, I mean… By counterfactual, I mean…"), then bound the whole exercise with a
counterfactual test: government action is worth doing only if it beats the private-development
counterfactual. This is his authentic version of the bounded close (what is worth doing, and against
what benchmark). **Flag (authentic, kept):** "counterfactural" is his typo, kept verbatim; "Finally,"
+ "it is important to understand" are soft throat-clears (ai-tells §8, §14) preserved as pre-AI hand
signals, not constructions to imitate. The definitional move and the counterfactual test are the model.

---

## EXTENDED

### 6. Evidence — the worked economic example with a number
**Source:** `cciio-aca-problems-and-reforms-251211` (CCIIO ACA reform; **Dec 1, 2025, earliest memo**). Authentic: earliest, hand-written, a numerical mechanism worked in prose.

> A problem with 3x or 3-1 community rating is that it makes insurance pools unstable. Community rating forces young enrollees to bear some of the costs of older enrollees. For example, if an older enrollee costs 5x of what a younger one does, but the plan cannot charge the older one more than 3x the younger one, then the plan must charge the younger enrollee more than her actual costs to break even. This extra charge functions as a cross-subsidy from young enrollees to old ones, lowering the premium the older ones must pay. The problem is that many younger individuals are not willing to pay more than they cost, so they dis-enroll, unraveling the benefit of community rating. If individuals who cost less than 1/3 of older enrollees exit, their cross-subsidy vanishes, and premiums for older individuals rise.

*Move:* walks a mechanism to instability with a single concrete number (5x cost, 3x cap), naming the
cross-subsidy and following the young enrollee's exit decision to the unraveling. The academic-econ
move ported straight into a policy memo; the closest memo cousin of the community-rating reasoning in
his law and econ banks.

---

### 7. Evidence — re-describe a policy as an economic object
**Source:** `oa-hassett-nec-meeting-briefing-v4`, "What the Uninsured Actually Pay" (OA briefing; **Feb 5, 2026, hand-written**). Authentic: early, an economist's reframe of a statute.

> EMTALA (1986) required Medicare-participating hospitals to stabilize and treat emergency patients regardless of ability to pay. Its underappreciated effect was to force hospitals to extend credit: deliver care first, bill later. The implicit loan carries a zero interest rate for borrowers no private lender would touch. Consumer bankruptcy law makes the terms more generous still — a patient who cannot pay can file for Chapter 7 and discharge the debt. Because both sides know this, hospitals typically negotiate bills down to a fraction of the sticker price. A bankruptcy filing occurs only the rare cases when negotiation fails.

*Move:* takes a familiar statute and re-describes it as an economic object — EMTALA plus bankruptcy law
is an implicit zero-interest loan to the uninsured — then follows the equilibrium (both sides know it,
so bills get negotiated down). **Flag (authentic, kept):** one appositive em-dash; "occurs only the
rare cases" drops an "in" (his typo, kept).

---

### 8. Evidence — debunk a claim with a homemade analogy
**Source:** `oa-hassett-nec-meeting-briefing-v4`, §A (OA briefing; **Feb 5, 2026, hand-written**). Authentic: early, the dinner-table analogy is a signature move. Clean.

> The popular narrative traces to Elizabeth Warren's studies, which surveyed people who had already filed for bankruptcy and classified anyone with medical bills or health-related financial stress as a "medical bankruptcy." More than half of filers qualified. But this confuses correlation with causation. Bankrupt individuals carry many kinds of debt; that a filer also has medical bills does not mean those bills caused the filing, any more than owning a car causes bankruptcy. Total debt load, not any particular category, is the best predictor.

*Move:* names the inference error (correlation for causation), then defeats it with a homemade analogy
anyone can run ("any more than owning a car causes bankruptcy"). "Total debt load, not any particular
category, is the best predictor" is a full contrastive clause carrying the real finding, the permitted
form (ai-tells §1).

---

### 9. Options framing — rank solutions by efficacy, trade against political feasibility
**Source:** `cciio-aca-problems-and-reforms-251211` (CCIIO ACA reform; **Dec 1, 2025, earliest memo**). Authentic: earliest, his standing method for organizing options.

> This memo reviews the ACA and the problems it has created, and suggests solutions to each problem, organized by the efficacy of those solutions. The most efficient solution is often the least politically feasible. Second- and third-best solutions tend to ones that account for political feasibility.

*Move:* states his organizing principle for an options memo up front — rank by economic efficacy, then
note that efficacy and political feasibility usually trade off, so the second- and third-best options
buy feasibility at a known efficiency cost. The scaffold he hangs most reform memos on. **Flag
(authentic, kept):** "tend to ones" drops "to be" (his slip, kept).

---

### 10. Evidence — diagnose the mispricing, then locate the cause
**Source:** `cciio-moop-av-conflict-solutions`, "Policy logic" of the corrected-PAP option (CCIIO MOOP; **Jan 31, 2026, hand-written**). Authentic: early, an economic diagnosis of a formula.

> The MOOP-AV tension exists because the PAP has systematically understated premium growth in the market where the MOOP binds. The all-market average is dominated by employer-sponsored insurance, which covers roughly 155 million people with younger, healthier risk pools and slower claims growth. The individual market — where the MOOP actually matters — is a small fraction of the denominator. Correcting the estimation methodology to reflect individual-market costs is not a workaround; it is a more faithful implementation of the statute's indexing design. Congress intended the MOOP to grow with health insurance costs. It has not, because the Secretary's estimate has tracked the wrong market.

*Move:* diagnoses why a formula misfires — the index is dominated by the wrong (employer) market, so it
understates growth where the cap actually binds — and closes on the crisp cause ("the Secretary's
estimate has tracked the wrong market"). **Flag (authentic, kept):** one appositive em-dash; "is not a
workaround; it is…" is a full contrastive clause (permitted).

---

### 11. Reframe — translate a market feature into economic categories
**Source:** `tech-healthcare-data-liquidity-v1` (**the fall report, Dec 2, 2025**), market-structure section. Authentic: earliest, pure academic-econ reasoning in a report.

> Third, while non-PII data is substitutable, PII data is largely non-substitutable. This means that PII data owners start with market power, and can command high prices. The non-PII market has lower prices. This does not imply, however, that the non-PII market is unimportant. Because of HIPAA, new companies and new products without pre-existing relationships to a large number of patients are blocked from the PII market. Moreover, the quantity in the non-PII market is so large that the revenue (price times quantity) in the non-PII market may be as large as that in the PII market which has higher (potential) prices, but lower volume.

*Move:* maps an institutional feature (substitutability) onto an economic category (market power →
pricing power), then refuses the easy inference (low price ≠ unimportant) by reasoning about revenue as
price times quantity. Reasons like an economist about a market he is describing, not just prescribing
for. "Moreover" here is a real enumeration beat (ai-tells §8 carve-out).

---

### 12. Reframe — the N-part mechanism, stated as "it does <N> things"
**Source:** `oa-value-of-medical-innovation-v7-am`, Executive Summary (OA medical innovation; **Jul 13, 2026, `-am` hand-edit, on his own research** with Lakdawalla and Reif). Authentic despite the late date: hand-edited and drawn from his own published work.

> New medical treatments give insurance its value, and over time they also substitute for insurance. When a disease lacks any treatment, no amount of insurance helps patients soften its impact. But after a new treatment emerges, it does two things. First, it converts a physical risk, the risk of illness or death, into a financial risk — a bill — that insurance can help you finance. Second, because a treatment usually sells for less than the cost of the illness it addresses, it shrinks the patient's risk directly, lowering the amount of insurance required to buffer it.

*Move:* the "it does two things. First… Second…" partition applied to a mechanism, converting an
abstract claim (innovation is worth more than insurance) into two concrete channels. Included to show
that his authentic voice persists into the AI era when he is writing about his own ideas and hand-edits
the draft. **Flag:** late date (Jul 2026), so weighted below the Dec–Feb sources; one appositive
em-dash pair ("— a bill —"), authentic and kept.

---

### 13. Evidence — weigh a body of work by design quality
**Source:** `cmcs-sdoh-evidence-assessment-v9`, §1 (CMCS / SDOH; **Feb 25, 2026, hand-written**). Authentic: early; the one strong pick retained from the prior bank. Clean.

> The single large RCT of medically tailored meals found no benefit on rehospitalization or ED visits, casting serious doubt on these observational results. This pragmatic trial (n=1,977) across five Kaiser Permanente hospitals found no reduction in all-cause 90-day rehospitalization (aHR: 1.02, 95% CI: 0.86-1.21) and no benefit from adding nutritional counseling; the trial did find lower mortality and fewer heart failure-specific hospitalizations, but the primary endpoints were null. This divergence is the central evidence problem in the SDOH space: observational studies cannot rule out selection effects, because MTM participants are clinically triaged and more engaged in care. The American Heart Association's 2023 Presidential Advisory acknowledges that "relatively few studies have been conducted with designs that provide strong evidence."

*Move:* weighs the evidence by design — one RCT against a body of observational work — and names the
exact confound (selection: triaged, more-engaged participants) that reconciles the divergence.
Evidence handled with a researcher's skepticism, put in service of a decision.

---

### 14. Bounded close — what regulation can do, what needs Congress, and the venue
**Source:** `oa-hassett-nec-meeting-briefing-v4`, §C close (OA briefing; **Feb 5, 2026, hand-written**). Authentic: early, the agency-vs-Congress boundary drawn plainly. Clean.

> Peter is addressing this through the payment notice, which can adjust AV calculations and provide temporary relief. The permanent fix requires Congress to amend the indexing formula. This is worth flagging for Hassett: the NEC can champion a technical correction with bipartisan appeal. No one benefits from a market that mechanically sheds its healthiest enrollees.

*Move:* the honest, bounded close in miniature — regulation buys temporary relief, the permanent fix
sits with Congress, and the venue for that fix is named (the NEC). The early hand-written cousin of
the archetype the prior bank could only fill from a late-July memo.

---

### 15. Bounded close — recommend, but qualify the recommendation against a side effect
**Source:** `oa-value-of-medical-innovation-v7-am`, §III (OA medical innovation; **Jul 13, 2026, `-am` hand-edit, own research**). Authentic-late; hand-edited.

> Second, price negotiation should be careful not to cut R&D. Most of health care's value comes from the research behind new treatments, not from the financing of care. Spending on that research is itself a kind of insurance premium that society pays to protect against future illness, one that pays off only when the research yields a new treatment. A price cut that is too aggressive saves money now but risks discouraging the next treatment that sustains the value of insurance.

*Move:* makes the recommendation (don't cut R&D through price negotiation) and in the same breath
grounds it in a mechanism (R&D as society's insurance premium) and qualifies it against the side
effect (short-run saving, long-run loss of innovation). The instinct to qualify his own recommendation
in the next sentence is a defining feature of the register. "not from the financing of care" is a full
contrastive clause (permitted). **Flag:** late date, weighted below the Dec–Feb sources.

---

## What changed from the prior bank (memo-v1-recent-corpus.md)

**Direction of the shift: hard toward the earliest, hand-written memos.**

- **Old CORE dates:** all five from **late-June/July 2026** (`fraud-hcfac` Jun 29, `oa-accessibility`
  Jul 6, `tech-awv` Jun 16, `cciio-py2026-rate` Jul 1, `oce-residency` Jul 7) — the window where AI
  drafting dominates.
- **New CORE dates:** **Dec 2, 2025; Dec 1, 2025; Jan 31, 2026; Feb 5, 2026; Feb 25, 2026** — four of
  five from before March 2026, all hand-written-from-scratch, none `-am`-on-an-AI-base. The single
  latest quote anywhere in the new bank is EXT 12/15 (Jul 13, and only because it is `-am` on his own
  research).
- **Source overlap with the old bank: near zero.** Only one paragraph is retained across both banks —
  the SDOH RCT-vs-observational paragraph (old EXT-13, new EXT-13), which was already early (Feb 25)
  and authentic. Every other new paragraph is new to the bank; every old late-2026 CORE/EXT pick was
  dropped.
- **The em-dash reversal.** The old bank advertised "zero em-dashes… a fact about his memo voice," and
  explicitly **dropped the MOOP two-by-two for using a dash.** That two-by-two is now CORE 3, and the
  new bank documents that his authentic memos use appositive em-dashes at roughly his academic rate.
  The "restraint" the old bank celebrated was AI polish, not his voice.
- **Typos and slips are now kept and flagged** (`counterfactural`, "tend to ones", "occurs only the
  rare cases", "which increases in out-of-pocket premiums") as positive evidence of hand-writing,
  rather than screened out.
- **New registers surfaced:** the principal-briefing voice ("You asked me…", "My read is…") from the
  Hassett and SDOH memos, and the market-structure *report* voice from the fall report — both absent
  from the old bank, both more academically resonant and more authentically his.

**One-line summary:** the new bank is almost entirely disjoint from the contaminated one, shifted from
a June–July 2026 AI-era selection to a December 2025–February 2026 hand-written selection, and it
reverses the old bank's central (false) claim that his memo voice is em-dash-free.

---

## Screening note (against ai-tells.md) — read differently from the old bank

This bank does **not** treat "passes the ai-tells screen" as the selection criterion; that criterion
is what produced the contaminated predecessor. Tells that are authentic to his hand are kept and
flagged, not excluded.

- **Em-dashes: present and intentional, but do not emulate their density.** CORE 1, 3, 5 and EXT 7,
  10, 12 carry appositive/definitional em-dashes, all authentic, all flagged. Keeping them corrects
  the old bank's false "zero-dash" signal (the appositive dash is genuinely his), per the
  flag-not-exclude rule shared with the academic banks. But the memo **drafting target is ~1 per 1,000
  words** (voice-registry): the corpus these are drawn from postdates his AI adoption and runs
  AI-inflated, so treat these dashes as evidence the construction is *authentic*, not as a *rate* to
  match. This is provisional pending the memo-dating run, which will gather a genuinely pre-AI sample.
- **Rhetorical questions: none in the quoted paragraphs.** (His authentic voice does use the occasional
  one — e.g., "Surely this reflects the value of insurance?" in the innovation memo — but none was
  needed to represent an archetype, so none is included.)
- **§1 "X, not Y":** every instance quoted ("not broad expansion", "not any particular category…is the
  best predictor", "is not a workaround; it is…", "not from the financing of care") is a full
  contrastive clause carrying a real fact — the permitted form, not a slogan.
- **§8 connectives / §14 hedges:** a few soft ones survive verbatim ("Moreover," "Finally,", "it is
  important to understand") and are flagged inline as authentic pre-AI hand signals, not models.
- **Typos:** kept verbatim and flagged (`counterfactural`, "tend to ones", "occurs only the rare
  cases", "which increases in out-of-pocket premiums") — authenticity signals, not to imitate.
- **Data hygiene:** every quoted paragraph is analytical/argumentative, free of PII/PHI and
  beneficiary-level data; sensitive pre-decisional sections (the MA "apparent deal", the personal-care
  fraud options, the ffs-bimodal editing dialogue) were read but not quoted (see Prioritization note).
